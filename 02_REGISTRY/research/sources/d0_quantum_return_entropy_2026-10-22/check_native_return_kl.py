#!/usr/bin/env python3
"""Full128 native non-reset port first-return measured KL source.

The native Fourier/CAR/Golden construction is loaded UNCHANGED by AST,
with a pinned SHA256. Original 128 recorded labels and all16 CAR modes
are used. The coarse port comparison retains every finite cap-abort.
No iid/Markov replacement, selected Book03 Info or GR claim.

Run from repo root:
  OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_quantum_return_entropy_2026-10-22/check_native_return_kl.py
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm, solve_sylvester

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
PIN = "1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9"
P = (math.sqrt(5)-1)/2
ELL = math.log(1/P)
I = np.eye(16, dtype=complex)
CHECKS = 0

def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not bool(ok):
        raise ArithmeticError(message)

def close(x,y,tol,message):
    require(abs(x-y)<tol, message + f": {x} vs {y}; tol={tol}")

def native_constructor():
    raw=SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,
            "literal unchanged native source SHA256 pin")
    tree=ast.parse(raw)
    names={"adj","herm","root","creators","native"}
    body=[n for n in tree.body
          if isinstance(n,ast.FunctionDef) and n.name in names]
    require({n.name for n in body}==names,
            "all five original CAR16 constructor functions")
    env={"np":np,"P":P,"EYE":I,"expm":expm,
         "solve_sylvester":solve_sylvester,"RR":128,"Z":2**-20}
    exec(compile(ast.Module(body=body,type_ignores=[]),str(SOURCE),"exec"),env)
    return env["native"]

def port_maps(k):
    """Original full 128 Kraus, row-vectorized 16x16 DATA superoperators."""
    out=[]
    for parity in (0,1):
        superop=np.zeros((256,256),complex)
        for op in k[parity::2]:
            superop+=np.kron(op,op.conj())
        out.append(superop)
    return out

def fine_two_MI(k,rho):
    """REAL 128-fine-output two-round MI; dark outcomes stay in full space."""
    effects=np.matmul(k.conj().transpose(0,2,1),k)
    prob=np.einsum("bij,ji->b",effects,rho).real
    active=np.flatnonzero(prob>1e-14)
    require(len(active)==64,"proper-boost original fine support is 64/128")
    cond=np.matmul(np.matmul(k[active],rho),
                   k[active].conj().transpose(0,2,1))
    joint=np.einsum("bij,aji->ab",effects[active],cond).real
    q=prob[active]
    close(float(sum(q)),1.,2e-11,"full native fine archive normalized")
    close(float(np.linalg.norm(joint.sum(axis=0)-q)),0.,2e-11,
          "true native second fine marginal")
    close(float(np.linalg.norm(joint.sum(axis=1)-q)),0.,2e-11,
          "true native first fine marginal")
    require(bool(np.all(joint>0)),"positive active fine pairs")
    return float(np.sum(joint*np.log(joint/(q[:,None]*q[None,:]))))

def harmonic(r):
    """Already-owned exact ORIGINAL CAR16 quadratic spectral polynomial."""
    mu=9*(5*r**4+r**3-8*r**2-r+5)/(3200*(1-r*r)**2)
    det=81*(23*r**4+6*r**3-32*r*r-10*r+25)/(10240000*(1-r*r)**2)
    return det/mu

def nu_constant_native_port(r):
    # The original harmonic native energy scales exactly as nu^2.
    return .6*math.sqrt(harmonic(1/9)/harmonic(r))

def kl_bernoulli(a,b):
    d=a-b
    return a*math.log1p(d/b)+(1-a)*math.log1p(-d/(1-b))

def run(native,r,nu,K,check=False):
    k,_=native(2*math.atanh(r),nu)
    require(k.shape==(128,16,16),"full original 128 x CAR16 column")
    delta=(I-k[0])/(2*P**2)
    delta=(delta+delta.conj().T)/2
    rho=np.linalg.inv(delta)
    rho/=np.trace(rho)
    col=rho.reshape(-1)
    trace=I.reshape(-1)
    maps=port_maps(k)
    q=np.array([float(np.real(trace@(op@col))) for op in maps])
    require(bool(np.all(q>0)) and abs(sum(q)-1)<1e-11,
            "complete native two-port Born probabilities")
    close(float(np.linalg.norm((maps[0]+maps[1])@col-col)),0.,3e-11,
          "actually generated stationary native DATA marginal")
    pairs=np.array([[float(np.real(trace@(b@(a@col)))) for b in maps]
                    for a in maps])
    mi=float(np.sum(pairs*np.log(pairs/(q[:,None]*q[None,:]))))
    entropy_one=-sum(float(x)*math.log(float(x)) for x in q)
    KL=chain=H=C=mean=prob=abort=0.
    for a in (0,1):
        alive=maps[a]@col
        for j in range(1,K+1):
            incoming=float(np.real(trace@alive))
            if incoming<1e-250:
                # Real branch remains positive; this numerical threshold
                # is negligible relative to the INDEPENDENT ANALYTIC tail.
                alive=np.zeros_like(alive)
                break
            match=max(0.,float(np.real(trace@(maps[a]@alive))))
            if check:
                p_next=match/incoming
                chain+=incoming*kl_bernoulli(p_next,float(q[a]))
            iid=q[a]*q[1-a]**(j-1)*q[a]
            if match:
                KL+=match*math.log(match/iid)
                H-=match*math.log(match)
                mean+=match*(j+1)
                C+=match*(2*(a+1)+(j-1)*(2-a))
                prob+=match
            alive=maps[1-a]@alive
        remain=max(0.,float(np.real(trace@alive)))
        ref=q[a]*q[1-a]**K
        if remain:
            KL+=remain*math.log(remain/ref)
            H-=remain*math.log(remain)
            mean+=remain*(K+1)
            C+=remain*((a+1)+K*(2-a))
            prob+=remain
        abort+=remain
    if check:
        # The real log reference is iid at the same q, not a Golden
        # physical reset; real actual paths remain correlated.
        close(prob,1.,1e-11,"complete original match/abort normalization")
        close(KL,chain,1e-12,"independent complete KL: leaf vs conditional tree")
        n1=C-mean; n0=2*mean-C
        cross=-n0*math.log(q[0])-n1*math.log(q[1])
        close(KL,cross-H,1e-12,"full stopped entropy and actual 0/10 code")
        e1=np.sum(k[1::2].conj().transpose(0,2,1)@k[1::2],axis=0)
        close(float(np.linalg.norm(e1-4*P**3*delta)),0.,1e-11,
              "unchanged original Golden effect E_port1=4p^3 Delta")
        q_exact=4*P**3*(16/np.trace(np.linalg.inv(delta)).real)
        close(float(q[1]),q_exact,1e-11,
              "native Golden port probability equals harmonic CAR energy")
        fine_mi=fine_two_MI(k,rho)
        require(fine_mi>mi>1e-10,"actual fine archive MI > original port MI")
        require(KL>fine_mi,"whole coarse stopped KL bounds first-two fine MI numerically")
    else:
        fine_mi=None
    evals=np.linalg.eigvalsh(delta)
    a,b=4*P**3*float(evals[0]),4*P**3*float(evals[-1])
    require(a>0 and b<1,"strict full native port effects")
    chi=(b-a)**2/(q[1]*q[0])
    # EXACT theorem, numerically evaluated; every conditional port1
    # probability in [a,b] by its native positive E1=4p^3 Delta.
    tail=chi*(q[0]*b**K/(1-b)+q[1]*(1-a)**K/a)
    rho_e=np.linalg.eigvalsh(rho)
    S=-float(sum(x*math.log(x) for x in rho_e))
    return dict(q=q.tolist(),MI2_port_nats=mi,MI2_fullfine_nats=fine_mi,
                KL_stop_port_nats=KL,whole_port_entropy_nats=H,
                one_port_entropy_nats=entropy_one,mean_native_rounds=mean,
                actual_port_code_mean=C,cap_abort=abort,
                holevo_upper_nats=2*S,analytic_KL_tail_bound=tail,
                port_effect_interval=[a,b])

def main():
    native=native_constructor()
    K=3500
    r0=1/9
    base=run(native,r0,.6,K,True)
    require(base["KL_stop_port_nats"]>base["MI2_fullfine_nats"]>0,
            "strict stopped-memory information beyond two native fine records")
    require(base["KL_stop_port_nats"]<base["holevo_upper_nats"],
            "real native quantum predictive-memory capacity budget")
    require(base["analytic_KL_tail_bound"]<1e-20,
            "true uncapped stopping KL tail is analytically tiny")
    # Genuine original unpadded native 0/10 measured Price-Info, NOT
    # the separate padded N1 CQ field source.
    q=base["q"]
    S1=1+q[1]-base["one_port_entropy_nats"]/ELL
    S_capped=base["actual_port_code_mean"]-base["whole_port_entropy_nats"]/ELL
    S_inf=3*S1+base["KL_stop_port_nats"]/ELL
    close(S_capped,S_inf,1e-10,
          "native measured Golden complete price and correct stopped clock tail")
    sources=[]
    for step in (1e-3,5e-4,2.5e-4):
        left=run(native,r0-step,nu_constant_native_port(r0-step),K)
        right=run(native,r0+step,nu_constant_native_port(r0+step),K)
        dq=(right["q"][1]-left["q"][1])/(2*step)
        dKL=(right["KL_stop_port_nats"]-left["KL_stop_port_nats"])/(2*step)
        dMI=(right["MI2_port_nats"]-left["MI2_port_nats"])/(2*step)
        require(abs(dq)<1e-10,"real CAR two-parameter port-invisible tangent")
        require(5.5e-7<dKL<6.3e-7,
                "nonzero full STOPPED native measured first source: NUMERICAL")
        require(8e-9<dMI<1e-8,"original two-port first source persists")
        sources.append(dict(step=step,Dq=dq,D_KL_nats=dKL,
                            D_KL_golden_units=dKL/ELL,D_first2MI_nats=dMI))
    require(max(x["D_KL_nats"] for x in sources)-
            min(x["D_KL_nats"] for x in sources)<8e-11,
            "three independent finite-difference steps stable")
    print(json.dumps(dict(status="NUMERICAL_NATIVE_PASS",
       proven_operator_identities="ANALYTICAL_PARENT_NOTE",
       pinned_original_constructor_sha256=PIN,
       pinned_original_blob="ee8de4635d24c668949ac9a0186616ab7d59f2ed",
       checks=CHECKS,K=K,native=base,
       original_one_port_invisible_direction=sources,
       entire_128_fine_stopped_info_numerical=False,
       compulsory_Book03_Info_selected=False,
       independent_upstream_Euler_closed=False,
       GR_closed=False),indent=2))

if __name__=="__main__":
    main()
