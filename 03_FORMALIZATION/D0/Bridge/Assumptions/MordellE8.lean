namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the `E_8` genus-uniqueness theorem (L. J. Mordell, *The definite quadratic
forms in eight variables with determinant unity*, J. Math. Pures Appl. 17 (1938) 41–46; cf.
Conway–Sloane, *SPLAG*). The classical theorem: `E_8` is the UNIQUE (up to isometry) even
unimodular positive-definite lattice of rank 8. D0 proves only that the specific E8 Gram IS
even and unimodular (`D0-ICOSIAN-E8-GRAM-001`); the uniqueness ("this lattice IS `E_8`") needs
lattice-genus machinery absent from Mathlib and is assumed, not re-proved. -/
structure MordellE8Uniqueness where
  /-- `E_8` is the unique even unimodular positive-definite lattice of rank 8. -/
  uniqueEvenUnimodularRank8 : Prop
  cited : uniqueEvenUnimodularRank8

end BridgeAssumption

abbrev MordellE8Uniqueness := BridgeAssumption.MordellE8Uniqueness

end D0.Bridge
