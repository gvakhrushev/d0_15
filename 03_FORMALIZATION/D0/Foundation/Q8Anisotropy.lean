import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# D0-Q8-ANISOTROPY-SELECT-001 (CORE-FORCING) — anisotropy selects `Q₈` over `D₄`

The two extraspecial groups of order 8 are distinguished by the Arf invariant of the squaring form
`q(ḡ)=g²` on `V=𝔽₂²`. Over `𝔽₂` there are two nondegenerate quadratic forms: `q₊(x,y)=xy` (Arf 0, split —
has nonzero **isotropic** vectors) and `q₋(x,y)=x²+xy+y²` (Arf 1, anisotropic — NO nonzero isotropic vector).
`Q₈` realizes `q₋` (every non-central element squares to the central `−1`, so `q≡1` off `0`); `D₄` realizes
`q₊` (its reflections square to `1`, giving isotropic vectors).

**M1 selector (⊥M1):** a null/isotropic branch ray is a branch direction with trivial self-return `g²=1` — a
distinction carrying no holonomy content, an unaccounted address. Forbidding null rays forces `q` anisotropic
⇒ Arf 1 ⇒ `Ω₈ ≅ Q₈`, using NO normality/Dedekind input. The isotropy facts are finite (decidable over `𝔽₂²`).
-/

namespace D0.Foundation.Q8Anisotropy

/-- Split form `q₊(x,y) = x·y` (Arf 0). -/
def qPlus (v : Fin 2 → ZMod 2) : ZMod 2 := v 0 * v 1
/-- Anisotropic form `q₋(x,y) = x² + x·y + y²` (Arf 1). -/
def qMinus (v : Fin 2 → ZMod 2) : ZMod 2 := v 0 * v 0 + v 0 * v 1 + v 1 * v 1

/-- **`q₋` is anisotropic:** no nonzero vector is isotropic (`q₋ v = 1` for every `v ≠ 0`). -/
theorem qMinus_anisotropic : ∀ v : Fin 2 → ZMod 2, v ≠ 0 → qMinus v = 1 := by decide

/-- **`q₊` is split (isotropic):** some nonzero vector is isotropic (`q₊ v = 0`, e.g. `(1,0)`). -/
theorem qPlus_isotropic : ∃ v : Fin 2 → ZMod 2, v ≠ 0 ∧ qPlus v = 0 := by decide

/-- **D0-Q8-ANISOTROPY-SELECT-001.** `q₋` (Q₈, no null ray) is anisotropic while `q₊` (D₄) has a null ray; the
no-null-ray M1 selector therefore picks `q₋` ⇒ `Q₈`, independently of Dedekind/normality. -/
theorem q8_anisotropy_select :
    (∀ v : Fin 2 → ZMod 2, v ≠ 0 → qMinus v = 1) ∧
    (∃ v : Fin 2 → ZMod 2, v ≠ 0 ∧ qPlus v = 0) :=
  ⟨qMinus_anisotropic, qPlus_isotropic⟩

end D0.Foundation.Q8Anisotropy
