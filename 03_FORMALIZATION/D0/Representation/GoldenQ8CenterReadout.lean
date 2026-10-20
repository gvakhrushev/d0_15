import D0.Representation.GoldenOrderInterferometer
import D0.Foundation.Omega8Center

/-! Native #334 extension extracted without changing the accepted base owner.
Original declarations: `03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean` at
`07f2f2b15b7050a612d0075aa73db8dc46087a95`.
The shared definitions are imported from their maintained main modules. -/

namespace D0.Representation.GoldenOrderInterferometer

open Matrix

/-- Mathematical decoding of the ALREADY OWNED central Q8 ±1 pair.
Only intended for center inputs with q=qONE or q=qNEG. -/
def q8_center_sign (q : D0.Foundation.UQuat) : ℝ :=
  if q = D0.Foundation.qNEG then -1 else 1

theorem q8_center_sign_plus :
    q8_center_sign D0.Foundation.qONE = 1 := by
  simp [q8_center_sign, D0.Foundation.qONE, D0.Foundation.qNEG]

theorem q8_center_sign_minus :
    q8_center_sign D0.Foundation.qNEG = -1 := by
  simp [q8_center_sign]

/-- The ORIGINAL Q8 order commutator already yields the minus input
which the separately registered Golden order detector can distinguish. -/
theorem original_q8_ij_order_has_negative_golden_sign :
    q8_center_sign
      (D0.Foundation.uqmul
        (D0.Foundation.uqmul (0,1,0,0) (0,0,1,0))
        (D0.Foundation.uqmul
          (D0.Foundation.uqinv (0,1,0,0))
          (D0.Foundation.uqinv (0,0,1,0)))) = -1 := by
  rw [D0.Foundation.commutator_ij_eq_neg]
  exact q8_center_sign_minus

/-- An EXACT positive Golden order-port comparison of native Q8
center records: the +1 central class has a dark second port,
while the -1 commutator class gives probability 4*p^3 >0.
No new angle, detector, or Q8 group operation has been defined. -/
theorem q8_center_order_golden_detectable :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    (output a p (q8_center_sign D0.Foundation.qONE) 1)^2 = 0 ∧
    (output a p (q8_center_sign D0.Foundation.qNEG) 1)^2 = 4*p^3 ∧
    0 < (output a p (q8_center_sign D0.Foundation.qNEG) 1)^2 := by
  dsimp
  have ha := Real.sq_sqrt (le_of_lt primitive_positive)
  have hp := D0.primitive_root_satisfies
  rw [q8_center_sign_plus, q8_center_sign_minus]
  have hplus := plus_path_returns (Real.sqrt D0.primitiveRoot) D0.primitiveRoot ha hp
  have hminus := minus_path_weights (Real.sqrt D0.primitiveRoot) D0.primitiveRoot ha hp
  refine ⟨?_, hminus.2.1, ?_⟩
  · rw [hplus]
    norm_num
  · rw [hminus.2.1]
    exact mul_pos (by norm_num) (pow_pos primitive_positive _)


end D0.Representation.GoldenOrderInterferometer
