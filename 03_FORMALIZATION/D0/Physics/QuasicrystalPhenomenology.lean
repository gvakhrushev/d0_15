import D0.Geometry.PhaseUnfoldingQuasicrystal
import D0.Condensed.CondensedPhiVacuum
import D0.Physics.QuasiGenerationsInflation
import D0.Physics.ArchivePhasonDarkMatter
import D0.Physics.WindowOffsetChirality
import D0.Physics.PhasonFlipInertia
import D0.Physics.WindowFractionalCharge

namespace D0.Physics

/-!
D0-QUASI-002: quasicrystal phenomenology operator origin.

The package records five finite readouts of the same phi-quasicrystal support:
inflation classes, archive phason strain, acceptance-window offset, phason flip
cost, and three-sector window weights.
-/

structure D0PhiCutProject where
  terminalModulus : Nat
  terminalBranches : Nat
  electroweakModulus : Nat
  electroweakDepth : Nat

def d0PhiCutProject : D0PhiCutProject where
  terminalModulus := 44
  terminalBranches := 20
  electroweakModulus := 710
  electroweakDepth := 35

theorem d0_phi_cut_project_matches_phase_unfolding :
    d0PhiCutProject.terminalModulus = 44 /\
      d0PhiCutProject.terminalBranches = 20 /\
      d0PhiCutProject.electroweakModulus = 710 /\
      d0PhiCutProject.electroweakDepth = 35 /\
      D0.Geometry.QuasicrystalOrderNotPeriodicLattice := by
  exact
    ⟨rfl, rfl, rfl, rfl,
      D0.Geometry.quasicrystal_order_not_periodic_lattice⟩

/-- The physics-facing cut-project readout is the condensed phi-vacuum support readout. -/
theorem d0_phi_cut_project_matches_condensed_phi_vacuum :
    d0PhiCutProject.terminalModulus = D0.d0CutProjectQuasicrystal.terminalModulus /\
      d0PhiCutProject.terminalBranches = D0.d0CutProjectQuasicrystal.terminalBranches /\
      d0PhiCutProject.electroweakModulus = D0.d0CutProjectQuasicrystal.electroweakModulus /\
      d0PhiCutProject.electroweakDepth = D0.d0CutProjectQuasicrystal.electroweakDepth /\
      D0.Geometry.QuasicrystalOrderNotPeriodicLattice := by
  exact ⟨rfl, rfl, rfl, rfl, D0.condensedPhiVacuum.quasicrystalSupport⟩

structure QuasicrystalPhenomenologyOperatorOrigin where
  cutProject : D0PhiCutProject
  phaseOwner : D0.Geometry.QuasicrystalOrderNotPeriodicLattice
  generations :
    Fintype.card D0GenerationCarrier = 3 /\
      Matrix.trace (D0.Dynamics.T ^ 2) = 3
  darkPhason :
    forall w : PhasonStrainField,
      0 < w.energy ->
        EMCouplingArchive w = 0 /\
          exists G : GravityCouplingArchive w, 0 < G.response
  chiralWindow : ChiralReadout unitOffsetWindow
  inertia :
    forall p : MovingDefect,
      NonzeroAcceleration p -> exists n : Nat, 0 < InertialCost p n
  fractionalCharge :
    (forall S : Finset ColorSector,
      S.card = 1 -> WindowWeight S = 1 / 3) /\
    (forall S : Finset ColorSector,
      S.card = 2 -> WindowWeight S = 2 / 3)

def quasicrystalPhenomenologyOperatorOrigin :
    QuasicrystalPhenomenologyOperatorOrigin where
  cutProject := d0PhiCutProject
  phaseOwner := D0.Geometry.quasicrystal_order_not_periodic_lattice
  generations := by
    exact
      ⟨generation_carrier_is_three_inflation_classes,
        generation_trace_layer_eq_three⟩
  darkPhason := by
    intro w hw
    exact archive_phason_strain_em_dark_metric_visible w hw
  chiralWindow := window_offset_forces_chiral_readout
  inertia := by
    intro p hp
    exact phason_flip_drag_positive_cost p hp
  fractionalCharge := by
    exact fractional_charge_window_weights

theorem quasicrystal_phenomenology_operator_origin :
    D0.Geometry.QuasicrystalOrderNotPeriodicLattice /\
      Fintype.card D0GenerationCarrier = 3 /\
      (forall w : PhasonStrainField,
        0 < w.energy ->
          EMCouplingArchive w = 0 /\
            exists G : GravityCouplingArchive w, 0 < G.response) /\
      ChiralReadout unitOffsetWindow /\
      (forall p : MovingDefect,
        NonzeroAcceleration p -> exists n : Nat, 0 < InertialCost p n) /\
      (forall S : Finset ColorSector,
        S.card = 1 -> WindowWeight S = 1 / 3) /\
      (forall S : Finset ColorSector,
        S.card = 2 -> WindowWeight S = 2 / 3) := by
  exact
    ⟨D0.Geometry.quasicrystal_order_not_periodic_lattice,
      generation_carrier_is_three_inflation_classes,
      archive_phason_strain_em_dark_metric_visible,
      window_offset_forces_chiral_readout,
      phason_flip_drag_positive_cost,
      fractional_charge_window_weights.1,
      fractional_charge_window_weights.2⟩

end D0.Physics
