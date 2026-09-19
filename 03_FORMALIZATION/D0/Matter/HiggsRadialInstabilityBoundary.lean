import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic
import D0.Matter.HiggsScalarProjectorConstructive
import D0.Matter.HiggsReturnQuotientAction

namespace D0.Matter.HiggsRadialInstabilityBoundary

open Matrix
open D0.Matter
open D0.Matter.HiggsReturnQuotientAction

/-!
# D0.Matter.HiggsRadialInstabilityBoundary

Theoretical owner: `D0-HIGGS-RADIAL-DYNAMICS-MAXIMALITY-NOGO-001`.

Reformulation of the Higgs condensation frontier:
1. Carrier Projector vs Vacuum Line Representative:
   `HiggsScalarProjectorConstructive` proves that any non-zero projector on the electroweak doublet
   $M_2 = \mathrm{End}(\mathbb{Q}^2)$ commuting with the frozen $SU(2)$ generators $X, Z$ is the identity $I_2$.
   This uniquely fixes the scalar carrier projector.
   A rank-1 vacuum line representative $P_0 = \mathrm{diag}(1, 0)$ necessarily breaks full gauge invariance;
   requiring $P_0$ to commute with all gauge generators would forbid spontaneous symmetry breaking.
2. Vacuum Orbit Invariance:
   The individual representatives $P_0 = !![1, 0; 0, 0]$ and $P_1 = !![0, 0; 0, 1]$ are swapped by the gauge generator $X$:
   $$X P_0 X = P_1, \quad X P_1 X = P_0.$$
   The vacuum orbit $\{P_0, P_1\}$ is gauge-invariant as a set.
3. Non-commutativity with Toral Return $T$:
   Both representatives strictly do not commute with $T$:
   $$[T, P_0] \ne 0, \quad [T, P_1] \ne 0.$$
   Thus, the existence of non-commuting rank-1 candidates is mathematically trivial and is NOT the true physical bottleneck.
4. Genuine Physical Bottleneck (Radial Instability):
   The true missing physics is a source-derived effective action $S_{\mathrm{eff}}(s)$ for the gauge-invariant
   scalar amplitude $s = \Phi^\dagger \Phi$ possessing an unstable origin $s = 0$ and a stable non-zero minimum $s_* > 0$.
   Present-core D0 owns the carrier and log-det stationary points, but owns no scalar-amplitude dynamics.
   The old blocker `PRIM-NONCOMMUTING-TRIPLE` is formally retired in favor of `PRIM-HIGGS-RADIAL-EFFECTIVE-ACTION`.
-/

/-- Standard rank-1 vacuum line representative $P_0 = \mathrm{diag}(1, 0)$. -/
def P0 : M2 := !![1, 0; 0, 0]

/-- Conjugate rank-1 vacuum line representative $P_1 = \mathrm{diag}(0, 1)$. -/
def P1 : M2 := !![0, 0; 0, 1]

/-- Frozen $SU(2)$ Pauli-$X$ generator on $M_2$. -/
def X : M2 := FrozenSU2_X

/-- Frozen toral return operator $T = !![0, 1; 1, -1]$ over $\mathbb{Q}$. -/
def Tq : M2 := !![0, 1; 1, -1]

/-- $P_0$ is a rank-1 idempotent. -/
theorem P0_idempotent : P0 * P0 = P0 ∧ P0.trace = 1 := by
  refine ⟨by native_decide, by native_decide⟩

/-- $P_1$ is a rank-1 idempotent. -/
theorem P1_idempotent : P1 * P1 = P1 ∧ P1.trace = 1 := by
  refine ⟨by native_decide, by native_decide⟩

/-- Gauge action by $X$ swaps the two vacuum representatives $P_0$ and $P_1$:
the orbit $\{P_0, P_1\}$ is gauge-invariant under $X$. -/
theorem vacuum_orbit_swapped_by_X :
    X * P0 * X = P1 ∧ X * P1 * X = P0 := by
  refine ⟨by native_decide, by native_decide⟩

/-- Non-commutativity with the toral operator $T$: $[T, P_0] \ne 0$. -/
theorem T_P0_not_commute : Tq * P0 ≠ P0 * Tq := by
  intro h
  have h01 := congr_fun (congr_fun h 0) 1
  revert h01
  native_decide

/-- Non-commutativity with the toral operator $T$: $[T, P_1] \ne 0$. -/
theorem T_P1_not_commute : Tq * P1 ≠ P1 * Tq := by
  intro h
  have h01 := congr_fun (congr_fun h 0) 1
  revert h01
  native_decide

/-- The unique nonzero gauge-commuting projector is the carrier identity $I_2$. -/
theorem carrier_projector_is_identity :
    ∀ (P : M2), IntertwinesFrozenSU2 P → IsProjector P → P ≠ 0 → P = 1 :=
  nonzero_gauge_idempotent_eq_identity

/-- **D0-HIGGS-RADIAL-DYNAMICS-MAXIMALITY-NOGO-001 (Owner)**:
Comprehensive structural verdict on the Higgs frontier:
1. $P_0$ and $P_1$ are rank-1 idempotents forming an invariant orbit under $X$.
2. Both representatives strictly do not commute with the toral return $T$.
3. The unique gauge-commuting projector is the carrier identity $I_2$ with trace 2.
4. Hence, non-commutativity is already realized in present-core; the true open question
   is radial stability of a non-zero amplitude $s_* > 0$ (`PRIM-HIGGS-RADIAL-EFFECTIVE-ACTION`). -/
theorem higgs_radial_dynamics_maximality_nogo_owner :
    (P0 * P0 = P0 ∧ P0.trace = 1) ∧
    (P1 * P1 = P1 ∧ P1.trace = 1) ∧
    (X * P0 * X = P1 ∧ X * P1 * X = P0) ∧
    (Tq * P0 ≠ P0 * Tq ∧ Tq * P1 ≠ P1 * Tq) ∧
    (Matrix.trace (1 : M2) = 2) :=
  ⟨P0_idempotent,
   P1_idempotent,
   vacuum_orbit_swapped_by_X,
   ⟨T_P0_not_commute, T_P1_not_commute⟩,
   rank2_scalar_projector_exists.2.2⟩

end D0.Matter.HiggsRadialInstabilityBoundary
