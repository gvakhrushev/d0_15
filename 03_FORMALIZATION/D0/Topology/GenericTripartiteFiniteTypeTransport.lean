import D0.Topology.GenericTripartiteUniversalHomology
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-FINITE-TYPE-TRANSPORT-001

This module proves the carrier transport that was deliberately left open by
the canonical `Fin` theorem.  For arbitrary finite types `A,B,C`, the natural
typed boundary matrices are explicitly reindexed canonical matrices.  Hence,
for nonempty zones and every commutative coefficient ring `R`,

```
ker ∂₂(A,B,C;R) ≃ₗ[R]
  ((Fin (|A|-1) × Fin (|B|-1) × Fin (|C|-1)) → R).
```

This is an actual conjugation of chain carriers along finite equivalences, not
an appeal to informal invariance.
-/

namespace D0.Topology.GenericTripartiteFiniteTypeTransport
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFirstHomologyRing

variable (R : Type) [CommRing R]
variable {A B C : Type} [Fintype A] [Fintype B] [Fintype C]
  [DecidableEq A] [DecidableEq B] [DecidableEq C]
variable {p q r : ℕ}

abbrev TypeVertex (A B C : Type) := A ⊕ (B ⊕ C)
abbrev TypeEdge (A B C : Type) := TripartiteEdge A B C
abbrev TypeTriangle (A B C : Type) := TripartiteTriangle A B C

def typeBoundary1 : Matrix (TypeVertex A B C) (TypeEdge A B C) R
  | Sum.inl a, Sum.inl (a', _) => if a = a' then -1 else 0
  | Sum.inl a, Sum.inr (Sum.inl (a', _)) => if a = a' then -1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl b), Sum.inl (_, b') => if b = b' then 1 else 0
  | Sum.inr (Sum.inl _), Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inl b), Sum.inr (Sum.inr (b', _)) =>
      if b = b' then -1 else 0
  | Sum.inr (Sum.inr _), Sum.inl _ => 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inl (_, c')) =>
      if c = c' then 1 else 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inr (_, c')) =>
      if c = c' then 1 else 0

def typeBoundary2 : Matrix (TypeEdge A B C) (TypeTriangle A B C) R
  | Sum.inl (a,b), (a',b',_) => if a=a' ∧ b=b' then 1 else 0
  | Sum.inr (Sum.inl (a,c)), (a',_,c') => if a=a' ∧ c=c' then -1 else 0
  | Sum.inr (Sum.inr (b,c)), (_,b',c') => if b=b' ∧ c=c' then 1 else 0

noncomputable def typeVertexEquivCanonical
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    TypeVertex A B C ≃ GenericVertex p q r :=
  Equiv.sumCongr eA (Equiv.sumCongr eB eC)

noncomputable def typeEdgeEquivCanonical
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    TypeEdge A B C ≃ GenericEdge p q r :=
  Equiv.sumCongr (Equiv.prodCongr eA eB)
    (Equiv.sumCongr (Equiv.prodCongr eA eC) (Equiv.prodCongr eB eC))

noncomputable def typeTriangleEquivCanonical
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    TypeTriangle A B C ≃ GenericTriangle p q r :=
  Equiv.prodCongr eA (Equiv.prodCongr eB eC)

lemma typeBoundary1_eq_reindex
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    typeBoundary1 R (A:=A) (B:=B) (C:=C) =
      Matrix.reindex
        (typeVertexEquivCanonical eA eB eC).symm
        (typeEdgeEquivCanonical eA eB eC).symm
        (boundary1R R (p:=p) (q:=q) (r:=r)) := by
  ext v e
  rcases v with a | v
  · rcases e with ab | rest
    · rcases ab with ⟨a',b⟩
      simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
        boundary1R]
    · rcases rest with ac | bc
      · rcases ac with ⟨a',c⟩
        simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
          boundary1R]
      · rcases bc with ⟨b,c⟩
        simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
          boundary1R]
  · rcases v with b | c
    · rcases e with ab | rest
      · rcases ab with ⟨a,b'⟩
        simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
          boundary1R]
      · rcases rest with ac | bc
        · rcases ac with ⟨a,c⟩
          simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
            boundary1R]
        · rcases bc with ⟨b',c⟩
          simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
            boundary1R]
    · rcases e with ab | rest
      · rcases ab with ⟨a,b⟩
        simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
          boundary1R]
      · rcases rest with ac | bc
        · rcases ac with ⟨a,c'⟩
          simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
            boundary1R]
        · rcases bc with ⟨b,c'⟩
          simp [typeBoundary1, typeVertexEquivCanonical, typeEdgeEquivCanonical,
            boundary1R]

lemma typeBoundary2_eq_reindex
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    typeBoundary2 R (A:=A) (B:=B) (C:=C) =
      Matrix.reindex
        (typeEdgeEquivCanonical eA eB eC).symm
        (typeTriangleEquivCanonical eA eB eC).symm
        (boundary2R R (p:=p) (q:=q) (r:=r)) := by
  ext e t
  rcases t with ⟨a,b,c⟩
  rcases e with ab | rest
  · rcases ab with ⟨a',b'⟩
    simp [typeBoundary2, typeEdgeEquivCanonical, typeTriangleEquivCanonical,
      boundary2R]
  · rcases rest with ac | bc
    · rcases ac with ⟨a',c'⟩
      simp [typeBoundary2, typeEdgeEquivCanonical, typeTriangleEquivCanonical,
        boundary2R]
    · rcases bc with ⟨b',c'⟩
      simp [typeBoundary2, typeEdgeEquivCanonical, typeTriangleEquivCanonical,
        boundary2R]

noncomputable def triangleFunctionsEquivCanonical
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    (TypeTriangle A B C → R) ≃ₗ[R] (GenericTriangle p q r → R) :=
  LinearEquiv.funCongrLeft R R (typeTriangleEquivCanonical eA eB eC).symm

noncomputable def edgeFunctionsFromCanonical
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    (GenericEdge p q r → R) ≃ₗ[R] (TypeEdge A B C → R) :=
  LinearEquiv.funCongrLeft R R (typeEdgeEquivCanonical eA eB eC)

lemma typeBoundary2_mulVec_transport
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1))
    (x : TypeTriangle A B C → R) :
    (typeBoundary2 R (A:=A) (B:=B) (C:=C)).mulVec x =
      edgeFunctionsFromCanonical R eA eB eC
        ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
          (triangleFunctionsEquivCanonical R eA eB eC x)) := by
  rw [typeBoundary2_eq_reindex R eA eB eC]
  change
    (Matrix.reindex
      (typeEdgeEquivCanonical eA eB eC).symm
      (typeTriangleEquivCanonical eA eB eC).symm
      (boundary2R R (p:=p) (q:=q) (r:=r))).mulVecLin x = _
  rw [Matrix.mulVecLin_reindex]
  rfl

noncomputable def topKernelEquivCanonical
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    LinearMap.ker (typeBoundary2 R (A:=A) (B:=B) (C:=C)).mulVecLin ≃ₗ[R]
      TopKernel R (p:=p) (q:=q) (r:=r) where
  toFun z := ⟨triangleFunctionsEquivCanonical R eA eB eC z, by
    rw [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    apply (edgeFunctionsFromCanonical R eA eB eC).injective
    rw [map_zero]
    rw [← typeBoundary2_mulVec_transport R eA eB eC]
    exact z.property⟩
  invFun z := ⟨(triangleFunctionsEquivCanonical R eA eB eC).symm z, by
    rw [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    rw [typeBoundary2_mulVec_transport R eA eB eC]
    simp only [LinearEquiv.apply_symm_apply]
    have hz :
        (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
          (z : GenericTriangle p q r → R) = 0 := by
      have hz' := z.property
      rw [LinearMap.mem_ker, Matrix.mulVecLin_apply] at hz'
      exact hz'
    rw [hz, map_zero]⟩
  left_inv z := by
    apply Subtype.ext
    exact (triangleFunctionsEquivCanonical R eA eB eC).symm_apply_apply z
  right_inv z := by
    apply Subtype.ext
    exact (triangleFunctionsEquivCanonical R eA eB eC).apply_symm_apply z
  map_add' x y := by
    apply Subtype.ext
    exact map_add _ _ _
  map_smul' c x := by
    apply Subtype.ext
    exact map_smul _ _ _

noncomputable def typeTopCoordinateEquiv
    (eA : A ≃ Fin (p+1)) (eB : B ≃ Fin (q+1)) (eC : C ≃ Fin (r+1)) :
    LinearMap.ker (typeBoundary2 R (A:=A) (B:=B) (C:=C)).mulVecLin ≃ₗ[R]
      (TopCycleIndex p q r → R) :=
  (topKernelEquivCanonical R eA eB eC).trans (topCoordinateEquivR R)

/-- Canonical enumeration of a nonempty finite type with offset
`Fintype.card A - 1`. -/
noncomputable def typeEquivFinSucc
    (A : Type) [Fintype A] (hA : 0 < Fintype.card A) :
    A ≃ Fin ((Fintype.card A - 1) + 1) :=
  Fintype.equivFinOfCardEq (by omega)

/-- **Automatic finite-type top-homology coordinates.**  The only hypotheses
are nonemptiness of the three finite zones. -/
noncomputable def finiteTypeTopCoordinateEquiv
    (hA : 0 < Fintype.card A)
    (hB : 0 < Fintype.card B)
    (hC : 0 < Fintype.card C) :
    LinearMap.ker (typeBoundary2 R (A:=A) (B:=B) (C:=C)).mulVecLin ≃ₗ[R]
      (TopCycleIndex
        (Fintype.card A - 1)
        (Fintype.card B - 1)
        (Fintype.card C - 1) → R) :=
  typeTopCoordinateEquiv R
    (typeEquivFinSucc A hA)
    (typeEquivFinSucc B hB)
    (typeEquivFinSucc C hC)

/-- Rational top Betti number of the natural typed boundary complex. -/
noncomputable def finiteTypeTopBetti : ℕ :=
  Module.finrank ℚ
    (LinearMap.ker
      (typeBoundary2 ℚ (A:=A) (B:=B) (C:=C)).mulVecLin)

/-- The top Betti number of arbitrary nonempty finite zones is the product of
their reduced cardinalities. -/
theorem finiteTypeTopBetti_formula
    (hA : 0 < Fintype.card A)
    (hB : 0 < Fintype.card B)
    (hC : 0 < Fintype.card C) :
    finiteTypeTopBetti (A:=A) (B:=B) (C:=C) =
      (Fintype.card A - 1) *
        (Fintype.card B - 1) *
        (Fintype.card C - 1) := by
  unfold finiteTypeTopBetti
  calc
    Module.finrank ℚ
        (LinearMap.ker
          (typeBoundary2 ℚ (A:=A) (B:=B) (C:=C)).mulVecLin) =
        Module.finrank ℚ
          (TopCycleIndex
            (Fintype.card A - 1)
            (Fintype.card B - 1)
            (Fintype.card C - 1) → ℚ) :=
      (finiteTypeTopCoordinateEquiv ℚ hA hB hC).finrank_eq
    _ =
        (Fintype.card A - 1) *
          (Fintype.card B - 1) *
          (Fintype.card C - 1) := by
      rw [Module.finrank_fintype_fun_eq_card]
      simp [TopCycleIndex, Nat.mul_assoc]

end D0.Topology.GenericTripartiteFiniteTypeTransport
