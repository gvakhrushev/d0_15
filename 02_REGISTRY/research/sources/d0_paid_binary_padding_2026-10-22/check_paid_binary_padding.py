#!/usr/bin/env python3
"""Positive paid ONE-unit idle after the SHORTER original Golden 0/10 outcome.

A distinct measured-CQ programme, conditional on genuine admission/cost of
deterministic branch-controlled idle. On the original fixed cap9/20 bank and
complete measured-pointer interface the FULL off-null first-source (and every
higher field jet) equals the already selected configured N=1 CQ scalar source.
This does NOT derive original compulsory Book03 Info or a physical GR minimum.

Run from repo root: python3 02_REGISTRY/research/sources/d0_paid_binary_padding_2026-10-22/check_paid_binary_padding.py
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import sys
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[4]
NATIVE_REL="02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py"
NATIVE_SHA="525b257ec671500bd02c4791f9579dbde2439f21"

def demand(statement,label):
    if not bool(statement):
        raise AssertionError(label)

def pinned_original():
    data=(ROOT/NATIVE_REL).read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    demand(actual==NATIVE_SHA,"pinned existing GoldenMaster native price changed")
    sys.path.insert(0,str((ROOT/NATIVE_REL).parent))
    from native_master import GoldenMaster
    return GoldenMaster

def analytic():
    r,K,p=sp.symbols("r K p",positive=True)
    ln_phi=-sp.log(p)  # p=phi^-1, so log(phi)>0
    H=-(r*sp.log(r)+(1-r)*sp.log(1-r))/ln_phi
    c_raw=1+r
    c_pad=(1-r)*(1+1)+r*(2+0)
    demand(sp.simplify(c_pad-2)==0,"equal complete code cost")
    demand(sp.simplify(sp.diff(c_raw-H,r)-sp.diff(c_pad-H,r)-1)==0,
           "raw report includes extra d r")
    demand(sp.simplify(sp.diff(c_pad-H,r)+sp.diff(H,r))==0,
           "paid report first source is negative actual Shannon differential")
    d0,d1=sp.symbols("d0 d1",integer=True,nonnegative=True)
    derivative=sp.diff((1-r)*(1+d0)+r*(2+d1),r)
    demand(derivative==1+d1-d0,"source-neutral extra integer charge")
    demand(sp.solve(derivative,d0)==[1+d1],
           "unique nonnegative integer branch charge family")
    # Exact geometric series for retained uncapped FIRST MATCH:
    # P(0,1^n,0)=(1-r)^2 r^n, P(1,0^n,1)=r^2(1-r)^n.
    # For physical r∈(0,1), the four explicit series below converge.
    zero_sum=(1-r)**2/(1-r)
    one_sum=r**2/r
    zero_n=(1-r)**2*r/(1-r)**2
    one_n=r**2*(1-r)/r**2
    demand(sp.simplify(zero_sum+one_sum-1)==0,
           "complete normalized uncapped first-match history")
    demand(sp.simplify(2*(zero_sum+one_sum)+zero_n+one_n-3)==0,
           "exact expected three full IID binary trials")
    H_stop=-((2*zero_sum+one_n)*sp.log(1-r)
             +(2*one_sum+zero_n)*sp.log(r))/ln_phi
    demand(sp.simplify(H_stop-3*H)==0,
           "WHOLE complete first-match tape Shannon entropy = 3 H")
    demand(sp.simplify(6-H_stop-3*(2-H))==0,
           "true retained stopped Cost minus measured Info")
    L=3-r**K-(1-r)**K
    S_cap=L*(2-H)
    D_cap=sp.diff(S_cap,r)
    demand(sp.simplify(D_cap+L*sp.diff(H,r)-(2-H)*sp.diff(L,r))==0,
           "finite-K clock source contains complete boundary derivative")
    for kk in (1,2,5,10,20):
        dc=sp.simplify((sp.diff(L,r)+K*r**(K-1)
                        -K*(1-r)**(K-1)).subs(K,kk))
        demand(dc==0,"finite-K derivative true")
    demand(L.subs(K,1)==2,"single later trial has fixed length two")
    demand(sp.simplify(L.subs(K,2)-(3-r*r-(1-r)**2))==0,
           "finite two-later-trial normalization")
    return {
      "native_code_costs":{"outcome_0":1,"outcome_10":2},
      "additional_PAID_identity":{"after_0":1,"after_10":0},
      "full_length_PER_complete_trial":2,
      "minimal_nonnegative_integer_policy":"d0=d1+1; minimum(d0,d1)=(1,0)",
      "uncapped_firstmatch":{"mean_complete_trials":3,
        "mean_padded_report_cost":6,"whole_history_entropy":"3*H_phi(r)"},
      "finite_stop_K":"L_K=3-r^K-(1-r)^K; dS_K=−L_K H'(r)dr+(2−H)dL_K",
      "no_capped_source_neutrality_claim":True}

def original_native():
    GoldenMaster=pinned_original()
    native=GoldenMaster(65)
    phi_log=mp.log(1/native.p)
    gamma=native.alpha*native.beta
    demand(native.a<0 and native.b>0,"original N1 sigma-minus source sign")
    demand(mp.mpf(0)<native.r0<mp.mpf(1),"native complete positive click")
    def S_conf(x,y):
        return native.F(x,y)  # exactly −alpha beta [H(r)−H(r0)]
    def S_pad(x,y):
        r=native.raw_probability(x,-y)
        return gamma*(mp.mpf(2)-native.entropy(r))
    def S_raw(x,y):
        r=native.raw_probability(x,-y)
        return gamma*(1+r-native.entropy(r))
    const=gamma*(2-native.entropy(native.r0))
    controls=[]
    for xs,ys in (("0","0"),("0.00017","-0.00011"),
                  ("-0.00023","0.00041")):
        x,y=mp.mpf(xs),mp.mpf(ys)
        r=native.raw_probability(x,-y)
        diff=S_pad(x,y)-S_conf(x,y)
        demand(abs(diff-const)<mp.mpf("1e-55"),
               "entire full native N1 PRICE differs only by a constant")
        sx=mp.diff(lambda xx:S_pad(xx,y)-S_conf(xx,y),x)
        sy=mp.diff(lambda yy:S_pad(x,yy)-S_conf(x,yy),y)
        sxx=mp.diff(lambda xx:S_pad(xx,y)-S_conf(xx,y),x,2)
        syy=mp.diff(lambda yy:S_pad(x,yy)-S_conf(x,yy),y,2)
        demand(max(abs(t) for t in (sx,sy,sxx,syy))<mp.mpf("1e-55"),
               "full off-null geometry and material gradient/Hessian match")
        extra=mp.diff(lambda xx:S_raw(xx,y)-S_conf(xx,y),x)
        expected=gamma*mp.diff(lambda xx:native.raw_probability(xx,-y),x)
        demand(abs(extra-expected)<mp.mpf("1e-55"),
               "raw code adds genuinely nonzero gamma * d r")
        demand(abs(extra)>mp.mpf("1e-14"),
               "negative control: original unpadded Price differs in source")
        controls.append({"x":xs,"y":ys,"true_native_click":mp.nstr(r,31),
                         "source_difference_x":mp.nstr(sx,9),
                         "source_difference_y":mp.nstr(sy,9),
                         "Hessian_difference_xx":mp.nstr(sxx,9),
                         "Hessian_difference_yy":mp.nstr(syy,9),
                         "unpaid_raw_code_extra_gradient_x":mp.nstr(extra,20)})
    return {"original_bank_caps":[9,20],"readiness":mp.nstr(gamma,31),
            "r_null":mp.nstr(native.r0,31),
            "fixed_value_difference":mp.nstr(const,31),
            "three_same_native_offnull_samples":controls}

if __name__=="__main__":
    print(json.dumps({
      "status":"PASS_MINIMAL_POSITIVE_GOLDEN_REPORT_CHARGE_SOURCE",
      "exact":analytic(),"native":original_native(),
      "scope":{
        "positive_conditional_idle_charge_physically_admitted":False,
        "original_Golden_0_10_report_retained":True,
        "all_failed_factory_transcripts_paid_conditionally":True,
        "unchanged_native_complete_CQ_field_price_fixed_input":True,
        "actual_unmeasured_Book03_operator_heat_price_equated":False,
        "full_field_moving_upstream_work_clock_source_solved":False,
        "source_and_Hessian_match_for_any_all42_pullback":True,
        "physically_compulsory_D0_selection_proved":False,
        "GR_closed":False
      }
    },indent=2))
