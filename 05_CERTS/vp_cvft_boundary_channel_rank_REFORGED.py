#!/usr/bin/env python3
"""D0-CVFT-F7 (leg 1) REFORGED — boundary-channel rank lemma on the actual scene.

Replaces 05_CERTS/vp_cvft_boundary_channel_rank.py, whose checks were tautologies
over a hardcoded 4x3 literal and whose "negative control" was an unconditional
print on the success path (CERT_CANFAIL_SWEEP_REPORT.md Finding F2).

WHAT IS VERIFIED (all objects constructed, nothing hardcoded but the owned scene):
  * Scene layer: K(9,11,13) complete tripartite graph built exactly; owned
    invariants recomputed: |V|=33, |E|=359, triangles=1287, Laplacian spectrum
    {0^1, 20^12, 22^10, 24^8, 33^2}, zone-average projector P has rank 3 /
    nullity 30 and [L,P]=0.
  * Typing layer (BOOK_05 05.27 / closure contract): P orthogonal projection,
    Q=I-P, U unitary (verified numerically), F=(QUP)^dagger(QUP) Hermitian PSD,
    and the allowed identity F = P - (PUP)^dagger(PUP).
  * Lemma layer (BOOK_02 02.CVFT.v5 / BOOK_07 rank localization):
      rank(F) = rank(QUP);
      im(QUP) subset B_boundary  =>  rank(F) <= dim B_boundary;
      rank(F) <= rank(P) (ambient fallback).
    B_boundary is CONSTRUCTED from the touched registration channels (the cut
    channels opened by the phase gate), not declared as a literal.
  * Discipline layer (registry: "supports localization only and is not an A4
    proof"): the bound is an inequality, not an equality law — a computed
    non-saturation witness (rank(F) < dim B) and a computed saturation witness
    (rank(F) = dim B) must BOTH exist. An inequality with strict slack on
    admissible members cannot serve as an A/4 capacity equality (BOOK_05 05.28
    forbidden shortcut: "rank boundary as A/4 proof").
  * Forbidden-shortcut refutation (05.27): Q != 0 with F = 0 is exhibited by the
    graph flow U=exp(-i theta L) itself ([L,P]=0 => QUP=0): `Q!=0 -> F!=0` is
    refuted by a computed witness, not by a printed slogan.

EXECUTED NEGATIVE CONTROLS (mutation-style; each control RUNS the same verifier
on a perturbed object and the cert FAILS unless the verifier rejects it):
  NC_SCENE_EDGE_DELETED      — delete one cut edge: invariant layer must reject.
  NC_DECLARED_B_TOO_SMALL    — declare a 2-channel B for a 4-channel gate:
                               the im(QUP) subset B check must reject.
  NC_RANK_EQUALITY_MUTATION  — F + full-rank Hermitian perturbation: the
                               rank(F)=rank(QUP) check must reject.
  NC_PSD_MUTATION            — F - 2*lambda_max*I: the PSD check must reject.
  NC_NONUNITARY_DILATION     — U -> 1.03*U: unitarity AND the allowed identity
                               F = P-(PUP)^dagger(PUP) must both reject.

`NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT <name>` is printed ONLY after the mutated
check has actually run and failed. Any control not caught => exit 1.

Numerics hygiene: macOS Accelerate BLAS raises spurious FP-status flags inside
matmul on perfectly finite inputs (verified: eye(33)@eye(33) trips them). The
unreliable warning channel is therefore silenced FOR MATMUL ONLY, and replaced
by a strictly stronger explicit gate: every computed operator passes
`require_finite` (NaN/inf anywhere => hard FAIL). A cert that warns and exits 0
was the sweep's row-13 pathology; here non-finite values are a failure path.
"""
from __future__ import annotations

import warnings

import numpy as np

warnings.filterwarnings(
    "ignore", message=".*encountered in matmul.*", category=RuntimeWarning
)  # Accelerate-BLAS false positives; require_finite() below carries the real load

TOL = 1e-9          # residual tolerance for exact identities
RANK_TOL = 1e-7     # singular-value threshold for numerical rank
ZONES = (9, 11, 13)


class NonFiniteOperator(Exception):
    pass


def require_finite(name: str, M) -> "np.ndarray":
    if not np.isfinite(M).all():  # complex-aware: checks real and imag parts
        raise NonFiniteOperator(name)
    return M


# ----------------------------------------------------------------- scene layer
def build_scene():
    """K(9,11,13): adjacency, Laplacian, zone index list."""
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
    """Owned invariants of K(9,11,13), all recomputed from the built objects."""
    if n != 33:
        return False
    if int(round(A.sum() / 2)) != 359:
        return False
    tri = int(round(np.trace(A @ A @ A) / 6))
    if tri != 1287:
        return False
    w = np.linalg.eigvalsh(L)
    expected = [0.0] * 1 + [20.0] * 12 + [22.0] * 10 + [24.0] * 8 + [33.0] * 2
    if not np.allclose(np.sort(w), np.array(expected), atol=1e-8):
        return False
    return True


def zone_average_projector(n, zone):
    """P = orthogonal projector onto span{1_Z9, 1_Z11, 1_Z13} (rank 3, owned)."""
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


# ---------------------------------------------------------------- verifiers
def is_unitary(U) -> bool:
    return np.linalg.norm(U.conj().T @ U - np.eye(U.shape[0])) < TOL


def is_psd_hermitian(F) -> bool:
    if np.linalg.norm(F - F.conj().T) >= TOL:
        return False
    return float(np.min(np.linalg.eigvalsh((F + F.conj().T) / 2))) > -TOL


def rank_equality_ok(F, QUP) -> bool:
    return num_rank(F) == num_rank(QUP)


def image_contained(QUP, B_basis) -> bool:
    """im(QUP) subset span(B_basis) — computed residual, not a declaration."""
    if B_basis.shape[1] == 0:
        return np.linalg.norm(QUP) < TOL
    Qb, _ = np.linalg.qr(B_basis)
    resid = QUP - Qb @ (Qb.conj().T @ QUP)
    return np.linalg.norm(resid) < 1e-8


def allowed_identity_ok(F, P, U) -> bool:
    """BOOK_05 05.27: F = P - (PUP)^dagger(PUP) (holds iff U isometric on ran P)."""
    PUP = P @ U @ P
    return np.linalg.norm(F - (P - PUP.conj().T @ PUP)) < 1e-8


def boundary_channel_space(UL, Q, touched):
    """B = span{ U_L Q e_j : j touched } — the cut channels opened by the gate.

    QUP = Q U_L D_S P = U_L Q D_S P  (uses [U_L,P]=0, verified upstream) and
    Q D_S P = sum_j (e^{i phi_j}-1) (Q e_j)(e_j^T P), so im(QUP) lies in B by
    construction; the certificate still CHECKS the containment numerically.
    """
    cols = [UL @ Q[:, j] for j in touched]
    return np.column_stack(cols) if cols else np.zeros((Q.shape[0], 0))


def main() -> int:
    try:
        return _main()
    except NonFiniteOperator as exc:
        print(f"FAIL_NON_FINITE_OPERATOR {exc}")
        return 1


def _main() -> int:
    rng = np.random.default_rng(20260705)
    failures: list[str] = []

    # ---- C1: scene + owned invariants -------------------------------------
    n, zone, A, L = build_scene()
    require_finite("L", L)
    if not scene_invariants_ok(n, zone, A, L):
        print("FAIL_SCENE_INVARIANTS")
        return 1
    print("PASS_SCENE_K_9_11_13_INVARIANTS |V|=33 |E|=359 tri=1287 spec={0^1,20^12,22^10,24^8,33^2}")

    # ---- C2: owned projector, rank/nullity 3/30, [L,P]=0 ------------------
    P = zone_average_projector(n, zone)
    Q = np.eye(n) - P
    pr = num_rank(P)
    qr_ = num_rank(Q)
    commut = np.linalg.norm(L @ P - P @ L)
    if not (pr == 3 and qr_ == 30 and commut < TOL and np.linalg.norm(P @ P - P) < TOL):
        print(f"FAIL_ZONE_PROJECTOR rank(P)={pr} rank(Q)={qr_} ||[L,P]||={commut:.2e}")
        return 1
    print(f"PASS_ZONE_PROJECTOR rank(P)=3 nullity=30 ||[L,P]||={commut:.2e}")

    # ---- C3: forbidden-shortcut refutation: Q!=0 with F=0 ------------------
    for theta in (0.3, 1.1):
        UL = unitary_from_laplacian(L, theta)
        if not is_unitary(UL):
            print("FAIL_UL_NOT_UNITARY")
            return 1
        leak = np.linalg.norm(Q @ UL @ P)
        if leak >= TOL:
            print(f"FAIL_GRAPH_FLOW_LEAKS theta={theta} ||QUP||={leak:.2e}")
            return 1
    if np.linalg.norm(Q) < 1.0:
        print("FAIL_Q_DEGENERATE")
        return 1
    print("PASS_FORBIDDEN_SHORTCUT_REFUTED Q!=0 with F=0 witnessed by U=exp(-i theta L), ||QUP||<1e-9")

    # ---- C4: lemma layer on constructed members ----------------------------
    # (touched channels, phases, theta, expected dim B, expected rank F)
    members = [
        ("m1_single_channel", [0], [2.0], 0.7, 1, 1),
        ("m2_two_zones", [0, 9], [2.0, 1.2], 0.7, 2, 2),
        ("m3_same_zone_equal_phase", [0, 1], [1.3, 1.3], 0.4, 2, 1),
        ("m4_four_channels_pcap", [0, 9, 20, 21], [1.0, 2.2, 0.9, 2.8], 1.0, 4, 3),
    ]
    kept = {}
    for name, touched, phases, theta, dimB_exp, rankF_exp in members:
        UL = unitary_from_laplacian(L, theta)
        U = UL @ phase_gate(n, touched, phases)
        if not is_unitary(U):
            failures.append(f"{name}: U not unitary")
            continue
        QUP = require_finite("QUP", Q @ U @ P)
        F = require_finite("F", QUP.conj().T @ QUP)
        B = require_finite("B", boundary_channel_space(UL, Q, touched))
        dimB = num_rank(B)
        rF, rQUP = num_rank(F), num_rank(QUP)
        checks = {
            "psd": is_psd_hermitian(F),
            "rank_eq": rank_equality_ok(F, QUP),
            "containment": image_contained(QUP, B),
            "rank_le_dimB": rF <= dimB,
            "rank_le_rankP": rF <= pr,
            "identity": allowed_identity_ok(F, P, U),
            "dimB_as_expected": dimB == dimB_exp,
            "rankF_as_expected": rF == rankF_exp,
        }
        bad = [k for k, v in checks.items() if not v]
        if bad:
            failures.append(f"{name}: failed {bad} (rankF={rF} rankQUP={rQUP} dimB={dimB})")
        else:
            print(f"PASS_MEMBER {name}: rank(F)=rank(QUP)={rF} <= dimB={dimB} <= |S|={len(touched)}; rank(F)<=rank(P)=3; identity ok")
        kept[name] = (U, UL, QUP, F, B, dimB, rF, touched)
    if failures:
        print("FAIL_CVFT_BOUNDARY_CHANNEL_RANK_REFORGED")
        for f in failures:
            print("  -", f)
        return 1

    # ---- C5: localization-only discipline (not an A4 equality) -------------
    nonsat = [(nm, v[6], v[5]) for nm, v in kept.items() if v[6] < v[5]]
    sat = [(nm, v[6], v[5]) for nm, v in kept.items() if v[6] == v[5]]
    if not nonsat or not sat:
        print(f"FAIL_A4_DISCIPLINE nonsat={nonsat} sat={sat}")
        return 1
    print(f"PASS_LOCALIZATION_ONLY_NOT_A4 strict-slack witness {nonsat[0][0]} rank(F)={nonsat[0][1]}<dimB={nonsat[0][2]}; "
          f"attained on {sat[0][0]} — bound is an inequality, not a capacity equality")

    # ---- C6: EXECUTED negative controls ------------------------------------
    controls_ok = True

    # NC1: scene mutation — delete one cut edge, invariants must reject.
    A_bad = A.copy()
    A_bad[0, 9] = A_bad[9, 0] = 0.0
    L_bad = np.diag(A_bad.sum(axis=1)) - A_bad
    if scene_invariants_ok(n, zone, A_bad, L_bad):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_SCENE_EDGE_DELETED")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_SCENE_EDGE_DELETED")

    # NC2: declared boundary space too small for a 4-channel gate.
    U4, UL4, QUP4, F4, B4, _, _, touched4 = kept["m4_four_channels_pcap"]
    B_small = boundary_channel_space(UL4, Q, touched4[:2])
    if image_contained(QUP4, B_small):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_DECLARED_B_TOO_SMALL")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_DECLARED_B_TOO_SMALL")

    # NC3: rank-equality mutation — full-rank Hermitian perturbation of F.
    U2, UL2, QUP2, F2, B2, _, _, _ = kept["m2_two_zones"]
    G = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    F_mut = F2 + 1e-3 * (G + G.conj().T) / 2
    if rank_equality_ok(F_mut, QUP2):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_RANK_EQUALITY_MUTATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_RANK_EQUALITY_MUTATION")

    # NC4: PSD mutation.
    lam_max = float(np.max(np.linalg.eigvalsh(F2)))
    F_neg = F2 - 2.0 * lam_max * np.eye(n)
    if is_psd_hermitian(F_neg):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_PSD_MUTATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_PSD_MUTATION")

    # NC5: non-unitary dilation — typing layer must reject on BOTH gates.
    U_dil = 1.03 * U2
    QUP_dil = Q @ U_dil @ P
    F_dil = QUP_dil.conj().T @ QUP_dil
    if is_unitary(U_dil) or allowed_identity_ok(F_dil, P, U_dil):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_NONUNITARY_DILATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_NONUNITARY_DILATION")

    if not controls_ok:
        print("FAIL_CVFT_BOUNDARY_CHANNEL_RANK_REFORGED")
        return 1

    print("PASS_CVFT_BOUNDARY_CHANNEL_RANK")
    print("PASS_CVFT_BOUNDARY_RANK_BOUND")
    print("PASS_CVFT_BOUNDARY_CHANNEL_RANK_REFORGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
