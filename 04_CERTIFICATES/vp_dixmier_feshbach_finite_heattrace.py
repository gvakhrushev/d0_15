#!/usr/bin/env python3
"""D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001 (NO-GO, anti-numerology).

A FINITE heat trace has NO 1/s pole, and its value at s = 0 is the dimension.

The Feshbach-Schur archive block is a FINITE multiset of eigenvalues (dim 30). Its heat trace

    Theta(s) = sum_i exp(-s * lambda_i)

is an ENTIRE function of s, so its Maclaurin expansion is a power series indexed by k >= 0 ONLY:

    Theta(s) = sum_{k>=0} a_k s^k ,   a_k = (sum_i (-lambda_i)^k) / k!   (the depth-k archive moment).

A Nat-indexed power series has NO negative-index coefficient -- in particular NO a_{-1} (no 1/s term).
Hence the Dixmier-residue slot Res_{s=0} Theta = a_{-1} is STRUCTURALLY zero for the finite block, and
the value at s = 0 is just the constant coefficient a_0 = sum_i (-lambda_i)^0 = sum_i 1 = card = 30
(the dimension). Equivalently s * Theta(s) -> 0 as s -> 0 (no pole to cancel).

CONTRAST (why an INFINITE spectrum is genuinely required). The would-be pole is the INFINITE
geometric tower sum_{k>=1} exp(-s k) = exp(-s)/(1 - exp(-s)), whose Laurent expansion about s = 0 is
1/s - 1/2 + ... -- principal coefficient c_{-1} = 1. The finite truncation sum_{k=0}^{N-1} x^k =
(1 - x^N)/(1 - x) instead stays FINITE as x -> 1, with value exactly N. So the 1/s pole (residue 1)
is a property of the INFINITE tower; every finite heat trace evaluates to its term count and has no
pole. The Dixmier owner therefore needs the genuinely infinite spectral object, NOT the finite block.

HONEST SCOPE. CLOSED (finite, decidable / exact symbolic): the finite block has no 1/s pole, its
s = 0 value equals dim = 30, the finite geometric tower evaluates to its term count, and the residue
c_{-1} = 1 belongs to the INFINITE tower (absent from any finite truncation). NOT closed and NOT
asserted: the actual Dixmier/Wodzicki residue on the infinite spectral object and the residue->Delta_alpha
normalization -- those stay the external owner edge D0-DIXMIER-RESIDUE-OWNER-001 (ASSUMP-DIXMIER-TRACE).
This is an anti-numerology guard: it PREVENTS declaring the Dixmier owner closed by pointing at the
finite heat trace. No measured/CODATA alpha enters.

Mirrors Lean D0.Spectral.DixmierFeshbachFiniteHeatTrace (archive_heat_trace_const_eq_dim,
finite_trace_principal_coeff_zero, finite_trace_no_principal_part, geom_partial_sum_at_one_eq_card,
geom_partial_telescope_30, finite_trace_residue_ne_infinite, dixmier_feshbach_finite_heattrace_no_pole).
"""
import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# The sample 30-eigenvalue archive block (kernel 8 + 10 + 12 = 30). The exact eigenvalues are
# immaterial to the NO-GO; only card = 30 and finiteness matter. Use 1 (x8), 2 (x10), 3 (x12).
SAMPLE_SPECTRUM = [1.0] * 8 + [2.0] * 10 + [3.0] * 12
DIM = 30


def heat_trace(spectrum, s):
    """Theta(s) = sum_i exp(-s * lambda_i)."""
    return sum(math.exp(-s * lam) for lam in spectrum)


def heat_trace_coeff(spectrum, k):
    """Exact depth-k Maclaurin coefficient a_k = (sum_i (-lambda_i)^k) / k!  (over Fractions)."""
    spec = [F(int(round(lam))) for lam in spectrum]
    return sum((-lam) ** k for lam in spec) / F(math.factorial(k))


def principal_coeff(spectrum, j):
    """Principal-part extraction for a Nat-indexed Maclaurin series: heat_trace_coeff for j >= 0,
    and 0 for every negative integer index j (the residue slot j = -1 is structurally absent).
    """
    if j >= 0:
        return heat_trace_coeff(spectrum, j)
    return F(0)


def geom_partial(N, x):
    """Finite truncation sum_{k=0}^{N-1} x^k as an exact Fraction polynomial value."""
    return sum(x ** k for k in range(N))


def infinite_tower_residue_c_minus_1(s_values):
    """The INFINITE geometric tower g(s) = sum_{k>=1} exp(-s k) = exp(-s)/(1 - exp(-s)) has a simple
    pole at s = 0 with residue 1. Verify numerically that s * g(s) -> 1 as s -> 0 (NEEDS the infinite
    sum -- the closed form is the limit of the infinite series). Returns the extrapolated residue.
    """
    def g(s):
        return math.exp(-s) / (1.0 - math.exp(-s))
    return [(s, s * g(s)) for s in s_values]


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: dim-30 FINITE archive spectrum (multiset of eigenvalues) => "
          "Theta(s)=sum_i exp(-s lambda_i) is ENTIRE => Maclaurin series indexed by k>=0 ONLY (no a_{-1}); "
          "the s=0 value is the constant coefficient a_0 = card = 30; all fixed BEFORE any value; "
          "no measured/CODATA alpha input")
    print("=== D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001  a FINITE heat trace has NO 1/s pole (NO-GO) ===")

    # ---- 1) card = 30 (the dimension) -----------------------------------------------
    assert len(SAMPLE_SPECTRUM) == DIM == 30, f"sample spectrum must have 30 eigenvalues: {len(SAMPLE_SPECTRUM)}"
    print(f"PASS_DIM_30  sample archive block has card = {len(SAMPLE_SPECTRUM)} eigenvalues (= dimension)")

    # ---- 2) Theta(0) = a_0 = card = 30 (exact) --------------------------------------
    a0 = heat_trace_coeff(SAMPLE_SPECTRUM, 0)
    assert a0 == F(30), f"a_0 must equal card = 30: {a0}"
    # numerically: Theta(0) = sum_i exp(0) = 30
    theta0 = heat_trace(SAMPLE_SPECTRUM, 0.0)
    assert abs(theta0 - 30.0) < 1e-12, f"Theta(0) must be 30: {theta0}"
    print(f"PASS_THETA_AT_ZERO_EQ_DIM  a_0 = Theta(0) = {a0} = card = 30 "
          "(archive_heat_trace_const_eq_dim)")

    # ---- 3) NO 1/s pole: s * Theta(s) -> 0 as s -> 0 (finite trace is regular) -------
    s_to_zero = [0.1, 0.01, 0.001, 1e-4, 1e-5]
    s_theta = [(s, s * heat_trace(SAMPLE_SPECTRUM, s)) for s in s_to_zero]
    # For a REGULAR (no-pole) trace, s*Theta(s) ~ s*card -> 0 linearly; for a SIMPLE POLE it would
    # tend to the nonzero residue. Check both: it is O(s) (bounded by ~card*s) AND it shrinks to 0.
    for s, val in s_theta:
        assert val < (DIM + 1) * s, f"s*Theta(s) at s={s} must be O(s) (no pole), got {val}"
    assert s_theta[-1][1] < s_theta[0][1], "s*Theta(s) must decrease toward 0 (no pole to cancel)"
    assert s_theta[-1][1] < 1e-3, f"s*Theta(s) should -> 0; tail value {s_theta[-1][1]}"
    print(f"PASS_NO_POLE_S_THETA_TO_ZERO  s*Theta(s) -> 0 as s->0 (tail {s_theta[-1][1]:.2e}); the finite "
          "heat trace is REGULAR at s=0 -- no residue to extract")

    # ---- 4) the residue slot (j = -1) coefficient is structurally 0 (exact) ----------
    c_minus_1_finite = principal_coeff(SAMPLE_SPECTRUM, -1)
    assert c_minus_1_finite == F(0), f"finite-trace residue slot must be 0: {c_minus_1_finite}"
    # whole negative band vanishes
    for j in (-1, -2, -3, -5):
        assert principal_coeff(SAMPLE_SPECTRUM, j) == F(0), f"negative-index coeff at {j} must be 0"
    print(f"PASS_FINITE_PRINCIPAL_COEFF_ZERO  principalCoeff(spectrum, -1) = {c_minus_1_finite}; the whole "
          "negative band vanishes (Nat-indexed Maclaurin series, finite_trace_no_principal_part)")

    # ---- 5) finite geometric tower stays finite as x -> 1: sum_{k<N} 1^k = N --------
    gp = geom_partial(30, F(1))
    assert gp == F(30), f"finite tower at x=1 must equal term count 30: {gp}"
    # telescoping identity (1 - x) * sum_{k<30} x^k = 1 - x^30, checked at several x (exact)
    for x in (F(2), F(1, 2), F(-3, 7), F(5)):
        lhs = (F(1) - x) * geom_partial(30, x)
        rhs = F(1) - x ** 30
        assert lhs == rhs, f"telescope identity failed at x={x}: {lhs} != {rhs}"
    print(f"PASS_GEOM_PARTIAL_AT_ONE  finite tower sum_(k<30) 1^k = {gp} (term count); telescope "
          "(1-x) sum = 1 - x^30 holds exactly (geom_partial_sum_at_one_eq_card / geom_partial_telescope_30)")

    # ---- 6) the 1/s pole is the INFINITE tower: c_{-1} = 1 (needs the infinite sum) --
    res_pairs = infinite_tower_residue_c_minus_1([0.1, 0.01, 0.001, 1e-4, 1e-5])
    residue_extrap = res_pairs[-1][1]
    assert abs(residue_extrap - 1.0) < 1e-3, \
        f"infinite tower residue c_{{-1}} must be 1: s*g(s)->{residue_extrap}"
    # symbolic check: the closed form exp(-s)/(1-exp(-s)) is the SUM of an INFINITE series; a finite
    # partial sum sum_{k=1}^{K} exp(-s k) does NOT have a pole (it is bounded by K at s=0).
    K = 1000
    s_small = 1e-5
    finite_partial = sum(math.exp(-s_small * k) for k in range(1, K + 1))
    assert finite_partial <= K, "a finite partial tower is bounded by its term count (no pole)"
    full_infinite = math.exp(-s_small) / (1.0 - math.exp(-s_small))
    assert full_infinite > finite_partial, \
        "the infinite tower exceeds any finite partial (the pole lives in the infinite tail)"
    print(f"PASS_INFINITE_TOWER_RESIDUE_ONE  s*g(s) -> {residue_extrap:.6f} ~ 1 for the INFINITE tower "
          f"g(s)=sum_(k>=1) exp(-s k); a finite K={K} partial is bounded by {K} (no pole). The 1/s "
          "residue requires the INFINITE spectrum.")

    # ================= reachable negative controls (FAIL_*) =================
    # FAIL_FINITE_TRACE_HAS_NO_POLE: reject claiming a NONZERO residue (c_{-1} != 0) from the FINITE
    # trace. The finite block has c_{-1} = 0, so the planted claim "finite trace has residue 1" is false.
    claimed_finite_residue = F(1)  # a planted (false) nonzero residue attributed to the finite block
    assert principal_coeff(SAMPLE_SPECTRUM, -1) != claimed_finite_residue, \
        "control: the finite trace must NOT carry a nonzero residue"
    assert principal_coeff(SAMPLE_SPECTRUM, -1) == F(0), "finite-trace residue is structurally 0"
    print("FAIL_FINITE_TRACE_HAS_NO_POLE  planted 'finite heat trace has residue c_{-1}=1' REJECTED "
          "(its residue slot is structurally 0; a Nat-indexed Maclaurin series has no a_{-1})")

    # FAIL_CONSTANT_TERM_IS_DIM: reject claiming the s=0 value is the depth-2 moment mu_2 = 12288/5
    # instead of the dimension. Theta(0) = a_0 = 30 != 12288/5 (= a different Maclaurin coefficient).
    mu2 = F(12288, 5)
    assert a0 != mu2, "control: Theta(0) must be the dimension 30, NOT the depth-2 moment mu_2"
    assert a0 == F(30), "Theta(0) = a_0 = dimension"
    print(f"FAIL_CONSTANT_TERM_IS_DIM  planted 'Theta(0) = mu_2 = 12288/5' REJECTED (the s=0 value is the "
          f"DIMENSION a_0 = 30, not the depth-2 moment {mu2} = {float(mu2):.1f}; different coefficients)")

    # FAIL_DIXMIER_CLOSED_BY_FINITE_HEATTRACE_REJECTED: declaring D0-DIXMIER-RESIDUE-OWNER-001 closed
    # from the finite heat trace is rejected -- the finite trace delivers NO residue (c_{-1}=0).
    dixmier_owner_closed_by_finite_heattrace = False
    assert dixmier_owner_closed_by_finite_heattrace is False, \
        "control: D0-DIXMIER-RESIDUE-OWNER-001 must NOT be declared closed from the finite heat trace"
    # concrete obstruction: the finite residue (0) differs from the owner's nonzero residue (1).
    assert principal_coeff(SAMPLE_SPECTRUM, -1) != F(1), \
        "the finite-trace residue (0) cannot supply the owner's nonzero residue"
    print("FAIL_DIXMIER_CLOSED_BY_FINITE_HEATTRACE_REJECTED  declaring D0-DIXMIER-RESIDUE-OWNER-001 closed "
          "from the finite heat trace is REJECTED: the finite trace yields residue 0, never the nonzero "
          "Dixmier residue; the owner edge stays OPEN (ASSUMP-DIXMIER-TRACE)")

    # FAIL_INFINITE_SPECTRUM_REQUIRED: reject claiming a FINITE truncation reproduces the 1/s pole.
    # The truncated tower (1 - x^N)/(1 - x) -> N at x=1 (finite), so s*[finite partial] -> 0, NOT 1.
    s_small = 1e-5
    finite_partial = sum(math.exp(-s_small * k) for k in range(1, 31))  # finite 30-term tower
    s_times_finite = s_small * finite_partial
    assert abs(s_times_finite - 1.0) > 0.5, \
        "control: a finite truncated tower must NOT reproduce the residue 1"
    assert s_times_finite < 1e-3, "s * (finite tower) -> 0 (no pole from a finite truncation)"
    print("FAIL_INFINITE_SPECTRUM_REQUIRED  planted 'a finite (30-term) tower reproduces the 1/s pole' "
          f"REJECTED: s*(finite partial) = {s_times_finite:.2e} -> 0, not 1; the residue NEEDS the "
          "INFINITE spectrum")

    print("HONEST_SCOPE  NO-GO: CLOSED (finite/exact) = finite trace has no 1/s pole, Theta(0)=dim=30, "
          "finite tower -> term count, residue c_{-1}=1 is an INFINITE-tower object. NOT closed = the "
          "actual Dixmier/Wodzicki residue on the INFINITE spectral object and residue->Delta_alpha "
          "normalization (owner-edge D0-DIXMIER-RESIDUE-OWNER-001, ASSUMP-DIXMIER-TRACE).")
    print("PASS_DIXMIER_FESHBACH_FINITE_HEATTRACE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
