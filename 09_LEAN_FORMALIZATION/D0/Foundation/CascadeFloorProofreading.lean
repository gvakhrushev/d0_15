import Mathlib.Tactic
import D0.Foundation.CascadeChain

/-!
# The proofreading floor: one equilibrium test cannot reach the verified-record fidelity

**The first structural import of the cross-substrate program** (licensed by
`D0-INFORMATION-CONNECTIVITY-001`; program artifact `COVERAGE_MATRIX_REWIND_2026_08.md`).
The imported structure is kinetic proofreading (Hopfield 1974 PNAS 71:4135; Ninio 1975
Biochimie 57:587 — external-cited, the same grade as Baer 1933 in the role-algebra row):
a single equilibrium discrimination between a right and a wrong substrate is bounded by one
Boltzmann factor — the wrong/right acceptance ratio cannot go below a floor `δ`; reaching
the squared factor `δ²` requires a SECOND test separated by an irreversible reset, i.e. a
second record register plus an arrow-of-time cost. Biology pays this cost in every
replication fork; that is a structural fact about records, not about chemistry.

**In the cascade's own shape** (`CascadeStep`, `D0-CASCADE-CHAIN-SCAFFOLD-001`): the floor
extends the chain at the record/comparison end (moves 1–2 of the coverage matrix).

- Carrier below: ONE equilibrium test — achievable ratios are exactly `ρ ≥ δ` (the
  one-Boltzmann-factor bound is the DEFINING hypothesis of the carrier, stated inside the
  statement, same grade as "one ℤ register" in the 4→5 floor).
- Obligation: reach the proofread error level `errOf (δ·δ)`.
- `insufficient`: provably impossible below — `errOf` is strictly monotone and `δ² < δ`
  for `0 < δ < 1`.
- Repair/control: TWO tests (a pair of ratio slots — the pair carrier whose necessity the
  4→5 floor owns) compose multiplicatively and reach `δ²` exactly.
- Ladder: `n+1` stages strictly beat `n` stages for every `n` — the proofreading cascade
  is unbounded in depth, each stage a genuine floor.

**Honest scope (pre-registered).**
1. The multiplicative composition of the two-stage carrier ENCODES the irreversible-reset
   assumption (without the reset, detailed balance collapses both tests into one
   equilibrium test — Hopfield's own point); the reset's irreversibility is the arrow
   floor's object (T5) at prose grade — the interlock statement "the proofreading repair
   is the arrow floor's failing carrier" is NOT formalized here and remains a named
   target.
2. NO biological numbers are claimed: the polymerase/ribosome error-rate passports
   (acquisition targets A1/A2) do not exist yet; when they do, they anchor the premise
   `0 < δ < 1` and the observed multi-stage fidelity, nothing else.
3. `δ` is parametric — the floor exists for every discrimination limit strictly between
   0 and 1; no specific value is chosen or needed.
-/

namespace D0.Foundation

/-- Error probability of a discrimination channel whose wrong/right acceptance ratio is
`ρ`: accept-wrong weight `ρ` against accept-right weight `1`. -/
def errOf (ρ : ℚ) : ℚ := ρ / (1 + ρ)

/-- `errOf` is strictly monotone on nonnegative ratios: better ratio, strictly better
error. -/
theorem errOf_lt_errOf {ρ₁ ρ₂ : ℚ} (h₀ : 0 ≤ ρ₁) (h : ρ₁ < ρ₂) :
    errOf ρ₁ < errOf ρ₂ := by
  unfold errOf
  have h1 : (0 : ℚ) < 1 + ρ₁ := by linarith
  have h2 : (0 : ℚ) < 1 + ρ₂ := by linarith
  rw [div_lt_div_iff₀ h1 h2]
  nlinarith

theorem errOf_le_errOf {ρ₁ ρ₂ : ℚ} (h₀ : 0 ≤ ρ₁) (h : ρ₁ ≤ ρ₂) :
    errOf ρ₁ ≤ errOf ρ₂ := by
  rcases eq_or_lt_of_le h with rfl | hlt
  · exact le_refl _
  · exact (errOf_lt_errOf h₀ hlt).le

/-- The one-test carrier: a single equilibrium discrimination. Achievable ratios are
exactly `ρ ≥ δ` (one Boltzmann factor — the carrier's defining hypothesis). The carrier
reaches `target` iff some achievable ratio does. -/
def OneTestReaches (δ target : ℚ) : Prop :=
  ∃ ρ : ℚ, δ ≤ ρ ∧ errOf ρ ≤ target

/-- The two-stage carrier: two tests separated by an irreversible reset — ratios compose
multiplicatively (the reset is what forbids detailed balance from collapsing the pair into
one test). -/
def TwoStageReaches (δ target : ℚ) : Prop :=
  ∃ ρ₁ ρ₂ : ℚ, δ ≤ ρ₁ ∧ δ ≤ ρ₂ ∧ errOf (ρ₁ * ρ₂) ≤ target

/-- **The floor fails**: one equilibrium test cannot reach the proofread error level —
for `0 < δ < 1` we have `δ² < δ`, and `errOf` is strictly monotone. -/
theorem one_test_insufficient (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) :
    ¬ OneTestReaches δ (errOf (δ * δ)) := by
  rintro ⟨ρ, hρ, herr⟩
  have hmin : errOf δ ≤ errOf ρ := errOf_le_errOf h₀.le hρ
  have hsq : errOf (δ * δ) < errOf δ :=
    errOf_lt_errOf (by positivity) (by nlinarith)
  linarith

/-- **The repair succeeds**: two tests at the limit compose to exactly `δ²`. -/
theorem two_stage_control (δ : ℚ) : TwoStageReaches δ (errOf (δ * δ)) :=
  ⟨δ, δ, le_refl _, le_refl _, le_refl _⟩

/-- **The proofreading floor in the registered cascade shape**: the same obligation —
reach the proofread error level `errOf (δ²)` — provably fails on the one-test carrier and
provably holds on the two-stage carrier, for every discrimination limit `0 < δ < 1`. -/
def stepProofreading (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) : CascadeStep where
  name := "one equilibrium test cannot reach the proofread fidelity (record → verified record)"
  ObligationBelow := OneTestReaches δ (errOf (δ * δ))
  ObligationAbove := TwoStageReaches δ (errOf (δ * δ))
  insufficient := one_test_insufficient δ h₀ h₁
  control := two_stage_control δ

/-- The floor discriminates (via the scaffold's own theorem): it is a real change of
structure, not a renaming. -/
theorem stepProofreading_discriminates (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) :
    ¬ ((stepProofreading δ h₀ h₁).ObligationBelow ↔
        (stepProofreading δ h₀ h₁).ObligationAbove) :=
  step_discriminates _

/-- **The proofreading ladder**: `n+1` stages strictly beat `n` stages — each added
register-plus-reset is a genuine floor, for every `n`. The cascade of verified records is
unbounded in depth. -/
theorem proofreading_ladder (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) (n : ℕ) :
    errOf (δ ^ (n + 1)) < errOf (δ ^ n) := by
  apply errOf_lt_errOf (by positivity)
  have hpow : δ ^ (n + 1) = δ ^ n * δ := pow_succ δ n
  nlinarith [pow_pos h₀ n]

/-- Assembly: the floor exists at every discrimination limit, and the ladder descends
strictly at every depth. -/
theorem proofreading_floor (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) :
    (¬ OneTestReaches δ (errOf (δ * δ)))
      ∧ TwoStageReaches δ (errOf (δ * δ))
      ∧ ∀ n : ℕ, errOf (δ ^ (n + 1)) < errOf (δ ^ n) :=
  ⟨one_test_insufficient δ h₀ h₁, two_stage_control δ, proofreading_ladder δ h₀ h₁⟩

end D0.Foundation
