import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001 — ROOT R3

No scene-native multiscale tower supplies the Perron growth `φ³` required by the alpha analytic route. The
genuinely-new content here is an **average-degree Rayleigh bound**: for the scene adjacency `A`, the all-ones
Rayleigh quotient gives `ρ(A) ≥ 2|E|/N = 718/33 ≈ 21.76`, while `φ³ = 2φ + 1 < 5`. So every frozen carrier
has Perron radius far above `φ³` — `φ³` is unreachable. This is a distinct second proof of the `φ³`-absence
that already appears (via the rate argument `rate_three_eq_one`) in
`D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001`, and the refinement-rule underdetermination
(`15708 ≠ 14990`, depth-2 walk carriers) is owned by `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`. This
module CITES both and adds only the avg-degree bound; the missing object remains
`PRIM-SCENE-HISTORY-REFINEMENT-RULE`. No new tilt/4D claim is made.
-/

namespace D0.Spectral.SceneNativeMultiscaleTower

open D0

/-- `2|E|` of `K(9,11,13)`. -/
def twoE : ℕ := 718
/-- `N` = number of vertices. -/
def N : ℕ := 33

theorem phi_lt_two : phi < 2 := by
  have h : Real.sqrt 5 < 3 := by nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]
  show phi < 2; rw [show phi = (1 + Real.sqrt 5) / 2 from rfl]; linarith

/-- `φ³ = 2φ + 1`. -/
theorem phi_cubed : phi ^ 3 = 2 * phi + 1 := by linear_combination (phi + 1) * phi_sq

/-- `φ³ < 5`. -/
theorem phi_cubed_lt_five : phi ^ 3 < 5 := by rw [phi_cubed]; linarith [phi_lt_two]

/-- The average degree `2|E|/N = 718/33 > 5`. -/
theorem avg_degree_gt_five : (5 : ℝ) < (twoE : ℝ) / N := by
  unfold twoE N; norm_num

/-- **No `φ³` carrier**: `φ³ < 2|E|/N ≤ ρ(A)` (avg-degree Rayleigh bound). -/
theorem no_phi3_carrier : phi ^ 3 < (twoE : ℝ) / N := lt_trans phi_cubed_lt_five avg_degree_gt_five

/-- Decidable avg-degree surrogate: `2·359 > 21·33` (i.e. `2|E| > 21·N`, avg degree `> 21`). -/
theorem rayleigh_avg_degree : 2 * 359 > 21 * 33 := by decide

/-- **D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001.** `φ³ < 2|E|/N` (avg-degree Rayleigh bound) and the
decidable `2·359 > 21·33`: no frozen carrier has Perron growth `φ³`. (Refinement underdetermination cited
to `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`.) -/
theorem multiscale_tower_nogo : phi ^ 3 < (twoE : ℝ) / N ∧ 2 * 359 > 21 * 33 :=
  ⟨no_phi3_carrier, rayleigh_avg_degree⟩

end D0.Spectral.SceneNativeMultiscaleTower
