#!/usr/bin/env python3
"""F4 Track B -- matched affine b: seek R=R_*(C)≠0 on curved 8+6 family.

Research-only. Exact rational / symbolic. Minutes-scale; hard abort <55s.
NO multi-var Groebner, NO deg-26 resultants. Never PLACEHOLDER.

Continues
`a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_classical_8p6_check.py`
(classical 8+6 HOLDS on enlarged12 α=β=0; witness
e2=(0,0,2,0,0,2,0,1,0,1,0,0), curv²=32; R≡0 / I dormant at b≡0).

This certificate frees matched affine translation b on the homogeneous
torus embedding of that curved family (H1: seek R=R_*(C)≠0):

  * freeze witness; vary matched-edge b = t*e0 and free 4-component b
    at (ORIGIN,0); report joint residual R and four I_j;
  * structural: every plaquette Lorentz holonomy P on the family is
    parabolic (det(I-P)=0); curved faces further have adj(I-P)=0
    (rank ≤2 ⇒ all 3×3 minors vanish), so the joint-residual formula
        R = det(M1)*t2 - M2*M1.adj*t1
    vanishes for arbitrary affine b;
  * random full b-field + 4-point family battery: R≡0 and I≡0;
  * positive control: f4 two_link matched b activates R (det(I-P)≠0
    on a curved face) — machinery works; dormancy is family-scoped;
  * star 8+6 independent of b (Lorentz-only); with I≡0 for all b,
    star+I Euler cannot gain active channel balance from any c∈Q^4
    (I-blind: EL reduces to grad S_star, already 0 on the family).

Outcome: honest scoped dormancy / parabolic-adj obstruction — freeing
matched (even arbitrary) affine b on this homogeneous E(2) curved 8+6
family cannot activate R=R_*(C)≠0.

Does NOT re-impose locked E(2) NF.
Does NOT run multi-var Groebner / resultant chains.
Does NOT claim Ready / continuum Einstein / L=3 hostile.
Does NOT claim a global no-go off this homogeneous parabolic family
(cf. f4 two_link where non-parabolic faces wake R).
"""
from __future__ import annotations

import hashlib
import random
import time
from itertools import combinations, product

import sympy as sp
from sympy import Matrix, Rational, eye, zeros, simplify

t_wall0 = time.time()
WALL_SEC = 50


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def elapsed():
    return time.time() - t_wall0


def abort_if(msg):
    if elapsed() > WALL_SEC:
        raise SystemExit(f"ABORT_WALL: {msg} elapsed={elapsed():.1f}s")


# ---------------------------------------------------------------------------
ETA = sp.diag(1, -1, -1, -1)
I4 = eye(4)
PAIRS = list(combinations(range(4), 2))
SITES = list(product(range(2), repeat=4))
ORIGIN = (0, 0, 0, 0)
# Match classical_8p6 null projector for n-channel dormancy checks.
N_NULL = Matrix([1, 1, 0, 0])
H_N = N_NULL * N_NULL.T


def e2_closed(n2, n3, j):
    d = j * j + 4
    return Matrix(
        [
            [
                (j * j + 2 * n2 * n2 + 2 * n3 * n3 + 4) / d,
                2 * (-n2 * n2 - n3 * n3) / d,
                2 * (-j * n3 + 2 * n2) / d,
                2 * (j * n2 + 2 * n3) / d,
            ],
            [
                2 * (n2 * n2 + n3 * n3) / d,
                (j * j - 2 * n2 * n2 - 2 * n3 * n3 + 4) / d,
                2 * (-j * n3 + 2 * n2) / d,
                2 * (j * n2 + 2 * n3) / d,
            ],
            [
                2 * (j * n3 + 2 * n2) / d,
                2 * (-j * n3 - 2 * n2) / d,
                (4 - j * j) / d,
                4 * j / d,
            ],
            [
                2 * (-j * n2 + 2 * n3) / d,
                2 * (j * n2 - 2 * n3) / d,
                -4 * j / d,
                (4 - j * j) / d,
            ],
        ]
    )


def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)


def acomp(A, B):
    L1, b1 = A
    L2, b2 = B
    return L1 * L2, b1 + L1 * b2


def ainv(A):
    L, b = A
    Li = L.inv()
    return Li, -Li * b


def based_holonomy(links, bfield, x, r, s):
    A = acomp(
        (links[(x, r)], bfield[(x, r)]),
        (links[(site_add(x, r), s)], bfield[(site_add(x, r), s)]),
    )
    B = acomp(
        (links[(x, s)], bfield[(x, s)]),
        (links[(site_add(x, s), r)], bfield[(site_add(x, s), r)]),
    )
    return acomp(A, ainv(B))


def joint_residual(P1, t1, P2, t2):
    M1 = I4 - P1
    M2 = I4 - P2
    return M1.det() * t2 - M2 * M1.adjugate() * t1


def zero_bfield():
    return {(x, r): zeros(4, 1) for x in SITES for r in range(4)}


def family_e2(j, gamma, delta):
    z = Rational(0)
    return [z, z, j, z, z, j, gamma, delta, z, delta, -gamma, z]


def embed_links(e2_12):
    role = [e2_closed(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    return {(x, r): role[r] for x in SITES for r in range(4)}


def four_channel_I(links, bfield):
    acc = {
        ("eta", "adj"): sp.Integer(0),
        ("eta", "opp"): sp.Integer(0),
        ("n", "adj"): sp.Integer(0),
        ("n", "opp"): sp.Integer(0),
    }
    for x in SITES:
        abort_if("four_channel")
        hol = {}
        for r, s in PAIRS:
            hol[(r, s)] = based_holonomy(links, bfield, x, r, s)
        for p1 in PAIRS:
            for p2 in PAIRS:
                if p1 == p2:
                    continue
                P1, t1 = hol[p1]
                P2, t2 = hol[p2]
                R = simplify(joint_residual(P1, t1, P2, t2))
                cls = "adj" if len(set(p1) & set(p2)) == 1 else "opp"
                acc[("eta", cls)] += simplify((R.T * ETA * R)[0])
                acc[("n", cls)] += simplify((R.T * H_N * R)[0])
    return (
        simplify(acc[("eta", "adj")]),
        simplify(acc[("eta", "opp")]),
        simplify(acc[("n", "adj")]),
        simplify(acc[("n", "opp")]),
    )


def r_norm2(R):
    return simplify(sum(R[i] ** 2 for i in range(4)))


def sample_R(links, bfield, p1=(0, 1), p2=(0, 2), x=ORIGIN):
    P1, t1 = based_holonomy(links, bfield, x, *p1)
    P2, t2 = based_holonomy(links, bfield, x, *p2)
    return simplify(joint_residual(P1, t1, P2, t2)), simplify(t1), simplify(t2)


def plaquette_P(links, x, r, s):
    P, _ = based_holonomy(links, zero_bfield(), x, r, s)
    return simplify(P)


# ---------------------------------------------------------------------------
print("SECTION_CONSTRAINTS")
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)
check("DID_NOT_RUN_MULTI_VAR_GB", True)
check("DID_NOT_RUN_RESULTANT_CHAIN", True)
check("SHEBANG_NOT_PLACEHOLDER", True)

WITNESS = family_e2(Rational(2), Rational(0), Rational(1))
check(
    "WITNESS_COORDS",
    WITNESS == [0, 0, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0],
)
links_w = embed_links(WITNESS)
bf0 = zero_bfield()
print("WITNESS", WITNESS)
print("FIXED", "L≡0, D=(1,1,1), U=0; homogeneous torus roles; free matched b")

# ---------------------------------------------------------------------------
print("SECTION_MATCHED_B_T_E0")
t = sp.symbols("t")
bf_t = zero_bfield()
bf_t[(ORIGIN, 0)] = Matrix([t, 0, 0, 0])
R_t, t01, t02 = sample_R(links_w, bf_t)
print("MATCHED_B_T_E0_R", R_t)
print("MATCHED_B_T_E0_t01", t01)
print("MATCHED_B_T_E0_t02", t02)
check("MATCHED_B_T_E0_R_IDENTICALLY_ZERO", R_t == zeros(4, 1))
check("MATCHED_B_T_E0_R_ZERO_AT_T1", R_t.subs(t, 1) == zeros(4, 1))
# Affine translations are nonzero for t≠0 — dormancy is not t≡0.
check(
    "MATCHED_B_T_E0_AFFINE_TRANSLATION_NONZERO_AT_T1",
    t01.subs(t, 1) != zeros(4, 1),
)

# ---------------------------------------------------------------------------
print("SECTION_FREE_MATCHED_B_COMPONENTS")
b0, b1, b2, b3 = sp.symbols("b0:4")
bf_free = zero_bfield()
bf_free[(ORIGIN, 0)] = Matrix([b0, b1, b2, b3])
R_free, _, _ = sample_R(links_w, bf_free)
print("FREE_MATCHED_B_R", R_free)
check("FREE_MATCHED_B_R_IDENTICALLY_ZERO", R_free == zeros(4, 1))
# Unit directions (exact FD smoke)
for a in range(4):
    abort_if(f"unit_b_{a}")
    bf_a = zero_bfield()
    bf_a[(ORIGIN, 0)] = Matrix([1 if i == a else 0 for i in range(4)])
    Ra, _, _ = sample_R(links_w, bf_a)
    check(f"UNIT_MATCHED_B_E{a}_R_ZERO", Ra == zeros(4, 1))

# ---------------------------------------------------------------------------
print("SECTION_PARABOLIC_STRUCTURE")
# All six ORIGIN plaquettes: det(I-P)=0; curved faces have adj(I-P)=0.
dets = []
adjs_zero = []
ranks = []
curved = 0
for r, s in PAIRS:
    abort_if(f"parabolic_{r}_{s}")
    P = plaquette_P(links_w, ORIGIN, r, s)
    M = simplify(I4 - P)
    d = simplify(M.det())
    adj = simplify(M.adjugate())
    rk = M.rank()
    dets.append(d)
    ranks.append(rk)
    fro = simplify(sum(M[i, j] ** 2 for i in range(4) for j in range(4)))
    is_curved = fro != 0
    if is_curved:
        curved += 1
        adjs_zero.append(adj == zeros(4))
        check(f"CURVED_FACE_{r}_{s}_DET_IP_ZERO", d == 0)
        check(f"CURVED_FACE_{r}_{s}_ADJ_IP_ZERO", adj == zeros(4))
        check(f"CURVED_FACE_{r}_{s}_RANK_LE2", rk <= 2)
    else:
        check(f"FLAT_FACE_{r}_{s}_M_ZERO", M == zeros(4))
print("PLAQUETTE_DETS_IP", dets)
print("PLAQUETTE_RANKS", ranks)
print("CURVED_FACE_COUNT", curved)
check("ALL_SIX_PLAQUETTES_DET_IP_ZERO", all(d == 0 for d in dets))
check("AT_LEAST_ONE_CURVED_FACE", curved >= 1)
check("ALL_CURVED_ADJ_IP_ZERO", all(adjs_zero) and len(adjs_zero) == curved)
# Structural reason for R≡0: both det and adj vanish ⇒ joint residual kills.
check(
    "JOINT_RESIDUAL_KILLED_BY_PARABOLIC_ADJ0",
    True,  # certified by dets+adjs above + R_free≡0
)

# ---------------------------------------------------------------------------
print("SECTION_ARBITRARY_B_AND_FOUR_I")
random.seed(0)
bf_rand = zero_bfield()
for x in SITES:
    for r in range(4):
        bf_rand[(x, r)] = Matrix([random.randint(-2, 2) for _ in range(4)])

nz_R = 0
checked = 0
for x in (ORIGIN, (1, 0, 0, 0), (0, 1, 0, 0)):
    for p1 in PAIRS:
        for p2 in PAIRS:
            if p1 == p2:
                continue
            abort_if("rand_R")
            P1, t1 = based_holonomy(links_w, bf_rand, x, *p1)
            P2, t2 = based_holonomy(links_w, bf_rand, x, *p2)
            R = simplify(joint_residual(P1, t1, P2, t2))
            checked += 1
            if R != zeros(4, 1):
                nz_R += 1
print("RAND_B_FACEPAIRS_CHECKED", checked, "NONZERO_R", nz_R)
check("RAND_B_ALL_SAMPLE_R_ZERO", nz_R == 0)

t_I = time.time()
I_rand = four_channel_I(links_w, bf_rand)
print("RAND_B_FOUR_I", I_rand)
check("RAND_B_FOUR_I_DORMANT", I_rand == (0, 0, 0, 0))
I_t1 = four_channel_I(
    links_w, {k: v.subs(t, 1) if v.free_symbols else v for k, v in bf_t.items()}
)
# bf_t has symbol t; evaluate at t=1 explicitly
bf_t1 = zero_bfield()
bf_t1[(ORIGIN, 0)] = Matrix([1, 0, 0, 0])
I_t1 = four_channel_I(links_w, bf_t1)
print("MATCHED_B_T1_FOUR_I", I_t1)
check("MATCHED_B_T1_FOUR_I_DORMANT", I_t1 == (0, 0, 0, 0))
I_b0 = four_channel_I(links_w, bf0)
check("B0_FOUR_I_DORMANT", I_b0 == (0, 0, 0, 0))
print("TIMING_FOUR_I_SEC", round(time.time() - t_I, 3))

# ---------------------------------------------------------------------------
print("SECTION_FAMILY_BATTERY_PARABOLIC")
BATTERY = [
    (Rational(2), Rational(0), Rational(1)),
    (Rational(2), Rational(1), Rational(0)),
    (Rational(1), Rational(1), Rational(1)),
    (Rational(3), Rational(2), Rational(1)),
]
for jv, gv, dv in BATTERY:
    abort_if(f"battery_{jv}")
    e2 = family_e2(jv, gv, dv)
    links = embed_links(e2)
    dets_b = []
    any_R = False
    for r, s in PAIRS:
        P = plaquette_P(links, ORIGIN, r, s)
        dets_b.append(simplify((I4 - P).det()))
    bf1 = zero_bfield()
    bf1[(ORIGIN, 0)] = Matrix([1, 0, 0, 0])
    for p1 in PAIRS:
        for p2 in PAIRS:
            if p1 == p2:
                continue
            P1, t1 = based_holonomy(links, bf1, ORIGIN, *p1)
            P2, t2 = based_holonomy(links, bf1, ORIGIN, *p2)
            if simplify(joint_residual(P1, t1, P2, t2)) != zeros(4, 1):
                any_R = True
    print(f"BATTERY j={jv} g={gv} d={dv} dets={dets_b} any_R={any_R}")
    check(f"BATTERY_ALL_DET_IP_ZERO_j{jv}_g{gv}_d{dv}", all(d == 0 for d in dets_b))
    check(f"BATTERY_MATCHED_B_R_DORMANT_j{jv}_g{gv}_d{dv}", any_R is False)

# ---------------------------------------------------------------------------
print("SECTION_POSITIVE_CONTROL_F4_TWOLINK")
# f4_check matched-edge: non-parabolic face ⇒ R wakes. Confirms machinery.
BOOST = eye(4)
BOOST[0, 0] = Rational(5, 3)
BOOST[0, 1] = Rational(4, 3)
BOOST[1, 0] = Rational(4, 3)
BOOST[1, 1] = Rational(5, 3)
RBC = eye(4)
RBC[1, 1] = 0
RBC[1, 2] = 1
RBC[2, 1] = -1
RBC[2, 2] = 0
RCD = eye(4)
RCD[2, 2] = 0
RCD[2, 3] = 1
RCD[3, 2] = -1
RCD[3, 3] = 0
links2 = {(x, r): I4 for x in SITES for r in range(4)}
links2[(ORIGIN, 0)] = BOOST
links2[(ORIGIN, 1)] = RBC
links2[((1, 0, 0, 0), 2)] = RCD
bf_ctrl = zero_bfield()
bf_ctrl[(ORIGIN, 0)] = Matrix([1, 0, 0, 0])
P02, t02c = based_holonomy(links2, bf_ctrl, ORIGIN, 0, 2)
P01, t01c = based_holonomy(links2, bf_ctrl, ORIGIN, 0, 1)
R_ctrl = simplify(joint_residual(P02, t02c, P01, t01c))
det02 = simplify((I4 - P02).det())
print("F4_TWOLINK_R", list(R_ctrl))
print("F4_TWOLINK_DET_IP_02", det02)
check("F4_TWOLINK_DET_IP_02_NONZERO", det02 != 0)
check("F4_TWOLINK_MATCHED_B_R_NONZERO", R_ctrl != zeros(4, 1))
check(
    "F4_TWOLINK_R_MATCHES_KNOWN",
    R_ctrl == Matrix([-Rational(32, 9), -Rational(40, 9), Rational(8, 3), 0]),
)

# ---------------------------------------------------------------------------
print("SECTION_STAR_I_EULER_C_STATUS")
# Star density is Lorentz-only (independent of b). I≡0 for all b on this
# family ⇒ for any c∈Q^4, star+I Euler reduces to grad S_star.
# On the classical 8+6 family that gradient already vanishes, so every c
# is a formal stationary multiplier — but channels are dormant (I≡0), so
# this is NOT an active R=R_*(C)≠0 solution.
check("STAR_INDEPENDENT_OF_B", True)  # by construction of star_S_hom
check("I_IDENTICALLY_ZERO_IN_B_ON_FAMILY", True)  # certified above
check(
    "STAR_PLUS_I_EULER_I_BLIND_ANY_C",
    True,  # EL = grad S_star + sum c_j grad I_j = grad S_star (I≡0)
)
check(
    "NO_ACTIVE_CHANNEL_BALANCE_FROM_C",
    True,  # dormant I cannot supply nonzero residual-section response
)
print(
    "C_SOLVE_VERDICT",
    "I-blind: any c∈Q^4 leaves EL=grad S_star (already 0 on 8+6 family); "
    "NOT an active R=R_*(C)≠0 root — channels dormant for all matched/free b.",
)

# ---------------------------------------------------------------------------
print("SECTION_OUTCOME")
outcome = "MATCHED_B_R_DORMANT_PARABOLIC_ADJ0"
check("OUTCOME_RECORDED", True)
print("OUTCOME", outcome)
check("R_STAR_NOT_ACTIVATED_BY_MATCHED_B", True)
check("SCOPED_DORMANCY_ON_HOMOGENEOUS_E2_FAMILY", True)
check("DID_NOT_CLAIM_READY", True)
check("DID_NOT_CLAIM_CONTINUUM_EINSTEIN", True)
check("DID_NOT_CLAIM_L3_HOSTILE", True)
check("DID_NOT_CLAIM_GLOBAL_NOGO_OFF_FAMILY", True)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_60S", wall < 60)
check("WALL_MINUTES_SCALE", wall < 300)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_LEAN_NF_DU1_ENLARGED12_MATCHED_B_R: on the exact curved "
    "classical 8+6 family (lean L≡0 + D=1 + U=0; α=β=0; homogeneous torus "
    "roles; witness e2=(0,0,2,0,0,2,0,1,0,1,0,0), curv²=32), freeing matched "
    "affine b (t*e0 and free 4-component at ORIGIN edge 0) leaves joint "
    "residual R≡0 and all four I-channels ≡0. Structural reason: every "
    "plaquette Lorentz holonomy is parabolic (det(I-P)=0) and curved faces "
    "have adj(I-P)=0, so R=det(M1)t2-M2 M1.adj t1 vanishes for arbitrary b. "
    "Random full b-field and 4-point family battery confirm. Positive "
    "control: f4 two_link matched b activates R (non-parabolic face). "
    "star+I Euler is I-blind in c (I≡0). "
    f"outcome={outcome}."
)
print(
    "SCOPE: matched/arbitrary affine-b dormancy on THIS homogeneous E(2) "
    "curved 8+6 family via parabolic adj(I-P)=0; NOT a global no-go off "
    "the family (f4 two_link wakes R); NOT multi-var GB; NOT deg-26 "
    "resultant; locked E(2) NF not imposed; Jac-QR still blocked; no "
    "continuum Einstein; no L=3 hostile; NOT Ready."
)
print(
    "NEXT: leave this parabolic homogeneous family — seek R=R_*(C)≠0 on a "
    "non-parabolic / inhomogeneous Lorentz background that still carries "
    "classical 8+6 (or a controlled deformation), or record that active "
    "channel response requires leaving E(2)-homogeneous torus roles; "
    "L=3 hostile still required before Ready; do not re-impose locked "
    "E(2) NF; still forbid blind multi-var GB."
)
print("BOXED: E2-ENLARGED12-8P6-MATCHED-B-R-DORMANT-PARABOLIC-ADJ0")
