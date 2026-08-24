import Mathlib.Tactic
import D0.Core.DyadComplementarity

/-!
# D0-DYAD-CLOSURE-FORCING-001 — the unit closure is FORCED, not normalized

The complementarity chain so far assumed the unit closure (`r11 + r22 = 1`).  The trace-2
control of `vp_dyad_complementarity.py` (contrast = V/2) exposed the real question: WHY is the
total response exactly 1?  This module answers it as a theorem, closing the last empirical-looking
joint of the dyad house.

Generalize the dyad to an arbitrary closure constant `k = r11 + r22` (total positive response)
with positivity `det ≥ 0`, and ask two independent questions of the RAW readout functionals
`D = |r11 − r22|`, `V = 2|r12|`:

* **Validity.**  `D² + V² ≤ 1` holds for every admissible state of closure `k`  ⟺  `k ≤ 1`.
  (For `k > 1` the near-pure state `r11 ≈ k, r22 ≈ 0, r12 = 0` gives `D² ≈ k² > 1`.)
* **Saturability.**  Some admissible state of closure `k` attains `D² + V² = 1`  ⟺  `k ≥ 1`.
  (For `k < 1` every state gives `D² + V² = k² − 4·det ≤ k² < 1` — the bound can never be
  reached; the descriptive capacity is dead.)

**Forcing theorem.**  Validity ∧ saturability holds  ⟺  `k = 1`.  The unit closure is the
UNIQUE closure constant at which the complementarity bound is both true everywhere and tight.

**Why this is a derivation, not a normalization choice.**  Any `k ≠ 1` forces one of two
description costs: either the raw readout violates the bound (theory broken), or an extra
normalization constant `1/k` must be carried in every readout statement.  A free real constant
in the law is exactly the exogenous catalog that M1 (§00, no obligatory external catalogue)
forbids.  So M1 + complementarity FORCE `k = 1` — and the unit closure is the same object the
primitive skeleton already owns as the response split `p + p² = 1` (`D0.Core.Phi`): one unit
section of registration, split into the direct branch `p` and the return branch `p²`.

Honest scope: the forcing is proved for the two-branch readout family; the identification of
"raw functionals must obey a k-independent bound" as the operative no-catalog requirement is
the M1 reading, stated here as the design principle it enforces, not as a separate formal axiom.
-/

namespace D0

/-- Dyad readout state with arbitrary closure constant `k = r11 + r22` and positivity. -/
structure GenDyadState (k : ℝ) where
  r11 : ℝ
  r22 : ℝ
  r12 : ℝ
  htrace : r11 + r22 = k
  hpsd : 0 ≤ r11 * r22 - r12 ^ 2

/-- Path functional of the generalized state. -/
def genD (k : ℝ) (ρ : GenDyadState k) : ℝ := |ρ.r11 - ρ.r22|

/-- Coherence functional of the generalized state. -/
def genV (k : ℝ) (ρ : GenDyadState k) : ℝ := 2 * |ρ.r12|

/-- The raw identity at closure `k`: `D² + V² = k² − 4·det`. -/
theorem gen_raw_identity (k : ℝ) (ρ : GenDyadState k) :
    genD k ρ ^ 2 + genV k ρ ^ 2 = k ^ 2 - 4 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) := by
  unfold genD genV
  have h1 : |ρ.r11 - ρ.r22| ^ 2 = (ρ.r11 - ρ.r22) ^ 2 := sq_abs _
  have h2 : (2 * |ρ.r12|) ^ 2 = 4 * ρ.r12 ^ 2 := by
    rw [mul_pow, sq_abs]
    ring
  rw [h1, h2]
  have h3 : (ρ.r11 - ρ.r22) ^ 2 + 4 * ρ.r12 ^ 2
      = (ρ.r11 + ρ.r22) ^ 2 - 4 * (ρ.r11 * ρ.r22 - ρ.r12 ^ 2) := by ring
  rw [h3, ρ.htrace]

/-- Counterexample family: the near-pure state carrying everything on one branch. -/
private theorem pure_state_D {k : ℝ} (hk : 0 < k) :
    genD k ⟨k, 0, 0, by linarith, by norm_num⟩ = k := by
  unfold genD
  rw [sub_zero, abs_of_pos hk]

private theorem pure_state_V {k : ℝ} :
    genV k ⟨k, 0, 0, by linarith, by norm_num⟩ = 0 := by
  unfold genV
  norm_num

/-- **Validity ⟺ k ≤ 1.**  The raw bound holds for every admissible state of closure `k`
    exactly when `k ≤ 1`. -/
theorem gen_bound_valid_iff (k : ℝ) (hk : 0 ≤ k) :
    (∀ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 ≤ 1) ↔ k ≤ 1 := by
  constructor
  · intro hall
    by_contra hkle
    push_neg at hkle
    have hkpos : 0 < k := by linarith
    have hval := hall ⟨k, 0, 0, by linarith, by norm_num⟩
    rw [pure_state_D hkpos, pure_state_V] at hval
    have hk2 : (1 : ℝ) < k ^ 2 := by nlinarith
    nlinarith
  · intro hkle ρ
    have hid := gen_raw_identity k ρ
    have hdet := ρ.hpsd
    have hk2le : k ^ 2 ≤ 1 := by nlinarith [hkle, hk]
    linarith

/-- **Saturability ⟺ k ≥ 1.**  Some admissible state of closure `k` attains the bound exactly
    when `k ≥ 1` (for `k < 1` the bound is unreachable: `D² + V² ≤ k² < 1`). -/
theorem gen_bound_saturable_iff (k : ℝ) (hk : 0 ≤ k) :
    (∃ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 = 1) ↔ 1 ≤ k := by
  constructor
  · rintro ⟨ρ, hρ⟩
    have hid := gen_raw_identity k ρ
    rw [hρ] at hid
    have hdet := ρ.hpsd
    have hkpos : 0 ≤ k ^ 2 := sq_nonneg k
    have h1 : (1 : ℝ) ≤ k ^ 2 := by linarith
    have hk1 : 1 ≤ k := by
      rcases lt_or_ge k 0 with hneg | _
      · -- 0 ≤ k and k < 0 give k = 0, but k² ≥ 1 is absurd
        have : k = 0 := by linarith
        rw [this] at h1
        norm_num at h1
      · -- k ≥ 0 and k² ≥ 1 ⇒ k ≥ 1
        nlinarith [h1]
    exact hk1
  · intro hk1
    -- witness: r11 = (k+1)/2, r22 = (k−1)/2, r12 = 0 ⇒ det = (k²−1)/4, D² + V² = k² − (k²−1) = 1
    refine ⟨⟨(k + 1) / 2, (k - 1) / 2, 0, ?_, ?_⟩, ?_⟩
    · linarith
    · have hprod : ((k + 1) / 2) * ((k - 1) / 2) = (k ^ 2 - 1) / 4 := by ring
      have hk2 : 1 ≤ k ^ 2 := by nlinarith
      have hge0 : 0 ≤ (k ^ 2 - 1) / 4 := by linarith
      rw [hprod]
      linarith
    · unfold genD genV
      rw [show (k + 1) / 2 - (k - 1) / 2 = 1 by ring, abs_of_nonneg (by norm_num : (0:ℝ) ≤ 1)]
      have : (2 * |(0:ℝ)|) ^ 2 = 0 := by norm_num
      rw [this, add_zero]
      ring

/-- **Forcing theorem.**  The closure constant is forced to be exactly 1: validity and
    saturability of the raw complementarity bound hold simultaneously  ⟺  `k = 1`. -/
theorem gen_closure_forced (k : ℝ) (hk : 0 ≤ k) :
    ((∀ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 ≤ 1)
      ∧ ∃ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 = 1) ↔ k = 1 := by
  constructor
  · rintro ⟨hvalid, ⟨ρ, hρ⟩⟩
    have hle := (gen_bound_valid_iff k hk).mp hvalid
    have hge := (gen_bound_saturable_iff k hk).mp ⟨ρ, hρ⟩
    linarith
  · intro hk1
    subst hk1
    have hk0 : (0 : ℝ) ≤ 1 := by norm_num
    have hvalid := (gen_bound_valid_iff 1 hk0).mpr le_rfl
    have hsat := (gen_bound_saturable_iff 1 hk0).mpr le_rfl
    exact ⟨hvalid, hsat⟩

/-- The owned unit closure realizes the forced value: a dyad state of `D0.Core.DyadState`
    is a `GenDyadState 1`, and its raw functionals coincide with the owned ones. -/
theorem dyad_state_is_forced_closure (ρ : DyadState) :
    ∃ ρ' : GenDyadState 1, genD 1 ρ' = distinguishability ρ ∧ genV 1 ρ' = visibility ρ :=
  ⟨⟨ρ.r11, ρ.r22, ρ.r12, ρ.htrace, ρ.hpsd⟩, by
    unfold genD distinguishability; rfl, by
    unfold genV visibility; rfl⟩

/-! ### Capstone -/

/-- **D0-DYAD-CLOSURE-FORCING-001 (capstone).**  Validity ⟺ k ≤ 1; saturability ⟺ k ≥ 1;
    both together force k = 1; and the owned dyad (unit closure, the p + p² split of the
    primitive skeleton) realizes exactly the forced value.  No normalization constant is free:
    M1 closes the last empirical-looking joint of the complementarity house. -/
theorem DYAD_CLOSURE_FORCING_PROVED :
    (∀ k : ℝ, 0 ≤ k →
        ((∀ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 ≤ 1) ↔ k ≤ 1)) ∧
    (∀ k : ℝ, 0 ≤ k →
        ((∃ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 = 1) ↔ 1 ≤ k)) ∧
    (∀ k : ℝ, 0 ≤ k →
        (((∀ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 ≤ 1)
            ∧ ∃ ρ : GenDyadState k, genD k ρ ^ 2 + genV k ρ ^ 2 = 1) ↔ k = 1)) ∧
    (∀ ρ : DyadState,
        ∃ ρ' : GenDyadState 1, genD 1 ρ' = distinguishability ρ ∧ genV 1 ρ' = visibility ρ) :=
  ⟨fun k hk => gen_bound_valid_iff k hk,
   fun k hk => gen_bound_saturable_iff k hk,
   fun k hk => gen_closure_forced k hk,
   fun ρ => dyad_state_is_forced_closure ρ⟩

end D0
