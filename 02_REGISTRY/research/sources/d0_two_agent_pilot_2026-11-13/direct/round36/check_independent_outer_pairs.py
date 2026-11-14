#!/usr/bin/env python3
"""Check actual placements, clock, rational bounds and non-symmetric split."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, itertools, json
import sympy as S
import independent_outer_pairs as f

P = Path(__file__).resolve().parent


def main():
    plan = f.build()
    a,b,n0,T = f.parameters()
    assert n0 == a+b and T == n0+4
    fixtures = 0
    for j in (0,2,42,2687):
        pairs = {(leg,sign):f.endpoint_parts(leg,sign,j)
                 for leg in ('forward','backward') for sign in ('plus','minus')}
        assert pairs['backward','plus']['pre'] == pairs['backward','minus']['pre']
        assert pairs['forward','plus']['post_before_final'] == pairs['forward','minus']['post_before_final']
        for (leg,sign),parts in pairs.items():
            pre_count = f.nb.counts(parts['pre'])
            post_count = f.nb.counts(parts['post_before_final'])
            pre_exp = (a if sign == 'plus' else b) if leg == 'forward' else n0
            post_exp = n0 if leg == 'forward' else (b if sign == 'plus' else a)
            assert pre_count['G'] == pre_exp and post_count['G'] == post_exp-1
            assert pre_count['CX'] == T-pre_exp and post_count['CX'] == T-post_exp
            assert sum(pre_count.values()) == T and sum(post_count.values()) == T-1
            assert f.core.b.physical_tree(parts['last_g']) == f.nb.gate('G',2+j)
            for tree in parts.values():
                for leaf in f.nb.leaves(tree):
                    assert leaf['op'] in ('G','CX')
                    assert not set(leaf['wires']).intersection((0,1,3))
            first = list(itertools.islice(f.execution_stages(leg,sign,j),4))
            assert [s['wire'] for s in first] == [0,1,2,3]
            assert all(s['kind'] == 'canonical_RAW_birth' for s in first)
            fixtures += 1
    # The new padding lengths are >=4. Check the 2/5 identity on every
    # arbitrary three-bit column; the repeat counts themselves are exact.
    positions = {q:i for i,q in enumerate([2,2705,f.core.g.namespace()['layout']['qubits']])}
    for length in range(4,16):
        gates = list(f.nb.expand(f.old.padding(length), 15))
        assert len(gates) == length
        for initial in range(8):
            x = initial
            for gate in gates:
                c,t = map(positions.get, gate['wires'])
                if (x >> c)&1:
                    x ^= 1 << t
            assert x == initial
    for exponent in (a,b,n0):
        twos,fives = f.old.identity_counts(T-exponent)
        assert 2*twos+5*fives == T-exponent
    # Symbolic identity for a completely general real compression, not a
    # reflection or symmetric matrix. The example also catches silently
    # equating the two actual independent analytic rows.
    aa,bb,cc,dd,x,y = S.symbols('a b c d x y', real=True)
    M = S.Matrix([[aa,bb],[cc,dd]])
    J = S.Matrix([[0,-1],[1,0]])
    v = S.Matrix([x,y])
    cf = (v.T*M*J*v)[0]
    cb = (-v.T*J*M*v)[0]
    cp = (v.T*(M*J-J*M)*v)[0]
    assert S.expand(cf+cb-cp) == 0
    assert S.expand(cf-cp/2-(bb-cc)*(x*x+y*y)/2) == 0
    assert S.expand(cf-cb).subs({bb:1,cc:0,x:1,y:0}) == 1
    # Independent clock sum on representative small layouts; every birth
    # and square gate is included, including the final SAM gate.
    clocks = 0
    for n in range(1,6):
        for L in range(1,8):
            for K in range(5):
                dims = [2**i for i in range(n)]+[2**n]*(L-1)
                for k in range(K):
                    dims.extend([2**(n+k),2**(n+k+1)])
                dims.append(2**(n+K))
                assert len(dims) == n+L+2*K
                assert sum(dims) == 2**n*(L-3+4*2**K)-1
                clocks += 1
    budget = f.bounds(int(plan['Nbase_hex'],16))
    assert budget['one_leg_finite_to_analytic_under_Gamma_s'] < F(1,2**73)
    assert budget['j2_each_leg_under_u_Gamma_s_strict_lower'] > F(1,2**46)
    assert plan['backward_pair_original_RAW_checkpoint_marks_identical']
    assert not plan['A31_inverse_J_applied_to_backward_variation']
    assert not plan['same_complete_task_membership_or_FN_fibre_proved']
    for path,digest in plan['source_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
    pins = [Path(__file__), P/'independent_outer_pairs.py', P/'INDEPENDENT_OUTER_PAIRS_PLAN.json']
    result = {'status':'PASS_ACTUAL_OUTER_PLACEMENTS_CLOCK_BUDGET_AND_NONSYMMETRIC_SPLIT',
              'four_word_direction_fixtures':fixtures, 'exact_small_clock_sums':clocks,
              'general_nonsymmetric_split_checked':True,
              'false_exact_actual_half_split_rejected':True,
              'backward_identical_forward_prefix_checked':True,
              'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
              'physical_C_closed':False, 'GR_closed':False}
    (P/'INDEPENDENT_OUTER_PAIRS_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
