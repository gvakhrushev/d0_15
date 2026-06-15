namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the **Frobenius theorem** (G. Frobenius, *Über lineare Substitutionen und
bilineare Formen*, J. Reine Angew. Math. 84 (1878) 1–63; "1877"): the only finite-dimensional
associative division algebras over `ℝ` are `ℝ` (dim 1), `ℂ` (dim 2), `ℍ` (dim 4). D0 proves only
the finite quaternion content (`D0-FROBENIUS-DIVISION-3D-001`: the Hamilton relations and that the
imaginary part of `ℍ` is 3-dimensional = rank-3 = space). The classification itself — that there
is NO other associative division algebra, and in particular none of dimension 3 — is the external
theorem, assumed, not re-proved. The `ℍ→𝕆` octet step is a separate HYP and is not part of this
assumption. -/
structure FrobeniusDivision3D where
  /-- The only finite-dim associative division algebras over `ℝ` are `ℝ`, `ℂ`, `ℍ`. -/
  onlyRealComplexQuaternion : Prop
  cited : onlyRealComplexQuaternion

end BridgeAssumption

abbrev FrobeniusDivision3D := BridgeAssumption.FrobeniusDivision3D

end D0.Bridge
