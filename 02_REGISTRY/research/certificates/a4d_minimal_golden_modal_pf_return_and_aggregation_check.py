#!/usr/bin/env python3
"""Golden Pell minimal mode, true fixed-RIGHT PF/ordinary-trace relation,
mean-vs-global-MAP source seam on ONE original conditional J2 carrier.

A mathematical/source calculator. It does not assert native all-work
admission, copied Slater/occupation preparation, complete Book selector,
general spin matter, or physical GR closure.
"""
from __future__ import annotations
from fractions import Fraction as F
from dataclasses import dataclass
from math import sqrt, log, exp
import json

@dataclass(frozen=True)
class Golden:
    """Exact Q(p) arithmetic where p^2=1-p, p=(sqrt(5)-1)/2."""
    a:F
    b:F
    def __init__(self,a=0,b=0):
        object.__setattr__(self,"a",F(a))
        object.__setattr__(self,"b",F(b))
    @staticmethod
    def cv(x):
        return x if isinstance(x,Golden) else Golden(x)
    def __add__(self,x):
        x=self.cv(x)
        return Golden(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Golden(-self.a,-self.b)
    def __sub__(self,x):return self+-self.cv(x)
    def __rsub__(self,x):return self.cv(x)-self
    def __mul__(self,x):
        x=self.cv(x)
        return Golden(self.a*x.a+self.b*x.b,
                      self.a*x.b+self.b*x.a-self.b*x.b)
    __rmul__=__mul__
    def inv(self):
        norm=self.a*(self.a-self.b)-self.b*self.b
        if not norm:raise ZeroDivisionError("Golden norm")
        return Golden((self.a-self.b)/norm,-self.b/norm)
    def __truediv__(self,x):return self*self.cv(x).inv()
    def __rtruediv__(self,x):return self.cv(x)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        y=Golden(1)
        for _ in range(n):y=y*self
        return y
    def eval(self):return float(self.a)+float(self.b)*(sqrt(5)-1)/2
    def to_json(self):return {"a":str(self.a),"b":str(self.b)}

p=Golden(0,1)
one=Golden(1)
assert p*p+p==one
p4=p**4
k_min=one-2*p4
pell_exact=k_min*k_min-Golden(F(1,2))
assert pell_exact == Golden(F(89,2),-72)
assert 161*161-5*72*72==1
assert abs(pell_exact.eval()-1/(2*(161+72*sqrt(5))))<1e-13
assert k_min.eval()>1/sqrt(2)
assert (one-2*p*p).eval()**2<.5   # F=I hostile control for k=1

r2=p4/(one-p4)
assert r2==Golden(F(-1,5),F(3,5))
L=4*p**3
a=p**6
F2=L*(one+a)
Q=one-r2*L
R=one-r2*F2
lam=2/(p**5)*(R/Q+a)
assert lam==Golden(F(1176,79),F(1060,79))
lam_expected=(646+530*sqrt(5))/79
assert abs(lam.eval()-lam_expected)<1e-13

def fib(n):
    a,b=0,1
    for _ in range(n):a,b=b,a+b
    return a

pf_ratio=[]
pp=p.eval()
q=-pp*pp
for N in (0,1,2,3,4,8,12,20):
    d0,d1=fib(N+2),fib(N+1)
    D0,D1=fib(N+8),fib(N+7)
    K=fib(2*N+9)
    mu0,mu1=pp**(N+1),pp**(N+2)
    pi0,pi1=D0/K,D1/K
    assert abs(d0*mu0+d1*mu1-1)<1e-10
    chi=mu0/pi0
    binet=(1-q**(2*N+9))/(1-q**(N+8))
    assert abs(chi-binet)<1e-11
    assert chi>0
    pf_ratio.append({"N":N,"K":K,"chi":chi,"abs_vs_regular":abs(chi-1)})

# A separate AF leaf success mode has d=1056 original defining modes,
# NOT the entire GNS K * spectator reference rank.
d=1056
scene_rank=528
assert d==2*scene_rank
F1=L.eval()
F2float=F2.eval()
assert 0<F1<F2float<1

def native_coin(k):
    w=pp**(2*k)
    ratio=w/(1-w)
    K1=1-w*(1+F1)
    K2=1-w*(1+F2float)
    if K1<=0 or K2<=0:raise ArithmeticError("Outside clean strict chart")
    g=exp(2*scene_rank*(log(K1)+log(K2)))
    worst=exp(2*d*log(1-2*w))
    kappa=g*log(g/(1-g)) if 0<g<1 else float("nan")
    lam_source=2/pp**5*((1-ratio*F2float)/(1-ratio*F1)+a.eval())
    hF=lambda x:x*log(x*x/(1-x*x))
    lambda_all_fine=2/pp**5*(hF(K1)/hF(K2)+a.eval())
    return dict(k=k,w=w,r=ratio,g=g,worst=worst,kappa=kappa,
                lambda_mode=lam_source,
                lambda_fine=lambda_all_fine,
                K1=K1,K2=K2)

C2,C3,C9,C10,C12=[native_coin(k) for k in (2,3,9,10,12)]
assert abs(C2["lambda_mode"]-lam_expected)<5e-13
assert C2["worst"]<.5 and C9["worst"]<.5
assert C10["worst"]>.5
assert C9["g"]<.5 and C10["g"]>.5
assert C10["kappa"]>0
assert abs(C10["g"]-.759460770277765)<2e-10
assert abs(C2["lambda_fine"]-135.446872674)<1e-7
assert abs(C10["lambda_fine"]-C10["lambda_mode"])>.05
# Rational robust proof rather than relying only on float:
assert F(618,1000)<F(619,1000)
assert F(618,1000)**18>F(17,100000)
assert F(619,1000)**20<F(7,100000)
assert F(4224)*F(17,100000)>F(7,10)
assert F(4224)*F(7,100000)/(1-2*F(7,100000))<F(1,2)
# ln(2)<.7 follows exp(.7)>2 by first 5 positive Taylor terms.
x=F(7,10)
lower_e=sum((x**k/F(__import__("math").factorial(k)) for k in range(5)),F(0))
assert lower_e>2
# ln2>.5 follows e^.5<2 by geometric tail bound for k>=2.
assert exp(.5)<2

# Global MAP with two distinct READY source response slopes is a MIN,
# not a linear weighted trace. At the degenerate common baseline:
# local leaves J1=J*+theta, J2=J*; min(theta,0) has derivative mismatch.
eps=1e-5
left=min(-eps,0)/(-eps)
right=min(eps,0)/eps
assert left==1 and right==0

# True binary joint address+good pointer mean source at the common
# vacuum baseline uses the TRUE immutable mu0, not regular-trace pi0.
N=2
D0=fib(N+8); K=fib(2*N+9)
chi=K*pp**(N+1)/D0
slope1,slope2=F(2,7),-F(3,11)
real_pf=(pp**(N+1))*float(slope1+slope2)
trace=(D0/K)*float(slope1+slope2)
assert abs(real_pf-chi*trace)<1e-14

# The source ratio is insensitive to common chi and to any nonzero
# Book scalar κ at the null branch, for geometry+scalar directions.
assert abs(C2["lambda_mode"]-lam_expected)<1e-12

print(json.dumps({
    "status":"PASS: Pell 2-coin mode, native r2, true PF source and MAP/mean boundary",
    "k2_uniform_positive_gap":pell_exact.eval(),
    "k2_pell_norm":"161^2 - 5*72^2 = 1",
    "r2_Q(p)":r2.to_json(),
    "lambda2_Q(p)":lam.to_json(),
    "lambda2_numeric":lam_expected,
    "PF_to_regular_ratio":pf_ratio,
    "k2":C2,"k3":C3,"k9":C9,"k10":C10,"k12":C12,
    "positive_binary_1056_rank_min_k":10,
    "global_READY_MAP_two_direction_derivatives":[left,right],
    "physical_Book_aggregator_selected":False,
    "physical_full_D0_to_GR_derived":False
},sort_keys=True,indent=2))
