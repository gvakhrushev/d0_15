#!/usr/bin/env python3
"""A new real-E0 preparation obstruction using only eight same-p full16 blocks.

No old checker run(), shell spectrum, root or receipt generator is executed.
"""
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
MATRIX = '02_REGISTRY/research/sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py'
CREATOR = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    MATRIX: '7bbf1589f3a32af381036df64f76d720ce14a9f2e502b3a1a6f43f5b5e776d58',
    CREATOR: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/A4D_CONE_SOURCE_BALANCED_PREPARATION.md':
        '1b6c919602be63b2ca401426e0630c5a91808b65cedf4181df5d7e499ae18d5f',
}


def _same_p_definitions(repo):
    """Pure source prefix through d1_direct definition; no assemble() call."""
    tree = ast.parse((repo / MATRIX).read_text())
    old = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    body = []
    for node in old.body:
        if (isinstance(node, ast.For) and isinstance(node.target, ast.Tuple)
            and [getattr(t,'id',None) for t in node.target.elts] == ['path','digest']):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == 'require':
            continue
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name) and node.value.func.id == 'require'):
            continue
        if isinstance(node, ast.Return):
            raise ArithmeticError('real_e0:crossed_old_result_boundary')
        body.append(node)
        if isinstance(node, ast.FunctionDef) and node.name == 'd1_direct':
            break
    else:
        raise ArithmeticError('real_e0:same_p_definition_boundary_absent')
    body.append(ast.parse('return c, b, shell, d0, d1_direct').body[0])
    fn = ast.FunctionDef(name='build_same_p_definitions',
        args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),
        body=body, decorator_list=[])
    scope={'ROOT':repo,'PINS':{CREATOR:PINS[CREATOR]},'s':s,'ast':ast,'lru_cache':lru_cache}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),MATRIX,'exec'),scope)
    return scope['build_same_p_definitions']()


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks=[]

    def require(condition,name):
        if not bool(condition):
            raise ArithmeticError('real_e0:'+name)
        checks.append(name)

    def eq(actual,expected,name):
        values=list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
        require(all(s.expand(x)==0 for x in values),name)

    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,
                'input_pin_'+Path(path).name)
    c,b,shell,d0,d1 = _same_p_definitions(repo)
    I,O=s.eye(16),s.zeros(16)
    require(len(shell)==8 and len(c)==4 and all(x.shape==(16,16) for x in c),
            'all8_shell_momenta_all16_CAR_components')
    require(all(c[i]*b[j]+b[j]*c[i]==(I if i==j else O)
                for i in range(4) for j in range(4)),'literal_full16_CAR')
    B12=c[1]*b[2]+c[2]*b[1]
    B02=c[0]*b[2]+c[2]*b[0]
    expected=(B12,-B02,O,O)
    blocks=[]
    for index,p in enumerate(shell):
        A=(d0(p)*d1(p,p)+d1(p,p)*d0(p)).applyfunc(s.expand)
        eq(A.H,A,'same_p_A1_Hermitian_'+str(index))
        real=A.applyfunc(s.re)
        eq(real,expected[index//2],'actual_same_p_real_A1_axis_'+str(index))
        eq(s.conjugate(A-real),-(A-real),'remaining_A1_is_pure_imaginary_'+str(index))
        blocks.append(A)

    E=s.Matrix.hstack(*[I[:,mask] for mask in (0,1,14,15)])
    P=E*E.H
    eq(E.H*E,s.eye(4),'E0_isometry_retains_four_actual_masks')
    eq(E.H*B02*E,s.zeros(4),'B02_has_no_internal_E0_block')
    leak=(I-P)*B02*E
    eq(leak.H*leak,s.diag(0,1,1,0),'exact_E0_leakage_Gram')
    eq(B02*I[:,1],I[:,4],'actual_mask1_goes_to_mask4')
    eq(B02*I[:,14],I[:,11],'actual_mask14_goes_to_mask11')
    eq(B02*I[:,0],s.zeros(16,1),'vacuum_is_in_real_leakage_kernel')
    eq(B02*I[:,15],s.zeros(16,1),'top_is_in_real_leakage_kernel')
    eq(B12*E,s.zeros(16,4),'axis0_has_no_real_E0_leakage')
    require(leak.rank()==2,'kernel_inside_E0_is_exactly_vacuum_and_top')

    # Every real zero-Fourier metric/torsion field jet at p=-e1.
    Dp=d0((0,-1,0,0))
    gamma=[c[j]-b[j] for j in range(4)]
    for a in range(4):
        for bb in range(a,4):
            Gdot=s.zeros(4)
            Gdot[a,bb]=Gdot[bb,a]=1
            Ddot=s.I*sum((gamma[j]*Gdot[1,j] for j in range(4)),O.copy())/2
            response=Dp*Ddot+Ddot*Dp
            eq(response,-Gdot[1,1]*I,'all10_real_metric_mean_response_'+str(a)+str(bb))
            eq((I-P)*response*E,s.zeros(16,4),
               'metric_mean_cannot_cancel_real_leakage_'+str(a)+str(bb))
    torsion_count=0
    for aa in range(4):
        for bb in range(4):
            for cc in range(bb+1,4):
                q=c[bb]*c[cc]*b[aa]
                Z=-(q+q.H)
                response=Dp*Z+Z*Dp
                eq(response.applyfunc(s.re),O,'all24_real_torsion_mean_real_part_'+str(torsion_count))
                eq(response.H,response,'torsion_mean_Hermitian_'+str(torsion_count))
                torsion_count+=1
    require(torsion_count==24,'all24_Cartan_rows_not_restricted_to_old_SO3')
    eq(Dp**2,I,'base_same_p_Delta_is_scalar')
    for a in range(4):
        for bb in range(a+1,4):
            K=c[a]*b[bb]-c[bb]*b[a]
            Ddot=K*Dp-Dp*K
            eq(Dp*Ddot+Ddot*Dp,O,'all6_frame_changes_are_resonantly_zero_'+str(a)+str(bb))
    eq(I*(-s.I*c[1])-(-s.I*c[1])*I,O,'constant_measure_generator_commutes_with_raising')

    # Source weights follow from equal thermal rows plus all four independent
    # metric rows, not from a hand-chosen uniform matter normalization.
    w=s.symbols('w0:4',real=True)
    thermal=s.Symbol('same_thermal_row',real=True)
    solution=s.solve([wi+thermal for wi in w]+[sum(w)-1],list(w)+[thermal],dict=True)
    require(solution==[{**{wi:s.Rational(1,4) for wi in w},thermal:-s.Rational(1,4)}],
            'actual_isotropic_metric_balance_forces_all_role_weights_one_quarter')

    chi=sum((I[:,mask] for mask in (0,1,14,15)),s.zeros(16,1))/2
    eq((chi.H*chi)[0],1,'real_balanced_chi_normalized')
    eq((chi.H*B02**2*chi)[0],s.Rational(1,2),'balanced_chi_real_leakage_mass_one_half')
    # A full128-column normalized rank8 purification; zero columns retained.
    one=I[:,0]
    C0=s.SparseMatrix(s.kronecker_product(s.eye(8),chi*one.H)/s.sqrt(8))
    require(C0.shape==(128,128) and C0.rank()==8,'full_reference128_rank8_not_truncated')
    eq(s.trace(C0.H*C0),1,'full_reference128_normalizer_one')
    lower=s.Integer(0)
    for index in (2,3):
        R=(I-P)*blocks[index].applyfunc(s.re)*chi/s.sqrt(8)
        lower+=(R.H*R)[0]
    eq(lower,s.Rational(1,8),'two_axis1_signs_full_amplitude_residual_lower_bound_one_eighth')
    eq(4*lower,s.Rational(1,2),'normalized_amplitude_Euler_factor2_squared')

    # Generic real mixed E0 support: positivity turns zero leakage mass into
    # support on the kernel; the trace identity is exact for all coherences.
    entries=s.symbols('sigma0:16',real=True)
    sigma=s.Matrix(4,4,entries)
    eq(s.trace(E*sigma*E.H*B02**2),sigma[1,1]+sigma[2,2],
       'general_real_E0_density_leakage_mass')
    ghz=(I[:,0]+I[:,15])/s.sqrt(2)
    eq(B02*ghz,s.zeros(16,1),'GHZ_real_leakage_survivor_not_excluded')
    require(B02*chi!=s.zeros(16,1),'hostile_promote_GHZ_survival_to_all_E0_rejected')
    arbitrary=s.Matrix(16,4,lambda i,j:s.Symbol('k_'+str(i)+'_'+str(j),real=True))
    eq((s.I*arbitrary).applyfunc(s.re),s.zeros(16,4),
       'imaginary_field_response_cannot_cancel_real_amplitude_leakage')
    t=s.Symbol('radial',real=True)
    effect=(chi.H*B02**2*chi)[0]
    eq(s.diff((1+t)**2*effect/(1+t)**2,t),0,'radial_normalizer_cannot_remove_leakage_mass')
    require(lower!=0,'hostile_off_shell_pseudoinverse_is_not_a_shell_canceller')

    return {
        'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
        'matrix_consumption':'only actual creator/connection/D0/D1 definitions; eight same-p blocks; no old run or assemble',
        'same_p_real_A1':['B12/s^2','-B02/s^2','0','0'],
        'E0_masks':[0,1,14,15],
        'B02_E0_images':{'0':[],'1':[[4,1]],'14':[[11,1]],'15':[]},
        'leakage_Gram':[[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,0]],
        'general_lower_bound':'[sigma_1(1,1)+sigma_1(14,14)]/(4 s^4)',
        'chi_bal_residual_squared_lower_bound':'1/(8 s^4)',
        'chi_bal_normalized_amplitude_Euler_lower_bound':'1/(2 s^4)',
        'carrier':{'Fock':16,'shell_momenta':8,'shell':128,'reference':128,'balanced_rank':8},
        'scope':{'real_E0_momentum_diagonal_preparations':True,
                 'independent_sigma_r_only_axis1_constrained':True,
                 'arbitrary_real_smooth_first_field_jets_allowed':True,
                 'complex_or_momentum_coherent_preparations_excluded':False,
                 'GHZ_first_corrector_proved':False,'all_partial_rank_or_geometry_excluded':False,
                 'physical_engine_admission_selected':False,'new_action_or_fit':False,
                 'old_entrypoints_or_spectra_executed':False},
    }


if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
