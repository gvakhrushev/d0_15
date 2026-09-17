import D0.Combinatorics.EulerPhi

namespace D0

def qT : ℕ := Nat.lcm 4 11
def mT : ℕ := 4 + 3
def d13 : ℕ := Nat.totient 44
def branchB : ℕ := 5
def L : ℕ := 2 * 33 + 5
def qEW : ℕ := 2 * branchB * L
def mEW : ℕ := branchB * d13 + 13
def DEW : ℕ := Nat.totient 710 / 8

theorem lcm_abcd_v11 : qT = 44 := by
  native_decide

theorem d13_from_return_window : d13 = 20 := by
  simp [d13, totient_44]

theorem qEW_forced : qEW = 710 := by
  native_decide

theorem ew_depth_from_omega8 : DEW = 35 := by
  simp [DEW, totient_710]

end D0
