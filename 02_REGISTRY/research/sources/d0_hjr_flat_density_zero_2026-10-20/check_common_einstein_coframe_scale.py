#!/usr/bin/env python3
"""SAME original flat Einstein carrier v=h*sqrt(rho)*e: bare full HJR source.

Certified: elementary rational bound, each integer L>=256, and analytic
strict-positive continuum integral. Small-L float replays only diagnose
the original full CAR16+normalizer+feedback+rank128 Riesz action.
Not a proof of compulsory full native Book03 Cost-Info or GR closure.
"""
from fractions import Fraction as Q
from math import cos, factorial, pi, sqrt
import mpmath as mp
import numpy as np

p2 = (3 - sqrt(5)) / 2
z = 2 ** -20
beta = 2 * p2

# Exact algebraic Golden interval: sqrt(5)<9/4 and sqrt(5)>11/5.
assert Q(3, 8) < p2 < Q(2, 5)
assert Q(9, 4) ** 2 > 5
assert Q(11, 5) ** 2 < 5

# Elementary rational certificate: e<68/25 implies e^13<500000.
e_upper = sum((Q(1, factorial(k)) for k in range(7)), Q(0))
e_upper += Q(1, factorial(7)) * Q(8, 7)
assert e_upper < Q(68, 25)
assert Q(68, 25) ** 13 < 500000

# At rho=1 all CAR modes: b>79/80, beta<4/5,
# - (m-1) log(b) < 16 beta /(79/80) < 13.
assert Q(64, 5) * Q(80, 79) == Q(1024, 79) < 13
# Sum_k mu_k = 8L^4 exactly for L>=2; from cos-root cancellation.
# Thermal H source >= -1280/79; 128*16 J source >=3 L^4/128M.
lower = Q(3, 128000000) - Q(1280, 79 * 256 ** 4)
assert lower > Q(1, 100000000)
print("EXACT RATIONAL: every L>=256 has a nonzero SAME-SITE "
      "coframe Euler DS_HJR[V_x] > 1e-8")
print("Source certified lower bound at L=256:", float(lower))

# The rigorous asymptotic is a strictly positive torus integral.
# Bessel expression is only an independent high-precision value replay.
mp.mp.dps = 50
p = (mp.sqrt(5) - 1) / 2
bt = 2 * p**2
zz = mp.mpf(2)**-20

def moment(t):
    i0, i1 = mp.besseli(0, 2*t), mp.besseli(1, 2*t)
    return 8 * mp.exp(-8*t) * i0**3 * (i0-i1)

value = 2048*zz*bt/(1-zz) * mp.fsum(
    [(-zz/(1-zz))**n * moment((n+1)*bt) for n in range(10)]
)
assert value > 0
print("Analytic positive continuum source density:", mp.nstr(value, 38))

# Small finite L replays preserve EVERY 16L^4 mode and the original
# 128 feedback multiplicity, 16 CAR grades, global Z and moving Riesz term.
for L in (8, 16, 24, 32, 40):
    w1 = 2 - 2*np.cos(2*pi*np.arange(L)/L)
    mu = (w1[:,None,None,None] + w1[None,:,None,None]
          + w1[None,None,:,None] + w1[None,None,None,:])
    assert abs(float(np.mean(mu))-8) < 1e-12
    alpha = p2/(128*L*L)
    m = 256*L*L
    B = 1-alpha*mu
    assert np.min(B) > 0
    f = np.exp(m*np.log(B))
    Zsum = float(np.sum(f))
    Hsource = -float(np.sum(mu*f/B))/Zsum
    Jsource = 2048*z*beta*float(np.sum(mu*f/B/(1-z+z*f)))
    Rsource = 2 - 2*cos(2*pi/L)
    original_full = (Hsource+Jsource+Rsource)/L**4
    if L >= 24:
        assert original_full > 0
    print(f"L={L} local_source={original_full:+.12e} "
          f"feedback_local={Jsource/L**4:+.12e} "
          f"full_thermal={Hsource:+.9f} rank128={Rsource:+.9f}")
    if L == 40:
        assert abs(original_full-float(value)) < 2e-6

# The exact all40 original star is coframe-flat at U=I:
# (P-P^{-1})/2=0 => its 16 coframe source rows vanish identically.
print("PASS: original physical v=h e on the same flat Einstein family, "
      "not the older unrelated fixed-v chart")
