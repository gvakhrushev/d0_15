import D0.Geometry.OriginalBookJuliaParity
import D0.Geometry.OriginalBookEffectWords
import Mathlib.Tactic

/-!
# Parity of actual source Kraus matrices and chronological effects

All operands, roots, Walsh signs, Golden combinations and words are the
previously defined actual source objects: uniform blob ee8de4635d24c668949ac9a0186616ab7d59f2ed
lines 75–99, modular blob d111c5bfeae3c384a4fe725f4a6d19277ea0005a
lines 125–182 and 217–222 at commit eebcb5e467742df3e9cf7fa9702042d7294aa742.
This proves parity containment; no span lower bound or physical admission is
assumed or asserted.
-/
open D0
open Matrix
open scoped BigOperators
open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.OriginalBookJuliaParity
open D0.Geometry.OriginalBookWalsh
open D0.Geometry.OriginalBookGoldenKraus
open D0.Geometry.OriginalBookEffectWords
open D0.Geometry.ChronologicalEffect

namespace D0.Geometry.OriginalBookEffectParity

lemma odd_sum {ι : Type*} (s : Finset ι) (f : ι → Operator)
    (hf : ∀ i ∈ s, IsOdd (f i)) : IsOdd (∑ i ∈ s, f i) := by
  unfold IsOdd at *
  simp only [Finset.mul_sum, Finset.sum_mul, ← Finset.sum_neg_distrib]
  exact Finset.sum_congr rfl hf

/-- Every original Julia pair has an odd first endpoint. -/
theorem rowPair_fst_odd (mode row : Fin 4) : IsOdd (rowPair mode row).1 := by
  fin_cases row
  · simpa [rowPair] using sourceAnalyticOperand_odd (modeRole mode)
  · simpa [rowPair] using odd_star (sourceAnalyticOperand_odd (modeRole mode))
  · simpa [rowPair] using odd_neg (sourceBase_odd (modeRole mode))
  · simpa [rowPair] using odd_neg (odd_star (sourceBase_odd (modeRole mode)))

/-- Every original Julia pair has an even second endpoint. -/
theorem rowPair_snd_even (mode row : Fin 4) : IsEven (rowPair mode row).2 := by
  fin_cases row
  · simpa [rowPair] using liveLeft_even (modeRole mode)
  · simpa [rowPair] using liveRight_even (modeRole mode)
  · simpa [rowPair, IsEven] using (baseLeft_even (modeRole mode)).neg_right
  · simpa [rowPair, IsEven] using (baseRight_even (modeRole mode)).neg_right

lemma wordEndpoint_odd (word : Fin 32) : IsOdd (wordEndpoint word 0) := by
  simpa [wordEndpoint, sourceWord] using rowPair_fst_odd (wordMode word) (wordRow word)

lemma wordEndpoint_even (word : Fin 32) : IsEven (wordEndpoint word 1) := by
  simpa [wordEndpoint, sourceWord] using rowPair_snd_even (wordMode word) (wordRow word)

/-- Walsh transformations preserve the endpoint parity. -/
theorem walshPairRow_odd (label : Fin 32) : IsOdd (walshPairRow label 0) := by
  unfold walshPairRow
  apply odd_smul_real
  apply odd_sum
  intro word _
  rw [← Int.cast_smul_eq_zsmul ℂ]
  exact odd_smul_complex _ (wordEndpoint_odd word)

theorem walshPairRow_even (label : Fin 32) : IsEven (walshPairRow label 1) := by
  unfold walshPairRow
  apply Commute.smul_right
  apply Commute.sum_right
  intro word _
  rw [← Int.cast_smul_eq_zsmul ℂ]
  exact (wordEndpoint_even word).smul_right _

lemma sourceWalshRow_odd (row : Fin 64) (h : rowEndpoint row = 0) : IsOdd (sourceWalshRow row) := by
  simpa [sourceWalshRow, h] using walshPairRow_odd (rowLabel row)

lemma sourceWalshRow_even (row : Fin 64) (h : rowEndpoint row = 1) : IsEven (sourceWalshRow row) := by
  simpa [sourceWalshRow, h] using walshPairRow_even (rowLabel row)

lemma anchor_odd : IsOdd sourceAnchor := by
  simpa [sourceAnchor, sourceWalshRow, rowLabel, rowEndpoint] using walshPairRow_odd 0

lemma sourceV_even (row : Fin 64) (h : rowEndpoint row = 0) : IsEven (sourceV row) := by
  exact odd_mul_odd (odd_star (sourceWalshRow_odd row h)) anchor_odd

lemma sourceV_odd (row : Fin 64) (h : rowEndpoint row = 1) : IsOdd (sourceV row) := by
  exact even_mul_odd (even_star (sourceWalshRow_even row h)) anchor_odd

/-- Endpoint 0 gives even K, including the identity-containing anchor row. -/
theorem goldenPair_even (row : Fin 64) (port : Fin 2) (h : rowEndpoint row = 0) :
    IsEven (sourceGoldenPair row port) := by
  have hv := sourceV_even row h
  fin_cases port
  · simp only [sourceGoldenPair]
    apply Commute.sub_right
    · split_ifs <;> simp
    · exact hv.smul_right _
  · simpa [sourceGoldenPair, IsEven] using (hv.smul_right (2 * goldenP * Real.sqrt goldenP)).neg_right

/-- Endpoint 1 is non-anchor and gives odd K for both fine ports. -/
theorem goldenPair_odd (row : Fin 64) (port : Fin 2) (h : rowEndpoint row = 1) :
    IsOdd (sourceGoldenPair row port) := by
  have hn : row ≠ 0 := by
    intro he
    subst row
    norm_num [rowEndpoint] at h
  have hv := sourceV_odd row h
  fin_cases port
  · simpa [sourceGoldenPair, hn] using odd_neg (odd_smul_real (2 * goldenP ^ 2) hv)
  · simpa [sourceGoldenPair] using odd_smul_real (-(2 * goldenP * Real.sqrt goldenP)) hv

/-- Each exact source Kraus slot is parity-homogeneous; zero slots may be both. -/
theorem sourceKraus_homogeneous (slot : Fin 128) :
    IsEven (sourceKraus slot) ∨ IsOdd (sourceKraus slot) := by
  have h : rowEndpoint (krausRow slot) = 0 ∨ rowEndpoint (krausRow slot) = 1 := by
    generalize he : rowEndpoint (krausRow slot) = x
    fin_cases x <;> simp_all
  rcases h with h | h
  · left
    exact goldenPair_even (krausRow slot) (krausPort slot) h
  · right
    exact goldenPair_odd (krausRow slot) (krausPort slot) h

/-- A homogeneous source Kraus update preserves even operators. -/
lemma homogeneous_update_even (K X : Operator) (hK : IsEven K ∨ IsOdd K) (hX : IsEven X) :
    IsEven (Kᴴ * X * K) := by
  rcases hK with hK | hK
  · exact ((even_star hK).mul_right hX).mul_right hK
  · exact odd_mul_odd (odd_mul_even (odd_star hK) hX) hK

/-- Every actual finite chronological source effect commutes with Fock parity. -/
theorem sourceEffect_even (path : List (Fin 128)) : IsEven (sourceEffect path) := by
  induction path with
  | nil => exact Commute.one_right _
  | cons first tail ih =>
    exact homogeneous_update_even (sourceKraus first) (sourceEffect tail)
      (sourceKraus_homogeneous first) ih

end D0.Geometry.OriginalBookEffectParity
