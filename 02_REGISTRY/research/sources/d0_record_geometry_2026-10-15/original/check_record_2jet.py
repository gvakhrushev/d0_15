#!/usr/bin/env python3
"""Exact local kinematic fixture, not D0 physical admission or an Einstein solution."""
import json
from itertools import product
from pathlib import Path
import sympy as s

I=s.I
pauli=[s.eye(2),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
labels=[ab for ab in product(range(4),repeat=2) if ab!=(0,0)]
T={ab:s.kronecker_product(pauli[ab[0]],pauli[ab[1]]) for ab in labels}
Alabels=[(0,1),(0,2),(0,3),(1,0)]
A=[T[a] for a in Alabels]
pairs=[(m,n) for m in range(4) for n in range(m,4)]
Blabels=[ab for ab in labels if ab not in Alabels][:10]
B={mn:T[ab] for mn,ab in zip(pairs,Blabels)}
zero=s.zeros(4)

def block(u,v):
    return zero.row_join(u).col_join(v.row_join(zero))

def ip(u,v):
    # Divide the actual projector metric by p^3; d=4.
    return s.simplify(s.re(s.trace(u*v))/8)

def getB(m,n):return B[tuple(sorted((m,n)))]

def check(ok,msg):
    if not ok:raise RuntimeError(msg)

p=(s.sqrt(5)-1)/2
check(s.simplify(p+p*p-1)==0,'golden normalization')
check(s.simplify(4*p**3+p**6-1)==0,'partition identity')
U1=[I*a for a in A]
U2={(m,n):I*getB(m,n)-(A[m]*A[n]+A[n]*A[m])/2
    for m in range(4) for n in range(4)}
P1=[block(u.conjugate().T,u) for u in U1]
P2={mn:block(u.conjugate().T,u) for mn,u in U2.items()}
Normals=[block(-I*B[mn],I*B[mn]) for mn in pairs]
G=s.Matrix([[ip(x,y) for y in P1] for x in P1])
check(G==s.eye(4),'first-jet metric')
for u in P2.values():
    check(all(ip(x,u)==0 for x in P1),'normal second jet')
for m,n in product(range(4),repeat=2):
    check(U2[m,n].conjugate().T+U2[m,n]
          +U1[m].conjugate().T*U1[n]+U1[n].conjugate().T*U1[m]==s.zeros(4),
          'unitarity second derivative')
C=s.Matrix([[ip(P2[mn],q) for q in Normals] for mn in pairs])
check(C==s.eye(10),'all ten metric directions')
for l,m,n in product(range(4),repeat=3):
    check(ip(P2[l,m],P1[n])+ip(P1[m],P2[l,n])==0,'first metric derivative')
sectional={f'{m}{n}':ip(P2[m,m],P2[n,n])-ip(P2[m,n],P2[m,n])
           for m,n in pairs if m<n}
check(sum(sectional.values())*2==-6,'scalar curvature scaled by p^3')
# Deliberately remove a true second-jet direction, leaving first jets intact.
Cbad=C.copy(); Cbad[:,9]=s.zeros(10,1)
check(Cbad.rank()==9,'rank-loss negative control')
null=Cbad.T.nullspace()[0]
check(Cbad.T*null==s.zeros(10,1) and null!=s.zeros(10,1),
      'nonzero hidden source after losing one normal direction')
# A purely linear H(x) has same U(0), dU(0) but zero controlled normal source map.
P2linear={mn:block((-(A[mn[0]]*A[mn[1]]+A[mn[1]]*A[mn[0]])/2),
                 (-(A[mn[0]]*A[mn[1]]+A[mn[1]]*A[mn[0]])/2)) for mn in pairs}
Clinear=s.Matrix([[ip(P2linear[mn],q) for q in Normals] for mn in pairs])
check(Clinear==s.zeros(10),'first jets do not determine second source access')
# Exact finite Fibonacci trace-band width.
F=[0,1]
for n in range(22):F.append(F[-1]+F[-2])
for n in range(1,20):
    width=abs(s.Rational(F[n+1],F[n+2])-s.Rational(F[n],F[n+1]))
    check(width==s.Rational(1,F[n+1]*F[n+2]),'finite trace-band endpoints')
# Observer-line signature reflection has an invertible ten-slot first derivative.
t=s.Matrix([1,0,0,0]); tt=t*t.T
basis=[]
for m,n in pairs:
    V=s.zeros(4);V[m,n]=1;V[n,m]=1;basis.append(V)
images=[2*(V*tt+tt*V-tt*(t.T*V*t)[0])-V for V in basis]
Lmap=s.Matrix([[V[m,n] for V in images] for m,n in pairs])
check(Lmap.rank()==10 and Lmap*Lmap==s.eye(10),'observer reflection preserves source rank')
result={
 'scope':'KINEMATIC_ANALYTIC_GERM_AND_EXACT_FINITE_ALGEBRA_ONLY',
 'return_family':'U(x)=exp(i sum A_mu x_mu + i/2 sum B_mu_nu x_mu x_nu)',
 'A_labels':Alabels,'B_labels':Blabels,'metric':'p^3 I4',
 'normal_metric_map':'-2 p^3 I10 in mu<=nu packing',
 'second_source_map_rank':int(C.rank()),
 'sectional_curvature_times_p3':{k:str(v) for k,v in sectional.items()},
 'scalar_curvature_times_p3':'-6',
 'rank_loss_control':int(Cbad.rank()),'same_first_jet_linear_normal_map_rank':int(Clinear.rank()),
 'observer_signature_reflection_rank':int(Lmap.rank()),
 'physical_native_admission':False,'Lorentzian_metric_derived':False,
 'native_action_identified':False,'GR_closed':False,
 'checks_are_not_independent_theorems':True}
print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
