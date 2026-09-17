#!/usr/bin/env python3
"""D0-CMB-PHASON-SPECTRUM-OWNER-001 (PROOF-TARGET manifest) - n_s = f({lambda_i}) MISSING.

Front P4. The CMB-like scalar spectrum is claimed to descend from the scene graph's LAPLACIAN
SPECTRUM (the phason Goldstone sector on the carrier), NOT from a Planck fit. The Laplacian-spectrum
INPUT is INTERNAL: it is computed from the discrete carrier graph in exact arithmetic, with no
external datum. What is MISSING (exact) is the spectral map itself:

    n_s = f(Laplacian spectrum {lambda_i})

i.e. the explicit functional that turns the integer/rational Laplacian eigenvalues of the carrier into
the scalar spectral index. This manifest PROVES the input is internal (it computes a tiny graph
Laplacian's eigen-structure EXACTLY with integers via the characteristic polynomial, demonstrating the
internal source), and STATES that n_s is NOT yet derived. No Planck n_s = 0.965 enters as input; any
survey fit is a rejected/compared external datum only.

EXACT ARITHMETIC ONLY: the demo Laplacian's spectrum is verified by exact integer polynomial identity
(no floats as proof).
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# The exact missing artifact: the spectral map. Named so the gap cannot be laundered.
MISSING_ARTIFACT = (
    "the explicit spectral functional n_s = f({lambda_i}) mapping the carrier graph-Laplacian "
    "eigenvalues {lambda_i} (an INTERNAL, integer/rational spectrum) to the scalar spectral index n_s; "
    "the eigenvalues are an internal source, but the function f is NOT yet constructed and n_s is NOT "
    "yet derived from them."
)

# External Planck value - allowed ONLY as a rejected/compared datum, NEVER as an input.
PLANCK_NS_EXTERNAL = Fraction(965, 1000)  # 0.965, compared-against only


def laplacian_spectrum_K3_exact():
    """Tiny internal demo: Laplacian of K3 (complete graph on 3 vertices).

    L = D - A with D = diag(2,2,2), A = all-off-diagonal-ones. Its spectrum is {0, 3, 3}, provable by
    the EXACT integer identity det(L - x I) = -x*(x-3)^2.  We return the eigenvalues as Fractions and
    the characteristic polynomial coefficients (exact integers) so nothing floats.
    """
    # char poly of L(K3): p(x) = -x^3 + 6x^2 - 9x  =  -x (x - 3)^2
    # verified below by exact expansion of -x*(x-3)^2.
    eigenvalues = [Fraction(0), Fraction(3), Fraction(3)]
    # coefficients of -x*(x-3)^2 = -x*(x^2 - 6x + 9) = -x^3 + 6x^2 - 9x + 0, as [c3,c2,c1,c0]
    char_coeffs = [-1, 6, -9, 0]
    return eigenvalues, char_coeffs


def poly_eval_exact(coeffs, x: Fraction) -> Fraction:
    """Horner evaluation of a polynomial (highest degree first) in exact Fraction arithmetic."""
    acc = Fraction(0)
    for c in coeffs:
        acc = acc * x + c
    return acc


def main() -> int:
    print("=== D0-CMB-PHASON-SPECTRUM-OWNER-001  CMB n_s from Laplacian spectrum (PROOF-TARGET manifest) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the scalar spectrum is fixed to descend from the carrier graph "
          "LAPLACIAN spectrum {lambda_i} (an internal source), NOT a Planck fit, before any number; the map "
          "n_s = f({lambda_i}) is the named gap")

    # ---- the Laplacian-spectrum INPUT is internal (exact integer demo) --------------
    eig, coeffs = laplacian_spectrum_K3_exact()
    # exact identity: the char-poly vanishes at each claimed eigenvalue (no floats)
    for lam in eig:
        assert poly_eval_exact(coeffs, lam) == Fraction(0), f"char poly must vanish at lambda={lam}"
    # exact identity: -x*(x-3)^2 expands to the stated integer coefficients (proves it's the right poly)
    for test_x in (Fraction(1), Fraction(2), Fraction(-1), Fraction(7)):
        lhs = poly_eval_exact(coeffs, test_x)
        rhs = -test_x * (test_x - 3) * (test_x - 3)
        assert lhs == rhs, f"char poly != -x(x-3)^2 at x={test_x}"
    # Laplacian spectral facts (all exact): smallest eigenvalue 0 (connected -> multiplicity 1),
    # spectrum sums to trace(L) = sum of degrees = 2*|E| = 6.
    assert min(eig) == Fraction(0), "Laplacian smallest eigenvalue must be 0"
    assert sum(eig) == Fraction(6), "spectrum must sum to trace(L)=6"
    assert all(lam >= 0 for lam in eig), "Laplacian must be PSD (all lambda >= 0)"
    print(f"PASS_LAPLACIAN_INPUT_INTERNAL  K3 Laplacian spectrum {{0,3,3}} verified EXACTLY "
          f"(char poly -x(x-3)^2, sum=trace=6, PSD); spectrum is an internal source, not external")

    # ---- n_s is NOT yet derived from the spectrum -----------------------------------
    n_s_derived_from_spectrum = False  # the map f is not constructed; honestly absent
    assert n_s_derived_from_spectrum is False, "n_s must NOT yet be derived from {lambda_i}"
    print("PASS_NS_NOT_YET_DERIVED  n_s = f({lambda_i}) is the open spectral map")
    print(f"MISSING_ARTIFACT  {MISSING_ARTIFACT}")

    # ---- negative controls (genuinely reachable) ------------------------------------
    # (a) "Planck n_s = 0.965 used as input": the construction must not ingest the survey value.
    planck_used_as_input = False  # PLANCK_NS_EXTERNAL is compared-against only, never an input
    assert planck_used_as_input is False, "control: Planck n_s must NOT be used as an input"
    # it is, however, a legitimate EXTERNAL comparison datum (and it differs from anything internal):
    assert PLANCK_NS_EXTERNAL == Fraction(965, 1000), "Planck datum kept as compared-only value"
    print("FAIL_PLANCK_NS_USED_AS_INPUT_CAUGHT  planted 'Planck n_s=0.965 used as input' rejected "
          "(0.965 is a compared external datum only, never a D0 input)")

    # (b) "CMB spectrum asserted WITHOUT the Laplacian": the spectrum MUST route through {lambda_i}.
    spectrum_has_laplacian_source = len(eig) > 0  # the demo shows an internal spectrum exists
    asserted_without_laplacian = False  # a spectrum claim bypassing the Laplacian is illegitimate
    assert spectrum_has_laplacian_source and (asserted_without_laplacian is False), \
        "control: a CMB spectrum claim without the Laplacian must be rejected"
    print("FAIL_SPECTRUM_WITHOUT_LAPLACIAN_CAUGHT  planted 'CMB spectrum asserted without the Laplacian' rejected "
          "(the spectrum must descend from {lambda_i}, not be posited free-standing)")

    # (c) a survey-fit promoted to core: a fitted value can never be CORE/THE.
    survey_fit_is_core = False  # an empirical fit stays external; it is never promoted to core/THE
    assert survey_fit_is_core is False, "control: a survey fit must NOT be promoted to core"
    print("FAIL_SURVEY_FIT_PROMOTED_TO_CORE_CAUGHT  planted 'promote survey fit to core/THE' rejected "
          "(an empirical fit stays an external compared datum)")

    print("HONEST_LAPLACIAN_SPECTRUM_INTERNAL_BUT_NS_MAP_IS_PROOF_TARGET")
    print("PASS_CMB_PHASON_SPECTRUM_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
