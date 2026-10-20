#!/usr/bin/env python3
"""D0 unknown-magnitude Golden17 sign verification and complete price.
Original u/v and all 15 neutral labels are consumed unchanged. No new
quantum coin, detector, compulsory Book Info or GR closure is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
import mpmath as mp
import sympy as sp

mp.mp.dps=90
P=(mp.sqrt(5)-1)/2
PHI=1/P

@dataclass(frozen=True)
class Golden:
    """Exact integer ring a+b*p with p^2=1-p and exact real ordering."""
    a:int
    b:int=0
    def __add__(self,other):
        if isinstance(other,int): other=Golden(other)
        return Golden(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self):return Golden(-self.a,-self.b)
    def __sub__(self,other):return self+(-other)
    def __mul__(self,other):
        if isinstance(other,int): other=Golden(other)
        a,b,c,d=self.a,self.b,other.a,other.b
        return Golden(a*c+b*d,a*d+b*c-b*d)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0:raise ValueError('nonnegative exponent required')
        out=Golden(1);base=self
        while n:
            if n&1:out=out*base
            base=base*base;n//=2
        return out
    def sign(self):
        u,v=2*self.a-self.b,self.b
        sg=lambda z:(z>0)-(z<0)
        if v==0:return sg(u)
        if u==0:return sg(v)
        if sg(u)==sg(v):return sg(u)
        return sg(u*u-5*v*v) if u>0 else -sg(u*u-5*v*v)
    def value(self):return mp.mpf(self.a)+mp.mpf(self.b)*P

GP=Golden(0,1);ONE=Golden(1);ZERO=Golden(0)
assert GP*GP+GP==ONE

def code_cost(j:int)->int:
    if j<1:raise ValueError('j>=1 required')
    ell=j.bit_length()
    return 2*ell+(j.bit_count()-1)

def weight(j:int)->Golden:return GP**code_cost(j)
checks=[]
def checked(name):checks.append(name);print('PASS',name,flush=True)

for ell in range(1,10):
    block=sum((weight(j) for j in range(2**(ell-1),2**ell)),ZERO)
    assert block==GP**(ell+1)
    partial=sum((weight(j) for j in range(1,2**ell)),ZERO)
    assert partial==ONE-GP**ell
checked('exact complete Golden scale code; partial Kraft mass 1-p^ell')
for a in range(-9,10):
    for b in range(-9,10):
        z=Golden(a,b)
        assert z.sign()==int(mp.sign(z.value()))
checked('exact real ordering in Z[p], no floating stopping decisions')

x,th=sp.symbols('x th',real=True)
p=(sp.sqrt(5)-1)/2;c=p**4/sp.Integer(98304)
u=c*(1+x/sp.sqrt(2))**2;v=c*(1-x/sp.sqrt(2))**2
neutral=1-u-v
assert sp.simplify(u-v-2*sp.sqrt(2)*c*x)==0
assert sp.simplify(u+v-(2*c+c*x*x))==0
assert sp.simplify(u*(1+th)+v*(1-th)+neutral-(1+th*(u-v)))==0
assert sp.simplify(v*(1+th)+u*(1-th)+neutral-(1-th*(u-v)))==0
eta=sp.symbols('eta',real=True)
g=(1+eta)*sp.log(1+th)/2+(1-eta)*sp.log(1-th)/2
assert sp.simplify(sp.diff(g,th)-(eta-th)/(1-th**2))==0
kap_symbol=sp.simplify(p-p*p/2)
assert sp.simplify(kap_symbol-(3*p-1)/2)==0 and float(kap_symbol)>0
checked('original native u/v, all neutral mass, conditional supermartingale and drift')

MAX_K=72
scales=[j for j in range(1,32) if (GP**j*MAX_K-ONE).sign()>=0]
cache={}
for j in scales:
    theta=GP**j;plus=[ONE];minus=[ONE]
    for n in range(MAX_K):
        plus.append(plus[-1]*(ONE+theta))
        minus.append(minus[-1]*(ONE-theta))
    cache[j]=(theta,weight(j),plus,minus)

def decision(k,nplus):
    if not 0<=nplus<=k<=MAX_K:raise ValueError('invalid counts')
    nminus=k-nplus
    for j,(theta,mu,plus,minus) in cache.items():
        if (theta*k-ONE).sign()<0:continue
        if (mu*plus[nplus]*minus[nminus]-Golden(10)).sign()>=0:return 1
        if (mu*plus[nminus]*minus[nplus]-Golden(10)).sign()>=0:return -1
    return 0

decisions={(k,n):decision(k,n) for k in range(1,MAX_K+1) for n in range(k+1)}

def finite_risk(bias:Fraction):
    pp=(1+bias)/2;alive={0:Fraction(1)};ep=em=Fraction(0)
    for k in range(1,MAX_K+1):
        nxt={}
        for n,mass in alive.items():
            for inc,pr in [(1,pp),(0,1-pp)]:
                key=n+inc;mm=mass*pr;d=decisions[k,key]
                if d>0:ep+=mm
                elif d<0:em+=mm
                else:nxt[key]=nxt.get(key,Fraction(0))+mm
        alive=nxt
    remaining=sum(alive.values(),Fraction(0))
    assert ep+em+remaining==1
    if bias<=0:assert ep<=Fraction(1,10)
    if bias>=0:assert em<=Fraction(1,10)
    return {'eta':str(bias),'plus':float(ep),'minus':float(em),
            'unresolved_at_k72':float(remaining)}
risks=[finite_risk(Fraction(n,4)) for n in [-3,-1,0,1,3]]
checked('exact finite absorbing DP: same rule at five unknown strengths')

cn=mp.mpf(str(sp.N(c,95)));kap=P-P*P/2;bounds=[]
for raw in ['0.10','0.05','0.02','0.01']:
    xi=mp.mpf(raw);rate=2*cn*(1+xi*xi/2)
    bias=mp.sqrt(2)*xi/(1+xi*xi/2);j=1
    while P**j>bias:j+=1
    theta=P**j;mu=P**code_cost(j)
    assert P*bias<=theta<=bias
    drift=(1+bias)*mp.log(1+theta)/2+(1-bias)*mp.log(1-theta)/2
    assert drift>=kap*bias*bias-mp.mpf('1e-80')
    activation=int(mp.ceil(1/theta));A=mp.log(1/(mp.mpf('.1')*mu))
    bound_k=activation+(A+PHI**3+mp.log(PHI))/drift
    lr=4*mp.atanh(xi/mp.sqrt(2))
    known_m=int(mp.ceil(mp.log(9)/lr));r=mp.exp(-known_m*lr)
    known_t=known_m*(1-r)/((2*mp.sqrt(2)*cn*xi)*(1+r))
    bounds.append({'xi':raw,'analysis_only_j':j,'code_cost':code_cost(j),
      'known_scale_optimal_raw':float(known_t),
      'universal_raw_upper_bound':float(bound_k/rate),
      'activation':activation,'drift':float(drift)})
checked('full native trial bound including neutral waiting and scale activation')

z,a=sp.symbols('z a',positive=True)
f=sp.log(sp.cosh(z))+(a-1)*z*sp.tanh(z)
assert sp.simplify(sp.diff(f,z)-(a*sp.tanh(z)+(a-1)*z/sp.cosh(z)**2))==0
checked('closed stopped Cost-minus-complete-record-Info derivative')
# Universal entropy-chain-rule check, NOT a replacement Golden17 quantum law.
uh=mp.mpf('.36');vh=mp.mpf('.14');rr=1-uh-vh
entropy=lambda ps:-sum(t*mp.log(t) for t in ps if t>0)
Hone=entropy([uh,vh,rr]);et=1/(uh+vh);eps=vh/(uh+vh)
Istop=mp.log(2)-entropy([eps,1-eps])
Hmix=entropy([uh+vh,rr])*et+mp.log(2)
assert abs(Hmix-(Hone*et+Istop))<mp.mpf('1e-70')
mu=[mp.mpf('.2'),mp.mpf('.3'),mp.mpf('.5')]
bar=[(uh+vh)/2,(uh+vh)/2,rr]
price=-sum(q*mp.log(m) for q,m in zip(bar,mu))*et-Hmix
mismatch=sum(q*mp.log(q/m) for q,m in zip(bar,mu))
assert abs(price-et*mismatch)<mp.mpf('1e-70')
checked('generic full stopped entropy and m1 relative-code-price cancellation')

out={'status':'AUTHOR_REPLAY_PASS','source_scope':'original Golden17 u/v; generic code lemmas separately marked',
 'c':float(cn),'phi':float(PHI),'checks':checks,'finite_exact_risks':risks,
 'raw_trial_bounds':bounds,'physical_Book_Info_selected':False,'GR_closed':False,
 'controller_gate_cost_optimality_claimed':False}
Path(__file__).with_name('UNKNOWN_SCALE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
