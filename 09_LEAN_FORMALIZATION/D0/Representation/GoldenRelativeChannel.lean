import D0.Representation.GoldenOrderInterferometer

/-!
# The golden asymmetry in relative readout

The kernel below is the squared-entry response of the existing golden gate.
It propagates diagonal input weights; coherent evolution is still the gate itself.
Iterating this kernel therefore requires diagonalization between stages and is not
identified with coherent ticks or spatial dimension.
-/
namespace D0.Representation.GoldenRelativeChannel

open Matrix D0.Representation.GoldenOrderInterferometer

noncomputable def delta (p : ℝ) : ℝ := (p - p^2) / 2
def kernel (p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![p,p^2; p^2,p]

theorem kernel_from_gate (a p : ℝ) (ha : a^2 = p) (i j : Fin 2) :
    kernel p i j = (gate a p i j)^2 := by
  fin_cases i <;> fin_cases j <;> simp [kernel, gate, ha]

theorem twice_delta (p : ℝ) (hp : p + p^2 = 1) :
    2 * delta p = p^3 := by
  unfold delta
  linarith [golden_cube p hp]

/-- Total weight is preserved, while the signed difference is multiplied by 2 delta. -/
theorem mass_and_contrast (p x y : ℝ) (hp : p + p^2 = 1) :
    (kernel p |>.mulVec ![x,y]) 0 + (kernel p |>.mulVec ![x,y]) 1 = x+y ∧
    (kernel p |>.mulVec ![x,y]) 0 - (kernel p |>.mulVec ![x,y]) 1 =
      2 * delta p * (x-y) := by
  simp [kernel, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  constructor
  · nlinarith [congrArg (fun t : ℝ => t*x) hp, congrArg (fun t : ℝ => t*y) hp]
  · unfold delta
    ring

/-- The same delta fixes both probabilities in the previously constructed coherent order detector. -/
theorem coherent_order_weights (a p : ℝ) (ha : a^2 = p) (hp : p + p^2 = 1) :
    (output a p (-1) 0)^2 = 4 * (delta p)^2 ∧
    (output a p (-1) 1)^2 = 8 * delta p ∧
    4 * (delta p)^2 + 8 * delta p = 1 := by
  have hw := minus_path_weights a p ha hp
  have hd := twice_delta p hp
  have hs : p^6 = 4 * (delta p)^2 := by
    calc
      p^6 = (p^3)^2 := by ring
      _ = 4 * (delta p)^2 := by rw [← hd]; ring
  rw [hs] at hw
  exact ⟨hw.1, by linarith [hw.2.1], by linarith [hw.2.2]⟩

end D0.Representation.GoldenRelativeChannel
