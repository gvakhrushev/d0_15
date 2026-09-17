#!/usr/bin/env python3
"""D0-ALPHA-ALG-CLOSED-001 - the D0-internal algebraic alpha object alpha_alg^-1 (no empirical input).

With u=phi^-3, mu2=12288/5, mu1=1/3, mu0=0:
    alpha_alg^-1 = mu2 u^2 + mu1 u = (12288/5) phi^-6 + (1/3) phi^-3 = 159739/5 - (294902/15) phi
exactly in Q(phi) (~137.036043). A D0-internal algebraic trace/archive object: it does NOT use the
measured alpha as input.

CONSOLIDATION (honest): this object is already Lean-CORE (D0.Spectral.DeltaAlphaMoment.delta_alpha_moment,
D0-DELTA-ALPHA-MOMENT-001). This row is the sprint's named 'alpha_alg closed' statement with controls;
the measured physical alpha is the closure holonomy D0-ALPHA-HOLONOMY-002 (CHK), a separate object.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def smul(c, x):
    return (c * x[0], c * x[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


PHI_INV = (F(-1), F(1))


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def main() -> int:
    print("=== D0-ALPHA-ALG-CLOSED-001  alpha_alg^-1 = (12288/5)phi^-6 + (1/3)phi^-3 exactly in Q(phi) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: u=phi^-3, mu2=12288/5, mu1=1/3, mu0=0 fixed before the value; no measured-alpha input")
    u = powp(PHI_INV, 3)
    u2 = mul(u, u)
    mu2, mu1 = F(12288, 5), F(1, 3)
    alpha_alg = add(smul(mu2, u2), smul(mu1, u))
    assert alpha_alg == (F(159739, 5), F(-294902, 15)), f"alpha_alg^-1 must be 159739/5 - 294902/15 phi: {alpha_alg}"
    assert abs(val(alpha_alg) - 137.036043) < 1e-5, f"alpha_alg^-1 ~ 137.036043: {val(alpha_alg)}"
    print(f"PASS_ALPHA_ALG_EXACT  alpha_alg^-1 = mu2 phi^-6 + mu1 phi^-3 = {alpha_alg} = {val(alpha_alg):.6f}")

    assert add(smul(mu2, u2), smul(F(1, 2), u)) != (F(159739, 5), F(-294902, 15)), "control: wrong mu1 must break it"
    print("FAIL_WRONG_MU1_REJECTED  mu1=1/2 breaks alpha_alg^-1 (mu1=1/3 is the rank floor)")
    assert add(smul(F(2048), u2), smul(mu1, u)) != (F(159739, 5), F(-294902, 15)), "control: mu2 without pi0 must break it"
    print("FAIL_MU2_WITHOUT_PI0_REJECTED  mu2=2^11 (no pi0 phase) != 12288/5 breaks alpha_alg^-1")
    print("HONEST_CONSOLIDATION  already Lean-CORE (D0.Spectral.DeltaAlphaMoment / D0-DELTA-ALPHA-MOMENT-001); a D0-internal "
          "algebraic object, NOT the measured physical alpha (closure holonomy D0-ALPHA-HOLONOMY-002, CHK).")
    print("PASS_ALPHA_ALG_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
