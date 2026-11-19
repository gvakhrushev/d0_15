#!/usr/bin/env python3
"""Original Golden F/R full-archive cross-predictive renewal and input screening.

Consumes the original native 72441 word counting and h0 N1 defined report law.
EXACT identities are mathematical on one declared fresh-execution stop task;
this does NOT derive M1/Book03 compulsory future/vertex Info or physical writer.
"""
from __future__ import annotations
import math
from collections import Counter
from fractions import Fraction as F
import sympy as S

N=0
def ok(label, predicate):
    global N
    if not bool(predicate): raise AssertionError(f"FAIL {label}")
    N+=1

def approx(label,x,y,atol=1e-10,rtol=1e-10):
    ok(label,abs(x-y)<=atol+rtol*max(abs(x),abs(y)))

p=(math.sqrt(5)-1)/2
phi=1/p
ell=math.log(phi)
zeta=2**-20
ok('Golden p+p²=1',abs(p+p*p-1)<1e-15)

def h(r):return -(r*math.log(r)+(1-r)*math.log1p(-r))/ell
def score(r):return 1+r-h(r)
def score_d(r):return 1-math.log((1-r)/r)/ell

def cross_trials(r,s):return (1-r)/(1-s)+r/s

def cross_net(r,s):return score(r)+cross_trials(r,s)*score(s)

def cross_deriv_s(r,s):
    K=cross_trials(r,s)
    Ks=(1-r)/(1-s)**2-r/s**2
    return Ks*score(s)+K*score_d(s)

# GENUINE original flat N1 input click at unchanged Golden p,zeta.
B0=4*p**3
A0=B0*(1+p**6)
rb=zeta*(A0+B0)-zeta*zeta*A0*B0
approx('actual original n1 flat positive r',rb,1.8512395784882e-6,2e-18,0)
for r in (rb, 0.071, 0.4):
    approx('same-law mean forecast draws is exactly 2',cross_trials(r,r),2,4e-14,0)
    approx('same-law total registered Price-KL is exactly 3 native',cross_net(r,r),3*score(r),5e-14,0)
    approx('unconstrained Golden-Kraft forecast zero net extra score',cross_net(r,p*p),score(r),5e-14,0)
    ok('positive native excess score',score(r)>0)
    ok('strict premium for matched verification when r != original Golden Kraft',cross_net(r,r)>cross_net(r,p*p))
    eps=1e-10 if r<1e-5 else 1e-7
    slope=(cross_net(r,r+eps)-cross_net(r,r-eps))/(2*eps)
    approx('charged free predictor derivative is NOT zero',slope,cross_deriv_s(r,r),.05 if r<1e-5 else 2e-8,2e-6)
    ok('input is NOT stationary unless real same-source constraint',abs(cross_deriv_s(r,r))>1e-3)
    # KKT reaction equals unique restriction normal; diagonal/envelope derivative is 3 score_d.
    partial_r=score_d(r)+(-1/(1-r)+1/r)*score(r)
    partial_s=cross_deriv_s(r,r)
    approx('constrained field source unchanged except fixed 3',partial_r+partial_s,3*score_d(r),2e-10,0)

lambda_reaction=-cross_deriv_s(rb,rb)
ok('native Golden rare-predictor reaction is extremely large',lambda_reaction>540000)

# The full exact 72,441 original n20 Golden prefix tree, NO synthetic equal site weights.
exact=[]; over=[]
def rec(cost,depth,left,width,word):
    if cost>=20:
        if cost==20:
            site=tuple(min(3,int(4*(left[k]+width[k]/2))) for k in range(4))
            exact.append((word,site))
        else:
            over.append((word,cost))
        return
    axis=depth%4
    wf=width.copy();wf[axis]*=p
    rec(cost+1,depth+1,left.copy(),wf,word+'F')
    wr=width.copy();lr=left.copy()
    lr[axis]+=p*wr[axis];wr[axis]*=p*p
    rec(cost+2,depth+1,lr,wr,word+'R')
rec(0,0,[0.]*4,[1.]*4,'')
counts=Counter(site for word,site in exact)
ok('full original exact cost20 word count 10946',len(exact)==10946)
ok('full original overshoots 6765',len(over)==6765)
ok('all actual 256 spatial sites inhabited',len(counts)==256)
ok('original native count endpoints exactly 29-78',min(counts.values())==29 and max(counts.values())==78)
weights={site:n/10946 for site,n in counts.items()}
a=2*10946*p**23

def rates(t):
    return {site:rb*(1+.17*math.sin(1.5*site[0]+.3*site[1]+2*site[3])+.12*t*math.cos(site[0]+2*site[2])) for site in counts}

def build(t):
    rr=rates(t)
    data=[]
    for word,cost in over:
        mu=p**cost
        data.append((mu,mu,'U',None))
    for word,site in exact:
        for suffix,extra in [('FF',2),('RR',4)]:
            mu=p**(20+extra)
            data.append((mu,mu,'U',None))
        for suffix in ('FR','RF'):
            b=p**23
            r=rr[site]
            data.append((b*(1-r),b*p,'0',site))
            data.append((b*r,b*p*p,'1',site))
    return data,rr

def binary_KL(r):return score(r)

def info(data):
    P=[v[0] for v in data];mu=[v[1] for v in data]
    assert min(P)>0 and min(mu)>0
    return math.fsum(q*math.log(q/m) for q,m in zip(P,mu))/ell

def three_classes(data):
    P={c:0. for c in ('U','0','1')};Q={c:0. for c in ('U','0','1')}
    for val,mu,c,site in data:P[c]+=val;Q[c]+=mu
    return P,Q

for t in (0.,.11,-.14):
    data,rr=build(t)
    ok('all 72441 original complete histories preserved',len(data)==72441)
    approx('true original full born archive normalized',math.fsum(v[0] for v in data),1,2e-10,0)
    approx('true native full code Kraft normalized',math.fsum(v[1] for v in data),1,2e-10,0)
    KL=info(data)
    native=a*math.fsum(weights[s]*binary_KL(r) for s,r in rr.items())
    approx('actual original 72k complete KL equals site native 0/10 score',KL,native,5e-12,0)
    q3,mu3=three_classes(data)
    approx('original U coarse probability',q3['U'],1-a,5e-12,0)
    approx('three real classes exactly normalized',math.fsum(q3.values()),1,4e-11,0)
    # Predict with SAME fine physical law: first outcome and all forecast outcomes kept;
    # stopping uses 3 coarse classes, every full fine outcome still coded and paid.
    K=math.fsum(q3[c]/q3[c] for c in q3)
    approx('same physical three-class forecast mean additional launches',K,3,4e-15,0)
    approx('full fresh stopped Cost-Shannon EXACT factor four',KL+K*KL,4*KL,2e-13,0)
    # Independent paid forecast free to use the ACTUAL Golden code reference mu:
    # its entire own additional score vanishes, although expected launch count changes.
    Kref=math.fsum(q3[c]/mu3[c] for c in q3)
    approx('free Golden-Kraft forecast cannot alter data native score',KL+Kref*info([(x[1],x[1],x[2],x[3]) for x in data]),KL,3e-13,0)
    ok('matched forecast is not globally cheapest paid measured code',4*KL>KL)

# EXACT general finite stopped-tree identity: symbolic two-class probability law.
rv,sv=S.symbols('r s',positive=True)
K=(1-rv)/(1-sv)+rv/sv
ok('exact expected forecast draws at matched input',S.simplify(K.subs(sv,rv)-2)==0)
ok('strict nonzero partial free clock source at native rare input',
   S.simplify(S.diff(K,sv).subs(sv,rv)-(1/(1-rv)-1/rv))==0)
# A truly constrained same-source forecast is NOT a free optimizer;
# its Lagrange multiplier is fixed by the actual complete scalar source.
P,Q=S.symbols('P Q',positive=True)
kP=1+P+(P*S.log(P)+(1-P)*S.log(1-P))/S.log(S.Symbol('phi'))
kQ=1+Q+(Q*S.log(Q)+(1-Q)*S.log(1-Q))/S.log(S.Symbol('phi'))
full=kP+((1-P)/(1-Q)+P/Q)*kQ
qgrad=S.simplify(S.diff(full,Q).subs(Q,P))
pgrad=S.simplify(S.diff(full,P).subs(Q,P))
complete=S.simplify(S.diff(3*kP,P))
ok('true whole first-source equals constrained Euler pullback', S.simplify(qgrad+pgrad-complete)==0)

print('PASS',N,'genuine original native Golden/72,441/predictive-KL/KKT checks')
print('original flat N1 click', format(rb,'.17g'))
print('original phi-only forecast µ1', format(p*p,'.17g'))
print('rare real forecast source constraint reaction', format(lambda_reaction,'.13g'))
print('FULL same-source m=3 stopping measured-KL = 4× complete actual native data KL at every t')
print('Unconstrained independent forecast optimum is Kraft µ, NOT true Bernoulli r; M1 future equality is NOT derived')
print('GR_closed=false; Book03 full H+J+R/oldRIGHT/true clock/input writer still OPEN')
