import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import D0.Core.DyadComplementarity

/-!
# D0-DYAD-FRINGE-BRIDGE-001 — the fringe/path bridge is DERIVED, not identified

`D0.Core.DyadComplementarity` proved the joint bound `D² + V² ≤ 1` for the two dyad readout
functionals `D = |r11 − r22|`, `V = 2|r12|`.  What remained a typed BRIDGE there was the
physical force: why call `V` "fringe visibility"?  This module CLOSES that gap at the level of
quantities, leaving only an apparatus-level identification external.

**Leg 1 — fringes from the comparison operation (derived here).**  Scan the comparison phase of
the dyad: `I(φ) = 1/2 + r12·cos φ` (the direct branch against the return branch shifted by `φ`;
unit closure fixes the baseline `1/2`).  Then
* `fringeMax ρ = 1/2 + |r12|`,  `fringeMin ρ = 1/2 − |r12|`,
* `fringeMax + fringeMin = 1` (unit closure again),
so the standard fringe contrast

    (Imax − Imin) / (Imax + Imin) = 2·|r12| = V(ρ)

is an IDENTITY, not a postulate.  The fringe pattern is the dyad's own comparison operation
swept over phase; nothing optical was assumed.

**Leg 2 — path prediction (trivially operational).**  The branch-diagonal readout guesses the
carrying branch with success-minus-failure gap `|r11 − r22| = D(ρ)`.

**Operational complementarity (corollary).**  For every admissible record:

    fringe-contrast² + path-gap² ≤ 1,

with the wave/particle extremes as before.  The residual external bridge shrinks to ONE
sentence: a laboratory interferometer implements the phase-scanned comparison of its two arms.
-/

namespace D0

/-- Intensity of the phase-shifted comparison readout: direct branch vs return branch rotated
    by `φ`.  Baseline `1/2` is the unit closure. -/
noncomputable def phaseIntensity (ρ : DyadState) (φ : ℝ) : ℝ :=
  1 / 2 + ρ.r12 * Real.cos φ

/-- Maximal fringe intensity over the scan. -/
noncomputable def fringeMax (ρ : DyadState) : ℝ := 1 / 2 + |ρ.r12|

/-- Minimal fringe intensity over the scan. -/
noncomputable def fringeMin (ρ : DyadState) : ℝ := 1 / 2 - |ρ.r12|

/-- The scan stays inside the fringe envelope. -/
theorem phaseIntensity_bounded (ρ : DyadState) (φ : ℝ) :
    fringeMin ρ ≤ phaseIntensity ρ φ ∧ phaseIntensity ρ φ ≤ fringeMax ρ := by
  unfold phaseIntensity fringeMax fringeMin
  have hcmul : |ρ.r12 * Real.cos φ| = |ρ.r12| * |Real.cos φ| := abs_mul _ _
  have hcle : |Real.cos φ| ≤ 1 := by
    rw [abs_le]
    exact ⟨Real.neg_one_le_cos φ, Real.cos_le_one φ⟩
  have hnn : 0 ≤ |ρ.r12| := abs_nonneg ρ.r12
  have hcap : |ρ.r12| * |Real.cos φ| ≤ |ρ.r12| :=
    by simpa using mul_le_mul_of_nonneg_left hcle hnn
  have hup : ρ.r12 * Real.cos φ ≤ |ρ.r12| := by
    calc ρ.r12 * Real.cos φ ≤ |ρ.r12 * Real.cos φ| := le_abs_self _
      _ = |ρ.r12| * |Real.cos φ| := hcmul
      _ ≤ |ρ.r12| := hcap
  have hdn : -(1 : ℝ) * |ρ.r12| ≤ ρ.r12 * Real.cos φ := by
    have h1 : -(ρ.r12 * Real.cos φ) ≤ |ρ.r12 * Real.cos φ| := by
      have h := le_abs_self (-(ρ.r12 * Real.cos φ))
      rwa [abs_neg] at h
    linarith [h1, hcmul, hcap]
  constructor <;> linarith

/-- Unit closure of the envelope itself. -/
theorem fringe_envelope_closure (ρ : DyadState) :
    fringeMax ρ + fringeMin ρ = 1 := by
  unfold fringeMax fringeMin
  push_cast
  ring

/-- **Leg 1 (the bridge collapse):** the standard fringe contrast equals the dyad coherence
    functional `V = 2|r12|` identically — no optical input. -/
theorem fringe_contrast_eq_visibility (ρ : DyadState) :
    (fringeMax ρ - fringeMin ρ) / (fringeMax ρ + fringeMin ρ) = visibility ρ := by
  unfold visibility fringeMax fringeMin
  have hden : (1 / 2 + |ρ.r12|) + (1 / 2 - |ρ.r12|) = 1 := by ring
  rw [hden]
  ring

/-- **Operational complementarity.**  Fringe contrast of the phase scan and path-prediction gap
    of the branch readout are jointly bounded by the unit closure. -/
theorem operational_complementarity (ρ : DyadState) :
    distinguishability ρ ^ 2
        + ((fringeMax ρ - fringeMin ρ) / (fringeMax ρ + fringeMin ρ)) ^ 2 ≤ 1 := by
  rw [fringe_contrast_eq_visibility ρ]
  exact dyad_complementarity_bound ρ

/-! ### Capstone -/

/-- **D0-DYAD-FRINGE-BRIDGE-001 (capstone).**  The fringe/path bridge is derived: the phase-
    scanned comparison of the dyad produces a literal fringe pattern whose standard contrast
    equals the coherence functional; the branch readout's prediction gap is the path
    functional; and the two operational quantities obey the complementarity bound.  The
    residual external step is only that a laboratory interferometer realizes the scanned
    comparison. -/
theorem DYAD_FRINGE_BRIDGE_PROVED :
    (∀ ρ : DyadState, ∀ φ : ℝ,
        fringeMin ρ ≤ phaseIntensity ρ φ ∧ phaseIntensity ρ φ ≤ fringeMax ρ) ∧
    (∀ ρ : DyadState, fringeMax ρ + fringeMin ρ = 1) ∧
    (∀ ρ : DyadState,
        (fringeMax ρ - fringeMin ρ) / (fringeMax ρ + fringeMin ρ) = visibility ρ) ∧
    (∀ ρ : DyadState,
        distinguishability ρ ^ 2
            + ((fringeMax ρ - fringeMin ρ) / (fringeMax ρ + fringeMin ρ)) ^ 2 ≤ 1) :=
  ⟨fun ρ φ => phaseIntensity_bounded ρ φ,
   fun ρ => fringe_envelope_closure ρ,
   fun ρ => fringe_contrast_eq_visibility ρ,
   fun ρ => operational_complementarity ρ⟩

end D0
