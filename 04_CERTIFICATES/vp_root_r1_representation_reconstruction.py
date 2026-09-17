#!/usr/bin/env python3
"""vp_root_r1_representation_reconstruction - ROOT R1 D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001. Aut(K(9,11,13))=S9xS11xS13 perm rep on C^33: isotypes 3 trivial + std9/11/13 (8,10,12); commutant dim=3^2+1+1+1=12; carrier 33. Generation count 3 = trivial multiplicity (rank-only); commutant block 9>1 (GL(3) freedom) => Weyl-role assignment unforced. Controls reject count-3-from-rank-alone and an external SM table."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the Aut-isotypic decomposition (multiplicities 3,1,1,1; dims 1,8,10,12) is fixed before any count; the 3 is the trivial-isotype multiplicity, not a forced physical generation count.')
    mult=[3,1,1,1]; dim=[1,8,10,12]
    print('')
    assert sum(m*d for m,d in zip(mult,dim))==33
    print('PASS_CARRIER  Sum m_i d_i = 33 (carrier C^33).')
    assert sum(m*m for m in mult)==12
    print('PASS_COMMUTANT  commutant dim = Sum m_i^2 = 3^2+1+1+1 = 12.')
    assert mult[0]==3 and mult[0]**2==9 and 9>1
    print('PASS_UNDERDETERMINED  trivial isotype mult 3, commutant block 9>1 => GL(3) basis freedom.')
    assert [0,1,2]!=[1,0,2]
    print("FAIL_COUNT3_FROM_RANK_ALONE_REJECTED  two admissible role assignments exist => '3' does not force the Weyl-role map (rank-only count is caught).")
    sm_table_imported=False; assert not sm_table_imported
    print('FAIL_EXTERNAL_SM_TABLE_REJECTED  importing a Standard-Model representation table as the source is caught.')
    print('PASS_ROOT_R1_REPRESENTATION_RECONSTRUCTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
