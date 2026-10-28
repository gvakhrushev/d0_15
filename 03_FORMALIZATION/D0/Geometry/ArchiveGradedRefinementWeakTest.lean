import D0.Geometry.ArchiveGradedRefinementComposedReadout
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Sinc

/-!
# A fixed smooth test for the composed frozen refinement

This is the sine-testing part of section 5 of the existing #310 source
`A4D_NATIVE_COCHAIN_REFINEMENT.md`, blob `c216f19daebc9a6b2a9e732d277350dd2d69f88c`.
It uses the literal adjacent pullbacks on the existing four-role carrier and
normalizes by the actual number of fine sites. It does not select a physical
readout, refinement, action, or field preparation.
-/

namespace D0.Geometry

open D0 Filter
open scoped BigOperators Topology
noncomputable section

/-- Fixed smooth test sampled on the actual fine four-role site carrier. -/
def archiveFixedSineTest (N : ℕ) (r : Role) (y : ArchiveRolePhaseGroup N) : ℝ :=
  Real.sin (2 * Real.pi * (((finZModEquiv N).symm (y r)).val : ℝ) /
    (archiveFibers N : ℝ))

/-- The normalized counting pairing, with no physical readout assumption. -/
def archiveSineWeakPairing (N : ℕ) (ψ : ArchiveCochain N) (r : Role) : ℝ :=
  (∑ y : ArchiveRolePhaseGroup N,
    archiveSingletonComponentError N ψ r y * archiveFixedSineTest N r y) /
    (Fintype.card (ArchiveRolePhaseGroup N) : ℝ)

/-- The exact contribution at every site of the same composed native map. -/
theorem archive_doubling_sine_term (N : ℕ) (r : Role)
    (y : ArchiveRolePhaseGroup (N + (N + 2))) :
    archiveSingletonComponentError (N + (N + 2))
        (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r y *
      archiveFixedSineTest (N + (N + 2)) r y =
    (if ((finZModEquiv (N + (N + 2))).symm (y r)).val < N + 2 then 1 else -1) *
      archiveFixedSineTest (N + (N + 2)) r y := by
  unfold archiveSingletonComponentError
  rw [archive_doubling_singleton_component]
  split_ifs <;> norm_num

/-- Summing a one-coordinate observable over all four roles counts the
other three coordinates, without changing the sampling convention. -/
theorem archive_sum_one_coordinate (N : ℕ) (r : Role)
    (f : ZMod (archiveFibers N) → ℝ) :
    (∑ y : ArchiveRolePhaseGroup N, f (y r)) =
      (∑ a : ZMod (archiveFibers N), f a) * (archiveFibers N : ℝ) ^ 3 := by
  classical
  let g : Role → ZMod (archiveFibers N) → ℝ := fun s a => if s = r then f a else 1
  calc
    _ = ∑ y : ArchiveRolePhaseGroup N, ∏ s : Role, g s (y s) := by
      apply Finset.sum_congr rfl
      intro y hy
      symm
      rw [Finset.prod_eq_single r]
      · simp [g]
      · intro s hs hsr
        simp [g, hsr]
      · simp
    _ = ∏ s : Role, ∑ a : ZMod (archiveFibers N), g s a := by
      simpa only [Fintype.piFinset_univ] using
        (Finset.sum_prod_piFinset (s := Finset.univ) g)
    _ = _ := by
      rw [Finset.prod_eq_mul_prod_diff_singleton_of_mem (Finset.mem_univ r)]
      have hp : (∏ s ∈ (Finset.univ : Finset Role) \ {r},
          ∑ a : ZMod (archiveFibers N), g s a) = (archiveFibers N : ℝ) ^ 3 := by
        calc
          _ = ∏ _s ∈ (Finset.univ : Finset Role) \ {r}, (archiveFibers N : ℝ) := by
            apply Finset.prod_congr rfl
            intro s hs
            have hsr : s ≠ r := by simpa using (Finset.mem_sdiff.mp hs).2
            simp [g, hsr, ZMod.card]
          _ = _ := by simp [Finset.prod_const, Finset.card_sdiff]
      rw [hp]
      simp [g]

/-- The normalized four-role mean is the one-dimensional coordinate mean. -/
theorem archive_average_one_coordinate (N : ℕ) (r : Role)
    (f : ZMod (archiveFibers N) → ℝ) :
    (∑ y : ArchiveRolePhaseGroup N, f (y r)) /
        (Fintype.card (ArchiveRolePhaseGroup N) : ℝ) =
      (∑ a : ZMod (archiveFibers N), f a) / (archiveFibers N : ℝ) := by
  rw [archive_sum_one_coordinate, card_archive_role_phase_group]
  have hn : (archiveFibers N : ℝ) ≠ 0 := by simp [archiveFibers]; positivity
  simp only [archiveModes, Nat.cast_pow]
  field_simp

/-- On the doubled grid the second half of the sine changes sign, exactly
matching the sign change of the transported-minus-sampled error. -/
theorem archive_signed_sine_sum (n : ℕ) (hn : 0 < n) :
    (∑ k ∈ Finset.range (n + n),
      (if k < n then (1 : ℝ) else -1) * Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) =
        2 * (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) := by
  have hnne : (n : ℝ) ≠ 0 := by positivity
  have htail (k : ℕ) : Real.sin (Real.pi * ((n + k : ℕ) : ℝ) / (n : ℝ)) =
      -Real.sin (Real.pi * (k : ℝ) / (n : ℝ)) := by
    have hangle : Real.pi * ((n + k : ℕ) : ℝ) / (n : ℝ) =
        Real.pi * (k : ℝ) / (n : ℝ) + Real.pi := by
      push_cast
      field_simp; ring
    rw [hangle, Real.sin_add_pi]
  rw [Finset.sum_range_add]
  have hfirst : (∑ k ∈ Finset.range n,
      (if k < n then (1 : ℝ) else -1) * Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) =
      ∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ)) := by
    apply Finset.sum_congr rfl
    intro k hk
    simp [Finset.mem_range.mp hk]
  have hsecond : (∑ k ∈ Finset.range n,
      (if n + k < n then (1 : ℝ) else -1) *
        Real.sin (Real.pi * ((n + k : ℕ) : ℝ) / (n : ℝ))) =
      ∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ)) := by
    apply Finset.sum_congr rfl
    intro k hk
    rw [htail k]
    simp
  rw [hfirst, hsecond]
  ring

/-- Finite sine summation follows from the cosine difference identity. -/
theorem sine_arithmetic_telescope (n : ℕ) (θ : ℝ) :
    (2 * Real.sin θ) * (∑ k ∈ Finset.range n, Real.sin (2 * (k : ℝ) * θ)) =
      Real.cos θ - Real.cos ((2 * (n : ℝ) - 1) * θ) := by
  rw [Finset.mul_sum]
  have hterm (k : ℕ) :
      (2 * Real.sin θ) * Real.sin (2 * (k : ℝ) * θ) =
        Real.cos ((2 * (k : ℝ) - 1) * θ) -
          Real.cos ((2 * ((k + 1 : ℕ) : ℝ) - 1) * θ) := by
    have h := Real.cos_sub_cos ((2 * (k : ℝ) - 1) * θ)
      ((2 * ((k + 1 : ℕ) : ℝ) - 1) * θ)
    have hsum : (((2 * (k : ℝ) - 1) * θ) +
        ((2 * ((k + 1 : ℕ) : ℝ) - 1) * θ)) / 2 = 2 * (k : ℝ) * θ := by
      push_cast; ring
    have hdiff : (((2 * (k : ℝ) - 1) * θ) -
        ((2 * ((k + 1 : ℕ) : ℝ) - 1) * θ)) / 2 = -θ := by
      push_cast; ring
    rw [hsum, hdiff, Real.sin_neg] at h
    nlinarith
  simp_rw [hterm]
  have htel := Finset.sum_range_sub (fun k : ℕ => Real.cos ((2 * (k : ℝ) - 1) * θ)) n
  simp only [Finset.sum_sub_distrib] at htel ⊢
  simp only [Nat.cast_zero, mul_zero, zero_sub, neg_mul, one_mul, Real.cos_neg] at htel
  linarith

/-- The exact finite mean of the sine on the original half of the doubled grid. -/
theorem archive_half_sine_mean (n : ℕ) (hn : 0 < n) :
    (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) / (n : ℝ) =
      (2 / Real.pi) * Real.cos (Real.pi / (2 * (n : ℝ))) /
        Real.sinc (Real.pi / (2 * (n : ℝ))) := by
  have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hnne : (n : ℝ) ≠ 0 := by positivity
  let θ : ℝ := Real.pi / (2 * (n : ℝ))
  have hθ : 0 < θ := by dsimp [θ]; positivity
  have hθlt : θ < Real.pi := by
    dsimp [θ]
    exact div_lt_self Real.pi_pos (by linarith)
  have hsin : Real.sin θ ≠ 0 := (Real.sin_pos_of_pos_of_lt_pi hθ hθlt).ne'
  have hsum := sine_arithmetic_telescope n θ
  have hang (k : ℕ) : 2 * (k : ℝ) * θ = Real.pi * (k : ℝ) / (n : ℝ) := by
    dsimp [θ]
    field_simp
  have hlast : (2 * (n : ℝ) - 1) * θ = Real.pi - θ := by
    dsimp [θ]
    field_simp
  simp_rw [hang] at hsum
  rw [hlast, Real.cos_pi_sub] at hsum
  have hsum' : Real.sin θ *
      (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) = Real.cos θ := by
    nlinarith [hsum]
  have hdivsum : (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) =
      Real.cos θ / Real.sin θ := by
    apply (eq_div_iff hsin).2
    nlinarith [hsum']
  change (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) / (n : ℝ) =
    (2 / Real.pi) * Real.cos θ / Real.sinc θ
  rw [hdivsum]
  rw [Real.sinc_of_ne_zero (ne_of_gt hθ)]
  dsimp [θ] at hsin ⊢
  field_simp [hsin, hnne, Real.pi_ne_zero]

/-- The one-dimensional sampled half-sine averages tend to `2/π`. -/
theorem archive_half_sine_mean_tendsto :
    Tendsto (fun N : ℕ =>
      (∑ k ∈ Finset.range (N + 2),
        Real.sin (Real.pi * (k : ℝ) / ((N + 2 : ℕ) : ℝ))) /
        ((N + 2 : ℕ) : ℝ)) atTop (𝓝 (2 / Real.pi)) := by
  have hinv : Tendsto (fun N : ℕ => (((N + 2 : ℕ) : ℝ))⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_nhds_zero_nat.comp (tendsto_add_atTop_nat 2)
  have hangle : Tendsto (fun N : ℕ => Real.pi / (2 * ((N + 2 : ℕ) : ℝ)))
      atTop (𝓝 0) := by
    have h := (tendsto_const_nhds (x := Real.pi / 2)).mul hinv
    convert h using 1 <;> simp [div_eq_mul_inv, mul_inv_rev, mul_assoc, mul_comm]
  have hcos := Real.continuous_cos.continuousAt.tendsto.comp hangle
  have hsinc := Real.continuous_sinc.continuousAt.tendsto.comp hangle
  have hlimit := ((tendsto_const_nhds (x := 2 / Real.pi)).mul hcos).div hsinc (by simp)
  have heq : (fun N : ℕ =>
      (∑ k ∈ Finset.range (N + 2),
        Real.sin (Real.pi * (k : ℝ) / ((N + 2 : ℕ) : ℝ))) /
        ((N + 2 : ℕ) : ℝ)) =ᶠ[atTop]
      (fun N : ℕ => (2 / Real.pi) *
        Real.cos (Real.pi / (2 * ((N + 2 : ℕ) : ℝ))) /
        Real.sinc (Real.pi / (2 * ((N + 2 : ℕ) : ℝ)))) :=
    Filter.Eventually.of_forall (fun N => archive_half_sine_mean (N + 2) (by omega))
  apply Tendsto.congr' heq.symm
  simpa using hlimit

/-- The actual four-role weak pairing reduces to the half-sine mean. -/
theorem archive_doubling_weak_pairing_eq_half_sine (N : ℕ) (r : Role) :
    archiveSineWeakPairing (N + (N + 2))
        (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r =
      (∑ k ∈ Finset.range (N + 2),
        Real.sin (Real.pi * (k : ℝ) / ((N + 2 : ℕ) : ℝ))) /
        ((N + 2 : ℕ) : ℝ) := by
  classical
  let M : ℕ := N + (N + 2)
  let n : ℕ := N + 2
  have hn : 0 < n := by dsimp [n]; omega
  have hnne : (n : ℝ) ≠ 0 := by positivity
  have hsize : archiveFibers M = n + n := by dsimp [M, n, archiveFibers]; omega
  let f : ZMod (archiveFibers M) → ℝ := fun a =>
    (if ((finZModEquiv M).symm a).val < n then (1 : ℝ) else -1) *
      Real.sin (2 * Real.pi * (((finZModEquiv M).symm a).val : ℝ) /
        (archiveFibers M : ℝ))
  have hpair : archiveSineWeakPairing M
      (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r =
        (∑ a : ZMod (archiveFibers M), f a) / (archiveFibers M : ℝ) := by
    unfold archiveSineWeakPairing
    calc
      _ = (∑ y : ArchiveRolePhaseGroup M, f (y r)) /
          (Fintype.card (ArchiveRolePhaseGroup M) : ℝ) := by
        congr 1
        apply Finset.sum_congr rfl
        intro y hy
        exact archive_doubling_sine_term N r y
      _ = _ := archive_average_one_coordinate M r f
  have hequiv : (∑ a : ZMod (archiveFibers M), f a) =
      ∑ i : Fin (archiveFibers M),
        (if i.val < n then (1 : ℝ) else -1) *
          Real.sin (2 * Real.pi * (i.val : ℝ) / (archiveFibers M : ℝ)) := by
    symm
    apply Fintype.sum_equiv (finZModEquiv M)
    intro i
    simp [f]
  have hangle (k : ℕ) : 2 * Real.pi * (k : ℝ) / ((n + n : ℕ) : ℝ) =
      Real.pi * (k : ℝ) / (n : ℝ) := by
    push_cast
    field_simp; ring
  have hfin : (∑ i : Fin (n + n), (fun k : ℕ =>
      (if k < n then (1 : ℝ) else -1) *
        Real.sin (2 * Real.pi * (k : ℝ) / ((n + n : ℕ) : ℝ))) i.val) =
      2 * (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) := by
    rw [Finset.sum_fin_eq_sum_range]
    simp_rw [hangle]
    calc
      _ = ∑ k ∈ Finset.range (n + n),
          (if k < n then (1 : ℝ) else -1) * Real.sin (Real.pi * (k : ℝ) / (n : ℝ)) := by
        apply Finset.sum_congr rfl
        intro k hk
        simp [Finset.mem_range.mp hk]
      _ = _ := archive_signed_sine_sum n hn
  rw [hpair, hequiv, hsize]
  change (∑ i : Fin (n + n), (fun k : ℕ =>
      (if k < n then (1 : ℝ) else -1) *
        Real.sin (2 * Real.pi * (k : ℝ) / ((n + n : ℕ) : ℝ))) i.val) /
      ((n + n : ℕ) : ℝ) =
    (∑ k ∈ Finset.range n, Real.sin (Real.pi * (k : ℝ) / (n : ℝ))) / (n : ℝ)
  rw [hfin]
  push_cast
  field_simp; ring

/-- One fixed smooth sine test detects a nonzero limit for the actual
composed adjacent pullbacks on the existing four-role finite carrier. -/
theorem archive_doubling_sine_weak_pairing_tendsto (r : Role) :
    Tendsto (fun N : ℕ => archiveSineWeakPairing (N + (N + 2))
      (archiveRepeatedGradedPullback N (archiveUnitSingletonCochain N r) (N + 2)) r)
      atTop (𝓝 (2 / Real.pi)) := by
  simpa only [archive_doubling_weak_pairing_eq_half_sine] using
    archive_half_sine_mean_tendsto

theorem archive_doubling_sine_weak_limit_ne_zero : (2 : ℝ) / Real.pi ≠ 0 := by
  exact div_ne_zero (by norm_num) Real.pi_ne_zero

end
end D0.Geometry
