"""Compare compiled Julia endpoints with the pinned original constructor."""
from __future__ import annotations

import hashlib
import itertools
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / ".git").exists())
CHECKER = (
    "02_REGISTRY/research/sources/d0_proof_architecture_car_creator_bridge_2026-11-04/"
    "check_future_even_algebra_modprime.py"
)
REVISION = "a358e91e764655b16082bf7e6161a79df96a24a6"
CHECKER_SHA = "1b1e75a8c46135eac9495bc47f9239b83ed36713c268d118d017ab176b95f3a5"
ROWS_SHA = "bc59ee384e3edc1b8d6419fdf5260f5a6a80303ffd599e6b0ae6020553fdee59"


def original_words():
    source = subprocess.check_output(["git", "show", f"{REVISION}:{CHECKER}"], cwd=ROOT)
    if hashlib.sha256(source).hexdigest() != CHECKER_SHA:
        raise ValueError("Original constructor digest mismatch")
    owner = {"__name__": "original_julia_fixture"}
    exec(compile(source, CHECKER, "exec"), owner)
    constructor = owner["original_kraus_mod"]
    split = (1009, 244, 626, 226, 278, 469)
    if split not in owner["SPLIT_PRIMES"]:
        raise ValueError("Missing reference split")
    words = []

    # The public return contains the later Kraus instruments. Capture the
    # intermediate endpoint table of this specific unmodified constructor.
    def returning(frame, event, _):
        if event == "return":
            words.extend(frame.f_locals["words"])
        return returning

    def enter(frame, event, _):
        if event == "call" and frame.f_code is constructor.__code__:
            return returning
        return None

    previous = sys.gettrace()
    try:
        sys.settrace(enter)
        constructor(split)
    finally:
        sys.settrace(previous)
    if len(words) != 32:
        raise ValueError(f"Expected 32 original words, received {len(words)}")
    return words


def compare(output):
    words = original_words()
    lines = output.splitlines()
    if len(lines) != 1024:
        raise ValueError(f"Expected 1024 Lean rows, received {len(lines)}")
    indices = itertools.product((469, 540), range(4), range(4), range(2), range(16))
    for line, key in zip(lines, indices):
        imaginary, mode, row, port, bra = key
        actual = [int(entry) for entry in line.split(",")]
        real, imag = words[8 * mode + 2 * row][port]
        expected = [int((real[bra, j] + imaginary * imag[bra, j]) % 1009) for j in range(16)]
        if actual != expected:
            raise ValueError(f"Endpoint mismatch at {key}")
    digest = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    if digest != ROWS_SHA:
        raise ValueError(f"Unexpected canonical row digest {digest}")
    print(f"Matched 16384 field entries; canonical rows SHA-256 {digest}")


def main():
    output = subprocess.check_output(
        ["lake", "env", "lean", str(HERE / "EvaluatePairs.lean")],
        cwd=ROOT / "03_FORMALIZATION",
        text=True,
    )
    compare(output)


if __name__ == "__main__":
    main()
