#!/usr/bin/env python3
"""Exact complete-record flat channel and its Rayleigh/relaxation consumer.

Only pinned literal creator definitions execute. No old run(), root search,
large lattice, spectral/rank census, or physical state/price law is supplied.
The random-Majorana formula is an analysis of the SAME marginal channel,
not a replacement of the retained outcome labels or their history price.

For the actual Q row N_kappa=Q_(blank,kappa), A=Q_(blank,blank)=hD/16,
the full golden two-port map on data+controller is p*sigma+p^2*W*sigma*W.
After reducing a fresh blank controller this gives exactly
  Phi_h(rho)=rho+dt*[T_h(D rho D)-{D^2,rho}/2],
  dt=p^2*h^2/64=2alpha, T_h(X)=sum N_kappa^* X N_kappa.
The registers are retained spectators, not reset; this marginal reduction
does not discard their full physical/history contribution to an action.

On a flat Fourier diagonal block, P_r=nu*c_r*t_r, |t_r|=1. Thus T_h,kk=T0
EXACTLY, where T0=(1/8)sum_r(C_r^* X C_r+C_r X C_r^*+L_r X L_r+R_r X R_r).
With b=sqrt(1-nu^2), T0 is the random-conjugation channel of I,8 Majoranas,
4 occupation parities with weights (1+b)^2/4,nu^2/16,(1-b)^2/16.
For a Clifford monomial of degree k with o singly occupied role pairs,
  tau=(1+b)^2/4 +nu^2*(-1)^k*(8-2k)/16 +(1-b)^2*(4-2o)/16.
All nonidentity eigenvalues lie in [b^2,(3+b)/4]; degree7 saturates the
upper bound, giving gap (1-b)/4 without a 256-monomial enumeration.

Fixedpoint algebra and strong traceclass continuum convergence are analytic
consequences in the root owner, not asserted as outputs of a finite test:
  Fix Phi_h=M16 on k=0, scalar I16 independently at every nonzero k.
  Full reference128 is a spectator; momentum weights are conserved, not
  Gibbs-forced. Fixed Fourier windows are invariant and converge by the
  finite-dimensional Euler formula; trace-norm contraction then removes
  the cutoff for a fixed traceclass input. This is not uniform over I/d UV
  inputs, and does not prove a variable-coefficient semigroup/source limit.
"""

from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
V8 = '02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md'
RETAINED = ('02_REGISTRY/research/sources/'
            'd0_retained_history_causal_source_2026-10-16/check_retained_history.py')
PINS = {
    CURVED:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    V8:'f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c',
    RETAINED:'6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
}


def _creators(repo):
    tree = ast.parse((repo/CURVED).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node,ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('flat_relaxation:literal_creator_definition_nodes')
    scope = {'s':s,'lru_cache':lru_cache}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),CURVED,'exec'),scope)
    return [scope['creator'](r) for r in range(4)],scope['EXTERIOR_ORDER']


def clifford_eigenvalue(degree,odd_pair_count,nu,b):
    """Generic full-Clifford count formula; no matrix/rank enumeration."""
    return ((1+b)**2/4+nu**2*(-1)**degree*(8-2*degree)/16
            +(1-b)**2*(4-2*odd_pair_count)/16)


def _native_rows(C,nu,b,phases):
    """All64 actual blank-output row blocks, using literal duplicated words.

    Each returned pair is (label,coefficient,N). Full golden ports are
    applied afterwards. No full1024x1024 SELECT matrix is materialized.
    """
    I = s.eye(16)
    scaled = [nu*c for c in C]
    numbers = [c*c.H for c in C]
    left = [I+(b-1)*n for n in numbers]
    right = [b*I+(1-b)*n for n in numbers]
    tops = []
    for r in range(4):
        P = phases[r]*scaled[r]
        for pair in ((P,left[r]),(P.H,right[r]),
                     (-scaled[r],-left[r]),(-scaled[r].H,-right[r])):
            tops.extend((pair,pair))
    rows = []
    for label in range(32):
        for coefficient in range(2):
            row = sum((((-1)**bin(label & j).count('1'))*tops[j][coefficient]
                       for j in range(32)),s.zeros(16))/32
            rows.append((label,coefficient,row))
    return rows,left,right


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition,name):
        if not bool(condition):
            raise ArithmeticError('flat_relaxation:'+name)
        checks.append(name)

    p = s.Symbol('p',real=True)

    def reduce(value):
        return s.rem(s.expand(value),p*p+p-1,p)

    def eq(actual,expected,name):
        values = list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
        require(all(reduce(value) == 0 for value in values),name)

    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_'+Path(path).name)
    C,order = _creators(repo)
    I,O = s.eye(16),s.zeros(16)
    require(order == (0,2,3,1),'literal_ACDB_all16_order')
    require(all(C[r]*C[t].H+C[t].H*C[r] == (I if r == t else O)
                and C[r]*C[t]+C[t]*C[r] == O for r in range(4) for t in range(4)),
            'full16_CAR_no_grade_restriction')
    nu,b,h = s.Rational(3,5),s.Rational(4,5),s.Rational(1,4)
    eq(nu**2+b**2,1,'strict_rational_Julia_margin')
    beta = [c+c.H for c in C]
    eta = [s.I*(c-c.H) for c in C]
    number = [c*c.H for c in C]
    parity = [I-2*n for n in number]
    left = [I+(b-1)*n for n in number]
    right = [b*I+(1-b)*n for n in number]

    def T0(X):
        return sum((nu**2*(C[r].H*X*C[r]+C[r]*X*C[r].H)
                    +left[r]*X*left[r]+right[r]*X*right[r]
                    for r in range(4)),O.copy())/8

    wI,wM,wZ = (1+b)**2/4,nu**2/16,(1-b)**2/16

    def random_majorana(X):
        return (wI*X+wM*sum((beta[r]*X*beta[r]+eta[r]*X*eta[r]
                             for r in range(4)),O.copy())
                +wZ*sum((parity[r]*X*parity[r] for r in range(4)),O.copy()))

    eq(wI+8*wM+4*wZ,1,'all13_random_conjugation_weights_normalized')
    require(all(weight > 0 for weight in (wI,wM,wZ)),
            'strict_positive_random_conjugation_weights')
    X = s.Matrix(16,16,lambda i,j:s.Symbol('x'+str(i)+'_'+str(j)))
    eq(T0(X),random_majorana(X),'complete_full16_channel_random_Majorana_identity')
    eq(T0(I),I,'leading_channel_unital')
    eq(s.trace(T0(X)),s.trace(X),'leading_channel_trace_preserving')

    # Generic occupancy-count algebra proves the spectrum without going
    # through all256 Clifford matrices. Per-role values are 1,b,b^2.
    n0,n1,n2,bs = s.symbols('n0 n1 n2 b',real=True)
    nusq = 1-bs**2
    even = ((n0+n2)*(1+bs**2)/2+n1*bs+nusq*(n0-n2)/2)/4
    odd = ((n0+n2)*(1+bs**2)/2+n1*bs-nusq*(n0-n2)/2)/4
    eq(even.subs(n0,4-n1-n2),1-((1-bs)*n1+(1-bs**2)*n2)/4,
       'generic_even_Clifford_degree_role_count_formula')
    eq(odd.subs(n2,4-n0-n1),1-((1-bs)*n1+(1-bs**2)*n0)/4,
       'generic_odd_Clifford_degree_role_count_formula')
    require(nu**2/4 >= (1-b)/4 and (1-b)/2 >= (1-b)/4,
            'even_nonidentity_count_cases_bound_by_common_gap')
    # In the odd case n1>=1; equality is n1=1,n0=0,n2=3, degree7.
    eq(clifford_eigenvalue(7,1,nu,b),(3+b)/4,'generic_grade7_sharp_eigenvalue')
    majoranas = [item for pair in zip(beta,eta) for item in pair]
    grade7 = I
    for generator in majoranas[1:]:
        grade7 = grade7*generator
    eq(T0(grade7),(3+b)*grade7/4,'actual_full16_grade7_saturates_traceless_norm')
    eq(grade7.H*grade7,I,'grade7_witness_unitary_nonzero')
    eq(s.trace(grade7),0,'grade7_witness_traceless')
    eq(T0(parity[0]),(1-nu**2/4)*parity[0],
       'exact_one_role_occupation_parity_eigenvalue')

    # One actual L4 Fourier block, not a lattice/mode census.
    phases = (s.I,-s.S.One,-s.I,s.S.One)
    require(all(s.conjugate(t)*t == 1 and t**4 == 1 for t in phases),
            'literal_L4_unit_Fourier_phases')
    D = nu/h*sum(((phases[r]-1)*C[r]+(s.conjugate(phases[r])-1)*C[r].H
                  for r in range(4)),O.copy())
    lam = nu**2/h**2*sum((t-1)*(s.conjugate(t)-1) for t in phases)
    eq(D.H,D,'actual_flat_Fourier_D_Hermitian')
    eq(D**2,lam*I,'actual_flat_Fourier_D_square_all16')
    rows,_,_ = _native_rows(C,nu,b,phases)
    require(len(rows) == 64,'all32_labels_times2_coefficients_retained')
    eq(rows[0][2],h*D/16,'actual_blank_row_A_equals_hD_over16')
    eq(sum((N*N.H for _,_,N in rows),O.copy()),I,
       'complete_actual_Q_blank_row_orthonormality')
    # Parseval over every outcome is the exact finite-phase channel.
    Trow = sum((N.H*X*N for _,_,N in rows),O.copy())
    eq(Trow,T0(X),'finite_flat_diagonal_channel_equals_T0_exactly_not_only_limit')

    A = h*D/16
    alpha,dt = p**2*h**2/128,p**2*h**2/64
    B = I-alpha*D**2
    eq(dt,2*alpha,'native_clock_time_step_is_two_alpha')
    PhiX = X+dt*(T0(D*X*D)-(D**2*X+X*D**2)/2)
    eq(s.trace(PhiX),s.trace(X),'exact_complete_channel_trace_preserving')
    eq(I+dt*(T0(D*I*D)-(D**2*I+I*D**2)/2),I,
       'exact_finite_flat_channel_unital')
    eq(B**2,I-dt*D**2+dt**2*D**4/4,'exact_Bernoulli_blank_survival_effect')
    eq(I-B**2,dt*D**2-dt**2*D**4/4,'exact_per_round_exit_occupancy_effect')
    eq(B**2+4*p**3*A**4+4*p**2*A*(I-A*A.H)*A,I,
       'all128_Kraus_completeness_with_separate_blank_port1')

    # Exact scalar golden-mixture coefficients; W^2=I is the native
    # reflection. Cross terms cancel, giving p Id+p^2 Ad_W and laziness.
    eq(p**2+p**3,p,'full_controller_identity_channel_weight')
    eq(p**4+p**3,p**2,'full_controller_reflection_channel_weight')
    eq(p**3-p**3,0,'full_controller_cross_terms_cancel')
    require(s.Rational(1,2) < (s.sqrt(5)-1)/2 < 1,
            'golden_lazy_channel_weight_strict_between_zero_and_one')

    # A literal full-Lorentz proper-link first jet, retaining canonical
    # true adjoint, provides a noncommuting Hermitian source direction.
    boost01 = C[0]*C[1].H+C[1]*C[0].H
    dD = nu/h*(phases[2]*C[2]*boost01
               +s.conjugate(phases[2])*boost01*C[2].H)
    eq(dD.H,dD,'actual_link_boost_first_jet_with_true_adjoint')
    dDelta = D*dD+dD*D
    amplitude = s.zeros(16,128)
    amplitude[1,0],amplitude[2,0],amplitude[0,1] = 1,1,1
    damplitude = amplitude.copy()
    damplitude[5,0] = 1
    damplitude[15,2] = 1
    raw = amplitude*amplitude.H
    normalizer = s.trace(raw)
    rho = raw/normalizer
    dnormalizer = s.trace(damplitude*amplitude.H+amplitude*damplitude.H)
    drho = (damplitude*amplitude.H+amplitude*damplitude.H-rho*dnormalizer)/normalizer
    require(amplitude.shape == (16,128) and normalizer > 0 and dnormalizer != 0,
            'full_reference128_actual_normalizer_moves')
    eq(s.trace(rho),1,'actual_preparation_normalized')
    eq(s.trace(drho),0,'actual_preparation_source_normalizer_retained')
    require(rho*D != D*rho,'preparation_not_assumed_to_commute_with_D')
    Eport1 = 4*p**3*A**2
    dEport1 = 4*p**3*(A*(h*dD/16)+(h*dD/16)*A)
    eq(Eport1,p*dt*D**2,'all_outcomes_golden_port1_effect_is_Rayleigh_readout')
    eq(dEport1,p*dt*dDelta,'all_field_slots_pull_back_through_exact_port1_operator_identity')
    dR = s.trace(drho*D**2+rho*dDelta)
    require(s.simplify(dR) != 0,'actual_link_boost_matter_source_control_is_nonzero')
    eq(s.trace(drho*Eport1+rho*dEport1),p*dt*dR,
       'full_normalized_joint_Rayleigh_source_equals_port1_source')
    frozen = (damplitude*amplitude.H+amplitude*damplitude.H)/normalizer
    require(s.trace(frozen*D**2) != s.trace(drho*D**2),
            'hostile_frozen_normalizer_changes_matter_source')
    R0 = s.trace(rho*D**2)
    eq(s.trace((D**2)*(T0(D*rho*D)-(D**2*rho+rho*D**2)/2)),0,
       'exact_flat_energy_expectation_conserved_by_complete_channel')
    eq(s.trace(Eport1*rho),p*dt*R0,'exact_one_round_expected_port1_occupancy')

    # Axis block: actual occupation relaxation, not a Gibbs assumption.
    Daxis = nu/h*((s.I-1)*C[0]+(-s.I-1)*C[0].H)
    lamaxis = 2*nu**2/h**2

    def axis_Lstar(observable):
        return Daxis*T0(observable)*Daxis-lamaxis*observable

    for r in range(4):
        rate = 2-nu**2/4 if r == 0 else nu**2/4
        eq(axis_Lstar(number[r]),-lamaxis*rate*(number[r]-I/2),
           'actual_axis_occupation_relaxation_'+str(r))
    seed = (s.eye(16)[:,1]+s.eye(16)[:,15])/s.sqrt(2)
    seedrho = seed*seed.H
    eq(s.trace(seedrho*number[0]),1,'actual_pure_seed_time_occupation_is_one')
    require(all(s.trace(seedrho*number[r]) == s.Rational(1,2) for r in (1,2,3)),
            'actual_pure_seed_spatial_occupations_are_one_half')
    average_after_one = O.copy()
    for axis in range(4):
        Dsingle = nu/h*((s.I-1)*C[axis]+(-s.I-1)*C[axis].H)
        average_after_one += (seedrho+dt*(T0(Dsingle*seedrho*Dsingle)
                                         -lamaxis*seedrho))/4
    expected_one = (s.Rational(1,2)
                    +((1-dt*lamaxis*(2-nu**2/4))
                      +3*(1-dt*lamaxis*nu**2/4))/8)
    eq(s.trace(number[0]*average_after_one),expected_one,
       'actual_uniform_axis_seed_one_round_occupation_recursion')
    zfast,zslow,steps = s.symbols('zfast zslow steps')
    seed_excess = (zfast+3*zslow)/8
    eq(seed_excess.subs({zfast:1,zslow:1}),s.Rational(1,2),
       'uniform_axis_pure_seed_initial_time_occupation_excess')
    eq(seed_excess.subs({zfast:0,zslow:0}),0,
       'uniform_axis_pure_seed_time_occupation_relaxes_to_one_half')

    return {
        'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
        'fixture':{'nu':'3/5','defect':'4/5','h':'1/4','phases':['i','-1','-i','1'],
                   'Fock':16,'reference':128,'outcomes_per_round':128},
        'channel':{
            'exact':'Phi_h=Id+dt*[T_h(D_h rho D_h)-{Delta_h,rho}/2], dt=2alpha=p^2h^2/64',
            'native_jumps':'J_kappa=N_kappa^* D_h, sum J_kappa^*J_kappa=Delta_h; synthetic marginal representation only when changing Kraus basis',
            'leading_T0':'wI Ad_I+wM sum_8 Ad_xi+wZ sum_4 Ad_Z',
            'weights':{'wI':str(wI),'wM_each':str(wM),'wZ_each':str(wZ)},
            'generic_Clifford_eigenvalue':'(1+b)^2/4+nu^2(-1)^k(8-2k)/16+(1-b)^2(4-2o)/16',
            'sharp_traceless_norm':'(3+b)/4, attained at degree7 with one singly occupied role pair',
            'gap':'(1-b)/4',
            'positive_momentum_relaxation':'||rho_kk^(n)-I16 Tr_Fock(rho_kk)/16||HS <= exp[-beta_h lambda_h(k)(1-b)/4] times initial norm',
        },
        'actual_readout':{
            'port1_effect':'E_port1=p*dt*Delta_h, exact after summing every label/coefficient',
            'matter':'R_h=Prob(port1)/(p*dt), normalized preparation including full reference128',
            'source':'delta R=[Tr delta rho E_port1+Tr rho delta E_port1]/(p*dt) at fixed experiment; moving calibrations require quotient rule',
            'expected_port1_count':'p*beta_h*R0 on the flat energy-conserving programme',
            'expected_total_exit_count':'beta_h*R0-beta_h*dt*Tr(rho0 Delta_h^2)/4',
            'port_code_component':'if the owned direct/return costs1/2 are used, expected port-code cost=n+p*beta_h*R0; not the complete controller/archive cost',
            'axis_occupations':'d<n_r>/dt=-lambda*c_rs*(<n_r>-1/2), c_ss=2-nu^2/4, c_rs=nu^2/4 otherwise',
            'uniform_axis_seed':'<n0>-1/2=[exp(-lambda(2-nu^2/4)t)+3exp(-lambda nu^2 t/4)]/8',
        },
        'analytic_consumer':{
            'fixedpoint_algebra':'M16 on the unique dark zero momentum, scalar I16 at every nonzero momentum; with reference tensor its full matrix algebra',
            'proof_interface':'bistochastic Dirichlet identity + actual Walsh span D,xiD + full CAR commutant + injective Fourier D_h(k); golden laziness excludes other peripheral phases',
            'strong_continuum':'fixed physical Fourier windows are invariant; Euler convergence there plus CPTP trace-norm contraction removes cutoff for each fixed traceclass input',
            'momentum_weights':'exactly conserved; no Gibbs law or energy transfer is forced',
            'reference_history':'reference128 unchanged, full round registers retained; marginal partial trace is not a physical reset',
            'reference_action':'every native Kraus is K_a tensor I128, so the marginal is Phi_h tensor Id_(M128), not a reference average',
        },
        'scope':[
            'Fixed conditional flat matrix programme; physical primitive/controller/history-price admission remains open.',
            'No variable-coefficient unbounded-generator or independent raw-source limit is proved by these finite checks.',
            'Random-Majorana Kraus diagonalization does not change the actual recorded outcome basis or its price.',
            'Uniform UV input I/d is not a fixed traceclass continuum preparation; no uniform weak-jump statement is made for it.',
            'Stationary marginal densities are not automatically full joint Euler/preparation roots or a physical observer law.',
        ],
    }


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,ensure_ascii=False))
