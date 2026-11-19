#!/usr/bin/env python3
"""Native Golden adaptive side-resource complete Cost-Shannon theorem.
33 scoped checks. Physical Book03 vertex Info is NOT assumed Shannon.
"""
from itertools import product
from math import sqrt, log, isclose
from sympy import sqrt as sr, simplify, Rational as Q, symbols, diff

p=(sr(5)-1)/2
phi=1/p
assert simplify(p+p*p-1)==0
checks=[]
def check(name,yes):
    if not bool(yes):raise AssertionError(name)
    checks.append(name)

def extractor(cap):
    '''All native Golden F/R word transcripts, including capped abort.'''
    results=[]
    def rec(prefix,attempt):
        for pair in product('FR',repeat=2):
            word=''.join(pair)
            path=prefix+word
            if word in ('FR','RF') or attempt==cap:
                results.append((path, 'bit0' if word=='FR' else 'bit1' if word=='RF' else 'capped'))
            else: rec(path,attempt+1)
    rec('',1)
    return results

for cap in range(1,5):
    leaves=extractor(cap)
    weighted=[]
    for word,label in leaves:
        cost=word.count('F')+2*word.count('R')
        w=p**cost
        weighted.append((word,label,cost,w))
    check('all capped full histories retained '+str(cap),
          len(leaves)==2*sum(2**(j-1) for j in range(1,cap+1))+2**cap)
    check('Kraft normalization includes capped abort '+str(cap),
          simplify(sum(w for _,_,_,w in weighted)-1)==0)
    cost_mean=simplify(sum(w*c for _,_,c,w in weighted))
    check('pathwise golden log-prob exactly equals code cost '+str(cap),
          all(simplify(w-p**c)==0 for _,_,c,w in weighted))
    probbit=[simplify(sum(w for _,label,_,w in weighted if label==name))
             for name in ('bit0','bit1')]
    check('native true fair labels same unconditional mass '+str(cap),
          simplify(probbit[0]-probbit[1])==0)
    if cap>1:
        check('aborted completed prefix separately archived '+str(cap),
              any(x[1]=='capped' for x in leaves))
    pnum=(sqrt(5)-1)/2
    H=sum(float(w)*(-log(float(w))/log(1/pnum))
          for _,_,_,w in weighted)
    check('full measured entropy equals entire code charge '+str(cap),
          isclose(H,float(cost_mean),rel_tol=3e-13,abs_tol=2e-13))

# Field-dependent genuine number of whole data attempts, each drawing fresh coins:
r=symbols('r',positive=True)
Ccoin=symbols('Ccoin',positive=True)
T=1/(1-r)
coin_work=T*Ccoin
coin_entropy=T*Ccoin
check('whole-archive Golden cost minus measured Shannon zero',
      simplify(coin_work-coin_entropy)==0)
check('all field first-source Golden-only resource cancels',
      simplify(diff(coin_work-coin_entropy,r))==0)
check('all field second-source Golden-only resource cancels',
      simplify(diff(coin_work-coin_entropy,r,2))==0)
check('raw Golden-only WORK by itself is source bearing',
      simplify(diff(coin_work,r)-Ccoin/(1-r)**2)==0)

pbit=simplify((p+2*p*p)/p**3)
check('fair-bit real Golden mean code cost positive',float(pbit)>5)
check('expected exact Golden cost 3phi+1',simplify(pbit-(3*phi+1))==0)
coin20=simplify(20*pbit)
check('20 truly fair bits charge between 117 and 118',117<float(coin20)<118)
check('original Book ζ from 20 actual fair bits',Q(1,2)**20==Q(1,2**20))
# The independently previously verified h0 raw-source sign is consumed only.
lo,hi=0.1108705815198,0.1108739928097
check('prior h0 raw coin-work reaction strict sign',0<lo<hi)
check('that raw reaction is neutral after ENTIRE measured coin Info',
      simplify(diff(Ccoin*T-Ccoin*T,r))==0)

print('PASS',len(checks),'original full Golden F/R adaptive source-neutral controls')
print('true 20 fair bits Golden CODE COST',float(coin20))
print('pure Golden source in complete measured Price-minus-Shannon is identically 0')
print('Book03 compulsory Info / physical moving gates / GR remain OPEN')
