import D0.Geometry.A4DScalarBackgroundWordMixing
import D0.Geometry.A4DStaggeredFirstJetPathExpansion
import D0.Geometry.A4DHorizontalDressingSecondJetFreedom

/-!
# Crossed-path algebra boundary

Bare spatial words are not closed under the vertical scalar action. The owned
first jet belongs to an additive path-expression sector of spatial word length
at most two. Horizontal composition in the explicit quadratic endpoint-dressing
class does not select the second jet.

No fields `pi`, `R`, `alpha`, or `W` are introduced. The crossed constitutive
law stays unconstructed.
-/

namespace D0.Geometry

theorem crossedPathAlgebraBoundary {n : ℕ} [NeZero n] (hn : 4 ≤ n) :
    ¬ oneLetterSector
        (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleShift n -
          scalarCycleShift n * scalarCycleG (scalarSite (0 : Fin n))) ∧
      (pathExprCost wordMixingExpression).maxWordLength = 2 ∧
      (pathExprCost firstJetPathExpression).maxWordLength = 2 ∧
      (∀ w : List Unit, firstJetPathExpression ≠ PathExpr.word w) ∧
      quadraticDressing 1 0 = 1 ∧
      quadraticDressing 2 0 = 1 ∧
      (∀ t, quadraticDressing 1 (-t) = quadraticDressing 1 t) ∧
      (∀ t, quadraticDressing 2 (-t) = quadraticDressing 2 t) ∧
      (quadraticDressing 1 (1 / 2) + quadraticDressing 1 (-(1 / 2)) -
          (2 : ℚ) • quadraticDressing 1 0) ≠
        (quadraticDressing 2 (1 / 2) + quadraticDressing 2 (-(1 / 2)) -
          (2 : ℚ) • quadraticDressing 2 0) ∧
      (∀ t, t = 0 ∨ t = 1 / 3 ∨ t = 1 / 2 →
        (quadraticDressing 1 t * quadraticDressingInv 2 t) *
            (quadraticDressing 2 t * quadraticDressingInv (-1) t) =
          quadraticDressing 1 t * quadraticDressingInv (-1) t) :=
  ⟨delta_wordMixing_not_oneLetter (Nat.le_trans (by decide) hn),
    wordMixingExpression_maxLength,
    firstJetPathExpression_maxLength,
    firstJetPathExpression_not_single_word,
    quadraticDressing_zero 1,
    quadraticDressing_zero 2,
    quadraticDressing_even 1,
    quadraticDressing_even 2,
    quadraticDressing_secondJets_differ,
    checker_quadratic_factors_compose⟩

end D0.Geometry
