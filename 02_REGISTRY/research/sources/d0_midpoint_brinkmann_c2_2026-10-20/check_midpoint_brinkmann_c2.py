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


# STRONGER: exactly the SAME fixed continuum Einstein metric is sampled at
# every lattice spacing, and genuine original CAR matter differences (not an
# independently assigned stress) match its source at the Cartan midpoint.
# The extra harmonic quartic xy(x²-y²) is also exact on every mesh.
def pw(t):
    return .04*sin(2.4*t)
def dpw(t):
    return .096*cos(2.4*t)
def A2(t):
    return .07*cos(1.8*t)
def B2(t):
    return .045*sin(3*t)
def A3(t):
    return .013*cos(4*t)
def B3(t):
    return -.009*sin(2*t)
def C4(t):
    return .011*cos(1.1*t)
def fixed_H(t,x,y):
    return (-lam*dpw(t)**2*(x*x+y*y)
            +A2(t)*(x*x-y*y)+2*B2(t)*x*y
            +A3(t)*(x**3-3*x*y*y)+B3(t)*(3*x*x*y-y**3)
            +C4(t)*x*y*(x*x-y*y))
def fixed_Hxx(t,x,y):
    return -2*lam*dpw(t)**2+2*A2(t)+6*A3(t)*x+6*B3(t)*y+6*C4(t)*x*y
def fixed_Hxy(t,x,y):
    return 2*B2(t)-6*A3(t)*y+6*B3(t)*x+3*C4(t)*(x*x-y*y)

for L in (8,16,32,64,128):
    h=1/L
    original_psi = pw(0.)
    max_sampling_err=0.
    for j in range(L):
        uj=j*h
        # Native chronological, not target-assigned material first source.
        nxt=original_psi+h*dpw(uj+h/2)
        max_sampling_err=max(max_sampling_err,abs(nxt-pw(uj+h)))
        original_psi=nxt
        assert abs(original_psi) < sqrt(1-p)
    assert max_sampling_err < .2*h*h

    j=2
    uj=j*h
    physical_midpoint=uj+h/2
    original_record_energy=dpw(physical_midpoint)**2
    x,y=.23,.27
    # Native coframe at j+1 is sampled from fixed continuum g at the
    # physical midpoint. Its 5-point stencil equals the true Laplacian.
    lap=(fixed_H(physical_midpoint,x+h,y)
         +fixed_H(physical_midpoint,x-h,y)
         +fixed_H(physical_midpoint,x,y+h)
         +fixed_H(physical_midpoint,x,y-h)
         -4*fixed_H(physical_midpoint,x,y))/h**2
    assert abs(lap+4*lam*original_record_energy)<2e-11

    # Actual original staggered Cartan connection and proper-link
    # curvature: on these polynomials both centered Hessian slots are
    # EXACT continuum values at their respective plaquette centers.
    kx=.5*(fixed_H(physical_midpoint,x,y)
           -fixed_H(physical_midpoint,x-h,y))
    kx_plus=.5*(fixed_H(physical_midpoint,x+h,y)
                -fixed_H(physical_midpoint,x,y))
    ky=.5*(fixed_H(physical_midpoint,x,y)
           -fixed_H(physical_midpoint,x,y-h))
    ky_plusx=.5*(fixed_H(physical_midpoint,x+h,y)
                 -fixed_H(physical_midpoint,x+h,y-h))
    assert abs(-2*(kx-kx_plus)/h**2
               -fixed_Hxx(physical_midpoint,x,y))<2e-11
    assert abs(-2*(ky-ky_plusx)/h**2
               -fixed_Hxy(physical_midpoint,x+h/2,y-h/2))<2e-11

    # The native scalar J2 sources cancel the full original geometric
    # first source EXACTLY, with no independently installed matter stress.
    source_euler=-lap/(2*h)-2*lam*original_record_energy/h
    assert abs(source_euler)<1e-8
    print(f"EXACT common Einstein class L={L}, "
          f"matter_record_err={max_sampling_err:.3g}, "
          f"native_euler={source_euler:+.2e}")

print("PASS: exact same continuum nonlinear sourced Einstein metric "
      "on every tested admissible lattice, O(h^2) CAR recovery at matter nodes")

# Small continuum amplitude alone does not guarantee admissibility on coarse
# meshes. This fixed smooth waveform resonates with a midpoint sampling grid.
N = 20
aliased_record = sum((1/N) * .01*2*pi*N*cos(2*pi*N*(j+.5)/N)
                     for j in range(N))
assert .01 < sqrt(1-p) and abs(aliased_record) > sqrt(1-p)
print("PASS: coarse-mesh CAR aliasing control; all-h claim requires admissibility")

