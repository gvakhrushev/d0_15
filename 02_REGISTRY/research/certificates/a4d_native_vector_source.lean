import D0.Algebra.GaugeKineticPositivity
import D0.Matter.VectorOperatorOrigin
import D0.Gauge.MatrixRepGaugeTransform
import D0.Gauge.NonAbelianSeamObstructionGap
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.PiL2

/-! Literal finite vector action: first variation, source range and background
response. This research capsule does not select a physical D(g), introduce
a new native action, or identify matrix conjugation with spacetime gauge. -/
open scoped BigOperators
open D0.Algebra D0.Matter
namespace D0.Research.NativeVectorSource
noncomputable section
set_option linter.unusedSectionVars false
variable {n : Type} [Fintype n] [DecidableEq n]

def frob (X Y : Matrix n n ℝ) : ℝ := Matrix.trace (X.transpose * Y)

lemma frob_entries (X Y : Matrix n n ℝ) :
    frob X Y = ∑ i, ∑ j, X i j * Y i j := by
  unfold frob Matrix.trace Matrix.diag
  simp only [Matrix.mul_apply, Matrix.transpose_apply]
  exact Finset.sum_comm

lemma frob_symm (X Y : Matrix n n ℝ) : frob X Y = frob Y X := by
  simp only [frob_entries, mul_comm]

lemma frob_add_left (X Y Z : Matrix n n ℝ) :
    frob (X+Y) Z = frob X Z + frob Y Z := by
  simp [frob, Matrix.transpose_add, Matrix.add_mul, Matrix.trace_add]

lemma frob_add_right (X Y Z : Matrix n n ℝ) :
    frob X (Y+Z) = frob X Y + frob X Z := by
  simp [frob, Matrix.mul_add, Matrix.trace_add]

lemma frob_smul_left (t : ℝ) (X Y : Matrix n n ℝ) :
    frob (t • X) Y = t * frob X Y := by
  simp [frob, Matrix.transpose_smul, Matrix.trace_smul]

lemma frob_smul_right (t : ℝ) (X Y : Matrix n n ℝ) :
    frob X (t • Y) = t * frob X Y := by
  rw [frob_symm, frob_smul_left, frob_symm]

lemma frob_neg_right (X Y : Matrix n n ℝ) : frob X (-Y) = -frob X Y := by
  simp [frob, Matrix.trace_neg]

lemma frob_nonneg (X : Matrix n n ℝ) : 0 ≤ frob X X :=
  trace_transpose_mul_self_nonnegative X

lemma frob_eq_zero_iff (X : Matrix n n ℝ) : frob X X = 0 ↔ X=0 := by
  rw [frob_entries]
  constructor
  · intro h
    ext i j
    have hrows : ∀ i, (∑ j, X i j * X i j) = 0 := by
      exact fun i => (Finset.sum_eq_zero_iff_of_nonneg
        (fun i _ => Finset.sum_nonneg (fun j _ => mul_self_nonneg (X i j)))).mp h i
          (Finset.mem_univ i)
    have hij := (Finset.sum_eq_zero_iff_of_nonneg
      (fun j _ => mul_self_nonneg (X i j))).mp (hrows i) j (Finset.mem_univ j)
    simpa only [Matrix.zero_apply] using (mul_self_eq_zero.mp hij)
  · intro h; simp [h]

lemma comm_add_right (D A B : Matrix n n ℝ) :
    D0.Algebra.commutator D (A+B) = D0.Algebra.commutator D A + D0.Algebra.commutator D B := by
  unfold D0.Algebra.commutator
  noncomm_ring

lemma comm_smul_right (D A : Matrix n n ℝ) (t : ℝ) :
    D0.Algebra.commutator D (t • A) = t • D0.Algebra.commutator D A := by
  simp [D0.Algebra.commutator, smul_sub]

lemma comm_swap (D A : Matrix n n ℝ) : D0.Algebra.commutator D A = -D0.Algebra.commutator A D := by
  unfold D0.Algebra.commutator; abel

/-- Frobenius adjoint of ad_D is minus ad_D for the actual skew D. -/
theorem comm_adjoint (D X Y : Matrix n n ℝ) (hD : isSkew D) :
    frob X (D0.Algebra.commutator D Y) = frob (-D0.Algebra.commutator D X) Y := by
  unfold frob D0.Algebra.commutator
  unfold isSkew at hD
  simp only [Matrix.transpose_neg, Matrix.transpose_sub, Matrix.transpose_mul, hD,
    Matrix.neg_mul, Matrix.mul_neg, Matrix.mul_sub, Matrix.sub_mul, Matrix.trace_sub,
    Matrix.trace_neg]
  rw [Matrix.trace_mul_cycle' X.transpose Y D]
  simp only [Matrix.mul_assoc]
  ring

/-- The missing owner equality, not merely positivity of an unrelated square. -/
theorem literal_energy_identity (D A : Matrix n n ℝ) (hD : isSkew D) :
    frob A (vectorLaplacian D A) = frob (D0.Algebra.commutator D A) (D0.Algebra.commutator D A) := by
  unfold vectorLaplacian
  rw [frob_symm, ← comm_adjoint D (D0.Algebra.commutator D A) A hD]

theorem literal_self_adjoint (D A B : Matrix n n ℝ) (hD : isSkew D) :
    frob A (vectorLaplacian D B) = frob (vectorLaplacian D A) B := by
  unfold vectorLaplacian
  rw [← comm_adjoint D (D0.Algebra.commutator D A) B hD]
  rw [frob_symm, ← comm_adjoint D (D0.Algebra.commutator D B) A hD, frob_symm]

theorem literal_kernel (D A : Matrix n n ℝ) (hD : isSkew D) :
    vectorLaplacian D A=0 ↔ D0.Algebra.commutator D A=0 := by
  constructor
  · intro h
    apply (frob_eq_zero_iff _).mp
    rw [← literal_energy_identity D A hD, h]
    simp [frob]
  · intro h
    rw [vectorLaplacian, h]
    simp [D0.Algebra.commutator]

theorem owned_action_square (D A : Matrix n n ℝ) (c : ℝ)
    (hD : isSkew D) (hA : isSkew A) :
    gaugeKineticAction (discreteGaugeCurvature D A) c =
      c * frob (D0.Algebra.commutator D A) (D0.Algebra.commutator D A) := by
  have hK := gauge_curvature_skew D A hD hA
  change (discreteGaugeCurvature D A).transpose = -discreteGaugeCurvature D A at hK
  change -c * Matrix.trace (discreteGaugeCurvature D A * discreteGaugeCurvature D A) =
    c * frob (discreteGaugeCurvature D A) (discreteGaugeCurvature D A)
  simp [frob, hK, Matrix.trace_neg]

lemma skew_add_smul (A B : Matrix n n ℝ) (t : ℝ)
    (hA : isSkew A) (hB : isSkew B) : isSkew (A+t • B) := by
  unfold isSkew at *
  simp [Matrix.transpose_add, Matrix.transpose_smul, hA, hB, smul_neg, add_comm]

/-- Exact quadratic variation of the existing action, with coefficient retained. -/
theorem owned_action_polarization (D A B : Matrix n n ℝ) (c t : ℝ)
    (hD : isSkew D) (hA : isSkew A) (hB : isSkew B) :
    gaugeKineticAction (discreteGaugeCurvature D (A+t • B)) c =
      gaugeKineticAction (discreteGaugeCurvature D A) c +
      2*c*t*frob (vectorLaplacian D A) B +
      c*t^2*frob (D0.Algebra.commutator D B) (D0.Algebra.commutator D B) := by
  rw [owned_action_square D _ c hD (skew_add_smul A B t hA hB),
    owned_action_square D A c hD hA, comm_add_right, comm_smul_right]
  simp only [frob_add_left, frob_add_right, frob_smul_left, frob_smul_right]
  have adj := comm_adjoint D (D0.Algebra.commutator D A) B hD
  change frob (D0.Algebra.commutator D A) (D0.Algebra.commutator D B) = frob (vectorLaplacian D A) B at adj
  rw [frob_symm (D0.Algebra.commutator D B) (D0.Algebra.commutator D A), adj]
  ring

theorem owned_action_first_variation (D A B : Matrix n n ℝ) (c : ℝ)
    (hD : isSkew D) (hA : isSkew A) (hB : isSkew B) :
    HasDerivAt (fun t : ℝ => gaugeKineticAction (discreteGaugeCurvature D (A+t • B)) c)
      (2*c*frob (vectorLaplacian D A) B) 0 := by
  have hf : (fun t : ℝ => gaugeKineticAction (discreteGaugeCurvature D (A+t • B)) c) =
      (fun t : ℝ => gaugeKineticAction (discreteGaugeCurvature D A) c +
        2*c*t*frob (vectorLaplacian D A) B +
        c*t^2*frob (D0.Algebra.commutator D B) (D0.Algebra.commutator D B)) := by
    funext t; exact owned_action_polarization D A B c t hD hA hB
  rw [hf]
  convert ((hasDerivAt_const (0 : ℝ) (gaugeKineticAction (discreteGaugeCurvature D A) c)).add
    (((hasDerivAt_id (0 : ℝ)).const_mul (2*c)).mul_const (frob (vectorLaplacian D A) B))).add
    ((((hasDerivAt_id (0 : ℝ)).pow 2).const_mul c).mul_const
      (frob (D0.Algebra.commutator D B) (D0.Algebra.commutator D B))) using 1; simp [id]

/-- Native stationarity tests the actual derivative on all admitted skew directions. -/
def FreeFieldStationary (D A : Matrix n n ℝ) (c : ℝ) : Prop :=
  ∀ B, isSkew B → deriv (fun t : ℝ =>
    gaugeKineticAction (discreteGaugeCurvature D (A+t • B)) c) 0=0

theorem full_field_gate (D A : Matrix n n ℝ) (c : ℝ) (hc : c≠0)
    (hD : isSkew D) (hA : isSkew A) :
    FreeFieldStationary D A c ↔ D0.Algebra.commutator D A=0 := by
  constructor
  · intro h
    have hh := h A hA
    rw [(owned_action_first_variation D A A c hD hA hA).deriv] at hh
    rw [frob_symm, literal_energy_identity D A hD] at hh
    apply (frob_eq_zero_iff _).mp
    exact (mul_eq_zero.mp hh).resolve_left (mul_ne_zero (by norm_num) hc)
  · intro h B hB
    rw [(owned_action_first_variation D A B c hD hA hB).deriv,
      (literal_kernel D A hD).mpr h]
    simp [frob]

/-- This is a background derivative, not yet a physical metric stress. -/
def backgroundResponse (D A : Matrix n n ℝ) : Matrix n n ℝ :=
  D0.Algebra.commutator A (D0.Algebra.commutator D A)

lemma background_eq_swapped (D A : Matrix n n ℝ) :
    backgroundResponse D A = vectorLaplacian A D := by
  unfold backgroundResponse vectorLaplacian D0.Algebra.commutator
  noncomm_ring

theorem background_first_variation (D A B : Matrix n n ℝ) (c : ℝ)
    (hD : isSkew D) (hA : isSkew A) (hB : isSkew B) :
    HasDerivAt (fun t : ℝ => gaugeKineticAction (discreteGaugeCurvature (D+t • B) A) c)
      (2*c*frob (backgroundResponse D A) B) 0 := by
  have hs : ∀ X Y : Matrix n n ℝ,
      gaugeKineticAction (discreteGaugeCurvature X Y) c =
      gaugeKineticAction (discreteGaugeCurvature Y X) c := by
    intro X Y
    unfold discreteGaugeCurvature
    rw [comm_swap X Y]
    simp [gaugeKineticAction]
  simp_rw [hs (D+_ • B) A]
  have he : vectorLaplacian A D = backgroundResponse D A := by
    unfold vectorLaplacian backgroundResponse D0.Algebra.commutator
    noncomm_ring
  rw [← he]
  exact owned_action_first_variation A D B c hA hD hB

theorem unsourced_zero_response (D A : Matrix n n ℝ) (c : ℝ) (hc : c≠0)
    (hD : isSkew D) (hA : isSkew A) (h : FreeFieldStationary D A c) :
    gaugeKineticAction (discreteGaugeCurvature D A) c=0 ∧
      backgroundResponse D A=0 := by
  have hK := (full_field_gate D A c hc hD hA).mp h
  dsimp only [discreteGaugeCurvature, backgroundResponse]
  rw [hK]
  simp [gaugeKineticAction, D0.Algebra.commutator]

/-- Algebraic simultaneous-conjugation identity; not a spacetime Ward assertion. -/
theorem actual_joint_ward (D A : Matrix n n ℝ) :
    D0.Algebra.commutator D (backgroundResponse D A)+D0.Algebra.commutator A (vectorLaplacian D A)=0 := by
  unfold backgroundResponse vectorLaplacian D0.Algebra.commutator
  noncomm_ring

theorem sourced_ward (D A J : Matrix n n ℝ) (h : vectorLaplacian D A=J) :
    D0.Algebra.commutator D (backgroundResponse D A)+D0.Algebra.commutator A J=0 := by
  rw [← h]
  exact actual_joint_ward D A

theorem necessary_source_compatibility (D A J B : Matrix n n ℝ)
    (hD : isSkew D) (h : vectorLaplacian D A=J) (hB : D0.Algebra.commutator D B=0) :
    frob J B=0 := by
  rw [← h, ← literal_self_adjoint D A B hD, (literal_kernel D B hD).mpr hB]
  simp [frob]

theorem solutions_differ_by_commutant (D A B : Matrix n n ℝ) (hD : isSkew D) :
    vectorLaplacian D A=vectorLaplacian D B ↔ D0.Algebra.commutator D (A-B)=0 := by
  have hsub : vectorLaplacian D (A-B) = vectorLaplacian D A-vectorLaplacian D B := by
    unfold vectorLaplacian D0.Algebra.commutator
    noncomm_ring
  rw [← literal_kernel D (A-B) hD, hsub, sub_eq_zero]

def asMatrix (v : EuclideanSpace ℝ (n × n)) : Matrix n n ℝ := fun i j => v (i,j)

def skewCarrier (m : Type) [Fintype m] : Submodule ℝ (EuclideanSpace ℝ (m × m)) where
  carrier := {v | isSkew (asMatrix v)}
  zero_mem' := by
    change (0 : Matrix m m ℝ).transpose = -0
    simp
  add_mem' := by
    intro x y hx hy
    change isSkew (asMatrix x) at hx
    change isSkew (asMatrix y) at hy
    change isSkew (asMatrix x + asMatrix y)
    unfold isSkew at *
    simp [Matrix.transpose_add, hx, hy, add_comm]
  smul_mem' := by
    intro t x hx
    change isSkew (asMatrix x) at hx
    change isSkew (t • asMatrix x)
    unfold isSkew at *
    simp [Matrix.transpose_smul, hx]

def skewVec (A : Matrix n n ℝ) (hA : isSkew A) : skewCarrier n :=
  ⟨WithLp.toLp 2 (fun p => A p.1 p.2), hA⟩

def vectorMap (D : Matrix n n ℝ) (hD : isSkew D) :
    skewCarrier n →ₗ[ℝ] skewCarrier n where
  toFun v := skewVec (vectorLaplacian D (asMatrix v.val))
    (vector_laplacian_preserves_skew D (asMatrix v.val) hD v.property)
  map_add' x y := by
    have h : vectorLaplacian D (asMatrix x.val+asMatrix y.val) =
        vectorLaplacian D (asMatrix x.val)+vectorLaplacian D (asMatrix y.val) := by
      unfold vectorLaplacian D0.Algebra.commutator
      noncomm_ring
    apply Subtype.ext
    ext p
    exact congrFun (congrFun h p.1) p.2
  map_smul' t x := by
    apply Subtype.ext
    ext p
    change vectorLaplacian D (t • asMatrix x.val) p.1 p.2 =
      (t • vectorLaplacian D (asMatrix x.val)) p.1 p.2
    simp only [vectorLaplacian, comm_smul_right, smul_neg]

lemma skew_inner (x y : skewCarrier n) :
    inner ℝ x y = frob (asMatrix x.val) (asMatrix y.val) := by
  rw [Submodule.coe_inner, PiLp.inner_apply, frob_entries]
  simp [asMatrix, Fintype.sum_prod_type, RCLike.inner_apply, mul_comm]

theorem actual_range_orthogonal_kernel (D : Matrix n n ℝ) (hD : isSkew D) :
    (vectorMap D hD).range = (vectorMap D hD).kerᗮ := by
  have hs : (vectorMap D hD).IsSymmetric := by
    intro x y
    rw [skew_inner, skew_inner]
    exact (literal_self_adjoint D (asMatrix x.val) (asMatrix y.val) hD).symm
  rw [LinearMap.orthogonal_ker, hs.adjoint_eq]

/-- Full finite Fredholm alternative on the actual skew state space. -/
theorem source_solvable_iff (D J : Matrix n n ℝ) (hD : isSkew D) (hJ : isSkew J) :
    (∃ A, isSkew A ∧ vectorLaplacian D A=J) ↔
      ∀ B, isSkew B → D0.Algebra.commutator D B=0 → frob J B=0 := by
  constructor
  · rintro ⟨A, _, hA⟩ B _ hB
    exact necessary_source_compatibility D A J B hD hA hB
  · intro h
    have horth : skewVec J hJ ∈ (vectorMap D hD).kerᗮ := by
      rw [Submodule.mem_orthogonal']
      intro b hb
      rw [skew_inner]
      change frob J (asMatrix b.val)=0
      apply h _ b.property
      apply (literal_kernel D _ hD).mp
      have hv : vectorMap D hD b=0 := hb
      ext i j
      exact congrArg (fun z : skewCarrier n => asMatrix z.val i j) hv
    rw [← actual_range_orthogonal_kernel D hD] at horth
    obtain ⟨a,ha⟩ := horth
    refine ⟨asMatrix a.val, a.property, ?_⟩
    ext i j
    exact congrArg (fun z : skewCarrier n => asMatrix z.val i j) ha

/-- The zero field has no conjugation tangent, while D is a kernel direction.
Nonzero D therefore cannot be removed from this kernel by calling it gauge. -/
theorem kernel_direction_at_zero (D X : Matrix n n ℝ) :
    vectorLaplacian D D=0 ∧ D0.Algebra.commutator X (0 : Matrix n n ℝ)=0 := by
  simp [vectorLaplacian, D0.Algebra.commutator]

/-- A supplied nonzero current cannot be balanced if D too is freely varied
and this action is the sole source of its equation. -/
theorem full_background_gate_rejects_nonzero_current (D A J : Matrix n n ℝ)
    (hA : isSkew A) (hfield : vectorLaplacian D A=J)
    (hback : backgroundResponse D A=0) : J=0 := by
  rw [background_eq_swapped] at hback
  have hK := (literal_kernel A D hA).mp hback
  have hK' : D0.Algebra.commutator D A=0 := by rw [comm_swap, hK, neg_zero]
  rw [← hfield, vectorLaplacian, hK']
  simp [D0.Algebra.commutator]

/-- Kernel shifts preserve the sourced field equation but need not preserve
the full background response. Only admissible preparation tangents may be
used when differentiating a reduced action value. -/
theorem background_kernel_shift (D A Z : Matrix n n ℝ)
    (hZ : D0.Algebra.commutator D Z=0) :
    backgroundResponse D (A+Z) = backgroundResponse D A+
      D0.Algebra.commutator Z (D0.Algebra.commutator D A) := by
  unfold backgroundResponse
  rw [comm_add_right, hZ, add_zero]
  unfold D0.Algebra.commutator
  noncomm_ring

/-- The existing source equation uses c=1/2. This binds its stationarity
premise to the derivative, without claiming ownership of the supplied J. -/
theorem supplied_source_gate (D A J : Matrix n n ℝ)
    (hD : isSkew D) (hA : isSkew A) (hJ : isSkew J) :
    (∀ B, isSkew B →
      deriv (fun t : ℝ => gaugeKineticAction (discreteGaugeCurvature D (A+t • B)) (1/2)) 0
        = frob J B) ↔ vectorLaplacian D A=J := by
  constructor
  · intro h
    apply vector_operator_origin_applies_to_field_equation D A J hD hA hJ
    intro B hB
    have hh := h B hB
    rw [(owned_action_first_variation D A B (1/2) hD hA hB).deriv] at hh
    norm_num at hh
    change frob B (vectorLaplacian D A-J)=0
    simp only [frob, Matrix.mul_sub, Matrix.trace_sub] at hh ⊢
    rw [← show Matrix.trace (J.transpose*B)=Matrix.trace (B.transpose*J) from frob_symm J B,
      ← show Matrix.trace ((vectorLaplacian D A).transpose*B)=
        Matrix.trace (B.transpose*vectorLaplacian D A) from frob_symm _ B]
    linarith
  · intro h B hB
    rw [(owned_action_first_variation D A B (1/2) hD hA hB).deriv, h]
    norm_num

end
end D0.Research.NativeVectorSource

#print axioms D0.Research.NativeVectorSource.comm_adjoint
#print axioms D0.Research.NativeVectorSource.literal_energy_identity
#print axioms D0.Research.NativeVectorSource.literal_self_adjoint
#print axioms D0.Research.NativeVectorSource.literal_kernel
#print axioms D0.Research.NativeVectorSource.owned_action_square
#print axioms D0.Research.NativeVectorSource.owned_action_polarization
#print axioms D0.Research.NativeVectorSource.owned_action_first_variation
#print axioms D0.Research.NativeVectorSource.full_field_gate
#print axioms D0.Research.NativeVectorSource.background_first_variation
#print axioms D0.Research.NativeVectorSource.unsourced_zero_response
#print axioms D0.Research.NativeVectorSource.actual_joint_ward
#print axioms D0.Research.NativeVectorSource.sourced_ward
#print axioms D0.Research.NativeVectorSource.necessary_source_compatibility
#print axioms D0.Research.NativeVectorSource.solutions_differ_by_commutant
#print axioms D0.Research.NativeVectorSource.actual_range_orthogonal_kernel
#print axioms D0.Research.NativeVectorSource.source_solvable_iff
#print axioms D0.Research.NativeVectorSource.kernel_direction_at_zero
#print axioms D0.Research.NativeVectorSource.full_background_gate_rejects_nonzero_current
#print axioms D0.Research.NativeVectorSource.background_kernel_shift
#print axioms D0.Research.NativeVectorSource.supplied_source_gate

#check D0.Research.NativeVectorSource.owned_action_first_variation
#check D0.Research.NativeVectorSource.full_field_gate
#check D0.Research.NativeVectorSource.background_first_variation
#check D0.Research.NativeVectorSource.actual_joint_ward
#check D0.Research.NativeVectorSource.source_solvable_iff
#check D0.Research.NativeVectorSource.full_background_gate_rejects_nonzero_current
#check D0.Research.NativeVectorSource.background_kernel_shift
#check D0.Research.NativeVectorSource.supplied_source_gate
