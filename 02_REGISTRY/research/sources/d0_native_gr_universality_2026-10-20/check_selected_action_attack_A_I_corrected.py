#!/usr/bin/env python3
"""Exact finite selection-gate checks for P25/P34: wrong A/C/D tests,
all-718 native clock absolute-scale blindness, and full mixed Hessian gate.
No claim physical G0 H+J+R action is selected. GR_closed=false.
"""
import math
import numpy as np
import sympy as sp

e=sp.symbols('e', real=True, positive=True)
u,y=sp.symbols('u y', real=True)
f=e**2*u**2
P=f
S=f+f**2*y
assert sp.simplify(e*sp.diff(f,e)-2*f)==0
assert sp.diff(S,y)==f**2 and sp.diff(f,y)==0
assert sp.simplify(sp.diff(S,u).subs(u,0))==0
assert sp.simplify(sp.diff(S,e).subs(u,0))==0
assert sp.simplify(sp.diff(S,y).subs(u,0))==0
assert sp.simplify(sp.diff(P,u).subs(u,0))==0
for a in (e,u,y):
 for b in (e,u,y):
  assert sp.simplify(sp.diff(S-P,a,b).subs(u,0))==0
assert sp.solve(sp.Eq(sp.diff(S,y),0),u)==[0]
print('PASS A_open not necessary: original-style homogeneous f=e²u², S=f+f²y')
print('PASS same Crit sets and exact on-shell Hessian; off-shell DS[dy]!=0')

th=sp.symbols('th', real=True)
so=sp.sin(th)
spin=sp.sin(th/2)
assert so.subs(th,sp.pi)==0 and sp.diff(so,th).subs(th,sp.pi)==-1
assert spin.subs(th,sp.pi)==1 and sp.diff(spin,th).subs(th,sp.pi)==0
assert sp.simplify(sp.diff(so,th).subs(th,-th)-sp.diff(so,th))==0
assert sp.simplify(so.subs(th,-th)+so)==0
print('PASS C/D source-grade correct: SO odd pi value 0 / derivative -1')
print('PASS Spin odd pi value 1 / derivative 0, link E even, coframe E odd')

L=sp.Matrix([[1,0,0],[0,1,0]])
proj=sp.diag(1,1,0)
Hgood=sp.Matrix([[2,3,0],[3,-1,0],[0,0,0]])
Hbad=sp.Matrix([[0,0,2],[0,0,0],[2,0,0]])
assert Hgood==proj*Hgood*proj and Hbad[2,2]==0
assert Hbad != proj*Hbad*proj and Hbad[:,2]!=sp.zeros(3,1)
assert L.T*Hgood[:2,:2]*L==Hgood
print('PASS full mixed Hessian: checking only vertical V,V can be false-positive')

N=33
parts=np.array([0]*9+[1]*11+[2]*13)
phi=(1+math.sqrt(5))/2
p=1/phi
K=np.array([[p if parts[i]!=parts[j] else 0.0 for j in range(N)] for i in range(N)])
assert np.count_nonzero(K)==718
Z2=float(np.trace(K@K))
Z3=float(np.trace(K@K@K))
K2=K@K
f2=np.zeros_like(K)
f3=np.zeros_like(K)
for i in range(N):
 for j in range(N):
  f2[i,j]=K[i,j]*K[j,i]/Z2
  f3[i,j]=K[i,j]*K2[j,i]/Z3
evals,rvecs=np.linalg.eigh(K)
lam=float(evals[-1])
r=rvecs[:,-1]
mu=K*np.outer(r,r)/(lam*np.dot(r,r))
assert abs(f2.sum()-1)<1e-12 and abs(f3.sum()-1)<1e-12
assert abs(mu.sum()-1)<1e-12
J=3*f3-2*f2-mu
assert abs(J.sum())<2e-13
Xi=Z3/(Z2*lam)
W=Z3/7722
for c in (0.93,1.03):
 M=c*K
 xc=float(np.trace(M@M@M)/(np.trace(M@M)*c*lam))
 wc=float(np.trace(M@M@M)/7722)
 assert abs(xc/Xi-1)<1e-12
 assert abs(wc/W-c**3)<1e-12
for i,j in ((0,9),(9,20),(20,0),(1,17)):
 h=1e-5
 def logxi(t):
  M=K.copy()
  M[i,j]*=math.exp(t)
  lc=float(np.linalg.eigvals(M).real.max())
  return math.log(float(np.trace(M@M@M)/(np.trace(M@M)*lc)))
 assert abs((logxi(h)-logxi(-h))/(2*h)-J[i,j])<2e-8
print('PASS all718 original J=3f3-2f2-mu=dlog Xi source, J·1=0')
print('PASS original W=Tr(K³)/7722 scales c³ while Xi fixed; J cannot set κ')
print('P25_P34_SELECTED_ACTION_GATE_A_I_CORRECTED_PASS; GR_closed=false')
