#!/usr/bin/env python3
"""Exact original G2/STAR spatial-rotation Euler obstruction.

Inside the spatially homogeneous diagonal coframe, pure spatial-boost
Lorentz-link ansatz, U_x,J12 has a STRICT nonzero first Euler source when
the transverse boost is nonzero on the small Golden chart. This is a
finite-plaquette, original-ambient variation, not a restricted-action
variation. It is NOT a no-go for the full D0 geometric field space.
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import sympy as sp
from scipy.linalg import expm

INPUT="02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py"
PIN="a57f0e3e845290923c2ac88d39ba5c08af4f6fd6"

def owner_blob(repo):
    data=(repo/INPUT).read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    assert actual==PIN,("original_G2STAR_owner_changed",actual,PIN)

def exact_no_go():
    ca,sa,cb,sb=sp.symbols("ca sa cb sb",real=True)
    h,k1,k2,X,R=sp.symbols("h k1 k2 X R",real=True,positive=True)
    U=sp.Matrix([[ca,sa,0],[sa,ca,0],[0,0,1]])
    V=sp.Matrix([[cb,0,sb],[0,1,0],[sb,0,cb]])
    Ui=sp.Matrix([[ca,-sa,0],[-sa,ca,0],[0,0,1]])
    Vi=sp.Matrix([[cb,0,-sb],[0,1,0],[-sb,0,cb]])
    J=sp.Matrix([[0,0,0],[0,0,1],[0,-1,0]])
    P=U*V*Ui*Vi
    Pin=V*U*Vi*Ui
    # A single native U_x left-link J12 derivative affects BOTH spatial
    # xy faces: first U_x factor based at z and inverse at z-y.
    dP=J*P-U*V*Ui*J*Vi
    dR=(dP+Pin*dP*Pin)/2 # true odd curvature (P-P^-1)/2
    gb=sp.groebner([sa**2-ca**2+1,sb**2-cb**2+1],
                   sa,sb,ca,cb,order="lex",domain=sp.QQ)
    rem=sp.factor(gb.reduce(sp.expand(dR[1,2]))[1])
    factor=ca*(cb-1)*(ca*(cb-1)-(cb+1))/2
    assert sp.factor(rem-factor)==0
    assert sp.factor(rem.subs({ca:1,sa:0})-(1-cb))==0
    E=X*R*factor.subs({ca:sp.cosh(h*k1),cb:sp.cosh(h*k2)})/h**2
    limit=sp.simplify(sp.limit(E,h,0,dir="+"))
    assert sp.simplify(limit+X*R*k2**2/2)==0
    # Analytic sign proof: cosh1<8/5. Hence for |a|,|b|<=1,
    # cosh(a)(cosh(b)-1)<(8/5)(3/5)=24/25<2<=cosh(b)+1.
    assert float(sp.cosh(1))<8/5
    assert sp.Rational(24,25)<2
    return {
       "full_based_face_J12_odd_curvature_jet":str(factor),
       "original_ambient_link_Euler":
        "X*R/(2*h^2)*cosh(h*k1)*(cosh(h*k2)-1)*"
        "[cosh(h*k1)*(cosh(h*k2)-1)-(cosh(h*k2)+1)]",
       "strict_negative_chart":
        "X,R,h>0; |h*k1|<=1; 0<|h*k2|<=1",
       "physical_spin_rescaled_hE_tends_zero":True,
       "RAW_left_link_Euler_limit":"-X*R*k2^2/2 != 0"}

def source_original_4x4():
    from check_star_rank2_seam import star_density, LORENTZ, I
    rng=np.random.default_rng(1948)
    errors=[]
    examples=[]
    for trial in range(15):
        h=float(rng.uniform(.02,.09))
        ks=rng.uniform(-.8,.8,3)
        X=float(rng.uniform(.6,1.4))
        R=float(rng.uniform(.6,1.4))
        e=np.diag([X,1/X,R,R]).astype(complex)
        def make_node(kvec):
            UU=np.asarray([I]+[
                expm(h*kvec[j]*LORENTZ[j]) for j in range(3)
            ],dtype=complex)
            return {"e":e.copy(),"u":UU,
                    "v":np.zeros((2,4),dtype=complex)}
        prev=make_node(rng.uniform(-.6,.7,3))
        cur=make_node(ks)
        nex=make_node(rng.uniform(-.6,.7,3))
        eps=1e-20
        old=cur["u"][1].copy()
        cur["u"][1]=expm(1j*eps*LORENTZ[3])@old
        measured=(star_density(prev,cur,h)+star_density(cur,nex,h)).imag/eps
        cur["u"][1]=old
        ca=np.cosh(h*ks[0]);cb=np.cosh(h*ks[1])
        predicted=X*R/(2*h*h)*ca*(cb-1)*(ca*(cb-1)-(cb+1))
        error=abs(measured-predicted)
        errors.append(error)
        assert error<2e-10,(trial,measured,predicted,error)
        if trial<2:
            examples.append({"h":h,"X":X,"R":R,"k":ks.tolist(),
                             "native":measured,"exact_expression":predicted})
    return {"original_full4_matrix_cases":15,
            "max_abs_error":max(errors),"examples":examples}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path)
    opts=parser.parse_args()
    if opts.repo: owner_blob(opts.repo)
    result={
     "status":"PASS_ORIGINAL_PUREBOOST_J12_FINITE_NO_GO",
     "exact":exact_no_go(),
     "native_full4":source_original_4x4(),
     "scope":{
        "same_native_n1_CQ_at_f_Q_zero":True,
        "obstruction_is_within_diagonal_pure_boost_homogeneous_sector":True,
        "remaining_field_space_may_resolve_it":True,
        "no_claim_of_full42_exact_root":True,
        "compulsory_original_Book03_selected":False,
        "GR_closed":False}}
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
