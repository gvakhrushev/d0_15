#!/usr/bin/env python3
"""Exact original coframe Dirac-port screen versus literal G2/STAR finite face.
Consumes actual native 3-history log-Jacobian checked independently in
check_native_full128_blank_odds.py. Reconstruction is NOT Book action selection.
"""
import sympy as sp
from itertools import combinations
p=(sp.sqrt(5)-1)/2
a=sp.sqrt(p)
nu=sp.Rational(3,5)
eta=sp.diag(1,-1,-1,-1)
ph=[sp.I,sp.I,-1,-sp.I]
k=sp.Matrix([z-1 for z in ph])
assert sp.simplify((k.conjugate().T*k)[0]-10)==0
base=sp.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
 [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
def qmatrix(column):
 Q=sp.zeros(4);index=0
 for i in range(4):
  for j in range(i,4):
   Q[i,j]=Q[j,i]=column[index];index+=1
 return Q
Qs=[qmatrix(base[:,j]) for j in range(3)]
for Q in Qs:assert all(sp.simplify(x)==0 for x in Q*k)
Qstar=Qs[0]+Qs[1]+Qs[2]
ell=sp.Matrix([0,1,-1,1])
assert Qstar==ell*ell.T
assert all(sp.simplify(x)==0 for x in Qstar*eta*k)
t=sp.symbols('t',real=True)
F=sp.eye(4)+t*eta*Qstar
assert sp.factor(F.det())==1-3*t
assert sp.simplify(F.T*eta*F-(eta+(2*t-3*t*t)*Qstar))==sp.zeros(4)
assert all(sp.simplify(x)==0 for x in F.T*k-k)
# Literal original A=hD/16, CAR anticommutator:
# A(F)^2=(nu²/256)|F^T k|² I16 at zero independent proper links.
# Original E_port1 = 4p³ A². Two complete fresh rounds,
# state/preparation-independent here because A² is scalar:
Cport=2+(p**3*nu**2/sp.Integer(32))*sp.expand_complex(
 (F.T*k).conjugate().dot(F.T*k))
assert sp.simplify(Cport-(2+10*p**3*nu**2/32))==0
# The screen is exactly three real dimensions inside symmetric ten.
qq=sp.symbols('q0:10',real=True)
Q=qmatrix(sp.Matrix(qq))
real_equations=[sp.re((Q*k)[j]) for j in range(4)]
imag_equations=[sp.im((Q*k)[j]) for j in range(4)]
screenmatrix=sp.Matrix([[sp.diff(y,x) for x in qq]
                         for y in real_equations+imag_equations])
assert screenmatrix.rank()==7
assert screenmatrix*base==sp.zeros(8,3)
# The three-score exact native raw full128 checker has already proved this J.
J=sp.Matrix([[0,-sp.Rational(4,3),0],
 [sp.Rational(16,9),-sp.Rational(125,18),sp.Rational(5,36)],
 [-16*a**3/13-sp.Rational(9,26),32*a**3/13-sp.Rational(1,2),
 -16*a**3/13-sp.Rational(145,52)]])
assert sp.simplify(J.det()+(1888*a**3+4595)/702)==0
assert all(sp.simplify(x)==0 for x in
 J*sp.ones(3,1)-sp.Matrix([-sp.Rational(4,3),-sp.Rational(181,36),
                          -sp.Rational(189,52)]))
B0=1-9*p*p/sp.Integer(320)
q_events=[sp.Rational(243,512000)*p**3*B0**2,
 sp.Rational(81,640000)*p**3*B0**2,
 sp.Rational(117,640000)*p**3*B0**2]
Fisher=J.T*sp.diag(*q_events)*J
assert sp.simplify(Fisher.det()-J.det()**2*sp.prod(q_events))==0
# Original literal old G2/STAR and extracted anti-symmetric F*bivector
pairs=list(combinations(range(4),2))
pid={ij:j for j,ij in enumerate(pairs)}
G2=sp.diag(*[eta[i,i]*eta[j,j] for i,j in pairs])
star=sp.zeros(6)
star_map={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
 (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for ij,(ab,sgn) in star_map.items():star[pid[ab],pid[ij]]=sgn
assert star*star==-sp.eye(6)
def E(i,j):return sp.eye(4)[:,i]*sp.eye(4)[:,j].T
lor=[E(0,j)+E(j,0) for j in (1,2,3)]+[
 E(1,2)-E(2,1),E(1,3)-E(3,1),E(2,3)-E(3,2)]
def biv(X):return sp.Matrix([(X*eta)[i,j] for i,j in pairs])
def wedge(u,v):return sp.Matrix([u[i]*v[j]-u[j]*v[i] for i,j in pairs])
def face_sign(pair):
 seq=list(pair)+[j for j in range(4) if j not in pair]
 return (-1)**sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
M=[]
for Qm in Qs:
 h=eta*Qm;out=[]
 for r in range(4):
  for X in lor:
   v=0
   for face in pairs:
    uu,vv=[i for i in range(4) if i not in face]
    dB=wedge(h[:,uu],sp.eye(4)[:,vv])+wedge(sp.eye(4)[:,uu],h[:,vv])
    source=sp.zeros(4)
    if r==face[0]:source+=(1-ph[face[1]])*X
    if r==face[1]:source+=(ph[face[0]]-1)*X
    v+=face_sign(face)*(dB.T*G2*star*biv(source))[0]
   out.append(sp.simplify(v))
 M.append(out)
M=sp.Matrix(M)
assert M.rank()==3
assert (sp.ones(1,3)*M)[1]==-6
M3=M[:,[0,1,5]]
assert sp.simplify(M3.det()+24-12*sp.I)==0
assert sp.simplify(J.det())!=0
# Invertible source-coordinate transfer exists uniquely:
# local old Palatini face bilinear dt^T M domega
#   = dlogodds^T (J^{-T}M) domega.
# This is just a mathematical reconstruction of an ALREADY OWNED source.
print('PASS original Dirac/Golden complete port: 3D screen and finite exact Qstar-dark metric curve')
print('PASS native 3 blank-anchored log odds: det J =',sp.factor(J.det()))
print('PASS OLD literal G2/STAR mixed face symbol rank3: det M3 =',sp.factor(M3.det()))
print('PASS source-coordinate transfer, det J^{-T}M3 = det(M3)/det(J) NONZERO')
print('FIREWALL: no physical compulsory scalar Book binding or full Einstein Euler; GR_closed=false')
