#!/usr/bin/env python3
"""Exact quadratic envelope symbol of the two-dimensional Y stationary center."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
import a4d_y_curved_response_quotient_check as B
import a4d_y_curved_normaljet_compatibility_check as C

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"02_REGISTRY/research/certificates/a4d_y_center_envelope_symbol_results.json"

def check(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n)

def mj(M): return [[str(sp.factor(M[i,j])) for j in range(M.cols)] for i in range(M.rows)]

H,labels,faces0=B.action_connection_hessian(sp.Integer(1))
faces=C.with_base_phases(faces0)
N=C.centers(H,labels,sp.Integer(1))
A1,A2,*_=C.blocks_all(H,faces,labels)
Y=[B.bordered_solve(H,N,-A1[i]*N) for i in range(4)]
K={}
for i,j in C.DIRPAIRS:
    if i==j:
        K[(i,j)]=(N.T*(A2[(i,j)]*N+A1[i]*Y[i])).applyfunc(sp.factor)
    else:
        K[(i,j)]=(N.T*(A2[(i,j)]*N+A1[i]*Y[j]+A1[j]*Y[i])).applyfunc(sp.factor)
check("CENTER_SYMBOL_DIAGONAL",all(M[0,1]==0 and M[1,0]==0 for M in K.values()))

t=sp.symbols("t0:4"); s=t[1]+t[2]+t[3]
r2=t[1]**2+t[2]**2+t[3]**2-s**2/3
S=sp.zeros(2)
for (i,j),M in K.items(): S += M*t[i]*t[j]
S=S.applyfunc(sp.factor)

Q1=26250*(t[0]-sp.Rational(16,75)*s)**2-sp.Rational(2283779,2)*r2
Q2=882*(t[0]-sp.Rational(16,21)*s)**2-sp.Rational(603687,2)*r2
expected1=sp.factor(-sp.Rational(2,188307)*Q1)
expected2=sp.factor(-sp.Rational(1,6408)*Q2)
check("Y_ENVELOPE_TRANSPORTED_WAVE_FORM",sp.factor(S[0,0]-expected1)==0)
check("DUAL_ENVELOPE_TRANSPORTED_WAVE_FORM",sp.factor(S[1,1]-expected2)==0)
check("TIME_COEFFICIENTS_NONZERO",K[(0,0)].det()!=0)

result={
 "schema":"a4d-y-center-envelope-symbol-v1",
 "z":"1",
 "center_basis":["Y tangent","boost-dual tangent"],
 "quadratic_coefficients":{f"{i}{j}":mj(M) for (i,j),M in K.items()},
 "symbol":mj(S),
 "transported_wave_forms":{
   "Y":"-2/188307 * [26250*(t0-16*s/75)^2-(2283779/2)*r_perp^2]",
   "dual":"-1/6408 * [882*(t0-16*s/21)^2-(603687/2)*r_perp^2]",
   "s":"t1+t2+t3",
   "r_perp^2":"t1^2+t2^2+t3^2-s^2/3"
 },
 "interpretation":"two decoupled transported 2+1 hyperbolic center envelopes; no elliptic spectral gap",
 "nonclaim":"quadratic principal symbol only; nonlinear envelope existence and energy estimate remain open"
}
if OUT.exists():
    check("RESULTS_MATCH_PINNED_JSON",result==json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
print("TERMINAL A4D-Y-CENTER-ENVELOPE-PRINCIPAL-SYMBOL-CERTIFIED")
