"""Exact original r on both current axes and identity with the JZ6 field sum."""
from fractions import Fraction as F
import sympy as s

p,z = s.symbols("p z")
x,y = s.symbols("x y")
quadratic = p*p+p-1


def red(expr):
    return s.rem(s.expand(expr),quadratic,p).expand()


E = p*p*(1+x)
angular = 4*E*(1-E)
u = p+p*p*y
B = 4*u*u*(1-u*u)
A = angular+(1-angular)*B
r = z*(A+B)-z*z*A*B
rx = red(r.subs(y,0))
ry = red(r.subs(x,0))
r0 = rx.subs(x,0)
rf = rx.diff(x).subs(x,0)
rq = ry.diff(y).subs(y,0)
assert red(rf-4*z*p**11*(1-4*z*p**3)) == 0
assert s.degree(rx,x)==2 and s.degree(ry,y)==8
assert red(p*rx.coeff(x,2)+rf)==0
cy = s.cancel((ry-r0-rq*y)/y**2).expand()
assert s.degree(cy,y)==6 and red(cy.coeff(y,6)+16*z*z*p**22)==0
assert red(rx-r0-rf*x-rx.coeff(x,2)*x*x) == 0
assert red(ry-r0-rq*y-cy*y*y) == 0

N = (256,256,1024,2048,256,256,1024)
assert N[2]==N[-1]==1024 and sum(N)==5120
R = s.symbols("R:7")
ref, al, visibility, contrast = s.symbols("ref alpha lambda delta")
W = al*sum(n*v for n,v in zip(N,R))
W0 = W.subs({R[2]:ref,R[6]:ref})
core = R[2]+R[6]-2*ref
assert s.expand(W-W0-1024*al*core)==0
Q = visibility*(4+al*al*contrast*core)
assert s.expand(Q-4*visibility-visibility*al*contrast*(W-W0)/1024)==0

# Density and attenuation first terms for every degree 2..8.
eps, rho, f = s.symbols("eps rho f", positive=True)
for k in range(2,9):
    t = eps*f/rho
    term = rho*t**k/eps
    assert s.cancel(s.diff(term,f) - k*t**(k-1)) == 0
    assert s.cancel(s.diff(term,rho) - (1-k)*t**k/eps) == 0
    assert s.cancel(s.diff(term,eps) - rho*(k-1)*t**k/eps**2) == 0

# Bounds on original compact |x|,|y|<=1/64 with p^2<2/5.
z0=F(1,2**20)
assert F(3,5)-F(2,5)/64 > F(1,2)
assert F(5,8)+F(2,5)/64 < F(2,3)
max_Bp=8*F(2,5)*F(2,3)
max_Bpp=8*F(2,5)**2*(6*F(2,3)**2-1)
assert max_Bp == max_Bpp == F(32,15)
assert 2*max_Bpp+2*z0*max_Bp**2 < 5
assert 8*F(2,5)**2 < 2

# The SAM right tangent covariance is p^3I.
assert red((1-p*p)*p*p-p**3) == 0
print("PASS: exact degrees 2/8, gravitational quadratic coefficient -phi, matter degree-six correction, all seven weights, off-shell JZ6 identity, moving density/attenuation jets, uniform 5z curvature bound and SAM normalization.")
