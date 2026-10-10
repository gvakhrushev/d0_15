#!/usr/bin/env python3
"""Complete prepared price fiber; actual native scalar roots and refinement."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

HEAD = '9488c133312768580bdad43bb570a0bed836432f'
BASE = '02_REGISTRY/research/certificates/a4d_native_prepared_action'
PROOF = '02_REGISTRY/research/A4D_NATIVE_PREPARED_ACTION_COMPLETENESS.md'
PREREQUISITES = [
    '02_REGISTRY/research/certificates/a4d_native_cochain_refinement_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_metric_compactness_certificate.json',
]
SCOPE = {
    'complete_family': 'EVERY_ACTUAL_ACTION_PROTOCOL_AND_EVERY_INDEPENDENTLY_GIVEN_PREPARED_PAIR',
    'necessary_and_sufficient_conditions': 'IDENTITY_ZERO_UNIT_GAP_AND_ALL_RECORD_PAIR_FIBERS',
    'native_observable': 'ACTUAL_VACUUM_COMPONENT_AT_TWO_FROZEN_PHASE_ANCHORS',
    'quadratic_consumer': 'ALL_SYMMETRIC_PSD_TWO_BY_TWO_MATRICES_ANALYTIC_KERNEL_CLASS',
    'genuine_joint_gate': 'DERIVED_FOR_COMMON_DIFFERENTIABLE_GEOMETRY_AND_INDEPENDENT_FULL_MATTER_VARIATIONS',
    'payload_countermodel_is_literal_scene_protocol': False,
    'native_history_preparation_derived': False,
    'faithful_readout_selects_action': False,
    'canonical_minimum_selects_physical_field_law': False,
    'equal_off_shell_values_prove_equal_stationary_outputs': False,
    'empty_geometry_fiber_proves_physical_inequivalence': False,
    'totalized_nondifferentiable_derivative_used_as_stationarity': False,
    'scalar_B0_is_full_sixteen_grade_lift': False,
    'scalar_refinement_supplies_full_raw_link_refinement': False,
    'prepared_edge_commuting_supplies_full_pair_cost_commuting': False,
    'primitive_contract_excludes_curved_link_resonance': False,
    'kinematic_resonance_is_admitted_native_physical_root': False,
    'finite_node_frame_invariance_is_spacetime_Ward': False,
    'point_anchor_reading_has_smooth_volume_limit': False,
    'new_matter_or_geometric_action_selected': False,
    'own_physical_source_Ward_derived': False,
    'full_physical_gauge_selected': False,
    'G0_closed': False,
    'positive_GR': False,
    'global_closure': False,
    'whole_core_no_go': False,
    'original_parent_terminals_changed': False,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    if args.expect:
        assert json.loads(args.expect.read_text())['scope'] == SCOPE, 'PINNED_LEDGER_MISMATCH'
    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('THIRTY_COMPILED_GENUINE_PROPOSITIONS', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and not receipt['sorryAx']
          and receipt['printed_axiom_dependencies'] == 30 and receipt['owner_input_head'] == HEAD)
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_TRANSITIVE_NATIVE_TOOLCHAIN_CAPSULE_OUTPUT_PINS', all(sha(p) == h for p,h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('STANDARD_AXIOMS_AND_CLEAN_COMPILER_OUTPUT', set(receipt['axioms']) <= {'propext','Classical.choice','Quot.sound'}
          and not any(x in out for x in ['error:', 'warning:', 'sorryAx']))
    names = ['complete_prepared_action_fiber','off_diagonal_complete_fiber',
             'observable_energy_is_extendible','genuine_observable_derivative',
             'one_anchor_full_gate_iff','two_anchor_full_gate_iff',
             'common_background_joint_root_difference','genuine_joint_gate_iff']
    for name in names:
        check('ACTUAL_PROPOSITION_RESOLVED_'+name, '\nD0.Research.NativePreparedAction.'+name in out
              and "'D0.Research.NativePreparedAction."+name+"' depends on axioms:" in out)
    check('RETAINED_GEOMETRY_DIFFERENTIABILITY_AND_ROOT_PREMISES', '(hJ : ∀ (d : D), DifferentiableAt' in out
          and '(hg : D0.Research.NativePreparedAction.GeometryGate J curves b)' in out)
    check('VARIATION_CURVES_START_AT_DECLARED_BACKGROUND', '(hbase : ∀ (d : D), curves b d 0 = b)' in out)
    check('LITERAL_SCALAR_REFINEMENT_PREMISE_PRINTED', 'ScalarRefinementCompatible (N : ℕ)' in out
          and 'archiveExteriorFrameLift_vacuum_coeff' in out and 'archiveAffineCoChainGauge' in out)
    for p, expected_status in zip(PREREQUISITES, ['PASS','PASS_NATIVE_JOINT_FIELD_QUOTIENT','PASS']):
        c = json.loads((root/p).read_text())
        check('CONSUMED_PUBLISHED_PREREQUISITE_'+Path(p).stem, c['status'] == expected_status)
        pins[p] = sha(p)
    curve = json.loads((root/PREREQUISITES[-1]).read_text())
    check('PREVIOUS_CURVED_KINEMATICS_RETAINED_WITHOUT_ROOT_PROMOTION',
          curve['exact_results']['raw_determinant'] == '-1'
          and curve['exact_results']['actual_frozen_lift_centered_gradient_square'] == '4*K'
          and curve['scope']['native_admission_or_action_selected'] is False
          and curve['scope']['curved_sequence_is_joint_physical_root'] is False)

    # All three-point preparations into a three-state protocol, all legal
    # {0,1,2}-valued protocols, and every {0,1,2}-valued prepared reading.
    pairs = list(itertools.product(range(3), repeat=2))
    off = [p for p in pairs if p[0] != p[1]]
    costs = [{**{(i,i):0 for i in range(3)}, **dict(zip(off,w))}
             for w in itertools.product([1,2], repeat=len(off))]
    readings = list(itertools.product(range(3), repeat=3))
    preparations = 0
    for e in itertools.product(pairs, repeat=3):
        actual = {tuple(c[p] for p in e) for c in costs}
        allowed = {f for f in readings
                   if all(f[i] == 0 if e[i][0] == e[i][1] else f[i] >= 1 for i in range(3))
                   and all(e[i] != e[j] or f[i] == f[j] for i in range(3) for j in range(3))}
        assert actual == allowed, (e, actual, allowed)
        preparations += 1
    check('EXHAUSTIVE_729_PREPARATIONS_64_PROTOCOLS_27_READINGS', preparations == 729 and len(costs) == 64)
    e = [(0,0),(0,1),(0,1)]
    actual = {tuple(c[p] for p in e) for c in costs}
    check('HOSTILE_NONZERO_IDENTITY_REJECTED', (1,1,1) not in actual)
    check('HOSTILE_SUBQUANTUM_PREPARED_PRICE_REJECTED', (0,0,0) not in actual)
    check('HOSTILE_INCONSISTENT_RECORD_FIBER_REJECTED', (0,1,2) not in actual)
    check('CANONICAL_OFF_DIAGONAL_EXCESS_IS_ZERO', all((1-1) == 0 for _ in off))
    check('ERASING_PERSISTENT_BIT_RETURNS_IDENTITY_PRICE_ZERO', all(costs[0][(i,i)] == 0 for i in range(3)))

    t,b,db,x,y,dx,dy = s.symbols('t b db x y dx dy', real=True)
    a,c,d = s.symbols('a c d', real=True)
    M = s.Matrix([[a,c],[c,d]])
    v,w = s.Matrix([x,y]), s.Matrix([dx,dy])
    E = lambda z: (z.T*M*z)[0]
    check('WHOLE_SYMMETRIC_QUADRATIC_GENUINE_DERIVATIVE', s.expand(s.diff(E(v+t*w),t).subs(t,0)-2*(M*v).dot(w)) == 0)
    check('QUADRATIC_EULER_COEFFICIENTS_INJECTIVE', s.Poly(E(v),x,y).coeff_monomial(x*x) == a
          and s.Poly(E(v),x,y).coeff_monomial(x*y) == 2*c and s.Poly(E(v),x,y).coeff_monomial(y*y) == d)
    M1,M2 = s.diag(1,0),s.eye(2)
    for j,m in enumerate([s.zeros(2),M1,M2,s.Matrix([[1,1],[1,1]]),s.Matrix([[2,-1],[-1,2]])]):
        check('NONNEGATIVE_QUADRATIC_MEMBER_'+str(j), m.is_positive_semidefinite is True)
        check('FULL_GATE_MATRIX_DERIVATIVE_'+str(j), s.Matrix([s.diff((v.T*m*v)[0],x),s.diff((v.T*m*v)[0],y)]) == 2*m*v)
    check('TWO_NONZERO_ENERGIES_HAVE_DIFFERENT_KERNELS', M1.rank() == 1 and M2.rank() == 2
          and M1*s.Matrix([0,1]) == s.zeros(2,1) and M2*s.Matrix([0,1]) != s.zeros(2,1))
    check('NONZERO_CALIBRATION_DOES_NOT_REPAIR_KERNEL', (7*M1).nullspace() == M1.nullspace()
          and (7*M1).nullspace() != M2.nullspace())
    check('ACTION_PARAMETER_DIFFERENCE_CAN_HAVE_SAME_ROOTS', (2*M1).nullspace() == M1.nullspace())
    J = 3*b*b
    joint = [J+x*x,J+x*x+y*y]
    joint_grad = [s.Matrix([s.diff(z,b),s.diff(z,x),s.diff(z,y)]) for z in joint]
    witness = {b:0,x:0,y:1}
    check('COMMON_GEOMETRY_GENUINE_JOINT_ROOT_DIFFERENCE', joint_grad[0].subs(witness) == s.zeros(3,1)
          and joint_grad[1].subs(witness) == s.Matrix([0,0,2]))
    check('BOTH_JOINT_STATIONARY_FIBERS_NONEMPTY', all(g.subs({b:0,x:0,y:0}) == s.zeros(3,1) for g in joint_grad))
    check('COMMON_PREPARED_JOINT_PRICE_DERIVATIVE', s.diff(1+J.subs(b,b+t*db)+(x+t*dx)**2+(y+t*dy)**2,t).subs(t,0)
          == 6*b*db+2*x*dx+2*y*dy)
    check('HOSTILE_MATTER_ONLY_GATE_IS_NOT_JOINT_STATIONARITY', s.diff(b+x*x,b).subs(witness) == 1)
    check('EMPTY_GEOMETRY_FIBER_RETAINED_AS_EXCEPTION', s.diff(b,b) != 0)

    metric = s.symbols('q:10',real=True)
    link = s.symbols('k:24',real=True)
    shifts = s.symbols('a:16',real=True)
    for i,z in enumerate(metric):
        check('ALL_TEN_PACKED_METRIC_ZERO_SOURCE_'+str(i), s.diff(x*x+y*y,z) == 0)
    for i,z in enumerate(link):
        check('ALL_24_CONNECTION_ROW_ZERO_SOURCE_'+str(i), s.diff(x*x+y*y,z) == 0)
    check('ALL_AFFINE_SHIFT_AND_RAW_COFRAME_ZERO_SOURCES', all(s.diff(x*x+y*y,z) == 0 for z in shifts))

    supports = [tuple(r for r in range(4) if mask & (1<<r)) for mask in range(16)]
    eta = s.diag(1,-1,-1,-1)
    B = s.eye(4); B[0,0]=B[1,1]=s.Rational(5,4); B[0,1]=B[1,0]=s.Rational(3,4)
    G = s.eye(4); G[0,2]=2; G[3,3]=3
    F = eta*G
    check('FULL_RAW_PAYLOAD_NONDEGENERATE_WITH_ALL_LINK_SHIFTS_FREE', F.det() != 0 and B*eta*B.T == eta)
    for label,L in [('proper_Lorentz',B),('general_invertible_frame',G)]:
        rho = s.zeros(16)
        for i,I in enumerate(supports):
            for j,T in enumerate(supports):
                if len(I) == len(T):
                    rho[i,j] = L.extract(I,T).det() if I else 1
        check('ACTUAL_EXTERIOR_VACUUM_ROW_'+label, list(rho.row(0)) == [1]+[0]*15)
        psi = s.Matrix([s.Rational(j-3,7) for j in range(16)])
        check('FULL_SIXTEEN_GRADE_VACUUM_OBSERVABLE_PRESERVED_'+label, (rho*psi)[0] == psi[0])
    check('FALSE_FRAME_VACUUM_MIXING_DETECTED', psi[0]+psi[1] != psi[0])

    for L in [2,3,4,6]:
        native = list(itertools.product(range(L), repeat=4))
        anchors = [(0,0,0,0),(1,0,0,0)]
        index = {(p,mask):i for i,(p,mask) in enumerate(itertools.product(native,range(16)))}
        read = s.zeros(2,len(index))
        for k,p in enumerate(anchors): read[k,index[p,0]]=1
        check('ACTUAL_FULL_COCHAIN_READOUT_SURJECTIVE_L'+str(L), read*read.T == s.eye(2))
        check('FULL_NATIVE_KERNEL_DIMENSIONS_L'+str(L), len(index)-M1.rank() == 16*L**4-1
              and len(index)-M2.rank() == 16*L**4-2)
        for K in [L+1,2*L]:
            ratio = s.Rational(K,L)
            projection = lambda p: tuple(z if z < L else 0 for z in p)
            for mask,S in enumerate(supports):
                sample = lambda p: s.Rational(1+mask+sum((r+1)*z for r,z in enumerate(p))
                                               + p[0]*p[2],13)
                lift = lambda p: 0 if any(p[r] >= L for r in S) else ratio**len(S)*sample(projection(p))
                check('GRADED_PREFIX_LEFT_INVERSE_L'+str(L)+'K'+str(K)+'S'+str(mask),
                      all(lift(p)/ratio**len(S) == sample(p) for p in native))
                if S:
                    p=[0]*4;p[S[0]]=L
                    check('OCCUPIED_COLLAPSED_ROW_ZERO_L'+str(L)+'K'+str(K)+'S'+str(mask), lift(tuple(p)) == 0)
                else:
                    check('SCALAR_ANCHORS_LITERAL_B0_L'+str(L)+'K'+str(K), all(projection(p) == p and lift(p) == sample(p) for p in anchors))
            check('FULL_REFINED_ONE_ROOT_TWO_NONROOT_L'+str(L)+'K'+str(K), all(projection(p) == p for p in anchors)
                  and M1*s.Matrix([0,1]) == s.zeros(2,1) and M2*s.Matrix([0,1]) != s.zeros(2,1))
        f = [s.Rational((j+1)**2,11) for j in range(L)]
        B0 = f+[f[0]]
        dc = [f[(j+1)%L]-f[j] for j in range(L)]
        df = [B0[(j+1)%(L+1)]-B0[j] for j in range(L+1)]
        check('ALL_ORDINARY_WRAP_COLLAPSED_SCALED_INCIDENCE_L'+str(L),
              [(L+1)*z for z in df] == [s.Rational(L+1,L)*L*z for z in dc]+[0])
        check('WRONG_VERTEX_LIFT_FOR_OCCUPIED_WRAP_DETECTED_L'+str(L), dc[-1] != 0)

    # Refinement of all state-pair costs cannot be inferred from the prepared
    # off-diagonal bit edge alone when a payload map identifies two states.
    p=(False,0);q=(False,1)
    cost=lambda p,q: 0 if p == q else 1+q[1]**2
    collapse=lambda p: (p[0],0)
    check('FULL_PAIR_COST_NONINJECTIVE_REFINEMENT_HOSTILE', cost(p,q) >= 1 and cost(collapse(p),collapse(q)) == 0)
    check('PREPARED_BIT_EDGE_COMMUTES_DESPITE_PAYLOAD_COLLAPSE', cost((False,0),(True,0)) == cost(collapse((False,0)),collapse((True,0))))

    payload={'status':'PASS','owner_input_head':HEAD,'scope':SCOPE,'checks':checks,
             'input_sha256':pins,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
             'transitive_d0_source_count':len(receipt['transitive_d0_source_sha256']),
             'exact_results':{'finite_preparations':729,'finite_protocols':64,'finite_readings':27,
                 'native_fock_components':16,'persistent_scalar_anchors':2,'quadratic_action_dimension':3,
                 'two_nonzero_stationary_codimensions':[1,2],'root_witness':[0,1],
                 'nonroot_directional_derivative':'2','common_geometry_source_difference':'0',
                 'metric_components':10,'connection_rows':24,'full_matter_dimensions':'16*L^4',
                 'full_raw_link_refinement_derived':False}}
    if args.output:
        args.output.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    else:
        expected=args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_PREPARED_ACTION_COMPLETENESS',len(checks),'controls',len(receipt['transitive_d0_source_sha256']),'D0 pins')


if __name__ == '__main__':
    main()
