import Mathlib.Tactic

/-!
# D0-COMPACTNESS-LIMIT-001 — causal-threshold compactness `C_max = 3/8` (algebra)

Python certificate: `05_CERTS/vp_gravastar_compactness.py`.

External anchor: the horizonless gravastar (Jampolski-Rezzolla, PRD 113 L121502, 2026).
Reading the horizon as D0's capacity-saturated measurement seam, the seam closes at the
causal-threshold compactness. Eliminating the orbit angles from the three closure
conditions (photon `χ₂=θ⋆`, OS junction `2C=sin²χ₂`, cycle `cosθ⋆=4C−1`) gives the master
equation `2C = 8C − 16C²`, i.e. `16C² − 6C = 0`, whose only roots are `C = 0` and
`C = 3/8`.  This module proves that root computation exactly over `ℚ`.

The structural reading `3/8 = rank/|Ω₈|` (rank = 3 spatial transport, `|Ω₈| = 8`) is the
NAMED GAP that keeps the claim at LEM, not THE: the bridge "rank-3 transport = the causal
light-cone on the 3-sphere seam" is postulated, not derived from M1 (see the cert and
T1.4). The algebra below is exact; only that identification is open.
-/

namespace D0.Gravity

/-- **Master-equation roots.** The causal-threshold compactness satisfies
`16C² − 6C = 0`, whose only solutions over `ℚ` are `C = 0` (trivial) and `C = 3/8`. -/
theorem compactness_master_roots (C : ℚ) :
    16 * C ^ 2 - 6 * C = 0 ↔ (C = 0 ∨ C = 3 / 8) := by
  constructor
  · intro h
    have he : 16 * C ^ 2 - 6 * C = 2 * (C * (8 * C - 3)) := by ring
    rw [he] at h
    have hf : C * (8 * C - 3) = 0 := by linarith
    rcases mul_eq_zero.mp hf with h0 | h1
    · exact Or.inl h0
    · exact Or.inr (by linarith)
  · rintro (rfl | rfl) <;> norm_num

/-- `C_max = 3/8` is a genuine (nontrivial) root of the master equation. -/
theorem compactness_threshold : 16 * (3 / 8 : ℚ) ^ 2 - 6 * (3 / 8 : ℚ) = 0 := by norm_num

/-- The threshold angle data is consistent: `cos θ⋆ = 4C − 1 = 1/2` at `C = 3/8`, so
`sin²θ⋆ = 3/4 = 2C` (the OS closure). -/
theorem compactness_angle_consistency :
    (4 * (3 / 8 : ℚ) - 1 = 1 / 2) ∧ (1 - (1 / 2 : ℚ) ^ 2 = 2 * (3 / 8)) := by
  norm_num

/-- **Structural reading.** `C_max = 3/8 = rank/|Ω₈|` with `rank = 3`, `|Ω₈| = 2³ = 8`.
(The identification of this ratio with the causal cone is the named gap; here we only
record the arithmetic `3/8 = 3/8` against the role-octet denominator.) -/
theorem compactness_rank_over_omega8 :
    (3 / 8 : ℚ) = (3 : ℚ) / (2 ^ 3 : ℚ) := by norm_num

/-- **D0-COMPACTNESS-LIMIT-001 (algebra).** The causal-threshold compactness is exactly
`3/8`: it is the unique nontrivial root of the seam master equation, with consistent
angle data and the `rank/|Ω₈|` structural form. -/
theorem compactness_limit :
    (∀ C : ℚ, 16 * C ^ 2 - 6 * C = 0 ↔ (C = 0 ∨ C = 3 / 8)) ∧
    16 * (3 / 8 : ℚ) ^ 2 - 6 * (3 / 8 : ℚ) = 0 ∧
    (3 / 8 : ℚ) = (3 : ℚ) / (2 ^ 3 : ℚ) :=
  ⟨compactness_master_roots, compactness_threshold, compactness_rank_over_omega8⟩

end D0.Gravity
