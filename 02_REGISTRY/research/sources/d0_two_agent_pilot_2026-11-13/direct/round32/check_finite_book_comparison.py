#!/usr/bin/env python3
"""Actual endpoint words, paid padding, stage accounting and source budgets."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import hashlib, itertools, json
import sympy as S
import finite_book_comparison as f
P = Path(__file__).resolve().parent


def main():
    plan = f.build(); a, b = f.powers(); pa, pb = f.align(a,b)
    # Exact padding convention on arbitrary three-bit states, including
    # an odd identity length. No selected bit, clean ancilla or measurement.
    logical = [2,2705,f.core.g.namespace()['layout']['qubits']]
    positions = {q:i for i,q in enumerate(logical)}
    for length in (0,2,4,5,6,7,9,10):
        tree = f.padding(length)
        gates = list(f.nb.expand(tree, 10))
        assert len(gates) == length
        for initial in range(8):
            x = initial
            for gate in gates:
                assert gate['op'] == 'CX'
                c,t = map(positions.get, gate['wires'])
                if (x >> c)&1:
                    x ^= 1 << t
            assert x == initial
    for x in range(30):
        for y in range(30):
            p,q = f.align(x,y)
            assert x+p == y+q
            assert 2*f.identity_counts(p)[0]+5*f.identity_counts(p)[1] == p
            assert 2*f.identity_counts(q)[0]+5*f.identity_counts(q)[1] == q
    # Actual giant exponents remain compact repeat DAGs; inspect every
    # syntactic gate in both endpoint directions at representative SAM wires.
    for j in (0,1,42,2687):
        plus, minus = f.endpoint_parts('plus',j), f.endpoint_parts('minus',j)
        assert sum(f.nb.counts(plus['pre']).values()) == sum(f.nb.counts(minus['pre']).values()) == a+pa == b+pb
        assert sum(f.nb.counts(plus['post_before_final']).values()) == sum(f.nb.counts(minus['post_before_final']).values()) == a+pa-1
        assert plus['last_g'] == minus['last_g'] == f.nb.gate('G',4+j)
        assert f.core.b.physical_tree(plus['last_g']) == f.nb.gate('G',2+j)
        for parts in (plus,minus):
            for tree in parts.values():
                for leaf in f.nb.leaves(tree):
                    assert leaf['op'] in ('G','CX') and not set(leaf['wires']).intersection((0,1,3))
                    assert all(q >= 0 for q in f.core.b.physical_tree(leaf)['wires'])
    # Initial real history begins with RAW births, not a freely supplied
    # SAM/WORK state; K late pairs do not change that early prefix.
    for sign in ('plus','minus'):
        first = list(itertools.islice(f.execution_stages(sign,0),4))
        assert [s['wire'] for s in first] == [0,1,2,3]
        assert all(s['kind'] == 'canonical_RAW_birth' for s in first)
    # Independently sum exact before-stage dimensions for small clocks.
    clocks = 0
    for n in range(1,8):
        for L in range(1,8):
            for K in range(6):
                dimensions = [2**i for i in range(n)] + [2**n]*(L-1)
                for k in range(K):
                    dimensions.extend([2**(n+k),2**(n+k+1)])
                dimensions.append(2**(n+K))
                assert len(dimensions) == n+L+2*K
                assert sum(dimensions) == 2**n*(L-3+4*2**K)-1
                clocks += 1
    # Exact all-input birth;G corner; no selected retained branch.
    p = (S.sqrt(5)-1)/2; a0 = S.sqrt(p)
    v = S.Matrix([a0,p]); G = S.Matrix([[a0,-p],[p,a0]])
    assert S.simplify((v.T*G*v)[0]-a0) == 0
    nbase = plan['early_canonical_RAW_births']+int(plan['endpoint_calls_before_retention'])
    bounds = f.budget(nbase)
    assert bounds['fd_truncation']+bounds['endpoint_angle_synthesis'] < F(1,2**74)
    assert bounds['all_mode_heat'] < F(1,2**76)
    assert bounds['one_SAM_row_total'] < F(1,2**73)
    assert 55*bounds['one_SAM_row_total'] < F(1,2**67)
    reference = json.loads((f.core.g.B/'round63/DETERMINANT_FD_BUDGET.json').read_text())
    rf = F(int(reference['fd_truncation_bound_numerator_hex'],16),int(reference['fd_truncation_bound_denominator_hex'],16))
    ra = F(int(reference['endpoint_synthesis_bound_numerator_hex'],16),int(reference['endpoint_synthesis_bound_denominator_hex'],16))
    assert bounds['fd_truncation'] == rf and bounds['endpoint_angle_synthesis'] == ra
    pins = [Path(__file__), P/'finite_book_comparison.py', P/'FINITE_BOOK_COMPARISON_PLAN.json',
            f.core.g.B/'round63/DETERMINANT_FD_BUDGET.json',
            f.core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',
            f.core.g.B/'round63/SUFFICIENT_G_INDEPENDENT_CHECK.json']
    out = {'status': 'PASS_EXPLICIT_FINITE_ENDPOINT_HISTORY_AND_BOUND_ACCOUNTING',
           'all_column_padding_inputs_per_fixture': 8, 'small_exact_clock_sums': clocks,
           'actual_endpoint_power_bits': [a.bit_length(),b.bit_length()],
           'K_late_retention_pairs': f.K_DEFAULT,
           'same_core_checkpoint_layer_and_final_SAM_gate': True,
           'independent_exact_determinant_bounds_match': True,
           'per_row_full_operator_price_error_under_R11_hypotheses_lt': '2^-73',
           'full_absolute_price_native_centre_or_stationarity_evaluated': False,
           'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
           'physical_C_closed': False, 'GR_closed': False}
    (P/'FINITE_BOOK_COMPARISON_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','small_exact_clock_sums','K_late_retention_pairs')}))


if __name__ == '__main__':
    main()
