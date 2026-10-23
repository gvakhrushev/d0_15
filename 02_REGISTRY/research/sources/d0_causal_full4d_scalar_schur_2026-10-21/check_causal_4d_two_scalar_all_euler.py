#!/usr/bin/env python3
"""D0 #334: causal exact-local inverse for BOTH original N1 scalar fields
on the ORIGINAL 75,025-word Golden n24/L8, full 4D spatial grid.
Finite Cauchy+inflow conditions, NOT all-sides Dirichlet or physical GR.
The exact finite existence theorem follows by triangular analytic IFT near
zero Cauchy data; printed nonzero-amplitude results are numerical controls.
"""
import importlib.util, json, math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
OWNER=Path(__file__).with_name('check_native_n1_scalar_flux.py')
if not OWNER.exists():
    OWNER=Path(__file__).resolve().parents[1]/'d0_native_golden_pf_material_flux_2026-10-21'/'check_native_n1_scalar_flux.py'
s=importlib.util.spec_from_file_location('native', OWNER)
N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
p,z,lnphi=map(float,(N.p,N.z,N.lnphi)); tau=.05;L=8; h=1/L
rho=np.array(N.native_counts(24,L)).reshape((L,)*4)*L**4/75025
assert int(round(rho.sum()*75025/L**4))==75025
assert abs(rho.min()-4096*4/75025)<1e-14
T=[(i-(L-1)/2)*h for i in range(L)]
r=np.array([N.radius_at_time(t) for t in T])
A=np.array([N.coframe(x)[0] for x in r]);B=1/A
G=np.array([[1/A[i]**2,-1/B[i]**2,-1/r[i]**2,-1/r[i]**2] for i in range(L)])
f=np.array([N.actual_star(t,h) for t in T[:-1]])
epsilon=(2*23.41640675188407497289558)**-.5
psi=np.zeros((2,L,L,L,L))
for i in range(L-1):psi[0,i+1]=psi[0,i]+h*epsilon*A[i]**2
for j in range(L):psi[1,:,j]=epsilon*j*h
baseline=psi.copy()

# Exact derivative, from the SAME old negative-orientation N1 raw r.
def phi_y(x,y,second=False):
    E=p*p*(1+x);ell=4*E*(1-E);u=p-p*p*y
    b=4*u*u*(1-u*u);by=-8*p*p*u*(1-2*u*u)
    byy=8*p**4*(1-6*u*u)
    Q=1-z*b;R=1-z*(ell+(1-ell)*b)
    click=1-Q*R;C=R+Q*(1-ell)
    ry=z*by*C;hy=math.log((1-click)/click)/lnphi
    fy=-hy*ry
    if not second:return fy
    ryy=z*byy*C-2*z*z*(1-ell)*by*by
    fyy=ry*ry/(click*(1-click)*lnphi)-hy*ryy
    return fy,fyy
base=phi_y(0,0)
flux=np.zeros((L-1,4,2,L-1,L-1,L-1))
qmax=0.;minfac=math.inf;maxfac=0.;newtonmax=0

def spatial(i,j,k,l):
    return np.array([(psi[:,i,j+1,k,l]-psi[:,i,j,k,l])/h,
                     (psi[:,i,j,k+1,l]-psi[:,i,j,k,l])/h,
                     (psi[:,i,j,k,l+1]-psi[:,i,j,k,l])/h])

def current(i,j,k,l,u,sp):
    q=G[i,0]*float(u@u)+sum(G[i,a+1]*float(sp[a]@sp[a]) for a in range(3))
    W=phi_y(-tau*f[i]/rho[i,j,k,l],tau*q/rho[i,j,k,l])/base
    return np.array([W*G[i,0]*u]+[W*G[i,a+1]*sp[a] for a in range(3)]),q

def solve(i,j,k,l,R,sp):
    global minfac,maxfac,newtonmax
    gt=G[i,0];cc=sum((G[i,a+1]*sp[a] for a in range(3)),np.zeros(2))
    qs=sum(G[i,a+1]*float(sp[a]@sp[a]) for a in range(3))
    x=-tau*f[i]/rho[i,j,k,l];scale=tau/rho[i,j,k,l]
    u=(psi[:,i,j,k,l]-psi[:,i-1,j,k,l])/h
    for step in range(16):
        q=gt*float(u@u)+qs
        W,Wy=phi_y(x,scale*q,True);W/=base;Wy/=base
        vec=gt*u+cc;res=W*vec-R
        aval=W*gt
        rank=1+2*scale*Wy/W*float(u@vec)
        assert aval>0 and rank>.8,('bad local characteristic',i,j,k,l)
        minfac=min(minfac,rank);maxfac=max(maxfac,rank)
        # Sherman-Morrison inverse of M=aval I+(2scale gt Wy vec)u^T
        v=2*scale*gt*Wy*vec
        update=res/aval-v*float(u@res)/(aval**2*rank)
        u-=update
        if max(abs(res))<5e-14:
            newtonmax=max(newtonmax,step+1)
            return u
    raise ArithmeticError(('local inverse failed',i,j,k,l))

for j in range(7):
 for k in range(7):
  for l in range(7):
   u=(psi[:,1,j,k,l]-psi[:,0,j,k,l])/h
   flux[0,:,:,j,k,l],_=current(0,j,k,l,u,spatial(0,j,k,l))
for i in range(1,7):
 for j in range(7):
  for k in range(7):
   for l in range(7):
    sp=spatial(i,j,k,l)
    if j*k*l==0:
        u=(psi[:,i+1,j,k,l]-psi[:,i,j,k,l])/h
    else:
        rhs=(flux[i-1,0,:,j,k,l]+flux[i,1,:,j-1,k,l]
             +flux[i,2,:,j,k-1,l]+flux[i,3,:,j,k,l-1])
        u=solve(i,j,k,l,rhs,sp)
        psi[:,i+1,j,k,l]=psi[:,i,j,k,l]+h*u
    flux[i,:,:,j,k,l],q=current(i,j,k,l,u,sp)
    qmax=max(qmax,abs(q))
res=[];offdiag=np.zeros((4,4))
for i in range(1,7):
 for j in range(1,7):
  for k in range(1,7):
   for l in range(1,7):
    eq=(flux[i-1,0,:,j,k,l]-flux[i,0,:,j,k,l]
        +flux[i,1,:,j-1,k,l]-flux[i,1,:,j,k,l]
        +flux[i,2,:,j,k-1,l]-flux[i,2,:,j,k,l]
        +flux[i,3,:,j,k,l-1]-flux[i,3,:,j,k,l])
    res.extend(eq)
    gr=np.array([(psi[:,i+1,j,k,l]-psi[:,i,j,k,l])/h,*spatial(i,j,k,l)])
    cross=gr@gr.T
    for a in range(4):
     for b in range(a+1,4):offdiag[a,b]=max(offdiag[a,b],abs(cross[a,b]))
resmax=max(abs(x) for x in res)
assert len(res)==2592 and resmax<1e-11 and qmax<.01
assert offdiag[0,1]>1e-5 # hostile 42->12 support test
out={'status':'PASS_CAUSAL_FULL_4D_TWO_SPECIES_ORIGINAL_N1',
    'native_cost':24,'native_count':75025,'role_sites':4096,
    'native_PF_minmax':[float(rho.min()),float(rho.max())],
    'causal_2x2_local_solves':1296,'both_material_Euler_rows':2592,
    'Euler_residual_max':resmax,
    'max_nonzero_nonlinear_q':qmax,
    'max_corrected_scalar_change':float(np.max(abs(psi-baseline))),
    'local_det_factor_minmax':[minfac,maxfac],
    'local_Newton_steps_max':newtonmax,
    'mixed_material_tx_stress':float(offdiag[0,1]),
    'homogeneous_Ward_42_to_12_preserved':False,
    'causal_initial_and_spatial_inflow_fixed':True,
    'all_four_dimensional_Dirichlet_not_solved':True,
    'genuinely_selected_Book03_full_price':False,'GR_closed':False}
print(json.dumps(out,indent=2))
