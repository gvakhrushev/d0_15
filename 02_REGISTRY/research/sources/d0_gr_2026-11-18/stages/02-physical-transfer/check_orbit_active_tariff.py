"""Exact permutation and active SourceI ledger, with both orientation choices."""
from itertools import product
from collections import Counter
from fractions import Fraction
from sympy import symbols, factor
states=[(bus,sp,d,b,sgn) for bus,sp,d,b,sgn in product(range(2),repeat=5) if bus or d or b]
def cx(i,j):return ('CX',i,j)
def swap(i,j):return [cx(i,j),cx(j,i),cx(i,j)]
source=('SourceI',)
def route(i,count):return swap(0,i)+[source]*count+swap(0,i)
cz=route(3,1)+route(2,1)+[cx(3,2)]+route(2,3)+[cx(3,2)]
wp=cz+[cx(3,2)]; wm=[cx(3,2)]+cz
def step(x,g):
    v=list(x)
    if g==source:
        v[4]^=v[0]*v[1]
        v[1]^=v[0]
    else:
        v[g[2]]^=v[g[1]]
    return tuple(v)
def histogram(w):
    out=[]
    for initial in states:
        x=initial;active=0
        for gate in w:
            active+=int(gate==source and x[0])
            x=step(x,gate)
        out.append(active)
    return Counter(out)
assert len(states)==28 and len(wp)==len(wm)==26
for g in set(wp):
    assert set(map(lambda x:step(x,g),states))==set(states)
hz=Counter({0:4,6:16,8:8})
hi=Counter({0:4,4:8,8:16})
for w in [wp+wp,wm+wm]:
    assert histogram(w)==hz
for w in [wp+wm,wm+wp]:
    assert histogram(w)==hi
for h in (hz,hi):
    assert Fraction(sum(k*n for k,n in h.items()),28)==Fraction(40,7)
t=symbols('t')
delta=sum((hz[i]-hi[i])*t**i for i in hz.keys()|hi.keys())/28
assert factor(delta+2*t**4*(1-t**2)**2/7)==0
# Entire unmasked word-list law is equal after uniformly masking parity.
laws=[]
for chi in (0,1):
    law=Counter()
    signal=0
    for h,k,st in product((0,1),(0,1),states):
        t2=h if (chi^k) else h^1
        law[(h,t2,st)] += 1
        final=list(st)
        for gate in ((wm if h else wp)+(wm if t2 else wp)):
            final=step(final,gate)
        if st[:4]==(0,0,0,1) and (st[4]^k)==0 and final[4]:
            signal+=1
    assert signal==4*chi
    laws.append(law)
assert laws[0]==laws[1]
print('PASS: all four 52-call distributions, active SourceI mean and partition, two-bit mask and selected-event coefficient.')
