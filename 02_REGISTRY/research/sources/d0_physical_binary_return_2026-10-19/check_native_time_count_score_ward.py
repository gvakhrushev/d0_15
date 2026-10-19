#!/usr/bin/env python3
"""Native Golden original first-shell EXIT indicator: Cost/Info score closure and hostile time schedule.

Uses actual one-round blank0 effect and native p. Time-varying scalar-shell
schedule requires real native admission; neither Book action nor GR is selected.
"""
from fractions import Fraction as F
from itertools import product
from math import log, sqrt
import sympy as s

phi=(1+sqrt(5))/2

def history(e,de):
    for x in product((0,1),repeat=len(e)):
        q=F(1); score=F(0)
        for bit,p,dp in zip(x,e,de):
            q*=p if bit else 1-p
            score+=dp/p if bit else -dp/(1-p)
        yield x,q,score

def fisher(e,de):
    Q={k:F(0) for k in range(len(e)+1)}
    dQ=dict(Q); full=F(0)
    for x,q,v in history(e,de):
        k=sum(x);Q[k]+=q;dQ[k]+=q*v;full+=q*v*v
    count=sum(dQ[k]*dQ[k]/Q[k] for k in Q if Q[k])
    return full,count,Q,dQ

n=4;e=[F(1,5)]*n
full,count,Q,dQ=fisher(e,[F(1,50)]*n)
assert full==count and full>0
assert all(dQ[k]==Q[k]*(k/F(1,5)-(n-k)/(1-F(1,5)))*F(1,50)
           for k in Q)
opp=[F(1,50),-F(1,50),F(1,50),-F(1,50)]
f,c,_,D=fisher(e,opp)
assert c==0 and f==F(1,100) and all(v==0 for v in D.values())

# Illustrative homogeneous CODE prior m, not falsely asserted to be the
# original unowned full 128-label Kraft distribution.
m=F(1,3)
R={k:F(0) for k in range(n+1)}
for x,prior,_ in history([m]*n,[F(0)]*n):R[sum(x)]+=prior
for x,q,_ in history(e,[F(0)]*n):
    k=sum(x);prior=s.prod([m if b else 1-m for b in x])
    assert q/Q[k]==prior/R[k]
Hlog=log(phi)
qrows=list(history(e,[F(0)]*n))
urows=list(history([m]*n,[F(0)]*n))
KLfine=sum(float(q)*log(float(q/u))/Hlog
           for (_,q,_),(_,u,_) in zip(qrows,urows))
KLcount=sum(float(Q[k])*log(float(Q[k]/R[k]))/Hlog for k in Q)
assert abs(KLfine-KLcount)<1e-13

# Genuine pinned original epsilon (h=1/4), first shell lambda=288/25.
p=(s.sqrt(5)-1)/2
eps=p**2/s.Integer(1024);lam=s.Rational(288,25)
prob=eps*lam-(eps*lam)**2/4;der=eps*(1-eps*lam/2)
N=1024
Ifine=s.simplify(N*der**2/(prob*(1-prob)))
assert s.simplify(Ifine-N*eps/(lam*(1-eps*lam/4)))==0

# Alternating native-type λ_even=λ-y, λ_odd=λ+y, with extra
# admission required for physically time-dependent schedules.
y,z=s.symbols('y z',real=True)
def eff(L):return eps*L-(eps*L)**2/4
E1,E2=eff(lam+y),eff(lam-y)
pair=s.expand((1-E1+z*E1)*(1-E2+z*E2))
assert s.expand(pair.subs(y,-y)-pair)==0
assert s.simplify(s.diff(pair,y).subs(y,0))==0

print("PASS homogeneous native count score/Fisher exactly sufficient")
print("PASS matching time-homogeneous CODE removes all extra timing KL")
print("PASS hostile 4 ticks: counted first-score/Fisher zero, full=1/100")
print("PASS exact original Golden epsilon and 1024-tick Fisher source")
print("PASS alternating-time count generating polynomial even in field")
print("Original first-shell information lost if alternate schedule admitted:",s.N(Ifine,16))
print("SCOPE: time-varying native actuation, complete Book and GR remain unproved")
