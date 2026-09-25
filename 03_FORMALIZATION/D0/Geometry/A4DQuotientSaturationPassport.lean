import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Quotient.Basic
import Mathlib.Tactic
import D0.Geometry.A4DRelativeAEComparisonSpan

/-!
# Same-fibre quotient saturation passport

Lean owner for the finite linear-algebra quotient-repair layer isolated by
research PR #128 / `MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md` §11.

For synthesis maps `B, S : E →ₗ[ℝ] V` and a candidate quotient kernel
`W ≤ V`, the same-fibre quotient relation is a graph if and only if

```
S(B⁻¹ W) ⊆ W.
```

For a supplied linear transport `P`, quotient transport between kernels
`W'` and `W` exists exactly when `P` carries `W'` onto `W`, and labelled-loop
endpoint independence requires `(P - id)(V) ⊆ W`.

The constructive saturation iteration beginning from a loop-coinvariant seed
is monotone, stabilizes in finite dimension, and is the least closed family
containing that seed. No physical observer / readout interpretation is
assigned to the resulting quotient.
-/

namespace D0.Geometry.A4DQuotientSaturationPassport

open D0.Geometry.A4DRelativeAEComparisonSpan

noncomputable section

variable {E V : Type*} [AddCommGroup E] [Module ℝ E]
  [AddCommGroup V] [Module ℝ V]

/-! ## Same-fibre graph criterion (11.1) -/

/-- Coefficient preimage `B⁻¹ W = { c | B c ∈ W }`. -/
abbrev preimageSubmodule (B : E →ₗ[ℝ] V) (W : Submodule ℝ V) : Submodule ℝ E :=
  W.comap B

/-- Induced vertical image `S(B⁻¹ W)`. -/
abbrev inducedImage (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) : Submodule ℝ V :=
  (W.comap B).map S

/-- Same-fibre graph closure: `S(B⁻¹ W) ⊆ W`. -/
def SameFibreGraphClosed (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) : Prop :=
  inducedImage B S W ≤ W

theorem sameFibreGraphClosed_iff_mem
    (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) :
    SameFibreGraphClosed B S W ↔ ∀ c : E, B c ∈ W → S c ∈ W := by
  constructor
  · intro h c hc
    exact h (Submodule.mem_map_of_mem (by simpa [preimageSubmodule] using hc))
  · intro h v hv
    rcases (Submodule.mem_map.mp hv) with ⟨c, hc, rfl⟩
    exact h c (by simpa [preimageSubmodule] using hc)

/-- Quotient pair `(q ∘ B, q ∘ S)` with `q : V → V ⧸ W`. -/
def quotientPair (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) :
    E →ₗ[ℝ] (V ⧸ W) × (V ⧸ W) :=
  LinearMap.prod (W.mkQ.comp B) (W.mkQ.comp S)

/-- Functional dependence of the quotient relation on the first coordinate. -/
def QuotientRelationIsGraph (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) : Prop :=
  ∀ c₁ c₂ : E,
    W.mkQ (B c₁) = W.mkQ (B c₂) → W.mkQ (S c₁) = W.mkQ (S c₂)

/-- Boxed (11.1): same-fibre quotient graph iff `S(B⁻¹ W) ⊆ W`. -/
theorem quotientRelationIsGraph_iff_sameFibreGraphClosed
    (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) :
    QuotientRelationIsGraph B S W ↔ SameFibreGraphClosed B S W := by
  constructor
  · intro h
    rw [sameFibreGraphClosed_iff_mem]
    intro c hc
    have hq : W.mkQ (S c) = W.mkQ (S (0 : E)) :=
      h c 0 (by
        simp only [map_zero]
        exact (Submodule.Quotient.mk_eq_zero W).mpr hc)
    have hq0 : W.mkQ (S c) = 0 := by
      simpa [map_zero] using hq
    exact (Submodule.Quotient.mk_eq_zero W).mp hq0
  · intro h c₁ c₂ hq
    have hdiff : B (c₁ - c₂) ∈ W := by
      have : W.mkQ (B c₁ - B c₂) = 0 := by
        simpa [map_sub] using sub_eq_zero.mpr hq
      exact (Submodule.Quotient.mk_eq_zero W).mp (by simpa [map_sub] using this)
    have hS : S (c₁ - c₂) ∈ W :=
      (sameFibreGraphClosed_iff_mem B S W).1 h (c₁ - c₂) hdiff
    have : W.mkQ (S c₁ - S c₂) = 0 :=
      (Submodule.Quotient.mk_eq_zero W).mpr (by simpa [map_sub] using hS)
    exact sub_eq_zero.mp (by simpa [map_sub] using this)

/-! ## Quotient transport and loop coinvariants (11.2) -/

/-- Quotient transport of kernels exists for `P` iff `P` carries `W'` onto `W`. -/
def QuotientTransportCompatible (P : V →ₗ[ℝ] V)
    (W' W : Submodule ℝ V) : Prop :=
  W'.map P = W

theorem quotientTransportCompatible_iff
    (P : V →ₗ[ℝ] V) (W' W : Submodule ℝ V) :
    QuotientTransportCompatible P W' W ↔
      W'.map P ≤ W ∧ W ≤ W'.map P := by
  simp [QuotientTransportCompatible, le_antisymm_iff]

/-- Loop coinvariant condition: `(P - I)(V) ⊆ W`. -/
def LoopCoinvariant (P : V →ₗ[ℝ] V) (W : Submodule ℝ V) : Prop :=
  LinearMap.range (P - LinearMap.id) ≤ W

theorem loopCoinvariant_iff_mem (P : V →ₗ[ℝ] V) (W : Submodule ℝ V) :
    LoopCoinvariant P W ↔ ∀ v : V, P v - v ∈ W := by
  constructor
  · intro h v
    exact h ⟨v, by simp [LinearMap.sub_apply]⟩
  · intro h x hx
    rcases hx with ⟨v, rfl⟩
    simpa [LinearMap.sub_apply] using h v

/-- Coinvariant defect spanned by a family of loop operators. -/
def coinvariantDefect {ι : Type*} (P : ι → V →ₗ[ℝ] V) : Submodule ℝ V :=
  ⨆ i : ι, LinearMap.range (P i - LinearMap.id)

theorem coinvariantDefect_le_of_loopCoinvariant {ι : Type*}
    (P : ι → V →ₗ[ℝ] V) (W : Submodule ℝ V)
    (h : ∀ i, LoopCoinvariant (P i) W) :
    coinvariantDefect P ≤ W := by
  refine iSup_le ?_
  intro i
  exact h i

/-! ## Finite saturation (11.3) -/

/-- One saturation step: `W ↦ W ⊔ S(B⁻¹ W)`. -/
def saturateStep (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) : Submodule ℝ V :=
  W ⊔ inducedImage B S W

theorem le_saturateStep (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V) :
    W ≤ saturateStep B S W :=
  le_sup_left

theorem saturateStep_mono (B S : E →ₗ[ℝ] V) {W₁ W₂ : Submodule ℝ V}
    (h : W₁ ≤ W₂) :
    saturateStep B S W₁ ≤ saturateStep B S W₂ := by
  refine so_le_sup h ?_
  refine Submodule.map_mono ?_
  exact Submodule.comap_mono h

theorem le_saturateStepFamily {ι : Type*} (B S : ι → E →ₗ[ℝ] V)
    (W : Submodule ℝ V) :
    W ≤ saturateStepFamily B S W :=
  le_sup_left

/-- Iteration of a single-site saturation step. -/
def saturateIter (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) : ℕ → Submodule ℝ V
  | 0 => W0
  | n + 1 => saturateStep B S (saturateIter B S W0 n)

theorem saturateIter_zero (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) :
    saturateIter B S W0 0 = W0 := rfl

theorem saturateIter_succ (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) (n : ℕ) :
    saturateIter B S W0 (n + 1) = saturateStep B S (saturateIter B S W0 n) := rfl

theorem saturateIter_mono_succ (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) (n : ℕ) :
    saturateIter B S W0 n ≤ saturateIter B S W0 (n + 1) := by
  simpa [saturateIter_succ] using le_saturateStep B S (saturateIter B S W0 n)

theorem saturateIter_mono (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V)
    {m n : ℕ} (hmn : m ≤ n) :
    saturateIter B S W0 m ≤ saturateIter B S W0 n := by
  induction n, hmn using Nat.le_induction with
  | base => exact le_rfl
  | succ n _ ih => exact ih.trans (saturateIter_mono_succ B S W0 n)

theorem saturateStep_eq_self_of_sameFibreGraphClosed
    (B S : E →ₗ[ℝ] V) (W : Submodule ℝ V)
    (h : SameFibreGraphClosed B S W) :
    saturateStep B S W = W := by
  simpa [saturateStep] using (sup_eq_left.mpr h)

theorem saturateIter_le_of_closed
    (B S : E →ₗ[ℝ] V) (W0 W : Submodule ℝ V)
    (hW0 : W0 ≤ W) (hclosed : SameFibreGraphClosed B S W) :
    ∀ n, saturateIter B S W0 n ≤ W := by
  intro n
  induction n with
  | zero => simpa [saturateIter_zero] using hW0
  | succ n ih =>
    rw [saturateIter_succ, saturateStep]
    exact so_le ih ((Submodule.map_mono (Submodule.comap_mono ih)).trans hclosed)

theorem exists_saturateIter_eq_succ [FiniteDimensional ℝ V]
    (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) :
    ∃ n : ℕ, saturateIter B S W0 (n + 1) = saturateIter B S W0 n := by
  classical
  by_contra h
  push Not at h
  have hlt : ∀ n,
      Module.finrank ℝ (saturateIter B S W0 n) <
        Module.finrank ℝ (saturateIter B S W0 (n + 1)) := by
    intro n
    refine Submodule.finrank_lt_finrank_of_lt ?_
    exact lt_of_le_of_ne (saturateIter_mono_succ B S W0 n) (h n).symm
  have hge : ∀ n : ℕ, n ≤ Module.finrank ℝ (saturateIter B S W0 n) := by
    intro n
    induction n with
    | zero => exact Nat.zero_le _
    | succ n ih =>
      exact (Nat.succ_le_succ ih).trans (Nat.succ_le_of_lt (hlt n))
  set N := Module.finrank ℝ V
  have hleN : Module.finrank ℝ (saturateIter B S W0 (N + 1)) ≤ N :=
    Submodule.finrank_le _
  have : N + 1 ≤ N := (hge (N + 1)).trans hleN
  exact (Nat.not_succ_le_self N this).elim

theorem saturateIter_eq_succ_of_finrank_eq [FiniteDimensional ℝ V]
    (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) (n : ℕ)
    (hdim : Module.finrank ℝ (saturateIter B S W0 (n + 1)) =
      Module.finrank ℝ (saturateIter B S W0 n)) :
    saturateIter B S W0 (n + 1) = saturateIter B S W0 n := by
  refine (Submodule.eq_of_le_of_finrank_eq
    (saturateIter_mono_succ B S W0 n) hdim.symm).symm

theorem sameFibreGraphClosed_of_saturateIter_fixed
    (B S : E →ₗ[ℝ] V) (W0 : Submodule ℝ V) (n : ℕ)
    (hfix : saturateIter B S W0 (n + 1) = saturateIter B S W0 n) :
    SameFibreGraphClosed B S (saturateIter B S W0 n) := by
  have : saturateStep B S (saturateIter B S W0 n) = saturateIter B S W0 n := by
    simpa [saturateIter_succ] using hfix
  exact (sup_eq_left.mp (by simpa [saturateStep] using this))

theorem saturateIter_minimal
    (B S : E →ₗ[ℝ] V) (W0 W : Submodule ℝ V) (n : ℕ)
    (hW0 : W0 ≤ W) (hclosed : SameFibreGraphClosed B S W) :
    saturateIter B S W0 n ≤ W :=
  saturateIter_le_of_closed B S W0 W hW0 hclosed n

/-- Choosing `W = verticalDefect B S` need not satisfy (11.1). Exact witness
lives in `A4DQuotientSaturationWitness`. -/
def VerticalDefectNotUniversalRepair : Prop :=
  ∃ (B S : LabelCoeff →ₗ[ℝ] LabelCoeff),
    ¬ SameFibreGraphClosed B S (verticalDefect B S)

end

end D0.Geometry.A4DQuotientSaturationPassport
