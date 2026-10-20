import D0.Representation.OrderMemoryReadout
import D0.Representation.GoldenOrderInterferometer
import D0.Foundation.Omega8Center
import D0.Foundation.EmpiricalTheoryFactorization
import D0.Foundation.EndogenousActionQuantum
import D0.Representation.FiniteProtocolClock
import Mathlib.Data.Matrix.Block

/-!
# Forward-only control for the finite order-memory protocol

This module reduces the implementation interface; it does not declare every
orthogonal matrix physically available. The tested UNCONTROLLED palette consists
of arbitrary real arm rotations and identical linear maps on the two arms.
Every word in this palette commutes with the arm quarter-turn. A relative sign
does not, so no finite word in that palette synthesizes it.

One additional LOCAL action, i on the signal arm, suffices for the relative sign,
inverse splitter and the comparison word with global j. All controls below are
the previous Q8 matrices. Only forward actions are needed.
-/

namespace D0.Representation.OrderMemoryControl

open Matrix
open D0.Representation.OrderMemoryReadout (spin)

abbrev Axis := Fin 4 ⊕ Fin 4
abbrev M4R := Matrix (Fin 4) (Fin 4) ℝ
abbrev M8R := Matrix Axis Axis ℝ
abbrev M8Q := Matrix Axis Axis ℚ

def mixer (a p : ℝ) : M8R :=
  fromBlocks (a • (1 : M4R)) ((-p) • (1 : M4R))
    (p • (1 : M4R)) (a • (1 : M4R))

def common (A : M4R) : M8R := fromBlocks A 0 0 A
def armTurn : M8R := fromBlocks 0 (-1 : M4R) 1 0
def relativeSign : M8R := fromBlocks (1 : M4R) 0 0 (-1)

theorem mixer_commutes_armTurn (a p : ℝ) :
    mixer a p * armTurn = armTurn * mixer a p := by
  simp [mixer, armTurn, fromBlocks_multiply]

theorem common_commutes_armTurn (A : M4R) :
    common A * armTurn = armTurn * common A := by
  simp [common, armTurn, fromBlocks_multiply]

/-- A generous comparison class; not a definition of all M1-admissible physics. -/
inductive CommonGenerated : M8R → Prop where
  | identity : CommonGenerated 1
  | mix (a p : ℝ) : CommonGenerated (mixer a p)
  | same (A : M4R) : CommonGenerated (common A)
  | compose {A B} : CommonGenerated A → CommonGenerated B → CommonGenerated (A * B)

theorem common_word_commutes {U : M8R} (h : CommonGenerated U) :
    U * armTurn = armTurn * U := by
  induction h with
  | identity => simp
  | mix a p => exact mixer_commutes_armTurn a p
  | same A => exact common_commutes_armTurn A
  | compose hA hB ihA ihB =>
      calc _ = _ := mul_assoc _ _ _
           _ = _ := congrArg (fun X => _ * X) ihB
           _ = _ := (mul_assoc _ _ _).symm
           _ = _ := congrArg (fun X => X * _) ihA
           _ = _ := mul_assoc _ _ _

theorem relativeSign_not_commuting :
    relativeSign * armTurn ≠ armTurn * relativeSign := by
  intro h
  have hl : relativeSign * armTurn = fromBlocks (0 : M4R) (-1) (-1) 0 := by
    simp [relativeSign, armTurn, fromBlocks_multiply]
  have hr : armTurn * relativeSign = fromBlocks (0 : M4R) 1 1 0 := by
    simp [relativeSign, armTurn, fromBlocks_multiply]
  rw [hl, hr] at h
  have he := congrArg (fun M : M8R => M (Sum.inl 0) (Sum.inr 0)) h
  norm_num [fromBlocks] at he

theorem no_relativeSign_from_common : ¬ CommonGenerated relativeSign := by
  intro h
  exact relativeSign_not_commuting (common_word_commutes h)

theorem relativeSign_square : relativeSign * relativeSign = 1 := by
  simp [relativeSign, fromBlocks_multiply, fromBlocks_one]

/-- The reverse mixer requires no inverse primitive once a relative sign exists. -/
theorem reverse_mixer_from_forward (a p : ℝ) :
    relativeSign * mixer a p * relativeSign = (mixer a p).transpose := by
  simp [relativeSign, mixer, fromBlocks_multiply, fromBlocks_transpose]

def localIQ : M8Q := fromBlocks 1 0 0 (spin 2)
def commonJQ : M8Q := fromBlocks (spin 4) 0 0 (spin 4)
def relativeSignQ : M8Q := fromBlocks 1 0 0 (-1)

theorem local_i_squared : localIQ * localIQ = relativeSignQ := by native_decide
theorem local_i_fourth : localIQ ^ 4 = 1 := by native_decide
theorem common_j_fourth : commonJQ ^ 4 = 1 := by native_decide
theorem local_i_orthogonal : localIQ.transpose * localIQ = 1 := by native_decide
theorem common_j_orthogonal : commonJQ.transpose * commonJQ = 1 := by native_decide

/-- Chronological execution: local i, global j, three local i, three global j.
Matrices act on column states, hence the reversed multiplication order here. -/
theorem forward_order_word :
    commonJQ ^ 3 * localIQ ^ 3 * commonJQ * localIQ = relativeSignQ := by
  native_decide

/-- Same cost and same generator multiplicities, with commuting runs grouped. -/
theorem forward_identity_word : commonJQ ^ 4 * localIQ ^ 4 = 1 := by native_decide

noncomputable def liftQ (M : M8Q) : M8R := M.map (Rat.castHom ℝ)

theorem liftQ_mul (A B : M8Q) : liftQ (A * B) = liftQ A * liftQ B :=
  Matrix.map_mul

theorem liftQ_relativeSign : liftQ relativeSignQ = relativeSign := by
  ext i j
  cases i <;> cases j <;>
    simp [liftQ, relativeSignQ, relativeSign, fromBlocks, Matrix.one_apply]
  all_goals split_ifs <;> norm_num

theorem local_i_squared_real : liftQ localIQ * liftQ localIQ = relativeSign := by
  rw [← liftQ_mul, local_i_squared, liftQ_relativeSign]

/-- This controller genuinely adds something absent from the common palette. -/
theorem local_i_not_from_common : ¬ CommonGenerated (liftQ localIQ) := by
  intro h
  have hs := CommonGenerated.compose h h
  rw [local_i_squared_real] at hs
  exact no_relativeSign_from_common hs

/-! ## EXACT native-Q8 central controller compiled from EXISTING forward gates

No extra primitive gate is needed to PRODUCE the relative sign:
the already-owned local i and common j words give either identity or
relativeSignQ with precisely four occurrences of EACH source gate.
This is a TYPED actuator-capacity bridge from the already-owned
Q8 central qONE/qNEG labels. The if branch is a mathematical
PROGRAM SELECTION dependent on a retained Q8 label; literal physical
Book/G0 still must transport that label into a clocked controlled
programme and pay its actual work. Do not infer such physical
selection or a Spin-sensitive Dirac detector from these identities.
-/

/-- Both original forward sequences use four local-i actions and
four common-j actions, differing ONLY in chronological order. -/
def originalQ8OrderWord : List Bool :=
  [true,false,true,true,true,false,false,false]

def originalQ8IdentityWord : List Bool :=
  [true,true,true,true,false,false,false,false]

theorem originalQ8ForwardWordsSamePrimitiveInventory :
    originalQ8OrderWord.length = 8 ∧
    originalQ8IdentityWord.length = 8 ∧
    originalQ8OrderWord.count true = 4 ∧
    originalQ8IdentityWord.count true = 4 ∧
    originalQ8OrderWord.count false = 4 ∧
    originalQ8IdentityWord.count false = 4 := by
  decide

/-- Use the original two finite Q8 forward words; NO new allowed
operator or continuously variable active matrix is installed. -/
def originalQ8CenterForwardProgram (q : D0.Foundation.UQuat) : M8Q :=
  if q = D0.Foundation.qNEG
  then commonJQ ^ 3 * localIQ ^ 3 * commonJQ * localIQ
  else commonJQ ^ 4 * localIQ ^ 4

theorem originalQ8CenterForwardProgram_plus :
    originalQ8CenterForwardProgram D0.Foundation.qONE = 1 := by
  simp [originalQ8CenterForwardProgram,
    D0.Foundation.qONE, D0.Foundation.qNEG, forward_identity_word]

theorem originalQ8CenterForwardProgram_minus :
    originalQ8CenterForwardProgram D0.Foundation.qNEG =
      relativeSignQ := by
  simp [originalQ8CenterForwardProgram, forward_order_word]

/-- The very same actual original i,j Q8 commutator is realized
by an EXISTING chronological eight-gate program as the native
relative sign operator, not merely an unimplemented abstract s=-1. -/
theorem originalQ8CommutatorForwardProgram :
    originalQ8CenterForwardProgram
      (D0.Foundation.uqmul
        (D0.Foundation.uqmul (0,1,0,0) (0,0,1,0))
        (D0.Foundation.uqmul
          (D0.Foundation.uqinv (0,1,0,0))
          (D0.Foundation.uqinv (0,0,1,0)))) =
      relativeSignQ := by
  rw [D0.Foundation.commutator_ij_eq_neg]
  exact originalQ8CenterForwardProgram_minus


/-- M1/MDL core lesson on the LITERAL ORIGINAL native Q8 gate vocabulary:
TWO chronological programs have the SAME four-i/four-j generator
inventory but DIFFERENT signed Golden order-port probability laws.
Hence primitive gate MULTISET/word-length compression is UNSOUND
as a complete predictor of future registered comparisons; actual
order-memory is a future-test invariant. This is not a claim the
full Book work cost is only the primitive word length. -/
theorem originalQ8SameGateInventoryButDifferentMeasuredHistory :
    let p := D0.primitiveRoot
    let a := Real.sqrt p
    originalQ8OrderWord.count true = originalQ8IdentityWord.count true ∧
    originalQ8OrderWord.count false = originalQ8IdentityWord.count false ∧
    (D0.Representation.GoldenOrderInterferometer.output a p
      (D0.Representation.GoldenOrderInterferometer.q8_center_sign
        D0.Foundation.qONE) 1)^2 ≠
    (D0.Representation.GoldenOrderInterferometer.output a p
      (D0.Representation.GoldenOrderInterferometer.q8_center_sign
        D0.Foundation.qNEG) 1)^2 := by
  dsimp
  have hc := originalQ8ForwardWordsSamePrimitiveInventory
  have hz := D0.Representation.GoldenOrderInterferometer.q8_center_order_golden_detectable
  refine ⟨?_, ?_, ?_⟩
  · simp [originalQ8OrderWord, originalQ8IdentityWord]
  · simp [originalQ8OrderWord, originalQ8IdentityWord]
  · intro h
    have dark := hz.1
    have bright := hz.2.2
    rw [dark] at h
    exact (ne_of_gt bright) h.symm


/-! ## Future-MDL: a single ORIGINAL Q8 chronological bit is irreducible

The two eight-letter native Q8 words have IDENTICAL action multiset
and length.  The existing Golden order port gives distinct exact
Born response probabilities. Therefore no encoder that merely stores
the unordered generator counts can predict the complete future
comparison. At least TWO future memory classes (one binary bit) are
necessary; retaining the chronological choice is sufficient.

The original existing finite reversible basis \`register\` explicitly
makes the stored program label visible at one later comparison. This
is a typed endogenous future-context witness on the previously-owned
mathematical action repertoire. Its ACTUAL full G0/Book real-control
permission and Cost−Info selection remain open.
-/

/-- Encode the two already-owned native Q8 center programmes, NOT a
new physical primitive or a third independent M1 checking line. -/
def nativeQ8ProgramClass (order : Bool) : D0.Foundation.UQuat :=
  if order then D0.Foundation.qNEG else D0.Foundation.qONE

/-- The existing literal Golden controlled-port probability for the
original grouped vs ordered Q8 eight-gate word. -/
def nativeQ8ProgramPort (order : Bool) : ℝ :=
  let p := D0.primitiveRoot
  let a := Real.sqrt p
  (D0.Representation.GoldenOrderInterferometer.output a p
    (D0.Representation.GoldenOrderInterferometer.q8_center_sign
      (nativeQ8ProgramClass order)) 1)^2

theorem nativeQ8ProgramPort_grouped :
    nativeQ8ProgramPort false = 0 := by
  simpa [nativeQ8ProgramPort, nativeQ8ProgramClass] using
    D0.Representation.GoldenOrderInterferometer.q8_center_order_golden_detectable.1

theorem nativeQ8ProgramPort_ordered :
    nativeQ8ProgramPort true = 4*D0.primitiveRoot^3 := by
  simpa [nativeQ8ProgramPort, nativeQ8ProgramClass] using
    D0.Representation.GoldenOrderInterferometer.q8_center_order_golden_detectable.2.1

theorem nativeQ8ProgramPort_grouped_ne_ordered :
    nativeQ8ProgramPort false ≠ nativeQ8ProgramPort true := by
  rw [nativeQ8ProgramPort_grouped, nativeQ8ProgramPort_ordered]
  exact ne_of_lt
    D0.Representation.GoldenOrderInterferometer.q8_center_order_golden_detectable.2.2

/-- A genuinely sufficient predictor MUST distinguish the two source
programmes, even though their original Q8 gate inventories coincide. -/
theorem nativeQ8ProgramPort_injective :
    Function.Injective nativeQ8ProgramPort := by
  intro x y h
  cases x <;> cases y
  · rfl
  · exact False.elim (nativeQ8ProgramPort_grouped_ne_ordered h)
  · exact False.elim (nativeQ8ProgramPort_grouped_ne_ordered h.symm)
  · rfl

/-- Minimal exact outcome-predictive order MEMORY requires at least
two possible states. This does NOT charge any arbitrary work/clock
price and does NOT posit a new physical readout primitive. -/
theorem nativeQ8ProgramFutureMemoryAtLeastTwo {Code : Type}
    [Fintype Code] (encode : Bool → Code) (decode : Code → ℝ)
    (correct : ∀ b, decode (encode b) = nativeQ8ProgramPort b) :
    2 ≤ Fintype.card Code := by
  have hinj : Function.Injective encode := by
    intro x y he
    apply nativeQ8ProgramPort_injective
    calc
      nativeQ8ProgramPort x = decode (encode x) := (correct x).symm
      _ = decode (encode y) := by rw [he]
      _ = nativeQ8ProgramPort y := correct y
  simpa using (Fintype.card_le_of_injective encode hinj)

/-- Original endogenous ActionProtocol quantization charges at least
ONE action unit for changing between the two distinguishable actual
programme states, IF both states and the change are admitted as the
physical ActionProtocol carrier. This does NOT select that programme
or force its preparation in G0. -/
theorem nativeQ8ProgramDistinctionHasUnitCost
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : D0.Foundation.EndogenousActionQuantum.ActionProtocol P)
    (source : Bool → P.State) (record : P.State → ℝ)
    (correct : ∀ b, record (source b) = nativeQ8ProgramPort b) :
    1 ≤ A.action (source false) (source true) := by
  have hne : source false ≠ source true := by
    intro eq
    apply nativeQ8ProgramPort_grouped_ne_ordered
    calc
      nativeQ8ProgramPort false = record (source false) := (correct false).symm
      _ = record (source true) := by rw [eq]
      _ = nativeQ8ProgramPort true := correct true
  exact A.action_nontrivial _ _ hne

/-- Existing internal reversible record-writing CNOT, with no new
step primitive: a Bool source programme and an initially blank record.
Actual Golden port outcomes above are the future output. -/
def nativeQ8RecordedProgramFuture :
    D0.Foundation.EmpiricalTheoryFactorization.FutureExecution where
  State := Bool × Bool
  Action := Bool
  Test := Unit
  Outcome := ℝ
  step := fun execute s =>
    if execute then D0.Representation.FiniteProtocolClock.register s else s
  observe := fun s _ => nativeQ8ProgramPort s.2

/-- Without the native reversible registration, both original
programme states have exactly the same CURRENT blank output. -/
theorem nativeQ8RecordedProgram_same_now :
    nativeQ8RecordedProgramFuture.observe (false,false) () =
    nativeQ8RecordedProgramFuture.observe (true,false) () := rfl

/-- After ONE existing reversible record operation, the original
Q8 chronology choices have distinct native Golden positive output
laws. Thus present-outcome MDL is unsound but ALL-FUTURE MDL
provably retains their source-order bit. -/
theorem nativeQ8RecordedProgram_separated_by_future :
    nativeQ8RecordedProgramFuture.profile (false,false) ≠
    nativeQ8RecordedProgramFuture.profile (true,false) := by
  intro h
  have hh : nativeQ8ProgramPort false = nativeQ8ProgramPort true := by
    simpa [nativeQ8RecordedProgramFuture,
      D0.Foundation.EmpiricalTheoryFactorization.FutureExecution.profile,
      D0.Foundation.EmpiricalTheoryFactorization.FutureExecution.run,
      D0.Representation.FiniteProtocolClock.register] using
      (congrFun (congrFun h [true]) ())
  exact nativeQ8ProgramPort_grouped_ne_ordered hh


/-! ## Direct word interpreter and exact finite-shot Popperian boundary

The following fold EXECUTES the existing native Q8 forward-only gates
in their original chronological order.  This strengthens merely
writing a matrix expression chosen by the programme label: the
actual gate-word itself produces the relative sign with no extra
continuous action.  A truthful full observation, however, is Born-
probabilistic. One bright event refutes the central +1 sign (whose
bright probability is EXACT zero), but the central -1 sign has
strictly positive all-dark probability for EVERY finite independent
repeat count.  This is a one-sided Popperian falsifier, not a
perfect finite-shot truth oracle. Physical independent reset/replay
and its true full Book clock/work are still unselected in G0.
-/

/-- Run an actual finite chronological list of the two ALREADY OWNED
forward native Q8 gate matrices. -/
def nativeQ8ChronologicalWord (word : List Bool) : M8Q :=
  word.foldl (fun U local =>
    (if local then localIQ else commonJQ) * U) 1

/-- The actual ordered SOURCE LIST itself evaluates to the original
relative central sign, with no free sign matrix used as a gate. -/
theorem nativeQ8OrderedWordEvaluates :
    nativeQ8ChronologicalWord originalQ8OrderWord = relativeSignQ := by
  native_decide

theorem nativeQ8GroupedWordEvaluates :
    nativeQ8ChronologicalWord originalQ8IdentityWord = 1 := by
  native_decide

/-- Zero false bright probability for original +1. -/
theorem nativeQ8PositiveCenterBrightImpossible :
    nativeQ8ProgramPort false = 0 :=
  nativeQ8ProgramPort_grouped

/-- Actual original negative Q8 center still sometimes yields dark:
the exact probability is primitive p^6 > 0. -/
theorem nativeQ8NegativeCenterDarkNonzero :
    0 < D0.primitiveRoot^6 :=
  pow_pos D0.Representation.GoldenOrderInterferometer.primitive_positive _

/-- The complete original two-port Golden law really has a positive
dark remainder under the Q8 -1 commutator sign. -/
theorem nativeQ8NegativeCenterProbabilityComplete :
    nativeQ8ProgramPort true + D0.primitiveRoot^6 = 1 := by
  rw [nativeQ8ProgramPort_ordered]
  have h := D0.Representation.GoldenOrderInterferometer.golden_response_closure
    D0.primitiveRoot D0.primitive_root_satisfies
  linarith

/-- N independent freshly reset repetitions of this SAME original
Golden port experiment: all-dark probability. Independence / ability
to repeat are explicit execution premises, NOT consequences of one
finite coherent 16-stage clock. -/
def nativeQ8IndependentAllDarkProbability (n : ℕ) : ℝ :=
  D0.primitiveRoot^(6*n)

/-- The probability of NEVER witnessing an original Q8 -1 order
signal after n independent trials is the exact p^(6n), positive
for EVERY finite n. Thus finite dark records cannot certify +1 with
logical certainty. -/
theorem nativeQ8IndependentAllDarkFormula (n : ℕ) :
    nativeQ8IndependentAllDarkProbability n =
      (1 - nativeQ8ProgramPort true)^n := by
  unfold nativeQ8IndependentAllDarkProbability
  rw [pow_mul, nativeQ8ProgramPort_ordered]
  congr 1
  have h := D0.Representation.GoldenOrderInterferometer.golden_response_closure
    D0.primitiveRoot D0.primitive_root_satisfies
  linarith

theorem nativeQ8IndependentAllDarkPositive (n : ℕ) :
    0 < nativeQ8IndependentAllDarkProbability n := by
  unfold nativeQ8IndependentAllDarkProbability
  exact pow_pos D0.Representation.GoldenOrderInterferometer.primitive_positive _

/-- All n-times-dark probability under +1 remains exactly 1 if
each individual sample has dark probability 1. This is an algebraic
statement on conditional IID repeated trials, NOT a D0 guaranteed
source of free independent fresh records. -/
theorem nativeQ8PositiveCenterAllDarkCertain (n : ℕ) :
    (1-nativeQ8ProgramPort false)^n = 1 := by
  rw [nativeQ8ProgramPort_grouped]
  simp


end D0.Representation.OrderMemoryControl
