# Self-Reading Functor — Global Outcome

**Outcome D — partial functor** (`D0.Extensions.CanonicalSelfReadingFunctor.canonical_self_reading_partial_functor`).

A forced-skeleton functor `S0 : Hist_D0 -> ReadoutRep_D0` EXISTS and is UNIQUE modulo natural equivalence on the Aut-canonical/forced subcategory; it generates every forced output (carrier 33, commutant 12, Laplacian spectrum, resolvent det/cycle-type, S_DE window 359/160, no-phi^3, orbit exponent set {1/4,1/3}). It does NOT extend to a unique total functor: each of the four disputed outputs is a genuine two-completion, and (by Outcome-D + the post-core dependence) the four do not merge.

- NOT Outcome A (unique): each disputed output separates across admissible completions.
- NOT Outcome B (finite family) globally: the skeleton IS unique; the non-uniqueness is in the extensions.
- NOT Outcome C (no functor): the skeleton functor genuinely exists.
- IS Outcome D: unique on a strict subcategory; the 4 disputed outputs remain four independent primitives.

Adversarial refinement: the Aut part-size order (9<11<13) RESOLVES the E1 Weyl-role bijection leg, so E1's load-bearing separator is the grading SIGNATURE (nc 8 vs 12), not the role bijection.

Honest caveat: the isotypic decomposition is encoded as a checked list in `FinitePathRepresentation.lean` (values verified) rather than proved from `Aut` inside Lean; the dependence matrix is a stipulated checked adjacency. The Lean theorems certify the VALUES (forced equalities + disputed inequalities), not a from-first-principles category derivation.
