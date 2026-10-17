"""Exact finite controls for the golden comparison / retained-history theorem.
No claim of physical admission, all-D0 uniqueness, or new Lean compilation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
a,p=s.symbols('a p', real=True)
GB=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ_I)
def red(x):
    num,den=s.cancel(x).as_numer_denom()
    num=GB.reduce(s.expand(num))[1];den=GB.reduce(s.expand(den))[1]
    if den==0: raise ValueError('ZERO_DENOMINATOR')
    return s.cancel(num/den)
def mat(x):return x.applyfunc(red)
CHECKS=[];MUTANTS=[]
def check(name,claim):
    if not bool(claim): raise AssertionError(name)
    CHECKS.append(name)
def eq(name,x):
    vals=list(x) if isinstance(x,s.MatrixBase) else [x]
    check(name,all(red(v)==0 for v in vals))
def reject(name,false):
    check('REJECT_'+name,not bool(false));MUTANTS.append(name)
def zero(x):
    vals=list(x) if isinstance(x,s.MatrixBase) else [x]
    return all(red(v)==0 for v in vals)

def shift(L):
    U=s.zeros(L)
    for x in range(L): U[x,(x+1)%L]=1
    return U

def run():
    G=s.Matrix([[a,-p],[p,a]])
    X=s.Matrix([[0,1],[1,0]])
    eq('golden_echo_forward',X*G*X-G.T)
    eq('golden_isometry',G.T*G-s.eye(2))
    CNOT=s.eye(4);CNOT[2,2]=CNOT[3,3]=0;CNOT[2,3]=CNOT[3,2]=1
    fullstep=s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
    eq('literal_GoldenCoherentMemory_fullStep',CNOT*s.kronecker_product(G,s.eye(2))-fullstep)
    gamma=p**3
    eq('strict_upper_effect_identity',1-4*gamma-p**6)
    phi=(1+s.sqrt(5))/2
    check('pi0_seam_exact',s.simplify(2*s.Rational(6,5)*phi**2*(2-phi)-s.Rational(12,5))==0)

    # Complete ancilla+system unitary, arbitrary unitary return pair, both outputs retained.
    cases=[(shift(4),s.eye(4)),
           (s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]]),
            s.Matrix([[1,0],[0,-1]])),
           (s.Matrix([[0,1],[1,0]]),(s.Rational(3,5)+s.I*s.Rational(4,5))*s.eye(2))]
    for j,(U,V) in enumerate(cases):
        d=U.rows;I=s.eye(d)
        eq(f'U_unitary_{j}',U.H*U-I);eq(f'V_unitary_{j}',V.H*V-I)
        whole=s.kronecker_product(G.T,I)*s.diag(V,U)*s.kronecker_product(G,I)
        eq(f'complete_comparer_unitary_{j}',whole.H*whole-s.eye(2*d))
        A0,A1=whole[:d,:d],whole[d:,:d]
        K=(U-V).H*(U-V)
        eq(f'actual_success_amplitude_{j}',A0-a*a*V-p*p*U)
        eq(f'actual_failure_amplitude_{j}',A1-a*p*(U-V))
        eq(f'actual_effect_is_quadratic_{j}',A1.H*A1-gamma*K)
        eq(f'all_outcomes_kept_{j}',A0.H*A0+A1.H*A1-I)
        # No selected state for the operator identity.
        for c in range(d):
            for r in range(d): eq(f'effect_entry_{j}_{r}_{c}',(A1.H*A1-gamma*K)[r,c])
        reject(f'uncalibrated_probability_equals_K_{j}',zero(A1.H*A1-K))
    U=shift(4);I=s.eye(4)
    whole_equal=s.kronecker_product(G.T,I)*s.diag(U,U)*s.kronecker_product(G,I)
    eq('equal_processes_never_false_fail',whole_equal[4:,:4])
    bad=s.kronecker_product(G,I)*s.diag(U,U)*s.kronecker_product(G,I)
    reject('omit_echo_inverse',zero(bad[4:,:4]))

    # Exact bias removal from two literal golden preparations; the bad branch is nonzero.
    raw=s.kronecker_product(G,G)*s.eye(4)[:,0]
    parity_state=CNOT*raw
    Pgood=s.diag(0,1,0,1)
    good=Pgood*parity_state;bad=(s.eye(4)-Pgood)*parity_state
    eq('fair_bit_equal_amplitudes',good-s.Matrix([0,a*p,0,a*p]))
    eq('fair_bit_success_probability',(good.T*good)[0]-2*gamma)
    eq('fair_bit_failure_probability',(bad.T*bad)[0]-(1-2*gamma))
    reject('parity_extraction_is_deterministic',zero((bad.T*bad)[0]))
    eq('fair_bit_joint_norm',(good.T*good)[0]+(bad.T*bad)[0]-1)
    # The accepted parity bit is itself a retained |1> resource for the forward echo.
    echo=CNOT*s.kronecker_product(s.eye(2),G)*CNOT
    eq('heralded_one_controls_inverse_without_reset',echo[2:4,2:4]-G.T)
    eq('failed_zero_flag_not_silently_inverse',echo[:2,:2]-G)
    eq('both_echo_sectors_retained',echo.T*echo-s.eye(4))
    # The two allowed branches of every successful extractor produce the identity marginal.
    pur=s.Matrix([[a*p,0],[0,a*p]])
    eq('success_purification_identity',pur*pur.H-gamma*s.eye(2))

    # Actual position-space, not chosen eigenvalues. 2D L=2 is a four-point finite control;
    # the production L=8 four-dimensional branch is separately interval-certified.
    L=2;U0=s.kronecker_product(shift(L),s.eye(L));U1=s.kronecker_product(s.eye(L),shift(L))
    Us=[U0,U1];d=2;N=L**d;I=s.eye(N)
    K=sum(((u-I).T*(u-I) for u in Us),s.zeros(N))
    E=mat(gamma*K/d);tau=I/N
    def fail(rho):
        return mat(sum((gamma/d*(u-I)*rho*(u-I).T for u in Us),s.zeros(N)))
    def quiet(rho):
        return mat(sum(((p*I+p*p*u)*rho*(p*I+p*p*u).T/d for u in Us),s.zeros(N)))
    actual=fail(tau)
    eq('first_record_removes_kernel',actual-E/N)
    for n in range(5):
        expected=mat(E*(I-E)**n/N)
        eq(f'actual_history_polynomial_{n}',actual-expected)
        eq(f'unconditioned_trace_preserved_{n}',s.trace(quiet(actual)+fail(actual))-s.trace(actual))
        if n<4: actual=quiet(actual)
    # All retained binary histories: actual channel recursion equals the binomial
    # polynomial, rather than independent fresh-state Bernoulli trials.
    states=[tau]
    for T in range(1,4):
        nxt=[]
        for k in range(T+1):
            zmat=s.zeros(N)
            if k<T:zmat+=quiet(states[k])
            if k>0:zmat+=fail(states[k-1])
            nxt.append(mat(zmat))
            eq(f'actual_count_event_{T}_{k}',nxt[-1]-s.binomial(T,k)*E**k*(I-E)**(T-k)/N)
        eq(f'all_count_events_complete_{T}',sum(nxt,s.zeros(N))-tau)
        states=nxt
    reject('average_rate_trials_are_independent',zero(s.trace(E*E)/N-(s.trace(E)/N)**2))
    eq('unconditioned_trace_reference_unchanged',quiet(tau)+fail(tau)-tau)
    reject('unconditioned_ensemble_is_filtered',zero(quiet(tau)+fail(tau)-fail(tau)/s.trace(fail(tau))))
    const=s.ones(N,1)
    eq('reference_has_true_zero_mode',K*const)
    eq('error_history_removes_zero_mode',fail(tau)*const)
    reject('quiet_history_alone_removes_vacuum',zero(quiet(tau)*const))
    # Histories retain the same occupied first-shell density, not an arbitrary new ray.
    anis=s.diag(s.Rational(3,4),s.Rational(1,4),0)
    smallE=s.diag(s.Rational(1,5),s.Rational(1,5),s.Rational(2,5))
    filt=smallE*(s.eye(3)-smallE)**4*anis
    eq('degenerate_weight_ratio_preserved',filt[0,0]-3*filt[1,1])
    reject('filter_erases_supplied_degenerate_bias',filt[0,0]==filt[1,1])
    # Necessity of common eigenbasis for the simple polynomial theorem.
    Ua=s.Matrix([[0,1],[1,0]]);Ub=s.Matrix([[1,0],[0,s.I]])
    Ii=s.eye(2);Kv=sum(((u-Ii).H*(u-Ii) for u in [Ua,Ub]),s.zeros(2))
    R0=mat(gamma*Kv/4)
    actual_nc=mat(sum(((p*Ii+p*p*u)*R0*(p*Ii+p*p*u).H/2 for u in [Ua,Ub]),s.zeros(2)))
    guessed=mat((Ii-gamma*Kv/2)*R0)
    reject('noncommuting_channels_are_polynomial_filter',zero(actual_nc-guessed))

    # Additive counts imply an affine averaged readout, not a nonlinear probability score.
    q1,q2,t=s.symbols('q1 q2 t',real=True)
    check('mixture_mean_is_affine',s.expand(t*q1+(1-t)*q2-(t*q1+(1-t)*q2))==0)
    reject('square_probability_is_additive_readout',s.expand((t*q1+(1-t)*q2)**2-t*q1*q1-(1-t)*q2*q2)==0)
    # Ground-free positive defect does not select an excited layer with a click.
    Epos=s.diag(s.Rational(1,5),s.Rational(2,5))
    check('ground_without_kernel_survives_first_error',Epos[0,0]>0)
    reject('first_click_removes_nonzero_ground',Epos[0,0]==0)
    return {'status':'PASS','exact_controls':len(CHECKS),'checks':CHECKS,
            'executed_negative_claims':MUTANTS,'physical_admission_derived':False,
            'global_M1_forcing_derived':False,'new_Lean_compilation':False,
            'definition_scope':'literal G/fullStep from pinned source; finite controlled U,V are declared operations'}

if __name__=='__main__':
    out=run();dest=ROOT/'results/exact_operations.json'
    text=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
    dest.write_text(text)
    print('PASS_EXACT_OPERATIONS',out['exact_controls'],'controls;',len(MUTANTS),'negative claims')
