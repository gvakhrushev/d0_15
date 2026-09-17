import D0.Claims.Q8DedekindMinimality
import D0.Core.BornQuadraticOrigin
import D0.UnifiedFiniteCore.Q8Terminal
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
# Finite order memory, faithful carriers and a reference-arm readout

Scope: the EXISTING Q8 table, not a proof that M1 forces this table. A scalar
multiplicative encoding loses order; a rational four-coordinate carrier retains
group elements. Its commuting quarter-turn permits a two-complex-coordinate
reading, but does not force complex quantum theory. The full group algebra needs
more than this spin block: the regular carrier below retains every coefficient.

The detector uses the existing calibrated quadratic-response interface and an
explicit coherent reference. The physical availability of the controlled path,
reference preparation and comparison operation is an apparatus bridge.
-/

namespace D0.Representation.OrderMemoryReadout

open Matrix
open D0.Claims (Q8 tableOf)

abbrev M4 := Matrix (Fin 4) (Fin 4) ℚ
abbrev V4 := Fin 4 → ℚ
abbrev M8 := Matrix (Fin 8) (Fin 8) ℚ

/-! No scalar encoding into ANY commutative monoid retains ij versus ji. -/

theorem scalar_loses_order {C : Type*} [CommMonoid C]
    (f : Fin 8 → C) (hm : ∀ a b, f (Q8.mul a b) = f a * f b) :
    f 6 = f 7 := by
  have h1 := hm 2 4
  have h2 := hm 4 2
  change f 6 = f 2 * f 4 at h1
  change f 7 = f 4 * f 2 at h2
  rw [h1, h2, mul_comm]

theorem scalar_not_faithful {C : Type*} [CommMonoid C]
    (f : Fin 8 → C) (hm : ∀ a b, f (Q8.mul a b) = f a * f b) :
    ¬ Function.Injective f := by
  intro hi
  have h := hi (scalar_loses_order f hm)
  exact (by decide : (6 : Fin 8) ≠ 7) h

theorem scalar_kills_central_sign {C : Type*} [CommGroup C]
    (f : Fin 8 → C) (hm : ∀ a b, f (Q8.mul a b) = f a * f b) :
    f 1 = f 0 := by
  have h := hm 1 6
  have he := hm 0 6
  change f 7 = f 1 * f 6 at h
  change f 6 = f 0 * f 6 at he
  apply mul_right_cancel (b := f 6)
  rw [← h, ← he, scalar_loses_order f hm]

/-! Rational quaternion left multiplication, ordered (1,-1,i,-i,j,-j,k,-k). -/

def left (a b c d : ℚ) : M4 :=
  !![a,-b,-c,-d; b,a,-d,c; c,d,a,-b; d,-c,b,a]

def spin : Fin 8 → M4 :=
  ![left 1 0 0 0, left (-1) 0 0 0,
    left 0 1 0 0, left 0 (-1) 0 0,
    left 0 0 1 0, left 0 0 (-1) 0,
    left 0 0 0 1, left 0 0 0 (-1)]

theorem spin_multiplicative : ∀ a b, spin (Q8.mul a b) = spin a * spin b := by
  native_decide

theorem spin_faithful : Function.Injective spin := by native_decide

theorem spin_identity : spin 0 = 1 := by native_decide
theorem spin_central_sign : spin 1 = -1 := by native_decide
theorem spin_orthogonal : ∀ g, (spin g).transpose * spin g = 1 := by native_decide
theorem spin_reversal : ∀ g, spin (Q8.inv g) = (spin g).transpose := by native_decide

/-- Right multiplication by i, commuting with all left actions. In coordinates
`z1 = x0 + i*x1`, `z2 = x2 - i*x3`, this is scalar multiplication by i. -/
def complexTurn : M4 := !![0,-1,0,0; 1,0,0,0; 0,0,0,1; 0,0,-1,0]

theorem complexTurn_square : complexTurn * complexTurn = -1 := by native_decide
theorem complexTurn_commutes : ∀ g, complexTurn * spin g = spin g * complexTurn := by
  native_decide

/-- Distinct orders give opposite operators, not the same scalar phase character. -/
theorem order_sign : spin 2 * spin 4 = -(spin 4 * spin 2) := by native_decide

/-- The closed comparison word i j i^-1 j^-1 is the central minus sign. -/
def orderLoop : M4 := spin 2 * spin 4 * spin (Q8.inv 2) * spin (Q8.inv 4)

theorem orderLoop_eq : orderLoop = -1 := by native_decide

/-! Faithfulness for group elements is weaker than for algebraic sums. -/

theorem spin_sum_collision : spin 0 + spin 1 = 0 := by native_decide

/-- Left regular action on the eight named history classes. -/
def regular (g : Fin 8) : M8 := fun a b => if a = Q8.mul g b then 1 else 0

theorem regular_multiplicative : ∀ a b, regular (Q8.mul a b) = regular a * regular b := by
  native_decide

theorem regular_reversal : ∀ g, regular (Q8.inv g) = (regular g).transpose := by
  native_decide

def memorySum (c : Fin 8 → ℚ) : M8 := ∑ g, c g • regular g

theorem regular_identity_column (g a : Fin 8) :
    regular g a 0 = if a = g then 1 else 0 := by
  have hr : ∀ g : Fin 8, Q8.mul g 0 = g := by decide
  simp [regular, hr]

/-- The identity column recovers ALL coefficients of the memory-class sum. -/
theorem memorySum_recovers (c : Fin 8 → ℚ) (a : Fin 8) : memorySum c a 0 = c a := by
  simp [memorySum, Matrix.sum_apply, regular_identity_column]

theorem memorySum_faithful : Function.Injective memorySum := by
  intro c d h
  funext a
  have hc := congrArg (fun m : M8 => m a 0) h
  simpa only [memorySum_recovers] using hc

/-- Concrete map from the regular carrier to quaternion coordinates. -/
def toSpin : Matrix (Fin 4) (Fin 8) ℚ :=
  !![1,-1,0,0,0,0,0,0; 0,0,1,-1,0,0,0,0;
     0,0,0,0,1,-1,0,0; 0,0,0,0,0,0,1,-1]

def orderSector : M8 := (1 / 2 : ℚ) • (1 - regular 1)

theorem toSpin_intertwines : ∀ g, toSpin * regular g = spin g * toSpin := by
  native_decide

theorem toSpin_onto : toSpin * toSpin.transpose = (2 : ℚ) • (1 : M4) := by
  native_decide

theorem toSpin_retains_order_sector :
    toSpin.transpose * toSpin = (2 : ℚ) • orderSector := by native_decide

theorem orderSector_projector : orderSector * orderSector = orderSector := by native_decide

/-- The older terminal owner uses (1,i,j,k,-1,-i,-j,-k), not our interleaved order. -/
def terminalOrder : Fin 8 → Fin 8 := ![0,2,4,6,1,3,5,7]

theorem orderSector_is_existing_E4 :
    orderSector.submatrix terminalOrder terminalOrder =
      D0.UnifiedFiniteCore.Q8Terminal.E4 := by native_decide

/-! Reference comparison: rational coordinates, with explicit normalization.
For input arms (v,w), outputs are ((v+w)/2,(v-w)/2). The total output
response equals HALF the raw input norm; these are homogeneous amplitudes,
not a claim that this scaled matrix is Euclidean-orthogonal.
-/

def response (v : V4) : ℚ := ∑ a, v a * v a
def plusArm (v w : V4) : V4 := fun a => (v a + w a) / 2
def minusArm (v w : V4) : V4 := fun a => (v a - w a) / 2

theorem response_nonnegative (v : V4) : 0 ≤ response v := by
  exact Finset.sum_nonneg (fun a _ => mul_self_nonneg (v a))

theorem comparison_conservation (v w : V4) :
    response (plusArm v w) + response (minusArm v w) = (response v + response w) / 2 := by
  simp only [response, plusArm, minusArm, Fin.sum_univ_succ]
  ring

theorem isolated_sign_invisible (v : V4) : response (-v) = response v := by
  simp [response]

theorem reference_separates_sign (v : V4) :
    plusArm v v = v ∧ minusArm v v = 0 ∧
    plusArm v (-v) = 0 ∧ minusArm v (-v) = v := by
  constructor
  · funext a; simp [plusArm]
  constructor
  · funext a; simp [minusArm]
  constructor
  · funext a; simp [plusArm]
  · funext a; simp [minusArm]

def plusProbability (v w : V4) : ℚ :=
  response (plusArm v w) / (response (plusArm v w) + response (minusArm v w))

theorem reference_probability_witness (v : V4) (hv : 0 < response v) :
    plusProbability v v = 1 ∧ plusProbability v (-v) = 0 := by
  rcases reference_separates_sign v with ⟨h1, h2, h3, h4⟩
  have hz : response 0 = 0 := by simp [response]
  simp [plusProbability, h1, h2, h3, h4, hz, ne_of_gt hv]

theorem orderLoop_readout (v : V4) (hv : 0 < response v) :
    plusProbability v ((1 : M4).mulVec v) = 1 ∧
    plusProbability v (orderLoop.mulVec v) = 0 := by
  simpa [orderLoop_eq, Matrix.neg_mulVec] using reference_probability_witness v hv

/-- No free response law is added: each of the two quadrature channels uses
the existing quarter-turn invariant, unit-calibrated quadratic interface. -/
def channel (v : V4) (a : Fin 2) : D0.PhaseAmplitude :=
  if a = 0 then ⟨v 0, v 1⟩ else ⟨v 2, -v 3⟩

theorem response_from_born_owner (Q : D0.UnitPhaseQuadraticResponse) (v : V4) :
    (∑ a : Fin 2, D0.phaseQuadraticEval Q.response (channel v a)) = response v := by
  simp only [D0.unit_phase_blind_quadratic_response_is_norm_sq Q]
  simp [Fin.sum_univ_succ, channel, D0.amplitudeNormSq, response, add_assoc]

/-- Concrete instance of the existing two-outcome normalization owner. -/
def comparisonResponse (v w : V4) (h : 0 < response v + response w) :
    D0.TwoChannelPositiveResponse where
  r0 := response (plusArm v w)
  r1 := response (minusArm v w)
  nonnegative0 := response_nonnegative _
  nonnegative1 := response_nonnegative _
  total_positive := by rw [comparison_conservation]; exact half_pos h

theorem comparison_born_weight (v w : V4) (h : 0 < response v + response w) :
    D0.responseBornWeight0 (comparisonResponse v w h) = plusProbability v w := rfl

theorem comparison_readout_unique (v w : V4) (h : 0 < response v + response w)
    (q : D0.TwoChannelReadout (comparisonResponse v w h)) :
    q.p0 = plusProbability v w :=
  (D0.finite_born_two_channel_readout_unique _ q).1

end D0.Representation.OrderMemoryReadout
