import D0.Core.Delta
import Mathlib.Tactic

namespace D0

noncomputable def stopIdeal : Real :=
  delta0 ^ 12

noncomputable def etaHC (ellP L : Real) : Real :=
  (ellP / L)^2

theorem phi_pos : 0 < phi := by
  unfold phi
  positivity

theorem delta0_pos : 0 < delta0 := by
  rw [delta_phi_cubed]
  exact one_div_pos.mpr (mul_pos (by norm_num) (pow_pos phi_pos 3))

theorem stopIdeal_positive : 0 < stopIdeal := by
  unfold stopIdeal
  exact pow_pos delta0_pos 12

theorem higher_curvature_suppressed_for_large_L
    {ellP L : Real}
    (hL : L >= ellP / delta0^6)
    (hpos : 0 < ellP) :
    etaHC ellP L <= delta0^12 := by
  have hdelta : 0 < delta0 := delta0_pos
  have hdelta6 : 0 < delta0^6 := pow_pos hdelta _
  have hLpos : 0 < L := by
    exact lt_of_lt_of_le (div_pos hpos hdelta6) hL
  have hmain : ellP <= L * delta0^6 := by
    have hLle : ellP / delta0^6 <= L := hL
    exact (div_le_iff₀ hdelta6).mp hLle
  have hratio : ellP / L <= delta0^6 := by
    rw [div_le_iff₀ hLpos]
    nlinarith
  have hratio_nonneg : 0 <= ellP / L := by
    exact le_of_lt (div_pos hpos hLpos)
  have hsq : (ellP / L)^2 <= (delta0^6)^2 := by
    simpa [pow_two] using
      (mul_le_mul hratio hratio hratio_nonneg (le_of_lt hdelta6))
  calc
    etaHC ellP L = (ellP / L)^2 := rfl
    _ <= (delta0^6)^2 := hsq
    _ = delta0^12 := by ring

end D0
