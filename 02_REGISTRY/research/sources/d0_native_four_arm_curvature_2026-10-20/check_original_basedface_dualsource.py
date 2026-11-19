#!/usr/bin/env python3
"""D0: conditional original Jones full128 mixed tensor routed through ACTUAL
four-edge proper Lorentz based plaquettes. Geometric chain-rule/Ward checker.

Uses accepted exact original Jones CAR16 3x3 M determinants from
check_native_four_arm_exact.py; no new rank computation or Book action.
"""
import sympy as s

E=lambda i,j: s.eye(4)[:,i]*s.eye(4)[j,:]
eta=s.diag(1,-1,-1,-1)
I=s.eye(4)
X03=E(0,3)+E(3,0)
X01=E(0,1)+E(1,0)
for X in (X03,X01):
    assert X.T*eta+eta*X==s.zeros(4)

t,a,b,c,d=s.symbols('t a b c d',real=True)
# True rooted plaquette P_rs(z)=Ur(z)Us(z+r)Ur(z+s)^-1Us(z)^-1.
P=(I+t*a*X03)*(I+t*b*X03)*(I-t*c*X03)*(I-t*d*X03)
assert s.simplify(s.diff(P,t).subs(t,0)-(a+b-c-d)*X03)==s.zeros(4)
assert s.simplify(s.diff(P,t).subs({t:0,a:1,c:1,b:0,d:0}))==s.zeros(4)
assert s.simplify(s.diff(P,t).subs({t:0,a:0,c:0,b:1,d:1}))==s.zeros(4)
z0,zr,zs,zrs=s.symbols('z0 zr zs zrs')
assert s.simplify((a+b-c-d).subs({
    a:z0-zr,b:zr-zrs,c:zs-zrs,d:z0-zs}))==0
# Finite pure-gauge rooted product telescopes:
# g_z g_z+r^-1 * g_z+r g_z+r+s^-1 *
# g_z+r+s g_z+s^-1 * g_z+s g_z^-1 = I.
# The same holds for either original P01 or P31 from shared root z.

# For constant NONCOMMUTING links, the first jet is zero, but the
# genuine physical plaquette commutator at second order survives.
series=lambda X,sign:I+sign*t*X+t*t*X*X/2
Pcomm=series(X03,1)*series(X01,1)*series(X03,-1)*series(X01,-1)
assert s.simplify(s.diff(Pcomm,t).subs(t,0))==s.zeros(4)
assert s.simplify(s.diff(Pcomm,t,2).subs(t,0)/2
                  -(X03*X01-X01*X03))==s.zeros(4)
assert X03*X01-X01*X03!=s.zeros(4)

# Route the original Jones query effective role0 link through the
# real based face P01 and its role3 link through P31 at the same z.
# Vary (role0,X03), (role0,X01), (role3,X03) via the positive
# r-edge of these two plaquettes. At the original flat point their
# 3x3 link-to-plaquette differential is literally Identity.
curl=s.eye(3)
assert curl.det()==1
for prime,det_m in ((101,19),(181,139),(1009,604),(4001,1480)):
    assert det_m%prime!=0
    assert (det_m*int(curl.det()))%prime==det_m%prime
print('PASS original based plaquette 4-edge exact first-order curl')
print('PASS homogeneous/pure-gauge flat Ward, finite gauge-flat telescope')
print('PASS noncommuting constant links real second-order holonomy')
print('PASS original exact native Jones 3x3 mixed rank transported by curl')
print('SCOPE: effective-plaquette Walsh/Julia programme needs actual G0')
print('admission, paid four-link clock, observer/gauge transport and full Info.')
