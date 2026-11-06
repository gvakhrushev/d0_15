import numpy as np
from scipy.linalg import expm
A=np.array([[2,0.3+0.4j],[0.3-0.4j,1]],complex); P=[np.diag([1.,0.]),np.diag([0.,1.])]; K=1j*np.array([[0,1],[1,0]],complex); v=[.23,-.41]; t=.7; d=.8; eta=.5; nu=1.3
mul=lambda a,b:np.einsum('ij,jk->ik',a,b)
def dagger(a):return a.conj().T
def ret(y):
 U=expm(y*K);return sum((t+y*v[i])*mul(mul(U,P[i]),dagger(U)) for i in range(2))
def price(y):
 C=ret(y);D=d*np.eye(2)+eta*mul(mul(C,A),dagger(C));x=np.linalg.det(D)
 if abs(x.imag)>=1e-13 or x.real<=0: raise ValueError('det not positive real')
 return -nu*np.log(x.real)
C=ret(0);V=sum(v[i]*P[i] for i in range(2));D=d*np.eye(2)+eta*mul(mul(C,A),dagger(C));R=np.linalg.inv(D);dD=eta*(mul(mul(V,A),dagger(C))+mul(mul(C,A),dagger(V)));trace_term=-nu*np.trace(mul(R,dD)).real
per_sum=-nu*eta*sum(v[i]*np.trace(mul(R,mul(mul(P[i],A),dagger(C))+mul(mul(C,A),dagger(P[i])))).real for i in range(2))
h=1e-4;fd=(-price(2*h)+8*price(h)-8*price(-h)+price(-2*h))/(12*h)
print('noncommutativity=',float(np.linalg.norm(mul(A,P[0])-mul(P[0],A))))
print('trace=',trace_term,'branch_sum=',per_sum,'five_point=',fd,'errors=',abs(trace_term-per_sum),abs(trace_term-fd))
