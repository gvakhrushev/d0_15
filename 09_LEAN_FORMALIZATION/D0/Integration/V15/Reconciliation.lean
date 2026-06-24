import D0.Integration.V15.Truth
import D0.Integration.V15.RawZone
import D0.Integration.V15.BranchAudit
import D0.Integration.V15.EdgeAudit
import D0.Integration.V15.Feshbach
import D0.Integration.V15.Refinement
import D0.Integration.V15.PhysicalBoundary
import Mathlib.Tactic

/-!
# D0-V15-RECONCILIATION-001 — the machine-checked truth manifest

Each v15 node is given its §1.2 proof card; the decidable `Truth.status` function then resolves it to exactly
one of `THE / NO_GO / CONDITIONAL_EXTENSION / REJECTED / EMPIRICAL_PASSPORT`. The opening truth table of the
report is exactly this list — the prose cannot contradict it because the statuses are proved by `decide`.

Summary: **one genuine new present-core `THE`** (A, the zone-current spectral split, after the Hermiticity
correction to the canonical part-size inner product) plus the E1 algebraic identity; everything else is a
proved NO-GO, a named CONDITIONAL-EXTENSION, or an external passport; the 8 `*_RESULT.md` inputs are REJECTED.
**D0 is NOT declared complete.**
-/

namespace D0.Integration.V15.Reconciliation

open D0.Integration.V15.Truth

/-- A (zone-current spectral split): all gates pass in the canonical inner product → `THE`. -/
def cardA : ProofCard := ⟨true, true, true, true, false, false, true, ""⟩
/-- E1 (Schur det factorization): algebraic identity, all gates → `THE`. -/
def cardE1 : ProofCard := ⟨true, true, true, true, false, false, true, ""⟩
/-- B (branch CP readout): negative theorem (family survives) → `NO_GO`. -/
def cardB : ProofCard := ⟨true, true, false, true, true, false, true, "PRIM-BRANCH-ISOTROPIC-READOUT"⟩
/-- D (lepton mass ratios): negative theorem (ratios free) → `NO_GO`. -/
def cardD : ProofCard := ⟨true, true, false, true, true, false, true, "PRIM-EFT-IR-MATCHING-FUNCTIONAL"⟩
/-- E2 (physical EOS / w): negative theorem (w underdetermined) → `NO_GO`. -/
def cardE2 : ProofCard := ⟨true, true, false, true, true, false, true, "PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT"⟩
/-- F1 (archive regular refinement): negative theorem (archive ≠ regular cover) → `NO_GO`. -/
def cardF1 : ProofCard := ⟨true, true, false, true, true, false, true, ""⟩
/-- C (physical edge cover): the cover is a `U(1)` λ-family with an injective separating observable
(`coverCoeffZ3 = −λ`, `EdgeAudit.cover_coeff_injective`); distinct admissible holonomies give inequivalent
covers, so no UNIQUE present-core cover exists — the same underdetermination/maximality shape as siblings
B/D/E2. Reclassified `CONDITIONAL_EXTENSION → NO_GO` (2026-06-24, Cycle 3) to align node C with its siblings;
`provedImpossibleInClass = true` (uniqueness impossible in the present class). Hybrid evidence: Lean owns the
injective separating observable, the cert `verify_unified_feedback.py` owns the `|λ|=1` continuum admissibility.
Missing selector still named (`PRIM-EDGE-HOLONOMY-SELECTOR`). -/
def cardC : ProofCard := ⟨true, true, false, true, true, false, true, "PRIM-EDGE-HOLONOMY-SELECTOR"⟩
/-- F2 (Sturmian refinement): exists, missing owner → `CONDITIONAL_EXTENSION`. -/
def cardF2 : ProofCard := ⟨true, true, false, true, false, false, true, "PRIM-STURMIAN-REFINEMENT-OWNER"⟩
/-- G (present-core limits): the suite of negative limits remains owned → `NO_GO`. -/
def cardG : ProofCard := ⟨true, true, false, true, true, false, true, ""⟩
/-- H (AMS heavy nuclei): external comparison data → `EMPIRICAL_PASSPORT`. -/
def cardH : ProofCard := ⟨false, false, false, false, false, true, true, ""⟩
/-- A phantom `*_RESULT.md` input → `REJECTED`. -/
def cardPhantom : ProofCard := ⟨true, true, true, true, false, false, false, ""⟩

/-- **The manifest, machine-checked.** Each node resolves to exactly its truth-table status. -/
theorem manifest_statuses :
    cardA.status = Status.THE ∧
    cardE1.status = Status.THE ∧
    cardB.status = Status.NO_GO ∧
    cardD.status = Status.NO_GO ∧
    cardE2.status = Status.NO_GO ∧
    cardF1.status = Status.NO_GO ∧
    cardC.status = Status.NO_GO ∧
    cardF2.status = Status.CONDITIONAL_EXTENSION ∧
    cardG.status = Status.NO_GO ∧
    cardH.status = Status.EMPIRICAL_PASSPORT ∧
    cardPhantom.status = Status.REJECTED := by
  refine ⟨?_,?_,?_,?_,?_,?_,?_,?_,?_,?_,?_⟩ <;> decide

/-- All ten audited (non-phantom) node cards. -/
def allCards : List ProofCard :=
  [cardA, cardE1, cardB, cardD, cardE2, cardF1, cardC, cardF2, cardG, cardH]

/-- Exactly two `THE` nodes (A spectral split, E1 algebraic identity) — and no more. -/
theorem exactly_two_the :
    (allCards.filter (fun c => decide (c.status = Status.THE))).length = 2 := by decide

/-- The two `THE` nodes are backed by the actual proved theorems. -/
theorem the_nodes_are_backed :
    (D0.Integration.V15.RawZone.comm * D0.Integration.V15.RawZone.comm * D0.Integration.V15.RawZone.comm
      = (-2840 : ℤ) • D0.Integration.V15.RawZone.comm) ∧
    (D0.Integration.V15.Feshbach.Mfull.det = D0.Integration.V15.Feshbach.Schur.det) :=
  ⟨D0.Integration.V15.RawZone.zone_annihilator,
   D0.Integration.V15.Feshbach.feshbach_schur_factorization.1⟩

/-- The NO-GO / CONDITIONAL nodes are backed by the actual proved negative theorems. -/
theorem nogo_nodes_are_backed :
    D0.Integration.V15.BranchAudit.rho1 ≠ D0.Integration.V15.BranchAudit.rho2 ∧
    D0.Integration.V15.BranchAudit.vandermonde.det ≠ 0 ∧
    D0.Integration.V15.Feshbach.w 3 1 ≠ D0.Integration.V15.Feshbach.w 1 3 ∧
    D0.Integration.V15.Refinement.archiveWindow ≠ D0.Integration.V15.Refinement.regularCoverRatio ∧
    D0.Integration.V15.EdgeAudit.coverCoeffZ3 1 ≠ D0.Integration.V15.EdgeAudit.coverCoeffZ3 2 :=
  ⟨D0.Integration.V15.BranchAudit.branch_readout_not_unique.1,
   D0.Integration.V15.BranchAudit.mass_ratio_underdetermined.2,
   D0.Integration.V15.Feshbach.eos_underdetermined.2,
   D0.Integration.V15.Refinement.archive_window_not_measure_preserving,
   D0.Integration.V15.EdgeAudit.edge_cover_is_family.2⟩

end D0.Integration.V15.Reconciliation
