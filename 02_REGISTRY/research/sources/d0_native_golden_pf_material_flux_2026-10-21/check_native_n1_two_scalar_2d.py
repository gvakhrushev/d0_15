#!/usr/bin/env python3
"""True native Golden n24/L8 PF, original non-VSI six-face time source,
and the SAME complete sigma-minus N1 GoldenMaster: solve BOTH independent
scalar Euler rows on a 2D temporal/spatial slab with fixed Dirichlet collar.
Geometric 16+24 and absolute Book03 not claimed.
"""
import importlib.util, numpy as np, json
from pathlib import Path
from scipy.optimize import root
spec=importlib.util.spec_from_file_location('one',Path(__file__).with_name('check_native_n1_scalar_flux.py'))
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
p=float(M.p);z=float(M.z);ell=float(M.lnphi)
L=8;n=24;h=1/L;tau=.05
counts=M.native_counts(n,L)
K=sum(counts)
assert K==75025
Nt,Nx=8,8
rho=np.array([[L**4*counts[((i*L+j)*L+4)*L+4]/K for j in range(Nx)] for i in range(Nt)])
T=np.array([(i-(Nt-1)/2)*h for i in range(Nt)])
r=np.array([M.radius_at_time(t) for t in T]); A=np.array([M.coframe(rr)[0] for rr in r]); B=1/A
gt=1/A**2;gx=-1/B**2
f=np.array([M.actual_star(t,h) for t in T])
epsilon=np.sqrt(1/(2*23.41640675188407497289558))
psi0=np.zeros((Nt,Nx));psi1=np.zeros((Nt,Nx))
for i in range(Nt-1):psi0[i+1,:]=psi0[i,:]+h*epsilon*A[i]**2
for j in range(Nx):psi1[:,j]=epsilon*j*h
# root unknowns at interior 6x6 each.
seeds=[psi0,psi1]
coords=[(i,j) for i in range(1,Nt-1) for j in range(1,Nx-1)]
unknown_count=2*len(coords)
assert unknown_count==72

def unpack(x):
  ps=[v.copy() for v in seeds]
  for a in range(2):
    for k,(i,j) in enumerate(coords):ps[a][i,j]=x[a*len(coords)+k]
  return ps

def F_y_ratio(x,y):
  E=p*p*(1+x); L0=4*E*(1-E)
  u=p-p*p*y;BB=4*u*u*(1-u*u)
  Q=1-z*BB;RR=1-z*(L0+(1-L0)*BB)
  raw=1-Q*RR
  r_y=z*(-8*p*p*u*(1-2*u*u))*(RR+Q*(1-L0))
  score=-np.log((1-raw)/raw)/ell*r_y
  return score/float(M.norm)

def mat_euler(x,info=False):
  ps=unpack(x)
  a,b=ps
  t0=(a[1:,:-1]-a[:-1,:-1])/h
  x0=(a[:-1,1:]-a[:-1,:-1])/h
  t1=(b[1:,:-1]-b[:-1,:-1])/h
  x1=(b[:-1,1:]-b[:-1,:-1])/h
  q=gt[:-1,None]*(t0*t0+t1*t1)+gx[:-1,None]*(x0*x0+x1*x1)
  x_var=-tau*f[:-1,None]/rho[:-1,:-1]
  y_var=tau*q/rho[:-1,:-1]
  w=F_y_ratio(x_var,y_var)
  flux=[]
  for vt,vx in ((t0,x0),(t1,x1)):
    jt=gt[:-1,None]*w*vt
    jx=gx[:-1,None]*w*vx
    flux.append(jt[:-1,1:]-jt[1:,1:]+jx[1:,:-1]-jx[1:,1:])
  residual=np.concatenate([x.flatten() for x in flux])
  if info:return residual,ps,q,w
  return residual
x0=np.array([v[i,j] for v in seeds for i,j in coords])
res0=mat_euler(x0)
print('before',np.linalg.norm(res0,np.inf),np.linalg.norm(res0), flush=True)
sol=root(mat_euler,x0,method='hybr',options={'xtol':1e-11,'maxfev':1200})
res=mat_euler(sol.x)
print('SOLVED',sol.success,sol.message,'calls',sol.nfev,'after',np.linalg.norm(res,np.inf),flush=True)
if not (np.linalg.norm(res,np.inf)<1e-9):raise AssertionError('full two scalar residual not solved')
_,ps,q,w=mat_euler(sol.x,True)
from scipy.optimize._numdiff import approx_derivative
J=approx_derivative(mat_euler,sol.x,method='3-point',abs_step=2e-6)
singular=np.linalg.svd(J,compute_uv=False)
assert singular[-1]>.8 and singular[0]/singular[-1]<65
print(json.dumps({'status':'PASS_NATIVE_ORIGINAL_FULL_TWO_SCALAR_FINITE_EULER' if sol.success else 'SMALL_RESIDUAL_SOLVER_DID_NOT_REPORT_SUCCESS',
 'n':n,'L':L,'native_histories':K,'native_rho_minmax':[float(rho.min()),float(rho.max())],
 'baseline_residual_inf':float(np.linalg.norm(res0,np.inf)),
 'solved_residual_inf':float(np.linalg.norm(res,np.inf)),
 'scalar0_before_inf':float(np.max(np.abs(res0[:len(coords)]))),
 'scalar1_before_inf':float(np.max(np.abs(res0[len(coords):]))),
 'scalar0_after_inf':float(np.max(np.abs(res[:len(coords)]))),
 'scalar1_after_inf':float(np.max(np.abs(res[len(coords):]))),
 'max_field_value_correction':max(float(np.max(np.abs(ps[a]-seeds[a]))) for a in (0,1)),
 'max_true_q_after':float(np.max(np.abs(q))),
 'full72x72_numerical_Jacobian_sigma_min':float(singular[-1]),
 'full72x72_numerical_Jacobian_cond2':float(singular[0]/singular[-1]),
 'Jacobian_certified_by_exact_intervals':False,
 'fixed_dirichlet_collars':all(np.array_equal(ps[a][0,:],seeds[a][0,:]) and np.array_equal(ps[a][-1,:],seeds[a][-1,:]) and np.array_equal(ps[a][:,0],seeds[a][:,0]) and np.array_equal(ps[a][:,-1],seeds[a][:,-1]) for a in (0,1)),
 'two_material_Euler_classes_solved_numerically':True,
 'genuine_42_geometric_root_proved':False,'Book03_selected':False,'GR_closed':False},indent=2))
