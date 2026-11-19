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

The exact inverse is first pinned by its Hermitian Frobenius norm. A stronger
rational Collatz certificate for H=M^{-T}M^{-1} proves ||M^{-1}||_2 < 20.
Combined with the separately certified global joint-symbol Lipschitz constant
22/7, a Neumann argument gives a uniform transverse inverse bound < 40
whenever the l1 angular distance from a folded point is <= 7/880.

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
COLLATZ_WEIGHTS=[
4186,2883,4084,3272,1925,5886,2923,9046,3598,3860,3745,6986,8018,4262,6601,
3500,3946,4224,4356,1541,7088,3534,2001,5849,4089,2476,6238,4054,2212,5919,
2398,6291,3227,1672,8504,2897,1785,1997,6314,3149,2123,4965,3023,1484,1773,
1000,4011,7212,1049,2399,1572,1690,3546,1921,4123,6820,5369,3639,3344,1417,
1425,1328,6487,8231,1303,2660,3705,2507,8246,6203,8647,4027,8403,7003,3760,
2729,5152,4438,6162,3528,7793,3439,6136,2739,3583,3389,4015,2949,3634,6648,
9046,3126,6593,5721,11551
]
COLLATZ_MAX=sp.Rational(
39324659450219131318503292696502016712938627281350055258788171173083,
100748164243965117045935891327267332674908454790124849815977965568,
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
phase_ok=True
for d,M in L.T.items():
    e=sum(d)%4
    for (r,c),v in M.todok().items():
        if v==0:
            continue
        phase_ok = phase_ok and e==(col_phase(c)-row_phase(r))%4
        key=(r,c)
        if key in seen:
            phase_ok = phase_ok and seen[key]==e
        else:
            seen[key]=e
ck("ALL_JOINT_CELLS_PHASE_COVARIANT",phase_ok and len(seen)>0)

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
H=Minv.T*Minv
ck("COLLATZ_WEIGHT_DIMENSION",len(COLLATZ_WEIGHTS)==95 and min(COLLATZ_WEIGHTS)>0)
collatz=[
    sp.factor(sum(abs(H[i,j])*COLLATZ_WEIGHTS[j] for j in range(95))
              /COLLATZ_WEIGHTS[i])
    for i in range(95)
]
ck("PINNED_COLLATZ_MAX",max(collatz)==COLLATZ_MAX)
ck("INVERSE_OPERATOR_BOUND_20",COLLATZ_MAX<20**2)

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
# At r=7/880 this is <=1/40, hence ||M_*^-1 delta M||<20/40=1/2.
radius=sp.Rational(7,880)
delta=sp.Rational(22,7)*radius
ck("NEUMANN_DELTA_BOUND",delta==sp.Rational(1,40))
ck("NEUMANN_PRODUCT_STRICT_HALF",sp.sqrt(COLLATZ_MAX)*delta<sp.Rational(1,2))

result={
 "schema":"a4d-y-curved-joint-folded-range-v3",
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
 "folded_inverse_frobenius_bound":"<31",
 "collatz_max_ratio":str(COLLATZ_MAX),
 "folded_inverse_operator_bound":"<20",
 "global_joint_lipschitz_per_coordinate":"22/7",
 "angular_metric":"l1 in theta coordinates, lambda_j=exp(i theta_j)",
 "certified_neighbourhood_radius":str(radius),
 "perturbation_bound_at_radius":"1/40",
 "neighbourhood_inverse_operator_bound":"<40",
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
