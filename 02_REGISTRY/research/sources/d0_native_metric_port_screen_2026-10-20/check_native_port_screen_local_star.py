#!/usr/bin/env python3
"""Exact native Golden port-cost blind 3-plane and old G2/STAR mixed symbol.

Companion full128 literal log-score replay: check_original_3_history_screen_likelihood.py
LOCAL finite Fourier symbol, NOT whole periodic Einstein Euler or Book price.
"""
import sympy as s
from itertools import combinations
p=(s.sqrt(5)-1)/2; nu=s.Rational(3,5);eta=s.diag(1,-1,-1,-1)
phase=[s.I,s.I,-1,-s.I]
k=s.Matrix([z-1 for z in phase])
N=s.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
            [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
def sym(v):
 M=s.zeros(4);j=0
 for a in range(4):
  for b in range(a,4):M[a,b]=M[b,a]=v[j];j+=1
 return M
Qs=[sym(N[:,i]) for i in range(3)]
assert all(Q*k==s.zeros(4,1) for Q in Qs)
q=s.symbols('q:10',real=True);Q=sym(s.Matrix(q))
A=s.Matrix([[s.diff(s.re((Q*k)[i]),v) for v in q] for i in range(4)]
 +[[s.diff(s.im((Q*k)[i]),v) for v in q] for i in range(4)])
assert A.rank()==7 and A*N==s.zeros(8,3)
G=s.Matrix(3,3,lambda i,j:s.re((Qs[i]*eta*k).conjugate().dot(Qs[j]*eta*k)))
assert G==s.Matrix([[16,-24,8],[-24,56,-32],[8,-32,24]])
assert G.rank()==2 and G*s.ones(3,1)==s.zeros(3,1)
ell=s.Matrix([0,1,-1,1])
Qstar=sum(Qs,s.zeros(4));assert Qstar==ell*ell.T
assert Qstar*eta*k==s.zeros(4,1)
t=s.symbols('t',real=True);F=s.eye(4)+t*eta*Qstar
assert F.T*k==k
assert s.simplify(F.T*eta*F-(eta+(2*t-3*t*t)*Qstar))==s.zeros(4)
port=2+p**3*nu**2/32*s.expand_complex((F.T*k).conjugate().dot(F.T*k))
assert s.simplify(port-2-10*p**3*nu**2/32)==0

pairs=list(combinations(range(4),2));ix={v:i for i,v in enumerate(pairs)}
G2=s.diag(*[eta[a,a]*eta[b,b] for a,b in pairs]);star=s.zeros(6)
for x,y,z in [((0,1),(2,3),-1),((0,2),(1,3),1),
              ((0,3),(1,2),-1),((1,2),(0,3),1),
              ((1,3),(0,2),-1),((2,3),(0,1),1)]:
 star[ix[y],ix[x]]=z
assert star*star==-s.eye(6)
def E(a,b):return s.eye(4)[:,a]*s.eye(4)[:,b].T
lor=[E(0,i)+E(i,0) for i in (1,2,3)]+[
 E(1,2)-E(2,1),E(1,3)-E(3,1),E(2,3)-E(3,2)]
def vec(X):return s.Matrix([(X*eta)[i,j] for i,j in pairs])
def wed(u,v):return s.Matrix([u[i]*v[j]-u[j]*v[i] for i,j in pairs])
M=[]
for Q in Qs:
 h=eta*Q;out=[]
 for role in range(4):
  for X in lor:
   acc=0
   for face in pairs:
    u,v=[i for i in range(4) if i not in face]
    seq=list(face)+[u,v]
    sign=(-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
    dB=wed(h[:,u],s.eye(4)[:,v])+wed(s.eye(4)[:,u],h[:,v])
    C=s.zeros(4)
    if role==face[0]:C+=(1-phase[face[1]])*X
    if role==face[1]:C+=(phase[face[0]]-1)*X
    acc+=sign*(dB.T*G2*star*vec(C))[0]
   out.append(s.simplify(acc))
 M.append(out)
M=s.Matrix(M)
assert M.rank()==3 and (s.ones(1,3)*M)[1]==-6
print('PASS 3d real metric port-first-jet screen, native port quadratic rank2')
print('PASS Qstar=ell ell^T remains EXACTLY port-blind at finite t')
print('PASS original local six-face G2/STAR mixed coframe-link symbol rank3')
print('GR_closed=false; physical Cost-Info / 16-site Euler / refinement open')
