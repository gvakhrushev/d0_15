import D0.Algebra.OriginalBookLocalBoost
import D0.Geometry.OriginalBookEffectWords
import Mathlib.Tactic

/-!
# Transport of chronological effects through source-local specializations

Candidate reusable adapter: any local family of matrices is transported as an
actual chronological Heisenberg effect to complex numbers, and to each of the
conjugate finite-field evaluations. Both modular images are needed: conjugation
occurs in the local coefficient ring before the scalar evaluation.

No specific family of source reduced Kraus matrices, source word, determinant,
rank, physical realization or source-to-Python equality is asserted here.
-/
open Matrix
open D0.Algebra.OriginalBookRadicalLocal
open D0.Algebra.OriginalBookRadicalMod1009
open D0.Algebra.OriginalBookLocalCreators
open D0.Algebra.OriginalBookLocalBoost

namespace D0.Algebra.OriginalBookLocalEffectTransport

variable {ι : Type*}

/-- Chronological Heisenberg effect over the actual local source ring. -/
noncomputable def localEffect (K : ι → LocalOperator) : List ι → LocalOperator
  | [] => 1
  | slot :: rest => (K slot)ᴴ * localEffect K rest * K slot

/-- Finite-field effect using the opposite specialization for the adjoint. -/
noncomputable def crossEffect (Kplus Kminus : ι → Matrix (Fin 16) (Fin 16) (ZMod 1009)) :
    List ι → Matrix (Fin 16) (Fin 16) (ZMod 1009)
  | [] => 1
  | slot :: rest => (Kminus slot).transpose * crossEffect Kplus Kminus rest * Kplus slot

/-- The local Heisenberg effect maps to the existing complex effect. -/
theorem localEffect_complex (K : ι → LocalOperator) (path : List ι) :
    (localEffect K path).map localSourceToComplex =
      D0.Geometry.ChronologicalEffect.effect (fun slot => (K slot).map localSourceToComplex) path := by
  induction path with
  | nil => simp [localEffect, D0.Geometry.ChronologicalEffect.effect]
  | cons slot rest ih =>
    simp [localEffect, D0.Geometry.ChronologicalEffect.effect,
      D0.Geometry.ChronologicalEffect.update, localDagger_complex, ih]

/-- The plus residue uses the minus residue for every adjoint. -/
theorem localEffect_mod_plus (K : ι → LocalOperator) (path : List ι) :
    (localEffect K path).map redPlus =
      crossEffect (fun slot => (K slot).map redPlus) (fun slot => (K slot).map redMinus) path := by
  induction path with
  | nil => simp [localEffect, crossEffect]
  | cons slot rest ih => simp [localEffect, crossEffect, localDagger_mod, ih]

/-- The minus residue uses the plus residue for every adjoint. -/
theorem localEffect_mod_minus (K : ι → LocalOperator) (path : List ι) :
    (localEffect K path).map redMinus =
      crossEffect (fun slot => (K slot).map redMinus) (fun slot => (K slot).map redPlus) path := by
  induction path with
  | nil => simp [localEffect, crossEffect]
  | cons slot rest ih => simp [localEffect, crossEffect, localDagger_mod_minus, ih]

end D0.Algebra.OriginalBookLocalEffectTransport
