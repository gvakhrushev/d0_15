#!/usr/bin/env python3
"""Exact inverse-coframe to CAR reference compiler identities on the declared coherent-query interface."""
import itertools
import sympy as s
eta=s.diag(1,-1,-1,-1)
perms=[(t,s.LeviCivita(*t)) for t in itertools.permutations(range(4))]
def wedge(u,v): return u*v.T-v*u.T
def star(b):
    low=eta*b*eta
    ans=s.zeros(4)
    for (a,b,c,d),sgn in perms:
        ans[a,b]+=sgn*low[c,d]/2
    return ans
e=s.Matrix([[2,1,0,1],[0,2,1,0],[1,0,2,1],[0,1,0,2]])
assert e.det()!=0
v=eta*e.inv().T
d=v.det()
pairs=list(itertools.combinations(range(4),2))
c=[]
for j in range(4):
    cj=s.zeros(16)
    for n in range(16):
        if not n & (1<<j):
            cj[n|(1<<j),n]=(-1)**((n&((1<<j)-1)).bit_count())
    c.append(cj)
def creator(u): return sum((u[j]*c[j] for j in range(4)),s.zeros(16))
def lift(b): return sum((b[i,j]*c[i]*c[j].T for i in range(4) for j in range(4)),s.zeros(16))
h=s.diag(*[s.prod(eta[j,j] for j in range(4) if n&(1<<j)) for n in range(16)])
assert h*h==s.eye(16)
cv=[creator(v[:,r]) for r in range(4)]
top=s.zeros(16);top[15,0]=1
assert cv[0]*cv[1]*cv[2]*cv[3]==d*top
majoranas=[ci+ci.T for ci in c]
central=s.zeros(16)
for mask in range(16):
    m=s.eye(16)
    for j in range(4):
        if mask&(1<<j): m=m*majoranas[j]
    central+=m*top.T*cv[0]*cv[1]*cv[2]*cv[3]*m.T
assert central==d*s.eye(16)
for r,t in pairs:
    u,w=[j for j in range(4) if j not in (r,t)]
    b=s.LeviCivita(r,t,u,w)*star(wedge(e[:,u],e[:,w]))*eta
    inverse_leg=wedge(v[:,r],v[:,t])*eta/d
    assert b==inverse_leg
    car=(cv[r]*h*cv[t].T*h-cv[t]*h*cv[r].T*h)/d
    assert car==lift(b)
    # All sixteen inverse-leg tangents, with full determinant derivative.
    for i,j in itertools.product(range(4),repeat=2):
        dv=s.zeros(4);dv[i,j]=1
        de=-e*dv.T*eta*e
        dd=d*s.trace(v.inv()*dv)
        db=s.LeviCivita(r,t,u,w)*star(wedge(de[:,u],e[:,w])+wedge(e[:,u],de[:,w]))*eta
        dr=(wedge(dv[:,r],v[:,t])+wedge(v[:,r],dv[:,t]))*eta/d-b*dd/d
        assert db==dr
print('PASS all six Hodge coframe faces from true inverse legs and all 96 first jets')
print('PASS full CAR16 bilinear numerator, actual determinant word and scalar centralization')
# The reciprocal polynomial is exact up to a single controlled remainder.
x=s.symbols('x',nonzero=True)
for orientation in [-1,1]:
    for n in range(6):
        rn=orientation*sum((1-orientation*x)**k for k in range(n+1))
        assert s.simplify(1/x-rn-(1-orientation*x)**(n+1)/x)==0
print('PASS fixed integer-coefficient reciprocal polynomial and signed determinant branch')
# Cheap exact quarter-turn has the desired reference through second order.
t=s.symbols('t',real=True)
j=s.Matrix([[0,-1],[1,0]])
rcheap=s.BlockMatrix([[s.sin(t)*j,s.cos(t)*s.eye(2)],
                       [-s.cos(t)*s.eye(2),-s.sin(t)*j]]).as_explicit()
rcanonical=s.BlockMatrix([[t*j,s.sqrt(1-t*t)*s.eye(2)],
                           [-s.sqrt(1-t*t)*s.eye(2),-t*j]]).as_explicit()
assert s.simplify(rcheap*rcheap)==-s.eye(4)
assert rcheap.T==-rcheap
for order in range(3):
    assert (rcheap-rcanonical).diff(t,order).subs(t,0)==s.zeros(4)
assert (rcheap-rcanonical).diff(t,3).subs(t,0)!=s.zeros(4)
print('PASS exact conjugated quarter-turn differs from canonical Julia reference only at order sigma^3')
# The two exact quarter-turns have the same flat feedback matrix. Therefore
# their paired feedback difference contains a holonomy increment, not a
# coframe-only O(sigma^3) term. This checks the corresponding mixed jet.
q=s.symbols('q',real=True)
vface=s.cos(q)*s.eye(2)+s.sin(q)*j
vpaired=s.diag(vface,vface.T)
def fref(r): return 2*s.eye(4)-r.T*vpaired-vpaired.T*r
df=fref(rcheap)-fref(rcanonical)
assert s.simplify(df.subs(q,0))==s.zeros(4)
for order in range(3):
    assert s.simplify(df.diff(t,order).subs(t,0))==s.zeros(4)
assert df.diff(t,3).diff(q).subs({t:0,q:0})!=s.zeros(4)
print('PASS identical flat feedback and first reference-price defect at sigma^3 times holonomy')
print('FIREWALL: continuous onsite Julia calls and actual work/cut pricing remain physical premises')
