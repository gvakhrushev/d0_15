import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

set_option linter.unusedSectionVars false

/-!
# D0.VNext2.GenericEndpointExpectationCanonicity

Theoretical owner: `D0-ENDPOINT-REYNOLDS-EXPECTATION-CANONICITY-001`.

Canonicity of the Reynolds conditional expectation for any finite quotient projection:
1. For any surjective map $e : H \to V$ between finite types, an admissible row-weight family
   $w : V \to H \to \mathbb{Q}$ is required to satisfy:
   - Support: $e(h) \neq v \implies w(v, h) = 0$;
   - Fiber symmetry: $e(h) = v = e(k) \implies w(v, h) = w(v, k)$;
   - Normalization: $\sum_{h : H} w(v, h) = 1$.
2. Theorem `fiber_symmetric_expectation_unique`:
   For every $v \in V$ and $h \in H$,
   $$w(v, h) = \begin{cases} \frac{1}{\#(e^{-1}(v))}, & \text{if } e(h) = v, \\ 0, & \text{otherwise.} \end{cases}$$
3. Conceptual integration:
   - Any non-uniform weighting inside an endpoint fiber necessarily consumes information
     that the quotient projection $e$ declared forgotten.
   - Parallels `D0.Foundation.CurrentDataFactorization`: history-invariance $\iff$ unique descent
     to current data.
   - Parallels `D0.Synthesis.AutomorphismHodgeSDEDecomposition`: orbit averaging $R$, lift $C$,
     with $R C = I$ and $C R = P_{\mathrm{Reynolds}}$.
-/

namespace D0.VNext2.GenericEndpointExpectationCanonicity

variable {H V : Type*} [Fintype H] [Fintype V] [DecidableEq H] [DecidableEq V]

/-- Fiber of the projection $e : H \to V$ above $v$. -/
def fiber (e : H → V) (v : V) : Finset H :=
  Finset.univ.filter (fun h => e h = v)

/-- Cardinality of the fiber above $v$ as a rational number. -/
def fiberMass (e : H → V) (v : V) : ℚ :=
  ((fiber e v).card : ℚ)

/-- Admissible expectation weights: supported on the fiber, fiber-symmetric, and normalized. -/
structure AdmissibleFiberExpectation (e : H → V) (w : V → H → ℚ) : Prop where
  support : ∀ v h, e h ≠ v → w v h = 0
  fiber_symm : ∀ v h k, e h = v → e k = v → w v h = w v k
  normalized : ∀ v, (∑ h : H, w v h) = 1

/-- **Theorem: Uniqueness of Fiber-Symmetric Expectation.**
The only admissible fiber-symmetric conditional expectation is the uniform Reynolds average
on each fiber. -/
theorem fiber_symmetric_expectation_unique
    (e : H → V) (he_surj : Function.Surjective e)
    (w : V → H → ℚ) (hadm : AdmissibleFiberExpectation e w) (v : V) (h : H) :
    w v h = if e h = v then (fiberMass e v)⁻¹ else 0 := by
  by_cases heh : e h = v
  · rw [if_pos heh]
    obtain ⟨h0, hh0⟩ := he_surj v
    have h_card_pos : 0 < (fiber e v).card := by
      have : h0 ∈ fiber e v := by
        simp only [fiber, Finset.mem_filter, Finset.mem_univ, true_and]
        exact hh0
      exact Finset.card_pos.mpr ⟨h0, this⟩
    have h_mass_ne_zero : fiberMass e v ≠ 0 := by
      unfold fiberMass
      exact Nat.cast_ne_zero.mpr (ne_of_gt h_card_pos)
    have h_sum := hadm.normalized v
    have h_split : (∑ k : H, w v k) = (∑ k ∈ fiber e v, w v k) := by
      rw [← Finset.sum_subset (Finset.subset_univ (fiber e v))]
      intro k _ hk_not
      have h_ne : e k ≠ v := by
        intro h_eq
        apply hk_not
        simp [fiber, h_eq]
      exact hadm.support v k h_ne
    rw [h_split] at h_sum
    have h_const : ∀ k ∈ fiber e v, w v k = w v h := by
      intro k hk
      simp only [fiber, Finset.mem_filter, Finset.mem_univ, true_and] at hk
      exact hadm.fiber_symm v k h hk heh
    have h_sum_const : (∑ k ∈ fiber e v, w v k) = (fiber e v).card * w v h := by
      rw [Finset.sum_congr rfl h_const]
      rw [Finset.sum_const]
      rfl
    rw [h_sum_const] at h_sum
    have h_eq_mul : (fiberMass e v) * w v h = 1 := by
      unfold fiberMass
      exact h_sum
    exact eq_inv_of_mul_eq_one_right h_eq_mul
  · rw [if_neg heh]
    exact hadm.support v h heh

/-- Canonical Reynolds average operator on fibers. -/
def canonicalReynoldsWeight (e : H → V) (v : V) (h : H) : ℚ :=
  if e h = v then (fiberMass e v)⁻¹ else 0

/-- The canonical Reynolds weight is admissible. -/
theorem canonicalReynoldsWeight_admissible
    (e : H → V) (he_surj : Function.Surjective e) :
    AdmissibleFiberExpectation e (canonicalReynoldsWeight e) := by
  refine ⟨?_, ?_, ?_⟩
  · intro v h h_ne
    unfold canonicalReynoldsWeight
    rw [if_neg h_ne]
  · intro v h k hh hk
    unfold canonicalReynoldsWeight
    rw [if_pos hh, if_pos hk]
  · intro v
    unfold canonicalReynoldsWeight
    obtain ⟨h0, hh0⟩ := he_surj v
    have h_card_pos : 0 < (fiber e v).card := by
      have : h0 ∈ fiber e v := by
        simp only [fiber, Finset.mem_filter, Finset.mem_univ, true_and]
        exact hh0
      exact Finset.card_pos.mpr ⟨h0, this⟩
    have h_mass_ne_zero : fiberMass e v ≠ 0 := by
      unfold fiberMass
      exact Nat.cast_ne_zero.mpr (ne_of_gt h_card_pos)
    have h_split : (∑ h : H, (if e h = v then (fiberMass e v)⁻¹ else 0)) =
        (∑ h ∈ fiber e v, (if e h = v then (fiberMass e v)⁻¹ else 0)) := by
      rw [← Finset.sum_subset (Finset.subset_univ (fiber e v))]
      intro h _ hk_not
      have h_ne : e h ≠ v := by
        intro h_eq
        apply hk_not
        simp [fiber, h_eq]
      rw [if_neg h_ne]
    have h_inner : (∑ h ∈ fiber e v, (if e h = v then (fiberMass e v)⁻¹ else 0)) =
        (∑ h ∈ fiber e v, (fiberMass e v)⁻¹) := by
      refine Finset.sum_congr rfl ?_
      intro x hx
      simp only [fiber, Finset.mem_filter] at hx
      rw [if_pos hx.2]
    rw [h_split, h_inner, Finset.sum_const]
    have h_cast : ((fiber e v).card : ℚ) = fiberMass e v := rfl
    rw [nsmul_eq_mul, h_cast]
    exact mul_inv_cancel₀ h_mass_ne_zero

/-- **D0-ENDPOINT-REYNOLDS-EXPECTATION-CANONICITY-001 (CORE-FORMALIZED).**
The uniform Reynolds fiber average is the unique admissible expectation operator for any
finite quotient projection. Any non-uniform weighting uses information forgotten by the quotient. -/
theorem endpoint_reynolds_expectation_canonicity_owner
    (e : H → V) (he_surj : Function.Surjective e) :
    (∃! w : V → H → ℚ, AdmissibleFiberExpectation e w) ∧
    (∀ w : V → H → ℚ, AdmissibleFiberExpectation e w → w = canonicalReynoldsWeight e) := by
  have h_exist : AdmissibleFiberExpectation e (canonicalReynoldsWeight e) :=
    canonicalReynoldsWeight_admissible e he_surj
  have h_unique : ∀ w, AdmissibleFiberExpectation e w → w = canonicalReynoldsWeight e := by
    intro w hw
    ext v h
    have h_val := fiber_symmetric_expectation_unique e he_surj w hw v h
    unfold canonicalReynoldsWeight
    exact h_val
  refine ⟨⟨canonicalReynoldsWeight e, h_exist, fun y hy => h_unique y hy⟩, h_unique⟩

end D0.VNext2.GenericEndpointExpectationCanonicity
