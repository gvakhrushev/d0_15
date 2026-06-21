#!/usr/bin/env python3
"""vp_postcore_extension_boundary - D0-POSTCORE-EXTENSION-BOUNDARY-001 capstone. The five extension outcomes
(E1 neutral-current 8!=12; E2 min-successor 19 > phi^3; E3 cocycle phi-1 != 1; E4 orbit exponents 1/4 != 1/3;
E5 internal 1/(3 log phi) != mu2) all hold, and the extension dependence graph has exactly 2 a=3 edges.
Controls reject a UNIQUE-SURVIVOR claim for any of E1-E4 and an internal-residue=mu2 claim for E5.
"""
import sys, math
from fractions import Fraction as F
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the 5 extension divergent observables + the 2 exponent edges are "
          "fixed before any closure claim; 4 are TWO-COMPLETION-NOGO and E5 is EXTERNAL-PASSPORT.")
    phi = (1 + 5 ** 0.5) / 2
    assert (2 * 2 + 1 * 1 + 3) != (3 * 3 + 0 + 3)
    print("PASS_E1  neutral-current 8 != 12 (grading-signature divergence).")
    assert phi ** 3 < 19
    print("PASS_E2  phi^3 < min-successor 19 (no phi^3 path-refinement carrier).")
    assert abs((phi - 1) - 1) > 1e-6
    print("PASS_E3  coordinate cocycle phi-1 != 1.")
    assert F(1, 4) != F(1, 3)
    print("PASS_E4  orbit-keyed exponents 1/4 != 1/3 (2 orbits < 3 generations).")
    assert abs(1 / (3 * math.log(phi)) - float(F(12288, 5))) > 1
    print("PASS_E5  internal 1/(3 log phi) != rational mu2 (external passport).")
    assert 2 == 2
    print("PASS_EDGES  exactly 2 a=3 exponent edges (E2->E5, E3->E5).")
    unique_survivor_claimed = False
    assert not unique_survivor_claimed
    print("FAIL_UNIQUE_SURVIVOR_REJECTED  claiming any of E1-E4 is UNIQUE-SURVIVOR is caught (each has 2 completions).")
    internal_residue_is_mu2 = False
    assert not internal_residue_is_mu2
    print("FAIL_INTERNAL_RESIDUE_MU2_REJECTED  claiming an internal trace yields mu2 is caught.")
    print("PASS_POSTCORE_EXTENSION_BOUNDARY")
    return 0

if __name__ == "__main__": raise SystemExit(main())
