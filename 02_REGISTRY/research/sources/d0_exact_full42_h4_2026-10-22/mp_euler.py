"""High precision source evaluation on exact rational collar and Cayley Lorentz coordinates.
This is an author high-precision reconstruction; interval certification is separate.
"""
import json,sys
from pathlib import Path
from mpmath import mp
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT))
mp.dps=65
N=4;I=mp.eye(4);ETA=mp.diag([1,-1,-1,-1])
PAIRS=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
G2=[ETA[a,a]*ETA[b,b] for a,b in PAIRS]
STARMAP={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
         (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
STAR=mp.matrix(6)
for a,(b,sgn) in STARMAP.items():STAR[PAIRS.index(b),PAIRS.index(a)]=sgn
L=[]
for i in (1,2,3):
 X=mp.matrix(4);X[0,i]=X[i,0]=1;L.append(X)
for i,j in ((1,2),(1,3),(2,3)):
 X=mp.matrix(4);X[i,j]=1;X[j,i]=-1;L.append(X)
SGNS={}
for r,s in PAIRS:
 seq=[r,s]+[a for a in range(4) if a not in (r,s)]
 SGNS[r,s]=(-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
P=(mp.sqrt(5)-1)/2;Z=mp.mpf(1)/2**20;LP=mp.log(1/P)

def mx_from_rows(rows):return mp.matrix([[mp.mpf(x) for x in row] for row in rows])
def v_inv(U):return ETA*U.T*ETA
def cayley(Y):return (I-Y/2)**-1*(I+Y/2)
def build():
 info=json.loads((OUT/'rational_root_center.json').read_text())
 h=mp.mpf(info['h']);nodes=[]
 for nd in info['nodes']:
  mat=[]
  for pars in nd['lie_params']:
   Y=mp.matrix(4)
   for k in range(6):Y+=mp.mpf(pars[k])*L[k]
   mat.append(cayley(Y))
  nodes.append(dict(e=mx_from_rows(nd['e']),U=mat,v=mx_from_rows(nd['v'])))
 return h,nodes

def fields(z,h,base):
 nodes=[dict(e=nd['e'].copy(),U=[x.copy() for x in nd['U']],v=nd['v'].copy()) for nd in base]
 for a in range(4):
  for b in range(4):nodes[1]['e'][a,b]+=z[4*a+b]
 for r in range(4):
  Y=mp.matrix(4)
  for k in range(6):Y+=z[16+6*r+k]*L[k]
  nodes[1]['U'][r]=cayley(Y)*nodes[1]['U'][r]
 for a in range(2):
  nodes[0]['v'][a,0]+=z[40+a]/h
  nodes[1]['v'][a,0]-=z[40+a]/h
 return nodes

def vec_b(F):
 T=F*ETA;return mp.matrix([T[i,j] for i,j in PAIRS])
def wedge(a,b):return mp.matrix([a[i]*b[j]-a[j]*b[i] for i,j in PAIRS])
def coef(f,q,rho):
 tau=mp.mpf('0.05');x=-tau*f/rho;y=tau*q/rho
 def dat(x,y):
  E=P*P*(1+x);ell=4*E*(1-E);v=P-P*P*y;B=4*v*v*(1-v*v)
  A=ell+(1-ell)*B;r=Z*(A+B)-Z*Z*A*B
  ellx=4*P*P*(1-2*E);rx=Z*(1-Z*B)*ellx*(1-B)
  By=-8*P*P*v*(1-2*v*v)
  ry=Z*((1-Z*A)*By+(1-Z*B)*(1-ell)*By)
  hp=mp.log((1-r)/r)/LP
  return hp*rx,hp*ry
 den=dat(0,0)[0];a,b=dat(x,y)
 return a/den,-b/den

def eval_euler(z,h,base):
 nodes=fields(z,h,base);Ee=[mp.matrix(4) for _ in range(3)];EU=[mp.matrix(4,6) for _ in range(3)];EG=[mp.matrix(2,1) for _ in range(3)]
 for j in range(2):
  e=nodes[j]['e'];volume=mp.mpf(0);epart=mp.matrix(4);upart=[mp.matrix(4,6) for _ in range(3)]
  for r,s in PAIRS:
   Uj=nodes[j]['U'];Un=nodes[j+1]['U'];factors=[(j,r,False,Uj[r]),(j+1 if r==0 else j,s,False,Un[s] if r==0 else Uj[s]),(j,r,True,v_inv(Uj[r])),(j,s,True,v_inv(Uj[s]))]
   A,B,invA,invB=[f[3] for f in factors]
   prod=[I,A,A*B,A*B*invA,A*B*invA*invB];Pm=prod[-1];Pinv=v_inv(Pm)
   R=(Pm-Pinv)/2;u,v=[k for k in range(4) if k not in (r,s)]
   beta=wedge(e[:,u],e[:,v]);coeff=mp.matrix(1,6)
   weighted=mp.matrix(1,6)
   for k in range(6):weighted[0,k]=beta[k]*G2[k]
   coeff=SGNS[r,s]*weighted*STAR/h**2
   volume+=(coeff*vec_b(R))[0]
   jet=STAR*vec_b(R)
   for a in range(4):
    va=mp.matrix(4,1);va[a]=1
    x=wedge(va,e[:,v]);y=wedge(e[:,u],va)
    sumx=sum(x[k]*G2[k]*jet[k] for k in range(6))
    sumy=sum(y[k]*G2[k]*jet[k] for k in range(6))
    epart[a,u]+=SGNS[r,s]*sumx/h**2
    epart[a,v]+=SGNS[r,s]*sumy/h**2
   suffix=[None]*5;suffix[4]=I
   for t in range(3,-1,-1):suffix[t]=factors[t][3]*suffix[t+1]
   for t,(site,axis,inverse,Ufac) in enumerate(factors):
    for k,X in enumerate(L):
     dF=-Ufac*X if inverse else X*Ufac
     dP=prod[t]*dF*suffix[t+1]
     dR=(dP+Pinv*dP*Pinv)/2
     upart[site][axis,k]+=(coeff*vec_b(dR))[0]
  g=e.T*ETA*e;gg=g**-1;pp=nodes[j]['v'];currents=gg*pp.T
  q=mp.mpf(0)
  for a in range(2):q+=(pp[a,:]*gg*pp[a,:].T)[0]
  w,vv=coef(volume,q,1)
  Ee[j]+=w*epart
  for site in range(3):EU[site]+=w*upart[site]
  tmp=ETA*e*currents
  for a in range(4):
   for mu in range(4):
    Ee[j][a,mu]+=-2*vv*sum(tmp[a,i]*currents[mu,i] for i in range(2))
  for a in range(2):
   term=2*vv*currents[0,a]/h
   EG[j][a]-=term;EG[j+1][a]+=term
 return mp.matrix([Ee[1][a,mu] for a in range(4) for mu in range(4)]+[h*EU[1][r,k] for r in range(4) for k in range(6)]+[h*EG[1][a] for a in range(2)])

if __name__=='__main__':
 from time import perf_counter
 from native42 import ROOT_UNIFORM
 h,b=build();z=[mp.mpf(0)]*42;t=perf_counter()
 r=eval_euler(z,h,b);print('mp eval sec',perf_counter()-t,'r max',mp.nstr(max(map(abs,r)),35),'first',mp.nstr(r[0],30))
