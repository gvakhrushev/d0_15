#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=1500
"""Metric-silent order-eps kernel ray of the mode-A character.

The connection Hessian at (i,i,-i,-i) has a 4-dimensional kernel. Exactly
one line of it is silent in the order-eps metric Euler. Along the real scale
of that line, after the order-eps^2 repair is readjusted, the order-eps^3
forcing stays outside the connection image.
"""
from itertools import combinations
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
Z4 = sp.zeros(4)
Z6 = sp.zeros(6, 1)
INC = (1, 1, -1, -1)
LORENTZ = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = X[i, 0] = 1
    LORENTZ.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ.append(X)
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
OP = G2 * STAR

def orient(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1

def shift(phase, role):
    return (phase + INC[role]) % 4

def wedge(u, v):
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])

def mmul(A, B):
    out = [Z4, Z4, Z4, Z4]
    for i, a in enumerate(A):
        if a == Z4:
            continue
        for j, b in enumerate(B):
            if i + j > 3 or b == Z4:
                continue
            out[i + j] += a * b
    return [sp.expand(x) for x in out]

def minv(A):
    N = [Z4, A[1], A[2], A[3]]
    N2 = mmul(N, N)
    N3 = mmul(N2, N)
    return [I4, sp.expand(-N[1]), sp.expand(-N[2] + N2[2]), sp.expand(-N[3] + N2[3] - N3[3])]

def pack(vec):
    out = []
    for role in range(4):
        acc = Z4
        for g in range(6):
            c = vec[6 * role + g]
            if c != 0:
                acc += c * LORENTZ[g]
        out.append(sp.expand(acc))
    return out

zA = (sp.I, sp.I, -sp.I, -sp.I)
dvec = sp.Matrix([sp.simplify(1 / zA[r] - 1) for r in range(4)])
q = sp.expand(dvec * dvec.T)
KVEC = sp.Matrix([-1 - sp.I, 0, 0, 0, 0, 0, -1 - sp.I, 0, 0, 0, 0, 0, 1, 0, -1, 0, 1, 0, 1, -1, 0, 1, 0, 0])
YK = pack(KVEC)
YKc = pack(sp.conjugate(KVEC))

def leg_rows(phase):
    chi = sp.I ** phase
    h = sp.expand(q * chi + sp.conjugate(q * chi))
    H = sp.expand(h * ETA / 2)
    S = sp.expand(-(h * ETA) ** 2 / 8)
    U = sp.expand((h * ETA) ** 3 / 16)
    return [(I4[:, i], H.row(i).T, S.row(i).T, U.row(i).T) for i in range(4)]

ROWS = [leg_rows(p) for p in range(4)]

def biv_poly(phase):
    out = {}
    rows = ROWS[phase]
    for r, sf in PAIRS:
        u, v = [i for i in range(4) if i not in (r, sf)]
        poly = [Z6, Z6, Z6, Z6]
        for i in range(4):
            for j in range(4 - i):
                poly[i + j] += wedge(rows[u][i], rows[v][j])
        out[(r, sf)] = [sp.expand(x) for x in poly]
    return out

BIV = [biv_poly(p) for p in range(4)]
BEND_GEN = []
for gen in LORENTZ:
    BEND_GEN.append(sp.Matrix([(gen * ETA)[a, b] for a, b in PAIRS]))

def link_of(phase, role, t, YP):
    A1 = t * ((sp.I ** phase) * YK[role] + ((-sp.I) ** phase) * YKc[role])
    A2 = Z4 if YP is None else ((-sp.Integer(1)) ** phase) * YP[role]
    return [I4, sp.expand(A1), sp.expand(A2), Z4]

def prepare(mats):
    invs = [minv(M) for M in mats]
    P = mmul(mmul(mats[0], mats[1]), mmul(invs[2], invs[3]))
    return invs, minv(P)

def dR_from_prep(mats, invs, Pinv, corner, gen):
    G = [gen, Z4, Z4, Z4]
    if corner == 0:
        dP = mmul(mmul(G, mats[1]), mmul(invs[2], invs[3]))
    elif corner == 1:
        dP = mmul(mmul(mats[0], G), mmul(invs[2], invs[3]))
    elif corner == 2:
        mid = mmul(mmul(invs[2], G), invs[2])
        dP = mmul(mmul(mats[0], mats[1]), mmul([sp.expand(-mid[n]) for n in range(4)], invs[3]))
    else:
        mid = mmul(mmul(invs[3], G), invs[3])
        dP = mmul(mmul(mats[0], mats[1]), mmul(invs[2], [sp.expand(-mid[n]) for n in range(4)]))
    back = mmul(mmul(Pinv, dP), Pinv)
    return [sp.expand((dP[n] + back[n]) / 2) for n in range(4)]

def euler_orders(t, p2):
    YP = None if p2 is None else pack(p2)
    acc = [[sp.zeros(24, 1) for _ in range(4)] for _ in range(4)]
    for base in range(4):
        for r, sf in PAIRS:
            Bpoly = BIV[base][(r, sf)]
            specs = [(base, r), (shift(base, r), sf), (shift(base, sf), r), (base, sf)]
            mats = [link_of(ph, role, t, YP) for ph, role in specs]
            invs, Pinv = prepare(mats)
            sign = orient((r, sf))
            for n, (ph, role) in enumerate(specs):
                for g, gen in enumerate(LORENTZ):
                    dRc = dR_from_prep(mats, invs, Pinv, n, gen)
                    bends = [sp.Matrix([(dRc[k] * ETA)[a, b] for a, b in PAIRS]) for k in range(4)]
                    for deg in range(4):
                        piece = 0
                        for i in range(deg + 1):
                            piece += (Bpoly[i].T * OP * bends[deg - i])[0]
                        acc[ph][deg][6 * role + g] += sign * piece
    return [[sp.Matrix([sp.expand(acc[ph][deg][i]) for i in range(24)]) for deg in range(4)] for ph in range(4)]

def fourier(orders, mode, deg):
    tot = sp.zeros(24, 1)
    for phase in range(4):
        tot += (sp.conjugate(sp.I ** mode) ** phase) * orders[phase][deg]
    return sp.simplify(tot)

FAILS = []

def check(name, cond):
    if cond:
        print("PASS_" + name, flush=True)
    else:
        FAILS.append(name)
        print("FAIL_" + name, flush=True)

bare = euler_orders(0, None)
real_fa = bare[0][2]
check("BARE_ORDER2_IS_REAL_FA", [sp.simplify(real_fa[i]) for i in range(6)] == [8, -4, -4, -4, -4, 0])
for phase in range(4):
    check("BARE_ORDER2_PHASE_%d" % phase, sp.simplify(bare[phase][2] - ((-1) ** phase) * real_fa) == sp.zeros(24, 1))

def B_of(r, sf):
    u, v = [i for i in range(4) if i not in (r, sf)]
    B = sp.zeros(6, 1)
    B[PINDEX[(u, v) if u < v else (v, u)]] = 1 if u < v else -1
    return B

def series_column(active_role, active_gen, chi):
    local = {phase: sp.zeros(24, 1) for phase in range(4)}
    for base in range(4):
        for r, sf in PAIRS:
            specs = [(base, r), (shift(base, r), sf), (shift(base, sf), r), (base, sf)]
            mats = []
            for ph, role in specs:
                M = I4
                if role == active_role:
                    M = M + sval * chi(ph) * LORENTZ[active_gen]
                mats.append(M)
            hol = mats[0] * mats[1] * mats[2].inv() * mats[3].inv()
            hinv = hol.inv()
            sign = orient((r, sf))
            Bb = B_of(r, sf)
            for n, (ph, role) in enumerate(specs):
                for g, gen in enumerate(LORENTZ):
                    L1, L2, L3, L4 = mats
                    if n == 0:
                        dP = gen * L2 * L3.inv() * L4.inv()
                    elif n == 1:
                        dP = L1 * gen * L3.inv() * L4.inv()
                    elif n == 2:
                        dP = L1 * L2 * (-L3.inv() * gen * L3.inv()) * L4.inv()
                    else:
                        dP = L1 * L2 * L3.inv() * (-L4.inv() * gen * L4.inv())
                    dR = (dP + hinv * dP * hinv) / 2
                    bend = sp.Matrix([(dR * ETA)[a, b] for a, b in PAIRS])
                    raw = sign * (Bb.T * G2 * STAR * bend)[0]
                    lin = sp.series(sp.expand(raw), sval, 0, 2).removeO().coeff(sval, 1)
                    if lin != 0:
                        local[ph][6 * role + g] += lin
    acc = sp.zeros(24, 1)
    for phase in range(4):
        acc += sp.conjugate(chi(phase)) * local[phase]
    return sp.simplify(acc)

sval = sp.symbols("s")
print("building Hessians", flush=True)
Hi = sp.Matrix.hstack(*[series_column(r, g, lambda ph: sp.I ** ph) for r in range(4) for g in range(6)])
Hm = sp.Matrix.hstack(*[series_column(r, g, lambda ph: (-1) ** ph) for r in range(4) for g in range(6)])
check("CHAR_I_RANK_20", Hi.rank() == 20)
check("CHAR_MINUS_RANK_24", Hm.rank() == 24)
check("K_IN_KERNEL", sp.simplify(Hi * KVEC) == sp.zeros(24, 1))
p2_ref = sp.Matrix([0, -4, -4, 4, 4, 0] * 4)
check("P2_NORMALIZATION", sp.simplify(Hm * p2_ref + 4 * real_fa) == sp.zeros(24, 1))

def metric_mode(vec):
    Y = pack(vec)
    local = {phase: sp.zeros(10, 1) for phase in range(4)}
    legs = [I4[:, i] for i in range(4)]
    SYM = [(a, b) for a in range(4) for b in range(a, 4)]
    for base in range(4):
        for r, sf in PAIRS:
            specs = [(base, r, 1), (shift(base, r), sf, 1), (shift(base, sf), r, -1), (base, sf, -1)]
            dR = Z4
            for ph, role, sign_c in specs:
                dR += sign_c * (sp.I ** ph) * Y[role]
            bend = sp.Matrix([sp.expand((dR * ETA)[a, b]) for a, b in PAIRS])
            u, v = [i for i in range(4) if i not in (r, sf)]
            sign = orient((r, sf))
            for nslot, (a, b) in enumerate(SYM):
                direction = sp.zeros(4)
                direction[a, b] = direction[b, a] = 1
                variation = direction * ETA / 2
                dw = wedge(variation[u, :].T, legs[v]) + wedge(legs[u], variation[v, :].T)
                local[base][nslot] += sign * (dw.T * G2 * STAR * bend)[0]
    acc = sp.zeros(10, 1)
    for phase in range(4):
        acc += ((-sp.I) ** phase) * local[phase]
    return sp.simplify(acc)

check("SILENT_RAY_METRIC_ZERO", metric_mode(KVEC) == sp.zeros(10, 1))
basis = Hi.nullspace()
check("KERNEL_DIM_4", len(basis) == 4)
metric_cols = [metric_mode(v) for v in basis]
metric_map = sp.Matrix.hstack(*metric_cols)
check("METRIC_RANK_ON_KERNEL_3", metric_map.rank() == 3)
silent = metric_map.nullspace()
check("SILENT_LINE_DIM_1", len(silent) == 1)
recon = sum((sp.simplify(silent[0][i]) * basis[i] for i in range(4)), sp.zeros(24, 1))
# The exhibited vector and this reconstructed line are the same complex line.
minors_ok = True
for i in range(24):
    for j in range(i + 1, 24):
        if sp.expand(recon[i] * KVEC[j] - recon[j] * KVEC[i]) != 0:
            minors_ok = False
            break
    if not minors_ok:
        break
check("SILENT_LINE_IS_EXHIBITED_VECTOR", minors_ok and sp.simplify(recon) != sp.zeros(24, 1))

left = Hi.T.nullspace()
check("LEFT_KERNEL_DIM_4", len(left) == 4)

def pairing_vector(force):
    return sp.Matrix([sp.simplify((v.T * force)[0]) for v in left])

samples = {}
for t in (0, 1, -1, 2):
    print("sample", t, flush=True)
    bare_t = euler_orders(t, None)
    f2 = fourier(bare_t, 2, 2)
    p2 = sp.simplify(Hm.solve(-f2))
    full = euler_orders(t, p2)
    check("ORDER2_CLEARED_%s" % t, sp.simplify(fourier(full, 2, 2)) == sp.zeros(24, 1))
    samples[t] = pairing_vector(fourier(full, 1, 3))

tt = sp.symbols("tt")
# Two independent pairings. The sampled left kernel makes components (0,1) equal and (2,3) opposite.
pi_a = (-64 - 64 * sp.I) + 128 * sp.I * tt + (32 + 16 * sp.I) * tt ** 2 + (8 + 20 * sp.I) * tt ** 3
pi_b = (4 + 4 * sp.I) * tt * (tt ** 2 + tt + 4 * sp.I)
for t, got in samples.items():
    check("SAMPLE_%s_A" % t, sp.expand(got[0] - pi_a.subs(tt, t)) == 0 and sp.expand(got[1] - got[0]) == 0)
    check("SAMPLE_%s_B" % t, sp.expand(got[2] - pi_b.subs(tt, t)) == 0 and sp.expand(got[3] + got[2]) == 0)

x = sp.symbols("x", real=True)
quad = x ** 2 + x + 4 * sp.I
check("QUADRATIC_FACTOR_NEVER_REAL_ZERO", sp.im(sp.expand(quad)) == 4)
check("ONLY_REAL_ZERO_OF_SECOND_PAIRING_IS_ZERO", sp.expand(pi_b.subs(tt, 0)) == 0)
check("FIRST_PAIRING_NONZERO_AT_ZERO", sp.expand(pi_a.subs(tt, 0)) != 0)

if FAILS:
    print("A4D-Q0-SILENT-KERNEL-RAY-ORDER3-OBSTRUCTION: FAIL (%d)" % len(FAILS))
    for name in FAILS:
        print("  - " + name)
    raise SystemExit(1)
print("A4D-Q0-SILENT-KERNEL-RAY-ORDER3-OBSTRUCTION")
print("The unique metric-silent order-eps kernel line does not put the order-eps^3 forcing in the connection image for any real scale.")
