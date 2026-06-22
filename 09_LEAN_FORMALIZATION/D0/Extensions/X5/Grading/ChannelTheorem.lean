import D0.Extensions.X5.Grading.SymmetryGroups
import Mathlib.Tactic

/-!
# D0-X5-G-CHANNEL-001 — candidate-sector dimension vs N_active (Section 3.3)

CORRECTION to the prior X5-G claim: `p² + q² + 3` is the **candidate-sector dimension**, NOT `N_active`. A real
`N_active` requires the coupling-weighted projector theorem `Tr(c · J_nc† R J_nc · c) > 0` over
response-orthogonal active projectors — which is a PROOF-TARGET, not closed. So no `N_active` value is claimed.
Decision **G2** (finite family): under `U3_inner` the gradings form 4 signature orbits with candidate-sector
dims `{8, 12}`; `Aut_raw` imposes no signature constraint, so no canonical selector exists without the X5-G
contract.
-/

namespace D0.Extensions.X5.Grading

/-- The CANDIDATE-SECTOR dimension of a grading signature `(p,q)` (NOT `N_active`). -/
def candidateSectorDim (p q : ℕ) : ℕ := p * p + q * q + 3

theorem candidate_sector_dims : candidateSectorDim 2 1 = 8 ∧ candidateSectorDim 3 0 = 12 := by decide

-- `N_active` is NOT determined by the candidate-sector dimension: it needs the (unclosed) coupling-weighted
-- channel theorem `Tr(c·J† R J·c) > 0` over response-orthogonal active projectors. It therefore remains a
-- PROOF-TARGET — recorded in prose / the registry, NOT as a vacuous `= true` theorem (would be a stub shell).

/-- **Decision G2 (finite family).** Four `U3_inner` signature orbits; candidate-sector dims `8 ≠ 12`;
`N_active` remains a proof-target (no value claimed — see the comment above). -/
theorem grading_G2_finite_family :
    candidateSectorDim 2 1 = 8 ∧ candidateSectorDim 3 0 = 12 ∧
      candidateSectorDim 2 1 ≠ candidateSectorDim 3 0 ∧ u3SignatureClasses.length = 4 :=
  ⟨candidate_sector_dims.1, candidate_sector_dims.2, by decide, u3_four_signature_classes⟩

end D0.Extensions.X5.Grading
