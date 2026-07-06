# SHELL-MEMBERSHIP v2 — pre-registered hardening of the PDG shell lead (FROZEN BEFORE RUNS)

**Status:** DRAFT prereg; frozen before any v2 computation. Follows PDG_PHI_LATTICE_RESULTS.md
(v1: exploratory lead — frozen A/B/C beats scrambles; 0/2000 ×2 under skeptic's structure-matched
nulls; capped by provenance + arm-redefinition). No registry edits; vocabulary caps below.

## Questions

- **Q1 (provenance/derivation — the prize):** does an OWNED, mass-blind scene rule predict shell
  MEMBERSHIP? Candidate source: BOOK_04 §04.CVFT.F3c identifies the three-orbit geometry with the
  zone carrier V_shell = span{|9>,|11>,|13>}; T2-P2 owns zone roles (9=defect/base, 11=memory
  torus, 13=terminal shell); Lean TorusCore13GeometryOrigin owns 3-shell radii (1,(a+1)/2,a).
  RULE DISCIPLINE: any candidate particle->zone typing must be stated from owned text (file:line)
  BEFORE its membership match is computed; matches are counted against the exact permutation null.
  A rule found by optimizing match count is FORBIDDEN (that is fitting).
- **Q2 (statistical hardening of the v1 lead):**
  (a) exact structure-matched permutation test: null = assignments preserving sizes (5/4/4),
      the overlap pattern (|A∩C|=2, others disjoint), and the excluded set ({6,7}); enumerate
      exactly if |null| <= 10^7, else 10^5 uniform samples; report exact/MC p.
  (b) leave-one-out stability: for each of the 13 slots, drop it, refit circles, recompute the
      frozen-vs-null percentile; criterion: frozen stays above the 95th percentile in >= 11/13 folds.
  (c) model-class control: repeat with straight-line fits (2-param) in the same (n_abs, H13_u)
      plane; if lines separate frozen-vs-null as well as circles, the "3 circles" reading carries
      no specific content beyond clustering (recorded as such).
- **Null gate (mass-scramble):** recompute node coordinates from masses randomly permuted among
  the 13 slots (200 draws); the frozen membership must NOT beat its null above chance
  (fire rate <= 5%), else the pipeline rewards labels, not structure.

## Acceptance criteria (frozen)

- **Q2 lead-confirmed** iff: exact/MC p <= 0.01 AND LOO >= 11/13 AND mass-scramble gate passes.
  Model-class note (c) qualifies but does not veto.
- **Q1 derivation-found** iff: an owned-text rule (stated before matching) reproduces the frozen
  membership with match count whose exact-null p <= 0.01. Partial matches reported descriptively.
- Vocabulary: "membership-signal-confirmed (pre-registered)" / "not-confirmed" /
  "derivation-found" / "derivation-not-found". FORBIDDEN: "masses derived", "shells derived from
  the scene" without Q1 passing, any registry/status change from this campaign.

## Pre-registered attack surface

- S1: the (n_abs, H13_u) embedding is itself mass-derived (n_abs from lattice fit of masses);
  a positive Q2 therefore shows structure of the EMBEDDING+membership pair, not mass-free
  geometry. Only Q1 lifts this cap. Stated up front.
- S2: 13 slots, small-N; exact enumeration of the structure-matched null is the antidote; no
  asymptotic p-values allowed.
- S3: rule-shopping risk in Q1 — bounded by the "state rule before matching" discipline and by
  reporting EVERY rule attempted (a rules ledger, including failures).
- S4: LOO folds are correlated (shared 12 nodes); the 11/13 threshold is a convention, frozen here.
