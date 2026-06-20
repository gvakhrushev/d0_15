import D0.Matter.HiggsPhasonOrbitNoGo

/-!
# D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001 — condensation route does not start

Maximality strengthening of `D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001`. A finite Higgs condensation needs a
nontrivial conjugation orbit `Qₙ = Tⁿ Q₀ T⁻ⁿ`, which requires `[T, Q₀] ≠ 0` (a non-commuting scalar/
archive action). But **every present-core frozen projector is a function (polynomial) of the return
operator `T`**, and therefore commutes with `T`:

- `tPoly_commutes`: for ALL `a b`, the present-core projector `a•1 + b•T` commutes with `T`;
- a commuting `Q₀` gives a constant orbit (`commuting_projector_has_trivial_orbit`) — no double-well, no
  condensation.

A non-commuting `Q₀` exists as a matrix (witness `Qnc = !![1,0;0,0]`, `[T,Qnc] ≠ 0`), but it is NOT a
polynomial in `T` — i.e. NOT a present-core frozen object; supplying it is a NEW independently-forced
primitive `(U, Q₀, Π_H)` (extension), not a present-core theorem. Hence the condensation route does not
start from present-core. Closed-negative; matches the named blocker `D0-HIGGS-FINITE-CONDENSATION-OWNER`.
-/

namespace D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo

open D0.Matter.HiggsReturnQuotientAction D0.Matter.HiggsPhasonOrbitNoGo

/-- **Every present-core (polynomial-in-`T`) projector commutes with `T`**: for all `a b : ZMod 44`,
`a•1 + b•T` commutes with `T`. The whole present-core scalar/archive class is commuting. -/
theorem tPoly_commutes (a b : ZMod 44) :
    Commute T (a • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) + b • T) :=
  Commute.add_right ((Commute.one_right T).smul_right a) ((Commute.refl T).smul_right b)

/-- A concrete non-commuting witness `Qnc = !![1,0;0,0]`: `[T, Qnc] ≠ 0`. This is the kind of object
condensation needs — and it is NOT a polynomial in `T` (not present-core). -/
def Qnc : Matrix (Fin 2) (Fin 2) (ZMod 44) := !![1, 0; 0, 0]

theorem Qnc_not_commute : ¬ Commute T Qnc := by
  unfold Commute SemiconjBy T Qnc; native_decide

/-- **D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001 (closed-negative).** Every present-core
projector (polynomial in `T`) commutes with `T` and hence gives a constant orbit (no double-well / no
condensation); the condensation route requires a non-commuting `Q₀` (witness `Qnc`, `[T,Qnc]≠0`), which is
NOT present-core (not a polynomial in `T`). The route does not start from present-core — a new
independently-forced `(U,Q₀,Π_H)` is required. -/
theorem higgs_condensation_present_core_maximality_nogo :
    (∀ a b : ZMod 44, Commute T (a • (1 : Matrix (Fin 2) (Fin 2) (ZMod 44)) + b • T))
      ∧ (∀ Q0 : Matrix (Fin 2) (Fin 2) (ZMod 44), Commute T Q0 → ∀ n, Commute (T ^ n) Q0)
      ∧ ¬ Commute T Qnc :=
  ⟨tPoly_commutes, fun Q0 h n => commuting_projector_has_trivial_orbit Q0 h n, Qnc_not_commute⟩

end D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo
