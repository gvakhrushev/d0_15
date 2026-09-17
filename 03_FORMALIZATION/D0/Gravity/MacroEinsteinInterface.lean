import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import D0.Gravity.EntropicArchiveInterface
import D0.Geometry.FiniteSpin2WaveOperator
import D0.Geometry.HigherCurvatureSuppression
import D0.Geometry.HeatTraceA2Decomposition
import D0.Geometry.SpectralActionLadder

open scoped BigOperators

namespace D0.Gravity

/-- Finite spectral A2/EH bridge data used by the macro gravity interface. -/
structure SpectralA2EHBridgeWitness where
  N : Type
  instFintype : Fintype N
  instDecEq : DecidableEq N
  L : Matrix N N Real
  rho : N -> Real
  rho_pos : forall i, rho i > 0
  L_symmetric : forall i j, L i j = L j i

attribute [instance] SpectralA2EHBridgeWitness.instFintype
attribute [instance] SpectralA2EHBridgeWitness.instDecEq

/-- The finite A2 trace identity that supplies the EH proxy slot. -/
def SpectralA2EHBridgeClosed (B : SpectralA2EHBridgeWitness) : Prop :=
  D0.Geometry.SpectralActionLadder.spectralTracePower B.L B.rho 2 =
    D0.Geometry.HeatTraceA2Decomposition.diagonalSquareTerm B.L B.rho
      + 2 * D0.Geometry.HeatTraceA2Decomposition.discreteEHActionProxy B.L B.rho

theorem spectral_a2_eh_bridge_closed
    (B : SpectralA2EHBridgeWitness) :
    SpectralA2EHBridgeClosed B := by
  unfold SpectralA2EHBridgeClosed
  exact
    D0.Geometry.SpectralActionLadder.a2_is_eh_proxy
      B.L B.rho B.rho_pos B.L_symmetric

/-- Finite D0 data from which the macro gravity constraints are read. -/
structure FiniteGravityInterfaceWitness where
  G : FiniteArchiveGraph
  flux : ArchiveFlux G
  flux_conserved : ConservedArchiveFlux G flux
  tension : EntropicBoundaryTension G
  Lsym : D0.Geometry.SymPert4 -> D0.Geometry.SymPert4
  tt_positive : D0.Geometry.TTPositiveOperator4 Lsym
  probe : D0.Geometry.SymPert4
  spectral : SpectralA2EHBridgeWitness

/-- Macro tensor class named by the finite gravity witness. -/
structure MacroTensionTensor where
  symmetric : Prop
  divergenceFree : Prop
  secondOrder : Prop
  finiteCutCompatible : Prop
  entropicResponseNonnegative : Prop
  ehA2Bridge : Prop

/-- Build the macro constraint object from finite D0 gravity data. -/
noncomputable def finite_gravity_witness_forces_macro_constraints
    (W : FiniteGravityInterfaceWitness) :
    MacroTensionTensor :=
  { symmetric := W.probe.h.transpose = W.probe.h
    divergenceFree := ∑ i, NetFluxAt W.G W.flux i = 0
    secondOrder := D0.HigherCurvatureCutoff D0.delta0
    finiteCutCompatible :=
      D0.Geometry.IsTT4 (D0.Geometry.WTT4 W.Lsym W.probe)
    entropicResponseNonnegative :=
      0 <= EntropicTensionEnergy W.G W.tension
    ehA2Bridge := SpectralA2EHBridgeClosed W.spectral }

theorem finite_gravity_macro_constraints_closed
    (W : FiniteGravityInterfaceWitness) :
    let M := finite_gravity_witness_forces_macro_constraints W
    M.symmetric /\
      M.divergenceFree /\
      M.secondOrder /\
      M.finiteCutCompatible /\
      M.entropicResponseNonnegative /\
      M.ehA2Bridge := by
  dsimp [finite_gravity_witness_forces_macro_constraints]
  exact
    ⟨W.probe.symm,
      conserved_flux_no_creation W.G W.flux W.flux_conserved,
      D0.Geometry.HigherCurvatureSuppression.higher_curvature_terms_below_finite_readout_cut,
      D0.Geometry.WTT4_preserves_tt W.Lsym W.probe,
      entropic_tension_energy_nonnegative W.G W.tension,
      spectral_a2_eh_bridge_closed W.spectral⟩

/-- Macro EH-interface object after the finite constraints are closed. -/
structure EinsteinHilbertMacroInterface where
  symmetric : Prop
  divergenceFree : Prop
  secondOrder : Prop
  ehA2Bridge : Prop
  higherCurvatureCut : Prop
  ttStressCoupling : Prop

/-- Promote an already closed macro tensor to the EH-interface class. -/
def macro_tension_yields_einstein_hilbert_interface
    (M : MacroTensionTensor)
    (_h_symm : M.symmetric)
    (_h_div : M.divergenceFree)
    (_h_second : M.secondOrder)
    (_h_cut : M.finiteCutCompatible)
    (_h_eh : M.ehA2Bridge) :
    EinsteinHilbertMacroInterface :=
  { symmetric := M.symmetric
    divergenceFree := M.divergenceFree
    secondOrder := M.secondOrder
    ehA2Bridge := M.ehA2Bridge
    higherCurvatureCut := M.secondOrder
    ttStressCoupling := M.finiteCutCompatible }

theorem macro_tension_einstein_hilbert_interface_closed
    (M : MacroTensionTensor)
    (h_symm : M.symmetric)
    (h_div : M.divergenceFree)
    (h_second : M.secondOrder)
    (h_cut : M.finiteCutCompatible)
    (h_eh : M.ehA2Bridge) :
    let EH :=
      macro_tension_yields_einstein_hilbert_interface
        M h_symm h_div h_second h_cut h_eh
    EH.symmetric /\
      EH.divergenceFree /\
      EH.secondOrder /\
      EH.ehA2Bridge /\
      EH.higherCurvatureCut /\
      EH.ttStressCoupling := by
  dsimp [macro_tension_yields_einstein_hilbert_interface]
  exact ⟨h_symm, h_div, h_second, h_eh, h_second, h_cut⟩

theorem finite_gravity_witness_yields_einstein_hilbert_interface
    (W : FiniteGravityInterfaceWitness) :
    let M := finite_gravity_witness_forces_macro_constraints W
    let EH :=
      macro_tension_yields_einstein_hilbert_interface
        M
        (finite_gravity_macro_constraints_closed W).1
        (finite_gravity_macro_constraints_closed W).2.1
        (finite_gravity_macro_constraints_closed W).2.2.1
        (finite_gravity_macro_constraints_closed W).2.2.2.1
        (finite_gravity_macro_constraints_closed W).2.2.2.2.2
    EH.symmetric /\
      EH.divergenceFree /\
      EH.secondOrder /\
      EH.ehA2Bridge /\
      EH.higherCurvatureCut /\
      EH.ttStressCoupling := by
  dsimp
  exact
    macro_tension_einstein_hilbert_interface_closed
      (finite_gravity_witness_forces_macro_constraints W)
      (finite_gravity_macro_constraints_closed W).1
      (finite_gravity_macro_constraints_closed W).2.1
      (finite_gravity_macro_constraints_closed W).2.2.1
      (finite_gravity_macro_constraints_closed W).2.2.2.1
      (finite_gravity_macro_constraints_closed W).2.2.2.2.2

end D0.Gravity
