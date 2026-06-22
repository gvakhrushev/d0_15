import D0.UnifiedFiniteCore.Q8Terminal
import D0.UnifiedFiniteCore.TerminalReturn
import D0.UnifiedFiniteCore.PhiReplication
import D0.Integration.V15.RawZone
import Mathlib.Tactic

/-!
# D0-v15 Unified finite-core theorem — the continuous chain

`K(9,11,13) → 𝒲 → (Q₉,Q₁₁,Q₁₃) → Q₈ Fourier (E₀,E₄,E₃) → 𝓗_term → U_E → F_term → W_eff → G_ℓ^fb → 𝒜_n`.

**Status: CONDITIONAL-EXTENSION (a constructed admissible object).** This is ONE explicit member of the
edge-cover holonomy family (the prior v15 audit classified the physical edge cover `CONDITIONAL`,
`D0-EDGE-COVER-FAMILY-001`): the holonomy `λ`, the balanced two-port feedback `R_*`, and the line-graph
contact are *chosen*, not forced by frozen data. The chain's internal identities are nonetheless exact and
machine-checked. **No physical lepton masses / charges / redshift / EOS are claimed** (firewall).

This module collects the parts proved decidably in Lean. The rational-function links of the chain
(`det(I−zU_term)`, the Feshbach factors `det(I−zW_μ)=(1+λz⁴)²/(1−λz⁴/4)`,
`det(I−zW_τ)=(1+√2λz³+λ²z⁶)/(1−λz³/(2√2))`, the dressed Green kernel
`G_ℓ^fb = Q₉/(1−z) + Q₁₁/(1+λz⁴) + (1+λz³/√2)/(1+√2λz³+λ²z⁶)·Q₁₃`, and the feedback law `F_term = ½P_br`)
are verified exactly — symbolically and on the real 359-edge graph — in
`05_CERTS/verify_unified_backbone.py` and `05_CERTS/verify_unified_feedback.py`.
-/

namespace D0.UnifiedFiniteCore

open scoped goldenRatio

/-- **D0-UNIFIED-EDGE-SPINE-001 (CONDITIONAL-EXTENSION).** The decidable spine of the unified chain:
1. the `Q₈` terminal Fourier system has the branch-order signature `(1,4,3)` (= `(tr E₀, tr E₄, tr E₃)`);
2. the terminal return sectors have exact orders `4` and `3`;
3. the raw zone current `i[D,A]` satisfies `comm³ = −2840·comm` (spectrum `{0,±2√710}`, from `RawZone`);
4. the Fibonacci replication obeys `A_{n+2}=A_{n+1}+A_n` with the Pisot correction
   `A_{n+1}−φA_n = ψⁿA₁`, `|ψ|<1`.
The branch orders `(1,4,3)` thus appear simultaneously in the `Q₈` Fourier ranks and the return orders. -/
theorem unified_finite_core (A1 : ℝ) (n : ℕ) :
    -- §3 Q₈ branch-order signature (1,4,3)
    (Q8Terminal.E0.trace = 1 ∧ Q8Terminal.E4.trace = 4 ∧ Q8Terminal.E3.trace = 3) ∧
    (Q8Terminal.E0 + Q8Terminal.E4 + Q8Terminal.E3 = (1 : Matrix (Fin 8) (Fin 8) ℚ)) ∧
    -- §5/§6 terminal return orders 4 and 3
    (TerminalReturn.Umu ^ 4 = 1 ∧ TerminalReturn.Utau ^ 3 = 1) ∧
    -- §2 raw zone current annihilator (spectrum {0,±2√710})
    (D0.Integration.V15.RawZone.comm * D0.Integration.V15.RawZone.comm *
        D0.Integration.V15.RawZone.comm = (-2840 : ℤ) • D0.Integration.V15.RawZone.comm) ∧
    -- §11 Fibonacci/Pisot replication
    (PhiReplication.A A1 (n + 2) = PhiReplication.A A1 (n + 1) + PhiReplication.A A1 n ∧
      PhiReplication.A A1 (n + 1) - φ * PhiReplication.A A1 n = ψ ^ n * A1 ∧ |ψ| < 1) :=
  ⟨Q8Terminal.branch_orders, Q8Terminal.fourier_complete,
    ⟨TerminalReturn.Umu_order4, TerminalReturn.Utau_order3⟩,
    D0.Integration.V15.RawZone.zone_annihilator,
    PhiReplication.phi_replication A1 n⟩

end D0.UnifiedFiniteCore
