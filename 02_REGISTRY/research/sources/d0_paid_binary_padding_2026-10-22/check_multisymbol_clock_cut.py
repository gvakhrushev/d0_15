#!/usr/bin/env python3
"""Any finite measured native code alphabet: unique minimum positive timing pad.

Also checks a CRITICAL negative control: an individually fixed-duration
Golden report does not make the TOTAL first-match stopping clock time-blind.
This is NOT a physically compulsory observer task or native Book03 Info.
"""
from __future__ import annotations
import json
import math
import sympy as sp

def require(cond,label):
    if not bool(cond): raise AssertionError(label)

def exact_multioutcome():
    q1,q2,q3=sp.symbols("q1 q2 q3",positive=True)
    q=[q1,q2,q3]
    native_lengths=(1,2,4)
    L=max(native_lengths)
    pads=tuple(L-v for v in native_lengths)
    raw=sum(a*b for a,b in zip(q,native_lengths))
    paid=sum(a*(b+c) for a,b,c in zip(q,native_lengths,pads))
    normalized=paid.subs(q3,1-q1-q2)
    require(sp.simplify(normalized-L)==0,"actual pad makes each COMPLETE report cost L")
    for var in (q1,q2):
        require(sp.diff(normalized,var)==0,"all off-null source jets of code Cost vanish")
        require(sp.diff(raw.subs(q3,1-q1-q2),var)!=0,
                "unpadded code has genuine outcome-price source")
    # General m proof: T is a deterministic function of retained symbol A.
    # I_phi(A;T)=H_phi(T)-H_phi(T|A)=H_phi(T).
    # Since every q_i>0, I_phi(A;T)=0 iff ALL T_i equal.
    # Nonnegative integer extras then obey d_i=L-l_i with L>=max(l_i),
    # and their unique cost-minimizer is the smallest possible L.
    return {
      "native_3_symbol_example_lengths":list(native_lengths),
      "unique_min_cost_positive_pads":list(pads),
      "clock_leak_identity":"I_phi(A;T)=H_phi(T); zero iff T is constant on positive support",
      "minimal_common_completion_tick":"max native original word length",
      "arbitrary_finite_alphabet":"d_i=max_j(ell_j)-ell_i >=0; actual Cost constant",
      "whole_record_entropy":"H(A,T)=H(A) (deterministic clock), not 2H(A)",
      "positive_extra_cost":"max_j(ell_j)-sum_i q_i ell_i"}

def firstmatch_clock_leak(r,limit=None):
    # Native first-match complete stopping law with every outcome retained.
    # Per-trial completion length 2 does NOT fix the total stop clock.
    p0=1-r;p1=r
    if limit is None:
        limit=max(160,int(math.ceil(36/min(p0,p1))))
    a0=p0*p0
    a1=p1*p1
    retained=0.0
    phi=(1+math.sqrt(5))/2
    info=0.0
    for n in range(limit):
        pn=a0+a1
        retained+=pn
        if a0>0:info+=a0*math.log(a0/(p0*pn),phi)
        if a1>0:info+=a1*math.log(a1/(p1*pn),phi)
        a0*=p1
        a1*=p0
    # Analytically account for the exact unenumerated geometric tails.
    tail=p0*p1**limit+p1*p0**limit
    require(abs(retained+tail-1)<1e-11,
            "positive original stopping law plus exact geometric tail")
    require(tail<1e-12,"numerical mutual-information tail is negligible")
    require(info>=-1e-12,"mutual information is nonnegative")
    if r!=0.5:require(info>1e-8,"whole stopped time leaks original initial bit")
    else:require(abs(info)<1e-12,"symmetric binary trial has no initial-bit clock leak")
    return {"native_click_r":r,"truncation_tail_probability":tail,
            "firstmatch_initial_bit_vs_total_time_MI_phi":info}

def finite_horizon():
    r,K=sp.symbols("r K",positive=True)
    p=sp.symbols("p",positive=True)
    lnphi=-sp.log(p)
    H=-(r*sp.log(r)+(1-r)*sp.log(1-r))/lnphi
    L=3-r**K-(1-r)**K
    # At cap K the COMPLETE stopped history has measured entropy L_K*H.
    # Keep every all-mismatch/abort path and its exact native probability.
    # Now PAY deterministic idle completion through K+1 full report slots,
    # and K comparison slots at fixed positive comparator price c.
    c=sp.symbols("c",nonnegative=True)
    price_fixed=2*(K+1)+c*K-L*H
    derivative=sp.diff(price_fixed,r)
    require(sp.simplify(derivative+L*sp.diff(H,r)+H*sp.diff(L,r))==0,
            "fixed TOTAL clock price has FULL stopped-history entropy jet")
    # The stopped program with only per-trial code padding instead had
    # L_K*(2-H), and therefore a different finite-K source.
    price_variable=L*(2-H)+c*(L-1)
    require(sp.simplify(price_fixed-price_variable-
        (2+c)*(K+1-L))==0,
        "all remaining fixed-horizon idle/comparison slots PAID")
    require(sp.simplify(sp.diff(price_fixed-price_variable,r)
        +(2+c)*sp.diff(L,r))==0,
        "finite K source difference is actual paid tail completion")
    return {
      "cap_K_stop_mean":"L_K=3-r^K-(1-r)^K",
      "fixed_total_report_plus_comparator_charge":"2(K+1)+c K",
      "whole_stopped_measured_entropy":"L_K H_phi(r)",
      "fixed_horizon_total_price":"2(K+1)+c K-L_K H_phi(r)",
      "source":"-L_K dH_phi(r)-H_phi(r) dL_K",
      "extra_paid_after_early_stop":"(2+c)*(K+1-L_K)",
      "total_stop_clock_without_cap":"cannot be a bounded deterministic horizon"}

if __name__=="__main__":
    samples=[firstmatch_clock_leak(r) for r in (0.25,0.5,0.0001)]
    print(json.dumps({
      "status":"PASS_GENERAL_POSITIVE_GOLDEN_CLOCK_NONLEAK_AND_WALD_CAP",
      "general":exact_multioutcome(),
      "firstmatch_clock_negative_control":samples,
      "finite_fixed_horizon":finite_horizon(),
      "scope":{
        "physical_clock_privacy_compulsory":False,
        "paid_after_stop_idle_admitted":False,
        "Book03_info_identified_with_measured_entropy":False,
        "cap_K_physical_programme_selected":False,
        "whole_history_completion_time_hidden_by_per_trial_pad":False,
        "GR_closed":False}},indent=2))
