"""Literal reflected weak query and finite-cohort comparison helpers.

The native word uses only the owned G/CX/SourceI interface.  The cohort
matrices are explicit comparison models, not extra native primitives or a
continuous selector of native words.  All flags and the source spin remain.
"""
from dataclasses import replace
from math import isqrt
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

SOURCES = Path(__file__).resolve().parent.parent
DOMAIN = SOURCES / "d0_native_execution_domain_2026-10-24"
PHASE = SOURCES / "d0_native_readiness_amplification_2026-10-24"
sys.path.insert(0, str(DOMAIN))
sys.path.insert(0, str(PHASE))
import native_execution as native
import native_phase
import amplified_execution

if Path(native.__file__).resolve() != (DOMAIN / "native_execution.py").resolve():
    raise ImportError("the owned native_execution sibling is required")


def layout(K):
    if type(K) is not int or K < 1:
        raise native.DomainError("K must be a positive integer")
    controls, meter, spin = tuple(range(1, K+1)), K+1, (K+2, K+3)
    execution = native.Execution(K+4, (0, *controls), (), (), native.G_CX_SOURCE_I,
                                 source_port=0, source_spin=spin)
    return execution, controls, meter


def bounds(execution):
    return dict(max_qubits=execution.qubits, max_expanded_stages=1000000)


def inverse_g(execution, wire, count=1):
    if type(count) is not int or count < 1:
        raise native.DomainError("the positive inverse multiplicity is explicit")
    return native.inverse_word(replace(execution,
        gates=(native.Gate("G", (wire,)),)*count), **bounds(execution))


def z_word(execution, wire):
    port = execution.source_port
    source = (native.Gate("SourceI", (port, *execution.source_spin)),)*2
    swap = () if wire == port else (
        native.Gate("CX", (wire, port)), native.Gate("CX", (port, wire)),
        native.Gate("CX", (wire, port)))
    return swap + source + swap


def controlled_word(execution, controls, meter, repeat=1):
    """Owned recursive K-controlled G**(2**K*repeat), on all columns.

    Signed recipes are internal syntax, expanded BEFORE native validation.
    No negative-G primitive is added to the actual profile.
    """
    if type(repeat) is not int or repeat < 1:
        raise native.DomainError("repeat must be a positive integer")
    if (len(set(controls)) != len(controls) or meter in controls
            or set(controls) & set(execution.source_spin or ())
            or meter in (execution.source_spin or ())):
        raise native.DomainError("the logical controls/target must be distinct from source spin")
    recipe = (("G", (meter,), 1),)*repeat
    for control in controls:
        inverse = tuple((op, wires, -sign if op == "G" else sign)
                        for op, wires, sign in reversed(recipe))
        cx = (("CX", (control, meter), 1),)
        recipe = recipe + cx + inverse + cx
    negative = inverse_g(execution, meter)
    return tuple(gate for op, wires, sign in recipe for gate in (
        negative if op == "G" and sign == -1 else (native.Gate(op, wires),)))


def middle_execution(K, repeat=1, *, reflected=True):
    execution, controls, meter = layout(K)
    m = (1 << (K-1))*repeat
    word = ((z_word(execution, meter) if reflected else ())
            + inverse_g(execution, meter, m)
            + controlled_word(execution, controls, meter, repeat))
    execution = replace(execution, gates=word)
    native.validate_execution(execution, **bounds(execution))
    return execution, controls, meter, m


def echo_execution(K, repeat=1, *, reflected=True):
    execution, controls, meter, m = middle_execution(K, repeat, reflected=reflected)
    forward = tuple(native.Gate("G", (q,)) for q in controls)
    backward = native.inverse_word(replace(execution, gates=forward), **bounds(execution))
    return replace(execution, gates=forward+execution.gates+backward), controls, meter, m


def expected_middle(execution, controls, meter, m, *, reflected):
    """Independent block definition, including every unready input column."""
    power = DomainMatrix.from_Matrix(native.G_LOCAL).convert_to(native.GOLDEN_FIELD).pow(m).to_Matrix()
    result = sp.zeros(1 << execution.qubits)
    target_bit = 1 << (execution.qubits-1-meter)
    for column in range(result.cols):
        ready = all(column & (1 << (execution.qubits-1-q)) for q in controls)
        rotation = power if ready else power.T
        block = rotation*sp.diag(1, -1) if reflected else rotation
        old = int(bool(column & target_bit))
        for new in (0, 1):
            result[(column & ~target_bit) | (new*target_bit), column] = block[new, old]
    return result


def alpha_interval(K, repeat, *, bits=96):
    m = (1 << (K-1))*repeat
    cosine, sine = native_phase.native_rotation_intervals(m, bits=bits)
    lower = 0 if sine[0] <= 0 <= sine[1] else min(sine[0]**2, sine[1]**2)
    return {"K": K, "repeat": repeat, "m": m, "bits": bits,
            "cosine": cosine, "sine": sine,
            "alpha": (4*lower, 4*max(sine[0]**2, sine[1]**2))}


def find_alpha(K, max_repeat=100, *, bits=96):
    for repeat in range(1, max_repeat+1):
        result = alpha_interval(K, repeat, bits=bits)
        if 1 < result["alpha"][0] and result["alpha"][1] < 2:
            return result
    raise native.DomainError("no alpha in (1,2) certified within the finite search budget")


def gram(alpha, gamma, q):
    x = gamma*q
    return 1-alpha*x*(1-x)


def kappa(alpha, gamma, q, gain=1):
    return gain*alpha*gamma*(1-2*gamma*q)/gram(alpha, gamma, q)


def x_pair_average(n):
    """READ-ONLY algebra diagnostic after a fixed basis change, not a gate."""
    if type(n) is not int or n < 2:
        raise ValueError("at least two distinct slots are required")
    result = sp.SparseMatrix.zeros(1 << n)
    for column in range(1 << n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    result[column ^ (1 << i) ^ (1 << j), column] += sp.Rational(1, n*(n-1))
    return result


def local_kernel(effect, cosine, sine, gamma, row, column):
    if row == column:
        return ((-1)**row)*cosine*sp.eye(effect.rows)
    return sine*(2*gamma*effect-sp.eye(effect.rows))


def returned_matrix(state, effects, cosines, sines, gammas):
    """Full private-DATA returned matrix for an arbitrary joint bank state."""
    M, dimension = len(effects), 1 << len(effects)
    result = sp.zeros(dimension)
    for row in range(dimension):
        for column in range(dimension):
            factors = [local_kernel(effects[j], cosines[j], sines[j], gammas[j],
                (row >> (M-1-j)) & 1, (column >> (M-1-j)) & 1) for j in range(M)]
            kernel = sp.kronecker_product(*factors)
            result[row, column] = (state.T*kernel*state)[0]
    return result


def full_logdet_gradient(state, effects, cosines, sines, gammas, zeta):
    """All joint-bank components from literal DATA matrix differentiation.

    One shared source spin4 is counted once.  The comparison matrices are
    real; this is the complete real pure-state tangent gradient.
    """
    M, dimension = len(effects), 1 << len(effects)
    corner = returned_matrix(state, effects, cosines, sines, gammas)
    Q = (1-zeta)*sp.eye(dimension)+zeta*corner.T*corner
    weight = corner*Q.inv()
    ambient = sp.zeros(state.rows, 1)
    for row in range(dimension):
        for column in range(dimension):
            factors = [local_kernel(effects[j], cosines[j], sines[j], gammas[j],
                (row >> (M-1-j)) & 1, (column >> (M-1-j)) & 1) for j in range(M)]
            ambient += (-16*zeta*weight[row, column])*(sp.kronecker_product(*factors)*state)
    return corner, sp.simplify(ambient-state*(state.T*ambient)[0])


def cohort_size(j):
    """max(2,ceil(j**(3/4))) computed with integer comparisons."""
    if type(j) is not int or j < 1:
        raise ValueError("cohort index must be positive")
    target, lower, upper = j**3, 0, isqrt(j**3)+2
    while lower+1 < upper:
        middle = (lower+upper)//2
        if middle**4 >= target:
            upper = middle
        else:
            lower = middle
    return max(2, upper)
