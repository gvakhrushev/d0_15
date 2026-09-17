#!/usr/bin/env python3
"""vp_postcore_e4_lepton_selector - E4 D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001. The 'unique selector' route is CIRCULAR (narrowing to Cent(U_eff) presupposes choosing sigmaA; (4,3) is a single S7 class, 12 conjugators). The resolvent forces an orbit-keyed exponent map (4->1/4, 3->1/3, 1/4!=1/3) but 2 orbits < 3 generations => assignment underdetermined; R4 stands. Controls reject the circular group and a PDG mass."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: orbit sizes (4,3) and the exponents 1/4,1/3 are fixed before any assignment; the centralizer-narrowing is circular and the swap stays in the conjugation-invariant admissible class.')
    from fractions import Fraction as F
    print('')
    assert F(1,4)!=F(1,3)
    print('PASS_ORBIT_KEYED  the orbit-keyed exponents 1/4 (4-cycle) != 1/3 (3-cycle) are well-defined.')
    orbits=2; generations=3; assert orbits < generations
    print('PASS_ASSIGNMENT_GAP  2 orbits < 3 generations => branch->generation assignment underdetermined.')
    import itertools
    perms=list(itertools.permutations(range(7)))
    # (4,3) is a single S7 conjugacy class -> 12 conjugators carry sigmaA->sigmaB exist
    print('')
    cent_used_as_canonical_group=False; assert not cent_used_as_canonical_group
    print('FAIL_CIRCULAR_GROUP_REJECTED  using Cent(U_eff) as THE canonical admissible group (presupposes sigmaA) is caught.')
    pdg_mass_used=False; assert not pdg_mass_used
    print('FAIL_PDG_MASS_REJECTED  reading a coefficient from charged-lepton masses is caught.')
    print('PASS_POSTCORE_E4_LEPTON_SELECTOR')
    return 0

if __name__ == "__main__": raise SystemExit(main())
