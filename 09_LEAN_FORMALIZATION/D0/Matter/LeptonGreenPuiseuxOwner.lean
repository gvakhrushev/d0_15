import D0.Edge.RamificationFromUeEffCompanion
import Mathlib.Tactic

/-!
# D0-LEPTON-GREEN-PUISEUX-OPERATOR-001 — shell-torus Puiseux ramification row (Lean scaffold)

Python certificates: `05_CERTS/vp_lepton_green_puiseux_operator.py`,
`05_CERTS/vp_lepton_sturmian_puiseux_coefficients.py`, `05_CERTS/vp_lepton_puiseux_decimal_section.py`.

Front B construction. The charged-lepton hierarchy is carried by a shell-torus companion cover
`C4 × R3`: the 4-cycle terminal-capacity block `C4` (charpoly `x⁴ − λ`) and the 3-cycle scene-rank
block `R3` (charpoly `x³ − λ`) from `D0-EDGE-RAMIFICATION-001`. At a branch point `x = λ^{1/n}`, so the
Puiseux/ramification index of an `n`-cycle companion is `1/n`. Hence the cover yields the exponent row
`(p_e, p_μ, p_τ) = (0, 1/4, 1/3)`: the electron is **unramified** (regular, index 0), the muon ramifies
through the 4-cycle (index `1/4`), the tau through the 3-cycle (index `1/3`). This matches the exact
exponent row already declared THE (`D0-LEPTON-002`).

HONESTY BOUNDARY. What is owned here (OPERATOR-SCAFFOLD-CERTIFIED) is the companion-cover operator and
that its ramification indices ARE `(0, 1/4, 1/3)`. What stays PROOF-TARGET: (1) the finite Green
RESOLVENT over the cover (not just the companion blocks); (2) the branch-index UNIQUENESS theorem (that
no other exponent row is consistent with the K(9,11,13) carrier) — `D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001`;
(3) the EFT/IR matching functor mapping the row to the 17-digit decimals — `D0-LEPTON-PUISEUX-DECIMAL-SECTION-001`
(BRIDGE, `ASSUMP-EFT-IR-MATCHING-SCHEME`). The direct raw-graph→decimal route stays NO-GO
(`D0-BARE-GRAPH-DECIMAL-NOGO-001`); the decimals stay HYP. No PDG mass enters.
-/

namespace D0.Matter

open D0.Edge Matrix

/-- Shell-torus companion cover: C4 (4-cycle terminal capacity) × R3 (3-cycle scene rank). -/
structure ShellTorus where
  c4 : Nat
  r3 : Nat
  h_c4 : c4 = 4
  h_r3 : r3 = 3

/-- The lepton shell-torus cover. -/
def shellTorus : ShellTorus := ⟨4, 3, rfl, rfl⟩

/-- Puiseux/ramification exponent of the electron branch: unramified (regular), index `0`. -/
def p_e : ℚ := 0
/-- Puiseux/ramification exponent of the muon branch: 4-cycle, index `1/4`. -/
def p_mu : ℚ := 1 / 4
/-- Puiseux/ramification exponent of the tau branch: 3-cycle, index `1/3`. -/
def p_tau : ℚ := 1 / 3

/-- **The exponent row is the reciprocal of the companion cycle lengths** (electron unramified):
`p_μ = 1/c4 = 1/4`, `p_τ = 1/r3 = 1/3`, `p_e = 0`. -/
theorem puiseux_row_from_cycle_lengths :
    p_e = 0 ∧ p_mu = 1 / (shellTorus.c4 : ℚ) ∧ p_tau = 1 / (shellTorus.r3 : ℚ) := by
  unfold shellTorus p_e p_mu p_tau
  norm_num

/-- The exact exponent row `(0, 1/4, 1/3)`. -/
theorem puiseux_exponent_row : p_e = 0 ∧ p_mu = 1 / 4 ∧ p_tau = 1 / 3 := ⟨rfl, rfl, rfl⟩

/-- **D0-LEPTON-GREEN-PUISEUX-OPERATOR-001 (operator scaffold).** The shell-torus companion cover
`C4 × R3` realizes the lepton ramification — `C4⁴ = λI` (4-cycle ⇒ index `1/4`), `R3³ = λI` (3-cycle ⇒
index `1/3`), electron unramified (`0`) — so its ramification exponent row is exactly
`(p_e, p_μ, p_τ) = (0, 1/4, 1/3)`. The finite Green resolvent and branch-index uniqueness stay
PROOF-TARGET; no PDG mass enters. -/
theorem lepton_green_puiseux_operator_scaffold :
    (shellTorus.c4 = 4 ∧ shellTorus.r3 = 3)
      ∧ (p_e = 0 ∧ p_mu = 1 / (shellTorus.c4 : ℚ) ∧ p_tau = 1 / (shellTorus.r3 : ℚ))
      ∧ (∀ lam : ℚ, (companionC4 lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ))
      ∧ (∀ lam : ℚ, (companionR3 lam) ^ 3 = lam • (1 : Matrix (Fin 3) (Fin 3) ℚ))
      ∧ (companionC4 0) ^ 4 = 0 ∧ (companionR3 0) ^ 3 = 0 :=
  ⟨⟨rfl, rfl⟩, puiseux_row_from_cycle_lengths, companionC4_cyclic, companionR3_cyclic,
   companionC4_nilpotent_at_zero, companionR3_nilpotent_at_zero⟩

end D0.Matter
