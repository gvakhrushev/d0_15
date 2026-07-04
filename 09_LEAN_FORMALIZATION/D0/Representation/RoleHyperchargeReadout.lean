import Mathlib.Tactic
import D0.Representation.RoleRealStructureNoGo

/-!
# Φ_Y — hypercharge readout on the six role blocks (reduces to J_role)

The six role blocks have ranks `(R₆,R₂,R_{3,+},R_{1,+},R_{3,-},R_{1,-}) = (6,2,3,1,3,1)`.
A hypercharge readout `Φ_Y` assigns one charge per block.  Both the SM hypercharge `Y` and
`B−L` are grav- and cubic-anomaly-free on these six blocks, so the readout is underdetermined
exactly as in `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` (A2): `B−L` is removed only by
declaring the singlet block `R_{1,-} = ν^c` uncharged, which needs the charge-conjugate
pairing `(R_{1,+},R_{1,-})` — i.e. `J_role`, which is a NO-GO.

Hence `Φ_Y` is NOT forced; it inherits the residual `PRIM-FINITE-SPECTRAL-TRIPLE-REP`.
Finite arithmetic verified in `D0_ROLE_OPERATORS_CERTIFICATE.py`.
-/

namespace D0.Representation.RoleHyperchargeReadout

/-- Ranks of the six role blocks in order `R₆,R₂,R₃₊,R₁₊,R₃₋,R₁₋`. -/
def blockRanks : List ℚ := [6, 2, 3, 1, 3, 1]

/-- Candidate SM hypercharge per block. -/
def Yrow : List ℚ := [1/6, -1/2, -2/3, 1, 1/3, 0]

/-- `B−L` per block. -/
def BLrow : List ℚ := [1/3, -1, -1/3, 1, -1/3, 1]

-- `decide` cannot kernel-reduce `ℚ` arithmetic on this toolchain (`Rat.add` is
-- irreducible); rational goals below use `norm_num` instead.

/-- Total dimension `6+2+3+1+3+1 = 16` (one SO(10) generation). -/
theorem footprint_sixteen : (blockRanks.sum) = 16 := by
  norm_num [blockRanks]

/-- Weighted (gravitational) anomaly sum `Σ rankᵢ · cᵢ`. -/
def gravSum (c : List ℚ) : ℚ := (List.zipWith (· * ·) blockRanks c).sum

/-- Weighted cubic anomaly sum `Σ rankᵢ · cᵢ³`. -/
def cubicSum (c : List ℚ) : ℚ := (List.zipWith (fun r x => r * x^3) blockRanks c).sum

theorem Y_grav_free : gravSum Yrow = 0 := by
  norm_num [gravSum, blockRanks, Yrow]

theorem Y_cubic_free : cubicSum Yrow = 0 := by
  norm_num [cubicSum, blockRanks, Yrow]

theorem BL_grav_free : gravSum BLrow = 0 := by
  norm_num [gravSum, blockRanks, BLrow]

theorem BL_cubic_free : cubicSum BLrow = 0 := by
  norm_num [cubicSum, blockRanks, BLrow]

/-- `Y` and `B−L` differ (independent readouts), e.g. on the singlet `ν^c` block (index 5). -/
theorem Y_ne_BL : Yrow ≠ BLrow := by
  norm_num [Yrow, BLrow]

/-- **Φ_Y NO-GO.** Both `Y` and `B−L` are anomaly-free on the six role blocks and differ,
so the readout is underdetermined; removing `B−L` needs the `(R₁₊,R₁₋)` charge-conjugate
pairing, which is the role real structure — a NO-GO. -/
theorem phi_Y_underdetermined :
    gravSum Yrow = 0 ∧ cubicSum Yrow = 0 ∧ gravSum BLrow = 0 ∧ cubicSum BLrow = 0
      ∧ Yrow ≠ BLrow :=
  ⟨Y_grav_free, Y_cubic_free, BL_grav_free, BL_cubic_free, Y_ne_BL⟩

end D0.Representation.RoleHyperchargeReadout
