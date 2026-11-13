"""All-column native compiler for one common exact predicate phase.

The emitted word is exact exp(J_r * 2**K * k * theta * P_pattern).
The strongest mode chooses one stable NATIVE phase, with no phase-error debt.
Optional pi/3 comparison helpers remain available.  No phase, negative G,
allocation, postselection, H or Toffoli primitive is introduced.  Source-spin
bits and immutable oldRIGHT are not predicate controls.
"""

from dataclasses import replace
from math import isqrt
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


_PREVIOUS_PACKET = (Path(__file__).resolve().parent.parent /
                    "d0_native_execution_domain_2026-10-24")
if str(_PREVIOUS_PACKET) not in sys.path:
    sys.path.insert(0, str(_PREVIOUS_PACKET))
import native_execution as native

if Path(native.__file__).resolve() != (_PREVIOUS_PACKET / "native_execution.py").resolve():
    raise ImportError("native_execution must be the owned sibling packet")

THETA = sp.acos(native.A)
TARGET_PHASE = sp.pi / 3


def _positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise native.DomainError(f"{name} must be a positive integer")
    return value


def _nonnegative_integer(value, name):
    if type(value) is not int or value < 0:
        raise native.DomainError(f"{name} must be a nonnegative integer")
    return value


def _pattern(pattern):
    if type(pattern) not in (list, tuple):
        raise native.DomainError("pattern must be a finite tuple/list")
    result = tuple(pattern)
    if any(type(bit) is not int or bit not in (0, 1) for bit in result):
        raise native.DomainError("pattern entries must be exact bits 0 or 1")
    return result


def phase_counts(pattern, k):
    """Exact counts for this literal compiler, with a distinct source port.

    Every negative G uses the prior packet's full-column inverse expansion:
    four SourceI, one positive G and two SWAPs (six CX).  No cancellations are
    credited.  If every desired bit is zero, every Walsh coefficient is +1.
    """
    pattern, k = _pattern(pattern), _positive_integer(k, "k")
    size = len(pattern)
    terms = 1 << size
    negative_terms = (terms // 2) if any(pattern) else 0
    negative_g = negative_terms * k
    parity_cx = size * terms
    return {"predicate_bits": size, "walsh_terms": terms,
            "angle_multiplier": terms * k,
            "signed_g_steps": terms * k, "negative_g_steps": negative_g,
            "g_count": terms * k, "source_i_count": 4 * negative_g,
            "parity_cx_count": parity_cx, "routing_cx_count": 6 * negative_g,
            "cx_count": parity_cx + 6 * negative_g,
            "expanded_stages": terms * k + parity_cx + 10 * negative_g}


def phase_word(layout: native.Execution, controls, pattern, rebit: int, k: int,
               *, max_qubits: int, max_expanded_stages: int):
    """Return a complete finite native word; allocate no wires implicitly.

    `layout` supplies the existing interface and primitive profile.  The bound
    applies to this macro and to validation of layout; a caller concatenating
    it into a larger circuit must validate that entire final circuit again.
    The realification rebit must already be a fresh declared blank, distinct
    from the source port/spin.  The macro is nevertheless exact on ALL its
    input columns, including arbitrary rebit and dirty source-port/spin input.
    """
    native.validate_execution(layout, max_qubits=max_qubits,
                              max_expanded_stages=max_expanded_stages)
    pattern, k = _pattern(pattern), _positive_integer(k, "k")
    if type(controls) not in (tuple, list):
        raise native.DomainError("controls must be a finite tuple/list")
    controls = tuple(controls)
    if any(type(q) is not int or not 0 <= q < layout.qubits for q in controls):
        raise native.DomainError("predicate controls must be valid wire indices")
    if len(controls) != len(pattern) or len(set(controls)) != len(controls):
        raise native.DomainError("predicate requires distinct controls and one bit per control")
    if type(rebit) is not int or not 0 <= rebit < layout.qubits:
        raise native.DomainError("rebit must be a valid wire index")
    if rebit not in layout.blank_wires or rebit in controls:
        raise native.DomainError("rebit must be a distinct declared fresh blank")
    forbidden = set(layout.old_right) | set(layout.source_spin or ())
    if forbidden.intersection(controls) or rebit in forbidden:
        raise native.DomainError("phase predicate/rebit cannot address oldRIGHT or source spin")
    if rebit == layout.source_port:
        raise native.DomainError("fresh phase rebit must be distinct from the source port")
    counts = phase_counts(pattern, k)
    if counts["expanded_stages"] > max_expanded_stages:
        raise native.DomainError("expanded phase exceeds the stage bound")
    positive = (native.Gate("G", (rebit,)),) * k
    negative = None
    if counts["negative_g_steps"]:
        if layout.profile != native.G_CX_SOURCE_I:
            raise native.DomainError("negative Walsh coefficients need the admitted source-I inverse")
        negative = native.inverse_word(replace(layout, gates=positive),
                                       max_qubits=max_qubits,
                                       max_expanded_stages=max_expanded_stages)
    word = []
    for mask in range(1 << len(controls)):
        subset = tuple(j for j in range(len(controls)) if mask & (1 << j))
        parity = tuple(native.Gate("CX", (controls[j], rebit)) for j in subset)
        sign = -1 if sum(pattern[j] for j in subset) % 2 else 1
        word.extend(parity)
        word.extend(positive if sign == 1 else negative)
        word.extend(reversed(parity))
    result = tuple(word)
    native.validate_execution(replace(layout, gates=result), max_qubits=max_qubits,
                              max_expanded_stages=max_expanded_stages)
    if len(result) != counts["expanded_stages"]:
        raise ArithmeticError("phase inventory does not match the emitted literal word")
    return result


def phase_error_squared(pattern, k):
    """Exact algebraic squared operator error from the fixed pi/3 phase.

    If G**m=[[c,-s],[s,c]], the error is 2-c-sqrt(3)*s, with m=2**K*k.
    This is an ALL-column operator norm, not success-weighted error.
    """
    multiplier = phase_counts(pattern, k)["angle_multiplier"]
    power = DomainMatrix.from_Matrix(native.G_LOCAL).convert_to(native.GOLDEN_FIELD)
    matrix = power.pow(multiplier).to_Matrix()
    return 2 - matrix[0, 0] - sp.sqrt(3) * matrix[1, 0]


def _rotation_intervals(multiplier, bits):
    """Return scale and integer-endpoint enclosures of cos/sin(m*theta)."""
    _positive_integer(multiplier, "angle multiplier")
    if type(bits) is not int or bits < 16:
        raise native.DomainError("interval precision bits must be an integer >=16")
    scale = 1 << bits

    def ceil_div(a, b):
        return -((-a) // b)

    def add(a, b):
        return a[0] + b[0], a[1] + b[1]

    def neg(a):
        return -a[1], -a[0]

    def mul(a, b):
        values = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
        return min(values) // scale, ceil_div(max(values), scale)

    def unit_component(interval):
        # Each accumulated complex number is a power of the exact unit G.
        lower, upper = max(-scale, interval[0]), min(scale, interval[1])
        if lower > upper:
            raise ArithmeticError("invalid interval enclosure of a unit rotation")
        return lower, upper

    def cmul(a, b):
        return (unit_component(add(mul(a[0], b[0]), neg(mul(a[1], b[1])))),
                unit_component(add(mul(a[1], b[0]), mul(a[0], b[1]))))

    sqrt5 = isqrt(5 * scale * scale)
    p = ((sqrt5 - scale) // 2, ceil_div(sqrt5 + 1 - scale, 2))
    a = (isqrt(p[0] * scale), isqrt(p[1] * scale) + 1)
    result, base, exponent = ((scale, scale), (0, 0)), (a, p), multiplier
    while exponent:
        if exponent & 1:
            result = cmul(result, base)
        exponent >>= 1
        if exponent:
            base = cmul(base, base)
    return scale, result[0], result[1]


def native_rotation_intervals(multiplier: int, *, bits: int = 96):
    """Certified rational cos/sin intervals for the exact positive G power."""
    scale, cosine, sine = _rotation_intervals(multiplier, bits)
    return (tuple(sp.Rational(v, scale) for v in cosine),
            tuple(sp.Rational(v, scale) for v in sine))


def matched_phase_index(Kmax: int, predicate_bits: int, k: int):
    """Exact index giving every predicate the same 2**Kmax*k*theta phase."""
    _nonnegative_integer(Kmax, "Kmax")
    _nonnegative_integer(predicate_bits, "predicate_bits")
    _positive_integer(k, "k")
    if predicate_bits > Kmax:
        raise native.DomainError("predicate_bits cannot exceed Kmax")
    return (1 << (Kmax - predicate_bits)) * k


def find_stable_native_phase(Kmax: int, max_k: int, bits: int = 96):
    """Bounded search for an EXACT native phase in a generic stable interval.

    Returned rational intervals certify sin(beta)>0 and
    1/2<cos(beta)<17/32, beta=2**Kmax*k*theta.  No target-phase approximation
    is made.  Search failure means only that this finite budget/precision did
    not certify a candidate; it is not a nonexistence result.  The interval
    was chosen for generic amplification stability, independently of fields.
    """
    _nonnegative_integer(Kmax, "Kmax")
    _positive_integer(max_k, "max_k")
    for k in range(1, max_k + 1):
        multiplier = (1 << Kmax) * k
        cosine, sine = native_rotation_intervals(multiplier, bits=bits)
        if cosine[0] > sp.Rational(1, 2) and cosine[1] < sp.Rational(17, 32) and sine[0] > 0:
            return {"Kmax": Kmax, "k": k, "angle_multiplier": multiplier,
                    "cosine": cosine, "sine": sine, "bits": bits,
                    "b_interval": (2 * cosine[0] - 1, 2 * cosine[1] - 1),
                    "a_interval": (2 - 2 * cosine[1], 2 - 2 * cosine[0])}
    raise native.DomainError("no stable native phase certified within max_k and bits")


def phase_error_bound(pattern, k, *, bits: int = 96):
    """Optional certified rational error bound from the fixed pi/3 phase.

    Integer roots and outward dyadic binary powering use no floating point
    trigonometry or sign oracle.  Exact-native-phase mode needs no such debt.
    """
    multiplier = phase_counts(pattern, k)["angle_multiplier"]
    scale, cosine, sine = _rotation_intervals(multiplier, bits)
    root3 = isqrt(3 * scale * scale)
    products = (root3 * sine[0], root3 * sine[1],
                (root3 + 1) * sine[0], (root3 + 1) * sine[1])
    product_lower = min(products) // scale
    upper_squared = 2 * scale - cosine[0] - product_lower
    if upper_squared < 0:
        raise ArithmeticError("invalid interval enclosure of nonnegative squared error")
    upper_squared = min(4 * scale, upper_squared)  # both matrices are unitary
    numerator = isqrt(upper_squared * scale)
    if numerator * numerator < upper_squared * scale:
        numerator += 1
    return sp.Rational(numerator, scale)
