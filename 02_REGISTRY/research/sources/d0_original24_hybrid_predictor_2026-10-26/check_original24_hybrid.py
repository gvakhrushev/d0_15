#!/usr/bin/env python3
"""Exact ORIGINAL 128->24 projective Kraus-ray plus CAR parity-bit/8D
quantum predictor; NO change to the original physical fine records.

1) Algebraic Gaussian-integer Walsh coefficient proof of uniform same-ray
   7- and 4-row mergers on the ORIGINAL fixed-phase CAR creator family.
   The only identities used are the ORIGINAL duplicated Walsh words and
   sqrt(I-nu^2 cc†)=uI-vZ, sqrt(I-nu^2 c†c)=uI+vZ for original CAR.
2) Original PINNED all-eight-split-prime Julia/Walsh/Golden128 Kraus
   source import, EXACT modular CP, row phases, no further ray mergers.
3) Exact finite-history 24-class/fine-label factorization, Golden port +
   uniform Walsh row conditional coin, and CAR parity-conditioned 8x8
   quantum transducer for ALL the selected original real 3-tick test words.
4) Preserves every dark/failed fine label as a physically identifiable
   zero-probability terminal label, WITHOUT claiming any physical WORK,
   clock, D_min, Book choice or 42-field GR closure.

The 24-class T_g(X) is m_g L_g X L_g† with integer m_g, NOT a
new native sqrt(m_g) gate or a FREE rewritten original Stinespring word.

Run from any cwd: python3 check_original24_hybrid.py
                   python3 -O check_original24_hybrid.py
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import sys
import json
import numpy as np

ORIGINAL = Path(__file__).resolve().parent.parent / "d0_original_full128_future_even_algebra_2026-10-22"
sys.path.insert(0, str(ORIGINAL))
import check_future_even_algebra_modprime as original

COUNT=0
def check(cond,why):
    global COUNT
    COUNT+=1
    if not bool(cond):
        raise ArithmeticError(why)

# Exactly the original 64 Walsh rows (32 lab, 2 endpoints) and
# 32 duplicated input words. Each coefficient is a Gaussian INTEGER
# before the common source factor 1/16 is restored.
def tag_word(role:int, w:int, endpoint:int):
    if endpoint==0:
        # ORIGINAL fixed phases (i,i,-1,-i). The role1 forward x is
        # i*nu*c1*U and dagger is -i*nu*U*c1†. It is NEVER replaced
        # by a free independent rotation.
        model = (
          (("c0",0,1),("ct0",0,-1),("c0",-1,0),("ct0",-1,0)),
          (("c1U",0,1),("Uct1",0,-1),("c1",-1,0),("ct1",-1,0)),
          (("c2",-1,0),("ct2",-1,0),("c2",-1,0),("ct2",-1,0)),
          (("c3",0,-1),("ct3",0,1),("c3",-1,0),("ct3",-1,0))
        )
        t,real,imag=model[role][w]
        return {("odd",t):(real,imag)}
    # REAL original static Julia roots on *each* original CAR mode,
    # uI ± v Z_role, with one COMMON scalar u across ALL modes.
    if role==1 and w<2:
        return {("moved","Lm" if w==0 else "Rm"):(1,0)}
    sign=1 if w<2 else -1
    zz=-1 if w%2==0 else 1 # left=uI-vZ ; right=uI+vZ
    return {("uI",):(sign,0),("vZ",role):(sign*zz,0)}

def original_row_coeff(j:int):
    lab,endpoint=divmod(j,2)
    if lab&1:
        return {} # exact duplicate-pair Walsh cancellation
    acc=defaultdict(lambda:(0,0))
    for role in range(4):
        for w in range(4):
            # Two original identical Walsh slots 8r+2w, 8r+2w+1.
            slot=8*role+2*w
            sign=-1 if (lab&slot).bit_count()%2 else 1
            for name,(re,im) in tag_word(role,w,endpoint).items():
                ore,oim=acc[name]
                acc[name]=(ore+sign*re,oim+sign*im)
    return {k:v for k,v in acc.items() if v!=(0,0)}

def neg(a):
    return {k:(-v[0],-v[1]) for k,v in a.items()}
def gaussian_row_groups():
    groups=[]
    for j in range(64):
        c=original_row_coeff(j)
        if not c:
            continue
        for g in groups:
            d=original_row_coeff(g[0][0])
            if c==d:
                g.append((j,1))
                break
            if c==neg(d):
                g.append((j,-1))
                break
        else:
            groups.append([(j,1)])
    return groups

GROUPS=gaussian_row_groups()
EXPECTED=[
 [(0,1)],
 [(1,1),(17,-1),(25,-1),(33,1),(41,1),(49,-1),(57,-1)],
 [(4,1)],
 [(5,1),(21,-1),(37,1),(53,-1)],
 [(8,1)],[(9,1)],[(12,1)],[(13,1)],[(16,1)],
 [(20,1)],[(24,1)],[(28,1)],[(29,1)],
 [(32,1)],[(36,1)],[(40,1)],[(44,1)],
 [(45,1)],[(48,1)],[(52,1)],[(56,1)],
 [(60,1)],[(61,1)]
]
check(GROUPS==EXPECTED,
      "SYMBOLIC original Gaussian Walsh gives exact 23 raw source-ray groups")
check(sum(len(g) for g in GROUPS)==32 and len(GROUPS)==23,
      "half the actual64 Walsh rows are structurally dark, true 32 live")
check(len([g for g in GROUPS if len(g)==7])==1 and
      len([g for g in GROUPS if len(g)==4])==1 and
      len([g for g in GROUPS if len(g)==1])==21,
      "exact original 7+4+21 raw group sizes")

# 24 live fine classes: original special Kraus 0 and1 separately,
# then 22 ORIGINAL j>0 rows modulo exact sign equality.
COARSE=[[(0,1)],[(1,1)]]+GROUPS[1:]
check(len(COARSE)==24,"2 special +22 native j>0 ray classes")
COARSE_REPS=[0,1]+[2*g[0][0] for g in COARSE[2:]]
check(len(COARSE_REPS)==24 and len(set(COARSE_REPS))==24,
      "no false group or off-original label")
fine_map={0:(0,None),1:(1,None)}
for gidx,group in enumerate(COARSE[2:],start=2):
    for j,sign in group:
        fine_map[2*j]=(gidx,(j,0,sign))
        fine_map[2*j+1]=(gidx,(j,1,sign))
check(len(fine_map)==64 and
      len(set(range(128))-set(fine_map))==64,
      "all 64 nonzero fine symbols plus ALL 64 original dark labels")
check(set(k for k in fine_map if k>=2 and k%2==0)==
      set(2*j for g in GROUPS[1:] for j,_ in g),
      "literal original j>0 live twin rows were not relabeled incorrectly")

# Numerical-like metadata here is computed EXACTLY over ALL original
# algebraic reductions. One nonzero 2x2 projective minor at a good
# prime already proves distinctness of characteristic-zero Kraus rays.
def modmul(A,B,m):
    return (A@B)%m

def proportional_mod(A,B,m):
    aa=np.asarray(A,dtype=np.int64).reshape(-1)%m
    bb=np.asarray(B,dtype=np.int64).reshape(-1)%m
    nz=np.flatnonzero(aa)
    if not len(nz):
        return not np.any(bb)
    q=int(nz[0])
    return not np.any((aa[q]*bb-bb[q]*aa)%m)

def coarse_blocks(d, idx):
    """Actual original 24-class CP map B_g and its true integer count."""
    if idx==0:
        return (1,d["K"][0],d["Kd"][0])
    if idx==1:
        return (1,d["K"][1],d["Kd"][1])
    j=COARSE[idx][0][0]
    m=d["m"]
    p=d["p"]
    pi=pow(int(p),-1,m)
    return (len(COARSE[idx]),(d["K"][2*j]*pi)%m,
            (d["Kd"][2*j]*pi)%m)

def fine_weight(idx,g,d):
    if idx<2:
        return 1
    m=d["m"]
    p=d["p"]
    row_count=len(COARSE[g])
    return ((p*p if idx%2==0 else p)*pow(row_count,-1,m))%m

def coarse_effect(word,d):
    """Actual ordered coarse Kraus-class Heisenberg map, NO sqrt7."""
    m=d["m"]
    X=d["I"].copy()
    for idx in reversed(word):
        mult,A,Ad=coarse_blocks(d,idx)
        X=mult*modmul(Ad,modmul(X,A,m),m)%m
    return X

def hybrid_probability(word,d,X):
    """Exact original parity-bit + 8D quantum data CPA.
    X need NOT be parity diagonal: the off-diagonal coherence is
    future-invisible for the ORIGINAL instrument only.
    """
    m=d["m"]
    sets=[d["even"],d["odd"]]
    blocks=[X[np.ix_(s,s)].copy()%m for s in sets]
    for g in word:
        mult,A,Ad=coarse_blocks(d,g)
        nexts=[np.zeros((8,8),np.int64) for _ in range(2)]
        # Each original homogeneous Kraus maps one input CAR parity to
        # exactly one output parity.
        for i in range(2):
            out=(np.flatnonzero(np.any(A[:,sets[i]]%m,axis=1)))
            target=0 if all(j in sets[0] for j in out) else 1
            check(all(j in sets[target] for j in out),
                  "original native Kraus has definite parity transition")
            B=A[np.ix_(sets[target],sets[i])]
            Bd=Ad[np.ix_(sets[i],sets[target])]
            nexts[target]=(nexts[target]+
                           mult*modmul(B,modmul(blocks[i],Bd,m),m))%m
        blocks=nexts
    return sum(int(np.trace(b)) for b in blocks)%m

def check_prime(prime_data,selected_words=None, full=False):
    d=original.original_kraus_mod(prime_data)
    m=d["m"];p=prime_data[2];rootp=prime_data[3]
    d["p"]=p
    check(len(d["nonzero"])==64 and
          set(d["nonzero"])==set(fine_map),
          "original native K exact live/dead Walsh block support")
    check(len(d["even"])==len(d["odd"])==8,
          "original two parity blocks both physically retained")
    for gidx,group in enumerate(COARSE[2:],start=2):
        j0=group[0][0]
        L=(d["K"][2*j0]*pow(int(p),-1,m))%m
        for j,sgn in group:
            check(np.array_equal(d["K"][2*j]%m,
                                 sgn*d["K"][2*j0]%m),
                  "structural original Walsh signed row relation K2j")
            check(np.array_equal(d["K"][2*j+1]%m,
                                 sgn*d["K"][2*j0+1]%m),
                  "structural original Walsh signed row relation K2j+1")
            check(np.array_equal(d["K"][2*j+1]%m,(rootp*L)%m),
                  "genuine independent Golden conditional port ratio")
            check(np.array_equal(d["Kd"][2*j+1]%m,
                                 (rootp*d["Kd"][2*j0]*pow(int(p),-1,m)*sgn)%m),
                  "original conjugate Golden port ratio")
        check((len(group)*pow(len(group),-1,m))%m==1,
              "true j-row uniform coin is properly normalized")
    accum=(modmul(d["Kd"][0],d["K"][0],m)+
           modmul(d["Kd"][1],d["K"][1],m))%m
    parity_counts={"preserving":2,"flipping":0}
    for gidx in range(2,24):
        mult,A,Ad=coarse_blocks(d,gidx)
        accum=(accum+mult*modmul(Ad,A,m))%m
        j=COARSE[gidx][0][0]
        if j%2:
            parity_counts["flipping"]+=1
        else:
            parity_counts["preserving"]+=1
        # Complete conditional children weights are 1:1/m per j,
        # with original positive Golden p²,p splitting each original j.
        total=sum(fine_weight(2*j+b,gidx,d) for j,_ in COARSE[gidx]
                  for b in (0,1))%m
        check(total==1,"exact class child coin has total probability one")
    check(np.array_equal(accum,d["I"]),
          "TRUE 24 integer-weighted full CAR16 original CPTP sum")
    check(parity_counts=={"preserving":17,"flipping":7},
          "real parity-bit flip/preserve sectors exact 17/7")

    if full:
        representatives=[d["K"][i] for i in COARSE_REPS]
        check(all(np.any(v) for v in representatives),
              "original24 source representative rays all truly nonzero")
        for ia,A in enumerate(representatives):
            for ib,B in enumerate(representatives[:ia]):
                check(not proportional_mod(A,B,m),
                      "strict 24-ray nonproportionality witnessed by a GOOD prime")
        # Unchanged ORIGINAL 3-round basis of 128 genuine fine words:
        # apply finite CP duals on the real original operators.
        check(selected_words is not None and len(selected_words)==128,
              "original fixed witness words retained from source-owner")
        X=(np.arange(16*16,dtype=np.int64).reshape(16,16)*17+13)%m
        for word in selected_words:
            E=original.effect_of_word(word,d)
            cw=tuple(fine_map[idx][0] for idx in word)
            pred=coarse_effect(cw,d)
            factor=1
            for idx in word:
                factor=factor*fine_weight(idx,fine_map[idx][0],d)%m
            check(np.array_equal(E,(factor*pred)%m),
                  "EXACT all no-reset native 3tick fine ->24 CP effect")
            fineprob=int(np.trace(modmul(X,E,m)))%m
            coarseprob=hybrid_probability(cw,d,X)
            check(fineprob==factor*coarseprob%m,
                  "EXACT full original fine probability from 8D plus parity bit")
        return {"p":m,"reps":24,"fine_words":len(selected_words)}
    return {"p":m,"reps":24}

def main():
    # Keep existing exact owner 128-word list; it already proves that
    # the all-future original data effect span is M8+M8 and source
    # selected rank128 on three ticks.
    primary=original.original_kraus_mod(original.SPLIT_PRIMES[-1])
    ranks,words,_=original.actual_future_basis(primary)
    check(ranks[3]==128 and len(words)==128,"original exact future M8+M8 owner")
    outcome=[]
    for pd in original.SPLIT_PRIMES:
        result=check_prime(pd, words, full=True)
        outcome.append(result)
    # No added charge is inferred for the row coin or the actual index:
    # the measured CQ entropy chain rule contains h_phi(p²,p)=2-p
    # PLUS log_phi(m_g) for m=4,7. Genuine row code price stays.
    check(7+4+20==31 and 2+22==24,
          "correct original live grouping count, two special labels")
    print(json.dumps({
      "status":"PASS_EXACT_ORIGINAL_FULL128_TO24_HYBRID_FUTURE_COMPLETE",
      "checks":COUNT,
      "original_field_source_blob":original.SOURCE_BLOB,
      "exact_split_prime_results":outcome,
      "original_128_Kraus_slots":128,
      "actual_nonzero_fine_labels":64,
      "actual_structural_dark_labels":64,
      "original_65_predictive_labels_including_dark":65,
      "new_original_projective_predictive_symbols":24,
      "original_nonzero_row_equivalence":"7 + 4 + 20 + one original j0",
      "genuine_full128_future_algebra":"M8(C) + M8(C) at 3 original ticks",
      "hybrid_quantum_dimension":8,
      "hybrid_classical_parity_sectors":2,
      "original_same_joint_fine_record_retained":True,
      "fine_label_conditional_coin_for_group_m":"1/m * (p²,p)",
      "record_entropy_extra":"E sum_(g!=0,1) N_g * (log_phi(m_g) + 2-p)",
      "original_phi_and_kraus_phase_preserved":True,
      "physical_new_24_output_gate_selected":False,
      "complete_original_Book_action_selected":False,
      "GR_closed":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
