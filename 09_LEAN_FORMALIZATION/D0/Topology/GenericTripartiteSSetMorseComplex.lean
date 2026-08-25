import D0.Topology.GenericTripartiteMorseComplex
import D0.Topology.GenericTripartiteSimplicialMorse
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-SSET-MORSE-COMPLEX-001

This module closes the chain-level interface between the literal Mathlib
simplicial-set realization and the previously constructed Morse complex.

The zero-differential free complex is now built directly on the actual
critical nondegenerate simplices of `GenericTripartiteSimplicialMorse`.
Degreewise equivalences identify it strictly with
`GenericTripartiteMorseComplex.criticalComplex`.  Consequently the source
simplicial chains are homotopy equivalent to a complex whose basis is the
critical simplices of the actual `SSet`.

The identification is explicit on generators:

* the unique critical zero-simplex is the root simplex and maps to the root
  degree-zero representative;
* the critical two-simplex indexed by `(i,j,k)` is the all-nonroot triangle
  and maps to its eight-triangle octahedral cycle.

This remains a chain-level theorem.  It does not turn the critical simplices
into a spatial subcomplex (which is impossible when `p*q*r ≠ 0`) and does not
assert the missing Forman/CW realization theorem.
-/

namespace D0.Topology.GenericTripartiteSSetMorseComplex

open CategoryTheory
open HomologicalComplex
open D0.Topology.GenericTripartiteMorseComplex
open D0.Topology.GenericTripartiteSimplicialMorse
open D0.Topology.GenericTripartiteSimplicialSet
open D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteZeroHomologyRing
open D0.Topology.GenericTripartiteChainRetraction
open D0.Topology.GenericTripartiteChainHomotopyEquiv

variable (R : Type) [CommRing R]
variable {p q r : ℕ}

abbrev ZeroModule := Fin 0 → R

/-- Free modules on the actual critical nondegenerate simplices. -/
def ssetCriticalObject : ℕ → ModuleCat R
  | 0 => ModuleCat.of R (CriticalZeroSimplex p q r → R)
  | 1 => ModuleCat.of R (CriticalOneSimplex p q r → R)
  | 2 => ModuleCat.of R (CriticalTwoSimplex p q r → R)
  | _ => ModuleCat.of R (ZeroModule R)

/-- The lacunary complex on actual critical simplices has zero differential. -/
def ssetCriticalDifferential :
    ∀ n : ℕ,
      ssetCriticalObject R (p:=p) (q:=q) (r:=r) (n+1) ⟶
        ssetCriticalObject R (p:=p) (q:=q) (r:=r) n
  | _ => 0

lemma ssetCriticalDifferential_sq (n : ℕ) :
    ssetCriticalDifferential R (p:=p) (q:=q) (r:=r) (n+1) ≫
      ssetCriticalDifferential R (p:=p) (q:=q) (r:=r) n = 0 := by
  simp [ssetCriticalDifferential]

/-- Zero-differential free complex on the actual critical simplices. -/
def ssetCriticalComplex : ChainComplex (ModuleCat R) ℕ :=
  ChainComplex.of
    (ssetCriticalObject R (p:=p) (q:=q) (r:=r))
    (ssetCriticalDifferential R (p:=p) (q:=q) (r:=r))
    (ssetCriticalDifferential_sq R (p:=p) (q:=q) (r:=r))

noncomputable def ssetCriticalZeroLinearEquiv :
    (CriticalZeroSimplex p q r → R) ≃ₗ[R]
      (CriticalZero p q r → R) :=
  LinearEquiv.funCongrLeft R R
    (criticalZeroSimplexEquiv (p:=p) (q:=q) (r:=r)).symm

noncomputable def ssetCriticalOneLinearEquiv :
    (CriticalOneSimplex p q r → R) ≃ₗ[R]
      (CriticalOne p q r → R) :=
  LinearEquiv.funCongrLeft R R
    (criticalOneSimplexEquiv (p:=p) (q:=q) (r:=r)).symm

noncomputable def ssetCriticalTwoLinearEquiv :
    (CriticalTwoSimplex p q r → R) ≃ₗ[R]
      (CriticalTwo p q r → R) :=
  LinearEquiv.funCongrLeft R R
    (criticalTwoSimplexEquiv (p:=p) (q:=q) (r:=r)).symm

noncomputable def ssetCriticalComponentIso :
    ∀ n : ℕ,
      (ssetCriticalComplex R (p:=p) (q:=q) (r:=r)).X n ≅
        (criticalComplex R (p:=p) (q:=q) (r:=r)).X n
  | 0 => (ssetCriticalZeroLinearEquiv R
      (p:=p) (q:=q) (r:=r)).toModuleIso
  | 1 => (ssetCriticalOneLinearEquiv R
      (p:=p) (q:=q) (r:=r)).toModuleIso
  | 2 => (ssetCriticalTwoLinearEquiv R
      (p:=p) (q:=q) (r:=r)).toModuleIso
  | _+3 => (LinearEquiv.refl R (Fin 0 → R)).toModuleIso

/-- The free complex on actual critical simplices is strictly isomorphic to
the typed critical-cell complex. -/
noncomputable def ssetCriticalIso :
    ssetCriticalComplex R (p:=p) (q:=q) (r:=r) ≅
      criticalComplex R (p:=p) (q:=q) (r:=r) :=
  HomologicalComplex.Hom.isoOfComponents
    (ssetCriticalComponentIso R (p:=p) (q:=q) (r:=r))
    (by
      intro i j hij
      simp only [ComplexShape.down_Rel] at hij
      subst i
      simp [ssetCriticalComplex, criticalComplex,
        ssetCriticalDifferential, criticalDifferential])

/-- Coordinates of actual critical zero-simplices. -/
noncomputable def ssetCriticalZeroCoordinateEquiv :
    (CriticalZeroSimplex p q r → R) ≃ₗ[R] R :=
  (ssetCriticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).trans
    (criticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r))

/-- Coordinates of actual critical two-simplices. -/
noncomputable def ssetCriticalTwoCoordinateEquiv :
    (CriticalTwoSimplex p q r → R) ≃ₗ[R]
      (TopCycleIndex p q r → R) :=
  (ssetCriticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).trans
    (criticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r))

/-- The actual `SSet` critical-simplex complex is strictly isomorphic to the
algebraic minimal complex. -/
noncomputable def ssetCriticalMinimalIso :
    ssetCriticalComplex R (p:=p) (q:=q) (r:=r) ≅
      minimalComplex R (p:=p) (q:=q) (r:=r) :=
  (ssetCriticalIso R (p:=p) (q:=q) (r:=r)).trans
    (criticalMinimalIso R (p:=p) (q:=q) (r:=r))

/-- Source chains are homotopy equivalent to the free complex on the actual
critical nondegenerate simplices. -/
noncomputable def sourceSSetCriticalHomotopyEquiv :
    HomotopyEquiv
      (sourceComplex R (p:=p) (q:=q) (r:=r))
      (ssetCriticalComplex R (p:=p) (q:=q) (r:=r)) :=
  (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).trans
    (HomotopyEquiv.ofIso
      (ssetCriticalIso R (p:=p) (q:=q) (r:=r)).symm)

/-- General projection from source zero-chains to functions on the actual
critical zero-simplex. -/
@[simp] theorem sourceSSetCritical_hom_zero
    (x : D0.Topology.GenericTripartiteHomology.GenericVertex p q r → R) :
    (sourceSSetCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).hom.f 0 x =
      (ssetCriticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
        ((criticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
          (augmentationR R x)) := by
  rfl

/-- General inclusion of actual critical zero-simplex coordinates into source
zero-chains. -/
@[simp] theorem sourceSSetCritical_inv_zero
    (g : CriticalZeroSimplex p q r → R) :
    (sourceSSetCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).inv.f 0 g =
      zeroHomologyInclusion R
        (criticalZeroLinearEquiv R
          (ssetCriticalZeroLinearEquiv R g)) := by
  rfl

/-- General projection from source two-chains to functions on the actual
critical two-simplices. -/
@[simp] theorem sourceSSetCritical_hom_two
    (x : D0.Topology.GenericTripartiteHomology.GenericTriangle p q r → R) :
    (sourceSSetCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).hom.f 2 x =
      (ssetCriticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
        ((criticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
          (topCoordinateAll R x)) := by
  rfl

/-- General inclusion of actual critical two-simplex coordinates into source
two-chains. -/
@[simp] theorem sourceSSetCritical_inv_two
    (g : CriticalTwoSimplex p q r → R) :
    (sourceSSetCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).inv.f 2 g =
      topHomologyInclusion R
        (criticalTwoLinearEquiv R
          (ssetCriticalTwoLinearEquiv R g)) := by
  rfl

/-- The actual critical zero-simplex, packaged in its degreewise subtype. -/
noncomputable def criticalZeroSimplexPoint : CriticalZeroSimplex p q r :=
  (criticalZeroSimplexEquiv (p:=p) (q:=q) (r:=r)).symm
    (Face.criticalZeroFaceMap ())

@[simp] theorem criticalZeroSimplexEquiv_criticalZeroSimplexPoint :
    criticalZeroSimplexEquiv
      (criticalZeroSimplexPoint (p:=p) (q:=q) (r:=r)) =
        Face.criticalZeroFaceMap () := by
  exact Equiv.apply_symm_apply _ _

/-- Actual critical zero-simplex coordinates are evaluation at the root
critical simplex. -/
@[simp] theorem ssetCriticalZeroCoordinateEquiv_apply
    (g : CriticalZeroSimplex p q r → R) :
    ssetCriticalZeroCoordinateEquiv R g =
      g (criticalZeroSimplexPoint (p:=p) (q:=q) (r:=r)) := by
  rfl

/-- The actual critical zero-simplex is the root simplex. -/
@[simp] theorem criticalZeroSimplexPoint_val :
    (criticalZeroSimplexPoint (p:=p) (q:=q) (r:=r)).1 =
      rootSimplex := by
  apply (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).injective
  calc
    nondegenerateFaceEquiv
        (criticalZeroSimplexPoint (p:=p) (q:=q) (r:=r)).1 =
        (Face.criticalZeroFaceMap () :
          Face.CriticalZeroFace p q r).1 := by
      exact congrArg Subtype.val
        (criticalZeroSimplexEquiv_criticalZeroSimplexPoint
          (p:=p) (q:=q) (r:=r))
    _ = Face.root := rfl
    _ = nondegenerateFaceEquiv
        (rootSimplex (p:=p) (q:=q) (r:=r)) :=
      nondegenerateFaceEquiv_rootSimplex.symm

/-- Basis vector of the actual critical zero-simplex. -/
noncomputable def ssetCriticalZeroGenerator :
    CriticalZeroSimplex p q r → R :=
  (ssetCriticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
    (criticalZeroGenerator R)

@[simp] theorem ssetCriticalZeroLinearEquiv_generator :
    ssetCriticalZeroLinearEquiv R
      (ssetCriticalZeroGenerator R (p:=p) (q:=q) (r:=r)) =
        criticalZeroGenerator R := by
  exact LinearEquiv.apply_symm_apply _ _

/-- Actual critical two-simplex indexed by a top-cycle coordinate. -/
noncomputable def criticalTwoSimplexMap
    (i : TopCycleIndex p q r) : CriticalTwoSimplex p q r :=
  (criticalTwoSimplexEquiv (p:=p) (q:=q) (r:=r)).symm
    (Face.criticalTwoFaceMap i)

@[simp] theorem criticalTwoSimplexEquiv_criticalTwoSimplexMap
    (i : TopCycleIndex p q r) :
    criticalTwoSimplexEquiv (criticalTwoSimplexMap i) =
      Face.criticalTwoFaceMap i := by
  exact Equiv.apply_symm_apply _ _

/-- Actual critical two-simplex coordinates are evaluation on the indexed
critical simplex. -/
@[simp] theorem ssetCriticalTwoCoordinateEquiv_apply
    (g : CriticalTwoSimplex p q r → R)
    (i : TopCycleIndex p q r) :
    ssetCriticalTwoCoordinateEquiv R g i =
      g (criticalTwoSimplexMap i) := by
  rfl

/-- The indexed actual critical two-simplex is precisely the nondegenerate
simplex of the all-nonroot critical triangle. -/
@[simp] theorem criticalTwoSimplexMap_val
    (i : TopCycleIndex p q r) :
    (criticalTwoSimplexMap i).1 =
      faceNondegenerateEquiv (Face.criticalTriangle i) := by
  apply (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).injective
  calc
    nondegenerateFaceEquiv (criticalTwoSimplexMap i).1 =
        (Face.criticalTwoFaceMap i :
          Face.CriticalTwoFace p q r).1 := by
      exact congrArg Subtype.val
        (criticalTwoSimplexEquiv_criticalTwoSimplexMap
          (p:=p) (q:=q) (r:=r) i)
    _ = Face.criticalTriangle i := rfl
    _ = nondegenerateFaceEquiv
        (faceNondegenerateEquiv (Face.criticalTriangle i)) :=
      ((nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).apply_symm_apply
        (Face.criticalTriangle i)).symm

/-- Basis vector of an indexed actual critical two-simplex. -/
noncomputable def ssetCriticalTwoGenerator (i : TopCycleIndex p q r) :
    CriticalTwoSimplex p q r → R :=
  (ssetCriticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
    (criticalTwoGenerator R i)

@[simp] theorem ssetCriticalTwoLinearEquiv_generator
    (i : TopCycleIndex p q r) :
    ssetCriticalTwoLinearEquiv R (ssetCriticalTwoGenerator R i) =
      criticalTwoGenerator R i := by
  exact LinearEquiv.apply_symm_apply _ _

/-- The root generator has coordinate `1`. -/
@[simp] theorem ssetCriticalZeroCoordinateEquiv_generator :
    ssetCriticalZeroCoordinateEquiv R
      (ssetCriticalZeroGenerator R (p:=p) (q:=q) (r:=r)) = 1 := by
  rw [ssetCriticalZeroCoordinateEquiv, LinearEquiv.trans_apply,
      ssetCriticalZeroLinearEquiv_generator,
      criticalZeroLinearEquiv_generator]

/-- An indexed critical two-simplex generator has the corresponding standard
coordinate vector. -/
@[simp] theorem ssetCriticalTwoCoordinateEquiv_generator
    (i : TopCycleIndex p q r) :
    ssetCriticalTwoCoordinateEquiv R (ssetCriticalTwoGenerator R i) =
      Pi.single i 1 := by
  rw [ssetCriticalTwoCoordinateEquiv, LinearEquiv.trans_apply,
      ssetCriticalTwoLinearEquiv_generator,
      criticalTwoLinearEquiv_generator]

/-- The root generator evaluates to `1` on the actual root simplex. -/
@[simp] theorem ssetCriticalZeroGenerator_at_point :
    ssetCriticalZeroGenerator R
      (criticalZeroSimplexPoint (p:=p) (q:=q) (r:=r)) = 1 := by
  calc
    ssetCriticalZeroGenerator R
        (criticalZeroSimplexPoint (p:=p) (q:=q) (r:=r)) =
        ssetCriticalZeroCoordinateEquiv R
          (ssetCriticalZeroGenerator R (p:=p) (q:=q) (r:=r)) :=
      (ssetCriticalZeroCoordinateEquiv_apply R
        (ssetCriticalZeroGenerator R (p:=p) (q:=q) (r:=r))).symm
    _ = 1 := ssetCriticalZeroCoordinateEquiv_generator R

/-- Exact Kronecker formula on actual critical two-simplices. -/
@[simp] theorem ssetCriticalTwoGenerator_at_map
    (i j : TopCycleIndex p q r) :
    ssetCriticalTwoGenerator R i (criticalTwoSimplexMap j) =
      if j = i then 1 else 0 := by
  calc
    ssetCriticalTwoGenerator R i (criticalTwoSimplexMap j) =
        ssetCriticalTwoCoordinateEquiv R
          (ssetCriticalTwoGenerator R i) j :=
      (ssetCriticalTwoCoordinateEquiv_apply R
        (ssetCriticalTwoGenerator R i) j).symm
    _ = if j = i then 1 else 0 := by
      have h := congrFun
        (ssetCriticalTwoCoordinateEquiv_generator R i) j
      simpa only [Pi.single_apply] using h

/-- Degree-zero component of the strict isomorphism to the minimal complex. -/
@[simp] theorem ssetCriticalMinimalIso_hom_zero
    (g : CriticalZeroSimplex p q r → R) :
    (ssetCriticalMinimalIso R (p:=p) (q:=q) (r:=r)).hom.f 0 g =
      ssetCriticalZeroCoordinateEquiv R g := by
  rfl

/-- Degree-two component of the strict isomorphism to the minimal complex. -/
@[simp] theorem ssetCriticalMinimalIso_hom_two
    (g : CriticalTwoSimplex p q r → R) :
    (ssetCriticalMinimalIso R (p:=p) (q:=q) (r:=r)).hom.f 2 g =
      ssetCriticalTwoCoordinateEquiv R g := by
  rfl

/-- Generator-level synthesis: the actual critical two-simplex indexed by
`i` maps to the corresponding eight-triangle octahedral cycle. -/
@[simp] theorem sourceSSetCritical_inv_generator_two
    (i : TopCycleIndex p q r) :
    (sourceSSetCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).inv.f 2
      (ssetCriticalTwoGenerator R i) = topCycleVecR R i := by
  change
    (sourceCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).inv.f 2
      (ssetCriticalTwoLinearEquiv R
        (ssetCriticalTwoGenerator R i)) = _
  rw [ssetCriticalTwoLinearEquiv_generator,
      sourceCritical_inv_generator_two]

/-- Generator-level synthesis in degree zero from the actual critical
root simplex. -/
@[simp] theorem sourceSSetCritical_inv_generator_zero :
    (sourceSSetCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).inv.f 0
      (ssetCriticalZeroGenerator R (p:=p) (q:=q) (r:=r)) =
        zeroHomologyInclusion R (1 : R) := by
  change
    (sourceCriticalHomotopyEquiv R
      (p:=p) (q:=q) (r:=r)).inv.f 0
      (ssetCriticalZeroLinearEquiv R
        (ssetCriticalZeroGenerator R)) = _
  rw [ssetCriticalZeroLinearEquiv_generator,
      sourceCritical_inv_generator_zero]

end D0.Topology.GenericTripartiteSSetMorseComplex
