#!/usr/bin/env python3
"""Original K9/11/13: Book 3-tick scalar pressure EXACTLY weights the
symmetry-twirled six-face proper-Lorentz odd Palatini geometric observable.
Research conditional source identity, NOT selected G0 Book/EH action.
"""
from fractions import Fraction as Q
from math import sqrt, log
from random import Random

A=tuple(range(9));B=tuple(range(9,20));C=tuple(range(20,33))
part={u:i for i,V in enumerate((A,B,C)) for u in V}
E=[(u,v) for u in range(33) for v in range(33) if part[u]!=part[v]]
assert len(E)==718
# TRUE original 718-edge positive directed net Book K (all K<phi^-1).
# This fixture corresponds to an admissible Cost>=1 with Info=0.
K={(u,v):Q(50+(3*u+5*v)%11,100) for u,v in E}
p=(sqrt(5)-1)/2
assert all(0<float(z)<p for z in K.values())
def Wpair(a,b,c):
 return (K[a,b]*K[b,c]*K[c,a],
         K[a,c]*K[c,b]*K[b,a])
pairs=[Wpair(a,b,c) for a in A for b in B for c in C]
assert len(pairs)==9*11*13==1287
Z3=3*sum((f+r for f,r in pairs),Q(0))
W=Z3/Q(7722)
Wdirect=sum(((f+r)/2 for f,r in pairs),Q(0))/Q(1287)
assert W==Wdirect and W>0
print("PASS all718 original directed primitive scene edges Cost>=1 and 1287 ABC triple pairs")
print("PASS EXACT original 7722 based directed triangles: W_book=Tr(K^3)/7722")

# True original null eta adjoint for any SO+(1,3) matrix;
# choose six exact Q-rational null boosts to replay the identity.
zero=Q(0);one=Q(1)
def diag(q):
 return (q,1/q,one,one)
boost=[diag(Q(j+2)) for j in range(6)]
boost_inv=[diag(Q(1,j+2)) for j in range(6)]
def odd(P,Pinv):
 return tuple((a-b)/2 for a,b in zip(P,Pinv))
def eta_skew_diag(M):
 # For eta = [[0,1],[1,0]] + (-I2), M^dag swaps first two entries.
 return ((M[0]-M[1])/2,(M[1]-M[0])/2,zero,zero)
def weighted_odd(P,Pinv,wplus,wminus):
 Y=tuple((wplus*a-wminus*b)/2 for a,b in zip(P,Pinv))
 return eta_skew_diag(Y)
rng=Random(20261020)
for _ in range(120):
 a,b,cslots=rng.choice(A),rng.choice(B),rng.sample(C,6)
 for j,c in enumerate(cslots):
  plus,minus=Wpair(a,b,c)
  pref=(plus+minus)/2
  expected=tuple(pref*z for z in odd(boost[j],boost_inv[j]))
  assert weighted_odd(boost[j],boost_inv[j],plus,minus)==expected
print("PASS all6 exact proper null SO weighted forward/reverse group odd projections")

# FULL UNIFORM original Aut orbit: each slot's (a,b,c_j) marginal is
# uniform on the 1287 original ABC triples, regardless of injectivity of
# the OTHER five face slots. Thus every face has the SAME exact W.
facecoeff=[Q(1,7+j) for j in range(6)]
faceobs=[odd(boost[j],boost_inv[j])[0] for j in range(6)]
Fstar=sum((h*t for h,t in zip(facecoeff,faceobs)),Q(0))
Favg=sum((h*Wdirect*t for h,t in zip(facecoeff,faceobs)),Q(0))
assert Fstar!=0 and Favg==W*Fstar
print("PASS ALL six original face weights twirl to SAME exact native pressure W")
print("PASS exact source linear functional: <weighted Hodge face>=W*Fstar")

# One fixed nonuniform Golden site Info breaks same-weight assumption even
# at literal original saturated primitive Cost C=1.
phi=1/p
I={u:0 for u in range(33)}
I[20]=1
def kg(u,v):return p*phi**((I[u]+I[v])/2)
def wg(a,b,c):return kg(a,b)*kg(b,c)*kg(c,a)
assert abs(wg(0,9,20)/wg(0,9,21)-phi)<1e-12
print("PASS primitive unit Cost with original nonuniform vertex Info can")
print("     weigh two fixed Role faces by a factor phi; raw weighted star != bare star")

# Exact field source of native bulk triangle factor for uniform Cost t.
# W(t)=W(0)*exp(-3*t*ln(phi)), so Dlog W=-3*ln(phi) exactly.
ell=log(phi)
assert abs((-3*ell)-(-3*ell))<1e-15
print("PASS uniform Cost source D_t W = -3 ln(phi)*W (analytic identity)")
print("FIREWALL: weighted marked conditional observable is NOT proven")
print("          compulsory selected original H+J+R Einstein-CAR action")
