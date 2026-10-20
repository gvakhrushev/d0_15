#!/usr/bin/env python3
"""Exact bounded checks for the same Golden full-record selector argument.

No external dependencies, repository mutations, or fitted constants.
The analytic note owns all-dimension/all-k statements.
"""
from fractions import Fraction as F
from math import log, sqrt
import json


class K:
    """Q[x]/(x^4+x^2-1), x=sqrt(phi^-1); exact Golden field arithmetic."""
    def __init__(self, a=0):
        if isinstance(a, K):
            self.a = a.a
        elif isinstance(a, (tuple, list)):
            q = list(map(F, a))
            q += [F(0)] * max(0, 4-len(q))
            for n in range(len(q)-1, 3, -1):
                q[n-4] += q[n]
                q[n-2] -= q[n]
            self.a = tuple(q[:4])
        else:
            self.a = (F(a), F(0), F(0), F(0))
    def __add__(self, b):
        b = K(b)
        return K([x+y for x,y in zip(self.a,b.a)])
    __radd__ = __add__
    def __neg__(self):
        return K([-x for x in self.a])
    def __sub__(self, b): return self + -K(b)
    def __rsub__(self, b): return K(b) + -self
    def __mul__(self, b):
        b = K(b); q = [F(0)]*7
        for i,x in enumerate(self.a):
            for j,y in enumerate(b.a): q[i+j] += x*y
        return K(q)
    __rmul__ = __mul__
    def __pow__(self, n):
        assert n >= 0
        out = K(1)
        for _ in range(n): out *= self
        return out
    def __eq__(self, b): return self.a == K(b).a
    def real(self):
        x = sqrt((sqrt(5)-1)/2)
        return sum(float(a)*x**i for i,a in enumerate(self.a))


checks = 0
def verify(v, label):
    global checks
    if not v: raise AssertionError(label)
    checks += 1


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),K())
             for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(z) for z in zip(*a)]
def eye(n): return [[K(int(i==j)) for j in range(n)] for i in range(n)]
def madd(a,b): return [[x+y for x,y in zip(u,v)] for u,v in zip(a,b)]
def msub(a,b): return [[x-y for x,y in zip(u,v)] for u,v in zip(a,b)]
def kron(a,b):
    return [[x*y for x in ar for y in br] for ar in a for br in b]


x=K([0,1]); p=x*x
G=[[x,-p],[p,x]]
verify(p*p+p==1, 'original p normalization')
verify(mm(tr(G),G)==eye(2),'Golden unitarity')
G2=mm(G,G)
verify(G2==[[p**3,-2*p*x],[2*p*x,p**3]],'literal G squared')

# Reporter keeps b, work, report word 0/10, and actual 1/2 tick clock.
# Each binary report/clock coordinate indexes the two distinct stored values.
R=[[K() for _ in range(4)] for _ in range(16)]
for b in range(2):
    for w in range(2):
        R[((b*2+w)*2+b)*2+b][b*2+w]=K(1)
verify(mm(tr(R),R)==eye(4),'complete reporter isometry')
PR=mm(R,tr(R))
U=madd(mm(mm(R,kron(G,eye(2))),tr(R)),msub(eye(16),PR))
verify(mm(tr(U),U)==eye(16),'field-independent full reporter transport unitary')

# Actual three-call cleanup, executed independently from its asserted formula.
fixtures=[(F(0),F(1)),(F(3,5),F(4,5)),(F(5,13),F(12,13)),
          (F(-3,5),F(4,5)),(F(8,17),F(15,17))]
for t,u in fixtures:
    verify(t*t+u*u==1,'rational complete query')
    W=[[K(t),K(-u)],[K(u),K(t)]]
    refl=[[K(1),K(0)],[K(0),K(-1)]]
    clean=[[K(1)],[K(0)]]
    raw=mm(mm(mm(mm(refl,tr(W)),refl),W),clean)
    # Flag P/Q; execute W only on flag one; keep every work output.
    out=[-raw[0][0],K(),-W[0][1]*raw[1][0],-W[1][1]*raw[1][0]]
    expected=[K(1-2*t*t),K(),K(2*t*(1-t*t)),K(-2*t*t*u)]
    verify(out==expected,'actual three-query full output')
    verify(sum((v*v for v in out),K())==1,'complete output normalized')
    q=out[2]**2+out[3]**2
    verify(q==4*t*t*(1-t*t),'all-work k0 probability')
    verify(q-out[2]**2==4*t**4*(1-t*t),'omitted-work hostile control')
    col=[[a] for a in out]
    left=mm(U,mm(R,col))
    right=mm(R,mm(kron(G,eye(2)),col))
    verify(left==right,'exact full retained output intertwining')

# Full first jets, not numerical finite differences. At Sigma all garbage
# derivatives vanish; the exact complete query tangent is 2|1,clean> dt.
power=eye(2)
for k in range(9):
    c,s=power[0][0],power[1][0]
    psi=[c,K(),s,K()]; dpsi=[-2*s,K(),2*c,K()]
    norm=sum((a*a for a in dpsi),K())
    overlap=sum((a*b for a,b in zip(psi,dpsi)),K())
    verify(4*(norm-overlap*overlap)==16,'full coherent QFI including k0')
    if k:
        verify(c!=0 and s!=0,'tested Golden chart is regular')
        dq=4*c*s
        # Clear positive denominator c²s² from Fisher=16.
        verify(dq*dq*(c*c+s*s)==16*c*c*s*s,'full pointer Fisher saturation')
    power=mm(power,G)

verify(p**6+4*p**3==1,'G2 complete clean law')
verify((4*p**3-p*p).real()>0,
       'G2 coherent reporting excess is positive')
phi=(1+sqrt(5))/2
def h(q): return (-q*log(q)-(1-q)*log(1-q))/log(phi)
z=2.0**-20
for t in [z/2,z/4,z/8,z/16]:
    q=4*t*t*(1-t*t)
    # log1p avoids cancellation at the actual tiny original signal scale.
    from math import log1p
    entropy=(-q*log(q)-(1-q)*log1p(-q))/log(phi)
    verify(0<q<=z*z<1/phi,'actual signal range')
    verify(entropy>q,'complete binary marginal forces strict pointer descent')

print(json.dumps({'status':'PASS','checks':checks,
  'scope':'Exact bounded complete-circuit, reporter-isometry and first-jet checks; analytic note owns all-k/all-carrier theorem.',
  'native_price_selection':False,'GR_closed':False},indent=2))
