import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# A finite internal stage register for a reversible comparison program

The concrete order-memory program has 14 comparison operations followed by one
registration operation. Sixteen clock labels distinguish stages 0 through 15.
A single fixed reversible transition advances the clock and selects the local
operation. This is a compiler over SUPPLIED reversible operations, not a proof
that those operations or a blank apparatus arise from M1.

The register is finite and cyclic. Stage/history claims here concern the first
15 transitions. No unbounded archive or irreversible erasure is inferred.
-/

namespace D0.Representation.FiniteProtocolClock

abbrev Clock := ZMod 16

/-- One autonomous transition. The program is stored in the fixed family U. -/
def step {S : Type*} (U : Clock → S ≃ S) : (Clock × S) ≃ (Clock × S) where
  toFun x := (x.1 + 1, U x.1 x.2)
  invFun x := (x.1 - 1, (U (x.1 - 1)).symm x.2)
  left_inv := by intro ⟨c,s⟩; simp
  right_inv := by intro ⟨c,s⟩; simp

def run {S : Type*} (U : Clock → S ≃ S) (s : S) : ℕ → Clock × S
  | 0 => (0,s)
  | n+1 => step U (run U s n)

theorem stage_is_internal {S : Type*} (U : Clock → S ≃ S) (s : S) (n : ℕ) :
    (run U s n).1 = (n : Clock) := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [run, step, ih] using (Nat.cast_add n 1 :
      ((n+1 : ℕ) : Clock) = (n : Clock) + (1 : Clock)).symm

/-- Clock content depends on the program stage, never on the signal arm. -/
theorem stage_does_not_record_arm {S : Type*} (U : Clock → S ≃ S)
    (v w : S) (n : ℕ) : (run U v n).1 = (run U w n).1 := by
  rw [stage_is_internal, stage_is_internal]

theorem first_sixteen_labels_distinct :
    Function.Injective (fun n : Fin 16 => (n.val : Clock)) := by native_decide

/-- Every individual transition is reversible on the complete carrier. -/
theorem step_loses_no_state {S : Type*} (U : Clock → S ≃ S) :
    Function.Injective (step U) := (step U).injective

/-- State-norm preservation reduces exactly to the supplied stage operators. -/
theorem step_preserves_response {S : Type*} (U : Clock → S ≃ S)
    (response : S → ℝ) (h : ∀ c s, response (U c s) = response s)
    (x : Clock × S) : response (step U x).2 = response x.2 := h x.1 x.2

theorem completed_stage {S : Type*} (U : Clock → S ≃ S) (s : S) :
    (run U s 15).1 = 15 := stage_is_internal U s 15

/-- Store the protocol choice INSIDE the machine. The same fixed transition
handles both programs and never overwrites the program label. -/
def programmedStep {P S : Type*} (U : P → Clock → S ≃ S) :
    (P × (Clock × S)) ≃ (P × (Clock × S)) where
  toFun x := (x.1, step (U x.1) x.2)
  invFun x := (x.1, (step (U x.1)).symm x.2)
  left_inv := by intro ⟨p,x⟩; simp
  right_inv := by intro ⟨p,x⟩; simp

theorem program_is_retained {P S : Type*} (U : P → Clock → S ≃ S)
    (x : P × (Clock × S)) : (programmedStep U x).1 = x.1 := rfl

/-- Reversible registration on BASIS labels (arm, record), not cloning an
unknown superposition. Its linear permutation extension correlates the record. -/
def register : (Bool × Bool) ≃ (Bool × Bool) where
  toFun x := (x.1, Bool.xor x.1 x.2)
  invFun x := (x.1, Bool.xor x.1 x.2)
  left_inv := by decide
  right_inv := by decide

theorem blank_record_receives_arm (arm : Bool) : register (arm, false) = (arm, arm) := by
  cases arm <;> rfl

theorem registration_does_not_erase : Function.Injective register := register.injective

end D0.Representation.FiniteProtocolClock
