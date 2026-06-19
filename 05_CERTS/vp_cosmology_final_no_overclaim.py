#!/usr/bin/env python3
"""vp_cosmology_final_no_overclaim - block cosmology grand-overclaim while named blockers remain.

NEGATION-AWARE (per VERIFIED_CLOSURE_PROTOCOL): an over-claim phrase is flagged only when it occurs
AFFIRMATIVELY -- i.e. NOT shortly preceded by a negation (no/not/never/without/n't/cannot/does not).
This lets honest disclaimers ("no survey confirms D0", "CMB n_s is NOT fitted") pass while a real
affirmative over-claim is caught. The phrases are licensed only if COSMOLOGY_CLOSURE_BLOCKERS.csv shows
zero global blockers (it does not). Reachable control: a planted affirmative over-claim is caught.
"""
import csv
import pathlib
import re
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "COSMOLOGY_CLOSURE_BLOCKERS.csv"

FORBIDDEN = [
    "DESI confirms D0", "Planck confirms D0", "CMB n_s fitted", "inflation derived from survey",
    "CPL defines core EOS", "H0 derived from topology alone", "all cosmology closed",
    "cosmology is complete", "n_s is fitted to Planck",
]
NEG = ("no ", "not ", "never ", "without ", "n't ", "cannot ", "does not ", "do not ", "neither ",
       "isn't", "is not ", "are not ", "rejects ", "reject ", "forbids ", "must not ")


def affirmative_hits(prose):
    """Return forbidden phrases that occur NOT preceded by a negation within ~40 chars."""
    hits = []
    low = prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p.lower()), low):
            ctx = low[max(0, m.start() - 40):m.start()]
            if not any(neg in ctx for neg in NEG):
                hits.append(p)
                break
    return hits


def global_blockers():
    rows = list(csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")))
    return [r for r in rows if r["is_global_blocker"].strip() == "True"]


def main() -> int:
    print("=== vp_cosmology_final_no_overclaim  no cosmology grand-overclaim while named blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the campaign closed narrow internal owners + named blockers, NOT a "
          "global cosmology closure; over-claim phrases are licensed only if zero global blockers -- fixed "
          "before any count. The scan is NEGATION-AWARE (honest disclaimers pass).")

    blockers = global_blockers()
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))

    hits = affirmative_hits(prose)
    if blockers:
        assert not hits, f"affirmative cosmology over-claim(s) while {len(blockers)} blockers remain: {hits}"
        print(f"PASS_NO_OVERCLAIM_WITH_BLOCKERS  {len(blockers)} global blockers remain; no AFFIRMATIVE "
              f"over-claim phrase appears (negated disclaimers allowed).")
    else:
        print("INFO_ZERO_BLOCKERS  blockers CSV shows zero global blockers; re-verify before licensing.")

    assert blockers, "expected named cosmology blockers (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} blockers named in COSMOLOGY_CLOSURE_BLOCKERS.csv.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    planted = "the survey result shows DESI confirms D0 and all cosmology closed."
    assert affirmative_hits(planted), "control: an affirmative over-claim must be caught"
    print("FAIL_AFFIRMATIVE_OVERCLAIM_CAUGHT  a planted affirmative 'DESI confirms D0 / all cosmology closed' is caught.")

    honest = "this owner does not claim DESI confirms D0, and CMB n_s is not fitted to Planck."
    assert not affirmative_hits(honest), "control: an honest negated disclaimer must NOT be flagged"
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest 'does not claim DESI confirms D0' disclaimer is NOT flagged.")

    print("PASS_COSMOLOGY_FINAL_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
