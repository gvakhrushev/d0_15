import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Tactic

/-!
# Matched branch amplitude derivative

For each copy the original matched corner has the form `1 - 2 * (Q₀ + g * Iⱼ)`.
This finite product rule derives the owner-supplied `hfield` amplitude
variation from differentiable, independently varying copy actions, on a
single real-parameter curve. Local equality with the actual branch amplitude
is an explicit input to the consumer below. This module constructs no actual
field map, resolvent-weight binding, native execution, full price or GR result.
The original source is #334 commit `b42db3deb79a55d4ede542ac4aef54a2c2f1106c`,
blob `886cac666344703940ebb699a304be2f86fb75bb`, H4/H5/H18 and §2 R1.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchAmplitude

open Filter
open scoped BigOperators Topology

/-- Finite product of the independent scalar action corners. -/
def amplitude (M : ℕ) (Q₀ g : ℝ) (I : Fin M → ℝ → ℝ) (y : ℝ) : ℝ :=
  ∏ j : Fin M, (1 - 2 * (Q₀ + g * I j y))

/-- Full finite-product derivative at a matched corner. No nonzero corner,
positivity or nonempty-index assumption is required. -/
theorem amplitude_hasDerivAt_matched
    (M : ℕ) (Q₀ g p c : ℝ) (I : Fin M → ℝ → ℝ) (dI : Fin M → ℝ)
    (hI : ∀ j, HasDerivAt (I j) (dI j) p)
    (hmatch : ∀ j, 1 - 2 * (Q₀ + g * I j p) = c) :
    HasDerivAt (amplitude M Q₀ g I)
      (-2 * g * c^(M-1) * ∑ j : Fin M, dI j) p := by
  let f : Fin M → ℝ → ℝ := fun j y => 1 - 2 * (Q₀ + g * I j y)
  have hf : ∀ j ∈ (Finset.univ : Finset (Fin M)),
      HasDerivAt (f j) (-2 * g * dI j) p := by
    intro j hj
    have h := (hasDerivAt_const p (1 : ℝ)).sub
      (((hI j).const_mul g).const_add Q₀ |>.const_mul 2)
    convert h using 1
    all_goals (try dsimp [f])
    all_goals ring
  have hp := HasDerivAt.fun_finsetProd hf
  have heach : ∀ j : Fin M,
      (∏ k ∈ (Finset.univ : Finset (Fin M)).erase j, f k p) = c^(M-1) := by
    intro j
    calc
      _ = ∏ _k ∈ (Finset.univ : Finset (Fin M)).erase j, c := by
        apply Finset.prod_congr rfl
        intro k hk
        exact hmatch k
      _ = c^(M-1) := by
        rw [Finset.prod_const, Finset.card_erase_of_mem (Finset.mem_univ j), Finset.card_fin]
  have hs : (∑ j ∈ (Finset.univ : Finset (Fin M)),
      (∏ k ∈ (Finset.univ : Finset (Fin M)).erase j, f k p) • (-2 * g * dI j)) =
      -2 * g * c^(M-1) * ∑ j : Fin M, dI j := by
    calc
      _ = ∑ j : Fin M, ((-2 * g * c^(M-1)) * dI j) := by
        apply Finset.sum_congr rfl
        intro j hj
        rw [heach j]
        simp only [smul_eq_mul]
        ring
      _ = _ := by rw [Finset.mul_sum]
  rw [hs] at hp
  exact hp

/-- If an actual branch amplitude has the stated product locally, its supplied
curve derivative must satisfy the field-source input used by the owner.
The local binding and the derivatives of each action are hypotheses. -/
theorem branch_derivatives_forced
    {θ : Type*} (s : Finset θ) (M : ℕ) (Q₀ g p c : ℝ)
    (amp : θ → ℝ → ℝ) (damp : θ → ℝ)
    (I : θ → Fin M → ℝ → ℝ) (dI : θ → Fin M → ℝ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hlocal : ∀ i ∈ s, amp i =ᶠ[𝓝 p] amplitude M Q₀ g (I i))
    (hI : ∀ i ∈ s, ∀ j, HasDerivAt (I i j) (dI i j) p)
    (hmatch : ∀ i ∈ s, ∀ j, 1 - 2 * (Q₀ + g * I i j p) = c) :
    ∀ i ∈ s, damp i = -2 * g * c^(M-1) * ∑ j : Fin M, dI i j := by
  intro i hi
  have h := amplitude_hasDerivAt_matched M Q₀ g p c (I i) (dI i)
    (hI i hi) (hmatch i hi)
  exact (hamp i hi).unique (h.congr_of_eventuallyEq (hlocal i hi))

/-- With no copies, the finite product is one and the derivative vanishes.
This does not remove the owner's separate assumption `M > 0`. -/
theorem amplitude_zero_copies (Q₀ g : ℝ) (I : Fin 0 → ℝ → ℝ) (p : ℝ) :
    amplitude 0 Q₀ g I p = 1 ∧ HasDerivAt (amplitude 0 Q₀ g I) 0 p := by
  have h : amplitude 0 Q₀ g I = fun _ => 1 := by
    funext y
    simp [amplitude]
  rw [h]
  exact ⟨rfl, hasDerivAt_const p 1⟩


/-- Two matched copy values with different independent velocities. -/
def twoCopyActions (j : Fin 2) (y : ℝ) : ℝ :=
  if j = 0 then y else -2 * y

/-- The copy derivatives 1 and -2 are retained separately; their sum gives
an amplitude derivative of 2. -/
theorem two_copy_independent_control :
    HasDerivAt (twoCopyActions 0) 1 0 ∧
    HasDerivAt (twoCopyActions 1) (-2) 0 ∧
    HasDerivAt (amplitude 2 0 1 twoCopyActions) 2 0 := by
  have ha : ∀ j : Fin 2,
      HasDerivAt (twoCopyActions j) (if j = 0 then 1 else -2) 0 := by
    intro j
    fin_cases j
    · simpa [twoCopyActions] using (hasDerivAt_id (0 : ℝ))
    · change HasDerivAt (fun y : ℝ => -2 * y) (-2) 0
      simpa using ((hasDerivAt_id (0 : ℝ)).const_mul (-2))
  have hm : ∀ j : Fin 2, 1 - 2 * (0 + 1 * twoCopyActions j 0) = 1 := by
    intro j
    fin_cases j <;> norm_num [twoCopyActions]
  have h := amplitude_hasDerivAt_matched 2 0 1 0 1 twoCopyActions
    (fun j => if j = 0 then 1 else -2) ha hm
  constructor
  · simpa using ha 0
  constructor
  · simpa using ha 1
  · norm_num [Fin.sum_univ_two] at h
    exact h

end D0.Analysis.MatchedBranchAmplitude
end
