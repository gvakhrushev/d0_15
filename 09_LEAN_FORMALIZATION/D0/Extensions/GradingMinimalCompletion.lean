import D0.Extensions.RepresentationReadoutExtension

/-!
# Grading-axis minimal-completion selection — the E1 no-go's positive face (DRAFT)

Claim: `D0-GRADING-MINIMAL-COMPLETION-SELECTION-001` (candidate). Memo:
`_TASKS_CENTER_ATTACK/GRADING_MINIMAL_COMPLETION_MEMO.md`. Synthesis source: the owner's
directive "no-go как источник прорывов" — this is the P-M1-SATURATION pattern applied to the
E1 two-completion front (`D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001`).

The E1 no-go stands UNCHANGED: no admissible DATUM selects between the grading signatures —
`(2,1)` and `(3,0)` are both anomaly-free and `S₃`-symmetric with divergent neutral-current
counts (`8 ≠ 12`). What THIS module adds is the no-go's positive face, in two machine-checked
steps:

1. **Exhaustion of the grading-SIGNATURE subclass (discharges the audit's named deficit).**
   The signatures on the 3-dimensional generation block (the `U3_inner` quotient of gradings —
   cite `D0-X5-G-SYMMETRY-001`; the grading OPERATOR stays unforced = the missing PRIM) are
   EXACTLY the `p + q = 3` list `[(3,0), (2,1), (1,2), (0,3)]` — a kernel-checked iff, both
   directions (`grading_axis_exhaustive`). The strength audit (`TWO_COMPLETION_WITNESS_AUDIT
   .csv` E1 = "exhaustion … on the scoped grading-signature subclass; no in-module
   forall-class theorem") had already GRANTED the scoped exhaustion; what was missing — the
   in-module forall-class theorem — is discharged here. E1's classification stays
   CLASS-SCOPED (the Weyl-role `S₃` axis and the operator-level class are NOT touched).
2. **Extremality selection by the OWNED P-schema functional.** The umbrella
   `D0-P-M1-SATURATION-001` already uses commutant-dimension minimization as an owned
   order/valuation functional (its COLOUR instance minimizes exactly a commutant dimension).
   `ncCount p q = p² + q² + 3` IS the grading-even commutant dimension (E1's own definition).
   Applied to the exhausted signature subclass: the minimum is `8`, attained EXACTLY by the
   flip pair `{(2,1), (1,2)}` (`min_attained_iff`), i.e. ONE signature class up to the
   grading-sign relabel `Γ ↦ −Γ` (`minimizers_flip_pair` — the up-to-sign two-class split is
   already narrated in `TypedRepresentationFunctorClassification.lean:13-15`, cited); the
   maximal signatures `(3,0)/(0,3)` are IN-CLASS non-minimizers carrying a saturation SURPLUS
   of `12 − 8 = 4` grading-even channels no admissible datum demands (`saturation_surplus`).
   NOTE (skeptic #20): this row is P-schema-ADJACENT, not "instance #5" — the schema's
   witness-just-past slot requires an OUTSIDE-class witness (that slot is held by the missing
   PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR / PRIM-FINITE-SPECTRAL-TRIPLE-REP), and the schema's
   X_core slot is empty here (the completion is external by construction). Only the
   FUNCTIONAL-FAMILY membership (commutant-dimension minimization) is shared with row 556.
   CONVERGENT OWNED CANDIDATE (cited, not consumed): `q8FSsignature = (2,1)`
   (`TypedRepresentationFunctorClassification.lean:32-36`, the Q₈ Frobenius–Schur route,
   gated by the external KO-convention `J²=±1`) points at the SAME minimal class — two
   independent fingers, neither owned as a selector; "no admissible datum selects" stands.

Honest grading (per the P-row precedent and the E1 audit):
* The no-go is NOT weakened: "no admissible datum selects" remains true and is re-stated here;
  the selection is by the OWNED extremality principle, not by a datum. Whether the M1/MDL
  reading (B00:471 — adding underivable structure lengthens the law) LICENSES applying the
  commutant-minimality functional to external completions is the NARRATED leg — exactly
  parallel to the P-umbrella's second-order schema leg, PROOF-TARGET, not machine-checked.
* The residual freedom inside the minimum — `(2,1)` vs `(1,2)` — is the grading-SIGN flip.
  Its status (relabel/torsor à la row 549, or physical) is a NAMED OPEN sub-question; this
  module proves only that the two minimizers are `Prod.swap` of each other.
* Numerological observation, NOT built upon (trap d): `ncCount 2 1 = 8 = dim ℂ[Q₈]` (the
  weak-commutant wall's `8 < 9`). Recorded as CHK-grade observation only.
-/

namespace D0.Extensions.GradingMinimalCompletion

open D0.Extensions.RepresentationReadoutExtension

/-- **Exhaustion of the grading axis.** The signatures on the 3-dim generation block are
exactly the `p + q = 3` pairs, and `gradingSignatures` lists ALL of them: the class is whole,
not a witness sample. -/
theorem grading_axis_exhaustive :
    ∀ p q : ℕ, p + q = 3 ↔ (p, q) ∈ gradingSignatures := by
  intro p q
  constructor
  · intro h
    have hp : p ≤ 3 := by omega
    interval_cases p
    · obtain rfl : q = 3 := by omega
      simp [gradingSignatures]
    · obtain rfl : q = 2 := by omega
      simp [gradingSignatures]
    · obtain rfl : q = 1 := by omega
      simp [gradingSignatures]
    · obtain rfl : q = 0 := by omega
      simp [gradingSignatures]
  · intro h
    fin_cases h <;> simp

/-- The neutral-current values over the whole class: `[12, 8, 8, 12]`. -/
theorem nc_values : gradingSignatures.map (fun s => ncCount s.1 s.2) = [12, 8, 8, 12] := by
  decide

/-- **The floor.** Every admissible signature has `ncCount ≥ 8`. -/
theorem nc_floor : ∀ s ∈ gradingSignatures, 8 ≤ ncCount s.1 s.2 := by
  decide

/-- **Extremality selection.** The floor `8` is attained EXACTLY by `(2,1)` and `(1,2)` —
the minimizer set over the WHOLE class is the flip pair, nothing else. -/
theorem min_attained_iff :
    ∀ s ∈ gradingSignatures, (ncCount s.1 s.2 = 8 ↔ s = (2, 1) ∨ s = (1, 2)) := by
  decide

/-- **The minimizers are one class up to the grading-sign flip** `Γ ↦ −Γ` (= `Prod.swap`).
The residual choice inside the minimum is exactly the sign relabel — a NAMED open
sub-question, not silently resolved here. -/
theorem minimizers_flip_pair : ((1, 2) : ℕ × ℕ) = Prod.swap (2, 1) := by decide

/-- **Saturation surplus of the in-class non-minimizers**: the maximal signatures sit at
`12 = 8 + 4` — four extra grading-even channels with no admissible datum demanding them.
(NOT the P-schema witness-just-past: these are IN-class; the outside-class witness slot is
held by the missing PRIM — see header.) -/
theorem saturation_surplus : ncCount 3 0 = 12 ∧ ncCount 0 3 = 12 ∧ 12 - 8 = 4 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **Grading-axis minimal-completion selection (bundle).** The E1 no-go's positive face:
the grading class is EXHAUSTED (`p+q=3` ⇔ membership), the neutral-current floor is `8`,
the minimizer set is exactly the flip pair `{(2,1),(1,2)}`, and the maximal signatures sit
just past at `12`. The E1 no-go itself (no admissible DATUM selects) is restated, unchanged:
`8 ≠ 12` stays divergent. -/
theorem grading_minimal_completion_selection :
    (∀ p q : ℕ, p + q = 3 ↔ (p, q) ∈ gradingSignatures) ∧
    (∀ s ∈ gradingSignatures, 8 ≤ ncCount s.1 s.2) ∧
    (∀ s ∈ gradingSignatures, (ncCount s.1 s.2 = 8 ↔ s = (2, 1) ∨ s = (1, 2))) ∧
    ncCount 2 1 ≠ ncCount 3 0 :=
  ⟨grading_axis_exhaustive, nc_floor, min_attained_iff, nc_divergent⟩

end D0.Extensions.GradingMinimalCompletion
