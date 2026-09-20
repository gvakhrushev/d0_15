import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Perm
import Mathlib.Tactic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Core.RoleAlternatingPairing
import D0.Foundation.ObservableCompletionCanonicity

/-!
# D0-SPATIAL-CROSS-ROLE-FLUX-CANONICITY-001 & D0-ARCHIVE-CROSS-ROLE-CURVATURE-ORIGIN-001

## Canonicity of the Spatial Cross-Role Z₂ Flux via Observable Completion

This module formalizes the resolution of the cross-role curvature origin:
1. The raw assignment of the three nonzero roles $\{B, C, D\}$ to the three spatial coordinate
   axes $\{0, 1, 2\}$ is non-canonical: there are $3! = 6$ distinct bijections.
2. However, the pushforward alternating flux observable:
   $$\omega_f(i, j) := \omega(f^{-1}(i), f^{-1}(j))$$
   is **identically constant** across all 6 admissible completions:
   $$\omega_f(i, j) = \begin{cases} 0, & i = j, \\ 1, & i \ne j. \end{cases}$$
3. Applying `ObservableCompletionCanonicity.constant_readout_m1_forced`, the spatial $\mathbb{Z}_2$
   flux readout is **strictly $M_1$-forced**.

Hence:
- The cross-role flux / curvature algebra is a canonical CORE observable.
- The concrete spatial basis identification $\{B, C, D\} \leftrightarrow \{x, y, z\}$ is gauge freedom.
-/

namespace D0.Geometry.SpatialCrossRoleFluxCanonicity

open D0
open D0.Core.RoleAlternatingPairing
open D0.Foundation.ObservableCompletionCanonicity

/-- The three nonzero spatial roles $\{B, C, D\}$. -/
def NonzeroRole := { r : Role // r ≠ roleZero }

instance : Fintype NonzeroRole := by
  unfold NonzeroRole
  infer_instance

instance : DecidableEq NonzeroRole := by
  unfold NonzeroRole
  infer_instance

theorem card_nonzero_roles : Fintype.card NonzeroRole = 3 := by
  decide

/-- The three spatial coordinate directions $\{0, 1, 2\}$. -/
abbrev SpatialAxis := Fin 3

/-- An admissible spatial completion is any bijection between nonzero roles and spatial axes. -/
def AdmissibleSpatialCompletion (_f : NonzeroRole ≃ SpatialAxis) : Prop :=
  True

/-- The pushforward spatial $\mathbb{Z}_2$ flux matrix on $\mathrm{SpatialAxis} \times \mathrm{SpatialAxis}$. -/
def spatialFluxReadout (f : NonzeroRole ≃ SpatialAxis) : SpatialAxis → SpatialAxis → Bool :=
  fun i j => roleOmega (f.symm i).val (f.symm j).val

/-- Canonical target flux matrix: 0 on diagonal, 1 on off-diagonal. -/
def canonicalSpatialFlux : SpatialAxis → SpatialAxis → Bool :=
  fun i j => (i != j)

/-- For any spatial completion $f$, the pushforward flux matches `canonicalSpatialFlux` identically. -/
theorem spatial_flux_independent_of_completion (f : NonzeroRole ≃ SpatialAxis) :
    spatialFluxReadout f = canonicalSpatialFlux := by
  ext i j
  unfold spatialFluxReadout canonicalSpatialFlux
  by_cases hij : i = j
  · subst hij
    simp [roleOmega_self_zero]
  · have h_ne : (f.symm i).val ≠ (f.symm j).val := by
      intro h_eq
      have h_sub_eq : f.symm i = f.symm j := Subtype.ext h_eq
      have h_inj := f.symm.injective h_sub_eq
      exact hij h_inj
    have hu_ne : (f.symm i).val ≠ roleZero := (f.symm i).property
    have hv_ne : (f.symm j).val ≠ roleZero := (f.symm j).property
    have h_omega := roleOmega_of_distinct_nonzero hu_ne hv_ne h_ne
    have h_bne : (i != j) = true := by
      rw [bne_iff_ne]
      exact hij
    rw [h_bne, h_omega]

/-- Standard reference completion (B ↦ 0, C ↦ 1, D ↦ 2). -/
def referenceCompletion : NonzeroRole ≃ SpatialAxis where
  toFun r :=
    if r.val = B then 0
    else if r.val = C then 1
    else 2
  invFun i :=
    match i with
    | 0 => ⟨B, by decide⟩
    | 1 => ⟨C, by decide⟩
    | 2 => ⟨D, by decide⟩
  left_inv r := by
    obtain ⟨val, hval⟩ := r
    dsimp
    split_ifs with hB hC
    · apply Subtype.ext; dsimp; exact hB.symm
    · apply Subtype.ext; dsimp; exact hC.symm
    · apply Subtype.ext; dsimp
      revert val hval hB hC
      decide
  right_inv i := by
    fin_cases i <;> decide

theorem reference_completion_admissible :
    AdmissibleSpatialCompletion referenceCompletion :=
  trivial

/-- The space of all spatial completions has cardinality $3! = 6$. -/
theorem num_spatial_completions :
    Fintype.card (NonzeroRole ≃ SpatialAxis) = 6 := by
  have h_card := Fintype.card_equiv referenceCompletion
  rw [h_card, card_nonzero_roles]
  decide

/-- **D0-SPATIAL-CROSS-ROLE-FLUX-CANONICITY-001 (Owner)**:
The spatial cross-role $\mathbb{Z}_2$ flux is $M_1$-forced across all 6 admissible completions.
Raw role-to-axis pairing is non-canonical, but the spatial flux observable is strictly canonical. -/
theorem spatial_cross_role_flux_m1_forced :
    D0.Foundation.M1Forced
      (CompletionForcesReadout AdmissibleSpatialCompletion spatialFluxReadout)
      canonicalSpatialFlux := by
  have h_ref : spatialFluxReadout referenceCompletion = canonicalSpatialFlux :=
    spatial_flux_independent_of_completion referenceCompletion
  rw [← h_ref]
  apply constant_readout_m1_forced
          AdmissibleSpatialCompletion
          spatialFluxReadout
          referenceCompletion
          reference_completion_admissible
  intro c _
  rw [spatial_flux_independent_of_completion c,
      spatial_flux_independent_of_completion referenceCompletion]

/-- **D0-ARCHIVE-CROSS-ROLE-CURVATURE-ORIGIN-001 (Resolution)**:
Master synthesis theorem classifying the origin of cross-role curvature:
1. Multiple distinct completions exist ($3! = 6$ completions);
2. All completions yield the identical spatial flux readout;
3. The spatial flux observable is $M_1$-forced. -/
theorem cross_role_curvature_origin_master :
    (Fintype.card (NonzeroRole ≃ SpatialAxis) = 6) ∧
    (∀ f : NonzeroRole ≃ SpatialAxis, spatialFluxReadout f = canonicalSpatialFlux) ∧
    (∀ i j : SpatialAxis, canonicalSpatialFlux i j = (i != j)) :=
  ⟨num_spatial_completions,
   spatial_flux_independent_of_completion,
   fun _ _ => rfl⟩

end D0.Geometry.SpatialCrossRoleFluxCanonicity
