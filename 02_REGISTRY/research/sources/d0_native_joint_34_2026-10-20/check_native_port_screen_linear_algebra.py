#!/usr/bin/env python3
"""Exact real screened-metric subspace of the native L4 port Fourier symbol.
Scope only: algebraic screening of port COST, not unrerun full128 history jets.
"""
import sympy as s
k=s.Matrix([-1+s.I,-1+s.I,-2,-1-s.I])
x=s.symbols('x0:10')
pairs=[(i,j) for i in range(4) for j in range(i,4)]
Q=s.zeros(4)
for y,(i,j) in zip(x,pairs):Q[i,j]=Q[j,i]=y
w=Q*k
M=s.Matrix([s.re(z) for z in w]+[s.im(z) for z in w]).jacobian(x)
assert M.rank()==7 and 10-M.rank()==3
l=s.Matrix([0,1,-1,1])
Qs=l*l.T
assert Qs*k==s.zeros(4,1)
eta=s.diag(1,-1,-1,-1)
t=s.symbols('t', real=True)
F=s.eye(4)+t*eta*Qs
assert (F.T*eta*F).diff(t).subs(t,0)==2*Qs
assert Qs*k==s.zeros(4,1)
# The index placement matters: CAR vector from F in this chart is
# k(F) = F.T eta k, so F(t).T eta k = k+t Qs k =k exactly.
assert s.simplify(F.T*eta*k-k)==s.zeros(4,1)
# The full Dirac symbol is fixed, so any scalar function only of D^2
# (including the complete original Golden port effect) is constant.
print('PASS real symmetric screening rank 7, nullity 3')
print('PASS exact finite-amplitude Qstar=ell ellT screen; coframe metric changes')
print('FIREWALL: no exact native two-round Walsh q(0,17)/q(0,27)/q(0,59) replay')
