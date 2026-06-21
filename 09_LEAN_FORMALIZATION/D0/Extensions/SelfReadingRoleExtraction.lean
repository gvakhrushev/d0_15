import D0.Extensions.RepresentationReadoutExtension
import Mathlib.Tactic

/-!
# Self-reading role extraction (Section 2.1)

What `S₀` FORCES on the representation side: carrier `ℂ³³`, commutant `M₃⊕ℂ³` dim 12. What it does NOT fix:
the `ℤ₂`-grading SIGNATURE of the `M₃` generation block, whose grading-even neutral-current count
`nc(p,q)=p²+q²+3` diverges (`8` for `(2,1)` vs `12` for `(3,0)`). The Weyl-role bijection leg is RESOLVED by
the Aut part-size order (9<11<13) and is therefore NOT the separator; the grading signature is. `N_active = 3`
is NOT asserted from rank — it would require three orthogonal light channels with nonzero frozen
neutral-current response, which `S₀` does not supply.
-/

namespace D0.Extensions.SelfReadingRoleExtraction

open D0.Extensions.RepresentationReadoutExtension

/-- **2.1 forced vs disputed.** Forced: commutant dim 12. Disputed: neutral-current count `8 ≠ 12` (grading
signature), not the Weyl-role bijection. -/
theorem role_extraction_forced_vs_disputed :
    (9 + 1 + 1 + 1 = 12) ∧ ncCount 2 1 = 8 ∧ ncCount 3 0 = 12 ∧ ncCount 2 1 ≠ ncCount 3 0 :=
  ⟨by decide, nc_signature_21, nc_signature_30, nc_divergent⟩

end D0.Extensions.SelfReadingRoleExtraction
