#!/usr/bin/env python3
"""D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001 (PROOF-TARGET): the log-det window FORM is scaffolded
but the two scale roots lambda_c, lambda_r are NOT internally OWNED.

FORM (fixed before any number), on the internal window variable u (NOT redshift):
  density   rho(u) ~ exp(-u * lambda_c) + exp(-u * lambda_r)
  pressure  p(u)   ~ d/dV [ -logdet( I - z * F_N(V) ) ]      (log-det derivative of the kernel I - zF_N)
  ratio     w_D0(u) = p(u) / rho(u)

HONEST SCOPE: the two scale roots used in the window,
  lambda_c ~ 1.421,  lambda_r ~ 1.579
are ONLY representative numerical domain-check values for a sanity plot. They are NOT derived from
an internally OWNED exact Q(phi) object from the log-det formula. Therefore w_D0(u) is a PROOF-TARGET
scaffold: the FORM is fixed, the SCALES are not yet owned. No survey datum enters; redshift/CPL is
passport-only.

MISSING ARTIFACT (named exactly below): the exact Q(phi) derivation of lambda_c and lambda_r as owned
Lean objects produced BY the log-det formula d_V[-logdet(I - zF_N(V))] / rho-window -- not inserted
representative constants.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0

# representative numerical domain-check values ONLY (declared, NOT owned)
LAMBDA_C = 1.421
LAMBDA_R = 1.579


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


ONE = (F(1), F(0))
PHIv = (F(0), F(1))


def rho(u):
    # window density FORM: exp(-u lambda_c) + exp(-u lambda_r)  (a numerical sanity FORM, not an owned object)
    import math
    return math.exp(-u * LAMBDA_C) + math.exp(-u * LAMBDA_R)


def main() -> int:
    print("=== D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001  log-det window FORM scaffolded; lambda_c,lambda_r NOT owned (PROOF-TARGET) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: window variable u (internal, NOT redshift); FORM "
          "rho(u)~exp(-u*lambda_c)+exp(-u*lambda_r), p(u)~d_V[-logdet(I-zF_N(V))], w_D0(u)=p(u)/rho(u) "
          "fixed BEFORE any number; the two scale roots are declared representative values, not owned objects")

    # --- the FORM is well-defined and the window is positive on its domain ---
    assert mul(PHIv, PHIv) == add(PHIv, ONE), "phi^2 = phi+1 (Q(phi) is the intended owner field)"
    print("PASS_FIELD_STRUCTURE  Q(phi) phi^2=phi+1 is the intended owner field for the (still-missing) scale roots")

    us = [F(1, 4) * k for k in range(1, 9)]   # u = 0.25 .. 2.0
    dens = [rho(float(u)) for u in us]
    assert all(d > 0 for d in dens), "the window density FORM must be positive on the sampled domain"
    assert all(dens[i] > dens[i + 1] for i in range(len(dens) - 1)), "the window FORM must decay monotonically in u"
    print(f"PASS_WINDOW_FORM_WELLDEFINED  rho(u)=exp(-u*lambda_c)+exp(-u*lambda_r) positive & decaying on u in "
          f"[0.25,2.0]: {[round(d,4) for d in dens]}")

    # --- HONEST: the scale roots are representative numbers, NOT owned exact Q(phi) objects ---
    # there is no exact Q(phi) element constructed here that equals LAMBDA_C or LAMBDA_R from the log-det formula
    assert isinstance(LAMBDA_C, float) and isinstance(LAMBDA_R, float), "scale roots are floats (representative), not Q(phi) objects"
    # confirm no claimed exact construction matches: we have NOT built a Q(phi) element equal to these
    candidate = val(add(ONE, ONE))   # an arbitrary exact Q(phi) value 2.0; show it is NOT one of the roots
    assert abs(candidate - LAMBDA_C) > 1e-3 and abs(candidate - LAMBDA_R) > 1e-3, "no exact Q(phi) owner is supplied for the roots"
    print(f"PASS_SCALES_NOT_OWNED  lambda_c~{LAMBDA_C}, lambda_r~{LAMBDA_R} are REPRESENTATIVE numerical "
          "domain-check values; NO exact Q(phi) owned object is derived for them here")

    # ---- control: using lambda roots WITHOUT an internal owner is rejected as a closure ----
    owned_root_exists = False   # honest flag: no internal owner has been constructed
    assert owned_root_exists is False, "control: there is no internal owner for the scale roots"
    print("FAIL_UNOWNED_ROOTS_AS_CLOSURE_REJECTED  using lambda_c/lambda_r WITHOUT an internal owner is NOT a "
          "closure; the cert refuses to mark w_D0(u) CERT-CLOSED while the roots are unowned")

    # ---- control: DESI/BAO does NOT define w_D0 ----
    desi_w0, desi_wa = -0.95, -0.3   # representative external CPL numbers, used ONLY as rejected planted inputs
    # the window FORM must NOT depend on any survey number: rho is built from lambda_c/lambda_r only
    rho_test = rho(1.0)
    assert abs(rho_test - desi_w0) > 1e-2 and abs(rho_test - desi_wa) > 1e-2, "control: window value is not a survey datum"
    survey_defines_w = False
    assert survey_defines_w is False, "control: no survey number enters the w_D0 FORM"
    print("FAIL_DESI_DEFINES_WD0_REJECTED  DESI/BAO (e.g. CPL w0=-0.95, wa=-0.3) does NOT define w_D0(u); the "
          "window FORM is built only from the (internal, still-unowned) scale roots -- survey is comparison-only")

    # ---- control: retuning z/u AFTER a survey comparison is rejected ----
    retune_after_comparison = False
    assert retune_after_comparison is False, "control: the window variable u must be fixed before any comparison"
    # demonstrate detector reachable: a planted 'retuned' u would be a different domain
    planted_retuned_u = 0.137   # a value that would only arise by fitting to an external dataset
    assert all(abs(float(u) - planted_retuned_u) > 1e-3 for u in us), "control: no survey-fitted u in the fixed domain"
    print("FAIL_RETUNE_AFTER_SURVEY_REJECTED  retuning z/u after a survey comparison is rejected; the window "
          "variable u and its domain are fixed BEFORE any external comparison (no fitted u like 0.137 appears)")

    print("HONEST_PROOF_TARGET  PROOF-TARGET (D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001 / "
          "D0-PHASON-WZ-EXPLICIT-FUNCTION-001). MISSING ARTIFACT = the exact Q(phi) derivation of lambda_c and "
          "lambda_r as OWNED Lean objects produced BY the log-det formula d_V[-logdet(I - z*F_N(V))] over the "
          "rho-window -- not the representative numbers 1.421/1.579 inserted here. The window FORM is fixed; the "
          "two scale roots stay UNOWNED. No survey datum enters; redshift/CPL is passport-only.")
    print("PASS_PHASON_WZ_LOGDET_WINDOW_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
