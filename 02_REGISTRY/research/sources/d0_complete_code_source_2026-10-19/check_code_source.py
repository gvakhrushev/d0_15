#!/usr/bin/env python3
"""Bounded controls for the complete-code-class source theorem; stdlib only.

All golden interval decisions are exact in Q(sqrt(5)); full finite laws,
scores, and binomial hostile identities use rational arithmetic. Logarithmic
inequalities use floating arithmetic, separately from those exact controls.
Does not execute a native D0 device or certify a GR solution.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
import math


@dataclass(frozen=True)
class Q5:
    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def cast(x):
        return x if isinstance(x, Q5) else Q5(F(x))

    def __add__(self, x):
        x = self.cast(x)
        return Q5(self.a + x.a, self.b + x.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, x):
        return self + (-self.cast(x))

    def __mul__(self, x):
        x = self.cast(x)
        return Q5(self.a*x.a + 5*self.b*x.b, self.a*x.b + self.b*x.a)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = Q5(F(1))
        for _ in range(n):
            out = out * self
        return out

    def sign(self):
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        d = a*a - 5*b*b
        assert d != 0  # sqrt(5) irrational; a,b nonzero rational
        return ((d > 0) - (d < 0)) * ((a > 0) - (a < 0))

    def __lt__(self, x):
        return (self - x).sign() < 0

    def __le__(self, x):
        return (self - x).sign() <= 0


p = Q5(F(-1, 2), F(1, 2))
one = Q5(F(1))
assert p + p*p == one
phi = (1 + math.sqrt(5))/2
ell = math.log(phi)
bphi = 2 + math.log(2)/ell


def cost(w):
    return sum(1 if x == 'F' else 2 for x in w)


def prefix_free(words):
    return len(set(words)) == len(words) and all(
        not b.startswith(a) for i, a in enumerate(words)
        for j, b in enumerate(words) if i != j)


def golden_code(law):
    """Existing owner's midpoint construction, with exact interval tests."""
    assert sum(law.values(), F(0)) == 1
    out = {}
    cumulative = F(0)
    for y, mass in sorted(law.items()):
        assert mass > 0
        mid = Q5(cumulative + mass/2)
        left, width = Q5(), one
        word = ''
        while Q5(mass/2) < width:
            previous = width
            cut = left + width*p
            if mid < cut:
                word += 'F'
                width = width*p
            else:
                word += 'R'
                left = cut
                width = width*p*p
        assert Q5(cumulative) <= left
        assert left + width <= Q5(cumulative + mass)
        assert Q5(mass/2) < previous
        assert Q5(mass/2)*p*p < width
        assert width == p**cost(word)
        out[y] = word
        cumulative += mass
    assert prefix_free(list(out.values()))
    assert sum((p**cost(w) for w in out.values()), Q5()) <= one
    return out


def type_law(words, key):
    counts = Counter(key(w) for w in words)
    T = len(counts)
    return {w: F(1, T*counts[key(w)]) for w in words}, T


def source_control(P, score, code, B, Kbound, N):
    assert sum(P.values(), F(0)) == 1
    assert sum((P[w]*score[w] for w in P), F(0)) == 0
    lengths = {w: cost(code[w]) for w in P}
    assert len(set(code.values())) == len(P)
    R = {w: lengths[w] + math.log(float(P[w]))/ell for w in P}
    assert max(R.values()) <= B + 1e-10
    I = float(sum((P[w]*score[w]**2 for w in P), F(0)))
    mass = sum((p**lengths[w] for w in P), Q5())
    assert mass <= Kbound
    a = math.log(Kbound)/ell
    C2 = B*B + a*a + 2*a/ell + 2/(ell*ell)
    ER = sum(float(P[w])*R[w] for w in P)
    ER2 = sum(float(P[w])*R[w]**2 for w in P)
    assert -a - 1e-10 <= ER <= B + 1e-10
    assert ER2 <= C2 + 1e-10
    # Exact derivative of the finite code expectation, not finite differences.
    dcode = float(sum((P[w]*score[w]*lengths[w] for w in P), F(0)))/N
    dentropy = -sum(float(P[w]*score[w])*math.log(float(P[w])) for w in P)/(N*ell)
    covariance = sum(float(P[w]*score[w])*R[w] for w in P)/N
    assert abs(dcode - dentropy - covariance) < 1e-10
    bound = math.sqrt(C2*I)/N
    assert abs(covariance) <= bound + 1e-10
    return {'source_error': covariance, 'source_bound': bound,
            'fisher': I, 'cost_max': max(lengths.values()), 'code_mass_bound': Kbound}


def iid_controls():
    reports = []
    for N in range(1, 7):
        words = list(product((0, 1), repeat=N))
        Q, T = type_law(words, sum)
        code = golden_code(Q)
        # Retain all outcomes but give one the empty complete description.
        # This is injective and non-prefix; it is no longer Kraft<=1.
        nonprefix = dict(code)
        nonprefix[words[0]] = ''
        assert not prefix_free(list(nonprefix.values()))
        assert one < sum((p**cost(w) for w in nonprefix.values()), Q5())
        for q in (F(1, 3), F(1, 2), F(1, 100)):
            P = {w: q**sum(w)*(1-q)**(N-sum(w)) for w in words}
            score = {w: F(sum(w), 1)/q - F(N-sum(w), 1)/(1-q) for w in words}
            assert all(P[w] <= T*Q[w] for w in words)
            for name, current in (('prefix', code), ('injective_nonprefix', nonprefix)):
                Kbound = 1 if name == 'prefix' else max(map(cost, current.values()))+1
                report = source_control(P, score, current, math.log(T)/ell+bphi, Kbound, N)
                assert abs(report['fisher'] - float(N/(q*(1-q)))) < 1e-9
                reports.append({'N': N, 'q': str(q), 'code': name, **report})
    return reports


def markov_control():
    N, q = 6, F(1, 3)
    words = list(product((0, 1), repeat=N+1))
    pi = {0: F(2, 5), 1: F(3, 5)}
    tr = {(0, 0): q, (0, 1): 1-q,
          (1, 0): 1-2*q/3, (1, 1): 2*q/3}
    dt = {(0, 0): F(1), (0, 1): F(-1),
          (1, 0): F(-2, 3), (1, 1): F(2, 3)}
    def key(w):
        c = Counter(zip(w, w[1:]))
        return (w[0], *(c[e] for e in sorted(tr)))
    Q, T = type_law(words, key)
    P, score, innovations = {}, {}, {}
    grouped = defaultdict(set)
    for w in words:
        val = pi[w[0]]
        inc = []
        for e in zip(w, w[1:]):
            val *= tr[e]
            inc.append(dt[e]/tr[e])
        P[w], score[w], innovations[w] = val, sum(inc, F(0)), inc
        grouped[key(w)].add(val)
    assert all(len(v) == 1 for v in grouped.values())
    assert T <= 2*(N+1)**4
    assert all(P[w] <= T*Q[w] for w in words)
    for i in range(N):
        for j in range(i):
            assert sum((P[w]*innovations[w][i]*innovations[w][j] for w in words), F(0)) == 0
    fullI = sum((P[w]*score[w]**2 for w in words), F(0))
    sumI = sum((P[w]*sum((v*v for v in innovations[w]), F(0)) for w in words), F(0))
    assert fullI == sumI
    code = golden_code(Q)
    result = source_control(P, score, code, math.log(T)/ell+bphi, 1, N)
    return {'steps': N, 'complete_histories': len(words), 'types': T,
            'martingale_fisher_exact': str(fullI), **result}


def binomial_second_jet(m):
    N = 4*m*m
    b = N//2 + m
    finite = -F(2*(N-1)*(2*m+1), b)*F(math.comb(N-2, b-1), 2**(N-2))
    if m <= 8:
        direct = sum((F(math.comb(N, k), 2**N) * F(16*(k-N//2)**2-4*N, N)
                      for k in range(N//2-m, N//2+m+1)), F(0))
        assert finite == direct
        first = sum((F(math.comb(N, k), 2**N) * F(4*(k-N//2), N)
                     for k in range(N//2-m, N//2+m+1)), F(0))
        assert first == 0
    return {'m': m, 'N': N, 'second_source_difference': float(finite)}


def literal_description_control():
    N, theta = 5, F(1, 2)
    words = list(product((0, 1), repeat=N))
    binary = {w: ''.join('10' if bit else '0' for bit in w) for w in words}
    assert len(set(binary.values())) == len(words)
    P = {w: theta**sum(w)*(1-theta)**(N-sum(w)) for w in words}
    score = {w: F(sum(w), 1)/theta-F(N-sum(w), 1)/(1-theta) for w in words}
    rate = sum((P[w]*len(binary[w]) for w in words), F(0))/N
    derivative = sum((P[w]*score[w]*len(binary[w]) for w in words), F(0))/N
    entropy_derivative = math.log(float((1-theta)/theta))/ell
    assert rate == 1+theta and derivative == 1 and entropy_derivative == 0
    return {'literal_rate': str(rate), 'literal_source': str(derivative),
            'entropy_source': entropy_derivative,
            'missing_premise': 'competitive same-object decoder equivalence'}


def main():
    counts = [1, 1]
    for c in range(2, 31):
        counts.append(counts[-1] + counts[-2])
    for c, count in enumerate(counts):
        assert count*p**c <= one
    iid = iid_controls()
    markov = markov_control()
    hostile = [binomial_second_jet(m) for m in (1, 2, 3, 4, 8, 32, 128)]
    limit = -8*math.exp(-0.5)/math.sqrt(2*math.pi)
    assert abs(hostile[-1]['second_source_difference']-limit) < 0.00003
    literal = literal_description_control()
    print(json.dumps({
        'status': 'PASS',
        'scope': 'finite code/source controls; analytic proofs in owner; physical GR open',
        'exact_golden_cost_levels': len(counts),
        'iid_code_source_fixtures': len(iid),
        'iid_small_probability_example': [r for r in iid if r['N'] == 6 and r['q'] == '1/100'],
        'correlated_complete_markov': markov,
        'second_jet_hostile': hostile,
        'second_jet_limit': limit,
        'literal_description_hostile': literal,
        'full_D0_price_selected': False, 'generic_joint_recovery': False, 'GR_closed': False
    }, indent=2))


if __name__ == '__main__':
    main()
