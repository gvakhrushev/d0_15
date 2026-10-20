import D0.Geometry.ArchiveAffineExteriorLink
import Mathlib.Tactic
import Mathlib.Data.Real.StarOrdered

/-! Research matrix kernels for variable solder, compression and the actual
role-order sign conversion. The literal abstract-exterior/counting-adjoint
bridge and the warped-field realization are separate analytic arguments.
No modified codifferential, selected bootstrap heat or physical Ward is added. -/
namespace D0.Research.CurvedSolderedHeat
open Matrix D0 D0.Geometry
open scoped BigOperators

section FiniteMatrices
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
local notation "M" => Matrix ι ι ℝ

/-- The defect of the stored left-multiplied backward coefficient. -/
theorem coefficient_shift_adjoint_defect (C S : M) :
    (C*(S-1)).transpose-(-(C.transpose*(1-S.transpose)))=
      S.transpose*C.transpose-C.transpose*S.transpose := by
  simp only [Matrix.transpose_mul,Matrix.transpose_sub,Matrix.transpose_one]
  noncomm_ring

/-- Own-axis coefficient invariance is represented by commuting with the shift. -/
theorem coefficient_shift_adjoint (C S : M) (hCS : C*S=S*C) :
    (C*(S-1)).transpose=-(C.transpose*(1-S.transpose)) := by
  have ht := congrArg Matrix.transpose hCS
  simp only [Matrix.transpose_mul] at ht
  apply sub_eq_zero.mp
  rw [coefficient_shift_adjoint_defect,ht,sub_self]

def shiftMatrix (s : Equiv.Perm ι) : M := fun i j => if j=s i then 1 else 0

/-- Exact finite own-axis condition for a scalar coefficient, with all sites kept. -/
theorem diagonal_shift_commutes_iff (s : Equiv.Perm ι) (a : ι → ℝ) :
    Matrix.diagonal a*shiftMatrix s=shiftMatrix s*Matrix.diagonal a ↔
      ∀ i, a (s i)=a i := by
  constructor
  · intro h i
    have hi := congrArg (fun X : M => X i (s i)) h
    simpa [Matrix.diagonal_mul,Matrix.mul_diagonal,shiftMatrix] using hi.symm
  · intro h
    ext i j
    simp only [Matrix.diagonal_mul,Matrix.mul_diagonal,shiftMatrix]
    by_cases hij : j=s i
    · subst j
      simp [h]
    · simp [hij]

/-- The nonconstant coefficient produces the mandatory commutator term. -/
theorem warped_two_factor_square (H0 H1 A : M)
    (hA : H1*A=A*H1) (h01 : H1*H0=-(H0*H1)) :
    (H0+A*H1)^2=H0^2+A^2*H1^2+(H0*A-A*H0)*H1 := by
  calc
    (H0+A*H1)^2=H0^2+A*(H1*A)*H1+(H0*A)*H1+A*(H1*H0) := by noncomm_ring
    _=H0^2+A*(A*H1)*H1+(H0*A)*H1+A*(-(H0*H1)) := by rw [hA,h01]
    _=_ := by noncomm_ring

/-- Spectator directions anticommute, but the time/warp commutator survives. -/
theorem warped_full_square (H0 H1 K A : M)
    (hA : H1*A=A*H1) (h01 : H1*H0=-(H0*H1))
    (hK0 : K*H0=-(H0*K)) (hK1 : K*H1=-(H1*K)) (hKA : K*A=A*K) :
    (H0+A*H1+K)^2=H0^2+A^2*H1^2+K^2+(H0*A-A*H0)*H1 := by
  have hK : K*(H0+A*H1)=-(H0+A*H1)*K := by
    calc
      K*(H0+A*H1)=K*H0+(K*A)*H1 := by noncomm_ring
      _=-(H0*K)+A*(K*H1) := by rw [hK0,hKA]; noncomm_ring
      _=-(H0*K)+A*(-(H1*K)) := by rw [hK1]
      _=_ := by noncomm_ring
  calc
    (H0+A*H1+K)^2=(H0+A*H1)^2+(H0+A*H1)*K+K*(H0+A*H1)+K^2 := by noncomm_ring
    _=(H0+A*H1)^2+K^2 := by rw [hK]; noncomm_ring
    _=_ := by rw [warped_two_factor_square H0 H1 A hA h01]; noncomm_ring

/-- Compression is not a spectral homomorphism: its second-order defect is
exactly the retained coupling to the complementary sector. -/
theorem projection_variance (P X : M) (hP : P.transpose=P) (hPP : P*P=P)
    (hX : X.transpose=X) :
    P*X^2*P-(P*X*P)^2=
      ((1-P)*X*P).transpose*((1-P)*X*P) := by
  have hc : (1-P)*(1-P)=1-P := by
    calc
      (1-P)*(1-P)=1-P-P+P*P := by noncomm_ring
      _=1-P := by rw [hPP]; abel
  have hA : (P*X*P)^2=P*X*P*X*P := by
    calc
      (P*X*P)^2=P*X*(P*P)*X*P := by noncomm_ring
      _=_ := by rw [hPP]
  rw [hA]
  simp only [Matrix.transpose_mul,Matrix.transpose_sub,Matrix.transpose_one,hP,hX]
  calc
    P*X^2*P-P*X*P*X*P=P*X*(1-P)*X*P := by noncomm_ring
    _=P*X*((1-P)*(1-P))*X*P := by rw [hc]
    _=_ := by noncomm_ring

set_option maxHeartbeats 800000 in
theorem projection_variance_posSemidef (P X : M) (hP : P.transpose=P) (hPP : P*P=P)
    (hX : X.transpose=X) : (P*X^2*P-(P*X*P)^2).PosSemidef := by
  rw [projection_variance P X hP hPP hX]
  simpa only [Matrix.conjTranspose_eq_transpose_of_trivial] using
    Matrix.posSemidef_conjTranspose_mul_self (R := ℝ) (m := ι) (n := ι) ((1-P)*X*P)

theorem projection_variance_trace (P X : M) (hP : P.transpose=P) (hPP : P*P=P)
    (hX : X.transpose=X) :
    Matrix.trace (P*X^2*P-(P*X*P)^2)=∑ i,∑ j, (((1-P)*X*P) j i)^2 := by
  rw [projection_variance P X hP hPP hX]
  have htrace (B : M) : Matrix.trace (B.transpose*B)=∑ i,∑ j,(B j i)^2 := by
    simp only [Matrix.trace,Matrix.diag,Matrix.mul_apply,Matrix.transpose_apply,pow_two]
  exact htrace ((1-P)*X*P)

theorem projection_variance_trace_nonnegative (P X : M)
    (hP : P.transpose=P) (hPP : P*P=P) (hX : X.transpose=X) :
    0≤Matrix.trace (P*X^2*P-(P*X*P)^2) := by
  rw [projection_variance_trace P X hP hPP hX]
  exact Finset.sum_nonneg (fun i _ => Finset.sum_nonneg (fun j _ => sq_nonneg _))

omit [DecidableEq ι] in
/-- Sign conjugation preserves adjointness in the whole retained carrier. -/
theorem sign_conjugacy_transpose (S X : M) (hS : S.transpose=S) :
    (S*X*S).transpose=S*X.transpose*S := by
  simp only [Matrix.transpose_mul,hS]
  simp only [Matrix.mul_assoc]

theorem sign_conjugacy_product (S X Y : M) (hSS : S*S=1) :
    (S*X*S)*(S*Y*S)=S*(X*Y)*S := by
  calc
    (S*X*S)*(S*Y*S)=S*X*(S*S)*Y*S := by noncomm_ring
    _=_ := by rw [hSS]; noncomm_ring

theorem sign_conjugacy_trace (S X : M) (hSS : S*S=1) :
    Matrix.trace (S*X*S)=Matrix.trace X := by
  rw [Matrix.trace_mul_cycle]
  rw [hSS,Matrix.one_mul]
end FiniteMatrices

/-- ABCD versus ACDB requires moving occupied B past occupied C and D. -/
def orderPhaseInt (s : ArchiveFockState) : ℤ :=
  (-1)^((s B).toNat*((s C).toNat+(s D).toNat))

/-- The only negative phases have occupied B and exactly one of C,D. -/
theorem orderPhaseInt_formula (s : ArchiveFockState) :
    orderPhaseInt s=(if s B=true ∧ s C≠s D then -1 else 1) := by
  cases hb : s B <;> cases hc : s C <;> cases hd : s D <;>
    norm_num [orderPhaseInt,hb,hc,hd]

theorem orderPhaseInt_square (s : ArchiveFockState) : orderPhaseInt s*orderPhaseInt s=1 := by
  cases hb : s B <;> cases hc : s C <;> cases hd : s D <;>
    norm_num [orderPhaseInt,hb,hc,hd]

/-- The actual two source definitions use different orders. -/
theorem actual_role_orders :
    (roleCode A,roleCode B,roleCode C,roleCode D)=(0,3,1,2) ∧
    (roleOrderIndex A,roleOrderIndex B,roleOrderIndex C,roleOrderIndex D)=(0,1,2,3) := by
  decide

/-- Integer Jordan--Wigner matrix in the code order used by the exterior basis. -/
def codeAnnihilateInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  if ket r=true ∧ bra r=false ∧ (∀ s : Role, s≠r → bra s=ket s) then
    if (Finset.univ.filter (fun s : Role => roleCode s<roleCode r ∧ ket s=true)).card % 2=0 then 1 else -1
  else 0

set_option maxRecDepth 200000 in
set_option maxHeartbeats 2000000 in
theorem actual_integer_order_conjugacy :
    ∀ r : Role,∀ bra ket : ArchiveFockState,
      codeAnnihilateInt r bra ket=
        orderPhaseInt bra*carAnnihilateInt r bra ket*orderPhaseInt ket := by
  decide

/-- The actual order phase is an orthogonal involution on all sixteen states. -/
def orderSignMatrix : Matrix ArchiveFockState ArchiveFockState ℝ :=
  Matrix.diagonal (fun s => (orderPhaseInt s : ℝ))

theorem actual_order_sign_involution :
    orderSignMatrix.transpose=orderSignMatrix ∧ orderSignMatrix*orderSignMatrix=1 := by
  constructor
  · simp [orderSignMatrix]
  unfold orderSignMatrix
  rw [Matrix.diagonal_mul_diagonal]
  have h (s : ArchiveFockState) : (orderPhaseInt s : ℝ)*(orderPhaseInt s : ℝ)=1 := by
    exact_mod_cast orderPhaseInt_square s
  simp_rw [h]
  exact Matrix.diagonal_one

/-- Type wrapper for the actual old matrix entries; no replacement operator. -/
def oldAnnihilateMatrix (r : Role) : Matrix ArchiveFockState ArchiveFockState ℝ :=
  carAnnihilate r

/-- Exact matrix conversion consumes the real old CAR owner. The additional
identification with the abstract exterior-basis operator is not claimed here. -/
theorem actual_real_order_conjugacy (r : Role) :
    ((fun bra ket => (codeAnnihilateInt r bra ket : ℝ)) : Matrix ArchiveFockState ArchiveFockState ℝ)=
      orderSignMatrix*oldAnnihilateMatrix r*orderSignMatrix := by
  ext bra ket
  simp only [orderSignMatrix,Matrix.mul_diagonal,Matrix.diagonal_mul,oldAnnihilateMatrix]
  rw [carAnnihilate_eq_intCast]
  exact_mod_cast actual_integer_order_conjugacy r bra ket

end D0.Research.CurvedSolderedHeat

#print D0.Geometry.roleCode
#print D0.Geometry.roleOrderIndex
#print D0.Geometry.archiveFockExteriorBasis
#print D0.Geometry.archiveExteriorCreator
#print D0.Geometry.archiveExteriorContraction
#check D0.Geometry.forward_backward_adjoint
#check D0.Geometry.createAction_adjoint
#check D0.Geometry.observer_contraction_adjoint_covariant
#print axioms D0.Research.CurvedSolderedHeat.coefficient_shift_adjoint_defect
#print axioms D0.Research.CurvedSolderedHeat.coefficient_shift_adjoint
#print axioms D0.Research.CurvedSolderedHeat.diagonal_shift_commutes_iff
#print axioms D0.Research.CurvedSolderedHeat.warped_two_factor_square
#print axioms D0.Research.CurvedSolderedHeat.warped_full_square
#print axioms D0.Research.CurvedSolderedHeat.projection_variance
#print axioms D0.Research.CurvedSolderedHeat.projection_variance_posSemidef
#print axioms D0.Research.CurvedSolderedHeat.projection_variance_trace
#print axioms D0.Research.CurvedSolderedHeat.projection_variance_trace_nonnegative
#print axioms D0.Research.CurvedSolderedHeat.sign_conjugacy_transpose
#print axioms D0.Research.CurvedSolderedHeat.sign_conjugacy_product
#print axioms D0.Research.CurvedSolderedHeat.sign_conjugacy_trace
#print axioms D0.Research.CurvedSolderedHeat.orderPhaseInt_formula
#print axioms D0.Research.CurvedSolderedHeat.orderPhaseInt_square
#print axioms D0.Research.CurvedSolderedHeat.actual_role_orders
#print axioms D0.Research.CurvedSolderedHeat.actual_integer_order_conjugacy
#print axioms D0.Research.CurvedSolderedHeat.actual_order_sign_involution
#print axioms D0.Research.CurvedSolderedHeat.actual_real_order_conjugacy
#print axioms D0.Geometry.forward_backward_adjoint
#print axioms D0.Geometry.createAction_adjoint
#print axioms D0.Geometry.observer_contraction_adjoint_covariant
