import Mathlib.Tactic
import Mathlib.NumberTheory.LucasLehmer
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Nat.Totient

/-!
# D0-WINDOW44-TOTIENT-M1-001 — `φ_E(44) = 20 = d₁₃` is exact

The first terminal phase-return window has size `q_T = |ABCD|·|V₁₁| = 4·11 = 44`. Its admissible
coprime branch count is the Euler totient `φ_E(44) = |(ℤ/44)*| = 20`, which coincides with the terminal
shell degree `d₁₃ = 9 + 11 = 20` (the degree of a zone-13 vertex in `K(9,11,13)`). This module proves the
exact number-theoretic content the cert checks:

* `q_T = 4·11 = 44` (window size);
* `Nat.totient 44 = 20` (`44 = 2²·11 ⇒ φ = 44·(1−1/2)·(1−1/11) = 20`), and the units group `(ZMod 44)ˣ`
  has `Fintype.card = 20`;
* `d₁₃ = 9 + 11 = 20`, so `φ_E(44) = d₁₃`.

M1 scope: the totient value is the automorphism count `|Aut(ℤ/44)| = φ_E(44)`; any other branch count
would change the window's automorphism class, needing an external catalogue (forbidden). This confirms and
sharpens `D0-WINDOW44-GROUP-SPECTRUM-001`; it introduces no new free number.
-/

namespace D0.VNext2.Window44Totient

/-- Window size `q_T = |ABCD|·|V₁₁| = 4·11 = 44`. -/
theorem window_size : 4 * 11 = 44 := by decide

/-- **Euler totient** `φ_E(44) = 20`. -/
theorem totient_44 : Nat.totient 44 = 20 := by decide

/-- The multiplicative-formula reading `44·(1−1/2)·(1−1/11) = 20` as an integer computation
    `44 / 2 = 22`, `22 − 22/11 = 20`. -/
theorem totient_44_multiplicative : (44 / 2) - (44 / 2) / 11 = 20 := by decide

/-- The **units group** `(ZMod 44)ˣ` has order `20` — the admissible coprime branch count. -/
theorem units_zmod44_card : Fintype.card (ZMod 44)ˣ = 20 := by
  rw [ZMod.card_units_eq_totient 44]
  decide

/-- Terminal shell degree `d₁₃ = 9 + 11 = 20` (degree of a zone-13 vertex in `K(9,11,13)`). -/
theorem d13_degree : 9 + 11 = 20 := by decide

/-- **The coincidence**: `φ_E(44) = d₁₃ = 20` — the window's totient branch count equals the terminal
    shell degree, both `20`. -/
theorem totient_eq_terminal_degree : Nat.totient 44 = 9 + 11 := by decide

end D0.VNext2.Window44Totient
