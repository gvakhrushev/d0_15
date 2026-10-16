#!/usr/bin/env python3
"""Exact record-source pullback and one literal joint-equation consumer."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_record_source_pullback_2026-10-15"
sys.path.insert(0, str(SOURCE))

from check_record_source import run_checks as source_checks
from joint_compatibility import run_checks as compatibility_checks

if __name__ == "__main__":
    source = source_checks(ROOT)
    joint = compatibility_checks(ROOT)
    print(json.dumps({"record_source": source, "joint_source_compatibility": joint}, sort_keys=True))
