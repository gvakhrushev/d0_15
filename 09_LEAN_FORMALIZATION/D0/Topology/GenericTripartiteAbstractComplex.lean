import D0.Topology.GenericTripartiteHomology
import Mathlib.AlgebraicTopology.SimplicialComplex.Basic
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-ABSTRACT-COMPLEX-001

This module constructs the actual Mathlib `AbstractSimplicialComplex` of the
canonical complete-tripartite clique complex `K(p+1,q+1,r+1)`.  A face is a
nonempty finite vertex set containing at most one vertex from each zone.

Two presentations are proved equivalent:

* a coordinate face with one optional coordinate in each zone;
* the typed face carrier `vertex | edge | triangle` already used by the chain
  complex.

The final equivalence identifies those typed cells with the literal face
subtype of `abstractComplex`.  Thus the earlier boundary matrices now have an
explicit underlying abstract simplicial complex rather than only typed
incidence carriers.

This module does not yet assert anything about geometric realization or
spatial homotopy type.
-/

namespace D0.Topology.GenericTripartiteAbstractComplex

open D0.Topology.GenericTripartiteHomology

variable {p q r : ℕ}
local notation "Vertex" => GenericVertex p q r

/-- Zone label of a canonical tripartite vertex. -/
def zone : Vertex → Fin 3
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl _) => 1
  | Sum.inr (Sum.inr _) => 2

/-- Vertices are compatible precisely when they lie in different zones. -/
def CrossZone (x y : Vertex) : Prop := zone x ≠ zone y

/-- Mathlib abstract simplicial complex of nonempty cross-zone vertex sets. -/
def abstractComplex : AbstractSimplicialComplex Vertex where
  faces := {s | s.Nonempty ∧ (s : Set Vertex).Pairwise CrossZone}
  isRelLowerSet_faces := by
    intro s hs
    refine ⟨hs.1, ?_⟩
    intro t hts ht
    exact ⟨ht, Set.Pairwise.mono (by simpa using hts) hs.2⟩
  singleton_mem v := by
    constructor <;> simp

abbrev RawFaceCoordinates (p q r : ℕ) :=
  Option (Fin (p+1)) × (Option (Fin (q+1)) × Option (Fin (r+1)))

/-- Coordinate presentation of a nonempty face: at most one vertex per zone. -/
abbrev FaceCoordinates (p q r : ℕ) :=
  {x : RawFaceCoordinates p q r //
    x.1.isSome ∨ x.2.1.isSome ∨ x.2.2.isSome}

namespace FaceCoordinates

abbrev a (f : FaceCoordinates p q r) := f.1.1
abbrev b (f : FaceCoordinates p q r) := f.1.2.1
abbrev c (f : FaceCoordinates p q r) := f.1.2.2

/-- Finset of actual vertices represented by coordinate face data. -/
def vertices (f : FaceCoordinates p q r) : Finset Vertex :=
  (match f.a with | none => ∅ | some x => {Sum.inl x}) ∪
  (match f.b with | none => ∅ | some y => {Sum.inr (Sum.inl y)}) ∪
  (match f.c with | none => ∅ | some z => {Sum.inr (Sum.inr z)})

lemma mem_vertices_A (f : FaceCoordinates p q r) (x : Fin (p+1)) :
    (Sum.inl x : Vertex) ∈ vertices f ↔ f.a = some x := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc <;>
    simp [vertices, FaceCoordinates.a, eq_comm]

lemma mem_vertices_B (f : FaceCoordinates p q r) (y : Fin (q+1)) :
    (Sum.inr (Sum.inl y) : Vertex) ∈ vertices f ↔ f.b = some y := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc <;>
    simp [vertices, FaceCoordinates.b, eq_comm]

lemma mem_vertices_C (f : FaceCoordinates p q r) (z : Fin (r+1)) :
    (Sum.inr (Sum.inr z) : Vertex) ∈ vertices f ↔ f.c = some z := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc <;>
    simp [vertices, FaceCoordinates.c, eq_comm]

lemma vertices_nonempty (f : FaceCoordinates p q r) : (vertices f).Nonempty := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  rcases hf with ha | hb | hc
  · rw [Option.isSome_iff_exists] at ha
    rcases ha with ⟨x,hx⟩
    exact ⟨Sum.inl x, (mem_vertices_A _ _).2 hx⟩
  · rw [Option.isSome_iff_exists] at hb
    rcases hb with ⟨y,hy⟩
    exact ⟨Sum.inr (Sum.inl y), (mem_vertices_B _ _).2 hy⟩
  · rw [Option.isSome_iff_exists] at hc
    rcases hc with ⟨z,hz⟩
    exact ⟨Sum.inr (Sum.inr z), (mem_vertices_C _ _).2 hz⟩

lemma vertices_pairwise (f : FaceCoordinates p q r) :
    ((vertices f : Finset Vertex) : Set Vertex).Pairwise CrossZone := by
  intro x hx y hy hxy
  rcases x with xa | xbc
  · rcases y with ya | ybc
    · have hxa := (mem_vertices_A f xa).1 hx
      have hya := (mem_vertices_A f ya).1 hy
      rw [hxa] at hya
      injection hya with hxy'
      exact (hxy (congrArg Sum.inl hxy')).elim
    · rcases ybc with yb | yc <;> simp [CrossZone, zone]
  · rcases xbc with xb | xc
    · rcases y with ya | ybc
      · simp [CrossZone, zone]
      · rcases ybc with yb | yc
        · have hxb := (mem_vertices_B f xb).1 hx
          have hyb := (mem_vertices_B f yb).1 hy
          rw [hxb] at hyb
          injection hyb with hxy'
          exact (hxy (congrArg (fun z => Sum.inr (Sum.inl z)) hxy')).elim
        · simp [CrossZone, zone]
    · rcases y with ya | ybc
      · simp [CrossZone, zone]
      · rcases ybc with yb | yc
        · simp [CrossZone, zone]
        · have hxc := (mem_vertices_C f xc).1 hx
          have hyc := (mem_vertices_C f yc).1 hy
          rw [hxc] at hyc
          injection hyc with hxy'
          exact (hxy (congrArg (fun z => Sum.inr (Sum.inr z)) hxy')).elim

lemma vertices_mem (f : FaceCoordinates p q r) :
    vertices f ∈ abstractComplex (p:=p) (q:=q) (r:=r) :=
  ⟨vertices_nonempty f, vertices_pairwise f⟩

/-- Recover the optional first-zone coordinate of any vertex finset. -/
noncomputable def readA (s : Finset Vertex) : Option (Fin (p+1)) :=
  if h : ∃ x, (Sum.inl x : Vertex) ∈ s then some h.choose else none

noncomputable def readB (s : Finset Vertex) : Option (Fin (q+1)) :=
  if h : ∃ y, (Sum.inr (Sum.inl y) : Vertex) ∈ s then some h.choose else none

noncomputable def readC (s : Finset Vertex) : Option (Fin (r+1)) :=
  if h : ∃ z, (Sum.inr (Sum.inr z) : Vertex) ∈ s then some h.choose else none

lemma same_zone_eq {s : Finset Vertex}
    (hs : (s : Set Vertex).Pairwise CrossZone)
    {x y : Vertex} (hx : x ∈ s) (hy : y ∈ s)
    (hzone : zone x = zone y) : x = y := by
  by_contra hxy
  exact (hs hx hy hxy) hzone

lemma readA_eq_some_iff {s : Finset Vertex}
    (hs : (s : Set Vertex).Pairwise CrossZone) (x : Fin (p+1)) :
    readA (p:=p) (q:=q) (r:=r) s = some x ↔
      (Sum.inl x : Vertex) ∈ s := by
  classical
  unfold readA
  split_ifs with h
  · constructor
    · intro heq
      have hx : h.choose = x := Option.some.inj heq
      simpa [hx] using h.choose_spec
    · intro hx
      have hv : (Sum.inl h.choose : Vertex) = Sum.inl x :=
        same_zone_eq hs h.choose_spec hx rfl
      have heq : h.choose = x := Sum.inl_injective hv
      simp [heq]
  · constructor
    · simp
    · intro hx
      exact (h ⟨x,hx⟩).elim

lemma readB_eq_some_iff {s : Finset Vertex}
    (hs : (s : Set Vertex).Pairwise CrossZone) (y : Fin (q+1)) :
    readB (p:=p) (q:=q) (r:=r) s = some y ↔
      (Sum.inr (Sum.inl y) : Vertex) ∈ s := by
  classical
  unfold readB
  split_ifs with h
  · constructor
    · intro heq
      have hy : h.choose = y := Option.some.inj heq
      simpa [hy] using h.choose_spec
    · intro hy
      have hv : (Sum.inr (Sum.inl h.choose) : Vertex) =
          Sum.inr (Sum.inl y) := same_zone_eq hs h.choose_spec hy rfl
      have heq : h.choose = y := Sum.inl_injective (Sum.inr_injective hv)
      simp [heq]
  · constructor
    · simp
    · intro hy
      exact (h ⟨y,hy⟩).elim

lemma readC_eq_some_iff {s : Finset Vertex}
    (hs : (s : Set Vertex).Pairwise CrossZone) (z : Fin (r+1)) :
    readC (p:=p) (q:=q) (r:=r) s = some z ↔
      (Sum.inr (Sum.inr z) : Vertex) ∈ s := by
  classical
  unfold readC
  split_ifs with h
  · constructor
    · intro heq
      have hz : h.choose = z := Option.some.inj heq
      simpa [hz] using h.choose_spec
    · intro hz
      have hv : (Sum.inr (Sum.inr h.choose) : Vertex) =
          Sum.inr (Sum.inr z) := same_zone_eq hs h.choose_spec hz rfl
      have heq : h.choose = z := Sum.inr_injective (Sum.inr_injective hv)
      simp [heq]
  · constructor
    · simp
    · intro hz
      exact (h ⟨z,hz⟩).elim

lemma readA_vertices (f : FaceCoordinates p q r) : readA (vertices f) = f.a := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc <;>
    simp_all [readA, vertices, FaceCoordinates.a]

lemma readB_vertices (f : FaceCoordinates p q r) : readB (vertices f) = f.b := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc <;>
    simp_all [readB, vertices, FaceCoordinates.b]

lemma readC_vertices (f : FaceCoordinates p q r) : readC (vertices f) = f.c := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc <;>
    simp_all [readC, vertices, FaceCoordinates.c]

lemma vertices_injective : Function.Injective
    (vertices : FaceCoordinates p q r → Finset Vertex) := by
  intro f g h
  apply Subtype.ext
  apply Prod.ext
  · calc
      f.1.1 = readA (vertices f) := (readA_vertices f).symm
      _ = readA (vertices g) := by rw [h]
      _ = g.1.1 := readA_vertices g
  · apply Prod.ext
    · calc
        f.1.2.1 = readB (vertices f) := (readB_vertices f).symm
        _ = readB (vertices g) := by rw [h]
        _ = g.1.2.1 := readB_vertices g
    · calc
        f.1.2.2 = readC (vertices f) := (readC_vertices f).symm
        _ = readC (vertices g) := by rw [h]
        _ = g.1.2.2 := readC_vertices g

noncomputable def ofFinset (s : Finset Vertex)
    (hs : s ∈ abstractComplex (p:=p) (q:=q) (r:=r)) : FaceCoordinates p q r := by
  let oa := readA (p:=p) (q:=q) (r:=r) s
  let ob := readB (p:=p) (q:=q) (r:=r) s
  let oc := readC (p:=p) (q:=q) (r:=r) s
  refine ⟨(oa,(ob,oc)), ?_⟩
  rcases hs.1 with ⟨v,hv⟩
  rcases v with x | yz
  · left
    rw [Option.isSome_iff_exists]
    exact ⟨x, (readA_eq_some_iff hs.2 x).2 hv⟩
  · rcases yz with y | z
    · right; left
      rw [Option.isSome_iff_exists]
      exact ⟨y, (readB_eq_some_iff hs.2 y).2 hv⟩
    · right; right
      rw [Option.isSome_iff_exists]
      exact ⟨z, (readC_eq_some_iff hs.2 z).2 hv⟩

lemma vertices_ofFinset (s : Finset Vertex)
    (hs : s ∈ abstractComplex (p:=p) (q:=q) (r:=r)) :
    vertices (ofFinset s hs) = s := by
  classical
  ext v
  rcases v with x | yz
  · rw [mem_vertices_A]
    change readA s = some x ↔ _
    exact readA_eq_some_iff hs.2 x
  · rcases yz with y | z
    · rw [mem_vertices_B]
      change readB s = some y ↔ _
      exact readB_eq_some_iff hs.2 y
    · rw [mem_vertices_C]
      change readC s = some z ↔ _
      exact readC_eq_some_iff hs.2 z

/-- The coordinate face type is equivalent to the actual face subtype of the
Mathlib abstract simplicial complex. -/
noncomputable def equivAbstractFaces :
    FaceCoordinates p q r ≃ {s : Finset Vertex //
      s ∈ abstractComplex (p:=p) (q:=q) (r:=r)} where
  toFun f := ⟨vertices f, vertices_mem f⟩
  invFun s := ofFinset s.1 s.2
  left_inv f := vertices_injective (vertices_ofFinset (vertices f) (vertices_mem f))
  right_inv s := Subtype.ext (vertices_ofFinset s.1 s.2)

end FaceCoordinates
end D0.Topology.GenericTripartiteAbstractComplex

namespace D0.Topology.GenericTripartiteAbstractComplex

open D0.Topology.GenericTripartiteHomology

variable {p q r : ℕ}

/-- Typed cell presentation by dimension. -/
inductive Face (p q r : ℕ)
  | vertex : GenericVertex p q r → Face p q r
  | edge : GenericEdge p q r → Face p q r
  | triangle : GenericTriangle p q r → Face p q r
  deriving DecidableEq, Fintype

namespace Face

/-- Convert a typed cell to its optional-zone coordinate face. -/
def toCoordinates : Face p q r → FaceCoordinates p q r
  | .vertex (Sum.inl x) => ⟨(some x,(none,none)), by simp⟩
  | .vertex (Sum.inr (Sum.inl y)) => ⟨(none,(some y,none)), by simp⟩
  | .vertex (Sum.inr (Sum.inr z)) => ⟨(none,(none,some z)), by simp⟩
  | .edge (Sum.inl (x,y)) => ⟨(some x,(some y,none)), by simp⟩
  | .edge (Sum.inr (Sum.inl (x,z))) => ⟨(some x,(none,some z)), by simp⟩
  | .edge (Sum.inr (Sum.inr (y,z))) => ⟨(none,(some y,some z)), by simp⟩
  | .triangle (x,y,z) => ⟨(some x,(some y,some z)), by simp⟩

end Face

namespace FaceCoordinates

/-- Recover the typed face constructor from optional-zone coordinates. -/
def toFace (f : FaceCoordinates p q r) : Face p q r := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa with
  | none =>
      cases ob with
      | none =>
          cases oc with
          | none => simp at hf
          | some z => exact .vertex (Sum.inr (Sum.inr z))
      | some y =>
          cases oc with
          | none => exact .vertex (Sum.inr (Sum.inl y))
          | some z => exact .edge (Sum.inr (Sum.inr (y,z)))
  | some x =>
      cases ob with
      | none =>
          cases oc with
          | none => exact .vertex (Sum.inl x)
          | some z => exact .edge (Sum.inr (Sum.inl (x,z)))
      | some y =>
          cases oc with
          | none => exact .edge (Sum.inl (x,y))
          | some z => exact .triangle (x,y,z)

lemma toFace_toCoordinates (f : FaceCoordinates p q r) : f.toFace.toCoordinates = f := by
  rcases f with ⟨⟨oa,ob,oc⟩,hf⟩
  cases oa <;> cases ob <;> cases oc
  · simp at hf
  all_goals simp_all [toFace, Face.toCoordinates]

end FaceCoordinates

lemma Face.toCoordinates_toFace (f : Face p q r) : f.toCoordinates.toFace = f := by
  rcases f with v | e | t
  · rcases v with x | yz
    · simp [Face.toCoordinates, FaceCoordinates.toFace]
    · rcases yz with y | z <;> simp [Face.toCoordinates, FaceCoordinates.toFace]
  · rcases e with xy | rest
    · rcases xy with ⟨x,y⟩
      simp [Face.toCoordinates, FaceCoordinates.toFace]
    · rcases rest with xz | yz
      · rcases xz with ⟨x,z⟩
        simp [Face.toCoordinates, FaceCoordinates.toFace]
      · rcases yz with ⟨y,z⟩
        simp [Face.toCoordinates, FaceCoordinates.toFace]
  · rcases t with ⟨x,y,z⟩
    simp [Face.toCoordinates, FaceCoordinates.toFace]

namespace Face

/-- Actual vertex finset of a typed face. -/
def vertices (f : Face p q r) : Finset (GenericVertex p q r) :=
  f.toCoordinates.vertices

lemma vertices_mem (f : Face p q r) :
    f.vertices ∈ abstractComplex (p:=p) (q:=q) (r:=r) :=
  FaceCoordinates.vertices_mem f.toCoordinates

lemma vertices_injective : Function.Injective
    (vertices : Face p q r → Finset (GenericVertex p q r)) := by
  intro f g h
  have hcoord : f.toCoordinates = g.toCoordinates :=
    FaceCoordinates.vertices_injective h
  calc
    f = f.toCoordinates.toFace := (Face.toCoordinates_toFace f).symm
    _ = g.toCoordinates.toFace := by rw [hcoord]
    _ = g := Face.toCoordinates_toFace g

end Face

/-- The typed face carrier is exactly the disjoint union of vertices, edges,
and triangles. -/
def faceEquivSum :
    Face p q r ≃
      GenericVertex p q r ⊕
        (GenericEdge p q r ⊕ GenericTriangle p q r) where
  toFun
    | .vertex v => Sum.inl v
    | .edge e => Sum.inr (Sum.inl e)
    | .triangle t => Sum.inr (Sum.inr t)
  invFun
    | Sum.inl v => .vertex v
    | Sum.inr (Sum.inl e) => .edge e
    | Sum.inr (Sum.inr t) => .triangle t
  left_inv f := by cases f <;> rfl
  right_inv x := by
    rcases x with v | rest
    · rfl
    · rcases rest with e | t <;> rfl

/-- Total number of nonempty faces in the canonical abstract complex. -/
theorem face_card_formula :
    Fintype.card (Face p q r) =
      (p + q + r + 3) +
        ((p + 1) * (q + 1) +
          (p + 1) * (r + 1) +
          (q + 1) * (r + 1)) +
        (p + 1) * (q + 1) * (r + 1) := by
  rw [Fintype.card_congr (faceEquivSum (p:=p) (q:=q) (r:=r))]
  simp [GenericVertex, GenericEdge, GenericTriangle,
    D0.SelfReading.TypedIncidenceCarriers.TripartiteEdge,
    D0.SelfReading.TypedIncidenceCarriers.TripartiteTriangle]
  ring

/-- The total face count splits into the critical-cell count
`1 + p*q*r` plus two copies of the graph-edge carrier. -/
theorem face_card_morse_balance :
    Fintype.card (Face p q r) =
      1 + p * q * r +
        2 * Fintype.card (GenericEdge p q r) := by
  rw [Fintype.card_congr (faceEquivSum (p:=p) (q:=q) (r:=r))]
  simp [GenericVertex, GenericEdge, GenericTriangle,
    D0.SelfReading.TypedIncidenceCarriers.TripartiteEdge,
    D0.SelfReading.TypedIncidenceCarriers.TripartiteTriangle]
  ring

/-- Source-scene face count: `33 + 359 + 1287 = 1679`. -/
theorem scene_face_card :
    Fintype.card (Face 8 10 12) = 1679 := by
  simpa using face_card_formula (p:=8) (q:=10) (r:=12)

/-- Typed cells are equivalent to optional-zone coordinate faces. -/
def faceEquivCoordinates : Face p q r ≃ FaceCoordinates p q r where
  toFun := Face.toCoordinates
  invFun := FaceCoordinates.toFace
  left_inv := Face.toCoordinates_toFace
  right_inv := FaceCoordinates.toFace_toCoordinates

/-- Exact equivalence between typed cells and the actual face subtype of the
Mathlib abstract simplicial complex. -/
noncomputable def faceEquivAbstractFaces :
    Face p q r ≃ {s : Finset (GenericVertex p q r) //
      s ∈ abstractComplex (p:=p) (q:=q) (r:=r)} :=
  faceEquivCoordinates.trans FaceCoordinates.equivAbstractFaces

end D0.Topology.GenericTripartiteAbstractComplex
