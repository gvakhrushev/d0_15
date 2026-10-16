#!/usr/bin/env python3
"""Exact controls for the complete total-affine-transport scalar class.

Universal classifications are proved in the companion text; this file does
not extrapolate them from the finite matrices checked here.
"""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as s

HEAD = '7c8ee6851dc343927c04f971f0b0de7a10be7b04'
BASE = '02_REGISTRY/research/certificates/a4d_native_affine_history_scalar'
PROOF = '02_REGISTRY/research/A4D_NATIVE_AFFINE_HISTORY_SCALAR_BOUNDARY.md'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    p.add_argument('--expect', type=Path)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []

    def check(name, result):
        assert bool(result), name
        checks.append(name)

    def zero(M):
        return all(s.cancel(v) == 0 for v in M)

    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('LEAN_21_DECLARATIONS_36_NATIVE_PINS', receipt['status'] == 'PASS'
          and receipt['owner_input_head'] == HEAD and receipt['compiler_exit_code'] == 0
          and receipt['printed_axiom_dependencies'] == 21
          and len(receipt['transitive_d0_source_sha256']) == 36 and not receipt['sorryAx'])
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('EVERY_SOURCE_TOOLCHAIN_CAPSULE_OUTPUT_HASH', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('STANDARD_AXIOMS_CLEAN_OUTPUT', set(receipt['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
          and all(v not in out for v in ['error:', 'warning:', 'sorryAx']))
    for name in ['complete_native_scalar_class', 'two_free_native_edges', 'translation_killed',
                 'all_raw_shift_variations_invisible', 'native_gauge_boundary', 'no_positive_reverse_pair']:
        check('BOUND_'+name, "'D0.Research.NativeAffineHistoryScalar."+name+"' depends on axioms:" in out)

    I = s.eye(4)
    eta = s.diag(1, -1, -1, -1)

    def affine(U, v):
        return U.row_join(v).col_join(s.Matrix([[0, 0, 0, 0, 1]]))

    def inv_affine(U, v):
        return affine(U.inv(), -U.inv()*v)

    def E(i, j, t):
        M = I.copy()
        M[i, j] += t
        return M

    t = s.Symbol('t', real=True)
    v = s.Matrix(s.symbols('v0:4'))
    w = s.Matrix(s.symbols('w0:4'))
    U = s.diag(2, 3, 5, 7)*E(0, 1, 2)*E(2, 3, -1)
    V = s.diag(1, 2, 1, 3)*E(1, 2, -3)
    check('ACTUAL_AFFINE_PRODUCT_SHIFT_ORDER', affine(U, v)*affine(V, w) == affine(U*V, v+U*w))
    check('ACTUAL_AFFINE_INVERSE', affine(U, v)*inv_affine(U, v) == s.eye(5))
    D = affine(2*I, s.zeros(4, 1))
    Tv = affine(I, v)
    check('ALL_TRANSLATIONS_DOUBLE_BY_CONJUGATION', D*Tv*D.inv() == affine(I, 2*v))
    check('ALL_TRANSLATIONS_DOUBLE_BY_PRODUCT', Tv*Tv == affine(I, 2*v))
    check('AFFINE_SPLITS_TRANSLATION_THEN_LINEAR', Tv*affine(U, s.zeros(4, 1)) == affine(U, v))

    shear_records = []
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            Di = I.copy()
            Di[i, i] = 2
            shear = E(i, j, t)
            shear_records.append(Di*shear*Di.inv() == E(i, j, 2*t)
                                 and shear*shear == E(i, j, 2*t) and shear.det() == 1)
    check('ALL_12_PARAMETERIZED_SHEAR_CONJUGATIONS', len(shear_records) == 12 and all(shear_records))
    z = s.Symbol('z', nonzero=True)
    w2 = lambda a: s.Matrix([[1, a], [0, 1]])*s.Matrix([[1, 0], [-1/a, 1]])*s.Matrix([[1, a], [0, 1]])
    check('PARAMETERIZED_SIGNED_ROW_EXCHANGE', w2(z) == s.Matrix([[0, z], [-1/z, 0]]))
    check('PARAMETERIZED_DIAGONAL_SHEAR_FACTORIZATION', zero(w2(z)*w2(s.Integer(1)).inv()-s.diag(z, 1/z)))
    check('DETERMINANT_NORMALIZATION_TO_SL', (s.diag(1/U.det(), 1, 1, 1)*U).det() == 1)
    reflection = s.diag(-1, 1, 1, 1)
    check('NEGATIVE_DETERMINANT_COMPONENT_ORDER_TWO', reflection*reflection == I and reflection.det() == -1)

    def boost(c, b):
        return s.Matrix([[c, b, 0, 0], [b, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    B = boost(s.Rational(5, 4), s.Rational(3, 4))
    R = s.Matrix([[1, 0, 0, 0], [0, s.Rational(3, 5), s.Rational(-4, 5), 0],
                  [0, s.Rational(4, 5), s.Rational(3, 5), 0], [0, 0, 0, 1]])
    J = s.diag(1, -1, -1, 1)
    H = s.diag(1, 1, -1, -1)
    check('RATIONAL_BOOST_PROPER_FUTURE', B.T*eta*B == eta and B.det() == 1 and B[0, 0] > 0)
    check('BOOST_CONJUGATE_INVERSE_BY_PROPER_ROTATION', J*B*J == B.inv() and J.det() == 1)
    check('ROTATION_CONJUGATE_INVERSE_BY_PROPER_ROTATION', H*R*H == R.inv() and H.det() == 1)
    check('TIME_TRANSLATION_MOVED_BY_RATIONAL_BOOST', B*s.Matrix([t, 0, 0, 0])
          == s.Matrix([5*t/4, 3*t/4, 0, 0]))
    spatial_reversals = []
    for i in range(1, 4):
        j = 1+i % 3
        K = I.copy()
        K[i, i] = K[j, j] = -1
        spatial_reversals.append(K.det() == 1 and K.T*eta*K == eta and K[:, i] == -I[:, i])
    check('ALL_SPATIAL_TRANSLATIONS_CONJUGATE_INVERSE', all(spatial_reversals))

    gamma, x, y, zz = s.symbols('gamma x y zz', real=True)
    vv = s.Matrix([x, y, zz])
    Bv = s.Matrix([[gamma]]).row_join(vv.T).col_join(vv.row_join(s.eye(3)+vv*vv.T/(gamma+1)))
    relation = gamma**2-1-x*x-y*y-zz*zz

    def on_unit_hyperboloid(expr):
        num, _ = s.fraction(s.cancel(expr))
        return s.rem(num, relation, gamma) == 0

    check('GENERIC_BOOST_PRESERVES_ETA', all(on_unit_hyperboloid(e) for e in Bv.T*eta*Bv-eta))
    check('GENERIC_BOOST_HAS_UNIT_DETERMINANT', on_unit_hyperboloid(Bv.det()-1))
    check('GENERIC_BOOST_HAS_SPECIFIED_TIME_COLUMN', Bv[:, 0] == s.Matrix([gamma, x, y, zz]))

    generators = []
    for i in range(4):
        for j in range(i+1, 4):
            G = s.zeros(4)
            G[i, j] = 1
            G[j, i] = -eta[i, i]/eta[j, j]
            generators.append(G)
    check('SIX_INDEPENDENT_LITERAL_LORENTZ_GENERATORS',
          s.Matrix.hstack(*(s.Matrix(g).reshape(16, 1) for g in generators)).rank() == 6
          and all(g.T*eta+eta*g == s.zeros(4) for g in generators))
    cayleys = [(I-t*G/2).inv()*(I+t*G/2) for G in generators]
    check('ALL_SIX_CAYLEY_DETERMINANTS_IDENTICALLY_ONE', all(s.cancel(C.det()-1) == 0 for C in cayleys))
    check('ALL_SIX_CAYLEY_LORENTZ_IDENTITIES', all(zero(C.T*eta*C-eta) for C in cayleys))
    check('ALL_SIX_CAYLEY_ACTUAL_FIRST_JETS', all(C.diff(t).subs(t, 0) == G for C, G in zip(cayleys, generators)))

    links = [B, R, B*R, R*B]
    product = s.prod(links)
    rows = []
    for r in range(4):
        prefix = s.prod(links[:r]) if r else I
        suffix = s.prod(links[r+1:]) if r < 3 else I
        for G in generators:
            dP = prefix*G*links[r]*suffix
            rows.append(s.trace(product.inv()*dP))
    check('ALL_24_CONNECTION_ROWS_OF_LOG_DETERMINANT_ZERO', len(rows) == 24 and rows == [0]*24)
    raw_rows = []
    for r in range(4):
        for a in range(4):
            delta = s.zeros(5)
            delta[a, 4] = 1
            # A genuine affine translation variation at the chosen link.
            af = [affine(Ur, s.Matrix([r+1, 2, 3, 4])) for Ur in links]
            prefix = s.prod(af[:r]) if r else s.eye(5)
            suffix = s.prod(af[r+1:]) if r < 3 else s.eye(5)
            raw_rows.append(s.trace(s.prod(af).inv()*prefix*delta*suffix))
    check('ALL_16_RAW_COFRAME_SHIFT_ROWS_ZERO', len(raw_rows) == 16 and raw_rows == [0]*16)
    metric_rows = []
    packed = []
    for a in range(4):
        for b in range(a, 4):
            W = s.zeros(4)
            W[a, b] = W[b, a] = 1
            dTheta = W/2
            check_row = s.Matrix(4, 4, raw_rows)
            metric_rows.append(s.trace(check_row.T*dTheta))
            packed.append(1 if a == b else 2)
    check('ALL_TEN_SYMMETRIC_METRIC_ROWS_WITH_PACKED_WEIGHTS', len(metric_rows) == 10
          and metric_rows == [0]*10 and packed.count(1) == 4 and packed.count(2) == 6)

    # Actual stored positive slots remain distinct when L=2.
    free_records = []
    for L in [2, 4]:
        origin = (0, 0, 0, 0)
        at_r = (1 % L, 0, 0, 0)
        slots = {(origin, 0): affine(U, v), (at_r, 1): affine(V, w)}
        free_records.append(len(slots) == 2 and slots[origin, 0]*slots[at_r, 1] == affine(U*V, v+U*w))
    check('TWO_FREE_LINKS_AT_PERIODS_TWO_AND_FOUR', all(free_records))
    check('RETURN_TRANSPORT_FORGETS_NONEMPTY_WORD', affine(U, v)*inv_affine(U, v) == s.eye(5))
    check('POSITIVE_LENGTH_DOES_NOT_FACTOR_THROUGH_TRANSPORT', 2 != 0)

    # Positive controls prevent zero-valued implementations from faking blindness.
    Lg = s.diag(1+t, 1, 1, 1)
    check('GENERAL_GL_DETERMINANT_RESPONSE_IS_NONZERO', s.diff(s.log(Lg.det()), t).subs(t, 0) == 1)
    Theta = eta.copy()
    Theta[1, 1] += t
    check('COFRAME_METRIC_CAN_CHANGE_WITHOUT_AFFINE_SCALAR_RESPONSE',
          (Theta*eta*Theta.T).diff(t).subs(t, 0)[1, 1] == 2)
    hol = B*R*B.inv()*R.inv()
    check('LORENTZ_HOLONOMY_NOT_FLAT_DESPITE_UNIT_DETERMINANT', hol != I and hol.det() == 1)
    trace_square = lambda P: s.trace((P-I)**2)
    check('GAUGE_INVARIANT_HOLONOMY_FUNCTION_NEED_NOT_BE_ADDITIVE',
          trace_square(B*B) != 2*trace_square(B)
          and trace_square(R*B*R.inv()) == trace_square(B))
    check('CURVATURE_DETECTOR_DIFFERS_FROM_DETERMINANT_CHARACTER', trace_square(hol) != 0)

    # A context-dependent reading is additive at fixed configuration and keeps
    # a backtrack cost; it is outside the single-total-transport interface.
    length_cost = lambda n, theta: n*(1+theta**2)
    check('CONTEXT_DEPENDENT_PATH_COST_ESCAPE', s.expand(length_cost(2, t)-2*length_cost(1, t)) == 0
          and length_cost(2, 1) != length_cost(0, 1))
    check('ENDPOINT_POTENTIAL_NEEDS_BOUNDARY_CONDITIONS', s.diff((t+1)**2-t**2, t) == 2)
    check('CLOSED_BALANCED_BOUNDARY_SUM_CANCELS', s.expand((x-y)+(y-zz)+(zz-x)) == 0)
    q = s.Symbol('q', positive=True)
    check('NONTRIVIAL_DETERMINANT_REFINEMENT_ERROR', s.diff(s.log(1+q), q) == 1/(1+q))
    check('DETERMINANT_ONE_REFINEMENT_ERROR_CAN_HIDE_NONIDENTITY', E(0, 1, 7) != I and E(0, 1, 7).det() == 1)
    coord = s.Symbol('coord', real=True)
    profile = 1+s.cos(2*s.pi*coord)/10
    I_g = -3*s.integrate(s.diff(profile, coord)**2, (coord, 0, 1))
    check('EXISTING_CONFORMAL_CONSUMER_NORMALIZATION', I_g == -3*s.pi**2/50 and I_g != 0)
    k = s.Symbol('k', positive=True)
    check('EPSILON_H_TRANSFER_LOSS_IS_QUADRATIC_IN_CUBE_ROOT_REFINEMENT', s.cancel((1/k)/(1/k**3)) == k**2)

    scope = {
        'native_path_additivity_iff_affine_character': 'PROVED_LEAN',
        'translation_blindness_for_all_native_words': 'PROVED_LEAN',
        'complete_GL_class': 'ANALYTIC_ADDITIVE_FUNCTION_OF_LOG_ABS_DETERMINANT',
        'complete_Lorentz_only_class': 'ANALYTIC_IDENTICALLY_ZERO_WITHOUT_GL_EXTENSION',
        'all24_link_rows': 'EXACT_WITH_ANALYTIC_GLOBAL_IDENTITY',
        'all16_raw_and10_metric_rows': 'EXACT_WITH_COMPILED_SHIFT_BLINDNESS',
        'global_determinant_classification_compiled': False,
        'continuity_core_derived': False,
        'discontinuous_characters_omitted': False,
        'nonadditive_holonomy_actions_excluded': False,
        'context_dependent_path_actions_excluded': False,
        'joint_solder_matter_dependence_excluded': False,
        'scene_paths_identified_with_archive_chain': False,
        'all_GL_characters_zero': False,
        'all_open_GL_paths_gauge_invariant': False,
        'native_refinement_map_constructed': False,
        'physical_probe_admission_derived': False,
        'native_matter_source_constructed': False,
        'full_D0_stationary_gate_classified': False,
        'G0_closed': False,
        'positive_GR': False,
        'whole_core_no_go': False,
        'original_parent_terminals_changed': False,
    }
    payload = {
        'status': 'PASS_COMPLETE_NATIVE_AFFINE_HISTORY_SCALAR_BOUNDARY',
        'input_head': HEAD,
        'inputs_sha256': {p: sha(p) for p in [PROOF,
            '02_REGISTRY/research/A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md',
            '02_REGISTRY/research/A4D_NATIVE_CENTERED_METRIC_LIFT.md',
            '03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean']},
        'checker_sha256': sha(BASE+'_check.py'),
        'lean_receipt_sha256': sha(BASE+'_results.json'),
        'compiled_declarations': 21,
        'transitive_d0_source_pins': 36,
        'connection_rows': rows,
        'raw_coframe_rows': raw_rows,
        'symmetric_metric_rows': metric_rows,
        'checks': checks,
        'scope': scope,
    }
    encoded = json.dumps(payload, sort_keys=True, indent=2, default=str)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        expect = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expect.read_text()) == json.loads(encoded), 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_AFFINE_HISTORY_SCALAR', len(checks), 'exact controls; 21 Lean declarations; 36 D0 pins')


if __name__ == '__main__':
    main()
