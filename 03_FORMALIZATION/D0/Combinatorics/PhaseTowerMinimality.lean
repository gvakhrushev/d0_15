import D0.Combinatorics.PhaseTower

namespace D0

theorem terminalWindow_minimal
    (C : CapacityState)
    (hRoles : 0 < C.roles)
    (hShell : 0 < C.shell) :
    TerminalSynchronized C (terminalWindow C) ∧
    ∀ q, TerminalSynchronized C q → terminalWindow C ≤ q := by
  constructor
  · constructor
    · exact Nat.dvd_lcm_left C.roles C.shell
    constructor
    · exact Nat.dvd_lcm_right C.roles C.shell
    · exact Nat.lcm_pos hRoles hShell
  · intro q hq
    have hdvd : terminalWindow C ∣ q := by
      exact Nat.lcm_dvd hq.1 hq.2.1
    exact Nat.le_of_dvd hq.2.2 hdvd

theorem C0_full_oriented_coprime :
    Nat.Coprime (2 * pointedAlphabet C0) (fullOrientedLength C0) := by
  native_decide

theorem fullOrientedWindow_minimal
    (C : CapacityState)
    (hA : 0 < pointedAlphabet C)
    (hL : 0 < fullOrientedLength C)
    (hCoprime :
      Nat.Coprime (2 * pointedAlphabet C) (fullOrientedLength C)) :
    FullOrientedSynchronized C (fullOrientedWindow C) ∧
    ∀ q, FullOrientedSynchronized C q → fullOrientedWindow C ≤ q := by
  constructor
  · constructor
    · unfold fullOrientedWindow
      exact dvd_mul_right (2 * pointedAlphabet C) (fullOrientedLength C)
    constructor
    · unfold fullOrientedWindow
      exact dvd_mul_left (fullOrientedLength C) (2 * pointedAlphabet C)
    · unfold fullOrientedWindow
      exact Nat.mul_pos (Nat.mul_pos (by norm_num) hA) hL
  · intro q hq
    have hdvd : fullOrientedWindow C ∣ q := by
      unfold fullOrientedWindow
      exact hCoprime.mul_dvd_of_dvd_of_dvd hq.1 hq.2.1
    exact Nat.le_of_dvd hq.2.2 hdvd

theorem fullOrientedWindow_C0_minimal :
    FullOrientedSynchronized C0 710 ∧
    ∀ q, FullOrientedSynchronized C0 q → 710 ≤ q := by
  have hmin := fullOrientedWindow_minimal C0 (by native_decide) (by native_decide)
    C0_full_oriented_coprime
  rw [fullOrientedWindow_C0] at hmin
  exact hmin

theorem terminalWindow_C0_minimal :
    TerminalSynchronized C0 44 ∧
    ∀ q, TerminalSynchronized C0 q → 44 ≤ q := by
  have hmin := terminalWindow_minimal C0 (by native_decide) (by native_decide)
  rw [terminalWindow_C0] at hmin
  exact hmin

end D0
