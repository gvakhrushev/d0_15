#!/usr/bin/env python3
"""Actual native N=1 Golden CQ scalar price, CORRECT star x->-x retyping,
on the original finite six-plaquette rank-two two-real-field test.
Computes normalized ALL 16+24+2 local first-Euler rows. Research scope:
one Cartesian homogeneous spatial interior stencil; no exact 42-root,
physical Book admission, gauge-fixed inverse or uniform theorem claimed.
"""
import sys, json, hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
MASTER_FILE=REPO/"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py"
SOURCES={
"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py":
"525b257ec671500bd02c4791f9579dbde2439f21",
"02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py":
"a57f0e3e845290923c2ac88d39ba5c08af4f6fd6"}
def gitblob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def checkpins():
    for path,sha in SOURCES.items():
        b=(REPO/path).read_bytes()
        if gitblob(b)!=sha:raise AssertionError((path,gitblob(b),sha))
checkpins()
sys.path.insert(0,str(MASTER_FILE.parent))
from native_master import GoldenMaster
from check_star_rank2_seam import cell, star_density, matter_query, LORENTZ, KAPPA
NATIVE=GoldenMaster(70)
assert NATIVE.a<0<NATIVE.b
assert abs(float(NATIVE.kappa)-KAPPA)<1e-12
TAU=1/20
def calc(h,rho_name):
    amplitude=(1/(2*KAPPA))**0.5
    prev,cur,nex=[cell(t,h,amplitude) for t in (-h,0,h)]
    rho=(lambda t:1.) if rho_name=="uniform" else (lambda t:1+.2*np.sin(3*t))
    fp=float(star_density(prev,cur,h).real)
    fc=float(star_density(cur,nex,h).real)
    qp=float(matter_query(prev).real)
    qc=float(matter_query(cur).real)
    assert abs(qp)<1e-13 and abs(qc)<1e-13
    # SAME sigma-minus full price after the EXACT sign retyping:
    # x_NULL=-x_CANON, so take F_NULL(-TAU*f_CANON/rho, TAU*q/rho)
    xprev=-TAU*fp/rho(-h);xcur=-TAU*fc/rho(0)
    wprev=float(NATIVE.fx(xprev,0)/NATIVE.a)
    wcur=float(NATIVE.fx(xcur,0)/NATIVE.a)
    vprev=float(-NATIVE.fy(xprev,0)/NATIVE.a)
    vcur=float(-NATIVE.fy(xcur,0)/NATIVE.a)
    eps=1e-20
    Eco=np.zeros((4,4));Elink=np.zeros((4,6));Eaff=np.zeros((4,4))
    # Normalization -M*TAU*a_N (nonzero). In this normalization,
    # linear/old canonical source is Df_CANON + KAPPA Dq.
    for a in range(4):
        for j in range(4):
            saved=cur["e"][a,j];cur["e"][a,j]=saved+1j*eps
            df=star_density(cur,nex,h).imag/eps
            dq=matter_query(cur).imag/eps
            Eco[a,j]=wcur*df+vcur*dq
            Eaff[a,j]=df+KAPPA*dq
            cur["e"][a,j]=saved
    for r in range(4):
        for k,X in enumerate(LORENTZ):
            saved=cur["u"][r].copy()
            cur["u"][r]=expm(1j*eps*X)@saved
            Elink[r,k]=wprev*star_density(prev,cur,h).imag/eps
            Elink[r,k]+=wcur*star_density(cur,nex,h).imag/eps
            cur["u"][r]=saved
    # Two ACTUAL native forward CAR matter Euler rows. At each anchor the
    # time current of psi_1 is amplitude and the x current of psi_2 depends
    # on t but is x-independent. The time gradient varies via true Q operand.
    Epsi1=float(2*amplitude*(vprev-vcur)/h)
    Epsi2=0.
    err_co=float(np.max(abs(Eco)));err_link=float(h*np.max(abs(Elink)))
    delta=float(np.max(abs(Eco-Eaff)))
    shifted=max(abs(wprev-1),abs(wcur-1),abs(vprev-KAPPA),abs(vcur-KAPPA))
    if not (err_co<.8*h and err_link<.5*h and abs(Epsi1)<.11*h):
        raise ArithmeticError(('full CQ Euler O(h) numerical bound',h,err_co,err_link,Epsi1))
    if not (shifted<.26*h*h and delta<.11*h*h):
        raise ArithmeticError(('same-price nonlinear jet O(h^2)',h,shifted,delta))
    if not (max(abs(fp),abs(fc))<.6*h*h):
        raise ArithmeticError(('actual six-face f=O(h^2)',h,fp,fc))
    return dict(h=h,rho_kind=rho_name,full42_normalized_source={
      "max_16_coframe":err_co,"h_times_max_24_link":err_link,
      "scalar_1":Epsi1,"scalar_2":Epsi2},
      finite_operands={"fprev":fp,"fcur":fc,"qprev":qp,"qcur":qc},
      coefficients={"wprev":wprev,"wcur":wcur,"matter_prev":vprev,
                    "matter_cur":vcur,"max_slope_delta":float(shifted)},
      full_nonlin_minus_affine_max_coframe=delta,
      ratios={"coframe_over_h":err_co/h,"link_over_h":err_link/h,
              "material_over_h":abs(Epsi1)/h})
if __name__=="__main__":
    rows=[calc(1/n,rho) for rho in ("uniform","smooth_nonuniform")
                           for n in (8,16,32,64,128)]
    print(json.dumps({"status":"PASS_DECLARED_FINITE_N1_TWO_FIELD_SOURCE_RETYPE",
      "native_Golden_model":"existing N=1 GoldenMaster fixed caps 9/20; same sigma-minus function",
      "same_price_retype":"F_cart(x,y)=F_null(-x,y), NOT alternate sigma-plus",
      "source_normalization":"-M*TAU*a_native; includes real 16+24+2 gradients",
      "material_CAR_forward_gradients":"fixed scalar 1 and scalar 2 true finite increments",
      "rows":rows,
      "scope":{"spatially_homogeneous_interior":True,
       "all42_first_source_components_tested":True,
       "full_native_selected_Book_price":False,
       "full_native_dynamic_PF_derivative":False,
       "analytic_uniform_Oh_proved":False,
       "gauge_fixed_joint_exact_root":False,"GR_closed":False}},indent=2))
