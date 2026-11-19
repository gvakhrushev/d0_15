#!/usr/bin/env python3
"""Exact algebraic three-round original CAR16 channel mixing certificate.

Imports the exact modular CAR16 builder next to this file. There is no
floating matrix rank or uncharged experimental step. Mathematical result
for the pinned original 128-outcome process, not physical GR selection.
"""
import hashlib
import json
import numpy as np
from check_future_even_algebra_modprime import (
    SPLIT_PRIMES, original_kraus_mod, check
)

def full_three_round_span(d):
    m=d["m"]
    op=d["K"]
    active=d["nonzero"]
    prev=[(d["I"].copy(),())]
    counts=[]
    for depth in (1,2,3):
        pivot=[]
        echelon=[]
        selected=[]
        for X,path in prev:
            for label in active:
                mat=(op[label]@X)%m
                v=mat.reshape(-1).copy()
                for j,row in zip(pivot,echelon):
                    if v[j]:
                        v=(v-v[j]*row)%m
                idx=np.flatnonzero(v)
                if len(idx)==0:
                    continue
                j=int(idx[0])
                echelon.append(
                    (v*pow(int(v[j]),-1,m))%m)
                pivot.append(j)
                selected.append((mat,path+(label,)))
                if len(selected)==256:
                    break
            if len(selected)==256:
                break
        counts.append(len(selected))
        prev=selected
    check(counts==[18,144,256],
          "exact original Kraus spans by precise length 1,2,3")
    check(all(len(path)==3 for _mat,path in prev),
          "all original selected matrix words have length exactly three")
    return counts,[path for _mat,path in prev]

def main():
    results={}
    for entry in SPLIT_PRIMES:
        d=original_kraus_mod(entry)
        counts,paths=full_three_round_span(d)
        results[str(entry[0])]=counts
        if entry[0]==1009:
            digest=hashlib.sha256(
                json.dumps(paths,separators=(",",":")).encode()
            ).hexdigest()
            check(
                digest=="ab70fb7bbdf3f1deabf26b5b919051156e199029e9206ffce83681b49d2af750",
                "frozen exact 256 original three-round matrix proof witness")
    print(json.dumps({
        "status":"EXACT_ORIGINAL_KRAUS_THREE_ROUND_FULL_MATRIX_SPAN",
        "field_dimension":16,
        "operator_dimension":256,
        "modular_ranks":results,
        "actual_full128_stationary_preparation_selected_by_channel":True,
        "complete_Book03_physical_GR_selected":False
    },sort_keys=True,indent=2))

if __name__=="__main__":
    main()
