"""Exact branch, passive overlap and commuting activation counts on the paid words."""
from collections import Counter
from itertools import product

import sympy as s


def check_preparation():
    p = (s.sqrt(5) - 1) / 2
    a = s.sqrt(p)
    virgin = s.kronecker_product(s.Matrix([a, p]), s.Matrix([a, p]))
    xor = s.zeros(4)
    for f, y in product(range(2), repeat=2):
        xor[2*(f ^ y)+y, 2*f+y] = 1
    odd = s.diag(0, 0, 1, 1)
    raw = odd*xor*virgin
    target = s.Matrix([0, 0, 1, 1])/s.sqrt(2)
    assert (raw - a*p*s.sqrt(2)*target).applyfunc(s.simplify) == s.zeros(4, 1)
    assert s.simplify(raw.dot(raw) - 2*p**3) == 0
    assert s.simplify(virgin.dot(target)**2 - p*p*(a+p)**2/2) == 0


A, B, U = "CX(e,y)", "CX(y,e)", "SourceI(e)"
moves = (A, B, A)
phase = (*moves, U, U, *moves)
base = (*phase, *phase, A, A)
signed = (*phase, A, *phase, A)


def occupation(word, e, y):
    start = (e, y)
    count, n = Counter(), 0
    for gate in word:
        # L_i^(n+2) acts as -L_i^n on the complete conditional Spin state.
        count[gate, e, y, n % 2] += 1
        if gate == A:
            y ^= e
        elif gate == B:
            e ^= y
        elif gate == U:
            n += e
        else:
            raise ValueError(gate)
    assert (e, y) == start
    return count, n


def check_registers_and_prices():
    assert len(base) == len(signed) == 18 and Counter(base) == Counter(signed)
    z, q_event, p = s.symbols("z Q p")
    difference = 0
    for e in (0, 1):
        address_sum = {word: Counter() for word in (base, signed)}
        for y in (0, 1):
            cnt_base, n_base = occupation(base, e, y)
            cnt_signed, n_signed = occupation(signed, e, y)
            assert n_base == 4*y
            assert n_signed == 4*(1-e)*y + 2*e
            assert n_base % 4 == 0 and n_signed % 4 == 2*e
            address_sum[base].update(cnt_base)
            address_sum[signed].update(cnt_signed)
            mass = 2*p**3*(q_event if e else 1-q_event)/2
            difference += mass*(z**n_signed-z**n_base)
        assert address_sum[base] == address_sum[signed]
    assert s.factor(difference + p**3*q_event*(1-z**2)**2) == 0
    first = s.diff(difference, z).subs(z, 1)
    second = s.diff(difference, z, 2).subs(z, 1) + first
    assert s.simplify(first) == 0
    assert s.simplify(second + 8*p**3*q_event) == 0


def check_four_writers():
    # Condition on odd parity. Q is arbitrary; R is the actual noisy copy of e.
    Q, t = s.symbols("Q t", positive=True)
    laws = {word: Counter() for word in (base, signed)}
    for e, y, noise in product(range(2), repeat=3):
        prob = (Q if e else 1-Q)*(t if noise else 1-t)/2
        report = e ^ noise
        for word in (base, signed):
            bits = []
            a, b = e, y
            for gate in word:
                if gate == A:
                    b ^= a
                elif gate == B:
                    a ^= b
                else:
                    # Same two CX with three genuine blanks on each visit.
                    container = (a, 0, a)
                    assert container in ((0, 0, 0), (1, 0, 1))
                    bits.append(container[0])
            assert bits == ([y]*4 if word == base else [y, y, y^e, y^e])
            laws[word][tuple(bits), report] += prob
    q = t + (1-2*t)*Q
    for word in (base, signed):
        law = laws[word]
        assert s.simplify(sum(law.values()) - 1) == 0
        assert s.simplify(sum(v for (_, r), v in law.items() if r) - q) == 0
        assert s.simplify(sum(v*(4+sum(bits)) for (bits, _), v in law.items()) - 6) == 0
        contrast = sum(v for (bits, _), v in law.items() if bits[0] != bits[2])
        assert s.simplify(contrast - (0 if word == base else Q)) == 0
    # The joint-law factorizations give the Shannon chain rules for any (Q,t).
    for y, r in product(range(2), repeat=2):
        assert s.simplify(laws[base][(y,)*4, r] - (q if r else 1-q)/2) == 0
        for e in range(2):
            v = laws[signed][(y, y, y^e, y^e), r]
            assert s.simplify(v - (Q if e else 1-Q)*(t if r^e else 1-t)/2) == 0


if __name__ == "__main__":
    check_preparation()
    check_registers_and_prices()
    check_four_writers()
    print("PASS: four actual 0/10 encodings, full joint laws, record gain, equal encoded length, same H.1 report.")
    print("PASS: native XOR, retained parity, passive overlap, every conditional occupation, field counting identity and variance.")
