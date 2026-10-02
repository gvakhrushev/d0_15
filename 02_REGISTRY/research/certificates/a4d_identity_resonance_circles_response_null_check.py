#!/usr/bin/env python3
"""Exact quadratic response-null identity on all six flat resonance circles.

This is not a torus zero census.  It consumes the already certified physical
circle kernel v(a) and proves coefficientwise that its Hermitian self-pair
metric moment vanishes for every a on the circle:
    v(a)^* D_Q A(a,a,i,i)[q] v(a) = 0
for all ten Gram directions and all three spatial permutations.  Real
coefficients give the three conjugate circles.

The proof reconstructs the solder derivative of the literal connection
symbol from the same face brackets used by the exact 0/1-solder response
certificate.  Its a-dependence has Laurent support {-1,0,1}; multiplying by
v(a)=c+a*l and v(a)^*=c^*+a^-1*l^* gives support {-2,...,2}.  Every Laurent
coefficient is checked exactly over Q(i).
"""
from __future__ import annotations

from fractions import Fraction as F
import sympy as sp
import numpy as np

import a4d_identity_physical_resonance_circles_check as P
import a4d_joint_response_solder01_defect_census_check as C


def ck(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def qitosp(x):
    return (sp.Rational(x.re.numerator, x.re.denominator)
            + sp.I * sp.Rational(x.im.numerator, x.im.denominator))


def derivative_face_forms(q_index):
    S = sp.eye(4)
    gram = S.T * C.ETA * S
    lift = S * gram.inv() * C.Q_DIRECTIONS[q_index] / 2
    fp = C.family_brackets(S + lift)
    fm = C.family_brackets(S - lift)
    out = []
    for (r1, s1, p), (r2, s2, m) in zip(fp, fm):
        assert (r1, s1) == (r2, s2)
        out.append((r1, s1, (sp.Matrix(p) - sp.Matrix(m)) / 2))
    return out


DFORMS = [derivative_face_forms(q) for q in range(10)]


def dconnection(forms, spatial, a, fixed=sp.I):
    phase = [fixed] * 4
    phase[0] = phase[spatial] = a
    return C.family_connection(forms, phase).applyfunc(sp.expand)


def circle_vectors(spatial):
    constant, linear, _coord = P.circle_kernel(spatial)
    return (sp.Matrix([qitosp(x) for x in constant]),
            sp.Matrix([qitosp(x) for x in linear]))


def laurent_coefficients(forms, spatial):
    # D(a)=D_-1/a + D_0 + D_+1*a.  The support bound follows directly
    # from the one direct and one inverse character factor in family_connection.
    plus = dconnection(forms, spatial, sp.Integer(1))
    minus = dconnection(forms, spatial, sp.Integer(-1))
    quarter = dconnection(forms, spatial, sp.I)
    zero = (plus + minus) / 2
    positive = (plus - zero + (quarter - zero) / sp.I) / 2
    negative = plus - zero - positive

    # Exact held-out interpolation control at a non-fourth-root unit character.
    held = sp.Rational(3, 5) + sp.I * sp.Rational(4, 5)
    actual = dconnection(forms, spatial, held)
    predicted = negative / held + zero + positive * held
    ck(f"HELD_OUT_DQA_LAURENT_SPATIAL_{spatial}",
       actual == predicted)
    return {-1: negative, 0: zero, 1: positive}


def self_pair_coefficients(spatial, q_index):
    c, l = circle_vectors(spatial)
    left = {0: sp.conjugate(c), -1: sp.conjugate(l)}
    right = {0: c, 1: l}
    dcoef = laurent_coefficients(DFORMS[q_index], spatial)
    coeff = {p: sp.Integer(0) for p in range(-2, 3)}
    for pl, vl in left.items():
        for pd, D in dcoef.items():
            for pr, vr in right.items():
                coeff[pl + pd + pr] += sp.expand((vl.T * D * vr)[0])
    return {p: sp.simplify(v) for p, v in coeff.items()}


def run():
    # The old flat L=4 exact census found 20 singular characters.  Independently
    # count the fourth-root samples of the six already certified circles.
    roots = (1, sp.I, -1, -sp.I)
    sampled = set()
    for fixed in (sp.I, -sp.I):
        for spatial in (1, 2, 3):
            for a in roots:
                phase = [fixed] * 4
                phase[0] = phase[spatial] = a
                sampled.add(tuple(phase))
    ck("SIX_CIRCLES_HAVE_20_DISTINCT_L4_SAMPLES", len(sampled) == 20)

    for spatial in (1, 2, 3):
        c, l = circle_vectors(spatial)
        for q in range(10):
            coeff = self_pair_coefficients(spatial, q)
            ck(f"SELF_PAIR_RESPONSE_NULL_S{spatial}_Q{q}",
               all(x == 0 for x in coeff.values()))

    print("RESULT A4D-IDENTITY-ALL-PHYSICAL-RESONANCE-CIRCLES-QUADRATIC-RESPONSE-NULL",
          flush=True)


if __name__ == "__main__":
    run()
