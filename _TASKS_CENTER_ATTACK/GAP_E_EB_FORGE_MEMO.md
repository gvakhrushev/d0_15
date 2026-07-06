# GAP_E_EB_FORGE — forge the E-b no-skip / `+2`-uniqueness clause to close the top-zone upper bound `z₃ = 13`, or prove it unownable and sharpen to the irreducible residual (DRAFT; self-contained forge → own skeptic pass → accept/repair)

**Status:** DRAFT candidate. NO registry row edited; NO `.lean` added to the built tree; NO edit to `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` or `03_THEORY_MAP/theory_status_map.csv`. Lean sketches below are code blocks only. Companion can-fail script: `_TASKS_CENTER_ATTACK/gap_e_eb_check.py`.
**Task:** forge the E-b clause (that the top step is `+2` and NOT `+4` — that `+2` is the *unique admissible even step*, not merely even-and-minimal-by-narration) so that `{(9,11,13)}` is the unique 3-zone tower under owned constraints, OR prove it unownable and sharpen to the exact irreducible residual.
**Parents (cross-referenced, NOT duplicated):**
- `GAP_E_COMPLETENESS_MEMO.md` (v2) — delivered the R3 two-route missing-object spec; E-b is its "step route / consecutive fork" clause. Its §F1 already found G-STEP is one-sentence-killable (`+4` preserves the orientation class the printed `det` argument checks). Its G-2 already found `scene_triple_unique` (row 530) is conditional on `{+2-ladder hypothesis, window}` and CANNOT substitute for the gap.
- `GAP_E_CLOSE_MEMO.md` — attacked E-b via the empty-slot route; its Skeptic-#1 "KILL" (z₃=13 owned) was **OVERTURNED** by the main-loop counter-correction banner (2026-07-05), which is the open point this memo inherits. Its NEG-1 (empty-slot schema is surplus-over-inventory, inventory-relative, no owned step-inventory contains 13 non-circularly) is the strongest prior finding; this memo does NOT re-litigate it, it tests the ONE route NEG-1 did not: whether the **capacity route** owns 13 as an address PRIOR to the step, dissolving the begging-point.
**Pre-flight (2026-07-05):** grepped `theory_status_map.csv` + `CLAIM_TO_LEAN_MAP.csv` + `05_CERTS/` for `z₃ / z3 / admissibility window / no-skip / junction step / +2 unique / even step / (9,11,15)`. Owners found (cross-referenced, not duplicated): D0-SCENE-TRIPLE-UNIQUE-001 (row 530, conditional on `+2`-ladder HYPOTHESIS — see §OWN-0), D0-CARRIER-FULL-FORCING-001 (`address_ladder`, `by decide` arithmetic), D0-TOWER-STOP-NOEXT-001 (row 257, COUNT-3 only). **No row owns "the top step is `+2` and not `+4`" as a forcing.** Confirmed: the open point stands.

---

> **MAIN-LOOP VERIFICATION (2026-07-05, the self-skeptic dropped on API before finishing):** the two load-bearing facts are CONFIRMED against primary sources — §01.20:1556 verbatim excludes only `V8/V10/V12` (all interior/below 13, none above) → nothing owned forbids `V15`; BOOK_01:1899 verbatim says "the **minimal** admissible junction step is `+2`" via the orientation-parity argument (`5→6` flips, needs external bit ⊥M1; `5→7` preserves) — **minimal, not unique; the parity argument excludes the ODD step, not the even `+4`.** So the UNDERDETERMINED verdict and the `+4→V15` escape hold. **Error of record:** the memo's "capacity fixes cardinalities 9,11,13" citation `:1835` should be **`:1556`** ("This gives the first complete scene sizes (9,11,13). The construction rules out alternatives…"). Substance correct at :1556.

## VERDICT UP FRONT — **UNDERDETERMINED**, sharpened to a single irreducible residual (candidate)

**The E-b no-skip / `+2`-uniqueness clause does NOT close from owned material.** But the pass is not empty: it **dissolves one half of the begging-point and pins the other half to a single owned-vs-unowned seam**, which is a strict sharpening over both parent memos.

Precise outcome, three parts:

1. **The begging-point PARTIALLY dissolves — the half that concerned "is 13 an address/cardinality at all" is OWNED and step-independent.** The capacity route (§01.20:1548-1556; §01.22:1817-1835) fixes `V₁₃ = V₉ ⊔ ABCD` as a **set-extension of the base shell**, and states outright "capacity fixes the address cardinalities `9, 11, 13`" (BOOK_01:1835) with the parity route only "fix[ing] the increment" and "neither lean[ing] on the other" (BOOK_01:1899, verbatim). So **13 IS an owned cardinality, produced by a route that never mentions a step.** The parent memo's begging-point ("13 is a slot only if you assume the ladder") is refuted for the *over-base capacity reading*: `V₁₃ = V₉ ⊔ ABCD` needs no ladder.

2. **BUT the half that E-b actually needs does NOT dissolve — and the reason is now exact.** E-b is a claim about the **consecutive/step fork** (`9 →+2→ 11 →+? → z₃`): it must exclude a `+4` top *step*. The capacity route owns `13 = V₉ ⊔ ABCD` as a **cardinality**, but a `+4` step `11 → 15` does NOT deny that `V₁₃ = 13` exists — it builds a *different* top zone `V₁₅` of size 15 as a *different* extension, and asks why THAT zone is inadmissible as the third rung. The capacity route's own answer is COUNT-based and value-blind: `V₁₅ = V₉ ⊔ X` with `|X| = 6`, and **nothing owned rejects `|X| = 6` by name** (§01.20:1556 excludes only V8, V10, V12 — all *interior/below*, none *above* 13; verified §OWN-2). The capacity route fixes THREE cardinalities `{9, 11, 13}`; it does not own that `{9, 11, 13}` is the *complete* set of extension cardinalities — that completeness IS GAP-E, unmoved. **So the capacity route dissolves "is 13 a slot" but not "is 15 forbidden".**

3. **The irreducible residual is a single owned-vs-unowned seam, statable in one sentence (§RES).** What would close E-b is exactly ONE owned sentence: *"the admissible extension alphabets of `V₉` are exactly the dyad `D₂` and the terminal role square `ABCD`; there is no admissible extension of size 6 (or any size ∉ {2,4})."* The corpus owns the *list* `{D₂, ABCD}` (§01.20:1548) and owns *why each of 2 and 4 is forced* (D₂ = direct/return; |ABCD| = 4 by the `D_anchor` empty-slot forcing, BOOK_03:931-932) — but it owns NO closure clause `∀X (AdmExt(X) → |X| ∈ {2,4})`. The `+4`-excluding sentence and the extension-completeness sentence are **the same missing sentence**. E-b and E-a are not two routes; under the fork-identification `4 = 2·2` they are one gap seen from two sides.

**One-line residual:** *`z₃ = 13`'s upper bound is owned as a **cardinality** (`V₁₃ = V₉ ⊔ ABCD`) but NOT as a **maximum**: no owned sentence says the extension-alphabet inventory `{D₂, ABCD}` is closed, so a size-6 extension (`→ V₁₅`, the `+4` top step) is not excluded by any owned text — only by the narrated words "minimal"/"strictly"/"any other step".* The single owned sentence that would close it: an M1-forcing that **any extension alphabet is a power of the dyad `2^k`, and `2^k` for `k ≥ 3` repeats the signed square** (⇒ CASE-2 copy-symmetry kill, `NoExtension.lean:47`) — which would leave exactly `{2, 4}` and kill 6 (`6 = 2·3`, not a power of 2). That sentence is NOT owned; its candidate sketch is §RES-SKETCH; it is flagged, not claimed.

**Skeptic's strongest finding (self-run, §SKEPTIC below):** [filled after the skeptic pass]

---

## OWN-0. The exact open point, re-verified verbatim against primary sources (not re-litigated)

**OWN-0.1** `SceneTripleUnique.lean:74-85` (repo-root copy read this pass, identical to built copy):
```
theorem scene_triple_unique (z₀ z₁ z₂ n : ℕ)
    (hladder₁ : z₁ = z₀ + 2) (hladder₂ : z₂ = z₁ + 2)
    (hcentre : z₁ = lucas n) (hlo : 9 ≤ z₁) (hhi : z₁ ≤ 13) :
    (z₀, z₁, z₂) = (9, 11, 13)
```
The top step `z₂ = z₁ + 2` (`hladder₂`) is a **HYPOTHESIS**, and `unique_lucas_in_window` (`:59`) constrains only the **centre** `z₁` (it forces `n = 5 ⇒ z₁ = 11`). The top zone `z₂` is then `11 + 2 = 13` *by the hypothesis*. **A `+4` top step `(9,11,15)` satisfies `hladder₁`, `hcentre`, `hlo`, `hhi` but NOT `hladder₂`, so it lives OUTSIDE the theorem's scope, not inside its conclusion.** `scene_triple_unique` does not exclude `(9,11,15)`; it declines to speak about it. (This is `GAP_E_COMPLETENESS_MEMO` G-2, re-verified.) **Script §I confirms `(9,11,15)` survives every owned constraint.**

**OWN-0.2** `CarrierForcing.lean:81` `theorem address_ladder : (4 + 5 = 9) ∧ (9 + 2 = 11) ∧ (11 + 2 = 13) := by decide` — **pure arithmetic**. `11 + 2 = 13` being true does not exclude `11 + 4 = 15`; `by decide` forces no step choice. (Re-verified this pass.)

**OWN-0.3** `NoExtension.lean:61-65` (`no_extension_theorem`, D0-TOWER-STOP-NOEXT-001) proves three algebra facts (quadratic closure; `p³` reduces into `span{1,p}`; `|S₂|>1`); its docstring `:25-27` states "The COUNT (3 slots, no 4th) is proved here". **It is silent on zone SIZES.** `(9,11,15)` is a *3-zone* tower (count 3), so COUNT-3 does not exclude it (script §I).

## OWN-1. The parity argument owns EVEN, not `+2` — exact reach re-verified (BOOK_01:1899 / BOOK_03:1042-1058)

`BOOK_01…md:1897-1907` (§01.22, verbatim, re-read this pass):
> "`ε_n := φ^n − L_n = −ψ^n = (−1)^{n+1} φ^{−n}`. So the sign of the defect alternates with `n`: at `n=5` the holonomy parity is `+`, at `n=6` it is `−`. Now attempt a unit junction step `5 → 6`. The orientation/torsion class flips, and to splice the two layers across that flip one must supply an external orientation bit … forbidden by M1 … The step `5 → 7` preserves the orientation class, so the splice closes with no exogenous parameter. Hence the minimal admissible junction step is `+2`…"

**Exact owned content (script §II):** the mechanism kills a step iff it flips the `ℤ₂` orientation class, i.e. iff the step is **ODD** (in the index `n`). `+1` (written), `+3, +5` (same mechanism) die; `+2` AND `+4` both preserve the class and reach NO `⊥`. **The word "minimal" (1907) is a conclusion-word the printed mechanism never reaches for `+4`.** Two independent confirmations: (i) `BOOK_03:1044-1047` machine-checks only `det(T^{n+2}) = det(T^n)` (evenness), with the `+1` flip as the negative control — `+4` also satisfies `det(T^{n+4}) = det(T^n)`; (ii) the argument is entirely in the **Lucas index `n`** (`5→6`, `5→7`), which maps to address values `L₅=11 → L₆=18` / `L₇=29`, NOT to `11→13` — so it does not even reach the address-value `+2` step cleanly (domain-confusion noted in `GAP_E_CLOSE` ATT-C, re-confirmed). Net: parity owns **step-evenness**; the narrowing to `+2` over `+4` is **narration**, not forcing. This is E-b's exact hole.

## OWN-2. The capacity route owns 13 as a step-independent CARDINALITY — begging-point half 1 dissolves

`BOOK_01…md:1548-1556` (§01.20, verbatim):
> "The next two shell extensions are the only primitive unresolved capacities over the pointed shell: the direct/return dyad and the full terminal role square. Therefore `V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ four terminal roles A,B,C,D`. … The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10` without losing direct/return capacity, and `V13` cannot be replaced by `V12` without losing one terminal role."

`BOOK_01…md:1817-1835` (§01.22 restatement, verbatim):
> "`V₉ = |Ω₈| + 1 = 9` … `V₁₁ = V₉ + D₂ = 11`, `V₁₃ = V₉ + |four terminal roles A,B,C,D| = 13`."

and the two-route independence, `BOOK_01…md:1899` (verbatim):
> "capacity sets the cardinalities, orientation-parity sets the increment, and **neither leans on the other**"

and `BOOK_01…md:1835` (verbatim):
> "capacity fixes the address cardinalities `9, 11, 13`, the `(−1)^n` orientation parity fixes the `+2` step that connects them"

**Owned content:** `V₁₃ = V₉ ⊔ ABCD` is a **set-extension of the base shell**, produced with **no step at all** (script §III). So **13 IS an owned cardinality independent of the ladder** — the parent memo's begging-point ("13 is a slot only if you assume the ladder") is **refuted for the over-base reading**. This is the genuine gain of the pass: the capacity-fixing route *does* independently own that 13 is a shell size, prior to and independent of the step choice, exactly as the task's dissolution-condition asks.

## OWN-3. …but the capacity route does NOT own that 15 is FORBIDDEN — begging-point half 2 stands

The dissolution asks: "If the cardinality-fixing route independently owns that 13 is an address, the begging-point dissolves and `+4` is killed." **It dissolves only half.** Here is the exact reason the other half survives (script §IV):

- The `+4` top step `11 → 15` does **not** deny that `V₁₃ = 13` exists. It builds a **different** top zone `V₁₅ = V₉ ⊔ X` with `|X| = 6`, and asks why THAT zone is inadmissible as the third rung of a 3-zone tower whose second rung is `V₁₁`.
- The capacity route's exclusions (§01.20:1556) are `V8, V10, V12` — **all interior/below 13**. **No owned sentence rejects a size-6 extension, or any size above 13, by name** (verified: whole cert `vp_v1141_abcd_omega8_v9_phi_capacity.py` has no V15/composite-extension check; the "V10 exclusion" is literally `10 > 9`, `GAP_E_CLOSE` NEG-1 finding, re-confirmed).
- So the capacity route fixes **three cardinalities** `{9, 11, 13}` but does **not** own that `{9, 11, 13}` is the **complete** set of admissible extension cardinalities. That completeness is exactly GAP-E, **unmoved by the dissolution of half 1**.

**Why half 1's dissolution does NOT propagate to half 2 (the precise seam):** owning "13 is a cardinality" is an **existence** fact (`V₁₃ = V₉ ⊔ ABCD` exists and has size 13). Excluding `+4` is a **completeness/maximality** fact (no admissible extension has size 6, or ∉ {2,4}). Existence of the owned extensions does not entail non-existence of a rival extension. The empty-slot pattern (OWN-4) is the corpus's only tool for a maximality fact — and it fires the WRONG way (see OWN-4).

## OWN-4. The empty-slot pattern is surplus-over-inventory — it cannot make 15 the empty slot (confirms `GAP_E_CLOSE` NEG-1)

`BOOK_03…md:931-932` (§03.23.1, verbatim): "`D_anchor > 4`: empty address slots appear; to tell an empty slot from a significant one you must import an exogenous significance catalog. Banned." Inventory = closed role alphabet `{A,B,C,D}`, `|roles| = 4`; empty ⇔ count exceeds 4.

`BOOK_01…md:1911-1913` (§01.22, verbatim): "`N > 9`: the cycle has 'empty' steps that correspond to no address. To tell an empty step from a significant one the cycle would need an external catalog of significance, which is `⊥M1`." Inventory = closed address count `D = 9`; empty ⇔ `N` exceeds 9.

**Both instances fire when a structure supplies `k > |I|` positions for an owned inventory `I` — a SURPLUS.** E-b needs the opposite: a `+4` step that *skips* address 13 inside a laid-out space, making 13 a *deficit* slot. For that the corpus would need an owned address space of size ≥ 13 in which 13 pre-exists as a slot a `+4` leaps over. **The only owned address space is exactly the 9 positions of `V₉`** (`BOOK_01:1909`: "the address count is `D = 9` … giving 9 distinguishable address positions"). There is **no owned laid-out space of size 13+**, so the empty-slot pattern has nothing to make 13-when-skipped "empty." This is why the empty-slot route (the task's candidate seed) does **not** transfer — confirmed independently of `GAP_E_CLOSE`, and now located precisely: the pattern is a *surplus* detector, E-b needs a *skip* detector, and no owned laid-out space supports "skip." **Half 1's dissolution does not rescue this: knowing `V₁₃` is a cardinality does not lay out a 13-position address space through which a walk could skip.**

---
