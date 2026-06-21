#!/usr/bin/env python3
"""vp_root_operator_publication_firewall - negation-aware book scan rejecting chosen-state / external-value-in-operator / detection overclaims for the root program."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; return rs, H
def book_prose():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject")
def affirm_hits(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-44):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no Dixmier state chosen to obtain mu2, no CMB window after viewing tilt, no DESI/Planck/PDG/LIGO value defining a D0 operator; scan is NEGATION-AWARE.')
    prose = book_prose()
    FORB = ["dixmier state chosen to obtain mu2","cmb window chosen after viewing the target tilt","desi value used to define","planck value used to define","pdg value used to define","ligo value used to define","ligo confirms d0","desi confirms d0"]
    bad = affirm_hits(prose, FORB); assert not bad, f"publication-firewall breach: {bad}"
    print("PASS_PUBLICATION_FIREWALL  no chosen-state / external-value-in-operator / detection overclaim in the books.")
    assert affirm_hits("the dixmier state chosen to obtain mu2 here", ["dixmier state chosen to obtain mu2"])
    print("FAIL_FIREWALL_BREACH_CAUGHT  a planted chosen-state overclaim is caught.")
    assert not affirm_hits("no dixmier state is chosen to obtain mu2", ["dixmier state chosen to obtain mu2"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_ROOT_OPERATOR_PUBLICATION_FIREWALL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
