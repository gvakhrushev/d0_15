#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact local isolation of the four folded curved-Y joint Bloch zeros.

Uses the literal 136x96 Laurent stencil from the mu4 owner.  Delete one
phase-0 Y coordinate, prove an exact 95-column transverse Gram bound at the
folded point, build an exact square graph chart, and show that the reduced
four-angle residual has rank-four derivative.  The same rank-four conclusion
is checked at all four folded copies over Q(i).

This is local analytic isolation, not a global unit-torus zero-locus theorem.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
import a4d_y_curved_joint_mu4_locus_check as M

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_folded_isolation_results.json"
LIP=json.loads((HERE/"a4d_y_curved_joint_torus_lipschitz_results.json").read_text())

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

ROWS=[101,121,112,134,114,132,74,26,37,85,117,119,99,97,72,24,61,13,83,33,35,87,79,29,76,93,25,45,36,28,126,44,90,78,88,54,12,95,55,75,6,66,20,68,64,30,106,16,77,32,40,62,46,43,50,8,73,27,92,11,59,19,98,118,69,102,82,124,41,21,84,9,91,86,1,80,53,111,17,22,81,39,60,4,49,47,67,56,51,65,70,89,94,5,38]
FROWS=[34,31,42,14]
DELCOL=M.LABELS.index((0,0,3))
COLS=[j for j in range(96) if j!=DELCOL]
REST=[r for r in range(136) if r not in set(ROWS)]

def eval_at(zeta):
    return sum((zeta**sum(d)*M.T[d] for d in M.SUPPORT),sp.zeros(136,96))

def deriv_hat(zeta,k):
    return sum((sp.Integer(d[k])*zeta**sum(d)*M.T[d] for d in M.SUPPORT),sp.zeros(136,96))

Q0=eval_at(sp.Integer(1))
Qperp=Q0[:,COLS]
G=(Qperp.T*Qperp).to_DM().convert_to(sp.QQ)
ck("TRANSVERSE_GRAM_RANK95",G.rank()==95)
Ginv=G.inv().to_Matrix()
Ginv_frob2=sp.factor(sum(x*x for x in Ginv))
ck("TRANSVERSE_SIGMA_GT_9_OVER_100",
   Ginv_frob2 < sp.Rational(10000,81)**2)

Lmax=max(sp.Rational(x) for x in LIP["coordinate_derivative_frobenius_upper_bounds"])
ck("EXPLICIT_TRANSVERSE_CHART_RADIUS_1_OVER_300",
   Lmax*sp.Rational(1,300) < sp.Rational(9,100))

S=Q0.extract(ROWS,COLS)
Sinv=S.to_DM().convert_to(sp.QQ).inv().to_Matrix()
Sinv_frob2=sp.factor(sum(x*x for x in Sinv))
ck("SQUARE_GRAPH_SIGMA_GT_1_OVER_40",Sinv_frob2 < sp.Integer(40)**2)
ck("EXPLICIT_SQUARE_CHART_RADIUS_1_OVER_1000",
   Lmax*sp.Rational(1,1000) < sp.Rational(1,40))

q=Q0.extract(ROWS,[DELCOL])
x0=-(Sinv*q)
v0=sp.zeros(96,1); v0[DELCOL]=1
for k,c in enumerate(COLS): v0[c]=x0[k]
ck("GRAPH_VECTOR_IS_FOLDED_KERNEL",Q0*v0==sp.zeros(136,1))

N0=Q0.extract(REST,COLS)
J=sp.zeros(len(REST),4)
for k in range(4):
    D=deriv_hat(sp.Integer(1),k)
    SD=D.extract(ROWS,COLS); qD=D.extract(ROWS,[DELCOL])
    xD=-(Sinv*(qD+SD*x0))
    ND=D.extract(REST,COLS); rD=D.extract(REST,[DELCOL])
    J[:,k]=rD+ND*x0+N0*xD
ck("REDUCED_BLOCH_DERIVATIVE_RANK4",J.rank()==4)
sel=[REST.index(r) for r in FROWS]
J4=J.extract(sel,range(4))
detJ=sp.factor(J4.det())
expected_det=-sp.Rational(62976744635716940958283670688,206230323499945683191645561081)
ck("REDUCED_J4_DETERMINANT",detJ==expected_det)
Jinv=J4.inv(); Jinv_frob2=sp.factor(sum(x*x for x in Jinv))
ck("REDUCED_J4_SIGMA_GT_1_OVER_5",Jinv_frob2 < sp.Integer(5)**2)

folded_ranks=[]
for j,zeta in enumerate(M.ROOTS):
    Q=eval_at(zeta)
    Sfold=Q.extract(ROWS,COLS)
    ck("FOLD_%d_SQUARE_CHART_RANK95"%j,Sfold.to_DM(extension=True).rank()==95)
    Sinvf=Sfold.to_DM(extension=True).inv().to_Matrix()
    xf=-(Sinvf*Q.extract(ROWS,[DELCOL]))
    Nf=Q.extract(REST,COLS)
    Jf=sp.zeros(len(REST),4)
    for k in range(4):
        D=deriv_hat(zeta,k)
        xd=-(Sinvf*(D.extract(ROWS,[DELCOL])+D.extract(ROWS,COLS)*xf))
        Jf[:,k]=D.extract(REST,[DELCOL])+D.extract(REST,COLS)*xf+Nf*xd
    rr=Jf.to_DM(extension=True).rank()
    ck("FOLD_%d_REDUCED_DERIVATIVE_RANK4"%j,rr==4)
    folded_ranks.append(rr)

result={
 "schema":"a4d-y-curved-joint-folded-isolation-v1",
 "terminal":"A4D-Y-CURVED-FOLDED-JOINT-LOCALLY-ISOLATED",
 "deleted_coordinate":"phase0:role0:J12",
 "transverse_columns":95,
 "transverse_gram_inverse_frobenius_squared":str(Ginv_frob2),
 "certified_transverse_sigma_lower":"9/100",
 "explicit_transverse_L1_chart_radius":"1/300",
 "square_graph_rows":ROWS,
 "square_inverse_frobenius_squared":str(Sinv_frob2),
 "certified_square_sigma_lower":"1/40",
 "explicit_square_L1_chart_radius":"1/1000",
 "reduced_residual_rows":FROWS,
 "reduced_J4_determinant":str(detJ),
 "reduced_J4_inverse_frobenius_squared":str(Jinv_frob2),
 "certified_reduced_derivative_sigma_lower":"1/5",
 "folded_reduced_derivative_ranks":folded_ranks,
 "conclusion":"each of the four folded rank-95 joint characters is an analytically isolated Bloch zero; no additional joint zeros can accumulate into a folded point",
 "scope_fence":[
   "local analytic isolation only",
   "the 95-column transverse chart has an explicit L1 neighborhood, but the inverse-function uniqueness radius for the full reduced residual is not quantified here",
   "no global compact-complement zero-locus theorem",
   "no nonlinear range theorem or task-level response terminal"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n"); print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-FOLDED-JOINT-LOCALLY-ISOLATED")
