import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-JONES-INDEX-PHI-001 — φ is the n=5 Jones index value (Lean algebraic core)

Python certificate: `05_CERTS/vp_jones_index_phi_finite.py` (the trig series `4cos²(π/n)`,
n=3..6 = 1,2,φ²,3, is verified numerically there).

Jones' subfactor index theorem (Invent. Math. 72, 1983) quantizes the index of a type-II₁
subfactor: in `[1,4)` the only admissible values are `{4cos²(π/n) : n=3,4,5,…}`. The n=5 slot
is `4cos²(π/5) = (3+√5)/2 = φ²` — the squared Fibonacci quantum dimension `d_τ = φ`. This
module closes the **algebraic core** with no floating point, reusing the frozen `D0.Core.Phi`:

  * `(3+√5)/2 = φ²`               (the n=5 value is exactly φ²);
  * `φ² = φ + 1`                  (the Fibonacci fusion relation `τ⊗τ = 1 ⊕ τ`, `d_τ = φ`).

The trig identity `4cos²(π/5) = (3+√5)/2` (via `cos(π/5) = (1+√5)/4`) is not available as a
Mathlib lemma in this pin, so it is verified numerically in the cert; the algebraic value
`(3+√5)/2 = φ²` is closed here. The Jones quantization OBSTRUCTION (no index in `(1,4)` other
than the series) is the external owner `ASSUMP-JONES-INDEX`; it is not re-proved.
-/

namespace D0.Claims

open D0

/-- The n=5 Jones index value `(3+√5)/2` equals `φ²` (exact; reuses `D0.Core.Phi`). -/
theorem jones_index_n5_value : (3 + Real.sqrt 5) / 2 = phi ^ 2 := by
  unfold phi
  nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]

/-- The Fibonacci quantum dimension `d_τ = φ` satisfies the fusion relation `d_τ² = d_τ + 1`
(`τ⊗τ = 1 ⊕ τ`). This is exactly `phi_sq`. -/
theorem fib_quantum_dim_fusion : phi ^ 2 = phi + 1 := phi_sq

/-- So the n=5 Jones index value is `φ + 1 = (3+√5)/2`. -/
theorem jones_index_n5_eq_phi_add_one : (3 + Real.sqrt 5) / 2 = phi + 1 := by
  rw [jones_index_n5_value]; exact phi_sq

/-- **D0-JONES-INDEX-PHI-001.** The Jones index value forced at slot n=5 of the quantized
series is the golden number `φ² = φ + 1 = (3+√5)/2` — the squared Fibonacci quantum dimension.
The quantization OBSTRUCTION (no index in `(1,4)` other than `4cos²(π/n)`) is the external
owner `ASSUMP-JONES-INDEX`; here the n=5 value is closed exactly. -/
theorem jones_index_phi :
    (3 + Real.sqrt 5) / 2 = phi ^ 2 ∧ phi ^ 2 = phi + 1 :=
  ⟨jones_index_n5_value, phi_sq⟩

end D0.Claims
