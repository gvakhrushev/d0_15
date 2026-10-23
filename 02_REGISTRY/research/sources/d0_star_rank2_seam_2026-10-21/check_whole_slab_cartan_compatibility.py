#!/usr/bin/env python3
"""Original six-face 24-link Cartan gate: isolated site IFT versus coherent
three-time-slice link correction on the same rank-two non-VSI geometry.
Finite local L4 spatially homogeneous test ONLY, not an exact whole-slab root.
"""
from __future__ import annotations
import json
import numpy as np
import sympy as sp
from scipy.optimize import root
from scipy.linalg import expm
from check_star_rank2_seam import cell,star_density,matter_query,LORENTZ,KAPPA

def exact_covariant_difference():
    h=sp.symbols('h')
    F=sp.Matrix([[0,1],[-2,0]])
    Z=sp.Matrix([[1,2],[3,4]])
    Zd=sp.Matrix([[2,3],[5,7]])
    P=sp.eye(2)+h*F
    # Original forward based face at U_time=I; left variations of TWO true
    # neighbor spatial links: U_next and U_now.
    single=sp.expand(-P*Z)
    coherent=sp.expand((Z+h*Zd)*P-P*Z)
    assert sp.expand(coherent-h*(Zd+Z*F-F*Z)-h*h*Zd*F)==sp.zeros(2)
    assert single.subs(h,0)!=sp.zeros(2)
    assert coherent.subs(h,0)==sp.zeros(2)
    return {'single_site_normalized_curvature_correction':'-P Z = O(1)',
            'smooth_neighbor_normalized_curvature_correction':'h*(Zd+[Z,F])+h^2*Zd F',
            'first_order_identity':'d(P0i)/h^2=Z_next P0i-P0i Z_now'}
def gradient_links(prev,cur,nex,h):
    def act():return star_density(prev,cur,h)+star_density(cur,nex,h)
    eps=1e-20
    out=np.zeros(24)
    for r in range(4):
        for j,X in enumerate(LORENTZ):
            saved=cur['u'][r].copy()
            cur['u'][r]=expm(1j*eps*X)@saved
            out[6*r+j]=act().imag/eps
            cur['u'][r]=saved
    return out
def gradient_coframe(prev,cur,nex,h,amp):
    def act():return star_density(prev,cur,h)+star_density(cur,nex,h)+KAPPA*matter_query(cur)
    eps=1e-20
    out=np.zeros((4,4))
    for i in range(4):
        for j in range(4):
            saved=cur['e'][i,j]
            cur['e'][i,j]=saved+1j*eps
            out[i,j]=act().imag/eps
            cur['e'][i,j]=saved
    return out

def solve(h,kind):
    amp=(1/(2*KAPPA))**.5
    prev,cur,nex=[cell(t,h,amp) for t in (-h,0,h)]
    nodes=[prev,cur,nex]
    bases=[n['u'].copy() for n in nodes]
    def field(theta):
        # One REAL original so(1,3) correction per Role direction.
        # Isolated modifies only one time slice; coherent transports that
        # SAME smooth correction across each neighboring temporal slice.
        idxs=(1,) if kind=='isolated' else (0,1,2)
        for k,n in enumerate(nodes):
            if k not in idxs:n['u'][:]=bases[k]
            else:
                for r in range(4):
                    X=sum(theta[6*r+j]*LORENTZ[j] for j in range(6))
                    n['u'][r]=expm(h*X)@bases[k][r]
        return gradient_links(prev,cur,nex,h)
    sol=root(field,np.zeros(24),method='hybr',
             options={'xtol':1e-10,'maxfev':400})
    residual=field(sol.x)
    co=gradient_coframe(prev,cur,nex,h,amp)
    linkerr=float(np.max(np.abs(residual)))
    coerr=float(np.max(np.abs(co)))
    spin=float(np.max(np.abs(sol.x)))
    if not sol.success or linkerr>1e-9:
        raise ArithmeticError(('original24 central Cartan root',kind,h,sol.message,linkerr))
    if not spin<.5*h:raise ArithmeticError(('spin corrections not O(h)',kind,h,spin))
    if kind=='isolated':
        if not .70<coerr<.85:raise ArithmeticError(('isolated time spike',h,coerr))
    else:
        if not coerr<.8*h:raise ArithmeticError(('coherent source not O(h)',h,coerr))
    return {'h':h,'kind':kind,'central_link_24_max_source':linkerr,
            'spin_correction_max':spin,'all16_coframe_max_source':coerr,
            'coframe_over_h':coerr/h}
def main():
    out={'status':'PASS_SCOPED_WHOLE_SLAB_CARTAN_COMPATIBILITY',
         'analytic':exact_covariant_difference(),
         'rows':[solve(1/n,kind) for kind in ('isolated','coherent')
                 for n in (8,16,32,64)],
         'scope':{'central_24_link_rows_solved':True,
                  'neighbor_link_rows_also_solved':False,
                  'coframe_16_rows_exactly_zero':False,
                  'material_2_rows_full_CQ_exactly_zero':False,
                  'actual_full_discrete_root_proved':False,
                  'separate_link_site_Newton_is_a_valid_whole_slab_inverse':False,
                  'one_full_native_Book_price_selected':False,'GR_closed':False}}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
