"""Independent reconstruction of the exact six-face/N1 CQ 42-source owner,
for a posteriori inclusion tests. Not a new native or selected physical action.
"""
import numpy as np
from itertools import combinations
from scipy.linalg import expm
from scipy.optimize import brentq, root
from scipy.special import erfi
from math import sqrt,pi

ETA=np.diag([1.,-1.,-1.,-1.])
PAIRS=list(combinations(range(4),2))
G2=np.array([ETA[a,a]*ETA[b,b] for a,b in PAIRS])
STARMAP={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
         (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
STAR=np.zeros((6,6))
for a,(b,sgn) in STARMAP.items():STAR[PAIRS.index(b),PAIRS.index(a)]=sgn
I=np.eye(4);L=[]
for i in (1,2,3):
 X=np.zeros((4,4));X[0,i]=X[i,0]=1;L.append(X)
for i,j in ((1,2),(1,3),(2,3)):
 X=np.zeros((4,4));X[i,j]=1;X[j,i]=-1;L.append(X)
SGNS={}
for r,s in PAIRS:
 seq=[r,s]+[a for a in range(4) if a not in (r,s)]
 SGNS[r,s]=(-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
KAPPA=23.41640675188407497289558
P=(sqrt(5)-1)/2; Z=2**-20; LP=np.log(1/P)

def clock(r): return np.sqrt(np.pi/2)*(erfi(r/np.sqrt(2))-erfi(1/np.sqrt(2)))
def radius(t):return brentq(lambda r:clock(r)-t,.5,1.6,xtol=1e-14)
def golden_curve(r): return np.sqrt(r)*np.exp(-r*r/4),(1-r**-2)/2,np.exp(-r*r/4)/np.sqrt(r)
def comm(x,y):return np.sinh(x)*np.sinh(y)*(1-(np.cosh(x)-1)*(np.cosh(y)-1)/2)

def make_slab(n=2):
 ts=np.linspace(clock(1.),clock(1.2),n+1);h=float(ts[1]-ts[0]);amp=(2*KAPPA)**-.5
 k1=golden_curve(1.)[1];nodes=[];psi=np.zeros((n+1,2))
 for j in range(n):
  r=radius(ts[j]);rn=radius(ts[j+1]);A,_,k2=golden_curve(r);k2n=golden_curve(rn)[2]
  S2=np.sinh(h*(k2n-k2));C12=comm(h*k1,h*k2);C22=comm(h*k2,h*k2)
  def equations(z):
   X,R=z;return [(2*R*C12+C22/X)/h**2-X,(2*R*S2+X*C22)/h**2+X**3]
  solved=root(equations,[A,r],tol=1e-11)
  X,R=solved.x
  assert max(abs(np.array(equations(solved.x))))<1e-9
  k1next=k1+np.arcsinh(-(S2/X+X*C12)/R)/h
  U=np.array([I]+[expm(h*k*L[a]) for a,k in enumerate((k1,k2,k2))])
  nodes.append(dict(e=np.diag([X,1/X,R,R]),U=U,v=np.array([[amp*X**2,0,0,0],[0,amp,0,0]])))
  psi[j+1,0]=psi[j,0]+h*amp*X**2;k1=k1next
 last=np.array([I]+[expm(h*k*L[a]) for a,k in enumerate((k1,golden_curve(1.2)[2],golden_curve(1.2)[2]))])
 nodes.append(dict(e=np.diag([1,1,1.2,1.2]),U=last,v=np.zeros((2,4))))
 return h,nodes,psi

def wv(f,q,rho=1,tau=.05):
 x=-tau*f/rho;y=tau*q/rho
 def dat(x,y):
  E=P*P*(1+x);ell=4*E*(1-E)
  b=P-P*P*y;B=4*b*b*(1-b*b)
  A=ell+(1-ell)*B
  r=Z*(A+B)-Z*Z*A*B
  ellx=4*P*P*(1-2*E)
  rx=Z*(1-Z*B)*ellx*(1-B)
  By=-8*P*P*b*(1-2*b*b)
  ry=Z*((1-Z*A)*By+(1-Z*B)*(1-ell)*By)
  hp=np.log((1-r)/r)/LP
  return hp*rx,hp*ry
 den=dat(0,0)[0];a,b=dat(x,y)
 return a/den,-b/den

def wedge(a,b):return np.array([a[i]*b[j]-a[j]*b[i] for i,j in PAIRS])
def bvec(F):
 T=F@ETA
 return np.array([T[i,j] for i,j in PAIRS])
def facelist(nodes,j,r,s):
 Uj=nodes[j]['U'];nxt=nodes[j+1]['U']
 return ((j,r,False,Uj[r]),(j+1 if r==0 else j,s,False,nxt[s] if r==0 else Uj[s]),
         (j,r,True,np.linalg.inv(Uj[r])),(j,s,True,np.linalg.inv(Uj[s])))

def full_source(nodes,h,rhos=None,tau=.05):
 n=len(nodes);Ee=np.zeros((n,4,4));EU=np.zeros((n,4,6));EG=np.zeros((n,2));qlist=[];flist=[];wlist=[];vlist=[]
 for j in range(n-1):
  e=nodes[j]['e'];volume=0.;epart=np.zeros((4,4));upart=np.zeros((n,4,6))
  for r,s in PAIRS:
   factors=facelist(nodes,j,r,s);A,B,invA,invB=[f[3] for f in factors]
   prod=[I,A,A@B,A@B@invA,A@B@invA@invB];Pmat=prod[-1];Pinv=np.linalg.inv(Pmat)
   R=(Pmat-Pinv)/2;u,v=[i for i in range(4) if i not in (r,s)]
   beta=wedge(e[:,u],e[:,v]);coeff=SGNS[r,s]*(beta*G2)@STAR/h**2
   volume+=coeff@bvec(R)
   for a in range(4):
    va=np.zeros(4);va[a]=1.;jet=STAR@bvec(R)
    epart[a,u]+=SGNS[r,s]*(wedge(va,e[:,v])*G2)@jet/h**2
    epart[a,v]+=SGNS[r,s]*(wedge(e[:,u],va)*G2)@jet/h**2
   suffix=[None]*5;suffix[4]=I
   for t in range(3,-1,-1):suffix[t]=factors[t][3]@suffix[t+1]
   for t,(site,axis,invmat,Ufac) in enumerate(factors):
    for k,X in enumerate(L):
     dF=-Ufac@X if invmat else X@Ufac
     dP=prod[t]@dF@suffix[t+1]
     dR=(dP+Pinv@dP@Pinv)/2
     upart[site,axis,k]+=coeff@bvec(dR)
  rho=1 if rhos is None else rhos[j]
  g=e.T@ETA@e;gg=np.linalg.inv(g);pp=nodes[j]['v'];q=sum(v@gg@v for v in pp)
  w,vv=wv(volume,q,rho,tau)
  Ee[j]+=w*epart;EU+=w*upart
  currents=gg@pp.T
  for a in range(4):
   for mu in range(4):
    Ee[j,a,mu]+=vv*(-2)*sum((ETA@e@currents[:,i])[a]*currents[mu,i] for i in range(2))
  for i in range(2):
   value=2*vv*currents[0,i]/h
   EG[j,i]-=value;EG[j+1,i]+=value
  qlist.append(q);flist.append(volume);wlist.append(w);vlist.append(vv)
 return dict(e=Ee,U=EU,psi=EG,f=np.array(flist),q=np.array(qlist),w=np.array(wlist),v=np.array(vlist))

def problem(weights=(1.,1.)):
 h,base,psi=make_slab(2);amp=(2*KAPPA)**-.5
 def fields(z):
  nodes=[dict(e=c['e'].copy(),U=c['U'].copy(),v=c['v'].copy()) for c in base]
  ps=psi.copy();x=z[:42];nodes[1]['e']+=x[:16].reshape(4,4)
  for r in range(4):
   generator=sum(x[16+6*r+k]*L[k] for k in range(6));nodes[1]['U'][r]=expm(h*generator)@nodes[1]['U'][r]
  ps[1]+=x[40:42]
  for j in range(2):
   nodes[j]['v'][:]=0;nodes[j]['v'][0,0]=(ps[j+1,0]-ps[j,0])/h
   nodes[j]['v'][1,0]=(ps[j+1,1]-ps[j,1])/h;nodes[j]['v'][1,1]=amp
  return nodes
 def euler(z,detail=False):
  nodes=fields(z);s=full_source(nodes,h,weights,.05)
  residual=np.r_[s['e'][1].ravel(),(h*s['U'][1]).ravel(),h*s['psi'][1]]
  return (residual,s,nodes) if detail else residual
 return h,fields,euler

ROOT_UNIFORM=np.array([
.09276994940732128,-.00005530276219115076,.07918351028423412,.07918351028423605,
.0029637115438480694,.005861957569430607,.0006534403863364799,.0006534403863362567,
.6688617391053804,.000002383804809400516,-.029908876456385288,.004321073390941389,
.6688617391053937,.000002383804809967549,.004321073390941312,-.02990887645638443,
-.00025082195387275447,.35139138304665823,.3513913830466797,.00007416110259034022,
.00007416110258833871,5.014705842870588e-16,-.0039225288010511245,.000009661241760025315,
.000009661241759966424,-.000803648197002412,-.000803648197003844,5.997084910237858e-17,
.000014232219065981457,-.00003194980790665453,-.0011439145513916288,-9.152447602949038e-7,
.000004143085348863488,.000628097042461798,.00001423221906580788,-.0011439145513914895,
-.00003194980790664468,.000004143085348845979,-9.152447615766663e-7,-.0006280970424625247,
-.00020467664038117673,-.000024170276912649685]);assert len(ROOT_UNIFORM)==42
if __name__=='__main__':
 from scipy.optimize._numdiff import approx_derivative
 h,fields,euler=problem();r=euler(ROOT_UNIFORM)
 print('h',h,'res',np.max(abs(r)),'full norm',np.linalg.norm(r))
 J=approx_derivative(euler,ROOT_UNIFORM,method='3-point',abs_step=5e-6)
 print('svals',np.linalg.svd(J,compute_uv=False)[[0,-1]])
