import D0.Representation.OrderMemoryReadout
import D0.Representation.GoldenQ8CenterReadout
import D0.Foundation.Omega8Center
import D0.Foundation.FutureExecutionCompleteness
import D0.Foundation.ProspectiveReversalSymmetry
import D0.Representation.FiniteProtocolClock
import Mathlib.Data.Matrix.Block
import Init.Data.Vector.OfFn

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

/-- Concrete finite storage on ALL original eight axis labels. The matrix
fold accumulates data, not function-valued caches which can be re-evaluated
entry by entry. This changes proof evaluation only, not physical primitives. -/
abbrev NativeQ8AxisData (α : Type) := Vector α 4 × Vector α 4

def nativeQ8TabulateAxis {α : Type} (f : Axis → α) : NativeQ8AxisData α :=
  (Vector.ofFn (fun i => f (Sum.inl i)),
   Vector.ofFn (fun i => f (Sum.inr i)))

def nativeQ8ViewAxis {α : Type} (a : NativeQ8AxisData α) : Axis → α
  | .inl i => a.1.get i
  | .inr i => a.2.get i

theorem nativeQ8ViewAxis_tabulate {α : Type} (f : Axis → α) :
    nativeQ8ViewAxis (nativeQ8TabulateAxis f) = f := by
  funext i
  cases i <;> simp [nativeQ8ViewAxis, nativeQ8TabulateAxis, Vector.get, Vector.ofFn]

abbrev NativeQ8MatrixData := NativeQ8AxisData (NativeQ8AxisData ℚ)

def nativeQ8TabulateMatrix (M : M8Q) : NativeQ8MatrixData :=
  nativeQ8TabulateAxis (fun i => nativeQ8TabulateAxis (M i))

def nativeQ8ViewMatrix (D : NativeQ8MatrixData) : M8Q :=
  fun i j => nativeQ8ViewAxis (nativeQ8ViewAxis D i) j

theorem nativeQ8ViewMatrix_tabulate (M : M8Q) :
    nativeQ8ViewMatrix (nativeQ8TabulateMatrix M) = M := by
  funext i j
  simp only [nativeQ8ViewMatrix, nativeQ8TabulateMatrix, nativeQ8ViewAxis_tabulate]

def nativeQ8MatrixStep (I J : M8Q) (U : M8Q) (b : Bool) : M8Q :=
  (if b then I else J) * U

def nativeQ8DataStep (I J : M8Q) (D : NativeQ8MatrixData) (b : Bool) : NativeQ8MatrixData :=
  nativeQ8TabulateMatrix (nativeQ8MatrixStep I J (nativeQ8ViewMatrix D) b)

theorem nativeQ8ViewDataStep (I J : M8Q) (D : NativeQ8MatrixData) (b : Bool) :
    nativeQ8ViewMatrix (nativeQ8DataStep I J D b) = nativeQ8MatrixStep I J (nativeQ8ViewMatrix D) b := by
  exact nativeQ8ViewMatrix_tabulate _

theorem nativeQ8FoldlView (I J : M8Q) (word : List Bool) (D : NativeQ8MatrixData) :
    nativeQ8ViewMatrix (word.foldl (nativeQ8DataStep I J) D) =
      word.foldl (nativeQ8MatrixStep I J) (nativeQ8ViewMatrix D) := by
  induction word generalizing D with
  | nil => rfl
  | cons b word ih =>
      simp only [List.foldl_cons, ih, nativeQ8ViewDataStep]

theorem nativeQ8ScanlView (I J : M8Q) (word : List Bool) (D : NativeQ8MatrixData) :
    (word.scanl (nativeQ8DataStep I J) D).map nativeQ8ViewMatrix =
      word.scanl (nativeQ8MatrixStep I J) (nativeQ8ViewMatrix D) := by
  induction word generalizing D with
  | nil => rfl
  | cons b word ih =>
      simp only [List.scanl_cons, List.map_cons, ih, nativeQ8ViewDataStep]

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
  have h : nativeQ8ViewMatrix
      (([true,false,true,true,true,false,false,false] : List Bool).foldl
        (nativeQ8DataStep localIQ commonJQ) (nativeQ8TabulateMatrix 1)) =
      relativeSignQ := by native_decide
  rw [nativeQ8FoldlView, nativeQ8ViewMatrix_tabulate] at h
  simpa [nativeQ8MatrixStep, pow_succ, mul_assoc] using h

/-- Same cost and same generator multiplicities, with commuting runs grouped. -/
theorem forward_identity_word : commonJQ ^ 4 * localIQ ^ 4 = 1 := by
  rw [common_j_fourth, local_i_fourth, one_mul]

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
noncomputable def nativeQ8ProgramPort (order : Bool) : ℝ :=
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
  exact ne_of_lt (mul_pos (by norm_num)
    (pow_pos D0.Representation.GoldenOrderInterferometer.primitive_positive _))

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
noncomputable def nativeQ8RecordedProgramFuture :
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
  word.foldl (fun U isLocal =>
    (if isLocal then localIQ else commonJQ) * U) 1

/-- Same chronological fold, retaining concrete data between products. -/
def nativeQ8ChronologicalWordEager (word : List Bool) : M8Q :=
  nativeQ8ViewMatrix
    (word.foldl (nativeQ8DataStep localIQ commonJQ) (nativeQ8TabulateMatrix 1))

/-- The compiler may use eager storage only through this proved equality.
Every original word, gate order and endpoint operator is retained exactly. -/
@[csimp] theorem nativeQ8ChronologicalWord_eq_eager :
    nativeQ8ChronologicalWord = nativeQ8ChronologicalWordEager := by
  funext word
  simp only [nativeQ8ChronologicalWord, nativeQ8ChronologicalWordEager,
    nativeQ8FoldlView, nativeQ8ViewMatrix_tabulate]
  rfl

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
noncomputable def nativeQ8IndependentAllDarkProbability (n : ℕ) : ℝ :=
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


/-! ## Existing reversible record makes BOTH programme and register necessary

Even with only ONE native Q8 chronological programme bit, the already
owned reversible \`FiniteProtocolClock.register\` preserves its previous
record input.  On the full four-state (programme,record) carrier the
current Golden port has only TWO possible probabilities, whereas the
profile containing an optional ONE registered future comparison is
faithful on all FOUR states. Thus the minimal retained whole-history
memory is TWO bits, not merely its one visible port bit. This is the
literal-native analogue of the general hiddenBitExecution theorem.
-/

/-- Current and one-future-step original Golden port probabilities
together determine the entire original programme+record pair. -/
theorem nativeQ8RecordedProgram_futureProfile_injective :
    Function.Injective nativeQ8RecordedProgramFuture.profile := by
  intro s t h
  have h0 : nativeQ8ProgramPort s.2 = nativeQ8ProgramPort t.2 := by
    simpa [nativeQ8RecordedProgramFuture,
      D0.Foundation.EmpiricalTheoryFactorization.FutureExecution.profile,
      D0.Foundation.EmpiricalTheoryFactorization.FutureExecution.run] using
      (congrFun (congrFun h []) ())
  have h1 : nativeQ8ProgramPort (Bool.xor s.1 s.2) =
      nativeQ8ProgramPort (Bool.xor t.1 t.2) := by
    simpa [nativeQ8RecordedProgramFuture,
      D0.Foundation.EmpiricalTheoryFactorization.FutureExecution.profile,
      D0.Foundation.EmpiricalTheoryFactorization.FutureExecution.run,
      D0.Representation.FiniteProtocolClock.register] using
      (congrFun (congrFun h [true]) ())
  have e0 := nativeQ8ProgramPort_injective h0
  have e1 := nativeQ8ProgramPort_injective h1
  rcases s with ⟨sp,sr⟩
  rcases t with ⟨tp,tr⟩
  dsimp at e0 e1
  cases sp <;> cases sr <;> cases tp <;> cases tr <;>
    simp_all [Bool.xor]

/-- The ORIGINAL existing Q8 programme bit and reversible retained
record bit cost exactly TWO BITS of future-sufficient state. No third
witness line, new Q8 physics, or free Born truth oracle is assumed. -/
theorem nativeQ8RecordedProgram_futureMemoryAtLeastFour
    {Code : Type} [Fintype Code]
    (encode : nativeQ8RecordedProgramFuture.State → Code)
    (decode : Code → List nativeQ8RecordedProgramFuture.Action →
      nativeQ8RecordedProgramFuture.Test →
        nativeQ8RecordedProgramFuture.Outcome)
    (correct : ∀ s, decode (encode s) =
      nativeQ8RecordedProgramFuture.profile s) :
    4 ≤ Fintype.card Code := by
  have hinj : Function.Injective encode := by
    intro s t he
    apply nativeQ8RecordedProgram_futureProfile_injective
    calc
      nativeQ8RecordedProgramFuture.profile s =
          decode (encode s) := (correct s).symm
      _ = decode (encode t) := by rw [he]
      _ = nativeQ8RecordedProgramFuture.profile t := correct t
  letI : Fintype nativeQ8RecordedProgramFuture.State := by
    change Fintype (Bool × Bool)
    infer_instance
  simpa [nativeQ8RecordedProgramFuture] using
    (Fintype.card_le_of_injective encode hinj)


/-! ## The decisive MDL obstruction: commutative primitive counts lose truth

Both actual eight-gate Q8 programmes have EXACTLY the same scalar
generator inventory (four local i, four common j), hence the same
strict primitive sum if their respective gate costs are label-only
and context independent.  Any putative code depending SOLELY on this
commutative two-count inventory gives the same prediction for both.
The ORIGINAL Golden order port does not. Consequently an EXACT
future-sufficient MDL description must encode an additional ORDER
distinction, even after primitive input costs are fixed canonically.
-/

/-- No scalar predictor of the original Q8 primitive-gate inventory
can reproduce both actual Golden order-response distributions. -/
theorem originalQ8InventoryCannotPredictGolden :
    ¬ ∃ forecast : ℕ → ℕ → ℝ,
      forecast (originalQ8OrderWord.count true)
          (originalQ8OrderWord.count false) = nativeQ8ProgramPort true ∧
      forecast (originalQ8IdentityWord.count true)
          (originalQ8IdentityWord.count false) = nativeQ8ProgramPort false := by
  rintro ⟨forecast,ordered,grouped⟩
  have h1 : (originalQ8OrderWord.count true) = 4 := by decide
  have h2 : (originalQ8OrderWord.count false) = 4 := by decide
  have h3 : (originalQ8IdentityWord.count true) = 4 := by decide
  have h4 : (originalQ8IdentityWord.count false) = 4 := by decide
  rw [h1,h2] at ordered
  rw [h3,h4] at grouped
  exact nativeQ8ProgramPort_grouped_ne_ordered (grouped.symm.trans ordered)



/-! ## MDL HOSTILE TEST: two gates make SAME OUTPUT as eight actual gates

The existing native local_i_squared already implements the relative
sign with TWO localIQ primitives. Thus the eight-gate ordered history
is NOT the shortest gate WORD to implement its final operator. It is
a fixed-inventory SOURCE-HISTORY comparison. An endpoint-only Golden
measurement cannot identify the SOURCE path length/work/provenance:
the 2-gate and 8-gate programmes have the same exact operator on all
eight real coordinates and identical full Born response.

This is the precise extra source rule needed for FULL D0 MDL: compress
away raw history ONLY if all actually admitted FUTURE TESTS including
the previously retained clock/provenance/paid Book price still agree.
No free eight-step physical cost theorem follows merely from the
operator equality; charging each executed nonidentity primitive is
conditional on its genuine admitted state-transition cost.
-/

/-- Minimal primitive executable word for the SAME original relative
sign gate: just two already-owned LOCAL quaternion-i gates. -/
theorem originalQ8TwoLocalForwardGates :
    nativeQ8ChronologicalWord [true,true] = relativeSignQ := by
  native_decide

/-- Exactly the same completed matrix (and hence any endpoint-only
Golden/Born readout) is obtained from a 2-gate and 8-gate original
execution. Their HISTORIES and paid sequence lengths are different. -/
theorem originalQ8TwoForwardGatesEqualEightChronology :
    nativeQ8ChronologicalWord [true,true] =
      nativeQ8ChronologicalWord originalQ8OrderWord := by
  rw [originalQ8TwoLocalForwardGates, nativeQ8OrderedWordEvaluates]

theorem originalQ8IdentityNeedsNoForwardGates :
    nativeQ8ChronologicalWord [] = 1 := rfl

/-- No original word of zero or one primitive forward action can
synthesize the relative sign. Thus 2 is the MINIMAL GATE COUNT
on the native {localIQ,commonJQ} alphabet, whereas 8 is a
chronological provenance-conditioned source history. -/
theorem originalQ8RelativeSignCannotUseLessThanTwoGates
    (w : List Bool) (h : w.length < 2) :
    nativeQ8ChronologicalWord w ≠ relativeSignQ := by
  cases w with
  | nil =>
      native_decide
  | cons b ws =>
      cases ws with
      | nil =>
          cases b <;> native_decide
      | cons b' rest =>
          simp at h

/-- The original chronological 8-gate Book source CANNOT be recovered
from its completed operator alone: two distinct histories have
identical final matrix but different paid step count. This is
a FULL-HISTORY information obstruction even before Q8 Spin source
or Golden control is addressed in physical G0. -/
theorem originalQ8EndpointCannotRecoverPaidHistoryLength :
    ¬ ∃ decoder : M8Q → ℕ,
       decoder (nativeQ8ChronologicalWord [true,true]) = 2 ∧
       decoder (nativeQ8ChronologicalWord originalQ8OrderWord) = 8 := by
  rintro ⟨decoder, htwo, height⟩
  rw [originalQ8TwoForwardGatesEqualEightChronology] at htwo
  omega



/-- The ACTUAL native FiniteProtocolClock records the time spent.
The two-gate and eight-gate programmes have identical final Q8
operator, but their ORIGINAL internal time registers are 2 and 8.
This is already a retained future-readable distinction in the
registered 16-stage protocol, not an invented witness or new gate. -/
theorem originalQ8SameEndpointDifferentNativeClock
    {S : Type} (U : D0.Representation.FiniteProtocolClock.Clock → S ≃ S)
    (s : S) :
    (D0.Representation.FiniteProtocolClock.run U s 2).1 ≠
      (D0.Representation.FiniteProtocolClock.run U s 8).1 := by
  rw [D0.Representation.FiniteProtocolClock.stage_is_internal,
      D0.Representation.FiniteProtocolClock.stage_is_internal]
  change (2 : ZMod 16) ≠ 8
  decide



/-! ## ORIGINAL full-prefix physically priced history — NOT only endpoint unitary

The original ActionProtocol charges transitions between faithfully
represented states. This conditional theorem does not assign prices
to letter NAMES, invent a new Cost functional, or claim the original
M1/G0 actually chooses this representation. If actual native physical
states faithfully distinguish the 8-gate executed-prefix OPERATORS,
then every gate in that 8-gate history changes such a state and the
whole-history executed action costs AT LEAST 8 native units. The
shortest 2-gate representative costs AT LEAST 2 units on its own
actual executed history. These are independent LOWER BOUNDS, NOT a
claim the actual two-gate execution is physically cheaper for every
admissible ActionProtocol.

The two histories have identical final relativeSignQ matrix and
Golden outcome distribution but DIFFER in their full temporal
register (native FiniteProtocolClock stage 2 vs stage 8). Thus
minimization using only the final unitary would be an invalid
replacement when the actual stage/provenance is future-readable.
-/

/-- All actual native Q8 prefix operators along chronological
execution, including the original input identity prefix. -/
def nativeQ8ExecutionPrefixes (word : List Bool) : List M8Q :=
  word.scanl
    (fun U isLocal => (if isLocal then localIQ else commonJQ) * U)
    1

/-- Eager storage for the ENTIRE original prefix list, including identity. -/
def nativeQ8ExecutionPrefixesEager (word : List Bool) : List M8Q :=
  (word.scanl (nativeQ8DataStep localIQ commonJQ) (nativeQ8TabulateMatrix 1)).map
    nativeQ8ViewMatrix

/-- No prefix, comparison, primitive count or finite search case is removed. -/
@[csimp] theorem nativeQ8ExecutionPrefixes_eq_eager :
    nativeQ8ExecutionPrefixes = nativeQ8ExecutionPrefixesEager := by
  funext word
  simp only [nativeQ8ExecutionPrefixes, nativeQ8ExecutionPrefixesEager,
    nativeQ8ScanlView, nativeQ8ViewMatrix_tabulate]
  rfl

/-- The actual successive active changes in a Q8 execution trace. -/
def nativeQ8ExecutionPairs (word : List Bool) : List (M8Q × M8Q) :=
  let prefixes := nativeQ8ExecutionPrefixes word
  prefixes.zip prefixes.tail

/-- Every one of the two short native sign-gate actions changes
the entire existing 8×8 operator prefix. -/
theorem nativeQ8TwoExecutionNoIdle :
    ∀ xy ∈ nativeQ8ExecutionPairs [true,true], xy.1 ≠ xy.2 := by
  native_decide

/-- Every one of the eight original based chronological actions is
nontrivial on the existing complete 8×8 Q8 operator register. -/
theorem nativeQ8EightExecutionNoIdle :
    ∀ xy ∈ nativeQ8ExecutionPairs originalQ8OrderWord,
      xy.1 ≠ xy.2 := by
  native_decide

/-- Price a FULL actual chronological list of state changes with
the ALREADY EXISTING physical ActionProtocol, once the source
state interpretation is supplied. No new cost or weight assigned. -/
def nativeQ8WholeWordPaidCost
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : D0.Foundation.EndogenousActionQuantum.ActionProtocol P)
    (source : M8Q → P.State)
    (word : List Bool) : ℝ :=
  ((nativeQ8ExecutionPairs word).map
    (fun xy => A.action (source xy.1) (source xy.2))).sum

/-- Any genuine ActionProtocol which retains different states at
every actual chronological step pays at least one ORIGINAL quantum
for every actual executed step. No stationarity/canonical price
is supplied by this conditional universal lower bound. -/
theorem nativeQ8WordPaidCostGePrimitiveCount
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : D0.Foundation.EndogenousActionQuantum.ActionProtocol P)
    (source : M8Q → P.State) (word : List Bool)
    (h : ∀ xy ∈ nativeQ8ExecutionPairs word,
       source xy.1 ≠ source xy.2) :
    ((nativeQ8ExecutionPairs word).length : ℝ) ≤
       nativeQ8WholeWordPaidCost A source word := by
  have aux : ∀ xs : List (M8Q × M8Q),
      (∀ xy ∈ xs, source xy.1 ≠ source xy.2) →
      (xs.length : ℝ) ≤
      (xs.map (fun xy => A.action (source xy.1) (source xy.2))).sum := by
    intro xs
    induction xs with
    | nil =>
        intro _
        simp
    | cons xy xs ih =>
        intro hfull
        have hx : source xy.1 ≠ source xy.2 :=
          hfull xy (by simp)
        have ht : ∀ yz ∈ xs, source yz.1 ≠ source yz.2 := by
          intro yz hy
          exact hfull yz (by simp [hy])
        have hsum := ih ht
        have ha := A.action_nontrivial (source xy.1) (source xy.2) hx
        simp only [List.length_cons, Nat.cast_add, Nat.cast_one,
          List.map_cons, List.sum_cons]
        linarith
  exact aux (nativeQ8ExecutionPairs word) h

theorem nativeQ8TwoGateActualWorkAtLeastTwo
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : D0.Foundation.EndogenousActionQuantum.ActionProtocol P)
    (source : M8Q → P.State)
    (hfaithful : Function.Injective source) :
    2 ≤ nativeQ8WholeWordPaidCost A source [true,true] := by
  have hall : ∀ xy ∈ nativeQ8ExecutionPairs [true,true],
      source xy.1 ≠ source xy.2 := by
    intro xy hm
    exact hfaithful.ne (nativeQ8TwoExecutionNoIdle xy hm)
  have hb := nativeQ8WordPaidCostGePrimitiveCount A source
    [true,true] hall
  have hl : (nativeQ8ExecutionPairs [true,true]).length = 2 := by
    native_decide
  simpa [hl] using hb

theorem nativeQ8EightGateActualWorkAtLeastEight
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : D0.Foundation.EndogenousActionQuantum.ActionProtocol P)
    (source : M8Q → P.State)
    (hfaithful : Function.Injective source) :
    8 ≤ nativeQ8WholeWordPaidCost A source originalQ8OrderWord := by
  have hall : ∀ xy ∈ nativeQ8ExecutionPairs originalQ8OrderWord,
      source xy.1 ≠ source xy.2 := by
    intro xy hm
    exact hfaithful.ne (nativeQ8EightExecutionNoIdle xy hm)
  have hb := nativeQ8WordPaidCostGePrimitiveCount A source
    originalQ8OrderWord hall
  have hl : (nativeQ8ExecutionPairs originalQ8OrderWord).length = 8 := by
    native_decide
  simpa [hl] using hb



/-! ## An exact countermodel to endpoint-only Book Cost, even at S_min

The already-defined canonical primitive rule from EndogenousActionQuantum
prices each actual NONIDENTITY state change at exactly one unit.
Apply that existing rule to the concrete Q8 gate-operator prefixes,
retaining each executed step. No extra code price, clock rate or
fitted coupling. The 2- and 8-gate words have the same final operator,
but canonical ACTUAL executed-history costs 2 vs 8.

This establishes that an endpoint-only scalar function of the final
unitary is insufficient to recover even the most economical native
primitive history Cost if the source history/provenance is among the
admitted retained distinctions. Full Book03 Cost−Info, preparation,
observer/clock, failure-work and matter terms remain different objects.
-/

/-- Canonical Cost=1 on every genuinely changed original Q8 operator
prefix, identity Cost=0, in the already-established endogenous
ActionProtocol convention. This is the exact native MINIMAL witness
price, not the complete physical Book03 programme price. -/
def nativeQ8CanonicalExecutedAction (word : List Bool) : ℕ :=
  ((nativeQ8ExecutionPairs word).filter
    (fun xy => xy.1 ≠ xy.2)).length

theorem nativeQ8CanonicalPriceTwoVsEight :
    nativeQ8CanonicalExecutedAction [true,true] = 2 ∧
    nativeQ8CanonicalExecutedAction originalQ8OrderWord = 8 := by
  native_decide

/-- Same full final SO/Q8 operator, different exact canonical original
executed-history primitive price; endpoint-only dynamics cannot
recover both costs even under the simplest D0 minimal rule. -/
theorem nativeQ8CanonicalActionCannotFactorThroughEndpoint :
    ¬ ∃ f : M8Q → ℕ,
        (∀ w : List Bool,
          f (nativeQ8ChronologicalWord w) =
            nativeQ8CanonicalExecutedAction w) := by
  rintro ⟨f, hf⟩
  have ha := hf [true,true]
  have hb := hf originalQ8OrderWord
  rw [originalQ8TwoForwardGatesEqualEightChronology] at ha
  have hcost := nativeQ8CanonicalPriceTwoVsEight
  rw [hcost.1] at ha
  rw [hcost.2] at hb
  omega



/-! ## Unexpected exact common GOLDEN quantum in time-Cost and darkness

For the ACTUAL original canonical primitive action Cost=1 per
successfully changed Q8 prefix, the eight-gate provenance history
costs six more quanta than the two-gate same-endpoint implementation.
Its raw φ-Book cost weight ratio is therefore φ^(-6)=p^6.
The SAME primitive p^6 is the exact DARK conditional Born probability
of the nontrivial Q8 order interferometer. This is an exact algebraic
identity on the existing native primitives, NOT a theorem that the
COMPLETE original Book03 Cost−Info/Info/clock history weight equals
that Bernoulli probability; no cross-carrier physical cost selection
is inserted.
-/

/-- Canonical original executed-prefix Book weight of the exact two-
versus-eight Q8 source: six additional action units, already counted
by nativeQ8CanonicalPriceTwoVsEight. -/
theorem nativeQ8CanonicalCostGapSix :
    nativeQ8CanonicalExecutedAction originalQ8OrderWord -
      nativeQ8CanonicalExecutedAction [true,true] = 6 := by
  native_decide

/-- Identically, the primitive Book weight ratio of these SOURCE
histories at the canonical physical unit quantum is p^6, and
precisely matches the dark port in the ACTUAL original Q8- Golden
sign comparison. All Info/preparation/clock extras remain OPEN. -/
theorem nativeQ8CanonicalCostGapEqualsDarkLogWeight :
    D0.primitiveRoot^8 / D0.primitiveRoot^2 =
      1 - nativeQ8ProgramPort true := by
  have hp0 : D0.primitiveRoot ≠ 0 :=
    ne_of_gt D0.Representation.GoldenOrderInterferometer.primitive_positive
  have hbook : D0.primitiveRoot^8 /
      D0.primitiveRoot^2 = D0.primitiveRoot^6 := by
    field_simp
  have hdark := nativeQ8NegativeCenterProbabilityComplete
  rw [nativeQ8ProgramPort_ordered] at hdark
  rw [hbook, nativeQ8ProgramPort_ordered]
  linarith



/-! ## Same Born histories, different admissible absolute SECOND Book sources

The original primitive gate ActionProtocol admits ANY nonnegative excess
above the endogenous nonidentity floor one. The two otherwise identical
native Q8 terminal operators can be executed by two or eight distinct
physical transitions. For the perfectly admissible source-controlled
primitive Cost C(t)=1+t^2 on EVERY changed source state, the full
chronological additive primitive cost of an executed path is
(# actual transitions)*(1+t²), never just the final matrix cost.

Its centred second finite difference differs by EXACTLY 12*t² between
the two histories, while all endpoint-only positive Golden Born laws
remain identical for EVERY t. Thus a full action's SECOND field source
cannot be reconstructed from the final unitary/detector alone, even
though its instantaneous output and first derivative coincide at t=0.

This constructs a legal PRICE FIBRE counterexample. It does not
prove that physical Book03 selects the field dependence 1+t², and
does not assert the entire H+J+R action equals this primitive sum.
-/

/-- An explicitly admissible primitive nonidentity price family. -/
def nativeQ8LegalPrimitiveCost (t : ℝ) : ℝ := 1 + t^2

theorem nativeQ8LegalPrimitiveCost_floor (t : ℝ) :
    1 ≤ nativeQ8LegalPrimitiveCost t := by
  unfold nativeQ8LegalPrimitiveCost
  nlinarith [sq_nonneg t]

/-- Exact original minimal additive price of the FULL observed
execution at a declared legal primitive cost chart. -/
def nativeQ8LegalWholeHistoryPrice
    (word : List Bool) (t : ℝ) : ℝ :=
  (nativeQ8CanonicalExecutedAction word : ℝ) *
    nativeQ8LegalPrimitiveCost t

/-- Positive admissible field variation changes the absolute Book
history second source even when endpoint matrix and Born effects are
IDENTICAL: the exact centered SECOND jet contrast is 12 t². -/
theorem nativeQ8SameEndBookSecondSourceGap (t : ℝ) :
    ((nativeQ8LegalWholeHistoryPrice originalQ8OrderWord t +
       nativeQ8LegalWholeHistoryPrice originalQ8OrderWord (-t) -
       2 * nativeQ8LegalWholeHistoryPrice originalQ8OrderWord 0) -
      (nativeQ8LegalWholeHistoryPrice [true,true] t +
       nativeQ8LegalWholeHistoryPrice [true,true] (-t) -
       2 * nativeQ8LegalWholeHistoryPrice [true,true] 0)) =
     12 * t^2 := by
  have hh := nativeQ8CanonicalPriceTwoVsEight
  simp [nativeQ8LegalWholeHistoryPrice,
    nativeQ8LegalPrimitiveCost, hh.1, hh.2]
  ring



/-! ## Direct ORIGINAL Q8 finite-order return: a four-tick circle IS NOT idle

This is a concrete witness of the new FOUNDATION theorem
original_roundtrip_forces_paid_history, now using one actual
native Q8 finite-order primitive. Four local-i forward operations
return the exact full two-arm operator to I8, just like the empty
history, but all four intermediate operator-prefix states differ
and the native clock has reached stage FOUR (rather than ZERO).
Canonical per-primitive S_min=1 cost gives FOUR paid units.
This is a strict no-go for identifying time or history work with
net endpoint change. No actual Book/CAR matter law is assumed.
-/

theorem nativeQ8FourLocalGatesReturnIdentity :
    nativeQ8ChronologicalWord [true,true,true,true] = 1 := by
  native_decide

theorem nativeQ8FourLocalGatesNoIdle :
    ∀ xy ∈ nativeQ8ExecutionPairs [true,true,true,true],
      xy.1 ≠ xy.2 := by
  native_decide

theorem nativeQ8FourStepIdentityHasNonzeroPaidHistory :
    nativeQ8CanonicalExecutedAction [true,true,true,true] = 4 ∧
    nativeQ8CanonicalExecutedAction [] = 0 := by
  native_decide

theorem nativeQ8FourStepCircleClockIsNotIdle
    {S : Type} (U : D0.Representation.FiniteProtocolClock.Clock → S ≃ S)
    (s : S) :
    (D0.Representation.FiniteProtocolClock.run U s 4).1 ≠
      (D0.Representation.FiniteProtocolClock.run U s 0).1 := by
  rw [D0.Representation.FiniteProtocolClock.stage_is_internal,
      D0.Representation.FiniteProtocolClock.stage_is_internal]
  change (4 : ZMod 16) ≠ 0
  decide



/-! ## Ex-ante MDL CORRECTION: even the 8-step matched-inventory assay is NOT shortest

The existing 8-step words are mathematically correct source records,
but a THREE-step matched-inventory pair already distinguishes the
chronological central Q8 sign with the SAME original gates:
chronological I,J,I returns the global common J (the two-arm
interference cancels), while J,I,I returns relativeSignQ*commonJQ.
Both use two local-i and one common-j; their original Golden
bright responses differ by 4p^3 in the existing comparator.
No new gate symbol or externally tuned angle is introduced.

This is a proof that the source-test optimization MUST happen BEFORE
execution if D_min is intended as a PHYSICAL GENERATION LAW, not a
retrospective text compressor. It is NOT a proof native G0 actually
selects the shortest test, or that the three-gate assay preserves the
same full Book clock/provenance as the 8-gate original history.
-/

/-- The shorter ACTUAL chronological Q8 control WORDS, using only
the original localIQ and commonJQ primitives. -/
def nativeQ8MinimalReferenceWord : List Bool := [true,false,true]
def nativeQ8MinimalOrderWord : List Bool := [false,true,true]

theorem nativeQ8ThreeWordSamePrimitiveInventory :
    nativeQ8MinimalReferenceWord.length = 3 ∧
    nativeQ8MinimalOrderWord.length = 3 ∧
    nativeQ8MinimalReferenceWord.count true = 2 ∧
    nativeQ8MinimalOrderWord.count true = 2 ∧
    nativeQ8MinimalReferenceWord.count false = 1 ∧
    nativeQ8MinimalOrderWord.count false = 1 := by
  decide

/-- Native chronological I,J,I equals the old global common-j gate:
no relative sign is present at the Golden comparison. -/
theorem nativeQ8ThreeGateIJIEqualsCommonJ :
    nativeQ8ChronologicalWord nativeQ8MinimalReferenceWord =
      commonJQ := by
  native_decide

/-- Native chronological J,I,I differs solely by the ALREADY
OWNED Q8 relativeSignQ central element. -/
theorem nativeQ8ThreeGateJIIEqualsRelativeCommonJ :
    nativeQ8ChronologicalWord nativeQ8MinimalOrderWord =
      relativeSignQ * commonJQ := by
  native_decide

theorem nativeQ8ThreeGateDistinctSourceOperators :
    nativeQ8ChronologicalWord nativeQ8MinimalReferenceWord ≠
      nativeQ8ChronologicalWord nativeQ8MinimalOrderWord := by
  native_decide



/-! ## PROSPECTIVE MDL FOR THE COMPLETE ORIGINAL OPERATOR, NOT ONLY THE PORT

The earlier 3-gate equal-inventory comparison IJI/JII is minimal
for the COARSE native Golden bright-port distinction, but leaves a
COMMON Q8 j-rotation on the entire spin/reference carrier.  If the
full task specifies the EXACT reference identity and the EXACT
relative-sign operator on ALL quaternion coordinates, those three
gates do not solve the same task. Appending the three ALREADY OWNED
common-j forward rotations (j^4=1) gives a SIX-gate matched-inventory
comparison; the former EIGHT-gate one was not prospective-minimal.

This is especially relevant to physical D_min: minimize over
alternatives matching the SAME COMPLETE admitted future observable
contract, not a coarser detector subtask or a history selected earlier.
The exact six-word existence and full matrix identities are Lean;
global <6 minimality is independently exhaustively checked on
all 127 possible original gate words of lengths 0..6, and not
advertised as a separately compiled Lean minimality theorem.
-/

/-- Fixed native positive Q8 source, all operators forward only:
literal chronological IJIJJJ -> entire identity I8. -/
def nativeQ8SixGateFullReferenceWord : List Bool :=
  [true,false,true,false,false,false]

/-- Same actual generator multiset, but JIIJJJ -> entire native
relative sign R8, including the quaternion-reference subsystem. -/
def nativeQ8SixGateFullOrderWord : List Bool :=
  [false,true,true,false,false,false]

theorem nativeQ8SixGateSamePrimitiveInventory :
    nativeQ8SixGateFullReferenceWord.length = 6 ∧
    nativeQ8SixGateFullOrderWord.length = 6 ∧
    nativeQ8SixGateFullReferenceWord.count true = 2 ∧
    nativeQ8SixGateFullOrderWord.count true = 2 ∧
    nativeQ8SixGateFullReferenceWord.count false = 4 ∧
    nativeQ8SixGateFullOrderWord.count false = 4 := by
  decide

theorem nativeQ8SixGateFullMatchedReference :
    nativeQ8ChronologicalWord nativeQ8SixGateFullReferenceWord = 1 := by
  native_decide

theorem nativeQ8SixGateFullMatchedOrder :
    nativeQ8ChronologicalWord nativeQ8SixGateFullOrderWord =
       relativeSignQ := by
  native_decide

/-- The 3-gate assay is NOT a literal exact full-carrier replacement
for the six- or eight-gate identity/sign end-point goal. -/
theorem nativeQ8ThreeGateNotFullyNormalized :
    nativeQ8ChronologicalWord nativeQ8MinimalReferenceWord ≠ 1 ∧
    nativeQ8ChronologicalWord nativeQ8MinimalOrderWord ≠ relativeSignQ := by
  native_decide

/-- Both full-output-precise original six-gate words have the SAME
terminal Q8 operators as the previous eight-gate source words. -/
theorem nativeQ8SixAndEightSameCompleteOutcomes :
    nativeQ8ChronologicalWord nativeQ8SixGateFullReferenceWord =
      nativeQ8ChronologicalWord originalQ8IdentityWord ∧
    nativeQ8ChronologicalWord nativeQ8SixGateFullOrderWord =
      nativeQ8ChronologicalWord originalQ8OrderWord := by
  constructor
  · rw [nativeQ8SixGateFullMatchedReference, nativeQ8GroupedWordEvaluates]
  · rw [nativeQ8SixGateFullMatchedOrder, nativeQ8OrderedWordEvaluates]


/-! ## PROSPECTIVE MINIMAL CLOSED Q8 SCENE TEST — first nontrivial loop is 3 ticks

This is the physically significant contrast to a word-length-only MDL
test. In the original K(9,11,13) scene, every two-edge closed word is
a backtrack (u,v,u), and a correctly inverse-respecting Q8 edge
connection has q_uv*q_vu=1. In contrast a three-zone true ABC loop
can carry nontrivial central qNEG without ANY newly invented group
element. The original Q8 i,j,k edge assignments give i*j*k=-1.
Replacing the final k by the ALSO EXISTING opposite Q8 element -k
gives +1. The original positive Golden-order comparison distinguishes
their central classes with second-port 4p^3 vs zero.

Both are 3-edge MINIMAL closed original scene history programmes
under canonical primitive nonidentity Cost=1, while the original
primitive Cost-floor BY ITSELF does not choose which of the two
gauge-invariant central sheet values is physically selected.
That selection requires full native Info/initial data/allowed history
and future test, not an ex-post replacement or fitted Einstein action.
The Q8 assignment to actual scene transport is an explicitly
declared mathematical candidate; literal paid G0 does not yet
supply an executable scene-edge-to-Q8 active representation.
-/

/-- All eight TRUE original Q8 elements have a trivial chronological
two-step forward+inverse backtrack holonomy. -/
theorem originalQ8TwoTickBacktrackAlwaysTrivial :
    (D0.Foundation.Q8.map (fun q =>
      D0.Foundation.uqmul q (D0.Foundation.uqinv q))).all
      (fun q => q == D0.Foundation.qONE) = true := by
  native_decide

/-- The already-existing Q8 generators i,j,k produce nontrivial
center sign on one true 3-edge ABC history. -/
theorem originalQ8ThreeTickTriangleFirstClosedSpinDistinction :
    D0.Foundation.uqmul
      (D0.Foundation.uqmul (0,1,0,0) (0,0,1,0))
      (0,0,0,1) = D0.Foundation.qNEG ∧
    D0.Foundation.uqmul
      (D0.Foundation.uqmul (0,1,0,0) (0,0,1,0))
      (0,0,0,-1) = D0.Foundation.qONE := by
  native_decide

/-- No added spinor detector: the same EXISTING native Q8 sign to
Golden-port map distinguishes the two already-available three-tick
central source histories, IF their actual scene Q8 labels can be
transported into this existing active sign port. -/
theorem originalQ8ThreeTickTriangleGoldenWitness :
    nativeQ8ProgramPort false = 0 ∧
    nativeQ8ProgramPort true = 4 * D0.primitiveRoot^3 ∧
    nativeQ8ProgramPort false ≠ nativeQ8ProgramPort true := by
  exact ⟨nativeQ8ProgramPort_grouped, nativeQ8ProgramPort_ordered,
    nativeQ8ProgramPort_grouped_ne_ordered⟩


/-! ## Strong prospective D_min reversal: a selected UNIFORM Spin sheet
has NO 327 independently stored source parameters — one CLOCK PARITY law.

All 327 original K913 Q8 central sheet bits label the general
mathematically possible graph gauge-quotient.  IF a future compulsory
prospective information-price rule selects the UNIQUE gauge class with
every original ABC triangle syndrome qNEG, then the original
representative with all directed central edge lifts qNEG exists.
Every based closed word of length n has central holonomy (-1)^n,
a function ONLY of an already owned native clock parity.

Thus the generative-description complexity of this SINGLE selected
Spin gauge class is a fixed rule, rather than 327 independent initial
sheet bits. The previously established 327-bit lower bound is
conditional on the actual physical world needing to preserve all
2^327 allowed source sheets and compare each under future tests.
This theorem proves only the parity formula on original Q8 central
group; it does NOT select all-negative physical vacuum or claim
the actual whole Book03 Info is Golden output Shannon.
-/

/-- Exact native Q8 central holonomy of n consecutive source edges
each with the original central element qNEG. This is a
representative of a possible flat projective gauge connection,
not a new physical primitive edge. -/
def nativeQ8UniformNegativeLoop : ℕ → D0.Foundation.UQuat
  | 0 => D0.Foundation.qONE
  | n + 1 =>
      D0.Foundation.uqmul D0.Foundation.qNEG
        (nativeQ8UniformNegativeLoop n)

/-- The true already-owned original center has exact period two. -/
theorem nativeQ8CenterTwiceIsIdentity (q : D0.Foundation.UQuat) :
    D0.Foundation.uqmul D0.Foundation.qNEG
      (D0.Foundation.uqmul D0.Foundation.qNEG q) = q := by
  rcases q with ⟨a,b,c,d⟩
  simp [D0.Foundation.uqmul, D0.Foundation.qNEG]

theorem nativeQ8UniformNegativeLoop_periodTwo (n : ℕ) :
    nativeQ8UniformNegativeLoop (n + 2) =
      nativeQ8UniformNegativeLoop n := by
  simp only [nativeQ8UniformNegativeLoop]
  exact nativeQ8CenterTwiceIsIdentity _

theorem nativeQ8UniformNegativeLoop_even (n : ℕ) :
    nativeQ8UniformNegativeLoop (2*n) = D0.Foundation.qONE := by
  induction n with
  | zero => rfl
  | succ n ih =>
      have h : 2*(n+1) = 2*n+2 := by omega
      rw [h, nativeQ8UniformNegativeLoop_periodTwo, ih]

theorem nativeQ8UniformNegativeLoop_odd (n : ℕ) :
    nativeQ8UniformNegativeLoop (2*n+1) =
      D0.Foundation.qNEG := by
  change D0.Foundation.uqmul D0.Foundation.qNEG
    (nativeQ8UniformNegativeLoop (2*n)) = D0.Foundation.qNEG
  rw [nativeQ8UniformNegativeLoop_even]
  native_decide


/-! ## Exact observational gauge of the ex-ante minimal three-gate witness

The six-gate matched-inventory words achieve literal full operator
I8/R8, while the three-gate words differ from them by the SAME
already owned block-common quaternion J. Whether that J matters
depends on which genuine future readouts M1 admits. For a port-
only observer invariant under the left action of commonJQ, the
three-gate and six-gate implementations have IDENTICAL outcomes
on the WHOLE complete two-arm carrier. This is the CORRECT
prospective D_min question; there is no privileged external
frame test unless one is actually physically executable/registered.

A separate independent direct native-matrix certificate checks that
the actual primitive Golden two-port POVM has this invariance
for EVERY 8-dimensional real input vector. Other future Q8 frame-
sensitive readouts could break it. Nothing here assumes that
Book03 selects or pays either execution.
-/

/-- Strong original operator relation: the exact 3-gate native
reference differs from the 6-gate full-reference ONLY by ONE
globally common original j on both quaternion spin arms. -/
theorem nativeQ8ThreeSixReferenceCommonFrame :
    nativeQ8ChronologicalWord nativeQ8MinimalReferenceWord =
      commonJQ * nativeQ8ChronologicalWord nativeQ8SixGateFullReferenceWord := by
  native_decide

theorem nativeQ8ThreeSixOrderCommonFrame :
    nativeQ8ChronologicalWord nativeQ8MinimalOrderWord =
      commonJQ * nativeQ8ChronologicalWord nativeQ8SixGateFullOrderWord := by
  native_decide

/-- Full source MATHEMATICAL gauge equivalence relative to ANY
actual observer which cannot read an overall common-j rotation. -/
theorem nativeQ8ThreeSixCommonFrameInvariant
    {Obs : Type} (readout : M8Q → Obs)
    (hinvariant : ∀ U : M8Q,
      readout (commonJQ * U) = readout U) :
    readout (nativeQ8ChronologicalWord nativeQ8MinimalReferenceWord) =
      readout (nativeQ8ChronologicalWord nativeQ8SixGateFullReferenceWord) ∧
    readout (nativeQ8ChronologicalWord nativeQ8MinimalOrderWord) =
      readout (nativeQ8ChronologicalWord nativeQ8SixGateFullOrderWord) := by
  constructor
  · rw [nativeQ8ThreeSixReferenceCommonFrame]
    exact hinvariant _
  · rw [nativeQ8ThreeSixOrderCommonFrame]
    exact hinvariant _


/-! ## NO nonminimal six-step output requirement can be imposed by a shorter exact word

This checks the deliberately MORE STRICT original whole-carrier
task: BOTH native source words must have exactly the SAME primitive
inventory and terminal operators literally (I8,R8), not merely the
same full TWO-PORT Golden statistics up to common-j gauge.

All 0..5-gate candidate words are generated only from the TWO
original Q8 gate primitives and tested in the exact rational
8×8 source representation. This is an exhaustive FINITE certificate
rather than a new physical axiom. The six-step pair has already
been exhibited in the same original module.
-/

/-- All source words of a given length, from the ORIGINAL two
forward primitives localIQ/commonJQ only. -/
def nativeQ8AllWordsOfLength : ℕ → List (List Bool)
  | 0 => [[]]
  | n + 1 =>
      (nativeQ8AllWordsOfLength n).flatMap
        (fun w => [true :: w, false :: w])

/-- A literal whole-operator same-inventory pair, not a port-only
observational gauge quotient. -/
def nativeQ8FullMatchedPairAtLength (n : ℕ) : Bool :=
  (nativeQ8AllWordsOfLength n).any (fun w =>
    (nativeQ8AllWordsOfLength n).any (fun v =>
      (w.count true == v.count true) &&
      decide (nativeQ8ChronologicalWord w = 1) &&
      decide (nativeQ8ChronologicalWord v = relativeSignQ)))

/-- Cache the two ORIGINAL endpoint tests once per source word. The tuple
stores values; its data fold is evaluated before any pairwise comparison. -/
def nativeQ8WordSummary (word : List Bool) : ℕ × Bool × Bool :=
  let data := word.foldl (nativeQ8DataStep localIQ commonJQ) (nativeQ8TabulateMatrix 1)
  let U := nativeQ8ViewMatrix data
  (word.count true, decide (U = 1), decide (U = relativeSignQ))

theorem nativeQ8WordSummary_eq (word : List Bool) :
    nativeQ8WordSummary word =
      (word.count true, decide (nativeQ8ChronologicalWord word = 1),
        decide (nativeQ8ChronologicalWord word = relativeSignQ)) := by
  simp only [nativeQ8WordSummary, nativeQ8FoldlView, nativeQ8ViewMatrix_tabulate]
  rfl

/-- The original full ordered-pair search over ALL words, with only repeated
endpoint evaluations cached. No endpoint quotient or deduplication is used. -/
def nativeQ8FullMatchedPairAtLengthEager (n : ℕ) : Bool :=
  let summaries := (nativeQ8AllWordsOfLength n).map nativeQ8WordSummary
  summaries.any (fun w =>
    summaries.any (fun v => (w.1 == v.1) && w.2.1 && v.2.2))

/-- Exact equivalence for EVERY length, not just the finite certified range. -/
@[csimp] theorem nativeQ8FullMatchedPairAtLength_eq_eager :
    nativeQ8FullMatchedPairAtLength = nativeQ8FullMatchedPairAtLengthEager := by
  funext n
  simp only [nativeQ8FullMatchedPairAtLength, nativeQ8FullMatchedPairAtLengthEager,
    List.any_map, Function.comp_def, nativeQ8WordSummary_eq]

/-- ORIGINAL 0,1,2,3,4,5-gate equal-inventory Q8 source words
cannot realize EXACT full I8 and relativeSignQ outputs at once.
The existing two six-gate construction achieves this bound. -/
theorem nativeQ8NoWholeMatchedPairBeforeSix :
    (List.range 6).all (fun n =>
       !nativeQ8FullMatchedPairAtLength n) = true := by
  native_decide

/-- Prospective minimal LENGTH for this particular full-operator
task is SIX. For a Golden-port-only test, common-j is invisible
and the corresponding true prospective minimum is THREE. -/
theorem nativeQ8FullMatchedSixIsFeasible :
    nativeQ8FullMatchedPairAtLength 6 = true := by
  native_decide

end D0.Representation.OrderMemoryControl
