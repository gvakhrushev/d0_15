#!/usr/bin/env python3
"""Reusable off-shell matter response for the owned v8 shell.

Candidate interface for N07. The nonlinear elimination
Psi = J sqrt(tau) V, E = 0, Tr(tau J* J) = 1 and ||G_Q|| < 4
is taken from SOURCE 33267713b2e6d3e78af7789547b00f50cdceb43d.
It is not re-derived here. The historical row-wave and conformal
scopes are read from 74e62cdc716e10883accba9d34ccf0e21d58eb65.

This module does not allocate the 16,744,448 excluded real
Q-amplitude coordinates, does not invert the field/shell saddle,
and does not claim physical preparation or an Einstein limit.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import sympy as s


OWNER_SHA = "33267713b2e6d3e78af7789547b00f50cdceb43d"
HISTORICAL_SHA = "74e62cdc716e10883accba9d34ccf0e21d58eb65"

SHELL_RANK = 128
REFERENCE_RANK = 128
FOCK_RANK = 16
MOMENTUM_MODES = 4096
CARRIER_DIM = MOMENTUM_MODES * FOCK_RANK
EXCLUDED_REAL_Q_COORDINATES = 2 * (CARRIER_DIM - SHELL_RANK) * REFERENCE_RANK

CERTIFIED_GAP_LOWER = Fraction(1, 2)
WINDOW_DELTA = Fraction(1, 8)
WINDOW_EPSILON = Fraction(1, 8)
RQ_NORM_UPPER = 2
GQ_STRICT_UPPER = 4

ROOT_CENTER_D = "0.063635191594344535042829697433316630182693569761541"
ROOT_CENTER_O = "0.0040167350432317252873844519148251220686807163526359"
ROOT_RADIUS = "1e-12"

# Executable operations that never form the complement matrix or the
# excluded real amplitude vector. Traces stay on shell blocks or on a
# caller-supplied spectrum of scalar eigenvalues.
MATRIX_FREE_OPERATIONS = (
    "fourier_shell_mask",
    "modewise_RQ_apply",
    "neumann_GQ_apply",
    "shell_gram_on_coupling_blocks",
    "kappa_divided_difference",
    "rank_one_Z_normalizer",
    "shell_trace_contraction",
)

SHELL_MOMENTA = tuple(
    tuple((sign % 8 if i == axis else 0) for i in range(4))
    for axis in range(4)
    for sign in (1, -1)
)


class MatterResponseError(ValueError):
    """The caller left the proved domain or asked for a refused reduction."""


def is_zero(value):
    """Exact vanishing. Symbolic zeros are expanded before a structural test."""
    if isinstance(value, s.MatrixBase):
        return all(is_zero(entry) for entry in value)
    expanded = s.expand(value)
    if expanded == 0:
        return True
    cancelled = s.cancel(s.together(expanded))
    if cancelled == 0:
        return True
    return s.simplify(expanded) == 0


def _as_fraction(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, s.Rational) and value.is_rational:
        return Fraction(int(value.p), int(value.q))
    raise MatterResponseError("bound inputs must be exact rationals")


def _strictly_less(left, right):
    return _as_fraction(left) < _as_fraction(right)


def decimal_rational(text):
    """Exact rational from a decimal string. No binary float."""
    dec = Decimal(str(text))
    sign, digits, exp = dec.as_tuple()
    number = int("".join(str(digit) for digit in digits) or "0")
    if sign:
        number = -number
    if exp >= 0:
        return s.Integer(number) * (s.Integer(10) ** exp)
    return s.Rational(number, s.Integer(10) ** (-exp))


def certified_root_rectangle():
    """Consume the published v8 rectangle. Do not estimate a new gap."""
    radius = decimal_rational(ROOT_RADIUS)
    d_lo = decimal_rational(ROOT_CENTER_D) - radius
    d_hi = decimal_rational(ROOT_CENTER_D) + radius
    o_lo = decimal_rational(ROOT_CENTER_O) - radius
    o_hi = decimal_rational(ROOT_CENTER_O) + radius
    lam = 128 - 64 * s.sqrt(2)
    # lam * d_lo - 2 = a + b sqrt(2), b < 0. Positive iff a^2 > 2 b^2.
    excess = s.expand(lam * d_lo - 2)
    a = s.Rational(excess.subs(s.sqrt(2), 0))
    b = s.Rational(s.together((excess - a) / s.sqrt(2)))
    zero_mode_clears = a > 0 and b < 0 and (a * a - 2 * b * b) > 0
    return {
        "d_interval": (d_lo, d_hi),
        "o_interval": (o_lo, o_hi),
        "d_above_o": d_lo > o_hi > 0,
        "d_above_one_sixteenth": d_lo > s.Rational(1, 16),
        "epsilon0_above_2": bool(zero_mode_clears),
        "positive_mode_gap": "certified > 1/2; not recomputed",
        "field_inverse_estimated": False,
        "physical_admission": False,
    }


def is_shell_momentum(mode):
    """Matrix-free shell mask. O(1) membership, no projector matrix."""
    return tuple(mode) in SHELL_MOMENTA


def uniform_shell_complement_bound(delta_op_norm, epsilon_shift, *, gap_exceeds_certified):
    """Uniform complement bound inherited from the certified gap only.

    ||R_Q|| <= 2 when the owned gap is strictly above 1/2.
    ||G_Q|| < 4 only on the open window
    ||Delta-Delta0|| < 1/8 and |epsilon-epsilon0| < 1/8.
    A larger observed gap does not tighten these constants, and neither
    constant estimates the full field/shell Hessian inverse.
    """
    record = {
        "source": "certified_next_shell_gap_lower",
        "certified_gap": ">1/2",
        "rq_norm_upper": None,
        "gq_strict_upper": None,
        "window_open": False,
        "field_inverse_estimated": False,
        "declared_domain_only": True,
    }
    if gap_exceeds_certified is not True:
        record["reason"] = "certified gap was not supplied; no substitute estimate"
        return record
    record["rq_norm_upper"] = RQ_NORM_UPPER
    window = (
        _strictly_less(abs(_as_fraction(delta_op_norm)), WINDOW_DELTA)
        and _strictly_less(abs(_as_fraction(epsilon_shift)), WINDOW_EPSILON)
    )
    record["window_open"] = window
    if window:
        record["gq_strict_upper"] = GQ_STRICT_UPPER
        record["reason"] = "open spectral window and certified gap"
    else:
        record["reason"] = "outside the declared open window; ||G_Q||<4 is not claimed"
    return record


def neumann_tail_bound(order, contraction, resolvent_norm=RQ_NORM_UPPER):
    """Owned tail ||R0|| t^(k+1)/(1-t), strict < 4 * 2^(-(k+1)) for t<1/2."""
    if order < 0:
        raise MatterResponseError("Neumann order must be nonnegative")
    t = _as_fraction(contraction)
    r0 = _as_fraction(resolvent_norm)
    if not (0 <= t < Fraction(1, 2)):
        raise MatterResponseError("tail bound requires contraction t < 1/2")
    if r0 > RQ_NORM_UPPER:
        raise MatterResponseError("tail uses the certified resolvent bound, not a larger norm")
    exact = r0 * (t ** (order + 1)) / (1 - t)
    uniform = Fraction(GQ_STRICT_UPPER, 2 ** (order + 1))
    return {"exact_tail": exact, "uniform_tail": uniform, "strict": exact < uniform}


def matrix_free_neumann(q_offsets, v_diagonal, steps):
    """Modewise Neumann apply. Workspace length equals the Q-mode count.

    q_offsets are the diagonal entries of Delta0-epsilon0 on Q.
    v_diagonal is the diagonal of V_Q in that eigenbasis.
    No complement-by-complement matrix is formed.
    """
    if len(q_offsets) != len(v_diagonal):
        raise MatterResponseError("Neumann diagonals must share the Q-mode basis")
    if 2 * len(q_offsets) * SHELL_RANK >= EXCLUDED_REAL_Q_COORDINATES:
        raise MatterResponseError("refusing a Q basis large enough to be the excluded carrier")
    values = []
    workspace = []
    for offset, shift in zip(q_offsets, v_diagonal):
        exact = s.simplify(1 / (offset + shift))
        series = s.Integer(0)
        term = s.simplify(1 / offset)
        for _ in range(steps + 1):
            series += term
            term = s.simplify(-term * shift / offset)
        values.append(s.simplify(exact))
        workspace.append(series)
    return {
        "exact": values,
        "partial": [s.simplify(item) for item in workspace],
        "workspace_length": len(workspace),
        "matrix_free": True,
        "operation": "neumann_GQ_apply",
        "excluded_coordinates_materialized": 0,
    }


def refuse_native_dense_materialization(carrier_dim, shell_rank, reference_rank):
    """The excluded real vector is not an allocatable workspace."""
    excluded = 2 * (carrier_dim - shell_rank) * reference_rank
    if excluded >= EXCLUDED_REAL_Q_COORDINATES:
        raise MatterResponseError(
            "refusing dense Q-amplitude coordinates: %s real entries" % excluded
        )
    return excluded


def auxiliary_unfolding(K, A):
    """sigma_* = K/Tr K and X_* = A^{-1}. Auxiliary, not physical Psi."""
    Z = s.simplify(s.trace(K))
    if Z == 0:
        raise MatterResponseError("auxiliary K has vanishing trace")
    return {
        "sigma_aux": s.simplify(K / Z),
        "X_aux": s.simplify(A.inv()),
        "trace_sigma": s.Integer(1),
        "is_physical_matter": False,
        "is_reference_frame": False,
        "predicate": "Tr sigma = 1 is the unfolding constraint, not Tr(tau J* J) = 1",
    }


def _eye(size):
    return s.eye(size)


def off_shell_factors(delta, epsilon, U, W):
    """Block Schur factors. U spans P and W spans Q; both are isometries.

    Returns shell-sized E, gram, and the Q-block coefficient of J.
    The stacked map J = U + W J_Q is not allocated when the excluded
    real count would reach the native complement.
    """
    shell = U.cols
    complement = W.cols
    refuse_native_dense_materialization(U.rows, shell, shell)
    QdQ = s.simplify(W.H * delta * W)
    QdP = s.simplify(W.H * delta * U)
    PdP = s.simplify(U.H * delta * U)
    gq = s.simplify((QdQ - epsilon * _eye(complement)).inv())
    Jq = s.simplify(-gq * QdP)
    gram = s.simplify(_eye(shell) + Jq.H * Jq)
    E = s.simplify(PdP - epsilon * _eye(shell) - QdP.H * gq * QdP)
    return {"E": E, "gram": gram, "J_Q": Jq, "G_Q": gq, "Q_Delta_P": QdP}


def reconstruction_factors(J_Q, tau, V):
    """Psi factors J sqrt(tau) V without a dense excluded coordinate vector.

    shell_factor lives in the reference/shell block.
    Q_factor is the complement coefficient in the W basis. Its real
    dimension is reported and, on the native carrier, refused upstream.
    """
    sqrt_tau = hermitian_sqrt(tau)
    shell_factor = s.simplify(sqrt_tau * V)
    Q_factor = s.simplify(J_Q * shell_factor)
    return {
        "sqrt_tau": sqrt_tau,
        "shell_factor": shell_factor,
        "Q_factor": Q_factor,
        "formula": "Psi = J sqrt(tau) V",
        "excluded_real_coordinates_materialized": 0,
        "Q_coefficient_real_dimension": 2 * J_Q.rows * J_Q.cols,
    }


def hermitian_sqrt(tau):
    """Square root for diagonal or already-factored Hermitian tau."""
    if tau.rows != tau.cols:
        raise MatterResponseError("tau must be square on the shell")
    if all(tau[i, j] == 0 for i in range(tau.rows) for j in range(tau.cols) if i != j):
        out = s.zeros(tau.rows)
        for i in range(tau.rows):
            if s.simplify(tau[i, i]) == 0:
                out[i, i] = 0
            else:
                out[i, i] = s.sqrt(tau[i, i])
        return out
    try:
        vectors, values = tau.diagonalize()
    except (ValueError, s.matrices.exceptions.MatrixError) as exc:
        raise MatterResponseError("non-diagonal tau needs an explicit Hermitian square root") from exc
    rooted = s.diag(*[s.sqrt(values[i, i]) for i in range(values.rows)])
    return s.simplify(vectors * rooted * vectors.inv())


def normalization_value(tau, gram):
    """Moving-gram constraint Tr(tau gram). Frozen Tr(tau) is not accepted."""
    moving = s.simplify(s.trace(tau * gram))
    frozen = s.simplify(s.trace(tau))
    return {
        "moving_gram_trace": moving,
        "frozen_trace": frozen,
        "normalized": s.simplify(moving - 1) == 0,
        "frozen_reading_accepted": False,
    }


def normalization_restoring_tau_jet(tau, gram, dgram, d2gram):
    """Particular trace correction holding Tr(tau gram) through second order.

    Traceless Hermitian directions of tau stay free. They are not gauge.
    """
    moving0 = s.trace(tau * gram)
    d_moving_frozen = s.trace(tau * dgram)
    # dtau = c1 I, d2tau = c2 I. Traceless directions are not fixed.
    tr_g = s.trace(gram)
    if s.simplify(tr_g) == 0:
        raise MatterResponseError("gram trace vanished; normalization chart failed")
    c1 = s.simplify(-s.trace(tau * dgram) / tr_g)
    c2 = s.simplify(-(2 * c1 * s.trace(dgram) + s.trace(tau * d2gram)) / tr_g)
    return {
        "trace_correction_first": c1,
        "trace_correction_second": c2,
        "frozen_first_residual": s.simplify(d_moving_frozen),
        "frozen_second_residual": s.simplify(s.trace(tau * d2gram)),
        "held_value": s.simplify(moving0),
        "traceless_directions_free": tau.rows * tau.rows - 1,
        "declared_gauge": False,
    }


def _jet(expr, parameter):
    first = s.diff(expr, parameter)
    second = s.diff(first, parameter)
    return {
        "value": s.simplify(expr.subs(parameter, 0)),
        "first": s.simplify(first.subs(parameter, 0)),
        "second": s.simplify(second.subs(parameter, 0)),
    }


def response_curve_jets(delta_of_t, epsilon_of_t, tau_of_t, V_of_t, U, W, parameter):
    """Value, first jet and second jet of the owned reconstruction at t = 0.

    The field jet is delta_of_t. E uses the proved Schur block.
    dE_identity is the jet of J* (dDelta) J - gram depsilon, so its value
    is the first derivative of E and its first component is the second.
    The normalization jet is Tr(tau gram), not the frozen trace of tau.
    V is retained in the Q/shell factors and is not quotiented out.
    The curve parameter must be a real SymPy symbol.
    """
    refuse_native_dense_materialization(U.rows, U.cols, U.cols)
    factors = off_shell_factors(delta_of_t, epsilon_of_t, U, W)
    identity = dE_formula(
        factors["J_Q"], factors["gram"], U, W,
        s.diff(delta_of_t, parameter), s.diff(epsilon_of_t, parameter),
    )
    built = reconstruction_factors(factors["J_Q"], tau_of_t, V_of_t)
    normalization = s.trace(tau_of_t * factors["gram"])
    frozen = s.trace(tau_of_t)
    return {
        "E": _jet(factors["E"], parameter),
        "dE_identity": _jet(identity, parameter),
        "gram": _jet(factors["gram"], parameter),
        "normalization": _jet(normalization, parameter),
        "frozen_trace": _jet(frozen, parameter),
        "Q_factor": _jet(built["Q_factor"], parameter),
        "shell_factor": _jet(built["shell_factor"], parameter),
        "declared_gauge": False,
        "excluded_real_coordinates_materialized": 0,
    }


def dE_formula(J_Q, gram, U, W, dDelta, depsilon):
    """Proved identity dE = J* (dDelta) J - gram depsilon, off the shell too."""
    refuse_native_dense_materialization(U.rows, U.cols, U.cols)
    J_shell = U + W * J_Q
    formed = J_shell.H * dDelta * J_shell
    return s.simplify(formed - gram * depsilon)


def projected_compatibility(E, tau, *, schmidt_rank, shell_rank):
    """Operator equality E = 0 only at full Schmidt rank.

    Below full rank the proved condition is E tau = 0 on the support.
    A rank-one preparation does not inherit E = 0 as an operator equation.
    """
    if schmidt_rank > shell_rank or schmidt_rank < 0:
        raise MatterResponseError("Schmidt rank must lie between 0 and the shell rank")
    full = schmidt_rank == shell_rank and shell_rank > 0
    support = is_zero(E * tau)
    operator = is_zero(E)
    return {
        "full_schmidt": full,
        "operator_equality_proved": full,
        "operator_zero": operator if full else None,
        "support_zero": support,
        "compatible": operator if full else support,
        "imposed_operator_equality_below_full_rank": False,
    }


def linear_shell_split(shell_block, *, full_schmidt):
    """Split P Delta' P into its trace and the traceless shell residual T.

    P Delta' P = epsilon' P is returned only for a full Schmidt preparation.
    """
    rank = shell_block.rows
    epsilon_trace = s.simplify(s.trace(shell_block) / rank)
    residual = s.simplify(shell_block - epsilon_trace * _eye(rank))
    operator_zero = is_zero(residual)
    return {
        "epsilon_prime": epsilon_trace if full_schmidt else None,
        "trace_average": epsilon_trace,
        "T": residual,
        "operator_equality_proved": bool(full_schmidt),
        "operator_compatible": bool(operator_zero) if full_schmidt else None,
    }


def kernel_coordinates(shell_rank, reference_rank):
    """Untouched shell multiplier and reference fiber. Not a gauge quotient."""
    if shell_rank != reference_rank:
        # The owned purification uses the same 128. A mismatch is data, not a reduction.
        same = False
    else:
        same = True
    return {
        "shell_rank": shell_rank,
        "reference_rank": reference_rank,
        "shell_matches_reference128": same and shell_rank == SHELL_RANK,
        "hermitian_tau_real_dimension": shell_rank * shell_rank,
        "traceless_shell_multiplier_real_dimension": shell_rank * shell_rank - 1,
        "antihermitian_reference_real_dimension": reference_rank * reference_rank,
        "coordinates_materialized": False,
        "declared_gauge": False,
        "reading": (
            "anti-Hermitian V is the polar reference fiber of this price; "
            "traceless Hermitian S remains in the unsolved saddle. "
            "Neither is declared a physical gauge."
        ),
        "field_shell_kernel_solved": False,
        "lower_saddle_block_inverted": False,
    }


def matter_hessian_term(shell_trace, shell_rank):
    """Third term of H_red: -(2/r) Re Tr(P X_w R_Q X_v P). Not an inverse."""
    return s.simplify(-2 * s.re(shell_trace) / shell_rank)


def kappa_scalar(eigenvalue, *, alpha, exponent, beta, fugacity, feedback_multiplicity, Z):
    """Owned spectral weight. Z is the full carrier trace, not a shell trace."""
    base = 1 - alpha * eigenvalue
    power = base ** (exponent - 1)
    return s.simplify(
        -power / Z
        + feedback_multiplicity * beta * fugacity * power
        / (1 - fugacity + fugacity * base ** exponent)
    )


def thermal_feedback_source(eigenvalues, jet_diagonal, jet_off, calibrations, *,
                            shell_mask, omit_normalizer=False, drop_outside_shell=False):
    """Full-carrier thermal/feedback source of an actual first jet.

    jet_diagonal[i] is the eigenbasis diagonal of Delta'.
    jet_off is a list of (i, j, value) with i != j.
    Dropping non-shell modes, or the rank-one Z derivative, is a refused
    reading: the returned comparison shows the lost term rather than using it.
    """
    if len(eigenvalues) != len(jet_diagonal) or len(shell_mask) != len(eigenvalues):
        raise MatterResponseError("thermal carrier, jet and shell mask disagree")
    alpha = calibrations["alpha"]
    exponent = calibrations["exponent"]
    beta = calibrations["beta"]
    fugacity = calibrations["fugacity"]
    feedback = calibrations["feedback_multiplicity"]
    Z = calibrations["Z"]
    multiplicities = calibrations.get("multiplicities", [1] * len(eigenvalues))
    g_values = [(1 - alpha * lam) ** (exponent - 1) for lam in eigenvalues]
    weights = [
        kappa_scalar(
            lam, alpha=alpha, exponent=exponent, beta=beta, fugacity=fugacity,
            feedback_multiplicity=feedback, Z=Z,
        )
        for lam in eigenvalues
    ]
    variable = s.symbols("thermal_eigenvalue")
    symbolic = kappa_scalar(
        variable, alpha=alpha, exponent=exponent, beta=beta, fugacity=fugacity,
        feedback_multiplicity=feedback, Z=Z,
    )
    derivative = s.diff(symbolic, variable)

    def weight_derivative(index):
        return s.simplify(derivative.subs(variable, eigenvalues[index]))

    def divided(i, j):
        if eigenvalues[i] == eigenvalues[j]:
            return weight_derivative(i)
        return s.simplify((weights[i] - weights[j]) / (eigenvalues[i] - eigenvalues[j]))

    dZ = -beta * sum(
        multiplicities[i] * g_values[i] * jet_diagonal[i] for i in range(len(eigenvalues))
    )
    dZ = s.simplify(dZ)
    first = s.Integer(0)
    shell_only = s.Integer(0)
    for i, diagonal in enumerate(jet_diagonal):
        term = multiplicities[i] * weights[i] * diagonal
        first += term
        if shell_mask[i]:
            shell_only += term
    first = s.simplify(first)
    shell_only = s.simplify(shell_only)
    # Rank-one normalizer, visible on every mode including the shell.
    normalizer_on_shell = s.Integer(0)
    if not omit_normalizer:
        for i, on_shell in enumerate(shell_mask):
            if on_shell:
                normalizer_on_shell += multiplicities[i] * g_values[i] * dZ / Z ** 2
    normalizer_on_shell = s.simplify(normalizer_on_shell)
    outside_diagonal = s.simplify(first - shell_only)
    # Second-source contraction of this same jet against itself, full carrier.
    second = s.Integer(0)
    for i, diagonal in enumerate(jet_diagonal):
        # Diagonal divided difference of the fixed-Z weight. The rank-one
        # normalizer is the separate contraction added after the off-diagonal loop.
        second += multiplicities[i] * weight_derivative(i) * diagonal * diagonal
    for i, j, value in jet_off:
        second += multiplicities[i] * divided(i, j) * value * s.conjugate(value)
    if not omit_normalizer:
        second += dZ / Z ** 2 * sum(
            multiplicities[i] * g_values[i] * jet_diagonal[i] for i in range(len(eigenvalues))
        )
        # The last sum is -dZ/beta, so this term is -dZ^2 /(beta Z^2). Kept
        # in the jet form above so a shell-supported probe still sees dZ.
    second = s.simplify(second)
    shell_probe = s.simplify(normalizer_on_shell)
    if drop_outside_shell:
        reported_first = shell_only
    else:
        reported_first = first
    return {
        "first_source": s.simplify(reported_first),
        "first_source_keeping_outside": first,
        "shell_truncation": shell_only,
        "outside_shell_diagonal_contribution": outside_diagonal,
        "normalizer_visible_on_shell": shell_probe,
        "normalizer_omitted": omit_normalizer,
        "outside_shell_dropped": drop_outside_shell,
        "second_contraction": second,
        "dZ": dZ,
        "feedback_multiplicity_used": feedback,
        "reference_rank_not_substituted": True,
        "matrix_free": True,
        "operation": "kappa_divided_difference",
    }


def gamma_second(d, o, rotated_norm_squared):
    """Owned positive coefficient of -E2 on each active +/- e2 block."""
    A = 128 + 64 * s.sqrt(2)
    B = 2 * A * (d + o)
    lam = 128 - 64 * s.sqrt(2)
    return s.simplify(lam * rotated_norm_squared * (1 + B / (B + 256 * o)) / 2)


def gamma_memo_form(d, o, rotated_norm_squared):
    """Same coefficient as written in the owner transport note."""
    lam = 128 - 64 * s.sqrt(2)
    numer = (2 + s.sqrt(2)) * (d + o) + o
    denom = (2 + s.sqrt(2)) * (d + o) + 2 * o
    return s.simplify(lam * rotated_norm_squared * numer / denom)


def row_wave_family(a, b):
    """Stored-adjoint row-2 rotation. Length acceleration is the matter repair.

    The nonroot frame a>b>0 is the owned rational chart, not a new root.
    phi is independent of x2, so the parallel-leg condition holds for every t.
    """
    if getattr(a, "is_number", False) and getattr(b, "is_number", False) and not (a > b > 0):
        raise MatterResponseError("row-wave chart requires a > b > 0")
    frame = (a - b) * s.eye(4) + b * s.ones(4)
    gram = s.simplify(frame * frame.T)
    d = s.simplify(gram[0, 0])
    o = s.simplify(gram[0, 1])
    leg = frame.row(2).T
    generator = s.zeros(4)
    generator[2, 3] = -1
    generator[3, 2] = 1
    rotated = s.simplify(generator * leg)
    rotated_norm = s.simplify((rotated.T * rotated)[0])
    gamma = gamma_second(d, o, rotated_norm)
    lam = 128 - 64 * s.sqrt(2)
    length = s.simplify(gamma / (2 * lam * d))
    x0, x1, x2 = s.symbols("x0 x1 x2", real=True)
    phi = s.cos(2 * s.pi * (3 * x0 + 3 * x1) / 8)
    blocks = {}
    for mode in SHELL_MOMENTA:
        active = mode[2] in (1, 7)
        blocks[mode] = s.simplify(-gamma if active else 0)
    repaired = {
        mode: s.simplify(value + (gamma if mode[2] in (1, 7) else 0))
        for mode, value in blocks.items()
    }
    return {
        "scope": "stored_rotational_row_wave",
        "stored_adjoint_admissible": bool(s.diff(phi, x2) == 0),
        "phi_independent_of_x2": True,
        "d": d,
        "o": o,
        "rotated_norm_squared": rotated_norm,
        "gamma": gamma,
        "length_acceleration": length,
        "leg_second_jet_identity": s.simplify((leg.T * (generator ** 2 * leg))[0] + rotated_norm),
        "shell_blocks_before_repair": blocks,
        "shell_blocks_after_repair": repaired,
        "shell_second_rows_repaired": all(is_zero(value) for value in repaired.values()),
        "nonscalar_within_block": False,
        "matter_second_contribution": s.simplify(-gamma / 4),
        "normal_response_nonzero": s.simplify(gamma) != 0,
        "normal_matter_response": "Q Psi' = -R_Q X Psi0 on k ± (3,3,0,0); shell fiber kept",
        "thermal_recomputed": False,
        "outside_shell_policy": "retained on the full carrier; this scope does not rerun the 8192-edge sum",
        "field_shell_kernel_solved": False,
        "declared_gauge": False,
        "physical_admission": False,
    }


def lattice_z(mode):
    """Literal L=8 symbol z_r = 8 (exp(2 pi i k_r/8) - 1)."""
    root = s.sqrt(2) / 2
    roots = (
        s.Integer(1),
        root * (1 + s.I),
        s.I,
        root * (-1 + s.I),
        s.Integer(-1),
        root * (-1 - s.I),
        -s.I,
        root * (1 - s.I),
    )
    return s.Matrix([8 * (roots[index % 8] - 1) for index in mode])


def symbol_quadratic(z_left, z_right, d, o):
    """z_left* G z_right for G = (d-o) I + o 11^T."""
    inner = sum(s.conjugate(z_left[i]) * z_right[i] for i in range(4))
    total_left = sum(z_left[i] for i in range(4))
    total_right = sum(z_right[i] for i in range(4))
    return s.expand((d - o) * inner + o * s.conjugate(total_left) * total_right)


def _partners(mode, wave=(3, 3, 0, 0)):
    return [
        tuple((mode[i] + sign * wave[i]) % 8 for i in range(4))
        for sign in (1, -1)
    ]


def car_trace_square(epsilon, energy, inner):
    """Owned full-16 trace Tr(X* X) for the conformal coefficient jet."""
    return (epsilon ** 2 + energy ** 2) / 2 + 2 * epsilon * energy + inner * s.conjugate(inner)


def occupied_second_trace(d, o, mode):
    """Owned scalar trace of E2_k. Not an operator replacement by that trace."""
    zk = lattice_z(mode)
    epsilon = s.simplify(symbol_quadratic(zk, zk, d, o))
    result = 6 * epsilon
    for partner in _partners(mode):
        zl = lattice_z(partner)
        energy = s.simplify(symbol_quadratic(zl, zl, d, o))
        inner = s.simplify(symbol_quadratic(zl, zk, d, o))
        square = car_trace_square(epsilon, energy, inner)
        result += energy - 2 * square / (energy - epsilon)
    return s.simplify(s.expand(result))


def occupied_trace_contrast(d, o):
    """Owned Tr E2_(e0) - Tr E2_(e2), negative for every d > o > 0."""
    rt2 = s.sqrt(2)
    polynomial = (14 + rt2) * d ** 2 + (2 + 2 * rt2) * d * o - (8 + 7 * rt2) * o ** 2
    return s.simplify(
        -64 * (d + 3 * o) * polynomial
        / ((d + o) * ((7 + 5 * rt2) * d + (11 + 8 * rt2) * o))
    )


def occupied_vacuum_defect(d, o, mode=(1, 0, 0, 0)):
    """Vacuum entry minus the full-16 mean. Nonscalar inside one Fock block."""
    zk = lattice_z(mode)
    epsilon = s.simplify(symbol_quadratic(zk, zk, d, o))
    defect = s.Integer(0)
    for partner in _partners(mode):
        zl = lattice_z(partner)
        energy = s.simplify(symbol_quadratic(zl, zl, d, o))
        inner = s.simplify(symbol_quadratic(zl, zk, d, o))
        defect += (epsilon * energy - inner * s.conjugate(inner)) / (4 * (energy - epsilon))
    return s.simplify(s.expand(defect))


def conformal_obstruction(d, o):
    """Coefficient wave is a different scope from the row-wave repair.

    dot G = phi G_* violates G_rr(x) = G_rr(x+r) along r = 0, 1.
    The nonscalar defect survives every scalar coefficient acceleration.
    """
    if getattr(d, "is_number", False) and getattr(o, "is_number", False) and not (d > o > 0):
        raise MatterResponseError("conformal sign domain is d > o > 0")
    x0, x1 = s.symbols("x0 x1", real=True)
    phi = s.cos(2 * s.pi * (3 * x0 + 3 * x1) / 8)
    shifted = s.simplify(phi.subs(x0, x0 + 1) - phi)
    defect = occupied_vacuum_defect(d, o)
    contrast = occupied_trace_contrast(d, o)
    return {
        "scope": "nonscalar_conformal_obstruction",
        "stored_adjoint_admissible": False,
        "diagonal_invariance_residual": shifted,
        "vacuum_defect": defect,
        "trace_contrast": contrast,
        "nonscalar_within_block": True,
        "scalar_repair_clears_defect": False,
        "shell_second_rows_repaired": False,
        "operator_shell_equation_held": False,
        "normal_matter_response": "Q response exists but does not cancel the nonscalar shell block",
        "field_shell_kernel_solved": False,
        "declared_gauge": False,
        "physical_admission": False,
        "reason": (
            "homogeneous scalar acceleration shifts E2 by a scalar matrix "
            "and leaves the vacuum-minus-mean defect unchanged"
        ),
    }


def solve_matter_response(delta_prime, delta_second, parameters):
    """Callable N07 imports.

    Inputs are an actual first jet, an actual second jet, and the allowed
    shell/reference parameters. Outputs are projected compatibility, the
    normal matter response, the remaining kernel coordinates, and the
    matter contribution to the first and second source.

    E = 0 and the traceless shell equation are retained. They are not
    solved by inverting the saddle, and free reference directions are
    not declared gauge. carrier='native_dense' is refused.
    """
    if delta_second is None:
        raise MatterResponseError("Delta'' is required; a missing second jet is not zero")
    carrier = parameters["carrier"]
    if carrier == "native_dense":
        refuse_native_dense_materialization(
            parameters.get("carrier_dim", CARRIER_DIM),
            parameters.get("shell_rank", SHELL_RANK),
            parameters.get("reference_rank", REFERENCE_RANK),
        )
    if carrier == "row_wave":
        family = row_wave_family(parameters["a"], parameters["b"])
        if delta_prime.get("scope") != family["scope"] or delta_second.get("scope") != family["scope"]:
            raise MatterResponseError("row-wave jets must carry the row-wave scope")
        coordinates = kernel_coordinates(SHELL_RANK, REFERENCE_RANK)
        compatible = all(is_zero(value) for value in family["shell_blocks_after_repair"].values())
        return _pack(
            scope=family["scope"],
            compatible=compatible,
            operator_equality_proved=True,
            normal=family["normal_matter_response"],
            normal_nonzero=family["normal_response_nonzero"],
            coordinates=coordinates,
            first={"matter": 0, "reason": "P X P = 0 on this wave; thermal dZ is not a general vanishing"},
            second={
                "matter_eliminated_term": family["matter_second_contribution"],
                "thermal_feedback_term": "not_recomputed_full_carrier_retained",
                "shell_multiplier_unsolved": True,
                "lower_saddle_block_inverted": False,
            },
            shell_held=compatible,
            extra=family,
            parameters=parameters,
        )
    if carrier == "conformal":
        obstacle = conformal_obstruction(parameters["d"], parameters["o"])
        if delta_prime.get("scope") != obstacle["scope"] or delta_second.get("scope") != obstacle["scope"]:
            raise MatterResponseError("conformal jets must carry the conformal scope")
        coordinates = kernel_coordinates(SHELL_RANK, REFERENCE_RANK)
        return _pack(
            scope=obstacle["scope"],
            compatible=False,
            operator_equality_proved=True,
            normal=obstacle["normal_matter_response"],
            normal_nonzero=True,
            coordinates=coordinates,
            first={"matter": "shell trace contrast is not a single epsilon'", "thermal": "full carrier required"},
            second={
                "matter_shell_blocks": "nonscalar; no common epsilon''",
                "vacuum_defect": obstacle["vacuum_defect"],
                "trace_contrast": obstacle["trace_contrast"],
                "scalar_repair_clears_defect": False,
                "lower_saddle_block_inverted": False,
            },
            shell_held=False,
            extra=obstacle,
            parameters=parameters,
        )
    if carrier != "block_fixture":
        raise MatterResponseError("unknown carrier")
    factors = off_shell_factors(
        parameters["delta"], parameters["epsilon"], parameters["U"], parameters["W"]
    )
    compatibility = projected_compatibility(
        factors["E"], parameters["tau"],
        schmidt_rank=parameters["schmidt_rank"],
        shell_rank=parameters["U"].cols,
    )
    linear = linear_shell_split(parameters["U"].H * delta_prime * parameters["U"],
                                full_schmidt=compatibility["full_schmidt"])
    built = reconstruction_factors(factors["J_Q"], parameters["tau"], parameters["V"])
    norm = normalization_value(parameters["tau"], factors["gram"])
    coordinates = kernel_coordinates(parameters["U"].cols, parameters["V"].cols)
    bound = uniform_shell_complement_bound(
        parameters.get("delta_op_norm", 1),
        parameters.get("epsilon_shift", 1),
        gap_exceeds_certified=parameters.get("gap_exceeds_certified", False),
    )
    first_matter = s.simplify(s.trace(parameters["tau"] * (
        parameters["U"] + parameters["W"] * factors["J_Q"]
    ).H * delta_prime * (
        parameters["U"] + parameters["W"] * factors["J_Q"]
    )))
    return _pack(
        scope="block_fixture",
        compatible=compatibility["compatible"] and (
            linear["operator_compatible"] is not False
        ),
        operator_equality_proved=compatibility["operator_equality_proved"],
        normal={"Q_factor": built["Q_factor"], "formula": built["formula"]},
        normal_nonzero=built["Q_factor"] != s.zeros(*built["Q_factor"].shape),
        coordinates=coordinates,
        first={"matter": first_matter, "normalization": norm},
        second={
            "Delta_second_retained": True,
            "matter_hessian_factor": "-2/r Re Tr(P X R_Q X P)",
            "lower_saddle_block_inverted": False,
            "shell_residual_T": linear["T"],
        },
        shell_held=compatibility["compatible"],
        extra={
            "factors": {key: factors[key] for key in ("E", "gram", "J_Q")},
            "linear": linear,
            "normalization": norm,
            "bound": bound,
            "compatibility": compatibility,
            "reconstruction": built,
        },
        parameters=parameters,
    )


def _pack(*, scope, compatible, operator_equality_proved, normal, normal_nonzero,
         coordinates, first, second, shell_held, extra, parameters):
    return {
        "scope": scope,
        "projected_compatibility": {
            "compatible": compatible,
            "operator_equality_proved": operator_equality_proved,
            "pure16_accepted": False,
        },
        "normal_matter_response": normal,
        "normal_response_nonzero": bool(normal_nonzero),
        "remaining_kernel_coordinates": coordinates,
        "first_source": first,
        "second_source": second,
        "shell_equations_satisfied": bool(shell_held),
        "shell_equations_retained": True,
        "E0_retained": True,
        "engine_narrower_than_full_hermitian_sphere": True,
        "field_shell_kernel_solved": False,
        "lower_saddle_block_inverted": False,
        "declared_gauge": False,
        "physical_admission": False,
        "gr_derived": False,
        "excluded_real_coordinates_materialized": 0,
        "matrix_free_operations": MATRIX_FREE_OPERATIONS,
        "gq_bound_domain": "||G_Q||<4 only for certified gap > 1/2 and the open 1/8 window",
        "extra": extra,
        "reference_rank": parameters.get("reference_rank", REFERENCE_RANK),
    }


def pure16_native_reduction(shell_rank, reference_rank):
    """The owned shell is the 128-state purification, not a raw 16-vector."""
    if shell_rank == FOCK_RANK or reference_rank == FOCK_RANK or shell_rank != SHELL_RANK:
        raise MatterResponseError(
            "false pure16 reduction: shell128 and reference128 stay in place"
        )
    return {"shell_rank": shell_rank, "reference_rank": reference_rank, "accepted": True}
