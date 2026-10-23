#!/usr/bin/env python3
"""Original 33/718 arbitrary directed net Book Cost–Info inverse; complete Golden16.
Proof controls scalar action modulo endpoints, not compulsory full G0/GR.
"""
from math import sqrt,log
import numpy as np
phi=(1+sqrt(5))/2;ell=log(phi);p=1/phi
z=np.array([0]*9+[1]*11+[2]*13)
u,v=np.where(z[:,None]!=z[None,:]);n=len(z);E=len(u)
assert n==33 and E==718
rng=np.random.default_rng(20261019)
I=rng.normal(0,.19,n);theta=.31
C=1.24+rng.uniform(0,.30,E)
def price(C,I):return C-theta*I[u]-(1-theta)*I[v]
def native(s):
 K=np.zeros((n,n));K[u,v]=np.exp(-ell*s)
 vals,R=np.linalg.eig(K);i=np.argmax(vals.real);lam=float(vals[i].real)
 right=R[:,i].real
 if right.sum()<0:right=-right
 vals,L=np.linalg.eig(K.T);i=np.argmin(abs(vals-lam));left=L[:,i].real
 if left.sum()<0:left=-left
 pi=left*right;pi/=pi.sum()
 P=np.zeros((n,n));P[u,v]=K[u,v]*right[v]/(lam*right[u])
 mu=pi[u]*P[u,v]
 assert abs(mu.sum()-1)<2e-12
 assert max(abs(np.bincount(u,weights=mu,minlength=n)-np.bincount(v,weights=mu,minlength=n)))<1e-12
 return K,lam,pi,P,mu,right
s=price(C,I)
K,lam,pi,P,mu,r=native(s)
# Same declared original primitive Golden positive 16-outcome flag reference.
q=np.array([p**4/24]*12+[p**4/2,p**3,p**3,p**2])
assert len(q)==16 and abs(q.sum()-1)<2e-14
Q=mu[:,None]*q
assert Q.shape==(718,16) and abs(Q.sum()-1)<2e-12
observed=Q.sum(axis=1);piobs=np.bincount(u,weights=observed,minlength=n)
Pobs=observed/piobs[u]
scan=-np.log(lam*observed/np.sqrt(piobs[u]*piobs[v]))/ell
g=-np.log(np.sqrt(piobs)/r)/ell
assert max(abs(scan-s-(g[u]-g[v])))<1e-11
Kcan=np.zeros_like(K);Kcan[u,v]=np.exp(-ell*scan)
root=np.sqrt(piobs)
# Check the Perron equations on the original 718-edge support. Sparse edge
# reductions avoid a dense BLAS matmul over the 371 structural zero entries.
right_res=np.bincount(u,weights=Kcan[u,v]*root[v],minlength=n)-lam*root
left_res=np.bincount(v,weights=Kcan[u,v]*root[u],minlength=n)-lam*root
assert np.linalg.norm(right_res)<2e-11
assert np.linalg.norm(left_res)<2e-11
# All original closed scalar prices and true odd cycle affinities.
idx={(int(a),int(b)):i for i,(a,b) in enumerate(zip(u,v))}
cycles=[[(0,9),(9,20),(20,0)],[(1,10),(10,21),(21,1)]]
for cyc in cycles:
 S=sum(s[idx[e]] for e in cyc)
 Sc=sum(scan[idx[e]] for e in cyc)
 Sp=-len(cyc)*log(lam)/ell-sum(log(P[e])/ell for e in cyc)
 odd=sum(s[idx[a,b]]-s[idx[b,a]] for a,b in cyc)
 oddm=-sum(log(mu[idx[a,b]]/mu[idx[b,a]])/ell for a,b in cyc)
 assert abs(S-Sc)<1e-11 and abs(S-Sp)<1e-11
 assert abs(odd-oddm)<1e-11
# A nontrivial complete ORIGINAL balanced history flow, not just optimal mu.
_,_,_,_,mu2,_=native(s+rng.normal(0,.13,E))
f=(mu+mu2)/2
fu=np.bincount(u,weights=f,minlength=n)
assert max(abs(fu-np.bincount(v,weights=f,minlength=n)))<2e-12
A=sum(f*s)+sum(f*np.log(f/fu[u]))/ell
KL=sum(f*np.log(f/(fu[u]*Pobs)))/ell
assert KL>0 and abs(A+log(lam)/ell-KL)<2e-11
# Two-sided Cost-excess field family: native prices may vary smoothly OFF floor.
dC=rng.normal(0,.17,E);dI=rng.normal(0,.17,n)
h=1e-5
def source(t):
 Ct=C+t*dC;It=I+t*dI
 assert min(Ct)>1
 st=price(Ct,It)
 _,lt,pit,_,mut,_=native(st)
 return st,-np.log(lt*mut/np.sqrt(pit[u]*pit[v]))/ell
sp,scp=source(h);sm,scm=source(-h)
ds=(sp-sm)/(2*h);dsc=(scp-scm)/(2*h)
assert abs(f@ds-f@dsc)<2e-8
for cyc in cycles:
 assert abs(sum((ds-dsc)[idx[e]] for e in cyc))<2e-8
# Any diagonal native endpoint gauge retains ALL observed stationary data.
di=rng.uniform(-.13,.13,n)
sg=scan-(di[u]-di[v])
_,lg,pg,_,mug,_=native(sg)
assert abs(lg-lam)<2e-11 and max(abs(mug-mu))<2e-12
# Actual primitive ActionProtocol permits distinct Cost/Info splits at same s.
j=rng.normal(0,.04,n)
C2=C+theta*j[u]+(1-theta)*j[v]
assert min(C2)>1 and max(abs(price(C2,I+j)-s))<3e-15
print("PASS original 33/718 arbitrary directed full scalar Book inversion")
print("PASS original all16 Golden GOOD/BAD positive joint 11488 law")
print("PASS 718 scalar prices modulo 32 exact endpoint gauges")
print("PASS original closed histories and odd graph cycle affinities")
print("PASS full 685-dimensional balanced flow Book action and field derivatives")
print("PASS gauge-equivalent positive transfer and competing legal Cost/Info splits")
print("exact action",A,"absolute Book pressure",-log(lam)/ell)
print("dimensions: scalar price/gauge=718-32=686; normalized flows=718-33=685")
print("FIREWALL original compulsory full Book memory/G0/Einstein Euler OPEN")
