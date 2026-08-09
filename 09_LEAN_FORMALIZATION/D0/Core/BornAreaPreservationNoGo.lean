import D0.Core.BornQuadraticResponse

/-!
# D0-BORN-AREA-PRESERVATION-INSUFFICIENT-NOGO-001 — area preservation does NOT force `x²+y²`

The prose of BOOK_01 §01.6.1b closes the Gleason 2D loophole by saying that a phase-blind response
"must preserve symplectic area, which uniquely forces the quadratic form `x²+y²`". **That stated
implication is false**, and this module proves it false with an explicit second object.

Area preservation is `det = 1` on the acting map. The quarter-turn `J(x,y) = (-y,x)` has `det J = 1`
— but so does the shear `S(x,y) = (x+y, y)`, and `S` does **not** preserve `x²+y²`:
`amplitudeNormSq (S (1,1)) = 2² + 1² = 5 ≠ 2 = amplitudeNormSq (1,1)`.

So `det = 1` is strictly weaker than what the argument needs. What actually does the work — and what
the Lean owner `D0.Core.BornQuadraticResponse` has always used — is invariance under the **specific
order-4 rotation** `J`, i.e. phase blindness, not area preservation. The two are not
interchangeable: `J` generates a finite cyclic group and pins the form; the area-preserving group
`SL(2,ℚ)` is far larger and pins nothing on its own (a form invariant under all of `SL(2,ℚ)` in this
setting must be trivial, since the shear alone already fails).

Consequence for the claim ledger: the Gleason-2D closure stands, but it stands on
`QuarterTurnInvariant`, and any text attributing it to symplectic-area preservation is overstating
the premise. `D0-SYMPLECTIC-GLEASON-001` must cite phase blindness, never area preservation, as the
load-bearing hypothesis.

This module is the **negative control** the argument lacked: it is exactly the object whose absence
made "area preservation forces the form" look admissible. Per the closure contract, a uniqueness
claim is only as strong as the exhibited failure of its weaker neighbours.
-/

namespace D0

/-- The shear `S(x,y) = (x+y, y)` — an area-preserving map (`det = 1`) that is not a rotation. -/
def phaseShear (z : PhaseAmplitude) : PhaseAmplitude where
  re := z.re + z.im
  im := z.im

/-- Both maps are area preserving: `det J = 1` and `det S = 1`, in exact rational arithmetic. -/
theorem quarter_turn_and_shear_both_area_preserving :
    (!![(0 : ℚ), -1; 1, 0]).det = 1 ∧ (!![(1 : ℚ), 1; 0, 1]).det = 1 := by
  constructor <;> simp [Matrix.det_fin_two]

/-- The quarter-turn preserves the squared norm — the premise the Born argument actually uses. -/
theorem quarter_turn_preserves_norm (z : PhaseAmplitude) :
    amplitudeNormSq (phaseQuarterTurn z) = amplitudeNormSq z := by
  simp [amplitudeNormSq, phaseQuarterTurn]
  ring

/-- **The negative control.** The shear is area preserving yet does NOT preserve `x²+y²`:
at `z = (1,1)` the norm jumps from `2` to `5`. -/
theorem shear_does_not_preserve_norm :
    amplitudeNormSq (phaseShear { re := 1, im := 1 }) ≠ amplitudeNormSq { re := 1, im := 1 } := by
  norm_num [amplitudeNormSq, phaseShear]

/-- The squared-norm response, as a `PhaseQuadraticResponse`. -/
def normSqResponse : PhaseQuadraticResponse where
  xx := 1
  xy := 0
  yy := 1

/-- `x²+y²` is quarter-turn invariant (so the positive side of the uniqueness is non-vacuous). -/
theorem normSqResponse_quarter_turn_invariant : QuarterTurnInvariant normSqResponse := by
  intro z
  simp [phaseQuadraticEval, normSqResponse, phaseQuarterTurn]
  ring

/-- A second, genuinely different quadratic form that is **also** preserved by an area-preserving
map — witnessing that "area preserving" cannot single out `x²+y²`. The shear fixes `y²`. -/
def shearInvariantResponse : PhaseQuadraticResponse where
  xx := 0
  xy := 0
  yy := 1

theorem shear_fixes_a_different_form (z : PhaseAmplitude) :
    phaseQuadraticEval shearInvariantResponse (phaseShear z)
      = phaseQuadraticEval shearInvariantResponse z := by
  simp [phaseQuadraticEval, shearInvariantResponse, phaseShear]

/-- **D0-BORN-AREA-PRESERVATION-INSUFFICIENT-NOGO-001.** Area preservation (`det = 1`) is strictly
weaker than the premise the Born-quadratic uniqueness needs: the shear is area preserving, fails to
preserve `x²+y²`, and preserves a *different* quadratic form instead. The uniqueness therefore rests
on quarter-turn (phase-blindness) invariance, which `x²+y²` does satisfy. -/
theorem area_preservation_insufficient :
    ((!![(1 : ℚ), 1; 0, 1]).det = 1) ∧
    (amplitudeNormSq (phaseShear { re := 1, im := 1 }) ≠ amplitudeNormSq { re := 1, im := 1 }) ∧
    (∀ z, phaseQuadraticEval shearInvariantResponse (phaseShear z)
        = phaseQuadraticEval shearInvariantResponse z) ∧
    QuarterTurnInvariant normSqResponse :=
  ⟨(quarter_turn_and_shear_both_area_preserving).2, shear_does_not_preserve_norm,
    shear_fixes_a_different_form, normSqResponse_quarter_turn_invariant⟩

end D0
