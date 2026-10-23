#!/usr/bin/env python3
"""Original D0 full Golden17: inversion, exact Chernoff and native Fisher.
Consumes owner: 12 marked genuine positive outcomes plus 5 individually
inversion-even complementary (including Bell failure). NOT full Book action.
"""
import sympy as s
from math import log,ceil
E=lambda i,j:s.eye(4)[:,i]*s.eye(4)[j,:]
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
G=[E(1,2)+E(2,0),E(1,3)+E(3,0),E(0,2)+E(2,1),E(0,3)+E(3,1),E(2,3)-E(3,2),E(1,1)-E(0,0)]
p=(s.sqrt(5)-1)/2
c=s.simplify(p**4/(24*4096))
I=s.eye(4);tr=s.trace
assert all(a.T*eta+eta*a==s.zeros(4) for a in G)
assert s.Matrix([[tr(a.T*b) for b in G] for a in G])==2*s.eye(6)
x,y=s.symbols('x y',real=True)
def nil(g,t):
    assert g**3==s.zeros(4)
    return I+t*g+t*t*g*g/2
P=nil(G[0],x)*nil(G[3],y)*nil(G[0],-x)*nil(G[3],-y)
Pi=eta*P.T*eta
assert s.simplify(P.T*eta*P-eta)==s.zeros(4)
assert s.simplify(P*Pi-I)==s.zeros(4)
F=s.simplify((P-Pi)/2)
assert s.simplify(F-s.Add(*[tr(a.T*P)*a/2 for a in G]))==s.zeros(4)
assert all(s.simplify(tr(a.T*Pi)+tr(a.T*P))==0 for a in G)
tau=tr(P)/4
u=[tr(a.T*P)/(2*s.sqrt(2)) for a in G]
pos=[c*(tau+t)**2 for t in u]
neg=[c*(tau-t)**2 for t in u]
amp=[2*s.sqrt(c)*t for t in u] # positive original amplitude branch
j=s.simplify(sum(t*t for t in amp))
fn=s.simplify(tr(F.T*F))
assert s.simplify(j-c*fn)==0
# All FIVE native complementary categories are individually inversion-even
# in the consumed Golden17 owner. Their full positive sum is retained here.
rest=s.simplify(1-sum(pos+neg))
aff=s.simplify(rest+sum(2*c*(tau*tau-t*t) for t in u))
assert s.simplify(aff-(1-j))==0
assert s.simplify(aff-(1-c*fn))==0
for ga in G:
    t=s.symbols('t',real=True);Q=I+t*ga;tt=tr(Q)/4
    uu=[tr(g.T*Q)/(2*s.sqrt(2)) for g in G]
    prob=[c*(tt+v)**2 for v in uu]+[c*(tt-v)**2 for v in uu]
    fisher=s.simplify(sum(s.diff(v,t).subs(t,0)**2/v.subs(t,0) for v in prob))
    assert s.simplify(fisher-4*c)==0
assert s.simplify(s.diff(P,x,y).subs({x:0,y:0})-G[4])==s.zeros(4)
assert s.simplify(s.diff(j,x,2,y,2).subs({x:0,y:0})-8*c)==0
u0={x:s.Rational(1,10),y:s.Rational(1,13)}
assert all(float(q.subs(u0))>0 for q in pos+neg)
assert float(rest.subs(u0))>0
B=float(aff.subs(u0));d=.1
assert 0<B<1 and abs(B+float(j.subs(u0))-1)<1e-12
necessary=ceil(log(4*d*(1-d))/(2*log(B)))
sufficient=ceil(log(2*d)/log(B))
assert 0<necessary<=sufficient
print('PASS original proper SO 6 generators, all native positive amplitudes')
print('PASS full 17-outcome inversion/Hellinger and exact Chernoff expression')
print('PASS exact 4c*I6 Fisher, real based commutator and native h^-4 bound')
print({'c':float(c),'affinity':B,'curvature_norm_sq':float(fn.subs(u0)),
       'fisher_per_axis':float(4*c),'min_required_runs':necessary,
       'sufficient_runs':sufficient})
print('GR_closed=false; Book Info/admission source not selected.')
