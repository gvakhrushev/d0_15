#!/usr/bin/env python3
"""Scoped first coframe-gradient pullback control on the existing two-shear path.

At S=I, prescribe dS_10=dS_21=1 in one physical direction mu.
Use a local affine solder jet S(x)=I+eps*x_mu*dS and solve the literal
zero-frequency background Euler equation H(1)k=-f_solder. For each quarter
center, use exp(eps*k_r)exp(delta*i^sum(x)*T_r(S(x))) and retain eps*delta.
Assemble all based and incoming face incidences, not a separate dN estimate.
Project with the owned lower14 normal rows and common full8 annihilator.

The exact controls include phase-weight derivatives, center derivatives,
background link transport, all24 connection and10 metric rows, frozen
kernel identities, and direct contraction with the new saturated witness.
A local affine jet is not a globally periodic background or exact root.
"""
import sys,time,json
from fractions import Fraction as F
from pathlib import Path
MODULE_DIR=Path(__file__).resolve().parent
sys.path.insert(0,str(MODULE_DIR))
import argparse,hashlib
SOURCE_GIT_BLOBS={'a4d_generic_coframe_circle_lift_check.py': '39ac587e6e9c9fdba9505fb474659a4a362d8af7', 'a4d_identity_quarter_nonlinear_response_check.py': '55d2268c12049e613a4cb07be7744c980a6eac97', 'a4d_y_curved_joint_rational_stencil.py': 'e96283c5761f395096080843de30d00ae5826f71', 'a4d_designated_full_gap_check.py': 'a843847c4c169da6dba98e9608fc265fac534d56', 'a4d_spatial_transport_entropy_results.json': '0c71395b5299453fd53297c14f1995ee4afb272d', 'a4d_identity_quarter_nonlinear_response_results.json': '481db19fe7f42daf470ed8caea3af358ea8ff91f', 'a4d_full_quartic_source_quotient_results.json': '238f0e94aefb5dceb012f355199560e56e591977', 'a4d_quartic_joint_transport_syzygy_results.json': 'a3e57e3d9dae84e1a94d43774520d5b50fd5fd27'}
for name,pin in SOURCE_GIT_BLOBS.items():
 data=(MODULE_DIR/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==pin,('source pin changed',name)
RUN_START=time.monotonic()
JETS=[]
import numpy as np, sympy as sp
import a4d_generic_coframe_circle_lift_check as C
import a4d_identity_quarter_nonlinear_response_check as N
from a4d_designated_full_gap_check import QI
I=np.eye(4,dtype=object); Z=np.zeros((4,4),dtype=object); GEN=np.array(C.S.GEN,dtype=object)
S0=np.eye(4,dtype=object);S0[1,0]=S0[2,1]=F(0)
SD=Z.copy();SD[1,0]=SD[2,1]=1
free=[5,11,16,21];cols=[j for j in range(24) if j not in free]
def mul(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),QI()) for j in range(len(B[0]))] for i in range(len(A))]
h,c=C.symbol(S0.tolist(),[QI(0,1)]*4,True);J=h+c
m=[[J[i][j] for j in cols+free]+[QI.of(i==j) for j in range(34)] for i in range(34)]
for k in range(20):
 p=next(i for i in range(k,34) if m[i][k]);m[k],m[p]=m[p],m[k];v=m[k][k];m[k]=[a/v for a in m[k]]
 for i in range(34):
  if i!=k and m[i][k]:
   v=m[i][k];m[i]=[a-v*b for a,b in zip(m[i],m[k])]
B=[row[24:] for row in m[20:]]
TC=[];TD=[]
for r in range(4):
 u,v,w=[j for j in range(4) if j!=r]
 a=S0[:,v]-S0[:,u];b=S0[:,w]-S0[:,u];da=SD[:,v]-SD[:,u];db=SD[:,w]-SD[:,u]
 coeff=N.wedge(a,b);dcoeff=N.wedge(da,b)+N.wedge(a,db);slot=free[r]%6;q=coeff[slot];dq=dcoeff[slot]
 tc=coeff/q;td=dcoeff/q-coeff*dq/(q*q)
 TC.append(sum(tc[j]*GEN[j] for j in range(6)));TD.append(sum(td[j]*GEN[j] for j in range(6)))
T=[[QI.of(TC[j//6][C.S.PAIRS[j%6][0],C.S.PAIRS[j%6][1]]) if k==j//6 else QI() for k in range(4)] for j in range(24)]
assert not any(v for row in mul(J,T) for v in row)
Gam=[]
for mu in range(4):
 p=[QI(0,1)]*4;n=p[:];p[mu]=QI.of(1);n[mu]=QI.of(-1)
 hp,cp=C.symbol(S0.tolist(),p,True);hn,cn=C.symbol(S0.tolist(),n,True)
 d=[[(a-b)/2 for a,b in zip(ra,rb)] for ra,rb in zip(hn+cn,hp+cp)]
 Gam.append(mul(mul(B,d),T))
R=[]
for g in Gam:
 real=[[F(0)]*8 for _ in range(28)]
 for o in range(14):
  for j in range(4):
   real[o][j]=g[o][j].im/2;real[o][j+4]=-g[o][j].re/2;real[o+14][j]=-g[o][j].re/2;real[o+14][j+4]=-g[o][j].im/2
 R.append(real)
GG=sp.Matrix([[sp.Rational(v) for mu in range(4) for v in R[mu][r]] for r in range(28)])
ANN=sp.Matrix.hstack(*GG.T.nullspace()).T
owned_gamma=json.loads((MODULE_DIR/'a4d_spatial_transport_entropy_results.json').read_text())['first_slow_full_gamma']
assert R==[[[F(v) for v in row] for row in gm] for gm in owned_gamma]
print('PASS_OWNED_LITERAL_FIRSTSLOW_GAMMA_IDENTITY',flush=True)
WG=[];DW=[]
eta=np.diag(C.S.ETA_SIG).astype(object);qi=np.array(sp.Matrix(S0.T@eta@S0).inv().tolist(),dtype=object);qi=np.array([[F(v) for v in row] for row in qi],dtype=object)
for r,s in C.S.PAIRS:
 u,v=[j for j in range(4) if j not in (r,s)]
 w=N.orient(r,s)*N.weight(N.wedge(S0[:,u],S0[:,v]));wd=N.orient(r,s)*N.weight(N.wedge(SD[:,u],S0[:,v])+N.wedge(S0[:,u],SD[:,v]));WG.append((w,wd))
 dd=[]
 for a,b in C.S.SYM:
  dq=Z.copy();dq[a,b]=dq[b,a]=1;ds=S0@qi@dq*F(1,2)
  dd.append(N.orient(r,s)*N.weight(N.wedge(ds[:,u],S0[:,v])+N.wedge(S0[:,u],ds[:,v])))
 DW.append(dd)

def const(A):return [A.copy(),Z.copy(),Z.copy(),Z.copy()]
def jm(A,B):return [A[0]@B[0],A[1]@B[0]+A[0]@B[1],A[2]@B[0]+A[0]@B[2],A[3]@B[0]+A[1]@B[2]+A[2]@B[1]+A[0]@B[3]]
def ji(A):return [a.T*eta.diagonal()[:,None]*eta.diagonal()[None,:] for a in A]
def ej(mu,kk,role):
 ek=np.zeros((4,24),dtype=object);eq=np.zeros((4,10),dtype=object)
 powers=[QI.of(1),QI(0,1),QI.of(-1),QI(0,-1)]
 def link(pos,r):
  phase=powers[sum(pos)%4];tt=TC[r] if r==role else Z;td=TD[r] if r==role else Z
  return [I,kk[r],tt*phase,(kk[r]@tt+pos[mu]*td)*phase]
 for face,(r,s) in enumerate(C.S.PAIRS):
  er=tuple(int(j==r) for j in range(4));es=tuple(int(j==s) for j in range(4))
  for base in ((0,0,0,0),tuple(-v for v in er),tuple(-v for v in es)):
   def plus(a,b):return tuple(x+y for x,y in zip(a,b))
   loc=[(base,r,False),(plus(base,er),s,False),(plus(base,es),r,True),(base,s,True)]
   fac=[ji(link(p,a)) if inv else link(p,a) for p,a,inv in loc]
   pref=[const(I)]
   for f in fac:pref.append(jm(pref[-1],f))
   if base==(0,0,0,0):
    for q in range(10):
     for d in range(4):eq[d,q]+=np.sum(DW[face][q]*pref[4][d])
   w,wd=WG[face];wj=[w,base[mu]*wd,Z,Z]
   for k,(pos,a,inv) in enumerate(loc):
    if pos!=(0,0,0,0):continue
    for g in range(6):
     df=[-GEN[g]@v if inv else v@GEN[g] for v in fac[k]]
     p=const(I)
     for o in range(4):p=jm(p,df if o==k else fac[o])
     ek[0,6*a+g]+=np.sum(wj[0]*p[0])
     ek[1,6*a+g]+=np.sum(wj[0]*p[1]+wj[1]*p[0])
     ek[2,6*a+g]+=np.sum(wj[0]*p[2])
     ek[3,6*a+g]+=np.sum(wj[0]*p[3]+wj[1]*p[2])
 return ek,eq
h0,c0=C.symbol(S0.tolist(),[1]*4,True);HH=sp.Matrix([[sp.Rational(v.re) for v in row] for row in h0]);HHI=HH.inv();print('H0_det',HH.det(),flush=True)
for mu in range(4):
 k0=[Z]*4;ek,eq=ej(mu,k0,-1);force=sp.Matrix([sp.Rational(v.re) if isinstance(v,QI) else sp.Rational(v) for v in ek[1]])
 co=-HHI*force;kk=[sum(F(co[6*r+g])*GEN[g] for g in range(6)) for r in range(4)]
 ek,eq=ej(mu,kk,-1);assert not any(ek[1]),ek[1]
 RR=[]
 for role in range(4):
  ek,eq=ej(mu,kk,role)
  assert not any(list(ek[2])+list(eq[2])), ('bad frozen kernel',role)
  forcing=[QI.of(x) for x in list(ek[3])+list(eq[3])]
  RR.append([sum((b*v for b,v in zip(row,forcing)),QI()) for row in B])
 real=[[F(0)]*8 for _ in range(28)]
 for o in range(14):
  for j in range(4):
   v=RR[j][o];real[o][j]=v.re/2;real[o][j+4]=v.im/2;real[o+14][j]=v.im/2;real[o+14][j+4]=-v.re/2
 M=sp.Matrix([[sp.Rational(v) for v in row] for row in real]);P=ANN*M
 print('mu',mu,'background_k',[str(v) for v in co],'subprincipal_rank',M.rank(),'N_sub_rank',P.rank(),'N_sub_nonzero',sum(v!=0 for v in P),'N_sub_max',max([abs(v) for v in P]),flush=True)


 JETS.append({'mu':mu,'background_coeffs':[str(v) for v in co],'N_sub':[[str(v) for v in row] for row in P.tolist()],'subprincipal':[[str(v) for v in row] for row in M.tolist()],'kernel':[[str(v) for v in w] for w in P.nullspace()]})

P=MODULE_DIR
D=json.loads((P/'a4d_quartic_joint_transport_syzygy_results.json').read_text())
E=json.loads((P/'a4d_spatial_transport_entropy_results.json').read_text())
Q=json.loads((P/'a4d_identity_quarter_nonlinear_response_results.json').read_text())
R=json.loads((P/'a4d_full_quartic_source_quotient_results.json').read_text())
G=sp.Matrix([[sp.Rational(v) for mu in range(4) for v in E['first_slow_full_gamma'][mu][r]] for r in range(28)])
N=[[F(v) for v in row] for row in D['annihilator']]
assert N==[[F(v) for v in n] for n in G.T.nullspace()]

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def ev(poly,c):
 out=F(0)
 for m,v in poly:
  a=F(v)
  for j in m:a*=c[j]
  out+=a
 return out

def gates(c):
 q=[F(0)]*10;k=[F(0)]*28
 for m,row in zip(Q['quadratic_monomials'],Q['quadratic_gate_coefficients']):
  a=F(1)
  for j in m:a*=c[j]
  q=[x+a*F(v) for x,v in zip(q,row)]
 for m,row in zip(Q['cubic_monomials'],Q['cubic_gate_coefficients']):
  a=F(1)
  for j in m:a*=c[j]
  k=[x+a*F(v) for x,v in zip(k,row)]
 return q,[dot(n,k) for n in N]

def readout(c):
 out=[F(0)]*10
 for powers,row in zip(R['quartic_readout_monomial_powers'],R['complete_quartic_readout_coefficients']):
  a=F(1)
  for j,k in enumerate(powers):a*=c[j]**k
  out=[x+a*F(v) for x,v in zip(out,row)]
 return out
J=JETS
assert [sp.Matrix(j['N_sub']).rank() for j in J]==[4,0,4,4]
c=[F(x) for x in (0,1,0,0,0,0,1,0)];q,k=gates(c);assert not any(q) and any(k)
M=[[F(v) for v in row] for row in J[3]['N_sub']];g=[dot(row,c) for row in M]
w=next(x for x in D['identity_witnesses'] if x['coordinate']==1 and x['metric_slot']==0)
contract=sum(ev(poly,c)*g[j] for j,poly in w['annihilator_multipliers']);assert contract==-F(409,1980)
survivors=[]
for c in ((0,1,0,0,0,0,0,1),(0,0,0,-1,0,1,0,0)):
 c=[F(v) for v in c];q,k=gates(c);v=readout(c)
 assert not any(q) and any(k) and not any(dot(row,c) for row in M)
 assert v==[F(1,16),0,-F(1,8),0,0,0,0,F(1,16),0,0]
 survivors.append({'amplitudes':[str(x) for x in c],'R4':[str(x) for x in v],'NQ3_nonzero':sum(x!=0 for x in k)})
# Exact real source-zero cone in each rank-four kernel.
a,u,v,b=sp.symbols('a u v b', real=True)
for mu in (0,2):
 basis=sp.Matrix.hstack(*sp.Matrix(J[mu]['N_sub']).nullspace());c=basis*sp.Matrix((a,u,v,b))
 t1=sp.expand(c[0]*c[4]);t5=sp.expand(c[0]*c[5]+c[1]*c[4]);t6=sp.expand(c[0]*c[6]+c[2]*c[4])
 assert t1 in (u*v,-u*v) and (t5 in (u*u-v*v,v*v-u*u) or t6 in (u*u-v*v,v*v-u*u))
 # t1=0 and u²-v²=0 force u=v=0 over R. Remaining t4=a*b=0.
 assert sp.expand(c[3]*c[7])==a*b
# mu3: kernel columns parameterize c=(-u,z,u,-v,-w,v,w,z).
basis=sp.Matrix.hstack(*sp.Matrix(J[3]['N_sub']).nullspace());c=basis*sp.Matrix((u,v,a,b))
assert list(c)==[-u,b,u,-v,-a,v,a,b]
t0=sp.expand(c[0]*(c[1]-c[2]+c[3])-c[4]*(c[5]-c[6]+c[7]))
t1=sp.expand(c[0]*c[4]);t2=sp.expand(c[1]*c[5])
t5=sp.expand(c[0]*c[5]+c[1]*c[4]);t7=sp.expand(c[0]*c[7]+c[3]*c[4])
assert t1==u*a and t2==b*v and t5==-u*v-b*a and t7==-u*b+v*a
assert t0==u*u-a*a+u*v-u*b+a*v+a*b
assert t0.subs({a:0,v:0,b:0})==u*u
assert t0.subs({u:0,v:0,b:0})==-a*a
# t1=u*a; t5=-u*v-b*a; t7=-u*b+v*a.
# If u!=0, a=0 => v=b=0 => t0=u², contradiction.
# If a!=0, u=0 => v=b=0 => t0=-a², contradiction.
# Hence u=a=0 and t2=b*v=0: the two visible survivor axes above.
# A common linear detector that additionally erases all four first-gradient
# forcings on this one solder path loses observable sufficiency.
EXT=sp.Matrix.hstack(G,*[sp.Matrix(j['subprincipal']) for j in J]).T.nullspace()
assert len(EXT)==8
EXTF=[[F(v) for v in n] for n in EXT]
ext_controls=[]
for c in ((0,1,0,0,0,0,1,0),(0,1,0,0,0,0,0,1)):
 c=[F(v) for v in c];q,ordinary_gate=gates(c);raw=[F(0)]*28
 for mon,row in zip(Q['cubic_monomials'],Q['cubic_gate_coefficients']):
  z=F(1)
  for index in mon:z*=c[index]
  raw=[v+z*F(a) for v,a in zip(raw,row)]
 ext_gate=[dot(n,raw) for n in EXTF];metric=readout(c)
 assert not any(q) and any(ordinary_gate) and not any(ext_gate) and metric[0]==F(1,16)
 # At c_1=1, slot00 is1/16 while every proposed generator is0.
 assert c[1]*metric[0]==F(1,16)
 ext_controls.append({'amplitudes':[str(v) for v in c],'R4':[str(v) for v in metric],
                      'extended_cubic_gates':[str(v) for v in ext_gate],
                      'ordinary_annihilator_gate_nonzero':sum(v!=0 for v in ordinary_gate)})
print('PASS_COMMON_COFRAME_GRADIENT_ANNIHILATOR_LOSES_QUARTIC_READOUT',flush=True)
report={'model':'single two-shear affine coframe jet at s=0, ds=1; full literal local shared-link eps*delta coefficient',
 'source_git_blobs':SOURCE_GIT_BLOBS,
 'base_joint_first_slow_rank':12,'base_common_annihilator_rows':16,'subprincipal_annihilator_ranks':[4,0,4,4],
 'jet_ledgers':[{key:j[key] for key in ('mu','background_coeffs','N_sub','kernel')} for j in J],'existing_witness_coordinate':1,'existing_witness_metric_slot':0,
 'existing_witness_mu3_sourcezero_atom_contraction':str(contract),'mu3_sourcezero_survivors':survivors,
 'mu0_mu2_real_sourcezero_survivors':'only a3 or b3 axis; R4 zero',
 'extended_pointwise_annihilator_dimension':8,'extended_pointwise_annihilator':[[str(v) for v in n] for n in EXTF],
 'extended_annihilator_visible_zero_gate_controls':ext_controls,
 'nonclaims':['No exact joint field or globally periodic coframe is constructed.','No alternate covariant multiplier is excluded; the extended-annihilator control rules out only one common linear pointwise detector erasing every first-gradient direction on this path.','No fixed-source or raw-norm theorem is asserted.','This controls only the first coframe-gradient joint forcing; higher subprincipal orders remain.']}
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-json',action='store_true');args=parser.parse_args()
target=Path(__file__).with_name('a4d_two_shear_subprincipal_pullback_results.json')
if args.write_json:target.write_text(json.dumps(report,indent=2)+'\n')
else:assert json.loads(target.read_text())==report,'pinned subprincipal ledger changed'
print('PASS_PINNED_SUBPRINCIPAL_LEDGER',flush=True)
print('ELAPSED_SECONDS',round(time.monotonic()-RUN_START,2),flush=True)
print('PASS_LITERAL_STATIONARY_BACKGROUND_AND_FROZEN_JOINT_KERNEL_ASSERTIONS_FROM_JET_ASSEMBLER')
print('PASS_EXACT_COMMON_N_BASIS_MATCH_AND_REAL_SOURCEZERO_KERNEL_CONTROLS')
print('PASS_EXISTING_WITNESS_Q2_IDEAL_PULLBACK_REJECTED: -409/1980')
print('PASS_SURVIVOR_NONZERO_R4_WITH_NONZERO_NQ3; NOT_EXACT_ROOTS')
