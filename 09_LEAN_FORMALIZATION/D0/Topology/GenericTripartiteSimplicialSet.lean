import D0.Topology.GenericTripartiteMorseComplex
import Mathlib.AlgebraicTopology.SimplicialSet.NerveNondegenerate
import Mathlib.AlgebraicTopology.SimplicialSet.NonDegenerateSimplices
import Mathlib.AlgebraicTopology.SimplicialSet.TopAdj
import Mathlib.Data.Finset.Sort
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-SIMPLICIAL-SET-001

This module supplies the first literal spatial bridge for the canonical
complete-tripartite abstract simplicial complex.

The vertices are placed in a canonical zone-lexicographic linear order.  The
nerve of that finite order contains a subcomplex whose simplices are exactly
the monotone vertex strings whose image is a face of `abstractComplex`.
Consequently Mathlib's existing geometric-realization functor applies to an
actual simplicial set representing the D0 complex.

The key theorem is not merely a count: nondegenerate simplices of this
simplicial set are canonically equivalent to the typed face carrier
`vertex | edge | triangle`.  Thus the already proved discrete Morse matching
now has an exact carrier inside Mathlib's `SSet` API.

This does **not** yet prove a Forman collapse or the final homotopy equivalence
to a wedge of two-spheres.  The remaining missing bridge is to turn the
face matching into a suitable simplicial-set pairing/collapse theorem and then
transport it through geometric realization.
-/

namespace D0.Topology.GenericTripartiteSimplicialSet
open CategoryTheory Simplicial Opposite
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteAbstractComplex

variable {p q r : ℕ}


lemma image_symm_image {α β : Type*} [DecidableEq α] [DecidableEq β]
    (e : α ≃ β) (s : Finset α) :
    (s.image e).image e.symm = s := by
  ext x
  simp

abbrev OrderedVertex (p q r : ℕ) :=
  Fin (p + 1) ⊕ₗ (Fin (q + 1) ⊕ₗ Fin (r + 1))

noncomputable def vertexOrderEquiv (p q r : ℕ) :
    GenericVertex p q r ≃ OrderedVertex p q r :=
  (Equiv.sumCongr (Equiv.refl _) (toLex :
    (Fin (q + 1) ⊕ Fin (r + 1)) ≃ (Fin (q + 1) ⊕ₗ Fin (r + 1)))).trans
      (toLex :
        (Fin (p + 1) ⊕ (Fin (q + 1) ⊕ₗ Fin (r + 1))) ≃ OrderedVertex p q r)

noncomputable def faceNerve : SSet := CategoryTheory.nerve (OrderedVertex p q r)

noncomputable def simplexVertexFinset {n : ℕ}
    (x : (faceNerve (p:=p) (q:=q) (r:=r)) _⦋n⦌) :
    Finset (GenericVertex p q r) :=
  Finset.image (fun i => (vertexOrderEquiv p q r).symm (x.obj i)) Finset.univ

noncomputable def simplicialSet : (faceNerve (p:=p) (q:=q) (r:=r)).Subcomplex where
  obj n := {x | simplexVertexFinset x ∈ abstractComplex (p:=p) (q:=q) (r:=r)}
  map {U V} f x hx := by
    change simplexVertexFinset ((faceNerve (p:=p) (q:=q) (r:=r)).map f x) ∈
      abstractComplex (p:=p) (q:=q) (r:=r)
    refine ((abstractComplex (p:=p) (q:=q) (r:=r)).isRelLowerSet_faces hx).2 ?_ ?_
    · intro y hy
      simp only [simplexVertexFinset, Finset.mem_image, Finset.mem_univ, true_and] at hy ⊢
      rcases hy with ⟨i, rfl⟩
      refine ⟨f.unop i, ?_⟩
      rfl
    · exact Finset.image_nonempty.mpr Finset.univ_nonempty

/-- The geometric realization of the canonical tripartite simplicial set.
This object exists in Mathlib independently of the still-open Forman-collapse
theorem. -/
noncomputable abbrev realization (p q r : ℕ) : TopCat :=
  SSet.toTop.obj (simplicialSet (p:=p) (q:=q) (r:=r) : SSet)

lemma face_vertices_card (f : Face p q r) :
    f.vertices.card =
      D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension f + 1 := by
  rcases f with v | e | t
  · rcases v with a | bc
    · simp [Face.vertices, Face.toCoordinates, FaceCoordinates.vertices,
        D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension]
    · rcases bc with b | c <;>
        simp [Face.vertices, Face.toCoordinates, FaceCoordinates.vertices,
          D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension]
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp [Face.vertices, Face.toCoordinates, FaceCoordinates.vertices,
        D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp [Face.vertices, Face.toCoordinates, FaceCoordinates.vertices,
          D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension]
      · rcases bc with ⟨b,c⟩
        simp [Face.vertices, Face.toCoordinates, FaceCoordinates.vertices,
          D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension]
  · rcases t with ⟨a,b,c⟩
    simp [Face.vertices, Face.toCoordinates, FaceCoordinates.vertices,
      D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension]

noncomputable def orderedFaceVertices (f : Face p q r) : Finset (OrderedVertex p q r) :=
  f.vertices.image (vertexOrderEquiv p q r)

lemma orderedFaceVertices_card (f : Face p q r) :
    (orderedFaceVertices f).card =
      D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension f + 1 := by
  rw [orderedFaceVertices, Finset.card_image_of_injective _ (vertexOrderEquiv p q r).injective]
  exact face_vertices_card f

noncomputable def faceToNondegenerate (f : Face p q r) :
    (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N := by
  let s := orderedFaceVertices f
  let e : Fin (D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension f + 1) ↪o
      OrderedVertex p q r := Finset.orderEmbOfFin s (orderedFaceVertices_card f)
  let x : (faceNerve (p:=p) (q:=q) (r:=r))
      _⦋D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension f⦌ :=
    e.monotone.functor
  let hx : x ∈ (simplicialSet (p:=p) (q:=q) (r:=r)).obj _ := by
    change simplexVertexFinset x ∈ abstractComplex (p:=p) (q:=q) (r:=r)
    have hordered : Finset.image x.obj Finset.univ = s := by
      change Finset.image e Finset.univ = s
      exact Finset.image_orderEmbOfFin_univ s (orderedFaceVertices_card f)
    have horiginal : simplexVertexFinset x = Face.vertices f := by
      unfold simplexVertexFinset
      calc
        Finset.image (fun i => (vertexOrderEquiv p q r).symm (x.obj i)) Finset.univ =
            Finset.image (vertexOrderEquiv p q r).symm
              (Finset.image x.obj Finset.univ) := by
                simp [Finset.image_image, Function.comp_def]
        _ = Finset.image (vertexOrderEquiv p q r).symm s := by rw [hordered]
        _ = Face.vertices f := by
          unfold s orderedFaceVertices
          exact image_symm_image (vertexOrderEquiv p q r) (Face.vertices f)
    rw [horiginal]
    exact Face.vertices_mem f
  let xs : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet)
      _⦋D0.Topology.GenericTripartiteDiscreteMorse.Face.dimension f⦌ := ⟨x, hx⟩
  refine SSet.N.mk xs ?_
  apply (SSet.Subcomplex.mem_nonDegenerate_iff
    (simplicialSet (p:=p) (q:=q) (r:=r)) xs).2
  exact (PartialOrder.mem_nerve_nonDegenerate_iff_strictMono x).2 e.strictMono

end D0.Topology.GenericTripartiteSimplicialSet


namespace D0.Topology.GenericTripartiteSimplicialSet
open CategoryTheory Simplicial Opposite
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteDiscreteMorse

variable {p q r : ℕ}

@[simp] lemma faceToNondegenerate_dim (f : Face p q r) :
    (faceToNondegenerate f).dim = Face.dimension f := by
  rfl

lemma simplexVertexFinset_faceToNondegenerate (f : Face p q r) :
    simplexVertexFinset (faceToNondegenerate f).simplex.val = Face.vertices f := by
  unfold faceToNondegenerate
  dsimp
  let s := orderedFaceVertices f
  let e : Fin (Face.dimension f + 1) ↪o OrderedVertex p q r :=
    Finset.orderEmbOfFin s (orderedFaceVertices_card f)
  have hordered : Finset.image e Finset.univ = s :=
    Finset.image_orderEmbOfFin_univ s (orderedFaceVertices_card f)
  unfold simplexVertexFinset
  calc
    Finset.image (fun i => (vertexOrderEquiv p q r).symm (e i)) Finset.univ =
        Finset.image (vertexOrderEquiv p q r).symm
          (Finset.image e Finset.univ) := by
            simp [Finset.image_image, Function.comp_def]
    _ = Finset.image (vertexOrderEquiv p q r).symm s := by rw [hordered]
    _ = Face.vertices f := by
      unfold s orderedFaceVertices
      exact image_symm_image (vertexOrderEquiv p q r) (Face.vertices f)

lemma faceToNondegenerate_injective : Function.Injective
    (faceToNondegenerate : Face p q r →
      (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) := by
  intro f g h
  apply Face.vertices_injective
  rw [← simplexVertexFinset_faceToNondegenerate f,
      ← simplexVertexFinset_faceToNondegenerate g, h]

noncomputable def nondegenerateToFace
    (x : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) : Face p q r :=
  (faceEquivAbstractFaces (p:=p) (q:=q) (r:=r)).symm
    ⟨simplexVertexFinset x.simplex.val, x.simplex.property⟩

lemma nondegenerateToFace_vertices
    (x : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) :
    Face.vertices (nondegenerateToFace x) = simplexVertexFinset x.simplex.val := by
  change ((faceEquivAbstractFaces (p:=p) (q:=q) (r:=r))
      ((faceEquivAbstractFaces (p:=p) (q:=q) (r:=r)).symm
        ⟨simplexVertexFinset x.simplex.val, x.simplex.property⟩)).val = _
  rw [Equiv.apply_symm_apply]

@[simp] lemma nondegenerateToFace_faceToNondegenerate (f : Face p q r) :
    nondegenerateToFace (faceToNondegenerate f) = f := by
  apply Face.vertices_injective
  rw [nondegenerateToFace_vertices, simplexVertexFinset_faceToNondegenerate]

end D0.Topology.GenericTripartiteSimplicialSet


namespace D0.Topology.GenericTripartiteSimplicialSet
open CategoryTheory Simplicial Opposite
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteDiscreteMorse

variable {p q r : ℕ}

lemma nondegenerate_strictMono
    (x : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) :
    StrictMono x.simplex.val.obj := by
  apply (PartialOrder.mem_nerve_nonDegenerate_iff_strictMono x.simplex.val).1
  exact (SSet.Subcomplex.mem_nonDegenerate_iff
    (simplicialSet (p:=p) (q:=q) (r:=r)) x.simplex).1 x.nonDegenerate

lemma orderedSimplexVertexFinset_eq_image
    (x : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) :
    (simplexVertexFinset x.simplex.val).image (vertexOrderEquiv p q r) =
      Finset.image x.simplex.val.obj Finset.univ := by
  unfold simplexVertexFinset
  calc
    Finset.image (vertexOrderEquiv p q r)
        (Finset.image (fun i => (vertexOrderEquiv p q r).symm
          (x.simplex.val.obj i)) Finset.univ) =
      Finset.image ((vertexOrderEquiv p q r) ∘
        fun i => (vertexOrderEquiv p q r).symm
          (x.simplex.val.obj i)) Finset.univ := Finset.image_image
    _ = Finset.image x.simplex.val.obj Finset.univ := by
      simp [Function.comp_def]

lemma simplexVertexFinset_card
    (x : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) :
    (simplexVertexFinset x.simplex.val).card = x.dim + 1 := by
  unfold simplexVertexFinset
  rw [Finset.card_image_of_injective]
  · simp
  · exact (vertexOrderEquiv p q r).symm.injective.comp
      (nondegenerate_strictMono x).injective

lemma nondegenerate_eq_of_simplexVertexFinset_eq
    {x y : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N}
    (h : simplexVertexFinset x.simplex.val =
      simplexVertexFinset y.simplex.val) : x = y := by
  have hxcard := simplexVertexFinset_card x
  have hycard := simplexVertexFinset_card y
  have hcardeq : x.dim + 1 = y.dim + 1 := by rw [← hxcard, h, hycard]
  have hdim : x.dim = y.dim := Nat.add_right_cancel hcardeq
  let y' := y.cast hdim.symm
  have hy' : y' = y := y.cast_eq_self hdim.symm
  have h' : simplexVertexFinset x.simplex.val =
      simplexVertexFinset y'.simplex.val := by
    rw [hy']
    exact h
  suffices hxyeq : x = y' by simpa [hy'] using hxyeq
  apply (SSet.N.ext_iff x y').2
  rw [SSet.S.ext_iff']
  refine ⟨rfl, ?_⟩
  apply Subtype.ext
  apply CategoryTheory.nerve.ext_of_isThin
  funext i
  have hordered :
      Finset.image x.simplex.val.obj Finset.univ =
        Finset.image y'.simplex.val.obj Finset.univ := by
    calc
      Finset.image x.simplex.val.obj Finset.univ =
          (simplexVertexFinset x.simplex.val).image (vertexOrderEquiv p q r) :=
        (orderedSimplexVertexFinset_eq_image x).symm
      _ = (simplexVertexFinset y'.simplex.val).image (vertexOrderEquiv p q r) := by rw [h']
      _ = Finset.image y'.simplex.val.obj Finset.univ :=
        orderedSimplexVertexFinset_eq_image y'
  let s := Finset.image x.simplex.val.obj Finset.univ
  have hcard : s.card = x.dim + 1 := by
    unfold s
    rw [Finset.card_image_of_injective _ (nondegenerate_strictMono x).injective]
    simp
  have hxunique : x.simplex.val.obj = s.orderEmbOfFin hcard :=
    Finset.orderEmbOfFin_unique hcard
      (fun j => Finset.mem_image_of_mem _ (Finset.mem_univ j))
      (nondegenerate_strictMono x)
  have hyunique : y'.simplex.val.obj = s.orderEmbOfFin hcard := by
    apply Finset.orderEmbOfFin_unique hcard
    · intro j
      change y'.simplex.val.obj j ∈
        Finset.image x.simplex.val.obj Finset.univ
      rw [hordered]
      exact Finset.mem_image_of_mem _ (Finset.mem_univ j)
    · exact nondegenerate_strictMono y'
  exact congrFun (hxunique.trans hyunique.symm) i

lemma nondegenerateToFace_injective : Function.Injective
    (nondegenerateToFace :
      (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N → Face p q r) := by
  intro x y h
  apply nondegenerate_eq_of_simplexVertexFinset_eq
  rw [← nondegenerateToFace_vertices x,
      ← nondegenerateToFace_vertices y, h]

lemma nondegenerateToFace_surjective : Function.Surjective
    (nondegenerateToFace :
      (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N → Face p q r) := by
  intro f
  exact ⟨faceToNondegenerate f, nondegenerateToFace_faceToNondegenerate f⟩

noncomputable def nondegenerateFaceEquiv :
    (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N ≃ Face p q r :=
  Equiv.ofBijective nondegenerateToFace
    ⟨nondegenerateToFace_injective, nondegenerateToFace_surjective⟩

noncomputable def faceNondegenerateEquiv :
    Face p q r ≃ (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N :=
  (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).symm

@[simp] theorem faceNondegenerateEquiv_apply (f : Face p q r) :
    faceNondegenerateEquiv f = faceToNondegenerate f := by
  apply nondegenerateToFace_injective
  change (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
      (faceNondegenerateEquiv f) =
    (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
      (faceToNondegenerate f)
  have hleft : (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r))
      (faceNondegenerateEquiv f) = f :=
    (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply f
  exact hleft.trans (nondegenerateToFace_faceToNondegenerate f).symm

@[simp] theorem nondegenerateFaceEquiv_apply
    (x : (simplicialSet (p:=p) (q:=q) (r:=r) : SSet).N) :
    nondegenerateFaceEquiv x = nondegenerateToFace x := rfl

end D0.Topology.GenericTripartiteSimplicialSet
