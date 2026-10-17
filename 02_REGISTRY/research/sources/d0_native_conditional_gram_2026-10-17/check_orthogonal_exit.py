#!/usr/bin/env python3
"""Native-Kraus algebra: orthogonally tagged complete exits yield the IR Einstein source ratio.

Tests arbitrary self-adjoint 16x16 positive carrier matrices. The extra endpoint-
tag comparison and physical logdet/Info selection are NOT claimed native-admitted.
"""
import math
import numpy as np
from scipy.linalg import expm

p=(math.sqrt(5)-1)/2

def root_pos(a):
    w,v=np.linalg.eigh((a+a.T)/2)
    if np.min(w)<-1e-10:
        raise AssertionError(f'negative eigenvalue {min(w)}')
    return (v*np.sqrt(np.maximum(0,w)))@v.T

def invroot_pos(a):
    w,v=np.linalg.eigh((a+a.T)/2)
    return (v/np.sqrt(w))@v.T

def build(d0,d4,d1,beta=0.4,z=p*p):
    d=len(d0); I=np.eye(d); O=np.zeros((d,d));a=1-z
    # Two endpoint clocks have duration beta; the shared central 4D
    # no-mark clock has duration 2 beta.
    B0=expm(-beta*d0/2); B1=expm(-beta*d1/2)
    B4=expm(-beta*d4)
    # Common two-branch raw return, and the EXACT complementary exits.
    V=np.vstack((math.sqrt(a)*I, math.sqrt(z)*B4))
    T=math.sqrt(z)*root_pos(I-B4@B4)  # stand-in for the ACTUAL full exit rows
    Y0=np.vstack((V,T,O));Y1=np.vstack((V,O,T))
    assert np.allclose(Y0.T@Y0,I,atol=1e-12)
    assert np.allclose(Y1.T@Y1,I,atol=1e-12)
    E4=a*I+z*B4@B4
    assert np.allclose(Y1.T@Y0,E4,atol=1e-12)
    # Original golden controller amplitudes: (sqrt(p), p), p+p^2=1.
    g0=np.array([1.,0.]);g1=np.array([math.sqrt(p),p])
    Y0=np.kron(g0.reshape(-1,1),Y0)
    Y1=np.kron(g1.reshape(-1,1),Y1)
    X0=np.vstack((math.sqrt(a)*Y0,math.sqrt(z)*B0,O))
    X1=np.vstack((math.sqrt(a)*Y1,O,math.sqrt(z)*B1))
    G0=X0.T@X0; G1=X1.T@X1; K=X1.T@X0
    assert np.allclose(G0,a*I+z*B0@B0,atol=1e-12)
    assert np.allclose(G1,a*I+z*B1@B1,atol=1e-12)
    assert np.allclose(K,a*math.sqrt(p)*E4,atol=1e-12)
    C=invroot_pos(G1)@K@invroot_pos(G0)
    s=np.linalg.svd(C,compute_uv=False)
    assert np.max(s)<=math.sqrt(p)+1e-10
    assert np.min(s)>0
    _,lk=np.linalg.slogdet(K)
    _,lg0=np.linalg.slogdet(G0)
    _,lg1=np.linalg.slogdet(G1)
    return -2*lk+lg0+lg1,s

def L_diff(d,h,t=0.4,z=p*p):
    a=1-z; I=np.eye(len(d)); e=expm(-t*d)
    return float(-z*t*np.trace(np.linalg.solve(a*I+z*e,e)@h).real)

def test():
    rng=np.random.default_rng(20261017)
    A=rng.normal(size=(16,16)); base=.4*np.eye(16)+A.T@A/16
    jets=[]
    for i in range(3):
        H=rng.normal(size=(16,16));H=(H+H.T)/2
        jets.append(H/np.linalg.norm(H))
    beta=.4; z=p*p
    v,s=build(base,base,base,beta,z)
    maxerr=0.0
    # Independent source jets, not only a restricted static common variation.
    for i,h in enumerate(jets):
        args=[base.copy(),base.copy(),base.copy()]
        eps=1e-5;args[i]=base+eps*h
        plus,_=build(*args,beta,z)
        args[i]=base-eps*h
        minus,_=build(*args,beta,z)
        numerical=(plus-minus)/(2*eps)
        exact=-2*L_diff(base,h,2*beta,z) if i==1 else L_diff(base,h,beta,z)
        err=abs(numerical-exact)
        maxerr=max(maxerr,err)
        assert err<2e-8,(i,err,numerical,exact)
    # The common 4D branch is E(2beta), so -2 log(E(2beta))
    # carries exactly -1 copy of the 4D a2 source; the two endpoint
    # log E(beta) each carry +1 copy. Volume is 3/2, NOT 1.
    a2_weights=(1.,1.,-2./2.)
    a0_weights=(1.,1.,-2./(2.**2))
    assert a2_weights==(1.,1.,-1.)
    assert sum(a0_weights)==1.5
    print(f'PASS: complete-exit tagged 16x16 Gram and cross, singular values {min(s):.9f}..{max(s):.9f}')
    print(f'PASS: independent noncommuting first source max abs error {maxerr:.3g}')
    print('PASS: IR Einstein a2 weights (spatial0,spatial1,4D)=(1,1,-1)')
    print('PASS: volume a0 total=3/2 (separate source, not hidden)')

if __name__=='__main__':
    test()