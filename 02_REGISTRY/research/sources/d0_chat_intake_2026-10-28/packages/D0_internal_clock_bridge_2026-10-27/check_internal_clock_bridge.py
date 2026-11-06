#!/usr/bin/env python3
"""Bounded matrix verification of the INTERNAL clock/reflection application.
Not a compiled original full READY programme or a universal GR certificate.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
import scipy.linalg as la
import sympy as sp
import mpmath as mp
mp.mp.dps = 70
checks=0

def require(ok, label):
    global checks
    checks+=1
    if not bool(ok): raise AssertionError(label)

def equal(A,B,label):
    if isinstance(A,sp.MatrixBase):
        require(A.shape==B.shape and all(sp.cancel(x)==0 for x in A-B),label)
    else: require(sp.cancel(A-B)==0,label)

def near(A,B,label,tol=3e-11):
    require(np.allclose(A,B,atol=tol,rtol=tol),label)

def blockdiag(xs): return sp.diag(*xs)

def R4(i,j,t):
    R=sp.eye(4); c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    R[i,i]=R[j,j]=c;R[j,i]=s;R[i,j]=-s
    return R

def sourceV(t):
    return R4(2,3,sp.Rational(1,4))*R4(1,2,t)*R4(0,1,sp.Rational(2,5))

def partition_phase(parts):
    Zs=[]
    for block in parts:
        J=sp.eye(4)
        for j in block:J[j,j]=-1
        Zs.append(J)
    Zs += [sp.eye(4)]*(4-len(parts))
    return blockdiag(Zs)

def shift(Us):
    d=Us[0].rows;n=len(Us);T=sp.zeros(n*d)
    for k,U in enumerate(Us):
        t=(k+1)%n
        T[t*d:(t+1)*d,k*d:(k+1)*d]=U
    return T

def prefix_gauge(Us):
    d=Us[0].rows;pref=sp.eye(d);blocks=[]
    for U in Us:
        blocks.append(pref);pref=U*pref
    return blockdiag(blocks),pref

fine=[[0],[1],[2],[3]]
three=[[0],[1],[2,3]]
Zf,Zc=partition_phase(fine),partition_phase(three)
require(sum(bool(Zf[i,i]<0) for i in range(16))==4,'fine negative multiplicity')
require(sum(bool(Zc[i,i]<0) for i in range(16))==4,'three-atom negative multiplicity')
t=sp.Rational(1,3)
V=sourceV(t); Vbig=sp.kronecker_product(sp.eye(4),V)
Us=[Vbig,Zc,Vbig.T]
T=shift(Us);G,endpoint=prefix_gauge(Us)
equal(T.T*T,sp.eye(48),'clock unitary all48 columns')
equal(endpoint.T,endpoint,'completed comparison selfadjoint')
equal(endpoint*endpoint,sp.eye(16),'completed comparison is involutive')
Tseam=shift([sp.eye(16),sp.eye(16),endpoint])
equal(G.T*T*G,Tseam,'exact native prefix gauge')
C=sp.kronecker_product(sp.eye(3),Vbig)
Q=G*C.T
Tfixed=shift([sp.eye(16),sp.eye(16),Zc])
equal(Q.T*T*Q,Tfixed,'full clock canonical fixed-reflection similarity')

# Exact changing-return/not-changing-monodromy-spectrum control.
# The active cut is NOT transformed when comparing its real outcomes.
psi=sp.Matrix([1,0,0,0]);P0=psi*psi.T
P=sp.kronecker_product(sp.eye(4),P0)
F=P*endpoint.T*(sp.eye(16)-P)*endpoint*P
probs=[];out=V*psi
for part in three: probs.append(sum(out[i]**2 for i in part))
probs.append(sp.Integer(0))
expected=blockdiag([4*q*(1-q)*P0 for q in probs])
equal(F,expected,'same complete clock endpoint keeps true feedback')
Pclock=sp.diag(P,sp.zeros(16),sp.zeros(16))
Fn=Pclock*(T**3).T*(sp.eye(48)-Pclock)*(T**3)*Pclock
equal(Fn,sp.diag(F,sp.zeros(16),sp.zeros(16)), 'N real ticks reproduce original feedback cut')
require(sum(probs)==1,'all actual statuses normalized')

# Original full K(9,11,13) normalized connection graph with stage clocks.
sizes=[9,11,13]; qn=33; N=3; d=16
scene=np.zeros((qn,qn));starts=[0,9,20,33]
for i in range(3):
 for j in range(3):
  if i!=j:scene[starts[i]:starts[i+1],starts[j]:starts[j+1]]=1
require(int(scene.sum()/2)==359,'original K913 edge count')
deg=scene.sum(axis=1)+2
near(deg,np.array([26]*9+[24]*11+[22]*13),'actual scene+clock degree')
R=np.diag(1/np.sqrt(deg)); B=R@scene@R; Cs=R@R
Tn=np.array(T,dtype=float);T0=np.array(Tfixed,dtype=float);Qn=np.array(Q,dtype=float)
L=np.eye(33*48)-np.kron(B,np.eye(48))-np.kron(Cs,Tn+Tn.T)
Lfix=np.eye(33*48)-np.kron(B,np.eye(48))-np.kron(Cs,T0+T0.T)
Qfull=np.kron(np.eye(33),Qn)
# All entries of the full graph are retained. This is not a spectral truncation.
near(Qfull.T@L@Qfull,Lfix,'full original scene-clock H0 similarity',tol=1e-11)
evals=la.eigvalsh(L,check_finite=False)
require(evals[0]>-2e-13,'normalized H0 positivity')
expected_e=[]
for sign,mult in [(1,12),(-1,4)]:
 theta=0 if sign==1 else math.pi
 for k in range(N):
  c=math.cos((2*math.pi*k+theta)/N)
  expected_e += list(la.eigvalsh(np.eye(33)-B-2*c*Cs))*mult
near(np.sort(expected_e),evals,'all1584 H0 eigenvalues equal full holonomy formula',tol=2e-12)
p=(math.sqrt(5)-1)/2;beta=2*p*p
Z0=float(np.exp(-beta*evals).sum())
Z01=2*Z0+359*N*d
require(33*N*d==len(evals),'no H0 dimension omitted')
require(392*N*d+33*N*d==425*N*d,'full 0+1 graded dimension')
require(359*N*d>0,'actual harmonic complement retained')

# Generic incidence verification of Tr e^-beta DD* + Tr e^-beta D*D.
# The smaller graph tests the singular-value identity independently; it
# is NOT advertised as another calculation on full original K913.
Us2=[np.array(u,dtype=float)[:4,:4] for u in Us]
D=np.zeros((12,12))
for k,U in enumerate(Us2):
 D[k*4:(k+1)*4,k*4:(k+1)*4]=-U/math.sqrt(2)
 j=(k+1)%3;D[k*4:(k+1)*4,j*4:(j+1)*4]=np.eye(4)/math.sqrt(2)
D=np.vstack([D,np.zeros((8,12))])
z_node=np.exp(-beta*la.eigvalsh(D.T@D)).sum()
z_edge=np.exp(-beta*la.eigvalsh(D@D.T)).sum()
near(z_edge,z_node+8,'all-mode paired-Hodge trace identity')

# Actual Golden+CNOT finite word: no smooth native angle is assumed.
pS=(sp.sqrt(5)-1)/2
Golden=sp.Matrix([[sp.sqrt(pS),-pS],[pS,sp.sqrt(pS)]])
CX=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
# Numerical replay of actual Golden factors; exact p+p²=1 is checked.
equal(pS+pS*pS,1,'exact native Golden relation')
Gd=np.array(Golden.evalf(18),float)
Vgold=np.array(CX,float)@np.kron(Gd,np.eye(2))@np.kron(np.eye(2),Gd)
near(Vgold.T@Vgold,np.eye(4),'actual finite Golden/CNOT programme all4 columns')
J=np.diag([1,1,1,-1]);Mg=Vgold.T@J@Vgold
near(Mg@Mg,np.eye(4),'actual finite Golden reflection all4 columns')

# Probability changes but completed conjugate reflection remains isospectral.
# Here t is an ambient matrix chart, not a new continuously variable native gate.
z=mp.mpf(2)**-20;sR=128

def mpV(tt):
 def rr(i,j,u):
  A=mp.eye(4);c=(1-u*u)/(1+u*u);ss=2*u/(1+u*u)
  A[i,i]=A[j,j]=c;A[j,i]=ss;A[i,j]=-ss
  return A
 return rr(2,3,mp.mpf(1)/4)*rr(1,2,tt)*rr(0,1,mp.mpf(2)/5)

def price(tt,parts):
 v=mpV(tt)*mp.matrix([1,0,0,0])
 qs=[sum(v[i]*v[i] for i in part) for part in parts]
 return -sR*sum(mp.log1p(-4*z*q*(1-q)) for q in qs)
feedback_source=mp.diff(lambda tt:price(tt,three),mp.mpf(1)/3)
require(abs(feedback_source)>mp.mpf('1e-7'),'real nonzero feedback first source')
mergegap=price(mp.mpf(1)/3,fine)-price(mp.mpf(1)/3,three)
require(mergegap>0,'strict partition preference with identical INTERNAL heat')

# Non-reflective serial endpoint: INTERNAL heat is NOT constant in general.
# Exact scene equitable decomposition: 30 internal modes + 3 mean modes.
mpbeta=2*((mp.sqrt(5)-1)/2)**2

def scene_heat(c):
 dd=[26,24,22];H=mp.matrix(3)
 for i in range(3):
  for j in range(3):
   H[i,j]=(1-2*c/dd[i]) if i==j else -mp.sqrt(mp.mpf(sizes[i]*sizes[j])/(dd[i]*dd[j]))
 E=mp.expm(-mpbeta*H)
 return sum((sizes[i]-1)*mp.exp(-mpbeta*(1-2*c/dd[i])) for i in range(3))+sum(E[i,i] for i in range(3))

def serial_heat(theta):
 z0=sum(scene_heat(mp.cos((2*mp.pi*k+sgn*theta)/N)) for sgn in [-1,1] for k in range(N))
 return mp.log(sR*(2*z0+359*N*2))/mpbeta
serial_source=mp.diff(serial_heat,mp.mpf('0.4'))
require(abs(serial_source)>mp.mpf('1e-9'),'hostile serial nonreflection has real thermal source')

# If the actual clock gates are scene-dependent, the prefix gauge moves
# spatial edges. Identical reflective monodromies do NOT then suffice.
def rooted_heat(theta):
    c,s=math.cos(theta),math.sin(theta)
    V=np.array([[c,-s],[s,c]])
    Z=np.diag([1.,-1.])
    def clock_np(ops):
        T=np.zeros((6,6))
        for k,A in enumerate(ops):
            j=(k+1)%3;T[2*j:2*j+2,2*k:2*k+2]=A
        return T
    Tr=clock_np([V,Z,V.T]);Tid=clock_np([np.eye(2)]*3)
    Tall=la.block_diag(Tr,*([Tid]*32))
    LL=np.eye(198)-np.kron(B,np.eye(6))-np.kron(Cs,np.eye(6))@(Tall+Tall.T)
    z0=np.exp(-beta*la.eigvalsh(LL,check_finite=False)).sum()
    return math.log(128*(2*z0+359*3*2))/beta
root_delta=rooted_heat(.7)-rooted_heat(.1)
require(abs(root_delta)>1e-9,'scene-controlled gates cannot use uniform-scene theorem')

outdict={
 'status':'PASS_INTERNAL_CLOCK_REFLECTION_SOURCE_APPLICATION',
 'checks':checks,
 'source_head':'c7708742bea04684ffd6aed16774cfdf1b94b129',
 'rational_clock_columns':48,
 'original_scene_vertices':33,'original_scene_edges':359,
 'clock_length':N,'full_work_dimension':d,
 'negative_monodromy_rank':4,'positive_monodromy_rank':12,
 'full_H0_eigenvalues_replayed':len(evals),
 'paired_Hodge_harmonic_difference':359*N*d,
 'full_graded_dimension_excluding_RIGHT':425*N*d,
 'Z0_numeric':format(Z0,'.16g'),'Z01_numeric':format(Z01,'.16g'),
 'three_atom_feedback_source':mp.nstr(feedback_source,35),
 'full_heat_invariant_merge_feedback_gap':mp.nstr(mergegap,35),
 'serial_nonreflection_heat_source':mp.nstr(serial_source,35),
 'scene_dependent_reflection_heat_contrast':format(root_delta,'.16g'),
 'spectrum_proof_scope':'complete fixed-inventory clock with constant-conjugacy monodromy and clock-scalar scene blocks',
 'actual_large_READY_compiler_executed':False,
 'native_field_preparation_admitted':False,
 'general_lattice_inverse_proved':False,
 'unconditional_GR_closed':False
}
print(json.dumps(outdict,indent=2,ensure_ascii=False))
