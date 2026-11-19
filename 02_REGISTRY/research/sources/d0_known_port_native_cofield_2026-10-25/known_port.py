"""Owned W_K on a genuinely known port, with exact native inverses.

No symmetric G^(-m) or Z middle is used by the positive construction.
The rational score helpers are comparison algebra, not new native gates.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

SOURCES = Path(__file__).resolve().parent.parent
REFLECTED = SOURCES / "d0_exact_report_reflected_cohorts_2026-10-25"
sys.path.insert(0, str(REFLECTED))
import reflected_report as rr

native = rr.native
if Path(rr.__file__).resolve() != (REFLECTED / "reflected_report.py").resolve():
    raise ImportError("the owned reflected-word sibling is required")


def layout(K):
    execution, controls, port = rr.layout(K)
    return replace(execution, blank_wires=(*execution.blank_wires, port)), controls, port


def middle_execution(K, repeat=1, *, stages=None):
    execution, controls, port = layout(K)
    word = rr.controlled_word(execution, controls, port, repeat)
    if stages is not None:
        if type(stages) is not int or stages < len(word) or (stages-len(word)) % 2:
            raise native.DomainError("matching this fixed parity uses actual two-CX identities")
        word += (native.Gate("CX", (controls[0], port)),)* (stages-len(word))
    execution = replace(execution, gates=word)
    native.validate_execution(execution, **rr.bounds(execution))
    return execution, controls, port, (1 << K)*repeat


def expected_middle(execution, controls, port, theta_power):
    rotation = DomainMatrix.from_Matrix(native.G_LOCAL).convert_to(
        native.GOLDEN_FIELD).pow(theta_power).to_Matrix()
    result = sp.zeros(1 << execution.qubits)
    target = 1 << (execution.qubits-1-port)
    for column in range(result.cols):
        ready = all(column & (1 << (execution.qubits-1-q)) for q in controls)
        if not ready:
            result[column, column] = 1
        else:
            old = int(bool(column & target))
            for new in (0, 1):
                result[(column & ~target) | new*target, column] = rotation[new, old]
    return result


def source_echo(power, *, stages=134):
    if type(power) is not int or power < 1:
        raise native.DomainError("a positive integer source power is required")
    middle, controls, port, theta_power = middle_execution(1)
    source = (native.Gate("G", (controls[0],)),)*power
    inverse = native.inverse_word(replace(middle, gates=source), **rr.bounds(middle))
    word = source+middle.gates+inverse
    if type(stages) is not int or stages < len(word) or (stages-len(word)) % 2:
        raise native.DomainError("the predeclared common clock uses a nonnegative even gap")
    word += (native.Gate("CX", (controls[0], port)),)*(stages-len(word))
    execution = replace(middle, gates=word)
    native.validate_execution(execution, **rr.bounds(execution))
    return execution, controls[0], port, theta_power


def prefix_execution(cohorts, *, fork=None, base_power=5, stages=134,
                     old_right_count=1):
    if type(cohorts) is not int or cohorts < 1:
        raise native.DomainError("a positive finite cohort count is required")
    if type(old_right_count) is not int or old_right_count < 0:
        raise native.DomainError("oldRIGHT count is an explicit nonnegative integer")
    if fork is not None and (not isinstance(fork, tuple) or len(fork) != 2
            or type(fork[0]) is not int or not 1 <= fork[0] <= cohorts):
        raise native.DomainError("the fixed fork must occur in this finite prefix")
    old = tuple(range(3, 3+old_right_count))
    start = 3+old_right_count
    word, private = [], []
    for j in range(1, cohorts+1):
        local, _, _, _ = source_echo(fork[1] if fork and j == fork[0] else base_power,
                                     stages=stages)
        control, port = start+2*(j-1), start+2*(j-1)+1
        mapping = {0: 0, 1: control, 2: port, 3: 1, 4: 2}
        word.extend(native.Gate(g.op, tuple(mapping[q] for q in g.wires)) for g in local.gates)
        private.append((control, port))
    execution = native.Execution(start+2*cohorts,
        (0, *(q for pair in private for q in pair)), old, tuple(word),
        native.G_CX_SOURCE_I, 0, (1, 2))
    native.validate_execution(execution, **rr.bounds(execution))
    return execution, tuple(private)


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("an exact integer or Fraction is required")
    return Fraction(value)


def scalar_data(reports, d=Fraction(3, 4), gamma=Fraction(3, 4),
                zeta=Fraction(1, 2**20), *, protected_rank=4):
    d, gamma, zeta = map(rational, (d, gamma, zeta))
    reports = tuple(map(rational, reports))
    if not reports or any(not 0 < q < Fraction(1, 2) for q in reports):
        raise ValueError("the actual positive report collar is required")
    if not Fraction(1, 2) <= d <= 1 or not Fraction(1, 2) <= gamma <= 1 or not 0 < zeta < 1:
        raise ValueError("the actual positive native parameter bounds are required")
    if type(protected_rank) is not int or protected_rank < 1:
        raise ValueError("the SINGLE protected rank is a positive integer")
    amplitudes = tuple(1-d*gamma*q for q in reports)
    grams = tuple(s*s for s in amplitudes)
    slopes = tuple(2*d*gamma/s for s in amplitudes)
    product = Fraction(1)
    for t in grams:
        product *= t
    denominator = 1-zeta+zeta*product
    weight = protected_rank*zeta*product/denominator
    return dict(rank=protected_rank, amplitudes=amplitudes, grams=grams,
                slopes=slopes, product=product, denominator=denominator, weight=weight)


def product_gradient(state, effects, d, gamma, zeta, *, protected_rank=4):
    """Exact whole scalar-return gradient, including entangled bank directions."""
    kernels = [sp.eye(P.rows)-d*gamma*P for P in effects]
    kernel = sp.kronecker_product(*kernels)
    corner = (state.T*kernel*state)[0]
    denominator = 1-zeta+zeta*corner*corner
    weight = protected_rank*zeta*corner*corner/denominator
    gradient = (-4*protected_rank*zeta*corner/denominator)*(kernel*state-corner*state)
    return corner, weight, gradient


def heat_counts(K, *, old_dimension=1):
    """Full real fibre eigenmultiplicities; paired heat doubles THESE counts."""
    if type(K) is not int or K < 1 or type(old_dimension) is not int or old_dimension < 1:
        raise ValueError("positive control depth and actual old Hilbert dimension required")
    return ((1 << (K+4))-16)*old_dimension, 8*old_dimension, 8*old_dimension


def aa_support_fixture():
    """Emit the OWNED AA API word, without a long matrix simulation.

    Bank7 is a spectator in THIS tiny fixture.  A real report may read its
    arbitrary bank; being free in P_ref does not forbid such interaction.
    """
    base = native.Execution(8, (1, 2, 3), (),
        (native.Gate("G", (1,)), native.Gate("G", (2,))),
        native.G_CX_SOURCE_I, source_port=0, source_spin=(5, 6))
    plan = rr.amplified_execution.amplify_execution(base,
        ready_controls=(1,), rebit=3, report_bit=2, rounds=1,
        max_qubits=8, max_expanded_stages=200000,
        max_phase_k=1000, interval_bits=96)
    book = replace(plan.execution, blank_wires=(0, 1, 2, 3, 4, 7))
    native.validate_execution(book, max_qubits=8, max_expanded_stages=200000)
    return plan, book
