#!/usr/bin/env python3
"""Temporary exact codegen for WRK-A4D-SCHUR-EINSTEIN-DIRECT-LEAN.

Reads the merged #270 owner only through K_SCHUR, then emits compact JSON for
A0, A0_INV, and the four momentum coefficients of C1.  It mutates nothing.
This helper is removed once the standalone Lean constants are generated.
"""
from __future__ import annotations
import json
import os
import sympy as sp

HERE=os.path.dirname(os.path.abspath(__file__))
OWNER=os.path.join(HERE,"a4d_metric_null_hessian_complex_check.py")
src=open(OWNER,encoding="utf-8").read()
cut=src.index("# Exact E_eta quadratic symbol in the #201 convention.")
ns={"__name__":"_lean_codegen_owner","__file__":OWNER}
exec(compile(src[:cut],OWNER,"exec"),ns)
A0=ns["A0"]; A0I=ns["A0_INV"]; C=ns["C"]; d=ns["d"]

def rat(x):
    x=sp.Rational(x)
    return [int(x.p),int(x.q)]

def mat(M):
    return [[rat(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]

cc=[]
for i in range(C.rows):
    row=[]
    for j in range(C.cols):
        p=sp.Poly(sp.expand(C[i,j]),*d)
        row.append([rat(p.coeff_monomial(d[r])) for r in range(4)])
    cc.append(row)

payload={"A0":mat(A0),"A0I":mat(A0I),"Ccoef":cc}
print("LEAN_CODEGEN_JSON="+json.dumps(payload,separators=(",",":")))
