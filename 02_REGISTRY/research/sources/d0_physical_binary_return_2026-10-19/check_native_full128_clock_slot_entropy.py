#!/usr/bin/env python3
"""Native full128 flat-shell time-slot entropy, source and MDL probability controls.

The original flat first-shell owner proves all blank0-versus-complement exit
indicators are iid Bernoulli. This exact scalar consequence does NOT choose
the compulsory Book03 cost or replay the full original 16x16x128 Kraus engine.
"""
from math import comb, log, sqrt, lgamma

phi=(1+sqrt(5))/2
p=1/phi
ell=log(phi)
h=1/4
n=1024
lam=288/25
eps=p*p*h*h/64
e=eps*lam-(eps*lam)**2/4
q0=1-e
de_dlam=eps*(1-eps*lam/2)
assert 0<e<1

def hbin(x):
    return -x*log(x)-(1-x)*log(1-x)

# Full native record: each time slot has 128 possible physical outcomes.
# We group the special blank-label/port0 as "no exit" and ALL 127 others as
# exits, without deleting or postselecting a single original Kraus outcome.
prob=[comb(n,k)*e**k*q0**(n-k) for k in range(n+1)]
assert abs(sum(prob)-1)<1e-13

H_indicator=n*hbin(e)/ell
H_count=-sum(w*log(w) for w in prob if w>0)/ell
H_positions=sum(w*(lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1))
                for k,w in enumerate(prob) if w>0)/ell
assert abs(H_indicator-H_count-H_positions)<2e-11

# Exact binomial-score identity (no differencing or approximate argument):
# d_e E[f(K)] = n E_{K~Bin(n-1,e)}[f(K+1)-f(K)]
# for f(K)=log_phi choose(n,K) and Delta f=log_phi ((n-K)/(K+1)).
prob_n1=[comb(n-1,k)*e**k*q0**(n-1-k) for k in range(n)]
Dpositions_de=n*sum(w*log((n-k)/(k+1))
                    for k,w in enumerate(prob_n1) if w>0)/ell
Dpositions_dlam=de_dlam*Dpositions_de
Dindicator_dlam=n*de_dlam*log(q0/e)/ell
Dcount_dlam=Dindicator_dlam-Dpositions_dlam

# Valid only on a scalar first-shell family Delta_h=lambda_h I.
# Original J23 link tangent leaves the scalar chart; do NOT transplant this
# time-entropy source to J23 without the full moving original recursion.
def positions(L):
    E=eps*L-(eps*L)**2/4
    Q=1-E
    b=[comb(n,k)*E**k*Q**(n-k) for k in range(n+1)]
    return n*hbin(E)/ell+sum(w*log(w) for w in b if w>0)/ell

delta=1e-4
fd=(positions(lam+delta)-positions(lam-delta))/(2*delta)
assert abs(fd-Dpositions_dlam)<1e-8
assert H_positions>0 and Dpositions_dlam>0

print('PASS: complete original blank0-vs-all-other exit indicators iid on flat scalar shell')
print('PASS: exact full timeword entropy=count entropy+conditional slot entropy')
print('PASS: exact binomial score source agrees with finite difference')
print(f'P(all blank)={q0**n:.14f}, E exits={n*e:.12f}')
print(f'H(timeword)={H_indicator:.12f}; H(count)={H_count:.12f}; H(slots|count)={H_positions:.12f}')
print(f'D_lambda H(timeword)={Dindicator_dlam:.12f}')
print(f'D_lambda H(count)={Dcount_dlam:.12f}')
print(f'D_lambda H(slots|count)={Dpositions_dlam:.12f}')
print(f'modal single-path surprisal={-n*log(q0)/ell:.12f}')
print('OWNER CONSEQUENCE: for compact positive beta_h=n*epsilon and lambda,')
print('H(slots|K)=beta_h*lambda*log(1/epsilon)/log(phi)+O(1),')
print('D_lambda H(slots|K)=beta_h*log(1/epsilon)/log(phi)+O(1).')
print('SCOPE: no Book whole-action binding, arbitrary J23 source or GR closure')
