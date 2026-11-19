#!/usr/bin/env python3
import json
import math
import numpy as np

rng=np.random.default_rng(282810)

def herm(n):
 M=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
 M=(M+M.conj().T)/2
 return M/np.linalg.norm(M,2)

def anti(n):
 return 1j*herm(n)

def unitary(n):
 M=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
 Q,R=np.linalg.qr(M)
 phase=np.diag(R)/np.abs(np.diag(R))
 return Q@np.diag(phase)

def expanti(K,t):
 vals,V=np.linalg.eigh(-1j*K)
 return (V*np.exp(1j*t*vals))@V.conj().T

def heat(Delta,beta):
 vals=np.linalg.eigvalsh(Delta)
 m=float(vals.min())
 return -m+math.log(float(np.exp(-beta*(vals-m)).sum()))/beta

def rho(Delta,beta):
 vals,V=np.linalg.eigh(Delta)
 w=np.exp(-beta*(vals-vals.min()));w/=w.sum()
 return (V*w)@V.conj().T

def pairing(A,B):
 return float(np.vdot(A,B).real)

def bkm(Delta,beta,A,B):
 vals,V=np.linalg.eigh(Delta)
 probs=np.exp(-beta*(vals-vals.min()));probs/=probs.sum()
 Ap=V.conj().T@A@V;Bp=V.conj().T@B@V
 L=np.empty((len(vals),len(vals)))
 for i in range(len(vals)):
  for j in range(len(vals)):
   if abs(vals[i]-vals[j])<1e-12:
    L[i,j]=(probs[i]+probs[j])/2
   else:
    L[i,j]=(probs[i]-probs[j])/(-beta*(vals[i]-vals[j]))
 first=np.sum(L*Ap*Bp.T).real
 ma=np.sum(probs*np.diag(Ap)).real;mb=np.sum(probs*np.diag(Bp)).real
 return float(first-ma*mb)

def mixed_fd(fun,h=0.004):
 stencil=((-2,1),(-1,-8),(1,8),(2,-1))
 return sum(ci*cj*fun(i*h,j*h) for i,ci in stencil for j,cj in stencil)/(144*h*h)

def first_fd(fun,h=0.001):
 return (fun(-2*h)-8*fun(-h)+8*fun(h)-fun(2*h))/(12*h)

def price(P,U,Delta,beta,z):
 I=np.eye(len(P));C=(I-P)@U@P;F=C.conj().T@C
 vals=np.linalg.eigvalsh((F+F.conj().T)/2)
 return heat(Delta,beta)-float(np.log1p(-z*vals).sum())

def gradients(P,U,Delta,beta,z):
 I=np.eye(len(P));C=(I-P)@U@P
 R=np.linalg.inv(I-z*C.conj().T@C)
 A=R@C.conj().T@U-U@R@C.conj().T
 return -rho(Delta,beta),2*z*C@R,z*(A+A.conj().T)

heat_rows=[]
for n in (3,4,6,8):
 Delta=2*np.eye(n)+herm(n)
 A=herm(n);B=herm(n);C=herm(n);beta=0.7
 rr=rho(Delta,beta)
 cv=bkm(Delta,beta,A,B)
 predicted=-pairing(rr,C)+beta*cv
 actual=mixed_fd(lambda t,s:heat(Delta+t*A+s*B+t*s*C,beta))
 bound=np.linalg.norm(C,2)+beta*np.linalg.norm(A,2)*np.linalg.norm(B,2)
 var_a=pairing(rr,A@A)-pairing(rr,A)**2
 bkm_a=bkm(Delta,beta,A,A)
 err=abs(actual-predicted)
 if err>2e-8 or abs(predicted)>bound+1e-12 or bkm_a>var_a+1e-12 or bkm_a<-1e-12:
  raise RuntimeError(('heat',n,actual,predicted,err,bkm_a,var_a,bound))
 if min(np.linalg.norm(Delta@A-A@Delta),abs(pairing(rr,C)),abs(beta*cv))<1e-6:
  raise RuntimeError(('heat negative control is not discriminating',n))
 heat_rows.append(dict(n=n,error=err,predicted=predicted,bound=float(bound),noncommuting_norm=float(np.linalg.norm(Delta@A-A@Delta)),missing_delta_xy_defect=abs(pairing(rr,C)),missing_bkm_defect=abs(beta*cv),BKM_variance=bkm_a,ordinary_variance=var_a))

source_rows=[]
for n in (4,6,8):
 P=np.diag([1.]*(n//2)+[0.]*(n-n//2));U=unitary(n)
 Delta=2*np.eye(n)+herm(n);D=herm(n);K=anti(n);W=anti(n)
 beta=0.63;z=0.17
 gd,gu,gp=gradients(P,U,Delta,beta,z)
 dP=K@P-P@K;dU=U@W
 expected=pairing(gd,D)+pairing(gu,dU)+pairing(gp,dP)
 actual=first_fd(lambda t:price(expanti(K,t)@P@expanti(K,t).conj().T,U@expanti(W,t),Delta+t*D,beta,z))
 err=abs(actual-expected)
 if err>2e-9:
  raise RuntimeError(('source',n,actual,expected,err))
 source_rows.append(dict(n=n,error=err,moving_P_source=pairing(gp,dP),moving_U_source=pairing(gu,dU),moving_Delta_source=pairing(gd,D)))

n=6;length=5;P=np.diag([1.]*3+[0.]*3);Delta=2*np.eye(n)+herm(n)
word=[unitary(n) for _ in range(length)]
beta=0.63;z=0.17

def total(w):
 out=np.eye(n,dtype=complex)
 for V in w:
  out=V@out
 return out

U=total(word);gd,G,gp=gradients(P,U,Delta,beta,z)
word_rows=[];Gs=[]
for j in range(length):
 right=total(word[:j]);left=total(word[j+1:])
 Gj=left.conj().T@G@right.conj().T
 Gs.append(Gj)
 X=anti(n)
 expected=pairing(Gj,word[j]@X)
 def varied_price(t):
  w=list(word);w[j]=w[j]@expanti(X,t)
  return price(P,total(w),Delta,beta,z)
 actual=first_fd(varied_price)
 eta=word[j].conj().T@Gj;eta=(eta-eta.conj().T)/2
 body=pairing(eta,X)
 err=max(abs(actual-expected),abs(body-expected))
 if err>2e-9:
  raise RuntimeError(('word',j,actual,expected,body,err))
 word_rows.append(dict(slot=j,error=err,source=expected))

# Internal frame changes on the SAME word telescope, with endpoints fixed.
Xs=[np.zeros((n,n),complex)]+[anti(n) for _ in range(length-1)]+[np.zeros((n,n),complex)]
dwords=[Xs[j+1]@word[j]-word[j]@Xs[j] for j in range(length)]
gauss_source=sum(pairing(Gs[j],dwords[j]) for j in range(length))
dtotal=np.zeros((n,n),complex)
for j in range(length):
 dtotal+=total(word[j+1:])@dwords[j]@total(word[:j])
if abs(gauss_source)>1e-12 or np.linalg.norm(dtotal)>1e-12:
 raise RuntimeError(('internal_frame',gauss_source,np.linalg.norm(dtotal)))

print(json.dumps(dict(status='PASS',scope='full original heat Hessian and moving-cut terminal covector, exact word-adjoint chain; no physical HDA or GR claim',heat_controls=heat_rows,source_controls=source_rows,word_adjoint_controls=word_rows,internal_frame_control=dict(source_residual=gauss_source,word_variation_norm=float(np.linalg.norm(dtotal)))),indent=2))
