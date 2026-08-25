# M1-UNIVERSALITY v2 — M1 as a schema over description systems (POST-SKEPTIC; R1–R8 applied)

**Date:** 2026-07-18 · **Status:** DRAFT v2; no ledger row edited yet (mint package §6).
> **[POST-MINT NOTE 2026-07-18, external review]** Header superseded: the §6 package was applied in the owner-authorized session — row 563 `D0-M1-UNIVERSALITY-001` is MINTED (LEAN_PROVED Leg A / release PROOF-TARGET) and `D0.Foundation.M1Universality` is WIRED at `All.lean:219`; full build green (4020 jobs, verified 2026-07-18).
**Skeptic #18 verdict on v1: WOUNDED (no §05.8.R kill of the core attribution); wounds accepted
in full and repaired:** (W1) v1's §0 three-prong restatement DROPPED clause 3 of DEF 0.3.1 (the
protocol exemption) — KILLED as stated, restored with the book's numbering (R3); (W2) v1's
"localization corollary" was unproved essayistic overreach — KILLED as stated, WITHDRAWN (v2
asserts no such corollary); (W3) "both directions" was packaged while only `.mpr` was stated —
kernel-refuted by a reflection-only rebuild; v2 states preservation AND no-manufacture as
theorems (R4); (W4) v1's negative control was technique-level — v2 ships two kernel-checked
conclusion-failing countermodels in-module (`nc1`, `nc2`) (R5); (W5) Leg B's
"`K(catalog|theory)=O(1)`" carried no parameter — vacuous pointwise — repaired to the FAMILY
form (R1); (W6) quote drift +54 lines and a splice-paraphrase in P4 — re-pinned verbatim (R6);
(W7) missing cross-reference to `D0-M1-PREDICATE-001` — added (R7); (W8) ASSUMP-AIT-INVARIANCE
had no Lean carrier for the assumption ledger — registration DROPPED, inline citation only (R8).
**Lean:** `09_LEAN_FORMALIZATION/D0/Foundation/M1Universality.lean` v2 — compiles, exit 0, not
wired.

## §0. Claim (schema form, v2)

**U-M1.** M1 is a SCHEMA over description systems: for any grammar `G`, `M1(G)` is the
exogenous-parameter test DEF 0.3.1 with the book's clauses — θ is exogenous iff it "(1) is not
derived inside the corpus, (2) affects a distinguishable result or a law's formulation, and
(3) is not an unavoidable part of the distinguishability protocol" (B00:398, verbatim). Legs:

- **Leg A (machine-checked; clause 1 only).** Clause 1 — the only clause MODELED as grammar-dependent (clause 2's "formulation" half is grammar-adjacent; W9 gloss) —
  is stable in BOTH directions along faithful interpretations: witnesses transport
  (`ExogenousWitness.transport`), derivability preserves and reflects
  (`faithful_preserves_derivable`, `faithful_reflects_derivable`), witnesses cannot be
  manufactured (`witness_not_manufactured`), bundle `m1_grammar_functorial`; finite worked
  instance `toy_transport`; conclusion-failing controls `nc1`/`nc2` (preservation-only breaks
  transport; reflection-only manufactures a witness — each hypothesis load-bearing).
  Clauses 2–3 and mandatoriness are protocol-level, carried as hypotheses; their preservation
  is per-instantiation, NOT claimed.
- **Leg B (narrated, external-owner grade; FAMILY form).** The corpus already owns the
  conditional-complexity razor at B00:471: "Adding an underivable `theta` moves the law from
  `K(T)` to `K(T) + K(theta | T)`". Its machine-independence is the classical CONDITIONAL
  invariance theorem `|K_U(x|y) − K_V(x|y)| ≤ c_{U,V}`. The robust separation is a family
  statement: for an empirical-catalog family `C_n` (data to size/precision `n`), a GENERATING
  theory satisfies `∃c ∀n, K(C_n | T) ≤ c`, while an IMPORTING theory has `K(C_n | T)`
  unbounded in `n` — anchored to B00:340's Oracle ("resolving arbitrary halting"). Pointwise
  `O(1)` over one finite pair separates nothing (skeptic #18's named gap — conceded); the
  family form separates, and is invariant under change of universal machine by conditional
  invariance. This HARMONIZES with :471 (already conditional) rather than replacing it.

v2 asserts NO localization corollary (v1's was killed). What the two legs jointly support is
narrower and honest: the M1 criterion's grammar-sensitive clause is functorial along faithful
interpretations, and its AIT razor is encoding-robust in family form — so objections of the
shape "M1 is an artifact of the D0 grammar" must attack the primitives (INCLUDING the
protocol data of clauses 2-3), the faithfulness class, or per-instantiation protocol
preservation — not clause 1's cross-grammar stability or the family-form razor (W9 repair).

## §1. Owned pre-facts (verbatim, re-pinned 2026-07-18 post-book-edit)

- **P1 (three-prong test).** B00:398: "θ counts as exogenous iff it (1) is not derived inside
  the corpus, (2) affects a distinguishable result or a law's formulation, and (3) is not an
  unavoidable part of the distinguishability protocol." Long form :455-459.
- **P2 (AIT grounding, absolute form).** B00:342: "A theory that imports an empirical catalog
  carries `K_catalog > 0` — the catalog cannot be regenerated from the theory's own finite
  primitives".
- **P3 (the dichotomy proof).** B00:480: "Proof (by contradiction): suppose an exogenous
  parameter is mandatory yet distinguishability-neutral. … this violates DEF 0.3.3 (no
  dependence on hidden conventions). Contradiction."
- **P4 (keystone, verbatim).** B00:482: "So M1 is not an assertion about physics; it is the
  **minimal condition under which the THE/LEM/DEF language is meaningful at all**."
- **P5 (conditional-K razor, the owned parent of Leg B).** B00:471: "Let `K(·)` be
  (conditional) Kolmogorov complexity in a fixed universal language. Adding an underivable
  `theta` moves the law from `K(T)` to `K(T) + K(theta | T)`".
- **P6 (external owner theorem).** Conditional invariance of Kolmogorov complexity
  (Kolmogorov/Solomonoff/Levin) — cited inline at the same grade as Dedekind-1897 usage; NOT
  registered in the assumption ledger (no Lean carrier — R8).
- **P7 (in-house neighbor).** `D0.Foundation.M1Predicate` (`D0-M1-PREDICATE-001`): `M1Forced`
  = unique witness of a canonical finite constraint WITHIN one system;
  `RequiresExternalCatalogue Forced b := ¬ Forced b`. Relation: M1Predicate is within-system
  forcing; M1Universality is cross-system stability of the classification. Disjoint by design;
  composition (transport of `M1Forced` along faithful maps) is future work, not claimed.

## §2. What is proved (Lean v2, all kernel-checked)

Transport + preservation + reflection + no-manufacture + bundle + finite instance + two
conclusion-failing countermodels. Grade note per trap (m): the abstract theorems' sole content
is the schema attribution; they carry no D0-specificity and are graded accordingly.

## §3. Pre-registered attack surface (v2)

- **ATT-1 (residual triviality).** Even with both directions and controls, the abstract legs
  are short logic facts; the content is the ATTRIBUTION plus the controls showing each
  hypothesis load-bearing. Priced: that is the claim, nothing more.
- **ATT-2 (protocol clauses).** Clauses 2–3 not transported (per-instantiation). Priced and
  scoped in v2 everywhere.
- **ATT-3 (faithfulness class).** "Same theory in another grammar" = faithfully interpretable;
  non-faithful translations are different theories where the schema re-instantiates. A skeptic
  wanting cross-THEORY invariance is asking for a different (false) claim.
- **ATT-4 (family-form attackable).** The `C_n` family needs a definition of "the same catalog
  at size n" — priced: it is supplied per-theory by the passport discipline (frozen forms,
  e.g. the empirical-passport rows), not by this memo.

## §4. What this does NOT show

Unchanged from v1 plus: no localization corollary; no transport of clauses 2–3; no formalized
Kolmogorov complexity; no book edit applied.

## §5. Verification

`lake env lean D0/Foundation/M1Universality.lean` exit 0, no sorry; `toy_transport`, `nc1`,
`nc2` kernel-checked; each `Faithful` direction shown load-bearing by its countermodel.

## §6. Ready-to-mint package (owner decision; NOT applied)

1. New row `D0-M1-UNIVERSALITY-001` (both ledgers): B00 §00.9 anchor;
   `D0.Foundation.M1Universality` /
   `m1_grammar_functorial;witness_not_manufactured;toy_transport;nc1_transport_fails_without_reflection;nc2_witness_manufactured_without_preservation`;
   lean_status LEAN_PROVED (Leg A/clause 1 only); release PROOF-TARGET (Leg B narrated); note
   carries W1–W8 + per-leg grading + P7 cross-reference.
2. Wire into `D0/All.lean`; full build.
3. B00:342 edit (owner-gated, CORRECTED SPEC per R2): robustify BOTH literals via the FAMILY
   form (importer: `K(C_n|T)` unbounded; generator: `∃c ∀n ≤ c`), route the Solomonoff clause
   through the chain rule `K(T, C_n) ≈ K(T) + K(C_n|T)` (= :471's owned form), cite
   conditional invariance. If not adopted, :342 stays untouched — Leg B stands on :471 alone.
