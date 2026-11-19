#!/usr/bin/env python3
"""Exact native binary test-algebra future quotient/rank for D0 FutureExecution.

Original CX-accessible pair-XOR future tests have a one-global-complement
gauge kernel (n-1 essential memory bits); adding ONE actual absolute source
bit test restores full n bits. Nonlinear pair-AND tests instead separate
ALL states after at most one charged flip. No external catalogue or third
history-comparison primitive. Scope: this declared finite Boolean
subcarrier, NOT original CAR16/full128 complete Book action.
"""
from __future__ import annotations
from itertools import combinations
from math import comb
import json
COUNT=0
def check(ok, reason):
    global COUNT
    COUNT+=1
    if not bool(ok):
        raise ArithmeticError(reason)

def bits(n):
    return range(1<<n)

def rank2(rows):
    pivots={}
    for row in rows:
        q=row
        while q:
            h=q.bit_length()-1
            if h in pivots:
                q^=pivots[h]
            else:
                pivots[h]=q
                break
    return len(pivots)

def observations(x,rows):
    return tuple((x&r).bit_count()%2 for r in rows)

cases=[]
for n in range(2,10):
    pairXOR=[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
    pairAND=[(i,j) for i,j in combinations(range(n),2)]
    check(rank2(pairXOR)==n-1,
          "all nchoose2 pair XOR readouts yield exactly rank n-1 over F2")
    with_absolute=pairXOR+[1]
    check(rank2(with_absolute)==n,
          "one original absolute bit detector fixes the one global complement")
    pairXOR_classes={observations(x,pairXOR) for x in bits(n)}
    check(len(pairXOR_classes)==2**(n-1),
          "complete future pair XOR quotient has precisely 2^(n-1) classes")
    full_classes={observations(x,with_absolute) for x in bits(n)}
    check(len(full_classes)==2**n,
          "one added native available absolute-bit test retains all distinctions")
    if n<=6:
        allmask=(1<<n)-1
        for x in bits(n):
            for y in bits(n):
                equivalence=(observations(x,pairXOR)==observations(y,pairXOR))
                check(equivalence==(x==y or x^y==allmask),
                      "pair native XOR observational kernel exactly global complement")
                for i in range(n):
                    xa=x^(1<<i);ya=y^(1<<i)
                    check((observations(xa,pairXOR)==observations(ya,pairXOR))
                          ==equivalence,
                          "ALL charged common future bitflip actions preserve XOR gauge")
    # Adjacent/current AND observations may be coarse; arbitrary future
    # single-bit flips completely separate the original input states.
    and_obs={tuple(((x>>i)&1)&((x>>j)&1) for i,j in pairAND)
             for x in bits(n)}
    check(len(and_obs)==2**n-n,
          "exact current nonlinear pair AND quotient 2^n-n")
    check(n==2 or 2**(n-1)<2**n-n,
          "for n>=3 nonlinear pair tests already require n binary memory bits")
    for x in bits(n):
        for y in bits(n):
            if x==y:continue
            i=next(i for i in range(n) if ((x>>i)&1)!=((y>>i)&1))
            xx,yy=(x,y) if ((x>>i)&1) else (y,x)
            j=(i+1)%n
            if not ((xx>>j)&1):
                xx^=1<<j
                yy^=1<<j
            check(((xx>>i)&1)&((xx>>j)&1)==1
                  and ((yy>>i)&1)&((yy>>j)&1)==0,
                  "sharp <=1 future transition exposes any genuinely different bit state")
    cases.append({"bits":n,"native_pair_XOR_rows":comb(n,2),
                  "native_future_XOR_rank":rank2(pairXOR),
                  "native_future_XOR_classes":len(pairXOR_classes),
                  "one_absolute_test_rank":rank2(with_absolute),
                  "nonlinear_pair_AND_current_classes":len(and_obs),
                  "nonlinear_pair_AND_complete_future_classes":2**n,
                  "max_shortest_AND_future_flip":1})

# General exact F2 future profile for ANY binary linear test frame,
# under common internal translation actions: same kernel for every w.
n=5
for rows in ([0], [1,2], [3,5,11], [(1<<n)-1],
             [1<<i for i in range(n)],[]):
    r=rank2(rows)
    outputs={observations(x,rows) for x in bits(n)}
    check(len(outputs)==2**r,
          "general native binary future quotient equals GF2 row rank")
    for x in bits(n):
        for y in bits(n):
            if observations(x,rows)==observations(y,rows):
                for word in (0,1,3,7,11,31):
                    check(observations(x^word,rows)==observations(y^word,rows),
                          "whole future profile preserved by actual common transitions")

print(json.dumps({
 "status":"PASS_EXACT_BINARY_FUTURE_TEST_RANK_AND_GAUGE_MEMORY",
 "checks":COUNT,
 "cases":cases,
 "general_G_F2_future_profile":"kernel of admitted test matrix L",
 "native_pair_XOR_gauge_dim":1,
 "true_memory_bits_for_XOR":"n-1",
 "true_memory_bits_for_AND_plus_flips":"n",
 "cost_sensitive_Book_future_equivalence_proved":False,
 "physical_original_CAR16_full_action_selected":False,
 "GR_closed":False
},indent=2,sort_keys=True))
