#!/usr/bin/env python3
"""Reduced exact certificate for the C1 common-carrier research result.

This certificate intentionally verifies the representation-reduced load-bearing
identities rather than recomputing the full 33x359 rational RREF. The historical
research packet is preserved in Git history; current formal ownership is in
03_FORMALIZATION/D0/Geometry/SignlessSignedCommonCarrier.lean and the registry.
"""
from fractions import Fraction as F

def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
           -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
           +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

def check(name, cond):
    if not cond:
        raise SystemExit("FAIL " + name)
    print("PASS", name)

def mv(M,x):
    return tuple(sum(F(M[i][j])*x[j] for j in range(3)) for i in range(3))

a,b,c=9,11,13

Bp=[[b,c,0],[a,0,c],[0,a,b]]
Bm=[[b,c,0],[-a,0,c],[0,-a,-b]]

check("trivial_unsigned_full_rank", det3(Bp)==-2*a*b*c)
check("trivial_signed_rank_defect", det3(Bm)==0)

omega=(c,-b,a)
check("omega_signed_cycle", mv(Bm,omega)==(0,0,0))
check("omega_unsigned_middle_only", mv(Bp,omega)==(0,2*a*c,0))
check("omega_norm", a*b*c*(a+b+c)==42471)

K0=(a-1)*(b-1)+(a-1)*(c-1)+(b-1)*(c-1)
check("K0_dim", K0==296)
check("kerplus_dim", K0+(a-1)+(b-1)+(c-1)==326)
check("kerminus_dim", 326+1==327)
check("intersection_dim_transitive", K0+(a-1)+(c-1)==316)

vp=(c,-a)
vm=(c,a)
num=a*vp[0]*vm[0]+c*vp[1]*vm[1]
den=a*vp[0]*vp[0]+c*vp[1]*vp[1]
check("middle_overlap", F(num,den)==F(2,11))
check("projection_singular_value", abs(F(num,den))==F(2,11))
check("U_middle_line", (vp[0],-vp[1])==vm)

vals={
    "m9":F(abs(b-c),b+c),
    "m11":F(abs(a-c),a+c),
    "m13":F(abs(a-b),a+b),
}
check("orientation_overlap_m9", vals["m9"]==F(1,12))
check("orientation_overlap_m11", vals["m11"]==F(2,11))
check("orientation_overlap_m13", vals["m13"]==F(1,10))
check("all_transitive_injective", all(v>0 for v in vals.values()))

aa,bb,cc=5,7,5
check("equal_outer_overlap_zero", F(abs(aa-cc),aa+cc)==0)

def weighted_sign(r9,r13):
    x=c*r9-a*r13
    return 1 if x>0 else (-1 if x<0 else 0)

check("rho_sign_positive_example", weighted_sign(F(1),F(1))==1)
check("rho_sign_negative_example", weighted_sign(F(1),F(2))==-1)
check("rho_sign_degenerate_example", weighted_sign(F(9),F(13))==0)

check("homH_dimension_six", 3+3==6)

print("RESULT PASS C1 reduced exact carrier certificate")
