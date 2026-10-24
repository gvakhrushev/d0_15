import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier
import D0.Geometry.ArchiveCubicalCoboundary

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveNaiveWeightedDegreeLeakageNoGo

Owner: `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001`.

The registered research target concerns the position-dependent operator
`d_w = sqrt(w) d` and whether its square has a nonzero two-direction
cross-term. This file now includes one exact finite witness using the
repository's CAR16 cubical differential at refinement `N = 1`. It proves a
degree-zero scalar input has coefficient `1` in a degree-two output after two
weighted steps for the stated site-weight profile. This is a concrete
counterexample to universal preservation of `d_w² = 0`; it does not establish
failure for every nonconstant weight profile or prove that geometry must
enter only through a Hodge metric.
-/

/-- The first fixed sample weight used only in the square-root inequality below. -/
def naiveWeight0 : ℝ := 1

/-- The second fixed sample weight used only in the square-root inequality below. -/
def naiveWeight1 : ℝ := 4

theorem sqrt_naive_weights_ne : Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1 := by
  unfold naiveWeight0 naiveWeight1
  have h1 : Real.sqrt 1 = 1 := Real.sqrt_one
  have h4 : Real.sqrt 4 = 2 := by
    have : (2 : ℝ) ^ 2 = 4 := by norm_num
    rw [← this, Real.sqrt_sq]
    linarith
  rw [h1, h4]
  norm_num

/-! ## Exact finite-carrier witness

The next result uses the existing CAR16 cubical differential at refinement
`N = 1` (three phases in each role direction). The input is a scalar delta at
the two-step site `A+B`; the site weight is `4` at the intermediate `A`
site and `1` elsewhere. The `sqrt(w)`-weighted differential therefore has a
nonzero degree-two component after two applications. This is one concrete
counterexample to universal preservation of `d_w² = 0`; it is not a theorem
for every nonconstant weight profile.
-/

def naiveWeightTestOrigin : ArchiveRolePhaseGroup 1 := 0

def naiveWeightTestSiteA : ArchiveRolePhaseGroup 1 :=
  roleTranslatePlus 1 D0.A naiveWeightTestOrigin

def naiveWeightTestSiteAB : ArchiveRolePhaseGroup 1 :=
  roleTranslatePlus 1 D0.B naiveWeightTestSiteA

def naiveWeightTestSiteB : ArchiveRolePhaseGroup 1 :=
  roleTranslatePlus 1 D0.B naiveWeightTestOrigin

def naiveWeightTestPairState : ArchiveFockState :=
  fun r => r = D0.A ∨ r = D0.B

def naiveWeightTestScalarProfile : ArchiveRolePhaseGroup 1 → ℝ :=
  fun x => if x = naiveWeightTestSiteAB then 1 else 0

def naiveWeightTestSiteProfile : ArchiveRolePhaseGroup 1 → ℝ :=
  fun x => if x = naiveWeightTestSiteA then naiveWeight1 else naiveWeight0

noncomputable def naiveWeightedCubicalDifferential
    (ψ : ArchiveCochain 1) : ArchiveCochain 1 :=
  fun p => Real.sqrt (naiveWeightTestSiteProfile p.1) * cubicalCoboundary 1 ψ p

private theorem cubicalCoboundary_scalar_singleton
    (f : ArchiveRolePhaseGroup 1 → ℝ) (r : Role) (x : ArchiveRolePhaseGroup 1) :
    cubicalCoboundary 1 (scalarCochain 1 f) (x, singletonFockState r) =
      f (roleTranslatePlus 1 r x) - f x := by
  calc
    cubicalCoboundary 1 (scalarCochain 1 f) (x, singletonFockState r) =
        (forwardDifferenceScale 1)⁻¹ *
          oneFormComponent 1 (dForward 1 (scalarCochain 1 f)) r x := rfl
    _ = (forwardDifferenceScale 1)⁻¹ * forwardDifference 1 r f x := by
      rw [dForward_scalar_oneForm_component]
    _ = f (roleTranslatePlus 1 r x) - f x := by
      norm_num [forwardDifference, forwardDifferenceScale, archiveFibers]
      ring

private theorem naiveWeightedScalar_singleton
    (f : ArchiveRolePhaseGroup 1 → ℝ) (r : Role) (x : ArchiveRolePhaseGroup 1) :
    naiveWeightedCubicalDifferential (scalarCochain 1 f) (x, singletonFockState r) =
      Real.sqrt (naiveWeightTestSiteProfile x) *
        (f (roleTranslatePlus 1 r x) - f x) := by
  rw [naiveWeightedCubicalDifferential, cubicalCoboundary_scalar_singleton]

private theorem sqrt_naiveWeight1_eq_two : Real.sqrt naiveWeight1 = 2 := by
  unfold naiveWeight1
  have hsquare : (2 : ℝ) ^ 2 = 4 := by norm_num
  rw [← hsquare, Real.sqrt_sq]
  norm_num

private theorem naiveWeightTestSiteA_ne_origin :
    naiveWeightTestSiteA ≠ naiveWeightTestOrigin := by
  decide

private theorem naiveWeightTestSiteAB_ne_origin :
    naiveWeightTestSiteAB ≠ naiveWeightTestOrigin := by
  decide

private theorem naiveWeightTestSiteAB_ne_siteA :
    naiveWeightTestSiteAB ≠ naiveWeightTestSiteA := by
  decide

private theorem naiveWeightTestSiteAB_ne_siteB :
    naiveWeightTestSiteAB ≠ naiveWeightTestSiteB := by
  decide

private theorem naiveWeightTestSiteB_ne_siteA :
    naiveWeightTestSiteB ≠ naiveWeightTestSiteA := by
  decide

private theorem roleTranslateA_siteB_eq_siteAB :
    roleTranslatePlus 1 D0.A naiveWeightTestSiteB = naiveWeightTestSiteAB := by
  dsimp [naiveWeightTestSiteAB, naiveWeightTestSiteB, naiveWeightTestSiteA,
    naiveWeightTestOrigin, roleTranslatePlus, roleTranslate, roleStep]
  abel

private theorem naiveWeightSqrt_at_origin :
    Real.sqrt (naiveWeightTestSiteProfile naiveWeightTestOrigin) = 1 := by
  have h := Ne.symm naiveWeightTestSiteA_ne_origin
  simp [naiveWeightTestSiteProfile, naiveWeight0, h]

private theorem naiveWeightSqrt_at_siteA :
    Real.sqrt (naiveWeightTestSiteProfile naiveWeightTestSiteA) = 2 := by
  simp only [naiveWeightTestSiteProfile]
  exact sqrt_naiveWeight1_eq_two

private theorem naiveWeightSqrt_at_siteB :
    Real.sqrt (naiveWeightTestSiteProfile naiveWeightTestSiteB) = 1 := by
  have h := naiveWeightTestSiteB_ne_siteA
  simp [naiveWeightTestSiteProfile, naiveWeight0, h]

private theorem naiveScalar_at_origin :
    naiveWeightTestScalarProfile naiveWeightTestOrigin = 0 := by
  have h := Ne.symm naiveWeightTestSiteAB_ne_origin
  simp [naiveWeightTestScalarProfile, h]

private theorem naiveScalar_at_siteA :
    naiveWeightTestScalarProfile naiveWeightTestSiteA = 0 := by
  have h := Ne.symm naiveWeightTestSiteAB_ne_siteA
  simp [naiveWeightTestScalarProfile, h]

private theorem naiveScalar_at_siteB :
    naiveWeightTestScalarProfile naiveWeightTestSiteB = 0 := by
  have h := Ne.symm naiveWeightTestSiteAB_ne_siteB
  simp [naiveWeightTestScalarProfile, h]

private theorem naiveScalar_at_siteAB :
    naiveWeightTestScalarProfile naiveWeightTestSiteAB = 1 := by
  simp [naiveWeightTestScalarProfile]

private theorem weightedScalar_siteA_singletonB :
    naiveWeightedCubicalDifferential
      (scalarCochain 1 naiveWeightTestScalarProfile)
      (naiveWeightTestSiteA, singletonFockState D0.B) = 2 := by
  rw [naiveWeightedScalar_singleton, naiveWeightSqrt_at_siteA]
  rw [show roleTranslatePlus 1 D0.B naiveWeightTestSiteA = naiveWeightTestSiteAB by rfl,
    naiveScalar_at_siteAB, naiveScalar_at_siteA]
  norm_num

private theorem weightedScalar_siteB_singletonA :
    naiveWeightedCubicalDifferential
      (scalarCochain 1 naiveWeightTestScalarProfile)
      (naiveWeightTestSiteB, singletonFockState D0.A) = 1 := by
  rw [naiveWeightedScalar_singleton, naiveWeightSqrt_at_siteB,
    roleTranslateA_siteB_eq_siteAB, naiveScalar_at_siteAB, naiveScalar_at_siteB]
  norm_num

private theorem weightedScalar_origin_singletonA :
    naiveWeightedCubicalDifferential
      (scalarCochain 1 naiveWeightTestScalarProfile)
      (naiveWeightTestOrigin, singletonFockState D0.A) = 0 := by
  rw [naiveWeightedScalar_singleton, naiveWeightSqrt_at_origin]
  rw [show roleTranslatePlus 1 D0.A naiveWeightTestOrigin = naiveWeightTestSiteA by rfl,
    naiveScalar_at_siteA, naiveScalar_at_origin]
  norm_num

private theorem weightedScalar_origin_singletonB :
    naiveWeightedCubicalDifferential
      (scalarCochain 1 naiveWeightTestScalarProfile)
      (naiveWeightTestOrigin, singletonFockState D0.B) = 0 := by
  rw [naiveWeightedScalar_singleton, naiveWeightSqrt_at_origin]
  rw [show roleTranslatePlus 1 D0.B naiveWeightTestOrigin = naiveWeightTestSiteB by rfl,
    naiveScalar_at_siteB, naiveScalar_at_origin]
  norm_num

private theorem carCreate_pair_A_sparse (ket : ArchiveFockState)
    (hket : ket ≠ singletonFockState D0.B) :
    carCreate D0.A naiveWeightTestPairState ket = 0 := by
  by_contra hzero
  have hs := carCreate_support D0.A naiveWeightTestPairState ket hzero
  have hB : ket D0.B = true := by
    have h := hs.2.2 D0.B (by decide)
    simpa [naiveWeightTestPairState] using h.symm
  have hstate : ket = singletonFockState D0.B := by
    funext s
    by_cases hsA : s = D0.A
    · subst s
      simpa [fockSingletonState, D0.A, D0.B] using hs.2.1
    · by_cases hsB : s = D0.B
      · subst s
        exact hB
      · have h := hs.2.2 s hsA
        have hpair : naiveWeightTestPairState s = false := by
          simp [naiveWeightTestPairState, hsA, hsB]
        have hfalse : ket s = false := by
          simpa [hpair] using h.symm
        simpa [fockSingletonState, hsB] using hfalse
  exact hket hstate

private theorem carCreate_pair_B_sparse (ket : ArchiveFockState)
    (hket : ket ≠ singletonFockState D0.A) :
    carCreate D0.B naiveWeightTestPairState ket = 0 := by
  by_contra hzero
  have hs := carCreate_support D0.B naiveWeightTestPairState ket hzero
  have hA : ket D0.A = true := by
    have h := hs.2.2 D0.A (by decide)
    simpa [naiveWeightTestPairState] using h.symm
  have hstate : ket = singletonFockState D0.A := by
    funext s
    by_cases hsB : s = D0.B
    · subst s
      simpa [fockSingletonState, D0.A, D0.B] using hs.2.1
    · by_cases hsA : s = D0.A
      · subst s
        exact hA
      · have h := hs.2.2 s hsB
        have hpair : naiveWeightTestPairState s = false := by
          simp [naiveWeightTestPairState, hsA, hsB]
        have hfalse : ket s = false := by
          simpa [hpair] using h.symm
        simpa [fockSingletonState, hsA] using hfalse
  exact hket hstate

private theorem carCreate_pair_C_zero (ket : ArchiveFockState) :
    carCreate D0.C naiveWeightTestPairState ket = 0 := by
  by_contra hzero
  have hs := carCreate_support D0.C naiveWeightTestPairState ket hzero
  have hpair := hs.1
  simp [naiveWeightTestPairState, D0.C, D0.A, D0.B] at hpair

private theorem carCreate_pair_D_zero (ket : ArchiveFockState) :
    carCreate D0.D naiveWeightTestPairState ket = 0 := by
  by_contra hzero
  have hs := carCreate_support D0.D naiveWeightTestPairState ket hzero
  have hpair := hs.1
  simp [naiveWeightTestPairState, D0.D, D0.A, D0.B] at hpair

private theorem carCreate_pair_A_singletonB :
    carCreate D0.A naiveWeightTestPairState (singletonFockState D0.B) = 1 := by
  have h : carCreateInt D0.A naiveWeightTestPairState (singletonFockState D0.B) = 1 := by
    native_decide
  rw [carCreate_eq_intCast, h]
  norm_num

private theorem carCreate_pair_B_singletonA :
    carCreate D0.B naiveWeightTestPairState (singletonFockState D0.A) = -1 := by
  have h : carCreateInt D0.B naiveWeightTestPairState (singletonFockState D0.A) = -1 := by
    native_decide
  rw [carCreate_eq_intCast, h]
  norm_num

private theorem role_sum_expand (F : Role → ℝ) :
    (∑ r : Role, F r) = F D0.A + F D0.B + F D0.C + F D0.D := by
  classical
  have huniv : (Finset.univ : Finset Role) =
      insert D0.D (insert D0.C (insert D0.B {D0.A})) := by
    decide
  rw [huniv]
  simp [D0.A, D0.B, D0.C, D0.D]
  ring

private theorem pair_sum_A (ψ : ArchiveCochain 1)
    (xplus x : ArchiveRolePhaseGroup 1) :
    (∑ ket : ArchiveFockState,
      carCreate D0.A naiveWeightTestPairState ket * (ψ (xplus, ket) - ψ (x, ket))) =
      carCreate D0.A naiveWeightTestPairState (singletonFockState D0.B) *
        (ψ (xplus, singletonFockState D0.B) - ψ (x, singletonFockState D0.B)) := by
  classical
  rw [Finset.sum_eq_single (singletonFockState D0.B)]
  · intro ket _ hket
    rw [carCreate_pair_A_sparse ket hket]
    simp
  · simp

private theorem pair_sum_B (ψ : ArchiveCochain 1)
    (xplus x : ArchiveRolePhaseGroup 1) :
    (∑ ket : ArchiveFockState,
      carCreate D0.B naiveWeightTestPairState ket * (ψ (xplus, ket) - ψ (x, ket))) =
      carCreate D0.B naiveWeightTestPairState (singletonFockState D0.A) *
        (ψ (xplus, singletonFockState D0.A) - ψ (x, singletonFockState D0.A)) := by
  classical
  rw [Finset.sum_eq_single (singletonFockState D0.A)]
  · intro ket _ hket
    rw [carCreate_pair_B_sparse ket hket]
    simp
  · simp

private theorem pair_sum_C (ψ : ArchiveCochain 1)
    (xplus x : ArchiveRolePhaseGroup 1) :
    (∑ ket : ArchiveFockState,
      carCreate D0.C naiveWeightTestPairState ket * (ψ (xplus, ket) - ψ (x, ket))) = 0 := by
  classical
  apply Finset.sum_eq_zero
  intro ket _
  rw [carCreate_pair_C_zero]
  simp

private theorem pair_sum_D (ψ : ArchiveCochain 1)
    (xplus x : ArchiveRolePhaseGroup 1) :
    (∑ ket : ArchiveFockState,
      carCreate D0.D naiveWeightTestPairState ket * (ψ (xplus, ket) - ψ (x, ket))) = 0 := by
  classical
  apply Finset.sum_eq_zero
  intro ket _
  rw [carCreate_pair_D_zero]
  simp

/-- Exact evaluation of the two-step weighted differential on the CAR16
carrier: the selected degree-two coefficient is `1`, hence is nonzero. -/
theorem naive_weighted_cubical_differential_square_witness :
    naiveWeightedCubicalDifferential
      (naiveWeightedCubicalDifferential
        (scalarCochain 1 naiveWeightTestScalarProfile))
      (naiveWeightTestOrigin, naiveWeightTestPairState) = 1 := by
  classical
  let ψ : ArchiveCochain 1 :=
    naiveWeightedCubicalDifferential (scalarCochain 1 naiveWeightTestScalarProfile)
  change Real.sqrt (naiveWeightTestSiteProfile naiveWeightTestOrigin) *
      cubicalCoboundary 1 ψ (naiveWeightTestOrigin, naiveWeightTestPairState) = 1
  rw [naiveWeightSqrt_at_origin, one_mul, cubicalCoboundary_apply]
  rw [role_sum_expand]
  change
    (∑ ket : ArchiveFockState,
      carCreate D0.A naiveWeightTestPairState ket *
        (ψ (naiveWeightTestSiteA, ket) - ψ (naiveWeightTestOrigin, ket))) +
    (∑ ket : ArchiveFockState,
      carCreate D0.B naiveWeightTestPairState ket *
        (ψ (naiveWeightTestSiteB, ket) - ψ (naiveWeightTestOrigin, ket))) +
    (∑ ket : ArchiveFockState,
      carCreate D0.C naiveWeightTestPairState ket *
        (ψ (roleTranslatePlus 1 D0.C naiveWeightTestOrigin, ket) -
          ψ (naiveWeightTestOrigin, ket))) +
    (∑ ket : ArchiveFockState,
      carCreate D0.D naiveWeightTestPairState ket *
        (ψ (roleTranslatePlus 1 D0.D naiveWeightTestOrigin, ket) -
          ψ (naiveWeightTestOrigin, ket))) = 1
  rw [pair_sum_A, pair_sum_B, pair_sum_C, pair_sum_D]
  rw [show ψ = naiveWeightedCubicalDifferential
    (scalarCochain 1 naiveWeightTestScalarProfile) by rfl]
  rw [carCreate_pair_A_singletonB, carCreate_pair_B_singletonA,
    weightedScalar_siteA_singletonB, weightedScalar_origin_singletonB,
    weightedScalar_siteB_singletonA, weightedScalar_origin_singletonA]
  norm_num

/-- The selected output label is a degree-two CAR state. -/
theorem naiveWeightTestPairState_degree_two :
    fockDegree naiveWeightTestPairState = 2 := by
  native_decide

/-- The counterexample starts from an actual scalar (degree-zero) cochain. -/
theorem naiveWeightTestInput_homogeneous_degree_zero :
    HomogeneousCochain 1 0 (scalarCochain 1 naiveWeightTestScalarProfile) := by
  intro x S hS
  by_cases h : S = vacuumFockState
  · subst S
    simp [fockDegree, fockVacuumState] at hS
  · simp [scalarCochain, h]

/-- Current finite owner slice: the sample weights differ, the full four-role
carrier is used, and the chosen scalar input has a nonzero degree-two output
after two weighted steps. This is one explicit counterexample, not a universal
no-go for all nonconstant weights. -/
theorem archive_naive_weighted_car_degree_leakage_nogo_owner :
    (Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1) ∧
    (Fintype.card Role = 4) ∧
    (fockDegree naiveWeightTestPairState = 2) ∧
    HomogeneousCochain 1 0 (scalarCochain 1 naiveWeightTestScalarProfile) ∧
    (naiveWeightedCubicalDifferential
      (naiveWeightedCubicalDifferential
        (scalarCochain 1 naiveWeightTestScalarProfile))
      (naiveWeightTestOrigin, naiveWeightTestPairState) = 1) ∧
    (naiveWeightedCubicalDifferential
      (naiveWeightedCubicalDifferential
        (scalarCochain 1 naiveWeightTestScalarProfile))
      (naiveWeightTestOrigin, naiveWeightTestPairState) ≠ 0) := by
  exact ⟨sqrt_naive_weights_ne, card_role,
    naiveWeightTestPairState_degree_two,
    naiveWeightTestInput_homogeneous_degree_zero,
    naive_weighted_cubical_differential_square_witness,
    ne_of_eq_of_ne naive_weighted_cubical_differential_square_witness (by norm_num)⟩

/-- Registry-name compatibility wrapper. It exposes the same finite witness
and therefore does not assert the broader universal wording of the claim row. -/
theorem archive_naive_weighted_degree_leakage_nogo_owner :
    (Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1) ∧
    (Fintype.card Role = 4) ∧
    (fockDegree naiveWeightTestPairState = 2) ∧
    HomogeneousCochain 1 0 (scalarCochain 1 naiveWeightTestScalarProfile) ∧
    (naiveWeightedCubicalDifferential
      (naiveWeightedCubicalDifferential
        (scalarCochain 1 naiveWeightTestScalarProfile))
      (naiveWeightTestOrigin, naiveWeightTestPairState) = 1) ∧
    (naiveWeightedCubicalDifferential
      (naiveWeightedCubicalDifferential
        (scalarCochain 1 naiveWeightTestScalarProfile))
      (naiveWeightTestOrigin, naiveWeightTestPairState) ≠ 0) :=
  archive_naive_weighted_car_degree_leakage_nogo_owner

end D0.Geometry
