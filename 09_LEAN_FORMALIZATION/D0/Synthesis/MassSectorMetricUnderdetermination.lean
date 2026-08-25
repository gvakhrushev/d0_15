import D0.Synthesis.ChargedLeptonShellBridge

/-!
# Mass-sector metric boundary: order is closed, one positive gap remains free

The charged-lepton branch names, the structural shells, and the ordered transport roots are
already connected by unique order-preserving bridges.  None of those theorems fixes the numerical
torus parameter `a`.

This module identifies the exact residual rather than merely calling it "missing data":

* every admissible shell metric is an equally spaced triple
  `(1, 1 + g, 1 + 2g)` for one positive rational gap `g`;
* `TorusParameter` is equivalent to the type of positive rational gaps, so this is exactly one
  metric degree of freedom, not three unrelated radii;
* the owned radial-order profile is constant on that whole family;
* therefore no selector that factors only through the owned order can choose a unique metric;
* the charged-lepton-to-transport-root labeling is parameter-free and remains unchanged while
  the numerical gap varies.

This is a no-go only for extracting the numerical metric from the present order data.  It does
not rule out a new dynamical equation, measured passport, Green-resolvent condition, or EFT/IR
matching functional that selects one positive gap.
-/

namespace D0.Synthesis.MassSectorMetricUnderdetermination

open D0.Geometry
open D0.Matter
open D0.Synthesis.ChargedLeptonShellBridge
open D0.Synthesis.GenerationRootOrderBridge
open D0.Synthesis.TransportRootLabeling

/-- The single adjacent radial gap carried by an admissible torus parameter. -/
def shellGap (T : TorusParameter) : ℚ :=
  TorusShell.radius T .coreD11 - TorusShell.radius T .innerD9

/-- The shell gap is exactly the minor torus radius `(a-1)/2`. -/
theorem shellGap_eq_minor (T : TorusParameter) :
    shellGap T = T.minor := by
  simp [shellGap, TorusShell.radius, TorusShell.toShell3,
    TorusParameter.shellRadius, TorusParameter.core, TorusParameter.inner,
    TorusParameter.minor]
  ring

/-- Every admissible shell gap is positive. -/
theorem shellGap_pos (T : TorusParameter) :
    0 < shellGap T := by
  rw [shellGap_eq_minor]
  exact T.minor_pos

/-- The core radius is reconstructed from the unit inner radius and the one free gap. -/
theorem core_radius_eq_one_add_gap (T : TorusParameter) :
    TorusShell.radius T .coreD11 = 1 + shellGap T := by
  simp [shellGap, TorusShell.radius, TorusShell.toShell3,
    TorusParameter.shellRadius, TorusParameter.core, TorusParameter.inner]

/-- The outer radius is reconstructed from the same gap. -/
theorem outer_radius_eq_one_add_two_gap (T : TorusParameter) :
    TorusShell.radius T .outerD13 = 1 + 2 * shellGap T := by
  simp [shellGap, TorusShell.radius, TorusShell.toShell3,
    TorusParameter.shellRadius, TorusParameter.core, TorusParameter.inner,
    TorusParameter.outer]
  ring

/-- The two adjacent shell gaps are forced to be equal. -/
theorem outer_core_gap_eq_shellGap (T : TorusParameter) :
    TorusShell.radius T .outerD13 - TorusShell.radius T .coreD11 = shellGap T := by
  rw [core_radius_eq_one_add_gap, outer_radius_eq_one_add_two_gap]
  ring

/-- The original torus parameter is exactly recoverable from the positive gap. -/
theorem torusParameter_eq_one_add_two_gap (T : TorusParameter) :
    T.a = 1 + 2 * shellGap T := by
  rw [shellGap_eq_minor]
  simp [TorusParameter.minor]
  ring

/-- Carrier for the exact residual metric datum. -/
structure PositiveShellGap where
  value : ℚ
  h_pos : 0 < value

theorem torusParameter_ext {T U : TorusParameter} (h : T.a = U.a) : T = U := by
  cases T
  cases U
  simp_all

theorem positiveShellGap_ext {G H : PositiveShellGap} (h : G.value = H.value) : G = H := by
  cases G
  cases H
  simp_all

/-- Forget an admissible torus parameter down to its sole positive metric modulus. -/
def torusToPositiveGap (T : TorusParameter) : PositiveShellGap :=
  ⟨shellGap T, shellGap_pos T⟩

/-- Reconstruct the full torus parameter from one positive rational gap. -/
def positiveGapToTorus (G : PositiveShellGap) : TorusParameter where
  a := 1 + 2 * G.value
  h_gt_one := by linarith [G.h_pos]

theorem positiveGapToTorus_torusToPositiveGap (T : TorusParameter) :
    positiveGapToTorus (torusToPositiveGap T) = T := by
  apply torusParameter_ext
  exact (torusParameter_eq_one_add_two_gap T).symm

theorem torusToPositiveGap_positiveGapToTorus (G : PositiveShellGap) :
    torusToPositiveGap (positiveGapToTorus G) = G := by
  apply positiveShellGap_ext
  simp [torusToPositiveGap, positiveGapToTorus, shellGap, TorusShell.radius,
    TorusShell.toShell3, TorusParameter.shellRadius, TorusParameter.core,
    TorusParameter.inner]
  ring

/-- **Exact metric classification.** Admissible shell metrics are equivalent to one positive
rational number. -/
def torusParameterEquivPositiveGap : TorusParameter ≃ PositiveShellGap where
  toFun := torusToPositiveGap
  invFun := positiveGapToTorus
  left_inv := positiveGapToTorus_torusToPositiveGap
  right_inv := torusToPositiveGap_positiveGapToTorus

/-- The gap, hence the whole radial triple, separates torus parameters. -/
theorem shellGap_injective : Function.Injective shellGap := by
  intro T U h
  apply torusParameter_ext
  rw [torusParameter_eq_one_add_two_gap T, torusParameter_eq_one_add_two_gap U, h]

/-- The complete branch-name-to-transport-root bridge; it contains no metric parameter. -/
def chargedLeptonTransportBridge
    (R : D0.Synthesis.YukawaQualitativeSelectorNoGo.TransportRootFrame) :
    ChargedLeptonBranch → ℝ :=
  fun b => generationRootBridge R (chargedLeptonShellBridge b)

@[simp] theorem chargedLeptonTransportBridge_electron
    (R : D0.Synthesis.YukawaQualitativeSelectorNoGo.TransportRootFrame) :
    chargedLeptonTransportBridge R .electron = R.root 0 := rfl

@[simp] theorem chargedLeptonTransportBridge_muon
    (R : D0.Synthesis.YukawaQualitativeSelectorNoGo.TransportRootFrame) :
    chargedLeptonTransportBridge R .muon = R.root 1 := rfl

@[simp] theorem chargedLeptonTransportBridge_tau
    (R : D0.Synthesis.YukawaQualitativeSelectorNoGo.TransportRootFrame) :
    chargedLeptonTransportBridge R .tau = R.root 2 := rfl

/-- The exact two-bit order profile currently visible to the mass-sector bridge. -/
def radialOrderCode (T : TorusParameter) : Bool × Bool :=
  (decide (TorusShell.radius T .innerD9 < TorusShell.radius T .coreD11),
   decide (TorusShell.radius T .coreD11 < TorusShell.radius T .outerD13))

/-- Every positive gap has the same owned order code. -/
theorem radialOrderCode_constant (T : TorusParameter) :
    radialOrderCode T = (true, true) := by
  have h := torusShell_radius_strictMono T
  simp [radialOrderCode, h.1, h.2]

/-- A metric selector is order-only when it cannot distinguish equal owned order profiles. -/
def FactorsThroughRadialOrder (select : TorusParameter → Prop) : Prop :=
  ∀ T U, radialOrderCode T = radialOrderCode U → (select T ↔ select U)

/-- Every order-only metric selector is constant on the entire admissible parameter family. -/
theorem orderOnlySelector_constant (select : TorusParameter → Prop)
    (hfactor : FactorsThroughRadialOrder select) (T U : TorusParameter) :
    select T ↔ select U :=
  hfactor T U ((radialOrderCode_constant T).trans (radialOrderCode_constant U).symm)

/-- First concrete admissible metric witness: `a=2`, gap `1/2`. -/
def metricWitnessTwo : TorusParameter where
  a := 2
  h_gt_one := by norm_num

/-- Second concrete admissible metric witness: `a=3`, gap `1`. -/
def metricWitnessThree : TorusParameter where
  a := 3
  h_gt_one := by norm_num

theorem metricWitnessTwo_gap :
    shellGap metricWitnessTwo = 1 / 2 := by
  norm_num [shellGap, metricWitnessTwo, TorusShell.radius, TorusShell.toShell3,
    TorusParameter.shellRadius, TorusParameter.core, TorusParameter.inner]

theorem metricWitnessThree_gap :
    shellGap metricWitnessThree = 1 := by
  norm_num [shellGap, metricWitnessThree, TorusShell.radius, TorusShell.toShell3,
    TorusParameter.shellRadius, TorusParameter.core, TorusParameter.inner]

theorem metricWitnessTwo_ne_Three :
    metricWitnessTwo ≠ metricWitnessThree := by
  intro h
  have ha := congrArg TorusParameter.a h
  norm_num [metricWitnessTwo, metricWitnessThree] at ha

/-- **Metric underdetermination no-go.** No selector factoring only through the already-owned
radial order can select exactly one admissible metric. -/
theorem no_unique_order_only_metric_selector (select : TorusParameter → Prop)
    (hfactor : FactorsThroughRadialOrder select) :
    ¬ ∃! T : TorusParameter, select T := by
  rintro ⟨T, hT, huniq⟩
  have hTwo : select metricWitnessTwo :=
    (orderOnlySelector_constant select hfactor T metricWitnessTwo).mp hT
  have hThree : select metricWitnessThree :=
    (orderOnlySelector_constant select hfactor T metricWitnessThree).mp hT
  have h2 : metricWitnessTwo = T := huniq metricWitnessTwo hTwo
  have h3 : metricWitnessThree = T := huniq metricWitnessThree hThree
  exact metricWitnessTwo_ne_Three (h2.trans h3.symm)

/-- Capstone boundary: labeling/order is parameter-free, while the numerical shell metric is
exactly one positive modulus and is not selectable from order alone. -/
theorem mass_sector_metric_boundary :
    (∀ T : TorusParameter,
      TorusShell.radius T (chargedLeptonShellBridge .electron) <
          TorusShell.radius T (chargedLeptonShellBridge .muon)
      ∧ TorusShell.radius T (chargedLeptonShellBridge .muon) <
          TorusShell.radius T (chargedLeptonShellBridge .tau))
    ∧ (∀ T : TorusParameter,
        TorusShell.radius T .innerD9 = 1
        ∧ TorusShell.radius T .coreD11 = 1 + shellGap T
        ∧ TorusShell.radius T .outerD13 = 1 + 2 * shellGap T
        ∧ 0 < shellGap T)
    ∧ radialOrderCode metricWitnessTwo = radialOrderCode metricWitnessThree
    ∧ shellGap metricWitnessTwo ≠ shellGap metricWitnessThree
    ∧ (∀ select : TorusParameter → Prop,
        FactorsThroughRadialOrder select → ¬ ∃! T : TorusParameter, select T) := by
  refine ⟨chargedLeptonShellBridge_strict, ?_, ?_, ?_, no_unique_order_only_metric_selector⟩
  · intro T
    exact ⟨torusShell_inner_unit T, core_radius_eq_one_add_gap T,
      outer_radius_eq_one_add_two_gap T, shellGap_pos T⟩
  · rw [radialOrderCode_constant metricWitnessTwo,
      radialOrderCode_constant metricWitnessThree]
  · rw [metricWitnessTwo_gap, metricWitnessThree_gap]
    norm_num

end D0.Synthesis.MassSectorMetricUnderdetermination
