"""Literal paid clock padding and a native all-column holonomy witness.

This is not an implementation of a general Solovay-Kitaev compiler or a
selection of physical beta/z. Every helper returns actual native letters.
"""
from dataclasses import replace
from pathlib import Path
import sys
import sympy as sp

DOMAIN = Path(__file__).resolve().parent.parent / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(DOMAIN))
import native_execution as native


def two_cx_identity(a, b):
    if type(a) is not int or type(b) is not int or a == b:
        raise native.DomainError("identity needs two distinct addressed wires")
    return (native.Gate("CX", (a, b)),) * 2


def five_cx_identity(a, b, c):
    if any(type(q) is not int for q in (a, b, c)) or len({a, b, c}) != 3:
        raise native.DomainError("five-letter identity needs three distinct wires")
    ab, bc, ac = (native.Gate("CX", pair) for pair in ((a, b), (b, c), (a, c)))
    return ab, bc, ab, bc, ac  # chronological; ab;bc;ab;bc equals ac


def pad_word_same_clock(execution, stages, wires, *, max_qubits, max_expanded_stages):
    bounds = dict(max_qubits=max_qubits, max_expanded_stages=max_expanded_stages)
    native.validate_execution(execution, **bounds)
    if type(stages) is not int or stages < 1 or stages < len(execution.gates) or stages > max_expanded_stages:
        raise native.DomainError("invalid final paid stage bound")
    if (type(wires) not in (tuple, list) or len(wires) != 3
            or any(type(q) is not int for q in wires) or len(set(wires)) != 3):
        raise native.DomainError("padding requires three distinct active wires")
    forbidden = set(execution.old_right) | set(execution.source_spin or ())
    if any(type(q) is not int or not 0 <= q < execution.qubits or q in forbidden for q in wires):
        raise native.DomainError("padding cannot touch oldRIGHT or source spin")
    gap = stages - len(execution.gates)
    if gap in (1, 3):
        raise native.DomainError("gap not representable by paid lengths two and five")
    odd = gap % 2
    word = tuple(execution.gates) + (five_cx_identity(*wires) if odd else ())
    word += two_cx_identity(*wires[:2]) * ((gap - 5 * odd) // 2)
    padded = replace(execution, gates=word)
    native.validate_execution(padded, **bounds)
    if len(word) != stages:
        raise ArithmeticError("padding stage mismatch")
    return padded


def pad_catalogue_same_clock(executions, wires, *, max_qubits, max_expanded_stages):
    executions = tuple(executions)
    if not executions:
        raise native.DomainError("empty clock catalogue")
    interface = replace(executions[0], gates=())
    if any(replace(e, gates=()) != interface for e in executions):
        raise native.DomainError("common-clock catalogue must retain layout, cut and apparatus interface")
    # Compile accuracy FIRST. Every resulting gap is at least four.
    stages = max(len(e.gates) for e in executions) + 4
    return tuple(pad_word_same_clock(e, stages, wires, max_qubits=max_qubits,
                                   max_expanded_stages=max_expanded_stages) for e in executions)


def controlled_holonomy_word(Q, data, rebit):
    if type(Q) is not int or Q < 1 or data == rebit:
        raise native.DomainError("positive return index and distinct wires required")
    return ((native.Gate("CX", (data, rebit)),)
            + (native.Gate("G", (rebit,)),) * (2 * Q)
            + (native.Gate("CX", (data, rebit)),))


def skew_holonomy_generator(K):
    """Rebit-first coordinate ordering; actual wire placement remains explicit."""
    K = sp.Matrix(K)
    m = K.rows
    if K.cols != m or m < 1 or m & (m - 1):
        raise native.DomainError("full scene dimension must be a power of two; no free level padding")
    if K != K.T or any(x.is_real is not True for x in K):
        raise native.DomainError("K must be an explicitly real symmetric matrix")
    return sp.kronecker_product(sp.Matrix([[0, -1], [1, 0]]), K)
