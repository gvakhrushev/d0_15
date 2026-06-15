/-
D0.Matter.HiggsScalarProjectorConstructive
Constructive finite Higgs scalar-projector closure, now with LOAD-BEARING proofs (Iter-18).

The frozen doublet block is C^2 (here over ℚ for decidability). The frozen SU(2) generators are the
Pauli X and Z. A scalar projector P must (i) commute with X and Z (gauge compatibility), and (ii) be
idempotent. We prove, over concrete 2×2 matrices:

  * commutes_XZ_forces_scalar_matrix : [P,X]=[P,Z]=0  ⇒  P is scalar (off-diagonals 0, equal diagonal);
  * nonzero_gauge_idempotent_eq_identity : a scalar idempotent that is nonzero is the identity I₂;
  * rank1_scalar_projector_breaks_su2_gauge_compatibility : the rank-1 projector diag(1,0) does NOT
    commute with X (so rank-1 is gauge-incompatible);
  * rank2_scalar_projector_exists : I₂ commutes with X and Z, is idempotent, and has trace 2 (rank 2);
  * minimal_positive_scalar_projector_rank_two : a nonzero gauge-compatible idempotent has trace 2;
  * minimal_positive_scalar_projector_unique : it is unique — it must equal I₂;
  * higgs_yukawa_core_promotion_valid : the forced projector is I₂, whose trace is the rank 2 and which
    introduces no second scale (a single idempotent, not a new anchor).

These replace the previous `: True := by trivial` token stubs; the Python cert
vp_higgs_scalar_projector_constructive.py is the numeric companion.
-/
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

namespace D0.Matter

/-- The frozen doublet block: 2×2 matrices over ℚ. -/
abbrev M2 := Matrix (Fin 2) (Fin 2) ℚ

/-- Frozen SU(2) generator X (Pauli-X) on the doublet. -/
def FrozenSU2_X : M2 := !![0, 1; 1, 0]

/-- Frozen SU(2) generator Z (Pauli-Z) on the doublet. -/
def FrozenSU2_Z : M2 := !![1, 0; 0, -1]

/-- Additive commutator of two doublet operators. -/
def comm (A B : M2) : M2 := A * B - B * A

/-- IntertwinesFrozenSU2 P : P commutes with both frozen SU(2) generators. -/
def IntertwinesFrozenSU2 (P : M2) : Prop := comm P FrozenSU2_X = 0 ∧ comm P FrozenSU2_Z = 0

/-- A doublet projector: idempotent operator. -/
def IsProjector (P : M2) : Prop := P * P = P

/-- commutes_XZ_forces_scalar_matrix: a doublet operator in the commutant of the frozen SU(2)
generators is scalar — off-diagonals vanish and the diagonal entries are equal. -/
theorem commutes_XZ_forces_scalar_matrix (P : M2) (h : IntertwinesFrozenSU2 P) :
    P 0 1 = 0 ∧ P 1 0 = 0 ∧ P 0 0 = P 1 1 := by
  obtain ⟨hX, hZ⟩ := h
  have z01 := congrFun (congrFun hZ 0) 1
  have z10 := congrFun (congrFun hZ 1) 0
  have x01 := congrFun (congrFun hX 0) 1
  simp only [comm, FrozenSU2_X, FrozenSU2_Z, Matrix.sub_apply, Matrix.mul_apply, Fin.sum_univ_two,
    Matrix.zero_apply, Matrix.of_apply, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
    Matrix.head_fin_const, Matrix.cons_val', Matrix.empty_val', Matrix.cons_val_fin_one,
    mul_zero, zero_mul, mul_one, one_mul, mul_neg, neg_mul, sub_zero, zero_sub, add_zero, zero_add,
    neg_zero] at z01 z10 x01
  refine ⟨by linarith, by linarith, by linarith⟩

/-- nonzero_gauge_idempotent_eq_identity: a scalar idempotent (P = a·I₂ form, captured by the
commutant + idempotent constraints) that is nonzero equals the identity I₂. -/
theorem nonzero_gauge_idempotent_eq_identity (P : M2)
    (hc : IntertwinesFrozenSU2 P) (hp : IsProjector P) (hne : P ≠ 0) : P = 1 := by
  obtain ⟨h01, h10, hdiag⟩ := commutes_XZ_forces_scalar_matrix P hc
  -- idempotence at (0,0): (P*P) 0 0 = P 0 0, with off-diagonals zero ⇒ (P 0 0)² = P 0 0
  have hp' : P * P = P := hp
  have e00 := congrFun (congrFun hp' 0) 0
  simp only [Matrix.mul_apply, Fin.sum_univ_two, h01, h10, mul_zero, zero_mul, add_zero,
    zero_add] at e00
  have hfac : P 0 0 * (P 0 0 - 1) = 0 := by linear_combination e00
  rcases mul_eq_zero.mp hfac with h0 | h1
  · exfalso; apply hne
    have h11 : P 1 1 = 0 := by rw [← hdiag]; exact h0
    ext i j; fin_cases i <;> fin_cases j <;> simp_all [Matrix.zero_apply]
  · have ha : P 0 0 = 1 := by linarith
    have h11 : P 1 1 = 1 := by rw [← hdiag]; exact ha
    ext i j; fin_cases i <;> fin_cases j <;> simp_all [Matrix.one_apply]

/-- rank1_scalar_projector_breaks_su2_gauge_compatibility: the rank-1 diagonal projector diag(1,0)
is idempotent but does NOT commute with the frozen generator X — rank-1 is gauge-incompatible. -/
theorem rank1_scalar_projector_breaks_su2_gauge_compatibility :
    IsProjector (!![1, 0; 0, 0] : M2) ∧ ¬ IntertwinesFrozenSU2 (!![1, 0; 0, 0] : M2) := by
  constructor
  · show (!![1, 0; 0, 0] : M2) * !![1, 0; 0, 0] = !![1, 0; 0, 0]
    ext i j; fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two]
  · intro h
    have := (commutes_XZ_forces_scalar_matrix _ h).2.2
    simp at this

/-- rank2_scalar_projector_exists: the identity I₂ commutes with X and Z, is idempotent, and has
trace 2 (it is the rank-2 doublet projector). -/
theorem rank2_scalar_projector_exists :
    IntertwinesFrozenSU2 (1 : M2) ∧ IsProjector (1 : M2) ∧ Matrix.trace (1 : M2) = 2 := by
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · simp [comm]
  · simp [comm]
  · simp [IsProjector]
  · rw [Matrix.trace_fin_two]; norm_num [Matrix.one_apply]

/-- minimal_positive_scalar_projector_rank_two: a nonzero gauge-compatible idempotent has trace 2. -/
theorem minimal_positive_scalar_projector_rank_two (P : M2)
    (hc : IntertwinesFrozenSU2 P) (hp : IsProjector P) (hne : P ≠ 0) :
    Matrix.trace P = 2 := by
  have : P = 1 := nonzero_gauge_idempotent_eq_identity P hc hp hne
  rw [this, Matrix.trace_fin_two]; norm_num [Matrix.one_apply]

/-- minimal_positive_scalar_projector_unique: the nonzero gauge-compatible idempotent is unique. -/
theorem minimal_positive_scalar_projector_unique (P Q : M2)
    (hcP : IntertwinesFrozenSU2 P) (hpP : IsProjector P) (hneP : P ≠ 0)
    (hcQ : IntertwinesFrozenSU2 Q) (hpQ : IsProjector Q) (hneQ : Q ≠ 0) :
    P = Q := by
  rw [nonzero_gauge_idempotent_eq_identity P hcP hpP hneP,
      nonzero_gauge_idempotent_eq_identity Q hcQ hpQ hneQ]

/-- higgs_yukawa_core_promotion_valid: the forced projector is I₂; its trace is the rank 2 and it is
a single idempotent (it introduces no second scale anchor — the single-action-section is preserved). -/
theorem higgs_yukawa_core_promotion_valid (P : M2)
    (hc : IntertwinesFrozenSU2 P) (hp : IsProjector P) (hne : P ≠ 0) :
    P = 1 ∧ Matrix.trace P = 2 ∧ P * P = P := by
  have hP1 : P = 1 := nonzero_gauge_idempotent_eq_identity P hc hp hne
  exact ⟨hP1, by rw [hP1, Matrix.trace_fin_two]; norm_num [Matrix.one_apply], hp⟩

end D0.Matter
