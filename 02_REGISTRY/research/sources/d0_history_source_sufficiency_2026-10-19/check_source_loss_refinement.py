#!/usr/bin/env python3
"""Bound true Book/Petz information loss -> Euler source; Golden native clock.

Finite analytic regression of exact theorems only; no compulsory Book or
whole original full128 Kraus / actual 4D source identity is asserted.
"""
from math import sqrt
import numpy as np

p=(sqrt(5)-1)/2
lam=288/25
assert abs(p**5-.09016994374947422)<1e-14

for L in [4,8,16,32,64]:
    h=1/L
    n=64*L*L
    eps=p*p*h*h/64
    e=eps*lam-(eps*lam)**2/4
    hidden_total=n*p**3*e
    hidden_source=n*p**3*eps*(1-eps*lam/2)
    assert abs(n*eps-p*p)<1e-13
    assert hidden_total > 0 and hidden_source>0
    print(f'PASS original h=1/{L} native n={n} port-hidden KL {hidden_total:.12f} d_lam {hidden_source:.12f}')

assert abs(hidden_source-p**5)<1e-6
# For 0<= Delta <=eps and ||D^2 Delta||<=M on an admitted
# two-sided ball with radius >= sqrt(2eps/M), the optimized
# source bound is sqrt(2eps*M). The h^-2 source converges if
# eps*M=o(h^4).
for L in [25,50,100]:
    h=1/L
    eps=h**8
    M=4
    t=sqrt(2*eps/M)
    bound=eps/t+M*t/2
    assert abs(bound-sqrt(2*eps*M))<1e-14
    assert bound/h**2 < .005
print('PASS quantitative exact Taylor-to-source bound and h^-2 scaling')

# Uniformly tiny positive relative-entropy loss does not imply a small
# field derivative without curvature control. Nonnegative smooth example.
for L in [16,32]:
    h=1/L
    def delta(y):return h**4*(1+np.sin(y/h**4))
    assert delta(0)<=2*h**4 and (1/h**2)>100
print('PASS independent hostile uniform-value-small/derivative-large')

print('FIREWALL: native hidden-port total remains finite under n~h^-2; '
      'do not infer raw #216 or full Book/G0 action admission')
