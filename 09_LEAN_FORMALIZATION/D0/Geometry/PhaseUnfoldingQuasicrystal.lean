import D0.Dynamics.ToralAutomorphism
import D0.Geometry.HurwitzRigidPhaseGenerator
import D0.Geometry.PhaseReturnBranchCount

namespace D0.Geometry

/-!
Information-quasicrystal integration layer for D0 phase unfolding.

The object is finite, ordered and aperiodic: toral time supplies the ordered
runtime, `alphaD0 = phi^-2` blocks rational phase locking, and finite return
moduli expose detector-visible branch counts.
-/

/-- Stable branch coherence is finite return arithmetic plus a non-periodic phase generator. -/
def StableLongRangeReturnStructure : Prop :=
  NonPeriodicPhase D0.alphaD0 /\
    D0.qT = 44 /\
      D0.d13 = 20 /\
        D0.qEW = 710 /\
          D0.DEW = 35

/-- A periodic lattice lock is represented by a rational phase generator. -/
def PeriodicLatticeLock (alpha : Real) : Prop :=
  ¬ NonPeriodicPhase alpha

/-- D0 phase-unfolding order: coherent finite branches without periodic lattice locking. -/
def QuasicrystalOrderNotPeriodicLattice : Prop :=
  StableLongRangeReturnStructure /\ ¬ PeriodicLatticeLock D0.alphaD0

/-- Ordered runtime supplied by the finite toral time automorphism. -/
def ToralOrderedRuntime : Prop :=
  Matrix.trace (D0.Dynamics.T ^ 2) = 3 /\
    Matrix.trace (D0.Dynamics.T ^ 3) = -4 /\
      Matrix.trace (D0.Dynamics.T ^ 5) = -11

/--
The D0 time automorphism supplies an ordered runtime while the phase owner
keeps the visible return structure non-periodic.
-/
theorem toral_runtime_supplies_quasicrystal_order :
    ToralOrderedRuntime /\
      StableLongRangeReturnStructure := by
  refine ⟨?_, ?_⟩
  · exact D0.Dynamics.trace_evolution_unfolds_d0_geometry
  · unfold StableLongRangeReturnStructure
    exact
      ⟨phi_phase_is_nonperiodic,
        D0.lcm_abcd_v11,
        D0.d13_from_return_window,
        D0.qEW_forced,
        D0.ew_depth_from_omega8⟩

/--
Finite phase order has branch coherence without translational period: the D0
phase is irrational and the visible arms appear only through finite return
quotients.
-/
theorem quasicrystal_order_not_periodic_lattice :
    QuasicrystalOrderNotPeriodicLattice := by
  unfold QuasicrystalOrderNotPeriodicLattice PeriodicLatticeLock
  constructor
  · exact (toral_runtime_supplies_quasicrystal_order).2
  · intro h
    exact h phi_phase_is_nonperiodic

/-- Integrated information-quasicrystal closure package. -/
structure PhaseUnfoldingQuasicrystalClosure where
  phase_nonperiodic : NonPeriodicPhase D0.alphaD0
  finite_return_branches : FiniteReturnModulusBranchCount
  quasicrystal_not_lattice : QuasicrystalOrderNotPeriodicLattice

def phaseUnfoldingQuasicrystalClosure :
    PhaseUnfoldingQuasicrystalClosure where
  phase_nonperiodic := phi_phase_is_nonperiodic
  finite_return_branches := finite_return_modulus_unfolds_branches
  quasicrystal_not_lattice := quasicrystal_order_not_periodic_lattice

end D0.Geometry
