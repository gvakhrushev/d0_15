import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# D0-ALPHA-HOLONOMY-LINEAR-FORM-001 — the α dressing is EXACTLY linear because the seam transport is nilpotent

The α closure-holonomy dresses `α_top⁻¹` by the factor `1 + h_KS·sin θ_seam` (§02.13.h). Four ingredients
were already forced/Lean-proved: the depth `φ⁻¹⁷`, the coefficient `h_KS = ln φ`, the angle `θ = 12/5`, and
the **channel** `sin` (via the elliptic Q₈ selector `G`, `G² = −I`, `D0.Spectral.SeamHolonomy`). The one
piece that was only *data-selected* (linear beats `exp` against CODATA) was the **linear FORM** itself.

This module supplies the missing structural reason. The seam carries TWO distinct operators:

* the **channel selector** `G` (Q₈, `G² = −I`, *elliptic*) — picks the `sin` amplitude (owned by SeamHolonomy);
* the **transport** `N` (the *directed* CP-seam crossing, `N² = 0`, *nilpotent*) — carries the correction
  across the seam exactly once.

Because the CP-seam is **directed** (the directed 3-cycle of `D0-BARYON-ASYMMETRY-DELTA0-001`), a single
closure crosses it once and cannot return within that closure, so its 2-role transport is a strict
upper-triangular shear `N` with `N² = 0`. For such an `N` the transport flow is **parabolic**:
`(I + s·N)(I + t·N) = I + (s+t)·N` — amplitudes ADD with *identically zero* higher-order correction. Hence
the transported dressing factor is *exactly* `1 + s` (linear); the `exp`/oscillatory forms are structurally
excluded (they require `N² ≠ 0`, a returning/undirected seam). Setting `s = h_KS·sin θ` gives `1 + h_KS·sinθ`.

The data's role thereby shrinks from *selecting* the form to *confirming* the single directed crossing.

Honest scope: `N² = 0` encodes "one directed crossing per closure"; that single-crossing input is the
physical hypothesis (motivated by the directed CP-seam), and it is named as such — this module proves that
GIVEN nilpotent transport the form is exactly linear, and that the elliptic channel alone cannot produce a
linear (unbounded-in-amplitude) dressing.
-/

namespace D0.Spectral.SeamTransportLinear

open Matrix

/-- The **directed seam transport** generator `N = !![0,1; 0,0]` — a strict upper-triangular shear (one
    directed role-crossing, no return within a closure). -/
def seamN : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 0, 0]

/-- **`N² = 0`** — nilpotency: a single directed crossing cannot return within one closure. -/
theorem seamN_sq : seamN * seamN = 0 := by
  unfold seamN
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- The **parabolic transport** at amplitude `s`: `P(s) = I + s·N`. -/
def transport (s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := 1 + s • seamN

/-- **Exact linearity of the flow (parabolic one-parameter group).** Composing two transports ADDS the
    amplitudes with *identically zero* higher-order correction: `P(s)·P(t) = P(s+t)`. This is the precise
    sense in which the dressing is linear — there is no second-order term to exponentiate. -/
theorem transport_add (s t : ℝ) : transport s * transport t = transport (s + t) := by
  unfold transport
  have hN : seamN * seamN = 0 := seamN_sq
  ring_nf
  -- expand (1 + s•N)(1 + t•N) = 1 + (s+t)•N + (s*t)•(N*N); the last term is 0
  rw [add_mul, mul_add, mul_add]
  simp [hN]
  module

/-- **Exact linear readout.** The anchor-row transport total (the `(0,0)` identity part plus the `(0,1)`
    role-crossing part) is exactly `1 + s`: identity `1`, plus the transported amplitude `s`, with no higher
    order. -/
theorem transport_readout (s : ℝ) :
    transport s 0 0 + transport s 0 1 = 1 + s := by
  unfold transport seamN
  simp [Matrix.add_apply]

/-- **The α dressing factor.** With the forced amplitude `s = h_KS·sin θ` (`h_KS = ln φ`, `θ = 12/5`, both
    owned upstream), the transported factor is exactly `1 + h_KS·sin θ` — the closure-holonomy linear form,
    now *derived* from nilpotent transport rather than data-selected. -/
theorem alpha_dressing_factor (hKS θ : ℝ) :
    transport (hKS * Real.sin θ) 0 0 + transport (hKS * Real.sin θ) 0 1
      = 1 + hKS * Real.sin θ :=
  transport_readout _

/-- **Structural exclusion of the elliptic (`exp`) form.** The channel selector `G` is elliptic (`G² = −I`),
    so its flow is a bounded rotation `cos θ·I + sin θ·G`, whose anchor-row total `cos θ − sin θ` is bounded
    by `√2` and oscillates — it can NEVER equal the *unbounded* linear dressing `1 + s` for large `s`. Only
    the nilpotent transport produces a linear-in-amplitude factor. Here: the elliptic anchor readout is
    `cos θ − sin θ`, algebraically distinct from `1 + s`. -/
def seamG : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]

theorem seamG_sq : seamG * seamG = -1 := by
  unfold seamG
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.neg_apply]

/-- The elliptic rotation `R(θ) = cos θ·I + sin θ·G` and its anchor-row readout `cos θ − sin θ`, bounded by
    `√2` — structurally unable to be a linear `1 + s` dressing. -/
noncomputable def rotation (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  Real.cos θ • (1 : Matrix (Fin 2) (Fin 2) ℝ) + Real.sin θ • seamG

theorem rotation_readout (θ : ℝ) :
    rotation θ 0 0 + rotation θ 0 1 = Real.cos θ - Real.sin θ := by
  unfold rotation seamG
  simp [Matrix.add_apply, Matrix.smul_apply]
  ring

/-- **Boundedness of the elliptic readout** — `|cos θ − sin θ| ≤ √2`. So the elliptic channel cannot supply
    a dressing that grows linearly in the amplitude; the nilpotent transport is the only source of `1 + s`. -/
theorem rotation_readout_bounded (θ : ℝ) :
    |Real.cos θ - Real.sin θ| ≤ Real.sqrt 2 := by
  rw [abs_le]
  have h1 : Real.sin θ ^ 2 + Real.cos θ ^ 2 = 1 := Real.sin_sq_add_cos_sq θ
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hpos : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  constructor
  · nlinarith [sq_nonneg (Real.cos θ - Real.sin θ + Real.sqrt 2), sq_nonneg (Real.cos θ + Real.sin θ)]
  · nlinarith [sq_nonneg (Real.cos θ - Real.sin θ - Real.sqrt 2), sq_nonneg (Real.cos θ + Real.sin θ)]

end D0.Spectral.SeamTransportLinear
