#!/usr/bin/env python3
"""Exact fixed-background stored-adjoint / null-source intersection.
No physical GR closure, no new action; consumes the already-owned projection theorem.
"""
from itertools import combinations
from sympy import Matrix, diag, eye, Rational, symbols, sqrt, simplify, factor, diff, trace, zeros
import json

checks=0

def check(ok, msg):
    global checks
    if not bool(ok):
        raise RuntimeError(msg)
    checks += 1

def eq(a,b,msg):
    if isinstance(a,Matrix):
        check(a.shape==b.shape and all(simplify(x-y)==0 for x,y in zip(a,b)),msg)
    else:
        check(simplify(a-b)==0,msg)

eta=diag(1,-1,-1,-1)
lam=Matrix([205,144,96,72])/83
tau=eta*lam
v=tau[1:4,0]
gamma=tau[0]
F=zeros(4)
F[0,0]=gamma
for i in range(3):
    F[0,i+1]=v[i]
    F[i+1,0]=v[i]
    for j in range(3):
        F[i+1,j+1]=int(i==j)+v[i]*v[j]/(gamma+1)

# Real actual regular stored-adjoint background: proper Lorentz boost F, all four own legs spatially nonzero.
eq(F*eta*F.T, eta, 'regular owner Q=F eta F^T')
eq(F.det(), 1, 'proper frame det')
eq(F[:,0], tau, 'owner future tau=F n')
eq((tau.T*eta*tau)[0],1,'tau unit and future')
for i in range(4):
    check(sum(F[i,j]**2 for j in range(1,4))>0, 'own spatial leg regular')

pairs=list(combinations(range(4),2))
def P(i,j):
    Pij=zeros(4); Pij[i,j]=Pij[j,i]=1
    return Pij

# Linearized exact owner conditions on full-support Fourier modes:
# H_rr=0, lambda^T H lambda=0. Construct the real 5D tangent basis explicitly.
pivot=(0,1)
ws=Matrix([2*lam[i]*lam[j] for (i,j) in pairs])
check(ws[0]!=0,'nonzero pivot full-support observer')
basis=[]
for i,j in pairs[1:]:
    X=P(i,j) - (lam[i]*lam[j]/(lam[0]*lam[1]))*P(*pivot)
    check(all(X[r,r]==0 for r in range(4)),'native own-leg diagonal invariant')
    eq((lam.T*X*lam)[0],0,'native observer normalization tangent')
    basis.append(X)
# index vectors of accessible offdiag slots; rank five.
M=Matrix([[X[i,j] for X in basis] for i,j in pairs])
check(M.rank()==5,'five allowed metric directions')
check((ws.T*M)==Matrix([[0]*5]),'five basis lies in weighted offdiag kernel')

# Exact nonlinear integration: vary 02, solve 01 by the real unit-tau equation;
# no arbitrary extra metric source, no forcing gravitational action.
z=symbols('z', real=True)
bz=(13824*z+205*sqrt(20736-39360*z-12073*z**2)-29520)/21289
Qz=eta + bz*P(0,1)+z*P(0,2)
eq(Qz.diagonal(),eta.diagonal(), 'all four own-edge diagonal invariants finite')
eq((tau.T*Qz.inv()*tau)[0],1,'exact nonlinear unit observer constraint')
eq(bz.subs(z,0),0,'same original field root')
eq(diff(bz,z).subs(z,0),-Rational(2,3),'actual first admitted coframe velocity')
eq(diff(bz,z,2).subs(z,0),-Rational(2665,1296),'nonlinear second observer/edge source')
H=P(0,2)-Rational(2,3)*P(0,1)
eq(Qz.diff(z).subs(z,0),H,'tangent integrates without changing own edges')
eq((lam.T*H*lam)[0],0,'tangent observer exact')

# Strong scoped no-go: none of the null rank-one coframe shears, nor scale, belongs
# to the full-support fixed-own-leg Fourier tangent image.
nulls=[Matrix([1,1,0,0]), Matrix([1,-1,0,0]), Matrix([1,Rational(3,5),Rational(4,5),0]), Matrix([1,0,0,1])]
for n in nulls:
    eq((n.T*eta*n)[0],0, 'true Lorentz null direction')
    Hnull=n*n.T
    check(any(Hnull[r,r]!=0 for r in range(4)), 'nonzero null shear violates own-edge invariants')
check(any(eta[r,r]!=0 for r in range(4)),'scale cannot be admitted on full support')

# A generic nonzero Bianchi-divergence-free Einstein-covector residual, invisible to
# ALL five allowed metric variations, yet detected by forbidden null shears.
k=Matrix([1,2,3,4])
a=eta*k
s=(lam.T*a)[0]
check(all(a[i]!=0 for i in range(4)), 'generic full-support k')
E=lam*lam.T - s*diag(*[lam[i]/a[i] for i in range(4)])
eq(E*a,zeros(4,1),'genuine covector Bianchi E Qk=0')
check(E!=zeros(4),'residual is not zero')
for X in basis:
    eq(trace(E*X),0,'source invisible to every admissible metric variation')
bn=Matrix([1,1,0,0])
eq((bn.T*E*bn)[0], Rational(209448,6889),'forbidden null source actually nonzero')
Poff=lam*lam.T-diag(*[lam[i]**2 for i in range(4)])
check(all(Poff[i,i]==0 for i in range(4)), 'offdiag extra test has zero diagonal')
check((lam.T*Poff*lam)[0]>0,'extra offdiag probe violates stored constraint')
eq(trace(E*Poff),Rational(3645929088,47458321),'single scalar probes generic residual')

# Exceptional Fourier a0=0 retains a diagonal residual invisible even to Poff.
kexc=Matrix([0,1,2,3]); aexc=eta*kexc
check(aexc[0]==0 and all(aexc[i]!=0 for i in range(1,4)),'exceptional momentum')
Eexc=diag(1,0,0,0)
eq(Eexc*aexc,zeros(4,1),'exceptional source Bianchi')
for X in basis:
    eq(trace(Eexc*X),0,'exceptional source invisible to native metric tangent')
eq(trace(Eexc*Poff),0,'one generic completion misses exceptional residual')
check((bn.T*Eexc*bn)[0]!=0,'exceptional source violates same null equation')

# Ten algebraic rank-complete positive Fourier probes, restricted to the actual 5D
# stored Lorentz tangent, cannot have rank above five.
settings=[(i,) for i in range(4)] + list(combinations(range(4),2))
R=Matrix([[sum(X[a,b] for a in S for b in S) for X in basis] for S in settings])
check(R.rank()==5,'ten Fourier readouts cannot increase five physical Euler tangent rows')
print(json.dumps({
    'status':'PASS','exact_controls':checks,'proper_native_F':[[str(F[i,j]) for j in range(4)] for i in range(4)],
    'lambda':[str(x) for x in lam], 'native_metric_tangent_dim':M.rank(),
    'nonlinear_Q_01(z)':str(bz), 'nonlinear_b_prime':'-2/3',
    'nonlinear_b_second':'-2665/1296',
    'generic_k':[1,2,3,4], 'generic_s':str(s),
    'bianchi_residual_null':str((bn.T*E*bn)[0]),
    'generic_completion_pairing':str(trace(E*Poff)),
    'exceptional_k':[0,1,2,3],'exceptional_completion_pairing':'0',
    'full_10_probe_restricted_rank':R.rank(),
    'native_null_shears_admitted':False, 'native_metric_scale_admitted':False,
    'all_GR_sources_closed':False,'original_hminus2_closed':False
},sort_keys=True,ensure_ascii=False))
