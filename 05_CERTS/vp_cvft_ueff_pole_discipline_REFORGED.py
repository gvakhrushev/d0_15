#!/usr/bin/env python3
"""D0-CVFT-F4 (leg 2) REFORGED — U_eff contraction and pole discipline on the actual scene.

Replaces 05_CERTS/vp_cvft_ueff_pole_discipline.py, whose "U_eff" was a hardcoded
eigenvalue list (0.8*e^{0.3i}, 0.5, 0), whose "pole check" was |0.3-0.3|<1e-12,
whose "positivity of bare F" was `isinstance(x, float) and x >= 0` over a second
hardcoded list, and whose two NEGATIVE_CONTROL_CAUGHT lines were printed
unconditionally on the success path (CERT_CANFAIL_SWEEP_REPORT.md Finding F2).

CLAIM CONTENT (BOOK_02 02.CVFT.v5; BOOK_05 05.27; closure contract):
  * U_eff = P U P is a contraction (sigma_max <= 1);
  * complex pole language (energy E = arg lambda, width gamma = -log|lambda| > 0)
    belongs to the compressed non-normal U_eff (or Feshbach-Schur), NEVER to the
    bare positive F: "complex mass/width poles from bare positive F_N" is a
    contract-level forbidden shortcut;
  * bare F = (QUP)^dagger(QUP) is Hermitian PSD with real nonnegative spectrum;
  * allowed identity (05.27): F = P - (PUP)^dagger(PUP), i.e. on the active
    block U_eff^dagger U_eff + F_c = I — damping (sigma<1) <=> leakage (F != 0),
    quantitatively: 3 - sum sigma_i^2(U_eff) = tr F.

WHAT IS CONSTRUCTED: K(9,11,13) scene; P = rank-3 zone-average projector with
orthonormal block basis Z (Z Z^dagger = P); U = exp(-i theta L) * D_S unitary;
U_eff = Z^dagger U Z (3x3, genuinely non-normal for leaky members — verified);
poles = eig(U_eff) with computed energies and widths; bare F spectrum computed
with a GENERAL eigensolver (not a float type check).

EXECUTED NEGATIVE CONTROLS (each runs a verifier on a perturbed/planted object):
  NC_COMPLEX_POLES_FROM_BARE_F — the fabricated control, made real: the
        complex-spectrum detector must return False on every computed bare F,
        True on F + skew-Hermitian plant (which also fails the Hermitian gate),
        and True on U_eff itself (which fails the "bare positive" typing gate):
        computed complex pole phases exist while spec(F) is real to 1e-10 —
        the phases provably do not come from bare F.
  NC_ORIGINAL_MODULUS_IDENTITY — the retired cert's implicit identity
        spec(F) = |eig(U_eff)|^2 is FALSE under the owned typing: computed
        sorted(1 - sigma_i^2) vs sorted(|lambda_i|^2) differ beyond tolerance
        on a genuinely non-normal member.
  NC_NONUNITARY_DILATION — U -> 1.05 U: contraction AND identity must reject.
  NC_UNDAMPED_MUTATION   — U_eff scaled past unit spectral radius: the
        no-growth gate (all gamma >= 0) must reject.
  NC_UNITARY_BLOCK_ON_LEAKY — the hypothesis "U_eff^dagger U_eff = I" must be
        rejected for a leaky member (damping <=> leakage dichotomy is real).

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


def zone_block_basis(n, zone):
    """Z: 33x3 orthonormal columns spanning ran P (zone averages); Z Z^T = P."""
    cols = []
    for zi, size in enumerate(ZONES):
        v = (zone == zi).astype(float)
        cols.append(v / np.sqrt(size))
    return np.column_stack(cols)


def unitary_from_laplacian(L, theta):
    w, V = np.linalg.eigh(L)
    return require_finite("U_L", (V * np.exp(-1j * theta * w)) @ V.conj().T)


def phase_gate(n, touched, phases):
    d = np.ones(n, dtype=complex)
    for j, ph in zip(touched, phases):
        d[j] = np.exp(1j * ph)
    return np.diag(d)


# ---------------------------------------------------------------- verifiers
def has_complex_spectrum(M, tol=1e-8) -> bool:
    return bool(np.max(np.abs(np.linalg.eigvals(M).imag)) > tol)


def is_hermitian(M) -> bool:
    return np.linalg.norm(M - M.conj().T) < TOL


def bare_positive_spectrum_ok(F) -> bool:
    """Bare positive F: Hermitian, and GENERAL eigensolver returns real >= 0."""
    if not is_hermitian(F):
        return False
    ev = np.linalg.eigvals(F)
    return bool(np.max(np.abs(ev.imag)) < 1e-10 and np.min(ev.real) > -1e-10)


def contraction_ok(M) -> bool:
    return float(np.max(np.linalg.svd(M, compute_uv=False))) <= 1.0 + TOL


def no_growth_ok(poles) -> bool:
    """All widths gamma = -log|lambda| >= 0 (no amplifying pole)."""
    return all(-np.log(abs(lam)) >= -1e-9 for lam in poles if abs(lam) > 1e-12)


def main() -> int:
    try:
        return _main()
    except NonFiniteOperator as exc:
        print(f"FAIL_NON_FINITE_OPERATOR {exc}")
        return 1


def _main() -> int:
    rng = np.random.default_rng(20260705)
    n, zone, A, L = build_scene()
    if not scene_invariants_ok(n, zone, A, L):
        print("FAIL_SCENE_INVARIANTS")
        return 1
    Z = zone_block_basis(n, zone)
    P = Z @ Z.T
    Q = np.eye(n) - P
    if np.linalg.norm(Z.T @ Z - np.eye(3)) >= TOL:
        print("FAIL_BLOCK_BASIS")
        return 1
    print("PASS_SCENE_K_9_11_13_INVARIANTS block basis Z (3 zone channels) orthonormal, ZZ^T=P")

    members = {
        "flow_only": ([], [], 0.9),
        "leaky_2ch": ([0, 9], [2.0, 1.2], 0.7),
        "leaky_4ch": ([0, 9, 20, 21], [1.0, 2.2, 0.9, 2.8], 1.0),
    }
    kept = {}
    for name, (touched, phases, theta) in members.items():
        U = unitary_from_laplacian(L, theta) @ phase_gate(n, touched, phases)
        if np.linalg.norm(U.conj().T @ U - np.eye(n)) >= TOL:
            print(f"FAIL_U_NOT_UNITARY {name}")
            return 1
        U_eff = require_finite("U_eff", Z.conj().T @ U @ Z)          # 3x3 compressed transfer
        QUP = require_finite("QUP", Q @ U @ P)
        F = require_finite("F", QUP.conj().T @ QUP)
        F_c = require_finite("F_c", Z.conj().T @ F @ Z)

        # contraction + allowed identity U_eff^dagger U_eff + F_c = I_3
        if not contraction_ok(U_eff):
            print(f"FAIL_UEFF_CONTRACTION {name}")
            return 1
        ident = np.linalg.norm(U_eff.conj().T @ U_eff + F_c - np.eye(3))
        if ident >= 1e-8:
            print(f"FAIL_ALLOWED_IDENTITY {name} ||U_eff^dag U_eff + F_c - I||={ident:.2e}")
            return 1

        # poles of the compressed transfer
        poles = np.linalg.eigvals(U_eff)
        if not no_growth_ok(poles):
            print(f"FAIL_POLE_GROWTH {name}")
            return 1

        # bare positive F: real nonnegative spectrum by GENERAL eigensolver
        if not bare_positive_spectrum_ok(F) or not bare_positive_spectrum_ok(F_c):
            print(f"FAIL_BARE_F_SPECTRUM {name}")
            return 1

        # damping <=> leakage, quantitatively: 3 - sum sigma^2 = tr F
        sig = np.linalg.svd(U_eff, compute_uv=False)
        lhs = 3.0 - float(np.sum(sig**2))
        rhs = float(np.real(np.trace(F)))
        if abs(lhs - rhs) >= 1e-8:
            print(f"FAIL_DAMPING_LEAKAGE_BALANCE {name} {lhs} vs {rhs}")
            return 1

        gam = np.array([-np.log(abs(l)) for l in poles])
        ene = np.array([np.angle(l) for l in poles])
        kept[name] = dict(U=U, U_eff=U_eff, F=F, F_c=F_c, poles=poles, gam=gam, ene=ene, sig=sig)
        print(f"PASS_MEMBER {name}: sigma_max={sig.max():.6f}<=1; ||U_eff^dag U_eff + F_c - I||={ident:.1e}; "
              f"3-sum(sigma^2)=tr(F)={rhs:.6f}; widths gamma={np.round(gam, 6).tolist()}")

    # ---- pole discipline: flow-only member has NO damping, leaky members DO --
    g0 = kept["flow_only"]["gam"]
    if not (np.max(np.abs(g0)) < 1e-9 and np.real(np.trace(kept["flow_only"]["F"])) < 1e-12):
        print("FAIL_FLOW_ONLY_SHOULD_BE_UNDAMPED")
        return 1
    for name in ("leaky_2ch", "leaky_4ch"):
        gam, ene = kept[name]["gam"], kept[name]["ene"]
        damped_complex = [(e, g) for e, g in zip(ene, gam) if g > 1e-6 and abs(e) > 1e-6]
        if not damped_complex:
            print(f"FAIL_NO_DAMPED_COMPLEX_POLE {name}")
            return 1
    e_w, g_w = max(
        ((e, g) for nm in ("leaky_2ch", "leaky_4ch") for e, g in zip(kept[nm]["ene"], kept[nm]["gam"]) if g > 1e-6),
        key=lambda t: t[1],
    )
    print(f"PASS_UEFF_POLE_DISCIPLINE damped complex poles arise ONLY with leakage: flow-only gamma~0; "
          f"witness pole E={e_w:.6f}, gamma={g_w:.6f} computed from the 33-dim scene (not hardcoded 0.3)")

    # ---- EXECUTED negative controls -----------------------------------------
    controls_ok = True
    Fh = kept["leaky_2ch"]["F"]
    U_eff2 = kept["leaky_2ch"]["U_eff"]

    # NC1: complex poles cannot come from bare positive F.
    bare_all_real = all(not has_complex_spectrum(kept[nm]["F"]) for nm in kept)
    Ksk = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    F_plant = Fh + 0.05 * (Ksk - Ksk.conj().T)       # skew-Hermitian plant
    plant_caught = has_complex_spectrum(F_plant) and not bare_positive_spectrum_ok(F_plant)
    ueff_complex = has_complex_spectrum(U_eff2) and not is_hermitian(U_eff2)
    phases_not_from_F = float(np.max(np.abs(np.linalg.eigvals(Fh).imag))) < 1e-10 and \
        float(np.max(np.abs(kept["leaky_2ch"]["ene"]))) > 1e-3
    if not (bare_all_real and plant_caught and ueff_complex and phases_not_from_F):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_COMPLEX_POLES_FROM_BARE_F")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_COMPLEX_POLES_FROM_BARE_F bare F real to 1e-10 on all members; "
              "skew plant caught by BOTH gates; complex phases live in non-Hermitian U_eff only")

    # NC2: the retired cert's implicit identity spec(F) = |eig(U_eff)|^2 is false
    #      under the owned typing on a genuinely non-normal member.
    nonnormal = np.linalg.norm(U_eff2 @ U_eff2.conj().T - U_eff2.conj().T @ U_eff2)
    if nonnormal < 1e-6:
        print("FAIL_WITNESS_SETUP U_eff unexpectedly normal")
        return 1
    mod_sq = np.sort(np.abs(np.linalg.eigvals(U_eff2)) ** 2)
    one_minus_sig_sq = np.sort(1.0 - np.linalg.svd(U_eff2, compute_uv=False) ** 2)
    spec_Fc = np.sort(np.linalg.eigvalsh((kept["leaky_2ch"]["F_c"] + kept["leaky_2ch"]["F_c"].conj().T) / 2))
    typing_holds = np.allclose(spec_Fc, one_minus_sig_sq, atol=1e-8)  # both sorted ascending
    original_identity_holds = np.allclose(np.sort(spec_Fc), np.sort(mod_sq), atol=1e-6)
    if not typing_holds or original_identity_holds:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_ORIGINAL_MODULUS_IDENTITY")
        controls_ok = False
    else:
        print(f"NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_ORIGINAL_MODULUS_IDENTITY spec(F_c)=1-sigma^2 holds "
              f"(owned identity) but spec(F_c)!=|eig(U_eff)|^2 (retired cert's hardcoded relation): "
              f"{np.round(spec_Fc, 6).tolist()} vs {np.round(mod_sq, 6).tolist()}")

    # NC3: non-unitary dilation must be rejected by contraction AND identity.
    U_dil = 1.05 * kept["leaky_2ch"]["U"]
    Ue_dil = Z.conj().T @ U_dil @ Z
    Fc_dil = Z.conj().T @ ((Q @ U_dil @ P).conj().T @ (Q @ U_dil @ P)) @ Z
    dil_caught = (not contraction_ok(Ue_dil)) and \
        np.linalg.norm(Ue_dil.conj().T @ Ue_dil + Fc_dil - np.eye(3)) > 1e-6
    if not dil_caught:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_NONUNITARY_DILATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_NONUNITARY_DILATION")

    # NC4: push U_eff past unit spectral radius: no-growth gate must reject.
    sr = float(np.max(np.abs(np.linalg.eigvals(U_eff2))))
    U_amp = U_eff2 * (1.03 / sr)
    if no_growth_ok(np.linalg.eigvals(U_amp)):
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_UNDAMPED_MUTATION")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_UNDAMPED_MUTATION amplified block rejected (gamma<0 detected)")

    # NC5: "U_eff^dagger U_eff = I" must be rejected for a leaky member.
    if np.linalg.norm(U_eff2.conj().T @ U_eff2 - np.eye(3)) <= 1e-8:
        print("FAIL_NEGATIVE_CONTROL_NOT_CAUGHT NC_UNITARY_BLOCK_ON_LEAKY")
        controls_ok = False
    else:
        print("NEGATIVE_CONTROL_EXECUTED_AND_CAUGHT NC_UNITARY_BLOCK_ON_LEAKY damping<=>leakage dichotomy is real")

    if not controls_ok:
        print("FAIL_UEFF_CONTRACTION_POLE_DISCIPLINE")
        return 1

    print("PASS_UEFF_CONTRACTION_POLE_DISCIPLINE")
    print("PASS_UEFF_POLE_DISCIPLINE")
    print("PASS_UEFF_POLE_DISCIPLINE_REFORGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
