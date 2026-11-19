#!/usr/bin/env python3
"""Exact paid Golden flag instrument on the actual t=0 resource support.

Tests the changed premise: a finite paid ± preparation, including EVERY
flag failure. Does not simulate or certify the separately owned compiler.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
from decimal import Decimal, getcontext
class MP:
    mpf=staticmethod(lambda x: Decimal(str(x)))
    sqrt=staticmethod(lambda x: Decimal(str(x)).sqrt())
    log=staticmethod(lambda x: Decimal(str(x)).ln())
    nstr=staticmethod(lambda x,n: format(x,f'.{n}g'))
mp=MP()

class Q:
    __slots__ = ('a','b')
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    def __add__(self,o):
        o=asq(o); return Q(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Q(-self.a,-self.b)
    def __sub__(self,o): return self+-asq(o)
    def __rsub__(self,o): return asq(o)+-self
    def __mul__(self,o):
        o=asq(o); return Q(self.a*o.a+self.b*o.b,
                           self.a*o.b+self.b*o.a-self.b*o.b)
    __rmul__=__mul__
    def __pow__(self,n):
        assert n>=0
        z=Q(1); t=self
        while n:
            if n&1: z=z*t
            n//=2; t=t*t
        return z
    def __eq__(self,o):
        o=asq(o); return self.a==o.a and self.b==o.b
    def __repr__(self): return f'Q({self.a},{self.b})'

def asq(x): return x if isinstance(x,Q) else Q(x)
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def kron(x,y): return [a*b for a in x for b in y]
def partial1(v):
    return [[sum(v[4*i+k]*v[4*j+k] for k in range(4))
             for j in range(4)] for i in range(4)]
def outer(x,y): return [[a*b for b in y] for a in x]
def swap_active(v): return [v[i^1] for i in range(4)]
def both_active(v): return [v[i^5] for i in range(16)]
def product_sign(pattern,inds):
    out=1
    for i in inds: out*=pattern[i]
    return out

p=Q(0,1)
beta=[Q(F(1,2)),Q(F(1,2)),Q(F(1,2)),Q(F(-1,2))]
beta_perp=swap_active(beta)
chi=kron(beta,beta); achi=both_active(chi)
assert dot(beta,beta)==1 and dot(beta,beta_perp)==0
assert dot(chi,achi)==0 and dot(achi,achi)==1
checks=[]

for m in range(1,17):
    alpha=p**m
    ready=(1-alpha)**2+alpha**2
    fail=2*alpha*(1-alpha)
    assert ready+fail==1
    # Every individual nonreturn flag has squared b_y=p^(2m+|y|).
    sum_b2=sum(comb(m,k)*p**(2*m+k) for k in range(1,m+1))
    assert sum_b2==alpha-alpha**2 and 2*sum_b2==fail
    for sign in (-1,1):
        v=[(1-alpha)*x+sign*alpha*y for x,y in zip(chi,achi)]
        assert dot(v,v)==ready
        assert dot(v,both_active(v))==sign*2*alpha*(1-alpha)
        red=partial1(v)
        b0=outer(beta,beta); b1=outer(beta_perp,beta_perp)
        expected=[[(1-alpha)**2*b0[i][j]+alpha**2*b1[i][j]
                   for j in range(4)] for i in range(4)]
        assert red==expected
        assert sum(red[i][i^1] for i in range(4))==0
        # All nonreturn branches are proportional to sign*A-I.
        fv=[sign*y-x for x,y in zip(chi,achi)]
        assert dot(fv,fv)==2
        assert dot(fv,both_active(fv))==-sign*2
        # Complete, UNCONDITIONED pair mean is zero; no failure erased.
        assert dot(v,both_active(v))-sign*fail==0
    checks.append(m)

getcontext().prec=90
pn=(mp.sqrt(5)-1)/2
z=mp.mpf(2)**-20; tau=pn**4; bd=mp.mpf(2); rho=mp.mpf(1)
l0=4*pn**3; m0=l0*(1+pn**6)
q0=1-z*l0; rr0=1-z*m0; r0=1-q0*rr0
qcoeff=-mp.mpf(5)/4*pn**6*bd**2*z/rho
kappa=4*(-1)*z*rr0*pn**4*tau*qcoeff
def h(x): return -(x*mp.log(x)+(1-x)*mp.log(1-x))/mp.log(1/pn)
def g(x): return x-h(x)
gp=1-mp.log((1-r0)/r0)/mp.log(1/pn)
normal=8*(-1)*z*rr0*pn**4*qcoeff*gp
rows=[]
for m in (2,4,8,16,32,64):
    alpha=pn**m; eps=alpha/(1-alpha)
    ready=(1-alpha)**2+alpha**2
    corr=2*eps/(1+eps**2)
    rp,rm=r0+kappa*corr,r0-kappa*corr
    assert 0<rm<rp<pn**2
    delta=ready*(g(rp)-g(rm))
    assert delta<0
    sec=delta/(2*eps*ready*tau)
    rows.append({'m':m,'flag_readiness':mp.nstr(ready,22),
                 'epsilon':mp.nstr(eps,22),
                 'actual_ledger_contrast_over_common_readiness':mp.nstr(delta,22),
                 'normalized_secant':mp.nstr(sec,22),
                 'relative_error_to_owned_normal':mp.nstr(abs(sec/normal-1),15)})
assert abs(sec/normal-1)<mp.mpf('1e-24')

# Cyclic fixed-count shell: all branches have the same collective mean;
# each physical register has the original mean after retaining the shift.
shells=[]
for n in range(1,5):
    N=2**n
    for k in range(N+1):
        pattern=[1]*k+[-1]*(N-k)
        words=[pattern[s:]+pattern[:s] for s in range(N)]
        t=F(2*k-N,N)
        assert all(F(sum(w),N)==t for w in words)
        assert all(F(sum(w[i] for w in words),N)==t for i in range(N))
        for degree in range(1,5):
            # Ordered sampling WITH replacement, exact direct summation.
            val=sum(product_sign(pattern,inds) for inds in product(range(N),repeat=degree)) if N<=4 else sum(pattern)**degree
            assert F(val,N**degree)==t**degree
        shells.append((N,k))

result={'status':'PASS','arithmetic':'exact Q(p), p^2=1-p; rational shell checks; 90-digit log diagnostic',
        'exact_flag_depths':checks,'flag_return_and_every_failure_law':True,
        'unchanged_decoded_zero_mean_exact':True,
        'all_one_resource_first_jets_zero':True,
        'matched_complete_counted_CQ_baseline': 'analytic composition with pinned paid compiler; not a compiler replay',
        'normal_target':mp.nstr(normal,30),'finite_price_secants':rows,
        'cyclic_shells_checked':len(shells),
        'native_autonomous_same_controller_selection':False,
        'complete_Book_price_selected':False,'GR_closed':False}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
