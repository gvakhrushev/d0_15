import D0.Geometry.A4DStarFiniteLorentzQuotient
import D0.Geometry.ArchiveAffineExteriorLink
import Mathlib.Analysis.Calculus.Deriv.Add

/-! Research consumer of the actual nondegenerate raw-solder, Lorentz-link
and exterior-matter owners. No field action or physical admission is added. -/
namespace D0.Research.NativeJointFieldQuotient
open D0 D0.Geometry
open scoped BigOperators
noncomputable section
abbrev Mat := Matrix Role Role ℝ

def gram (F : Mat) : Mat := F*roleLorentzMetric*F.transpose

theorem same_gram_relative_frame (F G : Mat) (hF : IsUnit F.det)
    (h : gram F=gram G) : IsRoleLorentz (F⁻¹*G) := by
  change F*roleLorentzMetric*F.transpose=G*roleLorentzMetric*G.transpose at h
  have hi : F⁻¹*F=1 := Matrix.nonsing_inv_mul F hF
  change (F⁻¹*G)*roleLorentzMetric*(F⁻¹*G).transpose=roleLorentzMetric
  calc
    (F⁻¹*G)*roleLorentzMetric*(F⁻¹*G).transpose =
        F⁻¹*(G*roleLorentzMetric*G.transpose)*F⁻¹.transpose := by
          simp only [Matrix.transpose_mul,Matrix.mul_assoc]
    _ = F⁻¹*(F*roleLorentzMetric*F.transpose)*F⁻¹.transpose := by rw [←h]
    _ = (F⁻¹*F)*roleLorentzMetric*(F⁻¹*F).transpose := by
          simp only [Matrix.transpose_mul,Matrix.mul_assoc]
    _ = roleLorentzMetric := by rw [hi]; simp

theorem frame_reconstructs (F G : Mat) (hF : IsUnit F.det) :
    F*(F⁻¹*G)=G := by
  rw [←Matrix.mul_assoc,Matrix.mul_nonsing_inv F hF,Matrix.one_mul]

theorem unique_relative_frame (F G Λ : Mat) (hF : IsUnit F.det)
    (h : F*Λ=G) : Λ=F⁻¹*G := by
  rw [←h,←Matrix.mul_assoc,Matrix.nonsing_inv_mul F hF,Matrix.one_mul]

theorem dressed_reconstruct (Fx Fy U : Mat) (hx : IsUnit Fx.det) (hy : IsUnit Fy.det) :
    Fx⁻¹*a4dDressedLink Fx U Fy*Fy=U := by
  unfold a4dDressedLink
  calc
    Fx⁻¹*(Fx*U*Fy⁻¹)*Fy=(Fx⁻¹*Fx)*U*(Fy⁻¹*Fy) := by simp only [Matrix.mul_assoc]
    _ = U := by rw [Matrix.nonsing_inv_mul Fx hx,Matrix.nonsing_inv_mul Fy hy]; simp

theorem dressed_metric_compatibility (Fx Fy U : Mat) (hy : IsUnit Fy.det)
    (hU : IsRoleLorentz U) :
    a4dDressedLink Fx U Fy*gram Fy*(a4dDressedLink Fx U Fy).transpose=gram Fx := by
  have hi := Matrix.nonsing_inv_mul Fy hy
  change U*roleLorentzMetric*U.transpose=roleLorentzMetric at hU
  unfold a4dDressedLink gram
  calc
    (Fx*U*Fy⁻¹)*(Fy*roleLorentzMetric*Fy.transpose)*(Fx*U*Fy⁻¹).transpose =
      Fx*U*(Fy⁻¹*Fy)*roleLorentzMetric*(Fy⁻¹*Fy).transpose*U.transpose*Fx.transpose := by
        simp only [Matrix.transpose_mul,Matrix.mul_assoc]
    _ = Fx*roleLorentzMetric*Fx.transpose := by
      rw [hi];simp only [Matrix.mul_one,Matrix.transpose_one]
      simpa only [Matrix.mul_assoc] using congrArg (fun X => Fx*X*Fx.transpose) hU

theorem same_dressed_group_iff {G : Type*} [Group G] (F P H Q U V : G) :
    F*U*P⁻¹=H*V*Q⁻¹ ↔ V=(F⁻¹*H)⁻¹*U*(P⁻¹*Q) := by
  constructor
  · intro h
    have hh := congrArg (fun z => H⁻¹*z*Q) h
    dsimp only at hh
    have hright : H⁻¹*(H*V*Q⁻¹)*Q=V := by group
    rw [hright] at hh
    calc
      V=H⁻¹*(F*U*P⁻¹)*Q := hh.symm
      _ = (F⁻¹*H)⁻¹*U*(P⁻¹*Q) := by group
  · intro h
    rw [h]
    group

theorem same_vector_reading_iff (F G : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (v w : RoleSpace) : F v=G w ↔ w=G.symm (F v) := by
  constructor
  · intro h
    rw [h,LinearEquiv.symm_apply_apply]
  · intro h
    rw [h,LinearEquiv.apply_symm_apply]

def exteriorEquiv (F : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ) where
  toLinearMap := archiveExteriorFrameLift F
  invFun := archiveExteriorFrameLift F.symm
  left_inv ψ := by
    have h := congrArg (fun L => L ψ) (archiveExteriorFrameLift_inverse F).2
    exact h
  right_inv ψ := by
    have h := congrArg (fun L => L ψ) (archiveExteriorFrameLift_inverse F).1
    exact h

theorem exterior_matter_complete (F G : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (ψ χ : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift F ψ=archiveExteriorFrameLift G χ ↔
      χ=archiveExteriorFrameLift G.symm (archiveExteriorFrameLift F ψ) := by
  constructor
  · intro h
    have hh := congrArg (archiveExteriorFrameLift G.symm) h
    have hi := (exteriorEquiv G).left_inv χ
    change archiveExteriorFrameLift G.symm (archiveExteriorFrameLift G χ)=χ at hi
    rw [hi] at hh
    exact hh.symm
  · intro h
    rw [h]
    exact ((exteriorEquiv G).right_inv (archiveExteriorFrameLift F ψ)).symm

theorem exterior_comp_is_native (F G : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift (G.trans F) ψ=
      archiveExteriorFrameLift F (archiveExteriorFrameLift G ψ) := by
  exact congrArg (fun L => L ψ) (archiveExteriorFrameLift_comp F G).symm

def incomingRows {N : ℕ} (D : A4DLinearLinkField N)
    (x : ArchiveRolePhaseGroup N) : Mat :=
  fun r a => D (roleTranslateMinus N r x) r r a

def centerFactor {N : ℕ} (D : A4DLinearLinkField N)
    (x : ArchiveRolePhaseGroup N) : Mat := (1/2:ℝ) • (1+incomingRows D x)

def dressedField {N : ℕ} (F : ArchiveRolePhaseGroup N → Mat)
    (U : A4DLinearLinkField N) : A4DLinearLinkField N :=
  fun x r => a4dDressedLink (F x) (U x r) (F (roleTranslatePlus N r x))

theorem dressed_times_target (Fx Fy U : Mat) (hy : IsUnit Fy.det) :
    a4dDressedLink Fx U Fy*Fy=Fx*U := by
  unfold a4dDressedLink
  rw [Matrix.mul_assoc,Matrix.nonsing_inv_mul Fy hy,Matrix.mul_one]

theorem transported_center_factorization {N : ℕ}
    (F : ArchiveRolePhaseGroup N → Mat) (U : A4DLinearLinkField N)
    (x : ArchiveRolePhaseGroup N) (hx : IsUnit (F x).det) :
    transportedSolderCenter N F U x=centerFactor (dressedField F U) x*F x := by
  have hrow (r : Role) :
      dressedField F U (roleTranslateMinus N r x) r*F x=
        F (roleTranslateMinus N r x)*U (roleTranslateMinus N r x) r := by
    simp only [dressedField,roleTranslate_inverse_plus]
    exact dressed_times_target _ _ _ hx
  rw [centerFactor,Matrix.smul_mul,Matrix.add_mul,Matrix.one_mul]
  ext r a
  have hp : (incomingRows (dressedField F U) x*F x) r a=
      (F (roleTranslateMinus N r x)*U (roleTranslateMinus N r x) r) r a := by
    simpa only [Matrix.mul_apply,incomingRows] using
      congrArg (fun M : Mat => M r a) (hrow r)
  simp only [transportedSolderCenter,Matrix.smul_apply,smul_eq_mul,Matrix.add_apply]
  rw [hp]
  ring

theorem transported_gram_factorization {N : ℕ}
    (F : ArchiveRolePhaseGroup N → Mat) (U : A4DLinearLinkField N)
    (x : ArchiveRolePhaseGroup N) (hx : IsUnit (F x).det) :
    gram (transportedSolderCenter N F U x)=
      centerFactor (dressedField F U) x*gram (F x)*(centerFactor (dressedField F U) x).transpose := by
  rw [transported_center_factorization F U x hx]
  simp only [gram,Matrix.transpose_mul,Matrix.mul_assoc]

def constraintExtension (source target d : ℝ) : ℝ := d*d*target-source

theorem ambient_source_derivative (source target d : ℝ) :
    HasDerivAt (fun x => constraintExtension x target d) (-1) source := by
  simpa only [constraintExtension,zero_sub] using
    (hasDerivAt_const source (d*d*target)).sub (hasDerivAt_id source)

theorem constrained_extension_identically_zero (d : ℝ) :
    (fun q => constraintExtension (d*d*q) q d)=(fun _ : ℝ => 0) := by
  funext q
  simp [constraintExtension]

theorem constrained_source_derivative_zero (d q : ℝ) :
    HasDerivAt (fun t => constraintExtension (d*d*t) t d) 0 q := by
  rw [constrained_extension_identically_zero]
  exact hasDerivAt_const q 0

end
end D0.Research.NativeJointFieldQuotient

#print axioms D0.Research.NativeJointFieldQuotient.same_gram_relative_frame
#print axioms D0.Research.NativeJointFieldQuotient.frame_reconstructs
#print axioms D0.Research.NativeJointFieldQuotient.unique_relative_frame
#print axioms D0.Research.NativeJointFieldQuotient.dressed_reconstruct
#print axioms D0.Research.NativeJointFieldQuotient.dressed_metric_compatibility
#print axioms D0.Research.NativeJointFieldQuotient.same_dressed_group_iff
#print axioms D0.Research.NativeJointFieldQuotient.same_vector_reading_iff
#print axioms D0.Research.NativeJointFieldQuotient.exterior_matter_complete
#print axioms D0.Research.NativeJointFieldQuotient.exterior_comp_is_native
#print axioms D0.Research.NativeJointFieldQuotient.dressed_times_target
#print axioms D0.Research.NativeJointFieldQuotient.transported_center_factorization
#print axioms D0.Research.NativeJointFieldQuotient.transported_gram_factorization
#print axioms D0.Research.NativeJointFieldQuotient.ambient_source_derivative
#print axioms D0.Research.NativeJointFieldQuotient.constrained_extension_identically_zero
#print axioms D0.Research.NativeJointFieldQuotient.constrained_source_derivative_zero
