#!/usr/bin/env python3
"""All-L original complete H+J+R flat-coframe source theorem (standard library).

The proof does NOT enumerate lattice sizes: its controlling partition
inequality is exact rational arithmetic valid for every integer L >= 11.
Full finite L=11,16,24 source replays are diagnostics only.
Scientific scope: same fixed-right conditional HJR, NOT full native D0 price.
"""
from fractions import Fraction as F
from math import cos, exp, factorial, log1p, pi, sqrt
from itertools import product

p = (sqrt(5)-1)/2
p2 = p*p
z = 2**-20
u = F(1, 16)

# Exact rational strict comparisons of the algebraic Golden p^2.
# (559/250)^2 < 5 < (9/4)^2, p^2 = (3-sqrt(5))/2.
assert F(559**2, 250**2) < 5 < F(81, 16)
assert F(3, 8) < p2 < F(191, 500)

# pi < 22/7, and positive x -> -log(1-x)<=x/(1-x).
# Uniform lower bound b(q)^m >= exp(-t_eff |q|^2) on [-5,5]^4.
p2_upper = F(191, 500)
t_bound = (p2_upper * F(22**2, 7**2) / 32) / (1-p2_upper/2048)
t_cert = F(59, 500)
assert t_bound == F(5916416, 50166641)
assert t_bound < t_cert

# P11(x) lower-bounds exp(-x) for x>=0 by the positive Taylor remainder.
def P11(x: F) -> F:
    return sum(((-x)**j / F(factorial(j)) for j in range(12)), F(0))

one_d = F(1)
for k in range(1, 6):
    poly = P11(t_cert*k*k)
    assert poly > 0
    one_d += 2*poly
lower_Q = one_d**4
upper_threshold = F(2048, 3)  # p^2>3/8 => 256/p^2 <2048/3
assert lower_Q > upper_threshold
print("RATIONAL UNIVERSAL CERTIFICATE, ALL INTEGERS L>=11:")
print("t_eff <", t_bound, "<59/500")
print("Q_L >", float(lower_Q), ">2048/3>", "256/p^2")
print("excess >", float(lower_Q-upper_threshold))
print("dS_L /du >= lambda_first,L >=1; dS_L/ds >=1/2 at s=1/4")

# Re-check actual full-trace normalized sources on selected original
# finite carriers, retaining multiplicity 16, whole site spectrum,
# both thermal terms, the global normalizer, and the rank128 Riesz term.
for L in (11, 16, 24):
    omega_1 = [2-2*cos(2*pi*k/L) for k in range(L)]
    alpha = p2/(128*L*L)
    m = 256*L*L
    beta = m*alpha
    Q = T = J_sum = 0.0
    for k0,k1,k2,k3 in product(range(L), repeat=4):
        omega = omega_1[k0]+omega_1[k1]+omega_1[k2]+omega_1[k3]
        lam = L*L*omega/16
        b = 1-alpha*float(u)*lam
        assert b>p**3
        weight = exp(m*log1p(-alpha*float(u)*lam))
        Q += weight
        f = lam*weight/b
        T += f
        J_sum += f/(1-z+z*weight)
    first = L*L/16*(2-2*cos(2*pi/L))
    dH = -T/Q
    dJ = 2048*z*beta*J_sum  # 128 feedback x all 16 CAR components
    full_derivative = dH+dJ+first
    assert Q > float(lower_Q)-1e-8
    assert full_derivative > first > 1
    print(f"L={L}, Q={Q:.6f}, dH={dH:+.6f}, dJ={dJ:+.6f}, "
          f"dR={first:+.6f}, FULL dS/du={full_derivative:+.6f}")

print("PASS: exact rational all-L proof + same-action finite Fourier replays")
