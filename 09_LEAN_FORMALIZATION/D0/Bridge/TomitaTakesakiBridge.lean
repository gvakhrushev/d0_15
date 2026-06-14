namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the Tomita–Takesaki modular theory (Tomita 1967; Takesaki, *Tomita's
theory of modular Hilbert algebras*, LNM 128, 1970) together with Connes' uniqueness. The
classical theorem: a von Neumann algebra with a cyclic and separating vector carries a
canonical one-parameter modular automorphism group `σ_t = Δ^{it}·Δ^{-it}`; the state is KMS
w.r.t. `σ_t`, and (Connes, Radon–Nikodym cocycle) the modular flow is unique up to inner
automorphism. This owns the D0 link "time = modular flow" (thermal time; BOOK_06 §06.7/§06.30a):
time is not an external catalogue parameter but is forced by the (algebra, state) pair — in
accord with M1. D0 proves only the Pisot/symbolic structure of the time layer
(`D0-TIME-2D-PISOT-001`); the modular-flow identification is assumed, not re-proved. -/
structure TomitaModularFlow where
  /-- D0-side anchor: the time layer is a single Pisot/symbolic automorphism (no external clock). -/
  d0PisotTimeLayer : Prop
  /-- External: time = the canonical modular automorphism flow (unique up to inner). -/
  timeEqualsModularFlow : Prop
  d0Witness : d0PisotTimeLayer
  cited : timeEqualsModularFlow

end BridgeAssumption

abbrev TomitaModularFlow := BridgeAssumption.TomitaModularFlow

/-- Conditional bridge: given the D0 Pisot time layer and Tomita–Takesaki/Connes modular
uniqueness (assumed), time is the canonical modular flow. Proved ONLY relative to the declared
external assumption (`ASSUMP-TOMITA-TAKESAKI`). -/
theorem tomita_modular_flow_conditional (h : TomitaModularFlow) :
    h.d0PisotTimeLayer ∧ h.timeEqualsModularFlow :=
  ⟨h.d0Witness, h.cited⟩

end D0.Bridge
