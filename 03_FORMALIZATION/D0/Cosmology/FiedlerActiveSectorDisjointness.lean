import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Claims.Signature31Split
import D0.Claims.InvariantGenerationBridge
import D0.Cosmology.FiedlerProjectorOperator
import D0.Spectral.DarkArchiveStructure

/-!
# D0.Cosmology.FiedlerActiveSectorDisjointness

Theoretical owner: `D0-CMB-FIEDLER-ACTIVE-SECTOR-DISJOINTNESS-001`.

Sector mismatch between the Hodge-Fiedler fluctuation mode and the visible/active scalar sector:
1. The Fiedler spectral projector $\Pi_F$ on $K(9,11,13)$ is supported strictly on the unique
   13-vertex partition $V_{13}$, acting as $I_{13} - \frac{1}{13} J_{13}$ with rank 12.
2. The image of $\Pi_F$ is strictly zero-sum across each of the three zones:
   $$\forall z \in \{0, 1, 2\}, \quad \operatorname{zoneSum}(\Pi_F v, z) = 0.$$
   Therefore, $\operatorname{im}(\Pi_F) \subset H_{\mathrm{archive}}$, where $H_{\mathrm{archive}}$
   is the 30-dimensional dark archive subspace of zone-balanced states.
3. The visible sector is the 3-dimensional subspace of zone-constant states, onto which the
   Reynolds projector $Q$ (`D0.Claims.InvariantGenerationBridge.Q`) projects.
4. Any scalar active curvature projector $P_{\mathrm{active}}$ factoring through the visible sector
   ($Q P_{\mathrm{active}} = P_{\mathrm{active}} Q = P_{\mathrm{active}}$) strictly annihilates $\Pi_F$:
   $$P_{\mathrm{active}} \Pi_F = 0, \quad \Pi_F P_{\mathrm{active}} = 0.$$
5. Exact orthogonality:
   $$H_{\mathrm{archive}} \cap H_{\mathrm{visible}} = \{0\}.$$
   Consequently:
   $$Q \cdot \Pi_F = 0 \quad \text{and} \quad \Pi_F \cdot Q = 0,$$
   $$(1 - Q) \cdot \Pi_F = \Pi_F \quad \text{and} \quad \Pi_F \cdot (1 - Q) = \Pi_F.$$
-/

namespace D0.Cosmology.FiedlerActiveSectorDisjointness

open D0.Claims
open D0.Claims.InvariantGenerationBridge
open D0.Cosmology.FiedlerProjectorOperator
open D0.Spectral.DarkArchiveStructure

/-- The Reynolds projector $Q$ on `Fin 33` strictly annihilates $\Pi_F$ on the left:
$Q \cdot \Pi_F = 0$. -/
theorem Q_mul_PiF_eq_zero : Q * PiF = 0 := by
  native_decide

/-- The Reynolds projector $Q$ on `Fin 33` strictly annihilates $\Pi_F$ on the right:
$\Pi_F \cdot Q = 0$. -/
theorem PiF_mul_Q_eq_zero : PiF * Q = 0 := by
  native_decide

/-- Mutual annihilation of the Reynolds projector and the Fiedler projector:
$Q \cdot \Pi_F = 0$ and $\Pi_F \cdot Q = 0$. -/
theorem reynolds_Q_PiF_disjoint :
    Q * PiF = 0 ∧ PiF * Q = 0 :=
  ⟨Q_mul_PiF_eq_zero, PiF_mul_Q_eq_zero⟩

/-- The Fiedler projector lies entirely within the complementary 30-dimensional archive projector
$P_{\mathrm{archive}} = 1 - Q$:
$(1 - Q) \cdot \Pi_F = \Pi_F$ and $\Pi_F \cdot (1 - Q) = \Pi_F$. -/
theorem archive_P_mul_PiF :
    (1 - Q) * PiF = PiF ∧ PiF * (1 - Q) = PiF := by
  have h_left : (1 - Q) * PiF = PiF := by
    rw [Matrix.sub_mul, Matrix.one_mul, Q_mul_PiF_eq_zero, sub_zero]
  have h_right : PiF * (1 - Q) = PiF := by
    rw [Matrix.mul_sub, Matrix.mul_one, PiF_mul_Q_eq_zero, sub_zero]
  exact ⟨h_left, h_right⟩

/-- Any visible-subspace projector (such as the 2D active scalar curvature projector) that
factors through $Q$ strictly annihilates the Fiedler projector. -/
theorem visible_subprojector_annihilates_PiF
    (P_active : Matrix (Fin 33) (Fin 33) ℚ)
    (h_left_factor : P_active = P_active * Q)
    (h_right_factor : P_active = Q * P_active) :
    P_active * PiF = 0 ∧ PiF * P_active = 0 := by
  have h1 : P_active * PiF = 0 := by
    calc P_active * PiF = (P_active * Q) * PiF := by rw [← h_left_factor]
    _ = P_active * (Q * PiF) := by rw [Matrix.mul_assoc]
    _ = P_active * 0 := by rw [Q_mul_PiF_eq_zero]
    _ = 0 := Matrix.mul_zero P_active
  have h2 : PiF * P_active = 0 := by
    calc PiF * P_active = PiF * (Q * P_active) := by rw [← h_right_factor]
    _ = (PiF * Q) * P_active := by rw [Matrix.mul_assoc]
    _ = 0 * P_active := by rw [PiF_mul_Q_eq_zero]
    _ = 0 := Matrix.zero_mul P_active
  exact ⟨h1, h2⟩

/-- Matrix-vector multiplication for rational matrices on `Fin 33`. -/
def mulv (M : Matrix (Fin 33) (Fin 33) ℚ) (v : Fin 33 → ℚ) : Fin 33 → ℚ :=
  fun u => ∑ w, M u w * v w

/-- For any state $v$, each column of $\Pi_F$ has zero sum on every zone:
its image is strictly supported inside $H_{\mathrm{archive}}$. -/
theorem PiF_col_sum_zone (z : Fin 3) (j : Fin 33) :
    (∑ k : Fin 33, if zone31 k = z then PiF k j else 0) = 0 := by
  revert z j
  native_decide

/-- For any state $v$, its Fiedler projection $\Pi_F v$ has zero sum on every zone:
$\operatorname{zoneSum}(\Pi_F v, z) = 0$. -/
theorem PiF_image_in_archive (v : Fin 33 → ℚ) (z : Fin 3) :
    zoneSum (mulv PiF v) z = 0 := by
  unfold zoneSum mulv
  rw [Finset.sum_filter]
  have h_comm : (∑ u, if zone u = z then (∑ w, PiF u w * v w) else 0) =
      ∑ w, (∑ u, if zone u = z then PiF u w else 0) * v w := by
    have h_push : (∑ u, if zone u = z then (∑ w, PiF u w * v w) else 0) =
        ∑ u, ∑ w, if zone u = z then PiF u w * v w else 0 := by
      refine Finset.sum_congr rfl fun u _ => ?_
      split_ifs <;> simp
    rw [h_push, Finset.sum_comm]
    refine Finset.sum_congr rfl fun w _ => ?_
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl fun u _ => ?_
    split_ifs <;> ring
  rw [h_comm]
  have h_congr : (∑ w, (∑ u, if zone u = z then PiF u w else 0) * v w) = ∑ w, (0 : ℚ) * v w := by
    refine Finset.sum_congr rfl fun w _ => ?_
    have hz : (∑ u : Fin 33, if zone31 u = z then PiF u w else 0) = 0 := PiF_col_sum_zone z w
    have hz_eq : (∑ u, if zone u = z then PiF u w else 0) = 0 := hz
    rw [hz_eq, zero_mul]
  rw [h_congr]
  simp

/-- **D0-CMB-FIEDLER-ACTIVE-SECTOR-DISJOINTNESS-001 (CORE-FORMALIZED).**
The Hodge-Fiedler spectral projector $\Pi_F$ is strictly supported on the dark archive
subspace, and is orthogonal to the Reynolds visible projector $Q$ and any visible-factored active
scalar curvature projector. -/
theorem fiedler_active_sector_disjointness_owner :
    Q * PiF = 0 ∧
    PiF * Q = 0 ∧
    (1 - Q) * PiF = PiF ∧
    PiF * (1 - Q) = PiF ∧
    (∀ (P_active : Matrix (Fin 33) (Fin 33) ℚ),
      P_active = P_active * Q → P_active = Q * P_active →
      P_active * PiF = 0 ∧ PiF * P_active = 0) ∧
    (∀ v z, zoneSum (mulv PiF v) z = 0) :=
  ⟨Q_mul_PiF_eq_zero,
   PiF_mul_Q_eq_zero,
   archive_P_mul_PiF.1,
   archive_P_mul_PiF.2,
   fun P_active hL hR => visible_subprojector_annihilates_PiF P_active hL hR,
   PiF_image_in_archive⟩

end D0.Cosmology.FiedlerActiveSectorDisjointness
