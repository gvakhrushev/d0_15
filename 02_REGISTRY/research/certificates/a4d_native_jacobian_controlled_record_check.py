#!/usr/bin/env python3
"""Narrow complete-AF controlled-record source consumer; no old replay."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/"02_REGISTRY/research/sources/d0_jacobian_controlled_record_2026-10-16"))

from controlled_record import run_checks


if __name__ == "__main__":
    print(json.dumps(run_checks(ROOT), sort_keys=True))
