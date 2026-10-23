#!/usr/bin/env python3
"""Independent exact N1 whole-CQ entropy derivative for the ACTUAL original
4D causal two-scalar solution, at six independently perturbed input sites.
This is a bounded high-precision author replay, not an interval certificate.
"""
import importlib.util, json
from pathlib import Path
import numpy as np
import mpmath as mp
mp.mp.dps=70
SRC=Path(__file__).with_name('check_causal_4d_two_scalar_all_euler.py')
s=importlib.util.spec_from_file_location('causal',SRC)
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)

p=(mp.sqrt(5)-1)/2;z=mp.mpf(2)**-20;lnphi=mp.log(1/p)

def local_full_price(psi,which,point,imag):
    i,j,k,l=point
    # Only five TRUE original forward-anchored cells contain this field value.
    affected=[point,(i-1,j,k,l),(i,j-1,k,l),(i,j,k-1,l),(i,j,k,l-1)]
    total=mp.mpc('0')
    for ii,jj,kk,ll in affected:
        G=[mp.mpf(str(v)) for v in C.G[ii]]
        grads=[]
        for A in range(2):
            arr=[]
            for direction in range(4):
                b=[ii,jj,kk,ll];e=b.copy();e[direction]+=1
                def val(coord):
                    t=mp.mpf(str(psi[(A,)+tuple(coord)]))
                    return t+mp.j*imag if A==which and coord==[i,j,k,l] else t
                arr.append((val(e)-val(b))/mp.mpf(str(C.h)))
            grads.append(arr)
        q=sum(G[d]*(grads[0][d]**2+grads[1][d]**2) for d in range(4))
        rho=mp.mpf(str(C.rho[ii,jj,kk,ll]))
        x=-mp.mpf(str(C.tau))*mp.mpf(str(C.f[ii]))/rho
        y=mp.mpf(str(C.tau))*q/rho
        E=p*p*(1+x);ell=4*E*(1-E)
        u=p-p*p*y;B=4*u*u*(1-u*u)
        R=1-(1-z*B)*(1-z*(ell+(1-ell)*B))
        H=-(R*mp.log(R)+(1-R)*mp.log(1-R))/lnphi
        total-=rho*H
    return total

def current(psi,i,j,k,l):
    grad=np.array([(psi[:,i+1,j,k,l]-psi[:,i,j,k,l])/C.h,
       (psi[:,i,j+1,k,l]-psi[:,i,j,k,l])/C.h,
       (psi[:,i,j,k+1,l]-psi[:,i,j,k,l])/C.h,
       (psi[:,i,j,k,l+1]-psi[:,i,j,k,l])/C.h])
    q=sum(C.G[i,d]*float(grad[d]@grad[d]) for d in range(4))
    w=C.phi_y(-C.tau*C.f[i]/C.rho[i,j,k,l],C.tau*q/C.rho[i,j,k,l])/C.base
    return np.array([w*C.G[i,d]*grad[d] for d in range(4)])

def divergence(psi,pt):
    i,j,k,l=pt;now=current(psi,i,j,k,l)
    return (current(psi,i-1,j,k,l)[0]-now[0]
        +current(psi,i,j-1,k,l)[1]-now[1]
        +current(psi,i,j,k-1,l)[2]-now[2]
        +current(psi,i,j,k,l-1)[3]-now[3])

rows=[]
for a in range(2):
    for node in [(2,2,2,2),(3,4,2,5),(5,3,4,3)]:
        direct=float(mp.im(local_full_price(C.psi,a,node,mp.mpf('1e-30')))/mp.mpf('1e-30'))
        predictor=float((2*C.tau/C.h)*C.base*divergence(C.psi,node)[a])
        original=float(mp.im(local_full_price(C.baseline,a,node,mp.mpf('1e-30')))/mp.mpf('1e-30'))
        original_pred=float((2*C.tau/C.h)*C.base*divergence(C.baseline,node)[a])
        rows.append({'species':a,'node':node,'full_price_derivative':direct,
                     'flux_predictor':predictor,'baseline_nonzero':original,
                     'baseline_flux_predictor':original_pred})
assert max(abs(r['full_price_derivative']-r['flux_predictor']) for r in rows)<2e-17
assert max(abs(r['baseline_nonzero']-r['baseline_flux_predictor']) for r in rows)<2e-17
assert max(abs(r['baseline_nonzero']) for r in rows)>1e-10
assert max(abs(r['full_price_derivative']) for r in rows)<2e-17
print(json.dumps({'status':'PASS_INDEPENDENT_ORIGINAL_N1_FULL_BINARY_CQ_PRICE_EULER',
                  'rows':rows,'GR_closed':False},indent=2))
