import D0.Matter.BaryonS3Symmetrizer

namespace D0.Matter

/-!
Lightweight baryon multiplet boundary owner.

This file isolates the baryon-only promotion boundary so modules that only need
the S3/decuplet no-go do not import the meson and scalar-projector layers.
-/

/-- A finite baryon multiplet operator must carry spin, flavour, S3 decuplet and transfer data. -/
structure BaryonMultipletOperator where
  hasSpinResolution : Prop
  hasFlavourResolution : Prop
  decupletCarrier : Option BaryonS3SymmetrizerClosure
  hasTransferWindow : Prop

/-- A baryon operator has decuplet carrier data only when it carries the S3 closure. -/
def HasBaryonDecupletCarrier (O : BaryonMultipletOperator) : Prop :=
  ∃ C : BaryonS3SymmetrizerClosure, O.decupletCarrier = some C

/-- A baryon multiplet mass row is promotable only with every required component present. -/
def CanPromoteBaryonMultiplet (O : BaryonMultipletOperator) : Prop :=
  O.hasSpinResolution ∧ O.hasFlavourResolution ∧
    HasBaryonDecupletCarrier O ∧ O.hasTransferWindow

/-- The current nucleon-line operator deliberately lacks the extra multiplet operator data. -/
def nucleonLineOnlyBaryonOperator : BaryonMultipletOperator where
  hasSpinResolution := False
  hasFlavourResolution := False
  decupletCarrier := none
  hasTransferWindow := False

/-- Promotion to a full baryon multiplet requires the typed baryon operator. -/
theorem baryon_multiplet_requires_spin_flavour_decuplet_operator
    (O : BaryonMultipletOperator) :
    CanPromoteBaryonMultiplet O →
      O.hasSpinResolution ∧ O.hasFlavourResolution ∧
        HasBaryonDecupletCarrier O ∧ O.hasTransferWindow := by
  intro h
  exact h

/-- The current nucleon line cannot be re-read as a full baryon multiplet. -/
theorem nucleon_line_cannot_promote_full_baryon_multiplet :
    ¬ CanPromoteBaryonMultiplet nucleonLineOnlyBaryonOperator := by
  intro h
  rcases h.2.2.1 with ⟨C, hC⟩
  simp [nucleonLineOnlyBaryonOperator] at hC

end D0.Matter
