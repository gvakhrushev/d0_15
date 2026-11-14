#!/usr/bin/env python3
"""Independent exterior-minor and exact 32-column Julia factorization audit."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json
import sympy as s
import numpy as np
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round19');P=Path(__file__).resolve().parent
paths=[D/'coframe_factorization.py',D/'check_coframe_factorization.py'];dg={str(p):sha256(p.read_bytes()).hexdigest() for p in paths}
spec=importlib.util.spec_from_file_location('b40_original_coframe',paths[0]);f=importlib.util.module_from_spec(spec);sys.modules[spec.name]=f;spec.loader.exec_module(f)
ORDER=(0,2,3,1);assert f.ORDER==ORDER
basis=[[j for j in ORDER if mask&(1<<j)] for mask in range(16)]
def exterior(V):
 z=s.zeros(16)
 for x in range(16):
  for y in range(16):
   if len(basis[x])==len(basis[y]):z[x,y]=V.extract(basis[x],basis[y]).det() if basis[x] else 1
 return z
def creator(j):
 z=s.zeros(16)
 for mask in range(16):
  if not mask&(1<<j):z[mask|(1<<j),mask]=(-1)**sum(bool(mask&(1<<x)) for x in ORDER[:ORDER.index(j)])
 return z
creators=[creator(j) for j in range(4)];eye=s.eye(16)
for j in range(4):
 for k in range(4):assert creators[j]*creators[k].T+creators[k].T*creators[j]==(eye if j==k else s.zeros(16))
c,z=s.symbols('c z',real=True)
def mod(expr):return s.rem(s.Poly(s.expand(expr),z),s.Poly(z*z+c*c-1,z)).as_expr().expand()
def matzero(M):return all(mod(x)==0 for x in M)
# Exact exterior minors independently determine all four signs, including the
# full occupation sector. Compare against the actual source pair generator.
for j in (1,2,3):
 V=s.eye(4);V[0,0]=V[j,j]=c;V[j,0]=z;V[0,j]=-z
 E=exterior(V);F=s.eye(16);pairs=list(f.fock_pairs(j));assert len(pairs)==4
 for a,b,sign in pairs:F[a,a]=F[b,b]=c;F[b,a]=sign*z;F[a,b]=-sign*z
 assert matzero(E-F) and matzero(F.T*F-eye)
 for q in range(4):
  expected=sum((V[k,q]*creators[k] for k in range(4)),s.zeros(16));assert matzero(F*creators[q]*F.T-expected)
# Exact 32-column Julia with three nontrivial rational planes and nonzero
# positive/negative components. No numerical eigensolver or native proxy.
checks=0
for vsgn in (1,-1):
 u=s.Matrix([s.Rational(3,100),s.Rational(4*vsgn,100),s.Rational(12,100),s.Rational(84*vsgn,100)]);n=s.Rational(17,20);d=s.sqrt(111)/20
 rotations=[(3,s.Rational(13,85),s.Rational(84*vsgn,85)),(2,s.Rational(5,13),s.Rational(12,13)),(1,s.Rational(3,5),s.Rational(4*vsgn,5))]
 V=s.eye(4);F=s.eye(16)
 for j,co,si in rotations:
  R=s.eye(4);R[0,0]=R[j,j]=co;R[j,0]=si;R[0,j]=-si;V=R*V;F=exterior(R)*F
 assert V[:,0]==u/n and F==exterior(V) and F.T*F==eye
 C=sum((u[j]*creators[j] for j in range(4)),s.zeros(16));CC=C*C.T;CtC=C.T*C
 left=eye-CC/(1+d);right=eye-CtC/(1+d)
 assert all(s.simplify(x)==0 for x in left*left-eye+CC) and all(s.simplify(x)==0 for x in right*right-eye+CtC)
 J=C.row_join(left).col_join(right.row_join(-C.T));X=s.zeros(32);R=s.eye(32)
 for x in range(32):X[x^16,x]=1
 for rest in range(0,16,2):
  a,b=rest|1,rest|16;R[a,a]=R[b,b]=d;R[b,a]=-n;R[a,b]=n
 W=s.diag(F,F);assert all(s.simplify(x)==0 for x in W*R*X*W.T-J);checks+=1024
 # Also test the actual floating routine's dominant-first order, not the
 # independently chosen rational order, against the exact 32-column target.
 got,actualV,actualF,rots=f.compiled_target([float(q) for q in u]);target=np.array(J.evalf(),dtype=float)
 assert len(rots)==3 and np.max(abs(got-target))<1e-14 and np.max(abs(actualV[:,0]-np.array(u/n,dtype=float).ravel()))<1e-14
 assert np.linalg.norm(np.array([float(q) for q in u]))<1
for p,h in dg.items():assert sha256(Path(p).read_bytes()).hexdigest()==h
out={'status':'PASS_INDEPENDENT_COFRAME_SIGN_ORDER_AND_JULIA','input_sha256':dg,'exact_all_pair_signs_against_exterior_minors':True,'exact_CAR_covariance_modes':12,'exact_32_by_32_column_entries':checks,'two_mixed_sign_nonzero_three_plane_vectors':True,'actual_dominant_first_order_float_cross_check':True,'maximum_ideal_macros':'2*(3*4)+1+1=26','native_angle_certificate_constructed':False,'full_Omega_SELECT_present':False,'physical_C_closed':False,'GR_closed':False}
(P/'INDEPENDENT_COFRAME_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
