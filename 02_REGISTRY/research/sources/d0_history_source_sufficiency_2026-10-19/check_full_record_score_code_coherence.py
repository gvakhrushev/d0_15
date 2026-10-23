#!/usr/bin/env python3
"""Native p Golden original full128 port-code signature: score != code != quantum.
EXACT finite chain-source theorem consumer; *not* selected Book action or GR.
"""
from math import sqrt, log
import numpy as np

p=(sqrt(5)-1)/2
ell=log(1/p)
assert abs(p+p*p-1)<1e-15
assert abs(p-p*p-p**3)<1e-15

# Genuine original native GOLDEN nonblank port CONDITIONALS.
port_q=np.array([p*p,p])
port_code=np.array([p,p*p])
hidden_one=sum(a*log(a/b)/ell for a,b in zip(port_q,port_code))
assert abs(hidden_one-p**3)<1e-14
print('PASS original full128 Golden nonblank port KL exact p^3 =',hidden_one)

# Finite full-history illustrative label fixture consumes ACTUAL port q/mu.
# The nonblank label A/B prevalence is an inert, declared test marginal,
# not a fabricated native full128 empirical likelihood.
alpha=.3
ref_nonblank=.32
e_base=.42
e_slope=.17
def pair(y):
    e=e_base+e_slope*y
    q=np.array([1-e,e*alpha*p*p,e*alpha*p,e*(1-alpha)*p*p,e*(1-alpha)*p])
    mu=np.array([1-ref_nonblank, ref_nonblank*alpha*p,
                 ref_nonblank*alpha*p*p,ref_nonblank*(1-alpha)*p,
                 ref_nonblank*(1-alpha)*p*p])
    return q,mu

def KL(q,mu):
    return float(sum(x*log(x/y) for x,y in zip(q,mu))/ell)

def group(q,mu,indices):
    return np.bincount(indices,weights=q),np.bincount(indices,weights=mu)
blank_vs_exit=np.array([0,1,1,1,1],dtype=int)
blank_vs_port=np.array([0,1,2,1,2],dtype=int)
for y in [-.2,0,.2]:
    q,mu=pair(y)
    Q,M=group(q,mu,blank_vs_exit)
    Qp,Mp=group(q,mu,blank_vs_port)
    extra=KL(q,mu)-KL(Q,M)
    assert abs(extra-(e_base+e_slope*y)*p**3)<3e-14
    assert abs(KL(q,mu)-KL(Qp,Mp))<3e-14
print('PASS exact Golden nonblank source gap E(y)*p^3 and port-retaining repair')

de=e_slope
# The nonblank labels have fixed conditional proportions c_i. Evaluate both
# Fisher norms from the complete probability vectors and their exact
# analytic tangent instead of subtracting nearby finite-difference values.
q,mu=pair(0.)
dq=de*np.array([-1.,alpha*p*p,alpha*p,(1-alpha)*p*p,(1-alpha)*p])
Q,M=group(q,mu,blank_vs_exit)
dQ,_=group(dq,np.zeros_like(dq),blank_vs_exit)
Ifull=float(sum(dq*dq/q))
Icoarse=float(sum(dQ*dQ/Q))
assert abs(Ifull-Icoarse)<3e-15

# The moving Bernoulli term cancels in the KL derivative; the remaining
# exact source is de times the actual Golden conditional port KL. alpha and
# ref_nonblank remain illustrative marginals, not native full128 evidence.
source_full=float(sum(dq*(np.log(q/mu)+1.))/ell)
source_coarse=float(sum(dQ*(np.log(Q/M)+1.))/ell)
assert abs(source_full-source_coarse-de*p**3)<1e-14
print('PASS all classical field Fisher unchanged by blank-vs-exit forgetting')
print('PASS true CLASSICAL code source still lost:',source_full-source_coarse)

# Independent quantum memory (illustrative mathematical hostile control):
# classical pointer probabilities are constant even as coherent source moves.
prior=np.array([.4,.6])
pointer=np.array([.65,.35])
def quantumKL(t):
    rho=np.array([[.65,t],[t,.35]])
    eig=np.linalg.eigvalsh(rho)
    assert min(eig)>0
    return (sum(x*log(x) for x in eig)-sum(pointer*np.log(prior)))/ell
base=KL(pointer,prior)
t=.08
coherent_price=quantumKL(t)-base
disc=sqrt(.09+4*t*t)
lam_plus=(1+disc)/2
lam_minus=(1-disc)/2
coh_source=(2*t/disc)*log(lam_plus/lam_minus)/ell
assert abs(coherent_price-.027572064175238)<2e-12
assert abs(coh_source-.692550638440915)<2e-12
print('PASS pointer classical source exactly zero while coherent quantum source is',coh_source)
print('PASS hidden coherent Cost-Info at same pointer q:',coherent_price)
print('NOTE: 2x2 coherence example is mathematical; actual native full128 coherent data remain separately owned')
print('NOTE: full Book action must be PHYSICALLY selected before applying this source criterion to GR')
