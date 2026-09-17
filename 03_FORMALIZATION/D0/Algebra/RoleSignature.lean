import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

namespace D0

inductive RoleSig where
  | A | B | C | D
  deriving DecidableEq, Repr, Fintype

def roleSign : RoleSig -> Int
  | RoleSig.A => 1
  | RoleSig.B => -1
  | RoleSig.C => -1
  | RoleSig.D => -1

def positiveRoles : Nat :=
  ((Finset.univ : Finset RoleSig).filter (fun r => roleSign r = 1)).card

def negativeRoles : Nat :=
  ((Finset.univ : Finset RoleSig).filter (fun r => roleSign r = -1)).card

theorem role_signature_1_3 :
    positiveRoles = 1 ∧ negativeRoles = 3 := by
  native_decide

theorem role_cardinality_four :
    Fintype.card RoleSig = 4 := by
  native_decide

end D0
