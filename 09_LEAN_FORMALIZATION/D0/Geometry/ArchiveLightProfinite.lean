import D0.Geometry.ArchiveRefinementTower
import Mathlib.CategoryTheory.Functor.OfSequence
import Mathlib.CategoryTheory.FintypeCat
import Mathlib.Topology.Category.Profinite.Basic
import Mathlib.Topology.Category.LightProfinite.Basic

/-!
# D0-ARCHIVE-LIGHTPROFINITE-001 — the archive tower as a genuine Mathlib `LightProfinite`

`D0.Geometry.ArchiveRefinementTower` proved the archive tower's inverse limit is nonempty using a
bespoke `InverseLimit` subtype of a hand-rolled `FiniteInverseSystem`. This module UPGRADES that to
the real Mathlib categorical object: the tower is a genuine `ℕᵒᵖ ⥤ FintypeCat` diagram (objects = the
finite archive levels `ArchivePoints n = Fin (modes n)`, bonding maps `n+1 ⟶ n` = `archiveProjection`),
and its limit in `Profinite` packages as a `LightProfinite` (a compact Hausdorff totally-disconnected,
second-countable space). Reuses `Functor.ofOpSequence`, `FintypeCat.of`/`homMk`, `LightDiagram`, and
`lightDiagramToLightProfinite` from the pinned Mathlib — no new dependency.
-/

namespace D0

open CategoryTheory CategoryTheory.Limits

/-- The archive refinement tower as a sequential diagram of finite sets: level `n` is the finite set
`ArchivePoints n = Fin (modes n)`, and the bonding map `n+1 ⟶ n` is `archiveProjection n`. -/
noncomputable def archiveFintypeDiagram : ℕᵒᵖ ⥤ FintypeCat :=
  Functor.ofOpSequence (X := fun n => FintypeCat.of (ArchivePoints n))
    (fun n => FintypeCat.homMk (archiveProjection n))

/-- The `n`-th object of the archive diagram is the finite archive level `ArchivePoints n`. -/
@[simp] theorem archiveFintypeDiagram_obj (n : ℕ) :
    archiveFintypeDiagram.obj (Opposite.op n) = FintypeCat.of (ArchivePoints n) := rfl

/-- The successor transition map of the archive diagram IS the archive projection. -/
theorem archiveFintypeDiagram_succ (n : ℕ) :
    archiveFintypeDiagram.map (homOfLE (Nat.le_add_right n 1)).op
      = FintypeCat.homMk (archiveProjection n) :=
  Functor.ofOpSequence_map_homOfLE_succ _ n

/-- The bonding maps of the archive diagram are surjective (they are the surjective `archiveProjection`). -/
theorem archiveDiagram_transition_surjective (n : ℕ) :
    Function.Surjective (archiveFintypeDiagram.map (homOfLE (Nat.le_add_right n 1)).op) := by
  rw [archiveFintypeDiagram_succ]
  intro y
  obtain ⟨x, hx⟩ := archive_projection_surjective n y
  exact ⟨x, by simpa using hx⟩

/-- The archive tower's limit data in `Profinite`: the diagram together with its (existing) limit cone. -/
noncomputable def archiveLightDiagram : LightDiagram where
  diagram := archiveFintypeDiagram
  cone := limit.cone (archiveFintypeDiagram ⋙ FintypeCat.toProfinite)
  isLimit := limit.isLimit _

/-- **The archive refinement tower as a genuine `LightProfinite`.** The inverse limit of the finite
archive levels, realised as a real compact Hausdorff totally-disconnected second-countable space via
Mathlib's `Profinite`/`LightProfinite` machinery — the categorical upgrade of the bespoke
`archive_tower_defines_profinite_object` nonempty-inverse-limit witness. -/
noncomputable def archiveLightProfinite : LightProfinite :=
  lightDiagramToLightProfinite.obj archiveLightDiagram

/-- The underlying space of `archiveLightProfinite` is the limit cone point of the archive diagram. -/
theorem archiveLightProfinite_def :
    archiveLightProfinite = LightProfinite.of archiveLightDiagram.cone.pt := rfl

end D0
