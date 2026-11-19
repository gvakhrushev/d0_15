#!/usr/bin/env python3
"""D0: same original n24 L8 4096 GOLDEN boxes, full TRUE 4D scalar source.
Attempt genuine fixed-metric nonlinear N1 material Euler root for both scalar
fields (2*6^4=2592 interior variables) with real four-dimensional collar.
Research numerical only; not full 16+24 geom or Book03 selection.
"""
from pathlib import Path
import importlib.util,json,time
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import splu
s=importlib.util.spec_from_file_location('one',Path(__file__).with_name('check_native_n1_scalar_flux.py'))
M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
L=8;n=24;h=1/L;tau=.05;p=float(M.p);z=float(M.z);lnphi=float(M.lnphi)
counts=M.native_counts(n,L)
assert sum(counts)==75025
rho=np.array(counts,dtype=float).reshape((L,)*4)*L**4/75025
r=np.array([M.radius_at_time((i-(L-1)/2)*h) for i in range(L)])
A=np.array([M.coframe(rr)[0] for rr in r]);B=1/A
f=np.array([M.actual_star((i-(L-1)/2)*h,h) for i in range(L)])
eps=np.sqrt(1/(2*23.41640675188407497289558))
coords=[(i,j,k,l) for i in range(L) for j in range(L) for k in range(L) for l in range(L)]
N=L**4
unknown_sites=[x for x in coords if all(1<=v<=L-2 for v in x)]
idxmap={x:i for i,x in enumerate(unknown_sites)}
Nin=len(unknown_sites)
assert Nin==6**4
nvar=2*Nin
psi=np.zeros((2,L,L,L,L),dtype=float)
for i in range(L-1):psi[0,i+1,:,:,:]=psi[0,i,:,:,:]+h*eps*A[i]**2
for j in range(L):psi[1,:,j,:,:]=eps*j*h
interior=np.array(unknown_sites,dtype=int)

def state(x):
  f0=psi.copy()
  for a in range(2):f0[(a,)+tuple(interior.T)]=x[a*Nin:(a+1)*Nin]
  return f0

# Cells that have all 4 positive neighbor directions inside the full grid.
cells=[(i,j,k,l) for i in range(L-1) for j in range(L-1) for k in range(L-1) for l in range(L-1)]
Ncell=len(cells)
# per-cell (species, derivative-direction) order a0_t,a0_x,a0_y,a0_z,a1_t,a1_x,a1_y,a1_z
rows=[];cols=[];values=[];gfix=np.zeros(Ncell*8)
Gcoeff=np.zeros((Ncell,8))
RHO=np.zeros(Ncell);FF=np.zeros(Ncell)
for ci,coord in enumerate(cells):
  i,j,k,l=coord
  g=[1/A[i]**2,-1/B[i]**2,-1/r[i]**2,-1/r[i]**2]
  RHO[ci]=rho[coord]
  FF[ci]=f[i]
  for a in range(2):
    for direction in range(4):
      slot=ci*8+a*4+direction
      Gcoeff[ci,a*4+direction]=g[direction]
      target=list(coord);target[direction]+=1
      target=tuple(target)
      for c,sign in ((coord,-1),(target,1)):
        val=sign/h
        if c in idxmap:
          rows.append(slot);cols.append(a*Nin+idxmap[c]);values.append(val)
        else:
          gfix[slot]+=val*psi[(a,)+c]
GG=coo_matrix((values,(rows,cols)),shape=(Ncell*8,nvar)).tocsr()
GN=Gcoeff.reshape(-1)
Smat=coo_matrix((np.ones(Ncell*8),(np.repeat(np.arange(Ncell),8),np.arange(Ncell*8))),shape=(Ncell,Ncell*8)).tocsr()
X=-tau*FF/RHO
Ymul=tau/RHO

def F_y_ratio(x,y):
 E=p*p*(1+x); ell=4*E*(1-E)
 u=p-p*p*y;Bb=4*u*u*(1-u*u)
 Q=1-z*Bb;RR=1-z*(ell+(1-ell)*Bb)
 pr=1-Q*RR
 R_y=z*(-8*p*p*u*(1-2*u*u))*(RR+Q*(1-ell))
 return (-np.log((1-pr)/pr)/lnphi*R_y)/float(M.norm)

x0=np.array([psi[(a,)+c] for a in range(2) for c in unknown_sites])

def source(x,buildJac=False):
 grad=(GG@x+gfix)
 g=grad.reshape(Ncell,8)
 qq=(Gcoeff*g*g).sum(axis=1)
 value=F_y_ratio(X,Ymul*qq)
 vec=(value[:,None]*Gcoeff*g).reshape(-1)
 residual=GG.T@vec
 if not buildJac:return residual,(qq,value)
 # Exact derivative of the SAME full N1 nonlinear source, including
 # the cross-species and cross-direction dependence through q.
 V_y=np.imag(F_y_ratio(X,Ymul*qq+1e-20j))/1e-20
 weighted=Smat@diags((Gcoeff*g).reshape(-1))@GG
 J=GG.T@diags((value[:,None]*Gcoeff).reshape(-1))@GG
 J=J+weighted.T@diags(2*Ymul*V_y)@weighted
 return residual,(qq,value),J.tocsc()

start=time.time();res0,_=source(x0)
print('INITIAL',np.max(abs(res0)),np.linalg.norm(res0),'time',time.time()-start,flush=True)
x=x0.copy();success=False
for it in range(40):
  residual,(qq,v),J=source(x,True)
  e0=float(np.max(np.abs(residual)))
  print('ITER',it,'residual',e0,'q',float(np.max(abs(qq))),'time',time.time()-start,flush=True)
  if e0<1e-13:
    success=True;break
  LU=splu(J,permc_spec='COLAMD',diag_pivot_thresh=.4)
  dx=LU.solve(-residual)
  step=1
  for trial in range(12):
    rr,_=source(x+step*dx)
    if np.max(abs(rr))<e0:
      x+=step*dx;break
    step*=.5
  else:raise ArithmeticError('line search failed')
res,(qq,v)=source(x)
assert np.linalg.norm(res,np.inf)<1e-9
ps=state(x)
assert max(np.max(abs(ps[a][0]-psi[a][0])) for a in range(2))==0
assert max(np.max(abs(ps[a][-1]-psi[a][-1])) for a in range(2))==0
correct=float(np.max(abs(x-x0)))
print(json.dumps({'status':'PASS_NUMERICAL_TRUE_N1_BOTH_SCALAR_FULL4D_NATIVE_PF',
 'n':n,'L':L,'original_cost_n_histories':75025,'native_original_sites':4096,
 'interior_scalar_unknowns':nvar,'all_original_4d_dirichlet_collar_fixed':True,
 'original_native_PF_minmax':[float(rho.min()),float(rho.max())],
 'before_residual_inf':float(np.max(abs(res0))),
 'after_residual_inf':float(np.max(abs(res))),
 'per_species_after':[float(np.max(abs(res[a*Nin:(a+1)*Nin]))) for a in range(2)],
 'max_original_scalar_field_correction':correct,
 'max_actual_resulting_nonlinear_q':float(np.max(abs(qq))),
 'iterations':it,'numerical_source_only':True,
 'native_coframe16_proved_root':False,'proper_link24_proved_root':False,
 'Book03_compulsory_price_selected':False,'GR_closed':False},indent=2))
