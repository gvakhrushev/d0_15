#!/usr/bin/env python3
"""D0 backward-GR binary source bridge: exact identity + numerical controls.

This checks only the universal calculus theorem, including moving old-address
weights. It does NOT verify the physical Golden detector-to-original-book map.
Optional --original-M consumes the published original 24x24 checker; it is not
an independently discovered Hessian nor an owner-approved detector composition.
"""
import math
import pathlib
import runpy
import sys

PHI = (1.0 + math.sqrt(5.0)) / 2.0
LOG_PHI = math.log(PHI)
J_STAR = 0.14
A = (-0.7, 0.15, 0.55)
B = (0.23, -0.31, 0.08)
C2 = (0.5, -0.1, 0.18)
W = (0.45, 0.3, 0.25)

def verify(ok, name):
    if not ok:
        raise ArithmeticError(name)
    print("PASS", name)

def ell(j):
    if j <= 0:
        raise ValueError("The binary GOOD probability must be less than one")
    return math.log(math.expm1(2.0*j)) / LOG_PHI

def d_ell(j):
    return 2.0 / (-math.expm1(-2.0*j)*LOG_PHI)

def dd_ell(j):
    g = math.exp(-2.0*j)
    return -4.0*g/((1.0-g)**2 * LOG_PHI)

def test_point(y):
    raw = [W[i]*math.exp(A[i]*y) for i in range(3)]
    z = sum(raw)
    mu = [v/z for v in raw]
    da = sum(mu[i]*A[i] for i in range(3))
    dmu = [mu[i]*(A[i]-da) for i in range(3)]
    jj = [J_STAR+B[i]*y + 0.5*C2[i]*y*y for i in range(3)]
    djj = [B[i]+C2[i]*y for i in range(3)]
    lhs = sum(mu[i]*d_ell(jj[i])*djj[i]+dmu[i]*ell(jj[i])
              for i in range(3))
    cstar = d_ell(J_STAR)
    old = cstar*sum(mu[i]*djj[i] for i in range(3))
    t1 = sum(mu[i]*(d_ell(jj[i])-cstar)*djj[i] for i in range(3))
    t2 = sum(dmu[i]*(ell(jj[i])-ell(J_STAR)) for i in range(3))
    delta = max(abs(j-J_STAR) for j in jj)
    gmax = math.exp(-2.0*min(J_STAR, min(jj)))
    local_c = 2.0 / ((1.0-gmax)*LOG_PHI)
    local_l = 4.0*gmax / ((1.0-gmax)**2 * LOG_PHI)
    bound = delta*(local_l*sum(mu[i]*abs(djj[i]) for i in range(3))
                   +local_c*sum(abs(v) for v in dmu))
    verify(abs(sum(dmu))<1e-14,"normalized moving preparation")
    verify(abs((lhs-old)-(t1+t2))<1e-12,"exact source-difference identity")
    verify(abs(lhs-old)<=bound+1e-12,"non-null mean-value bound")
    if y==0.0:
        verify(abs(lhs-old)<1e-12,"common-null moving-preparation cancellation")
    else:
        verify(abs(t2)>1e-8,"off-null endpoint/preparation term is nonzero")
    print("DETAIL y",y,"defect",lhs-old,"bound",bound,"preparation",t2)

def check_original_hessian():
    """Optional downstream control: the original owned M, NOT new physics."""
    script = (pathlib.Path(__file__).resolve().parents[1] /
              "d0_two_null_crossing_2026-10-19" /
              "check_mixed_cartan_exact.py")
    verify(script.is_file(),"owned original 24-link checker exists")
    namespace = runpy.run_path(str(script),run_name="d0_import_not_main")
    import sympy as sp
    m = namespace["flat_hessian"]()
    verify(m.shape==(24,24),"original Hessian has all24 link directions")
    eig = m.eigenvals()
    expected = {sp.Integer(2):4,sp.Integer(-2):4,
                sp.Integer(1):8,sp.Integer(-1):8}
    verify(eig==expected and m.det()==256,"owned Lorentz 12+/12- spectrum")
    gstar = math.exp(-2.0*J_STAR)
    cstar = 2.0/((1.0-gstar)*LOG_PHI)
    alpha = sp.Rational(3,2) # formal NONZERO test parameter; NOT fitted to D0
    factor = cstar*float(alpha)
    verify(factor>0,"log-odds second jet multiplies original M with positive scale")
    for eigen in (sp.Integer(2),sp.Integer(-2)):
        vec = next(vects for lam, mult, vects in m.eigenvects() if lam==eigen)[0]
        norm2 = float((vec.T*vec)[0])
        lam = float(eigen)
        def observed(t):
            f = 0.5*lam*norm2*t*t
            return ell(J_STAR + float(alpha)*f)
        t = 0.001
        second = (observed(t)+observed(-t)-2.0*observed(0.0))/(t*t)
        target = factor*lam*norm2
        verify(abs(second-target)<abs(target)*0.001,
               "native log-odds Hessian sign: eigenvalue "+str(eigen))
    print("SCOPE: second jet uses formal J(f), not the yet-unproved full Book price")

if __name__ == "__main__":
    test_point(0.0)
    test_point(0.017)
    verify(d_ell(J_STAR)>0 and dd_ell(J_STAR)<0,
           "exact local log-odds derivative signs")
    if "--original-M" in sys.argv:
        check_original_hessian()
    print("GR_closed=false; physical full-action and preparation/clock gates remain")
