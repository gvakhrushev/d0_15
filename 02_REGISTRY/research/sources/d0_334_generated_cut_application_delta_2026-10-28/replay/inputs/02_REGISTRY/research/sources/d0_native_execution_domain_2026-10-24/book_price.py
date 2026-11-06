"""Exact full-carrier clock/Hodge realization of Book03's scalar functional.

This is the declared finite execution sector described in BOOK_MAP.md.  It does
not identify this clock operator with an original spatial or scene operator.
Every supplied matrix must be a full primitive unitary, not a prepared/key
compression.  Chronological gates multiply on the left; no closing idle is
inserted.  The cut occupies degree zero of H0 + H1, so feedback is counted once
and the heat trace includes both complete Hodge degrees.
"""

from dataclasses import dataclass
from typing import Sequence

import sympy as sp
from sympy.polys.constructor import construct_domain
from sympy.polys.matrices import DomainMatrix


@dataclass(frozen=True)
class ClockBookOperators:
    stages: int
    fibre_dimension: int
    input_rank: sp.Expr
    word: sp.ImmutableMatrix
    prefixes: tuple
    tick: sp.ImmutableSparseMatrix
    differential: sp.ImmutableSparseMatrix
    delta0: sp.ImmutableSparseMatrix
    delta1: sp.ImmutableSparseMatrix
    paired_delta: sp.ImmutableSparseMatrix
    history_cut: sp.ImmutableSparseMatrix
    leakage: sp.ImmutableSparseMatrix
    feedback: sp.ImmutableSparseMatrix
    paired_cut: sp.ImmutableSparseMatrix
    paired_feedback: sp.ImmutableSparseMatrix
    endpoint_feedback: sp.ImmutableMatrix

    @property
    def heat_dimension(self) -> int:
        return 2 * self.stages * self.fibre_dimension


def _square(matrix, label):
    result = sp.ImmutableMatrix(matrix)
    if result.rows < 1 or result.rows != result.cols:
        raise ValueError(f"{label} must be a nonempty square matrix")
    if any(value.has(sp.Float) for value in result):
        raise ValueError(f"{label} must be exact; floating point entries rejected")
    return result


def _blocks(blocks, size):
    """Assemble (block row, block column, matrix) without dense zero blocks."""
    entries = {}
    for row, column, block in blocks:
        for (i, j), value in block.todok().items():
            if value != 0:
                entries[row * block.rows + i, column * block.cols + j] = value
    return sp.ImmutableSparseMatrix(size, size, entries)


def build_clock(gates: Sequence[sp.MatrixBase], p0: sp.MatrixBase,
                *, max_clock_dimension: int = 2048) -> ClockBookOperators:
    """Build the literal N-stage cycle and its complete paired Hodge.

    Exact unitarity and the orthogonal-projector identities are checked.  The
    dense fibre helpers and full sparse clock are intended for bounded fixtures;
    the dimension cap is computational, not a physical admission condition.
    Symbolic identities must reduce exactly in SymPy's expression domain.
    """
    gates = tuple(_square(g, f"gate {j}") for j, g in enumerate(gates))
    if not gates:
        raise ValueError("at least one actual primitive stage is required")
    p0 = _square(p0, "p0")
    dimension, stages = p0.rows, len(gates)
    if any(g.rows != dimension for g in gates):
        raise ValueError("all primitive gates and p0 need the same full carrier")
    if type(max_clock_dimension) is not int or max_clock_dimension < 1:
        raise ValueError("max_clock_dimension must be a positive integer")
    if stages * dimension > max_clock_dimension:
        raise ValueError("clock exceeds the explicit computational dimension cap")

    # One exact domain keeps long algebraic prefixes small.  Conjugate entries
    # are included so the same arithmetic also handles complex exact matrices.
    entries = [v for m in (*gates, p0) for v in m]
    domain, _ = construct_domain(entries + [sp.conjugate(v) for v in entries],
                                 extension=True)

    def dm(matrix):
        return DomainMatrix.from_Matrix(sp.Matrix(matrix)).convert_to(domain)

    def sm(matrix):
        return sp.ImmutableMatrix(matrix.to_Matrix())

    def adjoint(matrix):
        return dm(sm(matrix).H)

    def is_zero(matrix):
        if matrix.is_zero_matrix:
            return True
        return all(sp.simplify(v) == 0 for v in matrix.to_Matrix())

    identity = DomainMatrix.eye((dimension, dimension), domain)
    p = dm(p0)
    if not is_zero(p - adjoint(p)) or not is_zero(p.matmul(p) - p):
        raise ValueError("p0 is not an exactly verified orthogonal projector")
    primitive = tuple(dm(g) for g in gates)
    checked = set()
    for j, (gate, matrix) in enumerate(zip(gates, primitive)):
        if gate not in checked:
            if not is_zero(adjoint(matrix).matmul(matrix) - identity):
                raise ValueError(f"gate {j} is not exactly verified unitary")
            checked.add(gate)

    prefixes, cuts, prefix = [], [], identity
    for matrix in primitive:
        prefixes.append(sm(prefix))
        cuts.append(prefix.matmul(p).matmul(adjoint(prefix)))
        prefix = matrix.matmul(prefix)
    word = sm(prefix)
    size = stages * dimension
    tick = _blocks([((j + 1) % stages, j, gate)
                    for j, gate in enumerate(gates)], size)
    history_cut = _blocks([(j, j, sm(cut)) for j, cut in enumerate(cuts)], size)
    # Block j of (I-P_hist) T P_hist.  This evaluates that complete-carrier
    # formula; it does not substitute a selected key or success Kraus block.
    leakage_blocks = []
    feedback_blocks = []
    for j, matrix in enumerate(primitive):
        leak = (identity - cuts[(j + 1) % stages]).matmul(matrix).matmul(cuts[j])
        leakage_blocks.append(((j + 1) % stages, j, sm(leak)))
        feedback_blocks.append((j, j, sm(adjoint(leak).matmul(leak))))
    leakage = _blocks(leakage_blocks, size)
    feedback = _blocks(feedback_blocks, size)
    endpoint = p.matmul(adjoint(prefix)).matmul(identity - p).matmul(prefix).matmul(p)
    clock_identity = sp.ImmutableSparseMatrix.eye(size)
    differential = sp.ImmutableSparseMatrix((clock_identity - tick) / sp.sqrt(2))
    # T is exactly unitary: both products d^dagger d and d d^dagger equal this.
    laplacian = sp.ImmutableSparseMatrix(clock_identity - (tick + tick.H) / 2)
    zero = sp.ImmutableSparseMatrix(size, size, {})
    return ClockBookOperators(
        stages, dimension, sp.trace(p0), word, tuple(prefixes), tick,
        differential, laplacian, laplacian,
        _blocks([(0, 0, laplacian), (1, 1, laplacian)], 2 * size),
        history_cut, leakage, feedback,
        _blocks([(0, 0, history_cut), (1, 1, zero)], 2 * size),
        _blocks([(0, 0, feedback), (1, 1, zero)], 2 * size), sm(endpoint))


def feedback_expression(clock: ClockBookOperators, z):
    """Exact -log det(I-z F) on the full endpoint fibre (zero modes included)."""
    z = sp.sympify(z)
    determinant = (sp.eye(clock.fibre_dimension) - z * clock.endpoint_feedback).det()
    return -sp.log(sp.factor(determinant))


def exact_price(clock: ClockBookOperators, beta, z, *, max_heat_dimension=64):
    """Exact spectral expression for a small fixture; never forms a matrix exp.

    The thermodynamic real branch requires beta>0 and 0<z<1.  Symbols may be
    retained under these explicit hypotheses.  No normalized/P-weighted heat
    trace occurs: every eigenvalue of delta0 has its paired multiplicity two.
    """
    beta, z = sp.sympify(beta), sp.sympify(z)
    if beta.is_nonpositive is True or z.is_nonpositive is True or (z - 1).is_nonnegative is True:
        raise ValueError("real Book branch requires beta>0 and 0<z<1")
    if clock.heat_dimension > max_heat_dimension:
        raise ValueError("exact eigensolver fixture limit exceeded; use evaluate_price")
    spectrum = clock.delta0.eigenvals(error_when_incomplete=False)
    if sum(spectrum.values()) != clock.delta0.rows:
        raise ValueError("exact eigensolver did not return all heat modes")
    heat_trace = 2 * sum(mult * sp.exp(-beta * value)
                         for value, mult in spectrum.items())
    heat = sp.log(heat_trace) / beta
    feedback = feedback_expression(clock, z)
    return {"heat_trace": heat_trace, "heat": heat, "feedback": feedback,
            "book": heat + feedback, "heat_mode_count": clock.heat_dimension}


def evaluate_price(clock: ClockBookOperators, beta, z, *, tolerance=1e-10):
    """Evaluate the actual small-matrix price numerically, with all heat modes.

    This convenience evaluation is floating point, not an interval certificate.
    The exact operators and determinant identity remain available separately.
    """
    import numpy as np

    beta, z = float(beta), float(z)
    if not np.isfinite(beta) or beta <= 0 or not np.isfinite(z) or not 0 < z < 1:
        raise ValueError("real Book branch requires finite beta>0 and 0<z<1")
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    laplacian = np.asarray(clock.delta0.evalf(), dtype=complex)
    endpoint = np.asarray(clock.endpoint_feedback.evalf(), dtype=complex)
    heat_eigenvalues = np.linalg.eigvalsh(laplacian)
    feedback_eigenvalues = np.linalg.eigvalsh(endpoint)
    if heat_eigenvalues.min() < -tolerance or heat_eigenvalues.max() > 2 + tolerance:
        raise ValueError("clock Laplacian failed the [0,2] numerical check")
    if feedback_eigenvalues.min() < -tolerance or feedback_eigenvalues.max() > 1 + tolerance:
        raise ValueError("feedback failed the [0,1] numerical check")
    # Zero modes contribute exp(0)=1.  The prefactor two is the WHOLE Hodge pair.
    exponents = -beta * heat_eigenvalues
    top = float(exponents.max())
    log_heat_trace = float(np.log(2) + top + np.log(np.exp(exponents - top).sum()))
    feedback = float(-np.log1p(-z * feedback_eigenvalues).sum())
    heat = log_heat_trace / beta
    return {"heat": heat, "feedback": feedback, "book": heat + feedback,
            "log_heat_trace": log_heat_trace,
            "heat_mode_count": clock.heat_dimension,
            "history_cut_rank": clock.stages * clock.input_rank,
            "input_rank": clock.input_rank}
