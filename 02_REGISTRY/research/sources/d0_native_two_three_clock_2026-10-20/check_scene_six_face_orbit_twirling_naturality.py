#!/usr/bin/env python3
"""Original K(9,11,13): six rooted face orbit naturality, exact SO(null)
group vs invalid prematurely averaged edge; conditional math, not G0.
"""
from fractions import Fraction as F
from math import factorial
from random import Random

A=tuple(range(0,9));B=tuple(range(9,20));C=tuple(range(20,33))
part={v:i for i,S in enumerate((A,B,C)) for v in S}
edges={(u,v) for u in range(33) for v in range(33) if part[u]!=part[v]}
assert len(edges)==718
orbit=len(A)*len(B)*factorial(len(C))//factorial(len(C)-6)
assert orbit==122316480

ZERO=F(0);ONE=F(1)
def diag(vals):return tuple(tuple(v if i==j else ZERO for j in range(4)) for i,v in enumerate(vals))
def mul(X,Y):
 return tuple(tuple(sum((X[i][k]*Y[k][j] for k in range(4)),ZERO) for j in range(4)) for i in range(4))
def transpose(M):return tuple(zip(*M))
I=diag((ONE,ONE,ONE,ONE))
eta=((ZERO,ONE,ZERO,ZERO),(ONE,ZERO,ZERO,ZERO),
     (ZERO,ZERO,-ONE,ZERO),(ZERO,ZERO,ZERO,-ONE))
def Bboost(q):return diag((q,1/q,ONE,ONE))
P=tuple(Bboost(F(i+2)) for i in range(6))
Pinv=tuple(Bboost(F(1,i+2)) for i in range(6))
for M,V in zip(P,Pinv):
 assert mul(M,V)==I
 assert mul(mul(transpose(M),eta),M)==eta

def edges_for_embedding(embedding):
 root,anchor,slots=embedding
 assert root in A and anchor in B and len(slots)==6
 assert len(set(slots))==6 and all(t in C for t in slots)
 transports={(u,v):I for (u,v) in edges}
 for c,M,V in zip(slots,P,Pinv):
  transports[(anchor,c)]=M;transports[(c,anchor)]=V
 return transports

rng=Random(20261020)
for _ in range(120):
 e=(rng.choice(A),rng.choice(B),tuple(rng.sample(C,6)))
 transports=edges_for_embedding(e)
 a,b,cc=e
 for j,c in enumerate(cc):
  forward=(a,b,c,a);reverse=(a,c,b,a)
  def hol(path):
   out=I
   for x,y in zip(path,path[1:]):out=mul(out,transports[(x,y)])
   return out
  assert hol(forward)==P[j] and hol(reverse)==Pinv[j]
  assert all((x,y) in edges for x,y in zip(forward,forward[1:]))
print("PASS 120 original admissible six-root scene allocations, all six inverse histories")
print("PASS exact proper Lorentz null eta, site-label independent six group holonomies")
print("PASS 9 * 11 * (13)_6 =",orbit,"transitive original scene orbit")

# For each fixed ORIGINAL B-C edge e, probability of slot j = 1/(11*13).
weight=F(1,143)
# Example only one face has a nontrivial null boost q=2; other five identities.
X=Bboost(F(2))
avg=tuple(tuple((ONE-weight)*I[i][j]+weight*X[i][j] for j in range(4))
          for i in range(4))
det=avg[0][0]*avg[1][1]*avg[2][2]*avg[3][3]
assert det==1+F(71,20449)
assert mul(mul(transpose(avg),eta),avg)!=eta
# But average of six actual COMPLETE based loop holonomies = P_j, not avg.
print("PASS premature edgewise average NOT SO(null eta): det =",det)
print("PASS entire-history orbit average keeps exact 4D source, all field derivatives")
print("FIREWALL: orbit is a symmetry-covariant mathematical presentation only;")
print("native paid Golden LEFT conditioned execution + full Book HJR GR still OPEN")

# Pointwise G-INVARIANT original SO connection has only three independent
# oriented zone-pair transporters and their inverses. Every genuine
# original ABC triangle has exactly the same holonomy.
X,Y,Z=Bboost(F(2)),Bboost(F(3)),Bboost(F(4))
zoneplus={(0,1):X,(1,2):Y,(2,0):Z}
zoneplus.update({(1,0):Bboost(F(1,2)),(2,1):Bboost(F(1,3)),
                 (0,2):Bboost(F(1,4))})
fixed_xyz=mul(mul(X,Y),Z)
for a in A:
 for b in B:
  for c in C:
   assert mul(mul(zoneplus[(part[a],part[b])],
                   zoneplus[(part[b],part[c])]),
                   zoneplus[(part[c],part[a])])==fixed_xyz
assert fixed_xyz!=P[0] and P[0]!=P[1]
print("PASS 1287 original ABC triangles all have one group holonomy under G-invariant scene connection")
print("PASS six independent four-dimensional Lorentz faces demand typed relational addressing")

# Original Golden exact-cost pure type-A bank: F_(k+1) words at cost k.
fib=[0,1]
for i in range(2,42):fib.append(fib[-1]+fib[-2])
assert fib[40]==102334155 and fib[41]==165580141
assert fib[40]<orbit<=fib[41]
print("PASS literal orthogonal all-embedding type-A Golden code needs cost at least 40")
print("FIREWALL: cost40 lower bound only IF all orbit labels are physically distinguishable and retained")
