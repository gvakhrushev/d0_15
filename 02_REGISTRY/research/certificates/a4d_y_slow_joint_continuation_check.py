#!/usr/bin/env python3
"""Exact primary-scaling bridge from the #259 Y slow lift to the #260 N0 sector.

Task: WRK-A4D-Y-SLOW-JOINT-CONTINUATION

The merged #259 owner solves the order-h connection forcing at fixed
microstructure amplitude z.  This checker:

1. re-executes that owner and computes its first unresolved fixed-z h^2
   connection forcing on all 96 phase/role/Lorentz equations;
2. specializes the primary scaling z=h and extracts the total h^3 forcing;
3. builds the exact flat real period-4 connection Hessian L0 and metric
   readout M0 using integer doubled matrices;
4. proves rank L0=80, nullity 16, while rank [L0;M0]=88;
5. proves the remaining 8-real joint-invisible kernel is exactly the
   cosine/sine realification of the four complex diagonal N0 vectors owned
   by #252/#260;
6. constructs an exact next range correction for the h^3 forcing and proves
   that its metric response cancels the complete #259 h^3 slope response.

This is a primary-scaling continuation theorem.  It does not solve the
nonlinear slow-background equations on the residual N0 sector; that is the
remaining bridge to the degree-5 real-ray problem in #260.

Terminal:
J2-Y-SLOW-PRIMARY-SCALING-RANGE-RESPONSE-REDUCES-TO-N0
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
OWNER = HERE / "a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py"


def check(name: str, cond: bool, detail: str = "") -> None:
    if not cond:
        raise AssertionError(name + (": " + detail if detail else ""))
    print("PASS_" + name)


# ---------------------------------------------------------------------------
# 1. Execute the merged #259 owner and compute the next fixed-z forcing.
# ---------------------------------------------------------------------------

spec = importlib.util.spec_from_file_location("_y259_owner", OWNER)
owner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(owner)

z, h, x0 = owner.z, owner.h, owner.x0
D = 3 * z**2 + 4

labels = [(p, r, g) for p in range(4) for r in range(4) for g in range(6)]
forcing2: dict[tuple[int, int, int], sp.Expr] = {}
for p in range(4):
    site = (p, 0, 0, 0)
    for role in range(4):
        for gi, gen in enumerate(owner.GENERATORS):
            value = owner.edge_euler(site, role, gen, owner.wave, owner.solder)
            series = sp.series(sp.together(value), h, 0, 3).removeO()
            c2 = sp.factor(series.coeff(h, 2))
            if c2 != 0:
                forcing2[(p, role, gi)] = c2

expected_forcing2 = {
    (1, 0, 0): z**2 * (z - 2) / D**2,
    (1, 0, 1): -z**2 * (z - 2) / D**2,
    (1, 0, 3): -2 * x0 * z / D,
    (1, 0, 4): 2 * x0 * z / D,
    (1, 0, 5): 4 * x0 * z / D,
    (3, 0, 0): -z**2 * (z - 2) / D**2,
    (3, 0, 1): z**2 * (z - 2) / D**2,
    (3, 0, 3): 2 * x0 * z / D,
    (3, 0, 4): -2 * x0 * z / D,
    (3, 0, 5): -4 * x0 * z / D,
}
check(
    "FIXED_Z_ORDER_H2_FORCING",
    forcing2.keys() == expected_forcing2.keys()
    and all(sp.factor(forcing2[k] - v) == 0 for k, v in expected_forcing2.items()),
)

# For h^2 f2(z), putting z=h gives a total h^3 term only from the x0*z
# entries.  Factor x0 out.  Store 4*f3 so every coordinate is integral.
s4 = np.zeros(96, dtype=np.int64)
def li(label):
    return labels.index(label)

s4[li((1, 0, 3))] = -2
s4[li((1, 0, 4))] = 2
s4[li((1, 0, 5))] = 4
s4[li((3, 0, 3))] = 2
s4[li((3, 0, 4))] = -2
s4[li((3, 0, 5))] = -4

# ---------------------------------------------------------------------------
# 2. Exact doubled flat period-4 connection Hessian L2 = 2 L0.
# ---------------------------------------------------------------------------

ETA = np.diag([1, -1, -1, -1]).astype(np.int64)
I4 = np.eye(4, dtype=np.int64)
Z4 = np.zeros((4, 4), dtype=np.int64)
GEN = [np.array(g.tolist(), dtype=np.int64) for g in owner.GENERATORS]
PAIRS = list(owner.PAIRS)
G2 = np.array(owner.G2.tolist(), dtype=np.int64)
STAR = np.array(owner.STAR.tolist(), dtype=np.int64)
BASIS = [I4[:, r] for r in range(4)]


def phase(site):
    return sum(site) % 4


def shift(site, role, step=1):
    out = list(site)
    out[role] = (out[role] + step) % 4
    return tuple(out)


def orient(a, b):
    rest = [j for j in range(4) if j not in (a, b)]
    seq = [a, b] + rest
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def wedge(u, v):
    return np.array([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS], dtype=np.int64)


def bivector(matrix):
    dressed = matrix @ ETA
    return np.array([dressed[a, b] for a, b in PAIRS], dtype=np.int64)


FACE_ROW = {}
for a, b in PAIRS:
    u, v = [j for j in range(4) if j not in (a, b)]
    FACE_ROW[(a, b)] = orient(a, b) * (wedge(BASIS[u], BASIS[v]) @ G2 @ STAR)


def dual_mul(left, right):
    a0, a1 = left
    b0, b1 = right
    return a0 @ b0, a0 @ b1 + a1 @ b0


def dual_product(factors):
    out = (I4, Z4)
    for factor in factors:
        out = dual_mul(out, factor)
    return out


def input_factor(loc, role, inverted, in_phase, in_role, generator):
    if role != in_role or phase(loc) != in_phase:
        return I4, Z4
    return I4, (-generator if inverted else generator)


def doubled_hessian_entry(out_phase, out_role, out_gen, in_phase, in_role, in_gen):
    site = (out_phase, 0, 0, 0)
    test = GEN[out_gen]
    source = GEN[in_gen]
    total = 0
    for a, b in PAIRS:
        if out_role == a:
            corners = [(site, 0), (shift(site, b, -1), 2)]
        elif out_role == b:
            corners = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base, corner in corners:
            places = [
                (base, a, False),
                (shift(base, a), b, False),
                (shift(base, b), a, True),
                (base, b, True),
            ]
            factors = [
                input_factor(loc, role, inverted, in_phase, in_role, source)
                for loc, role, inverted in places
            ]
            _hol0, hol1 = dual_product(factors)

            varied = list(factors)
            _f0, f1 = varied[corner]
            if corner < 2:
                varied[corner] = (test, f1 @ test)
            else:
                varied[corner] = (-test, -test @ f1)
            dp0, dp1 = dual_product(varied)

            # At the identity plaquette, twice the first derivative of
            # (dp + P^{-1} dp P^{-1})/2 is integral.
            two_dc1 = 2 * dp1 - hol1 @ dp0 - dp0 @ hol1
            total += int(FACE_ROW[(a, b)] @ bivector(two_dc1))
    return total


L2 = np.zeros((96, 96), dtype=np.int64)
for oi, (op, orole, og) in enumerate(labels):
    for ii, (ip, irole, ig) in enumerate(labels):
        L2[oi, ii] = doubled_hessian_entry(op, orole, og, ip, irole, ig)

check("L2_ENTRIES", set(np.unique(L2)).issubset({-1, 0, 1}))
check("L2_SYMMETRIC", np.array_equal(L2, L2.T))
rank_L = sp.Matrix(L2.tolist()).rank()
check("L0_RANK_80", rank_L == 80, str(rank_L))
check("L0_NULLITY_16", 96 - rank_L == 16)

# ---------------------------------------------------------------------------
# 3. Exact doubled pointwise metric readout M2 = 2 M0.
# ---------------------------------------------------------------------------

SYM = [(a, b) for a in range(4) for b in range(a, 4)]


def metric_column(in_phase, in_role, in_gen):
    source = GEN[in_gen]
    out = np.zeros(40, dtype=np.int64)
    for p in range(4):
        site = (p, 0, 0, 0)
        for qi, (qa, qb) in enumerate(SYM):
            q = np.zeros((4, 4), dtype=np.int64)
            q[qa, qb] = 1
            q[qb, qa] = 1
            # two_var is twice the Gram lift q*eta/2.
            two_var = q @ ETA
            total = 0
            for a, b in PAIRS:
                dP = np.zeros((4, 4), dtype=np.int64)
                for loc, role, sign in (
                    (site, a, 1),
                    (shift(site, a), b, 1),
                    (shift(site, b), a, -1),
                    (site, b, -1),
                ):
                    if role == in_role and phase(loc) == in_phase:
                        dP += sign * source
                u, v = [j for j in range(4) if j not in (a, b)]
                two_dw = wedge(two_var[u, :], BASIS[v]) + wedge(BASIS[u], two_var[v, :])
                total += int(orient(a, b) * (two_dw @ G2 @ STAR @ bivector(dP)))
            out[10 * p + qi] = total
    return out


M2 = np.zeros((40, 96), dtype=np.int64)
for ii, (ip, irole, ig) in enumerate(labels):
    M2[:, ii] = metric_column(ip, irole, ig)

check("M2_ENTRIES", set(np.unique(M2)).issubset({-1, 0, 1}))
rank_joint = sp.Matrix(np.vstack([L2, M2]).tolist()).rank()
check("JOINT_STACK_RANK_88", rank_joint == 88, str(rank_joint))
check("JOINT_INVISIBLE_REAL_DIM_8", 96 - rank_joint == 8)
check("METRIC_VISIBLE_PART_OF_CONNECTION_KERNEL_DIM_8", rank_joint - rank_L == 8)

# ---------------------------------------------------------------------------
# 4. Identify the 8-real stack kernel with the owned #260 N0 realification.
# ---------------------------------------------------------------------------

n0 = [
    (0, [0, 0, 0, 1, -1, 1]),
    (1, [0, 1, -1, 0, 0, 1]),
    (2, [1, 0, -1, 0, 1, 0]),
    (3, [1, -1, 0, 1, 0, 0]),
]
cosine = [1, 0, -1, 0]
sine = [0, 1, 0, -1]
cols = []
for role, weights in n0:
    for dressing in (cosine, sine):
        vec = np.zeros(96, dtype=np.int64)
        for p in range(4):
            for gi, coefficient in enumerate(weights):
                vec[li((p, role, gi))] = dressing[p] * coefficient
        cols.append(vec)
N0real = np.stack(cols, axis=1)

check("N0_REAL_RANK_8", sp.Matrix(N0real.tolist()).rank() == 8)
check("N0_REAL_IN_CONNECTION_KERNEL", np.array_equal(L2 @ N0real, np.zeros((96, 8), dtype=np.int64)))
check("N0_REAL_METRIC_INVISIBLE", np.array_equal(M2 @ N0real, np.zeros((40, 8), dtype=np.int64)))
# Since the stack nullity is exactly 8, these inclusions prove equality.
print("EXACT_KERNEL_IDENTIFICATION: ker[L0;M0] = realification(span{lambda1,lambda3,lambda4,lambda6}).")

# ---------------------------------------------------------------------------
# 5. Primary z=h next range correction and metric cancellation.
# ---------------------------------------------------------------------------

# Write r3 = (x0/2) * x2 in the 96 real link coordinates.
x2 = np.zeros(96, dtype=np.int64)
x2[li((0, 0, 1))] = 1
x2[li((0, 0, 2))] = -1
x2[li((2, 0, 1))] = -1
x2[li((2, 0, 2))] = 1

# L0=L2/2, r3=x0*x2/2, and f3=x0*s4/4.
# Therefore L0*r3+f3 = x0*(L2*x2+s4)/4.
check("PRIMARY_H3_RANGE_CORRECTION", np.array_equal(L2 @ x2 + s4, np.zeros(96, dtype=np.int64)))

# The #259 fixed-z order-h^2 metric jet has, at z=h, the h^3 slope
# coefficient below (four times the coefficient, with x0 factored out).
signs = [1, 1, -1, -1]
base4 = np.zeros(40, dtype=np.int64)
for p, sign in enumerate(signs):
    base4[10 * p + 5] = -sign
    base4[10 * p + 6] = sign
    base4[10 * p + 7] = -sign
    base4[10 * p + 9] = sign

# M0*r3 = x0*M2*x2/4.  It exactly cancels the complete h^3 response.
check("PRIMARY_H3_METRIC_RESPONSE_CANCELS",
      np.array_equal(base4 + M2 @ x2, np.zeros(40, dtype=np.int64)))

print("L0_RANK", rank_L)
print("L0_NULLITY", 96 - rank_L)
print("JOINT_STACK_RANK", rank_joint)
print("JOINT_INVISIBLE_DIM_REAL", 96 - rank_joint)
print("PRIMARY_H3_CORRECTION_NONZERO", [
    (labels[i], int(x2[i])) for i in range(96) if x2[i]
])
print("PRIMARY_H3_RESPONSE: CANCELLED exactly on the canonical range correction.")
print("SOURCE_CONTRACT: at total order h^2, the 16-real homogeneous connection freedom")
print("splits into 8 source-visible directions and the exact 8-real #260 N0 sector.")
print("BOUNDARY: nonlinear slow-background continuation inside N0 is not solved by the range calculation above.")

# ---------------------------------------------------------------------------
# 6. Primary-scaling slow-background cross operator on N0^real.
#
# Latest #260 proves that the selected constant-solder real ray has an
# orthogonal degree-3 Euler outside all frozen phase-dependent link images.
# That is not yet the slow-background verdict.  On the primary z=h scaling
# the residual N0 freedom enters naturally at order h^2.  Its cubic
# self-interaction is therefore order h^6; the first relevant term is instead
# the h^3 cross term with the O(h) Y microstructure / slow solder.
#
# Compute that exact 96 x 8 map on the entire owned N0^real carrier and test
# its Fredholm class against the already-owned flat operator L0.
# ---------------------------------------------------------------------------

aa = sp.symbols("aa")
SETA = owner.ETA
SI4 = owner.I4
SGEN = list(owner.GENERATORS)
SG2 = owner.G2
SSTAR = owner.STAR
SBASIS = [SI4[:, r] for r in range(4)]
U_h = sp.simplify(owner.U.subs(z, h))
Ui_h = sp.simplify(owner.Ui.subs(z, h))
slow_solder_1 = SI4 + h * (owner.alpha * SETA / 2).T


def _s_lorentz_inverse(matrix):
    return SETA * matrix.T * SETA


def _s_wedge(left, right):
    return sp.Matrix([
        left[i] * right[j] - left[j] * right[i]
        for i, j in owner.PAIRS
    ])


def _s_bivector(matrix):
    dressed = matrix * SETA
    return sp.Matrix([dressed[a, b] for a, b in owner.PAIRS])


def _n0_tangent(column, p, role):
    out = sp.zeros(4)
    for gi in range(6):
        coefficient = int(N0real[li((p, role, gi)), column])
        if coefficient:
            out += coefficient * SGEN[gi]
    return out


def _background_link(p, role):
    if role != 0:
        return SI4
    if p == 0:
        return U_h
    if p == 2:
        return Ui_h
    return SI4


def _n0_link(column, loc, role):
    p = phase(loc)
    base = _background_link(p, role)
    tangent = _n0_tangent(column, p, role)
    # Only the derivative at aa=0 is used.  Since the N0 amplitude is h^2,
    # omitted O(aa^2 h^4) terms cannot contribute to the linear h^3 cross map.
    return base * (SI4 + aa * h**2 * tangent)


def _slow_n0_edge_euler(column, site, role, generator):
    result = sp.Integer(0)
    for a, b in owner.PAIRS:
        if role == a:
            corners = [(site, 0), (shift(site, b, -1), 2)]
        elif role == b:
            corners = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base_site, corner in corners:
            places = [
                (base_site, a, False),
                (shift(base_site, a), b, False),
                (shift(base_site, b), a, True),
                (base_site, b, True),
            ]
            factors = []
            for loc, rel, inverted in places:
                link = _n0_link(column, loc, rel)
                factors.append(_s_lorentz_inverse(link) if inverted else link)
            plaquette = factors[0] * factors[1] * factors[2] * factors[3]
            pinv = _s_lorentz_inverse(plaquette)
            varied = list(factors)
            if corner < 2:
                varied[corner] = factors[corner] * generator
            else:
                varied[corner] = -generator * factors[corner]
            dp = varied[0] * varied[1] * varied[2] * varied[3]
            dc = (dp + pinv * dp * pinv) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            area = _s_wedge(slow_solder_1[:, u], slow_solder_1[:, v])
            result += owner.orientation(a, b) * (
                area.T * SG2 * SSTAR * _s_bivector(dc)
            )[0]
    return sp.together(result)


cross_h3 = sp.zeros(96, 8)
for column in range(8):
    no_h2 = True
    for oi, (p, role, gi) in enumerate(labels):
        value = _slow_n0_edge_euler(column, (p, 0, 0, 0), role, SGEN[gi])
        linear = sp.diff(value, aa).subs(aa, 0)
        series = sp.series(sp.together(linear), h, 0, 4).removeO()
        expanded = sp.expand(series)
        # N0 is an exact flat kernel: an h^2 amplitude must have no order-h^2
        # Euler before the O(h) background is inserted.
        no_h2 &= sp.simplify(expanded.coeff(h, 2)) == 0
        cross_h3[oi, column] = sp.factor(expanded.coeff(h, 3))
    check("N0_CROSS_COL_%d_NO_H2" % column, no_h2)
    print("N0_CROSS_PROGRESS", column, flush=True)

rank_cross = L2.rank() if isinstance(L2, sp.MatrixBase) else sp.Matrix(L2.tolist()).rank()
L2sp = sp.Matrix(L2.tolist())
aug_cross = L2sp.row_join(cross_h3)
rank_aug_cross = aug_cross.rank()
fredholm_rank = rank_aug_cross - rank_L
surviving_n0_dim = 8 - fredholm_rank

check("N0_CROSS_BASE_RANK_STILL_80", rank_cross == 80, str(rank_cross))
check(
    "N0_SLOW_CROSS_FREDHOLM_RANK_BOUNDED",
    0 <= fredholm_rank <= 8,
    str(fredholm_rank),
)

# Exact left-kernel projection gives the same obstruction rank and makes the
# carrier boundary explicit.
left_kernel = L2sp.T.nullspace()
check("L0_LEFT_KERNEL_DIM_16", len(left_kernel) == 16, str(len(left_kernel)))
left_matrix = sp.Matrix.vstack(*[v.T for v in left_kernel])
projected_cross = sp.simplify(left_matrix * cross_h3)
projection_rank = projected_cross.rank()
check(
    "N0_SLOW_CROSS_RANK_PAIRING_AGREE",
    projection_rank == fredholm_rank,
    "projection=%d augmented=%d" % (projection_rank, fredholm_rank),
)

print("N0_SLOW_CROSS_FREDHOLM_RANK", fredholm_rank)
print("N0_SLOW_CROSS_SURVIVING_DIM_REAL", surviving_n0_dim)
print("N0_SLOW_CROSS_PROJECTED_MATRIX", projected_cross.tolist())

if fredholm_rank == 8:
    print("TERMINAL: J2-Y-SLOW-N0-CROSS-TERM-KILLS-JOINT-INVISIBLE-SEAM")
elif fredholm_rank > 0:
    print("PARTIAL: J2-Y-SLOW-N0-CROSS-TERM-PARTIAL-FREDHOLM-OBSTRUCTION")
else:
    print("PARTIAL: J2-Y-SLOW-N0-CROSS-TERM-IN-RANGE")
