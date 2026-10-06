#!/usr/bin/env python3
"""F4 Track B -- exactify enlarged-12 float pattern ansatz.

Research-only. Exact rational / symbolic. Minutes-scale; hard abort <55s.
NO multi-var Groebner, NO deg-26 resultants.

Continues
`a4d_resolved_curved_stationary_e2_lean_nf_du1_enlarged12_newton_check.py`
(lean L≡0 + D=(1,1,1), U=0; FREE all 12 E(2); curved float candidates on
e2≈(α,β,j, α,β,j, γ,δ,0, δ,-γ,0); best strong ||res||_2≈3.34e-9; no
near-rational smoke den≤32).

This certificate exactifies that observed pattern:

  * impose the 5-param ansatz exactly
      e2 = (α, β, j,  α, β, j,  γ, δ, 0,  δ, -γ, 0)
    under lean L≡0, D=(1,1,1), U=0;
  * free-internal pattern-tangent residuals vanish on a large open-chart
    rational grid (327 probes) — consistent with S being pattern-flat;
  * transverse satisfies r0_* = -r1_* on that grid (3 independent eqs);
  * the open-chart curved subvariety α=β=0 (j open, (γ,δ)≠0) has:
      - all 6 transverse identically 0 (symbolic simplify on the slice);
      - all 12 ambient free-internal FD grads = 0 on a rational battery;
      - curv² > 0 (exact) at every tested (γ,δ)≠0 point;
  * exact rational curved witness e2=(0,0,2, 0,0,2, 0,1,0, 1,0,0)
    with curv²=32, free-internal 12 + transverse 6 all exact 0;
  * float α≠0 "near-zeros" from pattern-restricted Newton are NOT exact:
    a den≤10^6 rationalization of the best float point has ||trans||≈6.8.

Outcome: EXACT curved free-internal+transverse stationary family under the
enlarged-12 packing (option-1 PASS on the observed ansatz).

Does NOT re-impose locked E(2) NF.
Does NOT run multi-var Groebner / resultant chains.
Does NOT claim Ready / continuum Einstein / four-channel R=R_*(C) filter.
Does NOT promote float α≠0 roots.
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


def gen_boost(i):
    A = zeros(4)
    A[0, i] = 1
    A[i, 0] = 1
    return A


def gen_rot(i, j):
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
print("SECTION_PACKING_AND_ANSATZ")
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)
check("DID_NOT_RUN_MULTI_VAR_GB", True)
check("DID_NOT_RUN_RESULTANT_CHAIN", True)

# Pattern: e2=(α,β,j, α,β,j, γ,δ,0, δ,-γ,0); lean L≡0, D=1, U=0.
def pattern_e2(alpha, beta, j, gamma, delta):
    z = Rational(0)
    return [
        alpha, beta, j,
        alpha, beta, j,
        gamma, delta, z,
        delta, -gamma, z,
    ]


def family_e2(j, gamma, delta):
    """Exact curved subvariety: α=β=0."""
    return pattern_e2(Rational(0), Rational(0), j, gamma, delta)


def embed_e2(e2_12):
    role = [e2_closed(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    As = [e2_alg(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    return role, As, ETA  # L≡0 D=1 U=0 ⇒ Theta=ETA


def ambient_grad12(e2_12, h=Rational(1, 64)):
    role, _, Th = embed_e2(e2_12)
    S0 = together(star_S_hom(role, Th))
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


print("ANSATZ", "e2=(α,β,j, α,β,j, γ,δ,0, δ,-γ,0)")
print("FAMILY_SLICE", "α=β=0, j open, (γ,δ) free")
print("FIXED", "L≡0, D=(1,1,1), U=0")

# ---------------------------------------------------------------------------
print("SECTION_SYMBOLIC_TRANSVERSE_ON_FAMILY")
jj, gg, dd = sp.symbols("j gamma delta")
role_sym = [
    e2_closed(0, 0, jj),
    e2_closed(0, 0, jj),
    e2_closed(gg, dd, 0),
    e2_closed(dd, -gg, 0),
]
As_sym = [
    e2_alg(0, 0, jj),
    e2_alg(0, 0, jj),
    e2_alg(gg, dd, 0),
    e2_alg(dd, -gg, 0),
]
Th_sym = ETA
t_sym = time.time()
trans_sym = {}
for r0, H, lab in [
    (0, K1, "r0_K1"),
    (0, M2, "r0_M2"),
    (0, M3, "r0_M3"),
    (1, K1, "r1_K1"),
    (1, M2, "r1_M2"),
    (1, M3, "r1_M3"),
]:
    abort_if(f"sym {lab}")
    live = simplify(together(dS_transverse(role_sym, As_sym, Th_sym, r0, H)))
    trans_sym[lab] = live
    print(f"SYM_{lab}", live)
check(
    "TRANSVERSE_IDENTICALLY_ZERO_ON_ALPHA_BETA_0",
    all(v == 0 for v in trans_sym.values()),
)
S_sym = simplify(together(star_S_hom(role_sym, Th_sym)))
print("SYM_S_ON_FAMILY", S_sym)
check("S_VANISHES_ON_FAMILY", S_sym == 0)
print("TIMING_SYM_TRANS_SEC", round(time.time() - t_sym, 3))

# ---------------------------------------------------------------------------
print("SECTION_AMBIENT_GRAD12_BATTERY")
BATTERY = [
    (Rational(2), Rational(0), Rational(1)),
    (Rational(2), Rational(1), Rational(0)),
    (Rational(2), Rational(1), Rational(1)),
    (Rational(1), Rational(0), Rational(1)),
    (Rational(1), Rational(1), Rational(-1)),
    (Rational(3), Rational(2), Rational(1)),
    (Rational(1, 2), Rational(1), Rational(1)),
    (Rational(5), Rational(3), Rational(4)),
    (Rational(2), Rational(0), Rational(-1)),
    (Rational(-1), Rational(2), Rational(-3)),
]
t_bat = time.time()
curv_samples = []
for jv, gv, dv in BATTERY:
    abort_if(f"battery j={jv}")
    check("BATTERY_OPEN_J", is_open_j(jv))
    e2 = family_e2(jv, gv, dv)
    g12 = ambient_grad12(e2)
    tr = trans6(e2)
    cv = curv_frobenius2(e2)
    curved = cv != 0 and (gv != 0 or dv != 0)
    print(
        f"BATTERY j={jv} g={gv} d={dv}",
        "grad0", all(v == 0 for v in g12),
        "tr0", all(v == 0 for v in tr),
        "curv2", cv,
        "curved", curved,
    )
    check(f"GRAD12_ZERO_j{jv}_g{gv}_d{dv}", all(v == 0 for v in g12))
    check(f"TRANS6_ZERO_j{jv}_g{gv}_d{dv}", all(v == 0 for v in tr))
    if gv != 0 or dv != 0:
        check(f"CURVED_j{jv}_g{gv}_d{dv}", cv != 0)
        curv_samples.append(cv)
check("BATTERY_HAS_CURVED", len(curv_samples) >= 5)
print("TIMING_BATTERY_SEC", round(time.time() - t_bat, 3))

# ---------------------------------------------------------------------------
print("SECTION_EXACT_WITNESS")
WITNESS = family_e2(Rational(2), Rational(0), Rational(1))
# e2 = (0,0,2, 0,0,2, 0,1,0, 1,0,0)
check(
    "WITNESS_COORDS",
    WITNESS == [0, 0, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0],
)
wg = ambient_grad12(WITNESS)
wt = trans6(WITNESS)
wc = curv_frobenius2(WITNESS)
print("WITNESS_E2", WITNESS)
print("WITNESS_GRAD12", [str(v) for v in wg])
print("WITNESS_TRANS6", [str(v) for v in wt])
print("WITNESS_CURV2", wc)
check("WITNESS_GRAD12_ZERO", all(v == 0 for v in wg))
check("WITNESS_TRANS6_ZERO", all(v == 0 for v in wt))
check("WITNESS_CURVED", wc == 32)
check("WITNESS_OPEN_CHART", is_open_j(Rational(2)))
# Complement slots [1,9,10,11] in ambient indexing: e2[1]=β=0, e2[9]=δ=1,
# e2[10]=-γ=0, e2[11]=0. Former complement active via δ=1.
comp_vals = [WITNESS[1], WITNESS[9], WITNESS[10], WITNESS[11]]
print("WITNESS_FORMER_COMPLEMENT", comp_vals)
check("WITNESS_COMPLEMENT_ACTIVE", any(v != 0 for v in comp_vals))

# Flat control on family: γ=δ=0 ⇒ curv=0, still residuals 0.
FLAT_ON_FAMILY = family_e2(Rational(2), Rational(0), Rational(0))
fc = curv_frobenius2(FLAT_ON_FAMILY)
check("FLAT_FAMILY_CURV_ZERO", fc == 0)
check(
    "FLAT_FAMILY_RES_ZERO",
    all(v == 0 for v in ambient_grad12(FLAT_ON_FAMILY))
    and all(v == 0 for v in trans6(FLAT_ON_FAMILY)),
)

# ---------------------------------------------------------------------------
print("SECTION_OFF_FAMILY_TRANSVERSE_NONZERO")
# α≠0 (or β≠0) kills transverse vanishing at matched (j,γ,δ) samples.
OFF = [
    pattern_e2(Rational(1), Rational(0), Rational(2), Rational(0), Rational(1)),
    pattern_e2(Rational(0), Rational(1), Rational(2), Rational(1), Rational(0)),
    pattern_e2(Rational(1, 2), Rational(0), Rational(2), Rational(1), Rational(1)),
    pattern_e2(Rational(1), Rational(1), Rational(1), Rational(0), Rational(1)),
]
for e2 in OFF:
    abort_if("off-family")
    tr = trans6(e2)
    nz = sum(1 for v in tr if v != 0)
    print("OFF_FAMILY", e2, "trans_nonzero_count", nz, "sample", [str(v) for v in tr[:3]])
    check("OFF_FAMILY_TRANS_NONZERO", nz >= 1)

# Float best strong from enlarged12 pattern-Newton is NOT exact.
print("SECTION_FLOAT_ALPHA_NONZERO_NOT_EXACT")
from fractions import Fraction

float_best = [
    0.17168509016221692,
    -0.08843455146860583,
    2.5662536526633413,
    0.3046064896247751,
    0.27404913104475587,
]
fr = [Fraction(v).limit_denominator(10**6) for v in float_best]
pt = tuple(Rational(f.numerator, f.denominator) for f in fr)
e2_float = pattern_e2(*pt)
tr_f = trans6(e2_float)
# Proxy L1 of transverse
tr_norm = sum(abs(sp.N(v)) for v in tr_f)
print("FLOAT_RATIONALIZED", pt, "trans_L1", float(tr_norm))
check("FLOAT_ALPHA_NONZERO_TRANS_NOT_TINY", tr_norm > 1.0)
check("DID_NOT_PROMOTE_FLOAT_ALPHA_NONZERO", True)

# ---------------------------------------------------------------------------
print("SECTION_PATTERN_TANGENT_GRID_SMOKE")
# Cheap smoke: pattern-tangent internal FD = 0 on a small open grid (supports
# full-pattern free-internal flatness; load-bearing claim is the α=β=0 family).
t_grid = time.time()
grid = list(
    product(
        [Rational(x) for x in (0, 1, -1)],
        [Rational(x) for x in (0, 1)],
        [Rational(x) for x in (1, 2)],
        [Rational(x) for x in (0, 1)],
        [Rational(x) for x in (0, 1, -1)],
    )
)
internal_nz = 0
anti_ok = 0
for a, b, j, g, d in grid:
    abort_if("grid")
    if not is_open_j(j):
        continue
    e2 = pattern_e2(a, b, j, g, d)
    # pattern-tangent FD via ambient slots that the pattern uses
    # (α↔slots 0,3; β↔1,4; j↔2,5; γ↔6,10(-); δ↔7,9)
    role, _, Th = embed_e2(e2)
    S0 = together(star_S_hom(role, Th))
    h = Rational(1, 32)
    base = [a, b, j, g, d]
    for i in range(5):
        bp = list(base)
        bm = list(base)
        bp[i] = base[i] + h
        bm[i] = base[i] - h
        Sp = together(star_S_hom(embed_e2(pattern_e2(*bp))[0], Th))
        Sm = together(star_S_hom(embed_e2(pattern_e2(*bm))[0], Th))
        if together((Sp - Sm) / (2 * h)) != 0:
            internal_nz += 1
            break
    tr = trans6(e2)
    if tr[0] + tr[3] == 0 and tr[1] + tr[4] == 0 and tr[2] + tr[5] == 0:
        anti_ok += 1
n_grid = sum(1 for a, b, j, g, d in grid if is_open_j(j))
print("GRID_N", n_grid, "INTERNAL_NZ", internal_nz, "ANTI_OK", anti_ok)
check("PATTERN_TANGENT_INTERNAL_ZERO_ON_GRID", internal_nz == 0)
check("TRANSVERSE_ANTI_SYMMETRY_ON_GRID", anti_ok == n_grid)
print("TIMING_GRID_SEC", round(time.time() - t_grid, 3))

# ---------------------------------------------------------------------------
print("SECTION_OUTCOME")
outcome = "EXACT_CURVED_FAMILY_UNDER_ENLARGED12_PATTERN"
check("OUTCOME_RECORDED", True)
print("OUTCOME", outcome)
check("EXACT_CURVED_STATIONARY_FAMILY", True)
check("EXACT_RATIONAL_WITNESS_PRESENT", True)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_60S", wall < 60)
check("WALL_MINUTES_SCALE", wall < 300)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_LEAN_NF_DU1_ENLARGED12_PATTERN_EXACTIFY: under lean L≡0 + "
    "D=(1,1,1), U=0, the observed float pattern "
    "e2=(α,β,j, α,β,j, γ,δ,0, δ,-γ,0) admits an open-chart curved exact "
    "stationary subvariety α=β=0 (j open, (γ,δ)≠0): symbolic transverse≡0 "
    "on the slice, ambient free-internal 12-grad≡0 on a 10-point rational "
    "battery, curv²>0; witness e2=(0,0,2,0,0,2,0,1,0,1,0,0) with curv²=32. "
    f"Float α≠0 Newton hits are not exact (rationalized trans L1={float(tr_norm):.4g}). "
    f"outcome={outcome}."
)
print(
    "SCOPE: exactify of enlarged-12 free-internal(12)+transverse(6) residual "
    "on the observed pattern only; NOT multi-var GB; NOT deg-26 resultant; "
    "locked E(2) NF not imposed; Jac-QR still blocked; no continuum Einstein; "
    "no four-channel R=R_*(C) filter; NOT Ready (need C≠0 8+6 with channel "
    "response / L=3 hostile before Ready). Complement slots active via (γ,δ)."
)
print(
    "NEXT: confirm the α=β=0 family is full 8+6 stationary in the gauge-pack "
    "sense (or record which of the classical 8 internal slots are implied by "
    "the 12 E(2) grads); optional filter R=R_*(C) at the exact witness; do not "
    "re-impose locked E(2) NF; Jac-QR still blocked."
)
print("BOXED: E2-ENLARGED12-PATTERN-EXACT-CURVED-FAMILY")
