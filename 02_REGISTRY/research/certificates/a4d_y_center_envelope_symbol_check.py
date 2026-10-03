#!/usr/bin/env python3
"""Exact quadratic envelope symbol of the two-dimensional Y stationary center."""
from __future__ import annotations
import argparse
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

# Exact spectra distinguish the propagating soft lines from the stationary
# spatial sector. Do not infer these facts from numerical eigenvalues.
rho=sp.symbols("rho")
stationary_spectra={}
spectral_specs=(
 ("Y",0,sp.Matrix([sp.Rational(16,25),1,1,1]),
  rho*(3087*rho-37439)**2*(26901*rho+8524)/256354935669,
  (3087*rho-37439)**2*(26901*rho+1024)/256354935669,
  ["0","-8524/26901","37439/3087 (multiplicity 2)"],
  ["-1024/26901","37439/3087 (multiplicity 2)"]),
 ("dual",1,sp.Matrix([sp.Rational(16,7),1,1,1]),
  rho*(48*rho-2261)**2*(1068*rho+403)/2460672,
  (48*rho-2261)**2*(267*rho+64)/615168,
  ["0","-403/1068","2261/48 (multiplicity 2)"],
  ["-64/267","2261/48 (multiplicity 2)"]),
)
for name,index,soft,full_expected,stationary_expected,full_roots,stationary_roots in spectral_specs:
    A=sp.hessian(S[index,index],t)/2
    Astat=A[1:,1:]
    full_char=sp.factor(A.charpoly(rho).as_expr())
    stat_char=sp.factor(Astat.charpoly(rho).as_expr())
    check(name+"_EXACT_FULL_CHARACTERISTIC_POLYNOMIAL",sp.factor(full_char-full_expected)==0)
    check(name+"_EXACT_STATIONARY_CHARACTERISTIC_POLYNOMIAL",sp.factor(stat_char-stationary_expected)==0)
    check(name+"_SOFT_LINE_HAS_NONZERO_TIME_COMPONENT",A*soft==sp.zeros(4,1) and soft[0]!=0)
    if name=="Y":
        negative,positive= -sp.Rational(1024,26901),sp.Rational(37439,3087)
    else:
        negative,positive= -sp.Rational(64,267),sp.Rational(2261,48)
    check(name+"_STATIONARY_DIAGONAL_NEGATIVE_EIGENLINE",
          Astat*sp.ones(3,1)==negative*sp.ones(3,1))
    for vec in (sp.Matrix([1,-1,0]),sp.Matrix([1,1,-2])):
        check(name+"_STATIONARY_SUM_ZERO_POSITIVE_PLANE",
              Astat*vec==positive*vec)
    stationary_spectra[name]={
      "full_characteristic_polynomial":str(full_char),
      "full_eigenvalues":full_roots,
      "stationary_characteristic_polynomial":str(stat_char),
      "stationary_eigenvalues":stationary_roots,
      "soft_kernel_vector":[str(x) for x in soft],
      "stationary_negative_direction":"(1,1,1)",
      "positive_transverse_plane":"t1+t2+t3=0"
    }

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
 "stationary_spectra":stationary_spectra,
 "interpretation":"two decoupled transported 2+1 hyperbolic center envelopes; no elliptic spectral gap",
 "nonclaim":"quadratic principal symbol only; nonlinear envelope existence and energy estimate remain open"
}
parser=argparse.ArgumentParser()
parser.add_argument("--write",action="store_true")
args=parser.parse_args()
if OUT.exists() and not args.write:
    check("RESULTS_MATCH_PINNED_JSON",result==json.loads(OUT.read_text()))
else:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
print("TERMINAL A4D-Y-CENTER-ENVELOPE-PRINCIPAL-SYMBOL-CERTIFIED")
