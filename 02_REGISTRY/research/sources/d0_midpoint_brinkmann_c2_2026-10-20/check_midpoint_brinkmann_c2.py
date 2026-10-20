#!/usr/bin/env python3
"""Native all40+2 Brinkmann equation, midpoint clock and C2 convergence.

This deliberately uses the ALREADY OWNED exact all40+2 reduction as input.
It replays the new explicit analytic harmonic lift, actual native forward
matter source and natural midpoint readout; no new physical action/selector.
"""
from math import asinh, cos, sin, sqrt, exp, pi

p = (sqrt(5) - 1)/2
z = 2**-20
Q = 1-z*4*p**3
R = 1-z*4*p**3*(1+p**6)
lam = -2*p**-5*(R/Q+p**6)
assert -23.417 < lam < -23.416

# Nonconstant original scalar/top CAR source and two independent harmonic
# gravitational modes. Amplitudes are small enough for the unchanged
# positive normalized native CAR complement.
def psi(t):
    return .04*sin(2.4*t)
def dpsi(t):
    return .096*cos(2.4*t)
def Ec(h,t):
    return ((psi(t+h/2)-psi(t-h/2))/h)**2
def E(t):
    return dpsi(t)**2

modes = [
    (1.3, lambda t:.03*(1+.2*cos(2.5*t))),
    (.7, lambda t:-.012*sin(1.7*t)),
]
def alpha(h,k):
    return 2*asinh(abs(sin(k*h/2)))/h

def H(h,t,x,y):
    source = -lam*Ec(h,t)*(x*x+y*y)
    return source+sum(A(t)*exp(alpha(h,k)*x)*cos(k*y) for k,A in modes)

def H0(t,x,y):
    return -lam*E(t)*(x*x+y*y)+sum(
        A(t)*exp(k*x)*cos(k*y) for k,A in modes)

def hess(h,t,x,y):
    xx = -2*lam*Ec(h,t)
    yy = xx
    xy = 0.0
    for k,A in modes:
        c = A(t)*exp(alpha(h,k)*x)
        a=alpha(h,k)
        xx += c*a*a*cos(k*y)
        yy -= c*k*k*cos(k*y)
        xy -= c*a*k*sin(k*y)
    return xx,yy,xy

def hess0(t,x,y):
    xx = yy = -2*lam*E(t)
    xy = 0.0
    for k,A in modes:
        c = A(t)*exp(k*x)
        xx += c*k*k*cos(k*y)
        yy -= c*k*k*cos(k*y)
        xy -= c*k*k*sin(k*y)
    return xx,yy,xy

t,x,y = .32,.30,.20
oldH=oldC=None
for L in (8,16,32,64,128):
    h=1/L
    # Actual source at ORIGINAL j and metric at next native slice,
    # both assigned to the same physical midpoint tmid = u_j+h/2.
    j=2
    uj=j*h
    tmid=uj+h/2
    Ej=((psi(uj+h)-psi(uj))/h)**2
    assert abs(Ej-Ec(h,tmid))<1e-13
    lap=(H(h,tmid,x+h,y)+H(h,tmid,x-h,y)
        +H(h,tmid,x,y+h)+H(h,tmid,x,y-h)-4*H(h,tmid,x,y))/h**2
    # Equation (13) of the ORIGINAL arbitrary Brinkmann all40 theorem.
    assert abs(lap+4*lam*Ej)<3e-11

    # Original fully varied Cartan link K on the u_j time link:
    # source and advanced coframe at same actual time midpoint.
    Kx=.5*(H(h,tmid,x,y)-H(h,tmid,x-h,y))
    Ky=.5*(H(h,tmid,x,y)-H(h,tmid,x,y-h))
    # The normalized central Laplacian carries h^-2; the native link
    # variation is therefore -h^3/2 times lap, as in the all40 theorem.
    ex=-h**3/2*lap
    source=h*(Kx-.5*(H(h,tmid,x+h,y)-H(h,tmid,x,y))
         +Ky-.5*(H(h,tmid,x,y+h)-H(h,tmid,x,y)))
    assert abs(source-ex)<3e-13
    full_j2_euler=-lap/(2*h)-2*lam*Ej/h
    assert abs(full_j2_euler)<1e-8

    errH=abs(H(h,t,x,y)-H0(t,x,y))
    errC=max(abs(a-b) for a,b in zip(hess(h,t,x,y),hess0(t,x,y)))
    xx,yy,_=hess(h,t,x,y)
    Ric_source_error=(xx+yy)/2+2*lam*Ec(h,t)
    exact_error=.5*sum(A(t)*(alpha(h,k)**2-k*k)
             *exp(alpha(h,k)*x)*cos(k*y) for k,A in modes)
    assert abs(Ric_source_error-exact_error)<1e-12
    if oldH is not None:
        assert 3.5 < oldH/errH < 4.5
        assert 3.5 < oldC/errC < 4.5
    print(f"L={L:3} h={h:.6f} nativeEul={full_j2_euler:+.2e} "
          f"C0err={errH:.8g} C2err={errC:.8g} "
          f"RicciError={Ric_source_error:.8g}")
    oldH,oldC=errH,errC

# The continuum has both genuinely nonzero Ricci and tracefree Weyl.
xx0,yy0,xy0=hess0(t,x,y)
assert E(t)>0 and (abs(xx0-yy0)>1e-6 or abs(xy0)>1e-6)
assert abs((xx0+yy0)/2+2*lam*E(t))<1e-12
print("PASS: exact original reduced finite 40+2 Euler, nonflat nonvacuum, "
      "O(h^2) metric and curvature convergence on midpoint clock")
