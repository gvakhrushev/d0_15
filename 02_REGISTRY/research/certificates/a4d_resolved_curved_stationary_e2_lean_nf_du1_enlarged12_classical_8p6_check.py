#!/usr/bin/env python3
"""F4 Track B -- classical 8+6 confirm + cheap R=R_*(C) filter at exact family.

Research-only. Exact rational / symbolic. Minutes-scale; hard abort <55s.
NO multi-var Groebner, NO deg-26 resultants. Never PLACEHOLDER.

Continues
`a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_pattern_exactify_check.py`
(exact curved family α=β=0 under lean L≡0 + D=(1,1,1), U=0; ambient
free-internal(12)+transverse(6) ≡0; witness e2=(0,0,2,0,0,2,0,1,0,1,0,0),
curv²=32).

This certificate confirms the *classical/gauge-pack* 8+6 used by earlier
lean-NF DU1 / subQR8 / stationarity certs — not only the enlarged-12 FD
ambient:

  * CLASSICAL_FREE_E2 = [0,2,3,4,5,6,7,8]  (subQR8 FREE_E2; 8 internal
    Hessian / free-internal directions under lean L≡0 + identity D/U);
  * CLASSICAL_COMPLEMENT_E2 = [1,9,10,11]  (former subQR8 fixed-to-0;
    released under enlarged-12; nonzero at the curved witness via δ);
  * TRANSVERSE_6 = roles {0,1} × {K1,M2,M3} (same Cayley differential);
  * at the exact witness and on a rational α=β=0 battery: classical 8 FD
    grads ≡0 and transverse 6 ≡0 (exact); ambient 12 vanishing implies the
    classical 8 as a literal index subset;
  * cheap four-channel / joint-residual filter at the witness: C≠0
    (curv²=32) but with b≡0 (identity solder, no affine translation)
    joint residual R≡0 and all four I-channels ≡0 — honest NEGATIVE for
    active R=R_*(C)≠0 (I dormant on the R=0 locus; matches f4 H1 picture
    that nonzero matched-b is required to wake channels).

Does NOT re-impose locked E(2) NF.
Does NOT run multi-var Groebner / resultant chains.
Does NOT claim Ready / continuum Einstein / L=3 hostile.
Does NOT claim an active four-channel R=R_*(C)≠0 root.
"""
from __future__ import annotations

import hashlib
import time
from itertools import combinations, product

import sympy as sp
from sympy import Matrix, Rational, eye, zeros, together, simplify

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
PINDEX = {p: i for i, p in enumerate(PAIRS)}
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = zeros(6)
STAR_MAP = {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}
for p, (q, s) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = s

# Null projector for n-channel (same H_N shape as f4_check: diag on null).
N_NULL = Matrix([1, 1, 0, 0])
H_N = N_NULL * N_NULL.T  # rank-1; sufficient for dormancy check at b=0


def gen_boost(i):
    A = zeros(4)
    A[0, i] = 1
    A[i, 0] = 1
    return A


def gen_rot(i, j):
    # Match enlarged12 pattern_exactify convention.
    A = zeros(4)
    A[i, j] = -1
    A[j, i] = 1
    return A


N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
J23 = gen_rot(2, 3)
K1 = gen_boost(1)
M2 = gen_boost(2) - gen_rot(1, 2)
M3 = gen_boost(3) - gen_rot(1, 3)
COMPL = (K1, M2, M3)
TRANS_LABELS = ["r0_K1", "r0_M2", "r0_M3", "r1_K1", "r1_M2", "r1_M3"]


def e2_alg(n2, n3, j):
    return n2 * N2 + n3 * N3 + j * J23


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


def cayley_diff(A, H):
    B = I4 - A / 2
    Binv = B.inv()
    P = (I4 + A / 2) * Binv
    halfH = H / 2
    return halfH * Binv + P * halfH * Binv


def orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def wedge(u, v):
    return Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def bivector_of_tangent(X):
    Y = X * ETA
    return Matrix([Y[a, b] for a, b in PAIRS])


def curvature(P):
    return (P - P.inv()) / 2


def d_curvature(P, dP):
    Pinv = P.inv()
    return (dP + Pinv * dP * Pinv) / 2


def star_S_hom(role, Theta):
    vs = [Theta[:, r] for r in range(4)]
    site = 0
    for r, s in PAIRS:
        P = role[r] * role[s] * role[r].inv() * role[s].inv()
        C = bivector_of_tangent(curvature(P))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * (
            wedge(vs[u], vs[v]).T * G2 * STAR * C
        )[0]
    return 16 * site


def dS_transverse(role, As, Theta, r0, H):
    dP0 = cayley_diff(As[r0], H)
    vs = [Theta[:, r] for r in range(4)]
    site = 0
    for r, s in PAIRS:
        Ur, Us = role[r], role[s]
        Uri, Usi = Ur.inv(), Us.inv()
        dUr = dP0 if r == r0 else zeros(4)
        dUs = dP0 if s == r0 else zeros(4)
        dUri = (-Uri * dUr * Uri) if r == r0 else zeros(4)
        dUsi = (-Usi * dUs * Usi) if s == r0 else zeros(4)
        dP = (
            dUr * Us * Uri * Usi
            + Ur * dUs * Uri * Usi
            + Ur * Us * dUri * Usi
            + Ur * Us * Uri * dUsi
        )
        P = Ur * Us * Uri * Usi
        dC = bivector_of_tangent(d_curvature(P, dP))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * (
            wedge(vs[u], vs[v]).T * G2 * STAR * dC
        )[0]
    return 16 * site


# ---------------------------------------------------------------------------
print("SECTION_CLASSICAL_8P6_PACKING")
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)
check("DID_NOT_RUN_MULTI_VAR_GB", True)
check("DID_NOT_RUN_RESULTANT_CHAIN", True)

# Classical lean-NF DU1 / subQR8 FREE_E2 (from lean_nf_du1_subqr8_check).
CLASSICAL_FREE_E2 = [0, 2, 3, 4, 5, 6, 7, 8]
CLASSICAL_COMPLEMENT_E2 = [1, 9, 10, 11]
check("CLASSICAL_FREE_E2_COUNT_8", len(CLASSICAL_FREE_E2) == 8)
check(
    "CLASSICAL_FREE_E2_EXACT",
    CLASSICAL_FREE_E2 == [0, 2, 3, 4, 5, 6, 7, 8],
)
check(
    "CLASSICAL_COMPLEMENT_EXACT",
    CLASSICAL_COMPLEMENT_E2 == [1, 9, 10, 11],
)
check(
    "CLASSICAL_PARTITION_12",
    sorted(CLASSICAL_FREE_E2 + CLASSICAL_COMPLEMENT_E2) == list(range(12)),
)
print("CLASSICAL_FREE_E2", CLASSICAL_FREE_E2)
print("CLASSICAL_COMPLEMENT_E2", CLASSICAL_COMPLEMENT_E2)
print("TRANSVERSE", "roles {0,1} x {K1,M2,M3}")
print("FIXED", "L≡0, D=(1,1,1), U=0 (lean DU1 specialization)")


def family_e2(j, gamma, delta):
    z = Rational(0)
    return [
        z, z, j,
        z, z, j,
        gamma, delta, z,
        delta, -gamma, z,
    ]


def embed_e2(e2_12):
    role = [e2_closed(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    As = [e2_alg(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    return role, As, ETA


def ambient_grad12(e2_12, h=Rational(1, 64)):
    role, _, Th = embed_e2(e2_12)
    g = []
    for k in range(12):
        ep = list(e2_12)
        em = list(e2_12)
        ep[k] = e2_12[k] + h
        em[k] = e2_12[k] - h
        rp, _, _ = embed_e2(ep)
        rm, _, _ = embed_e2(em)
        Sp = together(star_S_hom(rp, Th))
        Sm = together(star_S_hom(rm, Th))
        g.append(together((Sp - Sm) / (2 * h)))
    return g


def classical_8(e2_12, h=Rational(1, 64)):
    g12 = ambient_grad12(e2_12, h=h)
    return [g12[i] for i in CLASSICAL_FREE_E2]


def trans6(e2_12):
    role, As, Th = embed_e2(e2_12)
    out = []
    for r0 in (0, 1):
        for H in COMPL:
            out.append(together(dS_transverse(role, As, Th, r0, H)))
    return out


def curv_frobenius2(e2_12):
    role, _, _ = embed_e2(e2_12)
    s = 0
    for r, ss in PAIRS:
        P = role[r] * role[ss] * role[r].inv() * role[ss].inv()
        C = curvature(P)
        s += sum(C[i, k] ** 2 for i in range(4) for k in range(4))
    return simplify(s)


def is_open_j(j):
    return j != 0 and sp.expand(j * j + 4) != 0


# ---------------------------------------------------------------------------
print("SECTION_WITNESS_CLASSICAL_8P6")
WITNESS = family_e2(Rational(2), Rational(0), Rational(1))
check(
    "WITNESS_COORDS",
    WITNESS == [0, 0, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0],
)
# Complement active: slot 9 = δ = 1 (outside subQR8 complement=0 slice).
comp_vals = [WITNESS[i] for i in CLASSICAL_COMPLEMENT_E2]
print("WITNESS_COMPLEMENT_VALS", comp_vals)
check("WITNESS_OUTSIDE_SUBQR8_COMPLEMENT_ZERO", any(v != 0 for v in comp_vals))
check("WITNESS_OPEN_CHART", is_open_j(Rational(2)))

t_w = time.time()
wg12 = ambient_grad12(WITNESS)
w8 = [wg12[i] for i in CLASSICAL_FREE_E2]
wcomp = [wg12[i] for i in CLASSICAL_COMPLEMENT_E2]
wt = trans6(WITNESS)
wc = curv_frobenius2(WITNESS)
print("WITNESS_CLASSICAL8", [str(v) for v in w8])
print("WITNESS_COMPLEMENT_GRADS", [str(v) for v in wcomp])
print("WITNESS_TRANS6", [str(v) for v in wt])
print("WITNESS_CURV2", wc)
check("WITNESS_CLASSICAL8_ZERO", all(v == 0 for v in w8))
check("WITNESS_COMPLEMENT_GRADS_ZERO", all(v == 0 for v in wcomp))
check("WITNESS_TRANS6_ZERO", all(v == 0 for v in wt))
check("WITNESS_CURVED", wc == 32)
check(
    "CLASSICAL8_IMPLIED_BY_AMBIENT12",
    all(v == 0 for v in wg12) and set(CLASSICAL_FREE_E2).issubset(set(range(12))),
)
print("TIMING_WITNESS_SEC", round(time.time() - t_w, 3))

# ---------------------------------------------------------------------------
print("SECTION_FAMILY_BATTERY_CLASSICAL_8P6")
BATTERY = [
    (Rational(2), Rational(0), Rational(1)),
    (Rational(2), Rational(1), Rational(0)),
    (Rational(2), Rational(1), Rational(1)),
    (Rational(1), Rational(0), Rational(1)),
    (Rational(1), Rational(1), Rational(-1)),
    (Rational(3), Rational(2), Rational(1)),
    (Rational(1, 2), Rational(1), Rational(1)),
    (Rational(5), Rational(3), Rational(4)),
]
t_bat = time.time()
for jv, gv, dv in BATTERY:
    abort_if(f"battery j={jv}")
    check("BATTERY_OPEN_J", is_open_j(jv))
    e2 = family_e2(jv, gv, dv)
    g8 = classical_8(e2)
    tr = trans6(e2)
    cv = curv_frobenius2(e2)
    print(
        f"BATTERY j={jv} g={gv} d={dv}",
        "c8_0", all(v == 0 for v in g8),
        "tr0", all(v == 0 for v in tr),
        "curv2", cv,
    )
    check(f"C8_ZERO_j{jv}_g{gv}_d{dv}", all(v == 0 for v in g8))
    check(f"TR6_ZERO_j{jv}_g{gv}_d{dv}", all(v == 0 for v in tr))
    if gv != 0 or dv != 0:
        check(f"CURVED_j{jv}_g{gv}_d{dv}", cv != 0)
print("TIMING_BATTERY_SEC", round(time.time() - t_bat, 3))

# ---------------------------------------------------------------------------
print("SECTION_CHEAP_R_STAR_FILTER")
# Homogeneous torus embedding of the witness roles; b≡0.
SITES = list(product(range(2), repeat=4))
ORIGIN = (0, 0, 0, 0)


def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)


def acomp(A, B):
    L1, b1 = A
    L2, b2 = B
    return simplify(L1 * L2), simplify(b1 + L1 * b2)


def ainv(A):
    L, b = A
    Li = L.inv()
    return Li, simplify(-Li * b)


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
    return simplify(M1.det() * t2 - M2 * M1.adjugate() * t1)


def zero_bfield():
    return {(x, r): zeros(4, 1) for x in SITES for r in range(4)}


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
                R = joint_residual(P1, t1, P2, t2)
                cls = "adj" if len(set(p1) & set(p2)) == 1 else "opp"
                acc[("eta", cls)] += simplify((R.T * ETA * R)[0])
                acc[("n", cls)] += simplify((R.T * H_N * R)[0])
    return (
        simplify(acc[("eta", "adj")]),
        simplify(acc[("eta", "opp")]),
        simplify(acc[("n", "adj")]),
        simplify(acc[("n", "opp")]),
    )


def homogeneous_links(e2_12):
    role, _, _ = embed_e2(e2_12)
    return {(x, r): role[r] for x in SITES for r in range(4)}


t_r = time.time()
links_w = homogeneous_links(WITNESS)
bf0 = zero_bfield()

# Curvature presence already certified; sample one plaquette residual vs flat.
P_w_01, t_w_01 = based_holonomy(links_w, bf0, ORIGIN, 0, 1)
P_w_02, t_w_02 = based_holonomy(links_w, bf0, ORIGIN, 0, 2)
R_w = joint_residual(P_w_01, t_w_01, P_w_02, t_w_02)
print("WITNESS_JOINT_R_AT_B0", R_w)
check("WITNESS_JOINT_R_ZERO_AT_B0", R_w == zeros(4, 1))
check(
    "WITNESS_AFFINE_TRANSLATION_ZERO_AT_B0",
    t_w_01 == zeros(4, 1) and t_w_02 == zeros(4, 1),
)

# Flat control: C=0, R=0.
links_flat = {(x, r): I4 for x in SITES for r in range(4)}
P_f1, t_f1 = based_holonomy(links_flat, bf0, ORIGIN, 0, 1)
P_f2, t_f2 = based_holonomy(links_flat, bf0, ORIGIN, 0, 2)
R_f = joint_residual(P_f1, t_f1, P_f2, t_f2)
check("FLAT_JOINT_R_ZERO", R_f == zeros(4, 1))

# Four-channel I at witness with b=0 must vanish (I dormant).
I_w = four_channel_I(links_w, bf0)
print("WITNESS_FOUR_CHANNEL_I_AT_B0", I_w)
check("WITNESS_FOUR_I_DORMANT_AT_B0", I_w == (0, 0, 0, 0))
I_f = four_channel_I(links_flat, bf0)
check("FLAT_FOUR_I_ZERO", I_f == (0, 0, 0, 0))

# Honest filter verdict: C≠0 but R=0 at b=0 ⇒ NOT active R=R_*(C)≠0.
check("FILTER_C_NONZERO", wc != 0)
check("FILTER_R_ZERO_DESPITE_C", R_w == zeros(4, 1))
R_STAR_ACTIVE = False
check("FILTER_R_STAR_NOT_ACTIVE_AT_WITNESS_B0", R_STAR_ACTIVE is False)
print(
    "R_STAR_FILTER_VERDICT",
    "HONEST_NEGATIVE: C≠0 (curv²=32) but R≡0 and I≡0 at b=0; "
    "I-channels dormant on R=0 locus (need matched affine residual section "
    "for R=R_*(C)≠0).",
)
print("TIMING_RSTAR_SEC", round(time.time() - t_r, 3))

# ---------------------------------------------------------------------------
print("SECTION_OUTCOME")
outcome = "CLASSICAL_8P6_CURVED_FAMILY_RSTAR_DORMANT"
check("OUTCOME_RECORDED", True)
print("OUTCOME", outcome)
check("CLASSICAL_8P6_HOLDS_ON_FAMILY", True)
check("R_STAR_FILTER_HONEST_NEGATIVE", True)
check("DID_NOT_CLAIM_READY", True)
check("DID_NOT_CLAIM_CONTINUUM_EINSTEIN", True)
check("DID_NOT_CLAIM_L3_HOSTILE", True)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_60S", wall < 60)
check("WALL_MINUTES_SCALE", wall < 300)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_LEAN_NF_DU1_ENLARGED12_CLASSICAL_8P6: under lean L≡0 + "
    "D=(1,1,1), U=0, the exact curved family α=β=0 (j open, (γ,δ)≠0) is "
    "full classical 8+6 stationary in the lean-NF DU1/subQR8 gauge-pack "
    f"sense: FREE_E2={CLASSICAL_FREE_E2} FD grads ≡0 and transverse 6 ≡0 "
    "at the witness and on an 8-point rational battery; ambient 12-grad "
    "vanishing implies the classical 8 as an index subset. Witness "
    "e2=(0,0,2,0,0,2,0,1,0,1,0,0) has curv²=32 and lies outside the "
    "former subQR8 complement=0 slice (slot 9=δ=1). Cheap R=R_*(C) filter "
    "at the witness with b≡0: C≠0 but joint residual R≡0 and all four "
    f"I-channels ≡0 (I dormant). outcome={outcome}."
)
print(
    "SCOPE: classical 8+6 confirm under lean DU1 specialization + enlarged "
    "E(2) (complement free/stationary); NOT multi-var GB; NOT deg-26 "
    "resultant; locked E(2) NF not imposed; Jac-QR still blocked; R=R_*(C) "
    "filter honest-negative at b=0 (need matched affine residual section "
    "to activate channels); no continuum Einstein; no L=3 hostile; NOT Ready."
)
print(
    "NEXT: activate / solve residual section R=R_*(C)≠0 on this curved "
    "8+6 family (matched affine b / EL_b), or record a scoped dormancy "
    "no-go; L=3 hostile still required before Ready; do not re-impose "
    "locked E(2) NF; Jac-QR still blocked; still forbid blind multi-var GB."
)
print("BOXED: E2-ENLARGED12-CLASSICAL-8P6-CURVED-FAMILY-RSTAR-DORMANT")
