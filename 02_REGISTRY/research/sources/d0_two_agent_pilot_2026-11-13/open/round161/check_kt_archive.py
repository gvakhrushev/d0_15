"""Exact lossless Golden KT code and its outward transverse derivative check."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PILOT/"direct/round78/h1_code"))
sys.path.insert(0,str(PILOT/"direct/round76/record"))
import check_type_code as code
import check_noisy_site_price as interval

I,O = interval.I,interval.O
PINS = {
    "direct/round78/h1_code/TYPE_CODE_RU.md":
        "fb1ce41205075545c31e34b5b663fe3fb1f6f6345a66b1222473ff769092649d",
    "direct/round78/h1_code/check_type_code.py":
        "7c1d761e86d2aa1e5c1dda8e6de25c76f6d1703892d6b1952a2aac552d3c3f6e",
    "direct/round78/selection/H1_EQUATIONS_RU.md":
        "8d95e35baa5c0e48c761dc952007fc81b44b5e5dc59f28b8e1efb95cd27c8a98",
}
COMPENSATION = 8
PHI = code.add(code.ONE,code.P)


@lru_cache(maxsize=None)
def rising(a,n):
    y = Q(1)
    for j in range(n):
        y *= a+j
    return y


def types(n,d):
    if d == 1:
        yield (n,)
        return
    for u in range(n+1):
        for tail in types(n-u,d-1):
            yield (u,*tail)


def kt_type(counts):
    n,d = sum(counts),len(counts)
    mass = Q(1)/rising(Q(d,2),n)
    arrangements = 1
    for k in counts:
        arrangements *= comb(n,k)
        n -= k
        mass *= rising(Q(1,2),k)
    return mass,arrangements


def golden_interval(lo,hi):
    lo_f,hi_f,mid = code.field(lo),code.field(hi),code.field((lo+hi)/2)
    pos,span = (0,0),code.ONE
    result = []
    while code.sign(code.sub(pos,lo_f)) < 0 or code.sign(code.sub(code.add(pos,span),hi_f)) > 0:
        left = code.mul(span,code.P)
        cut = code.add(pos,left)
        if code.sign(code.sub(mid,cut)) < 0:
            result.append(0)
            span = left
        else:
            result.append(1)
            pos,span = cut,code.sub(span,left)
    bound = code.mul(code.mul(code.P,code.P),code.field((hi-lo)/2))
    O.require(code.sign(code.sub(span,bound)) > 0, "shortest contained Golden cylinder")
    return code.emit(result)


def fixed_weight_index(rank,total):
    if total == 1:
        return ""
    counts = [1,1]
    while counts[-1] < total:
        counts.append(counts[-1]+counts[-2])
    weight = len(counts)-1
    digits = []
    while weight:
        if rank < counts[weight-1]:
            digits.append(0)
            weight -= 1
        else:
            rank -= counts[weight-1]
            digits.append(1)
            weight -= 2
    O.require(rank == 0, "Fibonacci word rank")
    return code.emit(digits)


@lru_cache(maxsize=None)
def golden_power(exponent):
    current = PHI if exponent >= 0 else code.P
    result = code.ONE
    exponent = abs(exponent)
    while exponent:
        if exponent % 2:
            result = code.mul(result,current)
        exponent //= 2
        if exponent:
            current = code.mul(current,current)
    return result


@lru_cache(maxsize=None)
def type_header(counts):
    target_left = None
    cumulative = Q(0)
    for rows in product(*(types(sum(x),len(x)) for x in counts)):
        word,amount = Q(1),1
        for row in rows:
            q,a = kt_type(row)
            word *= q
            amount *= a
        if rows == counts:
            target_left,word_q,arrangements = cumulative,word,amount
        cumulative += word*amount
    O.require(cumulative == 1 and target_left is not None, "normalized KT type header")
    return golden_interval(target_left,target_left+word_q*arrangements),word_q,arrangements


@lru_cache(maxsize=None)
def padding_slots(word_q,a,base_length):
    target = code.field(word_q**(-a))

    def sufficient(extra):
        exponent = a*(base_length-COMPENSATION)+extra
        return code.sign(code.sub(golden_power(exponent),target)) >= 0

    low,high = -1,a*(COMPENSATION+1)
    O.require(not sufficient(0) and sufficient(high), "bounded positive padding")
    while high-low > 1:
        mid = (low+high)//2
        if sufficient(mid):
            high = mid
        else:
            low = mid
    O.require(sufficient(high) and not sufficient(high-1), "exact average rounding")
    return high


def encode(block,dims):
    grouped = [[symbol for tag,symbol in block if tag == t] for t in (0,1)]
    counts = tuple(tuple(xs.count(i) for i in range(d)) for xs,d in zip(grouped,dims))
    header,word_q,arrangements = type_header(counts)
    _,_,v0,a0 = code.type_ranks(grouped[0],dims[0])
    _,_,v1,a1 = code.type_ranks(grouped[1],dims[1])
    O.require(a0*a1 == arrangements,"placement size")
    rank = v0*a1+v1
    body = fixed_weight_index(rank,arrangements)
    total_padding = padding_slots(word_q,arrangements,len(header)+len(body))
    c,r = divmod(total_padding,arrangements)
    tags = "".join(("0","1010")[tag] for tag,_ in block)
    return tags+header+body+"0"*(c+(rank<r))


def binomial_log(n,probability,shift):
    r,s = I.rational(probability),I.rational(1-probability)
    mass = I(1.)
    for _ in range(n):
        mass = mass*s
    lo,hi = [],[]
    for k in range(n+1):
        lo.append(float(mass.lo)); hi.append(float(mass.hi))
        if k < n:
            mass = mass*Q(n-k,k+1)*r/s
    probs = I(np.array(lo),np.array(hi))
    O.require(O.reduce_sum(probs).contains(1),"outward binomial normalization")
    xs = I(np.arange(n+1,dtype=float)+float(shift))
    return O.reduce_sum(probs*interval.ln(xs))


def derivative_example():
    tau = (Q(7,10),Q(3,10))
    p = ((Q(1,2),Q(1,3),Q(1,6)),(Q(3,5),Q(2,5)))
    dp = ((Q(1,4),Q(-1,8),Q(-1,8)),(Q(-1,7),Q(1,7)))
    ell = -O.logarithm((I(5.).sqrt()-1)/2)
    result,previous = [],None
    for m in (32,64,128,256,512):
        transverse = I(0.)
        tag_parts = []
        for t in (0,1):
            out = binomial_log(m-1,tau[t],Q(len(p[t]),2))
            for value,tangent in zip(p[t],dp[t]):
                term = O.logarithm(I.rational(value))-binomial_log(m-1,tau[t]*value,Q(1,2))
                transverse = transverse+I.rational(tau[t]*tangent)*term/ell
                out = out+I.rational(value)*term
            tag_parts.append(out/ell)
        O.require(transverse.lo > 0 or transverse.hi < 0,"nonzero illustrative transverse jet")
        relay = (tag_parts[1]-tag_parts[0])*m
        result.append({"block":m,
                       "transverse_jet":O.bounds(transverse),
                       "m_squared_transverse":O.bounds(transverse*m*m),
                       "m_times_parallel_adjustment":O.bounds(relay)})
        if previous is not None and m >= 128:
            ratio = previous/transverse
            O.require(ratio.lo > 3 and ratio.hi < 5,"quadratic derivative convergence fixture")
        previous = transverse
    return result


def main():
    for name,digest in PINS.items():
        O.require(hashlib.sha256((PILOT/name).read_bytes()).hexdigest()==digest,"pinned codec input")
    options = [(0,0),(0,1),(0,2),(1,0),(1,1)]
    words = {encode(z,(3,2)):z for z in product(options,repeat=4)}
    O.require(len(words)==5**4,"all archives recoverable")
    sorted_words = sorted(words)
    O.require(all(not b.startswith(a) for a,b in zip(sorted_words,sorted_words[1:])),
              "complete encoded words are prefix-free")
    print(json.dumps({
        "round":"B161",
        "exact_full_code_fixture_words":len(words),
        "rank_padding_unit":1,
        "common_per_block_padding_target":COMPENSATION,
        "rate_fixture":derivative_example(),
        "full_native_archive_composition_proven":False,
        "full_Einstein_Hessian_on_admitted_chart_proven":False,
        "GR_closed":False,
        "pinned_inputs":PINS,
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
