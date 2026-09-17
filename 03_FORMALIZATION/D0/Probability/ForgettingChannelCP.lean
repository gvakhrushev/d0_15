import Mathlib.Analysis.CStarAlgebra.CompletelyPositiveMap
import Mathlib.Analysis.CStarAlgebra.CStarMatrix
import Mathlib.Analysis.CStarAlgebra.Classes
import Mathlib.Analysis.RCLike.Basic
import Mathlib.Analysis.Complex.Order

/-!
# D0-FORGETTING-CHANNEL-CP-001 — a genuine `CompletelyPositiveMap` for the *-hom forgetting model

Companion to D0-FORGETTING-CHANNEL-PTP-001. That module proved the *depolarizing* forgetting channel
`M ↦ (tr M/n)·I` is positive + trace-preserving, but noted that full complete positivity (a Mathlib
`CompletelyPositiveMap` over `CStarMatrix`) is NOT bounded for it — the depolarizing map is not a
`*`-homomorphism, so the only CP constructor in the pin (`NonUnitalStarAlgHomClass.instCompletelyPositiveMapClass`)
does not apply.

This module supplies the CP side for the `*`-homomorphism forgetting model: any `*`-homomorphism between
the matrix C*-algebras `CStarMatrix (Fin n) (Fin n) ℂ` is a GENUINE `CompletelyPositiveMap` (the
`map_cstarMatrix_nonneg'` obligation over every `k×k` amplification is discharged by Mathlib, no `sorry`).
The identity (forget-nothing) channel is the limiting instance; a `*`-hom block-embedding /
Heisenberg-dual compression is the faithful forgetting-onto-a-subalgebra model. The depolarizing channel's
complete positivity remains the named THEOREM-TARGET.
-/

open scoped CStarAlgebra ComplexOrder

namespace D0.Probability

/-- The C*-algebra of `n×n` complex matrices: a genuine non-unital C*-algebra + star-ordered ring. -/
abbrev MatAlg (n : ℕ) := CStarMatrix (Fin n) (Fin n) ℂ

/-- **Any `*`-homomorphism between matrix C*-algebras is a genuine `CompletelyPositiveMap`** — the
reusable CP forgetting model (block-embedding / compression-as-`*`-hom), via Mathlib's
`NonUnitalStarAlgHomClass.instCompletelyPositiveMapClass`. -/
noncomputable def d0HomCP {m n : ℕ} (φ : MatAlg m →⋆ₙₐ[ℂ] MatAlg n) : MatAlg m →CP MatAlg n :=
  (φ : CompletelyPositiveMap (MatAlg m) (MatAlg n))

/-- D0 forgetting in the trivial (forget-nothing) limit: the identity channel as a genuine
`CompletelyPositiveMap`. -/
noncomputable def d0ForgetIdCP (n : ℕ) : MatAlg n →CP MatAlg n :=
  d0HomCP (NonUnitalStarAlgHom.id ℂ (MatAlg n))

/-- The complete-positivity obligation is genuinely discharged (real, over every amplification `k`). -/
theorem d0ForgetIdCP_completelyPositive (n : ℕ) :
    ∀ (k : ℕ) (M : CStarMatrix (Fin k) (Fin k) (MatAlg n)), 0 ≤ M → 0 ≤ M.map (d0ForgetIdCP n) :=
  fun k M hM => (d0ForgetIdCP n).map_cstarMatrix_nonneg' k M hM

/-- The identity CP channel acts as the identity on elements. -/
theorem d0ForgetIdCP_apply (n : ℕ) (M : MatAlg n) : d0ForgetIdCP n M = M := rfl

end D0.Probability
