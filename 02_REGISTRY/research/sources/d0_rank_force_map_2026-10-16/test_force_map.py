#!/usr/bin/env python3
"""Run the force-map certificate. No assert: python -O keeps every check."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import force_map


def main():
    result = force_map.run()
    if result["exact_checks"] < 40:
        raise AssertionError("too_few_checks")
    if result["exact_checks"] != len(result["checks"]):
        raise AssertionError("check_count_mismatch")
    if len(result["checks"]) != len(set(result["checks"])):
        raise AssertionError("duplicate_check_name")
    for flag in (
        "nonlinear_branch_continued",
        "geometric_source_assigned",
        "pr_334_merged",
        "gr_closed",
        "claims_csv_changed",
    ):
        if result[flag]:
            raise AssertionError(flag)
    if result["normalized_operator"] != "J(t)=memo B(t)":
        raise AssertionError("operator_name")
    witness = result["witnesses"]
    if witness["blank_rank"] != 1 or witness["boundary_rank"] != 1 or witness["half_boundary_rank"] != 2:
        raise AssertionError("witness_ranks")
    print(json.dumps({
        "status": "PASS",
        "exact_checks": result["exact_checks"],
        "witnesses": witness,
        "gr_closed": False,
        "nonlinear_branch_continued": False,
        "geometric_source_assigned": False,
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
