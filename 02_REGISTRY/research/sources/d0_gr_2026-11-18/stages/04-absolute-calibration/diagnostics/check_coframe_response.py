"""All 16 geometric rows of the full128, independently scaled to exact integer matrices."""
from fractions import Fraction as F
from collections import defaultdict
import numpy as np
import sympy as s

order=(0,2,3,1); ph=((0,1),(0,1),(-1,0),(0,-1))
I=np.eye(16,dtype=np.int64); O=I*0; cs=[]
for r in range(4):
 c=O.copy()
 for b in range(16):
  if not (b>>r)&1:
   c[b|(1<<r),b]=(-1)**sum((b>>k)&1 for k in order[:order.index(r)])
 cs.append(c)
walsh=np.array([[(-1)**(bin(i&j).count('1')%2) for j in range(32)] for i in range(32)],dtype=np.int64)
def pref(x,mult): return np.array([x*mult[0],x*mult[1]])
def both(raw):
 return np.tensordot(walsh,np.asarray(raw,dtype=np.int64),axes=(1,0)).reshape(64,2,16,16)
def make(role,slot):
 words=[]; jets=[]
 for r,c in enumerate(cs):
  dc=cs[slot] if r==role else O
  pr,pi=ph[r]; occ=c@c.T
  l=5*I-occ; h=4*I+occ
  def rootj(diag,rhs):
   den=diag.diagonal()[:,None]+diag.diagonal()[None,:]
   assert (1080%den==0).all()
   return -(1080//den)*rhs
  dl=rootj(l,dc@c.T+c@dc.T); dh=rootj(h,dc.T@c+c.T@dc)
  for atom,jet in zip(
     [(pref(3*c,(pr,pi)),pref(l,(1,0))),(pref(3*c.T,(pr,-pi)),pref(h,(1,0))),
      (pref(-3*c,(1,0)),pref(-l,(1,0))),(pref(-3*c.T,(1,0)),pref(-h,(1,0)))],
     [(pref(360*dc,(pr,pi)),pref(dl,(1,0))),(pref(360*dc.T,(pr,-pi)),pref(dh,(1,0))),
      (pref(-360*dc,(1,0)),pref(-dl,(1,0))),(pref(-360*dc.T,(1,0)),pref(-dh,(1,0)))]):
   words.extend((atom,atom));jets.extend((jet,jet))
 return both(words),both(jets)

# Each array entry has an elementary absolute bound <=32*3*360; the row
# products and 16-term sums below have absolute value < 2^45, inside int64.
rows={}; lamrows={}; primes=set()
for r in range(4):
 for t in range(4):
  base,jet=make(r,t); coeff=defaultdict(F)
  diag=(base*base).sum(axis=(1,3))
  ddiag=2*(base*jet).sum(axis=(1,3))
  # Full check of the diagonal spectra, including imaginary offdiagonals.
  for (R,J),v in zip(base,diag):
   assert np.array_equal(R@R.T+J@J.T,np.diag(v))
   assert np.array_equal(J@R.T-R@J.T,O)
  assert (ddiag[diag==0]==0).all()
  lamrows[r,t]=F(int(ddiag[0].sum()),160*11520)
  for m,dm in zip(diag[1:].ravel(),ddiag[1:].ravel()):
   if not dm or not m:continue
   mu=F(int(m),160**2)
   d=F(-int(dm),160*11520)
   for prime,exp in s.factorint(mu.numerator).items(): coeff[prime]+=d*int(exp)
   for prime,exp in s.factorint(mu.denominator).items(): coeff[prime]-=d*int(exp)
  rows[r,t]={prime:value for prime,value in coeff.items() if value};primes|=set(rows[r,t])
k0=(0,1)
D={}
for r in range(4):
 for t in range(4):
  fin={z:rows[r,t].get(z,F(0))-rows[k0].get(z,F(0))*lamrows[r,t]/lamrows[k0] for z in primes}
  D[r,t]={z:a for z,a in fin.items() if a}
  if r!=t: assert not D[r,t],(r,t,D[r,t])
assert D[0,0]==D[1,1]==D[3,3]
d=D[0,0];d2=D[2,2]
lin=lambda v:sum(s.Rational(c.numerator,c.denominator)*s.log(z) for z,c in v.items())
p=(s.sqrt(5)-1)/2
fac=p*p*s.Rational(9,640)/4
assert s.expand_log(lin(d),force=True).expand()==s.Rational(3,10)*(41*s.log(2)+16*s.log(3)-4*s.log(5)).expand() or s.simplify(lin(d)-s.Rational(3,10)*(41*s.log(2)+16*s.log(3)-4*s.log(5)))==0
print('diagonal logarithm-coefficient vectors before common p^2*(9/640)/4:',d,d2)
print('delta coeffs:',{z:d2.get(z,F(0))-d.get(z,F(0)) for z in primes if d2.get(z,F(0))!=d.get(z,F(0))})
print('numerical checks',s.N(fac*lin(d),16),s.N(fac*lin(d2),16))
def logpositive(vec):
 D=s.ilcm(*[c.denominator for c in vec.values()])
 a,b=1,1
 for z,c in vec.items():
  k=int(D*c)
  if k>0:a*=int(z)**k
  else:b*=int(z)**(-k)
 return a>b
def combo(a,b):
 return {z:a*d.get(z,F(0))+b*d2.get(z,F(0)) for z in primes}
assert logpositive(combo(1,-1)) # d2 < d
assert logpositive(combo(-18,19)) # d2 > 18d/19
print('proved exactly 18d/19<d2<d by positive integer powers of primes.')
# Exact local three-outcome reader, including its physical quiet branch.
Id=s.eye(2); X=s.Matrix([[0,1],[1,0]]); ap=s.sqrt(p)*p
reader=[ap*(Id+X),-ap*(Id-X),p**3*Id,s.zeros(2)]
se=s.simplify(4*p**3)
law=[se/2,se/2,1-se,0]
effects=[K.T*K for K in reader]
assert (sum(effects,s.zeros(2))-Id).applyfunc(s.simplify)==s.zeros(2)
for E,prob in zip(effects,law):
    assert all(s.simplify(E[i,i]-prob)==0 for i in range(2))
assert len(reader)==4 and law[-1]==0
# The archive orthogonalizes all inputs j, so the six-bit criterion is exactly
# the product of these equal diagonal tests, without a large Stinespring matrix.
q=s.symbols('q',positive=True); budget,hm=s.symbols('d H')
for n in range(1,9):
    A=sum(q**i for i in range(n)); dq=s.diff
    mean=sum((k+1)*((1-q)*q**k) for k in range(n))+n*q**n
    charge=sum((k*(2+budget)+1+budget)*((1-q)*q**k) for k in range(n))+n*(2+budget)*q**n
    assert s.expand(mean-A)==0 and s.expand(charge-A*(1+budget+q))==0
    # Coefficients of log(q), log(1-q) in the full cylinder entropy.
    logq=-sum(k*((1-q)*q**k) for k in range(n))-n*q**n
    log1q=-sum(((1-q)*q**k) for k in range(n))
    assert s.expand(logq+A*q)==0 and s.expand(log1q+A*(1-q))==0
baseq=float(se*9/640); sf=float(se); from math import log
ent=lambda v: -v*log(v)-(1-v)*log(1-v)
Hm=6*(ent(sf)+sf*log(2))
net2=56+2*baseq-(Hm-(1+2*baseq)*log(baseq)+2*baseq*log(1-baseq))/log((1+5**.5)/2)
netinf=56-(Hm-log(baseq))/log((1+5**.5)/2)
assert 2**23>100**2*3**6
assert net2>0 and netinf>0
print('PASS: full binary probe cycles, both physical bits incl. quiet/dark; finite stopped cylinders for n=1..8; C-Info gains with 54 unit stages:',net2,netinf)
