# E1 RESIDUAL COLLAPSE — the exact LOCATION of the two-completion residual: signature/
# orientation axes reduce to the KO bit; completion-grain residual = the named PRIM pair
# (no-go-synthesis pass #2; POST-SKEPTIC v2, #21 repairs applied)

**Date:** 2026-07-18 · **Status:** DRAFT candidate; no ledger row edited (mint package §5).
**Program:** "no-go как источник прорывов", pass #2 (pass #1 = grading argmin selection,
`D0-GRADING-MINIMAL-COMPLETION-SELECTION-001`).
**Pre-flight:** pass-#1 dossier + full read of `TypedRepresentationFunctorNoGo.lean` (the
`Completion` type; the vacuous `∨ True` conjunct skeptic #20 named), `TypedRepresentation-
FunctorClassification.lean` (the FS candidate GROUNDED: Q₈ terminal sectors `E₀:+1, E₄:−1,
E₃:+1`, one quaternionic sector; the named external gate `KO_dimension_convention_is_external`
/ `PRIM-FINITE-SPECTRAL-TRIPLE-REP`), E1 header ("no canonical basis — cited from R1" for the
Weyl-role freedom; "the genuinely-NEW content here is the neutral-current divergence").
**Companion Lean:** `D0/Representation/CompletionResidualCollapse.lean` (compiles exit 0, NOT
wired) + an authorized REPAIR of the owned `residual_minimal_two_classes` (the vacuous second
conjunct `∨ True` replaced by the genuine dichotomy, proved inline; skeptic-#20 finding
discharged at the source).

## §0. Claim (composition, not new postulate)

The E1 two-completion residual DECOMPOSES, at stated grades, into three named factors (the
"ONE bit" headline of the draft was RE-GRAINED by skeptic #21 — see the capstone below for
the honest two-grain statement):

| factor | resolution | grade |
|---|---|---|
| Weyl-role `S₃` freedom | RESOLVED internally at cert grade: "the Aut part-size order 9<11<13 RESOLVES the E1 Weyl-role leg" (`D0-CANONICAL-SELF-READING-FUNCTOR-001`, row 477, CERT-CLOSED); the residual physical e/μ/τ NAMING stays inside the external PRIM (row 559); the invariant `nc` never references roles (Lean) | owned cert-grade citation (477) + named external residue (559); skeptic #21 R1 |
| signature CLASS ({8-pair} vs {12-pair}) | exhausted + argmin-selected (pass #1: floor 8, minimizers = flip pair) | Lean (arithmetic) + narrated licensing (PROOF-TARGET) |
| ORIENTATION within the minimal class ((2,1) vs (1,2)) | FS-selected: the Q₈ sector signs `(+1,+1,−1)` have exactly ONE quaternionic sector = the `q`-slot of `(2,1)`, not `(1,2)` — CONDITIONAL on the KO bit `J²=±1` | Lean (counting) + the bit stays EXTERNAL (the Classification module's own named gate) |

Machine-checked (all kernel `decide`/`interval_cases`): `completion_nc_dichotomy` (every
completion has `nc ∈ {12,8}` — the genuine form of the repaired conjunct);
`nc_flip_invariant`; `nc_eq_iff_flip_class_sig` + lift (`nc`-fibres = flip-classes, EXACTLY
two); `ncCount_defs_agree` (the two in-tree defs, definitional `rfl`);
`fs_orientation_selects` (one `−1` sector ⇒ `(2,1)` not `(1,2)` under odd=quaternionic);
`completion_cases`.

**Capstone reading (re-grained, skeptic #21 R2):** the E1 no-go ("no admissible datum
selects") stays TRUE and untouched. At SIGNATURE grain the residual reduces, conditionally,
to the single KO bit: class = argmin (pass #1, licensing narrated), orientation = FS-counted
(conditional on the bit), role-bijection = cert-resolved (row 477) with the physical-naming
residue external (row 559). At COMPLETION grain the residual is the NAMED external object
pair, exactly as the registry holds it: `PRIM-FINITE-SPECTRAL-TRIPLE-REP` (= the KO bit + the
role-resolution/physical-naming functor, R1 row 460/559) and
`PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR` (the operator-level class, row 489). No uniqueness of
the completion is asserted; what is proved is WHERE the remaining freedom lives and that the
signature/orientation axes need only the one bit. This is the narrowing program executed on
E1 at honest grain.

## §1. What this does NOT claim

- NOT that the KO bit is derivable (it is the named external PRIM; the Classification module
  owns the gate statement; we cite, never absorb).
- NOT that the FS pullback is owned (the odd=quaternionic reading IS the KO bit; conditional
  framing everywhere; `fs_orientation_selects` proves only the counting).
- NOT a new role-axis mechanism: the internal resolution is row 477's (cert grade, cited);
  the physical-naming residue is row 559's (external); we formalize only that `nc` factors
  through signatures. ('Gauge' wording of the draft was KILLED by skeptic #21 — misattributed
  to R1; accepted, replaced.)
- NOT a promotion of pass #1's licensing leg (still narrated PROOF-TARGET).
- The E1/R1 no-go rows are NOT edited (the only owned-module edit is the vacuity repair,
  which STRENGTHENS the no-go's own minimality statement).

## §2. Pre-registered attack surface

- **ATT-1 (decomposition completeness).** "The residual = roles × class × orientation" — is
  there a FOURTH freedom (e.g. the operator-level grading class beyond signatures, the
  missing PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR)? PRICED: the decomposition is stated over
  the SIGNATURE quotient (pass-#1 scope); the operator-level class stays open exactly as
  before — the collapse claim is scoped to the E1 signature/role/orientation data, and the
  outside-class witness slot stays with the PRIMs.
- **ATT-2 (FS grounding).** The sector signs `(+1,+1,−1)` are narrated in the Classification
  module, not Lean-derived from Q₈ representation theory in-tree. PRICED: `fsSectorSigns` is
  a DEF citing that narration (classical FS data of Q₈); deriving it in-tree (mathlib rep
  theory of Q₈) is a named upgrade, not claimed.
- **ATT-3 (role-axis attribution — LANDED, kill accepted).** The draft's "roles = gauge"
  was killed by #21: "no canonical basis" is E1-header-local (not in R1's row); R1 grades the
  role resolution as part of the external PRIM; and row 477 (CERT-CLOSED) owns the OPPOSITE —
  an internal cert-grade resolution by the Aut part-size order. v2 cites 477 + 559; the Lean
  proves only that `nc` factors through `(p,q)`.
- **ATT-4 (owned-module edit).** Editing `residual_minimal_two_classes` changes an owned
  theorem's statement. PRICED: the edit strictly STRENGTHENS it (removes a vacuous disjunct,
  proves the genuine dichotomy), carries a dated repair note citing skeptic #20, and the old
  first conjunct is untouched; downstream users of the theorem only gain.

## §3. Verification

`lake env lean` exit 0 on both files; all theorems kernel-checked (no native_decide); the
owned-module repair compiles standalone.

## §4. Ready-to-mint package (owner-authorized; apply after skeptic)

1. New row `D0-COMPLETION-RESIDUAL-COLLAPSE-001` (both ledgers): BOOK_04 §04.E1/P3-A anchor;
   `D0.Representation.CompletionResidualCollapse` / `completion_residual_collapse;
   completion_nc_dichotomy;nc_flip_invariant;nc_eq_iff_flip_class_sig;nc_eq_iff_flip_class;
   fs_orientation_selects;ncCount_defs_agree`; lean_status LEAN_PROVED (composition legs);
   release PROOF-TARGET (KO bit external; licensing narrated); note = §0 table + §1 guards +
   ATT-1..4 + cross-refs (E1, R1, pass #1, Classification's KO gate, the repaired conjunct).
2. Note append to `D0-POSTCORE-REPRESENTATION-EXTENSION-NOGO-001`: "RESIDCOLLAPSE[2026-07-18]:
   the residual's LOCATION is now theorem-grade at signature grain — signature class =
   argmin-selected (pass #1, licensing narrated), orientation = FS-counted CONDITIONAL on the
   KO bit, role-bijection = cert-resolved by the Aut part-size order (row 477) with physical
   naming external (row 559); signature/orientation axes provably reduce to the single KO bit;
   completion-grain residual = the named PRIM pair (PRIM-FINITE-SPECTRAL-TRIPLE-REP, row
   460/559; PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR, row 489). No-go unchanged; no completion
   uniqueness asserted (D0-COMPLETION-RESIDUAL-COLLAPSE-001)."
   PLUS reconciliation appends on row 565 (both CSVs; the GRADAXIS precedent): the stale
   cross-ref "residual_minimal_two_classes second conjunct vacuous (∨ True)" is DISCHARGED —
   the conjunct is repaired to the genuine dichotomy (2026-07-18).
3. Wire into `D0/All.lean`; full build; guards. NO book edits (parallel session owns 01_BOOKS).
