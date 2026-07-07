# ATTACK_F7_SELECTOR_CHILD_MEMO — the hypercharge F7 charge-residue is a CHILD of the selector-M1-no-go

**Type:** center-attack forcing memo (coordinator-originated). Memo-only. No commit. Never touch `053040`.
**Date:** 2026-07-07.
**Companion cert:** `_TASKS_CENTER_ATTACK/attack_f7_check.py` (can-fail, mutation-tested; 8/8 PASS, `--selftest` 3/3 mutations flip).
**Verdict:** **CONSOLIDATED** (F7 splits: owned-structure LOCALIZATION leg + M1-forbidden CHARGE-label leg = corollary-of `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` / `D0-P-INVARIANT-MINIMAL-001`). **NO closure claimed.** No status flip.

---

## 0. One-paragraph result

The single discrete gate between the 2-dim anomaly-free freedom `span{Y, B−L}` and the physical hypercharge ray `span{Y}` is the registered assumption **`ASSUMP-KERNEL-CHARGE-LOCALIZATION`** (`LEAN_ASSUMPTION_LEDGER.csv:25`, PHYSICS_DICTIONARY: "`ν^c` uncharged = `ν_R` localized in `ker(A)`"). This label **bundles two objects of different codimension** that BOOK_04:1408 itself says are "*strictly stronger, not equivalent*":

- **LOCALIZATION leg** `ν_R ∈ ker(A)` — **codimension 3** (the 30-dim zone-balanced kernel, 30 of 33). Its *kernel structure* is CERT-CLOSED exact linear algebra; its *physical identification* (this kernel **is** the neutrino) is an R2 graph→physics **MECH-LIMIT** (`D0-GRAPH-SPACE-NO-ISOMETRY-001`), not pure Core.
- **CHARGE leg** `Y_{ν^c}=0` (i.e. `2·Y_{ν^c}=0`, `b=0`) — **codimension 1** in `span{Y, B−L}`. This is the **within-zone selector-M1-no-go in the charge sector**: the only `Aut(K)=S₉×S₁₁×S₁₃`-invariant covectors are the three zone-indicators, each vanishing on `ker(A)`; `Y_{ν^c}` reads a **single vertex**, is not zone-constant, hence not `Aut`-invariant, and needs an exogenous label. That is *verbatim* the mechanism of `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (row 549) / its positive face `D0-P-INVARIANT-MINIMAL-001` (row 555).

**Consequence.** F7 does **not** close — closing the charge leg would repeat the theorem-backed selector no-go. But the assumption is **sharpened and consolidated**: it splits into an owned-*structure* localization leg + an M1-forbidden charge-label leg that is a **corollary-of** the selector no-go, filing F7 under the owned selector family instead of leaving it a "physics-dictionary black box."

---

## 1. The argument, verified verbatim on disk (±10 lines)

### 1.1 The assumption bundles two claims (BOOK_04:1408, exact)

> `ker A ⟺ Majorana route.` The membership `ν_R ∈ ker(A)` is codimension 3 (zone-balanced, 30-dim of 33) while Majorana-admissibility `2·Y_{ν^c}=0` is codimension 1 in `span{Y, B−L}` — **strictly stronger, *not* equivalent.** Worse, no scene-*forced* functional can bridge them: the only `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`-invariant covectors are the three zone-indicators (distinct zone sizes ⇒ no zone swaps), and every one of them **vanishes on `ker(A)`**; `Y_{ν^c}` reads a **single vertex, is not zone-constant, hence is not `Aut`-invariant** and needs an exogenous label (owners `D0.Foundation.GraphSpaceNoIsometry`, `D0.Matter.HyperchargeU1MassKernelA2`).

The Lean assumption file confirms the bundling in its own words:
`09_LEAN_FORMALIZATION/D0/Bridge/Assumptions/KernelChargeLocalization.lean:13-14` — "*this bridge **is** the R2 localization, so the hypercharge-direction obligation and the R2 MECH-LIMIT are one obligation, not two.*" (The Lean file collapses the two into one *bridge*; BOOK_04:1408 proves they are two objects of different codimension — the split this memo makes.)

### 1.2 The LOCALIZATION leg (honest two-layer ownership grade)

- **Kernel STRUCTURE — CERT-CLOSED (owned).** BOOK_04:260-285: `Nullity(A)=33−3=30`, zone split `30=8+10+12`, "*A acts equally across a zone, so every within-zone difference vector lies in `Ker(A)`*", "*the split itself is the theorem*", Status **CERT-CLOSED**. The 30-fold kernel and its zone-balance are exact linear algebra, no free parameter.
- **Physical IDENTIFICATION — MECH-LIMIT (external).** "*Neutrinos live in the 30-fold degenerate kernel (the Sterile Archive)*" (BOOK_04:629), "*30-dim kernel*" (:657), "*sterile traced-out complement: kernel 30-fold degenerate*" (:1258). But the ledger and `KernelChargeLocalization.lean:6-7` type the identification as "*the R2 graph→physics localization, which is a MECH-LIMIT, not a forced identity (`D0-GRAPH-SPACE-NO-ISOMETRY-001`)*."

**Grade (pre-registered attack surface #1, answered honestly):** the localization is **owned-in-structure, MECH-LIMIT-in-identification** — NOT fully Core. This is *weaker* than a bare "OWNED" claim. It still supports the consolidation: the localization structure is owned exact math and the only external residue on this leg is the *same* R2 MECH-LIMIT already registered — a **different** external from the charge leg (see §2). So F7 does not become "two fresh externals"; it becomes **one owned kernel structure + one already-registered R2 MECH-LIMIT (LOC) + one selector-no-go charge label (CHG)**.

### 1.3 The CHARGE leg is the selector-M1-no-go (BOOK_04:1408 + row 549 + A2 cert)

The vanishing-on-kernel / not-Aut-invariant / single-vertex argument at :1408 is the *same* mechanism as `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` (`theory_status_map.csv:549`, LEAN_PROVED): "*Aut(K)=S₉×S₁₁×S₁₃ acts freely-transitively within each zone ⇒ 0 Aut-invariant canonical labelings*", positive face `D0-P-INVARIANT-MINIMAL-001` (row 555). The A2 cert already states the identity explicitly:

> `vp_a2_hypercharge_u1_mass_kernel.py`: "*Any operator that kills exactly B-L's coefficient is equivalent to the `ν^c`-localization bridge already recorded as `ASSUMP-KERNEL-CHARGE-LOCALIZATION`, not a forced graph-flow operator.*"

---

## 2. Exact compute (companion cert `attack_f7_check.py`, stdlib/Fraction, no load-bearing floats)

| check | statement | result |
|---|---|---|
| C1 | codim split: `dim ker(A)=30`, codim(LOC)=3 vs `dim span{Y,B−L}=2`, codim(CHG)=1 | PASS |
| C2 | Aut-invariant covector space = fixed space of `S₉×S₁₁×S₁₃` = `span{1₉,1₁₁,1₁₃}`, **dim 3** (computed by solving the within-zone constancy constraints, not asserted) | PASS |
| C3 | every Aut-invariant (zone-constant) covector **vanishes on** every within-zone difference mode of `ker(A)` | PASS |
| C4 | `Y_{ν^c}` is a **single-vertex** covector, **not zone-constant** ⇒ not Aut-invariant ⇒ M1-forbidden charge label | PASS |
| C5 | **0** Aut-invariant covectors separate two same-zone vertices = the selector no-go statement (0 within-zone-separating invariant readings) | PASS |
| N1 | control: a **zone-constant** charge WOULD be Aut-invariant ⇒ the kill is genuinely **single-vertex-gated** | PASS |
| N2 | control: the LOCALIZATION leg (`ker A`=30-dim) survives with **no reference to any charge covector** | PASS |
| N3 | control: legs have **different codimension** (3 ≠ 1) ⇒ the ASSUMP genuinely **bundles** two objects | PASS |

`--selftest` mutation battery (each mutation MUST flip its target; content-free checks exit non-zero):
`equate_codim → C1 FAILS` ✓ · `zone_const_Yc → C4 FAILS` ✓ · `kernel_not_balanced → C3 FAILS` ✓. **Selftest PASS** (every check is falsifiable).

---

## 3. Pre-registered attack surface — adjudicated

1. **Is `ν_R∈ker(A)` genuinely OWNED, or itself a physics-map choice?** — **Split answer (honest).** Kernel *structure* CERT-CLOSED (owned exact math); physical *identification* is the R2 MECH-LIMIT (external, already registered). So the LOC leg is **not** fully Core. The consolidation survives because (a) the owned structure carries the codimension-3 fact that separates the legs, and (b) the LOC external is the *same* R2 MECH-LIMIT, not a new one — F7's external residue is therefore **one selector-no-go charge label**, plus the pre-existing R2 MECH-LIMIT on the identification. Not "two fresh externals."
2. **Is the charge leg IDENTICALLY the selector no-go, or merely analogous?** — **Identical mechanism** (C5). The selector no-go is about within-zone *labelings*; `Y_{ν^c}` is a *covector reading a vertex*. Both are M1-legal-rule-invariant readings that must **distinguish two same-zone vertices**, and both die by the *same* free-transitivity argument: `Aut` acts transitively within a zone, so any invariant object is zone-constant, so it cannot separate same-zone vertices. C5 computes exactly this (0 separators). The covector/labeling difference is presentation, not mechanism.
3. **Do NOT claim F7 closed.** — Honored. Verdict is CONSOLIDATED; status of the hypercharge rows stays **NO-GO / bridge-assumptions-explicit**.

---

## 4. Independent skeptic pass (§05.8.R, kill-mandate) — accept/repair

**Primary kill target:** real consolidation, or superficial re-labeling? + is the localization ownership honest?

- **K1 (re-labeling?).** *Attempted kill:* "covector ≠ labeling; calling the charge leg the selector no-go is a naming trick." *Adjudication — NO KILL.* C5 exhibits the *shared theorem*: 0 `Aut`-invariant covectors separate two same-zone vertices, which is the free-transitive-within-zone fact that also gives the selector no-go's 0 invariant labelings. Same group action, same obstruction, same LEAN_PROVED owner (row 549). The A2 cert independently states the equivalence in print. Mechanism-identity established, not asserted.
- **K2 (localization over-owned?).** *Attempted kill:* "the memo leans on `ν_R∈ker A` being owned; it is a MECH-LIMIT." *Adjudication — PARTIAL, repaired.* The seed's "OWNED" was too strong. Repair applied throughout §0/§1.2/§3: LOC is **owned-structure + MECH-LIMIT-identification**. This *weakens* the LOC leg but does not touch the CHG-leg = selector-no-go finding, which is the load-bearing consolidation. The memo now states owned-vs-external precisely.
- **K3 (does the split change status?).** *Attempted kill:* "if you split it, do you smuggle a closure?" *Adjudication — NO KILL.* No status flip proposed. Both legs remain external (LOC: R2 MECH-LIMIT; CHG: selector no-go). The split is a *sharpening of the same NO-GO/bridge*, filing it under the owned selector family. `053040` untouched; no commit.

**Skeptic verdict:** **NO KILL** on the consolidation; **one repair applied** (localization ownership grade corrected from OWNED → owned-structure + MECH-LIMIT-identification).

---

## 5. Owned vs external — honest final statement

| object | grade |
|---|---|
| 30-dim zone-balanced kernel structure (`ker A`, split 8+10+12) | **OWNED** (CERT-CLOSED exact linear algebra) |
| identification "kernel = the neutrino `ν_R`" (LOC leg) | **EXTERNAL** — R2 graph→physics MECH-LIMIT (`D0-GRAPH-SPACE-NO-ISOMETRY-001`), already registered |
| anomaly variety `span{Y,B−L}`, rank-3, denominator-6 | **OWNED** (rows 361 / SM-HYPERCHARGE-MINIMAL-DENOMINATOR) |
| charge label `Y_{ν^c}=0` (CHG leg) | **EXTERNAL** — M1-forbidden single-vertex covector = **corollary-of** `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` / `P-INVARIANT-MINIMAL` |
| F7 hypercharge-row selection overall | **NO-GO / bridge** — unchanged; now typed as owned-structure + two externals, one of which is the selector-no-go child |

---

## 6. Proposed row-notes (owner-gated; NOT applied — memo only, no commit)

Split the assumption into two legs and add a `corollary-of` edge on the hypercharge rows. **No status flip.**

1. **`LEAN_ASSUMPTION_LEDGER.csv:25` (`ASSUMP-KERNEL-CHARGE-LOCALIZATION`)** — proposed justification addendum:
   > SPLIT[2026-07-07]: this assumption bundles TWO distinct-codimension objects (BOOK_04:1408, ATTACK_F7_SELECTOR_CHILD_MEMO): (LOC) `ν_R∈ker A`, codim 3 — kernel STRUCTURE CERT-CLOSED, physical identification = R2 MECH-LIMIT `D0-GRAPH-SPACE-NO-ISOMETRY-001`; (CHG) `Y_{ν^c}=0`, codim 1 — M1-forbidden single-vertex charge label, **corollary-of `D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` / `D0-P-INVARIANT-MINIMAL-001`** (0 Aut-invariant covectors separate same-zone vertices; attack_f7_check.py C5). Status unchanged (PHYSICS_DICTIONARY / EXPLICIT); F7 does NOT close.

2. **`theory_status_map.csv:361` (`D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`)** and the F7-INTERFACE note there — proposed cross-link addendum (row unchanged):
   > F7-SELECTOR-CHILD[2026-07-07]: the single gate ASSUMP-KERNEL-CHARGE-LOCALIZATION splits (ATTACK_F7_SELECTOR_CHILD_MEMO): its CHARGE leg `Y_{ν^c}=0` is corollary-of D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 / P-INVARIANT-MINIMAL (single-vertex covector not Aut-invariant, vanishes-on-kernel). LOC leg = owned kernel structure + R2 MECH-LIMIT identification. F7 raised from physics-dictionary black box to owned-localization + selector-no-go charge residue; NO status change.

3. **Optional** — a `corollary-of` edge `D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 --charge-leg--> D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001` in `theory_graph.json` (owner decision; regen via `sync_theory_status_map.py`, never edit the generated file by hand — per registry source-of-truth).

**All motions HELD (owner-gated). No file in the corpus modified by this memo except the two new files in `_TASKS_CENTER_ATTACK/`.**
