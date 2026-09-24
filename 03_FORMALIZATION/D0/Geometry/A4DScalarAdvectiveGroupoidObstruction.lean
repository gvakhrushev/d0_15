import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Geometry.A4DScalarDeltaSecondJet
import D0.Geometry.A4DSecondOrderCartanCongruence

/-!
# Scalar advective groupoid obstruction

Inside the explicit output-site-local class

`(g_ξ ψ)_x = ξ_x (D_e ψ)_x`, with flat operator `D_0 = D`,

groupoid composition forces

`[M_ξ, D] = -H₀(Δξ)`, `B_adv(ξ, h) = -M_ξ H₀(h) D`, and
`K_ξ = G_ξ² + B_adv(ξ, h_ξ) = M_{ξ²} D²`.

This `K_ξ` is a particular second jet of that class. It does not replace the
generic `K` of the congruence package and it does not select a universal matter
representation. On the `L = 5` delta witness the induced energy Hessian has the
same-axis entry `(D²W)_{+1,-1} = -25/2`. A direct elementary-cell Hessian cannot
carry that entry when `L ≥ 5`. The comparison jet `𝒮` is not constructed.
-/

namespace D0.Geometry

open Matrix TwoJet
open scoped BigOperators

set_option linter.unusedSimpArgs false

variable {n : ℕ} [NeZero n]

private lemma fin_val_one (hn : 2 ≤ n) : ((1 : Fin n).val) = 1 := by
  have hlt : 1 < n := by omega
  change (1 % n) = 1
  exact Nat.mod_eq_of_lt hlt

private lemma fin_val_neg_one (hn : 1 ≤ n) : ((-1 : Fin n).val) = n - 1 := by
  obtain ⟨k, hk⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
  subst hk
  simp [Fin.coe_neg_one]

private lemma zero_ne_one_public (hn : 2 ≤ n) : (0 : Fin n) ≠ 1 := by
  intro h
  have := congrArg Fin.val h
  rw [fin_val_one hn] at this
  simp at this

private lemma zero_ne_neg_one_public (hn : 2 ≤ n) : (0 : Fin n) ≠ -1 := by
  intro h
  have := congrArg Fin.val h
  rw [fin_val_neg_one (by omega : 1 ≤ n)] at this
  simp at this
  omega

private lemma one_ne_neg_one_far (hn : 5 ≤ n) : (1 : Fin n) ≠ -1 := by
  intro h
  have := congrArg Fin.val h
  rw [fin_val_one (by omega), fin_val_neg_one (by omega : 1 ≤ n)] at this
  omega

private lemma neg_one_ne_succ_one (hn : 5 ≤ n) : (-1 : Fin n) ≠ (1 : Fin n) + 1 := by
  intro h
  have hval := congrArg Fin.val h
  rw [fin_val_neg_one (by omega : 1 ≤ n), Fin.val_add, fin_val_one (by omega)] at hval
  have h2 : 2 < n := by omega
  rw [Nat.mod_eq_of_lt h2] at hval
  omega

theorem scalarCycleD_skew : (scalarCycleD n)ᵀ = -scalarCycleD n := by
  ext i j
  simp [scalarCycleD, Matrix.transpose_smul, Matrix.transpose_sub, Matrix.transpose_transpose,
    Matrix.smul_apply, Matrix.sub_apply, Matrix.neg_apply]
  ring

omit [NeZero n] in
theorem scalarCycleMul_transpose (v : Fin n → ℚ) :
    (scalarCycleMul v)ᵀ = scalarCycleMul v := by
  ext i j
  by_cases h : i = j
  · simp [scalarCycleMul, Matrix.transpose_apply, Matrix.diagonal, h]
  · simp [scalarCycleMul, Matrix.transpose_apply, Matrix.diagonal, h, Ne.symm h]

/-- Output-site locality at the flat operator: `[M_ξ, D] = -H₀(Δξ)`. -/
theorem outputSiteLocal_commutator (hn : 3 ≤ n) (v : Fin n → ℚ) :
    scalarCycleMul v * scalarCycleD n - scalarCycleD n * scalarCycleMul v =
      -scalarCycleH0 (scalarDisplacement v) := by
  have hsym := scalarCycle_firstJet_eq_negative_symmetrized hn v
  have hG : (scalarCycleG v)ᵀ = -(scalarCycleD n * scalarCycleMul v) := by
    calc
      (scalarCycleG v)ᵀ = (scalarCycleD n)ᵀ * (scalarCycleMul v)ᵀ := by
        simp [scalarCycleG, Matrix.transpose_mul]
      _ = (-scalarCycleD n) * scalarCycleMul v := by
        rw [scalarCycleD_skew, scalarCycleMul_transpose]
      _ = -(scalarCycleD n * scalarCycleMul v) := by
        simp [neg_mul]
  have hsum :
      scalarCycleG v + (scalarCycleG v)ᵀ =
        scalarCycleMul v * scalarCycleD n - scalarCycleD n * scalarCycleMul v := by
    calc
      scalarCycleG v + (scalarCycleG v)ᵀ
          = scalarCycleG v + -(scalarCycleD n * scalarCycleMul v) := by rw [hG]
      _ = scalarCycleMul v * scalarCycleD n - scalarCycleD n * scalarCycleMul v := by
          rw [scalarCycleG]
          abel
  rw [← hsum]
  simpa using (congrArg Neg.neg hsym).symm

theorem outputSiteLocal_transport (hn : 3 ≤ n) (v : Fin n → ℚ) :
    scalarCycleD n * scalarCycleMul v =
      scalarCycleMul v * scalarCycleD n + scalarCycleH0 (scalarDisplacement v) := by
  have hcom := outputSiteLocal_commutator hn v
  apply sub_eq_zero.mp
  calc
    scalarCycleD n * scalarCycleMul v -
        (scalarCycleMul v * scalarCycleD n + scalarCycleH0 (scalarDisplacement v))
      = -(scalarCycleMul v * scalarCycleD n - scalarCycleD n * scalarCycleMul v +
          scalarCycleH0 (scalarDisplacement v)) := by abel
    _ = 0 := by rw [hcom]; abel

/-- Particular mixed derivative inside output-site locality. Not a chosen `𝒮`. -/
def advectiveBackgroundDerivative (v h : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  -(scalarCycleMul v * scalarCycleH0 h * scalarCycleD n)

theorem forcedOperatorDerivative (hn : 3 ≤ n) (v : Fin n → ℚ) :
    scalarCycleG v * scalarCycleD n - scalarCycleD n * scalarCycleG v =
      -(scalarCycleH0 (scalarDisplacement v) * scalarCycleD n) := by
  have hcom := outputSiteLocal_commutator hn v
  calc
    scalarCycleG v * scalarCycleD n - scalarCycleD n * scalarCycleG v
        = (scalarCycleMul v * scalarCycleD n) * scalarCycleD n -
            scalarCycleD n * (scalarCycleMul v * scalarCycleD n) := by
          simp [scalarCycleG, scalarCycleMul]
    _ = (scalarCycleMul v * scalarCycleD n - scalarCycleD n * scalarCycleMul v) *
          scalarCycleD n := by
          simp [sub_mul, mul_assoc]
    _ = (-scalarCycleH0 (scalarDisplacement v)) * scalarCycleD n := by rw [hcom]
    _ = -(scalarCycleH0 (scalarDisplacement v) * scalarCycleD n) := by simp [neg_mul]

theorem advectiveBackgroundDerivative_forced (hn : 3 ≤ n) (v : Fin n → ℚ) :
    advectiveBackgroundDerivative v (scalarDisplacement v) =
      scalarCycleMul v *
        (scalarCycleG v * scalarCycleD n - scalarCycleD n * scalarCycleG v) := by
  rw [forcedOperatorDerivative hn v, advectiveBackgroundDerivative]
  simp [mul_neg, neg_mul, mul_assoc]

/-- Derived second jet of the output-site-local class: `K_ξ = G_ξ² + B_adv = M_{ξ²} D²`. -/
def advectiveSecondJet (v : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  scalarCycleG v * scalarCycleG v +
    advectiveBackgroundDerivative v (scalarDisplacement v)

theorem advectiveSecondJet_eq_mulSquare (hn : 3 ≤ n) (v : Fin n → ℚ) :
    advectiveSecondJet v =
      diagonal (fun i => v i * v i) * (scalarCycleD n * scalarCycleD n) := by
  rw [advectiveSecondJet, advectiveBackgroundDerivative_forced hn v]
  have hDM := outputSiteLocal_transport hn v
  calc
    scalarCycleG v * scalarCycleG v +
        scalarCycleMul v * (scalarCycleG v * scalarCycleD n -
          scalarCycleD n * scalarCycleG v)
        = (scalarCycleMul v * scalarCycleD n) * (scalarCycleMul v * scalarCycleD n) +
            scalarCycleMul v * ((scalarCycleMul v * scalarCycleD n) * scalarCycleD n -
              scalarCycleD n * (scalarCycleMul v * scalarCycleD n)) := by
          simp [scalarCycleG, scalarCycleMul]
    _ = scalarCycleMul v * (scalarCycleD n * scalarCycleMul v) * scalarCycleD n +
          (scalarCycleMul v * (scalarCycleMul v * scalarCycleD n) * scalarCycleD n -
            scalarCycleMul v * (scalarCycleD n * scalarCycleMul v) * scalarCycleD n) := by
          simp [mul_sub, mul_assoc]
    _ = scalarCycleMul v * (scalarCycleMul v * scalarCycleD n) * scalarCycleD n := by
          rw [hDM]
          abel
    _ = (scalarCycleMul v * scalarCycleMul v) * (scalarCycleD n * scalarCycleD n) := by
          rw [mul_assoc, mul_assoc, ← mul_assoc]
    _ = diagonal (fun i => v i * v i) * (scalarCycleD n * scalarCycleD n) := by
          unfold scalarCycleMul
          rw [Matrix.diagonal_mul_diagonal]

theorem advective_mixedCocycle (hn : 3 ≤ n) (ξ ζ : Fin n → ℚ) :
    advectiveBackgroundDerivative ζ (scalarDisplacement ξ) -
        advectiveBackgroundDerivative ξ (scalarDisplacement ζ) +
        (scalarCycleG ζ * scalarCycleG ξ - scalarCycleG ξ * scalarCycleG ζ) = 0 := by
  rw [advectiveBackgroundDerivative, advectiveBackgroundDerivative, scalarCycleG, scalarCycleG,
    scalarCycleMul, scalarCycleMul]
  set Mξ := diagonal ξ
  set Mζ := diagonal ζ
  set Hξ := scalarCycleH0 (scalarDisplacement ξ)
  set Hζ := scalarCycleH0 (scalarDisplacement ζ)
  set D := scalarCycleD n
  have hξ : D * Mξ = Mξ * D + Hξ := by
    simpa [Mξ, Hξ, D, scalarCycleMul] using outputSiteLocal_transport hn ξ
  have hζ : D * Mζ = Mζ * D + Hζ := by
    simpa [Mζ, Hζ, D, scalarCycleMul] using outputSiteLocal_transport hn ζ
  have hdiag : Mξ * Mζ = Mζ * Mξ := by
    simp [Mξ, Mζ, Matrix.diagonal_mul_diagonal, mul_comm]
  calc
    -(Mζ * Hξ * D) - -(Mξ * Hζ * D) + ((Mζ * D) * (Mξ * D) - (Mξ * D) * (Mζ * D))
      = -(Mζ * Hξ * D) + (Mξ * Hζ * D) +
          (Mζ * (D * Mξ) * D - Mξ * (D * Mζ) * D) := by
          simp [mul_assoc, sub_eq_add_neg]
    _ = -(Mζ * Hξ * D) + (Mξ * Hζ * D) +
          (Mζ * (Mξ * D + Hξ) * D - Mξ * (Mζ * D + Hζ) * D) := by
          rw [hξ, hζ]
    _ = 0 := by
          have hmove : Mζ * (Mξ * (D * D)) = Mξ * (Mζ * (D * D)) := by
            calc
              Mζ * (Mξ * (D * D)) = (Mζ * Mξ) * (D * D) := by simp [mul_assoc]
              _ = (Mξ * Mζ) * (D * D) := by rw [← hdiag]
              _ = Mξ * (Mζ * (D * D)) := by simp [mul_assoc]
          simp [mul_add, add_mul, mul_assoc, hmove, sub_eq_add_neg]
          abel_nf

/-- Energy Hessian induced by the derived jet through the generic congruence. -/
def advectiveEnergyHessian (v : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  (TwoJet.mk (scalarCycleG v) (advectiveSecondJet v)).secondOrderCongruenceCoefficient

theorem advectiveSecondJet_row_support (hn : 3 ≤ n) (i j : Fin n) (hi : i ≠ 0) :
    advectiveSecondJet (scalarSite (0 : Fin n)) i j = 0 := by
  rw [advectiveSecondJet_eq_mulSquare hn]
  simp [scalarCycleMul, Matrix.mul_apply, Matrix.diagonal, scalarSite, hi]

theorem advectiveEnergyHessian_sameAxis (hn : 3 ≤ n) :
    advectiveEnergyHessian (scalarSite (0 : Fin n)) (1 : Fin n) (-1) =
      -((n : ℚ) ^ 2) / 2 := by
  rw [advectiveEnergyHessian, secondOrderCongruenceCoefficient_formula]
  have hsq := scalarDelta_G_sq hn
  have htsq := scalarDelta_Gt_sq hn
  have hGtG := scalarDelta_GtG_apply hn (1 : Fin n) (-1)
  have hfwd : scalarCycleD n (0 : Fin n) (1 : Fin n) = (n : ℚ) / 2 := by
    simpa using D_forward hn (0 : Fin n)
  have hback : scalarCycleD n (0 : Fin n) (-1) = -((n : ℚ) / 2) := by
    have hstep : (-1 : Fin n) = (0 : Fin n) - 1 := by simp
    rw [hstep]
    exact D_backward hn 0
  have hK1 : advectiveSecondJet (scalarSite (0 : Fin n)) (1 : Fin n) (-1) = 0 :=
    advectiveSecondJet_row_support hn 1 (-1) (zero_ne_one_public (by omega)).symm
  have hKm : advectiveSecondJet (scalarSite (0 : Fin n)) (-1) (1 : Fin n) = 0 :=
    advectiveSecondJet_row_support hn (-1) 1 (zero_ne_neg_one_public (by omega)).symm
  simp only [hsq, htsq, Matrix.smul_apply, Matrix.add_apply, Matrix.sub_apply,
    Matrix.transpose_apply, Matrix.zero_apply, hK1, hKm, hGtG, hfwd, hback]
  ring

/-- A direct elementary cell uses matter values on one adjacent pair. -/
def HasDirectElementaryCellSupport (M : Matrix (Fin n) (Fin n) ℚ) : Prop :=
  ∀ i j, M i j ≠ 0 → i = j ∨ j = i + 1 ∨ i = j + 1

theorem elementaryCell_misses_sameAxis_distanceTwo (hn : 5 ≤ n)
    (M : Matrix (Fin n) (Fin n) ℚ) (hM : HasDirectElementaryCellSupport M) :
    M (1 : Fin n) (-1) = 0 := by
  by_contra hnz
  rcases hM 1 (-1) hnz with hEq | hFwd | hBwd
  · exact one_ne_neg_one_far hn hEq
  · exact neg_one_ne_succ_one hn hFwd
  · have hstep : (-1 : Fin n) + 1 = 0 := by simp
    rw [hstep] at hBwd
    exact (zero_ne_one_public (by omega)).symm hBwd

/-- Scoped no-go: output-site-local transport cannot be a direct elementary-cell energy.
This is not a universal local-matter no-go, not an inverse-free parent no-go, and not a
no-go for a larger patch or for a generator carrying the comparison correction `𝒮`. -/
theorem outputSiteLocal_noDirectElementaryCellInvariantEnergy (hn : 5 ≤ n)
    (M : Matrix (Fin n) (Fin n) ℚ) (hM : HasDirectElementaryCellSupport M)
    (hmatch : M = advectiveEnergyHessian (scalarSite (0 : Fin n))) : False := by
  have hzero := elementaryCell_misses_sameAxis_distanceTwo hn M hM
  have hentry := advectiveEnergyHessian_sameAxis (by omega : 3 ≤ n)
  rw [hmatch, hentry] at hzero
  have hn0 : (n : ℚ) ≠ 0 := by exact_mod_cast (by omega : n ≠ 0)
  have hne : -((n : ℚ) ^ 2) / 2 ≠ 0 :=
    div_ne_zero (neg_ne_zero.mpr (pow_ne_zero 2 hn0)) (by norm_num)
  exact hne hzero

/-- Any other flat mixed cocycle differs from `B_adv` by a term symmetric in the two
translations. No canonical comparison jet `𝒮` is chosen; its overlap law belongs to
`EXP-A4D-ENDPOINT-COMPARISON-JET-OVERLAP-LAW`. -/
theorem flatComparison_difference_symmetric
    (B Badv : (Fin n → ℚ) → (Fin n → ℚ) → Matrix (Fin n) (Fin n) ℚ)
    (ξ ζ : Fin n → ℚ)
    (hB : B ζ (scalarDisplacement ξ) - B ξ (scalarDisplacement ζ) +
        (scalarCycleG ζ * scalarCycleG ξ - scalarCycleG ξ * scalarCycleG ζ) = 0)
    (hA : Badv ζ (scalarDisplacement ξ) - Badv ξ (scalarDisplacement ζ) +
        (scalarCycleG ζ * scalarCycleG ξ - scalarCycleG ξ * scalarCycleG ζ) = 0) :
    B ζ (scalarDisplacement ξ) - Badv ζ (scalarDisplacement ξ) =
      B ξ (scalarDisplacement ζ) - Badv ξ (scalarDisplacement ζ) := by
  let comm := scalarCycleG ζ * scalarCycleG ξ - scalarCycleG ξ * scalarCycleG ζ
  have hBdiff : B ζ (scalarDisplacement ξ) - B ξ (scalarDisplacement ζ) = -comm :=
    (add_eq_zero_iff_eq_neg.mp hB)
  have hAdiff : Badv ζ (scalarDisplacement ξ) - Badv ξ (scalarDisplacement ζ) = -comm :=
    (add_eq_zero_iff_eq_neg.mp hA)
  have heq :
      B ζ (scalarDisplacement ξ) - B ξ (scalarDisplacement ζ) =
        Badv ζ (scalarDisplacement ξ) - Badv ξ (scalarDisplacement ζ) := by
    rw [hBdiff, hAdiff]
  apply sub_eq_zero.mp
  have hrearr :
      (B ζ (scalarDisplacement ξ) - Badv ζ (scalarDisplacement ξ)) -
          (B ξ (scalarDisplacement ζ) - Badv ξ (scalarDisplacement ζ)) =
        (B ζ (scalarDisplacement ξ) - B ξ (scalarDisplacement ζ)) -
          (Badv ζ (scalarDisplacement ξ) - Badv ξ (scalarDisplacement ζ)) := by
    abel
  rw [hrearr, heq, sub_self]

theorem advective_is_particular_cocycle (hn : 3 ≤ n) (ξ ζ : Fin n → ℚ) :
    advectiveBackgroundDerivative ζ (scalarDisplacement ξ) -
        advectiveBackgroundDerivative ξ (scalarDisplacement ζ) +
        (scalarCycleG ζ * scalarCycleG ξ - scalarCycleG ξ * scalarCycleG ζ) = 0 :=
  advective_mixedCocycle hn ξ ζ

/-- `L = 5` delta jet, in cyclic order `(0,+1,+2,-2,-1)`. -/
theorem advectiveDelta_K_L5 :
    advectiveSecondJet (scalarSite (0 : Fin 5)) =
      !![(-25 / 2), 0, (25 / 4), (25 / 4), 0;
         0, 0, 0, 0, 0;
         0, 0, 0, 0, 0;
         0, 0, 0, 0, 0;
         0, 0, 0, 0, 0] := by
  native_decide

/-- Induced `L = 5` energy Hessian. The same-axis entry `(+1,-1)` is `-25/2`. -/
theorem advectiveDelta_hessian_L5 :
    advectiveEnergyHessian (scalarSite (0 : Fin 5)) =
      !![25, 0, (-25 / 4), (-25 / 4), 0;
         0, (25 / 2), 0, 0, (-25 / 2);
         (-25 / 4), 0, 0, 0, 0;
         (-25 / 4), 0, 0, 0, 0;
         0, (-25 / 2), 0, 0, (25 / 2)] := by
  native_decide

theorem advectiveDelta_hessian_distanceTwo_L5 :
    advectiveEnergyHessian (scalarSite (0 : Fin 5)) (1 : Fin 5) (-1) = -25 / 2 := by
  simpa using advectiveEnergyHessian_sameAxis (n := 5) (by decide)

/-- Nondelta control `ξ = δ₀ + 2δ₁` at `L = 5`: `G² ≠ 0`, so delta nilpotence does not extend. -/
theorem nondelta_L5_square_ne_zero :
    (scalarCycleG (scalarNondelta : Fin 5 → ℚ) *
        scalarCycleG (scalarNondelta : Fin 5 → ℚ)) ≠ 0 :=
  nondelta_G_sq_ne_zero (n := 5) (by decide)

theorem nondelta_advective_K_L5 :
    advectiveSecondJet (scalarNondelta : Fin 5 → ℚ) =
      !![(-25 / 2), 0, (25 / 4), (25 / 4), 0;
         0, (-50), 0, 25, 25;
         0, 0, 0, 0, 0;
         0, 0, 0, 0, 0;
         0, 0, 0, 0, 0] := by
  native_decide

end D0.Geometry
