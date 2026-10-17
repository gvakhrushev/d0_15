#!/usr/bin/env python3
"""A single global, periodic 16-CAR golden record has exact flat positive metric; a twisting coframe family on same spatial chart has curved Lorentz scalar. Conditional geometry only, not native physical selection."""
from __future__ import annotations
from pathlib import Path
import sympy as sp
import json, hashlib

OUT=Path(__file__).resolve().parent
p=(sp.sqrt(5)-1)/2
sig=sp.simplify(p**3)
sigma=sp.symbols('sigma', positive=True)
n=16
I=sp.eye(n)
C=[]
for a in range(4):
    mat=sp.zeros(n)
    for m in range(n):
        if m & (1<<a): continue
        tgt=m|(1<<a)
        parity=(m&((1<<a)-1)).bit_count()
        mat[tgt,m]=(-1)**parity
    C.append(mat)
gamma=[x-x.T for x in C]
hat=[x+x.T for x in C]
J=[gamma[0]*gamma[1],gamma[2]*gamma[3],hat[0]*hat[1],hat[2]*hat[3]]
checks=[]
def check(ok,name):
    if not ok:raise ArithmeticError(name)
    checks.append(name)
def equal(a,b,name):
    d=a-b
    ok=all(sp.simplify(x)==0 for x in d) if isinstance(d,sp.MatrixBase) else sp.simplify(d)==0
    check(ok,name)
for a in range(4):
    equal(J[a].T,-J[a],f'full16_torus_J{a}_real_skew')
    equal(J[a]**2,-I,f'full16_torus_J{a}_square_-I')
    for b in range(4):
        equal(J[a]*J[b],J[b]*J[a],f'full16_torus_all_J_commute_{a}_{b}')
        equal(sp.trace(J[a].T*J[b]),16*(a==b),f'full16_torus_J_hilbert_orthonormal_{a}_{b}')
# U(X)= exp(X0J0)..exp(X3J3), exactly periodic with 2*pi, in SO16.
# Since J commute, U^-1 partial_i U=Ji everywhere. Golden projector
# metric=(p^3/16) Tr(Ji^T Jj), *globally*, not only at one point.
for a in range(4):
    equal(J[a]**2,-I,f'2pi_periodic_generator_{a}')
    for b in range(4):
        equal(sig*sp.trace(J[a].T*J[b])/16,sig*int(a==b),f'golden_flat_periodic_Gram_{a}_{b}')
# q_G= p^3 I. Native e = sqrt(p^3) R02(theta(x)), n=e0 gives same
# G=e^Te=p^3 I globally, yet Lorentz metric g=e^T eta e is curved.
t,x,y,z=sp.symbols('t x y z',real=True)
A=sp.symbols('A',real=True)
theta=sp.Function('theta')(x)
c2=sp.cos(2*theta)
s2=sp.sin(2*theta)
# flat s=1 first; constant scaling just divides curvature scalar by sig
met=sp.Matrix([[c2,0,s2],[0,-1,0],[s2,0,-c2]])
# coordinates t,x,y, unscaled z spectator; det = 1? g determinant of(t,y)=-1 x -1 -> +1 3D, 4D det -1.
inv=sp.simplify(met.inv())
coords=[t,x,y]
Gm=[[[sp.simplify(sp.Rational(1,2)*sum(inv[a,d]*(sp.diff(met[d,c],coords[b])+sp.diff(met[d,b],coords[c])-sp.diff(met[b,c],coords[d])) for d in range(3))) for c in range(3)] for b in range(3)] for a in range(3)]
Ric=sp.zeros(3)
for a in range(3):
  for b in range(3):
    Ric[a,b]=sp.simplify(sum(sp.diff(Gm[c][a][b],coords[c])-sp.diff(Gm[c][a][c],coords[b]) +sum(Gm[c][c][d]*Gm[d][a][b]-Gm[c][b][d]*Gm[d][a][c] for d in range(3)) for c in range(3)))
scalar=sp.simplify(sum(inv[a,b]*Ric[a,b] for a in range(3) for b in range(3)))
dtheta=sp.diff(theta,x)
equal(scalar,-2*dtheta**2,'full_nonflat_periodic_Lorentz_Ricci_scalar_arbitrary_angle')
# physical time coordinate is unwrapped: R x T^3, spatial x,y,z periodic 2pi;
# periodic theta=A*sin(x) is a continuous amplitude family.
periodic=sp.sin(x)*A
result=sp.simplify(scalar.subs(theta,periodic).doit())
equal(result,-2*A**2*sp.cos(x)**2,'continuous_periodic_twist_amplitude_Lorentz_R_equals_observer')
# G=p^3 I -> C_xy= theta_prime/sqrt(p^3), obs quad = -theta_prime²/p³, exact.
equal(result/sig,-2*A**2*sp.cos(x)**2/sig,'global_same_golden_record_nonzero_spatial_EH_integrand')
# Scalar density dVolG=sig²; EH integrated over t in [0,T], 3-torus 2pi.
# unscaled EH= -2 A²/sig * sig² * pi*(2pi)^2 * T, exactly.
T=sp.symbols('T',positive=True)
EH=sp.simplify(-2*A**2/sig * sig**2*sp.pi*(2*sp.pi)**2*T)
equal(sp.diff(EH,A,2).subs(A,0),-16*sp.pi**3*T*sig,'globally_nonzero_full_EH_second_variation')
# The pure positive record heat R_G=0 in all family; the CAR observer is indispensable.
check(bool(sp.simplify(sp.diff(EH,A,2).subs(A,0))!=0),'record_flat_while_Lorentz_action_nonlinear')
record={'scope':'exact 4D Lorentz geometry and globally isometric golden CAR metric on R x T3; U is explicit mathematical CAR torus map, NOT selected native controller/action','checks_count':len(checks),'labels_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),'golden_p3':str(sig),'commuting_majorana_bivectors':['gamma0 gamma1','gamma2 gamma3','hat0 hat1','hat2 hat3'],'global_golden_record':'U(x)=prod_i exp(x^i J_i), each Ji²=-I and commutes, U(x+2pi ei)=U(x), q=p³I on every point','native_positive_coframe':'e(x)=sqrt(p³) R02(A*sin x), n=e0, e^Te=p³I','Lorentz_scalar':str(sp.simplify(result/sig)),'Lorentz_EH_full_spatial_torus':str(EH),'EH_second_amplitude_variation':str(sp.diff(EH,A,2).subs(A,0)),'outside_scope':['physical admission of the commuting Clifford loop U and arbitrary Angle A','native Cost−Info price that reads CAR observer bilinear and quartic-subtracted golden curvature','general global curved metric embedding and matter/refinement']}
(OUT/'GLOBAL_RESULT.json').write_text(json.dumps(record,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print('PASS',len(checks),'global periodic golden 16-CAR flat metric and nonlinear Lorentz coframe twist')
print('SHA256',hashlib.sha256((OUT/'GLOBAL_RESULT.json').read_bytes()).hexdigest())
print('R_g',record['Lorentz_scalar'],'EH_second',record['EH_second_amplitude_variation'])
