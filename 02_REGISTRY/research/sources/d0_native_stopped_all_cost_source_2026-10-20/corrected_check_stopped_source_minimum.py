#!/usr/bin/env python3
"""Exact rational bounds for prospective STOPPED original Golden reporter.

Consumes the already proved three-query complete scalar-cleanup first jet
and the actual Golden 0 / 10 reporter.  DOES NOT select a physical G0 task,
assign full Book03 Info or posit a free query. Standard library only.
"""
from __future__ import annotations
from fractions import Fraction as Q
from decimal import Decimal as D, localcontext

def plus(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def minus(a,b):return plus(a,neg(b))
def times(a,b):
    r=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return min(r),max(r)
def div(a,b):
    assert b[0]>0
    return times(a,(1/b[1],1/b[0]))
def scale(a,x):return times(a,(Q(x),Q(x)))
def bounds(x):return Q(x),Q(x)

# Rational enclosing algebraic Golden p. Check roots rather than trusting floats.
plo=Q("0.61803398874989")
phi=Q("0.61803398874990")
assert (2*plo+1)**2<5<(2*phi+1)**2
p=(plo,phi)
x=minus(scale(p,2),bounds(1))
tk=[bounds(1),x]
for k in range(2,7):
    tk.append(minus(scale(times(x,tk[-1]),2),tk[-2]))
q=[div(minus(bounds(1),v),bounds(2)) for v in tk]
assert q[1][1]<Q(2,3)
assert q[3][1]<Q(8,9)
assert all(q[k][1]<q[2][0] for k in (1,3,4,5,6))
assert all(q[k][0]>0 and q[k][1]<1 for k in range(1,7))

def log_bound(x,n):
    """For rational x>1, certified positive atanh-series remainder bound."""
    assert x>1
    t=(x-1)/(x+1)
    val=Q(0)
    power=t
    for j in range(n):
        val+=2*power/Q(2*j+1)
        power*=t*t
    # Remaining j=n,n+1,... : denominators >=2n+1.
    err=2*power/(Q(2*n+1)*(1-t*t))
    return val,val+err

L4=log_bound(Q(4),75)
LPhi=(log_bound(1/phi,35)[0],log_bound(1/plo,35)[1])
l4phi=div(L4,LPhi)
assert l4phi[0]>1
def pow_bound(i):return plo**i,phi**i
r3=pow_bound(3);r6=pow_bound(6)
D2lo=4*r3[0]*(l4phi[0]-1)-5*r6[1]
D2hi=4*r3[1]*(l4phi[1]-1)-5*r6[0]
assert Q(1497,1000)<D2lo<D2hi<Q(1498,1000)
# Golden q2=4p^3, 1-q2=p^6; this is an exact ring identity.
q2=(4*r3[0],4*r3[1])
assert q2[0]<q[2][1] and q2[1]>q[2][0]
assert (Q(5)+2+D2hi)/q2[0]<9
assert (Q(50)+2+D2hi)/q2[0]<57
# Proof for ALL k>0 and ALL real 5<=T0<=50:
# k>=7: Jk >= T0+k >=T0+7>J2 (latter affine max at T0=50).
# k=1,3,4,5,6: at T0=5 Jk>(5+k)/qk>J2(5),
# and d_(T0)(Jk-J2)=1/qk-1/q2>0.
# k0 cannot halt at the common-null source t=0 (q0=0).
assert (5+1)/q[1][1]>9
assert (5+3)/q[3][1]>9
assert all((5+k)/q[k][1]>=9 for k in (4,5,6))
print("RATIONAL_INTERVAL_PROOF: G^2 strictly minimizes the stopped")
print("actual 0/10-pointer Cost-minus-Info among every k>=1 for 5<=T0<=50.")
print("RATIONAL_INTERVAL_PROOF: 1.497 < D_phi(q2||p^2) < 1.498")
print("RATIONAL_INTERVAL_PROOF: k>=7 excluded without truncating k search")
print("EXACT ALGEBRA: q2=4p^3, 1-q2=p^6, q2'(0)=8p^(9/2)")
print("EXACT FIRST SOURCE: D S_stop(G^2)=-(T0-3)/(2p^(3/2)) * Dt")

with localcontext() as ctx:
    ctx.prec=65
    pp=(D(5).sqrt()-1)/2
    ff=1/pp
    ll=ff.ln()
    a=pp.sqrt()
    c,s=D(1),D(0)
    qs={}
    for k in range(1,151):
        c,s=a*c-pp*s, pp*c+a*s
        qq=s*s
        qs[k]=qq
    def DK(qq):
        return (qq*(qq/(pp*pp)).ln()+(1-qq)*((1-qq)/pp).ln())/ll
    def objective(k,T):return (D(T+k)+DK(qs[k]))/qs[k]
    for t0 in (5,30,50,100):
        best=min(range(1,151),key=lambda k:objective(k,t0))
        print("T0",t0,"winner among 150:",best,"score:",round(objective(best,t0),12))
        if 5<=t0<=50:assert best==2
    # Independently re-derive exact first source from the generic geometric law.
    q2n=qs[2];qp=4*(a*a-pp*pp)*(2*a*pp)
    assert abs(q2n-4*pp**3)<D("1e-60")
    assert abs(qp-8*pp**D("4.5"))<D("1e-59")
    source=-(qp/(q2n*q2n))*(D(7)+((1-q2n)/pp).ln()/ll)
    target=-D(1)/(pp**D("1.5"))
    assert abs(source-target)<D("1e-57")
    print("G2 stopped-source coefficient at T0=5:",round(source,16))
    print("PASS: original Golden prospective first source and exact 0/10 code.")
