import D0.Representation.TypedRepresentationFunctorNoGo
import D0.Extensions.GradingMinimalCompletion

/-!
# E1 residual collapse — the two-completion underdetermination compresses to ONE external bit
# (no-go-synthesis pass #2, DRAFT)

Claim: `D0-COMPLETION-RESIDUAL-COLLAPSE-001` (candidate). Memo:
`_TASKS_CENTER_ATTACK/COMPLETION_RESIDUAL_COLLAPSE_MEMO.md`.

Composition of owned/graded pieces — nothing new is postulated:
* The Weyl-role `S₃` freedom is RESOLVED internally at cert grade — "the Aut part-size order
  9<11<13 RESOLVES the E1 Weyl-role leg" (`D0-CANONICAL-SELF-READING-FUNCTOR-001`) — with the
  physical e/μ/τ NAMING residue external (row 559); the invariant `nc` never references roles.
* The signature axis is exhausted and argmin-selected (`D0-GRADING-MINIMAL-COMPLETION-
  SELECTION-001`, pass #1): floor `8`, minimizers = the flip pair.
* Within the minimal class, the Frobenius–Schur assignment of the Q₈ terminal sectors
  (`E₀:+1, E₄:−1, E₃:+1` — exactly ONE quaternionic sector) selects the ORIENTATION `(2,1)`
  over `(1,2)` — CONDITIONAL on the KO-dimension convention `J² = ±1`, which is the external
  `PRIM-FINITE-SPECTRAL-TRIPLE-REP` (the Classification module's own named open obligation).

Machine-checked here:
1. `completion_nc_dichotomy` — every completion has `nc = 12 ∨ nc = 8` (this is the GENUINE
   form of the vacuous second conjunct of `residual_minimal_two_classes`, whose `∨ True`
   skeptic #20 named; the owned module is repaired in the same pass, cited).
2. `nc_flip_invariant` + `nc_eq_iff_flip_class` — the invariant is flip-symmetric, and two
   completions share `nc` IFF they are equal or flip-related: the nc-fibres ARE the
   flip-classes; there are exactly two.
3. `ncCount_defs_agree` — the two in-tree `ncCount` definitions (E1's and Classification's)
   agree definitionally (discharges skeptic #20's duplicate-def observation).
4. `fs_orientation_selects` — the FS count (exactly one `−1` sector) matches the `q`-slot of
   `(2,1)` and NOT of `(1,2)`: GIVEN the odd=quaternionic reading (the KO bit), the
   orientation inside the minimal class is determined. The bit itself stays external.

The capstone reading (honest grades): the E1 residual decomposes as
  roles (cert-RESOLVED, row 477; naming residue external, row 559) ×
  signature-class (ARGMIN-selected; licensing narrated) ×
  orientation (FS-determined CONDITIONAL on the KO bit) —
so at SIGNATURE grain the residual reduces, conditionally, to the single KO bit; at
COMPLETION grain the residual is the named PRIM pair (`PRIM-FINITE-SPECTRAL-TRIPLE-REP` =
KO bit + role-resolution/physical naming; `PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR` = the
operator-level class). The E1 no-go stays true and unchanged; no completion uniqueness is
asserted. What this pass adds is the exact LOCATION of the remaining freedom.
-/

namespace D0.Representation.CompletionResidualCollapse

open D0.Representation.TypedRepresentationFunctorNoGo
open D0.Representation.TypedRepresentationFunctorClassification

/-- The two in-tree `ncCount` definitions agree (definitionally). -/
theorem ncCount_defs_agree :
    ∀ p q : ℕ,
      D0.Representation.TypedRepresentationFunctorClassification.ncCount p q =
        D0.Extensions.RepresentationReadoutExtension.ncCount p q :=
  fun _ _ => rfl

/-- **Dichotomy (the genuine form of the vacuous conjunct).** Every completion's
neutral-current invariant is `12` or `8`. -/
theorem completion_nc_dichotomy : ∀ c : Completion, c.nc = 12 ∨ c.nc = 8 := by
  intro c
  have h := c.sum_three
  have hp : c.p ≤ 3 := by omega
  unfold Completion.nc
  interval_cases hc : c.p
  · obtain hq : c.q = 3 := by omega
    rw [hq]; left; decide
  · obtain hq : c.q = 2 := by omega
    rw [hq]; right; decide
  · obtain hq : c.q = 1 := by omega
    rw [hq]; right; decide
  · obtain hq : c.q = 0 := by omega
    rw [hq]; left; decide

/-- The grading-sign flip on completions: `(p,q) ↦ (q,p)`. -/
def flip (c : Completion) : Completion := ⟨c.q, c.p, by have := c.sum_three; omega⟩

/-- **Flip-invariance of the invariant.** -/
theorem nc_flip_invariant (c : Completion) : (flip c).nc = c.nc := by
  unfold Completion.nc flip
  simp [D0.Representation.TypedRepresentationFunctorClassification.ncCount]
  ring

/-- Every completion's signature pair is one of the four `p+q=3` values. -/
theorem completion_cases (c : Completion) :
    (c.p, c.q) = (3, 0) ∨ (c.p, c.q) = (2, 1) ∨ (c.p, c.q) = (1, 2) ∨ (c.p, c.q) = (0, 3) := by
  have h := c.sum_three
  have hp : c.p ≤ 3 := by omega
  interval_cases hc : c.p
  · have hq : c.q = 3 := by omega
    simp [hq]
  · have hq : c.q = 2 := by omega
    simp [hq]
  · have hq : c.q = 1 := by omega
    simp [hq]
  · have hq : c.q = 0 := by omega
    simp [hq]

/-- **The nc-fibres are exactly the flip-classes (signature level, whole class by decide).**
Over the exhausted signature list: two signatures share `ncCount` IFF equal or swap-related —
`nc` is a complete invariant of the flip-quotient, which has exactly two classes. -/
theorem nc_eq_iff_flip_class_sig :
    ∀ a ∈ D0.Extensions.RepresentationReadoutExtension.gradingSignatures,
      ∀ b ∈ D0.Extensions.RepresentationReadoutExtension.gradingSignatures,
        (D0.Representation.TypedRepresentationFunctorClassification.ncCount a.1 a.2 =
          D0.Representation.TypedRepresentationFunctorClassification.ncCount b.1 b.2
          ↔ a = b ∨ a = Prod.swap b) := by
  decide

/-- **Lift to completions.** Two completions share the invariant IFF their signature pairs are
equal or swap-related. -/
theorem nc_eq_iff_flip_class (c d : Completion) :
    c.nc = d.nc ↔ ((c.p, c.q) = (d.p, d.q) ∨ (c.p, c.q) = Prod.swap (d.p, d.q)) := by
  have hc := completion_cases c
  have hd := completion_cases d
  unfold Completion.nc
  rcases hc with h1 | h1 | h1 | h1 <;> rcases hd with h2 | h2 | h2 | h2 <;>
    rw [show c.p = (c.p, c.q).1 from rfl, show c.q = (c.p, c.q).2 from rfl,
        show d.p = (d.p, d.q).1 from rfl, show d.q = (d.p, d.q).2 from rfl, h1, h2] <;>
    decide

/-- The Frobenius–Schur sector signs of the Q₈ terminal sectors in the canonical in-tree
order `(E₀, E₄, E₃)` (`q8Ranks`, TypedRepresentationFunctor.lean): `E₀:+1, E₄:−1, E₃:+1` —
exactly ONE quaternionic (`−1`) sector, the classical FS data of Q₈, as narrated in the
Classification module (cited, not in-tree derived — named upgrade). -/
def fsSectorSigns : List Int := [1, -1, 1]

/-- **FS orientation selection (CONDITIONAL leg — the KO bit stays external).** The number of
quaternionic (`−1`) sectors is `1`, which equals the `q`-slot of `(2,1)` and NOT of `(1,2)`:
under the odd=quaternionic reading (= the KO-dimension convention `J²=±1`, the external
`PRIM-FINITE-SPECTRAL-TRIPLE-REP`), the orientation inside the minimal flip-class is
determined at `(2,1)` = `q8FSsignature`. Absent the bit, the flip stays open (pass #1). -/
theorem fs_orientation_selects :
    (fsSectorSigns.filter (· = -1)).length = 1 ∧
    (2, 1).2 = 1 ∧ (1, 2).2 ≠ 1 ∧ q8FSsignature = (2, 1) := by
  refine ⟨by decide, by decide, by decide, rfl⟩

/-- **E1 residual collapse (bundle).** The invariant is dichotomous (`{12,8}`),
flip-symmetric with the nc-fibres = flip-classes (exactly two), the two `ncCount`
definitions agree, and the FS data selects the orientation inside the minimal class
conditional on the external KO bit. Composed with pass #1 (exhaustion + argmin) and the
R1-cited role-gauge reading: the E1 underdetermination compresses to the ONE named
external bit. The E1 no-go itself is unchanged. -/
theorem completion_residual_collapse :
    (∀ c : Completion, c.nc = 12 ∨ c.nc = 8) ∧
    (∀ c : Completion, (flip c).nc = c.nc) ∧
    ((fsSectorSigns.filter (· = -1)).length = 1 ∧ q8FSsignature = (2, 1)) :=
  ⟨completion_nc_dichotomy, nc_flip_invariant,
   ⟨by decide, rfl⟩⟩

end D0.Representation.CompletionResidualCollapse
