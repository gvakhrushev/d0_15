#!/usr/bin/env python3
"""Native Fibonacci matrix-state lift and Cost-Info information readouts.
Exact algebra + outward intervals; no claim of M1 action selection or GR.
Default: compare immutable receipt. --write: explicit initial/refreshed receipt.
--math-only: run gates without receipt integrity (used only for hostile tests).
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sympy as s
import mpmath as mp

HERE = Path(__file__).resolve().parent
CHECKS: list[str] = []

def ck(name: str, predicate: object) -> None:
    if not bool(predicate):
        raise AssertionError(name)
    CHECKS.append(name)

def zmat(M: s.MatrixBase) -> bool:
    return all(s.simplify(x) == 0 for x in M)

def gram(amps: list[s.Matrix], rho: s.Matrix) -> s.Matrix:
    return s.Matrix(len(amps), len(amps),
                    lambda i,j: s.expand(s.trace(amps[i]*rho*amps[j].H)))

def gram_dot(amps, dots, rho, drho):
    return s.Matrix(len(amps),len(amps),lambda i,j:
        s.expand(s.trace(dots[i]*rho*amps[j].H + amps[i]*drho*amps[j].H
                + amps[i]*rho*dots[j].H)))

def advance(A, B, K0, K1):
    # Native cost cut: ready leaves split; pending return leaves are carried.
    return [K0*x for x in A] + list(B), [K1*x for x in A]

def advance_dot(A, B, dA, dB, K0, K1, dK0, dK1):
    return ([dK0*x+K0*dx for x,dx in zip(A,dA)] + list(dB),
            [dK1*x+K1*dx for x,dx in zip(A,dA)])

def restrict_state(X, W, a):
    # Dual of iota(A,B)=(diag(A,B),A), on ordinary state densities.
    return X[:a,:a] + W, X[a:,a:]

def recover_state(A, B, p):
    return s.diag(p*A, B), p**2*A

def code(word):
    return tuple(x for b in word for x in ((0,) if b == 0 else (1,0)))

def word_cost(word):
    return sum(1 if b == 0 else 2 for b in word)

def exact():
    q=s.Rational; I=s.eye(2); O=s.zeros(2)
    rho=s.Matrix([[q(3,5),s.I/10],[-s.I/10,q(2,5)]])
    K0=s.diag(q(3,5),q(5,13))
    rot=s.Matrix([[q(3,5),-q(4,5)],[q(4,5),q(3,5)]])
    K1=rot*s.diag(q(4,5),q(12,13))
    ck('full_initial_density',rho==rho.H and s.trace(rho)==1 and rho.det()>0)
    ck('full_two_outcome_completeness',K0.H*K0+K1.H*K1==I)
    ck('genuine_noncommuting_two_outcome_control',K0*K1!=K1*K0)
    X=s.Matrix([[0,s.I],[s.I,0]])/7
    Y=s.Matrix([[0,1],[-1,0]])/11
    dK0=O; dK1=X*K1; drho=Y*rho-rho*Y
    ck('true_Kraus_tangent',zmat(dK1.H*K1+K1.H*dK1))
    ck('moving_state_normalization',s.trace(drho)==0 and drho==drho.H)
    A,B=[K0],[K1];dA,dB=[dK0],[dK1]
    wa,wb=[(0,)],[(1,)]
    p=s.symbols('p',positive=True);t=s.symbols('t',positive=True)
    expected=[(1,1),(2,1),(3,2),(5,3),(8,5)]
    for n,(a,b) in enumerate(expected):
        ck(f'native_dimensions_{n}',(len(A),len(B))==(a,b))
        ck(f'cost_depth_ready_{n}',all(word_cost(w)==n+1 for w in wa))
        ck(f'cost_depth_pending_{n}',all(word_cost(w)==n+2 for w in wb))
        ck(f'no_history_erasure_{n}',len(set(wa+wb))==a+b)
        ck(f'actual_prefix_cut_{n}',all(word_cost(w[:-1])<n+1 for w in wa+wb))
        ck(f'own_code_lengths_{n}',all(len(code(w))==word_cost(w) for w in wa+wb))
        ck(f'golden_trace_normalized_{n}',s.rem(a*p**(n+1)+b*p**(n+2)-1,p*p+p-1,p)==0)
        ck(f'complete_record_isometry_{n}',sum((M.H*M for M in A+B),s.zeros(2))==I)
        SA,SB=gram(A,rho),gram(B,rho)
        DA,DB=gram_dot(A,dA,rho,drho),gram_dot(B,dB,rho,drho)
        ck(f'whole_record_state_{n}',SA==SA.H and SB==SB.H and s.trace(SA)+s.trace(SB)==1)
        ck(f'whole_record_source_{n}',DA==DA.H and DB==DB.H and s.trace(DA)+s.trace(DB)==0)
        # Exact rank is diagnostic, not a replacement for the Gram positivity proof.
        ck(f'finite_memory_rank_{n}',SA.rank()<=4 and SB.rank()<=4)
        AN,BN=advance(A,B,K0,K1)
        dAN,dBN=advance_dot(A,B,dA,dB,K0,K1,dK0,dK1)
        FN,WN=gram(AN,rho),gram(BN,rho)
        dFN,dWN=gram_dot(AN,dAN,rho,drho),gram_dot(BN,dBN,rho,drho)
        PA,PB=restrict_state(FN,WN,a)
        ck(f'full_AF_restriction_A_{n}',PA==SA)
        ck(f'full_AF_restriction_B_{n}',PB==SB)
        DPA,DPB=restrict_state(dFN,dWN,a)
        ck(f'full_AF_jet_A_{n}',DPA==DA)
        ck(f'full_AF_jet_B_{n}',DPB==DB)
        ck(f'actual_new_rectangular_coherence_{n}',FN[:a,a:]!=s.zeros(a,b))
        # h is the RN density relative to the native weighted trace, NOT a
        # faithful density on B(H_GNS). No GNS trace normalization is changed.
        hA,hB=SA/t,SB/(p*t)
        hFN,hWN=FN/(p*t),WN/(p*p*t)
        ck(f'native_PF_martingale_A_{n}',zmat(p*hFN[:a,:a]+p*p*hWN-hA))
        ck(f'native_PF_martingale_B_{n}',zmat(hFN[a:,a:]-hB))
        recX,recW=recover_state(SA,SB,p)
        recA,recB=restrict_state(recX,recW,a)
        ck(f'positive_reference_recovery_A_{n}',zmat(recA-(p+p*p)*SA))
        ck(f'positive_reference_recovery_B_{n}',recB==SB)
        ck(f'REJECT_actual_state_equals_reference_recovery_{n}',FN[:a,a:]!=recX[:a,a:])
        if n==1:
            ck('REJECT_diagonal_only_AF_state',FN[0,1]!=0)
            ck('REJECT_drop_return_copy',FN[:a,:a]!=SA)
            ck('REJECT_frozen_state_source',DA!=s.zeros(a))
            ck('REJECT_split_pending_return_again',len(AN)!=2*len(A+B))
        A,B,dA,dB=AN,BN,dAN,dBN
        wa,wb=[w+(0,) for w in wa]+wb,[w+(1,) for w in wa]

    # The source/pair-amplitude map is basis covariant, on the entire state.
    Z=s.Matrix([[s.I,0],[0,-s.I]])/3
    d0=Z*K0-K0*Z;d1=Z*K1-K1*Z;dg=Z*rho-rho*Z
    Ag,Bg=[K0],[K1];dAg,dBg=[d0],[d1]
    for n in range(3):
        ck(f'joint_data_basis_Ward_A_{n}',zmat(gram_dot(Ag,dAg,rho,dg)))
        ck(f'joint_data_basis_Ward_B_{n}',zmat(gram_dot(Bg,dBg,rho,dg)))
        newA,newB=advance(Ag,Bg,K0,K1)
        newdA,newdB=advance_dot(Ag,Bg,dAg,dBg,K0,K1,d0,d1)
        Ag,Bg,dAg,dBg=newA,newB,newdA,newdB
    # Completeness separately on each history is not enough for offdiagonal
    # compatibility if those histories use different instruments.
    bad0=s.diag(1,-1)*K0; bad1=K1
    ck('history_dependent_instrument_still_complete',bad0.H*bad0+bad1.H*bad1==I)
    ck('REJECT_diagonal_completeness_implies_cross_compatibility',
       bad0.H*K0+bad1.H*K1!=I)

    # Actual golden direct/return process: (a I, p U), not the error
    # interferometer (p I+p^2 U, ap(U-I)). Native symbols keep their meanings.
    a=s.symbols('a',real=True);rel=a**4+a*a-1
    def red(x):return s.rem(s.expand(x),rel,a)
    def rz(M):return all(red(x)==0 for x in M)
    U=rot;C0=a*I;C1=a*a*U
    ck('literal_golden_direct_return_norm',rz(C0.H*C0+C1.H*C1-I))
    # Noncommuting genuinely golden returns retain the native path measure.
    GN0=a*s.diag(1,-1);GN1=C1
    ck('golden_return_order_not_erased',GN0*GN1!=GN1*GN0)
    AA,BB=[GN0],[GN1]
    for level in range(3):
        for M in AA:
            ck('golden_ready_effect_is_native_weight',rz(M.H*M-a**(2*(level+1))*I))
        for M in BB:
            ck('golden_pending_effect_is_native_weight',rz(M.H*M-a**(2*(level+2))*I))
        AA,BB=advance(AA,BB,GN0,GN1)
    T=s.symbols('u',real=True)
    rhoT=(I+T*s.Matrix([[0,-s.I],[s.I,0]]))/2
    AS,BS=[C0*C0,C1],[C1*C0]
    GA,GB=gram(AS,rhoT),gram(BS,rhoT)
    wanted=a**4*s.Matrix([[1,q(3,5)+s.I*q(4,5)*T],
                         [q(3,5)-s.I*q(4,5)*T,1]])
    ck('exact_coherent_golden_AF_state',zmat(GA-wanted) and GB==s.Matrix([[a**6]]))
    ck('all_diagonal_readouts_fixed',s.diff(GA[0,0],T)==s.diff(GA[1,1],T)==s.diff(GB[0,0],T)==0)
    ck('native_mu_equals_actual_diagonal',GA[0,0]==GA[1,1]==a**4 and GB[0,0]==a**6)
    ck('REJECT_golden_probabilities_determine_full_state',s.diff(GA[0,1],T)!=0)
    v=s.symbols('v');char=(v*s.eye(2)-GA).det()
    ck('full_coherence_spectrum',s.expand(char-((v-a**4)**2-a**8*(q(9,25)+q(16,25)*T*T)))==0)
    # Actual loop rotation jet: c'= -4/5 at c=3/5, keeping probability fixed.
    c=s.symbols('c',positive=True)
    Phi=s.symbols('Phi',positive=True)
    D=p*p*((1+c)*s.log(1+c)+(1-c)*s.log(1-c))/s.log(Phi)
    dD=s.diff(D,c)
    ck('exact_information_covector',s.simplify(dD-p*p*(s.log(1+c)-s.log(1-c))/s.log(Phi))==0)
    # Fixed-instrument affine input: r(u)=sqrt(c^2+sine^2 u^2).
    r=s.sqrt(q(9,25)+q(16,25)*T*T)
    DD=p*p*((1+r)*s.log(1+r)+(1-r)*s.log(1-r))/s.log(Phi)
    ck('first_input_jet_zero_at_reference',s.simplify(s.diff(DD,T).subs(T,0))==0)
    curvature=s.simplify(s.diff(DD,T,2).subs(T,0))
    ck('nonzero_affine_input_information_hessian',
       s.simplify(curvature-16*p*p*s.log(4)/(15*s.log(Phi)))==0)
    ck('REJECT_fixed_quadratic_expectation_has_this_hessian',curvature!=0)
    # Symbolic full Cost-Info and coherence decomposition: quantities are
    # evaluated in the interval/matrix controls below, not asserted from names.
    cost=4*p*p+3*p**3
    ck('exact_native_expected_cost',s.rem(cost-(1+2*p),p*p+p-1,p)==0)
    return {'exact_conditions':len(CHECKS),
            'negative_conditions':sum(x.startswith('REJECT') for x in CHECKS)}

def intervals():
    before=len(CHECKS);mp.iv.dps=70;iv=mp.iv
    p=(iv.sqrt(5)-1)/2;logphi=-iv.log(p)
    c=iv.mpf(3)/5
    action=p*p*((1+c)*iv.log(1+c)+(1-c)*iv.log(1-c))/logphi
    source=-iv.mpf(4)/5*p*p*iv.log(4)/logphi
    hessian=iv.mpf(16)/15*p*p*iv.log(4)/logphi
    ck('strict_positive_coherence_cost',action.a>iv.mpf('0.3059856063173529') and action.b<iv.mpf('0.3059856063173531'))
    ck('strict_information_source',source.a>iv.mpf('-0.8803064263350401') and source.b<iv.mpf('-0.8803064263350399'))
    ck('strict_information_hessian',hessian.a>iv.mpf('1.1737419017800533') and hessian.b<iv.mpf('1.1737419017800535'))
    mu=[p*p,p*p,p**3]
    vals=[p*p*(1+c),p*p*(1-c),p**3]
    cost=2*(mu[0]+mu[1])+3*mu[2]
    entropy=-sum(v*iv.log(v) for v in vals)
    shannon=-sum(v*iv.log(v) for v in mu)
    for x in (cost-entropy/logphi-action, cost-shannon/logphi):
        ck('cost_information_relative_entropy_identity',x.a<=0<=x.b and (x.b-x.a)<iv.mpf('1e-60'))
    ck('state_positive_interior',min(v.a for v in vals)>0)
    ck('coherence_not_classical_entropy', (shannon-entropy).a>iv.mpf('.14'))
    # A fully interacting 3-state (M2 + M1) entropy-chain control.
    # The fine density and recovered density do not commute.
    lam=[iv.mpf(3)/8+iv.sqrt(41)/40,iv.mpf(3)/8-iv.sqrt(41)/40,iv.mpf(1)/4]
    trlog=sum(v*iv.log(v) for v in lam)
    fine=trlog-iv.mpf(9)/4*iv.log(p)
    coarse=-iv.log(2)-iv.mpf(3)/2*iv.log(p)
    recovery_pair=trlog-(iv.mpf(1)/4*iv.log(p/2)+iv.mpf(1)/2*iv.log(iv.mpf(1)/2)+iv.mpf(1)/4*iv.log(p*p/2))
    eq=fine-coarse-recovery_pair
    ck('interacting_entropy_chain_interval',eq.a<=0<=eq.b and eq.b-eq.a<iv.mpf('1e-60'))
    ck('strict_positive_conditional_increment',recovery_pair.a>0)
    return {'interval_conditions':len(CHECKS)-before,
            'cost_info_interval':['0.3059856063173529','0.3059856063173531'],
            'loop_source_interval':['-0.8803064263350401','-0.8803064263350399'],
            'affine_preparation_hessian_interval':['1.1737419017800533','1.1737419017800535']}

SCOPE={
 'full_native_AF_state_and_Radon_Nikodym_martingale':True,
 'actual_shared_two_outcome_instrument_coherences_retained':True,
 'noncommuting_instrument_and_moving_state_jets':True,
 'native_cost_minus_operator_entropy_identity':True,
 'operator_entropy_is_an_explicit_readout_not_core_derived_Info':True,
 'constant_rank_or_faithful_stratum_required_for_log_derivative':True,
 'all_distinct_cuts_have_zero_source_difference':False,
 'arbitrary_history_control_preserves_fixed_AF_inclusion':False,
 'complete_record_tape_physically_dephased':False,
 'same_state_as_faithful_GNS_Gibbs':False,
 'M1_forcing_of_complete_physical_action':False,
 'new_Lean_build_or_physical_Ward_or_GR':False,
 'old_H_J_R_stationarity_promoted_to_Cost_Info':False,
}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    pa=argparse.ArgumentParser();pa.add_argument('--write',action='store_true');pa.add_argument('--math-only',action='store_true');args=pa.parse_args()
    result={'scope':SCOPE,'exact':exact(),'interval':intervals()}
    result['conditions_executed']=len(CHECKS)
    result['unique_condition_names']=len(set(CHECKS))
    if args.math_only:
        print(json.dumps(result,sort_keys=True));return
    result['source_sha256']={name:digest(HERE/name) for name in ('verify.py','RESULT.md')}
    path=HERE/'receipt.json'
    if args.write:path.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    else:
        stored=json.loads(path.read_text())
        if stored!=result:raise RuntimeError('IMMUTABLE_RECEIPT_MISMATCH')
    print('PASS_NATIVE_AF_COHERENT_COST_INFO',result['conditions_executed'],json.dumps(result['exact']))
if __name__=='__main__':main()
