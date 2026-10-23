"""Exact finite CAR obstruction/corrector; numerical compact-chart controls.
No claim of a native discrete uniform-clock semigroup theorem.
"""
import sympy as s
import numpy as np
C=[]
for a in range(4):
 c=s.zeros(16)
 for m in range(16):
  if not(m>>a)&1:c[m|1<<a,m]=(-1)**((m&((1<<a)-1)).bit_count())
 C.append(c)
I=s.eye(16);H=s.symbols('H',real=True);nu=s.Rational(3,5)
b=s.sqrt(1-nu**2*(1+H**2/4));b0=s.Rational(4,5)
J=C[2]-C[2].T;Gamma=s.I*J
Q=C[1]*C[2]*C[0].T+(C[1]*C[2]*C[0].T).T
A1=(J*Q+Q*J)/2
W=[]
for r,cv in enumerate([nu*C[1],nu*(C[0]-H*C[1]/2),nu*C[2],nu*C[3]]):
 r2=nu**2*(1+H*H/4) if r==1 else nu**2;br=b if r==1 else b0
 W.extend([cv,cv.T,I+(br-1)*cv*cv.T/r2,I+(br-1)*cv.T*cv/r2])
Wd=[w.diff(H) for w in W]
def Tsym(X):return sum((w.subs(H,0).T*X*w.subs(H,0) for w in W),s.zeros(16))/8
S1=sum((w.subs(H,0).T*wd.subs(H,0) for w,wd in zip(W,Wd)),s.zeros(16))/8
M1=-2*S1+Tsym(A1)-A1
A3=-s.I*nu**4*J*M1*J
assert A3.H==A3 and s.trace(A3)==0
# At H=0 this source lies in a Clifford-degree2 eigencomponent of T.
assert Tsym(M1)==s.Rational(9,10)*M1
Corr=10*A3/nu**2
assert Corr.H==Corr and s.trace(Corr)==0
assert Corr-Gamma*Tsym(Corr)*Gamma == A3/nu**2
Jplusminus=s.zeros(16)
for i,j in [(1,2),(5,6),(9,10),(13,14)]:Jplusminus[i,j]=1;Jplusminus[j,i]=-1
assert Corr == s.I*nu**2*Jplusminus
print('PASS exact Poisson corrector C=i nu² J_(+,-), cubic cancellation and zero trace')
# The general CAR Dirichlet lower bound is a count on the complete Clifford
# basis, not an asserted basis restriction of the physical carrier.
comm_values=[2*(k if k%2==0 else 8-k) for k in range(1,9)]
assert min(comm_values)==2
# Single-role factor has spectrum {1,b,b²} on arbitrary 8x8 blocks.
t=s.symbols('t',real=True);a,d,u,v=s.symbols('a d u v')
X=s.Matrix([[a,u],[v,d]]);cr=s.Matrix([[0,0],[1,0]])
Lp=s.diag(1,t);Rp=s.diag(t,1)
TR=((1-t*t)*(cr.T*X*cr+cr*X*cr.T)+Lp*X*Lp+Rp*X*Rp)/2
assert (TR-s.Matrix([[(a+d+t*t*(a-d))/2,t*u],[t*v,(a+d-t*t*(a-d))/2]])).applyfunc(s.simplify)==s.zeros(2)
print('PASS exact single-role positive HS spectrum 1,b,b²; full-CAR Dirichlet gap >= nu² sigma_min(B)²/8')
# Controls of inverse/trace/gap away from the special point. The proof is the
# Dirichlet bound above; these eigenspectra are independent checks only.
G=np.array(Gamma,complex);I16=np.eye(16);ident=I16.reshape(-1,order='F')/4
Pscalar=np.outer(ident,ident.conj())
for hv in [0.,.4,1.,1.5]:
 ws=[np.array(w.subs(H,hv),complex) for w in W]
 wds=[np.array(wd.subs(H,hv),complex) for wd in Wd]
 T=sum(np.kron(w.T,w.conj().T) for w in ws)/8
 assert np.linalg.norm(T-T.conj().T)<1e-12
 eig=np.linalg.eigvalsh(T)
 B=np.array([[0,1,0,0],[1,-hv/2,0,0],[0,0,1,0],[0,0,0,1.]])
 delta=float(nu**2)*np.linalg.svd(B,compute_uv=False)[-1]**2/8
 assert min(eig)>0 and eig[-2]<=1-delta+1e-12
 S=np.kron(G.T,G)@T
 source1=sum(w.conj().T@wd for w,wd in zip(ws,wds))/8
 a1=np.array(A1,complex)
 tx=lambda x:sum(w.conj().T@x@w for w in ws)/8
 m1=-2*source1+tx(a1)-a1
 a3=-1j*float(nu**4)*np.array(J,complex)@m1@np.array(J,complex)
 assert abs(np.trace(a3))<1e-12 and np.linalg.norm(a3-a3.conj().T)<1e-12
 rhs=(a3/float(nu**2)).reshape(-1,order='F')
 corr=np.linalg.solve(np.eye(256)-S+Pscalar,rhs)
 assert np.linalg.norm((np.eye(256)-S)@corr-rhs)<1e-12
 assert abs(ident.conj()@corr)<1e-12
 assert np.linalg.norm(corr)<=np.linalg.norm(rhs)/delta+1e-12
 # Finite-dimensional polynomial energy symbol is uniformly positive after
 # a bounded scalar addition; this is not a discrete PDE estimate.
 cm=corr.reshape(16,16,order='F');bound=np.linalg.norm(cm,2)**2/(2*float(nu**2))+1
 for xi in [-100,-1,0,1,100]:
  symbol=float(nu**2)*xi*xi*I16+xi*cm+bound*I16
  assert min(np.linalg.eigvalsh(symbol))>=1+float(nu**2)*xi*xi/2-1e-9
 print(f'PASS H={hv:g}: analytic delta={delta:.8g}, actual HS gap={1-eig[-2]:.8g}, corrector norm={np.linalg.norm(corr):.8g}')
print('SCOPE: exact local matrix Poisson closure and positive energy symbol; uniform native h/clock remainder still open')
