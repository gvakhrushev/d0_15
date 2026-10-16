#!/usr/bin/env python3
"""Literal null-shear full-Euler obstruction and pinned exact replay.

Compute all 24 shared-link connection rows and all 10 Gram metric slots.
The periodic global implication is proved in the accompanying research memo;
this certificate checks its exact local extraction identities. It does not
exclude general Lorentz links or multidimensional null-subgroup fields.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, help="D0 repository root")
parser.add_argument("--output", type=Path, help="Pinned results JSON")
parser.add_argument("--write", action="store_true", help="Write results instead of replaying the pinned artifact")
args = parser.parse_args()
repo = args.repo
if repo is None:
    repo = next((p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file()), None)
if repo is None:
    parser.error("Cannot locate a D0 repository; supply --repo")
repo = repo.resolve()
owner_dir = repo / "02_REGISTRY/research/certificates"
owner_hashes = {
    "a4d_identity_quarter_nonlinear_response_check.py": "f930d5d674b62f0c500b1aa1e28c1b3076a900899767d13b2dd2cd6a59142865",
    "a4d_designated_full_gap_check.py": "fb76349e723ff532ef9b2222fd07cef5d7fa3e7e2b5d2c94b01ad4b056b8885d",
}
for name, expected in owner_hashes.items():
    actual = hashlib.sha256((owner_dir / name).read_bytes()).hexdigest()
    if actual != expected:
        raise AssertionError(f"Input owner drift: {name}: {actual} != {expected}")
sys.path.insert(0, str(owner_dir))
output = args.output or Path(__file__).with_name("a4d_null_shear_full_euler_results.json")

def zero(x):
    assert s.expand(x) == 0, x

import numpy as np
import sympy as s
from fractions import Fraction as F
import a4d_identity_quarter_nonlinear_response_check as N
I=N.I;ETA=np.diag(N.SIG).astype(object)
k=np.array([1,1,0,0],dtype=object);kf=k@ETA
n=[]
for j in (2,3):
 e=I[:,j]
 n.append(np.outer(k,e@ETA)-np.outer(e,kf))
for m in n:
 assert not np.any(m@m@m)
 assert not np.any(m.T@ETA+ETA@m)
assert not np.any(n[0]@n[1]-n[1]@n[0])
H=s.symbols('Hm H0 Hp')
z=[[s.symbols(f'{nm}m {nm}0 {nm}p') for nm in ('a','b','c','d')], [s.symbols(f'{nm}m {nm}0 {nm}p') for nm in ('e','f','g','j')]]
def solder(p):return I+F(1,2)*H[p+1]*np.outer(k,kf)
def ex(v):return I+v+F(1,2)*v@v
def links(p,r):
 v=z[0][r][p+1]*n[0]+z[1][r][p+1]*n[1]
 return ex(v)
def inv(u):return ETA@u.T@ETA
weights={};dweights={}
for p in (-1,0):
 E=solder(p);Q=E.T@ETA@E;Qi=I@ETA-H[p+1]*np.outer(k,k)
 lifts=[]
 for r,t in N.SYM:
  dq=np.zeros((4,4),dtype=object);dq[r,t]=dq[t,r]=1
  de=E@Qi@dq*F(1,2)
  for value in (de.T@ETA@E+E.T@ETA@de-dq).flat:zero(value)
  lifts.append(de)
 for f,(r,t) in enumerate(N.PAIRS):
  u,v=[j for j in range(4) if j not in (r,t)]
  weights[p,f]=N.orient(r,t)*N.weight(N.wedge(E[:,u],E[:,v]))
  dweights[p,f]=[N.orient(r,t)*N.weight(N.wedge(de[:,u],E[:,v])+N.wedge(E[:,u],de[:,v])) for de in lifts]
# Verify physical Lorentz links and the universal curvature pairing identity.
for pos in (-1, 0, 1):
 for role in range(4):
  link=links(pos,role)
  for value in (link.T@ETA@link-ETA).flat:zero(value)
for generator in N.G:
 assert not np.any(inv(generator)+generator)
generic=np.array(s.symbols("z0:16"),dtype=object).reshape(4,4)
generic_projected=(generic-inv(generic))*F(1,2)
all_weights=list(weights.values())+[dw for collection in dweights.values() for dw in collection]
for w in all_weights:
 for value in (inv(w)+w).flat:zero(value)
 # This holds for arbitrary deltaP, hence every full Lorentz tangent.
 zero(np.sum(w*(generic-generic_projected)))
 # Same equation expresses the effective weight in a direct P variation.
 for value in ((w-inv(w))*F(1,2)-w).flat:zero(value)
ek=np.zeros((4,6),dtype=object);ek_curv=np.zeros_like(ek)
xi=np.zeros(10,dtype=object);xi_curv=np.zeros_like(xi)
cell=0;cell_curv=0;variation_count=0
for p in (-1,0):
 for f,(r,t) in enumerate(N.PAIRS):
  loc=[(p,r,False),(p+int(r==2),t,False),(p+int(t==2),r,True),(p,t,True)]
  fac=[inv(links(q,j)) if iv else links(q,j) for q,j,iv in loc]
  prefix=[I]
  for u in fac:prefix.append(prefix[-1]@u)
  suffix=[None]*5;suffix[4]=I
  for j in range(3,-1,-1):suffix[j]=fac[j]@suffix[j+1]
  prod=prefix[4]
  curvature=(prod-inv(prod))*F(1,2)
  if p==0:
   cell+=np.sum(weights[p,f]*prod)
   cell_curv+=np.sum(weights[p,f]*curvature)
   for m in range(10):
    xi[m]+=np.sum(dweights[p,f][m]*prod)
    xi_curv[m]+=np.sum(dweights[p,f][m]*curvature)
  for j,(q,role,iv) in enumerate(loc):
   if q!=0:continue
   co=suffix[j+1]@weights[p,f].T@prefix[j]
   jet=-fac[j]@co if iv else co@fac[j]
   # dC(P)[deltaP]=(deltaP-eta*deltaP.T*eta)/2 on a Lorentz curve.
   # Pairing with W projects W to (W-eta*W.T*eta)/2, identically W.
   # Independently accumulate every shared-link variation using that weight.
   wc=np.array([s.expand(v) for v in ((weights[p,f]-inv(weights[p,f]))*F(1,2)).flat],dtype=object).reshape(4,4)
   cc=suffix[j+1]@wc.T@prefix[j]
   jc=-fac[j]@cc if iv else cc@fac[j]
   for g in range(6):
    raw=np.sum(jet.T*N.G[g]);curv=np.sum(jc.T*N.G[g])
    zero(raw-curv)
    ek[role,g]+=raw;ek_curv[role,g]+=curv
    variation_count+=1

assert variation_count == 144, variation_count
zero(cell-cell_curv)
for actual,curv in zip(xi,xi_curv):zero(actual-curv)
for actual,curv in zip(ek.flat,ek_curv.flat):zero(actual-curv)
print("PASS_CURVATURE_PAIRING_ACTION_10_GRAM_SLOTS_24_FULL_EULER_ROWS",flush=True)
E=solder(0);Q=E.T@ETA@E
zero(s.det(s.Matrix(E.tolist()))-1)
for vv in (E.T@ETA@E-ETA-H[1]*np.outer(kf,kf)).flat:zero(vv)
A,B,C,D=z[0];EE,FF,GG,J=z[1]
expected=[-(B[1]-B[2])/2,(A[1]-A[2]-B[1]+B[2])/2,(J[1]-J[2])/2,-(D[1]-D[2])/2,(A[1]-A[2])/2,(J[1]-J[2])/2,-(D[1]-D[2])/2,0,-(EE[1]-EE[2]+FF[1]-FF[2])/2,(A[1]-A[2]+B[1]-B[2])/2]
for actual,want in zip(xi,expected):zero(actual-want)
zero(cell+(A[1]-A[2]+B[1]-B[2]))
# Extract every exact stationary restriction used in the global proof.
zero(ek[2,0]-(A[2]+B[2]))
zero(ek[3,5]+A[1]+B[1])
zero(ek[2,5]-(EE[2]+FF[2]))
zero(ek[3,0]-(EE[1]+FF[1]))
sub={B[i]:-A[i] for i in range(3)}|{FF[i]:-EE[i] for i in range(3)}
row=lambda r,g:s.expand(s.sympify(ek[r,g]).subs(sub))
zero(row(0,0)+row(1,0)+2*(C[0]+J[1]))
zero(row(0,0)-row(1,0)+A[0]-A[2])
zero(row(0,5)+row(1,5)-2*(D[1]-GG[0]))
zero(row(0,5)-row(1,5)+EE[0]-EE[2])
zero(row(2,1)+(A[1]*A[2]-EE[1]*EE[2]+J[2]))
zero(row(2,2)+(A[1]*EE[2]+A[2]*EE[1]-D[2]))
zero(row(3,1)-(-2*A[1]*EE[1]+GG[0]+(J[0]-J[2])/2))
zero(row(3,2)-(A[1]**2-EE[1]**2-C[0]+(D[2]-D[0])/2))
# Once period-two products and the rows above make all coefficients constant:
a,e=s.symbols('a e',real=True)
const=[a,-a,a*a-e*e,2*a*e,e,-e,2*a*e,e*e-a*a]
const_sub={z[t][r][i]:const[4*t+r] for t in range(2) for r in range(4) for i in range(3)}
red=[[s.factor(s.sympify(v).subs(const_sub)) for v in row] for row in ek]
P=a**4-4*a**3*e-6*a*a*e*e+4*a*e**3+e**4
QQ=a**4+4*a**3*e-6*a*a*e*e-4*a*e**3+e**4
zero(red[0][1]-(P-2*a-H[1]+H[0])/2)
zero(red[0][2]-(QQ-2*e)/2)
zero(P*P+QQ*QQ-2*(a*a+e*e)**4)
# Literal full residuals are NOT killed by reduced null variations.
subexample={v:0 for row in z for ls in row for v in ls}
subexample|={A[0]:s.Rational(1,10),A[1]:s.Rational(1,10),A[2]:s.Rational(1,10),B[0]:-s.Rational(1,10),B[1]:-s.Rational(1,10),B[2]:-s.Rational(1,10),H[0]:0,H[1]:0,H[2]:0}
zero(s.sympify(ek[3,2]).subs(subexample)-s.Rational(1,100))
# For each link role the Euler pairing with both null generators vanishes identically.
for r in range(4):
 for null in n:
  coeff=[null[a,b] for a,b in N.PAIRS]
  zero(sum(ek[r,g]*coeff[g] for g in range(6)))
report={
 'input_commit':'f4f88161325574e4c5750e0af4a8cc14a2f4b48e',
 'input_owner_sha256':owner_hashes,
 'curvature_pairing_audit':{
  'weight_and_Gram_derivative_weights':'eta*W.T*eta=-W',
  'generic_projection_identity':'<W,Z>=<W,(Z-eta*Z.T*eta)/2> for every symbolic 4x4 Z',
  'physical_Lorentz_inverse':'P^-1=eta*P.T*eta',
  'action_and_metric':'direct C(P) and P evaluations agree exactly for action and all ten Gram slots',
  'connection':'all 24 rows agree with the full C(P) Lorentz derivative; every local shared-link generator variation is checked',
  'local_full_generator_variations_checked':variation_count,
 },
 'full_connection_rows':[[str(s.factor(v)) for v in row] for row in ek],
 'full_gram_slots':[str(s.factor(v)) for v in xi],
 'cell_action':str(s.factor(cell)),
 'null_generators':[[[int(v) for v in row] for row in mat] for mat in n],
 'variables':[[[str(v) for v in ls] for ls in row] for row in z],
 'constant_reduction_rows':[[str(v) for v in row] for row in red],
 'verdict':'For any L>=3 and periodic H_j and real coefficients depending only on x2, full stationarity implies H_j constant and Xi=0. No smallness assumption is needed.',
 'chart_extra':'If H is constant, nonzero null stationary constant coefficients obey (a+i*e)^3=1-i and sqrt(a^2+e^2)=2^(1/6)>1; consequently they lie outside any log chart with sufficiently small coefficient bound.',
 'scope_exclusion':'No conclusion about null-subgroup fields depending on transverse x0,x1,x3 or general Lorentz links.'}
if args.write:
 output.write_text(json.dumps(report,indent=2)+"\n")
 print("PASS_WRITTEN_PINNED_RESULTS",flush=True)
else:
 pinned=json.loads(output.read_text())
 assert report==pinned,"Pinned artifact mismatch; audit the change before using --write"
 print("PASS_PINNED_REPLAY",flush=True)
print("PASS_FULL_NULL_SHEAR_24_EULER_10_GRAM_AND_GLOBAL_PROOF_EXTRACTIONS",flush=True)
