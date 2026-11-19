#!/usr/bin/env python3
"""Scoped original no-reset CAR16/full128 one-tick Holevo bound and two-tick
memory/price replay. No independent geometric GR source or physical
Book03 H+J+R action is selected. Only standard NumPy/SciPy and existing
native_excerpt.py (actual original 128 Kraus) are required.
Runs identically under python3 and python3 -O.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import numpy as np

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent
           / "d0_native65_causal_source_2026-10-22")
)
from native_excerpt import native

P = (math.sqrt(5) - 1.0) / 2.0
ELL = math.log(1.0/P)
NTEST = 0

def check(cond, label):
    global NTEST
    NTEST += 1
    if not bool(cond):
        raise ArithmeticError(label)

def near(a, b, eps, label):
    check(abs(a-b)<eps, label+f": {a} != {b}")

def Hnat(weights):
    x=np.asarray(weights).ravel()
    x=x[x>1e-16]
    return float(-np.dot(x,np.log(x)))

def vnentropy(X):
    evals=np.linalg.eigvalsh((X+X.conj().T)*0.5)
    check(evals.min()>-1e-11, "conditional density positive")
    ev=evals[evals>1e-13]
    return float(-np.dot(ev,np.log(ev)))

def main():
    r=1/9
    K,_=native(2*math.atanh(r), 0.6, (1j,1j,-1.0,-1j))
    check(K.shape==(128,16,16), "literal original full128")
    eye=np.eye(16,dtype=complex)
    C=np.einsum("aij,aik->jk", K.conj(),K,optimize=True)
    near(float(np.linalg.norm(C-eye)),0,1e-11, "all128 Kraus CPTP")
    Delta=(eye-K[0])/(2*P*P)
    inv=np.linalg.inv(Delta)
    rho=inv/np.trace(inv)
    uncond=np.einsum("aij,jk,alk->il",K,rho,K.conj(),optimize=True)
    near(float(np.linalg.norm(uncond-rho)),0,1e-11,
         "unique previously owned original inverse-square stationary DATA")
    X=np.einsum("aij,jk,alk->ail",K,rho,K.conj(),optimize=True)
    q=np.maximum(np.trace(X,axis1=1,axis2=2).real,0)
    near(float(q.sum()),1,1e-11,"original unconditioned fine Born normalization")
    A=np.einsum("aij,aik->ajk",K.conj(),K,optimize=True)
    P2=np.maximum(np.einsum("aij,bji->ab",X,A,optimize=True).real,0)
    near(float(P2.sum()),1,1e-11,"genuine no-reset 128x128 normalization")
    near(float(np.max(np.abs(P2.sum(axis=1)-q))),0,1e-11,
         "exact fine prefix marginal")
    H1=Hnat(q)
    H2=Hnat(P2)
    CHI = vnentropy(rho) - sum(
        prob*vnentropy(x/prob)
        for prob,x in zip(q,X) if prob>1e-15
    )
    check(0 < CHI < math.log(16), "strict original one-step Holevo information")
    MI_fine=2*H1-H2
    check(0<MI_fine<CHI,"true fine-past/future MI bounded by one-step Holevo")
    cbar=1+q[1::2].sum()
    s1=cbar-H1/ELL
    s_upper=s1+CHI/ELL
    near(s1,0.7283481307600606,1e-10,"original complete fine one-tick CQ")
    near(s_upper,0.728700489392904,1e-10,
         "ACTUAL previous native65 DATA-only one-tick CQ")
    check(s_upper-s1<0.001, "new sharp complete observer-entropy rate bracket")

    q1=float(q[1::2].sum())
    port=np.zeros((2,2))
    for a in range(2):
        for b in range(2):
            port[a,b]=float(P2[a::2,b::2].sum())
    marg=port.sum(axis=0)
    near(float(np.max(np.abs(marg-np.array([1-q1,q1])))),
         0,1e-11,"stationary full128 two-tick port marginals")
    delta=float(port[1,1]-q1*q1)
    check(delta>0, "genuine non-reset original positive port covariance")
    check((8*delta*delta) < MI_fine,
          "strict Pinsker certified-form lower inequality on finite sample")
    pinser_lower=s1+8*delta*delta/ELL
    check(s1 < pinser_lower < s_upper, "positive original price memory bracket")

    # Literal row-controlled Golden X reassigns only original j>0 twin labels.
    idx=np.arange(128)
    for j in range(1,64):
        idx[2*j],idx[2*j+1]=idx[2*j+1],idx[2*j]
    KX=K[idx]
    near(float(np.linalg.norm(
        np.einsum("aij,jk,alk->il",KX,rho,KX.conj(),optimize=True)
        -uncond)),0,1e-11,"original physical channel unchanged by native X")
    qX=q[idx]
    near(Hnat(qX),H1,1e-12,"entire original one-tick fine Shannon invariant")
    PX2=P2[np.ix_(idx,idx)]
    near(Hnat(PX2),H2,1e-12,
         "entire original two-tick no-reset fine Shannon invariant")
    qNB=float(q[2:].sum())
    mu=float(np.trace(Delta).real)/16
    h=16/float(np.trace(inv).real)
    near(qNB,4*P*P*h*(1-mu),1e-11,
         "original exactly derived CAR16 nonblank effect")
    cbarX=1+qX[1::2].sum()
    near(cbar-cbarX,P**3*qNB,1e-11,
         "original conditional X full recorded terminal-price shift")
    check((1-P**3)*qNB>0,
          "genuinely paid one-extra-record-change original orientation wins")
    muprime=-328779/204800000
    hprime=-20040939/9885993640
    diffboost=4*P**5*(hprime*(1-mu)-h*muprime)
    near(diffboost,-0.0007130815017834955,1e-12,
         "original rigorous-signed rational boost derivative of price shift")

    print(json.dumps({
      "status":"PASS_ORIGINAL_FULL128_HOLEVO_RATE_BRACKET_BOUNDED_REPLAY",
      "checks":NTEST,
      "one_tick_H_fine_nats":H1,
      "two_tick_H_fine_nats":H2,
      "one_tick_Holevo_nats":CHI,
      "stationary_fine_Golden_rate_lower":s1,
      "stationary_Golden_rate_upper_DATA_cut":s_upper,
      "rate_interval_width_Golden":CHI/ELL,
      "strict_true_2tick_mutual_information_nats":MI_fine,
      "true_original_coarse_port_covariance":delta,
      "exact_formula_nonblank_probability":qNB,
      "uncharged_X_source_price_saving_per_tick":P**3*qNB,
      "paid_X_extra_cost_lower_than_original_per_tick":False,
      "compulsory_Book03_HJR_and_GR_closed":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
