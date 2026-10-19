#!/usr/bin/env python3
"""Exact algebra + finite controls: pointer/binary/full coherent native price.

NOT a physical admission, Book selector or original 128-channel replay.
"""
import math

phi=(1+math.sqrt(5))/2
p=1/phi
ell=math.log(phi)

# Two independent native Golden letters, costs 1 and 2, full 4 histories.
# All outcomes retained. Original reference code mu is a normalized Kraft law.
C=(2,3,3,4)
mu=[p**cost for cost in C]
assert abs(sum(mu)-1)<1e-14
q=[.1,.2,.3,.4]
partition=((0,1),(2,3))

def kl(q,mu):
    return sum(x*math.log(x/y)/ell for x,y in zip(q,mu))

qcoarse=[sum(q[i] for i in block) for block in partition]
mucoarse=[sum(mu[i] for i in block) for block in partition]
chain=kl(qcoarse,mucoarse)
for block,weight,refweight in zip(partition,qcoarse,mucoarse):
    chain+=weight*kl([q[i]/weight for i in block],[mu[i]/refweight for i in block])
assert abs(kl(q,mu)-chain)<1e-14

# Purely internal reallocation at fixed measured GOOD/BAD probabilities.
def internal(t):
    x=q.copy();x[0]+=t;x[1]-=t
    return kl(x,mu)
eps=1e-6
source=(internal(eps)-internal(-eps))/(2*eps)
expected=math.log(q[0]*mu[1]/(q[1]*mu[0]))/ell
assert abs(source-expected)<1e-9
assert abs(source)>1e-3
assert all(abs(sum((q[0]+t,q[1]-t))-qcoarse[0])<1e-14 for t in [-eps,eps])

# Two-outcome coherent retained-record state with unchanged Born outcomes.
# lambda±=(1±sqrt((2g−1)^2+4c^2))/2.
g=3/4
prior=(p,p*p)
assert abs(sum(prior)-1)<1e-14

def snat(c):
    r=math.sqrt((2*g-1)**2+4*c*c)
    eigen=((1+r)/2,(1-r)/2)
    return -sum(v*math.log(v) for v in eigen)

def quantum_relative_entropy(c):
    return (-snat(c)-g*math.log(prior[0])-(1-g)*math.log(prior[1]))/ell

def classical_relative_entropy():
    return kl([g,1-g],prior)

for c in [0.,1/16,1/8,3/16]:
    gap=(-g*math.log(g)-(1-g)*math.log(1-g)-snat(c))/ell
    assert abs(quantum_relative_entropy(c)-classical_relative_entropy()-gap)<1e-13
    assert gap>=-1e-13
c=1/8
num=(quantum_relative_entropy(c+eps)-quantum_relative_entropy(c-eps))/(2*eps)
r=math.sqrt((2*g-1)**2+4*c*c)
analytic=(2*c/r)*math.log((1+r)/(1-r))/ell
assert abs(num-analytic)<1e-9
assert analytic>0

# The actual full128 first-shell upstream C1 owner proves the asymptotic
# source. This toy test does NOT simulate that original operator/channel.
print('PASS: 4 native Golden-history code weights sum to 1')
print('PASS: full classical KL = coarse binary KL + conditional fine KL')
print(f'PASS: binary statistics fixed, internal classical price source={source:.12f}')
print('PASS: coherent operator KL = full classical KL + relative coherence')
print(f'PASS: binary probabilities fixed, coherent price source={analytic:.12f}')
print('PASS: coherent correction positive and first source nonzero')
print('OWNER CONSEQUENCE: actual flat-shell (H_ptr−S_coh)/ln(phi) has ln(1/eps) leading C1 source')
print('STATUS: actual channel replay, physically compulsory Info and GR remain open')
