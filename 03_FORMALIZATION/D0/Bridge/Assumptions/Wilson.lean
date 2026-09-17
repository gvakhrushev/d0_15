namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of **lattice gauge rigor** (K. Wilson, *Confinement of quarks*, Phys. Rev. D 10
(1974) 2445): non-perturbative gauge theory is rigorously defined ONLY on a finite lattice; a
continuum (`a→0`) definition with a mass gap is the open Yang–Mills Clay problem. D0 uses this to
force finiteness of the carrier (and, with M1 forbidding an exogenous spacing `a`, the unique
self-similar φ-quasicrystal carrier — `D0-LATTICE-FINITENESS-BRIDGE-001`, composing with
`D0-QUASICRYSTAL-CARRIER-FORCING-001`). The lattice-rigor statement and the open continuum limit
are the external owners, assumed, not re-proved. -/
structure WilsonLatticeRigor where
  /-- Non-perturbative gauge theory is rigorously defined only on a finite lattice. -/
  nonperturbativeGaugeOnlyOnFiniteLattice : Prop
  cited : nonperturbativeGaugeOnlyOnFiniteLattice

end BridgeAssumption

abbrev WilsonLatticeRigor := BridgeAssumption.WilsonLatticeRigor

end D0.Bridge
