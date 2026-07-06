#!/usr/bin/env python3
"""D0-CVFT-F4 (leg 1) REFORGED — UV feedback-tail refined bound on the actual scene.

Replaces 05_CERTS/vp_cvft_uv_feedback_tail_bound_refined.py, which checked one
hardcoded eigenvalue list at one (z, M), truncated the tail at m<80 with no
truncation control, hardcoded `delta12 = 1e-6` (which is NOT the owned
delta_0^12), and printed its "negative control" unconditionally on the success
path (CERT_CANFAIL_SWEEP_REPORT.md Finding F2).

CLAIM CONTENT (BOOK_02 02.CVFT.v5, BOOK_07 UV-tail-cut clause; registry
D0-CVFT-F4: "deterministic finite cert candidates for the refined tail bound
under |z|rho(F_N)<1"):

    T_M(z,F) = sum_{m>M} z^m/m * Tr(F^m),   a = |z| rho(F) < 1
    |T_M(z,F)| <= rank(F)/(M+1) * a^(M+1)/(1-a)        (refined bound)
    fallback rank(P) when only the ambient retained support is known.

    delta_0^12 with delta_0 = (sqrt5-2)/2 = 1/(2 phi^3) (owned, BOOK_01 01.6)
    is the finite readout noise-floor: |T_M| < delta_0^12 <=> smooth heat-trace /
    macroscopic interface regime; it is NOT the analytic convergence radius
    (BOOK_07: "not the analytic convergence radius of the feedback-resolvent
    series").

WHAT IS CONSTRUCTED: the K(9,11,13) scene, rank-3 zone-average P, scene-typed
F = (QUP)^dagger(QUP) members of computed rank 1/2/3; T_M computed by TWO
independent routes (eigen closed form -sum_i[Log(1-z lam_i) + sum_{m<=M}
(z lam_i)^m/m] vs direct partial summation with a certified geometric remainder)
that must agree; the bound checked over grids of (a, phase(z), M).

EXECUTED NEGATIVE CONTROLS (verifier re-run on perturbed input, must reject):
  NC_EXPONENT_WEAKENED    — bound with an extra factor a (a^(M+2)): violated by
                            the computed rank-1 member at small a.
  NC_RANK_WEAKENED        — bound with rank(F)-1: violated by the computed
                            rank-2 member at (a=0.1, M=0).
  NC_DIVERGENCE_REFUSED   — a>=1 refused by the checker; partial sums computed
                            to demonstrate actual growth past any fixed bound.
  NC_TRUNCATION_SENSITIVE — premature truncation (K=M+2 terms at a=0.9) must
                            disagree with the closed form beyond tolerance:
                            the two-route consistency gate has teeth.
  NC_DELTA0_AS_RADIUS     — the fake control, made real, both confusion shapes:
                            (c1) "converges iff a < delta_0^12" misclassifies a
                            computed convergent a=0.5 instance;
                            (c2) "bound valid only if |T_M| <= delta_0^12" is
                            refuted by a computed witness where the bound HOLDS
                            with |T_M| >> delta_0^12.

Also exposed: the original's hardcoded delta12=1e-6 differs from the owned
delta_0^12 = ((sqrt5-2)/2)^12 ~ 7.35e-12 by more than 5 orders of magnitude.

Numerics hygiene: Accelerate-BLAS spurious matmul FP warnings silenced for
matmul only; every computed operator passes require_finite (NaN/inf => FAIL).
"""
from __future__ import annotations

import warnings

import numpy as np

warnings.filterwarnings(
    "ignore", message=".*encountered in matmul.*", category=RuntimeWarning
)  # Accelerate-BLAS false positives; require_finite() carries the real load

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


def spectrum_of(F):
    lam = np.linalg.eigvalsh((F + F.conj().T) / 2)
    return np.where(lam < 0, 0.0, lam)


# ---------------------------------------------------------------- tail engine
def tail_closed(z, lam, M):
    """T_M via the eigen closed form; None if a>=1 (domain enforced)."""
    rho = float(np.max(lam)) if len(lam) else 0.0
    if not abs(z) * rho < 1.0 - 1e-12:
        return None
    active = lam[lam > RANK_TOL**2].astype(complex)
    total = -np.sum(np.log(1.0 - z * active))          # sum_{m>=1} z^m/m Tr(F^m)
    head = sum((z * active) ** m / m for m in range(1, M + 1)) if M >= 1 else 0.0
    head_sum = np.sum(head) if M >= 1 else 0.0
    return complex(total - head_sum)


def tail_partial(z, lam, M, K):
    """Direct partial sum m=M+1..K, plus its certified geometric remainder bound.

    Computed via the JOINT powers (z*lam_i)^m (modulus <= a), never z^m and
    lam^m separately — the separate route overflows for |z|>1 at large m even
    though the product is bounded (a genuine failure mode, caught in testing).
    """
    active = lam[lam > RANK_TOL**2]
    w = z * active.astype(complex)
    ms = np.arange(M + 1, K + 1, dtype=float)
    powers = require_finite("tail_powers", w[None, :] ** ms[:, None])
    s = complex(np.sum(powers / ms[:, None]))
    a = abs(z) * float(np.max(lam))
    remainder = len(active) / (K + 1) * a ** (K + 1) / (1.0 - a) if a < 1 else float("inf")
    return s, remainder


def refined_tail_bound(rank_f, a, M):
    return rank_f / (M + 1) * a ** (M + 1) / (1.0 - a)


def tail_bound_holds(z, F, M, rank_override=None) -> "bool | None":
    """The claimed bound, with the two-route consistency gate. None = a>=1 refused."""
    lam = spectrum_of(F)
    rho = float(np.max(lam))
    a = abs(z) * rho
    t = tail_closed(z, lam, M)
    if t is None:
        return None
    K = M + max(60, int(np.ceil(np.log(1e-18) / np.log(max(a, 1e-6)))))
    t2, rem = tail_partial(z, lam, M, K)
    if abs(t - t2) > 1e-10 * max(1.0, abs(t)) + rem:
        return False  # the two routes disagree beyond the certified remainder
    rank_f = rank_override if rank_override is not None else int(np.sum(lam > RANK_TOL**2))
    return bool(abs(t) <= refined_tail_bound(rank_f, a, M) + BOUND_TOL)


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
    rank_p = num_rank(P)
    if rank_p != 3:
        print("FAIL_RANK_P")
        return 1
    print("PASS_SCENE_K_9_11_13_INVARIANTS rank(P)=3")

    # ---- owned noise floor (computed two ways, exact identity) --------------
    phi = (1.0 + np.sqrt(5.0)) / 2.0
    delta0_a = (np.sqrt(5.0) - 2.0) / 2.0
    delta0_b = 1.0 / (2.0 * phi ** 3)
    if abs(delta0_a - delta0_b) > 1e-15:
        print("FAIL_DELTA0_IDENTITY")
        return 1
    delta12 = delta0_a ** 12
    if not (delta12 < 1e-10 < 1e-6):
        print("FAIL_DELTA0_12_MAGNITUDE")
        return 1
    print(f"PASS_DELTA0_OWNED delta_0=(sqrt5-2)/2=1/(2 phi^3)={delta0_a:.12f}; delta_0^12={delta12:.6e}")
    print(f"NOTE_ORIGINAL_DEFECT the retired cert hardcoded delta12=1e-6; owned delta_0^12={delta12:.3e} — off by {1e-6/delta12:.0f}x")

    # ---- scene-typed members ------------------------------------------------
    members = {
        "rank1": scene_F(L, P, Q, [0, 1], [0.6, 0.6], 0.4),
        "rank2": scene_F(L, P, Q, [0, 9], [2.0, 1.2], 0.7),
        "rank3": scene_F(L, P, Q, [0, 9, 20, 21], [1.0, 2.2, 0.9, 2.8], 1.0),
    }
    expected_rank = {"rank1": 1, "rank2": 2, "rank3": 3}
    for name, F in members.items():
        lam = spectrum_of(F)
        rk = int(np.sum(lam > RANK_TOL**2))
        rho = float(np.max(lam))
        if rk != expected_rank[name] or not (0 < rho <= 1 + TOL) or rk > rank_p:
            print(f"FAIL_MEMBER_TYPED {name} rank={rk} rho={rho}")
            return 1
        print(f"PASS_MEMBER_TYPED {name} rank(F)={rk}<=rank(P)=3 rho(F)={rho:.6f}")

    # ---- refined bound over grids (and the rank(P) fallback) ----------------
    a_grid = (0.1, 0.5, 0.9, 0.99)
    psi_grid = (0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 3 * np.pi / 2)
    m_grid = (0, 1, 2, 4, 8)
    tested = 0
    for name, F in members.items():
        lam = spectrum_of(F)
        rho = float(np.max(lam))
        for a_t in a_grid:
            for psi in psi_grid:
                z = (a_t / rho) * np.exp(1j * psi)
                for M in m_grid:
                    if tail_bound_holds(z, F, M) is not True:
                        print(f"FAIL_TAIL_BOUND {name} a={a_t} psi={psi:.3f} M={M}")
                        return 1
                    if tail_bound_holds(z, F, M, rank_override=rank_p) is not True:
                        print(f"FAIL_TAIL_BOUND_FALLBACK_RANK_P {name} a={a_t} psi={psi:.3f} M={M}")
                        return 1
                    tested += 2
    print(f"PASS_CVFT_UV_TAIL_BOUND_REFINED_GRID {tested} instances (3 members x 4 radii x 6 phases x 5 cuts, refined + rank(P) fallback)")

    # ---- delta_0^12 regime clause (BOOK_07), computed both sides -------------
    F3 = members["rank3"]
    lam3 = spectrum_of(F3)
    rho3 = float(np.max(lam3))
    z_a = 0.5 / rho3                       # a = 0.5 < 1: series converges
    tA = tail_closed(z_a, lam3, 2)
    tB = tail_closed(z_a, lam3, 40)
    if tA is None or tB is None:
        print("FAIL_REGIME_WITNESS_DOMAIN")
        return 1
    if not (abs(tA) > delta12 and abs(tB) < delta12):
        print(f"FAIL_REGIME_WITNESSES |T_2|={abs(tA):.3e} |T_40|={abs(tB):.3e} delta12={delta12:.3e}")
        return 1
    print(f"PASS_NOISE_FLOOR_REGIMES same a=0.5: |T_2|={abs(tA):.3e} > delta_0^12 (finite-feedback regime) "
          f"while |T_40|={abs(tB):.3e} < delta_0^12 (smooth-interface regime) — the floor classifies (M,|T_M|), not a")

    # ---- EXECUTED negative controls ------------------------------------------
    controls_ok = True
    lam1 = spectrum_of(members["rank1"])
    rho1 = float(np.max(lam1))

    # NC1: extra factor a in the bound must be violated (rank-1, a=0.3, M=2).
    z1 = 0.3 / rho1
    t1 = tail_closed(z1, lam1, 2)
    weak1 = refined_tail_bound(1, 0.3, 2) * 0.3      # a^(M+2) instead of a^(M+1)
    if t1 is None or abs(t1) <= weak1:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_EXPONENT_WEAKENED")
        controls_ok = False
    else:
        print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_EXPONENT_WEAKENED |T_2|={abs(t1):.6f} > a*bound={weak1:.6f}")

    # NC2: rank(F)-1 bound must be violated by the rank-2 member at (a=0.1, M=0).
    lam2 = spectrum_of(members["rank2"])
    lam2_active = lam2[lam2 > RANK_TOL**2]
    ratio = float(np.min(lam2_active) / np.max(lam2_active))
    if ratio < 0.06:
        print(f"FAIL_WITNESS_SETUP rank2 spectral ratio {ratio:.3f} too small for NC_RANK_WEAKENED")
        return 1
    rho2 = float(np.max(lam2))
    z2 = 0.1 / rho2
    t2v = tail_closed(z2, lam2, 0)
    if t2v is None or abs(t2v) <= refined_tail_bound(1, 0.1, 0):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_RANK_WEAKENED")
        controls_ok = False
    else:
        print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_RANK_WEAKENED |T_0|={abs(t2v):.6f} > (rank-1)-bound={refined_tail_bound(1, 0.1, 0):.6f}")

    # NC3: a>=1 refused; partial sums genuinely grow.
    z_div = 1.02 / rho1
    if tail_bound_holds(z_div, members["rank1"], 2) is not None:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_DIVERGENCE_REFUSED")
        controls_ok = False
    else:
        s100, _ = tail_partial(z_div, lam1, 2, 100)
        s200, _ = tail_partial(z_div, lam1, 2, 200)
        if not abs(s200) > 2.0 * abs(s100) > 0:
            print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_DIVERGENCE_REFUSED growth check")
            controls_ok = False
        else:
            print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_DIVERGENCE_REFUSED a=1.02 refused; partial sums grow |S_100|={abs(s100):.3e} -> |S_200|={abs(s200):.3e}")

    # NC4: premature truncation must disagree with the closed form.
    z_fat = 0.9 / rho1
    t_fat = tail_closed(z_fat, lam1, 0)
    t_short, _ = tail_partial(z_fat, lam1, 0, 2)     # only 2 terms of a fat tail
    if t_fat is None or abs(t_fat - t_short) <= 1e-10 * max(1.0, abs(t_fat)):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_TRUNCATION_SENSITIVE")
        controls_ok = False
    else:
        print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_TRUNCATION_SENSITIVE closed-vs-2-term gap {abs(t_fat - t_short):.3e} (the original truncated blind at m<80)")

    # NC5: delta_0^12-as-radius confusions, both shapes, computed.
    a_conv = 0.5
    converged = tail_bound_holds(z_a, F3, 2) is True         # computed convergent instance at a=0.5
    c1_confusion_passes = a_conv < delta12                    # "converges iff a < delta_0^12"
    c2_confusion_passes = abs(tA) <= delta12                  # "bound valid only if |T_M| <= floor"
    bound_holds_at_A = tail_bound_holds(z_a, F3, 2) is True
    if c1_confusion_passes or not converged:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_DELTA0_AS_RADIUS c1")
        controls_ok = False
    elif c2_confusion_passes or not bound_holds_at_A:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_DELTA0_AS_RADIUS c2")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_DELTA0_AS_RADIUS a=0.5>delta_0^12 yet convergent+bounded; "
              "|T_2|>delta_0^12 yet bound holds — the floor is a readout threshold, not the convergence radius")

    if not controls_ok:
        print("FAIL_CVFT_UV_TAIL_BOUND_REFINED")
        return 1

    print("PASS_CVFT_UV_TAIL_BOUND_REFINED")
    print("PASS_CVFT_UV_FEEDBACK_TAIL_BOUND")
    print("PASS_CVFT_UV_TAIL_BOUND_REFINED_REFORGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
