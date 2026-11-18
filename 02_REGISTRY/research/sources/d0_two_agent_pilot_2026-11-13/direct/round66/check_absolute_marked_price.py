"""Finite weighted readouts of one stored bit, fresh probes and a stopped tree."""
from fractions import Fraction as F
from itertools import product
from math import comb

import sympy as sp


def one_bit():
    q, w0, w1, dq, dw0, dw1 = sp.symbols("q w0 w1 dq dw0 dw1", positive=True)
    z = (1-q)*w0 + q*w1
    mu = q*w1/z
    direct = -(dq*(w1-w0)+(1-q)*dw0+q*dw1)/z
    score = (q-mu)*dq/(q*(1-q)) - (1-mu)*dw0/w0 - mu*dw1/w1
    assert sp.cancel(direct-score) == 0
    q0, q1 = F(2, 5), F(3, 7)
    for a, b in ((F(1, 100), F(3)), (F(5), F(8, 99)), (F(3), F(3))):
        ratio = ((1-q1)*a+q1*b)/((1-q0)*a+q0*b)
        bounds = sorted(((1-q1)/(1-q0), q1/q0))
        assert bounds[0] <= ratio <= bounds[1]


def repeated_print():
    # Keep the ink factor as an independent exact variable in the binomial identity.
    s, ink = sp.symbols("s ink", positive=True)
    for m in (1, 2, 4):
        for sign in (-1, 1):
            weighted = sum(comb(m, k)*s**k*(1-s)**(m-k)*ink**(3*m+sign*k)
                           for k in range(m+1))
            assert sp.expand(weighted-ink**(3*m)*(1-s+s*ink**sign)**m) == 0
    p = (sp.sqrt(5)-1)/2
    assert sp.simplify(2*p**6 - (18-8*sp.sqrt(5))) == 0
    q0 = F(2, 5)
    for m in (1, 6, 24, 100):
        # Two rational brackets for s lie on either side of the real Golden value.
        for sx in (F(55, 1000), F(56, 1000)):
            ratio = ((1-sx+sx/2)/(1-sx+2*sx))**m
            assert 0 < (1-ratio)/(1-q0+q0*ratio) < 1/(1-q0)
    assert F(55, 1000) < p**6 < F(56, 1000)


def stopped_tree():
    # 0 stops at the first call. Only branch 1 uses the second physical field.
    q0, q1 = F(2, 5), F(3, 7)
    dz0, dz1 = F(7, 13), F(-2, 5)
    leaf_p = ((1-q0), q0*(1-q1), q0*q1)
    leaf_dp = (-dz0, dz0*(1-q1)-q0*dz1, dz0*q1+q0*dz1)
    toll = (F(1, 2), F(3), F(4, 11))
    dtoll = (F(5, 7), F(-3, 8), F(9))
    mass = sum(p*w for p, w in zip(leaf_p, toll))
    mu = [p*w/mass for p, w in zip(leaf_p, toll)]
    visit = mu[1]+mu[2]
    first = (q0-visit)*dz0/(q0*(1-q0))
    second = visit*(q1-mu[2]/visit)*dz1/(q1*(1-q1))
    nuisance = sum(v*dw/w for v, dw, w in zip(mu, dtoll, toll))
    direct = -sum(dp*w+p*dw for dp, w, p, dw in zip(leaf_dp, toll, leaf_p, dtoll))/mass
    assert direct == first+second-nuisance


def golden_match():
    # Actual raw tag bits and the actual one- or two-bit print of each tag.
    x = sp.Symbol("p")
    modulus = x*x+x-1
    def reduce(poly):
        return sp.rem(poly, modulus, x).expand()
    s = x**6
    passive = []
    marked = []
    counts = []
    for law in ({(0,0):s, (1,0):1-s}, {(1,0):1-s, (1,1):s}):
        total_passive = total_marked = count = 0
        for tags, prob in law.items():
            declared = tags + tuple(t for bit in tags for t in ((1,0) if bit else (0,)))
            cylinder = x**sum(1+t for t in declared)
            # Each reference read has two real leaves even when the event fails.
            ref_total = match = 0
            for new in product((0,1), repeat=len(declared)):
                measure = x**sum(1+t for t in new)
                ref_total += measure
                count += 1
                if new == declared:
                    match += measure
            assert reduce(ref_total-1) == 0 and reduce(match-cylinder) == 0
            total_passive += cylinder*ref_total
            total_marked += prob*match
        passive.append(reduce(total_passive))
        marked.append(reduce(total_marked))
        counts.append(count)
    assert counts == [48,96]
    assert passive == [reduce(x**4+x**7), reduce(x**7+x**10)]
    assert marked == [reduce(s*x**4+(1-s)*x**7), reduce((1-s)*x**7+s*x**10)]
    p = (sp.sqrt(5)-1)/2
    assert (5*marked[0]-6*marked[1]).subs(x,p).simplify() > 0
    assert (marked[1].subs(x,p)).simplify() > 0


def fresh_fields():
    q, cap = F(2, 5), F(4, 5)
    for n in (1, 2, 5):
        for coupling in (F(1), F(2, 3)):
            law = {}
            for bits in product((0, 1), repeat=n):
                k = sum(bits)
                adjacent = sum(a*b for a, b in zip(bits, bits[1:]))
                toll = cap**k * coupling**adjacent
                law[bits] = q**k*(1-q)**(n-k)*toll
            total = sum(law.values())
            expected_count = sum(sum(bits)*v for bits, v in law.items())/total
            gain = (n*q-expected_count)/(q*(1-q))
            assert gain >= n*(1-cap)/(1-q+cap*q)
            if coupling == 1:
                assert gain == n*(1-cap)/(1-q+cap*q)
    # Mismatched correlations need not change either marginal at a common centre.
    reference = {(a,b):q**(a+b)*(1-q)**(2-a-b) for a,b in product((0,1), repeat=2)}
    different = {(a,b):p*(1+(a-q)*(b-q)) for (a,b),p in reference.items()}
    assert sum(different.values()) == 1 and different != reference
    assert all(sum(p for bits,p in different.items() if bits[i]) == q for i in range(2))


if __name__ == "__main__":
    one_bit()
    repeated_print()
    stopped_tree()
    golden_match()
    fresh_fields()
    print("PASS: positive one-bit partition, all printed leaves, stopped independent scores, context-dependent fresh-probe gain and matching marginal control.")
