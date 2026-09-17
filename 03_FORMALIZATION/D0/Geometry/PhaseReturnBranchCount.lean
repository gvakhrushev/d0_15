import D0.Combinatorics.ForcedReturnWindows

namespace D0.Geometry

/-!
Finite return-modulus branch counts for the D0 phase-unfolding windows.
-/

/-- Branch-count statement for the terminal and electroweak return windows. -/
def FiniteReturnModulusBranchCount : Prop :=
  D0.qT = 44 /\
    D0.mT = 7 /\
      D0.d13 = 20 /\
        D0.qEW = 710 /\
          D0.mEW = 113 /\
            Nat.totient D0.qEW = 280 /\
              D0.DEW = 35

/-- The finite return moduli unfold the D0 visible branch counts. -/
theorem finite_return_modulus_unfolds_branches :
    FiniteReturnModulusBranchCount := by
  unfold FiniteReturnModulusBranchCount
  refine ⟨D0.lcm_abcd_v11, ?_, D0.d13_from_return_window, D0.qEW_forced, ?_, ?_, D0.ew_depth_from_omega8⟩
  · native_decide
  · native_decide
  · rw [D0.qEW_forced]
    exact D0.totient_710

/-- Terminal branch count is Euler's totient of the first return modulus. -/
theorem terminal_return_branch_count :
    Nat.totient D0.qT = 20 := by
  rw [D0.lcm_abcd_v11]
  exact D0.totient_44

/-- Electroweak branch count is Euler's totient of the second return modulus. -/
theorem electroweak_return_branch_count :
    Nat.totient D0.qEW = 280 := by
  rw [D0.qEW_forced]
  exact D0.totient_710

/-- The electroweak branch count projects through the eight-role orientation quotient. -/
theorem electroweak_return_depth_eq_35 :
    D0.DEW = 35 := by
  exact D0.ew_depth_from_omega8

end D0.Geometry
