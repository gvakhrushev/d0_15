import D0.Foundation.PopperianBootstrap
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.A4DSymRoleCentralDifference
import D0.Gravity.A1RieszMismatch
import Mathlib.Tactic

/-!
# M1 verification does not select the Riesz block weights

`VerificationContract` forces two registered lines to return the same
comparison of records.  That contract does not mention the scene edge carrier
or the three block weights of `R`.

The owned algebraic fact remains `positive_weight_mismatch_zero_iff`: for
positive block weights, the bare mismatch vanishes on `KPlus` if and only if
the three weights are equal.  A correct verification contract coexists with a
nonuniform positive weight whose mismatch does not vanish.

A radius-one link average `α I + β U_r⁻¹` reproduces the owned centered
difference on the length-3 carrier if and only if `α = β = 1/2`.  That
classification uses the owned forward/centered intertwining.  It is not a
consequence of `VerificationContract`.
-/

namespace D0.Foundation.M1RieszRepresentationGap

open D0.Foundation.PopperianBootstrap
open D0.Foundation.VerifiabilityNecessity
open D0.Geometry
open D0.Gravity.A1RieszMismatch

/-- The Boolean two-line protocol is a verification contract, and a nonuniform
positive block weight still has nonzero bare mismatch. -/
theorem verification_contract_coexists_with_nonuniform_mismatch :
    VerificationContract boolProtocol ∧
      0 < (1 : ℚ) ∧ 0 < (2 : ℚ) ∧ 0 < (3 : ℚ) ∧
      ¬ ((1 : ℚ) = 2 ∧ (2 : ℚ) = 3) ∧
      ¬ (∀ X : KPlus, mismatchOnK (1 : ℚ)⁻¹ 2⁻¹ 3⁻¹ X = 0) := by
  refine ⟨boolProtocol_killingTest.toContract, by norm_num, by norm_num, by norm_num, ?_, ?_⟩
  · intro h
    exact (by norm_num : (1 : ℚ) ≠ 2) h.1
  · intro h
    have hunif := (positive_weight_mismatch_zero_iff (1 : ℚ) 2 3
      (by norm_num) (by norm_num) (by norm_num)).mp h
    exact (by norm_num : (1 : ℚ) ≠ 2) hunif.1

/-- Pairwise block equalities are strictly weaker than uniformity, so a
readout pair that equates only two blocks has a different zero locus. -/
theorem pairwise_weight_locus_is_not_uniform :
    ((1 : ℚ) = 1 ∧ ¬ (1 : ℚ) = 2) ∧
      ¬ ((1 : ℚ) = 1 ∧ (1 : ℚ) = 2) := by
  constructor
  · exact ⟨rfl, by norm_num⟩
  · intro h
    exact (by norm_num : (1 : ℚ) ≠ 2) h.2

/-- Missing representation premise.  A weld would have to send the two
registered lines of a `VerificationProtocol` to two scene readouts, preserve
line exchange, and prove that readout equality is uniform positive block
weight.  `VerificationContract` supplies none of those fields. -/
structure M1RieszRepresentationPremise (P : VerificationProtocol) where
  readout₁ : P.Line → EdgeCochain →ₗ[ℚ] VertexCochain
  readout₂ : P.Line → EdgeCochain →ₗ[ℚ] VertexCochain
  lines_exchange : ∀ l l', l ≠ l' → readout₁ l ≠ readout₂ l'
  equality_iff_uniform :
    ∀ (x y z : ℚ), 0 < x → 0 < y → 0 < z →
      (∀ l, readout₁ l = readout₂ l) ↔ x = y ∧ y = z

theorem boolProtocol_has_no_supplied_riesz_representation :
    VerificationContract boolProtocol ∧
      ¬ (∀ X : KPlus, mismatchOnK (1 : ℚ)⁻¹ 2⁻¹ 3⁻¹ X = 0) :=
  ⟨verification_contract_coexists_with_nonuniform_mismatch.1,
   verification_contract_coexists_with_nonuniform_mismatch.2.2.2.2.2⟩

/-! ## Radius-one averages and the owned centered difference -/

/-- Radius-one combination of the identity and the backward role translation. -/
def radiusOneAverage (α β : ℝ) (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  fun x => α * f x + β * f (roleTranslateMinus N r x)

theorem radiusOneAverage_half_eq_backwardAverage (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    radiusOneAverage (1 / 2) (1 / 2) N r f = backwardAverage N r f := by
  funext x
  simp [radiusOneAverage, backwardAverage]
  ring

theorem half_radius_reproduces_centered (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    radiusOneAverage (1 / 2) (1 / 2) N r (forwardDifference N r f) =
      centeredDifference N r f := by
  rw [radiusOneAverage_half_eq_backwardAverage]
  exact (centeredDifference_eq_average_forward N r f).symm

/-- Equality with the owned backward average forces both radius-one
coefficients to be one half.  Constant functions do not see `α` and `β`
separately; the two indicator probes below do. -/
theorem radius_one_eq_backward_forces_half (α β : ℝ)
    (h : ∀ (r : Role) (f : ArchiveRolePhaseGroup 1 → ℝ) (x : ArchiveRolePhaseGroup 1),
      radiusOneAverage α β 1 r f x = backwardAverage 1 r f x) :
    α = 1 / 2 ∧ β = 1 / 2 := by
  let r : Role := D0.A
  let z0 : ArchiveRolePhaseGroup 1 := 0
  have hshift : roleTranslateMinus 1 r z0 ≠ z0 := by
    intro heq
    have hr := congrFun heq r
    simp [roleTranslateMinus, roleTranslate, roleStep, r, z0, sub_eq_add_neg] at hr
    exact absurd hr (by decide : (1 : ZMod 3) ≠ 0)
  let f0 : ArchiveRolePhaseGroup 1 → ℝ := fun x => if x = z0 then 1 else 0
  have hα := h r f0 z0
  have hf0z : f0 z0 = 1 := by simp [f0]
  have hf0m : f0 (roleTranslateMinus 1 r z0) = 0 := by
    simp [f0, hshift]
  simp [radiusOneAverage, backwardAverage, hf0z, hf0m] at hα
  let fm : ArchiveRolePhaseGroup 1 → ℝ := fun x =>
    if x = roleTranslateMinus 1 r z0 then 1 else 0
  have hβ := h r fm z0
  have hfmz : fm z0 = 0 := by
    simp [fm, z0, hshift.symm]
  have hfmm : fm (roleTranslateMinus 1 r z0) = 1 := by simp [fm]
  simp [radiusOneAverage, backwardAverage, hfmz, hfmm] at hβ
  constructor
  · linarith
  · linarith

theorem forward_only_average_not_backward :
    ¬ (∀ (r : Role) (f : ArchiveRolePhaseGroup 1 → ℝ) (x),
        radiusOneAverage 1 0 1 r f x = backwardAverage 1 r f x) := by
  intro h
  have hc := radius_one_eq_backward_forces_half 1 0 h
  exact (by norm_num : (1 : ℝ) ≠ 1 / 2) hc.1

/-- Constant functions do not select the coefficients: both sides vanish. -/
theorem constants_do_not_select_average (α β : ℝ) (N : ℕ) (r : Role) (c : ℝ) :
    radiusOneAverage α β N r (forwardDifference N r (fun _ => c)) =
      centeredDifference N r (fun _ => c) := by
  rw [forwardDifference_const, centeredDifference_const]
  funext x
  simp [radiusOneAverage]

end D0.Foundation.M1RieszRepresentationGap
