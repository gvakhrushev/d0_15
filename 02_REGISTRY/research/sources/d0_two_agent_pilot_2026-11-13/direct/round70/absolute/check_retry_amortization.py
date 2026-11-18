"""Exact checks for the emitted 0/10 length and the retained first-hit record.

Fresh fully regenerated trials have a common pointwise readiness gamma. Every
completed trial has the same long-word probability u. A final abort emits 0.
Repeated words are deterministic copies of the one output. The emitted length
omits the separately paid attempts, flags, registration, preparation and clock.
"""

from fractions import Fraction as F

import sympy as sp


def first_hit(gamma, u, attempts):
    """Physical records (first successful attempt, B), plus the unique abort."""
    survival = F(1)
    records = {}
    for attempt in range(1, attempts + 1):
        hit = survival * gamma
        records[attempt, 0] = hit * (1 - u)
        records[attempt, 1] = hit * u
        survival *= 1 - gamma
    records[None, 0] = survival
    return records


def entropy_coefficients(weights):
    """Coefficients of log_phi(prime) in the entropy of a rational law."""
    coefficients = {}
    for weight in weights:
        if not weight:
            continue
        for number, sign in [(weight.numerator, -1), (weight.denominator, 1)]:
            for prime, exponent in sp.factorint(number).items():
                coefficients[prime] = coefficients.get(prime, 0) + sign * weight * exponent
    return {prime: c for prime, c in coefficients.items() if c}


def check_records(gamma, u, attempts):
    records = first_hit(gamma, u, attempts)
    assert sum(records.values()) == 1
    assert len(records) == 2 * attempts + 1
    success = 1 - (1 - gamma) ** attempts
    times = {}
    for (time, _), weight in records.items():
        times[time] = times.get(time, 0) + weight

    joint = entropy_coefficients(records.values())
    hit_entropy = entropy_coefficients(times.values())
    bit_entropy = entropy_coefficients([1 - u, u])
    for prime in joint.keys() | hit_entropy.keys() | bit_entropy.keys():
        assert joint.get(prime, 0) == hit_entropy.get(prime, 0) + success * bit_entropy.get(prime, 0)

    for copies in (1, 2, 7):
        printed = {
            (time, ('10' if bit else '0',) * copies): probability
            for (time, bit), probability in records.items()
        }
        assert len(printed) == 2 * attempts + 1
        expected_length = sum(weight * sum(map(len, words)) for (_, words), weight in printed.items())
        assert expected_length / copies == 1 + success * u
        assert entropy_coefficients(printed.values()) == joint


def check_general_first_hit():
    # Each successful time of mass a splits into a*u and a*v. In any
    # common logarithm base its incremental entropy is a*h(u), v=1-u.
    a, u, v, q = sp.symbols("a u v q", positive=True)
    k = sp.symbols("k", integer=True, nonnegative=True)
    copies = sp.symbols("m", integer=True, positive=True)
    single_bit_entropy = -u*sp.log(u) - v*sp.log(v)
    split_entropy = -a*u*sp.log(a*u) - a*v*sp.log(a*v)
    split_error = sp.expand_log(split_entropy) + a*sp.log(a) - a*single_bit_entropy
    assert sp.expand(split_error.subs(v, 1-u)) == 0
    assert sp.expand((a*v*copies + a*u*2*copies).subs(v, 1-u) - a*copies*(1+u)) == 0
    # The successful time masses telescope to 1-q^L. Its complement q^L
    # is the unsplit final abort, emitting exactly m short words.
    assert sp.simplify((1-q)*q**k - (q**k - q**(k+1))) == 0


def check_general_jet():
    q, u = sp.symbols("q u", positive=True)
    dgamma, du = sp.symbols("dgamma du", real=True)
    attempts = sp.symbols("L", integer=True, positive=True)
    # q = 1-gamma, hence Dq = -Dgamma.
    observed = (1 - q ** attempts) * u
    derivative = -sp.diff(observed, q) * dgamma + sp.diff(observed, u) * du
    error = -q ** attempts * du + u * attempts * q ** (attempts - 1) * dgamma
    # Exact covector identity. For 0 <= q,u <= 1, the triangle inequality
    # in any dual norm gives q^L ||Du|| + L q^(L-1) ||Dgamma||.
    assert sp.simplify(derivative - du - error) == 0
    for q0, u0 in [(F(1, 2), F(3, 4)), (F(3, 5), F(1, 3))]:
        for g1, u1 in [(F(-1, 6), F(1, 4)), (F(2, 3), F(0)), (F(1, 7), F(-2, 5))]:
            for count in (1, 2, 5):
                jet_error = -q0**count * u1 + u0 * count * q0**(count-1) * g1
                assert abs(jet_error) <= q0**count * abs(u1) + count * q0**(count-1) * abs(g1)


def check_nonconstant_readiness():
    # Exact probability-law witness, without assigning it to D0 hardware.
    # For |t| <= 1/4 the entire interval lies inside 0 < gamma(t),u(t) < 1.
    t = sp.symbols("t", real=True)
    gamma = sp.Rational(1, 2) - t / 6
    u = sp.Rational(3, 4) + t / 4
    for endpoint in (-sp.Rational(1, 4), sp.Rational(1, 4)):
        assert 0 < gamma.subs(t, endpoint) < 1 and 0 < u.subs(t, endpoint) < 1
    count = sp.symbols("L", integer=True, positive=True)
    jet = sp.diff((1 - (1 - gamma)**count) * u, t).subs(t, 0)
    formula = (1 - (count + 1) / 2**count) / 4
    assert sp.simplify(jet - formula) == 0
    assert gamma.diff(t) == -sp.Rational(1, 6) and u.diff(t) == sp.Rational(1, 4)
    assert formula.subs(count, 1) == 0
    assert formula.subs(count, 2) == sp.Rational(1, 16)
    # 2^L > L+1 for L>=2; the correction decreases strictly thereafter.
    ratio = sp.simplify(((count + 2) / 2**(count+1)) / ((count + 1) / 2**count))
    assert sp.simplify(1 - ratio - count / (2 * (count + 1))) == 0
    assert sp.limit(formula, count, sp.oo) == sp.Rational(1, 4)


if __name__ == "__main__":
    for gamma, u in [(F(1, 2), F(3, 4)), (F(2, 5), F(5, 7))]:
        for attempts in (1, 2, 3, 6):
            check_records(gamma, u, attempts)
    check_general_first_hit()
    check_general_jet()
    check_nonconstant_readiness()
    print("PASS: exact first-hit record entropy, deterministic copied length, any-L source error; witness DP_1=0, DP_2=1/16, limit Du=1/4.")
