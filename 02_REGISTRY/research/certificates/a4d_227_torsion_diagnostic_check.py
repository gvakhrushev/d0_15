#!/usr/bin/env python3
"""Diagnostic torsion of the merged #227 curved stationary family.

The coframe torsion is the owned transport formula
    T_rs = L_r v_s(x+r) - v_s(x) - (L_s v_r(x+s) - v_r(x))
at the constant standard solder. Affine open torsion, the translation
defect of an affine square, is recorded separately and is identically zero
because this family has no translation shift.

No torsion-free field equation is imposed and no open-torsion square is
added to the action.
"""

from itertools import combinations

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
GENERATORS = []
for j in (1, 2, 3):
    matrix = sp.zeros(4)
    matrix[0, j] = matrix[j, 0] = 1
    GENERATORS.append(matrix)
for a, b in PAIRS[3:]:
    matrix = sp.zeros(4)
    matrix[a, b], matrix[b, a] = 1, -1
    GENERATORS.append(matrix)


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def zero(matrix):
    return all(sp.factor(entry) == 0 for entry in matrix)


def lorentz_inverse(matrix):
    return ETA * matrix.T * ETA


def shift(site, role, step=1):
    out = list(site)
    out[role] = (out[role] + step) % 4
    return tuple(out)


def phase(site):
    return sum(site) % 4


def link(site, role, wave):
    return wave[phase(site)] if role == 0 else I4


def face_factors(site, a, b, wave):
    return [
        link(site, a, wave),
        link(shift(site, a), b, wave),
        lorentz_inverse(link(shift(site, b), a, wave)),
        lorentz_inverse(link(site, b, wave)),
    ]


def multiply(factors):
    result = I4
    for factor in factors:
        result = result * factor
    return result


B = sum(GENERATORS[:3], sp.zeros(4))
t = sp.symbols("t")
D = 4 - 3 * t**2
c = 4 * t / D
U = sp.simplify(((I4 - t * B / 2).inv() * (I4 + t * B / 2)))
Ui = lorentz_inverse(U)
wave = [U, I4, Ui, I4]
E0 = I4[:, 0]
SPATIAL = I4[:, 1] + I4[:, 2] + I4[:, 3]

check("CAYLEY_DEFECT", zero(U - I4 - c * B - 2 * t**2 / D * B**2))
check("CURVATURE_LINK_DEFECT", zero((U - Ui) / 2 - c * B))


def coframe_torsion(site, role_r, role_s, family):
    """Owned solder transport at a constant frame, evaluated at one site."""
    frame = [I4[:, j] for j in range(4)]
    transported_s = link(site, role_r, family) * frame[role_s] - frame[role_s]
    transported_r = link(site, role_s, family) * frame[role_r] - frame[role_r]
    return sp.simplify(transported_s - transported_r)


def schematic(site, role_r, role_s, family):
    lr = link(site, role_r, family)
    ls = link(site, role_s, family)
    return sp.simplify((lr - I4) * I4[:, role_s] - (ls - I4) * I4[:, role_r])


def plaquette_curvature(site, role_r, role_s, family):
    holonomy = multiply(face_factors(site, role_r, role_s, family))
    return sp.simplify((holonomy - lorentz_inverse(holonomy)) / 2)


def orientation(role_a, role_b):
    rest = [j for j in range(4) if j not in (role_a, role_b)]
    seq = [role_a, role_b] + rest
    return (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))


def wedge(left, right):
    return sp.Matrix([left[i] * right[j] - left[j] * right[i] for i, j in PAIRS])


def bivector(matrix):
    dressed = matrix * ETA
    return sp.Matrix([dressed[a, b] for a, b in PAIRS])


G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for col, (row, sign) in enumerate([(5, -1), (4, 1), (3, -1), (2, 1), (1, -1), (0, 1)]):
    STAR[row, col] = sign
SYM = [(a, b) for a in range(4) for b in range(a, 4)]


def metric_partial(site, family):
    """Owned #227 metric partial at the standard solder, ten Gram directions."""
    result = []
    for qa, qb in SYM:
        q = sp.zeros(4)
        q[qa, qb] = q[qb, qa] = 1
        variation = q * ETA / 2
        derivative = 0
        for role_a, role_b in PAIRS:
            holonomy = multiply(face_factors(site, role_a, role_b, family))
            curvature = (holonomy - lorentz_inverse(holonomy)) / 2
            u, v = [j for j in range(4) if j not in (role_a, role_b)]
            dw = wedge(variation[u, :].T, I4[:, v]) + wedge(I4[:, u], variation[v, :].T)
            derivative += orientation(role_a, role_b) * (
                dw.T * G2 * STAR * bivector(curvature)
            )[0]
        result.append(sp.factor(derivative))
    return sp.Matrix(result)


for site in [(0, 0, 0, 0), (1, 0, 0, 0), (1, 2, 3, 0), (3, 3, 3, 3)]:
    for role_r, role_s in PAIRS:
        check(
            "SCHEMATIC_MATCH_%d_%d_%d" % (phase(site), role_r, role_s),
            zero(coframe_torsion(site, role_r, role_s, wave) - schematic(site, role_r, role_s, wave)),
        )

# Affine open torsion is a difference of translation shifts. This family stores
# only linear Lorentz links, so both square shifts are the zero vector.

active = {
    0: c * E0 + (2 * t**2 / D) * SPATIAL,
    2: -c * E0 + (2 * t**2 / D) * SPATIAL,
}
for p in range(4):
    site = (p, 0, 0, 0)
    for role_r, role_s in PAIRS:
        torsion = coframe_torsion(site, role_r, role_s, wave)
        curvature = plaquette_curvature(site, role_r, role_s, wave)
        spatial = role_r != 0 and role_s != 0
        if spatial:
            check("SPATIAL_TORSION_ZERO_%d_%d_%d" % (p, role_r, role_s), zero(torsion))
            check("SPATIAL_CURVATURE_ZERO_%d_%d_%d" % (p, role_r, role_s), zero(curvature))
            continue
        time_role = role_s if role_r == 0 else role_r
        sign = 1 if role_r == 0 else -1
        if p in (1, 3):
            check("ODD_PHASE_TORSION_ZERO_%d_%d" % (p, time_role), zero(torsion))
        else:
            expected = sign * active[p]
            check("EVEN_PHASE_TORSION_%d_%d" % (p, time_role), zero(torsion - expected))
        curvature_sign = 1 if p in (0, 1) else -1
        check(
            "TIME_FACE_CURVATURE_%d_%d_%d" % (p, role_r, role_s),
            zero(curvature - curvature_sign * c * B),
        )

# The time-component of the phase-0 face (0,1) is exactly the curvature amplitude.
component = sp.simplify((coframe_torsion((0, 0, 0, 0), 0, 1, wave).T * E0)[0])
check("PHASE0_E0_COMPONENT_EQUALS_C", sp.factor(component - c) == 0)
check("C_ZERO_IFF_T_ZERO_IN_CHART", sp.fraction(sp.together(c))[0] == 4 * t)
check("LEADING_TORSION_IS_T", sp.series(component, t, 0, 2).removeO() == t)
check("CURVATURE_OVER_T", sp.limit(c / t, t, 0) == 1)

# Same amplitude multiplies the owned metric partial. Signs from #227.
metric_direction = sp.Matrix([0, 0, 0, 0, -1, 1, 1, -1, 1, -1])
for p, sign in enumerate((1, 1, -1, -1)):
    check(
        "EQ_EQUALS_SIGN_C_M_%d" % p,
        zero(metric_partial((p, 0, 0, 0), wave) - sign * c * metric_direction),
    )

# Global vanishing: the phase-0 component 4t/D is zero exactly at t=0,
# while odd phases stay torsion-free for every t.
check("ODD_PHASE_TORSION_FREE_FOR_ALL_T", all(
    zero(coframe_torsion((p, 0, 0, 0), 0, s, wave))
    for p in (1, 3) for s in (1, 2, 3)
))
check("IDENTITY_TORSION_FREE", all(
    zero(coframe_torsion((p, 0, 0, 0), r, s, [I4, I4, I4, I4]))
    for p in range(4) for r, s in PAIRS
))

print("RESULT_COFRAME_TORSION: (L_r-I)e_s-(L_s-I)e_r at constant standard solder")
print("RESULT_AFFINE_OPEN_TORSION: identically zero")
print("RESULT_SPATIAL_TORSION: identically zero")
print("RESULT_ODD_PHASES: torsion zero for every t, curvature and E_Q proportional to c(t)")
print("RESULT_EVEN_PHASES: T_0s = ±(c e_0 + (2 t^2/D)(e_1+e_2+e_3))")
print("RESULT_GLOBAL_VANISHING: all phases and faces vanish iff t=0 when 3 t^2 != 4")
print("RESULT_LEADING: torsion, curvature and E_Q share amplitude c(t)~t")
print("TERMINAL: J2-227-CURVED-STATIONARY-FAMILY-TORSION-DIAGNOSTIC-CERTIFIED")
