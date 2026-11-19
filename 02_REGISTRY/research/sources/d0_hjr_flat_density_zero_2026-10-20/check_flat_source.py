#!/usr/bin/env python3
"""Original L8 CAR16 H+J+R: flat-holonomy coframe-source diagnostic.

Pure Python independent algebra/counting check. This test never declares the
HJR candidate to be the compulsory D0 physical action or a GR solution.
"""
from collections import Counter
from itertools import product
from math import exp, log, log1p, sqrt

L = 8
H = 1 / L
P = (sqrt(5) - 1) / 2  # phi^-1
ALPHA = P * P * H * H / 128
M = 16384
BETA = M * ALPHA  # 2*p^2 at L=8
ZETA = 2**-20
CAR_DIM = 16
HILBERT_DIM = CAR_DIM * L**4

# Exact eigenvalue lambda(q,s) = s^2 * 4*(A+B*sqrt(2)) in Z[sqrt(2)].
# Each 1D (2-2cos(2*pi*k/8)) is one of these exact pairs.
PAIR = ((0, 0), (2, -1), (2, 0), (2, 1), (4, 0),
        (2, 1), (2, 0), (2, -1))
hist = Counter()
for q in product(range(L), repeat=4):
    a = sum(PAIR[k][0] for k in q)
    b = sum(PAIR[k][1] for k in q)
    hist[(4*a, 4*b)] += CAR_DIM

assert sum(hist.values()) == HILBERT_DIM == 65536
assert hist[(0, 0)] == CAR_DIM
# Exactly the eight first-shell momenta (+/- unit in one coordinate) x CAR16.
assert hist[(8, -4)] == 128
assert all((a, b) == (0, 0) or a+b*sqrt(2) > 8-4*sqrt(2)-1e-12
           for (a, b) in hist)
trace_a = sum(n*a for (a, b), n in hist.items())
trace_b = sum(n*b for (a, b), n in hist.items())
assert (trace_a, trace_b) == (2097152, 0)
mean_lambda = trace_a/HILBERT_DIM
assert mean_lambda == 32
occ_lambda = 8-4*sqrt(2)

# At U=I, every original based-face P=I and six-face Palatini f_i=0,
# independent of all invertible coframes v_r=s*e_r/4 (s>0).
# The same full conditional H+J+R action has
# S(u) = log(C*Tr B(u)^M)/BETA -128 Tr log(1-ZETA+ZETA B(u)^M)
#        + u*occ_lambda, B(u)=I-ALPHA*u*Delta0, u=s^2.
# Its exact RIGHT-I_128/128 Riesz preparation is the complete first shell.
# For u->0+ (only a computational extension; u=0 has degenerate coframe),
# dS/du = -Tr Delta0/N + 128*ZETA*BETA*Tr Delta0 + occ_lambda.
leading = -mean_lambda + 128*ZETA*BETA*trace_a + occ_lambda
radical = 744 - 256*sqrt(5) - 4*sqrt(2)
assert abs(BETA-2*P*P) < 1e-14
assert abs(leading-radical) < 1e-9
# Rigorous strict sign with sqrt(5)<9/4 and sqrt(2)<3/2:
# leading > 744 -256*(9/4) -4*(3/2) = 162.
assert leading > 162

spec = Counter({a+b*sqrt(2): n for (a, b), n in hist.items()})
assert len(spec) == len(hist)

def native_action_jet(s):
    """Unmodified complete trace, normalizer and moving first-shell R term."""
    u = s*s
    weights = {v: exp(M*log1p(-ALPHA*u*v)) for v in spec}
    Z = sum(n*weights[v] for v, n in spec.items())
    Hpart = (log(Z)-log(HILBERT_DIM))/BETA  # C cancels, constant in g
    Jpart = -128*sum(n*log1p(ZETA*(weights[v]-1))
                    for v, n in spec.items())
    Rpart = u*occ_lambda
    # Correct derivative of global log Z; not a fixed-normalizer surrogate.
    weighted = sum(n*v*weights[v]/(1-ALPHA*u*v)
                   for v, n in spec.items())
    dH = -weighted/Z
    dJ = 128*ZETA*BETA*sum(
        n*v*weights[v]/((1-ALPHA*u*v)*(1-ZETA+ZETA*weights[v]))
        for v, n in spec.items())
    return Hpart+Jpart+Rpart, dH+dJ+occ_lambda

for s in (0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1):
    val, jet = native_action_jet(s)
    print(f's={s:.3f}: DeltaS={val:+.12f}; dS/d(s^2)={jet:+.9f}')
    if s == 0.01:
        assert 165.3 < jet < 165.5  # independent real point, not coframe collapse
assert abs(native_action_jet(0.01)[0]/1e-4-leading) < 1
print('PASS: complete flat spectrum', HILBERT_DIM,
      'occupied=128, first shell', occ_lambda)
print('EXACT analytic leading source = 744 - 256*sqrt(5) - 4*sqrt(2) =', radical)
print('PASS: nonzero flat-holonomy coframe source; no unqualified F(f_i) representation')
