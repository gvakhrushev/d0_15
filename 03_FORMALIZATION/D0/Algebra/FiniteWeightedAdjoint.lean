import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic
import D0.Algebra.FiniteCoordinateBasis
import D0.Algebra.FiniteHermitianAdjoint

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

/-- The defining adjoint identity, valid for every finite linear operator and
every nowhere-zero diagonal weight profile. -/
theorem finiteWeightedPairing_adjoint (w : ι → K) (hw : ∀ i, w i ≠ 0)
    (A : (ι → K) →ₗ[K] (ι → K)) (x y : ι → K) :
    finiteWeightedPairing w (A x) y =
      finiteWeightedPairing w x (finiteWeightedAdjoint w A y) := by
  have hAx : A x = ∑ i, x i • A (Pi.single i (1 : K)) := by
    calc
      A x = A (∑ i, x i • Pi.single i (1 : K)) :=
        congrArg A (finiteCoordinate_eq_sum_single x)
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

section Pairing

variable {ι K : Type*} [Fintype ι] [Field K]

/-- The diagonal bilinear pairing is symmetric, independently of the signs of
its weights. -/
theorem finiteWeightedPairing_symm (w : ι → K) (x y : ι → K) :
    finiteWeightedPairing w x y = finiteWeightedPairing w y x := by
  unfold finiteWeightedPairing
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- Additivity of the diagonal pairing in its left argument. -/
theorem finiteWeightedPairing_add_left (w : ι → K) (x y z : ι → K) :
    finiteWeightedPairing w (x + y) z =
      finiteWeightedPairing w x z + finiteWeightedPairing w y z := by
  simp only [finiteWeightedPairing, Pi.add_apply]
  calc
    (∑ i, w i * (x i + y i) * z i) =
        ∑ i, (w i * x i * z i + w i * y i * z i) := by
          apply Finset.sum_congr rfl
          intro i hi
          ring
    _ = (∑ i, w i * x i * z i) + ∑ i, w i * y i * z i :=
      Finset.sum_add_distrib

/-- Additivity of the diagonal pairing in its right argument. -/
theorem finiteWeightedPairing_add_right (w : ι → K) (x y z : ι → K) :
    finiteWeightedPairing w x (y + z) =
      finiteWeightedPairing w x y + finiteWeightedPairing w x z := by
  simp only [finiteWeightedPairing, Pi.add_apply]
  calc
    (∑ i, w i * x i * (y i + z i)) =
        ∑ i, (w i * x i * y i + w i * x i * z i) := by
          apply Finset.sum_congr rfl
          intro i hi
          ring
    _ = (∑ i, w i * x i * y i) + ∑ i, w i * x i * z i :=
      Finset.sum_add_distrib

end Pairing

section PositivePairing

variable {ι : Type*} [Fintype ι]

/-- A pointwise-positive diagonal profile makes the finite weighted pairing
positive definite. This is a conditional algebraic inner-product statement;
it does not choose or derive a profile. -/
theorem finiteWeightedPairing_pos_def (w x : ι → ℝ)
    (hw : ∀ i, 0 < w i) (hx : x ≠ 0) :
    0 < finiteWeightedPairing w x x := by
  classical
  obtain ⟨i, hxi⟩ := Function.ne_iff.mp hx
  have hnonneg (j : ι) : 0 ≤ w j * x j * x j := by
    convert mul_nonneg (le_of_lt (hw j)) (sq_nonneg (x j)) using 1
    ring
  have hpositive : 0 < w i * x i * x i := by
    convert mul_pos (hw i) (sq_pos_of_ne_zero hxi) using 1
    ring
  unfold finiteWeightedPairing
  exact Finset.sum_pos' (fun j _ => hnonneg j)
    ⟨i, Finset.mem_univ i, hpositive⟩

end PositivePairing

section PositiveWeightConjugation

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Coordinate multiplication by the square root of a supplied positive
diagonal profile. This is an algebraic change of Hilbert-space coordinates;
it does not derive or select the profile. -/
noncomputable def finiteWeightSquareRoot (w : ι → ℝ) :
    (ι → ℝ) →ₗ[ℝ] (ι → ℝ) where
  toFun x i := Real.sqrt (w i) * x i
  map_add' x y := by
    funext i
    simp only [Pi.add_apply]
    ring
  map_smul' c x := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

/-- The inverse coordinate scaling for a positive diagonal profile. -/
noncomputable def finiteWeightInvSquareRoot (w : ι → ℝ) :
    (ι → ℝ) →ₗ[ℝ] (ι → ℝ) where
  toFun x i := (Real.sqrt (w i))⁻¹ * x i
  map_add' x y := by
    funext i
    simp only [Pi.add_apply]
    ring
  map_smul' c x := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

omit [Fintype ι] [DecidableEq ι] in
private theorem finiteWeightSquareRoot_inv_apply (w x : ι → ℝ)
    (hw : ∀ i, 0 < w i) :
    finiteWeightSquareRoot w (finiteWeightInvSquareRoot w x) = x := by
  funext i
  have hroot : Real.sqrt (w i) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mpr (hw i))
  change Real.sqrt (w i) * ((Real.sqrt (w i))⁻¹ * x i) = x i
  field_simp [hroot]

omit [DecidableEq ι] in
/-- The weighted real pairing is the standard finite Hermitian pairing after
the positive square-root coordinate change. -/
theorem finiteHermitianPairing_weightSquareRoot (w x y : ι → ℝ)
    (hw : ∀ i, 0 < w i) :
    finiteHermitianPairing (finiteWeightSquareRoot w x)
        (finiteWeightSquareRoot w y) =
      finiteWeightedPairing w x y := by
  unfold finiteHermitianPairing finiteWeightedPairing
  apply Finset.sum_congr rfl
  intro i hi
  have hsq : Real.sqrt (w i) * Real.sqrt (w i) = w i := by
    simpa [pow_two] using (Real.sq_sqrt (le_of_lt (hw i)))
  simp only [finiteWeightSquareRoot, LinearMap.coe_mk, AddHom.coe_mk,
    star_trivial]
  calc
    (Real.sqrt (w i) * x i) * (Real.sqrt (w i) * y i) =
        (Real.sqrt (w i) * Real.sqrt (w i)) * x i * y i := by ring
    _ = w i * x i * y i := by rw [hsq]

/-- Conjugate a weighted operator into the standard finite Hilbert-space
coordinates using the caller's positive diagonal profile. -/
noncomputable def finiteWeightedConjugate (w : ι → ℝ)
    (A : (ι → ℝ) →ₗ[ℝ] (ι → ℝ)) :
    (ι → ℝ) →ₗ[ℝ] (ι → ℝ) :=
  (finiteWeightSquareRoot w).comp
    (A.comp (finiteWeightInvSquareRoot w))

/-- If a real operator is self-adjoint for a caller-supplied positive
diagonal pairing, its square-root conjugate is self-adjoint for the standard
finite Hermitian pairing. This proves the algebraic representative only; it
does not construct a geometric weight or select one physically. -/
theorem finiteWeightedConjugate_self_adjoint (w : ι → ℝ)
    (hw : ∀ i, 0 < w i) (A : (ι → ℝ) →ₗ[ℝ] (ι → ℝ))
    (hA : ∀ x y, finiteWeightedPairing w (A x) y =
      finiteWeightedPairing w x (A y)) :
    finiteHermitianAdjoint (finiteWeightedConjugate w A) =
      finiteWeightedConjugate w A := by
  apply finiteHermitianAdjoint_unique
  intro x y
  change finiteHermitianPairing
      (finiteWeightSquareRoot w (A (finiteWeightInvSquareRoot w x))) y =
    finiteHermitianPairing x
      (finiteWeightSquareRoot w (A (finiteWeightInvSquareRoot w y)))
  calc
    finiteHermitianPairing
        (finiteWeightSquareRoot w (A (finiteWeightInvSquareRoot w x))) y =
      finiteHermitianPairing
        (finiteWeightSquareRoot w (A (finiteWeightInvSquareRoot w x)))
        (finiteWeightSquareRoot w (finiteWeightInvSquareRoot w y)) := by
          rw [finiteWeightSquareRoot_inv_apply w y hw]
    _ = finiteWeightedPairing w
        (A (finiteWeightInvSquareRoot w x))
        (finiteWeightInvSquareRoot w y) :=
          finiteHermitianPairing_weightSquareRoot w _ _ hw
    _ = finiteWeightedPairing w
        (finiteWeightInvSquareRoot w x)
        (A (finiteWeightInvSquareRoot w y)) :=
          hA _ _
    _ = finiteHermitianPairing
        (finiteWeightSquareRoot w (finiteWeightInvSquareRoot w x))
        (finiteWeightSquareRoot w
          (A (finiteWeightInvSquareRoot w y))) :=
          (finiteHermitianPairing_weightSquareRoot w _ _ hw).symm
    _ = finiteHermitianPairing x
        (finiteWeightSquareRoot w (A (finiteWeightInvSquareRoot w y))) := by
          rw [finiteWeightSquareRoot_inv_apply w x hw]

end PositiveWeightConjugation

section

variable {ι K : Type*} [Fintype ι] [DecidableEq ι] [Field K]

/-- The adjoint identity in its equivalent right-operator form. -/
theorem finiteWeightedPairing_adjoint_right (w : ι → K) (hw : ∀ i, w i ≠ 0)
    (A : (ι → K) →ₗ[K] (ι → K)) (x y : ι → K) :
    finiteWeightedPairing w (finiteWeightedAdjoint w A x) y =
      finiteWeightedPairing w x (A y) := by
  calc
    finiteWeightedPairing w (finiteWeightedAdjoint w A x) y =
        finiteWeightedPairing w y (finiteWeightedAdjoint w A x) :=
      finiteWeightedPairing_symm w _ _
    _ = finiteWeightedPairing w (A y) x :=
      (finiteWeightedPairing_adjoint w hw A y x).symm
    _ = finiteWeightedPairing w x (A y) := finiteWeightedPairing_symm w _ _

/-- The adjoint of the zero operator is zero. -/
theorem finiteWeightedAdjoint_zero (w : ι → K) :
    finiteWeightedAdjoint w (0 : (ι → K) →ₗ[K] (ι → K)) = 0 := by
  ext x i
  simp [finiteWeightedAdjoint]

/-- Nilpotency transfers to the weighted adjoint by reversing composition. -/
theorem finiteWeightedAdjoint_comp_self_eq_zero (w : ι → K)
    (hw : ∀ i, w i ≠ 0) (A : (ι → K) →ₗ[K] (ι → K))
    (hA : A.comp A = 0) :
    (finiteWeightedAdjoint w A).comp (finiteWeightedAdjoint w A) = 0 := by
  calc
    (finiteWeightedAdjoint w A).comp (finiteWeightedAdjoint w A) =
        finiteWeightedAdjoint w (A.comp A) :=
      (finiteWeightedAdjoint_comp w hw A A).symm
    _ = finiteWeightedAdjoint w 0 := by rw [hA]
    _ = 0 := finiteWeightedAdjoint_zero w

/-- A function is supported in one grade when all coordinates of other grades
vanish. -/
def finiteDegreeSupported (degree : ι → ℕ) (k : ℕ) (x : ι → K) : Prop :=
  ∀ i, degree i ≠ k → x i = 0

/-- The weighted adjoint of a degree-raising operator lowers degree. The
conclusion is stated without subtraction: its value at coordinate `i` can be
nonzero only when `degree i + 1 = k`. -/
theorem finiteWeightedAdjoint_degree_lower (w : ι → K) (hw : ∀ i, w i ≠ 0)
    (A : (ι → K) →ₗ[K] (ι → K)) (degree : ι → ℕ)
    (hA : ∀ k x, finiteDegreeSupported degree k x →
      finiteDegreeSupported degree (k + 1) (A x))
    (k : ℕ) (x : ι → K) (hx : finiteDegreeSupported degree k x)
    (i : ι) (hik : degree i + 1 ≠ k) :
    finiteWeightedAdjoint w A x i = 0 := by
  have hei : finiteDegreeSupported degree (degree i) (Pi.single i (1 : K)) := by
    intro j hj
    by_cases hji : j = i
    · subst j
      exact (hj rfl).elim
    · simp [Pi.single, hji]
  have hAei := hA (degree i) (Pi.single i (1 : K)) hei
  have hleft :
      finiteWeightedPairing w (A (Pi.single i (1 : K))) x = 0 := by
    unfold finiteWeightedPairing
    apply Finset.sum_eq_zero
    intro j hj
    by_cases hdeg : degree j = degree i + 1
    · have hjk : degree j ≠ k := by
        intro heq
        exact hik (hdeg.symm.trans heq)
      simp [hx j hjk]
    · simp [hAei j hdeg]
  have hpair := finiteWeightedPairing_adjoint w hw A (Pi.single i (1 : K)) x
  rw [finiteWeightedPairing_single_left] at hpair
  rw [hleft] at hpair
  have hzero : w i * finiteWeightedAdjoint w A x i = 0 := hpair.symm
  exact (mul_eq_zero.mp hzero).resolve_left (hw i)

/-- The finite weighted Hodge-Dirac symmetrization `A + A†_w`. -/
noncomputable def finiteWeightedHodgeDirac (w : ι → K)
    (A : (ι → K) →ₗ[K] (ι → K)) : (ι → K) →ₗ[K] (ι → K) :=
  A + finiteWeightedAdjoint w A

/-- `A + A†_w` is self-adjoint for the supplied symmetric diagonal pairing
whenever every weight is nonzero. -/
theorem finiteWeightedHodgeDirac_pairing_self_adjoint
    (w : ι → K) (hw : ∀ i, w i ≠ 0) (A : (ι → K) →ₗ[K] (ι → K))
    (x y : ι → K) :
    finiteWeightedPairing w (finiteWeightedHodgeDirac w A x) y =
      finiteWeightedPairing w x (finiteWeightedHodgeDirac w A y) := by
  unfold finiteWeightedHodgeDirac
  calc
    finiteWeightedPairing w (A x + finiteWeightedAdjoint w A x) y =
        finiteWeightedPairing w (A x) y +
          finiteWeightedPairing w (finiteWeightedAdjoint w A x) y := by
            rw [finiteWeightedPairing_add_left]
    _ = finiteWeightedPairing w x (finiteWeightedAdjoint w A y) +
          finiteWeightedPairing w x (A y) := by
            rw [finiteWeightedPairing_adjoint w hw A x y,
              finiteWeightedPairing_adjoint_right w hw A x y]
    _ = finiteWeightedPairing w x (A y + finiteWeightedAdjoint w A y) := by
            rw [finiteWeightedPairing_add_right]
            ring

/-- If `A² = 0`, then the square of `A + A†_w` is the Hodge
anticommutator `A A†_w + A†_w A`. -/
theorem finiteWeightedHodgeDirac_square
    (w : ι → K) (hw : ∀ i, w i ≠ 0) (A : (ι → K) →ₗ[K] (ι → K))
    (hA : A.comp A = 0) :
    (finiteWeightedHodgeDirac w A).comp (finiteWeightedHodgeDirac w A) =
      A.comp (finiteWeightedAdjoint w A) +
        (finiteWeightedAdjoint w A).comp A := by
  have hAdj := finiteWeightedAdjoint_comp_self_eq_zero w hw A hA
  apply LinearMap.ext
  intro x
  change
    A (A x + finiteWeightedAdjoint w A x) +
        finiteWeightedAdjoint w A (A x + finiteWeightedAdjoint w A x) =
      A (finiteWeightedAdjoint w A x) +
        finiteWeightedAdjoint w A (A x)
  rw [map_add, map_add]
  have hA0 : A (A x) = 0 := by
    have h := congrArg (fun f : (ι → K) →ₗ[K] (ι → K) => f x) hA
    simpa [LinearMap.comp_apply] using h
  have hAdj0 : finiteWeightedAdjoint w A (finiteWeightedAdjoint w A x) = 0 := by
    have h := congrArg (fun f : (ι → K) →ₗ[K] (ι → K) => f x) hAdj
    simpa [LinearMap.comp_apply] using h
  rw [hA0, hAdj0]
  ext i
  abel

/-- The Hodge square preserves every finite grading when `A` raises degree by
one and is nilpotent of order two. No positivity of the diagonal weights is
needed; only nondegeneracy is used to define the adjoint. -/
theorem finiteWeightedHodgeDirac_square_preserves_degree
    (w : ι → K) (hw : ∀ i, w i ≠ 0) (A : (ι → K) →ₗ[K] (ι → K))
    (degree : ι → ℕ)
    (hA : ∀ k x, finiteDegreeSupported degree k x →
      finiteDegreeSupported degree (k + 1) (A x))
    (hA2 : A.comp A = 0) (k : ℕ) (x : ι → K)
    (hx : finiteDegreeSupported degree k x) :
    finiteDegreeSupported degree k
      (finiteWeightedHodgeDirac w A (finiteWeightedHodgeDirac w A x)) := by
  let adj := finiteWeightedAdjoint w A
  have hadjLower (q : ℕ) (y : ι → K)
      (hy : finiteDegreeSupported degree q y) :
      finiteDegreeSupported degree (q - 1) (adj y) := by
    intro i hi
    apply finiteWeightedAdjoint_degree_lower w hw A degree hA q y hy i
    omega
  have hadjZero (y : ι → K) (hy : finiteDegreeSupported degree 0 y) :
      adj y = 0 := by
    funext i
    apply finiteWeightedAdjoint_degree_lower w hw A degree hA 0 y hy i
    omega
  have hAadj : finiteDegreeSupported degree k (A (adj x)) := by
    cases k with
    | zero => simp [finiteDegreeSupported, hadjZero x hx]
    | succ k => exact hA k (adj x) (hadjLower (k + 1) x hx)
  have hadjA : finiteDegreeSupported degree k (adj (A x)) :=
    hadjLower (k + 1) (A x) (hA k x hx)
  have hcross : finiteDegreeSupported degree k (A (adj x) + adj (A x)) := by
    intro i hi
    simp only [Pi.add_apply]
    rw [hAadj i hi, hadjA i hi]
    simp
  have hsquare := finiteWeightedHodgeDirac_square w hw A hA2
  have hvalue :
      finiteWeightedHodgeDirac w A (finiteWeightedHodgeDirac w A x) =
        A (adj x) + adj (A x) := by
    have h := congrArg (fun f : (ι → K) →ₗ[K] (ι → K) => f x) hsquare
    simpa [adj, finiteWeightedHodgeDirac, LinearMap.comp_apply,
      LinearMap.add_apply] using h
  rw [hvalue]
  exact hcross

section UnitRealProfile

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

omit [DecidableEq ι] in
/-- With the real unit profile, the weighted bilinear pairing is exactly the
standard finite Hermitian pairing specialized to `ℝ`, whose star is trivial.
This is a compatibility boundary only; it says nothing about nonconstant
profiles or physical metric selection. -/
theorem finiteWeightedPairing_one_eq_finiteHermitianPairing
    (x y : ι → ℝ) :
    finiteWeightedPairing (fun _ : ι => (1 : ℝ)) x y =
      finiteHermitianPairing x y := by
  simp [finiteWeightedPairing, finiteHermitianPairing, star_trivial]

/-- The unit-profile real weighted adjoint is the specialization of the
generic Hermitian adjoint. The arbitrary-field, arbitrary-nonzero-weight
theorems above remain independent and strictly more general in their own
bilinear setting. -/
theorem finiteWeightedAdjoint_one_eq_finiteHermitianAdjoint
    (A : (ι → ℝ) →ₗ[ℝ] (ι → ℝ)) :
    finiteWeightedAdjoint (fun _ : ι => (1 : ℝ)) A =
      finiteHermitianAdjoint A := by
  apply finiteWeightedAdjoint_unique (fun _ : ι => (1 : ℝ))
    (by intro i; norm_num) A
  intro x y
  rw [finiteWeightedPairing_one_eq_finiteHermitianPairing]
  rw [finiteWeightedPairing_one_eq_finiteHermitianPairing]
  exact finiteHermitianPairing_adjoint A x y

end UnitRealProfile

end

end D0.Algebra
