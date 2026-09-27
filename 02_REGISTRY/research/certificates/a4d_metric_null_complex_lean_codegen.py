#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Temporary exact certificate generator for A4DMetricNullHessianComplex Lean.

Reads merged #292 coefficient JSON, reconstructs C(d), and exports the eleven
#270 projective 9x9 minors as unnormalized polynomial matrices with exact
determinant and adjugate certificates. Removed before REVIEW.
"""
from __future__ import annotations
import json, os, sympy as sp

HERE=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(HERE,"a4d_haq_coefficientwise_identity_coefficients.json")
J=json.load(open(DATA,encoding="utf-8"))
d=sp.symbols("d0:4")
C=sp.zeros(24,10)
for r in range(4):
    M=J["C_r"][r]["matrix"]
    for i in range(24):
        for j in range(10):
            C[i,j]+=d[r]*sp.Rational(M[i][j])

SPECS={
0:[
((6,7,8,9,10,13,14,15,20),(1,2,3,4,5,6,7,8,9)),
((0,1,2,4,5,6,7,10,13),(0,1,2,3,4,5,6,7,8)),
],
1:[
((0,1,2,3,4,13,15,16,22),(0,1,2,3,5,6,7,8,9)),
((0,1,2,3,4,6,9,10,15),(0,1,2,3,4,5,6,7,8)),
((0,1,2,3,4,7,9,10,15),(0,1,2,3,4,5,6,7,8)),
],
2:[
((0,1,2,3,5,6,9,11,23),(0,1,2,3,4,5,6,8,9)),
((0,1,2,3,4,7,9,10,15),(0,1,2,3,4,5,6,7,8)),
((0,1,2,3,5,9,13,15,17),(0,1,2,3,4,5,6,7,8)),
],
3:[
((0,1,2,4,5,6,10,11,17),(0,1,2,3,4,5,6,7,8)),
((0,1,2,3,4,7,9,10,15),(0,1,2,3,4,5,6,7,8)),
((0,1,2,3,5,9,13,15,17),(0,1,2,3,4,5,6,7,8)),
]}

def poly_text(x):
    return str(sp.factor(sp.cancel(x)))

def sparse_matrix(M):
    out=[]
    for i in range(M.rows):
        for j in range(M.cols):
            v=sp.factor(sp.cancel(M[i,j]))
            if v!=0:
                out.append([i,j,str(v)])
    return out

payload={}
for ch,specs in SPECS.items():
    rec=[]
    for n,(rows,cols) in enumerate(specs):
        B=C.extract(rows,cols)
        det=sp.factor(B.det())
        adj=B.adjugate().applyfunc(lambda x: sp.factor(sp.cancel(x)))
        assert sp.simplify(B*adj-det*sp.eye(9))==sp.zeros(9)
        assert sp.simplify(adj*B-det*sp.eye(9))==sp.zeros(9)
        rec.append({
          "rows":list(rows),"cols":list(cols),
          "det":str(det),"adj":sparse_matrix(adj),
        })
        print(f"PASS_CHART_{ch}_MINOR_{n}_ADJUGATE entries={len(rec[-1]['adj'])}")
    payload[str(ch)]=rec

print("A4D_METRIC_NULL_LEAN_JSON="+json.dumps(payload,separators=(",",":")))
print("A4D-METRIC-NULL-LEAN-CODEGEN-EXACT")
