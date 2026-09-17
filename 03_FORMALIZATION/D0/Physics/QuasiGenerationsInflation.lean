import D0.Dynamics.ToralAutomorphism

namespace D0.Physics

/-!
D0-QUASI-002 generation owner.

Generations are represented as three inflation classes of one local defect
kind.  The arithmetic owner is the already closed time trace layer
`trace (T^2) = 3`.
-/

inductive D0GenerationCarrier where
  | gen0
  | gen1
  | gen2
deriving DecidableEq, Fintype, Repr

inductive LocalPhasonDefect where
  | terminal
deriving DecidableEq, Fintype, Repr

def generationInflate : D0GenerationCarrier -> D0GenerationCarrier
  | D0GenerationCarrier.gen0 => D0GenerationCarrier.gen1
  | D0GenerationCarrier.gen1 => D0GenerationCarrier.gen2
  | D0GenerationCarrier.gen2 => D0GenerationCarrier.gen2

def generationDefectType (_g : D0GenerationCarrier) : LocalPhasonDefect :=
  LocalPhasonDefect.terminal

def generationSeed : D0GenerationCarrier :=
  D0GenerationCarrier.gen0

theorem generation_carrier_is_three_inflation_classes :
    Fintype.card D0GenerationCarrier = 3 := by
  decide

theorem generation_trace_layer_eq_three :
    Matrix.trace (D0.Dynamics.T ^ 2) = 3 := by
  exact D0.Dynamics.trace_T2

theorem generation_inflation_orbit_three_classes :
    generationSeed = D0GenerationCarrier.gen0 /\
      generationInflate generationSeed = D0GenerationCarrier.gen1 /\
      generationInflate (generationInflate generationSeed) =
        D0GenerationCarrier.gen2 := by
  constructor
  · rfl
  · constructor <;> rfl

theorem generation_inflation_transports_same_defect_type
    (g : D0GenerationCarrier) :
    generationDefectType (generationInflate g) =
      generationDefectType g := by
  cases g <;> rfl

theorem quasi_generation_inflation_orbit :
    Fintype.card D0GenerationCarrier = 3 /\
      Matrix.trace (D0.Dynamics.T ^ 2) = 3 /\
      (forall g : D0GenerationCarrier,
        generationDefectType (generationInflate g) =
          generationDefectType g) := by
  exact
    ⟨generation_carrier_is_three_inflation_classes,
      generation_trace_layer_eq_three,
      generation_inflation_transports_same_defect_type⟩

end D0.Physics
