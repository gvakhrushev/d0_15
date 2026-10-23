#!/usr/bin/env python3
"""Two TRUE original CAR16/full128 allblank Born probabilities -> ALL finite Hodge+Book jets.

Uses original all128 Kraus generator at its pinned Git BLOB SHA (not a synthetic
2x2 instrument), genuine oldRIGHT128, all registered harmonic zero modes, and
the analytic native role-1 proper boost. Never creates 128**n histories.
No selected Book03 scene Hodge/Info, paid Choi prep, GR or D_min claim.

Run in the existing PR checkout:
  OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_native_two_blank_hodge_recursion_2026-10-22/check_two_blank_complete_book.py

Optional local developer fixture-only smoke when raw checkout is unavailable:
  python3 .../check_two_blank_complete_book.py --transcription-smoke /path/to/native_formula_transcription.py
Smoke explicitly disables original Git-blob pin verification.
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm, solve_sylvester

SOURCE_REL = ("02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/"
              "check_uniform_book_source.py")
SOURCE_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P = (math.sqrt(5)-1)/2
BETA = 2*P*P
ZETA = 2**-20
NATIVE_MU = 141489/10240000
NATIVE_H = 69399/5030720
NATIVE_MU_JET = -328779/204800000
NATIVE_H_JET = -20040939/9885993640
IDENTITY = np.eye(16, dtype=complex)
CHECKS: list[str] = []

def check(assertion, label):
    if not bool(assertion):
        raise ArithmeticError(label)
    CHECKS.append(label)

def close(actual, expected, atol, label):
    check(abs(actual-expected)<atol,
          f"{label}: actual={actual} expected={expected}, tol={atol}")

def native_from_pinned_file():
    smoke = len(sys.argv)==3 and sys.argv[1]=="--transcription-smoke"
    if smoke:
        source=Path(sys.argv[2])
    else:
        check(len(sys.argv)==1, "expected no arguments or --transcription-smoke PATH")
        source=Path(__file__).resolve().parents[4]/SOURCE_REL
    raw=source.read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if not smoke:
        check(blob==SOURCE_BLOB,
              "EXACT unchanged native original all128 constructor Git blob pin")
    module=ast.parse(raw, filename=str(source))
    wanted={"adj","herm","root","creators","native"}
    selections=[node for node in module.body
                if isinstance(node,ast.FunctionDef) and node.name in wanted]
    check({node.name for node in selections}==wanted,
          "all five original all128 Fourier/JULIA/CAR constructor defs")
    namespace={"np":np,"P":P,"EYE":IDENTITY,"expm":expm,
               "solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=selections,type_ignores=[]),str(source),"exec"),
         namespace)
    return namespace["native"],not smoke,blob

def power_recurrence(blank1,blank2,jet1,jet2,length):
    # Cayley-Hamilton for the actual two eightfold x=eig(B**2).
    scalar=2*blank1
    det=2*blank1**2-blank2
    dscalar=2*jet1
    ddet=4*blank1*jet1-jet2
    trace=[2.,scalar]
    dtrace=[0.,dscalar]
    for k in range(2,length+1):
        trace.append(scalar*trace[k-1]-det*trace[k-2])
        dtrace.append(dscalar*trace[k-1]+scalar*dtrace[k-1]
                      -ddet*trace[k-2]-det*dtrace[k-2])
    return trace,dtrace,det,ddet

def factorial(n):
    acc=1
    for k in range(2,n+1):
        acc*=k
    return acc

def observable_functionals(n, blank1, blank2, jet1, jet2, heat_cap=20):
    trace,dtrace,det,ddet=power_recurrence(blank1,blank2,jet1,jet2,n*heat_cap)
    w_minus_one=(ZETA*(1-ZETA)*(trace[n]-2)
                 +ZETA**2*(det**n-1))
    w=1+w_minus_one
    dw=ZETA*(1-ZETA)*dtrace[n]+n*ZETA**2*det**(n-1)*ddet
    check(w>0 and w<=1+1e-12,"true logdet positive original native pencil")
    J=-1024*math.log1p(w_minus_one)
    DJ=-1024*dw/w
    value=deriv=0.
    term=1.
    for k in range(heat_cap+1):
        value+=term*trace[n*k]
        deriv+=term*dtrace[n*k]
        term*=BETA/(k+1)
    value*=math.exp(-BETA)
    deriv*=math.exp(-BETA)
    dimension=2048*128**n
    correction=(value-2)/128**n
    H=(math.log(2048)+n*math.log(128)+math.log1p(correction))/BETA
    Z=dimension-4096+2048*value
    DH=2048*deriv/(BETA*Z)
    heat_tail_bound=4096*BETA**(heat_cap+1)/factorial(heat_cap+1)
    check(heat_tail_bound<1e-13,"Poisson certified native complete Hodge tail")
    return dict(n=n,feedback=J,heat=H,source_feedback=DJ,
                source_heat=DH,source=DJ+DH,actual_dimension=dimension,
                true_zeros=dimension-4096,
                matrix_heat_trace=Z,heat_tail_upper=heat_tail_bound,
                characteristic_det=det)

def direct_native_matrix(n, B, dB):
    # Independent full CAR16 matrix evaluator; entire oldRIGHT128 inherited
    # as a tensor spectator, NO source-normalization by original dimension.
    powers=[IDENTITY]
    for _ in range(2*n):
        powers.append(powers[-1]@B)
    f=IDENTITY-powers[2*n]
    df=-sum((powers[j]@dB@powers[2*n-1-j]
             for j in range(2*n)),np.zeros_like(IDENTITY))
    f=(f+f.conj().T)/2
    df=(df+df.conj().T)/2
    eig,frame=np.linalg.eigh(f)
    check(eig.min()>0 and eig.max()<1,
          "all actual 16 CAR original F eigenvalues positive")
    Q=IDENTITY-ZETA*f
    J=-128*np.linalg.slogdet(Q)[1]
    DJ=128*ZETA*float(np.trace(np.linalg.solve(Q,df)).real)
    eh=(frame*np.exp(-BETA*eig))@frame.conj().T
    nfull=2048*128**n
    Z=nfull-4096+2*128*float(np.trace(eh).real)
    H=math.log(Z)/BETA
    DH=-2*128*float(np.trace(eh@df).real)/Z
    return dict(n=n,feedback=J,heat=H,source_feedback=DJ,
                source_heat=DH,source=DJ+DH)

def main():
    native,pinned,blob=native_from_pinned_file()
    r=1/9
    theta=2*math.atanh(r)
    ks,dks=native(theta,.6)
    check(ks.shape==(128,16,16) and dks.shape==ks.shape,
          "actual 128 original records, all 16 CAR grades")
    complete=(ks.conj().transpose(0,2,1)@ks).sum(axis=0)
    close(float(np.linalg.norm(complete-IDENTITY)),0,3e-13,
          "true original full128 complete NOT only blank history")
    B=ks[0]
    dB=dks[0]*(2/(1-r*r)) # original derivative is theta; field r=tanh(theta/2)
    close(float(np.linalg.norm(B-B.conj().T)),0,3e-13,
          "actual native labelled K0=B is positive Hermitian")
    eigB=np.linalg.eigvalsh(B)
    check(0<eigB.min() and eigB.max()<1,
          "true original blank K0 strictly positive contraction")
    Delta=(IDENTITY-B)/BETA
    dDelta=-dB/BETA
    mu=float(np.trace(Delta).real)/16
    h=16/float(np.trace(np.linalg.inv(Delta)).real)
    dmu=float(np.trace(dDelta).real)/16
    di=np.linalg.inv(Delta)
    dh=16*float(np.trace(di@dDelta@di).real)/float(np.trace(di).real)**2
    close(mu,NATIVE_MU,5e-14,"unaltered original rational CAR16 mean Delta")
    close(h,NATIVE_H,5e-14,"unaltered original rational CAR16 harmonic Delta")
    close(dmu,NATIVE_MU_JET,6e-13,"full moving genuine Lorentz mean first jet")
    close(dh,NATIVE_H_JET,6e-13,"full moving genuine Lorentz harmonic first jet")
    close(float(np.linalg.norm(Delta@Delta-2*mu*Delta+mu*h*IDENTITY)),
          0,1e-12,"ORIGINAL 16x16 quadratic spectrum from actual K0")
    b2=B@B
    db2=dB@B+B@dB
    b4=b2@b2
    db4=db2@b2+b2@db2
    blank1=float(np.trace(b2).real)/16
    blank2=float(np.trace(b4).real)/16
    jet1=float(np.trace(db2).real)/16
    jet2=float(np.trace(db4).real)/16
    check(0<blank2<blank1<1 and
          blank2>blank1**2 and 2*blank1**2-blank2>0,
          "TWO TRUE allblank probabilities yield positive native 2-mode spectrum")
    eps=math.sqrt(mu*(mu-h))
    x=[(1-BETA*(mu-eps))**2,(1-BETA*(mu+eps))**2]
    close(blank1,sum(x)/2,2e-13,"one original blank Born probability vs exact spectrum")
    close(blank2,sum(v*v for v in x)/2,2e-13,
          "TWO-round ORIGINAL 00 probability is NOT square of one round")
    close(blank2-blank1**2,((x[0]-x[1])/2)**2,2e-13,
          "native two-blank covariance captures the actual CAR16 spectral split")
    recovered=[blank1-math.sqrt(blank2-blank1**2),
               blank1+math.sqrt(blank2-blank1**2)]
    check(max(abs(u-v) for u,v in zip(sorted(x),sorted(recovered)))<4e-12,
          "EXACT positive two-eigen x-spectrum from just 2 native Born events")
    check(ZETA>0 and 1-ZETA>ZETA,"original positive Book03 calibration")
    dW1_db=-ZETA**2
    dJ1_db=-1024*dW1_db/((1-ZETA)**2+
             2*ZETA*(1-ZETA)*blank1+ZETA**2*(2*blank1**2-blank2))
    check(dJ1_db>0,"second blank event NECESSARY even for one-tick Book determinant")
    out=[]
    for n in (1,2,3,33,130):
        pred=observable_functionals(n,blank1,blank2,jet1,jet2)
        direct=direct_native_matrix(n,B,dB)
        close(pred["feedback"],direct["feedback"],3e-10,
              f"whole oldRIGHT original n={n} Book feedback value reconstructed")
        close(pred["heat"],direct["heat"],3e-10,
              f"entire original work+harmonic n={n} Hodge value reconstructed")
        close(pred["source_feedback"],direct["source_feedback"],3e-10,
              f"genuine noncommuting 16x16 n={n} Book first field source")
        close(pred["source_heat"],direct["source_heat"],3e-10,
              f"whole original Hodge n={n} first source")
        if n==1:
            check(pred["source"]>0,"original complete n1 native Hodge+J Ward >0")
        else:
            check(pred["source"]<0,"original complete n>=2 native Hodge+J Ward <0")
        out.append(dict(n=n,feedback=pred["feedback"],source=pred["source"],
                        source_direct=direct["source"],
                        true_harmonic_modes=pred["true_zeros"]))
    result={"status":"PASS" if pinned else "TRANSCRIPTION_SMOKE_PASS",
            "assertions":len(CHECKS),"native_original_git_blob":SOURCE_BLOB,
            "native_git_blob_verified":pinned,"actual_local_loaded_blob":blob,
            "all128_completeness_replayed":True,
            "oldRIGHT_dimension":128,"CAR16_eigen_mult":[8,8],
            "measured_blank_one":blank1,"measured_blank_two":blank2,
            "measured_blank_variance":blank2-blank1**2,
            "proper_boost_jet_blank_one":jet1,
            "proper_boost_jet_blank_two":jet2,
            "one_blank_not_sufficient_for_Book":True,
            "two_blank_entire_Hodge_and_J_source_reconstructed":True,
            "finite_n_cases":out,
            "selected_physical_Book03_scene_Hodge":False,
            "same_programme_full42_Euler_closed":False,
            "GR_closed":False}
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
