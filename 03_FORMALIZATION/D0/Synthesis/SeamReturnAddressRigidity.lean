import Mathlib.Tactic
import D0.Geometry.Pi0DiscreteAngle
import D0.Synthesis.ToralCompositionSeventeen

/-!
# Seam-return address rigidity: the unique pair `(12,5)`

**Target context.** The α-seam front owns two exact objects independently:

* the reduced seam angle `θ = 12/5` (`D0-PI0-DISCRETE-ANGLE-001`);
* the toral depth arithmetic `17 = 12 + 5` and
  `φ⁻¹⁷ = (φ⁵−11)(322−φ¹²)` (`D0-TORAL-COMPOSITION-SEVENTEEN-001`).

The remaining P2 semantic primitive is to identify the seam transport with those toral returns.
This module does **not** assert that identification. It proves the strongest arithmetic statement
available before it:

> If a return address `(m,n)` is required to encode the reduced angle as `m/n = 12/5` and the
> total depth as `m+n = 17`, then `(m,n) = (12,5)` uniquely.

Thus there is no rival integer return pair compatible with both owned quantities. The numerator
is forced to the twelfth return, the denominator to the fifth return, and the two owned
return-defect factors and their product follow. The residual P2 content is exactly the semantic
rule that the seam uses this angle/depth address — not any arithmetic choice among return pairs.
-/

namespace D0.Synthesis.SeamReturnAddressRigidity

open Real
open scoped goldenRatio
open D0.Geometry
open D0.Synthesis.ToralCompositionSeventeen

/-- An integer return address whose ratio is the owned reduced seam angle and whose sum is the
owned total depth. `m` is the transport/numerator address; `n` is the seam/denominator address. -/
def ReturnAddress (m n : ℕ) : Prop :=
  0 < n ∧ (m : ℚ) / n = 12 / 5 ∧ m + n = 17

/-- The owned pair `(12,5)` is an address. -/
theorem twelve_five_is_address : ReturnAddress 12 5 := by
  norm_num [ReturnAddress]

/-- **Address uniqueness.** Any positive-denominator integer address with ratio `12/5` and
sum `17` is exactly `(12,5)`. -/
theorem return_address_unique {m n : ℕ} (h : ReturnAddress m n) :
    m = 12 ∧ n = 5 := by
  rcases h with ⟨hn, hratio, hsum⟩
  have hnq : (n : ℚ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hn)
  have hcrossQ : (5 : ℚ) * m = 12 * n := by
    field_simp [hnq] at hratio
    linarith
  have hcross : 5 * m = 12 * n := by exact_mod_cast hcrossQ
  omega

/-- The address is reduced: `gcd(12,5)=1`. -/
theorem address_coprime : Nat.Coprime 12 5 := by decide

/-- The owned discrete angle supplies exactly the address ratio. -/
theorem owned_angle_is_address_ratio :
    2 * pi0 * (2 - D0.phi) = (12 : ℝ) / 5 :=
  seam_angle_eq_twelve_fifths

/-- Any compatible address forces the fifth-return seam defect. -/
theorem address_forces_seam_return {m n : ℕ} (h : ReturnAddress m n) :
    n = 5 ∧ (φ⁻¹) ^ n = φ ^ 5 - 11 := by
  have hn := (return_address_unique h).2
  subst n
  exact ⟨rfl, seam_factor_toral_address⟩

/-- Any compatible address forces the twelfth-return transport defect. -/
theorem address_forces_transport_return {m n : ℕ} (h : ReturnAddress m n) :
    m = 12 ∧ (φ⁻¹) ^ m = 322 - φ ^ 12 := by
  have hm := (return_address_unique h).1
  subst m
  exact ⟨rfl, transport_factor_toral_address⟩

/-- Any compatible address forces the full toral factorization of the depth. -/
theorem address_forces_total_factorization {m n : ℕ} (h : ReturnAddress m n) :
    (φ⁻¹) ^ (m + n) = (φ ^ 5 - 11) * (322 - φ ^ 12) := by
  obtain ⟨rfl, rfl⟩ := return_address_unique h
  exact registered_total_toral_form

/-- Capstone: the exact angle, existence/uniqueness of `(12,5)`, both return defects, and their
composed depth. This is arithmetic address rigidity; the seam-to-toral semantic identification
remains the explicitly named P2 primitive. -/
theorem seam_return_address_rigidity :
    2 * pi0 * (2 - D0.phi) = (12 : ℝ) / 5
      ∧ ReturnAddress 12 5
      ∧ (∀ m n : ℕ, ReturnAddress m n → m = 12 ∧ n = 5)
      ∧ (φ⁻¹) ^ 5 = φ ^ 5 - 11
      ∧ (φ⁻¹) ^ 12 = 322 - φ ^ 12
      ∧ (φ⁻¹) ^ 17 = (φ ^ 5 - 11) * (322 - φ ^ 12) :=
  ⟨owned_angle_is_address_ratio, twelve_five_is_address,
    fun _ _ => return_address_unique, seam_factor_toral_address,
    transport_factor_toral_address, registered_total_toral_form⟩

end D0.Synthesis.SeamReturnAddressRigidity
