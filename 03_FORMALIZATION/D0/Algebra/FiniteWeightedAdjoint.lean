import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic

/-!
# Finite weighted adjoints

For a finite coordinate space over a field, a diagonal nondegenerate bilinear
form has a canonical adjoint for every linear operator. No positivity is
assumed: this is an algebraic result and also applies to signed (Krein-type)
weights. It does not choose a metric or a physical inner product.
-/

namespace D0.Algebra

open Finset

section

variable {ι K : Type*} [Fintype ι] [DecidableEq ι] [Field K]

/-- The diagonal bilinear form with coordinate weights `w`. -/
def finiteWeightedPairing (w : ι → K) (x y : ι → K) : K :=
  ∑ i, w i * x i * y i

/-- The coordinate formula for the weighted transpose. Its adjoint identity
requires the diagonal weights to be nonzero; no positivity is asserted. -/
def finiteWeightedAdjoint (w : ι → K)
    (A : (ι → K) →ₗ[K] (ι → K)) : (ι → K) →ₗ[K] (ι → K) where
  toFun y i := (w i)⁻¹ * ∑ j, w j * A (Pi.single i 1) j * y j
  map_add' y z := by
    funext i
    simp only [Pi.add_apply, Finset.sum_add_distrib, mul_add]
  map_smul' c y := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    ring

private theorem pi_eq_sum_single (x : ι → K) :
    x = ∑ i, x i • Pi.single i (1 : K) := by
  funext j
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  rw [Finset.sum_eq_single j]
  · simp
  · intro i hi hij
    simp [hij]
  · simp

/-- The defining adjoint identity, valid for every finite linear operator and
every nowhere-zero diagonal weight profile. -/
theorem finiteWeightedPairing_adjoint (w : ι → K) (hw : ∀ i, w i ≠ 0)
    (A : (ι → K) →ₗ[K] (ι → K)) (x y : ι → K) :
    finiteWeightedPairing w (A x) y =
      finiteWeightedPairing w x (finiteWeightedAdjoint w A y) := by
  have hAx : A x = ∑ i, x i • A (Pi.single i (1 : K)) := by
    calc
      A x = A (∑ i, x i • Pi.single i (1 : K)) :=
        congrArg A (pi_eq_sum_single x)
      _ = ∑ i, x i • A (Pi.single i (1 : K)) := by simp
  have hAx_apply (j : ι) :
      A x j = ∑ i, x i * A (Pi.single i (1 : K)) j := by
    rw [hAx]
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  change (∑ j, w j * A x j * y j) =
    ∑ i, w i * x i *
      ((w i)⁻¹ * ∑ j, w j * A (Pi.single i 1) j * y j)
  simp_rw [hAx_apply]
  calc
    (∑ j, w j * (∑ i, x i * A (Pi.single i 1) j) * y j) =
        ∑ i, x i * (∑ j, w j * A (Pi.single i 1) j * y j) := by
      calc
        (∑ j, w j * (∑ i, x i * A (Pi.single i 1) j) * y j) =
            ∑ j, ∑ i, x i * (w j * A (Pi.single i 1) j * y j) := by
          apply Finset.sum_congr rfl
          intro j hj
          simp [Finset.mul_sum, mul_left_comm, mul_comm]
        _ = ∑ i, ∑ j, x i * (w j * A (Pi.single i 1) j * y j) :=
          Finset.sum_comm
        _ = ∑ i, x i * (∑ j, w j * A (Pi.single i 1) j * y j) := by
          apply Finset.sum_congr rfl
          intro i hi
          simp [Finset.mul_sum, mul_assoc]
    _ = ∑ i, w i * x i *
          ((w i)⁻¹ * ∑ j, w j * A (Pi.single i 1) j * y j) := by
      apply Finset.sum_congr rfl
      intro i hi
      have hwi := hw i
      field_simp [hwi]

private theorem finiteWeightedPairing_single_left (w : ι → K) (i : ι)
    (z : ι → K) :
    finiteWeightedPairing w (Pi.single i (1 : K)) z = w i * z i := by
  classical
  simp only [finiteWeightedPairing]
  rw [Finset.sum_eq_single i]
  · simp
  · intro j hj hji
    simp [hji]
  · intro hi
    exact (hi (Finset.mem_univ i)).elim

/-- The adjoint identity uniquely determines its right-hand operator when the
diagonal pairing is nondegenerate. -/
theorem finiteWeightedAdjoint_unique (w : ι → K) (hw : ∀ i, w i ≠ 0)
    (A B : (ι → K) →ₗ[K] (ι → K))
    (hB : ∀ x y, finiteWeightedPairing w (A x) y =
      finiteWeightedPairing w x (B y)) :
    finiteWeightedAdjoint w A = B := by
  apply LinearMap.ext
  intro y
  funext i
  have hAdj := finiteWeightedPairing_adjoint w hw A (Pi.single i 1) y
  have hB' := hB (Pi.single i 1) y
  have hPair := hAdj.symm.trans hB'
  have hCoord : (finiteWeightedAdjoint w A y) i = (B y) i := by
    rw [finiteWeightedPairing_single_left] at hPair
    rw [finiteWeightedPairing_single_left] at hPair
    simpa [hw i] using hPair
  exact hCoord

/-- The adjoint of a composite is the composite of the adjoints in reverse
order. -/
theorem finiteWeightedAdjoint_comp (w : ι → K) (hw : ∀ i, w i ≠ 0)
    (A B : (ι → K) →ₗ[K] (ι → K)) :
    finiteWeightedAdjoint w (A.comp B) =
      (finiteWeightedAdjoint w B).comp (finiteWeightedAdjoint w A) := by
  apply finiteWeightedAdjoint_unique w hw (A.comp B)
  intro x y
  change finiteWeightedPairing w (A (B x)) y =
    finiteWeightedPairing w x
      (finiteWeightedAdjoint w B (finiteWeightedAdjoint w A y))
  calc
    finiteWeightedPairing w (A (B x)) y =
        finiteWeightedPairing w (B x) (finiteWeightedAdjoint w A y) :=
      finiteWeightedPairing_adjoint w hw A (B x) y
    _ = finiteWeightedPairing w x
        (finiteWeightedAdjoint w B (finiteWeightedAdjoint w A y)) :=
      finiteWeightedPairing_adjoint w hw B x (finiteWeightedAdjoint w A y)

end

end D0.Algebra
