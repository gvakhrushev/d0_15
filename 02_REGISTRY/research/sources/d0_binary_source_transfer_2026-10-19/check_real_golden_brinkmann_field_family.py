#!/usr/bin/env python3
"""Exact original Golden binary fields on an all40 Brinkmann/CAR source family.

Consumes (does not re-prove) owned original six-plaquette unrestricted
40->3->1 Brinkmann theorem and native two-tick J2 field inputs.
All good/failure complements remain in the instrument; fundamental Book
Cost-Info/preparation/controller/clock physical selection is NOT inferred.
"""
from math import sqrt,log,log1p,exp

p=(sqrt(5)-1)/2
PHI=1/p
D=1056
T=1.0

def native(k,f,q,sigma=-1):
    z=p**(2*k)/(1-p**(2*k))
    A=exp(2*D*log1p(-p**(2*k)))
    E=p*p*(1+T*T*f)
    b=(p+sigma*p*p*T*T*q)**2
    B=4*b*(1-b)
    lam=4*E*(1-E)
    Q=1-z*B
    R=1-z*(lam+(1-lam)*B)
    if not (0<E<1 and 0<b<1 and Q>0 and R>0):
        raise ValueError("outside original operator-positive native chart")
    J=-(D/2)*(log(Q)+log(R))
    return J,A*exp(-2*J)

def analytic(k,sigma=-1):
    z=p**(2*k)/(1-p**(2*k))
    B=4*p**3
    Q=1-z*B
    R=1-z*(B+p**6*B)
    af=(D/2)*z*4*p**11*T*T/R
    aq=(D/2)*z*8*sigma*p**6*T*T*(1/Q+p**6/R)
    return af,aq,aq/af

def lap(H,u,x,y,h):
    return (H(u,x+h,y)+H(u,x-h,y)
            +H(u,x,y+h)+H(u,x,y-h)-4*H(u,x,y))/(h*h)

def test(k):
    af,aq,lam=analytic(k)
    h=1e-5
    fd=(native(k,h,0)[0]-native(k,-h,0)[0])/(2*h)
    qd=(native(k,0,h)[0]-native(k,0,-h)[0])/(2*h)
    assert abs((fd-af)/af)<1e-5 and abs((qd-aq)/aq)<1e-5
    gstar=native(k,0,0)[1]
    c=2/((1-gstar)*log(PHI))
    assert c*af>0 and abs(c*aq/(c*af)-lam)<1e-12
    # The original all40 N2/N3 equation is
    # Delta_h H(u+h,x,y)=-4*lambda*|D_u Psi(u)|^2.
    # Harmonic Weyl cubic and lattice-corrected quartic remain nonzero.
    energy=lambda u: 0.1+.015*u+.002*u*u
    for h in (.2,.125,.05):
        def H(u,x,y):
            W3=x**3-3*x*y*y
            W4=x**4-6*x*x*y*y+y**4-h*h*(x*x+y*y)
            return -lam*energy(u-h)*(x*x+y*y)+.04*W3+.01*W4
        for u,x,y in ((.5,.3,-.2),(1.25,-.4,.6),(2.,.15,-.45)):
            assert abs(lap(H,u+h,x,y,h)+4*lam*energy(u))<1e-9
    return gstar,af,aq,lam

if __name__=="__main__":
    for k,ref in ((2,1.155885924e-311),(9,.486548287616),
                  (10,.759460770278)):
        g,af,aq,lam=test(k)
        if k==2: assert abs(g-ref)/ref<1e-8
        else: assert abs(g-ref)<1e-11
        print(f"PASS original k={k}: GOOD={g:.16g}, alpha_f={af:.16g}, "
              f"alpha_q={aq:.16g}, lambda={lam:.16g}; "
              "all three exact finite lattice harmonic checks")
    print("SCOPE: conditional original detector field Euler class, not fundamental Book action; GR_closed=false")
