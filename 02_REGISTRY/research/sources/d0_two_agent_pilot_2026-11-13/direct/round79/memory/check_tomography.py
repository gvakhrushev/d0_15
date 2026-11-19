"""Exact RAW tomography, certified error propagation, and observable Q8 moments."""
from fractions import Fraction
from pathlib import Path
from math import comb
import sys

import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

SOURCE = Path(__file__).resolve().parents[4] / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(SOURCE))
import native_execution as native


def rational(value):
    return Fraction(int(value.numerator), int(value.denominator))


def abs_upper(element):
    # n/10^8 encloses the positive primitive generator a, root of a^4+a^2=1.
    lo, hi = Fraction(78615137, 10**8), Fraction(78615138, 10**8)
    assert lo**4+lo**2 < 1 < hi**4+hi**2
    low = high = Fraction(0)
    for c in element.to_list():
        terms = (low*lo, low*hi, high*lo, high*hi)
        low, high = min(terms)+rational(c), max(terms)+rational(c)
    return max(abs(low), abs(high))


def exact_design():
    field = native.GOLDEN_FIELD
    def matrix(m):
        return DomainMatrix.from_Matrix(m).convert_to(field)
    def scalar(x):
        return field.from_sympy(x)
    a, p = native.A, native.P
    one = matrix(sp.eye(2))
    x = matrix(sp.Matrix([[0, 1], [1, 0]]))
    z = matrix(sp.diag(1, -1))
    g = matrix(native.G_LOCAL)
    v = matrix(sp.Matrix([a, p]))
    states = [v, g*v, g*g*v]
    basis = (one, x, z)
    def row(vec, ops):
        return [(vec.transpose()*op*vec).to_list()[0][0] for op in ops]
    def make(rows):
        return DomainMatrix(rows, (len(rows), len(rows[0])), field)
    m = make([row(s, basis) for s in states])
    assert m.det() == scalar(-8*a*p**3)
    def kron(left, right):
        l, r = left.to_list(), right.to_list()
        return make([[lv*rv for lv in lrow for rv in rrow] for lrow in l for rrow in r])
    j = matrix(sp.Matrix([[0, -1], [1, 0]]))
    yy = -kron(j, j)
    ops = [kron(l, r) for l in basis for r in basis]+[yy]
    raw_pair = kron(v, v)
    cx = matrix(sp.eye(4).extract((0, 1, 3, 2), (0, 1, 2, 3)))
    entangled = cx*raw_pair
    parity = kron(one, matrix(sp.diag(0, 1)))
    retained = cx*parity*cx*raw_pair
    assert (retained - matrix(sp.Matrix([0, a*p, a*p, 0]))).is_zero_matrix
    assert (retained.transpose()*retained).to_list()[0][0] == scalar(2*p**3)
    rows = [row(kron(l, r), ops) for l in states for r in states]
    assert all(vec[-1] == field.zero for vec in rows)
    rows.append(row(entangled, ops))
    two = make(rows)
    assert rows[-1][-1] == scalar(-2*a*p**4)
    assert two.det() == rows[-1][-1]*m.det()**6
    for design, dimension, limit, normlimit in (
        (m, 2, Fraction(233, 100), Fraction(455, 100)),
        (two, 4, Fraction(1339, 100), Fraction(3382, 100))):
        inv = design.inv()
        rowsums = [sum(abs_upper(x) for x in rowv) for rowv in inv.to_list()]
        assert max(rowsums) < limit
        assert dimension*sum(s*s for s in rowsums) < normlimit**2
        print("rank", design.rank(), "inverse row bound <", float(limit),
              "operator-error factor <", float(normlimit))
    mid, last = g*g*v, g*g*g*g*v
    w = scalar(1/(16*p**3))
    def density(vec):
        return vec*vec.transpose()
    mixed = density(v)*w + density(mid)*(field.one-2*w) + density(last)*w
    assert mixed == one*scalar(sp.Rational(1, 2))
    assert scalar(2*p**9+6*p**13+10*p**14-16*p**12) == field.zero
    assert scalar(p**9/(16*p**12)) == w
    selected = {1: 2, 5: 6, 6: 10}
    assert all(comb(8, i) >= number for i, number in selected.items())
    print("Golden selector with exact accepted mass 16 p^12 verified")


def mul(a, b):
    return np.einsum('ij,jk->ik', a, b)


def check_native_spin():
    g = native.Gate
    gates = (g("CX", (0, 1)), g("CX", (1, 0)), g("SourceI", (1, 2, 3)))
    ex = native.Execution(4, (), (), gates, profile=native.G_CX_SOURCE_I,
                          source_port=1, source_spin=(2, 3))
    ne = native.execution_from_json(native.canonical_json(ex), max_qubits=4,
                                    max_expanded_stages=3)
    field = native.GOLDEN_FIELD
    def exact(m):
        return DomainMatrix.from_Matrix(m).convert_to(field)
    exact_word = exact(native.word_matrix(ne, max_qubits=4, max_expanded_stages=3))
    exact_birth = exact(sp.kronecker_product(sp.eye(2), sp.Matrix([native.A, native.P]), sp.eye(4)))
    exact_c = exact_birth.transpose()*exact_word*exact_birth
    exact_a = exact_c.transpose()*exact_c
    identity = exact(sp.eye(8))
    p, p2 = field.from_sympy(native.P), field.from_sympy(native.P**2)
    assert ((exact_a - identity*p)*(exact_a-identity*p2)).is_zero_matrix
    assert sum(exact_a.to_list()[i][i] for i in range(8)) == field.convert(4)
    word = np.eye(16)
    for gate in gates:
        op = native.gate_matrix(ne, gate, max_qubits=4, max_expanded_stages=3)
        word = mul(np.array(op, dtype=float), word)
    v = np.array([[float(native.A)], [float(native.P)]])
    birth = np.kron(np.kron(np.eye(2), v), np.eye(4))
    pcut = mul(birth, birth.T)
    qcut = mul(word.T, mul(pcut, word))
    effect = mul(birth.T, mul(qcut, birth))
    # The full, validated native example has an actual L_i off-diagonal block.
    assert abs(effect[0,5]) > 0.1
    assert np.linalg.norm(effect-0.5*np.eye(8), ord='fro') > 0.3
    witness = (1, 1j, 2, -1)
    spin = np.array(witness)/np.linalg.norm(witness)
    tau = np.outer(spin, spin.conj())
    state = mul(birth, mul(np.kron(np.eye(2)/2, tau), birth.T))
    moment = np.eye(8)
    for k in range(1, 9):
        proj = qcut if k % 2 else pcut
        state = mul(proj, mul(state, proj))
        moment = mul(moment, effect)
        u = np.trace(moment)/8
        assert abs(np.trace(state)-u) < 1e-12
        expected = (float(native.P)**k + float(native.P)**(2*k))/2
        assert abs(u-expected) < 1e-12
    # No sequence of the actual gates can transfer either quaternion plane's population.
    invariant = np.kron(np.eye(4), np.diag([1, 1, 0, 0]))
    assert np.max(np.abs(mul(invariant, word)-mul(word, invariant))) < 1e-12
    assert abs(np.trace(moment)/8-0.5**8) > 0.002
    print("non-scalar RAW word: alternating success 8 = %.12g" % (np.trace(moment)/8))


if __name__ == "__main__":
    exact_design()
    check_native_spin()
