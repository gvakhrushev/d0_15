import Mathlib.Tactic

/-!
# D0-V15-TRUTH-SCHEMA-001 — the derivability discipline as a decidable schema (campaign §1, §12 Book 00)

This module encodes the v15 truth discipline so that the *status of every node is a decidable function of its
proof card*, not a matter of prose. It is the schema referenced by `RawZone`, `BranchAudit`, `EdgeAudit`,
`Feshbach`, `Refinement`, `PhysicalBoundary`, and consolidated in `Reconciliation`.

**§1.2 universal derivability criterion.** An object `X` may be a present-core `THE` iff *all four* gates hold:
`derivedFromFrozen` (`X = f(𝔇₀)` by allowed ops), `autCovariant` (`gXg⁻¹ = X` or an exact equivariance law),
`uniqueModGauge` (any admissible `X'` is gauge-equivalent), `nonzeroResponse` (a nonzero readout witness).

The five — and only five — admissible results, in priority order of the decision function:
* `REJECTED` — the input does not exist in frozen source (a phantom `*_RESULT.md`);
* `EMPIRICAL_PASSPORT` — an external comparison datum (never a D0 primitive);
* `THE` — all four gates pass;
* `NO_GO` — a negative theorem is proved (`provedImpossibleInClass`): not derivable in the declared class;
* `CONDITIONAL_EXTENSION` — gates fail, not impossible, but a missing primitive is named.

§12 "no silent primitive insertion": a `CONDITIONAL_EXTENSION` MUST name its missing primitive; a card with
gates failing, not impossible, and no named primitive falls back to `NO_GO` (you may not claim a conditional
extension without saying what is being added).
-/

namespace D0.Integration.V15.Truth

/-- The five admissible v15 node results. -/
inductive Status
  | THE                    -- proved from frozen D0 primitives only
  | NO_GO                  -- a negative theorem: underivable in a declared admissible class
  | CONDITIONAL_EXTENSION  -- exists only after a named new primitive/map/contract
  | REJECTED               -- input does not exist / cannot be sourced
  | EMPIRICAL_PASSPORT     -- external target, comparison only
  deriving DecidableEq, Repr

/-- The §1.2 proof card. -/
structure ProofCard where
  derivedFromFrozen : Bool        -- X = f(𝔇₀) by allowed ops
  autCovariant : Bool             -- gXg⁻¹ = X ∀g, or an exact equivariance law
  uniqueModGauge : Bool           -- admissible X' ⇒ X' ∼_gauge X
  nonzeroResponse : Bool          -- a nonzero readout witness exists
  provedImpossibleInClass : Bool  -- a negative theorem holds (NO-GO)
  isExternal : Bool               -- external comparison datum (PASSPORT)
  inputExists : Bool              -- input present in frozen source (else REJECTED)
  missingPrimitive : String       -- the exact missing primitive (required for CONDITIONAL)
  deriving Repr

/-- All four present-core gates hold. -/
def ProofCard.allGates (c : ProofCard) : Bool :=
  c.derivedFromFrozen && c.autCovariant && c.uniqueModGauge && c.nonzeroResponse

/-- **The status function (§1.2).** -/
def ProofCard.status (c : ProofCard) : Status :=
  if ¬ c.inputExists then Status.REJECTED
  else if c.isExternal then Status.EMPIRICAL_PASSPORT
  else if c.allGates then Status.THE
  else if c.provedImpossibleInClass then Status.NO_GO
  else if c.missingPrimitive ≠ "" then Status.CONDITIONAL_EXTENSION
  else Status.NO_GO

/-- **THE requires all four gates** (and a real, internal input). -/
theorem the_needs_all_gates (c : ProofCard) (h : c.status = Status.THE) :
    c.inputExists = true ∧ c.isExternal = false ∧ c.allGates = true := by
  unfold ProofCard.status at h
  by_cases he : c.inputExists
  · by_cases hx : c.isExternal
    · simp [he, hx] at h
    · by_cases hg : c.allGates
      · exact ⟨he, by simpa using hx, hg⟩
      · by_cases hi : c.provedImpossibleInClass
        · simp [he, hx, hg, hi] at h
        · by_cases hp : c.missingPrimitive = "" <;> simp [he, hx, hg, hi, hp] at h
  · simp [he] at h

/-- **No silent primitive insertion (§12).** A `CONDITIONAL_EXTENSION` always names a missing primitive. -/
theorem conditional_names_primitive (c : ProofCard) (h : c.status = Status.CONDITIONAL_EXTENSION) :
    c.missingPrimitive ≠ "" := by
  unfold ProofCard.status at h
  by_cases he : c.inputExists
  · by_cases hx : c.isExternal
    · simp [he, hx] at h
    · by_cases hg : c.allGates
      · simp [he, hx, hg] at h
      · by_cases hi : c.provedImpossibleInClass
        · simp [he, hx, hg, hi] at h
        · by_cases hp : c.missingPrimitive = ""
          · simp [he, hx, hg, hi, hp] at h
          · exact hp
  · simp [he] at h

/-- A failed gate forbids THE. -/
theorem dropped_gate_not_the (df ug nr ic ex : Bool) (mp : String) :
    (ProofCard.mk df false ug nr ic ex true mp).status ≠ Status.THE := by
  intro h
  have := (the_needs_all_gates _ h).2.2
  simp [ProofCard.allGates] at this

/-- The zone-current card (Work Package A: all four gates pass) resolves to `THE`. -/
def zoneCurrentCard : ProofCard := ⟨true, true, true, true, false, false, true, ""⟩
theorem zone_current_is_the : zoneCurrentCard.status = Status.THE := by decide

/-- A phantom input (a missing `*_RESULT.md`) resolves to `REJECTED`. -/
def phantomCard : ProofCard := ⟨true, true, true, true, false, false, false, ""⟩
theorem phantom_is_rejected : phantomCard.status = Status.REJECTED := by decide

end D0.Integration.V15.Truth
