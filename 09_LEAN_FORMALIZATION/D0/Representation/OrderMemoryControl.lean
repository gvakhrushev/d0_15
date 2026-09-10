import D0.Representation.OrderMemoryReadout
import D0.Representation.GoldenOrderInterferometer
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

end D0.Representation.OrderMemoryControl
