import Mathlib.Tactic
import D0.Geometry.A4DDiscreteEnergyKernel
import D0.Geometry.ArchivePathWordAlgebra

/-!
# The owned first jet is an additive length-at-most-two path expression

`flatStaggeredH` is not redefined. The identities below are the literal
average `A_r = (I + U_r⁻¹) / 2`, the two-word flux
`M_e U_s A_r E_sr = ½ M_e (U_s + U_s U_r⁻¹) E_sr`, and the symmetric scalar
link. Same-role corners contribute the empty spatial word. Distinct roles
contribute a length-two corner. CAR endomorphisms and their adjoints stay in
the sum. The equal weights `1/2` are the owned coefficients; path
concatenation is not used to select them.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

/-- Literal average `A_r = (I + U_r⁻¹) / 2` on each Fock component. -/
theorem backwardAverage_half_identity_plus_inverse (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    cochainBackwardAverage N r ψ =
      fun p => (ψ p + cochainBackwardShift N r ψ p) / 2 := by
  funext p
  simp [cochainBackwardAverage, backwardAverage, cochainBackwardShift]

/-- `M_e U_s A_r E_sr = ½ M_e (U_s + U_s U_r⁻¹) E_sr`. -/
theorem fluxForward_half_two_words (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (ψ : ArchiveCochain N) :
    cochainFluxForward N e s r ψ =
      fun p =>
        e p.1 *
          (cochainCarEnd N s r ψ (roleTranslatePlus N s p.1, p.2) +
            cochainCarEnd N s r ψ
              (roleTranslateMinus N r (roleTranslatePlus N s p.1), p.2)) / 2 := by
  funext p
  exact cochainFluxForward_corner_expansion N e s r ψ p.1 p.2

/-- Same-role second source is the original site: the empty spatial word. -/
theorem sameRole_corner_is_onsite (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslateMinus N r (roleTranslatePlus N r x) = x := by
  rw [roleTranslateMinus_apply, roleTranslatePlus_apply]
  abel

theorem fluxForward_sameRole_onsite (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (r : Role) (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) :
    cochainFluxForward N e r r ψ (x, S) =
      e x * (cochainCarEnd N r r ψ (roleTranslatePlus N r x, S) +
        cochainCarEnd N r r ψ (x, S)) / 2 := by
  rw [cochainFluxForward_corner_expansion, sameRole_corner_is_onsite]

/-- Symmetric scalar link: one forward edge and one backward edge. -/
theorem linkSymmetric_oneEdge_pair (N : ℕ) (r : Role)
    (a : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    cochainLinkSymmetric N r a ψ =
      fun p =>
        (a p.1 * ψ (roleTranslatePlus N r p.1, p.2) +
          a (roleTranslateMinus N r p.1) *
            ψ (roleTranslateMinus N r p.1, p.2)) / 2 := rfl

/-- Full owned first jet, as the link sum minus forward flux and adjoint. -/
theorem flatStaggeredH_additive_expansion (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    flatStaggeredH N e ψ =
      (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) -
        ∑ s : Role, ∑ r : Role,
          (cochainFluxForward N (fun x => e x s r) s r ψ +
            cochainFluxAdjoint N (fun x => e x s r) s r ψ) := by
  funext p
  simp [flatStaggeredH, Pi.sub_apply, Pi.add_apply, Finset.sum_apply]

/-- Empty word, one-edge words, and one length-two corner.
CAR endomorphisms are fibre operators and are not spatial letters. -/
def firstJetPathExpression : PathExpr Unit :=
  .add
    (.add (.word []) (.word [()]))
    (.add (.word [()]) (.word [(), ()]))

theorem firstJetPathExpression_maxLength :
    (pathExprCost firstJetPathExpression).maxWordLength = 2 := by
  simp [firstJetPathExpression, pathExprCost]

theorem firstJetPathExpression_not_single_word :
    ∀ w : List Unit, firstJetPathExpression ≠ PathExpr.word w := by
  intro w
  simp [firstJetPathExpression]

theorem firstJet_lengthAtMostTwo_additive (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    flatStaggeredH N e ψ =
      (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) -
        ∑ s : Role, ∑ r : Role,
          (cochainFluxForward N (fun x => e x s r) s r ψ +
            cochainFluxAdjoint N (fun x => e x s r) s r ψ) ∧
      (pathExprCost firstJetPathExpression).maxWordLength = 2 ∧
      (∀ w : List Unit, firstJetPathExpression ≠ PathExpr.word w) :=
  ⟨flatStaggeredH_additive_expansion N e ψ, firstJetPathExpression_maxLength,
    firstJetPathExpression_not_single_word⟩

theorem firstJet_retains_rawNyquist :
    (∀ x : ArchiveRolePhaseGroup 0,
      centeredCoframeMatrix 0 periodTwoNyquistCoframe x = 0) ∧
      (∀ (t : ℝ) (x : ArchiveRolePhaseGroup 0),
        solderMetricMatrix 0 (t • periodTwoNyquistCoframe) x = roleLorentzMetric) ∧
      flatStaggeredH 0 periodTwoNyquistCoframe periodTwoOneFormProbe
        (0, singletonFockState A) = 2 :=
  centeredNyquist_nonzero_H_oneForm

theorem firstJet_retains_periodThree_corner
    (e : ArchiveRolePhaseGroup 1 → ℝ) (s r : Role) (hsr : s ≠ r)
    (ψ : ArchiveCochain 1) (x : ArchiveRolePhaseGroup 1) (S : ArchiveFockState) :
    cochainFluxForward 1 e s r ψ (x, S) =
      e x * (cochainCarEnd 1 s r ψ (roleTranslatePlus 1 s x, S) +
        cochainCarEnd 1 s r ψ
          (roleTranslateMinus 1 r (roleTranslatePlus 1 s x), S)) / 2 ∧
      roleTranslateMinus 1 r (roleTranslatePlus 1 s x) ≠ x ∧
      roleTranslateMinus 1 r (roleTranslatePlus 1 s x) ≠
        roleTranslatePlus 1 s x :=
  periodThree_gradedH_corner_distance_two e s r hsr ψ x S

theorem firstJet_retains_degree (N k : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (flatStaggeredH N e ψ) :=
  flatStaggeredH_preserves_degree N k e ψ hψ

theorem firstJet_retains_parity (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    flatStaggeredH N e (parityCochain N ψ) =
      parityCochain N (flatStaggeredH N e ψ) :=
  flatStaggeredH_preserves_parity N e ψ

theorem firstJet_distinctRole_corner (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (hsr : s ≠ r) (ψ : ArchiveCochain N)
    (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    cochainFluxForward N e s r ψ (x, S) =
      e x * (cochainCarEnd N s r ψ (roleTranslatePlus N s x, S) +
        cochainCarEnd N s r ψ
          (roleTranslateMinus N r (roleTranslatePlus N s x), S)) / 2 ∧
      roleTranslateMinus N r (roleTranslatePlus N s x) ≠ x ∧
      roleTranslateMinus N r (roleTranslatePlus N s x) ≠
        roleTranslatePlus N s x :=
  gradedH_requires_corner_distance_two N e s r hsr ψ x S

end D0.Geometry
