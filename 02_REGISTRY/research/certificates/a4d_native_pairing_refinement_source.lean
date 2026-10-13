import D0.Geometry.ArchiveMetricMeasureHodgeLift
import D0.Geometry.ArchiveRefinementHodgeWeights
import Mathlib.Tactic

/-!
Research kernel for A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md.
All inclusions are genuinely rectangular: the fine index ν and coarse index ι
are independent. The algebraic first jets below do not assume or prove native
admission, positivity of a supplied Gram, a differentiable preparation, a
thermal functional-calculus theorem, or the continuum source transfer.
The final positivity statements are in orthonormal real coordinates.
The two imported owner propositions are printed exactly: their endpoint and
arithmetic conclusions are not a theorem of adjoint refinement.
-/
namespace D0.Research.PairingRefinementSource

set_option linter.unusedSectionVars false

variable {ι ν : Type*} [Fintype ι] [Fintype ν] [DecidableEq ι] [DecidableEq ν]

local notation "MC" => Matrix ι ι ℝ
local notation "MF" => Matrix ν ν ℝ
local notation "Lift" => Matrix ν ι ℝ
local notation "Readback" => Matrix ι ν ℝ

def rectAdjoint (Gi : MC) (G : MF) (R : Lift) : Readback :=
  Gi * R.transpose * G

/-- Isometry and a genuine inverse Gram give a left inverse, with no equality
of coarse and fine dimensions. -/
theorem isometric_readback_left_inverse (J : Lift) (Gf : MF) (Gc Gci : MC)
    (hi : Gci * Gc = 1) (hiso : J.transpose * Gf * J = Gc) :
    rectAdjoint Gci Gf J * J = 1 := by
  simp only [rectAdjoint, Matrix.mul_assoc] at *
  rw [hiso, hi]

theorem complement_projection (J : Lift) (C : Readback) (hCJ : C * J = 1) :
    (1-J*C)*J=0 ∧ C*(1-J*C)=0 ∧ (1-J*C)*(1-J*C)=1-J*C := by
  have hJ : (1-J*C)*J=0 := by
    simp only [Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc, hCJ, Matrix.mul_one, sub_self]
  have hC : C*(1-J*C)=0 := by
    simp only [Matrix.mul_sub, Matrix.mul_one, ← Matrix.mul_assoc, hCJ, Matrix.one_mul, sub_self]
  refine ⟨hJ,hC,?_⟩
  simp only [Matrix.mul_sub, Matrix.sub_mul, Matrix.one_mul, Matrix.mul_one,
    Matrix.mul_assoc]
  rw [← Matrix.mul_assoc C J, hCJ, Matrix.one_mul]
  abel

/-- The adjoint of the chain equation gives a readback identity globally;
the opposite readback identity still needs the leakage to vanish. -/
theorem chain_adjoint_readback (J : Lift) (df Gf Gfi : MF) (dc Gc Gci : MC)
    (hf : Gf*Gfi=1) (hc : Gc*Gci=1) (hchain : df*J=J*dc) :
    rectAdjoint Gci Gf J * (Gfi*df.transpose*Gf) =
      (Gci*dc.transpose*Gc) * rectAdjoint Gci Gf J := by
  have ht := congrArg Matrix.transpose hchain
  simp only [Matrix.transpose_mul] at ht
  unfold rectAdjoint
  calc
    Gci*J.transpose*Gf*(Gfi*df.transpose*Gf)=Gci*(J.transpose*df.transpose)*Gf := by
      simp only [Matrix.mul_assoc]
      rw [← Matrix.mul_assoc Gf Gfi, hf, Matrix.one_mul]
    _=Gci*(dc.transpose*J.transpose)*Gf := by rw [ht]
    _=(Gci*dc.transpose*Gc)*(Gci*J.transpose*Gf) := by
      simp only [Matrix.mul_assoc]
      rw [← Matrix.mul_assoc Gc Gci, hc, Matrix.one_mul]

theorem adjoint_compression (J : Lift) (C : Readback) (dfAdj : MF) (dcAdj : MC)
    (hCJ : C*J=1) (hread : C*dfAdj=dcAdj*C) : C*dfAdj*J=dcAdj := by
  rw [hread, Matrix.mul_assoc, hCJ, Matrix.mul_one]

/-- The Dirac compression follows from the actual chain equation and its
adjoint readback, without assuming full adjoint intertwining. -/
theorem dirac_compression (J : Lift) (C : Readback) (df dfAdj : MF) (dc dcAdj : MC)
    (hCJ : C*J=1) (hchain : df*J=J*dc) (hread : C*dfAdj=dcAdj*C) :
    C*(df+dfAdj)*J=dc+dcAdj := by
  have hd : C*df*J=dc := by
    rw [Matrix.mul_assoc,hchain,← Matrix.mul_assoc,hCJ,Matrix.one_mul]
  simp only [Matrix.mul_add,Matrix.add_mul,hd,adjoint_compression J C dfAdj dcAdj hCJ hread]

theorem leakage_is_intertwining_defect (J : Lift) (C : Readback) (D : MF) :
    (1-J*C)*D*J=D*J-J*(C*D*J) := by
  simp only [Matrix.sub_mul,Matrix.one_mul,Matrix.mul_assoc]

/-- Exact rectangular Schur reaction identity. -/
theorem compressed_square_reaction (J : Lift) (C : Readback) (D : MF) :
    C*(D*D)*J=(C*D*J)*(C*D*J)+(C*D*(1-J*C))*(D*J) := by
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_one,Matrix.mul_assoc]
  abel

theorem compressed_square_complement (J : Lift) (C : Readback) (D : MF)
    (hCJ : C*J=1) :
    C*(D*D)*J=(C*D*J)*(C*D*J)+(C*D*(1-J*C))*((1-J*C)*D*J) := by
  have hQ := (complement_projection J C hCJ).2.2
  calc
    C*(D*D)*J=(C*D*J)*(C*D*J)+(C*D*(1-J*C))*(D*J) :=
      compressed_square_reaction J C D
    _=(C*D*J)*(C*D*J)+(C*D*((1-J*C)*(1-J*C)))*(D*J) := by rw [hQ]
    _=_ := by simp only [Matrix.mul_assoc]

/-- The adjoint relation needed to identify the reaction as R†R. This is a
weighted rectangular identity; all inverse-Gram hypotheses are exposed. -/
theorem leakage_weighted_adjoint (J : Lift) (C : Readback) (D Gf Gfi Q : MF)
    (Gci : MC) (hf : Gf*Gfi=1) (hC : C=rectAdjoint Gci Gf J)
    (hD : Gfi*D.transpose*Gf=D) (hQ : Gfi*Q.transpose*Gf=Q) :
    rectAdjoint Gci Gf (Q*D*J)=C*D*Q := by
  subst C
  unfold rectAdjoint
  simp only [Matrix.transpose_mul]
  calc
    Gci*(J.transpose*(D.transpose*Q.transpose))*Gf =
        Gci*J.transpose*Gf*(Gfi*D.transpose*Gf)*(Gfi*Q.transpose*Gf) := by
      simp only [Matrix.mul_assoc]
      simp only [← Matrix.mul_assoc Gf Gfi,hf,Matrix.one_mul]
    _=Gci*J.transpose*Gf*D*Q := by rw [hD,hQ]

theorem leakage_zero_iff_intertwining (J : Lift) (C : Readback) (D : MF) :
    (1-J*C)*D*J=0 ↔ D*J=J*(C*D*J) := by
  rw [leakage_is_intertwining_defect, sub_eq_zero]

theorem weighted_complement_adjoint (J : Lift) (Gf Gfi : MF) (Gci : MC)
    (hf : Gfi*Gf=1) (hfs : Gf.transpose=Gf) (hcs : Gci.transpose=Gci) :
    Gfi*(1-J*rectAdjoint Gci Gf J).transpose*Gf=1-J*rectAdjoint Gci Gf J := by
  unfold rectAdjoint
  simp only [Matrix.transpose_sub,Matrix.transpose_one,Matrix.transpose_mul,
    Matrix.transpose_transpose,hfs,hcs,Matrix.mul_sub,Matrix.sub_mul,
    Matrix.mul_one,Matrix.mul_assoc]
  simp only [← Matrix.mul_assoc Gfi Gf,hf,Matrix.one_mul]

/-- Weighted capstone: exact positive-reaction form, before imposing a
positivity assumption or passing to orthonormal coordinates. -/
theorem weighted_compressed_square (J : Lift) (C : Readback) (D Gf Gfi : MF)
    (Gci Dc : MC) (hCJ : C*J=1) (hf : Gf*Gfi=1)
    (hC : C=rectAdjoint Gci Gf J) (hD : Gfi*D.transpose*Gf=D)
    (hQ : Gfi*(1-J*C).transpose*Gf=1-J*C) (hcomp : C*D*J=Dc) :
    C*(D*D)*J=Dc*Dc+
      rectAdjoint Gci Gf ((1-J*C)*D*J)*((1-J*C)*D*J) := by
  rw [leakage_weighted_adjoint J C D Gf Gfi (1-J*C) Gci hf hC hD hQ]
  simpa only [hcomp] using compressed_square_complement J C D hCJ

/-- Explicit first derivative of the rectangular weighted adjoint. The four
product terms on the left include the inverse coarse Gram derivative. -/
theorem rectangular_adjoint_first_jet (R E : Lift) (Gci Gcdot : MC)
    (Gf Gfi Gfdot : MF) (hi : Gf*Gfi=1) :
    (-Gci*Gcdot*Gci)*R.transpose*Gf+Gci*E.transpose*Gf+Gci*R.transpose*Gfdot =
      rectAdjoint Gci Gf E-(Gci*Gcdot)*rectAdjoint Gci Gf R+
        rectAdjoint Gci Gf R*(Gfi*Gfdot) := by
  unfold rectAdjoint
  simp only [Matrix.mul_assoc,Matrix.neg_mul]
  rw [← Matrix.mul_assoc Gf Gfi,hi,Matrix.one_mul]
  abel

/-- The full Gram-dependent reaction jet. E is dot R and Eadj is its weighted
adjoint; Kf and Kc are the two distinct Gram logarithmic derivatives. -/
theorem reaction_first_jet (R E : Lift) (Radj Eadj : Readback) (Kc : MC) (Kf : MF) :
    (Eadj+Radj*Kf-Kc*Radj)*R+Radj*E =
      Eadj*R+Radj*E+Radj*Kf*R-Kc*(Radj*R) := by
  simp only [Matrix.add_mul,Matrix.sub_mul,Matrix.mul_assoc]
  abel

/-- Twice the balanced derivative avoids denominators while retaining all
moving Gram terms. This identity is rectangular on both sides. -/
theorem reaction_twice_balanced (R E : Lift) (Radj Eadj : Readback) (Kc : MC) (Kf : MF) :
    let S := Radj*R
    let T := (Eadj+Radj*Kf-Kc*Radj)*R+Radj*E
    T+T+Kc*S-S*Kc =
      (Eadj+Eadj+Radj*Kf-Kc*Radj)*R+Radj*(E+E+Kf*R-R*Kc) := by
  dsimp
  simp only [Matrix.add_mul,Matrix.sub_mul,Matrix.mul_add,Matrix.mul_sub,Matrix.mul_assoc]
  abel

/-- The adjoint in the balanced reaction formula is the actual rectangular
weighted adjoint. These are precisely the two Gram-symmetry relations used. -/
theorem rectangular_balanced_adjoint (R E : Lift) (Gci Kc : MC) (Gf Kf : MF)
    (hc : Gci*Kc.transpose=Kc*Gci) (hf : Kf.transpose*Gf=Gf*Kf) :
    rectAdjoint Gci Gf (E+E+Kf*R-R*Kc)=
      rectAdjoint Gci Gf E+rectAdjoint Gci Gf E+
        rectAdjoint Gci Gf R*Kf-Kc*rectAdjoint Gci Gf R := by
  have hfR : rectAdjoint Gci Gf (Kf*R)=rectAdjoint Gci Gf R*Kf := by
    unfold rectAdjoint
    simp only [Matrix.transpose_mul,Matrix.mul_assoc]
    rw [hf]
  have hcR : rectAdjoint Gci Gf (R*Kc)=Kc*rectAdjoint Gci Gf R := by
    unfold rectAdjoint
    simp only [Matrix.transpose_mul,← Matrix.mul_assoc]
    rw [hc]
  have hlin : rectAdjoint Gci Gf (E+E+Kf*R-R*Kc)=
      rectAdjoint Gci Gf E+rectAdjoint Gci Gf E+
        rectAdjoint Gci Gf (Kf*R)-rectAdjoint Gci Gf (R*Kc) := by
    simp only [rectAdjoint,Matrix.transpose_add,Matrix.transpose_sub,
      Matrix.mul_add,Matrix.mul_sub,Matrix.add_mul,Matrix.sub_mul]
  rw [hlin,hfR,hcR]

/-- Moving the inclusion and readback is part of the leakage jet. -/
theorem moving_complement_jet (J Jdot : Lift) (C Cdot : Readback) (D Ddot : MF) :
    (-(Jdot*C+J*Cdot))*D*J+(1-J*C)*Ddot*J+(1-J*C)*D*Jdot =
      Ddot*J+D*Jdot-Jdot*(C*D*J)-J*(Cdot*D*J+C*Ddot*J+C*D*Jdot) := by
  simp only [Matrix.add_mul,Matrix.sub_mul,Matrix.mul_add,
    Matrix.neg_mul,Matrix.one_mul,Matrix.mul_assoc]
  abel

/-- Joint change of bases sends a rectangular weighted adjoint contravariantly.
The explicit inverse hypotheses prevent a Gram change from being mistaken
for a pure basis change. -/
theorem rectangular_adjoint_basis_covariance (R : Lift) (Gci Tc Tci : MC)
    (Gf Tf Tfi : MF) (hc : Tci*Tc=1) (hf : Tfi*Tf=1) :
    rectAdjoint (Tc*Gci*Tc.transpose) (Tfi.transpose*Gf*Tfi) (Tf*R*Tci) =
      Tc*rectAdjoint Gci Gf R*Tfi := by
  have hct : Tc.transpose*Tci.transpose=1 := by
    simpa only [Matrix.transpose_mul,Matrix.transpose_one] using congrArg Matrix.transpose hc
  have hft : Tf.transpose*Tfi.transpose=1 := by
    simpa only [Matrix.transpose_mul,Matrix.transpose_one] using congrArg Matrix.transpose hf
  unfold rectAdjoint
  simp only [Matrix.transpose_mul,Matrix.mul_assoc]
  rw [← Matrix.mul_assoc Tc.transpose Tci.transpose,hct,Matrix.one_mul,
    ← Matrix.mul_assoc Tf.transpose Tfi.transpose,hft,Matrix.one_mul]

theorem reaction_basis_covariance (R : Lift) (Radj : Readback) (Tc Tci : MC)
    (Tf Tfi : MF) (hf : Tfi*Tf=1) :
    (Tc*Radj*Tfi)*(Tf*R*Tci)=Tc*(Radj*R)*Tci := by
  simp only [Matrix.mul_assoc]
  rw [← Matrix.mul_assoc Tfi Tf,hf,Matrix.one_mul]

/-- Positivity and its zero criterion for a genuine rectangular leakage in
orthonormal real coordinates. -/
theorem reaction_diagonal_nonnegative (R : Lift) (i : ι) :
    0 ≤ (R.transpose*R) i i := by
  simp only [Matrix.mul_apply,Matrix.transpose_apply]
  exact Finset.sum_nonneg (fun k _ => mul_self_nonneg (R k i))

theorem reaction_zero_iff (R : Lift) : R.transpose*R=0 ↔ R=0 := by
  constructor
  · intro h
    ext k i
    have hd : ∑ a, R a i * R a i = 0 := by
      simpa only [Matrix.mul_apply,Matrix.transpose_apply,Matrix.zero_apply] using
        congrArg (fun X : MC => X i i) h
    have hz := (Finset.sum_eq_zero_iff_of_nonneg (fun a _ => mul_self_nonneg (R a i))).mp hd k (Finset.mem_univ k)
    exact mul_self_eq_zero.mp hz
  · intro h
    subst R
    simp

theorem orthogonal_compressed_square (J : Lift) (D : MF)
    (hJ : J.transpose*J=1) (hD : D.transpose=D) :
    J.transpose*(D*D)*J=(J.transpose*D*J)*(J.transpose*D*J)+
      ((1-J*J.transpose)*D*J).transpose*((1-J*J.transpose)*D*J) := by
  have hQt : (1-J*J.transpose).transpose=1-J*J.transpose := by
    simp only [Matrix.transpose_sub,Matrix.transpose_one,Matrix.transpose_mul,Matrix.transpose_transpose]
  have hr : ((1-J*J.transpose)*D*J).transpose=J.transpose*D*(1-J*J.transpose) := by
    simp only [Matrix.transpose_mul,hQt,hD,Matrix.mul_assoc]
  rw [hr]
  exact compressed_square_complement J J.transpose D hJ

/-- A square intertwiner forces a Dirac intertwiner; positivity of the complete
retained leakage is the substantive implication. -/
theorem orthogonal_square_intertwining_iff (J : Lift) (D : MF)
    (hJ : J.transpose*J=1) (hD : D.transpose=D) :
    (D*D)*J=J*((J.transpose*D*J)*(J.transpose*D*J)) ↔
      D*J=J*(J.transpose*D*J) := by
  constructor
  · intro hs
    have hcomp := congrArg (fun X : Lift => J.transpose*X) hs
    have he : J.transpose*(D*D)*J=(J.transpose*D*J)*(J.transpose*D*J) := by
      simpa only [← Matrix.mul_assoc,hJ,Matrix.one_mul] using hcomp
    have hreact := orthogonal_compressed_square J D hJ hD
    rw [he] at hreact
    have hz : ((1-J*J.transpose)*D*J).transpose*((1-J*J.transpose)*D*J)=0 := by
      exact add_left_cancel (show
        (J.transpose*D*J)*(J.transpose*D*J)+((1-J*J.transpose)*D*J).transpose*((1-J*J.transpose)*D*J)=
        (J.transpose*D*J)*(J.transpose*D*J)+0 by simpa using hreact.symm)
    exact (leakage_zero_iff_intertwining J J.transpose D).mp ((reaction_zero_iff _).mp hz)
  · intro hd
    calc
      (D*D)*J=D*(D*J) := Matrix.mul_assoc _ _ _
      _=D*(J*(J.transpose*D*J)) := by rw [hd]
      _=(D*J)*(J.transpose*D*J) := (Matrix.mul_assoc _ _ _).symm
      _=J*((J.transpose*D*J)*(J.transpose*D*J)) := by rw [hd,Matrix.mul_assoc]

/-- Algebraic correction for two distinct Gibbs weights; equality of these
weights is deliberately not a hypothesis. -/
theorem source_covector_correction (W V A T : MC) :
    -Matrix.trace (W*(A+T))+Matrix.trace (V*A)=
      -Matrix.trace ((W-V)*A)-Matrix.trace (W*T) := by
  simp only [Matrix.mul_add,Matrix.sub_mul,Matrix.trace_add,Matrix.trace_sub]
  ring

theorem symmetric_reaction_contraction (W : MC) (R E : Lift)
    (hW : W.transpose=W) :
    Matrix.trace (W*(E.transpose*R+R.transpose*E))=
      2*Matrix.trace (W*R.transpose*E) := by
  have h : Matrix.trace (W*(E.transpose*R))=Matrix.trace (W*(R.transpose*E)) := by
    calc
      Matrix.trace (W*(E.transpose*R))=Matrix.trace ((W*(E.transpose*R)).transpose) :=
        (Matrix.trace_transpose _).symm
      _=Matrix.trace ((R.transpose*E)*W) := by
        simp only [Matrix.transpose_mul,Matrix.transpose_transpose,hW]
      _=Matrix.trace (W*(R.transpose*E)) := Matrix.trace_mul_comm _ _
  rw [Matrix.mul_add,Matrix.trace_add,h]
  simp only [Matrix.mul_assoc]
  ring

theorem source_internal_ward (W A V : MC) (hWA : W*A=A*W) :
    Matrix.trace (W*(V*A-A*V))=0 := by
  have h : Matrix.trace (W*(V*A))=Matrix.trace (W*(A*V)) := by
    calc
      Matrix.trace (W*(V*A))=Matrix.trace (A*(W*V)) := by
        rw [← Matrix.mul_assoc,Matrix.trace_mul_comm]
      _=Matrix.trace ((W*A)*V) := by rw [← Matrix.mul_assoc,← hWA]
      _=Matrix.trace (W*(A*V)) := by rw [Matrix.mul_assoc]
  rw [Matrix.mul_sub,Matrix.trace_sub,h,sub_self]

end D0.Research.PairingRefinementSource

-- Actual consumed definitions and propositions, not their explanatory comments.
#print D0.Geometry.hodgeMetricMeasureWeight
#print D0.Geometry.hodgeGramTraceDegree
#print D0.Geometry.totalHodgeGramTraceSum
#print D0.Geometry.archive_metric_measure_hodge_lift_owner
#print D0.Geometry.archive_refinement_hodge_weights_owner
#check D0.Geometry.archive_metric_measure_hodge_lift_owner
#check D0.Geometry.archive_refinement_hodge_weights_owner
#check D0.Research.PairingRefinementSource.weighted_compressed_square
#check D0.Research.PairingRefinementSource.orthogonal_square_intertwining_iff
#check D0.Research.PairingRefinementSource.rectangular_adjoint_first_jet
#check D0.Research.PairingRefinementSource.rectangular_balanced_adjoint
#print axioms D0.Research.PairingRefinementSource.isometric_readback_left_inverse
#print axioms D0.Research.PairingRefinementSource.complement_projection
#print axioms D0.Research.PairingRefinementSource.chain_adjoint_readback
#print axioms D0.Research.PairingRefinementSource.adjoint_compression
#print axioms D0.Research.PairingRefinementSource.dirac_compression
#print axioms D0.Research.PairingRefinementSource.leakage_is_intertwining_defect
#print axioms D0.Research.PairingRefinementSource.compressed_square_reaction
#print axioms D0.Research.PairingRefinementSource.compressed_square_complement
#print axioms D0.Research.PairingRefinementSource.leakage_weighted_adjoint
#print axioms D0.Research.PairingRefinementSource.leakage_zero_iff_intertwining
#print axioms D0.Research.PairingRefinementSource.weighted_complement_adjoint
#print axioms D0.Research.PairingRefinementSource.weighted_compressed_square
#print axioms D0.Research.PairingRefinementSource.rectangular_adjoint_first_jet
#print axioms D0.Research.PairingRefinementSource.reaction_first_jet
#print axioms D0.Research.PairingRefinementSource.reaction_twice_balanced
#print axioms D0.Research.PairingRefinementSource.rectangular_balanced_adjoint
#print axioms D0.Research.PairingRefinementSource.moving_complement_jet
#print axioms D0.Research.PairingRefinementSource.rectangular_adjoint_basis_covariance
#print axioms D0.Research.PairingRefinementSource.reaction_basis_covariance
#print axioms D0.Research.PairingRefinementSource.reaction_diagonal_nonnegative
#print axioms D0.Research.PairingRefinementSource.reaction_zero_iff
#print axioms D0.Research.PairingRefinementSource.orthogonal_compressed_square
#print axioms D0.Research.PairingRefinementSource.orthogonal_square_intertwining_iff
#print axioms D0.Research.PairingRefinementSource.source_covector_correction
#print axioms D0.Research.PairingRefinementSource.symmetric_reaction_contraction
#print axioms D0.Research.PairingRefinementSource.source_internal_ward
#print axioms D0.Geometry.archive_metric_measure_hodge_lift_owner
#print axioms D0.Geometry.archive_refinement_hodge_weights_owner
