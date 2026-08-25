# YUKAWA_COMMUTANT_SPECTRUM — resolution-2 mathematics + the honest numeric negative (POST-SKEPTIC 2026-08-03: 2× WOUNDED-FIXABLE, 0 kills, all repairs applied)

Campaign 3 item 4 of `NEXT_FRONT_PLAN_2026_08.md`, exploring resolution 2 of
`YUKAWA_COMMUTANT_TENSION_LOG.md` (2026-08-01). Lean: `D0.Synthesis.YukawaCommutantSpectrum`
(sorry-free, axioms `propext/Classical.choice/Quot.sound`, wired into `D0/All.lean`, 4466 jobs,
2026-08-03). **No row edited; the tension log's owner fork stays open; nothing minted.**

## Claims (DEF-0.2.2 form)

**C1 (Lean, positive — what the equivariant class guarantees).** If the Yukawa operator on the
generation 3-space is taken from the equivariant-and-adjacency-compatible class — the `ℚ[Q]`
identification being DOCSTRING-GRADE in the owner (`visible_centraliser_dim` is a placeholder
`rfl`; flagged exactly like spectral mapping, per skeptic W4; the Lean theorems quantify over
`(a,b,c)` literally and are self-contained) — then:

  1. `no_rational_root_rat`: the FULLY QUANTIFIED field statement `∀ q : ℚ, q³−359q−2574 ≠ 0`
     (new: all owned no-root statements are integer-divisor sweeps; the rational-root-theorem
     step and a self-contained integer exclusion close ℚ).
  2. `qq_spectrum_splits` — **automatic non-degeneracy**: EVERY non-scalar member takes pairwise
     distinct values on distinct transport roots. Mechanism: degeneracy forces `λ+μ = −b/c ∈ ℚ`,
     and the two root equations alone yield `(λ+μ)³ − 359(λ+μ) + 2574 = 0`, making `b/c` a
     rational root of the transport cubic — contradiction. *The irreducibility that defines the
     commutant is the same fact that forbids Yukawa degeneracy.*
  3. `transport_three_real_roots`: three distinct real roots WITH the locations EXPORTED in
     the statement, in the OWNED integer brackets `(−13,−12)`, `(−10,−9)`, `(21,22)` (ℚ sign
     table: `TransportNotGolden.transport_roots_bracketed` — an owner the first draft failed to
     cite, skeptic W1/W2). Realness priors: discriminant-grade "three distinct real roots" is
     already minted at `D0-MIXING-HIERARCHY-INVERSION-001`, `D0-RANK3-METRIC-TRANSPORT-001`,
     `D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001` (skeptic W3); the increment here is strictly
     "first Lean proposition with real-typed root existence + exported brackets".
  3'. `no_rational_value_at_root` (NEW, formalizing the skeptic's C2(b) counterexample):
     non-scalar members take IRRATIONAL values at every transport root — a rational value would
     make `b/c` (or a rational combination) a root of the cubic, same mechanism as splitting.
  4. Assembled `equivariant_yukawa_rigidity`: 9 free parameters (3×3 matrix) collapse to 3
     rational ones, with three non-degenerate generation values forced for every non-scalar
     choice.

**C2 (computed, negative — the honest numeric verdict the plan demanded).** Reproducible
(`numpy.roots([1,0,-359,-2574])`):

    roots  λ = −12.079099, −9.758283, 21.837382   (e₂ = −359 ✓, e₃ = 2574 ✓)
    |λ| ratios      : 1.2378, 1.8079          (spectrum of Q itself — parameter-free)
    λ² ratios       : 1.5322, 3.2684          (spectrum of Q² — parameter-free, positive)
    lepton targets  : m_μ/m_e = 206.768, m_τ/m_μ = 16.817

  (a) The **parameter-free members are falsified**, with corrected margins (skeptic wound 4):
      the kill is carried by the first ratio — factor ≥ 9.3 in the MOST favorable convention
      (m ~ y², spec Q²: required 14.38 vs available 1.53), and the second ratio misses by 1.25×
      there (4.10 vs 3.27) — the pair must match JOINTLY, so the falsification stands, but the
      margin reads "factor ≥ 9 on the first ratio in every convention", not "two orders of
      magnitude on both". Float-free confirmation from the EXPORTED owned brackets: all
      `|λ|`-ratios ≤ 22/9 < 2.5, squares < 6 — refuting 206.8/16.8 AND the √-targets 14.4/4.1
      without any float input. The plan's hope "eigenvalues forced to be the roots ⇒ hierarchy
      with no free matrix" is TRUE only for the member `Q` and is DEAD there. Honest negative
      recorded.
  (b) The **general member predicts nothing about ratios** — REPAIRED per the skeptic's second
      object (the triple `(0,1,2)`): `(a,b,c)` fits any real triple **to arbitrary precision**
      (V invertible, ℚ³ dense), NOT exactly — by our own mechanism, now theorem-grade
      (`no_rational_value_at_root`): non-scalar members never take rational values at roots, so
      the attainable set is a dense countable image, and rational targets are all UNATTAINABLE
      exactly. Zero predictive surplus survives unchanged: a falsifiable binding needs an owned
      selector of `(a,b,c)` — deliberately NOT named as a PRIM (owner's call).

**Net:** resolution 2's mathematics is now theorem-grade and its physics hope is honestly
bounded: what survives is structural (forced non-degeneracy + forced irrationality +
parametrization), not numeric. The tension log's fork (resolution 1 vs 2) remains the owner's;
C2 shifts the cost balance — resolution 2 now needs BOTH the carrier decision AND a selector.
Cross-reference (skeptic W5): the RIVAL owned hierarchy route needs no selector —
`D0-LEPTON-002` owns the integer part `L₁₁ + L₄ = 206` as THE, and
`D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001` (PROOF-TARGET) owns the shell-overlap+Puiseux route with
exponent row `(0, 1/4, 1/3)`; this strengthens the negative — the corpus's hierarchy story
already lives on a carrier where resolution 2's machinery is not needed.

## Owned pre-facts (verbatim, checked 2026-08-03)

1. Tension log: "Fitting `aI + bQ + cQ²` to the overlap's first row forces `(a,b,c) =
   (−108/11, −1/2, 1/22)`, whose second row is `(9/11, 13/11, −13/11) ≠ (1,0,1)`" ✓ (the
   scaffold ∉ ℚ[Q] fact this memo builds on).
2. `JointCommutant.lean:23-27`: "the joint commutant splits as `(centraliser of Q in M₃) ⊕ ℚ ⊕
   ℚ ⊕ ℚ`… irreducible over ℚ, so Q has three distinct eigenvalues and its centraliser is
   ℚ[Q], of dimension three" ✓.
3. `JointCommutant.lean:70`: `no_rational_root : ∀ r ∈ divisors2574, charQ r ≠ 0` (divisor-list
   grade — C1.1's increment is the full-ℚ statement) ✓.
4. Plan item 4 (`NEXT_FRONT_PLAN_2026_08.md:110-115`): "if the numerics are wrong, record the
   honest negative (the ratios are fixed, so this is immediately falsifiable)" ✓ — C2(a) is
   that record.
5. Tension log cross-ref: the Puiseux/Green-function leg lives on the 7-point shell torus, "a
   different carrier" — untouched here ✓.

## Pre-registered attack surface

- **ATT-1 (strongest, against C2(b)):** "zero predictive surplus" could be attacked by naming
  an owned constraint that already cuts `(a,b,c)` (e.g. a trace condition, positivity, an owned
  normalization). Defense: we know of none in the registry; if the skeptic names one, C2(b)
  rescopes to "surplus = named constraint count − 3" and the memo gains, not dies.
- **ATT-2 (spectral-mapping grade):** eigenvalues of `a+bQ+cQ²` = `a+bλ+cλ²` is used at
  docstring grade (standard spectral mapping), not formalized. A kill would need this to be
  load-bearing for a THEOREM; it is not — all theorems are about root values directly.
- **ATT-3 (universal check):** C1.2 quantifies over the WHOLE class — legitimate because ℚ[Q]
  is 3-dimensional by the owned Cayley–Hamilton argument; the quantifier runs over (a,b,c)
  literally. No unexhausted class (kill-shape 1 checked).
- **ATT-4 (carrier check):** everything lives on the visible generation 3-space — the same
  carrier as the owned commutant result. The lepton TABLE is on the empirical side and is only
  compared numerically, never bound (kill-shape 2 checked). The (m ~ y vs m ~ y²) convention
  does not rescue the fit: the first-ratio miss is ≥ 9.3× in every convention (√-targets 14.4,
  4.1 vs available 1.24/1.81 and 1.53/3.27; joint match required).
- **ATT-5 (numeric grade — TWICE repaired; final state):** the first draft's interval-only
  bound was WRONG (λ₂ ∈ (−10,0) bounds no ratio — both skeptics confirmed the flaw
  independently of the pre-verdict self-repair). Final state: the Lean statement EXPORTS the
  owned brackets `(−13,−12)`, `(−10,−9)`, `(21,22)` (ℚ sign table owned by
  `TransportNotGolden.transport_roots_bracketed`, now cited), giving float-free bounds
  `|λ₁|/|λ₂| ≤ 13/9 < 1.45`, `λ₃/|λ₁| ≤ 22/12 < 1.84`, `λ₃/|λ₂| ≤ 22/9 < 2.45`; squares < 6.
  These refute 206.8/16.8 and the √-targets 14.4/4.1 with no float input.

## Negative controls

- The splitting theorem can fail where it should: for the SCALAR member (b=c=0) the values
  coincide — excluded by hypothesis, and the hypothesis is necessary (control reachable).
- `no_integer_root`'s finite sweep covers ±21 and the tail bound is tight at 22 (22·(22²−359) =
  2750 > 2574 but 21·(21²−359) = 1722 < 2574 — the bound cannot be shrunk; sweep is not
  decorative).

## Status language

Candidate/DRAFT throughout; registry proposal (Tier 6 item 25) owner-gated; the tension-log
fork is untouched.


## SKEPTIC VERDICT (2026-08-03) — accepted in full, repairs applied

Two lenses (math / ownership): WOUNDED-FIXABLE, WOUNDED-FIXABLE, zero kills. Errors of record:

1. **ATT-5's stated defense failed** (both lenses independently): the "interval-only" bound
   imported a numpy root and the intervals as then stated bounded no ratio. REPAIRED: statement
   now exports the owned brackets; float-free bounds rederived above. (A pre-verdict
   self-repair had tightened the intervals, but still without citing the owner.)
2. **Missed owner in preflight**: `TransportNotGolden.transport_roots_bracketed` (ℚ sign table
   with tighter brackets) was not cited; three minted discriminant-grade realness rows also
   uncited. REPAIRED: all cited; "first formal realness" scoped to "first real-typed existence
   proposition".
3. **C2(b) "fits exactly" was false by our own mechanism** (skeptic's second object: the triple
   (0,1,2)): non-scalar members never take rational values at roots. REPAIRED: "to arbitrary
   precision (dense countable image)"; the counterexample formalized as
   `no_rational_value_at_root` — the memo GAINED a theorem from the kill attempt.
4. **Margin overstatement**: "two orders of magnitude on both ratios" → corrected to "factor
   ≥ 9 on the first ratio in every convention; joint match required".
5. **Registry item 25 misstated the Lean content** (brackets). REPAIRED below and in the
   proposals file.
6. **Class-identification grade**: ℚ[Q] = centraliser is docstring-grade in the owner
   (`visible_centraliser_dim` is placeholder `rfl`). REPAIRED: flagged like spectral mapping.
7. **Rival owned route unacknowledged** (L₁₁+L₄ = 206 THE; Puiseux exponents). REPAIRED:
   cross-referenced in Net — strengthens the negative.
