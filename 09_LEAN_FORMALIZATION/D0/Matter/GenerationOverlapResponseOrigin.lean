import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import D0.Matter.GenerationSelectorOrigin

namespace D0.Matter

/-- A finite generation basis is a labelling of the three generation states. -/
structure FiniteGenerationBasis where
  vector : GenCarrier -> GenCarrier

/-- A generation selector is a finite integer operator on the generation chain. -/
structure GenerationSelector where
  selector : GenCarrier -> GenCarrier -> Int

/-- Origin object for a pair of up/down generation selectors. -/
structure BasisSelectorOrigin where
  up : GenerationSelector
  down : GenerationSelector
  selectors_noncommute : SelectorsDoNotCommute up.selector down.selector

/--
Phase-blind quadratic overlap response.  The amplitude may be supplied by a
unitary overlap computation; this finite layer records the Born-style square.
-/
noncomputable def generationOverlapResponse
    (amplitude : Matrix GenCarrier GenCarrier Complex) :
    Matrix GenCarrier GenCarrier Real :=
  fun i j => Complex.normSq (amplitude i j)

/-- A response matrix is a genuine column permutation witness only via a permutation. -/
def IsPermutationWitness (M : Matrix GenCarrier GenCarrier Real) : Prop :=
  exists sigma : Equiv.Perm GenCarrier,
    forall i j, M i j = if j = sigma i then 1 else 0

/-- Multi-support row: one row has two distinct positive overlap channels. -/
def HasMultiSupportRow (M : Matrix GenCarrier GenCarrier Real) : Prop :=
  exists i j1 j2, j1 != j2 /\ 0 < M i j1 /\ 0 < M i j2

/-- Finite unitary-overlap condition for the amplitude matrix. -/
def IsUnitaryOverlapAmplitude
    (amplitude : Matrix GenCarrier GenCarrier Complex) : Prop :=
  (forall i j,
    Finset.univ.sum
      (fun k : GenCarrier => star (amplitude k i) * amplitude k j) =
        if i = j then 1 else 0) /\
  (forall i j,
    Finset.univ.sum
      (fun k : GenCarrier => amplitude i k * star (amplitude j k)) =
        if i = j then 1 else 0)

/--
Unistochastic overlap interface: the response comes from squared amplitudes and
is doubly stochastic.  Concrete amplitudes are certified outside Lean for now.
-/
structure IsUnistochasticOverlap (M : Matrix GenCarrier GenCarrier Real) where
  amplitude : Matrix GenCarrier GenCarrier Complex
  amplitude_unitary :
    IsUnitaryOverlapAmplitude amplitude
  response_eq :
    M = generationOverlapResponse amplitude
  row_sum :
    forall i, Finset.univ.sum (fun j : GenCarrier => M i j) = 1
  col_sum :
    forall j, Finset.univ.sum (fun i : GenCarrier => M i j) = 1
  nonnegative :
    forall i j, 0 <= M i j

/--
The generation-overlap origin is attached to the D0 ordinal/adjacency selectors,
not to an arbitrary fixture matrix.
-/
def d0GenerationSelectorOrigin : BasisSelectorOrigin where
  up := { selector := generationOrdinalSelector }
  down := { selector := generationDownSelector }
  selectors_noncommute := generation_selectors_do_not_commute

/-- D0-origin bridge: the concrete generation selectors force noncommutation. -/
theorem d0_generation_selectors_force_nonpermutation_overlap :
    SelectorsDoNotCommute
      generationOrdinalSelector
      generationDownSelector := by
  exact generation_selectors_do_not_commute

/--
Torus-origin bridge: radial shell hopping and shell phase/radius drift supply the
noncommuting selector source used by the generation-overlap layer.
-/
theorem torus_shell_noncommutativity_forces_nonpermutation_overlap_source
    (T : D0.Geometry.TorusParameter) :
    HasNonCommutingGenerationSelectors
      D0.Geometry.radialAdjacency
      (D0.Geometry.phaseDrift T) := by
  exact torus_geometry_forces_generation_selector_noncommute T

/--
Closure package for the algebraic overlap-origin layer.  It records the corrected
permutation notion and the D0-origin selector obstruction without claiming
physical CKM entries.
-/
structure GenerationOverlapResponseOriginClosure where
  origin : BasisSelectorOrigin
  origin_is_d0 :
    origin = d0GenerationSelectorOrigin
  permutation_is_equiv_perm :
    forall M : Matrix GenCarrier GenCarrier Real,
      IsPermutationWitness M <->
        exists sigma : Equiv.Perm GenCarrier,
          forall i j, M i j = if j = sigma i then 1 else 0
  selector_obstruction :
    SelectorsDoNotCommute generationOrdinalSelector generationDownSelector
  torus_selector_obstruction :
    forall T : D0.Geometry.TorusParameter,
      HasNonCommutingGenerationSelectors
        D0.Geometry.radialAdjacency
        (D0.Geometry.phaseDrift T)

/-- Concrete algebraic generation-overlap origin closure. -/
def generation_overlap_response_origin_closure :
    GenerationOverlapResponseOriginClosure := by
  refine
    { origin := d0GenerationSelectorOrigin
      origin_is_d0 := rfl
      permutation_is_equiv_perm := ?_
      selector_obstruction :=
        d0_generation_selectors_force_nonpermutation_overlap
      torus_selector_obstruction :=
        torus_shell_noncommutativity_forces_nonpermutation_overlap_source }
  intro M
  rfl

end D0.Matter
