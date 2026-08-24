import Mathlib.Tactic
import D0.Core.TriadComplementarity

/-!
# D0-TRIAD-SUFFICIENCY-001 — the magnitude region is EXACTLY (caps ∧ determinant face)

The open residual of `D0-TRIAD-COMPLEMENTARITY-001`: the trinary law was proved NECESSARY
(every admissible record obeys the determinant face); whether it (with the pairwise caps) is
also SUFFICIENT for realizability stayed open.  This module closes it for real-symmetric
records, CONSTRUCTIVELY.

**Realization.**  Given branch weights `a, b, c` (unit closure, nonnegative) and pair
coherences `t1, t2, t3` (nonnegative) satisfying

* **caps:** `t1² ≤ b·c`,  `t2² ≤ a·c`,  `t3² ≤ a·b`   (the three 2×2 principal minors),
* **face:** `a·b·c + 2·t1·t2·t3 ≥ a·t1² + b·t2² + c·t3²`   (the trinary law),

the ALIGNED-PHASE record `(r12, r13, r23) = (+t3, +t2, +t1)` is admissible: every principal
minor is a cap, and the determinant is exactly the face gap.  No search over phases is needed —
the aligned choice realizes the whole region.

**Characterization (capstone).**  A magnitude six-tuple in the unit-closure simplex is
realizable by an admissible triad record  ⟺  caps ∧ face.  Necessity is
`triad_constraint` + the Sylvester minors of `TriadState`; sufficiency is the constructive
witness above.  The admissible magnitude region of the triad is therefore COMPLETELY described
by two transparent conditions — the pairwise caps and the trinary law — with nothing hidden.

Honest scope: real-symmetric records (the phase space of the complex case collapses to signs
here); the complex-Hermitian analogue (phases on the unit circle, one continuous parameter)
is queued.  Operational identification inherits the apparatus bridge of
`D0-DYAD-FRINGE-BRIDGE-001`.
-/

namespace D0

/-- Magnitude data of a triad record: three branch weights (summing to one) and three pair
    coherences, all nonnegative, subject to the pairwise caps and the trinary law. -/
structure TriadMagnitudes where
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
  hface : a * b * c + 2 * t1 * t2 * t3 ≥ a * t1 ^ 2 + b * t2 ^ 2 + c * t3 ^ 2

/-- **Realization (constructive sufficiency).**  The aligned-phase record carries exactly the
    prescribed magnitudes and is admissible. -/
theorem aligned_realization (m : TriadMagnitudes) :
    ∃ ρ : TriadState,
      ρ.r11 = m.a ∧ ρ.r22 = m.b ∧ ρ.r33 = m.c
        ∧ ρ.r12 = m.t3 ∧ ρ.r13 = m.t2 ∧ ρ.r23 = m.t1 := by
  have hann := m.hann
  obtain ⟨ha, hb, hc, ht1, ht2, ht3⟩ := hann
  -- determinant positivity is exactly the face, in the constructor's monomial order
  have hface' : 0 ≤ m.a * m.b * m.c + 2 * m.t3 * m.t1 * m.t2
      - m.a * m.t1 ^ 2 - m.b * m.t2 ^ 2 - m.c * m.t3 ^ 2 := by
    have hreorder : m.a * m.b * m.c + 2 * m.t3 * m.t1 * m.t2
        = m.a * m.b * m.c + 2 * m.t1 * m.t2 * m.t3 := by ring
    rw [hreorder]
    linarith [m.hface]
  refine ⟨⟨m.a, m.b, m.c, m.t3, m.t2, m.t1,
            by linarith [m.htr],
            by linarith [m.hcap3],
            by linarith [m.hcap2],
            by linarith [m.hcap1],
            hface'⟩,
          rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- **Necessity into magnitude language.**  Every admissible record produces magnitude data
    satisfying caps ∧ face (caps from the Sylvester minors, face from `triad_constraint`). -/
theorem magnitudes_of_admissible (ρ : TriadState) :
    t1 ρ ^ 2 ≤ ρ.r22 * ρ.r33
      ∧ t2 ρ ^ 2 ≤ ρ.r11 * ρ.r33
      ∧ t3 ρ ^ 2 ≤ ρ.r11 * ρ.r22
      ∧ ρ.r11 * ρ.r22 * ρ.r33 + 2 * t1 ρ * t2 ρ * t3 ρ
          ≥ ρ.r11 * t1 ρ ^ 2 + ρ.r22 * t2 ρ ^ 2 + ρ.r33 * t3 ρ ^ 2 := by
  refine ⟨?_, ?_, ?_, triad_constraint ρ⟩
  · unfold t1
    rw [sq_abs]
    linarith [ρ.hmin23]
  · unfold t2
    rw [sq_abs]
    linarith [ρ.hmin13]
  · unfold t3
    rw [sq_abs]
    linarith [ρ.hmin12]

/-! ### Capstone -/

/-- **D0-TRIAD-SUFFICIENCY-001 (capstone).**  Realizability of a magnitude six-tuple by an
    admissible triad record is EQUIVALENT to caps ∧ face: necessity flows back through the
    Sylvester minors and `triad_constraint`, sufficiency is the aligned-phase construction.
    The admissible magnitude region of the triad is completely described — nothing hidden. -/
theorem TRIAD_MAGNITUDE_CHARACTERIZATION_PROVED :
    (∀ m : TriadMagnitudes,
        ∃ ρ : TriadState,
          ρ.r11 = m.a ∧ ρ.r22 = m.b ∧ ρ.r33 = m.c
            ∧ ρ.r12 = m.t3 ∧ ρ.r13 = m.t2 ∧ ρ.r23 = m.t1) ∧
    (∀ ρ : TriadState,
        t1 ρ ^ 2 ≤ ρ.r22 * ρ.r33
          ∧ t2 ρ ^ 2 ≤ ρ.r11 * ρ.r33
          ∧ t3 ρ ^ 2 ≤ ρ.r11 * ρ.r22
          ∧ ρ.r11 * ρ.r22 * ρ.r33 + 2 * t1 ρ * t2 ρ * t3 ρ
              ≥ ρ.r11 * t1 ρ ^ 2 + ρ.r22 * t2 ρ ^ 2 + ρ.r33 * t3 ρ ^ 2) :=
  ⟨fun m => aligned_realization m,
   fun ρ => magnitudes_of_admissible ρ⟩

end D0
