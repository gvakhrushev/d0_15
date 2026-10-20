import numpy as np
from scipy.linalg import eigh
from price_equivalence2_smooth import C,I,N,nu,ku,root

def make(L=8,amp=.4):
 h=1/L;xs=np.arange(L)*h;H=amp*np.sin(2*np.pi*xs);K=(H-np.roll(H,1))/(2*h);dim=16*L
 cs=[np.tile(nu*C[1],(L,1,1)),nu*(np.tile(C[0],(L,1,1))-H[:,None,None]*C[1]/2),np.tile(nu*C[2],(L,1,1)),np.tile(nu*C[3],(L,1,1))]
 lift=np.array([I+h*k*N+(h*k)**2*(N@N)/2 for k in K]);ps=[cs[0]@lift*np.exp(1j*ku*h),cs[1],cs[2],cs[3]]
 pp=[];cc=[]
 for r in range(4):
  p=np.zeros((dim,dim),complex);c=np.zeros_like(p)
  for x in range(L):
   p[16*x:16*x+16,16*((x+1)%L if r==2 else x):16*((x+1)%L if r==2 else x)+16]=ps[r][x]
   c[16*x:16*x+16,16*x:16*x+16]=cs[r][x]
  pp.append(p);cc.append(c)
 d=sum(p-c for p,c in zip(pp,cc))/h;D=d+d.T.conj();Delta=D@D
 def blockroot(m):
  out=np.zeros_like(m)
  for x in range(L):out[16*x:16*x+16,16*x:16*x+16]=root(m[16*x:16*x+16,16*x:16*x+16])
  return out
 W=[]
 for p,c in zip(pp,cc):
  W += [p,p.T.conj(),blockroot(np.eye(dim)-p@p.T.conj()),blockroot(np.eye(dim)-p.T.conj()@p),c,c.T.conj(),blockroot(np.eye(dim)-c@c.T.conj()),blockroot(np.eye(dim)-c.T.conj()@c)]
 TDelta=sum(w@Delta@w.T.conj() for w in W)/16
 A=D@TDelta@D-Delta@Delta
 vals,vecs=eigh(Delta);lam=4*nu**2*np.sin(ku*h/2)**2/h**2
 mask=abs(vals-lam)<1e-9;E=vecs[:,mask]; gap=min(abs(vals[~mask]-lam))
 assert sum(mask)==8
 assert gap>.05
 proj=E@E.T.conj();compressed=E.T.conj()@A@E
 ac,us=eigh(compressed)
 assert min(ac)>.005
 J=np.zeros((dim,4),complex)
 for x in range(L):
  for j,m in enumerate([0,2,13,15]):J[16*x+m,j]=1/np.sqrt(L)
 print('L',L,'λ',lam,'multiplicity',sum(mask),'gap',gap,'eigA',ac.tolist())
 print('A quartet=',np.real_if_close(J.T.conj()@A@J))
 assert np.linalg.norm((J.T.conj()@A@J)[:2,2:])<1e-11
 print('offdiagA quartet low-high',np.linalg.norm((J.T.conj()@A@J)[:2,2:]))
 assert np.linalg.norm((proj-J[:,:2]@J[:,:2].T.conj())@A@J[:,:2])<1e-10
 print('low outside SAME eigencluster',np.linalg.norm((proj-J[:,:2]@J[:,:2].T.conj())@A@J[:,:2]))
 print('cluster normalized pressure',np.trace(compressed).real/len(ac))
 # Corrected actual two-round price, all original effects and clock retained.
 p=(np.sqrt(5)-1)/2;eps=p*p*h*h/64;c=h*h/256
 Q=Delta-c*Delta@Delta
 TQ=sum(w@Q@w.T.conj() for w in W)/16
 LQ=D@TQ@D-(Delta@Q+Q@Delta)/2
 H_eff=Delta+p**3*eps*(2*Q+eps*LQ)
 ev,uv=eigh(H_eff)
 # Original whole λ cluster selected by its small relative perturbation.
 near=abs(ev-(lam+2*p**3*eps*(lam-c*lam*lam)))<gap/4
 assert sum(near)==8
 Enew=uv[:,near];rho=Enew@Enew.T.conj()/sum(near)
 assert np.linalg.norm(H_eff@rho-rho@H_eff)<1e-10
 assert np.linalg.norm(Enew@Enew.T.conj()-proj)<1e-8
 print('two-round corrected full fixedRIGHT stationarity',np.linalg.norm(H_eff@rho-rho@H_eff),'rank',sum(near),'projector shift',np.linalg.norm(Enew@Enew.T.conj()-proj))
 return vals,E,A,D
if __name__=='__main__':
 for L in (8,16,32):make(L)
