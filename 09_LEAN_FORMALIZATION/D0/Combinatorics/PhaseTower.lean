import Mathlib.NumberTheory.ArithmeticFunction.Misc
import Mathlib.Tactic

namespace D0

structure CapacityState where
  roles : Nat
  oriented : Nat
  witness : Nat
  shell : Nat
  rank : Nat
  totalV : Nat
  deriving DecidableEq, Repr

def D2n : Nat := 2
def ABCDn : Nat := D2n * D2n
def Omega8n : Nat := 2 * ABCDn
def V9n : Nat := Omega8n + 1
def V11n : Nat := V9n + D2n
def V13n : Nat := V9n + ABCDn
def Vtotaln : Nat := V9n + V11n + V13n

def C0 : CapacityState :=
  { roles := ABCDn,
    oriented := Omega8n,
    witness := 1,
    shell := V11n,
    rank := 3,
    totalV := Vtotaln }

def terminalWindow (C : CapacityState) : Nat :=
  Nat.lcm C.roles C.shell

def pointedAlphabet (C : CapacityState) : Nat :=
  C.roles + C.witness

def fullOrientedLength (C : CapacityState) : Nat :=
  2 * C.totalV + pointedAlphabet C

def fullOrientedWindow (C : CapacityState) : Nat :=
  2 * pointedAlphabet C * fullOrientedLength C

def admissibleBranches (q : Nat) : Nat := Nat.totient q

def TerminalSynchronized (C : CapacityState) (q : Nat) : Prop :=
  C.roles ∣ q ∧ C.shell ∣ q ∧ 0 < q

def FullOrientedSynchronized (C : CapacityState) (q : Nat) : Prop :=
  2 * pointedAlphabet C ∣ q ∧ fullOrientedLength C ∣ q ∧ 0 < q

theorem D2n_value : D2n = 2 := rfl
theorem ABCDn_value : ABCDn = 4 := by native_decide
theorem Omega8n_value : Omega8n = 8 := by native_decide
theorem V9n_value : V9n = 9 := by native_decide
theorem V11n_value : V11n = 11 := by native_decide
theorem V13n_value : V13n = 13 := by native_decide
theorem Vtotaln_value : Vtotaln = 33 := by native_decide

theorem terminalWindow_C0 : terminalWindow C0 = 44 := by
  native_decide

theorem pointedAlphabet_C0 : pointedAlphabet C0 = 5 := by
  native_decide

theorem fullOrientedLength_C0 : fullOrientedLength C0 = 71 := by
  native_decide

theorem fullOrientedWindow_C0 : fullOrientedWindow C0 = 710 := by
  native_decide

theorem branches_are_totient (q : Nat) :
    admissibleBranches q = Nat.totient q := rfl

end D0
