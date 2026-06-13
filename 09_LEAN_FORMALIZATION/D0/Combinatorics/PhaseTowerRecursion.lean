import D0.Combinatorics.PhaseTowerControls

namespace D0

structure PhaseStep where
  C : CapacityState
  qTerm : Nat
  qFull : Nat
  branchesTerm : Nat
  branchesFull : Nat
  deriving DecidableEq, Repr

def phaseStep (C : CapacityState) : PhaseStep :=
  { C := C,
    qTerm := terminalWindow C,
    qFull := fullOrientedWindow C,
    branchesTerm := Nat.totient (terminalWindow C),
    branchesFull := Nat.totient (fullOrientedWindow C) }

def nextShellFromBranches (s : PhaseStep) : Nat :=
  s.branchesTerm

def nextDepthPerOrientation (s : PhaseStep) : Nat :=
  s.branchesFull / s.C.oriented

theorem C0_next_shell :
    nextShellFromBranches (phaseStep C0) = 20 := by
  native_decide

theorem C0_next_depth :
    nextDepthPerOrientation (phaseStep C0) = 35 := by
  native_decide

theorem C0_full_branches :
    (phaseStep C0).branchesFull = 280 := by
  native_decide

theorem C0_oriented_divides_full_branches :
    C0.oriented ∣ Nat.totient (fullOrientedWindow C0) := by
  native_decide

theorem fullBranches_project_to_oriented_depth
    (C : CapacityState)
    (h : C.oriented ∣ Nat.totient (fullOrientedWindow C)) :
    C.oriented * ((Nat.totient (fullOrientedWindow C)) / C.oriented)
      = Nat.totient (fullOrientedWindow C) := by
  exact Nat.mul_div_cancel' h

end D0
