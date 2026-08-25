import D0.Core.Phi
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# D0-TOWER-STOP-NOEXT-001 — algebraic inputs to the M1 no-extension no-go

Python certificates: `05_CERTS/vp_zone_repeat_catalog.py` (CASE 2),
`vp_member_zone_isomorphism.py` (CASE 1), `vp_degree2_three_types.py` (seam).

Formalizes three inputs used by the prose no-extension argument. It does **not** yet define an
arbitrary scene candidate, formalize M1-admissibility, or prove a quantified statement excluding a
fourth zone. The missing conversion from these inputs to an injective classification of all zones
into three slots is exposed as a typed interpretation in `D0.Foundation.SceneCountReduction`.

The prose argument proceeds by contradiction (DEF-0.2.2) in two cases on a hypothetical fourth
zone `Z4`:

* **CASE 2 — `Z4` repeats an existing type.** `≥2` indistinguishable copies carry a nontrivial
  copy-permutation symmetry (`|S_2|=2>1`), so there is no canonical copy and the copy-choice is
  an external catalogue ⇒ `⊥M1`. (Same forcing as `Ω₈≅Q₈` via Dedekind, BOOK_01 §01.7.1A.)
* **CASE 1 — `Z4` is a new type of necessity.** The prose identifies the types of necessity with
  the SLOTS of the
  forced quadratic `p²+p=1` (`p=φ⁻¹`): `p` (distinguish), `p²` (preserve), `=1` (close) — three
  `= 2` terms `+ 1` closure, not a list. There is no fourth INDEPENDENT slot: the algebra
  `ℤ[p]/(p²+p−1)` is rank 2 and every higher power reduces.

`D0.Tower.NoExtensionBoundary` proves that the last inference does not follow: `p³ = 2p−1` is
still distinct from `1`, `p`, and `p²`, and in fact all powers `pⁿ` are distinct. Thus identifying
algebraic dependence with a repeated structural type needs a separate semantic theorem.

Turning these two branches into `⊥M1` still requires formal definitions of "new type", "repeat",
"external catalogue", and scene admissibility. Consequently the count is not claimed by this
module; only the algebraic and finite-symmetry premises below are.
-/

namespace D0.Tower

open D0

/-- **CASE 1 / no-4th (degree-2 closure).** `p=φ⁻¹` satisfies the forced quadratic `p²+p=1`: the
two terms `p, p²` plus the closure `=1` are the three structural slots. -/
theorem degree2_closure : phi⁻¹ + phi⁻¹ ^ 2 = 1 := phi_inv_satisfies_primitive

/-- **CASE 1 algebraic input.** The next power reduces into the rank-2 algebra
`span{1,p}`: `p³ = 2p − 1`. This is a linear-dependence theorem, not an equality with one of the
first three values and therefore not, by itself, a no-new-type theorem. -/
theorem p_cubed_reduces : phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1 := by
  linear_combination (phi⁻¹ - 1) * phi_inv_satisfies_primitive

/-- **CASE 2 arithmetic input.** Two copies carry a nontrivial copy-permutation symmetry:
`|S_2| = 2 > 1`. The actual M1 no-go, requiring a relabelling-invariant constraint and proving it
cannot force a copy, is `NoExtensionBoundary.repeated_zone_type_not_m1_forced`. -/
theorem repeat_has_nontrivial_copy_symmetry : 1 < Fintype.card (Equiv.Perm (Fin 2)) := by
  native_decide

/-- A single first instance is canonical: `|S_1| = 1` (no catalogue) — the no-go bites only on
repeats `(n≥2)`, not on first instances. -/
theorem first_instance_canonical : Fintype.card (Equiv.Perm (Fin 1)) = 1 := by native_decide

/-- **D0-TOWER-STOP-NOEXT-001 (owner-fact bundle).** The three machine-checked premises used by the
two prose cases:
* the forced quadratic closes at degree 2 (`p²+p=1`);
* CASE 1 — the candidate higher power reduces (`p³ = 2p−1`);
* CASE 2 — two copies carry a nontrivial copy-symmetry (`|S_2|>1`).

The implications "reducible power ⇒ no new admissible zone" and "copy symmetry ⇒ external
catalogue ⇒ `⊥M1`" are not propositions in this file, so this conjunction alone is not a quantified
no-fourth-zone theorem.
(The decorative `3 = 2+1` conjunct was dropped 2026-06-24 per the corpus over-claim sweep — a vacuous
arithmetic fact that added no content; the theorem now rests only on the three substantive facts.) -/
theorem no_extension_theorem :
    (phi⁻¹ + phi⁻¹ ^ 2 = 1) ∧
    (phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1) ∧
    (1 < Fintype.card (Equiv.Perm (Fin 2))) :=
  ⟨degree2_closure, p_cubed_reduces, repeat_has_nontrivial_copy_symmetry⟩

end D0.Tower
