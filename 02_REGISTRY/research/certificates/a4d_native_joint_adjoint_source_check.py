#!/usr/bin/env python3
"""Exact finite controls; analytic classification is in the pinned proof.

Default mode verifies the immutable certificate; --write seals only a ready
proof and successful narrow Lean receipt. No physical selection is performed.
"""
import argparse
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source'
PROOF = '02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md'
INPUTS = [
    '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
    '02_REGISTRY/research/A4D_NATIVE_CURVED_SOLDERED_HEAT.md',
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source.py',
    '03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '03_FORMALIZATION/D0/Cosmology/FeedbackPartitionFunction.lean',
]
spec = importlib.util.spec_from_file_location('joint_adjoint_program', ROOT/(BASE+'.py'))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
s = P.s


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def source_closure(paths):
    found, pending = set(), list(paths)
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        if path.endswith('.lean'):
            for line in (ROOT/path).read_text().splitlines():
                if line.startswith('import '):
                    pending.extend('03_FORMALIZATION/'+name.replace('.', '/')+'.lean'
                        for name in line.split()[1:] if name.startswith('D0.'))
    return sorted(found)


def controls(include_receipt=True):
    checks, mutants = [], []
    def zero(value):
        vals = value.todok().values() if isinstance(value, s.MatrixBase) else [value]
        return all(s.simplify(v) == 0 for v in vals)
    def check(name, truth):
        assert bool(truth), name
        checks.append(name)
    def eq(name, value):
        check(name, zero(value))
    def reject(name, false):
        check('REJECT_'+name, not false)
        mutants.append(name)

    E, I4, I16 = P.ETA, s.eye(4), s.eye(16)
    e0, e1, e2, e3 = [I4[:, i] for i in range(4)]
    boost = s.Matrix([[s.Rational(5,4), s.Rational(3,4), 0, 0],
                      [s.Rational(3,4), s.Rational(5,4), 0, 0], [0,0,1,0], [0,0,0,1]])
    ny = s.Matrix([s.Rational(13,12), 0, s.Rational(5,12), 0])
    nx, vy = boost*ny, s.Matrix([1, 2, -1, 3])
    vx = boost*vy
    data = P.edge(boost, nx, ny, vx, vy)
    eq('rational_link_Lorentz', boost.T*E*boost-E)
    for tag, n in [('x', nx), ('y', ny)]:
        eq('unit_observer_'+tag, (n.T*E*n)[0]-1)
        h = P.observer(n)
        eq('unit_observer_Gram_determinant_'+tag, h.det()-1)
        for j in range(1,5):
            check('positive_observer_Gram_%s_minor%d' % (tag,j), h[:j,:j].det() > 0)
        eq('actual_full16_Gram_compound_'+tag, P.exterior_gram(h)-P.exterior(h))
    eq('full16_exterior_inverse', data['U']*P.exterior(boost.inv())-I16)
    eq('full16_boosted_observer_edge_adjoint', data['defect'])
    eq('observer_edge_congruence', boost.T*data['hx']*boost-data['hy'])
    eq('transported_leg_condition', vx-boost*vy)
    eq('full16_positive_observer_congruence', data['U'].T*data['Gx']*data['U']-data['Gy'])
    eq('full16_classifier_T_identity', data['T']-I4)
    eq('full16_classifier_b_equals_c', data['b']-data['c'])
    eq('observer_sign_is_unseen', P.observer(-nx)-P.observer(nx))
    eq('negative_observer_branch_still_adjoint', P.edge(boost,-nx,ny,vx,vy)['defect'])
    reject('POSITIVE_OBSERVER_SIGN_WITHOUT_TIME_ORIENTATION', zero(boost*ny+nx))
    reject('LORENTZ_LINK_ALONE_GIVES_STORED_ADJOINT', zero(P.edge(boost,e0,e0,vx,vy)['defect']))
    reject('OBSERVER_CONGRUENCE_ALONE_GIVES_STORED_ADJOINT', zero(P.edge(boost,nx,ny,vx+e3,vy)['defect']))
    contraction = P.creator(data['b']).T
    eq('full16_edge_reduction_equation', contraction-P.exterior(data['T'])*P.creator(data['c']).T)

    gl = I4+E*0
    gl[1,1] = 2
    escaped = P.edge(gl,e0,e0,e1,2*e1)
    eq('GL_rank_one_full16_adjoint_exception', escaped['defect'])
    eq('GL_rank_one_T', escaped['T']-(I4+3*e1*e1.T))
    reject('GL_EXCEPTION_IS_LORENTZ', zero(gl.T*E*gl-E))
    Fx, Fy = E, s.diag(1,-2,-1,-1)
    qx, qy = Fx*E*Fx.T, Fy*E*Fy.T
    dressed = Fx*gl*Fy.inv()
    eq('GL_same_dressed_carrier_exact_defect', dressed*qy*dressed.T-qx-Fx*(gl*E*gl.T-E)*Fx.T)
    reject('GL_ESCAPE_PRESERVES_SAME_CARRIER', zero(dressed*qy*dressed.T-qx))
    fooled = P.edge(s.diag(2,3,1,1),e0,e0,e0/2,e0)
    eq('degree_one_only_classifier_can_pass', fooled['b']-fooled['c'])
    eq('degree_one_only_edge_can_pass', fooled['defect'].extract([0],[1,2,4,8]))
    reject('DEGREE_ONE_PROVES_FULL16_ADJOINT', zero(fooled['defect']))
    # Arbitrary GL construction uses an orthogonal direction map and one dilation.
    source, target = s.Matrix([1,0,0,0]), s.Matrix([s.Rational(3,5),s.Rational(4,5),0,0])
    rotation = P.minimal_rotation(source,target)
    general_gl = rotation*(I4+2*source*source.T)
    eq('GL_constructive_direction_rotation', rotation*source-target)
    eq('GL_constructive_rotation_orthogonal', rotation.T*rotation-I4)
    eq('GL_constructive_full16_exception', P.edge(general_gl,e0,e0,2*target,6*source)['defect'])

    ranks = []
    lorentz_basis = [P.lorentz_jet(s.eye(6)[:,j]) for j in range(6)]
    for j,W in enumerate(lorentz_basis):
        eq('all_six_Lorentz_link_generators_%d'%j,W.T*E+E*W)
    for flags in product((0,1),repeat=4):
        constraint, metric = P.tangent_system(flags)
        rank = constraint.rank()
        image = constraint.col_join(metric).rank()-rank
        b, spatial = flags[0], sum(flags[1:])
        tag = ''.join(map(str,flags))
        check('joint_constraint_rank_'+tag,rank == 18+4*b+2*spatial)
        check('joint_linearized_solution_dimension_'+tag,43-rank == 25-4*b-2*spatial)
        check('joint_metric_image_rank_'+tag,image == 10-b-spatial-b*spatial)
        check('joint_metric_kernel_'+tag,43-rank-image == 15-3*b-spatial+b*spatial)
        null = s.Matrix.hstack(*constraint.nullspace())
        image_matrix = metric*null
        forbidden = [j for j,(r,t) in enumerate(P.SLOTS)
                     if (r == t and flags[r]) or (r == 0 and t > 0 and flags[0] and flags[t])]
        eq('joint_metric_forbidden_slots_'+tag,image_matrix.extract(forbidden,range(image_matrix.cols)))
        check('joint_metric_full_allowed_image_'+tag,image == 10-len(forbidden))
        gauge_columns = []
        for j,W in enumerate(lorentz_basis):
            column = list(E*W)+list((-W[:,0])[1:4,0])
            for r in range(4):
                column += list(-flags[r]*s.eye(6)[:,j])
            gauge_columns.append(s.Matrix(column))
        native_gauge = s.Matrix.hstack(*gauge_columns)
        eq('native_Lorentz_gauge_admitted_'+tag,constraint*native_gauge)
        eq('native_Lorentz_gauge_metric_null_'+tag,metric*native_gauge)
        check('native_Lorentz_gauge_free_six_'+tag,native_gauge.rank()==6)
        ranks.append({'nonzero_pattern':list(flags),'constraint_rank':rank,
            'linearized_solution_dimension':43-rank,'metric_image_rank':image,
            'metric_map_kernel':43-rank-image})
    L = s.symbols('L',integer=True,positive=True)
    def lattice_sum(expression):
        return sum(s.binomial(3,k)*(L-1)**(b+k)*expression(b,k) for b in (0,1) for k in range(4))
    eq('all_level_joint_solution_dimension',lattice_sum(lambda b,k:25-4*b-2*k)-(15*L**4+10*L**3))
    eq('all_level_metric_image_dimension',lattice_sum(lambda b,k:10-b-k-b*k)-(3*L**4+10*L**3-3*L**2))
    eq('all_level_metric_kernel_dimension',lattice_sum(lambda b,k:15-3*b-k+b*k)-(12*L**4+3*L**2))
    eq('all_level_native_gauge_quotient_linearized_dimension',
       lattice_sum(lambda b,k:25-4*b-2*k-6)-(9*L**4+10*L**3))
    eq('all_level_nongauge_metric_null_dimension',
       lattice_sum(lambda b,k:15-3*b-k+b*k-6)-(6*L**4+3*L**2))
    # The comparator is ordinary Fourier coordinate gauge, not native admission.
    gauge = s.Matrix([[int(r == j)+int(t == j) for j in range(4)] for r,t in P.SLOTS])
    allowed = s.Matrix.hstack(*[s.eye(10)[:,P.SLOTS.index(slot)] for slot in [(1,2),(1,3),(2,3)]])
    combined = allowed.row_join(gauge)
    check('generic_metric_plus_coordinate_gauge_dimension',combined.rank() == 7)
    witness = s.Matrix([0,0,0,0,1,0,0,-1,0,0])
    reject('GENERIC_MISSING_PROBE_IS_COORDINATE_GAUGE', combined.row_join(witness).rank() == combined.rank())

    # All ten coefficients of the nonlinear lift at one site; axis conditions
    # and existence of its edge rotations are the analytic construction.
    eps = s.symbols('eps',real=True)
    diagonal = s.Matrix([2,4,-2,6])
    time_A, time_B = s.Matrix([1,2,3]), s.Matrix([4,-1,2])
    spatial_cross = s.Matrix([[0,2,-4],[2,0,6],[-4,6,0]])
    legs = P.metric_lift_legs(eps,diagonal,time_A,time_B,spatial_cross)
    frame = P.raw_frame(legs)
    H = s.diag(*diagonal)
    for i in range(3):
        H[0,i+1] = H[i+1,0] = time_A[i]+time_B[i]
    for i in range(3):
        for j in range(3):
            if i != j:
                H[i+1,j+1] = spatial_cross[i,j]
    eq('nonlinear_metric_lift_base_frame',frame.subs(eps,0)-E)
    eq('nonlinear_metric_lift_all_ten_first_jets',(frame*E*frame.T).diff(eps).subs(eps,0)-H)
    for r,t in P.SLOTS:
        target = s.zeros(4)
        target[r,t] = target[t,r] = 1
        diagonal_basis = s.Matrix([target[j,j] for j in range(4)])
        time_basis = target[0,1:4].T
        spatial_basis = target[1:4,1:4]-s.diag(*[target[j,j] for j in range(1,4)])
        lifted = P.raw_frame(P.metric_lift_legs(eps,diagonal_basis,
                         time_basis/3,2*time_basis/3,spatial_basis))
        eq('nonlinear_metric_lift_independent_slot_%d%d'%(r,t),
           (lifted*E*lifted.T).diff(eps).subs(eps,0)-target)
    for i in range(3):
        spatial_leg = legs[i+1][1:4,0]
        eq('nonlinear_lift_spatial_norm_%d'%i,(spatial_leg.T*spatial_leg)[0]-(1-eps*diagonal[i+1]/2)**2)
    # Exact finite nonconstant direction: rational circle parameterization.
    a,b = s.Rational(1,5),s.Rational(1,3)
    circle = lambda t:s.Matrix([(1-t*t)/(1+t*t),2*t/(1+t*t),0])
    uy,ux = circle(a),circle(b)
    rot = P.minimal_rotation(uy,ux)
    eq('nonlinear_finite_rotation_orthogonal',rot.T*rot-s.eye(3))
    eq('nonlinear_finite_rotation_determinant',rot.det()-1)
    eq('nonlinear_finite_rotation_transports_leg',rot*uy-ux)
    link = s.diag(1,1,1,1)
    link[1:4,1:4] = rot
    lvx,lvy = s.Matrix([s.Rational(1,7),*list(2*ux)]),s.Matrix([s.Rational(1,7),*list(2*uy)])
    eq('nonlinear_finite_joint_edge_full16',P.edge(link,e0,e0,lvx,lvy)['defect'])
    # Exact periodic holonomy forbids a particular linearized joint velocity.
    generator = s.zeros(4)
    generator[2,1],generator[1,2] = 1,-1
    eq('holonomy_bad_jet_passes_first_order_leg',generator*e0)
    eq('holonomy_bad_jet_passes_first_order_observer',generator*e0)
    bad_jet = s.zeros(43,1)
    bad_jet[1] = -1  # delta v_0=e_1, hence delta F_01=-1
    bad_jet[22] = -1  # temporal link rotation in the spatial 12 plane
    eq('holonomy_bad_jet_passes_full_joint_linearization',
       P.tangent_system((0,0,0,0))[0]*bad_jet)
    reject('ALL_LINEARIZED_JOINT_SOLUTIONS_INTEGRATE',zero(4*generator*e1))
    rational_turn = I4.copy()
    rational_turn[1:3,1:3] = s.Matrix([[1-eps**2/4,-eps],[eps,1-eps**2/4]])/(1+eps**2/4)
    eq('holonomy_witness_links_exactly_Lorentz',rational_turn.T*E*rational_turn-E)
    eq('holonomy_witness_link_first_jet',rational_turn.diff(eps).subs(eps,0)-generator)
    holonomy = rational_turn**4
    eq('holonomy_exact_second_order_obstruction',
       (holonomy*(eps*e1)-eps*e1).diff(eps,2).subs(eps,0)-8*generator*e1)
    finite_turn = rational_turn.subs(eps,s.Rational(1,10))
    finite_leg = e0+e1/10
    eq('holonomy_leg_jet_separately_exact',P.edge(I4,e0,e0,finite_leg,finite_leg)['defect'])
    eq('holonomy_link_jet_separately_exact',P.edge(finite_turn,e0,e0,e0,e0)['defect'])
    reject('FIRST_ORDER_HOLONOMY_JET_SUFFICES_FOR_EXACT_ADJOINT',
           zero(P.edge(finite_turn,e0,e0,finite_leg,finite_leg)['defect']))

    # Unique neighboring-grade completion, distinct from selecting native heat.
    g = s.symbols('g',positive=True)
    G = P.exterior_gram(s.diag(g,1,1,1))
    d = P.creator(e0)
    adjd = P.dagger(d,G)
    D = d+adjd
    eq('general_positive_G_full16_adjoint',G*adjd-d.T*G)
    eq('general_positive_G_full16_completion_selfadjoint',G*D-D.T*G)
    eq('fixed_creator_full16_heat_square',D*D-g*I16)
    beta = s.symbols('beta',positive=True)
    partition = 16*s.exp(-beta*g)
    eq('fixed_creator_actual_Gibbs_weight',s.exp(-beta*g)*I16/partition-I16/16)
    eq('fixed_creator_actual_log_heat_derivative',s.diff(s.log(partition)/beta,g)+1)
    deltaG = G.diff(g)
    K = G.inv()*deltaG
    rho = I16/16
    CG = -2*P.comm(rho*D,adjd)
    eq('fixed_creator_full16_Gram_source_minus_one',s.trace(CG*K)+1)
    eq('general_Gram_source_traceless',s.trace(CG))
    eq('general_Gram_source_selfadjoint',P.dagger(CG,G)-CG)
    movingd = d/s.sqrt(g)
    movingD = movingd+P.dagger(movingd,G)
    eq('true_basis_full16_heat_square',movingD*movingD-I16)
    movingCG = -2*P.comm(rho*movingD,P.dagger(movingd,G))
    eq('true_basis_full16_heat_Ward',-4*s.trace(rho*movingD*movingd.diff(g))+s.trace(movingCG*K))
    reject('FIXED_CREATOR_GRAM_CHANGE_IS_ONLY_BASIS',zero(s.trace(CG*K)))
    extra = P.creator(e0)*P.creator(e1)*P.creator(e2)
    extra += extra.T
    eq('additional_odd_grade_three_selfadjoint',extra-extra.T)
    reject('SELFADJOINT_ODD_ALONE_FIXES_NEIGHBOR_COMPLETION',zero(extra))

    fixture = P.covector_fixture()
    G,d,U,Pi,K,X,A,Z,rho,z = [fixture[k] for k in ('G','d','U','P','K','X','A','Z','rho','z')]
    data = P.joint_covector(d,G,Pi,U,z,rho)
    D,N,F,R,C,J,CG = [data[k] for k in ('D','N','F','R','C','J','CG')]
    adj = lambda M:P.dagger(M,G)
    eq('covector_projection_idempotent',Pi*Pi-Pi)
    eq('covector_projection_G_selfadjoint',adj(Pi)-Pi)
    eq('covector_unitarity',adj(U)*U-I4)
    eq('covector_feedback_selfadjoint',adj(F)-F)
    eq('covector_feedback_support',Pi*F*Pi-F)
    eq('covector_feedback_resolvent',R*(I4-z*F)-z*I4)
    eq('covector_commuting_positive_weight',P.comm(rho,D))
    eq('covector_weight_normalized',s.trace(rho)-1)
    weight_orthonormal = fixture['T'].inv()*rho*fixture['T']
    eq('covector_weight_G_selfadjoint',adj(rho)-rho)
    for j in range(1,5):
        check('covector_surrogate_positive_minor%d'%j,weight_orthonormal[:j,:j].det()>0)
    eq('balanced_K_selfadjoint',adj(K)-K)
    eq('balanced_X_selfadjoint',adj(X)-X)
    eq('balanced_projection_tangent',Pi*X+X*Pi-X)
    eq('balanced_A_skewadjoint',adj(A)+A)
    dotd = Z-P.comm(K,d)/2
    dotP = X-P.comm(K,Pi)/2
    dotU = U*A-P.comm(K,U)/2
    dotadjU = adj(dotU)+P.comm(adj(U),K)
    dotD = dotd+adj(dotd)+P.comm(adj(d),K)
    dotN = dotadjU*(I4-Pi)*U-adj(U)*dotP*U+adj(U)*(I4-Pi)*dotU
    dotF = dotP*N*Pi+Pi*dotN*Pi+Pi*N*dotP
    eq('raw_projection_tangent',Pi*dotP+dotP*Pi-dotP)
    eq('raw_projection_moving_adjoint',adj(dotP)+P.comm(Pi,K)-dotP)
    eq('raw_unitary_moving_adjoint',dotadjU*U+adj(U)*dotU)
    heat = -s.trace(rho*(D*dotD+dotD*D))
    feedback = s.trace(R*dotF)
    eq('balanced_heat_covector_factor_four',heat+4*s.trace(rho*D*Z))
    eq('balanced_feedback_covector',feedback-s.trace(C*X)-s.trace(J*A))
    eq('raw_heat_Gram_covector',heat+4*s.trace(rho*D*dotd)-s.trace(CG*K))
    eq('raw_feedback_covector',feedback-s.trace(C*dotP)-s.trace(J*U.inv()*dotU))
    eq('feedback_Noether_cancellation',P.comm(Pi,C)+U*J*U.inv()-J)
    eq('feedback_is_independent_of_explicit_Gram_slot',F-Pi*U.inv()*(I4-Pi)*U*Pi)
    eq('Gram_covector_selfadjoint',adj(CG)-CG)
    eq('Gram_covector_trace_zero',s.trace(CG))
    reject('DROP_HEAT_GRAM_COVECTOR',zero(s.trace(CG*K)))
    reject('DROP_HEAT_FACTOR_TWO',zero(heat+2*s.trace(rho*D*Z)))
    reject('DROP_FEEDBACK_RESOLVENT_SIGN',zero(feedback+s.trace(C*X)+s.trace(J*A)))
    metricGram = CG*G.inv()
    eq('raw_Gram_covector_symmetric',metricGram-metricGram.T)
    for i,j in P.SLOTS:
        Q = s.zeros(4)
        Q[i,j] = Q[j,i] = 1
        Kg = G.inv()*Q
        direct = -s.trace(rho*(D*P.comm(adj(d),Kg)+P.comm(adj(d),Kg)*D))
        packed = metricGram[i,i] if i == j else 2*metricGram[i,j]
        eq('all_ten_Gram_packed_coefficients_%d%d'%(i,j),direct-packed)
    off = next((metricGram[i,j] for i,j in P.SLOTS if i != j and metricGram[i,j] != 0))
    reject('DROP_Gram_PACKED_OFFDIAGONAL_TWO',zero(2*off-off))
    for i in range(4):
        for j in range(4):
            Eij = s.zeros(4)
            Eij[i,j] = 1
            deltaD = Eij+adj(Eij)
            eq('all_sixteen_d_covector_coefficients_%d%d'%(i,j),
               -s.trace(rho*(D*deltaD+deltaD*D))+4*s.trace(rho*D*Eij))
    V = s.Matrix(4,4,[2,-1,0,3,1,4,2,0,-2,1,3,1,0,2,-1,5])
    basisK = -adj(V)-V
    basisdotd,basisdotP,basisdotU = [P.comm(V,M) for M in (d,Pi,U)]
    basisdotD = basisdotd+adj(basisdotd)+P.comm(adj(d),basisK)
    eq('full_joint_basis_D_Ward',basisdotD-P.comm(V,D))
    eq('full_joint_basis_heat_Ward',-4*s.trace(rho*D*basisdotd)+s.trace(CG*basisK))
    eq('full_joint_basis_feedback_Ward',s.trace(C*basisdotP)+s.trace(J*U.inv()*basisdotU))

    if not include_receipt:
        return {'exact_controls':len(checks),'mutants':mutants,'ranks':ranks}
    receipt_path = BASE+'_lean_results.json'
    receipt = json.loads((ROOT/receipt_path).read_text())
    output = (ROOT/(BASE+'_lean_output.txt')).read_text()
    check('narrow_Lean_receipt_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
    check('Lean_capsule_fingerprint',receipt['capsule_sha256']==sha(BASE+'.lean'))
    check('Lean_actual_output_fingerprint',receipt['output_sha256']==sha(BASE+'_lean_output.txt'))
    actual_axioms = {name:[a.strip() for a in body.split(',') if a.strip()]
        for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output)}
    check('Lean_actual_axiom_receipt',actual_axioms==receipt['axioms'])
    check('Lean_declared_closures_resolved',set(actual_axioms)==set(receipt['declarations']))
    printed = set(re.findall(r'^#print axioms ([A-Za-z0-9_.]+)',
                           (ROOT/(BASE+'.lean')).read_text(),re.MULTILINE))
    check('Lean_every_capsule_axiom_request_resolved',set(actual_axioms)==printed)
    for name,axioms in actual_axioms.items():
        check('Lean_standard_axioms_'+name,set(axioms)<={'propext','Classical.choice','Quot.sound'})
    for name in receipt.get('diagnostic_definitions',[]):
        check('Lean_actual_definition_print_'+name,
              ('def '+name+' ') in output or ('theorem '+name+' ') in output)
    for name in receipt.get('diagnostic_checks',[]):
        check('Lean_actual_declaration_check_'+name,(name+' ') in output or (name+'\n') in output)
    for name in receipt.get('diagnostic_printed_propositions',[]):
        check('Lean_actual_proposition_print_'+name,('theorem '+name+' ') in output)
    for path,fingerprint in receipt['input_sha256'].items():
        check('Lean_source_input_'+path,sha(path)==fingerprint)
    check('Lean_original_cache_preserved',receipt['original_cache_unchanged'])
    prior = receipt['verified_overlay_receipt']
    check('Lean_prior_overlay_receipt_binding',sha(prior['path'])==prior['sha256'])
    check('Lean_overlay_55_source_modules',len(receipt['cache_source_comparison'])==55)
    check('Lean_46_matching_source_cache_artifacts',
          receipt['matching_cache_source_reuse_count']==46 and
          list(receipt['cache_source_comparison'].values()).count('MATCH')==46)
    check('Lean_nine_prior_source_rebuilds_not_new_compiles',
          receipt['verified_prior_source_rebuild_count']==9 and
          receipt['new_overlay_compilation_count']==0 and len(receipt['source_overlay_rebuilds'])==9)
    for entry in receipt['source_overlay_rebuilds']:
        check('Lean_inherited_SOURCE_build_success_'+entry['module'],entry['exit_code']==0)
        check('Lean_inherited_SOURCE_build_output_'+entry['module'],
              hashlib.sha256(entry['compiler_stdout'].encode()).hexdigest()==entry['output_sha256'])
        source_path='03_FORMALIZATION/'+entry['module'].replace('.','/')+'.lean'
        check('Lean_inherited_SOURCE_build_source_'+entry['module'],sha(source_path)==entry['source_sha256'])
    source = re.search(r'Input SOURCE\s+`([0-9a-f]{40})`',(ROOT/PROOF).read_text()).group(1)
    check('proof_Lean_SOURCE_agree',source==receipt['source_commit'])
    inputs = source_closure(INPUTS+list(receipt['input_sha256']))
    return {'schema':'d0-native-joint-adjoint-source/1',
        'verdict':'COMPLETE_STORED_JOINT_ADJOINT_CLASS_AND_CONDITIONAL_COVECTOR',
        'input_source_sha':source,'exact_controls':len(checks),'controls':checks,
        'executed_mathematical_mutants':mutants,'joint_tangent_patterns':ranks,
        'generic_nonzero_frequency_metric_rank':3,'generic_metric_plus_coordinate_gauge_rank':7,
        'L4_linearized_dimensions':{'unknowns':11008,'constraints':6528,'solutions':4480,'metric_image':1360,'metric_kernel':3120,
            'native_Lorentz_gauge':1536,'solution_after_native_gauge':2944,'nongauge_metric_null':1584},
        'scope':'Exact full16 edge, Gram, CAR and scalar-square controls; exact linear systems, symbolic jets and constrained covector kernels. Complete classes, general nonlinear realizability and thermal differentiation are analytic statements in the pinned proof; not all are Lean-formalized.',
        'commuting_fixture_weight':'Normalized (I+D^2)^-1: exact algebraic surrogate, not Gibbs; full16 scalar-square case uses exact Gibbs weight I16/16.',
        'general_G_completion_native_admission':'OPEN','bootstrap_heat_identification':'OPEN',
        'native_joint_preparation':'OPEN','source_Ward_GR':'OPEN','curved_joint_on_shell':'OPEN',
        'quantitative_refinement_soundness_recovery':'OPEN','original_parent_terminal':'OPEN',
        'input_sha256':{path:sha(path) for path in inputs},
        'proof_sha256':sha(PROOF),'program_sha256':sha(BASE+'.py'),'checker_sha256':sha(BASE+'_check.py'),
        'Lean_capsule_sha256':sha(BASE+'.lean'),'Lean_output_sha256':sha(BASE+'_lean_output.txt'),
        'Lean_receipt_sha256':sha(receipt_path)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args = parser.parse_args()
    result = controls()
    target = ROOT/(BASE+'_certificate.json')
    if args.write:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(target.read_text())==result,'JOINT_ADJOINT_SOURCE_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_NATIVE_JOINT_ADJOINT_SOURCE controls=%d mutants=%d native_heat_binding=OPEN'%
          (result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':
    main()
