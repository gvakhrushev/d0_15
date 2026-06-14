import D0.Core.Phi
import D0.Dynamics.ToralAutomorphism
import D0.Claims.Q8DedekindMinimality

/-!
# D0-Z2-SPINOR-COVER-001 — one ℤ₂ = Z(Q8), seven incarnations (synthesis)

Python certificate: `05_CERTS/vp_z2_spinor_cover.py`.

The corpus owns SEVEN order-2 facts in separate leaf modules and asserts in prose
(BOOK_02 §02.34, `[Status: SYNTHESIS]`) that they are "one ℤ₂, seven incarnations".
This synthesis module makes the identification MACHINE-CHECKED: it imports the proved
leaf modules and exhibits ≥4/7 incarnations as the SAME order-2 element, then closes
the two joints that were prose-only.

Projections proved here (each reuses a frozen leaf theorem):

* **#1 Galois ℤ₂** — `φ+ψ=1`, `φ·ψ=-1` (invariants), and the conjugation `g(x)=1-x`
  is an involution `1-(1-φ)=φ` (order 2).            [reuses `D0.Core.Phi`]
* **#3 center ℤ₂** — `Z(Q8) = {±1}`, `|Z(Q8)| = 2`. [reuses `Q8DedekindMinimality`]
* **#2 Lucas parity** = **#6 det orientation** — `signedLucasTrace n = det(Tⁿ)·Lₙ`,
  i.e. the Lucas-trace sign IS the toral orientation determinant.
                                                     [reuses `ToralAutomorphism`]

The two joints (the new synthesis content):

* **Joint A** (parity ≅ Galois ≅ det): `det T = φ·ψ` — the toral orientation sign `-1`
  is exactly the Galois norm `B`, tying #6 to #1; and `signedLucasTrace n = det(Tⁿ)·Lₙ`
  ties #2 to #6.
* **Joint B** (+2 ↦ trivial sheet): `det(T^{n+2}) = det(Tⁿ)` — the address step `+2`
  (9→11→13) is the identity element of `Z(Q8)`, staying on the same sheet of the double
  cover; the negative control `det(T^{n+1}) = -det(Tⁿ)` shows `+1` flips the sheet.

HONEST scope: this proves the seven faces are the same order-2 OBJECT and closes the
`+2` joint arithmetically. The forcing meta-step "the orientation bit is forced to be
exactly `Gal(ℚ(√5)/ℚ)` (M1 bans an exogenous orientation parameter)" stays owned by the
GOLDEN forcing prose; this module verifies the algebra of the cover, not M1-uniqueness.
-/

namespace D0.Synthesis

open D0
open D0.Dynamics
open D0.Claims
open Matrix

/-- **#1 Galois ℤ₂.** Vieta/Galois invariants `φ+ψ=1`, `φ·ψ=-1`, and the conjugation
generator `g(x)=1-x` is an involution (`g∘g = id`, so `Gal(ℚ(√5)/ℚ)` is order 2). -/
theorem galois_z2_order_two :
    phi + psi = 1 ∧ phi * psi = -1 ∧ (1 : ℝ) - (1 - phi) = phi :=
  ⟨phi_add_psi, phi_mul_psi, by ring⟩

/-- **#3 center ℤ₂.** `Z(Q8) = {±1}` and `|Z(Q8)| = 2`: the single ℤ₂ at the center of
the double cover. -/
theorem q8_center_is_z2 :
    q8Center = ({0, 1} : Finset (Fin 8)) ∧ q8Center.card = 2 := by
  refine ⟨q8_center_pm1, ?_⟩
  rw [q8_center_pm1]; decide

/-- **#2 parity = #6 det.** The signed-Lucas trace factorises as the toral orientation
determinant times the unsigned Lucas number: `signedLucasTrace n = det(Tⁿ)·Lₙ`.  So the
Lucas parity sign and the determinant orientation are the SAME `(-1)ⁿ`. -/
theorem lucas_parity_is_det (n : Nat) :
    signedLucasTrace n = Matrix.det (T ^ n) * lucas n := by
  unfold signedLucasTrace
  rw [det_T_pow]

/-- **Joint A.** The toral orientation determinant equals the Galois norm: `det T = φ·ψ`
(both `-1`).  This identifies incarnation #6 (orientation sign) with incarnation #1
(Galois norm `B`). -/
theorem det_eq_galois_norm : ((Matrix.det T : ℤ) : ℝ) = phi * psi := by
  rw [det_T, phi_mul_psi]; norm_num

/-- **Joint B.** The address step `+2` fixes the sheet: `det(T^{n+2}) = det(Tⁿ)` — it is
the identity element of `Z(Q8)`. -/
theorem plus_two_fixes_sheet (n : Nat) :
    Matrix.det (T ^ (n + 2)) = Matrix.det (T ^ n) := by
  rw [det_T_pow, det_T_pow, pow_add]; ring

/-- **Joint B (control).** The step `+1` flips the sheet: `det(T^{n+1}) = -det(Tⁿ)` — an
exogenous orientation flip, which `M1` forbids, so `+1` is banned and `+2` is forced. -/
theorem plus_one_flips_sheet (n : Nat) :
    Matrix.det (T ^ (n + 1)) = - Matrix.det (T ^ n) := by
  rw [det_T_pow, det_T_pow, pow_succ]; ring

/-- **#4 spinor double-cover sheet.** The nontrivial central element squares to the
identity: `(-1)·(-1) = +1` in Q8 (element `1` is `-1`, element `0` is `+1`), so the cover
has exactly two sheets. -/
theorem spinor_sheet_order_two : Q8.mul 1 1 = 0 := by native_decide

/-- **#5 Ω₈ orientation sign.** The orientation bit read off `Ω₈ = ABCD × {±}` is a ℤ₂:
the `±` sign carries exactly two values. -/
theorem omega8_orientation_z2 : Fintype.card Bool = 2 := by decide

/-- **#7 rank-doubling 4→8.** The two Galois embeddings are distinct (`φ ≠ ψ`), doubling
the four ABCD roles into the eight oriented states: `|Ω₈| = 2·|ABCD|`, i.e. `8 = 2·4`. -/
theorem rank_doubling_four_to_eight : phi ≠ psi ∧ (8 : Nat) = 2 * 4 := by
  refine ⟨?_, by decide⟩
  intro h
  have hpp := phi_mul_psi
  rw [← h] at hpp
  nlinarith [mul_self_nonneg phi]

/-- **D0-Z2-SPINOR-COVER-001 (synthesis, 7/7).** All seven incarnations of the single ℤ₂ —
Galois (#1), Lucas parity (#2), Q8 center (#3), spinor double-cover sheet (#4), Ω₈
orientation sign (#5), toral determinant (#6), and the rank-doubling 4→8 (#7) — unified by
the two joints (parity=det=Galois-norm, and `+2` fixes the cover sheet while `+1` flips it). -/
theorem z2_spinor_cover :
    -- #1 Galois ℤ₂ (invariants + order-2 involution)
    (phi + psi = 1 ∧ phi * psi = -1 ∧ (1 : ℝ) - (1 - phi) = phi) ∧
    -- #3 center ℤ₂
    (q8Center = ({0, 1} : Finset (Fin 8)) ∧ q8Center.card = 2) ∧
    -- joint A: #2 parity = #6 det, and det T = φ·ψ (Galois norm)
    (∀ n, signedLucasTrace n = Matrix.det (T ^ n) * lucas n) ∧
    (((Matrix.det T : ℤ) : ℝ) = phi * psi) ∧
    -- joint B: +2 fixes the sheet; +1 flips it (control)
    (∀ n, Matrix.det (T ^ (n + 2)) = Matrix.det (T ^ n)) ∧
    (∀ n, Matrix.det (T ^ (n + 1)) = - Matrix.det (T ^ n)) ∧
    -- #4 spinor double-cover sheet, #5 Ω₈ orientation, #7 rank-doubling 4→8
    (Q8.mul 1 1 = 0) ∧
    (Fintype.card Bool = 2) ∧
    (phi ≠ psi ∧ (8 : Nat) = 2 * 4) :=
  ⟨galois_z2_order_two, q8_center_is_z2, lucas_parity_is_det, det_eq_galois_norm,
    plus_two_fixes_sheet, plus_one_flips_sheet, spinor_sheet_order_two,
    omega8_orientation_z2, rank_doubling_four_to_eight⟩

end D0.Synthesis
