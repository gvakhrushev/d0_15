import Mathlib.Tactic

/-!
# A dense direct limit cannot inherit a nontrivial affine action levelwise

This capsule proves the analytic closure step used by the accompanying scoped
research note: a continuous operator on the completed direct-limit carrier is
determined by its action on the dense union of finite levels. The separate
finite Lorentz-covariant unitary theorem supplies the levelwise fixedness
hypothesis when every level is invariant under the affine action.
-/

namespace D0.Research.AffineDirectLimitLevelwiseNoGo

universe u

variable {K : Type} [NontriviallyNormedField K]
variable {E : Type u} [NormedAddCommGroup E] [NormedSpace K E]

/-- A continuous linear map fixed on a dense set is the identity everywhere. -/
theorem continuousLinearMap_eq_id_of_dense_fixed
    (T : E →L[K] E) (S : Set E) (hS : Dense S)
    (hfix : ∀ x ∈ S, T x = x) : T = ContinuousLinearMap.id K E := by
  have hclosed : IsClosed {x : E | T x = x} := isClosed_eq T.cont continuous_id
  have hsub : S ⊆ {x : E | T x = x} := by
    intro x hx
    exact hfix x hx
  have hclosure : closure S ⊆ {x : E | T x = x} := closure_minimal hsub hclosed
  apply ContinuousLinearMap.ext
  intro x
  exact hclosure (hS x)

/-- If a bounded translation operator is trivial on every finite level whose
union is dense, it is trivial on the completed carrier. -/
theorem directLimit_translation_eq_id
    {B : Type*} (T : B → E →L[K] E) (stages : ℕ → Set E)
    (hdense : Dense (⋃ n, stages n))
    (hlevel : ∀ b n x, x ∈ stages n → T b x = x) :
    ∀ b, T b = ContinuousLinearMap.id K E := by
  intro b
  apply continuousLinearMap_eq_id_of_dense_fixed (T b) (⋃ n, stages n) hdense
  intro x hx
  rcases Set.mem_iUnion.mp hx with ⟨n, hn⟩
  exact hlevel b n x hn

#check continuousLinearMap_eq_id_of_dense_fixed
#print axioms continuousLinearMap_eq_id_of_dense_fixed
#check directLimit_translation_eq_id
#print axioms directLimit_translation_eq_id

end D0.Research.AffineDirectLimitLevelwiseNoGo
