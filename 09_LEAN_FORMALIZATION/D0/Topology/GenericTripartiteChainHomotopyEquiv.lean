import D0.Topology.GenericTripartiteChainRetraction
import Mathlib.Algebra.Homology.Homotopy
import Mathlib.Algebra.Category.ModuleCat.Basic
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-CHAIN-HOMOTOPY-EQUIV-001

The explicit deformation-retraction identities for the complete tripartite
clique complex are packaged as a Mathlib `HomotopyEquiv`.

For every commutative ring `R`, the chain complex

```
C₂ --∂₂--> C₁ --∂₁--> C₀
```

is chain-homotopy equivalent to the zero-differential minimal complex

```
R^(Fin p × Fin q × Fin r) in degree 2,
0                         in degree 1,
R                         in degree 0.
```

The projection is augmentation in degree zero and all-nonroot coordinates in
degree two.  The inclusion selects the root vertex and synthesizes the
octahedral top cycles.  The inverse composite on the minimal complex is
strictly the identity; the other composite is joined to the identity by the
explicit `contract0` and `contract1` operators.

This is an algebraic chain-homotopy equivalence.  It does not assert a spatial
homotopy equivalence of geometric realizations.
-/

namespace D0.Topology.GenericTripartiteChainHomotopyEquiv

open CategoryTheory
open HomologicalComplex
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFirstHomologyRing
open D0.Topology.GenericTripartiteZeroHomologyRing
open D0.Topology.GenericTripartiteChainRetraction

variable (R : Type) [CommRing R]
variable {p q r : ℕ}

local notation "Vertex" => GenericVertex p q r
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r

/-- The zero module used outside degrees `0`, `1`, and `2`. -/
abbrev ZeroModule := Fin 0 → R

/-- Objects of the canonical complete-tripartite chain complex. -/
def sourceObject : ℕ → ModuleCat R
  | 0 => ModuleCat.of R (Vertex → R)
  | 1 => ModuleCat.of R (Edge → R)
  | 2 => ModuleCat.of R (Triangle → R)
  | _ => ModuleCat.of R (ZeroModule R)

/-- Differentials of the canonical complete-tripartite chain complex. -/
def sourceDifferential :
    ∀ n : ℕ,
      sourceObject R (p:=p) (q:=q) (r:=r) (n+1) ⟶
        sourceObject R (p:=p) (q:=q) (r:=r) n
  | 0 => ModuleCat.ofHom
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin
  | 1 => ModuleCat.ofHom
      (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin
  | _+2 => 0

lemma sourceDifferential_sq (n : ℕ) :
    sourceDifferential R (p:=p) (q:=q) (r:=r) (n+1) ≫
        sourceDifferential R (p:=p) (q:=q) (r:=r) n = 0 := by
  rcases n with _ | _ | n
  · apply ModuleCat.hom_ext
    exact LinearMap.ext (fun x => by
      change
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec
          ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x) = 0
      rw [Matrix.mulVec_mulVec, boundary1R_boundary2R_zero,
        Matrix.zero_mulVec])
  · simp [sourceDifferential]
  · simp [sourceDifferential]

/-- The canonical complete-tripartite chain complex in `ModuleCat R`. -/
def sourceComplex : ChainComplex (ModuleCat R) ℕ :=
  ChainComplex.of
    (sourceObject R (p:=p) (q:=q) (r:=r))
    (sourceDifferential R (p:=p) (q:=q) (r:=r))
    (sourceDifferential_sq R (p:=p) (q:=q) (r:=r))

/-- Objects of the minimal complex, supported only in degrees zero and two. -/
def minimalObject : ℕ → ModuleCat R
  | 0 => ModuleCat.of R R
  | 2 => ModuleCat.of R (TopCycleIndex p q r → R)
  | _ => ModuleCat.of R (ZeroModule R)

/-- Every differential of the minimal complex vanishes. -/
def minimalDifferential :
    ∀ n : ℕ,
      minimalObject R (p:=p) (q:=q) (r:=r) (n+1) ⟶
        minimalObject R (p:=p) (q:=q) (r:=r) n
  | _ => 0

lemma minimalDifferential_sq (n : ℕ) :
    minimalDifferential R (p:=p) (q:=q) (r:=r) (n+1) ≫
        minimalDifferential R (p:=p) (q:=q) (r:=r) n = 0 := by
  simp [minimalDifferential]

/-- The zero-differential minimal model with only `H₀` and `H₂`. -/
def minimalComplex : ChainComplex (ModuleCat R) ℕ :=
  ChainComplex.of
    (minimalObject R (p:=p) (q:=q) (r:=r))
    (minimalDifferential R (p:=p) (q:=q) (r:=r))
    (minimalDifferential_sq R (p:=p) (q:=q) (r:=r))

/-- Degreewise projection from chains to the minimal model. -/
def projectionComponent :
    ∀ n : ℕ,
      (sourceComplex R (p:=p) (q:=q) (r:=r)).X n ⟶
        (minimalComplex R (p:=p) (q:=q) (r:=r)).X n
  | 0 => ModuleCat.ofHom
      (augmentationR R (p:=p) (q:=q) (r:=r))
  | 1 => 0
  | 2 => ModuleCat.ofHom
      (topCoordinateAll R (p:=p) (q:=q) (r:=r))
  | _+3 => 0

lemma projection_comm (n : ℕ) :
    projectionComponent R (p:=p) (q:=q) (r:=r) (n+1) ≫
        (minimalComplex R (p:=p) (q:=q) (r:=r)).d (n+1) n =
      (sourceComplex R (p:=p) (q:=q) (r:=r)).d (n+1) n ≫
        projectionComponent R (p:=p) (q:=q) (r:=r) n := by
  rcases n with _ | _ | n
  · apply ModuleCat.hom_ext
    exact LinearMap.ext (fun x => by
      change
        0 = augmentationR R
          ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec x)
      rw [augmentationR_boundary1R_zero])
  · change
      ModuleCat.ofHom
          (topCoordinateAll R (p:=p) (q:=q) (r:=r)) ≫ 0 =
        ModuleCat.ofHom
            (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin ≫ 0
    simp
  · rcases n with _ | n
    · change
        0 ≫ 0 =
          0 ≫ ModuleCat.ofHom
            (topCoordinateAll R (p:=p) (q:=q) (r:=r))
      simp
    · simp [projectionComponent, sourceComplex, minimalComplex,
        sourceDifferential, minimalDifferential]

/-- Chain projection onto the minimal model. -/
def projection :
    sourceComplex R (p:=p) (q:=q) (r:=r) ⟶
      minimalComplex R (p:=p) (q:=q) (r:=r) :=
  ChainComplex.ofHom
    (projectionComponent R (p:=p) (q:=q) (r:=r))
    (projection_comm R (p:=p) (q:=q) (r:=r))

/-- Degreewise inclusion of the minimal model into chains. -/
def inclusionComponent :
    ∀ n : ℕ,
      (minimalComplex R (p:=p) (q:=q) (r:=r)).X n ⟶
        (sourceComplex R (p:=p) (q:=q) (r:=r)).X n
  | 0 => ModuleCat.ofHom
      (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r))
  | 1 => 0
  | 2 => ModuleCat.ofHom
      (topHomologyInclusion R (p:=p) (q:=q) (r:=r))
  | _+3 => 0

lemma inclusion_comm (n : ℕ) :
    inclusionComponent R (p:=p) (q:=q) (r:=r) (n+1) ≫
        (sourceComplex R (p:=p) (q:=q) (r:=r)).d (n+1) n =
      (minimalComplex R (p:=p) (q:=q) (r:=r)).d (n+1) n ≫
        inclusionComponent R (p:=p) (q:=q) (r:=r) n := by
  rcases n with _ | _ | n
  · change
      0 ≫ ModuleCat.ofHom
          (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin =
        0 ≫ ModuleCat.ofHom
          (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r))
    simp
  · apply ModuleCat.hom_ext
    exact LinearMap.ext (fun g => by
      change
        (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
          (topHomologyInclusion R g) = 0
      exact boundary2_topHomologyInclusion R g)
  · rcases n with _ | n
    · change
        0 ≫ 0 =
          0 ≫ ModuleCat.ofHom
            (topHomologyInclusion R (p:=p) (q:=q) (r:=r))
      simp
    · simp [inclusionComponent, sourceComplex, minimalComplex,
        sourceDifferential, minimalDifferential]

/-- Chain inclusion of the minimal model. -/
def inclusion :
    minimalComplex R (p:=p) (q:=q) (r:=r) ⟶
      sourceComplex R (p:=p) (q:=q) (r:=r) :=
  ChainComplex.ofHom
    (inclusionComponent R (p:=p) (q:=q) (r:=r))
    (inclusion_comm R (p:=p) (q:=q) (r:=r))

lemma inclusion_projection_identity (n : ℕ) :
    (inclusion R (p:=p) (q:=q) (r:=r) ≫
        projection R (p:=p) (q:=q) (r:=r)).f n =
      ((𝟙 (minimalComplex R (p:=p) (q:=q) (r:=r))) :
        minimalComplex R (p:=p) (q:=q) (r:=r) ⟶
          minimalComplex R (p:=p) (q:=q) (r:=r)).f n := by
  rcases n with _ | _ | n
  · apply ModuleCat.hom_ext
    exact LinearMap.ext (fun c => by
      change
        augmentationR R
          (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r) c) = c
      exact augmentation_zeroHomologyInclusion R c)
  · apply ModuleCat.hom_ext
    exact LinearMap.ext (fun _ => by
      funext i
      exact Fin.elim0 i)
  · rcases n with _ | n
    · apply ModuleCat.hom_ext
      exact LinearMap.ext (fun g => by
        change
          topCoordinateAll R
            (topHomologyInclusion R (p:=p) (q:=q) (r:=r) g) = g
        exact topCoordinateAll_topHomologyInclusion R g)
    · apply ModuleCat.hom_ext
      exact LinearMap.ext (fun _ => by
        funext i
        exact Fin.elim0 i)

/-- The minimal model is a strict retract of the source complex. -/
lemma inclusion_projection_eq_id :
    inclusion R (p:=p) (q:=q) (r:=r) ≫
        projection R (p:=p) (q:=q) (r:=r) =
      𝟙 (minimalComplex R (p:=p) (q:=q) (r:=r)) := by
  apply HomologicalComplex.Hom.ext
  funext n
  exact inclusion_projection_identity R n

/-- The two nonzero components of the contracting homotopy. -/
def contractionComponent :
    ∀ n : ℕ,
      (sourceComplex R (p:=p) (q:=q) (r:=r)).X n ⟶
        (sourceComplex R (p:=p) (q:=q) (r:=r)).X (n+1)
  | 0 => ModuleCat.ofHom
      (contract0 R (p:=p) (q:=q) (r:=r))
  | 1 => ModuleCat.ofHom
      (contract1 R (p:=p) (q:=q) (r:=r))
  | _+2 => 0

/-- Full bidegree family used by Mathlib's `Homotopy` structure. -/
def contractionHom :
    ∀ i j : ℕ,
      (sourceComplex R (p:=p) (q:=q) (r:=r)).X i ⟶
        (sourceComplex R (p:=p) (q:=q) (r:=r)).X j :=
  fun i j =>
    if h : i + 1 = j then
      contractionComponent R (p:=p) (q:=q) (r:=r) i ≫
        eqToHom (by rw [h])
    else 0

lemma contractionHom_zero (i j : ℕ)
    (hrel : ¬(ComplexShape.down ℕ).Rel j i) :
    contractionHom R (p:=p) (q:=q) (r:=r) i j = 0 := by
  rw [contractionHom, dif_neg]
  simpa only [ComplexShape.down_Rel, eq_comm] using hrel

lemma projection_inclusion_homotopy_comm (n : ℕ) :
    ((𝟙 (sourceComplex R (p:=p) (q:=q) (r:=r))) :
      sourceComplex R (p:=p) (q:=q) (r:=r) ⟶
        sourceComplex R (p:=p) (q:=q) (r:=r)).f n =
      dNext n (contractionHom R (p:=p) (q:=q) (r:=r)) +
        prevD n (contractionHom R (p:=p) (q:=q) (r:=r)) +
          (projection R (p:=p) (q:=q) (r:=r) ≫
            inclusion R (p:=p) (q:=q) (r:=r)).f n := by
  rcases n with _ | _ | n
  · simp only [HomologicalComplex.id_f,
      Homotopy.dNext_zero_chainComplex,
      Homotopy.prevD_chainComplex,
      HomologicalComplex.comp_f]
    dsimp [sourceComplex, sourceObject, contractionHom,
      contractionComponent, projection, projectionComponent,
      inclusion, inclusionComponent]
    change
      𝟙 _ =
        0 +
          ModuleCat.ofHom
              (contract0 R (p:=p) (q:=q) (r:=r)) ≫
            ModuleCat.ofHom
              (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin +
          ModuleCat.ofHom
              (augmentationR R (p:=p) (q:=q) (r:=r)) ≫
            ModuleCat.ofHom
              (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r))
    apply ModuleCat.hom_ext
    exact LinearMap.ext (fun y => by
      change
        LinearMap.id y =
          (ModuleCat.Hom.hom
            (0 +
              ModuleCat.ofHom
                  (contract0 R (p:=p) (q:=q) (r:=r)) ≫
                ModuleCat.ofHom
                  (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin +
              ModuleCat.ofHom
                  (augmentationR R (p:=p) (q:=q) (r:=r)) ≫
                ModuleCat.ofHom
                  (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r)))) y
      change
        y =
          (0 +
            (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin.comp
              (contract0 R (p:=p) (q:=q) (r:=r)) +
            (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r)).comp
              (augmentationR R (p:=p) (q:=q) (r:=r))) y
      simp
      change
        y =
          (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec
              (contract0 R y) +
            zeroHomologyInclusion R (augmentationR R y)
      exact (boundary1_contract0_identity R y).symm)
  · simp only [HomologicalComplex.id_f,
      Homotopy.dNext_succ_chainComplex,
      Homotopy.prevD_chainComplex,
      HomologicalComplex.comp_f]
    dsimp [sourceComplex, sourceObject, contractionHom,
      contractionComponent, projection, projectionComponent,
      inclusion, inclusionComponent]
    change
      𝟙 _ =
        ModuleCat.ofHom
            (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin ≫
          ModuleCat.ofHom
            (contract0 R (p:=p) (q:=q) (r:=r)) +
        ModuleCat.ofHom
            (contract1 R (p:=p) (q:=q) (r:=r)) ≫
          ModuleCat.ofHom
            (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin +
        0
    apply ModuleCat.hom_ext
    exact LinearMap.ext (fun z => by
      change
        z =
          contract0 R
              ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z) +
            (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
              (contract1 R z) +
            0
      rw [add_zero, add_comm]
      exact (boundary2_contract1_identity R z).symm)
  · rcases n with _ | n
    · simp only [HomologicalComplex.id_f,
        Homotopy.dNext_succ_chainComplex,
        Homotopy.prevD_chainComplex,
        HomologicalComplex.comp_f]
      dsimp [sourceComplex, sourceObject, contractionHom,
        contractionComponent, projection, projectionComponent,
        inclusion, inclusionComponent]
      change
        𝟙 _ =
          ModuleCat.ofHom
              (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin ≫
            ModuleCat.ofHom
              (contract1 R (p:=p) (q:=q) (r:=r)) +
          0 +
          ModuleCat.ofHom
              (topCoordinateAll R (p:=p) (q:=q) (r:=r)) ≫
            ModuleCat.ofHom
              (topHomologyInclusion R (p:=p) (q:=q) (r:=r))
      apply ModuleCat.hom_ext
      exact LinearMap.ext (fun x => by
        change
          x =
            contract1 R
                ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x) +
              0 +
              topHomologyInclusion R (topCoordinateAll R x)
        rw [add_zero]
        exact (contract1_boundary2_top_identity R x).symm)
    · simp only [HomologicalComplex.id_f,
        Homotopy.dNext_succ_chainComplex,
        Homotopy.prevD_chainComplex,
        HomologicalComplex.comp_f]
      dsimp [sourceComplex, sourceObject, contractionHom,
        contractionComponent, projection, projectionComponent,
        inclusion, inclusionComponent]
      apply ModuleCat.hom_ext
      exact LinearMap.ext (fun _ => by
        funext i
        exact Fin.elim0 i)

/-- The identity is homotopic to projection followed by inclusion. -/
noncomputable def projection_inclusion_homotopy :
    Homotopy
      ((𝟙 (sourceComplex R (p:=p) (q:=q) (r:=r))) :
        sourceComplex R (p:=p) (q:=q) (r:=r) ⟶
          sourceComplex R (p:=p) (q:=q) (r:=r))
      (projection R (p:=p) (q:=q) (r:=r) ≫
        inclusion R (p:=p) (q:=q) (r:=r)) where
  hom := contractionHom R (p:=p) (q:=q) (r:=r)
  zero := contractionHom_zero R (p:=p) (q:=q) (r:=r)
  comm :=
    projection_inclusion_homotopy_comm R (p:=p) (q:=q) (r:=r)

/-- The complete tripartite chain complex is homotopy equivalent to its
zero-differential homology model over every commutative ring. -/
noncomputable def chainHomotopyEquiv :
    HomotopyEquiv
      (sourceComplex R (p:=p) (q:=q) (r:=r))
      (minimalComplex R (p:=p) (q:=q) (r:=r)) where
  hom := projection R (p:=p) (q:=q) (r:=r)
  inv := inclusion R (p:=p) (q:=q) (r:=r)
  homotopyHomInvId :=
    (projection_inclusion_homotopy R
      (p:=p) (q:=q) (r:=r)).symm
  homotopyInvHomId :=
    Homotopy.ofEq
      (inclusion_projection_eq_id R (p:=p) (q:=q) (r:=r))

end D0.Topology.GenericTripartiteChainHomotopyEquiv
