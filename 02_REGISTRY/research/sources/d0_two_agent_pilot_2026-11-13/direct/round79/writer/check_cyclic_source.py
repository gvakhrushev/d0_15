"""Exact equal cold selector weights and the first jet on independent recipe legs."""
from itertools import product

import sympy as sp
from check_sharp_history_writer import FIELD, G, X, a, equal, p, v


def selector():
    one = FIELD.one
    prob_one = FIELD.from_sympy(p) ** 2
    born = [one - prob_one, prob_one]
    split, idle = [], []
    for h in (0, 1):
        flip = X if h else sp.eye(2)
        r = flip * G.T * v
        t = G * flip * v
        u = flip * G * flip * G * v
        contraction = lambda state: FIELD.from_sympy((v.T * state)[0])
        assert equal(r, sp.eye(2)[:, h])
        split.append(contraction(r) * contraction(t)**3 * contraction(u))
        idle.append(contraction(r) * contraction(t)**5 * contraction(u))
    step = FIELD.from_sympy(p)**6
    assert [born[h] * split[h] for h in (0, 1)] == [step, step]
    assert idle == [step, step]

    for d in range(1, 18):
        depth = (d - 1).bit_length()
        weights = [FIELD.zero] * d
        priors = [FIELD.zero] * d
        for bits in product((0, 1), repeat=depth):
            lo, hi = 0, d
            w = mass = one
            for h in bits:
                is_split = hi - lo > 1
                w *= born[h] * (split[h] if is_split else idle[h])
                mass *= born[h]
                if is_split:
                    middle = (lo + hi) // 2
                    lo, hi = (middle, hi) if h else (lo, middle)
            assert hi == lo + 1
            weights[lo] += w
            priors[lo] += mass
        assert weights == [step**depth] * d
        assert sum(priors, FIELD.zero) == one
        if d == 2:
            assert priors == born and priors[0] != priors[1]
    print("positive Golden selector: each of d=1..17 leaves has cold weight p^(6m)")


def rotation(t):
    return sp.Matrix([[1-t*t, -2*t], [2*t, 1-t*t]]) / (1+t*t)


def logdet_jet(cold, dcold, alpha):
    kernel = sp.eye(cold.cols) + alpha * cold.T * cold
    return -alpha * sp.trace(kernel.inv() * (dcold.T * cold + cold.T * dcold))


def source():
    t = sp.symbols("x0:4")
    live = sp.Matrix([[2, 1], [-1, 3]]) / 7
    motion = sp.Matrix([[1, -2], [3, 2]]) / 11
    angle = sp.Rational(1, 3)
    ref = sp.Matrix([1, 0])
    cut = ref * ref.T
    # Separate realizations of BOTH legs of the same true rank-one test.
    probe = (ref.T * rotation(angle+t[2]).T * cut * rotation(angle+t[1]) * ref)[0]
    record = sp.Rational(2, 3) + t[3]/11
    block = (live + t[0]*motion) * probe * record
    center = dict.fromkeys(t, 0)
    cold = block.subs(center)
    jets = [block.diff(x).subs(center) for x in t]
    assert all(j != sp.zeros(2) for j in jets)
    A, dA = cold.T*cold, cold.T*jets[0]+jets[0].T*cold
    assert A*dA != dA*A
    alpha = sp.Rational(3, 7)
    for d in (2, 3, 4, 5):
        scale = sp.Rational(2, 9)  # test an arbitrary fixed selector amplitude
        slopes = [sp.Rational((-1)**k*(k+1), 7) for k in range(d)]
        terms = [sum((jets[role] * slopes[(k+role) % d]
                      for role in range(4)), sp.zeros(2)) for k in range(d)]
        tangent = scale * sum(terms, sp.zeros(2))/d
        average = sum(slopes)/d
        expected = sum(jets, sp.zeros(2))*average
        assert tangent == scale*expected
        assert logdet_jet(scale*cold, tangent, alpha) == logdet_jet(
            cold, expected, alpha*scale**2)
        for i in range(d):
            row = sum((jets[j] for k in range(d) for j in range(4)
                       if (k+j) % d == i), sp.zeros(2))
            assert row == sum(jets, sp.zeros(2))

    # Nuisance gain times two independently varied calibration legs.
    gain = 1 + t[0]
    response = gain * (1+t[3]/10) / (1+(t[1]+t[2])/2)
    j = [response.diff(x).subs(center) for x in t]
    assert j == [1, -sp.Rational(1, 2), -sp.Rational(1, 2), sp.Rational(1, 10)]
    assert sum(j[:3]) == 0 and sum(j) == sp.Rational(1, 10)
    # A residual failure branch routed only into one uncalibrated old program.
    fail = sp.Rational(1, 9)
    assert (1-fail)*sum(j[:3])/2 + fail*j[0] == fail
    # An ordinary Born read on the two routed branches has a different vertical.
    assert equal(p - p**2, p**3)
    print("noncommuting two-column matrix, independent forward/reverse jets and failure checked")


if __name__ == "__main__":
    selector()
    source()
