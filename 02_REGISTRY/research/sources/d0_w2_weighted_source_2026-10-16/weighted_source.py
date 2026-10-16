#!/usr/bin/env python3
"""Fixed-carrier transport of a supplied positive site weight.

omega_x > 0 is an input field. It is not a PF probability and not a
geometric volume. The literal stored operator is conjugated; it is not
replaced by d + d†.

Consumed, not re-proved: the unweighted edge law and the whitening
identities of A4D_NATIVE_JOINT_ADJOINT_SOURCE and section 0.3 of
A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT at
74e62cdc716e10883accba9d34ccf0e21d58eb65. The ACDB/ABCD sign bridge is a
site-independent fibre similarity, so it does not change endpoint factors.
"""
from __future__ import annotations

import math
from typing import Iterable

import numpy as np

PINNED_SOURCE = "74e62cdc716e10883accba9d34ccf0e21d58eb65"
JOINT_KERNEL_DELTA = "33267713b2e6d3e78af7789547b00f50cdceb43d"
FIBER = 16
# Exact extra source for a later raw-norm budget. Do not drop it, and do
# not fold it into C, M, a counting trace, or a PF weight.
EXTRA_SOURCE_NOT_TO_DROP = (
    "endpoint factor sqrt(omega_x/omega_y) on the conjugated stored shift, "
    "and the edge jet (1/2)(d log omega_x - d log omega_y) in [K, hat D]; "
    "not a PF probability, not a geometric volume, not a rescaling of C or M"
)


def _as_vector(v: Iterable[float]) -> np.ndarray:
    out = np.asarray(list(v), dtype=float)
    if out.shape != (4,):
        raise ValueError("expected a 4-vector")
    return out


def _as_matrix(a: Iterable[Iterable[float]]) -> np.ndarray:
    out = np.asarray(a, dtype=float)
    if out.shape != (4, 4):
        raise ValueError("expected a 4x4 matrix")
    return out


def creation(v: Iterable[float]) -> np.ndarray:
    """Euclidean exterior creation on the sorted bit basis, C(v) alpha = v wedge alpha."""
    coeff = _as_vector(v)
    matrix = np.zeros((FIBER, FIBER))
    for mask in range(FIBER):
        for role in range(4):
            if mask & (1 << role):
                continue
            if coeff[role] == 0.0:
                continue
            sign = 1.0 if bin(mask & ((1 << role) - 1)).count("1") % 2 == 0 else -1.0
            matrix[mask | (1 << role), mask] += sign * coeff[role]
    return matrix


def contraction(v: Iterable[float]) -> np.ndarray:
    """Euclidean interior product, the counting adjoint of creation(v)."""
    return creation(v).T


def exterior_lift(linear: Iterable[Iterable[float]]) -> np.ndarray:
    """Induced map on the sorted exterior basis. Degree 0 is 1."""
    matrix = _as_matrix(linear)
    out = np.zeros((FIBER, FIBER))
    bits = [tuple(i for i in range(4) if mask & (1 << i)) for mask in range(FIBER)]
    for row, row_bits in enumerate(bits):
        for col, col_bits in enumerate(bits):
            if len(row_bits) != len(col_bits):
                continue
            if not row_bits:
                out[row, col] = 1.0
            else:
                minor = matrix[np.ix_(row_bits, col_bits)]
                out[row, col] = float(np.linalg.det(minor))
    return out


def gamma_action(generator: Iterable[Iterable[float]]) -> np.ndarray:
    """Derivative of exterior_lift at the identity, Leibniz rule."""
    gen = _as_matrix(generator)
    out = np.zeros((FIBER, FIBER))
    for mask in range(FIBER):
        bits = [i for i in range(4) if mask & (1 << i)]
        for pos, role in enumerate(bits):
            sign_remove = 1.0 if pos % 2 == 0 else -1.0
            rest = mask ^ (1 << role)
            for image in range(4):
                coeff = gen[image, role]
                if coeff == 0.0 or rest & (1 << image):
                    continue
                sign_insert = 1.0 if bin(rest & ((1 << image) - 1)).count("1") % 2 == 0 else -1.0
                dest = rest | (1 << image)
                out[dest, mask] += sign_remove * sign_insert * coeff
    return out


def acdb_phase() -> np.ndarray:
    """Site-independent sign bridge consumed from the soldered packet.

    Diagonal entries are (-1)**(bit1 * (bit2 + bit3)) on masks 0..15.
    """
    signs = [
        (-1) ** (int(bool(mask & 2)) * (int(bool(mask & 4)) + int(bool(mask & 8))))
        for mask in range(FIBER)
    ]
    return np.diag(np.asarray(signs, dtype=float))


def block_diag(blocks: list[np.ndarray]) -> np.ndarray:
    if not blocks:
        raise ValueError("empty block list")
    fiber = blocks[0].shape[0]
    out = np.zeros((len(blocks) * fiber, len(blocks) * fiber))
    for index, block in enumerate(blocks):
        if block.shape != (fiber, fiber):
            raise ValueError("inconsistent fibre blocks")
        start = index * fiber
        out[start : start + fiber, start : start + fiber] = block
    return out


def cycle_transport(blocks: list[np.ndarray]) -> np.ndarray:
    """(S phi)(x) = blocks[x] phi(x+1), one oriented cycle."""
    count = len(blocks)
    fiber = blocks[0].shape[0]
    out = np.zeros((count * fiber, count * fiber))
    for arrival, block in enumerate(blocks):
        source = (arrival + 1) % count
        row = arrival * fiber
        col = source * fiber
        out[row : row + fiber, col : col + fiber] = block
    return out


def cycle_inverse(blocks: list[np.ndarray]) -> np.ndarray:
    count = len(blocks)
    fiber = blocks[0].shape[0]
    out = np.zeros((count * fiber, count * fiber))
    for arrival, block in enumerate(blocks):
        source = (arrival + 1) % count
        inverse = np.linalg.inv(block)
        row = source * fiber
        col = arrival * fiber
        out[row : row + fiber, col : col + fiber] = inverse
    return out


def cycle_adjoint(blocks: list[np.ndarray]) -> np.ndarray:
    """Counting adjoint on the whitened Euclidean fibre."""
    count = len(blocks)
    fiber = blocks[0].shape[0]
    out = np.zeros((count * fiber, count * fiber))
    for arrival, block in enumerate(blocks):
        source = (arrival + 1) % count
        row = source * fiber
        col = arrival * fiber
        out[row : row + fiber, col : col + fiber] = block.T
    return out


def require_positive_weights(omega: Iterable[float]) -> np.ndarray:
    weights = np.asarray(list(omega), dtype=float)
    if weights.ndim != 1 or weights.size < 2:
        raise ValueError("expected at least two site weights")
    if np.any(weights <= 0.0):
        raise ValueError("site weight must be positive")
    return weights


def endpoint_factor(omega_arrival: float, omega_source: float) -> float:
    if omega_arrival <= 0.0 or omega_source <= 0.0:
        raise ValueError("site weight must be positive")
    return math.sqrt(omega_arrival / omega_source)


def endpoint_blocks(omega: Iterable[float], linears: list[np.ndarray]) -> list[np.ndarray]:
    """Conjugated shift blocks with both endpoint factors.

    Arrival x reads source y = x+1 through sqrt(omega_x/omega_y) Lambda(O_xy).
    """
    weights = require_positive_weights(omega)
    if len(linears) != len(weights):
        raise ValueError("one linear map per oriented edge")
    blocks = []
    for arrival, linear in enumerate(linears):
        source = (arrival + 1) % len(weights)
        factor = endpoint_factor(float(weights[arrival]), float(weights[source]))
        blocks.append(factor * exterior_lift(linear))
    return blocks


def frozen_endpoint_blocks(
    omega: Iterable[float],
    linears: list[np.ndarray],
    mode: str,
) -> list[np.ndarray]:
    """Incorrect one-sided weights. Not a transport of the supplied field."""
    weights = require_positive_weights(omega)
    if len(linears) != len(weights):
        raise ValueError("one linear map per oriented edge")
    blocks = []
    for arrival, linear in enumerate(linears):
        source = (arrival + 1) % len(weights)
        if mode == "freeze_source":
            factor = endpoint_factor(float(weights[arrival]), float(weights[arrival]))
        elif mode == "freeze_arrival":
            factor = endpoint_factor(float(weights[source]), float(weights[source]))
        elif mode == "absolute_arrival_only":
            factor = math.sqrt(float(weights[arrival]))
        else:
            raise ValueError("unknown frozen-weight mode")
        blocks.append(factor * exterior_lift(linear))
    return blocks


def edge_log_derivative(dlog_arrival: float, dlog_source: float) -> float:
    """Logarithmic derivative of sqrt(omega_arrival/omega_source)."""
    return 0.5 * (dlog_arrival - dlog_source)


def edge_self_adjoint_law(
    linear: Iterable[Iterable[float]],
    u_arrival: Iterable[float],
    u_source: Iterable[float],
    omega_arrival: float,
    omega_source: float,
) -> dict[str, object]:
    """Necessary and sufficient fibre law for one oriented edge.

    O^T O = I + (kappa-1) P and O^T u_arrival = (omega_source/omega_arrival) u_source.
    A vanishing leg makes the contraction identity vacuous for every invertible O.
    """
    if omega_arrival <= 0.0 or omega_source <= 0.0:
        raise ValueError("site weight must be positive")
    op = _as_matrix(linear)
    left = _as_vector(u_arrival)
    right = _as_vector(u_source)
    ratio = omega_source / omega_arrival
    leg = op.T @ left - ratio * right
    gram = op.T @ op
    axis_norm = float(np.linalg.norm(right))
    if axis_norm < 1e-12:
        holds = float(np.linalg.norm(leg)) < 1e-9
        return {
            "holds": holds,
            "kappa": None,
            "vacuous_leg": True,
            "leg_residual": float(np.linalg.norm(leg)),
            "quadratic_residual": 0.0,
            "weight_ratio": ratio,
        }
    axis = right / axis_norm
    projector = np.outer(axis, axis)
    excess = gram - np.eye(4)
    kappa = 1.0 + float(axis @ excess @ axis)
    quadratic = excess - (kappa - 1.0) * projector
    holds = (
        float(np.linalg.norm(leg)) < 1e-8
        and float(np.linalg.norm(quadratic)) < 1e-8
        and kappa > 0.0
    )
    return {
        "holds": holds,
        "kappa": kappa,
        "vacuous_leg": False,
        "leg_residual": float(np.linalg.norm(leg)),
        "quadratic_residual": float(np.linalg.norm(quadratic)),
        "weight_ratio": ratio,
    }


def local_creation(legs: list[np.ndarray]) -> np.ndarray:
    return block_diag([creation(leg) for leg in legs])


def local_contraction(legs: list[np.ndarray]) -> np.ndarray:
    return block_diag([contraction(leg) for leg in legs])


def whitened_literal_dirac(
    legs: list[np.ndarray],
    shift_blocks: list[np.ndarray],
    inv_ell: float,
) -> np.ndarray:
    """Literal stored conjugate: creators on S and contractions on S^{-1}.

    This is I D I^{-1}. It is not the counting adjoint completion.
    """
    if inv_ell == 0.0:
        raise ValueError("mesh factor inv_ell must be nonzero")
    shift = cycle_transport(shift_blocks)
    backward = cycle_inverse(shift_blocks)
    identity = np.eye(shift.shape[0])
    creators = local_creation(legs)
    contractions = local_contraction(legs)
    return inv_ell * (creators @ (shift - identity) + contractions @ (backward - identity))


def forced_adjoint_completion(
    legs: list[np.ndarray],
    shift_blocks: list[np.ndarray],
    inv_ell: float,
) -> np.ndarray:
    """Habit d + d†. A different operator unless the edge law already holds."""
    if inv_ell == 0.0:
        raise ValueError("mesh factor inv_ell must be nonzero")
    shift = cycle_transport(shift_blocks)
    identity = np.eye(shift.shape[0])
    raising = inv_ell * local_creation(legs) @ (shift - identity)
    return raising + raising.T


def naive_inverse_swap(
    legs: list[np.ndarray],
    shift_blocks: list[np.ndarray],
    inv_ell: float,
) -> np.ndarray:
    """Replace S^{-1} by S* inside the contraction slot. Not the adjoint."""
    if inv_ell == 0.0:
        raise ValueError("mesh factor inv_ell must be nonzero")
    forward = cycle_transport(shift_blocks)
    backward = cycle_adjoint(shift_blocks)
    identity = np.eye(forward.shape[0])
    creators = local_creation(legs)
    contractions = local_contraction(legs)
    return inv_ell * (creators @ (forward - identity) + contractions @ (backward - identity))


def fibre_adjoint_identity(
    linear: Iterable[Iterable[float]],
    u_arrival: Iterable[float],
    u_source: Iterable[float],
    omega_arrival: float,
    omega_source: float,
) -> np.ndarray:
    """(omega_arrival/omega_source) U^T i(u_arrival) U - i(u_source). Zero iff the law holds."""
    op = exterior_lift(linear)
    scale = omega_arrival / omega_source
    left = scale * (op.T @ contraction(u_arrival) @ op)
    return left - contraction(u_source)


def whitening_blocks(omega: Iterable[float], square_roots: list[np.ndarray]) -> list[np.ndarray]:
    """I_x = sqrt(omega_x) Lambda(L_x), L_x a supplied positive square root of h_x."""
    weights = require_positive_weights(omega)
    if len(square_roots) != len(weights):
        raise ValueError("one square root per site")
    blocks = []
    for weight, root in zip(weights, square_roots):
        blocks.append(math.sqrt(float(weight)) * exterior_lift(root))
    return blocks


def observer_generator(
    dlog_omega: float,
    square_root: Iterable[Iterable[float]],
    d_square_root: Iterable[Iterable[float]],
) -> np.ndarray:
    """K = (1/2) d log omega + Gamma(Ldot L^{-1}) on one fibre."""
    root = _as_matrix(square_root)
    velocity = _as_matrix(d_square_root)
    left_log = velocity @ np.linalg.inv(root)
    return 0.5 * dlog_omega * np.eye(FIBER) + gamma_action(left_log)


def raw_stored_dirac(
    raw_legs: list[np.ndarray],
    link_blocks: list[np.ndarray],
    metrics: list[np.ndarray],
    inv_ell: float,
) -> np.ndarray:
    """Literal d + ell in the fixed exterior component basis.

    d uses C(v)(T-I) and ell uses i_(h v)(T^{-1}-I). No weight is inserted.
    """
    if inv_ell == 0.0:
        raise ValueError("mesh factor inv_ell must be nonzero")
    shift_blocks = [exterior_lift(link) for link in link_blocks]
    shift = cycle_transport(shift_blocks)
    backward = cycle_inverse(shift_blocks)
    identity = np.eye(shift.shape[0])
    creators = local_creation(raw_legs)
    lowered = [metric @ leg for metric, leg in zip(metrics, raw_legs)]
    contractions = local_contraction(lowered)
    return inv_ell * (creators @ (shift - identity) + contractions @ (backward - identity))


def weighted_gram_blocks(omega: Iterable[float], square_roots: list[np.ndarray]) -> list[np.ndarray]:
    """Component Gram omega_x Lambda(L_x)^T Lambda(L_x). Not a PF measure."""
    weights = require_positive_weights(omega)
    grams = []
    for weight, root in zip(weights, square_roots):
        lifted = exterior_lift(root)
        grams.append(float(weight) * (lifted.T @ lifted))
    return grams


def weighted_inner(left: np.ndarray, right: np.ndarray, grams: list[np.ndarray]) -> float:
    total = 0.0
    fiber = grams[0].shape[0]
    for index, gram in enumerate(grams):
        start = index * fiber
        piece_l = left[start : start + fiber]
        piece_r = right[start : start + fiber]
        total += float(piece_l @ gram @ piece_r)
    return total


def corrected_unitary_blocks(
    omega: Iterable[float],
    link_blocks: list[np.ndarray],
) -> list[np.ndarray]:
    """Weight-corrected transport, unitary on the weighted Gram when A preserves h.

    (U psi)(x) = sqrt(omega_y/omega_x) Lambda(A_xy) psi(y). This is not the stored shift.
    """
    weights = require_positive_weights(omega)
    blocks = []
    for arrival, link in enumerate(link_blocks):
        source = (arrival + 1) % len(weights)
        factor = endpoint_factor(float(weights[source]), float(weights[arrival]))
        blocks.append(factor * exterior_lift(link))
    return blocks


def counting_unitary(operator: np.ndarray, atol: float = 1e-8) -> bool:
    size = operator.shape[0]
    gram = operator.T @ operator
    return bool(np.allclose(gram, np.eye(size), atol=atol, rtol=0.0))


def scalar_price(
    operator: np.ndarray,
    rho: np.ndarray,
    *,
    alpha: float,
    m: int,
    z: float,
    C: float,
    M: float,
) -> dict[str, float]:
    """Unchanged v8 scalar price on one finite symmetric operator.

    C and M stay external bookkeeping factors. They are not multiplied by
    a site-weight sum, and the counting trace is not renamed as a PF measure.
    """
    if alpha <= 0.0 or m < 1 or not (0.0 <= z < 1.0) or C <= 0.0 or M <= 0.0:
        raise ValueError("price calibrations must stay in the declared window")
    if operator.shape != rho.shape or operator.ndim != 2:
        raise ValueError("operator and rho must be square of one size")
    if not np.allclose(operator, operator.T, atol=1e-8):
        raise ValueError("scalar price is only read on a symmetric stored operator")
    delta = operator @ operator
    identity = np.eye(operator.shape[0])
    survival = identity - alpha * delta
    eigenvalues = np.linalg.eigvalsh(survival)
    if np.any(eigenvalues <= 0.0):
        raise ValueError("outside the positive survival window")
    kernel = np.linalg.matrix_power(survival, m)
    feedback = (1.0 - z) * identity + z * kernel
    feedback_eigenvalues = np.linalg.eigvalsh(feedback)
    if np.any(feedback_eigenvalues <= 0.0):
        raise ValueError("feedback factor is not positive")
    raw_trace = float(np.trace(kernel))
    if raw_trace <= 0.0:
        raise ValueError("raw survival trace vanished")
    beta = m * alpha
    matter = float(np.trace(rho @ delta))
    heat = math.log(C * raw_trace) / beta
    program = -M * float(np.sum(np.log(feedback_eigenvalues)))
    sigma_trace = float(np.trace(kernel / raw_trace))
    return {
        "S": matter + heat + program,
        "R": matter,
        "heat": heat,
        "program": program,
        "Z_raw": raw_trace,
        "sigma_trace": sigma_trace,
        "C": float(C),
        "M": float(M),
        "beta": beta,
    }


def source_one_form(
    operator: np.ndarray,
    rho: np.ndarray,
    d_operator: np.ndarray,
    d_rho: np.ndarray,
    *,
    alpha: float,
    m: int,
    z: float,
    M: float,
) -> float:
    """First source Tr((D W + W D) dD) + Tr(Delta d rho), fixed C, beta, z, M.

    W = rho - B^{m-1}/Z + M beta z B^{m-1} A^{-1}, as in the consumed price jet.
    """
    if alpha <= 0.0 or m < 1 or not (0.0 <= z < 1.0) or M <= 0.0:
        raise ValueError("source calibrations must stay in the declared window")
    identity = np.eye(operator.shape[0])
    delta = operator @ operator
    survival = identity - alpha * delta
    if np.any(np.linalg.eigvalsh(0.5 * (survival + survival.T)) <= 0.0):
        raise ValueError("outside the positive survival window")
    power = np.linalg.matrix_power(survival, m - 1)
    kernel = power @ survival
    raw_trace = float(np.trace(kernel))
    feedback = (1.0 - z) * identity + z * kernel
    beta = m * alpha
    weight = (
        rho
        - power / raw_trace
        + (M * beta * z) * (power @ np.linalg.inv(feedback))
    )
    commutator_term = (operator @ weight + weight @ operator) @ d_operator
    return float(np.trace(commutator_term) + np.trace(delta @ d_rho))


def site_masses(operator: np.ndarray, sites: int) -> np.ndarray:
    fiber = operator.shape[0] // sites
    masses = np.zeros(sites)
    for index in range(sites):
        start = index * fiber
        masses[index] = float(np.trace(operator[start : start + fiber, start : start + fiber]))
    return masses


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def max_abs(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(matrix))) if matrix.size else 0.0
