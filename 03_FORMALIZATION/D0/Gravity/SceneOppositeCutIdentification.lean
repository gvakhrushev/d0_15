import D0.Geometry.OppositeCutPairing
import D0.Gravity.A1RieszMismatch
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic

/-!
# Scene opposite-cut identification of the bare Riesz mismatch

`A9`, `A11`, and `A13` are the opposite-cut embeddings of the three zone
standard spaces.  Their coefficients are the complementary zone cardinalities.
The bare mismatch on each standard sector is therefore the block-weight
difference times that cut, and the numerical factors `143`, `117`, `99` are
the products `11*13`, `9*13`, and `9*11`.

The same cut on `K(2,6,6)`, `K(3,3,8)`, and `K(2,3,4)` produces the products
of those scenes' own complementary sizes.

The rank count below is the rank of the mismatch on the span of the three
standard sectors.  It is the sum of the active balanced dimensions
`8`, `10`, and `12`.  Pairwise weight differences are linearly dependent, so
the only values are `0`, `18`, `20`, `22`, and `30`.
-/

namespace D0.Gravity.SceneOppositeCutIdentification

open D0.Geometry.OppositeCutPairing
open D0.Geometry.SignlessSignedCommonCarrier
open D0.Gravity.A1RieszMismatch

abbrev Z9 := D0.Geometry.SignlessSignedCommonCarrier.V9
abbrev Z11 := D0.Geometry.SignlessSignedCommonCarrier.V11
abbrev Z13 := D0.Geometry.SignlessSignedCommonCarrier.V13

theorem A9_eq_oppositeCut (f : Balanced9) :
    A9 f = oppositeCutAlpha (α := Z9) (β := Z11) (γ := Z13) f.1 := by
  funext e
  rcases e with ⟨i, j⟩ | e
  · simp [A9, oppositeCutAlpha, Fintype.card_fin]
  · rcases e with ⟨i, k⟩ | ⟨j, k⟩
    · simp [A9, oppositeCutAlpha, Fintype.card_fin]
    · simp [A9, oppositeCutAlpha]

theorem A11_eq_oppositeCut (f : Balanced11) :
    A11 f = oppositeCutBeta (α := Z9) (β := Z11) (γ := Z13) f.1 := by
  funext e
  rcases e with ⟨i, j⟩ | e
  · simp [A11, oppositeCutBeta, Fintype.card_fin]
  · rcases e with ⟨i, k⟩ | ⟨j, k⟩
    · simp [A11, oppositeCutBeta]
    · simp [A11, oppositeCutBeta, Fintype.card_fin]

theorem A13_eq_oppositeCut (f : Balanced13) :
    A13 f = oppositeCutGamma (α := Z9) (β := Z11) (γ := Z13) f.1 := by
  funext e
  rcases e with ⟨i, j⟩ | e
  · simp [A13, oppositeCutGamma]
  · rcases e with ⟨i, k⟩ | ⟨j, k⟩
    · simp [A13, oppositeCutGamma, Fintype.card_fin]
    · simp [A13, oppositeCutGamma, Fintype.card_fin]

theorem BPlus_eq_unsignedIncidence (X : A1RieszMismatch.EdgeCochain) :
    BPlus X = unsignedIncidence (α := Z9) (β := Z11) (γ := Z13) X := by
  funext v
  rcases v with i | j | k <;> rfl

theorem R_eq_blockScale (a b c : ℚ) (X : A1RieszMismatch.EdgeCochain) :
    R a b c X = blockScale (α := Z9) (β := Z11) (γ := Z13) a b c X := by
  funext e
  rcases e with e | e | e <;> rfl

theorem lift9_eq_liftAlpha (f : Balanced9) :
    lift9 f = liftAlpha (β := Z11) (γ := Z13) f.1 := by
  funext v
  rcases v with i | j | k <;> simp [lift9, liftAlpha]

theorem lift11_eq_liftBeta (f : Balanced11) :
    lift11 f = liftBeta (α := Z9) (γ := Z13) f.1 := by
  funext v
  rcases v with i | j | k <;> simp [lift11, liftBeta]

theorem lift13_eq_liftGamma (f : Balanced13) :
    lift13 f = liftGamma (α := Z9) (β := Z11) f.1 := by
  funext v
  rcases v with i | j | k <;> simp [lift13, liftGamma]

theorem scene_cut_coefficients :
    (Fintype.card Z11 : ℚ) * Fintype.card Z13 = 143 ∧
    (Fintype.card Z9 : ℚ) * Fintype.card Z13 = 117 ∧
    (Fintype.card Z9 : ℚ) * Fintype.card Z11 = 99 := by
  simp [Z9, Z11, Z13, Fintype.card_fin]
  norm_num

theorem mismatch_A9_oppositeCut (a b c : ℚ) (f : Balanced9) :
    mismatch a b c (A9 f) =
      ((Fintype.card Z11 : ℚ) * Fintype.card Z13 * (a - b)) • lift9 f := by
  have hgen := unsignedIncidence_block_oppositeCutAlpha (α := Z9) (β := Z11)
    (γ := Z13) a b c f.1 (balanced_sum f)
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply, A9_eq_oppositeCut,
    R_eq_blockScale, BPlus_eq_unsignedIncidence, hgen, lift9_eq_liftAlpha]

theorem mismatch_A11_oppositeCut (a b c : ℚ) (f : Balanced11) :
    mismatch a b c (A11 f) =
      ((Fintype.card Z9 : ℚ) * Fintype.card Z13 * (a - c)) • lift11 f := by
  have hgen := unsignedIncidence_block_oppositeCutBeta (α := Z9) (β := Z11)
    (γ := Z13) a b c f.1 (balanced_sum f)
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply, A11_eq_oppositeCut,
    R_eq_blockScale, BPlus_eq_unsignedIncidence, hgen, lift11_eq_liftBeta]

theorem mismatch_A13_oppositeCut (a b c : ℚ) (f : Balanced13) :
    mismatch a b c (A13 f) =
      ((Fintype.card Z9 : ℚ) * Fintype.card Z11 * (b - c)) • lift13 f := by
  have hgen := unsignedIncidence_block_oppositeCutGamma (α := Z9) (β := Z11)
    (γ := Z13) a b c f.1 (balanced_sum f)
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply, A13_eq_oppositeCut,
    R_eq_blockScale, BPlus_eq_unsignedIncidence, hgen, lift13_eq_liftGamma]

theorem mismatch_standard_sectors_are_opposite_cuts (a b c : ℚ)
    (f9 : Balanced9) (f11 : Balanced11) (f13 : Balanced13) :
    mismatch a b c (A9 f9) =
        ((Fintype.card Z11 : ℚ) * Fintype.card Z13 * (a - b)) • lift9 f9 ∧
    mismatch a b c (A11 f11) =
        ((Fintype.card Z9 : ℚ) * Fintype.card Z13 * (a - c)) • lift11 f11 ∧
    mismatch a b c (A13 f13) =
        ((Fintype.card Z9 : ℚ) * Fintype.card Z11 * (b - c)) • lift13 f13 :=
  ⟨mismatch_A9_oppositeCut a b c f9,
   mismatch_A11_oppositeCut a b c f11,
   mismatch_A13_oppositeCut a b c f13⟩

theorem owned_numeric_factors_are_cut_products (a b c : ℚ) (f9 : Balanced9)
    (f11 : Balanced11) (f13 : Balanced13) :
    mismatch a b c (A9 f9) = (143 * (a - b)) • lift9 f9 ∧
    mismatch a b c (A11 f11) = (117 * (a - c)) • lift11 f11 ∧
    mismatch a b c (A13 f13) = (99 * (b - c)) • lift13 f13 := by
  rcases scene_cut_coefficients with ⟨h143, h117, h99⟩
  refine ⟨?_, ?_, ?_⟩
  · rw [mismatch_A9_oppositeCut, h143]
  · rw [mismatch_A11_oppositeCut, h117]
  · rw [mismatch_A13_oppositeCut, h99]

/-- Rank contribution of the three standard sectors.  A summand is present
exactly when the corresponding block weights differ. -/
def standardSectorRank (a b c : ℚ) : ℕ :=
  (if a = b then 0 else 8) + (if a = c then 0 else 10) + (if b = c then 0 else 12)

theorem weight_difference_telescopes (a b c : ℚ) :
    (a - b) + (b - c) = a - c := by ring

theorem standardSectorRank_strata (a b c : ℚ) :
    standardSectorRank a b c = 0 ∨ standardSectorRank a b c = 18 ∨
    standardSectorRank a b c = 20 ∨ standardSectorRank a b c = 22 ∨
    standardSectorRank a b c = 30 := by
  by_cases hab : a = b <;> by_cases hac : a = c <;> by_cases hbc : b = c
  · simp [standardSectorRank, hab, hac, hbc]
  · exact False.elim (hbc (hab.symm.trans hac))
  · exact False.elim (hac (hab.trans hbc))
  · simp [standardSectorRank, if_pos hab, if_neg hac, if_neg hbc]
  · exact False.elim (hab (hac.trans hbc.symm))
  · simp [standardSectorRank, if_neg hab, if_pos hac, if_neg hbc]
  · simp [standardSectorRank, if_neg hab, if_neg hac, if_pos hbc]
  · simp [standardSectorRank, if_neg hab, if_neg hac, if_neg hbc]

def standardSectorMap (a b c : ℚ) :
    Balanced9 × Balanced11 × Balanced13 →ₗ[ℚ] A1RieszMismatch.VertexCochain where
  toFun p :=
    mismatch a b c (A9 p.1) + mismatch a b c (A11 p.2.1) +
      mismatch a b c (A13 p.2.2)
  map_add' p q := by
    simp only [Prod.fst_add, Prod.snd_add, map_add]
    abel
  map_smul' r p := by
    simp only [Prod.smul_fst, Prod.smul_snd, map_smul, RingHom.id_apply, smul_add]

theorem standardSectorMap_zoneA (a b c : ℚ)
    (p : Balanced9 × Balanced11 × Balanced13) (i : Z9) :
    standardSectorMap a b c p (Sum.inl i) =
      (Fintype.card Z11 : ℚ) * Fintype.card Z13 * (a - b) * p.1.1 i := by
  have h9 := congrFun (mismatch_A9_oppositeCut a b c p.1) (Sum.inl i)
  have h11 := congrFun (mismatch_A11_oppositeCut a b c p.2.1) (Sum.inl i)
  have h13 := congrFun (mismatch_A13_oppositeCut a b c p.2.2) (Sum.inl i)
  change (mismatch a b c (A9 p.1) + mismatch a b c (A11 p.2.1) +
      mismatch a b c (A13 p.2.2)) (Sum.inl i) = _
  rw [Pi.add_apply, Pi.add_apply, h9, h11, h13]
  simp only [lift9, lift11, lift13, Pi.smul_apply, smul_eq_mul]
  ring

theorem standardSectorMap_zoneB (a b c : ℚ)
    (p : Balanced9 × Balanced11 × Balanced13) (j : Z11) :
    standardSectorMap a b c p (Sum.inr (Sum.inl j)) =
      (Fintype.card Z9 : ℚ) * Fintype.card Z13 * (a - c) * p.2.1.1 j := by
  have h9 := congrFun (mismatch_A9_oppositeCut a b c p.1) (Sum.inr (Sum.inl j))
  have h11 := congrFun (mismatch_A11_oppositeCut a b c p.2.1) (Sum.inr (Sum.inl j))
  have h13 := congrFun (mismatch_A13_oppositeCut a b c p.2.2) (Sum.inr (Sum.inl j))
  change (mismatch a b c (A9 p.1) + mismatch a b c (A11 p.2.1) +
      mismatch a b c (A13 p.2.2)) (Sum.inr (Sum.inl j)) = _
  rw [Pi.add_apply, Pi.add_apply, h9, h11, h13]
  simp only [lift9, lift11, lift13, Pi.smul_apply, smul_eq_mul]
  ring

theorem standardSectorMap_zoneC (a b c : ℚ)
    (p : Balanced9 × Balanced11 × Balanced13) (k : Z13) :
    standardSectorMap a b c p (Sum.inr (Sum.inr k)) =
      (Fintype.card Z9 : ℚ) * Fintype.card Z11 * (b - c) * p.2.2.1 k := by
  have h9 := congrFun (mismatch_A9_oppositeCut a b c p.1) (Sum.inr (Sum.inr k))
  have h11 := congrFun (mismatch_A11_oppositeCut a b c p.2.1) (Sum.inr (Sum.inr k))
  have h13 := congrFun (mismatch_A13_oppositeCut a b c p.2.2) (Sum.inr (Sum.inr k))
  change (mismatch a b c (A9 p.1) + mismatch a b c (A11 p.2.1) +
      mismatch a b c (A13 p.2.2)) (Sum.inr (Sum.inr k)) = _
  rw [Pi.add_apply, Pi.add_apply, h9, h11, h13]
  simp only [lift9, lift11, lift13, Pi.smul_apply, smul_eq_mul]
  ring

theorem standard_sector_domain_finrank :
    Module.finrank ℚ (Balanced9 × Balanced11 × Balanced13) = 30 := by
  simp [Module.finrank_prod, balanced9_finrank, balanced11_finrank, balanced13_finrank]

theorem standardSectorMap_eq_zero_iff (a b c : ℚ)
    (p : Balanced9 × Balanced11 × Balanced13) :
    standardSectorMap a b c p = 0 ↔
      (a ≠ b → p.1 = 0) ∧ (a ≠ c → p.2.1 = 0) ∧ (b ≠ c → p.2.2 = 0) := by
  constructor
  · intro hp
    refine ⟨?_, ?_, ?_⟩
    · intro hab
      apply Subtype.ext
      funext i
      have hi := congrFun hp (Sum.inl i)
      rw [standardSectorMap_zoneA] at hi
      have hcoeff : (Fintype.card Z11 : ℚ) * Fintype.card Z13 * (a - b) ≠ 0 := by
        simp [Z11, Z13, Fintype.card_fin, sub_ne_zero.mpr hab]
      exact (mul_eq_zero.mp hi).resolve_left hcoeff
    · intro hac
      apply Subtype.ext
      funext j
      have hj := congrFun hp (Sum.inr (Sum.inl j))
      rw [standardSectorMap_zoneB] at hj
      have hcoeff : (Fintype.card Z9 : ℚ) * Fintype.card Z13 * (a - c) ≠ 0 := by
        simp [Z9, Z13, Fintype.card_fin, sub_ne_zero.mpr hac]
      exact (mul_eq_zero.mp hj).resolve_left hcoeff
    · intro hbc
      apply Subtype.ext
      funext k
      have hk := congrFun hp (Sum.inr (Sum.inr k))
      rw [standardSectorMap_zoneC] at hk
      have hcoeff : (Fintype.card Z9 : ℚ) * Fintype.card Z11 * (b - c) ≠ 0 := by
        simp [Z9, Z11, Fintype.card_fin, sub_ne_zero.mpr hbc]
      exact (mul_eq_zero.mp hk).resolve_left hcoeff
  · intro ⟨h9, h11, h13⟩
    ext v
    rcases v with i | j | k
    · by_cases hab : a = b
      · simpa [hab] using standardSectorMap_zoneA a b c p i
      · rw [standardSectorMap_zoneA, h9 hab]
        simp
    · by_cases hac : a = c
      · simpa [hac] using standardSectorMap_zoneB a b c p j
      · rw [standardSectorMap_zoneB, h11 hac]
        simp
    · by_cases hbc : b = c
      · simpa [hbc] using standardSectorMap_zoneC a b c p k
      · rw [standardSectorMap_zoneC, h13 hbc]
        simp

theorem standardSectorMap_injective_of_distinct {a b c : ℚ}
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    Function.Injective (standardSectorMap a b c) := by
  intro p q hpq
  have hker : standardSectorMap a b c (p - q) = 0 := by
    rw [map_sub, hpq, sub_self]
  have hk := (standardSectorMap_eq_zero_iff a b c (p - q)).mp hker
  have hf : p.1 = q.1 := by
    have hsub : (p - q).1 = 0 := hk.1 hab
    exact sub_eq_zero.mp (by simpa using hsub)
  have hg : p.2.1 = q.2.1 := by
    have hsub : (p - q).2.1 = 0 := hk.2.1 hac
    exact sub_eq_zero.mp (by simpa using hsub)
  have hh : p.2.2 = q.2.2 := by
    have hsub : (p - q).2.2 = 0 := hk.2.2 hbc
    exact sub_eq_zero.mp (by simpa using hsub)
  exact Prod.ext hf (Prod.ext hg hh)

theorem distinct_weights_standard_sector_finrank {a b c : ℚ}
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    Module.finrank ℚ (LinearMap.range (standardSectorMap a b c)) = 30 := by
  rw [LinearMap.finrank_range_of_inj
    (standardSectorMap_injective_of_distinct hab hac hbc)]
  exact standard_sector_domain_finrank

theorem uniform_weights_standard_sector_finrank {a b c : ℚ}
    (hab : a = b) (hbc : b = c) :
    Module.finrank ℚ (LinearMap.range (standardSectorMap a b c)) = 0 := by
  have hzero : standardSectorMap a b c = 0 := by
    apply LinearMap.ext
    intro p
    exact (standardSectorMap_eq_zero_iff a b c p).mpr
      ⟨fun h => (h hab).elim, fun h => (h (hab.trans hbc)).elim,
        fun h => (h hbc).elim⟩
  rw [hzero, LinearMap.range_zero, finrank_bot]

theorem standard_sector_rank_matches_active_dimensions {a b c : ℚ}
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) :
    Module.finrank ℚ (LinearMap.range (standardSectorMap a b c)) =
      standardSectorRank a b c := by
  rw [distinct_weights_standard_sector_finrank hab hac hbc]
  simp [standardSectorRank, hab, hac, hbc]

end D0.Gravity.SceneOppositeCutIdentification
