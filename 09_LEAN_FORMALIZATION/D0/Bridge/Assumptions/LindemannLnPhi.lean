namespace D0.Bridge

namespace BridgeAssumption

/-- **ASSUMP-LINDEMANN-LNPHI** — Lindemann–Weierstrass: for an algebraic `φ ≠ 1`, `ln φ` is
transcendental over ℚ. This classical theorem (Lindemann 1882 / Weierstrass 1885) is absent from
the pinned Mathlib 4.30, which formalizes only the analytic part
(`Mathlib.NumberTheory.Transcendental.Lindemann.AnalyticalPart`). It is carried as one explicit
bridge assumption, never a global `axiom`. The concrete statement `Transcendental ℚ (Real.log φ)`
is threaded as the hypothesis `LindemannLnPhi` in `D0.Spectral.DeltaAlphaResidueBlocked`
(`delta_alpha_residue_route_blocked`); this structure is its canonical bridge-ledger owner. -/
structure LindemannLnPhiAssumption where
  statement : Prop
  cited : statement

end BridgeAssumption

abbrev LindemannLnPhiAssumption := BridgeAssumption.LindemannLnPhiAssumption

end D0.Bridge
