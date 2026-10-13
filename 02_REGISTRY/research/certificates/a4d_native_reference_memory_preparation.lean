import D0.Geometry.A4DObserverPositiveExterior
import D0.Representation.GoldenCoherentMemory
import D0.Representation.GoldenOrderInterferometer
import Mathlib.Tactic

/-!
Finite shared-reference kernels. Distinct histories, universal product
programs, endpoint-normalized apparatus frames and self-conditioned frames
are separate hypotheses. No native preparation, blank reset, indefinite
state norm, physical source, or all-history unitary is silently supplied.
-/
namespace D0.Research.ReferenceMemoryPreparation
noncomputable section
open Matrix
set_option linter.unusedSectionVars false

variable {ι ν κ : Type*} [Fintype ι] [Fintype ν] [Fintype κ]
  [DecidableEq ι] [DecidableEq ν] [DecidableEq κ]
local notation "M" => Matrix ι ι ℝ
local notation "Frame" => Matrix ν ι ℝ

/-- Equal-overlap Jones frames contain two orthogonal history coordinates.
This changes coordinates in the full frame span, not the history Gram. -/
theorem history_symmetric_frames (G F : Frame) (a p : ℝ)
    (hG : G.transpose*G=1) (hF : F.transpose*F=1)
    (hGF : G.transpose*F=(p^3) • (1 : M))
    (ha : a^2=p) (hp : p+p^2=1) (ha0 : a≠0) (hp0 : p≠0) :
    let E := (2*a)⁻¹ • (G+F)
    let H := (2*p)⁻¹ • (G-F)
    E.transpose*E=1 ∧ H.transpose*H=1 ∧ E.transpose*H=0 := by
  have hFG : F.transpose*G=(p^3) • (1 : M) := by
    simpa using congrArg Matrix.transpose hGF
  have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  have he : (2*a)⁻¹*(2*a)⁻¹*(2+2*p^3)=1 := by field_simp; nlinarith
  have hh : (2*p)⁻¹*(2*p)⁻¹*(2-2*p^3)=1 := by field_simp; nlinarith
  dsimp
  simp only [Matrix.transpose_add,Matrix.transpose_sub,
    Matrix.smul_mul,Matrix.mul_smul,Matrix.add_mul,Matrix.mul_add,
    Matrix.sub_mul,Matrix.mul_sub,hG,hF,hGF,hFG]
  constructor
  · calc
      _=((2*a)⁻¹*(2*a)⁻¹*(2+2*p^3)) • (1 : M) := by module
      _=1 := by rw [he]; simp
  constructor
  · calc
      _=((2*p)⁻¹*(2*p)⁻¹*(2-2*p^3)) • (1 : M) := by module
      _=1 := by rw [hh]; simp
  · module

theorem history_coordinates_recover (G F : Frame) (a p : ℝ)
    (ha : a≠0) (hp : p≠0) :
    a • ((2*a)⁻¹ • (G+F))+p • ((2*p)⁻¹ • (G-F))=G ∧
    a • ((2*a)⁻¹ • (G+F))-p • ((2*p)⁻¹ • (G-F))=F := by
  have ha' : a*(2*a)⁻¹=(1:ℝ)/2 := by field_simp
  have hp' : p*(2*p)⁻¹=(1:ℝ)/2 := by field_simp
  simp only [smul_smul,ha',hp']
  constructor <;> module

/-- One isometry preserves the complete cross-history Gram. -/
theorem common_isometry_preserves_overlap (G F : Frame) (V : Matrix κ ν ℝ)
    (hV : V.transpose*V=1) :
    (V*G).transpose*(V*F)=G.transpose*F := by
  simp only [Matrix.transpose_mul,Matrix.mul_assoc]
  rw [← Matrix.mul_assoc V.transpose V,hV,Matrix.one_mul]

theorem common_isometry_cannot_collapse (G F : Frame) (V : Matrix κ ν ℝ)
    (hV : V.transpose*V=1) (h : V*G=V*F) : G=F := by
  have ht := congrArg (fun X : Matrix κ ι ℝ => V.transpose*X) h
  simpa only [← Matrix.mul_assoc,hV,Matrix.one_mul] using ht

/-- Full data-space embedding with a product reference, with no chosen data
input. The program occupies the first tensor coordinate. -/
def productProgramFrame (r : κ → ℝ) : Matrix (κ × ι) ι ℝ :=
  fun k j => if k.2=j then r k.1 else 0

theorem product_program_cross_gram (r s : κ → ℝ) :
    (productProgramFrame (ι := ι) r).transpose*productProgramFrame s=
      (dotProduct r s) • (1 : M) := by
  ext i j
  by_cases h : i=j
  · subst j
    simp [productProgramFrame,Matrix.mul_apply,Fintype.sum_prod_type,dotProduct]
  · simp [productProgramFrame,Matrix.mul_apply,Fintype.sum_prod_type,dotProduct,h,Ne.symm h]

/-- Product-program Gram relation, independently of any tensor coordinate
convention. Input and output program Gram assumptions are explicit. -/
theorem universal_program_gram (P Q A B : Frame) (U V : M)
    (W : Matrix ν ν ℝ) (c d : ℝ)
    (hW : W.transpose*W=1) (hPQ : P.transpose*Q=c • (1 : M))
    (hAB : A.transpose*B=d • (1 : M)) (hP : W*P=A*U) (hQ : W*Q=B*V) :
    c • (1 : M)=d • (U.transpose*V) := by
  have h := common_isometry_preserves_overlap P Q W hW
  rw [hP,hQ,hPQ] at h
  calc
    c • (1 : M)=(A*U).transpose*(B*V) := h.symm
    _=U.transpose*(A.transpose*B)*V := by simp only [Matrix.transpose_mul,Matrix.mul_assoc]
    _=d • (U.transpose*V) := by rw [hAB]; simp

/-- If the requested relative operation is not scalar, both program overlaps
must vanish. This is a universal-input theorem, not a one-state collision rule. -/
theorem nonscalar_programs_orthogonal [Nonempty ι] (R : M) (c d : ℝ)
    (hnonscalar : ∀ t : ℝ, R≠t • (1 : M))
    (h : c • (1 : M)=d • R) : c=0 ∧ d=0 := by
  have hd : d=0 := by
    by_contra hd
    apply hnonscalar (d⁻¹*c)
    have ht := congrArg (fun X : M => d⁻¹ • X) h
    simpa only [smul_smul,inv_mul_cancel₀ hd,one_smul] using ht.symm
  have hzero : c • (1 : M)=0 := by simpa only [hd,zero_smul] using h
  obtain ⟨i⟩ := ‹Nonempty ι›
  have hc := congrArg (fun X : M => X i i) hzero
  exact ⟨by simpa using hc,hd⟩

/-- The literal two golden orientations already have a nonscalar relative
operation: its off-diagonal entry is 2ap. -/
theorem golden_relative_nonscalar (a p : ℝ) (ha : 0<a) (hp : 0<p) :
    ∀ t : ℝ,
      (D0.Representation.GoldenOrderInterferometer.gate a p).transpose *
        (D0.Representation.GoldenOrderInterferometer.gate a p).transpose ≠
          t • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  intro t heq
  have h := congrArg (fun X : Matrix (Fin 2) (Fin 2) ℝ => X 0 1) heq
  simp [D0.Representation.GoldenOrderInterferometer.gate,
    Matrix.mul_apply,Fin.sum_univ_two] at h
  nlinarith [mul_pos ha hp]

/-- The actual two-port primitives produce the same normalized output from
two distinct preparation histories; they are two different operations. -/
theorem owned_histories_shared_output (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (D0.Representation.GoldenOrderInterferometer.gate a p).transpose.mulVec ![a,p]=![1,0] ∧
    (D0.Representation.GoldenOrderInterferometer.gate a p).mulVec ![a,-p]=![1,0] := by
  constructor <;> ext i <;> fin_cases i <;>
    simp [D0.Representation.GoldenOrderInterferometer.gate,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two] <;> nlinarith

theorem owned_history_gram (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    dotProduct ![a,p] ![a,p]=1 ∧ dotProduct ![a,-p] ![a,-p]=1 ∧
      dotProduct ![a,p] ![a,-p]=p^3 := by
  have hc := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  simp [dotProduct,Fin.sum_univ_two]
  constructor <;> nlinarith

/-- Exact actual Role reflection. The invariant vector cannot lie in the
strict timelike sector; the statement says nothing against an invariant line. -/
def timeReflection (v : D0.Geometry.RoleVector) : D0.Geometry.RoleVector :=
  fun r => if r=D0.A then -v r else v r

theorem reflection_fixed_not_timelike (v : D0.Geometry.RoleVector)
    (h : timeReflection v=v) :
    ¬ 0 < ∑ r : D0.Role, D0.Geometry.roleLorentzSign r*v r^2 := by
  have hz := congrFun h D0.A
  simp [timeReflection] at hz
  have hA : v D0.A=0 := by linarith
  simp only [Fintype.sum_prod_type,Fin.sum_univ_two]
  norm_num [D0.Geometry.roleLorentzSign,D0.Geometry.roleRoleSigEquiv,
    D0.roleSign,D0.A,D0.B,D0.C,D0.D] at hA ⊢
  nlinarith [sq_nonneg (v D0.B),sq_nonneg (v D0.C),sq_nonneg (v D0.D)]

theorem reflection_fixed_not_unit_observer (v : D0.Geometry.RoleVector)
    (h : timeReflection v=v) : ¬ D0.Geometry.lorentzUnitObserver v := by
  intro hu
  have ht := reflection_fixed_not_timelike v h
  unfold D0.Geometry.lorentzUnitObserver at hu
  rw [hu] at ht
  norm_num at ht

def feedback (P V Vadj : M) : M := P*Vadj*(1-P)*V*P

/-- Complete endpoint feedback with the final endpoint cut. Changing the last
cut to the initial cut is a different experiment. -/
theorem endpoint_feedback_covariance (E0 C0 E1 C1 P V Vadj : M)
    (h0 : C0*E0=1) (h1 : C1*E1=1) :
    (E0*P*C0)*(E0*Vadj*C1)*(1-E1*P*C1)*(E1*V*C0)*(E0*P*C0)=
      E0*feedback P V Vadj*C0 := by
  unfold feedback
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.mul_assoc]
  simp only [← Matrix.mul_assoc C0 E0,h0,Matrix.one_mul,
    ← Matrix.mul_assoc C1 E1,h1]

/-- Endpoint-normalized frames give the actual weighted adjoint relation,
without dropping the final Gram from that adjoint. -/
theorem endpoint_adjoint_relation (E0 C0 E1 C1 U W0 W1 : M)
    (h0 : C0.transpose=W0*E0) (h1 : E1.transpose*W1=C1) :
    (E1*U*C0).transpose*W1=W0*(E0*U.transpose*C1) := by
  simp only [Matrix.transpose_mul,Matrix.mul_assoc]
  rw [h0]
  calc
    W0*E0*(U.transpose*(E1.transpose*W1))=W0*E0*(U.transpose*C1) := by rw [h1]
    _=_ := by simp only [Matrix.mul_assoc]

theorem endpoint_isometry (C0 E1 U W0 W1 : M)
    (h0 : C0.transpose*C0=W0) (h1 : E1.transpose*W1*E1=1)
    (hU : U.transpose*U=1) :
    (E1*U*C0).transpose*W1*(E1*U*C0)=W0 := by
  simp only [Matrix.transpose_mul,Matrix.mul_assoc] at *
  calc
    C0.transpose*(U.transpose*(E1.transpose*(W1*(E1*(U*C0)))))=
        C0.transpose*(U.transpose*((E1.transpose*(W1*E1))*(U*C0))) := by
      simp only [Matrix.mul_assoc]
    _=C0.transpose*C0 := by
      rw [h1,Matrix.one_mul,← Matrix.mul_assoc U.transpose U,hU,Matrix.one_mul]
    _=W0 := h0

def chronological (T : ℕ → M) : ℕ → M
  | 0 => 1
  | n+1 => T n*chronological T n

/-- Every intermediate frame cancels; no fresh blank or same-frame replacement
is inserted into the chronological product. -/
theorem endpoint_telescope (E C : ℕ → M) (U : M)
    (hCE : ∀ n, C n*E n=1) (hEC0 : E 0*C 0=1) (n : ℕ) :
    chronological (fun k => E (k+1)*U*C k) n=E n*U^n*C 0 := by
  induction n with
  | zero => simp [chronological,hEC0]
  | succ n ih =>
    rw [chronological,ih]
    calc
      (E (n+1)*U*C n)*(E n*U^n*C 0)=E (n+1)*U*(C n*E n)*U^n*C 0 := by noncomm_ring
      _=E (n+1)*U^(n+1)*C 0 := by rw [hCE n,Matrix.mul_one,pow_succ']; simp only [Matrix.mul_assoc]

/-- In the fixed parity chart a blank input cannot have both positive first
and top components after one literal block step. -/
theorem blank_endpoint_sign_conflict (a p x y z w : ℝ) (hx : x=z) (hy : y=w) :
    (p*x+a*y)+(-p*z-a*w)=0 ∧ ¬ (0<p*x+a*y ∧ 0< -p*z-a*w) := by
  constructor
  · rw [hx,hy]; ring
  · rw [hx,hy]
    intro h
    linarith [h.1,h.2]

theorem golden_root_gt_seventeen_twenty_eight (p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) : (17:ℝ)/28<p := by
  by_contra h
  have hb : p≤(17:ℝ)/28 := le_of_not_gt h
  have hm := mul_nonneg hp0.le (sub_nonneg.mpr hb)
  nlinarith

/-- Exact fifth-power identity of the owned golden R+ block. -/
theorem owned_golden_fifth_power (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (D0.Representation.GoldenOrderInterferometer.gate a p)^5+
      (28*p-17) • D0.Representation.GoldenOrderInterferometer.gate a p+
      (4*a*p^3) • (1 : Matrix (Fin 2) (Fin 2) ℝ)=0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pow_succ,D0.Representation.GoldenOrderInterferometer.gate,
      Matrix.mul_apply,Fin.sum_univ_two]
  · linear_combination (a^3-10*a*p^2+a*p)*ha+(5*a*p^2-11*a*p+17*a)*hp
  · linear_combination (-5*a^2*p+10*p^3-5*p^2)*ha+(-p^3+11*p^2-17*p)*hp
  · linear_combination (5*a^2*p-10*p^3+5*p^2)*ha+(p^3-11*p^2+17*p)*hp
  · linear_combination (a^3-10*a*p^2+a*p)*ha+(5*a*p^2-11*a*p+17*a)*hp

theorem positive_retained_coordinate_fails_by_fifth (a p y0 y1 y5 : ℝ)
    (ha : 0<a) (hp0 : 0<p) (hp : p+p^2=1)
    (h0 : 0<y0) (h1 : 0<y1)
    (hfive : y5+(28*p-17)*y1+4*a*p^3*y0=0) : y5<0 := by
  have hc : 0<28*p-17 := by
    have hh := golden_root_gt_seventeen_twenty_eight p hp hp0
    linarith
  have hleft := mul_pos hc h1
  have hright : 0<4*a*p^3*y0 := by positivity
  linarith

/-- Application to every coordinate of every initial vector for the actual
owned R+; no recurrence is supplied as an extra hypothesis. -/
theorem owned_positive_coordinate_fails_by_fifth (a p : ℝ) (v : Fin 2 → ℝ) (i : Fin 2)
    (ha2 : a^2=p) (ha : 0<a) (hp0 : 0<p) (hp : p+p^2=1)
    (h0 : 0<v i) (h1 : 0<(D0.Representation.GoldenOrderInterferometer.gate a p).mulVec v i) :
    ((D0.Representation.GoldenOrderInterferometer.gate a p)^5).mulVec v i<0 := by
  have h := congrArg (fun X : Matrix (Fin 2) (Fin 2) ℝ => X.mulVec v i)
    (owned_golden_fifth_power a p ha2 hp)
  simp only [Matrix.add_mulVec,Matrix.smul_mulVec,Pi.add_apply,Pi.smul_apply,
    smul_eq_mul,Matrix.one_mulVec,Matrix.zero_mulVec,Pi.zero_apply] at h
  exact positive_retained_coordinate_fails_by_fifth a p _ _ _ ha hp0 hp h0 h1 h

/-- The already owned delta is exactly the overlap of these normalized
histories; its square is the pure-history fidelity. This reuses the existing
cubic-overlap theorem rather than declaring new independent invariants. -/
theorem owned_history_delta_link (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    dotProduct ![a,p] ![a,-p]=2*D0.Representation.GoldenRelativeChannel.delta p ∧
    (dotProduct ![a,p] ![a,-p])^2=
      4*(D0.Representation.GoldenRelativeChannel.delta p)^2 := by
  have hh := (owned_history_gram a p ha hp).2.2
  have hd := D0.Representation.GoldenRelativeChannel.twice_delta p hp
  constructor
  · exact hh.trans hd.symm
  · rw [hh,← hd]; ring

/-- Applied to the actual gate's populations, the existing relative channel
preserves their unit mass and sends the initial contrast 2 delta to 4 delta².
This statement supplies no identification with a physical observer field. -/
theorem owned_population_contrast_delta_link (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    a^2-p^2=2*D0.Representation.GoldenRelativeChannel.delta p ∧
    (D0.Representation.GoldenRelativeChannel.kernel p |>.mulVec ![a^2,p^2]) 0 +
      (D0.Representation.GoldenRelativeChannel.kernel p |>.mulVec ![a^2,p^2]) 1=1 ∧
    (D0.Representation.GoldenRelativeChannel.kernel p |>.mulVec ![a^2,p^2]) 0 -
      (D0.Representation.GoldenRelativeChannel.kernel p |>.mulVec ![a^2,p^2]) 1=
        4*(D0.Representation.GoldenRelativeChannel.delta p)^2 := by
  have hc : a^2-p^2=2*D0.Representation.GoldenRelativeChannel.delta p := by
    unfold D0.Representation.GoldenRelativeChannel.delta
    rw [ha]
    ring
  have hm := D0.Representation.GoldenRelativeChannel.mass_and_contrast p (a^2) (p^2) hp
  refine ⟨hc,?_,?_⟩
  · rw [hm.1,ha,hp]
  · rw [hm.2,hc]; ring

/-- The old dimensional ladder has a Fibonacci recurrence for every scale
coefficient. Index k means its Q_(k+1), without natural subtraction. This
recurrence does not determine the dimension of physical spacetime. -/
theorem golden_quantum_fibonacci_recurrence (delta : ℝ) (k : ℕ) :
    2*delta*D0.phi^(k+2)=2*delta*D0.phi^(k+1)+2*delta*D0.phi^k := by
  rw [pow_add,pow_add,pow_one,D0.phi_sq]
  ring

end
end D0.Research.ReferenceMemoryPreparation

#print D0.Representation.GoldenOrderInterferometer.gate
#print D0.Representation.GoldenCoherentMemory.fullStep
#print D0.Geometry.lorentzUnitObserver
#print D0.Representation.GoldenOrderInterferometer.gate_orthogonal
#print D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
#print D0.Representation.GoldenCoherentMemory.blank_record_evolution
#check D0.Research.ReferenceMemoryPreparation.history_symmetric_frames
#check D0.Research.ReferenceMemoryPreparation.universal_program_gram
#check D0.Research.ReferenceMemoryPreparation.nonscalar_programs_orthogonal
#check D0.Research.ReferenceMemoryPreparation.reflection_fixed_not_timelike
#check D0.Research.ReferenceMemoryPreparation.endpoint_feedback_covariance
#check D0.Research.ReferenceMemoryPreparation.endpoint_telescope
#check D0.Research.ReferenceMemoryPreparation.owned_positive_coordinate_fails_by_fifth
#print axioms D0.Research.ReferenceMemoryPreparation.history_symmetric_frames
#print axioms D0.Research.ReferenceMemoryPreparation.history_coordinates_recover
#print axioms D0.Research.ReferenceMemoryPreparation.common_isometry_preserves_overlap
#print axioms D0.Research.ReferenceMemoryPreparation.common_isometry_cannot_collapse
#print axioms D0.Research.ReferenceMemoryPreparation.product_program_cross_gram
#print axioms D0.Research.ReferenceMemoryPreparation.universal_program_gram
#print axioms D0.Research.ReferenceMemoryPreparation.nonscalar_programs_orthogonal
#print axioms D0.Research.ReferenceMemoryPreparation.golden_relative_nonscalar
#print axioms D0.Research.ReferenceMemoryPreparation.owned_histories_shared_output
#print axioms D0.Research.ReferenceMemoryPreparation.owned_history_gram
#print axioms D0.Research.ReferenceMemoryPreparation.reflection_fixed_not_timelike
#print axioms D0.Research.ReferenceMemoryPreparation.reflection_fixed_not_unit_observer
#print axioms D0.Research.ReferenceMemoryPreparation.endpoint_feedback_covariance
#print axioms D0.Research.ReferenceMemoryPreparation.endpoint_adjoint_relation
#print axioms D0.Research.ReferenceMemoryPreparation.endpoint_isometry
#print axioms D0.Research.ReferenceMemoryPreparation.endpoint_telescope
#print axioms D0.Research.ReferenceMemoryPreparation.blank_endpoint_sign_conflict
#print axioms D0.Research.ReferenceMemoryPreparation.golden_root_gt_seventeen_twenty_eight
#print axioms D0.Research.ReferenceMemoryPreparation.owned_golden_fifth_power
#print axioms D0.Research.ReferenceMemoryPreparation.positive_retained_coordinate_fails_by_fifth
#print axioms D0.Research.ReferenceMemoryPreparation.owned_positive_coordinate_fails_by_fifth
#print axioms D0.Representation.GoldenOrderInterferometer.gate_orthogonal
#print axioms D0.Representation.GoldenOrderInterferometer.golden_cube
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
#print axioms D0.Representation.GoldenCoherentMemory.blank_record_evolution
#check D0.Research.ReferenceMemoryPreparation.owned_history_delta_link
#check D0.Research.ReferenceMemoryPreparation.owned_population_contrast_delta_link
#check D0.Research.ReferenceMemoryPreparation.golden_quantum_fibonacci_recurrence
#print axioms D0.Research.ReferenceMemoryPreparation.owned_history_delta_link
#print axioms D0.Research.ReferenceMemoryPreparation.owned_population_contrast_delta_link
#print axioms D0.Research.ReferenceMemoryPreparation.golden_quantum_fibonacci_recurrence
#print axioms D0.Representation.GoldenRelativeChannel.twice_delta
#print axioms D0.Representation.GoldenRelativeChannel.mass_and_contrast
#print axioms D0.phi_sq
