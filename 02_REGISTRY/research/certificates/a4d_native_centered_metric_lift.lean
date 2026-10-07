import D0.Geometry.A4DRawSolderFrameAction
import D0.Geometry.A4DMetricStressInterface
import D0.Geometry.A4DDiscreteEnergyKernel

/-! Research capsule for the actual centered metric map.
The companion proof distinguishes the analytical Fourier/smooth-limit results
from these compiled owner bindings. No physical field equation is assumed.
-/
open scoped BigOperators
open D0 D0.Geometry

namespace D0.Research.NativeCenteredMetricLift
noncomputable section

 theorem average_kernel_iff (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    backwardAverage N r f = 0 ↔
      ∀ x, f (roleTranslateMinus N r x) = -f x := by
  constructor
  · intro h x
    have hx := congrFun h x
    simp only [backwardAverage_apply, Pi.zero_apply] at hx
    linarith
  · intro h
    funext x
    simp [backwardAverage, h x]

 theorem actual_average_adjoint (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    (∑ x, backwardAverage N r f x * g x) =
      ∑ x, f x * ((g x + g (roleTranslatePlus N r x))/2) := by
  have hs : (∑ x, f (roleTranslateMinus N r x) * g x) =
      ∑ x, f x * g (roleTranslatePlus N r x) := by
    have h := sum_translate N (roleStep N r)
      (fun x => f (x-roleStep N r) * g x)
    simpa only [roleTranslateMinus_apply, roleTranslatePlus_apply, add_sub_cancel_right]
      using h.symm
  calc
    (∑ x, backwardAverage N r f x * g x) =
        ((∑ x, f x*g x) + (∑ x, f (roleTranslateMinus N r x)*g x))/2 := by
      simp only [backwardAverage_apply, div_mul_eq_mul_div, add_mul]
      rw [← Finset.sum_div, Finset.sum_add_distrib]
    _ = ((∑ x, f x*g x)+(∑ x, f x*g (roleTranslatePlus N r x)))/2 := by rw [hs]
    _ = ∑ x, f x * ((g x + g (roleTranslatePlus N r x))/2) := by
      symm
      calc
        _ = ∑ x, (f x*g x+f x*g (roleTranslatePlus N r x))/2 := by
          apply Finset.sum_congr rfl
          intro x _
          ring
        _ = _ := by rw [← Finset.sum_div, Finset.sum_add_distrib]

 theorem actual_centered_add (N : ℕ) (e v : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N (e+v) x =
      centeredCoframeMatrix N e x + centeredCoframeMatrix N v x := by
  ext r a
  simp [centeredCoframeMatrix, backwardAverage]
  ring

 theorem actual_centered_raw_solder (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    solderMatrix N e x r a =
      (rawSolderMatrix N e x r a +
        rawSolderMatrix N e (roleTranslateMinus N r x) r a)/2 := by
  simp [solderMatrix, centeredCoframeMatrix, backwardAverage, rawSolderMatrix]
  ring

 def gram (Theta : Matrix Role Role ℝ) :=
  Theta * roleLorentzMetric * Theta.transpose
 def gramDerivative (Theta H : Matrix Role Role ℝ) :=
  H * roleLorentzMetric * Theta.transpose + Theta * roleLorentzMetric * H.transpose

 theorem actual_gram_binding (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N e x = gram (solderMatrix N e x) := rfl

 theorem gram_polynomial (Theta H : Matrix Role Role ℝ) (t : ℝ) :
    gram (Theta+t • H) = gram Theta + t • gramDerivative Theta H +
      t^2 • gram H := by
  simp only [gram, gramDerivative, Matrix.transpose_add, Matrix.transpose_smul,
    Matrix.add_mul, Matrix.mul_add, Matrix.smul_mul, Matrix.mul_smul,
    smul_add, smul_smul, pow_two]
  abel

 theorem actual_metric_polynomial (N : ℕ) (e v : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (t : ℝ) :
    solderMetricMatrix N (e+t • v) x = solderMetricMatrix N e x +
      t • gramDerivative (solderMatrix N e x) (centeredCoframeMatrix N v x) +
      t^2 • gram (centeredCoframeMatrix N v x) := by
  have hs : solderMatrix N (e+t • v) x =
      solderMatrix N e x + t • centeredCoframeMatrix N v x := by
    simp [solderMatrix, actual_centered_add, centeredCoframeMatrix_smul, add_assoc]
  simp only [actual_gram_binding, hs]
  exact gram_polynomial _ _ _

 theorem centering_kernel_keeps_metric (N : ℕ) (e n : LocalCoframeField N)
    (hn : ∀ x, centeredCoframeMatrix N n x = 0) :
    solderMetricMatrix N (e+n) = solderMetricMatrix N e := by
  funext x
  simp [solderMetricMatrix, solderMatrix, actual_centered_add, hn x]

 def rawScale (N : ℕ) (e : LocalCoframeField N) (c : ℝ) : LocalCoframeField N :=
  fun x r a => c*rawSolderMatrix N e x r a-roleLorentzMetric r a

 theorem actual_solder_raw_scale (N : ℕ) (e : LocalCoframeField N)
    (c : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMatrix N (rawScale N e c) x=c • solderMatrix N e x := by
  ext r a
  simp [solderMatrix, centeredCoframeMatrix, backwardAverage, rawScale, rawSolderMatrix]
  ring

 theorem actual_metric_raw_scale (N : ℕ) (e : LocalCoframeField N)
    (c : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (rawScale N e c) x=c^2 • solderMetricMatrix N e x := by
  simp only [solderMetricMatrix, actual_solder_raw_scale, Matrix.transpose_smul,
    Matrix.smul_mul, Matrix.mul_smul, smul_smul, pow_two]

 def pointwiseMetricLift (K V : Matrix Role Role ℝ) :=
  (1/2:ℝ) • (V*K*roleLorentzMetric)

 theorem pointwise_all_symmetric_lift (Theta K V : Matrix Role Role ℝ)
    (hK : K*Theta.transpose=1) (hV : V.transpose=V) :
    gramDerivative Theta (pointwiseMetricLift K V)=V := by
  have hKT : Theta*K.transpose=1 := by
    simpa only [Matrix.transpose_mul, Matrix.transpose_transpose, Matrix.transpose_one]
      using congrArg Matrix.transpose hK
  have hleft : (V*K*roleLorentzMetric)*roleLorentzMetric*Theta.transpose=V := by
    rw [Matrix.mul_assoc (V*K) roleLorentzMetric roleLorentzMetric,
      roleLorentzMetric_sq, Matrix.mul_one, Matrix.mul_assoc, hK, Matrix.mul_one]
  have hright : Theta*roleLorentzMetric*(V*K*roleLorentzMetric).transpose=V := by
    simp only [Matrix.transpose_mul, roleLorentzMetric_transpose, hV]
    calc
      Theta*roleLorentzMetric*(roleLorentzMetric*(K.transpose*V)) =
          (Theta*(roleLorentzMetric*roleLorentzMetric))*K.transpose*V := by
            simp only [Matrix.mul_assoc]
      _ = V := by rw [roleLorentzMetric_sq, Matrix.mul_one, hKT, Matrix.one_mul]
  simp only [gramDerivative, pointwiseMetricLift, Matrix.smul_mul,
    Matrix.transpose_smul, Matrix.mul_smul, hleft, hright]
  ext r s
  simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]
  ring

 theorem gram_product (B T : Matrix Role Role ℝ) :
    gram (B*T)=B*gram T*B.transpose := by
  simp only [gram, Matrix.transpose_mul, Matrix.mul_assoc]

 theorem gram_fiber_lorentz_iff (Theta K Other : Matrix Role Role ℝ)
    (hleft : K*Theta=1) (hright : Theta*K=1) :
    gram Other=gram Theta ↔ IsRoleLorentz (K*Other) := by
  constructor
  · intro h
    change gram (K*Other)=roleLorentzMetric
    rw [gram_product,h,← gram_product,hleft]
    simp [gram]
  · intro h
    have hprod : Theta*(K*Other)=Other := by rw [← Matrix.mul_assoc,hright,Matrix.one_mul]
    rw [← hprod]
    exact solderGram_right_lorentz_invariant Theta (K*Other) h

 theorem gram_fiber_parametrization (Theta K Other : Matrix Role Role ℝ)
    (hleft : K*Theta=1) (hright : Theta*K=1) :
    gram Other=gram Theta ↔
      ∃ Lambda, IsRoleLorentz Lambda ∧ Other=Theta*Lambda := by
  constructor
  · intro h
    refine ⟨K*Other,(gram_fiber_lorentz_iff Theta K Other hleft hright).mp h,?_⟩
    rw [← Matrix.mul_assoc,hright,Matrix.one_mul]
  · rintro ⟨Lambda,hL,rfl⟩
    exact solderGram_right_lorentz_invariant Theta Lambda hL

 theorem frame_tangent_kills_gram (Theta a : Matrix Role Role ℝ)
    (ha : IsRoleLorentzTangent a) : gramDerivative Theta (Theta*a)=0 := by
  have h := lorentzTangent_right_condition a ha
  calc
    gramDerivative Theta (Theta*a) =
        Theta*(a*roleLorentzMetric+roleLorentzMetric*a.transpose)*Theta.transpose := by
      simp only [gramDerivative, Matrix.transpose_mul, Matrix.mul_add,
        Matrix.add_mul, Matrix.mul_assoc]
    _ = 0 := by rw [h]; simp

 theorem literal_zero_field_euler (N : ℕ) (e : LocalCoframeField N) :
    (0 : ArchiveCochain N)+flatStaggeredH N e 0=0 ∧
    (∀ v : LocalCoframeField N, cochainPairing N 0 (flatStaggeredH N v 0)=0) ∧
    fluxEnergy N e 0=0 := by
  have hh : flatStaggeredH N e 0=0 := by rw [← fluxHMatrix_apply]; simp
  refine ⟨?_,?_,?_⟩
  · simp [hh]
  · intro v; simp [cochainPairing]
  · simp [fluxEnergy]

 theorem flat_field_gate_iff (N : ℕ) (psi : ArchiveCochain N) :
    psi+flatStaggeredH N 0 psi=0 ↔ psi=0 := by
  rw [flatStaggeredH_zero]
  simp

#print axioms average_kernel_iff
#print axioms actual_average_adjoint
#print axioms actual_centered_add
#print axioms actual_centered_raw_solder
#print axioms actual_gram_binding
#print axioms gram_polynomial
#print axioms actual_metric_polynomial
#print axioms centering_kernel_keeps_metric
#print axioms actual_solder_raw_scale
#print axioms actual_metric_raw_scale
#print axioms pointwise_all_symmetric_lift
#print axioms gram_product
#print axioms gram_fiber_lorentz_iff
#print axioms gram_fiber_parametrization
#print axioms frame_tangent_kills_gram
#print axioms literal_zero_field_euler
#print axioms flat_field_gate_iff
#print axioms D0.Geometry.rawNyquist_is_not_centered_data
#print axioms D0.Geometry.symFrobenius_factor_two
#check D0.Geometry.solderMetricMatrix
#check D0.Geometry.coframeMetricReadout
#check D0.Geometry.fluxEnergy
#check D0.Geometry.rawNyquist_is_not_centered_data
#check D0.Geometry.centeredNyquist_nonzero_H_oneForm

end
end D0.Research.NativeCenteredMetricLift
