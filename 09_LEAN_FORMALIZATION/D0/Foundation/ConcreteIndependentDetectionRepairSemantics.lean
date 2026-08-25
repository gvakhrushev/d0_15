import D0.Foundation.IndependentDetectionRepairGrammar
import D0.Synthesis.ConcretePhysicalDetectorRepresentation
import D0.Geometry.TorusShellAttachment
import D0.Synthesis.SceneAnisotropyCapacityWeld

/-!
# Concrete independent-detection repair semantics and physical scene representation

This module removes the last modelling premise left by
`IndependentDetectionRepairGrammar`: that a repair's observational datum is its order-arity over
the two independent detector loops.

The concrete D0 comparison carrier is binary, and its catalogue is already two-sided:

`InputSide → Current → Bool`.

Therefore a comparison has a *history-support* consisting of the argument positions (`left`,
`right`) at which changing history while holding current data fixed can change the result. This is
an actual extensional predicate on the concrete `Observation` comparison function, not a declared
kind. The observational arity is the cardinality of that support.

Because `InputSide` has exactly two elements, every concrete comparison has arity `0`, `1`, or `2`.
All three arities are realised:

* membership comparison — support `∅`, arity `0`;
* left-history read — support `{left}`, arity `1`;
* history equality — support `{left,right}`, arity `2`.

Quotienting *all concrete comparisons* by equality of this computed arity gives a quotient
equivalent to `RepairArity 2`, hence to the structural `RepairObservationQuotient`. This is the
physical repair-grammar completeness theorem: the former "repair datum = order-arity" premise is
now a theorem of the concrete two-sided independent-detection model.

The same arity equivalence is then composed with the already-owned radial-order equivalence
`Shell3 ≃ TorusShell`, yielding a concrete faithful representation of repair classes in the in-repo
physical shell scene. The mapping is structural: arity `0/1/2` maps to inner/core/outer radial
position. No zone-size selector is claimed; the existing `TorusShell.zoneSize` labels remain owned
by their separate frozen attachment.
-/

namespace D0.Foundation.ConcreteIndependentDetectionRepairSemantics

open scoped Classical

open D0.Foundation
open D0.Foundation.DetectionCapabilityBoundary
open D0.Foundation.DiscriminationKinds
open D0.Foundation.DiscriminationRetyping
open D0.Foundation.IndependentDetectionRepairGrammar
open D0.Foundation.M1CascadeSceneNoGo
open D0.Foundation.M1RepairObservationalQuotient
open D0.Foundation.SceneCountReduction
open D0.Synthesis.ConcretePhysicalDetectorRepresentation
open D0.Geometry
open D0.Synthesis.SceneAnisotropyCapacityWeld

/-- Current membership/value data agree; only history may differ. -/
def SameCurrent (x x' : Observation) : Prop :=
  x.member = x'.member ∧ x.value = x'.value

/-- Extensional dependence on the history coordinate of one binary-input side. -/
def UsesHistorySide (cmp : Comparison) : InputSide → Prop
  | .left =>
      ∃ x x' y : Observation,
        SameCurrent x x' ∧ cmp x y ≠ cmp x' y
  | .right =>
      ∃ x y y' : Observation,
        SameCurrent y y' ∧ cmp x y ≠ cmp x y'

/-- Actual history-support of a concrete binary comparison. -/
noncomputable def historySupport (cmp : Comparison) : Finset InputSide :=
  Finset.univ.filter (UsesHistorySide cmp)

/-- The computed repair arity: number of independently variable history sides used. -/
noncomputable def comparisonRepairArity (cmp : Comparison) :
    RepairArity detectionBudget := by
  refine ⟨(historySupport cmp).card, ?_⟩
  have hle : (historySupport cmp).card ≤ Fintype.card InputSide :=
    Finset.card_le_univ _
  have hcard : Fintype.card InputSide = detectionBudget := by decide
  rw [hcard] at hle
  exact Nat.lt_succ_of_le hle

/-! ## Three concrete witnesses -/

def obsHistoryFalse : Observation := ⟨false, false, false⟩
def obsHistoryTrue : Observation := ⟨false, false, true⟩

/-- Arity-0 witness: current membership comparison ignores both histories. -/
def zeroArityComparison : Comparison := membershipComparison

/-- Arity-1 witness: read only the left history. -/
def oneArityComparison : Comparison := fun x _ => x.history

/-- Arity-2 witness: compare both histories. -/
def twoArityComparison : Comparison := historyComparison

theorem zeroArity_uses_no_side (s : InputSide) :
    ¬ UsesHistorySide zeroArityComparison s := by
  cases s with
  | left =>
      rintro ⟨x, x', y, hcur, hneq⟩
      apply hneq
      simp [zeroArityComparison, membershipComparison, hcur.1]
  | right =>
      rintro ⟨x, y, y', hcur, hneq⟩
      apply hneq
      simp [zeroArityComparison, membershipComparison, hcur.1]

theorem oneArity_uses_left :
    UsesHistorySide oneArityComparison .left := by
  refine ⟨obsHistoryFalse, obsHistoryTrue, obsHistoryFalse, ?_, ?_⟩
  · exact ⟨rfl, rfl⟩
  · decide

theorem oneArity_not_uses_right :
    ¬ UsesHistorySide oneArityComparison .right := by
  rintro ⟨x, y, y', _, hneq⟩
  exact hneq rfl

theorem twoArity_uses_left :
    UsesHistorySide twoArityComparison .left := by
  refine ⟨obsHistoryFalse, obsHistoryTrue, obsHistoryFalse, ?_, ?_⟩
  · exact ⟨rfl, rfl⟩
  · decide

theorem twoArity_uses_right :
    UsesHistorySide twoArityComparison .right := by
  refine ⟨obsHistoryFalse, obsHistoryFalse, obsHistoryTrue, ?_, ?_⟩
  · exact ⟨rfl, rfl⟩
  · decide

theorem zeroArity_support :
    historySupport zeroArityComparison = ∅ := by
  ext s
  simp [historySupport, zeroArity_uses_no_side]

theorem oneArity_support :
    historySupport oneArityComparison = {.left} := by
  ext s
  cases s <;>
    simp [historySupport, oneArity_uses_left, oneArity_not_uses_right]

theorem twoArity_support :
    historySupport twoArityComparison = Finset.univ := by
  ext s
  cases s <;>
    simp [historySupport, twoArity_uses_left, twoArity_uses_right]

theorem zeroArity_value :
    comparisonRepairArity zeroArityComparison = 0 := by
  apply Fin.ext
  simp [comparisonRepairArity, zeroArity_support]

theorem oneArity_value :
    comparisonRepairArity oneArityComparison = 1 := by
  apply Fin.ext
  simp [comparisonRepairArity, oneArity_support]

theorem twoArity_value :
    comparisonRepairArity twoArityComparison = 2 := by
  apply Fin.ext
  simp [comparisonRepairArity, twoArity_support,
    show Fintype.card InputSide = 2 by decide]

/-! ## Physical comparison quotient by computed support arity -/

/-- Physical repair comparisons are observationally equivalent exactly when their computed
left/right history-support cardinalities agree. -/
def SamePhysicalRepairObservation (p q : Comparison) : Prop :=
  comparisonRepairArity p = comparisonRepairArity q

def physicalRepairObservationSetoid : Setoid Comparison where
  r := SamePhysicalRepairObservation
  iseqv := {
    refl := fun _ => rfl
    symm := fun h => h.symm
    trans := fun h₁ h₂ => h₁.trans h₂
  }

abbrev PhysicalRepairObservationQuotient :=
  Quotient physicalRepairObservationSetoid

def physicalRepairClass (p : Comparison) :
    PhysicalRepairObservationQuotient :=
  Quotient.mk physicalRepairObservationSetoid p

noncomputable def physicalClassArity :
    PhysicalRepairObservationQuotient → RepairArity detectionBudget :=
  Quotient.lift comparisonRepairArity (by
    intro p q h
    exact h)

/-- Canonical concrete comparison realising each support arity. -/
def comparisonOfArity (a : RepairArity detectionBudget) : Comparison :=
  if a = 0 then zeroArityComparison
  else if a = 1 then oneArityComparison
  else twoArityComparison

@[simp] theorem comparisonOfArity_has_arity
    (a : RepairArity detectionBudget) :
    comparisonRepairArity (comparisonOfArity a) = a := by
  apply Fin.ext
  fin_cases a <;>
    simp [comparisonOfArity, zeroArity_value, oneArity_value, twoArity_value]

/-- **Physical grammar completeness.** The quotient of all concrete binary comparisons by computed
independent-side history arity is exactly `RepairArity 2`. -/
noncomputable def physicalRepairQuotientEquivArity :
    PhysicalRepairObservationQuotient ≃ RepairArity detectionBudget where
  toFun := physicalClassArity
  invFun := fun a => physicalRepairClass (comparisonOfArity a)
  left_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro p
    apply Quotient.sound
    change comparisonRepairArity
      (comparisonOfArity (comparisonRepairArity p)) =
      comparisonRepairArity p
    exact comparisonOfArity_has_arity _
  right_inv := comparisonOfArity_has_arity

noncomputable instance physicalRepairObservationQuotientFintype :
    Fintype PhysicalRepairObservationQuotient :=
  Fintype.ofEquiv (RepairArity detectionBudget)
    physicalRepairQuotientEquivArity.symm

theorem physicalRepairObservationQuotient_card :
    Fintype.card PhysicalRepairObservationQuotient = detectionBudget + 1 := by
  rw [Fintype.card_congr physicalRepairQuotientEquivArity]
  exact repair_arity_count detectionBudget

/-- The physical quotient and the structural cascade quotient are the same repair grammar. -/
noncomputable def physicalRepairQuotientEquivStructural :
    PhysicalRepairObservationQuotient ≃ RepairObservationQuotient :=
  physicalRepairQuotientEquivArity.trans quotientEquivRepairArity.symm

/-! ## Concrete in-repo physical scene representation -/

/-- Order arity and radial shell position are the same three-step carrier. -/
def repairArityEquivTorusShell :
    RepairArity detectionBudget ≃ TorusShell :=
  (Equiv.refl (RepairArity detectionBudget)).trans
    torusShellEquivShell3.symm

/-- The derived structural repair quotient mapped to the actual in-repo shell carrier. -/
def repairQuotientEquivTorusShell :
    RepairObservationQuotient ≃ TorusShell :=
  quotientEquivRepairArity.trans repairArityEquivTorusShell

/-- SceneCandidate carried by the concrete TorusShell physical scene. -/
noncomputable def torusShellScene : SceneCandidate :=
  ⟨Fintype.card TorusShell,
    Fintype.card_pos_iff.mpr ⟨TorusShell.innerD9⟩⟩

/-- **Concrete faithful scene representation**, no longer an external application assumption. -/
noncomputable def torusShellSceneRepresentation :
    FaithfulRepairSceneRepresentation
      torusShellScene RepairObservationQuotient where
  repairToZone :=
    (repairQuotientEquivTorusShell.trans
      (Fintype.equivFin TorusShell)).toEmbedding
  zoneToRepair :=
    (repairQuotientEquivTorusShell.trans
      (Fintype.equivFin TorusShell)).symm.toEmbedding

/-- The physical shell scene has the quotient-forced zone count. -/
theorem torusShellScene_zoneCount :
    torusShellScene.zoneCount = 3 :=
  faithful_scene_zoneCount torusShellScene torusShellSceneRepresentation

/-- Exact physical interpretation: support arity `0/1/2` maps to inner/core/outer shell. -/
theorem repair_arity_shell_mapping :
    repairArityEquivTorusShell (0 : RepairArity detectionBudget) =
        TorusShell.innerD9
      ∧ repairArityEquivTorusShell (1 : RepairArity detectionBudget) =
        TorusShell.coreD11
      ∧ repairArityEquivTorusShell (2 : RepairArity detectionBudget) =
        TorusShell.outerD13 := by
  exact ⟨rfl, rfl, rfl⟩

/-- Zone-size readout transported from the actual physical shell attachment. -/
def repairClassZoneSize (q : RepairObservationQuotient) : ℕ :=
  (repairQuotientEquivTorusShell q).zoneSize

/-- The carried repair classes acquire the ordered physical sizes through support arity and radial
position, not through a count-only inference. -/
theorem carried_repair_zone_sizes :
    repairClassZoneSize (repairClass discComparison) = 9
      ∧ repairClassZoneSize (repairClass discOneLoop) = 11
      ∧ repairClassZoneSize (repairClass discOrderMemory) = 13 := by
  refine ⟨?_, ?_, ?_⟩ <;>
    simp [repairClassZoneSize, repairQuotientEquivTorusShell,
      quotientEquivRepairArity, repairQuotientEquivDatumKind,
      repairArityEquivDatumKind, repairArityEquivTorusShell,
      repairClass, repairClassKind, kindToArity, arityToKind,
      kindOf, discComparison, discOneLoop, discOrderMemory,
      torusShellEquivShell3, TorusShell.ofShell3, TorusShell.zoneSize]

/-- **Independent size selector composed with the repair scene.** The capacity defects
`|ABCD|` and `qT` uniquely reconstruct the centered scene; the repair-to-shell interpretation
realises that unique triple. The sizes are therefore not inferred from `zoneCount = 3`. -/
theorem repair_scene_sizes_selected_independently :
    (repairClassZoneSize (repairClass discComparison),
      repairClassZoneSize (repairClass discOneLoop),
      repairClassZoneSize (repairClass discOrderMemory)) = (9, 11, 13)
      ∧ ∀ m d : ℤ, 0 ≤ d →
        3 * m ^ 2 - centeredEdges m d = (Fintype.card D0.Role : ℤ) →
        m ^ 3 - centeredTriangles m d = (D0.qT : ℤ) →
        (m - d, m, m + d) = ((9 : ℤ), 11, 13) := by
  exact ⟨by simpa using carried_repair_zone_sizes,
    capacity_defects_reconstruct_scene⟩

/-- Capstone: physical repair grammar completeness from actual two-sided comparison support,
equivalence with the structural quotient, and concrete faithful representation in the in-repo
TorusShell scene. -/
theorem concrete_independent_detection_repair_semantics :
    Fintype.card InputSide = detectionBudget
      ∧ comparisonRepairArity zeroArityComparison = 0
      ∧ comparisonRepairArity oneArityComparison = 1
      ∧ comparisonRepairArity twoArityComparison = 2
      ∧ Nonempty
        (PhysicalRepairObservationQuotient ≃ RepairObservationQuotient)
      ∧ Nonempty
        (FaithfulRepairSceneRepresentation
          torusShellScene RepairObservationQuotient)
      ∧ torusShellScene.zoneCount = 3
      ∧ (repairClassZoneSize (repairClass discComparison),
          repairClassZoneSize (repairClass discOneLoop),
          repairClassZoneSize (repairClass discOrderMemory)) = (9, 11, 13) :=
  ⟨by decide,
   zeroArity_value,
   oneArity_value,
   twoArity_value,
   ⟨physicalRepairQuotientEquivStructural⟩,
   ⟨torusShellSceneRepresentation⟩,
   torusShellScene_zoneCount,
   repair_scene_sizes_selected_independently.1⟩

end D0.Foundation.ConcreteIndependentDetectionRepairSemantics
