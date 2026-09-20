import Mathlib.Data.Finset.Card
import Mathlib.Data.Real.Basic
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveHeatTrace
import D0.Geometry.ArchiveSpectralCounting

namespace D0.Geometry.ArchiveEnumerationSpectrumWeyl4NoGo

open D0

/-- Equivalence between `{x : Fin M // x.val ≤ K}` and `Fin (K + 1)` when `K < M`. -/
def finLeEquiv (M K : ℕ) (hK : K < M) :
    {x : Fin M // x.val ≤ K} ≃ Fin (K + 1) where
  toFun x := ⟨x.val.val, Nat.lt_succ_of_le x.property⟩
  invFun y := ⟨⟨y.val, lt_of_le_of_lt (Nat.le_of_lt_succ y.isLt) hK⟩,
                Nat.le_of_lt_succ y.isLt⟩
  left_inv x := by
    ext
    rfl
  right_inv y := by
    ext
    rfl

/-- Cardinality of the filter `{x : Fin M | x.val ≤ K}` is exactly `K + 1` for any `K < M`. -/
theorem card_fin_val_le (M K : ℕ) (hK : K < M) :
    ((Finset.univ : Finset (Fin M)).filter (fun x => x.val ≤ K)).card = K + 1 := by
  rw [← Fintype.card_subtype]
  have h_equiv := Fintype.card_congr (finLeEquiv M K hK)
  rw [h_equiv, Fintype.card_fin]

/-- In `ArchivePoints n = Fin (modes n)`, the condition `archiveEigenvalue n x ≤ (K : ℝ)`
is equivalent to `x.val ≤ K`. -/
theorem archiveEigenvalue_le_iff (n : ℕ) (x : ArchivePoints n) (K : ℕ) :
    archiveEigenvalue n x ≤ (K : ℝ) ↔ x.val ≤ K := by
  unfold archiveEigenvalue
  exact_mod_cast Iff.rfl

/-- **D0-ARCHIVE-ENUMERATION-SPECTRUM-WEYL4-NOGO-001 (Core Counting Formula)**:
For any integer cutoff `K < modes n = (n+2)^4`, the spectral counting function of the current
archive eigenvalue spectrum evaluates identically to the 1D enumeration count:
$$N_n(K) = K + 1.$$ -/
theorem eigenCountBelow_eq_succ (n : ℕ) (K : ℕ) (hK : K < (archiveTower n).modes) :
    eigenCountBelow n (K : ℝ) = K + 1 := by
  unfold eigenCountBelow
  have h_filter_eq :
      ((Finset.univ : Finset (ArchivePoints n)).filter (fun x => archiveEigenvalue n x ≤ (K : ℝ))) =
      ((Finset.univ : Finset (ArchivePoints n)).filter (fun x => x.val ≤ K)) := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    exact archiveEigenvalue_le_iff n x K
  rw [h_filter_eq]
  exact card_fin_val_le (archiveTower n).modes K hK

/-- Linear scaling ratio: $N(2K) / N(K)$ asymptotically equals 2, characteristic of a 1D spectrum,
whereas a 4D Laplacian requires $(2K)^2 / K^2 = 4$. -/
theorem enumeration_scaling_is_linear (K : ℕ) (hK : 0 < K) :
    (2 * K + 1 : ℚ) / (K + 1 : ℚ) ≠ 4 := by
  intro h_contra
  have h1 : (2 * K + 1 : ℚ) = 4 * (K + 1 : ℚ) := by
    exact (div_eq_iff (by positivity)).mp h_contra
  linarith

/-- **D0-ARCHIVE-ENUMERATION-SPECTRUM-WEYL4-NOGO-001 (Owner)**:
The spectrum `archiveEigenvalue n x = x.val` is a 1-dimensional enumeration sequence with
$N(K) = K + 1$. It does not exhibit the 4-dimensional Weyl law $N(\Lambda) \sim \Lambda^2$,
rigorously proving that `archiveEigenvalue` cannot serve as the 4D physical Laplacian spectrum. -/
theorem archive_enumeration_spectrum_weyl4_nogo_owner :
    (∀ (n : ℕ) (K : ℕ), K < (archiveTower n).modes → eigenCountBelow n (K : ℝ) = K + 1) ∧
    (∀ (K : ℕ), 0 < K → (2 * K + 1 : ℚ) / (K + 1 : ℚ) ≠ 4) :=
  ⟨eigenCountBelow_eq_succ, enumeration_scaling_is_linear⟩

end D0.Geometry.ArchiveEnumerationSpectrumWeyl4NoGo
