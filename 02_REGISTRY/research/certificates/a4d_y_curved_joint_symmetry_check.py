#!/usr/bin/env python3
"""Exact discrete symmetries of the curved z=1 full joint Bloch stencil.

Certifies three symmetries used to reduce the physical unit-torus spectral
problem:

1. common quarter shift:
   Q(zeta*lambda)=D_out(zeta) Q(lambda) D_in(zeta), zeta^4=1;
2. full spatial S3:
   the even 3-cycle acts by the natural spatial coordinate/role/generator
   permutation, while an odd swap is accompanied by fast-phase p -> p+2
   because it sends Y -> -Y and hence U <-> U^-1;
3. physical inversion:
   Q(exp(-i theta)) = conjugate(Q(exp(i theta))) because every Laurent
   coefficient is rational-real.

Thus rank and singular values are constant on the generated physical orbit,
whose generic size is 4*6*2=48.  The certificate does not construct a global
fundamental-domain cover or prove the all-Bloch rank theorem by itself.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

import a4d_y_curved_joint_torus_lipschitz_check as L

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_symmetry_results.json"


def ck(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)


COEFF={}
rational_real=True
for d,M in L.T.items():
    for (r,c),v in M.todok().items():
        if v:
            q=sp.Rational(v)
            rational_real = rational_real and bool(q.is_Rational)
            COEFF[(d,r,c)]=q
ck("ALL_LAURENT_COEFFICIENTS_RATIONAL_REAL",rational_real)
ck("COEFFICIENT_LEDGER_NONEMPTY",len(COEFF)>0)


def row_phase(row):
    return row//24 if row<96 else (row-96)//10


def col_phase(col):
    return col//24


# Common quarter multiplication of all four Bloch characters.
quarter_ok=all(
    sum(d)%4==(col_phase(c)-row_phase(r))%4
    for d,r,c in COEFF
)
ck("GLOBAL_COMMON_QUARTER_COVARIANCE",quarter_ok)


SYM=L.B.SYM
METRIC_INDEX={pair:i for i,pair in enumerate(SYM)}


def check_spatial_symmetry(name,pi,gmap,phase_shift):
    invpi={v:k for k,v in pi.items()}

    def map_col(c):
        p,role,g=L.LABELS[c]
        gp,sg=gmap[g]
        return L.LABELS.index(((p+phase_shift)%4,pi[role],gp)),sg

    def map_row(r):
        if r<96:
            return map_col(r)
        phase=(r-96)//10
        mi=(r-96)%10
        a,b=SYM[mi]
        aa,bb=pi[a],pi[b]
        pair=(aa,bb) if aa<=bb else (bb,aa)
        return 96+10*((phase+phase_shift)%4)+METRIC_INDEX[pair],1

    ok=True
    for (d,r,c),v in COEFF.items():
        rr,sr=map_row(r)
        cc,sc=map_col(c)
        dd=tuple(d[invpi[k]] for k in range(4))
        if COEFF.get((dd,rr,cc),sp.Integer(0))!=sr*sc*v:
            ok=False
            break
    ck(name,ok)


# Even cycle 1->2->3->1.  It fixes Y exactly.
cycle={0:0,1:2,2:3,3:1}
cycle_g={
  0:(1,1), 1:(2,1), 2:(0,1),
  3:(5,1), 4:(3,-1), 5:(4,-1),
}
check_spatial_symmetry("SPATIAL_C3_COVARIANCE",cycle,cycle_g,0)

# Odd transposition 2<->3 sends Y -> -Y.  Fast phase +2 interchanges the
# U and U^-1 background phases and restores the owned curved cell.
swap={0:0,1:1,2:3,3:2}
swap_g={
  0:(0,1), 1:(2,1), 2:(1,1),
  3:(4,1), 4:(3,1), 5:(5,-1),
}
check_spatial_symmetry("SPATIAL_ODD_SWAP_WITH_PHASE2_COVARIANCE",
                       swap,swap_g,2)

# The cycle and one transposition generate S3.
result={
 "schema":"a4d-y-curved-joint-symmetry-v1",
 "terminal":"A4D-Y-CURVED-JOINT-DISCRETE-SYMMETRIES-CERTIFIED",
 "operator_shape":[136,96],
 "laurent_coefficient_count":len(COEFF),
 "symmetries":{
   "common_quarter":{
     "action":"lambda -> zeta lambda, zeta^4=1",
     "operator":"Q(zeta lambda)=D_out(zeta) Q(lambda) D_in(zeta)"
   },
   "spatial_S3":{
     "even_generator":"cycle 1->2->3->1",
     "odd_generator":"swap 2<->3 plus fast-phase p->p+2",
     "note":"odd generator sends Y to -Y before the phase-2 restoration"
   },
   "physical_inversion":{
     "action":"theta -> -theta",
     "reason":"all Laurent coefficient matrices are rational-real, so on |lambda|=1 Q(lambda^-1)=conjugate(Q(lambda))"
   }
 },
 "generic_physical_orbit_size":48,
 "cover_use":"a physical unit-torus rank/gap cover may be reduced by these exact orbit symmetries before certification",
 "scope_fence":[
   "exact stencil covariance only",
   "no explicit fundamental-domain tiling is certified here",
   "no all-Bloch rank or positive-gap theorem",
   "no nonlinear response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)

print("TERMINAL A4D-Y-CURVED-JOINT-DISCRETE-SYMMETRIES-CERTIFIED")
