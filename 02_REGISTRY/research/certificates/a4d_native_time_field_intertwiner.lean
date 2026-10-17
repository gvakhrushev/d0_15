import D0.Dynamics.TwoTickSymplectic
import D0.Core.FixedDetectorTimeLadder
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.Calculus.FDeriv.Linear

/-! The complete regular readout boundary for the owned two-tick operator
and the existing common-parent transfer family. No field preparation,
action, time identification or spatial refinement is installed. -/
namespace D0.Research.NativeTimeFieldIntertwiner
noncomputable section
open D0.Dynamics

section Algebra
variable {E F : Type*} [AddCommGroup E] [Module ℝ E]
  [AddCommGroup F] [Module ℝ F]

def nativeStep (z : E × E) : E × E :=
  (z.1-z.2, -z.1+(2:ℝ) • z.2)

def nativeInverse (z : E × E) : E × E :=
  ((2:ℝ) • z.1+z.2, z.1+z.2)

def parentStep (A : F →ₗ[ℝ] F) (z : F × F) : F × F :=
  (z.1-z.2, -z.1+A z.1+(2:ℝ) • z.2-A z.2)

def parentInverse (A : F →ₗ[ℝ] F) (z : F × F) : F × F :=
  ((2:ℝ) • z.1-A z.1+z.2, z.1-A z.1+z.2)

theorem native_inverse_right (z : E × E) : nativeStep (nativeInverse z)=z := by
  ext <;> simp [nativeStep,nativeInverse] <;> module

theorem native_inverse_left (z : E × E) : nativeInverse (nativeStep z)=z := by
  ext <;> simp [nativeStep,nativeInverse] <;> module

theorem native_quadratic (z : E × E) :
    nativeStep (nativeStep z)-(3:ℝ) • nativeStep z+z=0 := by
  ext <;> simp [nativeStep] <;> module

theorem parent_inverse_right (A : F →ₗ[ℝ] F) (z : F × F) :
    parentStep A (parentInverse A z)=z := by
  ext <;> simp [parentStep,parentInverse] <;> module

theorem parent_inverse_left (A : F →ₗ[ℝ] F) (z : F × F) :
    parentInverse A (parentStep A z)=z := by
  ext <;> simp [parentStep,parentInverse] <;> module

/-- The block characteristic defect is exactly minus A times the transfer. -/
theorem parent_quadratic_defect (A : F →ₗ[ℝ] F) (z : F × F) :
    parentStep A (parentStep A z)-(3:ℝ) • parentStep A z+z =
      (-A (parentStep A z).1,-A (parentStep A z).2) := by
  ext <;> simp [parentStep] <;> module

def Intertwines (A : F →ₗ[ℝ] F) (P : (E × E) →ₗ[ℝ] (F × F)) : Prop :=
  ∀ z, parentStep A (P z)=P (nativeStep z)

/-- No self-adjointness or chosen eigenbasis is assumed. -/
theorem intertwiner_range_in_kernel (A : F →ₗ[ℝ] F)
    (P : (E × E) →ₗ[ℝ] (F × F)) (h : Intertwines A P) (z : E × E) :
    A (P z).1=0 ∧ A (P z).2=0 := by
  have hz (w : E × E) :
      parentStep A (parentStep A (P w))-(3:ℝ) • parentStep A (P w)+P w=0 := by
    rw [h w,h (nativeStep w),← map_smul,← map_sub,← map_add,native_quadratic,map_zero]
  have hh := hz (nativeInverse z)
  rw [parent_quadratic_defect,h (nativeInverse z),native_inverse_right] at hh
  constructor
  · have := congrArg Prod.fst hh
    simpa using this
  · have := congrArg Prod.snd hh
    simpa using this

def reading (U V : E →ₗ[ℝ] F) (z : E × E) : F × F :=
  (U z.1+V z.2,V z.1+U z.2-V z.2)

/-- Completeness, including all response-null directions, not only examples. -/
theorem complete_linear_readout (A : F →ₗ[ℝ] F)
    (P : (E × E) →ₗ[ℝ] (F × F)) :
    Intertwines A P ↔ ∃ U V : E →ₗ[ℝ] F,
      (∀ x, A (U x)=0) ∧ (∀ x, A (V x)=0) ∧ ∀ z, P z=reading U V z := by
  constructor
  · intro h
    let U := (LinearMap.fst ℝ F F).comp (P.comp (LinearMap.inl ℝ E E))
    let V := (LinearMap.fst ℝ F F).comp (P.comp (LinearMap.inr ℝ E E))
    have hu (x : E) : U x=(P (x,0)).1 := rfl
    have hv (x : E) : V x=(P (0,x)).1 := rfl
    refine ⟨U,V,?_,?_,?_⟩
    · intro x
      exact (intertwiner_range_in_kernel A P h (x,0)).1
    · intro x
      exact (intertwiner_range_in_kernel A P h (0,x)).1
    · intro z
      have split (x y : E) : P (x,y)=P (x,0)+P (0,y) := by
        rw [← map_add]
        congr 1
        ext <;> simp
      have hw (x : E) : (P (x,0)).2=V x := by
        have ht := congrArg Prod.fst (h (x,0))
        have hp : P (x,-x)=P (x,0)-P (0,x) := by
          rw [← map_sub]
          congr 1
          ext <;> simp
        have hh : U x-(P (x,0)).2=U x-V x := by
          simpa [nativeStep,parentStep,hp,← hu,← hv] using ht
        exact sub_right_inj.mp hh
      have hx (x : E) : (P (0,x)).2=U x-V x := by
        have ht := congrArg Prod.fst (h (0,x))
        have hp : P (-x,(2:ℝ) • x)= -P (x,0)+(2:ℝ) • P (0,x) := by
          rw [← map_neg,← map_smul,← map_add]
          congr 1
          ext <;> simp
        have hh : V x-(P (0,x)).2= -U x+(2:ℝ) • V x := by
          simpa [nativeStep,parentStep,hp,← hu,← hv] using ht
        calc
          (P (0,x)).2 = V x-(V x-(P (0,x)).2) := by abel
          _ = V x-(-U x+(2:ℝ) • V x) := by rw [hh]
          _ = U x-V x := by module
      rcases z with ⟨x,y⟩
      rw [split x y]
      ext <;> simp [reading,hu,hv,hw,hx] <;> abel
  · rintro ⟨U,V,hU,hV,hP⟩ z
    rw [hP z,hP (nativeStep z)]
    ext <;> simp [reading,nativeStep,parentStep,hU,hV] <;> module

theorem injective_spatial_operator_forces_zero (A : F →ₗ[ℝ] F)
    (hA : Function.Injective A) (P : (E × E) →ₗ[ℝ] (F × F))
    (h : Intertwines A P) : P=0 := by
  apply LinearMap.ext
  intro z
  have hh := intertwiner_range_in_kernel A P h z
  apply Prod.ext
  · exact hA (by simpa using hh.1)
  · exact hA (by simpa using hh.2)

theorem surjective_readout_forces_zero_spatial_operator (A : F →ₗ[ℝ] F)
    (P : (E × E) →ₗ[ℝ] (F × F)) (h : Intertwines A P)
    (hs : Function.Surjective P) : A=0 := by
  ext x
  obtain ⟨z,hz⟩ := hs (x,0)
  have hh := (intertwiner_range_in_kernel A P h z).1
  simpa [hz] using hh

def defect (A : F →ₗ[ℝ] F) (P : (E × E) →ₗ[ℝ] (F × F)) (z : E × E) :=
  parentStep A (P z)-P (nativeStep z)

/-- Exact error identity. Its norm estimate does not assume a uniform inverse. -/
theorem quantitative_defect_identity (A : F →ₗ[ℝ] F)
    (P : (E × E) →ₗ[ℝ] (F × F)) (z : E × E) :
    (A (P z).1,A (P z).2)=
      -defect A P z+parentInverse A (defect A P (nativeInverse z)) := by
  have hlin (x y : F × F) :
      parentInverse A (x-y)=parentInverse A x-parentInverse A y := by
    ext <;> simp [parentInverse] <;> module
  have he : parentInverse A (defect A P (nativeInverse z))=
      P (nativeInverse z)-parentInverse A (P z) := by
    rw [defect,native_inverse_right,hlin,parent_inverse_left]
  rw [he,defect]
  have hh : P (nativeStep z)+P (nativeInverse z)=(3:ℝ) • P z := by
    rw [← map_add,← map_smul]
    congr 1
    ext <;> simp [nativeStep,nativeInverse] <;> module
  have hh1 := congrArg Prod.fst hh
  have hh2 := congrArg Prod.snd hh
  change (P (nativeStep z)).1+(P (nativeInverse z)).1=(3:ℝ) • (P z).1 at hh1
  change (P (nativeStep z)).2+(P (nativeInverse z)).2=(3:ℝ) • (P z).2 at hh2
  apply Prod.ext
  · change A (P z).1= _
    calc
      A (P z).1 = -(parentStep A (P z)).1+(3:ℝ) • (P z).1-
          (parentInverse A (P z)).1 := by simp [parentStep,parentInverse]; module
      _ = _ := by rw [← hh1]; simp; abel
  · change A (P z).2= _
    calc
      A (P z).2 = -(parentStep A (P z)).2+(3:ℝ) • (P z).2-
          (parentInverse A (P z)).2 := by simp [parentStep,parentInverse]; module
      _ = _ := by rw [← hh2]; simp; abel

end Algebra

/-- Binding to the actual rational update declarations, not just their names. -/
theorem owned_rational_update (q p : ℚ) :
    nativeStep ((q:ℝ),(p:ℝ))=
      ((updateQ q p:ℝ),(updateP q p:ℝ)) := by
  ext <;> simp [nativeStep,updateQ,updateP]

/-- Binding to the actual integer state evolution, two ticks. -/
theorem owned_integer_update (z : D0.Core.TimeState) :
    nativeStep ((z 0:ℝ),(z 1:ℝ))=
      ((D0.Core.evolveState 2 z 0:ℝ),(D0.Core.evolveState 2 z 1:ℝ)) := by
  ext <;> simp [nativeStep,D0.Core.evolveState,pow_two,T,Matrix.mul_apply,
    Fin.sum_univ_two] <;> push_cast <;> ring

section Calculus
variable {X Y : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
  [NormedAddCommGroup Y] [NormedSpace ℝ Y]

/-- The first-jet intertwiner is derived by the chain rule, not assumed. -/
theorem derivative_of_equivariant_readout (B : X →L[ℝ] X) (M : Y →L[ℝ] Y)
    (f : X → Y) (P : X →L[ℝ] Y) (hf : HasFDerivAt f P 0)
    (he : ∀ x, f (B x)=M (f x)) : P.comp B=M.comp P := by
  have hleft : HasFDerivAt (fun x => f (B x)) (P.comp B) 0 := by
    exact (show HasFDerivAt f P (B 0) by simpa using hf).comp 0 B.hasFDerivAt
  have hright : HasFDerivAt (fun x => M (f x)) (M.comp P) 0 :=
    M.hasFDerivAt.comp 0 hf
  have heq : (fun x => f (B x))=(fun x => M (f x)) := funext he
  rw [heq] at hleft
  exact hleft.unique hright

def nativeContinuous : (X × X) →L[ℝ] (X × X) :=
  ((ContinuousLinearMap.fst ℝ X X)-(ContinuousLinearMap.snd ℝ X X)).prod
    (-(ContinuousLinearMap.fst ℝ X X)+(2:ℝ) • (ContinuousLinearMap.snd ℝ X X))

def parentContinuous (A : Y →L[ℝ] Y) : (Y × Y) →L[ℝ] (Y × Y) :=
  ((ContinuousLinearMap.fst ℝ Y Y)-(ContinuousLinearMap.snd ℝ Y Y)).prod
    (-(ContinuousLinearMap.fst ℝ Y Y)+A.comp (ContinuousLinearMap.fst ℝ Y Y)+
      (2:ℝ) • (ContinuousLinearMap.snd ℝ Y Y)-A.comp (ContinuousLinearMap.snd ℝ Y Y))

theorem native_continuous_binding (z : X × X) : nativeContinuous z=nativeStep z := rfl
theorem parent_continuous_binding (A : Y →L[ℝ] Y) (z : Y × Y) :
    parentContinuous A z=parentStep A.toLinearMap z := rfl

/-- Universal nonlinear first-jet boundary at the native fixed state. -/
theorem nonlinear_readout_derivative_range (A : Y →L[ℝ] Y)
    (f : (X × X) → (Y × Y)) (P : (X × X) →L[ℝ] (Y × Y))
    (hf : HasFDerivAt f P 0)
    (he : ∀ z, f (nativeStep z)=parentStep A.toLinearMap (f z)) (z : X × X) :
    A (P z).1=0 ∧ A (P z).2=0 := by
  have hd := derivative_of_equivariant_readout nativeContinuous
    (parentContinuous A) f P hf he
  apply intertwiner_range_in_kernel A.toLinearMap P.toLinearMap
  intro w
  exact (congrArg (fun L : (X × X) →L[ℝ] (Y × Y) => L w) hd).symm

theorem nonlinear_submersive_readout_forces_zero (A : Y →L[ℝ] Y)
    (f : (X × X) → (Y × Y)) (P : (X × X) →L[ℝ] (Y × Y))
    (hf : HasFDerivAt f P 0)
    (he : ∀ z, f (nativeStep z)=parentStep A.toLinearMap (f z))
    (hs : Function.Surjective P) : A=0 := by
  apply ContinuousLinearMap.ext
  intro y
  obtain ⟨z,hz⟩ := hs (y,0)
  have hh := (nonlinear_readout_derivative_range A f P hf he z).1
  simpa [hz] using hh

end Calculus

/-- A nonconstant polynomial equivariant map with zero first jet is allowed. -/
def invariantReading (z : ℝ × ℝ) : ℝ × ℝ := (z.1^2-z.1*z.2-z.2^2,0)

theorem nonlinear_zero_jet_control (z : ℝ × ℝ) :
    invariantReading (nativeStep z)=
      parentStep (LinearMap.id : ℝ →ₗ[ℝ] ℝ) (invariantReading z) := by
  ext <;> simp [invariantReading,nativeStep,parentStep] <;> ring

theorem nonlinear_control_nonconstant : invariantReading (1,0)≠invariantReading (0,0) := by
  norm_num [invariantReading]

end
#check owned_integer_update
#check owned_rational_update
#check native_inverse_right
#check native_inverse_left
#check native_quadratic
#check parent_inverse_right
#check parent_inverse_left
#check parent_quadratic_defect
#check intertwiner_range_in_kernel
#check complete_linear_readout
#check injective_spatial_operator_forces_zero
#check surjective_readout_forces_zero_spatial_operator
#check derivative_of_equivariant_readout
#check quantitative_defect_identity
#check native_continuous_binding
#check parent_continuous_binding
#check nonlinear_readout_derivative_range
#check nonlinear_submersive_readout_forces_zero
#check nonlinear_zero_jet_control
#check nonlinear_control_nonconstant
#print axioms owned_integer_update
#print axioms owned_rational_update
#print axioms native_inverse_right
#print axioms native_inverse_left
#print axioms native_quadratic
#print axioms parent_inverse_right
#print axioms parent_inverse_left
#print axioms parent_quadratic_defect
#print axioms intertwiner_range_in_kernel
#print axioms complete_linear_readout
#print axioms injective_spatial_operator_forces_zero
#print axioms surjective_readout_forces_zero_spatial_operator
#print axioms derivative_of_equivariant_readout
#print axioms quantitative_defect_identity
#print axioms native_continuous_binding
#print axioms parent_continuous_binding
#print axioms nonlinear_readout_derivative_range
#print axioms nonlinear_submersive_readout_forces_zero
#print axioms nonlinear_zero_jet_control
#print axioms nonlinear_control_nonconstant
end D0.Research.NativeTimeFieldIntertwiner
