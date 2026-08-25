import D0.Topology.GenericTripartitePerfectMorse
import D0.Topology.GenericTripartiteChainHomotopyEquiv
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-MORSE-COMPLEX-001

This module identifies the two independently constructed minimal models of
the complete-tripartite clique complex:

* the algebraic minimal complex from the explicit chain deformation
  retraction;
* the free complex on the actual critical cells of the perfect discrete Morse
  matching.

For every commutative ring `R`, the critical-cell complex has zero differential
and is strictly isomorphic to the algebraic minimal complex.  Composing with
the existing chain homotopy equivalence gives

```
C_*(K(p+1,q+1,r+1); R) ≃ₕ
  R[critical 0-cell] ⊕ R[critical 2-cells][2].
```

The identification is proved on generators, not just by cardinality:

* the unique critical `0`-cell maps to the root representative of `H₀`;
* the critical `2`-cell indexed by `(i,j,k)` maps to the explicit
  eight-triangle octahedral cycle

```
(e_(i+1)-e_0) ⊗ (e_(j+1)-e_0) ⊗ (e_(k+1)-e_0).
```

This is the exact chain-level Morse synthesis.  It still does not assert the
missing spatial realization theorem or a topological `HomotopyEquiv` of
geometric realizations.
-/

namespace D0.Topology.GenericTripartiteMorseComplex

open CategoryTheory
open HomologicalComplex
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteZeroHomologyRing
open D0.Topology.GenericTripartiteChainRetraction
open D0.Topology.GenericTripartiteChainHomotopyEquiv
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteDiscreteMorse.Face

variable (R : Type) [CommRing R]
variable {p q r : ℕ}

abbrev CriticalZero (p q r : ℕ) := CriticalZeroFace p q r
abbrev CriticalOne (p q r : ℕ) := CriticalOneFace p q r
abbrev CriticalTwo (p q r : ℕ) := CriticalTwoFace p q r
abbrev ZeroModule := Fin 0 → R

/-- Free modules on the actual critical cells. -/
def criticalObject : ℕ → ModuleCat R
  | 0 => ModuleCat.of R (CriticalZero p q r → R)
  | 1 => ModuleCat.of R (CriticalOne p q r → R)
  | 2 => ModuleCat.of R (CriticalTwo p q r → R)
  | _ => ModuleCat.of R (ZeroModule R)

/-- The lacunary critical-cell model has zero differential. -/
def criticalDifferential :
    ∀ n : ℕ,
      criticalObject R (p:=p) (q:=q) (r:=r) (n+1) ⟶
        criticalObject R (p:=p) (q:=q) (r:=r) n
  | _ => 0

lemma criticalDifferential_sq (n : ℕ) :
    criticalDifferential R (p:=p) (q:=q) (r:=r) (n+1) ≫
        criticalDifferential R (p:=p) (q:=q) (r:=r) n = 0 := by
  simp [criticalDifferential]

/-- Zero-differential free complex on the perfect critical cells. -/
def criticalComplex : ChainComplex (ModuleCat R) ℕ :=
  ChainComplex.of
    (criticalObject R (p:=p) (q:=q) (r:=r))
    (criticalDifferential R (p:=p) (q:=q) (r:=r))
    (criticalDifferential_sq R (p:=p) (q:=q) (r:=r))

/-- Degree-zero critical-cell functions are canonically one copy of `R`. -/
noncomputable def criticalZeroLinearEquiv :
    (CriticalZero p q r → R) ≃ₗ[R] R :=
  (LinearEquiv.funCongrLeft R R
    (criticalZeroFaceEquiv (p:=p) (q:=q) (r:=r)).symm).trans
      (LinearEquiv.funUnique Unit R R)

/-- Degree-one critical-cell functions are the zero module. -/
noncomputable def criticalOneLinearEquiv :
    (CriticalOne p q r → R) ≃ₗ[R] (Fin 0 → R) :=
  letI : IsEmpty (CriticalOne p q r) :=
    criticalOneFace_isEmpty (p:=p) (q:=q) (r:=r)
  LinearEquiv.funCongrLeft R R
    (Equiv.equivOfIsEmpty (Fin 0) (CriticalOne p q r))

/-- Degree-two critical-cell functions are the octahedral coordinate module. -/
noncomputable def criticalTwoLinearEquiv :
    (CriticalTwo p q r → R) ≃ₗ[R] (TopCycleIndex p q r → R) :=
  LinearEquiv.funCongrLeft R R
    (criticalTwoFaceEquiv (p:=p) (q:=q) (r:=r)).symm

noncomputable def criticalMinimalComponentIso :
    ∀ n : ℕ,
      (criticalComplex R (p:=p) (q:=q) (r:=r)).X n ≅
        (minimalComplex R (p:=p) (q:=q) (r:=r)).X n
  | 0 => (criticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).toModuleIso
  | 1 => (criticalOneLinearEquiv R (p:=p) (q:=q) (r:=r)).toModuleIso
  | 2 => (criticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).toModuleIso
  | _+3 => (LinearEquiv.refl R (Fin 0 → R)).toModuleIso

/-- The free critical-cell complex is strictly isomorphic to the algebraic
minimal complex. -/
noncomputable def criticalMinimalIso :
    criticalComplex R (p:=p) (q:=q) (r:=r) ≅
      minimalComplex R (p:=p) (q:=q) (r:=r) :=
  HomologicalComplex.Hom.isoOfComponents
    (criticalMinimalComponentIso R (p:=p) (q:=q) (r:=r))
    (by
      intro i j hij
      simp only [ComplexShape.down_Rel] at hij
      subst i
      simp [criticalComplex, minimalComplex, criticalDifferential,
        minimalDifferential])

/-- Source chains are homotopy equivalent to the perfect critical-cell
complex over every commutative ring. -/
noncomputable def sourceCriticalHomotopyEquiv :
    HomotopyEquiv
      (sourceComplex R (p:=p) (q:=q) (r:=r))
      (criticalComplex R (p:=p) (q:=q) (r:=r)) :=
  (chainHomotopyEquiv R (p:=p) (q:=q) (r:=r)).trans
    (HomotopyEquiv.ofIso
      (criticalMinimalIso R (p:=p) (q:=q) (r:=r)).symm)

/-- General degree-zero projection formula. -/
@[simp] theorem sourceCritical_hom_zero
    (x : GenericVertex p q r → R) :
    (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).hom.f 0 x =
      (criticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
        (augmentationR R x) := by
  rfl

/-- General degree-zero inclusion formula. -/
@[simp] theorem sourceCritical_inv_zero
    (g : CriticalZero p q r → R) :
    (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).inv.f 0 g =
      zeroHomologyInclusion R
        (criticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r) g) := by
  rfl

/-- General degree-two projection formula. -/
@[simp] theorem sourceCritical_hom_two
    (x : GenericTriangle p q r → R) :
    (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).hom.f 2 x =
      (criticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
        (topCoordinateAll R x) := by
  rfl

/-- General degree-two inclusion formula. -/
@[simp] theorem sourceCritical_inv_two
    (g : CriticalTwo p q r → R) :
    (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).inv.f 2 g =
      topHomologyInclusion R
        (criticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r) g) := by
  rfl

/-- The canonical basis vector of the critical `2`-cell indexed by `i`. -/
noncomputable def criticalTwoGenerator (i : TopCycleIndex p q r) :
    CriticalTwo p q r → R :=
  (criticalTwoLinearEquiv R (p:=p) (q:=q) (r:=r)).symm
    (Pi.single i 1)

/-- The canonical basis vector of the unique critical `0`-cell. -/
noncomputable def criticalZeroGenerator : CriticalZero p q r → R :=
  (criticalZeroLinearEquiv R (p:=p) (q:=q) (r:=r)).symm 1

@[simp] theorem criticalTwoLinearEquiv_generator (i : TopCycleIndex p q r) :
    criticalTwoLinearEquiv R
      (criticalTwoGenerator R i) = Pi.single i 1 := by
  exact LinearEquiv.apply_symm_apply _ _

@[simp] theorem criticalZeroLinearEquiv_generator :
    criticalZeroLinearEquiv R
      (criticalZeroGenerator R (p:=p) (q:=q) (r:=r)) = 1 := by
  exact LinearEquiv.apply_symm_apply _ _

/-- A critical `2`-cell becomes the corresponding coordinate basis vector in
the strict minimal model. -/
@[simp] theorem criticalMinimalIso_generator_two (i : TopCycleIndex p q r) :
    (criticalMinimalIso R (p:=p) (q:=q) (r:=r)).hom.f 2
      (criticalTwoGenerator R i) = Pi.single i 1 := by
  change criticalTwoLinearEquiv R
    (criticalTwoGenerator R i) = Pi.single i 1
  exact criticalTwoLinearEquiv_generator R i

/-- The unique critical `0`-cell becomes `1 : R` in the strict minimal model. -/
@[simp] theorem criticalMinimalIso_generator_zero :
    (criticalMinimalIso R (p:=p) (q:=q) (r:=r)).hom.f 0
      (criticalZeroGenerator R (p:=p) (q:=q) (r:=r)) = (1 : R) := by
  change criticalZeroLinearEquiv R
    (criticalZeroGenerator R) = (1 : R)
  exact criticalZeroLinearEquiv_generator R

lemma topHomologyInclusion_single (i : TopCycleIndex p q r) :
    topHomologyInclusion R (Pi.single i 1) = topCycleVecR R i := by
  unfold topHomologyInclusion
  change (((topSynthesisR R) (Pi.single i 1) :
    TopKernel R) : GenericTriangle p q r → R) = topCycleVecR R i
  have h : topSynthesisR R (Pi.single i 1) = topCycleR R i := by
    unfold topSynthesisR
    rw [Fintype.linearCombination_apply_single]
    simp
  exact congrArg Subtype.val h

/-- Generator-level synthesis: the inverse homotopy equivalence sends the
critical `2`-cell indexed by `i` to its eight-triangle octahedral cycle. -/
@[simp] theorem sourceCritical_inv_generator_two (i : TopCycleIndex p q r) :
    (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).inv.f 2
      (criticalTwoGenerator R i) = topCycleVecR R i := by
  rw [sourceCritical_inv_two, criticalTwoLinearEquiv_generator]
  exact topHomologyInclusion_single R i

/-- Generator-level synthesis in degree zero: the unique critical vertex maps
to the chosen root representative of `H₀`. -/
@[simp] theorem sourceCritical_inv_generator_zero :
    (sourceCriticalHomotopyEquiv R (p:=p) (q:=q) (r:=r)).inv.f 0
      (criticalZeroGenerator R (p:=p) (q:=q) (r:=r)) =
        zeroHomologyInclusion R (1:R) := by
  rw [sourceCritical_inv_zero, criticalZeroLinearEquiv_generator]

end D0.Topology.GenericTripartiteMorseComplex
