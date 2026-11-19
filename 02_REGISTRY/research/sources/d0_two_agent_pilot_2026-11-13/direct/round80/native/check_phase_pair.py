"""Exact native words, finite-field obstruction, and a full-clock phase contrast."""
from collections import Counter
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round79" / "writer"))
from check_sharp_history_writer import FIELD, G, X, a, e0, equal, execution, gate, nt, p, v


def swap(i, j):
    return (gate("CX", i, j), gate("CX", j, i), gate("CX", i, j))


def routed_phase(q):
    src = gate("SourceI", 0, 1, 2)
    return swap(q, 0) + (src, src) + swap(q, 0)


def ordered_phase_pair():
    z, w = routed_phase(3), swap(3, 4)
    phase_same, phase_split = z + w + w + z, z + w + z + w
    assert Counter(phase_same) == Counter(phase_split)
    assert len(phase_same) == len(phase_split) == 22
    Z = sp.diag(1, -1)
    for word, desired in ((phase_same, sp.eye(32)),
                          (phase_split, sp.kronecker_product(sp.eye(8), Z, Z))):
        matrix = nt.word_matrix(execution(5, word, 0, (1, 2)), max_qubits=5,
                                max_expanded_stages=22)
        assert matrix == desired
    return z, w


def encoder(n):
    k = (n + 5) // 6
    padding = 6*k - n
    wires = 3 + 6*k + k
    seed = 3
    sharp = range(4, 3+n)
    t_aux = range(3+n, 3+n+padding)
    u_aux = range(3+6*k, wires)
    gates = []
    for target in sharp:
        reset = nt.inverse_word(execution(wires, [gate("G", target)], 0, (1, 2)),
                                max_qubits=wires, max_expanded_stages=11)
        gates.extend((*reset, gate("CX", seed, target)))
    for target in t_aux:
        gates.extend((gate("CX", seed, target), gate("G", target)))
    for target in u_aux:
        gates.extend((gate("G", target), gate("CX", seed, target),
                      gate("G", target), gate("CX", seed, target)))
    e = nt.Execution(wires, tuple(range(3, wires)), (), tuple(gates),
                     nt.G_CX_SOURCE_I, 0, (1, 2))
    budget = 12*(n-1) + 2*padding + 4*k
    inventory = nt.inventory(e, max_qubits=wires, max_expanded_stages=budget)
    assert (inventory.blank_count, len(gates)) == (7*k, budget)
    return k, padding


def check_encoders():
    f_p, f_a = FIELD.from_sympy(p), FIELD.from_sympy(a)
    for h in (0, 1):
        flip = X if h else sp.eye(2)
        assert equal(flip*G.T*v, sp.eye(2)[:, h])
        t, u = G*flip*v, flip*G*flip*G*v
        assert equal((v.T*t)[0], (a, p)[h])
        assert equal((v.T*u)[0], (p**3, 1)[h])
    for n in (1, 2, 5, 6, 7, 12, 14, 30):
        k, pad = encoder(n)
        gain = f_p**(6*k)
        assert f_a**(n+pad)*f_p**(3*k) == f_p**(n+pad) == gain
        for sign in (1, -1):
            high = gain**4 * (f_a+sign*f_p)**4
            low = gain**4 * (f_a-sign*f_p)**4
            assert high-low == sign*8*f_a*f_p*gain**4
            # Direct use of the true passive v after an inverse encoder.
            high = (f_a*f_a+sign*f_p*f_p)**4
            low = (f_a*f_a-sign*f_p*f_p)**4
            assert high-low == sign*(1-f_p**12)
            # One shared real c for a literal two-rail code, including c=0.
            def full(orientation):
                return (f_p*(f_a**(2*n)*f_a+orientation*f_p**(2*n)*f_p)**2
                        + f_p**2*(f_a*f_p)**(2*n)*(f_a+orientation*f_p)**2)
            assert full(sign)-full(-sign) == sign*4*f_a*f_p*(f_a*f_p)**(2*n)
        S = 44
        z = F(1, 2**20)
        def heat_bound(m):
            return F(S, 50) * F(7, 200)**(4*m) / (4**m*factorial(4*m))
        assert heat_bound(1) < z*(1-F(2, 3)**12)
        assert heat_bound(2*k+2) < z * 2 * F(1, 2)**(24*k)
    print("native encoders for n=1..30 (representative widths), equal cold weights and signed full-clock inequalities")


def mul4(x, y):
    # omega=2, omega^2=3, omega^2+omega+1=0.
    out = 0
    while y:
        if y & 1:
            out ^= x
        y >>= 1
        x = (x << 1) ^ (7 if x & 2 else 0)
    return out


def moments(amplitudes):
    bit_count = (len(amplitudes)-1).bit_length()
    total, means = 0, [0]*bit_count
    for index, value in enumerate(amplitudes):
        total ^= value
        for bit in range(bit_count):
            if index >> bit & 1:
                means[bit] ^= value
    return total, means


def no_complement():
    assert mul4(2, 2) == 3 and mul4(3, 2) == 1
    # The signed Spin source reduces to the actual linear permutation on basis bits.
    for x in range(8):
        port = (x >> 2) & 1
        assert abs(nt.SOURCE_I_LOCAL[x ^ port, x]) == 1
    for h in range(3):
        for value in range(4):
            # Check the affine first-moment update on every one-column input.
            for x in range(8):
                vec = [0]*8
                vec[x] = value
                new = [mul4(2, vec[y]) ^ mul4(3, vec[y^(1<<h)]) for y in range(8)]
                mass, m = moments(vec)
                m[h] ^= mul4(3, mass)
                assert moments(new) == (mass, m)
    # Integer multiples of omega^2 cannot be one in characteristic two.
    assert 1 not in {0, 3}
    print("positive unitary word cannot create deterministic parity one from the all-zero old column")


if __name__ == "__main__":
    ordered_phase_pair()
    check_encoders()
    no_complement()
