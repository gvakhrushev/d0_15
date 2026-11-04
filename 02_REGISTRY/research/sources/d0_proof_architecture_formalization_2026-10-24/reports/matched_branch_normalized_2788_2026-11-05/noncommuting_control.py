import numpy as np
from scipy.linalg import expm
mul=lambda a,b:np.einsum('ij,jk->ik',a,b)
dagger=lambda a:a.conj().T
A=np.array([[1,1j],[-1j,1]],complex);P=[np.diag([1.,0.]),np.diag([0.,1.])];K=1j*np.array([[0,1],[1,0]],complex);v=[.23,-.41];d=.8
for t,eta,nu in ((.7,.6,1.3),(-.7,.6,1.3),(0.,.6,1.3),(.7,0.,1.3),(.7,.6,-1.3)):
 def ret(y):
  U=expm(y*K);return sum((t+y*v[i])*mul(mul(U,P[i]),dagger(U)) for i in range(2))
 def price(y):
  C=ret(y);D=d*np.eye(2)+eta*mul(mul(C,A),dagger(C));x=np.linalg.det(D)
  if abs(x.imag)>1e-13 or x.real<=0:raise ValueError('invalid determinant')
  return -nu*np.log(x.real)
 q=eta*t*t;R=np.linalg.inv(d*np.eye(2)+q*A);B=mul(R,A);w=np.trace(B).real;pi=[np.trace(mul(P[i],B)).real/w for i in range(2)];gamma=2*nu*eta*t*w
 derivative=-gamma*sum(v[i]*pi[i] for i in range(2));h=1e-4;fd=(-price(2*h)+8*price(h)-8*price(-h)+price(-2*h))/(12*h)
 if not (w>0 and min(pi)>=-1e-12 and abs(sum(pi)-1)<1e-12 and abs(derivative-fd)<1e-8): raise ValueError('control failed')
 print('t=',t,'eta=',eta,'nu=',nu,'q=',q,'w=',w,'pi=',pi,'gamma=',gamma,'derivative=',derivative,'finite_difference=',fd,'error=',abs(derivative-fd))
print('noncommutativity=',np.linalg.norm(mul(A,P[0])-mul(P[0],A)))
