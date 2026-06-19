#!/usr/bin/env python3
"""vp_eight_front_final_closure_no_overclaim - block grand-closure overclaim after the eight-front campaign.

The eight-front campaign closed 6 CERT-CLOSED + 2 NO-GO owners and minted PROOF-TARGETs with exact
gaps; it did NOT achieve global closure. This guard scans the assembled books and fails if any
grand-closure phrase appears UNLESS FINAL_EIGHT_FRONT_BLOCKERS.csv shows zero global blockers AND
all campaign owners are registered-closed. Since named blockers remain, the phrases are forbidden
outright. A planted phrase is caught (reachable control).
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "FINAL_EIGHT_FRONT_BLOCKERS.csv"

FORBIDDEN = [
    "D0 complete",
    "zero theorem debt",
    "all open joints closed",
    "all open joints are closed",
    "TOE finished",
    "Theory of Everything is complete",
    "final theory complete",
    "all mathematical gaps closed",
    "all mathematical gaps are closed",
    "DESI confirms",
    "KATRIN confirms",
    "LIGO confirms",
    "Planck confirms",
]


def global_blockers():
    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    return [r for r in rows if r["is_global_blocker"].strip() == "True"]


def main() -> int:
    print("=== vp_eight_front_final_closure_no_overclaim  no grand-closure while named blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the eight fronts produced narrow finite owners + no-gos, NOT a "
          "global closure; grand-closure phrases are licensed ONLY if FINAL_EIGHT_FRONT_BLOCKERS.csv shows "
          "zero global blockers -- fixed before any count.")

    blockers = global_blockers()
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))

    hits = [f for f in FORBIDDEN if f in prose]
    if blockers:
        assert not hits, f"grand-closure phrase(s) present while {len(blockers)} named blockers remain: {hits}"
        print(f"PASS_NO_OVERCLAIM_WITH_BLOCKERS  {len(blockers)} global blockers remain and none of the "
              f"{len(FORBIDDEN)} grand-closure phrases appear in the books.")
    else:
        print("INFO_ZERO_BLOCKERS  blockers CSV shows zero global blockers; grand-closure phrases would be "
              "permitted -- re-verify the registry before relying on this branch.")

    # the campaign's own honest conclusion must be present somewhere (the dependency graph names blockers)
    assert blockers, "expected named blockers from the eight-front campaign (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} blockers named in FINAL_EIGHT_FRONT_BLOCKERS.csv.")

    # negative control: a planted grand-closure phrase is detected while blockers remain
    planted = "intro: D0 complete and all mathematical gaps closed and zero theorem debt."
    caught = [f for f in FORBIDDEN if f in planted]
    assert caught and blockers, "control failed: the overclaim detector must be reachable while blockers remain"
    print(f"FAIL_PLANTED_FINAL_OVERCLAIM_CAUGHT  detector catches a planted grand-closure phrase ({caught[0]!r}).")

    print("PASS_EIGHT_FRONT_FINAL_CLOSURE_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
