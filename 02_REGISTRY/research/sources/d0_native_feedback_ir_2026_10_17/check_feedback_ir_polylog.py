#!/usr/bin/env python3
"""Unchanged v8 feedback IR coefficients, value and actual first-source checks.

The scalar potential v is a NON-NATIVE diagnostic of the heat coefficient,
not a new gravitational action/matter mass. Full exterior16 multiplicity.
"""
import math
import mpmath as mp
mp.mp.dps = 50
phi = (1 + mp.sqrt(5)) / 2
beta = 2 / phi**2
z = mp.mpf(1) / 2**20
q = z/(1-z)
M = mp.mpf(128)
pi = mp.pi
Phi = lambda n: -mp.polylog(n, -q)

def theta(t):
    kmax = int(mp.ceil(mp.sqrt(48*mp.log(10)/(4*pi*pi*t)))) + 2
    return 1+2*mp.fsum(mp.exp(-4*pi*pi*t*k*k) for k in range(1,kmax+1))

def dtheta(t):
    kmax = int(mp.ceil(mp.sqrt(48*mp.log(10)/(4*pi*pi*t)))) + 2
    return -8*pi*pi*mp.fsum(k*k*mp.exp(-4*pi*pi*t*k*k) for k in range(1,kmax+1))

def native_j(R,v=0,a=(1,1,1,1),deriv=None):
    a = tuple(mp.mpf(x) for x in a)
    v=mp.mpf(v); R=mp.mpf(R)
    out=mp.mpf(0)
    for n in range(1,11):
        t=n*beta/(R*R)
        ts=[t/u**2 for u in a]
        thetas=[theta(x) for x in ts]
        val=16*mp.exp(-t*v)*mp.fprod(thetas)
        if deriv=="v": val *= -t
        if deriv=="a0": val *= -2*ts[0]*dtheta(ts[0])/(a[0]*thetas[0])
        out += (-1)**(n+1)*q**n*val/n
    return -M*out

def asympt(R,v):
    R=mp.mpf(R);v=mp.mpf(v)
    a0=mp.mpf(16)
    a2=-16*v
    a4=8*v*v
    return -M/(16*pi*pi)*(R**4*Phi(3)*a0/beta**2
                         +R**2*Phi(2)*a2/beta+Phi(1)*a4)

def check(b, note, tol):
    if abs(b)>tol: raise RuntimeError(f"{note}: {b} > {tol}")

def run():
    cr=M*Phi(2)/(12*pi*pi*beta)
    rho=M*Phi(3)/(pi*pi*beta*beta)
    print("native c_R",mp.nstr(cr,24),"native rho",mp.nstr(rho,24))
    check(cr-mp.mpf("0.000001349194805331122753927471"),"cR",mp.mpf("1e-25"))
    for R in (8,16,32):
        v=mp.mpf("2.5")
        err=native_j(R,v)-asympt(R,v)
        dd=native_j(R,v,deriv="v")
        pred=M*Phi(2)*R**2/(pi*pi*beta)-M*Phi(1)*v/(pi*pi)
        check(err,"value small-time IR",mp.mpf(".000001"))
        check(dd-pred,"field-source small-time IR",mp.mpf(".000001"))
        print(f"R={R} value_error={mp.nstr(err,12)} source_error={mp.nstr(dd-pred,12)}")
    a=(mp.mpf("1.1"),mp.mpf(".9"),mp.mpf("1.2"),mp.mpf(".97"))
    R=16
    exact=native_j(R,0,a,deriv="a0")
    theory=-rho*R**4*mp.fprod(a)/a[0]
    check(exact/theory-1,"flat metric source",mp.mpf("1e-12"))
    print("anisotropic native metric derivative relative_error",mp.nstr(exact/theory-1,12))
    print("status=PASS; scalar potential and anisotropic metrics are mathematical checks")
if __name__=="__main__":run()
