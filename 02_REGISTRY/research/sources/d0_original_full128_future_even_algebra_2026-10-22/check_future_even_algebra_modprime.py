#!/usr/bin/env python3
"""EXACT finite-field certificate: original CAR16/Julia/Walsh/Golden128
three-tick no-reset fine-history POVM effects span the complete
fermion-parity-even operator algebra M8(C) + M8(C).

This is a proof of ORIGINAL finite operational effect completeness at the
pinned r=1/9, nu=3/5, phases=(i,i,-1,-i) fixture, not a proof of
compulsory Book03 information/price or GR. No float arithmetic in the
certificate. Requires numpy for exact bounded int64 matrix operations.
Use python3 check_future_even_algebra_modprime.py and python3 -O ...

The formulas are the five original functions adj/herm/root/creators/native
from original file blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
transcribed into a finite characteristic specialization; no iid reset.
"""
from __future__ import annotations
import collections
import hashlib
import json
import numpy as np

# (prime, image sqrt(5), image golden p=1/phi, image sqrt(p),
#  image sqrt(12071/20000), image i). Each tuple satisfies all equations.
SPLIT_PRIMES = (
    (229, 66, 147, 39, 78, 107),
    (401, 178, 289, 17, 27, 20),
    (521, 199, 99, 52, 215, 235),
    (709, 341, 170, 322, 234, 96),
    (761, 183, 91, 231, 358, 39),
    (809, 124, 466, 320, 377, 318),
    (941, 455, 227, 449, 451, 97),
    (1009, 244, 626, 226, 278, 469),
)
SOURCE_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
TEST_PATHS_SHA256 = "7da6c5e307a8afac819f4096a8c173576b2498f9faede3e316ec21e7b0485e3a"
TOTAL_CHECKS = 0


def check(condition, description):
    global TOTAL_CHECKS
    TOTAL_CHECKS += 1
    if not bool(condition):
        raise ArithmeticError(description)


def original_kraus_mod(prime_data):
    prime, root5, p, rootp, rootq, rooti = prime_data
    m = prime
    check(root5 * root5 % m == 5 % m, "sqrt5 split")
    check((p * 2 - (root5 - 1)) % m == 0, "original p=phi^-1")
    check((p*p + p - 1) % m == 0, "original p+p^2=1")
    check((rootp*rootp-p) % m == 0, "original Golden sqrtp")
    check((rootq*rootq*20000-12071) % m == 0, "Julia moved square root")
    check((rooti*rooti+1) % m == 0, "original complex i")
    check(prime < 10_000, "int64 exact safety with 16x16 dot")

    inv = lambda n: pow(int(n) % m, -1, m)
    eye = np.eye(16, dtype=np.int64)
    zero = np.zeros((16, 16), dtype=np.int64)
    mul = lambda a,b: (a @ b) % m
    plus = lambda a,b: (a+b) % m
    sub = lambda a,b: (a-b) % m
    sc = lambda x,a: (int(x)*a) % m
    real = lambda a: (a,zero.copy())
    pair_plus = lambda a,b: (plus(a[0],b[0]),plus(a[1],b[1]))
    pair_scale = lambda x,a: (sc(x,a[0]),sc(x,a[1]))
    pair_adj = lambda a: (a[0].T,sc(-1,a[1].T))
    def pair_mul(a,b):
        return (sub(mul(a[0],b[0]),mul(a[1],b[1])),
                plus(mul(a[0],b[1]),mul(a[1],b[0])))
    # The complex dagger is formed SYMBOLICALLY using (a+ib)* = a-ib
    # BEFORE evaluating i as the finite-field square root rooti.
    evaluate = lambda a: plus(a[0],sc(rooti,a[1]))
    evaluate_adj = lambda a: sub(a[0].T,sc(rooti,a[1].T))

    # The ACTUAL 4-CAR original creator ordering (0,2,3,1).
    order = (0,2,3,1)
    cs = []
    for r in range(4):
        c = zero.copy()
        before = order[:order.index(r)]
        for bits in range(16):
            if not (bits >> r) & 1:
                sign=(-1)**sum((bits >> j) & 1 for j in before)
                c[bits | (1 << r), bits] = sign
        cs.append(c % m)
    for i in range(4):
        for j in range(4):
            check(not np.any((mul(cs[i],cs[j])+mul(cs[j],cs[i]))%m),
                  "actual CAR anti-commuting creators")
            cc=(mul(cs[i],cs[j].T)+mul(cs[j].T,cs[i]))%m
            check(np.array_equal(cc,eye if i==j else zero),
                  "actual CAR mixed canonical anti-commutator")
    generator = plus(mul(cs[0],cs[1].T),mul(cs[1],cs[0].T))
    check(np.array_equal(mul(mul(generator,generator),generator),generator),
          "original boost generator G^3=G")
    # Original theta=2atanh(1/9)=ln(5/4), so cosh=41/40, sinh=9/40.
    U = plus(plus(eye,sc(inv(40),mul(generator,generator))),
             sc(9*inv(40),generator))
    nu = 3*inv(5) % m
    t1 = 9*inv(25) % m
    t2 = 7929*inv(20000) % m
    check((1-t1-(4*inv(5))**2)%m==0,"Julia nonmoving spectrum 9/25")
    check((1-t2-rootq*rootq)%m==0,"Julia moved spectrum 7929/20000")

    def positive_julia_root(T):
        # Algebraic functional calculus: sqrt(I-T) on EXACT eigenvalues
        # 0, 9/25, 7929/20000. Positive REAL sign is taken in source
        # field; modular images are a valid specialization.
        roots = (0,t1,t2)
        values = (1,4*inv(5)%m,rootq)
        result = zero.copy()
        for k in range(3):
            numerator = eye.copy()
            denominator = 1
            for j in range(3):
                if j!=k:
                    numerator = mul(numerator,sub(T,sc(roots[j],eye)))
                    denominator = denominator * (roots[k]-roots[j]) % m
            result=plus(result,sc(values[k]*inv(denominator),numerator))
        check(not np.any((mul(result,result)-eye+T)%m),
              "EXACT moved Julia sqrt polynomial")
        return result

    words=[]
    for r,c in enumerate(cs):
        base = sc(nu,c)
        operand = mul(base,U) if r==1 else base
        # Original phases i,i,-1,-i, all evaluated symbolically.
        if r in (0,1): x=(zero.copy(),operand)
        elif r==2: x=(sc(-1,operand),zero.copy())
        else: x=(zero.copy(),sc(-1,operand))
        xx=pair_mul(x,pair_adj(x))
        yy=pair_mul(pair_adj(x),x)
        check(not np.any(xx[1]) and not np.any(yy[1]),
              "original Julia even positive real spectral operands")
        if r==1:
            for T in (xx[0],yy[0]):
                zero_poly=mul(mul(T,sub(T,sc(t1,eye))),sub(T,sc(t2,eye)))
                check(not np.any(zero_poly),
                      "EXACT original moved spectral cubic")
            left=positive_julia_root(xx[0])
            right=positive_julia_root(yy[0])
        else:
            left=sub(eye,sc(inv(5),mul(c,c.T)))
            right=sub(eye,sc(inv(5),mul(c.T,c)))
            check(not np.any((mul(left,left)-eye+xx[0])%m),
                  "EXACT original static Julia left sqrt")
            check(not np.any((mul(right,right)-eye+yy[0])%m),
                  "EXACT original static Julia right sqrt")
        l0=sub(eye,sc(inv(5),mul(c,c.T)))
        r0=sub(eye,sc(inv(5),mul(c.T,c)))
        for word in (
            (x,real(left)),
            (pair_adj(x),real(right)),
            (real(sc(-1,base)),real(sc(-1,l0))),
            (real(sc(-1,base.T)),real(sc(-1,r0))),
        ):
            words.extend((word,word))
    check(len(words)==32,"original duplicated Julia Walsh words")

    # Original 32 Walsh rows, 2 endpoints per row.
    rows=[]
    for label in range(32):
        signs=[(-1)**(bin(label & j).count("1")%2) for j in range(32)]
        for b in range(2):
            rr=zero.copy()
            ii=zero.copy()
            for j in range(32):
                rr=(rr+signs[j]*words[j][b][0])%m
                ii=(ii+signs[j]*words[j][b][1])%m
            rows.append(pair_scale(inv(32),(rr,ii)))
    check(len(rows)==64,"original 64 Walsh endpoint rows")
    a=rows[0]
    K=[]
    for j,nj in enumerate(rows):
        v=pair_mul(pair_adj(nj),a)
        k0=pair_plus(real(eye if j==0 else zero.copy()),
                     pair_scale(-2*p*p,v))
        k1=pair_scale(-2*p*rootp,v)
        K.extend((k0,k1))
    check(len(K)==128,"actual native full128 fine Kraus")
    KE=np.asarray([evaluate(k) for k in K],dtype=np.int64)%m
    KD=np.asarray([evaluate_adj(k) for k in K],dtype=np.int64)%m
    nonzero=[j for j,kk in enumerate(KE) if np.any(kk)]
    check(len(nonzero)==64, "EXACT original 64 dark +64 nonzero fine slots")
    check(sum(np.any(KE[j]) for j in range(1,128,2))==32,
          "nonzero odd-label count")
    cptp = zero.copy()
    for j in range(128):
        cptp=plus(cptp,mul(KD[j],KE[j]))
    check(np.array_equal(cptp,eye),"EXACT native 128-Kraus CPTP")

    parity=np.asarray([(-1)**(bin(k).count("1")%2) for k in range(16)],
                      dtype=np.int64)
    even=[k for k in range(16) if parity[k]==1]
    odd=[k for k in range(16) if parity[k]==-1]
    counts={"even":0,"odd":0}
    for j in nonzero:
        M=KE[j]
        comm=(parity[:,None]*M-M*parity[None,:])%m
        anti=(parity[:,None]*M+M*parity[None,:])%m
        check((not np.any(comm)) != (not np.any(anti)),
              "every original Kraus parity-homogeneous")
        counts["even" if not np.any(comm) else "odd"]+=1
    check(counts=={"even":32,"odd":32}, "original exact even/odd Kraus count")
    return {"m":m,"K":KE,"Kd":KD,"nonzero":nonzero,
            "even":even,"odd":odd,"I":eye,"parity_counts":counts}


def parity_vector(X,d):
    e=d["even"];o=d["odd"]
    return np.concatenate((X[np.ix_(e,e)].reshape(-1),
                           X[np.ix_(o,o)].reshape(-1)))%d["m"]


def effect_of_word(word,d):
    """Exact original no-reset Born effect for a chronological word."""
    X=d["I"].copy()
    for j in reversed(word):
        X=(d["Kd"][j] @ X @ d["K"][j])%d["m"]
    return X


def mod_span_selected(d,chosen_words):
    """Exact Gauss rank of ACTUAL 128 selected histories, no SVD/tolerance."""
    m=d["m"]
    pivots=[]
    echelon=[]
    for path in chosen_words:
        vec=parity_vector(effect_of_word(path,d),d)
        for pivot,row in zip(pivots,echelon):
            if vec[pivot]:
                vec=(vec-vec[pivot]*row)%m
        loc=np.flatnonzero(vec)
        if len(loc):
            pivot=int(loc[0])
            vec=(vec*pow(int(vec[pivot]),-1,m))%m
            pivots.append(pivot)
            echelon.append(vec)
    return len(pivots)


def actual_future_basis(d):
    """Choose independent ORIGINAL WORDS, not synthetic linear combinations.

    An independent actual history effect basis spans the same linear space
    as all histories of that depth. Applying each Heisenberg Kraus update
    to that basis therefore spans every next round; no 64^3 listing needed.
    """
    m=d["m"]
    pivots=[];echelon=[];representatives=[];paths=[]
    def insert(X,path):
        vec=parity_vector(X,d)
        for pivot,row in zip(pivots,echelon):
            if vec[pivot]:
                vec=(vec-vec[pivot]*row)%m
        loc=np.flatnonzero(vec)
        if len(loc)==0:return False
        pivot=int(loc[0])
        vec=(vec*pow(int(vec[pivot]),-1,m))%m
        pivots.append(pivot)
        echelon.append(vec)
        representatives.append(X.copy())
        paths.append(path)
        return True
    for j in d["nonzero"]:
        insert(effect_of_word((j,),d),(j,))
    ranks={1:len(paths)}
    for depth in (2,3):
        old=list(zip(representatives,paths))
        for X,path in old:
            for j in d["nonzero"]:
                candidate=(d["Kd"][j]@X@d["K"][j])%m
                insert(candidate,(j,)+path)
                if len(paths)==128:
                    break
            if len(paths)==128:break
        ranks[depth]=len(paths)
    check(ranks=={1:11,2:122,3:128},
          "ORIGINAL exact GFp future-effect rank 11/122/128")
    check(len(paths)==128, "full 128-dimensional even-algebra effect span")
    check(set(pivots)==set(range(128)),"all 128 parity matrix coordinates independent")
    return ranks,paths,pivots



def verify_original_65_merged_future(d,prime_data,selected_words):
    """Independent exact source-algebra check for original 128->65
    paired Golden bits on SAME no-reset paths, including dark rows."""
    m=d["m"]
    p=prime_data[2]
    sqrtp=prime_data[3]
    invp=pow(int(p),-1,m)
    check((p*p+p-1)%m==0,"Golden pair keeps full CPTP")
    check((p**3-(2*p-1))%m==0,"original exact p^3 paid coin residual")
    check(len(d["K"])==128,"literal original 128 fine K")
    L=[d["K"][0],d["K"][1]]
    LD=[d["Kd"][0],d["Kd"][1]]
    for row in range(1,64):
        fine0=2*row
        fine1=fine0+1
        elem=(d["K"][fine0]*invp)%m
        adj=(d["Kd"][fine0]*invp)%m
        check(np.array_equal((sqrtp*elem)%m,d["K"][fine1]),
              "original every j>0 twin K=(pL,sqrtp L)")
        check(np.array_equal((sqrtp*adj)%m,d["Kd"][fine1]),
              "original every j>0 dagger twin")
        L.append(elem)
        LD.append(adj)
    check(len(L)==65,"65 precise merged native Kraus slots")
    comp=np.zeros((16,16),dtype=np.int64)
    for a,b in zip(L,LD):
        comp=(comp+b@a)%m
    check(np.array_equal(comp,d["I"]),
          "whole 65 merged instrument keeps exact original CPTP")
    for path in selected_words:
        w=1
        merged=[]
        for a in path:
            if a<=1:
                merged.append(a)
            else:
                row=a//2
                merged.append(row+1)
                w=(w*(p*p if a%2==0 else p))%m
        # Original no-reset chronological effect for these SAME outputs.
        X=d["I"].copy()
        for k in reversed(tuple(merged)):
            X=(LD[k]@X@L[k])%m
        E128=effect_of_word(path,d)
        check(np.array_equal(E128,(w*X)%m),
              "no original future effect lost by 65 labelled predictor")
    return len(L)

def main():
    reference=SPLIT_PRIMES[-1]
    native=original_kraus_mod(reference)
    ranks,words,pivots=actual_future_basis(native)
    digest=hashlib.sha256(
        json.dumps(words,separators=(",",":")).encode("utf-8")).hexdigest()
    check(digest==TEST_PATHS_SHA256,"frozen genuine 128-word test set")
    verify_primes={}
    for row in SPLIT_PRIMES:
        spec=original_kraus_mod(row)
        rank=mod_span_selected(spec,words)
        check(rank==128,"same 128 physical words independent mod prime")
        check(verify_original_65_merged_future(spec,row,words)==65,
              "complete 65-label predictor retains all 128 effect basis rows")
        verify_primes[str(row[0])]=rank
    length_hist=dict(sorted(collections.Counter(map(len,words)).items()))
    check(length_hist=={1:11,2:111,3:6},
          "finite three-round original test distribution")
    print(json.dumps({
      "status":"PASS_EXACT_MODULAR_ORIGINAL_CAR16_3TICK_EVEN_EFFECT_COMPLETENESS",
      "checks":TOTAL_CHECKS,
      "original_source_blob":SOURCE_BLOB,
      "actual_native_fine_Kraus_slots":128,
      "source_faithful_native_merged_labels":65,
      "native_pair_port_Cost_minus_Information":"p^3=2p-1 exact",
      "nonzero_Kraus_slots":64,
      "original_Kraus_even_odd_counts":native["parity_counts"],
      "modular_future_ranks_by_depth":ranks,
      "operator_algebra_upper_bound_from_fermion_parity":128,
      "selected_original_no_reset_words_by_length":length_hist,
      "same_word_rank_over_eight_split_primes":verify_primes,
      "selected_original_test_words_sha256":digest,
      "GR_closed":False,
      "compulsory_Book03_price_selected":False
    },sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
