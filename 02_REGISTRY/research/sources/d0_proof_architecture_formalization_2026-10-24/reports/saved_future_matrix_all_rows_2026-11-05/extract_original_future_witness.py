"""Opt-in single replay of pinned #334 selector; do not run during Lean builds.

This extracts the originally selected words only; it does not search for a new
witness, check eight primes, attest discovery, or prove the complex lower bound.
The caller must coordinate execution and provide an unused output directory.
"""
from __future__ import annotations

import argparse
import collections
import csv
import ctypes
import hashlib
import io
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import types

SELECTOR_GIT_BLOB = "d111c5bfeae3c384a4fe725f4a6d19277ea0005a"
SELECTOR_SHA256 = "1b1e75a8c46135eac9495bc47f9239b83ed36713c268d118d017ab176b95f3a5"
UNIFORM_GIT_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
UNIFORM_SHA256 = "1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9"
EXPECTED_WORDS_SHA256 = "7da6c5e307a8afac819f4096a8c173576b2498f9faede3e316ec21e7b0485e3a"
SOURCE_COMMIT = "eebcb5e467742df3e9cf7fa9702042d7294aa742"
EXPECTED_PRIME_DATA = (1009, 244, 626, 226, 278, 469)
MIN_AVAILABLE_BYTES = 4 * 1024**3
MIN_FREE_BYTES = 100 * 1024**2


class Refusal(Exception):
    pass


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # Never echo supplied arguments or an absolute executable path.
        raise Refusal("invalid command arguments")


def pin(path: pathlib.Path, expected_sha256: str, expected_blob: str) -> bytes:
    data = path.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if hashlib.sha256(data).hexdigest() != expected_sha256 or blob != expected_blob:
        raise Refusal("source pin mismatch")
    return data


def available_memory() -> int:
    class Status(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                    ("total_phys", ctypes.c_ulonglong), ("available_phys", ctypes.c_ulonglong),
                    ("total_page", ctypes.c_ulonglong), ("available_page", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong), ("available_virtual", ctypes.c_ulonglong),
                    ("available_extended", ctypes.c_ulonglong)]
    value = Status()
    value.length = ctypes.sizeof(value)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(value)):
        raise Refusal("memory availability check failed")
    return value.available_phys


def lean_build_running() -> bool:
    # Conservative point-in-time check; cannot prevent another process starting later.
    expression = ("$ErrorActionPreference='Stop'; $items = @((Get-CimInstance Win32_Process) | "
                  "Where-Object { $_.Name -in @('lean.exe','lake.exe') -or "
                  "$_.CommandLine -match '[l]ean_task_build[.]py' } | "
                  "Select-Object ProcessId,Name); ConvertTo-Json -InputObject $items -Compress")
    result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", expression],
                            capture_output=True, text=True, timeout=20, check=True)
    decoded = json.loads(result.stdout)
    if not isinstance(decoded, list):
        raise Refusal("build process check returned unexpected data")
    return bool(decoded)


def main() -> int:
    parser = SafeParser(prog="extract-pinned-selector", description=__doc__)
    parser.add_argument("--selector", type=pathlib.Path, required=True)
    parser.add_argument("--uniform", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True,
                        help="A new directory beneath an existing parent")
    parser.add_argument("--build-lock", type=pathlib.Path, required=True,
                        help="Existing d0-task-build.lock for the coordinated checkout")
    args = parser.parse_args()
    if os.name != "nt":
        raise Refusal("Windows resource checks required")
    import msvcrt
    # The repository build helper locks exactly this byte. Hold it through the
    # complete replay and publication; this does not coordinate other checkouts
    # or direct Lake invocations, which require external scheduling.
    if args.build_lock.name != "d0-task-build.lock":
        raise Refusal("unexpected build lock name")
    with args.build_lock.open("r+b") as lock:
        if os.fstat(lock.fileno()).st_size < 1:
            raise Refusal("build lock is empty")
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise Refusal("coordinated Lean build lock is held") from error
        try:
            return replay(args)
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def replay(args: argparse.Namespace) -> int:
    target = args.output_dir.absolute()
    if target.exists() or not target.parent.is_dir():
        raise Refusal("output directory must be absent and parent must exist")
    available = available_memory()
    if available < MIN_AVAILABLE_BYTES:
        raise Refusal("insufficient available physical memory")
    if shutil.disk_usage(target.parent).free < MIN_FREE_BYTES:
        raise Refusal("insufficient free disk space")
    if lean_build_running():
        raise Refusal("Lean build process detected")
    selector = pin(args.selector, SELECTOR_SHA256, SELECTOR_GIT_BLOB)
    pin(args.uniform, UNIFORM_SHA256, UNIFORM_GIT_BLOB)

    # Must be set before the trusted pinned source imports NumPy.
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[name] = "1"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    module = types.ModuleType("pinned_selector")
    module.__file__ = "pinned_selector.py"
    exec(compile(selector, "pinned_selector.py", "exec"), module.__dict__)
    if tuple(module.SPLIT_PRIMES[-1]) != EXPECTED_PRIME_DATA:
        raise Refusal("prime tuple mismatch")
    native = module.original_kraus_mod(EXPECTED_PRIME_DATA)
    ranks, words, pivots = module.actual_future_basis(native)
    if ranks != {1: 11, 2: 122, 3: 128} or len(words) != 128 or sorted(pivots) != list(range(128)):
        raise Refusal("selector result mismatch")
    if collections.Counter(map(len, words)) != {1: 11, 2: 111, 3: 6}:
        raise Refusal("word lengths mismatch")
    if any(any(type(slot) is not int or not 0 <= slot < 128 for slot in word) for word in words):
        raise Refusal("word slot out of range")
    if len({tuple(word) for word in words}) != 128:
        raise Refusal("duplicate words")
    canonical = json.dumps(words, separators=(",", ":")).encode("utf-8")
    if hashlib.sha256(canonical).hexdigest() != EXPECTED_WORDS_SHA256:
        raise Refusal("canonical witness digest mismatch")
    import numpy as np
    metadata = {"kind": "single-pinned-selector-extraction", "source_commit": SOURCE_COMMIT,
                "selector_git_blob": SELECTOR_GIT_BLOB, "selector_sha256": SELECTOR_SHA256,
                "uniform_git_blob": UNIFORM_GIT_BLOB, "uniform_sha256": UNIFORM_SHA256,
                "prime": 1009, "prime_tuple": list(EXPECTED_PRIME_DATA),
                "ranks_cumulative": ranks, "word_length_histogram": {"1": 11, "2": 111, "3": 6},
                "word_count": 128, "canonical_words_sha256": EXPECTED_WORDS_SHA256,
                "serialization": "UTF-8 json.dumps(words,separators=(',',':')); no trailing newline",
                "python": platform.python_version(), "numpy": np.__version__,
                "thread_limits": {name: os.environ[name] for name in
                    ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
                "available_memory_at_start_bytes": available, "wall_seconds": time.perf_counter()-wall_start,
                "process_cpu_seconds": time.process_time()-cpu_start,
                "scope": "One pinned 1009 selector replay; no eight-prime replay or complex Lean proof.",
                "resources_note": "The selected build lock is held; direct Lake and other checkouts require external coordination."}
    # Stage complete, mutually consistent files in a new sibling folder. Rename
    # is atomic on the same volume; never intentionally replace an existing target.
    stage = pathlib.Path(tempfile.mkdtemp(prefix=".d0-selector-", dir=target.parent))
    try:
        (stage / "histories.canonical.json").write_bytes(canonical)
        (stage / "selector-source.py").write_bytes(selector)
        (stage / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True)+"\n", encoding="utf-8")
        os.rename(stage, target)
    except Exception:
        # Leave the staging directory for inspection; never delete a computed path.
        raise
    print(json.dumps({"status": "success", "word_count": 128,
                      "canonical_words_sha256": EXPECTED_WORDS_SHA256}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Refusal as error:
        print(json.dumps({"status": "refused", "reason": str(error)}), file=sys.stderr)
        raise SystemExit(2)
    except Exception as error:
        # Exception text can contain local user paths; retain only its class.
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}), file=sys.stderr)
        raise SystemExit(1)
