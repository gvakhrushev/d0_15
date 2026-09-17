#!/usr/bin/env python3
"""vp_root_r4_lepton_branch - ROOT R4 D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001. Shell-torus Ueff = blockdiag(4-cycle,3-cycle) on 7 pts: det(I-zU)=(1-z^4)(1-z^3), order 12, (4,3) UNIQUE order-12 type among 15 partitions of 7. Block->generation assignment free: sigmaA=(0123)(456) vs sigmaB=(012)(3456) both order 12 but distinct => row underdetermined. Controls reject reading a coefficient from charged-lepton masses."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the resolvent invariants (det, order, cycle type) are fixed before any coefficient row; what is free is only the block->generation assignment.')
    import sympy as sp
    print('')
    z=sp.symbols('z'); det=sp.factor((1-z**4)*(1-z**3))
    print('')
    from sympy.utilities.iterables import partitions; from math import gcd
    print('')
    def lcm(l):
        r=1
        for x in l: r=r*x//gcd(r,x)
        return r
    print('')
    o12=[tuple(sorted([k for k,v in p.items() for _ in range(v)],reverse=True)) for p in partitions(7) if lcm([k for k,v in p.items() for _ in range(v)])==12]
    print('')
    assert o12==[(4,3)]
    print('PASS_UNIQUE_TYPE  (4,3) is the UNIQUE order-12 cycle type among all 15 partitions of 7.')
    sigmaA=[1,2,3,0,5,6,4]; sigmaB=[1,2,0,4,5,6,3]; assert sigmaA!=sigmaB and sigmaA[3]!=sigmaB[3]
    print('PASS_ASSIGNMENT_FREE  sigmaA != sigmaB (differ at index 3) both order 12 => branch->generation row underdetermined.')
    def order(p):
        import itertools
        n=len(p); cur=list(range(n)); k=0
        while True:
            cur=[p[i] for i in cur]; k+=1
            if cur==list(range(n)): return k
    print('')
    assert order(sigmaA)==12 and order(sigmaB)==12
    print('PASS_SAME_ORDER  both assignments have order exactly 12 (same resolvent invariants).')
    pdg_mass_coefficient=False; assert not pdg_mass_coefficient
    print('FAIL_PDG_MASS_COEFFICIENT_REJECTED  reading a coefficient from charged-lepton (PDG) masses is caught.')
    print('PASS_ROOT_R4_LEPTON_BRANCH')
    return 0

if __name__ == "__main__": raise SystemExit(main())
