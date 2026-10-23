#!/usr/bin/env python3
"""Exact consumer of D0's pinned 15-setting CAR/clock metrology.

Derives the complete count-macroevent likelihood and tests its source as a
candidate gravity action. A failed candidate is not a no-go for all D0.
Run: python check_macrohistory.py [--owner PATH]
Uses explicit checks, not assertions. Does not execute the owner's main().
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import sympy as s

SOURCE_REF = '48fbb7a144b124b5ed881103d466041b317d5590'
OWNER_BLOB = '1c5df0367784f911b4684d2d1aacc87bf469ea2f'
CHECKS: list[str] = []


def check(name: str, condition: bool) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def equal(name: str, left, right=0) -> None:
    d = left - right
    seq = list(d) if isinstance(d, s.MatrixBase) else [d]
    check(name, all(s.simplify(s.cancel(v)) == 0 for v in seq))


def gitblob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_owner(path: Path):
    data = path.read_bytes()
    check('exact_owner_blob', gitblob(data) == OWNER_BLOB)
    spec = importlib.util.spec_from_file_location('d0_pinned_meter_owner', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the pinned owner')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    check('no_old_control_suite_executed', not module.CHECKS)
    return module


def main(owner_path: Path) -> dict:
    owner = load_owner(owner_path)
    creators = owner.creators()
    zet = [c - c.T for c in creators]
    I = s.eye(16)
    zero = s.zeros(16)
    eta = s.diag(1, -1, -1, -1)
    delta = s.Rational(3, 5)
    r = delta**2
    root = s.Rational(4, 5)
    F0 = s.eye(4)
    # The single clock and all four original raised coefficient vectors.
    vectors = [s.eye(4)[:, 0]] + [eta.row(i).T for i in range(4)]
    names = ['clock'] + [f'single_{i}' for i in range(4)]
    pairs: list[tuple[int, int]] = [(1+i, 1+j) for i in range(4) for j in range(i+1, 4)]
    pairs += [(1+i, 0) for i in range(4)]
    settings: list[tuple[int, ...]] = [(i,) for i in range(5)] + pairs
    labels = names + [f'pair_{i}_{j}' for i, j in itertools.combinations(range(4), 2)]
    labels += [f'clock_pair_{i}' for i in range(4)]

    def zeta(v):
        return sum((v[i]*zet[i] for i in range(4)), s.zeros(16))

    probs = []
    for label, setting in zip(labels, settings):
        if len(setting) == 1:
            v = vectors[setting[0]]
            K1 = delta*zeta(v)
            probability = delta**2*v.dot(v)
            K0 = root*I
        else:
            i, j = setting
            vi, vj = vectors[i], vectors[j]
            K1 = root*delta*(zeta(vi)+zeta(vj))
            K0 = root**2*I+delta**2*zeta(vi)*zeta(vj)
            probability = 2*r*(1-r)+2*r*(1-r)*vi.dot(vj)
        equal(label+'_scalar_flag_effect', K1.T*K1, probability*I)
        equal(label+'_full_binary_completeness', K0.T*K0+K1.T*K1, I)
        check(label+'_strict_probability', 0 < probability < 1)
        probs.append(probability)
    check('all_15_original_settings', len(settings) == len(probs) == 15)

    packed = [(i,j) for i in range(4) for j in range(i,4)]
    J = s.zeros(15, 10)
    for col,(a,b) in enumerate(packed):
        V=s.zeros(4); V[a,b]=1; V[b,a]=1
        dF=V*eta/2
        equal(f'actual_metric_lift_{a}_{b}', dF*eta+eta*dF.T, V)
        dU=dF*eta
        dvs=[s.zeros(4,1)]+[dU.row(i).T for i in range(4)]
        dr=[2*delta**2*v.dot(dv) for v,dv in zip(vectors,dvs)]
        ds=[-v/(2*root) for v in dr]
        for row,setting in enumerate(settings):
            if len(setting)==1:
                i=setting[0]
                dp=dr[i]
                A=delta*zeta(vectors[i]); dA=delta*zeta(dvs[i])
            else:
                i,j=setting
                vi,vj=vectors[i],vectors[j]
                dvi,dvj=dvs[i],dvs[j]
                dp=(1-2*r)*(dr[i]+dr[j])+2*delta**2*(
                    (ds[i]*root+root*ds[j])*vi.dot(vj)
                    +root**2*(dvi.dot(vj)+vi.dot(dvj)))
                A=delta*root*(zeta(vi)+zeta(vj))
                dA=delta*(ds[i]*zeta(vj)+root*zeta(dvj)
                           +ds[j]*zeta(vi)+root*zeta(dvi))
            equal(f'word_effect_jet_{a}_{b}_{row}',dA.T*A+A.T*dA,dp*I)
            J[row,col]=s.factor(dp)
    check('all_ten_metric_directions_measured', J.rank()==10)
    fisher=s.simplify(J.T*s.diag(*[1/(v*(1-v)) for v in probs])*J)
    lower,diagonal=fisher.LDLdecomposition(hermitian=False)
    equal('exact_full_Fisher_LDL',lower*diagonal*lower.T,fisher)
    check('all_Fisher_pivots_strictly_positive',all(diagonal[i,i]>0 for i in range(10)))

    # The same scalar effects work on all reference columns and any rank.
    C=s.zeros(16,128)
    for j in range(128):
        C[j%16,j]=1+(j%3)
    dC=s.zeros(16,128)
    for j in range(128):
        dC[(j+1)%16,j]=1
    N=s.trace(C.T*C); dN=2*s.trace(C.T*dC)
    Ef=probs[5]*I
    equal('full_reference128_probability',s.trace(C.T*Ef*C)/N,probs[5])
    equal('full_moving_preparation_source_cancels',
          2*s.trace(dC.T*Ef*C)/N-s.trace(C.T*Ef*C)*dN/N**2,0)
    check('all_reference_columns_retained',all(C[:,j]!=s.zeros(16,1) for j in range(128)))

    # Complete count-event, not an ad hoc function of the reconstructed metric.
    M=625
    counts=[int(M*p) for p in probs]
    equal('all_target_counts_are_exact',s.Matrix(counts),M*s.Matrix(probs))
    # Generic symbolic Bernoulli source and Hessian (natural-log units).
    x=s.symbols('x',real=True)
    q0=s.Rational(9,25)
    q=q0+x/17+x*x/23
    loss=-M*q0*s.log(q)-M*(1-q0)*s.log(1-q)
    score=M*(q-q0)*s.diff(q,x)/(q*(1-q))
    equal('exact_count_score',s.diff(loss,x),score)
    equal('matched_event_full_first_source_zero',s.diff(loss,x).subs(x,0),0)
    equal('matched_event_Hessian_not_value_only',s.diff(loss,x,2).subs(x,0),
          M*s.diff(q,x).subs(x,0)**2/(q0*(1-q0)))
    for m in (1,2,5,9):
        p=s.symbols('p',positive=True)
        total=sum(s.binomial(m,k)*p**k*(1-p)**(m-k) for k in range(m+1))
        equal(f'complete_count_cut_normalizer_{m}',total,1)
    m,k=s.symbols('m k',integer=True,positive=True)
    p,p0=s.symbols('p p0',positive=True)
    # Differentiating excludes only the SAME parameter-independent binomial factor.
    ll=-m*p0*s.log(p)-m*(1-p0)*s.log(1-p)
    kl=m*(p0*s.log(p0/p)+(1-p0)*s.log((1-p0)/(1-p)))
    equal('exact_relative_macro_KL_source',s.diff(ll,p),s.diff(kl,p))

    # Fixed spacetime-flat, exactly volume-preserving physical shear.
    t=s.symbols('t',real=True)
    Ft=s.diag(1/(1+t),1+t,1,1)
    qt=Ft*eta*Ft.T
    gt=qt.inv()
    equal('flat_shear_volume_fixed',gt.det(),-1)
    V=qt.diff(t).subs(t,0)
    v=s.Matrix([V[i,j] for i,j in packed])
    equal('flat_shear_actual_tangent',V,s.diag(-2,-2,0,0))
    derivative=J*v
    c=s.factor((v.T*fisher*v)[0])
    cformula=s.factor(12*r/(1-r)+10*r*(1-2*r)**2/((1-r)*(1-2*r+2*r*r)))
    equal('full_15_setting_shear_coefficient',c,cformula)
    equal('exact_shear_coefficient_value',c,s.Rational(20403,2696))
    check('flat_volume_preserving_macro_source_is_not_EH',c>0)
    # Full Ricci is zero because gt has no dependence on spacetime variables.
    spacetime=s.symbols('x0:4')
    check('every_spacetime_metric_jet_zero',all(s.diff(gt[i,j],coord)==0
          for i in range(4) for j in range(4) for coord in spacetime))

    # Nondemolition operator identity: arbitrary input and reference allowed.
    K0=s.kronecker_product(s.diag(s.Rational(4,5),s.Rational(3,5)),I)
    K1=s.kronecker_product(s.diag(s.Rational(3,5),s.Rational(4,5)),zet[0])
    identity=s.eye(32)
    equal('controlled_full_instrument_complete',K0.T*K0+K1.T*K1,identity)
    for g in (0,1):
        proj=s.kronecker_product(s.diag(1-g,g),I)
        equal(f'geometry_marginal_invariant_{g}',K0.T*proj*K0+K1.T*proj*K1,proj)
    swap=s.kronecker_product(s.Matrix([[0,1],[1,0]]),I)
    P0=s.kronecker_product(s.diag(1,0),I)
    check('actual_geometry_changing_step_is_outside_this_theorem',swap.T*P0*swap!=P0)

    # Same completely retained golden tree, two different macro readouts.
    pg=s.symbols('pg')
    def golden(poly):
        return s.rem(s.expand(poly),pg**2+pg-1,pg)
    words=list(itertools.product((0,1),repeat=3))
    weights={w:pg**sum(1+b for b in w) for w in words}
    equal('all_eight_golden_histories_complete',golden(sum(weights.values())),1)
    first=sum(v for w,v in weights.items() if w[0]==0)
    three=weights[(0,0,0)]
    equal('first_direct_macro_weight',golden(first-pg),0)
    equal('three_direct_macro_weight',golden(three-pg**3),0)
    check('golden_code_does_not_name_one_macro_event',golden(first-three)!=0)
    equal('three_direct_complement_retained',golden(1-three-2*pg**2),0)

    # Two complete raw weights with the SAME conditional law; no claim that
    # both are physically selected D0 models. This is an identification theorem.
    raw=s.Matrix([s.exp(-x),s.exp(-2*x)])
    scale=s.exp(-x*x)
    cond=raw/sum(raw)
    moved=scale*raw/sum(scale*raw)
    equal('conditional_probabilities_do_not_fix_raw_scale',cond,moved)
    equal('all_first_conditional_jets_identical',cond.diff(x),moved.diff(x))
    equal('all_second_conditional_jets_identical',cond.diff(x,2),moved.diff(x,2))
    gamma_prime=-s.diff(sum(raw),x)/sum(raw)
    new_prime=-s.diff(sum(scale*raw),x)/sum(scale*raw)
    equal('geometric_raw_source_still_changes',new_prime-gamma_prime,2*x)

    # Both original one-body survival and the new collective determinant are
    # real possible event laws. Their ensemble choice must not be erased.
    e,z,u=s.symbols('e z u',real=True)
    feedback=s.diag(e+u,e-u,e+u,e-u)
    surv=s.eye(4)-z*feedback
    wd=surv.det()
    wr=(s.trace(surv)/4)**4
    equal('actual_two_copy_AF_determinant',wd,((1-z*e)**2-z*z*u*u)**2)
    equal('four_independent_trace_trials',wr,(1-z*e)**4)
    hdet=(-s.diff(wd,u,2)/wd+s.diff(wd,u)**2/wd**2).subs(u,0)
    hrep=(-s.diff(wr,u,2)/wr+s.diff(wr,u)**2/wr**2).subs(u,0)
    equal('full_collective_source_differs',hdet-hrep,4*z*z/(1-z*e)**2)
    equal('common_scalar_first_source',
          (-s.diff(wd,e)/wd).subs(u,0),-s.diff(wr,e)/wr)

    return {
      'status':'PASS_EXACT_SCOPED_MACROEVENT_SOURCE',
      'source_ref':SOURCE_REF,
      'input_git_blob':OWNER_BLOB,
      'python':sys.version.split()[0], 'sympy':s.__version__,
      'checks':len(CHECKS), 'check_names':CHECKS,
      'settings':labels, 'probabilities_at_base':[str(p) for p in probs],
      'repetitions_each_setting':M, 'target_counts':counts,
      'metric_packed_slots':packed,
      'probability_metric_jacobian':[[str(v) for v in J.row(i)] for i in range(15)],
      'Fisher_LDL_pivots':[str(diagonal[i,i]) for i in range(10)],
      'Fisher_rank':10,
      'log_phi_times_action_shear_Hessian':str(M*c),
      'all_curvature_rows_on_shear':'zero: coefficients constant in spacetime',
      'native_admission_of_all_meter_words_proved':False,
      'full_native_geometric_prior_selected':False,
      'macroevent_alone_is_Einstein_action':False,
      'D0_to_GR_proved':False,
      'general_D0_no_go_proved':False,
      'original_raw_terminal_closed':False,
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    local=here/'inputs'/'check_operational_metric.py'
    native=here.parent/'d0_operational_car_clock_readout_2026-10-17'/'check_operational_metric.py'
    parser.add_argument('--owner',type=Path,default=local if local.exists() else native)
    opts=parser.parse_args()
    print(json.dumps(main(opts.owner),ensure_ascii=False,sort_keys=True,indent=2))
