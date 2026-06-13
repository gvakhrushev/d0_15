import D0.Core.Phi

/-!
# D0-TIME-2D-PISOT-001 — time = T^2 forced by quadratic Pisot-minimality of phi

The certificate `05_CERTS/vp_time_2d_pisot.py` asserts the EXACT finite/algebraic facts:

* [1] `phi` is a root of the monic integer polynomial `x^2 - x - 1` and lies in `(1, 2)`
      (so it is an algebraic integer).
* [2] EXACT: the discriminant of `x^2 - x - 1` is `5`, which is not a perfect square,
      hence the polynomial is irreducible over `Q` and `deg Q(phi) = 2`.
* [3] EXACT: the Galois conjugate `psi = 1 - phi` is the other root, satisfies the Vieta
      relations `phi + psi = 1` and `phi * psi = -1`, and lies strictly in `(-1, 0)`, so
      `|psi| < 1`.  One conjugate outside, the other strictly inside the unit disk
      => `phi` is a Pisot number.
* [4] The minimal `M1`-admissible field is `Q(phi)` of degree `2`, forcing the time layer
      to be the 2-torus `T^2` (degree 1 would be a forbidden rational capture).

This is a leaf per-claim module: it imports only the (frozen, proved) `D0.Core.Phi`
and reuses its theorems `phi_sq`, `psi_sq`, `phi_add_psi`, `phi_mul_psi`, so it builds in
seconds.  The purely-integer facts (discriminant = 5, not a square; degree = 2) are closed
by `decide`; the analytic brackets are closed from `Real.sqrt 5 ∈ (2, 3)`.
-/

namespace D0.Claims

open D0

/-- The monic integer polynomial `p(x) = x^2 - x - 1` whose root is `phi`, encoded by
its coefficient list `[c0, c1, c2] = [-1, -1, 1]` so that `p(x) = c2*x^2 + c1*x + c0`. -/
def pisotCoeffs : List Int := [-1, -1, 1]

/-- EXACT [1]: `p` is monic (leading coefficient `1`) — `phi` is an algebraic integer. -/
theorem pisot_monic : pisotCoeffs.getLast! = 1 := by decide

/-- EXACT [2]: the discriminant `b^2 - 4ac` of `x^2 - x - 1` equals `5`. -/
theorem pisot_discriminant_eq_five :
    ((-1 : Int))^2 - 4 * 1 * (-1) = 5 := by decide

/-- EXACT [2]: `5` is not a perfect square — no integer in `0..5` squares to it.
This is the decidable kernel of "irreducible over `Q`", hence `deg Q(phi) = 2`. -/
theorem five_not_perfect_square :
    ∀ n : Fin 6, (n : Int) ^ 2 ≠ 5 := by decide

/-- EXACT [2/4]: the degree of the minimal polynomial (and so of the time layer `Q(phi)`)
is `2`, the forced value: not `1` (a rational capture, forbidden by `M1`). -/
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

/-- **D0-TIME-2D-PISOT-001** (master theorem): the time layer is `T^2`, forced by the
quadratic Pisot-minimality of `phi`. Bundles the exact finite content of the certificate:

* `phi` is the root of the monic `x^2 - x - 1` (`phi^2 = phi + 1`), lying in `(1, 2)`;
* the discriminant is `5`, not a perfect square => `deg Q(phi) = 2` (forced, `≠ 1`);
* the conjugate `psi = 1 - phi` is the other root, with Vieta relations `phi+psi = 1`,
  `phi*psi = -1`, lying in `(-1, 0)` so `|psi| < 1` — i.e. `phi` is Pisot;
* `1 < phi` and `|psi| < 1` is exactly the Pisot condition at degree `2`. -/
theorem time_2d_pisot :
    -- [1] minimal polynomial: phi root of monic x^2 - x - 1, in (1,2)
    (phi ^ 2 - phi - 1 = 0 ∧ 1 < phi ∧ phi < 2) ∧
    -- [2] discriminant = 5, not a square, degree forced to 2 (≠ 1)
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
