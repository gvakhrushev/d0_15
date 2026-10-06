import D0.Core.Phi

/-!
# D0-TIME-2D-PISOT-001 — finite quadratic-root and conjugate facts

The declaration names are historical. Read the proposition `time_2d_pisot`
itself as the owner: it bundles the two root equations, root brackets, Vieta
identities, the discriminant calculation, a bounded `Fin 6` nonsquare check,
and the degree of the explicit coefficient list. It reuses `D0.Core.Phi`.

This module does not construct a time torus, a physical time variable, an
entropy law, a KAM result, or a coefficient selector. In particular the list
length calculation is not a formal proof that a specified polynomial is a
minimal polynomial or that a number-field extension has degree two. Such
identifications require separate statements. No mathematical declaration or
proof is changed by this scope clarification.
-/

namespace D0.Claims

open D0

/-- The monic integer polynomial `p(x) = x^2 - x - 1` whose root is `phi`, encoded by
its coefficient list `[c0, c1, c2] = [-1, -1, 1]` so that `p(x) = c2*x^2 + c1*x + c0`. -/
def pisotCoeffs : List Int := [-1, -1, 1]

/-- The last entry of the specified coefficient list is `1`. -/
theorem pisot_monic : pisotCoeffs.getLast! = 1 := by decide

/-- EXACT [2]: the discriminant `b^2 - 4ac` of `x^2 - x - 1` equals `5`. -/
theorem pisot_discriminant_eq_five :
    ((-1 : Int))^2 - 4 * 1 * (-1) = 5 := by decide

/-- EXACT [2]: `5` is not a perfect square — no integer in `0..5` squares to it.
This statement is bounded to `Fin 6`; it is not an irreducibility declaration. -/
theorem five_not_perfect_square :
    ∀ n : Fin 6, (n : Int) ^ 2 ≠ 5 := by decide

/-- The explicit coefficient list has length minus one equal to `2`, not `1`. -/
theorem pisot_degree_eq_two : pisotCoeffs.length - 1 = 2 ∧ (2 : Nat) ≠ 1 := by decide

/-- [1] `phi` is a root of `x^2 - x - 1`, i.e. `phi^2 - phi - 1 = 0`. -/
theorem phi_root_minimal_poly : phi ^ 2 - phi - 1 = 0 := by
  have h := phi_sq
  linarith

/-- [3] `psi = 1 - phi` is the Galois conjugate: it is the other root of `x^2 - x - 1`,
i.e. `psi^2 - psi - 1 = 0`. -/
theorem psi_root_minimal_poly : psi ^ 2 - psi - 1 = 0 := by
  have h := psi_sq
  linarith

/-- [3] Vieta sum: `phi + psi = 1` (sum of the two conjugate roots). -/
theorem pisot_vieta_sum : phi + psi = 1 := phi_add_psi

/-- [3] Vieta product: `phi * psi = -1` (product of the two conjugate roots; magnitude `1`
with one root outside and one inside the unit disk). -/
theorem pisot_vieta_prod : phi * psi = -1 := phi_mul_psi

/-- `Real.sqrt 5` lies strictly in the open interval `(2, 3)`. -/
theorem sqrt5_bracket : 2 < Real.sqrt 5 ∧ Real.sqrt 5 < 3 := by
  constructor
  · have : (2 : ℝ) = Real.sqrt 4 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    rw [this]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  · have h : Real.sqrt 5 < Real.sqrt 9 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    rwa [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)] at h

/-- [1] `phi ∈ (1, 2)`: the dominant root lies strictly between `1` and `2`. -/
theorem phi_bracket : 1 < phi ∧ phi < 2 := by
  obtain ⟨h2, h3⟩ := sqrt5_bracket
  unfold phi
  constructor <;> linarith

/-- [3] `psi ∈ (-1, 0)`: the conjugate root lies strictly inside the unit disk, so
`|psi| < 1`. Together with `phi > 1` this is the Pisot property of `phi`. -/
theorem psi_bracket : -1 < psi ∧ psi < 0 := by
  obtain ⟨h2, h3⟩ := sqrt5_bracket
  unfold psi
  constructor <;> linarith

/-- [3] Pisot conclusion: `|psi| < 1` (the conjugate is strictly inside the unit disk). -/
theorem psi_abs_lt_one : |psi| < 1 := by
  obtain ⟨h2, h3⟩ := psi_bracket
  rw [abs_lt]
  constructor <;> linarith

/-- Bundle of the displayed finite/algebraic root facts. The conclusion contains
no time torus or physical-time construction. -/
theorem time_2d_pisot :
    -- [1] phi root equation and bracket
    (phi ^ 2 - phi - 1 = 0 ∧ 1 < phi ∧ phi < 2) ∧
    -- [2] discriminant, bounded nonsquare test and coefficient-list degree
    (((-1 : Int))^2 - 4 * 1 * (-1) = 5 ∧
      (∀ n : Fin 6, (n : Int) ^ 2 ≠ 5) ∧
      pisotCoeffs.length - 1 = 2 ∧ (2 : Nat) ≠ 1) ∧
    -- [3] conjugate psi: other root, Vieta, strictly inside unit disk => Pisot
    (psi ^ 2 - psi - 1 = 0 ∧ phi + psi = 1 ∧ phi * psi = -1 ∧
      |psi| < 1 ∧ 1 < phi) := by
  refine ⟨⟨phi_root_minimal_poly, phi_bracket.1, phi_bracket.2⟩,
    ⟨pisot_discriminant_eq_five, five_not_perfect_square, ?_, ?_⟩,
    ⟨psi_root_minimal_poly, pisot_vieta_sum, pisot_vieta_prod, psi_abs_lt_one,
      phi_bracket.1⟩⟩
  · decide
  · decide

end D0.Claims
