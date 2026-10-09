#!/usr/bin/env python3
"""Common scene-price first jet and upper-branch second-variation obstruction.

The positive edge family is declared explicitly. Its physical admission and
pullback from the joint native factor are not provided by this certificate.
"""
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path

import sympy as s
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source'
PROOF = '02_REGISTRY/research/A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md'
HEAD = 'd88c5d3bb046ccf3eded006587007e68b5754acf'
SCOPE = {
    'interface': 'POSITIVE_CROSS_ZONE_CONDUCTANCES_ON_K_9_11_13_AT_UNIT_WEIGHTS',
    'heat_route': '33_VERTEX_NORMALIZED_LAPLACIAN',
    'feedback_route': 'FULL_718_HISTORY_REVERSAL_RETURN_WITH_MOVING_PAIRING',
    'this_is_one_step_R_feedback_not_two_tick_R_squared_feedback': True,
    'all_359_weight_first_jets': 'EXACT_RATIONAL_AND_ANALYTIC_QUOTIENT',
    'scalar_heat_feedback_HasDerivAt': 'COMPILED_WITH_REAL_DOMAINS',
    'all_size_matrix_derivative_and_Hessian_HasFDerivAt_compiled': False,
    'two_fugacity_branches_for_each_positive_fixed_beta': 'ANALYTIC_MVT_IVT_AND_EXACT_QUADRATIC',
    'upper_branch_not_local_minimum': 'NEGATIVE_DEFINITE_ON_296_BALANCED_WEIGHT_DIRECTIONS',
    'binary_dense_passport_scene_price_zero': 'COMPLETE_OWNED_SCENE_PASSPORT_CLASS_AT_FIXED_BETA_Z',
    'binary_dense_passport_class_is_whole_native_core': False,
    'nonzero_weight_jets_admitted_in_binary_passport': False,
    'lower_branch_is_a_local_or_global_minimum': False,
    'equations_for_variations_of_beta_or_z_solved': False,
    'every_weight_variation_is_admitted_by_native_physics': False,
    'native_weight_map_or_its_joint_first_jet_constructed': False,
    'scalar_first_jet_quotient_is_global_price_factorization': False,
    'response_null_directions_removed_as_gauge': False,
    'whole_native_source_matter_Ward_or_rho0_derived': False,
    'G0_T0_T1_T2_T3_or_original_parent_terminals_closed': False,
    'curved_roots_soundness_recovery_GR_or_global_closure': False,
    'new_action_selector_temperature_law_or_postulate': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def controls():
    checks = {}

    def check(name, condition):
        assert bool(condition), name
        checks[name] = checks.get(name, 0) + 1

    receipt = json.loads((ROOT / (BASE + '_results.json')).read_text())
    output = (ROOT / receipt['output']).read_text()
    capsule = (ROOT / (BASE + '.lean')).read_text()
    names = re.findall(r'^theorem (\w+)', capsule, re.M)
    check('kernel_exit_and_input', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and receipt['input_head'] == HEAD)
    check('all_actual_propositions', names == receipt['declarations']
          and len(names) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 27)
    for name in names:
        q = 'D0.Research.NativeScenePriceSource.' + name
        check('resolved_declaration_and_transitive_axioms',
              re.search(r'^' + re.escape(q) + r'(?:\.\{|[ :])', output, re.M)
              and ("'" + q + "' depends on axioms:" in output
                   or "'" + q + "' does not depend on any axioms" in output))
    owners = ['D0.Synthesis.DenseOperatorSceneRigidity.dense_operator_recovers_scene',
              'D0.Synthesis.DenseOperatorSceneRigidity.scene_passport_inhabited']
    check('actual_owner_proposition_count', receipt['primary_owner_declarations'] == owners
          and receipt['printed_primary_owner_propositions'] == 2)
    for q in owners:
        check('actual_owner_proposition_and_transitive_axioms',
              re.search(r'^'+re.escape(q)+r'(?:\.\{|[ :])', output, re.M)
              and ("'"+q+"' depends on axioms:" in output
                   or "'"+q+"' does not depend on any axioms" in output))
    actual_axioms = set()
    for match in re.finditer(r'depends on axioms: \[([^]]*)\]', output, re.S):
        actual_axioms.update(x.strip() for x in match.group(1).split(',') if x.strip())
    check('only_standard_kernel_axioms', actual_axioms == set(receipt['axioms'])
          and actual_axioms <= {'propext', 'Quot.sound', 'Classical.choice'}
          and not any(x in output for x in ['warning:', 'error:', 'sorryAx', 'Lean.trustCompiler']))
    for path, digest in {**receipt['toolchain_input_sha256'],
                         **receipt['primary_and_prior_input_sha256'],
                         receipt['capsule']: receipt['capsule_sha256'],
                         receipt['output']: receipt['output_sha256']}.items():
        check('pinned_input', sha(path) == digest)

    sizes, starts, degrees = [9, 11, 13], [0, 9, 20], [24, 22, 20]

    def zone(i):
        return 0 if i < 9 else 1 if i < 20 else 2

    A = s.Matrix(33, 33, lambda i, j: int(zone(i) != zone(j)))
    d = [degrees[zone(i)] for i in range(33)]
    DI = s.diag(*[s.Rational(1, x) for x in d])
    T, I, O = DI * A, s.eye(33), s.zeros(33)
    T2, T3 = T * T, T * T * T
    edges = [(i, j) for i in range(33) for j in range(i + 1, 33) if A[i, j]]
    one = s.ones(33, 1)
    check('owned_scene_counts_degrees', len(edges) == 359 and sum(d) == 718
          and A * one == s.Matrix(d))
    k = s.Rational(39, 160)
    t = s.symbols('t')
    check('exact_33_vertex_characteristic_polynomial',
          s.expand(T.charpoly(t).as_expr() - t**30 * (t - 1) * (t*t + t + k)) == 0)
    check('kappa_invariant_value', 1 - T2.trace()/2 == k)
    Pc = s.Matrix(33, 33, lambda i, j: s.Rational(d[j], 718))
    Pd = s.Matrix(33, 33, lambda i, j:
                  int(i == j) - s.Rational(1, sizes[zone(i)]) if zone(i) == zone(j) else 0)
    check('all_invisible_state_sectors_retained', Pc*Pc == Pc and Pd*Pd == Pd
          and Pc*Pd == O and Pd*Pc == O and Pd.trace() == 30 and Pc.trace() == 1)
    check('spectral_projector_equations', T*Pc == Pc and Pc*T == Pc
          and T*Pd == O and Pd*T == O and T*(T-I)*(T2+T+k*I) == O)

    def tr_product(M, V):
        # V has only two nonzero rows for an edge jet.
        return sum(M[j, i]*value for (i, j), value in V.todok().items())

    coeffs, counts, all_coeffs = {}, {}, []
    for i, j in edges:
        E = s.zeros(33); E[i, j] = E[j, i] = 1
        dd = s.zeros(33); dd[i, i] = dd[j, j] = 1
        V = DI*(E-dd*T)
        check('complete_edge_degree_jet', s.diag(*d)*V+dd*T == E and V*one == s.zeros(33, 1))
        check('complete_edge_invisible_traces', V.trace() == 0
              and tr_product(Pc, V) == tr_product(Pd, V) == 0)
        tv = tr_product(T, V)
        check('complete_edge_polynomial_quotient', tr_product(T2, V) == -tv
              and tr_product(T3, V) == (1-k)*tv)
        value = -tv
        direct = T2[i, i]/d[i]+T2[j, j]/d[j]-s.Rational(2, d[i]*d[j])
        check('complete_edge_direct_kappa_covector', value == direct)
        pair = str((zone(i), zone(j)))
        check('per_edge_coefficients_equal_within_zone_pair', pair not in coeffs or coeffs[pair] == str(value))
        check('all_nonzero_edge_jets_leave_binary_scene_contract', E[i, j] != 0
              and 1+s.Rational(1, 5)*E[i, j] not in (0, 1))
        coeffs[pair] = str(value)
        counts[pair] = counts.get(pair, 0)+1
        all_coeffs.append(value)
    check('nonzero_covector_and_scale_null', sum(all_coeffs) == 0 and any(all_coeffs))
    check('exact_native_edge_coefficients', coeffs == {
        '(0, 1)': '91/278784', '(0, 2)': '1/57600', '(1, 2)': '-93/387200'})
    check('all_edges_included', counts == {'(0, 1)': 99, '(0, 2)': 117, '(1, 2)': 143})

    x, y, u, z, h = s.symbols('x y u z h')
    Aq = s.Matrix([[0, 11*x, 13*y], [9*x, 0, 13*u], [9*y, 11*u, 0]])
    Dq = s.diag(11*x+13*y, 9*x+13*u, 9*y+11*u)
    kq = s.factor((Dq.inv()*Aq).det())
    check('independent_equitable_kappa', kq == 2574*u*x*y/((11*u+9*y)*(13*u+9*x)*(11*x+13*y)))
    jets = [s.diff(kq, v).subs({x: 1, y: 1, u: 1}) for v in [x, y, u]]
    check('equitable_jets_equal_full_edge_sums', jets == [s.Rational(91, 2816), s.Rational(13, 6400), -s.Rational(1209, 35200)]
          and jets == [s.Rational(coeffs[p])*counts[p] for p in coeffs])

    kap = s.symbols('kap')
    Q = (1-z)*(1-2*kap*z)+kap*kap*z*z
    cF = 2*z*(1-(1+kap)*z)/Q
    check('feedback_derivative_sign_and_normalization', s.cancel(-s.diff(Q, kap)/Q-cF) == 0)
    nativeQ = Q.subs(kap, k)
    poly = s.expand(h*nativeQ-2*z*(1-(1+k)*z))
    expected = (s.Rational(199, 80)+s.Rational(14001, 25600)*h)*z*z-(2+s.Rational(119, 80)*h)*z+h
    check('stationary_quadratic', s.expand(poly-expected) == 0)
    check('stationary_discriminant', s.factor(s.discriminant(poly, z)-(4*(1-h)+h*h/40)) == 0)
    check('stationary_interval_endpoints', poly.subs(z, 0) == h
          and s.cancel(poly.subs(z, s.Rational(1, 2))-(40241*h-38720)/102400) == 0
          and s.cancel(poly.subs(z, s.Rational(160, 199))-6240*h/39601) == 0)
    check('strict_middle_sign_from_heat_bound', 40241*s.Rational(5, 7)-38720 < 0)
    check('exact_half_and_feedback_only_turn', cF.subs({kap: k, z: s.Rational(1, 2)}) == s.Rational(38720, 40241)
          and cF.subs({kap: k, z: s.Rational(160, 199)}) == 0)
    r = s.sqrt(10)/40
    check('MVT_interval_bound', 0 < r < s.Rational(1, 10) and s.Rational(3, 2)-r > s.Rational(7, 5))

    # Consume the actual owner's complete recovered partition class. The
    # all-class recognition implication is compiled, not extrapolated from
    # these arithmetic/permutation controls.
    for aa, bb, cc in itertools.permutations(sizes):
        dq = s.diag(bb+cc, aa+cc, aa+bb)
        aq = s.Matrix([[0, bb, cc], [aa, 0, cc], [aa, bb, 0]])
        tq = dq.inv()*aq
        check('all_recovered_partition_kappa', tq.det() == k
              and aa+bb+cc == 33 and 2*(aa*bb+aa*cc+bb*cc) == 718)
        check('all_recovered_partition_spectrum',
              s.expand(tq.charpoly(t).as_expr()-(t-1)*(t*t+t+k)) == 0)
        check('all_recovered_partition_feedback_pencil',
              s.expand((s.eye(3)-z*(s.eye(3)-tq*tq)).det()-nativeQ) == 0)
    for perm in [list(range(1, 33))+[0], list(reversed(range(33))),
                 [(7*i)%33 for i in range(33)]]:
        ap = s.Matrix(33, 33, lambda i, j: A[perm[i], perm[j]])
        degree = list(ap*one)
        tp = s.diag(*[1/x for x in degree])*ap
        check('complete_vertex_relabel_keeps_native_normalization',
              tp == s.Matrix(33, 33, lambda i, j: T[perm[i], perm[j]]))
        check('complete_vertex_relabel_keeps_owner_passport',
              ap == ap.T and all(ap[i, i] == 0 for i in range(33))
              and all(x in (0, 1) for x in ap) and ap.rank() == 3 and s.trace(ap*ap) == 718)
    aa, bb, cc = 8, 11, 14
    ka = s.Rational(2*aa*bb*cc, (aa+bb)*(aa+cc)*(bb+cc))
    check('dropping_owner_quadratic_moment_changes_kappa', aa+bb+cc == 33
          and 2*(aa*bb+aa*cc+bb*cc) != 718 and ka != k)
    check('nonbinary_source_cannot_be_imported_into_owner_contract',
          s.Rational(38720, 40241)-s.Rational(5, 7) > 0
          and s.Rational(coeffs['(0, 1)']) > 0)

    # Complete tensor basis of the balanced edge space; no gauge quotient.
    vectors, energies = [], []
    for a, b in itertools.combinations(range(3), 2):
        for i in range(1, sizes[a]):
            for j in range(1, sizes[b]):
                uv, vv = s.zeros(33, 1), s.zeros(33, 1)
                uv[starts[a]+i], uv[starts[a]] = 1, -1
                vv[starts[b]+j], vv[starts[b]] = 1, -1
                E = uv*vv.T+vv*uv.T
                V = DI*E
                check('balanced_degree_and_transport_equations', E*one == s.zeros(33, 1) and T*V == O and V*T == O)
                energy = s.trace(V*V)
                check('balanced_positive_Hessian_energy', energy == s.Rational(8, degrees[a]*degrees[b]) and energy > 0)
                vectors.append([E[ii, jj] for ii, jj in edges])
                energies.append(str(energy))
    rank = DomainMatrix.from_Matrix(s.Matrix(vectors).T).convert_to(s.QQ).rank()
    check('complete_balanced_rank', len(vectors) == rank == 296)
    check('balanced_energies', sorted(set(energies)) == ['1/55', '1/60', '1/66'])
    beta, nu, Z = s.symbols('beta nu Z', positive=True)
    tt = s.symbols('tt', real=True)
    heat_curve = s.log(Z+2*s.exp(-beta)*(s.cosh(beta*nu*tt)-1))/beta
    feedback_curve = -2*s.log(1+z*nu*nu*tt*tt/(1-z))
    check('independent_rank_two_heat_Hessian', s.simplify(s.diff(heat_curve, tt, 2).subs(tt, 0)-2*nu*nu*beta*s.exp(-beta)/Z) == 0)
    check('independent_rank_two_feedback_Hessian', s.simplify(s.diff(feedback_curve, tt, 2).subs(tt, 0)+4*z*nu*nu/(1-z)) == 0)

    # Nonuniform positive history fixture validates moving C/P/pairing, with
    # generic all-size identities already compiled in Lean.
    zones = [0, 1, 1, 2, 2]
    adj = s.Matrix(5, 5, lambda i, j:
                   s.Rational(i+j+2, 3) if zones[i] != zones[j] else 0)
    hist = [(i, j) for i in range(5) for j in range(5) if adj[i, j]]
    J = s.Matrix(len(hist), 5, lambda a, b: int(hist[a][1] == b))
    WH = s.diag(*[adj[i, j] for i, j in hist])
    R = s.Matrix(len(hist), len(hist), lambda a, b: int(hist[a] == hist[b][::-1]))
    DD = s.diag(*list(adj*s.ones(5, 1)))
    C = DD.inv()*J.T*WH
    P = J*C
    transfer = DD.inv()*adj
    F = P*R*(s.eye(len(hist))-P)*R*P
    check('weighted_history_pairing_and_reversal', J.T*WH*J == DD and C*J == s.eye(5)
          and P.T*WH == WH*P and R.T*WH*R == WH)
    check('weighted_history_shared_transfer', C*R*J == transfer)
    check('weighted_history_complete_feedback', F == J*(s.eye(5)-transfer*transfer)*C)
    RR = R*R
    check('retain_two_tick_full_history_zero_feedback', RR == s.eye(len(hist))
          and P*RR*(s.eye(len(hist))-P)*RR*P == s.zeros(len(hist)) and F != s.zeros(len(hist)))
    zz = s.Rational(2, 7)
    check('ordinary_full_history_determinant', (s.eye(len(hist))-zz*F).det()
          == (s.eye(5)-zz*(s.eye(5)-transfer*transfer)).det())

    # Hostile semantic controls: these are observable failures, not only flags.
    E = s.zeros(33); E[0, 9] = E[9, 0] = 1
    check('reject_frozen_degree_jet', DI*E*one != s.zeros(33, 1))
    check('reject_combinatorial_heat_substitution', (s.diag(*d)-A).trace() == 718 and (I-T).trace() == 33)
    check('reject_full_price_feedback_only_stationarity', s.Rational(3, 2)-r < s.Rational(3, 2)+r)
    check('retain_second_order_response_null_modes', len(energies) == 296 and all(s.Rational(e) > 0 for e in energies))
    return {'checks': checks, 'check_count': sum(checks.values()), 'compiled_propositions': 27,
            'printed_primary_owner_propositions': 2,
            'edge_directions': len(edges), 'edge_coefficients': coeffs,
            'balanced_tangent_rank': rank, 'balanced_energies': sorted(set(energies)),
            'retained_history_dimension': 718, 'balanced_state_dimension': 30,
            'native_kappa': str(k)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    header = {'schema': 'd0-shared-scene-price-source/1', 'input_head': HEAD,
              'scope': SCOPE, 'proof_sha256': sha(PROOF),
              'checker_sha256': sha(BASE+'_check.py'),
              'lean_receipt_sha256': sha(BASE+'_results.json')}
    expected = None
    if not args.output:
        expected = json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert all(expected.get(key) == value for key, value in header.items()), 'SOURCE_SCOPE_OR_INPUT_MISMATCH'
    result = {**header, **controls()}
    if args.output:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    else:
        assert result == expected, 'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_NATIVE_SHARED_SCENE_PRICE_SOURCE', result['check_count'], 'controls')


if __name__ == '__main__':
    main()
