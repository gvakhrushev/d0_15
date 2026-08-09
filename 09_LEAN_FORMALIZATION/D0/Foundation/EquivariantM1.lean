import D0.Foundation.M1Predicate
import Mathlib.Tactic

/-!
# D0-EQUIVARIANT-M1-001 — forcing lives on symmetry quotients

`M1Forced` says that a finite obligation has one admissible answer.  This file
adds the missing symmetry theorem.  If the obligation is invariant under a
family of transformations, then its unique answer must be fixed by every
transformation.  Hence a symmetry orbit with no common fixed point cannot
contain an M1-forced representative.

Unlike the full-relabeling result in `D0.Tower.NoExtensionBoundary`, the
transformations here may be any specified action family.  This is needed for
the scene application: local relabelings preserve each of the three zones and
are a proper subgroup of all permutations of the 33 vertices.

No group laws are required.  The result uses only the operational content of
symmetry: preservation of the forcing predicate.
-/

namespace D0.Foundation.EquivariantM1

open D0.Foundation

/-- A forcing predicate is invariant under the supplied transformation
family.  Group laws are deliberately not assumed: invariance is the only
property used by the no-go theorem. -/
def SymmetryInvariant {G α : Type}
    (act : G → α → α) (Forced : α → Prop) : Prop :=
  ∀ g x, Forced x ↔ Forced (act g x)

/-- An M1-forced answer under an invariant obligation is fixed by every
allowed symmetry. -/
theorem m1_forced_is_fixed_under_symmetry
    {G α : Type} {act : G → α → α} {Forced : α → Prop} {a : α}
    (hInvariant : SymmetryInvariant act Forced)
    (ha : M1Forced Forced a) :
    ∀ g, act g a = a := by
  intro g
  exact ha.unique (act g a) ((hInvariant g a).mp ha.forced)

/-- If every candidate is moved by at least one allowed symmetry, no
symmetry-invariant obligation can M1-force a representative. -/
theorem no_m1_forced_of_pointwise_movable
    {G α : Type} (act : G → α → α)
    (hMovable : ∀ a, ∃ g, act g a ≠ a)
    (Forced : α → Prop)
    (hInvariant : SymmetryInvariant act Forced) :
    ¬ ∃ a, M1Forced Forced a := by
  rintro ⟨a, ha⟩
  obtain ⟨g, hg⟩ := hMovable a
  exact hg (m1_forced_is_fixed_under_symmetry hInvariant ha g)

/-- Equivalent local reading: forcing a moved point necessarily breaks the
specified symmetry. -/
theorem forcing_moved_point_breaks_symmetry
    {G α : Type} {act : G → α → α} {Forced : α → Prop} {a : α}
    (ha : M1Forced Forced a)
    (hMoved : ∃ g, act g a ≠ a) :
    ¬ SymmetryInvariant act Forced := by
  intro hInvariant
  obtain ⟨g, hg⟩ := hMoved
  exact hg (m1_forced_is_fixed_under_symmetry hInvariant ha g)

/-! ## Negative control

The obstruction is movement, not the mere presence of a symmetry parameter.
The trivial action fixes every point, so a genuine singleton obligation may
still be M1-forced and invariant.
-/

def trivialAct {G α : Type} : G → α → α := fun _ x => x

def zeroOnly : Fin 2 → Prop := fun x => x = 0

theorem zeroOnly_m1_forced : M1Forced zeroOnly 0 where
  forced := rfl
  unique := by
    intro b hb
    exact hb

theorem zeroOnly_trivial_invariant :
    SymmetryInvariant (trivialAct (G := Fin 3) (α := Fin 2)) zeroOnly := by
  intro g x
  rfl

end D0.Foundation.EquivariantM1
