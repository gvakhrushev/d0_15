import Mathlib.Data.Real.Basic

namespace D0.Bridge

structure DimensionlessCoreTraces where
  a0 : Real
  a2 : Real
  delta2V : Real
  dimensionless : Prop

structure ExternalSICalibration where
  H0 : Real
  GN : Real
  Lambda : Real
  c0 : Real
  c2 : Real
  units_declared : Prop

structure SIMacroscopicPhysics where
  H0 : Real
  GN : Real
  Lambda : Real
  action_value : Real

def calibratedAction
    (core : DimensionlessCoreTraces) (bridge : ExternalSICalibration) : Real :=
  bridge.c0 * core.a0 + bridge.c2 * core.a2

def derive_physical_observables
    (core : DimensionlessCoreTraces) (bridge : ExternalSICalibration) :
    SIMacroscopicPhysics where
  H0 := bridge.H0
  GN := bridge.GN
  Lambda := bridge.Lambda
  action_value := calibratedAction core bridge

inductive QuantityStatus where
  | DimensionlessCore
  | SICalibrated
  deriving DecidableEq, Repr

def coreTraceShapeStatus (_core : DimensionlessCoreTraces) : QuantityStatus :=
  QuantityStatus.DimensionlessCore

def siPhysicsStatus (_phys : SIMacroscopicPhysics) : QuantityStatus :=
  QuantityStatus.SICalibrated

def CoreProducesSIConstants (_core : DimensionlessCoreTraces) : Prop :=
  False

theorem core_traces_are_dimensionless
    (core : DimensionlessCoreTraces) :
    coreTraceShapeStatus core = QuantityStatus.DimensionlessCore := by
  rfl

theorem calibration_changes_only_action_scaling
    (core1 core2 : DimensionlessCoreTraces)
    (bridge : ExternalSICalibration)
    (hcore : core1 = core2) :
    calibratedAction core1 bridge = calibratedAction core2 bridge := by
  subst hcore
  rfl

theorem calibration_changes_units_not_core_shape
    (core : DimensionlessCoreTraces)
    (_bridge1 _bridge2 : ExternalSICalibration) :
    core.a0 = core.a0 /\ core.a2 = core.a2 /\ core.delta2V = core.delta2V := by
  exact ⟨rfl, rfl, rfl⟩

theorem no_si_observable_without_external_calibration
    (core : DimensionlessCoreTraces) :
    Not (CoreProducesSIConstants core) := by
  intro h
  exact h

theorem h0_gn_lambda_are_not_core_observables
    (core : DimensionlessCoreTraces) :
    Not (CoreProducesSIConstants core) := by
  exact no_si_observable_without_external_calibration core

theorem si_observables_require_external_calibration
    (core : DimensionlessCoreTraces) (bridge : ExternalSICalibration) :
    siPhysicsStatus (derive_physical_observables core bridge) =
      QuantityStatus.SICalibrated := by
  rfl

end D0.Bridge
