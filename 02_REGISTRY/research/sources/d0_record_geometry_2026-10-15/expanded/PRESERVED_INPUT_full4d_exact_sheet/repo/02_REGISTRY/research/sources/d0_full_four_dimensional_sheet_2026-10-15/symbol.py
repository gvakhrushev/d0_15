from itertools import combinations
import sympy as s
PAIR=list(combinations(range(4),2)); eta=s.diag(1,-1,-1,-1)
GEN=[]
for i in (1,2,3):
 X=s.zeros(4); X[0,i]=X[i,0]=1; GEN.append(X)
for i,j in ((1,2),(1,3),(2,3)):
 X=s.zeros(4);X[i,j]=1;X[j,i]=-1;GEN.append(X)
G2=s.diag(*(eta[a,a]*eta[b,b] for a,b in PAIR));STAR=s.zeros(6)
for p,(q,sg) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),(1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items(): STAR[PAIR.index(q),PAIR.index(p)]=sg

def wedge(u,v):return s.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIR])
def symbol(E,z):
 result=s.zeros(24)
 for r,ss in PAIR:
  u,v=[i for i in range(4) if i not in (r,ss)]; seq=[r,ss,u,v]
  sg=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2))
  pairing=sg*wedge(E[:,u],E[:,v]).T*G2*STAR
  bf=s.zeros(6)
  for i,xi in enumerate(GEN):
   for j,xj in enumerate(GEN):
    yy=(xi*xj-xj*xi)*eta
    bf[i,j]=(pairing*s.Matrix([yy[a,b] for a,b in PAIR]))[0]
  roles=[r,ss,r,ss];direct=[s.S.One,z[r],-z[ss],-s.S.One];inverse=[s.S.One,1/z[r],-1/z[ss],-s.S.One]
  rf=s.zeros(4)
  for i,j in combinations(range(4),2):
   rf[roles[i],roles[j]]+=direct[i]*inverse[j]/2
   rf[roles[j],roles[i]]-=inverse[i]*direct[j]/2
  result+=s.kronecker_product(rf,bf)
 return result.applyfunc(s.expand).T
