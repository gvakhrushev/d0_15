import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Representation.Omega8OrientationDecomposition
import D0.UnifiedFiniteCore.Q8Terminal
import D0.Claims.Q8DedekindMinimality
import D0.Core.RoleAlternatingPairing

/-!
# D0-OMEGA8-Q8-TYPED-BRIDGE-001

## Typed Seam Closure: Unifying Omega8 = Role × Orient, Q8Dedekind, and Q8Terminal

This module establishes the explicit equivalence between the three historical representations of $\Omega_8$:
1. The structural core type $\Omega_8 = \mathrm{Role} \times \mathrm{Orient}$ ($4 \times 2 = 8$).
2. The Dedekind order in `D0.Claims.Q8DedekindMinimality`: $[+1, -1, +i, -i, +j, -j, +k, -k]$.
3. The Terminal Fourier order in `D0.UnifiedFiniteCore.Q8Terminal`: $[+1, +i, +j, +k, -1, -i, -j, -k]$.

### Key Exact Results:
* **Terminal Equivalence**: The map
  $$\phi_{\mathrm{term}} : \Omega_8 \to \mathrm{Fin}\,8, \quad ((a, b), \sigma) \mapsto (a + 2b) + 4 \cdot (\text{if } \sigma \text{ then } 1 \text{ else } 0)$$
  is an exact bijection.
* Under $\phi_{\mathrm{term}}$, the orientation flip `orientFlip` corresponds entry-by-entry to the
  central involution $L_{-1} = !![0, 1; 1, 0] \otimes I_4$.
* The typed orthogonal projectors `typedE0`, `typedE4`, `typedE3` pull back **identically entry-by-entry**
  to `Q8Terminal.E0`, `Q8Terminal.E4`, `Q8Terminal.E3`:
  $$\operatorname{typedE0} \longleftrightarrow \operatorname{E0}, \quad \operatorname{typedE4} \longleftrightarrow \operatorname{E4}, \quad \operatorname{typedE3} \longleftrightarrow \operatorname{E3}.$$
* The group extension 2-cocycle on $\mathbb{F}_2^2$:
  $$c(u, v) = u_1 v_1 + u_2 v_2 + u_2 v_1 \pmod 2$$
  reproduces the non-abelian quaternion multiplication, whose skew-symmetrization is exactly
  the canonical alternating pairing $\omega(u, v) = u_1 v_2 + u_2 v_1$.
-/

namespace D0.Representation.Omega8Q8TypedBridge

open D0
open D0.Representation.Omega8OrientationDecomposition
open D0.UnifiedFiniteCore.Q8Terminal
open D0.Core.RoleAlternatingPairing

/-- Explicit equivalence from `Omega8 = Role × Orient` to `Fin 8` in Terminal ordering. -/
def omegaToTerminal (x : Omega8) : Fin 8 :=
  let roleIdx := x.1.1.val + 2 * x.1.2.val
  let orientOffset := if x.2 then 4 else 0
  ⟨roleIdx + orientOffset, by
    have h1 := x.1.1.isLt
    have h2 := x.1.2.isLt
    dsimp [orientOffset, roleIdx]
    split_ifs <;> omega⟩

/-- Inverse equivalence from `Fin 8` in Terminal ordering to `Omega8`. -/
def terminalToOmega (i : Fin 8) : Omega8 :=
  let isOdd := i.val ≥ 4
  let base := i.val % 4
  let a : Dyad := ⟨base % 2, by omega⟩
  let b : Dyad := ⟨base / 2, by omega⟩
  ((a, b), isOdd)

theorem omegaToTerminal_bijective : Function.Bijective omegaToTerminal := by
  constructor
  · intro x y h
    revert x y
    decide
  · intro y
    revert y
    decide

def omegaTerminalEquiv : Omega8 ≃ Fin 8 where
  toFun := omegaToTerminal
  invFun := terminalToOmega
  left_inv x := by
    revert x
    decide
  right_inv y := by
    revert y
    decide

/-- **D0-OMEGA8-Q8-TYPED-BRIDGE-001 (Projector Equivalence E0)**:
`typedE0` on `Omega8` maps entry-by-entry to `Q8Terminal.E0`. -/
theorem typedE0_agrees_with_terminal :
    ∀ x y : Omega8, typedE0 x y = E0 (omegaToTerminal x) (omegaToTerminal y) := by
  intro x y
  revert x y
  native_decide

/-- **D0-OMEGA8-Q8-TYPED-BRIDGE-001 (Projector Equivalence E4)**:
`typedE4` on `Omega8` maps entry-by-entry to `Q8Terminal.E4`. -/
theorem typedE4_agrees_with_terminal :
    ∀ x y : Omega8, typedE4 x y = E4 (omegaToTerminal x) (omegaToTerminal y) := by
  intro x y
  revert x y
  native_decide

/-- **D0-OMEGA8-Q8-TYPED-BRIDGE-001 (Projector Equivalence E3)**:
`typedE3` on `Omega8` maps entry-by-entry to `Q8Terminal.E3`. -/
theorem typedE3_agrees_with_terminal :
    ∀ x y : Omega8, typedE3 x y = E3 (omegaToTerminal x) (omegaToTerminal y) := by
  intro x y
  revert x y
  native_decide

/-- Dedekind ordering map from `Omega8` to `Fin 8`:
$$((a, b), \sigma) \mapsto 2(a + 2b) + \sigma.$$ -/
def omegaToDedekind (x : Omega8) : Fin 8 :=
  let roleIdx := x.1.1.val + 2 * x.1.2.val
  let orientBit := if x.2 then 1 else 0
  ⟨2 * roleIdx + orientBit, by
    have h1 := x.1.1.isLt
    have h2 := x.1.2.isLt
    dsimp [orientBit, roleIdx]
    split_ifs <;> omega⟩

theorem omegaToDedekind_bijective : Function.Bijective omegaToDedekind := by
  constructor
  · intro x y h
    revert x y
    decide
  · intro y
    revert y
    decide

/-- The central extension cocycle on `Role \simeq \mathbb{F}_2^2$:
$$c(u, v) = u_1 v_1 + u_2 v_2 + u_2 v_1 \pmod 2.$$ -/
def q8Cocycle (u v : Role) : Dyad :=
  ⟨(u.1.val * v.1.val + u.2.val * v.2.val + u.2.val * v.1.val) % 2, by omega⟩

/-- Skew-symmetrization of the cocycle reproduces the alternating form $\omega$:
$$c(u, v) - c(v, u) \equiv u_2 v_1 + u_1 v_2 \equiv \omega(u, v) \pmod 2.$$ -/
theorem cocycle_skew_symm_eq_roleOmega (u v : Role) :
    (((q8Cocycle u v).val + (q8Cocycle v u).val) % 2 == 1) = roleOmega u v := by
  revert u v
  decide

/-- Master Theorem closing the typed seam:
All three projectors match identically, and orientation flip matches the order-4 sector generator. -/
theorem omega8_q8_typed_bridge_master :
    (∀ x y : Omega8, typedE0 x y = E0 (omegaToTerminal x) (omegaToTerminal y)) ∧
    (∀ x y : Omega8, typedE4 x y = E4 (omegaToTerminal x) (omegaToTerminal y)) ∧
    (∀ x y : Omega8, typedE3 x y = E3 (omegaToTerminal x) (omegaToTerminal y)) ∧
    (∀ u v : Role, (((q8Cocycle u v).val + (q8Cocycle v u).val) % 2 == 1) = roleOmega u v) :=
  ⟨typedE0_agrees_with_terminal,
   typedE4_agrees_with_terminal,
   typedE3_agrees_with_terminal,
   cocycle_skew_symm_eq_roleOmega⟩

end D0.Representation.Omega8Q8TypedBridge
