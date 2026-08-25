import D0.Synthesis.MassSectorMetricUnderdetermination

/-!
# Joint mass-sector completion no-go: both continuous fibers must be broken

Two exact residual families have now been identified:

* the non-scalar Yukawa coefficient family is invisible to the owned qualitative
  equality/irrationality profile;
* the positive shell-gap family is invisible to the owned radial order.

This module proves that combining those two coarse data sets does not restore uniqueness.
More sharply, any unique joint selector of a non-scalar Yukawa coefficient and a shell metric
must use new information on **both** axes:

1. it must distinguish coefficient triples with identical owned Yukawa profiles;
2. it must distinguish metrics with identical owned radial-order codes.

A single cross-coupled functional may satisfy both obligations, but neither the qualitative
Yukawa theorem nor the shell order — separately or together — can do so.
-/

namespace D0.Synthesis.MassSectorCompletionNoGo

open D0.Geometry
open D0.Synthesis.YukawaQualitativeSelectorNoGo
open D0.Synthesis.MassSectorMetricUnderdetermination

/-- A joint candidate consists of one equivariant Yukawa coefficient triple and one shell
metric parameter. -/
abbrev MassCandidate := YukawaCoeff × TorusParameter

/-- Current theorem-level data identify two joint candidates when both the qualitative Yukawa
profile and the radial order code agree. -/
def CurrentMassDataEquivalent (R : TransportRootFrame)
    (x y : MassCandidate) : Prop :=
  OwnedProfileEquivalent R x.1 y.1 ∧ radialOrderCode x.2 = radialOrderCode y.2

/-- All non-scalar joint candidates are equivalent under the current coarse data. -/
theorem all_nonScalar_mass_candidates_equivalent (R : TransportRootFrame)
    (x y : MassCandidate) (hx : NonScalar x.1) (hy : NonScalar y.1) :
    CurrentMassDataEquivalent R x y :=
  ⟨all_nonScalar_profile_equivalent R x.1 y.1 hx hy,
    (radialOrderCode_constant x.2).trans (radialOrderCode_constant y.2).symm⟩

/-- A selector factors through the complete currently-owned mass data when it is invariant under
the joint equivalence above. -/
def FactorsThroughCurrentMassData (R : TransportRootFrame)
    (select : MassCandidate → Prop) : Prop :=
  ∀ x y, CurrentMassDataEquivalent R x y → (select x ↔ select y)

/-- Coefficient blindness at fixed metric: the selector cannot distinguish non-scalar
coefficients with the same owned Yukawa profile. -/
def CoefficientProfileBlind (R : TransportRootFrame)
    (select : MassCandidate → Prop) : Prop :=
  ∀ (k l : YukawaCoeff) (T : TorusParameter),
    NonScalar k → NonScalar l → OwnedProfileEquivalent R k l →
    (select (k, T) ↔ select (l, T))

/-- Metric blindness at fixed coefficient: the selector cannot distinguish shell metrics with
the same owned radial order. -/
def RadialOrderBlind (select : MassCandidate → Prop) : Prop :=
  ∀ (k : YukawaCoeff) (T U : TorusParameter),
    radialOrderCode T = radialOrderCode U →
    (select (k, T) ↔ select (k, U))

/-- Joint-data factorization implies coefficient blindness. -/
theorem factorsThroughCurrentMassData_coefficientBlind (R : TransportRootFrame)
    (select : MassCandidate → Prop) (h : FactorsThroughCurrentMassData R select) :
    CoefficientProfileBlind R select := by
  intro k l T hk hl hprofile
  exact h (k, T) (l, T) ⟨hprofile, rfl⟩

/-- Joint-data factorization implies radial-order blindness. -/
theorem factorsThroughCurrentMassData_radialBlind (R : TransportRootFrame)
    (select : MassCandidate → Prop) (h : FactorsThroughCurrentMassData R select) :
    RadialOrderBlind select := by
  intro k T U horder
  -- `OwnedProfileEquivalent` is reflexive on any non-scalar coefficient; the arbitrary `k`
  -- need not be non-scalar, so establish reflexivity directly from the definition.
  have hrefl : OwnedProfileEquivalent R k k := by
    constructor <;> intro <;> simp
  exact h (k, T) (k, U) ⟨hrefl, horder⟩

/-- Coefficient-profile blindness alone already prevents a unique non-scalar joint candidate,
even if the selector may use the shell metric arbitrarily. -/
theorem no_unique_mass_selector_if_coefficientBlind (R : TransportRootFrame)
    (select : MassCandidate → Prop) (hblind : CoefficientProfileBlind R select) :
    ¬ ∃! x : MassCandidate, NonScalar x.1 ∧ select x := by
  rintro ⟨x, hx, huniq⟩
  let x0 : MassCandidate := (affineFamily 0, x.2)
  let x1 : MassCandidate := (affineFamily 1, x.2)
  have h0ns : NonScalar x0.1 := affineFamily_nonScalar 0
  have h1ns : NonScalar x1.1 := affineFamily_nonScalar 1
  have hp0 : OwnedProfileEquivalent R x.1 x0.1 :=
    all_nonScalar_profile_equivalent R x.1 x0.1 hx.1 h0ns
  have hp1 : OwnedProfileEquivalent R x.1 x1.1 :=
    all_nonScalar_profile_equivalent R x.1 x1.1 hx.1 h1ns
  have hs0 : select x0 := (hblind x.1 x0.1 x.2 hx.1 h0ns hp0).mp hx.2
  have hs1 : select x1 := (hblind x.1 x1.1 x.2 hx.1 h1ns hp1).mp hx.2
  have heq0 : x0 = x := huniq x0 ⟨h0ns, hs0⟩
  have heq1 : x1 = x := huniq x1 ⟨h1ns, hs1⟩
  have hcoeff : affineFamily (0 : ℚ) = affineFamily 1 :=
    congrArg Prod.fst (heq0.trans heq1.symm)
  exact (by norm_num : (0 : ℚ) ≠ 1) (affineFamily_injective hcoeff)

/-- Radial-order blindness alone already prevents a unique joint candidate, even if the selector
may use the Yukawa coefficients arbitrarily. -/
theorem no_unique_mass_selector_if_radialBlind
    (select : MassCandidate → Prop) (hblind : RadialOrderBlind select) :
    ¬ ∃! x : MassCandidate, NonScalar x.1 ∧ select x := by
  rintro ⟨x, hx, huniq⟩
  let x2 : MassCandidate := (x.1, metricWitnessTwo)
  let x3 : MassCandidate := (x.1, metricWitnessThree)
  have horder : radialOrderCode metricWitnessTwo = radialOrderCode metricWitnessThree :=
    (radialOrderCode_constant metricWitnessTwo).trans
      (radialOrderCode_constant metricWitnessThree).symm
  have hs2 : select x2 := by
    have hx2 := hblind x.1 x.2 metricWitnessTwo
      ((radialOrderCode_constant x.2).trans
        (radialOrderCode_constant metricWitnessTwo).symm)
    exact hx2.mp hx.2
  have hs3 : select x3 := by
    have hx3 := hblind x.1 x.2 metricWitnessThree
      ((radialOrderCode_constant x.2).trans
        (radialOrderCode_constant metricWitnessThree).symm)
    exact hx3.mp hx.2
  have heq2 : x2 = x := huniq x2 ⟨hx.1, hs2⟩
  have heq3 : x3 = x := huniq x3 ⟨hx.1, hs3⟩
  have hmetric : metricWitnessTwo = metricWitnessThree :=
    congrArg Prod.snd (heq2.trans heq3.symm)
  exact metricWitnessTwo_ne_Three hmetric

/-- Combining the two currently-owned coarse profiles still cannot select a unique mass
candidate. -/
theorem no_unique_current_mass_data_selector (R : TransportRootFrame)
    (select : MassCandidate → Prop) (hfactor : FactorsThroughCurrentMassData R select) :
    ¬ ∃! x : MassCandidate, NonScalar x.1 ∧ select x :=
  no_unique_mass_selector_if_coefficientBlind R select
    (factorsThroughCurrentMassData_coefficientBlind R select hfactor)

/-- **Two-axis necessity.** Every genuinely unique mass completion must break both present
fibers: the Yukawa coefficient profile and the shell-order profile. -/
theorem unique_mass_selector_requires_two_axis_information (R : TransportRootFrame)
    (select : MassCandidate → Prop)
    (huniq : ∃! x : MassCandidate, NonScalar x.1 ∧ select x) :
    ¬ CoefficientProfileBlind R select ∧ ¬ RadialOrderBlind select := by
  constructor
  · intro h
    exact no_unique_mass_selector_if_coefficientBlind R select h huniq
  · intro h
    exact no_unique_mass_selector_if_radialBlind select h huniq

/-- Capstone on an actual transport-root frame: current data collapse the whole non-scalar
coefficient × positive-metric product, and every unique completion must add information on both
axes. -/
theorem mass_sector_completion_information_boundary :
    ∃ R : TransportRootFrame,
      (∀ x y : MassCandidate, NonScalar x.1 → NonScalar y.1 →
        CurrentMassDataEquivalent R x y)
      ∧ (∀ select : MassCandidate → Prop,
          FactorsThroughCurrentMassData R select →
          ¬ ∃! x : MassCandidate, NonScalar x.1 ∧ select x)
      ∧ (∀ select : MassCandidate → Prop,
          (∃! x : MassCandidate, NonScalar x.1 ∧ select x) →
          ¬ CoefficientProfileBlind R select ∧ ¬ RadialOrderBlind select) := by
  obtain ⟨R⟩ := transportRootFrame_exists
  exact ⟨R, all_nonScalar_mass_candidates_equivalent R,
    no_unique_current_mass_data_selector R,
    unique_mass_selector_requires_two_axis_information R⟩

end D0.Synthesis.MassSectorCompletionNoGo
