import D0.Algebra.OriginalBookLocalJuliaPairs
import D0.Algebra.OriginalBookLocalEffectTransport
import D0.Geometry.OriginalBookEffectRadicalReduction
import D0.Geometry.OriginalBookEffectSpanUpper
import D0.Algebra.FiniteSpecialization

/-!
# The local coefficients of the original 128 reduced slots and their effects

The Julia pairs, Walsh characters, row and port indexing below are those of the
original source. The odd-port square roots are restored at the effect level by
the existing positive path weight. The two residue maps act on one local word.
-/

open Matrix
open D0.Geometry.OriginalBookJuliaWords D0.Geometry.OriginalBookWalsh
open D0.Geometry.OriginalBookGoldenKraus D0.Geometry.OriginalBookEffectWords
open D0.Geometry.OriginalBookEffectRadicalReduction
open D0.Algebra.OriginalBookRadicalLocal D0.Algebra.OriginalBookRadicalSourceConstants
open D0.Algebra.OriginalBookLocalCreators D0.Algebra.OriginalBookLocalBoost
open D0.Algebra.OriginalBookLocalJuliaPairs D0.Algebra.OriginalBookLocalEffectTransport

namespace D0.Algebra.OriginalBookLocalEffectWords

noncomputable def localEndpoint (word : Fin 32) (port : Fin 2) : LocalOperator :=
  let pair := localRowPair (wordMode word) (wordRow word)
  if port = 0 then pair.1 else pair.2

theorem localEndpoint_complex (word : Fin 32) (port : Fin 2) :
    (localEndpoint word port).map localSourceToComplex = wordEndpoint word port := by
  have hp := localRowPair_complex (wordMode word) (wordRow word)
  by_cases h : port = 0
  · simpa [localEndpoint, wordEndpoint, sourceWord, h] using congrArg Prod.fst hp
  · simpa [localEndpoint, wordEndpoint, sourceWord, h] using congrArg Prod.snd hp

/-- Flatten the two endpoints of every normalized Walsh row in source order. -/
noncomputable def localWalshRow (row : Fin 64) : LocalOperator :=
  (4405 * localInvD)^5 • ∑ word : Fin 32,
    (walshSign (rowLabel row) word) • localEndpoint word (rowEndpoint row)

theorem localWalshRow_complex (row : Fin 64) :
    (localWalshRow row).map localSourceToComplex = sourceWalshRow row := by
  ext i j
  have he (word : Fin 32) := congrArg (fun M : Operator => M i j)
    (localEndpoint_complex word (rowEndpoint row))
  simp only [Matrix.map_apply] at he
  simp only [localWalshRow, sourceWalshRow, walshPairRow, Matrix.map_apply,
    Matrix.smul_apply, Matrix.sum_apply]
  simp only [smul_eq_mul, zsmul_eq_mul, map_mul,
    map_pow, map_sum, map_intCast, map_ofNat, complexInvD, he, Complex.real_smul]
  push_cast
  ring

/-- The slot matrix over the localized source ring, after the positive odd
port scalar has been separated by sourceEffect_eq_weighted_reduced. -/
noncomputable def localReducedKraus (slot : Fin 128) : LocalOperator :=
  let row := krausRow slot
  let v := (localWalshRow row)ᴴ * localWalshRow 0
  if krausPort slot = 0 then
    (if row = 0 then 1 else 0) - (2 * localP^2) • v
  else (- (2 * localP)) • v

theorem localReducedKraus_complex (slot : Fin 128) :
    (localReducedKraus slot).map localSourceToComplex = reducedKraus slot := by
  have hv (r : Fin 64) :
      ((localWalshRow r)ᴴ * localWalshRow 0).map localSourceToComplex = sourceV r := by
    simp [sourceV, sourceAnchor, localDagger_complex, localWalshRow_complex]
  have hp := localSourceConstants_complex.1
  have he (r : Fin 64) (i j : Fin 16) := congrArg (fun M : Operator => M i j) (hv r)
  simp only [Matrix.map_apply] at he
  by_cases hport : krausPort slot = 0 <;> by_cases hrow : krausRow slot = 0 <;>
    simp only [localReducedKraus, reducedKraus, hport, hrow, if_false, if_true] <;>
    ext i j <;>
    simp only [Matrix.map_apply, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul,
      map_sub, map_mul, map_neg, map_ofNat, map_pow, hp, he, Complex.real_smul,
      Complex.ofReal_mul, Complex.ofReal_pow, Complex.ofReal_neg, Complex.ofReal_ofNat,
      Matrix.one_apply, Matrix.zero_apply, apply_ite, map_one, map_zero]

/-- For every chronological path, including repeated and zero slots, restore
the exact source effect from the same local coefficient matrices. -/
theorem sourceEffect_eq_local (path : List (Fin 128)) :
    sourceEffect path =
      pathWeight path • (localEffect localReducedKraus path).map localSourceToComplex := by
  rw [localEffect_complex, sourceEffect_eq_weighted_reduced]
  simp only [localReducedKraus_complex]

open D0.Algebra.OriginalBookRadicalMod1009
open D0.Geometry.OriginalBookEffectSpanUpper

/-- Entries of the reduced chronological effects, evaluated in the finite
field. The adjoint uses the *opposite* specialization before transpose. -/
noncomputable def residueRows {n : ℕ} (paths : Fin n → List (Fin 128))
    (coord : Fin n → Fin 16 × Fin 16) : Matrix (Fin n) (Fin n) (ZMod 1009) :=
  fun i j => crossEffect (fun k => (localReducedKraus k).map redPlus)
    (fun k => (localReducedKraus k).map redMinus) (paths i) (coord j).1 (coord j).2

private def readCoordinates {n : ℕ} (coord : Fin n → Fin 16 × Fin 16) :
    Operator →ₗ[ℂ] (Fin n → ℂ) where
  toFun X j := X (coord j).1 (coord j).2
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- A nonzero residue minor for the actual local words suffices for
independence of the *original*, positively weighted complex effects. -/
theorem sourceEffects_independent_of_residue_det {n : ℕ}
    (paths : Fin n → List (Fin 128)) (coord : Fin n → Fin 16 × Fin 16)
    (hw : (residueRows paths coord).det ≠ 0) :
    LinearIndependent ℂ (fun i => sourceEffect (paths i)) := by
  let M : Matrix (Fin n) (Fin n) LocalSource := fun i j =>
    localEffect localReducedKraus (paths i) (coord j).1 (coord j).2
  have hmod : redPlus.mapMatrix M = residueRows paths coord := by
    ext i j
    exact congrArg (fun X : Matrix (Fin 16) (Fin 16) (ZMod 1009) =>
      X (coord j).1 (coord j).2) (localEffect_mod_plus localReducedKraus (paths i))
  have hli := D0.Algebra.FiniteSpecialization.mapped_rows_independent redPlus
    localSourceToComplex localSourceToComplex_injective M (by rwa [hmod])
  apply (sourceEffects_linearIndependent_iff paths).2
  apply LinearIndependent.of_comp (readCoordinates coord)
  have hrows : (readCoordinates coord) ∘ (fun i =>
      D0.Geometry.ChronologicalEffect.effect reducedKraus (paths i)) =
      fun i => (localSourceToComplex.mapMatrix M) i := by
    funext i j
    have he := localEffect_complex localReducedKraus (paths i)
    simp only [localReducedKraus_complex] at he
    exact congrArg (fun X : Operator => X (coord j).1 (coord j).2) he.symm
  rwa [hrows]

/-- Combined with the owned parity upper bound, a full minor on 128 words
would determine the entire complex span dimension. -/
theorem sourceEffectSpan_finrank_of_residue_det
    (paths : Fin 128 → List (Fin 128)) (coord : Fin 128 → Fin 16 × Fin 16)
    (hw : (residueRows paths coord).det ≠ 0) : Module.finrank ℂ sourceEffectSpan = 128 := by
  have hle : Submodule.span ℂ (Set.range (fun i => sourceEffect (paths i))) ≤ sourceEffectSpan :=
    Submodule.span_mono (by rintro _ ⟨i, rfl⟩; exact ⟨paths i, rfl⟩)
  have hdim := finrank_span_eq_card (sourceEffects_independent_of_residue_det paths coord hw)
  exact le_antisymm sourceEffectSpan_finrank_le (by
    simpa only [hdim, Fintype.card_fin] using Submodule.finrank_mono hle)

end D0.Algebra.OriginalBookLocalEffectWords
