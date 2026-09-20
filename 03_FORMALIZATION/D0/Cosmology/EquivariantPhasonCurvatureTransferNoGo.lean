import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Claims.Signature31Split
import D0.Claims.InvariantGenerationBridge
import D0.Cosmology.FiedlerProjectorOperator
import D0.Cosmology.FiedlerActiveSectorDisjointness
import D0.Spectral.DarkArchiveStructure
import D0.Synthesis.EquivariantSeamNoGo

/-!
# D0.Cosmology.EquivariantPhasonCurvatureTransferNoGo

Theoretical owner: `D0-CMB-EQUIVARIANT-PHASON-CURVATURE-TRANSFER-NOGO-001`.

Universal no-go theorem ruling out any canonical $\mathrm{Aut}(K(9,11,13))$-equivariant transfer
operator from the Hodge-Fiedler phason mode to the scalar curvature / active sector:

1. Let $T \in \mathrm{End}(\mathbb{Q}^{33})$ be ANY operator equivariant under all same-zone
   transpositions (generating $\mathrm{Aut}(K(9,11,13)) = S_9 \times S_{11} \times S_{13}$).
2. By `D0.Synthesis.EquivariantSeamNoGo.archive_invariant`, $T$ maps zone-balanced archive
   states to zone-balanced archive states:
   $$\forall v \in H_{\mathrm{archive}}, \quad T v \in H_{\mathrm{archive}}.$$
3. Since $\operatorname{im}(\Pi_F) \subset H_{\mathrm{archive}}$ (`PiF_image_in_archive`),
   every column of $T \Pi_F$ is strictly zone-balanced.
4. The visible Reynolds projector $Q = \sum_z \frac{1}{|z|} \mathbf{1}_z \mathbf{1}_z^T$
   acts on any zone-balanced vector as zero:
   $$Q (T \Pi_F) = 0.$$
5. Any visible or active scalar curvature projector $P_{\mathrm{active}}$ that factors through
   the visible sector ($P_{\mathrm{active}} = P_{\mathrm{active}} Q$) identically satisfies:
   $$P_{\mathrm{active}} \cdot T \cdot \Pi_F = 0.$$

Physical consequence:
Neither the scene adjacency matrix, nor the graph Laplacian $L$, nor the normalized Laplacian,
nor any resolvent $(L + k^2)^{-1}$, nor heat-kernel covariance $e^{-t L}$, nor ANY polynomial
or function of them can produce a non-zero phason-to-curvature transfer operator $T_{\mathcal R}$.
Any non-zero transfer operator necessarily requires external symmetry-breaking data outside the
scene's automorphism group.
-/

namespace D0.Cosmology.EquivariantPhasonCurvatureTransferNoGo

open D0.Claims
open D0.Claims.InvariantGenerationBridge
open D0.Cosmology.FiedlerProjectorOperator
open D0.Cosmology.FiedlerActiveSectorDisjointness
open D0.Spectral.DarkArchiveStructure
open D0.Synthesis.EquivariantSeamNoGo

/-- The Reynolds projector $Q$ annihilates any zone-balanced vector. -/
theorem Q_annihilates_zone_balanced (w : Fin 33 → ℚ) (hw : ∀ z : Fin 3, zoneSum w z = 0) :
    ∀ i : Fin 33, (∑ j : Fin 33, Q i j * w j) = 0 := by
  intro i
  simp only [Q, Matrix.of_apply]
  have h_split : (∑ j : Fin 33, (if zone31 i = zone31 j then (zoneSize (zone31 i))⁻¹ else 0) * w j) =
      (zoneSize (zone31 i))⁻¹ * (∑ j : Fin 33, if zone31 i = zone31 j then w j else 0) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    split_ifs <;> ring
  rw [h_split]
  have h_zone_sum : (∑ j : Fin 33, if zone31 i = zone31 j then w j else 0) =
      zoneSum w (zone31 i) := by
    unfold zoneSum
    rw [Finset.sum_filter]
    refine Finset.sum_congr rfl fun j _ => ?_
    have h_eq : (zone31 i = zone31 j) ↔ (zone j = zone31 i) := by
      constructor
      · intro h; exact h.symm
      · intro h; exact h.symm
    by_cases h : zone31 i = zone31 j
    · have h' : zone j = zone31 i := h_eq.mp h
      simp [h, h']
    · have h' : ¬ (zone j = zone31 i) := fun h_contra => h (h_eq.mpr h_contra)
      simp [h, h']
  rw [h_zone_sum, hw (zone31 i), mul_zero]

/-- Matrix-matrix action against Reynolds projector: if every column of $M$ is zone-balanced,
then $Q \cdot M = 0$. -/
theorem Q_mul_matrix_eq_zero_of_columns_balanced (M : Matrix (Fin 33) (Fin 33) ℚ)
    (h_cols : ∀ j : Fin 33, ∀ z : Fin 3, zoneSum (fun i => M i j) z = 0) :
    Q * M = 0 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.zero_apply]
  exact Q_annihilates_zone_balanced (fun k => M k j) (h_cols j) i

/-- **Universal Transfer No-Go Theorem.**
For ANY $\mathrm{Aut}(K(9,11,13))$-equivariant operator $T$, the Reynolds-factored transfer
$Q \cdot T \cdot \Pi_F$ is identically zero. -/
theorem equivariant_transfer_annihilated_by_Q
    (T : Matrix (Fin 33) (Fin 33) ℚ)
    (hT : Equivariant (fun i j => T i j)) :
    Q * (T * PiF) = 0 := by
  apply Q_mul_matrix_eq_zero_of_columns_balanced
  intro j z
  have h_col : (fun i => (T * PiF) i j) = Synthesis.EquivariantSeamNoGo.mulv (fun i j => T i j) (fun k => PiF k j) := by
    ext i
    unfold Synthesis.EquivariantSeamNoGo.mulv
    simp only [Matrix.mul_apply]
  rw [h_col]
  have h_arch_col : ∀ z' : Fin 3, zoneSum (fun k => PiF k j) z' = 0 := by
    intro z'
    have h_sum := PiF_col_sum_zone z' j
    unfold zoneSum
    rw [Finset.sum_filter]
    refine Eq.trans ?_ h_sum
    refine Finset.sum_congr rfl fun k _ => ?_
    by_cases hz : zone k = z'
    · have hz' : zone31 k = z' := hz
      simp [hz, hz']
    · have hz' : ¬ (zone31 k = z') := hz
      simp [hz, hz']
  exact archive_invariant (fun i j => T i j) hT (fun k => PiF k j) h_arch_col z

/-- **Corollary: Active Scalar Curvature Transfer Vanishes Identically.**
Any active scalar curvature projector $P_{\mathrm{active}}$ factoring through the visible sector
($P_{\mathrm{active}} = P_{\mathrm{active}} Q$) strictly satisfies:
$$P_{\mathrm{active}} \cdot T \cdot \Pi_F = 0.$$ -/
theorem equivariant_phason_curvature_transfer_nogo
    (T : Matrix (Fin 33) (Fin 33) ℚ)
    (hT : Equivariant (fun i j => T i j))
    (P_active : Matrix (Fin 33) (Fin 33) ℚ)
    (hP : P_active = P_active * Q) :
    P_active * T * PiF = 0 := by
  have h_assoc : P_active * T * PiF = P_active * (T * PiF) := by simp only [Matrix.mul_assoc]
  rw [h_assoc, hP]
  have h_assoc2 : (P_active * Q) * (T * PiF) = P_active * (Q * (T * PiF)) := by
    simp only [Matrix.mul_assoc]
  rw [h_assoc2, equivariant_transfer_annihilated_by_Q T hT, Matrix.mul_zero]

/-- Adjacency is $\mathrm{Aut}$-equivariant. -/
theorem adj31_equivariant : Equivariant (fun i j => Adj31 i j) := by
  intro a b hab u w
  revert a b u w
  native_decide

/-- Laplacian is $\mathrm{Aut}$-equivariant. -/
theorem lap_equivariant : Equivariant (fun i j => Lap i j) := by
  intro a b hab u w
  revert a b u w
  native_decide

/-- **D0-CMB-EQUIVARIANT-PHASON-CURVATURE-TRANSFER-NOGO-001 (CORE-FORMALIZED).**
Every $\mathrm{Aut}(K(9,11,13))$-equivariant operator $T$ identically satisfies
$P_{\mathrm{active}} T \Pi_F = 0$. In particular, the adjacency and graph Laplacian can never
couple the Hodge-Fiedler phason mode to the observable scalar curvature sector. -/
theorem equivariant_phason_curvature_transfer_owner :
    (∀ (T : Matrix (Fin 33) (Fin 33) ℚ), Equivariant (fun i j => T i j) → Q * (T * PiF) = 0) ∧
    (∀ (T P_active : Matrix (Fin 33) (Fin 33) ℚ),
      Equivariant (fun i j => T i j) → P_active = P_active * Q → P_active * T * PiF = 0) ∧
    Equivariant (fun i j => Adj31 i j) ∧
    Equivariant (fun i j => Lap i j) :=
  ⟨equivariant_transfer_annihilated_by_Q,
   fun T P hT hP => equivariant_phason_curvature_transfer_nogo T hT P hP,
   adj31_equivariant,
   lap_equivariant⟩

end D0.Cosmology.EquivariantPhasonCurvatureTransferNoGo
