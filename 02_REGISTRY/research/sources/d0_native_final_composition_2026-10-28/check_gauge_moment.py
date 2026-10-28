#!/usr/bin/env python3
"""Exact controls of the original return's diagonal boundary moment.

Structural algebra, not proof of physical D0 boundary admission or GR.
No assert-based tests: normal and optimized execution exercise every gate.
"""
import hashlib
import json
from pathlib import Path
import sympy as S

controls = []

def zero(name, value):
    entries = list(value) if isinstance(value, S.MatrixBase) else [value]
    if any(S.cancel(S.expand(x)) != 0 for x in entries):
        raise RuntimeError(name + ': exact zero test failed')
    controls.append(name)

def require(name, flag):
    if not flag:
        raise RuntimeError(name + ': condition failed')
    controls.append(name)

I = S.eye(2)
P = S.diag(1, 0)
J = S.Matrix([[0, -1], [1, 0]])
c, s, z = S.Rational(4,5), S.Rational(3,5), S.Rational(1,4)
U = S.Matrix([[c,-s],[s,c]])
T = U.T*P*U
R = (I-z*P*(I-T)*P).inv()
A = P*R*P
mu = -z*(T*A-A*T)
zero('rational_native_rotation_unitary', U.T*U-I)
zero('second_endpoint_is_projector', T*T-T)
zero('exact_moment_matrix', mu-S.Rational(12,91)*J)
muJ=S.trace(mu*J)
zero('exact_common_angle_moment', muJ+S.Rational(24,91))

# No finite-difference approximation: differentiate original rational-rotation
# line at t=0, preserving its exact source and the complete active determinant.
t = S.symbols('t', real=True)
rot = S.Matrix([[S.cos(t),-S.sin(t)],[S.sin(t),S.cos(t)]])
Pt = rot*P*rot.T
Ft=Pt*(I-T)*Pt
price=-S.log((I-z*Ft).det())
first=S.simplify(S.diff(price,t).subs(t,0))
second=S.simplify(S.diff(price,t,2).subs(t,0))
zero('original_return_first_angle_source', first-S.Rational(24,91))
zero('original_return_second_angle_source', second-S.Rational(1850,8281))
require('vertical_contraction_nonzero', second != 0)

# The common-angle direction has zero scalar derivative but nonzero contraction
# with the exact pair symplectic form.
W=second*S.Matrix([[0,1],[-1,0]])
v=S.Matrix([1,1])
zero('price_covariance_is_not_basicness', (v.T*W)-S.Matrix([[-second,second]]))
require('pair_form_nondegenerate', W.det() != 0)
grad_inv=S.Matrix([1,-1])
zero('invariant_coordinate_bracket_zero', (grad_inv.T*W.inv()*grad_inv)[0])

# Full original P,U feedback covectors cancel in the total cotangent moment.
C=(I-P)*U*P
F=C.T*C
Rf=(I-z*F).inv()
E=Rf*C.T*U-U*Rf*C.T
gp=z*(E+E.T)
gu=2*z*C*Rf
dP=J*P-P*J
dU=J*U-U*J
pcon=S.trace(gp*dP)
ucon=S.trace(gu.T*dU)
zero('full_original_moment_balance', pcon+ucon)

# A nontrivial independent matrix comparison: 3D rational orthogonal U and
# arbitrary skew X; this avoids relying only on the commuting SO(2) rotation.
I3=S.eye(3)
P3=S.diag(1,1,0)
K3=S.Matrix([[0,1,2],[-1,0,1],[-2,-1,0]])/5
U3=(I3-K3).inv()*(I3+K3)
X3=S.Matrix([[0,2,-1],[-2,0,3],[1,-3,0]])/7
C3=(I3-P3)*U3*P3
Rf3=(I3-z*C3.T*C3).inv()
E3=Rf3*C3.T*U3-U3*Rf3*C3.T
gp3=z*(E3+E3.T)
gu3=2*z*C3*Rf3
p3=S.trace(gp3*(X3*P3-P3*X3))
u3=S.trace(gu3.T*(X3*U3-U3*X3))
zero('three_dimensional_total_moment_balance', p3+u3)
require('separate_retained_sectors_nonzero', p3 != 0 and u3 != 0)

# Any symmetric terminal Hessian pulls the cotangent form back to zero.
h11,h12,h22=S.symbols('h11 h12 h22', real=True)
H=S.Matrix([[h11,h12],[h12,h22]])
L=S.eye(2).col_join(H)
O=S.zeros(4)
O[:2,2:]=S.eye(2)
O[2:,:2]=-S.eye(2)
zero('terminal_gradient_graph_lagrangian', L.T*O*L)

# Commuting endpoint projectors have zero moment; noncommuting pair does not.
for label,T0 in [('same',P),('orthogonal',I-P)]:
    A0=P*(I-z*P*(I-T0)*P).inv()*P
    zero('commuting_zero_moment_'+label, T0*A0-A0*T0)
require('transverse_pair_nonzero_moment', mu != S.zeros(2))

# Lapse-component smearing: exact exterior derivative and original-term
# countercontrols. The coordinates are comparison charts, not newly admitted
# physical local lapse directions.
x,y,n1,n2=S.symbols('x y n1 n2', real=True)
bb=x*x+3*x*y+2*y*y
alpha1=n1*S.diff(bb,x)
alpha2=n2*S.diff(bb,y)
dal=S.diff(alpha2,x)-S.diff(alpha1,y)
zero('lapse_smearing_exterior_derivative', dal-(n2-n1)*S.diff(bb,x,y))
zero('uniform_weight_integrable_control', dal.subs(n2,n1))
e1,e2=S.symbols('e1 e2', real=True)
heat=S.log(S.exp(-e1)+S.exp(-e2))
heat12=S.simplify(S.diff(heat,e1,e2).subs({e1:0,e2:S.log(2)}))
zero('full_heat_cross_source', heat12+S.Rational(2,9))
require('heat_independent_smearing_not_closed', heat12 != 0)
return12=-second
zero('original_return_mixed_source', return12+S.Rational(1850,8281))
require('return_independent_smearing_not_closed', return12 != 0)

result={
 'status':'PASS_EXACT_BOUNDARY_MOMENT_CONTROLS',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'control_count':len(controls),'controls':controls,
 'rational_original_pair':{'c':'4/5','s':'3/5','z':'1/4',
  'mu_matrix_coefficient':'12/91','mu_common_angle':'-24/91',
  'f_second':'1850/8281'},
 'full_cotangent_3D_sector_sources':{'P':str(p3),'U':str(u3),'sum':'0'},
 'lapse_smearing_cross_sources':{'heat':'-2/9','return':'-1850/8281',
  'criterion':'d alpha_N = (N_b-N_a) B_ab dy_a wedge dy_b'},
 'scope':'Exact original-return structural controls. No native physical boundary, total reduction, local lapse, HDA, full42 or GR closure.'
}
print(json.dumps(result,indent=2,sort_keys=True))
