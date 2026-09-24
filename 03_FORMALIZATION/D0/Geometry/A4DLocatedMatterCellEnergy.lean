import Mathlib.Tactic
import D0.Geometry.A4DDiscreteEnergyKernel
import D0.Geometry.A4DLocatedTopologicalStar
import D0.Geometry.A4DPathCovariantHodge

set_option linter.unusedSimpArgs false

/-!
# Reference strict-cell weights on the uncentered coframe

The two reference laws are

`W_c = I + H + c M_q`,

with `H = flatStaggeredH` the owned flux first jet and

`q_∅ = Σ_{r,a} (e_r^a)²`, `q_S = Σ_{r ∈ S, a} (e_r^a)²` otherwise.

They share the flat value and the complete first jet. They depend on the full
uncentered coframe, preserve degree and parity, and the quadratic correction is
strictly local at the same site and Fock label. `L = 2` Nyquist and an `L = 3`
corner separate them at second order.

`J` is the located placement. It does not select `c` or `B`. This is not a
metric star and not a Lorentz-covariant stress.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-- Cell density on the full uncentered coframe. The empty label sums every
role; every other label sums the roles it occupies. -/
def cellQuadraticDensity (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) : ℝ :=
  if S = fockVacuumState then
    ∑ r : Role, ∑ a : Role, (e x r a) ^ 2
  else
    ∑ r : Role, ∑ a : Role, if S r = true then (e x r a) ^ 2 else 0

def referenceQuadratic (N : ℕ) (e : LocalCoframeField N) (ψ : ArchiveCochain N) :
    ArchiveCochain N :=
  fun p => cellQuadraticDensity N e p.1 p.2 * ψ p

/-- `W_c = I + H(e) + c M_q`. -/
def referenceCellWeight (c : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  ψ + flatStaggeredH N e ψ + c • referenceQuadratic N e ψ

private lemma cochainMultiply_smul (N : ℕ) (c : ℝ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) :
    cochainMultiply N (c • m) ψ = c • cochainMultiply N m ψ := by
  funext p
  simp [cochainMultiply, Pi.smul_apply, smul_eq_mul]
  ring

private lemma cochainLinkSymmetric_smul (N : ℕ) (c : ℝ) (r : Role)
    (e : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    cochainLinkSymmetric N r (c • e) ψ = c • cochainLinkSymmetric N r e ψ := by
  funext p
  simp [cochainLinkSymmetric, Pi.smul_apply, smul_eq_mul]
  ring

private lemma cochainCarEnd_smul (N : ℕ) (c : ℝ) (s r : Role) (ψ : ArchiveCochain N) :
    cochainCarEnd N s r (c • ψ) = c • cochainCarEnd N s r ψ := by
  funext p
  simp only [cochainCarEnd, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro ket _
  ring

private lemma cochainBackwardShift_smul (N : ℕ) (c : ℝ) (r : Role) (ψ : ArchiveCochain N) :
    cochainBackwardShift N r (c • ψ) = c • cochainBackwardShift N r ψ := by
  funext p
  simp [cochainBackwardShift, Pi.smul_apply]

private lemma cochainForwardAverage_smul (N : ℕ) (c : ℝ) (r : Role) (ψ : ArchiveCochain N) :
    cochainForwardAverage N r (c • ψ) = c • cochainForwardAverage N r ψ := by
  funext p
  simp [cochainForwardAverage, Pi.smul_apply, smul_eq_mul]
  ring

private lemma cochainFluxForward_smul (N : ℕ) (c : ℝ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (ψ : ArchiveCochain N) :
    cochainFluxForward N (c • e) s r ψ = c • cochainFluxForward N e s r ψ := by
  simp [cochainFluxForward, cochainMultiply_smul]

private lemma cochainFluxAdjoint_smul (N : ℕ) (c : ℝ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (ψ : ArchiveCochain N) :
    cochainFluxAdjoint N (c • e) s r ψ = c • cochainFluxAdjoint N e s r ψ := by
  simp only [cochainFluxAdjoint, cochainMultiply_smul, cochainBackwardShift_smul,
    cochainForwardAverage_smul, cochainCarEnd_smul]

theorem flatStaggeredH_smul (N : ℕ) (c : ℝ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    flatStaggeredH N (c • e) ψ = c • flatStaggeredH N e ψ := by
  funext p
  have hslice : ∀ s r, (fun x => (c • e) x s r) = c • fun x => e x s r := by
    intro s r
    funext x
    simp [Pi.smul_apply]
  simp only [flatStaggeredH, Pi.sub_apply]
  simp_rw [hslice, cochainLinkSymmetric_smul, cochainFluxForward_smul, cochainFluxAdjoint_smul]
  simp only [Pi.smul_apply, smul_eq_mul]
  have hlink :
      (∑ r, c * cochainLinkSymmetric N r (fun x => e x r r) ψ p) =
        c * ∑ r, cochainLinkSymmetric N r (fun x => e x r r) ψ p := by
    rw [Finset.mul_sum]
  have hflux :
      (∑ s, ∑ r,
          (c * cochainFluxForward N (fun x => e x s r) s r ψ p +
            c * cochainFluxAdjoint N (fun x => e x s r) s r ψ p)) =
        c * ∑ s, ∑ r,
          (cochainFluxForward N (fun x => e x s r) s r ψ p +
            cochainFluxAdjoint N (fun x => e x s r) s r ψ p) := by
    have hterm (s r : Role) :
        c * cochainFluxForward N (fun x => e x s r) s r ψ p +
            c * cochainFluxAdjoint N (fun x => e x s r) s r ψ p =
          c * (cochainFluxForward N (fun x => e x s r) s r ψ p +
            cochainFluxAdjoint N (fun x => e x s r) s r ψ p) := by
      ring
    simp_rw [hterm, ← Finset.mul_sum]
  rw [hlink, hflux, flatStaggeredH]
  ring

theorem cellQuadraticDensity_smul (N : ℕ) (c : ℝ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    cellQuadraticDensity N (c • e) x S = c ^ 2 * cellQuadraticDensity N e x S := by
  classical
  simp only [cellQuadraticDensity, Pi.smul_apply]
  by_cases hS : S = fockVacuumState
  · simp only [hS, if_true, pow_two, Finset.mul_sum]
    refine Finset.sum_congr rfl ?_
    intro r _
    refine Finset.sum_congr rfl ?_
    intro a _
    ring
  · simp only [hS, if_false, pow_two, Finset.mul_sum]
    refine Finset.sum_congr rfl ?_
    intro r _
    refine Finset.sum_congr rfl ?_
    intro a _
    by_cases hr : S r = true
    · simp [hr]
      ring
    · simp [hr]

theorem referenceQuadratic_smul (N : ℕ) (c : ℝ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    referenceQuadratic N (c • e) ψ = c ^ 2 • referenceQuadratic N e ψ := by
  funext p
  simp only [referenceQuadratic, cellQuadraticDensity_smul, Pi.smul_apply, smul_eq_mul]
  ring

theorem referenceCellWeight_flat (c : ℝ) (N : ℕ) (ψ : ArchiveCochain N) :
    referenceCellWeight c N 0 ψ = ψ := by
  funext p
  simp [referenceCellWeight, referenceQuadratic, cellQuadraticDensity, flatStaggeredH_zero,
    Pi.smul_apply]

theorem referenceCellWeight_scaled (c t : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    referenceCellWeight c N (t • e) ψ =
      ψ + t • flatStaggeredH N e ψ + (c * t ^ 2) • referenceQuadratic N e ψ := by
  funext p
  simp only [referenceCellWeight, flatStaggeredH_smul, referenceQuadratic_smul, Pi.add_apply,
    Pi.smul_apply, smul_eq_mul]
  ring

theorem referenceCellWeight_same_flat (N : ℕ) (ψ : ArchiveCochain N) :
    referenceCellWeight 1 N 0 ψ = referenceCellWeight 2 N 0 ψ := by
  rw [referenceCellWeight_flat, referenceCellWeight_flat]

theorem referenceCellWeight_same_firstJet (t : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    referenceCellWeight 1 N (t • e) ψ - referenceCellWeight 2 N (t • e) ψ =
      ((1 - 2) * t ^ 2) • referenceQuadratic N e ψ := by
  funext p
  simp only [referenceCellWeight_scaled, Pi.sub_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem referenceCellWeight_secondOrder_separates (t : ℝ) (N : ℕ)
    (e : LocalCoframeField N) (ψ : ArchiveCochain N) :
    referenceCellWeight 2 N (t • e) ψ - referenceCellWeight 1 N (t • e) ψ =
      (t ^ 2) • referenceQuadratic N e ψ := by
  funext p
  simp only [referenceCellWeight_scaled, Pi.sub_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem referenceQuadratic_sameSite (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) (p : ArchiveCochainBasis N) (hψ : ψ p = 0) :
    referenceQuadratic N e ψ p = 0 := by
  simp [referenceQuadratic, hψ]

theorem referenceCellWeight_preserves_degree (c : ℝ) (N k : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (referenceCellWeight c N e ψ) := by
  intro x S hS
  have h0 := hψ x S hS
  have hH := flatStaggeredH_preserves_degree N k e ψ hψ x S hS
  simp [referenceCellWeight, referenceQuadratic, h0, hH, Pi.smul_apply]

theorem referenceCellWeight_preserves_parity (c : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    referenceCellWeight c N e (parityCochain N ψ) =
      parityCochain N (referenceCellWeight c N e ψ) := by
  funext p
  have hH := congrFun (flatStaggeredH_preserves_parity N e ψ) p
  simp only [referenceCellWeight, referenceQuadratic, parityCochain, Pi.add_apply,
    Pi.smul_apply, smul_eq_mul, hH]
  ring

theorem cellQuadraticDensity_zero (N : ℕ) (x : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) : cellQuadraticDensity N 0 x S = 0 := by
  classical
  simp [cellQuadraticDensity]

/-- Off-diagonal uncentered component `e_A^B`, invisible to a diagonal-only readout. -/
def shearCoframe (N : ℕ) : LocalCoframeField N :=
  fun x r a => if x = 0 ∧ r = A ∧ a = B then 1 else 0

private lemma roleSum_single {β : Type*} [AddCommMonoid β] (r0 : Role) (f : Role → β)
    (hf : ∀ r, r ≠ r0 → f r = 0) : (∑ r : Role, f r) = f r0 := by
  classical
  exact Finset.sum_eq_single r0 (fun r _ hr => hf r hr) (fun h => absurd (Finset.mem_univ _) h)

theorem shearCoframe_vacuumDensity (N : ℕ) :
    cellQuadraticDensity N (shearCoframe N) 0 fockVacuumState = 1 := by
  classical
  simp only [cellQuadraticDensity, shearCoframe, fockVacuumState, if_true]
  let f : Role → ℝ := fun r =>
    ∑ a : Role, (if (0 : ArchiveRolePhaseGroup N) = 0 ∧ r = A ∧ a = B then (1 : ℝ) else 0) ^ 2
  have hinner : ∀ r, r ≠ A → f r = 0 := by
    intro r hr
    have h := roleSum_single (β := ℝ) B
      (fun a => (if (0 : ArchiveRolePhaseGroup N) = 0 ∧ r = A ∧ a = B then (1 : ℝ) else 0) ^ 2)
      (by
        intro a ha
        simp [hr, ha])
    unfold f
    rw [h]
    simp [hr]
  have hA : f A = 1 := by
    have h := roleSum_single (β := ℝ) B
      (fun a => (if (0 : ArchiveRolePhaseGroup N) = 0 ∧ A = A ∧ a = B then (1 : ℝ) else 0) ^ 2)
      (by
        intro a ha
        simp [ha])
    unfold f
    rw [h]
    simp
  have hsum := roleSum_single (β := ℝ) A f hinner
  change (∑ r, f r) = 1
  rw [hsum, hA]

theorem periodTwoNyquist_vacuumDensity (y : ArchiveRolePhaseGroup 0) :
    cellQuadraticDensity 0 periodTwoNyquistCoframe y fockVacuumState = 4 := by
  classical
  simp only [cellQuadraticDensity, if_true]
  have hrow : ∀ r : Role, r ≠ A →
      (∑ a : Role, (periodTwoNyquistCoframe y r a) ^ 2) = 0 := by
    intro r hr
    refine Finset.sum_eq_zero ?_
    intro a _
    simp [periodTwoNyquistCoframe, hr]
  have hcol : ∀ a : Role, a ≠ A → (periodTwoNyquistCoframe y A a) ^ 2 = 0 := by
    intro a ha
    simp [periodTwoNyquistCoframe, ha]
  have hAA : (periodTwoNyquistCoframe y A A) ^ 2 = 4 := by
    by_cases hy : y A = 0
    · simp [periodTwoNyquist_zero y hy]; norm_num
    · simp [periodTwoNyquist_offZero y hy]; norm_num
  calc
      (∑ r : Role, ∑ a : Role, (periodTwoNyquistCoframe y r a) ^ 2) =
          ∑ a : Role, (periodTwoNyquistCoframe y A a) ^ 2 := by
        refine Finset.sum_eq_single A ?_ ?_
        · intro r _ hr
          exact hrow r hr
        · intro h
          exact absurd (Finset.mem_univ _) h
    _ = (periodTwoNyquistCoframe y A A) ^ 2 := by
        refine Finset.sum_eq_single A ?_ ?_
        · intro a _ ha
          exact hcol a ha
        · intro h
          exact absurd (Finset.mem_univ _) h
    _ = 4 := hAA

/-- `L = 3` corner supported on the two diagonal edges `A` and `B` at the origin. -/
def cornerCoframe : LocalCoframeField 1 :=
  fun x r a =>
    if x = 0 ∧ r = A ∧ a = A then 1
    else if x = 0 ∧ r = B ∧ a = B then 1
    else 0

private lemma corner_entry (x : ArchiveRolePhaseGroup 1) (r a : Role) :
    cornerCoframe x r a =
      if x = 0 ∧ r = A ∧ a = A then 1
      else if x = 0 ∧ r = B ∧ a = B then 1 else 0 := rfl

private lemma sum_corner_squares (x : ArchiveRolePhaseGroup 1) :
    (∑ r : Role, ∑ a : Role, (cornerCoframe x r a) ^ 2) =
      (if x = 0 then (2 : ℝ) else 0) := by
  classical
  let f : Role → ℝ := fun r => ∑ a : Role, (cornerCoframe x r a) ^ 2
  have hA : f A = if x = 0 then 1 else 0 := by
    have h := roleSum_single (β := ℝ) A (fun a => (cornerCoframe x A a) ^ 2) (by
      intro a ha
      by_cases hx : x = 0 <;> simp [corner_entry, hx, ha, (by decide : A ≠ B), (by decide : B ≠ A)])
    unfold f
    rw [h]
    by_cases hx : x = 0 <;> simp [corner_entry, hx, (by decide : A ≠ B), (by decide : B ≠ A)]
  have hB : f B = if x = 0 then 1 else 0 := by
    have h := roleSum_single (β := ℝ) B (fun a => (cornerCoframe x B a) ^ 2) (by
      intro a ha
      by_cases hx : x = 0 <;> simp [corner_entry, hx, ha, (by decide : A ≠ B), (by decide : B ≠ A)])
    unfold f
    rw [h]
    by_cases hx : x = 0 <;> simp [corner_entry, hx, (by decide : A ≠ B), (by decide : B ≠ A)]
  have hrest : ∀ r, r ≠ A → r ≠ B → f r = 0 := by
    intro r hrA hrB
    have h := roleSum_single (β := ℝ) A (fun a => (cornerCoframe x r a) ^ 2) (by
      intro a _
      simp [corner_entry, hrA, hrB])
    unfold f
    rw [h]
    simp [corner_entry, hrA, hrB]
  have hsplit := Finset.sum_filter_add_sum_filter_not (s := Finset.univ)
    (p := fun r : Role => r = A ∨ r = B) f
  have hzero : ∑ r ∈ Finset.univ.filter (fun r => ¬ (r = A ∨ r = B)), f r = 0 := by
    apply Finset.sum_eq_zero
    intro r hr
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, not_or] at hr
    exact hrest r hr.1 hr.2
  have hset : Finset.univ.filter (fun r : Role => r = A ∨ r = B) = {A, B} := by
    ext r
    simp
  have hpair : ∑ r ∈ Finset.univ.filter (fun r => r = A ∨ r = B), f r = f A + f B := by
    rw [hset, Finset.sum_pair (by decide : A ≠ B)]
  have hsum : ∑ r, f r = f A + f B := by
    rw [← hsplit, hzero, hpair, add_zero]
  rw [hsum, hA, hB]
  by_cases hx : x = 0 <;> simp [hx] <;> norm_num

private lemma occupied_square (x : ArchiveRolePhaseGroup 1) (s : Role) :
    (∑ r : Role, ∑ a : Role, if (fockSingletonState s) r = true then (cornerCoframe x r a) ^ 2 else 0) =
      ∑ a : Role, (cornerCoframe x s a) ^ 2 := by
  classical
  have hrest : ∀ r, r ≠ s →
      (∑ a : Role, if (fockSingletonState s) r = true then (cornerCoframe x r a) ^ 2 else 0) = 0 := by
    intro r hr
    have h := roleSum_single (β := ℝ) A
      (fun a => if (fockSingletonState s) r = true then (cornerCoframe x r a) ^ 2 else 0)
      (by
        intro a _
        simp [fockSingletonState, hr])
    rw [h]
    simp [fockSingletonState, hr]
  have hself : (∑ a : Role, if (fockSingletonState s) s = true then (cornerCoframe x s a) ^ 2 else 0) =
      ∑ a : Role, (cornerCoframe x s a) ^ 2 := by
    refine Finset.sum_congr rfl ?_
    intro a _
    simp [fockSingletonState]
  simpa [hself] using roleSum_single (β := ℝ) s
    (fun r => ∑ a : Role, if (fockSingletonState s) r = true then (cornerCoframe x r a) ^ 2 else 0)
    hrest

theorem cornerCoframe_split (x : ArchiveRolePhaseGroup 1) :
    cellQuadraticDensity 1 cornerCoframe x fockVacuumState =
      cellQuadraticDensity 1 cornerCoframe x (fockSingletonState A) +
        cellQuadraticDensity 1 cornerCoframe x (fockSingletonState B) := by
  classical
  have hv : fockVacuumState ≠ fockSingletonState A := by
    intro h
    have := congrFun h A
    simp [fockVacuumState, fockSingletonState] at this
  have hb : fockVacuumState ≠ fockSingletonState B := by
    intro h
    have := congrFun h B
    simp [fockVacuumState, fockSingletonState] at this
  simp only [cellQuadraticDensity, hv, hb, if_false, if_true, occupied_square]
  have hA : (∑ a : Role, (cornerCoframe x A a) ^ 2) = if x = 0 then 1 else 0 := by
    have h := roleSum_single (β := ℝ) A (fun a => (cornerCoframe x A a) ^ 2) (by
      intro a ha
      by_cases hx : x = 0 <;> simp [corner_entry, hx, ha, (by decide : A ≠ B), (by decide : B ≠ A)])
    rw [h]
    by_cases hx : x = 0 <;> simp [corner_entry, hx, (by decide : A ≠ B), (by decide : B ≠ A)]
  have hB : (∑ a : Role, (cornerCoframe x B a) ^ 2) = if x = 0 then 1 else 0 := by
    have h := roleSum_single (β := ℝ) B (fun a => (cornerCoframe x B a) ^ 2) (by
      intro a ha
      by_cases hx : x = 0 <;> simp [corner_entry, hx, ha, (by decide : A ≠ B), (by decide : B ≠ A)])
    rw [h]
    by_cases hx : x = 0 <;> simp [corner_entry, hx, (by decide : A ≠ B), (by decide : B ≠ A)]
  rw [sum_corner_squares, hA, hB]
  by_cases hx : x = 0 <;> simp [hx, hv.symm, hb.symm] <;> norm_num

theorem nyquist_weights_separate (y : ArchiveRolePhaseGroup 0) (ψ : ArchiveCochain 0)
    (hψ : ψ (y, fockVacuumState) ≠ 0) :
    referenceCellWeight 1 0 periodTwoNyquistCoframe ψ ≠
      referenceCellWeight 2 0 periodTwoNyquistCoframe ψ := by
  intro h
  have hdiff := congrFun h (y, fockVacuumState)
  simp only [referenceCellWeight, Pi.add_apply, Pi.smul_apply, referenceQuadratic,
    periodTwoNyquist_vacuumDensity, smul_eq_mul] at hdiff
  have hzero : (4 : ℝ) * ψ (y, fockVacuumState) = 0 := by
    linarith
  exact hψ ((mul_eq_zero.mp hzero).resolve_left (by norm_num))

/-- Supplied weight, then the fixed located placement. `J` does not choose `c`. -/
def placedReferenceWeight (c : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (ψ : PrimalCochain N) : DualCochain N :=
  locatedPrimalStar N ⟨referenceCellWeight c N e ψ.coeff⟩

theorem locatedPlacement_independent_of_weight (N : ℕ) (φ : PrimalCochain N) :
    locatedPrimalStar N φ = ⟨locatedPrimalStarCoeff N φ.coeff⟩ := rfl

theorem placedReference_uses_fixed_star (c : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (ψ : PrimalCochain N) :
    placedReferenceWeight c N e ψ =
      locatedPrimalStar N ⟨referenceCellWeight c N e ψ.coeff⟩ := rfl

/-- The same located placement is applied to either reference weight.
It has no coefficient `c`, so it does not select the Hessian. -/
theorem locatedStar_does_not_select_reference_weight (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N)
    (_hsep : referenceCellWeight 1 N e ψ ≠ referenceCellWeight 2 N e ψ) :
    placedReferenceWeight 1 N e ⟨ψ⟩ =
        locatedPrimalStar N ⟨referenceCellWeight 1 N e ψ⟩ ∧
      placedReferenceWeight 2 N e ⟨ψ⟩ =
        locatedPrimalStar N ⟨referenceCellWeight 2 N e ψ⟩ ∧
      ∀ φ : PrimalCochain N, locatedPrimalStar N φ = ⟨locatedPrimalStarCoeff N φ.coeff⟩ := by
  exact ⟨rfl, rfl, locatedPlacement_independent_of_weight N⟩

end

end D0.Geometry
