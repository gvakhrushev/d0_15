#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=240
"""Exact finite-field torsion census for the curved z=1 full joint Bloch symbol.

Consumes the literal Laurent stencil and Gaussian-prime reduction from the
mu4 owner. Exhaustively checks mu_8^4 and mu_12^4. Modular full column rank
certifies characteristic-zero full rank at each regular torsion character.
The only modular rank drops are the four quarter-wave diagonal copies already
checked exactly over Q(i) by the mu4 owner.

This is a torsion census, not an all-unit-torus theorem.
"""
from __future__ import annotations
from itertools import product
import json
from pathlib import Path
import numpy as np
import sympy as sp
import a4d_y_curved_joint_mu4_locus_check as M

HERE=Path(__file__).resolve().parent
OUT=HERE/"a4d_y_curved_joint_torsion_census_results.json"

def ck(n,c):
    if not c: raise AssertionError(n)
    print("PASS_"+n,flush=True)

P=M.P
g=int(sp.primitive_root(P))

def roots(n):
    ck("ORDER_%d_DIVIDES_P_MINUS_1"%n,(P-1)%n==0)
    w=pow(g,(P-1)//n,P)
    return [pow(w,k,P) for k in range(n)]

def census(n):
    R=roots(n)
    powtab={}
    for d in M.SUPPORT:
        tab=[[1]*n for _ in range(4)]
        for r,e in enumerate(d):
            if e==1: tab[r]=R[:]
            elif e==-1: tab[r]=[pow(x,P-2,P) for x in R]
        powtab[d]=tab
    candidates=[]
    for ids in product(range(n),repeat=4):
        A=np.zeros((136,96),dtype=np.int64)
        for d,Td in M.TMOD.items():
            c=1
            for r in range(4): c=c*powtab[d][r][ids[r]]%P
            A=(A+c*Td)%P
        rr=M.rank_mod(A)
        if rr<96: candidates.append((ids,rr))
    q=n//4
    expected=[((j*q,)*4,95) for j in range(4)]
    ck("MU_%d_ONLY_QUARTER_FOLDED"%n,candidates==expected)
    return candidates

c8=census(8)
c12=census(12)
result={
 "schema":"a4d-y-curved-joint-torsion-census-v1",
 "terminal":"A4D-Y-CURVED-JOINT-MU8-MU12-CENSUS-CERTIFIED",
 "background":"z=1 exact Y vacuum; full 136x96 joint symbol",
 "modulus":P,
 "orders":{
   "8":{"character_count":8**4,"rank95_count":4,"rank96_count":8**4-4,
        "singular_ids":[list(x[0]) for x in c8]},
   "12":{"character_count":12**4,"rank95_count":4,"rank96_count":12**4-4,
         "singular_ids":[list(x[0]) for x in c12]}
 },
 "conclusion":"for mu_8^4 and mu_12^4 the only joint rank drops are the four quarter-wave diagonal characters already owned exactly by the mu4 certificate",
 "scope_fence":[
   "finite exact torsion censuses only",
   "does not exclude irrational unit-torus zeros or torsion points of untested order",
   "does not prove a uniform transverse singular-value gap",
   "does not close nonlinear response decoupling"
 ]
}
if "--write" in __import__("sys").argv:
    OUT.write_text(json.dumps(result,indent=2)+"\n"); print("WROTE",OUT)
elif OUT.exists():
    ck("RESULTS_MATCH_PINNED_JSON",json.loads(OUT.read_text())==result)
print("TERMINAL A4D-Y-CURVED-JOINT-MU8-MU12-CENSUS-CERTIFIED")
