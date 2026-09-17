#!/usr/bin/env python3
"""D0-PHI-LADDER-SEMIGROUP-001 — the phi-tick ladder and its unique continuum semigroup envelope.

The detector-clock split is p = phi^-1 with p + p^2 = 1. The finite tick ladder
    A_{n+1} = p A_n,   B_{n+1} = B_n + p^2 A_n
solves to A_n = A_0 phi^-n, B_n = (1 - phi^-n) A_0, R_n = B_n/A_n = phi^n - 1. Its unique continuum
envelope is A(s) = A_0 exp(-s log phi), with the semigroup law A(s+t) = A(s) A(t) / A_0. This is the
FIRST D0 continuum -- the continuous envelope of a certified discrete self-similar tick -- NOT yet a
smooth-manifold theorem (that stays the Rieffel/GHP + Connes owner-edge).

Backing: the integer ladder Q(D)=phi^(D-4) is CORE (D0-DIM-LADDER-COMPACT-001); the golden split
W_ext=phi^-1 / W_int=phi^-2 is CORE (D0-IM-002); the envelope cocycle is Lean-proved
(D0.IM.ContinuumFromFractalTick.env_cocycle / env_restricts_to_ladder, D0-IM-003). This cert is the
sprint's consolidated can-FAIL statement of the ladder + envelope.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


# exact ℚ(φ): (a,b) = a + b·φ, φ² = φ + 1
def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


ONE = (F(1), F(0))
PHIv = (F(0), F(1))
P = (F(-1), F(1))      # p = φ⁻¹ = φ − 1
P2 = (F(2), F(-1))     # p² = φ⁻² = 2 − φ


def powp(x, n):
    out = ONE
    for _ in range(n):
        out = mul(out, x)
    return out


def main() -> int:
    print("=== D0-PHI-LADDER-SEMIGROUP-001  phi-tick ladder + unique continuum semigroup envelope ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: p=phi^-1 with p+p^2=1 (golden split, M1-forced); the tick ladder and "
          "its continuous envelope are fixed before any value")

    # golden split p + p^2 = 1
    assert add(P, mul(P, P)) == ONE, "golden split p + p^2 = 1 must hold"
    print("PASS_GOLDEN_SPLIT  p + p^2 = 1 with p = phi^-1 (W_ext=phi^-1, W_int=phi^-2)")

    # discrete ladder: A_n = phi^-n solves A_{n+1}=p A_n; B_n=1-phi^-n solves B_{n+1}=B_n+p^2 A_n; R_n=phi^n-1
    for n in range(0, 16):
        A_n = powp(P, n)               # A_0 = 1
        A_n1 = powp(P, n + 1)
        assert A_n1 == mul(A_n, P), f"A_(n+1)=p A_n must hold at n={n}"
        B_n = sub(ONE, A_n)
        B_n1 = sub(ONE, A_n1)
        assert B_n1 == add(B_n, mul(P2, A_n)), f"B_(n+1)=B_n+p^2 A_n must hold at n={n}"
        R_n = sub(powp(PHIv, n), ONE)  # R_n = phi^n - 1
        # consistency R_n = B_n/A_n  <=>  R_n * A_n = B_n
        assert mul(R_n, A_n) == B_n, f"R_n = phi^n - 1 must equal B_n/A_n at n={n}"
    print("PASS_DISCRETE_LADDER  A_n=phi^-n, B_n=1-phi^-n, R_n=phi^n-1 solve the tick recurrences exactly (n=0..15)")

    # continuum envelope A(s)=A0 exp(-s log phi): restricts to integers + semigroup law
    A0 = 3.0

    def env(s):
        return A0 * math.exp(-s * math.log(PHI))

    for n in range(0, 8):
        assert abs(env(n) - A0 * PHI ** (-n)) < 1e-9, f"envelope must restrict to A0 phi^-n at n={n}"
    for s, t in ((1.3, 2.1), (0.0, 4.7), (-1.2, 3.4)):
        assert abs(env(s + t) - env(s) * env(t) / A0) < 1e-9, f"semigroup A(s+t)=A(s)A(t)/A0 must hold at {s},{t}"
    print("PASS_CONTINUUM_ENVELOPE  A(s)=A0 exp(-s log phi) restricts to A0 phi^-n on integers; A(s+t)=A(s)A(t)/A0")

    # ---- negative controls (must FAIL the forced structure) ----
    r = F(3, 2)  # an arbitrary ratio != phi^-1
    assert add((r, F(0)), mul((r, F(0)), (r, F(0)))) != ONE, "control: ratio 3/2 must break p+p^2=1"
    print("FAIL_ARBITRARY_RATIO_REJECTED  r=3/2 (!= phi^-1) breaks p+p^2=1 (the split is forced, not chosen)")

    # additive ladder A_n = A_0 + n does NOT satisfy the multiplicative semigroup
    add_env = lambda s: A0 + s
    assert abs(add_env(1.3 + 2.1) - add_env(1.3) * add_env(2.1) / A0) > 1e-6, \
        "control: an additive ladder must fail the multiplicative semigroup law"
    print("FAIL_ADDITIVE_LADDER_REJECTED  A_n=A0+n fails A(s+t)=A(s)A(t)/A0 (the envelope is multiplicative, not additive)")

    # an external continuum base b != phi breaks the integer restriction tie to the phi-ladder
    b = math.e
    assert abs((A0 * b ** (-1.0)) - A0 * PHI ** (-1.0)) > 1e-3, "control: base b=e != phi gives a different envelope"
    print("FAIL_EXTERNAL_BASE_REJECTED  base b=e != phi gives a different envelope (the base is forced to phi)")

    print("HONEST_FIRST_CONTINUUM  this is the phi-ladder continuum envelope (the FIRST D0 continuum); the smooth-manifold "
          "limit stays the Rieffel/GHP + Connes owner-edge (D0-SMOOTH-MANIFOLD-PASSPORT-001), NOT claimed here.")
    print("PASS_PHI_LADDER_SEMIGROUP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
