# F4 LEAN-LIFT WAVE LOG (Fable finalization)

**Date started: 2026-07-06. Discipline: foreground lake builds; native_decide for Fintype-Perm/matrix evaluation; cards→literals before Nat arithmetic; per-module targeted build + `#print axioms`; ONE full `D0.All` at the end. Registry CSV untouched (flip-proposals only, below). 053040 untouched. No commit.**

Baseline: warm cache confirmed (`lake build D0.Foundation.CanonicalSelectorNoGo` → "Build completed successfully (2946 jobs)").

## Targets

| # | target | module | status |
|---|--------|--------|--------|
| 1 | BRIDGE span-equality P=Q | D0/Claims/InvariantGenerationBridge.lean | LANDED |
| 2 | P-INVARIANT-MINIMAL orbit-minimality | D0/Foundation/InvariantMinimal.lean | LANDED |
| 3 | dimA_strictMono + 33-skip totality | D0/VNext/AFD0LaplacianComparisonNoGo.lean (extend) | LANDED |
| 4 | numGenerations = Tr(T²) typing | D0/Extensions/LeptonSelectorExtension.lean (extend) | LANDED |
| 5 | W-REC skeleton | D0/Core/WRecArchitecture.lean | LANDED |
| 6 | R-A assumption carrier (coordinator addition) | D0/Bridge/Assumptions/ClassRecordIsAddressable.lean | LANDED |

## Pre-flight notes

- Target 1 anti-circularity (R3b pre-registration, BRIDGE_INVARIANT_GENERATION_MEMO.md §6/§9): `gens` written as a LITERAL list of 30 `Equiv.swap` terms, NOT derived from the zone map. Face-G projector `Q` uses the in-tree `D0.Claims.zone31` (Signature31Split.lean:47) — ties Face G to the existing adjacency-factorization module.
- Target 4 anchor found in-tree: `D0.Dynamics.trace_T2 : Matrix.trace (T ^ 2) = 3` (ToralAutomorphism.lean:23) + zone-count route via `D0.Claims.zone31`. BOTH honestly derivable; both landed.
- Target 5: F3_HONEST_BRIDGES_PACKAGE.md TASK 3 skeleton followed leg-by-leg (L1 concrete model; L2–L4 decidable ℤ-scaled Fin 8; L5/L6/L7 explicit hypotheses). The TASK-1 Lean carrier `D0/Bridge/Assumptions/ClassRecordIsAddressable.lean` is created here (F3 §1.1(4) says it is an F4-wave artifact), pattern verbatim from KernelChargeLocalization.lean (`statement : Prop; cited : statement`).

---

## Per-target entries

### Target 1 — BRIDGE span-equality: **LANDED**

- **File:** `09_LEAN_FORMALIZATION/D0/Claims/InvariantGenerationBridge.lean` (new).
- **Theorems:** `bridge_entrywise` (∀ i j, P i j = Q i j, native_decide payload), `bridge_projector_eq : P = Q` (THE bridge), `q_idempotent : Q*Q = Q`, `q_symmetric : Qᵀ = Q`, `q_trace_three : tr Q = 3`, `orbit_count_three : (univ.image orbit).card = 3` (from the literal gens alone, no zone map), capstone `invariant_generation_bridge` (conjunction). Plus `gens_length : gens.length = 30`.
- **Anti-circularity (R3b) honored:** `gens` = literal list of 30 `Equiv.swap` terms; `P` = Reynolds/orbit-averaging projector via computable orbit closure (`step^[33]`) from `gens` only; `Q` = zone-indicator projector from the in-tree `D0.Claims.zone31`. The two sides use genuinely different inputs.
- **Build:** `lake build D0.Claims.InvariantGenerationBridge` → green (2953 jobs, module 21s).
- **Axioms:** propext, Classical.choice, Quot.sound + native_decide reduceBool axioms only. **No sorryAx.**
- **Honesty carried in docstring:** memo §0 honesty clause (definition-unfolding pricing), R2 inheritance (owned as far as csv:555; universal no-proper-refinement outsourced to LEAN_PROVED row 549; class-function-universality EVIDENCE-grade), R3 zone-axis wording, R4 Face-G grade caveat; count 3 NOT re-derived; Weyl-role freedom intact; "gens generate Aut" cited-not-formalized (only orbit closure is used).

### Target 2 — P-INVARIANT-MINIMAL orbit-minimality: **LANDED**

- **File:** `09_LEAN_FORMALIZATION/D0/Foundation/InvariantMinimal.lean` (new).
- **Theorems:** `orbit_count_three` (dim R^Aut = 3 as orbit count of the literal generator list), `deg_three_values`, `deg_classifies_orbits : ∀ i j, j ∈ orbit i ↔ deg i = deg j` (the owned degree observable — COMPUTED from adjacency, not declared — classifies the orbits), `step_constant` + `classifier_constant_on_orbits` (abstract: ANY generator-invariant classifier is constant on orbits — genuine ∀ over classifiers, structural induction, NO native_decide, axioms = propext/choice/Quot.sound only), capstone `invariant_minimal_meet : ∀ c, gens-invariant c separating deg ⇒ (c i = c j ↔ j ∈ orbit i)` — the lattice-meet: every Aut-closed separating partition algebra IS R^Aut; no Aut-closed proper refinement separates deg.
- **RR-1 upgrade honestly logged:** the cert's single-witness refinement clause is now a UNIVERSAL over all partition classifiers in Lean (better than cert-grade on that leg); the partition-algebra ↔ subalgebra equivalence and "gens generate Aut" stay cited-not-formalized; class-function-universality of owned functionals stays EVIDENCE-grade (row-549 scope) — docstring carries all three caveats.
- **Build:** green (module 8.7s). **Axioms:** clean (native_decide reduceBool only where used; no sorryAx).
- **Debug note (precedent for future waves):** first build hit `(deterministic) timeout at whnf` in the CONSUMING theorem — the elaborator fell into the 33-step `Finset` closure term when whnf-ing `j ∈ orbit i` at default transparency. Fix: `attribute [irreducible] step orbit` placed AFTER all native_decide/simp-unfold uses, BEFORE consumers. Same family as the kernel-`decide` Fintype-Perm wall; new entry in the discipline list: **membership statements over computed Finsets must be sealed irreducible before downstream use.**

### Target 3 — dimA_strictMono + 33-skip totality: **LANDED**

- **File:** `09_LEAN_FORMALIZATION/D0/VNext/AFD0LaplacianComparisonNoGo.lean` (extended in place; existing theorems untouched).
- **Theorems (new):** `pc_pos`, `dimA_succ : dimA (n+1) = dimA n + a·(a+2b)` (the T2A.3 recurrence, exact/additive), `dimA_strictMono : StrictMono dimA` (T2A.4), `pc_eq_fib : pc n = (F(n+2), F(n+1))`, `dimA_eq_fib : dimA n = F(2n+3)` (T2A.6 typed separator, via Mathlib `Nat.fib_two_mul_add_one`), `af_skips_d0_dim_total : ∀ N, dimA N ≠ d0LaplacianDim` (THE totality closure — upgrades the `N ≤ 3` quantifier of `laplacian_tower_compatibility_no_go` to ALL N), capstone `laplacian_tower_compatibility_no_go_total`.
- **Build:** green (2947 jobs). **Axioms: propext/Classical.choice/Quot.sound ONLY — no native_decide, no sorryAx.** Kernel-grade throughout (induction + `Nat.fib` lemmas + omega).
- This is exactly the memo-named lift: W4_DECOMPOSITION_MEMO.md §2a "Named Lean lift candidate: `dimA_strictMono` + unbounded `∀ N, dimA N ≠ 33`".

### Target 4 — numGenerations = Tr(T²) typing: **LANDED**

- **File:** `09_LEAN_FORMALIZATION/D0/Extensions/LeptonSelectorExtension.lean` (extended; existing theorems untouched; new imports `D0.Dynamics.ToralAutomorphism`, `D0.Claims.Signature31Split`).
- **Theorems (new):** `numGenerations_eq_trace : (numGenerations : ℤ) = Matrix.trace (D0.Dynamics.T ^ 2)` (via the in-tree `D0.Dynamics.trace_T2 : tr(T²) = 3`, `T = !![0,1;1,-1]`) AND `numGenerations_eq_zone_count : numGenerations = (Finset.univ.image D0.Claims.zone31).card` (the OWNED zone-count root, computed image-cardinality). Both routes were honestly derivable in-tree, so BOTH landed; the docstring names the zone-count as the owned root and the trace as the tick-dynamics face of the same number.
- **Build:** green. **Axioms:** native_decide reduceBool only (inherited from `trace_T2` on the trace leg); no sorryAx.

### Target 6 (coordinator addition) — R-A assumption carrier: **LANDED**

- **File:** `09_LEAN_FORMALIZATION/D0/Bridge/Assumptions/ClassRecordIsAddressable.lean` (new; the F3 §1.1(4) "later F4-wave artifact").
- **Content:** `structure D0.Bridge.BridgeAssumption.ClassRecordIsAddressableAssumption where statement : Prop; cited : statement` + `abbrev D0.Bridge.ClassRecordIsAddressableAssumption` — verbatim carrier pattern of `KernelChargeLocalization.lean:22-24` (the F3-cited precedent). NOTHING proven; explicit hypothesis carrier only.
- **Docstring carries (per F3 Task 1 + coordinator brief):** the R-A copula content ("IS, not interacts-with, an addressable registration"), the §01.3/§01.11.3 layer-boundary assembly (:253 𝔮 / :996 / :988 INTERACT-WITH-only), no in-print name-match (unlike GAP-E's :836/:862/:67), failure meaning (W-ELEM demotes to narrated, |V_base| seal reverts, no regression), reopening hook (:253 𝔮-scoping), and the taxonomy type.
- **Taxonomy (validator-checked):** docstring leads with **`D0_INTERNAL_FORCING_TARGET`** — the F3 §1.1(3) SANCTIONED FALLBACK — because `check_no_sorry_in_core.py`'s `INTERNAL_TARGET_TYPES` whitelist does NOT contain the F3-primary coinage `D0_INTERNAL_TYPING_TARGET` (a verbatim F3 §1.2 row would fire `bad type`). Flip-proposal below carries the corrected row.
- **Build:** green. **Axioms:** n/a (no theorems; no `axiom` keyword — structure hypothesis pattern).
- **Guard state (handoff, expected):** `check_assumption_ledger_ownership.py` → PASS. `check_no_sorry_in_core.py` → exactly ONE new FAIL: `D0/Bridge/Assumptions/ClassRecordIsAddressable.lean: BridgeAssumption structure missing from ledger` — this is the chicken-and-egg by design: the ledger row is the INTEGRATION pass's move (this wave does not touch CSVs). The guard goes green the moment the F3 §1.2 row (with the taxonomy fix below) is appended to `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv`.

### Target 5 — W-REC skeleton: **LANDED**

- **File:** `09_LEAN_FORMALIZATION/D0/Core/WRecArchitecture.lean` (new; imports `D0.Core.WitnessForcing` + the Target-6 carrier).
- **Leg map (F3 TASK 3, followed exactly):**
  - L1 **PROVED** `retained_traced_partition : Pret + Qtr = 1 ∧ Pret * Qtr = 0` on the concrete model `RecordSupport = Fin 9` (1 readout + 8 archive slots); P/Q↔retained/traced identification stays a docstring citation (:33-34/:37).
  - L2 **PROVED** `marker_average_address_blind : ∀ a, cAvgSum (marker a) = 1` (ℤ-scaled, `cAvgSum = 8·cAvg`; mirrors check 1).
  - L3 **PROVED** `addr_disjoint_from_trace` : no marker shift-invariant ∧ every circulant basis element shift-invariant, nonzero, not a marker (mirrors check 3; the circulant side made explicit so the disjointness is two-sided).
  - L4 **PROVED** `avg_idempotent : ∀ e, cAvgSum (cAvgSum (stdB e)) = 8 • cAvgSum (stdB e)` on the full matrix-unit basis (mirrors check 6).
  - L5 **EXPLICIT HYPOTHESIS** `structure SingleQNWriterSweep` (corpus sweep; the F3 optional decidable shadow deliberately NOT built — must not masquerade as the sweep).
  - L6 **EXPLICIT HYPOTHESIS** `structure PhysicalityRequiresAddressable` (:988 cited, not formalized).
  - L7 **EXPLICIT HYPOTHESIS** = `D0.Bridge.ClassRecordIsAddressableAssumption` (Target 6).
- **Capstone:** `card_base_forced_wrec (m) (h_wrec) (h_g2) (h_ra) (h_halt : 1 ≤ m) (h_nocopy : m < 2) : Fintype.card Omega8 + m = 9` — a THIN RE-EXPORT of the built `card_base_forced_conditional` (one forcing statement in D0.All, re-attributed not re-proved). **Honesty guard honored: `h_halt` NOT promoted to a proved term** (memo :406).
- **Build:** green. **Axioms:** capstone = propext/Classical.choice/Quot.sound ONLY; L1–L4 add native_decide reduceBool axioms; no sorryAx. Note: `D0/Core/` is a `check_no_sorry_in_core.py` CORE dir — file scanned clean (no forbidden tokens in code).

---

## FINAL — build, guards, LANDED/HELD table

**D0.All: `Build completed successfully (4015 jobs)`** (baseline 4011 + 4 new modules; foreground build). Aggregates regenerated via `../tools/generate_lean_aggregates.py` (rewrote `D0/All.lean`, `D0/TheoremLedger/ClaimMap.lean`, `D0/TheoremLedger/ActiveClosureIndex.lean`); all four new imports present in `D0/All.lean` (:23, :67, :111, :216).

Guards: `check_assumption_ledger_ownership.py` PASS · `check_claim_map_coverage.py` PASS · `check_no_sorry_in_core.py` = 1 expected handoff FAIL (Target 6 ledger row pending integration, see above).

| # | target | module / theorems | verdict |
|---|--------|-------------------|---------|
| 1 | BRIDGE span-equality | `D0.Claims.InvariantGenerationBridge` — `bridge_projector_eq : P = Q`, `q_idempotent`, `q_symmetric`, `q_trace_three`, `orbit_count_three`, `invariant_generation_bridge` | **LANDED** |
| 2 | P-INVARIANT-MINIMAL minimality | `D0.Foundation.InvariantMinimal` — `orbit_count_three`, `deg_classifies_orbits`, `classifier_constant_on_orbits` (axiom-pure), `invariant_minimal_meet` | **LANDED** |
| 3 | dimA strictMono + 33-skip totality | `D0.VNext.AFD0LaplacianComparisonNoGo` (extended) — `dimA_succ`, `dimA_strictMono`, `pc_eq_fib`, `dimA_eq_fib`, `af_skips_d0_dim_total`, `laplacian_tower_compatibility_no_go_total` (ALL kernel-grade, zero native_decide) | **LANDED** |
| 4 | numGenerations typing | `D0.Extensions.LeptonSelectorExtension` (extended) — `numGenerations_eq_trace`, `numGenerations_eq_zone_count` | **LANDED** |
| 5 | W-REC skeleton | `D0.Core.WRecArchitecture` — L1–L4 proved, L5–L7 explicit-hypothesis carriers, `card_base_forced_wrec` capstone | **LANDED** |
| 6 | R-A assumption carrier | `D0.Bridge.Assumptions.ClassRecordIsAddressable` — carrier structure only, validator-taxonomy corrected | **LANDED** |

Nothing HELD; no target fought back structurally. (One debug precedent minted: whnf-explosion on computed-Finset membership → `attribute [irreducible]` seal, Target 2 entry.)

---

## FLIP-PROPOSALS (for the guarded integration pass — NOT applied here; CLAIM_TO_LEAN_MAP.csv is the source of truth, regen generated files via sync_theory_status_map.py)

1. **Mint `D0-INVARIANT-GENERATION-BRIDGE-001`** (BRIDGE_INVARIANT_GENERATION_MEMO.md §7 M1 text, verbatim) with the Lean fields NOW FILLABLE at mint: `lean_module=D0.Claims.InvariantGenerationBridge`, `lean_theorem=bridge_projector_eq` (+ capstone `invariant_generation_bridge`), lean_status **LEAN_PROVED** (native_decide/ofReduceBool; gens literal per pre-registered R3b), release PROOF-TARGET per the memo's inheritance clause (status stays tied to D0-P-INVARIANT-MINIMAL-001). Apply memo M2/M3 note-appends to csv:51 and csv:460 unchanged.
2. **`D0-P-INVARIANT-MINIMAL-001` (csv:555):** lean fields ← `D0/Foundation/InvariantMinimal.lean` / `invariant_minimal_meet` (+ `orbit_count_three`, `deg_classifies_orbits`); lean_status **OPEN → LEAN_PROVED**. This IS row-550's EXACT-MISSING item (1) (the Fin-33 orbit-count/minimality lemma). Note must carry: quantification = partition classifiers; algebra↔partition equivalence + "gens generate Aut" cited-not-formalized; class-function-universality of owned functionals stays EVIDENCE-grade (row-549 scope) — the Lean lift upgrades the RR-1 single-witness clause to a universal over partitions, nothing else.
3. **`D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001` (row 412 area, lean module `AFD0LaplacianComparisonNoGo`):** note-append — the `N ≤ 3` quantifier is CLOSED TOTALLY in Lean (`af_skips_d0_dim_total : ∀ N, dimA N ≠ 33` via `dimA_strictMono` + `dimA_eq_fib = F(2n+3)`, kernel-grade, no native_decide); W4_DECOMPOSITION_MEMO §2a's "named Lean lift candidate" is DONE. No release-status change needed (already owned NO-GO); lean_theorem may append `laplacian_tower_compatibility_no_go_total`.
4. **`D0-POSTCORE-LEPTON-SELECTOR-MAXIMALITY-NOGO-001`:** note-append — the `numGenerations := 3` literal is now TYPED in-tree: `numGenerations_eq_trace` (= tr T², via `D0.Dynamics.trace_T2`) and `numGenerations_eq_zone_count` (= #zones via `D0.Claims.zone31`, the owned root). No status change.
5. **`D0-GAP-W-WITNESS-PLUS-ONE-001` (csv:545):** BOTH conditions of the F3 §1.3 upgrade path are now met (W-REC lift landed with decidable OB-W1/OB-W2/OB-W3 + partition; re-attributed capstone `card_base_forced_wrec` consumes `ClassRecordIsAddressableAssumption` explicitly). Flip: lean_status **OPEN → LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS**, `uses_bridge_assumptions=True`, `assumption_ids=ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`, lean fields += `D0/Core/WRecArchitecture.lean` / `card_base_forced_wrec` (precedent row: D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001). Release stays PROOF-TARGET per F3 until R-A is owned.
6. **`LEAN_ASSUMPTION_LEDGER.csv`: append the F3 §1.2 row for `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE` with ONE correction — `assumption_type: D0_INTERNAL_TYPING_TARGET → D0_INTERNAL_FORCING_TARGET`** (the F3 §1.1(3) sanctioned fallback; the primary coinage is not in `check_no_sorry_in_core.py`'s `INTERNAL_TARGET_TYPES` whitelist and fires `bad type`). Owner file now exists (`lean_file` existence check green). This flips the one pending guard FAIL to green. Alternative (NOT recommended without a tools-owner decision): whitelist the coinage in the guard.

**Discipline confirmations:** no registry/ledger CSV touched; 053040 untouched; no commit; all builds foreground; native_decide only where kernel `decide` is precedent-forbidden; cards-to-literals discipline respected (no symbolic `.card` inside kernel Nat arithmetic); per-module `#print axioms` all clean of sorryAx.
