import D0.RG.PhiDifference

namespace D0

theorem betaPhi_linear_flow (g0 b : Real) (k : Nat) :
    betaPhi (fun n => g0 + b * (n : Real) * Real.log phi) k = b := by
  unfold betaPhi
  let L := Real.log phi
  have hL : L ≠ 0 := by
    dsimp [L]
    exact log_phi_ne_zero
  change ((g0 + b * ((k + 1 : Nat) : Real) * L) -
      (g0 + b * (k : Real) * L)) / L = b
  have hnum :
      (g0 + b * ((k + 1 : Nat) : Real) * L) -
      (g0 + b * (k : Real) * L) = b * L := by
    norm_num
    ring
  rw [hnum]
  field_simp [hL]

end D0
