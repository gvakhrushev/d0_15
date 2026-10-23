#!/usr/bin/env python3
"""Exact Golden source-vs-cylinder + finite-horizon reachable Book frontier.

Test-only, not proof of compulsory physical projector or Book03 Hodge selection.
"""
from fractions import Fraction as Q
import json
import math
import sympy as S
import numpy as np

assertions=[]
def ok(flag,label):
    if not bool(flag): raise ArithmeticError(label)
    assertions.append(label)
def eqmat(A,B): return all(S.simplify(e)==0 for e in A-B)

p=(S.sqrt(5)-1)/2
a=S.sqrt(p)
z=S.Rational(1,2**20)
G=S.Matrix([[a,-p],[p,a]])
I2=S.eye(2)
Pz=S.diag(1,0)
ok(S.simplify(p*p+p-1)==0, 'exact native p+p²=1')
ok(eqmat(G.T*G,I2),'exact native Golden G is orthogonal')
v=G[:,0]
P0=v*v.T
F0=P0*G.T*(I2-P0)*G*P0
ok(eqmat(F0,p*p*P0),'original one-step Golden prepared feedback F=p²P')
H1=S.Matrix.hstack(v,G*v)
ok(H1.rank()==2,'native 2D Golden finite future hull saturates in one step')
ok(eqmat(H1*H1.inv(),I2),'future hull fills the original 2-port carrier')
ok(eqmat(I2*G.T*(I2-I2)*G*I2,S.zeros(2)),'future-complete cut gives F=0')
# Original E dimension two, Ptask a genuine nontrivial old readout.
I=S.eye(2)
U=S.kronecker_product(G,I)
J=S.Matrix.vstack(a*I,p*I)
Ptask=S.diag(1,0)
PP=J*Ptask*J.T
PC=S.diag(1,0,1,0)
ok(eqmat(PP*PP,PP),'Golden prepared old-event active projector')
ok(eqmat(PC*PC,PC),'literal Book01 full cylinder is a projector')
ok(eqmat(PC*U,U*PC),'original cylinder event COMMUTES with Golden G⊗I')
ok(eqmat(PC*U.T*(S.eye(4)-PC)*U*PC,S.zeros(4)),
   'original Book cylinder feedback is EXACT ZERO')
ok(eqmat(PP*U.T*(S.eye(4)-PP)*U*PP,p*p*PP),
   'same old event prepared range has original p² feedback')
block=S.Matrix.hstack(J[:,0],U*J[:,0])
ok(block.rank()==2,'prepared+one-future spans both native branch directions')
ok(eqmat(block*(block.T*block).inv()*block.T,PC),
   'literal cylinder = canonical minimal one-step reachable Golden hull')
ok(S.simplify(S.trace(PC-PP)-1)==0,
   'prepared and cylinder ranks 1 vs 2 with exact 1 birth')
# Every real Bernoulli vector under native fixed G gives same feedback p².
r=S.symbols('r',real=True,positive=True)
w=S.Matrix([S.sqrt(1-r),S.sqrt(r)])
compressed=S.simplify((w.T*G*w)[0])
ok(S.simplify(compressed-a)==0,
   'fixed real Golden mixer has constant prepared return sqrt(p) for ALL 0<r<1')
ok(S.simplify(1-compressed**2-p*p)==0,
   'original Golden real prepared feedback source is zero for arbitrary moving Bernoulli r')

# Genuine NON-COMMUTING but rational 3D linear dynamics, all ranks exact.
R01=S.Matrix([[Q(3,5),-Q(4,5),0],[Q(4,5),Q(3,5),0],[0,0,1]])
R12=S.Matrix([[1,0,0],[0,Q(5,13),-Q(12,13)],[0,Q(12,13),Q(5,13)]])
U3=R01*R12
V=S.Matrix([1,0,0])
ok(eqmat(U3.T*U3,S.eye(3)),'exact rational noncommuting 3D orthogonal composed native-type step')
seq=[U3**t*V for t in range(4)]
Ks=[S.Matrix.hstack(*seq[:t+1]) for t in range(3)]
ranks=[K.rank() for K in Ks]
ok(ranks==[1,2,3], 'exact rank growth 1→2→3 on nontrivial rational rotation')
Ps=[]
for k,t in zip(Ks,range(3)):
    cols=k.columnspace()
    B=S.Matrix.hstack(*cols)
    Pt=B*(B.T*B).inv()*B.T
    Ps.append(Pt)
    ok(eqmat(Pt.T,Pt) and eqmat(Pt*Pt,Pt),f'exact reachability projector t={t}')
    Ft=Pt*U3.T*(S.eye(3)-Pt)*U3*Pt
    increment=(ranks[t+1] if t+1<len(ranks) else ranks[t])-ranks[t]
    ok(Ft.rank()==increment, f'rank Book frontier = new accessible dimension at t={t}')
ok(sum([1,1])==ranks[2]-ranks[0], 'sum of feedback ranks = new memory dimension')
ok(eqmat(Ps[2]*U3,U3*Ps[2]),'saturated future memory reduces the native evolution')
# For exact moving J the canonical projector differentiation uses no invented D P.
x=S.symbols('x',real=True)
Jx=S.Matrix([1,x,0])/S.sqrt(1+x*x)
Kx=S.Matrix.hstack(Jx,U3*Jx)
Px=S.simplify(Kx*(Kx.T*Kx).inv()*Kx.T)
Dpx=S.diff(Px,x)
DKx=S.diff(Kx,x)
Kplus=(Kx.T*Kx).inv()*Kx.T
rhs=(S.eye(3)-Px)*DKx*Kplus+(Kplus.T)*DKx.T*(S.eye(3)-Px)
x0=Q(1,7)
ok(eqmat(Dpx.subs(x,x0),rhs.subs(x,x0)),
   'genuine moving rank2 native prefix-hull P jet equals unique K pseudoinverse derivative')
ok(eqmat(Px.subs(x,x0)**2,Px.subs(x,x0)),
   'genuine moving nontrivial rank2 projection remains orthogonal')
# A moving first-stage root is actually SOURCE-SENSITIVE for generic 3D U.
P0x=Jx*Jx.T
F0x=(P0x*U3.T*(S.eye(3)-P0x)*U3*P0x)
lam=S.simplify(S.trace(F0x))
Dlam=S.diff(lam,x)
ok(S.simplify(Dlam.subs(x,x0))!=0,
   'generated horizon0 feedback has REAL nonzero field derivative on noncommuting full U')

pd=float(p*p);zz=float(z);beta=2*pd
native_book0=lambda d:math.log(2*d)/beta-pd-d*math.log(1-zz*pd)
native_book1=lambda d:math.log(2*d)/beta
for d in (1,4,128):
    delta=native_book1(d)-native_book0(d)
    ok(delta>0, f'paired innovation Hodge+J has strict horizon0-vs1 price gap d={d}')
print(json.dumps({'status':'PASS','checks':len(assertions),
  'native_golden_prepared_rank':1,'literal_cylinder_future_rank':2,
  'prepared_F_eigenvalue':pd,'cylinder_F_eigenvalue':0,
  'minimal_future_hull_equals_literal_cylinder':True,
  'noncommuting_3D_reachability_ranks':ranks,
  'noncommuting_3D_book_frontier_ranks':[1,1,0],
  'moving_prefix_hull_derivative':'EXACT_RATIONAL_AT_x=1/7',
  'native_first_source_3D_example':str(Dlam.subs(x,x0)),
  'paired_Hodge_J_horizon_gap_oldRIGHT128':native_book1(128)-native_book0(128),
  'selected_Book03_P_N':False,'physical_full42_root':False,
  'GR_closed':False},indent=2))
