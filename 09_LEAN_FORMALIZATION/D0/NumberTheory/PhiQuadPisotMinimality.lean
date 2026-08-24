import Mathlib.Tactic
import D0.NumberTheory.HurwitzMinimaxPhi

/-!
# D0-PHI-QUADPISOT-MINIMALITY-001 — `φ` is the minimal quadratic Pisot number (triple selector)

The D0 primitive detector skeleton forces the response split `p + p² = 1` with unique root
`p = φ⁻¹` (`D0.Core.Phi`, §01.6).  This module adds an **independent leg** to that forcing:
within *all* quadratic Pisot numbers, `φ` is the minimum.

Three classical selectors each single out `φ`, and this module composes them:

* **Selector 1 — self-reference (owned upstream).**  The period-one fixed-point family
  `β_a = a + tail_a`, where `tail_a² + a·tail_a = 1`
  (`D0.NumberTheory.HurwitzMinimaxPhi.periodOneTail`); equivalently, roots of `x² − a·x − 1`
  with `a ≥ 1`, and `β₁ = φ`.
* **Selector 2 — Hurwitz minimax within the class (owned upstream).**
  `periodOneBadApproxConstant_max_at_one`: the badly-approximable constant `1/√(a²+4)`
  of the family is maximal at `a = 1`.
* **Selector 3 — quadratic-Pisot minimality (NEW here).**  Every quadratic Pisot number `γ`
  (real root of `x² − s·x + t` with `s t : ℤ`, `γ > 1`, conjugate `|s − γ| < 1`) satisfies
  `φ ≤ γ`, with equality **iff** `(s, t) = (1, −1)`, i.e. iff `γ` is `φ` itself.

Honest scope (no overclaim): the naive global statement "`φ` is the smallest Pisot number" is
FALSE — the plastic number `ρ ≈ 1.3247` (root of `x³ = x + 1`) is a Pisot number strictly below
`φ`.  The correct global statements are: minimal **quadratic** Pisot number; simplest defining
polynomial among Pisot numbers (degree 2); Hurwitz-extremal worst-approximable irrational.
The certificate `vp_phi_quadpisot_minimality.py` gates exactly this boundary: the naive claim
must FAIL there.  Lean formalization of the plastic witness is queued as follow-up work.

Proof notes.  No transcendence and no `Irrational` machinery is used anywhere: the equality
case `(s, t) = (1, −1)` is derived by an integer-parity argument (`k² = k + 1` has no integer
solution), keeping every step inside elementary ordered-field arithmetic.
-/

namespace D0

/-! ### Basic order facts about `φ` -/

private theorem phi_gt_one : (1 : ℝ) < phi := by
  unfold phi
  have h2 : (2 : ℝ) ^ 2 < (5 : ℝ) := by norm_num
  have hpos : (0 : ℝ) ≤ 2 := by norm_num
  have h : (2 : ℝ) < Real.sqrt 5 := (Real.lt_sqrt hpos).mpr h2
  linarith

private theorem phi_lt_two : phi < (2 : ℝ) := by
  have h9pos : (0 : ℝ) ≤ Real.sqrt 9 := Real.sqrt_nonneg 9
  have h9sq : (Real.sqrt 9 : ℝ) ^ 2 = 9 := by
    rw [sq]
    exact Real.mul_self_sqrt (by norm_num)
  have h9 : (Real.sqrt 9 : ℝ) = 3 := by nlinarith
  unfold phi
  have h5 : (5 : ℝ) < 9 := by norm_num
  have h3 : Real.sqrt 5 < Real.sqrt 9 := Real.sqrt_lt_sqrt (by norm_num) h5
  linarith

/-- For `x > 1`: `x² − x − 1 ≥ 0 ↔ φ ≤ x` — the parabola opens upward and its second root
    `ψ = 1 − φ` lies below every `x > 1`. -/
private theorem phi_le_of_sub_sq_nonneg {x : ℝ} (hx : 1 < x) (h : 0 ≤ x ^ 2 - x - 1) : phi ≤ x := by
  have key : (x - phi) * (x - psi) = x ^ 2 - x * (phi + psi) + phi * psi := by ring
  have hprod : (x - phi) * (x - psi) = x ^ 2 - x - 1 := by
    rw [key, phi_add_psi, phi_mul_psi]
    ring
  have hpsilt1 : psi < (1 : ℝ) := by
    have hs : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
    unfold psi
    linarith
  have hxpsi : (0 : ℝ) < x - psi := by linarith
  rcases le_total 0 (x - phi) with hp | hn
  · linarith
  · rcases lt_or_eq_of_le hn with hlt | heq
    · exfalso
      have hneg : (x - phi) * (x - psi) < 0 := mul_neg_of_neg_of_pos hlt hxpsi
      rw [hprod] at hneg
      linarith
    · linarith

/-- `k² = k + 1` has no integer solution (elementary size argument, no irrationality). -/
private theorem no_int_root_sq_eq_succ (k : ℤ) : k * k ≠ k + 1 := by
  intro hk
  rcases lt_or_ge k 0 with hk0 | hk1
  · have hpos : 1 ≤ k * k := by nlinarith [(by omega : (1 : ℤ) ≤ -k)]
    have hle : k + 1 ≤ 0 := by omega
    omega
  · rcases eq_or_lt_of_le hk1 with hz | hp
    · subst hz
      norm_num at hk
    · rcases lt_or_ge k 2 with h1 | h2
      · have hk1' : k = 1 := by omega
        subst hk1'
        norm_num at hk
      · have hge : 2 * k ≤ k * k := by nlinarith
        have hgt : k + 1 < 2 * k := by omega
        omega

/-! ### The quadratic Pisot class and its minimum -/

/-- Quadratic Pisot condition: `γ > 1` is a real root of `x² − s·x + t` (`s t : ℤ`; monic ⇒
    algebraic integer) whose conjugate `s − γ` lies strictly inside the unit disk.  This is
    precisely "Pisot number of degree ≤ 2"; integers appear as the degenerate case `t = 0`. -/
def QuadPisotCond (s t : ℤ) (γ : ℝ) : Prop :=
  1 < γ ∧ γ ^ 2 - (s : ℝ) * γ + (t : ℝ) = 0 ∧ |(s : ℝ) - γ| < 1

/-- Vieta consequence: `t = γ · (s − γ)`. -/
theorem quad_pisot_vieta {s t : ℤ} {γ : ℝ} (hcond : QuadPisotCond s t γ) :
    (t : ℝ) = γ * ((s : ℝ) - γ) := by
  have h : γ ^ 2 - (s : ℝ) * γ + (t : ℝ) = 0 := hcond.2.1
  linarith

/-- Conjugate bounds extracted from `QuadPisotCond`, kept as standalone hypotheses so they
    survive the destructuring of `hcond`. -/
theorem quad_pisot_bounds {s t : ℤ} {γ : ℝ} (hcond : QuadPisotCond s t γ) :
    (1 : ℝ) < γ ∧ γ ^ 2 - (s : ℝ) * γ + (t : ℝ) = 0
      ∧ (s : ℝ) - 1 < γ ∧ γ < (s : ℝ) + 1 := by
  obtain ⟨hγ1, hpoly, hconj⟩ := hcond
  have hnabs : -(1 : ℝ) < -|(s : ℝ) - γ| := by linarith
  have hlo := neg_abs_le ((s : ℝ) - γ)
  have hself := le_abs_self ((s : ℝ) - γ)
  exact ⟨hγ1, hpoly, by linarith, by linarith⟩

/-- **Quadratic-Pisot minimality.**  Every quadratic Pisot number is `≥ φ`. -/
theorem quad_pisot_phi_le {s t : ℤ} {γ : ℝ} (hcond : QuadPisotCond s t γ) : phi ≤ γ := by
  obtain ⟨hγ1, hpoly, hγlo, hγhi⟩ := quad_pisot_bounds hcond
  have hvieta := quad_pisot_vieta hcond
  rcases eq_or_ne t 0 with ht0 | ht0
  · -- degenerate case t = 0: γ = s is an integer ≥ 2
    have hfac : γ * ((s : ℝ) - γ) = 0 := by rw [← hvieta]; exact_mod_cast ht0
    have hgs : γ = (s : ℝ) := by
      rcases mul_eq_zero.mp hfac with h0 | h0
      · exact absurd h0 (by linarith)
      · linarith
    have hs2 : (2 : ℤ) ≤ s := by
      have hcontra : ¬ (s ≤ 1) := by
        intro hh
        have hsup : (s : ℝ) ≤ 1 := by exact_mod_cast hh
        linarith
      omega
    have hge2 : (2 : ℝ) ≤ γ := by rw [hgs]; exact_mod_cast hs2
    exact le_trans phi_lt_two.le hge2
  · -- genuine quadratic case: |t| ≥ 1
    have htint : 1 ≤ |(t : ℝ)| := by
      have habs : 1 ≤ |(t : ℤ)| := Int.one_le_abs ht0
      have hcast : (((|t| : ℤ) : ℝ)) = |(t : ℝ)| := by push_cast; rfl
      rw [← hcast]
      exact_mod_cast habs
    rcases lt_or_ge s 1 with hs0 | hs1
    · exfalso
      have hsint : (s : ℤ) ≤ 0 := by omega
      have hsup : (s : ℝ) ≤ 0 := by exact_mod_cast hsint
      linarith
    rcases lt_or_ge s 2 with hs1' | hs2
    · -- s = 1: |t| = γ(γ−1) ≥ 1 forces γ² − γ − 1 ≥ 0
      have hsone : (s : ℤ) = 1 := by omega
      have hs'1 : (s : ℝ) = 1 := by exact_mod_cast hsone
      have habsgamma : |(t : ℝ)| = γ * (γ - 1) := by
        have hval : (t : ℝ) = -(γ * (γ - 1)) := by
          rw [hvieta, hs'1]; ring
        rw [hval, abs_neg, abs_of_nonneg (by nlinarith : (0 : ℝ) ≤ γ * (γ - 1))]
      have hge : γ * (γ - 1) ≥ 1 := by rw [← habsgamma]; exact htint
      have hsq : 0 ≤ γ ^ 2 - γ - 1 := by nlinarith
      exact phi_le_of_sub_sq_nonneg hγ1 hsq
    · -- s ≥ 2: if γ < 2 then s = 2 and t = γ(2−γ) ∈ (0,1), not a nonzero integer
      rcases lt_or_ge γ 2 with hlt2 | hge2
      · exfalso
        have hs_ub : (s : ℤ) < 3 := by
          by_contra hc
          push_neg at hc
          have hsup : (3 : ℝ) ≤ (s : ℝ) := by exact_mod_cast hc
          linarith
        have hs_eq_2 : (s : ℤ) = 2 := by omega
        have hs'2 : (s : ℝ) = 2 := by exact_mod_cast hs_eq_2
        have htval : (t : ℝ) = γ * (2 - γ) := by
          rw [hvieta, hs'2]
        have hp1 : (0 : ℝ) < γ * (2 - γ) :=
          mul_pos (by linarith) (by linarith)
        have hp2 : γ * (2 - γ) < 1 := by
          have hnz : (0 : ℝ) < (γ - 1) ^ 2 := by
            apply sq_pos_of_ne_zero
            linarith
          nlinarith [hnz]
        rw [htval, abs_of_pos hp1] at htint
        linarith
      · exact le_trans phi_lt_two.le hge2

/-- `φ` itself is a quadratic Pisot number: root of `x² − x − 1`, conjugate `1 − φ`. -/
theorem phi_quad_pisot : QuadPisotCond 1 (-1 : ℤ) phi := by
  refine ⟨phi_gt_one, ?_, ?_⟩
  · have h := phi_sq
    push_cast
    linarith
  · rw [abs_lt]
    push_cast
    constructor <;> linarith [phi_gt_one, phi_lt_two]

/-- Helper: `φ·(1−φ) = −1`, direct consequence of `φ² = φ + 1`. -/
private theorem phi_mul_one_minus_phi_eq_neg_one : phi * (1 - phi) = -1 := by
  have h := phi_sq
  nlinarith

/-- **Equality case.**  A quadratic Pisot number equals `φ` iff its defining polynomial is
    exactly `x² − x − 1` (i.e. `(s, t) = (1, −1)`). -/
theorem quad_pisot_eq_phi_iff {s t : ℤ} {γ : ℝ} (hcond : QuadPisotCond s t γ) :
    γ = phi ↔ s = 1 ∧ t = -1 := by
  obtain ⟨hγ1, hpoly, hγlo, hγhi⟩ := quad_pisot_bounds hcond
  have hvieta := quad_pisot_vieta hcond
  constructor
  · intro heq
    subst heq
    have hlow : (0 : ℝ) < (s : ℝ) := by
      have h1 : -(1 : ℝ) < -((s : ℝ) - phi) := by linarith
      have h2 := neg_abs_le ((s : ℝ) - phi)
      linarith [phi_gt_one]
    have hhigh : (s : ℝ) < 3 := by
      have h1 := le_abs_self ((s : ℝ) - phi)
      linarith [phi_lt_two]
    have hint1 : (0 : ℤ) < s := by exact_mod_cast hlow
    have hint2 : s < 3 := by exact_mod_cast hhigh
    rcases lt_or_ge s 2 with hlt2 | hge2
    · refine ⟨by omega, ?_⟩
      have hsone : (s : ℤ) = 1 := by omega
      rw [hsone] at hvieta
      push_cast at hvieta
      have htreal : (t : ℝ) = -1 :=
        by linarith [hvieta, phi_mul_one_minus_phi_eq_neg_one]
      exact_mod_cast htreal
    · exfalso
      have hstwo : (s : ℤ) = 2 := by omega
      rw [hstwo] at hvieta
      have hval : phi * (2 - phi) = phi - 1 := by nlinarith [phi_sq]
      have htphi : ((t + 1 : ℤ) : ℝ) = phi := by
        push_cast at hvieta ⊢
        linarith [hvieta, hval]
      have hksq : ((t + 1 : ℤ) : ℝ) ^ 2 = ((t + 1 : ℤ) : ℝ) + 1 := by
        rw [htphi]
        linarith [phi_sq]
      have hexpand : ((t + 1 : ℤ) : ℝ) ^ 2
          = (((t + 1) * (t + 1) : ℤ) : ℝ) := by
        rw [sq]; push_cast; ring
      rw [hexpand] at hksq
      exact no_int_root_sq_eq_succ (t + 1) (mod_cast hksq)
  · rintro ⟨hs, ht⟩
    subst hs
    subst ht
    push_cast at hpoly
    have hdif : (γ - phi) * (γ + phi - 1) = 0 := by
      nlinarith [hpoly, phi_sq]
    have hpos : (0 : ℝ) < γ + phi - 1 := by linarith [hγ1, phi_gt_one]
    rcases mul_eq_zero.mp hdif with h | h
    · linarith
    · exact absurd h (by linarith)

/-! ### The period-one family: every member is quadratic Pisot, and the triple selects `a = 1` -/

/-- Tail bound: for `a ≥ 1` the period-one tail lies strictly below 1. -/
theorem periodOneTail_lt_one (a : ℕ) (ha : 1 ≤ a) : periodOneTail a < 1 := by
  by_contra h
  push_neg at h
  have hpos : (0 : ℝ) ≤ periodOneTail a := le_of_lt (periodOneTail_positive a)
  have hfix := periodOneTail_fixed_point a
  have ha1 : (1 : ℝ) ≤ a := by exact_mod_cast ha
  -- τ² ≥ τ and aτ ≥ a give 1 = τ² + aτ ≥ τ + a ≥ 2, absurd
  have h1 : periodOneTail a ^ 2 ≥ periodOneTail a := by nlinarith
  have h2 : (a : ℝ) * periodOneTail a ≥ (a : ℝ) := by nlinarith
  linarith

/-- The Pisot member of the period-one class at partial quotient `a`: `β_a = a + tail_a`,
    the root `> 1` of `x² − a·x − 1`. -/
noncomputable def betaOne (a : ℕ) : ℝ := (a : ℝ) + periodOneTail a

theorem betaOne_poly (a : ℕ) : betaOne a ^ 2 - (a : ℝ) * betaOne a - 1 = 0 := by
  unfold betaOne
  have hfix := periodOneTail_fixed_point a
  ring_nf
  linarith [hfix]

theorem betaOne_quad_pisot (a : ℕ) (ha : 1 ≤ a) :
    QuadPisotCond (a : ℤ) (-1 : ℤ) (betaOne a) := by
  have htail := periodOneTail_lt_one a ha
  have ha1 : (1 : ℝ) ≤ a := by exact_mod_cast ha
  refine ⟨?_, ?_, ?_⟩
  · unfold betaOne
    linarith [periodOneTail_positive a]
  · have hp := betaOne_poly a
    push_cast at hp ⊢
    linarith
  · unfold betaOne
    rw [abs_lt]
    push_cast
    constructor <;> linarith [periodOneTail_positive a]

theorem betaOne_one_eq_phi : betaOne 1 = phi := by
  unfold betaOne periodOneTail phi
  norm_num
  ring

/-! ### Capstone: the triple selector -/

/-- **D0-PHI-QUADPISOT-MINIMALITY-001 (capstone).**  Composing the three selectors:
    `φ` is a quadratic Pisot number; every quadratic Pisot number is `≥ φ`; the equality case
    is exactly the polynomial `x² − x − 1`; every admissible member `β_a` (`a ≥ 1`) of the
    period-one self-referential class is quadratic Pisot; and `β₁ = φ`.  Together with the
    upstream Hurwitz leg (`periodOneBadApproxConstant_max_at_one`), all three classical
    selectors agree on `a = 1`, i.e. on `φ`. -/
theorem PHI_QUADPISOT_MINIMALITY_PROVED :
    QuadPisotCond 1 (-1 : ℤ) phi ∧
    (∀ (s t : ℤ) (γ : ℝ), QuadPisotCond s t γ → phi ≤ γ) ∧
    (∀ (s t : ℤ) (γ : ℝ), QuadPisotCond s t γ → (γ = phi ↔ s = 1 ∧ t = -1)) ∧
    (∀ a : ℕ, 1 ≤ a → QuadPisotCond (a : ℤ) (-1 : ℤ) (betaOne a)) ∧
    betaOne 1 = phi :=
  ⟨phi_quad_pisot,
   fun s t γ hcond => quad_pisot_phi_le hcond,
   fun s t γ hcond => quad_pisot_eq_phi_iff hcond,
   fun a ha => betaOne_quad_pisot a ha,
   betaOne_one_eq_phi⟩

end D0
