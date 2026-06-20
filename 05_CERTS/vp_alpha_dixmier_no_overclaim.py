#!/usr/bin/env python3
"""vp_alpha_dixmier_no_overclaim - block alpha-Dixmier overclaim while named blockers remain.

NEGATION-AWARE (per VERIFIED_CLOSURE_PROTOCOL): an over-claim phrase is flagged only when AFFIRMATIVE
(not shortly preceded by a negation). Honest disclaimers ("the finite heat trace does NOT have a pole",
"CODATA alpha is not derived") pass; a real affirmative over-claim is caught. Over-claim phrases are
licensed only if ALPHA_DIXMIER_BLOCKERS.csv shows zero global blockers (it does not -- Outcome B).
"""
import csv
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "ALPHA_DIXMIER_BLOCKERS.csv"
FORBIDDEN = [
    "finite heat trace has a pole", "finite heat trace has a 1/s", "finite zeta residue equals dixmier",
    "finite zeta residue is the dixmier trace", "zeta residue equals the dixmier trace",
    "codata alpha derived", "codata alpha is derived", "derive the measured alpha", "derives measured alpha",
    "external trace state inserted", "external dixmier state inserted",
    "2^11 chosen by hand", "2^11 is chosen by hand", "all alpha routes closed", "all alpha routes are closed",
    "dixmier trace equals mu_2", "dixmier realization of mu_2",
]
NEG = ("no ", "not ", "never ", "without ", "n't ", "cannot ", "does not ", "do not ", "neither ",
       "is not ", "are not ", "rejects ", "reject ", "forbids ", "must not ", "no finite", "not a ")


def affirmative_hits(prose):
    hits, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p.lower()), low):
            ctx = low[max(0, m.start() - 40):m.start()]
            if not any(neg in ctx for neg in NEG):
                hits.append(p)
                break
    return hits


def global_blockers():
    return [r for r in csv.DictReader(BLOCKERS.open(encoding="utf-8", newline=""))
            if r["is_global_blocker"].strip() == "True"]


def main() -> int:
    print("=== vp_alpha_dixmier_no_overclaim  no alpha-Dixmier grand-overclaim while blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Outcome B closed a trace-class NO-GO + the tower spectral data, "
          "NOT a Dixmier realization of mu_2; over-claim phrases licensed only if zero global blockers. "
          "Scan is NEGATION-AWARE.")
    blockers = global_blockers()
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    hits = affirmative_hits(prose)
    if blockers:
        assert not hits, f"affirmative alpha-Dixmier over-claim(s) while {len(blockers)} blockers remain: {hits}"
        print(f"PASS_NO_OVERCLAIM_WITH_BLOCKERS  {len(blockers)} global blockers remain; no AFFIRMATIVE "
              "over-claim phrase appears.")
    else:
        print("INFO_ZERO_BLOCKERS  re-verify before licensing.")
    assert blockers, "expected named alpha-Dixmier blockers (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} blockers named in ALPHA_DIXMIER_BLOCKERS.csv.")

    planted = "result: the finite zeta residue equals the dixmier trace, CODATA alpha derived, all alpha routes closed."
    assert affirmative_hits(planted), "control: an affirmative over-claim must be caught"
    print("FAIL_AFFIRMATIVE_OVERCLAIM_CAUGHT  a planted 'zeta residue = Dixmier trace / CODATA derived' is caught.")
    honest = "The finite heat trace does not have a pole; CODATA alpha is not derived; 2^11 is not chosen by hand."
    assert not affirmative_hits(honest), "control: an honest negated disclaimer must NOT be flagged"
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_ALPHA_DIXMIER_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
