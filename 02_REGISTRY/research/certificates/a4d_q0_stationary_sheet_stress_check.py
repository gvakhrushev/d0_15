#!/usr/bin/env python3
"""Two-mode optical sheet for the real q0 Fourier path.

Task: EXP-A4D-Q0-STATIONARY-SHEET-STRESS

Characters:
  A = (i, i, -i, -i), every backward difference nonzero;
  B = (-1, 1, -1, 1), zeros on roles 1 and 3.

The metric path is the #262 real conjugate pair on the flat center,

  Q(x) = eta + eps * (q0(z) chi_z(x) + conjugate),

with q0 = d d^T and d_r = z_r^{-1} - 1. The source is held at vacuum.
No nine-orbit census, no rank-9 rerun, and no recomputation of the open
#240 shear moment.

Terminal: A4D-Q0-TWO-MODE-OPTICAL-SHEET-JET
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

import sympy as sp

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + ((" :: " + detail) if detail else ""))


PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
ETA_DIAG = (1, -1, -1, -1)
I4 = sp.eye(4)
SYM = [(a, b) for a in range(4) for b in range(a, 4)]

LORENTZ = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = 1
    X[i, 0] = 1
    LORENTZ.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ.append(X)
LORENTZ_INT = [[[int(X[a, b]) for b in range(4)] for a in range(4)] for X in LORENTZ]

G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
check("STAR_SQUARE_MINUS_ID", STAR * STAR == -sp.eye(6))


def orient(face) -> int:
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def wedge(u, v):
    return sp.Matrix([sp.expand(u[a] * v[b] - u[b] * v[a]) for a, b in PAIRS])


def bivector(tangent):
    dressed = tangent * ETA
    return sp.Matrix([dressed[a, b] for a, b in PAIRS])


def gram_lift(q):
    return q * ETA / 2


def sym_vec(q):
    return sp.Matrix([sp.expand(q[a, b]) for a, b in SYM])


def einstein_coord(h, k):
    k = sp.Matrix(k)
    k_up = ETA * k
    k2 = sp.expand((k.T * ETA * k)[0])
    tr = sp.expand(sum(ETA[a, a] * h[a, a] for a in range(4)))
    kkh = sp.expand((k_up.T * h * k_up)[0])
    lower = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            kh_nu = sum(k_up[r] * h[nu, r] for r in range(4))
            kh_mu = sum(k_up[r] * h[mu, r] for r in range(4))
            lower[mu, nu] = sp.expand(
                sp.Rational(1, 2)
                * (
                    k[mu] * kh_nu
                    + k[nu] * kh_mu
                    - k2 * h[mu, nu]
                    - k[mu] * k[nu] * tr
                    - ETA[mu, nu] * (kkh - k2 * tr)
                )
            )
    upper = sp.expand(ETA * lower * ETA)
    return sp.Matrix([
        sp.expand((1 if a == b else 2) * upper[a, b]) for a, b in SYM
    ])


# Owned polarized symbol, cut before the projective rank cover.
_OWNER = (
    "02_REGISTRY/research/certificates/a4d_metric_null_hessian_complex_check.py"
)
_src = open(_OWNER, encoding="utf-8").read()
_cut = _src.index("# Exact projective cover of d != 0.")
_ns = {"__name__": "_q0_owner_cut"}
exec(compile(_src[:_cut], _OWNER, "exec"), _ns)
C_OF_D = _ns["C"]
D_SYMS = _ns["d"]


def C_at(values):
    return C_OF_D.subs({D_SYMS[i]: values[i] for i in range(4)})


# ---------------------------------------------------------------------------
# Degree-2 arithmetic for the vacuum connection Hessian.
# ---------------------------------------------------------------------------

PAIR_GEN = []
for gen in LORENTZ:
    vec = sp.simplify(G2 * STAR * bivector(gen))
    PAIR_GEN.append([Fraction(int(vec[i])) for i in range(6)])


class Poly:
    __slots__ = ("c",)

    def __init__(self, c=None):
        self.c = c or {}

    @staticmethod
    def K(v):
        return Poly({(0, 0): Fraction(v)}) if v else Poly()

    def __add__(self, other):
        out = dict(self.c)
        for key, val in other.c.items():
            out[key] = out.get(key, Fraction(0)) + val
            if out[key] == 0:
                del out[key]
        return Poly(out)

    def __mul__(self, other):
        out = {}
        for (i, j), a in self.c.items():
            for (k, l), b in other.c.items():
                if i + k + j + l > 2:
                    continue
                key = (i + k, j + l)
                out[key] = out.get(key, Fraction(0)) + a * b
                if out[key] == 0:
                    del out[key]
        return Poly(out)

    def ts(self):
        return self.c.get((1, 1), Fraction(0))


def eye_m():
    M = [[Poly() for _ in range(4)] for _ in range(4)]
    for i in range(4):
        M[i][i] = Poly.K(1)
    return M


def mul_m(A, B):
    C = [[Poly() for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for k in range(4):
            if not A[i][k].c:
                continue
            for j in range(4):
                if B[k][j].c:
                    C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C


def add_gen(M, coeff, gen):
    """Add coeff(t,s) * integer generator into a link matrix."""
    for i in range(4):
        for j in range(4):
            if gen[i][j]:
                M[i][j] = M[i][j] + Poly({coeff: Fraction(gen[i][j])})
    return M


def inv_series(X):
    XX = mul_m(X, X)
    out = eye_m()
    for i in range(4):
        for j in range(4):
            out[i][j] = out[i][j] + Poly({k: -v for k, v in X[i][j].c.items()}) + XX[i][j]
    return out


def shift_I(L):
    return [[L[i][j] + Poly({(0, 0): Fraction(-1)}) if i == j else L[i][j] for j in range(4)] for i in range(4)]


def curvature_R(L1, L2, L3, L4):
    P = mul_m(mul_m(L1, L2), mul_m(inv_series(shift_I(L3)), inv_series(shift_I(L4))))
    X = shift_I(P)
    inv = inv_series(X)
    half = Poly.K(Fraction(1, 2))
    return [[half * (P[i][j] + Poly({k: -v for k, v in inv[i][j].c.items()})) for j in range(4)] for i in range(4)]


# G2*STAR in the bivector basis. The vacuum density is B^T (G2 STAR) bivector(R),
# with bivector(R)_(a,b) = (R eta)_(a,b).
_STAR_OP = G2 * STAR
STAR_OP = [[Fraction(int(_STAR_OP[i, j])) for j in range(6)] for i in range(6)]


def vacuum_density(R, face):
    u, v = [i for i in range(4) if i not in face]
    B = [Fraction(0)] * 6
    if u < v:
        B[PINDEX[(u, v)]] = Fraction(1)
    else:
        B[PINDEX[(v, u)]] = Fraction(-1)
    biv = []
    for a, b in PAIRS:
        biv.append(Poly.K(ETA_DIAG[b]) * R[a][b])
    contracted = [Poly() for _ in range(6)]
    for i in range(6):
        for j in range(6):
            if STAR_OP[i][j] and biv[j].c:
                contracted[i] = contracted[i] + Poly.K(STAR_OP[i][j]) * biv[j]
    acc = Poly()
    sign = orient(face)
    for i in range(6):
        if B[i] and contracted[i].c:
            acc = acc + Poly.K(sign * B[i]) * contracted[i]
    return acc


def step(site, role, period):
    moved = list(site)
    moved[role] = (moved[role] + 1) % period
    return tuple(moved)


def hessian(period, chi) -> list[list[Fraction]]:
    sites = list(product(range(period), repeat=4))
    ch = {site: Fraction(int(chi(site))) for site in sites}

    def link(site, role, dir_a, dir_b):
        M = eye_m()
        amp = ch[site]
        for direction, monomial in ((dir_a, (1, 0)), (dir_b, (0, 1))):
            role_d, gen_d = divmod(direction, 6)
            if role == role_d:
                add_gen(M, monomial, [[LORENTZ_INT[gen_d][i][j] * int(amp) for j in range(4)] for i in range(4)])
        return M

    def bilinear(dir_a, dir_b) -> Fraction:
        total = Poly()
        for y in sites:
            for r, s in PAIRS:
                R = curvature_R(
                    link(y, r, dir_a, dir_b),
                    link(step(y, r, period), s, dir_a, dir_b),
                    link(step(y, s, period), r, dir_a, dir_b),
                    link(y, s, dir_a, dir_b),
                )
                total = total + vacuum_density(R, (r, s))
        return total.ts()

    H = [[Fraction(0) for _ in range(24)] for _ in range(24)]
    for b in range(24):
        for a in range(b, 24):
            val = bilinear(a, b)
            H[a][b] = val
            H[b][a] = val
    return H


# ---------------------------------------------------------------------------
# Position-space connection Euler at identity links.
# ---------------------------------------------------------------------------

def connection_euler(period, leg_of):
    sites = list(product(range(period), repeat=4))
    acc = {(site, role, g): sp.Integer(0) for site in sites for role in range(4) for g in range(6)}
    for y in sites:
        legs = leg_of(y)
        for r, s in PAIRS:
            u, v = [i for i in range(4) if i not in (r, s)]
            B = wedge(legs[u], legs[v])
            sign = orient((r, s))
            weighted = [sp.expand(sign * (B.T * sp.Matrix(PAIR_GEN[g]))[0]) for g in range(6)]
            slots = (
                (y, r, 1),
                (step(y, r, period), s, 1),
                (step(y, s, period), r, -1),
                (y, s, -1),
            )
            for site, role, slot_sign in slots:
                for g in range(6):
                    acc[(site, role, g)] += slot_sign * weighted[g]
    return acc


def fourier(acc, chi):
    out = [sp.Integer(0) for _ in range(24)]
    for (site, role, g), value in acc.items():
        out[6 * role + g] += sp.conjugate(chi(site)) * value
    return sp.Matrix([sp.expand(x) for x in out])


def series_coeff(vec, eps, n):
    out = []
    for v in vec:
        series = sp.series(sp.sympify(v), eps, 0, n + 1).removeO()
        out.append(sp.expand(series).coeff(eps, n))
    return sp.Matrix(out)


# ---------------------------------------------------------------------------
# Modes, symbol null vector, and the two Einstein covectors.
# ---------------------------------------------------------------------------

Z_A = (sp.I, sp.I, -sp.I, -sp.I)
Z_B = (sp.Integer(-1), sp.Integer(1), sp.Integer(-1), sp.Integer(1))


def d_of(z):
    return sp.Matrix([sp.together(1 / z[r] - 1) for r in range(4)])


def q_of(z):
    d = d_of(z)
    return sp.expand(d * d.T)


D_A = d_of(Z_A)
Q_A = q_of(Z_A)
D_B = d_of(Z_B)
Q_B = q_of(Z_B)
TH_A = sp.Matrix([sp.arg(Z_A[i]) for i in range(4)])
TH_B = sp.Matrix([sp.arg(Z_B[i]) for i in range(4)])

check("A_D", [sp.simplify(D_A[i]) for i in range(4)] == [-1 - sp.I, -1 - sp.I, -1 + sp.I, -1 + sp.I])
check("B_D", [sp.simplify(D_B[i]) for i in range(4)] == [-2, 0, -2, 0])
check("A_MINKOWSKI_NONZERO", sp.simplify((D_A.T * ETA * D_A)[0]) == 4 * sp.I)
check("B_MINKOWSKI_NULL", sp.simplify((D_B.T * ETA * D_B)[0]) == 0)
check(
    "B_SUPPORT_00_02_22",
    [sp.simplify(sym_vec(Q_B)[i]) for i in range(10)] == [4, 0, 4, 0, 0, 0, 0, 4, 0, 0],
)
check("B_SLOT_11_ZERO", sp.simplify(Q_B[1, 1]) == 0)

def parallel(u, v) -> bool:
    return all(sp.simplify(u[a] * v[b] - u[b] * v[a]) == 0 for a, b in PAIRS)

check("A_D_NOT_PARALLEL_TO_ARG", not parallel(D_A, TH_A))
check("B_D_PARALLEL_TO_ARG", parallel(D_B, TH_B))
check("A_C_Q0_ZERO", sp.simplify(C_at(D_A) * sym_vec(Q_A)) == sp.zeros(24, 1))
check("B_C_Q0_ZERO", sp.simplify(C_at(D_B) * sym_vec(Q_B)) == sp.zeros(24, 1))

G_A_TH = sp.simplify(einstein_coord(Q_A, TH_A))
G_A_D = sp.simplify(einstein_coord(Q_A, D_A))
G_B_TH = sp.simplify(einstein_coord(Q_B, TH_B))
G_B_D = sp.simplify(einstein_coord(Q_B, D_B))
check(
    "A_G_AT_ARG",
    [G_A_TH[i] for i in range(10)] == [sp.pi ** 2, -2 * sp.pi ** 2, 0, 0, sp.pi ** 2, 0, 0, 0, 0, 0],
)
check("A_G_AT_D_ZERO", G_A_D == sp.zeros(10, 1))
check("B_G_AT_ARG_ZERO", G_B_TH == sp.zeros(10, 1))
check("B_G_AT_D_ZERO", G_B_D == sp.zeros(10, 1))
check("A_CONJUGATE_EINSTEIN", sp.simplify(einstein_coord(sp.conjugate(Q_A), -TH_A) - sp.conjugate(G_A_TH)) == sp.zeros(10, 1))
check("GAUGE_AT_A_ARG", sp.simplify(einstein_coord(TH_A * TH_A.T, TH_A)) == sp.zeros(10, 1))
h_hostile = sp.zeros(4)
h_hostile[1, 2] = h_hostile[2, 1] = 1
check("HOSTILE_EINSTEIN_NONZERO", sp.simplify(einstein_coord(h_hostile, [1, 0, 0, 0])) != sp.zeros(10, 1))

# ---------------------------------------------------------------------------
# Gram signature.  Brief amplitude is q chi + conjugate(q chi).
# ---------------------------------------------------------------------------

eps = sp.symbols("eps", real=True)


def brief_amp(q, chi):
    return sp.expand(q * chi + sp.conjugate(q * chi))


def gram(q, chi):
    return sp.simplify(ETA + eps * brief_amp(q, chi))


for bit, chi in ((1, 1), (-1, -1)):
    Grm = gram(Q_B, chi)
    check("B_DET_CHI_%d" % bit, sp.factor(Grm.det()) == -1)
    disc = 64 * eps ** 2 + 1
    check("B_SQRT_GAP_CHI_%d" % bit, sp.simplify(disc - (8 * eps) ** 2) == 1)
    # Eigenvalues -1, -1 and 8*bit*eps ± sqrt(disc). The gap forces one of
    # each sign, so the inertia is (1, 3) for every real eps.
    root_sum = sp.simplify((8 * bit * eps + sp.sqrt(disc)) + (8 * bit * eps - sp.sqrt(disc)))
    root_prod = sp.simplify((8 * bit * eps + sp.sqrt(disc)) * (8 * bit * eps - sp.sqrt(disc)))
    check("B_ROOTS_CHI_%d" % bit, root_sum == 16 * bit * eps and root_prod == -1)

for t in range(4):
    chi = sp.I ** t
    Grm = gram(Q_A, chi)
    det = sp.factor(Grm.det())
    expected = {0: -1, 1: 8 * eps - 1, 2: -1, 3: -8 * eps - 1}[t]
    check("A_DET_PHASE_%d" % t, sp.simplify(det - expected) == 0)

check("A_ODD_SQRT_GAP", sp.simplify((16 * eps ** 2 + 1) - (4 * eps) ** 2) == 1)
lam = sp.symbols("lam")
cubic = lam ** 3 + lam ** 2 - (1 + 64 * eps ** 2) * lam - 1
for t in (0, 2):
    Grm = gram(Q_A, sp.I ** t)
    char = sp.factor(Grm.charpoly(lam).as_expr())
    check("A_EVEN_CHAR_PHASE_%d" % t, sp.expand(char - (lam + 1) * cubic) == 0)
disc_cubic = sp.factor(sp.discriminant(cubic, lam))
check("A_EVEN_DISC", disc_cubic == 2048 * eps ** 2 * (512 * eps ** 4 + 26 * eps ** 2 + 1))
quad = sp.Poly(512 * eps ** 2 + 26 * eps + 1, eps)
check("A_EVEN_DISC_QUARTIC_POSITIVE", int(quad.discriminant()) < 0 and quad.LC() == 512)
check("A_EVEN_F_M1", sp.expand(cubic.subs(lam, -1) - 64 * eps ** 2) == 0)
check("A_EVEN_F_0", sp.expand(cubic.subs(lam, 0) + 1) == 0)
check("A_EVEN_F_1", sp.expand(cubic.subs(lam, 1) + 64 * eps ** 2) == 0)
check("A_EVEN_AT_ZERO", sp.factor(cubic.subs(eps, 0)) == (lam - 1) * (lam + 1) ** 2)

# ---------------------------------------------------------------------------
# Exact frames and connection Euler.
# ---------------------------------------------------------------------------

def chi_B(site):
    return sp.Integer((-1) ** (site[0] + site[2]))


def chi_A(site):
    t = (site[0] + site[1] - site[2] - site[3]) % 4
    return sp.I ** t


def chi_z2(site):
    return sp.Integer((-1) ** sum(site))


H_B = gram_lift(Q_B)
check("B_FRAME_QUADRATIC_VANISHES", sp.simplify(H_B * ETA * H_B.T) == sp.zeros(4))


def legs_B(site):
    scale = eps * chi_B(site)
    return [I4[:, i] + scale * H_B.row(i).T for i in range(4)]


acc_B = connection_euler(2, legs_B)
check(
    "B_CONNECTION_EULER_EXACT_ZERO",
    all(sp.expand(val) == 0 for val in acc_B.values()),
)

Q_11 = sp.zeros(4)
Q_11[1, 1] = 1
H_11 = gram_lift(Q_11)


def legs_11(site):
    scale = eps * chi_B(site)
    return [I4[:, i] + scale * H_11.row(i).T for i in range(4)]


lin_11 = series_coeff(fourier(connection_euler(2, legs_11), chi_B), eps, 1)
check("HOSTILE_Q11_CONNECTION_EULER_NONZERO", lin_11 != sp.zeros(24, 1))


def amp_A(site):
    chi = chi_A(site)
    return sp.expand(Q_A * chi + sp.conjugate(Q_A * chi))


def frame_H(site):
    return gram_lift(amp_A(site))


def frame_S(site):
    H = frame_H(site)
    return sp.Rational(-1, 2) * (H * ETA * H.T) * ETA


def legs_A(site):
    H = frame_H(site)
    S = frame_S(site)
    return [I4[:, i] + eps * H.row(i).T + eps ** 2 * S.row(i).T for i in range(4)]


probe = (1, 0, 0, 0)
Theta = sp.zeros(4)
for i in range(4):
    Theta[i, :] = legs_A(probe)[i].T
gram_err = sp.expand(Theta * ETA * Theta.T - (ETA + eps * amp_A(probe)))
low = sp.Matrix([
    [sp.series(gram_err[i, j], eps, 0, 3).removeO() for j in range(4)]
    for i in range(4)
])
check("A_FRAME_GRAM_THROUGH_EPS2", sp.expand(low) == sp.zeros(4))

print("computing mode A connection Euler")
acc_A = connection_euler(4, legs_A)
check("A_EPS0_ZERO", series_coeff(fourier(acc_A, chi_A), eps, 0) == sp.zeros(24, 1))
for label, chi in (("CHI", chi_A), ("ONE", lambda s: sp.Integer(1)), ("CHI2", lambda s: chi_A(s) ** 2), ("CHI3", lambda s: sp.conjugate(chi_A(s)))):
    c1 = series_coeff(fourier(acc_A, chi), eps, 1)
    check("A_%s_EPS1_ZERO" % label, c1 == sp.zeros(24, 1))

rhs4 = series_coeff(fourier(acc_A, chi_z2), eps, 2)
check("A_CHI2_EQUALS_CHARACTER_SQUARE", all(sp.expand(chi_A(s) ** 2 - chi_z2(s)) == 0 for s in product(range(4), repeat=4)))
check("A_EPS2_NONZERO", rhs4 != sp.zeros(24, 1))

# The eps^2 field is period 2, so the L=4 Fourier sum is 16 times one L=2 cell.
period2_ok = True
for (site, role, g), val in acc_A.items():
    coeff = sp.expand(sp.series(val, eps, 0, 3).removeO().coeff(eps, 2))
    for axis in range(4):
        moved = list(site)
        moved[axis] = (moved[axis] + 2) % 4
        other = sp.expand(sp.series(acc_A[(tuple(moved), role, g)], eps, 0, 3).removeO().coeff(eps, 2))
        if coeff != other:
            period2_ok = False
            break
    if not period2_ok:
        break
check("A_EPS2_FIELD_PERIOD_2", period2_ok)
phase_only = True
by_phase = {}
for (site, role, g), val in acc_A.items():
    coeff = sp.expand(sp.series(val, eps, 0, 3).removeO().coeff(eps, 2))
    key = ((site[0] + site[1] - site[2] - site[3]) % 4, role, g)
    if key in by_phase and by_phase[key] != coeff:
        phase_only = False
        break
    by_phase[key] = coeff
check("A_EPS2_DEPENDS_ONLY_ON_PHASE", phase_only)

# ---------------------------------------------------------------------------
# Vacuum Hessians.  Period-1 determinant must reproduce owned det A0 = 256.
# ---------------------------------------------------------------------------

print("building vacuum Hessians")
H1 = sp.Matrix(hessian(1, lambda _s: 1))
check("TRIVIAL_HESSIAN_DET_256", sp.factor(H1.det()) == 256)
check("TRIVIAL_HESSIAN_RANK_24", H1.rank() == 24)
_a0_start = _src.index("# Rebuild the zero-character connection Hessian A0")
_a0_end = _src.index('check("IR_CONNECTION_HESSIAN_DET_256"')
exec(compile(_src[_a0_start:_a0_end], _OWNER + ":A0", "exec"), _ns)
check("TRIVIAL_HESSIAN_EQUALS_OWNED_A0", H1 == _ns["A0"])
H2_const = sp.Matrix(hessian(2, lambda _s: 1))
check("VOLUME_FACTOR_16_CONSTANT", H2_const == 16 * H1)

Hz2 = sp.Matrix(hessian(2, chi_z2))
check("Z2_HESSIAN_FULL_RANK", Hz2.rank() == 24)
# One L=4 entry of the same character must be 16 times the L=2 entry.
# Computed directly on directions (0, 5), the first nonzero solved slot below
# is not assumed: any single pair certifies the cover factor for this chi.


def hessian_entry(period, chi, dir_a, dir_b) -> Fraction:
    sites = list(product(range(period), repeat=4))
    ch = {site: Fraction(int(chi(site))) for site in sites}

    def link(site, role):
        M = eye_m()
        amp = ch[site]
        for direction, monomial in ((dir_a, (1, 0)), (dir_b, (0, 1))):
            role_d, gen_d = divmod(direction, 6)
            if role == role_d:
                add_gen(
                    M,
                    monomial,
                    [[LORENTZ_INT[gen_d][i][j] * int(amp) for j in range(4)] for i in range(4)],
                )
        return M

    total = Poly()
    for y in sites:
        for r, s in PAIRS:
            R = curvature_R(
                link(y, r),
                link(step(y, r, period), s),
                link(step(y, s, period), r),
                link(y, s),
            )
            total = total + vacuum_density(R, (r, s))
    return total.ts()


check(
    "VOLUME_FACTOR_16_ON_Z2",
    hessian_entry(4, chi_z2, 0, 5) == 16 * hessian_entry(2, chi_z2, 0, 5),
)

check("A_RHS_DIVISIBLE_BY_16", all(int(rhs4[i]) % 16 == 0 for i in range(24)))
rhs2 = sp.Matrix([Fraction(int(rhs4[i]), 16) for i in range(24)])
p2 = sp.simplify(Hz2.LUsolve(-rhs2))
check("A_P2_SOLVES", sp.simplify(Hz2 * p2 + rhs2) == sp.zeros(24, 1))
check("A_P2_NONZERO", p2 != sp.zeros(24, 1))
check("A_P2_EXACT", all(sp.simplify(p2[i]).is_rational for i in range(24)))
print("MODE_A_P2", [int(p2[i]) for i in range(24)])

C_Z2 = C_at([-2, -2, -2, -2])
check("A_CORRECTION_METRIC_SILENT_SYMBOL", sp.simplify(C_Z2.T * p2) == sp.zeros(10, 1))

# Position-space metric Euler of this correction on the L=2 cell, identity legs.
Y = [sp.zeros(4) for _ in range(4)]
for r in range(4):
    for g in range(6):
        Y[r] += p2[6 * r + g] * LORENTZ[g]


def R_linear(site, r, s):
    def X(at, role):
        return chi_z2(at) * Y[role]
    return X(site, r) + X(step(site, r, 2), s) - X(step(site, s, 2), r) - X(site, s)


legs0 = [I4[:, i] for i in range(4)]
metric = sp.zeros(10, 1)
for site in product(range(2), repeat=4):
    for r, s in PAIRS:
        bend = bivector(R_linear(site, r, s))
        u, v = [i for i in range(4) if i not in (r, s)]
        for n, (a, b) in enumerate(SYM):
            direction = sp.zeros(4)
            direction[a, b] = direction[b, a] = 1
            variation = gram_lift(direction)
            dw = wedge(variation[u, :].T, legs0[v]) + wedge(legs0[u], variation[v, :].T)
            metric[n] += orient((r, s)) * (dw.T * G2 * STAR * bend)[0]
check("A_CORRECTION_METRIC_EULER_ZERO", sp.expand(metric) == sp.zeros(10, 1))

# Flat mode-B Hessian. The recorded #240 witness is an input vector, not a
# recomputed shear moment.
HB = sp.Matrix(hessian(2, chi_B))
check("B_HESSIAN_FULL_RANK", HB.rank() == 24)
WITNESS = sp.Matrix([
    0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, -1, 0, -1, 1,
    2, 1, 0, 1, 0, 0,
])
image = sp.simplify(HB * WITNESS)
check("B_WITNESS_NOT_FLAT_KERNEL", image != sp.zeros(24, 1))
print("WITNESS_FLAT_IMAGE", [(i, int(image[i])) for i in range(24) if image[i] != 0])

if FAILS:
    print("A4D-Q0-TWO-MODE-OPTICAL-SHEET-JET: FAIL (%d)" % len(FAILS))
    for name in FAILS:
        print("  - " + name)
    raise SystemExit(1)

print("A4D-Q0-TWO-MODE-OPTICAL-SHEET-JET")
print("MODE_B: identity connection is an exact joint vacuum on the real q0 path for every real eps.")
print("MODE_A: eps^2 obstruction at (-1,-1,-1,-1) has a unique rational solution and that solution is metric-silent.")
print("COMPARE: discrete jet E_Q = O(eps^3); -1/2 G(d) = 0 on both modes; -1/2 G(arg) vanishes on B and not on A.")
print("SCOPE: no physical NOGO, no closure of PR #240, no nine-orbit census, no shear-moment recomputation.")
