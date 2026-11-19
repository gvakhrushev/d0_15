#!/usr/bin/env python3
"""Original CAR16 full128 no-reset first-match harmonic return quantum transfer LOG.

Loads the UNCHANGED original source by its EXACT Git blob SHA; every original
Kraus and real proper boost first jet retained. Same preparation, no DATA
reset, all fine word register slots and oldRIGHT spectator preserved.

H_inf=sum_a Tr[-log(I-T_a) I_a(rho*)], genuine complete original PORT return.
Its moving full source uses the actual d(K_alpha), d(rho*) AND d(T_a).
The complete Shannon/KL of the SAME first-return port history is separately
computed; the harmonic reward is NOT its Shannon reward.
Exponential K3900 value/first-source tail certificates are analytic.
The fully selected Book03 Hodge and vertex Info, independent physical
preparation/input Euler, 42-field writer, raw216 and GR are NOT certified.

Run from PR checkout:
 OPENBLAS_NUM_THREADS=1 python3 \
  02_REGISTRY/research/sources/d0_native_transfer_harmonic_2026-10-22/check_original_quantum_harmonic.py
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm, logm, solve_sylvester

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
PIN="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P=(math.sqrt(5)-1)/2
LNPHI=math.log(1/P)
EYE=np.eye(16,dtype=complex)
TESTS=0
def test(condition,msg):
    global TESTS
    TESTS+=1
    if not bool(condition):
        raise ArithmeticError(msg)
def close(value,expected,atol,msg):
    test(abs(value-expected)<atol,
         f"{msg}: {value} != {expected}, atol={atol}")

def native_pinned():
    raw=SOURCE.read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    test(blob==PIN,"original literal 128 Kraus Git blob immutable")
    tree=ast.parse(raw)
    want={"adj","herm","root","creators","native"}
    defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in want]
    test(set(n.name for n in defs)==want,"original five CAR16 native Julia constructor defs")
    ns={"np":np,"EYE":EYE,"P":P,"expm":expm,
        "solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(SOURCE),"exec"),ns)
    return ns["native"],blob

def matrices(native,r,nu):
    K,DKtheta=native(2*math.atanh(r),nu)
    DK=DKtheta*2/(1-r*r)
    test(K.shape==(128,16,16) and DK.shape==K.shape,
         "all original 128 CAR Kraus and moving real boost first jets")
    compl=np.sum(K.conj().transpose(0,2,1)@K,axis=0)
    close(float(np.linalg.norm(compl-EYE)),0,5e-12,
          "all original 128 labels complete, no herald/postselection")
    t=2*P*P
    Delta=(EYE-K[0])/t
    dDelta=-DK[0]/t
    R=np.linalg.inv(Delta)
    dR=-R@dDelta@R
    Z=float(np.trace(R).real)
    dZ=float(np.trace(dR).real)
    rho=R/Z
    drho=dR/Z-R*(dZ/Z**2)
    close(float(np.trace(rho).real),1.,1e-12,
          "original stationary rho*=Delta^-1/TrDelta^-1")
    close(float(np.trace(drho).real),0.,1e-12,
          "real moving preparation first source, not pinned rho")
    tr=EYE.reshape(-1).conj()
    x=rho.reshape(-1)
    dx=drho.reshape(-1)
    mats=[]; dots=[]; etas=[]; Ls=[]
    for a in (0,1):
        M=np.zeros((256,256),complex)
        dM=np.zeros_like(M)
        E=np.zeros((16,16),complex)
        l=0.
        for k,dk in zip(K[a::2],DK[a::2]):
            M+=np.kron(k,k.conj())
            dM+=np.kron(dk,k.conj())+np.kron(k,dk.conj())
            E+=k.conj().T@k
            l+=2*np.linalg.norm(k,ord=2)*np.linalg.norm(dk,ord=2)
        mats.append(M);dots.append(dM)
        etas.append(float(np.linalg.eigvalsh((E+E.conj().T)/2).min()))
        Ls.append(float(l))
    close(np.linalg.norm((mats[0]+mats[1])@x-x),0,3e-11,
          "original moving rho stationary under COMPLETE native CPTP Phi")
    test(min(etas)>0 and etas[0]>.98 and etas[1]>.0125,
         "genuine ORIGINAL coarse native port effects have uniform positive floors")
    test(max(Ls)<91 and float(np.linalg.norm(drho,ord="nuc"))<210,
         "strict original native derivative-norm margin for certified C1 tail")
    return K,DK,x,dx,tr,mats,dots,etas,Ls

def harmonic(native,r,nu,Kcap,with_details=True):
    _,_,rho,drho,tr,mats,dots,etas,Ls=matrices(native,r,nu)
    q=[float((tr@(m@rho)).real) for m in mats]
    dq=[float((tr@(dm@rho+m@drho)).real) for m,dm in zip(mats,dots)]
    close(sum(q),1.,1e-12,"original coarse PORT probabilities normalized")
    close(sum(dq),0.,3e-12,"original proper boost PORT probability jets conserved")
    H1=-sum(qi*math.log(qi) for qi in q)
    DH1=-sum(dqi*(math.log(qi)+1) for qi,dqi in zip(q,dq))
    info=0;dinfo=0;parts=[]
    for a in (0,1):
        T=mats[1-a];dT=dots[1-a]
        sigma=mats[a]@rho
        dsigma=dots[a]@rho+mats[a]@drho
        old=sigma.copy();dold=dsigma.copy()
        Ha=0;dHa=0
        for k in range(1,Kcap+1):
            cur=T@old
            dcur=T@dold+dT@old
            Ha+=float((tr@cur).real)/k
            dHa+=float((tr@dcur).real)/k
            old,dold=cur,dcur
        # Independent 256-dimensional matrix log of UNCHANGED original
        # nonselfadjoint quantum CP transfer, NO truncated-series fit.
        L=-logm(np.eye(256)-T)
        logval=tr@L@sigma
        close(float(logval.imag),0.,2e-12,
              "native quantum transfer log has REAL original harmonic source")
        close(Ha,float(logval.real),4e-14,
              "entire SAME original quantum return tail equals transfer LOG")
        qa=float((tr@sigma).real)
        info+=Ha;dinfo+=dHa
        parts.append({"anchor_port":a,"q_anchor":qa,
                      "original_eta_event_floor":etas[a],
                      "harmonic_full_log_value":float(logval.real),
                      "harmonic_Kcap_sum":Ha,
                      "harmonic_full_real_source_Kcap":dHa,
                      "native_coarse_effect_first_jet_bound":Ls[1-a]})
    pair=np.zeros((2,2))
    for a in range(2):
        for b in range(2):
            pair[a,b]=float((tr@(mats[b]@(mats[a]@rho))).real)
    covariance=pair[1,1]-q[1]**2
    test(covariance>2e-7,"genuine non-reset two-port covariance positive")
    firstcorr=-2*covariance
    qstatus=-sum(qi*math.log(qi) for qi in q)
    close(H1,qstatus,2e-14,"true first port Shannon")
    test((info-H1)<-1e-5,
         "actual ORIGINAL quantum harmonic waiting is NOT iid Shannon")
    test((dinfo-DH1)<-1.9e-4,
         "moving ORIGINAL native Info waiting source is NOT iid entropy source")
    alpha=(79/80)**Kcap
    # Conservative STRICT source: q<=1, event eta>=1/80, genuine original
    # ||D T||_{1->1, Herm}<91 and ||D sigma||_1<91+210=301,
    # both anchors included, all genuinely moving source components.
    value_tail=2*(79/80)**(Kcap+1)*80/(Kcap+1)
    source_tail=2*(91*alpha*80+301*alpha*80/(Kcap+1))
    test(value_tail<3e-23 and source_tail<1e-17,
         "ALL original no-reset return harmonic VALUE+FIRST SOURCE tails certified")
    return {"native_boost":r,"nu":nu,"full128_original":True,
            "actual_PORT_q":q,"full_proper_boost_q_source":dq,
            "actual_PORT_pair_probabilities":pair.tolist(),
            "actual_port_pair_covariance":covariance,
            "first_survival_harmonic_memory_correction":firstcorr,
            "native_iid_first_port_Shannon_nats":H1,
            "native_iid_Shannon_first_jet":DH1,
            "original_NO_RESET_harmonic_return_nats":info,
            "original_NO_RESET_harmonic_return_first_jet":dinfo,
            "harmonic_minus_Shannon_nats":info-H1,
            "harmonic_minus_Shannon_first_jet":dinfo-DH1,
            "actual_two_anchor_superoperator_logs":parts,
            "certified_harmonic_Kcap":Kcap,
            "analytic_VALUE_tail_upper":value_tail,
            "analytic_FIRST_JET_tail_upper":source_tail,
            "GR_closed":False}

def stopped_binary_kl(mats,tr,rho,q,K=3500):
    # Exact finite complete stopped PORT language, including every abort
    # without independent re-preparation of DATA and without losing labels.
    KL=0.;capmass=0.;expected_count=0.
    for a in (0,1):
        live=mats[a]@rho
        for n in range(1,K+1):
            success=float((tr@(mats[a]@live)).real)
            reference=q[a]*q[a]*q[1-a]**(n-1)
            if success>1e-290 and reference>1e-290:
                KL+=success*math.log(success/reference)
                expected_count+=success*(n+1)
            live=mats[1-a]@live
        abort=max(0.,float((tr@live).real))
        capmass+=abort
        ref=q[a]*q[1-a]**K
        if abort>0 and ref>0:
            KL+=abort*math.log(abort/ref)
            expected_count+=abort*(K+1)
    return KL,capmass,expected_count

def main():
    native,blob=native_pinned()
    r=1/9;nu=.6
    result=harmonic(native,r,nu,3900)
    _,_,rho,_,tr,mats,_,_,_=matrices(native,r,nu)
    kl,abort,mean=stopped_binary_kl(mats,tr,rho,result["actual_PORT_q"])
    test(1.5e-8<kl<1.7e-8,
         "TRUE same original stopped-history KL tiny but NOT harmonic source")
    test(abort<4e-22 and abs(mean-3)<2e-8,
         "all terminated/abort actual PORT records keep exact Kac mean=3")
    result.update({
        "status":"PASS_ORIGINAL_GIT_PINNED_NO_RESET_TRANSFER_LOG_INFO",
        "checks":TESTS,"literal_original_source_Git_blob":blob,
        "actual_same_full128_PORT_stopped_path_KL_nats":kl,
        "actual_stopped_K3500_total_ABORT":abort,
        "Kac_true_mean_full_trials":mean,
        "harmonic_information_correction_to_path_KL_ratio":
             abs(result["harmonic_minus_Shannon_nats"])/kl,
        "physical_selected_Book03_Info":False,
        "physical_selected_Book03_SCENE_Hodge":False,
        "physical_same_history_all42_GR_closed":False})
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
