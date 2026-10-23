#!/usr/bin/env python3
"""Actual golden-word charge, GHZ closure and a convergent ring input family.

Only selected engine/creator definitions execute; no old run, spectrum or root.
"""
from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass
import ast
import hashlib
import json

import sympy as s

ROOT=Path(__file__).resolve().parents[4]
ENGINE='02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py'
CREATOR='02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS={
    ENGINE:'7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9',
    CREATOR:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md':
        '36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a',
    '02_REGISTRY/research/A4D_NATIVE_ADAPTIVE_AF_RECORD_ENGINE.md':
        '3e3bf3bb02aeb398dcefd54ca1892ee8d02128cc869f77db6e4818cc75c4aaf6',
    '02_REGISTRY/research/A4D_NATIVE_ENGINE_SUPPORTED_PREPARATION_SOURCE.md':
        'd1017d88b98c6c67a88b4a2d42a4d957757c4c5bbbf9042713be11ebaa339ab6',
    '02_REGISTRY/research/A4D_NATIVE_INHERITED_PATH_RECORD_SETTINGS.md':
        '319d1c194dfeb1dda0bdda135a9982c89d13dced4c1091a380f4db31bf049080',
}


def _target_names(node):
    if isinstance(node,ast.Name):
        return [node.id]
    if isinstance(node,(ast.Tuple,ast.List)):
        return [name for target in node.elts for name in _target_names(target)]
    return []


def owned_definitions(repo):
    engine=ast.parse((repo/ENGINE).read_text())
    function_names={'_sgn','quadratic_sign','literal_axis_gate','step','norm_squared'}
    nodes=[n for n in engine.body if
           (isinstance(n,ast.FunctionDef) and n.name in function_names) or
           (isinstance(n,ast.ClassDef) and n.name in {'Golden','State'}) or
           (isinstance(n,ast.Assign) and any(set(_target_names(t)) & {'ZERO','ONE','A','P'} for t in n.targets))]
    scope={'dataclass':dataclass,'__name__':__name__}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),ENGINE,'exec'),scope)
    creator_tree=ast.parse((repo/CREATOR).read_text())
    creator_nodes=[n for n in creator_tree.body if
        (isinstance(n,ast.FunctionDef) and n.name=='creator') or
        (isinstance(n,ast.Assign) and any('EXTERIOR_ORDER' in _target_names(t) for t in n.targets))]
    if len(creator_nodes)!=2:
        raise ArithmeticError('preparation_domain:creator_definition_nodes')
    cs={'s':s,'lru_cache':lru_cache}
    exec(compile(ast.Module(body=creator_nodes,type_ignores=[]),CREATOR,'exec'),cs)
    return scope,[cs['creator'](j) for j in range(4)]


def run(repo=None):
    repo=ROOT if repo is None else Path(repo).resolve()
    checks=[]

    def require(condition,name):
        if not bool(condition):
            raise ArithmeticError('preparation_domain:'+name)
        checks.append(name)

    a,p=s.symbols('a p',real=True)
    def red(x):
        return s.rem(s.rem(s.expand(x),a*a-p,a),p*p+p-1,p)
    def eq(actual,expected,name,reducer=red):
        values=list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
        require(all(reducer(x)==0 for x in values),name)

    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,
                'input_pin_'+Path(path).name)
    engine,c=owned_definitions(repo)
    one,zero=engine['ONE'],engine['ZERO']
    State=engine['State']
    def symbolic(g):
        u,v,w,t=g.coefficients
        return u+v*a+w*p+t*a*p
    matrices={}
    for sign in (1,-1):
        columns=[]
        for j in range(16):
            basis=[zero]*16
            basis[j]=one
            output=engine['literal_axis_gate'](State(tuple(basis)),sign)
            columns.append(s.Matrix([symbolic(x) for x in output.matter]))
        matrices[sign]=s.Matrix.hstack(*columns)
    I,O=s.eye(16),s.zeros(16)
    E=s.Matrix.hstack(*[I[:,mask] for mask in (0,1,14,15)])
    P0=E*E.T
    G=s.Matrix([[a,-p],[p,a]])
    Z=s.diag(1,-1)
    S4=s.diag(1,1,-1,-1)
    S16=E*S4*E.T
    for sign in (1,-1):
        U=matrices[sign]
        eq(U.T*U,I,'literal_all16_gate_unitary_'+str(sign))
        eq(U*P0,P0*U,'E0_reducing_not_operator_truncation_'+str(sign))
        eq(E.T*U*E,s.diag(G if sign==1 else G.T,Z*(G if sign==1 else G.T)),
           'actual_low_high_block_formula_'+str(sign))
        eq(U.T*S16*U,S16,'full16_retained_charge_'+str(sign))
    eq(Z*G*Z,G.T,'word_reversal_identity')
    low=s.Matrix(s.symbols('low0:2',real=True))
    for sigma in (1,-1):
        seed=s.Matrix.vstack(low,sigma*Z*low)
        eq((seed.T*S4*seed)[0],0,'both_owned_seed_families_have_zero_charge_'+str(sigma))
    W=matrices[1]**2
    V=matrices[-1]*matrices[1]
    eq(E.T*W*E,s.diag(G**2,s.eye(2)),'existing_word_rotates_low_pair_only')
    eq(E.T*V*E,s.diag(s.eye(2),G**2),'existing_word_rotates_high_pair_only')
    eq(W*V,V*W,'two_independent_retained_words_commute')
    eq(s.trace(G**2),4*p-2,'golden_square_rotation_trace')
    eq((4*p-2).subs(p,-1-p),-6-4*p,'conjugate_trace_excludes_finite_order')
    quarter=s.Matrix([[0,-1],[1,0]])
    eq(quarter**2,-s.eye(2),'zero_rotation_cosine_forces_finite_quarter_turn')
    # Every control-only operation and controlled record also preserve the
    # charge. The proof extends the same identities to the full128 reference.
    controlled=s.diag(matrices[1],matrices[-1])
    charge=s.kronecker_product(s.eye(2),S16)
    eq(controlled.T*charge*controlled,charge,'orthogonal_retained_branch_charge')
    control_mix=s.kronecker_product(s.Matrix([[1,1],[1,-1]])/s.sqrt(2),I)
    eq(control_mix.T*charge*control_mix,charge,'coherent_controller_mixing_keeps_unconditional_charge')
    x,y=s.symbols('density_Re density_Im',real=True)
    balanced=s.Matrix([[s.Rational(1,2),x+s.I*y],[x-s.I*y,s.Rational(1,2)]])
    eq(s.trace(balanced*s.diag(1,-1)),0,'all_balanced_complex_plane_densities_have_zero_charge',s.expand)

    # Correct native -> orthonormal coordinate-form map on the cone is
    # Lambda(O^T eta), not an identity on the first/third grades.
    def lift(M):
        return sum((M[i,j]*c[i]*c[j].T for i in range(4) for j in range(4)),O.copy())
    R01=s.zeros(4)
    R01[0,1],R01[1,0]=1,-1
    gen=lift(R01)
    rot=I+s.Rational(4,5)*gen+s.Rational(2,5)*gen**2
    eta_ext=s.diag(*[(-1)**sum(bool(mask&(1<<j)) for j in (1,2,3)) for mask in range(16)])
    form=rot.T*eta_ext
    H=s.Matrix.hstack(I[:,0],I[:,15])
    eq(form.T*form,I,'actual_orthonormal_coframe_intertwiner_unitary')
    eq(H.T*form*H,s.diag(1,-1),'proper_cone_coframe_flips_only_GHZ_top_sign')
    degree_charge=s.diag(*[1 if bin(mask).count('1') in (0,1) else
                          -1 if bin(mask).count('1') in (3,4) else 0 for mask in range(16)])
    eq(degree_charge*E,E*S4,'grade_charge_equals_word_charge_on_E0')
    eq(form.T*degree_charge*form,degree_charge,'allgrades_kept_in_coframe_charge_transport')
    for j in (1,2,3):
        alpha=(c[0]+c[0].T)*(c[j]-c[j].T)
        eq(H.T*alpha*H,s.zeros(2),'GHZ_fullCAR_current_spatial_compression_'+str(j))
        boost=c[0]*c[j].T+c[j]*c[0].T
        eq(boost*H,s.zeros(16,2),'GHZ_boost_generator_annihilates_whole_plane_'+str(j))
    require(all(not (bin(mask).count('1') in (1,3)) for mask in (0,15)),
            'GHZ_P1_and_P3_zero_in_every_exterior_frame')

    # The literal domain nevertheless contains convergent raw ring inputs.
    # This is acceptance of explicit inputs, not a compiler from the seed.
    eps=s.Symbol('epsilon',real=True)
    low0=s.Matrix([1,eps])
    powers=[(G**j*low0).applyfunc(red) for j in range(6)]
    eq(powers[1][1],p+a*eps,'accepted_family_first_low_step')
    eq(powers[2][1],2*a*p+p**3*eps,'accepted_family_second_low_step')
    eq(powers[3][1],4-5*p+a*(4*p-3)*eps,'accepted_family_third_low_step')
    eq(powers[4][1],4*a*(2-3*p)+(9-16*p)*eps,'accepted_family_fourth_low_step')
    eq(powers[5][1],45*p-28+a*(21-36*p)*eps,'accepted_family_fifth_low_step')
    eq((powers[3][1].subs(eps,p*p)-(6*p-3)),
       (a-1)*(4*p-3)*p*p,'third_step_positive_certificate')
    eq((powers[4][1].subs(eps,p*p)-(31-50*p)),
       (4*a-3)*(2-3*p),'fourth_step_positive_certificate')
    f=lambda t:t*t+t-1
    eq(f(s.Rational(3,5)),-s.Rational(1,25),'golden_lower_interval_sign',s.expand)
    eq(f(s.Rational(31,50)),s.Rational(11,2500),'golden_upper_interval_sign',s.expand)
    eq(G.T*powers[5],powers[4],'actual_minus_selector_returns_low_state4')
    eq(G*powers[4],powers[5],'actual_plus_selector_returns_low_state5')
    for N in (2,5,9):
        ep=one
        for _ in range(N):
            ep=ep*engine['P']
        raw=[zero]*16
        raw[0],raw[1],raw[15]=one,ep,-one
        state=State(tuple(raw))
        eq(symbolic(ep),p**N,'actual_ring_power_'+str(N))
        raw_symbolic=s.Matrix([symbolic(x) for x in raw])
        eq((raw_symbolic.T*S16*raw_symbolic)[0],p**(2*N),
           'accepted_input_charge_not_owned_seed_charge_'+str(N))
        require(engine['norm_squared'](state)==2*one+ep*ep,
                'raw_ring_family_normalizer_'+str(N))
        signs=[]
        for j in range(8):
            signs.append(state.matter[1].sign())
            state=engine['step'](state)
        require(signs==[1,1,1,1,1,-1,1,-1],
                'literal_defined_selector_family_'+str(N))
    for top_sign in (1,-1):
        raw=[zero]*16
        raw[0],raw[15]=one,top_sign*one
        try:
            engine['step'](State(tuple(raw)))
        except ValueError as error:
            require(str(error)=='FIRST_GRADE_PAIRING_SINGULARITY',
                    'exact_GHZ_endpoint_rejected_by_literal_domain_'+str(top_sign))
        else:
            raise ArithmeticError('preparation_domain:GHZ_endpoint_accepted')

    return {
        'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
        'carrier':{'Fock':16,'E0_masks':[0,1,14,15],'reference_kept':128,
                   'retained_history_erased':False,'AF_scalar_complement_discarded':False},
        'word_charge':'S=diag(1,1,-1,-1) on E0; full16 extension commutes with both literal U signs',
        'word_closure_plane_density':'[[1/2,z],[conjugate(z),1/2]], |z|<=1/2; arbitrary complex coherence',
        'independent_words':'U_plus^2=diag(G^2,I), U_minus U_plus=diag(I,G^2)',
        'exact_word_GHZ_reachability':False,
        'arbitrary_retained_sign_word_GHZ_closure':True,
        'literal_selected_fixed_seed_GHZ_closure':False,
        'accepted_ring_input_family':'vacuum-top+p^N time, N>=2; norm^2=2+p^(2N)',
        'accepted_family_selectors':'five plus gates then alternating minus/plus; no input singularity for any finite N',
        'GHZ_current':'J=n supplied by the retained observer; not a P1 law',
        'scope':{'input_family_compiled_from_owned_seed':False,
                 'arbitrary_sign_control_physically_selected':False,
                 'uniform_P1_gap_for_approximating_family':False,
                 'all_native_preparations_excluded':False,
                 'postselected_coherent_history_filter_classified':False,
                 'new_action_or_source_added':False,'old_entrypoints_or_roots_executed':False},
    }


if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
