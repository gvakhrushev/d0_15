import Mathlib.Tactic
import D0.Representation.CompatibleInvolutionClassification
import D0.Synthesis.IntrinsicDegreeFibreFrame
import D0.Synthesis.RepresentationAndCirculationCanonicity

/-!
# Terminal-orientation operator transported onto the intrinsic generation frame

The previous canonicity theorem proved that every bijection between the three owned
terminal Fourier sectors and the three generation lines preserves the sign multiset
(+,-,+), hence preserves the neutral-current readout.

This module upgrades that signature-level statement to an actual operator on the
graph-derived degree-fibre frame.  For every transport permutation σ we assign the
owned terminal orientation sign to the corresponding intrinsic fibre projector and
obtain a concrete rational 3x3 grading.

For every σ the resulting operator:
* is exactly the signed sum of the graph-derived projectors fibre24/fibre22/fibre20;
* commutes with the intrinsic degree operator;
* squares to the identity;
* is neither +I nor -I;
* therefore has nc = 8.

Thus the choice of sector-to-fibre bijection is not a remaining operator ambiguity for
this observable.  The honest remaining boundary is provenance: why the terminal Fourier
sector algebra is the physical grading source for the generation observable algebra.
-/

namespace D0.Representation.OrientationOperatorTransport

open Matrix
open D0.Synthesis.IntrinsicDegreeFibreFrame
open D0.Synthesis.RepresentationAndCirculationCanonicity
open D0.Representation.CompatibleInvolutionClassification

abbrev M3 := Matrix (Fin 3) (Fin 3) ℚ
abbrev OrientationTransport := Equiv.Perm (Fin 3)

/-- Rational sign pulled from the literal owned terminal orientation sector. -/
def transportedSign (σ : OrientationTransport) (g : Fin 3) : ℚ :=
  if transportedSectorPositive σ g = true then 1 else -1

/-- The three graph-derived rank-one fibre projectors. -/
def intrinsicProjector : Fin 3 → M3
  | 0 => fibre24
  | 1 => fibre22
  | 2 => fibre20

/-- Actual grading operator obtained by transporting the terminal sign to each
intrinsic degree fibre. -/
def transportedGrading (σ : OrientationTransport) : M3 :=
  (transportedSign σ 0) • fibre24 +
  (transportedSign σ 1) • fibre22 +
  (transportedSign σ 2) • fibre20

/-- The operator is diagonal in the intrinsic degree-fibre basis, with exactly the
transported terminal signs on its diagonal. -/
theorem transportedGrading_closed_form (σ : OrientationTransport) :
    transportedGrading σ = Matrix.diagonal (transportedSign σ) := by
  unfold transportedGrading
  rw [fibre24_closed_form, fibre22_closed_form, fibre20_closed_form]
  ext i j
  fin_cases i <;> fin_cases j <;>
    by_cases h0 : transportedSectorPositive σ 0 = true <;>
    by_cases h1 : transportedSectorPositive σ 1 = true <;>
    by_cases h2 : transportedSectorPositive σ 2 = true <;>
    simp [transportedSign, h0, h1, h2]

private lemma transportedSign_sq (σ : OrientationTransport) (g : Fin 3) :
    transportedSign σ g * transportedSign σ g = 1 := by
  unfold transportedSign
  split <;> norm_num

/-- Every transported operator is a valid typed involution. -/
theorem transportedGrading_compatible (σ : OrientationTransport) :
    CompatibleInvolution (transportedGrading σ) := by
  rw [transportedGrading_closed_form]
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [D0.Representation.TypedRepresentationFunctor.degreeOp,
        Matrix.mul_apply, Fin.sum_univ_three] <;> ring
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_three, transportedSign_sq]

private lemma transportedSign_eq_one_iff (σ : OrientationTransport) (g : Fin 3) :
    transportedSign σ g = 1 ↔ transportedSectorPositive σ g = true := by
  cases h : transportedSectorPositive σ g <;>
    simp [transportedSign, h] <;> norm_num

private lemma transportedSign_eq_neg_one_iff (σ : OrientationTransport) (g : Fin 3) :
    transportedSign σ g = -1 ↔ transportedSectorPositive σ g = false := by
  cases h : transportedSectorPositive σ g <;>
    simp [transportedSign, h] <;> norm_num

/-- Every transported operator is genuinely non-scalar. -/
theorem transportedGrading_nonscalar (σ : OrientationTransport) :
    NonScalar (transportedGrading σ) := by
  have hsig := transported_signature_invariant σ
  have hpos : transportedPositiveCount σ = 2 := by
    exact congrArg Prod.fst hsig
  constructor
  · intro hI
    have hall : ∀ g : Fin 3, transportedSectorPositive σ g = true := by
      intro g
      apply (transportedSign_eq_one_iff σ g).mp
      have hentry := congrArg (fun M : M3 => M g g) hI
      rw [transportedGrading_closed_form] at hentry
      simpa using hentry
    have hfilter :
        (Finset.univ.filter (fun g : Fin 3 => transportedSectorPositive σ g = true)) =
          Finset.univ := by
      apply Finset.filter_eq_self.mpr
      intro g _
      exact hall g
    unfold transportedPositiveCount at hpos
    rw [hfilter] at hpos
    norm_num at hpos
  · intro hI
    have hall : ∀ g : Fin 3, transportedSectorPositive σ g = false := by
      intro g
      apply (transportedSign_eq_neg_one_iff σ g).mp
      have hentry := congrArg (fun M : M3 => M g g) hI
      rw [transportedGrading_closed_form] at hentry
      simpa using hentry
    have hfilter :
        (Finset.univ.filter (fun g : Fin 3 => transportedSectorPositive σ g = true)) =
          ∅ := by
      apply Finset.filter_eq_empty_iff.mpr
      intro g _
      have := hall g
      simp [this]
    unfold transportedPositiveCount at hpos
    rw [hfilter] at hpos
    norm_num at hpos

/-- Consequently every actual transported grading gives neutral-current readout 8. -/
theorem transportedGrading_nc_eight (σ : OrientationTransport) :
    ncReadout (transportedGrading σ) = 8 := by
  exact nonscalar_compatible_involution_nc
    (transportedGrading σ)
    (transportedGrading_compatible σ)
    (transportedGrading_nonscalar σ)

/-- The operator-level transport family has no observable ambiguity: every completion
is a compatible non-scalar grading and every completion returns 8. -/
theorem orientation_operator_transport_owner :
    (∀ σ : OrientationTransport,
      CompatibleInvolution (transportedGrading σ)) ∧
    (∀ σ : OrientationTransport,
      NonScalar (transportedGrading σ)) ∧
    (∀ σ : OrientationTransport,
      ncReadout (transportedGrading σ) = 8) := by
  exact ⟨transportedGrading_compatible,
    transportedGrading_nonscalar,
    transportedGrading_nc_eight⟩

end D0.Representation.OrientationOperatorTransport
