import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Algebra.FiniteMatrixTensorProduct
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Geometry.ArchivePhaseEdgeMetricScale
import D0.Geometry.ArchiveRoleProductLaplacian
import D0.Geometry.ArchiveCARFockCarrier
import D0.Geometry.ArchiveCARRelations

namespace D0.Geometry

open D0
open D0.Geometry.ArchiveRolePhaseProductCarrier
open D0.Geometry.ArchiveRoleProductLaplacian
open D0.Geometry.ArchivePhaseEdgeMetricScale
open BigOperators Matrix

noncomputable section

/-!
# D0.Geometry.ArchiveCARDirac

Public name: **hopping CAR**.

`carDirac` / `hoppingCarDirac` is the self-adjoint nearest-neighbour Clifford
hopping operator.  It is not the massless Hodge/difference operator.  The
forward/backward operator `hodgeCarDirac`, its adjoint, parity and square live
in `D0.Geometry.ArchiveHodgeCARDirac`.

The declarations `archive_car_dirac_square_owner`, `archive_car_zero_mode_owner`,
`archive_car_spectrum_amplification_owner` and
`archive_dirac_heattrace_multiplicity_owner` are arithmetic scaffolds.  The
finite `L = 2` controls below state the literal operator square and exclude a
zero mode only at that period; they do not identify the declared kernel
dimension, prove a uniform-in-period result, or establish a spinor
decomposition or heat trace.
-/

/-- Derivative lattice scale factor: exactly L = n + 2 = d_edge⁻¹. -/
def diracDerivativeScale (n : ℕ) : ℝ :=
  (archiveFibers n : ℝ)

theorem dirac_derivative_scale_eq_fibers (n : ℕ) :
    diracDerivativeScale n = (archiveFibers n : ℝ) := rfl

/-- Total Hilbert space dimension: 16 * L^4. -/
def carHilbertSpaceDim (n : ℕ) : ℕ :=
  16 * archiveModes n

theorem car_hilbert_space_dim_eq (n : ℕ) :
    carHilbertSpaceDim n = 16 * (n + 2) ^ 4 := rfl

/-! ## Explicit typed CAR Dirac carrier and operator -/

/-- Basis points for the finite CAR Hilbert carrier. -/
abbrev CARHilbertPoint (n : ℕ) : Type :=
  ArchiveRolePhasePoint n × ArchiveFockState

/-- Matrix algebra on the finite CAR Hilbert carrier. -/
abbrev CARHilbertMatrix (n : ℕ) : Type :=
  Matrix (CARHilbertPoint n) (CARHilbertPoint n) ℝ

/-- The self-adjoint Majorana generator attached to a CAR mode. -/
def fockGamma (r : Role) : Matrix ArchiveFockState ArchiveFockState ℝ :=
  fun bra ket => carAnnihilate r bra ket + carCreate r bra ket

theorem fockGamma_symmetric (r : Role) :
    (fockGamma r).transpose = fockGamma r := by
  ext bra ket
  simp only [transpose_apply, fockGamma, carCreate]
  ring

/-- The explicitly supported one-coordinate finite hopping component.

It is supported only when all other role coordinates agree and the selected
coordinate is a cyclic nearest neighbour.  This is a finite support operator,
not a continuum derivative claim. -/
def spatialDiracComponent (n : ℕ) (r : Role) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y =>
    if (∀ s : Role, s ≠ r → x s = y s) ∧
       (((y r).val = ((x r).val + 1) % (archiveFibers n)) ∨
        ((x r).val = ((y r).val + 1) % (archiveFibers n))) then
      (diracDerivativeScale n) / 2
    else 0

theorem spatialDiracComponent_symmetric (n : ℕ) (r : Role) :
    (spatialDiracComponent n r).transpose = spatialDiracComponent n r := by
  ext x y
  simp only [transpose_apply, spatialDiracComponent]
  have h_cond : ((∀ s : Role, s ≠ r → y s = x s) ∧
                 (((x r).val = ((y r).val + 1) % (archiveFibers n)) ∨
                  ((y r).val = ((x r).val + 1) % (archiveFibers n)))) ↔
                ((∀ s : Role, s ≠ r → x s = y s) ∧
                 (((y r).val = ((x r).val + 1) % (archiveFibers n)) ∨
                  ((x r).val = ((y r).val + 1) % (archiveFibers n)))) := by
    constructor
    · rintro ⟨h1, h2⟩
      exact ⟨fun s hs => (h1 s hs).symm, h2.symm⟩
    · rintro ⟨h1, h2⟩
      exact ⟨fun s hs => (h1 s hs).symm, h2.symm⟩
  rw [if_congr h_cond rfl rfl]

/-- Hopping CAR operator: nearest-neighbour Clifford adjacency, not a difference Dirac operator. -/
def carDirac (n : ℕ) : CARHilbertMatrix n :=
  fun ⟨x, f⟩ ⟨y, g⟩ =>
    ∑ r : Role, spatialDiracComponent n r x y * fockGamma r f g

/-- Public alias.  `carDirac` remains the compatibility name of this hopping operator. -/
abbrev hoppingCarDirac (n : ℕ) : CARHilbertMatrix n := carDirac n

theorem hoppingCarDirac_eq_carDirac (n : ℕ) : hoppingCarDirac n = carDirac n := rfl

theorem carDirac_self_adjoint (n : ℕ) :
    (carDirac n).transpose = carDirac n := by
  ext ⟨x, f⟩ ⟨y, g⟩
  simp only [transpose_apply, carDirac]
  apply Finset.sum_congr rfl
  intro r _
  have hs : spatialDiracComponent n r y x = spatialDiracComponent n r x y := by
    have h := congr_fun (congr_fun (spatialDiracComponent_symmetric n r) x) y
    exact h
  have hg : fockGamma r g f = fockGamma r f g := by
    have h := congr_fun (congr_fun (fockGamma_symmetric r) f) g
    exact h
  rw [hs, hg]

/-- Compatibility name for the shared finite matrix tensor product. -/
abbrev tensorProduct {X Y : Type*} [Fintype X] [Fintype Y]
    (A : Matrix X X ℝ) (B : Matrix Y Y ℝ) :
    Matrix (X × Y) (X × Y) ℝ :=
  D0.Algebra.finiteMatrixTensorProduct A B

theorem tensorProduct_mul {X Y : Type*} [Fintype X] [Fintype Y]
    (A C : Matrix X X ℝ) (B D : Matrix Y Y ℝ) :
    tensorProduct A B * tensorProduct C D = tensorProduct (A * C) (B * D) := by
  exact D0.Algebra.finiteMatrixTensorProduct_mul A C B D

theorem tensorProduct_transpose {X Y : Type*} [Fintype X] [Fintype Y]
    (A : Matrix X X ℝ) (B : Matrix Y Y ℝ) :
    (tensorProduct A B).transpose = tensorProduct A.transpose B.transpose := by
  exact D0.Algebra.finiteMatrixTensorProduct_transpose A B

/-- Identity matrix on the Fock factor. -/
def fockIdMatrix : Matrix ArchiveFockState ArchiveFockState ℝ :=
  fun bra ket => if bra = ket then 1 else 0

/-- Fermionic occupation number of a typed Fock state. -/
def fockOccupationCount (s : ArchiveFockState) : ℕ :=
  (if s D0.A then 1 else 0) +
  (if s D0.B then 1 else 0) +
  (if s D0.C then 1 else 0) +
  (if s D0.D then 1 else 0)

/-- The typed Fock grading sign `(-1)^(N_F)`. -/
def fockParitySign (s : ArchiveFockState) : ℝ :=
  if fockOccupationCount s % 2 = 0 then 1 else -1

/-- The fermionic parity operator on the actual 16-state Fock carrier. -/
def fockParityMatrix : Matrix ArchiveFockState ArchiveFockState ℝ :=
  fun bra ket => if bra = ket then fockParitySign bra else 0

theorem fockParityMatrix_symmetric :
    fockParityMatrix.transpose = fockParityMatrix := by
  have hdiag : fockParityMatrix = Matrix.diagonal fockParitySign := rfl
  rw [hdiag, Matrix.diagonal_transpose]

theorem fockParityMatrix_sq :
    fockParityMatrix * fockParityMatrix = fockIdMatrix := by
  ext bra ket
  simp only [Matrix.mul_apply, fockParityMatrix, fockIdMatrix]
  have h_single :
      (∑ mid : ArchiveFockState,
        (if bra = mid then fockParitySign bra else 0) *
          (if mid = ket then fockParitySign mid else 0)) =
      (if bra = ket then (fockParitySign bra) ^ 2 else 0) := by
    rw [Finset.sum_eq_single bra]
    · simp only [if_true]
      by_cases h : bra = ket
      · subst h
        simp [sq]
      · simp [h]
    · intro mid _ hmid
      have hzero :
          (if bra = mid then fockParitySign bra else (0 : ℝ)) = 0 :=
        if_neg (Ne.symm hmid)
      simp [hzero]
    · intro h
      exact (h (Finset.mem_univ bra)).elim
  rw [h_single]
  by_cases h : bra = ket
  · subst h
    simp only [if_true]
    unfold fockParitySign
    split_ifs <;> ring
  · simp [h]

/-- Identity on the spatial factor. -/
def spatialIdMatrix (n : ℕ) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y => if x = y then 1 else 0

theorem spatialIdMatrix_symmetric (n : ℕ) :
    (spatialIdMatrix n).transpose = spatialIdMatrix n := by
  have hdiag : spatialIdMatrix n =
      Matrix.diagonal (fun _ : ArchiveRolePhasePoint n => (1 : ℝ)) := rfl
  rw [hdiag, Matrix.diagonal_transpose]

theorem spatialIdMatrix_mul {n : ℕ}
    (A : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ) :
    spatialIdMatrix n * A = A := by
  ext x y
  simp only [Matrix.mul_apply, spatialIdMatrix]
  rw [Finset.sum_eq_single x]
  · simp
  · intro a _ ha
    have hzero : (if x = a then (1 : ℝ) else 0) = 0 := if_neg (Ne.symm ha)
    simp [hzero]
  · intro h
    exact (h (Finset.mem_univ x)).elim

theorem mul_spatialIdMatrix {n : ℕ}
    (A : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ) :
    A * spatialIdMatrix n = A := by
  ext x y
  simp only [Matrix.mul_apply, spatialIdMatrix]
  rw [Finset.sum_eq_single y]
  · simp
  · intro a _ ha
    have hzero : (if a = y then (1 : ℝ) else 0) = 0 := if_neg ha
    simp [hzero]
  · intro h
    exact (h (Finset.mem_univ y)).elim

/-- Fock parity lifted to the same typed CAR Hilbert carrier. -/
def totalParityOperator (n : ℕ) : CARHilbertMatrix n :=
  tensorProduct (spatialIdMatrix n) fockParityMatrix

theorem totalParityOperator_symmetric (n : ℕ) :
    (totalParityOperator n).transpose = totalParityOperator n := by
  change (tensorProduct (spatialIdMatrix n) fockParityMatrix).transpose =
    tensorProduct (spatialIdMatrix n) fockParityMatrix
  rw [tensorProduct_transpose, spatialIdMatrix_symmetric,
    fockParityMatrix_symmetric]

lemma role_cases (r : Role) :
    r = D0.A ∨ r = D0.B ∨ r = D0.C ∨ r = D0.D := by
  rcases r with ⟨⟨x, hx⟩, ⟨y, hy⟩⟩
  interval_cases x <;> interval_cases y
  · left; rfl
  · right; right; left; rfl
  · right; right; right; rfl
  · right; left; rfl

lemma fockOccupationCount_annihilate_step
    (r : Role) (bra ket : ArchiveFockState)
    (h_ket : ket r = true) (h_bra : bra r = false)
    (h_agree : ∀ s : Role, s ≠ r → bra s = ket s) :
    fockOccupationCount ket = fockOccupationCount bra + 1 := by
  unfold fockOccupationCount
  rcases role_cases r with hr | hr | hr | hr
  · subst hr
    have hB : bra D0.B = ket D0.B := h_agree D0.B (by decide)
    have hC : bra D0.C = ket D0.C := h_agree D0.C (by decide)
    have hD : bra D0.D = ket D0.D := h_agree D0.D (by decide)
    rw [h_ket, h_bra, hB, hC, hD]
    cases (ket D0.B) <;> cases (ket D0.C) <;> cases (ket D0.D) <;> rfl
  · subst hr
    have hA : bra D0.A = ket D0.A := h_agree D0.A (by decide)
    have hC : bra D0.C = ket D0.C := h_agree D0.C (by decide)
    have hD : bra D0.D = ket D0.D := h_agree D0.D (by decide)
    rw [h_ket, h_bra, hA, hC, hD]
    cases (ket D0.A) <;> cases (ket D0.C) <;> cases (ket D0.D) <;> rfl
  · subst hr
    have hA : bra D0.A = ket D0.A := h_agree D0.A (by decide)
    have hB : bra D0.B = ket D0.B := h_agree D0.B (by decide)
    have hD : bra D0.D = ket D0.D := h_agree D0.D (by decide)
    rw [h_ket, h_bra, hA, hB, hD]
    cases (ket D0.A) <;> cases (ket D0.B) <;> cases (ket D0.D) <;> rfl
  · subst hr
    have hA : bra D0.A = ket D0.A := h_agree D0.A (by decide)
    have hB : bra D0.B = ket D0.B := h_agree D0.B (by decide)
    have hC : bra D0.C = ket D0.C := h_agree D0.C (by decide)
    rw [h_ket, h_bra, hA, hB, hC]
    cases (ket D0.A) <;> cases (ket D0.B) <;> cases (ket D0.C) <;> rfl

lemma fockParitySign_add_step (n : ℕ) :
    (if (n + 1) % 2 = 0 then (1 : ℝ) else -1) +
      (if n % 2 = 0 then (1 : ℝ) else -1) = 0 := by
  have h2 : n % 2 = 0 ∨ n % 2 = 1 := by omega
  rcases h2 with h0 | h1
  · have h_mod : (n + 1) % 2 = 1 := by omega
    rw [h0, h_mod]
    simp
  · have h_mod : (n + 1) % 2 = 0 := by omega
    rw [h1, h_mod]
    simp

lemma fockParitySign_sum_annihilate
    (r : Role) (bra ket : ArchiveFockState)
    (h_ket : ket r = true) (h_bra : bra r = false)
    (h_agree : ∀ s : Role, s ≠ r → bra s = ket s) :
    fockParitySign bra + fockParitySign ket = 0 := by
  have h_step := fockOccupationCount_annihilate_step r bra ket h_ket h_bra h_agree
  unfold fockParitySign
  rw [h_step]
  have hsign := fockParitySign_add_step (fockOccupationCount bra)
  linarith

theorem fock_parity_anticommutes_with_gamma (r : Role) :
    fockParityMatrix * fockGamma r + fockGamma r * fockParityMatrix = 0 := by
  ext bra ket
  simp only [Matrix.add_apply, Matrix.mul_apply, Matrix.zero_apply, fockParityMatrix]
  have h_mul1 :
      (∑ mid : ArchiveFockState,
        (if bra = mid then fockParitySign bra else 0) * fockGamma r mid ket) =
      fockParitySign bra * fockGamma r bra ket := by
    rw [Finset.sum_eq_single bra]
    · simp
    · intro mid _ hmid
      have hzero :
          (if bra = mid then fockParitySign bra else (0 : ℝ)) = 0 :=
        if_neg (Ne.symm hmid)
      simp [hzero]
    · intro h
      exact (h (Finset.mem_univ bra)).elim
  have h_mul2 :
      (∑ mid : ArchiveFockState,
        fockGamma r bra mid *
          (if mid = ket then fockParitySign mid else 0)) =
      fockGamma r bra ket * fockParitySign ket := by
    rw [Finset.sum_eq_single ket]
    · simp
    · intro mid _ hmid
      have hzero :
          (if mid = ket then fockParitySign mid else (0 : ℝ)) = 0 :=
        if_neg hmid
      simp [hzero]
    · intro h
      exact (h (Finset.mem_univ ket)).elim
  rw [h_mul1, h_mul2]
  have h_factor :
      fockParitySign bra * fockGamma r bra ket +
        fockGamma r bra ket * fockParitySign ket =
      (fockParitySign bra + fockParitySign ket) * fockGamma r bra ket := by
    ring
  rw [h_factor]
  unfold fockGamma
  by_cases h_ann : carAnnihilate r bra ket = 0
  · by_cases h_cre : carCreate r bra ket = 0
    · have h_ann_cast : (carAnnihilateInt r bra ket : ℝ) = 0 := by
        simpa only [carAnnihilate_eq_intCast] using h_ann
      have h_cre_cast : (carCreateInt r bra ket : ℝ) = 0 := by
        simpa only [carCreate_eq_intCast] using h_cre
      have h_ann_int : carAnnihilateInt r bra ket = 0 := by
        exact_mod_cast h_ann_cast
      have h_cre_int : carCreateInt r bra ket = 0 := by
        exact_mod_cast h_cre_cast
      simp [h_ann, h_cre, h_ann_int, h_cre_int]
    · unfold carCreate at h_cre
      unfold carAnnihilate at h_cre
      split_ifs at h_cre with h_cond
      · rcases h_cond with ⟨h_bra, h_ket, h_agree⟩
        have h_sum := fockParitySign_sum_annihilate r ket bra h_bra h_ket h_agree
        have h_comm : fockParitySign bra + fockParitySign ket = 0 := by
          linarith [h_sum]
        rw [h_comm, zero_mul]
      · contradiction
  · unfold carAnnihilate at h_ann
    split_ifs at h_ann with h_cond
    · rcases h_cond with ⟨h_ket, h_bra, h_agree⟩
      have h_sum := fockParitySign_sum_annihilate r bra ket h_ket h_bra h_agree
      rw [h_sum, zero_mul]
    · contradiction

theorem carDirac_eq_sum_tensorProduct (n : ℕ) :
    carDirac n = ∑ r : Role,
      tensorProduct (spatialDiracComponent n r) (fockGamma r) := by
  rfl

theorem carDirac_parity_anticommutation (n : ℕ) :
    totalParityOperator n * carDirac n + carDirac n * totalParityOperator n = 0 := by
  rw [carDirac_eq_sum_tensorProduct]
  simp only [Finset.mul_sum, Finset.sum_mul]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro r _
  unfold totalParityOperator
  rw [tensorProduct_mul, tensorProduct_mul]
  rw [spatialIdMatrix_mul (spatialDiracComponent n r)]
  rw [mul_spatialIdMatrix (spatialDiracComponent n r)]
  ext ⟨x, f⟩ ⟨y, g⟩
  simp only [Matrix.add_apply, Matrix.zero_apply, tensorProduct,
    D0.Algebra.finiteMatrixTensorProduct, Matrix.kronecker,
    Matrix.kroneckerMap_apply]
  have h_anti := fock_parity_anticommutes_with_gamma r
  have h_entry :
      (fockParityMatrix * fockGamma r + fockGamma r * fockParityMatrix) f g = 0 := by
    rw [h_anti]
    rfl
  simp only [Matrix.add_apply] at h_entry
  rw [← mul_add, h_entry, mul_zero]

/-- Finite spectral pairing: an eigenvector is carried to an eigenvector at
the opposite eigenvalue by the typed parity operator. -/
theorem spectral_symmetry_pairing (n : ℕ)
    (v : CARHilbertPoint n → ℝ) (lambdaVal : ℝ)
    (h_eig : (carDirac n) *ᵥ v = lambdaVal • v) :
    (carDirac n) *ᵥ ((totalParityOperator n) *ᵥ v) =
      (-lambdaVal) • ((totalParityOperator n) *ᵥ v) := by
  have h_anti := carDirac_parity_anticommutation n
  have h_mul :
      ((totalParityOperator n * carDirac n +
        carDirac n * totalParityOperator n) *ᵥ v) = 0 := by
    rw [h_anti]
    simp
  rw [Matrix.add_mulVec] at h_mul
  rw [← Matrix.mulVec_mulVec] at h_mul
  rw [h_eig] at h_mul
  rw [← Matrix.mulVec_mulVec] at h_mul
  have h_comm_smul :
      (totalParityOperator n) *ᵥ (lambdaVal • v) =
        lambdaVal • ((totalParityOperator n) *ᵥ v) := by
    ext i
    simp only [Matrix.mulVec, dotProduct, Pi.smul_apply, smul_eq_mul]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [h_comm_smul] at h_mul
  ext i
  have hi := congr_fun h_mul i
  simp only [Pi.add_apply, Pi.zero_apply, Pi.smul_apply, smul_eq_mul] at hi ⊢
  linarith

/-- **D0-ARCHIVE-CAR-DIRAC-OWNER-001 (Owner)**:
Construction of the self-adjoint CAR Dirac operator:
1. It is an explicit matrix on the typed finite carrier;
2. Its spatial entries have the stated nearest-neighbour support;
3. It is built from the existing CAR creation/annihilation operators;
4. It is self-adjoint on that carrier. -/
theorem archive_car_dirac_owner (n : ℕ) :
    ((carDirac n).transpose = carDirac n) ∧
    (Fintype.card Role = 4) ∧
    (Fintype.card ArchiveFockState = 16) ∧
    (diracDerivativeScale n = (archiveFibers n : ℝ)) :=
  ⟨carDirac_self_adjoint n, card_role, card_archive_fock_state, rfl⟩

/-- Arithmetic Fock-dimension scaffold.  This is not an operator square. -/
def carDiracSquareScalarSectorFactor : ℕ := 16

theorem carDiracSquareScalarSectorFactor_eq_fock_dim :
    carDiracSquareScalarSectorFactor = Fintype.card ArchiveFockState := by
  rw [card_archive_fock_state]
  rfl

theorem archive_car_dirac_square_owner :
    (carDiracSquareScalarSectorFactor = 16) ∧
    (Fintype.card ArchiveFockState = 16) :=
  ⟨rfl, card_archive_fock_state⟩

/-- Spatially constant vacuum vector on the actual site × Fock carrier. -/
def archiveConstantVacuumVector (n : ℕ) : CARHilbertPoint n → ℝ :=
  fun p => if p.2 = fockVacuumState then 1 else 0

/-- Origin site in the four finite cyclic coordinates. -/
def archiveZeroSite (n : ℕ) : ArchiveRolePhasePoint n :=
  fun _ => ⟨0, by unfold archiveFibers; omega⟩

/-- The tensor product of a site operator with Fock identity acts on a
spatially constant vacuum vector by its site action. -/
theorem tensorProduct_fockId_mulVec_constant_vacuum (n : ℕ)
    (M : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ) :
    tensorProduct M fockIdMatrix *ᵥ archiveConstantVacuumVector n =
      fun p => if p.2 = fockVacuumState then
        (M *ᵥ (fun _ => (1 : ℝ))) p.1 else 0 := by
  classical
  funext ⟨x, f⟩
  simp only [Matrix.mulVec, dotProduct, tensorProduct,
    D0.Algebra.finiteMatrixTensorProduct]
  rw [Fintype.sum_prod_type]
  by_cases hf : f = fockVacuumState
  · subst f
    simp [fockIdMatrix, archiveConstantVacuumVector]
  · simp [fockIdMatrix, archiveConstantVacuumVector, hf]

/-- The actual hopping matrix moves the constant vacuum into a nonzero
singleton component already at the smallest archive period `L = 2`. -/
private theorem carAnnihilate_singleton_vacuum_zero (r s : Role) :
    carAnnihilate r (fockSingletonState s) fockVacuumState = 0 := by
  by_contra h
  have h_occ :=
    (carAnnihilate_support r (fockSingletonState s) fockVacuumState h).1
  simp [fockVacuumState] at h_occ

private theorem fockGamma_singleton_vacuum (r s : Role) :
    fockGamma r (fockSingletonState s) fockVacuumState = roleDelta r s := by
  unfold fockGamma
  rw [carAnnihilate_singleton_vacuum_zero, carCreate_singleton_vacuum]
  simp

private theorem carDirac_mulVec_constant_vacuum_singleton (n : ℕ)
    (x : ArchiveRolePhasePoint n) (s : Role) :
    (carDirac n *ᵥ archiveConstantVacuumVector n)
      (x, fockSingletonState s) =
        ∑ y : ArchiveRolePhasePoint n, spatialDiracComponent n s x y := by
  classical
  simp only [Matrix.mulVec, dotProduct, carDirac, archiveConstantVacuumVector]
  rw [Fintype.sum_prod_type]
  simp [fockGamma_singleton_vacuum, roleDelta]

theorem carDirac_constant_vacuum_nonzero_at_singleton_A :
    (carDirac 0 *ᵥ archiveConstantVacuumVector 0)
      (archiveZeroSite 0, fockSingletonState D0.A) ≠ 0 := by
  classical
  rw [carDirac_mulVec_constant_vacuum_singleton]
  let oneIndex : archivePhaseIndex 0 := ⟨1, by unfold archiveFibers; omega⟩
  let y : ArchiveRolePhasePoint 0 := Function.update (archiveZeroSite 0) D0.A oneIndex
  have hterm : spatialDiracComponent 0 D0.A (archiveZeroSite 0) y = 1 := by
    norm_num [spatialDiracComponent, y, oneIndex, archiveZeroSite,
      diracDerivativeScale, archiveFibers, archivePhaseIndex, Function.update]
  have hnonneg : ∀ z ∈ Finset.univ,
      0 ≤ spatialDiracComponent 0 D0.A (archiveZeroSite 0) z := by
    intro z _
    simp only [spatialDiracComponent]
    split_ifs <;> norm_num [diracDerivativeScale, archiveFibers]
  have hbound : 1 ≤
      ∑ z : ArchiveRolePhasePoint 0,
        spatialDiracComponent 0 D0.A (archiveZeroSite 0) z := by
    calc
      1 = spatialDiracComponent 0 D0.A (archiveZeroSite 0) y := hterm.symm
      _ ≤ ∑ z : ArchiveRolePhasePoint 0,
          spatialDiracComponent 0 D0.A (archiveZeroSite 0) z :=
        Finset.single_le_sum hnonneg (Finset.mem_univ y)
  exact ne_of_gt (lt_of_lt_of_le (by norm_num) hbound)

/-- Scoped no-go for the literal `carDirac`: at `L = 2` its square cannot be
the owned metric role-product Laplacian tensored with the Fock identity. The
constant mode is killed by the Laplacian, while self-adjointness and the
explicit vacuum-to-singleton matrix entry rule out a zero square there.
This does not decide a different operator or repair the unresolved source
locator of `D0-ARCHIVE-CAR-DIRAC-SQUARE-001`. -/
theorem carDirac_square_ne_archiveMetricProductLaplacian_at_zero :
    carDirac 0 * carDirac 0 ≠
      tensorProduct (archiveMetricProductLaplacian 0) fockIdMatrix := by
  intro hsq
  let v := archiveConstantVacuumVector 0
  have htarget :
      tensorProduct (archiveMetricProductLaplacian 0) fockIdMatrix *ᵥ v = 0 := by
    rw [tensorProduct_fockId_mulVec_constant_vacuum]
    have hconstant := archiveMetricProductLaplacian_constant_zero 0 1
    rw [hconstant]
    funext p
    simp
  have hD2 : (carDirac 0 * carDirac 0) *ᵥ v = 0 := by
    rw [hsq]
    exact htarget
  have hD2' : carDirac 0 *ᵥ (carDirac 0 *ᵥ v) = 0 := by
    rw [Matrix.mulVec_mulVec]
    exact hD2
  have hnorm : dotProduct (carDirac 0 *ᵥ v) (carDirac 0 *ᵥ v) = 0 := by
    calc
      dotProduct (carDirac 0 *ᵥ v) (carDirac 0 *ᵥ v) =
          dotProduct v ((carDirac 0).transpose *ᵥ (carDirac 0 *ᵥ v)) := by
            exact (Matrix.dotProduct_transpose_mulVec (carDirac 0) v
              (carDirac 0 *ᵥ v)).symm
      _ = dotProduct v (carDirac 0 *ᵥ (carDirac 0 *ᵥ v)) := by
            rw [carDirac_self_adjoint]
      _ = 0 := by rw [hD2']; simp
  have hentry :
      (carDirac 0 *ᵥ v)
        (archiveZeroSite 0, fockSingletonState D0.A) = 0 := by
    have hentry_sq : ∀ i : CARHilbertPoint 0, (carDirac 0 *ᵥ v) i = 0 := by
      intro i
      have hle : (carDirac 0 *ᵥ v) i ^ 2 ≤
          dotProduct (carDirac 0 *ᵥ v) (carDirac 0 *ᵥ v) := by
        unfold dotProduct
        simpa [pow_two, mul_comm] using
          (Finset.single_le_sum
            (fun j _ => sq_nonneg ((carDirac 0 *ᵥ v) j))
            (Finset.mem_univ i))
      rw [hnorm] at hle
      nlinarith
    exact hentry_sq _
  exact carDirac_constant_vacuum_nonzero_at_singleton_A hentry

/-! ## Exact smallest-period CAR control

At `n = 0`, the archive has period `L = 2`.  The spatial role blocks are
coordinate flips, so they square to identity and commute.  The Fock blocks
anticommute by the already-owned finite CAR relations.  The following
factorized calculation proves `D^2 = 4 I` on this one complete finite
carrier; it is not a uniform refinement theorem. -/

/-- Integral `L = 2` shadow of the literal spatial hopping block. -/
private def spatialL2Int (r : Role) :
    Matrix (ArchiveRolePhasePoint 0) (ArchiveRolePhasePoint 0) ℤ :=
  fun x y =>
    if (∀ s : Role, s ≠ r → x s = y s) ∧
        (((y r).val = ((x r).val + 1) % 2) ∨
         ((x r).val = ((y r).val + 1) % 2)) then 1 else 0

/-- The four integral coordinate-flip blocks each square to the spatial
identity.  This finite decision proof covers all sites at `L = 2`. -/
private theorem spatialL2Int_sq_pointwise :
    ∀ r : Role, ∀ x y : ArchiveRolePhasePoint 0,
      (spatialL2Int r * spatialL2Int r) x y =
        if x = y then (1 : ℤ) else 0 := by
  native_decide

/-- Distinct coordinate flips commute on the complete finite `L = 2`
carrier. -/
private theorem spatialL2Int_comm_pointwise :
    ∀ r s : Role, ∀ x y : ArchiveRolePhasePoint 0,
      (spatialL2Int r * spatialL2Int s) x y =
        (spatialL2Int s * spatialL2Int r) x y := by
  native_decide

private theorem spatial_zero_entry_eq_L2Int (r : Role)
    (x y : ArchiveRolePhasePoint 0) :
    spatialDiracComponent 0 r x y = (spatialL2Int r x y : ℝ) := by
  simp [spatialDiracComponent, spatialL2Int, diracDerivativeScale, archiveFibers]

private theorem spatial_zero_square (r : Role) :
    spatialDiracComponent 0 r * spatialDiracComponent 0 r = spatialIdMatrix 0 := by
  ext x y
  simp only [Matrix.mul_apply]
  simp_rw [spatial_zero_entry_eq_L2Int]
  calc
    (∑ z : ArchiveRolePhasePoint 0,
        (spatialL2Int r x z : ℝ) * (spatialL2Int r z y : ℝ)) =
        ((∑ z : ArchiveRolePhasePoint 0,
          spatialL2Int r x z * spatialL2Int r z y : ℤ) : ℝ) := by simp
    _ = ((if x = y then (1 : ℤ) else 0) : ℝ) := by
      have h := spatialL2Int_sq_pointwise r x y
      simpa [Matrix.mul_apply] using congrArg (fun z : ℤ => (z : ℝ)) h
    _ = spatialIdMatrix 0 x y := by simp [spatialIdMatrix]

private theorem spatial_zero_commute (r s : Role) :
    spatialDiracComponent 0 r * spatialDiracComponent 0 s =
      spatialDiracComponent 0 s * spatialDiracComponent 0 r := by
  ext x y
  simp only [Matrix.mul_apply]
  simp_rw [spatial_zero_entry_eq_L2Int]
  calc
    (∑ z : ArchiveRolePhasePoint 0,
        (spatialL2Int r x z : ℝ) * (spatialL2Int s z y : ℝ)) =
        ((∑ z : ArchiveRolePhasePoint 0,
          spatialL2Int r x z * spatialL2Int s z y : ℤ) : ℝ) := by simp
    _ = ((∑ z : ArchiveRolePhasePoint 0,
          spatialL2Int s x z * spatialL2Int r z y : ℤ) : ℝ) := by
      have h := spatialL2Int_comm_pointwise r s x y
      simpa [Matrix.mul_apply] using congrArg (fun z : ℤ => (z : ℝ)) h
    _ = ∑ z : ArchiveRolePhasePoint 0,
          (spatialL2Int s x z : ℝ) * (spatialL2Int r z y : ℝ) := by simp

private theorem fockGamma_anticommutator_entry
    (r s : Role) (bra ket : ArchiveFockState) :
    (fockGamma r * fockGamma s + fockGamma s * fockGamma r) bra ket =
      2 * roleDelta r s * fockIdentity bra ket := by
  change anticommutator (fockGamma r) (fockGamma s) bra ket = _
  have haa := car_annihilate_anticommutator r s bra ket
  have hcc := car_create_anticommutator r s bra ket
  have hac := car_mixed_anticommutator r s bra ket
  have hca := car_mixed_anticommutator_create_first r s bra ket
  unfold anticommutator at haa hcc hac hca
  unfold anticommutator fockGamma
  simp only [add_mul, mul_add, Finset.sum_add_distrib]
  linear_combination haa + hcc + hac + hca

private theorem fockGamma_anticommutator (r s : Role) :
    fockGamma r * fockGamma s + fockGamma s * fockGamma r =
      (2 * roleDelta r s) • fockIdMatrix := by
  ext bra ket
  rw [fockGamma_anticommutator_entry]
  simp [fockIdMatrix, roleDelta, fockIdentity]

/-- Factorized Clifford square: commuting spatial blocks paired with CAR
anticommuting Fock blocks leave only the diagonal role terms. -/
private theorem sum_tensor_square_eq_sum_diagonal
    {X Y : Type*} [Fintype X] [Fintype Y]
    (A : Role → Matrix X X ℝ)
    (G : Role → Matrix Y Y ℝ)
    (J : Matrix Y Y ℝ)
    (hAcomm : ∀ r s, A r * A s = A s * A r)
    (hGanti : ∀ r s, G r * G s + G s * G r =
      (2 * roleDelta r s) • J) :
    (∑ r : Role, ∑ s : Role,
      tensorProduct (A r * A s) (G r * G s)) =
      ∑ r : Role, tensorProduct (A r * A r) J := by
  have hGanti' : ∀ r s,
      G r * G s + G s * G r =
        (if r = s then (2 : ℝ) else 0) • J := by
    intro r s
    simpa [roleDelta] using hGanti r s
  simpa [tensorProduct] using
    (D0.Algebra.finiteMatrixTensorProduct_sum_square_eq_diagonal
      A G J hAcomm hGanti')

private theorem tensorProduct_spatialId_fockId :
    tensorProduct (spatialIdMatrix 0) fockIdMatrix =
      (1 : CARHilbertMatrix 0) := by
  change D0.Algebra.finiteMatrixTensorProduct
    (spatialIdMatrix 0) fockIdMatrix = _
  rw [show spatialIdMatrix 0 = (1 : Matrix (ArchiveRolePhasePoint 0)
      (ArchiveRolePhasePoint 0) ℝ) by
        ext x y
        simp [spatialIdMatrix, Matrix.one_apply],
    show fockIdMatrix = (1 : Matrix ArchiveFockState ArchiveFockState ℝ) by
        ext f g
        simp [fockIdMatrix, Matrix.one_apply]]
  exact D0.Algebra.finiteMatrixTensorProduct_one

/-- Exact square of the literal hopping matrix at the smallest period:
`carDirac 0 ^ 2 = 4 I`. -/
theorem carDirac_square_eq_four_id_at_zero :
    carDirac 0 * carDirac 0 =
      (4 : ℝ) • (1 : CARHilbertMatrix 0) := by
  have hexp : carDirac 0 * carDirac 0 =
      ∑ r : Role, ∑ s : Role,
        tensorProduct
          (spatialDiracComponent 0 s * spatialDiracComponent 0 r)
          (fockGamma s * fockGamma r) := by
    rw [carDirac_eq_sum_tensorProduct]
    simp only [Finset.sum_mul, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro r hr
    apply Finset.sum_congr rfl
    intro s hs
    rw [tensorProduct_mul]
  calc
    carDirac 0 * carDirac 0 =
        ∑ r : Role, ∑ s : Role,
          tensorProduct
            (spatialDiracComponent 0 s * spatialDiracComponent 0 r)
            (fockGamma s * fockGamma r) := hexp
    _ = ∑ r : Role, ∑ s : Role,
          tensorProduct
            (spatialDiracComponent 0 r * spatialDiracComponent 0 s)
            (fockGamma r * fockGamma s) := by
      rw [Finset.sum_comm]
    _ = ∑ r : Role,
          tensorProduct (spatialDiracComponent 0 r * spatialDiracComponent 0 r)
            fockIdMatrix :=
      sum_tensor_square_eq_sum_diagonal
        (A := fun r => spatialDiracComponent 0 r)
        (G := fockGamma) (J := fockIdMatrix)
        spatial_zero_commute fockGamma_anticommutator
    _ = (4 : ℝ) • (1 : CARHilbertMatrix 0) := by
      simp_rw [spatial_zero_square, tensorProduct_spatialId_fockId]
      simp
      ext i j
      simp [Matrix.ofNat_apply, Matrix.one_apply, Matrix.smul_apply]

/-- At the smallest archive period, the literal hopping operator has no
nonzero zero mode. The result is finite-period control only; it does not
identify a continuum kernel or change the open uniform claim. -/
theorem carDirac_zero_kernel_trivial_at_zero
    (v : CARHilbertPoint 0 → ℝ)
    (hv : carDirac 0 *ᵥ v = 0) : v = 0 := by
  have hD2v : (carDirac 0 * carDirac 0) *ᵥ v = 0 := by
    rw [← Matrix.mulVec_mulVec, hv]
    simp
  have hfour : (4 : ℝ) • v = 0 := by
    calc
      (4 : ℝ) • v = ((4 : ℝ) • (1 : CARHilbertMatrix 0)) *ᵥ v := by
        simp [Matrix.smul_mulVec, Matrix.one_mulVec]
      _ = (carDirac 0 * carDirac 0) *ᵥ v := by
        rw [carDirac_square_eq_four_id_at_zero]
      _ = 0 := hD2v
  funext i
  have hi := congrFun hfour i
  simp only [Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at hi
  change v i = 0
  nlinarith

/-- Declared integer 16.  This definition does not identify `ker hoppingCarDirac`. -/
def carDiracKernelDim : ℕ := 16

theorem car_zero_mode_independent_of_L (_n : ℕ) :
    carDiracKernelDim = 16 := rfl

theorem archive_car_zero_mode_owner (n : ℕ) :
    (carDiracKernelDim = 16) ∧
    (carDiracKernelDim < 3 * (n + 2)^4 + 2) := by
  refine ⟨rfl, ?_⟩
  unfold carDiracKernelDim
  have h1 : 2 ≤ n + 2 := by omega
  have h2 : 16 ≤ (n + 2)^4 := by
    have : 2^4 ≤ (n + 2)^4 := Nat.pow_le_pow_left h1 4
    exact this
  linarith

/-- **D0-ARCHIVE-CAR-PARITY-SPECTRUM-001 (Owner)**:
Typed Fock parity is an involutive self-adjoint grading which anticommutes
with each CAR Majorana generator and hence with the supported finite CAR
Dirac operator.  The finite spectral consequence is the explicit
eigenvector pairing theorem `spectral_symmetry_pairing`; no infinite
dimensional spectral theorem is imported. -/
def fockEvenStateCount : ℕ := 8
def fockOddStateCount : ℕ := 8

theorem fock_parity_dimension_split :
    fockEvenStateCount + fockOddStateCount = Fintype.card ArchiveFockState := by
  rw [card_archive_fock_state]
  rfl

theorem archive_car_parity_spectrum_owner (n : ℕ) (r : Role) :
    (fockEvenStateCount = 8) ∧
    (fockOddStateCount = 8) ∧
    (fockEvenStateCount + fockOddStateCount = 16) ∧
    (fockParityMatrix.transpose = fockParityMatrix) ∧
    (fockParityMatrix * fockParityMatrix = fockIdMatrix) ∧
    (fockParityMatrix * fockGamma r + fockGamma r * fockParityMatrix = 0) ∧
    (totalParityOperator n * carDirac n +
      carDirac n * totalParityOperator n = 0) :=
  ⟨rfl, rfl, rfl, fockParityMatrix_symmetric, fockParityMatrix_sq,
   fock_parity_anticommutes_with_gamma r,
   carDirac_parity_anticommutation n⟩

/-- Arithmetic declaration `4`.  No spinor decomposition or continuum limit is proved. -/
def carDiracAmplificationFactor : ℕ := 4

theorem car_amplification_times_spinor_eq_sixteen :
    carDiracAmplificationFactor * 4 = Fintype.card ArchiveFockState := by
  rw [card_archive_fock_state]
  rfl

theorem archive_car_spectrum_amplification_owner :
    (carDiracAmplificationFactor = 4) ∧
    (carDiracAmplificationFactor * 4 = 16) :=
  ⟨rfl, rfl⟩

/-- Arithmetic declaration `16`.  No heat-trace identity is stated. -/
def diracHeatTraceMultiplicity : ℕ := 16

theorem diracHeatTraceMultiplicity_eq_fock_dim :
    diracHeatTraceMultiplicity = Fintype.card ArchiveFockState := by
  rw [card_archive_fock_state]
  rfl

theorem archive_dirac_heattrace_multiplicity_owner :
    (diracHeatTraceMultiplicity = 16) ∧
    (Fintype.card ArchiveFockState = 16) :=
  ⟨rfl, card_archive_fock_state⟩

end
end D0.Geometry
