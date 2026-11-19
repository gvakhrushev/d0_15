"""Exact checks for six affine shears, two-curvature product and FLRW row."""
from sympy import Matrix, Rational, diag, diff, eye, simplify, symbols

half=Rational(1,2)
grams=((1,0,1),(2,0,1),(1,0,2),(1,half,1),(1,-half,1),(2,half,1))
readings=Matrix([[u**2,u*v,u*w,v**2,v*w,w**2] for u,v,w in grams])
assert all(u*w>v*v and u>0 for u,v,w in grams)
assert readings.det()==Rational(3,8)
inv_norm=max(sum(abs(c) for c in readings.inv().row(i)) for i in range(6))
assert inv_norm==10
print("shear determinant",readings.det(),"inverse infinity norm",inv_norm)
k,l,t=symbols('k l t', real=True, nonzero=True)
ricci2=2*k**2+2*l**2
riemann2=4*k**2+4*l**2
R=2*(k+l)
weyl2=simplify(riemann2-2*ricci2+R**2/3)
weyl_der=simplify(diff(t*weyl2.subs(k,k/t),t).subs(t,1))
assert simplify(weyl_der-Rational(4,3)*(k+l)*(l-k))==0
print("Weyl product variation",weyl_der)
q=symbols('q',real=True)
b=t**Rational(1,3)
H=diff(b,t)/b
g=diag(-1,b*b,b*b,b*b)
Ein_lower=diag(3*H**2,*[-(2*diff(H,t)+3*H**2)*b*b]*3)
Ein_upper=g.inv()*Ein_lower*g.inv()
Hess_phi=diag(-q/t**2,*[-H*b*b*q/t]*3)
scalar=simplify(-2*(Ein_upper*Hess_phi).trace())
assert simplify(scalar-4*q/(3*t**4))==0
print("curvature-kinetic residual on canonical scalar FLRW",scalar)
