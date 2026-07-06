# DEEP SYNTHESIS PASS — batch M — LEPTON-DECIMAL family

Scope: genuine per-no-go synthesis (NOT a cluster tag). Five no-gos, each a worked verdict.
Method: d0-adversarial-forcing-loop (depth-emphasis). Compute-first; verbatim citations verified on disk.
Hard rules honored: 053040 untouched; no commit; no registry/book edits (row-notes PROPOSED only).

Date: 2026-07-06. Certs re-run this pass: 4/4 PASS (see §7).

---

## 0. Preflight — verbatim decisive statements (file:line, verified on disk)

The five prompt-named no-gos resolve to these registry rows and Lean/cert owners. Two of the five
(RAW-GRAPH-COEFFICIENT, RAW-SELF-READING) are general/track-II owners; three are the sharp objects.

| # | claim_id | status | cert | Lean owner |
|---|---|---|---|---|
| N1 | `D0-LEPTON-DECIMAL-MASS-RATIOS` | NO-GO | (none, Lean-only) | `D0.Integration.V15.BranchAudit.mass_ratio_underdetermined` |
| N2 | `D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001` | NO-GO | `vp_lepton_raw_graph_coefficient_nogo.py` | (cites LeptonBranchAssignmentNoGo + LeptonPuiseuxUniquenessObstruction) |
| N3 | `D0-BARE-GRAPH-DECIMAL-NOGO-001` | NO-GO | `vp_bare_graph_decimal_nogo.py` | (cert-only) |
| N4 | `D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001` | NO-GO | `vp_lepton_branch_fixing_operator_nogo.py` | `D0.Extensions.LeptonBranchFixingNoGo.lepton_branch_fixing_operator_nogo` |
| N5 | `D0-RAW-SELF-READING-EXTRACTIONS-001` | NO-GO | `vp_raw_grading_no_manual_signature.py` | `D0.SelfReading.RawSelfReadingExtractions.extraction_grading_G2` (+ L3, C4, P3) |

**N1 decisive** (`09_LEAN_FORMALIZATION/D0/Integration/V15/BranchAudit.lean:70-73`), verbatim:
> "**D is a NO-GO.** The Vandermonde determinant at `{0,1/4,1/3}` is nonzero (`1/144`), so the quadratic
> interpolation map is onto: every target `(r_μ, r_τ)` is realized by a smooth positive matching function. The
> exponents do not determine the mass ratios." … `theorem mass_ratio_underdetermined : vandermonde.det = 1/144 ∧ vandermonde.det ≠ 0`
> Missing owner (line 28): `PRIM-EFT-IR-MATCHING-FUNCTIONAL`.

**N2 decisive** (`05_CERTS/vp_lepton_raw_graph_coefficient_nogo.py:3-9` docstring), verbatim:
> "the frozen raw graph forces only the structural SKELETON — integer Lucas part L11+L4 = 206 …, depth-exponent
> row (0, 1/4, 1/3) … finite Green resolvent det(I - z U_eff) = (1 - z^4)(1 - z^3), order lcm(4,3) = 12 … but
> NOT the lepton mass COEFFICIENT … underdetermined over the FULL frozen-resolvent-invariant class."
> Registry (`CLAIM_TO_LEAN_MAP.csv:306`): "EXACT-MISSING: PRIM-LEPTON-BRANCH-FIXING-OPERATOR (provably absent from
> frozen data: 2 orbits < 3 generations)."

**N3 decisive** (`05_CERTS/vp_bare_graph_decimal_nogo.py:2-13` docstring), verbatim:
> "A raw finite graph operator cannot DIRECTLY output the 17-digit charged-lepton decimal rows without importing
> an external EFT/IR matching catalogue (M1-forbidden). … r_mu = 3.8814328681047283 is NOT such a scene invariant
> … it RECONSTRUCTS the measured charged-lepton mass ratio (it is PDG-mass-derived, an EFT/IR-matched decimal).
> … The EFT/IR matching convention … is the EXACT external datum the direct extraction needs."

**N4 decisive** (`09_LEAN_FORMALIZATION/D0/Extensions/LeptonBranchFixingNoGo.lean:57-62`), verbatim:
> "The frozen shell-torus supplies exactly `numBranches = 2` orbit-branches for `numGenerations = 3` generations,
> and has no fixed point … By cardinality there is no injection `Gen(3) ↪ Branch(2)`, no surjection
> `Branch(2) ↠ Gen(3)`, and no bijection `Branch(2) ≃ Gen(3)`. Therefore no branch→generation full-row operator is
> constructible from the frozen 2-orbit data: `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` must be an external primitive."

**N5 decisive** (`09_LEAN_FORMALIZATION/D0/SelfReading/RawSelfReadingExtractions.lean:11-15` + `35-40`), verbatim:
> "For each front the FORCED part is a raw graph invariant and the DISPUTED part remains a two-completion …
> II-C lepton → **L3** (swap-invariant)." — `extraction_lepton_L3 : (1/4:ℚ) ≠ 1/3 ∧ orbitSizes.length < numGenerations`.
> Registry (`CLAIM_TO_LEAN_MAP.csv:485`): "II-C lepton L3 (forced 1/4!=1/3; disputed 2 orbits<3, swap-invariant) …
> Each: forced part raw, disputed part two-completion."

---

## 1. The organizing frame this family sits in (verified, not manufactured)

Per `TORSOR_GAUGE_SYNTHESIS_MEMO.md` (v2.1, post-skeptic-#2) the import ledger is four-typed
**A / B(meas·adj·ext) / C / D**, and the lepton branch objects are ALREADY typed there:

- **Assignment half** (which order-12 perm σ realizes the shell-torus) → **class C / Continent 1**
  (`memo:208, 255`): S₇-conjugation point-choice on the OWNED shell-torus torsor; σ_A ~ σ_B are conjugate
  (explicit h), same order 12, same resolvent invariants — **no class-A invariant moves** ⇒ gauge-fixing,
  "cannot be wrong," contentless.
- **Counting half** (2 branches < 3 generations) → **Continent 3** existence wall (`memo:280`):
  "2 branches < 3 generations — empty admissible set for the third branch."
- The parallel **BRANCH-CP-READOUT** (V15 WP-B) was re-filed **B-ext / Continent 2** (`memo:266`) because
  "same marginals, different coherence" IS an invariant-content difference (missing PRIM-BRANCH-ISOTROPIC-READOUT).

This is the decisive lens for all five: the win is not a decimal derivation (the over-claim the owner
rejects) but the **sharp split** between what the graph OWNS (integers/structure, class A) and what it
IMPORTS (the matching functor / the branch-fixing row, class B-ext or a Continent-3 wall).

---

## 2. Worked verdicts (one per no-go)

### N4 — D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001 (the sharpest object; do it first)

The prompt flags this as the sharpest missing-object spec. Ladder:

- **(a) LIFT.** Can `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` be built from frozen data? NO — proven by the
  Lean pigeonhole (`lepton_branch_fixing_operator_nogo`, all clauses `decide`): `numBranches=2`,
  `numGenerations=3`, `sigmaShell` has no fixed point, and there is no injection/surjection/bijection between
  `Fin 3` and `Fin 2`. Cert `vp_lepton_branch_fixing_operator_nogo.py` 6/6 PASS this pass. LIFT IMPOSSIBLE by
  cardinality — this is the strongest possible negative and it is airtight.
- **(b) CLOSE — is the operator owned anywhere? Read past-citations ±10.** Swept all 122 repo mentions of the
  primitive. Result: **1 FORCED-tag** and **4 "owned"** hits are the SHELL-TORUS / exponent-SET being owned
  (4→1/4, 3→1/3, the resolvent, the (4,3) type), never the branch→generation ROW. Every hit tagged against the
  ROW is MISSING / EXTERNAL / HYP / POSTULATED / absent (`FIVE_PRIMITIVE_COMPLETION_BOARD.csv:L`,
  `CLAIM_MAP:463,471,485,491,498`). NOT owned. CLOSE fails — correctly.
- **(c) DECOMPOSE.** The object splits cleanly (this is the real synthesis content):
  1. **Orbit-keyed exponent selector** (4→1/4, 3→1/3, 1/4≠1/3) — **OWNED, class A**, branch-sensitive WITHOUT
     post-hoc group narrowing (orbit sizes are intrinsically distinct; `extraction_lepton_L3` first conjunct).
  2. **Assignment half** (which of the 420 order-12 (4,3)-type perms) — **class C / Continent 1**, gauge-fixing,
     contentless (σ_A ~ σ_B conjugate). B_row ("point 0 in the size-4 orbit") is one bit of C(7,4)=35, NECESSARY
     but not sufficient (passes 240/420, not 1) — `D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001` (csv:516).
  3. **Counting half** (2 orbits < 3 generations, no third in-carrier branch) — **Continent-3 existence wall**;
     the electron index-0 branch is genuinely external (no fixed point). This is the IRREDUCIBLE residue.
- **(d) GENUINE-BOUNDARY + exact external import.** The boundary is EXACT: the branch→generation full row is
  a **B-ext new primitive** (Continent-3 for the third-branch half, class C for the assignment half). Exact
  external import = **PRIM-LEPTON-BRANCH-FIXING-OPERATOR = the full orbit-labeling C(7,4)=35→1** (of which B_row
  is 35→20, one bit). It is provably non-constructible internally (2<3). This is the honest terminal.

**VERDICT N4:** SOLID NO-GO, sharpest object in the family. Owned = orbit-keyed exponent selector (class A) +
the shell-torus torsor. External = the branch→generation row (C(7,4)=35→1), split Continent-1-C (assignment) +
Continent-3 (third-branch existence). No repair needed; the row's 2026-07 PR-fix already promoted PROOF-TARGET→NO-GO.

### N1 — D0-LEPTON-DECIMAL-MASS-RATIOS (v15 WP-D; the decimals themselves)

- **(a) LIFT.** Can the finite branch class force `(r_μ, r_τ)`? NO — `mass_ratio_underdetermined` proves the
  Vandermonde at {0,1/4,1/3} is invertible (det = 1/144 ≠ 0, `native_decide`), so the quadratic interpolation is
  ONTO: EVERY target pair is realized by a smooth positive matching function. The exponents impose ZERO constraint
  on the ratios. **Independently recomputed this pass** (fractions, exact): det = 1/144, product form
  (1/4−0)(1/3−0)(1/3−1/4) = 1/144. LIFT IMPOSSIBLE — the onto-ness is the *reason* it can't be lifted.
- **(b) CLOSE.** Is `PRIM-EFT-IR-MATCHING-FUNCTIONAL` owned? NO. It is the same object as
  `ASSUMP-EFT-IR-MATCHING-SCHEME` (D0-LEPTON-002) / the EFT/IR functor named across csv:309,320,321,339. Class B-ext.
  Not owned; CLOSE fails correctly.
- **(c) DECOMPOSE.** Structure vs value: the exponent ROW (0,1/4,1/3) is exact THE (owned); the achievable-ratio
  SET is all of ℝ²₊ (unconstrained). The two are orthogonal — no partial credit leaks from row to value.
- **(d) GENUINE-BOUNDARY.** Exact import = `PRIM-EFT-IR-MATCHING-FUNCTIONAL` (the renormalization-scheme + measured
  mass carrier). This is stronger than N3/N4: N4 blocks the *branch row*, N1 blocks the *decimal value even given
  the row* — because Vandermonde-onto means the row is a free frame, not a constraint.

**VERDICT N1:** SOLID NO-GO. This is the *tightest* statement in the family: it proves the decimals are
underdetermined not just "hard to derive" — the interpolation is provably surjective onto all target pairs.
Owned = exponent row (THE). External = PRIM-EFT-IR-MATCHING-FUNCTIONAL (B-ext).

### N2 — D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 (general owner; direct+indirect)

- **(a) LIFT.** Can the frozen raw graph force the coefficient? NO — cert enumerates the full 420-perm order-12
  (4,3)-type class and exhibits SEP-1 (σ_A≠σ_B, same resolvent, different block→generation assignment) + SEP-2
  (two 4×4 companions, same charpoly x⁴−λ, different operators). Both machine-checked, self-tested controls fire.
  LIFT IMPOSSIBLE over the full invariant class.
- **(b) CLOSE.** Same missing object as N4 (PRIM-LEPTON-BRANCH-FIXING-OPERATOR). Not owned.
- **(c) DECOMPOSE.** This is the UMBRELLA: it lifts N3's DIRECT-route no-go to the GENERAL (direct+indirect) owner
  level. It bundles SEP-1 (= N4 assignment freedom, Continent-1-C) and SEP-2 (= LeptonPuiseuxUniquenessObstruction,
  Continent-3 insufficiency: companions AGREE on the invariant charpoly). The forced skeleton (Lucas 206, exponents,
  order-12 resolvent) is class A / owned.
- **(d) GENUINE-BOUNDARY.** Exact owned/external split identical to N4 but stated at the *coefficient* level.
  No new import beyond N4's primitive + N1's matching functor.

**VERDICT N2:** SOLID NO-GO, correctly the general umbrella. Not a duplicate of N4: N4 is the pigeonhole
non-constructibility of the ROW; N2 is the underdetermination of the COEFFICIENT over the full invariant class.
They are the two faces (structure-side / value-side of the assignment) and cross-cite cleanly.

### N3 — D0-BARE-GRAPH-DECIMAL-NOGO-001 (direct route)

- **(a) LIFT.** Can a raw graph operator DIRECTLY emit the 17-digit decimal? NO — r_μ = 3.8814328681047283 misses
  every small Q(φ)/Lucas scene invariant by > 1e-3 (cert asserts + a non-vacuous control that 2φ IS reachable).
  LIFT IMPOSSIBLE.
- **(b) CLOSE.** The needed datum is the EFT/IR matching scheme carrying m_μ — the same B-ext functor (N1). Not owned.
- **(c) DECOMPOSE.** Narrowest scope: blocks only the DIRECT bare-graph→decimal route. Integer Lucas L11+L4=206 +
  exponents (0,1/4,1/3) stay THE; the indirect Green/Puiseux route (csv:309) is a SEPARATE program, unaffected.
- **(d) GENUINE-BOUNDARY.** Import = EFT/IR matching scheme. Subsumed by N2 (which lifts N3 to direct+indirect).

**MINOR CERT-PROSE FLAG (not a kill):** The docstring says r_μ "RECONSTRUCTS the measured mass ratio
(~(m_μ/m_e)^(1/4))". Recomputed: r_μ⁴ = 226.97, PDG m_μ/m_e = 206.768 — so r_μ is NOT literally the 4th root;
it is the depth-1/4 *transfer* decimal, a looser encoding. The **load-bearing** fact (r_μ misses the scene
lattice, and encodes an externally-measured quantity) HOLDS; only the parenthetical "~(...)^(1/4)" is imprecise.
Proposed as a row-note clarification, not a status change.

**VERDICT N3:** SOLID NO-GO (direct route). Correctly the narrowest; subsumed by N2. One cosmetic prose imprecision.

### N5 — D0-RAW-SELF-READING-EXTRACTIONS-001 (Track II, four terminals)

- **(a) LIFT.** Can the raw S₃ functor be totalized (Outcome A)? NO — `RawSelfReadingExtractions` proves four
  terminals (G2, C4, L3, P3), each = FORCED raw invariant + DISPUTED two-completion. The lepton front L3 IS N4's
  fact re-run against the raw functor: `orbitSizes.length < numGenerations` (2<3), swap-invariant. LIFT IMPOSSIBLE.
- **(b) CLOSE.** No single derived object subsumes the four primitives —
  `D0-SELF-READING-PRIMITIVE-MINIMALITY-001` (csv:478): "conjunction-of-independent … 0 proof-edges among E1–E4."
  So PRIM-LEPTON-BRANCH-FIXING-OPERATOR is one of four *semantically independent* missing primitives, not closable
  by any master functor. CLOSE fails correctly.
- **(c) DECOMPOSE.** The lepton terminal L3 of N5 = the same 2<3 counting wall as N4, viewed through the raw
  self-reading functor rather than the shell-torus. The mapped cert `vp_raw_grading_no_manual_signature.py` is the
  *grading* front (nc 8≠12), not the lepton front — the lepton content lives in `extraction_lepton_L3`.
- **(d) GENUINE-BOUNDARY.** Import = the same branch-fixing primitive (for L3) + three sibling primitives (G/H/P).
  N5 adds the *independence* result (no master functor collapses them).

**VERDICT N5:** SOLID NO-GO (four terminals, conjunction-of-independent). Its lepton terminal is N4 seen from the
self-reading side; the value-add is proving the four missing primitives are mutually independent (no single-object close).

---

## 3. Independent skeptic pass (§05.8.R) — per headline

**Skeptic on N4 headline ("branch→generation row is non-constructible, 2<3"):**
- *Attack S1 — is 2<3 the real obstruction, or an artifact of picking σ = (0123)(456)?* Any cycle type realizing
  det(I−zU)=(1−z⁴)(1−z³) has exactly 2 non-trivial orbits (a 4- and a 3-orbit) on 7 points with no fixed point;
  (4,3) is the UNIQUE order-12 partition of 7 (15 partitions checked, csv:463). So numBranches=2 is forced by the
  resolvent, not by the choice of σ. NO-KILL.
- *Attack S2 — could a branch-SENSITIVE selector exist if the admissible group EXCLUDES the block-swap?* This is the
  real live crack, and it is already flagged in-repo (csv:463 SCOPE-REPAIR): the R4 swap-witness proves "no canonical
  assignment" only because the admissible symmetry group CONTAINS the swap. BUT N4's pigeonhole is independent of that:
  even with a branch-sensitive selector, 2 orbits cannot inject/surject/biject onto 3 generations — the third
  (electron, index-0) branch is simply absent from the 7-point carrier (no fixed point). So N4 survives S2 where R4
  alone would not. NO-KILL; N4 is strictly stronger than R4 here.
- *Attack S3 — is "numGenerations=3" smuggled?* It is `rfl` from K(9,11,13) trivial-isotype multiplicity Tr(T²)=3
  (`numGenerations_eq_three`), an owned upstream fact, not a lepton input. NO-KILL.
- **Skeptic verdict N4: ACCEPT.** No repair. (The S2 subtlety is why N4 exists as a separate row from R4.)

**Skeptic on N1 headline ("mass ratios underdetermined, Vandermonde onto"):**
- *Attack S1 — det=1/144 recomputed?* YES, exact fractions, and product form (1/4)(1/3)(1/12)=1/144 agrees. NO-KILL.
- *Attack S2 — onto ⇒ underdetermined is the right logic?* An invertible 3×3 Vandermonde ⇒ the quadratic through
  (0,m_e),(1/4,·),(1/3,·) hits any target; positivity/smoothness of the matching m(p) is a mild extra the memo
  states but does not over-claim. The no-go is a POSITIVE underdetermination (∃ many completions), the cleanest kind.
  NO-KILL.
- *Attack S3 — does the Lean B-part (branch_readout_not_unique) contaminate D?* No; B and D are independent theorems
  in the same file; D (mass ratio) rests only on the Vandermonde det. NO-KILL.
- **Skeptic verdict N1: ACCEPT.** No repair.

**Skeptic on N2/N3 headlines (coefficient / direct-decimal underdetermination):**
- *Attack S1 — is N3 vacuous because r_μ trivially misses a finite lattice?* The cert plants a non-vacuous control
  (2φ IS reachable) and a falsifier (a scene-invariant r_μ would void the no-go). The lattice is genuinely populated,
  so "misses it" is content. NO-KILL.
- *Attack S2 — the "(m_μ/m_e)^(1/4)" parenthetical.* r_μ⁴ = 226.97 ≠ 206.77 (recomputed). This IS an imprecise
  parenthetical in the N3 docstring. It is NOT load-bearing (the load-bearing claim is lattice-miss + external-datum);
  flagged as a row-note repair, not a status change. **PARTIAL — cosmetic repair proposed (RN-3).**
- *Attack S3 — is N2 a mere duplicate of N4?* No: N4 = pigeonhole on the ROW; N2 = 420-class underdetermination of the
  COEFFICIENT with two SEPARATORS (assignment + companion). Distinct theorems, clean cross-cite. NO-KILL.
- **Skeptic verdict N2/N3: ACCEPT with one cosmetic row-note (RN-3) on N3's parenthetical.**

**Skeptic on N5 headline (four terminals, conjunction-of-independent):**
- *Attack S1 — mapped cert is the GRADING cert, not the lepton cert; is the row mis-owned?* The row's Lean owner
  `extraction_lepton_L3` carries the lepton content correctly; `vp_raw_grading_no_manual_signature.py` is the
  python cert for the GRADING terminal (G2), which is one of the four this row bundles. The four-terminal row is
  legitimately multi-cert; the lepton fact is Lean-owned. Not a mis-ownership, but the python-cert column names only
  the grading front — worth a row-note (RN-5) so a reader does not expect the lepton check in that script. **PARTIAL.**
- **Skeptic verdict N5: ACCEPT with one clarifying row-note (RN-5).**

---

## 4. Can-fail check (computable, run this pass)

Recomputed, exact arithmetic (see §7 command):
- Vandermonde det at {0,1/4,1/3} = **1/144** (matches BranchAudit); product (1/4−0)(1/3−0)(1/3−1/4) = 1/144. ✓
- order-12 (4,3)-type perms of S₇ = 7!/(4·3) = **420** (matches csv:306/516). ✓
- C(7,4) = **35**, B_row bit = one of these. ✓
- r_μ⁴ = 226.97 ≠ PDG 206.768 ⇒ the N3 "~(...)^(1/4)" parenthetical is loose (RN-3). ✓ (control fires against the prose)
- Lucas closed form 206 + 2φ⁻² = 206.7639… misses PDG 206.7683 by 4.35e-3 (matches D0-LEPTON-002 note). ✓

All four target certs re-run: **4/4 PASS** (`vp_bare_graph_decimal_nogo`, `vp_lepton_raw_graph_coefficient_nogo`,
`vp_lepton_branch_fixing_operator_nogo`, `vp_raw_grading_no_manual_signature`).

---

## 5. Proposed row-notes (NOT applied — propose-only per hard rules)

- **RN-3** (`D0-BARE-GRAPH-DECIMAL-NOGO-001`, csv:307): append to the note —
  "[Batch-M clarify] r_mu is the depth-1/4 TRANSFER decimal, not literally (m_mu/m_e)^(1/4) (r_mu^4=226.97 vs
  206.768); the docstring's '~(m_mu/m_e)^(1/4)' is a loose gloss. Load-bearing fact = r_mu misses the Q(phi)/Lucas
  scene lattice AND encodes an externally-measured quantity; that stands. No status change."
- **RN-5** (`D0-RAW-SELF-READING-EXTRACTIONS-001`, csv:485): append —
  "[Batch-M clarify] python-cert column names vp_raw_grading_no_manual_signature.py (the GRADING/G2 terminal);
  the LEPTON terminal L3 (2<3, swap-invariant) is Lean-owned (extraction_lepton_L3), not in that script. Four
  terminals are multi-cert. No status change."
- **RN-N4** (`D0-LEPTON-BRANCH-FIXING-OPERATOR-OWNER-001`, csv:491): OPTIONAL —
  "[Batch-M] Confirmed sharpest object of the lepton-decimal family: owned = orbit-keyed exponent selector (class A);
  external = branch->generation row C(7,4)=35->1, split Continent-1/class-C (assignment, gauge-fixing) + Continent-3
  (third-branch existence wall, 2<3). Strictly stronger than R4 (survives the group-excludes-swap counter). Certs 6/6."
- No row-notes proposed for N1/N2 — they are already precisely stated.

---

## 6. Net synthesis — the honest owned/imported split (family verdict)

| object | status | class | owner |
|---|---|---|---|
| integer Lucas part L11+L4 = 206 | OWNED / THE | A | D0-LEPTON-002 (04.8.L.1) |
| exponent row (0,1/4,1/3) | OWNED / THE | A | D0-LEPTON-002, D0-LEPTON-GREEN-PUISEUX-OPERATOR-001 |
| order-12 resolvent (1−z⁴)(1−z³), unique (4,3) type | OWNED / THE | A | R4 (csv:463) |
| orbit-keyed exponent SELECTOR (4→1/4,3→1/3) | OWNED | A | L4 (csv:491) |
| shell-torus torsor (which σ, 420 perms) | gauge-fixing | **C** | R4 assignment half, Continent 1 |
| branch→generation ROW (C(7,4)=35→1) | EXTERNAL | **B-ext / Continent 3** | PRIM-LEPTON-BRANCH-FIXING-OPERATOR (2<3 wall) |
| 17-digit decimals r_μ, r_τ (VALUE) | HYP passport | **B-ext** | PRIM-EFT-IR-MATCHING-FUNCTIONAL / ASSUMP-EFT-IR-MATCHING-SCHEME |

**The five no-gos are one boundary seen from five angles**, not a cluster to be tagged:
N3 = value-side, direct route (narrowest); N2 = value-side, direct+indirect (umbrella); N4 = structure-side,
the row's non-constructibility (sharpest object); N1 = value-side, the tightest (Vandermonde-onto proves the
decimals are FREE given the row); N5 = the raw-functor view + the independence of the four missing primitives.
No decimal-mass derivation was manufactured (the owner's rejected over-claim); the win is the exact A-vs-(C,B-ext)
split with every object cited.
