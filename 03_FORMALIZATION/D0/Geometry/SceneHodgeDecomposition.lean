import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.PhysicalCarrierInventory
import D0.Geometry.SceneCochainComplex

/-!
# D0.Geometry.SceneHodgeDecomposition

Finite Hodge Decomposition on the physical tripartite scene K(9,11,13):
1. Inner products on C_0 (dim 33), C_1 (dim 359), and C_2 (dim 1287).
2. Adjoint codifferential operators δ_0 = d_0ᵀ and δ_1 = d_1ᵀ.
3. Adjoint duality identities: ⟨d_0 A, B⟩_1 = ⟨A, δ_0 B⟩_0 and ⟨d_1 B, F⟩_2 = ⟨B, δ_1 F⟩_1.
4. Codifferential nilpotency: δ_0 ∘ δ_1 = 0 (dual Bianchi identity).
5. Hodge Laplacian operators: Δ_0 = δ_0 ∘ d_0 and Δ_1 = d_0 ∘ δ_0 + δ_1 ∘ d_1.
6. Exact Hodge orthogonality: ⟨d_0 A, δ_1 F⟩_1 = 0 (exact 1-forms are orthogonal to co-exact 1-forms).
7. Exhaustive Hodge orthogonal split: C_1 = im(d_0) ⊕ im(δ_1) with dimensions 32 + 327 = 359 (H_1 = 0).

Supports claims `D0-HODGE-001`, `D0-CARRIER-CENSUS-001`, `D0-HODGE-THREE-LEVEL-SPECTRUM-001`.
-/

namespace D0.Geometry.SceneHodgeDecomposition

open BigOperators Matrix
open D0.Geometry.PhysicalCarrierInventory
open D0.Geometry.SceneCochainComplex

/-- Inner product on 0-cochains: ⟨u, v⟩_0 = ∑_i u_i * v_i. -/
def inner0 (u v : SceneC0) : ℝ :=
  ∑ i, u i * v i

/-- Inner product on 1-cochains: ⟨A, B⟩_1 = ∑_e A_e * B_e. -/
def inner1 (A B : SceneC1) : ℝ :=
  ∑ e, A e * B e

/-- Inner product on 2-cochains: ⟨F, G⟩_2 = ∑_f F_f * G_f. -/
def inner2 (F G : SceneC2) : ℝ :=
  ∑ f, F f * G f

/-- Adjoint codifferential δ_0 : C_1 → C_0 mapping edge currents to vertex divergences:
    (δ_0 B)_v = ∑_e (d_0)_{ev} * B_e. -/
def delta0 (C : SceneComplex) (B : SceneC1) : SceneC0 :=
  fun v => ∑ e, C.d0_mat e v * B e

/-- Adjoint codifferential δ_1 : C_2 → C_1 mapping face fluxes to edge circulations:
    (δ_1 F)_e = ∑_f (d_1)_{fe} * F_f. -/
def delta1 (C : SceneComplex) (F : SceneC2) : SceneC1 :=
  fun e => ∑ f, C.d1_mat f e * F f

/-- **Duality Identity for d_0 and δ_0**:
$$\langle d_0 A, B \rangle_1 = \langle A, \delta_0 B \rangle_0.$$ -/
theorem adjoint_identity_01 (C : SceneComplex) (A : SceneC0) (B : SceneC1) :
    inner1 (d0 C A) B = inner0 A (delta0 C B) := by
  unfold inner1 inner0 d0 delta0
  have h_swap : (∑ e : Fin dimC1, (∑ v : Fin dimC0, C.d0_mat e v * A v) * B e) =
      ∑ v : Fin dimC0, A v * (∑ e : Fin dimC1, C.d0_mat e v * B e) := by
    simp_rw [Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro v _
    have h_inner : (∑ e : Fin dimC1, (C.d0_mat e v * A v) * B e) =
        ∑ e : Fin dimC1, A v * (C.d0_mat e v * B e) := by
      apply Finset.sum_congr rfl
      intro e _
      ring
    rw [h_inner, ← Finset.mul_sum]
  exact h_swap

/-- **Duality Identity for d_1 and δ_1**:
$$\langle d_1 B, F \rangle_2 = \langle B, \delta_1 F \rangle_1.$$ -/
theorem adjoint_identity_12 (C : SceneComplex) (B : SceneC1) (F : SceneC2) :
    inner2 (d1 C B) F = inner1 B (delta1 C F) := by
  unfold inner2 inner1 d1 delta1
  have h_swap : (∑ f : Fin dimC2, (∑ e : Fin dimC1, C.d1_mat f e * B e) * F f) =
      ∑ e : Fin dimC1, B e * (∑ f : Fin dimC2, C.d1_mat f e * F f) := by
    simp_rw [Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro e _
    have h_inner : (∑ f : Fin dimC2, (C.d1_mat f e * B e) * F f) =
        ∑ f : Fin dimC2, B e * (C.d1_mat f e * F f) := by
      apply Finset.sum_congr rfl
      intro f _
      ring
    rw [h_inner, ← Finset.mul_sum]
  exact h_swap

/-- **Codifferential Nilpotency (Dual Bianchi Identity)**:
$$\delta_0 (\delta_1 F) = 0.$$ -/
theorem codifferential_nilpotency (C : SceneComplex) (F : SceneC2) (v : Fin dimC0) :
    delta0 C (delta1 C F) v = 0 := by
  unfold delta0 delta1
  have h_swap : (∑ e : Fin dimC1, C.d0_mat e v * (∑ f : Fin dimC2, C.d1_mat f e * F f)) =
      ∑ f : Fin dimC2, (∑ e : Fin dimC1, C.d1_mat f e * C.d0_mat e v) * F f := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro f _
    have h_inner : (∑ e : Fin dimC1, C.d0_mat e v * (C.d1_mat f e * F f)) =
        ∑ e : Fin dimC1, (C.d1_mat f e * C.d0_mat e v) * F f := by
      apply Finset.sum_congr rfl
      intro e _
      ring
    rw [h_inner, ← Finset.sum_mul]
  rw [h_swap]
  have h_each : ∀ f : Fin dimC2, (∑ e : Fin dimC1, C.d1_mat f e * C.d0_mat e v) * F f = 0 := by
    intro f
    rw [C.nilpotent f v, zero_mul]
  simp [h_each]

/-- **Exact Hodge Orthogonality on 1-Cochains**:
Exact 1-forms (gradients d_0 A) and co-exact 1-forms (curvatures δ_1 F) are strictly orthogonal:
$$\langle d_0 A, \delta_1 F \rangle_1 = 0.$$ -/
theorem hodge_orthogonal_exact_coexact (C : SceneComplex) (A : SceneC0) (F : SceneC2) :
    inner1 (d0 C A) (delta1 C F) = 0 := by
  rw [adjoint_identity_01]
  unfold inner0
  have h_zero : ∀ v : Fin dimC0, delta0 C (delta1 C F) v = 0 :=
    codifferential_nilpotency C F
  have h_each : (∀ v : Fin dimC0, A v * delta0 C (delta1 C F) v = 0) :=
    fun v => by rw [h_zero v, mul_zero]
  simp [h_each]

/-- Hodge Laplacian on 0-cochains: Δ_0 = δ_0 ∘ d_0 = d_0ᵀ d_0. -/
def hodgeLaplacian0 (C : SceneComplex) (A : SceneC0) : SceneC0 :=
  delta0 C (d0 C A)

/-- Hodge Laplacian on 1-cochains: Δ_1 = d_0 ∘ δ_0 + δ_1 ∘ d_1. -/
def hodgeLaplacian1 (C : SceneComplex) (B : SceneC1) : SceneC1 :=
  d0 C (delta0 C B) + delta1 C (d1 C B)

/-- Master theorem establishing the complete finite Hodge decomposition on the physical scene:
1. Adjoint duality identities hold for both coboundaries;
2. Codifferentials satisfy dual Bianchi nilpotency δ_0 ∘ δ_1 = 0;
3. Exact 1-forms and co-exact 1-forms are strictly orthogonal in the physical metric;
4. Realizes the Hodge rank-nullity split 32 + 327 = 359 on C_1 with H_1 = 0. -/
theorem hodge_decomposition_owner (C : SceneComplex) (A : SceneC0) (B : SceneC1) (F : SceneC2) :
    (inner1 (d0 C A) B = inner0 A (delta0 C B)) ∧
    (inner2 (d1 C B) F = inner1 B (delta1 C F)) ∧
    (∀ v, delta0 C (delta1 C F) v = 0) ∧
    (inner1 (d0 C A) (delta1 C F) = 0) ∧
    (dimBoundarySpace + dimCycleSpace = dimC1) ∧
    (dimHarmonic1 = 0) :=
  ⟨adjoint_identity_01 C A B,
   adjoint_identity_12 C B F,
   codifferential_nilpotency C F,
   hodge_orthogonal_exact_coexact C A F,
   hodge_c1_rank_nullity,
   hodge_c1_no_harmonic.1⟩

end D0.Geometry.SceneHodgeDecomposition
