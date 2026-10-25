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

end
end D0.Research.NativeWeightedDiracMomentIdentities
