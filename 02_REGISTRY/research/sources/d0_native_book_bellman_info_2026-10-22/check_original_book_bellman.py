#!/usr/bin/env python3
"""Native ORIGINAL full128 TWO-tick Book03 Born+local-gain Bellman Info.

Mathematical conditional theorem: (i) normalized scalar Book weights must
equal the same original Born P, (ii) mean per-vertex gain = CONDITIONAL
Shannon. Without these physical gates it is NOT a selected Book03 Info.
Loads unchanged all128 original CAR16 Julia/Walsh/Golden K, including dark
labels, oldRIGHT spectator, real proper boost first jets. No DATA reset
at second tick. Only original literal port 0/10 costs are included here;
fine factory/controller/clock/right preparation costs remain separate.

Run in real PR checkout:
 OPENBLAS_NUM_THREADS=1 python3 \
  02_REGISTRY/research/sources/d0_native_book_bellman_info_2026-10-22/check_original_book_bellman.py
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm, solve_sylvester

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
SOURCE_PIN="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P=(math.sqrt(5)-1)/2
EL=math.log(1/P)
COST=1+(np.arange(128)%2)
EYE=np.eye(16,dtype=complex)
CHECKS=0
def ok(c,s):
    global CHECKS
    CHECKS+=1
    if not bool(c):
        raise ArithmeticError(s)
def close(x,y,err,msg):
    ok(abs(x-y)<err,f"{msg}: {x} vs {y}, tol={err}")

def native_original():
    raw=SOURCE.read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    ok(sha==SOURCE_PIN,"original immutable 128 Kraus Git blob")
    astree=ast.parse(raw)
    want={"adj","herm","root","creators","native"}
    nodes=[v for v in astree.body
           if isinstance(v,ast.FunctionDef) and v.name in want]
    ok(set(v.name for v in nodes)==want,
       "all five original native CAR16 fine constructors")
    env={"np":np,"EYE":EYE,"P":P,"expm":expm,
         "solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SOURCE),"exec"),env)
    return env["native"],sha

def actual_prob_and_jet(native,r=1/9,nu=.6):
    K,DKtheta=native(2*math.atanh(r),nu)
    DK=DKtheta*2/(1-r*r)
    ok(K.shape==(128,16,16) and DK.shape==K.shape,
       "128 original full CAR16 Kraus and proper-Lorentz field jets")
    cp=np.sum(K.conj().transpose(0,2,1)@K,axis=0)
    close(np.linalg.norm(cp-EYE),0,3e-12,
          "complete original fine instrument, all failed/dark labels")
    # The actual second native step ACTS ON previous DATA, no iid reset.
    W=np.einsum("bik,akj->abij",K,K,optimize=True)
    DW=(np.einsum("bik,akj->abij",DK,K,optimize=True)
       +np.einsum("bik,akj->abij",K,DK,optimize=True))
    joint=(np.abs(W)**2).sum((2,3))/16
    dJoint=(2*np.real(np.sum(np.conj(W)*DW,axis=(2,3))))/16
    row=joint.sum(axis=1)
    dRow=dJoint.sum(axis=1)
    close(joint.sum(),1,1e-12,"original all128 squared fine history normalized")
    close(dJoint.sum(),0,2e-10,"every original moving CAR Kraus source normalized")
    ok(int((joint>1e-19).sum())==4096,
       "all 4096 positive original 2tick full fine leaves, dark 12288 retained")
    return row,dRow,joint,dJoint

def price_gain(row,drow,joint,djoint):
    LIVE=row>1e-19
    ok(int(LIVE.sum())==64,
       "original one-tick physically 64 live/64 permanently dark outputs")
    rEntropy=-np.dot(row[LIVE],np.log(row[LIVE]))/EL
    rEntropyJet=-np.dot(drow[LIVE],np.log(row[LIVE]))/EL
    expectedCost=np.dot(row,COST)
    expectedCostJet=np.dot(drow,COST)
    child=np.zeros(128)
    dchild=np.zeros(128)
    infolast=np.zeros_like(joint)
    dInfolast=np.zeros_like(joint)
    for a in np.where(LIVE)[0]:
        cond=joint[a]/row[a]
        dcond=(djoint[a]*row[a]-joint[a]*drow[a])/(row[a]**2)
        nz=cond>1e-19
        # Bellman leaves are EXACT 0. Every child index has native actual cost.
        hc=-np.dot(cond[nz],np.log(cond[nz]))/EL
        dhc=-np.dot(dcond[nz],np.log(cond[nz]))/EL
        cc=np.dot(cond,COST)
        dcc=np.dot(dcond,COST)
        child[a]=2*hc-cc
        dchild[a]=2*dhc-dcc
        infolast[a,nz]=COST[nz]+np.log(cond[nz])/EL+child[a]
        dInfolast[a,nz]=dcond[nz]/cond[nz]/EL+dchild[a]
        close(np.dot(cond,infolast[a]),hc,2e-11,
              "every positive original native source prefix gains entropy")
    froot=2*rEntropy-expectedCost+np.dot(row,child)
    dfroot=2*rEntropyJet-expectedCostJet+np.dot(drow,child)+np.dot(row,dchild)
    Iroot=np.zeros(128)
    DIroot=np.zeros(128)
    Iroot[LIVE]=COST[LIVE]+np.log(row[LIVE])/EL+froot-child[LIVE]
    DIroot[LIVE]=drow[LIVE]/row[LIVE]/EL+dfroot-dchild[LIVE]
    close(np.dot(row,Iroot),rEntropy,2e-12,
          "ORIGINAL first native vertex expected Info equals Shannon entropy")
    positive=joint>1e-19
    hJoint=-np.dot(joint[positive],np.log(joint[positive]))/EL
    dhJoint=-np.dot(djoint[positive],np.log(joint[positive]))/EL
    ecJoint=float((joint*COST[:,None]).sum()+(joint*COST[None,:]).sum())
    decJoint=float((djoint*COST[:,None]).sum()+(djoint*COST[None,:]).sum())
    close(froot,2*hJoint-ecJoint,2e-12,
          "ENTIRE noreset tree Bellman root equals unique full-history normalizer")
    close(dfroot,2*dhJoint-decJoint,2e-10,
          "ENTIRE noreset tree REAL SOURCE equals derivative of complete history")
    score=COST[:,None]+COST[None,:]-Iroot[:,None]-infolast
    dScore=-DIroot[:,None]-dInfolast
    Wbook=np.zeros_like(joint)
    DWbook=np.zeros_like(joint)
    Wbook[positive]=np.exp(-EL*score[positive])
    DWbook[positive]=-EL*Wbook[positive]*dScore[positive]
    Zbook=Wbook.sum()
    DZbook=DWbook.sum()
    close(Zbook,math.exp(EL*froot),1e-12,
          "raw ORIGINAL Book03 partition equals phi^Bellman(root)")
    close(DZbook,EL*Zbook*dfroot,3e-11,
          "all original history Book probability source normalizer correct")
    posterior=Wbook/Zbook
    dposterior=(DWbook*Zbook-Wbook*DZbook)/Zbook**2
    ok(np.max(np.abs(posterior-joint))<1e-14,
       "ALL 128 squared original complete Born weights reconstructed")
    ok(np.max(np.abs(dposterior-djoint))<1e-11,
       "ALL original 16384 fine Born first sources reconstructed")
    expectedI=np.dot(row,Iroot)+float((joint*infolast).sum())
    expectedS=float((joint*score).sum())
    close(expectedI,hJoint,1e-12,"global expected Book gain = true full Shannon")
    close(expectedS,ecJoint-hJoint,1e-12,
          "expected literal Book net charge = ORIGINAL port Cost−Shannon")
    return dict(H_root=rEntropy,H_full=hJoint,port_cost_two_ticks=ecJoint,
                froot=froot,Dfroot=dfroot,
                raw_book_partition=Zbook,book_partition_source=DZbook,
                global_expected_Information=expectedI,
                global_expected_action=expectedS,
                source_corrected_action=decJoint-dhJoint,
                book_probability_error=float(np.max(np.abs(posterior-joint))),
                book_probability_source_error=float(np.max(np.abs(dposterior-djoint))),
                minimum_realized_Gain=float(min(Iroot[LIVE].min(),infolast[positive].min())))

def native_original_pair():
    # Exact original scalar p+p^2=1 gives TRUE nonblank Golden twin.
    q=np.array([P*P,P])
    originalReference=np.array([P,P*P])
    c=np.array([1,2])
    H=-np.dot(q,np.log(q))/EL
    EC=np.dot(q,c)
    f=2*H-EC
    gains=c+np.log(q)/EL+f
    raw=np.exp(-EL*(c-gains))
    resulting=raw/raw.sum()
    close(f,3*P*P,1e-13,
          "unique original reversed-Golden Book normalizer 3p²")
    close(gains[0],3*P*P-1,1e-13,"original true cheap-port gain")
    close(gains[1],3*P*P+1,1e-13,"original true expensive-port gain")
    close(np.dot(q,gains),H,1e-13,"original onepair expected gain=H")
    ok(max(abs(resulting-q))<1e-14,
       "native whole Book weights return ORIGINAL reversed port probabilities")
    # WRONG surprisal I=-logφP leads W=φ^-c / P and different normalized born
    wrong=originalReference/q
    wrong/=wrong.sum()
    ok(np.max(abs(wrong-q))>0.3,
       "naive surprisal path Info cannot reproduce native Book Born outcomes")
    qrare=1e-6
    binary=np.array([1-qrare,qrare])
    hb=-np.dot(binary,np.log(binary))/EL
    fr=2*hb-(1+qrare)
    rareInfo=2+math.log(qrare)/EL+fr
    ok(rareInfo< -20,
       "true original rare N1-type reporter forces NEGATIVE realized Bellman gain")
    return dict(P=P,nativeTruePortProbabilities=q.tolist(),
                originalFRCosts=c.tolist(),goldenOnePairH=H,
                nativeOnePairBookJ=f,originalBookVertexGains=gains.tolist(),
                wrongSurprisalBookProbabilities=wrong.tolist(),
                nativeRareClickTest:qrare if False else qrare,
                nativeRareClickBellmanGain:rareInfo)

def main():
    native,sha=native_original()
    row,drow,joint,djoint=actual_prob_and_jet(native)
    result=price_gain(row,drow,joint,djoint)
    pair=native_original_pair()
    print(json.dumps({
        "status":"PASS_ORIGINAL_FULL128_TWO_TICK_BOOK_BELLMAN_BORN_INFO",
        "checks":CHECKS,
        "original_native_Kraus_Git_blob":sha,
        "original_Born_Book_unique_Bellman_2tick":result,
        "original_reversed_Golden_0slash10_pair_and_rare_sign":pair,
        "Book03_required_scalar_Born_equality_physically_proved":False,
        "Book03_required_mean_vertex_Shannon_gain_physically_proved":False,
        "Book03_signed_realized_vertex_Info_allowed":False,
        "full_Book03_compulsory_scene_Hodge_selected":False,
        "physical_same_execution_full42_Euler_closed":False,
        "GR_closed":False},indent=2))

if __name__=="__main__":
    main()
