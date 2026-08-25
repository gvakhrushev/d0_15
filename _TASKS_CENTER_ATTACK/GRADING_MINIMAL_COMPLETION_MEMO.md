# GRADING MINIMAL-COMPLETION SELECTION — the E1 two-completion no-go inverted into an
# exhaustion + extremality-selection theorem (DRAFT, pre-skeptic)

**Date:** 2026-07-18 · **Status:** DRAFT candidate; no ledger row edited (mint package §5).
**Owner directive:** "no-go как источник прорывов" — this is synthesis pass #1 of that program.
**Pre-flight (recon agent, full read):** the 79-row no-go inventory; the colour-corner cluster
(typed-carrier no-go, four Weyl walls, anomaly-variety-2dim, minimal-denominator — verbatim
file:line dossier); the positive faces already minted (RIGIDITY-EXTREMALITY, FINDING-C,
P-INVARIANT-MINIMAL); the completion-strength audit `D0-TWO-COMPLETION-NOGO-STRENGTH-001`
(E1 graded `classScoped`; NO front at `fullMaximality`); `RepresentationReadoutExtension.lean`
(E1: two freedoms — grading signature and Weyl-role `S₃`; `ncCount p q = p² + q² + 3`;
divergence `8 ≠ 12`; missing object `PRIM-FINITE-SPECTRAL-TRIPLE-REP`). KEY NEGATIVE FINDING
honored throughout: colour `N_c = 3` is an INPUT everywhere in the anomaly/denominator ledgers
(SMCharges/AnomalySums/FlowLattice hard-code the 3s); the derived "3" is GENERATIONS — so no
claim here touches "colour derived" (that stays owned-NO-GO).
**Companion Lean:** `09_LEAN_FORMALIZATION/D0/Extensions/GradingMinimalCompletion.lean` —
compiles exit 0, NOT wired, NOT minted.

## §0. Claim (P-schema-ADJACENT argmin-selection, over the E1 grading axis)

The E1 no-go stands UNCHANGED: no admissible DATUM selects between grading signatures — both
`(2,1)` and `(3,0)` are anomaly-free and `S₃`-symmetric, and `PRIM-FINITE-SPECTRAL-TRIPLE-REP`
stays absent. The positive face, machine-checked:

1. **Exhaustion (deficit-discharge, NOT a grade transition — skeptic #20 R1).** The
   grading-SIGNATURE subclass (the `U3_inner` quotient of gradings, cite `D0-X5-G-SYMMETRY-001`;
   the grading OPERATOR stays unforced = the missing PRIM) on the 3-dim generation block is
   EXACTLY `{(p,q) : p+q=3} = {(3,0),(2,1),(1,2),(0,3)}` (`grading_axis_exhaustive` — an iff,
   both directions). The strength audit had ALREADY granted E1 "exhaustion on the scoped
   grading-signature subclass" with the named deficit "no in-module forall-class theorem"
   (`04_VERIFICATION/TWO_COMPLETION_WITNESS_AUDIT.csv` E1; `POSTCORE_NOGO_STRENGTH_AUDIT.md`);
   THIS theorem discharges exactly that deficit. E1's classification does NOT move
   (stays classScoped: the Weyl-role `S₃` axis and the operator-level class are untouched).
2. **Extremality selection.** `ncCount` — E1's own grading-even commutant dimension — is an
   instance of the OWNED P-schema functional family (the umbrella's COLOUR instance minimizes
   a commutant dimension; `D0-P-M1-SATURATION-001`). Over the exhausted class: floor `8`
   (`nc_floor`), attained EXACTLY by the flip pair `{(2,1),(1,2)}` (`min_attained_iff`), which
   is ONE signature class up to the grading-sign relabel `Γ ↦ −Γ` (`minimizers_flip_pair`:
   `(1,2) = Prod.swap (2,1)`; the up-to-sign split is already narrated in
   `TypedRepresentationFunctorClassification.lean:13-15` — cited, not re-derived). The maximal
   signatures `(3,0)/(0,3)` are IN-CLASS non-minimizers with saturation SURPLUS `12 = 8+4`
   (`saturation_surplus`) — NOT the P-schema witness-just-past (that slot needs an
   OUTSIDE-class witness = the missing PRIM; and the schema X_core slot is empty here), so
   this row is **P-schema-ADJACENT** (a new argmin-selection pattern), sharing only the
   commutant-dimension FUNCTIONAL FAMILY with row 556 (skeptic #20 R3). CONVERGENT owned
   candidate, cited not consumed: `q8FSsignature = (2,1)` (Q₈ Frobenius–Schur route,
   `TypedRepresentationFunctorClassification.lean:32-36`, gated by external KO-convention
   `J²=±1`) points at the same minimal class; neither route is an owned selector.

Read as the no-go inversion: "no datum selects" (the no-go, true) + "the owned-FAMILY
extremality functional WOULD select — its licensing for external completions is narrated,
PROOF-TARGET" (what IS machine-checked: the exhaustion + argmin arithmetic) = the selection
gap is not a defect but the exact seam where an M1-as-MDL principle, if licensed, does the
work data cannot (skeptic #20 R5 wording).

## §1. What this does NOT claim (guards, stated before the skeptic)

- NOT "colour derived" (owned NO-GO untouched; N_c=3 stays an input of the frozen ledger).
- NOT a weakening of E1: `nc_divergent` (`8 ≠ 12`) is restated INSIDE the bundle; the missing
  primitive `PRIM-FINITE-SPECTRAL-TRIPLE-REP` stays missing; the no-go row is not edited.
- NOT a resolution of the flip: `(2,1)` vs `(1,2)` — the grading-sign relabel — is a NAMED
  open sub-question (relabel/torsor à la row 549, or physical); only `swap`-relatedness is
  proved.
- NOT a licensing theorem: whether M1-as-MDL (B00:471) licenses applying commutant-minimality
  to EXTERNAL completions is the NARRATED leg (PROOF-TARGET), exactly parallel to the
  P-umbrella's second-order schema leg. The Lean owns the arithmetic of exhaustion +
  selection; the principle's applicability is graded narrated.
- NOT built on the rhyme `ncCount(2,1) = 8 = dim ℂ[Q₈]` — recorded as a CHK-grade observation
  only (trap d).

## §2. Owned pre-facts (file:line)

- E1 module: `D0/Extensions/RepresentationReadoutExtension.lean` — `ncCount` def :22, four
  signatures :25, `nc_divergent` :31-ish, no-go bundle + "Missing object:
  PRIM-FINITE-SPECTRAL-TRIPLE-REP" (header :14).
- Strength audit: registry row `D0-TWO-COMPLETION-NOGO-STRENGTH-001` (E1 = classScoped; no
  front fullMaximality) — the row whose NAMED E1 DEFICIT this memo discharges (no grade move).
- P-functional precedent: `D0-P-M1-SATURATION-001` + `D0.Foundation.M1CoreSaturation`
  (COLOUR instance = commutant-dimension minimization; uniqueness graded to the M1 family —
  the same grading discipline used here for the flip residual).
- MDL parent: B00:471 (conditional-K razor — the owned sentence the narrated leg cites).

## §3. Pre-registered attack surface (strongest first)

- **ATT-1 (functional licensing).** "ncCount-minimization is an OWNED functional" — the
  P-umbrella minimizes commutant dimension over M1 ZONE FRAMES; applying the same functional
  family to EXTERNAL completions is an analogical extension, not owned. PRICED: §1 grades the
  licensing as narrated PROOF-TARGET; the machine-checked content (exhaustion + argmin) is
  functional-free arithmetic. A skeptic ruling the licensing un-owned confirms our own grading.
- **ATT-2 (exhaustion scope).** `p+q=3` as THE admissible grading class: is `p+q=3` itself
  owned (signature on a 3-dim block must split 3 = p+q), or could degenerate/partial gradings
  (p+q<3) be admissible? The E1 module's own list has exactly the four `p+q=3` signatures —
  the exhaustion theorem proves OUR list = the `p+q=3` class; if E1's list is itself
  incomplete, the upgrade inherits that gap. Named and priced: the iff is against `p+q=3`,
  stated, not against "all conceivable gradings".
- **ATT-3 (does minimality even point the right way?).** Why is FEWER neutral-current
  channels the M1-preferred direction (rather than more)? Narrated answer: extra channels =
  extra grading-even structure with no admissible datum demanding it = the underivable-θ shape
  of B00:471. A skeptic can demand this as a theorem — that IS the narrated leg, conceded.
- **ATT-4 (flip status).** If the Γ-sign flip is later adjudicated PHYSICAL (not relabel),
  the "unique up to flip" grading weakens to "two-element minimum class". Priced: stated as
  the named open sub-question; the bundle claims only swap-relatedness.
- **ATT-5 (registry duplication).** The RAISE-1/FINDING-C positive faces cover the zone-frame
  extremum; this row covers the COMPLETION-class extremum — different objects; cross-refs
  required, absorption forbidden.

## §4. Verification

`lake env lean D0/Extensions/GradingMinimalCompletion.lean` — exit 0, no sorry. All seven
theorems kernel-checked (`decide`/`interval_cases`+`omega`); the exhaustion is an iff (both
directions); `nc_divergent` re-exported inside the bundle (the no-go not weakened).

## §5. Ready-to-mint package (owner-authorized session; apply after skeptic)

1. New row `D0-GRADING-MINIMAL-COMPLETION-SELECTION-001` (both ledgers): BOOK_04 §04.E1
   anchor; `D0.Extensions.GradingMinimalCompletion` / `grading_minimal_completion_selection`;
   lean_status LEAN_PROVED (arithmetic legs); release PROOF-TARGET (licensing leg narrated);
   note = §0 + §1 guards + ATT-1..5 + cross-refs (E1 no-go unchanged, strength audit upgraded
   on the grading axis only, P-umbrella functional precedent, flip open, rhyme CHK).
2. Append to `D0-TWO-COMPLETION-NOGO-STRENGTH-001` note (deficit-discharge wording, NO grade
   transition): "GRADAXIS[2026-07-18]: the audit's named E1 deficit ('no in-module
   forall-class theorem' on the scoped grading-signature subclass) is DISCHARGED by
   D0.Extensions.GradingMinimalCompletion.grading_axis_exhaustive (kernel iff, p+q=3 ⇔
   membership) + argmin selection (floor 8, minimizers = the flip pair {(2,1),(1,2)});
   E1 classification UNCHANGED classScoped (Weyl-role axis + operator-level class untouched);
   licensing of the extremality functional for external completions = narrated PROOF-TARGET."
   ALSO append to `D0-GRADING-NEUTRAL-CURRENT-MAXIMALITY-NOGO-001` (row 489) note:
   "GRADAXIS[2026-07-18]: the 'witness-only (no whole-class exhaustion)' clause is now
   registry-reconciled — signature-subclass exhaustion + argmin are Lean-owned in
   D0.Extensions.GradingMinimalCompletion; row 489's PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR
   stays the missing outside-class object; the pre-existing RAISE → P-INVARIANT-MINIMAL
   attribution on this axis is a DIFFERENT object (observable algebra, not completion class) —
   both stand." Cross-refs required in the new row: TypedRepresentationFunctorClassification
   (flip narration, q8FSsignature), TypedRepresentationFunctorNoGo (Completion type; its
   `residual_minimal_two_classes` second conjunct is vacuous `∨ True` — the argmin here is the
   genuine content that theorem gestured at), X5/Grading/SymmetryGroups (u3SignatureClasses
   duplicate list; U3_inner caveat).
3. Wire into `D0/All.lean`; full build; guards. NO book edits in this pass (parallel session
   owns 01_BOOKS).
