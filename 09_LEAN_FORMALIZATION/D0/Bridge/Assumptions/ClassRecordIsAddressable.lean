/-!
# ASSUMP-CLASS-RECORD-IS-ADDRESSABLE — R-A carrier (explicit, un-discharged)

Owner file for the `LEAN_ASSUMPTION_LEDGER.csv` id `ASSUMP-CLASS-RECORD-IS-ADDRESSABLE`
(F3_HONEST_BRIDGES_PACKAGE.md Task 1; CLOSE_GAP_W_MEMO.md §3.3, post-independent-skeptic
2026-07-06). Assumption taxonomy: **`D0_INTERNAL_FORCING_TARGET`** — the F3 §1.1(3)
SANCTIONED FALLBACK, used because it is the whitelisted internal-target type in
`check_no_sorry_in_core.py` (`INTERNAL_TARGET_TYPES`); the F3-primary coinage
`D0_INTERNAL_TYPING_TARGET` is NOT whitelisted and would fail the validator. Semantics
unchanged: a D0-internal typing target, NOT an external classical theorem citation.

**The assumption (R-A, the entire content is the copula).** The re-detection
class-record **IS** — not merely *interacts-with* — an addressable registration. This is
a NAMED EXTERNAL ASSEMBLY-BRIDGE assembled across the BOOK_01 §01.3/§01.11.3 layer
boundary: `:253` types the record atom `𝔮` as addressable at the primitive-dyad layer,
`:996` types the re-detection class as a physical object over records; the IS-join
spanning the two layers is UN-OWNED. `:988` (the CORE contradiction theorem) forces only
INTERACT-WITH an addressable registration, never IS. There is **no in-print name-match**
(unlike GAP-E's `:836`/`:862`/`:67`, probe-confirmed), so this is NOT an assembly-grade
matched typing (skeptic E-CW-1). W-REC (owned architecture: `P_N + Q_N = I` `:33-34`/`:37`,
single `:1998` `Q_N`-writer — `D0.Core.WRecArchitecture`) removes the alternative carrier
but does NOT close the IS-gap. This is the forced-explicit-external-bridge honest closure
(selector-M1-forbidden pattern), not an open-unattempted.

**Failure meaning.** If the class-record is NOT an addressable registration, W-ELEM
reopens (demotes to narrated) and the window lower bound `|V_base| = |Ω₈| + 1 = 9` loses
its CONDITIONAL seal, reverting to GAP_W_SYNTHESIS_MEMO v2's narrated-W-ELEM state (no
regression below that).

**Reopening hook.** A maintainer scoping `:253`'s `𝔮` strictly to the primitive dyad
blocks the bridge and demotes W-ELEM to narrated; conversely, owning the IS-typing or
finding an in-print name-match upgrades the GAP-W seal to a full owned closure and
retires the ledger row.

Consumed by: `D0.Core.WRecArchitecture.card_base_forced_wrec` (the re-attributed GAP-W
capstone; `used_by_theorem` = `card_base_forced_conditional`, `WitnessForcing.lean`).
Nothing is proven here: the structure is an explicit hypothesis CARRIER (the
`statement : Prop; cited : statement` pattern of `KernelChargeLocalization.lean`).
-/

namespace D0.Bridge

namespace BridgeAssumption

/-- R-A carrier: the un-owned IS-typing "the re-detection class-record IS an addressable
registration" as an explicit `Prop` + citation field. EXPLICIT hypothesis, never a Lean
theorem — see module docstring for the layer-boundary assembly, failure meaning, and
reopening hook. -/
structure ClassRecordIsAddressableAssumption where
  statement : Prop
  cited : statement

end BridgeAssumption

abbrev ClassRecordIsAddressableAssumption :=
  BridgeAssumption.ClassRecordIsAddressableAssumption

end D0.Bridge
