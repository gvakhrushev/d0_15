import numpy as np
from scipy.linalg import expm
mul=lambda a,b:np.einsum('ij,jk->ik',a,b)
dag=lambda a:a.conj().T
A=np.array([[1,1j],[-1j,1]],complex); P=[np.diag([1.,0.]),np.diag([0.,1.])]; K=1j*np.array([[0,1],[1,0]],complex)
M=2;c=.83;d=.8; L=np.array([.7,-.4]);z0=np.array([.6,-.2]);dz=np.array([[[1.,.1],[-.2,.4]],[[.3,-.5],[.6,.8]]]);field=np.einsum('k,ijk->ij',L,dz)
for g,eta,nu in ((.35,.6,1.3),(0.,.6,1.3),(.35,0.,1.3),(.35,.6,0.),(-.35,.6,1.3)):
 def amp(i,y):return np.prod([c-2*g*y*field[i,j] for j in range(M)])
 def ret(y):
  U=expm(y*K);return sum(amp(i,y)*mul(mul(U,P[i]),dag(U)) for i in range(2))
 def price(y):
  C=ret(y); D=d*np.eye(2)+eta*mul(mul(C,A),dag(C));x=np.linalg.det(D)
  if abs(x.imag)>=1e-13 or x.real<=0:raise ValueError('invalid determinant')
  return -nu*np.log(x.real)
 t=c**M; q=eta*t*t; R=np.linalg.inv(d*np.eye(2)+q*A);w=np.trace(mul(R,A)).real; pi=np.array([np.trace(mul(P[i],mul(R,A))).real/w for i in range(2)])
 def mean(y):return sum((pi[i]+(.1 if i==0 else -.1)*y)/M*sum(z0+y*dz[i,j] for j in range(M)) for i in range(2))
 dmean=sum(pi[i]/M*sum(dz[i,j] for j in range(M)) for i in range(2)); owner_gain=nu*eta*t*t*w; gamma=4*g*M*owner_gain/c; predicted=gamma*np.dot(L,dmean)
 h=1e-4; fd=(-price(2*h)+8*price(h)-8*price(-h)+price(-2*h))/(12*h); fdmean=(mean(h)-mean(-h))/(2*h)
 if abs(fd-predicted)>1e-8 or np.max(np.abs(fdmean-dmean))>1e-8:raise ValueError('control failed')
 print('g=',g,'eta=',eta,'nu=',nu,'M=',M,'c=',c,'gamma=',gamma,'L_dmean=',np.dot(L,dmean),'predicted=',predicted,'finite_difference=',fd,'error=',abs(predicted-fd))
print('norm_commutator=',np.linalg.norm(mul(A,P[0])-mul(P[0],A)))
