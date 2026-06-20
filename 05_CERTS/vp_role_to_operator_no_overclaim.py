#!/usr/bin/env python3
"""vp_role_to_operator_no_overclaim - block role-to-operator overclaim while named blockers remain.

NEGATION-AWARE (per VERIFIED_CLOSURE_PROTOCOL): an over-claim phrase is flagged only when it occurs
AFFIRMATIVELY -- not shortly preceded by a negation. Honest disclaimers ("no SM table imported as
proof", "lepton masses are NOT derived from graph decimals") pass; a real affirmative over-claim is
caught. Phrases licensed only if ROLE_TO_OPERATOR_BLOCKERS.csv shows zero global blockers (it does not).
"""
import csv
import pathlib
import re
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "ROLE_TO_OPERATOR_BLOCKERS.csv"
FORBIDDEN = [
    "D0 proves all Standard Model matter", "SM row imported as graph-flow proof", "CKM fitted from data",
    "lepton decimal masses derived", "Higgs 246 GeV derived", "246 GeV derived",
    "all Gauge-Matter Functor closed", "role-to-operator functor closed", "canonical role carrier exists",
]
NEG = ("no ", "not ", "never ", "without ", "n't ", "cannot ", "does not ", "do not ", "neither ",
       "is not ", "are not ", "rejects ", "reject ", "forbids ", "must not ")


def affirmative_hits(prose):
    hits, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p.lower()), low):
            ctx = low[max(0, m.start() - 40):m.start()]
            if not any(neg in ctx for neg in NEG):
                hits.append(p); break
    return hits


def global_blockers():
    return [r for r in csv.DictReader(BLOCKERS.open(encoding="utf-8", newline="")) if r["is_global_blocker"].strip() == "True"]


def main() -> int:
    print("=== vp_role_to_operator_no_overclaim  no role-to-operator grand-overclaim while named blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the campaign closed the hypercharge row + cites existing owners, "
          "NOT a Standard-Model derivation; over-claim phrases licensed only if zero global blockers. The "
          "scan is NEGATION-AWARE (honest disclaimers pass).")
    blockers = global_blockers()
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    hits = affirmative_hits(prose)
    if blockers:
        assert not hits, f"affirmative role-to-operator over-claim(s) while {len(blockers)} blockers remain: {hits}"
        print(f"PASS_NO_OVERCLAIM_WITH_BLOCKERS  {len(blockers)} global blockers remain; no AFFIRMATIVE over-claim phrase appears.")
    else:
        print("INFO_ZERO_BLOCKERS  blockers CSV shows zero global blockers; re-verify before licensing.")
    assert blockers, "expected named role-to-operator blockers (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} blockers named in ROLE_TO_OPERATOR_BLOCKERS.csv.")
    planted = "result: D0 proves all Standard Model matter and role-to-operator functor closed."
    assert affirmative_hits(planted), "control: an affirmative over-claim must be caught"
    print("FAIL_AFFIRMATIVE_OVERCLAIM_CAUGHT  a planted 'D0 proves the Standard Model / all matter sector closed' is caught.")
    honest = "no canonical role carrier exists, and lepton decimal masses are not derived."
    assert not affirmative_hits(honest), "control: an honest negated disclaimer must NOT be flagged"
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest 'does not import SM charges' disclaimer is NOT flagged.")
    print("PASS_ROLE_TO_OPERATOR_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
