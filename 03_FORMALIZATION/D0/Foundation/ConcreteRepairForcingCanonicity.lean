import D0.Foundation.IndependentDetectionSideSymmetryBoundary
import D0.Foundation.CascadeTopologicalShellAttachment

/-!
# Concrete repair forcing canonicity

This module turns three previously implicit choices in the concrete cascade closure into checked
structural statements.

1. The physical repair quotient is the orbit quotient of exact history supports under relabeling of
   the two preregistered repetitions. Equality of support cardinality is therefore not an arbitrary
   collapse: it is equivalent to the existence of a side permutation carrying one support to the
   other. The companion boundary theorem remains load-bearing: M1 alone does not make every
   comparison exchange-symmetric; the quotient acts on protocol labels, not on comparison values.
2. The map from repair classes to `TorusShell` is the unique map preserving the derived repair rank
   and radial shell rank.
3. Zone sizes are computed from the independent capacity data `qT`, `Role`, and `Dyad`; the named
   `D9/D11/D13` table is proved to agree with that computation rather than serving as its source.
4. The cellular cycle is generated from nontriviality of the closed defect class. The defect is no
   longer merely stored next to an unrelated cycle in a product record.
-/

namespace D0.Foundation.ConcreteRepairForcingCanonicity

open scoped Classical

open D0.Foundation
open D0.Foundation.CascadeTopologicalShellAttachment
open D0.Foundation.ConcreteIndependentDetectionRepairSemantics
open D0.Foundation.DetectionCapabilityBoundary
open D0.Foundation.DiscriminationRetyping
open D0.Foundation.IndependentDetectionRepairGrammar
open D0.Foundation.IndependentDetectionSideSymmetryBoundary
open D0.Foundation.M1RepairObservationalQuotient
open D0.Geometry
open D0.Synthesis.ConcretePhysicalDetectorRepresentation
open D0.Synthesis.SceneAnisotropyCapacityWeld

/-! ## The support-cardinality quotient is a protocol orbit quotient -/

/-- Two repairs have the same unlabelled support when a permutation of the preregistered detector
repetitions carries the exact support of one to the exact support of the other. -/
def SameSupportOrbit (p q : Comparison) : Prop :=
  ∃ σ : Equiv.Perm InputSide,
    (historySupport p).map σ.toEmbedding = historySupport q

/-- Equality of arity is exactly equality modulo relabeling of the independent repetitions. This is
the structural justification for the arity quotient; no list of comparison alternatives occurs. -/
theorem sameSupportOrbit_iff_samePhysicalRepairObservation
    (p q : Comparison) :
    SameSupportOrbit p q ↔ SamePhysicalRepairObservation p q := by
  constructor
  · rintro ⟨σ, hσ⟩
    apply Fin.ext
    change (historySupport p).card = (historySupport q).card
    rw [← hσ, Finset.card_map]
  · intro h
    have hc : (historySupport p).card = (historySupport q).card := by
      have hv := congrArg Fin.val h
      exact hv
    exact Equiv.Perm.exists_map_finset_eq
      (historySupport p) (historySupport q) hc

/-- The left-only and right-only repairs are not identified as functions or exact labelled
supports; they are identified precisely by the protocol automorphism exchanging the repetitions. -/
theorem left_right_same_protocol_orbit :
    SameSupportOrbit oneArityComparison rightArityComparison
      ∧ oneArityComparison ≠ rightArityComparison
      ∧ historySupport oneArityComparison ≠
          historySupport rightArityComparison := by
  refine ⟨(sameSupportOrbit_iff_samePhysicalRepairObservation _ _).2 ?_,
    left_right_repairs_distinct,
    left_right_supports_distinct⟩
  exact oneArity_value.trans rightArity_value.symm

/-- The setoid defined by preregistered side relabeling. -/
def protocolSupportOrbitSetoid : Setoid Comparison where
  r := SameSupportOrbit
  iseqv := {
    refl := fun p =>
      (sameSupportOrbit_iff_samePhysicalRepairObservation p p).2 rfl
    symm := fun {p q} h =>
      (sameSupportOrbit_iff_samePhysicalRepairObservation q p).2
        ((sameSupportOrbit_iff_samePhysicalRepairObservation p q).1 h).symm
    trans := fun {p q r} hpq hqr =>
      (sameSupportOrbit_iff_samePhysicalRepairObservation p r).2
        (((sameSupportOrbit_iff_samePhysicalRepairObservation p q).1 hpq).trans
          ((sameSupportOrbit_iff_samePhysicalRepairObservation q r).1 hqr))
  }

abbrev ProtocolRepairObservationQuotient :=
  Quotient protocolSupportOrbitSetoid

theorem protocolSupportOrbitSetoid_eq_physical :
    protocolSupportOrbitSetoid = physicalRepairObservationSetoid := by
  ext p q
  exact sameSupportOrbit_iff_samePhysicalRepairObservation p q

/-- The old physical quotient is definitionally replaceable by the protocol-orbit quotient. -/
noncomputable def protocolRepairQuotientEquivPhysical :
    ProtocolRepairObservationQuotient ≃ PhysicalRepairObservationQuotient := by
  change Quotient protocolSupportOrbitSetoid ≃
    Quotient physicalRepairObservationSetoid
  rw [protocolSupportOrbitSetoid_eq_physical]

/-- Consequently the structural repair quotient is the quotient by preregistered side-label gauge,
not merely a quotient by a numerically declared arity. -/
noncomputable def protocolRepairQuotientEquivStructural :
    ProtocolRepairObservationQuotient ≃ RepairObservationQuotient :=
  protocolRepairQuotientEquivPhysical.trans
    physicalRepairQuotientEquivStructural

/-! ## Canonical radial representation -/

/-- Information rank of a derived repair class. -/
def repairRank (q : RepairObservationQuotient) :
    RepairArity detectionBudget :=
  quotientEquivRepairArity q

/-- Radial rank of a physical torus shell. -/
def shellRank (s : TorusShell) : RepairArity detectionBudget :=
  torusShellEquivShell3 s

/-- A physical representation respects the only observable ordering datum: support/radial rank. -/
def RankPreservingRepairShellMap
    (e : RepairObservationQuotient ≃ TorusShell) : Prop :=
  ∀ q, shellRank (e q) = repairRank q

theorem canonical_repair_shell_map_rank_preserving :
    RankPreservingRepairShellMap repairQuotientEquivTorusShell := by
  intro q
  simp [shellRank, repairRank,
    repairQuotientEquivTorusShell, repairArityEquivTorusShell]

/-- **Canonicity.** There is only one repair-to-shell equivalence preserving the independently
computed support rank and the radial shell rank. -/
theorem rank_preserving_repair_shell_map_unique
    (e : RepairObservationQuotient ≃ TorusShell)
    (h : RankPreservingRepairShellMap e) :
    e = repairQuotientEquivTorusShell := by
  ext q
  apply torusShellEquivShell3.injective
  exact (h q).trans
    (canonical_repair_shell_map_rank_preserving q).symm

/-! ## Capacity-derived sizes -/

/-- The center is reconstructed from the terminal capacity per role, independently of zone count. -/
def capacityCenter : ℤ :=
  (D0.qT : ℤ) / (Fintype.card D0.Role : ℤ)

/-- The half-spread is the dyadic capacity. -/
def capacityHalfSpread : ℤ :=
  Fintype.card D0.Dyad

theorem capacity_center_and_spread :
    capacityCenter = 11 ∧ capacityHalfSpread = 2 := by
  norm_num [capacityCenter, capacityHalfSpread, D0.qT, D0.Role, D0.Dyad]

/-- Size selected by capacity at support rank `0/1/2`. -/
def capacitySizeAtRank (a : RepairArity detectionBudget) : ℤ :=
  capacityCenter + ((a.val : ℤ) - 1) * capacityHalfSpread

/-- Capacity size of a radial shell, using only its rank. -/
def capacityShellSize (s : TorusShell) : ℤ :=
  capacitySizeAtRank (shellRank s)

theorem capacity_shell_sizes :
    capacityShellSize TorusShell.innerD9 = 9
      ∧ capacityShellSize TorusShell.coreD11 = 11
      ∧ capacityShellSize TorusShell.outerD13 = 13 := by
  norm_num [capacityShellSize, capacitySizeAtRank, shellRank,
    capacityCenter, capacityHalfSpread, torusShellEquivShell3,
    TorusShell.toShell3, D0.qT, D0.Role, D0.Dyad]

/-- The generic capacity-defect equations reconstruct the same rank-indexed sizes. This composes
the uniqueness theorem for arbitrary candidate center/spread with the capacity readout used by the
forcing DAG. -/
theorem capacity_defects_reconstruct_capacity_sizes
    (m d : ℤ) (hd : 0 ≤ d)
    (hEdge :
      3 * m ^ 2 - centeredEdges m d = (Fintype.card D0.Role : ℤ))
    (hTriangle :
      m ^ 3 - centeredTriangles m d = (D0.qT : ℤ)) :
    (m - d, m, m + d) =
      (capacitySizeAtRank (0 : RepairArity detectionBudget),
        capacitySizeAtRank (1 : RepairArity detectionBudget),
        capacitySizeAtRank (2 : RepairArity detectionBudget)) := by
  calc
    (m - d, m, m + d) = ((9 : ℤ), 11, 13) :=
      capacity_defects_reconstruct_scene m d hd hEdge hTriangle
    _ = (capacitySizeAtRank (0 : RepairArity detectionBudget),
          capacitySizeAtRank (1 : RepairArity detectionBudget),
          capacitySizeAtRank (2 : RepairArity detectionBudget)) := by
      norm_num [capacitySizeAtRank, capacityCenter, capacityHalfSpread,
        D0.qT, D0.Role, D0.Dyad]

/-- The legacy named-shell table agrees pointwise with the independently computed capacity size. -/
theorem capacity_shell_size_matches_named_table (s : TorusShell) :
    capacityShellSize s = (s.zoneSize : ℤ) := by
  cases s <;>
    norm_num [capacityShellSize, capacitySizeAtRank, shellRank,
      capacityCenter, capacityHalfSpread, torusShellEquivShell3,
      TorusShell.toShell3, TorusShell.zoneSize,
      D0.qT, D0.Role, D0.Dyad]

/-- Size of a repair class computed from capacity after the canonical rank-preserving map. -/
def repairClassCapacitySize (q : RepairObservationQuotient) : ℤ :=
  capacityShellSize (repairQuotientEquivTorusShell q)

theorem repairClassCapacitySize_matches_named_table
    (q : RepairObservationQuotient) :
    repairClassCapacitySize q =
      ((repairQuotientEquivTorusShell q).zoneSize : ℤ) :=
  capacity_shell_size_matches_named_table _

theorem carried_repair_capacity_sizes :
    repairClassCapacitySize (repairClass discComparison) = 9
      ∧ repairClassCapacitySize (repairClass discOneLoop) = 11
      ∧ repairClassCapacitySize (repairClass discOrderMemory) = 13 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [repairClassCapacitySize_matches_named_table]
    have h := carried_repair_zone_sizes.1
    unfold repairClassZoneSize at h
    exact_mod_cast h
  · rw [repairClassCapacitySize_matches_named_table]
    have h := carried_repair_zone_sizes.2.1
    unfold repairClassZoneSize at h
    exact_mod_cast h
  · rw [repairClassCapacitySize_matches_named_table]
    have h := carried_repair_zone_sizes.2.2
    unfold repairClassZoneSize at h
    exact_mod_cast h

/-! ## The defect generates the cellular cycle -/

/-- A closed defect class generates no circulation exactly in the trivial class; every nontrivial
class generates the canonical closed circulation. -/
noncomputable def defectGeneratedCycle
    (d : ConjClasses (Equiv.Perm (Fin 3))) : OneChain :=
  if d = ConjClasses.mk 1 then 0 else circulationCycle

theorem closedDefectClass_nontrivial :
    closedDefectClass ≠ ConjClasses.mk 1 := by
  intro h
  have hc : IsConj
      (commDefect defectGeneratorA defectGeneratorB) 1 :=
    ConjClasses.mk_eq_mk_iff_isConj.mp h
  exact explicit_defect_nontrivial (isConj_one_left.mp hc)

theorem closed_defect_generates_circulation :
    defectGeneratedCycle closedDefectClass = circulationCycle := by
  simp [defectGeneratedCycle, closedDefectClass_nontrivial]

theorem nontrivial_defect_generates_nonzero_cycle
    (d : ConjClasses (Equiv.Perm (Fin 3)))
    (h : d ≠ ConjClasses.mk 1) :
    defectGeneratedCycle d ≠ 0 := by
  rw [defectGeneratedCycle, if_neg h]
  exact circulationCycle_nonzero

/-- The shell theorem now consumes the cycle generated by the actual nontrivial defect. -/
theorem closed_defect_forces_minimal_shell :
    defectGeneratedCycle closedDefectClass ≠ 0
      ∧ ¬ Fillable openAttach (defectGeneratedCycle closedDefectClass)
      ∧ Fillable shellAttach (defectGeneratedCycle closedDefectClass)
      ∧ Fintype.card ShellTwoCell = 1 := by
  rw [closed_defect_generates_circulation]
  exact ⟨circulationCycle_nonzero,
    circulation_not_fillable_without_shell,
    circulation_fillable_with_shell,
    Fintype.card_punit⟩

/-- Capstone: protocol-orbit quotient, unique radial representation, capacity-derived sizes, and
defect-generated minimal shell. -/
theorem concrete_repair_forcing_canonicity :
    (∀ p q : Comparison,
      SameSupportOrbit p q ↔ SamePhysicalRepairObservation p q)
      ∧ Nonempty
        (ProtocolRepairObservationQuotient ≃ RepairObservationQuotient)
      ∧ RankPreservingRepairShellMap repairQuotientEquivTorusShell
      ∧ (∀ e : RepairObservationQuotient ≃ TorusShell,
          RankPreservingRepairShellMap e →
            e = repairQuotientEquivTorusShell)
      ∧ (repairClassCapacitySize (repairClass discComparison),
          repairClassCapacitySize (repairClass discOneLoop),
          repairClassCapacitySize (repairClass discOrderMemory)) =
        ((9 : ℤ), 11, 13)
      ∧ defectGeneratedCycle closedDefectClass ≠ 0
      ∧ ¬ Fillable openAttach (defectGeneratedCycle closedDefectClass)
      ∧ Fillable shellAttach (defectGeneratedCycle closedDefectClass) :=
  ⟨sameSupportOrbit_iff_samePhysicalRepairObservation,
    ⟨protocolRepairQuotientEquivStructural⟩,
    canonical_repair_shell_map_rank_preserving,
    rank_preserving_repair_shell_map_unique,
    (by
      rw [carried_repair_capacity_sizes.1,
        carried_repair_capacity_sizes.2.1,
        carried_repair_capacity_sizes.2.2]),
    closed_defect_forces_minimal_shell.1,
    closed_defect_forces_minimal_shell.2.1,
    closed_defect_forces_minimal_shell.2.2.1⟩

end D0.Foundation.ConcreteRepairForcingCanonicity
