#!/usr/bin/env python3
"""Validate the strict empirical-passport matrix."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "08_PASSPORTS" / "_MATRIX" / "empirical_passport_matrix.json"
REQUIRED = {
    "ICECUBE-PHAS1",
    "SPARC-HALO1",
    "DESI-SDE1",
    "CMB-PHASON1",
    "CKM-PDG1",
    "MESON-PDG1",
}


def main() -> int:
    if not MATRIX.exists():
        print(f"FAIL missing {MATRIX}")
        return 1
    rows = json.loads(MATRIX.read_text(encoding="utf-8"))["rows"]
    ids = {row["passport_id"] for row in rows}
    missing = sorted(REQUIRED - ids)
    failures = []
    if missing:
        failures.append(f"missing passport rows: {missing}")
    for row in rows:
        if row["passport_id"] in {"SPARC-HALO1", "DESI-SDE1"}:
            if "FAIL_ARBITRARY_KERNEL_REPAIR" not in row["negative_controls"]:
                failures.append(f"{row['passport_id']} lacks arbitrary-kernel negative control")
            if "boundary" not in row["promotion_boundary"].lower():
                failures.append(f"{row['passport_id']} lacks boundary diagnostic promotion boundary")
        if row["allowed_status"].startswith("EMPIRICAL") and "core" in row["promotion_boundary"].lower():
            failures.append(f"{row['passport_id']} promotion boundary mentions core ambiguously")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS_EMPIRICAL_PASSPORT_MATRIX_CHECK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
