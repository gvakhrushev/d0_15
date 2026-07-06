#!/usr/bin/env python3
"""w4_decomposition_check — W4 T4 "Missing-object=Decomposition" computation layer (can-fail).

Companion to _TASKS_CENTER_ATTACK/W4_DECOMPOSITION_MEMO.md. READ-ONLY on registry/books:
this script rebuilds every load-bearing object INDEPENDENTLY (no import from the corpus)
and checks the claims with exact arithmetic (int / Fraction only; no floats anywhere).

Targets:
  T1  D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001  — contravariant (co-tower) reading
  T2A D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 — two-layer decomposition + 33-skip totality
  T2B D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001 — split into 2 independent primitives
  T3  D0-PHASE-TOWER-002 — shell-2: unit-group reading + attractor census
  T4  E4+L4 third-generation T4-hypothesis adjudication (STRICT: no derivation attempted)

Domain-quantification discipline (traps (k)-(o), GAP_E §SKEPTIC-#1 calibration): every
totality scan states its domain next to the assertion; bounded scans are closed by an
explicit monotonicity/recurrence argument checked at the algebraic step, not by hope.
Every negative control can fail the CONCLUSION (a rival object is actually constructed
and actually fails), not merely the technique.
"""
from fractions import Fraction
from math import gcd

CHECKS = 0
def ok(name: str, cond: bool) -> None:
    global CHECKS
    if not cond:
        print(f"FAIL {name}")
        raise SystemExit(1)
    CHECKS += 1
    print(f"PASS {name}")

# ============================================================================
# Shared exact builders (independent of the corpus code)
# ============================================================================

def totient(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)

def units(n: int):
    return [k for k in range(1, n + 1) if gcd(k, n) == 1]

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)

# ============================================================================
# T1 — archive co-tower: modes(n) = (n+2)^4, projection = mod (ArchiveRefinementTower.lean:16,67)
# ============================================================================
print("== T1: INDUCTIVE-SPECTRAL-TRIPLE — contravariant co-tower content ==")

def modes(n: int) -> int:
    return (n + 2) ** 4

def proj(n: int, x: int) -> int:            # archiveProjection n : A_{n+1} -> A_n
    return x % modes(n)

# T1.1 levels & monotonicity (domain: n in 0..6 scanned; closed for all n by (n+3)^4>(n+2)^4)
ok("T1.1 modes 0..6 = 16,81,256,625,1296,2401,4096 and strictly increasing",
   [modes(n) for n in range(7)] == [16, 81, 256, 625, 1296, 2401, 4096]
   and all(modes(n + 1) > modes(n) for n in range(6)))

# T1.2 bonding surjectivity (FULL image scan at n=0,1,2 — the claim's domain is each single step)
ok("T1.2 archiveProjection surjective at n=0,1,2 (full image scan)",
   all(set(proj(n, x) for x in range(modes(n + 1))) == set(range(modes(n))) for n in range(3)))

# T1.3 kernel pullback compatibility along the COMPOSITE (Delta_{n+1}(x,y)=Delta_n(Px,Py), rfl in Lean).
# Independent rebuild: Delta_0 = equality kernel on Fin 16; Delta_1, Delta_2 by pullback. FULL scan at
# level 2 (256^2 pairs) that Delta_2(x,y) == Delta_0(P0(P1 x), P0(P1 y)) — composite compatibility.
def delta0(a: int, b: int) -> int:
    return 1 if a == b else 0
def delta1(a: int, b: int) -> int:
    return delta0(proj(0, a), proj(0, b))
def delta2(a: int, b: int) -> int:
    return delta1(proj(1, a), proj(1, b))
ok("T1.3 pullback kernels compatible along composites (full 256^2 scan)",
   all(delta2(x, y) == delta0(proj(0, proj(1, x)), proj(0, proj(1, y)))
       for x in range(modes(2)) for y in range(modes(2))))

# T1.4 NEGATIVE CONTROL (can fail the conclusion): the rival "direct mod" family A_2->A_0,
# x -> x mod 16 is NOT the diagram's composite bonding map — compatibility is non-vacuous.
direct_vs_composite = [(x, x % modes(0), proj(0, proj(1, x))) for x in range(modes(2))]
mismatches = [t for t in direct_vs_composite if t[1] != t[2]]
ok("T1.4 rival direct-mod family FAILS compatibility (witness x=100: 4 != 3; mismatches exist)",
   (100, 4, 3) in direct_vs_composite and len(mismatches) > 0)

# T1.5 fiber sizes of P_0 are NON-uniform: sizes {6 x1, 5 x15}, sum 81 (exact census).
fib0 = {u: [x for x in range(modes(1)) if proj(0, x) == u] for u in range(modes(0))}
sizes0 = sorted(len(v) for v in fib0.values())
ok("T1.5 P_0 fiber census: one fiber of size 6, fifteen of size 5, total 81",
   sizes0 == [5] * 15 + [6] and sum(sizes0) == modes(1))

# T1.6 the CANONICAL (uniform) measure family is NOT projectively compatible:
# pushforward of uniform(81) along P_0 gives {6/81 once, 5/81 else} != uniform(16).
push = {u: Fraction(len(fib0[u]), modes(1)) for u in range(modes(0))}
ok("T1.6 uniform measures NOT projectively compatible (pushforward 6/81,5/81 != 1/16)",
   push[0] == Fraction(6, 81) and push[1] == Fraction(5, 81)
   and any(push[u] != Fraction(1, modes(0)) for u in range(modes(0))))

# T1.7 uniform-fiber CONTROL (the same check CAN pass on the right structure): toy tower
# 4 -> 8 (mod 4, fibers uniform size 2): pushforward of uniform(8) IS uniform(4).
toy_push = {u: Fraction(sum(1 for x in range(8) if x % 4 == u), 8) for u in range(4)}
ok("T1.7 control: divisible tower (8->4 mod) has compatible uniform measures",
   all(toy_push[u] == Fraction(1, 4) for u in range(4)))

# T1.8 conditional-expectation coherence FAILS for uniform weights on the archive tower:
# E_0∘E_1 != E_composite. Witness: indicator of {0} on A_2. Exact Fractions.
fib1 = {u: [x for x in range(modes(2)) if proj(1, x) == u] for u in range(modes(1))}
fibC = {u: [x for x in range(modes(2)) if proj(0, proj(1, x)) == u] for u in range(modes(0))}
f = {x: Fraction(1 if x == 0 else 0) for x in range(modes(2))}
E1f = {u: sum(f[x] for x in fib1[u]) / len(fib1[u]) for u in range(modes(1))}
E0E1f = {u: sum(E1f[v] for v in fib0[u]) / len(fib0[u]) for u in range(modes(0))}
ECf = {u: sum(f[x] for x in fibC[u]) / len(fibC[u]) for u in range(modes(0))}
ok("T1.8 E_0∘E_1 != E_composite at u=0 (uniform fiber-average expectations not coherent)",
   E0E1f[0] != ECf[0])
# ... and the SAME construction IS coherent on the divisible toy tower 16->8->4 (mod maps):
tf = {x: Fraction(1 if x == 0 else 0) for x in range(16)}
tE1 = {u: sum(tf[x] for x in range(16) if x % 8 == u) / 2 for u in range(8)}
tE0E1 = {u: sum(tE1[v] for v in range(8) if v % 4 == u) / 2 for u in range(4)}
tEC = {u: sum(tf[x] for x in range(16) if x % 4 == u) / 4 for u in range(4)}
ok("T1.9 control: on the divisible tower 16->8->4 the expectations ARE coherent",
   all(tE0E1[u] == tEC[u] for u in range(4)))

# T1.10 exact weighted intertwining E_0 · Delta_1 · U_0 = Delta_0 · W_0 (W_0 = fiber-size diagonal).
# NOTE (trap (m)): this identity holds for ANY base kernel pulled back along ANY surjection —
# its sole content is the ATTRIBUTION: the defect from Delta_0 is exactly the fiber-multiplicity
# (capacity) diagonal W_0. Checked for the equality kernel AND a nontrivial cyclic kernel.
def check_intertwining(base):
    m0, m1 = modes(0), modes(1)
    lhs = [[Fraction(0)] * m0 for _ in range(m0)]
    for u in range(m0):
        for v in range(m0):
            # (E0 Delta1 U0)(u,v) = (1/|fib(u)|) sum_{x in fib(u)} sum_{y in fib(v)} base(P x, P y)
            s = sum(Fraction(base(proj(0, x), proj(0, y))) for x in fib0[u] for y in fib0[v])
            lhs[u][v] = s / len(fib0[u])
    rhs = [[Fraction(base(u, v)) * len(fib0[v]) for v in range(m0)] for u in range(m0)]
    return lhs == rhs
ok("T1.10 E_0·Δ_1·U_0 = Δ_0·W_0 exactly (equality kernel)", check_intertwining(delta0))
ok("T1.11 E_0·Δ_1·U_0 = Δ_0·W_0 exactly (cyclic kernel — attribution is generic)",
   check_intertwining(lambda a, b: 1 if (a - b) % modes(0) in (1, modes(0) - 1) else 0))

# T1.12 the pullback candidate J is NOT an isometry and cannot be normalized into Dirac
# compatibility: U_0^T U_0 = W_0 != c·I (sizes 6 and 5 differ), and after any per-fiber
# normalization the diagonal demand |fib u|^2 = |fib u| forces |fib u| = 1 — false here.
ok("T1.12 isometry obstruction: fiber sizes {5,6} differ and |fib|^2 != |fib| for all fibers",
   len(set(sizes0)) == 2 and all(s * s != s for s in sizes0))

# ============================================================================
# T2A — AF tower vs frozen 33-dim scene: totality of the 33-skip
# ============================================================================
print("== T2A: DIRAC-LAPLACIAN-COMPATIBILITY — 33-skip totality + two-layer split ==")

def pc(n: int):
    a, b = 1, 1
    for _ in range(n):
        a, b = a + b, a
    return a, b
def dimA(n: int) -> int:
    a, b = pc(n)
    return a * a + b * b

ok("T2A.1 dimA 0..5 = 2,5,13,34,89,233 (matches FibonacciAFAlgebra.lean:32)",
   [dimA(n) for n in range(6)] == [2, 5, 13, 34, 89, 233])
ok("T2A.2 scene carrier 33 = 9+11+13 = 1+12+10+8+2 (both owned partitions)",
   9 + 11 + 13 == 33 and 1 + 12 + 10 + 8 + 2 == 33)
# Totality (domain: ALL n, not the Lean row's n<=3): dimA(n+1)-dimA(n) = a(a+2b) with a,b>=1,
# so dimA is strictly increasing for ALL n; dimA(3)=34>33 closes n>=3; scan closes n<=3.
# The algebraic step is itself checked exactly on a window, plus positivity of a,b.
def step_gap(n: int) -> int:
    a, b = pc(n)
    return dimA(n + 1) - dimA(n) - a * (a + 2 * b)
ok("T2A.3 recurrence identity dimA(n+1)-dimA(n) = a(a+2b) holds exactly (n=0..40)",
   all(step_gap(n) == 0 for n in range(41)))
ok("T2A.4 a,b >= 1 for n=0..40 and induction step (a,b>=1 -> a+b>=2, a>=1) is arithmetic",
   all(pc(n)[0] >= 1 and pc(n)[1] >= 1 for n in range(41)))
ok("T2A.5 33-skip TOTAL: dimA(n) != 33 for n<=3 by scan, for n>3 by dimA(3)=34 + strict growth",
   all(dimA(n) != 33 for n in range(4)) and dimA(3) == 34
   and all(dimA(n + 1) > dimA(n) for n in range(41)))
# Cross-identity: dimA(n) = F(2n+3) (odd-indexed Fibonacci) — typed separator, no level hits 33.
F = [0, 1]
for _ in range(90):
    F.append(F[-1] + F[-2])
ok("T2A.6 dimA(n) = F(2n+3) for n=0..40 and 33 is not an odd-indexed Fibonacci",
   all(dimA(n) == F[2 * n + 3] for n in range(41)) and 33 not in {F[2 * n + 3] for n in range(41)}
   and 33 not in F[:20])

# ============================================================================
# T2B — the single primitive splits into 2 INDEPENDENT primitives (scale ⊕ comparison)
# ============================================================================
print("== T2B: ISOMETRIC-DIRAC-TOWER — independence of the two split layers ==")

# Scale layer: witness pair phi^N vs 2^N in exact Z[phi] pairs (phi^n = F(n-1)+F(n)·phi).
def phi_pow(n: int):
    return (F[n - 1] if n >= 1 else (1 if n == 0 else None), F[n])
ok("T2B.1 scale witness pair genuinely distinct: phi^N != 2^N for N=1..20 (exact Z[phi])",
   all(phi_pow(n) != (2 ** n, 0) for n in range(1, 21)))
# Comparison layer, made non-vacuous (skeptic repair, replaces a vacuous list==itself check):
# model the scale law as an EXPLICIT parameter of a joint object (scale_value_n, dim_n) and
# actually VARY it over the owned witness pair. The dim component is invariant under the
# variation while the scale component differs at every level.
# HONESTY LABEL: that dimA takes no scale input is DEFINITIONAL BOOKKEEPING of the owned
# formalization (FibonacciAFAlgebra.lean:23-28 — pc/dimA have no scale parameter); this check
# exhibits the variation, it does not prove independence beyond what the definitions carry.
joint_phi = [(phi_pow(n), dimA(n)) for n in range(1, 21)]
joint_two = [((2 ** n, 0), dimA(n)) for n in range(1, 21)]
ok("T2B.2 varied joint (scale, dim) object: dim components equal, scale components differ, all levels",
   all(a[1] == b[1] for a, b in zip(joint_phi, joint_two))
   and all(a[0] != b[0] for a, b in zip(joint_phi, joint_two)))
ok("T2B.3 the 33-skip persists under BOTH scale choices of the varied joint object",
   all(d != 33 for _, d in joint_phi) and all(d != 33 for _, d in joint_two)
   and min(abs(d - 33) for _, d in joint_phi[:9]) == 1)

# ============================================================================
# T3 — PHASE-TOWER-002: shell chain, unit-group reading, attractor census
# ============================================================================
print("== T3: PHASE-TOWER-002 — shell-2 as unit-group layer; seed-independence guard ==")

ROLES = 4  # ABCDn (PhaseTower.lean:16, ABCDn_value = 4)
def next_shell(s: int) -> int:
    return max(1, totient(lcm(ROLES, s)))

# T3.1 the owned chain from the owned seed shell0 = V11n = 11 (PhaseTower.lean:27)
chain = [11]
for _ in range(6):
    chain.append(next_shell(chain[-1]))
ok("T3.1 shell chain 11 -> 20 -> 8 -> 4 -> 2 -> 2 -> 2 (stabilization depth 4)",
   chain == [11, 20, 8, 4, 2, 2, 2])
ok("T3.2 windows along the chain: 44, 20, 8, 4, 4 (terminal window = 4 = |ABCD|)",
   [lcm(ROLES, s) for s in chain[:5]] == [44, 20, 8, 4, 4])

# T3.3 unit-group reading (owned instance THE-A BOOK_01:1615 at q=44; totient=|units| is
# theorem-grade): verify phi(q) = |units(Z/q)| by direct census at every window in the chain.
ok("T3.3 phi(q) = #units(Z/q) by direct census at q in {44,20,8,4}",
   all(totient(q) == len(units(q)) for q in (44, 20, 8, 4)))
ok("T3.4 owned weld instance: phi(44) = 20 (= d13, BOOK_01:1431/1615) and (Z/44)* has order 20",
   totient(44) == 20 and len(units(44)) == 20)
ok("T3.5 terminal unit group (Z/4)* = {1,3} = {+1,-1 mod 4}, cyclic of order 2",
   units(4) == [1, 3] and (3 - (-1)) % 4 == 0 and (3 * 3) % 4 == 1)

# T3.6 fixed-point census over the recursion's ACTUAL domain (all seeds s>=1; bounded scan
# B=10000 closed by: for s > 2, lcm(4,s) >= s and phi(m) <= m/2 for even m, and lcm(4,s) is
# always even, so next_shell(s) <= lcm(4,s)/2 <= 2s ... — closure is by the DESCENT check
# T3.7 below, not by this inequality alone; the census itself is the exhaustive scan).
fixed = [s for s in range(1, 10001) if next_shell(s) == s]
ok("T3.6 unique fixed point s=2 in 1..10000", fixed == [2])

# T3.7 GLOBAL ATTRACTOR (anti-over-read guard, trap (m)): EVERY seed 1..10000 reaches 2.
# If the terminal value 2 is seed-independent, then "stabilizes at shell two" carries ZERO
# scene-specific information in its VALUE — the scene content lives in the owned seed 11,
# the owned weld phi(44)=20=d13, and the depth-4 path, NOT in the terminal 2.
def reaches_two(s: int, cap: int = 200) -> bool:
    seen = set()
    while s not in seen:
        seen.add(s)
        s = next_shell(s)
        if s == 2:
            return True
    return s == 2
ok("T3.7 every seed 1..10000 reaches 2 (value 2 is a universal totient attractor)",
   all(reaches_two(s) for s in range(1, 10001)))

# T3.8 disambiguation control: M2's 'shell' is the 9-object pointed shell V9 = Omega8 ⊔ {w0};
# the capacity shell field is a DIFFERENT object (initialized at V11n=11, not 9).
ok("T3.8 capacity shell seed = 11 = V11n != 9 = |V9| (M2 pointed shell is a different object)",
   chain[0] == 11 and 11 != 9 and 8 + 1 == 9)

# T3.9 SKEPTIC KILL ARITHMETIC (BOOK_01:1403 precondition): the owned branch semantics of THE-A
# requires a RETURN window — an integer pair (q,m) with |q − m·τ₀| ≪ 1 (τ₀ = 44/7 from the owned
# first return 44 ≈ 7τ₀, BOOK_01:1393, which is EXACT for the surrogate: |44 − 7·(44/7)| = 0).
# The downstream windows 20, 8, 4 all FAIL the precondition: best |q − m·τ₀| over all m ∈ 0..2q
# is 8/7, 12/7, 16/7 respectively — none ≪ 1 (all > 1). Exact Fractions; hence the unit-group
# branch reading is NOT owned at the terminal window and the T4 reading of shell-2 is BLOCKED.
tau0 = Fraction(44, 7)
def best_return_defect(q: int) -> Fraction:
    return min(abs(Fraction(q) - m * tau0) for m in range(0, 2 * q + 1))
ok("T3.9 return-window precondition: defect 0 at q=44; 8/7, 12/7, 16/7 at q=20,8,4 (all > 1)",
   best_return_defect(44) == 0
   and best_return_defect(20) == Fraction(8, 7)
   and best_return_defect(8) == Fraction(12, 7)
   and best_return_defect(4) == Fraction(16, 7)
   and all(best_return_defect(q) > 1 for q in (20, 8, 4)))

# ============================================================================
# T4 — E4+L4: adjudicate the layer-hypothesis WITHOUT deriving a third generation
# ============================================================================
print("== T4: E4+L4 third generation — layer-hypothesis adjudication (no derivation) ==")

# sigma = (0 1 2 3)(4 5 6) on 7 points (LeptonBranchFixingNoGo.lean:37)
sigma = [1, 2, 3, 0, 5, 6, 4]
# T4.1 orbits and fixed points (full scan of the actual 7-point domain)
def orbits(perm):
    seen, out = set(), []
    for i in range(len(perm)):
        if i in seen:
            continue
        o, j = [i], perm[i]
        while j != i:
            o.append(j); j = perm[j]
        seen.update(o); out.append(sorted(o))
    return out
orbs = orbits(sigma)
ok("T4.1 sigma has exactly 2 orbits, sizes {4,3}, and NO fixed point (full scan)",
   sorted(len(o) for o in orbs) == [3, 4] and all(sigma[i] != i for i in range(7)))

# T4.2 trivial-isotype multiplicity of the branch carrier = #orbits = 2, by Burnside over
# <sigma> ≅ C12 (exact integer average of fixed-point counts).
def perm_pow(perm, k):
    out = list(range(len(perm)))
    for _ in range(k):
        out = [perm[i] for i in out]
    return out
fixes = [sum(1 for i in range(7) if perm_pow(sigma, k)[i] == i) for k in range(12)]
ok("T4.2 Burnside: (1/12)·sum fix(sigma^k) = 24/12 = 2 trivial-isotype copies in C^7",
   sum(fixes) == 24 and Fraction(sum(fixes), 12) == 2 and perm_pow(sigma, 12) == list(range(7)))

# T4.3 generation count on the OTHER owned carrier: T = [[0,1],[1,-1]] (BOOK_01:1136),
# Tr(T^2) = 3 — exact integer matrix arithmetic.
T = [[0, 1], [1, -1]]
T2 = [[sum(T[i][k] * T[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
ok("T4.3 Tr(T^2) = 3 (generation count lives on the scene/toral side, not the 7-pt carrier)",
   T2[0][0] + T2[1][1] == 3)

# T4.4 pigeonhole totality over the ACTUAL map domains (all 8 maps Fin3->Fin2; all 9... —
# no: all 2^3=8 and 3^2=9 maps enumerated exhaustively):
inj = [f for f in [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
       if len(set(f)) == 3]
sur = [g for g in [(a, b) for a in range(3) for b in range(3)] if set(g) == {0, 1, 2}]
ok("T4.4 no injection Gen(3)->Branch(2) among all 8 maps; no surjection Branch(2)->Gen(3) among all 9",
   inj == [] and sur == [])

# T4.5 the IN-CARRIER form of the T4 layer-hypothesis is refuted: the trivial-isotype layer
# count of the branch carrier is 2 (= the branches themselves, one per orbit), and the
# would-be third 'regular/fixed' layer requires a fixed point — sigma has none (T4.1).
ok("T4.5 in-carrier layer count 2 = numBranches; no third in-carrier layer exists",
   Fraction(sum(fixes), 12) == 2 and all(sigma[i] != i for i in range(7)))

# T4.6 NEGATIVE CONTROL (can fail the conclusion): a rival carrier WITH a fixed point —
# sigma' = (0 1 2 3)(4 5 6 -> shifted to fix 6)? Use (0 1 2 3)(4 5) fixing 6 on 7 points:
# it HAS a third (trivial) orbit, and Burnside then gives 3 — i.e. the check distinguishes
# carriers where the layer-reading WOULD supply a third branch from the owned one that can't.
sigma_r = [1, 2, 3, 0, 5, 4, 6]
orbs_r = orbits(sigma_r)
fixes_r = [sum(1 for i in range(7) if perm_pow(sigma_r, k)[i] == i) for k in range(4)]
ok("T4.6 control: rival (0123)(45)(6) has 3 orbits incl. a fixed point; Burnside gives 3",
   sorted(len(o) for o in orbs_r) == [1, 2, 4] and Fraction(sum(fixes_r), 4) == 3)

print(f"ALL {CHECKS} CHECKS PASS — rc=0")
print("VERDICTS (computation layer, post-skeptic): T1 co-tower kernel-level compatible (module owner")
print("row 24; rfl theorems registry-UNREGISTERED — hygiene item), expectation-level needs a weight")
print("datum (uniform fails coherence: T1.6/T1.8; nearest owned neighbor row 41 ARCHIVE-LAPLACIAN-RG);")
print("T2A decomposition OWNED + 33-skip TOTAL; T2B split OWNED, variation exhibited (bookkeeping");
print("label); T3 HONEST-BLOCKED — unit-group branch semantics is return-window-conditional and 20/8/4")
print("fail the |q−m·τ₀|≪1 precondition (T3.9); value 2 is a universal attractor anyway (T3.7);")
print("T4 HONEST-BLOCKED — in-carrier third layer refuted, cross-carrier bridge =")
print("PRIM-LEPTON-BRANCH-FIXING-OPERATOR stays the exact missing object.")
