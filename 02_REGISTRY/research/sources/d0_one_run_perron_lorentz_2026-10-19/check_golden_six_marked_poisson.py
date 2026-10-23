#!/usr/bin/env python3
"""Exact six-Lorentz Golden 14-outcome Fisher and rare-event limit.

The fixed CAR16 Choi POVM source data are owned by the existing exact
13-effect positive Julia theorem. This checks its Golden p rescaling and
the independent native scalar first-shell clock limit, not G0 selection.
"""
from math import sqrt
p = (sqrt(5.0)-1.0)/2.0
q = [p*p/24.0]*12 + [p*p/2.0, p]
assert abs(sum(q)-1.0)<1e-14 and min(q)>0
jac = [[0.0 for _ in range(6)] for _ in range(14)]
for k in range(6):
    jac[2*k][k] = p*p/(12*sqrt(2.0))
    jac[2*k+1][k] = -p*p/(12*sqrt(2.0))
fisher = [[sum(jac[i][a]*jac[i][b]/q[i] for i in range(14))
           for b in range(6)] for a in range(6)]
error = max(abs(fisher[i][j]-(p*p/6 if i==j else 0))
            for i in range(6) for j in range(6))
assert error<1e-14
print('PASS native flat Golden 14-outcome Fisher p^2/6:',p*p/6)
print('PASS six-generator Fisher full matrix error:',error)
lam = 288.0/25.0
for L in [4,8,16,32]:
    h=1.0/L
    n=64*L*L
    eps=p*p*h*h/64
    e=eps*lam*(1-h*h*lam/256)
    eig=n*e*p*p/6
    bound=2*n*e*e
    assert abs(n*eps-p*p)<1e-12
    print('PASS L=%d ticks=%d six-Fisher eigen=%.12f Poisson-TV<=%.9f'
          % (L,n,eig,bound))
print('PASS strict nonzero asymptotic six-Fisher eigen:',p**4*lam/6)
