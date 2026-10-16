import D0.Geometry.ArchiveAffineExteriorLink
import Mathlib.Tactic

/-! Research kernel for the literal soldered operator and its homogeneous
metric jet. The generic matrix calculations retain all ten symmetric slots.
The Fourier assembly and heat derivative have analytic/certificate status;
this capsule does not select the square of archiveSolderedDirac as the native
bootstrap heat, prove curved self-adjointness, or construct a physical source. -/
namespace D0.Research.SolderedHeatSource
noncomputable section
open Matrix D0 D0.Geometry

abbrev M4 := Matrix (Fin 4) (Fin 4) ℝ

/-- All ten independent entries, with six unscaled off-diagonal coordinates. -/
def metricMatrix (x : Fin 10 → ℝ) : M4 :=
  !![x 0,x 4,x 5,x 6; x 4,x 1,x 7,x 8;
     x 5,x 7,x 2,x 9; x 6,x 8,x 9,x 3]

/-- The actual fixed-v rest pullback: only the time/time entry keeps its sign. -/
def restPullback (H : M4) : M4 :=
  fun i j => if i=0 ∧ j=0 then H i j else -H i j

def restSlots (x : Fin 10 → ℝ) : Fin 10 → ℝ :=
  fun i => if i=0 then x i else -x i

def packedPair (w x : Fin 10 → ℝ) : ℝ :=
  w 0*x 0+w 1*x 1+w 2*x 2+w 3*x 3+
    2*(w 4*x 4+w 5*x 5+w 6*x 6+w 7*x 7+w 8*x 8+w 9*x 9)

theorem metricMatrix_symmetric (x : Fin 10 → ℝ) :
    (metricMatrix x).transpose=metricMatrix x := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem restPullback_formula (H : M4) (i j : Fin 4) :
    restPullback H i j=-H i j+(if i=0 ∧ j=0 then 2*H 0 0 else 0) := by
  by_cases h : i=0 ∧ j=0
  · rcases h with ⟨rfl,rfl⟩
    simp [restPullback]
    ring
  · simp [restPullback,h]

theorem restPullback_involutive (H : M4) :
    restPullback (restPullback H)=H := by
  ext i j
  by_cases h : i=0 ∧ j=0 <;> simp [restPullback,h]

theorem all_ten_rest_pullback (x : Fin 10 → ℝ) :
    restPullback (metricMatrix x)=metricMatrix (restSlots x) := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [restPullback,metricMatrix,restSlots,Fin.ext_iff]

theorem metricMatrix_injective : Function.Injective metricMatrix := by
  intro x y h
  funext i
  fin_cases i
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 0 0) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 1 1) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 2 2) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 3 3) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 0 1) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 0 2) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 0 3) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 1 2) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 1 3) h
  · simpa [metricMatrix] using congrArg (fun M : M4 => M 2 3) h

theorem trace_packed_weights (w x : Fin 10 → ℝ) :
    Matrix.trace (metricMatrix w*metricMatrix x)=packedPair w x := by
  simp [Matrix.trace,Matrix.diag,Matrix.mul_apply,Fin.sum_univ_succ,
    metricMatrix,packedPair]
  ring

theorem rest_trace_pullback (w x : Fin 10 → ℝ) :
    -Matrix.trace (metricMatrix w*restPullback (metricMatrix x))=
      packedPair (fun i => if i=0 then -w i else w i) x := by
  rw [all_ten_rest_pullback,trace_packed_weights]
  norm_num [packedPair,restSlots,Fin.ext_iff]
  ring

/-- Every homogeneous symmetric probe satisfies the true link-metric tangent
at the identity dressed link, with both endpoint Grams varying. -/
theorem homogeneous_constraint_tangent (q : M4) (x : Fin 10 → ℝ) :
    (0 : M4)*q*(1 : M4).transpose+
      (1 : M4)*metricMatrix x*(1 : M4).transpose+
      (1 : M4)*q*(0 : M4).transpose-metricMatrix x=0 := by simp

/-- The full nonlinear constraint already holds throughout a homogeneous
curve, so the preceding tangent is not an off-constraint metric partial. -/
theorem homogeneous_constraint_curve (q : ℝ → M4) (t : ℝ) :
    (1 : M4)*q t*(1 : M4).transpose=q t := by simp

/-- The two-site literal left-multiplied forward difference at L=2. -/
def rawTwoSite (f0 f1 : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-2*f0,2*f0; 2*f1,-2*f1]

theorem rawTwoSite_factorization (f0 f1 : ℝ) :
    rawTwoSite f0 f1=
      !![f0,0;0,f1]*(2 : ℝ) • (!![0,1;1,0]-(1 : Matrix (Fin 2) (Fin 2) ℝ)) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rawTwoSite,Matrix.mul_apply,Fin.sum_univ_two] <;> ring

theorem rawTwoSite_adjoint_defect (f0 f1 : ℝ) :
    rawTwoSite f0 f1-(rawTwoSite f0 f1).transpose=
      (2*(f0-f1)) • !![0,1;-1,0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rawTwoSite,Matrix.transpose_apply] <;> ring

theorem rawTwoSite_symmetric_iff (f0 f1 : ℝ) :
    (rawTwoSite f0 f1).transpose=rawTwoSite f0 f1 ↔ f0=f1 := by
  constructor
  · intro h
    have h01 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    simp [rawTwoSite,Matrix.transpose_apply] at h01
    linarith
  · intro h
    subst f1
    ext i j
    fin_cases i <;> fin_cases j <;> rfl

theorem exact_variable_solder_defect :
    rawTwoSite (3/2) (1/2)=!![-3,3;1,-1] ∧
    (rawTwoSite (3/2) (1/2)).transpose≠rawTwoSite (3/2) (1/2) := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [rawTwoSite]
  · intro h
    have hne := (rawTwoSite_symmetric_iff (3/2) (1/2)).mp h
    norm_num at hne

/-- Actual consumed exterior creator, not a replacement symbolic matrix. -/
theorem actual_creator_square_zero (v : RoleSpace) (psi : ArchiveFockState → ℝ) :
    archiveExteriorCreator v (archiveExteriorCreator v psi)=0 := by
  have h := archiveExteriorCreator_anticommute v v psi
  funext p
  have hp := congrFun h p
  simp only [Pi.add_apply,Pi.zero_apply] at hp
  change _=0
  linarith

theorem actual_contraction_square_zero (alpha : Module.Dual ℝ RoleSpace)
    (psi : ArchiveFockState → ℝ) :
    archiveExteriorContraction alpha (archiveExteriorContraction alpha psi)=0 := by
  have h := archiveExteriorContraction_anticommute alpha alpha psi
  funext p
  have hp := congrFun h p
  simp only [Pi.neg_apply] at hp
  change _=0
  linarith

/-- Real constant-symbol CAR square on all sixteen literal exterior components.
The complex Fourier assembly is an additional analytic argument. -/
theorem actual_constant_CAR_square (v : RoleSpace) (alpha : Module.Dual ℝ RoleSpace)
    (psi : ArchiveFockState → ℝ) :
    archiveExteriorCreator v (archiveExteriorCreator v psi+archiveExteriorContraction alpha psi)+
    archiveExteriorContraction alpha
      (archiveExteriorCreator v psi+archiveExteriorContraction alpha psi)=alpha v • psi := by
  have creator_add (a b : ArchiveFockState → ℝ) :
      archiveExteriorCreator v (a+b)=archiveExteriorCreator v a+archiveExteriorCreator v b := by
    simp [archiveExteriorCreator,map_add,mul_add]
  simp only [creator_add,map_add,actual_creator_square_zero,actual_contraction_square_zero,
    zero_add,add_zero]
  simpa [add_comm] using archiveExterior_contraction_creator_car alpha v psi

/-- All sixteen spatially constant Fock values remain in the kernel at flat
links, even before any homogeneous-solder or positive-heat claim is made. -/
theorem actual_flat_links_kill_constants (N : ℕ) (e : LocalCoframeField N)
    (n : ArchiveRolePhaseGroup N → RoleVector) (c : ArchiveFockState → ℝ) :
    archiveSolderedDirac (flatAffineConnection N) e n (fun p => c p.2)=0 := by
  have hz (v : RoleSpace) : archiveExteriorCreator v (fun _ => 0)=0 := by
    change archiveExteriorCreator v 0=0
    simp [archiveExteriorCreator]
  have ha (a : Module.Dual ℝ RoleSpace) : archiveExteriorContraction a (fun _ => 0)=0 := by
    change archiveExteriorContraction a 0=0
    exact map_zero _
  funext p
  simp [archiveSolderedDirac,archiveSolderedForwardDifferential,
    archiveSolderedCreateDirection,archiveSolderedCodifferential,
    archiveSolderedAnnihilateDirection,archiveAffinePullFiber,
    archiveAffineExteriorLink,archiveAffinePullPreviousFiber,
    flatAffineConnection,archiveExteriorFrameLift_id,hz,ha]

/-- Complete rest-point joint jet for metric H and quotient observer u=δv.
The definition exposes that the observer time rescaling has zero first jet. -/
def jointRestSlots (x : Fin 10 → ℝ) (u : Fin 4 → ℝ) : Fin 10 → ℝ :=
  ![x 0,-x 1,-x 2,-x 3,-x 4+2*u 1,-x 5+2*u 2,-x 6+2*u 3,
    -x 7,-x 8,-x 9]

theorem joint_rest_packed_contraction (w x : Fin 10 → ℝ) (u : Fin 4 → ℝ) :
    -Matrix.trace (metricMatrix w*metricMatrix (jointRestSlots x u))=
    packedPair (fun i => if i=0 then -w i else w i) x-
      4*(w 4*u 1+w 5*u 2+w 6*u 3) := by
  rw [trace_packed_weights]
  change -(w 0*x 0+w 1*(-x 1)+w 2*(-x 2)+w 3*(-x 3)+
    2*(w 4*(-x 4+2*u 1)+w 5*(-x 5+2*u 2)+w 6*(-x 6+2*u 3)+
       w 7*(-x 7)+w 8*(-x 8)+w 9*(-x 9)))=_
  norm_num [packedPair,Fin.ext_iff]
  ring

/-- This is a kinematic kernel calculation, not a declaration of gauge. -/
theorem joint_rest_kernel (x : Fin 10 → ℝ) (u : Fin 4 → ℝ) :
    metricMatrix (jointRestSlots x u)=0 ↔
    x 0=0 ∧ x 1=0 ∧ x 2=0 ∧ x 3=0 ∧
    x 4=2*u 1 ∧ x 5=2*u 2 ∧ x 6=2*u 3 ∧ x 7=0 ∧ x 8=0 ∧ x 9=0 := by
  have hzero : metricMatrix (fun _ => 0)=0 := by ext i j; fin_cases i <;> fin_cases j <;> rfl
  rw [← hzero,metricMatrix_injective.eq_iff]
  simp [funext_iff,Fin.forall_fin_succ,jointRestSlots,neg_add_eq_zero]

theorem joint_rest_observer_rescale (x : Fin 10 → ℝ) (u : Fin 4 → ℝ) (t : ℝ) :
    jointRestSlots x (fun i => if i=0 then u i+t else u i)=jointRestSlots x u := by
  ext i
  fin_cases i <;> norm_num [jointRestSlots,Fin.ext_iff]

end
end D0.Research.SolderedHeatSource

#check D0.Geometry.archiveSolderedDirac
#check D0.Geometry.solderLegVector
#check D0.Geometry.observerMetric_posDef
#check D0.Geometry.observer_contraction_adjoint_covariant
#check D0.Geometry.archiveExterior_contraction_creator_car

-- Actual defining terms expose the operator consumed from the compiled import.
#print D0.Geometry.solderLegVector
#print D0.Geometry.archiveSolderedCreateDirection
#print D0.Geometry.archiveSolderedAnnihilateDirection
#print D0.Geometry.archiveSolderedCodifferential
#print D0.Geometry.archiveSolderedDirac
#print D0.Geometry.observerMetric

-- Axiom closure includes the actual exterior owners consumed above.
#print axioms D0.Research.SolderedHeatSource.metricMatrix_symmetric
#print axioms D0.Research.SolderedHeatSource.restPullback_formula
#print axioms D0.Research.SolderedHeatSource.restPullback_involutive
#print axioms D0.Research.SolderedHeatSource.all_ten_rest_pullback
#print axioms D0.Research.SolderedHeatSource.metricMatrix_injective
#print axioms D0.Research.SolderedHeatSource.trace_packed_weights
#print axioms D0.Research.SolderedHeatSource.rest_trace_pullback
#print axioms D0.Research.SolderedHeatSource.homogeneous_constraint_tangent
#print axioms D0.Research.SolderedHeatSource.homogeneous_constraint_curve
#print axioms D0.Research.SolderedHeatSource.rawTwoSite_factorization
#print axioms D0.Research.SolderedHeatSource.rawTwoSite_adjoint_defect
#print axioms D0.Research.SolderedHeatSource.rawTwoSite_symmetric_iff
#print axioms D0.Research.SolderedHeatSource.exact_variable_solder_defect
#print axioms D0.Research.SolderedHeatSource.actual_creator_square_zero
#print axioms D0.Research.SolderedHeatSource.actual_contraction_square_zero
#print axioms D0.Research.SolderedHeatSource.actual_constant_CAR_square
#print axioms D0.Research.SolderedHeatSource.actual_flat_links_kill_constants
#print axioms D0.Research.SolderedHeatSource.joint_rest_packed_contraction
#print axioms D0.Research.SolderedHeatSource.joint_rest_kernel
#print axioms D0.Research.SolderedHeatSource.joint_rest_observer_rescale
#print axioms D0.Geometry.archiveExteriorCreator_anticommute
#print axioms D0.Geometry.archiveExteriorContraction_anticommute
#print axioms D0.Geometry.archiveExterior_contraction_creator_car
#print axioms D0.Geometry.observerMetric_posDef
#print axioms D0.Geometry.observer_contraction_adjoint_covariant
#print axioms D0.Geometry.archiveExteriorFrameLift_id
