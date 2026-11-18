#!/usr/bin/env python3
"""Exact macro identities plus exhaustive local-sector float diagnostics."""
from pathlib import Path
from hashlib import sha256
from itertools import product
from collections import Counter
import importlib.util,sys,json,math
from fractions import Fraction as F
import numpy as np
from scipy.linalg import expm
import sympy as s
import proper_link_factorization as f
t=f.t;P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round19');B=P.parent
spec=importlib.util.spec_from_file_location('b41_locality',D/'julia_locality.py');loc=importlib.util.module_from_spec(spec);sys.modules[spec.name]=loc;spec.loader.exec_module(loc)
cat=json.loads((D/'JULIA_LOCAL_SECTORS.json').read_text());assert cat['banks']==loc.catalogue()
for p,h in cat['input_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h
assert sha256((D/'julia_locality.py').read_bytes()).hexdigest()==cat['source_sha256']
# Exact original ETA, nilpotent and Lie algebra checks; original source bounds.
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
# Verify the stated source bounds and original null/cartesian transform.
assert F(t.META['k0_original'])<24 and t.H==.25 and t.SAMP==2**-30
assert all(0<=x[2]<=3 and 0<=x[3]<=3 for x in t.SITES)
T=s.Matrix([[1,1,0,0],[1,-1,0,0],[0,0,s.sqrt(2),0],[0,0,0,-s.sqrt(2)]])/s.sqrt(2);cart=s.diag(1,-1,-1,-1)
assert T.T*T==s.eye(4) and T.det()==1 and T*cart*T.T==eta
# Coordinate-aligned boost is exactly diagonalized by an SO4 rotation.
g,h=s.symbols('gamma h',real=True);B4=s.eye(4);B4[0,0]=B4[1,1]=g;B4[0,1]=B4[1,0]=h
H4=s.eye(4);H4[:2,:2]=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);H4[3,3]=-1
assert H4.T*H4==s.eye(4) and H4.det()==1 and all(s.simplify(x)==0 for x in H4.T*B4*H4-s.diag(g+h,g-h,1,1))
N2=s.zeros(4);N2[1,2]=N2[2,0]=1;N3=s.zeros(4);N3[1,3]=N3[3,0]=1
for N in (N2,N3):assert N.T*eta+eta*N==s.zeros(4) and N**3==s.zeros(4)
assert all((a*N2+b*N3)**3==s.zeros(4) for a,b in ((1,0),(0,1),(1,1),(2,-3)))
a,b=s.symbols('a b');N=a*N2+b*N3;assert N**3==s.zeros(4)
for i in range(4):
 for j in range(i+1,4):
  anti=s.zeros(4);anti[i,j]=1;anti[j,i]=-1;G=eta*anti;assert G.T*eta+eta*G==s.zeros(4) and G.T*G==s.diag(*[int(k in (i,j)) for k in range(4)])
# Rigorous coarse rational bound: K0<24, pi<22/7 => A<0.096,
# 0<=x,y<=3/4, h=1/4, |kx|,|ky|<63/3200 each.
# A = k0 (2pi)^2 /10000; use pi<22/7 and k0<24.
Ab=F(24)*4*F(22,7)**2/F(10000); assert Ab<F(12,125)
kbound=(F(12,125)+F(3,100))*F(5,16)/2;assert kbound<F(1,50)
assert 2*kbound+F(6,2**30)<F(1,20)
# exp(z)<=1/(1-z), z<=1/20; reference boost norm is 9/7.
assert F(20,19)<F(9,7)<2 and 1-F(9,14)**2==F(115,196)
# Independent exact exterior minors, for every SO4 coordinate-plane rotation.
order=t.ORDER;c,z=s.symbols('c z',real=True);basis=[[j for j in order if x>>j&1] for x in range(16)]
def reduce(x):return s.rem(s.Poly(s.expand(x),z),s.Poly(z*z+c*c-1,z)).as_expr().expand()
for i in range(4):
 for j in range(i+1,4):
  V=s.eye(4);V[i,i]=V[j,j]=c;V[j,i]=z;V[i,j]=-z;E=s.zeros(16);M=s.eye(16)
  for x in range(16):
   for y in range(16):
    if len(basis[x])==len(basis[y]):E[x,y]=V.extract(basis[x],basis[y]).det() if basis[x] else 1
  pairs=list(f.fock_pairs(i,j));assert len(pairs)==4
  for x,y,sign in pairs:M[x,x]=M[y,y]=c;M[y,x]=sign*z;M[x,y]=-sign*z
  assert all(reduce(q)==0 for q in E-M)
# Exact base 32x32: chronology X_t then four rotations conditioned on the
# two singular eigenmode bits; c_g^2+d_g^2=1 with independent d_g.
d=s.symbols('d0:4',real=True);e=s.symbols('e0:4',real=True);X=s.zeros(32);R=s.eye(32);Ddiag=s.zeros(16);Sdiag=s.zeros(16)
for x in range(32):X[x^16,x]=1
for mask in range(16):
 g=(mask&1)+2*((mask>>1)&1);Ddiag[mask,mask]=d[g];Sdiag[mask,mask]=e[g];R[mask,mask]=R[mask+16,mask+16]=e[g];R[mask+16,mask]=-d[g];R[mask,mask+16]=d[g]
J=Ddiag.row_join(Sdiag).col_join(Sdiag.row_join(-Ddiag));assert R*X==J
# Enumerate every local sector, caching repeated exact same float targets.
base=t.fields('f',None)[1]; static={bank:t.fields(bank,None)[1] for bank in t.BANKS if bank!='f'}
coords=loc.COORD; cache={};counts=Counter();zero_count=0;max_lor=0.;max_decomp=0.;max_julia=0.;max_norm=0.;max_orth=0.
patterns=list(product((0,1),repeat=6)); theta={}
for pat in patterns:
 W=np.zeros((4,4))
 for v,key in zip(pat,((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))):W+=t.SAMP*(v-t.PVAL**2)*t.GENERATORS[key]
 theta[pat]=expm(W)
for bank in t.BANKS:
 for row in cat['banks'][bank]:
  if row['kind']!='proper_link':continue
  ix=t.INDEX[tuple(row['site'])];role=row['direction'];ids=row['SAM_indices'];L0=base[ix,role] if bank=='f' else static[bank][ix,role]
  ps=product((0,1),repeat=len(ids)) if ids else [()]
  for pat in ps:
   if ids:
    assert len(ids)==6;local=tuple((tuple(coords[x]['generator']),v) for x,v in zip(ids,pat));pv=dict(local);ordered=tuple(pv[k] for k in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3)));U=theta[ordered]@L0
   else:U=L0
   counts[bank]+=1;key=U.tobytes()
   if key in cache:continue
   assert len(cache)<10000
   J,(L,diag,R,mx,iszero)=f.factorized_julia(U);expected=t.link_julia_cached(np.ascontiguousarray(U).tobytes());assert all(np.isfinite(q).all() for q in (U,J,L,diag,R,expected))
   for Q in (L,R):
    factors,rem=f.so4_givens(Q); assert len(factors)==6 and np.max(abs(rem-np.eye(4)))<2e-12 and np.max(abs(f.compose_givens(factors)-Q))<2e-12
   err=float(np.max(abs(J-expected))); decomp=float(np.max(abs(L@np.diag(diag)@R.T-U))); lor=float(np.max(abs(U.T@t.ETA@U-t.ETA)));orth=max(float(np.max(abs(L.T@L-np.eye(4)))),float(np.max(abs(R.T@R-np.eye(4)))))
   assert err<2e-12 and decomp<2e-12 and lor<2e-12 and orth<2e-12 and mx<9/7+2e-12 and np.linalg.det(L)>0 and np.linalg.det(R)>0
   max_julia=max(max_julia,err);max_decomp=max(max_decomp,decomp);max_lor=max(max_lor,lor);max_norm=max(max_norm,mx);max_orth=max(max_orth,orth);zero_count+=iszero;cache[key]=True
for Q in (np.eye(4),-np.eye(4),np.diag([-1.,-1.,1.,1.])):
 factors,rem=f.so4_givens(Q);assert len(factors)==6 and np.max(abs(rem-np.eye(4)))<1e-15 and np.max(abs(f.compose_givens(factors)-Q))<1e-15
assert sum(counts.values())==23296
assert all(counts[k]==cat['counts'][k]['by_kind']['proper_link'] for k in t.BANKS)
# Original independently defined field generator agrees in representative
# full-SAM inputs; contrast with locally assembled six-bit generator.
for bits in ((0,)*6,(1,)*6,(0,1,0,1,0,1),(1,0,0,1,1,0)):
 label=np.zeros(2688,dtype=np.int8)
 for q in coords:
  if q['kind']=='proper_link':label[q['sam_index']]=bits[((0,1),(0,2),(0,3),(1,2),(1,3),(2,3)).index(tuple(q['generator']))]
 actual=t.current(label)[1]
 for row in cat['banks']['f']:
  if row['kind']!='proper_link' or not row['SAM_indices']:continue
  ix=t.INDEX[tuple(row['site'])];role=row['direction'];assert np.max(abs(actual[ix,role]-theta[bits]@base[ix,role]))<1e-15
out={'status':'PASS_STRUCTURAL_JULIA_PROPER_LINK_WITH_BOUNDED_FLOAT_DIAGNOSTICS','by_bank_sectors':dict(counts),'all_proper_link_sectors':sum(counts.values()),'unique_float_target_matrices':len(cache),'diagnostic_zero_boost_unique':int(zero_count),'max_float_J32_difference':max_julia,'max_float_LDR_difference':max_decomp,'max_float_lorentz_error':max_lor,'max_float_orthogonality_error':max_orth,'max_float_singular_norm':max_norm,'exact_lie_nilpotent_generator_checks':True,'exact_all_six_exterior_plane_signs':True,'exact_diagonal_J32_identity':True,'analytic_uniform_norm_upper':'9/7','analytic_defect_gap_lower':'115/196','six_givens_reconstruction_all_unique_targets_and_identity_negative_pivots':True,'factorization_macro_bound':101,'native_angle_certificate_constructed':False,'native_word_constructed':False,'full_Julia_SELECT_present':False,'GR_closed':False,'source_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in [Path(f.__file__),Path(__file__),Path(t.__file__),D/'julia_locality.py',D/'JULIA_LOCAL_SECTORS.json']}}
(P/'PROPER_LINK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
