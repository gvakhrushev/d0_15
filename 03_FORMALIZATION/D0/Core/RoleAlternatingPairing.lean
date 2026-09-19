import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import Mathlib.Tactic

/-!
# D0-ROLE-ALTERNATING-PAIRING-001 & D0-CANONICAL-CROSS-ROLE-Z2-FLUX-001

## Canonical Alternating Z₂ Pairing on Roles

The four terminal roles are:
$$\mathrm{Role} = \mathrm{Dyad} \times \mathrm{Dyad} = \mathbb{F}_2^2 = \{A, B, C, D\}.$$

The unique non-degenerate symplectic / alternating pairing on $\mathbb{F}_2^2$ is:
$$\omega(u, v) = u_1 v_2 + u_2 v_1 \pmod 2.$$

Key Theorem:
For the four elements of $\mathrm{Role}$,
$$\boxed{\omega(u, v) = 1 \iff u \ne (0,0) \wedge v \ne (0,0) \wedge u \ne v.}$$

From this universal characterization it follows immediately that:
1. $\omega(u, u) = 0$ (alternating).
2. $\omega(u, v) = \omega(v, u)$ (symmetric over $\mathbb{F}_2$).
3. **Gauge/Permutation Invariance**: For every permutation $\sigma : \mathrm{Role} \simeq \mathrm{Role}$
   fixing the zero role $\sigma((0,0)) = (0,0)$:
   $$\omega(\sigma(u), \sigma(v)) = \omega(u, v).$$

Hence the cross-role $\mathbb{Z}_2$ pairing / flux is **strictly canonical** and independent of
any basis choice or raw identification of the three nonzero roles $\{B, C, D\}$ with spatial coordinates.
-/

namespace D0.Core.RoleAlternatingPairing

open D0

/-- The distinguished zero role $A = (0, 0)$. -/
def roleZero : Role := (0, 0)

theorem roleZero_eq_A : roleZero = A := rfl

/-- The symplectic / alternating bilinear form on $\mathrm{Role} \simeq \mathbb{F}_2^2$:
$$\omega(u, v) = u_1 v_2 + u_2 v_1 \pmod 2.$$ -/
def roleOmega (u v : Role) : Bool :=
  ((u.1.val * v.2.val + u.2.val * v.1.val) % 2 == 1)

/-- The pairing is strictly alternating: $\omega(u, u) = 0$. -/
theorem roleOmega_self_zero (u : Role) : roleOmega u u = false := by
  revert u
  decide

/-- The pairing is symmetric over $\mathbb{F}_2$: $\omega(u, v) = \omega(v, u)$. -/
theorem roleOmega_comm (u v : Role) : roleOmega u v = roleOmega v u := by
  revert u v
  decide

/-- **D0-ROLE-ALTERNATING-PAIRING-001 (Universal Characterization)**:
$\omega(u, v) = 1$ if and only if $u$ and $v$ are distinct nonzero roles. -/
theorem roleOmega_iff_distinct_nonzero (u v : Role) :
    roleOmega u v = true ↔ u ≠ roleZero ∧ v ≠ roleZero ∧ u ≠ v := by
  revert u v
  decide

/-- Distinct nonzero roles always have $\omega(u, v) = 1$. -/
theorem roleOmega_of_distinct_nonzero {u v : Role}
    (hu : u ≠ roleZero) (hv : v ≠ roleZero) (huv : u ≠ v) :
    roleOmega u v = true :=
  (roleOmega_iff_distinct_nonzero u v).mpr ⟨hu, hv, huv⟩

/-- **D0-CANONICAL-CROSS-ROLE-Z2-FLUX-001 (Invariance under zero-preserving permutations)**:
Any bijection $\sigma : \mathrm{Role} \simeq \mathrm{Role}$ fixing the zero role preserves $\omega$ identically.
Thus the cross-role flux is canonical without choosing a basis among $\{B, C, D\}$. -/
theorem roleOmega_perm_invariant (σ : Equiv.Perm Role) (hσ0 : σ roleZero = roleZero) (u v : Role) :
    roleOmega (σ u) (σ v) = roleOmega u v := by
  rw [Bool.eq_iff_iff]
  rw [roleOmega_iff_distinct_nonzero, roleOmega_iff_distinct_nonzero]
  have hu_iff : σ u ≠ roleZero ↔ u ≠ roleZero := by
    constructor
    · intro h hu
      apply h
      rw [hu, hσ0]
    · intro h hu
      apply h
      have h_inj := σ.injective
      have hu' : σ u = σ roleZero := by rw [hu, hσ0]
      exact h_inj hu'
  have hv_iff : σ v ≠ roleZero ↔ v ≠ roleZero := by
    constructor
    · intro h hv
      apply h
      rw [hv, hσ0]
    · intro h hv
      apply h
      have h_inj := σ.injective
      have hv' : σ v = σ roleZero := by rw [hv, hσ0]
      exact h_inj hv'
  have huv_iff : σ u ≠ σ v ↔ u ≠ v := by
    constructor
    · intro h heq
      apply h
      rw [heq]
    · intro h heq
      apply h
      exact σ.injective heq
  rw [hu_iff, hv_iff, huv_iff]

/-- Evaluated concrete values on standard ABCD roles:
$\omega(A, \cdot) = 0$, and $\omega(r_1, r_2) = 1$ for any distinct pair among $\{B, C, D\}$. -/
theorem roleOmega_ABCD :
    roleOmega A B = false ∧
    roleOmega A C = false ∧
    roleOmega A D = false ∧
    roleOmega B C = true ∧
    roleOmega B D = true ∧
    roleOmega C D = true := by
  decide

end D0.Core.RoleAlternatingPairing
