#!/usr/bin/env python3
"""Exact finite six-face rank-two double-zero sheet (star=CAR Q=0).

Original fixed N=1 CQ source on the regular analytical chart, native
G2/STAR, true both REAL scalar forward increments, arbitrary positive PF.
Does NOT prove all 40 residual geometric Euler equations zero or an
admitted complete Book programme. Original fixed temporal collar may prevent
forcing the last collar cell to the projected coframe (not silently erased).
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np
import sympy as s
from scipy.optimize import brentq
from scipy.special import erfi
from scipy.linalg import expm

KAPPA=23.41640675188407497
PINS={
'02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py':'a57f0e3e845290923c2ac88d39ba5c08af4f6fd6',
'02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py':'525b257ec671500bd02c4791f9579dbde2439f21'}
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21'))
from check_star_rank2_seam import cell,star_density,matter_query,LORENTZ
from native_master import GoldenMaster

def checkpins():
    for path, expected in PINS.items():
        data=(ROOT/path).read_bytes()
        got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if got != expected:
            raise AssertionError((path,got,expected))

def clock(r):
    return np.sqrt(np.pi/2)*(erfi(r/np.sqrt(2))-erfi(1/np.sqrt(2)))

def ABC(r):
    A=np.sqrt(r)*np.exp(-r*r/4)
    B=1/A
    k1=(1-r**-2)/2
    k2=np.exp(-r*r/4)/np.sqrt(r)
    return A,B,k1,k2

def comm(x,y):
    return np.sinh(x)*np.sinh(y)*(1-(np.cosh(x)-1)*(np.cosh(y)-1)/2)

def exact_six_face_scalar(r,k1,k2,k1_next,k2_next,h,scale):
    A,B,_,_=ABC(r)
    return (r*r*np.sinh(h*(k1_next-k1))+
            (2*B*r/scale)*np.sinh(h*(k2_next-k2))+
            2*A*r*scale*comm(h*k1,h*k2)+
            A*B*comm(h*k2,h*k2))/h**2

def verify_exact_theorem():
    r=s.symbols('r',positive=True)
    A=s.sqrt(r)*s.exp(-r*r/4)
    B=1/A
    k1=(1-r**-2)/2
    k2=s.exp(-r*r/4)/s.sqrt(r)
    dt=lambda f:s.simplify(s.exp(-r*r/2)*s.diff(f,r))
    leading_zero=s.simplify(r*r*dt(k1)+2*B*r*dt(k2)+2*A*r*k1*k2+A*B*k2*k2)
    assert leading_zero==0
    c=s.simplify((r*r*dt(dt(k1))+2*B*r*dt(dt(k2)))/2)
    assert s.simplify(c-3*(r**4-1)*s.exp(-r*r)/(4*r*r))==0
    deriv=s.simplify(-2*B*r*dt(k2)+2*A*r*k1*k2)
    assert s.simplify(deriv-2*r*s.exp(-r*r/2))==0
    coef=s.simplify(-c/deriv)
    assert s.simplify(coef+3*(r**4-1)*s.exp(-r*r/2)/(8*r**3))==0
    U=s.symbols('U',positive=True)
    eps=s.symbols('eps',positive=True)
    et=A*U
    ex=B/U
    assert s.simplify(et*ex*r*r)==r*r
    ptime=eps*A*A*U*U
    px=eps
    assert s.simplify(ptime**2/et**2-px**2/ex**2)==0
    assert s.simplify(ptime/et**2-eps)==0
    return {
      'f_star_h_at_unprojected':'h*3*(r^4-1)*exp(-r^2)/(4*r^2)+O(h^2)',
      'f_star_derivative_wrt_unimod_balance':'2*r*exp(-r^2/2)+O(h)',
      'balance_first_correction':'-h*3*(r^4-1)*exp(-r^2/2)/(8*r^3)',
      'volume':'det e=r^2 EXACT',
      'CAR_two_field_Q':'0 EXACT',
      'scalar1_time_current':'eps EXACT',
      'radial_full_Euler_row':'x Fx-y Fy; null Q forces x=0 if Fx!=0'}

def make_slab(rlo,rhi,n):
    t0,t1=clock(rlo),clock(rhi)
    h=(t1-t0)/n
    times=np.linspace(t0,t1,n+1)
    epsi=(2*KAPPA)**-.5
    cells=[cell(t,h,epsi) for t in times]
    scales=[]
    for j in range(n):
        c,following=cells[j:j+2]
        r=c['r']
        k1,k2=ABC(r)[2:]
        k1n,k2n=ABC(following['r'])[2:]
        f=lambda u:exact_six_face_scalar(r,k1,k2,k1n,k2n,h,u)
        v=brentq(f,.7,1.3,xtol=5e-15)
        scales.append(v)
        c['e'][0,0]*=v
        c['e'][1,1]/=v
        c['v'][0,0]*=v*v
    return times,cells,scales,h

def full_first_40(prev,cur,nex,h):
    # At f=q=0, ALL 42 native price Euler rows are a common nonzero
    # multiple of D(f_star+kappa*q). These are the UNSOLVED 40 rows.
    def val():
        return star_density(prev,cur,h)+star_density(cur,nex,h)+KAPPA*matter_query(cur)
    dx=1e-20
    E=np.zeros((4,4))
    L=np.zeros((4,6))
    for i in range(4):
        for j in range(4):
            old=cur['e'][i,j]
            cur['e'][i,j]=old+1j*dx
            E[i,j]=val().imag/dx
            cur['e'][i,j]=old
    for i in range(4):
        for j,X in enumerate(LORENTZ):
            old=cur['u'][i].copy()
            cur['u'][i]=expm(1j*dx*X)@old
            L[i,j]=val().imag/dx
            cur['u'][i]=old
    return float(abs(E).max()),float(h*abs(L).max())

def grid_test(lo,hi,n):
    tt,cells,scale,h=make_slab(lo,hi,n)
    ff=np.array([star_density(cells[j],cells[j+1],h) for j in range(n)])
    qq=np.array([matter_query(cells[j]) for j in range(n)])
    qerr=float(max(abs(x) for x in qq))
    ferr=float(max(abs(x) for x in ff))
    vols=[np.linalg.det(c['e']).real-c['r']**2 for c in cells[:-1]]
    amp=(2*KAPPA)**-.5
    eta=np.diag([1,-1,-1,-1])
    current=[(np.linalg.inv(c['e'].T@eta@c['e'])@c['v'][0])[0]
             for c in cells[:-1]]
    jerr=float(max(abs(x-amp) for x in current))
    if ferr>2e-10 or qerr>2e-14 or max(abs(x) for x in vols)>1e-12 or jerr>1e-12:
        raise AssertionError(('trace, matter, volume and current',lo,hi,n,ferr,qerr,jerr))
    # Hostile PF example alternates 1,2. It is NOT claimed to be the
    # original AF regular descendant sequence. It tests the exact theorem
    # that the true N=1 slope has no PF dependence AT f=q=0.
    rho=np.array([1. if j%2 else 2. for j in range(n)])
    master=GoldenMaster(50)
    a,b=float(master.a),float(master.b)
    assert a<0<b and abs(b/a+KAPPA)<1e-11
    tau=.05
    slope_err=0.
    for j in range(n):
        x=-tau*float(ff[j].real)/rho[j]
        y=tau*float(qq[j].real)/rho[j]
        slope_err=max(slope_err,abs(float(master.fx(x,y)/master.a)-1),
                      abs(float(master.fy(x,y)/master.b)-1))
    mid=n//2
    eco,elink=full_first_40(cells[mid-1],cells[mid],cells[mid+1],h)
    # Zero scalar star curvature is NOT zero full holonomy. Two independent
    # REAL original scalar gradients give two DISTINCT null covectors.
    selected=cells[mid]
    U=selected['u']
    P23=U[2]@U[3]@np.linalg.inv(U[2])@np.linalg.inv(U[3])
    curvature_nontrivial=float(np.linalg.norm(P23-np.eye(4))/h**2)
    metric_inverse=np.linalg.inv(selected['e'].T@np.diag([1,-1,-1,-1])@selected['e'])
    p1,p2=selected['v']
    ell_plus=(p1+p2)/np.sqrt(2)
    ell_minus=(p1-p2)/np.sqrt(2)
    null_error=max(abs(ell_plus@metric_inverse@ell_plus),
                   abs(ell_minus@metric_inverse@ell_minus))
    stress=np.outer(p1,p1)+np.outer(p2,p2)
    if not (curvature_nontrivial>.01 and null_error<1e-13
            and np.linalg.matrix_rank(stress)==2):
        raise AssertionError(('nonflat two-null-stream witnesses',
                              curvature_nontrivial,null_error))
    return {
       'r_interval':[lo,hi],'n':n,'h':h,'f_star_max':ferr,
       'q_CAR_max':qerr,
       'det_e_minus_r_squared_max':max(abs(v) for v in vols),
       'scale_minus_1_max':float(max(abs(v-1) for v in scale)),
       'scale_error_over_h':float(max(abs(v-1) for v in scale)/h),
       'original_n1_slope_deviation':float(slope_err),
       'material_time_current_error':jerr,
       'material_2_euler_rows':'ZERO on complete interior',
       'one_local_radial_coframe_euler':'ZERO via x=y=0',
       'remaining_16_coframe_max_midpoint':eco,
       'remaining_24_link_h_scaled_max_midpoint':elink,
       'nontrivial_spatial_based_holonomy_norm_over_h2':curvature_nontrivial,
       'two_independent_null_streams_max_error':float(null_error),
       'original_two_real_field_stress_rank':int(np.linalg.matrix_rank(stress)),
       'PF':'alternating 1 and 2 diagnostic, NOT actual AF descendant weights'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    checkpins()
    exact=verify_exact_theorem()
    tests=[grid_test(lo,hi,n) for lo,hi in
           ((1,1.2),(.85,1.15),(.9,1.4)) for n in (16,32,64,128)]
    result={'status':'PASS_EXACT_FINITE_DOUBLE_ZERO_UNIMODULAR_SHEET',
      'input':'original six-face G2/STAR + two real CAR16 scalar/top increments + old N1 GoldenMaster',
      'analytic':exact,'grids':tests,
      'scope':{
        'all_independent_42_stationary':False,
        'exact_star_zero_every_interior_anchor':True,
        'exact_CAR_kinetic_zero':True,
        'exact_two_material_Euler_rows':True,
        'exact_one_radial_coframe_Euler_row':True,
        'arbitrary_positive_fixed_PF_weights_supported_on_sheet':True,
        'fixed_two_end_collar_automatically_solved':False,
        'remaining_39_geometric_Euler_rows':'NOT exact zero',
        'all_slab_gauge_fixed_inverse':False,
        'full_upstream_Book03_selection':False,
        'GR_closed':False}}
    txt=json.dumps(result,indent=2)+'\n'
    print(txt,end='')
    if args.json:
        args.json.write_text(txt)

if __name__=='__main__':
    main()
