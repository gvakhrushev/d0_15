#!/usr/bin/env python3
"""New bounded cone kernel/source-cokernel identities; no old entrypoint replay."""
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
MATRIX_SOURCE = '02_REGISTRY/research/sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py'
CREATOR_SOURCE = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
SOURCE_PINS = {
    MATRIX_SOURCE:'7bbf1589f3a32af381036df64f76d720ce14a9f2e502b3a1a6f43f5b5e776d58',
    CREATOR_SOURCE:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}


def _matrix_definitions_only(repo):
    """Extract inspected pure construction through a=assemble(), never run()."""
    module = ast.parse((repo/MATRIX_SOURCE).read_text())
    original = next(n for n in module.body if isinstance(n,ast.FunctionDef)
                    and n.name == 'run')
    body = []
    for node in original.body:
        if (isinstance(node,ast.For) and isinstance(node.target,ast.Tuple)
            and [getattr(t,'id',None) for t in node.target.elts] == ['path','digest']):
            continue  # Its old validation loop is not part of matrix construction.
        if isinstance(node,ast.FunctionDef) and node.name == 'require':
            continue
        if (isinstance(node,ast.Expr) and isinstance(node.value,ast.Call)
            and isinstance(node.value.func,ast.Name) and node.value.func.id == 'require'):
            continue
        if isinstance(node,ast.Return):
            raise ArithmeticError('matrix extraction crossed old result boundary')
        body.append(node)
        if (isinstance(node,ast.Assign)
            and any(isinstance(t,ast.Name) and t.id == 'a' for t in node.targets)):
            if not (isinstance(node.value,ast.Call) and
                    isinstance(node.value.func,ast.Name) and node.value.func.id == 'assemble'):
                raise ArithmeticError('unexpected matrix construction boundary')
            break
    else:
        raise ArithmeticError('matrix boundary absent')
    body.append(ast.parse('return a, shell, c, b').body[0])
    function = ast.FunctionDef(name='build_matrix_only',
        args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),
        body=body,decorator_list=[])
    scope = {'ROOT':repo,'PINS':{CREATOR_SOURCE:SOURCE_PINS[CREATOR_SOURCE]},
             's':s,'lru_cache':lru_cache,'ast':ast}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),
                 MATRIX_SOURCE,'exec'),scope)
    return scope['build_matrix_only']()


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = []

    def require(condition,name):
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    for path,digest in SOURCE_PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_'+Path(path).name)
    A,shell,c,b = _matrix_definitions_only(repo)
    A = s.SparseMatrix(A)
    I16,I64,I128 = s.eye(16),s.eye(64),s.eye(128)
    z16 = s.zeros(16)
    require(A == s.conjugate(A.T) and s.trace(A*A) == 52,
            'same_full128_true_adjoint_resonant_matrix')
    expected_shell = [tuple(sign if r == j else 0 for r in range(4))
                      for j in range(4) for sign in (-1,1)]
    require(shell == expected_shell,'all8_shell_momenta_full16_no_reference_removed')
    A01,A2 = A[:64,:64],A[64:96,64:96]
    P3 = s.diag(*([0]*96+[1]*32))
    require(A == s.diag(A01,A2,s.zeros(32)),
            'exact_axis01_axis2_axis3_reducing_blocks')
    A01sq,A2sq = A01*A01,A2*A2
    require(16*A01sq*A01sq-24*A01sq+I64 == s.zeros(64),
            'axis01_annihilator_16x4_minus24x2_plus1')
    require(8*A2sq == s.eye(32),'axis2_annihilator_8x2_minus1')
    inverse = s.diag(24*A01-16*A01*A01sq,8*A2,s.zeros(32))
    require(A*inverse == I128-P3 and inverse*A == I128-P3,
            'exact_inverse_on_all96_non_axis3_directions')
    Asq = A*A
    projector = I128-32*Asq+208*Asq*Asq-128*Asq*Asq*Asq
    require(projector == P3 and A*projector == s.zeros(128)
            and projector*projector == projector and s.trace(projector) == 32,
            'kernel_projector_I_minus32A2_plus208A4_minus128A6')
    # No eigenvalue catalogue is recomputed. These exact scalar factors suffice.
    x = s.symbols('x',real=True)
    require(s.expand((4*x*x-4*x-1)*(4*x*x+4*x-1)) == 16*x**4-24*x*x+1,
            'scalar_factorization_for_nonzero_spectral_gap')
    amin,cmax = (s.sqrt(2)-1)/2,(s.sqrt(2)+1)/2
    roots = [-cmax,-amin,amin,cmax]
    require(all(s.simplify(16*r**4-24*r*r+1) == 0 for r in roots)
            and amin > 0 and amin**2 < s.Rational(1,8),
            'all_nonzero_axis_eigenvalues_have_abs_at_least_sqrt2_minus1_over2')
    # Spectral variance: zero-atom mass p and the remaining atoms. The displayed
    # two-atom algebra checks the pairwise summand identity; the proof sums it.
    p,u,l1,l2 = s.symbols('p u l1 l2',real=True)
    v = 1-p-u
    variance = u*l1*l1+v*l2*l2-(u*l1+v*l2)**2
    pairwise = p*(u*l1*l1+v*l2*l2)+u*v*(l1-l2)**2
    require(s.expand(variance-pairwise) == 0,'spectral_variance_pairwise_identity')
    lower = s.simplify(s.Rational(1,4)*s.Rational(3,4)*amin**2)
    require(s.simplify(lower-(9-6*s.sqrt(2))/64) == 0 and lower > 0,
            'positive_uniform_source_balanced_amplitude_residual_bound')

    # Independent counterjet cokernel: p=-e0, original mask labels2 and4.
    gamma = [c[j]-b[j] for j in range(4)]
    Dp = -s.I*gamma[0]
    W = s.zeros(16)
    W[2,4] = W[4,2] = 1
    require(W == W.T and s.trace(W) == 0 and s.trace(W*A[:16,:16]) == 2,
            'real_tracefree_witness_W_E24_plus_E42_detects_fixed_A')
    torsion_rows = []
    for aa in range(4):
        for bb in range(4):
            for cc in range(bb+1,4):
                Q = c[bb]*c[cc]*b[aa]
                Z = Q+Q.T
                # Actual d=d_dR-Q convention, hence delta D=-Z.
                response = -(Dp*Z+Z*Dp)
                torsion_rows.append(s.trace(W*response))
    require(len(torsion_rows) == 24 and all(r == 0 for r in torsion_rows),
            'W_annihilates_all24_actual_real_Cartan_torsion_counterjets')
    metric_responses = []
    for aa in range(4):
        for bb in range(aa,4):
            Gdot = s.zeros(4)
            Gdot[aa,bb] = Gdot[bb,aa] = 1
            Ddot = s.I*sum((gamma[j]*Gdot[0,j] for j in range(4)),z16)/2
            response = Dp*Ddot+Ddot*Dp
            metric_responses.append(response == -Gdot[0,0]*I16 and
                                    s.trace(W*response) == 0)
    require(len(metric_responses) == 10 and all(metric_responses),
            'all10_constant_metric_rows_scalar_and_annihilated_by_W')
    frame_responses = []
    for aa in range(4):
        for bb in range(aa+1,4):
            K = c[aa]*b[bb]-c[bb]*b[aa]
            Ddot = K*Dp-Dp*K
            frame_responses.append(Dp*Ddot+Ddot*Dp == z16)
    require(len(frame_responses) == 6 and all(frame_responses),
            'all6_constant_positive_frame_GammaK_responses_zero')
    dpoint = -s.I*c[0]
    require(I16*dpoint-dpoint*I16 == z16,
            'constant_measure_whitening_commutator_zero')
    require(s.trace(W*(A[:16,:16]-s.symbols('epsilon',real=True)*I16)) == 2,
            'hostile_scalar_R1_subtraction_cannot_remove_W_residual')
    return {
        'status':'PASS','exact_check_groups':len(checks),'checks':checks,
        'source_pins':SOURCE_PINS,'full_Fock_components':16,
        'first_shell_dimension':128,'reference_dimension':128,
        'old_entrypoints_executed':False,'full_eigenspectrum_recomputed':False,
        'matrix_construction':'AST pure prefix through a=assemble(); no run() call or old checks',
        'axis_block_dimensions':[64,32,32],
        'axis01_annihilator':'16 A01^4-24 A01^2+I64=0',
        'axis2_annihilator':'8 A2^2-I32=0',
        'nonkernel_inverse':'diag(24 A01-16 A01^3,8 A2,0_32)',
        'kernel_projector':'I128-32 A^2+208 A^4-128 A^6=diag(0_96,I_32)',
        'A_rank':96,'A_nullity':32,
        'kernel_momentum_support':['-e3 tensor full16','+e3 tensor full16'],
        'source_balance_premise':'all four axis-pair masses=1/4; independent leading-source proof owned separately',
        'one_eigenvalue_axis3_mass':'1 for epsilon1=0; 0 for epsilon1!=0; never required1/4',
        'no_source_balanced_preparation_scope':'any normalized PSD rho supported on ONE A eigenvalue, any rank, fixed exact-LC geometry and first jets',
        'uniform_residual_squared_lower_bound':'(9-6 sqrt(2))/(64 s^4)>0',
        'uniform_residual_proof':'spectral zero mass1/4, other mass3/4; zero/nonzero pair variance >=(1/4)(3/4) amin^2, amin=(sqrt2-1)/(2s^2)',
        'counterjet_witness':{
            'operator':'W=E24+E42, zero-based native mask labels, momentum p=-e0',
            'Tr_W_Ablock':'2/s^2','Tr_W_I':'0',
            'real_torsion_rows_annihilated':24,'metric_rows_annihilated':10,
            'positive_frame_rows_annihilated':6,'constant_measure_row':'0',
            'nonzero_Fourier_jet_rule':'coefficient frequency q maps p to p+q; q!=0 cannot contribute to this same-p diagonal',
            'faithful_extension_scope':'conditional on actual C1-controlled output(G,T,measure) and positive-isometric-frame jet parametrization; excludes faithful first amplitude even with such real smooth field counterjets',
            'partial_rank_arbitrary_counterjets':'NOT_DECIDED',
        },
        'not_proved':['general native joint branch nonexistence','physical preparation/admission',
                      'original fixed-g fixed-tau terminal or Einstein source equality'],
    }


if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
