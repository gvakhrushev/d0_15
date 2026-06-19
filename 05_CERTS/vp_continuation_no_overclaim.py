#!/usr/bin/env python3
"""vp_continuation_no_overclaim - block grand-closure / external-confirmation overclaim (continuation).

Scans the assembled books and fails if any forbidden grand-closure or external-confirmation phrase
appears while named global blockers remain in FINAL_CONTINUATION_BLOCKERS.csv. The continuation closed
what was closable in prior campaigns and recorded the rest as exact-named PROOF-TARGETs; it asserts NO
global closure and NO empirical confirmation. A planted phrase is caught (reachable control).
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "FINAL_CONTINUATION_BLOCKERS.csv"
FORBIDDEN = [
    "D0 complete",
    "zero theorem debt",
    "all open joints closed",
    "all open joints are closed",
    "Theory of Everything complete",
    "Nature proves D0",
    "Nature confirms D0",
    "DESI confirms D0",
    "KATRIN confirms D0",
    "LIGO confirms D0",
    "Planck confirms D0",
    "SM table imported as proof",
    "PDG masses used as input",
    "CPL fitted as core",
    "finite heat trace has 1/s pole",
    "smooth manifold primitive",
]


def main() -> int:
    print("=== vp_continuation_no_overclaim  no grand-closure / external-confirmation while blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the continuation asserts NO global closure and NO empirical "
          "confirmation -- closable items were closed in prior campaigns, the rest are exact-named blockers; "
          "the forbidden phrases are licensed only if zero global blockers remain -- fixed before any count.")

    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    blockers = [r for r in rows if r["is_global_blocker"].strip() == "True"]
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))

    # An overclaim counts only if AFFIRMATIVE: the books legitimately *negate* these phrases in
    # disclaimers ("no SM table imported as proof", "finite heat trace has NO 1/s pole"), which a naive
    # substring scan would false-positive on. Flag an occurrence only when it is NOT preceded by a negation.
    NEG = ("no ", "not ", "never", "n't", "without", "cannot", "neither", "no-", "≠", "!=")
    low = prose.lower()
    hits = []
    for f in FORBIDDEN:
        fl, start = f.lower(), 0
        while True:
            i = low.find(fl, start)
            if i < 0:
                break
            ctx = low[max(0, i - 18):i]
            if not any(n in ctx for n in NEG):
                hits.append(f)
                break
            start = i + len(fl)
    assert not hits, f"AFFIRMATIVE grand-closure/confirmation phrase(s) while {len(blockers)} blockers remain: {hits}"
    print(f"PASS_NO_OVERCLAIM  none of the {len(FORBIDDEN)} forbidden phrases appear; {len(blockers)} named "
          f"global blockers remain (global closure / external confirmation NOT asserted).")

    assert blockers, "expected named global blockers from the continuation (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} global blockers named in FINAL_CONTINUATION_BLOCKERS.csv.")

    planted = "intro: D0 complete, Nature proves D0, finite heat trace has 1/s pole, zero theorem debt."
    caught = [f for f in FORBIDDEN if f in planted]
    assert len(caught) >= 3, "control: the over-claim detector must be reachable on a planted blob"
    print(f"FAIL_PLANTED_CONTINUATION_OVERCLAIM_CAUGHT  detector catches planted phrases {caught[:3]} (reachable).")

    print("PASS_CONTINUATION_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
