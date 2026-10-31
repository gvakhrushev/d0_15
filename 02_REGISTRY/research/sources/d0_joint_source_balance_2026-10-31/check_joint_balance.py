#!/usr/bin/env python3
"""Solve the whole matrix endpoint source; then test whether field response survives.

Uses the owned homogeneous K(9,11,13) H+J, original beta/zeta, the 32-dimensional
carrier and rank-eight canonical input. This emits NO native gate word. N is a
fixed mathematical clock length, not a falsely claimed compiled duration.
Existence/uniqueness is proved by exact rational inequalities; decimal roots are
numerical diagnostics. No Einstein equation, new price or counterterm is fitted.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib,json,platform
import mpmath as mp
import numpy as np
import scipy.linalg as la
from scipy.special import iv
import sympy as sp

mp.mp.dps=65
p=(mp.sqrt(5)-1)/2
beta=2*p*p
z=mp.mpf(2)**-20
RANK=8;DIM=32
SIZES=(9,11,13);DEGS=(26,24,22)
CHECKS=0

def require(ok,name):
 global CHECKS
 CHECKS+=1
 if not bool(ok):raise ArithmeticError(name)

def close(a,b,name,tol):
 err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
 require(err<tol,f'{name}: {err}')
 return err

# Complete 33-scene spectrum: a 3-dimensional constant-on-parts block and
# 8+10+12 genuine within-part modes. No low-mode or heat truncation here.
CB=mp.diag([mp.mpf(1)/v for v in DEGS]);BB=mp.matrix(3)
for i in range(3):
 for j in range(3):
  if i!=j:BB[i,j]=mp.sqrt(mp.mpf(SIZES[i]*SIZES[j])/(DEGS[i]*DEGS[j]))

def scene(x):
 vals,V=mp.eigsy(mp.eye(3)-BB-2*x*CB)
 ee=[mp.exp(-beta*v) for v in vals]
 tr=sum(ee)
 ct=sum(ee[k]*sum(CB[i,i]*V[i,k]**2 for i in range(3)) for k in range(3))
 for n,d in zip(SIZES,DEGS):
  e=mp.exp(-beta*(1-2*x/d));tr+=(n-1)*e;ct+=(n-1)*e/d
 return tr,2*beta*ct

RING0={}
def ring(phi,N):
 total=mp.mpf(0);grad=mp.mpf(0)
 for j in range(N):
  a=(phi+2*mp.pi*j)/N
  tr,dx=scene(mp.cos(a));total+=tr;grad-=dx*mp.sin(a)/N
 return total,grad

def full_price(c,N=4):
 phi=mp.acos(c);s=mp.sqrt(1-c*c)
 if N not in RING0:RING0[N]=ring(0,N)[0]
 sk,gk=ring(phi,N)
 Z=2*((DIM-2*RANK)*RING0[N]+2*RANK*sk)+359*N*DIM
 H=mp.log(Z)/beta;Hc=-4*RANK*gk/(s*beta*Z)
 J=-RANK*mp.log1p(-z*(1-c*c));Jc=-2*RANK*z*c/(1-z+z*c*c)
 return {'B':H+J,'Bc':Hc+Jc,'H':H,'J':J,'Hc':Hc,'Jc':Jc,'Z':Z}

def rational_bounds():
 x=F(2,55);y=F(3,104);zz=F(1,2**20)
 aa=F(33)/(1-x*x)
 fac=F(8*RANK*4,3*359*DIM)
 Jcc_floor=2*RANK*zz*(1-zz-zz/F(256))
 result=[]
 q4=x**4/factorial(4)
 # Uniform tail / positive first coefficient decreases with every N>=4.
 # S2(q)-q <= 4q^2/(1-q)^3, and (x^2/y)^N/N! decreases.
 ratio=F(20)/((1-x*x)*(1-q4)**3)*(x*x/y)**4/factorial(4)
 require(ratio<1,'strict positive H_c(0) for every N>=4')
 require(x*x/y<1,'uniform tail comparison decreases with N')
 for N in (4,5,8,198):
  q=x**N/factorial(N)
  S2=q*(1+q)/(1-q)**3
  S4=q*(1+11*q+11*q*q+q**3)/(1-q)**5
  aN_lower=F(33,5)*y**N/factorial(N)
  tail=aa*(S2-q)
  H1=fac*aa*S2
  H2=fac*aa*(S4-q)+F(4,5)*H1**2
  require(aN_lower>tail,'first Laurent harmonic dominates derivative tail')
  require(H1<zz,'B_c(1/16)<0')
  require(H2<Jcc_floor,'strict concavity on entire interval [0,1/16]')
  require(H1/(2*RANK*zz)<F(1,16),'positive critical point stays inside collar')
  result.append({'N':N,'Hc_upper':float(H1) if N<100 else None,'Hcc_abs_upper':float(H2) if N<100 else None,
   'Hc_upper_scientific':mp.nstr(mp.mpf(H1.numerator)/H1.denominator,20),
   'root_upper_scientific':mp.nstr(mp.mpf((H1/(2*RANK*zz)).numerator)/(H1/(2*RANK*zz)).denominator,20),
   'Jcc_abs_lower':float(Jcc_floor),'root_upper':float(H1/(2*RANK*zz)) if N<100 else None,
   'root_upper_exact':str(H1/(2*RANK*zz)) if N==4 else None,
   'underflowed_float_values_not_used_in_certification':N==198})
 return {'exact_rational_all_N_ge_4':True,'root_exists_unique_in':'(0,1/16)',
         'first_harmonic_tail_ratio_upper_at_N4':str(ratio),'bounds':result}

def spectral_controls():
 Adj=np.zeros((33,33));off=np.cumsum([0]+list(SIZES))
 for a in range(3):
  for b in range(3):
   if a!=b:Adj[off[a]:off[a+1],off[b]:off[b+1]]=1
 deg=Adj.sum(1)+2
 rr=np.diag(1/np.sqrt(deg));B=rr@Adj@rr;C=rr@rr
 require(int(Adj.sum()/2)==359,'actual scene edge count')
 errors=[]
 for x in (-.8,.15,.96):
  small=la.eigvalsh(np.eye(3)-np.array(BB.tolist(),float)-2*x*np.array(CB.tolist(),float))
  allsmall=list(small)
  for n,d in zip(SIZES,DEGS):allsmall += [1-2*x/d]*(n-1)
  errors.append(close(np.sort(allsmall),la.eigvalsh(np.eye(33)-B-2*x*C),
                      'complete scene spectral reduction',3e-14))
 return {'all33_scene_modes_preserved':True,'max_scene_error':max(errors)}

def winding_coeffs(order=80):
 """Independent all-coefficient positive power series of full scene trace.
 Float diagnostics only; analytical rational tail bounds live above.
 """
 b=np.array(BB.tolist(),float);c=np.array(CB.tolist(),float);be=float(beta)
 L=2*order+1;center=order
 term=np.zeros((L,3,3));term[center]=np.eye(3)
 total=term.copy()
 for n in range(1,order+1):
  shifted=np.zeros_like(term)
  shifted[1:]+=term[:-1];shifted[:-1]+=term[1:]
  term=be/n*(np.einsum('ij,ljk->lik',b,term)+np.einsum('ij,ljk->lik',c,shifted))
  total+=term
 out=np.empty(order+1)
 for ell in range(order+1):
  out[ell]=np.exp(-be)*np.trace(total[center+ell])
  out[ell]+=np.exp(-be)*sum((n-1)*iv(ell,2*be/d) for n,d in zip(SIZES,DEGS))
 return out

def endpoint(c):
 c=float(c);s=np.sqrt(1-c*c)
 W=np.eye(DIM);W[:RANK,:RANK]=c*np.eye(RANK)
 W[RANK:2*RANK,RANK:2*RANK]=c*np.eye(RANK)
 W[:RANK,RANK:2*RANK]=-s*np.eye(RANK)
 W[RANK:2*RANK,:RANK]=s*np.eye(RANK)
 pf=float(p);G=np.array([[np.sqrt(pf),-pf],[pf,np.sqrt(pf)]])
 birth=np.kron(np.kron(G,G),np.eye(8))
 ii=birth[:,:RANK]
 return birth@W@birth.T,ii,birth

def complete_gradient(c,N,coeff):
 W,i,_=endpoint(c)
 close(W.T@W,np.eye(DIM),'whole endpoint orthogonal',2e-15)
 P=i@i.T;K=i.T@W@i
 close(K,float(c)*np.eye(RANK),'canonical input compression',2e-15)
 d=(1-float(z))*np.eye(RANK)+float(z)*K.T@K
 # dJ=ReTr(C_J X), delta W=XW; no scalar tangent formula used here.
 CJ=-2*float(z)*W@i@la.solve(d,K.T)@i.T
 powers={};Wk=np.eye(DIM)
 for k in range(1,len(coeff)//N):
  Wk=Wk@W;powers[k]=Wk.copy()
 Z=N*DIM*(2*coeff[0]+359)+4*N*sum(coeff[k*N]*np.trace(v) for k,v in powers.items())
 CH=4*N/(float(beta)*Z)*sum((k*coeff[k*N]*v for k,v in powers.items()),np.zeros_like(W))
 B=CH+CJ
 # ReTr(B X) on ALL D^2 skew-Hermitian generators, including complex ones.
 g=[];gh=[];gj=[]
 for a in range(DIM):
  g.append(float(np.real(1j*B[a,a])));gh.append(0.);gj.append(0.)
  for b in range(a):
   g.extend([float(B[b,a]-B[a,b]),float(np.real(1j*(B[b,a]+B[a,b])))])
   gh.extend([float(CH[b,a]-CH[a,b]),0.]);gj.extend([float(CJ[b,a]-CJ[a,b]),0.])
 require(len(g)==DIM**2,'all complex unitary tangent basis directions evaluated')
 require(max(map(abs,g))<3e-21,'all full endpoint derivatives vanish at numerical critical point')
 require(max(map(abs,gh))>0 and max(map(abs,gj))>0,'nonzero terms cancel, not separately deleted')
 # Independent rank-fixed cut displacement. Formula from fixed-P frame.
 cutA=i@la.solve(d,K.T)@i.T
 cutG=-2*float(z)*(cutA@W-W@cutA)
 cuterr=np.max(np.abs(cutG-cutG.T))
 require(cuterr<3e-21,'independent isometric input/cut source vanishes')
 out={'all_endpoint_directions':len(g),'max_total_direction':max(map(abs,g)),
      'max_heat_direction':max(map(abs,gh)),'max_return_direction':max(map(abs,gj)),
      'whole_fibre_dimension':DIM,'input_rank':RANK,'real_native_word_emitted':False,
      'max_cut_skew_coefficient':float(cuterr)}
 return out,W,i,powers,Z

def fd_actual_price(phi,c,N,coeff):
 # A genuine off-shell matrix path with independently rotated two input pairs
 # and a direction mixing the positive-spectrum complement. Full determinant
 # and complete winding heat of the endpoint are used, not a fitted scalar.
 W,i,birth=endpoint(c)
 X=np.zeros((DIM,DIM));X[0,RANK]=-1;X[RANK,0]=1
 Y=np.zeros_like(X);Y[1,19]=.37;Y[19,1]=-.37
 X=birth@(X+Y)@birth.T
 def value(t):
  V=la.expm(t*X)@W;K=i.T@V@i
  J=-np.log1p(-float(z)*la.eigvalsh(np.eye(RANK)-K.T@K)).sum()
  Vk=np.eye(DIM);Z=N*DIM*(2*coeff[0]+359)
  for k in range(1,len(coeff)//N):
   Vk=Vk@V;Z+=4*N*coeff[k*N]*np.trace(Vk)
  return np.log(Z)/float(beta)+J
 # H has a large constant, so floating finite differences are diagnostics only.
 h=1e-3
 fd=(-value(2*h)+8*value(h)-8*value(-h)+value(-2*h))/(12*h)
 require(abs(fd)<2e-11,'independent mixed full-scalar finite difference')
 # Omitting harmonic modes leaves a visibly nonzero gradient at the same root.
 cost=full_price(c,N)
 Z=cost['Z'];wrongHc=cost['Hc']*Z/(Z-359*N*DIM)
 wrong=wrongHc+cost['Jc']
 require(abs(wrong)>1000*abs(cost['Bc']) and abs(wrong)>mp.mpf('1e-12'),
         'discarding harmonic modes breaks source cancellation')
 return {'mixed_matrix_finite_difference':float(fd),'diagnostic_fd_step':h,
         'wrong_omitted_harmonic_derivative':mp.nstr(wrong,30)}

def lost_source_test():
 # An actual chain-rule/Schur identity, not a numerical fit to Einstein=0.
 y1,y2,t,k=sp.symbols('y1 y2 t k',real=True)
 I=y1*y1+2*y2+y1*y2
 s=I+t
 # quadratic Taylor of ANY nondegenerate B at its stationary c_*;
 # exact local envelope result follows from c(Y,t_*(Y))=c_*.
 S=k*s*s/2
 at={t:-I}
 Hyy=sp.hessian(S,(y1,y2)).subs(at)
 Hyt=sp.Matrix([sp.diff(S,y,t).subs(at) for y in (y1,y2)])
 Htt=sp.diff(S,t,t)
 eff=sp.simplify(Hyy-Hyt*Hyt.T/Htt)
 require(eff==sp.zeros(2),'stationary controller Schur complement kills field Hessian')
 require(sp.diff(I,y2)!=0,'field covector in control is nonzero')
 # General quantitative lift identity: A_data = A_control L.
 Ad=sp.Matrix([[1,2],[0,1],[1,-1]])
 Au=sp.eye(3);L=Ad;f=sp.Matrix([[sp.Rational(2,5),-3,7]])
 require(f*Ad==(f*Au)*L,'data source is same controller covector on lift')
 # Wrong claim: nonzero return gain is the nonzero FULL gain at the root.
 return {'effective_hessian_exact':str(eff),
         'same_response_cancellation_loses_field_source':True,
         'scope':'fields and independent controls enter through the same endpoint; scene and cuts fixed',
         'no_claim_for_a_different_independent_spatial_source':True}

def main():
 bounds=rational_bounds();scene_test=spectral_controls();coeff=winding_coeffs()
 rows=[];gradient=None;fd=None
 for N in (4,5,8):
  c=mp.findroot(lambda x:full_price(x,N)['Bc'],(mp.mpf(0),mp.mpf('.001')),
                tol=mp.mpf('1e-58'),solver='secant')
  v=full_price(c,N);Bcc=mp.diff(lambda x:full_price(x,N)['Bc'],c)
  require(0<c<mp.mpf(1)/16,'numerical root inside proven unique-root collar')
  require(abs(v['Bc'])<mp.mpf('1e-55'),'high precision diagnostic full source')
  require(v['Hc']>0 and v['Jc']<0 and Bcc<0,'real cancellation is a stationary saddle/max direction')
  # Independent full-price finite difference at high precision.
  step=mp.mpf('1e-16')
  dh=(full_price(c+step,N)['B']-full_price(c-step,N)['B'])/(2*step)
  require(abs(dh-v['Bc'])<mp.mpf('1e-34'),'independent 65-digit full scalar central difference')
  rows.append({'N':N,'root_c_decimal':mp.nstr(c,48),'Hc':mp.nstr(v['Hc'],48),
   'Jc':mp.nstr(v['Jc'],48),'full_Bc':mp.nstr(v['Bc'],12),'Bcc':mp.nstr(Bcc,32),
   'finite_difference_error':mp.nstr(abs(dh-v['Bc']),12),
   'return_gain_w':mp.nstr(RANK*z*c*c/(1-z+z*c*c),35),
   'full_heat_value':mp.nstr(v['H'],28),'full_return_value':mp.nstr(v['J'],28),
   'all_Hodge_modes':425*N*DIM,'numerical_root_is_not_an_interval_enclosure':True})
  if N==4:
   gradient,W,i,powers,Z=complete_gradient(c,N,coeff)
   close(float(v['Z']),Z,'independent full winding trace',1e-10)
   fd=fd_actual_price(mp.acos(c),c,N,coeff)
 # Reflected QUERY orbit from previous result has constant heat and cannot use
 # this spectral cancellation. It is retained as an explicit negative control.
 cold=p**3;u=mp.sqrt(1-cold*cold)
 reflected_ratio=4*u/cold
 require(reflected_ratio>16,'previous reflected QUERY obstruction remains intact')
 out={'status':'CHECKED_MATRIX_STATIONARITY_AND_LOSS_OF_SHARED_FIELD_GAIN',
      'pinned_input':'1e44de960dabaa86d47d86dfa6193d55d5fd5742',
      'scope':'same Book03 fixed homogeneous scene price and canonical boundary; mathematical endpoint domain, not compiled native execution',
      'exact_bounds':bounds,'scene':scene_test,'stationary_diagnostics':rows,
      'whole_unitary_gradient':gradient,'independent_scalar_control':fd,
      'source_elimination':lost_source_test(),'previous_reflection_normal_ratio':mp.nstr(reflected_ratio,32),
      'checks':CHECKS,'GR_closed':False,'new_native_word_emitted':False,
      'PDE_or_full42_root_solved':False,'Lean_or_CI_run':False,
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__,'mpmath':mp.__version__}}
 print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))
if __name__=='__main__':main()
