# CLAY-CORE INTERNAL-FORCING AUDIT (DRAFT — proposal only, pre-skeptic)

**Task**: audit the three "Clay-core" internal-forcing bridge assumptions flagged as each carrying
~100% of their claim's weight and reading as "the whole problem assumed", with none de-listed or
honestly re-scoped.

> **Provenance of the flag (Skeptic #1 repair #4, accepted).** This "~100% weight / whole problem
> assumed / none de-listed" flag is quoted here from the **task prompt**, and is a *paraphrase*. It
> was NOT located verbatim in an owned referee source: `D0_REFEREE_ASSESSMENT.md` (180 lines) and
> `D0_REVIEW_REPORT.md` (62 lines) were both searched (grep for `clay|hodge|lyapunov|riemann|
> reflection|bridge|assum|100|whole problem|de-list|re-scop`) and **neither mentions these three
> Clay-core bridge assumptions or this flag**. A corpus-wide grep for `"whole problem assumed"` /
> `"100% of … weight"` returns **only this memo**. So the flag has no located referee-owned
> file:line citation; it is treated as the task's framing, not as a verbatim referee finding. All
> *other* citations in this memo (Lean, ledger, registry) are owned and quoted verbatim.

**Scope discipline (binding)**: this memo is a *proposal*. It makes NO edits to
`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`, the `LEAN_ASSUMPTION_LEDGER.csv`, or any
built `.lean`. All registry/ledger motions below are drafts. Lean is shown as code blocks only.
Language is candidate/DRAFT throughout; no "forced/closed/derived" verdict is asserted before an
adversarial skeptic pass. An honest bridge that must be IMPORTED is a VALID G2 closure when it is
explicit, minimal, and labelled — never hidden as "derived".

**The three assumptions (ledger rows 21–23)** map 1:1 to the three Millennium reformulations:

| # | assumption_id | claim_id | Millennium problem |
|---|---------------|----------|--------------------|
| A | `ASSUMP-HODGE-ALGEBRAIC-FORCING` | `D0-HODGE-M1-REDUCTIO-001` | Hodge conjecture (§28) |
| B | `ASSUMP-PACKAGING-REFLECTION-SYMMETRY` | `D0-RIEMANN-AXIS-M1-001` | Riemann hypothesis (§29) |
| C | `ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL` | `D0-PVSNP-LYAPUNOV-M1-001` | P vs NP (§24) |

---

## Headline finding (DRAFT)

At the **registry/ledger plumbing level**, all three are already honest: each dependent claim is
tagged `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, carries `uses_bridge_assumptions=True`, names its
`assumption_id`, states a `failure_meaning`, and passes `STATUS_INFLATION_AUDIT`
(`open_inside_prose=no`, `contradiction=none`). So the referee's "none de-listed / never
re-scoped" charge is **not** a plumbing gap.

The real asymmetry is **conditional-vs-unconditional**, and it splits the three into two classes.

> **Correction (Skeptic #1, accepted in full).** An earlier draft of this memo grounded the split
> on `M1Predicate.lean:44-49` — claiming that criterion supplies "a real score behind `Forced`" that
> A/C fail and B passes, and that A/C are the "standalone `¬Forced` shell the module declares
> content-free." **That grounding was a MISATTRIBUTION and is withdrawn.** The actual :44-49
> criterion is whether the `m1_*` lemma is *stated against an `M1Forced` hypothesis* versus *as a
> standalone `:= ¬Forced` shell* — and **all three theorems route through an `M1Forced` witness**, so
> by that test A/C **pass equally with B**. See the verbatim quote and the three witness citations in
> the "Re-grounding" block below. The true B-vs-A/C asymmetry is stated next and does not rest on
> :44-49.

- **B (Riemann) — HONEST (unconditional witness).** The `M1Forced` witness `half_is_m1_forced_axis`
  (`CriticalAxisM1.lean:33-35`) is proven **unconditionally**: `forced := norm_num`,
  `unique := linarith` over `ℝ`, with no assumed structure field. The residual weight is a genuinely
  *external* bridge (the claim that the packaging symmetry IS the reflection `s ↦ 1-s`). No assumed,
  never-instantiated field inside the Lean.

- **A (Hodge) and C (Lyapunov) — CONDITIONAL (witness derived from an assumed field).** Their
  `M1Forced` witnesses (`hodge_algebraic_m1_forced H` / `solution_m1_forced N`) are **derived from an
  assumed structure field** — `H.algebraic_forced` (`HodgeAlgebraicRealization.lean:39`) /
  `N.solution_forced` (`HeatTraceLyapunov.lean:33`) — that is **never instantiated** anywhere in the
  corpus (`KappaStableHodgeClass` / `LyapunovNavigable` occur 4× each: the `structure` + 3 theorems
  taking it as a hypothesis; no `example`/witness `def`). The reductio therefore carries no content
  beyond the assumed uniqueness: **conditional on an un-discharged bridge field**. This is *not* the
  ":44-49 shell" case — the lemmas ARE stated against a real `M1Forced` hypothesis; the defect is that
  the `M1Forced` witness is itself only *hypothetical* (assumed field), not *proven* as B's is.

DRAFT verdicts per assumption follow, each with verbatim citation, weight analysis, and the exact
proposed motion. Every appearance of the withdrawn ":44-49 shell" grounding below has been corrected
to the conditional-vs-unconditional asymmetry.

<!-- SECTIONS APPENDED BELOW -->

---

## Re-grounding (post-Skeptic #1): what `M1Predicate.lean:44-49` actually says, and the true asymmetry

**Verbatim, `D0/Foundation/M1Predicate.lean:44-49`:**

> "**Load-bearing only with a real `Forced`.** This definition is `¬ Forced b`; it carries content
> *only* when `Forced` is an actual finite obligation (e.g. `StrictSelected S ·`, `admissible_unique`).
> A bare `¬ Forced` over a vacuous `Forced` is not a theorem about anything. The `m1_*` lemmas below
> are therefore always stated *against an `M1Forced` hypothesis* (a real `forced ∧ unique` obligation),
> and every instance in this file (`demoSelector`, `seamDegreeSelector`) discharges that obligation
> through the proven `StrictSelected` / `strict_selected_unique` spine — never as a standalone
> `:= ¬Forced` shell."

**The criterion is "stated against an `M1Forced` hypothesis" vs "standalone `:= ¬Forced` shell."**
All three §-reductios route their `RequiresExternalCatalogue` (= `¬Forced`) conclusion through an
`M1Forced` witness — so **all three PASS this test**:

- Hodge: `m1_alternative_needs_catalogue (hodge_algebraic_m1_forced H) …`
  (`HodgeAlgebraicRealization.lean:53`), where `hodge_algebraic_m1_forced H : M1Forced …`
  (`:42-44`).
- Lyapunov: `m1_alternative_needs_catalogue (solution_m1_forced N) …`
  (`HeatTraceLyapunov.lean:53`), where `solution_m1_forced N : M1Forced …` (`:36-38`).
- Riemann: `m1_alternative_needs_catalogue half_is_m1_forced_axis …`
  (`CriticalAxisM1.lean:46`), where `half_is_m1_forced_axis : M1Forced …` (`:33-35`).

So `:44-49` does **not** discriminate A/C from B. The real asymmetry is one level up, in *how the
`M1Forced` witness is obtained*:

| | `M1Forced` witness | how obtained | conditional? |
|---|---|---|---|
| **B** Riemann | `half_is_m1_forced_axis` (`:33-35`) | `forced := norm_num`, `unique := linarith` — **proven** | **unconditional** |
| **A** Hodge | `hodge_algebraic_m1_forced H` (`:42-44`) | `selector_M1Forced … H.algebraic_forced` — **from assumed field** (`:39`) | conditional |
| **C** Lyapunov | `solution_m1_forced N` (`:36-38`) | `selector_M1Forced … N.solution_forced` — **from assumed field** (`:33`) | conditional |

B's witness is a proven fact; A/C's witnesses are `selector_M1Forced` applied to a structure field
(`algebraic_forced` / `solution_forced`) that is **never instantiated** in the corpus. That — not a
:44-49 shell — is the honest discriminant.

---

## A. `ASSUMP-HODGE-ALGEBRAIC-FORCING` → `D0-HODGE-M1-REDUCTIO-001` (§28 Hodge)

### Verbatim text

Ledger (`09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv:21`), justification field:

> "[Iter20] The hypothesis that the canonical finite cohomology data M1-forces (strictly selects)
> the algebraic realization. This is the sect28 content (kappa-stable rational class => algebraic)
> assumed as a structure field, NOT derived. It is a D0-INTERNAL named target (not an external
> classical theorem); deriving the strict selection from kappa-stability + the finite cohomology
> functional is the open work. The reductio (non-algebraic => external catalogue) is proven
> CONDITIONAL on it via D0.Foundation.m1_alternative_needs_catalogue."

`failure_meaning` (same row): "the sect28 reductio stays conditional on the algebraic-forcing
hypothesis; that hypothesis is the named open content."

Lean, the assumption itself (`D0/Topology/HodgeAlgebraicRealization.lean:35-39`):

> ```lean
> structure KappaStableHodgeClass where
>   realizationSelector : FiniteSelector HodgeRealization
>   /-- `ASSUMP-HODGE-ALGEBRAIC-FORCING`: the canonical finite data strictly selects (M1-forces) the
>   algebraic realization. This is the §28 content (κ-stable ⇒ algebraic), assumed here, not derived. -/
>   algebraic_forced : StrictSelected realizationSelector HodgeRealization.algebraic
> ```

Lean, the dependent "reductio" theorem (`HodgeAlgebraicRealization.lean:50-54`):

> ```lean
> theorem hodge_nonalgebraic_needs_catalogue (H : KappaStableHodgeClass) :
>     RequiresExternalCatalogue (fun x => StrictSelected H.realizationSelector x)
>       HodgeRealization.nonAlgebraicIndex :=
>   m1_alternative_needs_catalogue (hodge_algebraic_m1_forced H)
>     HodgeRealization.nonAlgebraicIndex (by decide)
> ```

### What it assumes

That there exists a finite score selector on `{algebraic, nonAlgebraicIndex}` whose **strict
minimum is `algebraic`** — i.e. `StrictSelected realizationSelector HodgeRealization.algebraic`
holds. In plain terms: that a κ-stable rational Hodge class *is* algebraic. That is the Hodge
conjecture's content (D0-reformulated), taken as an uninstantiated structure field.

### What carries the claim's weight

100% of it. The theorem `hodge_nonalgebraic_needs_catalogue` unfolds to:
`RequiresExternalCatalogue Forced b := ¬ Forced b`, discharged by
`m1_alternative_needs_catalogue`, which is nothing but `a ≠ b ∧ (a is the unique Forced) ⇒ ¬Forced b`
(Foundation `M1Predicate.lean:61-64`). The *only* non-trivial input is `algebraic_forced` — the
assumed strict selection. Everything downstream is `by decide` on `algebraic ≠ nonAlgebraicIndex`
and the generic uniqueness reductio.

**Where the weight actually sits (corrected — NOT a :44-49 shell).** The `M1Forced` obligation IS
stated (`hodge_algebraic_m1_forced H`, `:42-44`), so this reductio passes the :44-49 test exactly as
B does — it is **not** the "standalone `¬Forced` shell" case. The defect is one level up: that
`M1Forced` witness is built by `selector_M1Forced H.realizationSelector … H.algebraic_forced`, and
`algebraic_forced` (`HodgeAlgebraicRealization.lean:39`) is an **assumed structure field that is
never instantiated**. `KappaStableHodgeClass` occurs 4× in the corpus (the `structure` plus 3
theorems taking `H` as hypothesis); there is **no `example`, no witness `def`, no populated
`FiniteSelector HodgeRealization`**. So the witness is *hypothetical, not proven* — the reductio is
**conditional** on an un-discharged bridge field, and that field is the Hodge content.

*(For contrast, the Foundation demos DO discharge their obligation with a proven score —
`demoSelector.score i := (i.val:ℚ)` (`M1Predicate.lean:81-84`), `seamDegreeSelector.score d :=
((d.val:ℚ)-(w.val:ℚ))^2` (`:103-105`) — and B's witness is likewise proven. A's is not; that is the
gap. This is a conditional-vs-unconditional distinction, NOT the populated-vs-shell distinction
:44-49 draws.)*

### Verdict (DRAFT): CONDITIONAL on an un-discharged bridge field (theorem-content); HONEST at the ledger level.

The ledger row is honestly labelled (`D0_INTERNAL_FORCING_TARGET`, "NOT derived", failure_meaning
stated) and the claim is tagged `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`. The Lean is a genuine
conditional reductio whose entire non-trivial input is the assumed, never-instantiated
`algebraic_forced` field — so it reads as "the whole problem assumed" in the sense that its `M1Forced`
witness is hypothetical, not proven. That is the honest reading; it does **not** rest on any :44-49
"shell" claim (withdrawn above).

### Proposed motion (proposal only — pick ONE)

**(A1) No re-tag required; optional clarifying note only (revised post-Skeptic #1).**
The row is *already* `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` with `uses_bridge_assumptions=True`, a
named `assumption_id`, a stated `failure_meaning`, and it passes `STATUS_INFLATION_AUDIT`
(`open_inside_prose=no`, `contradiction=none`; verified `CLAIM_TO_LEAN_MAP.csv:282`,
`STATUS_INFLATION_AUDIT.csv:277`, ledger `:21`). Once the withdrawn ":44-49 shell" grounding is
removed, **the plumbing is already honest and the earlier re-tag is not warranted** — there is no
"unpopulated score" defect for :44-49 to flag; the honest fact is *conditional-on-an-assumed-field*,
which the existing tag + `assumption_type=D0_INTERNAL_FORCING_TARGET` + failure_meaning already
convey.

- **Re-tag: DROPPED.** The earlier proposal `D0_INTERNAL_FORCING_TARGET → …_UNPOPULATED_SELECTOR`
  **mislabelled** the gap as missing score instantiation, which is not what :44-49 flags. No
  `assumption_type` change is proposed. (If a label were ever wanted, the accurate one is
  `_ASSUMPTION_DERIVED_M1FORCED` — the `M1Forced` witness is derived from an assumed field — but even
  that is redundant with the current honest row.)
- **Optional note only** (DRAFT `CLAIM_TO_LEAN_MAP.csv` note append, row 282): "AUDIT-CLAY-CORE: the
  reductio's `M1Forced` witness `hodge_algebraic_m1_forced` is derived from the assumed, never-
  instantiated field `algebraic_forced` (`FiniteSelector HodgeRealization` has no witness `def`); the
  theorem is conditional on that field. Contrast Riemann (`half_is_m1_forced_axis` is unconditional).
  Weight = 100% on the named assumption. This is NOT the M1Predicate.lean:44-49 `¬Forced`-shell case —
  the lemma IS stated against an `M1Forced` hypothesis."

**(A2) Discharge the D0 hypotheses (the real close, larger).** Populate
`realizationSelector : FiniteSelector HodgeRealization` with an actual `score` built from the finite
cohomology functional (the κ-stability energy), and *prove* `StrictSelected ... algebraic` from
κ-stability — as `seamDegreeSelector` proves `seam_degree_strictly_selected` from `(d-w)²`. Only then
does the reductio acquire content and the assumption stop being the claim. This is the "open work"
the ledger already names; it is NOT done here and is likely Hodge-hard.

**Recommendation**: A1 (no re-tag; optional note only) — the row is already an honest G2 closure;
A2 flagged as the open target.

---

## B. `ASSUMP-PACKAGING-REFLECTION-SYMMETRY` → `D0-RIEMANN-AXIS-M1-001` (§29 Riemann)

### Verbatim text

Ledger (`09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv:22`), justification field:

> "[Iter20] The hypothesis that the canonical D0 spectral-packaging functional equation IS the
> reflection s|->1-s and that its zeros/critical data lie on the reflection-fixed axis. The Lean
> facts (1/2 = unique fixed point of sigma|->1-sigma; shifted axis needs a catalogue) are elementary
> and UNCONDITIONAL; the RH-content (that the packaging symmetry is this reflection) is assumed not
> derived, a named target (a property of the profinite-limit packaging). NOT the ZFC Riemann
> statement about the zeta function."

`failure_meaning`: "the sect29 axis result is conditional on the packaging having the s|->1-s
reflection symmetry; given it, Re=1/2 is forced (proven)."

Lean, the constraint and the unconditional core (`D0/Spectral/CriticalAxisM1.lean:29-39`):

> ```lean
> def ReflectionFixed (σ : ℝ) : Prop := σ = 1 - σ
>
> theorem half_is_m1_forced_axis : M1Forced ReflectionFixed (1 / 2) where
>   forced := by unfold ReflectionFixed; norm_num
>   unique := fun σ hσ => by unfold ReflectionFixed at hσ; linarith
> ```

### What it assumes

The assumption is *external* to the Lean file: that the D0 spectral-packaging functional equation
IS the reflection `s ↦ 1 - s`, and that the packaging's zeros lie on its fixed axis. The Lean does
NOT assume this; it takes `ReflectionFixed` as given and proves `1/2` is its unique fixed point.

### What carries the claim's weight

Split, and honestly so. Two distinct pieces:

1. **Inside Lean (UNCONDITIONAL, real content):** `half_is_m1_forced_axis` (`CriticalAxisM1.lean:33-35`)
   genuinely proves over `ℝ` that `1/2 = 1 - 1/2` (`forced := norm_num`) and is the *unique* such `σ`
   (`unique := linarith`). This `M1Forced` witness is **proven with no assumed structure field** — that
   is the discriminant from A/C, whose witnesses are `selector_M1Forced` of an assumed field. (All
   three route through an `M1Forced` hypothesis, so all three pass :44-49 equally; the difference is
   that B's witness is *proven* and A/C's are *hypothetical*.) Hence `shifted_axis_needs_catalogue`
   (`CriticalAxisM1.lean:44-47`) is unconditional content.

2. **The bridge (`ASSUMP-PACKAGING-REFLECTION-SYMMETRY`):** the identification "packaging symmetry =
   this reflection" + "zeros on the fixed axis." This is where the RH weight sits — and it is
   correctly located *outside* the proven Lean, named, tagged, and disclaimed as "NOT the ZFC Riemann
   statement."

### Verdict (DRAFT): HONEST. Unconditional witness; no assumed field inside the Lean.

Unlike Hodge/Lyapunov, the `M1Forced` witness (`1/2` is the unique fixed axis) is *proven
unconditionally*, not derived from an assumed, never-instantiated field. The residual weight is an
honest **external** import (the packaging IS this reflection), which is exactly what a labelled bridge
assumption is for. This is a VALID G2 closure as-is.

### Proposed motion (proposal only)

**(B1) No re-tag required.** Keep `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`. Optional hardening: add a
one-line note distinguishing B from A/C so a future referee does not lump them —
DRAFT `CLAIM_TO_LEAN_MAP.csv` note append (row 283): "AUDIT-CLAY-CORE: DISTINGUISHED from Hodge/PvsNP
— `half_is_m1_forced_axis` is an *unconditional* `M1Forced` witness (`norm_num`/`linarith`), not
derived from an assumed field; the fixed-axis fact is unconditional. Weight sits in the *external*
packaging-identification bridge, correctly labelled."

**(B2) Discharge the bridge (open target).** Derive `packaging functional equation = (s ↦ 1-s)` from
the profinite-limit packaging construction (`D0.Spectral.ZetaResidueAlpha`, cited in row 283). Not
done here; genuinely RH-hard. Flag as open, not required for honest closure.

---

## C. `ASSUMP-GLOBAL-LYAPUNOV-POTENTIAL` → `D0-PVSNP-LYAPUNOV-M1-001` (§24 P vs NP)

### Verbatim text

Ledger (`09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv:23`), justification field:

> "[Iter20] The hypothesis that a global heat-trace Lyapunov navigation potential V exists that
> strictly selects the accepting/solution state (V = lim u->inf e^{-uL} b with a uniform spectral
> gap). Assumed as a structure field, NOT derived: the corpus has the static
> symmetric/nonneg/zero-mode Laplacian (D0.Geometry.ArchiveLaplacianProperties) but no u->inf
> heat-flow limit and the uniform-across-tower spectral gap is assumed. Given V, the sect24 reductio
> (a promising-branch != solution requires an external branch-catalogue) is proven via
> D0.Foundation.m1_alternative_needs_catalogue. Regularized P_D0 vs NP_D0 at fixed UV; NOT the ZFC
> P=?NP question."

`failure_meaning`: "the NP_D0 subseteq P_D0 collapse is conditional on the existence of the global
Lyapunov potential V; without V the exogenous branch-catalogue is exactly the worst-case phase."

Lean, the assumption itself (`D0/Complexity/HeatTraceLyapunov.lean:30-33`):

> ```lean
> structure LyapunovNavigable (α : Type) where
>   potential : FiniteSelector α
>   solution : α
>   solution_forced : StrictSelected potential solution
> ```

Lean, the dependent reductio (`HeatTraceLyapunov.lean:50-53`):

> ```lean
> theorem branch_without_potential_needs_catalogue {α : Type} (N : LyapunovNavigable α)
>     (b : α) (hb : b ≠ N.solution) :
>     RequiresExternalCatalogue (fun x => StrictSelected N.potential x) b :=
>   m1_alternative_needs_catalogue (solution_m1_forced N) b hb
> ```

### What it assumes

That there exists a global potential `V` (as a `FiniteSelector α` with a `score`) whose strict
minimum is the accepting state — `solution_forced : StrictSelected potential solution`. The intended
`V = lim_{u→∞} e^{-uL} b` with a uniform spectral gap. Taken as an uninstantiated structure field.

### What carries the claim's weight

100% of it — structurally identical to Hodge (A). `branch_without_potential_needs_catalogue` is again
`m1_alternative_needs_catalogue (solution_m1_forced N) b hb`, i.e. the generic
`a≠b ∧ unique-Forced(a) ⇒ ¬Forced(b)` reductio. The sole non-trivial input is `solution_forced`.

**Same conditional-on-an-assumed-field defect (NOT a :44-49 shell).** As with Hodge, the `M1Forced`
obligation IS stated (`solution_m1_forced N`, `HeatTraceLyapunov.lean:36-38`), so the reductio passes
the :44-49 test exactly as B does. The defect is that this witness is
`selector_M1Forced N.potential … N.solution_forced`, and `solution_forced`
(`HeatTraceLyapunov.lean:33`) is an **assumed field that is never instantiated**: `LyapunovNavigable`
occurs 4× in the corpus (structure + 3 theorems taking `N` as hypothesis); `potential : FiniteSelector
α` is never given a `score` — no `e^{-uL}` limit, no `u→∞` heat flow, no witness `def`. The ledger
even concedes the corpus "has the static ... Laplacian ... but no u->inf heat-flow limit and the
uniform-across-tower spectral gap is assumed." So the witness is *hypothetical, not proven* — the
reductio is **conditional** on that un-discharged field.

### Verdict (DRAFT): CONDITIONAL on an un-discharged bridge field (theorem-content); HONEST at the ledger level.

Same as A. The ledger/registry labelling is honest and complete; the Lean reductio's entire
non-trivial input is the assumed, never-instantiated `solution_forced` field — "the whole problem
assumed" in the sense that its `M1Forced` witness is hypothetical, not proven. It does **not** rest on
any :44-49 "shell" claim (withdrawn above).

### Proposed motion (proposal only — pick ONE)

**(C1) No re-tag required; optional clarifying note only (revised post-Skeptic #1).**
The row is already `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` with `assumption_id`, `failure_meaning`, and
it passes `STATUS_INFLATION_AUDIT` (verified `CLAIM_TO_LEAN_MAP.csv:284`,
`STATUS_INFLATION_AUDIT.csv:279`, ledger `:23`). The plumbing is honest; the earlier re-tag is not
warranted.
- **Re-tag: DROPPED.** `COMPLEXITY_NAVIGATION_POTENTIAL → …_UNPOPULATED_SELECTOR` mislabelled the gap
  as missing score instantiation, which is not what :44-49 flags. No `assumption_type` change is
  proposed. (Accurate label if ever wanted: `_ASSUMPTION_DERIVED_M1FORCED`; redundant with the current
  row.)
- **Optional note only** (DRAFT `CLAIM_TO_LEAN_MAP.csv` note append, row 284): "AUDIT-CLAY-CORE: the
  reductio's `M1Forced` witness `solution_m1_forced` is derived from the assumed, never-instantiated
  field `solution_forced` (`potential : FiniteSelector α` has no `u→∞` heat flow / no score); the
  theorem is conditional on that field. Contrast Riemann (`half_is_m1_forced_axis` is unconditional).
  Weight = 100% on the named assumption. NOT the M1Predicate.lean:44-49 `¬Forced`-shell case — the
  lemma IS stated against an `M1Forced` hypothesis."

**(C2) Discharge the D0 hypotheses (the real close, larger).** Construct `V` as the heat-trace
relaxation from the existing `D0.Geometry.ArchiveLaplacianProperties`: build the `u→∞` limit
`lim e^{-uL} b`, *prove* the uniform-across-tower spectral gap, populate `potential.score` from it,
and derive `StrictSelected potential solution`. Only then is the reductio non-vacuous. Not done here;
the gap and the `u→∞` limit are the ledger's own named open work; likely P-vs-NP-hard.

**Recommendation**: C1 now; C2 flagged as the open target.

---

## Consolidated registry motion (DRAFT — proposal only, NOT applied)

| assumption | claim | honest verdict | motion | effect |
|---|---|---|---|---|
| A Hodge | `D0-HODGE-M1-REDUCTIO-001` | conditional on assumed field | A1 **no re-tag**; optional note only | plumbing already honest; note records the conditional-on-assumed-field reading |
| B Riemann | `D0-RIEMANN-AXIS-M1-001` | HONEST (unconditional witness) | B1 optional distinguishing note only | no change to status; keeps `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` |
| C P vs NP | `D0-PVSNP-LYAPUNOV-M1-001` | conditional on assumed field | C1 **no re-tag**; optional note only | same as A |

All three claims **stay** `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` (they already are, verified). The
referee-paraphrase "re-tag LEAN_PROVED → LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS" motion is **already
satisfied** in the registry. **Post-Skeptic #1, the earlier `_UNPOPULATED_SELECTOR` re-tags are
DROPPED** — they mislabelled the gap as a missing-score-instantiation defect, which is not what
:44-49 flags. The true asymmetry is conditional-vs-unconditional: A/C's `M1Forced` witnesses are
derived from assumed, never-instantiated fields; B's is proven. The optional notes record only that
distinction; they do NOT re-tag, do NOT downgrade below the current bridge tag, and do NOT claim a
close.

## Failure-meaning restatement (per the task's honest-bridge requirement)

- **A / C**: if the assumption fails (κ-stable class is NOT algebraic / no global `V` exists), the
  reductio says nothing — its `M1Forced` witness was hypothetical (built from the assumed field), so
  it never had content beyond the assumption. The Millennium content is entirely in the un-discharged
  `algebraic_forced` / `solution_forced` field. This is a labelled import, valid as a G2 closure
  because it is flagged as *conditional on an un-discharged bridge field*, never as "derived."
- **B**: if the assumption fails (packaging symmetry is NOT `s ↦ 1-s`), the unconditional `1/2`-axis
  fact survives but no longer connects to RH. The bridge is the identification; failure severs the
  Millennium link but leaves the proven kernel intact.

## Skeptic-facing self-attack (pre-registered; updated post-Skeptic #1)

- **Strongest attack on this memo (WAS the winning attack — accepted)**: "The verdict spine rests on
  `M1Predicate.lean:44-49` supplying a 'real score behind `Forced`' test that A/C fail and B passes,
  and on A/C being 'the standalone `¬Forced` shell the module declares content-free.' But :44-49's
  actual criterion is *stated against an `M1Forced` hypothesis* vs *standalone `:= ¬Forced` shell*,
  and all three route through an `M1Forced` witness — so A/C PASS equally with B. The citation is
  misattributed." **This attack landed. The :44-49 grounding is withdrawn throughout; the verdict is
  re-grounded on conditional-vs-unconditional** (B's witness proven; A/C's derived from an assumed
  field). See the repair log below.
- **Residual attack**: "Once :44-49 is removed, is anything left to say beyond the already-honest
  tag?" *Response*: yes, but it is a *documentation* observation, not a plumbing defect. The rows are
  already honest (`LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` + `assumption_id` + `failure_meaning`, pass
  `STATUS_INFLATION_AUDIT`). The audit's remaining value is the verified fact that A/C's `M1Forced`
  witnesses are *derived from never-instantiated fields* while B's is *proven* — captured in optional
  notes, no re-tag. If nothing more is wanted, the honest position is "no motion required; the rows
  are already a valid G2 closure."
- **Witness-existence attack**: "Maybe a witness selector exists elsewhere and the grep missed it."
  *Response*: `KappaStableHodgeClass` / `LyapunovNavigable` = 4 corpus occurrences each, all accounted
  for (structure def + 3 hypothesis-taking theorems); no `example`/witness `def`. If a future witness
  is added with a real score, A/C convert to B's unconditional class — that is exactly motion A2/C2.
- **Owned NO-GO respect**: this memo re-opens nothing. It cites the existing honest ledger rows and
  the Foundation module; the "derive the strict selection" work is already named-open in the ledger,
  not asserted closed here.

## Provenance (owned file:line citations, all quoted verbatim above)

- `09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv:21,22,23` (three justification + failure_meaning fields)
- `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:282,283,284` (three claim rows, all `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`)
- `09_LEAN_FORMALIZATION/D0/Foundation/M1Predicate.lean:44-49` (the load-bearing self-warning — its criterion is "stated against an `M1Forced` hypothesis" vs "standalone `:= ¬Forced` shell"; **it does NOT discriminate A/C from B** — all three pass it; see Skeptic #1 repair log), `:61-64` (the generic reductio), `:81-84`,`:103-105` (real-score demos)
- `09_LEAN_FORMALIZATION/D0/Topology/HodgeAlgebraicRealization.lean:35-39` (structure + assumed `algebraic_forced` field at `:39`), `:42-44` (`hodge_algebraic_m1_forced` — the `M1Forced` witness, derived from the assumed field), `:50-54` (the reductio)
- `09_LEAN_FORMALIZATION/D0/Spectral/CriticalAxisM1.lean:29-39` (`ReflectionFixed` + `half_is_m1_forced_axis` at `:33-35` — `M1Forced` witness proven UNCONDITIONALLY, `norm_num`/`linarith`), `:44-47` (the reductio)
- `09_LEAN_FORMALIZATION/D0/Complexity/HeatTraceLyapunov.lean:30-33` (structure + assumed `solution_forced` field at `:33`), `:36-38` (`solution_m1_forced` — the `M1Forced` witness, derived from the assumed field), `:50-53` (the reductio)
- `04_VERIFICATION/STATUS_INFLATION_AUDIT.csv:277,278,279` (all three: `open_inside_prose=no`, `contradiction=none`)
- `04_VERIFICATION/TOTAL_FINAL_CLAIM_INDEX.csv:277,278,279` (all three: `BRIDGE-ASSUMPTIONS-EXPLICIT`, `PASSPORT-CLOSED`)
- **Referee sources searched, flag NOT found**: `D0_REFEREE_ASSESSMENT.md`, `D0_REVIEW_REPORT.md` (see Provenance-of-the-flag box at top). The "~100% weight / whole problem assumed" flag is a task-prompt paraphrase, not an owned referee quote.

---

## Skeptic #1 verdict + repair log (accepted in full)

**Verdict: WOUNDED.** Accepted in full, no defense. The memo's structural observations survive in
weakened form (the rows are honest; A/C are conditional on un-discharged fields, B is unconditional),
but the *grounding* of the verdict was defective and is repaired below. All four repairs applied;
load-bearing changes re-verified against source.

### Errors of record

1. **MISATTRIBUTED CITATION of `M1Predicate.lean:44-49` (the strongest finding).** The original memo
   made the verdict spine (A/C = "over-claim shell", B = "honest populated") and both `_UNPOPULATED_
   SELECTOR` re-tags rest on the claim that :44-49 supplies an objective test — "a real score behind
   `Forced`" — that A/C fail and B passes, and that A/C are "the standalone `¬Forced` shell the module
   declares content-free." **False.** Verified verbatim (`M1Predicate.lean:44-49`): the actual
   criterion is whether the `m1_*` lemma is *"stated against an `M1Forced` hypothesis"* vs *"as a
   standalone `:= ¬Forced` shell."* All three §-reductios route through an `M1Forced` witness
   (`hodge_algebraic_m1_forced H`, `HodgeAlgebraicRealization.lean:42-44`; `solution_m1_forced N`,
   `HeatTraceLyapunov.lean:36-38`; `half_is_m1_forced_axis`, `CriticalAxisM1.lean:33-35`), so **A/C
   PASS the :44-49 test equally with B.** *Repair*: every :44-49-as-discriminant claim withdrawn;
   verdict re-grounded on conditional-vs-unconditional (B's `M1Forced` witness proven by
   `norm_num`/`linarith`; A/C's derived from the assumed, never-instantiated fields
   `algebraic_forced`/`solution_forced`).

2. **MISLABELLED re-tag `_UNPOPULATED_SELECTOR`.** It framed the gap as missing *score instantiation*
   (a :44-49-shell defect), which is not the actual defect. *Repair*: re-tag **DROPPED** for both A
   and C. If a label were ever wanted the accurate one is `_ASSUMPTION_DERIVED_M1FORCED`, but it is
   redundant with the already-honest row, so no `assumption_type` change is proposed.

3. **UNREBUTTED self-attack #1 once :44-49 is removed.** The three rows already carry
   `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS` + `assumption_id` + `failure_meaning` and pass
   `STATUS_INFLATION_AUDIT` (verified `CLAIM_TO_LEAN_MAP.csv:282-284`,
   `STATUS_INFLATION_AUDIT.csv:277-279`, `LEAN_ASSUMPTION_LEDGER.csv:21-23`). With :44-49 gone there
   is no plumbing defect to motion against. *Repair*: motions demoted to **optional clarifying notes,
   no re-tag**; the honest position is recorded as "the rows are already a valid G2 closure; the
   audit's residual value is the verified conditional-vs-unconditional distinction."

4. **REFEREE FLAG NOT QUOTED VERBATIM.** The memo cited the "~100% weight / whole problem assumed /
   none de-listed" flag as if referee-owned; it was only the task-prompt paraphrase (self-admitted).
   *Repair*: searched `D0_REFEREE_ASSESSMENT.md` (180 lines) and `D0_REVIEW_REPORT.md` (62 lines) —
   **neither contains the flag or any mention of these three Clay-core assumptions**; a corpus-wide
   grep for the phrasing returns only this memo. Added an explicit Provenance-of-the-flag box marking
   it a task-prompt paraphrase with no located referee citation.

### Re-verification of load-bearing changes (post-repair)

- `M1Predicate.lean:44-49` criterion re-read in full and quoted verbatim in the Re-grounding block;
  confirmed it is *hypothesis-shape* not *score-population*. ✓
- All three `M1Forced` witnesses located and classified: B unconditional (`:33-35`, `norm_num`/
  `linarith`); A/C conditional on assumed fields (`HodgeAlgebraicRealization.lean:39`,
  `HeatTraceLyapunov.lean:33`), each never instantiated (4 corpus occurrences each). ✓
- Registry parity re-verified: all three `LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, `uses_bridge_
  assumptions=True`, named `assumption_id`, `open_inside_prose=no`, `contradiction=none`
  (`CLAIM_TO_LEAN_MAP.csv:282-284`, `STATUS_INFLATION_AUDIT.csv:277-279`, ledger `:21-23`). ✓
- Referee-source absence re-verified by grep. ✓

### Residual (what is open / bridge-ledger-ready)

- **No motion strictly required.** The three rows are already an honest G2 closure. The only optional
  drafts are the clarifying `CLAIM_TO_LEAN_MAP.csv` notes (rows 282/283/284) recording the
  conditional-vs-unconditional distinction — proposal only, not applied.
- **Still open (unchanged, ledger's own named targets):** motion A2 (derive `StrictSelected …
  algebraic` from κ-stability, populate the Hodge selector) and C2 (construct `V = lim_{u→∞} e^{-uL}b`
  with a uniform spectral gap, populate the Lyapunov potential) — the real closes, likely
  Hodge-/P-vs-NP-hard. B2 (derive `packaging = s↦1-s` from the profinite-limit packaging) —
  genuinely RH-hard.
- **Bridge-ledger status:** all three remain valid, honestly-labelled bridge assumptions. No new
  bridge assumption is minted; no NO-GO re-opened.

*End of DRAFT memo + Skeptic #1 repair log. Proposal only — no registry/ledger/built-`.lean` edits
applied. Candidate language throughout; no "forced/closed/derived" asserted.*
