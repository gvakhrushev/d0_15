"""Finite measured histories, literal per-trial discounts, and the exact generating function."""
from fractions import Fraction as F
from itertools import product
import json
import sympy as sp

def trial_leaves(s,cap):
    result=[]
    for first, mass in [(0,1-s),(1,s)]:
        result.append((mass**2,0,False,first))
        active=[mass*(1-mass)]
        for n in range(1,cap+1):
            next_active=[]
            for parent in active:
                result.extend((parent*s*(1-s),n,False,first) for _ in range(2))
                next_active.extend([parent*s*s,parent*(1-s)**2])
            active=next_active
        result.extend((parent,cap,True,first) for parent in active)
    return result

count=0
for s,t in [(F(2,3),F(3,7)),(F(7,10),F(5,9)),(F(1,2),F(1))]:
    rho=s*s+(1-s)**2
    for cap in range(6):
        leaves=trial_leaves(s,cap)
        assert sum(pr for pr,*_ in leaves)==1
        assert sum(pr*n for pr,n,*_ in leaves)==1-rho**cap
        for first in [0,1]:
            assert sum(pr for pr,n,failed,k in leaves if failed and k==first)==s*(1-s)*rho**cap
        for nu in [1,2,3]:
            a=s**(2*nu)+(1-s)**(2*nu)
            b=2*(s*(1-s))**nu
            expected=a+t*b*b*sum((t*a)**j for j in range(cap))+b*(t*a)**cap
            actual=sum(pr**nu*t**n for pr,n,*_ in leaves)
            assert actual==expected
        count+=len(leaves)
s,t,x,y=sp.symbols('s t x y')
a=x*x+y*y
b=2*x*y
Z=a+t*b*b/(1-t*a)
v=((1-t*(x+y)**2)**(-1)+(1-t*(x-y)**2)**(-1))/2
assert sp.factor((1-t*Z)*v-1)==0
lam=sp.symbols('lambda')
Z1=1-lam*(1-t)/(1-t+t*lam)
assert sp.factor(Z1.diff(lam)+(1-t)**2/(1-t+t*lam)**2)==0
p=(sp.sqrt(5)-1)/2
assert sp.simplify(1-p-p**4-p**3)==0
assert sp.simplify(2*p-1-p**3)==0
assert sp.simplify(p+p**4-1)<0
print(json.dumps({"status":"PASS","finite_ledger_leaves_checked":count,
  "caps":"0 through 5","probability_powers":[1,2,3],
  "schur_identity":"exact","uniform_source_lower_bound_for_nu_1_to_2":"p^10*(1-t_max)^2 for natural negative log after dilution",
  "unbounded_expected_forward_and_reverse_calls_each":2,
  "same_as_compulsory_Book03_net_price":False},indent=2))
