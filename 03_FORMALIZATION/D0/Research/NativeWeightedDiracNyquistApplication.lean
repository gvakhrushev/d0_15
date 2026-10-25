import D0.Research.NativeWeightedDiracBoundary
import D0.Research.NativeWeightedDiracLinearOperator
import D0.Geometry.A4DMetricStarSignatureBoundary
import Mathlib.Tactic

/-! Exact L=4 application of the source's flat-Lorentz spatial Nyquist block
on the existing Archive cochain/Fock carrier. This is a mathematical operator
binding; it selects no physical action, matter sector, or observer pairing. -/
namespace D0.Research.NativeWeightedDiracNyquistApplication
open D0 D0.Geometry D0.Research.NativeWeightedDiracBoundary
open scoped BigOperators
noncomputable section

private def periodFourAlternatingSign (z : Fin 4) : ℝ := if z.val % 2 = 0 then 1 else -1

private theorem periodFourAlternatingSign_add_one (z : Fin 4) : periodFourAlternatingSign (z + 1) = -periodFourAlternatingSign z := by
  fin_cases z <;> norm_num [periodFourAlternatingSign, Fin.val_add, Fin.val_add_eq_ite]

private def z4AlternatingSign (z : ZMod 4) : ℝ := periodFourAlternatingSign z

private theorem z4AlternatingSign_add_one (z : ZMod 4) : z4AlternatingSign (z + 1) = -z4AlternatingSign z := by
  fin_cases z
  · change periodFourAlternatingSign ((0 : Fin 4) + 1) = -periodFourAlternatingSign 0
    exact periodFourAlternatingSign_add_one 0
  · change periodFourAlternatingSign ((1 : Fin 4) + 1) = -periodFourAlternatingSign 1
    exact periodFourAlternatingSign_add_one 1
  · change periodFourAlternatingSign ((2 : Fin 4) + 1) = -periodFourAlternatingSign 2
    exact periodFourAlternatingSign_add_one 2
  · change periodFourAlternatingSign ((3 : Fin 4) + 1) = -periodFourAlternatingSign 3
    exact periodFourAlternatingSign_add_one 3

private theorem z4AlternatingSign_sub_one (z : ZMod 4) : z4AlternatingSign (z - 1) = -z4AlternatingSign z := by
  have h := z4AlternatingSign_add_one (z - 1)
  calc
    z4AlternatingSign (z - 1) = -z4AlternatingSign ((z - 1) + 1) := by linarith
    _ = -z4AlternatingSign z := by congr 1; abel

def spatialNyquistBCharacter : ArchiveRolePhaseGroup 2 → ℝ := fun x => z4AlternatingSign (x B)

private theorem nyq_plus_B (x : ArchiveRolePhaseGroup 2) :
    spatialNyquistBCharacter (roleTranslatePlus 2 B x) = -spatialNyquistBCharacter x := by
  unfold spatialNyquistBCharacter roleTranslatePlus roleTranslate roleStep
  simpa [archiveFibers, roleStep] using z4AlternatingSign_add_one (x B)

private theorem nyq_minus_B (x : ArchiveRolePhaseGroup 2) :
    spatialNyquistBCharacter (roleTranslateMinus 2 B x) = -spatialNyquistBCharacter x := by
  have hcoord : roleTranslateMinus 2 B x B = x B - 1 := by
    simp [roleTranslateMinus, roleTranslate, roleStep, sub_eq_add_neg]
  rw [spatialNyquistBCharacter, hcoord]
  exact z4AlternatingSign_sub_one (x B)

private theorem nyq_plus_other (r : Role) (hr : r ≠ B) (x : ArchiveRolePhaseGroup 2) :
    spatialNyquistBCharacter (roleTranslatePlus 2 r x) = spatialNyquistBCharacter x := by
  unfold spatialNyquistBCharacter roleTranslatePlus roleTranslate roleStep
  have hne : B ≠ r := Ne.symm hr
  simp [hne]

private theorem nyq_minus_other (r : Role) (hr : r ≠ B) (x : ArchiveRolePhaseGroup 2) :
    spatialNyquistBCharacter (roleTranslateMinus 2 r x) = spatialNyquistBCharacter x := by
  unfold spatialNyquistBCharacter roleTranslateMinus roleTranslate roleStep
  have hne : B ≠ r := Ne.symm hr
  simp [hne]

private theorem nyq_forward_B (x : ArchiveRolePhaseGroup 2) :
    forwardDifference 2 B spatialNyquistBCharacter x = -8 * spatialNyquistBCharacter x := by
  simp [forwardDifference, forwardDifferenceScale, archiveFibers, nyq_plus_B]
  ring

private theorem nyq_backward_B (x : ArchiveRolePhaseGroup 2) :
    backwardDifference 2 B spatialNyquistBCharacter x = 8 * spatialNyquistBCharacter x := by
  simp [backwardDifference, forwardDifferenceScale, archiveFibers, nyq_minus_B]
  ring

private theorem nyq_forward_other (r : Role) (hr : r ≠ B) (x : ArchiveRolePhaseGroup 2) :
    forwardDifference 2 r spatialNyquistBCharacter x = 0 := by
  simp [forwardDifference, forwardDifferenceScale, archiveFibers, nyq_plus_other r hr x]

private theorem nyq_backward_other (r : Role) (hr : r ≠ B) (x : ArchiveRolePhaseGroup 2) :
    backwardDifference 2 r spatialNyquistBCharacter x = 0 := by
  simp [backwardDifference, forwardDifferenceScale, archiveFibers, nyq_minus_other r hr x]

private lemma role_sign_sq' (r : Role) : roleLorentzSign r ^ 2 = 1 := by
  fin_cases r <;> norm_num [roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]

private lemma flatLorentzSubsetWeight_sq' (S : ArchiveFockState) :
    flatLorentzSubsetWeight S ^ 2 = 1 := by
  rw [flatLorentzSubsetWeight_eq_sign_product, ← Finset.prod_pow]
  simp [role_sign_sq']

private lemma flatLorentzSubsetWeight_vacuum' : flatLorentzSubsetWeight vacuumFockState = 1 := by
  rw [flatLorentzSubsetWeight_eq_sign_product]
  simp [vacuumFockState, fockVacuumState]

private lemma flatLorentzSubsetWeight_singletonB' :
    flatLorentzSubsetWeight (singletonFockState B) = -1 := by
  rw [flatLorentzSubsetWeight_eq_sign_product]
  have hfilter : Finset.univ.filter (fun r : Role => singletonFockState B r) = {B} := by
    ext r
    simp [singletonFockState, fockSingletonState]
  rw [hfilter]
  simp [roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]

noncomputable def flatLorentzWeightEquiv (N : ℕ) : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N where
  toFun ψ p := flatLorentzSubsetWeight p.2 * ψ p
  invFun ψ p := flatLorentzSubsetWeight p.2 * ψ p
  left_inv ψ := by
    funext p
    change flatLorentzSubsetWeight p.2 * (flatLorentzSubsetWeight p.2 * ψ p) = ψ p
    rw [← mul_assoc, ← pow_two, flatLorentzSubsetWeight_sq', one_mul]
  right_inv ψ := by
    funext p
    change flatLorentzSubsetWeight p.2 * (flatLorentzSubsetWeight p.2 * ψ p) = ψ p
    rw [← mul_assoc, ← pow_two, flatLorentzSubsetWeight_sq', one_mul]
  map_add' ψ φ := by
    funext p
    simp [mul_add]
  map_smul' c ψ := by
    funext p
    simp [Pi.smul_apply, mul_left_comm]

private theorem fockDegree_one_iff' (S : ArchiveFockState) :
    fockDegree S = 1 ↔ ∃ r : Role, S = singletonFockState r := by
  constructor
  · intro h
    let occ : Finset Role := Finset.univ.filter (fun r => S r = true)
    have hcard : occ.card = 1 := by simpa [occ, fockDegree] using h
    obtain ⟨r, hr⟩ := Finset.card_eq_one.mp hcard
    refine ⟨r, ?_⟩
    funext s
    by_cases hs : s = r
    · subst s
      have hm : r ∈ occ := by rw [hr]; simp
      have ht : S r = true := (Finset.mem_filter.mp hm).2
      simpa [fockSingletonState] using ht
    · have hnm : s ∉ occ := by rw [hr]; simp [hs]
      have hn : S s ≠ true := by
        intro hsTrue
        exact hnm (Finset.mem_filter.mpr ⟨Finset.mem_univ s, hsTrue⟩)
      cases hval : S s <;> simp [fockSingletonState, hs, hval] at *
  · rintro ⟨r, hS⟩
    subst S
    unfold fockDegree
    have hf : Finset.univ.filter (fun s : Role => fockSingletonState r s = true) = {r} := by
      ext s
      simp [fockSingletonState]
    rw [hf]
    simp

private lemma singletonFockState_injective' : Function.Injective (singletonFockState : Role → ArchiveFockState) := by
  intro r s h
  by_contra hrs
  have hval := congrFun h r
  simp [fockSingletonState, hrs] at hval

private lemma scalar_homogeneous' (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    HomogeneousCochain N 0 (scalarCochain N f) := by
  intro x S hS
  by_cases h : S = vacuumFockState
  · subst S
    have hz : fockDegree vacuumFockState = 0 := by simp [fockDegree, vacuumFockState, fockVacuumState]
    exact (hS hz).elim
  · simp [scalarCochain, h]

private theorem dForward_scalar_eq_oneForm' (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    dForward N (scalarCochain N f) =
      oneFormCochain N (fun x r => forwardDifference N r f x) := by
  classical
  funext p
  rcases p with ⟨x,S⟩
  by_cases hdeg : fockDegree S = 1
  · obtain ⟨r, hr⟩ := (fockDegree_one_iff' S).mp hdeg
    subst S
    change dForward N (scalarCochain N f) (x, singletonFockState r) =
      ∑ s : Role, if singletonFockState r = singletonFockState s then
        forwardDifference N s f x else 0
    rw [show dForward N (scalarCochain N f) (x, singletonFockState r) =
      forwardDifference N r f x by
        have hh := congrFun (dForward_scalar_oneForm_component N f r) x
        simpa [oneFormComponent] using hh]
    rw [Finset.sum_eq_single r]
    · simp
    · intro s hs hsr
      have hne : singletonFockState r ≠ singletonFockState s := by
        intro heq
        exact hsr (singletonFockState_injective' heq.symm)
      simp [hne]
    · simp
  · have hhom := dForward_degree_raise N 0 (scalarCochain N f) (scalar_homogeneous' N f)
    have hzero : dForward N (scalarCochain N f) (x,S) = 0 := hhom x S hdeg
    rw [hzero]
    unfold oneFormCochain
    symm
    apply Finset.sum_eq_zero
    intro r hr
    have hne : S ≠ singletonFockState r := by
      intro hs
      subst S
      apply hdeg
      exact (fockDegree_one_iff' (singletonFockState r)).mpr ⟨r, rfl⟩
    simp [hne]

private lemma carAnnihilate_vacuum_zero' (r : Role) (S : ArchiveFockState) :
    carAnnihilate r S vacuumFockState = 0 := by
  by_contra hc
  have hs := carAnnihilate_support r S vacuumFockState hc
  have htrue : fockVacuumState r = true := hs.1
  simp [fockVacuumState] at htrue

private lemma hodgeCodifferential_scalar_zero' (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    hodgeCodifferential N (scalarCochain N f) = 0 := by
  classical
  funext p
  rcases p with ⟨x,S⟩
  unfold hodgeCodifferential
  apply Finset.sum_eq_zero
  intro r hr
  rw [backwardAnnihilateDirection_eq]
  change -(∑ ket : ArchiveFockState, carAnnihilate r S ket *
    backwardDifference N r (fun y => scalarCochain N f (y, ket)) x) = 0
  rw [Finset.sum_eq_single vacuumFockState]
  · rw [carAnnihilate_vacuum_zero']
    simp [scalarCochain]
  · intro ket hket hne
    have hz : (fun y : ArchiveRolePhaseGroup N => scalarCochain N f (y, ket)) =
        (fun _ => 0) := by
      funext y
      simp [scalarCochain, hne]
    rw [hz]
    simp [backwardDifference]
  · simp

def spatialNyquistVacuum : ArchiveCochain 2 := scalarCochain 2 spatialNyquistBCharacter
private def spatialNyquistBAlpha (x : ArchiveRolePhaseGroup 2) (r : Role) : ℝ := if r = B then spatialNyquistBCharacter x else 0
private def spatialNyquistBOneForm : ArchiveCochain 2 := oneFormCochain 2 spatialNyquistBAlpha
def spatialNyquistBState : ArchiveCochain 2 := fun p => if p.2 = singletonFockState B then spatialNyquistBCharacter p.1 else 0

private theorem spatialNyquistBOneForm_eq_direct : spatialNyquistBOneForm = spatialNyquistBState := by
  classical
  funext p
  rcases p with ⟨x,S⟩
  by_cases hS : S = singletonFockState B
  · subst S
    unfold spatialNyquistBOneForm oneFormCochain spatialNyquistBAlpha spatialNyquistBState
    rw [Finset.sum_eq_single B]
    · simp
    · intro r hr hne
      by_cases hrB : r = B
      · subst r
        exact (hne rfl).elim
      · simp [hrB]
    · simp
  · unfold spatialNyquistBOneForm oneFormCochain spatialNyquistBAlpha spatialNyquistBState
    rw [if_neg hS]
    apply Finset.sum_eq_zero
    intro r hr
    by_cases hrB : r = B
    · subst r
      simp [hS]
    · simp [hrB]

private lemma oneFormCochain_smul' (N : ℕ) (c : ℝ) (α : LocalRoleVector N) :
    oneFormCochain N (fun x r => c * α x r) = c • oneFormCochain N α := by
  classical
  funext p
  simp [oneFormCochain, Finset.mul_sum, smul_eq_mul]

private theorem dForward_spatialNyquistVacuum :
    dForward 2 spatialNyquistVacuum = (-8 : ℝ) • spatialNyquistBState := by
  rw [show spatialNyquistVacuum = scalarCochain 2 spatialNyquistBCharacter by rfl, dForward_scalar_eq_oneForm']
  have hα : (fun x r => forwardDifference 2 r spatialNyquistBCharacter x) =
      fun x r => (-8 : ℝ) * spatialNyquistBAlpha x r := by
    funext x r
    by_cases hr : r = B
    · subst r
      simpa [spatialNyquistBAlpha] using nyq_forward_B x
    · simpa [spatialNyquistBAlpha, hr] using nyq_forward_other r hr x
  rw [hα]
  calc
    oneFormCochain 2 (fun x r => (-8 : ℝ) * spatialNyquistBAlpha x r) =
        (-8 : ℝ) • oneFormCochain 2 spatialNyquistBAlpha := oneFormCochain_smul' 2 (-8) spatialNyquistBAlpha
    _ = (-8 : ℝ) • spatialNyquistBState := congrArg (fun ψ : ArchiveCochain 2 => (-8 : ℝ) • ψ)
      spatialNyquistBOneForm_eq_direct

private theorem spatialNyquistBCharacter_forward_function :
    forwardDifference 2 B spatialNyquistBCharacter = fun x => (-8 : ℝ) * spatialNyquistBCharacter x := by
  funext x
  exact nyq_forward_B x

private theorem spatialNyquistBCharacter_backward_scaled (x : ArchiveRolePhaseGroup 2) :
    backwardDifference 2 B (fun y => (-8 : ℝ) * spatialNyquistBCharacter y) x =
      (-8 : ℝ) * backwardDifference 2 B spatialNyquistBCharacter x := by
  unfold backwardDifference
  ring

private theorem nyq_scalar_laplacian (x : ArchiveRolePhaseGroup 2) :
    scalarDifferenceLaplacian 2 spatialNyquistBCharacter x = 64 * spatialNyquistBCharacter x := by
  unfold scalarDifferenceLaplacian
  rw [Finset.sum_eq_single B]
  · rw [spatialNyquistBCharacter_forward_function, spatialNyquistBCharacter_backward_scaled, nyq_backward_B]
    ring
  · intro r hr hne
    have hrB : r ≠ B := by
      intro h
      exact hne h
    have hf : forwardDifference 2 r spatialNyquistBCharacter = fun _ => 0 := by
      funext y
      exact nyq_forward_other r hrB y
    rw [hf]
    change -backwardDifference 2 r (fun _ => 0) x = 0
    simp [backwardDifference]
  · simp

private theorem nyq_cochain_laplacian :
    cochainDifferenceLaplacian 2 spatialNyquistVacuum = 64 • spatialNyquistVacuum := by
  funext p
  rcases p with ⟨x,S⟩
  by_cases hS : S = vacuumFockState
  · subst S
    simp only [spatialNyquistVacuum, scalarCochain, cochainDifferenceLaplacian, if_pos]
    simpa [scalarCochain] using nyq_scalar_laplacian x
  · simp [cochainDifferenceLaplacian, spatialNyquistVacuum, scalarCochain, scalarDifferenceLaplacian,
      forwardDifference, backwardDifference, hS]

private lemma spatialNyquistBCharacter_zero : spatialNyquistBCharacter (0 : ArchiveRolePhaseGroup 2) = 1 := by
  change z4AlternatingSign (0 : ZMod 4) = 1
  change periodFourAlternatingSign (0 : Fin 4) = 1
  rfl

theorem spatialNyquistVacuum_ne_zero : spatialNyquistVacuum ≠ 0 := by
  intro h
  have hh := congrFun h ((0 : ArchiveRolePhaseGroup 2), vacuumFockState)
  change spatialNyquistBCharacter 0 = 0 at hh
  rw [spatialNyquistBCharacter_zero] at hh
  norm_num at hh

theorem spatialNyquistBState_ne_zero : spatialNyquistBState ≠ 0 := by
  intro h
  have hh := congrFun h ((0 : ArchiveRolePhaseGroup 2), singletonFockState B)
  change spatialNyquistBCharacter 0 = 0 at hh
  rw [spatialNyquistBCharacter_zero] at hh
  norm_num at hh

private lemma flatLorentzW_scalar (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    flatLorentzWeightEquiv N (scalarCochain N f) = scalarCochain N f := by
  funext p
  by_cases hS : p.2 = vacuumFockState
  · simp [flatLorentzWeightEquiv, scalarCochain, hS, flatLorentzSubsetWeight_vacuum']
  · simp [flatLorentzWeightEquiv, scalarCochain, hS]

private lemma flatLorentzWsymm_scalar (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    (flatLorentzWeightEquiv N).symm (scalarCochain N f) = scalarCochain N f := by
  funext p
  by_cases hS : p.2 = vacuumFockState
  · simp [flatLorentzWeightEquiv, scalarCochain, hS, flatLorentzSubsetWeight_vacuum']
  · simp [flatLorentzWeightEquiv, scalarCochain, hS]

private lemma flatLorentzW_nyqB :
    flatLorentzWeightEquiv 2 spatialNyquistBState = -spatialNyquistBState := by
  funext p
  rcases p with ⟨x,S⟩
  by_cases hS : S = singletonFockState B
  · subst S
    simp [flatLorentzWeightEquiv, spatialNyquistBState, flatLorentzSubsetWeight_singletonB']
  · simp [flatLorentzWeightEquiv, spatialNyquistBState, hS]

private lemma hodgeDirac_spatialNyquistVacuum :
    hodgeCarDirac 2 spatialNyquistVacuum = (-8 : ℝ) • spatialNyquistBState := by
  unfold hodgeCarDirac
  rw [dForward_spatialNyquistVacuum]
  have hcod : hodgeCodifferential 2 spatialNyquistVacuum = 0 := by
    simpa [spatialNyquistVacuum] using hodgeCodifferential_scalar_zero' 2 spatialNyquistBCharacter
  rw [hcod]
  simp

private lemma dForward_nyqB_zero : dForward 2 spatialNyquistBState = 0 := by
  have h := D0.Research.NativeWeightedDiracBoundary.kernel_d_sq 2 spatialNyquistVacuum
  rw [dForward_spatialNyquistVacuum, dForward_smul] at h
  funext p
  have hp : (-8 : ℝ) • dForward 2 spatialNyquistBState p = 0 := by
    simpa only [Pi.smul_apply] using congrFun h p
  have hmul : (-8 : ℝ) * dForward 2 spatialNyquistBState p = 0 := by
    simpa only [smul_eq_mul] using hp
  change dForward 2 spatialNyquistBState p = 0
  nlinarith [hmul]

private lemma hodgeDirac_nyqB :
    hodgeCarDirac 2 spatialNyquistBState = (-8 : ℝ) • spatialNyquistVacuum := by
  have hsq := hodgeCarDirac_sq 2 spatialNyquistVacuum
  rw [hodgeDirac_spatialNyquistVacuum, hodgeCarDirac_smul, nyq_cochain_laplacian] at hsq
  calc
    hodgeCarDirac 2 spatialNyquistBState = (1 : ℝ) • hodgeCarDirac 2 spatialNyquistBState := by simp
    _ = ((-1 / 8 : ℝ) * (-8)) • hodgeCarDirac 2 spatialNyquistBState := by congr 1; norm_num
    _ = (-1 / 8 : ℝ) • ((-8 : ℝ) • hodgeCarDirac 2 spatialNyquistBState) := by rw [← smul_smul]
    _ = (-1 / 8 : ℝ) • ((64 : ℝ) • spatialNyquistVacuum) := by
      rw [hsq]
      ext p
      simp
    _ = ((-1 / 8 : ℝ) * 64) • spatialNyquistVacuum := by rw [smul_smul]
    _ = (-8 : ℝ) • spatialNyquistVacuum := by congr 1; norm_num

private lemma hodgeCodifferential_nyqB :
    hodgeCodifferential 2 spatialNyquistBState = (-8 : ℝ) • spatialNyquistVacuum := by
  have h := hodgeDirac_nyqB
  unfold hodgeCarDirac at h
  rw [dForward_nyqB_zero] at h
  simpa using h

private lemma weightedCodiff_spatialNyquistVacuum :
    weightedCodiff 2 (flatLorentzWeightEquiv 2) spatialNyquistVacuum = 0 := by
  unfold weightedCodiff
  have hW : flatLorentzWeightEquiv 2 spatialNyquistVacuum = spatialNyquistVacuum := by
    simpa [spatialNyquistVacuum] using flatLorentzW_scalar 2 spatialNyquistBCharacter
  rw [hW]
  have hcod : hodgeCodifferential 2 spatialNyquistVacuum = 0 := by
    simpa [spatialNyquistVacuum] using hodgeCodifferential_scalar_zero' 2 spatialNyquistBCharacter
  rw [hcod]
  simp

private lemma weightedCodiff_nyqB :
    weightedCodiff 2 (flatLorentzWeightEquiv 2) spatialNyquistBState =
      (8 : ℝ) • spatialNyquistVacuum := by
  unfold weightedCodiff
  rw [flatLorentzW_nyqB]
  rw [show -spatialNyquistBState = (-1 : ℝ) • spatialNyquistBState by simp]
  rw [hodgeCodifferential_smul, hodgeCodifferential_nyqB]
  rw [smul_smul]
  norm_num
  have hWsymm : (flatLorentzWeightEquiv 2).symm spatialNyquistVacuum = spatialNyquistVacuum := by
    simpa [spatialNyquistVacuum] using flatLorentzWsymm_scalar 2 spatialNyquistBCharacter
  rw [hWsymm]

theorem spatialNyquist_weightedDirac_block :
    weightedDirac 2 (flatLorentzWeightEquiv 2) spatialNyquistVacuum = (-8 : ℝ) • spatialNyquistBState ∧
    weightedDirac 2 (flatLorentzWeightEquiv 2) spatialNyquistBState = (8 : ℝ) • spatialNyquistVacuum := by
  constructor
  · unfold weightedDirac
    rw [dForward_spatialNyquistVacuum, weightedCodiff_spatialNyquistVacuum]
    simp
  · unfold weightedDirac
    rw [dForward_nyqB_zero, weightedCodiff_nyqB]
    simp

/-! The application uses the generic typed matrix adapter in the actual finite
`ArchiveCochainBasis 2` coordinates. -/

noncomputable def flatLorentzWeightedDiracMatrix :
    Matrix (ArchiveCochainBasis 2) (ArchiveCochainBasis 2) ℝ :=
  D0.Research.NativeWeightedDiracLinearOperator.weightedDiracMatrix 2
    (flatLorentzWeightEquiv 2)

theorem spatialNyquist_weightedDirac_matrix_block :
    Matrix.mulVec flatLorentzWeightedDiracMatrix spatialNyquistVacuum = (-8 : ℝ) • spatialNyquistBState ∧
    Matrix.mulVec flatLorentzWeightedDiracMatrix spatialNyquistBState = (8 : ℝ) • spatialNyquistVacuum := by
  have hblock := spatialNyquist_weightedDirac_block
  constructor
  · calc
      Matrix.mulVec flatLorentzWeightedDiracMatrix spatialNyquistVacuum =
          weightedDirac 2 (flatLorentzWeightEquiv 2) spatialNyquistVacuum := by
        simpa only [flatLorentzWeightedDiracMatrix] using
          D0.Research.NativeWeightedDiracLinearOperator.weightedDiracMatrix_mulVec
            2 (flatLorentzWeightEquiv 2) spatialNyquistVacuum
      _ = (-8 : ℝ) • spatialNyquistBState := hblock.1
  · calc
      Matrix.mulVec flatLorentzWeightedDiracMatrix spatialNyquistBState =
          weightedDirac 2 (flatLorentzWeightEquiv 2) spatialNyquistBState := by
        simpa only [flatLorentzWeightedDiracMatrix] using
          D0.Research.NativeWeightedDiracLinearOperator.weightedDiracMatrix_mulVec
            2 (flatLorentzWeightEquiv 2) spatialNyquistBState
      _ = (8 : ℝ) • spatialNyquistVacuum := hblock.2

/-- The actual L=4 flat-Lorentz CAR/Hodge matrix cannot be self-adjoint for
any positive-definite bilinear pairing on the full cochain carrier. This is
the source's Eq. (6) obstruction applied to this exact matrix; it does not
derive a physical pairing or claim that D0 selects one. -/
theorem flatLorentzWeightedDirac_no_positive_selfadjoint_pairing
    (G : Matrix (ArchiveCochainBasis 2) (ArchiveCochainBasis 2) ℝ)
    (hpos : ∀ x, x ≠ 0 → 0 < dotProduct x (G.mulVec x))
    (hadj : flatLorentzWeightedDiracMatrix.transpose * G =
      G * flatLorentzWeightedDiracMatrix) : False := by
  have hblock := spatialNyquist_weightedDirac_matrix_block
  have hTu : Matrix.mulVec flatLorentzWeightedDiracMatrix spatialNyquistVacuum =
      -(2 * (4 : ℝ)) • spatialNyquistBState := by
    simpa only [show (2 * (4 : ℝ) : ℝ) = 8 by norm_num] using hblock.1
  have hTv : Matrix.mulVec flatLorentzWeightedDiracMatrix spatialNyquistBState =
      (2 * (4 : ℝ)) • spatialNyquistVacuum := by
    simpa only [show (2 * (4 : ℝ) : ℝ) = 8 by norm_num] using hblock.2
  exact positive_selfadjoint_spatial_invariant_block_impossible
    (i := ArchiveCochainBasis 2) 4 (by norm_num)
    flatLorentzWeightedDiracMatrix G spatialNyquistVacuum spatialNyquistBState
    spatialNyquistVacuum_ne_zero spatialNyquistBState_ne_zero hpos hadj hTu hTv

#print axioms spatialNyquist_weightedDirac_block
#print axioms spatialNyquist_weightedDirac_matrix_block
#print axioms flatLorentzWeightedDirac_no_positive_selfadjoint_pairing
#print axioms spatialNyquistVacuum_ne_zero
#print axioms spatialNyquistBState_ne_zero
end
end D0.Research.NativeWeightedDiracNyquistApplication
