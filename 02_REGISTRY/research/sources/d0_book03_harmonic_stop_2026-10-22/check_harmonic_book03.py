#!/usr/bin/env python3
"""Book03 native P U*Q U P return-logdet = complete harmonic stopped clock.
Exact operator identities + original 528+528 Golden A/B two-tick event.
Mathematical Naimark realization only: D0 native physical admission OPEN.
"""
import sympy as s
from mpmath import mp

r,t,z=s.symbols("r t z",real=True)
# Genuine rank2 P->Q amplitudes of 4x4 orthogonal rotations.
F=s.diag(s.sin(r)**2,s.sin(t)**2)
J=-s.log((s.eye(2)-z*F).det())
for v in (r,t):
    assert s.simplify(s.diff(J,v)-z*s.trace((s.eye(2)-z*F).inv()*F.diff(v)))==0
print("PASS symbolic original P U*Q U P source, two independent field jets")
mp.dps=80
zz=mp.mpf(2)**-20
vals=[mp.sin(mp.mpf(".27"))**2,mp.sin(mp.mpf(".43"))**2]
d=len(vals)
Jfull=-sum(mp.log(1-zz*f) for f in vals)
Nmax=9
mass=sum(sum((zz*f)**n*(1-zz*f) for f in vals)/d for n in range(Nmax+1))
tail=sum((zz*f)**(Nmax+1) for f in vals)/d
assert abs(mass+tail-1)<mp.mpf("1e-65")
H=lambda n:sum(mp.mpf(1)/k for k in range(1,n+1))
partial=sum(H(n)*sum((zz*f)**n*(1-zz*f) for f in vals)/d for n in range(Nmax+1))
assert 0< Jfull/d-partial < (H(Nmax+1)+1/(1-zz))*zz**(Nmax+1)
M=4
capped=sum(zz**n*sum(f**n for f in vals)/n for n in range(1,M+1))
assert abs(Jfull-capped)<=d*zz**(M+1)/((M+1)*(1-zz))
u=s.symbols("u")
for n in range(1,10):
    coefficient=s.series(-s.log(1-u)/(1-u),u,0,n+1).removeO().expand().coeff(u,n)
    assert coefficient==sum(s.Rational(1,k) for k in range(1,n+1))
print("PASS full stopped memory, exact cap tail and unique harmonic H_N")
step=mp.mpf("1e-12")
def book(aa,bb):
    return -sum(mp.log(1-zz*mp.sin(v)**2) for v in (aa,bb))
def source(v):
    return 2*zz*mp.sin(v)*mp.cos(v)/(1-zz*mp.sin(v)**2)
for aa,bb in ((mp.mpf(".27"),mp.mpf(".43")),(mp.mpf(".43"),mp.mpf(".27"))):
    assert abs((book(aa+step,bb)-book(aa-step,bb))/(2*step)-source(aa))<mp.mpf("1e-20")
print("PASS full exact Book first-source = harmonic stopped source")
p=(mp.sqrt(5)-1)/2
X=mp.mpf(".004");Y=mp.mpf("-.001")
def native_ab(x,y):
    e=p*p*(1+x);ell=4*e*(1-e)
    b=p-p*p*y;B=4*b*b*(1-b*b)
    A=ell+(1-ell)*B
    return A,B
def rr(x,y):
    A,B=native_ab(x,y)
    return zz*(A+B)-zz*zz*A*B
def jj(x,y):
    A,B=native_ab(x,y)
    return -528*(mp.log(1-zz*A)+mp.log(1-zz*B))
A,B=native_ab(X,Y)
assert 0<A<1 and 0<B<1
r_native=rr(X,Y)
J2=jj(X,Y)
assert abs(J2+528*mp.log(1-r_native))<mp.mpf("1e-65")
assert abs((1-zz*A)*(1-zz*B)-(1-r_native))<mp.mpf("1e-65")
assert abs(J2/1056+mp.log(1-r_native)/2)<mp.mpf("1e-65")
h=mp.mpf("1e-15")
for axis in (0,1):
    if axis==0:
        rp=(rr(X+h,Y)-rr(X-h,Y))/(2*h)
        jp=(jj(X+h,Y)-jj(X-h,Y))/(2*h)
    else:
        rp=(rr(X,Y+h)-rr(X,Y-h))/(2*h)
        jp=(jj(X,Y+h)-jj(X,Y-h))/(2*h)
    assert abs(jp-528*rp/(1-r_native))<mp.mpf("1e-25")
print("PASS actual native 528+528 J2 =1056 E[H_N] =-528 log(1-r)")
print("PASS same complete original two-band OR/no-click outcome and offnull x/y jets")
print("Book03 J =",mp.nstr(Jfull,22),"E H_N =",mp.nstr(Jfull/d,22))
print("PHYSICAL source/writer/cut/Book03 full HJR selection OPEN; GR_closed=false")
