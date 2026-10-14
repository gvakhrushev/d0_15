#!/usr/bin/env python3
"""Exact finite controls; all-time/all-L proofs remain explicitly analytic."""
# D0_CI_TIMEOUT_SECONDS=600
import argparse,hashlib,importlib.util,json,re,sys
import copy
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_correlated_current_transition'
PROOF='02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md'
INPUTS=[
    '02_REGISTRY/research/A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md',
    '02_REGISTRY/research/A4D_NATIVE_RECORDED_OBSERVER_PREPARATION.md',
    '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
    '02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation.py',
    '02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation_check.py',
    '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_check.py',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.lean',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_results.json',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_AUTONOMOUS_SCENE_RECORD.md',
    '02_REGISTRY/research/certificates/a4d_native_autonomous_record_program.py',
    '02_REGISTRY/research/certificates/a4d_native_autonomous_record_program_check.py',
    '02_REGISTRY/research/certificates/a4d_native_autonomous_record_program.lean',
    '02_REGISTRY/research/certificates/a4d_native_autonomous_record_program_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_autonomous_record_program_results.json',
    '02_REGISTRY/research/certificates/a4d_native_autonomous_record_program_certificate.json',
]
q=importlib.util.spec_from_file_location('correlated_program',ROOT/(BASE+'.py'))
P=importlib.util.module_from_spec(q);sys.modules[q.name]=P;q.loader.exec_module(P)
s,a,p,z=P.s,P.a,P.p,P.z
ENGINE='02_REGISTRY/research/certificates/a4d_native_closed_record_engine'
q=importlib.util.spec_from_file_location('closed_record_engine',ROOT/(ENGINE+'.py'))
E=importlib.util.module_from_spec(q);sys.modules[q.name]=E;q.loader.exec_module(E)
SCENE='02_REGISTRY/research/certificates/a4d_native_autonomous_record_program'
q=importlib.util.spec_from_file_location('autonomous_scene_program',ROOT/(SCENE+'.py'))
SP=importlib.util.module_from_spec(q);sys.modules[q.name]=SP;q.loader.exec_module(SP)

def engine_expr(value):
    u,v,w,t=value.coefficients
    return u+v*a+w*p+t*a*p

def engine_vector(state):
    return s.Matrix([engine_expr(value) for value in state.matter])

def engine_gate(sign):
    columns=[]
    for i in range(16):
        basis=[E.ZERO]*16;basis[i]=E.ONE
        columns.append(engine_vector(E.literal_axis_gate(E.State(tuple(basis)),sign)))
    return s.Matrix.hstack(*columns)

def scene_vector(state):
    return s.Matrix([engine_expr(value) for value in state.coordinates])

def scene_gate():
    columns=[]
    for i in range(64):
        basis=[SP.E.ZERO]*64;basis[i]=SP.E.ONE
        columns.append(scene_vector(SP.step(SP.ProgramState(tuple(basis)))))
    return s.Matrix.hstack(*columns)

def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def closure(paths):
    found=set();todo=list(paths)
    while todo:
        f=todo.pop()
        if f in found:continue
        found.add(f)
        if f.endswith('.lean'):
            for line in (ROOT/f).read_text().splitlines():
                if line.startswith('import '):
                    todo.extend('03_FORMALIZATION/'+v.replace('.','/')+'.lean'
                                for v in line.split()[1:] if v.startswith('D0.'))
    return sorted(found)

def parsed_axioms(output):
    result={name:[v.strip() for v in body.split(',') if v.strip()]
        for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output,re.S)}
    for name in re.findall(r"'([^']+)' does not depend on any axioms",output):result[name]=[]
    return result

def valid_Lean_structure(lean,output,capsule):
    axioms=parsed_axioms(output)
    requests=set(re.findall(r'^#print axioms (\S+)',capsule,re.M))
    checks=set(re.findall(r'^#check (\S+)',capsule,re.M))
    prints=set(re.findall(r'^#print (?!axioms\b)(\S+)',capsule,re.M))
    return (axioms==lean['axioms'] and set(axioms)==set(lean['declarations'])==requests
        and checks==set(lean['diagnostic_checks']) and prints==set(lean['diagnostic_prints'])
        and all(set(v)<=set(['propext','Classical.choice','Quot.sound']) for v in axioms.values())
        and all(re.search(r'^'+re.escape(name)+r'(?:\.\{[^}]*\})?(?:\s|:)',output,re.M)
                for name in checks)
        and all(('theorem '+name+' ') in output or ('def '+name+' ') in output for name in prints))

def audit_runtime_objects(lean):
    """Strict original-machine audit, deliberately separate from portable replay."""
    for f,digest in lean['actual_import_olean_sha256'].items():
        assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==digest,f
    for f,digest in lean['original_cache_olean_sha256'].items():
        assert hashlib.sha256((Path(lean['actual_cwd'])/f).read_bytes()).hexdigest()==digest,f
    assert hashlib.sha256(Path(lean['actual_command'][0]).read_bytes()).hexdigest()==lean['compiler_binary_sha256']

def controls(receipt=True):
    checks=[];mutants=[]
    def zero(v):
        return all(P.red(t)==0 for t in (v.todok().values() if isinstance(v,s.MatrixBase) else [v]))
    def check(name,v):
        assert bool(v),name;checks.append(name)
    def eq(name,v):check(name,zero(v))
    def reject(name,v):
        check('REJECT_'+name,not v);mutants.append(name)

    c,beta,gamma,alpha=P.car_operators()
    for i,j in product(range(4),repeat=2):
        eq('native_CAR_create_'+str((i,j)),c[i]*c[j]+c[j]*c[i])
        eq('native_CAR_annihilate_'+str((i,j)),c[i].T*c[j].T+c[j].T*c[i].T)
        eq('native_CAR_mixed_'+str((i,j)),c[i]*c[j].T+c[j].T*c[i]-int(i==j)*P.I16)
    for i,j in product(range(3),repeat=2):
        eq('full_current_Clifford_'+str((i,j)),alpha[i]*alpha[j]+alpha[j]*alpha[i]-2*int(i==j)*P.I16)
    for i in range(3):
        eq('full_current_selfadjoint_'+str(i),alpha[i]-alpha[i].T)
        eq('wrong_Euclidean_gamma_skew_'+str(i),beta*(c[i+1]+c[i+1].T)+(beta*(c[i+1]+c[i+1].T)).T)
    U,B,R=P.orbit_data();Uc=P.mat(R.T*U*R);Ac=P.mat(R.T*alpha[0]*R)
    eq('native_fullstep_all16',U-P.C.record(P.I4,P.I4[:,0])[0])
    Uminus=P.C.record(P.I4,-P.I4[:,0])[0]
    Ugplus,Ugminus=engine_gate(1),engine_gate(-1)
    eq('closed_engine_gate_plus_is_actual_native_fullstep',Ugplus-U)
    eq('closed_engine_gate_minus_is_actual_native_fullstep',Ugminus-Uminus)
    eq('closed_engine_plus_gate_orthogonal',Ugplus.T*Ugplus-P.I16)
    eq('closed_engine_minus_gate_orthogonal',Ugminus.T*Ugminus-P.I16)
    S=P.I16[:,[0,1,14,15]];PS=S*S.T;Sperp=P.I16-PS
    for sign,gate in [('plus',Ugplus),('minus',Ugminus)]:
        eq('closed_engine_'+sign+'_preserves_current_null_sector',Sperp*gate*S)
        eq('closed_engine_'+sign+'_preserves_sector_complement',PS*gate*Sperp)
    eq('closed_engine_positive_first_pair_is_Lean_lowerStep',
       (S.T*Ugplus*S).extract([0,1],[0,1])-s.Matrix([[a,-p],[p,a]]))
    eq('closed_engine_negative_first_pair_is_Lean_lowerStep',
       (S.T*Ugminus*S).extract([0,1],[0,1])-s.Matrix([[a,p],[-p,a]]))
    for i in range(3):
        eq('closed_engine_sector_spatial_CAR_compression_'+str(i),S.T*alpha[i]*S)
    sx,sy,sb,sc=s.symbols('engine_sx engine_sy engine_sb engine_sc',real=True)
    sector_state=S*s.Matrix([sx,sy,sb,sc])
    eq('closed_engine_sector_full_current_all_states',
       P.current(P.I4,sector_state)-P.I4[:,0])
    eq('closed_engine_sector_current_observer_pairing',
       P.observer_pairing(P.ETA,P.I4[:,0])-P.I4)
    engine_seed=E.seed()
    eq('closed_engine_seed_in_current_null_sector',
       engine_vector(engine_seed)-(P.I16[:,1]+P.I16[:,15]))
    eq('closed_engine_seed_first_pair_is_Lean_initial_value',
       engine_vector(engine_seed).extract([0,1],[0])-s.Matrix([0,1]))
    engine_state=engine_seed
    for tick in range(8):
        eq('closed_engine_finite_orbit_current_'+str(tick),
           P.current(P.I4,engine_vector(engine_state))-P.I4[:,0])
        if tick<7:engine_state=E.step(engine_state)
    # The source-active curve of section 6 occupies masks 0,14,3,13.
    # Positive rescaling removes the blank-code sqrt(2) normalization while
    # keeping its normalized full CAR current unchanged.
    source_state=[E.ZERO]*16
    source_state[0]=source_state[14]=E.A
    source_state[3]=source_state[13]=E.P
    source_state=E.State(tuple(source_state))
    source_vector=engine_vector(source_state)
    reject('SOURCE_ACTIVE_GOLDEN_STATE_LIES_IN_CLOSED_ENGINE_SECTOR',
           zero(S*S.T*source_vector-source_vector))
    try:
        E.step(source_state)
    except ValueError as exc:
        check('REJECT_CLOSED_ENGINE_ACCEPTS_SOURCE_ACTIVE_GOLDEN_STATE',
              str(exc)=='OUTSIDE_CERTIFIED_COLLINEAR_EXECUTOR')
        mutants.append('CLOSED_ENGINE_ACCEPTS_SOURCE_ACTIVE_GOLDEN_STATE')
    else:
        raise AssertionError('CLOSED_ENGINE_ACCEPTS_SOURCE_ACTIVE_GOLDEN_STATE')
    eq('source_active_golden_state_has_zero_engine_first_grade',source_vector[1])
    eq('source_active_golden_state_is_outside_engine_guard',source_vector[3]-p)
    eq('source_active_golden_fullstep_current',
       P.current(P.I4,U*source_vector)-s.Matrix([1,2*a*p,0,0]))
    # The already owned scene word is a fixed 64-dimensional executor,
    # repeated on all 359 native edge-reversal pairs.
    Wscene=scene_gate()
    controller_sector=[(c<<5)|(f<<4)|mask for c in range(2) for f in range(2)
                       for mask in (0,1,14,15)]
    Vscene=s.eye(64)[:,controller_sector];Pscene=Vscene*Vscene.T
    scene_perp=s.eye(64)-Pscene
    eq('autonomous_scene_actual_word_orthogonal',Wscene.T*Wscene-s.eye(64))
    eq('autonomous_scene_word_preserves_current_null_sector',scene_perp*Wscene*Vscene)
    eq('autonomous_scene_word_preserves_sector_complement',Pscene*Wscene*scene_perp)
    reject('AUTONOMOUS_SCENE_WORD_LEAVES_CURRENT_NULL_SECTOR',
           not zero(scene_perp*Wscene*Vscene))
    scene_seed=scene_vector(SP.seed(both_orientations=True))
    eq('autonomous_scene_seed_in_current_null_sector',scene_perp*scene_seed)
    for i in range(3):
        scene_alpha=s.kronecker_product(s.eye(4),alpha[i])
        eq('autonomous_scene_sector_current_compression_'+str(i),
           Vscene.T*scene_alpha*Vscene)
    check('autonomous_scene_all_718_history_coordinates',
          len(SP.SCENE_EDGES)==718 and len(SP.BASE_EDGES)==359
          and len(SP.scene_seed())==359)
    eq('whole_blank_code_isometry',B.T*B-s.eye(2))
    eq('whole_blank_code_actual_blank',P.P.full_tuple()[2]*B-B)
    eq('eightmask_space_invariant',U*R-R*Uc)
    eq('eightmask_space_orthonormal',R.T*R-s.eye(8))
    eq('whole_current_alpha1_reduces_eightmask',alpha[0]*R-R*Ac)
    eq('whole_current_two_tick_commutant',Uc**2*Ac-Ac*Uc**2)
    for i in (1,2):eq('whole_current_other_spatial_compression_'+str(i),R.T*alpha[i]*R)
    eq('whole_even_current_input',B.T*alpha[0]*B)
    eq('whole_odd_current_input',B.T*U.T*alpha[0]*U*B-s.Matrix([[0,1],[1,0]]))
    x,y=s.symbols('x y',real=True)
    J0=P.current(P.I4,B*s.Matrix([a,p]))
    J1=P.current(P.I4,U*B*s.Matrix([a,p]))
    eq('golden_full_current_even',J0-P.I4[:,0])
    eq('golden_full_current_odd',J1-s.Matrix([1,2*a*p,0,0]))
    eq('golden_current_norm_and_feedback',(J1.T*P.ETA*J1)[0]-p**6)
    reject('FULL_CURRENT_IS_OLD_P1_TOP_CHART',not zero(P.C.first(B*s.Matrix([a,p]))) and not zero((B*s.Matrix([a,p]))[15]))
    null=(P.I16[:,0]+P.I16[:,3])/s.sqrt(2)
    nullJ=P.current(P.I4,null)
    eq('actual_current_null_boundary',nullJ.T*P.ETA*nullJ)
    reject('ALL_NONZERO_MATTER_IS_TIMELIKE',not zero(nullJ.T*P.ETA*nullJ))

    # Proper spatial covariance fails for the old tensor marginal, succeeds for full CAR.
    rot=P.I4.copy();rot[1,1]=rot[3,3]=0;rot[1,3]=1;rot[3,1]=-1
    extE=P.C.ext(rot)
    m=B*s.Matrix([a,p]);oldbasis=P.C.B0
    T=s.Matrix([[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]])/s.sqrt(2)
    literalbasis=oldbasis*s.kronecker_product(T.T,s.eye(4))
    def marginal(v):return P.P.system_marginal(s.Matrix(4,4,list(literalbasis.T*v)))
    sigma=marginal(m)
    eq('old_marginal_golden_weights',sigma-s.diag(p,p**2))
    eq('old_marginal_rotation_invariant',marginal(extE*m)-sigma)
    oldh=P.P.pauli_positive_pairing(sigma)
    reject('OLD_PAULI_ROLE_READING_IS_SPATIALLY_COVARIANT',zero(oldh-rot*oldh*rot.T))
    eq('full_CAR_rotation_covariance',P.current(P.I4,extE*U*m)-rot*J1)
    reject('EUCLIDEAN_GAMMA_PRODUCT_IS_THIS_CURRENT',zero(((U*m).T*beta*(c[1]+c[1].T)*(U*m))[0]-J1[1]))
    for i in range(3):eq('spatial_CAR_operator_covariance_'+str(i),extE.T*alpha[i]*extE-sum((rot[i+1,j+1]*alpha[j] for j in range(3)),s.zeros(16)))

    for index,F in enumerate([s.diag(2,s.Rational(1,2),1,1),
            s.Matrix([[1,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,0,1]]),
            s.Matrix([[s.Rational(5,4),s.Rational(3,4),0,0],[s.Rational(3,4),s.Rational(5,4),0,0],[0,0,1,0],[0,0,0,1]])]):
        mf=P.C.ext(F)*U*m
        jf=P.current(F,mf);qf=F*P.ETA*F.T
        eq('actual_nonrest_full_current_'+str(index),jf-F*J1)
        eq('actual_nonrest_observer_pairing_'+str(index),P.observer_pairing(qf,jf)-F.inv().T*P.observer_pairing(P.ETA,J1)*F.inv())

    # Arbitrary complex chart Gram identity; no sample-state extrapolation.
    xx,yy,tt,zz,uu,ww,vv,kk=s.symbols('xx yy tt zz uu ww vv kk',real=True)
    Gram=s.Matrix([[xx,yy+s.I*tt],[yy-s.I*tt,zz]])
    b=s.Matrix([uu+s.I*ww,vv+s.I*kk]);hs=P.even_chart_sequence(Gram,b)
    c1,c2=164-264*p,1366-2208*p
    eq('all_Hermitian_chart_eight_tick_annihilator',hs[4]+c1*hs[3]+c2*hs[2]+c1*hs[1]+hs[0])
    eq('golden_cosine_cube',(4*(p**3)**3-3*p**3)-(130*p-81))
    for value,expected in [(s.Rational(41,66),s.Rational(31,4356)),(s.Rational(683,1104),s.Rational(1705,1218816))]:
        eq('positive_coefficient_endpoint_'+str(value),value*value+value-1-expected)
        check('positive_coefficient_endpoint_sign_'+str(value),expected>0)
    eq('chart_even_zero_row_transfer',(s.Matrix([[a,-p],[p,a]])**2)[0,1]+2*a*p)
    V=s.Matrix([[1,0],[0,0],[0,1]])
    eq('growing_archive_actual_isometry',V.T*V-s.eye(2))
    Gm=s.Matrix([[1,2],[3,4],[5,6],[7,8]])
    eq('growing_archive_full_Gram_retained',(Gm*V.T)*(Gm*V.T).T-Gm*Gm.T)
    badV=2*V
    reject('AMPLIFYING_ARCHIVE_IS_AN_ISOMETRY',badV.T*badV==s.eye(2))

    t=s.symbols('t',real=True);xy=P.preparation_curve(t);mt=U*B*xy
    norm=P.red((mt.T*mt)[0]);rt=P.red(2*xy[0]*xy[1]);r0=P.red(rt.subs(t,0));rp=P.red(s.diff(rt,t).subs(t,0))
    eq('actual_full_input_curve_norm',norm-1)
    eq('actual_current_curve_r_at_zero',r0-2*a*p)
    eq('actual_current_curve_r_derivative',rp-4*p**3)
    eq('actual_current_curve_in_all16',P.current(P.I4,mt)-s.Matrix([1,rt,0,0]))
    source_S=PS*mt;source_perp=Sperp*mt
    for i in range(3):
        eq('source_curve_S_self_current_'+str(i),(source_S.T*alpha[i]*source_S)[0])
        eq('source_curve_complement_self_current_'+str(i),
           (source_perp.T*alpha[i]*source_perp)[0])
        eq('source_curve_current_is_cross_sector_'+str(i),
           2*(source_S.T*alpha[i]*source_perp)[0]-(rt if i==0 else 0))
    reject('GOLDEN_SOURCE_CROSS_SECTOR_CURRENT_VANISHES',
           zero(2*(source_S.T*alpha[0]*source_perp)[0].subs(t,0)))
    W=P.I16;v=U*m;dv=P.mat(s.diff(mt,t).subs(t,0));dr=2*(dv.T*(alpha[0]-r0*P.I16)*v)[0]
    eq('current_normalized_genuine_jet',dr-rp)
    scaled=(1+t)*v
    eq('normalized_current_scale_null',s.diff(P.current(P.I4,scaled)[1],t).subs(t,0))
    reject('OMIT_CURRENT_DENOMINATOR_JET',zero(2*(v.T*alpha[0]*v)[0]))
    ell=s.Rational(7719,80008)
    eq('timelike_curve_exact_lower_constant',ell-(s.Rational(9999,8)-285)/10001)
    check('timelike_curve_lower_constant_positive',ell>0)
    for value in [s.Rational(617,1000),s.Rational(619,1000)]:
        check('golden_tight_root_bracket_'+str(value),(value**2+value-1<0)==(value==s.Rational(617,1000)))
    check('amplitude_tight_lower',s.Rational(785,1000)**2<s.Rational(617,1000))
    check('amplitude_tight_upper',s.Rational(787,1000)**2>s.Rational(619,1000))
    lo=2*s.Rational(785,1000)*s.Rational(617,1000)
    hi=2*s.Rational(787,1000)*s.Rational(619,1000)
    check('observer_K_lower_60',(1+lo)/(1-lo)>60)
    check('observer_K_upper_80',(1+hi)/(1-hi)<80)

    h=P.observer_pairing(P.ETA,s.Matrix([1,rt,0,0]));h0=P.mat(h.subs(t,0));dh=P.mat(s.diff(h,t).subs(t,0))
    eq('full_observer_pairing_determinant',P.red(h.det())-1)
    eq('current_pairing_shape_trace',s.trace(h0.inv()*dh))
    reject('VARYING_CURRENT_HAS_ZERO_PAIRING_JET',zero(dh))
    # Actual constant-field lower operator, all sixteen components, exact modes.
    for mode in [(0,0,0,0),(1,1,0,0),(1,0,0,0),(1,3,2,1),(2,1,3,2),(3,3,1,2)]:
        zs=s.Matrix([4*(s.I**k-1) for k in mode])
        d=sum((zs[i]*c[i] for i in range(4)),s.zeros(16))
        wc=P.mat(P.C.ext(h0));wci=P.mat(P.C.ext(P.ETA*h0*P.ETA))
        eq('actual_weighted_inverse_'+str(mode),wci*wc-P.I16)
        low=P.mat(wci*s.conjugate(d).T*wc)
        actual=d+low;lam=P.red((s.conjugate(zs).T*h0*zs)[0])
        eq('actual_all16_stored_square_'+str(mode),actual*actual-lam*P.I16)
    Ur,Pr,wr,wri=P.rest_lorentz_record(h0,s.Matrix([1,r0,0,0])/p**3)
    eq('actual_current_record_isometry',Ur.T*wr*Ur-wr)
    eq('actual_current_record_cut_projection',Pr*Pr-Pr)
    eq('actual_current_record_cut_adjoint',Pr.T*wr-wr*Pr)
    U2=P.mat(Ur*Ur);U2adj=P.mat(wri*U2.T*wr)
    F2=P.mat(Pr*U2adj*(P.I16-Pr)*U2*Pr)
    eq('actual_full_two_tick_feedback_trace',s.trace(F2)-16*p**3)
    eq('actual_full_two_tick_feedback_polynomial',F2*F2-4*p**3*F2)
    eq('actual_two_site_feedback_multiplicity',s.trace(s.diag(F2,F2))-32*p**3)
    check('full_periodic_feedback_site_and_grade_count_L4',4*(4**4)+12*(4**4)==16*(4**4))

    bounds=P.fixed_beta_rational_bounds()
    check('uniform_heat_negative_margin',bounds['negative_margin']>bounds['claimed_margin'])
    eq('uniform_heat_final_source_denominator',2*3000*81-bounds['source_denominator'])
    check('uniform_heat_Gaussian_bracket_11',1+2*5==11)
    check('uniform_heat_partition_bracket_81',(1+2*4)**2==81)
    check('uniform_heat_off_diagonal_constant',8*16*11*12==16896)
    reject('DIAGONAL_SOFT_MODES_CAN_BE_DELETED',bounds['off_upper']>=bounds['diagonal_lower'])

    if receipt:
        lean=json.loads((ROOT/(BASE+'_lean_results.json')).read_text())
        check('Lean_real_compiler_exit',lean['compiler_exit_code']==0 and lean['status']=='PASS')
        check('Lean_capsule_sha',lean['capsule_sha256']==sha(BASE+'.lean'))
        check('Lean_output_sha',lean['output_sha256']==sha(BASE+'_lean_output.txt'))
        output=(ROOT/(BASE+'_lean_output.txt')).read_text()
        capsule=(ROOT/(BASE+'.lean')).read_text()
        check('Lean_no_placeholder',not re.search(r'\bsorry\b|\bwarning\b|\berror\b',output,re.I))
        check('Lean_actual_declarations_axioms_and_propositions',valid_Lean_structure(lean,output,capsule))
        for f,digest in lean['input_sha256'].items():check('Lean_input_'+f,sha(f)==digest)
        actual={f for f in closure([BASE+'.lean']) if f.startswith('03_FORMALIZATION/D0/')}
        modules={f[len('03_FORMALIZATION/'):-5].replace('/','.') for f in actual}
        check('Lean_exact_SOURCE_module_closure',modules==set(lean['cache_source_comparison'])==set(lean['current_overlay_reuse']))
        check('Lean_exact_SOURCE_pin_closure',set(lean['input_sha256'])==actual|{'03_FORMALIZATION/lean-toolchain','03_FORMALIZATION/lake-manifest.json'})
        prior=lean['verified_prior_receipt']
        check('Lean_verified_prior_receipt_pin',sha(prior['path'])==prior['sha256'])
        old=json.loads((ROOT/prior['path']).read_text())
        check('Lean_prior_real_compilation',old['compiler_exit_code']==0 and old['status']=='PASS')
        check('Lean_same_verified_module_objects',lean['current_overlay_reuse']==old['current_overlay_reuse'])
        check('Lean_same_verified_SOURCE_rebuilds',lean['source_overlay_rebuilds']==old['source_overlay_rebuilds'])
        check('Lean_same_runtime_resolution',lean['actual_environment']==old['actual_environment'])
        check('Lean_exact_archived_object_set',set(lean['actual_import_olean_sha256'])==
              set(old['actual_import_olean_sha256'])|set(lean['actual_direct_dependency_resolution']))
        check('Lean_same_original_cache_evidence',lean['original_cache_olean_sha256']==old['original_cache_olean_sha256']
              and lean['original_cache_unchanged'] and old['original_cache_unchanged'])
        check('Lean_same_verified_compiler_binary',lean['compiler_binary_sha256']==old['compiler_binary_sha256']
              and lean['actual_command'][0]==old['actual_command'][0])
        for module,entry in lean['current_overlay_reuse'].items():
            check('Lean_module_SOURCE_'+module,sha('03_FORMALIZATION/'+module.replace('.','/')+'.lean')==entry['source_sha256'])
            check('Lean_module_object_'+module,lean['actual_import_olean_sha256'][entry['overlay_olean']]==entry['olean_sha256'])
        for f,digest in lean['actual_import_olean_sha256'].items():
            check('Lean_actual_object_'+Path(f).stem,re.fullmatch('[0-9a-f]{64}',digest) is not None
                  and (f not in old['actual_import_olean_sha256'] or digest==old['actual_import_olean_sha256'][f]))
        for f,digest in lean['original_cache_olean_sha256'].items():
            check('Lean_original_cache_'+f,digest==old['original_cache_olean_sha256'][f])
        check('Lean_actual_binary_pin',re.fullmatch('[0-9a-f]{64}',lean['compiler_binary_sha256']) is not None)
        for dependency in lean['actual_direct_dependency_resolution']:
            check('Lean_actual_direct_resolution_'+dependency,dependency in lean['actual_import_olean_sha256'])
        bad=copy.deepcopy(lean);bad['axioms'][bad['declarations'][0]]=[]
        reject('OMIT_ACTUAL_LEAN_AXIOM_DEPENDENCIES',valid_Lean_structure(bad,output,capsule))
        bad=copy.deepcopy(lean);bad['declarations']=bad['declarations'][1:]
        reject('DROP_REAL_LEAN_DECLARATION',valid_Lean_structure(bad,output,capsule))
        bad=copy.deepcopy(lean);bad['diagnostic_checks']=bad['diagnostic_checks'][1:]
        reject('OMIT_REAL_DIAGNOSTIC_PROPOSITION',valid_Lean_structure(bad,output,capsule))
    paths=closure(INPUTS+[BASE+'.py',BASE+'.lean'])
    return dict(status='PASS',input_source_head='39dbaecfb6e1c316c25c6d1898711a74164559ea',
        proof=PROOF,proof_sha256=sha(PROOF),program_sha256=sha(BASE+'.py'),checker_sha256=sha(BASE+'_check.py'),
        input_sha256={f:sha(f) for f in paths},exact_controls=len(checks),checks=checks,
        executed_mathematical_mutants=mutants,analytic_scope=['complete stabilizer covariance obstruction',
        'arbitrary complex spectator-isometry eight-tick boundary','all-time full current component',
        'all-L fixed-beta heat bound','exact closed-engine-and-scene/current-source sector decoupling',
        'positive source current is a checked cross-sector CAR term'],
        cross_owner_scope='CLOSED_ENGINE_AND_AUTONOMOUS_SCENE_SEED_STAY_IN_CURRENT_NULL_SECTOR; POSITIVE_SOURCE_RESPONSE_IS_CROSS_SECTOR',
        source_current_decomposition='r_i=2*m_S^T*alpha_i*m_perp on the owned B curve; r1(0)=2ap and r1_prime(0)=4p^3',
        full_feedback_pencil='(1-4zp^3)^(4L^4)',
        retained_zero_feedback_directions='12L^4',physical_admission_source_Ward_stationarity_GR_closed=False)

if __name__=='__main__':
    q=argparse.ArgumentParser();q.add_argument('--write',action='store_true');q.add_argument('--math-only',action='store_true');q.add_argument('--runtime-check',action='store_true');args=q.parse_args()
    result=controls(not args.math_only)
    dest=ROOT/(BASE+'_certificate.json')
    if args.write:
        assert not args.math_only
        dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    elif not args.math_only:
        assert json.loads(dest.read_text())==result,'STALE_CERTIFICATE'
    if args.runtime_check:
        assert not args.math_only
        audit_runtime_objects(json.loads((ROOT/(BASE+'_lean_results.json')).read_text()))
        print('PASS_ORIGINAL_RUNTIME_OBJECT_AUDIT')
    print('PASS_CORRELATED_CURRENT_TRANSITION',f"controls={result['exact_controls']}",f"mutants={len(result['executed_mathematical_mutants'])}",'native_admission=OPEN')
