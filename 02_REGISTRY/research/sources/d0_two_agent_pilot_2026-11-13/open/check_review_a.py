#!/usr/bin/env python3
"""Exact hostile controls for reviewing A; standard library only."""
from fractions import Fraction as Q
import json

checks = []
def need(condition, name):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

# L=(1,2): the Euclidean Moore-Penrose solution need not minimize the
# maximum-block operator norm, even though both are right inverses.
L = (Q(1), Q(2))
C_euclid = (Q(1,5), Q(2,5))
C_max = (Q(1,3), Q(1,3))
def LC(c): return sum(x*y for x,y in zip(L,c))
def infnorm(c): return max(abs(x) for x in c)
need(LC(C_euclid) == 1 and LC(C_max) == 1, 'both covering maps are exact')
need(infnorm(C_max) == Q(1,3) < infnorm(C_euclid) == Q(2,5),
     'Euclidean pseudoinverse need not minimize the max-block norm')
need(sum(abs(x) for x in L) * infnorm(C_max) == 1,
     'triangle lower bound certifies the max-block minimum')

# Two unit block tests on a max norm direct sum have dual norm two, not sqrt(2).
need(Q(1)+Q(1) == 2, 'two unit rows have max-block dual norm 2')
need(2*2 > 2, 'that dual norm exceeds the Hilbert sqrt-two estimate')

# Covering the whole space with I while the physical lift grows still needs
# the physical lift norm in the final normalized source budget.
for t in (Q(1), Q(10), Q(100), Q(1000)):
    lift = (Q(1), t)
    r = (Q(0), Q(1)/t)
    need(sum(x*y for x,y in zip(lift,r)) == 1, 'lifted residual remains 1 at t='+str(t))
    need((1+t*t)/(t*t) >= 1, 'lift norm times residual norm remains >=1 at t='+str(t))

print(json.dumps({'status':'PASS', 'checks':len(checks), 'check_names':checks,
                  'scope':'exact norm and normalization controls, not H.1 physical price',
                  'GR_closed':False},ensure_ascii=False,sort_keys=True,indent=2))
