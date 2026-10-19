#!/usr/bin/env python3
"""Original native K9,11,13 raw 2-/3-step Book clock ratio -> entire scalar action.

Finite independent all718 replay; same-clock original G0 selection is OPEN.
"""
import numpy as np
from math import sqrt,log
p=(sqrt(5)-1)/2;ell=log(1/p)
zone=np.array([0]*9+[1]*11+[2]*13)
u,v=np.where(zone[:,None]!=zone[None,:]);n=33
assert len(u)==718
rng=np.random.default_rng(19102026)
C=1.21+rng.uniform(.01,.26,len(u))
I=rng.normal(0,.23,n);theta=.4
s=C-theta*I[u]-(1-theta)*I[v]
def read(s):
 K=np.zeros((n,n));K[u,v]=np.exp(-ell*s)
 eig,R=np.linalg.eig(K);j=np.argmax(eig.real);lam=float(eig[j].real)
 right=R[:,j].real
 if right.sum()<0:right=-right
 ev,L=np.linalg.eig(K.T);j=np.argmin(abs(ev-lam));left=L[:,j].real
 if left.sum()<0:left=-left
 pi=left*right;pi/=pi.sum()
 P=np.zeros((n,n));P[u,v]=K[u,v]*right[v]/(lam*right[u])
 mu=pi[u]*P[u,v]
 assert abs(mu.sum()-1)<1e-12
 Z2=np.trace(K@K);Z3=np.trace(K@K@K)
 T2=np.trace(P@P);T3=np.trace(P@P@P)
 assert min(Z2,Z3,T2,T3)>0
 assert abs(Z2-lam**2*T2)<1e-10
 assert abs(Z3-lam**3*T3)<1e-9
 reconstructed=(Z3/Z2)*(T2/T3)
 assert abs(reconstructed-lam)<2e-11
 return lam,P,mu,(Z2,Z3,T2,T3),reconstructed
lam,P,mu,(Z2,Z3,T2,T3),rec=read(s)
# Independently SUM the actual original 2-tick backtracks and 3-tick
# closed triangles, with directed asymmetric original primitive prices.
K=np.zeros((n,n));K[u,v]=np.exp(-ell*s)
literal2=sum(K[a,b]*K[b,a] for a,b in zip(u,v))
literal3=0.
for a in range(n):
 for b in range(n):
  if zone[a]==zone[b]:continue
  for c in range(n):
   if zone[c] in (zone[a],zone[b]):continue
   literal3+=K[a,b]*K[b,c]*K[c,a]
assert abs(literal2-Z2)<1e-10 and abs(literal3-Z3)<1e-9
# Mathematical positive two-depth mixture with DECLARED, known
# attempt coefficients: NOT asserted a compulsory Golden physical clock.
a2,a3=.37,.63
clock3=a3*Z3/(a2*Z2+a3*Z3);clock2=1-clock3
from_clock=(clock3/clock2)*(a2/a3)*(T2/T3)
assert abs(from_clock-lam)<1e-12
# ALL16 primitive Golden-p complete GOOD/BAD original-type records
# may be marginalized from one joint mathematical native history law.
q=np.array([p**4/24]*12+[p**4/2,p**3,p**3,p**2])
assert len(q)==16 and abs(q.sum()-1)<2e-14
Q=mu[:,None]*q
assert Q.shape==(718,16) and abs(Q.sum()-1)<1e-12
assert max(abs(Q.sum(axis=1)-mu))<1e-15
# Arbitrary moving Cost and moving original Info: first source is the
# derivative of one TRUE original scalar Book absolute clock ratio.
dC=rng.normal(0,.13,len(u));dI=rng.normal(0,.10,n)
h=1e-5
def measure(t):
 Ct=C+t*dC;It=I+t*dI
 assert min(Ct)>1
 la,Pt,mut,(z2,z3,t2,t3),_=read(Ct-theta*It[u]-(1-theta)*It[v])
 return np.array([log(la),log(z3/z2)+log(t2/t3)])
a=measure(h);b=measure(-h)
sources=(a-b)/(2*h)
assert abs(sources[0]-sources[1])<2e-9
# EXACT normalized-depth blind mode: a common primitive scalar price
# shift changes clock odds but not the stationary native edge law.
t=.031
lamt,Pt,mut,(z2t,z3t,t2t,t3t),_=read(s+t)
assert max(abs(mut-mu))<2e-12
assert np.max(abs(Pt-P))<2e-12
assert abs(lamt/lam-np.exp(-ell*t))<1e-12
assert abs((z3t/z2t)/(Z3/Z2)-np.exp(-ell*t))<1e-12
print('PASS original all718 arbitrary directed native Book Cost/Info')
print('PASS literal original two-edge backtracks + three-edge ABC triangles')
print('PASS Tr K^n=lambda^n Tr P^n and global lambda=Z3/Z2 * TrP2/TrP3')
print('PASS positive jointly normalized native 2/3 clock ratios recover lambda')
print('PASS original full Golden16 Good/Bad flags marginalize to complete edge law')
print('PASS exact original absolute Book first field source from same 2/3 history odds')
print('PASS separate-depth normalized histories fail to see uniform Cost quantum')
print('lambda',lam,'absolute Book action',-log(lam)/ell)
print('D log(lambda) from original vs clock',sources.tolist())
print('FIREWALL physical Golden fullStep/Book HJR clock admission and Einstein OPEN')
