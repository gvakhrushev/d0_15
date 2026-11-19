"""Check the H.1 root weight, both LIVE branches, and the necessary cost gap."""
from fractions import Fraction as F
from math import exp, factorial, log
from itertools import product
import json
import numpy as np

from check_extra_work import Span, span
from check_live_parser import controller, terminal, traces
from check_local_gibbs_records import build, halo, mm, scene, scene_heat
from check_reference_pf_path import binary_kl, ln_interval
from check_repeat_clock import local_native
from check_source_price import load_control, need


def entropy(q):
    return -q*ln_interval(q)-(1-q)*ln_interval(1-q)


def certify_roots(q, ell):
    entropy0=entropy(q)
    out=[]
    for lower, upper, decreasing in [
            ("0.0324276829699111","0.0324276829699113",True),
            ("0.8736311345495272","0.8736311345495275",False)]:
        lo,hi=map(lambda x:span(F(x)), (lower,upper))
        left=binary_kl(q,lo)-entropy0
        right=binary_kl(q,hi)-entropy0
        need(left.lo>0 and right.hi<0 if decreasing else left.hi<0 and right.lo>0,
             "outward rational brackets straddle the unique monotone KL root")
        r=Span(lo.lo,hi.hi)
        price=ln_interval((1-r)/r)/ell
        out.append({"error_reference":r.fmt(16),"effective_price_gap":price.fmt(13),
                    "additional_gap_beyond_actual_codes":(price-1).fmt(13)})
    return out


def ledger():
    p=(span(5).sqrt()-1)/2
    q=p**2
    ell=ln_interval(1/p)
    for h,t,x in product(range(2),repeat=3):
        d=t^x
        labels=terminal(t,d,h^d,0,0,0,0)
        measured=sum(map(len,labels))
        branch=5+t+x if h else (4+3*x if not t else 7-x)
        need(measured==branch,"fine native four-code price on both H branches")
    gain=entropy(q)/ell
    need((gain-1-q).lo<=0<=(gain-1-q).hi,"golden entropy")
    coeff=q+(1-q)*(3-4*q)
    delta_pi=p**3*(2*p**3-q)
    need((delta_pi-p**8).lo<=0<=(delta_pi-p**8).hi,"two original NPS bank outputs")
    # Even / odd Taylor polynomials enclose exp(-2*beta) by the integral remainder.
    a=4*q
    exp_lo=sum(((-1)**j*a**j/factorial(j) for j in range(42)),span(0))
    exp_hi=exp_lo+a**42/factorial(42)
    damping=Span(exp_lo.lo,exp_hi.hi)
    z=F(1,2**20)
    corridor=(ln_interval(425/(359+66*damping))-4*ln_interval(span(1-z)))/ell
    pi0=q+p**3*q
    pi1=pi0+delta_pi
    old=2*(entropy(pi1)-entropy(pi0))/ell-delta_pi
    delta=coeff*delta_pi
    least=next(m for m in range(1,100) if (m*delta-old).lo>corridor.hi)
    need(((least-1)*delta-old).hi<corridor.lo,"previous cap not excluded by this corridor")
    return {"thresholds":certify_roots(q,ell),"native_bank_difference":delta_pi.fmt(15),
        "required_negative_per_copy_magnitude_all_H":delta.fmt(15),
        "both_grade_log_phi_partition_corridor_rank4":corridor.fmt(15),
        "old_two_state_report_only_bellman_secant":old.fmt(15),
        "first_M_excluded_by_this_universal_bound_for_stated_ledger":least,
        "absolute_pressure_ledger_physical_selection_verified":False}


def native_root():
    ne,digest=load_control()
    T,cuts,last,V,J=build(ne,0)
    p=float(ne.P)
    beta=2*p*p
    B,C=scene()
    eig,U=np.linalg.eigh(T+T.T)
    heat=[scene_heat(B,C,v,beta) for v in eig]
    K0=mm(U*np.array([h[32,32] for h in heat])[None,:],U.T)
    K=mm(last,K0[cuts[-1],cuts[-1]],last.T)
    reference=np.array([1.,0.,0.,1.])/np.sqrt(2.)
    psi=mm(np.kron(V,np.eye(2)),reference)
    targets=[]
    probs=[]
    for bits in ([1,1,0,0],[0,0,1,0],[0,0,0,1]):
        v=mm(np.kron(np.eye(2),np.kron(np.diag(bits),np.eye(2))),psi)
        probs.append(float(v@v))
        targets.append(float(exp(J)*v@mm(np.kron(K,np.eye(2)),v)))
    need(probs[-1]<1e-27 and targets[-1]<1e-27,"dark 11 retained")
    mass=sum(targets)
    ell=-log(p)
    k=p+p*p
    s0=-log(mass/k)/ell
    for price,weight in zip((1,2),targets[:2]):
        g=log((weight/mass)/(p**price/k))/ell
        need(abs(p**(s0+price-g)-weight)<1e-14,"sign and absolute scale of root work")
        need(abs(p**(price-g)-k*weight/mass)<1e-14,"uncalibrated leaf keeps only ratios")
    S=sum(scene_heat(B,C,2*np.cos(2*np.pi*j/128),beta) for j in range(128))/128
    ZH=359*len(T)+2*sum(np.trace(h) for h in heat)
    ZN=exp(J)*ZH
    physical_scale=len(T)*(359+2*np.trace(S))/S[32,32]
    err=(exp(2*beta)+66/359)*2*halo(beta/11,4)
    need(abs(log(physical_scale*mass/ZN))<err,"full graph including grade one and feedback")
    # Exact rational independent test of the tree recursion on a variable-depth support.
    branches={"0":(F(2,5),F(5,17)), "10":(F(1,10),F(2,17)), "11":(F(1,8),F(1,17))}
    k=sum(v[0] for v in branches.values()); a=sum(v[1] for v in branches.values())
    k1=branches["10"][0]+branches["11"][0]
    a1=branches["10"][1]+branches["11"][1]
    for name,(cost_weight,target) in branches.items():
        blend=(target/a)/(cost_weight/k) if name=="0" else (a1/a)/(k1/k)*(target/a1)/(cost_weight/k1)
        need(a/k*cost_weight*blend==target,"exact tree with conditional suffix normalizers")
    return {"native_sha256":digest,"native_clock_D":len(T),"both_degree_modes":425*len(T),
         "leaf_probabilities":[round(t,10) for t in probs],"absolute_raw_root":round(mass,10),
         "root_charge_gold_units":round(s0,10),"root_charge_includes_separate_layout_scale":False}


if __name__=="__main__":
    local_native()
    controller()
    traces()
    print(json.dumps({"status":"PASS","root_check":native_root(),"live_check":ledger()},
                     ensure_ascii=False,sort_keys=True,indent=2))
