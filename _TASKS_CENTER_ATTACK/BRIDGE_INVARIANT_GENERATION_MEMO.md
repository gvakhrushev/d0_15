# BRIDGE MEMO — D0-INVARIANT-GENERATION-BRIDGE-001

**Status: POST-SKEPTIC v2 — BRIDGE-SURVIVES (WOUND repaired in full, see §6). Memo-only; registry untouched; no commit; 053040 untouched.**
**Date: 2026-07-06. Loop: d0-adversarial-forcing-loop (F1 flagship forge).**
**Compute companion: `_TASKS_CENTER_ATTACK/bridge_invariant_generation_check.py` (ALL PASS incl. `--mutate`; not a registered cert).**

---

## 0. Claim (DEF-0.2.2 form)

**CLAIM (span identity on `Fin 33`, exact over `Q`).** On the frozen scene `K(9,11,13)`
(`|V| = 33`, `Aut = S₉ × S₁₁ × S₁₃`), the following two registry objects are **the same
subspace of `ℂ³³`** — same basis `{1₉, 1₁₁, 1₁₃}`, same dimension 3, same projector:

- **(Face S — selector/extremality):** `R^Aut = (ℂ^V)^Aut`, the extremal-minimal observable
  algebra (class functions; unique minimal Aut-closed unital subalgebra separating the owned
  observables) — RAISE_SELECTOR_MINIMAL_MEMO.md, registry mint `D0-P-INVARIANT-MINIMAL-001`
  (csv:555, PROOF-TARGET).
- **(Face G — matter/generation):** the trivial-isotype multiplicity space
  `span{1₉, 1₁₁, 1₁₃}` on which the `M₃` commutant block acts — the OWNED generation space
  — W2_QUANTITY_IDENT_MEMO.md:126-128, registry rows `D0-MATTER-REP-001` (csv:51,
  CORE-FORMALIZED) and `D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` (csv:460).

**HONESTY CLAUSE (load-bearing, stated first).** Mathematically, the Aut-fixed subspace and
the trivial-isotype subspace of a permutation representation are the image of the **same
projector** — the Reynolds / orbit-averaging operator `T = (1/|G|) Σ_g P_g`. The identity is
a **definition-unfolding**, not a nontrivial theorem. The bridge's content is therefore NOT
the linear algebra; it is the **IDENTIFICATION OF READINGS**: two historically separate
registry chains (the 2026-07-05 selector campaign and the R1/W2 representation chain) each
independently constructed, named, certified and consumed this ONE 3-dimensional object under
different descriptions, and the registry currently carries no edge saying so. The can-fail
content is (i) that both memos' printed bases/dims coincide exactly as claimed (verified by
THREE independently can-fail constructions; a fourth route is entailed and not counted —
skeptic repair R1, §3), (ii) lockstep negative controls, (iii) wrong-space rejections,
(iv) mutation hardening. See §3.

**The composite physics statement (the actual claim of value):**

> The generation degrees of freedom of D0 are exactly the extremal minimal observables of
> the scene. "Three generations" and "the smallest thing an observer of `K(9,11,13)` can
> measure" are one object read twice; the zone partition `{9,11,13}` is the single owned
> root of both faces.

---

## 1. Verbatim pre-facts (all re-verified on disk 2026-07-06)

**P1 — RAISE_SELECTOR_MINIMAL_MEMO.md:35-41 (Face S definition):**
> **(T1) R^Aut is well-defined and owned.** `R^Aut` is exactly the ring of **class functions** —
> functions constant on each within-zone orbit. Since each `Sₙ` is transitive on its zone, the
> orbits are the three zones, so `dim R^Aut = #orbits = 3`. It is a unital subalgebra (spanned by the
> three orbit-indicator idempotents, closed under pointwise product and sum). Ownership is C1's own
> clause (BOOK_01:1570: "*a part-internal exception would name a privileged vertex — an exogenous
> parameter — violating M1*"; BOOK_01:1576: "*`A` is constant on the orbits of `S9 × S11 × S13`*").
> **Computed:** `dim R^Aut = 3` (`T1: dim R^Aut = #orbits`), independent Reynolds-image rank `= 3`

**P2 — W2_QUANTITY_IDENT_MEMO.md:126-128 (Face G identification):**
> - the M₃ factor acts on **span{1₉, 1₁₁, 1₁₃}** — the trivial-isotype multiplicity space, which is
>   the OWNED generation space (P1: "generation count 3 = trivial-isotype multiplicity";
>   P2: "Matter generation multiplicity is exactly three").

**P3 — CLAIM_TO_LEAN_MAP.csv:51 (`D0-MATTER-REP-001`, CORE-FORMALIZED, LEAN_PROVED):**
> Matter generation multiplicity is exactly three.
> (Lean: `Matter.matter_rep_generation_multiplicity_three`, `09_LEAN_FORMALIZATION/D0/Matter/GenerationMultiplicity.lean:16`.)

**P4 — CLAIM_TO_LEAN_MAP.csv:460 (`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`):**
> [ROOT R1] Aut(K(9,11,13))=S9xS11xS13 perm rep on C^33: isotypes (mult 3,1,1,1; dims
> 1,8,10,12), carrier 33, commutant dim Sum m^2 = 3^2+1+1+1 = 12. The generation count 3 =
> trivial-isotype multiplicity is RANK-ONLY: commutant block 9>1 (GL(3) basis freedom) =>
> Weyl-role assignment unforced (>=2 admissible).

**P5 — CLAIM_TO_LEAN_MAP.csv:555 (`D0-P-INVARIANT-MINIMAL-001`, PROOF-TARGET):**
> POSITIVE extremality principle (script-certified; Lean-lift owner-gated -> PROOF-TARGET,
> not LEAN_PROVED). THEOREM (cert-grade, 21/21 mutation-tested): on the frozen scene
> K(9,11,13), R^Aut = (C^V)^Aut (the class functions) is the UNIQUE MINIMAL observ[able algebra …]

**P6 — BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md:182 (R1 in the book):**
> The `Aut`-rep on `ℂ³³` has commutant dim `3²+1+1+1=12`; the generation count 3 is the
> trivial-isotype multiplicity (rank-only, `GL(3)` basis freedom), so the Weyl-role assignment
> is unforced

**P7 — BOOK_04:542 (independent generation-count routes, cited for context only):**
> **Why exactly three, two forced routes.** Three generations are forced by the toral trace
> `|Tr(T^2)|=3` plus the torus-shell non-commuting selector (`phason_strain_forces_three_generations`). …

**Preflight (duplication):** `grep -c "INVARIANT-GENERATION" CLAIM_TO_LEAN_MAP.csv` → **0**;
no registry row or cross-ref connects `D0-P-INVARIANT-MINIMAL-001` to the generation space.
The 2026-07-06 RAISE wave added "corollary-of D0-P-INVARIANT-MINIMAL-001" edges to many
rows (e.g. csv:39, 312, 549) but **NOT to csv:51 or the generation-space reading of csv:460**
(csv:460's RAISE edge points at `D0-P-M1-SATURATION-001`, the commutant-maximality face —
a different parent). The bridge is not minted anywhere. Confirmed.

---

## 2. The two derivation chains, side by side

| | **Face S (selector/extremality)** | **Face G (matter/generation)** |
|---|---|---|
| Historical origin | 2026-07-05 selector-mechanism search: 4 no-go arms (equivariant / SSB / dynamical / basepoint), csv:549 | ROOT R1 representation audit + W2 quantity-identification, csv:460 / csv:51 |
| Construction | `R^Aut = (ℂ^V)^Aut`, fixed-point subalgebra of the observable algebra | trivial-isotype component of the perm rep; multiplicity space the `M₃` commutant block acts on |
| Why 3 | `dim = #orbits`; each `Sₙ` transitive on its zone ⇒ orbits = zones ⇒ 3 | isotype multiplicities (3,1,1,1); trivial multiplicity = 3 = generation count |
| Basis | the three orbit-indicator **idempotents** `1₉,1₁₁,1₁₃` (algebra structure) | `span{1₉,1₁₁,1₁₃}` as printed in W2:126 (module structure under the commutant) |
| Certification | `raise_selector_minimal_check.py` 21/21; mint csv:555 PROOF-TARGET | Lean `matter_rep_generation_multiplicity_three` (LEAN_PROVED — but proves card = 3 via the defect/branchRay route, NOT via isotypes); `w2_quantity_ident_check.py` |
| Grade caveat (skeptic R4) | extremality is script-grade; Lean lift owner-gated (csv:555) | `FinitePathRepresentation`'s isotype list `(3,1,1,1)` is DECLARED, not derived, in Lean; the trivial-isotype IDENTIFICATION of the generation space is script-grade (W2). Face G's LEAN_PROVED covers the count 3, not the isotype reading |
| Role in corpus | positive face of the within-zone-selector NO-GO; parent of 20+ RAISE edges | "exactly three generations" — the flagship matter count |
| Common root | **the zone partition of `K(9,11,13)`** (BOOK_01:1576 orbital theorem) | **the same zone partition** |

Both chains root in the SAME owned fact (orbits = zones). "Historically independent" means
**separately built and certified registry chains**, not logically independent axiom sets —
the bridge's value is exactly that it makes the common root explicit and puts the missing
edge in the registry.

---

## 3. Compute results (`bridge_invariant_generation_check.py`, ALL PASS + `--mutate` clean)

**THREE independently can-fail constructions** of the candidate space, all exact over `Q`
(count demoted from four per skeptic repair R1):

- **Route A** (Face S as printed): span of the zone-indicator vectors.
- **Route B** (group-theoretic): exact nullspace of the stacked constraints `f(g·v) = f(v)`
  over the 30 within-zone adjacent-transposition **generators** of `S₉×S₁₁×S₁₃` (each
  verified to be an automorphism of `A`; fixed-under-generators = fixed-under-group).
- **Route D** (Face G, commutant): the 9 zone-block pair-orbit matrices of the commutant
  each preserve the indicator span, and their restrictions span the FULL `M₃` (rank 9) —
  the W2 "`M₃` acts on span{1₉,1₁₁,1₁₃}" sentence recomputed from scratch.

**Route C (kept, NOT counted as independent — R1):** image of the Reynolds projector `T`
built from the **generator-derived orbits** (union-find). Given the separately checked
partition identity "orbits = zones", `span C = span A` is ENTAILED, so route C restates
the partition identity rather than adding a fourth independent test; its
idempotence/symmetry/commutation lines are implementation checks. The partition-identity
line itself (orbits computed from generators = zones) IS a real check and stays.

**Results on `K(9,11,13)`:** dim A = dim B = dim C = 3; span A = span B = span C (exact;
A=B and B=D-invariance independent, A=C entailed per above); basis is exactly
`{1₉,1₁₁,1₁₃}` (disjoint 0/1 supports of sizes 9/11/13); restricted commutant block =
full `M₃` (rank 9).

**Negative controls:**
- **Lockstep (zone-count ≠ 3):** `K(9,11)` → both faces dim 2; `K(2,3,4,5)` → both faces
  dim 4; the identity persists, the **3 does not** — the "three" comes from the frozen
  scene, never from the bridge.
- **Repeated sizes:** `K(3,3,5)` + zone-swap generator → orbits ≠ zones (2 orbits vs 3
  zones); BOTH group-derived faces collapse to dim 2 in lockstep; the per-listed-zone
  indicator span is strictly bigger than the fixed space. Distinct zone sizes are
  load-bearing for "basis = zone indicators".
- **Wrong-space:** a transversal section `{e_{v₀}}` (dim 3 but not Aut-invariant, ≠ the
  bridge space) REJECTED; a mean-zero standard-isotype vector lies outside the space and is
  annihilated by `T`.
- **Mutations (5/5 caught):** partial generating set inflates the fixed space (dim 25);
  corrupted Reynolds loses idempotence; cross-zone transposition rejected as automorphism;
  wrong dim claim on 4-zone scene; corrupted indicator breaks span equality.

One forge-time bug is itself evidence: the first draft built `T` by averaging over **zones**
and the `K(3,3,5)`-swap control caught it (zone-averaging ≠ group Reynolds when zones ≠
orbits). The repaired script derives orbits from the generators; "orbits = zones" on the
real scene is now an explicit PASS line, which is precisely the single owned root of §2.

---

## 4. Consequences (what the bridge adds, and what it does NOT)

**C1 (parent edge).** The generation count 3 acquires the extremality parent
`D0-P-INVARIANT-MINIMAL-001`: "exactly three generations" = "the extremal-minimal observable
algebra has dimension 3". Registry motion: corollary-of cross-refs on csv:51 and csv:460
(texts in §7). Status arithmetic is conservative: csv:555 is PROOF-TARGET, so the bridge
row must be PROOF-TARGET (an identity consuming a PROOF-TARGET face cannot outrank it);
csv:51's LEAN_PROVED status is untouched.

**C2 (single root).** The zone partition is the single owned root of both faces; the two
chains are two READINGS of it. This dissolves an implicit double-count risk: any future
argument using "dim R^Aut = 3" AND "3 generations" as two independent confirmations of the
scene would be counting one object twice. The bridge row makes that illegal.

**C3 (composite physics reading, R2+R3-repaired).** With the identity in place, the
selector face's extremality transfers to the generation space verbatim: *the generation
space is the unique minimal Aut-closed observable algebra — the smallest thing an observer
of the scene can measure — and a ZONE-AXIS generation index is a class function* (the
physical e/μ/τ-role labeling of the axes remains external,
`PRIM-FINITE-SPECTRAL-TRIPLE-REP`). Measuring "which zone-axis generation slot" IS
measuring the coarsest invariant observable. **Ownership inheritance (R2, RR-1/RR-2 of
csv:549/555):** this sentence is owned exactly as far as csv:555 is owned — the universal
no-proper-refinement leg is outsourced to the LEAN_PROVED no-section theorem
(`canonical_within_zone_selector_nogo`), while class-function-universality
("every owned functional is a class function") is EVIDENCE-grade with row-549 scope
(RR-1 single-witness refinement clause, RR-2 inherited EVIDENCE scope). The bridge
inherits, never upgrades, that grading. This is the flagship sentence; it is a
READING of the identity, owned exactly as far as csv:555's extremality theorem is owned
(cert-grade, Lean-lift gated).

**C4 (what the bridge must NOT and does NOT force — pre-registered):**
- **Weyl-role assignment stays unforced** (csv:460: `GL(3)` basis freedom, ≥2 admissible).
  The bridge is a statement about the SPACE, not about a physical-role labeling of its
  axes. Subtlety confronted head-on: Face S is an ALGEBRA and an algebra's minimal
  idempotents are canonical — so doesn't the bridge canonically frame the generation space
  and contradict "role unforced"? **No, and this is already owned:** the canonical
  idempotent axes are exactly the degree-typed zone axes (24/22/20), i.e. the W2
  typed-collapse (degree centralizer cuts the `M₃` block dim 9 → dim 3 zone-diagonal;
  W2_QUANTITY_IDENT_MEMO "Typed-collapse consistency"). What remains unforced is the map
  from PHYSICAL Weyl roles (e/μ/τ, up/down towers) to those zone axes — the missing object
  is still `PRIM-FINITE-SPECTRAL-TRIPLE-REP` and the bridge does not touch it.
- **No new generation-count derivation.** The lockstep controls prove the identity is
  scene-generic (`#orbits`-dim on ANY `K(sizes)` with distinct sizes); "three" is owned by
  the frozen scene (csv:51, BOOK_04:542 routes), not by the bridge.
- **No status uplift anywhere.** No row changes status; the bridge only adds edges + one
  new PROOF-TARGET row.

---

## 5. Pre-registered attack surface

- **A1 (STRONGEST — triviality).** "Is this an IDENTITY of one object or a trivial
  isomorphism of two? 'Fixed space = trivial isotype' is a textbook definition-unfolding;
  two names for one definition is not a discovery. And is 'same subspace' physics or
  bookkeeping?" — **Confronted in §0 honesty clause:** the linear algebra is admitted
  trivial; the claimed content is (a) the registry EDGE that is verifiably absent
  (preflight: 0 hits), (b) the composite reading C3 (extremality transfers to generations),
  (c) the double-count prohibition C2. If the skeptic judges (a)-(c) to be word-dressing,
  the honest verdict is KILLED-AS-TRIVIAL with the residue "add two cross-ref lines" — that
  outcome is explicitly on the table.
- **A2 (over-claim: generation physics).** Any import of mass ratios, mixing, Weyl roles,
  or a new "why 3" derivation is an over-read. Guarded by C4; skeptic to verify no such
  sentence survives.
- **A3 (hidden forcing via canonical idempotents).** Does the algebra face smuggle a
  canonical generation frame past csv:460's `GL(3)`-freedom no-go? Resolved in C4 via the
  owned typed-collapse; skeptic to check the resolution is real, not verbal.
- **A4 ("historically independent" wording).** Both chains share the BOOK_01:1576 root, so
  "independent derivations" must mean "separately built registry chains", never "logically
  independent". §2 words it that way; skeptic to kill any stronger phrasing.
- **A5 (scene-generality).** The identity holds on any `K(sizes)`; a reader must not come
  away thinking extremality alone forces 3. Guarded by the lockstep controls + C4.
- **A6 (source fidelity).** Both memo quotes, three csv rows, and the BOOK_04 lines to be
  re-verified verbatim ±10 lines by the independent skeptic.

---

## 6. Skeptic pass — INDEPENDENT (§05.8.R) — COMPLETED 2026-07-06

**Verdict: WOUND (repairable), NO-KILL on the core.** Triviality ruling (A1): the bridge
survives as a **registry-edge mint at PROOF-TARGET, "identity-of-readings"** — correctly
priced by the §0 honesty clause; not KILLED-AS-TRIVIAL. Source chains verified verbatim
±10 (A6 clean); script runs ALL PASS + 5/5 mutations. Four repairs mandated, ALL ACCEPTED
and applied in this revision:

- **R1 (over-count of independence).** "Four operationally different constructions" demoted:
  `span C = span A` is ENTAILED by the separately checked partition identity orbits = zones
  (route C restates it); T-idempotence/symmetry are implementation checks. Honest independent
  can-fail count = **THREE** (A, B, D). Applied: §0, §3, script docstring.
  **R1b:** script docstring "historically independent registry objects" → "separately built
  and certified registry objects" (the memo's own §2/A4 standard). Applied.
- **R2 (inheritance not named).** The flagship sentence in M1 + §8 must NAME the RR-1/RR-2
  inheritance from csv:555 explicitly: owned exactly as far as csv:555 is owned — universal
  no-proper-refinement outsourced to the LEAN_PROVED no-section theorem
  (`canonical_within_zone_selector_nogo`); class-function-universality EVIDENCE-grade,
  row-549 scope. Applied: §4 C3, §7 M1, §8.
- **R3 (role-labeling precision).** "a generation index is a class function" → "a ZONE-AXIS
  generation index is a class function (physical e/μ/τ-role labeling remains external,
  `PRIM-FINITE-SPECTRAL-TRIPLE-REP`)". Applied: §4 C3, §7 M1, §8.
  **R3b:** pre-register in §9 that the Lean `gens` must be a LITERAL permutation list, not
  derived from `zoneOf` (else `P = Q` becomes definitionally circular). Applied: §9.
- **R4 (Face G Lean-grade honesty).** csv:51's Lean proves card = 3 via the defect/branchRay
  route; `FinitePathRepresentation`'s isotype list `(3,1,1,1)` is DECLARED, not derived, in
  Lean; the trivial-isotype IDENTIFICATION of the generation space is script-grade (W2). No
  LEAN_PROVED over-read of Face G. Applied: §2 table (grade-caveat row), §7 M1.

---

## 7. Proposed registry motions (NOT applied; for a later guarded integration)

**M1 — mint (new row, PROOF-TARGET; post-R1/R2/R3/R4 text):**
> `D0-INVARIANT-GENERATION-BRIDGE-001,BOOK_04,04.R1 bridge,,,OPEN,False,,bridge_invariant_generation_check.py,PROOF-TARGET,"[F1 flagship bridge 2026-07-06, skeptic-repaired] IDENTITY OF READINGS: the OWNED generation space (trivial-isotype multiplicity space span{1_9,1_11,1_13} the M3 commutant block acts on; D0-MATTER-REP-001, D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001, W2_QUANTITY_IDENT_MEMO:126-128) IS the extremal-minimal observable algebra R^Aut = (C^V)^Aut (D0-P-INVARIANT-MINIMAL-001, RAISE_SELECTOR_MINIMAL_MEMO T1-T3): same subspace of C^33, same basis {1_9,1_11,1_13}, dim 3, same Reynolds projector. HONESTY: fixed-space = trivial-isotype is a definition-unfolding (one projector); the content is the identification of two separately built and certified registry chains + the composite reading: the generation degrees of freedom are exactly the extremal minimal observables of the scene -- a ZONE-AXIS generation index is a class function (physical e/mu/tau-role labeling stays external, PRIM-FINITE-SPECTRAL-TRIPLE-REP). INHERITANCE (RR-1/RR-2): the composite reading is owned exactly as far as D0-P-INVARIANT-MINIMAL-001 is owned -- universal no-proper-refinement outsourced to LEAN_PROVED canonical_within_zone_selector_nogo; class-function-universality EVIDENCE-grade, row-549 scope; the bridge inherits, never upgrades, that grading. Face G Lean-grade honesty: csv:51 Lean proves card=3 via the defect/branchRay route; the isotype list in FinitePathRepresentation is declared not derived; the trivial-isotype identification is script-grade (W2). Verified: 3-independent-route coincidence (indicator span / generator-fixed nullspace / commutant M3-block invariance; Reynolds route kept but entailed by the checked orbits=zones partition identity) + lockstep (zone-count != 3 moves both faces together) + repeated-size collapse + wrong-space controls, mutation-tested 5/5 (bridge_invariant_generation_check.py). Does NOT force Weyl-role assignment (GL(3) freedom intact; canonical idempotent axes = owned W2 typed-collapse zone axes); does NOT re-derive the count 3 (scene-generic identity; 3 owned by the frozen scene). Status tied to D0-P-INVARIANT-MINIMAL-001 (PROOF-TARGET; Lean lift = projector identity P=Q on Fin 33, native_decide-able, gens as LITERAL permutation list not derived from the zone map)."`

**M2 — cross-ref append on csv:51 (`D0-MATTER-REP-001`), note-field suffix:**
> ` BRIDGE[2026-07-06]: the generation space IS the extremal-minimal observable algebra R^Aut (D0-INVARIANT-GENERATION-BRIDGE-001, corollary-of D0-P-INVARIANT-MINIMAL-001): one owned 3-dim object read twice (matter-generation face / selector-extremality face); count 3 unchanged and still owned here.`

**M3 — cross-ref append on csv:460 (`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`), note-field suffix:**
> ` BRIDGE[2026-07-06]: the trivial-isotype multiplicity space span{1_9,1_11,1_13} = R^Aut, the extremal-minimal observable algebra (D0-INVARIANT-GENERATION-BRIDGE-001); the GL(3)/Weyl-role freedom of this row is UNTOUCHED (canonical idempotent axes = the owned typed-collapse zone axes; the physical-role map remains missing PRIM-FINITE-SPECTRAL-TRIPLE-REP).`

---

## 8. BOOK_04 block draft (≤15 lines, for §04.R1 vicinity; NOT applied)

```markdown
**[THE 04.R1-B] The generation space IS the minimal observable algebra [bridge].**
The OWNED generation space — the trivial-isotype multiplicity space `span{1₉,1₁₁,1₁₃}`
the `M₃` commutant block acts on (Root R1, `D0-MATTER-REP-001`) — and the extremal-
minimal observable algebra `R^Aut = (ℂ^V)^Aut` (`D0-P-INVARIANT-MINIMAL-001`) are ONE
subspace of `ℂ³³`: same basis, dim 3, same Reynolds projector
(`D0-INVARIANT-GENERATION-BRIDGE-001`). The identity is a definition-unfolding (fixed
space = trivial isotype); the content is the identification of two separately certified
chains and the composite reading: *the generation degrees of freedom are exactly the
smallest thing an observer of the scene can measure — a zone-axis generation index is a
class function* (e/μ/τ-role labeling external, `PRIM-FINITE-SPECTRAL-TRIPLE-REP`). Owned exactly as far as csv:555: no-proper-refinement
rests on LEAN_PROVED `canonical_within_zone_selector_nogo`; class-function-universality is
EVIDENCE-grade (row-549 scope, RR-1/RR-2). The zone partition is the single owned root of
both faces — "dim R^Aut = 3" and "3 generations" as two confirmations counts one object
twice. Nothing new forced: count 3 owned by the frozen scene; Weyl-role assignment stays
unforced (`GL(3)` freedom; idempotent axes = the owned typed-collapse zone axes).
```

---

## 9. Lean statement draft (F4; span equality on Fin 33, decide/native_decide route)

Two faces built by genuinely different Lean constructions, then a decidable matrix identity:

```lean
-- D0/Foundation/InvariantGenerationBridge.lean  (draft; not in-tree)
namespace D0.Foundation.InvariantGenerationBridge

def zoneOf (v : Fin 33) : Fin 3 :=
  if v.val < 9 then 0 else if v.val < 20 then 1 else 2

def zoneSize : Fin 3 → ℚ := ![9, 11, 13]

/-- Face G: the generation-space projector, written from the W2 indicator basis:
    Q = Σ_z (1/|z|) · 1_z 1_zᵀ. -/
def Q : Matrix (Fin 33) (Fin 33) ℚ :=
  fun i j => if zoneOf i = zoneOf j then (zoneSize (zoneOf i))⁻¹ else 0

/-- The 30 within-zone adjacent transpositions — a generating set of Aut(K(9,11,13)). -/
def gens : List (Equiv.Perm (Fin 33)) := ...  -- explicit list of Equiv.swap i (i+1)

/-- Face S: the Reynolds projector, built from the generator list by computable
    orbit closure (union-find on Fin 33), NOT from the zone map. -/
def P : Matrix (Fin 33) (Fin 33) ℚ := reynoldsOfGens gens

/-- THE BRIDGE: one projector, two constructions. -/
theorem invariant_generation_bridge : P = Q := by native_decide

theorem bridge_rank_three : Matrix.trace Q = 3 := by native_decide

theorem bridge_projector : Q * Q = Q ∧ Qᵀ = Q := by native_decide

/-- Equivariance: every generator's permutation matrix fixes the projector. -/
theorem bridge_equivariant :
    ∀ g ∈ gens, (permMatrix g) * Q = Q * (permMatrix g) := by native_decide
```

Notes: all four statements are finite rational-matrix identities ⇒ `native_decide`-able
(33×33 over ℚ; `decide` likely too slow, `native_decide` fine — same pattern as
`ToralSeedMarkovMaximalityNoGo`; `Matrix (Fin 33) (Fin 33) ℚ` precedent in-tree:
`CLightconePercolationOwner.lean:94`, `BoundaryRankLocalization.lean:73`,
`Signature31Split.lean:52`). The span-equality reading: `P = Q` + `trace = 3` +
idempotence gives "image P = image Q = a 3-dim space" without quantifying over ℚ-vectors.
The two-faces honesty survives in Lean: `Q` is defined from the zone map (Face G verbatim),
`P` from the generator list via orbit closure (Face S); their equality is the checked fact.

**Pre-registered anti-circularity constraint (skeptic R3b, binding on the F4 lift):**
`gens` MUST be a LITERAL list of 30 explicit `Equiv.swap` permutations (hard-coded indices
0-7, 9-18, 20-31 adjacent pairs), NOT generated by any function that consults `zoneOf` or
the zone boundaries. If `gens` were derived from `zoneOf`, `P = Q` would be definitionally
circular (both faces computed from the same zone datum) and the two-construction content
would evaporate. The reviewer of the lift must check this by inspection of the `gens`
definition; a mutation guard (perturb one literal index across a zone boundary ⇒ `P ≠ Q`)
should accompany the file, mirroring script mutation m5.

---

## 10. Verdict

**BRIDGE-SURVIVES** (independent skeptic: WOUND repairable, NO-KILL on the core; all 4
repairs R1/R1b/R2/R3/R3b/R4 applied in full in this revision; script re-run post-repair:
ALL PASS + 5/5 mutations).

**The honest content statement (final form):** the linear identity "Aut-fixed subspace =
trivial-isotype subspace" is a definition-unfolding — one Reynolds projector, one
3-dimensional subspace of `ℂ³³` with basis `{1₉,1₁₁,1₁₃}`. What the bridge mints is the
**identity of readings**: two separately built and certified registry chains (selector-
extremality face csv:555; matter-generation face csv:51/460) name this ONE object, and the
registry carried no edge saying so (preflight 0 hits). Consequences owned at PROOF-TARGET,
inheriting csv:555's grading (RR-1/RR-2): (1) the generation count 3 acquires the
extremality parent; (2) the zone partition is the single owned root of both faces —
double-counting "dim R^Aut = 3" and "3 generations" as independent confirmations becomes
illegal; (3) the composite reading: the generation degrees of freedom are exactly the
extremal minimal observables of the scene — a zone-axis generation index is a class
function; the physical e/μ/τ-role labeling remains external
(`PRIM-FINITE-SPECTRAL-TRIPLE-REP`), the `GL(3)`/Weyl-role freedom of csv:460 untouched,
and the count 3 remains owned by the frozen scene, not by the bridge.

**Deliverables:** mint M1 + cross-refs M2/M3 (§7, post-repair texts); BOOK_04 block (§8,
15 lines); Lean F4 statement (§9, with the R3b literal-`gens` constraint). Registry via a
later guarded integration only; nothing applied here; 053040 untouched; no commit.
