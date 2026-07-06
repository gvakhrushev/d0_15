#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
close_gap_e_owner_check.py — companion to CLOSE_GAP_E_OWNER_MEMO.md (10th pass, owner-route).

TWO LEGS:
  LEG 1 (invariant kill of X3 / z3=12 by OWNED parity):
    The owned parity clause (BOOK_01:1891-1909 + BOOK_03 §03.23.6 + SceneStepParity.lean row 522)
    bans parity-FLIPPING (= ODD) junction steps — the scope ALREADY adjudicated by three prior
    skeptic passes (DYAD-POWER OWN-4/EOR-2; COMPLETENESS F1/E-GE-2; window_forcing PARITY filter).
    An alphabet of ODD letter-count |X| makes an even-size zone 9+|X| in an odd tower — a parity
    flip under BOTH horns of the F3 fork, the ladder horn checked at both of its textual sites
    (consecutive B03:1049-56; nesting §03.23.7) and the over-base horn (:1551-53). Hence X3
    (|X|=3 -> z3=12), the nested chain (3) and the conjugacy-class partition (5 -> z=14) die on
    owned text AT ITS OPERATIVE GRADE — narrated CORE-FORCING + Lean-backed numerics (row 522),
    the same grade at which the corpus records "(9,11,15) is the parity-surviving escape". The
    NO-SKIP leg of row 522 (SceneStepParity.lean:18-20, docstring) is NOT used and NOT upgraded
    here — it stays the E-b missing clause. The memos 5-9's "z3=12 admissible under every clause
    the corpus owns" is an ERROR OF RECORD — mechanically exhibited (the 6th memo's misquote of
    the DYAD-POWER verdict; the campaign's own L0 tier already yielded "z3 odd >= 13").
  LEG 2 (uniqueness / which-one register — CANDIDATE, not owned):
    A two-co-admissible-candidates slot fork carries a which-one register (>=1 bit); for
    SIZE-forks the register is invariant-CHANGING (|V|, |E|, CAP=trace L, Laplacian spectrum —
    exact deltas computed here), hence NOT gauge (four-cell: not class C); same-size forks have
    ALL-ZERO deltas and are class-C/torsor territory (row 549) — the register argument must NOT
    fire on them (guard). theta-typing side-by-side with the OWNED Q8-normality precedent
    (BOOK_01:792) is computed (Q8 all-normal vs D4 non-normal conjugate-copy catalog).
    The pattern is REFUSED on: single-candidate underived presence (the KILLED 9th route) and on
    bridge-layer B-class rows (auto-close guard: n_s / CKM B-ext must stay open).

CAN-FAIL: every filter is built from independent objects (integer matrix powers, exact ranks over
Fraction, partition enumeration) — never from the conclusion. Negative controls can fail the
CONCLUSION: if parity killed z3=15 (even) the filter is over-strong (the +4 kill parity never
owned) -> rc=1; if z3=12 survived any owned reading -> rc=1; mutations MUT-A..MUT-E flip premises
and assert the conclusion MOVES.

rc semantics (family convention, cf. close_gap_e_meta_check.py):
  rc=1  any check failed (script or record broken)
  rc=2  ALL checks pass, uniqueness NOT granted: honest final state — Leg-1 kill VERIFIED-OWNED,
        window upper bound narrowed to {15,17}, still OPEN pending the owner sentence U
  rc=0  ALL checks pass AND --grant-uniqueness: demonstrates MUT-A sufficiency (U => z3<=13)
No registry row, cert, book or 053040 file is written. Read-only + stdout.
"""
import sys, os, math, itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GRANT_U = "--grant-uniqueness" in sys.argv

FAILS = []
NCHK = [0]
def check(name, cond, note=""):
    NCHK[0] += 1
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}" + (f" — {note}" if note else ""))
    if not cond:
        FAILS.append(name)

def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------------- QV: verbatim quote layer
print("=== QV — verbatim quote verification (owned pre-facts; failure = record broken) ===")
B01 = read("01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md")
B03 = read("01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md")
B00 = read("01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md")
LEAN = read("09_LEAN_FORMALIZATION/D0/Foundation/SceneStepParity.lean")
M5 = read("_TASKS_CENTER_ATTACK/CLOSE_GAP_E_MEMO.md")
M6 = read("_TASKS_CENTER_ATTACK/CLOSE_GAP_E_6TH_MEMO.md")
M7 = read("_TASKS_CENTER_ATTACK/RAISE_GAP_E_MINIMALITY_MEMO.md")
M9 = read("_TASKS_CENTER_ATTACK/CLOSE_GAP_E_META_MEMO.md")
DP = read("_TASKS_CENTER_ATTACK/GAP_E_DYAD_POWER_MEMO.md")
CC = read("_TASKS_CENTER_ATTACK/gap_e_completeness_check.py")

QUOTES = [  # (tag, blob-name, blob, exact substring)
 ("Q1 B01:1893 +2-never-+1 ban", "B01", B01,
  "the address ladder is forced to advance by `+2`, never `+1`, because a `+1` step would demand an external orientation bit"),
 ("Q2 B01:1903 flip=external bit", "B01", B01,
  "The orientation/torsion class flips, and to splice the two layers across that flip one must supply an external orientation bit"),
 ("Q3 B01:1903 +2 preserves", "B01", B01,
  "The step `5 → 7` preserves the orientation class, so the splice closes with no exogenous parameter"),
 ("Q4 B03 odd-step ban verbatim", "B03", B03,
  "A step `+1` (`5 -> 6`) flips the orientation/holonomy class; gluing the layers"),
 ("Q5 B03 exogenous Z2 bit", "B03", B03,
  "then needs an exogenous `Z_2` orientation bit not stored in the address"),
 ("Q6 B03 det machine-check", "B03", B03,
  "proved as `det(T^{n+2}) = det(T^n)` (with the `+1` flip"),
 ("Q7 Lean row 522 flip=catalog", "SceneStepParity.lean", LEAN,
  "A parity-*flipping* ladder would need a *second* independent"),
 ("Q8 B01:792 Q8-normality precedent", "B01", B01,
  "Telling those copies apart requires an external catalog of conjugates"),
 ("Q9 B01:1548 the LIST", "B01", B01,
  "the only primitive unresolved capacities over the pointed shell"),
 ("Q10 B00 DEF 0.3.1 clause-3 verbatim (clauses 1-2 quoted in memo P8, pinned by Q11/Q12 context)", "B00", B00,
  "it is **not an inevitable part of the distinguishability protocol**"),
 ("Q11 B00 M1 one-line (same outcome class)", "B00", B00,
  "If two constructions give the same class of distinguishable outcomes"),
 ("Q12 B00 blade cell (A) obligation", "B00", B00,
  "is contentful and *must* be derived/justified inside the corpus"),
 ("Q13 DYAD-POWER OWN-4 odd-iff scope", "DYAD_POWER", DP,
  "fires **iff the step flips the `ℤ₂` orientation class**, i.e. iff the step is **ODD**"),
 ("Q14 DYAD-POWER skeptic EOR-2 (even un-killed)", "DYAD_POWER", DP,
  "The even `+4`→V₁₅ escape is un-killed by parity"),
 ("Q15 completeness-check L0 residual odd>=13", "gap_e_completeness_check.py", CC,
  "L0+ residual family is exactly (9,11,z3), z3 odd >= 13"),
]
for tag, name, blob, s in QUOTES:
    check(tag, s in blob, f"substring present in {name}")

# ------------------------------------------------- LEG 1 / L1-1: det(T^n) computed exactly
print("\n=== LEG 1 — the owned parity clause applied to the rival alphabets ===")
def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def matpow(A, n):
    R = [[1,0],[0,1]]
    for _ in range(n): R = matmul(R, A)
    return R
def det2(A): return A[0][0]*A[1][1] - A[0][1]*A[1][0]
T = [[0,1],[1,-1]]           # the toral time operator, SceneStepParity.lean:31
check("L1-1 det T = -1 (Lean det_T reproduced)", det2(T) == -1)
check("L1-1 det(T^n) = (-1)^n for n=1..40 (computed, not assumed)",
      all(det2(matpow(T, n)) == (-1)**n for n in range(1, 41)))
def parity_class(n):          # orientation/holonomy class of address n = sign det(T^n)
    return det2(matpow(T, n))

# splice allowed iff the two layers carry the SAME Z2 class (Q2/Q4/Q5: flip => external bit => ⊥M1)
def splice_ok(m, n): return parity_class(m) == parity_class(n)

# Both F3 horns, the ladder horn at both of its textual sites (COMPLETENESS F3 + BOOK_03 §03.23.7).
# NOTE (post-skeptic R9): consecutive and nesting are two textual SITES of the ONE ladder horn,
# not independent readings — the kill is fork-robust across the TWO horns, not "three readings".
def kills_consecutive(tower):  # ladder horn, site 1 BOOK_03:1049-56: adjacent sorted steps
    t = sorted(tower)
    return any(not splice_ok(a, b) for a, b in zip(t, t[1:]))
def kills_nesting(tower):      # ladder horn, site 2 §03.23.7 Shell⊃Torus⊃Defect: same adjacency chain
    t = sorted(tower)
    return any(not splice_ok(t[i], t[i+1]) for i in range(len(t)-1))
def kills_overbase(tower):     # over-base horn :1551-53: every extension zone splices to the base 9
    base = min(tower)
    return any(not splice_ok(base, z) for z in tower if z != base)

def parity_kills_all_readings(tower):
    return kills_consecutive(tower) and kills_nesting(tower) and kills_overbase(tower)
def parity_kills_any_reading(tower):
    return kills_consecutive(tower) or kills_nesting(tower) or kills_overbase(tower)

X3_TOWER = (9, 11, 12)   # X3 = {{+1},{-1},{±i,±j,±k}}: 3 letters over V9 -> z3 = 12
check("L1-2 X3 tower (9,11,12) KILLED under BOTH F3 horns (ladder horn at both sites + over-base)",
      parity_kills_all_readings(X3_TOWER),
      "ladder: 11->12 = +1 (the book's own worked example); over-base: 9->12 = +3")
check("L1-2 owned tower (9,11,13) SURVIVES all readings", not parity_kills_any_reading((9,11,13)))
# NEGATIVE CONTROLS — the filter must NOT smuggle the +4 kill parity never owned (trap f):
check("L1-NC1 (9,11,15) SURVIVES parity in all readings (the V15 escape stays parity-alive)",
      not parity_kills_any_reading((9,11,15)),
      "if this failed, the filter would be over-strong — exactly EOR-2's banned over-read")
check("L1-NC2 (9,11,17) SURVIVES parity in all readings",
      not parity_kills_any_reading((9,11,17)))
check("L1-NC3 (9,13,17) survives parity (evenness admits +4 — reproduces NC_PARITY_ADMITS_PLUS4)",
      not parity_kills_any_reading((9,13,17)))

# L1-3: alphabet level — odd letter-count = parity flip; enumerate |X| = 1..8 over base 9
odd_killed, even_alive = [], []
for k in range(1, 9):
    tower = (9, 11, 9 + k) if 9 + k != 11 else (9, 11)  # degenerate 11 handled below
    if 9 + k == 11:
        continue  # |X|=2 reproduces the owned V11 (not a z3 rival)
    (odd_killed if parity_kills_all_readings(tower) else even_alive).append(k)
check("L1-3 parity kills EXACTLY the odd letter-counts {1,3,5,7}; even {4,6,8} ALIVE (honesty: "
      "the even rivals 6,8 are NOT closed by Leg 1 — no over-claim)",
      odd_killed == [1, 3, 5, 7] and even_alive == [4, 6, 8],
      f"killed={odd_killed}, alive={even_alive} (|X|=4 -> owned 13; 6,8 need LEG 2)")
check("L1-3 the nested chain {1,Z,Q8} (3 letters -> 12) dies the same owned death",
      parity_kills_all_readings((9, 11, 12)))
check("L1-3 the conjugacy-class partition (5 letters -> 14) dies the same owned death",
      parity_kills_all_readings((9, 11, 14)))

# L1-4: ERROR-OF-RECORD layer — mechanical exhibits
print("\n--- L1-4 errors of record (mechanical) ---")
check("EoR-B misquote: 6th memo P3 attributes a 'size 3' clause to the DYAD-POWER verdict",
      "size 3 (→ V₁₂)" in M6, "CLOSE_GAP_E_6TH_MEMO.md:96 (P3)")
check("EoR-B misquote: DYAD-POWER itself contains NO 'size 3' silence-exclusion (only size 6)",
      "size 3" not in DP and "size 6" in DP,
      "the silence-exclusion of the ODD size was never in the source memo")
check("EoR-A 5th memo carries 'z₃ = 12' as admissible survivor", "z₃ = 12" in M5)
check("EoR-C 7th memo carries 'z₃ = 12' as admissible residue", "z₃ = 12" in M7)
check("EoR-D META memo carries 'remains admissible under every clause the corpus owns' for z3=12",
      "remains admissible under every clause the corpus owns" in M9)
check("EoR-E the in-book window note B01:1562 carries the same over-claim (candidate layer)",
      "remains admissible under every clause the corpus owns" in B01)
# the campaign's OWN earlier tier already excluded 12 — the consistency dilemma:
def L0_evenness(tower):
    t = sorted(tower)
    return t[0] == 9 and len(t) == 3 and len(set(t)) == 3 and \
           all((b - a) % 2 == 0 for a, b in zip(t, t[1:]))
L0_surv = [z for z in range(10, 22) if L0_evenness((9, 11, z))]
check("EoR pin: the campaign's own L0 tier (base9+count3+evenness) leaves z3 odd >= 13 — 12 EXCLUDED",
      L0_surv == [13, 15, 17, 19, 21], f"L0 survivors z3={L0_surv}")
check("EoR pin: hence 'z3=12 admissible under EVERY clause' contradicts the campaign's own L0 record",
      12 not in L0_surv and "remains admissible under every clause the corpus owns" in M9)

# ------------------------------------------------- LEG 2 / L2-1: exact invariant deltas
print("\n=== LEG 2 — the which-one register (CANDIDATE layer; guards + computed deltas) ===")
def laplacian_K3(a, b, c):
    n = a + b + c
    part = [0]*a + [1]*b + [2]*c
    L = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and part[i] != part[j]:
                L[i][j] = -1
        L[i][i] = sum(1 for j in range(n) if j != i and part[j] != part[i])
    return L
def rank_frac(M):
    M = [[Fraction(x) for x in row] for row in M]
    n, m, r = len(M), len(M[0]), 0
    for col in range(m):
        piv = next((i for i in range(r, n) if M[i][col] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][col]
        M[r] = [x / inv for x in M[r]]
        for i in range(n):
            if i != r and M[i][col] != 0:
                M[i] = [x - M[i][col]*y for x, y in zip(M[i], M[r])]
        r += 1
        if r == n: break
    return r
def spectrum_K3(a, b, c):
    """Exact Laplacian spectrum via rank deficiency (independent of any formula)."""
    L = laplacian_K3(a, b, c)
    n = a + b + c
    spec = {}
    for lam in sorted({0, n, n - a, n - b, n - c}):
        Mm = [[L[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
        mult = n - rank_frac(Mm)
        if mult: spec[lam] = mult
    return spec, sum(L[i][i] for i in range(n)), n

INV = {}
for z in (12, 13, 15, 17):
    spec, capacity, n = spectrum_K3(9, 11, z)
    E = capacity // 2
    INV[z] = dict(V=n, E=E, CAP=capacity, spec=spec)
    print(f"  K(9,11,{z}): |V|={n} |E|={E} CAP=trace L={capacity} spec={spec}")
check("L2-1 spectra complete (multiplicities sum to n) for all four scenes",
      all(sum(INV[z]['spec'].values()) == INV[z]['V'] for z in INV))
check("L2-1 owned scene invariants: |V|=33, |E|=359, CAP=718",
      INV[13]['V'] == 33 and INV[13]['E'] == 359 and INV[13]['CAP'] == 718)
check("L2-1 X3 scene deltas NONZERO: (9,11,12) vs owned",
      INV[12]['V'] == 32 and INV[12]['E'] == 339 and INV[12]['CAP'] == 678
      and INV[12]['spec'] != INV[13]['spec'],
      "Δ|V|=-1, Δ|E|=-20, ΔCAP=-40, spectrum differs")
check("L2-1 V15 scene deltas NONZERO", INV[15]['E'] == 399 and INV[15]['spec'] != INV[13]['spec'])
check("L2-1 V17 scene deltas NONZERO", INV[17]['E'] == 439 and INV[17]['spec'] != INV[13]['spec'])
# (the same-size {Z,Q8∖Z} guard is computed at L2-3G below, AFTER the partition objects exist —
#  post-skeptic repair R2: tower sizes must be DERIVED from the partitions, not asserted)

# L2-2: the fork-register formalization + the firing rule (the theta-typing discriminator)
print("\n--- L2-2 fork-register + firing rule ---")
def register_bits(n_candidates): return math.ceil(math.log2(n_candidates)) if n_candidates > 1 else 0
def register_fires(n_candidates, deltas_nonzero, layer):
    """The candidate pattern U fires ONLY when: >=2 co-admissible candidates (a real fork),
    the fork is invariant-CHANGING (blade cell (A) content), and the fork sits in the
    M1-forced CONSTRUCTION layer (bridge-layer B-class rows legitimately consume declared
    external input — ASSUMP ledger practice)."""
    return n_candidates >= 2 and deltas_nonzero and layer == "construction"
# NOTE (post-skeptic R5): clause (iii) 'construction layer' of register_fires is AUTHORED IN THIS
# MEMO — no owned sentence restricts the pattern; it is disclosed as part of U's candidate content.
# The DEMO checks below exhibit the CANDIDATE rule's behavior; they are not corpus facts.
check("L2-2 DEMO: slot-3 size-fork {4,6} carries a 1-bit register and the candidate rule FIRES",
      register_bits(2) == 1 and register_fires(2, True, "construction"))
check("L2-2 DEMO: slot-3 size-fork {4,6,8} carries a 2-bit register and the candidate rule FIRES",
      register_bits(3) == 2 and register_fires(3, True, "construction"))
check("L2-2 DEMO: same-size fork does NOT fire (deltas zero -> gauge/torsor, class C)",
      not register_fires(2, False, "construction"))
check("L2-2 MUT-9TH REFUSAL: single candidate + underived presence does NOT fire",
      not register_fires(1, True, "construction"),
      "the KILLED 9th route (underived presence = ban) is NOT resurrected: no fork, no register")
# R4: the B-class rows' bridge-layer filing is READ FROM THE RECORD, not authored here:
W13 = read("_TASKS_CENTER_ATTACK/W1_W3_ALIGNMENT_MEMO.md")
TG = read("_TASKS_CENTER_ATTACK/TORSOR_GAUGE_SYNTHESIS_MEMO.md")
check("L2-2 QV: n_s row filed class B in the W1_W3 record (layer pinned by record, not authored)",
      "⇒ not C, not D ⇒ class B" in W13 and "n_s requires an" in W13, "W1_W3_ALIGNMENT_MEMO.md:187")
check("L2-2 QV: CKM completion filed class B-ext in the TORSOR_GAUGE record",
      "class B-ext** (Continent 2, parallel to CKM-OVERLAP)" in TG,
      "TORSOR_GAUGE_SYNTHESIS_MEMO.md:246")
B_CLASS_ROWS = [("n_s primordial tilt", 2, True, "bridge"),      # W1_W3:187, QV-pinned above
                ("CKM completion B-ext", 2, True, "bridge")]     # TORSOR_GAUGE:246, QV-pinned above
check("L2-2 MUT-D auto-close guard: bridge-layer B-class rows (n_s, CKM B-ext) do NOT fire",
      not any(register_fires(n, d, l) for _, n, d, l in B_CLASS_ROWS),
      "without the layer clause the pattern would 'close' every B-filed row — proves too much")
def register_fires_UNRESTRICTED(n_candidates, deltas_nonzero, layer):
    """MUTANT: the pattern WITHOUT the construction-layer clause (layer ignored)."""
    return n_candidates >= 2 and deltas_nonzero
check("L2-2 MUT-D' the UNRESTRICTED mutant fires on BOTH bridge B-class rows (conclusion moves)",
      all(register_fires_UNRESTRICTED(n, d, l) for _, n, d, l in B_CLASS_ROWS)
      and not any(register_fires(n, d, l) for _, n, d, l in B_CLASS_ROWS),
      "the layer clause is load-bearing: removing it would auto-close every B-filed row")

# L2-3: theta-typing side-by-side with the OWNED precedent BOOK_01:792 (computed, not narrated)
print("\n--- L2-3 Q8 vs D4: the conjugate-copy catalog of :792, computed ---")
# Q8 = {1,-1,i,-i,j,-j,k,-k} as indices 0..7 with exact multiplication table
Q8 = ["1","-1","i","-i","j","-j","k","-k"]
def qmul(x, y):
    sx, bx = (1, x) if not x.startswith("-") else (-1, x[1:])
    sy, by = (1, y) if not y.startswith("-") else (-1, y[1:])
    table = {("1","1"):"1", ("1","i"):"i", ("1","j"):"j", ("1","k"):"k",
             ("i","1"):"i", ("j","1"):"j", ("k","1"):"k",
             ("i","i"):"-1", ("j","j"):"-1", ("k","k"):"-1",
             ("i","j"):"k", ("j","i"):"-k", ("j","k"):"i", ("k","j"):"-i",
             ("k","i"):"j", ("i","k"):"-j"}
    r = table[(bx, by)]
    s = sx * sy * (1 if not r.startswith("-") else -1)
    b = r[1:] if r.startswith("-") else r
    return b if s == 1 else "-" + b
def qinv(x):
    for y in Q8:
        if qmul(x, y) == "1": return y
def subgroups(G, mul, inv):
    subs = []
    for r in range(0, len(G) + 1):
        for cand in itertools.combinations(G, r):
            S = set(cand)
            if not S or "1" not in S and "e" not in S: continue
            if all(mul(a, b) in S for a in S for b in S) and all(inv(a) in S for a in S):
                subs.append(frozenset(S))
    return set(subs)
def conjugates(G, H, mul, inv):
    return {frozenset(mul(mul(g, h), inv(g)) for h in H) for g in G}
q8_subs = subgroups(Q8, qmul, qinv)
q8_nonnormal = [H for H in q8_subs if len(conjugates(Q8, H, qmul, qinv)) > 1]
check("L2-3 Q8: EVERY subgroup normal (zero conjugate-copy catalogs) — the owned :792 mechanism",
      len(q8_nonnormal) == 0, f"{len(q8_subs)} subgroups, 0 non-normal")
# D4 (contrast object): symmetries of the square as permutations of 4 corners
def pcomp(p, q): return tuple(p[q[i]] for i in range(4))
def pinv(p):
    r = [0]*4
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
rot = (1, 2, 3, 0); refl = (1, 0, 3, 2)
D4 = set()
frontier = {(0, 1, 2, 3)}
while frontier:
    x = frontier.pop(); D4.add(x)
    for g in (rot, refl):
        y = pcomp(x, g)
        if y not in D4: frontier.add(y)
D4 = sorted(D4)
def d4subgroups():
    subs = []
    for r in range(1, 9):
        for cand in itertools.combinations(D4, r):
            S = set(cand)
            if (0,1,2,3) not in S: continue
            if all(pcomp(a, b) in S for a in S for b in S) and all(pinv(a) in S for a in S):
                subs.append(frozenset(S))
    return set(subs)
d4_nn = []
for H in d4subgroups():
    copies = {frozenset(pcomp(pcomp(g, h), pinv(g)) for h in H) for g in D4}
    if len(copies) > 1: d4_nn.append((H, len(copies)))
check("L2-3 D4 contrast: non-normal subgroups EXIST, each dragging a conjugate-copy catalog",
      len(d4_nn) > 0 and all(c >= 2 for _, c in d4_nn),
      f"{len(d4_nn)} non-normal subgroups, copy-catalog sizes {sorted(set(c for _, c in d4_nn))}"
      " -> >=1-bit which-copy register: the FORMAL shape Leg 2 transfers")
# (post-skeptic R2: the former "register shape identical" check was a tautology — DELETED;
#  the 1-bit shape correspondence is carried by the D4 catalog check above + register_bits(2)==1)
# the honest DIS-analogy bit, computed: both rival partitions DO coexist on the realized carrier
Q8set = frozenset(Q8)
X3_part = [frozenset({"1"}), frozenset({"-1"}), frozenset({"i","-i","j","-j","k","-k"})]
ROLE_part = [frozenset({"1","-1"}), frozenset({"i","-i"}), frozenset({"j","-j"}), frozenset({"k","-k"})]
def is_partition(blocks, ground):
    u = set()
    for b in blocks:
        if u & b: return False
        u |= b
    return u == ground
check("L2-3 co-presence: X3 and the role-coset partition are BOTH partitions of the one realized Q8",
      is_partition(X3_part, Q8set) and is_partition(ROLE_part, Q8set),
      "the fork's CARRIERS are object-internal; what is NOT object-internal is the ADMISSIBILITY "
      "flag on them — the graded dis-analogy the memo prices (SELF-ATT-U1)")

# L2-3G: the same-size guard, REBUILT (post-skeptic R2) — tower sizes DERIVED from the partitions
print("\n--- L2-3G same-size guard: {Z, Q8∖Z} rival, sizes derived from the partition objects ---")
ZQ8C_part = [frozenset({"1", "-1"}),
             frozenset({"i", "-i", "j", "-j", "k", "-k"})]   # {Z, Q8∖Z}: 2 letters, blocks 2,6
SIGN_part = [frozenset({"1", "i", "j", "k"}),
             frozenset({"-1", "-i", "-j", "-k"})]            # 2-letter SIZE-model of the dyad slot
# (disclosed: SIGN models only the slot-2 LETTER-COUNT; the owned dyad's identity is the
#  direct/return capacity :1548 — the two-universe issue of the 5th/6th passes, unchanged)
def tower_from(p_slot2, p_slot3):
    return tuple(sorted((9, 9 + len(p_slot2), 9 + len(p_slot3))))
check("L2-3G {Z,Q8∖Z} IS a partition of Q8 (blocks 2,6) and has 2 letters",
      is_partition(ZQ8C_part, Q8set) and len(ZQ8C_part) == 2 and
      sorted(len(b) for b in ZQ8C_part) == [2, 6])
t_owned = tower_from(SIGN_part, ROLE_part)
t_same = tower_from(ZQ8C_part, ROLE_part)
t_x3 = tower_from(SIGN_part, X3_part)
check("L2-3G derived towers: owned-size (9,11,13); {Z,Q8∖Z}-rival (9,11,13); X3-rival (9,11,12)",
      t_owned == (9, 11, 13) and t_same == (9, 11, 13) and t_x3 == (9, 11, 12))
check("L2-3G same-size rival has ALL-ZERO graph deltas (spectrum/|V|/|E|/CAP identical, computed)",
      spectrum_K3(*t_same) == spectrum_K3(*t_owned),
      "invariant-preserving fork => class-C/torsor territory (row 549), NOT killable by the register")
check("L2-3G contrast: the X3-rival tower derived the same way has NONZERO deltas",
      spectrum_K3(*t_x3) != spectrum_K3(*t_owned),
      "the guard distinguishes; it is not vacuously equal")

# L2-4: the survivor cascade (per-filter enumeration over alphabet pairs)
print("\n--- L2-4 survivor cascade over alphabet pairs (|X2|,|X3|) in {1..8}^2 ---")
def cascade(grant_u, use_parity=True):
    pairs = [(a, b) for a in range(1, 9) for b in range(1, 9)]          # F0 partition bound (<=8 blocks)
    stages = [("F0 partition-rule bound (5th, ASSEMBLY): 1<=|X|<=8", pairs)]
    p2 = [(a, b) for a, b in pairs if a < b]                             # F1 distinct sizes, ordered
    stages.append(("F1 distinct sizes (E4 ASSEMBLY: |S2|>1 equal-zone kill) + order", p2))
    if use_parity:
        p3 = [(a, b) for a, b in p2 if a % 2 == 0 and b % 2 == 0]        # F2 OWNED parity (Leg 1)
    else:
        p3 = list(p2)
    stages.append(("F2 parity: odd letter-count = Z2 flip (OWNED, Leg 1)", p3))
    if grant_u:
        p4 = [(a, b) for a, b in p3 if (a, b) == (2, 4)]                 # F3 U granted
        stages.append(("F3 U (which-one register ban, CANDIDATE) + membership :1548", p4))
    return stages
st = cascade(False)
for name, s in st:
    print(f"  {name}: {len(s)} survive" + (f" -> {s}" if len(s) <= 8 else ""))
surv_no_u = st[-1][1]
check("L2-4 after OWNED+ASSEMBLY filters the rival space is EXACTLY 6 towers",
      surv_no_u == [(2,4),(2,6),(2,8),(4,6),(4,8),(6,8)],
      "sorted-tower images: (9,11,13) owned + rivals (9,11,15),(9,11,17),(9,13,15),(9,13,17),(9,15,17)")
check("L2-4 z3 rival VALUES after Leg 1 = {15, 17} (12 gone; FINITE given the ASSEMBLY-grade "
      "partition bound; owned-parity-only residue = z3 odd >= 13, UNBOUNDED)",
      sorted({9 + b for _, b in surv_no_u if (9 + b) != 13}) == [15, 17],
      "finiteness rests on the 5th's partition rule (assembly), disclosed — R7; parity alone "
      "gives the unbounded odd family, exactly the prior L0+ record")
st_u = cascade(True)
check("MUT-A sufficiency: granting U collapses the cascade to the owned pair (2,4) alone",
      st_u[-1][1] == [(2, 4)], "U + membership => AdmExt sizes {2,4}, tower (9,11,13), z3<=13")
st_nop = cascade(False, use_parity=False)
check("MUT-B parity load-bearing: dropping F2 revives odd pairs incl. (2,3) -> (9,11,12)",
      (2, 3) in st_nop[-1][1], "the Leg-1 conclusion CAN fail — the filter is not decorative")
# MUT-C (post-skeptic R2 rebuild): model "U without membership" — per-slot size-uniqueness alone
uniq_worlds = sorted({(a, b) for a in (2, 4, 6, 8) for b in (2, 4, 6, 8) if a < b})
check("MUT-C membership load-bearing: U alone (per-slot uniqueness) leaves 6 candidate worlds — "
      "values NOT pinned; only owned membership :1548 selects (2,4)",
      len(uniq_worlds) == 6 and (2, 4) in uniq_worlds and
      "the only primitive unresolved capacities" in B01,
      f"uniqueness-only worlds = {uniq_worlds}; each is a consistent 'unique per slot' assignment")

# ------------------------------------------------------------------- final state
print("\n=== FINAL STATE ===")
print(f"checks: {NCHK[0]} run, {len(FAILS)} failed")
if FAILS:
    print("BROKEN:", *FAILS, sep="\n  - ")
    sys.exit(1)
print("LEG 1: X3 / z3=12 (and every odd letter-count) KILLED at the owned parity clause's "
      "operative grade, under BOTH F3 horns; errors of record exhibited mechanically "
      "(5th/6th/7th/META/B01:1562).")
print("LEG 2: which-one register = CANDIDATE, DOOR-(a)-ARMED (:792-ANALOGOUS form, clause (iii) "
      "authored+disclosed; refuses the killed 9th route and bridge-layer B-class rows). "
      "Residual rival set after Leg 1: z3 in {15, 17} given the assembly-grade partition bound "
      "(owned-parity-only residue: z3 odd >= 13, unbounded) — awaiting the owner sentence "
      "U or H7 (either door-(a) text closes the window).")
if GRANT_U:
    print("rc=0 (--grant-uniqueness): MUT-A demonstrated — U seals z3<=13, AdmExt sizes {2,4}.")
    sys.exit(0)
print("rc=2 — HONEST-OPEN: door ARMED, not closed; window upper bound NARROWED; no owned rule minted.")
sys.exit(2)
