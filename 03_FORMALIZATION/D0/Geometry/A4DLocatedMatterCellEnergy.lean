import Mathlib.Tactic
import D0.Geometry.A4DDiscreteEnergyKernel
import D0.Geometry.A4DLocatedTopologicalStar

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Located strict-cell reference matter laws

These are reference cochains on the complete, uncentered coframe. Their
quadratic term is onsite and does not alter the already-owned first jet. The
two coefficients remain distinct models; this module selects neither one.
-/

/-- Full uncentered strict-cell square: for an empty occupation use every
coframe component; otherwise retain all frame components in occupied roles. -/
def strictCellEnergyDensity (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) : ℝ :=
  ∑ r : Role, ∑ a : Role,
    (if ∀ s : Role, S s = false then (e x r a) ^ 2
     else if S r then (e x r a) ^ 2 else 0)

/-- Taylor-polynomial reference law with independently supplied quadratic
coefficient `c`. -/
def strictCellMatterLaw (N : ℕ) (c t : ℝ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : ArchiveCochain N := fun p =>
  ψ p + t * flatStaggeredH N e ψ p +
    c * t ^ 2 * strictCellEnergyDensity N e p.1 p.2 * ψ p

def strictCellMatterLawOne (N : ℕ) (t : ℝ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  strictCellMatterLaw N 1 t e ψ

def strictCellMatterLawTwo (N : ℕ) (t : ℝ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  strictCellMatterLaw N 2 t e ψ

theorem strictCellEnergyDensity_smul (N : ℕ) (t : ℝ)
    (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    strictCellEnergyDensity N (t • e) x S = t ^ 2 * strictCellEnergyDensity N e x S := by
  unfold strictCellEnergyDensity
  simp only [Pi.smul_apply, smul_eq_mul]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro r hr
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro a ha
  split_ifs <;> ring

theorem strictCellMatterLaw_flat (N : ℕ) (c t : ℝ) (ψ : ArchiveCochain N) :
    strictCellMatterLaw N c t 0 ψ = ψ := by
  funext p
  simp [strictCellMatterLaw, strictCellEnergyDensity, flatStaggeredH_zero]

theorem strictCellMatterLaw_flatValue (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : strictCellMatterLaw N 1 0 e ψ = ψ := by
  funext p
  simp [strictCellMatterLaw]

theorem strictCellMatterLaw_firstJet (N : ℕ) (c t : ℝ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N) (p : ArchiveRolePhaseGroup N × ArchiveFockState) :
    strictCellMatterLaw N c t e ψ p - ψ p =
      t * flatStaggeredH N e ψ p + c * t ^ 2 *
        strictCellEnergyDensity N e p.1 p.2 * ψ p := by
  simp [strictCellMatterLaw]
  ring

/-- The two reference laws have identical constant and first-order pieces;
their complete coefficient difference is the explicit quadratic cell term. -/
theorem strictCellMatterLawTwo_sub_one (N : ℕ) (t : ℝ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N)
    (p : ArchiveRolePhaseGroup N × ArchiveFockState) :
    strictCellMatterLawTwo N t e ψ p - strictCellMatterLawOne N t e ψ p =
      t ^ 2 * strictCellEnergyDensity N e p.1 p.2 * ψ p := by
  simp [strictCellMatterLawTwo, strictCellMatterLawOne, strictCellMatterLaw]
  ring

/-- Any occupied cell with nonzero uncentered energy and amplitude explicitly
separates the `c=1` and `c=2` second-order reference laws at nonzero parameter. -/
theorem strictCellMatterLawTwo_ne_one_of_nonzero_cell
    (N : ℕ) (t : ℝ) (ht : t ≠ 0)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N)
    (p : ArchiveRolePhaseGroup N × ArchiveFockState)
    (hq : strictCellEnergyDensity N e p.1 p.2 ≠ 0) (hψ : ψ p ≠ 0) :
    strictCellMatterLawTwo N t e ψ p ≠ strictCellMatterLawOne N t e ψ p := by
  intro heq
  have hnonzero := strictCellMatterLawTwo_sub_one N t e ψ p
  rw [heq, sub_self] at hnonzero
  have hprod : t ^ 2 * strictCellEnergyDensity N e p.1 p.2 * ψ p ≠ 0 :=
    mul_ne_zero (mul_ne_zero (pow_ne_zero 2 ht) hq) hψ
  exact hprod hnonzero.symm

/-- The nonlinear correction has strict onsite carrier support: it vanishes
at every cell where the input cochain vanishes. -/
theorem strictCellMatterLaw_quadratic_support (N : ℕ) (c t : ℝ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N)
    (p : ArchiveRolePhaseGroup N × ArchiveFockState) (hψ : ψ p = 0) :
    c * t ^ 2 * strictCellEnergyDensity N e p.1 p.2 * ψ p = 0 := by
  rw [hψ]
  ring

/-- A fixed invertible located pairing transports, but cannot identify, two
distinct matter operators. This is the algebraic firewall between `J` and
the nonlinear energy Hessian. -/
theorem locatedPairing_does_not_select_matter_operator
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    (J : V ≃ₗ[ℝ] V) (W₁ W₂ : V →ₗ[ℝ] V) (hW : W₁ ≠ W₂) :
    J.symm.toLinearMap.comp W₁ ≠ J.symm.toLinearMap.comp W₂ := by
  intro h
  apply hW
  ext v
  apply J.symm.injective
  exact LinearMap.congr_fun h v

/-- Uncentered oriented plaquette curl of a coframe component. -/
def uncenteredPlaquetteCurl (N : ℕ) (e : LocalCoframeField N)
    (r s a : Role) (x : ArchiveRolePhaseGroup N) : ℝ :=
  forwardDifference N r (fun y => e y s a) x -
    forwardDifference N s (fun y => e y r a) x

def uncenteredPlaquetteCurlSquare (N : ℕ) (e : LocalCoframeField N)
    (r s a : Role) (x : ArchiveRolePhaseGroup N) : ℝ :=
  (uncenteredPlaquetteCurl N e r s a x) ^ 2

/-- Commuting forward differences make the local curl vanish on every pure
forward-gauge coframe, at every period including Nyquist periods. -/
theorem uncenteredPlaquetteCurl_forwardGauge_zero (N : ℕ)
    (xi : LocalRoleVector N) (r s a : Role) (x : ArchiveRolePhaseGroup N) :
    uncenteredPlaquetteCurl N (forwardGaugeCoframe N xi) r s a x = 0 := by
  unfold uncenteredPlaquetteCurl
  simp only [forwardGaugeCoframe]
  have h := congrFun (forwardDifference_comm N r s (fun y => xi y a)) x
  simpa using congrArg (fun z : ℝ => z -
    forwardDifference N s (fun y => forwardDifference N r (fun z => xi z a) y) x) h

/-- The squared-curl Hessian perturbation is invisible to all pure-gauge
two-jet tests, yet detects any coframe with nonzero plaquette curl. -/
theorem uncenteredPlaquetteCurlSquare_gauge_zero (N : ℕ)
    (xi : LocalRoleVector N) (r s a : Role) (x : ArchiveRolePhaseGroup N) :
    uncenteredPlaquetteCurlSquare N (forwardGaugeCoframe N xi) r s a x = 0 := by
  simp [uncenteredPlaquetteCurlSquare,
    uncenteredPlaquetteCurl_forwardGauge_zero]

theorem uncenteredPlaquetteCurlSquare_detects_transverse
    (N : ℕ) (e : LocalCoframeField N) (r s a : Role)
    (x : ArchiveRolePhaseGroup N)
    (hcurl : uncenteredPlaquetteCurl N e r s a x ≠ 0) :
    uncenteredPlaquetteCurlSquare N e r s a x ≠ 0 := by
  exact pow_ne_zero 2 hcurl

theorem strictCellMatterLaw_preserves_degree (N k : ℕ) (c t : ℝ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (strictCellMatterLaw N c t e ψ) := by
  intro x S hS
  simp only [strictCellMatterLaw]
  rw [hψ x S hS]
  simp only [flatStaggeredH_preserves_degree N k e ψ hψ x S hS]
  ring

theorem strictCellMatterLaw_preserves_parity (N : ℕ) (c t : ℝ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N) :
    parityCochain N (strictCellMatterLaw N c t e ψ) =
      strictCellMatterLaw N c t e (parityCochain N ψ) := by
  funext p
  have hp := flatStaggeredH_preserves_parity N e ψ
  simp only [strictCellMatterLaw, parityCochain]
  rw [hp]
  simp [parityCochain]
  ring

/-- The `L=2` oriented Nyquist control remains visible to the complete raw
coframe first jet used by both reference laws; it is not replaced by a
centered-metric readout. -/
theorem strictCellMatterLaw_periodTwoNyquist_firstJet_nonzero :
    flatStaggeredH 0 periodTwoNyquistCoframe periodTwoOneFormProbe ≠ 0 := by
  intro hz
  have hval := congrFun hz (0, singletonFockState A)
  rw [centeredNyquist_nonzero_H_oneForm.2.2] at hval
  norm_num at hval

/-- The `L=3` forward corner response of the common first jet is the owned
half-weight value. The two cell laws differ only at second order. -/
theorem strictCellMatterLaw_periodThree_corner_firstJet :
    scalarComponent 1
      (flatStaggeredH 1 periodThreeOffsiteCoframe periodThreeOffsiteScalar) 0 =
      (1 / 2 : ℝ) :=
  periodThree_offsite_scalar_response

end

end D0.Geometry
