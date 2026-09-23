import D0.Core.FiniteTypes
import D0.Foundation.PopperianBootstrap
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.A4DSymRoleCentralDifference
import D0.Gravity.A1RieszMismatch
import Mathlib.Logic.Equiv.Fin.Basic
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

/-! ## Typed zones and scene ordinals

`D0.V9` is `Omega8 ⊕ Witness`.  The scene zone used by the Riesz carrier is
`Fin 9`.  Equal cardinality does not identify them.  The same split holds for
the 11- and 13-zones.
-/

abbrev Scene9 := D0.Gravity.A1RieszMismatch.V9
abbrev Scene11 := D0.Gravity.A1RieszMismatch.V11
abbrev Scene13 := D0.Gravity.A1RieszMismatch.V13

def typedWitness9 : D0.V9 := Sum.inr PUnit.unit

/-- Base-2 enumeration of `Omega8`, with the unique witness sent to `8`. -/
def typedZone9Index : D0.V9 → Scene9
  | Sum.inl (((a, b), o)) =>
      Fin.mk (a.val + 2 * b.val + 4 * (if o then 1 else 0)) (by
        fin_cases a <;> fin_cases b <;> cases o <;> decide)
  | Sum.inr _ => 8

def scene9Preimage : Scene9 → D0.V9
  | 0 => Sum.inl (((0, 0), false))
  | 1 => Sum.inl (((1, 0), false))
  | 2 => Sum.inl (((0, 1), false))
  | 3 => Sum.inl (((1, 1), false))
  | 4 => Sum.inl (((0, 0), true))
  | 5 => Sum.inl (((1, 0), true))
  | 6 => Sum.inl (((0, 1), true))
  | 7 => Sum.inl (((1, 1), true))
  | 8 => typedWitness9

def typedZone9Equiv : D0.V9 ≃ Scene9 where
  toFun := typedZone9Index
  invFun := scene9Preimage
  left_inv v := by
    cases v with
    | inl p =>
        rcases p with ⟨⟨a, b⟩, o⟩
        fin_cases a <;> fin_cases b <;> cases o <;>
          simp [typedZone9Index, scene9Preimage, typedWitness9]
    | inr w =>
        cases w
        simp [typedZone9Index, scene9Preimage, typedWitness9]
  right_inv i := by
    fin_cases i <;> simp [typedZone9Index, scene9Preimage, typedWitness9]

def typedZone11Index : D0.V11 → Scene11
  | Sum.inl v => Fin.mk (typedZone9Index v).val (by
      have hlt := (typedZone9Index v).isLt
      omega)
  | Sum.inr d => Fin.mk (9 + d.val) (by fin_cases d <;> decide)

def scene11Preimage : Scene11 → D0.V11
  | 0 => Sum.inl (scene9Preimage 0)
  | 1 => Sum.inl (scene9Preimage 1)
  | 2 => Sum.inl (scene9Preimage 2)
  | 3 => Sum.inl (scene9Preimage 3)
  | 4 => Sum.inl (scene9Preimage 4)
  | 5 => Sum.inl (scene9Preimage 5)
  | 6 => Sum.inl (scene9Preimage 6)
  | 7 => Sum.inl (scene9Preimage 7)
  | 8 => Sum.inl (scene9Preimage 8)
  | 9 => Sum.inr 0
  | 10 => Sum.inr 1

def typedZone11Equiv : D0.V11 ≃ Scene11 where
  toFun := typedZone11Index
  invFun := scene11Preimage
  left_inv v := by
    cases v with
    | inl w =>
        have h9 := typedZone9Equiv.left_inv w
        cases w with
        | inl p =>
            rcases p with ⟨⟨a, b⟩, o⟩
            fin_cases a <;> fin_cases b <;> cases o <;>
              simp [typedZone11Index, scene11Preimage, typedZone9Index, scene9Preimage, h9]
        | inr u =>
            cases u
            simp [typedZone11Index, scene11Preimage, typedZone9Index, scene9Preimage, typedWitness9]
    | inr d =>
        fin_cases d <;> simp [typedZone11Index, scene11Preimage]
  right_inv i := by
    fin_cases i <;> simp [typedZone11Index, scene11Preimage, typedZone9Index, scene9Preimage,
      typedWitness9]

def typedZone13Index : D0.V13 → Scene13
  | Sum.inl v => Fin.mk (typedZone9Index v).val (by
      have hlt := (typedZone9Index v).isLt
      omega)
  | Sum.inr (a, b) => Fin.mk (9 + a.val + 2 * b.val) (by
      fin_cases a <;> fin_cases b <;> decide)

def scene13Preimage : Scene13 → D0.V13
  | 0 => Sum.inl (scene9Preimage 0)
  | 1 => Sum.inl (scene9Preimage 1)
  | 2 => Sum.inl (scene9Preimage 2)
  | 3 => Sum.inl (scene9Preimage 3)
  | 4 => Sum.inl (scene9Preimage 4)
  | 5 => Sum.inl (scene9Preimage 5)
  | 6 => Sum.inl (scene9Preimage 6)
  | 7 => Sum.inl (scene9Preimage 7)
  | 8 => Sum.inl (scene9Preimage 8)
  | 9 => Sum.inr (0, 0)
  | 10 => Sum.inr (1, 0)
  | 11 => Sum.inr (0, 1)
  | 12 => Sum.inr (1, 1)

def typedZone13Equiv : D0.V13 ≃ Scene13 where
  toFun := typedZone13Index
  invFun := scene13Preimage
  left_inv v := by
    cases v with
    | inl w =>
        cases w with
        | inl p =>
            rcases p with ⟨⟨a, b⟩, o⟩
            fin_cases a <;> fin_cases b <;> cases o <;>
              simp [typedZone13Index, scene13Preimage, typedZone9Index, scene9Preimage]
        | inr u =>
            cases u
            simp [typedZone13Index, scene13Preimage, typedZone9Index, scene9Preimage, typedWitness9]
    | inr r =>
        rcases r with ⟨a, b⟩
        fin_cases a <;> fin_cases b <;>
          simp [typedZone13Index, scene13Preimage]
  right_inv i := by
    fin_cases i <;> simp [typedZone13Index, scene13Preimage, typedZone9Index, scene9Preimage,
      typedWitness9]

/-- A cardinality bridge.  Its fields do not mention weights, records, or line comparison. -/
structure CardinalityBridge where
  zone9 : D0.V9 ≃ Scene9
  zone11 : D0.V11 ≃ Scene11
  zone13 : D0.V13 ≃ Scene13

def explicitCardinalityBridge : CardinalityBridge where
  zone9 := typedZone9Equiv
  zone11 := typedZone11Equiv
  zone13 := typedZone13Equiv

theorem cardinality_bridge_not_unique :
    ∃ b₁ b₂ : CardinalityBridge, b₁ ≠ b₂ := by
  let swap9 : Scene9 ≃ Scene9 := Equiv.swap 8 0
  have hswap : swap9 8 = 0 := by
    exact Equiv.swap_apply_left (a := (8 : Scene9)) (b := (0 : Scene9))
  refine ⟨explicitCardinalityBridge,
    { explicitCardinalityBridge with zone9 := typedZone9Equiv.trans swap9 }, ?_⟩
  intro h
  have hfun := congrArg CardinalityBridge.zone9 h
  have hw := congrFun (congrArg Equiv.toFun hfun) typedWitness9
  simp [explicitCardinalityBridge, typedZone9Equiv, typedZone9Index, typedWitness9, swap9,
    hswap] at hw

theorem witness_landing_not_forced :
    ∃ e₁ e₂ : D0.V9 ≃ Scene9, e₁ typedWitness9 = 8 ∧ e₂ typedWitness9 = 0 := by
  let swap9 : Scene9 ≃ Scene9 := Equiv.swap 8 0
  refine ⟨typedZone9Equiv, typedZone9Equiv.trans swap9, ?_, ?_⟩
  · simp [typedZone9Equiv, typedZone9Index, typedWitness9]
  · have hswap : swap9 8 = 0 := by
      exact Equiv.swap_apply_left (a := (8 : Scene9)) (b := (0 : Scene9))
    simp [typedZone9Equiv, typedZone9Index, typedWitness9, swap9, hswap]

/-! ## Readouts sourced from the verification outcome

A readout may depend on a line only through that line's outcome table.  The
contract makes those tables equal, so the two readouts agree for every correct
protocol.  That agreement is not the uniform-weight locus.
-/

structure OutcomeSourcedReadout (P : VerificationProtocol) where
  ofOutcome : (P.Catalogue → P.State → P.State → Bool) →
    EdgeCochain →ₗ[ℚ] VertexCochain

theorem outcome_sourced_readouts_agree {P : VerificationProtocol}
    (V : VerificationContract P) (R : OutcomeSourcedReadout P) (l l' : P.Line) :
    R.ofOutcome (verificationLineOutcome P l) =
      R.ofOutcome (verificationLineOutcome P l') := by
  rw [verificationLineOutcome_eq V]

theorem uniform_positive_weight_iff_mismatch_zero (x y z : ℚ)
    (hx : 0 < x) (hy : 0 < y) (hz : 0 < z) :
    (x = y ∧ y = z) ↔
      ∀ X : KPlus, D0.Geometry.SignlessSignedCommonCarrier.BPlusLin
        (WInverse x y z (X : EdgeCochain)) = 0 :=
  (positive_weight_mismatch_zero_iff x y z hx hy hz).symm

theorem outcome_agreement_does_not_force_uniform_weight
    (R : OutcomeSourcedReadout boolProtocol) :
    (∀ l l' : boolProtocol.Line,
      R.ofOutcome (verificationLineOutcome boolProtocol l) =
        R.ofOutcome (verificationLineOutcome boolProtocol l')) ∧
      0 < (1 : ℚ) ∧ 0 < (2 : ℚ) ∧ 0 < (3 : ℚ) ∧
      ¬ ((1 : ℚ) = 2 ∧ (2 : ℚ) = 3) ∧
      ¬ (∀ X : KPlus, mismatchOnK (1 : ℚ)⁻¹ 2⁻¹ 3⁻¹ X = 0) := by
  obtain ⟨V, hx, hy, hz, hneq, hmis⟩ :=
    verification_contract_coexists_with_nonuniform_mismatch
  exact ⟨fun l l' => outcome_sourced_readouts_agree V R l l', hx, hy, hz, hneq, hmis⟩

/-- The centered radius-one identity can hold while the block weights stay nonuniform. -/
theorem centering_coexists_with_nonuniform_mismatch :
    (∀ (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℝ),
      radiusOneAverage (1 / 2) (1 / 2) N r f = backwardAverage N r f) ∧
      ¬ (∀ X : KPlus, mismatchOnK (1 : ℚ)⁻¹ 2⁻¹ 3⁻¹ X = 0) := by
  exact ⟨fun N r f => radiusOneAverage_half_eq_backwardAverage N r f,
    verification_contract_coexists_with_nonuniform_mismatch.2.2.2.2.2⟩

end D0.Foundation.M1RieszRepresentationGap
