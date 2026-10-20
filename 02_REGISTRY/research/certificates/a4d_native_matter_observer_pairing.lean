import D0.Geometry.A4DObserverPositiveExterior
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Inv

/-! Generic joint rank-one and norm derivatives. This is a research capsule,
not a supported CORE owner, a full Lorentz Hom formalization or a physical
selection of the pairing as native heat. -/
namespace D0.Research.MatterObserverPairing
noncomputable section
open scoped BigOperators

def normContraction {I : Type*} [Fintype I]
    (a : I → I → ℝ) (v : I → ℝ) : ℝ :=
  ∑ i, ∑ j, v i * a i j * v j

def normTangent {I : Type*} [Fintype I]
    (a da : I → I → ℝ) (v w : I → ℝ) : ℝ :=
  ∑ i, ∑ j, (w i * a i j * v j + v i * da i j * v j + v i * a i j * w j)

theorem normContraction_hasDerivAt {I : Type*} [Fintype I]
    (a : ℝ → I → I → ℝ) (v : ℝ → I → ℝ)
    (da : I → I → ℝ) (w : I → ℝ) (t : ℝ)
    (ha : ∀ i j, HasDerivAt (fun s => a s i j) (da i j) t)
    (hv : ∀ i, HasDerivAt (fun s => v s i) (w i) t) :
    HasDerivAt (fun s => normContraction (a s) (v s))
      (normTangent (a t) da (v t) w) t := by
  unfold normContraction normTangent
  apply HasDerivAt.fun_sum
  intro i hi
  apply HasDerivAt.fun_sum
  intro j hj
  convert ((hv i).mul (ha i j)).mul (hv j) using 1
  dsimp
  ring

def pairingEntry (q vi vj k : ℝ) : ℝ := -q + 2 * vi * vj / k

theorem pairingEntry_hasDerivAt
    (q vi vj k : ℝ → ℝ) (dq wi wj dk t : ℝ)
    (hq : HasDerivAt q dq t) (hi : HasDerivAt vi wi t)
    (hj : HasDerivAt vj wj t) (hk : HasDerivAt k dk t) (hk0 : k t ≠ 0) :
    HasDerivAt (fun s => pairingEntry (q s) (vi s) (vj s) (k s))
      (-dq + 2 * (wi * vj t + vi t * wj) / k t
        - 2 * dk * vi t * vj t / (k t)^2) t := by
  have hprod := ((hasDerivAt_const t (2 : ℝ)).mul hi).mul hj
  have h := hq.neg.add (hprod.div hk hk0)
  convert h using 1
  dsimp
  field_simp
  ring

theorem pairingEntry_scale_invariant (q vi vj k c : ℝ)
    (hk : k ≠ 0) (hc : c ≠ 0) :
    pairingEntry q (c*vi) (c*vj) (c^2*k) = pairingEntry q vi vj k := by
  unfold pairingEntry
  field_simp

theorem pairingEntry_radial_matter_tangent (vi vj k c : ℝ) (hk : k ≠ 0) :
    2 * (c*vi*vj + vi*(c*vj)) / k - 2 * (2*c*k) * vi * vj / k^2 = 0 := by
  field_simp
  ring

theorem pairingEntry_metric_dilation_tangent (q vi vj k : ℝ) (hk : k ≠ 0) :
    -(2*q) - 2 * (-2*k) * vi * vj / k^2 = 2 * pairingEntry q vi vj k := by
  unfold pairingEntry
  field_simp
  ring

end
end D0.Research.MatterObserverPairing

#check D0.Research.MatterObserverPairing.normContraction_hasDerivAt
#check D0.Research.MatterObserverPairing.pairingEntry_hasDerivAt
#print axioms D0.Research.MatterObserverPairing.normContraction_hasDerivAt
#print axioms D0.Research.MatterObserverPairing.pairingEntry_hasDerivAt
#print axioms D0.Research.MatterObserverPairing.pairingEntry_scale_invariant
#print axioms D0.Research.MatterObserverPairing.pairingEntry_radial_matter_tangent
#print axioms D0.Research.MatterObserverPairing.pairingEntry_metric_dilation_tangent
#print axioms D0.Geometry.observerMetric_posDef
#print axioms D0.Geometry.observerExteriorBladeGram_pos
