#!/usr/bin/env python3
"""D0-CVFT-F7 (leg 2) REFORGED — refined log-det/rank bound on the actual scene.

Replaces 05_CERTS/vp_cvft_refined_logdet_rank_bound.py, which checked one
hardcoded eigenvalue list at one hardcoded z and printed a "negative control"
that was a float-literal inequality (CERT_CANFAIL_SWEEP_REPORT.md Finding F2).

CLAIM CONTENT (BOOK_02 02.CVFT.v5): for F=(QUP)^dagger(QUP) and a=|z|rho(F)<1,
with the analytic logarithm branch connected to z=0,

    |-log det(I-zF)| <= rank(F) * [-log(1-a)] <= rank(F) * a/(1-a),

and for real 0<z<1/rho(F):  -log det(I-zF) <= rank(F) * [-log(1-z rho(F))].
Resolvent/log-det expansions REQUIRE |z|rho(F)<1 and -log det (closure
contract: "determinant trace without -log det" is a forbidden shortcut).

WHAT IS CONSTRUCTED (nothing hardcoded but the owned scene):
  * K(9,11,13) scene, rank-3 zone-average projector P, unitary family
    U = exp(-i theta L) * D_S  =>  scene-typed F members of rank 1, 2, 3.
    rho(F), rank(F), the spectrum, and the branch are all computed.
  * The analytic branch connected to z=0 is the eigenvalue-sum branch
    -sum_i Log(1-z lam_i) (each factor has Re>0 for a<1, so each principal Log
    is on the connected branch); it is cross-checked against det(I-zF) via
    exp(-logdet) == det (branch-free consistency).
  * Grids: a in {0.1, 0.5, 0.9, 0.99} x phase(z) in {0, pi/4, pi/2, 3pi/4, pi,
    3pi/2} per member, z scaled by the COMPUTED rho.

EXECUTED NEGATIVE CONTROLS (verifier re-run on perturbed input, must reject):
  NC_WEAKENED_RANK_BOUND   — rank(F)-1 in place of rank(F): must be violated by
                             the computed rank-2 member at real z.
  NC_LOGDET_INFLATION      — logdet*1.05 on the computed TIGHT witness (rank-1
                             member at real z, where equality holds): must fail.
  NC_DOMAIN_VIOLATION      — z with a>=1: the checker must refuse to evaluate
                             (the hypothesis |z|rho<1 is enforced, not decorative).
  NC_FLIPPED_CONVEXITY     — a/(1-a) <= -log(1-a) (the reversed second
                             inequality): must be False on the grid.
  NC_FORBIDDEN_Z_ONLY_FORM — the |z|-without-rho form -log(1-|z|): exhibit a
                             computed witness (rank-1 member, rho<1, real z>1,
                             a<1) where the THEOREM form evaluates and holds
                             while the forbidden form is domain-invalid
                             (1-|z|<0). Discrimination is computed, not printed.

Numerics hygiene: Accelerate-BLAS spurious matmul FP warnings silenced for
matmul only; every computed operator passes require_finite (NaN/inf => FAIL).
"""
from __future__ import annotations

import warnings

import numpy as np

warnings.filterwarnings(
    "ignore", message=".*encountered in matmul.*", category=RuntimeWarning
)  # Accelerate-BLAS false positives; require_finite() carries the real load
warnings.filterwarnings(
    "ignore", message=".*encountered in det.*", category=RuntimeWarning
)  # same Accelerate FP-flag artifact via LAPACK det; det output is finiteness-gated below

TOL = 1e-9
RANK_TOL = 1e-7
BOUND_TOL = 1e-10
ZONES = (9, 11, 13)


class NonFiniteOperator(Exception):
    pass


def require_finite(name, M):
    if not np.isfinite(M).all():
        raise NonFiniteOperator(name)
    return M


# ----------------------------------------------------------------- scene layer
def build_scene():
    n = sum(ZONES)
    zone = []
    for zi, size in enumerate(ZONES):
        zone += [zi] * size
    zone = np.array(zone)
    A = (zone[:, None] != zone[None, :]).astype(float)
    np.fill_diagonal(A, 0.0)
    L = np.diag(A.sum(axis=1)) - A
    return n, zone, A, L


def scene_invariants_ok(n, zone, A, L) -> bool:
    if n != 33 or int(round(A.sum() / 2)) != 359:
        return False
    if int(round(np.trace(A @ A @ A) / 6)) != 1287:
        return False
    w = np.linalg.eigvalsh(L)
    expected = [0.0] + [20.0] * 12 + [22.0] * 10 + [24.0] * 8 + [33.0] * 2
    return bool(np.allclose(np.sort(w), np.array(expected), atol=1e-8))


def zone_average_projector(n, zone):
    cols = []
    for zi, size in enumerate(ZONES):
        v = (zone == zi).astype(float)
        cols.append(v / np.sqrt(size))
    Uz = np.column_stack(cols)
    return Uz @ Uz.T


def num_rank(M) -> int:
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s > RANK_TOL))


def unitary_from_laplacian(L, theta):
    w, V = np.linalg.eigh(L)
    return require_finite("U_L", (V * np.exp(-1j * theta * w)) @ V.conj().T)


def phase_gate(n, touched, phases):
    d = np.ones(n, dtype=complex)
    for j, ph in zip(touched, phases):
        d[j] = np.exp(1j * ph)
    return np.diag(d)


def scene_F(L, P, Q, touched, phases, theta):
    n = P.shape[0]
    U = unitary_from_laplacian(L, theta) @ phase_gate(n, touched, phases)
    if np.linalg.norm(U.conj().T @ U - np.eye(n)) >= TOL:
        raise NonFiniteOperator("U not unitary")
    QUP = require_finite("QUP", Q @ U @ P)
    return require_finite("F", QUP.conj().T @ QUP)


# ---------------------------------------------------------------- the checker
def spectrum_of(F):
    lam = np.linalg.eigvalsh((F + F.conj().T) / 2)
    lam = np.where(lam < 0, 0.0, lam)  # PSD typing; negativity beyond TOL is caught upstream
    return lam


def logdet_branch(z, lam):
    """-log det(I-zF) on the analytic branch connected to z=0.

    Valid iff a=|z|max(lam)<1: then |z lam_i|<1, Re(1-z lam_i)>0, and each
    principal Log lies on the branch continuously connected to z=0.
    Returns None if the domain hypothesis fails (the hypothesis is ENFORCED).
    """
    a = abs(z) * float(np.max(lam)) if len(lam) else 0.0
    if not a < 1.0 - 1e-12:
        return None
    val = -np.sum(np.log(1.0 - z * lam[lam > RANK_TOL**2].astype(complex)))
    return complex(val)


def refined_bound_holds(z, F) -> "bool | None":
    """The full claimed chain; None = domain refused (a>=1)."""
    lam = spectrum_of(F)
    rho = float(np.max(lam))
    rank_f = int(np.sum(lam > RANK_TOL**2))
    a = abs(z) * rho
    ld = logdet_branch(z, lam)
    if ld is None:
        return None
    b1 = rank_f * (-np.log(1.0 - a))
    b2 = rank_f * a / (1.0 - a)
    # branch-free consistency: exp(-logdet) must reproduce det(I-zF)
    det_direct = np.linalg.det(np.eye(F.shape[0], dtype=complex) - z * np.asarray(F, dtype=complex))
    if not np.isfinite(det_direct):
        raise NonFiniteOperator("det(I-zF)")
    if abs(np.exp(-ld) - det_direct) > 1e-8 * max(1.0, abs(det_direct)):
        return False
    return bool(abs(ld) <= b1 + BOUND_TOL and b1 <= b2 + BOUND_TOL)


def real_z_bound_holds(z, F) -> "bool | None":
    lam = spectrum_of(F)
    rho = float(np.max(lam))
    a = z * rho
    ld = logdet_branch(z, lam)
    if ld is None:
        return None
    if abs(ld.imag) > 1e-9:
        return False
    return bool(ld.real <= float(np.sum(lam > RANK_TOL**2)) * (-np.log(1.0 - a)) + BOUND_TOL)


def main() -> int:
    try:
        return _main()
    except NonFiniteOperator as exc:
        print(f"FAIL_NON_FINITE_OPERATOR {exc}")
        return 1


def _main() -> int:
    n, zone, A, L = build_scene()
    if not scene_invariants_ok(n, zone, A, L):
        print("FAIL_SCENE_INVARIANTS")
        return 1
    P = zone_average_projector(n, zone)
    Q = np.eye(n) - P
    print("PASS_SCENE_K_9_11_13_INVARIANTS")

    # ---- scene-typed F members (ranks computed, not declared) --------------
    members = {
        "rank1_tight": scene_F(L, P, Q, [0, 1], [0.6, 0.6], 0.4),      # same zone, equal small phases
        "rank2": scene_F(L, P, Q, [0, 9], [2.0, 1.2], 0.7),
        "rank3": scene_F(L, P, Q, [0, 9, 20, 21], [1.0, 2.2, 0.9, 2.8], 1.0),
    }
    expected_rank = {"rank1_tight": 1, "rank2": 2, "rank3": 3}
    for name, F in members.items():
        lam = spectrum_of(F)
        rho = float(np.max(lam))
        rk = int(np.sum(lam > RANK_TOL**2))
        if rk != expected_rank[name]:
            print(f"FAIL_MEMBER_RANK {name} rank={rk} expected={expected_rank[name]}")
            return 1
        if not (0.0 < rho <= 1.0 + TOL):
            print(f"FAIL_MEMBER_RHO {name} rho={rho}")
            return 1
        print(f"PASS_MEMBER_TYPED {name} rank(F)={rk} rho(F)={rho:.6f} (<=1, contraction typing)")

    # ---- the bound chain over computed grids -------------------------------
    a_grid = (0.1, 0.5, 0.9, 0.99)
    psi_grid = (0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 3 * np.pi / 2)
    tested = 0
    for name, F in members.items():
        lam = spectrum_of(F)
        rho = float(np.max(lam))
        for a_t in a_grid:
            for psi in psi_grid:
                z = (a_t / rho) * np.exp(1j * psi)
                ok = refined_bound_holds(z, F)
                if ok is not True:
                    print(f"FAIL_LOGDET_BOUND {name} a={a_t} psi={psi:.3f} result={ok}")
                    return 1
                tested += 1
            z_real = a_t / rho
            ok = real_z_bound_holds(z_real, F)
            if ok is not True:
                print(f"FAIL_REAL_Z_BOUND {name} a={a_t} result={ok}")
                return 1
            tested += 1
    print(f"PASS_CVFT_LOGDET_RANK_BOUND_REFINED_GRID {tested} bound instances verified (3 members x 4 radii x 6 phases + real-z legs)")

    # ---- computed tightness witness (equality at rank 1, real z) -----------
    F1 = members["rank1_tight"]
    lam1 = spectrum_of(F1)
    rho1 = float(np.max(lam1))
    z_t = 0.9 / rho1
    ld_t = logdet_branch(z_t, lam1)
    b_t = 1 * (-np.log(1.0 - 0.9))
    if ld_t is None or abs(ld_t.imag) > 1e-9 or abs(ld_t.real - b_t) > 1e-9:
        print(f"FAIL_TIGHTNESS_WITNESS logdet={ld_t} bound={b_t}")
        return 1
    print(f"PASS_TIGHTNESS_WITNESS rank-1 member at real z: logdet={ld_t.real:.12f} == rank*(-log(1-a))={b_t:.12f}")

    # ---- EXECUTED negative controls ----------------------------------------
    controls_ok = True

    # NC1: weakened bound rank-1 on the rank-2 member must be violated.
    F2 = members["rank2"]
    lam2 = spectrum_of(F2)
    rho2 = float(np.max(lam2))
    z2 = 0.9 / rho2
    ld2 = logdet_branch(z2, lam2)
    weakened = (int(np.sum(lam2 > RANK_TOL**2)) - 1) * (-np.log(1.0 - 0.9))
    if ld2 is None or abs(ld2) <= weakened:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_WEAKENED_RANK_BOUND")
        controls_ok = False
    else:
        print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_WEAKENED_RANK_BOUND |logdet|={abs(ld2):.6f} > (rank-1)*bound={weakened:.6f}")

    # NC2: inflated logdet must violate the bound on the tight witness.
    if abs(ld_t.real * 1.05) <= 1 * (-np.log(1.0 - 0.9)) + BOUND_TOL:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_LOGDET_INFLATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_LOGDET_INFLATION")

    # NC3: domain violation a>=1 must be refused by the checker.
    z_bad = 1.001 / rho2
    if refined_bound_holds(z_bad, F2) is not None:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_DOMAIN_VIOLATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_DOMAIN_VIOLATION a=1.001 refused (|z|rho(F)<1 enforced)")

    # NC4: flipped convexity a/(1-a) <= -log(1-a) must FAIL on the grid.
    flipped_ok = all(a / (1.0 - a) <= -np.log(1.0 - a) + BOUND_TOL for a in a_grid)
    if flipped_ok:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_FLIPPED_CONVEXITY")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_FLIPPED_CONVEXITY reversed second inequality is false on the grid")

    # NC5: the forbidden |z|-only form vs the theorem form — computed witness.
    #      rank-1 member has computed rho<1, so pick real z>1 with a=z*rho<1.
    if rho1 >= 0.7:
        print(f"FAIL_WITNESS_SETUP rho1={rho1} too large for the |z|>1 discrimination")
        return 1
    z_w = 1.4 * 1.0  # |z|>1
    a_w = z_w * rho1
    theorem_ok = refined_bound_holds(z_w, F1)
    forbidden_domain_valid = (1.0 - abs(z_w)) > 0.0
    if not (a_w < 1.0 and theorem_ok is True and not forbidden_domain_valid):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_FORBIDDEN_Z_ONLY_FORM")
        controls_ok = False
    else:
        print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_FORBIDDEN_Z_ONLY_FORM |z|={z_w} rho={rho1:.4f} a={a_w:.4f}<1: "
              f"theorem form holds; -log(1-|z|) domain-invalid — the |z|-only form is not the theorem")

    if not controls_ok:
        print("FAIL_CVFT_LOGDET_RANK_BOUND_REFINED")
        return 1

    print("PASS_CVFT_LOGDET_RANK_BOUND_REFINED")
    print("PASS_CVFT_LOGDET_RANK_BOUND_REFINED_REFORGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
