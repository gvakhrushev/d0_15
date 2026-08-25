import Mathlib.Tactic

/-!
# The visible sector in closed form: a rank-one update of the zone sizes

`D0.Spectral.TransportSelfAdjoint` shows the transport operator `Q` is self-adjoint in the
zone-size measure. This module gives the reason and the consequence: `Q` is a **rank-one update of
a diagonal**, so its whole spectrum and eigenbasis close in the zone sizes `9, 11, 13` with no
numerical diagonalisation anywhere.

Write `n = (9, 11, 13)`, `D = diag n`, `𝟙` the all-ones column. Then

    Q = 𝟙 · nᵀ − D                                  (`transport_rank_one`)

— off the diagonal `(𝟙nᵀ)ᵢⱼ = nⱼ` and `Dᵢⱼ = 0`, on the diagonal `nᵢ − nᵢ = 0`. Everything follows.

**Spectrum.** For `Qx = λx` write `s = n · x`. The identity gives `𝟙 s = (D + λ)x`, so
`xᵢ = s / (nᵢ + λ)`, and feeding that back into `s = n · x` yields the secular equation

    9/(9+λ) + 11/(11+λ) + 13/(13+λ) = 1 .

Clearing denominators turns it into `−(λ³ − 359λ − 2574) = 0` (`secular_eq_cubic`): the transport
cubic *is* the secular equation of the rank-one update, not an unrelated characteristic polynomial.

**Eigenbasis.** In the generation basis (zone indicators) the eigenvector for a root `λ` is simply

    x = (1/(9+λ), 1/(11+λ), 1/(13+λ))                (`secular_root_gives_eigenvector`)

verified directly: `(Qx)ᵢ = Σⱼ nⱼxⱼ − nᵢxᵢ = 1 − nᵢ/(nᵢ+λ) = λ/(nᵢ+λ) = λxᵢ`. So the change of
basis from generations to transport modes is written out in the zone sizes alone — the `O(3)`
rotation of `TransportSelfAdjoint` has closed-form entries `√nᵢ/(nᵢ+λ)` after the measure weighting,
and no free parameter enters at any point.

**What this buys.** The visible sector is now completely explicit: three modes, given by the three
roots of a secular equation in the zone sizes, with eigenvectors rational in those sizes and the
root. Together with `D0.Synthesis.ZoneIsGeneration` (one visible direction plus `nᵢ − 1` dark ones
per zone) and `D0.Synthesis.DarkSectorCensus` (three dark couplings, degeneracies `8, 10, 12`), the
whole `33`-dimensional carrier is accounted for in closed form by the three numbers `9, 11, 13`.
-/

namespace D0.Spectral.TransportClosedForm

/-- The transport matrix in the generation basis. -/
def Q : Matrix (Fin 3) (Fin 3) ℚ := !![0, 11, 13; 9, 0, 13; 9, 11, 0]

/-- The zone sizes. -/
def n : Fin 3 → ℚ := ![9, 11, 13]

/-- The rank-one matrix `𝟙 · nᵀ`: every row is the zone-size vector. -/
def onesN : Matrix (Fin 3) (Fin 3) ℚ := Matrix.of fun _ j => n j

/-- The zone-size diagonal. -/
def Dm : Matrix (Fin 3) (Fin 3) ℚ := Matrix.diagonal n

/-- **The structural identity.** `Q` is a rank-one update of the zone-size diagonal. -/
theorem transport_rank_one : Q = onesN - Dm := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Q, onesN, Dm, n, Matrix.diagonal]

/-- Every row of `onesN` is the same, so it has rank one. -/
theorem onesN_rows_equal (i i' j : Fin 3) : onesN i j = onesN i' j := rfl

/-- **The secular equation is the transport cubic.** Clearing denominators in
`Σ nᵢ/(nᵢ+λ) = 1` gives `λ³ − 359λ − 2574 = 0`. -/
theorem secular_eq_cubic (l : ℚ) (h9 : 9 + l ≠ 0) (h11 : 11 + l ≠ 0) (h13 : 13 + l ≠ 0) :
    (9 / (9 + l) + 11 / (11 + l) + 13 / (13 + l) = 1) ↔ l ^ 3 - 359 * l - 2574 = 0 := by
  rw [div_add_div _ _ h9 h11, div_add_div _ _ (mul_ne_zero h9 h11) h13,
    div_eq_one_iff_eq (mul_ne_zero (mul_ne_zero h9 h11) h13)]
  constructor <;> intro h <;> nlinarith [h, sq_nonneg l]

/-- **The eigenvector in closed form.** For a root of the secular equation the vector
`x = (1/(9+λ), 1/(11+λ), 1/(13+λ))` satisfies `Qx = λx`, checked coordinate by coordinate. -/
theorem secular_root_gives_eigenvector (l : ℚ)
    (h9 : 9 + l ≠ 0) (h11 : 11 + l ≠ 0) (h13 : 13 + l ≠ 0)
    (hsec : 9 / (9 + l) + 11 / (11 + l) + 13 / (13 + l) = 1) :
    11 * (1 / (11 + l)) + 13 * (1 / (13 + l)) = l * (1 / (9 + l)) ∧
    9 * (1 / (9 + l)) + 13 * (1 / (13 + l)) = l * (1 / (11 + l)) ∧
    9 * (1 / (9 + l)) + 11 * (1 / (11 + l)) = l * (1 / (13 + l)) := by
  have e9 : 9 / (9 + l) = 9 * (1 / (9 + l)) := by ring
  have e11 : 11 / (11 + l) = 11 * (1 / (11 + l)) := by ring
  have e13 : 13 / (13 + l) = 13 * (1 / (13 + l)) := by ring
  rw [e9, e11, e13] at hsec
  refine ⟨?_, ?_, ?_⟩
  · have hx : (9 : ℚ) * (1 / (9 + l)) + l * (1 / (9 + l)) = 1 := by
      field_simp
    linarith [hsec, hx]
  · have hx : (11 : ℚ) * (1 / (11 + l)) + l * (1 / (11 + l)) = 1 := by
      field_simp
    linarith [hsec, hx]
  · have hx : (13 : ℚ) * (1 / (13 + l)) + l * (1 / (13 + l)) = 1 := by
      field_simp
    linarith [hsec, hx]

/-- **Assembled.** Rank-one structure, secular equation equal to the transport cubic, and the
closed-form eigenvector — the visible sector expressed entirely in `9, 11, 13`. -/
theorem visible_sector_closed_form :
    Q = onesN - Dm ∧
    (∀ l : ℚ, 9 + l ≠ 0 → 11 + l ≠ 0 → 13 + l ≠ 0 →
      ((9 / (9 + l) + 11 / (11 + l) + 13 / (13 + l) = 1) ↔ l ^ 3 - 359 * l - 2574 = 0)) :=
  ⟨transport_rank_one, fun l a b c => secular_eq_cubic l a b c⟩

end D0.Spectral.TransportClosedForm
