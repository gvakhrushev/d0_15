"""Exact Golden full-column and branch checks for two orders and their resets."""
from collections import Counter
from math import log, sqrt
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[4] /
                       "d0_native_execution_domain_2026-10-24"))
import native_execution as native


def execution(word):
    # Canonical RAW births are applied explicitly below, not as zero blanks.
    return native.Execution(4, (), (), tuple(word), profile=native.G_CX_SOURCE_I,
                            source_port=1, source_spin=(2, 3))


def matrix(word):
    return native.word_matrix(execution(word), max_qubits=4,
                              max_expanded_stages=len(word))


def same(actual, expected):
    assert native.exact_matrix_equal(sp.Matrix(actual), sp.Matrix(expected))


def scalar(actual, expected):
    same([[actual]], [[expected]])


def h_phi(x):
    return -(x*log(x) + (1-x)*log(1-x)) / log(1/float(native.P))


def main():
    a, p = native.A, native.P
    zero, one, v = sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([a, p])
    tags_b = (zero, sp.Matrix([2*a*p, p**3]))
    g = native.Gate("G", (1,))
    cx = native.Gate("CX", (0, 1))
    back = native.Gate("CX", (1, 0))
    inverse_g = native.inverse_word(execution([g]), max_qubits=4, max_expanded_stages=5)
    word_a, word_b = inverse_g + (cx,), (cx,) + inverse_g
    assert len(word_a) == len(word_b) == 6 and Counter(word_a) == Counter(word_b)
    spin = sp.eye(4)
    tensor = sp.kronecker_product
    for word, tags in ((word_a, (zero, one)), (word_b, tags_b)):
        for x, tag in zip((zero, one), tags):
            same(matrix(word)*tensor(x, v, spin), tensor(x, tag, spin))
            scalar(tag.dot(tag), 1)
    overlap = tags_b[0].dot(tags_b[1])
    scalar(overlap, 2*a*p)
    scalar(1-overlap**2, p**6)
    scalar(p**3*(1-overlap**2), p**9)
    scalar(p**2 * tags_b[1][1]**2, p**8)
    scalar(p**2 * tags_b[1][0]**2, 4*p**5)
    scalar(p + 4*p**5 + p**8, 1)
    # Both exact erasure on A and the worst-branch optimal approximation
    # on B retain the entire four-dimensional unknown Spin as an identity.
    swap = (cx, back, cx)
    recovery = (g, cx) + inverse_g + swap + inverse_g
    assert len(recovery) == 15
    optimal = (sp.Matrix([a, -p]), sp.Matrix([p, a]))
    for x, tag, best in zip((zero, one), tags_b, optimal):
        same(matrix((back,)) * tensor(x, x, spin), tensor(zero, x, spin))
        same(matrix(recovery) * tensor(x, tag, spin), tensor(zero, best, spin))
        scalar(tag.dot(best)**2, p)
    scalar(optimal[0].dot(optimal[1]), 0)
    scalar((1+p**3)/2, p)
    scalar(1-p, p**2)

    # Complete adaptive stopping tree on binary labels. Raw printed lengths
    # per label are 1 and 2. The final empty branch at the outer root costs 0.
    words = ("0", "100", "101", "11")
    lengths = [len(w) + w.count("1") for w in words]
    weights = [p**length for length in lengths]
    scalar(sum(weights), 1)
    mean_length = sum(w*l for w, l in zip(weights, lengths))
    mean_stops = sum(w*len(s) for w, s in zip(weights, words))
    scalar(mean_length, (1+p**2)*mean_stops)

    q = float(p**2)
    golden_entropy = h_phi(q)
    assert abs(golden_entropy - (1+q)) < 1e-13
    eigen_small = (1-sqrt(1-4*float(p**9)))/2
    e_b = h_phi(eigen_small)
    assert 0 < e_b < golden_entropy
    print("PASS full Spin columns, equal six addressed gates, A reset, B optimal reset")
    print(f"p={float(p):.12f}, H={golden_entropy:.12f}, E_B={e_b:.12f}, "
          f"H(X|R)_B={golden_entropy-e_b:.12f}, event 11={float(p**8):.12f}")


if __name__ == "__main__":
    main()
