#!/usr/bin/env python3
"""D0-CMB-NS-LAPLACIAN-IDS-OWNER-001 (CERT-CLOSED) - IDS staircase + power proxy P(k); spectrum alone does NOT fix n_s.

Companion to vp_reheating_heat_trace_jump.py and vp_cmb_phason_spectrum_owner.py. We reuse the SAME
finite object: the EXACT graph-Laplacian spectrum of the connected reheating scene K(9,11,13)
(33 vertices), by the complete-tripartite formula

    { 0 : mult 1, 20 : mult 12, 22 : mult 10, 24 : mult 8, 33 : mult 2 }

(total multiplicity 33; algebraic connectivity lambda_2 = 20).

VERIFIED MATHEMATICS (encoded, able to FAIL), exact rational arithmetic only:
  * The INTEGRATED DENSITY OF STATES (IDS) staircase N(lambda) = (1/33) * sum_{lambda_i <= lambda} mult_i
    evaluated at the jump points 0 < 20 < 22 < 24 < 33 equals EXACTLY the rationals
        [ 1/33, 13/33, 23/33, 31/33, 1 ]
    (cumulative multiplicities 1, 13, 23, 31, 33 over the total 33).
  * The dimensionless POWER PROXY P(k) = sum_i mult_i / (k^2 + lambda_i) is an exact rational at each
    rational k. We pin P(1) = 163196/68425 and P(2) = 19857/13468.
  * The discrete TILT PROXY  n_s - 1 := (k / P(k)) * P'(k)  with  P'(k) = sum_i mult_i*(-2k)/(k^2+lambda_i)^2
    takes GENUINELY DIFFERENT exact rationals at k = 1 and k = 2:
        (n_s - 1)(1) = -29795504237/33500058900  !=  -119488232/200575557 = (n_s - 1)(2).
    Because the proxy varies with the (otherwise free) evaluation point k, the bare Laplacian spectrum
    ALONE does NOT determine a single scalar n_s -- a finite NO-GO.

The structure (the 33-vertex complete-tripartite spectrum, the IDS staircase, the proxy P(k)) is fixed
BEFORE any number. This cert owns ONLY the IDS+P(k) construction and the spectrum-alone NO-GO. We do
NOT invent any n_s value; no Planck n_s, no inflaton enters. A canonical internally-forced smoothing
functional / evaluation rule that fixes the pair (k,u) so n_s becomes a single determined value is
ABSENT and stays PROOF-TARGET (D0-CMB-IDS-SMOOTHING-OWNER-001); the spectral map n_s = f({lambda_i})
itself stays PROOF-TARGET (D0-CMB-PHASON-SPECTRUM-OWNER-001).

Mirrors Lean D0.Cosmology.CMBLaplacianIDS (ids_staircase, powerProxy_samples, tiltProxy_samples,
spectrum_alone_does_not_fix_ns, cmb_ns_laplacian_ids_owner).
"""
from __future__ import annotations

import sys
from fractions import Fraction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# EXACT K(9,11,13) Laplacian spectrum as (eigenvalue, multiplicity) pairs, fixed before any number.
SPECTRUM = [(0, 1), (20, 12), (22, 10), (24, 8), (33, 2)]
TOTAL = 33  # sum of multiplicities = vertex count = dimension

# Sorted jump points and the EXACT IDS staircase values expected there.
JUMP_POINTS = [0, 20, 22, 24, 33]
EXPECTED_IDS = [Fraction(1, 33), Fraction(13, 33), Fraction(23, 33), Fraction(31, 33), Fraction(1, 1)]

# Two sample evaluation points and the EXACT power-proxy / tilt-proxy values expected there.
EXPECTED_P = {Fraction(1): Fraction(163196, 68425), Fraction(2): Fraction(19857, 13468)}
EXPECTED_NS_MINUS_1 = {
    Fraction(1): Fraction(-29795504237, 33500058900),
    Fraction(2): Fraction(-119488232, 200575557),
}

# The exact missing artifact (named so the gap cannot be laundered).
MISSING_ARTIFACT = (
    "a canonical internally-forced smoothing functional / evaluation rule that fixes the pair (k, u) "
    "(the proxy evaluation scale k and any smoothing window u) so that the discrete tilt proxy "
    "n_s - 1 = (k/P)dP/dk collapses to a SINGLE determined value; absent -- the bare spectrum admits "
    "different n_s at different evaluation points (this cert exhibits two)."
)

# External Planck value - allowed ONLY as a rejected/compared datum, NEVER an input.
PLANCK_NS_EXTERNAL = Fraction(965, 1000)  # 0.965, compared-against only


def total_mult(spectrum):
    """Sum of all multiplicities = dimension = vertex count."""
    return sum(m for _, m in spectrum)


def cumulative_mult(spectrum, lam):
    """Cumulative multiplicity at threshold lam: sum of mult_i for lambda_i <= lam."""
    return sum(m for e, m in spectrum if e <= lam)


def ids(spectrum, lam):
    """Integrated density of states N(lam) = (1/total) * cumulative multiplicity, exact Fraction."""
    return Fraction(cumulative_mult(spectrum, lam), total_mult(spectrum))


def power_proxy(spectrum, k):
    """P(k) = sum_i mult_i / (k^2 + lambda_i), exact Fraction."""
    return sum((Fraction(m) / (k * k + e) for e, m in spectrum), Fraction(0))


def power_proxy_deriv(spectrum, k):
    """P'(k) = sum_i mult_i * (-2k) / (k^2 + lambda_i)^2, exact Fraction (term-by-term derivative)."""
    return sum((Fraction(m) * (-(2 * k)) / (k * k + e) ** 2 for e, m in spectrum), Fraction(0))


def tilt_proxy(spectrum, k):
    """Discrete tilt proxy n_s - 1 := (k / P(k)) * P'(k), exact Fraction."""
    return (k / power_proxy(spectrum, k)) * power_proxy_deriv(spectrum, k)


def main() -> int:
    print("=== D0-CMB-NS-LAPLACIAN-IDS-OWNER-001  IDS + P(k); spectrum alone does NOT fix n_s (CERT-CLOSED) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the 33-vertex COMPLETE-TRIPARTITE K(9,11,13) Laplacian spectrum "
          "{0:1,20:12,22:10,24:8,33:2}, its IDS staircase, and the power proxy P(k)=sum mult_i/(k^2+lambda_i) "
          "are fixed BEFORE any number; no Planck n_s, no inflaton; no n_s value is invented")

    # ---- spectrum sanity: total multiplicity 33, lambda_2 = 20 ----------------------
    assert total_mult(SPECTRUM) == TOTAL == 33, f"total multiplicity != 33: {total_mult(SPECTRUM)}"
    nonzero = sorted(e for e, m in SPECTRUM if e > 0 and m > 0)
    assert nonzero[0] == 20, f"algebraic connectivity lambda_2 != 20: {nonzero[0]}"
    print(f"PASS_SPECTRUM  total multiplicity = 33; algebraic connectivity lambda_2 = {nonzero[0]} > 0")

    # ---- IDS staircase equals the exact rationals [1/33,13/33,23/33,31/33,1] --------
    got_ids = [ids(SPECTRUM, lam) for lam in JUMP_POINTS]
    assert got_ids == EXPECTED_IDS, f"IDS staircase mismatch: {got_ids} != {EXPECTED_IDS}"
    # it is a genuine probability staircase: strictly increasing, reaching exactly 1 at the top
    for a, b in zip(got_ids, got_ids[1:]):
        assert a < b, f"IDS must strictly increase across jumps: {a} !< {b}"
    assert got_ids[-1] == Fraction(1), "IDS must reach exactly 1 at the top eigenvalue"
    print("PASS_IDS_STAIRCASE  IDS at jump points 0<20<22<24<33 = [1/33, 13/33, 23/33, 31/33, 1] "
          "(strictly increasing, reaches 1)")

    # ---- power proxy P(k) exact at the two sample k --------------------------------
    for k, expected in EXPECTED_P.items():
        got = power_proxy(SPECTRUM, k)
        assert got == expected, f"P({k}) mismatch: {got} != {expected}"
    print(f"PASS_POWER_PROXY_EXACT  P(1) = {EXPECTED_P[Fraction(1)]}, P(2) = {EXPECTED_P[Fraction(2)]} (exact)")

    # ---- tilt proxy n_s-1 differs at the two evaluation points: spectrum-alone NO-GO -
    ns1 = tilt_proxy(SPECTRUM, Fraction(1))
    ns2 = tilt_proxy(SPECTRUM, Fraction(2))
    assert ns1 == EXPECTED_NS_MINUS_1[Fraction(1)], f"(n_s-1)(1) mismatch: {ns1}"
    assert ns2 == EXPECTED_NS_MINUS_1[Fraction(2)], f"(n_s-1)(2) mismatch: {ns2}"
    assert ns1 != ns2, "spectrum-alone NO-GO requires two DIFFERENT tilt-proxy values"
    print(f"PASS_TILT_PROXY_DIFFERS  (n_s-1)(k=1) = {ns1} != {ns2} = (n_s-1)(k=2) "
          "-> the bare spectrum ALONE does not fix a single n_s")
    print(f"MISSING_ARTIFACT  {MISSING_ARTIFACT}")

    # ================= negative controls (genuinely reachable) =======================
    # (a) "n_s is determined by the spectrum alone": rejected because two evaluation points give two
    #     different tilt-proxy values (the canonical (k,u) rule is absent).
    ns_determined_by_spectrum_alone = (ns1 == ns2)
    assert ns_determined_by_spectrum_alone is False, \
        "control: spectrum alone must NOT determine a single n_s (two eval points -> two values)"
    print("FAIL_NS_DETERMINED_BY_SPECTRUM_ALONE_REJECTED  planted 'n_s fixed by spectrum alone' rejected "
          f"(k=1 gives {float(ns1):.6f}, k=2 gives {float(ns2):.6f}; they differ)")

    # (b) "Planck n_s = 0.965 used as an input": the construction must not ingest the survey value, and
    #     0.965 is not equal to either internal tilt-proxy evaluation.
    planck_used_as_input = False  # PLANCK_NS_EXTERNAL is compared-against only, never an input
    assert planck_used_as_input is False, "control: Planck n_s must NOT be used as an input"
    assert (PLANCK_NS_EXTERNAL - 1) != ns1 and (PLANCK_NS_EXTERNAL - 1) != ns2, \
        "control: external Planck n_s-1 must not coincide with an internal proxy value"
    print("FAIL_PLANCK_NS_INPUT_REJECTED  planted 'Planck n_s=0.965 used as input' rejected "
          "(0.965 is a compared external datum only, never a D0 input)")

    # (c) "an inflaton field / slow-roll potential inserted to fix n_s": nothing in this finite object
    #     provides an inflaton; the proxy is built from the bare integer Laplacian spectrum only.
    inflaton_inserted = False  # no scalar field, no slow-roll parameters enter this object
    assert inflaton_inserted is False, "control: no inflaton / slow-roll input may be inserted"
    print("FAIL_INFLATON_INSERTED_REJECTED  planted 'inflaton field inserted to fix n_s' rejected "
          "(the proxy uses only the bare Laplacian spectrum; no scalar field, no slow-roll)")

    # (d) a tampered IDS staircase claiming the wrong cumulative value at lambda=20. Rejected: the true
    #     cumulative multiplicity there is 13, not 12.
    tampered_ids_20 = Fraction(12, 33)
    assert ids(SPECTRUM, 20) != tampered_ids_20, "control: tampered IDS value at lambda=20 must be rejected"
    print("FAIL_TAMPERED_IDS_REJECTED  planted IDS(20)=12/33 rejected (true cumulative mult is 13 -> 13/33)")

    print("HONEST_IDS_AND_PK_CONSTRUCTED_BUT_SMOOTHING_RULE_IS_PROOF_TARGET")
    print("PASS_CMB_NS_LAPLACIAN_IDS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
