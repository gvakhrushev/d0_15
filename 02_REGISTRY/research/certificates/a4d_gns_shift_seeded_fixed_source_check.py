#!/usr/bin/env python3
"""Field-independent paired GNS shift seed: exact counts and bounded source.

This is a conditional mathematical controller / measured-history calculation.
It does NOT establish physical native active-wire admission, Book source
binding, real-gate finite synthesis, matter stress or physical GR.
"""
import json
import math
from fractions import Fraction

p = (math.sqrt(5)-1)/2
ell = math.log(1/p)
a0 = p*p
h = lambda x: -x*math.log(x)-(1-x)*math.log(1-x)
hp = lambda x: math.log((1-x)/x)
z = lambda x: 1 + 2*math.exp(h(x))
zp = lambda x: 2*math.exp(h(x))*hp(x)
sstar = (z(a0)-1)/z(a0)

def fib(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

checks = 0
source_cases = []
for N in range(1,8):
    a,b = fib(N+2),fib(N+1)
    u = a*p**(N+1)
    v = b*p**(N+2)
    assert abs(u+v-1) < 1e-10
    # Each retained seed shift s pairs with each RIGHT j exactly once.
    # This is an exact classical outcome identity on the full matched GNS.
    conditional_by_block = {}
    for typ,size in (("X",a),("Y",b)):
        outcomes={}
        for s in range(size):
            for j in range(size):
                i=(j+s)%size
                assert (i,j) not in outcomes
                outcomes[(i,j)] = (s,Fraction(1,size*size))
        assert len(outcomes)==size*size
        for j in range(size):
            assert sum((q for (i,jj),(s,q) in outcomes.items()
                        if jj==j),Fraction(0)) == Fraction(1,size)
        for (i,j),(s,q) in outcomes.items():
            assert s==(i-j)%size
        conditional_by_block[typ]=outcomes
        checks+=size*size

    # On the common complete pair pointer, all work shift labels become
    # functions of the pair, so H(shift|LEFT,RIGHT)=0.
    labels=[]
    for typ,size,mass in (("X",a,u),("Y",b,v)):
        for (i,j),(s,q) in conditional_by_block[typ].items():
            # Geometric f depends on LEFT, never on RIGHT.
            f = ((3*i+(0 if typ=="X" else 2))%9-4)/4
            labels.append((typ,i,j,s,mass*float(q),f))
    assert len(labels)==a*a+b*b
    assert abs(sum(row[4] for row in labels)-1)<1e-10
    center_gap = abs(u-a*a/(a*a+b*b))

    # For varying complete AF effects, the seed and conditional success
    # state are FIXED at their vacuum values. Compare its true first source
    # against fully optimized log-sum-exp on the same entire pair partition.
    for c in (0.005, 0.01):
        ai=[a0+c*row[5] for row in labels]
        assert min(ai)>0 and max(ai)<0.5
        weight=[row[4] for row in labels]
        f=[row[5] for row in labels]
        D=sum(z(x) for x in ai)
        Dgamma_free=sum(c*zp(x)*y for x,y in zip(ai,f))/(ell*D)
        Dseed=sstar*c*sum(q*hp(x)*y for q,x,y in zip(weight,ai,f))/ell
        normalized_error=abs(Dseed-Dgamma_free)/c
        # A conservative numerical fixture guard, NOT a substitute for
        # the analytic uniform-N Lipschitz error in the owner.
        assert normalized_error < center_gap+c
        source_cases.append({
            "N":N, "c":c,
            "right_center_gap":center_gap,
            "source_error_divided_by_c":normalized_error,
        })
print(json.dumps({
    "terminal":"PASS: REAL cyclic shift GNS seeded paired readout and source",
    "levels":"N=1..7",
    "exact_pair_combinatorial_checks":checks,
    "right_marginal":"UNCHANGED for every conditional LEFT permutation",
    "work_outcome":"DETERMINISTIC_FROM_COMPLETE_PAIR",
    "source_cases":source_cases
},indent=2,sort_keys=True))
