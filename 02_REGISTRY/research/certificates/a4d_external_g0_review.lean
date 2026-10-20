import D0.Geometry.A4DScalarDeltaSecondJet
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.Calculus.Deriv.Polynomial

/-! Independent review of the supplied G0 report. The countermodels concern
its interface implications, not physical D0 solutions or an owned gauge.
The cycle theorem below uses the literal native scalarCycleG definition. -/

namespace D0.Research.ExternalG0Review
open Matrix D0.Geometry
noncomputable section

theorem transpose_mul_zero_forces_zero {I : Type*} [Fintype I] [DecidableEq I]
    (A : Matrix I I ℚ) (h : Aᵀ*A=0) : A=0 := by
  ext i j
  have hd := congrArg (fun M : Matrix I I ℚ => M j j) h
  have hs : ∑ k, A k j*A k j=0 := by simpa [Matrix.mul_apply] using hd
  have ht := (Finset.sum_eq_zero_iff_of_nonneg
    (fun k (_ : k ∈ Finset.univ) => mul_self_nonneg (A k j))).mp hs i (Finset.mem_univ i)
  exact mul_self_eq_zero.mp ht

theorem skew_cube_zero_forces_zero {I : Type*} [Fintype I] [DecidableEq I]
    (A : Matrix I I ℚ) (ha : Aᵀ = -A) (h3 : (A*A)*A=0) : A=0 := by
  have h2s : (A*A)ᵀ = A*A := by rw [transpose_mul,ha,neg_mul_neg]
  have h4 : (A*A)*(A*A)=0 := by rw [← mul_assoc,h3,zero_mul]
  have h2 : A*A=0 := transpose_mul_zero_forces_zero _ (by rw [h2s,h4])
  exact transpose_mul_zero_forces_zero _ (by rw [ha,neg_mul,h2,neg_zero])

theorem native_constant_generator_eq_difference (n : ℕ) [NeZero n] :
    scalarCycleG (scalarOnes n)=scalarCycleD n := by
  have hm : scalarCycleMul (scalarOnes n)=(1 : Matrix (Fin n) (Fin n) ℚ) := by
    ext i j
    simp [scalarCycleMul,scalarOnes,Matrix.diagonal,Matrix.one_apply]
  rw [scalarCycleG,hm,one_mul]

theorem native_cycle_difference_skew (n : ℕ) [NeZero n] :
    (scalarCycleD n)ᵀ = -(scalarCycleD n) := by
  simp only [scalarCycleD,transpose_smul,transpose_sub,transpose_transpose]
  module

theorem native_cycle_difference_nonzero (n : ℕ) [NeZero n] (hn : 3≤n) :
    scalarCycleD n≠0 := by
  intro hz
  have he := D_forward hn (0 : Fin n)
  rw [hz] at he
  have hnq : (0:ℚ)<n := by exact_mod_cast (show 0<n by omega)
  simp only [Matrix.zero_apply] at he
  linarith

/-- All carrier sizes, not a finite scan. The explicit entry formula is
proved analytically and independently checked in the companion certificate. -/
theorem native_constant_cycle_cube_nonzero (n : ℕ) [NeZero n] (hn : 3≤n) :
    (scalarCycleG (scalarOnes n)*scalarCycleG (scalarOnes n))*
      scalarCycleG (scalarOnes n) ≠ 0 := by
  rw [native_constant_generator_eq_difference]
  intro h
  exact native_cycle_difference_nonzero n hn
    (skew_cube_zero_forces_zero _ (native_cycle_difference_skew n) h)

def rankOne {X : Type*} [AddCommGroup X] [Module ℝ X]
    (l : X →ₗ[ℝ] ℝ) (a : ℝ) : X →ₗ[ℝ] X →ₗ[ℝ] ℝ :=
  l.smulRight (l.smulRight a)

theorem rank_one_symmetric {X : Type*} [AddCommGroup X] [Module ℝ X]
    (l : X →ₗ[ℝ] ℝ) (a : ℝ) (x y : X) : rankOne l a x y=rankOne l a y x := by
  change l x*(l y*a)=l y*(l x*a)
  ring

theorem single_direction_evaluation_surjective {X : Type*} [AddCommGroup X] [Module ℝ X]
    (l : X →ₗ[ℝ] ℝ) (v : X) (hv : l v=1) (a : ℝ) :
    ∃ S : X →ₗ[ℝ] X →ₗ[ℝ] ℝ, (∀ x y, S x y=S y x) ∧ S v v=a := by
  exact ⟨rankOne l a,rank_one_symmetric l a,by simp [rankOne,hv]⟩

/-- Surjectivity of one diagonal observation does not imply injectivity. -/
theorem single_direction_has_nonzero_kernel :
    ∃ S : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ) →ₗ[ℝ] ℝ,
      (∀ x y, S x y=S y x) ∧
      S (Pi.single 0 1) (Pi.single 0 1)=0 ∧
      S (Pi.single 1 1) (Pi.single 1 1)=1 := by
  refine ⟨rankOne (LinearMap.proj (1 : Fin 2)) 1,rank_one_symmetric _ _,?_,?_⟩ <;>
    norm_num [rankOne,LinearMap.smulRight_apply,LinearMap.proj_apply,Pi.single_apply]

theorem all_diagonals_determine_symmetric_form {X : Type*} [AddCommGroup X] [Module ℝ X]
    (S T : X →ₗ[ℝ] X →ₗ[ℝ] ℝ)
    (hs : ∀ x y, S x y=S y x) (ht : ∀ x y, T x y=T y x)
    (h : ∀ x, S x x=T x x) : S=T := by
  ext x y
  have hh := h (x+y)
  simp only [map_add,LinearMap.add_apply] at hh
  rw [← hs x y,← ht x y] at hh
  linarith [h x,h y]

abbrev Field := ℝ × ℝ

def shear (a : ℝ) (v : Field) : Field := (v.1+a*v.2,v.2)
def frame (e : ℝ) : Field → Field := shear (e^2/2)
def transport (e x : ℝ) : Field → Field := shear (e*x+x^2/2)
def reading (v : Field) : ℝ := v.1
def probe : Field := (0,1)

theorem shear_composition (a b : ℝ) (v : Field) :
    shear a (shear b v)=shear (a+b) v := by
  apply Prod.ext
  · change v.1+b*v.2+a*v.2=v.1+(a+b)*v.2
    ring
  · rfl

theorem shear_inverse (a : ℝ) (v : Field) : shear (-a) (shear a v)=v := by
  rw [shear_composition]
  simp [shear]

theorem transport_from_frames (e x : ℝ) (v : Field) :
    transport e x v=frame (e+x) (shear (-(e^2/2)) v) := by
  apply Prod.ext
  · dsimp [transport,frame,shear]
    ring
  · rfl

theorem full_transport_composition (e x y : ℝ) (v : Field) :
    transport (e+x) y (transport e x v)=transport e (x+y) v := by
  apply Prod.ext
  · dsimp [transport,shear]
    ring
  · rfl

theorem transport_background_derivative (e x : ℝ) :
    HasDerivAt (fun b => reading (transport b x probe)) x e := by
  simpa [reading,transport,probe,shear] using ((hasDerivAt_id e).mul_const x).add_const (x^2/2)

theorem transport_background_second_derivative (x : ℝ) :
    HasDerivAt (fun e => deriv (fun b => reading (transport b x probe)) e) 0 0 := by
  have hf : (fun e => deriv (fun b => reading (transport b x probe)) e) = fun _ => x := by
    funext e
    exact (transport_background_derivative e x).deriv
  rw [hf]
  exact hasDerivAt_const 0 x

theorem transport_parameter_derivative (t : ℝ) :
    HasDerivAt (fun a => reading (transport 0 a probe)) t t := by
  convert ((hasDerivAt_id t).pow 2).div_const 2 using 1 <;>
    simp [reading,transport,probe,shear]

theorem transport_parameter_second_derivative :
    HasDerivAt (fun t => deriv (fun a => reading (transport 0 a probe)) t) 1 0 := by
  have hf : (fun t => deriv (fun a => reading (transport 0 a probe)) t) = fun t => t := by
    funext t
    exact (transport_parameter_derivative t).deriv
  rw [hf]
  exact hasDerivAt_id 0

/-- For trivial isotropy every readout is isotropy invariant. A frame
change can nevertheless change a fixed readout on the same input. -/
theorem isotropy_covariance_does_not_force_frame_invariance :
    (∀ (P : Field → ℝ) v, P (id v)=id (P v)) ∧
    reading (frame 2 probe)≠reading probe := by
  constructor
  · intros; rfl
  · norm_num [reading,frame,shear,probe]

def constantReading (_ : Field) : Field := probe

/-- Failure of output equivariance does not force distinguishable values
under frame changes: this readout has the same value on every input. -/
theorem failed_isotropy_covariance_does_not_force_frame_sensitivity :
    constantReading (shear 1 (0,0))≠shear 1 (constantReading (0,0)) ∧
    (∀ e v, constantReading (frame e v)=constantReading v) := by
  constructor
  · norm_num [constantReading,probe,shear]
  · intros; rfl

#print axioms transpose_mul_zero_forces_zero
#print axioms skew_cube_zero_forces_zero
#print axioms native_constant_generator_eq_difference
#print axioms native_cycle_difference_skew
#print axioms native_cycle_difference_nonzero
#print axioms native_constant_cycle_cube_nonzero
#print axioms rank_one_symmetric
#print axioms single_direction_evaluation_surjective
#print axioms single_direction_has_nonzero_kernel
#print axioms all_diagonals_determine_symmetric_form
#print axioms shear_composition
#print axioms shear_inverse
#print axioms transport_from_frames
#print axioms full_transport_composition
#print axioms transport_background_derivative
#print axioms transport_background_second_derivative
#print axioms transport_parameter_derivative
#print axioms transport_parameter_second_derivative
#print axioms isotropy_covariance_does_not_force_frame_invariance
#print axioms failed_isotropy_covariance_does_not_force_frame_sensitivity
#check scalarCycleG
#check native_constant_cycle_cube_nonzero
#check single_direction_evaluation_surjective
#check single_direction_has_nonzero_kernel
#check transport_background_second_derivative
#check transport_parameter_second_derivative
#check isotropy_covariance_does_not_force_frame_invariance
#check failed_isotropy_covariance_does_not_force_frame_sensitivity

end
end D0.Research.ExternalG0Review
