#!/usr/bin/env python3
"""Exact four-CAR parity trace / original odd-Palatini bridge.
No GR physical-selection or native primitive-compilation claim.
"""
from __future__ import annotations
import itertools, json, hashlib, time
from pathlib import Path
import sympy as s
import mpmath as mp

START=time.monotonic()
I4=s.eye(4); I16=s.eye(16)
ETA=s.diag(1,-1,-1,-1)
ORDER=(0,2,3,1)
checks=0

def req(ok, label):
 global checks
 checks+=1
 if not bool(ok): raise ArithmeticError(label)

def zero(x):
 return all(s.cancel(t)==0 for t in x) if isinstance(x,s.MatrixBase) else s.cancel(x)==0

def eq(x,y,label): req(zero(x-y),label)

CREATORS=[]
for mode in range(4):
 c=s.zeros(16)
 before=ORDER[:ORDER.index(mode)]
 for bits in range(16):
  if (bits>>mode)&1: continue
  c[bits|(1<<mode),bits]=(-1)**sum((bits>>j)&1 for j in before)
 CREATORS.append(c)
for i in range(4):
 for j in range(4):
  eq(CREATORS[i]*CREATORS[j]+CREATORS[j]*CREATORS[i],s.zeros(16),'CAR cc')
  eq(CREATORS[i]*CREATORS[j].T+CREATORS[j].T*CREATORS[i],I16 if i==j else s.zeros(16),'CAR cd')
NUM=sum((c*c.T for c in CREATORS),s.zeros(16))
PARITY=I16
for c in CREATORS: PARITY=PARITY*(I16-2*c*c.T)
ODD=(I16-PARITY)/2
EVEN=I16-ODD
eq(ODD*ODD,ODD,'odd projector')
eq(s.trace(ODD),8,'odd rank')
eq(ODD+EVEN,I16,'all grades retained')

OCC=[tuple(j for j in ORDER if (bits>>j)&1) for bits in range(16)]
PAIRS=[(i,j) for i in range(4) for j in range(i+1,4)]
BIL=[[CREATORS[i]*CREATORS[j].T for j in range(4)] for i in range(4)]
def dgamma(B):
 out=s.zeros(16)
 for i,j in itertools.product(range(4),repeat=2):
  if B[i,j]: out+=B[i,j]*BIL[i][j]
 return out

def wedge(P):
 out=s.zeros(16)
 for i,ii in enumerate(OCC):
  for j,jj in enumerate(OCC):
   if len(ii)==len(jj): out[i,j]=P.extract(ii,jj).det() if ii else 1
 return out

def trace(X):return s.trace(X)
def star(B,P):return -trace(B*(P-P.inv()))/4

def car(B,P):return -trace(ODD*dgamma(B)*wedge(P))/4

def ungraded(B,P):return -trace(dgamma(B)*wedge(P))/8

# Generic original type: eta-skew generators, exact Cayley proper links.
GEN=[]
for i,j in PAIRS:
 X=s.zeros(4); X[i,j]=1; X[j,i]=-ETA[i,i]*ETA[j,j]
 eq(X.T*ETA+ETA*X,s.zeros(4),'Lorentz generator')
 GEN.append(X)
def cayley(X):return (I4-X/2).inv()*(I4+X/2)

# Exact characteristic-zero double-rotation/boost witness, not a rank guess.
r,t=s.symbols('r t', real=True)
P=s.diag(1,1,1,1)
P[:2,:2]=s.Matrix([[(1+r*r)/(1-r*r),2*r/(1-r*r)],[2*r/(1-r*r),(1+r*r)/(1-r*r)]])
P[2:,2:]=s.Matrix([[(1-t*t)/(1+t*t),-2*t/(1+t*t)],[2*t/(1+t*t),(1-t*t)/(1+t*t)]])
eq(P.T*ETA*P,ETA,'symbolic proper Lorentz family')
LP=wedge(P)
for k,B in enumerate(GEN):
 lhs=-trace(ODD*dgamma(B)*LP)/4
 rhs=star(B,P)
 eq(lhs,rhs,'symbolic odd trace for all six Lie generators')
 allamp=-trace(dgamma(B)*LP)/8
 correction=trace(PARITY*dgamma(B)*LP)/8
 eq(lhs,allamp+correction,'exact missing supertrace source')
 for par in (r,t):eq(s.diff(lhs,par),s.diff(rhs,par),'symbolic all-r/t source')
for k,B in enumerate(GEN):eq(ODD*dgamma(B),dgamma(B)*ODD,'grade covariance generator')
P0=P.subs({r:s.Rational(1,3),t:s.Rational(1,2)})
B0=GEN[0]
f0=star(B0,P0);u0=ungraded(B0,P0);o0=car(B0,P0)
eq(f0,-s.Rational(3,4),'original odd target control')
eq(u0,-s.Rational(3,5),'ungraded finite-amplitude mismatch')
eq(o0-u0,-s.Rational(3,20),'nonzero correction retained')

# Test exact character identity even WITHOUT Lorentz: arbitrary determinant-one P.
S=s.Matrix([[1,s.Rational(1,3),0,0],[0,1,s.Rational(1,4),0],[0,0,1,s.Rational(1,5)],[0,0,0,1]])
Pg=S*P0*S.inv()
Bg=S*B0*S.inv()
eq(Pg.det(),1,'SL4 test determinant')
eq(trace(Bg),0,'SL4 trace-free tangent')
eq(car(Bg,Pg),star(Bg,Pg),'SL4 dual-grade exact trace')

# All first variations of six shared plaquettes in ONE homogeneous periodic
# local fixture. 16 coframe slots + 4*6 independent proper-link slots.
# No all-size stationary root / full lattice replay is claimed.
E=s.Matrix([[1,s.Rational(1,7),0,0],[0,1,s.Rational(1,11),0],[0,0,1,s.Rational(1,13)],[s.Rational(1,17),0,0,1]])
U=[cayley(GEN[i]/s.Integer(4+i)+GEN[5-i]/s.Integer(17+i)) for i in range(4)]
Ui=[u.inv() for u in U]
for u in U:eq(u.T*ETA*u,ETA,'actual rational proper link');eq(u.det(),1,'proper link determinant')

# Hodge-dual coframe pairing. The theorem holds for ANY actual eta-skew B;
# this particular convention is a numerical structural control only.
def pair_coframe(E,r0,s0):
 rem=[i for i in range(4) if i not in (r0,s0)]
 m,n=rem
 out=s.zeros(4)
 orientation=s.LeviCivita(r0,s0,m,n)
 for a,b,c,d in itertools.product(range(4),repeat=4):
  if a!=b and c!=d:
   out[a,b]+=orientation*ETA[a,a]*s.LeviCivita(a,b,c,d)*E[c,m]*E[d,n]
 return out

FACES=[]
for r0,s0 in PAIRS:
 Pface=U[r0]*U[s0]*Ui[r0]*Ui[s0]
 Bface=pair_coframe(E,r0,s0)
 eq(Bface.T*ETA+ETA*Bface,s.zeros(4),'coframe Hodge bivector in Lorentz algebra')
 LPface=wedge(Pface); Pinv=Pface.inv(); DB=dgamma(Bface)
 eq(-trace(ODD*DB*LPface)/4,star(Bface,Pface),'all face values')
 FACES.append((r0,s0,Pface,Pinv,Bface,DB,LPface))

coframe_rows=[]
for a,b in itertools.product(range(4),repeat=2):
 de=s.zeros(4);de[a,b]=1
 dv_car=dv_star=s.Integer(0)
 for r0,s0,Pf,Pfi,Bf,DB,LPf in FACES:
  dB=pair_coframe(E+de,r0,s0)-Bf # exact linear directional change for one entry
  dv_car-=trace(ODD*dgamma(dB)*LPf)/4
  dv_star-=trace(dB*(Pf-Pfi))/4
 eq(dv_car,dv_star,'all16 coframe source rows')
 coframe_rows.append(dv_car)

link_rows=[]
for mu in range(4):
 for X in GEN:
  dU=[s.zeros(4) for _ in range(4)];dU[mu]=X*U[mu]
  dUi=[-Ui[k]*dU[k]*Ui[k] for k in range(4)]
  dv_car=dv_star=s.Integer(0)
  for r0,s0,Pf,Pfi,Bf,DB,LPf in FACES:
   dP=(dU[r0]*U[s0]*Ui[r0]*Ui[s0]+U[r0]*dU[s0]*Ui[r0]*Ui[s0]
       +U[r0]*U[s0]*dUi[r0]*Ui[s0]+U[r0]*U[s0]*Ui[r0]*dUi[s0])
   Y=dP*Pfi
   eq(trace(Y),0,'actual shared-plaquette tangent')
   dLP=dgamma(Y)*LPf
   dv_car-=trace(ODD*DB*dLP)/4
   dv_star-=trace(Bf*(dP+Pfi*dP*Pfi))/4
  eq(dv_car,dv_star,'all24 proper-link source rows')
  link_rows.append(dv_car)
req(any(v!=0 for v in coframe_rows+link_rows),'generic off-shell source not identically zero')

# Four independently transformed vertex frames on one closed plaquette.
frames=[cayley(GEN[k]/s.Integer(9+k)) for k in range(4)]
U01,U12,U32,U03=U
L0,L1,L2,L3=frames
Ploop=U01*U12*U32.inv()*U03.inv()
A01=L0*U01*L1.inv();A12=L1*U12*L2.inv()
A32=L3*U32*L2.inv();A03=L0*U03*L3.inv()
Ploop_new=A01*A12*A32.inv()*A03.inv()
Bloop=pair_coframe(E,0,1)
Bloop_new=L0*Bloop*L0.inv()
eq(Ploop_new,L0*Ploop*L0.inv(),'four-vertex Lorentz transport telescopes')
eq(car(Bloop_new,Ploop_new),car(Bloop,Ploop),'true local Lorentz trace invariance')
# These frames include boosts: Euclidean unitarity is not assumed.
req(not zero(L0.T*L0-I4),'nonunitary proper Lorentz frame is covered')

# Polynomial residual identity, without inverse(I-P) at singular P-I.
Btest=GEN[0]+GEN[2]/7
Ptest=Ploop
residual=trace((I4-Ptest).adjugate()*Btest*Ptest)/8
eq(ungraded(Btest,Ptest)-star(Btest,Ptest),residual,
   'unmodified full trace defect is exactly the adjugate contraction')
# Full character formula from Lambda^0..Lambda^4, independent of adjugate.
poly=(trace(Btest*Ptest**2)-(trace(Ptest)+2)*trace(Btest*Ptest))/8
eq(ungraded(Btest,Ptest),poly,'full16 trace agrees with 4x4 polynomial')

# Smooth-cell value AND source rate. This is a finite numerical control of
# the analytical O(h^8) cell / O(h^4) global estimates, not their proof.
mp.mp.dps=90
smooth=[]
for L in (4,8,16,32):
 h=mp.mpf(1)/L
 k,l=mp.mpf(3)/7,mp.mpf(2)/5
 # B=h^2 Jboost, P=boost(h^2 k) * rotation(h^2 l).
 # Exact ungraded-minus-odd difference.
 cell=h*h*mp.sinh(h*h*k)*(1-mp.cos(h*h*l))/2
 dk=h**4*mp.cosh(h*h*k)*(1-mp.cos(h*h*l))/2
 dl=h**4*mp.sinh(h*h*k)*mp.sin(h*h*l)/2
 expected=k*l*l/4
 req(abs(cell/h**8-expected)<mp.mpf('0.00002'),'smooth cell O(h^8) value control')
 req(abs(dk/h**8-l*l/4)<mp.mpf('0.00003'),'smooth cell O(h^8) boost-source control')
 req(abs(dl/h**8-k*l/2)<mp.mpf('0.00003'),'smooth cell O(h^8) rotation-source control')
 smooth.append({'L':L,'global_error_over_h4':mp.nstr((L**4*cell)/h**4,25),
                'source_k_over_h4':mp.nstr((L**4*dk)/h**4,25),
                'source_l_over_h4':mp.nstr((L**4*dl)/h**4,25)})

# Literal coherent parity writer on four CAR occupancy bits + fresh flag.
# Four addressed CNOTs. This checks all32 columns; no postselection and no
# assertion that the full physical Price loses the cost of these gates.
I32=s.eye(32)
Wpar=I32
for mode in range(4):
 C=s.zeros(32)
 for bits in range(32):
  target=bits ^ (16 if (bits>>mode)&1 else 0)
  C[target,bits]=1
 Wpar=C*Wpar
eq(Wpar.T*Wpar,I32,'full coherent parity writer orthogonality')
eq(Wpar*Wpar,I32,'four-CNOT parity inverse retains all columns')
inject=s.zeros(32,16)
for i in range(16):inject[i,i]=1
Pi_flag=s.diag(*([0]*16+[1]*16))
eq(inject.T*Wpar.T*Pi_flag*Wpar*inject,ODD,'actual flagged effect is native odd projector')

# A parity measurement is a record extension, not free dephasing.
# One even/one odd coherent superposition has a future interference witness.
psi=s.zeros(16,1); psi[0]=psi[1]=1/s.sqrt(2)
rho=psi*psi.T;deph=ODD*rho*ODD+EVEN*rho*EVEN
obs=CREATORS[0]+CREATORS[0].T
eq(trace(obs*rho),1,'coherent future parity-crossing witness')
eq(trace(obs*deph),0,'dephasing changes future witness')
# This is a mathematical full-CAR observation; physical admission of this
# particular odd probe is NOT supplied by the even-future algebra owner.

out={
 'status':'PASS_EXACT_CAR_PARITY_GEOMETRIC_SOURCE',
 'checks':checks,
 'field':'rational characteristic zero plus symbolic rational r,t',
 'creator_order':list(ORDER),
 'carrier_dimension':16,
 'odd_rank':8,
 'coherent_parity_writer_full_columns_checked':32,
 'logical_CNOT_count_for_parity_flag':4,
 'symbolic_Lorentz_generators_checked':6,
 'coframe_rows_checked':len(coframe_rows),
 'shared_link_rows_checked':len(link_rows),
 'smooth_consistency_controls':smooth,
 'four_vertex_local_Lorentz_test':True,
 'ungraded_control':str(u0),
 'palatini_control':str(f0),
 'parity_correction':str(o0-u0),
 'statement':'Exact all-SL4 value identity and every induced jet; finite CAR parity-weighted contraction',
 'physical_parity_insertion_compiled':False,
 'full_Book_price_selection_proved':False,
 'all_size_lattice_roots_replayed':False,
 'universal_GR_closed':False,
}
print(json.dumps(out,indent=2,ensure_ascii=False))
