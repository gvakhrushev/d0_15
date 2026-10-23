#!/usr/bin/env python3
"""Real original complete 128-Kraus Walsh+Golden instrument at two phase profiles.
Checks exact full-flag two-tick vacuum->CAR-top Pluecker area probability.
SOURCE SCOPE: different profiles are separately admitted mathematical native
Fourier symbols, NOT an owned one-geometry moving-background compiler or GR.
"""
import numpy as np
from math import sqrt
nu=3/5
p=(sqrt(5)-1)/2
a=sqrt(p)
I=np.eye(16,dtype=complex)
CRE=[]
for r in range(4):
    C=np.zeros((16,16),complex)
    pred=(0,2,3,1)[:(0,2,3,1).index(r)]
    for mask in range(16):
        if (mask>>r)&1==0:
            C[mask|(1<<r),mask]=(-1)**sum((mask>>j)&1 for j in pred)
    CRE.append(C)
H=np.array([[(-1)**((lab&j).bit_count())/32 for j in range(32)]
             for lab in range(32)],float)
def full128(phases):
    words=[]
    for r in range(4):
        C=CRE[r]
        P=nu*np.exp(1j*phases[r])*C
        L=I-.2*C@C.conj().T
        R=I-.2*C.conj().T@C
        for item in ((P,L),(P.conj().T,R),(-nu*C,-L),
                     (-nu*C.conj().T,-R)):
            words.extend((item,item))
    Q=np.array([np.einsum('ij,jab->iab',H,np.asarray([w[t] for w in words]))
                for t in (0,1)]).transpose(1,0,2,3).reshape(64,16,16)
    A=Q[0] # native hD/16 on this exact Fourier block
    assert np.linalg.norm(A-A.conj().T)<1e-12
    K=np.empty((128,16,16),complex)
    for j,Qj in enumerate(Q):
        K[2*j]=-2*p**2*Qj.conj().T@A
        K[2*j+1]=-2*a*p*Qj.conj().T@A
    K[0]+=I # only blank label/coefficient0/port0 has identity
    complete=np.einsum('kij,kil->jl',K.conj(),K)
    assert np.linalg.norm(complete-I)<1e-12
    return K
def amp(K2,K1):
    return np.einsum('ki,ji->kj',K2[:,15,:],K1[:,:,0])
def leg(t):
    return (nu/16)*(np.exp(-1j*np.array(t))-1)
def area(t1,t2):
    x,y=leg(t1),leg(t2)
    return np.linalg.norm(x)**2*np.linalg.norm(y)**2-abs(np.vdot(x,y))**2
factor=p**4*nu**4/2
for t1,t2 in (
    ((.03,0,0,0),(0,0,.02,0)),
    ((.3,0,0,0),(0,0,.5,0)),
    ((.12,.25,.10,.04),(.24,.01,.09,.03)),
    ((.3,.2,-.3,0),(-.15,.4,0,.2)),
    ((0,0,0,0),(.1,.2,.3,.4)),
):
    first=full128(t1);second=full128(t2)
    A=amp(second,first)
    P=float(np.vdot(A,A).real)
    predicted=float(factor*area(t1,t2))
    assert abs(P-predicted)<max(1e-22,1e-11*predicted)
    assert abs(A.sum())<1e-11
    print('full native profiles',t1,t2,'P_top',P,'analytic Gram area',predicted)
for t in ((.1,.2,.3,.4),(.7,-.8,.21,.4)):
    K=full128(t)
    assert np.linalg.norm(amp(K,K))<1e-12
# Finite EXACT pair-of-axes sine law, original unmodified port normalization.
s1,s2=.7,.8
K1=full128((s1,0,0,0));K2=full128((0,0,s2,0))
P=float(np.linalg.norm(amp(K2,K1))**2)
expected=p**4*nu**8/(2*16**4)*(4*np.sin(s1/2)**2)*(4*np.sin(s2/2)**2)
assert abs(P-expected)<1e-20
assert (abs(amp(K2,K1))>1e-14).sum()==128
print('PASS all original 128x128 two-tick Kraus outcomes normalized, native p+ p^2=1, full exact bivector-area law')
print('PASS equal Fourier profiles produce ZERO 0->top; two distinct role phases yield 128 nonzero marked histories')
print('FIREWALL: coherent signed amplitudes are not determined by individual record probabilities.')
print('FIREWALL: physical single moving geometry selecting distinct tick profiles and full Book source remains OPEN.')
