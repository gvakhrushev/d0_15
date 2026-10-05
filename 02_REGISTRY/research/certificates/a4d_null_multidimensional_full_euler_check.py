#!/usr/bin/env python3
"""Full multidimensional null-subgroup stencil and exact obstruction inputs.

The accompanying proof gives the all-period conclusion. This certificate
reconstructs all 24 Euler face kernels, ten metric slots, the finite Laurent
inverse, quadratic constants and centered CR identities. No general Lorentz
or parent fixed-source terminal is claimed.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path)
parser.add_argument('--output',type=Path)
parser.add_argument('--write',action='store_true')
args=parser.parse_args()
repo=args.repo or next((p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').is_file()),None)
if repo is None:parser.error('Supply --repo with the D0 repository root')
owner_dir=repo.resolve()/'02_REGISTRY/research/certificates'
owners={
 'a4d_identity_quarter_nonlinear_response_check.py':'f930d5d674b62f0c500b1aa1e28c1b3076a900899767d13b2dd2cd6a59142865',
 'a4d_designated_full_gap_check.py':'fb76349e723ff532ef9b2222fd07cef5d7fa3e7e2b5d2c94b01ad4b056b8885d',
}
for name,digest in owners.items():assert hashlib.sha256((owner_dir/name).read_bytes()).hexdigest()==digest,name
sys.path.insert(0,str(owner_dir))
import numpy as np
import sympy as s
import a4d_identity_quarter_nonlinear_response_check as N

def zero(value):assert s.cancel(s.expand(value))==0,value

def coeff_norm(expression,variables):
 return sum(abs(c) for c in s.Poly(s.expand(expression),*variables).coeffs())

I=N.I;eta=np.diag(N.SIG).astype(object)
k=np.array([1,1,0,0],dtype=object);kf=k@eta
ng=[np.outer(k,I[:,j]@eta)-np.outer(I[:,j],kf) for j in (2,3)]
H,p,q,P,Q=s.symbols('H p q P Q',real=True)
E=I+F(1,2)*H*np.outer(k,kf)
qi=eta-H*np.outer(k,k)

def U(a,b):
 v=a*ng[0]+b*ng[1]
 return I+v+F(1,2)*v@v

def adjoint(matrix):return eta@matrix.T@eta

up=U(p,q);uq=U(P,Q)
for generator in N.G:assert not np.any(adjoint(generator)+generator)
for value in ((U(p,q)-U(-p,-q))*F(1,2)-p*ng[0]-q*ng[1]).flat:zero(value)
for value in (up.T@eta@up-eta).flat:zero(value)
for null in ng:
 assert not np.any(null@null@null)
 assert not np.any(adjoint(null)+null)
assert not np.any(ng[0]@ng[1]-ng[1]@ng[0])
for value in (E.T@eta@E-eta-H*np.outer(kf,kf)).flat:zero(value)
zero(s.det(s.Matrix(E.tolist()))-1)

# Every entry is a full Lorentz-generator variation of a literal face.
kernels=[];metric_maps=[];linear_kernels=[];quadratic_kernels=[];constant_kernels=[]
for face,(r,t) in enumerate(N.PAIRS):
 u,wleg=[j for j in range(4) if j not in (r,t)]
 w=N.orient(r,t)*N.weight(N.wedge(E[:,u],E[:,wleg]))
 for value in (adjoint(w)+w).flat:zero(value)
 coeff=uq@w.T@up
 row=[s.expand(np.sum(coeff.T*g)) for g in N.G]
 const=[rg.subs({p:0,q:0,P:0,Q:0}) for rg in row]
 linear=[sum(s.Poly(rg,p,q,P,Q).coeff_monomial(v)*v for v in (p,q,P,Q)) for rg in row]
 quad=[s.expand(rg-cg-lg) for rg,cg,lg in zip(row,const,linear)]
 for rg,qg in zip(row,quad):
  assert s.Poly(rg,p,q,P,Q).total_degree()<=2
  if qg!=0:assert s.Poly(qg,p,q,P,Q).homogeneous_order()==2
 for gi in (0,5):assert quad[gi]==0
 for entry in linear+quad:zero(s.diff(entry,H))
 # Null pairings are constant on each face, so their full shared rows telescope.
 for null in ng:
  coords=[null[a,b] for a,b in N.PAIRS]
  for vv in (p,q,P,Q):zero(s.diff(sum(row[g]*coords[g] for g in range(6)),vv))
 kernels.append(row);constant_kernels.append(const);linear_kernels.append(linear);quadratic_kernels.append(quad)
 maps=[]
 for ar,br in N.SYM:
  dq=np.zeros((4,4),dtype=object);dq[ar,br]=dq[br,ar]=1
  de=E@qi@dq*F(1,2)
  for value in (de.T@eta@E+E.T@eta@de-dq).flat:zero(value)
  dw=N.orient(r,t)*N.weight(N.wedge(de[:,u],E[:,wleg])+N.wedge(E[:,u],de[:,wleg]))
  for value in (adjoint(dw)+dw).flat:zero(value)
  entries=[s.expand(np.sum(dw*null)) for null in ng]
  for entry in entries:zero(s.diff(entry,H))
  maps.append(entries)
 metric_maps.append(maps)

# Literal shift convention: plaquette=(r,x),(t,x+r),(r,x+t)^-1,(t,x)^-1.
phase=s.symbols('l0:4',nonzero=True)
v=s.symbols('v0:8')
S=s.zeros(24,8);X=s.zeros(10,8)
for face,(r,t) in enumerate(N.PAIRS):
 vr=s.Matrix(v[2*r:2*r+2]);vt=s.Matrix(v[2*t:2*t+2])
 def ev(pre,post,g):return s.expand(linear_kernels[face][g].subs({p:pre[0],q:pre[1],P:post[0],Q:post[1]}))
 prer=vr;postr=phase[r]*vt-phase[t]*vr-vt
 prem=(vr+phase[r]*vt)/phase[t];postm=-vr-vt/phase[t]
 pres=vr/phase[r]+vt;posts=-(phase[t]*vr+vt)/phase[r]
 pren=vr+phase[r]*vt-phase[t]*vr;postn=-vt
 for g in range(6):
  rr=ev(prer,postr,g)-ev(prem,postm,g)
  ss=ev(pres,posts,g)-ev(pren,postn,g)
  for i,var in enumerate(v):S[6*r+g,i]+=s.diff(rr,var);S[6*t+g,i]+=s.diff(ss,var)
 curvature=[(phase[r]-1)*v[2*t+j]-(phase[t]-1)*v[2*r+j] for j in range(2)]
 for m in range(10):
  readout=sum(metric_maps[face][m][j]*curvature[j] for j in range(2))
  for i,var in enumerate(v):X[m,i]+=s.diff(readout,var)

selected=[1,2,7,8,13,14,19,20]
M=S[selected,:]
zero(M[:4,:4].det()-1);zero(M[4:,4:].det()-1)
Mi=M.inv().applyfunc(s.cancel)
for value in M*Mi-s.eye(8):zero(value)
for value in Mi*M-s.eye(8):zero(value)
# All inverse entries are Laurent polynomials, not growing mesh inverses.
row_norms=[]
for r in range(8):
 norm=0
 for value in Mi[r,:]:
  terms=s.Add.make_args(s.expand(value))
  for term in terms:
   coefficient,monomial=term.as_coeff_Mul()
   assert coefficient.is_Rational
   powers=monomial.as_powers_dict()
   assert all(base in phase or base==1 for base in powers)
   norm+=abs(coefficient)
 row_norms.append(norm)
assert max(row_norms)==3

# Exact local quadratic coefficient bounds for every face occurrence.
e=s.symbols('e0:8');vectors=[s.Matrix(e[2*j:2*j+2]) for j in range(4)]
incidences=[(vectors[0],vectors[1]-vectors[2]-vectors[3]),
            (vectors[0]+vectors[1],-vectors[2]-vectors[3]),
            (vectors[0]+vectors[1]-vectors[2],-vectors[3])]
qbound=0
for row in quadratic_kernels:
 for gi in (1,2):
  for pre,post in incidences:
   expression=s.expand(row[gi].subs({p:pre[0],q:pre[1],P:post[0],Q:post[1]}))
   qbound=max(qbound,coeff_norm(expression,e))
assert qbound<=8
# Each shared row has <=6 face incidences, giving the conservative bound 48.
assert 6*qbound<=48

# Source forcing and exact leading response for H=H(x2,x3).
Hm=s.symbols('Hm0:4');H0=s.Symbol('H0')
forcing=s.zeros(24,1)
for face,(r,t) in enumerate(N.PAIRS):
 for g,cg in enumerate(constant_kernels[face]):
  forcing[6*r+g]+=cg.subs(H,H0)-cg.subs(H,Hm[t])
  forcing[6*t+g]+=cg.subs(H,Hm[r])-cg.subs(H,H0)
f_pp=forcing.subs({Hm[0]:H0,Hm[1]:H0})[selected,:]
expected=s.Matrix([(Hm[2]-H0)/2,(Hm[3]-H0)/2,(Hm[2]-H0)/2,(Hm[3]-H0)/2,0,0,0,0])
for value in f_pp-expected:zero(value)
lead=s.Matrix([-(1-1/phase[2])/2,-(1-1/phase[3])/2,(1-1/phase[2])/2,(1-1/phase[3])/2,0,0,0,0])
fourier_forcing=expected.subs({H0:1,Hm[2]:1/phase[2],Hm[3]:1/phase[3]})
for value in M.subs({phase[0]:1,phase[1]:1})*lead+fourier_forcing:zero(value)

# Exact full D/R rows after longitudinal averaging; no quadratic or H term.
Drows=[0,5,6,11,12,17,18,23]
D=S[Drows,:].subs({phase[0]:1,phase[1]:1})
for value in D[4,:]-s.Matrix([[phase[2],0,phase[2],0,0,0,0,0]]):zero(value)
for value in D[5,:]-s.Matrix([[0,phase[2],0,phase[2],0,0,0,0]]):zero(value)
C2=phase[2]-1/phase[2];C3=phase[3]-1/phase[3]
sub={v[2]:-v[0],v[3]:-v[1]}
row0=(D[0,:]-D[2,:])*s.Matrix(v)
row1=(D[1,:]-D[3,:])*s.Matrix(v)
zero(row0[0].subs(sub)-C2*v[0]-C3*v[1])
zero(row1[0].subs(sub)+C3*v[0]-C2*v[1])
s2,s3=s.symbols('s2 s3',real=True)
cr=s.Matrix([[2*s.I*s2,2*s.I*s3],[-2*s.I*s3,2*s.I*s2]])
zero(cr.det()+4*(s2*s2+s3*s3))
for value in cr.conjugate().T*cr-4*(s2*s2+s3*s3)*s.eye(2):zero(value)
# Projection identity P*T_j^2=P gives P*D^-H=-P*central_second(H)/2.
c=s.Symbol('c')
assert s.rem(s.expand(c*(1-1/c+(c-2+1/c)/2)),c*c-1,c)==0

report={
 'input_commit':'f4f88161325574e4c5750e0af4a8cc14a2f4b48e','input_owner_sha256':owners,
 'variable_convention':'v=(a0,b0,a1,b1,a2,b2,a3,b3); l_j is forward shift T_j',
 'full_face_kernel_convention':'K_f(pre,post)=trace(U(post)*W_f(H).T*U(pre)*G); signs and positions follow the literal shared-link plaquette',
 'all_six_full_generator_face_kernels':[[str(s.factor(x)) for x in row] for row in kernels],
 'all_ten_Gram_linear_curvature_maps':[[[str(x) for x in pair] for pair in matrix] for matrix in metric_maps],
 'full_24_row_linear_symbol':[[str(s.factor(x)) for x in S[r,:]] for r in range(24)],
 'all_10_metric_symbol_rows':[[str(s.factor(x)) for x in X[r,:]] for r in range(10)],
 'selected_complementary_full_rows':selected,
 'selected_operator':[[str(s.factor(x)) for x in M[r,:]] for r in range(8)],
 'finite_Laurent_inverse':[[str(s.factor(x)) for x in Mi[r,:]] for r in range(8)],
 'inverse_sup_row_coefficient_norms':[str(x) for x in row_norms],
 'quadratic_face_occurrence_coefficient_bound':str(qbound),
 'conservative_full_quadratic_row_bound':48,
 'pp_forcing_selected_rows':[str(x) for x in expected],
 'exact_leading_pp_log_symbol':[str(s.factor(x)) for x in lead],
 'longitudinal_average_D_R_rows':[[str(s.factor(x)) for x in D[r,:]] for r in range(8)],
 'constants':{'chart_coefficient_delta_max':'1/288','automatic_log_sup':'3*h*C1','leading_log_error_sup':'1296*h^2*C1^2','projected_backward_H_difference_sup':'h^2*C2/2','fixed_profile_necessary_bound':'C1 <= h*(2*C2+5184*C1^2)'},
 'period_scope':'Every L>=3; even L has four transverse checkerboard characters, odd L only the constant; no L multiple4 assumption is needed.',
 'verdict':'In coefficient chart delta<=1/288, arbitrary multidimensional null-subgroup full stationary fields on an unbounded refinement sequence require fixed H(y2,y3) constant. Source is unrestricted; no exact fixed nonconstant pp-profile sequence is constructed.',
 'scope_exclusion':'The all-period proof does not cover general Lorentz links, another background section, or a larger unspecified chart.'}
output=args.output or Path(__file__).with_name('a4d_null_multidimensional_full_euler_results.json')
if args.write:output.write_text(json.dumps(report,indent=2)+'\n');print('PASS_WRITTEN_PINNED_RESULTS')
else:assert json.loads(output.read_text())==report,'Pinned artifact drift';print('PASS_PINNED_REPLAY')
print('PASS_FULL_MULTIDIMENSIONAL_NULL_EULER_METRIC_LAURENT_INVERSE_QUADRATIC_AND_CR_IDENTITIES')
