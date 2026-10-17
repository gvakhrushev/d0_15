#!/usr/bin/env python3
"""Exact finite golden-cylinder 4D vs 3D curvature inclusion-exclusion.
An exact geometric readout in supplied conditional instrument class; NOT a native selected physical action.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import sympy as s
HOME=Path(__file__).resolve().parent
checks=[]
def ck(v,name):
 if v is not True and v!=s.true: raise ArithmeticError(name+': '+str(v))
 checks.append(name)
def eq(x,y,name):ck(s.factor(x-y)==0,name)
p=(s.sqrt(5)-1)/2
u=s.symbols('u',real=True)
t=s.symbols('tau',real=True)
eq(p+p*p,1,'golden_split_reference_normalized')
# FF/RF/FR/RR: zero branches physically retained with their original p^2,p^4 weights.
weights=[p*p,p**3,p**3,p**4]
eps=[0,1,-1,0]
eq(sum(weights),1,'all_four_golden_histories_retained')
for power in (1,3):eq(sum(w*e**power for w,e in zip(weights,eps)),0,'odd_golden_signed_moment_'+str(power))
for power in (2,4):eq(sum(w*e**power for w,e in zip(weights,eps)),2*p**3,'even_golden_signed_moment_'+str(power))
# Symmetric noncommuting 3D shape and actual moving shape source.
A3=s.Matrix([[s.Rational(2,5)+t,s.Rational(1,3),0],
             [s.Rational(1,3),-s.Rational(1,7)+2*t,s.Rational(1,5)],
             [0,s.Rational(1,5),s.Rational(3,4)-t]])
R3=s.expand(s.trace(A3)**2-s.trace(A3*A3))
M3=sum(weights[k]*(s.eye(3)-u*eps[k]*A3).det() for k in range(4))
eq(s.expand(M3),1+p**3*u**2*R3,'3D_golden_spatial_curvature_exact_finite_any_u')
eq(s.diff((M3-1)/(p**3*u**2),t),s.diff(R3,t),'3D_actual_moving_shape_source_exact')
ck(s.diff(R3,t)!=0,'3D_spatial_source_nontrivial_moving')
# Same existing size-four normal-matrix compiler, pad the spatial shape with a zero temporal eigenvalue.
A3pad=s.diag(0,1,1,1)
A4sp=s.diag(0,1,1,1) # explicitly construct a full4 matrix with pure spatial shape in lower block
for i in range(3):
 for j in range(3): A4sp[i+1,j+1]=A3[i,j]
M4sp=sum(weights[k]*(s.eye(4)-u*eps[k]*A4sp).det() for k in range(4))
eq(s.expand(M4sp),M3,'same_original_size4_golden_compiler_reads_spatial_zero_lift')
ck(A4sp.det()==0,'spatial_zero_lift_quartic_vanishes_without_subtraction')
# Generic 4D extrinsic normal settings: preserve quartic; two scales 1,2 eliminate it exactly.
A4a=s.Matrix([[s.Rational(2,3)+t,s.Rational(1,4),0,0],
              [s.Rational(1,4),s.Rational(3,5),s.Rational(1,8),0],
              [0,s.Rational(1,8),s.Rational(5,7)-t,s.Rational(1,6)],
              [0,0,s.Rational(1,6),s.Rational(7,9)]])
A4b=s.Matrix([[s.Rational(1,5),0,s.Rational(2,7),0],
              [0,s.Rational(4,3)+t,0,s.Rational(1,9)],
              [s.Rational(2,7),0,s.Rational(3,8),0],
              [0,s.Rational(1,9),0,s.Rational(1,4)-t]])
shape4=[A4a,A4b]
R4=sum(s.trace(A)**2-s.trace(A*A) for A in shape4)
Q4=sum(A.det() for A in shape4)
M4=sum(sum(weights[k]*(s.eye(4)-u*eps[k]*A).det() for k in range(4)) for A in shape4)
eq(s.expand(M4),2+p**3*u**2*R4+2*p**3*u**4*Q4,'4D_full_golden_moment_includes_real_quartic')
ck(s.factor(Q4)!=0,'quartic_native_four_dimensional_obstruction_present')
# Unique extraction of exactly R4 from 0,u,2u, with no small-u premise.
R4extract=(16*(M4-2)-M4.subs(u,2*u)+2)/(12*p**3*u**2)
eq(s.expand(R4extract),s.expand(R4),'exact_0_u_2u_curvature_source_removes_entire_quartic')
eq(s.diff(R4extract,t),s.diff(R4,t),'exact_moving_four_dimensional_source_no_frozen_shape')
ck(s.diff(R4,t)!=0,'4D_moving_source_nontrivial')
# Combined spatial subtraction: exact finite Lorentz geometric curvature R_G-2R3.
RGminus2R3=(R4extract-2*(M3-1)/(p**3*u**2))
eq(s.expand(RGminus2R3),s.expand(R4-2*R3),'golden_full_lorentz_scalar_from_finite_0_u_2u_scores')
eq(s.diff(RGminus2R3,t),s.diff(R4-2*R3,t),'golden_full_lorentz_moving_shape_source_exact')
# Product immersion graph(t,x,y,z): 4D shape diag(0,A3) has R4=R3.
R4product=s.trace(A4sp)**2-s.trace(A4sp*A4sp)
eq(R4product,R3,'product_space_four_curvature_equals_spatial_three')
eq(R4product-2*R3,-R3,'product_Lorentz_spatial_sign_forced_by_reverse_EH')
# Relative coefficient is mathematically unique already on product sector.
q=s.symbols('q')
eq(s.solve(s.Eq(R4product+q*R3,-R3),q)[0],-2,'relative_coefficient_minus_two_unique_from_product')
# Hostile control: one 4D scale cannot remove quartic for arbitrary A4 normal controls.
ck(s.factor((M4-2)/(p**3*u**2)-R4)!=0,'one_scale_4D_fails_when_quartic_is_real')
# A basic exact 3D graph immersion, principal curvatures a,b,c -> intrinsic scalar 2(ab+ac+bc).
a,b,c=s.symbols('a b c')
Ga=s.diag(a,b,c)
eq(s.trace(Ga)**2-s.trace(Ga*Ga),2*(a*b+a*c+b*c),'intrinsic_R3_Gauss_hypersurface_example')
# Probability positivity of each actual determinant effect requires ||u A||<1, not all amplitudes.
Afix=A3.subs(t,0)
ck(all(v.is_real is not False for v in Afix.eigenvals()),'spatial_shape_selfadjoint_real')
receipt={'scope':'Finite geometry on existing golden four-history weights plus conditional normal-shape compiler; NOT physical native selection',
 'checks_count':len(checks),'checks':checks,
 'relative_metric_Lorentz_curvature':'R_G−2R_3 from exact 4D and 3D normal Jacobian scores',
 'four_dimensional_source':'(16(M4(u)-D4)−(M4(2u)−D4))/(12 p³ u²)',
 'three_dimensional_source':'(M3(u)-D3)/(p³ u²) with spatial shape embedded as diag(0,A3) in the existing four-dimensional compiler',
 'native_spatial_accepted_owner':'03_FORMALIZATION/D0/Geometry/ArchiveSpatialHistorySplit.lean blob e019851589ad7e750e183ff1098c24283a093d19; literal spatial Hodge square on A-invariant cochains, full16 fibre',
 'blockers':['native physical admission of shape-matrix controlled golden return','same physical clock/observer spatial embedding and source','selection of signed combined contrast by SAME Cost−Info programme','true local Lorentz metric, preparation, matter and uniform exact joint refinement']}
(HOME/'GOLDEN_RESULTS.json').write_text(json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS',len(checks),'finite golden 3D+4D full Lorentz geometric curvature and first source')
print('SHA256',hashlib.sha256((HOME/'GOLDEN_RESULTS.json').read_bytes()).hexdigest())
