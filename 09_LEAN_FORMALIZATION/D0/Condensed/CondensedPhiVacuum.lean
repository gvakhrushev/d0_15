import D0.Condensed.OperatorNaturality
import D0.Geometry.PhaseUnfoldingQuasicrystal

namespace D0

/-!
Condensed/profinite phi-vacuum support for the finite cut-and-project layer.

The module is deliberately finite: it records the terminal and electroweak
return quotients as a projective readout support, then ties that support to the
already proved information-quasicrystal phase owner.
-/

/-- Two finite return stages used by the phi-vacuum support. -/
inductive PhiVacuumStage where
  | terminal
  | electroweak
  deriving DecidableEq, Repr, Fintype

/-- Return modulus visible at each phi-vacuum stage. -/
def PhiVacuumStage.modulus : PhiVacuumStage -> Nat
  | .terminal => 44
  | .electroweak => 710

/-- Branch count visible at each phi-vacuum stage. -/
def PhiVacuumStage.branches : PhiVacuumStage -> Nat
  | .terminal => 20
  | .electroweak => 280

/-- Depth after the eight-role electroweak quotient where applicable. -/
def PhiVacuumStage.depth : PhiVacuumStage -> Nat
  | .terminal => 20
  | .electroweak => 35

/-- Finite stage cardinality of the condensed phi-vacuum stage carrier. -/
theorem phi_vacuum_stage_card_eq_two :
    Fintype.card PhiVacuumStage = 2 := by
  native_decide

/-- Condensed phi-vacuum support as finite return quotient data. -/
structure CondensedPhiVacuum where
  quasicrystalSupport : D0.Geometry.QuasicrystalOrderNotPeriodicLattice
  terminalModulus : D0.qT = 44
  terminalBranches : Nat.totient D0.qT = 20
  electroweakModulus : D0.qEW = 710
  electroweakBranches : Nat.totient D0.qEW = 280
  electroweakDepth : D0.DEW = 35

/-- Concrete condensed phi-vacuum support. -/
def condensedPhiVacuum : CondensedPhiVacuum where
  quasicrystalSupport := D0.Geometry.quasicrystal_order_not_periodic_lattice
  terminalModulus := D0.lcm_abcd_v11
  terminalBranches := D0.Geometry.terminal_return_branch_count
  electroweakModulus := D0.qEW_forced
  electroweakBranches := D0.Geometry.electroweak_return_branch_count
  electroweakDepth := D0.Geometry.electroweak_return_depth_eq_35

/-- Finite cut-and-project quasicrystal readout over the condensed phi-vacuum. -/
structure CutProjectQuasicrystal where
  vacuum : CondensedPhiVacuum
  terminalModulus : Nat
  terminalBranches : Nat
  electroweakModulus : Nat
  electroweakBranches : Nat
  electroweakDepth : Nat

/-- Concrete D0 cut-and-project support. -/
def d0CutProjectQuasicrystal : CutProjectQuasicrystal where
  vacuum := condensedPhiVacuum
  terminalModulus := 44
  terminalBranches := 20
  electroweakModulus := 710
  electroweakBranches := 280
  electroweakDepth := 35

/-- Condensed phi-vacuum support is exactly the finite information-quasicrystal owner. -/
theorem condensed_phi_vacuum_support_closed :
    D0.Geometry.QuasicrystalOrderNotPeriodicLattice /\
      D0.qT = 44 /\
      Nat.totient D0.qT = 20 /\
      D0.qEW = 710 /\
      Nat.totient D0.qEW = 280 /\
      D0.DEW = 35 := by
  exact
    ⟨condensedPhiVacuum.quasicrystalSupport,
      condensedPhiVacuum.terminalModulus,
      condensedPhiVacuum.terminalBranches,
      condensedPhiVacuum.electroweakModulus,
      condensedPhiVacuum.electroweakBranches,
      condensedPhiVacuum.electroweakDepth⟩

/-- The finite cut-and-project object exposes the terminal and electroweak quotients. -/
theorem cut_project_quasicrystal_matches_phase_unfolding :
    d0CutProjectQuasicrystal.terminalModulus = 44 /\
      d0CutProjectQuasicrystal.terminalBranches = 20 /\
      d0CutProjectQuasicrystal.electroweakModulus = 710 /\
      d0CutProjectQuasicrystal.electroweakBranches = 280 /\
      d0CutProjectQuasicrystal.electroweakDepth = 35 /\
      D0.Geometry.QuasicrystalOrderNotPeriodicLattice := by
  exact
    ⟨rfl, rfl, rfl, rfl, rfl,
      condensedPhiVacuum.quasicrystalSupport⟩

/-- Machine-checkable condensed/cut-project closure package. -/
structure CondensedPhiVacuumCutProjectClosure where
  stage_card : Fintype.card PhiVacuumStage = 2
  vacuum_closed :
    D0.Geometry.QuasicrystalOrderNotPeriodicLattice /\
      D0.qT = 44 /\
      Nat.totient D0.qT = 20 /\
      D0.qEW = 710 /\
      Nat.totient D0.qEW = 280 /\
      D0.DEW = 35
  cut_project_closed :
    d0CutProjectQuasicrystal.terminalModulus = 44 /\
      d0CutProjectQuasicrystal.terminalBranches = 20 /\
      d0CutProjectQuasicrystal.electroweakModulus = 710 /\
      d0CutProjectQuasicrystal.electroweakBranches = 280 /\
      d0CutProjectQuasicrystal.electroweakDepth = 35 /\
      D0.Geometry.QuasicrystalOrderNotPeriodicLattice

/-- The condensed phi-vacuum and cut-project support close as one finite package. -/
def condensedPhiVacuumCutProjectClosure :
    CondensedPhiVacuumCutProjectClosure where
  stage_card := phi_vacuum_stage_card_eq_two
  vacuum_closed := condensed_phi_vacuum_support_closed
  cut_project_closed := cut_project_quasicrystal_matches_phase_unfolding

end D0
