#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Numeric diagnostic for the physical flat joint singular set on N=4,8,12.

This is deliberately a scout, not a theorem certificate.  It evaluates the
already coefficientwise-certified literal physical stencil J=(A^T;C) on root
grids and compares the observed singular points with the six exact resonance
circles.  Only N=4 is asserted against an owned theorem.  N=8,12 are printed
as diagnostics for deciding whether a global determinantal proof is worth
attempting.
"""
from __future__ import annotations

import cmath
import itertools
import numpy as np

import a4d_identity_physical_resonance_circles_check as P


def cpx(x):
    try:
        return complex(float(x))
    except TypeError:
        return complex(x)


def coeff_complex(x):
    # literal stencils use Fraction coefficients
    return complex(float(x), 0.0)


H = []
C = []
for shift, entries in P.H_LITERAL.items():
    H.append((shift, [(r,c,coeff_complex(v)) for (r,c),v in entries.items()]))
for shift, entries in P.C_LITERAL.items():
    C.append((shift, [(r,c,coeff_complex(v)) for (r,c),v in entries.items()]))


def eval_joint(z):
    J = np.zeros((34,24), dtype=np.complex128)
    for off,terms in ((0,H),(24,C)):
        for shift,entries in terms:
            phase = 1+0j
            for q,p in zip(z,shift):
                if p:
                    phase *= q**p
            for r,c,v in entries:
                J[off+r,c] += phase*v
    return J


def nullity(z):
    s = np.linalg.svd(eval_joint(z), compute_uv=False)
    tol = 1e-8 * max(1.0, float(s[0]))
    return int(np.sum(s <= tol))


def near(a,b,tol=1e-8):
    return abs(a-b) < tol


def on_owned_circle(z):
    for fixed in (1j,-1j):
        for spatial in (1,2,3):
            other = [j for j in (1,2,3) if j != spatial]
            if (near(z[other[0]],fixed) and near(z[other[1]],fixed)
                    and near(z[0],z[spatial])):
                return True
    return False


def scan(N):
    roots = [cmath.exp(2j*cmath.pi*k/N) for k in range(N)]
    singular = []
    outside = []
    total_null = 0
    hist = {}
    for z in itertools.product(roots, repeat=4):
        d = nullity(z)
        if d:
            singular.append(z)
            total_null += d
            hist[d] = hist.get(d,0)+1
            if not on_owned_circle(z):
                outside.append((z,d))
    expected_points = 6*N-4
    expected_total = 6*N+2
    print(
        "SCOUT_N",N,
        "SINGULAR_POINTS",len(singular),
        "TOTAL_NULLITY",total_null,
        "NULLITY_HIST",sorted(hist.items()),
        "OWNED_CIRCLE_POINTS_EXPECTED",expected_points,
        "OWNED_CIRCLE_TOTAL_NULLITY_EXPECTED",expected_total,
        "OUTSIDE_OWNED_CIRCLES",len(outside),
        flush=True,
    )
    for z,d in outside[:12]:
        print("SCOUT_OUTSIDE",N,tuple(complex(round(x.real,6),round(x.imag,6)) for x in z),d,flush=True)
    return len(singular),total_null,outside


def main():
    p4,n4,o4 = scan(4)
    assert p4 == 20 and n4 == 26 and not o4
    print("PASS_OWNED_L4_CENSUS_MATCHES_SIX_CIRCLES",flush=True)
    scan(8)
    scan(12)
    print("SCOUT_ONLY_NO_GLOBAL_LOCUS_CLAIM",flush=True)


if __name__ == "__main__":
    main()
