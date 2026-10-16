#!/usr/bin/env python3
"""Exact retained-record engine on the certified collinear native sector.

All sixteen exterior coordinates are stored. The transition receives only the
current matter state, never an iteration index, an archive log or fresh blanks.
The geometric binding is Q=I, q=diag(1,-1,-1,-1); the apparatus axis is read
from the actual first grade. This is a restricted executor of the published
conditional binding, not a physical refinement/admission law.
"""
import argparse
from dataclasses import dataclass
import json


def _sgn(x):
    return (x > 0) - (x < 0)


def quadratic_sign(u, v):
    """Exact sign of u+v*p, p=(sqrt(5)-1)/2; no floating-point decisions."""
    x, y = 2 * u - v, v
    if not y:
        return _sgn(x)
    if not x or _sgn(x) == _sgn(y):
        return _sgn(y)
    return _sgn(x) * _sgn(x * x - 5 * y * y)


@dataclass(frozen=True)
class Golden:
    """Canonical integers in Z[a], a>0, a^4+a^2=1, basis 1,a,a^2,a^3."""
    coefficients: tuple

    def __post_init__(self):
        if not isinstance(self.coefficients, tuple) or len(self.coefficients) != 4 or any(type(v) is not int for v in self.coefficients):
            raise TypeError('FOUR_EXACT_INTEGER_COEFFICIENTS_REQUIRED')

    @staticmethod
    def integer(n):
        return Golden((int(n), 0, 0, 0))

    def __add__(self, other):
        if isinstance(other, int):
            other = Golden.integer(other)
        return Golden(tuple(x + y for x, y in zip(self.coefficients, other.coefficients)))

    __radd__ = __add__

    def __neg__(self):
        return Golden(tuple(-x for x in self.coefficients))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, int):
            return Golden(tuple(other * x for x in self.coefficients))
        out = [0] * 7
        for i, x in enumerate(self.coefficients):
            for j, y in enumerate(other.coefficients):
                out[i + j] += x * y
        for degree in range(6, 3, -1):
            out[degree - 4] += out[degree]
            out[degree - 2] -= out[degree]
        return Golden(tuple(out[:4]))

    __rmul__ = __mul__

    def sign(self):
        # X+a*Y, X,Y in Z[p]. If signs differ, compare X^2 and p*Y^2.
        u, r, v, t = self.coefficients
        sx, sy = quadratic_sign(u, v), quadratic_sign(r, t)
        if not sx:
            return sy
        if not sy or sx == sy:
            return sx
        X, Y = Golden((u, 0, v, 0)), Golden((r, 0, t, 0))
        difference = (X * X - P * Y * Y).coefficients
        sd = quadratic_sign(difference[0], difference[2])
        assert sd, 'NONZERO_FIELD_ELEMENT_CANNOT_HAVE_ZERO_SQUARED_COMPARISON'
        return sx * sd

    def __bool__(self):
        return any(self.coefficients)


ZERO, ONE = Golden.integer(0), Golden.integer(1)
A, P = Golden((0, 1, 0, 0)), Golden((0, 0, 1, 0))


@dataclass(frozen=True)
class State:
    matter: tuple

    def __post_init__(self):
        if not isinstance(self.matter, tuple) or len(self.matter) != 16 or any(not isinstance(x, Golden) for x in self.matter):
            raise TypeError('ALL_SIXTEEN_EXTERIOR_COORDINATES_REQUIRED')


def seed():
    m = [ZERO] * 16
    m[1] = m[15] = ONE
    return State(tuple(m))


def literal_axis_gate(state, sign):
    """Full CAR U_(sign*e0), including all eight low/high spatial pairs."""
    if sign not in (-1, 1):
        raise ValueError('UNIT_OBSERVER_SIGN_REQUIRED')
    out = [ZERO] * 16
    for mask in range(0, 16, 2):
        x, y = state.matter[mask], state.matter[mask | 1]
        out[mask] = A * x - sign * P * y
        if bin(mask).count('1') <= 1:
            out[mask | 1] = sign * P * x + A * y
        else:
            out[mask | 1] = -sign * P * x - A * y
    return State(tuple(out))


def step(state):
    # The six zero coordinates define this executor's invariant sector.
    # They remain stored and are acted on by the literal sixteen-row gate.
    if any(state.matter[i] for i in (2, 3, 4, 5, 8, 9)):
        raise ValueError('OUTSIDE_CERTIFIED_COLLINEAR_EXECUTOR')
    sign = state.matter[1].sign()
    if not sign:
        raise ValueError('FIRST_GRADE_PAIRING_SINGULARITY')
    out = literal_axis_gate(state, sign)
    if not out.matter[1]:
        raise ValueError('OUTPUT_FIRST_GRADE_PAIRING_SINGULARITY')
    return out


def inverse_axis_gate(state, sign):
    """Algebraic transpose of the same full operator; no reset."""
    if sign not in (-1, 1):
        raise ValueError('UNIT_OBSERVER_SIGN_REQUIRED')
    out = [ZERO] * 16
    for mask in range(0, 16, 2):
        x, y = state.matter[mask], state.matter[mask | 1]
        if bin(mask).count('1') <= 1:
            out[mask] = A * x + sign * P * y
            out[mask | 1] = -sign * P * x + A * y
        else:
            out[mask] = A * x - sign * P * y
            out[mask | 1] = -sign * P * x - A * y
    return State(tuple(out))


def predecessor_on_seed_orbit(state):
    """Recover the previous full state on the proved seed orbit only.

    This is a mathematical decoder, not an assertion that reversing the
    apparatus is an independently admitted physical operation. It reads no
    external index and stores no history. Orbit membership is its premise.
    """
    initial = seed()
    if state == initial:
        raise ValueError('INITIAL_SEED_HAS_NO_RECORDED_PREDECESSOR')
    one = step(initial)
    if state == one:
        return initial
    if state == step(one):
        return one
    return inverse_axis_gate(state, -state.matter[1].sign())


def norm_squared(state):
    return sum((v * v for v in state.matter), ZERO)


def encode(state):
    """Self-delimiting signed integer code; persistent data, not free reals.

    Map z to 2*z+1 for z>=0 and -2*z for z<0, then Elias gamma code. There
    are exactly 64 integers in canonical mask/basis order, so no length field
    or external history is necessary. This is an audit codec, not native bits.
    """
    parts = []
    for value in state.matter:
        for z in value.coefficients:
            positive = 2 * z + 1 if z >= 0 else -2 * z
            digits = bin(positive)[2:]
            parts.append('0' * (len(digits) - 1) + digits)
    return ''.join(parts)


def decode(bits):
    integers, pos = [], 0
    for _ in range(64):
        zeros = 0
        while pos + zeros < len(bits) and bits[pos + zeros] == '0':
            zeros += 1
        start, stop = pos + zeros, pos + 2 * zeros + 1
        if stop > len(bits) or bits[start] != '1' or any(c not in '01' for c in bits[start:stop]):
            raise ValueError('TRUNCATED_OR_INVALID_INTERNAL_STATE')
        positive = int(bits[start:stop], 2)
        integers.append((positive - 1) // 2 if positive % 2 else -(positive // 2))
        pos = stop
    if pos != len(bits):
        raise ValueError('TRAILING_UNDECLARED_STATE_DATA')
    return State(tuple(Golden(tuple(integers[i:i + 4])) for i in range(0, 64, 4)))


def bounded_step(state, capacity_bits):
    """Diagnostic finite store: halt at overflow; never silently add cells."""
    if len(encode(state)) > capacity_bits:
        raise OverflowError('INPUT_EXCEEDS_DECLARED_INTERNAL_STORE')
    out = step(state)
    if len(encode(out)) > capacity_bits:
        raise OverflowError('NEXT_STATE_REQUIRES_MORE_INTERNAL_STORE')
    return out


def archive_modes(stage):
    if stage < 0:
        raise ValueError('NEGATIVE_ARCHIVE_STAGE')
    return (stage + 2) ** 4


def archive_projection(stage, child):
    if not 0 <= child < archive_modes(stage + 1):
        raise ValueError('CHILD_OUTSIDE_ACTUAL_ARCHIVE_STAGE')
    return child % archive_modes(stage)


def inherit(stage, field):
    """Literal pullback of a field by the owned archiveProjection.

    This is an explicit refinement adapter, not a step trigger. No physical
    spatial metric, link update or law of cell division is inferred from it.
    """
    if len(field) != archive_modes(stage):
        raise ValueError('FIELD_AND_ARCHIVE_STAGE_DISAGREE')
    return tuple(field[archive_projection(stage, child)]
                 for child in range(archive_modes(stage + 1)))


def minimum_audit_stage(bits):
    # Capacity comparison only, under an explicit ONE AUDIT BIT PER POINT
    # convention. No such capacity assignment is an owned D0 physical law.
    stage = 0
    while archive_modes(stage) < bits:
        stage += 1
    return stage


def diagnostic(state, ordinal):
    bits = len(encode(state))
    return {
        'diagnostic_iteration_not_transition_input': ordinal,
        'observer_sign': state.matter[1].sign(),
        'stored_exterior_coordinates': 16,
        'max_coefficient_bits': max(abs(c).bit_length() for v in state.matter for c in v.coefficients),
        'canonical_state_bits': bits,
        'minimum_archive_stage_if_one_audit_bit_per_point': minimum_audit_stage(bits),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--steps', type=int, default=256)
    parser.add_argument('--capacity-bits', type=int)
    args = parser.parse_args()
    if args.steps < 0 or (args.capacity_bits is not None and args.capacity_bits < 0):
        parser.error('nonnegative steps and capacity required')
    state, rows, status = seed(), [], 'COMPLETED_REQUESTED_FINITE_RUN'
    interesting = {0, 1, 2, 3, 4, 16, 64, 256, 1024, args.steps}
    for k in range(args.steps + 1):
        if k in interesting:
            rows.append(diagnostic(state, k))
        if k == args.steps:
            break
        try:
            state = step(state) if args.capacity_bits is None else bounded_step(state, args.capacity_bits)
        except OverflowError as exc:
            status = str(exc)
            rows.append({'halt_before_diagnostic_iteration': k + 1})
            break
    print(json.dumps({
        'status': status,
        'transition': 'ACTUAL_GOLDEN_RECORD_READS_CURRENT_FIRST_GRADE',
        'scope': 'CONDITIONAL_COLLINEAR_LOCAL_ENGINE_NOT_PHYSICAL_UNIVERSE',
        'external_tick_or_history_used_by_transition': False,
        'new_blank_or_reset': False,
        'native_refinement_trigger_derived': False,
        'persistent_exact_state_storage_accounted': True,
        'rows': rows,
    }, indent=2))


if __name__ == '__main__':
    main()
