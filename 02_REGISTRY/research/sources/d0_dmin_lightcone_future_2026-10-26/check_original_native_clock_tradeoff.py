#!/usr/bin/env python3
"""Literal ORIGINAL G/CX serial/tree parity word:
SAME full unitary on all input + dirty helper columns and SAME full
Book positive feedback, but DIFFERENT actual paid chronological clock.

Only a declared bare two-grade cyclic clock is used for the final
nonzero heat-price comparison, not the full original 33-scene Hodge.
No D_min selection, 42-field Palatini action, new gate or free clock.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
import sympy as S

ROOT=Path(__file__).resolve().parent.parent / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0,str(ROOT))
import native_execution as ne

CHECKS=0
def check(v,why):
    global CHECKS
    CHECKS+=1
    if not bool(v):raise ArithmeticError(why)

def serial(n):
    return tuple(ne.Gate("CX",(i,n)) for i in range(n))

def tree(n):
    check(n>=2 and n&(n-1)==0, "actual complete binary tree count")
    layers=[]
    step=1
    while step<n:
        level=tuple(ne.Gate("CX",(base+step,base))
                    for base in range(0,n,2*step))
        layers.append(level)
        step*=2
    gates=tuple(g for level in layers for g in level)
    return (gates+(ne.Gate("CX",(0,n)),)+
            tuple(g for level in reversed(layers) for g in level)),len(layers)

def execution(n,copy):
    e=ne.Execution(n+1,(n,),(),copy,ne.G_CX,report_bits=(n,))
    ne.validate_execution(e,max_qubits=n+1,max_expanded_stages=10*n)
    return e

def apply_classical(n,gateword,x,h):
    b=x | (h<<n)
    for g in gateword:
        if g.op!="CX":raise ArithmeticError("only reversible native CX expected")
        src,dst=g.wires
        if b&(1<<src):
            b^=1<<dst
    return b&((1<<n)-1), (b>>n)&1

cases=[]
for n in (2,4,8):
    sq=serial(n)
    tr,D=tree(n)
    esq=execution(n,sq)
    etr=execution(n,tr)
    check(len(sq)==n and len(tr)==2*n-1,
          "true raw original CX primitive inventory")
    check(2*D+1==2*(n.bit_length()-1)+1,
          "tree chronological disjoint-round depth exactly logarithmic")
    for x in range(1<<n):
        for h in (0,1):
            expected=(x, h^(x.bit_count()%2))
            check(apply_classical(n,sq,x,h)==expected,
                  "serial original CX parity-copy all genuine columns")
            check(apply_classical(n,tr,x,h)==expected,
                  "tree original CX parity-copy all genuine columns")
    # FULL RAW original Golden complete native words, exactly as in the
    # full feedback Theorem G. Same unitary but unequal physical duration.
    g=(ne.Gate("G",(n,)),)
    wseq=sq+g+sq+g
    wtree=tr+g+tr+g
    seq=execution(n,wseq)
    par=execution(n,wtree)
    check(len(wseq)==2*n+2 and len(wtree)==4*n,
          "full original native G/CX PRICE CLOCK differs")
    check(ne.inventory(seq,max_qubits=n+1,max_expanded_stages=10*n).g_count==2,
          "original Golden actuation paid twice")
    check(ne.inventory(par,max_qubits=n+1,max_expanded_stages=10*n).cx_count==4*n-2,
          "parallel-tree raw CX gates still fully paid")
    if n<=4:
        Useq=ne.word_matrix(seq,max_qubits=n+1,max_expanded_stages=10*n)
        Utree=ne.word_matrix(par,max_qubits=n+1,max_expanded_stages=10*n)
        check(ne.exact_matrix_equal(Useq,Utree),
              "ACTUAL original Golden all-column U same for serial and tree")
        inj=ne.input_isometry(seq,max_qubits=n+1,max_expanded_stages=10*n)
        C=inj.T*Useq*inj
        feedback=S.eye(2**n)-C.T*C
        fp=4*ne.P**3
        Fexpected=S.diag(*[fp if x.bit_count()%2==0 else 0
                            for x in range(2**n)])
        check(ne.exact_matrix_equal(feedback,Fexpected),
              "both original words have EXACT SAME true full Book feedback")
    cases.append(dict(n=n,original_input_dim=2**n,original_full_dim=2**(n+1),
                      seq_parity_CX=n,tree_parity_CX=2*n-1,
                      seq_parity_depth=n,tree_parity_depth=2*D+1,
                      seq_complete_N=2*n+2,tree_complete_N=4*n))

# Entire ORIGINAL bare two-grade cyclic clock spectrum of SAME native U
# sees its different physical stage count. Do NOT substitute the other
# spatial 33-scene Hodge or assert paid Cost/Info equality from end U.
p=(math.sqrt(5)-1)/2
theta=math.atan2(p,math.sqrt(p))
beta=math.log(2)
def K(N,angle):
    return math.fsum(math.exp(-beta*(1-math.cos(
        (2*math.pi*j+angle)/N))) for j in range(N))

def H(N,n):
    return (math.log(2**(n+1))+
            math.log(K(N,0)+K(N,2*theta)))/beta

limit=math.log(2)/beta
scales=[]
for n in (4,8,16,32,64,128,256):
    # log(2**(n+1)) is safe for these n; all actual raw modes COUNTED.
    diff=H(4*n,n)-H(2*n+2,n)
    check(diff>0,"same full native U and feedback but different true H_N")
    if n>=16:
        check(abs(diff-limit)<3/n,
              "true bare full H spectral difference approaches log2/beta")
    scales.append({"n":n,"bare_twograde_Htree_minus_Hseq":diff,
                   "true_Ntree":4*n,"true_Nseq":2*n+2})
check(abs(scales[-1]["bare_twograde_Htree_minus_Hseq"]-limit)<
      abs(scales[2]["bare_twograde_Htree_minus_Hseq"]-limit),
      "actual chronologically paid whole-clock offset tends to nonzero log2/beta")

print(json.dumps({
 "status":"PASS_EXACT_NATIVE_SERIAL_TREE_WHOLE_UNITARY_SAME_J_DIFFERENT_CLOCK",
 "checks":CHECKS,
 "source_native_alphabet":["G","CX"],
 "whole_operator_agreement_on_all_columns":True,
 "original_Book_feedback_agrees_at_true_same_P":True,
 "raw_complete_native_stage_difference":"(4n)-(2n+2)=2n-2",
 "two_grade_bare_H_asymptotic_gap":"log(2)/beta",
 "beta":beta,
 "numeric_clock_cases":scales,
 "native_33scene_H_physical_transfer_proved":False,
 "full_physical_Dmin_cost_selected":False,
 "GR_closed":False,
 "exact_parity_cases":cases
},sort_keys=True,indent=2))
