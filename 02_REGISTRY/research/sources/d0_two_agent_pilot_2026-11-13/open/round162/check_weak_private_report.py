"""Exact marked scratch contractions and outward first-source bounds."""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
sys.path.insert(0, str(HERE.parent / "round160"))
from check_marked_echo_source import I, O, QMIN, QMAX, Z, bounds, power

PARENT = "216c1e7d0f9bf309b3a07415436e56893126a17c"
EI14 = ("02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/"
        "2026-11-19/metric/ei14_fine_result.json")


def verify_symbolic():
    j, e, d, w, omega, q = sp.symbols("j e d w omega q", real=True)
    c = 1 - 2*q
    denominator = 1 - (d*omega*c)**2
    mark = sum(w*(j*c + sign*e*omega)**2 / (2*(1+sign*d*omega*c))
               for sign in (1, -1))
    h0 = w*j*j*c*c
    residual = w*(e-j*d*c*c)**2 / denominator
    derivative = -4*w*c*(j-e*d*omega**2)**2 / denominator**2
    O.require(sp.cancel(mark-h0-omega**2*residual) == 0, "wrong paired overlap")
    O.require(sp.cancel(sp.diff(mark, q)-derivative) == 0, "wrong first derivative")
    dephase = sp.symbols("eta", real=True)
    pure = w*((1+dephase-2*d*d)*c*c+1-dephase)/(1-d*d*c*c)
    pure_derivative = -4*w*c*(1+dephase)*(1-d*d)/(1-d*d*c*c)**2
    defect = sp.together(sp.diff(pure,q)-pure_derivative).as_numer_denom()[0]
    O.require(sp.rem(defect, dephase**2+d**2-1, dephase) == 0,
              "balanced rotated pointer derivative")
    for count in range(5):
        # Independent coherent scratch computation on explicit computational states.
        a, b = sp.Rational(4,5), sp.Rational(3,5)
        v = (a,b)
        d0 = a*a-b*b
        for m in (0,1):
            initial, flag0, flag1 = [], [], []
            for word in product((0,1), repeat=count):
                amplitude = sp.prod(v[bit] for bit in word)
                parity = sum(word) % 2
                initial.append(amplitude)
                flag0.append(amplitude*v[m ^ parity])
                flag1.append(amplitude*v[m ^ parity ^ 1])
            first, second, scratch = map(sp.Matrix, (flag0, flag1, initial))
            sign = (-1)**m
            O.require(first.dot(first) == (1+sign*d0**(count+1))/2
                      and second.dot(second) == (1-sign*d0**(count+1))/2,
                      "scratch mark norms")
            O.require(first.dot(second) == a*b, "unattenuated overlap")
            O.require(scratch.dot(first) == (a+b+sign*(a-b)*d0**count)/2
                      and scratch.dot(second) == (a+b-sign*(a-b)*d0**count)/2,
                      "scratch passive overlap")
    p = (sp.sqrt(5)-1)/2
    a, b = sp.sqrt(p), p
    v = sp.Matrix([a,b])
    gate = sp.Matrix([[a,-b],[b,a]])
    x = sp.Matrix([[0,1],[1,0]])
    for m in (0,1):
        t = gate*x**m*v
        u = (x**m*gate)**2*v
        actual = p**(7+5*m)*(v.dot(t)*v.dot(u))**2
        O.require(sp.simplify(actual-p**14) == 0, "literal balancing tails")


def grid(lo, hi, n, row):
    cuts = [I.rational(lo+(hi-lo)*Q(k,n)) for k in range(n+1)]
    shape = (1,n) if row else (n,1)
    lower = np.array([i.lo for i in cuts[:-1]]).reshape(shape)
    upper = np.array([i.hi for i in cuts[1:]]).reshape(shape)
    return I(lower,upper)


def verify_outward():
    one = I(1.)
    p = (I(5.).sqrt()-1)/2
    j, e, d, w = p.sqrt()+p, p.sqrt()-p, power(p,3), power(p,14)
    q, omega = grid(QMIN,QMAX,512,False), grid(Q(0),Q(1),128,True)
    c = one-2*q
    c2, o2 = c.square(), omega.square()
    k2 = d.square()*o2
    den = one-k2*c2
    numerator = e-j*d*c2
    residual = w*numerator.square()/den
    residual_dq = w*(8*numerator*j*d*c*den-4*numerator.square()*k2*c)/den.square()
    h = w*j.square()*c2 + o2*residual
    dh = -4*w*c*(j-e*d*o2).square()/den.square()
    ddh = 8*w*(j-e*d*o2).square()*(one+3*k2*c2)/power(den,3)
    beta = one-I.rational(Z)+I.rational(Z)*h
    gain = -dh/beta
    gain_dq = -ddh/beta+I.rational(Z)*(dh/beta).square()
    O.require(np.min(gain.lo) > 0.0021, "positive cold gain floor")
    O.require(np.max(gain_dq.hi) < 0., "gain should decrease in q")
    O.require(np.min(den.lo) > 0.95, "strictly nonzero occupied branches")
    return {
        "q": [str(QMIN), str(QMAX)],
        "omega": [0,1],
        "h": bounds(h),
        "cold_gain_divided_by_z": bounds(gain),
        "cold_gain_q_derivative_divided_by_z": bounds(gain_dq),
        "h_minus_h0_over_omega_squared": [0., bounds(residual)[1]],
        "dq_h_minus_h0_over_omega_squared": bounds(residual_dq),
    }


def verify_rotated_pointer():
    one = I(1.)
    p = (I(5.).sqrt()-1)/2
    real, imag = p.sqrt(), p
    a, b = one, I(0.)
    remaining = 1048
    while remaining:
        if remaining % 2:
            a, b = a*real-b*imag, a*imag+b*real
        real, imag = real.square()-imag.square(), 2*real*imag
        remaining //= 2
    contrast = a.square()-b.square()
    O.require(a.lo > 0 and b.lo > 0 and contrast.lo > .0000840
              and contrast.hi < .0000841, "finite positive weak rotation")
    k2 = contrast.square()
    eta = (one-k2).sqrt()
    channel_error = k2/(one+eta)
    O.require(channel_error.hi < 3.54e-9, "coherent old-output disturbance")
    q = grid(QMIN,QMAX,512,False)
    c = one-2*q
    den = one-k2*c.square()
    w = power(p,14)
    h = w*((one+eta-2*k2)*c.square()+channel_error)/den
    dh = -4*w*c*(one+eta)*(one-k2)/den.square()
    z = I.rational(Z)
    gain = -dh/(one-z+z*h)
    O.require(np.min(gain.lo) > .0022, "disturbance can be small at positive cold gain")
    return {"positive_G_power_including_birth": 1048, "mark_contrast": bounds(contrast),
            "old_channel_diamond_error_upper": bounds(channel_error)[1],
            "cold_gain_divided_by_z": bounds(gain)}


def verify_ei14():
    raw = subprocess.check_output(["git", "show", f"{PARENT}:{EI14}"], cwd=REPO)
    primary = json.loads(raw)
    O.require(primary["status"] == "PASS" and primary["sign_words_each_orientation"] == 1024,
              "EI14 owner's exact truth table")
    lower, upper = Q("1.84369213362159864e-6"), Q("1.85870820040087242e-6")
    rounding = Q(1,2*10**24)
    O.require(lower < Q(primary["native_table_min"])-rounding
              and upper > Q(primary["native_table_max"])+rounding, "EI14 outward constants")
    width = upper-lower
    eta1, eta0 = width/lower, width/(1-upper)

    def log_bound(t):
        return sum(t**k/k for k in range(1,10)) + t**10/(10*(1-t))

    rate1, rate0 = [t*t/(1-t) for t in (eta1,eta0)]
    coefficient = [log_bound(eta1)+log_bound(eta0), rate1+rate0,
                   upper*rate1+(1-lower)*rate0]
    displayed = ("0.008178", "0.00006688", "0.0000000001244")
    O.require(all(value<Q(limit) for value,limit in zip(coefficient,displayed)),
              "relative-order C1 bounds")
    return {"primary_result_sha256": sha256(raw).hexdigest(),
            "C1_nats_coefficients_strict_upper": list(displayed)}


def main():
    verify_symbolic()
    print(json.dumps({
        "round": "B162",
        "exact_explicit_scratch_contraction_and_balanced_overlap": True,
        "retained_scratch_flag_distinguishability": "d, independent of k",
        "mark_only_flag_distinguishability": "lambda=d^(k+1)",
        "conditional_gain_bounds": verify_outward(),
        "balanced_rotated_pointer": verify_rotated_pointer(),
        "EI14_unattenuated_report": verify_ei14(),
        "full_physical_Cost_minus_Info": False,
        "GR_closed": False,
        "status": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
