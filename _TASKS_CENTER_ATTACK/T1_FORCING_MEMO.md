# T1 FORCING MEMO — the scene-native refinement rule (DRAFT, candidate-THE, no status claimed)

**Author:** chief researcher. **Status of this document:** DRAFT forcing argument in the DEF-0.2.2
schema, submitted for adversarial review. It edits no registry row; `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`
and `PRIM-SCENE-HISTORY-REFINEMENT-RULE` remain in force until this memo survives review and a
Lean/cert owner is minted under the closure protocol.

## Claim X

The M1-admissible scene-native history refinement rule on K(9,11,13) is unique: **NB** — the family
of all compositions of *advance* moves on the directed-edge carrier (the Hashimoto transfer), with the
Ihara–Bass identity as the canonical comparison map Ξ between the 718-dim transfer and the 33-dim
scene data (A, D).

## Step alphabet (exhaustive dichotomy — no third option)

A history step from directed edge (u→v) goes to some (v→w). Either w = u (**return**) or w ≠ u
(**advance**). This is a complete, disjoint dichotomy on the step alphabet. The three vNext2 families
are exactly: W = endpoint compression of {advance ∪ return}∗; E = full edge-transfer (de Bruijn,
includes return transitions); NB = {advance}∗ (Hashimoto). (Family constructions: W1 report;
`D0/VNext2/SceneNativeRefinementClassification.lean`.)

## The forcing (DEF-0.2.2 instantiation)

Assume ¬X. Then the admissible family either (A) contains a return step, or (B) is a proper
restriction/extension of {advance}∗ that is not W or E.

**(A) kills W and E.** The return move is not a free letter: it is already a typed channel of the
grammar — the p²-return/comparison channel of the detector closure p + p² = 1 (BOOK_00 §00.3), with
its own weight and role. A family containing return steps registers the same physical act twice: once
as the typed channel, once as a history letter. To keep the distinguishable outcome class unchanged,
the family must then carry a rule θ separating "channel-return" occurrences from "history-return"
occurrences — a which-copy register. θ affects distinguishable outcomes (it reweights every closed
walk containing a backtrack), is not derivable from prior DEF/THE, and is not part of the
distinguishability protocol: θ is exogenous (DEF 0.3.1), ⊥M1. This is the same blade that excluded
the candidate 40 in the Λ_act uniqueness control (§03.20, "double-counts witness endpoint").

*Exact arithmetic witness (cert-backed, `vp_scene_ihara_bass_nb.py`, PASS):* the depth-2 excess of W
over NB is Σd² − Σd(d−1) = 15708 − 14990 = 718 = 2|E| — exactly one immediate return per directed
edge, i.e. the excess *is* the return channel, enumerated once per edge orientation. E contains the
same transitions at operator level (W1 report: E = de Bruijn edge transfer ⊇ backtracks).

**(B) kills every sub/super-family.** A family that drops some advance moves needs a selection rule
θ′ ("which advances are excluded") not derivable from prior structure — an exogenous catalog, ⊥M1.
A family that adds letters beyond the step alphabet contradicts the dichotomy above. Hence ¬X is
impossible and X is forced. ∎ (pending review)

## Completeness guard — nothing is discarded

The obvious objection: "excluding returns loses the p²-channel information." Ihara–Bass answers it
exactly, on this scene (cert-verified, modular determinants, 5 rational points × 3 primes):

```
det(I − uB) = (1 − u²)^(|E|−|V|) · det(I − uA + u²(D − I)),   |E|−|V| = 326
```

The right side *is* the all-walks data (A, D) with the backtrack correction u²(D−I) appearing as a
separately-typed term; the left side is pure NB transfer. The identity says: the return channel is
**factored**, not discarded — which is exactly the D0 requirement (typed channel, not history letter).
External owner: Hashimoto 1989 / Bass 1992; the identity requires no regularity (W5 report), and the
md ≥ 2 hypothesis holds (scene degrees 20/22/24).

## Consequences if this survives review

1. `PRIM-SCENE-HISTORY-REFINEMENT-RULE` is discharged: the rule is NB, Ξ = Ihara–Bass.
2. The vNext2 Outcome D collapses from "≥2 inequivalent admissible families" to "one admissible,
   two excluded by the double-count blade" — the downstream gates (Ξ, Dirac scale, spectral lift)
   reopen against the NB transfer.
3. FINDING (no promotion here): the nonzero adjacency charpoly of the scene is λ³ − 359λ − 2574 —
   the §08.12.4 "vacuum cubic". Since the Ihara–Bass side lives in unnormalized (A, D), a forced NB
   rule bears on the cubic-vs-quadratic fork; to be examined separately, not asserted.

## Named open obligations (what review must attack)

1. **The which-copy step.** (A) needs the sharpest form of "double registration ⇒ mandatory
   which-copy register ⇒ exogenous θ" checked against DEF 0.3.1's three clauses. If a reviewer can
   exhibit a return-containing family whose weights need *no* copy-separating rule (e.g. by absorbing
   the p² weight identically), (A) fails — name it.
2. **Family-space scope.** The dichotomy covers step-generated (Markov-on-edges) families, which is
   the class vNext2 itself classified. Non-step-generated (history-dependent) families need either
   exclusion by the same M1 blade (memory-of-history = register) or an explicit scope restriction of X.
3. **Weighted version.** The grammar's channels carry φ-weights; the cert verifies the unweighted
   identity. The weighted (typed) Ihara–Bass with p, p² on advance/return must be written and
   cert-verified — this is the natural follow-up cert.
4. **Owner minting.** Under `VERIFIED_CLOSURE_PROTOCOL.md`: grounded scout → Lean/cert owner →
   negative controls → gate. Nothing in this memo substitutes for that chain.
