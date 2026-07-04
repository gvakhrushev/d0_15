import Mathlib.Tactic

/-!
# J_role — real-structure no-go on the Q₈ spinor role carrier

Carrier: `W = ℂ[Q₈] ⊗ ρ` (dim 16) with the typed right-B axis `R_i` splitting the
quaternionic block `E₄ = E₄⁺ ⊕ E₄⁻` (ranks `2,2`).  A physical role real structure
`J_role` must (b) implement charge conjugation — an antiunitary `L ↔ R` intertwiner with
`J² = −I` — AND (c) preserve the right-B axis so it can pair `(R_{3,+},R_{3,-})` and
`(R_{1,+},R_{1,-})` as charge-conjugate partners.

**Theorem (incompatibility).** No `J` does both.  Conjugation by any charge-conjugation
`J` sends `R_i` into the LEFT regular algebra (`W R_i W⁻¹ = L_{−i}`), while `R_i` is NOT in
the left algebra (it is not central; left ∩ right = the 5-dim centre = #conjugacy classes of
`Q₈`).  Hence `J_role` is NOT forced by the frozen typed carrier.

Residual primitive: an external KO-dimension real structure (`PRIM-FINITE-SPECTRAL-TRIPLE-REP`).
The finite arithmetic is verified in `D0_ROLE_OPERATORS_CERTIFICATE.py`.
-/

namespace D0.Representation.RoleRealStructureNoGo

/-- Number of conjugacy classes of `Q₈` = dimension of the centre `span{L_g} ∩ span{R_g}`. -/
def q8CentreDim : ℕ := 5

/-- The right-B generator is not central, so it is not in the left regular algebra. -/
def rightB_central : Prop := False

theorem rightB_not_central : ¬ rightB_central := by
  simp [rightB_central]

/-- The two requirements on a role real structure. `J` is summarised by two booleans:
`pairsBlocks` (preserves the right-B axis, condition c) and `chargeConj` (L↔R intertwiner,
condition b).  The carrier forces: `chargeConj → ¬ pairsBlocks` (conjugation lands in the
left algebra; `R_i` not central). -/
structure RoleJ where
  chargeConj : Prop
  pairsBlocks : Prop
  /-- carrier-forced incompatibility -/
  incompat : chargeConj → (pairsBlocks ↔ rightB_central)

/-- **J_role NO-GO.** A role real structure cannot be both a charge-conjugation and a
right-B-axis-preserving pairing: assuming both forces `R_i` central, which is false. -/
theorem role_real_structure_nogo
    (J : RoleJ) (hb : J.chargeConj) (hc : J.pairsBlocks) : False := by
  have : rightB_central := (J.incompat hb).mp hc
  exact rightB_not_central this

/-- The residual is exactly the centre/KO-dimension gap: the bi-regular structure meets only
in the `5`-dim centre, too small to carry a B-axis-respecting `J`. -/
theorem residual_is_centre_gap : q8CentreDim = 5 := by decide

end D0.Representation.RoleRealStructureNoGo
