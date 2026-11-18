#!/usr/bin/env python3
"""Exact null-frame gauge and raw inverse-coframe chart check for B21."""
from pathlib import Path
import json,sympy as s
P=Path(__file__).resolve().parent
H,kx,ky,nu=s.symbols('H kx ky nu',real=True,nonzero=True)
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
R=s.diag(1,1,-1,-1);assert R.det()==1 and R.T*eta*R==eta
E=lambda i,j:s.S.One if i==j else s.S.Zero
e0=s.eye(4);e0[1,0]=H/2
e=R*e0;u0=nu*eta*e0.inv().T;u=R*u0
assert s.simplify(u-nu*eta*e.inv().T)==s.zeros(4)
assert s.simplify(e-nu*eta*u.inv().T)==s.zeros(4)
assert u==s.Matrix([[0,nu,0,0],[nu,-nu*H/2,0,0],[0,0,nu,0],[0,0,0,nu]])
N2=s.zeros(4);N2[1,2]=N2[2,0]=1
N3=s.zeros(4);N3[1,3]=N3[3,0]=1
V=kx*N2+ky*N3
assert V**3==s.zeros(4) and R*N2*R==-N2 and R*N3*R==-N3
U0=s.eye(4)+V+V**2/2;U=R*U0*R
assert U==s.eye(4)-V+V**2/2 and s.simplify(U.T*eta*U-eta)==s.zeros(4)
# Exterior action for diagonal R, in owned CAR ordering (0,2,3,1).
order=(0,2,3,1); signs=[1,1,-1,-1]
L=s.diag(*[s.prod(signs[i] for i in order if mask & (1<<i)) for mask in range(16)])
creators=[]
for i in range(4):
 C=s.zeros(16)
 for mask in range(16):
  if not (mask>>i)&1:C[mask|(1<<i),mask]=(-1)**sum(bool(mask&(1<<j)) for j in order[:order.index(i)])
 creators.append(C);assert L*C*L==signs[i]*C
# Exterior eta built from exact minors; constant gauge preserves it.
def ix(mask):return [i for i in order if mask&(1<<i)]
HE=s.Matrix(16,16,lambda a,b: eta.extract(ix(a),ix(b)).det() if len(ix(a))==len(ix(b)) else 0)
assert L*HE*L==HE and L*L==s.eye(16)
# For nonsingular u: e=nu eta u^-T is a diffeomorphism; its inverse is u=nu eta e^-T.
# Differential delta e= -e (delta u)^T u^-T, hence invertible with inverse differential.
D=s.Matrix(4,4,lambda i,j:s.Symbol(f'd{i}{j}'))
de=-e*D.T*u.inv().T
du=-u*de.T*e.inv().T
assert s.simplify(du-D)==s.zeros(4)
result={'status':'PASS_EXACT_CURRENT_GAUGE_AND_RAW_INVERSE_COFRAME_CHART','R':'diag(1,1,-1,-1)','R_is_proper_eta_null_lorentz':True,
 'coframe':'e=R e0, u=R u0=nu eta e^-T','B21_raw_u_matches_exactly':True,'links':'U=R U0 R^-1=exp(-kx N2-ky N3)',
 'full_CAR_creator_covariance_all_4':True,'exterior_metric_gauge_invariant':True,'all_16_chart_directions_differential_invertible':True,
 'scope':'exact constant gauge and local chart; no native history, density variation, or full GR closure','GR_closed':False}
(P/'CURRENT_FRAME_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
