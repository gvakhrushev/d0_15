import D0.Matter.HiggsLogdetStationary
import D0.Matter.HiggsRadialInstabilityBoundary
import D0.Cosmology.FeedbackPartitionFunction
import D0.Geometry.ArchiveStressEdgeReadout
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-! Research analysis of the already specified scalar/matrix log-det formula.
No core action, physical operator map or on-shell gate is installed here.
The all-size source-image and convex-profile proofs are in the companion memo. -/

namespace D0.Research.NativeLogdet
open Matrix
open scoped BigOperators
noncomputable section

def scalarLogdet (z : ℝ) (f : ℝ → ℝ) (t : ℝ) : ℝ :=
  -2 * Real.log (1-z*f t)

theorem scalarLogdet_hasDerivAt (f : ℝ → ℝ) (z x fp : ℝ)
    (hf : HasDerivAt f fp x) (hD : 1-z*f x ≠ 0) :
    HasDerivAt (scalarLogdet z f) (2*z*fp/(1-z*f x)) x := by
  have h := (((hasDerivAt_const x (1:ℝ)).sub (hf.const_mul z)).log hD).const_mul (-2)
  convert h using 1
  dsimp
  ring

theorem scalarLogdet_stationary_iff (f : ℝ → ℝ) (z x fp : ℝ)
    (hf : HasDerivAt f fp x) (hD : 1-z*f x ≠ 0) (hz : z ≠ 0) :
    deriv (scalarLogdet z f) x=0 ↔ fp=0 := by
  rw [(scalarLogdet_hasDerivAt f z x fp hf hD).deriv]
  simp [div_eq_zero_iff, hD, hz]

def realProfile (t : ℝ) : ℝ := t/(1+t^2)

theorem realProfile_cast (q : ℚ) :
    realProfile (q:ℝ)=(D0.Matter.fProfile q:ℝ) := by
  simp [realProfile,D0.Matter.fProfile]

theorem realProfile_hasDerivAt (x : ℝ) :
    HasDerivAt realProfile ((1-x^2)/(1+x^2)^2) x := by
  have hp : 1+x^2 ≠ (0:ℝ) := ne_of_gt (by positivity)
  have h := (hasDerivAt_id x).div ((hasDerivAt_const x (1:ℝ)).add ((hasDerivAt_id x).pow 2)) hp
  convert h using 1
  dsimp
  ring

def profileEncoding (z U : ℝ) : ℝ := (1-Real.exp (-U/2))/z

theorem profileEncoding_domain (z U : ℝ) (hz : z ≠ 0) :
    1-z*profileEncoding z U=Real.exp (-U/2) := by
  unfold profileEncoding
  field_simp
  ring

theorem profileEncoding_positive_domain (z U : ℝ) (hz : z ≠ 0) :
    0 < 1-z*profileEncoding z U := by
  rw [profileEncoding_domain z U hz]
  exact Real.exp_pos _

theorem arbitrary_profile_exact_encoding {X : Type} (U : X → ℝ) (z : ℝ) (hz : z ≠ 0) :
    ∀ x, -2*Real.log (1-z*profileEncoding z (U x))=U x := by
  intro x
  rw [profileEncoding_domain z (U x) hz,Real.log_exp]
  ring

theorem profile_encoding_is_not_selection (z : ℝ) (hz : z ≠ 0) :
    profileEncoding z 0 ≠ profileEncoding z 1 := by
  intro h
  have h0 := arbitrary_profile_exact_encoding (fun _ : Unit => (0:ℝ)) z hz ()
  have h1 := arbitrary_profile_exact_encoding (fun _ : Unit => (1:ℝ)) z hz ()
  change -2*Real.log (1-z*profileEncoding z 0)=0 at h0
  change -2*Real.log (1-z*profileEncoding z 1)=1 at h1
  rw [h] at h0
  linarith

variable {I : Type} [Fintype I] [DecidableEq I]

theorem determinant_similarity (U : (Matrix I I ℝ)ˣ) (F : Matrix I I ℝ) (z : ℝ) :
    (1-z • ((U : Matrix I I ℝ)*F*(↑U⁻¹ : Matrix I I ℝ))).det = (1-z • F).det := by
  have h : 1-z • ((U : Matrix I I ℝ)*F*(↑U⁻¹ : Matrix I I ℝ)) =
      (U : Matrix I I ℝ)*(1-z • F)*(↑U⁻¹ : Matrix I I ℝ) := by
    simp only [mul_sub,sub_mul,mul_one,mul_smul_comm,smul_mul_assoc,
      Units.mul_inv]
  rw [h]
  exact Matrix.det_units_conj U (1-z • F)

theorem logdet_similarity (U : (Matrix I I ℝ)ˣ) (F : Matrix I I ℝ) (z : ℝ) :
    -Real.log (1-z • ((U : Matrix I I ℝ)*F*(↑U⁻¹ : Matrix I I ℝ))).det =
      -Real.log (1-z • F).det := by
  rw [determinant_similarity]

theorem rank_two_scalar_reduction (z f : ℝ) :
    -Real.log ((1 : Matrix (Fin 2) (Fin 2) ℝ)-z • (f • 1)).det =
      -2*Real.log (1-z*f) := by
  have he : ((1 : Matrix (Fin 2) (Fin 2) ℝ)-z • (f • 1))=(1-z*f) • 1 := by
    rw [smul_smul,sub_smul,one_smul]
  rw [he,Matrix.det_smul,Matrix.det_one]
  simp only [Fintype.card_fin,mul_one,Real.log_pow,Nat.cast_ofNat]
  ring

omit [DecidableEq I] in
theorem conjugation_ward (R F K : Matrix I I ℝ) (hRF : R*F=F*R) :
    Matrix.trace (R*(K*F-F*K))=0 := by
  rw [mul_sub,Matrix.trace_sub,← Matrix.mul_assoc,← Matrix.mul_assoc,
    Matrix.trace_mul_cycle R K F,hRF]
  simp only [Matrix.mul_assoc,sub_self]

def edgeVector (i j : I) : I → ℝ :=
  fun a => (if a=i then 1 else 0)-(if a=j then 1 else 0)

omit [Fintype I] in
theorem edgeVector_ne_zero (i j : I) (hij : i ≠ j) : edgeVector i j ≠ 0 := by
  intro h
  have := congrFun h i
  simp [edgeVector,hij] at this

theorem edge_quadratic (R : Matrix I I ℝ) (i j : I) :
    edgeVector i j ⬝ᵥ (R *ᵥ edgeVector i j)=R i i+R j j-R i j-R j i := by
  simp only [dotProduct,Matrix.mulVec,edgeVector,mul_sub,sub_mul,Finset.sum_sub_distrib]
  simp
  ring

theorem positive_definite_edge (R : Matrix I I ℝ) (hR : R.PosDef)
    (i j : I) (hij : i ≠ j) : 0 < R i i+R j j-R i j-R j i := by
  have h := hR.dotProduct_mulVec_pos (edgeVector_ne_zero i j hij)
  simpa only [star_trivial,edge_quadratic] using h

theorem actual_edge_readout_positive (R : Matrix I I ℝ) (hR : R.PosDef)
    (i j : I) (hij : i ≠ j) (c : ℝ) (hc : 0<c) :
    0 < D0.Geometry.edgeStressReadout c (R i i) (R j j) (R i j) := by
  have h := positive_definite_edge R hR i j hij
  have hs : R j i=R i j := by
    have he := congrFun (congrFun hR.isHermitian i) j
    simpa only [Matrix.conjTranspose_apply,star_trivial] using he
  unfold D0.Geometry.edgeStressReadout
  apply mul_pos hc
  rw [hs] at h
  linarith

theorem inverse_edge_source_positive (H : Matrix I I ℝ) (hH : H.PosDef)
    (i j : I) (hij : i ≠ j) (z c : ℝ) (hz : 0<z) (hc : 0<c) :
    0 < z*D0.Geometry.edgeStressReadout c
      (H⁻¹ i i) (H⁻¹ j j) (H⁻¹ i j) := by
  exact mul_pos hz (actual_edge_readout_positive H⁻¹ hH.inv i j hij c hc)

theorem full_edge_gate_impossible (H : Matrix I I ℝ) (hH : H.PosDef)
    (i j : I) (hij : i ≠ j) (z c : ℝ) (hz : 0<z) (hc : 0<c) :
    z*D0.Geometry.edgeStressReadout c (H⁻¹ i i) (H⁻¹ j j) (H⁻¹ i j) ≠ 0 :=
  ne_of_gt (inverse_edge_source_positive H hH i j hij z c hz hc)

theorem nonzero_coupling_edge_gate_impossible (H : Matrix I I ℝ) (hH : H.PosDef)
    (i j : I) (hij : i ≠ j) (z c : ℝ) (hz : z ≠ 0) (hc : 0<c) :
    z*D0.Geometry.edgeStressReadout c (H⁻¹ i i) (H⁻¹ j j) (H⁻¹ i j) ≠ 0 :=
  mul_ne_zero hz (ne_of_gt (actual_edge_readout_positive H⁻¹ hH.inv i j hij c hc))

theorem actual_role_edge_source_positive (n : ℕ)
    (H : Matrix (D0.Geometry.ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint n)
      (D0.Geometry.ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint n) ℝ)
    (hH : H.PosDef) (i j : D0.Geometry.ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint n)
    (hij : D0.Geometry.rolePhaseAdjacent n i j) (z : ℝ) (hz : 0<z) :
    0 < z*D0.Geometry.edgeStressReadout
      (D0.Geometry.ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
      (H⁻¹ i i) (H⁻¹ j j) (H⁻¹ i j) := by
  apply inverse_edge_source_positive H hH i j _ z _ hz
    (D0.Geometry.ArchivePhaseEdgeMetricScale.archive_phase_edge_metric_scale_owner.2.2 n)
  intro heq
  subst j
  exact D0.Geometry.rolePhaseAdjacent_irreflexive n i hij

open D0.Geometry D0.Geometry.ArchiveRolePhaseProductCarrier

theorem mixed_profile_neighbor_zero (n : ℕ) (r s : D0.Role) (hrs : r ≠ s)
    (x y : ArchiveRolePhasePoint n) (hxy : rolePhaseAdjacent n x y)
    (f g : D0.archivePhaseIndex n → ℝ) (hf : f (x r)=0) (hg : g (x s)=0) :
    f (y r)*g (y s)=0 := by
  rcases hxy with ⟨a,ha,_⟩
  by_cases h : r=a
  · subst a
    rw [← ha s (Ne.symm hrs),hg,mul_zero]
  · rw [← ha r h,hf,zero_mul]

theorem actual_local_matrix_mixed_probe_zero (n : ℕ) (D : LocalLaplacianVariation n)
    (r s : D0.Role) (hrs : r ≠ s) (x : ArchiveRolePhasePoint n)
    (f g : D0.archivePhaseIndex n → ℝ) (hf : f (x r)=0) (hg : g (x s)=0) :
    (D.1 *ᵥ (fun y => f (y r)*g (y s))) x=0 := by
  change (∑ y, D.1 x y*(f (y r)*g (y s)))=0
  apply Finset.sum_eq_zero
  intro y _
  by_cases heq : x=y
  · subst y
    simp [hf]
  · by_cases hadj : rolePhaseAdjacent n x y
    · rw [mixed_profile_neighbor_zero n r s hrs x y hadj f g hf hg,mul_zero]
    · rw [D.2.2.2 x y heq hadj,zero_mul]

theorem actual_conductance_mixed_probe_zero (n : ℕ) (w : EdgeConductanceVariation n)
    (r s : D0.Role) (hrs : r ≠ s) (x : ArchiveRolePhasePoint n)
    (f g : D0.archivePhaseIndex n → ℝ) (hf : f (x r)=0) (hg : g (x s)=0) :
    (forwardMatrix n w *ᵥ (fun y => f (y r)*g (y s))) x=0 :=
  actual_local_matrix_mixed_probe_zero n (archiveLocalLaplacianForward n w) r s hrs x f g hf hg

end
end D0.Research.NativeLogdet

#print axioms D0.Research.NativeLogdet.scalarLogdet_hasDerivAt
#print axioms D0.Research.NativeLogdet.scalarLogdet_stationary_iff
#print axioms D0.Research.NativeLogdet.realProfile_cast
#print axioms D0.Research.NativeLogdet.realProfile_hasDerivAt
#print axioms D0.Research.NativeLogdet.profileEncoding_domain
#print axioms D0.Research.NativeLogdet.profileEncoding_positive_domain
#print axioms D0.Research.NativeLogdet.arbitrary_profile_exact_encoding
#print axioms D0.Research.NativeLogdet.profile_encoding_is_not_selection
#print axioms D0.Research.NativeLogdet.determinant_similarity
#print axioms D0.Research.NativeLogdet.logdet_similarity
#print axioms D0.Research.NativeLogdet.rank_two_scalar_reduction
#print axioms D0.Research.NativeLogdet.conjugation_ward
#print axioms D0.Research.NativeLogdet.edgeVector_ne_zero
#print axioms D0.Research.NativeLogdet.edge_quadratic
#print axioms D0.Research.NativeLogdet.positive_definite_edge
#print axioms D0.Research.NativeLogdet.actual_edge_readout_positive
#print axioms D0.Research.NativeLogdet.inverse_edge_source_positive
#print axioms D0.Research.NativeLogdet.full_edge_gate_impossible
#print axioms D0.Research.NativeLogdet.nonzero_coupling_edge_gate_impossible
#print axioms D0.Research.NativeLogdet.actual_role_edge_source_positive
#print axioms D0.Research.NativeLogdet.mixed_profile_neighbor_zero
#print axioms D0.Research.NativeLogdet.actual_local_matrix_mixed_probe_zero
#print axioms D0.Research.NativeLogdet.actual_conductance_mixed_probe_zero
#check D0.Matter.higgs_logdet_scalar_sector_stationary
#check D0.Matter.HiggsRadialInstabilityBoundary.higgs_radial_dynamics_maximality_nogo_owner
#check D0.Cosmology.feedback_variation_universal_source
#check D0.Research.NativeLogdet.scalarLogdet_hasDerivAt
#check D0.Research.NativeLogdet.inverse_edge_source_positive
#check D0.Research.NativeLogdet.actual_conductance_mixed_probe_zero
