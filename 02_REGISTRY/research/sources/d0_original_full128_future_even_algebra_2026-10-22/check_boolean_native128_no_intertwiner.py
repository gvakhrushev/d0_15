#!/usr/bin/env python3
"""Exact native ORIGINAL 128-Kraus vs Boolean Book-projector no-intertwiner.

Uses the established exact CAR16/Galois modular builder beside this file.
No floating point or invented gravity action. Checks eight good split primes
of the true native CAR source. Ordinary/-O parity enforced by explicit guards.
"""
from __future__ import annotations

import json
import numpy as np

from check_future_even_algebra_modprime import (
    SPLIT_PRIMES, original_kraus_mod, check
)

def independent_count(mod, matrices):
    pivots=[]
    echelon=[]
    positions=[]
    for i,mat in enumerate(matrices):
        vec=mat.reshape(-1).copy()
        for j,row in zip(pivots,echelon):
            if vec[j]:
                vec=(vec-vec[j]*row)%mod
        idx=np.flatnonzero(vec)
        if len(idx)==0:
            continue
        j=int(idx[0])
        echelon.append((vec*pow(int(vec[j]),-1,mod))%mod)
        pivots.append(j)
        positions.append(i)
    return len(positions),positions

def verify_fixture(entry):
    data=original_kraus_mod(entry)
    prime=data["m"]
    p=entry[2]
    rp=entry[3]
    K=data["K"]
    Kd=data["Kd"]
    I=data["I"]
    eye=np.eye(16,dtype=np.int64)
    def matmul(a,b):return (a@b)%prime
    def sc(n,a):return (int(n)*a)%prime
    check(np.array_equal(eye,I), "same original CAR16 basis")
    inv=lambda n:pow(int(n)%prime,-1,prime)
    D=sc(inv(2*p*p),(I-K[0])%prime)
    check(np.array_equal(K[1],sc(-2*p*rp,D)),
          "original j0 orphan K1 exactly -2p sqrtp Delta")
    check(np.any((matmul(D,D)-D)%prime),
          "ORIGINAL Delta is NOT a Boolean projection")
    check(np.any(D),"original Delta nonzero")
    check(not np.array_equal(D,I),"original Delta not identity")
    complementary=(I-matmul(Kd[0],K[0])-matmul(Kd[1],K[1]))%prime
    predicted=sc(4*p*p,matmul(D,(I-D)%prime))
    check(np.array_equal(complementary,predicted),
          "EXACT original missing j>0 port source = 4p² Delta(I-Delta)")
    qnb=np.zeros((16,16),dtype=np.int64)
    for k in range(2,128):
        qnb=(qnb+matmul(Kd[k],K[k]))%prime
    check(np.array_equal(qnb,complementary),
          "actual 126 original j>0 fine outcomes exhaust missing sector")
    rankC,_=independent_count(prime, [complementary[:,j].copy()
                                      for j in range(16)])
    check(rankC==16,"original extra nonblank effect has FULL DATA rank16")

    # Every nonblank pair is the two original Golden factors of same M_j.
    L=[]
    for j in range(1,64):
        k0=K[2*j]
        k1=K[2*j+1]
        check(np.array_equal(sc(rp,k0),sc(p,k1)),
              "original K_j twin p L_j /sqrtp L_j")
        L.append(k0)
    rankL,pivots=independent_count(prime,L)
    check(rankL==17,
          "exact modular rank17 of original nonblank Kraus family")
    fixed_j=[
        1,4,5,8,9,12,13,16,20,24,28,29,32,36,45,48,61
    ]
    explicit=[K[2*j] for j in fixed_j]
    rfixed,_=independent_count(prime,explicit)
    check(rfixed==17,
          "same 17 originally named nonblank Kraus labels are independent")
    return {
      "original_full_EXTRA_effect_rank":rankC,
      "nonblank_Kraus_Choi_rank_at_least":rankL,
      "fixed_17_independent_original_rows":fixed_j
    }

def main():
    results={}
    for entry in SPLIT_PRIMES:
        results[str(entry[0])]=verify_fixture(entry)
    print(json.dumps({
        "status":"PASS_EXACT_NATIVE128_BOOLEAN_BOOK_SOURCE_NO_INTERTWINER",
        "split_prime_checks":results,
        "theorem":"nonprojector Delta forbids invariant binary-Boolean poststate intertwiner; original nonblank Choi rank at least17",
        "GR_closed":False,
        "physical_common_Book03_implementation_proved":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
