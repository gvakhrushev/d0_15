#!/usr/bin/env python3
"""Critical forcing test on the SAME v10 operator, not a new installed action.

Exact algebra and outward-rounded interval for the inherited L=8 root box.
A local run does not recompile Lean or reprove the v10 root existence theorem.
The receipt is immutable by default. --write is an explicit initial issuance.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S
import mpmath as mp

HERE = Path(__file__).resolve().parent
P = S.Symbol('p', real=True)
REL = P**2 + P - 1
@lru_cache(maxsize=None)
def red(v):
    num, den = S.cancel(v).as_numer_denom()
    num = S.rem(S.expand(num), REL, P)
    den = S.rem(S.expand(den), REL, P)
    if den == 0:
        raise ZeroDivisionError('golden denominator')
    return S.rem(S.expand(num * S.invert(den, REL, P)), REL, P)
def mat(A):
    return A.applyfunc(red)

CHECKS = []
NEGATIVE = []
def check(name, value):
    if not bool(value):
        raise AssertionError(name)
    CHECKS.append(name)
def eq(name, value):
    vs = list(value) if isinstance(value, S.MatrixBase) else [value]
    check(name, all(red(v) == 0 for v in vs))
def reject(name, false_value):
    check('REJECT_' + name, not bool(false_value))
    NEGATIVE.append(name)

def math():
    c = red(P**3)
    s = 4*c
    x, h, e, t, kappa = S.symbols('x h e t kappa', real=True)
    f = x + c*x*x*(1-x)
    check('golden_coefficient_not_fitted', c == 2*P-1)
    eq('golden_probability_closure', c*c + s - 1)
    eq('same_vacuum', f.subs(x,0))
    eq('same_cutoff', f.subs(x,1)-1)
    eq('same_low_energy_calibration', S.diff(f,x).subs(x,0)-1)
    eq('positive_difference_factor', f-x-c*x*x*(1-x))
    eq('upper_bound_below_one', 1-f-(1-x)*(1-c*x*x))
    eq('strict_monotonicity_lower_factor', S.diff(f,x)-(1-c)-c*(1-x)*(3*x+1))
    eq('monotonicity_upper_factor', (1+c/3)-S.diff(f,x)-3*c*(x-S.Rational(1,3))**2)
    reject('only_linear_quadratic_in_state_observable', red(f-x)==0)

    # On the same three error records, these scores use only the error COUNT.
    scores0 = [S.Rational(n,3)/s for n in range(4)]
    scores1 = [red(S.Rational(n,3)/s + c*S.binomial(n,2)/(3*s*s)
                   -c*int(n==3)/(s**3)) for n in range(4)]
    expectation0 = sum(S.binomial(3,n)*(s*x)**n*(1-s*x)**(3-n)*scores0[n]
                       for n in range(4))
    expectation1 = sum(S.binomial(3,n)*(s*x)**n*(1-s*x)**(3-n)*scores1[n]
                       for n in range(4))
    eq('actual_count_readout_linear', expectation0-x)
    eq('actual_count_readout_polynomial', expectation1-f)
    # Exact positivity follows from 1/5<c<1/4 and s=4c; endpoint below.
    eq('score_increment_1', scores1[1]-1/(3*s))
    eq('score_increment_2', scores1[2]-scores1[1]-(1/(3*s)+c/(3*s*s)))
    eq('score_increment_3', scores1[3]-scores1[2]-c*(8*c-1)/(s**3))
    reject('same_source_from_same_error_records', red(scores1[2]-scores0[2])==0)

    # Literal two projections and the existing I-versus-V golden comparator.
    I = S.eye(6)
    Q = S.diag(S.Matrix([[S.Rational(3,5),-S.Rational(4,5)],
                        [S.Rational(4,5),S.Rational(3,5)]]),
               S.Matrix([[S.Rational(5,13),-S.Rational(12,13)],
                         [S.Rational(12,13),S.Rational(5,13)]]), S.eye(2))
    Pc = S.diag(1,0,1,0,0,0)
    Pr = Q.T*Pc*Q
    V = -(2*Pc-I)*(2*Pr-I)
    K = (Pc+Pr-I)**2
    Kf = K + c*(K*K-K**3)
    check('whole_loop_unitarity', V.T*V==I)
    check('whole_loop_defect', (I-V).T*(I-V)==4*K)
    check('commuting_loop_and_energy', V*K==K*V)
    check('every_original_state_retained', K.shape==(6,6) and Kf.shape==(6,6))
    eq('same_exact_cutoff_on_complement', Kf[4:,4:]-S.eye(2))
    reject('two_scores_same_operator', mat(Kf-K)==S.zeros(6))
    rho = S.ones(6,6)/6
    psi = S.ones(6,1)
    eq('both_readouts_quadratic_state_normalized',
       (psi.T*Kf*psi)[0]/(psi.T*psi)[0]-S.trace(rho*Kf))

    C0 = P*I + P*P*V
    C1 = V-I
    E = mat(c*C1.T*C1)
    eq('actual_golden_error_effect', E-s*K)
    eq('actual_golden_complete_instrument', C0.T*C0+E-I)
    def branch(X, bit):
        return mat(c*C1.T*X*C1 if bit else C0.T*X*C0)
    A0, A1 = S.zeros(6), S.zeros(6)
    for word in itertools.product((0,1), repeat=3):
        effect = I
        for bit in reversed(word):
            effect = branch(effect,bit)
        n = sum(word)
        eq('full_history_effect_'+''.join(map(str,word)),
           effect - E**n*(I-E)**(3-n))
        A0 += scores0[n]*effect
        A1 += scores1[n]*effect
    eq('full_coherent_instrument_score0', A0-K)
    eq('full_coherent_instrument_score1', A1-Kf)
    reject('omit_three_error_normalization',
       mat(A1+c*E**3/s**3-Kf)==S.zeros(6))

    # A genuine moving comparison; do not freeze the second projector.
    T = S.zeros(6); T[0,1]=1; T[1,0]=-1
    Qdot = Q*T
    Rdot = Qdot.T*Pc*Q+Q.T*Pc*Qdot
    Kdot = (Pc+Pr-I)*Rdot + Rdot*(Pc+Pr-I)
    Ldot = Kdot+c*(K*Kdot+Kdot*K-K*K*Kdot-K*Kdot*K-Kdot*K*K)
    reject('frozen_extra_readout_source', mat(Ldot-Kdot)==S.zeros(6))
    Qfield = Q*(S.eye(6)+t*T)  # correct first jet, not an exact finite-time unitary
    Rfield = Qfield.T*Pc*Qfield
    Kfield = (Pc+Rfield-I)**2
    Ffield = Kfield+c*(Kfield*Kfield-Kfield**3)
    eq('actual_nonfrozen_comparison_derivative', Ffield.diff(t).subs(t,0)-Ldot)
    # Noncommuting tangent: varying the rank-two plane rather than an eigenvalue only.
    T2 = S.zeros(6); T2[0,3]=1; T2[3,0]=-1
    R2=(Q*T2).T*Pc*Q+Q.T*Pc*(Q*T2)
    K2=(Pc+Pr-I)*R2+R2*(Pc+Pr-I)
    reject('general_tangent_commutes', K*K2==K2*K)
    dot2=K2+c*(K*K2+K2*K-K*K*K2-K*K2*K-K2*K*K)
    S0=S.Symbol('z',real=True)
    C=K+S0*K2
    eq('noncommuting_polynomial_Frechet',
       (C+c*(C*C-C**3)).diff(S0).subs(S0,0)-dot2)

    # Entire v10 refinement relation survives, not only a prepared subspace.
    J = S.eye(12)[:,:6]
    Kplus = J*K*J.T+S.eye(12)-J*J.T
    Fplus = Kplus+c*(Kplus*Kplus-Kplus**3)
    eq('exact_all_old_and_new_refinement', Fplus-J*Kf*J.T-(S.eye(12)-J*J.T))
    eq('refinement_intertwiner', Fplus*J-J*Kf)
    T3=S.zeros(12);T3[0,8]=1;T3[8,0]=-1
    Jdot=T3*J
    plusdot=Jdot*K*J.T+J*K*Jdot.T-Jdot*J.T-J*Jdot.T
    fdot=plusdot+c*(Kplus*plusdot+plusdot*Kplus-Kplus*Kplus*plusdot-
                    Kplus*plusdot*Kplus-plusdot*Kplus*Kplus)
    eq('moving_refinement_source',fdot*J+Fplus*Jdot-Jdot*Kf)
    reject('refinement_may_freeze_embedding',mat(fdot*J)==S.zeros(12,6))
    # Refuting singleton does not mean an arbitrary catalogue was introduced.
    for out in (K,Kf):
        eq('catalogue_relabel_invariant_'+str(out==K), Q.T*out*Q -
           ((Q.T*K*Q) if out==K else Q.T*K*Q+c*((Q.T*K*Q)**2-(Q.T*K*Q)**3)))

    delta = e + c*kappa*e**2-c*kappa**2*e**3
    diff = delta-e
    radial = S.diff(diff,e)*(-2*e)
    eq('complete_radial_difference',radial-(-4*c*kappa*e**2+6*c*kappa**2*e**3))
    normed = S.expand(radial.subs(kappa,h*h/256)/h**2)
    eq('normalized_exact_formula',normed-(-c*e**2/64+3*c*h*h*e**3/32768))
    limit=S.limit(normed,h,0)
    eq('normalization_survives_refinement',limit+c*e**2/64)
    reject('ordinary_small_error_is_normalized_small',limit==0)
    basis = S.eye(6)[:,0]
    eigen = K[0,0]
    eq('same_full_matter_eigenstate', Kf*basis-(eigen+c*eigen**2*(1-eigen))*basis)
    tangent=S.eye(6)[:,2]
    eq('full_normalized_sphere_first_variation',
       2*(tangent.T*(Kf-(eigen+c*eigen**2*(1-eigen))*I)*basis)[0])
    # The unchanged H and J cancel in the difference identically; no full root
    # of the alternative theory is being asserted.
    H,Jprice,Rold = S.symbols('H Jprice Rold')
    eq('same_heat_same_actual_program', (H+Jprice+Rold+diff)-(H+Jprice+Rold)-diff)
    # Exact native Fibonacci prefix cost, not an assumed new scoring function.
    def code(word):return ''.join('10' if y else '0' for y in word)
    def decode(text):
        out=[];i=0
        while i<len(text):
            if text[i]=='0':out.append(0);i+=1
            elif text[i:i+2]=='10':out.append(1);i+=2
            else:raise ValueError('outside native forbid-11 prefix code')
        return tuple(out)
    for N in range(7):
        words=list(itertools.product((0,1),repeat=N))
        check('native_code_no_erasure_'+str(N),all(decode(code(w))==w for w in words))
        check('native_cost_actual_length_'+str(N),all(len(code(w))==N+sum(w) for w in words))
        eq('native_reference_mass_'+str(N),sum(P**len(code(w)) for w in words)-1)
    length_effect=3*I+3*s*K
    eq('code_cost_pullback_on_actual_instrument', (length_effect-3*I)/(3*s)-K)
    # Independently reconstruct its measured three-round length operator.
    measured_length=S.zeros(6)
    for w in itertools.product((0,1),repeat=3):
        Eword=I
        for y in reversed(w):Eword=branch(Eword,y)
        measured_length+=len(code(w))*Eword
    eq('literal_length_operator_from_full_records',measured_length-length_effect)
    # Golden code measure is NOT silently declared the outcome distribution.
    reject('reference_measure_equals_all_physical_outcomes',mat(E-P**2*I)==S.zeros(6))

    # Positive likelihood lift on the native support. A genuinely noncommuting
    # two-Kraus instrument shows no QND premise is needed for compatibility.
    A0=S.diag(S.Rational(3,5),S.Rational(5,13))
    A1=S.Matrix([[0,1],[1,0]])*S.diag(S.Rational(4,5),S.Rational(12,13))
    check('likelihood_actual_instrument_complete',A0.T*A0+A1.T*A1==S.eye(2))
    check('likelihood_noncommuting_history_control',A0*A1!=A1*A0)
    def amplitude(w):
        out=S.eye(2)
        for y in w:out=(A1 if y else A0)*out
        return out
    def likelihood(w):
        A=amplitude(w)
        return mat((A.T*A)/P**len(code(w)))
    for N in range(4):
        normalized=S.zeros(2)
        for w in itertools.product((0,1),repeat=N):
            eq('operator_likelihood_refinement_'+str(N),
               P*likelihood(w+(0,))+P**2*likelihood(w+(1,))-likelihood(w))
            normalized+=P**len(code(w))*likelihood(w)
        eq('full_likelihood_mass_'+str(N),normalized-S.eye(2))
    leaves=[()]
    for level in range(7):
        check('cost_cut_covers_no_selected_event_'+str(level),
              all(len(code(w))>=level and (not w or len(code(w[:-1]))<level) for w in leaves))
        eq('cost_cut_operator_normalization_'+str(level),
           sum((P**len(code(w))*likelihood(w) for w in leaves),S.zeros(2))-S.eye(2))
        leaves=[u for w in leaves for u in ((w+(0,),w+(1,)) if len(code(w))==level else (w,))]
    reject('likelihood_is_always_identity',likelihood((0,))==S.eye(2))
    # Native cost cuts are not fixed numbers of comparator rounds.
    r=S.Symbol('r',real=True)
    mean_errors=(1-r)*r+r
    mean_rounds=2*(1-r)**2+2*(1-r)*r+r
    eq('cost2_expected_count',mean_errors-(2*r-r*r))
    eq('cost2_expected_rounds',mean_rounds-(2-r))
    eq('cost2_single_mode_ratio',mean_errors-r*mean_rounds)
    # Two-mode mixture at effects (0,1/2): fixed-time average 1/4.
    stopped_ratio=S.Rational(3,8)/S.Rational(7,4)
    reject('cost_clock_equals_raw_round_clock_for_mixtures',stopped_ratio==S.Rational(1,4))
    eq('exact_stopped_mixture_gap',stopped_ratio-S.Rational(1,4)+S.Rational(1,28))

    # Positive elimination criterion: concatenation plus calibrated one-letter
    # costs fixes every word by induction. Validate the finite kernel only.
    for n in range(7):
      for word in itertools.product((0,1), repeat=n):
        # grouped name deliberately one per length, no thousands-of-theorems claim
        value=sum(S.Integer(y)/s for y in word)
        eq('additive_word_kernel_length_'+str(n),value-S.Integer(sum(word))/s)
    reject('nonlinear_score_obeys_same_primitive_additivity',
           red(3*scores1[2]-2/s)==0)
    eq('exact_primitive_additivity_defect',3*scores1[2]-2/s-c/s**2)
    # Source normalization cannot be removed by one universal unit rescaling.
    eq('energy_squared_scaling',limit.subs(e,2*e)-4*limit)
    reject('one_linear_energy_unit_absorbs_correction',S.expand(limit.subs(e,2*e)-2*limit)==0)
    return {'counted_conditions':len(CHECKS),'distinct_condition_names':len(set(CHECKS)),
            'negative_controls':NEGATIVE,
            'source_gap_limit':'-phi^(-3)*epsilon_infinity^2/64',
            'refinement_defect_zero':True}

def intervals():
    mp.iv.dps=60; iv=mp.iv
    p=(iv.sqrt(5)-1)/2;c=p**3;s=4*c
    check('golden_interval_lower',bool(c>iv.mpf(1)/5))
    check('golden_interval_upper',bool(c<iv.mpf(1)/4))
    scores=[iv.mpf(0),1/(3*s),2/(3*s)+c/(3*s*s),1/s+c/s**2-c/s**3]
    for i in range(3):check('all_scores_nonnegative_increasing_'+str(i),bool(scores[i+1]>scores[i]))
    # Consumes the already-proved v10 box, does NOT issue another root certificate.
    d=iv.mpf('0.063635191594344535042829697433316630182693569761541')+iv.mpf(['-1e-12','1e-12'])
    eps=d*(128-64*iv.sqrt(2)); h=iv.mpf(1)/8;k=h*h/256
    gap=(-4*c*k*eps**2+6*c*k*k*eps**3)/(h*h)
    check('v10_box_positive_matter',bool(eps>2))
    check('v10_energy_lower',bool(eps>iv.mpf('2.3857044602')))
    check('v10_energy_upper',bool(eps<iv.mpf('2.3857044604')))
    check('v10_gap_lower',bool(gap>iv.mpf('-0.020989183')))
    check('v10_gap_upper',bool(gap<iv.mpf('-0.020989182')))
    rawgap=c*(2*k*eps-3*k*k*eps**2)*(128-64*iv.sqrt(2))/(h*h)
    check('raw_G_metric_source_gap_lower',bool(rawgap>iv.mpf('0.164918041')))
    check('raw_G_metric_source_gap_upper',bool(rawgap<iv.mpf('0.164918044')))
    check('radial_raw_G_gap_consistency',bool(abs(gap+2*d*rawgap)<iv.mpf('1e-10')))
    return {'conditional_on_pinned_v10_root_box':True,
            'normalized_radial_gap_enclosure':['-0.020989183','-0.020989182'],
            'epsilon8_enclosure':['2.3857044602','2.3857044604'],
            'normalized_raw_G_packed_source_gap_enclosure':['0.164918041','0.164918044']}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run():
    a=math();b=intervals()
    return {'schema':'d0-direct-forcing-attack/1','status':'PASS',
            'input_head':'9e28597a917c581f684aa26e33ad0323c3265989',
            'proof_sha256':sha(HERE/'RESULT.md'),'checker_sha256':sha(Path(__file__)),
            'algebra':a,'interval':b,'conditions_total':len(CHECKS),
            'distinct_conditions_total':len(set(CHECKS)),
            'scope':{'same_full_tape_same_heat_and_J':True,
                     'alternative_is_installed_D0_action':False,
                     'all_D0_premises_satisfied_by_alternative':False,
                     'v10_listed_structural_tests_force_unique_matter_readout':False,
                     'M1_class_admissibility_alone_forces_original':False,
                     'primitive_additivity_would_select_linear_score':True,
                     'literal_Fibonacci_code_mean_cost_pullback_proved':True,
                     'native_code_positive_likelihood_lift_proved':True,
                     'full_Cost_minus_Info_physical_action_identity_proved':False,
                     'error_flag_to_native_return_forced_by_M1':False,
                     'exact_joint_root_for_alternative_proved':False,
                     'original_310_terminal_or_GR_closed':False,
                     'new_Lean_compilation':False}}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    report=run();dest=HERE/'receipt.json'
    if args.write:dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    else:
        old=json.loads(dest.read_text())
        if old!=report:raise AssertionError('IMMUTABLE_RECEIPT_MISMATCH')
    print(json.dumps(report,ensure_ascii=False,indent=2))
