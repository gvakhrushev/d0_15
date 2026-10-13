import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.ArchiveWeightedHodgeDirac
import D0.Cosmology.FeedbackPartitionFunction
import Mathlib.Tactic

/-! Research kernels for the full finite real carrier with a supplied positive
Gram matrix. Inverse and first-jet data are explicit hypotheses. The analytic
log/heat derivative, tangent-path integration and native field binding are
separate results; no supported codifferential or selected action is changed.
The printed weighted-Hodge and feedback owners expose their actual propositions.
-/
namespace D0.Research.JointAdjointSource
open Matrix

section FiniteMatrices
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
local notation "M" => Matrix ι ι ℝ

def commutator (A B : M) : M := A*B-B*A
def weightedAdjoint (Gi G A : M) : M := Gi*A.transpose*G

/-- Nondegeneracy forces the supplied adjoint; no choice of an adjoint remains. -/
theorem weighted_adjoint_unique (G Gi d a : M) (hGiG : Gi*G=1)
    (ha : G*a=d.transpose*G) : a=weightedAdjoint Gi G d := by
  have h := congrArg (fun X : M => Gi*X) ha
  simpa only [← Matrix.mul_assoc,hGiG,Matrix.one_mul,weightedAdjoint] using h

/-- Product differentiation with dot(G inverse)=-G inverse dotG G inverse.
This is a genuine all-size first-jet identity, not a differentiability wrapper. -/
theorem weighted_adjoint_first_jet (G Gi H d E : M) (hGGi : G*Gi=1) :
    (-Gi*H*Gi)*d.transpose*G+Gi*E.transpose*G+Gi*d.transpose*H=
      weightedAdjoint Gi G E+
        commutator (weightedAdjoint Gi G d) (Gi*H) := by
  unfold weightedAdjoint commutator
  have h : Gi*d.transpose*G*(Gi*H)=Gi*d.transpose*H := by
    calc
      Gi*d.transpose*G*(Gi*H)=Gi*d.transpose*(G*Gi)*H := by noncomm_ring
      _=_ := by rw [hGGi]; simp
  rw [h]
  noncomm_ring

/-- The inverse-Gram jet itself satisfies the differentiated inverse equation. -/
theorem inverse_gram_first_jet (G Gi H : M) (hGGi : G*Gi=1) :
    G*(-Gi*H*Gi)+H*Gi=0 := by
  calc
    G*(-Gi*H*Gi)+H*Gi=-(G*Gi)*H*Gi+H*Gi := by noncomm_ring
    _=0 := by rw [hGGi]; simp

/-- Full moving-pairing covariance under one joint change of basis. -/
theorem weighted_adjoint_basis_covariance (G Gi d T Ti : M) (hTiT : Ti*T=1) :
    weightedAdjoint (T*Gi*T.transpose) (Ti.transpose*G*Ti) (T*d*Ti)=
      T*weightedAdjoint Gi G d*Ti := by
  have htrans : T.transpose*Ti.transpose=1 := by
    simpa only [Matrix.transpose_mul,Matrix.transpose_one] using congrArg Matrix.transpose hTiT
  unfold weightedAdjoint
  simp only [Matrix.transpose_mul]
  calc
    T*Gi*T.transpose*(Ti.transpose*(d.transpose*T.transpose))*(Ti.transpose*G*Ti)=
      T*Gi*(T.transpose*Ti.transpose)*d.transpose*(T.transpose*Ti.transpose)*G*Ti := by noncomm_ring
    _=_ := by rw [htrans]; simp only [Matrix.mul_one,Matrix.mul_assoc]

/-- Twice the metric-compatible jet avoids choosing a square-root frame.
This links the moving-Gram adjoint jet to the fixed-pairing tangent chart. -/
theorem weighted_adjoint_twice_balanced (G Gi K d E : M) (hGGi : G*Gi=1)
    (hK : weightedAdjoint Gi G K=K) :
    2*(weightedAdjoint Gi G E+commutator (weightedAdjoint Gi G d) K)+
        commutator K (weightedAdjoint Gi G d)=
      weightedAdjoint Gi G (2*E+commutator K d) := by
  have hprod (X Y : M) : weightedAdjoint Gi G (X*Y)=
      weightedAdjoint Gi G Y*weightedAdjoint Gi G X := by
    unfold weightedAdjoint
    simp only [Matrix.transpose_mul]
    calc
      Gi*(Y.transpose*X.transpose)*G=Gi*Y.transpose*(G*Gi)*X.transpose*G := by
        rw [hGGi]; noncomm_ring
      _=_ := by noncomm_ring
  have hlin : weightedAdjoint Gi G (2*E+commutator K d)=
      2*weightedAdjoint Gi G E+weightedAdjoint Gi G d*K-K*weightedAdjoint Gi G d := by
    calc
      weightedAdjoint Gi G (2*E+commutator K d)=
          2*weightedAdjoint Gi G E+weightedAdjoint Gi G (K*d)-weightedAdjoint Gi G (d*K) := by
        unfold weightedAdjoint commutator
        simp only [Matrix.transpose_add,Matrix.transpose_sub,Matrix.transpose_mul,Matrix.transpose_ofNat]
        noncomm_ring
      _=_ := by rw [hprod,hprod,hK]
  rw [hlin]
  unfold commutator
  noncomm_ring

/-- A genuine moving self-adjoint projector jet becomes a self-adjoint
balanced jet; the Gram term is retained, rather than discarded by convention. -/
theorem weighted_projection_balanced_adjoint (G Gi K P E : M) (hGGi : G*Gi=1)
    (hK : weightedAdjoint Gi G K=K) (hP : weightedAdjoint Gi G P=P)
    (hjet : weightedAdjoint Gi G E+commutator P K=E) :
    weightedAdjoint Gi G (2*E+commutator K P)=2*E+commutator K P := by
  have h := weighted_adjoint_twice_balanced G Gi K P E hGGi hK
  rw [hP,hjet] at h
  exact h.symm

/-- The same balanced chart respects the complete moving-unitarity equation. -/
theorem weighted_unitary_balanced_tangent (G Gi K U V E : M) (hGGi : G*Gi=1)
    (hK : weightedAdjoint Gi G K=K) (hV : weightedAdjoint Gi G U=V)
    (hVU : V*U=1)
    (hjet : (weightedAdjoint Gi G E+commutator V K)*U+V*E=0) :
    weightedAdjoint Gi G (2*E+commutator K U)*U+V*(2*E+commutator K U)=0 := by
  have h := weighted_adjoint_twice_balanced G Gi K U E hGGi hK
  rw [hV] at h
  rw [← h]
  calc
    (2*(weightedAdjoint Gi G E+commutator V K)+commutator K V)*U+
        V*(2*E+commutator K U)=
      2*((weightedAdjoint Gi G E+commutator V K)*U+V*E)+commutator K (V*U) := by
        unfold commutator; noncomm_ring
    _=0 := by rw [hjet,hVU]; simp [commutator]

/-- Both off-diagonal projector tangent blocks are retained. -/
theorem projection_tangent_diagonal_zero (P X : M) (hP : P*P=P)
    (hX : P*X+X*P=X) : P*X*P=0 := by
  have h := congrArg (fun Y : M => P*Y) hX
  have he : P*X+P*X*P=P*X := by
    simpa only [Matrix.mul_add,← Matrix.mul_assoc,hP] using h
  exact add_left_cancel (show P*X+P*X*P=P*X+0 by simpa using he)

theorem projection_tangent_offdiagonal (P X : M) (hP : P*P=P)
    (hX : P*X+X*P=X) : X=(1-P)*X*P+P*X*(1-P) := by
  have hzero := projection_tangent_diagonal_zero P X hP hX
  calc
    X=P*X+X*P := hX.symm
    _=(1-P)*X*P+P*X*(1-P)+2*(P*X*P) := by noncomm_ring
    _=_ := by rw [hzero]; simp

/-- Conversely every off-diagonal block gives an idempotent tangent. -/
theorem projection_offdiagonal_tangent (P B C : M) (hP : P*P=P) :
    let X := (1-P)*B*P+P*C*(1-P)
    P*X+X*P=X := by
  dsimp
  have h1 : P*((1-P)*B*P)=0 := by
    calc
      P*((1-P)*B*P)=(P-P*P)*B*P := by noncomm_ring
      _=0 := by rw [hP]; simp
  have h2 : (P*C*(1-P))*P=0 := by
    calc
      (P*C*(1-P))*P=P*C*(P-P*P) := by noncomm_ring
      _=0 := by rw [hP]; simp
  rw [Matrix.mul_add,Matrix.add_mul,h1,h2]
  simp only [zero_add,add_zero]
  calc
    P*(P*C*(1-P))+(1-P)*B*P*P=(P*P)*C*(1-P)+(1-P)*B*(P*P) := by noncomm_ring
    _=_ := by rw [hP]; abel

/-- The canonical infinitesimal rotation realizes the full projector tangent. -/
theorem projection_tangent_generator (P X : M) (hP : P*P=P)
    (hX : P*X+X*P=X) : commutator (commutator X P) P=X := by
  have hzero := projection_tangent_diagonal_zero P X hP hX
  unfold commutator
  calc
    (X*P-P*X)*P-P*(X*P-P*X)=X*(P*P)+(P*P)*X-2*(P*X*P) := by noncomm_ring
    _=X*P+P*X := by rw [hP,hzero]; simp
    _=X := by rw [add_comm]; exact hX

theorem projection_tangent_generator_skew (P X : M)
    (hP : P.transpose=P) (hX : X.transpose=X) :
    (commutator X P).transpose= -commutator X P := by
  simp only [commutator,Matrix.transpose_sub,Matrix.transpose_mul,hP,hX]
  abel

/-- The full orthogonal-group tangent is a skew generator, not an arbitrary jet. -/
theorem orthogonal_tangent_iff (U V E : M) (hVU : V*U=1)
    (hUV : U*V=1) (hV : V=U.transpose) :
    E.transpose*U+U.transpose*E=0 ↔ (V*E).transpose= -(V*E) := by
  subst V
  simp only [Matrix.transpose_mul,Matrix.transpose_transpose]
  exact add_eq_zero_iff_eq_neg

/-- Inverse motion replaces the full moving-metric adjoint jet on unitary paths. -/
theorem unitary_inverse_first_jet (U V E F : M) (hUV : U*V=1)
    (hjet : F*U+V*E=0) : F= -(V*E*V) := by
  have h := congrArg (fun X : M => X*V) hjet
  have he : F+V*E*V=0 := by
    simpa only [Matrix.add_mul,Matrix.zero_mul,Matrix.mul_assoc,hUV,Matrix.mul_one] using h
  exact add_eq_zero_iff_eq_neg.mp he

theorem trace_commutator_zero (A B : M) : Matrix.trace (commutator A B)=0 := by
  simp only [commutator,Matrix.trace_sub,Matrix.trace_mul_comm A B,sub_self]

/-- This is the finite internal trace Ward kernel; no spacetime Ward is asserted. -/
theorem trace_commutator_pairing (Y X K : M) :
    Matrix.trace (Y*commutator K X)=Matrix.trace (commutator X Y*K) := by
  unfold commutator
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.trace_sub]
  have h : Matrix.trace (Y*(K*X))=Matrix.trace (X*Y*K) := by
    rw [← Matrix.mul_assoc,Matrix.trace_mul_cycle]
  rw [h]
  simp only [Matrix.mul_assoc]

theorem trace_internal_ward (Y X K : M) (hYX : Y*X=X*Y) :
    Matrix.trace (Y*commutator K X)=0 := by
  rw [trace_commutator_pairing]
  simp [commutator,hYX]

/-- The heat Gram covector can be written using either half of D=d+a. -/
theorem gram_stress_two_forms (Y d a : M) (hYD : Y*(d+a)=(d+a)*Y) :
    -commutator Y a=commutator Y d := by
  unfold commutator
  have h : Y*d+Y*a=d*Y+a*Y := by simpa only [Matrix.mul_add,Matrix.add_mul] using hYD
  apply sub_eq_zero.mp
  calc
    -(Y*a-a*Y)-(Y*d-d*Y)= -((Y*d+Y*a)-(d*Y+a*Y)) := by noncomm_ring
    _=0 := by rw [h]; simp

theorem gram_stress_trace_zero (Y d : M) :
    Matrix.trace (2*commutator Y d)=0 := by
  have h : 2*commutator Y d=commutator Y d+commutator Y d := by noncomm_ring
  rw [h,Matrix.trace_add,trace_commutator_zero]; simp

/-- The trace first jet reduces onto the actual supported resolvent block. -/
theorem trace_projector_sandwich (R P X : M) (hPR : P*R=R) (hRP : R*P=R) :
    Matrix.trace (R*(P*X*P))=Matrix.trace (R*X) := by
  calc
    Matrix.trace (R*(P*X*P))=Matrix.trace (P*(R*P)*X) := by
      simp only [← Matrix.mul_assoc]
      rw [Matrix.trace_mul_cycle]
      simp only [Matrix.mul_assoc]
    _=Matrix.trace (R*X) := by rw [hRP,hPR]

/-- Full feedback first variation, including both cut endpoints and the middle cut.
Here R is the supported resolvent R_P; V is the supplied inverse of U. -/
theorem feedback_first_jet_covector (P N R U V E A : M)
    (hPR : P*R=R) (hRP : R*P=R) :
    Matrix.trace (R*(E*N*P+P*N*E+P*(commutator N A-V*E*U)*P))=
      Matrix.trace ((N*R+R*N-U*R*V)*E)+Matrix.trace (commutator R N*A) := by
  have h1 : Matrix.trace (R*(E*N*P))=Matrix.trace ((N*R)*E) := by
    calc
      Matrix.trace (R*(E*N*P))=Matrix.trace (P*R*(E*N)) := by
        simp only [← Matrix.mul_assoc]; rw [Matrix.trace_mul_cycle]
        simp only [Matrix.mul_assoc]
      _=Matrix.trace (R*(E*N)) := by rw [hPR]
      _=Matrix.trace ((N*R)*E) := by rw [← Matrix.mul_assoc,Matrix.trace_mul_cycle]
  have h2 : Matrix.trace (R*(P*N*E))=Matrix.trace ((R*N)*E) := by
    simp only [← Matrix.mul_assoc,hRP]
  have h3 : Matrix.trace (R*(V*E*U))=Matrix.trace ((U*R*V)*E) := by
    simp only [← Matrix.mul_assoc]; rw [Matrix.trace_mul_cycle]
    simp only [Matrix.mul_assoc]
  have h4 : Matrix.trace (R*(A*N))=Matrix.trace ((N*R)*A) := by
    rw [← Matrix.mul_assoc,Matrix.trace_mul_cycle]
  simp only [Matrix.mul_add,Matrix.trace_add]
  rw [h1,h2,trace_projector_sandwich R P _ hPR hRP]
  unfold commutator
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.add_mul,
    Matrix.trace_add,Matrix.trace_sub]
  rw [h3,h4]
  simp only [Matrix.mul_assoc]
  ring

/-- The resolvent commutation on F=PNP gives the single needed support balance. -/
theorem feedback_resolvent_support_balance (P N R : M)
    (hPR : P*R=R) (hRP : R*P=R) (hFR : (P*N*P)*R=R*(P*N*P)) :
    P*N*R=R*N*P := by
  calc
    P*N*R=P*N*(P*R) := by rw [hPR]
    _=(P*N*P)*R := by noncomm_ring
    _=R*(P*N*P) := hFR
    _=(R*P)*N*P := by noncomm_ring
    _=R*N*P := by rw [hRP]

/-- Exact Noether cancellation, before taking any trace. The hypotheses are
the inverse-gate intertwiners and the genuine supported-resolvent balance. -/
theorem feedback_noether_identity (P N R U V : M)
    (hPR : P*R=R) (hRP : R*P=R)
    (hbalance : P*N*R=R*N*P)
    (hNV : N*V=V*(1-P)) (hUN : U*N=(1-P)*U) :
    commutator P (N*R+R*N-U*R*V)+
      U*commutator R N*V-commutator R N=0 := by
  unfold commutator
  calc
    P*(N*R+R*N-U*R*V)-(N*R+R*N-U*R*V)*P+
        U*(R*N-N*R)*V-(R*N-N*R)=
      P*N*R+(P*R)*N-P*U*R*V-N*(R*P)-R*N*P+U*R*V*P+
        U*R*(N*V)-(U*N)*R*V-R*N+N*R := by noncomm_ring
    _=0 := by rw [hPR,hRP,hbalance,hNV,hUN]; noncomm_ring

/-- The intertwiners in the preceding Ward identity follow from the actual
full feedback definition with V=U inverse, not an independently chosen N. -/
theorem feedback_inverse_intertwiners (P U V : M) (hUV : U*V=1) :
    (V*(1-P)*U)*V=V*(1-P) ∧ U*(V*(1-P)*U)=(1-P)*U := by
  constructor
  · calc
      (V*(1-P)*U)*V=V*(1-P)*(U*V) := by noncomm_ring
      _=_ := by rw [hUV]; simp
  · calc
      U*(V*(1-P)*U)=(U*V)*(1-P)*U := by noncomm_ring
      _=_ := by rw [hUV]; simp

end FiniteMatrices
end D0.Research.JointAdjointSource

#print D0.Geometry.archive_weighted_hodge_dirac_owner
#print D0.Cosmology.feedback_variation_universal_source
#print D0.Geometry.archiveSolderedCodifferential
#check D0.Geometry.archiveSolderedForwardDifferential_frame
#check D0.Geometry.observerExteriorPairing_congruence
#print axioms D0.Geometry.archive_weighted_hodge_dirac_owner
#print axioms D0.Cosmology.feedback_variation_universal_source
#print axioms D0.Geometry.archiveSolderedForwardDifferential_frame
#print axioms D0.Geometry.observerExteriorPairing_congruence
#print axioms D0.Research.JointAdjointSource.weighted_adjoint_unique
#print axioms D0.Research.JointAdjointSource.weighted_adjoint_first_jet
#print axioms D0.Research.JointAdjointSource.inverse_gram_first_jet
#print axioms D0.Research.JointAdjointSource.weighted_adjoint_basis_covariance
#print axioms D0.Research.JointAdjointSource.weighted_adjoint_twice_balanced
#print axioms D0.Research.JointAdjointSource.weighted_projection_balanced_adjoint
#print axioms D0.Research.JointAdjointSource.weighted_unitary_balanced_tangent
#print axioms D0.Research.JointAdjointSource.projection_tangent_diagonal_zero
#print axioms D0.Research.JointAdjointSource.projection_tangent_offdiagonal
#print axioms D0.Research.JointAdjointSource.projection_offdiagonal_tangent
#print axioms D0.Research.JointAdjointSource.projection_tangent_generator
#print axioms D0.Research.JointAdjointSource.projection_tangent_generator_skew
#print axioms D0.Research.JointAdjointSource.orthogonal_tangent_iff
#print axioms D0.Research.JointAdjointSource.unitary_inverse_first_jet
#print axioms D0.Research.JointAdjointSource.trace_commutator_zero
#print axioms D0.Research.JointAdjointSource.trace_commutator_pairing
#print axioms D0.Research.JointAdjointSource.trace_internal_ward
#print axioms D0.Research.JointAdjointSource.gram_stress_two_forms
#print axioms D0.Research.JointAdjointSource.gram_stress_trace_zero
#print axioms D0.Research.JointAdjointSource.trace_projector_sandwich
#print axioms D0.Research.JointAdjointSource.feedback_first_jet_covector
#print axioms D0.Research.JointAdjointSource.feedback_resolvent_support_balance
#print axioms D0.Research.JointAdjointSource.feedback_noether_identity
#print axioms D0.Research.JointAdjointSource.feedback_inverse_intertwiners
