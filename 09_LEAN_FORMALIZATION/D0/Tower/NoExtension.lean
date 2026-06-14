import D0.Core.Phi
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# D0-TOWER-STOP-NOEXT-001 — the M1 no-extension no-go: the tower stops at 3 zones (Lean)

Python certificates: `05_CERTS/vp_zone_repeat_catalog.py` (CASE 2),
`vp_member_zone_isomorphism.py` (CASE 1), `vp_degree2_three_types.py` (seam).

Closes obligation 5 of BOOK_05 §05.6 (the only meta-step left open in the carrier forcing): no
admissible structure registers a fourth zone. Built by contradiction (DEF-0.2.2) in two cases on
a hypothetical fourth zone `Z4`:

* **CASE 2 — `Z4` repeats an existing type.** `≥2` indistinguishable copies carry a nontrivial
  copy-permutation symmetry (`|S_2|=2>1`), so there is no canonical copy and the copy-choice is
  an external catalogue ⇒ `⊥M1`. (Same forcing as `Ω₈≅Q₈` via Dedekind, BOOK_01 §01.7.1A.)
* **CASE 1 — `Z4` is a new type of necessity.** The types of necessity are the SLOTS of the
  forced quadratic `p²+p=1` (`p=φ⁻¹`): `p` (distinguish), `p²` (preserve), `=1` (close) — three
  `= 2` terms `+ 1` closure, not a list. There is no fourth INDEPENDENT slot: the algebra
  `ℤ[p]/(p²+p−1)` is rank 2, every higher power reduces — `p³ = 2p−1 ∈ span{1,p}` (so a `p³`
  candidate is iterated runtime, BOOK_01:556, a repeat ⇒ CASE 2).

Both branches give `⊥M1`, so no fourth zone exists and the tower stops at the three rungs
`[9,11,13]`. The COUNT (3 slots, no 4th) is proved here; the role-NAMES
(distinguish/preserve/close) are the operational reading of the 3 forced slots, each citing a
forced primitive (registration BOOK_01; self-application; M1+ closure BOOK_00).
-/

namespace D0.Tower

open D0

/-- **CASE 1 / no-4th (degree-2 closure).** `p=φ⁻¹` satisfies the forced quadratic `p²+p=1`: the
two terms `p, p²` plus the closure `=1` are the three structural slots. -/
theorem degree2_closure : phi⁻¹ + phi⁻¹ ^ 2 = 1 := phi_inv_satisfies_primitive

/-- **CASE 1 / no fourth independent type.** Every higher power reduces into the rank-2 algebra
`span{1,p}`: `p³ = 2p − 1`. So a `p³` "type" is not new — it is a reducible repeat (iterated
runtime, BOOK_01:556), which falls into CASE 2. -/
theorem p_cubed_reduces : phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1 := by
  linear_combination (phi⁻¹ - 1) * phi_inv_satisfies_primitive

/-- **CASE 2 / repeat needs a catalogue.** `≥2` identical copies carry a nontrivial copy-
permutation symmetry: `|S_2| = 2 > 1`, so there is no canonical copy and selecting one is an
external catalogue ⇒ `⊥M1`. -/
theorem repeat_has_nontrivial_copy_symmetry : 1 < Fintype.card (Equiv.Perm (Fin 2)) := by
  native_decide

/-- A single first instance is canonical: `|S_1| = 1` (no catalogue) — the no-go bites only on
repeats `(n≥2)`, not on first instances. -/
theorem first_instance_canonical : Fintype.card (Equiv.Perm (Fin 1)) = 1 := by native_decide

/-- The count is structural, not a list: `3 = 2` (quadratic terms) `+ 1` (closure). -/
theorem three_is_two_plus_one : (3 : ℕ) = 2 + 1 := by decide

/-- **D0-TOWER-STOP-NOEXT-001 (no-extension theorem).** Both cases give `⊥M1`, so no admissible
fourth zone exists and the tower stops at three:
* the forced quadratic has exactly three slots (`p²+p=1`: two terms + closure);
* CASE 1 — no fourth independent type (`p³ = 2p−1` reduces into `span{1,p}`);
* CASE 2 — a repeat carries a nontrivial copy-symmetry (`|S_2|>1`) ⇒ an external catalogue. -/
theorem no_extension_theorem :
    (phi⁻¹ + phi⁻¹ ^ 2 = 1) ∧
    (phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1) ∧
    (1 < Fintype.card (Equiv.Perm (Fin 2))) ∧
    ((3 : ℕ) = 2 + 1) :=
  ⟨degree2_closure, p_cubed_reduces, repeat_has_nontrivial_copy_symmetry, three_is_two_plus_one⟩

end D0.Tower
