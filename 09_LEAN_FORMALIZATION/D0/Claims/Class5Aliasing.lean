import D0.Claims.Window44GroupSpectrum

/-!
# D0-CLASS5-ALIASING-001 — class-5 aliasing exclusion (Cabibbo soft joint, structural)

Python certificate: `05_CERTS/vp_class5_aliasing_cabibbo.py`.

The terminal-window branch group `(ℤ/44)*` has characteristic-subgroup orders `{1,4,5,20}`
(owned by `D0.Claims.Window44GroupSpectrum`).  Class 4 is killed by orientation blindness;
class 5 by ALIASING — the odd part (the `Z5` subgroup) has order `5 = D_Σ`, so the
period-5 winding orbit collides with the 5 operational address classes (a pointer
collision = hidden memory, M1-forbidden), leaving the M1-admissible survivors `{1, 20}`.

This module proves the STRUCTURAL exclusion (the `|Z5| = 5 = D_Σ` alias and the survivor
set), reusing the frozen window-44 spectrum.  The Cabibbo readout `sin θ_C = 1/√20` is a
separate BRIDGE comparison and is NOT promoted here.
-/

namespace D0.Claims

/-- Operational address-class count `D_Σ = 5` (BOOK_04 §04.1). -/
def addressClasses : ℕ := 5

/-- The order-5 (odd-part / `Z5`) subgroup of `(ℤ/44)*` has cardinality `5 = D_Σ` — the
exact alias that collides winding-5 with the address classes. -/
theorem class5_alias_card : (units44.image (fun u => u ^ 2)).card = addressClasses :=
  window44_odd_part_card

/-- Removing class 4 (orientation) and class 5 (aliasing) from the characteristic orders
`{1,4,5,20}` leaves the M1-admissible survivors `{1, 20}`. -/
theorem class5_survivors : (({1, 4, 5, 20} : Finset ℕ) \ {4, 5}) = {1, 20} := by decide

/-- **D0-CLASS5-ALIASING-001 (structural).** `|Z5| = 5 = D_Σ` (the alias), the survivors
after the class-4 and class-5 kills are `{1, 20}`, and `20 = 4·5 = |ABCD|·D_Σ`. -/
theorem class5_aliasing :
    (units44.image (fun u => u ^ 2)).card = 5 ∧
    (({1, 4, 5, 20} : Finset ℕ) \ {4, 5}) = {1, 20} ∧
    4 * 5 = 20 :=
  ⟨window44_odd_part_card, by decide, by decide⟩

end D0.Claims
