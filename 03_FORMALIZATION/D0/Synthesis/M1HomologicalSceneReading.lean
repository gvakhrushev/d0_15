import D0.Foundation.EquivariantM1
import D0.SelfReading.TypedCapacityRawScene
import D0.Synthesis.CarrierTopologicalScenePassport
import Mathlib.Tactic

/-!
# D0-M1-HOMOLOGICAL-SCENE-READING-001

This module joins three previously separate parts of the corpus:

* the proof-theoretic forcing predicate `M1Forced`;
* the actual rational top homology of complete tripartite clique complexes;
* the within-zone relabeling gauge of the typed `9+11+13` scene.

The result has a positive and a negative half.

1. Among ordered canonical complete-tripartite candidates, the two intrinsic
   coordinates

   ```
   |V| = 33,  β₂ = 960
   ```

   M1-force the unique reduced sizes `(p,q,r)=(8,10,12)`, hence the zone
   sizes `(9,11,13)`.  Here `β₂` is not a declared product: it is the finrank
   of the kernel of the proved generic boundary matrix.

2. No predicate invariant under local relabelings
   `S₉ × S₁₁ × S₁₃` can M1-force an individual typed vertex.  Every vertex is
   moved by a swap inside its own zone.

Together these give a precise self-reading boundary: the homological carrier
data force the quotient scene (the three zone cardinalities), while symmetry
forbids upgrading that quotient datum to a preferred vertex name.

Both coordinates are load-bearing.  Vertex count alone also admits
`(p,q,r)=(7,10,13)`; top Betti number alone also admits `(8,8,15)`.

Honest scope: this is a reconstruction theorem inside the ordered canonical
positive complete-tripartite class.  It does not derive the observed
coordinates `33` and `960` from M1 alone, nor does it identify arbitrary
finite complexes from their Betti numbers.
-/

namespace D0.Synthesis.M1HomologicalSceneReading

open D0.Foundation
open D0.Foundation.EquivariantM1
open D0.SelfReading.TypedCapacityRawScene
open D0.Synthesis.CarrierTopologicalScenePassport
open D0.Topology.GenericTripartiteHomology

/-- Ordered reduced-size coordinates for the canonical zones
`Fin (p+1)`, `Fin (q+1)`, `Fin (r+1)`. -/
@[ext]
structure OrderedTripartiteCandidate where
  p : ℕ
  q : ℕ
  r : ℕ
  hpq : p ≤ q
  hqr : q ≤ r

/-- The reduced source coordinates corresponding to zone sizes `(9,11,13)`. -/
def sourceScene : OrderedTripartiteCandidate where
  p := 8
  q := 10
  r := 12
  hpq := by omega
  hqr := by omega

/-- The actual mixed carrier/homology obligation. -/
def HomologicalSceneConstraint (S : OrderedTripartiteCandidate) : Prop :=
  Fintype.card (GenericVertex S.p S.q S.r) = 33 ∧
    canonicalTopBetti S.p S.q S.r = 960

theorem sourceScene_satisfies_homological_constraint :
    HomologicalSceneConstraint sourceScene := by
  exact scene_canonical_vertex_beta2_coordinates

/-- **Positive synthesis.** Actual vertex carrier plus actual top homology
M1-force the source scene inside the stated candidate class. -/
theorem homological_scene_m1_forced :
    M1Forced HomologicalSceneConstraint sourceScene where
  forced := sourceScene_satisfies_homological_constraint
  unique := by
    intro S hS
    have hReconstruct :=
      reconstruct_canonical_fin_from_vertex_beta2
        S.p S.q S.r S.hpq S.hqr hS.1 hS.2
    have hCoordinates :
        (S.p + 1, S.q + 1, S.r + 1) = (9, 11, 13) := by
      simpa using hReconstruct
    have hp : S.p = 8 := by
      have h := congrArg
        (fun t : ℕ × ℕ × ℕ => t.1) hCoordinates
      simp at h
      omega
    have hq : S.q = 10 := by
      have h := congrArg
        (fun t : ℕ × ℕ × ℕ => t.2.1) hCoordinates
      simp at h
      omega
    have hr : S.r = 12 := by
      have h := congrArg
        (fun t : ℕ × ℕ × ℕ => t.2.2) hCoordinates
      simp at h
      omega
    apply OrderedTripartiteCandidate.ext
    · exact hp
    · exact hq
    · exact hr

/-! ## Both coordinates are necessary -/

def vertexOnlyRival : OrderedTripartiteCandidate where
  p := 7
  q := 10
  r := 13
  hpq := by omega
  hqr := by omega

def betaOnlyRival : OrderedTripartiteCandidate where
  p := 8
  q := 8
  r := 15
  hpq := by omega
  hqr := by omega

def VertexOnlyConstraint (S : OrderedTripartiteCandidate) : Prop :=
  Fintype.card (GenericVertex S.p S.q S.r) = 33

def BetaOnlyConstraint (S : OrderedTripartiteCandidate) : Prop :=
  canonicalTopBetti S.p S.q S.r = 960

theorem sourceScene_vertex_only : VertexOnlyConstraint sourceScene := by
  norm_num [VertexOnlyConstraint, sourceScene, GenericVertex]

theorem vertexOnlyRival_vertex_only :
    VertexOnlyConstraint vertexOnlyRival := by
  norm_num [VertexOnlyConstraint, vertexOnlyRival, GenericVertex]

theorem vertexOnlyRival_ne_source :
    vertexOnlyRival ≠ sourceScene := by
  intro h
  have hp := congrArg OrderedTripartiteCandidate.p h
  norm_num [vertexOnlyRival, sourceScene] at hp

theorem vertex_count_alone_not_m1_forced :
    ¬ M1Forced VertexOnlyConstraint sourceScene := by
  intro h
  exact vertexOnlyRival_ne_source
    (h.unique vertexOnlyRival vertexOnlyRival_vertex_only)

theorem sourceScene_beta_only : BetaOnlyConstraint sourceScene := by
  rw [show BetaOnlyConstraint sourceScene =
      (canonicalTopBetti 8 10 12 = 960) by rfl]
  rw [canonical_top_betti_formula]

theorem betaOnlyRival_beta_only :
    BetaOnlyConstraint betaOnlyRival := by
  rw [show BetaOnlyConstraint betaOnlyRival =
      (canonicalTopBetti 8 8 15 = 960) by rfl]
  rw [canonical_top_betti_formula]

theorem betaOnlyRival_ne_source :
    betaOnlyRival ≠ sourceScene := by
  intro h
  have hq := congrArg OrderedTripartiteCandidate.q h
  norm_num [betaOnlyRival, sourceScene] at hq

theorem beta2_alone_not_m1_forced :
    ¬ M1Forced BetaOnlyConstraint sourceScene := by
  intro h
  exact betaOnlyRival_ne_source
    (h.unique betaOnlyRival betaOnlyRival_beta_only)

/-! ## Local symmetry forbids a preferred vertex -/

/-- The genuine local gauge group: labels may change independently inside
each typed zone, but zones are not mixed. -/
abbrev LocalRelabelling :=
  Equiv.Perm V9T × Equiv.Perm V11T × Equiv.Perm V13T

/-- Action of the local relabeling gauge on typed vertices. -/
def localRelabel : LocalRelabelling → TypedVertex → TypedVertex
  | σ, .zone9 x => .zone9 (σ.1 x)
  | σ, .zone11 x => .zone11 (σ.2.1 x)
  | σ, .zone13 x => .zone13 (σ.2.2 x)

/-- Every vertex is moved by some relabeling confined to its own zone. -/
theorem every_typed_vertex_is_locally_movable :
    ∀ v : TypedVertex, ∃ σ : LocalRelabelling, localRelabel σ v ≠ v := by
  classical
  letI : Nontrivial V9T :=
    Fintype.one_lt_card_iff_nontrivial.mp (by
      rw [D0.card_v9]
      norm_num)
  letI : Nontrivial V11T :=
    Fintype.one_lt_card_iff_nontrivial.mp (by
      rw [D0.card_v11]
      norm_num)
  letI : Nontrivial V13T :=
    Fintype.one_lt_card_iff_nontrivial.mp (by
      rw [D0.card_v13]
      norm_num)
  intro v
  cases v with
  | zone9 x =>
      obtain ⟨y, hyx⟩ := exists_ne x
      refine ⟨(Equiv.swap x y, 1, 1), ?_⟩
      simp [localRelabel, hyx]
  | zone11 x =>
      obtain ⟨y, hyx⟩ := exists_ne x
      refine ⟨(1, Equiv.swap x y, 1), ?_⟩
      simp [localRelabel, hyx]
  | zone13 x =>
      obtain ⟨y, hyx⟩ := exists_ne x
      refine ⟨(1, 1, Equiv.swap x y), ?_⟩
      simp [localRelabel, hyx]

/-- A scene-vertex obligation is intrinsic only if it is invariant under the
local within-zone gauge. -/
def LocalSceneInvariant (Forced : TypedVertex → Prop) : Prop :=
  SymmetryInvariant localRelabel Forced

/-- **Negative synthesis.** No locally intrinsic obligation can M1-force an
individual typed scene vertex. -/
theorem no_invariant_m1_forced_scene_vertex
    (Forced : TypedVertex → Prop)
    (hInvariant : LocalSceneInvariant Forced) :
    ¬ ∃ v, M1Forced Forced v :=
  no_m1_forced_of_pointwise_movable
    localRelabel every_typed_vertex_is_locally_movable Forced hInvariant

/-- One bundled statement of the quotient/representative boundary. -/
theorem m1_homological_scene_reading :
    M1Forced HomologicalSceneConstraint sourceScene ∧
      (∀ Forced : TypedVertex → Prop,
        LocalSceneInvariant Forced →
          ¬ ∃ v, M1Forced Forced v) := by
  exact ⟨homological_scene_m1_forced,
    no_invariant_m1_forced_scene_vertex⟩

end D0.Synthesis.M1HomologicalSceneReading
