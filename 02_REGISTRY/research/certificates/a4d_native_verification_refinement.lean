import D0.Foundation.VerifiabilityNecessity
import D0.Synthesis.ConcretePhysicalDetectorRepresentation
import D0.Geometry.ArchiveLaplacianRG

/-! Actual verification/process interfaces and the existing phase refinement.
This does not select an action, a physical state space, or a new variation gate.
The equality-test process class and the exact phase tower are explicit scopes. -/
namespace D0.Research.NativeVerificationRefinement
open D0.Foundation
open D0.Foundation.M1ClassAdmissibility
open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open scoped BigOperators
noncomputable section

def equalityProtocol (α : Type) [DecidableEq α] : VerificationProtocol where
  State := α
  Record := α
  Line := Bool
  Catalogue := Bool
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x≠y)

def equalityProtocolVerified (α : Type) [DecidableEq α] [Nontrivial α] :
    VerificationContract (equalityProtocol α) where
  state_nontrivial := by change Nontrivial α; infer_instance
  line_nontrivial := by change Nontrivial Bool; infer_instance
  catalogue_nonempty := by change Nonempty Bool; infer_instance
  correct := by intros; rfl

/-- This is the exact expressive strength of the existing formal interface.
It is not a theorem that all such equality oracles are physical apparatuses. -/
theorem verifiable_iff_nontrivial (T : EmpiricalTheory) :
    OperationallyVerifiable T ↔ Nontrivial (EmpiricalState T) := by
  classical
  constructor
  · rintro ⟨E⟩
    obtain ⟨x,y,hxy⟩ := E.contract.state_nontrivial.exists_pair_ne
    exact ⟨⟨E.represents x,E.represents y,fun h => hxy (E.represents.injective h)⟩⟩
  · intro h
    letI := h
    exact ⟨{
      protocol := equalityProtocol (EmpiricalState T)
      contract := equalityProtocolVerified (EmpiricalState T)
      represents := Equiv.refl _ }⟩

variable {P : VerificationProtocol}

/-- The literal pull-test law fixes every inverse image of a point test. -/
theorem operational_point_fiber (V : VerificationContract P)
    (O : OperationalProcess (operationalEmpiricalTheory P))
    (l : P.Line) (c : P.Catalogue) (x y : P.State) :
    O.run x=y ↔ x=(O.pullTest (l,y)).2 := by
  have h := O.compatible x c (l,y)
  change P.compare l c (P.record (O.run x)) (P.record y) =
    P.compare (O.pullTest (l,y)).1 c (P.record x)
      (P.record (O.pullTest (l,y)).2) at h
  rw [V.correct, V.correct] at h
  exact not_iff_not.mp (decide_eq_decide.mp h)

theorem operational_run_bijective (V : VerificationContract P)
    (O : OperationalProcess (operationalEmpiricalTheory P)) :
    Function.Bijective O.run := by
  obtain ⟨l,_,_⟩ := V.line_nontrivial.exists_pair_ne
  obtain ⟨c⟩ := V.catalogue_nonempty
  constructor
  · intro x y hxy
    have hx := (operational_point_fiber V O l c x (O.run x)).mp rfl
    have hy := (operational_point_fiber V O l c y (O.run x)).mp hxy.symm
    exact hx.trans hy.symm
  · intro y
    exact ⟨(O.pullTest (l,y)).2,(operational_point_fiber V O l c _ y).mpr rfl⟩

def processOfEquiv (V : VerificationContract P) (σ : P.State ≃ P.State) :
    OperationalProcess (operationalEmpiricalTheory P) where
  run := σ
  pullTest e := (e.1,σ.symm e.2)
  compatible := by
    intro s c e
    change P.compare e.1 c (P.record (σ s)) (P.record e.2) =
      P.compare e.1 c (P.record s) (P.record (σ.symm e.2))
    rw [V.correct,V.correct]
    have heq : σ s=e.2 ↔ s=σ.symm e.2 := by
      constructor
      · intro h; rw [← h]; simp
      · intro h; rw [h]; simp
    exact decide_eq_decide.mpr (not_congr heq)

def HasOperationalLift (P : VerificationProtocol) (f : P.State → P.State) : Prop :=
  ∃ O : OperationalProcess (operationalEmpiricalTheory P), O.run=f

/-- Complete run classification for this actual point-test interface. -/
theorem operational_lift_iff_bijective (V : VerificationContract P)
    (f : P.State → P.State) : HasOperationalLift P f ↔ Function.Bijective f := by
  constructor
  · rintro ⟨O,rfl⟩; exact operational_run_bijective V O
  · intro h
    exact ⟨processOfEquiv V (Equiv.ofBijective f h),rfl⟩

theorem invariant_all_verified_processes_iff_constant (V : VerificationContract P)
    {Y : Type*} (a : P.State → Y) :
    (∀ O : OperationalProcess (operationalEmpiricalTheory P), ∀ x, a (O.run x)=a x) ↔
      ∀ x y, a x=a y := by
  classical
  constructor
  · intro h x y
    have hh := h (processOfEquiv V (Equiv.swap x y)) x
    simpa [processOfEquiv] using hh.symm
  · intro h O x; exact h (O.run x) x

/-- A different existing empirical test interface admits arbitrary runs.
This protects the point-test hypothesis in the bijectivity theorem. -/
def predicateTheory (α : Type) : EmpiricalTheory where
  State := α
  Test := α → Bool
  Catalogue := Bool
  Outcome := Bool
  observe s _ e := e s

def predicateProcess (α : Type) (f : α → α) : OperationalProcess (predicateTheory α) where
  run := f
  pullTest e := e ∘ f
  compatible := by intros; rfl

theorem arbitrary_predicate_run (α : Type) (f : α → α) :
    ∃ O : OperationalProcess (predicateTheory α), O.run=f :=
  ⟨predicateProcess α f,rfl⟩

local instance archiveFibersNeZero (n : ℕ) : NeZero (archiveFibers n) :=
  ⟨by simp [archiveFibers]⟩

/-- Literal old-state inclusion and the one new phase point. -/
def phaseOld (n : ℕ) (i : archivePhaseIndex n) : archivePhaseIndex (n+1) :=
  ⟨i.val,by have hi:=i.isLt; simp only [archiveFibers] at *; omega⟩

def phaseNew (n : ℕ) : archivePhaseIndex (n+1) :=
  ⟨n+2,by simp [archiveFibers]⟩

theorem phase_projection_old (n : ℕ) (i : archivePhaseIndex n) :
    archiveRGPhaseProjection n (phaseOld n i)=i := by
  apply Fin.ext
  simp [archiveRGPhaseProjection,phaseOld,Nat.mod_eq_of_lt i.isLt]

theorem phase_projection_zero (n : ℕ) : archiveRGPhaseProjection n 0=0 := by
  apply Fin.ext
  simp [archiveRGPhaseProjection,archiveFibers]

theorem phase_projection_new (n : ℕ) : archiveRGPhaseProjection n (phaseNew n)=0 := by
  apply Fin.ext
  simp [archiveRGPhaseProjection,phaseNew,archiveFibers]

theorem phase_projection_zero_fiber (n : ℕ) (i : archivePhaseIndex (n+1)) :
    archiveRGPhaseProjection n i=0 ↔ i=0 ∨ i=phaseNew n := by
  constructor
  · intro h
    have hi := i.isLt
    change i.val < n+1+2 at hi
    by_cases hsmall : i.val<n+2
    · left
      apply Fin.ext
      have hh := congrArg Fin.val h
      simpa [archiveRGPhaseProjection,archiveFibers,Nat.mod_eq_of_lt hsmall] using hh
    · right
      apply Fin.ext
      change i.val=n+2
      omega
  · rintro (rfl|rfl)
    · exact phase_projection_zero n
    · exact phase_projection_new n

theorem phase_projection_nonzero_injective (n : ℕ)
    (i j : archivePhaseIndex (n+1))
    (h : archiveRGPhaseProjection n i=archiveRGPhaseProjection n j)
    (hi : archiveRGPhaseProjection n i≠0) : i=j := by
  have hsmall (x : archivePhaseIndex (n+1)) (hx : archiveRGPhaseProjection n x≠0) :
      x.val<n+2 := by
    have hb := x.isLt
    change x.val<n+1+2 at hb
    by_contra hn
    have he : x=phaseNew n := by apply Fin.ext; change x.val=n+2; omega
    exact hx ((phase_projection_zero_fiber n x).mpr (Or.inr he))
  have hi' := hsmall i hi
  have hj' := hsmall j (by rwa [← h])
  apply Fin.ext
  have hh := congrArg Fin.val h
  simpa [archiveRGPhaseProjection,archiveFibers,Nat.mod_eq_of_lt hi',Nat.mod_eq_of_lt hj'] using hh

theorem commuting_phase_permutations_fix_coarse_zero (n : ℕ)
    (σ : Equiv.Perm (archivePhaseIndex n))
    (τ : Equiv.Perm (archivePhaseIndex (n+1)))
    (hc : ∀ i, archiveRGPhaseProjection n (τ i)=σ (archiveRGPhaseProjection n i)) :
    σ 0=0 := by
  by_contra hz
  have he : archiveRGPhaseProjection n (τ 0)=archiveRGPhaseProjection n (τ (phaseNew n)) := by
    rw [hc,hc,phase_projection_zero,phase_projection_new]
  have hn : archiveRGPhaseProjection n (τ 0)≠0 := by rwa [hc,phase_projection_zero]
  have hf := τ.injective (phase_projection_nonzero_injective n _ _ he hn)
  have hv := congrArg Fin.val hf
  simp [phaseNew] at hv

/-- Every exact reversible process on every stage of the actual phase tower
is the identity. This does not identify the phase tower with flattened ArchivePoints. -/
theorem coherent_phase_permutations_identity
    (σ : ∀ n, Equiv.Perm (archivePhaseIndex n))
    (hc : ∀ n i, archiveRGPhaseProjection n (σ (n+1) i)=σ n (archiveRGPhaseProjection n i)) :
    ∀ n i, σ n i=i := by
  have hz (n : ℕ) := commuting_phase_permutations_fix_coarse_zero n (σ n) (σ (n+1)) (hc n)
  intro n
  induction n with
  | zero =>
    change ∀ i : Fin 2, σ 0 i=i
    intro i
    fin_cases i
    · exact hz 0
    · have hn : σ 0 (1 : Fin 2)≠0 := by
        intro h
        have hh := (σ 0).injective (h.trans (hz 0).symm)
        have hv := congrArg Fin.val hh
        norm_num at hv
      have hb := (σ 0 (1 : Fin 2)).isLt
      change (σ 0 (1 : Fin 2)).val<2 at hb
      have hv : (σ 0 (1 : Fin 2)).val≠0 := by
        intro h; exact hn (Fin.ext h)
      apply Fin.ext
      change (σ 0 (1 : Fin 2)).val=1
      omega
  | succ n ih =>
    intro i
    have hp : archiveRGPhaseProjection n (σ (n+1) i)=archiveRGPhaseProjection n i := by
      rw [hc,ih]
    by_cases hpi : archiveRGPhaseProjection n i=0
    · rcases (phase_projection_zero_fiber n i).mp hpi with hi|hi
      · subst i; exact hz (n+1)
      · have hni : i≠0 := by rw [hi]; intro h; have hv:=congrArg Fin.val h; simp [phaseNew] at hv
        have hsni : σ (n+1) i≠0 := by
          intro h
          exact hni ((σ (n+1)).injective (h.trans (hz (n+1)).symm))
        rcases (phase_projection_zero_fiber n (σ (n+1) i)).mp (hp.trans hpi) with hs|hs
        · exact False.elim (hsni hs)
        · exact hs.trans hi.symm
    · exact phase_projection_nonzero_injective n _ _ hp (by rwa [hp])

def boolFlip : Bool ≃ Bool where
  toFun b := !b
  invFun b := !b
  left_inv b := by cases b <;> rfl
  right_inv b := by cases b <;> rfl

def verifiedFlip := processOfEquiv (equalityProtocolVerified Bool) boolFlip

/-- A literal two-preparation test of the existing native Dirichlet action. -/
def phasePreparation (b : Bool) : archivePhaseIndex 1 → ℝ :=
  fun i => if b then (if i.val=0 then 1 else 0) else 0

theorem phase_preparation_zero_energy :
    archiveDirichletEnergy 1 (phasePreparation false)=0 := by
  simp [archiveDirichletEnergy,phasePreparation]

theorem phase_preparation_radial_energy (t : ℝ) :
    archiveDirichletEnergy 1 (fun i => (1+t)*phasePreparation true i)=4*(1+t)^2 := by
  change (∑ i : Fin 3, ∑ j : Fin 3,
    if min ((i.val+3-j.val)%3) ((j.val+3-i.val)%3)=1 then
    ((1+t)*(if i.val=0 then 1 else 0)-(1+t)*(if j.val=0 then 1 else 0))^2 else 0)=4*(1+t)^2
  norm_num [Fin.sum_univ_succ]
  ring

theorem phase_preparation_pulse_energy :
    archiveDirichletEnergy 1 (phasePreparation true)=4 := by
  simpa using phase_preparation_radial_energy 0

theorem phase_preparation_radial_contrast (ε : ℝ) :
    archiveDirichletEnergy 1 (fun i => (1+ε)*phasePreparation true i)-
      archiveDirichletEnergy 1 (fun i => (1-ε)*phasePreparation true i)=16*ε := by
  have hminus := phase_preparation_radial_energy (-ε)
  rw [phase_preparation_radial_energy]
  simp only [sub_eq_add_neg] at *
  rw [hminus]
  ring

theorem verified_flip_changes_owned_energy :
    archiveDirichletEnergy 1 (phasePreparation (verifiedFlip.run false))-
      archiveDirichletEnergy 1 (phasePreparation false)=4 := by
  change archiveDirichletEnergy 1 (phasePreparation true)-
    archiveDirichletEnergy 1 (phasePreparation false)=4
  rw [phase_preparation_pulse_energy,phase_preparation_zero_energy]
  ring

theorem constant_run_fails_point_test_lift :
    ¬ HasOperationalLift (equalityProtocol Bool) (fun _ => false) := by
  rw [operational_lift_iff_bijective (equalityProtocolVerified Bool)]
  intro h
  change Function.Bijective (fun _ : Bool => false) at h
  have hh : (false : Bool)=true := h.1 (a₁:=false) (a₂:=true) rfl
  cases hh

end
end D0.Research.NativeVerificationRefinement

#print axioms D0.Research.NativeVerificationRefinement.equalityProtocolVerified
#print axioms D0.Research.NativeVerificationRefinement.verifiable_iff_nontrivial
#print axioms D0.Research.NativeVerificationRefinement.operational_point_fiber
#print axioms D0.Research.NativeVerificationRefinement.operational_run_bijective
#print axioms D0.Research.NativeVerificationRefinement.operational_lift_iff_bijective
#print axioms D0.Research.NativeVerificationRefinement.invariant_all_verified_processes_iff_constant
#print axioms D0.Research.NativeVerificationRefinement.arbitrary_predicate_run
#print axioms D0.Research.NativeVerificationRefinement.phase_projection_zero_fiber
#print axioms D0.Research.NativeVerificationRefinement.phase_projection_nonzero_injective
#print axioms D0.Research.NativeVerificationRefinement.commuting_phase_permutations_fix_coarse_zero
#print axioms D0.Research.NativeVerificationRefinement.coherent_phase_permutations_identity
#print axioms D0.Research.NativeVerificationRefinement.phase_preparation_radial_contrast
#print axioms D0.Research.NativeVerificationRefinement.verified_flip_changes_owned_energy
#print axioms D0.Research.NativeVerificationRefinement.constant_run_fails_point_test_lift
#check D0.Research.NativeVerificationRefinement.verifiable_iff_nontrivial
#check D0.Research.NativeVerificationRefinement.operational_lift_iff_bijective
#check D0.Research.NativeVerificationRefinement.coherent_phase_permutations_identity
#print axioms D0.Synthesis.ConcretePhysicalDetectorRepresentation.concrete_physical_detector_representation
#check D0.Synthesis.ConcretePhysicalDetectorRepresentation.concrete_physical_detector_representation
#print axioms D0.Foundation.M1ClassAdmissibility.non_singleton_class_not_M1Forced
#check D0.Foundation.M1ClassAdmissibility.non_singleton_class_not_M1Forced
