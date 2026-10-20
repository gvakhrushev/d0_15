import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Complex.BigOperators
import Mathlib.LinearAlgebra.Complex.Module
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# Real span of a fixed Hermitian source triple

For Hermitian matrices of one fixed size, `Tr(S M) = 0` for every admissible
traceless source-neutral `S` if and only if `M` lies in the real span of
`{I, J₁, J₂, J₃}`.

`J₁, J₂, J₃` are data. In the memorandum they are the sources `B_r`, not a
new operator and not a CAR representation. The index `n` is fixed for the
whole statement. The scalar field of the span is `ℝ`: a complex coefficient
is not a membership witness.

The pairing is the real part of the trace. On Hermitian arguments that real
part is the trace itself. Linear independence of the four matrices is not
assumed, so a degenerate triple still has the same equivalence. A single
vector identity `M χ = λ χ + ∑ β_r J_r χ` is strictly weaker and is not the
statement proved here.

No field kernel, curvature equation, or physical operator is constructed.
-/

namespace D0.Research.MemoryTangentSpan

open Matrix Complex Finset
open scoped Matrix

set_option linter.unusedSectionVars false

noncomputable section

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Real vector space of Hermitian matrices of the fixed index `n`. -/
abbrev Herm (n : Type*) [Fintype n] [DecidableEq n] :=
  selfAdjoint (Matrix n n ℂ)

/-- The ordered quadruple `(I, J₁, J₂, J₃)`. -/
def sourceMatrix (J1 J2 J3 : Matrix n n ℂ) : Fin 4 → Matrix n n ℂ
  | 0 => 1
  | 1 => J1
  | 2 => J2
  | 3 => J3

/-- `M` lies in `span_ℝ {I, J₁, J₂, J₃}`. -/
def MemRealSpan (J1 J2 J3 M : Matrix n n ℂ) : Prop :=
  ∃ c : Fin 4 → ℝ, M = ∑ i, c i • sourceMatrix J1 J2 J3 i

/-- Admissible traceless source-neutral test matrix.

`S` is Hermitian, `Tr S = 0`, and `Tr(S J_r) = 0` for each of the three
fixed matrices. -/
structure IsAdmissibleTangent (J1 J2 J3 S : Matrix n n ℂ) : Prop where
  hermitian : S.IsHermitian
  trace_zero : S.trace = 0
  neutral₁ : (S * J1).trace = 0
  neutral₂ : (S * J2).trace = 0
  neutral₃ : (S * J3).trace = 0

lemma sourceMatrix_hermitian {J1 J2 J3 : Matrix n n ℂ}
    (h1 : J1.IsHermitian) (h2 : J2.IsHermitian) (h3 : J3.IsHermitian) (i : Fin 4) :
    (sourceMatrix J1 J2 J3 i).IsHermitian := by
  fin_cases i
  · simp [sourceMatrix]
  · simp [sourceMatrix, h1]
  · simp [sourceMatrix, h2]
  · simp [sourceMatrix, h3]

lemma real_smul_eq_coe (c : ℝ) (A : Matrix n n ℂ) : c • A = (c : ℂ) • A := by
  ext i j
  simp [smul_apply, real_smul]

lemma real_smul_hermitian {A : Matrix n n ℂ} (hA : A.IsHermitian) (c : ℝ) :
    (c • A).IsHermitian := by
  rw [real_smul_eq_coe]
  exact hA.smul <| by
    rw [IsSelfAdjoint, star_def, conj_ofReal]

lemma memRealSpan_iff_coeffs (J1 J2 J3 M : Matrix n n ℂ) :
    MemRealSpan J1 J2 J3 M ↔
      ∃ a b c d : ℝ, M = a • (1 : Matrix n n ℂ) + b • J1 + c • J2 + d • J3 := by
  constructor
  · rintro ⟨coeff, hM⟩
    refine ⟨coeff 0, coeff 1, coeff 2, coeff 3, ?_⟩
    rw [hM, Fin.sum_univ_four]
    simp [sourceMatrix]
  · rintro ⟨a, b, c, d, hM⟩
    refine ⟨![a, b, c, d], ?_⟩
    rw [hM, Fin.sum_univ_four]
    simp [sourceMatrix, Matrix.cons_val_zero, add_assoc]

lemma memRealSpan_isHermitian {J1 J2 J3 M : Matrix n n ℂ}
    (h1 : J1.IsHermitian) (h2 : J2.IsHermitian) (h3 : J3.IsHermitian)
    (hM : MemRealSpan J1 J2 J3 M) : M.IsHermitian := by
  rcases hM with ⟨coeff, rfl⟩
  rw [Fin.sum_univ_four]
  simp only [sourceMatrix]
  exact (((real_smul_hermitian isHermitian_one (coeff 0)).add
    (real_smul_hermitian h1 (coeff 1))).add
    (real_smul_hermitian h2 (coeff 2))).add
    (real_smul_hermitian h3 (coeff 3))

/-- `Tr(S J)` is real when both matrices are Hermitian. -/
lemma trace_mul_isSelfAdjoint {S J : Matrix n n ℂ}
    (hS : S.IsHermitian) (hJ : J.IsHermitian) :
    star ((S * J).trace) = (S * J).trace := by
  rw [← trace_conjTranspose, conjTranspose_mul, hS.eq, hJ.eq, trace_mul_comm]

lemma trace_mul_eq_ofReal_re {S J : Matrix n n ℂ}
    (hS : S.IsHermitian) (hJ : J.IsHermitian) :
    (S * J).trace = (((S * J).trace).re : ℂ) := by
  have hstar := trace_mul_isSelfAdjoint hS hJ
  rw [star_def] at hstar
  exact (conj_eq_iff_re.mp hstar).symm

lemma trace_mul_re_eq_zero_iff {S J : Matrix n n ℂ}
    (hS : S.IsHermitian) (hJ : J.IsHermitian) :
    ((S * J).trace).re = 0 ↔ (S * J).trace = 0 := by
  rw [trace_mul_eq_ofReal_re hS hJ]
  simp

lemma trace_mul_self_eq_sum_normSq {A : Matrix n n ℂ} (hA : A.IsHermitian) :
    (A * A).trace = ∑ i, ∑ j, (normSq (A i j) : ℂ) := by
  simp_rw [trace, diag_apply, mul_apply]
  refine sum_congr rfl fun i _ => sum_congr rfl fun j _ => ?_
  have hji : A j i = star (A i j) := (hA.apply j i).symm
  rw [hji, star_def, mul_conj]

/-- The real Frobenius form is positive definite on Hermitian matrices. -/
lemma hermitian_mul_self_trace_eq_zero_iff {A : Matrix n n ℂ} (hA : A.IsHermitian) :
    (A * A).trace = 0 ↔ A = 0 := by
  rw [trace_mul_self_eq_sum_normSq hA]
  constructor
  · intro h
    have hcast :
        (∑ i, ∑ j, (normSq (A i j) : ℂ)) =
          ((∑ i, ∑ j, normSq (A i j) : ℝ) : ℂ) := by
      simp_rw [← ofReal_sum]
    rw [hcast] at h
    have hsum : ∑ i, ∑ j, normSq (A i j) = 0 := ofReal_eq_zero.mp h
    ext i j
    have houter : ∑ j, normSq (A i j) = 0 :=
      (sum_eq_zero_iff_of_nonneg fun _ _ =>
        sum_nonneg fun _ _ => normSq_nonneg _).mp hsum i (mem_univ _)
    have hij : normSq (A i j) = 0 :=
      (sum_eq_zero_iff_of_nonneg fun _ _ => normSq_nonneg _).mp houter j (mem_univ _)
    exact normSq_eq_zero.mp hij
  · rintro rfl
    simp

/-- Right multiplication by a fixed matrix, as an `ℝ`-linear map.
A handwritten `where` body panics in the Lean 4.30 code generator, so this is
`LinearMap.mulRight`. -/
abbrev mulRightRe (J : Matrix n n ℂ) : Matrix n n ℂ →ₗ[ℝ] Matrix n n ℂ :=
  LinearMap.mulRight ℝ J

/-- Inclusion of Hermitian matrices into all matrices. -/
def hermIncl : Herm n →ₗ[ℝ] Matrix n n ℂ where
  toFun S := S
  map_add' _ _ := by simp [AddSubgroup.coe_add]
  map_smul' _ _ := by simp [selfAdjoint.val_smul]

/-- Real trace pairing against a fixed matrix, restricted to Hermitian matrices. -/
def hermPairing (J : Matrix n n ℂ) : Herm n →ₗ[ℝ] ℝ :=
  reLm.comp ((traceLinearMap n ℝ ℂ).comp ((mulRightRe J).comp hermIncl))

@[simp]
lemma hermPairing_apply (J : Matrix n n ℂ) (S : Herm n) :
    hermPairing J S = (((S : Matrix n n ℂ) * J).trace).re := by
  simp [hermPairing, mulRightRe, hermIncl, traceLinearMap, reLm_coe]

lemma pairing_smul_sum (S : Matrix n n ℂ) (c : Fin 4 → ℝ) (v : Fin 4 → Matrix n n ℂ) :
    (S * ∑ i, c i • v i).trace.re = ∑ i, c i * (S * v i).trace.re := by
  rw [mul_sum]
  simp_rw [Matrix.mul_smul, trace_sum, trace_smul, re_sum]
  refine sum_congr rfl fun i _ => ?_
  simp

lemma trace_re_mul_sub (S A B : Matrix n n ℂ) :
    (S * (A - B)).trace.re = (S * A).trace.re - (S * B).trace.re := by
  rw [Matrix.mul_sub, trace_sub, sub_re]

lemma admissible_source_trace {J1 J2 J3 S : Matrix n n ℂ}
    (hS : IsAdmissibleTangent J1 J2 J3 S) (i : Fin 4) :
    (S * sourceMatrix J1 J2 J3 i).trace = 0 := by
  fin_cases i
  · simpa [sourceMatrix, mul_one] using hS.trace_zero
  · simpa [sourceMatrix] using hS.neutral₁
  · simpa [sourceMatrix] using hS.neutral₂
  · simpa [sourceMatrix] using hS.neutral₃

/-- A real combination is orthogonal to every admissible test matrix. -/
theorem admissible_trace_vanishes_of_memRealSpan
    {J1 J2 J3 M S : Matrix n n ℂ}
    (hM : MemRealSpan J1 J2 J3 M) (hS : IsAdmissibleTangent J1 J2 J3 S) :
    (S * M).trace = 0 := by
  rcases hM with ⟨c, rfl⟩
  rw [mul_sum, trace_sum]
  refine sum_eq_zero fun i _ => ?_
  rw [Matrix.mul_smul, trace_smul, admissible_source_trace hS i, smul_zero]

/-- Vanishing against every admissible test matrix forces the real span. -/
theorem memRealSpan_of_admissible_trace_vanishes
    {J1 J2 J3 M : Matrix n n ℂ}
    (h1 : J1.IsHermitian) (h2 : J2.IsHermitian) (h3 : J3.IsHermitian)
    (hM : M.IsHermitian)
    (hvanish : ∀ S, IsAdmissibleTangent J1 J2 J3 S → (S * M).trace = 0) :
    MemRealSpan J1 J2 J3 M := by
  let L : Fin 4 → Herm n →ₗ[ℝ] ℝ := fun i => hermPairing (sourceMatrix J1 J2 J3 i)
  let K : Herm n →ₗ[ℝ] ℝ := hermPairing M
  have hker : ⨅ i, LinearMap.ker (L i) ≤ LinearMap.ker K := by
    intro S hS
    rw [LinearMap.mem_ker]
    have hzero : ∀ i, ((S : Matrix n n ℂ) * sourceMatrix J1 J2 J3 i).trace = 0 := by
      intro i
      have hmem : S ∈ LinearMap.ker (L i) :=
        (Submodule.mem_iInf fun i => LinearMap.ker (L i)).mp hS i
      rw [LinearMap.mem_ker] at hmem
      have hre : (((S : Matrix n n ℂ) * sourceMatrix J1 J2 J3 i).trace).re = 0 := by
        simpa [L, hermPairing_apply] using hmem
      exact (trace_mul_re_eq_zero_iff (Matrix.isHermitian_iff_isSelfAdjoint.mpr S.prop)
        (sourceMatrix_hermitian h1 h2 h3 i)).mp hre
    have hadm : IsAdmissibleTangent J1 J2 J3 (S : Matrix n n ℂ) := by
      refine ⟨Matrix.isHermitian_iff_isSelfAdjoint.mpr S.prop, ?_, ?_, ?_, ?_⟩
      · simpa [sourceMatrix, mul_one] using hzero 0
      · simpa [sourceMatrix] using hzero 1
      · simpa [sourceMatrix] using hzero 2
      · simpa [sourceMatrix] using hzero 3
    have htr : ((S : Matrix n n ℂ) * M).trace = 0 := hvanish _ hadm
    simpa [K, hermPairing_apply] using
      (trace_mul_re_eq_zero_iff (Matrix.isHermitian_iff_isSelfAdjoint.mpr S.prop) hM).mpr htr
  have hspan : K ∈ Submodule.span ℝ (Set.range L) := mem_span_of_iInf_ker_le_ker hker
  obtain ⟨c, hc⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).mp hspan
  let combo : Matrix n n ℂ := ∑ i, c i • sourceMatrix J1 J2 J3 i
  have hcombo : combo.IsHermitian :=
    memRealSpan_isHermitian h1 h2 h3 ⟨c, rfl⟩
  let Rmat : Matrix n n ℂ := M - combo
  have hR : Rmat.IsHermitian := hM.sub hcombo
  have hcoeff : ∀ S : Herm n,
      (((S : Matrix n n ℂ) * M).trace).re =
        ∑ i, c i * (((S : Matrix n n ℂ) * sourceMatrix J1 J2 J3 i).trace).re := by
    intro S
    have happly := (LinearMap.congr_fun hc S).symm
    simpa [L, K, hermPairing_apply, LinearMap.sum_apply, LinearMap.smul_apply, smul_eq_mul] using
      happly
  have hRpair : ∀ S : Herm n, (((S : Matrix n n ℂ) * Rmat).trace).re = 0 := by
    intro S
    have hcomboPair :
        (((S : Matrix n n ℂ) * combo).trace).re =
          ∑ i, c i * (((S : Matrix n n ℂ) * sourceMatrix J1 J2 J3 i).trace).re := by
      simpa [combo] using pairing_smul_sum (S : Matrix n n ℂ) c (sourceMatrix J1 J2 J3)
    rw [trace_re_mul_sub, hcoeff S, hcomboPair, sub_self]
  have hself : ((Rmat * Rmat).trace).re = 0 := by
    simpa using hRpair ⟨Rmat, Matrix.isHermitian_iff_isSelfAdjoint.mp hR⟩
  have hzero : (Rmat * Rmat).trace = 0 := (trace_mul_re_eq_zero_iff hR hR).mp hself
  have hR0 : Rmat = 0 := (hermitian_mul_self_trace_eq_zero_iff hR).mp hzero
  refine ⟨c, ?_⟩
  have hdiff : M - combo = 0 := by simpa [Rmat] using hR0
  simpa [combo, sub_eq_zero] using hdiff

/-- Traceless source-neutral orthogonality is real span membership. -/
theorem trace_vanishes_iff_memRealSpan
    {J1 J2 J3 M : Matrix n n ℂ}
    (h1 : J1.IsHermitian) (h2 : J2.IsHermitian) (h3 : J3.IsHermitian)
    (hM : M.IsHermitian) :
    (∀ S, IsAdmissibleTangent J1 J2 J3 S → (S * M).trace = 0) ↔
      MemRealSpan J1 J2 J3 M := by
  constructor
  · exact memRealSpan_of_admissible_trace_vanishes h1 h2 h3 hM
  · intro hspan S hS
    exact admissible_trace_vanishes_of_memRealSpan hspan hS

/-! ### Finite controls

The matrices below are coordinates. They are not field operators. -/

/-- Pauli `X` on two coordinates. -/
def pauliX : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

/-- Pauli `Z` on two coordinates. -/
def pauliZ : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- Traceless diagonal shift `diag(1/2, -1/2)`. -/
def halfShift : Matrix (Fin 2) (Fin 2) ℂ := !![(1 / 2 : ℂ), 0; 0, -(1 / 2 : ℂ)]

/-- The first basis vector. -/
def chi2 : Fin 2 → ℂ := ![1, 0]

lemma pauliX_hermitian : pauliX.IsHermitian := by
  refine IsHermitian.ext fun i j => ?_
  fin_cases i <;> fin_cases j <;>
    simp [pauliX]

lemma pauliZ_hermitian : pauliZ.IsHermitian := by
  refine IsHermitian.ext fun i j => ?_
  fin_cases i <;> fin_cases j <;>
    simp [pauliZ]

lemma halfShift_hermitian : halfShift.IsHermitian := by
  refine IsHermitian.ext fun i j => ?_
  fin_cases i <;> fin_cases j <;>
    simp [halfShift]

lemma pauliX_mul_self : pauliX * pauliX = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [pauliX, mul_apply, Fin.sum_univ_two]

lemma pauliZ_mul_pauliX :
    pauliZ * pauliX = !![0, 1; -1, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [pauliZ, pauliX, mul_apply, Fin.sum_univ_two]

lemma halfShift_mul_self :
    halfShift * halfShift = !![(1 / 4 : ℂ), 0; 0, (1 / 4 : ℂ)] := by
  ext i j
  fin_cases i <;> fin_cases j
  · simp [halfShift, mul_apply, Fin.sum_univ_two]; norm_num
  · simp [halfShift, mul_apply, Fin.sum_univ_two]
  · simp [halfShift, mul_apply, Fin.sum_univ_two]
  · simp [halfShift, mul_apply, Fin.sum_univ_two]; norm_num

lemma pauliZ_trace_zero : pauliZ.trace = 0 := by
  simp [trace_fin_two, pauliZ]

lemma halfShift_trace_zero : halfShift.trace = 0 := by
  simp [trace_fin_two, halfShift]

lemma pauliZ_pauliX_trace_zero : (pauliZ * pauliX).trace = 0 := by
  rw [pauliZ_mul_pauliX]
  simp [trace_fin_two]

/-- `Z` is admissible for the source triple `(X, 0, 0)`. -/
theorem pauliZ_isAdmissibleTangent : IsAdmissibleTangent pauliX 0 0 pauliZ where
  hermitian := pauliZ_hermitian
  trace_zero := pauliZ_trace_zero
  neutral₁ := pauliZ_pauliX_trace_zero
  neutral₂ := by simp
  neutral₃ := by simp

/-- `I + X` lies in `span_ℝ {I, X, 0, 0}`. -/
theorem eye_add_pauliX_memRealSpan : MemRealSpan pauliX 0 0 (1 + pauliX) := by
  rw [memRealSpan_iff_coeffs]
  refine ⟨1, 1, 0, 0, ?_⟩
  simp [one_smul, add_zero]

/-- Positive control: the admissible direction `Z` kills `I + X`. -/
theorem pauliZ_kills_eye_add_pauliX : (pauliZ * (1 + pauliX)).trace = 0 :=
  admissible_trace_vanishes_of_memRealSpan eye_add_pauliX_memRealSpan pauliZ_isAdmissibleTangent

/-- Traceless is not source-neutral: `X` pairs with itself by `2`. -/
theorem pauliX_self_trace_ne_zero : (pauliX * pauliX).trace ≠ 0 := by
  rw [pauliX_mul_self, trace_one]
  norm_num

theorem pauliX_not_admissible_to_itself : ¬ IsAdmissibleTangent pauliX 0 0 pauliX := by
  intro h
  have hzero : (pauliX * pauliX).trace = 0 := h.neutral₁
  exact pauliX_self_trace_ne_zero hzero

theorem halfShift_isAdmissibleTangent : IsAdmissibleTangent 0 0 0 halfShift where
  hermitian := halfShift_hermitian
  trace_zero := halfShift_trace_zero
  neutral₁ := by simp
  neutral₂ := by simp
  neutral₃ := by simp

theorem halfShift_self_trace_ne_zero : (halfShift * halfShift).trace ≠ 0 := by
  rw [halfShift_mul_self, trace_fin_two]
  norm_num

/-- Negative control: admissible against the zero triple, but not orthogonal to itself. -/
theorem halfShift_trace_test_fails :
    ¬ ∀ S, IsAdmissibleTangent (0 : Matrix (Fin 2) (Fin 2) ℂ) 0 0 S → (S * halfShift).trace = 0 := by
  intro h
  have hzero := h halfShift halfShift_isAdmissibleTangent
  exact halfShift_self_trace_ne_zero hzero

theorem halfShift_not_memRealSpan :
    ¬ MemRealSpan (0 : Matrix (Fin 2) (Fin 2) ℂ) 0 0 halfShift :=
  (trace_vanishes_iff_memRealSpan isHermitian_zero isHermitian_zero isHermitian_zero
      halfShift_hermitian).not.mp halfShift_trace_test_fails

/-- The ray test holds for `halfShift` on `χ = (1, 0)` and the zero sources. -/
theorem halfShift_mulVec_chi :
    halfShift.mulVec chi2 = (1 / 2 : ℝ) • chi2 := by
  ext i
  fin_cases i <;> simp [halfShift, chi2, mulVec, dotProduct, Fin.sum_univ_two, real_smul]

/-- The single-vector condition does not imply the real span. -/
theorem ray_member_not_memRealSpan :
    (∃ lambda beta1 beta2 beta3 : ℝ,
      halfShift.mulVec chi2 =
        lambda • chi2 +
          beta1 • ((0 : Matrix (Fin 2) (Fin 2) ℂ).mulVec chi2) +
          beta2 • ((0 : Matrix (Fin 2) (Fin 2) ℂ).mulVec chi2) +
          beta3 • ((0 : Matrix (Fin 2) (Fin 2) ℂ).mulVec chi2)) ∧
      ¬ MemRealSpan (0 : Matrix (Fin 2) (Fin 2) ℂ) 0 0 halfShift := by
  refine ⟨⟨1 / 2, 0, 0, 0, ?_⟩, halfShift_not_memRealSpan⟩
  simp [halfShift_mulVec_chi, zero_mulVec, add_zero]

#print axioms trace_vanishes_iff_memRealSpan
#print axioms admissible_trace_vanishes_of_memRealSpan
#print axioms memRealSpan_of_admissible_trace_vanishes
#print axioms pauliZ_isAdmissibleTangent
#print axioms eye_add_pauliX_memRealSpan
#print axioms pauliZ_kills_eye_add_pauliX
#print axioms pauliX_not_admissible_to_itself
#print axioms halfShift_trace_test_fails
#print axioms halfShift_not_memRealSpan
#print axioms halfShift_mulVec_chi
#print axioms ray_member_not_memRealSpan

end

end D0.Research.MemoryTangentSpan
