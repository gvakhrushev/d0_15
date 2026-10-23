#!/usr/bin/env python3
"""Independent exact finite full16 pp-wave preparation check.

Exact finite replay. No repository files are read or changed.
Uses all shifted true-adjoint rows of the actual degree-raising stencil,
not a continuum Hodge surrogate.  h=1, coframe inverse scale nu=1/5.
"""
import json
from itertools import product

import sympy as s


CREATORS = []
for a in range(4):
    matrix = s.zeros(16)
    for mask in range(16):
        if not (mask >> a) & 1:
            matrix[mask | (1 << a), mask] = (-1) ** (
                (mask & ((1 << a) - 1)).bit_count()
            )
    CREATORS.append(matrix)


def exterior(U):
    result = s.zeros(16)
    indices = [[j for j in range(4) if (mask >> j) & 1]
               for mask in range(16)]
    for i, I in enumerate(indices):
        for j, J in enumerate(indices):
            if len(I) == len(J):
                result[i, j] = U.extract(I, J).det()
    return result


ETA = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
N2 = s.zeros(4)
N2[1, 2] = N2[2, 0] = 1
N3 = s.zeros(4)
N3[1, 3] = N3[3, 0] = 1
ell = s.eye(4)[:, 1]
Omega = s.eye(16)[:, 15]
grade3 = CREATORS[1].T * Omega

# Direct nonunitary-control identities; Lambda(U) fixing grade3 is FALSE.
generator = s.Rational(1, 5) * N2 + s.Rational(2, 7) * N3
U = s.eye(4) + generator + generator * generator / 2
lift = exterior(U)
assert U.T * ETA * U == ETA and U.det() == 1 and U * ell == ell
assert lift.T * grade3 == grade3
assert CREATORS[1] * lift * grade3 == Omega
assert lift * grade3 != grade3

SIZES = (4, 3, 2, 2)
SITES = list(product(*map(range, SIZES)))
NU = s.Rational(1, 5)


def shift(site, role, sign):
    result = list(site)
    result[role] = (result[role] + sign) % SIZES[role]
    return tuple(result)


def create(vector):
    return sum((vector[a] * CREATORS[a] for a in range(4)), s.zeros(16))


CACHE = {}
LINK4 = {}
for site in SITES:
    u, v, x, y = site
    factor = s.Rational(1 + u, 25)
    H = factor * (x*x + 2*x*y + 3*y*y)
    generator = (
        factor * (x + y - s.Rational(1, 2)) * N2
        + factor * (x + 3*y - s.Rational(3, 2)) * N3
    )
    U = s.eye(4) + generator + generator * generator / 2
    assert U.T * ETA * U == ETA and U.det() == 1
    LINK4[site] = U
    vectors = [NU * s.eye(4)[:, 1],
               NU * (s.eye(4)[:, 0] - H/2 * s.eye(4)[:, 1]),
               NU * s.eye(4)[:, 2], NU * s.eye(4)[:, 3]]
    CACHE[site] = (
        [create(vector) for vector in vectors],
        [exterior(U)] + [s.eye(16)] * 3,
    )


def apply_D(field, site):
    result = s.zeros(16, 1)
    C_here, U_here = CACHE[site]
    for role in range(4):
        previous = shift(site, role, -1)
        C_previous, U_previous = CACHE[previous]
        # d = sum C(v(x)) [Lambda(U(x)) shift - I].
        result += C_here[role] * (
            U_here[role] * field[shift(site, role, 1)] - field[site]
        )
        # Its exact finite positive adjoint, including shifted endpoints.
        result += (
            U_previous[role].T * C_previous[role].T * field[previous]
            - C_here[role].T * field[site]
        )
    return result


basis = [s.eye(16)[:, 0], CREATORS[1] * s.eye(16)[:, 0], grade3, Omega]
rho = NU * (s.I - 1)
rho_bar = NU * (-s.I - 1)
expected = [(1, rho), (0, rho_bar), (3, rho), (2, rho_bar)]


def check_block():
    norm_squares = [s.expand(sum(entry**2 for entry in c*u))
                    for cs, us in CACHE.values() for c,u in zip(cs,us)]
    maximum_forward_frobenius_squared = max(norm_squares)
    assert maximum_forward_frobenius_squared < 1
    x0 = (0,0,0,0)
    x1 = shift(x0,2,1)
    face = LINK4[x0]*ETA*LINK4[x1].T*ETA
    assert face != s.eye(4)
    equalities = 0
    for vector, (target, coefficient) in zip(basis, expected):
        field = {site: s.I**site[0] * vector for site in SITES}
        for site in SITES:
            residual = apply_D(field, site) - s.I**site[0] * coefficient * basis[target]
            assert all(s.expand(entry) == 0 for entry in residual)
            equalities += 16

    return {
        "status": "PASS",
        "exact_component_equalities": equalities,
        "finite_sites": len(SITES),
        "full_CAR_dimension": 16,
        "proper_nonunitary_variable_links": True,
        "nonidentity_original_based_u_x_plaquette": True,
        "strict_full16_forward_Frobenius_squared_bound": str(maximum_forward_frobenius_squared),
        "wrong_LambdaU_fixes_grade3_control_rejected": True,
        "eigenvalue": str(s.simplify(rho * rho_bar)),
        "scope": "finite four-grade block; not full geometric/current/clock Euler",
    }


if __name__ == "__main__":
    print(json.dumps(check_block(), indent=2))
