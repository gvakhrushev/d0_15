import Mathlib.Tactic
import D0.Synthesis.SceneNormalizedQuotientDescent
import D0.Representation.TypedRepresentationFunctor
import D0.Representation.TypedRepresentationFunctorNoGo
import D0.UnifiedFiniteCore.Q8Terminal

/-!
# Intrinsic degree-fibre generation frame

This module removes the remaining *provenance* gap behind the formerly displayed
`diag(24,22,20)` generation operator.

Starting from the literal `33 × 33` scene degree operator, restrict after lifting the
three intrinsic degree fibres.  The resulting operator is proved to be exactly both
the already-owned quotient degree matrix and
`TypedRepresentationFunctor.degreeOp`.  Its three coordinate lines are then recovered
without choosing eigenvectors: they are the three Lagrange spectral projectors,
polynomials in that induced graph operator.

The conclusion has two deliberately explicit boundaries.

* The `Q₈` terminal owner really proves ranks `(1,4,3)`, and those ranks agree with the
  downstream rank tags in the declared order.  But the current corpus contains no map
  from the 33 scene vertices (or their degree fibres) to the `Q₈` regular carrier.
  Therefore the cross-carrier pairing remains a typed correspondence, not a theorem
  of the graph alone.  We exhibit two different rank decorations related by a
  permutation of the same intrinsic frame.
* Both residual grading signatures commute with the intrinsic degree operator and all
  three fibre projectors.  Hence graph reconstruction does not remove the existing
  `(p,q)` / KO-signature bit.

Thus the graph canonically fixes the *unordered* degree-fibre frame (and the distinct
degree values intrinsically label its three summands).  The displayed descending order
`24,22,20` is a coordinate convention, physical generation names are not derived, and
the residual signature no-go survives unchanged.
-/

namespace D0.Synthesis.IntrinsicDegreeFibreFrame

open Matrix

abbrev Vertex33 := Fin 33
abbrev Fibre3 := Fin 3

open D0.Synthesis.SceneNormalizedQuotientDescent

/-! ## Literal-scene provenance of the typed degree operator -/

/-- Restrict the literal 33-dimensional degree operator after lifting a vector which
is constant on each intrinsic degree fibre. -/
def intrinsicDegreeOp : Matrix Fibre3 Fibre3 ℚ :=
  representativeRestriction * fullDegree * D0.Claims.Cind31

/-- The restriction is the unique degree operator induced by the literal scene graph. -/
theorem intrinsicDegreeOp_eq_DWq :
    intrinsicDegreeOp = DWq := by
  unfold intrinsicDegreeOp
  calc
    representativeRestriction * fullDegree * D0.Claims.Cind31 =
        representativeRestriction *
          (fullDegree * D0.Claims.Cind31) := by
      rw [Matrix.mul_assoc]
    _ = representativeRestriction * (D0.Claims.Cind31 * DWq) := by
      rw [fullDegree_indicator_intertwining]
    _ = (representativeRestriction * D0.Claims.Cind31) * DWq := by
      rw [Matrix.mul_assoc]
    _ = DWq := by
      rw [representativeRestriction_indicator, Matrix.one_mul]

/-- **Closed provenance gap.**  The formerly hand-displayed typed degree operator is
exactly the operator induced by the literal `33 × 33` scene graph. -/
theorem intrinsicDegreeOp_eq_typedDegreeOp :
    intrinsicDegreeOp =
      D0.Representation.TypedRepresentationFunctor.degreeOp := by
  rw [intrinsicDegreeOp_eq_DWq]
  native_decide

/-- Any operator commuting with the graph-induced degree operator is diagonal in the
intrinsic degree-fibre frame. -/
theorem intrinsic_degree_commutant_diagonal
    (X : Matrix Fibre3 Fibre3 ℚ)
    (h : X * intrinsicDegreeOp = intrinsicDegreeOp * X) :
    ∀ i j, i ≠ j → X i j = 0 := by
  rw [intrinsicDegreeOp_eq_typedDegreeOp] at h
  exact
    D0.Representation.TypedRepresentationFunctor.degree_commutant_diagonal X h

/-! ## Basis-free recovery of the three fibre lines -/

/-- Spectral projector onto the degree-24 fibre, as a polynomial in the intrinsic
degree operator. -/
def fibre24 : Matrix Fibre3 Fibre3 ℚ :=
  (1 / 8 : ℚ) •
    ((intrinsicDegreeOp - (22 : ℚ) • 1) *
      (intrinsicDegreeOp - (20 : ℚ) • 1))

/-- Spectral projector onto the degree-22 fibre. -/
def fibre22 : Matrix Fibre3 Fibre3 ℚ :=
  (-1 / 4 : ℚ) •
    ((intrinsicDegreeOp - (24 : ℚ) • 1) *
      (intrinsicDegreeOp - (20 : ℚ) • 1))

/-- Spectral projector onto the degree-20 fibre. -/
def fibre20 : Matrix Fibre3 Fibre3 ℚ :=
  (1 / 8 : ℚ) •
    ((intrinsicDegreeOp - (24 : ℚ) • 1) *
      (intrinsicDegreeOp - (22 : ℚ) • 1))

theorem fibre24_closed_form :
    fibre24 = !![1, 0, 0; 0, 0, 0; 0, 0, 0] := by
  rw [fibre24, intrinsicDegreeOp_eq_typedDegreeOp]
  native_decide

theorem fibre22_closed_form :
    fibre22 = !![0, 0, 0; 0, 1, 0; 0, 0, 0] := by
  rw [fibre22, intrinsicDegreeOp_eq_typedDegreeOp]
  native_decide

theorem fibre20_closed_form :
    fibre20 = !![0, 0, 0; 0, 0, 0; 0, 0, 1] := by
  rw [fibre20, intrinsicDegreeOp_eq_typedDegreeOp]
  native_decide

/-- The graph-derived Lagrange projectors are a complete orthogonal decomposition. -/
theorem intrinsic_fibre_projectors :
    fibre24 * fibre24 = fibre24 ∧
    fibre22 * fibre22 = fibre22 ∧
    fibre20 * fibre20 = fibre20 ∧
    fibre24 + fibre22 + fibre20 = (1 : Matrix Fibre3 Fibre3 ℚ) ∧
    fibre24 * fibre22 = 0 ∧
    fibre24 * fibre20 = 0 ∧
    fibre22 * fibre20 = 0 := by
  rw [fibre24_closed_form, fibre22_closed_form, fibre20_closed_form]
  native_decide

/-- The original operator is reconstructed from its intrinsic polynomial projectors. -/
theorem intrinsicDegreeOp_spectral_reconstruction :
    intrinsicDegreeOp =
      (24 : ℚ) • fibre24 + (22 : ℚ) • fibre22 + (20 : ℚ) • fibre20 := by
  rw [intrinsicDegreeOp_eq_typedDegreeOp, fibre24_closed_form,
    fibre22_closed_form, fibre20_closed_form]
  native_decide

/-! ## What the Q8 owner does and does not fix -/

/-- The downstream rank tags are not merely numerology: in their declared order they
are exactly the traces of the three literal `Q₈` Fourier idempotents. -/
theorem q8_terminal_ranks_own_typed_tags :
    D0.UnifiedFiniteCore.Q8Terminal.E0.trace =
        D0.Representation.TypedRepresentationFunctor.q8Ranks 0 ∧
    D0.UnifiedFiniteCore.Q8Terminal.E4.trace =
        D0.Representation.TypedRepresentationFunctor.q8Ranks 1 ∧
    D0.UnifiedFiniteCore.Q8Terminal.E3.trace =
        D0.Representation.TypedRepresentationFunctor.q8Ranks 2 := by
  simpa [D0.Representation.TypedRepresentationFunctor.q8Ranks] using
    D0.UnifiedFiniteCore.Q8Terminal.branch_orders

/-- Swap the first two intrinsic degree fibres. -/
def swap01 : Fibre3 → Fibre3
  | 0 => 1
  | 1 => 0
  | 2 => 2

/-- A second Q8-rank decoration of the same intrinsic three-line frame. -/
def swappedQ8Ranks : Fibre3 → ℕ :=
  fun z => D0.Representation.TypedRepresentationFunctor.q8Ranks (swap01 z)

/-- **Exact cross-owner obstruction.**  The Q8 rank multiset and the graph-derived
three-line frame do not by themselves choose a pairing: the original and swapped
decorations are distinct, and both still use the same three pairwise-distinct ranks.
The fixed correspondence in `Q8Terminal` is therefore additional typed input unless a
future cross-carrier map is supplied. -/
theorem q8_pairing_not_fixed_by_unpaired_frame :
    D0.Representation.TypedRepresentationFunctor.q8Ranks ≠ swappedQ8Ranks ∧
    (D0.Representation.TypedRepresentationFunctor.q8Ranks 0,
        D0.Representation.TypedRepresentationFunctor.q8Ranks 1,
        D0.Representation.TypedRepresentationFunctor.q8Ranks 2) = (1, 4, 3) ∧
    (swappedQ8Ranks 0, swappedQ8Ranks 1, swappedQ8Ranks 2) = (4, 1, 3) ∧
    swappedQ8Ranks 0 ≠ swappedQ8Ranks 1 ∧
    swappedQ8Ranks 0 ≠ swappedQ8Ranks 2 ∧
    swappedQ8Ranks 1 ≠ swappedQ8Ranks 2 := by
  native_decide

/-! ## The residual signature survives the intrinsic frame -/

/-- The all-positive grading representative. -/
def grading30 : Matrix Fibre3 Fibre3 ℚ :=
  !![1, 0, 0; 0, 1, 0; 0, 0, 1]

/-- A `(2,1)` grading representative. -/
def grading21 : Matrix Fibre3 Fibre3 ℚ :=
  !![1, 0, 0; 0, 1, 0; 0, 0, -1]

/-- Both inequivalent signature representatives commute with everything recovered
from the literal degree operator. -/
theorem intrinsic_frame_is_signature_blind :
    grading30 ≠ grading21 ∧
    grading30 * intrinsicDegreeOp = intrinsicDegreeOp * grading30 ∧
    grading21 * intrinsicDegreeOp = intrinsicDegreeOp * grading21 ∧
    (∀ E ∈ ({fibre24, fibre22, fibre20} : Set (Matrix Fibre3 Fibre3 ℚ)),
      grading30 * E = E * grading30 ∧ grading21 * E = E * grading21) := by
  rw [intrinsicDegreeOp_eq_typedDegreeOp, fibre24_closed_form,
    fibre22_closed_form, fibre20_closed_form]
  constructor
  · native_decide
  constructor
  · native_decide
  constructor
  · native_decide
  intro E hE
  rcases hE with (rfl | rfl | rfl) <;> constructor <;> native_decide

/-- **Final boundary.**  The graph-derived degree frame is exact, while the old
two-completion no-go remains exact as well. -/
theorem intrinsic_frame_with_residual_signature :
    intrinsicDegreeOp =
        D0.Representation.TypedRepresentationFunctor.degreeOp ∧
    fibre24 + fibre22 + fibre20 = (1 : Matrix Fibre3 Fibre3 ℚ) ∧
    D0.Representation.TypedRepresentationFunctorNoGo.Phi1.nc = 12 ∧
    D0.Representation.TypedRepresentationFunctorNoGo.Phi2.nc = 8 ∧
    D0.Representation.TypedRepresentationFunctorNoGo.Phi1.nc ≠
      D0.Representation.TypedRepresentationFunctorNoGo.Phi2.nc :=
  ⟨intrinsicDegreeOp_eq_typedDegreeOp,
    intrinsic_fibre_projectors.2.2.2.1,
    D0.Representation.TypedRepresentationFunctorNoGo.typed_representation_functor_nogo.1,
    D0.Representation.TypedRepresentationFunctorNoGo.typed_representation_functor_nogo.2.1,
    D0.Representation.TypedRepresentationFunctorNoGo.typed_representation_functor_nogo.2.2⟩

end D0.Synthesis.IntrinsicDegreeFibreFrame
