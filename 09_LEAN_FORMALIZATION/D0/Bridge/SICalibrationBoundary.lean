import Mathlib.Data.Real.Basic
import D0.Traceability.StatusTaxonomy

namespace D0.Bridge

structure SpectralBridgeCoefficients where
  c0 : Real
  c2 : Real

structure CoreTraceShape where
  a0Shape : Real
  a2Shape : Real

structure CalibrationDictionary where
  coefficients : SpectralBridgeCoefficients
  status : D0.Traceability.D0Status

def calibratedActionValues
    (coeffs : SpectralBridgeCoefficients) (shape : CoreTraceShape) :
    Real × Real :=
  (coeffs.c0 * shape.a0Shape, coeffs.c2 * shape.a2Shape)

def coreTraceShapeAfterCalibration
    (_coeffs : SpectralBridgeCoefficients) (shape : CoreTraceShape) :
    CoreTraceShape :=
  shape

def siCalibrationDictionary
    (coeffs : SpectralBridgeCoefficients) : CalibrationDictionary where
  coefficients := coeffs
  status := D0.Traceability.D0Status.BRIDGE_CALIBRATION

theorem c0_c2_scale_action_values_only
    (coeffs : SpectralBridgeCoefficients) (shape : CoreTraceShape) :
    calibratedActionValues coeffs shape =
      (coeffs.c0 * shape.a0Shape, coeffs.c2 * shape.a2Shape) := by
  rfl

theorem c0_c2_cannot_alter_a0_a2_trace_shapes
    (coeffs : SpectralBridgeCoefficients) (shape : CoreTraceShape) :
    coreTraceShapeAfterCalibration coeffs shape = shape := by
  rfl

theorem si_calibration_belongs_to_bridge_calibration_status
    (coeffs : SpectralBridgeCoefficients) :
    (siCalibrationDictionary coeffs).status =
      D0.Traceability.D0Status.BRIDGE_CALIBRATION := by
  rfl

theorem si_calibration_cannot_promote_to_core_closed :
    ¬ D0.Traceability.canPromoteTo
      D0.Traceability.D0Status.BRIDGE_CALIBRATION
      D0.Traceability.D0Status.CORE_CLOSED := by
  unfold D0.Traceability.canPromoteTo
  intro h
  exact h

end D0.Bridge
