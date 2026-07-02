# TASK W7 REPORT — Typed (Bartholdi) zeta certificate: exact identity + golden-point specialization

**Scene:** K(9,11,13) — |V|=33, |E|=359, 2|E|=718 directed edges, |E|−|V|=326.
**Cert:** `_TASKS_CENTER_ATTACK/vp_scene_bartholdi_typed.py` (NOT in `05_CERTS/`, NOT registered).
**Status of this document:** deliverable of TASK W7. No registry row edited. No promotion language
outside quoted context. Local env: Python 3.9.6, numpy 2.0.2 (sympy present but not used — cert is
pure Fraction/modular).

This report is organised into four evidentiary tiers, kept strictly separate:
**SOURCED** (external literature), **PROVED-HERE** (exact computation in the cert),
**REPORT-ONLY** (numerical/structural comparisons, no decision weight), **OPEN** (unresolved).

---

## 0. One-paragraph verdict

The brief's identity

    det(I − u(B+tR)) = (1−(1−t)²u²)^326 · det(I − uA + (1−t)(D−(1−t)I)u²)

(B = non-backtracking Hashimoto, R = backtrack involution) matches the published Bartholdi–Ihara–Bass
determinant formula (Bartholdi 1999, Thm 5.4; Sato–Mitsuhashi–Morita 2013, "Theorem 2 (Bartholdi)")
**under a two-part dictionary** — (a) a variable-name transposition (u,t)_ours ↔ (t,u)_lit, and (b)
the brief's `B` is the *non-backtracking* Hashimoto matrix, whereas the published `B` (call it `B_pub`)
is the *full head-meets-tail* matrix `B_pub = B + R`; the published edge operator `B_pub − (1−t)R`
then equals the brief's `B + tR` identically. Both facts are PROVED-HERE (the cert implements the
published edge operator and shows it equals the brief's form bit-for-bit modularly). The exact
two-variable verification (7 rational (u,t), both degenerations), the exact golden-point verification
over ℚ(φ) (split-prime modular, both embeddings φ↦(1±√5)/2, plus exact 2-component scalar arithmetic),
and all four negative controls **PASS**. The exact compressed charpoly of B_p = B + pR over ℚ(φ) is a
sextic (§4). The strongest reason t=p may not be forced is in §5.

---

## 1. SOURCED — the external theorem and the dictionary

**Primary source.** Laurent Bartholdi, "Counting paths in graphs," *L'Enseignement Mathématique*
**45** (1999), no. 1–2, pp. 83–131. Theorem 5.4 states the Bartholdi zeta reciprocal; its edge form
(his §5) uses the operator `M = I − (B − (1−u)J) t`, with **`u` = bump variable, `t` = length
variable** — i.e. the opposite letter assignment to the brief.

**Cleanest verbatim restatement.** Iwao Sato, Hideo Mitsuhashi, Hideaki Morita, "A new determinant
expression for the weighted Bartholdi zeta function of a digraph," *Electron. J. Combin.* **20(1)**
(2013), #P27, **Theorem 2 (Bartholdi)** (verbatim, literature letters):

> ζ(G,u,t)⁻¹ = det(I_{2m} − t(B − (1−u)J₀))
>            = (1 − (1−u)²t²)^{m−n} · det(I − tA(G) + (1−u)(D − (1−u)I)t²).
> In the case of u = 0, Theorem 2 implies Theorem 1 [Ihara–Bass].

Here `B_{e,f}=1 iff t(e)=o(f)` is the **full** edge-adjacency (head-meets-tail) matrix — it *includes*
backtracks — and `J₀` is the reversal/backtrack involution (the brief's R). `m = |E|`, `n = |V|`,
exponent `m−n`. Third independent source (deformed-Laplacian form, `Q = D−I`, prefactor
`1−(1−u)²z²`): Guido–Isola–Lapidus, "Bartholdi Zeta Functions for Periodic Simple Graphs," Proc.
Sympos. Pure Math. 77 (AMS, 2008). Also: Mizuno–Sato, "A new Bartholdi zeta function of a graph,"
Int. J. Algebra 1 (2007) 269–281 (edge operator `B − (1−u)J₀`).

### 1.1 The dictionary (both parts PROVED-HERE in cert check [S])

| Brief (this task) | Published (Bartholdi / Sato–Mizuno / GILa) |
|---|---|
| `u` (length/path variable) | `t` (Sato), `z` (GILa) |
| `t` (bump weight) | `u` (bump variable, all three) |
| `1 − t` | `1 − u` |
| `B` = NON-backtracking Hashimoto | `B_pub = B + R` = full head-meets-tail matrix |
| edge operator `B + tR` | `B_pub − (1−t)R` |
| `A`, `D`, `|E|=m`, `|V|=n`, exponent 326 | identical |

**Part (a) — variable transposition.** The literature's bump variable is `u` and its length variable
is `t`; the brief swaps these letters. This is a pure renaming, no sign/shift.

**Part (b) — the edge operator.** The apparent discrepancy ("published is `B_pub − (1−t)R`, brief is
`B + tR`") dissolves because the two "B"s are different matrices. The published `B_pub` includes
backtracks (head-meets-tail); the brief's/W1's `B` is non-backtracking. Numerically on the scene,
`B_pub = B + R` exactly (cert check [1]). Then

    B_pub − (1−t)R = (B + R) − (1−t)R = B + R − R + tR = B + tR      (identically).

So the published edge operator equals the brief's `B + tR`. Cert check **[S]** verifies
`det(I − u(B_pub − (1−t)R)) == det(I − u(B + tR))` at 4 rational (u,t) × 3 primes — **PASS**. The RHS
(vertex side) is already verbatim identical after the letter swap; the exponent `m−n = 326` matches.

**Verdict:** the brief's identity is the published Bartholdi determinant formula under the dictionary
above — not a sign flip, not a `t→1−t` shift. The cert implements BOTH the published edge operator and
the brief's, and proves they agree.

### 1.2 Hypotheses (SOURCED)

- **Connectivity:** G connected (assumed; exponent `m−n` counts a spanning-tree complement). K(9,11,13)
  is connected.
- **Multigraphs allowed; simple NOT required; regularity NOT required** — the whole point of the
  Bass/Bartholdi generalization; `D` carries irregularity. K(9,11,13) is simple and irregular
  (degrees 24/22/20), fully inside the hypotheses.
- **No md≥2 / min-degree hypothesis is needed for the determinant identity itself.** (A δ≥2 condition
  appears elsewhere — infinitude of primes / no trivial zeta factors — but is not a hypothesis of the
  determinant formula.) The scene's degrees are 20/22/24, so md≥2 holds anyway.

### 1.3 Bump convention (SOURCED)

A **bump** = a backtrack = an arc immediately followed by its inverse. Bartholdi Def. 2.3 and Sato
et al.: the **cyclic bump count** `cbc(C) = |{i : e_i = e_{i+1}⁻¹}|` (indices mod n). Each prime cycle
C contributes `(1 − u^{cbc(C)} t^{|C|})⁻¹` (lit. letters) = `(1 − t^{cbc} u^{|C|})⁻¹` (brief letters):
length in the exponent of the length variable, cyclic-bump-count in the exponent of the bump variable.
t=0 (brief) / u=0 (lit) → only cbc=0 cycles survive → Ihara (non-backtracking). t=1 (brief) / u=1
(lit) → no penalty for backtracks → all closed walks. Both confirmed by cert checks [2a]/[2b].

---

## 2. PROVED-HERE — exact two-variable + golden-point verification

All PASS/FAIL logic is integer/modular (no floats in decisions). Cert runtime ~2–3 min
(≈130 determinants of size 718 across primes/embeddings). Determinants: numpy int64 Gaussian
elimination mod primes ≥ 10⁹ (ordinary primes `[1000000007, 998244353, 1000000009]` for the ℚ tests;
split primes `[1000000009, 1000000021, 1000000181, 1000000241, 1000000271, 1000000289]`, each
≡ ±1 mod 5, for the ℚ(φ) tests).

| Cert check | What it proves | Result |
|---|---|---|
| [1] | invariants |V|=33,|E|=359,2|E|=718, deg (24,22,20), rank(A)=3; R is a symmetric permutation involution (R²=I); B_pub = B+R | PASS |
| [S] | published `det(I−u(B_pub−(1−t)R))` == brief `det(I−u(B+tR))` at 4 (u,t) × 3 primes (the dictionary) | PASS |
| [2] | brief's two-variable identity at **7** rational (u,t) × 3 primes, incl. t=0 (×2) and t=1 (×2) degenerations + 3 interior | PASS |
| [2a] | **t=0 leg reproduces W1's Ihara–Bass numbers BIT-FOR-BIT** at W1's 5 u × 3 primes (lhs == W1-RHS == W7-RHS all equal) | PASS |
| [2b] | **t=1 degeneration**: prefactor (1−0)^326 = 1 and RHS == det(I − uA) at 3 u × 3 primes | PASS |
| [3i] | golden closure over ℚ(φ), exact 2-component: 1−(φ−1) == (φ−1)²; φ·(φ−1)==1; p⁴==(p²)². Values: p=φ−1=−1+φ, 1−p=p²=2−φ, p⁴=5−3φ | PASS |
| [3ii] | **golden specialization** `det(I−u(B+pR)) == (1−p⁴u²)^326·det(I−uA+p²(D−p²I)u²)` at 4 u × **12 embeddings** (both φ roots) × 6 split primes | PASS |

The t=0 leg (check [2a]) uses the exact W1 RHS routine `(1−u²)^326·det(I−uA+u²(D−I))` and confirms
lhs == W1-RHS == W7-RHS as integers mod each prime — i.e. the W7 cert reproduces W1's numbers where
they overlap, bit-for-bit.

The golden ℚ(φ) verification uses **split-prime modular arithmetic**: for each prime q ≡ ±1 mod 5,
√5 exists mod q, so x²−x−1 factors and φ has two residue embeddings (1±√5)/2. The cert asserts each
embedding satisfies φ²=φ+1 and 1−p=p² mod q, then checks the golden identity at both embeddings. Holding
at 12 embeddings across 6 primes pins the identity over ℚ(φ) (Chinese-remainder + both conjugates).
Scalar ℚ(φ) facts (check [3i]) are additionally verified with exact 2-component (a+bφ) arithmetic, no
modular reduction at all.

**RESULT: PASS, exit code 0.** Full transcript reproduced in §6.

---

## 3. PROVED-HERE — negative-control matrix (step 4)

Every control is reachable and demonstrably fires (the cert would exit non-zero if any control failed
to fire). Verified by construction: each control feeds a corrupted input into the SAME identity routines.

| # | Control | Mechanism | Expected | Observed |
|---|---|---|---|---|
| (i) | **corrupted bump matrix R** | one transposition wrong: reroute edges e₀,e₁ to each other's reverse (a genuine single-swap corruption of the involution) | identity FAILS | **fires** — mismatch at tested (u,t)×primes |
| (ii) | **wrong exponent 326±1** | use `bass_exp ∈ {325, 327}` in the prefactor power | identity FAILS | **fires** — mismatch |
| (iii) | **non-golden t=3/5 claimed golden** | separates identity from specialization | golden-STRUCTURE check (1−t==t²) FALSE **while** generic identity at t=3/5 still holds | **fires** — structure=False (1−3/5=2/5 ≠ 9/25), generic identity=True |
| (iv) | **K(9,11,15)** | different scene | invariants shift AND scene exponent 326 breaks its identity | **fires** — invariants (399,798,18420,798)≠(359,718,15708,718); exponent 326 breaks K(9,11,15)'s identity while its own exponent E5−V5 works |

Control (iii) is the discriminating one demanded by the brief: it shows the *generic* Bartholdi
identity is agnostic to the value of t (holds at the arbitrary t=3/5), whereas the *golden structure*
`1−t=t²` is a separate arithmetic fact true only at t=φ⁻¹. The cert cannot conflate "the identity
holds" with "t is the golden point."

---

## 4. REPORT-ONLY — spectral / structural data (step 5)

No PASS/FAIL weight. All quantities are exact over ℚ(φ) (2-component or split-prime cross-checked);
Perron values quoted numerically for orientation only.

### 4.1 (R-a) Adjacency zone quotient = vacuum cubic (W1 finding, re-emitted)

The rank-3 adjacency spectrum equals the roots of the 3×3 zone quotient
`Q = [[0,11,13],[9,0,13],[9,11,0]]`, charpoly **λ³ − 359λ − 2574** (the §08.12.4 "vacuum cubic").
Matches W1.

### 4.2 (R-b) Golden vertex-side polynomial P(u) = det(I − uA + p²(D − p²I)u²) over ℚ(φ)[u]

Built via the **equitable 3-zone quotient**: with p²=2−φ, x_a(u) = 1 + p²(d_a − p²)u² and

    P(u) = ∏_a x_a(u)^{size_a − 1} · det N(u),
    N[a][a] = x_a(u),  N[a][b] = −size_b·u  (a≠b),

zone data (size, degree): (9,24),(11,22),(13,20), and x-coefficients (coeff of u² in x_a):
zone0: 43−21φ, zone1: 39−19φ, zone2: 35−17φ. The compressed form is **exact-verified against the full
33-dim determinant** modulo split primes (cert [R-b], both φ embeddings, u∈{1/4, 2/7, −3/5}) — proven,
not asserted. **deg P = 66.** Low-order exact coefficients (deg u : a+bφ):

    u⁰ :  1
    u² :  912 − 619 φ
    u³ : −2574              ← the vacuum-cubic constant reappears
    u⁴ :  540341 − 368337 φ

(The complete degree-66 coefficient list is deterministic output of `golden_vertex_poly(...)` in the
cert; the four low-order terms above are the load-bearing ones for comparison in §4.4.)

### 4.3 (R-c) Compressed charpoly of B_p = B + pR over ℚ(φ)

The 718 directed edges partition by type (source-zone, target-zone) into **6 classes**; this partition
is **equitable** for B_p over ℚ(φ) (cert [R-c] verifies equitability exactly). The 6×6 quotient
(rows = source type, cols = target type; entries written a+bφ; each unit of the B-count contributes 1
and one backtrack contributes p = φ−1 = −1+φ, so a raw B-count of 7 plus one backtrack reads
7+(−1+φ) = 6+φ):

|          | (0,1) | (0,2) | (1,0) | (1,2) | (2,0) | (2,1) |
|----------|-------|-------|-------|-------|-------|-------|
| **(0,1)**| 0     | 0     | 6+φ   | 13    | 0     | 0     |
| **(0,2)**| 0     | 0     | 0     | 0     | 6+φ   | 11    |
| **(1,0)**| 8+φ   | 13    | 0     | 0     | 0     | 0     |
| **(1,2)**| 0     | 0     | 0     | 0     | 9     | 8+φ   |
| **(2,0)**| 11    | 10+φ  | 0     | 0     | 0     | 0     |
| **(2,1)**| 0     | 0     | 9     | 10+φ  | 0     | 0     |

(An entry "k+φ" means the integer k plus one R-contribution p=−1+φ, i.e. the raw B-count is k+1;
e.g. (1,0)→(0,1) has B-count 9 and one backtrack, giving 9+p = 8+φ.) Its exact characteristic
polynomial over ℚ(φ), `det(λI − Q₆) = Σ c_k λ^k` (cert [R-c] output, verified by split-prime
cross-check):

    charpoly(B_p quotient) =
        λ⁶ − (242 + 57φ) λ⁴ − 2574 λ³ − (8551 − 3558φ) λ² + (93689 − 57558φ)

    [cert emits: l^6:(1)  l^4:(-242-57φ)  l^3:(-2574)  l^2:(-8551+3558φ)  l^0:(93689-57558φ)]

(coefficients of λ⁵ and λ¹ are 0). The **Perron root** of this sextic is
**21.45398338905971**, matching Perron(B_p) ≈ 21.4540 to all printed digits (the 6×6 quotient's
eigenvalues embed into spec(B_p); the sextic is the exact minimal-polynomial-over-ℚ(φ) factor carrying
the Perron root). Note the **λ³ coefficient is exactly −2574** — the vacuum-cubic constant — the same
integer that appears as the u³ coefficient of P(u) (§4.2) and as the constant of the adjacency cubic
(§4.1). Reported without interpretation.

### 4.4 Comparison table vs owned invariants (REPORT-ONLY; hit/miss, no interpretation)

| Owned invariant | Appears in W7 data? | Where | Hit/Miss |
|---|---|---|---|
| **−2574** (vacuum-cubic constant λ³−359λ−2574) | yes | λ³ coeff of B_p quotient charpoly (§4.3); u³ coeff of golden P(u) (§4.2); constant of adjacency cubic (§4.1) | **HIT** (×3) |
| **359** (=|E|; adjacency cubic λ-coeff) | as −359 in adjacency cubic (§4.1) only; NOT as a B_p-quotient or P(u) coefficient | §4.1 | partial (adjacency only) |
| **326** (=|E|−|V|, Bass exponent) | yes — the identity's prefactor exponent; control (ii) shows 326±1 breaks it | §2, §3 | **HIT** |
| **718/33** (2|E| / |V|) | 718 = size of B, R, B_p; 33 = size of A,D; both structural, verified [1] | §2 | **HIT** (as dimensions) |
| **359/160** (archive window) | NOT observed as any charpoly coefficient or Perron value in W7 | — | **MISS** |
| **Perron(A) ≈ 21.8374** | root of λ³−359λ−2574 (§4.1) | §4.1 | HIT (adjacency Perron) |
| **Perron(B) ≈ 20.8335** | untyped Hashimoto Perron (W1); not recomputed exactly here | — | (not in W7 scope) |
| **Perron(B_p) ≈ 21.4540** | top root of the exact sextic (§4.3) | §4.3 | **HIT** (pinned to exact sextic) |
| **φ⁻¹ = p, p²=2−φ, p⁴=5−3φ** | the golden weights; all exact in ℚ(φ) (§2 [3i]) | §2 | **HIT** |

No claim is attached to any HIT. The recurrence of −2574 across three unrelated ℚ(φ) polynomials is
recorded as a structural coincidence for a reviewer, nothing more.

---

## 5. Tier summary + skeptic's paragraph

**SOURCED:** the brief's identity is the published Bartholdi–Ihara–Bass determinant formula under the
two-part dictionary of §1.1 (variable transposition + B non-backtracking vs B_pub head-meets-tail);
hypotheses (connectivity; irregularity allowed; no md≥2 needed) all hold on the scene. **PROVED-HERE:**
the exact two-variable identity (7 (u,t), both degenerations, 3 primes), the t=0-reproduces-W1 leg
(bit-for-bit), the t=1 degeneration to det(I−uA), the golden closure 1−p=p² and the golden
specialization over ℚ(φ) (12 embeddings, 6 split primes), and all four negative controls — cert PASS,
exit 0. **REPORT-ONLY:** the exact golden P(u)∈ℚ(φ)[u] (deg 66, compression exact-verified), the exact
sextic charpoly of the B_p edge-type quotient (Perron pinned to 21.45398338905971), and the invariant
comparison table. **OPEN:** the T1-addendum single-ledger-vs-two-ledger typing question — whether the
refinement family must *contain* the return channel (⇒ t=p) or *composes* with a separately-carried
p²-channel (⇒ t=0) — is a corpus-level typing decision, not a computation, and is untouched by this
cert. The admissible set remains {t=0, t=p}; this cert supplies calculation legs for both.

**Skeptic's paragraph (strongest reason t=p is NOT the forced typing).** The published bump convention
makes t=p look *unnatural*, and this is the sharpest attack on X′. In Bartholdi's own normalization the
bump weight is a *formal* variable u whose canonical, structurally-motivated values are exactly the two
endpoints t∈{0,1}: t=0 (non-backtracking / Ihara, the reduced-path object) and t=1 (all closed walks,
the full-transfer object). These are the values with a *combinatorial* meaning — count reduced cycles,
or count everything. The golden value t=φ⁻¹ has **no such combinatorial meaning inside the Bartholdi
grammar**: it is not "count paths with weight-per-bump equal to the golden ratio" as anything a graph
theorist would write down; it is imported from the D0 closure equation p+p²=1 by the *external*
observation that "1−t=t²" happens to be solvable at φ⁻¹. Nothing in the Bartholdi/Sato/Mizuno
literature privileges an interior t, and the identity holds for *every* t (control (iii) proves this
explicitly — it is a polynomial identity in t, agnostic to the value). So the case for t=p rests
entirely on the *corpus-side* claim that the return step "already carries" the grammar weight p — a
claim the T1 addendum itself flags as the unresolved single-ledger-vs-two-ledger gap. If the corpus
reads history and channel as two ledgers, t=0 is forced and t=p is over-counting; if one ledger, t=p.
The cert cannot adjudicate this: it proves the golden specialization is *arithmetically exact*, not
that it is *typed-forced*. Absent the ledger decision, calling t=p "the" typing over-reads the
computation — the honest status is the two-completion set {t=0, t=p}, with t=1 (W/E) excluded by the
untyped-weight blade and every other interior t excluded only if the single-ledger reading is adopted.

---

## 6. Cert transcript

Reproduced verbatim from a clean run of `vp_scene_bartholdi_typed.py`:

```
=== W7 . Bartholdi (typed) zeta exact certificate on K(9,11,13) ===
[1] |V|=33 |E|=359 2|E|=718 degrees(zone)=(24, 22, 20) rank(A)=3 ; R perm/involution/symmetric=True/True/True
    B_pub(head-meets-tail) == B + R : True ; |E|-|V|=326 : PASS
PASS_SCENE_INVARIANTS_AND_R_INVOLUTION
[S] published det(I - u(B_pub-(1-t)R)) == brief det(I - u(B+tR)) at 4 (u,t), 3 primes : PASS
PASS_SOURCING_DICTIONARY_PUBLISHED_EQUALS_BRIEF
[2] Bartholdi det(I-u(B+tR)) == (1-(1-t)^2u^2)^326 det(I-uA+(1-t)(D-(1-t)I)u^2) at 7 (u,t) pairs (incl. t=0,t=1), mod 3 primes : PASS
PASS_BARTHOLDI_TWO_VARIABLE_IDENTITY_EXACT_MODULAR
[2a] t=0 leg == W1 Ihara-Bass det(I-uB)=(1-u^2)^326 det(I-uA+u^2(D-I)) bit-for-bit at W1's 5 u, 3 primes : PASS
PASS_T0_LEG_REPRODUCES_W1_IHARA_BASS
[2b] t=1 degeneration: prefactor (1-0)^326=1 and RHS == det(I - uA) at 3 u, 3 primes : PASS
PASS_T1_DEGENERATION_TO_DET_I_MINUS_uA
[3i] Q(phi) exact 2-component: 1 - (phi-1) == (phi-1)^2 : True ; phi*(phi-1)==1 : True ; p^4==(p^2)^2 : True
     p=phi-1=-1 + 1*phi  1-p=2 - 1*phi  p^2=2 - 1*phi  p^4=5 - 3*phi
PASS_GOLDEN_CLOSURE_1_MINUS_t_EQUALS_t_SQUARED_EXACT
[3ii] golden det(I-u(B+pR)) == (1-p^4u^2)^326 det(I-uA+p^2(D-p^2 I)u^2) at 4 u, 12 embeddings across 6 split primes : PASS
PASS_GOLDEN_SPECIALIZATION_EXACT_QPHI_SPLIT_PRIME
Negative controls (each must break the identity / detect the change):
  (i)   corrupted bump matrix R (one transposition) breaks identity : PASS(control fires)
FAIL_CORRUPTED_R_BREAKS_IDENTITY
  (ii)  wrong exponent (326 +- 1) breaks identity : PASS(control fires)
FAIL_WRONG_EXPONENT_BREAKS_IDENTITY
  (iii) non-golden t=3/5: golden-structure (1-t==t^2) holds=False (must be False); generic identity at t=3/5 holds=True (must be True) : PASS(control fires)
FAIL_NONGOLDEN_STRUCTURE_WHILE_GENERIC_PASSES
  (iv)  K(9,11,15) invariants (399, 798, 18420, 798) != scene (359,718,15708,718) : True ; scene-exponent 326 breaks its identity : True : PASS(control fires)
FAIL_K91115_INVARIANTS_AND_EXPONENT_DIFFER
Report-only (no PASS/FAIL weight): spectral / structural fingerprints
  [R-a] adjacency zone-quotient charpoly = lambda^3 +0l^2 -359l -2574 (= l^3-359l-2574) : matches vacuum cubic
  [R-b] golden P(u)=det(I-uA+p^2(D-p^2 I)u^2) exact Q(phi)[u], deg=66 ; compressed form == full 33-dim det (exact, split-prime cross-check): True
        low-order coeffs: u^0:1; u^2:912 - 619*phi; u^3:-2574; u^4:540341 - 368337*phi   (full deg-66 list in TASK_W7_REPORT.md section 4)
  [R-c] B_p=B+pR edge-type quotient is 6x6 equitable over Q(phi): True ; p=-1 + 1*phi
        charpoly(quotient) = l^6:(1)  l^4:(-242 - 57*phi)  l^3:(-2574)  l^2:(-8551 + 3558*phi)  l^0:(93689 - 57558*phi)
        (Perron(B_p) is the top root ~21.4540; the sextic is its exact min-poly-over-Q(phi) factor; l^3 coeff = -2574 = vacuum-cubic constant)
RESULT: PASS
```
