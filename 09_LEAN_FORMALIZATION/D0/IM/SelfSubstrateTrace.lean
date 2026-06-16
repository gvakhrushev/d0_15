import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Tactic

/-!
# D0-IM-001 — self-substrate trace principle (background-free measurement)

BOOK_01/06. Python certificate: `05_CERTS/vp_self_substrate_trace_principle.py`.

Measurement/registration needs NO external background. An internal orthogonal map `U` splits a state by
an internal projector pair (retained sector `P`, trace sector `Q = I−P`); total norm is conserved
exactly, and the intensity deposited into the trace sector is the feedback expectation. For the cert's
explicit state `ψ = (1,2,0,0)` the retained/trace norms are `5c²` / `5s²`, so conservation is
`5 = 5c² + 5s²` whenever `c² + s² = 1`. The internal detector node is genuinely populated: at the
representative angle `θ = π/5` one has `c = cos(π/5) = φ/2`, giving `s² = (5−√5)/8 > 0`.

This module machine-checks that finite algebra. The "no external background / observer-collapse rejected"
readings (the cert's FAIL_* controls) are interpretive and stay in the cert.
-/

namespace D0.IM

open D0

/-- Retained (archive-sector) norm-squared for `ψ = (1,2,0,0)`: `‖P U P ψ‖² = 5c²`. -/
def sstRetainedNormSq (c : ℝ) : ℝ := 5 * c ^ 2

/-- Trace (feedback-sector) norm-squared for `ψ = (1,2,0,0)`: `‖Q U P ψ‖² = 5s²`. -/
def sstTraceNormSq (s : ℝ) : ℝ := 5 * s ^ 2

/-- Total substrate norm-squared `‖ψ‖² = 1² + 2² = 5`. -/
def sstTotalNormSq : ℝ := 5

/-- **Total substrate norm conservation:** for any orthogonal block (`c² + s² = 1`),
`‖ψ‖² = ‖retained‖² + ‖trace‖²`, i.e. `5 = 5c² + 5s²`. -/
theorem sst_norm_conservation (c s : ℝ) (hU : c ^ 2 + s ^ 2 = 1) :
    sstTotalNormSq = sstRetainedNormSq c + sstTraceNormSq s := by
  unfold sstTotalNormSq sstRetainedNormSq sstTraceNormSq
  linear_combination (-5 : ℝ) * hU

/-- At `θ = π/5`, `c = φ/2` gives `c² = (3+√5)/8`. -/
theorem sst_cos_sq : (phi / 2) ^ 2 = (3 + Real.sqrt 5) / 8 := by
  unfold phi; linear_combination (1 / 16 : ℝ) * sqrt_five_sq

/-- The internal projector node Pythagorean identity at `θ = π/5`: `c² + s² = 1` with
`c² = (3+√5)/8`, `s² = (5−√5)/8`. -/
theorem sst_pythagorean_at_phi : (3 + Real.sqrt 5) / 8 + (5 - Real.sqrt 5) / 8 = 1 := by
  ring

/-- **Detector node genuinely populated:** the trace-sector norm `s² = (5−√5)/8 > 0` (since `√5 < 5`),
so registration always leaves an internal trace. -/
theorem sst_detector_populated : (0 : ℝ) < (5 - Real.sqrt 5) / 8 := by
  linarith [sqrt_five_lt_three]

/-- **D0-IM-001.** Substrate norm is conserved for every orthogonal block; the `θ=π/5` node has
`c² = (3+√5)/8`, `c²+s² = 1`, and a strictly positive trace sector `s² = (5−√5)/8 > 0`. -/
theorem self_substrate_trace_principle_cert :
    (∀ c s : ℝ, c ^ 2 + s ^ 2 = 1 →
      sstTotalNormSq = sstRetainedNormSq c + sstTraceNormSq s) ∧
    (phi / 2) ^ 2 = (3 + Real.sqrt 5) / 8 ∧
    (3 + Real.sqrt 5) / 8 + (5 - Real.sqrt 5) / 8 = 1 ∧
    (0 : ℝ) < (5 - Real.sqrt 5) / 8 :=
  ⟨fun c s hU => sst_norm_conservation c s hU, sst_cos_sq, sst_pythagorean_at_phi,
   sst_detector_populated⟩

end D0.IM
