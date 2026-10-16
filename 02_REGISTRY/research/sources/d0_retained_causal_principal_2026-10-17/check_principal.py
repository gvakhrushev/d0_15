#!/usr/bin/env python3
"""Exact causal principal response of the existing retained role records.

Only pinned creator/order definitions execute.  No old entrypoint, root,
spectrum, new gate, price, preparation law or detector admission is used.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
CREATORS = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    CREATORS: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md':
        'd7f8498e30e788af43edeb2bfd6e763d429e221cea76b622198687bbf4af21db',
    '02_REGISTRY/research/sources/d0_retained_history_causal_source_2026-10-16/check_retained_history.py':
        '6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
}
CHARS = ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))
LABELS = (16, 8, 24)


def creators(repo):
    tree = ast.parse((repo / CREATORS).read_text())
    nodes = [n for n in tree.body if
             (isinstance(n, ast.FunctionDef) and n.name == 'creator') or
             (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in n.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('causal_principal:creator_definition_nodes')
    namespace = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, 'exec'), namespace)
    return [namespace['creator'](r) for r in range(4)], namespace['EXTERIOR_ORDER']


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('causal_principal:' + name)
        checks.append(name)

    def eq(actual, expected, name):
        values = list(actual - expected) if isinstance(actual, s.MatrixBase) else [actual - expected]
        require(all(s.expand(v) == 0 for v in values), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    C, order = creators(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'actual_ACDB_order_all16')
    for i in range(4):
        for j in range(4):
            eq(C[i]*C[j].T+C[j].T*C[i], I if i == j else O,
               'full16_CAR_' + str(i) + str(j))

    def lift(matrix):
        return sum((matrix[i, j]*C[i]*C[j].T for i in range(4)
                    for j in range(4)), O.copy())

    # Independent first jets of all three cone fields: X[r,a]=d_r theta_a.
    X = s.Matrix(4, 3, s.symbols('X01 X02 X03 X11 X12 X13 X21 X22 X23 X31 X32 X33', real=True))
    B, time = X[1:4, :], X[0, :]
    eta = s.diag(1, -1, -1, -1)
    # Linearized g=s^2 O^T eta O has dg_0a=2s^2 d(theta_a).
    dg = [s.Matrix(4, 4, lambda i, j: 2*((X[r, j-1] if i == 0 and j > 0 else 0)
                     +(X[r, i-1] if j == 0 and i > 0 else 0))) for r in range(4)]
    connection = [s.Matrix(4, 4, lambda k, j: eta[k, k]
                     *(dg[r][k, j]+dg[j][k, r]-dg[k][r, j])/2) for r in range(4)]
    M = [-g.T for g in connection]
    expected = [s.zeros(4) for _ in range(4)]
    for a in range(3):
        expected[0][0, a+1] = 2*time[a]
        for b in range(3):
            expected[0][a+1, b+1] = B[a, b]-B[b, a]
            expected[a+1][0, b+1] = B[a, b]-B[b, a]
            expected[a+1][b+1, 0] = -B[a, b]-B[b, a]
    for r in range(4):
        eq(M[r], expected[r], 'actual_covector_LC_firstjet_' + str(r))
        eq(M[r][:, r], s.zeros(4, 1), 'creator_parallel_column_' + str(r))
    L = [C[r]*lift(M[r]) for r in range(4)]
    J = [l+l.T for l in L]
    eq(sum(L, O.copy()), O, 'torsionfree_Cartan_sum_zero')
    eq(sum(J, O.copy()), O, 'continuum_D_keeps_flat_positive_metric')
    for variable in X:
        generic = sum((l.diff(variable) for l in L), O.copy())
        eq(generic, O, 'Cartan_all_twelve_direction_' + str(variable))

    chi_J = [sum((chi[r]*J[r] for r in range(4)), O.copy()) for chi in CHARS]
    pair_list = ((0, 1), (0, 2), (1, 2))
    base = 2*sum(B[i, j]**2+B[j, i]**2 for i, j in pair_list)
    Q = [s.expand(s.trace(j*j)/16) for j in chi_J]
    exceptional_pairs = ((1, 2), (0, 2), (0, 1))
    for index, (i, j) in enumerate(exceptional_pairs):
        eq(Q[index], base-4*B[i, j]*B[j, i],
           'actual_role_character_quadratic_' + str(LABELS[index]))
    curl = sum((B[i, j]-B[j, i])**2 for i, j in pair_list)
    symmetric = sum((B[i, j]+B[j, i])**2 for i, j in pair_list)
    total = sum(Q)
    eq(total, 2*symmetric+4*curl, 'complete_diagonal_role_union_quadratic')
    eq(total, 8*sum(s.trace(l.T*l)/16 for l in L),
       'forward_instrument_firstjet_has_identical_exact_kernel')
    blind = {X[0, a]: s.Symbol('t'+str(a), real=True) for a in range(3)}
    blind.update({B[i, j]: 0 for i in range(3) for j in range(3) if i != j})
    for r in range(4):
        eq(L[r].subs(blind), O, 'forward_leading_smooth_jet_blind_' + str(r))
    # Positivity of 2(sym)^2+4(curl)^2 proves the converse without a rank scan.
    eq(sum((2*(B[i, j]+B[j, i])**2+4*(B[i, j]-B[j, i])**2
            for i, j in pair_list)), total, 'six_offdiagonal_gradient_coercivity_identity')

    q = s.Matrix(s.symbols('q1:4', real=True))
    v = s.Matrix(s.symbols('v1:4', real=True))
    fourier = {B[i, j]: q[i]*v[j] for i in range(3) for j in range(3)}
    symbol = s.hessian(total.subs(fourier), v)/2
    expected_symbol = s.Matrix(3, 3, lambda i, j:
        6*sum(q[k]**2 for k in range(3) if k != i) if i == j else -2*q[i]*q[j])
    eq(symbol, expected_symbol, 'full_three_cone_Fourier_symbol')
    det = 32*(6*sum(q[i]**4*q[j]**2 for i in range(3) for j in range(3) if i != j)
              +13*q[0]**2*q[1]**2*q[2]**2)
    eq(symbol.det(), det, 'generic_Fourier_determinant_all_real_signs')
    eq(symbol.subs({q[1]: 0, q[2]: 0}), s.diag(0, 6*q[0]**2, 6*q[0]**2),
       'single_axis_longitudinal_kernel')
    eq(symbol.subs({q[i]: 0 for i in range(3)}), s.zeros(3),
       'all_temporal_Fourier_modes_principal_blind')

    # Integrated EH principal density: determinant is fixed; the omitted
    # part of the Gamma-Gamma formula is an actual boundary divergence.
    eh_unit = s.trace(connection[0]*connection[0])-sum(
        s.trace(connection[r]*connection[r]) for r in range(1, 4))
    eq(eh_unit, -2*curl, 'EH_GammaGamma_principal_density_mod_divergence')
    longitudinal = {B[0, 1]: 1, B[1, 0]: 1}
    longitudinal.update({B[i, j]: 0 for i in range(3) for j in range(3)
                         if (i, j) not in ((0, 1), (1, 0))})
    eq(total.subs(longitudinal), 8, 'diagonal_history_reads_pure_longitudinal_gauge')
    eq(eh_unit.subs(longitudinal), 0, 'EH_longitudinal_gauge_zero')
    w1, w2, w3, k = s.symbols('w1 w2 w3 k', real=True)
    difference = s.Poly(s.expand(w1*Q[0]+w2*Q[1]+w3*Q[2]-k*curl), list(B))
    solution = s.solve(difference.coeffs(), (w1, w2, w3, k), dict=True)
    require(solution == [{w1: 0, w2: 0, w3: 0, k: 0}],
            'no_nonzero_constant_diagonal_character_weight_is_full_EH')

    # A coherent event on the SAME retained labels, rather than a new gate.
    label_v = s.Matrix([1, 1, 1])/s.sqrt(3)
    detector = label_v*label_v.T
    eq(detector*detector, detector, 'coherent_three_label_detector_is_projector')
    eq(s.trace(detector), 1, 'coherent_detector_trace_one')
    full_detector = s.diag(0, detector)
    eq(full_detector*s.Matrix([1, 0, 0, 0]), s.zeros(4, 1),
       'coherent_event_orthogonal_to_complete_blank_role')
    jv = sum(chi_J, O.copy())/s.sqrt(3)
    eq(sum(chi_J, O.copy()), 4*J[0], 'coherent_contrast_extracts_role_zero')
    eq(s.trace(J[0]*J[0]), 8*curl, 'full16_role_zero_exact_curl_norm')
    eq(s.trace(jv*jv)/16, s.Rational(8, 3)*curl,
       'coherent_detector_recovers_EH_principal_all_three_cones')
    weights = s.Matrix([sum(chi[r] for chi in CHARS)/s.sqrt(3) for r in range(4)])
    eq((weights.T*weights)[0]/4, 1, 'all_eight_shell_kinetic_baseline_preserved')
    eq((sum(Q)/3-s.trace(jv*jv)/16).subs(longitudinal), s.Rational(8, 3),
       'hostile_discarding_label_coherence_changes_readout')
    scale, survival = s.symbols('scale survival', positive=True)
    history = survival*s.Rational(8, 3)*curl/(256*scale**2)
    eh = -2*scale**2*curl
    eq(history, -survival*eh/(192*scale**4), 'owned_clock_coherent_EH_principal_coefficient')

    # Direct final-port amplitudes of the existing golden round, with
    # noncommuting small matrix blocks.  This verifies that Pv reads their
    # coherences rather than a relabelled diagonal probability mixture.
    a, p = s.symbols('a p', real=True)
    def golden(value):
        return s.rem(s.rem(s.expand(value), a*a-p, a), p*p+p-1, p)
    def golden_eq(actual, expected, name):
        require(all(golden(value) == 0 for value in actual-expected), name)
    A0 = s.Matrix([[1, 1], [1, 2]])/10
    Ms = [s.diag(1, 2)/10, s.Matrix([[0, 1], [1, 1]])/10,
          s.Matrix([[1, 2], [2, -1]])/20]
    require(A0*Ms[0] != Ms[0]*A0 and Ms[0]*Ms[1] != Ms[1]*Ms[0],
            'coherent_port_fixture_is_noncommuting')
    port0 = s.Matrix.vstack(*[-2*p*p*m.H*A0 for m in Ms])
    port1 = s.Matrix.vstack(*[-2*a*p*m.H*A0 for m in Ms])
    retained_projector = s.kronecker_product(detector, s.eye(2))
    actual_effect = port0.H*retained_projector*port0+port1.H*retained_projector*port1
    mv = sum(Ms, s.zeros(2))/s.sqrt(3)
    coherent_effect = 4*p*p*A0.H*mv*mv.H*A0
    golden_eq(actual_effect, coherent_effect, 'two_actual_golden_ports_coherent_final_history_effect')
    diagonal_effect = (port0.H*port0+port1.H*port1)/3
    require(any(golden(value) != 0 for value in actual_effect-diagonal_effect),
            'hostile_diagonal_port_mixture_is_different_event')
    pv_blank = s.Matrix.vstack(s.zeros(2), port0)
    embedded_detector = s.kronecker_product(s.diag(0, detector), s.eye(2))
    golden_eq(pv_blank.H*embedded_detector*pv_blank,
              port0.H*retained_projector*port0,
              'coherent_nonblank_event_embeds_without_blank_interference')

    # For a PSD detector, vanishing on each pure-gradient pair forces it
    # to kill this sum-zero plane.  Positivity, not a fitted selector,
    # makes the surviving detector unique up to a nonnegative scalar.
    blind_vectors = []
    for i, j in pair_list:
        z = s.Matrix([chi[i+1]-chi[j+1] for chi in CHARS])
        blind_vectors.append(z)
        eq((z.T*label_v)[0], 0, 'longitudinal_detector_vector_sum_zero_' + str(i)+str(j))
    A = s.Matrix.hstack(blind_vectors[0], blind_vectors[1], label_v)
    eq(A.det()**2, 48, 'two_longitudinal_vectors_span_detector_orthogonal_plane')
    for z in blind_vectors:
        eq(detector*z, s.zeros(3, 1), 'coherent_detector_annihilates_longitudinal_vector')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks, 'source_pins': PINS,
        'carrier': {'Fock': 16, 'reference': 128, 'occupied_momenta': 8,
                    'labels': 32, 'coefficient_qubit': 2, 'golden_ports': 2,
                    'round_history': '128^n; retained without reset'},
        'actual_role_labels': list(LABELS),
        'cone_jet': 'X_ra=partial_r theta_a; all12 real first derivatives retained',
        'diagonal_union_quadratic': 'sum_i<a [2(Bia+Bai)^2+4(Bia-Bai)^2]',
        'forward_leading_smooth_instrument_kernel': 'partial_0 theta_a and the three diagonal partial_a theta_a',
        'Fourier_symbol': [[str(symbol[i, j]) for j in range(3)] for i in range(3)],
        'Fourier_rank': '3 with >=2 nonzero spatial components; 2 on one spatial axis; 0 for zero spatial frequency; temporal frequency arbitrary',
        'EH_principal_density': '-2*s^2 sum_i<a(Bia-Bai)^2, modulo boundary divergence',
        'coherent_detector': '(|16>+|8>+|24>)(<16|+<8|+<24|)/3; coefficient0, both ports',
        'coherent_comparison': 'deltaL=-(1-exp(-beta/s^2))*I_EH_principal/(192*s^4)',
        'PSD_three_label_detector_classification': 'vanishing on all longitudinal pair gauges implies W=t*P_coherent, t>=0',
        'scope': {'old_entrypoints_or_roots_executed': False,
                  'new_gate_price_or_native_detector_selected': False,
                  'coherent_detector_compilation_or_physical_admission_proved': False,
                  'all10_metric_or_nonlinear_EH_identity': False,
                  'stationary_preparation_continuation_claimed': False,
                  'first_probability_derivative_invertibility_at_flat_claimed': False,
                  'leading_jet_blindness_promoted_to_finite_h_all_history': False,
                  'result_is_principal_quadratic_and_readout_source_comparison': True},
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
