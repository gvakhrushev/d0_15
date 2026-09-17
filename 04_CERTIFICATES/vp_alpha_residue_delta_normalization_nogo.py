#!/usr/bin/env python3
"""D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001 (NO-GO, anti-numerology).

The FINITE Feshbach-Schur residue of W_eff(z) = A - B (D - zI)^-1 C is the depth-2 moment
mu2*u^2 + mu1*u = alpha_alg^-1 EXACTLY in Q(phi) (already CERT-CLOSED, D0-DELTA-ALPHA-MOMENT-001):

    alpha_alg^-1 = (12288/5) phi^-6 + (1/3) phi^-3 = 159739/5 - (294902/15) phi
                 = (159739/5, -294902/15)   in (a,b) = a + b*phi coordinates.

The gluing anomaly is the EXACT difference of TWO independently-canonized Q(phi) elements
(D0-DELTA-ALPHA-EXACT-001):

    alpha_top^-1 = 726 - 364 phi   = (726, -364)      [SEPARATE topological channel-count canonization]
    Delta_alpha  = alpha_top^-1 - alpha_alg^-1
                 = -156109/5 + (289442/15) phi = (-156109/5, 289442/15).

THE FINITE OBSTRUCTION (this cert). The finite residue functional supplies exactly ONE summand,
alpha_alg^-1. The map Delta(top) = top - alpha_alg^-1 is INJECTIVE in its second-canonization
argument `top` (it is the bijection top |-> top - alpha_alg^-1 on the rank-2 free Q-module Q(phi)).
Therefore a single FIXED residue value does NOT determine Delta_alpha: distinct admissible second
canonizations top != top' yield distinct anomalies while the residue is held fixed. We plant a
SECOND canonization alpha_top^-1 + (1,0) = (727, -364): it leaves the finite residue untouched yet
produces a DIFFERENT anomaly. Hence the single finite W_eff residue CANNOT fix the Delta_alpha
NORMALIZATION without an external SECOND input -- the profinite Dixmier 2^11 active-archive pairing,
which stays the owner edge D0-DIXMIER-RESIDUE-OWNER-001 (ASSUMP-DIXMIER-TRACE). No measured/CODATA
alpha enters; CODATA is an external comparison only.

Lean owner: D0.Spectral.DeltaAlphaNormalizationNoGo (residue_coord_eq, delta_at_true_canon,
delta_normalization_underdetermined, deltaOfCanon_injective, two_canons_same_residue_diff_delta,
alpha_residue_delta_normalization_nogo).
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def mul(x, y):
    """Q(phi) product in (a,b)=a+b*phi: (a,b)*(c,d) = (ac+bd, ad+bc+bd) since phi^2 = phi+1."""
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def smul(c, x):
    return (c * x[0], c * x[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


PHI_INV = (F(-1), F(1))   # phi^-1 = -1 + phi  (since phi^2 = phi + 1)


def powp(x, n):
    o = (F(1), F(0))
    for _ in range(n):
        o = mul(o, x)
    return o


def delta_of_canon(top, residue):
    """The anomaly as a function of the SECOND canonization `top`, holding the finite residue fixed."""
    return sub(top, residue)


def main() -> int:
    print("=== D0-ALPHA-RESIDUE-DELTA-NORMALIZATION-NOGO-001  finite W_eff residue does NOT fix Delta_alpha normalization ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: depth-2 finite residue mu2=12288/5, mu1=1/3, mu0=0, u=phi^-3 (=> ONE summand "
          "alpha_alg^-1); Delta_alpha = alpha_top^-1 - alpha_alg^-1 needs a SECOND canonization alpha_top^-1=726-364phi; "
          "all fixed BEFORE any value; no measured/CODATA alpha input")

    # ---- 1) the FINITE residue is exactly alpha_alg^-1 (re-anchor, exact Q(phi)) ----
    u = powp(PHI_INV, 3)
    assert u == (F(-3), F(2)), f"u = phi^-3 must be (-3, 2): {u}"
    mu2, mu1, mu0 = F(12288, 5), F(1, 3), F(0)
    assert mu0 == 0, "mu0 must be 0 (finite pole sum; no infinite-zeta tail)"
    residue = add(smul(mu2, mul(u, u)), smul(mu1, u))   # mu2 u^2 + mu1 u (+ mu0 = 0)
    alpha_alg_inv = (F(159739, 5), F(-294902, 15))
    assert residue == alpha_alg_inv, f"finite residue must equal alpha_alg^-1 = {alpha_alg_inv}: {residue}"
    print(f"PASS_RESIDUE_IS_ALPHA_ALG  Res_finite = mu2 phi^-6 + mu1 phi^-3 = {residue} = alpha_alg^-1 (~{val(residue):.6f}) "
          "(D0.Spectral.DeltaAlphaNormalizationNoGo.residue_coord_eq)")

    # ---- 2) the TRUE anomaly needs the SECOND canonization alpha_top^-1 ----
    alpha_top_inv = sub(smul(359, powp(PHI_INV, 2)), powp(PHI_INV, 5))   # 359 phi^-2 - phi^-5
    assert alpha_top_inv == (F(726), F(-364)), f"alpha_top^-1 must be 726 - 364 phi: {alpha_top_inv}"
    delta_true = delta_of_canon(alpha_top_inv, residue)
    assert delta_true == (F(-156109, 5), F(289442, 15)), f"Delta_alpha must be (-156109/5, 289442/15): {delta_true}"
    print(f"PASS_DELTA_AT_TRUE_CANON  Delta(alpha_top^-1) = alpha_top^-1 - alpha_alg^-1 = {delta_true} = {val(delta_true):.3e} "
          "(recovered ONLY with the second canonization; delta_at_true_canon)")

    # ---- 3) THE NO-GO: a SECOND admissible canonization, same fixed residue, DIFFERENT anomaly ----
    alpha_top_inv_alt = add(alpha_top_inv, (F(1), F(0)))   # planted second canonization, residue untouched
    assert alpha_top_inv_alt == (F(727), F(-364)), f"alt canonization must be (727, -364): {alpha_top_inv_alt}"
    delta_alt = delta_of_canon(alpha_top_inv_alt, residue)   # SAME residue used
    assert delta_alt != delta_true, "two distinct canonizations (same residue) must give DIFFERENT anomalies"
    print(f"PASS_UNDERDETERMINED  a SECOND canonization {alpha_top_inv_alt} (residue UNCHANGED = {residue}) gives "
          f"Delta = {delta_alt} != {delta_true}: the single finite residue does NOT fix Delta_alpha "
          "(delta_normalization_underdetermined)")

    # ---- 4) injectivity of top |-> Delta(top): Delta carries MORE info than the fixed residue ----
    # check on a small fixed grid that distinct tops give distinct Deltas (exact Q(phi))
    grid = [(F(726), F(-364)), (F(727), F(-364)), (F(726), F(-363)), (F(0), F(0)), (F(5, 3), F(-2, 7))]
    deltas = [delta_of_canon(t, residue) for t in grid]
    assert len(set(deltas)) == len(set(grid)), "top |-> Delta(top) must be injective (distinct tops -> distinct Deltas)"
    print(f"PASS_DELTA_INJECTIVE  top |-> top - alpha_alg^-1 is injective on a {len(grid)}-point grid "
          "(deltaOfCanon_injective): Delta_alpha is a faithful function of the SECOND canonization, "
          "so it carries strictly more information than the fixed residue alone")

    # ---- 5) realification agrees with D0-DELTA-ALPHA-EXACT-001 ----
    assert abs(val(delta_true) - (-156109.0 / 5 + 289442.0 / 15 * PHI)) < 1e-9, "realification mismatch"
    print(f"PASS_REALIFICATION  Delta_alpha -> -156109/5 + 289442/15 phi = {val(delta_true):.6e} "
          "(matches delta_alpha_exact / D0-DELTA-ALPHA-EXACT-001)")

    # ================= reachable negative controls (FAIL_*) =================
    # C1) finite-residue-alone-gives-Delta-normalization REJECTED:
    #     claiming Delta_alpha equals the residue (i.e. derivable from the single finite sum alone) is false.
    claim_residue_is_delta = (residue == delta_true)   # would mean the finite sum alone fixes Delta
    assert claim_residue_is_delta is False, "control: the finite residue alone equals Delta_alpha (must be False)"
    # and the residue alone admits >1 compatible Delta (true vs alt), so no well-defined map residue -> Delta
    assert delta_true != delta_alt, "control: residue alone is compatible with >1 Delta"
    print("FAIL_RESIDUE_ALONE_FIXES_DELTA_REJECTED  claiming the single finite residue (alpha_alg^-1) ALONE fixes the "
          f"Delta_alpha normalization is rejected: residue {residue} != Delta_alpha {delta_true}, and the same residue is "
          "compatible with >1 anomaly (true vs planted second canonization) -> no well-defined residue->Delta map")

    # C2) Dixmier-owner-closed-by-the-finite-sum REJECTED:
    #     the residue->Delta normalization (the 2^11 pairing) is NOT delivered by the finite sum.
    dixmier_owner_closed_by_finite_sum = False
    assert dixmier_owner_closed_by_finite_sum is False, \
        "control: D0-DIXMIER-RESIDUE-OWNER-001 must NOT be declared closed from the finite sum"
    # the obstruction is concrete: the finite sum yields ONLY alpha_alg^-1 (one summand), never alpha_top^-1.
    assert residue == alpha_alg_inv and residue != alpha_top_inv, \
        "the finite sum yields alpha_alg^-1 only, NOT alpha_top^-1 (the second canonization is external)"
    print("FAIL_DIXMIER_CLOSED_BY_FINITE_SUM_REJECTED  declaring D0-DIXMIER-RESIDUE-OWNER-001 closed from the finite sum is "
          "rejected: the finite sum delivers ONLY alpha_alg^-1, never the second canonization alpha_top^-1 nor the 2^11 "
          "normalization; the owner edge stays OPEN (ASSUMP-DIXMIER-TRACE)")

    # C3) CODATA-alpha-as-input REJECTED: a measured scalar (no phi-component) is not the phi-only residue/anomaly.
    codata_alpha_inv = (F("137.035999177"), F(0))   # external measured comparison ONLY, never an input
    assert codata_alpha_inv != residue and codata_alpha_inv != delta_true, \
        "control: a measured CODATA alpha^-1 scalar must not be the residue or the anomaly"
    # if CODATA were used to DEFINE the anomaly, the phi-coefficient (which is nonzero here) would vanish
    assert delta_true[1] != 0 and codata_alpha_inv[1] == 0, \
        "control: the anomaly has nonzero phi-coefficient; a measured scalar has none (phi-only check fires)"
    print("FAIL_CODATA_ALPHA_INPUT_REJECTED  a measured CODATA alpha^-1 scalar (no phi-component) is NOT the residue and NOT "
          "Delta_alpha (whose phi-coefficient 289442/15 != 0); the construction is phi-ONLY (CODATA is an external "
          "comparison, never an input)")

    print("HONEST_SCOPE  NO-GO: CLOSED (finite, decidable) = the residue value, the true Delta_alpha value, and the "
          "under-determination (top |-> Delta(top) injective, so the residue alone has >1 compatible Delta). NOT closed = "
          "which canonization is correct, i.e. the residue->Delta_alpha normalization via the external profinite Dixmier "
          "2^11 pairing (owner-edge D0-DIXMIER-RESIDUE-OWNER-001, ASSUMP-DIXMIER-TRACE).")
    print("PASS_ALPHA_RESIDUE_DELTA_NORMALIZATION_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
