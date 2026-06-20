#!/usr/bin/env python3
"""vp_toral_markov_no_overclaim - block toral-Markov overclaim while named blockers remain.

NEGATION-AWARE (per VERIFIED_CLOSURE_PROTOCOL): an over-claim phrase is flagged only when AFFIRMATIVE
(not shortly preceded by a negation). Honest disclaimers ("Adler-Weiss is NOT imported as core", "ordinary
shift equivalence is not sufficient for conjugacy") pass; a real affirmative over-claim is caught. Phrases
licensed only if TORAL_MARKOV_BLOCKERS.csv shows zero global blockers (it does not).
"""
import csv
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "TORAL_MARKOV_BLOCKERS.csv"
FORBIDDEN = [
    "Adler-Weiss theorem imported as core proof", "Adler-Weiss imported as core",
    "raw symbolic shift globally conjugate", "Williams shift equivalence alone proves conjugacy",
    "shift equivalence alone proves conjugacy", "T^44 = I", "T44 = I",
    "physical spacetime is literally a torus", "spacetime is a torus", "all geometry/time closed",
    "all geometry and time closed",
]
NEG = ("no ", "not ", "never ", "without ", "n't ", "cannot ", "does not ", "do not ", "neither ",
       "is not ", "are not ", "rejects ", "reject ", "forbids ", "must not ")


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
    print("=== vp_toral_markov_no_overclaim  no toral-Markov grand-overclaim while named blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the campaign closed the integral conjugacy + periodic seed and a "
          "canonical-Markov NO-GO, NOT a symbolic conjugacy; over-claim phrases licensed only if zero global "
          "blockers. Scan is NEGATION-AWARE.")
    blockers = global_blockers()
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    hits = affirmative_hits(prose)
    if blockers:
        assert not hits, f"affirmative toral over-claim(s) while {len(blockers)} blockers remain: {hits}"
        print(f"PASS_NO_OVERCLAIM_WITH_BLOCKERS  {len(blockers)} global blockers remain; no AFFIRMATIVE "
              "over-claim phrase appears.")
    else:
        print("INFO_ZERO_BLOCKERS  re-verify before licensing.")
    assert blockers, "expected named toral blockers (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} blockers named in TORAL_MARKOV_BLOCKERS.csv.")

    planted = "result: the raw symbolic shift globally conjugate to the torus and all geometry/time closed."
    assert affirmative_hits(planted), "control: an affirmative over-claim must be caught"
    print("FAIL_AFFIRMATIVE_OVERCLAIM_CAUGHT  a planted 'raw shift globally conjugate / all geometry closed' is caught.")
    honest = "Adler-Weiss is not imported as core proof, and shift equivalence alone does not prove conjugacy; T^44 != I."
    assert not affirmative_hits(honest), "control: an honest negated disclaimer must NOT be flagged"
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_TORAL_MARKOV_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
