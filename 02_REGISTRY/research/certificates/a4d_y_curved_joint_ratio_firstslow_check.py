#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact first-order isolation of the diagonal ratio in the curved joint symbol.

Use the zone-folded variables lambda_r = mu*rho_r with rho_0=1.  The 68
phase-1/phase-2 output rows do not contain the common Floquet variable
w=mu^4.  At rho=(1,1,1) this interior operator has rank 65, hence a
31-dimensional right kernel and a 3-dimensional left cokernel.

For transverse logarithmic ratio direction x=(x1,x2,x3), form the exact
3x31 first derivative
    R(x)=L^T (x1 D1+x2 D2+x3 D3) N.
Nine selected 3x3 minors give a projective cover: in each affine chart
x_j=1, three minors generate the unit ideal over Q.  Therefore R(x) has
row rank 3 for every nonzero complex x.

Scope: this is a first-order local ratio-isolation theorem.  It does not
prove the global ratio-torus rank or the common-phase/boundary equations.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_joint_rational_stencil as S

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_ratio_firstslow_results.json"

def ck(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)

def row_phase(row):
    return row//24 if row<96 else (row-96)//10

INTERIOR_ROWS=list(range(24,72))+list(range(106,126))
RINDEX={r:i for i,r in enumerate(INTERIOR_ROWS)}
M=sp.zeros(68,96)
D=[sp.zeros(68,96) for _ in range(3)]

for terms,off in ((S.ATERMS,0),(S.QTERMS,96)):
    for d,E in terms.items():
        for (r,c),v0 in E.items():
            row=off+r
            rp=row_phase(row)
            cp=c//24
            power=rp-cp+sum(d)
            ck("ZONE_POWER_DIVISIBLE_"+str(row)+"_"+str(c)+"_"+str(d),power%4==0)
            if rp not in (1,2):
                continue
            # Interior phases carry no common-phase wrap.
            ck("INTERIOR_ZONE_POWER_ZERO_"+str(row)+"_"+str(c)+"_"+str(d),power==0)
            q=sp.Rational(v0.numerator,v0.denominator)
            rr=RINDEX[row]
            M[rr,c]+=q
            for a in range(3):
                D[a][rr,c]+=d[a+1]*q

DM=DomainMatrix.from_Matrix(M).convert_to(QQ)
ck("INTERIOR_SHAPE",M.shape==(68,96))
ck("DIAGONAL_RATIO_INTERIOR_RANK65",DM.rank()==65)

N=DM.nullspace().to_Matrix().T
L=DomainMatrix.from_Matrix(M.T).convert_to(QQ).nullspace().to_Matrix().T
ck("RIGHT_KERNEL_DIM31",N.shape==(96,31))
ck("LEFT_COKERNEL_DIM3",L.shape==(68,3))
ck("RIGHT_KERNEL_EXACT",M*N==sp.zeros(68,31))
ck("LEFT_COKERNEL_EXACT",L.T*M==sp.zeros(3,96))

R=[(L.T*D[a]*N).applyfunc(sp.factor) for a in range(3)]
for a,A in enumerate(R):
    ck("AXIS_FIRSTSLOW_RANK3_"+str(a),DomainMatrix.from_Matrix(A).convert_to(QQ).rank()==3)

x1,x2,x3=sp.symbols("x1 x2 x3")
xs=(x1,x2,x3)
RX=x1*R[0]+x2*R[1]+x3*R[2]

CHART_MINORS={
  0:[(20,24,30),(21,24,30),(17,18,19)],
  1:[(17,21,24),(17,21,30),(18,20,21)],
  2:[(17,21,24),(17,21,30),(18,20,21)],
}
chart_records=[]
for chart,var in enumerate(xs):
    others=[z for z in xs if z!=var]
    polys=[]
    for cols in CHART_MINORS[chart]:
        det=sp.factor(RX[:,list(cols)].det())
        ck("NONZERO_MINOR_CHART_"+str(chart)+"_"+str(cols),det!=0)
        polys.append(sp.factor(det.subs(var,1)))
    G=sp.groebner(polys,*others,order="grevlex",domain=sp.QQ)
    ck("PROJECTIVE_CHART_UNIT_IDEAL_"+str(chart),
       len(G.polys)==1 and G.polys[0].as_expr()==1)
    chart_records.append({
      "chart":str(var)+"=1",
      "minor_column_triples":[list(c) for c in CHART_MINORS[chart]],
      "groebner_basis":["1"],
    })

result={
 "schema":"a4d-y-curved-joint-ratio-firstslow-v1",
 "terminal":"A4D-Y-CURVED-JOINT-DIAGONAL-RATIO-FIRSTSLOW-INJECTIVE",
 "background":"z=1 exact Y vacuum; zone-folded full joint symbol",
 "ratio_coordinates":"rho0=1; rho1,rho2,rho3 transverse to common Bloch phase",
 "interior_rows":"all 24 connection + 10 metric rows in phases 1 and 2",
 "interior_shape":[68,96],
 "rank_at_diagonal_ratio":65,
 "right_kernel_dimension":31,
 "left_cokernel_dimension":3,
 "firstslow_map_shape":[3,31],
 "axis_ranks":[3,3,3],
 "projective_cover":chart_records,
 "conclusion":"L^T (sum_a x_a D_a) N has row rank 3 for every nonzero complex transverse ratio direction x",
 "implication":"rho=(1,1,1) is first-order isolated as an interior-rank-drop ratio; any nearby off-diagonal ratio removes the three extra interior cokernel directions linearly",
 "scope_fence":[
   "first-order local statement near the diagonal ratio only",
   "does not prove global rank 68 of the interior operator on the full ratio torus",
   "does not solve the phase-0/phase-3 boundary equations or common Floquet phase",
   "does not prove the all-Bloch joint zero locus or task-level response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-DIAGONAL-RATIO-FIRSTSLOW-INJECTIVE")
