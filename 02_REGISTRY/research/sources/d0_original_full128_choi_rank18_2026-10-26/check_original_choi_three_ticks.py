#!/usr/bin/env python3
"""EXACT ORIGINAL full128 3-tick Kraus span M16 / Choi rank 256.

Uses the UNCHANGED native CAR16/Julia/Walsh/Golden Kraus constructor and
its eight authenticated split primes, no DATA reset or invented 256x256
channel. Selects ONE deterministic list of 256 actual 3-tick histories
and checks its EXACT full 256x256 determinant over all eight original
algebraic-field reductions. No floating rank/SVD; works with python -O.

Consequences proved in companion theorem:
- Choi rank Phi = 18, Choi rank Phi^3=256 (maximal);
- Phi^3 is positivity improving;
- a strictly positive quantum Doeblin coefficient exists for all
  original DATA states at the same authenticated native fixture;
- closed whole DATA+ARCHIVE information is NOT claimed erased or free;
- native Book H+J+R/GR selection remains OPEN.

This script is only the exact finite-algebraic certificate.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

SOURCE=Path(__file__).resolve().parent.parent / (
    "d0_original_full128_future_even_algebra_2026-10-22")
sys.path.insert(0,str(SOURCE))
from check_future_even_algebra_modprime import (  # noqa E402
    SPLIT_PRIMES, original_kraus_mod,
)

FIXED_256_HISTORY_SHA256 = (
    "78f343fe8a763998dd062310d1fb45c1a295771d3344f43016201f146924ed78"
)
EXPECTED_3TICK_DET={
    229:106,401:39,521:111,709:264,
    761:404,809:277,941:641,1009:260,
}
EXPECTED_2TICK_BASIS_SHA256=(
    "02d122c91575adb71ac135a3201cd397951d5d6fcb2d4c39ea9b32460035d678"
)
FIXED_REMOVED_PIVOT_POSITIONS={198,199,200,201}
FIXED_FOUR_REPAIR_WORDS=[
    (2,16,2),(24,18,2),(26,18,2),(58,18,2)
]
CHECKS=0

def require(ok,message):
    global CHECKS
    CHECKS+=1
    if not bool(ok):
        raise ArithmeticError(message)

def independent_actual_indices(rows,mod,limit=256):
    """Streaming EXACT Fp elimination. Input items are ORIGINAL K products.
    Each retained independent vector is normalized at its real first pivot.
    """
    chosen=[]
    pivots=[]
    basis=[]
    for t,row in enumerate(rows):
        v=np.asarray(row,dtype=np.int64).reshape(-1).copy()%mod
        require(len(v)==256,"one original DATA16 operator has exactly 256 coefficients")
        for c,b in zip(pivots,basis):
            scale=int(v[c])
            if scale:v=(v-scale*b)%mod
        candidates=np.flatnonzero(v)
        if len(candidates):
            c=int(candidates[0])
            v=(v*pow(int(v[c]),-1,mod))%mod
            pivots.append(c)
            basis.append(v)
            chosen.append(t)
            if len(chosen)==limit:break
    return chosen

def rank_from_actual_rows(rows,mod):
    return len(independent_actual_indices(rows,mod))

def determinant_mod(matrix,mod):
    M=np.asarray(matrix,dtype=np.int64).copy()%mod
    n=M.shape[0]
    require(M.shape==(n,n),"certified original square Kraus matrix")
    det=1
    for j in range(n):
        i=next((t for t in range(j,n) if M[t,j]),None)
        if i is None:return 0
        if i!=j:
            M[[i,j]]=M[[j,i]]
            det=-det
        p=int(M[j,j])
        det=det*p%mod
        inverse=pow(p,-1,mod)
        for t in range(j+1,n):
            scale=int(M[t,j])*inverse%mod
            if scale:
                M[t]=(M[t]-scale*M[j])%mod
    return det%mod

def selected_genuine_words(K1009):
    q=1009
    require(K1009.shape==(128,16,16),"actual 128 fine original Kraus")
    one_idx=independent_actual_indices(K1009,q)
    require(len(one_idx)==18,"original 1tick exact rank18")
    B1=K1009[one_idx]
    two=[(A@B)%q for A in B1 for B in B1]
    two_idx=independent_actual_indices(two,q)
    require(len(two_idx)==144,"actual 2tick rank at authenticated modular fixture")
    B2=[two[j] for j in two_idx]
    # Actual 3tick Kraus matrices K_left K_mid K_first.
    # No equality of order-reversed words is assumed or used.
    three_idx=independent_actual_indices(
        ((A@B)%q for A in B1 for B in B2),q)
    require(len(three_idx)==256,
            "complete 3tick original Kraus M16 rank256, max possible")
    raw=[]
    for pos in three_idx:
        outer=pos//len(B2)
        mid=pos%len(B2)
        t2=two_idx[mid]
        left=t2//len(B1)
        right=t2%len(B1)
        raw.append((int(one_idx[right]),
                    int(one_idx[left]),
                    int(one_idx[outer])))
    require(len(raw)==256,"256 true original full-length chronological words")
    final=[p for i,p in enumerate(raw)
           if i not in FIXED_REMOVED_PIVOT_POSITIONS]
    final+=FIXED_FOUR_REPAIR_WORDS
    require(len(final)==256 and len(set(final))==256,
            "fixed original four-word 401-prime source repair")
    digest=hashlib.sha256(
        json.dumps(final,separators=(",",":")).encode("utf8")).hexdigest()
    require(digest==FIXED_256_HISTORY_SHA256,
            "frozen actual selected original words exact SHA256")
    two_paths=[
        (int(one_idx[j%len(B1)]),int(one_idx[j//len(B1)]))
        for j in two_idx
    ]
    digest2=hashlib.sha256(
        json.dumps(two_paths,separators=(",",":")).encode("utf8")).hexdigest()
    require(digest2==EXPECTED_2TICK_BASIS_SHA256,
            "same original 144 exact finite 2tick basis word list")
    return final,two_paths,one_idx

def main():
    pdata=next(x for x in SPLIT_PRIMES if int(x[0])==1009)
    initial=original_kraus_mod(pdata)
    words3,words2,words1=selected_genuine_words(
        np.asarray(initial["K"],dtype=np.int64))
    require(len(set(words1))==18 and len(words2)==144,
            "one/two native horizon basis information preserved")
    certificate={}
    for row in SPLIT_PRIMES:
        q=int(row[0])
        actual=original_kraus_mod(row)
        K=np.asarray(actual["K"],dtype=np.int64)%q
        require(K.shape==(128,16,16),"full unchanged original CAR16 fine128")
        # All original fine chronological operations, not synthetic matrices
        two=[(K[b]@K[a])%q for a,b in words2]
        require(rank_from_actual_rows(two,q)==144,
                "SAME 144 original real 2tick words independently exact")
        three=np.stack([
            ((K[c]@K[b]@K[a])%q).reshape(-1)
            for a,b,c in words3
        ])
        require(three.shape==(256,256),
                "actual 256 original 3tick Kraus vectors, no dropped rows")
        det=determinant_mod(three,q)
        require(det==EXPECTED_3TICK_DET[q] and det!=0,
                "SAME frozen complete 3tick original K determinant exact over Fp")
        certificate[str(q)]={"actual_2tick_independent_K_words":144,
                             "actual_3tick_minor_nonzero":det,
                             "actual_3tick_K_operator_rank":256}
    print(json.dumps({
        "status":"PASS_EXACT_ORIGINAL_FULL128_THREE_TICK_MAXIMAL_KRAUS_CHOIRANK",
        "checks":CHECKS,
        "source":"unchanged certified original CAR16/Julia/Walsh/Golden128",
        "native_fixture":{"r":"1/9","nu":"3/5"},
        "full_fine_alphabet":128,
        "original_nonzero_labels":64,
        "one_tick_original_kraus_Choi_rank":18,
        "two_tick_certified_minimum_Choi_rank":144,
        "three_tick_original_kraus_Choi_rank":256,
        "three_tick_chronological_full_length_K_word_count":256,
        "three_tick_frozen_word_SHA256":FIXED_256_HISTORY_SHA256,
        "eight_same_actual_word_minors":certificate,
        "strict_positivity_of_Phi_cubed":"follows from positive definite Choi",
        "data_tracenorm_Doeblin_contraction":
            "||Phi^3(rho)-Phi^3(sigma)||_1 <= "
            "(1-16*lambda_min(Choi(Phi^3)))*||rho-sigma||_1",
        "environment_min_dim_1tick":18,
        "environment_min_dim_3tick":256,
        "full_archive_erased":False,
        "GR_closed":False
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
