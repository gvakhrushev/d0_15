"""A real RAW future separates a marked and an unmeasured original EIGHT tape."""
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[4] /
                       "d0_native_execution_domain_2026-10-24"))
import native_execution as ne


def check_hardware():
    gate = ne.Gate
    ex = ne.Execution(4, (), (), (gate("G", (0,)),), profile=ne.G_CX_SOURCE_I,
                      source_port=1, source_spin=(2, 3))
    swap = (gate("CX",(0,1)), gate("CX",(1,0)), gate("CX",(0,1)))
    z = swap + (gate("SourceI",(1,2,3)),)*2 + swap
    literal = z + ex.gates + z
    compiled = ne.inverse_word(ex, max_qubits=4, max_expanded_stages=17)
    for inverse, count in ((literal,12),(compiled,6)):
        assert [sum(g.op == op for g in inverse) for op in ("G","CX","SourceI")] == [1,count,4]
        full = ne.Execution(4, (), (), inverse, profile=ex.profile,
                            source_port=1, source_spin=(2, 3))
        turn = ne.word_matrix(full, max_qubits=4, max_expanded_stages=17)
        assert ne.exact_matrix_equal(turn, sp.kronecker_product(ne.G_LOCAL.T, sp.eye(8)))
    v = sp.Matrix([ne.A, ne.P])
    assert ne.exact_matrix_equal(ne.G_LOCAL.T*v, sp.Matrix([1,0]))
    marked = sp.diag(ne.P, ne.P**2)
    return_zero = ne.G_LOCAL.T * marked * ne.G_LOCAL
    assert ne.exact_matrix_equal(return_zero[:1,:1], sp.Matrix([[ne.P**2+ne.P**4]]))

    # W, SITE, measured B, oldRIGHT. For every w,b and every old input,
    # reading W at either side of the actual bank gives the same branch map.
    bank = ne.Execution(4, (), (3,), (gate("CX",(0,1)), gate("CX",(1,2))))
    unitary = ne.word_matrix(bank, max_qubits=4, max_expanded_stages=2)
    for w, b in product(range(2),repeat=2):
        pw = sp.diag(*(int(i//8 == w) for i in range(16)))
        pb = sp.diag(*(int((i//2)%2 == b) for i in range(16)))
        late = pw*pb*unitary
        early = pb*unitary*pw
        assert late == early
        # Same registered bit can have zero or unit probability according to SITE.
        for site in (0,1):
            basis = (w*8 + site*4)   # B initialized at zero
            assert (late.T*late)[basis,basis] == int(site^w == b)


def main():
    check_hardware()
    field = sp.QQ.algebraic_field(sp.sqrt(5))
    p = field.from_sympy(ne.P)
    r = p**2+p**4
    one = field.one
    def bounded(value, lower, upper):
        expression = field.to_sympy(value)
        assert (expression-sp.Rational(lower)).is_positive
        assert (sp.Rational(upper)-expression).is_positive

    # Conditional no-click probability: after the positive-price prefix ends
    # each unread trailing marked bit passes the inverse Golden test with r.
    @lru_cache(None)
    def future(deadline, need):
        if need <= 0:
            return r**deadline
        assert deadline > 0
        return p*future(deadline-1, need-1) + p**2*future(deadline-1, need-2)

    past, current = one, one
    for length in range(2,37):
        past, current = current, p*current+r*p**2*past
        assert future(length,length) == current
        if length <= 8:
            direct = field.zero
            for tape in product(range(2),repeat=length):
                total = 0
                for steps, bit in enumerate(tape,1):
                    total += 1+bit
                    if total >= length:
                        break
                prob = p**(length+sum(tape))
                # Given a sharp trailing bit b, inverse G followed by 0 has
                # probability p (b=0) or p^2 (b=1), independently for each bit.
                direct += prob * p**(length-steps+sum(tape[steps:]))
            assert current == direct
    sizes = {24: [840*comb(8,j)//j for j in range(1,9)],
             36: [705600*comb(8,j)//(j*j) for j in range(1,9)]}
    for length, k, lo, hi in [(24,4,".97424974",".97424976"),
                              (36,6,".99611940",".99611942")]:
        adaptive = one-future(length,length)
        bounded(adaptive,lo,hi)
        n = length-k
        prefix = sum((comb(n,j)*p**(n+j) for j in range(k,n+1)), field.zero)
        fixed = prefix*(one-r**k)
        bounded(fixed, ".9007104" if length==24 else ".9689047",
                ".9007105" if length==24 else ".9689048")
        inactive = one-sum(sizes[length])*p**length
        bounded(inactive/5, ".0779865" if length==24 else ".0782878",
                ".0779866" if length==24 else ".0782880")
        print(length, "adaptive, fixed, dark-event bound:",
              *(f"{float(field.to_sympy(x)):.12f}" for x in (adaptive,fixed,inactive/5)))
    print("PASS every port/Spin column; exact stopping recursion, prefix sums and deadline branch maps")


if __name__ == "__main__":
    main()
