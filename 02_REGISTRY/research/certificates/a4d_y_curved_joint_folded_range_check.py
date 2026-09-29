#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact transverse Lyapunov-Schmidt range chart at the four folded Y points.

Consumes the literal curved-z=1 joint Bloch Laurent stencil from
a4d_y_curved_joint_torus_lipschitz_check.py.  At each diagonal folded
character lambda in {1,i,-1,-i}, delete one nonzero coordinate of the exact
Y kernel and select the same 95 output rows.  The resulting 95x95 matrix is
invertible over Q(i).

The exact Hermitian Frobenius norm of its inverse is the same at all four
folded points and is < 36.  Combined with the separately certified global
joint-symbol Lipschitz constant 22/7, a Neumann argument gives a uniform
transverse inverse bound < 72 whenever the l1 angular distance from a folded
point is <= 7/1584.

This is a local folded-neighbourhood range theorem.  It is not a global
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
ROOTS=(sp.Integer(1),sp.I,sp.Integer(-1),-sp.I)

ROWS=[
101,121,112,134,114,132,74,26,37,85,117,119,99,97,72,24,61,13,83,33,
35,87,79,29,76,93,25,45,36,28,126,44,90,78,88,54,12,95,55,75,6,66,
20,68,64,30,106,16,77,32,40,62,46,43,50,8,73,27,92,11,59,19,98,118,
69,102,82,124,41,21,84,9,91,86,1,80,53,111,17,22,81,39,60,4,49,47,
67,56,51,65,70,89,94,5,38
]
DROP_LABEL=(0,0,3)
INV_FROB2=sp.Rational(
43923078667642902989968245702126572877287354217317226275940068803,
34722123986370742942017772636917718807712583361717519055864544,
)

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name,flush=True)

def joint_at_diagonal(z):
    return sum((z**sum(d)*L.T[d] for d in L.support),sp.zeros(136,96))

drop=L.LABELS.index(DROP_LABEL)
cols=[j for j in range(96) if j!=drop]
ck("RANGE_CHART_DIMENSIONS",len(ROWS)==95 and len(set(ROWS))==95 and len(cols)==95)
ck("DROPPED_COORDINATE_IS_PHASE0_Y_COMPONENT",DROP_LABEL==(0,0,3))

records=[]
for ri,z in enumerate(ROOTS):
    Q=joint_at_diagonal(z)
    v=sp.zeros(96,1)
    for g,c in ((3,1),(4,-1),(5,1)):
        v[L.LABELS.index((0,0,g)),0]=c
        v[L.LABELS.index((2,0,g)),0]=-z**2*c
    ck("EXACT_Y_KERNEL_"+str(ri),Q*v==sp.zeros(136,1) and v[drop]!=0)

    M=Q.extract(ROWS,cols)
    ck("FOLDED_RANGE_MINOR_RANK95_"+str(ri),M.to_DM(extension=True).rank()==95)
    Minv=M.inv()
    n2=sp.simplify(sum(sp.conjugate(x)*x for x in Minv))
    ck("COMMON_INVERSE_FROBENIUS_NORM_"+str(ri),n2==INV_FROB2)
    ck("INVERSE_OPERATOR_BOUND_36_"+str(ri),n2<36**2)
    records.append({
      "root_index":ri,
      "lambda":str(z),
      "minor_rank":95,
      "inverse_frobenius_norm_squared":str(n2),
      "inverse_operator_bound":"<36"
    })

# If ||theta-theta_*||_1 <= r, then ||delta M||_2 <= (22/7) r.
# At r=7/1584 this is <=1/72, hence ||M_*^-1 delta M||<36/72=1/2.
radius=sp.Rational(7,1584)
delta=sp.Rational(22,7)*radius
ck("NEUMANN_DELTA_BOUND",delta==sp.Rational(1,72))
ck("NEUMANN_PRODUCT_STRICT_HALF",sp.sqrt(INV_FROB2)*delta<sp.Rational(1,2))
inverse_near_bound=sp.Integer(72)

result={
 "schema":"a4d-y-curved-joint-folded-range-v1",
 "terminal":"A4D-Y-CURVED-JOINT-FOLDED-TRANSVERSE-RANGE-CERTIFIED",
 "z":"1",
 "operator_shape":[136,96],
 "dropped_connection_coordinate":{
   "label":list(DROP_LABEL),
   "meaning":"phase-0 role-0 J12; nonzero on the exact Y kernel"
 },
 "selected_output_rows":ROWS,
 "selected_metric_row_count":sum(r>=96 for r in ROWS),
 "folded_points":records,
 "common_inverse_frobenius_norm_squared":str(INV_FROB2),
 "folded_inverse_operator_bound":"<36",
 "global_joint_lipschitz_per_coordinate":"22/7",
 "angular_metric":"l1 in theta coordinates, lambda_j=exp(i theta_j)",
 "certified_neighbourhood_radius":str(radius),
 "perturbation_bound_at_radius":"1/72",
 "neighbourhood_inverse_operator_bound":"<72",
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
