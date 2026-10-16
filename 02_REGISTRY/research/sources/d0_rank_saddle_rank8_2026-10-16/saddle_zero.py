"""Candidate shape of the rank-8 saddle on V_field ⊕ V_k.

Equations (16)–(18) of A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION
at ec45c8cc4085e7bce888d97439251be9e578d4ff. The lower-right block is the
zero form. It is not inverted, and a positive thermal or auxiliary Hessian
is not written into that block or into T_k.

This module does not solve the field kernel, does not build a nonlinear
branch, and does not derive a gravitational equation.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import sympy as s

MEMO_COMMIT = "ec45c8cc4085e7bce888d97439251be9e578d4ff"
MEMO_PATH = "02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"
MEMO_SHA256 = "8ec54e4838aaa579469896eeaf369e16a24d6a6f0f67824ede6fa88f5cb9b622"

SHELL_RANK = 128
OCCUPIED_RANK = 8
RANK8_VK = 1983
FULL_RANK_VK = 16383

MEMO_ANCHORS = (
    "T_k(v)=Pi X_v Pi-Tr(Pi X_v)Pi/k",
    "(P-Pi)X_v Pi+Pi X_v(P-Pi).",
    "[ H_rho  T_k* ] [v] = 0,",
    "[ T_k      0  ] [S]",
    "Нижний нулевой блок не обращается",
    "dim_R V_k=2rk-k²-1.",
)


class ZeroBlockError(RuntimeError):
    """The shell block of the rank-8 saddle is zero and is not a pivot."""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def vk_dimension(shell: int, occupied: int) -> int:
    """Real dimension of traceless Hermitian matrices with zero empty-empty block."""
    return 2 * shell * occupied - occupied * occupied - 1


def memo_bytes() -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{MEMO_COMMIT}:{MEMO_PATH}"],
        cwd=repo_root(),
    )


def t_entry(i: int, j: int, occupied: int, x_ij, trace):
    """One entry of (16) in a basis adapted to the occupied projector."""
    row = i < occupied
    col = j < occupied
    if row and col:
        if i == j:
            return s.sympify(x_ij) - s.sympify(trace) / s.Integer(occupied)
        return x_ij
    if row or col:
        return x_ij
    return s.Integer(0)


def _occupied_trace(matrix, occupied: int):
    total = s.Integer(0)
    for i in range(occupied):
        total += matrix[i][i]
    return total


def t_matrix(matrix, occupied: int):
    size = len(matrix)
    trace = _occupied_trace(matrix, occupied)
    return [
        [t_entry(i, j, occupied, matrix[i][j], trace) for j in range(size)]
        for i in range(size)
    ]


def t_matrix_projectors(matrix, occupied: int):
    """Literal products Pi X Pi - (Tr Pi X / k) Pi + Q X Pi + Pi X Q."""
    size = len(matrix)
    occupied_mask = [1 if i < occupied else 0 for i in range(size)]
    empty_mask = [1 - bit for bit in occupied_mask]
    trace = _occupied_trace(matrix, occupied)
    shift = s.sympify(trace) / s.Integer(occupied)
    out = []
    for i in range(size):
        row = []
        for j in range(size):
            value = matrix[i][j]
            assembled = (
                occupied_mask[i] * value * occupied_mask[j]
                + empty_mask[i] * value * occupied_mask[j]
                + occupied_mask[i] * value * empty_mask[j]
            )
            if occupied_mask[i] and i == j:
                assembled -= shift
            row.append(assembled)
        out.append(row)
    return out


def frobenius(left, right):
    """Tr(left @ right) when right is Hermitian: sum left_ij * conjugate(right_ij)."""
    size = len(left)
    total = left[0][0] * 0
    for i in range(size):
        for j in range(size):
            total += left[i][j] * s.conjugate(right[i][j])
    return total


def trace_product(left, right):
    size = len(left)
    total = left[0][0] * 0
    for i in range(size):
        for j in range(size):
            total += left[i][j] * right[j][i]
    return total


def hermitian_from_pattern(size: int):
    """Deterministic Hermitian matrix with every block nonzero."""
    matrix = [[s.Integer(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i, size):
            real = s.Rational((3 * i + 5 * j) % 9 + 1, (i + 4 * j) % 7 + 1)
            if i == j:
                matrix[i][j] = real
                continue
            imag = s.Rational((2 * i + j) % 5 + 1, (i + j) % 3 + 2)
            matrix[i][j] = real + s.I * imag
            matrix[j][i] = real - s.I * imag
    return matrix


def symbolic_hermitian(size: int):
    matrix = [[s.Integer(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        matrix[i][i] = s.symbols(f"d{i}", real=True)
        for j in range(i + 1, size):
            real = s.symbols(f"a{i}_{j}", real=True)
            imag = s.symbols(f"b{i}_{j}", real=True)
            matrix[i][j] = real + s.I * imag
            matrix[j][i] = real - s.I * imag
    return matrix


def symbolic_vk(occupied: int, empty: int):
    """Generic point of V_k: trace zero and empty-empty block zero."""
    size = occupied + empty
    matrix = [[s.Integer(0) for _ in range(size)] for _ in range(size)]
    free = [s.symbols(f"s{i}", real=True) for i in range(occupied - 1)]
    for i, value in enumerate(free):
        matrix[i][i] = value
    matrix[occupied - 1][occupied - 1] = -sum(free, s.Integer(0))
    for i in range(occupied):
        for j in range(i + 1, occupied):
            real = s.symbols(f"p{i}_{j}", real=True)
            imag = s.symbols(f"q{i}_{j}", real=True)
            matrix[i][j] = real + s.I * imag
            matrix[j][i] = real - s.I * imag
    for i in range(occupied):
        for alpha in range(empty):
            j = occupied + alpha
            real = s.symbols(f"u{i}_{alpha}", real=True)
            imag = s.symbols(f"v{i}_{alpha}", real=True)
            matrix[i][j] = real + s.I * imag
            matrix[j][i] = real - s.I * imag
    return matrix


def in_vk(matrix, occupied: int) -> bool:
    size = len(matrix)
    trace = _occupied_trace(matrix, occupied)
    if s.expand(trace) != 0:
        return False
    for i in range(occupied, size):
        for j in range(occupied, size):
            if s.expand(matrix[i][j]) != 0:
                return False
    for i in range(size):
        for j in range(size):
            if s.expand(matrix[j][i] - s.conjugate(matrix[i][j])) != 0:
                return False
    return True


def matrices_equal(left, right) -> bool:
    if len(left) != len(right):
        return False
    for i, row in enumerate(left):
        for j, value in enumerate(row):
            if s.expand(value - right[i][j]) != 0:
                return False
    return True


def add_matrices(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left))]
        for i in range(len(left))
    ]


def scale_matrix(factor, matrix):
    return [[factor * matrix[i][j] for j in range(len(matrix))] for i in range(len(matrix))]


def occupied_traceless_witness(shell: int, occupied: int):
    """η = E_00 - E_11. Trace zero, empty block zero, so η lies in V_k."""
    matrix = [[s.Integer(0) for _ in range(shell)] for _ in range(shell)]
    matrix[0][0] = s.Integer(1)
    matrix[1][1] = s.Integer(-1)
    return matrix


def rectangular_witness(shell: int, occupied: int):
    """Real occupied-empty coherence. Empty-empty block stays zero."""
    matrix = [[s.Integer(0) for _ in range(shell)] for _ in range(shell)]
    slot = occupied
    matrix[0][slot] = s.Integer(1)
    matrix[slot][0] = s.Integer(1)
    return matrix


def pure_empty_witness(shell: int, occupied: int):
    """Traceless empty-empty matrix. This is not an element of V_k."""
    matrix = [[s.Integer(0) for _ in range(shell)] for _ in range(shell)]
    matrix[occupied][occupied] = s.Integer(1)
    matrix[occupied + 1][occupied + 1] = s.Integer(-1)
    return matrix


def hessian_diagonal(linear_coeff: int, scale: int) -> int:
    """Centered second difference of (1/2) scale x^2 + linear_coeff x on ±e_i."""
    if scale % 2 != 0:
        raise ValueError("scale must be even so the quadratic term stays integral")
    half = scale // 2
    return (linear_coeff + half) + (-linear_coeff + half)


def hessian_off(left_coeff: int, right_coeff: int, scale: int) -> int:
    """Polarization (Q(e_i+e_j) - Q(e_i-e_j)) / 4 of the same Lagrangian."""
    if scale % 2 != 0:
        raise ValueError("scale must be even so the quadratic term stays integral")
    plus = (left_coeff + right_coeff + scale) + (-(left_coeff + right_coeff) + scale)
    minus = (left_coeff - right_coeff + scale) + (-left_coeff + right_coeff + scale)
    gap = plus - minus
    if gap % 4 != 0:
        raise ValueError("off-diagonal polarization is not an integer Hessian entry")
    return gap // 4


def scan_lower_block(dimension: int, scale: int) -> dict:
    """Hessian matrix of dot(s, t) + (scale/2) ||s||^2 on R^dimension.

    scale = 0 is the memo saddle. A positive scale is an auxiliary shell Hessian.
    """
    if dimension <= 0:
        raise ValueError("V_k dimension must be positive")
    linear = [(index % 7) - 3 for index in range(dimension)]
    nonzero = 0
    diagonal_mismatch = 0
    off_mismatch = 0
    first_diagonal = hessian_diagonal(linear[0], scale)
    first_off = hessian_off(linear[0], linear[1], scale) if dimension > 1 else 0
    for i in range(dimension):
        diagonal = hessian_diagonal(linear[i], scale)
        if diagonal != scale:
            diagonal_mismatch += 1
        if diagonal != 0:
            nonzero += 1
        coeff = linear[i]
        for j in range(i + 1, dimension):
            off = hessian_off(coeff, linear[j], scale)
            if off != 0:
                off_mismatch += 1
                nonzero += 1
    pairs = dimension * (dimension + 1) // 2
    return {
        "dimension": dimension,
        "scale": scale,
        "pairs": pairs,
        "nonzero": nonzero,
        "diagonal_mismatch": diagonal_mismatch,
        "off_mismatch": off_mismatch,
        "first_diagonal": first_diagonal,
        "first_off": first_off,
    }


def thermal_quadratic(matrix, occupied: int):
    """k Tr(S^2), the equal-eigenvalue entropy Hessian extended by the same formula.

    On the occupied block at ρ = I_k/k this is the second variation of Tr(σ log σ).
    On empty-empty directions that extension is auxiliary: log is singular there.
    """
    return occupied * frobenius(matrix, matrix)


def entropy_second_variation(occupied: int = OCCUPIED_RANK):
    """Second t-derivative of Tr((ρ + t η) log(ρ + t η)) at the uniform state.

    ρ = I_k/k and η = E_01 + E_10. Equal eigenvalues make every divided
    difference of log equal to k, so the result is k Tr(η^2).
    """
    t = s.symbols("t", real=True)
    level = s.Rational(1, occupied)
    block = s.Matrix([[level, t], [t, level]])
    eigenvalues = list(block.eigenvals().keys())
    moving = sum(value * s.log(value) for value in eigenvalues)
    frozen = (occupied - 2) * level * s.log(level)
    second = s.simplify(s.diff(moving + frozen, t, 2).subs(t, 0))
    eta_square = s.Integer(2)
    return {"second": second, "k_tr_eta_square": occupied * eta_square}


def empty_log_divided_difference(occupied: int = OCCUPIED_RANK):
    """(log(1/k) - log ε) / (1/k - ε) as ε → 0+. The empty eigenvalue has no finite log Hessian."""
    eps = s.symbols("eps", positive=True)
    level = s.Rational(1, occupied)
    quotient = (s.log(level) - s.log(eps)) / (level - eps)
    return s.limit(quotient, eps, 0, dir="+")


def diagonal_sum_of_squares_minors(occupied: int = OCCUPIED_RANK) -> list:
    """Leading minors of the traceless diagonal form sum d_i^2 + (sum d_i)^2.

    The m-th minor of I + 11^T equals 1 + m. All are positive.
    """
    minors = []
    for width in range(1, occupied):
        gram = s.eye(width) + s.ones(width)
        minors.append(s.simplify(gram.det()))
    return minors


def linear_shell_second_difference(left, right, fixed):
    """Second difference of S ↦ Tr(S fixed) . It is zero for every fixed coupling."""

    def evaluate(matrix):
        return frobenius(matrix, fixed)

    zero = [[0 for _ in range(len(left))] for _ in range(len(left))]
    return evaluate(add_matrices(left, right)) - evaluate(left) - evaluate(right) + evaluate(zero)


def invert_lower_block(lower_scale: int):
    """Do not invert the physical zero block, and do not Schur-reduce a substitute."""
    del lower_scale
    raise ZeroBlockError(
        "the rank-8 lower block on V_k is zero and is not inverted"
    )


def shape_accepts(report: dict) -> bool:
    """True only for the memo saddle (18): zero lower block and off-diagonal T_k."""
    return bool(
        report["vk_dimension"] == RANK8_VK
        and report["lower_nonzero"] == 0
        and report["lower_quadratic_on_witness"] == 0
        and report["pairing_gap"] == 0
        and report["off_diagonal_is_t_k"] is True
        and report["inverted"] is False
        and report["thermal_matrix_replaced_t_k"] is False
    )


def candidate_flags() -> dict:
    return {
        "status": "candidate",
        "shell": SHELL_RANK,
        "occupied_rank": OCCUPIED_RANK,
        "vk_dimension": RANK8_VK,
        "lower_block": "zero",
        "lower_block_inverted": False,
        "thermal_hessian_substituted": False,
        "t_k_replaced_by_positive_thermal_matrix": False,
        "field_kernel_solved": False,
        "nonlinear_branch_built": False,
        "gr_derived": False,
        "claims_csv_row_added": False,
        "imports_r01": False,
        "imports_r02": False,
    }
