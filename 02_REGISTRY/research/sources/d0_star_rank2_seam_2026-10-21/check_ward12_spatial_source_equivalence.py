#!/usr/bin/env python3
"""EXACT original finite 42->12 source ZERO TEST on the declared
spatially homogeneous diagonal rank-two Cauchy family, using original
SO(1,3) local Lorentz Noether identity, star support and 6x6 minor.

NOT 12 solved zero equations, NOT a general 4D quotient/gauge inverse,
NOT an exact full42 finite Einstein root or compulsory Book03 price.
"""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as s
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PIN="a57f0e3e845290923c2ac88d39ba5c08af4f6fd6"
PATH="02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py"
sys.path.insert(0,str(HERE))
from check_star_rank2_seam import I,ETA,LORENTZ,star_density,matter_query,KAPPA

def pin_original():
    b=(ROOT/PATH).read_bytes()
    got=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert got==PIN,(got,PIN)

def exact_support():
    P=list(combinations(range(4),2))
    allowed=set()
    for r,t in P:
        u,v=[k for k in range(4) if k not in (r,t)]
        curv=[(0,t)] if r==0 else [(0,r),(0,t),(r,t)]
        for a,b in curv:
            complement=set(range(4))-{a,b}
            for A in range(4):
                if {A,v}==complement:allowed.add((A,u))
                if {u,A}==complement:allowed.add((A,v))
    expected={(i,i) for i in range(4)}|{(i,0) for i in (1,2,3)}
    assert allowed==expected
    allowed_link=[(i,j) for i in (1,2,3) for j in range(6)
                  if (i,j) not in {(1,5),(2,4),(3,3)}]
    targets=[(i,j) for i,j in allowed_link
             if (i,j) not in {(2,0),(3,0),(2,2)}]
    assert len(allowed_link)==15 and len(targets)==12
    return allowed,allowed_link,targets

def exact_six_by_six():
    x=s.symbols("X",positive=True)
    t=s.symbols("t",real=True)
    eta=s.diag(1,-1,-1,-1)
    gens=[]
    for i in (1,2,3):
        Z=s.zeros(4);Z[0,i]=Z[i,0]=1;gens.append(Z)
    for i,j in ((1,2),(1,3),(2,3)):
        Z=s.zeros(4);Z[i,j]=1;Z[j,i]=-1;gens.append(Z)
    # Rational SO^+(1,3) parameter t=tanh(h*k2/2), not fitted.
    c=(1+t*t)/(1-t*t)
    si=2*t/(1-t*t)
    def B(i):
        U=s.eye(4)
        U[0,0]=U[i,i]=c
        U[0,i]=U[i,0]=si
        return U
    U2,U3=B(2),B(3)
    pivots=[("e",1,0),("e",2,0),("e",3,0),
            ("link",2,0),("link",3,0),("link",2,2)]
    W=s.zeros(6,6)
    for i,Z in enumerate(gens):
        for j,(kind,a,b) in enumerate(pivots):
            if kind=="e":
                # diag original coframe e_t^0=X; only its temporal column
                W[i,j]=x*Z[a,0]
            else:
                D=Z-([None,None,U2,U3][a])*Z*([None,None,U2,U3][a]).inv()
                W[i,j]=s.factor(D[0,b+1])
    det=s.factor(W.det())
    assert s.simplify(det+x**3*si**3)==0,det
    assert det!=0
    return {"original_Noether_pivot":pivots,
            "exact_minor":"-X^3*sinh(h*k2)^3",
            "det_rational":str(det),
            "nonzero_conditions":"X>0; h>0; k2!=0"}

def cell(rng,h):
    # At t−1,t,t+1, arbitrary real ORIGINAL coframe and independent boost
    # profiles. Same spatial data at all sites of a slice.
    e=np.diag(rng.uniform(.68,1.5,size=4)).astype(complex)
    ks=rng.uniform(-.7,.7,size=3)
    U=np.asarray([I]+[expm(h*ks[j]*LORENTZ[j]) for j in range(3)],
                 dtype=complex)
    v=np.zeros((2,4),dtype=complex)
    v[0,0]=rng.uniform(.02,.15)
    v[1,1]=rng.uniform(.02,.15)
    return {"e":e,"u":U,"v":v}
def coefficient(D,index):
    if index<3:return D[0,index+1]
    ij=((1,2),(1,3),(2,3))[index-3]
    return D[ij]
def numerical_original_ward():
    allowed,alllinks,targets=exact_support()
    h=.11
    rng=np.random.default_rng(20261021)
    worst=0.;worst_forbidden=0.;worst_residual=0.
    for test in range(7):
        prev,cur,nxt=[cell(rng,h) for _ in range(3)]
        # FULL UNRESTRICTED original first derivative with all 16 and 24
        # independent true left-link generators; no symmetry-projected action.
        eco=np.zeros((4,4));elink=np.zeros((4,6))
        delta=1e-20
        for a in range(4):
            for b in range(4):
                old=cur["e"][a,b]
                cur["e"][a,b]=old+1j*delta
                eco[a,b]=(star_density(cur,nxt,h)+KAPPA*matter_query(cur)).imag/delta
                cur["e"][a,b]=old
        for axis in range(4):
            for j,Z in enumerate(LORENTZ):
                old=cur["u"][axis].copy()
                cur["u"][axis]=expm(1j*delta*Z)@old
                elink[axis,j]=(star_density(prev,cur,h)+
                               star_density(cur,nxt,h)).imag/delta
                cur["u"][axis]=old
        forbidden_e=max(abs(eco[a,b]) for a in range(4) for b in range(4)
                        if (a,b) not in allowed)
        forbidden_link=max(abs(elink[axis,j]) for axis in range(4)
                           for j in range(6)
                           if axis==0 or (axis,j) not in alllinks)
        worst_forbidden=max(worst_forbidden,float(forbidden_e),float(forbidden_link))
        for Z in LORENTZ:
            source=float(np.real(np.sum(eco*(Z@cur["e"]))))
            for axis in (1,2,3):
                D=Z-cur["u"][axis]@Z@np.linalg.inv(cur["u"][axis])
                coeffs=np.asarray([coefficient(D,j) for j in range(6)])
                source+=float(np.dot(elink[axis],coeffs).real)
            worst=max(worst,float(abs(source)))
        # Exact 12-target ZERO acceptance: given six Noether relations and
        # invertible pivot, if twelve targets vanish the other six must
        # vanish. This is a linear implication, NOT zero values in these
        # deliberately nonstationary numerical controls.
        full=np.array([elink[a,j] for a,j in targets],dtype=float)
        worst_residual=max(worst_residual,float(abs(full).max()))
    assert worst_forbidden<1e-10,worst_forbidden
    assert worst<1e-9,worst
    assert worst_residual>1e-4,"source target cannot be declared solved"
    return {"random_original_full4_tests":7,
            "max_forbidden_source_component":worst_forbidden,
            "max_exact_gauge_ward_residual":worst,
            "max_nonzero_chosen_12_source":worst_residual}

def main():
    pin_original()
    support,alllinks,targets=exact_support()
    exact=exact_six_by_six()
    actual=numerical_original_ward()
    print(json.dumps({
        "status":"PASS_SCOPED_NATIVE_42_TO_12_ZERO_TEST",
        "exact_original_coframe_allowed":[list(x) for x in sorted(support)],
        "original_link_15_allowed":alllinks,
        "twelve_source_acceptance_targets":targets,
        "Noether":exact,"controls":actual,
        "claim":"On the constructed exact 4-diagonal+2-scalar Cauchy branch, "
                "all 42 field Euler entries are zero IFF these 12 specified "
                "spatial-link entries are zero (given the exact support/Ward identities).",
        "scope":{"twelve_sources_already_zero":False,
                 "whole_slab_root_proved":False,
                 "native_arbitrary_spacetime_gauge_quotient":False,
                 "actual_Book03_selected":False,"GR_closed":False}},indent=2))
if __name__=="__main__":main()
