#!/usr/bin/env python3
"""Focused finite checks for the tower/source synthesis, not a GR certificate."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_tower_heat_synthesis_2026-10-15"
sys.path.insert(0, str(SOURCE))

from tower_trace import run_checks as tower_checks
from information_geometry import run_checks as information_checks


def main():
    original = SOURCE / "INPUT_D0_SINTEZ_BASHNYA_PHI_PREDEL.html"
    digest = hashlib.sha256(original.read_bytes()).hexdigest()
    if digest != "cc327e05d246a86847248c690469aae47cab3c27f68d49c9c9d4500dc1f3a84b":
        raise ValueError("Original user proposal bytes changed")
    proof = SOURCE / "HEAT_JOINT_LIMIT_PROOF.md"
    if not proof.is_file():
        raise ValueError("Analytic heat-limit proof is missing")
    result = {
        "input_sha256": digest,
        "tower": tower_checks(),
        "information_geometry": information_checks(ROOT),
        "heat_limit": "analytic proof in HEAT_JOINT_LIMIT_PROOF.md; not established by finite checks",
        "scope": "specified AF tower and diagnostic instrument; native binding and GR remain open",
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
