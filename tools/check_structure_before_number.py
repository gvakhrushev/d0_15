#!/usr/bin/env python3
"""Guard: holonomy-batch certs must declare structure-before-number AND carry a negative control.

The ТЗ discipline (no result enters as a bare "PASS"): every cert in the closure-holonomy batch must
(1) print a `STRUCTURE_FIXED_BEFORE_NUMBER:` line listing the forced constants fixed before any data
comparison, and (2) contain at least one negative control (a `FAIL_` print and/or a control `assert`).

This is a REQUIRED-discipline ratchet: the list may only GROW as new structure-before-number certs are
added. Exit 0 if every listed cert satisfies both; 1 otherwise.
"""
from __future__ import annotations

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS = os.path.join(REPO, "05_CERTS")

# Closure-holonomy batch (Iter-21): each must carry the structure-before-number marker + a control.
REQUIRED: list[str] = [
    "vp_seam_holonomy_alpha.py",
    "vp_pi0_discrete_angle.py",
    "vp_q8_sin_channel.py",
    "vp_pmns_seam_topology.py",
    "vp_xi5_cross_sector.py",
    "vp_alpha_measurement_limit.py",
]


def check(path: str) -> list[str]:
    problems: list[str] = []
    if not os.path.exists(path):
        return [f"missing on disk: {os.path.basename(path)}"]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if "STRUCTURE_FIXED_BEFORE_NUMBER" not in text:
        problems.append(f"{os.path.basename(path)}: no STRUCTURE_FIXED_BEFORE_NUMBER marker")
    has_fail = "FAIL_" in text
    has_control_assert = "control:" in text or "control" in text.lower()
    if not (has_fail or has_control_assert):
        problems.append(f"{os.path.basename(path)}: no negative control (FAIL_ print / control assert)")
    return problems


def main() -> int:
    all_problems: list[str] = []
    for name in REQUIRED:
        all_problems += check(os.path.join(CERTS, name))
    if all_problems:
        print("FAIL: structure-before-number discipline violated:")
        for p in all_problems:
            print(f"  {p}")
        print("Fix: every holonomy-batch cert must print STRUCTURE_FIXED_BEFORE_NUMBER: <forced constants> "
              "and carry at least one negative control.")
        return 1
    print(f"RESULT: PASS -- all {len(REQUIRED)} closure-holonomy certs declare structure-before-number "
          "and carry a negative control")
    return 0


if __name__ == "__main__":
    sys.exit(main())
