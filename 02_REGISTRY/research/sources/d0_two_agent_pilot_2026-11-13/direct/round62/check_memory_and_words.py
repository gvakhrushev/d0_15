"""Small independent checks of the stopped archive and the backward native letters."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import sqrt

import sympy as s


def stopped_law(coarse, power):
    """Enumerate actual stopping, aggregating fine labels only after powering."""
    @lru_cache(None)
    def lengths(seen):
        totals = defaultdict(lambda: F(0))
        for symbol, weight in coarse.items():
            if symbol in seen:
                totals[len(seen) + 1] += weight
            else:
                for t, submass in lengths(seen | {symbol}).items():
                    totals[t] += weight * submass
        return totals

    totals = lengths(frozenset())
    if power == 1:
        assert sum(totals.values()) == 1
    return totals


def archive_checks():
    # Rational fixture permits exact enumeration of every paid fine history for k=1.
    q, u, flag = F(2, 5), F(3, 8), F(3, 5)
    probes = ((1-q)*(1-u), (1-q)*u, q)
    fine = [(int(i == j == 2), probes[i] * probes[j] * f)
            for i, j in product(range(3), repeat=2) for f in (flag, 1-flag)]
    for order in (1, 2, 3):
        weights = defaultdict(lambda: F(0))
        for symbol, mass in fine:
            weights[symbol] += mass**order
        direct = defaultdict(lambda: F(0))
        for x, px in fine:
            for y, py in fine:
                if x == y:
                    direct[2] += (px*py)**order
                else:
                    for _, pz in fine:
                        direct[3] += (px*py*pz)**order
        assert direct == stopped_law(weights, order)
        for k in (1, 2, 3):
            words = {bits: (weights[0]/(flag**order+(1-flag)**order))**bits.count(0)
                           * (weights[1]/(flag**order+(1-flag)**order))**bits.count(1)
                           * (flag**order+(1-flag)**order)
                     for bits in product((0, 1), repeat=k)}
            totals = stopped_law(words, order)
            a, B = sum(words.values()), sum(v*v for v in words.values())
            assert totals[2] == B
            assert all(v <= (t-1)*a**(t-2)*B for t, v in totals.items())
            if order > 1:
                mean = sum(t*v for t, v in totals.items()) / sum(totals.values())
                assert mean <= 2/(1-a)**3
    # Full matrix derivative away from the scalar-effect section (moving prior).
    t = s.symbols('t', real=True)
    rho = s.Matrix([[s.Rational(2, 3)+t, t], [t, s.Rational(1, 3)-t]])
    E = s.eye(2)*s.Rational(2, 5) + t*s.Matrix([[2, 1], [1, -1]])
    for order in (2, 3):
        raw = sum(s.trace((rho*effect)**order) for effect in (E, s.eye(2)-E))
        ratio = raw/s.trace(rho**order)
        probs = [s.Rational(2, 5), s.Rational(3, 5)]
        escort = (rho**order/s.trace(rho**order)).subs(t, 0)
        score = s.trace(escort * E.diff(t))
        expected = order*score*(probs[0]**(order-1)-probs[1]**(order-1))
        assert s.simplify(ratio.diff(t).subs(t, 0)-expected) == 0
        assert expected != 0


def transfer_checks():
    p = (s.sqrt(5)-1)/2
    a = s.sqrt(p)
    D = s.diag(a, p)
    G = s.Matrix([[a, -p], [p, a]])
    rawG = s.Matrix([[1, p], [-1, 1]])/2
    exact = lambda M: all(s.simplify(s.radsimp(x)) == 0 for x in M)
    assert exact(D*rawG*D.inv()-G.T/(2*a))
    assert exact(s.Matrix([[p, p**2]])*D.inv()-s.Matrix([[a, p]]))
    CX = s.eye(4)
    CX.row_swap(2, 3)
    DD = s.kronecker_product(D, D)
    rawCX = s.diag(a, a, p, 1)*CX
    assert exact(DD*rawCX*DD.inv()-a*CX.T)
    # Noncommuting operations on a control wire: genuinely distinct terminal records.
    X, Y = s.kronecker_product(G, s.eye(2)), CX
    e0 = s.eye(4)[:, 0]
    E = s.diag(0, 0, 0, 1)
    factor = a/(2*a)
    values = []
    for V, M in ((X*Y, a*Y.T*X.T/(2*a)), (Y*X, X.T*a*Y.T/(2*a))):
        assert exact(M-factor*V.T)
        m = (e0.T*V.T*E*V*e0)[0]
        assert s.simplify((e0.T*M*E*M.T*e0)[0] - factor**2*m) == 0
        values.append(m)
    assert s.simplify(values[1]-values[0]-p**2) == 0


def central_example():
    p = (sqrt(5)-1)/2
    q = p*p + p**3 * (4 * 0.93793197770933667 * p**7)
    # One paid flag per whole word, both fine probes retained per symbol.
    f = p*p + p**4
    probe = ((1-q)*p, (1-q)*p**2, q)
    s1 = q**4
    s0 = sum(v*v for v in probe)**2-s1
    w0, w1 = f*s0, f*s1
    two, three = w0*w0+w1*w1, 2*w0*w1*(w0+w1)
    print(f"H.1 k=1: q={q:.9f}, Z2={two+three:.9f}, escort mean={(2*two+3*three)/(two+three):.9f}")


def reconstruct_gate():
    a, b, c, d, e = s.symbols("a b c d e", real=True)
    K = s.Matrix([[b, c], [d, e]])
    X = s.Matrix([[0, 1], [1, 0]])
    v = s.Matrix([a, a**2])
    assert s.expand((X*K*X*v)[1]-a*(a*b+c)) == 0
    assert s.expand((X*K*X*K)[1, 0]-b*(c+d)) == 0
    fixed = K.subs({c: -a*b, d: a*b})
    diff = (fixed*v).dot(fixed*v) - (fixed*X*v).dot(fixed*X*v)
    assert s.expand(diff-(a**2-a**4)*(b*b-e*e)) == 0
    assert s.expand((fixed.subs(e, -b)*v)[1]) == 0
    G = s.Matrix([[a, -a**2], [a**2, a]])
    assert fixed.subs(e, b) == b/a*G
    D = s.diag(a, a**2)
    raw = s.simplify(D.inv() * G.T * D)
    assert sum(raw.row(1)) == 0
    x = s.symbols("x")
    assert s.Poly(x**2+x+1, x, modulus=2).is_irreducible


if __name__ == "__main__":
    archive_checks()
    transfer_checks()
    reconstruct_gate()
    central_example()
    print("PASS: stopped records, transverse preparation, matched transfers and three-read reconstruction")
