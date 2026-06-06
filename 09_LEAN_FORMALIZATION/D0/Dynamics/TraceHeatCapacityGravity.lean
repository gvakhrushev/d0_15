import D0.Dynamics.TraceHeatLucasCore
import D0.Gravity.EntropicArchiveInterface
import D0.Gravity.MacroEinsteinInterface

namespace D0.Dynamics

/-- Local finite heat/capacity record over an archive graph region. -/
structure TraceHeatCapacityRegion
    (G : D0.Gravity.FiniteArchiveGraph) where
  region : Set G.V
  scale : Rat
  localHeatContent : Rat
  heat_nonnegative : 0 <= localHeatContent

def LocalHeatContent
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) : Rat :=
  R.localHeatContent

noncomputable def BoundaryCapacityForRegion
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) : Rat :=
  D0.Gravity.BoundaryCapacity G R.region

noncomputable def TraceHeatDefect
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) (idealLucasMoment : Rat) : Rat :=
  LocalHeatContent R - idealLucasMoment

noncomputable def SaturatedRegion
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) : Prop :=
  BoundaryCapacityForRegion R <= LocalHeatContent R

noncomputable def HorizonRegion
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) : Prop :=
  LocalHeatContent R = BoundaryCapacityForRegion R

noncomputable def RequiresBoundaryEncoding
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) : Prop :=
  SaturatedRegion R

theorem boundary_capacity_is_quarter_cut_weight
    (G : D0.Gravity.FiniteArchiveGraph) (S : Set G.V) :
    D0.Gravity.BoundaryCapacity G S =
      D0.Gravity.BoundaryCutWeight G S / 4 := by
  rfl

theorem saturated_region_forces_boundary_encoding
    {G : D0.Gravity.FiniteArchiveGraph}
    {R : TraceHeatCapacityRegion G}
    (h : SaturatedRegion R) :
    RequiresBoundaryEncoding R := by
  exact h

theorem horizon_region_saturated
    {G : D0.Gravity.FiniteArchiveGraph}
    {R : TraceHeatCapacityRegion G}
    (h : HorizonRegion R) :
    SaturatedRegion R := by
  unfold HorizonRegion at h
  unfold SaturatedRegion
  rw [h]

noncomputable def BlackHoleCapacitySaturation
    {G : D0.Gravity.FiniteArchiveGraph}
    (R : TraceHeatCapacityRegion G) : Prop :=
  SaturatedRegion R

theorem black_hole_capacity_saturation_rule
    {G : D0.Gravity.FiniteArchiveGraph}
    {R : TraceHeatCapacityRegion G}
    (h : BlackHoleCapacitySaturation R) :
    RequiresBoundaryEncoding R := by
  exact h

/--
Trace/heat saturation is an admissible finite precondition for the existing
macro gravity interface; the macro tensor itself still comes from the finite
gravity witness, not from a continuum Einstein equation.
-/
theorem heat_trace_entropy_gradient_admits_gravity_interface
    (W : D0.Gravity.FiniteGravityInterfaceWitness)
    (R : TraceHeatCapacityRegion W.G)
    (_hsat : SaturatedRegion R) :
    let M := D0.Gravity.finite_gravity_witness_forces_macro_constraints W
    let EH :=
      D0.Gravity.macro_tension_yields_einstein_hilbert_interface
        M
        (D0.Gravity.finite_gravity_macro_constraints_closed W).1
        (D0.Gravity.finite_gravity_macro_constraints_closed W).2.1
        (D0.Gravity.finite_gravity_macro_constraints_closed W).2.2.1
        (D0.Gravity.finite_gravity_macro_constraints_closed W).2.2.2.1
        (D0.Gravity.finite_gravity_macro_constraints_closed W).2.2.2.2.2
    EH.symmetric /\
      EH.divergenceFree /\
      EH.secondOrder /\
      EH.ehA2Bridge /\
      EH.higherCurvatureCut /\
      EH.ttStressCoupling := by
  exact D0.Gravity.finite_gravity_witness_yields_einstein_hilbert_interface W

end D0.Dynamics
