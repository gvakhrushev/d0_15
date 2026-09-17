import D0.Geometry.ArchiveHeatTrace
import D0.Geometry.ArchiveDirichletEnergy

open scoped BigOperators

namespace D0

def archiveLaplacian (n : Nat) (a b : ArchivePoints n) : Real :=
  if a = b then archiveEigenvalue n a else 0

def SymmetricKernel {alpha : Type} (K : alpha -> alpha -> Real) : Prop :=
  forall a b, K a b = K b a

noncomputable def quadraticForm
    (n : Nat) (f : ArchivePoints n -> Real) : Real :=
  Finset.sum Finset.univ (fun x => archiveEigenvalue n x * (f x)^2)

def zeroArchivePoint (n : Nat) : ArchivePoints n :=
  ⟨0, by
    simp [archiveTower, archiveModes, archiveFibers]⟩

theorem archive_laplacian_symmetric (n : Nat) :
    SymmetricKernel (archiveLaplacian n) := by
  intro a b
  unfold archiveLaplacian
  by_cases h : a = b
  · subst b
    simp
  · have hba : b ≠ a := Ne.symm h
    simp [h, hba]

theorem archive_laplacian_nonnegative (n : Nat) :
    forall f : ArchivePoints n -> Real, 0 <= quadraticForm n f := by
  intro f
  unfold quadraticForm
  exact Finset.sum_nonneg (fun x _hx =>
    mul_nonneg (archive_eigenvalue_nonnegative n x) (sq_nonneg (f x)))

theorem archive_laplacian_zero_mode_control (n : Nat) :
    exists z : ArchivePoints n,
      archiveEigenvalue n z = 0 /\
      forall x : ArchivePoints n, archiveEigenvalue n x = 0 -> x = z := by
  refine ⟨zeroArchivePoint n, ?_, ?_⟩
  · simp [archiveEigenvalue, zeroArchivePoint]
  · intro x hx
    apply Fin.ext
    unfold archiveEigenvalue at hx
    have hxnat : x.val = 0 := by
      exact_mod_cast hx
    simpa [zeroArchivePoint] using hxnat

def D0ArchiveSelfAdjoint : Prop :=
  forall n, SymmetricKernel (archiveLaplacian n)

def D0ArchiveNonnegative : Prop :=
  forall n, forall f : ArchivePoints n -> Real, 0 <= quadraticForm n f

theorem d0_archive_self_adjoint :
    D0ArchiveSelfAdjoint := by
  intro n
  exact archive_laplacian_symmetric n

theorem d0_archive_nonnegative :
    D0ArchiveNonnegative := by
  intro n f
  exact archive_laplacian_nonnegative n f

def SpectrallyEquivalent {n : Nat} (L1 L2 : ArchivePoints n → ArchivePoints n → Real) : Prop :=
  ∃ (c1 c2 : Real), 0 < c1 ∧ 0 < c2 ∧ ∀ f : ArchivePoints n → Real,
    c1 * graphQuadraticForm (archiveFiberGraph n) L1 f ≤ graphQuadraticForm (archiveFiberGraph n) L2 f ∧
    graphQuadraticForm (archiveFiberGraph n) L2 f ≤ c2 * graphQuadraticForm (archiveFiberGraph n) L1 f

structure ExternalLaplacianCompatibility (n : Nat) where
  compat : SpectrallyEquivalent (archiveDelta n) (graphLaplacian (archiveFiberGraph n))

theorem archiveDelta_spectrally_equivalent_graphLaplacian
    (n : Nat)
    (h : ExternalLaplacianCompatibility n) :
    SpectrallyEquivalent (archiveDelta n) (graphLaplacian (archiveFiberGraph n)) := by
  exact h.compat

end D0
