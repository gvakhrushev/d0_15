import D0.TheoremLedger.ClaimMap

/-!
# Historical release-ledger smoke tests

These declarations check only their explicitly displayed metadata propositions
(a tuple identity, a nonempty list and `True`). They are not theorem-owner
binding, proof-closure, bridge-discharge or physical-release certificates.
`claims.csv` retains independent proof/release axes; actual compilation and
scientific scope review are separate requirements. Names are preserved for
registry compatibility.
-/

namespace D0

def releaseHasM1Claims : Prop :=
  ("D0-FOUND-001", "D0-PHI-HURWITZ-001", "D0-PHASE-UNFOLD-002") =
  ("D0-FOUND-001", "D0-PHI-HURWITZ-001", "D0-PHASE-UNFOLD-002")

theorem release_m1_claims_present : releaseHasM1Claims := by
  rfl

def LeanCoreReleaseCandidate : Prop :=
  claimMap ≠ []

theorem lean_core_release_candidate : LeanCoreReleaseCandidate := by
  exact claimMap_nonempty

def BridgeAssumptionsExplicit : Prop := True

theorem lean_bridge_assumptions_explicit : BridgeAssumptionsExplicit := by
  trivial

end D0
