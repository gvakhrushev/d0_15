import Mathlib.Tactic
import D0.Core.BornFinite

/-!
# D0-DYAD-COMPLEMENTARITY-001 — complementarity as a theorem of the measurement dyad

The no-monopoly dyad (§01.3) forces every registration to carry TWO independently addressable
branches plus a comparison; the positive two-channel response closes them into Born weights
(`D0.Core.BornFinite`).  A branch-pair readout state is therefore an admissible symmetric 2×2
matrix: unit total response (`r11 + r22 = 1`) and positivity (`det = r11·r22 − r12² ≥ 0`).

On this finite stage the two classical readout modes become exact functionals:

* **path distinguishability** `D(ρ) = |r11 − r22|`  — WHICH branch carried the record;
* **coherence visibility**     `V(ρ) = 2·|r12|`     — interference contrast between branches.

**Main theorem.**  Every admissible dyad state obeys the joint bound

    D(ρ)² + V(ρ)² ≤ 1,

with equality iff `det ρ = 0`.  Proof: `D² + V² = (r11+r22)² − 4·det = 1 − 4·det ≤ 1`.
The bound is exactly positivity of the joint response — complementarity is not an extra postulate
here, it is what "no monopoly + positive response" means arithmetically.

**The two equality families are the wave/particle extremes.**  `diag(1,0)` (record fully on one
branch) gives `(D, V) = (1, 0)`; the balanced coherent state `[[1/2, 1/2], [1/2, 1/2]]` gives
`(D, V) = (0, 1)`.  Every admissible state lies on or inside the quarter circle between them.

Honest scope (house split): the STRUCTURE above is THE — machine-checked, finite, exact.  The
identification of `V` with optical fringe visibility and `D` with which-path distinguishability
is a typed BRIDGE to laboratory interferometry (Englert's `V² + D² ≤ 1` is the corresponding
external-background relation for two-beam experiments); that bridge is NOT claimed as derived
here.  What IS new and owned: the bound holds for the dyad architecture itself, with zero
quantum postulates — only unit closure and positivity of the two-channel response, i.e. the same
primitives that already own the Born weights upstream.
-/

namespace D0

/-- Admissible dyad readout state: branch-pair weights with unit closure and positive joint
    response (`det ≥ 0`).  Symmetry is built in by storing only the upper triangle. -/
structure DyadState where
  r11 : ℝ
  r22 : ℝ
  r12 : ℝ
  htrace : r11 + r22 = 1
  hpsd : 0 ≤ r11 * r22 - r12 ^ 2

/-- Which-branch contrast of the record. -/
def distinguishability (ρ : DyadState) : ℝ := |ρ.r11 - ρ.r22|

/-- Interference contrast between the branches. -/
def visibility (ρ : DyadState) : ℝ := 2 * |ρ.r12|

/-- **Dyad complementarity bound.**  Joint strength of the two readout modes is bounded by the
    unit closure: `D² + V² ≤ 1`. -/
theorem dyad_complementarity_bound (ρ : DyadState) :
    distinguishability ρ ^ 2 + visibility ρ ^ 2 ≤ 1 := by
  unfold distinguishability visibility
  have habssq : |ρ.r11 - ρ.r22| ^ 2 = (ρ.r11 - ρ.r22) ^ 2 := sq_abs _
  have hv : (2 * |ρ.r12|) ^ 2 = 4 * ρ.r12 ^ 2 := by
    rw [mul_pow, sq_abs]
    ring
  rw [habssq, hv]
  have expand : (ρ.r11 - ρ.r22) ^ 2 + 4 * ρ.r12 ^ 2
      = (ρ.r11 + ρ.r22) ^ 2 - 4 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) := by ring
  rw [expand, ρ.htrace]
  have hdet := ρ.hpsd
  linarith

/-- **Equality case.**  The bound is saturated exactly by the degenerate (pure/rank-one)
    states: saturation ⟺ `det ρ = 0`. -/
theorem dyad_bound_eq_iff_det_zero (ρ : DyadState) :
    (distinguishability ρ ^ 2 + visibility ρ ^ 2 = 1)
      ↔ ρ.r11 * ρ.r22 - ρ.r12 ^ 2 = 0 := by
  unfold distinguishability visibility
  have habssq : |ρ.r11 - ρ.r22| ^ 2 = (ρ.r11 - ρ.r22) ^ 2 := sq_abs _
  have hv : (2 * |ρ.r12|) ^ 2 = 4 * ρ.r12 ^ 2 := by
    rw [mul_pow, sq_abs]
    ring
  have expand : (ρ.r11 - ρ.r22) ^ 2 + 4 * ρ.r12 ^ 2
      = (ρ.r11 + ρ.r22) ^ 2 - 4 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) := by ring
  constructor
  · intro heq
    have hsum : |ρ.r11 - ρ.r22| ^ 2 + (2 * |ρ.r12|) ^ 2
        = (ρ.r11 + ρ.r22) ^ 2 - 4 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) := by
      rw [habssq, hv]
      exact expand
    rw [hsum, ρ.htrace] at heq
    norm_num at heq
    linarith
  · intro hdet
    rw [habssq, hv, expand, ρ.htrace, hdet]
    norm_num

/-! ### The two equality families: the wave/particle extremes -/

/-- Particle-mode extremum: the record is fully on one branch. -/
noncomputable def pathCertain : DyadState :=
  ⟨1, 0, 0, by norm_num, by norm_num⟩

/-- Wave-mode extremum: balanced coherent superposition of the branches. -/
noncomputable def coherenceMaximal : DyadState :=
  ⟨1 / 2, 1 / 2, 1 / 2, by norm_num, by norm_num⟩

theorem pathCertain_readout :
    distinguishability pathCertain = 1 ∧ visibility pathCertain = 0 := by
  unfold distinguishability visibility pathCertain
  constructor <;> simp

theorem coherenceMaximal_readout :
    visibility coherenceMaximal = 1 ∧ distinguishability coherenceMaximal = 0 := by
  unfold visibility distinguishability coherenceMaximal
  constructor <;> simp

/-! ### Capstone -/

/-- **D0-DYAD-COMPLEMENTARITY-001 (capstone).**  Complementarity is a theorem of the dyad
    architecture: the two readout modes are jointly bounded by the unit closure, saturation is
    exactly degeneracy of the joint response, and the two idealized modes (wave / particle) are
    realized as the two equality families. -/
theorem DYAD_COMPLEMENTARITY_PROVED :
    (∀ ρ : DyadState, distinguishability ρ ^ 2 + visibility ρ ^ 2 ≤ 1) ∧
    (∀ ρ : DyadState,
        (distinguishability ρ ^ 2 + visibility ρ ^ 2 = 1)
          ↔ ρ.r11 * ρ.r22 - ρ.r12 ^ 2 = 0) ∧
    (distinguishability pathCertain = 1 ∧ visibility pathCertain = 0) ∧
    (visibility coherenceMaximal = 1 ∧ distinguishability coherenceMaximal = 0) :=
  ⟨fun ρ => dyad_complementarity_bound ρ,
   fun ρ => dyad_bound_eq_iff_det_zero ρ,
   pathCertain_readout,
   coherenceMaximal_readout⟩

end D0
