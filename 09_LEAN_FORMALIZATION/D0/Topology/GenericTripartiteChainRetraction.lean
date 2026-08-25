import D0.Topology.GenericTripartiteUniversalHomology
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-CHAIN-RETRACTION-001

The constructive `H₀`, `H₁`, and `H₂` operators are assembled into an
explicit chain deformation retraction.  Over every commutative ring `R`, the
canonical complete-tripartite chain complex retracts to

```
R  in degree 0,
0  in degree 1,
R^(Fin p × Fin q × Fin r) in degree 2.
```

The three identities are proved on chains, not inferred from homology:

```
∂₁ h₀ + i₀ p₀ = id,
∂₂ h₁ + h₀ ∂₁ = id,
h₁ ∂₂ + i₂ p₂ = id.
```

This is a chain-level algebraic bridge toward a wedge-of-2-spheres model.  It
does not by itself assert a topological homotopy equivalence.
-/

namespace D0.Topology.GenericTripartiteChainRetraction
open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFirstHomologyRing
open D0.Topology.GenericTripartiteZeroHomologyRing

variable (R : Type) [CommRing R]
variable {p q r : ℕ}
local notation "Vertex" => GenericVertex p q r
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r

/-- Root representative of degree-zero homology. -/
def zeroHomologyInclusion : R →ₗ[R] (Vertex → R) :=
  LinearMap.single R (fun _ : Vertex => R) (Sum.inl (0 : Fin (p+1)))

@[simp] lemma zeroHomologyInclusion_apply (c : R) :
    zeroHomologyInclusion R (p:=p) (q:=q) (r:=r) c =
      Pi.single (Sum.inl (0 : Fin (p+1))) c := rfl

lemma augmentation_zeroHomologyInclusion (c : R) :
    augmentationR R (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r) c) = c := by
  rw [augmentationR_apply]
  simp [Pi.single_apply]

/-- Remove the degree-zero homology representative. -/
def reducedZeroChain : (Vertex → R) →ₗ[R] (Vertex → R) :=
  LinearMap.id -
    (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r)).comp
      (augmentationR R (p:=p) (q:=q) (r:=r))

lemma augmentation_reducedZeroChain (y : Vertex → R) :
    augmentationR R (reducedZeroChain R y) = 0 := by
  change
    augmentationR R
      (y - zeroHomologyInclusion R (augmentationR R y)) = 0
  rw [map_sub, augmentation_zeroHomologyInclusion, sub_self]

/-- The explicit spanning-tree formula as a linear map. -/
def zeroChainFillingLinear : (Vertex → R) →ₗ[R] (Edge → R) where
  toFun := zeroChainFilling R
  map_add' x y := by
    funext e
    rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      refine Fin.cases ?_ (fun i => ?_) a
      · refine Fin.cases ?_ (fun j => ?_) b
        · simp [zeroChainFilling, Finset.sum_add_distrib]
          abel
        · simp [zeroChainFilling]
      · refine Fin.cases ?_ (fun j => ?_) b
        · simp [zeroChainFilling]
          abel
        · simp [zeroChainFilling]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        refine Fin.cases ?_ (fun i => ?_) a <;> simp [zeroChainFilling]
      · simp [zeroChainFilling]
  map_smul' c x := by
    funext e
    rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      refine Fin.cases ?_ (fun i => ?_) a
      · refine Fin.cases ?_ (fun j => ?_) b
        · simp [zeroChainFilling]
          rw [mul_add, Finset.mul_sum]
        · simp [zeroChainFilling]
      · refine Fin.cases ?_ (fun j => ?_) b
        · simp [zeroChainFilling]
        · simp [zeroChainFilling]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c'⟩
        refine Fin.cases ?_ (fun i => ?_) a <;> simp [zeroChainFilling]
      · simp [zeroChainFilling]

/-- Degree-zero contracting homotopy. -/
def contract0 : (Vertex → R) →ₗ[R] (Edge → R) :=
  (zeroChainFillingLinear R).comp (reducedZeroChain R)

lemma boundary1_contract0 (y : Vertex → R) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec (contract0 R y) =
      reducedZeroChain R y := by
  exact boundary1R_zeroChainFilling R _ (augmentation_reducedZeroChain R y)

lemma boundary1_contract0_identity (y : Vertex → R) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec (contract0 R y) +
      zeroHomologyInclusion R (augmentationR R y) = y := by
  rw [boundary1_contract0]
  change
    y - zeroHomologyInclusion R (augmentationR R y) +
      zeroHomologyInclusion R (augmentationR R y) = y
  abel


/-- The explicit 1-cycle filler vanishes on every all-nonroot triangle. -/
theorem oneCycleFilling_nonroot
    (z : OneCycle R (p:=p) (q:=q) (r:=r))
    (i : Fin p) (j : Fin q) (k : Fin r) :
    oneCycleFilling R z (i.succ,j.succ,k.succ) = 0 := by
  simp [oneCycleFilling, residualFill, Fin.succ_ne_zero]

/-- A triangle chain is determined by its boundary and all-nonroot
coordinates. -/
theorem triangleChain_ext
    {x y : Triangle → R}
    (hBoundary :
      (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x =
        (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec y)
    (hCoordinate : ∀ i : TopCycleIndex p q r,
      x (i.1.succ,i.2.1.succ,i.2.2.succ) =
        y (i.1.succ,i.2.1.succ,i.2.2.succ)) :
    x = y := by
  let z : TopKernel R (p:=p) (q:=q) (r:=r) :=
    ⟨x-y, by
      rw [LinearMap.mem_ker, Matrix.mulVecLin_apply,
        Matrix.mulVec_sub, hBoundary, sub_self]⟩
  have hzcoord : topCoordinateR R z = 0 := by
    funext i
    change
      x (i.1.succ,i.2.1.succ,i.2.2.succ) -
        y (i.1.succ,i.2.1.succ,i.2.2.succ) = 0
    rw [hCoordinate]
    exact sub_self _
  have hz : z = 0 := (topCoordinateR_injective R) (by
    simpa using hzcoord)
  have hzval : x-y = 0 := congrArg Subtype.val hz
  exact sub_eq_zero.mp hzval

/-- The explicit universal 1-cycle filler as a linear map. -/
def oneCycleFillingLinear :
    OneCycle R (p:=p) (q:=q) (r:=r) →ₗ[R] (Triangle → R) where
  toFun := oneCycleFilling R
  map_add' x y := by
    apply triangleChain_ext R
    · rw [Matrix.mulVec_add,
        boundary2R_oneCycleFilling, boundary2R_oneCycleFilling,
        boundary2R_oneCycleFilling]
      rfl
    · intro i
      simp [oneCycleFilling_nonroot]
  map_smul' scalar x := by
    apply triangleChain_ext R
    · rw [Matrix.mulVec_smul,
        boundary2R_oneCycleFilling, boundary2R_oneCycleFilling]
      rfl
    · intro i
      simp [oneCycleFilling_nonroot]

/-- Remove the degree-zero tree part of an arbitrary edge chain. -/
def reducedOneChainLinear : (Edge → R) →ₗ[R] (Edge → R) :=
  LinearMap.id -
    (contract0 R).comp
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin

abbrev reducedOneChain (z : Edge → R) : Edge → R :=
  reducedOneChainLinear R z

@[simp] lemma reducedOneChain_apply (z : Edge → R) :
    reducedOneChain R z =
      z - contract0 R
        ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z) := rfl

lemma augmentation_boundary1R (z : Edge → R) :
    augmentationR R
      ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z) = 0 :=
  augmentationR_boundary1R_zero R z

lemma reducedZeroChain_boundary1R (z : Edge → R) :
    reducedZeroChain R
      ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z) =
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z := by
  change
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z -
      zeroHomologyInclusion R
        (augmentationR R
          ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z)) = _
  rw [augmentation_boundary1R]
  simp

lemma reducedOneChain_cycle (z : Edge → R) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec
      (reducedOneChain R z) = 0 := by
  rw [reducedOneChain_apply]
  rw [Matrix.mulVec_sub, boundary1_contract0, reducedZeroChain_boundary1R]
  exact sub_self _

/-- The cycle part of an arbitrary edge chain. -/
def reducedOneCycle : (Edge → R) →ₗ[R]
    OneCycle R (p:=p) (q:=q) (r:=r) where
  toFun z := ⟨reducedOneChain R z, by
    rw [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    exact reducedOneChain_cycle R z⟩
  map_add' x y := by
    apply Subtype.ext
    exact map_add (reducedOneChainLinear R) x y
  map_smul' c x := by
    apply Subtype.ext
    exact map_smul (reducedOneChainLinear R) c x

/-- Degree-one contracting homotopy. -/
def contract1 : (Edge → R) →ₗ[R] (Triangle → R) :=
  (oneCycleFillingLinear R).comp (reducedOneCycle R)

lemma boundary2_contract1 (z : Edge → R) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec (contract1 R z) =
      reducedOneChain R z := by
  exact boundary2R_oneCycleFilling R (reducedOneCycle R z)

lemma boundary2_contract1_identity (z : Edge → R) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec (contract1 R z) +
      contract0 R
        ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z) = z := by
  rw [boundary2_contract1]
  rw [reducedOneChain_apply]
  abel


/-- Read the all-nonroot coordinates of an arbitrary 2-chain. -/
def topCoordinateAll : (Triangle → R) →ₗ[R]
    (TopCycleIndex p q r → R) :=
  LinearMap.pi (fun i =>
    LinearMap.proj (R:=R) (φ:=fun _ : Triangle => R)
      (i.1.succ,i.2.1.succ,i.2.2.succ))

@[simp] lemma topCoordinateAll_apply
    (x : Triangle → R) (i : TopCycleIndex p q r) :
    topCoordinateAll R x i =
      x (i.1.succ,i.2.1.succ,i.2.2.succ) := rfl

/-- Include the top homology model by octahedral synthesis. -/
def topHomologyInclusion :
    (TopCycleIndex p q r → R) →ₗ[R] (Triangle → R) :=
  (LinearMap.ker
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin).subtype.comp
      (topSynthesisR R)

lemma boundary2_topHomologyInclusion
    (g : TopCycleIndex p q r → R) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
      (topHomologyInclusion R g) = 0 := by
  have h := (topSynthesisR R g).property
  rw [LinearMap.mem_ker, Matrix.mulVecLin_apply] at h
  exact h

@[simp] lemma topCoordinateAll_topHomologyInclusion
    (g : TopCycleIndex p q r → R) :
    topCoordinateAll R (topHomologyInclusion R g) = g := by
  simpa [topCoordinateAll, topHomologyInclusion, topCoordinateR,
    topCoordinateAtR] using topCoordinateR_topSynthesisR R g

lemma reducedOneChain_boundary2 (x : Triangle → R) :
    reducedOneChain R
      ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x) =
      (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x := by
  rw [reducedOneChain_apply]
  have hzero :
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec
        ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x) = 0 := by
    rw [Matrix.mulVec_mulVec, boundary1R_boundary2R_zero,
      Matrix.zero_mulVec]
  rw [hzero, map_zero, sub_zero]

lemma boundary2_contract1_boundary2 (x : Triangle → R) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
      (contract1 R
        ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x)) =
      (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x := by
  rw [boundary2_contract1, reducedOneChain_boundary2]

lemma contract1_boundary2_nonroot
    (x : Triangle → R) (i : Fin p) (j : Fin q) (k : Fin r) :
    contract1 R
      ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x)
      (i.succ,j.succ,k.succ) = 0 := by
  exact oneCycleFilling_nonroot R _ i j k

/-- Degree-two contracting identity: the surviving part is exactly the
octahedral top-homology projection. -/
theorem contract1_boundary2_top_identity (x : Triangle → R) :
    contract1 R
        ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x) +
      topHomologyInclusion R (topCoordinateAll R x) = x := by
  apply triangleChain_ext R
  · rw [Matrix.mulVec_add, boundary2_contract1_boundary2,
      boundary2_topHomologyInclusion, add_zero]
  · intro i
    rcases i with ⟨ia,ib,ic⟩
    simp only [Pi.add_apply]
    rw [contract1_boundary2_nonroot]
    change
      0 + topCoordinateR R
        (topSynthesisR R (topCoordinateAll R x)) (ia,ib,ic) =
          x (ia.succ,ib.succ,ic.succ)
    rw [topCoordinateR_topSynthesisR]
    simp [topCoordinateAll_apply]

/-- The three explicit identities form a chain deformation retraction onto
`R` in degree zero and `R^(p*q*r)` in degree two. -/
structure ChainRetractionPassport where
  degree0 : ∀ y : Vertex → R,
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec (contract0 R y) +
      zeroHomologyInclusion R (augmentationR R y) = y
  degree1 : ∀ z : Edge → R,
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec (contract1 R z) +
      contract0 R
        ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec z) = z
  degree2 : ∀ x : Triangle → R,
    contract1 R
        ((boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x) +
      topHomologyInclusion R (topCoordinateAll R x) = x
  degree0Split : ∀ c : R,
    augmentationR R (zeroHomologyInclusion R (p:=p) (q:=q) (r:=r) c) = c
  degree2Split : ∀ g : TopCycleIndex p q r → R,
    topCoordinateAll R (topHomologyInclusion R g) = g

noncomputable def chainRetractionPassport :
    ChainRetractionPassport R (p:=p) (q:=q) (r:=r) where
  degree0 := boundary1_contract0_identity R
  degree1 := boundary2_contract1_identity R
  degree2 := contract1_boundary2_top_identity R
  degree0Split := augmentation_zeroHomologyInclusion R
  degree2Split := topCoordinateAll_topHomologyInclusion R

end D0.Topology.GenericTripartiteChainRetraction
