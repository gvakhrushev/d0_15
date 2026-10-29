#!/usr/bin/env python3
"""Serialized Lean task build helper.

Use narrow builds while iterating and exactly one final D0.All build per unchanged
source tree. The helper rejects concurrent builds sharing the same .lake cache and
invalidates a result if Lean sources changed while the build was running.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import time
from contextlib import contextmanager

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORMAL = ROOT / "03_FORMALIZATION"
LAKE = FORMAL / ".lake"
LOCK = LAKE / "d0-task-build.lock"
STAMP = LAKE / "d0-final-build-receipt.json"


def _tracked_lean_symlink_targets() -> dict[str, tuple[bytes, pathlib.Path]]:
    """Return project Lean symlink entries and their checked-in target text.

    On Windows, Git commonly checks a symlink out as a regular file containing
    the link target. Lake then tries to parse that path as Lean source. Keep the
    target bytes from Git's index so both the digest and the temporary build
    view can use the source that a symlink-capable checkout reads.
    """
    try:
        entries = subprocess.check_output(
            ["git", "ls-files", "--stage", "-z", "--", "03_FORMALIZATION"],
            cwd=ROOT,
        )
    except (OSError, subprocess.CalledProcessError):
        return {}

    targets: dict[str, tuple[bytes, pathlib.Path]] = {}
    for entry in entries.split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, blob_sha, stage = metadata.split()
        if mode != b"120000" or stage != b"0" or not raw_path.endswith(b".lean"):
            continue
        relative = os.fsdecode(raw_path)
        link_text = subprocess.check_output(
            ["git", "cat-file", "blob", os.fsdecode(blob_sha)], cwd=ROOT
        )
        link_target = pathlib.Path(os.fsdecode(link_text))
        link_path = ROOT / pathlib.Path(relative)
        target_path = (link_path.parent / link_target).resolve(strict=True)
        try:
            target_path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise RuntimeError(
                f"tracked Lean symlink escapes the repository: {relative} -> {link_target}"
            ) from exc
        if not target_path.is_file():
            raise RuntimeError(
                f"tracked Lean symlink target is not a file: {relative} -> {link_target}"
            )
        targets[relative] = (link_text, target_path)
    return targets


@contextmanager
def materialize_windows_lean_symlinks(enabled=None):
    """Temporarily expose tracked Lean symlink targets to native Windows Lake."""
    if enabled is None:
        enabled = os.name == "nt"
    if not enabled:
        yield
        return

    materialized: list[tuple[pathlib.Path, bytes]] = []
    try:
        for relative, (link_text, target_path) in _tracked_lean_symlink_targets().items():
            link_path = ROOT / pathlib.Path(relative)
            if link_path.is_symlink():
                continue
            current = link_path.read_bytes()
            target_bytes = target_path.read_bytes()
            if current == target_bytes:
                # Recover from an earlier interrupted process that left the
                # temporary dereferenced bytes in place.
                materialized.append((link_path, link_text))
                continue
            if current != link_text:
                raise RuntimeError(
                    f"tracked Lean symlink placeholder has local edits: {relative}"
                )
            materialized.append((link_path, current))
            link_path.write_bytes(target_bytes)
        yield
    finally:
        for link_path, link_text in reversed(materialized):
            link_path.write_bytes(link_text)


def _source_bytes(path: pathlib.Path, symlink_targets: dict[str, tuple[bytes, pathlib.Path]]) -> bytes:
    """Read the bytes Lean sees, including a dereferenced Windows symlink."""
    source = path.read_bytes()
    try:
        relative = path.relative_to(ROOT).as_posix()
    except ValueError:
        return source
    target = symlink_targets.get(relative)
    if target is None or path.is_symlink():
        return source
    link_text, target_path = target
    if source == link_text:
        return target_path.read_bytes()
    if source == target_path.read_bytes():
        return source
    raise RuntimeError(f"tracked Lean symlink placeholder has local edits: {relative}")


class BuildLockBusy(Exception):
    """Raised when another process owns the shared Lake build cache."""


@contextmanager
def build_lock(path: pathlib.Path):
    """Lock one byte without truncating the persistent lock file.

    POSIX uses flock; Windows uses the CRT byte-range lock. Both are
    non-blocking so concurrent build attempts fail before starting Lake.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as lock:
        lock.seek(0, os.SEEK_END)
        if lock.tell() == 0:
            lock.write(b"\0")
            lock.flush()
        lock.seek(0)

        if os.name == "nt":
            import msvcrt

            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                if exc.errno in {13, 36} or getattr(exc, "winerror", None) in {33, 36}:
                    raise BuildLockBusy from exc
                raise
            try:
                yield
            finally:
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise BuildLockBusy from exc
            try:
                yield
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def source_digest() -> str:
    h = hashlib.sha256()
    # Project sources and Lake configuration only. The separate dependency
    # and environment receipt binds manifest pins, revalidates actual package
    # checkouts before/after a build and records its toolchain trust boundary.
    files = sorted(
        p for p in FORMAL.rglob("*.lean")
        if ".lake" not in p.relative_to(FORMAL).parts
    )
    for extra in ("lakefile.lean", "lakefile.toml", "lake-manifest.json", "lean-toolchain"):
        p = FORMAL / extra
        if p.exists():
            files.append(p)
    symlink_targets = _tracked_lean_symlink_targets()
    for p in sorted(set(files)):
        h.update(p.relative_to(FORMAL).as_posix().encode())
        h.update(b"\0")
        h.update(_source_bytes(p, symlink_targets).replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
        h.update(b"\0")
    return h.hexdigest()



class DependencyProvenanceError(RuntimeError):
    """The actual Lake dependency sources cannot be tied to the manifest."""


def _git_bytes(package: pathlib.Path, *args: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(package), *args], stderr=subprocess.PIPE
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DependencyProvenanceError(
            f"cannot verify dependency checkout {package}: {' '.join(args)}"
        ) from exc


def _safe_relative_path(value: str, kind: str) -> pathlib.Path:
    path = pathlib.PurePosixPath(value)
    if not value or path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        raise DependencyProvenanceError(f"invalid {kind}: {value!r}")
    return pathlib.Path(*path.parts)


def dependency_provenance() -> dict:
    """Verify actual git package checkouts at this instant, fail closed.

    Checks bracket a build/extraction, not every instant within it. `.lake`
    binary caches, downloaded build products and the actual executable bytes
    of the toolchain are not authenticated by this source-only check.
    """
    manifest_path = FORMAL / "lake-manifest.json"
    try:
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes)
        package_dir = _safe_relative_path(manifest["packagesDir"], "packagesDir")
        packages = manifest["packages"]
        if not isinstance(packages, list):
            raise ValueError("packages must be a list")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise DependencyProvenanceError("cannot parse Lake dependency manifest") from exc

    root = FORMAL.resolve()
    package_root = (FORMAL / package_dir).resolve()
    if not package_root.is_relative_to(root):
        raise DependencyProvenanceError("package directory escapes formalization root")
    verified = []
    names = set()
    for record in packages:
        if not isinstance(record, dict) or record.get("type") != "git":
            raise DependencyProvenanceError("only manifest-pinned git dependencies are supported")
        name, revision = record.get("name"), record.get("rev")
        if (not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", name)
                or name in names or not isinstance(revision, str)
                or not re.fullmatch(r"[0-9a-fA-F]{40,64}", revision)):
            raise DependencyProvenanceError("invalid dependency name or pinned revision")
        names.add(name)
        package = (package_root / name).resolve()
        if not package.is_relative_to(package_root) or not package.is_dir():
            raise DependencyProvenanceError(f"missing or escaped dependency checkout: {name}")
        top = pathlib.Path(os.fsdecode(_git_bytes(package, "rev-parse", "--show-toplevel").strip())).resolve()
        if top != package:
            raise DependencyProvenanceError(f"not an independent git checkout: {name}")
        head = _git_bytes(package, "rev-parse", "--verify", "HEAD").decode("ascii").strip().lower()
        if head != revision.lower():
            raise DependencyProvenanceError(f"dependency HEAD differs from manifest: {name}")
        try:
            status = subprocess.run(
                ["git", "-C", str(package), "diff", "--no-ext-diff", "--ignore-submodules=none",
                 "--quiet", "HEAD", "--"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
            )
        except OSError as exc:
            raise DependencyProvenanceError(f"cannot inspect dependency changes: {name}") from exc
        if status.returncode:
            raise DependencyProvenanceError(f"dependency tracked files changed or cannot be checked: {name}")
        # Index flags can hide a local edit from git diff. Reject such checkouts.
        flags = _git_bytes(package, "ls-files", "-v", "-z")
        for entry in flags.split(b"\0"):
            if entry and (entry[:1] == b"S" or entry[:1].islower()):
                raise DependencyProvenanceError(f"dependency index has hidden-worktree flags: {name}")
        entries = _git_bytes(package, "ls-files", "--stage", "-z")
        tracked = set()
        links = []
        for entry in entries.split(b"\0"):
            if not entry:
                continue
            metadata, path_bytes = entry.split(b"\t", 1)
            mode, blob, stage = metadata.split()
            path = os.fsdecode(path_bytes)
            if stage != b"0" or mode == b"160000":
                raise DependencyProvenanceError(f"unmerged or nested git dependency: {name}")
            tracked.add(path)
            # Do not trust only Git's stat cache: an edit with preserved metadata
            # can otherwise be missed. Check the actual checkout bytes against
            # the staged blob. This deliberately rejects transformed checkout
            # bytes, such as CRLF, rather than certifying unverified inputs.
            actual_path = package / path
            try:
                file_stat = actual_path.lstat()
                if mode == b"120000":
                    if stat.S_ISLNK(file_stat.st_mode):
                        data = os.fsencode(os.readlink(actual_path))
                    elif os.name == "nt" and stat.S_ISREG(file_stat.st_mode):
                        data = actual_path.read_bytes()
                    else:
                        raise DependencyProvenanceError(f"dependency symlink type changed: {name}/{path}")
                elif mode in (b"100644", b"100755") and stat.S_ISREG(file_stat.st_mode):
                    if os.name != "nt" and bool(file_stat.st_mode & 0o111) != (mode == b"100755"):
                        raise DependencyProvenanceError(f"dependency executable mode changed: {name}/{path}")
                    data = actual_path.read_bytes()
                else:
                    raise DependencyProvenanceError(f"unsupported dependency file type: {name}/{path}")
            except OSError as exc:
                raise DependencyProvenanceError(f"cannot read dependency file: {name}/{path}") from exc
            algorithm = "sha1" if len(blob) == 40 else "sha256" if len(blob) == 64 else None
            if algorithm is None:
                raise DependencyProvenanceError(f"unsupported Git object format: {name}")
            actual_blob = hashlib.new(algorithm, b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
            if actual_blob.encode("ascii") != blob:
                raise DependencyProvenanceError(f"dependency bytes differ from pinned Git blob: {name}/{path}")
            if mode == b"120000":
                links.append((path, blob))
        for path, blob in links:
            link_text = os.fsdecode(_git_bytes(package, "cat-file", "blob", os.fsdecode(blob)))
            try:
                target = ((package / path).parent / link_text).resolve(strict=True)
                target_name = target.relative_to(package).as_posix()
            except (OSError, ValueError) as exc:
                raise DependencyProvenanceError(f"dependency symlink escapes or is missing: {name}/{path}") from exc
            if target_name not in tracked or not target.is_file():
                raise DependencyProvenanceError(f"dependency symlink target is not tracked: {name}/{path}")
        for ignored in (False, True):
            cmd = ["ls-files", "--others"]
            if ignored:
                cmd.append("--ignored")
            # Lake's generated build tree contains generated C and setup JSON.
            # It is a cache outside this source attestation, not dependency source.
            # An arbitrary untracked filename can be consumed by Lake scripts.
            # Reject all such files, rather than guessing source suffixes.
            cmd += ["--exclude-standard", "-z", "--", ".", ":(exclude).lake/build/**",
                    ":(exclude).lake/build.barrel", ":(exclude).lake/build.barrel.trace",
                    ":(exclude)widget/package-lock.json.hash"]
            files = _git_bytes(package, *cmd)
            # Ignored Lean files inside .lake may be source roots even if most
            # of .lake is generated cache. Do not silently exclude them.
            internal_lean = _git_bytes(
                package, "ls-files", "--others", *( ["--ignored"] if ignored else [] ),
                "--exclude-standard", "-z", "--", ".lake/build/**/*.lean"
            )
            if any(files.split(b"\0")) or any(internal_lean.split(b"\0")):
                raise DependencyProvenanceError(f"untracked or ignored dependency source/config: {name}")
        verified.append({"name": name, "revision": head})
    return {
        "schema": "d0-lake-dependency-provenance-v1",
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "packages": sorted(verified, key=lambda row: row["name"]),
        "checks": "git HEAD, exact tracked checkout bytes and modes against index blobs, index flags, symlink targets, untracked/ignored files outside listed caches, Lean sources inside build cache",
        "boundary": "point-in-time source checks; generated .lake/build caches (except Lean source), .lake/build.barrel[.trace] and widget/package-lock.json.hash not authenticated",
    }


def dependency_provenance_digest(snapshot: dict) -> str:
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def build_environment_digest() -> str:
    # External source search paths could change without changing their spelling.
    if any(os.environ.get(key) for key in ("LEAN_PATH", "LEAN_SRC_PATH")):
        raise DependencyProvenanceError("external LEAN_PATH/LEAN_SRC_PATH is not attested")
    selected = {key: value for key, value in os.environ.items()
                if key.startswith(("LEAN_", "LAKE_", "ELAN_")) or key == "PATH"}
    return hashlib.sha256(json.dumps(selected, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _tool_command(command: list[str]) -> dict:
    try:
        proc = subprocess.run(command, cwd=FORMAL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=30, check=False)
        stdout, stderr = proc.stdout.decode("utf-8", errors="strict").strip(), proc.stderr.decode("utf-8", errors="strict").strip()
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        raise DependencyProvenanceError(f"cannot identify toolchain: {command[0]}") from exc
    if proc.returncode != 0 or not stdout:
        raise DependencyProvenanceError(f"toolchain command failed: {command!r}; stderr={stderr}")
    return {"command": command, "stdout": stdout, "stderr": stderr}


def _executable(path: str) -> dict[str, str]:
    try:
        resolved = pathlib.Path(path).resolve(strict=True)
        if not resolved.is_file() or not os.access(resolved, os.X_OK):
            raise OSError("not an executable regular file")
        h = hashlib.sha256()
        with resolved.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(chunk)
    except OSError as exc:
        raise DependencyProvenanceError(f"cannot read selected executable: {path}") from exc
    return {"resolved_path": str(resolved), "sha256": h.hexdigest()}


def toolchain_snapshot() -> dict:
    """Bind selected binary bytes and observed versions, not runtime libraries."""
    launcher = {name: shutil.which(name) for name in ("lean", "lake")}
    if any(path is None for path in launcher.values()):
        raise DependencyProvenanceError("lean and lake must both be available on PATH")
    elan = shutil.which("elan")
    result = {"resolution": "elan which" if elan else "PATH",
              "launchers": {name: _executable(path) for name, path in launcher.items()}}
    if elan:
        result["elan"] = _executable(elan)
        selected = {}
        for name in ("lean", "lake"):
            lookup = _tool_command([elan, "which", name])
            if ("\n" in lookup["stdout"] or "\r" in lookup["stdout"]
                    or not pathlib.Path(lookup["stdout"]).is_absolute()):
                raise DependencyProvenanceError(f"ambiguous elan executable path: {name}")
            selected[name] = {**_executable(lookup["stdout"]), "resolution_stderr": lookup["stderr"]}
    else:
        # An Elan shim without Elan available cannot identify its actual binary.
        if any(pathlib.Path(info["resolved_path"]).name.lower().startswith("elan")
               for info in result["launchers"].values()):
            raise DependencyProvenanceError("Elan shim cannot resolve its selected toolchain")
        selected = result["launchers"]
    result["selected"] = selected
    result["lean_version"] = _tool_command([launcher["lake"], "env", "lean", "--version"])
    result["lake_version"] = _tool_command([launcher["lake"], "--version"])
    result["boundary"] = "selected executable bytes and reported versions at two snapshots; dynamic libraries, kernel, external settings and generated caches are not authenticated"
    return result


def run_locked(command: list[str], target: str, *, final: bool = False, force: bool = False) -> int:
    LAKE.mkdir(parents=True, exist_ok=True)
    try:
        with build_lock(LOCK):
            with materialize_windows_lean_symlinks():
                toolchain_before = toolchain_snapshot()
                before = source_digest()
                dependencies_before = dependency_provenance()
                dependency_digest = dependency_provenance_digest(dependencies_before)
                environment_before = build_environment_digest()
                receipt = {"schema": "d0-lean-build-receipt-v1", "target": target, "command": command,
                           "source_sha256": before, "dependency_sha256": dependency_digest,
                           "environment_sha256": environment_before, "dependencies": dependencies_before,
                           "toolchain": toolchain_before}
                if final and not force and STAMP.exists():
                    try:
                        existing = json.loads(STAMP.read_text(encoding="utf-8"))
                    except (OSError, ValueError):
                        existing = None
                    if existing == receipt:
                        print("SKIP: this exact Lean source and dependency snapshot already passed final D0.All.")
                        print("D0_BUILD_RECEIPT " + json.dumps(receipt, sort_keys=True))
                        return 0
                # A failed or interrupted replacement cannot leave a success stamp.
                if final:
                    STAMP.unlink(missing_ok=True)
                started = time.monotonic()
                proc = subprocess.run(command, cwd=FORMAL)
                elapsed = time.monotonic() - started
                toolchain_after = toolchain_snapshot()
                after = source_digest()
                dependencies_after = dependency_provenance()
                environment_after = build_environment_digest()
            print(f"D0_BUILD target={target} seconds={elapsed:.1f} returncode={proc.returncode}")
            if before != after:
                print(
                    "INVALID_BUILD: Lean sources changed while lake was running. "
                    "The build may have compiled an obsolete file; rerun after edits stop.",
                    file=sys.stderr,
                )
                return 3
            if (dependencies_before != dependencies_after or environment_before != environment_after
                    or toolchain_before != toolchain_after):
                print("INVALID_BUILD: dependency or toolchain inputs changed while lake was running.", file=sys.stderr)
                return 3
            if proc.returncode == 0:
                if final:
                    # Under the build lock; replace only a complete receipt.
                    temporary = STAMP.with_name(STAMP.name + ".tmp")
                    temporary.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
                    temporary.replace(STAMP)
                print("D0_BUILD_RECEIPT " + json.dumps(receipt, sort_keys=True))
            return proc.returncode
    except BuildLockBusy:
        print(
            "REFUSE: another D0 Lean build already owns the shared .lake cache; "
            "do not start a second lake process.",
            file=sys.stderr,
        )
        return 2
    except (DependencyProvenanceError, OSError, RuntimeError) as exc:
        print(f"INVALID_BUILD: cannot verify build inputs: {exc}", file=sys.stderr)
        return 3


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)

    narrow = sub.add_parser("narrow")
    narrow.add_argument("target")

    cache = sub.add_parser("cache")
    cache.add_argument("targets", nargs="*", help="Lean modules/files whose Mathlib cache is needed")

    final = sub.add_parser("final")
    final.add_argument("--force", action="store_true")

    args = ap.parse_args()

    if args.mode == "narrow":
        if args.target in {"D0", "D0.All"}:
            print("REFUSE: use 'final' for D0.All; iterate on one narrow module target.", file=sys.stderr)
            return 2
        return run_locked(["lake", "build", args.target], args.target)

    if args.mode == "cache":
        return run_locked(["lake", "exe", "cache", "get", *args.targets], "mathlib-cache-get")

    return run_locked(["lake", "build", "D0.All"], "D0.All", final=True, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
