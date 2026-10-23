#!/usr/bin/env python3
"""Original scalar Book 33/718 Perron + complete primitive Golden p 16 flags.

Exact normalized joint experiment has Fisher rank38 and misses the original
absolute scalar pressure uniform-Info first source. This is a CONDITIONAL
joint mathematical apparatus, not compulsory native G0 execution or GR.
"""
import numpy as np
from math import sqrt,log

p=(sqrt(5)-1)/2;ell=log(1/p)
part=np.array([0]*9+[1]*11+[2]*13)
n=len(part)
u,v=np.where(part[:,None]!=part[None,:]);E=len(u)
assert (n,E)==(33,718)
rng=np.random.default_rng(1157)
I=rng.uniform(-.2,.2,n)

def scene(profile):
    K=np.zeros((n,n))
    K[u,v]=p*np.exp(ell/2*(profile[u]+profile[v]))
    eigen,vecs=np.linalg.eigh(K)
    lam=float(eigen[-1]);r=vecs[:,-1]
    if sum(r)<0:r=-r
    assert abs(r@r-1)<1e-13
    pi=r*r
    mu=K[u,v]*r[u]*r[v]/lam
    assert abs(mu.sum()-1)<1e-12
    assert max(abs(np.bincount(u,weights=mu,minlength=n)-pi))<1e-12
    return lam,K,r,pi,mu

lam,K,r,pi,mu=scene(I)
q=np.array([p**4/24]*12+[p**4/2,p**3,p**3,p**2])
assert len(q)==16 and abs(q.sum()-1)<1e-14 and min(q)>0
joint=np.outer(mu,q)
assert joint.shape==(718,16) and abs(joint.sum()-1)<1e-12

# Every edge and every complete flag is blind to uniform vertex Info shift,
# while the original absolute Perron Book action varies EXACTLY by -t.
for t in (-.33,-.1,.07,.23):
    lamt,Kt,rt,pit,mut=scene(I+np.ones(n)*t)
    qt=np.outer(mut,q)
    assert max(abs(qt.flatten()-joint.flatten()))<2e-14
    assert abs(-log(lamt)/ell-(-log(lam)/ell-t))<1e-12
assert abs(sum(-pi)+1)<1e-12

# Full 718-edge stationary source from eigenvector differentiation.
# d(log lambda)/dI_i=ell*pi_i, hence d(-log_phi lambda)/dI_i=-pi_i.
Q=np.eye(n)*lam-K+np.outer(r,r)
D=np.zeros((E,n))
for i in range(n):
    j=np.zeros(n);j[i]=1
    dK=np.zeros((n,n))
    dK[u,v]=ell/2*K[u,v]*(j[u]+j[v])
    dlam=ell*lam*pi[i]
    dr=np.linalg.solve(Q,(dK-dlam*np.eye(n))@r)
    assert abs(r@dr)<2e-12
    D[:,i]=(ell/2)*(j[u]+j[v])+dr[u]/r[u]+dr[v]/r[v]-dlam/lam
assert max(abs(D@np.ones(n)))<1e-10
FI=(D.T*mu)@D
eig=np.linalg.eigvalsh(FI)
assert abs(eig[0])<1e-12 and eig[1]>1e-5
assert sum(eig>1e-9)==32

# Original Golden p two-fresh GOOD/BAD 16-outcome CAR Choi mark at U=I;
# all six Lie generators have two labelled +/- positive mark probabilities.
Dq=np.zeros((16,6))
for i in range(6):
    Dq[2*i,i]=p**4/(12*sqrt(2))
    Dq[2*i+1,i]=-p**4/(12*sqrt(2))
assert max(abs(Dq.sum(axis=0)))<1e-14
Fcar=(Dq.T/q)@Dq
assert max(abs(Fcar-(p**4/6)*np.eye(6)).flatten())<1e-14

# One complete joint 718x16 physical-type law, without success selection.
SI=np.repeat(D,16,axis=0)
SX=np.tile(Dq/q[:,None],(E,1))
weights=joint.reshape(-1)
scores=np.concatenate((SI,SX),axis=1)
Fjoint=(scores.T*weights)@scores
assert max(abs(Fjoint[:n,n:]).flatten())<5e-14
assert max(abs(Fjoint[:n,:n]-FI).flatten())<5e-13
assert max(abs(Fjoint[n:,n:]-Fcar).flatten())<5e-13
eall=np.linalg.eigvalsh(Fjoint)
assert sum(eall>1e-9)==38 and abs(eall[0])<1e-12

# Independent finite scalar absolute gradient checks.
h=.0001
for i in (0,11,30):
    d=np.zeros(n);d[i]=1
    lp=scene(I+h*d)[0];lm=scene(I-h*d)[0]
    fd=(-log(lp)/ell+log(lm)/ell)/(2*h)
    assert abs(fd+pi[i])<1e-8
print('PASS exact original positive 718x16 complete joint probability law')
print('PASS whole record blind to uniform vertex Info; scalar absolute Book shifts -t')
print('PASS exact native original absolute Book first source = -pi, sum=-1')
print('PASS original 718 edge Info Fisher rank32 and only one constant Info kernel')
print('PASS all 16 Golden GOOD/BAD marks normalized and six CAR Fisher=p^4/6 I6')
print('PASS joint normalized Fisher 33+6 has one null, total positive rank38')
print('minimum nonzero history Fisher',eig[1], 'CAR value',p**4/6)
print('FIREWALL native full G0 admission and full HJR Einstein action OPEN')
