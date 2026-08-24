import Mathlib.Tactic
import D0.Core.DyadFringeBridge

/-!
# D0-DYAD-SUBENSEMBLES-001 — subensemble calculus: erasers, delayed choice, weak reads

Two explanation-bricks for existing laboratory situations, derived inside the dyad house
(zero quantum postulates beyond the owned primitives):

**1. Mixtures stay in the house (weak reads).**  A statistical `w`-mixture of admissible dyad
records is again an admissible record, and the complementarity bound applies to it directly.
Mechanism: the determinant of the mixture decomposes into weighted determinants plus a cross
term, and the cross term is nonnegative by Cauchy–Schwarz — each record's own positivity
supplies exactly what is needed.  Consequence: an INCOMPLETE readout — one whose coupling never
completes a registration — can distribute apparent path-knowledge and visibility across
conditional subensembles, yet NO single record ever leaves the bound.  Weak-measurement
trajectories coexist with fringes without paradox.

**2. Eraser identity (delayed choice).**  `antiPhase` swaps the branches and negates the
coherence — the anti-fringed partner.  Mixing a record with its anti-partner at weight `w`
yields visibility `|2w − 1|·V(ρ)`; the balanced choice `w = 1/2` ERASES the fringes completely.
And the scanned intensity is LINEAR in the record: `I(mix, φ) = w·I(ρ, φ) + (1−w)·I(σ, φ)` —
the unconditional pattern is fixed by bookkeeping alone, so making the choice before or after
the crossing changes nothing backward.  No retrocausality is available in the house, as a
theorem.

Honest scope: proved for two-branch records in real symmetric storage; physical readings
(weak-measurement ensembles, interferometric erasing) inherit the apparatus bridge of
`D0-DYAD-FRINGE-BRIDGE-001`.  Characterization of WHEN the mixed bound saturates (extreme-point
analysis) is queued, not claimed here.
-/

namespace D0

/-! ### Component facts -/

/-- Positivity as a quadratic form: the determinant condition makes the branch quadratic form
    nonnegative everywhere. -/
theorem dyad_qf_nonneg (ρ : DyadState) (x y : ℝ) :
    ρ.r11 * (x * x) + 2 * ρ.r12 * x * y + ρ.r22 * (y * y) ≥ 0 := by
  have hr11nn : 0 ≤ ρ.r11 := by
    by_contra hc
    push_neg at hc
    have hr22pos : (0 : ℝ) < ρ.r22 := by linarith [ρ.htrace]
    nlinarith [ρ.hpsd, sq_nonneg ρ.r12]
  rcases eq_or_lt_of_le hr11nn with hzz | hp
  · have hcabs : |ρ.r12| ≤ 0 := by
      have hdet := ρ.hpsd
      have hmul : ρ.r11 * ρ.r22 ≤ 0 := by
        rw [← hzz]
        simp
      have hsqr : |ρ.r12| ^ 2 = ρ.r12 ^ 2 := sq_abs _
      nlinarith [hdet, hmul, hsqr, sq_nonneg |ρ.r12|]
    have hc0 : ρ.r12 = 0 := by
      have heq : |ρ.r12| = 0 := le_antisymm hcabs (abs_nonneg ρ.r12)
      exact abs_eq_zero.mp heq
    have hr22pos : (0 : ℝ) < ρ.r22 := by linarith [ρ.htrace, hzz]
    have hzz' : ρ.r11 = 0 := hzz.symm
    have hq0 : ρ.r11 * (x * x) + 2 * ρ.r12 * x * y + ρ.r22 * (y * y)
        = ρ.r22 * (y * y) := by
      rw [hzz', hc0]
      simp only [zero_mul, zero_add, mul_zero]
    rw [hq0]
    exact mul_nonneg hr22pos.le (by nlinarith [sq_nonneg y])
  · have hcomplete :
        (ρ.r11 * x + ρ.r12 * y) ^ 2
          + (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) * (y * y)
          = ρ.r11 * (ρ.r11 * (x * x) + 2 * ρ.r12 * x * y + ρ.r22 * (y * y)) := by
      ring
    have hs1 : 0 ≤ (ρ.r11 * x + ρ.r12 * y) ^ 2 :=
      by nlinarith [hp, sq_nonneg (ρ.r11 * x + ρ.r12 * y)]
    have hs2 : 0 ≤ (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) * (y * y) :=
      by nlinarith [ρ.hpsd, sq_nonneg y]
    have hprod : 0 ≤ ρ.r11 * (ρ.r11 * (x * x) + 2 * ρ.r12 * x * y + ρ.r22 * (y * y)) := by
      rw [← hcomplete]
      linarith
    rcases lt_or_ge (ρ.r11 * (x * x) + 2 * ρ.r12 * x * y + ρ.r22 * (y * y)) 0 with hn | hp2
    · exact absurd hn (by nlinarith [hprod, hp])
    · exact hp2

/-- Branch weight 1 of any admissible record is nonnegative. -/
theorem r11_nonneg (ρ : DyadState) : 0 ≤ ρ.r11 := by
  have h := dyad_qf_nonneg ρ 1 0
  simpa using h

/-- Branch weight 2 of any admissible record is nonnegative. -/
theorem r22_nonneg (ρ : DyadState) : 0 ≤ ρ.r22 := by
  have h := dyad_qf_nonneg ρ 0 1
  simpa using h

/-- **Cauchy–Schwarz for two admissible records:** `a1·b2 + a2·b1 ≥ 2·c1·c2`. -/
theorem cross_nonneg (ρ σ : DyadState) :
    0 ≤ ρ.r11 * σ.r22 + σ.r11 * ρ.r22 - 2 * (ρ.r12 * σ.r12) := by
  set X := ρ.r11 * σ.r22 with hX
  set Y := σ.r11 * ρ.r22 with hY
  set Z := ρ.r12 * σ.r12 with hZ
  have hXnn : 0 ≤ X := mul_nonneg (r11_nonneg ρ) (r22_nonneg σ)
  have hYnn : 0 ≤ Y := mul_nonneg (r11_nonneg σ) (r22_nonneg ρ)
  have hc1le : ρ.r12 ^ 2 ≤ ρ.r11 * ρ.r22 := by linarith [ρ.hpsd]
  have hc2le : σ.r12 ^ 2 ≤ σ.r11 * σ.r22 := by linarith [σ.hpsd]
  have hAB1 : 0 ≤ ρ.r11 * ρ.r22 := by nlinarith [sq_nonneg ρ.r12]
  have hAB2 : 0 ≤ σ.r11 * σ.r22 := by nlinarith [sq_nonneg σ.r12]
  have hc2nn : 0 ≤ σ.r12 ^ 2 := sq_nonneg σ.r12
  have hZ2 : Z * Z ≤ X * Y := by
    calc Z * Z = ρ.r12 ^ 2 * σ.r12 ^ 2 := by ring
      _ ≤ (ρ.r11 * ρ.r22) * σ.r12 ^ 2 := mul_le_mul_of_nonneg_right hc1le hc2nn
      _ ≤ (ρ.r11 * ρ.r22) * (σ.r11 * σ.r22) := mul_le_mul_of_nonneg_left hc2le hAB1
      _ = X * Y := by ring
  have hface : (X + Y - 2 * Z) * (X + Y + 2 * Z)
      = (X - Y) ^ 2 + 4 * (X * Y - Z * Z) := by ring
  have hface_nn : 0 ≤ (X + Y - 2 * Z) * (X + Y + 2 * Z) := by
    rw [hface]
    nlinarith
  rcases lt_or_ge Z 0 with hzn | hzp
  · linarith
  · have hsum : 0 ≤ X + Y + 2 * Z := by linarith
    rcases lt_or_ge (X + Y + 2 * Z) 0 with hn2 | hp
    · have hz0 : X + Y + 2 * Z = 0 := le_antisymm (le_of_lt hn2) hsum
      have hx0 : X = 0 := by linarith
      have hy0 : Y = 0 := by linarith
      have hz00 : Z = 0 := by linarith
      linarith
    · nlinarith [hface_nn, hp]

/-! ### Mixtures -/

/-- **Mixture existence.**  For `0 ≤ w ≤ 1` the entrywise `w`-mixture of two admissible records
    is again an admissible record, with exactly the expected entries. -/
theorem mix_admissible (w : ℝ) (hw : 0 ≤ w) (hw1 : w ≤ 1) (ρ σ : DyadState) :
    ∃ μ : DyadState,
      μ.r11 = w * ρ.r11 + (1 - w) * σ.r11
        ∧ μ.r22 = w * ρ.r22 + (1 - w) * σ.r22
        ∧ μ.r12 = w * ρ.r12 + (1 - w) * σ.r12 := by
  refine ⟨⟨w * ρ.r11 + (1 - w) * σ.r11,
            w * ρ.r22 + (1 - w) * σ.r22,
            w * ρ.r12 + (1 - w) * σ.r12,
            by
              have h1 := ρ.htrace
              have h2 := σ.htrace
              have e1 : w * (ρ.r11 + ρ.r22) = w := by rw [h1]; ring
              have e2 : (1 - w) * (σ.r11 + σ.r22) = 1 - w := by rw [h2]; ring
              have e3 : w * ρ.r11 + (1 - w) * σ.r11
                  + (w * ρ.r22 + (1 - w) * σ.r22)
                  = w * (ρ.r11 + ρ.r22) + (1 - w) * (σ.r11 + σ.r22) := by ring
              rw [e3, e1, e2]
              ring,
            ?_⟩,
          rfl, rfl, rfl⟩
  have hexpand :
      (w * ρ.r11 + (1 - w) * σ.r11) * (w * ρ.r22 + (1 - w) * σ.r22)
          - (w * ρ.r12 + (1 - w) * σ.r12) ^ 2
        = w ^ 2 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2)
          + (1 - w) ^ 2 * (σ.r11 * σ.r22 - σ.r12 ^ 2)
          + w * (1 - w) * (ρ.r11 * σ.r22 + σ.r11 * ρ.r22 - 2 * (ρ.r12 * σ.r12)) := by
    ring
  have hw2nn : 0 ≤ w ^ 2 := by nlinarith [hw]
  have hww1nn : 0 ≤ (1 - w) ^ 2 := by nlinarith [hw1]
  have hw01nn : 0 ≤ w * (1 - w) := by nlinarith [hw, hw1]
  rw [hexpand]
  have p1 : 0 ≤ w ^ 2 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) := mul_nonneg hw2nn ρ.hpsd
  have p2 : 0 ≤ (1 - w) ^ 2 * (σ.r11 * σ.r22 - σ.r12 ^ 2) := mul_nonneg hww1nn σ.hpsd
  have p3 : 0 ≤ w * (1 - w) * (ρ.r11 * σ.r22 + σ.r11 * ρ.r22 - 2 * (ρ.r12 * σ.r12)) :=
    mul_nonneg hw01nn (cross_nonneg ρ σ)
  linarith

/-- Anti-fringed partner: branches swapped, coherence sign flipped. -/
noncomputable def antiPhase (ρ : DyadState) : DyadState :=
  ⟨ρ.r22, ρ.r11, -ρ.r12, by linarith [ρ.htrace], by
    rw [mul_comm ρ.r22 ρ.r11, neg_sq]
    exact ρ.hpsd⟩

/-! ### Eraser identity and no-retro bookkeeping -/

/-- **Eraser identity.**  Mixing a record with its anti-partner at weight `w` scales the
    visibility by exactly `|2w − 1|`; at `w = 1/2` the fringes erase completely. -/
theorem eraser_identity (w : ℝ) (hw : 0 ≤ w) (hw1 : w ≤ 1) (ρ : DyadState) :
    ∃ μ : DyadState,
      μ.r12 = (2 * w - 1) * ρ.r12
        ∧ visibility μ = |2 * w - 1| * visibility ρ := by
  obtain ⟨μ, _, _, h12⟩ := mix_admissible w hw hw1 ρ (antiPhase ρ)
  have h12anti : μ.r12 = (2 * w - 1) * ρ.r12 := by
    rw [h12]
    unfold antiPhase
    ring
  refine ⟨μ, h12anti, ?_⟩
  unfold visibility
  rw [h12anti, abs_mul]
  ring

/-- **No-retro bookkeeping.**  The scanned intensity is linear in the record: the unconditional
    pattern of a mixture is the weighted pattern — regardless of when the choice is made. -/
theorem phaseIntensity_mix (w : ℝ) (hw : 0 ≤ w) (hw1 : w ≤ 1) (ρ σ : DyadState) (φ : ℝ) :
    ∃ μ : DyadState,
      (μ.r11 = w * ρ.r11 + (1 - w) * σ.r11 ∧ μ.r12 = w * ρ.r12 + (1 - w) * σ.r12) ∧
      phaseIntensity μ φ = w * phaseIntensity ρ φ + (1 - w) * phaseIntensity σ φ := by
  obtain ⟨μ, h11, h22, h12⟩ := mix_admissible w hw hw1 ρ σ
  refine ⟨μ, ⟨h11, h12⟩, ?_⟩
  unfold phaseIntensity
  rw [h12]
  ring

/-! ### Capstone -/

/-- **D0-DYAD-SUBENSEMBLES-001 (capstone).**  Mixtures of admissible records stay inside the
    house and obey the complementarity bound (weak reads are safe); mixing with the
    anti-phased partner scales visibility by |2w−1| and erases it at balance (eraser /
    delayed choice); the unconditional intensity is linear in the records, so delayed choice
    has no backward reach. -/
theorem DYAD_SUBENSEMBLES_PROVED :
    (∀ w : ℝ, 0 ≤ w → w ≤ 1 → ∀ ρ σ : DyadState,
        ∃ μ : DyadState,
          μ.r11 = w * ρ.r11 + (1 - w) * σ.r11
            ∧ μ.r22 = w * ρ.r22 + (1 - w) * σ.r22
            ∧ μ.r12 = w * ρ.r12 + (1 - w) * σ.r12
            ∧ distinguishability μ ^ 2 + visibility μ ^ 2 ≤ 1) ∧
    (∀ w : ℝ, 0 ≤ w → w ≤ 1 → ∀ ρ : DyadState,
        ∃ μ : DyadState,
          μ.r12 = (2 * w - 1) * ρ.r12 ∧ visibility μ = |2 * w - 1| * visibility ρ) ∧
    (∀ w : ℝ, 0 ≤ w → w ≤ 1 → ∀ ρ σ : DyadState, ∀ φ : ℝ,
        ∃ μ : DyadState,
          phaseIntensity μ φ = w * phaseIntensity ρ φ + (1 - w) * phaseIntensity σ φ) := by
  refine ⟨?_, ?_, ?_⟩
  · intro w hw hw1 ρ σ
    obtain ⟨μ, h11, h22, h12⟩ := mix_admissible w hw hw1 ρ σ
    refine ⟨μ, h11, h22, h12, ?_⟩
    have hb := dyad_complementarity_bound μ
    unfold distinguishability visibility at hb ⊢
    rw [h11, h22, h12] at hb ⊢
    exact hb
  · intro w hw hw1 ρ
    exact eraser_identity w hw hw1 ρ
  · intro w hw hw1 ρ σ φ
    obtain ⟨μ, ⟨_, h12⟩, hI⟩ := phaseIntensity_mix w hw hw1 ρ σ φ
    exact ⟨μ, hI⟩

end D0
