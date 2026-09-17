import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Logic.Equiv.Fintype
import Mathlib.Tactic

/-!
# D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 (EQUIVARIANT arm, decidable no-go)

Python certificates: `04_CERTIFICATES/vp_selector_obstruction_nogo.py` (equivariant core, 25/25),
`04_CERTIFICATES/vp_selector_ssb_nogo.py`, `04_CERTIFICATES/vp_selector_dynamical_nogo.py`,
`04_CERTIFICATES/vp_selector_basepoint_nogo.py`.

**The equivariant sub-claim (this module, theorem-grade).**
Frozen scene `K(9,11,13)`, zones `V₉ ⊔ V₁₁ ⊔ V₁₃`, automorphism group
`Aut(K) = S₉ × S₁₁ × S₁₃` (BOOK_01:1576 orbital theorem; BOOK_04:1399). A **within-zone
labeling** of a zone `Vₙ` is a bijection `Vₙ → Lₙ` onto a fixed label alphabet `|Lₙ| = n`; up to
identifying the alphabet with `Fin n`, the set of labelings is `Equiv.Perm (Fin n)`. `Aut(K)`
restricts on zone `n` to the full symmetric group `Sₙ = Equiv.Perm (Fin n)` acting by
**precomposition** `g • b = b ∘ g⁻¹` (relabel which vertex carries which label). This is the
labeling **torsor**.

An `Aut`-**equivariant** canonical labeling is a section fixed by the whole `Sₙ`-action: a
bijection `b` with `b ∘ g⁻¹ = b` for **every** `g ∈ Sₙ`. This module proves, as a decidable
theorem on the finite structure, that

> **the number of `Sₙ`-fixed labelings is `0` for every `n ≥ 2`** (`1` for `n = 1`, the control).

Hence over `Aut(K) = S₉ × S₁₁ × S₁₃` (product action) the joint equivariant-section count is the
product of the per-zone counts, so it is `0`: **no internal `Aut`-equivariant canonical within-zone
labeling of `K(9,11,13)` exists.** The obstruction to an internal equivariant selector is
non-trivial.

**Proof idea (the invariance wall).** `Sₙ` acts *simply transitively* on `Equiv.Perm (Fin n)`
(the labelings): if `b ∘ g⁻¹ = b` and `b` is a bijection then `g⁻¹ = 1`, i.e. `g = 1`. So a
labeling fixed by *all* of `Sₙ` forces `g = 1` for every `g`, which fails as soon as `Sₙ` has a
non-identity element (`n ≥ 2`). Equivalently: an `Sₙ`-invariant function `Vₙ → Lₙ` is constant on
the single `Sₙ`-orbit of vertices, hence not injective for `n ≥ 2`.

**Honest scope (must stay in the notes).** This module closes ONLY the **equivariant** selector
class (arm X3a). It does NOT close the fully-general "any owned internal rule" case (X3b): the
SSB / dynamical / basepoint mechanisms are non-equivariant by construction and are handled by the
finite Python certificates via the M1 *relocation-of-catalog* test (every inspected mechanism
relocates the catalog; each owned functional is a class function of `Sₙ` so its extrema are
`Sₙ`-fixed or a degenerate `Sₙ`-orbit, never a unique non-symmetric point). X3b is **evidence**
(a completed mechanism sweep + the class-function argument), NOT a single universal impossibility
theorem. Only the equivariant arm is a Lean theorem; this is stated honestly and not over-claimed.

Cross-refs: extends `M2_PHASE_LABELING_MEMO` (detector-shell torsor up to `G_res`);
`D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001` (the triangle-level analogue,
`D0.Matter.DSigmaRoleCycleCarrierNoGo`); `D0-CARRIER-NOT-ICOSAHEDRAL-001`
(`D0.Claims.CarrierNotIcosahedral`, the complementary zone-*class* triviality); instantiates
`D0-M1-PREDICATE-001` (`D0.Foundation.M1Predicate`).
-/

namespace D0.Foundation.CanonicalSelectorNoGo

open Equiv

/-- The set of `Sₙ`-**equivariant** within-zone labelings of a zone of size `n`: bijections
`b : Fin n ≃ Fin n` (the labelings) that are fixed by the precomposition action `g • b = b ∘ g⁻¹`
of *every* `g ∈ Sₙ`. `Fintype`/`DecidableEq` on `Equiv.Perm (Fin n)` make this a decidable finite
filter, so its cardinality is computable. -/
def equivariantSections (n : ℕ) : Finset (Equiv.Perm (Fin n)) :=
  Finset.univ.filter (fun b => ∀ g : Equiv.Perm (Fin n), b.trans g⁻¹ = b)

/-! ### Concrete decidable checks on small `n` (surrogate for the general theorem)

These mirror `selector_obstruction_check.py`: `n = 1` is the control (a section *does* exist, so
the code can see one), `n = 2,3,4` measure the *absence* of an equivariant section. All four use
`native_decide` (compiled evaluation): kernel `decide` cannot reduce the `Fintype (Fin n ≃ Fin n)`
instance (built through embeddings/`Trunc`) in reasonable time even at `n = 1`. Concrete
enumeration is deliberately capped at `n ≤ 4` (`4! = 24` labelings); the zones `n = 9,11,13` are
handled ONLY by the abstract theorem below — nothing in this module evaluates `Perm (Fin n)` as a
`Finset` for `n > 4`. -/

/-- **Control (`n = 1`).** A size-1 zone admits exactly one labeling and it is trivially
equivariant — so the count is `1`. This guards against a vacuous "always reports 0" checker: the
measurement genuinely distinguishes existence from non-existence. -/
theorem control_n1_has_section : (equivariantSections 1).card = 1 := by native_decide

/-- `n = 2`: **no** equivariant section (the count is `0`). -/
theorem no_section_n2 : (equivariantSections 2).card = 0 := by native_decide

/-- `n = 3`: **no** equivariant section. -/
theorem no_section_n3 : (equivariantSections 3).card = 0 := by native_decide

/-- `n = 4`: **no** equivariant section. -/
theorem no_section_n4 : (equivariantSections 4).card = 0 := by native_decide

/-! ### The general theorem (why the small-`n` checks suffice for `n = 9,11,13`)

The count is `0` for *every* `n ≥ 2`, proved abstractly: a labeling fixed by all of `Sₙ` forces
every `g ∈ Sₙ` to be the identity, impossible once a non-identity permutation exists. -/

/-- A labeling `b` fixed by the whole `Sₙ`-action forces **every** `g ∈ Sₙ` to be the identity.
(`b.trans g⁻¹ = b` with `b` a bijection cancels to `g⁻¹ = 1`, i.e. `g = 1`.) -/
theorem fixed_forces_all_identity {n : ℕ} {b : Equiv.Perm (Fin n)}
    (hb : ∀ g : Equiv.Perm (Fin n), b.trans g⁻¹ = b) :
    ∀ g : Equiv.Perm (Fin n), g = 1 := by
  intro g
  -- `b.trans g⁻¹ = b` is `g⁻¹ * b = b` in the permutation group; cancel `b` on the right.
  have h : g⁻¹ * b = 1 * b := by
    rw [one_mul, Equiv.Perm.mul_def]
    exact hb g
  exact inv_eq_one.mp (mul_right_cancel h)

/-- Pointwise form of the no-go: for `n ≥ 2` **no** labeling is fixed by the whole `Sₙ`-action.
(A fixed `b` would force the swap of two distinct points to be the identity.) -/
theorem no_fixed_labeling {n : ℕ} (hn : 2 ≤ n) (b : Equiv.Perm (Fin n)) :
    ¬ (∀ g : Equiv.Perm (Fin n), b.trans g⁻¹ = b) := by
  intro hb
  -- two distinct points of `Fin n` (they exist since `n ≥ 2`)
  obtain ⟨x, y, hxy⟩ : ∃ x y : Fin n, x ≠ y :=
    ⟨⟨0, by omega⟩, ⟨1, by omega⟩, by
      intro h
      have h' : (0 : ℕ) = 1 := congrArg Fin.val h
      omega⟩
  -- from `b` fixed by all `g`, every `g` is the identity; contradict the non-identity swap.
  have hswap : Equiv.swap x y = 1 := fixed_forces_all_identity hb (Equiv.swap x y)
  have happ : Equiv.swap x y x = y := Equiv.swap_apply_left x y
  rw [hswap, Equiv.Perm.one_apply] at happ
  exact hxy happ

/-- **The equivariant no-go, general form.** For every `n ≥ 2` the set of `Sₙ`-equivariant
within-zone labelings is empty (its cardinality is `0`): a fixed labeling would force the
non-identity permutation that exists at `n ≥ 2` to be the identity. Purely abstract — no
enumeration of `Perm (Fin n)`, so instantiating at `n = 9, 11, 13` is free. -/
theorem no_equivariant_section {n : ℕ} (hn : 2 ≤ n) : (equivariantSections n).card = 0 := by
  rw [Finset.card_eq_zero]
  unfold equivariantSections
  rw [Finset.filter_eq_empty_iff]
  exact fun b _ => no_fixed_labeling hn b

/-! ### The scene `K(9,11,13)` and the joint product count -/

/-- Applied to the three actual zones `n ∈ {9,11,13}`: each has `0` equivariant sections. -/
theorem scene_zones_no_section :
    (∀ b : Equiv.Perm (Fin 9),  ¬ (∀ g, b.trans g⁻¹ = b)) ∧
    (∀ b : Equiv.Perm (Fin 11), ¬ (∀ g, b.trans g⁻¹ = b)) ∧
    (∀ b : Equiv.Perm (Fin 13), ¬ (∀ g, b.trans g⁻¹ = b)) :=
  ⟨no_fixed_labeling (by omega), no_fixed_labeling (by omega), no_fixed_labeling (by omega)⟩

/-- **D0-CANONICAL-WITHIN-ZONE-SELECTOR-M1-NOGO-001 (equivariant arm).** Over
`Aut(K) = S₉ × S₁₁ × S₁₃` the joint equivariant-section count is the product of the per-zone
counts. Each per-zone count is `0` (`no_equivariant_section`, verified concretely for the small
surrogates `n = 2,3,4`), so the joint count is `0 · 0 · 0 = 0`: **no internal `Aut`-equivariant
canonical within-zone labeling of `K(9,11,13)` exists.** The `n = 1` control shows the count is a
real measurement of absence (it reports `1` when a section exists). -/
theorem canonical_within_zone_selector_nogo :
    (equivariantSections 9).card = 0 ∧
    (equivariantSections 11).card = 0 ∧
    (equivariantSections 13).card = 0 ∧
    ((equivariantSections 9).card * (equivariantSections 11).card
      * (equivariantSections 13).card = 0) ∧
    (equivariantSections 1).card = 1 := by
  -- Rewrite ALL three cardinalities to the literal `0` BEFORE any arithmetic step: leaving
  -- a symbolic `(equivariantSections n).card` inside a `Nat` operation invites the kernel to
  -- normalize it to a literal — i.e. to enumerate `Perm (Fin n)` (`11! ≈ 4·10⁷` elements) —
  -- which is exactly the compile-hang this module twice hit. After the three rewrites the
  -- product goal is the literal `0 * 0 * 0 = 0` (closed by `rfl`).
  have h9  : (equivariantSections 9).card  = 0 := no_equivariant_section (by omega)
  have h11 : (equivariantSections 11).card = 0 := no_equivariant_section (by omega)
  have h13 : (equivariantSections 13).card = 0 := no_equivariant_section (by omega)
  exact ⟨h9, h11, h13, by rw [h9, h11, h13], control_n1_has_section⟩

end D0.Foundation.CanonicalSelectorNoGo
