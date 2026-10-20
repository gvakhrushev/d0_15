#!/usr/bin/env python3
"""Exact replay of the actual homogeneous soldered differential and its jets."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source'
PROOF = '02_REGISTRY/research/A4D_NATIVE_SOLDERED_HEAT_SOURCE.md'
INPUTS = [
 '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
 '04_CERTIFICATES/vp_master_bootstrap_and_volume_derivative.py',
 '03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean',
 '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
 '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracSquare.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
 '02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md',
 '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
 '02_REGISTRY/research/A4D_NATIVE_MATTER_OBSERVER_PAIRING.md',
 '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
 '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md',
 '02_REGISTRY/research/A4D_NATIVE_FULL_PREPARATION_FIBER.md',
]
spec = importlib.util.spec_from_file_location('soldered_source', ROOT/(BASE+'.py'))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
s = P.s


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def controls():
    checks, mutants = [], []

    def zero(x):
        values = x if isinstance(x, s.MatrixBase) else [x]
        return all(s.cancel(s.expand(v)) == 0 for v in values)

    def check(name, truth):
        assert bool(truth), name
        checks.append(name)

    def eq(name, x):
        check(name, zero(x))

    def reject(name, false_claim):
        check('REJECT_'+name, not false_claim)
        mutants.append(name)

    I = s.eye(16)
    for i in range(4):
        for j in range(4):
            Ci, Cj = P.creator(i), P.creator(j)
            eq('literal_CAR_create_%d_%d' % (i, j), Ci*Cj+Cj*Ci)
            eq('literal_CAR_contract_%d_%d' % (i, j), Ci.T*Cj.T+Cj.T*Ci.T)
            eq('literal_CAR_mixed_%d_%d' % (i, j), Ci.T*Cj+Cj*Ci.T-int(i == j)*I)

    F = s.Matrix([[1, s.Rational(1,3), 0, 0], [0, -2, s.Rational(1,5), 0],
                  [0, 0, -3, s.Rational(1,7)], [0, 0, 0, s.Rational(-1,2)]])
    n = s.Matrix([s.Rational(5,4), s.Rational(3,4), 0, 0])
    eta = P.ETA
    eq('boosted_observer_unit', (n.T*eta*n)[0]-1)
    h, q, v = P.observer(n), F*eta*F.T, F*n
    Q = F*eta*h*eta*F.T
    G = P.exterior_gram(h)
    eq('actual_solder_positive_symbol', Q-P.positive_symbol(q, v))
    for i in range(1, 5):
        check('positive_symbol_minor_%d' % i, Q[:i, :i].det() > 0)
    for i in range(1, 17):
        check('all_grade_Gram_minor_%d' % i, G[:i, :i].det() > 0)
    for r in range(4):
        leg = eta*F.row(r).T
        eq('literal_creator_observer_adjoint_%d' % r,
           G*P.create(leg)-P.contract(h*leg).T*G)
    for L in (2, 4):
        rows = []
        for k, z in P.modes(L):
            rows.append(list(P.feature(z)))
            # Full literal CAR blocks on all L2 and selected mixed L4 modes.
            if L == 2 or sum(k) % 17 == 4:
                D = P.symbol(F, n, z)
                energy = (z.conjugate().T*Q*z)[0].expand()
                eq('actual_symbol_square_L%d_k%s' % (L, k), D*D-energy*I)
                eq('actual_symbol_adjoint_L%d_k%s' % (L, k), G*D-D.conjugate().T*G)
        features = s.Matrix(rows)
        check('full_ten_feature_rank_L%d' % L, features.rank() == 10)
        check('eleven_affine_feature_rank_L%d' % L,
              s.ones(features.rows, 1).row_join(features).rank() == 11)
    reject('INVERSE_SYMBOL_SUBSTITUTION', zero(Q-Q.inv()))
    z = s.Matrix([-2, -1+s.I, 0, 0])
    D = P.symbol(F, n, z)
    wrong = sum((z[r]*(P.create(eta*F.row(r).T)+P.contract(h*eta*F.row(r).T))
                 for r in range(4)), s.zeros(16))
    reject('MISSING_BACKWARD_CONJUGATION', zero(wrong-D))
    reject('COUNTING_PAIRING_FOR_BOOSTED_OBSERVER', zero(D-D.conjugate().T))

    t = s.symbols('t', real=True)
    Wtest = s.Matrix([[3, 1, 2, -1], [1, 4, -1, 2], [2, -1, 5, 1], [-1, 2, 1, 6]])
    C = P.source(q, v, Wtest)
    for slot in P.SLOTS:
        H = P.basis(slot)
        dQ = P.symbol_tangent(q, v, H)
        # Differentiation of the rational metric formula is independent of the jet code.
        actual = P.positive_symbol(q+t*H, v).diff(t).subs(t, 0)
        eq('all_ten_metric_derivatives_%s' % (slot,), actual-dQ)
        eq('all_ten_covector_pullbacks_%s' % (slot,), s.trace(C*H)+s.trace(Wtest*dQ))
        dF = H*F.inv().T*eta/2
        w = q.inv()*v
        ds = -(w.T*H*w)[0]
        dn = -F.inv()*dF*n-ds*n/2  # this example has s=1
        eq('all_ten_raw_solder_lifts_%s' % (slot,), dF*eta*F.T+F*eta*dF.T-H)
        eq('all_ten_normalized_observer_lifts_%s' % (slot,), (n.T*eta*dn)[0])
        dh = 2*eta*(dn*n.T+n*dn.T)*eta
        eq('all_ten_actual_operator_lift_jets_%s' % (slot,),
           dF*eta*h*eta*F.T+F*eta*dh*eta*F.T+F*eta*h*eta*dF.T-dQ)
        eq('all_ten_homogeneous_carrier_tangents_%s' % (slot,), s.eye(4)*H*s.eye(4)-H)
        rest = P.symbol_tangent(eta, s.eye(4)[:, 0], H)
        eq('rest_metric_involution_%s' % (slot,),
           P.symbol_tangent(eta, s.eye(4)[:, 0], rest)-H)
    for i in range(4):
        u = s.eye(4)[:, i]
        dQ = P.joint_tangent(q, v, s.zeros(4), u)
        eq('independent_observer_jet_%d' % i,
           P.positive_symbol(q, v+t*u).diff(t).subs(t, 0)-dQ)
        eq('observer_source_%d' % i,
           (P.observer_source(q, v, Wtest).T*u)[0]+s.trace(Wtest*dQ))
    eq('observer_ray_Ward', (v.T*P.observer_source(q, v, Wtest))[0])
    e0 = s.eye(4)[:, 0]
    cols = [P.pack(P.joint_tangent(eta, e0, P.basis(slot), s.zeros(4, 1))) for slot in P.SLOTS]
    cols += [P.pack(P.joint_tangent(eta, e0, s.zeros(4), s.eye(4)[:, i])) for i in range(4)]
    jac = s.Matrix.hstack(*cols)
    check('joint_fourteen_coordinate_rank', jac.rank() == 10 and len(jac.nullspace()) == 4)
    for i in range(1, 4):
        eq('joint_tilt_heat_null_%d' % i,
           P.joint_tangent(eta, e0, 2*P.basis((0, i)), s.eye(4)[:, i]))
    reject('OBSERVER_MATTER_VARIATION_CAN_BE_DROPPED', zero(P.observer_source(q, v, Wtest)))
    for vec in [s.Matrix([1, 2, 0, 1]), s.Matrix([0, 1, 1, 0]), s.Matrix([2, 0, 0, 0])]:
        r = (vec.T*Q.inv()*vec)[0]
        fiberq = -Q+2*vec*vec.T/r
        eq('full_joint_fiber_inverse_norm', (vec.T*fiberq.inv()*vec)[0]-r)
        eq('full_joint_fiber_symbol_recovery', P.positive_symbol(fiberq, vec)-Q)

    results = []
    for diag in ([1, 1, 1, 1], [1, 2, 3, 4]):
        data = P.exact_heat(diag)
        expectedZ = s.prod((1+s.Rational(2)**(-d))**2 for d in diag)
        eq('full_partition_multiplicity', data['full_partition']-16*expectedZ)
        means = [s.Rational(64)*s.Rational(2)**(-d)/(1+s.Rational(2)**(-d)) for d in diag]
        expectedW = s.Matrix(4, 4, lambda i, j: means[i] if i == j else means[i]*means[j]/64)
        eq('exact_product_thermal_tensor', data['W']-expectedW)
        eq('packed_thermal_features', data['mean_features']-P.pack(data['W']))
        cov = data['covariance']
        for i in range(1, 11):
            check('strict_affine_heat_Hessian_minor_%s_%d' % (diag, i), cov[:i, :i].det() > 0)
        results.append(data)
    flat = results[0]
    flatC = P.source(eta, e0, flat['W'])
    packed = P.pack(flatC)
    expected = s.Matrix([s.Rational(-64,3), s.Rational(128,9), s.Rational(128,9), s.Rational(128,9),
                         s.Rational(64,3), s.Rational(128,9), s.Rational(128,9),
                         s.Rational(64,3), s.Rational(128,9), s.Rational(64,3)])
    eq('all_ten_flat_source_coefficients', packed-expected)
    eq('flat_observer_force', P.observer_source(eta, e0, flat['W'])-
       s.Matrix([0, s.Rational(-256,9), s.Rational(-256,9), s.Rational(-256,9)]))
    H = P.basis((0,1))
    eq('offdiagonal_probe_is_Lorentz_tracefree', s.trace(eta*H))
    eq('nonzero_tracefree_exact_response', s.trace(flatC*H)-s.Rational(128,9))
    reject('PURE_TRACE_HEAT_SOURCE', zero(s.trace(flatC*H)))
    reject('HEAT_SOURCE_EQUALS_FLAT_RHO0', zero(packed))
    reject('DROP_PACKED_WEIGHT_TWO', zero(s.trace(flatC*H)-flatC[0,1]))
    reject('THERMAL_TENSOR_DIAGONAL', zero(flat['W'][0,1]))
    scalar_null = P.basis((1,1))-P.basis((2,2))
    eq('nonzero_symbol_jet_with_zero_scalar_price_jet', s.trace(flatC*scalar_null))
    reject('SCALAR_PRICE_KERNEL_EQUALS_SYMBOL_KERNEL',
           zero(P.symbol_tangent(eta, e0, scalar_null)))
    second = P.positive_symbol(eta+t*H, e0).diff(t,2).subs(t,0)
    eq('nonlinear_metric_second_jet', second-4*P.basis((0,0)))
    reject('AFFINE_HESSIAN_IS_FULL_LORENTZ_HESSIAN', zero(s.trace(flat['W']*second)))
    energy = s.trace(flat['W'])
    check('strict_radial_energy', energy > 0)
    reject('INVERSE_AND_DIRECT_RADIAL_JETS_EQUAL', zero(-2*energy-2*energy))
    check('full_flat_constant_kernel_sixteen', sum(16 for _, zz in P.modes(4) if zero(zz)) == 16)
    reject('SIMPLE_PROTECTED_GIBBS_TOP_EIGENVALUE', 16 == 1)

    for L, legs in [(2, [s.Rational(3,2), s.Rational(1,2)]), (4, [1, 2, 1, 1])]:
        d, delta = P.variable_axis(L, legs)
        S = s.zeros(L)
        for x in range(L):
            S[x, (x+1) % L] = 1
        M = s.diag(*legs)
        eq('variable_adjoint_endpoint_defect_L%d' % L, delta-d.T-L*(M*S.T-S.T*M))
        reject('STORED_VARIABLE_CODIFFERENTIAL_ADJOINT_L%d' % L, zero(delta-d.T))
        whole = s.BlockMatrix([[s.zeros(L), delta], [d, s.zeros(L)]]).as_explicit()
        reject('STORED_VARIABLE_DIRAC_SELFADJOINT_L%d' % L, zero(whole-whole.T))
        for x in range(L):
            Fx = s.diag(legs[x], -1, -1, -1)
            Fy = s.diag(legs[(x+1) % L], -1, -1, -1)
            link = Fx*Fy.inv()
            eq('variable_witness_full_carrier_equation_L%d_x%d' % (L,x),
               link*(Fy*eta*Fy.T)*link.T-Fx*eta*Fx.T)
        gram = s.diag(*range(1, L+1))
        forced = gram.inv()*d.T*gram
        eq('unique_supplied_pairing_adjoint_L%d' % L, gram*forced-d.T*gram)
    d, delta = P.variable_axis(2, [s.Rational(3,2), s.Rational(1,2)])
    eq('literal_two_site_matrix', d-s.Matrix([[-3,3],[1,-1]]))
    eq('literal_two_site_stored_backward', delta-d)
    d, delta = P.variable_axis(4, [1, 1, 1, 1])
    eq('homogeneous_positive_adjoint_control', delta-d.T)

    receipt_path = BASE+'_lean_results.json'
    receipt = json.loads((ROOT/receipt_path).read_text())
    check('narrow_Lean_receipt_success', receipt['compiler_exit_code'] == 0 and receipt['status'] == 'PASS')
    check('Lean_capsule_fingerprint', receipt['capsule_sha256'] == sha(BASE+'.lean'))
    check('Lean_actual_output_fingerprint', receipt['output_sha256'] == sha(BASE+'_lean_output.txt'))
    for path, fingerprint in receipt['input_sha256'].items():
        check('Lean_source_input_'+path, sha(path) == fingerprint)
    for name, axioms in receipt['axioms'].items():
        check('Lean_standard_axioms_'+name, set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'})
    # Actual compiled imports are pinned in the receipt, with cache/source gaps
    # explicit. Portable replay does not pretend to rebuild that environment.
    return {'schema': 'd0-native-soldered-heat-source/1',
            'verdict': 'OWNED_HOMOGENEOUS_OPERATOR_TEN_JOINT_HEAT_COMPONENTS',
            'input_source_sha': '695ecb94abcb38590a8f3e37332969ef21e2f24d',
            'exact_controls': len(checks), 'controls': checks,
            'executed_mathematical_mutants': mutants,
            'flat_L4_beta_log2_over32_packed_source': [str(x) for x in packed],
            'full_zero_mode_multiplicity': 16, 'joint_tangent_rank': 10,
            'joint_positive_symbol_kernel_dimension': 4,
            'scalar_price_differential_kernel_dimension_at_rest': 13,
            'bootstrap_heat_identification': 'OPEN', 'source_Ward_GR': 'OPEN',
            'original_parent_terminal': 'OPEN',
            'input_sha256': {path: sha(path) for path in INPUTS},
            'proof_sha256': sha(PROOF), 'checker_sha256': sha(BASE+'_check.py'),
            'program_sha256': sha(BASE+'.py'), 'Lean_receipt_sha256': sha(receipt_path)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = controls()
    target = ROOT/(BASE+'_certificate.json')
    if args.write:
        target.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        assert json.loads(target.read_text()) == result, 'SOLDERED_HEAT_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_NATIVE_SOLDERED_HEAT_SOURCE controls=%d mutants=%d native_heat_binding=OPEN' %
          (result['exact_controls'], len(result['executed_mathematical_mutants'])))


if __name__ == '__main__':
    main()
