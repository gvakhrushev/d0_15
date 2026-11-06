import D0.Research.NativeWeightedDiracBoundary
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Tactic

/-!
# Finite moment identities for the native weighted-Dirac source

This module formalizes the arbitrary finite-degree binomial identities used
in §3 of `A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md`. Source pin: commit `db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, path `02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md` §3, blob `2de670c0e2f9a53104be8105a3554cdd9aaa85e7`. The contrast theorem below applies the capsule's generic finite-moment annihilator to the source's exact weights and inverse-scale powers. It does not construct the curved fibers or prove their physical source/refinement hypotheses.
-/

namespace D0.Research.NativeWeightedDiracMomentIdentities

open Finset
open scoped BigOperators

noncomputable section

def alternatingPowerSum (n j : ℕ) : ℝ :=
  ∑ r ∈ Finset.range (n + 1),
    ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) * ((r : ℝ) + 1) ^ j

def shiftedAlternatingPowerSum (n j : ℕ) : ℝ :=
  ∑ r ∈ Finset.range (n + 1),
    ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) * ((r : ℝ) + 2) ^ j

theorem alternatingPowerSum_succ (n j : ℕ) :
    alternatingPowerSum (n + 1) j =
      alternatingPowerSum n j - shiftedAlternatingPowerSum n j := by
  unfold alternatingPowerSum shiftedAlternatingPowerSum
  rw [Finset.sum_range_succ, Finset.sum_range_succ']
  simp_rw [Nat.choose_succ_succ', Nat.cast_add]
  simp only [Nat.choose_zero_right, Nat.cast_one, Nat.choose_self]
  rw [Finset.sum_range_succ'
    (fun r => ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) * ((r : ℝ) + 1) ^ j) n]
  rw [Finset.sum_range_succ
    (fun r => ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) * ((r : ℝ) + 2) ^ j) n]
  simp only [Nat.choose_eq_zero_of_lt (Nat.lt_succ_self n), Nat.cast_zero]
  simp [Nat.choose_zero_right, Nat.cast_one, Nat.choose_self, pow_succ]
  simp_rw [mul_add, add_mul]
  rw [Finset.sum_add_distrib]
  ring_nf

theorem shiftedAlternatingPowerSum_expand (n j : ℕ) :
    shiftedAlternatingPowerSum n j =
      ∑ k ∈ Finset.range (j + 1),
        (Nat.choose j k : ℝ) * alternatingPowerSum n k := by
  unfold shiftedAlternatingPowerSum alternatingPowerSum
  have hpow (r : ℕ) :
      ((r : ℝ) + 2) ^ j =
        ∑ k ∈ Finset.range (j + 1),
          ((r : ℝ) + 1) ^ k * (Nat.choose j k : ℝ) := by
    have h : (↑r + 2 : ℝ) = (↑r + 1) + 1 := by ring
    rw [h, add_pow]
    simp
  calc
    _ = ∑ r ∈ Finset.range (n + 1),
          ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) *
            (∑ k ∈ Finset.range (j + 1),
              ((r : ℝ) + 1) ^ k * (Nat.choose j k : ℝ)) := by
          apply Finset.sum_congr rfl
          intro r hr
          rw [hpow]
    _ = ∑ k ∈ Finset.range (j + 1),
          (Nat.choose j k : ℝ) *
            ∑ r ∈ Finset.range (n + 1),
              ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) * ((r : ℝ) + 1) ^ k := by
          simp_rw [Finset.mul_sum]
          rw [Finset.sum_comm]
          apply Finset.sum_congr rfl
          intro k hk
          apply Finset.sum_congr rfl
          intro r hr
          ring
    _ = ∑ k ∈ Finset.range (j + 1),
          (Nat.choose j k : ℝ) * alternatingPowerSum n k := by rfl

theorem alternatingPowerSum_eq_zero {n j : ℕ} (hj : j < n) :
    alternatingPowerSum n j = 0 := by
  induction n generalizing j with
  | zero => omega
  | succ n ih =>
      have hjle : j ≤ n := Nat.le_of_lt_succ hj
      have htail :
          ∑ k ∈ Finset.range j,
            (Nat.choose j k : ℝ) * alternatingPowerSum n k = 0 := by
        apply Finset.sum_eq_zero
        intro k hk
        have hklt : k < n := Nat.lt_of_lt_of_le (Finset.mem_range.mp hk) hjle
        simp [ih (j := k) hklt]
      have hsum :
          ∑ k ∈ Finset.range (j + 1),
            (Nat.choose j k : ℝ) * alternatingPowerSum n k =
              alternatingPowerSum n j := by
        rw [Finset.sum_range_succ, htail]
        simp [Nat.choose_self]
      rw [alternatingPowerSum_succ, shiftedAlternatingPowerSum_expand, hsum]
      ring

def sourceMomentWeightNat (p r : ℕ) : ℝ :=
  ((-1 : ℝ) ^ r) * (Nat.choose (p + 1) r : ℝ)

def sourceMomentWeight (p : ℕ) (r : Fin (p + 2)) : ℝ :=
  sourceMomentWeightNat p r.val

def sourceMomentScale {p : ℕ} (r : Fin (p + 2)) : ℝ :=
  1 / ((r.val : ℝ) + 1)

def sourceMomentInversePower {p : ℕ} (r : Fin (p + 2)) (j : ℕ) : ℝ :=
  (sourceMomentScale r ^ j)⁻¹

theorem sourceMomentScale_inverse_power {p : ℕ} (r : Fin (p + 2)) (j : ℕ) :
    sourceMomentInversePower r j = ((r.val : ℝ) + 1) ^ j := by
  simp [sourceMomentInversePower, sourceMomentScale]

theorem sourceMomentPowerSum_eq_zero (p j : ℕ) (hj : j ≤ p) :
    (∑ r : Fin (p + 2),
      sourceMomentWeight p r * ((r.val : ℝ) + 1) ^ j) = 0 := by
  change
    (∑ r : Fin (p + 2),
      sourceMomentWeightNat p r.val * ((r.val : ℝ) + 1) ^ j) = 0
  rw [Fin.sum_univ_eq_sum_range
    (fun r : ℕ => sourceMomentWeightNat p r * ((r : ℝ) + 1) ^ j) (p + 2)]
  simpa [sourceMomentWeightNat, alternatingPowerSum] using
    alternatingPowerSum_eq_zero (n := p + 1) (j := j) (by omega)

/-- Every fixed finite-degree inverse-scale polynomial is annihilated by the
source's binomial contrast weights, with arbitrary real coefficients. The
proof consumes the capsule's generic coefficient-independent annihilator. -/
theorem fixedDegreeScaleContrast_eq_zero (p : ℕ) (c : Fin (p + 1) → ℝ) :
    (∑ r : Fin (p + 2), sourceMomentWeight p r *
      (∑ j : Fin (p + 1), c j * sourceMomentInversePower r j.val)) = 0 := by
  simp_rw [sourceMomentScale_inverse_power]
  exact D0.Research.NativeWeightedDiracBoundary.finite_moment_annihilator
    (w := sourceMomentWeight p) (c := c)
    (v := fun j r => ((r.val : ℝ) + 1) ^ j.val)
    (by
      intro j
      exact sourceMomentPowerSum_eq_zero p j.val (by omega))

def alternatingReciprocalSum (n : ℕ) : ℝ :=
  ∑ r ∈ Finset.range (n + 1),
    ((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ) / ((r : ℝ) + 1)

theorem alternatingBinomialTail_eq_one (n : ℕ) :
    (∑ r ∈ Finset.range (n + 1),
      ((-1 : ℝ) ^ r) * (Nat.choose (n + 1) (r + 1) : ℝ)) = 1 := by
  have hfullZ := Int.alternating_sum_range_choose_of_ne (n := n + 1) (by omega)
  have hfull :
      (∑ k ∈ Finset.range (n + 2),
        ((-1 : ℝ) ^ k) * (Nat.choose (n + 1) k : ℝ)) = 0 := by
    exact_mod_cast hfullZ
  rw [Finset.sum_range_succ'] at hfull
  simp only [Nat.choose_zero_right, Nat.cast_one, pow_zero, one_mul] at hfull
  have hsign :
      (∑ r ∈ Finset.range (n + 1),
        ((-1 : ℝ) ^ (r + 1)) * (Nat.choose (n + 1) (r + 1) : ℝ)) =
        - (∑ r ∈ Finset.range (n + 1),
          ((-1 : ℝ) ^ r) * (Nat.choose (n + 1) (r + 1) : ℝ)) := by
    calc
      _ = ∑ r ∈ Finset.range (n + 1),
            - (((-1 : ℝ) ^ r) * (Nat.choose (n + 1) (r + 1) : ℝ)) := by
          apply Finset.sum_congr rfl
          intro r hr
          simp_rw [pow_succ]
          ring
      _ = - (∑ r ∈ Finset.range (n + 1),
            ((-1 : ℝ) ^ r) * (Nat.choose (n + 1) (r + 1) : ℝ)) := by
          rw [Finset.sum_neg_distrib]
  rw [hsign] at hfull
  linarith

theorem alternatingReciprocalSum_eq (n : ℕ) :
    alternatingReciprocalSum n = 1 / ((n : ℝ) + 1) := by
  unfold alternatingReciprocalSum
  calc
    _ = (1 / ((n : ℝ) + 1)) *
        ∑ r ∈ Finset.range (n + 1),
          ((-1 : ℝ) ^ r) * (Nat.choose (n + 1) (r + 1) : ℝ) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro r hr
      have hc := Nat.add_one_mul_choose_eq n r
      have hc' : ((n + 1 : ℕ) : ℝ) * (Nat.choose n r : ℝ) =
          (Nat.choose (n + 1) (r + 1) : ℝ) * ((r + 1 : ℕ) : ℝ) := by
        exact_mod_cast hc
      have hn : (n : ℝ) + 1 ≠ 0 := by positivity
      have hrn : (r : ℝ) + 1 ≠ 0 := by positivity
      field_simp [hn, hrn]
      simpa [Nat.cast_add, mul_comm, mul_left_comm, mul_assoc] using hc'
    _ = 1 / ((n : ℝ) + 1) := by
      rw [alternatingBinomialTail_eq_one]
      ring

theorem alternatingBinomialWeight_l1 (n : ℕ) :
    (∑ r ∈ Finset.range (n + 1),
      |((-1 : ℝ) ^ r) * (Nat.choose n r : ℝ)|) = 2 ^ n := by
  calc
    _ = ∑ r ∈ Finset.range (n + 1), (Nat.choose n r : ℝ) := by
      apply Finset.sum_congr rfl
      intro r hr
      rw [abs_mul]
      have hchoose : 0 ≤ (Nat.choose n r : ℝ) := Nat.cast_nonneg _
      rw [abs_of_nonneg hchoose]
      simp [abs_pow]
    _ = (2 : ℝ) ^ n := by exact_mod_cast Nat.sum_range_choose n

theorem sourceMomentScale_weighted_sum (p : ℕ) :
    (∑ r : Fin (p + 2), sourceMomentWeight p r * sourceMomentScale r) =
      1 / ((p + 2 : ℕ) : ℝ) := by
  change
    (∑ r : Fin (p + 2),
      sourceMomentWeightNat p r.val * (1 / ((r.val : ℝ) + 1))) = _
  rw [Fin.sum_univ_eq_sum_range
    (fun r : ℕ => sourceMomentWeightNat p r * (1 / ((r : ℝ) + 1))) (p + 2)]
  have hp : p + 2 = (p + 1) + 1 := by omega
  rw [hp]
  simpa [sourceMomentWeightNat, alternatingReciprocalSum, Nat.cast_add,
    Nat.cast_ofNat, div_eq_mul_inv] using
    alternatingReciprocalSum_eq (p + 1)

theorem sourceMomentWeight_l1 (p : ℕ) :
    (∑ r : Fin (p + 2), |sourceMomentWeight p r|) = 2 ^ (p + 1) := by
  change
    (∑ r : Fin (p + 2), |sourceMomentWeightNat p r.val|) = _
  rw [Fin.sum_univ_eq_sum_range
    (fun r : ℕ => |sourceMomentWeightNat p r|) (p + 2)]
  simpa [sourceMomentWeightNat] using alternatingBinomialWeight_l1 (p + 1)

/-- The explicit smallness threshold for the conditional finite-probe form of
the source's Eq. (3c). `Cbase` bounds the mesh error in the paired base-action
contrast and `Crem` bounds the weighted transfer remainder. -/
def eq3cSmallnessThreshold (p : ℕ) (Cbase Crem : ℝ) : ℝ :=
  min 1
    ((9 * Real.pi ^ 2 / (400 * ((p + 2 : ℕ) : ℝ))) /
      (Cbase / ((p + 2 : ℕ) : ℝ) + Crem + 1))

/-- Conditional Lean application of the finite-probe estimate in source §3,
Eq. (3c). The per-scale model keeps the physical base contrast, every
finite-degree inverse-scale moment, and the paired transfer remainder
separate. The moment identities cancel the polynomial terms exactly; the
owned error inequality then forces at least one experiment's transfer error
to reach the displayed scale. The curved fibers, the base-action estimate,
and the weighted remainder estimate remain explicit caller premises. -/
theorem eq3c_finite_probe_error_bound
    (p : ℕ) (Cbase Crem h ε M d : ℝ)
    (coeff : Fin (p + 1) → ℝ)
    (errors : Fin 2 → Fin (p + 2) → ℝ)
    (remainder : Fin (p + 2) → ℝ)
    (hCbase : 0 ≤ Cbase)
    (hCrem : 0 ≤ Crem)
    (hε : 0 < ε)
    (hεsmall : ε < eq3cSmallnessThreshold p Cbase Crem)
    (hh : h = ε ^ 3)
    (hd : |d + 9 * Real.pi ^ 2 / 200| ≤ Cbase * h)
    (hrem : |∑ r : Fin (p + 2),
      sourceMomentWeight p r * remainder r| ≤ Crem * h)
    (hprofile : ∀ r : Fin (p + 2),
      errors 0 r - errors 1 r =
        ε * d * sourceMomentScale r +
          (∑ j : Fin (p + 1),
            coeff j * sourceMomentInversePower r j.val) + remainder r)
    (hmax : ∀ c : Fin 2, ∀ r : Fin (p + 2), |errors c r| ≤ M) :
    (ε * (9 * Real.pi ^ 2 /
      (400 * ((p + 2 : ℕ) : ℝ)))) / (2 : ℝ) ^ (p + 2) ≤ M := by
  let n : ℝ := ((p + 2 : ℕ) : ℝ)
  let K : ℝ := Cbase / n + Crem
  let target : ℝ := 9 * Real.pi ^ 2 / (400 * n)
  have hn : 0 < n := by
    dsimp [n]
    positivity
  have hK : 0 ≤ K := by
    dsimp [K]
    exact add_nonneg (div_nonneg hCbase (le_of_lt hn)) hCrem
  have hK1 : 0 < K + 1 := by linarith
  have hεsmall' := hεsmall
  rw [eq3cSmallnessThreshold] at hεsmall'
  have hεlt1 : ε < 1 :=
    lt_of_lt_of_le hεsmall' (min_le_left _ _)
  have hεltRatio : ε < target / (K + 1) := by
    simpa [target, K, n] using
      lt_of_lt_of_le hεsmall' (min_le_right _ _)
  have hεsq : ε ^ 2 ≤ target / (K + 1) := by
    have hεsqε : ε ^ 2 ≤ ε := by
      nlinarith [mul_nonneg (le_of_lt hε) (sub_nonneg.mpr (le_of_lt hεlt1))]
    exact le_trans hεsqε (le_of_lt hεltRatio)
  have hKεsq : K * ε ^ 2 ≤ target := by
    have hmul := mul_le_mul_of_nonneg_left hεsq (le_of_lt hK1)
    have hKle : K ≤ K + 1 := by linarith
    calc
      K * ε ^ 2 ≤ (K + 1) * ε ^ 2 :=
        mul_le_mul_of_nonneg_right hKle (sq_nonneg ε)
      _ ≤ (K + 1) * (target / (K + 1)) := hmul
      _ = target := by field_simp [ne_of_gt hK1]
  have hKh : K * h ≤ ε * target := by
    rw [hh]
    calc
      K * ε ^ 3 = ε * (K * ε ^ 2) := by ring
      _ ≤ ε * target := mul_le_mul_of_nonneg_left hKεsq (le_of_lt hε)

  have hscaleWeighted :
      (∑ r : Fin (p + 2),
        sourceMomentWeight p r * sourceMomentScale r) = 1 / n := by
    simpa [n] using sourceMomentScale_weighted_sum p
  have hpolyWeighted :
      (∑ r : Fin (p + 2), sourceMomentWeight p r *
        (∑ j : Fin (p + 1),
          coeff j * sourceMomentInversePower r j.val)) = 0 :=
    fixedDegreeScaleContrast_eq_zero p coeff
  have hbaseWeighted :
      (∑ r : Fin (p + 2),
        sourceMomentWeight p r * (ε * d * sourceMomentScale r)) =
        (ε * d) *
          (∑ r : Fin (p + 2),
            sourceMomentWeight p r * sourceMomentScale r) := by
    calc
      _ = ∑ r : Fin (p + 2),
            (ε * d) *
              (sourceMomentWeight p r * sourceMomentScale r) := by
          apply Finset.sum_congr rfl
          intro r hr
          ring
      _ = _ := by rw [Finset.mul_sum]
  have hcontrast :
      (∑ r : Fin (p + 2), sourceMomentWeight p r *
        (errors 0 r - errors 1 r)) =
        ε * d / n +
          (∑ r : Fin (p + 2),
            sourceMomentWeight p r * remainder r) := by
    calc
      _ = ∑ r : Fin (p + 2), sourceMomentWeight p r *
            (ε * d * sourceMomentScale r +
              (∑ j : Fin (p + 1),
                coeff j * sourceMomentInversePower r j.val) + remainder r) := by
          apply Finset.sum_congr rfl
          intro r hr
          rw [hprofile r]
      _ = (∑ r : Fin (p + 2), sourceMomentWeight p r *
              (ε * d * sourceMomentScale r)) +
            (∑ r : Fin (p + 2), sourceMomentWeight p r *
              (∑ j : Fin (p + 1),
                coeff j * sourceMomentInversePower r j.val)) +
            (∑ r : Fin (p + 2), sourceMomentWeight p r * remainder r) := by
          simp_rw [mul_add]
          rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
      _ = ε * d / n +
            (∑ r : Fin (p + 2),
              sourceMomentWeight p r * remainder r) := by
          rw [hbaseWeighted, hscaleWeighted, hpolyWeighted]
          ring

  let g : ℝ := ε * d / n +
    (∑ r : Fin (p + 2), sourceMomentWeight p r * remainder r)
  have hpairBound : ∀ r : Fin (p + 2),
      |errors 0 r - errors 1 r| ≤ 2 * M := by
    intro r
    calc
      |errors 0 r - errors 1 r| =
          |errors 0 r + -(errors 1 r)| := by rfl
      _ ≤ |errors 0 r| + |-(errors 1 r)| := abs_add_le _ _
      _ = |errors 0 r| + |errors 1 r| := by simp
      _ ≤ M + M := add_le_add (hmax 0 r) (hmax 1 r)
      _ = 2 * M := by ring
  have hUpper : |g| ≤ (2 * M) *
      (∑ r : Fin (p + 2), |sourceMomentWeight p r|) := by
    dsimp [g]
    exact D0.Research.NativeWeightedDiracBoundary.finite_annihilator_error_bound
      (w := sourceMomentWeight p)
      (x := fun r : Fin (p + 2) => errors 0 r - errors 1 r)
      (E := 2 * M)
      (g := ε * d / n +
        (∑ r : Fin (p + 2), sourceMomentWeight p r * remainder r))
      hpairBound hcontrast
  have hUpper' : |g| ≤ (2 * M) * (2 : ℝ) ^ (p + 1) := by
    rw [sourceMomentWeight_l1 p] at hUpper
    exact hUpper

  have hclose :
      |g - ε * (-9 * Real.pi ^ 2 / 200) / n| ≤ K * h := by
    dsimp [g]
    calc
      |(ε * d / n +
          (∑ r : Fin (p + 2),
            sourceMomentWeight p r * remainder r)) -
          ε * (-9 * Real.pi ^ 2 / 200) / n| =
        |ε * (d + 9 * Real.pi ^ 2 / 200) / n +
          (∑ r : Fin (p + 2),
            sourceMomentWeight p r * remainder r)| := by
              congr 1; ring
      _ ≤ |ε * (d + 9 * Real.pi ^ 2 / 200) / n| +
          |∑ r : Fin (p + 2),
            sourceMomentWeight p r * remainder r| := abs_add_le _ _
      _ = ε * |d + 9 * Real.pi ^ 2 / 200| / n +
          |∑ r : Fin (p + 2),
            sourceMomentWeight p r * remainder r| := by
              rw [abs_div, abs_mul, abs_of_pos hε, abs_of_pos hn]
      _ ≤ ε * (Cbase * h) / n + Crem * h := by
          apply add_le_add
          · apply div_le_div_of_nonneg_right _ (le_of_lt hn)
            exact mul_le_mul_of_nonneg_left hd (le_of_lt hε)
          · exact hrem
      _ ≤ (Cbase / n) * h + Crem * h := by
          have hh0 : 0 ≤ h := by rw [hh]; positivity
          have hCbaseh : 0 ≤ Cbase * h := mul_nonneg hCbase hh0
          have hnum : ε * (Cbase * h) ≤ Cbase * h := by
            calc
              ε * (Cbase * h) ≤ 1 * (Cbase * h) :=
                mul_le_mul_of_nonneg_right (le_of_lt hεlt1) hCbaseh
              _ = Cbase * h := by ring
          have hdiv := div_le_div_of_nonneg_right hnum (le_of_lt hn)
          calc
            ε * (Cbase * h) / n + Crem * h ≤
                (Cbase * h) / n + Crem * h := add_le_add hdiv le_rfl
            _ ≤ (Cbase / n) * h + Crem * h :=
              add_le_add (le_of_eq (by ring)) le_rfl
      _ = K * h := by dsimp [K]; ring
  have hclose' :
      |g - ε * (-9 * Real.pi ^ 2 / 200) / n| ≤ ε * target :=
    le_trans hclose hKh
  have hbaseAbs :
      |ε * (-9 * Real.pi ^ 2 / 200) / n| = 2 * (ε * target) := by
    rw [abs_div, abs_mul, abs_of_pos hε, abs_of_pos hn]
    have hconst : 0 < 9 * Real.pi ^ 2 / 200 := by positivity
    have hnegEq : (-9 * Real.pi ^ 2 / 200 : ℝ) =
        -(9 * Real.pi ^ 2 / 200) := by ring
    rw [hnegEq, abs_neg, abs_of_pos hconst]
    dsimp [target]
    field_simp [ne_of_gt hn]
    ring
  have habsSub :
      |ε * (-9 * Real.pi ^ 2 / 200) / n - g| =
        |g - ε * (-9 * Real.pi ^ 2 / 200) / n| := by
    calc
      _ = |-(g - ε * (-9 * Real.pi ^ 2 / 200) / n)| := by
        congr 1; ring
      _ = _ := abs_neg _
  have htriangle :
      |ε * (-9 * Real.pi ^ 2 / 200) / n| ≤
        |g| + |g - ε * (-9 * Real.pi ^ 2 / 200) / n| := by
    calc
      _ = |g + (ε * (-9 * Real.pi ^ 2 / 200) / n - g)| := by
        congr 1; ring
      _ ≤ |g| + |ε * (-9 * Real.pi ^ 2 / 200) / n - g| := abs_add_le _ _
      _ = _ := by rw [habsSub]
  have hmin : ε * target ≤ |g| := by
    rw [hbaseAbs] at htriangle
    linarith [htriangle, hclose']
  have hproduct : ε * target ≤ M * (2 : ℝ) ^ (p + 2) := by
    calc
      ε * target ≤ |g| := hmin
      _ ≤ (2 * M) * (2 : ℝ) ^ (p + 1) := hUpper'
      _ = M * (2 : ℝ) ^ (p + 2) := by
        rw [show p + 2 = (p + 1) + 1 by omega, pow_succ]
        ring
  apply (div_le_iff₀ (by positivity :
    0 < (2 : ℝ) ^ (p + 2))).2
  simpa [target, n] using hproduct

end
end D0.Research.NativeWeightedDiracMomentIdentities
