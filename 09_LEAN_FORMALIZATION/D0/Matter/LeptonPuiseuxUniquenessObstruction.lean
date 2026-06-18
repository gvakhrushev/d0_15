import D0.Edge.RamificationFromUeEffCompanion
import D0.Matter.LeptonGreenPuiseuxOwner
import Mathlib.Tactic

/-!
# D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 — the branch-index shortcut is FORBIDDEN (NO-GO)

Python certificate: `05_CERTS/vp_lepton_puiseux_uniqueness_obstruction.py`.

The exact charged-lepton exponent row `(p_e, p_μ, p_τ) = (0, 1/4, 1/3)` is THE (`D0-LEPTON-002`) and the
companion cover `C4` (charpoly `x⁴ − λ`) `× R3` (charpoly `x³ − λ`) gives ramification indices `1/4, 1/3`
(`D0-LEPTON-GREEN-PUISEUX-OPERATOR-001`, `D0-EDGE-RAMIFICATION-001`). A tempting **shortcut** would
promote this exact-row + companion-index observation directly to a *branch-index theorem* ("the carrier's
branch indices ARE `(0,1/4,1/3)` and therefore the operator is fixed") **without** a finite Green
resolvent whose branch indices are *provably* this row AND a *uniqueness* certificate.

This module CLOSES that shortcut as a NO-GO by a finite obstruction object. We exhibit a **second**,
demonstrably distinct `4×4` operator `companionC4Alt` (the reverse-orientation cyclic companion,
charpoly `x⁴ − λ`) that satisfies the **same** defining relation `M⁴ = λ·I` as `companionC4`, hence has
the **same** ramification/Puiseux branch index `1/4` at the branch point. Two different operators, one
branch index: the index does **not** determine the operator. Therefore promoting the exponent row to a
branch-index theorem WITHOUT a uniqueness certificate is unsound — the shortcut is forbidden.

HONESTY BOUNDARY. This is the OBSTRUCTION (the shortcut is closed-negative), **not** a closure of the
masses or of the positive route. The missing positive artifacts — a finite Green RESOLVENT over the
full shell-torus cover plus a branch-index UNIQUENESS certificate — stay PROOF-TARGET under
`D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001`. No PDG mass enters.
-/

namespace D0.Matter

open D0.Edge Matrix

/-- **Second operator with the SAME branch index `1/4`.** The reverse-orientation 4-cycle companion
(charpoly `x⁴ − λ`), distinct from `companionC4` but satisfying the same relation `M⁴ = λ·I`. -/
def companionC4Alt (lam : ℚ) : Matrix (Fin 4) (Fin 4) ℚ :=
  !![0, 0, 0, lam; 1, 0, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0]

/-- **The alternate companion satisfies its charpoly:** `C4Alt⁴ = λ·I` — the SAME defining relation as
`companionC4`, hence the SAME ramification/Puiseux branch index `1/4`. -/
theorem companionC4Alt_cyclic (lam : ℚ) :
    (companionC4Alt lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ) := by
  simp only [pow_succ, pow_zero, one_mul]
  unfold companionC4Alt
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_four, Matrix.smul_apply]

/-- **Total ramification at the branch point `λ = 0`:** `C4Alt` is nilpotent (`C4Alt⁴ = 0`), exactly
like `companionC4` — both totally ramify, same branch index. -/
theorem companionC4Alt_nilpotent_at_zero : (companionC4Alt 0) ^ 4 = 0 := by native_decide

/-- **The two operators are DISTINCT for every `λ`.** They differ in entry `(0,1)`: `companionC4` has a
`1` there (the forward shift), `companionC4Alt` has a `0`. -/
theorem companionC4_ne_alt (lam : ℚ) : companionC4Alt lam ≠ companionC4 lam := by
  intro h
  have h01 : (companionC4Alt lam) 0 1 = (companionC4 lam) 0 1 := by rw [h]
  simp [companionC4Alt, companionC4] at h01

/-- **NON-UNIQUENESS of the operator from the branch index.** There exist two *distinct* `4×4` operators
that both satisfy `M⁴ = λ·I` (the same charpoly `x⁴ − λ`, the same ramification/Puiseux branch index
`1/4`). The branch index therefore does NOT pin the operator. -/
theorem branch_index_does_not_determine_operator (lam : ℚ) :
    ∃ A B : Matrix (Fin 4) (Fin 4) ℚ,
      A ≠ B ∧
      A ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ) ∧
      B ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ) :=
  ⟨companionC4Alt lam, companionC4 lam,
   companionC4_ne_alt lam, companionC4Alt_cyclic lam, companionC4_cyclic lam⟩

/-- Record of the forbidden shortcut: index → operator is the wrong direction. -/
structure ForbiddenShortcut where
  /-- the row is exact and THE (electron unramified, muon `1/4`, tau `1/3`) -/
  exactRow : ℚ × ℚ × ℚ
  /-- the row is genuinely the companion-index row -/
  hRow : exactRow = (0, 1 / 4, 1 / 3)
  /-- but the index map is many-to-one (two distinct operators, one index) -/
  manyToOne : ∃ A B : Matrix (Fin 4) (Fin 4) ℚ, A ≠ B ∧
    A ^ 4 = (1 : ℚ) • (1 : Matrix (Fin 4) (Fin 4) ℚ) ∧
    B ^ 4 = (1 : ℚ) • (1 : Matrix (Fin 4) (Fin 4) ℚ)

/-- The forbidden shortcut object exists: the exact row is real, yet the branch-index → operator map is
many-to-one, so promoting the row to a branch-index THEOREM without a uniqueness cert is unsound. -/
def leptonPuiseuxForbiddenShortcut : ForbiddenShortcut :=
  ⟨(0, 1 / 4, 1 / 3), rfl, branch_index_does_not_determine_operator 1⟩

/-- **D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001 (NO-GO).** The exact exponent row `(0,1/4,1/3)` is
real AND its companion-cover ramification indices are real (`C4⁴ = λI`, `C4Alt⁴ = λI`, both index `1/4`),
yet there exist two DISTINCT operators with the same branch index — the index does not determine the
operator. Hence the shortcut "exact row + companion index ⇒ branch-index theorem" is FORBIDDEN without an
independent uniqueness certificate. The finite Green resolvent + branch-index uniqueness stay
PROOF-TARGET (`D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001`). -/
theorem lepton_puiseux_uniqueness_obstruction :
    -- the exact row is real
    (p_e = 0 ∧ p_mu = 1 / 4 ∧ p_tau = 1 / 3)
      -- the companion index is real (C4 carries index 1/4 via C4⁴ = λI)
      ∧ (∀ lam : ℚ, (companionC4 lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ))
      -- a SECOND distinct operator carries the SAME index 1/4 (C4Alt⁴ = λI, C4Alt ≠ C4)
      ∧ (∀ lam : ℚ, (companionC4Alt lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ))
      ∧ (∀ lam : ℚ, companionC4Alt lam ≠ companionC4 lam)
      -- therefore the branch index does NOT determine the operator (NO-GO on the shortcut)
      ∧ (∀ lam : ℚ, ∃ A B : Matrix (Fin 4) (Fin 4) ℚ,
            A ≠ B ∧ A ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ)
                  ∧ B ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ)) :=
  ⟨puiseux_exponent_row, companionC4_cyclic, companionC4Alt_cyclic, companionC4_ne_alt,
   branch_index_does_not_determine_operator⟩

end D0.Matter
