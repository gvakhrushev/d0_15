import D0.Topology.GenericTripartiteDegeneratePairing
import Mathlib.AlgebraicTopology.SimplicialSet.TopAdj
import Mathlib.Topology.Homotopy.Contractible
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-ROOT-REALIZATION-001

The root subcomplex of the canonical tripartite simplicial set is represented
by the standard zero-simplex.  More precisely,

```
rootSubcomplex ≅ Δ[0].
```

Its geometric realization is therefore homeomorphic to the realization of
`Δ[0]`, has exactly one point, and is contractible.

Combined with `GenericTripartiteDegeneratePairing`, this proves that whenever
`p*q*r = 0` there is a contractible root subcomplex whose inclusion into the
full tripartite simplicial set is strong anodyne (and hence anodyne).

The current Mathlib tree still has no theorem transporting anodyne inclusions
through geometric realization to topological homotopy equivalences.  We
therefore do not assert contractibility of the full realization here.
-/

namespace D0.Topology.GenericTripartiteRootRealization

open CategoryTheory Simplicial Opposite
open D0.Topology.GenericTripartiteSimplicialMorse

variable {p q r : ℕ}

/-- The root critical simplex with definitionally zero dimension. -/
noncomputable def rootZeroSimplex :
    TripartiteSSet p q r _⦋0⦌ :=
  ((rootSimplex (p:=p) (q:=q) (r:=r)).cast
    (rootSimplex_dim (p:=p) (q:=q) (r:=r))).simplex

lemma rootSubcomplex_eq_ofSimplex :
    rootSubcomplex (p:=p) (q:=q) (r:=r) =
      SSet.Subcomplex.ofSimplex
        (rootZeroSimplex (p:=p) (q:=q) (r:=r)) := by
  change (rootSimplex (p:=p) (q:=q) (r:=r)).subcomplex =
    ((rootSimplex (p:=p) (q:=q) (r:=r)).cast
      (rootSimplex_dim (p:=p) (q:=q) (r:=r))).subcomplex
  rw [SSet.N.cast_eq_self]

lemma mem_rootSubcomplex_obj_iff_exists_map
    {n : SimplexCategoryᵒᵖ}
    (y : (TripartiteSSet p q r).obj n) :
    y ∈ (rootSubcomplex (p:=p) (q:=q) (r:=r)).obj n ↔
      ∃ f : n.unop ⟶ ⦋0⦌,
        (TripartiteSSet p q r).map f.op
          (rootZeroSimplex (p:=p) (q:=q) (r:=r)) = y := by
  rw [rootSubcomplex_eq_ofSimplex,
    SSet.Subcomplex.mem_ofSimplex_obj_iff]

/-- Every simplicial degree of the root subcomplex has exactly one section. -/
noncomputable instance rootObjUnique (n : SimplexCategoryᵒᵖ) :
    Unique ((rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet).obj n) where
  default :=
    ⟨(TripartiteSSet p q r).map
        (default : n.unop ⟶ ⦋0⦌).op
        (rootZeroSimplex (p:=p) (q:=q) (r:=r)),
      (mem_rootSubcomplex_obj_iff_exists_map _).2
        ⟨default, rfl⟩⟩
  uniq y := by
    apply Subtype.ext
    obtain ⟨f, hf⟩ :=
      (mem_rootSubcomplex_obj_iff_exists_map y.val).1 y.property
    have hfeq : f = default := Subsingleton.elim _ _
    subst f
    exact hf.symm

/-- The root subcomplex is represented by `[0]`. -/
noncomputable def rootRepresentableBy :
    ((rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet).RepresentableBy
      ⦋0⦌) where
  homEquiv {X} := Equiv.ofUnique (X ⟶ ⦋0⦌)
    ((rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet).obj (op X))
  homEquiv_comp _ _ := Subsingleton.elim _ _

/-- The root subcomplex is the standard zero-simplex. -/
noncomputable def rootStdSimplexIso :
    (Δ[0] : SSet) ≅
      (rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet) :=
  SSet.stdSimplex.isoOfRepresentableBy rootRepresentableBy

/-- Geometric realization of the root subcomplex is homeomorphic to
`|Δ[0]|`. -/
noncomputable def rootRealizationHomeomorph :
    (SSet.toTop.obj
      (rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet) : Type) ≃ₜ
      (SSet.toTop.obj (Δ[0] : SSet) : Type) :=
  TopCat.homeoOfIso (SSet.toTop.mapIso
    (rootStdSimplexIso (p:=p) (q:=q) (r:=r))).symm

/-- The realization of the root subcomplex has exactly one point. -/
noncomputable instance rootRealizationUnique :
    Unique
      (SSet.toTop.obj
        (rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet) : Type) :=
  (rootRealizationHomeomorph (p:=p) (q:=q) (r:=r)).unique

/-- In particular, the root realization is contractible. -/
noncomputable instance rootRealizationContractible :
    ContractibleSpace
      (SSet.toTop.obj
        (rootSubcomplex (p:=p) (q:=q) (r:=r) : SSet) : Type) :=
  inferInstance

/-- In the zero-top-cell cases there is a one-point contractible subcomplex
whose inclusion is strong anodyne. -/
theorem exists_contractible_strongAnodyne_of_topCount_zero
    (hzero : p * q * r = 0) :
    ∃ A : (TripartiteSSet p q r).Subcomplex,
      Nonempty (Unique (SSet.toTop.obj (A : SSet) : Type)) ∧
      ContractibleSpace (SSet.toTop.obj (A : SSet) : Type) ∧
        SSet.strongAnodyneExtensions A.ι := by
  refine ⟨rootSubcomplex, ⟨inferInstance⟩, inferInstance, ?_⟩
  exact
    D0.Topology.GenericTripartiteDegeneratePairing.root_inclusion_strongAnodyne_of_topCount_zero
      hzero

end D0.Topology.GenericTripartiteRootRealization
