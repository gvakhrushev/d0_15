import D0.Core.Phi
import Mathlib.NumberTheory.Real.Irrational

/-!
# D0-Z2-SPINOR-COVER-001 (item 2) — the Galois ℤ₂ is GENUINELY nontrivial (Mathlib reuse)

The Z2-spinor synthesis owns the "Galois ℤ₂" incarnation via `galois_z2_order_two`, but that only
records the Vieta invariants `φ+ψ=1`, `φψ=-1` and that the conjugation `x ↦ 1-x` is a ring-involution
(`1-(1-φ)=φ`). It does not establish that the extension `ℚ(φ)/ℚ` is genuinely quadratic — i.e. that
the conjugation φ↔ψ is a *nontrivial* order-2 automorphism rather than (vacuously) the identity.

This module supplies that content by REUSING Mathlib's number theory (no reinvention): `Real.sqrt 5`
is irrational (Mathlib `Nat.Prime.irrational_sqrt`), hence `φ = (1+√5)/2` is irrational, hence
`φ ≠ ψ`. So `ℚ(φ)/ℚ` is a genuine degree-2 extension and the φ↔ψ conjugation genuinely moves φ — the
"ℤ₂" is real, not a collapse.
-/

namespace D0

open Real

/-- `√5` is irrational — reused from Mathlib (`irrational_sqrt_natCast_iff`: `√n` irrational iff `n`
is not a perfect square), since `5` is not a perfect square. -/
theorem irrational_sqrt_five : Irrational (Real.sqrt 5) := by
  have h : Irrational (Real.sqrt ((5 : ℕ) : ℝ)) := by
    rw [irrational_sqrt_natCast_iff]; native_decide
  simpa using h

/-- `φ = (1+√5)/2` is irrational: if `φ` were rational then `√5 = 2φ−1` would be too. -/
theorem irrational_phi : Irrational phi := by
  rintro ⟨q, hq⟩
  refine irrational_sqrt_five ⟨2 * q - 1, ?_⟩
  have hsqrt : Real.sqrt 5 = 2 * phi - 1 := by unfold phi; ring
  rw [hsqrt, ← hq]; push_cast; ring

/-- `ψ = (1-√5)/2` is irrational: if `ψ` were rational then `√5 = 1−2ψ` would be too. -/
theorem irrational_psi : Irrational psi := by
  rintro ⟨q, hq⟩
  refine irrational_sqrt_five ⟨1 - 2 * q, ?_⟩
  have hsqrt : Real.sqrt 5 = 1 - 2 * psi := by unfold psi; ring
  rw [hsqrt, ← hq]; push_cast; ring

/-- The conjugation genuinely moves φ: `φ ≠ ψ` (their difference is `√5 > 0`). -/
theorem phi_ne_psi : phi ≠ psi := by
  have hpos : Real.sqrt 5 > 0 := Real.sqrt_pos.mpr (by norm_num)
  have hdiff : phi - psi = Real.sqrt 5 := by unfold phi psi; ring
  intro heq
  rw [heq, sub_self] at hdiff
  exact (ne_of_gt hpos) hdiff.symm

/-- **Galois ℤ₂ is genuinely nontrivial.** `φ` and `ψ` are irrational and distinct, so `ℚ(φ)/ℚ` is a
genuine quadratic extension and the φ↔ψ conjugation is a nontrivial order-2 automorphism — upgrading
the ring-involution `galois_z2_order_two` to a real field-theoretic ℤ₂ (Mathlib-backed). -/
theorem galois_z2_genuinely_nontrivial :
    Irrational phi ∧ Irrational psi ∧ phi ≠ psi :=
  ⟨irrational_phi, irrational_psi, phi_ne_psi⟩

end D0
