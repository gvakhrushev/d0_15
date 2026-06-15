import D0.Tower.NoExtension

/-!
# D0-DETECTION-QUADRATIC-001 — degree-2 forced by the detection act (Lean, 2nd channel)

Python certificate: `05_CERTS/vp_detection_quadratic_types.py`.

A fifth independent route to the primitive quadratic `p²+p=1` (`p=φ⁻¹`): the act of detection has
exactly TWO comparison kinds — by membership (`∈`, levels 1↔2 different categories ⇒ linear,
degree 1) and by value (levels 2↔3 one category ⇒ bilinear=area, degree 2). The degree is forced
to be 2 because there are exactly two comparison kinds, and a would-be third (a `p³` term) reduces
into `span{1,p}` (`p³ = 2p − 1`) so it is not an independent slot.

This module is deliberately thin: the decidable ALGEBRA is exactly the tower-stop content
(`D0.Tower.NoExtension.degree2_closure`, `p_cubed_reduces`) — reused, not re-proved. What is added
here is the count `|{membership, value}| = 2` and its bundling with the algebra into one statement,
the type-theoretic 2nd channel to obligation 5. The categorical "two kinds exhaust degree 2" is the
forcing READING (DEF-0.2.2 style), not a separate machine-checked categorical theorem.
-/

namespace D0.Tower

open D0

/-- The two comparison kinds of the detection act: `membership` (∈) and `value`. -/
inductive ComparisonKind
  | membership   -- levels 1↔2: different categories ⇒ linear (degree 1)
  | value        -- levels 2↔3: one category ⇒ bilinear=area (degree 2)
deriving DecidableEq, Fintype

/-- **Exactly two comparison kinds.** `|{membership, value}| = 2` — the degree of the primitive
`p²+p=1`. A third kind would be a degree-3 term, excluded by `p_cubed_reduces`. -/
theorem two_comparison_kinds : Fintype.card ComparisonKind = 2 := by decide

/-- **No third comparison kind.** A degree-3 term reduces into the rank-2 algebra `span{1,p}`
(`p³ = 2p − 1`), so there is no independent third slot — reuses the tower-stop reduction. -/
theorem no_third_comparison_kind : phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1 := p_cubed_reduces

/-- **D0-DETECTION-QUADRATIC-001.** The detection act forces degree 2: the primitive closes
(`p + p² = 1`), there are exactly two comparison kinds (`= 2`, the degree), and no independent
third kind (`p³ = 2p − 1` reduces). The algebra is the CORE tower-stop content; this is its
type-theoretic 2nd channel. -/
theorem detection_quadratic :
    (phi⁻¹ + phi⁻¹ ^ 2 = 1) ∧
    (Fintype.card ComparisonKind = 2) ∧
    (phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1) :=
  ⟨degree2_closure, two_comparison_kinds, no_third_comparison_kind⟩

end D0.Tower
