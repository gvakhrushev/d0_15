#!/usr/bin/env python3
"""Exact finite controls for joint affine-holonomy quotient completeness.

Research-only certificate. Exact rational arithmetic.

The checker independently constructs a homogeneous curved L=2 Lorentz-link
background and the polynomial two-holonomy residual

    R_{2|1} = det(I-P1) t2 - (I-P2) adj(I-P1) t1.

It proves sector-by-sector that the full residual map on affine edge shifts has
kernel exactly equal to node-translation gauge, classifies the six spatial
Role-stabilizer orbits of ordered face pairs, isolates the unique missing mode
of the complementary orbit, and checks the Lorentz-vs-observer quadratic
orientation control.
"""

from itertools import combinations, product
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
MOMENTA = list(product((1, -1), repeat=4))

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

BOOST = sp.eye(4)
BOOST[0, 0] = sp.Rational(5, 3)
BOOST[0, 1] = sp.Rational(4, 3)
BOOST[1, 0] = sp.Rational(4, 3)
BOOST[1, 1] = sp.Rational(5, 3)

RBC = sp.eye(4)
RBC[1, 1] = 0
RBC[1, 2] = 1
RBC[2, 1] = -1
RBC[2, 2] = 0

RCD = sp.eye(4)
RCD[2, 2] = 0
RCD[2, 3] = 1
RCD[3, 2] = -1
RCD[3, 3] = 0

for name, g in (("BOOST", BOOST), ("RBC", RBC), ("RCD", RCD)):
    check(name + "_LORENTZ", sp.simplify(g.T * ETA * g - ETA) == sp.zeros(4))
    check(name + "_DET_ONE", sp.simplify(g.det()) == 1)

# Exact generic rational homogeneous control.  The particular words are only
# witnesses; they are not a physical selector.
LINK = [
    sp.simplify(BOOST * RBC),
    sp.simplify(BOOST * RCD),
    sp.simplify(RCD * RBC),
    sp.simplify(BOOST * RBC * RCD * BOOST.inv()),
]

for r, L in enumerate(LINK):
    check("BACKGROUND_LINK_LORENTZ_" + str(r),
          sp.simplify(L.T * ETA * L - ETA) == sp.zeros(4))
    check("BACKGROUND_LINK_DET_ONE_" + str(r), sp.simplify(L.det()) == 1)

def linear_plaquette(r, s):
    Lr, Ls = LINK[r], LINK[s]
    return sp.simplify(Lr * Ls * Lr.inv() * Ls.inv())

for r, s in PAIRS:
    P = linear_plaquette(r, s)
    check("GENERIC_PLAQUETTE_LORENTZ_" + str(r) + str(s),
          sp.simplify(P.T * ETA * P - ETA) == sp.zeros(4))
    check("GENERIC_PLAQUETTE_DET_I_MINUS_P_" + str(r) + str(s),
          sp.factor((I4 - P).det()) == sp.Rational(-64, 9))

def face_symbol(r, s, chi):
    """Translation part of a based affine plaquette on one momentum character.

    Edge amplitudes are u=(u_A,u_B,u_C,u_D), each u_r in R^4, so T is 4x16.
    """
    Lr, Ls = LINK[r], LINK[s]
    P = linear_plaquette(r, s)
    T = sp.zeros(4, 16)
    T[:, 4*r:4*r+4] = sp.simplify(I4 - chi[s] * P * Ls)
    T[:, 4*s:4*s+4] = sp.simplify(chi[r] * Lr - P)
    return P, T

def joint_block(P1, T1, P2, T2):
    M1 = I4 - P1
    M2 = I4 - P2
    d1 = sp.factor(M1.det())
    return sp.simplify(d1 * T2 - M2 * M1.adjugate() * T1)

def node_difference_symbol(chi):
    D = sp.zeros(16, 4)
    for r in range(4):
        D[4*r:4*r+4, :] = sp.simplify(I4 - chi[r] * LINK[r])
    return D

def orbit_category(p1, p2):
    t1 = "T" if 0 in p1 else "S"
    t2 = "T" if 0 in p2 else "S"
    if t1 == "T" and t2 == "T":
        return "T_TO_T"
    if t1 == "S" and t2 == "S":
        return "S_TO_S"
    if t1 == "T" and t2 == "S":
        i = p1[1]
        return "T_TO_S_INC" if i in p2 else "T_TO_S_COMP"
    i = p2[1]
    return "S_TO_T_INC" if i in p1 else "S_TO_T_COMP"

ORBIT_NAMES = (
    "T_TO_T", "S_TO_S",
    "T_TO_S_INC", "T_TO_S_COMP",
    "S_TO_T_INC", "S_TO_T_COMP",
)

counts = {name: 0 for name in ORBIT_NAMES}
for p1 in PAIRS:
    for p2 in PAIRS:
        if p1 != p2:
            counts[orbit_category(p1, p2)] += 1
check("ROLE_ORBIT_COUNTS", counts == {
    "T_TO_T": 6,
    "S_TO_S": 6,
    "T_TO_S_INC": 6,
    "T_TO_S_COMP": 3,
    "S_TO_T_INC": 6,
    "S_TO_T_COMP": 3,
})

def eta_gram(blocks):
    H = sp.zeros(16, 16)
    for B in blocks:
        H += B.T * ETA * B
    return sp.simplify(H)

sector_rows = []
for chi in MOMENTA:
    fdata = {p: face_symbol(*p, chi) for p in PAIRS}
    by_orbit = {name: [] for name in ORBIT_NAMES}
    all_blocks = []

    for p1 in PAIRS:
        P1, T1 = fdata[p1]
        for p2 in PAIRS:
            if p1 == p2:
                continue
            P2, T2 = fdata[p2]
            B = joint_block(P1, T1, P2, T2)
            all_blocks.append(B)
            by_orbit[orbit_category(p1, p2)].append(B)

    J = sp.Matrix.vstack(*all_blocks)
    D = node_difference_symbol(chi)
    tag = "".join("p" if q == 1 else "m" for q in chi)

    check("SECTOR_GAUGE_RANK_" + tag, D.to_DM().rank() == 4)
    check("SECTOR_RESIDUAL_RANK_" + tag, J.to_DM().rank() == 12)
    check("SECTOR_GAUGE_IN_KERNEL_" + tag,
          J * D == sp.zeros(J.rows, 4))

    orbit_ranks = {
        name: sp.Matrix.vstack(*blocks).to_DM().rank()
        for name, blocks in by_orbit.items()
    }
    eta_ranks = {
        name: eta_gram(blocks).to_DM().rank()
        for name, blocks in by_orbit.items()
    }
    check("FULL_ETA_QUADRATIC_RANK_" + tag,
          eta_gram(all_blocks).to_DM().rank() == 12)
    check("INCIDENT_ETA_RANK_TS_" + tag,
          eta_ranks["T_TO_S_INC"] == 12)
    check("INCIDENT_ETA_RANK_ST_" + tag,
          eta_ranks["S_TO_T_INC"] == 12)

    sector_rows.append((chi, orbit_ranks, eta_ranks))

check("GLOBAL_NODE_GAUGE_RANK_64", sum(4 for _ in MOMENTA) == 64)
check("GLOBAL_JOINT_RESIDUAL_RANK_192", sum(12 for _ in MOMENTA) == 192)
check("GLOBAL_QUOTIENT_DIMENSION_192", 256 - 64 == 192)

check("TS_INCIDENT_COMPLETE_ALL_SECTORS",
      all(row[1]["T_TO_S_INC"] == 12 for row in sector_rows))
check("ST_INCIDENT_COMPLETE_ALL_SECTORS",
      all(row[1]["S_TO_T_INC"] == 12 for row in sector_rows))

KSTAR = (-1, -1, 1, 1)
for name in ("T_TO_S_COMP", "S_TO_T_COMP"):
    deficient = [
        chi for chi, ranks, _ in sector_rows
        if ranks[name] != 12
    ]
    check(name + "_UNIQUE_DEFICIENT_SECTOR", deficient == [KSTAR])
    krow = next(ranks for chi, ranks, _ in sector_rows if chi == KSTAR)
    check(name + "_DEFICIENT_RANK_11", krow[name] == 11)

def kappa_eta_sq(chi):
    kap = [1-q for q in chi]
    return kap[0]**2 - kap[1]**2 - kap[2]**2 - kap[3]**2

null_chars = [
    chi for chi in MOMENTA
    if chi != (1, 1, 1, 1) and kappa_eta_sq(chi) == 0
]
check("THREE_LORENTZ_NULL_CHECKERBOARDS", set(null_chars) == {
    (-1, -1, 1, 1),
    (-1, 1, -1, 1),
    (-1, 1, 1, -1),
})
check("COMPLEMENT_DEFECT_IS_LORENTZ_NULL", kappa_eta_sq(KSTAR) == 0)

fdata = {p: face_symbol(*p, KSTAR) for p in PAIRS}
comp_blocks = []
inc_blocks = []
for p1 in PAIRS:
    P1, T1 = fdata[p1]
    for p2 in PAIRS:
        if p1 == p2:
            continue
        P2, T2 = fdata[p2]
        B = joint_block(P1, T1, P2, T2)
        cat = orbit_category(p1, p2)
        if cat == "T_TO_S_COMP":
            comp_blocks.append(B)
        if cat == "T_TO_S_INC":
            inc_blocks.append(B)

Jcomp = sp.Matrix.vstack(*comp_blocks)
Jinc = sp.Matrix.vstack(*inc_blocks)
Dstar = node_difference_symbol(KSTAR)

w = sp.Matrix([
    0, 0, 0, 0,
    sp.Rational(4,3), sp.Rational(5,3), sp.Rational(3,8), sp.Rational(5,8),
    sp.Rational(-1,2), 0, sp.Rational(-5,8), sp.Rational(-3,8),
    0, sp.Rational(3,8), 0, sp.Rational(3,8),
])

check("COMPLEMENT_EXTRA_VECTOR_NULL",
      Jcomp * w == sp.zeros(Jcomp.rows, 1))
check("COMPLEMENT_EXTRA_VECTOR_NONGAUGE",
      Dstar.row_join(w).to_DM().rank() == 5)
check("INCIDENT_ORBIT_DETECTS_COMPLEMENT_EXTRA_VECTOR",
      Jinc * w != sp.zeros(Jinc.rows, 1))

# Hostile generic control: the checkerboard/complement defect above is not a
# universal identity. A second exact rational Lorentz-link word set makes all
# four cross-type spatial-Role orbits quotient-complete in every sector.
ALT_LINK = [
    sp.simplify(BOOST * RBC),
    sp.simplify(BOOST * RCD),
    sp.simplify(RCD * RBC),
    sp.simplify(BOOST * RCD * RBC.inv()),
]

def alt_plaquette(r, s):
    Lr, Ls = ALT_LINK[r], ALT_LINK[s]
    return sp.simplify(Lr * Ls * Lr.inv() * Ls.inv())

def alt_face_symbol(r, s, chi):
    Lr, Ls = ALT_LINK[r], ALT_LINK[s]
    P = alt_plaquette(r, s)
    T = sp.zeros(4, 16)
    T[:, 4*r:4*r+4] = sp.simplify(I4 - chi[s] * P * Ls)
    T[:, 4*s:4*s+4] = sp.simplify(chi[r] * Lr - P)
    return P, T

for r, s in PAIRS:
    check("ALT_GENERIC_PLAQUETTE_" + str(r) + str(s),
          sp.factor((I4 - alt_plaquette(r, s)).det())
          == sp.Rational(-64, 9))

alt_inc_sym_ranks = []
alt_comp_sym_ranks = []
alt_independence = []

for chi in MOMENTA:
    fdata = {p: alt_face_symbol(*p, chi) for p in PAIRS}
    by = {name: [] for name in ORBIT_NAMES}

    for p1 in PAIRS:
        P1, T1 = fdata[p1]
        for p2 in PAIRS:
            if p1 == p2:
                continue
            P2, T2 = fdata[p2]
            by[orbit_category(p1, p2)].append(
                joint_block(P1, T1, P2, T2)
            )

    tag = "".join("p" if q == 1 else "m" for q in chi)
    for name in (
        "T_TO_S_INC", "S_TO_T_INC",
        "T_TO_S_COMP", "S_TO_T_COMP",
    ):
        check("ALT_CROSS_ORBIT_COMPLETE_" + name + "_" + tag,
              sp.Matrix.vstack(*by[name]).to_DM().rank() == 12)

    H_inc = (
        eta_gram(by["T_TO_S_INC"])
        + eta_gram(by["S_TO_T_INC"])
    )
    H_comp = (
        eta_gram(by["T_TO_S_COMP"])
        + eta_gram(by["S_TO_T_COMP"])
    )
    alt_inc_sym_ranks.append(H_inc.to_DM().rank())
    alt_comp_sym_ranks.append(H_comp.to_DM().rank())

    pair = sp.Matrix.hstack(
        sp.Matrix(H_inc).reshape(256, 1),
        sp.Matrix(H_comp).reshape(256, 1),
    )
    alt_independence.append(pair.to_DM().rank())

check("ALT_PAIR_EXCHANGE_INCIDENT_COMPLETE",
      set(alt_inc_sym_ranks) == {12})
check("ALT_PAIR_EXCHANGE_COMPLEMENT_COMPLETE",
      set(alt_comp_sym_ranks) == {12})
check("ALT_TWO_SYMMETRIC_CROSS_ACTIONS_INDEPENDENT",
      set(alt_independence) == {2})

# Orientation/reversal scalar-channel control.
P1 = sp.simplify(BOOST * RCD)
P2 = sp.simplify(RBC * BOOST * RBC.inv())
t1 = sp.Matrix([1, 2, 0, -1])
t2 = sp.Matrix([0, -1, 3, 2])

def joint_residual(P1, t1, P2, t2):
    M1 = I4 - P1
    M2 = I4 - P2
    return sp.simplify(M1.det() * t2 - M2 * M1.adjugate() * t1)

R = joint_residual(P1, t1, P2, t2)
Rrev = sp.simplify(-P2.inv() * R)
check("TARGET_REVERSAL_LORENTZ_SCALAR_INVARIANT",
      sp.simplify((R.T * ETA * R)[0]
                  - (Rrev.T * ETA * Rrev)[0]) == 0)
check("TARGET_REVERSAL_REST_OBSERVER_SCALAR_CHANGES",
      sp.simplify((Rrev.T * Rrev)[0]
                  - (R.T * R)[0]) == sp.Rational(4096, 9))

flat_t1 = sp.Matrix([1, 2, 3, 4])
flat_t2 = sp.Matrix([-1, 0, 2, 5])
check("FLAT_JOINT_RESIDUAL_ZERO",
      joint_residual(I4, flat_t1, I4, flat_t2) == sp.zeros(4, 1))

print("RESULT_FULL_MAP: sector-by-sector rank 12 with rank-4 node gauge; global rank 192 and kernel exactly node gauge on the generic homogeneous curved L=2 control.")
print("RESULT_ROLE_ORBITS: incident cross-type orbits are complete on the primary control; its complementary defect is a special background resonance, not universal.")
print("RESULT_SPECIAL_RESONANCE: one symmetric control has a complementary-orbit defect at (-1,-1,+1,+1), but an independent generic link control removes it; the checkerboard coincidence is background-dependent, not a selector theorem.")\nprint("RESULT_SELECTOR: even after pair-exchange symmetry, incident and complementary cross-type Lorentz quadratics are independent and each quotient-complete on the hostile generic control, so symmetry+completeness leave a genuine action modulus.")
print("RESULT_SCALAR: equal-weight Lorentz quadratics are quotient-complete; target reversal preserves eta but not the rest-observer positive scalar.")
print("RESULT_FLAT: polynomial joint-residual terms vanish at flat holonomy and do not alter the accepted flat Hessian.")
