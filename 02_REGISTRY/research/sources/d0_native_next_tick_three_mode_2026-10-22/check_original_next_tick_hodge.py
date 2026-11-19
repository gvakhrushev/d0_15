#!/usr/bin/env python3
"""ORIGINAL 128-Kraus second-tick registered-memory Book/Hodge + source.

No synthetic new instrument: AST-selects unchanged original constructor
at pinned Git blob ee8de4635d24c668949ac9a0186616ab7d59f2ed;
all old 128 labels, oldRIGHT128 and 128 fresh second-work slots retained.
Exact generic CAR-mask proof is in sibling check_generic_original_support.py;
rational strict source-sign bounds are independent of float secants.
This physical cut and the cut-INCIDENCE Hodge are candidates, not
compulsory Book03 scene Delta and Info. GR_closed=False.

Run in repo root:
 OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_native_next_tick_three_mode_2026-10-22/check_original_next_tick_hodge.py
"""
from __future__ import annotations
import ast
from collections import Counter
from fractions import Fraction as Fr
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm,solve_sylvester

SOURCE_SHA="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
SOURCE="02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
P=(math.sqrt(5)-1)/2
BETA=2*P**2
ZETA=2**-20
EYE=np.eye(16,dtype=complex)
RIGHT=128
OLD_WORK=128
NEW_WORK=128
D=16*RIGHT*OLD_WORK*NEW_WORK
ACTIVE=118272
KCHECK=0
def ok(cond,msg):
    global KCHECK
    KCHECK+=1
    if not bool(cond):raise ArithmeticError(msg)
def close(a,b,tol,msg):
    ok(abs(a-b)<=tol,msg+": "+str(a)+" vs "+str(b))

def original_native():
    p=Path(__file__).resolve().parents[4]/SOURCE
    raw=p.read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    ok(sha==SOURCE_SHA,"EXACT original all128 Kraus constructor Git blob")
    tree=ast.parse(raw)
    needed={"adj","herm","root","creators","native"}
    functions=[node for node in tree.body
               if isinstance(node,ast.FunctionDef) and node.name in needed]
    ok(set(n.name for n in functions)==needed,"all five native CAR16 constructors")
    env={"np":np,"P":P,"EYE":EYE,"expm":expm,"solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=functions,type_ignores=[]),str(p),"exec"),env)
    return env["native"],sha

def mask_for(j):
    # Exact generic Walsh-support identities and algebraic rank at r=1/9
    # proved separately; no mask is fitted from numerical spectral values.
    if j%4 in (2,3):return ()
    if j in (1,5,17,21,25,33,37,41,49,53,57):
        return tuple(k for k in range(16) if k not in (0,4,8,12))
    if j==13:return tuple(k for k in range(16) if k!=12)
    if j==45:return tuple(k for k in range(16) if k!=0)
    if j in (29,61):return tuple(k for k in range(16) if k not in (0,12))
    return tuple(range(16))

def delta_corner(r):
    return 9*(5*r**4+2*r**3-6*r*r-2*r+5)/(3200*(1-r*r)**2)
def d_delta_corner(r):
    return 9*(1+r*r)*(r*r+4*r-1)/(1600*(1-r*r)**3)

def direct_spectral(B,DB,ks,dks):
    # Every genuine registered support projector first stage is a coordinate
    # mask on the original regular field chart, now the PRE-SECOND-tick cut.
    g=0.; dg=0.; sl=0.; dsl=0.; count=Counter()
    for j in range(64):
        labels=mask_for(j)
        rank=len(labels)
        count[rank]+=1
        k0,k1=ks[2*j],ks[2*j+1]
        Pj=np.diag([1. if a in labels else 0. for a in range(16)]).astype(complex)
        if rank:
            # exact support masks are OPERATOR PROPERTIES; this is a check
            # against UNALTERED actual 128 Kraus K_j, not SVD fitting.
            close(float(np.linalg.norm((EYE-Pj)@k0)),0.,3e-10,
                  "original native even Kraus entire output in true mask")
            close(float(np.linalg.norm((EYE-Pj)@k1)),0.,3e-10,
                  "original native odd port Kraus same true DATA range")
            # Genuine moving source of support vanishes on this ORIGINAL
            # analytic regular chart by generic symbolic 800-entry proof.
            close(float(np.linalg.norm((EYE-Pj)@dks[2*j])),0.,3e-9,
                  "proper Lorentz first derivative remains in true mask")
            close(float(np.linalg.norm((EYE-Pj)@dks[2*j+1])),0.,3e-9,
                  "port first derivative shares the same support")
            # Full rank IN declared mask, no hidden dropped eigenchannel.
            sing=np.linalg.svd(Pj@k0,compute_uv=False)
            actual=int(sum(sing>max(1e-12,sing[0]*1e-11)))
            ok(actual==rank,"EXACT original algebraic mask's current numerical rank")
            M=B[np.ix_(labels,labels)]
            dM=DB[np.ix_(labels,labels)]
            eig,U=np.linalg.eigh(M)
            ok(eig.min()>0 and eig.max()<1,"original K0 compression has strict eigen gap")
            f=1-eig**2
            ff=1-ZETA*f
            ok(np.all(ff>0),"full actual Book positive determinant pencil")
            g+=np.log(ff).sum()
            dMtilde=U.conj().T@dM@U
            deig=np.diag(dMtilde).real
            df=-2*eig*deig
            dg+=float(np.sum(ZETA*df/ff))
            sl+=float(np.sum(np.exp(-BETA*f)-1))
            dsl+=float(np.sum(np.exp(-BETA*f)*df))
        else:
            close(float(np.linalg.norm(k0)+np.linalg.norm(k1)),0,3e-12,
                  "original dark native duplicated Walsh row exactly empty")
    ok(count==Counter({16:17,12:11,15:2,14:2,0:32}),
       "original rank histogram of 64 2-port Walsh row events")
    R=2*RIGHT*sum(j*ct for j,ct in count.items())
    ok(R==ACTIVE,"same original 118272 true one-tick pointer support")
    FJ=-2*RIGHT*g
    DJ=2*RIGHT*dg
    Z=D+4*RIGHT*sl
    # Z = D - 2 R + 2 * 256 * sum_active(e^-beta f) EXACTLY.
    H=math.log(Z)/BETA
    DH=-4*RIGHT*dsl/Z
    return dict(J=FJ,DJ=DJ,H=H,DH=DH,source=DJ+DH,
                Z=Z,R=R,zero_modes=D-2*R,
                rank_row_histogram=dict(count))

def three_mode(r):
    mu=9*(5*r**4+r**3-8*r*r-r+5)/(3200*(1-r*r)**2)
    poly=81*(23*r**4+6*r**3-32*r*r-10*r+25)/(10240000*(1-r*r)**2)
    eps=math.sqrt(mu**2-poly)
    # Original true eigenvalue source formula: take exact rational
    # derivative via symmetric differences only in optional diagnostics;
    # real analytical first jet uses native fixed r=1/9 below.
    if r==1/9:
        mp=-328779/204800000
        hp=-20040939/9885993640
        h=poly/mu
        ep=((2*mu-h)*mp-mu*hp)/(2*eps)
        lams=[mu-eps,mu+eps]
        dlams=[mp-ep,mp+ep]
    else:
        # Generic local AD of true rational expressions by complex-step:
        # intrinsic analytical derivatives, not an independent source fit.
        step=1e-25
        def eigen_pair(z):
            zm=9*(5*z**4+z**3-8*z*z-z+5)/(3200*(1-z*z)**2)
            det=81*(23*z**4+6*z**3-32*z*z-10*z+25)/(10240000*(1-z*z)**2)
            ee=np.sqrt(zm*zm-det)
            return (zm-ee,zm+ee)
        lams=list(eigen_pair(r))
        dlams=[x.imag/step for x in eigen_pair(r+1j*step)]
    b=[1-BETA*l for l in lams]+[1-BETA*delta_corner(r)]
    db=[-BETA*d for d in dlams]+[-BETA*d_delta_corner(r)]
    ff=[1-v*v for v in b]
    dff=[-2*v*dv for v,dv in zip(b,db)]
    weights=[206,206,50]
    J=-2*RIGHT*sum(w*math.log1p(-ZETA*f) for w,f in zip(weights,ff))
    DJ=2*RIGHT*ZETA*sum(w*df/(1-ZETA*f)
                         for w,df,f in zip(weights,dff,ff))
    Z=D-2*ACTIVE+4*RIGHT*sum(
          w*math.exp(-BETA*f) for w,f in zip(weights,ff))
    H=math.log(Z)/BETA
    DH=-4*RIGHT*sum(w*math.exp(-BETA*f)*df
                    for w,df,f in zip(weights,dff,ff))/Z
    return dict(J=J,DJ=DJ,H=H,DH=DH,source=DJ+DH,Z=Z,
                f=ff,df=dff,b=b,db=db,delta_c=delta_corner(r),
                d_delta_c=d_delta_corner(r))

def main():
    native,sha=original_native()
    r=1/9
    k,dk_theta=native(2*math.atanh(r),.6)
    dk=dk_theta*(2/(1-r*r))
    ok(k.shape==(128,16,16) and dk.shape==k.shape,
       "original full128 CAR16 K and full proper Lorentz derivatives")
    complete=np.sum(k.conj().transpose(0,2,1)@k,axis=0)
    close(float(np.linalg.norm(complete-EYE)),0.,5e-12,
          "true original ALL128 Kraus instrument complete; not success-only")
    B=k[0]
    DB=dk[0]
    close(float(np.linalg.norm(B-B.conj().T)),0.,3e-12,
          "original actual K0 Hermitian positive CAR source")
    out=direct_spectral(B,DB,k,dk)
    model=three_mode(r)
    for key,tol in [("J",8e-10),("DJ",1e-9),("H",1e-10),
                    ("DH",1e-9),("source",1e-9),("Z",1e-6)]:
        close(out[key],model[key],tol,
              "direct original full128 next-tick vs 3-mode complete "+key)
    close(model["delta_c"],69489/5120000,1e-14,
          "original exact CAR delta33 rational")
    close(model["d_delta_c"],-328779/102400000,1e-14,
          "original exact proper Lorentz delta33 derivative")
    close(model["b"][2],float(B[3,3].real),1e-13,
          "original actual 16x16 native CAR diagonal third spectral mode")
    close(model["db"][2],float(DB[3,3].real),1e-12,
          "original actual native moving b33 source")
    ok(D==33554432 and out["zero_modes"]==33317888,
       "correct ALL 2tick oldRIGHT/oldwork/newwork harmonic ZERO modes")
    # Rigorous rational conservative interval bound on entire 3-mode
    # source using original independently proven lambda' inequalities.
    z=Fr(1,2**20)
    zlo=z-Fr(2,D-2*ACTIVE)
    zhi=z/(1-z)
    ok(zlo>Fr(89,10**8) and zhi<Fr(954,10**9),
       "strict rational original complete native K(f) envelope")
    upper=256*206*(-Fr(98,10**4)*zlo+Fr(624,10**5)*zhi)
    ok(upper<-Fr(1,10**4),
       "strict rational derivative bound, scalar third mode negative too")
    ok(model["df"][0]<-.0098 and 0<model["df"][1]<.00624
       and model["df"][2]<0,
       "original full CAR16 eigen source sign rational bracket applied")
    ok(out["source"]<0,
       "TRUE full next native registered book+Hodge Lorentz first source")
    # Three source-sufficient original Born moments, distinct paid inputs.
    q1=float(np.trace(B@B).real)/16
    q2=float(np.trace(B@B@B@B).real)/16
    basis3=float(np.real((B@B)[3,3]))
    dBprod=math.sqrt(2*q1*q1-q2)
    sB=math.sqrt(2*(q1+dBprod))
    recovered=(basis3+dBprod)/sB
    close(recovered,model["b"][2],5e-13,
          "two true mixed blank events plus basis CAR |3> blank Born")
    print(json.dumps({
        "status":"PASS_ORIGINAL_FULL128_SECOND_NATIVE_TICK_THREE_MODE",
        "checks":KCHECK,"original_native_Git_blob":sha,
        "native_r":"1/9","nu":"3/5",
        "full_2tick_Hilbert_dimension":D,
        "positive_Book_rank":ACTIVE,
        "all_harmonic_zero_modes":D-2*ACTIVE,
        "three_eigen_multiplicities":[52736,52736,12800],
        "original_two_Born_moments":[q1,q2],
        "additional_basis_3_Born_blank":basis3,
        "book_feedback":out["J"],
        "book_source":out["DJ"],
        "paired_cut_incidence_Hodge":out["H"],
        "paired_Hodge_source":out["DH"],
        "complete_H_plus_J_source":out["source"],
        "analytical_source_strict_upper":"-0.0001",
        "source_chart":"original proper boost r=1/9 on fixed positive nonzero rank masks",
        "true_full128_fine_work_retained":True,
        "oldRIGHT128_retained":True,
        "first_stage_unobserved_U_completion_needed":False,
        "next_Stinespring_unobserved_U_completion_needed":False,
        "compulsory_Book03_P_N_and_scene_Delta_selected":False,
        "same_programme_42_native_Euler_verified":False,
        "GR_closed":False},indent=2))

if __name__=="__main__":
    main()
