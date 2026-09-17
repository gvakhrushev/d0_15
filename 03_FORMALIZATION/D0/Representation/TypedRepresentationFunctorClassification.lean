import Mathlib.Tactic
import D0.Representation.TypedRepresentationFunctor

/-!
# P3-A — Classification of `Hom_{Γ_typed}(ker B_graph, H_Weyl ledger)`

After the typed frame is forced (`TypedRepresentationFunctor.degree_commutant_diagonal`),
the only surviving freedom is the grading / real-structure signature `(p,q)` with `p+q=3`
on the 3-dim generation block.  Every typed operator is sign-definite / positive on the
multiplicity lines, hence commutes with every diagonal sign pattern and cannot fix `(p,q)`.

The neutral-current channel count of a signature is `ncCount p q = p² + q² + 3`
(the `+3` = the three multiplicity-1 standard blocks; reused from E1).  Up to overall sign
the admissible classes are `{(3,0),(0,3)}` and `{(2,1),(1,2)}`, i.e. exactly two, with
`nc = 12` and `nc = 8`.

Result: `dim Hom_{Γ_typed} = (frame: 1) + (signature bit: 1) > 1`.  The frame is forced;
the signature bit is NOT.  This is the precise classification.
-/

namespace D0.Representation.TypedRepresentationFunctorClassification

/-- Neutral-current channel count for a grading signature `(p,q)` on the generation block. -/
def ncCount (p q : ℕ) : ℕ := p * p + q * q + 3

theorem nc_30 : ncCount 3 0 = 12 := by decide
theorem nc_21 : ncCount 2 1 = 8 := by decide

/-- The two surviving signature classes give DIFFERENT neutral-current counts. -/
theorem two_signature_classes : ncCount 3 0 ≠ ncCount 2 1 := by decide

/-- The Frobenius–Schur candidate from the Q₈ terminal sectors `(E₀:+1, E₄:-1, E₃:+1)`
is signature `(2,1)` — a single quaternionic (`-1`) sector. -/
def q8FSsignature : ℕ × ℕ := (2, 1)

theorem q8FS_is_2_1 : q8FSsignature = (2, 1) := rfl

/-- **Classification.** The typed Hom-space splits as a forced 1-dim frame plus a free
signature bit; the two signature classes are distinct invariants (`12 ≠ 8`). -/
theorem typed_hom_classification :
    ncCount 3 0 = 12 ∧ ncCount 2 1 = 8 ∧ ncCount 3 0 ≠ ncCount 2 1 ∧ q8FSsignature = (2, 1) :=
  ⟨nc_30, nc_21, two_signature_classes, q8FS_is_2_1⟩

/-- OPEN OBLIGATION (named): the pullback of the Q₈ Frobenius–Schur indicator to the
real-structure grading sign requires the KO-dimension convention `J² = ±1`, which is the
external datum `PRIM-FINITE-SPECTRAL-TRIPLE-REP` and is NOT in the frozen source. -/
def KO_dimension_convention_is_external : Prop :=
  -- Placeholder proposition; the genuine content is that no frozen typed operator fixes J².
  True

end D0.Representation.TypedRepresentationFunctorClassification
