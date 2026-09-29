#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact transverse Lyapunov-Schmidt range chart at the four folded Y points.

Consumes the literal curved-z=1 joint Bloch Laurent stencil from
a4d_y_curved_joint_torus_lipschitz_check.py.  At lambda=(1,1,1,1), delete
one nonzero coordinate of the exact Y kernel and select 95 output rows.  The
resulting 95x95 matrix is invertible over Q.

The stencil also proves diagonal fourth-root phase covariance entry by entry:
for every nonzero Laurent coefficient, sum(d) == p_col-p_row mod 4.  Hence
Q(z,z,z,z)=D_out(z) Q(1,1,1,1) D_in(z) for z^4=1, with unit-modulus diagonal
phase matrices.  The same selected minor is therefore invertible at all four
folded copies with exactly the same singular values and inverse Frobenius norm.

The exact Hermitian Frobenius norm of the inverse is < 31. Combined with the
separately certified global joint-symbol Lipschitz constant 22/7, a Neumann
argument gives a uniform transverse inverse bound < 62 whenever the l1
angular distance from a folded point is <= 7/1364.

This is a local folded-neighbourhood range theorem. It is not a global
all-Bloch zero-locus theorem and does not solve the reduced nonlinear center
equation.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

import a4d_y_curved_joint_torus_lipschitz_check as L

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_folded_range_results.json"

ROWS=[
101,121,112,134,114,132,25,73,30,78,119,99,118,98,74,26,6,117,40,87,
88,29,33,32,72,76,45,36,54,93,92,106,37,35,43,77,19,13,12,27,46,8,
61,85,68,20,11,126,83,28,69,95,75,44,66,2,48,55,86,41,21,64,62,9,
105,24,59,80,91,81,84,16,79,5,63,102,18,94,90,3,89,71,50,10,7,111,
14,53,0,47,42,52,38,1,97
]
DROP_LABEL=(0,0,4)
INV_FROB2=sp.Rational(
1449607289608826796462600607206428282020098585931893046315145431,
1525932452501592103567428379487267246378717660095190382527232,
)

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name,flush=True)

def row_phase(row):
    return row//24 if row<96 else (row-96)//10

def col_phase(col):
    return col//24

# Each Laurent cell has a unique phase exponent mod 4 on the diagonal.
seen={}
for d,M in L.T.items():
    e=sum(d)%4
    for (r,c),v in M.todok().items():
        if v==0: continue
        ck("PHASE_EXPONENT_"+str(r)+"_"+str(c)+"_"+str(d),
           e==(col_phase(c)-row_phase(r))%4)
        key=(r,c)
        if key in seen:
            ck("CELL_PHASE_EXPONENT_CONSISTENT_"+str(r)+"_"+str(c),seen[key]==e)
        else:
            seen[key]=e
ck("ALL_JOINT_CELLS_PHASE_COVARIANT",len(seen)>0)

Q0=sum((M for M in L.T.values()),sp.zeros(136,96))
drop=L.LABELS.index(DROP_LABEL)
cols=[j for j in range(96) if j!=drop]
ck("RANGE_CHART_DIMENSIONS",len(ROWS)==95 and len(set(ROWS))==95 and len(cols)==95)
ck("DROPPED_COORDINATE_IS_PHASE0_Y_COMPONENT",DROP_LABEL==(0,0,4))

v=sp.zeros(96,1)
for g,c in ((3,1),(4,-1),(5,1)):
    v[L.LABELS.index((0,0,g)),0]=c
    v[L.LABELS.index((2,0,g)),0]=-c
ck("EXACT_Y_KERNEL_AT_ONE",Q0*v==sp.zeros(136,1) and v[drop]!=0)

M0=Q0.extract(ROWS,cols)
ck("FOLDED_RANGE_MINOR_RANK95",M0.to_DM().rank()==95)
Minv=M0.inv()
n2=sp.factor(sum(x*x for x in Minv))
ck("PINNED_INVERSE_FROBENIUS_NORM",n2==INV_FROB2)
ck("INVERSE_OPERATOR_BOUND_31",n2<31**2)

# For z^4=1, diagonal phase covariance is implemented by unitary diagonal
# row/column factors. Therefore the selected minor has identical singular
# values and inverse Frobenius norm at all four folded copies.
for z in (sp.Integer(1),sp.I,sp.Integer(-1),-sp.I):
    Dr=sp.diag(*[z**(-row_phase(r)) for r in ROWS])
    Dc=sp.diag(*[z**col_phase(c) for c in cols])
    Qz=sum((z**sum(d)*L.T[d] for d in L.support),sp.zeros(136,96))
    ck("DIAGONAL_PHASE_COVARIANCE_"+str(z),
       Qz.extract(ROWS,cols)==Dr*M0*Dc)

# If ||theta-theta_*||_1 <= r, then ||delta M||_2 <= (22/7) r.
# At r=7/1364 this is <=1/62, hence ||M_*^-1 delta M||<31/62=1/2.
radius=sp.Rational(7,1364)
delta=sp.Rational(22,7)*radius
ck("NEUMANN_DELTA_BOUND",delta==sp.Rational(1,62))
ck("NEUMANN_PRODUCT_STRICT_HALF",sp.sqrt(INV_FROB2)*delta<sp.Rational(1,2))

result={
 "schema":"a4d-y-curved-joint-folded-range-v2",
 "terminal":"A4D-Y-CURVED-JOINT-FOLDED-TRANSVERSE-RANGE-CERTIFIED",
 "z":"1",
 "operator_shape":[136,96],
 "dropped_connection_coordinate":{
   "label":list(DROP_LABEL),
   "meaning":"phase-0 role-0 J13; nonzero on the exact Y kernel"
 },
 "selected_output_rows":ROWS,
 "selected_metric_row_count":sum(r>=96 for r in ROWS),
 "phase_covariance":{
   "statement":"Q(z,z,z,z)=D_out(z) Q(1,1,1,1) D_in(z) for z^4=1",
   "row_factor":"z^(-phase(row))",
   "column_factor":"z^(phase(column))",
   "consequence":"the selected folded minor has identical singular values at 1,i,-1,-i"
 },
 "minor_rank":95,
 "common_inverse_frobenius_norm_squared":str(INV_FROB2),
 "folded_inverse_operator_bound":"<31",
 "global_joint_lipschitz_per_coordinate":"22/7",
 "angular_metric":"l1 in theta coordinates, lambda_j=exp(i theta_j)",
 "certified_neighbourhood_radius":str(radius),
 "perturbation_bound_at_radius":"1/62",
 "neighbourhood_inverse_operator_bound":"<62",
 "lyapunov_schmidt_use":"the 95 selected equations solve uniquely for the 95 transverse connection coordinates; the remaining equations are reduced compatibility/center equations",
 "scope_fence":[
   "uniform over all four folded copies",
   "local folded neighbourhood only",
   "no global all-Bloch rank theorem",
   "no nonlinear reduced-center solvability theorem",
   "no task-level response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)

print("TERMINAL A4D-Y-CURVED-JOINT-FOLDED-TRANSVERSE-RANGE-CERTIFIED")
