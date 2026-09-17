#!/usr/bin/env python3
"""vp_vnext33_no_overclaim - reject vNext+1 grand-overclaim (negation-aware)."""
import pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
FORBIDDEN = ['34 minus 1 proves the d0 scene', 'af tower is now the d0 physical carrier', 'af tower is the d0 physical carrier', 'dirac scale is phi^n by definition', 'af quotient derives alpha', 'af quotient predicts n_s', 'af quotient predicts ns', 'af quotient derives higgs vev', 'smooth manifold follows automatically', 'all vnext+1 fronts closed', 'all vnext+1 fronts are closed']
NEG = ("no ", "not ", "never ", "without ", "does not ", "is not ", "are not ", "do not ", "no primitive ")
def hits(prose):
    out, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0, m.start() - 40):m.start()] for n in NEG):
                out.append(p); break
    return out

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the 33-scene anchor is closed-negative; no affirmative "
          "overclaim phrase may appear. Scan is NEGATION-AWARE.")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    h = hits(prose)
    assert not h, f"affirmative overclaim(s): {h}"
    print("PASS_NO_OVERCLAIM  no affirmative forbidden phrase in the books.")
    assert hits('the AF tower is now the D0 physical carrier and the AF quotient derives alpha; all vNext+1 fronts closed'), "control: a planted overclaim must be caught"
    print("FAIL_OVERCLAIM_CAUGHT  a planted overclaim is caught.")
    assert not hits("we do not claim the af tower is now the d0 physical carrier")
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print("PASS_VNEXT33_NO_OVERCLAIM")
    return 0

if __name__ == "__main__": raise SystemExit(main())
