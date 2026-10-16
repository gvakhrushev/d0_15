#!/usr/bin/env python3
"""Replay research certificates from one committed snapshot in isolated worktrees.

Local uncommitted edits are never copied. Each certificate gets a fresh detached
worktree; generators may create untracked products but must not change tracked
files or the checked commit. Logs are evidence, never a reusable result cache.
"""
from __future__ import annotations

import argparse
from concurrent.futures import CancelledError, ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = "02_REGISTRY/research/certificates"
TIMEOUT_DECL = re.compile(r"# D0_CI_TIMEOUT_SECONDS=([0-9]+)")


class ReplayCancelled(Exception):
    def __init__(self, signum: int):
        self.signum = signum
        super().__init__(f"Research replay cancelled by signal {signum}")


def stop_process_group(process: subprocess.Popen) -> None:
    # The leader may already have exited while descendants still hold its group.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=5)


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def certificate_timeout(source: str) -> int:
    declarations = [
        int(match[1])
        for line in source.splitlines()[:40]
        if (match := TIMEOUT_DECL.fullmatch(line))
    ]
    if len(declarations) > 1:
        raise ValueError("Multiple D0_CI_TIMEOUT_SECONDS declarations")
    seconds = declarations[0] if declarations else 180
    if not 180 <= seconds <= 1800:
        raise ValueError(f"Invalid research-certificate timeout {seconds}s; allowed range is 180..1800")
    return seconds


def select_certificates(repo: Path, commit: str, base: str | None) -> list[str]:
    if base is None:
        names = git(repo, "ls-tree", "-r", "--name-only", "-z", commit, "--", CERT_DIR)
    else:
        names = git(repo, "diff", "--name-only", "-z", "--diff-filter=ACMR", base, commit,
                    "--", f"{CERT_DIR}/*.py")
    return sorted({os.fsdecode(name) for name in names.split(b"\0")
                   if name and os.fsdecode(name).endswith(".py")})


def run_certificate(repo: Path, commit: str, cert: str, log_dir: Path,
                    cancelled: threading.Event | None = None) -> dict:
    cancelled = cancelled or threading.Event()
    started = time.monotonic()
    result = {"certificate": cert, "commit": commit, "status": "ERROR", "returncode": None}
    relative = PurePosixPath(cert).relative_to(CERT_DIR)
    if ".." in relative.parts or relative.suffix != ".py":
        raise ValueError("Invalid research-certificate path")
    logs = log_dir / f"{relative.stem}-{hashlib.sha256(cert.encode()).hexdigest()[:10]}"
    logs.mkdir(parents=True)
    result["logs"] = str(logs)
    try:
        if cancelled.is_set():
            raise CancelledError()
        # One checkout per certificate also isolates generators with common outputs.
        with tempfile.TemporaryDirectory(prefix="d0-research-cert-") as temp:
            sandbox = Path(temp).resolve() / "tree"
            try:
                git(repo, "worktree", "add", "--detach", str(sandbox), commit)
                source = sandbox / cert
                if not source.resolve().is_relative_to(sandbox):
                    raise ValueError("Certificate must resolve inside its isolated worktree")
                seconds = certificate_timeout(source.read_text(encoding="utf-8"))
                result["timeout_seconds"] = seconds
                if cancelled.is_set():
                    raise CancelledError()
                with (logs / "stdout.log").open("wb") as stdout, (logs / "stderr.log").open("wb") as stderr:
                    process = subprocess.Popen(
                        [sys.executable, str(source)], cwd=sandbox,
                        env={**os.environ, "PYTHONHASHSEED": "0"},
                        stdout=stdout, stderr=stderr, start_new_session=True,
                    )
                    try:
                        deadline = time.monotonic() + seconds
                        while True:
                            if cancelled.is_set():
                                result["status"] = "CANCELLED"
                                break
                            remaining = deadline - time.monotonic()
                            if remaining <= 0:
                                result.update(status="TIMEOUT", returncode=124)
                                break
                            try:
                                result["returncode"] = process.wait(timeout=min(0.1, remaining))
                                result["status"] = "PASS" if process.returncode == 0 else "FAIL"
                                break
                            except subprocess.TimeoutExpired:
                                continue
                    finally:
                        stop_process_group(process)

                status = git(sandbox, "status", "--porcelain=v1", "--untracked-files=no")
                head = git(sandbox, "rev-parse", "HEAD").decode().strip()
                (logs / "tracked-status.txt").write_bytes(status)
                (logs / "tracked.patch").write_bytes(
                    git(sandbox, "diff", "--no-ext-diff", "--binary", commit, "--"))
                (logs / "index.patch").write_bytes(
                    git(sandbox, "diff", "--no-ext-diff", "--binary", "--cached", commit, "--"))
                result["head_after"] = head
                result["tracked_mutation"] = bool(status or head != commit)
                if result["tracked_mutation"]:
                    result["execution_status"] = result["status"]
                    result["status"] = "MUTATION"
            finally:
                if sandbox.exists():
                    git(repo, "worktree", "remove", "--force", str(sandbox))
    except CancelledError:
        result["status"] = "CANCELLED"
    except Exception as error:
        result.update(status="ERROR", error=str(error))
        if isinstance(error, subprocess.CalledProcessError):
            (logs / "git-error.log").write_bytes(error.stderr or b"")
    result["duration_seconds"] = round(time.monotonic() - started, 3)
    return result


def replay(repo: Path, commit: str, certs: list[str], workers: int, log_dir: Path) -> list[dict]:
    log_dir.mkdir(parents=True, exist_ok=False)
    print(f"Research snapshot {commit}: {len(certs)} certificate(s), workers={workers}", flush=True)
    results = {}
    cancelled = threading.Event()
    received_signal = 0
    old_handlers = {}

    def request_cancel(signum, _frame):
        nonlocal received_signal
        received_signal = received_signal or signum
        cancelled.set()

    if threading.current_thread() is threading.main_thread():
        for signum in (signal.SIGINT, signal.SIGTERM):
            old_handlers[signum] = signal.signal(signum, request_cancel)
    pool = ThreadPoolExecutor(max_workers=workers)
    pending = {}
    try:
        for cert in certs:
            if cancelled.is_set():
                break
            pending[pool.submit(run_certificate, repo, commit, cert, log_dir, cancelled)] = cert
        for future in as_completed(pending):
            result = future.result()
            results[result["certificate"]] = result
            print(f"::group::{result['status']}: {result['certificate']}", flush=True)
            for name, stream in (("stdout.log", sys.stdout), ("stderr.log", sys.stderr)):
                path = Path(result["logs"]) / name
                if path.exists():
                    stream.write(path.read_bytes().decode("utf-8", errors="replace"))
                    stream.write("\n")
                    stream.flush()
            if result.get("error"):
                print(result["error"], file=sys.stderr, flush=True)
            print(f"{result['status']} rc={result['returncode']} logs={result['logs']}\n::endgroup::", flush=True)
            if cancelled.is_set():
                break
    finally:
        try:
            if sys.exc_info()[0] is not None:
                cancelled.set()
            # Running workers observe the event within 0.1s; queued work is cancelled.
            pool.shutdown(wait=True, cancel_futures=True)
            for future, cert in pending.items():
                if not future.cancelled() and cert not in results:
                    results[cert] = future.result()
            for cert in certs:
                if cert not in results:
                    results[cert] = {"certificate": cert, "commit": commit, "status": "CANCELLED", "returncode": None}
            ordered = sorted(results.values(), key=lambda item: item["certificate"])
            (log_dir / "results.json").write_text(
                json.dumps({"commit": commit, "workers": workers, "signal": received_signal,
                            "results": ordered}, indent=2) + "\n", encoding="utf-8")
        finally:
            for signum, handler in old_handlers.items():
                signal.signal(signum, handler)
    if received_signal:
        raise ReplayCancelled(received_signal)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--ref", default="HEAD", help="committed snapshot; working edits are omitted")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--base", help="replay cumulative changed certificates against this commit/ref")
    scope.add_argument("--all", action="store_true", help="replay every tracked research certificate")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--log-dir", type=Path, help="new directory for complete logs and mutation diagnostics")
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be in 1..8")
    try:
        commit = git(args.repo, "rev-parse", "--verify", f"{args.ref}^{{commit}}").decode().strip()
        base = (git(args.repo, "rev-parse", "--verify", f"{args.base}^{{commit}}").decode().strip()
                if args.base else None)
        if git(args.repo, "status", "--porcelain=v1", "--untracked-files=no"):
            print("Tracked working edits are omitted; replay uses committed snapshot " + commit, flush=True)
        certs = select_certificates(args.repo, commit, base)
        log_dir = args.log_dir or args.repo / ".build/research-certificates" / f"{commit[:12]}-{uuid.uuid4().hex[:8]}"
        results = replay(args.repo.resolve(), commit, certs, args.workers, log_dir.resolve())
    except ReplayCancelled as error:
        print(error, file=sys.stderr)
        return 128 + error.signum
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Research replay error: {error}", file=sys.stderr)
        return 1
    return int(any(result["status"] != "PASS" for result in results))


if __name__ == "__main__":
    sys.exit(main())
