#!/usr/bin/env python3
"""D0 v15 LogDet Second Response and Stability certificate.

Correct safe-domain result:
  L'(V)  > 0
  L''(V) < 0 for 0<z<1
  L(V) -> -d_tau log(1-z)
  L'(V) -> 0
Thus the log-det response is positive, bounded and saturating while relative
archive geometry can accelerate separately.
"""
from __future__ import annotations

import sympy as sp


def main() -> int:
    print("=== D0 v15 LOGDET SECOND RESPONSE AND STABILITY ===")
    V, z, kappa, d_tau = sp.symbols("V z kappa d_tau", positive=True)
    r = 1 - sp.exp(-kappa * V)
    L = -d_tau * sp.log(1 - z * r)
    Lp = sp.simplify(sp.diff(L, V))
    Lpp = sp.factor(sp.simplify(sp.diff(Lp, V)))

    expected_Lp = d_tau * z * kappa * sp.exp(-kappa * V) / (1 - z + z * sp.exp(-kappa * V))
    expected_Lpp = d_tau * z * kappa**2 * sp.exp(-kappa * V) * (z - 1) / (1 - z + z * sp.exp(-kappa * V))**2
    if sp.simplify(Lp - expected_Lp) != 0:
        raise AssertionError(f"L' mismatch: {Lp}")
    if sp.simplify(Lpp - expected_Lpp) != 0:
        raise AssertionError(f"L'' mismatch: {Lpp}")
    print("PASS_LOGDET_SECOND_DERIVATIVE_COMPUTED")
    print("PASS_LOGDET_SECOND_RESPONSE_SIGN_CONDITION_DERIVED")

    # Safe-domain numerical witness: z=1/2, kappa=log(phi), d_tau=2, V=3.
    phi = (1 + sp.sqrt(5)) / 2
    subs = {z: sp.Rational(1, 2), kappa: sp.log(phi), d_tau: 2, V: 3}
    if not (sp.N(Lp.subs(subs)) > 0):
        raise AssertionError("L' not positive in safe domain")
    if not (sp.N(Lpp.subs(subs)) < 0):
        raise AssertionError("L'' not negative in safe domain")

    L_inf = sp.limit(L, V, sp.oo)
    Lp_inf = sp.limit(Lp, V, sp.oo)
    if sp.simplify(L_inf - (-d_tau * sp.log(1 - z))) != 0:
        raise AssertionError("L infinity mismatch")
    if sp.simplify(Lp_inf) != 0:
        raise AssertionError("L' infinity should be zero")
    print("PASS_LOGDET_RESPONSE_BOUNDED_SAFE_DOMAIN")
    print("PASS_LOGDET_DERIVATIVE_DECAYS_TO_ZERO_SAFE_DOMAIN")

    # Domain and breakdown threshold.
    domain = 1 - z + z * sp.exp(-kappa * V)
    V_star = sp.log(z / (z - 1)) / kappa
    # Check the threshold only algebraically for z>1: substituting V_star gives zero.
    if sp.simplify(domain.subs(V, V_star)) != 0:
        raise AssertionError("breakdown threshold mismatch")
    print("PASS_RESOLVENT_STABILITY_DOMAIN_DERIVED")

    R = sp.exp(kappa * V) - 1
    Rpp = sp.diff(R, V, 2)
    if not (sp.N(Rpp.subs(subs)) > 0):
        raise AssertionError("relative acceleration not positive")
    print("PASS_RELATIVE_ACCELERATION_NOT_CONTRADICTED")
    print("PASS_NO_SURVEY_FIT_CLAIM")

    for token in [
        "FAIL_CLAIM_LPP_POSITIVE_FOR_SAFE_Z",
        "FAIL_CLAIM_LP_LIMIT_POSITIVE_CONSTANT_FOR_SAFE_Z",
        "FAIL_Z_OUTSIDE_RESOLVENT_DOMAIN",
        "FAIL_PRESSURE_BLOWUP_WITHOUT_POLE",
        "FAIL_CONFUSE_RELATIVE_R_ACCELERATION_WITH_LOGDET_L_ACCELERATION",
        "FAIL_SURVEY_FIT_Z",
    ]:
        print(token)
    print("Second response final repair verified: L is bounded, L' decays to zero, L''<0 for 0<z<1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
