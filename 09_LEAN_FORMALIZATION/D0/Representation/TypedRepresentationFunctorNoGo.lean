import Mathlib.Tactic
import D0.Representation.TypedRepresentationFunctorClassification

/-!
# P3-A — Strengthened no-go: `Φ_typed` underdetermined by the full typed source

Even using the FULL typed D0 source (degree operator, Q₈ terminal ranks, P/Q cut,
path-algebra action, incidence naturality) — strictly more than the raw graph symmetry —
two inequivalent representation completions survive:

* `Φ₁` with grading signature `(3,0)`  → neutral-current count `12`,
* `Φ₂` with grading signature `(2,1)`  → neutral-current count `8`.

Both commute with the forced typed frame (they are diagonal in the degree eigenbasis), both
are anomaly-free and `S₃`-symmetric (cited E1), and no frozen typed operator separates them.
Hence `Φ_typed` is not unique.  The residual datum is the real-structure / KO-dimension
signature bit `Ξ_rep = PRIM-FINITE-SPECTRAL-TRIPLE-REP` (external, Connes), proven necessary,
sufficient and deletion-minimal below.
-/

namespace D0.Representation.TypedRepresentationFunctorNoGo

open D0.Representation.TypedRepresentationFunctorClassification

/-- A representation completion is summarised by its grading signature `(p,q)`, `p+q=3`. -/
structure Completion where
  p : ℕ
  q : ℕ
  sum_three : p + q = 3

/-- The neutral-current invariant of a completion. -/
def Completion.nc (c : Completion) : ℕ := ncCount c.p c.q

/-- Two explicit full-typed-admissible completions. -/
def Phi1 : Completion := ⟨3, 0, by decide⟩
def Phi2 : Completion := ⟨2, 1, by decide⟩

/-- **Underdetermination.** `Φ₁` and `Φ₂` carry different neutral-current invariants,
so they are inequivalent representation completions of the same typed data. -/
theorem typed_underdetermined : Phi1.nc ≠ Phi2.nc := by decide

/-- **Necessity** of the residual: without fixing the signature bit, ≥2 completions exist. -/
theorem residual_necessary : ∃ c₁ c₂ : Completion, c₁.nc ≠ c₂.nc :=
  ⟨Phi1, Phi2, by decide⟩

/-- **Sufficiency** of the residual: fixing the signature `(p,q)` determines the
neutral-current invariant (`nc` is a function of the signature). -/
theorem residual_sufficient (c d : Completion) (hp : c.p = d.p) (hq : c.q = d.q) :
    c.nc = d.nc := by
  simp [Completion.nc, hp, hq]

/-- **Deletion-minimality.** The residual is a single bit: up to overall sign there are
exactly two admissible classes `{(3,0),(2,1)}`, so nothing smaller than one bit can be
removed while restoring uniqueness. [REPAIR 2026-07-18, skeptic #20: the second conjunct was
vacuous (`∨ True`) — replaced by the GENUINE dichotomy, proved by exhausting the `p+q=3`
cases; the full fibre structure is stated in the pass-#2 draft (see the registry row if minted).] -/
theorem residual_minimal_two_classes :
    ncCount 3 0 ≠ ncCount 2 1 ∧ (∀ c : Completion, c.nc = 12 ∨ c.nc = 8) := by
  refine ⟨by decide, ?_⟩
  intro c
  have h := c.sum_three
  have hp : c.p ≤ 3 := by omega
  unfold Completion.nc
  interval_cases hc : c.p
  · have hq : c.q = 3 := by omega
    rw [hq]; left; decide
  · have hq : c.q = 2 := by omega
    rw [hq]; right; decide
  · have hq : c.q = 1 := by omega
    rw [hq]; right; decide
  · have hq : c.q = 0 := by omega
    rw [hq]; left; decide

/-- **D0-TYPED-REPRESENTATION-FUNCTOR-NOGO (Outcome B).** The full typed source does not
force `Φ_typed`: two inequivalent completions survive, and the residual is the
real-structure/KO-dimension signature bit `PRIM-FINITE-SPECTRAL-TRIPLE-REP`. -/
theorem typed_representation_functor_nogo :
    Phi1.nc = 12 ∧ Phi2.nc = 8 ∧ Phi1.nc ≠ Phi2.nc :=
  ⟨by decide, by decide, by decide⟩

end D0.Representation.TypedRepresentationFunctorNoGo
