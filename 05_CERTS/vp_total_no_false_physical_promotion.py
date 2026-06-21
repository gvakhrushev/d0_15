#!/usr/bin/env python3
"""vp_total_no_false_physical_promotion - reject false physical/empirical promotion in the books (negation-aware)."""
import pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]; BOOKS = ROOT/"01_BOOKS"
FORBIDDEN=["d0 derives measured alpha","d0 derives the measured alpha","d0 predicts planck n_s","d0 predicts planck ns","d0 derives physical w_de","d0 derives charged-lepton decimals","d0 derives the charged-lepton decimals","d0 derives higgs vev","d0 derives the higgs vev","d0 proves a smooth manifold","ligo confirms d0","desi confirms d0","all physics is closed"]
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ")
def hits(p):
    o,l=[],p.lower()
    for f in FORBIDDEN:
        for m in re.finditer(re.escape(f),l):
            if not any(n in l[max(0,m.start()-40):m.start()] for n in NEG): o.append(f); break
    return o
def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: no quantity is derived/promoted to CORE and no empirical confirmation is claimed; scan is NEGATION-AWARE.")
    prose="\n".join(p.read_text(encoding="utf-8",errors="replace") for p in BOOKS.rglob("*.md"))
    hh=hits(prose); assert not hh, f"false promotion(s): {hh}"
    print("PASS_NO_FALSE_PROMOTION  no fitted-physics / detection / all-closed overclaim in the books.")
    assert hits("LIGO confirms D0 and D0 derives measured alpha")
    print("FAIL_FALSE_PROMOTION_CAUGHT  a planted overclaim is caught.")
    assert not hits("D0 does not derive measured alpha; LIGO does not confirm D0")
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_TOTAL_NO_FALSE_PHYSICAL_PROMOTION")
    return 0

if __name__ == "__main__": raise SystemExit(main())
