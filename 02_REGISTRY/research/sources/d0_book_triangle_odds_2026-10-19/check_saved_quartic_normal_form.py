#!/usr/bin/env python3
"""Exact sparse-support comparison with the pinned #334 1008-rational quartic vector.
This checks literal same-gauge identity, NOT gauge-equivalence or 840 Euler rows.
"""
import json
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOL=HERE.parent/"d0_two_null_crossing_2026-10-19"/"quartic_full_spatial_jet_solution.json"
record=json.loads(SOL.read_text())
assert record["amplitude"]==[2,2]
sol=list(map(Q,record["solution"]))
assert len(sol)==1008
def monomials(degree):
    return [(i,d-i) for d in range(degree+1) for i in range(d,-1,-1)]
lmono=monomials(6);cmono=monomials(5)
assert len(lmono)==28 and len(cmono)==21
assert len([v for v in sol[:672] if v])==118
assert len([v for v in sol[672:] if v])==20
def coframe(row,col):
    start=672+(4*row+col)*len(cmono)
    return {m:v for m,v in zip(cmono,sol[start:start+len(cmono)]) if v}
e00=coframe(0,0);e22=coframe(2,2);e33=coframe(3,3)
assert e00 == {
    (2,0):Q(3,128),(1,1):Q(3,128),(0,2):Q(3,128),
    (3,0):Q(3,256),(2,1):Q(3,256),(1,2):Q(3,256),(0,3):Q(3,256)}
assert e33=={}
assert e22 == {
    (0,2):Q(-7,256),(1,2):Q(-9,128),(0,3):Q(-1,128),
    (2,2):Q(3,128),(0,4):Q(1,256)}
# Continuum sigma4 and chi4 in their stated untransformed coordinates
sigma={(4,0):Q(-1,128),(2,2):Q(-1,64),(0,4):Q(-1,128)}
chi={(4,0):Q(3,1024),(2,2):Q(3,512),(0,4):Q(3,1024)}
assert e00!=sigma and e22!=chi and e33!=chi
print("PASS: pinned 1008-vector has 118 link + 20 coframe nonzero coefficients")
print("PASS: literal quartic sigma/chi representatives differ from stored finite vector")
print("SCOPED: no gauge equivalence, kernel-range or physical GR conclusion")
