#!/usr/bin/env python3
"""Independent first-source control, using the exact finite full16 fixture.

Run next to check_exact_finite_block.py. The first two quartet grades
have zero independent Lorentz link Rayleigh first sources.  Their Hodge
partners need not have zero sources.  Neither assertion is full H+J+R
geometry stationarity.
"""
import json

import sympy as s

import check_exact_finite_block as m

generators = []
for a in range(4):
    for b in range(a + 1, 4):
        antisymmetric = s.zeros(4)
        antisymmetric[a, b] = 1
        antisymmetric[b, a] = -1
        X = m.ETA * antisymmetric
        assert X.T * m.ETA + m.ETA * X == s.zeros(4)
        Gamma = sum((X[i, j] * m.CREATORS[i] * m.CREATORS[j].T
                     for i in range(4) for j in range(4)), s.zeros(16))
        generators.append(Gamma)

site = (0, 0, 1, 1)
nonzero_complementary_sources = []
zero_sources = 0
for internal in range(4):
    field = {x: s.I**x[0] * m.basis[internal] for x in m.SITES}
    target, coefficient = m.expected[internal]
    Dfield = {x: s.I**x[0] * coefficient * m.basis[target] for x in m.SITES}
    for role in range(4):
        next_site = m.shift(site, role, 1)
        C, U = m.CACHE[site]
        for generator_index, Gamma in enumerate(generators):
            # Genuine independent left-trivialized proper-Lorentz tangent.
            d_lift = Gamma * U[role]
            # Only the two incident d/d^dagger rows change.
            dD_here = C[role] * d_lift * field[next_site]
            dD_next = d_lift.T * C[role].T * field[site]
            derivative = s.simplify(2 * s.re(
                (Dfield[site].conjugate().T * dD_here)[0]
                + (Dfield[next_site].conjugate().T * dD_next)[0]
            ))
            if internal < 2:
                assert derivative == 0, (internal, role, generator_index, derivative)
                zero_sources += 1
            elif derivative != 0:
                nonzero_complementary_sources.append({
                    "quartet_internal_index": internal,
                    "role": role,
                    "Lorentz_generator_index": generator_index,
                    "unnormalized_Rayleigh_first_source": str(derivative),
                })

assert nonzero_complementary_sources
# Genuine nonlinear native-R square, with a proper opposite-null link
# perturbation. All complement components and the true adjoint are evaluated.
barN2 = s.zeros(4)
barN2[0, 2] = barN2[2, 1] = 1
step = s.Rational(1, 11) * barN2
perturb = s.eye(4) + step + step*step/2
old_create, old_lifts = m.CACHE[site]
# Existing exact null matrix at this source basepoint.
u, v, x, y = site
factor = s.Rational(1 + u, 25)
g = factor*(x+y-s.Rational(1,2))*m.N2 + factor*(x+3*y-s.Rational(3,2))*m.N3
oldU = s.eye(4)+g+g*g/2
changedU = perturb*oldU
assert changedU.T*m.ETA*changedU == m.ETA and changedU.det() == 1
changed_lifts = list(old_lifts)
changed_lifts[0] = m.exterior(changedU)
m.CACHE[site] = (old_create, changed_lifts)
def norm2(vector):
    return s.expand((vector.conjugate().T*vector)[0])
energies=[]
for internal in [0,1]:
    field={q:s.I**q[0]*m.basis[internal] for q in m.SITES}
    energies.append(s.simplify(sum(norm2(m.apply_D(field,q)) for q in m.SITES)/len(m.SITES)))
expected_lambda=s.Rational(2,25)
assert energies[0] == expected_lambda
# At a single changed u-edge, the exact raising-square addition is this vector.
raised=old_create[0]*(changed_lifts[0]-old_lifts[0])*m.basis[1]
penalty=s.simplify(norm2(raised)/len(m.SITES))
assert penalty > 0 and s.simplify(energies[1]-expected_lambda-penalty) == 0
m.CACHE[site] = (old_create, old_lifts)
print(json.dumps({
    "status": "PASS",
    "tested_edge_basepoint": list(site),
    "exact_zero_grade0_plus_grade1_sources": zero_sources,
    "all_six_independent_Lorentz_generators": True,
    "nonlinear_proper_link_R_addition": str(penalty),
    "grade0_R_stays_constant": str(energies[0]),
    "grade1_R_equals_baseline_plus_actual_d_square": str(energies[1]),
    "all_four_link_directions": True,
    "nonzero_complementary_grade3_plus_grade4_sources": nonzero_complementary_sources,
    "normalization": "All displayed first sources divide by 48 for normalized plane states.",
    "scope": "Rayleigh link partial sources; not whole-price or metric/current stationarity",
}, indent=2))
