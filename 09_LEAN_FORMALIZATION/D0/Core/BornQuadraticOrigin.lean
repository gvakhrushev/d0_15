import D0.Core.BornQuadraticResponse
import Mathlib.Tactic

namespace D0

/-- Finite phase quadrature carrier used by the Born quadratic-origin layer. -/
abbrev PhaseQuadrature := PhaseAmplitude

/-- Internal quarter-turn phase action. -/
def J (v : PhaseQuadrature) : PhaseQuadrature :=
  phaseQuarterTurn v

/-- Addition of finite phase quadratures. -/
def phaseQuadratureAdd (v w : PhaseQuadrature) : PhaseQuadrature where
  re := v.re + w.re
  im := v.im + w.im

/-- Subtraction of finite phase quadratures. -/
def phaseQuadratureSub (v w : PhaseQuadrature) : PhaseQuadrature where
  re := v.re - w.re
  im := v.im - w.im

/--
Parallelogram identity for the quadratic response induced by coefficients
`xx, xy, yy`.  This is the finite algebraic origin of the quadratic-response
interface used by `BornQuadraticResponse`.
-/
def QuadraticParallelogramLaw (Q : PhaseQuadraticResponse) : Prop :=
  forall v w : PhaseQuadrature,
    phaseQuadraticEval Q (phaseQuadratureAdd v w) +
        phaseQuadraticEval Q (phaseQuadratureSub v w) =
      2 * phaseQuadraticEval Q v + 2 * phaseQuadraticEval Q w

/-- A coefficient quadratic response satisfies the finite parallelogram law. -/
theorem parallelogram_response_is_quadratic_form
    (Q : PhaseQuadraticResponse) :
    QuadraticParallelogramLaw Q := by
  intro v w
  simp [phaseQuadratureAdd, phaseQuadratureSub, phaseQuadraticEval]
  ring

/--
Quarter-turn phase blindness plus unit calibration forces the norm-square
response `x^2 + y^2`.
-/
theorem quarter_turn_quadratic_forces_norm_square
    (Q : UnitPhaseQuadraticResponse) :
    forall v : PhaseQuadrature,
      phaseQuadraticEval Q.response v = amplitudeNormSq v :=
  unit_phase_blind_quadratic_response_is_norm_sq Q

/-- Constructive closure package for the Born quadratic-origin layer. -/
structure BornQuadraticOriginClosure where
  parallelogram_owner :
    forall Q : PhaseQuadraticResponse, QuadraticParallelogramLaw Q
  phase_blind_unit_owner :
    forall Q : UnitPhaseQuadraticResponse,
      forall v : PhaseQuadrature,
        phaseQuadraticEval Q.response v = amplitudeNormSq v
  finite_amplitude_born_owner :
    forall {Out State : Type} [Fintype Out] [Fintype State]
      (A : FiniteAmplitudeEffectFrame Out State)
      (q : FiniteAmplitudeBornReadout A),
      forall i, q.probability i = finiteAmplitudeBornWeight A i

/-- Concrete Born quadratic-origin closure object. -/
def born_quadratic_origin_closed : BornQuadraticOriginClosure where
  parallelogram_owner := parallelogram_response_is_quadratic_form
  phase_blind_unit_owner := quarter_turn_quadratic_forces_norm_square
  finite_amplitude_born_owner := by
    intro Out State hOut hState A q i
    exact finite_amplitude_born_readout_unique A q i

end D0
