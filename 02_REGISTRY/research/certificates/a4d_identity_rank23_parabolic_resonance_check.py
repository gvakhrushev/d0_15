#!/usr/bin/env python3
"""Quarantined exact algebra of the wrong-placement stack (A;C).

This is a negative control, not the literal Euler symbol (A^T;C).
Its algebraic ranks/derivatives are retained to reproduce the placement
error. Physical conclusions are superseded by the resonance-circle audit.
"""
from __future__ import annotations
import json, runpy, sys
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE=HERE/"a4d_identity_quarter_firstslow_injectivity_check.py"
OUT=HERE/"a4d_identity_rank23_parabolic_resonance_results.json"

_argv=sys.argv[:]
sys.argv=[str(BASE)]
O=runpy.run_path(str(BASE))
sys.argv=_argv
J=O["joint"]; I=sp.I

def ck(name,cond):
    if not cond: raise AssertionError(name)
    print("PASS_"+name,flush=True)

q=[1,1,I,I]
J0=J(q)
ck("REPRESENTATIVE_RANK23",J0.rank()==23)
ker=J0.nullspace()
ck("ONE_COMPLEX_CENTER",len(ker)==1)
n=ker[0]
n=n/next(v for v in n if v)
expected=sp.zeros(24,1)
for ix,val in {0:1,6:1,12:-1,14:1,16:-1,18:-1,19:1,21:-1}.items():
    expected[ix]=val
ck("EXACT_KERNEL_VECTOR",n==expected)

comp=list(range(1,24))
Rmat=J0[:,comp]
_,piv=Rmat.T.rref(); piv=list(piv)
rest=[r for r in range(34) if r not in piv]
R0=Rmat.extract(piv,range(23))
ck("RANGE_ROWS_EXPECTED",
   piv==[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,26])
ck("RANGE_DETERMINANT_NONZERO",
   sp.factor(R0.det())==-16*I*(-1-I))
Ri=R0.inv()

def embed(w):
    W=sp.zeros(24,1)
    for ii,c in enumerate(comp):
        W[c,0]=w[ii,0]
    return W

z=sp.symbols("z0:4",nonzero=True)
Jz=J(z)
subs={z[j]:q[j] for j in range(4)}
gam=[]
for a in range(4):
    D=(I*z[a]*Jz.diff(z[a])).subs(subs)
    src=D*n
    w=-Ri*src.extract(piv,[0])
    gam.append((src+J0*embed(w)).extract(rest,[0]).applyfunc(sp.simplify))

Real=sp.zeros(2*len(rest),4)
for j,g in enumerate(gam):
    for r,v in enumerate(g):
        Real[2*r,j]=sp.re(v)
        Real[2*r+1,j]=sp.im(v)
ck("FIRST_SLOW_REAL_RANK3",Real.rank()==3)
null=Real.nullspace()
ck("UNIQUE_CHARACTERISTIC_DIRECTION",
   len(null)==1 and null[0]==sp.Matrix([0,0,-1,1]))

r30=rest.index(30)
ck("ROW30_FIRST_DERIVATIVE",
   [sp.simplify(g[r30]) for g in gam]
   ==[-sp.Rational(1,2)-I/2,-sp.Rational(1,2)-I/2,0,0])

# Characteristic path of the wrong-placement control:
# z2=i exp(i s), z3=i exp(-i s).
# Put x=exp(i s), so z2=i x, z3=i/x. Since the first derivative
# vanishes, the angular second derivative is minus the x-second derivative.
x=sp.symbols("x",nonzero=True)
Jx=J([1,1,I*x,I/x])
Jp=Jx.diff(x).subs(x,1)
Jpp=Jx.diff(x,2).subs(x,1)
w1=-Ri*(Jp*n).extract(piv,[0])
W1=embed(w1)
F1=(Jp*n+J0*W1).extract(rest,[0]).applyfunc(sp.simplify)
ck("CHARACTERISTIC_FIRST_DERIVATIVE_ZERO",
   F1==sp.zeros(len(rest),1))

raw2=Jpp*n+2*Jp*W1
w2=-Ri*raw2.extract(piv,[0])
W2=embed(w2)
F2x=(raw2+J0*W2).extract(rest,[0]).applyfunc(sp.simplify)
ck("ROW30_X_SECOND_DERIVATIVE",F2x[r30]==-4+4*I)
F2s=-F2x
ell=sp.im(F2s[r30])-sp.re(F2s[r30])
ck("TRANSVERSE_SECOND_COKERNEL_PAIRING",ell==-8)

# Spatial S3 gives the three choices of the two i-valued spatial
# characters; conjugation gives the three -i copies. Check all six
# literal points as well.
pts=[]
for pair in ((1,2),(1,3),(2,3)):
    for eps in (I,-I):
        p=[1,1,1,1]
        for j in pair:
            p[j]=eps
        pts.append(p)
ck("SIX_LITERAL_RANK23_POINTS",all(J(p).rank()==23 for p in pts))

result={
 "schema":"a4d-identity-rank23-parabolic-placement-control-v2",
 "terminal":"A4D-IDENTITY-WRONG-PLACEMENT-PARABOLIC-CONTROL",
 "representative":["1","1","i","i"],
 "joint_rank":23,
 "center_complex_dimension":1,
 "range_rows":piv,
 "range_determinant":str(sp.factor(R0.det())),
 "first_slow_real_rank":3,
 "first_slow_real_kernel":[0,0,-1,1],
 "row30_first_derivative":["-1/2-I/2","-1/2-I/2","0","0"],
 "characteristic_x_second_row30":str(F2x[r30]),
 "characteristic_angular_second_cokernel_pairing":str(ell),
 "literal_rank23_points":[[str(x) for x in p] for p in pts],
 "local_consequence":"after range elimination the center residual is linear in three transverse real detunings and quadratic in the unique characteristic detuning; local inverse loss is at worst distance^-2",
 "operator":"NONPHYSICAL CONTROL J_wrong=(A;C); literal Euler is (A^T;C)",
 "physical_interpretation_superseded_by":"A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md",
 "scope_fence":[
   "wrong-placement algebra only; no physical injectivity, isolation, or inverse-loss claim",
   "local identity-sheet resonance only",
   "does not classify the full physical torus singular set",
   "does not prove the varying-background nonlinear stationary correspondence",
   "does not by itself prove a global h^-2 inverse bound"
 ]
}
if "--write" in sys.argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",
       json.loads(OUT.read_text())==result)
print("TERMINAL",result["terminal"])
