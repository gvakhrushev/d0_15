#!/usr/bin/env python3
"""All 8440 original Book loops x 17 complete Golden Bell outcomes:
exact conditional-clock gauge invisibility to primitive absolute Book Hessian.
Mathematical source COUNTERMODEL, not a physically admitted G0 programme.
"""
import math
import numpy as np
p=(math.sqrt(5)-1)/2
ell=math.log(1/p)
zone=[0]*9+[1]*11+[2]*13
loops=[]
for u in range(33):
    for v in range(33):
        if zone[u]==zone[v]:continue
        loops.append((u,v,u))
        for w in range(33):
            if zone[w] in (zone[u],zone[v]):continue
            loops.append((u,v,w,u))
assert len(loops)==8440
length=np.array([len(gamma)-1 for gamma in loops])
assert sum(length==2)==718 and sum(length==3)==7722
rng=np.random.default_rng(192026)
C=1.21+rng.uniform(.02,.27,(33,33))
I=rng.normal(0,.12,33)
K=np.zeros((33,33))
for u in range(33):
 for v in range(33):
  if zone[u]!=zone[v]:K[u,v]=p**(C[u,v]-.37*I[u]-.63*I[v])
base=np.array([np.prod([K[a,b] for a,b in zip(gamma,gamma[1:])]) for gamma in loops])
assert min(base)>0
attempt=np.where(length==2,p,p*p)
ref=attempt*base
q=ref/ref.sum()
assert abs(q.sum()-1)<1e-12
# TRUE primitive Golden-p 16 full marked/GOOD/BAD unconditional fractions,
# plus the ORIGINAL 64D Bell processor FAILURE (not postselected).
qcar=np.r_[np.repeat(p**4/24,12),p**4/2,p**3,p**3,p**2]/4096
qcar=np.r_[qcar,1-1/4096]
assert len(qcar)==17 and abs(qcar.sum()-1)<1e-12
Q=np.outer(q,qcar)
assert Q.shape==(8440,17) and abs(Q.sum()-1)<1e-12

def compute(t):
 c=p**(t*t)
 newprior2=p*c**-2
 newprior3=p*p*c**-3
 Zprior=newprior2+newprior3
 prior=np.where(length==2,newprior2/Zprior,newprior3/Zprior)
 different=prior*(c**length)*base
 out=different/different.sum()
 # Literal original Golden p,p^2 blank clock FIXED in BOTH experiments.
 # Only the separate CONDITIONAL depth-preparation acceptance changes.
 B=p*p
 success0=np.where(length==2,p,p*p)*B*base
 success1=np.where(length==2,p,p*p)*B*(c**(-length))*(c**length)*base
 assert np.max(abs(success0-success1))<1e-15
 assert B*c**-3<=1 and B*c**-2<=1
 reject0=np.array([p*(1-B),p*p*(1-B)])
 reject1=np.array([p*(1-B*c**-2),p*p*(1-B*c**-3)])
 return out,prior,reject0,reject1

for t in (0,.05,.1,.2):
 qnew,prior,reject0,reject1=compute(t)
 assert max(abs(qnew-q))<1e-16
 assert max(abs(np.outer(qnew,qcar)-Q).flatten())<1e-16
 assert abs(prior[0]+prior[-1]-1)<1e-14
 if t:assert np.max(np.abs(reject0-reject1))>0
 print('PASS t',t,'all8440 & all143480 invariant; clock priors',
       prior[0],prior[-1],'rejected-depth differences',reject1-reject0)
# Original native ABSOLUTE Book pressure is NOT gauge invariant.
root=max(np.linalg.eigvals(K).real)
for t in (0,.05,.1,.2):
 altroot=max(np.linalg.eigvals(p**(t*t)*K).real)
 assert abs((-math.log(altroot)/ell)-(-math.log(root)/ell+t*t))<1e-12
print('PASS whole accepted-tape source jets identical, absolute Book Hessian differs +2')
# From the tape only lambda*(effective alpha3/alpha2) is observed.
for t in (0,.05,.1,.2):
 c=p**(t*t)
 ratio=(p*p*c**-3)/(p*c**-2)
 assert abs(root*p-(root*c)*ratio)<1e-12
print('PASS native 2/3-clock ratio gauge leaves lambda*(alpha3/alpha2) invariant')
print('FIREWALL: conditional acceptance physical G0/oldRIGHT/Kraft admission is OPEN')


# STRONGER fully normalized positive finite instrument:
# ALL original path success × FULL Bell17, plus one TERMINAL fail for
# EACH actual 2/3 depth. EARLY clock and LATE path failures are coarsened
# together, so original primitive Book Hessian remains unidentified.
kappa=p**20
Z=np.array([base[length==k].sum() for k in (2,3)])
assert max(kappa*Z)<1
B=p*p
blank=np.array([p,p*p])
for t in (0,.05,.1,.2):
 c=p**(t*t)
 beta0=np.array([B,B]);beta1=np.array([B*c**-2,B*c**-3])
 assert max(beta1)<1
 success0=attempt*B*kappa*base
 success1=attempt*np.where(length==2,beta1[0],beta1[1])*kappa*(c**length)*base
 assert max(abs(success0-success1))<1e-16
 failures0=blank*(1-beta0*kappa*Z)
 failures1=blank*(1-beta1*kappa*(Z*(c**np.array([2,3]))))
 qfull0=np.r_[np.outer(success0,qcar).ravel(),failures0]
 qfull1=np.r_[np.outer(success1,qcar).ravel(),failures1]
 assert len(qfull0)==143482 and abs(qfull0.sum()-1)<2e-14
 assert min(qfull0)>0
 assert max(abs(qfull0-qfull1))<1e-16
 # The EARLY rejection STAGE carries the missing physical source.
 early0=blank*(1-beta0);early1=blank*(1-beta1)
 if t:assert max(abs(early0-early1))>1e-6
 print('PASS full 143482 including BOTH depth-labelled TERMINAL failures',
       t,'max',max(abs(qfull0-qfull1)),
       'DIFFERENT original EARLY-stage reject',early1-early0)
