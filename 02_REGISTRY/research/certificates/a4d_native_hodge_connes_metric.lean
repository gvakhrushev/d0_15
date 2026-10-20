import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchiveHodgeDiracMetricMismatchNoGo
import Mathlib.Tactic

namespace D0.Research.NativeHodgeConnesMetric
open D0 D0.Geometry
open scoped BigOperators
noncomputable section
set_option linter.unusedSimpArgs false

def siteMultiplier (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) : ArchiveCochain N := fun p => f p.1 * ψ p

def actualCommutator (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  hodgeCarDirac N (siteMultiplier N f ψ) -
    siteMultiplier N f (hodgeCarDirac N ψ)

def literalCommutator (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) : ArchiveCochain N := fun p =>
  ∑ r : Role, ∑ ket : ArchiveFockState,
    forwardDifferenceScale N *
      (carCreate r p.2 ket * (f (roleTranslatePlus N r p.1) - f p.1) *
          ψ (roleTranslatePlus N r p.1, ket) +
       carAnnihilate r p.2 ket * (f (roleTranslateMinus N r p.1) - f p.1) *
          ψ (roleTranslateMinus N r p.1, ket))

theorem actual_commutator_eq_literal (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    actualCommutator N f ψ = literalCommutator N f ψ := by
  funext p
  simp only [actualCommutator, siteMultiplier, hodgeCarDirac,
    dForward, hodgeCodifferential, forwardCreateDirection,
    backwardAnnihilateDirection, annihilateAction, backwardSite,
    forwardDifference, backwardDifference, Pi.sub_apply, Pi.add_apply]
  unfold literalCommutator
  simp_rw [← Finset.sum_neg_distrib, mul_add, Finset.mul_sum]
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib,
    ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro r _
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib,
    ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro ket _
  ring

theorem actual_commutator_constant (N : ℕ) (c : ℝ) (ψ : ArchiveCochain N) :
    actualCommutator N (fun _ => c) ψ = 0 := by
  rw [actual_commutator_eq_literal]
  funext p
  simp [literalCommutator]

def columnGammaInt (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  carCreateInt r bra ket + carAnnihilateInt r bra ket

theorem actual_fock_columns_orthogonal_int :
    ∀ r s : Role, ∀ ket : ArchiveFockState,
      (∑ bra : ArchiveFockState,
        columnGammaInt r bra ket * columnGammaInt s bra ket) =
          if r = s then (1 : ℤ) else 0 := by
  decide

def columnGamma (r : Role) (bra ket : ArchiveFockState) : ℝ :=
  carCreate r bra ket + carAnnihilate r bra ket

theorem columnGamma_eq_cast (r : Role) (bra ket : ArchiveFockState) :
    columnGamma r bra ket = (columnGammaInt r bra ket : ℝ) := by
  simp [columnGamma, columnGammaInt]

theorem actual_fock_columns_orthogonal (r s : Role) (ket : ArchiveFockState) :
    (∑ bra : ArchiveFockState, columnGamma r bra ket * columnGamma s bra ket) =
      if r = s then (1 : ℝ) else 0 := by
  have h := congrArg (fun z : ℤ => (z : ℝ))
    (actual_fock_columns_orthogonal_int r s ket)
  simpa [columnGamma_eq_cast] using h

theorem actual_fock_column_parseval (v : Role → ℝ) (ket : ArchiveFockState) :
    (∑ bra : ArchiveFockState, (∑ r : Role, columnGamma r bra ket * v r)^2) =
      ∑ r : Role, (v r)^2 := by
  calc
    _ = ∑ r : Role, ∑ s : Role, ∑ bra : ArchiveFockState,
          (columnGamma r bra ket * v r) * (columnGamma s bra ket * v s) := by
      simp_rw [pow_two, Finset.sum_mul, Finset.mul_sum]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro r _
      rw [Finset.sum_comm]
    _ = ∑ r : Role, ∑ s : Role,
          (v r * v s) * (∑ bra : ArchiveFockState,
            columnGamma r bra ket * columnGamma s bra ket) := by
      apply Finset.sum_congr rfl
      intro r _
      apply Finset.sum_congr rfl
      intro s _
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro bra _
      ring
    _ = ∑ r : Role, (v r)^2 := by
      simp [actual_fock_columns_orthogonal, pow_two]

theorem same_operator_heat_square (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N (hodgeCarDirac N ψ) = cochainDifferenceLaplacian N ψ :=
  hodgeCarDirac_sq N ψ

theorem same_operator_self_adjoint (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (hodgeCarDirac N ψ) φ =
      cochainPairing N ψ (hodgeCarDirac N φ) :=
  hodgeCarDirac_self_adjoint N ψ φ

end
end D0.Research.NativeHodgeConnesMetric

#check D0.Research.NativeHodgeConnesMetric.actual_commutator_eq_literal
#print axioms D0.Research.NativeHodgeConnesMetric.actual_commutator_eq_literal

#check D0.Research.NativeHodgeConnesMetric.actual_commutator_constant
#print axioms D0.Research.NativeHodgeConnesMetric.actual_commutator_constant

#check D0.Research.NativeHodgeConnesMetric.actual_fock_columns_orthogonal_int
#print axioms D0.Research.NativeHodgeConnesMetric.actual_fock_columns_orthogonal_int

#check D0.Research.NativeHodgeConnesMetric.columnGamma_eq_cast
#print axioms D0.Research.NativeHodgeConnesMetric.columnGamma_eq_cast

#check D0.Research.NativeHodgeConnesMetric.actual_fock_columns_orthogonal
#print axioms D0.Research.NativeHodgeConnesMetric.actual_fock_columns_orthogonal

#check D0.Research.NativeHodgeConnesMetric.actual_fock_column_parseval
#print axioms D0.Research.NativeHodgeConnesMetric.actual_fock_column_parseval

#check D0.Research.NativeHodgeConnesMetric.same_operator_heat_square
#print axioms D0.Research.NativeHodgeConnesMetric.same_operator_heat_square

#check D0.Research.NativeHodgeConnesMetric.same_operator_self_adjoint
#print axioms D0.Research.NativeHodgeConnesMetric.same_operator_self_adjoint

#check D0.Geometry.hodgeCarDirac_sq
#print axioms D0.Geometry.hodgeCarDirac_sq

#check D0.Geometry.hodgeCarDirac_self_adjoint
#print axioms D0.Geometry.hodgeCarDirac_self_adjoint

#check D0.Geometry.ArchiveHodgeDiracMetricMismatchNoGo.archive_hodge_dirac_euclidean_metric_mismatch_nogo_owner
#print axioms D0.Geometry.ArchiveHodgeDiracMetricMismatchNoGo.archive_hodge_dirac_euclidean_metric_mismatch_nogo_owner
