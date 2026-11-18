"""Replay independent research checks and verify the listed evidence files."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


def verify_lane(base, lane):
    for filename, digest in lane["evidence"].items():
        path = (base / filename).resolve()
        if not path.is_relative_to(base) or sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Evidence does not match: {filename}")
    script = lane["check"]
    if script not in lane["evidence"] or Path(script).suffix != ".py":
        raise ValueError(f"Missing pinned Python check: {script}")
    # Several scientific checks use assert. Keep them active under parent optimization.
    check_env = dict(os.environ, PYTHONOPTIMIZE="0")
    result = subprocess.run([sys.executable, "-B", str(base / script)], cwd=base,
                            env=check_env, check=True, capture_output=True)
    receipt = lane.get("stdout_matches")
    if receipt and (receipt not in lane["evidence"] or result.stdout != (base / receipt).read_bytes()):
        raise ValueError(f"Output differs from {receipt}")
    return lane["id"]


def verify_primary_sources(repo, pins, verified):
    for filename, expected in pins.items():
        key = (filename, expected)
        if key in verified:
            continue
        path = (repo / filename).resolve()
        if not path.is_relative_to(repo):
            raise ValueError(f"Primary source outside the checkout: {filename}")
        data = path.read_bytes()
        # The primary pins are object IDs from the shared SHA-1 Git repository.
        digest = sha1(f"blob {len(data)}\0".encode("ascii"))
        digest.update(data)
        if digest.hexdigest() != expected:
            raise ValueError(f"Primary Git blob does not match: {filename}")
        verified.add(key)


def main(manifests, workers=4):
    base = Path(__file__).resolve().parent
    # This pilot lives under 02_REGISTRY/research/sources in clones and exports.
    repo = base.parents[3]
    verified = set()
    lanes = []
    for manifest in manifests:
        portfolio = json.loads(Path(manifest).read_text(encoding="utf-8"))
        verify_primary_sources(repo, portfolio.get("primary_git_blobs_on_shared", {}), verified)
        lanes.extend(portfolio["lanes"])
    if not lanes or len({lane["id"] for lane in lanes}) != len(lanes):
        raise ValueError("Expected one unique entry per research lane")
    failed = False
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = {pool.submit(verify_lane, base, lane): lane["id"] for lane in lanes}
        for job in as_completed(jobs):
            name = jobs[job]
            try:
                print(f"PASS  {job.result()}", flush=True)
            except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
                print(f"FAIL  {name}: {exc}", file=sys.stderr)
                if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
                    sys.stderr.buffer.write(exc.stderr)
                failed = True
    return int(failed)


def verify_git_snapshot(revision, manifests, workers):
    """Run the committed verifier on the inputs declared at one revision."""
    pilot = Path(__file__).resolve().parent
    repo = pilot.parents[3]
    prefix = pilot.relative_to(repo)
    git = ["git", "-C", str(repo)]
    commit = subprocess.check_output(
        [*git, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}"],
        text=True).strip()
    names = [Path(path).resolve().relative_to(pilot) for path in manifests]

    def blob(path):
        return subprocess.check_output([*git, "cat-file", "blob", f"{commit}:{path.as_posix()}"])

    def relative_file(name):
        path = Path(name)
        if not path.parts or path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Expected a repository-relative file: {name}")
        return path

    files = {prefix / "verify_portfolio.py"}
    for name in names:
        path = prefix / name
        portfolio = json.loads(blob(path))
        files.add(path)
        files.update(relative_file(f) for f in portfolio.get("primary_git_blobs_on_shared", {}))
        for lane in portfolio["lanes"]:
            files.update(prefix / relative_file(f) for f in lane["evidence"])

    with TemporaryDirectory(prefix="d0-portfolio-") as folder:
        root = Path(folder)
        for path in sorted(files):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob(path))
        print(f"Git snapshot {commit}, {len(files)} committed files", flush=True)
        return subprocess.run(
            [sys.executable, "-B", "verify_portfolio.py", "--jobs", str(workers),
             *(str(name) for name in names)], cwd=root / prefix,
            env=dict(os.environ, PYTHONOPTIMIZE="0")).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="+", metavar="portfolio.json")
    parser.add_argument("--jobs", type=int, default=4, help="concurrent checks (default: 4)")
    parser.add_argument("--git-snapshot", metavar="REV",
                        help="replay the committed files of a self-contained portfolio")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    if args.git_snapshot:
        try:
            status = verify_git_snapshot(args.git_snapshot, args.manifests, args.jobs)
        except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
            parser.exit(1, f"Git snapshot verification failed: {exc}\n")
    else:
        status = main(args.manifests, args.jobs)
    sys.exit(status)
