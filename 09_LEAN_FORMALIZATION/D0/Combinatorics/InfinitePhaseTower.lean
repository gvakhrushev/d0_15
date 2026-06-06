import D0.Combinatorics.PhaseTowerRecursion

namespace D0

def nextShell (X : CapacityState) : Nat :=
  max 1 (Nat.totient (terminalWindow X))

def nextCapacity (X : CapacityState) : CapacityState :=
  { roles := X.roles,
    oriented := X.oriented,
    witness := X.witness,
    shell := nextShell X,
    rank := X.rank + 1,
    totalV := X.totalV }

def capacityTower : Nat -> CapacityState
  | 0 => C0
  | n + 1 => nextCapacity (capacityTower n)

def ValidCapacityState (X : CapacityState) : Prop :=
  X.roles = ABCDn ∧
  X.oriented = Omega8n ∧
  X.witness = 1 ∧
  0 < X.shell ∧
  X.totalV = Vtotaln

theorem nextShell_pos (X : CapacityState) : 0 < nextShell X := by
  unfold nextShell
  omega

theorem C_roles_all (n : Nat) : (capacityTower n).roles = ABCDn := by
  induction n with
  | zero =>
      rfl
  | succ n ih =>
      simp [capacityTower, nextCapacity, ih]

theorem C_oriented_all (n : Nat) : (capacityTower n).oriented = Omega8n := by
  induction n with
  | zero =>
      rfl
  | succ n ih =>
      simp [capacityTower, nextCapacity, ih]

theorem C_witness_all (n : Nat) : (capacityTower n).witness = 1 := by
  induction n with
  | zero =>
      rfl
  | succ n ih =>
      simp [capacityTower, nextCapacity, ih]

theorem C_totalV_all (n : Nat) : (capacityTower n).totalV = Vtotaln := by
  induction n with
  | zero =>
      rfl
  | succ n ih =>
      simp [capacityTower, nextCapacity, ih]

theorem C_shell_pos_all (n : Nat) : 0 < (capacityTower n).shell := by
  induction n with
  | zero =>
      native_decide
  | succ n _ =>
      simp [capacityTower, nextCapacity, nextShell_pos]

theorem capacity_recursion_total :
    ∀ n, ValidCapacityState (capacityTower n) := by
  intro n
  exact ⟨C_roles_all n, C_oriented_all n, C_witness_all n,
    C_shell_pos_all n, C_totalV_all n⟩

theorem forced_terminal_window_all :
    ∀ n, terminalWindow (capacityTower n) = Nat.lcm (capacityTower n).roles (capacityTower n).shell := by
  intro n
  rfl

theorem terminal_window_minimal_all :
    ∀ n q, TerminalSynchronized (capacityTower n) q ->
      terminalWindow (capacityTower n) ≤ q := by
  intro n q hq
  exact (terminalWindow_minimal (capacityTower n)
    (by rw [C_roles_all n, ABCDn_value]; norm_num)
    (C_shell_pos_all n)).2 q hq

theorem fullOrientedWindow_all (n : Nat) :
    fullOrientedWindow (capacityTower n) = 710 := by
  unfold fullOrientedWindow fullOrientedLength pointedAlphabet
  rw [C_roles_all n, C_witness_all n, C_totalV_all n]
  native_decide

theorem branch_projection_all :
    ∀ n, (capacityTower n).oriented ∣ Nat.totient (fullOrientedWindow (capacityTower n)) := by
  intro n
  rw [C_oriented_all n, fullOrientedWindow_all n]
  native_decide

abbrev Branches (n : Nat) := Fin ((capacityTower n).oriented)

def P (n : Nat) : Branches (n + 1) -> Branches n := fun b =>
  ⟨b.val, by
    have hb8 : b.val < 8 := by
      simpa [C_oriented_all (n + 1), Omega8n_value] using b.isLt
    simpa [C_oriented_all n, Omega8n_value] using hb8⟩

theorem projection_surjective :
    ∀ n, Function.Surjective (P n) := by
  intro n y
  refine ⟨⟨y.val, ?_⟩, ?_⟩
  · have hy := y.isLt
    have hy8 : y.val < 8 := by
      simpa [C_oriented_all n, Omega8n_value] using hy
    simpa [C_oriented_all (n + 1), Omega8n_value] using hy8
  · rfl

theorem C0_window_from_infinite_tower :
    terminalWindow (capacityTower 0) = 44 := terminalWindow_C0

theorem C0_full_window_from_infinite_tower :
    fullOrientedWindow (capacityTower 0) = 710 := fullOrientedWindow_C0

theorem C1_shell : (capacityTower 1).shell = 20 := by
  native_decide

theorem C2_shell : (capacityTower 2).shell = 8 := by
  native_decide

theorem C3_shell : (capacityTower 3).shell = 4 := by
  native_decide

theorem C4_shell : (capacityTower 4).shell = 2 := by
  native_decide

theorem shell_two_is_fixed
    (X : CapacityState)
    (hRoles : X.roles = ABCDn)
    (hShell : X.shell = 2) :
    (nextCapacity X).shell = 2 := by
  unfold nextCapacity nextShell terminalWindow
  simp [hRoles, hShell, ABCDn, D2n]
  native_decide

theorem current_recursion_stabilizes_at_shell_two :
    (capacityTower 4).shell = 2 ∧ (capacityTower 5).shell = 2 := by
  constructor
  · exact C4_shell
  · native_decide

end D0
