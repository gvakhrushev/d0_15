#!/usr/bin/env python3
"""Narrow exact check of direct J source on the ORIGINAL CAR16 zero row.

Consumes 7cx861's complete original U, not a replacement dilation.
No new spectrum census, preparation, phase flow, or GR assertion.
"""
from pathlib import Path
import hashlib
import json
import sys
import sympy as s


def main():
    checked = []

    def zero(expr, name):
        if "--progress" in sys.argv:
            print(name, file=sys.stderr, flush=True)
        entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
        if any(s.cancel(s.expand(e)) != 0 for e in entries):
            raise ArithmeticError(name)
        checked.append(name)

    r, nu = s.symbols("r nu", real=True)
    p = (s.sqrt(5)-1)/2
    z = s.Rational(1, 2**20)
    eye = s.eye(16)
    order = (0, 2, 3, 1)
    creators = []
    for mode in range(4):
        c = s.zeros(16)
        before = order[:order.index(mode)]
        for bits in range(16):
            if not (bits >> mode) & 1:
                c[bits | (1 << mode), bits] = (-1)**sum(
                    (bits >> j) & 1 for j in before)
        creators.append(c)
    gen = creators[0]*creators[1].T+creators[1]*creators[0].T
    boost = eye+2*r/(1-r*r)*gen+2*r*r/(1-r*r)*gen*gen
    row = s.zeros(16)
    for j, c in enumerate(creators):
        b = nu*c
        x = (s.I*b, s.I*b*boost, -b, -s.I*b)[j]
        row += x+x.H-b-b.H
    row = (row/16).applyfunc(s.cancel)
    poly_p = 5*r**4+r**3-8*r*r-r+5
    poly_q = 23*r**4+6*r**3-32*r*r-10*r+25
    sm = nu*nu*poly_p/(64*(1-r*r)**2)
    tm = nu**4*poly_q/(16384*(1-r*r)**2)
    alpha = 1-4*z*p**4*tm
    eta = 4*z*p*p*(1-p*p*sm)
    den = alpha*alpha-alpha*eta*sm+eta*eta*tm
    base = {r: s.Rational(1, 9), nu: s.Rational(3, 5)}
    a = row.subs(base).applyfunc(s.expand)
    A = (a.H*a).applyfunc(s.expand)
    sb, tb = sm.subs(base), tm.subs(base)
    al, et, dd = [s.expand(x.subs(base)) for x in (alpha, eta, den)]
    C = (eye-2*p*p*A).applyfunc(s.expand)
    F = (4*p*p*A-4*p**4*A*A).applyfunc(s.expand)
    D = eye-z*F
    inv_numerator = ((al-et*sb)*eye+et*A).applyfunc(s.expand)
    rc_numerator = ((al-et*sb+2*p*p*et*tb)*eye
                    +(et-2*p*p*al)*A).applyfunc(s.expand)
    zero(A*A-sb*A+tb*eye, "owned quadratic identity at original fixture")
    zero(s.trace(A)-8*sb, "owned multiplicity trace at original fixture")
    zero(D-(al*eye-et*A), "full feedback pencil reduction")
    zero(D*inv_numerator-dd*eye, "resolvent without state inverse")
    zero(inv_numerator*C-rc_numerator, "short noncommutative source numerator")
    zero(F-(eye-C*C), "full completion feedback")

    # Two-root determinant product, symbolic and independent of an eigensolver.
    x, y, aa, ee = s.symbols("x y alpha eta")
    zero((aa-ee*x)*(aa-ee*y)-(aa*aa-aa*ee*(x+y)+ee*ee*x*y),
         "two-root determinant identity")
    Ai = ((sb*eye-A)/tb).applyfunc(s.expand)
    Z = 8*sb/tb
    rho = Ai/Z
    rhoi = (Z*A).applyfunc(s.expand)
    q = 64*p**3/Z
    sources = {}
    noncommuting = []
    for v in (r, nu):
        da = row.diff(v).subs(base).applyfunc(s.expand)
        dA = (da.H*a+a.H*da).applyfunc(s.expand)
        dF = (4*p*p*dA-4*p**4*(A*dA+dA*A)).applyfunc(s.expand)
        source_num = s.expand(z*s.trace(inv_numerator*dF))
        simple_num = 8*z*p*p*s.re(s.trace(rc_numerator*a.H*da))
        scalar_num = -8*s.diff(den, v).subs(base)
        zero(source_num-simple_num,
             f"full noncommutative source equals direct a jet: {v}")
        zero(source_num-scalar_num,
             f"direct source equals scalar determinant derivative: {v}")
        dZ = -s.trace(Ai*dA*Ai)
        drho = (-Ai*dA*Ai/Z-Ai*dZ/Z**2).applyfunc(s.expand)
        dq = -64*p**3*dZ/Z**2
        observed_num = z/(16*p)*(s.trace(rc_numerator*rhoi)*dq
                    -q*s.trace(rc_numerator*rhoi*rhoi*drho))
        zero(source_num-observed_num,
             f"moving q and rho recover same direct source: {v}")
        if any(s.cancel(e) != 0 for e in A*dA-dA*A):
            noncommuting.append(str(v))
        sources[str(v)] = str(s.N(source_num/dd, 35))
        if v == nu:
            zero(drho, "endogenous rho has no native scale derivative")
            missing_q_num = z/(16*p)*s.trace(rc_numerator*rhoi)*dq
            zero(source_num-missing_q_num,
                 "q carries entire original scale source")
            if s.simplify(source_num) == 0:
                raise ArithmeticError("frozen-q negative control failed")
            checked.append("freezing q incorrectly loses a nonzero scale source")
    if not noncommuting:
        raise ArithmeticError("native tangent noncommutation control missing")

    d0 = den.subs(nu, 0)
    d1 = s.diff(den, nu).subs(nu, 0)
    d2 = s.diff(den, nu, 2).subs(nu, 0)
    a1 = row.diff(nu)
    zero(d0-1, "singular-source zero-price pencil")
    zero(d1, "singular-source zero first derivative")
    zero(-8*(d2/d0-d1*d1/d0**2)-8*z*p*p*s.trace(a1.H*a1),
         "singular-source exact nonzero second derivative")
    singular_second = s.simplify((-8*d2).subs(r, base[r]))
    if not singular_second.is_positive:
        raise ArithmeticError("positive singular-source second derivative")
    checked.append("positive second source without inverse A")

    repo = Path(__file__).resolve().parents[3]
    owner = repo / "02_REGISTRY/research/certificates/a4d_original_car16_two_eigenvalue_closed_form_check.py"
    result = {
        "status": "PASS", "GR_closed": False,
        "input_commit": "e120d891985e473e7e9e0e8a9da92b6d1fab7218",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "consumed_car_owner_sha256": hashlib.sha256(owner.read_bytes()).hexdigest(),
        "checks": checked,
        "native_fixture": {"r": "1/9", "nu": "3/5", "z": "2^-20", "data_dimension": 16},
        "native_noncommuting_tangents": noncommuting,
        "direct_sources_diagnostic": sources,
        "singular_second_source_diagnostic": str(s.N(singular_second, 35)),
        "scope": "Exact algebra and original CAR16 jets; consumes complete U proof; no new full2048 replay or all42/native-admission theorem."
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
