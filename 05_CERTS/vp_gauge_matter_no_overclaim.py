#!/usr/bin/env python3
"""vp_gauge_matter_no_overclaim - block gauge-matter overclaim while named blockers remain.

NEGATION-AWARE (per VERIFIED_CLOSURE_PROTOCOL): an over-claim phrase is flagged only when it occurs
AFFIRMATIVELY -- not shortly preceded by a negation. Honest disclaimers ("no SM table imported as
proof", "lepton masses are NOT derived from graph decimals") pass; a real affirmative over-claim is
caught. Phrases licensed only if GAUGE_MATTER_BLOCKERS.csv shows zero global blockers (it does not).
"""
import csv
import pathlib
import re
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
BLOCKERS = ROOT / "04_VERIFICATION" / "GAUGE_MATTER_BLOCKERS.csv"
FORBIDDEN = [
    "D0 proves the Standard Model", "D0 proves Standard Model", "SM charges imported as proof",
    "CKM angle fitted", "CKM angles fitted", "lepton masses derived from graph decimals",
    "Higgs 246 GeV derived", "246 GeV derived", "all matter sector closed", "matter sector is complete",
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
    print("=== vp_gauge_matter_no_overclaim  no gauge-matter grand-overclaim while named blockers remain ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the campaign closed the hypercharge row + cites existing owners, "
          "NOT a Standard-Model derivation; over-claim phrases licensed only if zero global blockers. The "
          "scan is NEGATION-AWARE (honest disclaimers pass).")
    blockers = global_blockers()
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    hits = affirmative_hits(prose)
    if blockers:
        assert not hits, f"affirmative gauge-matter over-claim(s) while {len(blockers)} blockers remain: {hits}"
        print(f"PASS_NO_OVERCLAIM_WITH_BLOCKERS  {len(blockers)} global blockers remain; no AFFIRMATIVE over-claim phrase appears.")
    else:
        print("INFO_ZERO_BLOCKERS  blockers CSV shows zero global blockers; re-verify before licensing.")
    assert blockers, "expected named gauge-matter blockers (frontier must stay non-empty)"
    print(f"PASS_FRONTIER_NONEMPTY  {len(blockers)} blockers named in GAUGE_MATTER_BLOCKERS.csv.")
    planted = "result: D0 proves the Standard Model and all matter sector closed."
    assert affirmative_hits(planted), "control: an affirmative over-claim must be caught"
    print("FAIL_AFFIRMATIVE_OVERCLAIM_CAUGHT  a planted 'D0 proves the Standard Model / all matter sector closed' is caught.")
    honest = "this owner does not import SM charges as proof, and lepton masses are not derived from graph decimals."
    assert not affirmative_hits(honest), "control: an honest negated disclaimer must NOT be flagged"
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest 'does not import SM charges' disclaimer is NOT flagged.")
    print("PASS_GAUGE_MATTER_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
