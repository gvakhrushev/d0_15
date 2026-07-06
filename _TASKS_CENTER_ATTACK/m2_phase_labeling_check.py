#!/usr/bin/env python3
"""m2_phase_labeling_check.py — companion for M2_PHASE_LABELING_MEMO.md (DRAFT, pre-skeptic).

M2-FORGING: what within-zone labeling of K(9,11,13) does OWNED scene structure force?
Computes (exact where load-bearing):
  S1  Q8 exact algebra: exponent 4 (no Z/8), Aut=24, Inn=V4, typed-pair-preserving = Inn.
  S2  G_res under three owned-reading models: R-strong=1, R-mid=V4(4), R-weak=(Z/2)^3(8);
      admissible Q8-labelings form ONE G_res-orbit (torsor) in each reading = "forced up to G_res".
  S3  mu9-labeling impossibility, quantified: no owned cyclic relation; 8! = 40320 orders;
      classes = 40320/|G_res| >= 5040 vs exactly 1 class for the Q8-labeling.
  S4  canonical function-system on V9: C^9 = C.omega0 (+) E0 (+) E3 (+) E4 (1+1+3+4),
      G_res-invariant blocks; refines the S9-irreducible std9 (8-dim) into 1+3+4.
  S5  33x33 tick consumer audit: owned +/-1 carriers (chi_B, chi_C, chi_D, act/undo s) fire with
      EXACT rational data ||PUQ||_F^2 = 80/81, ladder ratio -1/9, delay weight 8/9;
      the fully-canonical central-flip permutation L_z is VACUOUS (PUQ=0);
      global rho(QUQ)=1 for identity-padded carriers but the eigenvalue-1 directions are
      DECOUPLED from the ladder (exact 1-dim invariant ladder subspace);
      comparators: Phi9 (mu9 zone-9, un-owned), U3=diag(mu9;mu11;mu13) (reproduces (QUQ)^12=0).
  S6  torsor-invariance: tick quantities invariant under G_res and under random S9xS11xS13
      relabelings; NEGATIVE demo: per-slot values are NOT invariant (M2-membership gap).
  S7  negative controls (each can fail the CONCLUSION, not the technique).
NOT a minted cert. No registry row edited.
"""
import itertools
import sys
from fractions import Fraction

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
TOL = 1e-10
PASS = []
# macOS Accelerate BLAS emits SPURIOUS divide/overflow/invalid FP flags on complex matmul
# (values are correct). We silence the bogus warnings and instead enforce REAL finiteness
# assertions on every computed tick quantity (see tick_data) — the guard is the assert, not
# the warning.
np.seterr(divide="ignore", over="ignore", invalid="ignore")


def report(name, cond, detail=""):
    PASS.append((name, bool(cond)))
    print(("PASS_" if cond else "FAIL_") + name + ("  " + detail if detail else ""))
    assert cond, name


# ---------------------------------------------------------------- S1: exact Q8
# element = (s, u), s in {+1,-1}, u in '1ijk'
UNITS = "1ijk"
MUL = {  # unit*unit -> (sign, unit); Hamilton table (recorded corpus convention, SS01.7.1A/C)
    ("1", "1"): (1, "1"), ("1", "i"): (1, "i"), ("1", "j"): (1, "j"), ("1", "k"): (1, "k"),
    ("i", "1"): (1, "i"), ("j", "1"): (1, "j"), ("k", "1"): (1, "k"),
    ("i", "i"): (-1, "1"), ("j", "j"): (-1, "1"), ("k", "k"): (-1, "1"),
    ("i", "j"): (1, "k"), ("j", "i"): (-1, "k"),
    ("j", "k"): (1, "i"), ("k", "j"): (-1, "i"),
    ("k", "i"): (1, "j"), ("i", "k"): (-1, "j"),
}
Q8 = [(s, u) for u in UNITS for s in (1, -1)]


def mul(a, b):
    s, u = MUL[(a[1], b[1])]
    return (a[0] * b[0] * s, u)


def order(x):
    e, y, n = (1, "1"), x, 1
    while y != e:
        y, n = mul(y, x), n + 1
    return n


ident = (1, "1")
zC = (-1, "1")  # the unique order-2 element = center's nontrivial element = A-
report("Q8_TABLE_GROUP", all(mul(a, mul(b, c)) == mul(mul(a, b), c)
                             for a in Q8 for b in Q8 for c in Q8), "associativity, 512 triples exact")
orders = sorted(order(x) for x in Q8)
report("Q8_EXPONENT_4_NO_Z8", orders == [1, 2, 4, 4, 4, 4, 4, 4] and max(orders) == 4,
       f"element orders {orders}: NO order-8 element -> Omega8 carries no owned Z/8 cyclic structure")
report("Q8_UNIQUE_ORDER2_IS_CENTER", [x for x in Q8 if order(x) == 2] == [zC],
       "z=-1 definable from ANY table (unique involution) => A- pinned in every reading")

# Aut(Q8) by brute force: an automorphism is determined by (alpha(i), alpha(j))
AUTS = []
ord4 = [x for x in Q8 if order(x) == 4]
for ai in ord4:
    for aj in ord4:
        if aj in (ai, mul(ai, ai), mul(mul(ai, ai), ai), ident):
            continue
        # build map on generators, extend, check homomorphism
        m = {(1, "i"): ai, (1, "j"): aj}
        m[(1, "k")] = mul(ai, aj)
        m[(-1, "i")] = mul(zC, ai)
        m[(-1, "j")] = mul(zC, aj)
        m[(-1, "k")] = mul(zC, m[(1, "k")])
        m[ident] = ident
        m[zC] = zC
        if len(set(m.values())) == 8 and all(m[mul(a, b)] == mul(m[a], m[b]) for a in Q8 for b in Q8):
            AUTS.append(tuple(sorted(m.items())))
AUTS = [dict(a) for a in set(AUTS)]
report("AUT_Q8_ORDER_24", len(AUTS) == 24, "Aut(Q8) ~ S4, enumerated exactly")
INN = []
for g in Q8:
    ginv = next(x for x in Q8 if mul(g, x) == ident)
    cg = {x: mul(mul(g, x), ginv) for x in Q8}
    if cg not in INN:
        INN.append(cg)
report("INN_Q8_IS_V4", len(INN) == 4 and all(all(c[c[x]] == x for x in Q8) for c in INN),
       "Inn(Q8) ~ Z2xZ2 (order 4, all involutions): Hamiltonian => inner autos fix every axis setwise")
axes = {u: {(1, u), (-1, u)} for u in "ijk"}
pairfix = [a for a in AUTS if all({a[x] for x in axes[u]} == axes[u] for u in "ijk")]
report("PAIR_PRESERVING_AUTS_EQ_INN", len(pairfix) == 4 and all(p in INN for p in pairfix),
       "typed roles B,C,D kill Out(Q8)=S3: axis-fixing automorphisms = Inn = V4 exactly")
sectfix = [a for a in pairfix if all(a[(1, u)] == (1, u) for u in "ijk")]
report("SECTION_PRESERVING_AUTS_TRIVIAL", len(sectfix) == 1,
       "act/undo section {1,i,j,k} pinned per pair => only the identity relabeling survives")

# ------------------------------------------------- S2: G_res + labeling torsor
# V9 = [omega0, A+, A-, B+, B-, C+, C-, D+, D-]; owned data models:
#  R-strong: basepoint + typed pairs + group law (recorded table) + act/undo sign section per pair
#  R-mid   : basepoint + typed pairs + group law (recorded table)      [no per-pair sign section]
#  R-weak  : basepoint + typed pairs + group-iso-CLASS only            [table only up to iso]
# admissible labeling = bijection f: Omega8 -> Q8 with f(A+)=1, f(A-)=z (pinned: unique involution
# + recorded U_A=Id), f({X+,X-}) = the typed axis pair (typed naming B->i,C->j,D->k held fixed:
# Out-part is NAMING per T2_PRIME_FINAL_STATE.md correction "axis = Out(Q8) gauge").
ROLE = {"B": "i", "C": "j", "D": "k"}
sections = list(itertools.product((1, -1), repeat=3))  # sign of f(X+) on axes i,j,k
std = {"B+": (1, "i"), "B-": (-1, "i"), "C+": (1, "j"), "C-": (-1, "j"),
       "D+": (1, "k"), "D-": (-1, "k"), "A+": ident, "A-": zC}


def labeling(sig):
    f = {"A+": ident, "A-": zC}
    for (X, u), s in zip(ROLE.items(), sig):
        f[X + "+"] = (s, u)
        f[X + "-"] = (-s, u)
    return f


def is_iso(f):
    # transported law: f is iso from (Omega8, recorded std law) to (Q8, law)
    inv = {v: k for k, v in std.items()}
    return all(f[inv[mul(std[a], std[b])]] == mul(f[a], f[b]) for a in std for b in std)


lab_weak = [labeling(s) for s in sections]                       # pairs+basepoint only
lab_mid = [f for f in lab_weak if is_iso(f)]                      # + recorded table
lab_strong = [f for f in lab_mid if all(f[X + "+"][0] == 1 for X in ROLE)]  # + act section
report("LABELING_COUNTS_8_4_1", (len(lab_weak), len(lab_mid), len(lab_strong)) == (8, 4, 1),
       "admissible Q8-labelings: R-weak 8, R-mid 4, R-strong 1")
# G_res = stabilizer/deck group; torsor check: labelings in each reading form ONE orbit under
# the corresponding relabeling group acting by postcomposition with pair-preserving maps.
even = [s for s in sections if s[0] * s[1] * s[2] == 1]
report("R_MID_IS_EVEN_FLIPS_V4", [tuple(f[X + "+"][0] for X in ROLE) for f in lab_mid] ==
       even or set(tuple(f[X + "+"][0] for X in ROLE) for f in lab_mid) == set(even),
       "R-mid labelings = even sign sections (ijk=-1 preserved) <-> Inn(Q8)=V4 torsor")
tp = {}
for f in lab_weak:
    prod = mul(mul(f["B+"], f["C+"]), f["D+"])
    tp[tuple(f[X + "+"][0] for X in ROLE)] = prod
report("TRIPLE_PRODUCT_CHI_SEPARATES", all((tp[s] == zC) == (s[0] * s[1] * s[2] == 1) for s in sections),
       "chi = actB.actC.actD in {+1,-1}: -1 on even sections (Hamilton ijk=-1), +1 on odd; "
       "gauge-invariant detector of the R-weak/R-mid gap")
GRES = {"R-strong": 1, "R-mid": 4, "R-weak": 8}
for r, n in GRES.items():
    k = {"R-strong": len(lab_strong), "R-mid": len(lab_mid), "R-weak": len(lab_weak)}[r]
    report(f"TORSOR_{r.replace('-', '_')}", k == n and k // n == 1,
           f"{k} labelings / |G_res|={n} = 1 orbit: labeling FORCED up to G_res ({r})")

# ---------------------------------------------- S3: mu9 impossibility, quantified
# a mu9-labeling is a bijection V9 -> mu9 (9th roots of unity), basepoint omega0 -> 1.
# owned relations contain NO cyclic-successor relation (S1: no order-8/9 element; role data is
# a typed partition, not an order; SS01.24 circulation is continuous + emission G8-averaged).
n_mu9 = 40320  # 8! bijections Omega8 -> {zeta^1..zeta^8}
classes = {r: Fraction(n_mu9, n) for r, n in GRES.items()}
report("MU9_FREEDOM_QUANTIFIED",
       classes["R-strong"] == 40320 and classes["R-mid"] == 10080 and classes["R-weak"] == 5040,
       "mu9-labeling owned-equivalence classes: 40320 / 10080 / 5040 (vs Q8-labeling: exactly 1) "
       "-- no owned selector exists among them")
# orbit obstruction (free-action argument, EXERCISED not asserted): for |G_res|>1, no bijection
# f: Omega8 -> mu9\{1} satisfies f∘g = f for a nontrivial relabeling g (f injective, g moves a
# point => f(g(x)) != f(x)). Exercise: all 7 nontrivial flip relabelings x 500 random bijections.
OM8 = ["A+", "A-", "B+", "B-", "C+", "C-", "D+", "D-"]
flip_perms = []
for sig in itertools.product((0, 1), repeat=3):
    if sig == (0, 0, 0):
        continue
    g = {x: x for x in OM8}
    for X, s in zip("BCD", sig):
        if s:
            g[X + "+"], g[X + "-"] = X + "-", X + "+"
    flip_perms.append(g)
rng0 = np.random.default_rng(20260705)
violated = 0
for g in flip_perms:
    assert any(g[x] != x for x in OM8), "control premise: nontrivial g must move a point"
    for _ in range(500):
        perm = rng0.permutation(8)
        f = {x: int(perm[i]) for i, x in enumerate(OM8)}  # bijection Omega8 -> 8 phase slots
        if all(f[g[x]] == f[x] for x in OM8):
            violated += 1
report("MU9_NO_INVARIANT_BIJECTION", len(flip_perms) == 7 and violated == 0,
       "free action exercised: 7 nontrivial relabelings x 500 random bijections, ZERO invariant "
       "bijections found (and none can exist: f injective + g moves a pair) => under R-mid/R-weak "
       "a canonical per-vertex phase bijection cannot even be stated")

# --------------------------------- S4: canonical function system on V9 (1+1+3+4)
# index order: 0=omega0, 1..8 = A+,A-,B+,B-,C+,C-,D+,D- (recorded standard labeling)
V9N = ["omega0", "A+", "A-", "B+", "B-", "C+", "C-", "D+", "D-"]
q_of = {i: std[V9N[i]] for i in range(1, 9)}
def chi(u):  # linear character with kernel <u>
    def c(x):
        return 1.0 if x[1] in ("1", u) else -1.0
    return c
chiB, chiC, chiD = chi("i"), chi("j"), chi("k")
e_om = np.zeros(9); e_om[0] = 1.0
triv = np.zeros(9); triv[1:] = 1.0 / np.sqrt(8)          # E0 in C[Q8]
vB = np.array([0.0] + [chiB(q_of[i]) for i in range(1, 9)]) / np.sqrt(8)
vC = np.array([0.0] + [chiC(q_of[i]) for i in range(1, 9)]) / np.sqrt(8)
vD = np.array([0.0] + [chiD(q_of[i]) for i in range(1, 9)]) / np.sqrt(8)
E3 = np.stack([vB, vC, vD])
# E4 = odd part under central flip z (f(zx) = -f(x)); z-flip permutation swaps X+ <-> X-
zperm = [0, 2, 1, 4, 3, 6, 5, 8, 7]
Lz = np.zeros((9, 9))
for a, b in enumerate(zperm):
    Lz[b, a] = 1.0
E4 = []
for p in (1, 3, 5, 7):
    v = np.zeros(9); v[p], v[p + 1] = 1 / np.sqrt(2), -1 / np.sqrt(2)
    E4.append(v)
E4 = np.stack(E4)
blocks = [np.stack([e_om]), np.stack([triv]), E3, E4]
Gram = np.vstack([b for b in blocks])
report("V9_DECOMP_1_1_3_4", Gram.shape == (9, 9) and np.allclose(Gram @ Gram.T, np.eye(9), atol=TOL),
       "C^9 = C.omega0 (+) E0 (+) E3 (+) E4 orthonormal, dims 1+1+3+4")
# G_res-invariance of the blocks under the LARGEST freedom (R-weak (Z/2)^3 pair flips):
flips = []
for sig in itertools.product((0, 1), repeat=3):
    p = list(range(9))
    for bidx, s in zip((3, 5, 7), sig):
        if s:
            p[bidx], p[bidx + 1] = p[bidx + 1], p[bidx]
    M = np.zeros((9, 9))
    for a, b in enumerate(p):
        M[b, a] = 1.0
    flips.append(M)
ok = True
for M in flips:
    for b in blocks:
        Pb = b.T @ b
        ok &= np.allclose(M @ Pb @ M.T, Pb, atol=TOL)
report("BLOCKS_GRES_INVARIANT", ok,
       "all four block projectors invariant under the full (Z/2)^3 flip group (a fortiori V4): "
       "the 1+1+3+4 decomposition is reading-independent canonical")
report("E3_POINTWISE_FLIP_INVARIANT", all(np.allclose(M @ v, v, atol=TOL) for M in flips for v in E3),
       "characters chi_B,chi_C,chi_D are pointwise G_res-invariant (chi(-x)=chi(x))")
# std9 refinement: sum-zero space on 9 points (S9-irreducible, dim 8) = contrast (+) E3 (+) E4
contrast = np.zeros(9); contrast[0] = np.sqrt(8.0 / 9.0); contrast[1:] = -1 / np.sqrt(72)
sub = np.vstack([np.stack([contrast]), E3, E4])
report("STD9_REFINES_1_3_4", np.allclose(sub @ np.ones(9), 0, atol=TOL) and
       np.allclose(sub @ sub.T, np.eye(8), atol=TOL),
       "the labeling refines the graph-irreducible std9 (8-dim) into canonical 1+3+4 -- structure "
       "the bare graph cannot define (R1 no-go context)")

# ------------------------------------------------- S5: 33x33 tick consumer audit
sizes = [9, 11, 13]
N = 33
zone = sum(([i] * s for i, s in enumerate(sizes)), [])
A = np.array([[1.0 if zone[i] != zone[j] else 0.0 for j in range(N)] for i in range(N)])
w, V = np.linalg.eigh(A)
K = V[:, np.abs(w) < 1e-9]
Q = K @ K.T
P = np.eye(N) - Q
report("SPLIT_3_30", round(np.trace(P)) == 3 and round(np.trace(Q)) == 30, "frozen Feshbach split")


def zone9_diag(d9, pad=1.0):
    d = np.array(list(d9) + [pad] * 24, dtype=complex)
    return np.diag(d)


def tick_data(U, kmax=40):
    PUQ = P @ U @ Q
    QUQ = Q @ U @ Q
    QUP = Q @ U @ P
    fire = np.linalg.norm(PUQ)
    rho_g = max(abs(np.linalg.eigvals(QUQ)))
    # ladder-relevant data: term_k = PUQ (QUQ)^k QUP
    terms, T = [], PUQ.copy()
    for k in range(kmax):
        terms.append(np.linalg.norm(T @ QUP))
        T = T @ QUQ
    assert np.isfinite(fire) and np.isfinite(rho_g) and all(np.isfinite(t) for t in terms), \
        "non-finite tick data (real overflow, not the spurious Accelerate flag)"
    return fire, rho_g, terms


# owned carriers: +/-1 diagonals on zone 9 from the canonical label system
d_chiB = [1.0] + [chiB(q_of[i]) for i in range(1, 9)]
d_chiC = [1.0] + [chiC(q_of[i]) for i in range(1, 9)]
d_chiD = [1.0] + [chiD(q_of[i]) for i in range(1, 9)]
d_sect = [1.0] + [q_of[i][0] * 1.0 for i in range(1, 9)]  # act/undo sign (R-strong only)
owned = {"chi_B": d_chiB, "chi_C": d_chiC, "chi_D": d_chiD, "act_undo_s": d_sect}
# FRACTION-EXACT closed form (skeptic #1 repair; floats demoted to corroboration).
# For a zone-9 +/-1 diagonal with integer entries d (p entries +1, q entries -1, s = p - q):
#   ||PUQ||_F^2 = ||P9 D||_F^2 - ||P9 D P9||_F^2 = (sum d^2)/9 - s^2/81 = (81 - s^2)/81 in Q;
#   the ladder lives on the 1-dim space w ⊥ u inside span{u_+, u_-} with EXACT Rayleigh ratio
#   <w, QDQ w> = (q - p)/9; delay weight at z=1 = ||PUQ||_F^2 / (1 - ratio).
f2 = Fraction(80, 81)
ratio = Fraction(-1, 9)
delay = Fraction(8, 9)
for name, d in owned.items():
    di = [int(round(x)) for x in d]
    p_, q_ = di.count(1), di.count(-1)
    s_ = sum(di)
    F2x = Fraction(81 - s_ * s_, 81)
    RATx = Fraction(q_ - p_, 9)
    DELx = F2x / (1 - RATx)
    report(f"OWNED_{name}_EXACT_Q", (p_, q_) == (5, 4) and F2x == f2 and RATx == ratio and DELx == delay,
           f"Fraction-exact: split ({p_},{q_}), ||PUQ||_F^2 = {F2x} = 80/81, ratio = {RATx} = -1/9, "
           f"delay weight = {DELx} = 8/9 (all equalities in Q, no floats)")
    U = zone9_diag(d)
    fire, rho_g, terms = tick_data(U)
    report(f"OWNED_{name}_FIRES_FLOAT_MATCHES_Q", abs(fire**2 - float(F2x)) < 1e-9,
           f"numpy ||PUQ||_F^2 = {fire**2:.12f} matches the exact 80/81; carrier unitary, real, "
           "OWNED-label-built")
    g = [terms[k + 1] / terms[k] for k in range(3)]
    # signed Rayleigh check: x = QUP(zone-9 uniform) spans the ladder line; sign must match (q-p)/9
    u9 = np.zeros(N); u9[:9] = 1.0 / 3.0
    x = Q @ U @ P @ u9
    ray = float(np.real(x @ (Q @ U @ Q) @ x) / (x @ x))
    report(f"OWNED_{name}_LADDER_GEOMETRIC", all(abs(v - 1.0 / 9.0) < 1e-9 for v in g) and
           abs(ray - float(RATx)) < 1e-9,
           f"|term ratio| = 1/9 exact AND signed Rayleigh ratio {ray:.9f} = (q-p)/9 = {RATx}: "
           "convergent geometric ladder, closed-form in Q")
    report(f"OWNED_{name}_RHO_GLOBAL_1_DECOUPLED", abs(rho_g - 1.0) < 1e-9,
           "global rho(QUQ)=1 (untouched zones + in-zone eigendirections) but ladder support is the "
           "EXACT 1-dim contraction above; delay weight = F2/(1-ratio) = 8/9 in Q")
U_s = zone9_diag(d_sect)
U_c = zone9_diag(d_chiB)
report("OWNED_CARRIERS_SAME_FINGERPRINT",
       abs(tick_data(U_s)[0] - tick_data(U_c)[0]) < 1e-12,
       "all owned +/-1 carriers (5/4 split) share ONE exact rational tick fingerprint "
       "{80/81, -1/9, 8/9} -- a canonical, reading-independent class invariant")
# the omega0-extension bit (MY connective, not owned): chi(omega0) := -1 gives the 4/5 split.
# ||PUQ||_F^2 = (81 - s^2)/81 with s = sum(d): |s| = 1 either way -> 80/81 INVARIANT;
# the ladder ratio flips sign (-1/9 -> +1/9), so the z=1 delay weight moves 8/9 -> 10/9.
d_neg = [-1.0] + d_chiB[1:]
dni = [int(round(x)) for x in d_neg]
pn, qn, sn = dni.count(1), dni.count(-1), sum(dni)
F2n = Fraction(81 - sn * sn, 81)
RATn = Fraction(qn - pn, 9)
DELn = F2n / (1 - RATn)
fire_n, _, terms_n = tick_data(zone9_diag(d_neg))
gn = [terms_n[k + 1] / terms_n[k] for k in range(3)]
u9 = np.zeros(N); u9[:9] = 1.0 / 3.0
Un = zone9_diag(d_neg)
xn = Q @ Un @ P @ u9
rayn = float(np.real(xn @ (Q @ Un @ Q) @ xn) / (xn @ xn))
report("OMEGA0_EXTENSION_BIT_NAMED",
       F2n == Fraction(80, 81) and RATn == Fraction(1, 9) and DELn == Fraction(10, 9) and
       abs(fire_n**2 - float(F2n)) < 1e-9 and all(abs(x - 1.0 / 9.0) < 1e-9 for x in gn) and
       abs(rayn - float(RATn)) < 1e-9,
       f"chi(omega0)=-1 variant, Fraction-exact: split ({pn},{qn}), ||PUQ||_F^2 = {F2n} UNCHANGED, "
       f"ratio = {RATn} = +1/9 (SIGN flipped, Rayleigh {rayn:.9f} confirms), delay weight = {DELn} "
       "= 10/9 vs 8/9: the omega0-extension is a NAMED residual bit of the carrier construction, "
       "not owned -- invariant fingerprint is {80/81, |1/9|}")
# the fully-canonical PERMUTATION carrier: central flip L_z on zone 9
Uz = np.zeros((N, N)); Uz[:9, :9] = Lz; Uz[9:, 9:] = np.eye(24)
fire_z, rho_z, _ = tick_data(Uz)
report("CENTRAL_FLIP_VACUOUS", fire_z < TOL,
       "L_z (the owned Z2 register as an operator) is a graph automorphism => PUQ=0: the deepest-"
       "owned carrier CANNOT fire the tick; firing requires the diagonal (label-VALUE) grade")
# comparators (un-owned mu-lattices / cyclic order)
mu9 = [np.exp(2j * np.pi * v / 9) for v in range(9)]
Phi9_id = zone9_diag(mu9)                     # identity-padded (unitary)
Phi9_z0 = zone9_diag(mu9, pad=0.0)            # zero-padded (as a zone-9-only block object)
fire9, rho9_id, terms9 = tick_data(Phi9_id)
rho9_block = max(abs(np.linalg.eigvals((Q @ Phi9_z0 @ Q)[:9, :9])))
g9 = [terms9[k + 1] / terms9[k] for k in range(6)]
print(f"INFO_PHI9  ||PUQ||_F={fire9:.6f}; rho(QPhi9Q) zone-9 block={rho9_block:.6f} "
      f"(cos(pi/9)={np.cos(np.pi/9):.6f}); global(id-pad)={rho9_id:.6f}; "
      f"ladder ratios k=0..5: {[f'{x:.4f}' for x in g9]} (NOT geometric, unlike owned carriers)")
report("PHI9_FIRES", fire9 > 0.9, "un-owned mu9 comparator also fires (firing is NOT what "
       "distinguishes owned from un-owned; the LABEL VALUES are)")
# real form of the (un-owned) cyclic order: the 9-cycle shift C9, symmetrized (C+C^T)/2.
C9 = np.zeros((9, 9))
for v in range(9):
    C9[(v + 1) % 9, v] = 1.0
Sym9 = (C9 + C9.T) / 2.0
USym = np.zeros((N, N)); USym[:9, :9] = Sym9  # zero-padded zone-9 block object
rho_real = max(abs(np.linalg.eigvals((Q @ USym @ Q)[:9, :9])))
report("PHI9_REAL_FORM_COS_PI_9", abs(rho_real - np.cos(np.pi / 9)) < 1e-9,
       f"real/symmetric form of the 9-cycle: rho(QUQ) zone-9 block = cos(pi/9) = {rho_real:.9f} "
       "EXACT (= max|cos(2*pi*k/9)|, k=1..8, at k=4) -- reproduces the Feshbach-track input; "
       "the 9-cycle order behind it is exactly the UN-OWNED datum (S3)")
d = []
for n in sizes:
    d += [np.exp(2j * np.pi * v / n) for v in range(n)]
U3 = np.diag(np.array(d))
QU3Q = Q @ U3 @ Q
report("U3_NILPOTENT_12_REPRODUCED",
       np.linalg.norm(np.linalg.matrix_power(QU3Q, 12)) < 1e-8 and
       abs(np.linalg.norm(P @ U3 @ Q) - np.sqrt(3)) < 1e-9,
       "tri-phase comparator: (QUQ)^12=0 exact, ||PUQ||_F=sqrt(3) (tick memo v2 reproduced)")

# ------------------------------------- S6: torsor-invariance vs per-slot values
rng = np.random.default_rng(20260705)
base_fire, _, base_terms = tick_data(U_c)
inv_ok, slot_moved = True, False
for _ in range(20):
    perm = np.arange(N)
    perm[:9] = rng.permutation(9)
    perm[9:20] = 9 + rng.permutation(11)
    perm[20:] = 20 + rng.permutation(13)
    Pi = np.zeros((N, N), dtype=complex)
    for a, b in enumerate(perm):
        Pi[b, a] = 1.0
    Uc_rel = Pi @ U_c @ Pi.conj().T
    f_r, _, t_r = tick_data(Uc_rel, kmax=5)
    assert np.isfinite(f_r) and all(np.isfinite(x) for x in t_r), "non-finite tick data"
    inv_ok &= abs(f_r - base_fire) < 1e-9 and abs(t_r[1] / t_r[0] - 1.0 / 9.0) < 1e-9
    slot_moved |= abs((Uc_rel - U_c)[3, 3]) > 0.5
report("TICK_DATA_TORSOR_INVARIANT", inv_ok,
       "||PUQ||, ladder ratio invariant under 20 random within-zone relabelings: tick consumers "
       "are CLASS functions -- they never needed the graph-bridge resolved")
report("PER_SLOT_VALUES_NOT_INVARIANT", slot_moved,
       "the per-slot diagonal VALUE at a fixed vertex index moves under relabeling: M2-membership "
       "consumers are NOT class functions -- they need the bridge the scene does not own")
# graph-side no-go demo: the exact S9xS11xS13-orbit-average of ANY vertex functional is the
# zone mean (transitivity within zones), hence zone-CONSTANT: no graph-definable per-vertex label.
dr = rng.normal(size=N)
orbit_avg = np.concatenate([np.full(9, dr[:9].mean()),
                            np.full(11, dr[9:20].mean()),
                            np.full(13, dr[20:].mean())])
# EXACT average over the transitive cyclic subgroup Z/9 x Z/11 x Z/13 < S9 x S11 x S13
# (transitivity within each zone suffices; the cyclic average IS the zone mean, deterministically)
cyc = np.zeros(N)
for t9 in range(9):
    cyc[:9] += np.roll(dr[:9], t9) / 9.0
for t11 in range(11):
    cyc[9:20] += np.roll(dr[9:20], t11) / 11.0
for t13 in range(13):
    cyc[20:] += np.roll(dr[20:], t13) / 13.0
report("GRAPH_DEFINABLE_IS_ZONE_CONSTANT", np.allclose(cyc, orbit_avg, atol=TOL),
       "exact average over a transitive within-zone subgroup = zone mean: any Aut-invariant "
       "(graph-definable) vertex functional is zone-constant => NO graph-side within-zone labeling "
       "(C1 + within-zone transitivity, computed)")

# ------------------------------------------------------- S7: negative controls
# (a) exponent control: if Q8 had an order-8 element the mu9-impossibility would collapse.
report("CTRL_NO_ORDER8", not any(order(x) == 8 for x in Q8),
       "an order-8 element would refute the no-cyclic-structure conclusion; none exists (exact)")
# (b) zone-11 basepoint control: the owned-vocabulary model for zone 11/13 is EMPTY; a claimed
#     zone-11 basepoint would have to be Aut-invariant, but Aut is transitive within the zone.
stab_orbit = {tuple(sorted({(9 + (v + t) % 11) for t in range(11)})) for v in range(11)}
report("CTRL_ZONE11_NO_BASEPOINT", stab_orbit == {tuple(range(9, 20))},
       "zone-11 vertices form ONE transitivity class; an owned basepoint there would fail this "
       "(this control fails the CONCLUSION if zones 11/13 secretly carried owned structure)")
# (c) single repeated phase destroys U3 nilpotency (boundary probe, tick memo v2)
d_bad = list(d)
d_bad[1] = d_bad[0]
U3b = np.diag(np.array(d_bad))
M12 = np.linalg.matrix_power(Q @ U3b @ Q, 12)
pw_f = np.linalg.norm(M12)                      # Frobenius (the != 0 witness)
pw_op = np.linalg.norm(M12, 2)                  # spectral (sanity: contraction power <= 1)
report("CTRL_REPEATED_PHASE_DESTROYS", np.isfinite(pw_f) and pw_f > 1e-6 and pw_op <= 1.0 + 1e-9,
       f"one repeated phase => ||(QUQ)^12||_F = {pw_f:.6f} != 0 (op-norm {pw_op:.6f} <= 1 sane): "
       "the FULL lattice is load-bearing (reproduced)")
# (d) wrong-G_res control, FROM SCRATCH (skeptic #1 repair: the old check tested a hardcoded
#     dict against itself). Enumerate ALL 8! = 40320 permutations of Omega8 and count, per
#     reading, those preserving the owned relations; the derived orders must equal the claimed
#     G_res orders AND independently reproduce the labeling counts of S2.
n_weak = n_mid = n_strong = 0
inv_std = {v: k for k, v in std.items()}
for perm8 in itertools.permutations(OM8):
    g = dict(zip(OM8, perm8))
    # R-weak relations: A+ and A- fixed (identity + unique involution), typed pairs setwise
    if g["A+"] != "A+" or g["A-"] != "A-":
        continue
    if any({g[X + "+"], g[X + "-"]} != {X + "+", X + "-"} for X in "BCD"):
        continue
    n_weak += 1
    # R-mid: additionally an automorphism of the recorded table
    if all(g[inv_std[mul(std[a], std[b])]] == inv_std[mul(std[g[a]], std[g[b]])]
           for a in OM8 for b in OM8):
        n_mid += 1
        # R-strong: additionally fixes the act section pointwise
        if all(g[X + "+"] == X + "+" for X in "BCD"):
            n_strong += 1
report("CTRL_GRES_ORDERS_FROM_SCRATCH",
       (n_weak, n_mid, n_strong) == (8, 4, 1) == (len(lab_weak), len(lab_mid), len(lab_strong)),
       f"independent 8!-sweep derives relabeling-group orders ({n_weak},{n_mid},{n_strong}) = "
       "(8,4,1), matching S2's labeling counts; a claimed order 3, 6, or 24-with-typing is "
       "refuted by this enumeration, not by assertion")
# (e) sanity: an OWNED carrier with a 6/3 +/-1 split would change the exact fingerprint;
#     verify the formula ||PUQ||_F^2 = (81-s^2)/81 discriminates (s=3 -> 72/81).
d63 = [1.0] * 6 + [-1.0] * 3
f63 = tick_data(zone9_diag(d63))[0] ** 2
report("CTRL_FINGERPRINT_DISCRIMINATES", abs(f63 - 72.0 / 81.0) < 1e-9 and abs(f63 - 80.0 / 81.0) > 1e-3,
       "a different split gives 72/81 != 80/81: the 80/81 value is a real consequence of the "
       "owned 5/4 label pattern, not of the technique")

print(f"\n{'=' * 70}")
print(f"ALL {len(PASS)} CHECKS PASS" if all(p for _, p in PASS) else "FAILURES PRESENT")
print("SUMMARY: labeling V9 -> Q8 u {omega0} FORCED up to G_res in {1, V4, (Z/2)^3} "
      "(reading UN-adjudicated; all three G_res readings computed as valid torsors, none selected); "
      "mu9/cyclic labeling IMPOSSIBLE from owned data (quantified "
      ">= 5040 unselectable classes); zones 11/13 own NOTHING per-vertex; owned +/-1 carriers "
      "fire the tick with exact rational fingerprint {80/81, -1/9, 8/9}; tick data is "
      "torsor-invariant, per-slot values are not; M2's Q(phi)\\Q per-slot invariant is NOT "
      "supplied (owned labels are rational-valued).")
