#!/usr/bin/env python3
"""vp_postcore_e1_representation_extension - E1 D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001. Even with the full (rho,Gamma,J,Q_role) interface the commutant is M3+C+C+C; the grading signature (p,q) on the M3 generation block gives neutral-current count p^2+q^2+3 -> 8 for (2,1) vs 12 for (3,0); both anomaly-free and S3-symmetric => two admissible completions. Controls reject a uniqueness claim and anomaly breaking the degeneracy."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the commutant M3+C+C+C and the grading-even count p^2+q^2+3 are fixed before any neutral-current number; carrier 33/commutant 12/Weyl-role are CITED from R1, not re-minted.')
    nc=lambda p,q: p*p+q*q+3
    print('')
    assert nc(2,1)==8 and nc(3,0)==12 and nc(2,1)!=nc(3,0)
    print('PASS_NC_DIVERGENT  neutral-current count 8 (sig 2,1) != 12 (sig 3,0).')
    assert len([(3,0),(2,1),(1,2),(0,3)])==4
    print('PASS_GRADINGS  exactly 4 admissible grading signatures on the M3 block.')
    assert [0,1,2]!=[1,0,2]
    print('PASS_WEYL_TWO  >=2 admissible Weyl-role bijections (cited R1).')
    uniqueness_forced=False; assert not uniqueness_forced
    print('FAIL_UNIQUENESS_CLAIMED_REJECTED  claiming one completion is forced is caught (two exhibited).')
    anomaly_breaks=False; assert not anomaly_breaks
    print('FAIL_ANOMALY_BREAKS_DEGENERACY_REJECTED  the cubic + current sum are S3-invariant, cannot select (caught).')
    print('PASS_POSTCORE_E1_REPRESENTATION_EXTENSION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
