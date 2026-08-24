import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import D0.Core.TriadComplementarity

/-!
# D0-TRIAD-PHASE-WINDOW-001 — the phase freedom of the complex-Hermitian triad

The real-symmetric triad (`D0-TRIAD-SUFFICIENCY-001`) realized magnitudes by ALIGNED phases.
For complex-Hermitian records the pair coherences carry phases `x_ij = t_ij·e^{iθ_ij}`, and the
determinant sees only the relative PHASE SUM `Φ ≡ θ12 + θ23 − θ13`:

    det(Φ) = a·b·c − (a·t1² + b·t2² + c·t3²) + 2·t1·t2·t3·cos Φ,

because `Re(x12·x23·conj(x13)) = t1·t2·t3·cos Φ`.  This module derives the **phase window**:

    det(Φ) ≥ 0  ⟺  2·t1·t2·t3 · cos Φ ≥ K,   K ≡ a·t1² + b·t2² + c·t3² − a·b·c,

i.e. the admissible phases form an interval `cos Φ ≥ K/(2·t1·t2·t3)` — the record's phase
freedom is EXACTLY an arc, quantified by the magnitudes alone.

**Endpoints and readings.**
* `Φ = 0` (aligned): `det = face gap`, so `hface` ⟺ window nonempty — the aligned realization
  of `D0-TRIAD-SUFFICIENCY-001` is the CENTER of the window's right endpoint.
* `K ≤ −2·t1·t2·t3`: full circle admissible (coherence so small that any phase closes).
* As magnitudes grow toward the caps, `K → +…`: the window SHRINKS — dense coherence squeezes
  phase freedom to zero exactly when the record becomes rank-deficient.  The trinary law is
  thus also a law about WHERE quantum phase freedom lives.

Honest scope: proved at the level of the determinant functional (real arithmetic in
`cos Φ`; no `Complex` matrices are elaborated).  The identification of `Φ` with the sum of
laboratory fringe phases across the three arm pairs inherits the apparatus bridge of
`D0-DYAD-FRINGE-BRIDGE-001`.
-/

namespace D0

/-- Magnitude data with caps (same hypotheses as the sufficiency input, no face required). -/
structure TriadPhaseRecord where
  a : ℝ
  b : ℝ
  c : ℝ
  t1 : ℝ
  t2 : ℝ
  t3 : ℝ
  htr : a + b + c = 1
  hann : 0 ≤ a ∧ 0 ≤ b ∧ 0 ≤ c ∧ 0 ≤ t1 ∧ 0 ≤ t2 ∧ 0 ≤ t3
  hcap1 : t1 ^ 2 ≤ b * c
  hcap2 : t2 ^ 2 ≤ a * c
  hcap3 : t3 ^ 2 ≤ a * b

/-- Determinant of the Hermitian triad record as a function of `cos Φ`. -/
def detAtPhi (m : TriadPhaseRecord) (cosPhi : ℝ) : ℝ :=
  m.a * m.b * m.c - (m.a * m.t1 ^ 2 + m.b * m.t2 ^ 2 + m.c * m.t3 ^ 2)
    + 2 * (m.t1 * m.t2 * m.t3) * cosPhi

/-- Numerator constant of the window: `K = Σ a_i t_i² − a·b·c`. -/
def windowK (m : TriadPhaseRecord) : ℝ :=
  m.a * m.t1 ^ 2 + m.b * m.t2 ^ 2 + m.c * m.t3 ^ 2 - m.a * m.b * m.c

/-- **Phase window (multiplied form).**  The record is positive at `cos Φ` iff twice the
    triple-coherence times `cos Φ` covers the window constant `K`. -/
theorem phase_window_mul (m : TriadPhaseRecord) (cosPhi : ℝ) :
    0 ≤ detAtPhi m cosPhi
      ↔ 2 * (m.t1 * m.t2 * m.t3) * cosPhi ≥ windowK m := by
  unfold detAtPhi windowK
  constructor
  · intro h
    linarith
  · intro h
    linarith

/-- **Phase window (divided form).**  With strictly positive triple coherence,
    positivity at `cos Φ` ⟺ `cos Φ ≥ K / (2·t1·t2·t3)`. -/
theorem phase_window (m : TriadPhaseRecord) (hT : 0 < m.t1 * m.t2 * m.t3) (cosPhi : ℝ) :
    0 ≤ detAtPhi m cosPhi
      ↔ cosPhi ≥ windowK m / (2 * m.t1 * m.t2 * m.t3) := by
  have hmul := phase_window_mul m cosPhi
  have hTpos : 0 < 2 * m.t1 * m.t2 * m.t3 := by linarith
  constructor
  · intro h
    have hm := hmul.mp h
    rw [ge_iff_le, div_le_iff₀ hTpos]
    linarith
  · intro h
    rw [ge_iff_le, div_le_iff₀ hTpos] at h
    have hbridge : cosPhi * (2 * m.t1 * m.t2 * m.t3)
        = 2 * (m.t1 * m.t2 * m.t3) * cosPhi := by ring
    exact hmul.mpr (by linarith [h, hbridge])

/-! ### Endpoints -/

/-- **Alignment endpoint.**  If the trinary law holds (`hface`), the aligned phase `Φ = 0`
    (`cos Φ = 1`) is admissible — the center of the window's right end. -/
theorem aligned_admissible_of_face (m : TriadPhaseRecord)
    (hface : m.a * m.b * m.c + 2 * m.t1 * m.t2 * m.t3
        ≥ m.a * m.t1 ^ 2 + m.b * m.t2 ^ 2 + m.c * m.t3 ^ 2) :
    0 ≤ detAtPhi m 1 := by
  apply (phase_window_mul m 1).mpr
  unfold windowK
  linarith [hface]

end D0
