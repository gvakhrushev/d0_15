#!/usr/bin/env python3
"""Exact nonintegrable observer metric with Riemannian flat record source.
No native physical-action or joint-stationarity claim.
"""
import json,hashlib
from pathlib import Path
import sympy as S
x,k=S.symbols('x k',real=True)
coords=S.symbols('t'),x,S.symbols('y'),S.symbols('z')
c,si=S.cos(k*x),S.sin(k*x)
u=S.Matrix([c,0,si,0])
G=S.eye(4)
g=2*u*u.T-G
checks=[]
def eq(a,b,msg):
 if isinstance(a,S.MatrixBase): good=all(S.trigsimp(S.simplify(v))==0 for v in a-b)
 else:good=S.trigsimp(S.simplify(a-b))==0
 if not good:raise ArithmeticError(msg+' '+str(a-b))
 checks.append(msg)
eq((u.T*u)[0],1,'observer_G_unit')
eq(g*g,S.eye(4),'Lorentz_reflection_inverse_same_matrix')
eq(S.det(g),-1,'Lorentz_signature_volume_exact')
# true G-orthonormal spatial basis, its mixed observer derivative C_12=k
E1=S.Matrix([0,1,0,0]);E2=S.Matrix([-si,0,c,0]);E3=S.Matrix([0,0,0,1]);esp=[E1,E2,E3]
eq(S.Matrix(3,3,lambda i,j:(esp[i].T*esp[j])[0]),S.eye(3),'orthonormal_spatial_moving_frame')
C3=S.Matrix(3,3,lambda i,j:S.trigsimp((esp[j].T*E1)[0]*(esp[i].T*S.diff(u,x))[0]))
# above derivative along spatial e_i: e_i^x ∂_x u, projection along e_j
C3=S.Matrix(3,3,lambda i,j:S.trigsimp(esp[i][1]*(esp[j].T*S.diff(u,x))[0]))
assert C3==S.Matrix([[0,k,0],[0,0,0],[0,0,0]])
checks.append('all_nine_spatial_C_exact_nonzero_one_twisting_entry')
theta=S.trace(C3)
qobs=S.expand(theta**2-S.trace(C3.T*C3))
eq(qobs,-k*k,'full_CAR_twist_invariant_negative_k2')
eq(theta,0,'observer_expansion_zero')
# u-flat ^ du-flat has coefficient k dt^dx^dy; Frobenius FAIL for k nonzero.
wedgeF=S.trigsimp(u[0]*S.diff(u[2],x)-u[2]*S.diff(u[0],x))
eq(wedgeF,k,'nonintegrable_observer_frobenius_threeform_nonzero')
# Independent direct four-dimensional Ricci from g, no formula from D0 memo imported.
Gamma=[[[S.trigsimp(sum(g[a,b]*(S.diff(g[b,d],coords[c0])+S.diff(g[b,c0],coords[d])-S.diff(g[c0,d],coords[b]))/2 for b in range(4))) for d in range(4)] for c0 in range(4)] for a in range(4)]
Ric=S.zeros(4)
for b in range(4):
 for d in range(4):
  Ric[b,d]=S.trigsimp(sum(S.diff(Gamma[a][b][d],coords[a])-S.diff(Gamma[a][b][a],coords[d])+sum(Gamma[a][a][c0]*Gamma[c0][b][d]-Gamma[a][d][c0]*Gamma[c0][b][a] for c0 in range(4)) for a in range(4)))
RicTarget=S.zeros(4);RicTarget[1,1]=2*k*k
eq(Ric,RicTarget,'direct_full_Ricci_only_xx_2k2')
Rscalar=S.trigsimp(sum(g[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
eq(Rscalar,-2*k*k,'direct_4D_Lorentz_scalar_negative_twice_twist')
Einstein=Ric-S.Rational(1,2)*Rscalar*g
eq(Einstein,k*k*g+2*k*k*E1*E1.T,'full_ten_symmetric_Einstein_nonzero_winding_source')
eq(Rscalar,2*qobs,'same_one_record_twist_car_reconstructs_Ricci_scalar_exact')
eq(S.diff(Rscalar,k),S.diff(2*qobs,k),'same_actual_first_source_k')
result={'scope':'exact Lorentz geometry: flat G, nonintegrable twist u, full nonzero Ricci and Einstein, NOT native stationary',
 'checks_count':len(checks),'check_labels_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),
 'positive_metric_scalar':0,'observer_C_spatial':'C12=k, all others zero',
 'Frobenius_3form_coefficient':'k',
 'observer_quad':'-k^2', 'Lorentz_R':'-2k^2',
 'Ricci':'Ric_xx=2k^2, all other Ric=0',
 'Einstein':'G_munu=k^2*g_munu+2k^2 dx_mu dx_nu',
 'message':'The native positive-record heat R_G is flat yet the Lorentz metric is genuinely curved; same CAR observer bilinear supplies exact missing scalar, including twist'}
out=Path(__file__).resolve().parent/'TWIST_RESULTS.json';out.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
print('PASS',len(checks),'flat G + twisted observer gives full nonzero Lorentz Einstein curvature')
print('SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
