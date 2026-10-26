#!/usr/bin/env python3
"""EXACT original native full128 one-tick Choi rank 18 (not numerical SVD).

Reuses ORIGINAL frozen CAR16/Julia/Walsh/Golden Kraus builder from
d0_original_full128_future_even_algebra_2026-10-22/
check_future_even_algebra_modprime.py. This source itself authenticates
all CAR, Julia roots, Golden CPTP, odd/even K, 64 dark labels and eight
known good algebraic finite-field embeddings.

Mathematical NEW input:
  upper bound: actual 32 nonduplicated Walsh endpoint operators span
  <= 10 ODD + 7 EVEN CAR/Julia matrices, so original Kraus <= 17+1=18;
  lower bound: ONE explicit actual original K(18 labels x18 true matrix
  entries) minor nonzero at ALL eight known good field reductions.

Different classical RECORD tasks:
  unobserved channel Choi rank18;
  original 24 projective-ray coarse RECORD CPTP rank24;
  original 64 live fine-label RECORD CPTP rank64.
The latter two rank identities are elementary block-Choi theorems,
using 24/64 already owned exact original output-label counts.
No new physical M1 task/Book03 action/cut/clock or GR promotion.

Run both python3 and python3 -O. No skipped assertions.
"""
from __future__ import annotations
from pathlib import Path
import json
import sys
import numpy as np

SOURCE=Path(__file__).resolve().parent.parent / (
    "d0_original_full128_future_even_algebra_2026-10-22")
sys.path.insert(0,str(SOURCE))
from check_future_even_algebra_modprime import (  # noqa: E402
    SPLIT_PRIMES, original_kraus_mod,
)

MINOR_FINE_ROWS=(0,18,8,16,32,48,2,1,64,26,58,40,24,11,90,56,122,72)
MINOR_FULL_COORDS=(0,1,3,5,6,9,16,17,18,19,32,33,48,49,64,65,128,129)
EXPECTED_DIRECT_MINOR={
    229:164,401:249,521:269,709:459,
    761:128,809:520,941:769,1009:886,
}
EXPECTED_GENERATOR_MINOR={
    229:69,401:165,521:429,709:368,
    761:609,809:180,941:745,1009:1,
}
CHECKS=0

def require(ok,msg):
    global CHECKS
    CHECKS+=1
    if not bool(ok):
        raise ArithmeticError(msg)

def rank_mod(matrix,mod):
    """True exact Gaussian row rank modulo one of the owned good primes."""
    A=np.asarray(matrix,dtype=np.int64).copy()%mod
    rows,cols=A.shape
    rank=0
    for j in range(cols):
        idx=next((i for i in range(rank,rows) if A[i,j]!=0),None)
        if idx is None:continue
        if idx!=rank:
            A[[idx,rank]]=A[[rank,idx]]
        scale=pow(int(A[rank,j]),-1,mod)
        A[rank]=(A[rank]*scale)%mod
        for i in range(rank+1,rows):
            q=int(A[i,j])
            if q:
                A[i]=(A[i]-q*A[rank])%mod
        rank+=1
        if rank==rows:break
    return rank

def det_mod(matrix,mod):
    A=np.asarray(matrix,dtype=np.int64).copy()%mod
    n=A.shape[0]
    require(A.shape==(n,n),"exact fixed square original submatrix")
    determinant=1
    for j in range(n):
        idx=next((i for i in range(j,n) if A[i,j]!=0),None)
        if idx is None:return 0
        if idx!=j:
            A[[idx,j]]=A[[j,idx]]
            determinant=(-determinant)%mod
        d=int(A[j,j])
        determinant=determinant*d%mod
        inverse=pow(d,-1,mod)
        for i in range(j+1,n):
            q=int(A[i,j])*inverse%mod
            if q:A[i]=(A[i]-q*A[j])%mod
    return determinant%mod

def original_generator_certificate(row):
    """17 true ORIGINAL 0/1-Walsh-endpoint matrices -> 18 K span.
    Does not postulate a synthetic 18-Kraus quantum channel.
    """
    mod,root5,p,rootp,root_julia,root_i=map(int,row)
    inv=lambda n:pow(int(n)%mod,-1,mod)
    I=np.eye(16,dtype=np.int64)
    Z=np.zeros((16,16),dtype=np.int64)
    mul=lambda A,B:(A@B)%mod
    creators=[]
    order=(0,2,3,1)
    for role in range(4):
        C=Z.copy()
        prior=order[:order.index(role)]
        for bits in range(16):
            if not (bits>>role)&1:
                C[bits|(1<<role),bits]=(-1)**sum(
                    (bits>>j)&1 for j in prior)
        creators.append(C%mod)
    c0,c1,c2,c3=creators
    G=(mul(c0,c1.T)+mul(c1,c0.T))%mod
    U=(I+inv(40)*mul(G,G)+9*inv(40)*G)%mod
    require(np.array_equal(mul(mul(G,G),G),G),
            "TRUE original G^3=G")
    nu=3*inv(5)%mod
    root_observed=(0,9*inv(25)%mod,7929*inv(20000)%mod)
    val_observed=(1,4*inv(5)%mod,root_julia)
    def moved_root(T):
        out=Z.copy()
        for k in range(3):
            numerator=I.copy()
            denominator=1
            for j in range(3):
                if j!=k:
                    numerator=mul(numerator,(T-root_observed[j]*I)%mod)
                    denominator=denominator*(root_observed[k]-root_observed[j])%mod
            out=(out+val_observed[k]*inv(denominator)*numerator)%mod
        require(np.array_equal((mul(out,out)+T)%mod,I),
                "ORIGINAL positive Julia root polynomial, exact modulo prime")
        return out
    x=nu*mul(c1,U)%mod
    L=moved_root(mul(x,x.T))
    R=moved_root(mul(x.T,x))
    # Actual duplicated Walsh-row zero endpoint, exactly as in the
    # frozen original generator; i phase evaluated only AFTER the
    # formal symbolic source matrix coefficient is composed.
    a=(
        nu*inv(16)*(
            (root_i-1)*c0+(-root_i-1)*c0.T+
            root_i*mul(c1,U)-root_i*mul(U,c1.T)-c1-c1.T
        )
        -nu*inv(8)*(c2+c2.T)
        +nu*inv(16)*((-1-root_i)*c3+(-1+root_i)*c3.T)
    )%mod
    # The 10 odd original endpoint operators contain all original
    # creator/adjoint+moving-Lorentz ingredients.
    odd=(c0,c0.T,c1,c1.T,c2,c2.T,c3,c3.T,
         mul(c1,U),mul(U,c1.T))
    # All static roots are uI +/- vZ_j, plus two actual moved roots.
    even=(I,*[(I-2*mul(c.T,c))%mod for c in creators],L,R)
    require(len(odd)==10 and len(even)==7,
            "TRUE original CAR/Julia 10+7 endpoint-generator upper bound")
    raw=np.stack([*odd,*even]).reshape(17,256)%mod
    require(rank_mod(raw,mod)==17,
            "all 17 ORIGINAL Julia/Walsh endpoint generator matrices independent")
    bases=np.stack([I,*[mul(B.T,a) for B in (*odd,*even)]])%mod
    require(rank_mod(bases.reshape(18,256),mod)==18,
            "original 17 right-multiplied Walsh generators + exceptional I rank18")
    det=det_mod(bases.reshape(18,256)[:,MINOR_FULL_COORDS],mod)
    require(det==EXPECTED_GENERATOR_MINOR[mod],
            "frozen 18 generator minor has native algebraic field residue")
    delta=mul(a,a) # a=N0 is exactly Hermitian BEFORE embedding complex i
    expect0=(I-2*p*p*delta)%mod
    expect1=(-2*p*rootp*delta)%mod
    return bases.reshape(18,256),expect0,expect1

def main():
    require(len(MINOR_FINE_ROWS)==18 and len(set(MINOR_FINE_ROWS))==18,
            "18 DISTINCT actual original K fine-label indices")
    require(len(MINOR_FULL_COORDS)==18 and len(set(MINOR_FULL_COORDS))==18,
            "18 DISTINCT actual original 16x16 matrix coordinates")
    output={}
    for row in SPLIT_PRIMES:
        mod=int(row[0])
        d=original_kraus_mod(row) # unchanged original all128 Kraus
        K=np.asarray(d["K"],dtype=np.int64)%mod
        require(K.shape==(128,16,16),"complete untouched original full128 K")
        nonzero=np.flatnonzero(np.any(K.reshape(128,-1)!=0,axis=1))
        require(len(nonzero)==64,"exact original 64 nonzero plus64 dark fine slots")
        require(0 in nonzero and 1 in nonzero and
                all(i in nonzero for i in MINOR_FINE_ROWS),
                "original minor consumes only TRUE nonzero labelled Kraus")
        V=K.reshape(128,256)
        require(rank_mod(V,mod)==18,
                "actual source-owned full original K Choi rank EXACT18")
        witness=det_mod(V[np.array(MINOR_FINE_ROWS)][:,MINOR_FULL_COORDS],mod)
        require(witness==EXPECTED_DIRECT_MINOR[mod] and witness!=0,
                "EXACT original K 18x18 minor nonzero at certified prime")
        B,K0,K1=original_generator_certificate(row)
        require(np.array_equal(K[0],K0) and np.array_equal(K[1],K1),
                "actual source native K0 and K1 use THE SAME original N0 CAR row")
        require(rank_mod(np.concatenate((V,B),axis=0),mod)==18,
                "all original 128 literal K lie in true 18 generator-span after reduction")
        output[str(mod)]={
          "raw_Kraus_rank":18,
          "literal_original_nonzero_fine_Kraus":64,
          "original_K_18_minor":witness,
          "original_17plus1_CAR_generator_minor":EXPECTED_GENERATOR_MINOR[mod]
        }
    print(json.dumps({
       "status":"PASS_EXACT_ORIGINAL_FULL128_CHOIRANK_18_UNOBSERVED_24_COARSE_64_FINE",
       "checks":CHECKS,
       "native_field_r":"1/9","native_nu":"3/5",
       "all_8_original_split_prime_original_K_minors":output,
       "original_Kraus_channel_Choi_rank":18,
       "minimal_unobserved_Stinespring_bath_dimension":18,
       "original_24_class_recorded_instrument_Choi_rank":24,
       "original_64_live_fine_label_recorded_instrument_Choi_rank":64,
       "full_original_formal_fine_alphabet":128,
       "minimal_fixed_length_fine_record_binary_bits":6,
       "minimal_fixed_length_24_class_binary_bits":5,
       "matrix_17_generator_upper_bound_proof":"original Walsh parity duplication plus static/moved CAR roots",
       "global_native_action_Book_M1_selected":False,
       "GR_closed":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
