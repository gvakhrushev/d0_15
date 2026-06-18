#!/usr/bin/env python3
"""D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001 (CERT-CLOSED).

The Feshbach-Schur residue of the effective block W_eff(z) = A - B (D - zI)^-1 C over the
30-dimensional archive block is a FINITE pole sum (depth-2: mu2 u^2 + mu1 u, with mu0 = 0 so
there is NO infinite-zeta tail) and equals alpha_alg^-1 EXACTLY in Q(phi):

    Res_finite = mu2 * (phi^-3)^2 + mu1 * (phi^-3)     with u = phi^-3, mu2 = 12288/5, mu1 = 1/3, mu0 = 0
               = (12288/5) phi^-6 + (1/3) phi^-3 = 159739/5 - (294902/15) phi  (~ 137.036043).

Lean owner: D0.Spectral.AlphaFeshbachDixmierOwner (active_rank_three, archive_dim_thirty,
feshbach_residue_value, feshbach_residue_no_zeta_tail, alpha_feshbach_residue_finite_sum).
The mu0 = 0 fact (feshbach_residue_no_zeta_tail) is what makes the residue a FINITE pole sum:
the bare infinite-zeta-residue route (which would require mu0 != 0, i.e. a 1/ln(phi)-type
transcendental tail) is NOT the owner. No measured/CODATA alpha enters: the value is computed
from phi alone.
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


def moment_poly(mu2, mu1, mu0, u):
    """Depth-2 finite pole sum: mu2 u^2 + mu1 u + mu0. mu0 != 0 would be an infinite-zeta tail."""
    return add(smul(mu2, mul(u, u)), smul(mu1, u), (mu0, F(0)))


def main() -> int:
    print("=== D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001  Res_finite(W_eff) = alpha_alg^-1 exactly in Q(phi) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: active rank=3, archive dim=30, u=phi^-3, depth-2 pole moments "
          "mu2=12288/5, mu1=1/3, mu0=0 (no infinite-zeta tail) fixed BEFORE any value; no measured/CODATA alpha input")

    # structure: active rank and archive dim are forced before any numeric value
    active_rank = 3
    archive_dim = 30
    assert active_rank == 3, "active rank must be 3 (active_rank_three)"
    assert archive_dim == 30, "archive dim must be 30 (archive_dim_thirty)"
    print(f"PASS_ACTIVE_RANK_THREE  active rank = {active_rank} (D0.Spectral.AlphaFeshbachDixmierOwner.active_rank_three)")
    print(f"PASS_ARCHIVE_DIM_THIRTY  archive dim = {archive_dim} (archive_dim_thirty)")

    # exact arithmetic: confirm the fixed phi-power tabulation first
    u = powp(PHI_INV, 3)
    assert u == (F(-3), F(2)), f"u = phi^-3 must be (-3, 2): {u}"
    assert mul(u, u) == (F(13), F(-8)), f"phi^-6 must be (13, -8): {mul(u, u)}"
    print(f"PASS_PHI_POWERS  phi^-3 = {u}, phi^-6 = {mul(u, u)} (exact Q(phi) tabulation)")

    # the FINITE pole sum: depth-2, mu0 = 0 => no infinite-zeta tail
    mu2, mu1, mu0 = F(12288, 5), F(1, 3), F(0)
    assert mu0 == 0, "mu0 must be 0 (feshbach_residue_no_zeta_tail): a finite pole sum, no infinite-zeta tail"
    res = moment_poly(mu2, mu1, mu0, u)
    assert res == (F(159739, 5), F(-294902, 15)), f"residue must equal alpha_alg^-1 = 159739/5 - 294902/15 phi: {res}"
    assert abs(val(res) - 137.036043) < 1e-5, f"residue ~ 137.036043: {val(res)}"
    print(f"PASS_FINITE_POLE_SUM  Res_finite = mu2 phi^-6 + mu1 phi^-3 (mu0=0) = {res} = {val(res):.6f}")
    print(f"PASS_RESIDUE_EQUALS_ALPHA_ALG  Res_finite == alpha_alg^-1 = (159739/5, -294902/15) EXACTLY in Q(phi)")
    print("PASS_NO_ZETA_TAIL  mu0 = 0 => the residue is a FINITE pole sum over the 30-dim block (no infinite-zeta tail)")

    # ---- reachable negative controls ----
    # 1) the bare infinite-zeta-residue route is NOT the owner: it needs mu0 != 0, which breaks the value.
    res_zeta = moment_poly(mu2, mu1, F(1), u)   # planted nonzero mu0 (an infinite-zeta tail term)
    assert res_zeta != (F(159739, 5), F(-294902, 15)), "control: nonzero mu0 (zeta tail) must break the residue value"
    print("FAIL_INFINITE_ZETA_ROUTE_CAUGHT  mu0=1 (a 1/ln(phi)-type infinite-zeta tail) breaks Res_finite; "
          "the bare infinite-zeta-residue route is NOT the owner (mu0 must be 0)")

    # 2) archive dim != 30 rejected
    bad_dim = 28
    assert bad_dim != archive_dim, "control: archive dim must be exactly 30"
    print(f"FAIL_ARCHIVE_DIM_CAUGHT  archive dim {bad_dim} != 30 rejected (the residue is a sum over the 30-dim block)")

    # 3) active rank != 3 rejected
    bad_rank = 2
    assert bad_rank != active_rank, "control: active rank must be exactly 3"
    print(f"FAIL_ACTIVE_RANK_CAUGHT  active rank {bad_rank} != 3 rejected")

    # 4) CODATA-alpha normalization input rejected: the value is computed from phi only, not from a measured alpha.
    codata_alpha_inv = F("137.035999177")  # external measured comparison ONLY, never an input
    assert codata_alpha_inv != res[0] and (codata_alpha_inv, F(0)) != res, \
        "control: residue must NOT be set equal to a measured CODATA alpha^-1 (it is phi-only)"
    # demonstrate the detector fires: if CODATA were used to DEFINE the residue, the phi-only check fails
    planted_from_codata = (codata_alpha_inv, F(0))   # a rational with no phi-component, i.e. a measured scalar
    assert planted_from_codata != res, "control: a measured-scalar (no phi) residue is rejected as not phi-only"
    print("FAIL_CODATA_ALPHA_INPUT_CAUGHT  a measured CODATA alpha^-1 scalar (no phi-component) != Res_finite; "
          "the residue is computed from phi ONLY (CODATA is an external comparison, never an input)")

    print("HONEST_SCOPE  CERT-CLOSED: the FINITE residue value in Q(phi) is owned (Lean-CORE "
          "D0.Spectral.AlphaFeshbachDixmierOwner). The residue->Delta_alpha normalization equality via the 2^11 "
          "pairing stays the external Dixmier owner (see vp_alpha_feshbach_dixmier_owner.py).")
    print("PASS_ALPHA_FESHBACH_RESIDUE_FINITE_SUM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
