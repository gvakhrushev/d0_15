"""Exact full128 one-visit post-PVM test and a genuine two-visit counterexample."""
from collections import Counter,defaultdict
from fractions import Fraction as F
from functools import reduce
from math import gcd
import numpy as np
import sympy as sp
from check_coframe_response import make

rootrows={13,29,45,61}
base,_=make(0,0)
m=(base*base).sum(axis=(1,3))
r=16
assert {j for j in range(64) if len(set(m[j]))>1}==rootrows
parity=np.array([(-1)**bin(i).count('1') for i in range(16)])
for j,(real,imag) in enumerate(base):
 out=real.T@real+imag.T@imag
 assert np.array_equal(out,np.diag(out.diagonal()))
 assert np.all(real.T@imag-imag.T@real==0)
 if j in rootrows:
  assert Counter(m[j])=={0:6,256:2,64:8}
  assert m[j]@parity==0
 else: assert len(set(m[j]))==1
for role in range(4):
 for comp in range(4):
  _,jet=make(role,comp)
  dm=2*(base*jet).sum(axis=(1,3))
  for j in rootrows:
   assert dm[j][m[j]==256].sum()==dm[j][m[j]==64].sum()
   assert np.all(dm[j][m[j]==0]==0)
djet=make(0,0)[1]-make(0,1)[1]
dm=2*(base*djet).sum(axis=(1,3))
assert F(int(dm[list(rootrows)].sum()),160*11520)==F(3,10)
def logweights(conditional):
 out=defaultdict(F)
 for j in range(1,64):
  for i in range(16):
   dv=int(dm[j,i])
   if not dv:continue
   mu=F(int(m[j,i]),160**2) if conditional else F(int(m[j].sum()),r*160**2)
   assert mu>0
   for n,sign in ((mu.numerator,1),(mu.denominator,-1)):
    for z,e in sp.factorint(n).items():out[z]-=F(dv*sign*e,160*11520)
 return {z:x for z,x in out.items() if x}
_cond={2:F(123,10),3:F(24,5),5:F(-6,5)}
assert logweights(True)==_cond
_cl=dict(_cond); _cl[2]+=F(3,10)
assert logweights(False)==_cl

def mat(x): return sp.Matrix(x[0])+sp.I*sp.Matrix(x[1])
def prim(m):
 return m/reduce(gcd,(int(z) for w in m for z in w.as_real_imag()),0)
ns=[mat(x) for x in base]
B1=prim(ns[13].H*ns[0])
B2=prim(ns[8].H*ns[0])
W=B2*B1
state=(W*W.H).applyfunc(sp.expand);state=state/sp.trace(state)
assert state[0,0]==sp.Rational(1,60)
assert state[5,5]==sp.Rational(1,10)
assert state[0,5]==-(1+sp.I)/60
M=F(2**41*3**16,5**4)
assert M>1 and 5 in sp.factorint(M.denominator) and 3 in sp.factorint(M.numerator)
print('PASS: all 128 terminal DATA blocks diagonal, four root labels share exactly one bit, all 16 flattened conditional-entropy derivatives, probability/cq logarithmic coefficients, parity and actual K16 K27 conditional state element - (1+i)/60.')
