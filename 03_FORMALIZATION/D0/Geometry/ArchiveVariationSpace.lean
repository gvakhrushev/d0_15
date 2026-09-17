import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveVariation
import D0.Geometry.ArchiveFieldEquation

open scoped BigOperators

namespace D0

def RowSumZero {I : Type} [Fintype I] (M : Matrix I I ℝ) : Prop :=
  ∀ i, ∑ j, M i j = 0

def PhaseLocalSupport {n : Nat} (_M : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) : Prop :=
  True

structure AdmissibleLaplacianVariation (n : Nat) where
  dL : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ
  symmetric : MatrixSymmetric dL
  row_sum_zero : RowSumZero dL
  phase_local : PhaseLocalSupport dL

noncomputable def symPart {I : Type} (M : Matrix I I ℝ) : Matrix I I ℝ :=
  fun i j => (M i j + M j i) / 2

def SkewSymmetric {I : Type} (M : Matrix I I ℝ) : Prop :=
  ∀ i j, M i j = - M j i

def variationPairing {n : Nat}
    (A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
    (δ : AdmissibleLaplacianVariation n) : ℝ :=
  matrixInnerProduct A δ.dL

end D0
