"""Full-column tail equalizer and retained balanced-controller envelope."""
import json
import math
import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

from check_source_price import load_control, need
from check_balanced_controller_source import (
    SIZE, ids, N, NB, D1, D2, E1, E2, R1, R2, TN, TD1, TD2, TR1, TR2,
    p, r, a, ell, birth, oneq, cx, nc1, f, analytic_table, build,
)


def main():
    ne, digest = load_control()
    gate = ne.Gate
    source = dict(profile=ne.G_CX_SOURCE_I, source_port=2, source_spin=(3, 4))
    original = ne.Execution(5, (), (), (gate('G', (1,)),), **source)
    inverse = ne.inverse_word(original, max_qubits=5, max_expanded_stages=100)
    # Qubit 0 is Nbar, qubit 1 is TN. Port and spin are arbitrary inputs.
    word = inverse + (gate('CX', (0, 1)), gate('G', (1,)), gate('CX', (0, 1)))
    actual = ne.Execution(5, (), (), word, **source)
    inventory = ne.inventory(actual, max_qubits=5, max_expanded_stages=100)
    matrix = ne.word_matrix(actual, max_qubits=5, max_expanded_stages=100)
    expected = sp.kronecker_product(sp.diag(sp.eye(2), ne.G_LOCAL.T ** 2), sp.eye(8))
    exact_matrix = DomainMatrix.from_Matrix(matrix).convert_to(ne.GOLDEN_FIELD)
    target_matrix = DomainMatrix.from_Matrix(expected).convert_to(ne.GOLDEN_FIELD)
    need(exact_matrix == target_matrix, 'compiled equalizer on every column')
    need((inventory.g_count, inventory.cx_count, inventory.source_i_count) == (2, 8, 4),
         'actual forward-only inverse and port routing inventory')

    G = np.array([[a, -p], [p, a]])
    v = np.array([a, p])
    pre0, pre1 = G @ v, np.array([1.0, 0.0])
    post0, post1 = G.T @ G.T @ pre0, pre1
    need(np.linalg.norm(post0 - post1) < 1e-14, 'equalized live conditional tails')
    need(abs(pre0[1] ** 2 - 4 * p ** 3) < 1e-14 and pre1[1] == 0,
         'genuine inequivalent pre-equalizer tail states')

    def branches(t, n, u):
        state = np.zeros(SIZE)
        state[0] = 1
        for wire, value in ((N,u),(D1,r),(D2,r),(E1,t),(E2,0),
                            (R1,r),(R2,r),(TN,r),(TD1,r),(TD2,r),
                            (TR1,r),(TR2,r)):
            state = birth(state, wire, value)
        state = cx(state, N, NB)
        state = oneq(state, NB, np.array([[0.0, 1.0], [1.0, 0.0]]))
        outcomes = nc1(state, N)
        need(float(np.sum(outcomes[2] * outcomes[2])) < 1e-25, 'invalid N outcome absent')
        state = outcomes[n] / math.sqrt(u if n else 1 - u)
        state = oneq(state, TN, G.T)
        state = cx(state, NB, TN)
        state = oneq(state, TN, G)
        state = cx(state, NB, TN)
        need(np.linalg.norm(state[(ids & (1 << TN)) != 0]) < 1e-14,
             'actual corrected tail on both branches')
        table = {}
        for d1, v1 in enumerate(nc1(state, D1)[:2]):
            for d2, v2 in enumerate(nc1(v1, D2)[:2]):
                before1 = cx(v2, E1 if d1 == 0 else N, R1)
                for b1, v3 in enumerate(nc1(before1, R1)[:2]):
                    before2 = cx(v3, E1 if d2 == 0 else NB, R2)
                    for b2, v4 in enumerate(nc1(before2, R2)[:2]):
                        table[d1, d2, b1, b2] = v4
        return table

    # Final swap includes the heads AND the retained detector tails.
    pairs = ((N,NB),(D1,D2),(TD1,TD2),(R1,R2),(TR1,TR2))
    permutation = ids.copy()
    for x, y in pairs:
        permutation ^= (((permutation >> x) ^ (permutation >> y)) & 1) * ((1 << x) | (1 << y))
    err = 0.0
    for t in (0, 1):
        positive0, positive1 = branches(t, 0, r), branches(t, 1, r)
        for (d1,d2,b1,b2), vector in positive0.items():
            swapped = positive1[d2,d1,b2,b1]
            err = max(err, float(np.linalg.norm(vector[permutation] - swapped)))
        need(abs(sum(float(np.sum(v * v)) for v in positive0.values()) - 1) < 1e-12,
             'full conditional retained detector state')
    need(err < 1e-12, 'final simultaneous branch permutation')

    # Correcting an already recorded tail is unitary and preserves the actual
    # 32-branch joint registered law. No unrecorded outcomes are discarded.
    for u in (0.2, r, 0.67):
        for t in (0, 1):
            original_law, invalid = build(u, t, shared=True)
            need(invalid < 1e-25, 'original invalid leaves')
            for n in (0, 1):
                final = branches(t, n, u)
                for suffix, vec in final.items():
                    q = (u if n else 1-u) * float(np.sum(vec * vec))
                    need(abs(q - original_law[(n, *suffix)]) < 1e-12,
                         'corrector preserves every registered branch')

    # Exact envelope for arbitrary conditional extra costs, not a physical
    # assignment. Coefficients move with pi to test ALL envelope terms.
    def costs(pi):
        return ((0.30 + 0.02*pi, 0.50 - 0.01*pi),
                (0.45 - 0.03*pi, 0.35 + 0.04*pi))
    da = ((0.02, -0.01), (-0.03, 0.04))
    def optimum(x, y):
        return 1 / (1 + math.exp(ell * (1 + y - x)))
    def envelope(x, y):
        return x + 1 - math.log1p(math.exp(-ell * (1 + y - x))) / ell
    pi = 0.42
    ac = costs(pi)
    uopt = [optimum(*row) for row in ac]
    env = [envelope(*row) for row in ac]
    for t in (0, 1):
        x, y = ac[t]
        u = uopt[t]
        need(abs(f(u) + (1-u)*x + u*y - env[t]) < 1e-12, 'closed entropy envelope')
        need(abs(1 - math.log((1-u)/u)/ell + y - x) < 1e-12, 'controller stationarity')
    def reduced(q):
        acq = costs(q)
        g0,g1 = (envelope(*row) for row in acq)
        return p**7 + 2*p**6*q + r*((1-q)*g0+q*g1)
    d0 = (1-uopt[0])*da[0][0] + uopt[0]*da[0][1]
    d1 = (1-uopt[1])*da[1][0] + uopt[1]*da[1][1]
    dsource = 2*p**6 + r*(env[1]-env[0] + (1-pi)*d0 + pi*d1)
    step = 1e-6
    finite_diff = (reduced(pi+step)-reduced(pi-step))/(2*step)
    need(abs(dsource - finite_diff) < 1e-8, 'complete moving-cost field derivative')
    symmetric_u = optimum(0.7, 0.7)
    need(abs(symmetric_u-r) < 1e-14, 'swap-invariant conditional cost does not move u')
    # Nonnegative sector-specific charge (one code on T=0) reverses the
    # total slope; this is a diagnostic cost, not an assigned Book value.
    counterexample = 2*p**6-r
    need(counterexample < 0, 'independent T-cost survives N-symmetry')

    print(json.dumps({
        'status':'PASS', 'native_source_sha256':digest,
        'compiled_all_columns':inventory.full_dimension,
        'compiler_inventory':{'total':inventory.gate_count,'G':inventory.g_count,
                              'CX':inventory.cx_count,'SourceI':inventory.source_i_count},
        'tail_probability_one_before_n0':round(float(pre0[1]**2), 12),
        'tail_probability_one_before_n1':round(float(pre1[1]**2), 12),
        'tail_probability_one_after_both':round(float(post0[1]**2), 15),
        'final_swap_max_branch_vector_error':float(err),
        'full_retained_wires':13,
        'input_old_right_arbitrary_by_tensor_identity':True,
        'diagnostic_pi':pi,
        'diagnostic_optimal_u':[round(x,12) for x in uopt],
        'diagnostic_full_field_derivative':round(dsource,12),
        'diagnostic_finite_difference_error':float(abs(dsource-finite_diff)),
        'symmetric_cost_recovers_u':round(symmetric_u,12),
        'symmetric_but_T_dependent_slope':round(counterexample,12),
        'actual_book_cost_info_selected':False,
        'actual_growing_clock_and_intermediate_prices_computed':False,
        'GR_closed':False,
    },sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
