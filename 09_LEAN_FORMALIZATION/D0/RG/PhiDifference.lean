import D0.Core.Phi
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

namespace D0

noncomputable def LambdaAct : Real := 1

noncomputable def phiScale (k : Nat) : Real :=
  LambdaAct * phi^(-(k : Int))

noncomputable def betaPhi (g : Nat -> Real) (k : Nat) : Real :=
  (g (k + 1) - g k) / Real.log phi

theorem phi_pos : 0 < phi := by
  unfold phi
  positivity

theorem phi_ne_one : phi ≠ 1 := by
  unfold phi
  intro h
  have hs : Real.sqrt 5 = 1 := by linarith
  have hsq : (Real.sqrt 5)^2 = (1 : Real)^2 := by rw [hs]
  rw [sqrt_five_sq] at hsq
  norm_num at hsq

theorem log_phi_ne_zero : Real.log phi ≠ 0 :=
  Real.log_ne_zero_of_pos_of_ne_one phi_pos phi_ne_one

end D0
