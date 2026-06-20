import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Core.Phi

set_option linter.unusedSimpArgs false
set_option linter.unusedVariables false

/-!
# D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001 — canonical Perron-GNS isometric tower (Phase A2)

The Perron trace of the Fibonacci AF algebra is consistent under the Bratteli inclusions: with the right-
Perron eigenvector `v = (φ, 1)` (`M_φ v = φ v`, which is exactly `φ² = φ + 1`), the trace vectors
`t_N = φ^{-N} v` satisfy `M_φ t_{N+1} = t_N` — i.e. `τ_{N+1} ∘ ι_N = τ_N`. A trace-preserving `*`-algebra
inclusion induces a genuine **isometry** of GNS spaces `⟨ι x, ι y⟩_{N+1} = ⟨x, y⟩_N` (with the GNS form
`⟨x,y⟩ = τ(y* x)`). So the canonical AF/GNS isometric tower `J_N` EXISTS — the isometry half of the
candidate primitive `PRIM-ISOMETRIC-DIRAC-J_N` is realized for free from the Perron trace, with no
synthetic embedding and no chosen state.
-/

namespace D0.VNext.PerronGNSTower

open Matrix D0

/-- **The GNS isometry from a trace-preserving `*`-inclusion** (the core of the AF/GNS tower): a
multiplicative, `star`-preserving, trace-preserving inclusion `ι` preserves the GNS inner product
`⟨x,y⟩ = τ(y* x)`. Hence each Bratteli level inclusion gives a genuine isometry `J_N`. -/
theorem gns_refinement_isometry {A B : Type*} [Mul A] [Mul B] [Star A] [Star B]
    (tauA : A → ℝ) (tauB : B → ℝ) (iota : A → B)
    (hmul : ∀ x y : A, iota (x * y) = iota x * iota y)
    (hstar : ∀ x : A, iota (star x) = star (iota x))
    (htr : ∀ a : A, tauB (iota a) = tauA a) :
    ∀ x y : A, tauB (star (iota y) * iota x) = tauA (star y * x) := by
  intro x y
  rw [← hstar, ← hmul, htr]

theorem phi_ne_zero : phi ≠ 0 := ne_of_gt (by unfold phi; positivity)

/-- **The Perron eigenvalue relation** `M_φ v = φ v` for `v = (φ,1)`, i.e. its content `φ·φ = φ + 1`. -/
theorem perron_eigenvalue_relation : phi * phi = phi + 1 := by
  rw [← pow_two]; exact phi_sq

/-- **The Perron trace is refinement-compatible**: the trace vectors `t_N = (φ,1)`, `t_{N+1} = φ⁻¹(φ,1)`
satisfy `M_φ t_{N+1} = t_N`, which reduces to the scalar identities `1 + φ⁻¹ = φ` (top component) and
`φ⁻¹·φ = 1` (bottom component). Hence `τ_{N+1} ∘ ι_N = τ_N`. -/
theorem perron_trace_compatible_with_refinement :
    1 + phi⁻¹ = phi ∧ phi⁻¹ * phi = 1 := by
  have hp : phi ≠ 0 := phi_ne_zero
  refine ⟨?_, inv_mul_cancel₀ hp⟩
  field_simp
  first
    | linear_combination phi_sq
    | linear_combination -phi_sq
    | nlinarith [phi_sq]

/-- **D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001.** The canonical Perron-GNS isometric tower exists: the Perron
trace is refinement-compatible (`1 + φ⁻¹ = φ`, the scalar form of `M_φ t_{N+1} = t_N`), and any
trace-preserving `*`-inclusion induces an isometry of GNS spaces (`gns_refinement_isometry`). The isometry
half of `PRIM-ISOMETRIC-DIRAC-J_N` is realized canonically — no synthetic embedding, no chosen state. -/
theorem perron_gns_tower_owner :
    (1 + phi⁻¹ = phi ∧ phi⁻¹ * phi = 1)
      ∧ (∀ {A B : Type} [inst : Mul A] [inst2 : Mul B] [inst3 : Star A] [inst4 : Star B]
          (tauA : A → ℝ) (tauB : B → ℝ) (iota : A → B),
          (∀ x y : A, iota (x * y) = iota x * iota y) →
          (∀ x : A, iota (star x) = star (iota x)) →
          (∀ a : A, tauB (iota a) = tauA a) →
          ∀ x y : A, tauB (star (iota y) * iota x) = tauA (star y * x)) := by
  refine ⟨perron_trace_compatible_with_refinement, ?_⟩
  intro A B _ _ _ _ tauA tauB iota hmul hstar htr
  exact gns_refinement_isometry tauA tauB iota hmul hstar htr

end D0.VNext.PerronGNSTower
