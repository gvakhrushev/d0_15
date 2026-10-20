#!/usr/bin/env python3
"""Matrix-free bilinear action of the stored-native v8 price.

The callable is ``apply_hessian``. It returns the separate heat ``H``,
program ``J_program`` and matter ``R`` contributions, their sum ``H_red``,
and the linear saddle pairing of ``[H_red, T*; T, 0]`` in the real chart

    real Fourier pairing on field jets
    + real trace pairing on traceless Hermitian shell multipliers.

The lower block is zero and is not inverted. Auxiliary Schur elimination
is used only for the negative blocks of the unfolding variables ``sigma``
and ``X``. Constraint curvature stays inside ``Y``. The heat normalizer,
the indefinite resolvent and the full 4096-mode trace stay in the sum.

N05 (``stored_tangent``) and N06 (``solve_matter_response``) are imported
by path. Their results are not re-derived. The AF preparation second
variation is not added. The field/shell kernel is not classified.
"""

from __future__ import annotations

import importlib.util
import itertools
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import sympy as s


OWNER_SHA = "33267713b2e6d3e78af7789547b00f50cdceb43d"
HISTORICAL_SHA = "74e62cdc716e10883accba9d34ccf0e21d58eb65"
N05_SHA256 = "0881983de7a22a5c2dc027fb9de558776ff91d21c2af4ef1af66c65fc33906fb"
N06_SHA256 = "714dea96f2f86d6e43cd57d2b1b9bf63cd7724d5293638b6999be2b8fe0b1e0b"
HISTORICAL_SHA256 = {
    "02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md":
        "10d30839a5a6b3cf5762ba0b3d7b846b1965363554bd3a971fdb7e8f249908e5",
    "02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md":
        "d92aabf2d46d9ac7d8d9aa3bf5ed66a58f25bb83ca4460d66d25648c62f7e10b",
    "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py":
        "2b12f26d814a57cc99084e904deeac69a8f64a8d9a0eb9ee765e8104ef50bc37",
}
JOINT_SHA256 = (
    "b50614d5871377f0f70c2cffc9912b999eb95e162fccfe8fb3ebea1cf992a2f2"
)

REAL_CHART = "real_fourier_pairing_plus_traceless_hermitian_shell"
WAVE = (3, 3, 0, 0)
# z_r = 8 (exp(2 pi i k_r / 8) - 1), written as p + q sqrt(2).
_RE = ((0, 0), (-8, 4), (-8, 0), (-8, -4), (-16, 0),
       (-8, -4), (-8, 0), (-8, 4))
_IM = ((0, 0), (0, 4), (8, 0), (0, 4), (0, 0),
       (0, -4), (-8, 0), (0, -4))

_SOURCES = Path(__file__).resolve().parents[1]
_TANGENT = None
_MATTER = None
_FOURIER = None
_ROW_WAVE = {}


class HessianApplyError(ValueError):
    """The apply left the owned formula or the declared chart."""


class ZeroBlockError(HessianApplyError):
    """Schur was asked to invert the zero shell block."""


def _load(module_name, path):
    import sys
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    # Python 3.9 dataclasses read the module from sys.modules during exec.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def tangent():
    """N05 chart, imported by path. The directory is not a package."""
    global _TANGENT
    if _TANGENT is None:
        _TANGENT = _load(
            "stored_tangent",
            _SOURCES / "d0_w2_stored_tangent_2026-10-16" / "stored_tangent.py",
        )
    return _TANGENT


def matter():
    """N06 response, imported by path."""
    global _MATTER
    if _MATTER is None:
        _MATTER = _load(
            "matter_response",
            _SOURCES / "d0_w2_matter_response_2026-10-16" / "matter_response.py",
        )
    return _MATTER


def v8_calibrations():
    """Fixed gauges of the original v8 instrument. ``ell`` is not a field.

    ``workspaceDim = 128^8192`` stays a symbol inside the additive constant
    of ``H``. It is not materialized, and it does not enter any derivative.
    """
    p = (s.sqrt(5) - 1) / 2
    ell = s.Rational(1, 8)
    rounds = 8192
    alpha = s.simplify(p ** 2 * ell ** 2 / 128)
    beta = s.simplify(2 * rounds * alpha)
    return {
        "p": p,
        "ell": ell,
        "ell_is_field": False,
        "rounds": rounds,
        "exponent": 2 * rounds,
        "alpha": alpha,
        "beta": beta,
        "fugacity": s.Rational(1, 2 ** 20),
        "feedback_multiplicity": 128,
        "fock_multiplicity": 16,
        "shell_rank": 128,
        "reference_rank": 128,
        "workspace_coefficient": 128,
        "workspaceDim": "128^8192",
        "workspace_materialized": False,
        "b0": s.simplify(p ** 3),
        "af_preparation_second_variation_added": False,
    }


def refuse_dense_workspace(rows, cols=None):
    """The forbidden object is the dense history/workspace, not a scalar."""
    if rows == 128 and cols == 8192:
        raise HessianApplyError("refusing dense workspace 128^8192")
    if isinstance(rows, int) and rows >= 16744448:
        raise HessianApplyError("refusing a dense carrier of excluded coordinates")
    return {"rows": rows, "cols": cols, "materialized": False}


def refuse_shell_schur():
    """The lower block of ``[H_red, T*; T, 0]`` is zero."""
    raise ZeroBlockError(
        "Schur elimination requires an invertible block; "
        "the shell block of [H_red, T*; T, 0] is zero and is not inverted"
    )


def divided_difference(left, right, lam_left, lam_right, derivative=None):
    """Owned divided difference. Equal eigenvalues use the derivative limit.

    A finite-difference quotient is not accepted as this value.
    """
    if lam_left == lam_right or s.simplify(lam_left - lam_right) == 0:
        if derivative is None:
            raise HessianApplyError(
                "coincident eigenvalues require the owned derivative limit"
            )
        return derivative
    return (left - right) / (lam_left - lam_right)


def spectral_weights(energy, calibrations, Z):
    """Heat and program weights and their energy derivatives at fixed ``Z``.

    The rank-one normalizer is not inside these derivatives. ``Z`` is the
    full carrier trace.
    """
    alpha = calibrations["alpha"]
    exponent = calibrations["exponent"]
    beta = calibrations["beta"]
    fugacity = calibrations["fugacity"]
    feedback = calibrations["feedback_multiplicity"]
    base = 1 - alpha * energy
    power = base ** exponent
    heat = -(power / base) / Z
    denom = 1 - fugacity + fugacity * power
    program = feedback * beta * fugacity * (power / base) / denom
    heat_prime = (exponent - 1) * alpha * power / (Z * base * base)
    program_prime = (
        feedback * beta * fugacity * alpha * power / (denom * base * base)
        * (-(exponent - 1) + exponent * fugacity * power / denom)
    )
    short = power / base
    return heat, program, heat_prime, program_prime, short


def _conjugate(value):
    if isinstance(value, s.Expr):
        return s.conjugate(value)
    return value


def _real(value):
    if not isinstance(value, s.Expr):
        return value
    if value == 0 or value.is_real:
        return s.simplify(value)
    expanded = s.expand(value)
    if expanded.is_real:
        return s.simplify(expanded)
    return s.simplify(s.re(expanded))


def _off_map(jet):
    found = {}
    for i, j, value in jet.off:
        found[(i, j)] = value
    return found


def _negative(offset):
    if isinstance(offset, s.Expr):
        return s.simplify(offset) < 0
    return offset < 0


def normalizer_bilinear(shorts, diag_v, diag_w, multiplicities, beta, Z, active):
    """``- dZ[v] dZ[w] / (beta Z^2)`` from the moving heat trace."""
    trace_v = 0
    trace_w = 0
    for i, keep in enumerate(active):
        if not keep:
            continue
        trace_v += multiplicities[i] * shorts[i] * diag_v[i]
        trace_w += multiplicities[i] * shorts[i] * diag_w[i]
    dZ_v = -beta * trace_v
    dZ_w = -beta * trace_w
    return -dZ_v * dZ_w / (beta * Z * Z), dZ_v, dZ_w


def matter_resolvent_trace(jet_v, jet_w, mask, eigenvalues, epsilon, multiplicities,
                           drop_negative=False):
    """``Tr(P X_w R_Q X_v P)`` with ``R_Q = 1/(lambda_Q - epsilon)``.

    Negative offsets are kept. They are the indefinite side of the resolvent.
    """
    right = _off_map(jet_w)
    total = 0
    seen = 0
    for q_index, shell_index, xv_qs in jet_v.off:
        if mask[q_index] or not mask[shell_index]:
            continue
        offset = eigenvalues[q_index] - epsilon
        if drop_negative and _negative(offset):
            continue
        xw_sq = right[(shell_index, q_index)]
        total += multiplicities[shell_index] * xw_sq * xv_qs / offset
        seen += 1
    return total, seen


def price_bilinear(spectrum, jet_v, jet_w, y_diagonal, rho_diagonal, calibrations, Z,
                   epsilon=None, shell_rank=None, mutation=None):
    """Bilinear ``H``, ``J_program`` and ``R`` on one declared spectrum.

    ``spectrum`` has ``eigenvalues``, ``multiplicities`` and ``shell_mask``.
    Jets store a diagonal and ordered off-diagonal triples ``(i, j, value)``.
    Both triangles of a Hermitian jet are listed by the caller. No dense
    complement is built. ``mutation`` selects a negative control; the
    certified numbers are always the unmutated ones.
    """
    mutation = dict(mutation or {})
    if mutation.get("invert_lower_block"):
        refuse_shell_schur()
    if mutation.get("add_af_preparation"):
        raise HessianApplyError(
            "the accepted AF preparation second variation is not part of this v8 price"
        )
    eigenvalues = tuple(spectrum.eigenvalues)
    multiplicities = tuple(spectrum.multiplicities)
    mask = tuple(spectrum.shell_mask)
    count = len(eigenvalues)
    if not (len(multiplicities) == len(mask) == len(y_diagonal) == len(rho_diagonal) == count):
        raise HessianApplyError("spectral jet lengths disagree")
    if len(jet_v.diagonal) != count or len(jet_w.diagonal) != count:
        raise HessianApplyError("diagonal jets do not match the spectrum")

    def active_modes(drop):
        if not drop:
            return tuple(True for _ in range(count))
        return tuple(bool(bit) for bit in mask)

    def evaluate(drop_thermal, omit_normalizer, drop_negative, heat_is_delta):
        active = active_modes(drop_thermal)
        heats, programs, heat_primes, program_primes, shorts = [], [], [], [], []
        for energy in eigenvalues:
            heat, program, heat_prime, program_prime, short = spectral_weights(
                energy, calibrations, Z
            )
            if heat_is_delta:
                heat, heat_prime, short = energy, 1, 0
            heats.append(heat)
            programs.append(program)
            heat_primes.append(heat_prime)
            program_primes.append(program_prime)
            shorts.append(short)
        H_direct = J_direct = R_direct = 0
        H_dd = J_dd = 0
        for i, keep in enumerate(active):
            if not keep:
                continue
            H_direct += multiplicities[i] * heats[i] * y_diagonal[i]
            J_direct += multiplicities[i] * programs[i] * y_diagonal[i]
            R_direct += multiplicities[i] * rho_diagonal[i] * y_diagonal[i]
            H_dd += (
                multiplicities[i] * heat_primes[i]
                * jet_v.diagonal[i] * jet_w.diagonal[i]
            )
            J_dd += (
                multiplicities[i] * program_primes[i]
                * jet_v.diagonal[i] * jet_w.diagonal[i]
            )
        right = _off_map(jet_w)
        for i, j, value_v in jet_v.off:
            if not (active[i] and active[j]):
                continue
            value_w = right[(i, j)]
            same = eigenvalues[i] == eigenvalues[j]
            dH = heat_primes[i] if same else (
                heats[i] - heats[j]
            ) / (eigenvalues[i] - eigenvalues[j])
            dJ = program_primes[i] if same else (
                programs[i] - programs[j]
            ) / (eigenvalues[i] - eigenvalues[j])
            factor = multiplicities[i] * value_v * _conjugate(value_w)
            H_dd += dH * factor
            J_dd += dJ * factor
        if omit_normalizer or heat_is_delta:
            normalizer, dZ_v, dZ_w = 0, 0, 0
        else:
            normalizer, dZ_v, dZ_w = normalizer_bilinear(
                shorts, jet_v.diagonal, jet_w.diagonal, multiplicities,
                calibrations["beta"], Z, active,
            )
        H = H_direct + H_dd + normalizer
        J = J_direct + J_dd
        if epsilon is None:
            resolvent, couplings = 0, 0
        else:
            rank = shell_rank if shell_rank is not None else sum(
                multiplicities[i] for i, bit in enumerate(mask) if bit
            )
            resolvent, couplings = matter_resolvent_trace(
                jet_v, jet_w, mask, eigenvalues, epsilon, multiplicities,
                drop_negative=drop_negative,
            )
            resolvent = matter().matter_hessian_term(resolvent, rank)
        R = R_direct + resolvent
        return {
            "H": _real(H),
            "J_program": _real(J),
            "R": _real(R),
            "sum": _real(H + J + R),
            "normalizer": _real(normalizer),
            "dZ_v": _real(dZ_v),
            "dZ_w": _real(dZ_w),
            "direct_H": _real(H_direct),
            "direct_J": _real(J_direct),
            "direct_R": _real(R_direct),
            "resolvent_R": _real(resolvent),
            "couplings_used": couplings,
        }

    certified = evaluate(False, False, False, False)
    if not mutation:
        certified["mutation"] = None
        certified["mutation_discrepancy"] = 0
        return certified
    mutated = evaluate(
        bool(mutation.get("drop_off_shell_thermal")),
        bool(mutation.get("omit_normalizer") or mutation.get("freeze_normalizer")),
        bool(mutation.get("drop_negative_resolvent")),
        bool(mutation.get("replace_heat_by_delta")),
    )
    certified["mutation"] = sorted(key for key, bit in mutation.items() if bit)
    certified["mutated_sum"] = mutated["sum"]
    certified["mutation_discrepancy"] = _real(certified["sum"] - mutated["sum"])
    certified["lower_block_inverted"] = False
    return certified


def dirac_delta_jets(D, dD_v, dD_w, d2D):
    """``X = {D, dD}`` and ``Y = {dD_v, dD_w} + {D, d²D}``.

    These are the product rule for ``Delta = D²``. Finite differences are
    not used.
    """
    X_v = D * dD_v + dD_v * D
    X_w = D * dD_w + dD_w * D
    Y = dD_v * dD_w + dD_w * dD_v + D * d2D + d2D * D
    return X_v, X_w, Y


def _as_symbol(matrix):
    size = matrix.rows
    diagonal = tuple(matrix[i, i] for i in range(size))
    off = tuple(
        (i, j, matrix[i, j])
        for i in range(size) for j in range(size) if i != j
    )
    return SimpleNamespace(diagonal=diagonal, off=off)


def _require_diagonal(matrix, label):
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if i != j and matrix[i, j] != 0:
                raise HessianApplyError(
                    "%s is not diagonal in the declared eigenbasis" % label
                )


def shell_pairing(shell, diagonal, mask, multiplicities):
    """``Tr(S T)`` for a traceless Hermitian shell multiplier.

    ``T = PXP - (Tr PXP)/r P``, so the trace part of ``X`` drops out once
    ``S`` itself is traceless. A traceful ``S`` is not in the chart.
    """
    indices = [i for i, bit in enumerate(mask) if bit]
    if len(shell) != len(indices):
        raise HessianApplyError("shell multiplier does not match the shell")
    trace = 0
    for value, index in zip(shell, indices):
        trace += multiplicities[index] * value
    if s.simplify(trace) != 0:
        raise HessianApplyError(
            "shell multiplier must be traceless; its trace is epsilon, not S"
        )
    pairing = 0
    for value, index in zip(shell, indices):
        pairing += multiplicities[index] * value * diagonal[index]
    return _real(pairing)


def saddle_bilinear(price, shell_left, shell_right, jet_v, jet_w, spectrum):
    """Pairing of ``[H_red, T*; T, 0] (v, S)`` with ``(w, R)``.

    There is no ``S``-``R`` term. The zero block is not inverted.
    """
    if shell_left is None and shell_right is None:
        cross = 0
    else:
        if shell_left is None or shell_right is None:
            raise HessianApplyError("shell multipliers must be supplied together")
        cross = shell_pairing(
            shell_left, jet_w.diagonal, spectrum.shell_mask, spectrum.multiplicities
        ) + shell_pairing(
            shell_right, jet_v.diagonal, spectrum.shell_mask, spectrum.multiplicities
        )
    return {
        "H": price["H"],
        "J_program": price["J_program"],
        "R": price["R"],
        "sum": price["sum"],
        "shell_cross": _real(cross),
        "linear_action": _real(price["sum"] + cross),
        "real_chart": REAL_CHART,
        "lower_block_inverted": False,
        "lower_block": 0,
        "kernel_classified": False,
    }


def saddle_adjoint_bilinear(price, shell_left, shell_right, jet_v, jet_w, spectrum):
    """Adjoint in the same real pairing. ``H_red`` is symmetric by construction."""
    swapped = saddle_bilinear(price, shell_right, shell_left, jet_w, jet_v, spectrum)
    # price was computed as B(v, w). The swapped call above reuses that
    # scalar and only swaps the shell slots, which is the adjoint exactly
    # when B(v, w) = B(w, v). Callers compare with an explicit swap.
    return swapped


def first_source(spectrum, diagonal, rho_diagonal, calibrations, Z):
    """``Tr((rho + kappa) X)`` at fixed ``Z``. Off-diagonal ``X`` does not contribute."""
    total = 0
    for i, energy in enumerate(spectrum.eigenvalues):
        heat, program, _, _, _ = spectral_weights(energy, calibrations, Z)
        total += spectrum.multiplicities[i] * (
            rho_diagonal[i] + heat + program
        ) * diagonal[i]
    return _real(total)


def curve_versus_coordinate(coordinate_sum, acceleration_diagonal, spectrum,
                            rho_diagonal, calibrations, Z):
    """On a non-critical point the curve second derivative keeps ``dS[a]``.

    ``coordinate_sum`` is the bilinear form on the first jets. The
    acceleration is not discarded.
    """
    extra = first_source(
        spectrum, acceleration_diagonal, rho_diagonal, calibrations, Z
    )
    return {
        "coordinate_hessian": _real(coordinate_sum),
        "curve_second": _real(coordinate_sum + extra),
        "acceleration_term": extra,
        "acceleration_vanishes_automatically": False,
        "critical_point": False,
    }


def auxiliary_sigma_schur(curve):
    """Schur complement of the invertible trace-zero heat block.

    ``curve`` supplies two positive ``K`` branches and their first and
    second jets. The shell block is not involved.
    """
    beta = curve["beta"]
    K1, K2 = curve["K1"], curve["K2"]
    dK1, dK2 = curve["dK1"], curve["dK2"]
    d2K1, d2K2 = curve["d2K1"], curve["d2K2"]
    Z = K1 + K2
    sigma1, sigma2 = K1 / Z, K2 / Z
    dZ = dK1 + dK2
    dsigma1 = dK1 / Z - K1 * dZ / Z ** 2
    dsigma2 = dK2 / Z - K2 * dZ / Z ** 2
    correction = (dsigma1 ** 2 / sigma1 + dsigma2 ** 2 / sigma2) / beta
    # Frozen sigma, moving K. Second derivative of the dual heat.
    t = s.symbols("aux_t")
    K1t = K1 + t * dK1 + t ** 2 * d2K1 / 2
    K2t = K2 + t * dK2 + t ** 2 * d2K2 / 2
    frozen = (
        -sigma1 * s.log(sigma1) - sigma2 * s.log(sigma2)
        + sigma1 * s.log(K1t) + sigma2 * s.log(K2t)
    ) / beta
    frozen_second = s.diff(frozen, t, 2).subs(t, 0)
    direct = s.diff((1 / beta) * s.log(K1t + K2t), t, 2).subs(t, 0)
    # Explicit 1x1 inverse on the traceless coordinate diag(h, -h).
    h = s.symbols("aux_h")
    moved1 = sigma1 + h
    moved2 = sigma2 - h
    mixed = (
        -moved1 * s.log(moved1) - moved2 * s.log(moved2)
        + moved1 * s.log(K1t) + moved2 * s.log(K2t)
    ) / beta
    L_hh = s.diff(mixed, h, 2).subs({t: 0, h: 0})
    L_th = s.diff(mixed, t, h).subs({t: 0, h: 0})
    if s.simplify(L_hh) == 0:
        raise HessianApplyError("auxiliary heat block was singular on this curve")
    schur = s.diff(mixed, t, 2).subs({t: 0, h: 0}) - L_th ** 2 / L_hh
    return {
        "direct": s.simplify(direct),
        "frozen_plus_correction": s.simplify(frozen_second + correction),
        "schur_complement": s.simplify(schur),
        "correction": s.simplify(correction),
        "block_invertible": True,
        "block": "heat_sigma",
        "lower_shell_block_inverted": False,
    }


def auxiliary_program_schur(curve):
    """Schur complement of the invertible log-det block ``X``."""
    M = curve["M"]
    A1, A2 = curve["A1"], curve["A2"]
    dA1, dA2 = curve["dA1"], curve["dA2"]
    d2A1, d2A2 = curve["d2A1"], curve["d2A2"]
    X1, X2 = 1 / A1, 1 / A2
    dX1, dX2 = -X1 * dA1 * X1, -X2 * dA2 * X2
    correction = M * (A1 * dX1 * A1 * dX1 + A2 * dX2 * A2 * dX2)
    t = s.symbols("aux_t")
    A1t = A1 + t * dA1 + t ** 2 * d2A1 / 2
    A2t = A2 + t * dA2 + t ** 2 * d2A2 / 2
    frozen = M * (2 + s.log(X1 * X2) - (X1 * A1t + X2 * A2t))
    frozen_second = s.diff(frozen, t, 2).subs(t, 0)
    direct = s.diff(-M * (s.log(A1t) + s.log(A2t)), t, 2).subs(t, 0)
    h1, h2 = s.symbols("aux_h1 aux_h2")
    # Each positive X slot is free. A single common shift is not the block.
    mixed = M * (
        2 + s.log((X1 + h1) * (X2 + h2))
        - ((X1 + h1) * A1t + (X2 + h2) * A2t)
    )
    origin = {t: 0, h1: 0, h2: 0}
    L11 = s.diff(mixed, h1, 2).subs(origin)
    L22 = s.diff(mixed, h2, 2).subs(origin)
    L12 = s.diff(s.diff(mixed, h1), h2).subs(origin)
    Lt1 = s.diff(s.diff(mixed, t), h1).subs(origin)
    Lt2 = s.diff(s.diff(mixed, t), h2).subs(origin)
    det = s.simplify(L11 * L22 - L12 ** 2)
    if det == 0:
        raise HessianApplyError("auxiliary program block was singular on this curve")
    quad = (L22 * Lt1 ** 2 - 2 * L12 * Lt1 * Lt2 + L11 * Lt2 ** 2) / det
    schur = s.diff(mixed, t, 2).subs(origin) - quad
    return {
        "direct": s.simplify(direct),
        "frozen_plus_correction": s.simplify(frozen_second + correction),
        "schur_complement": s.simplify(schur),
        "correction": s.simplify(correction),
        "block_invertible": True,
        "block": "program_X",
        "lower_shell_block_inverted": False,
    }


def _qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _qsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _qmul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _qsum(values):
    total = (0, 0)
    for value in values:
        total = _qadd(total, value)
    return total


def _real_inner(left, right):
    return _qadd(_qmul(left[0], right[0]), _qmul(left[1], right[1]))


def _symbol(mode):
    return tuple((_RE[index], _IM[index]) for index in mode)


def _feature(vector):
    squares = _qsum(_real_inner(entry, entry) for entry in vector)
    total = (
        _qsum(entry[0] for entry in vector),
        _qsum(entry[1] for entry in vector),
    )
    return squares, _qsub(_real_inner(total, total), squares)


def fourier_feature_groups():
    """Exact Q(sqrt(2)) groups for all 4096 modes and 8192 directed edges.

    Edges are identified only when the exact feature pairs agree. Energies
    are not compared by a tolerance. The groups are the bilinear caller's
    carrier: each group stores one scalar coefficient and its multiplicity.
    """
    global _FOURIER
    if _FOURIER is not None:
        return _FOURIER
    modes = tuple(itertools.product(range(8), repeat=4))
    symbols = {mode: _symbol(mode) for mode in modes}
    features = {mode: _feature(symbols[mode]) for mode in modes}
    slopes = {}
    z2_norm = {}
    for mode, symbol in symbols.items():
        slopes[mode] = (
            _qadd(
                _real_inner(symbol[2], symbol[0]),
                _real_inner(symbol[2], symbol[1]),
            ),
            _real_inner(symbol[2], symbol[3]),
        )
        z2_norm[mode] = _real_inner(symbol[2], symbol[2])
    groups = Counter()
    for mode in modes:
        for sign in (-1, 1):
            partner = tuple((mode[i] + sign * WAVE[i]) % 8 for i in range(4))
            delta = tuple(
                (
                    _qsub(symbols[partner][i][0], symbols[mode][i][0]),
                    _qsub(symbols[partner][i][1], symbols[mode][i][1]),
                )
                for i in range(4)
            )
            common = (z2_norm[mode], _feature(delta))
            left = (features[mode], slopes[mode])
            right = (features[partner], slopes[partner])
            groups[(min(left, right), max(left, right), common)] += 1
    shell = matter().SHELL_MOMENTA
    shell_edges = []
    for mode in shell:
        for sign in (-1, 1):
            partner = tuple((mode[i] + sign * WAVE[i]) % 8 for i in range(4))
            delta = tuple(
                (
                    _qsub(symbols[partner][i][0], symbols[mode][i][0]),
                    _qsub(symbols[partner][i][1], symbols[mode][i][1]),
                )
                for i in range(4)
            )
            shell_edges.append({
                "source_feature": features[mode],
                "partner_feature": features[partner],
                "source_slope": slopes[mode],
                "partner_slope": slopes[partner],
                "z2_norm": z2_norm[mode],
                "delta_feature": _feature(delta),
                "partner_is_shell": partner in shell,
            })
    counts = Counter(features.values())
    _FOURIER = {
        "modes": 4096,
        "groups": tuple(groups.items()),
        "feature_counts": tuple(counts.items()),
        "shell_edges": tuple(shell_edges),
    }
    return _FOURIER


def directional_row_wave(digits=40):
    """Outward full-price Hessian of the owned row wave on the v8 rectangle.

    The midpoint is not treated as a root. No root solver is called.
    ``H`` and ``J_program`` are the full thermal contractions. ``R`` is the
    N06 matter term ``-gamma/4``. Their sum is the directional value.
    """
    import mpmath as mp

    cached = _ROW_WAVE.get(digits)
    if cached is not None:
        return dict(cached)
    tables = fourier_feature_groups()
    calibrations = v8_calibrations()
    box = tangent().receipt_root_box()
    iv = mp.iv
    previous = iv.dps
    iv.dps = digits
    try:
        # Endpoints come from the published rectangle. The midpoint is not a root.
        d = iv.mpf([box["lower_d"], box["upper_d"]])
        o = iv.mpf([box["lower_o"], box["upper_o"]])
        if not (d.a < d.b and o.a < o.b):
            raise HessianApplyError("root rectangle collapsed to a point")
        sqrt2 = iv.sqrt(2)
        p = (iv.sqrt(5) - 1) / 2
        alpha = p * p / calibrations["rounds"]
        beta = 2 * p * p
        fugacity = iv.mpf(1) / 2 ** 20
        exponent = calibrations["exponent"]
        feedback = calibrations["feedback_multiplicity"]
        fock = calibrations["fock_multiplicity"]
        cal = {
            "alpha": alpha,
            "exponent": exponent,
            "beta": beta,
            "fugacity": fugacity,
            "feedback_multiplicity": feedback,
        }
        cross = iv.sqrt((d - o) * (d + 3 * o))
        rotated = (3 * d - o + cross) / 4
        slope_b = (cross - (d - o)) / 4
        slope_c = ((d - o) + cross) / 2
        cache = {}

        def qiv(pair):
            if pair not in cache:
                cache[pair] = pair[0] + pair[1] * sqrt2
            return cache[pair]

        def energy_of(feature):
            return d * qiv(feature[0]) + o * qiv(feature[1])

        energies = {}
        weights = {}
        for feature, _count in tables["feature_counts"]:
            energies[feature] = energy_of(feature)
        bases = {feature: 1 - alpha * value for feature, value in energies.items()}
        if any(base.a <= 0 for base in bases.values()):
            raise HessianApplyError("survival left the positive cone on the rectangle")
        powers = {feature: base ** exponent for feature, base in bases.items()}
        Z = fock * sum(
            count * powers[feature] for feature, count in tables["feature_counts"]
        )
        for feature in energies:
            weights[feature] = spectral_weights(energies[feature], cal, Z)

        def contract(records, drop_off_shell):
            thermal_H = iv.mpf(0)
            thermal_J = iv.mpf(0)
            equal_edges = 0
            nonzero_edges = 0
            for record, multiplicity in records:
                if drop_off_shell and record.get("off_shell", True):
                    continue
                left, right, common = record["key"]
                source_feature, source_slope = left
                partner_feature, partner_slope = right
                z2, delta_feature = common
                norm_V = qiv(z2) * rotated
                norm_W = energy_of(delta_feature)
                bk = slope_b * qiv(source_slope[0]) + slope_c * qiv(source_slope[1])
                bl = slope_b * qiv(partner_slope[0]) + slope_c * qiv(partner_slope[1])
                coefficient = norm_W * norm_V / 4 + bk * bl
                if source_feature == partner_feature:
                    _, _, dH, dJ, _ = weights[source_feature]
                    equal_edges += multiplicity
                else:
                    gap = energies[partner_feature] - energies[source_feature]
                    if not (gap.a > 0 or gap.b < 0):
                        raise HessianApplyError(
                            "distinct feature energies meet on the rectangle"
                        )
                    heat_l, program_l, _, _, _ = weights[partner_feature]
                    heat_k, program_k, _, _, _ = weights[source_feature]
                    dH = (heat_l - heat_k) / gap
                    dJ = (program_l - program_k) / gap
                    nonzero_edges += multiplicity
                thermal_H += fock * multiplicity * dH * coefficient
                thermal_J += fock * multiplicity * dJ * coefficient
            return thermal_H, thermal_J, equal_edges, nonzero_edges

        full_records = tuple(
            ({"key": key, "off_shell": True}, multiplicity)
            for key, multiplicity in tables["groups"]
        )
        # Shell edges are removed from the mutated sum only. Their exact
        # contribution is computed on the same weights, then the mutation
        # keeps only that piece.
        shell_records = []
        for edge in tables["shell_edges"]:
            # Keep source and partner in the order of the directed edge.
            # Sorting would detach ``z2`` from the source slope.
            left = (edge["source_feature"], edge["source_slope"])
            right = (edge["partner_feature"], edge["partner_slope"])
            common = (edge["z2_norm"], edge["delta_feature"])
            shell_records.append((
                {"key": (left, right, common), "off_shell": False},
                1,
            ))
        thermal_H, thermal_J, equal_edges, nonzero_edges = contract(full_records, False)
        shell_H, shell_J, _, _ = contract(shell_records, False)
        lam = 128 - 64 * sqrt2
        amplitude = 128 + 64 * sqrt2
        gap_sum = 2 * amplitude * (d + o)
        gamma = lam * rotated * (1 + gap_sum / (gap_sum + 256 * o)) / 2
        matter_R = -gamma / 4
        total = thermal_H + thermal_J + matter_R
        off_shell = (thermal_H - shell_H) + (thermal_J - shell_J)
        result = {
            "H": thermal_H,
            "J_program": thermal_J,
            "R": matter_R,
            "sum": total,
            "off_shell_thermal": off_shell,
            "shell_only_thermal": shell_H + shell_J,
            "equal_energy_edges": equal_edges,
            "nonzero_gap_edges": nonzero_edges,
            "directed_edges": equal_edges + nonzero_edges,
            "scalar_groups": len(tables["groups"]),
            "thermal_modes": 4096,
            "fock_multiplicity": fock,
            "feedback_multiplicity": feedback,
            "shell_rank": 128,
            "Z": Z,
            "digits": digits,
            "root_solved": False,
            "midpoint_used_as_root": False,
            "rectangle": {
                "d": (box["lower_d"], box["upper_d"]),
                "o": (box["lower_o"], box["upper_o"]),
            },
            "direct_Y": "owned vanishing on this critical directional reduction; not recomputed",
            "lower_block_inverted": False,
            "kernel_classified": False,
            "workspace_materialized": False,
            "af_preparation_second_variation_added": False,
            "physical_admission": False,
            "gr_derived": False,
        }
        _ROW_WAVE[digits] = result
        return dict(result)
    finally:
        iv.dps = previous


def rational_matter_term(a, b):
    """N06 matter contribution on the rational non-root frame."""
    response = matter().solve_matter_response(
        {"scope": "stored_rotational_row_wave"},
        {"scope": "stored_rotational_row_wave"},
        {"carrier": "row_wave", "a": a, "b": b},
    )
    return response


def chart_gate(frame, phase, coordinates, role):
    """Consume the N05 value, inverse, C1 action and both jets.

    A vanishing C1 residual is not an Euler zero mode. The returned mixed
    jet is the coordinate second derivative: coordinate accelerations are
    absent.
    """
    st = tangent()
    tangent_vector = st.kernel_tangent(frame, phase, coordinates)
    residual = st.fourier_c1_action(frame, phase, tangent_vector)
    first = st.fourier_first_jet(frame, role, phase, coordinates)
    mixed = st.fourier_mixed_second(
        frame, role, (phase, coordinates), (phase, coordinates)
    )
    leg = tuple(frame.z[role][i] for i in range(3))
    value = st.edge_value(
        (0, 0, 0), (0, 0, 0), frame.tau[role], frame.rho[role], leg, leg, 0
    )
    recovered = st.edge_inverse(
        value.n_x, value.n_y, value.v_x, value.v_y, value.A
    )
    return {
        "tangent": tangent_vector,
        "c1_nonzero_rows": residual.nonzero_rows(),
        "first": first,
        "mixed": mixed,
        "edge": value,
        "recovered": recovered,
        "euler_kernel": False,
    }


def mixed_chart_symmetry(frame, role, left, right):
    """Schwarz symmetry of the N05 mixed jet on two real chart directions."""
    st = tangent()
    forward = st.fourier_mixed_second(frame, role, left, right)
    backward = st.fourier_mixed_second(frame, role, right, left)
    names = ("A", "F_x", "q_x", "v_x")
    return {
        name: st.is_zero(forward[name] - backward[name]) for name in names
    }, forward


def apply_hessian(operator_jet, matter_state=None, shell_left=None, shell_right=None,
                  calibrations=None, mutation=None):
    """Matrix-free bilinear Hessian action.

    ``operator_jet["kind"]`` is ``dirac``, ``spectral`` or ``row_wave``.

    A Dirac jet supplies ``D, dD_v, dD_w, d2D`` in a declared eigenbasis
    and a diagonal background. A spectral jet supplies the eigenvalues,
    the two Hermitian symbols and the diagonal of ``Y``. The row-wave kind
    evaluates the owned directional reduction on the published rectangle.

    Returns ``H``, ``J_program``, ``R``, their sum, and ``linear_action``.
    """
    kind = operator_jet["kind"]
    if kind == "row_wave":
        if mutation and mutation.get("invert_lower_block"):
            refuse_shell_schur()
        if mutation and mutation.get("add_af_preparation"):
            raise HessianApplyError(
                "the accepted AF preparation second variation is not part of this v8 price"
            )
        result = directional_row_wave(operator_jet.get("digits", 40))
        result["kind"] = "row_wave"
        result["real_chart"] = REAL_CHART
        result["linear_action"] = result["sum"]
        result["shell_cross"] = 0
        result["preparation_couples_this_wave"] = False
        if mutation and mutation.get("drop_off_shell_thermal"):
            result["mutation"] = ["drop_off_shell_thermal"]
            result["mutated_sum"] = result["shell_only_thermal"] + result["R"]
            result["mutation_discrepancy"] = result["sum"] - result["mutated_sum"]
        else:
            result["mutation"] = None
            result["mutation_discrepancy"] = 0
        if matter_state is not None:
            result["matter_scope"] = matter_state.get("scope")
        return result

    calibrations = calibrations or v8_calibrations()
    if kind == "dirac":
        D = operator_jet["D"]
        _require_diagonal(D, "background Dirac")
        X_v, X_w, Y = dirac_delta_jets(
            D, operator_jet["dD_v"], operator_jet["dD_w"], operator_jet["d2D"]
        )
        eigenvalues = tuple(D[i, i] ** 2 for i in range(D.rows))
        mask = tuple(operator_jet["shell_mask"])
        multiplicities = tuple(operator_jet.get("multiplicities", (1,) * D.rows))
        spectrum = SimpleNamespace(
            eigenvalues=eigenvalues,
            multiplicities=multiplicities,
            shell_mask=mask,
        )
        jet_v = _as_symbol(X_v)
        jet_w = _as_symbol(X_w)
        y_diagonal = tuple(Y[i, i] for i in range(Y.rows))
        rho = operator_jet.get("rho")
        if rho is None:
            rho_diagonal = tuple(0 for _ in eigenvalues)
            direct_rho = 0
        else:
            rho_diagonal = tuple(rho[i, i] for i in range(rho.rows))
            direct_rho = s.trace(rho * Y) - sum(
                multiplicities[i] * rho_diagonal[i] * y_diagonal[i]
                for i in range(len(eigenvalues))
            )
        Z = operator_jet["Z"]
        price = price_bilinear(
            spectrum, jet_v, jet_w, y_diagonal, rho_diagonal, calibrations, Z,
            epsilon=operator_jet.get("epsilon"),
            shell_rank=operator_jet.get("shell_rank"),
            mutation=mutation,
        )
        if direct_rho != 0:
            price["R"] = _real(price["R"] + direct_rho)
            price["sum"] = _real(price["sum"] + direct_rho)
            price["direct_R"] = _real(price["direct_R"] + direct_rho)
        price["delta_jets"] = {"X_v": X_v, "X_w": X_w, "Y": Y}
    elif kind == "spectral":
        spectrum = operator_jet["spectrum"]
        jet_v = operator_jet["jet_v"]
        jet_w = operator_jet["jet_w"]
        price = price_bilinear(
            spectrum, jet_v, jet_w, operator_jet["y_diagonal"],
            operator_jet["rho_diagonal"], calibrations, operator_jet["Z"],
            epsilon=operator_jet.get("epsilon"),
            shell_rank=operator_jet.get("shell_rank"),
            mutation=mutation,
        )
    else:
        raise HessianApplyError("unknown operator jet kind")

    linear = saddle_bilinear(price, shell_left, shell_right, jet_v, jet_w, spectrum)
    linear["kind"] = kind
    linear["mutation"] = price.get("mutation")
    linear["mutation_discrepancy"] = price.get("mutation_discrepancy", 0)
    linear["mutated_sum"] = price.get("mutated_sum")
    linear["normalizer"] = price.get("normalizer")
    linear["dZ_v"] = price.get("dZ_v")
    linear["resolvent_R"] = price.get("resolvent_R")
    linear["direct_R"] = price.get("direct_R")
    linear["workspace_materialized"] = False
    linear["af_preparation_second_variation_added"] = False
    linear["physical_admission"] = False
    linear["gr_derived"] = False
    linear["kernel_classified"] = False
    if kind == "dirac":
        linear["Y"] = price["delta_jets"]["Y"]
        linear["X_v"] = price["delta_jets"]["X_v"]
    return linear
