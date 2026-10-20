#!/usr/bin/env python3
"""Replay the frozen compact flag-source and conditional HJR minimum packet.

This is a thin CI entrypoint. The original checkers and expected records remain
unchanged. It checks the declared compact archive source and the fixed-L8
collar/bulk negative direction, not native admission or full GR closure.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]

# Literal declarations are consumed by the existing changed-input selector.
INPUTS = [
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/flag_source.md",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/collar_minimum.md",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/check_flag_source.py",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/check_collar_minimum.py",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/FLAG_SOURCE_OUTPUT.txt",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/COLLAR_MINIMUM.json",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/SOURCE_PINS.json",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/fixed_collar_root_07f2.md",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/collar_hessian_07f2.json",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/wide_collar_root_5b5.md",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/wide_collar_5b5.json",
    "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/inputs/wide_collar_checker_5b5.txt",
]

PACKET_ROOT = ROOT / "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20"
INPUT_ROOT = PACKET_ROOT / "inputs"

PINNED_SHA256 = {
    "flag_source.md": "1dabc2596c64e4e3e789fc48a6a63c1a18657d17d44e4bab3f826caaa6d51b61",
    "collar_minimum.md": "3101eaef72eb741af8006171f32c26210ff2fc887a9c135d7b0722d7554fc23f",
    "check_flag_source.py": "ad7bf0a5984fa4632d1c2e00bc7a7cdb2817b8c4c6d8eccb3f437302a3f4827f",
    "check_collar_minimum.py": "ab26adddc3ce261a77644636c61bdc9dc9a9b3ca7bd88562dcc9d087bb933388",
    "FLAG_SOURCE_OUTPUT.txt": "430922ab58829a595064d94b03e588601b5379c16e6b9b330a7453fdaf0740d0",
    "COLLAR_MINIMUM.json": "dc5116220505fb991b50eab4c59a679c7271d8e15a172289af84680e9d775a60"
}

PINNED_INPUT_SHA256 = {
    "SOURCE_PINS.json": "196fa7bc5920084c1cbd88eb122b84e800751c8d9d7851009e8a31227357b59f",
    "fixed_collar_root_07f2.md": "60149e109412b7716384aca6e64091b8a67f3374c4dfa02b170df1182e58dd1d",
    "collar_hessian_07f2.json": "a38386a86af4be283631d42a890caf66c035c12a4f9d421037160550d36989f4",
    "wide_collar_root_5b5.md": "9d90121a775dac6bd1df49cea04d398b248ca118fcf871b00e166000dd5db735",
    "wide_collar_5b5.json": "dee20425e01aeba2f090a55e2b1d221d57160a667eff9240a1c58368cd87e305",
    "wide_collar_checker_5b5.txt": "1956aff0f6227a72c4afe3224db898b846581268794d41eab1170b581a72bf28"
}


def verify_inputs() -> None:
    declared = {str((PACKET_ROOT / name).relative_to(ROOT)) for name in PINNED_SHA256}
    declared.update(str((INPUT_ROOT / name).relative_to(ROOT)) for name in PINNED_INPUT_SHA256)
    if set(INPUTS) != declared:
        raise AssertionError("Declared input paths and exact hash pins differ")
    for name, expected in PINNED_SHA256.items():
        path = PACKET_ROOT / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"Input hash mismatch: {path.relative_to(ROOT)}: {actual} != {expected}")
    for name, expected in PINNED_INPUT_SHA256.items():
        path = INPUT_ROOT / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"Input hash mismatch: {path.relative_to(ROOT)}: {actual} != {expected}")


def run_checker(relative: str, *arguments: str) -> str:
    result = subprocess.run(
        [sys.executable, "-B", "-W", "error", str(ROOT / relative), *arguments],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, result.args)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.stdout


def main() -> None:
    verify_inputs()
    flag_output = run_checker(
        "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/check_flag_source.py"
    )
    expected_flag = (
        ROOT / "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/FLAG_SOURCE_OUTPUT.txt"
    ).read_text(encoding="utf-8")
    if flag_output != expected_flag:
        raise AssertionError("Full flag-source output differs from the frozen scientific record")
    print("PASS complete stopped CAR16 flag-source replay matches its immutable output")

    collar_output = run_checker(
        "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/check_collar_minimum.py",
        "--root", str(ROOT),
    )
    expected_collar = json.loads((
        ROOT / "02_REGISTRY/research/sources/d0_native_flag_source_minimum_2026-10-20/COLLAR_MINIMUM.json"
    ).read_text(encoding="utf-8"))
    if json.loads(collar_output) != expected_collar:
        raise AssertionError("Collar/bulk minimum result differs from the frozen scientific record")
    print("PASS exact fixed-L8 collar/bulk negative-direction replay matches its immutable result")

    verify_inputs()
    print("PASS all 12 scientific input/output hash pins remain unchanged after replay")
    print("SCOPE: conditional compact flag first source and fixed-L8 HJR minimum gate; full native price and GR remain open.")


if __name__ == "__main__":
    main()
