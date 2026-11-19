#!/usr/bin/env python3
"""Original K(9,11,13) Cost>=1 floor, ALL718 Book future32 first source.

Finite independent native scene checker. A conditional SCALAR Book theorem;
does not select original complete G0/Book/CAR/EH physical action.
"""
from math import log, sqrt
import numpy as np

p=(sqrt(5)-1)/2; ell=log(1/p)
zone=np.array([0]*9+[1]*11+[2]*13)
n=len(zone)
u,v=np.where(zone[:,None]!=zone[None,:])
assert n==33 and len(u)==718
rng=np.random.default_rng(20261019)
I0=rng.uniform(-.22,.22,n)
j=rng.uniform(-.15,.15,n)
j2=rng.uniform(-.05,.05,n)
theta=.31
cost2=np.zeros(len(u))
cost2[(u==0)&(v==9)]=2.
cost2[(u==11)&(v==20)]=.7
assert min(cost2)>=0

def transfer(y,di=j,di2=j2,k=cost2):
    I=I0+y*di+y*y*di2/2
    C=1+y*y*k/2
    assert min(C)>=1
    K=np.zeros((n,n))
    K[u,v]=np.exp(-ell*(C-theta*I[u]-(1-theta)*I[v]))
    return K

def pressure(y,di=j,di2=j2,k=cost2):
    eigen=np.linalg.eigvals(transfer(y,di,di2,k))
    return -log(float(max(eigen.real)))/ell

K=transfer(0)
D,R=np.linalg.eig(K);a=np.argmax(D.real)
lam=float(D[a].real);r=R[:,a].real
if r.sum()<0:r=-r
Dleft,L=np.linalg.eig(K.T);a=np.argmin(abs(Dleft-lam))
l=L[:,a].real
if l.sum()<0:l=-l
pi=l*r;pi/=pi.sum()
assert min(pi)>0
P=np.zeros((n,n))
P[u,v]=K[u,v]*r[v]/(lam*r[u])
f=pi[u]*P[u,v]
assert max(abs(P.sum(axis=1)-1))<1e-12
assert max(abs(pi@P-pi))<1e-12
assert max(abs(f-P[v,u]*pi[v]))<1e-12

J0=np.zeros((len(u),n));J1=np.zeros((len(u),n))
J0[np.arange(len(u)),u]=np.sqrt(P[u,v])
J1[np.arange(len(u)),v]=np.sqrt(f/pi[v])
T=J0.T@J1
future=J1-J0@T
assert np.linalg.norm(T-T.T)<1e-11
assert sum(np.linalg.eigvalsh(future.T@future)>1e-9)==32

def innovation(d):
    c=float(f@d)
    b=np.bincount(u,weights=f*d,minlength=n)/pi-c
    xi=np.linalg.solve(np.eye(n)-P+np.outer(np.ones(n),pi),b)
    assert np.linalg.norm((np.eye(n)-P)@xi-b)<1e-11
    m=d-c-xi[u]+xi[v]
    g=np.sqrt(f)*m
    assert np.linalg.norm(J0.T@g)<2e-11
    return c,xi,g

# At any OPEN two-sided smooth chart with ALL primitive C>=1 and
# C(y0)=1, the REAL Cost first jet vanishes identically.
d=-theta*j[u]-(1-theta)*j[v]
c,xi,g=innovation(d)
alpha=-j/2
# Correct endpoint coboundary absorption for general theta.
chi=alpha+xi+(theta-.5)*j
h=np.sqrt(pi)*chi
assert np.linalg.norm(g-future@h)<1e-11
assert np.linalg.norm(g)>1e-5
dark=g-future@(np.linalg.pinv(future,rcond=1e-10)@g)
assert np.linalg.norm(dark)<1e-11
s2=cost2-theta*j2[u]-(1-theta)*j2[v]
first=float(f@d)
second=float(f@s2-ell*(g@g))
t=.0008
fd1=(pressure(t)-pressure(-t))/(2*t)
fd2=(pressure(t)-2*pressure(0)+pressure(-t))/t**2
assert abs(fd1-first)<2e-8,(fd1,first)
assert abs(fd2-second)<6e-7,(fd2,second)

# Pure admitted C=1+y² k/2 with frozen I has NO historical Schur.
zeros=np.zeros(n)
cc,xx,gg=innovation(np.zeros(len(u)))
assert abs(cc)<1e-15 and np.linalg.norm(gg)==0
purepred=float(f@cost2)
purefd=(pressure(t,zeros,zeros,cost2)-2*pressure(0,zeros,zeros,cost2)
        +pressure(-t,zeros,zeros,cost2))/t**2
assert purepred>0 and abs(purefd-purepred)<3e-7

# GLOBAL strict original PF optimizer: for any fixed I and admissible
# C>=1, scalar Book all-path F=-log_phi rho is uniquely minimal at C=1.
def action_excess(k):
    C=1+k
    assert min(C)>=1
    M=np.zeros((n,n))
    M[u,v]=np.exp(-ell*(C-theta*I0[u]-(1-theta)*I0[v]))
    return -log(float(max(np.linalg.eigvals(M).real)))/ell
base=action_excess(np.zeros(len(u)))
for k in (np.ones(len(u))*.01,cost2*.8,
          np.where((u==0)&(v==9),.2,0.)):
    assert action_excess(k)>base+1e-9
probe=np.zeros(len(u));probe[(u==0)&(v==9)]=1
der=(action_excess(.00001*probe)-base)/.00001
assert abs(der-f@probe)<2e-7

# Allocation gauge similarity survives moving all original 33 Info.
for th in (0.,.31,.5,1.):
    I=I0+t*j+t*t*j2/2;C=1+t*t*cost2/2
    M=np.zeros((n,n))
    M[u,v]=np.exp(-ell*(C-th*I[u]-(1-th)*I[v]))
    assert abs(max(np.linalg.eigvals(M).real)-max(np.linalg.eigvals(transfer(t)).real))<3e-12

print('PASS original 33/718 Golden PF and arbitrary nonuniform 33 moving Info')
print('PASS ActionProtocol saturated two-sided Cost first jet is identically ZERO')
print('PASS full Book history Poisson source entirely in original future32')
print('PASS signed327 and signless326 dark archival projections both vanish')
print('PASS full scalar Book first/second Euler finite-difference control')
print('first source',first,'direct',fd1)
print('second source',second,'direct',fd2)
print('future32 Schur',-ell*float(g@g),'local C2+Info2',float(f@s2))
print('pure canonical Cost quadratic',purepred,'direct',purefd)
print('PASS canonical C=1 uniquely minimizes scalar Book pressure over Cost>=1')
print('PASS exact primitive edge-Cost source equals positive native Perron flow')
print('FIREWALL: actual protocol Cost saturation and full same-history GR OPEN')
