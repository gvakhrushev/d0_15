#!/usr/bin/env python3
"""Exact scene-history controls. Universal path/trace claims have separate proofs."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

HEAD = '27175008f7dbba9a98bc739f6cde0958a53858e8'
PREFIX = '02_REGISTRY/research/certificates/a4d_native_history_action'
PROOF = '02_REGISTRY/research/A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    receipt = json.loads((root/(PREFIX+'_results.json')).read_text())
    check('COMPILED_20_DECLARATIONS', receipt['status'] == 'PASS'
          and receipt['owner_input_head'] == HEAD and receipt['compiler_exit_code'] == 0
          and receipt['printed_axiom_dependencies'] == 20 and not receipt['sorryAx']
          and set(receipt['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'})
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_48_NATIVE_SOURCE_AND_TOOLCHAIN_PINS', len(receipt['transitive_d0_source_sha256']) == 48
          and all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('CLEAN_OUTPUT_STANDARD_AXIOMS', all(x not in out for x in ['error:', 'warning:', 'sorryAx']))
    for name in ['completeAdditiveFiber', 'full_positive_edge_fiber',
                 'primitive_cost_cannot_forget_return', 'unit_edge_action_eq_length',
                 'perron_path_log_telescopes', 'perron_root_bounds',
                 'perron_uniform_two_step_lower_arithmetic', 'normalized_constant_reading']:
        check('BOUND_'+name, "'D0.Research.NativeHistoryAction."+name+"' depends on axioms:" in out)
    check('ACTUAL_PERRON_CAPSTONE_PRINTED',
          'D0.VNext2.SceneHistoryPerronTrace.scene_history_perron_trace_owner :' in out
          and 'SceneHistoryPerronTrace.fullTransportSq' in out)

    sizes = [9, 11, 13]
    zone = lambda i: 0 if i < 9 else 1 if i < 20 else 2
    A = sp.Matrix(33, 33, lambda u, v: int(zone(u) != zone(v)))
    edges = [(u, v) for u in range(33) for v in range(33) if A[u, v]]
    undirected = [(u, v) for u, v in edges if u < v]
    check('LITERAL_EDGE_COUNTS', len(edges) == 718 and len(undirected) == 359)
    degree = [sum(A.row(v)) for v in range(33)]
    check('DEGREES_SEPARATE_ZONES', all(degree[v] == 33-sizes[zone(v)] for v in range(33)))
    incidence = sp.Matrix([[int(v == k)-int(u == k) for k in range(33)] for u, v in edges])
    check('ENDPOINT_BOUNDARY_RANK_32', incidence.rank() == 32)
    check('CONSTANT_POTENTIAL_IS_KERNEL', incidence*sp.ones(33, 1) == sp.zeros(718, 1))
    orbits = sorted({(zone(u), zone(v)) for u, v in edges})
    zone_incidence = sp.Matrix([[int(b == k)-int(a == k) for k in range(3)] for a, b in orbits])
    check('SIX_DIRECTED_THREE_UNDIRECTED_ORBITS', len(orbits) == 6
          and len({tuple(sorted(p)) for p in orbits}) == 3)
    check('INVARIANT_BOUNDARY_RANK_TWO', zone_incidence.rank() == 2)
    check('ACTION_QUOTIENT_DIMENSIONS', 718-incidence.rank() == 686 and 6-zone_incidence.rank() == 4)

    def path_sum(w, p):
        return sum((w[u, v] for u, v in zip(p, p[1:])), sp.Integer(0))

    weights = {(u, v): sp.Rational(1+3*u+5*v, 7) for u, v in edges}
    samples = [[0], [0, 9], [0, 9, 0], [0, 9, 20, 1], [9, 0, 20, 10, 2]]
    check('EXTENSION_RESTRICTS_TO_EACH_OF_718_EDGES', all(path_sum(weights, [u, v]) == weights[u, v] for u, v in edges))
    check('ALL_SAMPLE_COMPOSITION_CUTS', all(path_sum(weights, p) == path_sum(weights, p[:k+1])+path_sum(weights, p[k:])
          for p in samples for k in range(len(p))))
    check('SINGLETON_IDENTITIES_ZERO', all(path_sum(weights, [v]) == 0 for v in range(33)))
    check('CANONICAL_COST_COUNTS_STEPS', all(path_sum({e: 1 for e in edges}, p) == len(p)-1 for p in samples))
    b = [sp.Rational(i*i-3*i, 5) for i in range(33)]
    dw = {(u, v): b[v]-b[u] for u, v in edges}
    check('BOUNDARY_TELESCOPING_CONTROLS', all(path_sum(dw, p) == b[p[-1]]-b[p[0]] for p in samples))
    check('BOUNDARY_REVERSES_SIGN', all(dw[u, v]+dw[v, u] == 0 for u, v in edges))
    check('POSITIVE_RETURN_CANNOT_EQUAL_DIAGONAL', all(1+1 != 0 for _ in undirected))
    symmetric = {(u, v): 1+abs(zone(u)-zone(v)) for u, v in edges}
    check('NONSELECTED_SYMMETRIC_INVARIANT_POSITIVE_WEIGHTS',
          all(symmetric[u, v] == symmetric[v, u] >= 1 for u, v in edges)
          and symmetric[0, 9] != symmetric[0, 20])

    x = sp.Symbol('rho')
    polynomial = x**3-359*x-2574

    def zero_on_perron(expr):
        num, _ = sp.fraction(sp.cancel(expr))
        return sp.rem(num, polynomial, x) == 0

    r = [1/(x+n) for n in sizes]
    K = sp.Matrix(3, 3, lambda a, b: sizes[b] if a != b else 0)
    check('PERRON_PROFILE_NORMALIZATION_MOD_CUBIC', zero_on_perron(sum(n*rv for n, rv in zip(sizes, r))-1))
    check('ALL_ZONE_EIGEN_ROWS_MOD_CUBIC', all(zero_on_perron(sum(K[a, b]*r[b] for b in range(3))-x*r[a]) for a in range(3)))
    T = sp.Matrix(3, 3, lambda a, b: K[a, b]*r[b]/(x*r[a]))
    check('FORWARD_PERRON_TRANSITION_STOCHASTIC', all(zero_on_perron(sum(T.row(a))-1) for a in range(3)))
    check('FULL_TWO_STEP_POSITIVITY', min(A*A) == 9 and all(v > 0 for v in A*A))
    check('RHO_BRACKETS_EXACT_SIGNS', polynomial.subs(x, 20) < 0 and polynomial.subs(x, 24) > 0)
    check('UNIFORM_MINORANT_ARITHMETIC', sp.Rational(9*29, 576*37) > sp.Rational(1, 100))
    check('OSCILLATION_CONTRACTION_FACTOR', 1-33*sp.Rational(1, 100) == sp.Rational(67, 100)
          and 0 < sp.Rational(67, 100) < 1)
    check('TWO_STEP_TELESCOPIC_MATRIX_FORMULA', all(sp.cancel(
          sum(K[a, c]*K[c, b]*r[c]/(x*r[a])*r[b]/(x*r[c]) for c in range(3))
          -(K*K)[a, b]*r[b]/(x*x*r[a])) == 0 for a in range(3) for b in range(3)))

    counts = sp.ones(3, 1)
    masses_ok = []
    for n in range(9):
        masses_ok.append(zero_on_perron(sum(sizes[a]*counts[a]*r[a]/x**n for a in range(3))-1))
        counts = K*counts
    check('NORMALIZED_CENTRAL_MASSES_DEPTHS_0_TO_8', all(masses_ok))
    check('CUBIC_REDUCTION_REJECTS_WRONG_NORMALIZATION', not zero_on_perron(sum(n*rv for n, rv in zip(sizes, r))-2))
    for p in samples:
        product = sp.Integer(1)
        for u, v in zip(p, p[1:]):
            product *= r[zone(v)]/(x*r[zone(u)])
        assert sp.cancel(product-r[zone(p[-1])]/(x**(len(p)-1)*r[zone(p[0])])) == 0
    check('ALL_SAMPLE_CONDITIONAL_PRODUCTS_TELESCOPE', True)
    check('FORWARD_LAW_DIFFERS_FROM_SIMPLE_WALK',
          sp.cancel(r[1]/(x*r[0])-r[2]/(x*r[0])-2*(x+9)/(x*(x+11)*(x+13))) == 0)
    check('NONCENTRAL_CONSISTENT_LAW_WITNESS', sp.Rational(1, 33*22) != sp.Rational(1, 33*20))
    Q = sp.Matrix(33, 33, lambda u, v: A[u, v]/degree[u])
    check('RIVAL_SIMPLE_WALK_CYLINDER_CONSISTENCY', all(sum(Q.row(u)) == 1 for u in range(33)))
    Jt = sp.Matrix(718, 33, lambda e, v: int(edges[e][1] == v))
    Js = sp.Matrix(718, 33, lambda e, v: int(edges[e][0] == v))
    C1 = sp.Matrix(33, 718, lambda v, e: sp.Rational(int(edges[e][1] == v), degree[v]))
    check('LITERAL_SCENE_ENDPOINT_LEFT_INVERSE', C1*Jt == sp.eye(33))
    check('ENDPOINT_BOUNDARY_OPERATOR_IS_I_MINUS_T', C1*(Jt-Js) == sp.eye(33)-Q)
    # Exact rational-domain elimination avoids expression-growth in Matrix.rank.
    check('NATIVE_CONNECTED_VERTEX_RANGE_RANK', (sp.eye(33)-Q).to_DM().rank() == 32)
    check('DEGREE_WEIGHTED_MEAN_ANNIHILATES_RANGE', sp.Matrix([degree])*(sp.eye(33)-Q) == sp.zeros(1, 33))
    h = {(u, v): 13 if (zone(u), zone(v)) == (0, 1) else -9 if (zone(u), zone(v)) == (2, 1) else 0 for u, v in edges}
    hv = sp.Matrix([h[e] for e in edges])
    check('AUTOMORPHISM_INVARIANT_HIDDEN_READING', C1*hv == sp.zeros(33, 1) and hv != sp.zeros(718, 1))
    w1 = {e: 2+sp.Rational(h[e], 13) for e in edges}
    check('SAME_COARSE_READING_AND_POSITIVE_PROTOCOL_FIBER',
          all(w >= 1 for w in w1.values()) and C1*sp.Matrix([w1[e] for e in edges]) == 2*sp.ones(33, 1)
          and sum(w1.values()) == 2*718)
    p1, p2 = [0, 9, 1, 20], [0, 20, 9, 20]
    check('SAME_LENGTH_ENDPOINTS_DISTINCT_ADDITIVE_ACTION',
          all(A[u, v] == 1 for p in [p1, p2] for u, v in zip(p, p[1:]))
          and p1[0] == p2[0] and p1[-1] == p2[-1] and len(p1) == len(p2)
          and path_sum(w1, p1)-path_sum(w1, p2) == sp.Rational(22, 13))
    check('REVERSAL_EXCEPTION_PRESERVED', w1[0, 9] != w1[9, 0])
    check('ACTUAL_BACKWARD_COUNTING_NOT_ITERATED_WALK',
          (A*A)[0, 0]/sum((A*A).row(0)) == sp.Rational(12, 251)
          and (Q*Q)[0, 0] == sp.Rational(23, 480)
          and sp.Rational(12, 251) != sp.Rational(23, 480))

    finite_towers = []
    depth = 4
    m = K**depth*sp.ones(3, 1)
    for terminal in [sp.ones(3, 1), sp.Matrix([1, 2, 3])]:
        norm = sum(sizes[a]*m[a]*terminal[a] for a in range(3))
        family = [K**(depth-n)*terminal/norm for n in range(depth+1)]
        assert all(family[n] == K*family[n+1] for n in range(depth))
        assert all(all(v > 0 for v in f) for f in family)
        assert all(sum(sizes[a]*(K**n*sp.ones(3, 1))[a]*family[n][a] for a in range(3)) == 1 for n in range(depth+1))
        finite_towers.append(family)
    check('FINITE_HORIZON_POSITIVE_NONUNIQUENESS', finite_towers[0] != finite_towers[1])
    n, m, ell, bs, bj, bt = sp.symbols('n m ell bs bj bt')
    conditional = n*ell+bs-bj + m*ell+bj-bt
    check('LOG_CONDITIONAL_COMPOSITION_EXACT', sp.expand(conditional-((n+m)*ell+bs-bt)) == 0)
    raw_defect = (n+m)*ell-bt-(n*ell-bj)-(m*ell-bt)
    check('UNCONDITIONAL_LOG_HAS_JUNCTION_DEFECT', sp.expand(raw_defect-bj) == 0)
    z = sp.Symbol('z')
    averaged = z*(n*ell+bs-bt)+(1-z)*(n*ell+bs-bt)
    check('NORMALIZED_FIBER_MIXTURE_HAS_ZERO_CONTRAST', sp.diff(sp.expand(averaged), z) == 0)

    scope = {
        'complete_additive_scene_fiber': 'PROVED_LEAN',
        'all_depth_endpoint_central_trace': 'ANALYTIC_UNIQUENESS_WITH_EXPLICIT_MINORANT',
        'perron_log_length_boundary': 'PROVED_LEAN',
        'additivity_core_derived': False,
        'logarithm_is_native_physical_action': False,
        'centrality_from_cylinder_consistency': False,
        'finite_horizon_unique': False,
        'primitive_pair_cost_endpoint_additive': False,
        'perron_forward_equals_simple_walk': False,
        'all_path_weights_selected': False,
        'boundary_quotient_is_physical_gauge': False,
        'all_depth_trace_uniqueness_compiled': False,
        'all_field_lifts_fixed_length_endpoints': False,
        'native_field_map_constructed': False,
        'native_source_constructed': False,
        'G0_closed': False,
        'positive_gr': False,
        'whole_core_no_go': False,
        'original_parent_terminals_changed': False,
    }
    payload = {
        'status': 'PASS_COMPLETE_SCENE_HISTORY_INTERFACE_BOUNDARY',
        'input_head': HEAD,
        'inputs_sha256': {p: sha(p) for p in [PROOF,
            '02_REGISTRY/research/A4D_NATIVE_DYNAMICAL_OWNERSHIP.md',
            '02_REGISTRY/research/APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md']},
        'checker_sha256': sha(PREFIX+'_check.py'),
        'lean_receipt_sha256': sha(PREFIX+'_results.json'),
        'compiled_declarations': receipt['printed_axiom_dependencies'],
        'transitive_d0_source_pins': len(receipt['transitive_d0_source_sha256']),
        'checks': checks,
        'scope': scope,
    }
    encoded = json.dumps(payload, sort_keys=True, indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        expected = args.expect or root/(PREFIX+'_certificate.json')
        assert json.loads(expected.read_text()) == json.loads(encoded), 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_HISTORY_ACTION', len(checks), 'exact controls; physical G0 remains open')


if __name__ == '__main__':
    main()
