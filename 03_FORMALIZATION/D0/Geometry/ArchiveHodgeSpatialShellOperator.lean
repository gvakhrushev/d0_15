import Mathlib.Tactic
import D0.Geometry.ArchiveCARDirac
import D0.Geometry.ArchiveDiagonalRoleTransport
import D0.Geometry.ArchiveHodgeCARDiracKernel
import D0.Geometry.ArchiveSpatialHistorySplit

/-!
# Spatial Role stabilizer and the first Hodge shell

The diagonal Role action preserves the A-invariant sector only for permutations
that fix `A`. On that stabilizer the rank-96 spatial shell is an invariant
operator carrier of `D_H²`, with eigenvalue `shellEnergy ^ 2`.

`spatialShellHodgeSquareCompression` is that restricted square. It is not the
BOOK finite feedback operator: nothing here identifies it with
`P_N U_N† Q_N U_N P_N`.
-/

namespace D0.Geometry

open D0
open RoleFockPermutation
open D0.Geometry.ArchiveRolePhaseProductCarrier
open scoped BigOperators Matrix

noncomputable section

variable {N : ℕ}

def FixesRoleA (σ : Equiv.Perm Role) : Prop :=
  σ A = A

abbrev SpatialRoleStabilizer := {σ : Equiv.Perm Role // FixesRoleA σ}

lemma FixesRoleA.symm {σ : Equiv.Perm Role} (hσ : FixesRoleA σ) :
    FixesRoleA σ.symm := by
  unfold FixesRoleA at hσ ⊢
  have h := congrArg σ.symm hσ
  simp only [Equiv.symm_apply_apply] at h
  exact h.symm

theorem spatialRoleTransport_preserves_axisInvariant (σ : Equiv.Perm Role)
    (hσ : FixesRoleA σ) (ψ : axisInvariantCochainSubmodule N) :
    diagonalRoleTransport σ ψ.val ∈ axisInvariantCochainSubmodule N := by
  intro x s
  have hA : σ.symm A = A := hσ.symm
  have hsite := permuteRoleSite_translatePlus σ.symm A x
  rw [hA] at hsite
  simp only [diagonalRoleTransport]
  refine Finset.sum_congr rfl fun ket _ => ?_
  have hinv := ψ.property (permuteRoleSite σ.symm x) ket
  rw [hsite, hinv]

/-- A permutation that moves `A` need not preserve the A-invariant sector. -/
theorem roleTransport_movingA_not_axisInvariant :
    ∃ σ : Equiv.Perm Role, ¬ FixesRoleA σ ∧
      ∃ ψ : axisInvariantCochainSubmodule 1,
        diagonalRoleTransport σ ψ.val ∉ axisInvariantCochainSubmodule 1 := by
  classical
  refine ⟨swapAB, ?_, ?_⟩
  · intro h
    have : B = A := by simpa [FixesRoleA, swapAB, Equiv.swap_apply_left] using h
    simp [A, B] at this
  · have hmem : bVacuumCochain ∈ axisInvariantCochainSubmodule 1 := by
      intro x s
      have hne : B ≠ A := by decide
      simp [bVacuumCochain, bZeroIndicator, roleTranslatePlus_apply, roleStep, hne]
    refine ⟨⟨bVacuumCochain, hmem⟩, ?_⟩
    intro hinv
    have hone : diagonalRoleTransport swapAB bVacuumCochain
        (witnessOrigin, fockVacuumState) = 1 := by
      classical
      simp only [diagonalRoleTransport]
      rw [Finset.sum_eq_single fockVacuumState]
      · have hsite : permuteRoleSite swapAB.symm witnessOrigin = witnessOrigin := by
          funext r
          simp [permuteRoleSite, witnessOrigin]
        have hsign : signedTransport swapAB fockVacuumState fockVacuumState = 1 := by
          unfold signedTransport
          rw [show transportState swapAB fockVacuumState = fockVacuumState by funext r; rfl]
          unfold fermionSign occupiedInversionCount fockVacuumState
          simp
        rw [hsite, hsign]
        simp [bVacuumCochain, bZeroIndicator, witnessOrigin]
      · intro ket _ hket
        simp [bVacuumCochain, hket]
      · intro hmem
        exact (hmem (Finset.mem_univ _)).elim
    have hzero : diagonalRoleTransport swapAB bVacuumCochain
        (roleTranslatePlus 1 A witnessOrigin, fockVacuumState) = 0 := by
      classical
      simp only [diagonalRoleTransport]
      rw [Finset.sum_eq_single fockVacuumState]
      · have hsite := permuteRoleSite_translatePlus swapAB.symm A witnessOrigin
        have hstep : swapAB.symm A = B := by
          simp [swapAB, Equiv.swap_apply_left]
        rw [hstep] at hsite
        have hsign : signedTransport swapAB fockVacuumState fockVacuumState = 1 := by
          unfold signedTransport
          rw [show transportState swapAB fockVacuumState = fockVacuumState by funext r; rfl]
          unfold fermionSign occupiedInversionCount fockVacuumState
          simp
        rw [hsite, hsign]
        have hpre : permuteRoleSite swapAB.symm witnessOrigin = witnessOrigin := by
          funext t
          simp [permuteRoleSite, witnessOrigin]
        have hB : roleTranslatePlus 1 B witnessOrigin B = 1 := by
          simp [roleTranslatePlus_apply, witnessOrigin, roleStep]
        rw [hpre]
        have hne : (1 : ZMod (archiveFibers 1)) ≠ 0 := by
          rw [show archiveFibers 1 = 3 by simp [archiveFibers]]
          decide
        simp [bVacuumCochain, bZeroIndicator, hB, hne]
      · intro ket _ hket
        simp [bVacuumCochain, hket]
      · intro hmem
        exact (hmem (Finset.mem_univ _)).elim
    have hagree := hinv witnessOrigin fockVacuumState
    rw [hone, hzero] at hagree
    norm_num at hagree

def spatialDiagonalTransport (σ : Equiv.Perm Role) (hσ : FixesRoleA σ)
    (φ : SpatialArchiveCochain N) : SpatialArchiveCochain N :=
  axisInvariantCochainEquivSpatial N
    ⟨diagonalRoleTransport σ (spatialCochainPullback N φ),
      spatialRoleTransport_preserves_axisInvariant σ hσ
        ⟨spatialCochainPullback N φ, spatialCochainPullback_invariant N φ⟩⟩

theorem spatialRoleTransport_commutes_axisInvariantHodgeSquare
    (σ : Equiv.Perm Role) (hσ : FixesRoleA σ)
    (ψ : axisInvariantCochainSubmodule N) :
    axisInvariantHodgeSquare N
        ⟨diagonalRoleTransport σ ψ.val,
          spatialRoleTransport_preserves_axisInvariant σ hσ ψ⟩ =
      ⟨diagonalRoleTransport σ (axisInvariantHodgeSquare N ψ).val,
        spatialRoleTransport_preserves_axisInvariant σ hσ
          (axisInvariantHodgeSquare N ψ)⟩ := by
  apply Subtype.ext
  exact (diagonalRoleTransport_commutes_hodgeSquare σ ψ.val).symm

theorem spatialRoleTransport_commutes_spatialLaplacian
    (σ : Equiv.Perm Role) (hσ : FixesRoleA σ) (φ : SpatialArchiveCochain N) :
    spatialDiagonalTransport σ hσ (spatialCochainLaplacian N φ) =
      spatialCochainLaplacian N (spatialDiagonalTransport σ hσ φ) := by
  let pulled : axisInvariantCochainSubmodule N :=
    ⟨spatialCochainPullback N φ, spatialCochainPullback_invariant N φ⟩
  let transported : axisInvariantCochainSubmodule N :=
    ⟨diagonalRoleTransport σ pulled.val,
      spatialRoleTransport_preserves_axisInvariant σ hσ pulled⟩
  have hcomm := diagonalRoleTransport_commutes_hodgeSquare σ pulled.val
  have hsq := spatialCochainPullback_hodgeSquare N φ
  have hsub :
      axisInvariantHodgeSquare N transported =
        ⟨diagonalRoleTransport σ (spatialCochainPullback N (spatialCochainLaplacian N φ)),
          spatialRoleTransport_preserves_axisInvariant σ hσ
            ⟨spatialCochainPullback N (spatialCochainLaplacian N φ),
              spatialCochainPullback_invariant N _⟩⟩ := by
    apply Subtype.ext
    change hodgeCarDirac N (hodgeCarDirac N (diagonalRoleTransport σ pulled.val)) =
      diagonalRoleTransport σ (spatialCochainPullback N (spatialCochainLaplacian N φ))
    rw [← hcomm, hsq]
  have hread := congrArg (axisInvariantCochainEquivSpatial N) hsub
  rw [axisInvariant_hodgeSquare_equiv_spatialLaplacian] at hread
  simpa [spatialDiagonalTransport, transported, pulled] using hread.symm

/-! ## The first shell as one operator carrier -/

def spatialShellSubmodule (N : ℕ) : Submodule ℝ (ArchiveCochain N) :=
  Submodule.span ℝ (Set.range (shellCochain N))

theorem spatialShellSubmodule_finrank (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    Module.finrank ℝ (spatialShellSubmodule N) = 96 := by
  simpa [spatialShellSubmodule] using spatial_shell_rank N hL

def hodgeShellEigen (N : ℕ) : Submodule ℝ (ArchiveCochain N) where
  carrier := {ψ | hodgeCarDirac N (hodgeCarDirac N ψ) =
    shellEnergy (archiveFibers N) ^ 2 • ψ}
  zero_mem' := by simp [hodgeCarDirac_zero]
  add_mem' := by
    intro a b ha hb
    simp only [Set.mem_setOf_eq] at ha hb ⊢
    rw [hodgeCarDirac_add, hodgeCarDirac_add, ha, hb, smul_add]
  smul_mem' := by
    intro c a ha
    simp only [Set.mem_setOf_eq] at ha ⊢
    rw [hodgeCarDirac_smul, hodgeCarDirac_smul, ha]
    rw [smul_comm]

theorem spatialShell_le_eigen (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    spatialShellSubmodule N ≤ hodgeShellEigen N := by
  rw [spatialShellSubmodule, Submodule.span_le]
  intro ψ hψ
  rcases hψ with ⟨p, rfl⟩
  have h2 : 2 ≤ archiveFibers N := by omega
  change hodgeCarDirac N (hodgeCarDirac N (shellCochain N p)) =
    shellEnergy (archiveFibers N) ^ 2 • shellCochain N p
  exact shellCochain_eigen N p h2

theorem hodgeSquare_on_spatialShell (N : ℕ) (hL : 3 ≤ archiveFibers N)
    (ψ : spatialShellSubmodule N) :
    hodgeCarDirac N (hodgeCarDirac N ψ.val) =
      shellEnergy (archiveFibers N) ^ 2 • ψ.val :=
  (spatialShell_le_eigen N hL) ψ.property

theorem hodgeSquare_maps_spatialShell (N : ℕ) (hL : 3 ≤ archiveFibers N)
    {ψ : ArchiveCochain N} (hψ : ψ ∈ spatialShellSubmodule N) :
    (hodgeCarDiracₗ N ∘ₗ hodgeCarDiracₗ N) ψ ∈ spatialShellSubmodule N := by
  change hodgeCarDirac N (hodgeCarDirac N ψ) ∈ spatialShellSubmodule N
  rw [hodgeSquare_on_spatialShell N hL ⟨ψ, hψ⟩]
  exact Submodule.smul_mem _ _ hψ

/-- Hodge square compressed onto the spatial first shell.

This operator is `shellEnergy (archiveFibers N) ^ 2` times the identity on
`spatialShellSubmodule N`. It is not the BOOK finite feedback operator.
-/
def spatialShellHodgeSquareCompression (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    spatialShellSubmodule N →ₗ[ℝ] spatialShellSubmodule N :=
  (hodgeCarDiracₗ N ∘ₗ hodgeCarDiracₗ N).restrict
    (fun _ hψ => hodgeSquare_maps_spatialShell N hL hψ)

theorem hodgeSquare_on_spatialShell_eq (N : ℕ) (hL : 3 ≤ archiveFibers N) :
    spatialShellHodgeSquareCompression N hL =
      shellEnergy (archiveFibers N) ^ 2 • LinearMap.id := by
  ext ψ q
  simp only [spatialShellHodgeSquareCompression, LinearMap.restrict_apply,
    LinearMap.comp_apply, LinearMap.smul_apply, LinearMap.id_apply]
  exact congr_fun (hodgeSquare_on_spatialShell N hL ψ) q

def permutedShellAxis (σ : Equiv.Perm Role) (hσ : FixesRoleA σ)
    (a : SpatialAxis) : SpatialAxis :=
  spatialAxisEquivRole.symm ⟨σ (spatialAxisRole a), by
    intro hA
    have hrole : spatialAxisRole a = A := by
      have hsym := congrArg σ.symm hA
      simp only [Equiv.symm_apply_apply] at hsym
      rw [show σ.symm A = A from hσ.symm] at hsym
      exact hsym
    cases a <;> simp [spatialAxisRole, A, B, C, D] at hrole⟩

lemma permutedShellAxis_role (σ : Equiv.Perm Role) (hσ : FixesRoleA σ)
    (a : SpatialAxis) :
    spatialAxisRole (permutedShellAxis σ hσ a) = σ (spatialAxisRole a) := by
  simpa [permutedShellAxis] using
    (spatialAxisEquivRole_val (spatialAxisEquivRole.symm
      ⟨σ (spatialAxisRole a), by
        intro hA
        have hrole : spatialAxisRole a = A := by
          have hsym := congrArg σ.symm hA
          simp only [Equiv.symm_apply_apply] at hsym
          rw [show σ.symm A = A from hσ.symm] at hsym
          exact hsym
        cases a <;> simp [spatialAxisRole, A, B, C, D] at hrole⟩)).symm

lemma shellMode_permuteRoleSite (σ : Equiv.Perm Role) (hσ : FixesRoleA σ)
    (a : SpatialAxis) (h : ShellHarmonic) (x : ArchiveRolePhaseGroup N) :
    shellMode N (a, h) (permuteRoleSite σ.symm x) =
      shellMode N (permutedShellAxis σ hσ a, h) x := by
  have hrole := permutedShellAxis_role σ hσ a
  cases h
  · simp only [shellMode, shellCos, permuteRoleSite, Equiv.symm_symm, hrole]
  · simp only [shellMode, shellSin, permuteRoleSite, Equiv.symm_symm, hrole]

theorem diagonalRoleTransport_shellCochain (σ : Equiv.Perm Role) (hσ : FixesRoleA σ)
    (p : (SpatialAxis × ShellHarmonic) × ArchiveFockState) :
    diagonalRoleTransport σ (shellCochain N p) =
      (fermionSign σ p.2 : ℝ) •
        shellCochain N
          ((permutedShellAxis σ hσ p.1.1, p.1.2), transportState σ p.2) := by
  classical
  funext q
  simp only [diagonalRoleTransport, shellCochain, Pi.smul_apply, smul_eq_mul]
  rw [Finset.sum_eq_single p.2]
  · rw [shellMode_permuteRoleSite σ hσ]
    by_cases htr : q.2 = transportState σ p.2
    · have hsign : signedTransport σ q.2 p.2 = fermionSign σ p.2 := by
        unfold signedTransport
        rw [if_pos htr]
      rw [hsign, htr]
      simp
    · have hε : signedTransport σ q.2 p.2 = 0 := by
        unfold signedTransport
        rw [if_neg htr]
      simp [hε, htr]
  · intro ket _ hket
    simp [hket]
  · intro hmem
    exact (hmem (Finset.mem_univ _)).elim

theorem spatialRoleTransport_preserves_shell (σ : Equiv.Perm Role) (hσ : FixesRoleA σ) :
    (spatialShellSubmodule N).map (diagonalRoleLinearEquiv σ).toLinearMap =
      spatialShellSubmodule N := by
  apply le_antisymm
  · rw [spatialShellSubmodule, LinearMap.map_span_le]
    intro ψ hψ
    rcases hψ with ⟨p, rfl⟩
    change diagonalRoleTransport σ (shellCochain N p) ∈ spatialShellSubmodule N
    rw [diagonalRoleTransport_shellCochain σ hσ p]
    exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨_, rfl⟩)
  · intro ψ hψ
    refine ⟨diagonalRoleTransport σ.symm ψ, ?_, diagonalRoleTransport_right_inv σ ψ⟩
    induction hψ using Submodule.span_induction with
    | mem φ hφ =>
        rcases hφ with ⟨p, rfl⟩
        change diagonalRoleTransport σ.symm (shellCochain N p) ∈ spatialShellSubmodule N
        rw [diagonalRoleTransport_shellCochain σ.symm hσ.symm p]
        exact Submodule.smul_mem _ _ (Submodule.subset_span ⟨_, rfl⟩)
    | zero =>
        have h0 : diagonalRoleTransport σ.symm (0 : ArchiveCochain N) = 0 := by
          simpa using diagonalRoleTransport_smul σ.symm (0 : ℝ) (0 : ArchiveCochain N)
        rw [h0]
        exact Submodule.zero_mem _
    | add x y _ _ hx hy =>
        rw [diagonalRoleTransport_add]
        exact Submodule.add_mem _ hx hy
    | smul c x _ hx =>
        rw [diagonalRoleTransport_smul]
        exact Submodule.smul_mem _ c hx

/-! ## Hopping comparison

The same diagonal action commutes with `hoppingCarDirac`. The distinction
between hopping and the Hodge operator remains their dispersion, not this
finite Role symmetry.
-/

def hoppingRoleTransport (n : ℕ) (σ : Equiv.Perm Role)
    (v : CARHilbertPoint n → ℝ) : CARHilbertPoint n → ℝ :=
  fun p => ∑ ket : ArchiveFockState,
    (signedTransport σ p.2 ket : ℝ) * v (permuteRole n σ p.1, ket)

lemma spatialDiracComponent_permute (n : ℕ) (σ : Equiv.Perm Role) (r : Role)
    (x y : ArchiveRolePhasePoint n) :
    spatialDiracComponent n r (permuteRole n σ x) (permuteRole n σ y) =
      spatialDiracComponent n (σ r) x y := by
  classical
  unfold spatialDiracComponent
  dsimp [permuteRole]
  apply if_congr
  · constructor
    · rintro ⟨hoff, hnear⟩
      refine ⟨?_, hnear⟩
      intro t ht
      have hs : σ.symm t ≠ r := by
        intro hs
        apply ht
        simpa using congrArg σ hs
      simpa using hoff (σ.symm t) hs
    · rintro ⟨hoff, hnear⟩
      refine ⟨?_, hnear⟩
      intro s hs
      exact hoff (σ s) (by
        intro hsr
        apply hs
        simpa using congrArg σ.symm hsr)
  · rfl
  · rfl

lemma fockGamma_signed_commute (σ : Equiv.Perm Role) (r : Role)
    (bra ket : ArchiveFockState) :
    (∑ mid, (signedTransport σ bra mid : ℝ) * fockGamma r mid ket) =
      ∑ mid, fockGamma (σ r) bra mid * (signedTransport σ mid ket : ℝ) := by
  classical
  simp only [fockGamma]
  calc
    (∑ mid, (signedTransport σ bra mid : ℝ) *
        (carAnnihilate r mid ket + carCreate r mid ket)) =
      (∑ mid, (signedTransport σ bra mid : ℝ) * carAnnihilate r mid ket) +
        ∑ mid, (signedTransport σ bra mid : ℝ) * carCreate r mid ket := by
        rw [← Finset.sum_add_distrib]
        refine Finset.sum_congr rfl fun mid _ => ?_
        ring
    _ = (∑ mid, carAnnihilate (σ r) bra mid * (signedTransport σ mid ket : ℝ)) +
        ∑ mid, carCreate (σ r) bra mid * (signedTransport σ mid ket : ℝ) := by
        rw [real_signed_annihilate_commute, real_signed_create_commute]
    _ = ∑ mid, fockGamma (σ r) bra mid * (signedTransport σ mid ket : ℝ) := by
        simp only [fockGamma]
        rw [← Finset.sum_add_distrib]
        refine Finset.sum_congr rfl fun mid _ => ?_
        ring

theorem hoppingRoleTransport_commutes_hoppingCarDirac (n : ℕ) (σ : Equiv.Perm Role)
    (v : CARHilbertPoint n → ℝ) :
    hoppingRoleTransport n σ ((hoppingCarDirac n).mulVec v) =
      (hoppingCarDirac n).mulVec (hoppingRoleTransport n σ v) := by
  classical
  funext p
  rcases p with ⟨x, f⟩
  simp only [hoppingRoleTransport, Matrix.mulVec, dotProduct, hoppingCarDirac, carDirac]
  calc
    (∑ ket, (signedTransport σ f ket : ℝ) *
        ∑ q : CARHilbertPoint n,
          (∑ r, spatialDiracComponent n r (permuteRole n σ x) q.1 * fockGamma r ket q.2) *
            v q) =
      ∑ ket, (signedTransport σ f ket : ℝ) *
        ∑ y, ∑ g, (∑ r, spatialDiracComponent n r (permuteRole n σ x) y *
            fockGamma r ket g) * v (y, g) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [Fintype.sum_prod_type]
    _ = ∑ ket, ∑ y, ∑ g, ∑ r,
        (signedTransport σ f ket : ℝ) *
          (spatialDiracComponent n r (permuteRole n σ x) y * fockGamma r ket g) *
            v (y, g) := by
        refine Finset.sum_congr rfl fun ket _ => ?_
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun y _ => ?_
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun g _ => ?_
        rw [← mul_assoc, Finset.mul_sum, Finset.sum_mul]
    _ =
      ∑ y, ∑ g, ∑ r, ∑ ket,
        (signedTransport σ f ket : ℝ) *
          (spatialDiracComponent n r (permuteRole n σ x) y * fockGamma r ket g) *
            v (y, g) := by
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun y _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun g _ => ?_
        rw [Finset.sum_comm]
    _ = ∑ z, ∑ g, ∑ r, ∑ ket,
        (signedTransport σ f ket : ℝ) *
          (spatialDiracComponent n r (permuteRole n σ x) (permuteRole n σ z) *
            fockGamma r ket g) * v (permuteRole n σ z, g) := by
        let e := permuteRole n σ
        have hsite := (e.sum_comp fun y =>
          ∑ g, ∑ r, ∑ ket,
            (signedTransport σ f ket : ℝ) *
              (spatialDiracComponent n r (permuteRole n σ x) y * fockGamma r ket g) *
                v (y, g)).symm
        simpa [e] using hsite
    _ = ∑ z, ∑ g, ∑ r,
        spatialDiracComponent n (σ r) x z *
          (∑ ket, (signedTransport σ f ket : ℝ) * fockGamma r ket g) *
            v (permuteRole n σ z, g) := by
        refine Finset.sum_congr rfl fun z _ => ?_
        refine Finset.sum_congr rfl fun g _ => ?_
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [spatialDiracComponent_permute]
        calc
          (∑ ket, (signedTransport σ f ket : ℝ) *
              (spatialDiracComponent n (σ r) x z * fockGamma r ket g) *
                v (permuteRole n σ z, g)) =
            ∑ ket, spatialDiracComponent n (σ r) x z *
              ((signedTransport σ f ket : ℝ) * fockGamma r ket g) *
                v (permuteRole n σ z, g) := by
              refine Finset.sum_congr rfl fun ket _ => ?_
              ring
          _ = (spatialDiracComponent n (σ r) x z *
                ∑ ket, (signedTransport σ f ket : ℝ) * fockGamma r ket g) *
              v (permuteRole n σ z, g) := by
              rw [← Finset.sum_mul, ← Finset.mul_sum]
    _ = ∑ z, ∑ g, ∑ r,
        spatialDiracComponent n (σ r) x z *
          (∑ mid, fockGamma (σ r) f mid * (signedTransport σ mid g : ℝ)) *
            v (permuteRole n σ z, g) := by
        refine Finset.sum_congr rfl fun z _ => ?_
        refine Finset.sum_congr rfl fun g _ => ?_
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [fockGamma_signed_commute]
    _ = ∑ z, ∑ g, ∑ r,
        spatialDiracComponent n r x z *
          (∑ mid, fockGamma r f mid * (signedTransport σ mid g : ℝ)) *
            v (permuteRole n σ z, g) := by
        refine Finset.sum_congr rfl fun z _ => ?_
        refine Finset.sum_congr rfl fun g _ => ?_
        simpa using (Equiv.sum_comp σ fun r =>
          spatialDiracComponent n r x z *
            (∑ mid, fockGamma r f mid * (signedTransport σ mid g : ℝ)) *
              v (permuteRole n σ z, g))
    _ = ∑ z, ∑ g, ∑ r, ∑ mid,
        spatialDiracComponent n r x z * fockGamma r f mid *
          (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g) := by
        refine Finset.sum_congr rfl fun z _ => ?_
        refine Finset.sum_congr rfl fun g _ => ?_
        refine Finset.sum_congr rfl fun r _ => ?_
        rw [Finset.mul_sum, Finset.sum_mul]
        refine Finset.sum_congr rfl fun mid _ => ?_
        ring
    _ = ∑ z, ∑ mid, ∑ g, ∑ r,
        spatialDiracComponent n r x z * fockGamma r f mid *
          (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g) := by
        refine Finset.sum_congr rfl fun z _ => ?_
        conv_lhs =>
          enter [2]
          ext g
          rw [Finset.sum_comm]
        exact Finset.sum_comm
    _ = ∑ z, ∑ mid,
        (∑ r, spatialDiracComponent n r x z * fockGamma r f mid) *
          (∑ g, (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) := by
        refine Finset.sum_congr rfl fun z _ => ?_
        refine Finset.sum_congr rfl fun mid _ => ?_
        have hR :
            (∑ r, spatialDiracComponent n r x z * fockGamma r f mid) *
              (∑ g, (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) =
              ∑ g, (∑ r, spatialDiracComponent n r x z * fockGamma r f mid) *
                ((signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) := by
          rw [Finset.mul_sum]
        calc
          (∑ g : ArchiveFockState, ∑ r : Role,
              spatialDiracComponent n r x z * fockGamma r f mid *
                (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) =
            ∑ g : ArchiveFockState,
              (∑ r : Role, spatialDiracComponent n r x z * fockGamma r f mid) *
                ((signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) := by
              refine Finset.sum_congr rfl fun g _ => ?_
              have hterm : ∀ r : Role,
                  spatialDiracComponent n r x z * fockGamma r f mid *
                    (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g) =
                  (spatialDiracComponent n r x z * fockGamma r f mid) *
                    ((signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) := by
                intro r
                ring
              simp_rw [hterm]
              rw [← Finset.sum_mul]
          _ = (∑ r, spatialDiracComponent n r x z * fockGamma r f mid) *
              (∑ g, (signedTransport σ mid g : ℝ) * v (permuteRole n σ z, g)) :=
              hR.symm
    _ = ∑ z, ∑ mid,
        (∑ r, spatialDiracComponent n r x z * fockGamma r f mid) *
          hoppingRoleTransport n σ v (z, mid) := by
        rfl
    _ = (hoppingCarDirac n).mulVec (hoppingRoleTransport n σ v) (x, f) := by
        simp only [Matrix.mulVec, dotProduct, hoppingCarDirac, carDirac]
        exact (Fintype.sum_prod_type fun q : CARHilbertPoint n =>
          (∑ r, spatialDiracComponent n r x q.1 * fockGamma r f q.2) *
            hoppingRoleTransport n σ v q).symm

end

end D0.Geometry
