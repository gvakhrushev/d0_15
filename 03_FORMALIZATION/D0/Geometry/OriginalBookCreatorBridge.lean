import D0.Geometry.ArchiveCARDirac

namespace D0.Geometry.OriginalBookCreatorBridge

open D0

/-!
An exact finite reindexing of the original Book source's four creator matrices.
The source is `check_uniform_book_source.py`, Git blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed` at commit
`eebcb5e467742df3e9cf7fa9702042d7294aa742`. Its `creators` loop uses
`order = (0, 2, 3, 1)`, integer occupation bit strings 0–15, and matrix
entry `[bits | (1 << r), bits]` with the Jordan–Wigner sign.
The original full128 modular checker's corresponding creator block is in
`check_future_even_algebra_modprime.py`, blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a` at the same commit.

This proves correspondence of the four elementary creator matrices only.
The original 128 Kraus operators, effect span and its two-block identification,
and physical admission are separate open obligations.
-/

/-- The source bit positions corresponding to roles ordered A, B, C, D. -/
def sourceBit (role : Role) : Nat :=
  if role = A then 0 else if role = B then 2 else if role = C then 3 else 1

/-- Interpret an original source integer as a typed four-role occupation. -/
def sourceState (bits : Fin 16) : ArchiveFockState :=
  fun role => bits.val.testBit (sourceBit role)

/-- Reassemble an occupation into the original integer basis index. -/
def sourceIndex (state : ArchiveFockState) : Fin 16 :=
  ⟨(if state A then 1 else 0) + (if state B then 4 else 0) +
   (if state C then 8 else 0) + (if state D then 2 else 0), by
     have hA : (if state A then 1 else 0 : Nat) ≤ 1 := by split <;> omega
     have hB : (if state B then 4 else 0 : Nat) ≤ 4 := by split <;> omega
     have hC : (if state C then 8 else 0 : Nat) ≤ 8 := by split <;> omega
     have hD : (if state D then 2 else 0 : Nat) ≤ 2 := by split <;> omega
     omega⟩

/-- Direct finite transcription of the upstream creator loop. -/
def sourceCreator (mode : Nat) (bra ket : Fin 16) : ℤ :=
  if ket.val.testBit mode = false ∧ bra.val = Nat.lor ket.val (2 ^ mode) then
    let before := ([0, 2, 3, 1] : List Nat).takeWhile (· != mode)
    let count := (before.filter (fun index => ket.val.testBit index)).length
    if count % 2 = 0 then 1 else -1
  else 0

set_option maxRecDepth 100000 in
private theorem creator_ket_0 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (0 : Fin 16) =
      carAnnihilateInt role (sourceState (0 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_1 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (1 : Fin 16) =
      carAnnihilateInt role (sourceState (1 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_2 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (2 : Fin 16) =
      carAnnihilateInt role (sourceState (2 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_3 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (3 : Fin 16) =
      carAnnihilateInt role (sourceState (3 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_4 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (4 : Fin 16) =
      carAnnihilateInt role (sourceState (4 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_5 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (5 : Fin 16) =
      carAnnihilateInt role (sourceState (5 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_6 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (6 : Fin 16) =
      carAnnihilateInt role (sourceState (6 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_7 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (7 : Fin 16) =
      carAnnihilateInt role (sourceState (7 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_8 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (8 : Fin 16) =
      carAnnihilateInt role (sourceState (8 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_9 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (9 : Fin 16) =
      carAnnihilateInt role (sourceState (9 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_10 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (10 : Fin 16) =
      carAnnihilateInt role (sourceState (10 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_11 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (11 : Fin 16) =
      carAnnihilateInt role (sourceState (11 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_12 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (12 : Fin 16) =
      carAnnihilateInt role (sourceState (12 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_13 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (13 : Fin 16) =
      carAnnihilateInt role (sourceState (13 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_14 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (14 : Fin 16) =
      carAnnihilateInt role (sourceState (14 : Fin 16)) (sourceState bra) := by
  decide

set_option maxRecDepth 100000 in
private theorem creator_ket_15 : ∀ (role : Role) (bra : Fin 16),
    sourceCreator (sourceBit role) bra (15 : Fin 16) =
      carAnnihilateInt role (sourceState (15 : Fin 16)) (sourceState bra) := by
  decide

theorem source_creator_eq_car
    (role : Role) (bra ket : Fin 16) :
    sourceCreator (sourceBit role) bra ket =
      carAnnihilateInt role (sourceState ket) (sourceState bra) := by
  fin_cases ket <;> first
    | exact creator_ket_0 role bra
    | exact creator_ket_1 role bra
    | exact creator_ket_2 role bra
    | exact creator_ket_3 role bra
    | exact creator_ket_4 role bra
    | exact creator_ket_5 role bra
    | exact creator_ket_6 role bra
    | exact creator_ket_7 role bra
    | exact creator_ket_8 role bra
    | exact creator_ket_9 role bra
    | exact creator_ket_10 role bra
    | exact creator_ket_11 role bra
    | exact creator_ket_12 role bra
    | exact creator_ket_13 role bra
    | exact creator_ket_14 role bra
    | exact creator_ket_15 role bra

/-- The source indices and the typed Fock states are actual inverse encodings. -/
theorem sourceIndex_sourceState : ∀ bits : Fin 16, sourceIndex (sourceState bits) = bits := by
  decide

theorem sourceState_sourceIndex (state : ArchiveFockState) :
    sourceState (sourceIndex state) = state := by
  funext role
  have h : ∀ (s : ArchiveFockState) (r : Role), sourceState (sourceIndex s) r = s r := by
    decide
  exact h state role

def sourceStateEquiv : Fin 16 ≃ ArchiveFockState where
  toFun := sourceState
  invFun := sourceIndex
  left_inv := sourceIndex_sourceState
  right_inv := sourceState_sourceIndex

/-- Matrix equality in the public real-valued CAR interface. -/
theorem source_creator_eq_real_car (role : Role) (bra ket : Fin 16) :
    (sourceCreator (sourceBit role) bra ket : ℝ) =
      carCreate role (sourceState bra) (sourceState ket) := by
  rw [carCreate, carAnnihilate_eq_intCast, ← source_creator_eq_car]

/-- The original integer bit count equals the typed Fock occupation. -/
theorem source_occupation_eq_car : ∀ bits : Fin 16,
    fockOccupationCount (sourceState bits) =
      (([0, 1, 2, 3] : List Nat).filter bits.val.testBit).length := by
  decide

/-- The original integer bit count induces the existing Fock parity sign. -/
theorem source_parity_eq_car (bits : Fin 16) :
    fockParitySign (sourceState bits) =
      (if (([0, 1, 2, 3] : List Nat).filter bits.val.testBit).length % 2 = 0
        then (1 : ℝ) else -1) := by
  simp only [fockParitySign, source_occupation_eq_car]

end D0.Geometry.OriginalBookCreatorBridge
