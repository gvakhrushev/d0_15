/-!
# ASSUMP-KERNEL-CHARGE-LOCALIZATION — the sterile-state charge-localization bridge

The gauged `U(1)` charge **vanishes on the sterile state** `ν^c` (equivalently `ν_R ∈ ker(A)`, the
30-dimensional zone-balanced archive kernel of `D0-TRIPARTITE-IMAGE-KERNEL-001` / `KernelZoneSplit`). Under
the D0 graph→physics map this is the **R2 graph→physics localization**, which is a **MECH-LIMIT, not a forced
identity** (`D0-GRAPH-SPACE-NO-ISOMETRY-001`). It is therefore carried as an EXPLICIT bridge assumption, never
promoted to Core.

Used by `D0.Matter.HyperchargeBLDirectionBridge.hypercharge_bl_direction_bridge` to collapse the 2-dimensional
anomaly-free family `span{Y, B−L}` to the unique hypercharge ray `span{Y}`. **Failure meaning:** if `ν_R` is
not kernel-localized, `B−L` stays gaugeable and the hypercharge direction is not fixed (the 2-dim freedom of
`D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` returns). Structural payoff: this bridge **is** the R2 localization,
so the hypercharge-direction obligation and the R2 MECH-LIMIT are one obligation, not two.
-/

namespace D0.Bridge

namespace BridgeAssumption

/-- The kernel-charge-localization bridge: a `Prop` carrier (the gauged charge vanishes on `ν^c`). -/
structure KernelChargeLocalizationAssumption where
  statement : Prop
  cited : statement

end BridgeAssumption

abbrev KernelChargeLocalizationAssumption :=
  BridgeAssumption.KernelChargeLocalizationAssumption

end D0.Bridge
