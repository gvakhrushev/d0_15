"""Exact replay of the retained H read of the live Bell-parity wire."""
from fractions import Fraction
from itertools import product
import json


ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)
A = (0, 1, 0, 0)
P = (0, 0, 1, 0)


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def add(left, right):
    return tuple(x + y for x, y in zip(left, right))


def scale(value, factor):
    return tuple(factor * x for x in value)


def multiply(left, right):
    coefficients = [0] * 7
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            coefficients[i + j] += x * y
    for i in range(6, 3, -1):
        # a^4 = 1 - a^2.
        coefficients[i - 4] += coefficients[i]
        coefficients[i - 2] -= coefficients[i]
    return tuple(coefficients[:4])


def square(value):
    return multiply(value, value)


def compose(first, second):
    c, s = first
    d, t = second
    return add(multiply(c, d), scale(multiply(s, t), -1)), add(multiply(s, d), multiply(c, t))


def rotation(exponent):
    result = ONE, ZERO
    power = A, P
    while exponent:
        if exponent % 2:
            result = compose(result, power)
        power = compose(power, power)
        exponent //= 2
    return result


def root_interval(bits=4096):
    denominator = 1 << bits
    lower, upper = 0, denominator
    while upper - lower > 1:
        middle = (lower + upper) // 2
        if middle**4 + (middle * denominator)**2 < denominator**4:
            lower = middle
        else:
            upper = middle
    return Fraction(lower, denominator), Fraction(upper, denominator)


ROOT = root_interval()


def sign(value):
    if value == ZERO:
        return 0
    lo, hi = Fraction(0), Fraction(0)
    for coefficient in reversed(value):
        candidates = [x * y for x in (lo, hi) for y in ROOT]
        lo, hi = min(candidates) + coefficient, max(candidates) + coefficient
    require(lo > 0 or hi < 0, "inconclusive exact sign enclosure")
    return 1 if lo > 0 else -1


def absolute(value):
    return scale(value, sign(value))


def bell_state(phase):
    state = [ZERO] * 8
    if phase == 0:
        state[0], state[6] = ONE, ONE
    else:
        state[2], state[4] = ONE, scale(ONE, -1)
    return state


def cnot(state, control, target):
    result = [ZERO] * 8
    for coordinate, value in enumerate(state):
        result[coordinate ^ (target if coordinate & control else 0)] = value
    return result


def rotate_target(state, cosine, sine):
    result = [ZERO] * 8
    for first in (0, 4):
        for tag in (0, 1):
            zero, one = first + tag, first + tag + 2
            x, y = state[zero], state[one]
            result[zero] = add(multiply(cosine, x), scale(multiply(sine, y), -1))
            result[one] = add(multiply(sine, x), multiply(cosine, y))
    return result


def parity_tag(state):
    return cnot(cnot(state, 4, 1), 2, 1)


def hadamard_numerator(state):
    # The shared 1/sqrt(2) is accounted for in the probability divisor.
    result = [ZERO] * 8
    for even in range(0, 8, 2):
        x, y = state[even], state[even + 1]
        result[even], result[even + 1] = add(x, y), add(x, scale(y, -1))
    return result


def probability_numerators(state):
    result = {(b, r): ZERO for b, r in product(range(2), repeat=2)}
    for coordinate, value in enumerate(state):
        key = (int(bool(coordinate & 4) != bool(coordinate & 2)), coordinate & 1)
        result[key] = add(result[key], square(value))
    return result


def arm_pairs(cosine, sine, central_sign):
    sine = scale(sine, central_sign)
    return (
        (multiply(A, cosine), scale(multiply(P, sine), -1)),
        (multiply(P, cosine), multiply(A, sine)),
    )


def tagged_trial(cosine, sine, phase, central_sign):
    initial = bell_state(phase)
    moved = rotate_target(initial, cosine, sine)
    tagged = parity_tag(moved)
    source = [scale(value, central_sign if i & 1 else 1) for i, value in enumerate(tagged)]
    late = rotate_target(hadamard_numerator(source), A, P)
    tagged_probs = probability_numerators(late)  # divisor 4: Bell and H.
    old = rotate_target(parity_tag(source), A, P)
    old_probs = probability_numerators(old)  # divisor 2: Bell only.
    require(late[::2] == old[::2], "r=0 reproduces the old conditional state")

    c, s = (cosine, sine) if phase == 0 else (scale(sine, -1), cosine)
    arms = arm_pairs(c, s, central_sign)
    positive_mass = ZERO
    for b, (u, v) in enumerate(arms):
        candidates = []
        for r in (0, 1):
            amplitude = add(u, scale(v, (-1)**r))
            require(tagged_probs[b, r] == scale(square(amplitude), 2), "two-arm formula")
            candidates.append(tagged_probs[b, r])
        require(tagged_probs[b, 0] == old_probs[b, 0], "r=0 reproduces the old conditional read")
        require(old_probs[b, 1] == ZERO, "old parity wire is returned")
        maximum = candidates[int(sign(u) * sign(v) < 0)]
        positive = add(absolute(u), absolute(v))
        require(maximum == scale(square(positive), 2), "positive cut mass from maximum")
        positive_mass = add(positive_mass, positive)
    require(positive_mass == multiply(add(A, P), add(absolute(cosine), absolute(sine))),
            "positive sum of both terminal cut arms")
    for r in (0, 1):
        require(add(tagged_probs[0, r], tagged_probs[1, r]) == scale(ONE, 2), "fair retained H label")
    return tagged_probs


def run():
    # The exact A89 finite pulse is 2320 theta modulo 2 pi.
    cosine, sine = rotation(2320)
    require(sign(sine) == 1 and sign(add(cosine, scale(sine, -1))) == 1, "positive small pulse")
    require(sign(add(A, scale(P, -1))) == 1, "Golden splitter imbalance")
    for cos_x, sin_x in ((cosine, sine), (cosine, scale(sine, -1))):
        c, s = compose((A, P), (cos_x, sin_x))
        require(sign(c) == 1 and sign(s) == 1, "A89 untagged arc")

    checked = {}
    for direction, phase, central in product((0, 1, -1), (0, 1), (1, -1)):
        c = ONE if direction == 0 else cosine
        checked[direction, phase, central] = tagged_trial(c, scale(sine, direction), phase, central)
    for phase, central, b, r in product((0, 1), (1, -1), (0, 1), (0, 1)):
        require(checked[1, phase, central][b, r] == checked[-1, phase, central][b, 1-r],
                "finite sign exchange permutes the retained H label")
        require(checked[1, 1, central][b, r] == checked[1, 0, central][1-b, r],
                "recorded phase swaps the terminal bit")

    # A89 no-background material clicks. Numerators have divisor 8.
    amplitude = multiply(P, rotation(448)[1])
    common = multiply(multiply(square(P), P), square(amplitude))
    q = [scale(common, 16), scale(common, 21)]
    require(sign(q[0]) == sign(add(q[1], scale(q[0], -1))) == sign(add(scale(ONE, 8), scale(q[1], -1))) == 1,
            "0 < q0 < q1 < 1 gives the strict untagged contrast")
    for k, j, route, m, phase, b, r in product(range(2), repeat=7):
        weight = q[j] if m else add(scale(ONE, 8), scale(q[j], -1))
        direction = (-1)**(route ^ m) if j ^ route == k else 0
        left = multiply(weight, checked[direction, phase, 1][b, r])
        right = multiply(weight, checked[-direction, phase, 1][b, 1-r])
        require(left == right, "complete ready archive is permuted leaf by leaf")

    print(json.dumps({
        "exact_ring": "Z[a], a^4+a^2=1",
        "actual_A89_pulse_steps": 2320,
        "literal_two_CX_H_and_final_G": True,
        "both_A90_central_signs": True,
        "both_retained_H_records_fair": True,
        "conditional_r0_reproduces_untagged": True,
        "two_arm_positive_mass_even": True,
        "all_tagged_A89_amplitude_secants_zero": True,
        "untagged_A89_first_sign": "negative",
        "untagged_A89_second_sign": "positive",
        "Book03_micro_weights_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    run()
