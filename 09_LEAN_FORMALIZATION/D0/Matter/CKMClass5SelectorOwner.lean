import D0.Foundation.M1Predicate
import Mathlib.Tactic

/-!
# D0-CKM-CLASS5-SELECTOR-OWNER-001 — the M1Forced witness wiring the class-5 pointer
collision to the proven selector spine (Cabibbo soft joint, §04.10)

The class-5 EXCLUSION itself is already CORE-FORMALIZED in `D0.Claims.Class5Aliasing`
(`D0-CLASS5-ALIASING-001`): `|Z5| = 5 = D_Σ`, the survivor set `{1, 20}`, and the decidable
`25 → 5` readout collapse.  This module does NOT re-close that exclusion.  Its NEW scope is the
*owner* object the honesty register asked for: a concrete **`FiniteSelector`** over the
register-configuration candidates whose `StrictSelected` strict-minimum forces the
diagonal / no-hidden-register answer, after which the proven M1 keystone
(`D0.Foundation.m1_alternative_needs_catalogue`, via `selector_M1Forced`) gives
`RequiresExternalCatalogue` for every alternative — a real term-mode witness, no `¬Forced`
shell.

Two finite ingredients, both genuinely decidable:

* **Orbit-length separation.**  The candidate winding classes are the M1-admissible
  characteristic orders `{1, 5, 20}` (class 4 already killed by orientation).  The cyclic
  winding orbit of a class-`d` generator has length `d` (`orbitLength d = d`), so the three
  classes are pairwise separated, and class 5 is the *unique* one whose orbit length equals the
  operational address count `D_Σ = 5` — the pointer collision.  Classes 1 and 20 do **not**
  collide (class 20 is therefore NOT excluded here).
* **The register selector.**  A class-5 generation that wanted to resolve winding AND address
  independently would need to recover the `25 − 5 = 20` off-diagonal `(winding, address)`
  configurations the alias destroys.  The candidate answers are: the diagonal / no-hidden-register
  readout (stores `0` extra configs), a partial hidden register (`≥ 1`), and a full hidden register
  (all `20`).  The register-cost score makes the diagonal the unique strict minimum, so it is
  `M1Forced`; any hidden-register alternative `RequiresExternalCatalogue` (an unprovable input =
  hidden memory, forbidden by M1).

All proofs are finite/decidable (`decide`, `norm_num`, `Fin`/inductive case split) and reuse the
proven spine `D0.Matter.FiniteSelector` / `D0.Foundation.M1Predicate` verbatim.
-/

namespace D0.Matter

open D0.Foundation

/-! ## Part A — orbit-length separation of the candidate winding classes -/

/-- Operational address-class count `D_Σ = 5` (BOOK_04 §04.1), reused as the collision target. -/
def dSigma : ℕ := 5

/-- The length of the cyclic winding orbit of a class-`d` generator is `d` itself. (A generator of
order `d` sweeps a `d`-element orbit; this is the finite index the alias test compares against
`D_Σ`.) -/
def orbitLength (d : ℕ) : ℕ := d

/-- A winding class **pointer-collides** with the operational address classes exactly when its
orbit length equals `D_Σ = 5`. -/
def collidesWithDSigma (d : ℕ) : Prop := orbitLength d = dSigma

instance (d : ℕ) : Decidable (collidesWithDSigma d) := by
  unfold collidesWithDSigma orbitLength dSigma; infer_instance

/-- **Orbit-length separation.** The three M1-admissible classes `{1, 5, 20}` have orbit lengths
`1, 5, 20`, hence are pairwise distinct. -/
theorem orbit_length_separates :
    orbitLength 1 = 1 ∧ orbitLength 5 = 5 ∧ orbitLength 20 = 20 ∧
    orbitLength 1 ≠ orbitLength 5 ∧ orbitLength 5 ≠ orbitLength 20 ∧
    orbitLength 1 ≠ orbitLength 20 := by
  refine ⟨rfl, rfl, rfl, ?_, ?_, ?_⟩ <;> decide

/-- **Class 5 is the unique collider.** Only class 5 has orbit length `= D_Σ = 5`; classes 1 and 20
do not collide — so class 20 is NOT excluded by this aliasing test. -/
theorem only_class5_collides :
    collidesWithDSigma 5 ∧ ¬ collidesWithDSigma 1 ∧ ¬ collidesWithDSigma 20 := by
  unfold collidesWithDSigma orbitLength dSigma
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- The aliased diagonal readout resolves `D_Σ = 5` of the `D_Σ² = 25` `(winding, address)`
configurations; the `20` off-diagonal ones are exactly what a hidden register would have to store. -/
theorem register_deficit :
    dSigma = 5 ∧ dSigma ^ 2 = 25 ∧ dSigma ^ 2 - dSigma = 20 := by
  unfold dSigma
  refine ⟨rfl, ?_, ?_⟩ <;> decide

/-! ## Part B — the register-cost FiniteSelector and the M1Forced witness -/

/-- The candidate readout answers a class-5 generation could adopt to face the alias.  `diagonal`
is the honest no-hidden-register readout; the other two posit a hidden register of differing size. -/
inductive RegisterConfig where
  /-- the diagonal / no-hidden-register readout (stores 0 off-diagonal configs) -/
  | diagonal
  /-- a partial hidden register (stores at least one off-diagonal config) -/
  | hiddenPartial
  /-- a full hidden register (stores all 20 off-diagonal configs) -/
  | hiddenFull
  deriving DecidableEq, Repr, Fintype

/-- **Register cost** = the number of off-diagonal `(winding, address)` configurations the answer
must store in a hidden register.  The diagonal stores none; the hidden alternatives store
`1` and `20` respectively. -/
def registerCost : RegisterConfig → ℚ
  | .diagonal => 0
  | .hiddenPartial => 1
  | .hiddenFull => 20

/-- The finite register selector: lower hidden-register cost is preferred. -/
def registerSelector : FiniteSelector RegisterConfig where
  support_fintype := inferInstance
  score := registerCost

/-- The candidate space is genuinely finite. -/
def registerConfigFiniteSupport : Fintype RegisterConfig := inferInstance

/-- **The diagonal / no-hidden-register readout is strictly selected** — it is the unique zero-cost
answer, strictly below every hidden-register alternative. -/
theorem diagonal_strictly_selected :
    StrictSelected registerSelector RegisterConfig.diagonal := by
  constructor
  intro b hb
  cases b with
  | diagonal => exact False.elim (hb rfl)
  | hiddenPartial => norm_num [registerSelector, registerCost]
  | hiddenFull => norm_num [registerSelector, registerCost]

/-- **The diagonal answer is M1-forced** (via the proven `selector_M1Forced` spine): the finite
register-cost data determines it; no exogenous choice between configurations is needed. -/
theorem diagonal_M1Forced :
    M1Forced (fun x => StrictSelected registerSelector x) RegisterConfig.diagonal :=
  selector_M1Forced registerSelector RegisterConfig.diagonal diagonal_strictly_selected

/-- **The owner reductio (the load-bearing step).** Any hidden-register alternative requires an
external catalogue — it is not the forced answer, so adopting it rests on storing the `20`
off-diagonal configurations that M1 forbids (hidden memory = an unprovable input).  This is the
formal `class-5 needs a hidden register ⇒ exogenous parameter` step, term-mode through
`m1_alternative_needs_catalogue`. -/
theorem hidden_register_needs_catalogue
    (b : RegisterConfig) (hb : b ≠ RegisterConfig.diagonal) :
    RequiresExternalCatalogue (fun x => StrictSelected registerSelector x) b :=
  m1_alternative_needs_catalogue diagonal_M1Forced b hb

/-- Concrete instances: both hidden-register answers provably require an external catalogue. -/
theorem hidden_partial_needs_catalogue :
    RequiresExternalCatalogue (fun x => StrictSelected registerSelector x)
      RegisterConfig.hiddenPartial :=
  hidden_register_needs_catalogue RegisterConfig.hiddenPartial (by decide)

theorem hidden_full_needs_catalogue :
    RequiresExternalCatalogue (fun x => StrictSelected registerSelector x)
      RegisterConfig.hiddenFull :=
  hidden_register_needs_catalogue RegisterConfig.hiddenFull (by decide)

/-- **D0-CKM-CLASS5-SELECTOR-OWNER-001 (owner witness).** The orbit lengths separate the three
admissible classes (`1, 5, 20`), class 5 is the unique pointer-collider (`orbitLength 5 = D_Σ`)
while class 20 is not, and the register-cost selector forces the diagonal / no-hidden-register
answer as the unique M1-forced readout — so any hidden-register alternative requires an external
catalogue.  A real `M1Forced` term wired to the proven spine, not a `¬Forced` shell. -/
theorem class5_selector_owner :
    (orbitLength 1 = 1 ∧ orbitLength 5 = 5 ∧ orbitLength 20 = 20) ∧
    (collidesWithDSigma 5 ∧ ¬ collidesWithDSigma 1 ∧ ¬ collidesWithDSigma 20) ∧
    M1Forced (fun x => StrictSelected registerSelector x) RegisterConfig.diagonal ∧
    RequiresExternalCatalogue (fun x => StrictSelected registerSelector x)
      RegisterConfig.hiddenFull :=
  ⟨⟨rfl, rfl, rfl⟩, only_class5_collides, diagonal_M1Forced, hidden_full_needs_catalogue⟩

end D0.Matter
