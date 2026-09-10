import D0.Integration.V15.RawZone

/-!
Finite algebra for the PRL comparison draft, 2026-09-05.
Imports the existing RawZone owner. This file does not assert that the new
continuous flow is the physical D0 clock, or reconstruct all quantum systems.
Analytic speed inequalities and the complex-state interpretation are in README.md.
-/

namespace D0.Research.PRL20260905

open Matrix
open D0.Integration.V15

def K : Matrix (Fin 3) (Fin 3) ℚ := RawZone.comm.map (fun z : ℤ => (z : ℚ))

/-- Columns are q=(0,1,2) and Kq. -/
def X : Matrix (Fin 3) (Fin 2) ℚ := !![0, 126; 1, 52; 2, -22]

def B : Matrix (Fin 2) (Fin 2) ℚ := !![0, -2840; 1, 0]

theorem columns_from_source :
    K.mulVec ![0, 1, 2] = ![126, 52, -22] := by native_decide

theorem active_plane_invariant : K * X = X * B := by native_decide

theorem active_plane_metric :
    Xᵀ * RawZone.Gq * X = (!![63, 0; 0, 178920] : Matrix (Fin 2) (Fin 2) ℚ) := by
  native_decide

theorem source_projectors_are_polynomials :
    RawZone.Pact = (-1 / 2840 : ℚ) • (K * K) ∧
    RawZone.P0 = (1 : Matrix (Fin 3) (Fin 3) ℚ) + (1 / 2840 : ℚ) • (K * K) := by
  native_decide

theorem active_and_neutral_on_plane : RawZone.Pact * X = X ∧ RawZone.P0 * X = 0 := by
  native_decide

theorem generator_projector_algebra :
    K * RawZone.Pact = K ∧ RawZone.Pact * K = K ∧
    K * RawZone.P0 = 0 ∧ RawZone.P0 * K = 0 ∧
    RawZone.Pact * RawZone.P0 = 0 ∧ RawZone.P0 * RawZone.Pact = 0 := by
  native_decide

/-- The default Euclidean metric would give the wrong adjoint. -/
theorem ordinary_metric_fails : Kᵀ + K ≠ 0 := by native_decide

end D0.Research.PRL20260905
