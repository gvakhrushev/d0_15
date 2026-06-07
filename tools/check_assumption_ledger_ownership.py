#!/usr/bin/env python3
"""Check that every ASSUMP-* row has an explicit owner and bridge status."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "LEAN_ASSUMPTION_LEDGER.csv"


REQUIRED = {
    "assumption_id",
    "lean_name",
    "lean_file",
    "used_by_theorem",
    "claim_id",
    "assumption_type",
    "status",
    "justification",
    "failure_meaning",
}


def main() -> int:
    if not LEDGER.exists():
        print(f"FAIL missing {LEDGER}")
        return 1
    failures: list[str] = []
    with LEDGER.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing_columns = REQUIRED - set(reader.fieldnames or [])
        if missing_columns:
            failures.append(f"missing columns: {sorted(missing_columns)}")
        for row in reader:
            aid = row.get("assumption_id", "")
            if not aid.startswith("ASSUMP-"):
                failures.append(f"{aid}: assumption_id must start with ASSUMP-")
            for field in REQUIRED:
                if not row.get(field, "").strip():
                    failures.append(f"{aid}: missing {field}")
            status = row.get("status", "").strip()
            if status not in {"EXPLICIT", "ETERNAL_BRIDGE", "CLOSE_PATH_DECLARED"}:
                failures.append(f"{aid}: status must be EXPLICIT, ETERNAL_BRIDGE or CLOSE_PATH_DECLARED")
            lean_file = row.get("lean_file", "").strip()
            if lean_file and not (ROOT / "09_LEAN_FORMALIZATION" / lean_file).exists():
                failures.append(f"{aid}: owner file does not exist: {lean_file}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("PASS_ASSUMPTION_LEDGER_OWNERSHIP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
