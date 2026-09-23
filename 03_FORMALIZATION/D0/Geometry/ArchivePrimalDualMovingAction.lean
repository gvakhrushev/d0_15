import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Dual.Basis
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Tactic

/-!
# Pairing-forced primal/dual action and passive Hodge transport

A perfect pairing `e : P ≃ D*` forces the dual equivalence of a primal equivalence `Q`.
The same `Q` is not chosen twice. In the standard dot-product coordinates the forced
dual map is `Q⁻ᵀ`.

`movingHodge` is passive covariance of a supplied map `S`. It is not a constitutive
selector. `fixesHodge` is the stricter condition that the supplied `S` is unchanged.
Those two statements agree only on the stabilizer of `S`.
-/

namespace D0.Geometry

noncomputable section

open Module

variable {K P D : Type*} [Field K]
variable [AddCommGroup P] [Module K P]
variable [AddCommGroup D] [Module K D]

/-- Transport of `Q` to the dual space along the supplied pairing equivalence. -/
def dualTransport (e : P ≃ₗ[K] Dual K D) (Q : P ≃ₗ[K] P) :
    Dual K D ≃ₗ[K] Dual K D :=
  e.symm.trans (Q.symm.trans e)

/-- The unique dual action compatible with `e`. Reflexivity sends it back to `D`. -/
def dualAction (e : P ≃ₗ[K] Dual K D) (Q : P ≃ₗ[K] P) [IsReflexive K D] :
    D ≃ₗ[K] D :=
  (evalEquiv K D).trans ((dualTransport e Q).dualMap.trans (evalEquiv K D).symm)

theorem pairing_dualAction
    (e : P ≃ₗ[K] Dual K D) (Q : P ≃ₗ[K] P) [IsReflexive K D] (p : P) (d : D) :
    e (Q p) (dualAction e Q d) = e p d := by
  set L : Dual K D ≃ₗ[K] Dual K D := dualTransport e Q
  have htransport : L (e (Q p)) = e p := by
    simp [L, dualTransport, LinearEquiv.trans_apply]
  calc
    e (Q p) (dualAction e Q d) =
        e (Q p) ((evalEquiv K D).symm (L.dualMap (evalEquiv K D d))) := by
          rfl
    _ = L.dualMap (evalEquiv K D d) (e (Q p)) := by
          simpa using (apply_evalEquiv_symm_apply (e (Q p)) (L.dualMap (evalEquiv K D d)))
    _ = evalEquiv K D d (L (e (Q p))) := by
          rw [LinearEquiv.dualMap_apply]
    _ = L (e (Q p)) d := by
          rw [evalEquiv_apply, Dual.eval_apply]
    _ = e p d := by
          rw [htransport]

/-- Two linear maps preserving the paired action agree. -/
theorem dualAction_unique
    (e : P ≃ₗ[K] Dual K D) (Q : P ≃ₗ[K] P) [IsReflexive K D]
    (R S : D →ₗ[K] D)
    (hR : ∀ p d, e (Q p) (R d) = e p d)
    (hS : ∀ p d, e (Q p) (S d) = e p d) :
    R = S := by
  ext d
  refine (evalEquiv K D).injective ?_
  ext φ
  obtain ⟨q, rfl⟩ := e.surjective φ
  obtain ⟨p, rfl⟩ := Q.surjective q
  rw [evalEquiv_apply, Dual.eval_apply, evalEquiv_apply, Dual.eval_apply, hR, hS]

theorem dualAction_mul
    (e : P ≃ₗ[K] Dual K D) (Q S : P ≃ₗ[K] P) [IsReflexive K D] :
    dualAction e (Q.trans S) = (dualAction e Q).trans (dualAction e S) := by
  apply LinearEquiv.toLinearMap_injective
  apply dualAction_unique e (Q.trans S)
    (dualAction e (Q.trans S)).toLinearMap
    ((dualAction e Q).trans (dualAction e S)).toLinearMap
  · intro p d
    exact pairing_dualAction e (Q.trans S) p d
  · intro p d
    change e (S (Q p)) (dualAction e S (dualAction e Q d)) = e p d
    rw [pairing_dualAction, pairing_dualAction]

theorem dualAction_inv
    (e : P ≃ₗ[K] Dual K D) (Q : P ≃ₗ[K] P) [IsReflexive K D] :
    dualAction e Q.symm = (dualAction e Q).symm := by
  apply LinearEquiv.toLinearMap_injective
  apply dualAction_unique e Q.symm
    (dualAction e Q.symm).toLinearMap (dualAction e Q).symm.toLinearMap
  · intro p d
    exact pairing_dualAction e Q.symm p d
  · intro p d
    simpa using
      (pairing_dualAction e Q (Q.symm p) ((dualAction e Q).symm d)).symm

/-- Passive moving law `S' = Q_D ∘ S ∘ Q_P⁻¹` for a supplied map. Not a selector. -/
def movingHodge (QD : D ≃ₗ[K] D) (S : P →ₗ[K] D) (QP : P ≃ₗ[K] P) : P →ₗ[K] D :=
  QD.toLinearMap.comp (S.comp QP.symm.toLinearMap)

/-- Fixed intertwiner `Q_D ∘ S = S ∘ Q_P`. This keeps `S` itself unchanged. -/
def fixesHodge (QD : D ≃ₗ[K] D) (S : P →ₗ[K] D) (QP : P ≃ₗ[K] P) : Prop :=
  QD.toLinearMap.comp S = S.comp QP.toLinearMap

theorem movingHodge_comp
    (QD RD : D ≃ₗ[K] D) (QP RP : P ≃ₗ[K] P) (S : P →ₗ[K] D) :
    movingHodge (QD.trans RD) S (QP.trans RP) =
      movingHodge RD (movingHodge QD S QP) RP := by
  ext v
  simp [movingHodge, LinearEquiv.trans_apply]

/-- The moved tensor equals the original tensor exactly on the fixed-intertwiner locus. -/
theorem movingHodge_eq_self_iff_fixed
    (QD : D ≃ₗ[K] D) (S : P →ₗ[K] D) (QP : P ≃ₗ[K] P) :
    movingHodge QD S QP = S ↔ fixesHodge QD S QP := by
  constructor
  · intro h
    ext v
    have hv := congrFun (congrArg DFunLike.coe h) (QP v)
    simpa [movingHodge] using hv
  · intro h
    ext v
    have hv := congrFun (congrArg DFunLike.coe h) (QP.symm v)
    simpa [movingHodge, h] using hv

/-- Under the pairing-forced dual, fixed symmetry is congruence invariance of `u ↦ e u ∘ S`. -/
theorem fixedHodge_iff_bilinearStabilizer
    (e : P ≃ₗ[K] Dual K D) (Q : P ≃ₗ[K] P) (S : P →ₗ[K] D) [IsReflexive K D] :
    fixesHodge (dualAction e Q) S Q ↔
      ∀ u v, e (Q u) (S (Q v)) = e u (S v) := by
  constructor
  · intro h u v
    have hfix : dualAction e Q (S v) = S (Q v) := by
      simpa using congrFun (congrArg DFunLike.coe h) v
    rw [← hfix]
    exact pairing_dualAction e Q u (S v)
  · intro h
    ext v
    refine (evalEquiv K D).injective ?_
    ext φ
    obtain ⟨q, rfl⟩ := e.surjective φ
    obtain ⟨u, rfl⟩ := Q.surjective q
    rw [evalEquiv_apply, Dual.eval_apply, evalEquiv_apply, Dual.eval_apply]
    calc
      e (Q u) ((dualAction e Q) (S v)) = e u (S v) :=
        pairing_dualAction e Q u (S v)
      _ = e (Q u) (S (Q v)) := (h u v).symm

/-! ## Dot-product coordinates

On `ι → K` with the basis pairing, the forced dual action is inverse transpose.
-/

open scoped Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem dotToDual_apply (p d : ι → K) :
    ((Pi.basisFun K ι).toDualEquiv p) d = ∑ i, p i * d i := by
  rw [Basis.toDualEquiv_apply]
  conv_lhs => rw [← (Pi.basisFun K ι).sum_repr d]
  rw [map_sum]
  simp only [LinearMap.map_smul, Basis.toDual_apply_left, Pi.basisFun_repr, smul_eq_mul]
  refine Finset.sum_congr rfl ?_
  intro _ _
  ring

/-- In dot-product coordinates, the matrix of `dualAction Q` is `Q⁻ᵀ`. -/
theorem dualAction_invTranspose (Q : (ι → K) ≃ₗ[K] (ι → K)) :
    LinearMap.toMatrix' (dualAction (Pi.basisFun K ι).toDualEquiv Q).toLinearMap =
      (LinearMap.toMatrix' Q.symm.toLinearMap).transpose := by
  ext i j
  rw [LinearMap.toMatrix'_apply, Matrix.transpose_apply, LinearMap.toMatrix'_apply]
  have hpair := pairing_dualAction (Pi.basisFun K ι).toDualEquiv Q
    (Q.symm (Pi.single i 1)) (Pi.single j 1)
  rw [LinearEquiv.apply_symm_apply, dotToDual_apply, dotToDual_apply] at hpair
  simp only [Pi.single_apply, mul_ite, ite_mul, one_mul, zero_mul, mul_one,
    mul_zero, Finset.sum_ite_eq', Finset.mem_univ, if_true] at hpair
  exact hpair

end

end D0.Geometry
