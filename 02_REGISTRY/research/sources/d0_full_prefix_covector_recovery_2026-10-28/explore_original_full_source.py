#!/usr/bin/env python3
"""Exploration, NOT a certified stationary GR/root theorem.
The unchanged full4096 Fourier/CAR return from the fixed-boundary owner is used.
Default checks the seven-scale candidate against all280 open-chart rows.
--full-solve repeats the unconstrained Newton-Krylov attempt and reports all
actual domain failures. Failed solver iterates are never admitted as solutions.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
 os.environ[key]='1'
import numpy as np, scipy.linalg as la, scipy.optimize as opt, itertools, time,json
p=(np.sqrt(5)-1)/2;k=2*p*p;z=2**-20;m=644
I=np.eye(16);order=(0,2,3,1)
cre=[]
for mode in range(4):
 c=np.zeros((16,16))
 for bits in range(16):
  if not (bits>>mode)&1: c[bits|(1<<mode),bits]=(-1)**sum((bits>>j)&1 for j in order[:order.index(mode)])
 cre.append(c)
# Exterior wedge representation in the same CAR basis (order 0,2,3,1).
# Act on vacuum, then use transformed creation columns for each occupied ordered mode.
def ext(M):
 out=np.zeros((16,16));vac=np.eye(16)[:,0]
 for bits in range(16):
  state=vac.copy()
  for mode in reversed([j for j in order if (bits>>j)&1]):
   state=sum(M[i,mode]*cre[i] for i in range(4))@state
  out[:,bits]=state
 return out
Rot=np.array([[24,-7],[7,24]])/25.
phase=np.array(list(itertools.product([1,1j,-1,-1j],repeat=4)))
Bs=[];es=[];vs=[]
for j in range(8):
 n=np.zeros(3);n[:2]=np.linalg.matrix_power(Rot,j)@np.array([1.,0.])
 M=np.zeros((4,4));M[0,0]=1;M[1:,1:]=2*np.outer(n,n)-np.eye(3)
 lm=ext(M)
 d=np.zeros((256,16,16),complex)
 for r in range(4):
  U=lm if r==0 else I
  block=cre[r][None,:,:]@(phase[:,r,None,None]*U-I)
  d+=block+block.conj().transpose(0,2,1)
 a=d/16;B=a@a;ev,V=np.linalg.eigh(B)
 Bs.append(B);es.append(ev);vs.append(V)
es=np.array(es);vs=np.array(vs)

def factors(j,nu):
 ev=1-k*nu*nu*es[j]
 if np.min(ev)<=0: raise ValueError('domain')
 V=vs[j];Q=(V*ev[:,None,:]**m)@V.conj().transpose(0,2,1)
 dQ=(V*(2*m*(-k*nu*nu*es[j])*ev**(m-1))[:,None,:])@V.conj().transpose(0,2,1)
 return Q,dQ
E=factors(0,.6)[0]
# scaled objective J/z, gradients wrt lognu
calls=0
def fun(lognu):
 global calls;calls+=1
 nus=np.exp(lognu)
 Qs=[];dQs=[]
 for j,nu in enumerate(nus,1):
  Q,dQ=factors(j,nu);Qs.append(Q);dQs.append(dQ)
 prefixes=[E]
 for Q in Qs:prefixes.append(Q@prefixes[-1])
 K=E@prefixes[-1]
 A=K.conj().transpose(0,2,1)@K
 R=np.linalg.inv((1-z)*I+z*A)
 ev=np.linalg.eigvalsh(A)
 value=-np.sum(np.log1p(-z*(1-ev)))/z
 grad=np.empty(7);T=E
 for j in reversed(range(7)):
  dK=T@dQs[j]@prefixes[j]
  grad[j]=-2*np.einsum('nij,nji->',R@K.conj().transpose(0,2,1),dK).real
  T=T@Qs[j]
 return value,grad

import torch
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
DT=torch.complex128
Ct=torch.tensor(np.array(cre),dtype=DT);It=torch.eye(16,dtype=DT)
ph=torch.tensor(phase,dtype=DT);Et=torch.tensor(E,dtype=DT)
# All six proper Lorentz generator directions, positive-adjoint representation.
Gs=[]
for a,b in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
 N=np.zeros((4,4));N[a,b]=1;N[b,a]=1 if a==0 else -1
 Gamma=sum(N[i,j]*cre[i]@cre[j].T for i in range(4) for j in range(4))
 Gs.append(Gamma)
Gt=torch.tensor(np.array(Gs),dtype=DT)
base=[]
for j in range(1,8):
 n=np.zeros(3);n[:2]=np.linalg.matrix_power(Rot,j)@np.array([1.,0.]);M=np.zeros((4,4));M[0,0]=1;M[1:,1:]=2*np.outer(n,n)-np.eye(3)
 base.append(np.stack([ext(M),I,I,I]))
base=torch.tensor(np.array(base),dtype=DT)


def function(x,return_extra=False):
 coframes=x[:,:16].reshape(7,4,4)
 con=x[:,16:].reshape(7,4,6)
 U=torch.matrix_exp(torch.einsum('jra,aik->jrik',con.to(DT),Gt))@base
 Cr=torch.einsum('jra,aik->jrik',coframes.to(DT),Ct)
 blocks=torch.einsum('jrik,jnrkl->jnril',Cr,ph[None,:,:,None,None]*U[:,None]-It)
 d=blocks.sum(2);d=(d+d.mH)/16
 A=d@d;C=It-k*A
 Q=torch.linalg.matrix_power(C,m)
 K=Et
 for j in range(7):K=Q[j]@K
 K=Et@K
 D=(1-z)*It+z*(K.mH@K)
 value=-torch.linalg.slogdet(D)[1].sum()/z
 if return_extra:return value,float(torch.linalg.eigvalsh(A).detach().max())
 return value

def main():
 import argparse,platform
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--full-solve',action='store_true');args=parser.parse_args()
 s7=opt.least_squares(lambda v:fun(v)[1],np.full(7,np.log(.45)),bounds=(np.log(.15),np.log(.8)),diff_step=2e-4,max_nfev=70,ftol=1e-10,xtol=1e-10,gtol=1e-10)
 scales=np.exp(s7.x);x=np.zeros((7,40));x[:,:16]=(scales[:,None,None]*np.eye(4)).reshape(7,16)
 xt=torch.tensor(x,requires_grad=True);f=function(xt);g=torch.autograd.grad(f,xt)[0].detach().numpy()
 out={'input_commit':'1e6420f319d714be53363a77823f76ec620a6473','status':'EXPLORATION_NOT_CLOSED',
      'price_normalization':'J/(zeta*kappa_actual), kappa not replaced by missing heat multiplicity',
      'source':'original all4096 Fourier/CAR retained return, fixed first/last 644-round groups',
      'seven_scales':scales.tolist(),'seven_scale_gradient':fun(s7.x)[1].tolist(),
      'all280_gradient':g.tolist(),'all280_max_abs':float(np.max(abs(g))),
      'old_domain_time_leg_row_first_group':float(g[0,0]),
      'full_stationary_root_proved':False,'full_heat_diagonalized':False,'GR_closed':False,
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'torch':torch.__version__}}
 if args.full_solve:
  def fullgrad(v):
   t=torch.tensor(v.reshape(7,40),requires_grad=True)
   return torch.autograd.grad(function(t),t)[0].detach().numpy().ravel()
  root=opt.root(fullgrad,x.ravel(),method='krylov',options={'maxiter':30,'fatol':1e-8,'jac_options':{'inner_maxiter':10,'rdiff':1e-5}})
  xx=root.x.reshape(7,40);co=xx[:,:16].reshape(7,4,4)
  with torch.no_grad():
   con=torch.tensor(xx[:,16:].reshape(7,4,6),dtype=DT)
   lam=torch.matrix_exp(torch.einsum('jra,aik->jrik',con,Gt))@base
   cr=torch.einsum('jra,aik->jrik',torch.tensor(co,dtype=DT),Ct)
   maximum=float(torch.linalg.matrix_norm(cr@lam,ord=2).max())
  out['joint_attempt']={'success_flag':bool(root.success),'message':str(root.message),
     'gradient_norm':float(np.linalg.norm(root.fun)),'coframe_inverse_determinants':np.linalg.det(co).tolist(),
     'largest_primitive_contraction_norm':maximum,'solution_accepted':False,
     'reason':'No proved root, and all chart/domain conditions must hold independently of optimizer stopping.'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
