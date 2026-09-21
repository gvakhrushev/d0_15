import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# D0.Gravity.A2CompensatorNoether

The finite Weyl/Stueckelberg compensator mechanism for an arbitrary finite
unsigned edge carrier.  `BPlus` is the unsigned endpoint-sum/Weyl operator;
no signed Hodge incidence or Einstein/TT interpretation is used here.

The action is kept generic in its positive edge weight `W`.  A vertex profile
`rho` is only converted to the accepted edge weight
`1 / (rho source * rho target)` by an explicit definition; no unit-weight
specialisation is built into the theorem package.
-/

namespace D0.Gravity.A2CompensatorNoether

open BigOperators Matrix

variable {V E : Type*} [Fintype V] [Fintype E]
variable [DecidableEq V] [DecidableEq E]

/-- The literal unsigned endpoint-sum matrix for an oriented presentation of
an undirected edge carrier.  The orientation is only an indexing device: both
endpoints enter with sign `+1`. -/
def endpointIncidence (source target : E → V) : Matrix V E ℚ := fun v e =>
  (if v = source e then (1 : ℚ) else 0) +
    (if v = target e then (1 : ℚ) else 0)

/-- The unsigned Weyl/Ward divergence operator. -/
def BPlus (B : Matrix V E ℚ) (T : E → ℚ) : V → ℚ := B.mulVec T

/-- The unsigned vertex shift, `J = BPlusᵀ`. -/
def J (B : Matrix V E ℚ) (xi : V → ℚ) : E → ℚ := B.transpose.mulVec xi

/-- The accepted vertex-profile-induced edge weight. -/
def rhoWeight (source target : E → V) (rho : V → ℚ) : E → ℚ := fun e =>
  (rho (source e) * rho (target e))⁻¹

theorem endpointIncidence_shift (source target : E → V) (xi : V → ℚ) (e : E) :
    J (endpointIncidence source target) xi e =
      xi (source e) + xi (target e) := by
  simp only [J, Matrix.mulVec, dotProduct, transpose_apply,
    endpointIncidence, add_mul, Finset.sum_add_distrib]
  simp [eq_comm]

theorem rhoWeight_pos (source target : E → V) (rho : V → ℚ)
    (h_rho : ∀ v, 0 < rho v) (e : E) :
    0 < rhoWeight source target rho e := by
  unfold rhoWeight
  exact inv_pos.mpr (mul_pos (h_rho _) (h_rho _))

/-- `J = BPlusᵀ` is adjoint to the unsigned divergence under the finite
coordinate pairing. -/
theorem unsigned_shift_divergence_adjoint
    (B : Matrix V E ℚ) (T : E → ℚ) (xi : V → ℚ) :
    (∑ e, T e * J B xi e) =
      ∑ v, xi v * BPlus B T v := by
  unfold J BPlus
  simp only [Matrix.mulVec, dotProduct, transpose_apply]
  calc
    (∑ e, T e * ∑ v, B v e * xi v) =
        ∑ e, ∑ v, T e * (B v e * xi v) := by
      apply Finset.sum_congr rfl
      intro e he
      rw [Finset.mul_sum]
    _ = ∑ v, ∑ e, T e * (B v e * xi v) := by
      rw [Finset.sum_comm]
    _ = ∑ v, xi v * ∑ e, B v e * T e := by
      apply Finset.sum_congr rfl
      intro v hv
      calc
        (∑ e, T e * (B v e * xi v)) =
            ∑ e, xi v * (B v e * T e) := by
          apply Finset.sum_congr rfl
          intro e he
          ring
        _ = xi v * ∑ e, B v e * T e := by rw [Finset.mul_sum]

/-- Coordinatewise multiplication by an edge weight. -/
def weightedEdge (W : E → ℚ) (x : E → ℚ) : E → ℚ :=
  (Matrix.diagonal W).mulVec x

theorem weightedEdge_apply (W : E → ℚ) (x : E → ℚ) (e : E) :
    weightedEdge W x e = W e * x e := by
  classical
  simp [weightedEdge, Matrix.mulVec, dotProduct, Matrix.diagonal,
    eq_comm]

/-- The compensator-completed edge field
`w = h - (1/2) J eta`. -/
def compensatorResidual (B : Matrix V E ℚ) (h : E → ℚ) (eta : V → ℚ) : E → ℚ :=
  fun e => h e - (1 / 2 : ℚ) * J B eta e

/-- The finite A1 action for an arbitrary edge weight `W`. -/
def extendedAction (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (eta : V → ℚ) : ℚ :=
  2 * ∑ e, W e * (compensatorResidual B h eta e) ^ 2

theorem compensatorResidual_shift
    (B : Matrix V E ℚ) (h : E → ℚ) (eta xi : V → ℚ) :
    compensatorResidual B (h + J B xi) (eta + 2 • xi) =
      compensatorResidual B h eta := by
  funext e
  simp only [compensatorResidual, Pi.add_apply]
  rw [show J B (eta + 2 • xi) = J B eta + J B (2 • xi) by
    unfold J
    rw [Matrix.mulVec_add]]
  change h e + J B xi e - (1 / 2 : ℚ) *
      (J B eta e + J B (2 • xi) e) =
    h e - (1 / 2 : ℚ) * J B eta e
  rw [show J B (2 • xi) = 2 • J B xi by
    unfold J
    rw [Matrix.mulVec_smul]]
  simp only [Pi.smul_apply]
  ring

theorem extendedAction_shift_invariant
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ) (eta xi : V → ℚ) :
    extendedAction B W (h + J B xi) (eta + 2 • xi) =
      extendedAction B W h eta := by
  unfold extendedAction
  rw [compensatorResidual_shift]

/-- Edge Euler response, i.e. the derivative with respect to `h`. -/
def edgeResponse (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (eta : V → ℚ) : E → ℚ := fun e =>
  4 * W e * compensatorResidual B h eta e

/-- Diagonal response in the matrix convention `T_ii = 2 dS/d eta_i`. -/
def diagonalResponse (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (eta : V → ℚ) : V → ℚ := fun v =>
  -4 * BPlus B (weightedEdge W (compensatorResidual B h eta)) v

theorem edge_euler_response (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (eta : V → ℚ) (e : E) :
    edgeResponse B W h eta e =
      4 * W e * compensatorResidual B h eta e := rfl

theorem extendedAction_edge_variation
    (B : Matrix V E ℚ) (W : E → ℚ) (h dh : E → ℚ) (eta : V → ℚ) :
    extendedAction B W (h + dh) eta - extendedAction B W h eta =
      (∑ e, dh e * edgeResponse B W h eta e) +
        2 * ∑ e, W e * (dh e) ^ 2 := by
  have hres : ∀ e,
      compensatorResidual B (h + dh) eta e =
        compensatorResidual B h eta e + dh e := by
    intro e
    change h e + dh e - (1 / 2 : ℚ) * J B eta e =
      h e - (1 / 2 : ℚ) * J B eta e + dh e
    ring
  simp only [extendedAction]
  simp_rw [hres]
  unfold edgeResponse
  rw [show
      2 * ∑ e, W e * (compensatorResidual B h eta e + dh e) ^ 2 -
        2 * ∑ e, W e * (compensatorResidual B h eta e) ^ 2 =
      2 * ∑ e, W e *
        ((compensatorResidual B h eta e + dh e) ^ 2 -
          (compensatorResidual B h eta e) ^ 2) by
    calc
      2 * ∑ e, W e * (compensatorResidual B h eta e + dh e) ^ 2 -
          2 * ∑ e, W e * (compensatorResidual B h eta e) ^ 2 =
          2 * ((∑ e, W e * (compensatorResidual B h eta e + dh e) ^ 2) -
            ∑ e, W e * (compensatorResidual B h eta e) ^ 2) := by ring
      _ = 2 * ∑ e, W e *
          ((compensatorResidual B h eta e + dh e) ^ 2 -
            (compensatorResidual B h eta e) ^ 2) := by
        calc
          2 * ((∑ e, W e * (compensatorResidual B h eta e + dh e) ^ 2) -
              ∑ e, W e * compensatorResidual B h eta e ^ 2) =
              2 * ∑ e, (W e * (compensatorResidual B h eta e + dh e) ^ 2 -
                W e * compensatorResidual B h eta e ^ 2) := by
            rw [← Finset.sum_sub_distrib]
          _ = 2 * ∑ e, W e *
              ((compensatorResidual B h eta e + dh e) ^ 2 -
                compensatorResidual B h eta e ^ 2) := by
            congr 1
            apply Finset.sum_congr rfl
            intro e he
            ring]
  have hquad :
      (∑ e, W e * ((compensatorResidual B h eta e + dh e) ^ 2 -
        (compensatorResidual B h eta e) ^ 2)) =
        ∑ e, (2 * W e * compensatorResidual B h eta e * dh e +
          W e * (dh e) ^ 2) := by
    apply Finset.sum_congr rfl
    intro e he
    ring
  rw [hquad]
  calc
    2 * ∑ e, (2 * W e * compensatorResidual B h eta e * dh e +
        W e * (dh e) ^ 2) =
        ∑ e, 2 * (2 * W e * compensatorResidual B h eta e * dh e +
          W e * (dh e) ^ 2) := by rw [Finset.mul_sum]
    _ = ∑ e, (dh e * (4 * W e * compensatorResidual B h eta e) +
        2 * W e * (dh e) ^ 2) := by
      apply Finset.sum_congr rfl
      intro e he
      ring
    _ = (∑ e, dh e * (4 * W e * compensatorResidual B h eta e)) +
        2 * ∑ e, W e * (dh e) ^ 2 := by
      rw [Finset.sum_add_distrib]
      congr 1
      calc
        (∑ e, 2 * W e * (dh e) ^ 2) =
            ∑ e, 2 * (W e * (dh e) ^ 2) := by
          apply Finset.sum_congr rfl
          intro e he
          ring
        _ = 2 * ∑ e, W e * (dh e) ^ 2 := by rw [Finset.mul_sum]

theorem diagonal_euler_response (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (eta : V → ℚ) (v : V) :
    diagonalResponse B W h eta v =
      -4 * BPlus B (weightedEdge W (compensatorResidual B h eta)) v := rfl

theorem off_shell_ward_identity (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (eta : V → ℚ) :
    diagonalResponse B W h eta +
        BPlus B (edgeResponse B W h eta) = 0 := by
  funext v
  unfold diagonalResponse edgeResponse BPlus
  rw [show weightedEdge W (compensatorResidual B h eta) =
      fun e => W e * compensatorResidual B h eta e by
    funext e
    exact weightedEdge_apply W _ e]
  change -4 * ∑ x, B v x * (W x * compensatorResidual B h eta x) +
      ∑ x, B v x * (4 * W x * compensatorResidual B h eta x) = 0
  rw [show (∑ x, B v x * (4 * W x * compensatorResidual B h eta x)) =
      4 * ∑ x, B v x * (W x * compensatorResidual B h eta x) by
    calc
      (∑ x, B v x * (4 * W x * compensatorResidual B h eta x)) =
          ∑ x, 4 * (B v x * (W x * compensatorResidual B h eta x)) := by
            apply Finset.sum_congr rfl
            intro e he
            ring
      _ = 4 * ∑ x, B v x * (W x * compensatorResidual B h eta x) := by
            rw [Finset.mul_sum]]
  ring

/-- The normal operator `(B W Bᵀ)` used by compensator elimination. -/
def normalOperator (B : Matrix V E ℚ) (W : E → ℚ) :
    (V → ℚ) →ₗ[ℚ] (V → ℚ) :=
  B.mulVecLin.comp ((Matrix.diagonal W).mulVecLin.comp B.transpose.mulVecLin)

theorem normalOperator_apply (B : Matrix V E ℚ) (W : E → ℚ)
    (phi : V → ℚ) :
    normalOperator B W phi = BPlus B (weightedEdge W (J B phi)) := rfl

theorem normalOperator_pairing (B : Matrix V E ℚ) (W : E → ℚ)
    (x : V → ℚ) :
    dotProduct x (normalOperator B W x) =
      ∑ e, W e * (J B x e) ^ 2 := by
  have hadj := unsigned_shift_divergence_adjoint B
    (weightedEdge W (J B x)) x
  calc
    dotProduct x (normalOperator B W x) =
        ∑ v, x v * BPlus B (weightedEdge W (J B x)) v := rfl
    _ = ∑ e, weightedEdge W (J B x) e * J B x e := by
      exact hadj.symm
    _ = ∑ e, W e * (J B x e) ^ 2 := by
      apply Finset.sum_congr rfl
      intro e he
      rw [weightedEdge_apply]
      ring

theorem normalOperator_ker_eq_shift_ker
    (B : Matrix V E ℚ) (W : E → ℚ)
    (hW : ∀ e, 0 < W e) :
    LinearMap.ker (normalOperator B W) =
      LinearMap.ker B.transpose.mulVecLin := by
  apply le_antisymm
  · intro x hx
    apply LinearMap.mem_ker.mpr
    have hpair : dotProduct x (normalOperator B W x) = 0 := by
      rw [LinearMap.mem_ker.mp hx]
      simp
    rw [normalOperator_pairing] at hpair
    have hnonneg : ∀ e, 0 ≤ W e * (J B x e) ^ 2 := by
      intro e
      exact mul_nonneg (le_of_lt (hW e)) (sq_nonneg _)
    have hzero := (Finset.sum_eq_zero_iff_of_nonneg
      (fun e _ => hnonneg e)).mp hpair
    funext e
    have hterm := hzero e (Finset.mem_univ e)
    have hsq : (J B x e) ^ 2 = 0 := by
      nlinarith [hW e]
    exact sq_eq_zero_iff.mp hsq
  · intro x hx
    apply LinearMap.mem_ker.mpr
    have hx' : J B x = 0 := LinearMap.mem_ker.mp hx
    rw [normalOperator_apply, hx']
    simp [weightedEdge, BPlus, Matrix.mulVec, dotProduct]

theorem normalOperator_range_eq_divergence_range
    (B : Matrix V E ℚ) (W : E → ℚ)
    (hW : ∀ e, 0 < W e) :
    LinearMap.range (normalOperator B W) =
      LinearMap.range B.mulVecLin := by
  have hker := normalOperator_ker_eq_shift_ker B W hW
  have hN := LinearMap.finrank_range_add_finrank_ker (normalOperator B W)
  have hBT := LinearMap.finrank_range_add_finrank_ker B.transpose.mulVecLin
  rw [hker] at hN
  have hrank : Module.finrank ℚ
      (LinearMap.range B.transpose.mulVecLin) =
      Module.finrank ℚ (LinearMap.range B.mulVecLin) := by
    change Matrix.rank B.transpose = Matrix.rank B
    rw [Matrix.rank_transpose]
  have hdim : Module.finrank ℚ (LinearMap.range (normalOperator B W)) =
      Module.finrank ℚ (LinearMap.range B.mulVecLin) := by
    omega
  apply Submodule.eq_of_le_of_finrank_eq
  · intro y hy
    rcases hy with ⟨x, rfl⟩
    refine ⟨weightedEdge W (J B x), ?_⟩
    rfl
  · exact hdim

/-- The normal equation always has a solution for positive edge weights. -/
theorem normal_equation_exists
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ)
    (hW : ∀ e, 0 < W e) :
    ∃ phi, normalOperator B W phi = BPlus B (weightedEdge W h) := by
  have hrange := normalOperator_range_eq_divergence_range B W hW
  have hmem : BPlus B (weightedEdge W h) ∈ LinearMap.range B.mulVecLin := by
    exact ⟨weightedEdge W h, rfl⟩
  rw [← hrange] at hmem
  exact hmem

theorem physical_residual_unique
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ)
    (hW : ∀ e, 0 < W e)
    {phi psi : V → ℚ}
    (hphi : normalOperator B W phi = BPlus B (weightedEdge W h))
    (hpsi : normalOperator B W psi = BPlus B (weightedEdge W h)) :
    compensatorResidual B h (2 • phi) =
      compensatorResidual B h (2 • psi) := by
  have hdiff : normalOperator B W (phi - psi) = 0 := by
    rw [map_sub, hphi, hpsi, sub_self]
  have hker : phi - psi ∈ LinearMap.ker (normalOperator B W) :=
    LinearMap.mem_ker.mpr hdiff
  have hshift : J B (phi - psi) = 0 := by
    have hker' := hker
    rw [normalOperator_ker_eq_shift_ker B W hW] at hker'
    exact LinearMap.mem_ker.mp hker'
  have hsub : J B (phi - psi) = J B phi - J B psi := by
    unfold J
    rw [Matrix.mulVec_sub]
  have heq : J B phi = J B psi := by
    apply sub_eq_zero.mp
    rw [← hsub]
    exact hshift
  have h2 : J B (2 • phi) = J B (2 • psi) := by
    rw [show J B (2 • phi) = 2 • J B phi by
      unfold J
      rw [Matrix.mulVec_smul],
      show J B (2 • psi) = 2 • J B psi by
        unfold J
        rw [Matrix.mulVec_smul],
      heq]
  unfold compensatorResidual
  rw [h2]

/-- A solution of the normal equation gives the projected physical response. -/
def physicalResponse (B : Matrix V E ℚ) (W : E → ℚ)
    (h : E → ℚ) (phi : V → ℚ) : E → ℚ :=
  4 • weightedEdge W (compensatorResidual B h (2 • phi))

theorem physical_response_eq_edge_response
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ) (phi : V → ℚ) :
    physicalResponse B W h phi = edgeResponse B W h (2 • phi) := by
  funext e
  simp only [physicalResponse, Pi.smul_apply]
  rw [weightedEdge_apply]
  unfold edgeResponse
  ring

theorem physical_response_divergence_free
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ) (phi : V → ℚ)
    (hphi : normalOperator B W phi = BPlus B (weightedEdge W h)) :
    BPlus B (physicalResponse B W h phi) = 0 := by
  unfold physicalResponse
  have hsplit :
      weightedEdge W (compensatorResidual B h (2 • phi)) =
        weightedEdge W h - weightedEdge W (J B phi) := by
    funext e
    rw [weightedEdge_apply]
    simp only [Pi.sub_apply]
    rw [weightedEdge_apply, weightedEdge_apply]
    simp only [compensatorResidual]
    rw [show J B (2 • phi) = 2 • J B phi by
      unfold J
      rw [Matrix.mulVec_smul]]
    simp only [Pi.smul_apply]
    ring
  rw [hsplit]
  have hnormal :
      BPlus B (weightedEdge W (J B phi)) =
        BPlus B (weightedEdge W h) := by
    rw [← hphi, normalOperator_apply]
  change B.mulVec (4 • (weightedEdge W h - weightedEdge W (J B phi))) = 0
  rw [Matrix.mulVec_smul, Matrix.mulVec_sub]
  change 4 • (BPlus B (weightedEdge W h) -
    BPlus B (weightedEdge W (J B phi))) = 0
  rw [hnormal]
  simp

end D0.Gravity.A2CompensatorNoether
