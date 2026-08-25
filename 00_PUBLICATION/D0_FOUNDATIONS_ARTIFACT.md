# Minimum description length as the axiom of a physical theory

*A self-contained statement of the results a foundations-of-physics reader can evaluate without
entering the D0 corpus. Every claim below names its machine-checked owner and its honest scope.*

---

## 1. The substitution

The operational reconstruction programme derives the complex Hilbert-space structure of quantum
mechanics from operational postulates — finite information capacity, continuity, and **tomographic
locality** (Hardy 2001; Chiribella–D'Ariano–Perinotti 2011; Masanes–Müller 2011).

D0 keeps the finite-capacity premise and replaces tomographic locality with a single admissibility
axiom:

> **M1.** If two constructions give the same class of distinguishable outcomes, the one requiring an
> extra mandatory external catalogue is inadmissible.

In Kolmogorov terms, adding an underivable `θ` moves a law from `K(T)` to `K(T) + K(θ|T)`: it
strictly lengthens the minimal description at unchanged predictive content. **M1 is minimum
description length applied to physical laws**, and its companion `M1⁺` (fix the canonical
representative, or pay for the choice index) is what terminates the regress
`a = b + c + c₁ + c₂ + …` that otherwise dissolves the distinction between a theorem and a fit.

That substitution — MDL in place of tomographic locality — is the novelty claim of this document.
Everything below is what it buys.

Owner: `D0-M1-PREDICATE-001` (`D0.Foundation.M1Predicate`), with grammar-stability under faithful
interpretations in `D0.Foundation.M1Universality` (kernel-checked countermodels show both transport
directions load-bearing).

---

## 2. Linearity of superposition, derived

Linearity is **postulate I** in every standard axiomatisation. Here it is a consequence.

- *Arity is exactly 2.* A connection law between given states cannot ignore its inputs, cannot
  depend on one only, and cannot demand a third argument not derived from the data — that third
  argument would be an exogenous parameter.
- *No interaction term.* To admit `P(S,T) = S ⊕ T ⊕ G(S,T)` one must fix a functional form and a
  coupling constant `γ`. A `γ` not derived from `S,T` is a catalogue entry; and the choice does not
  terminate — admitting `γ₁(S·T)` licenses `γ₂(S²·T)`, and truncating the series presupposes prior
  knowledge of scales, which is a catalogue again. The unique catalogue-free form has no interaction
  term.
- *Coefficients.* Symmetry gives `a = b`; a common scale `a ≠ 1` is a free constant, removed by unit
  calibration.

Scope: this is an argument from M1, not a theorem over a formalised space of connection laws. Its
strength is the same as the operational postulates' — it constrains admissible laws, it does not
compute one. Source: BOOK_01 §01.6.0.

---

## 3. The Born rule's quadratic form, including the case Gleason cannot reach

Gleason's theorem requires `dim ≥ 3`. In dimension 2 the Born rule does **not** follow from frame
functions — a named open loophole, closed in the literature only by moving to POVMs (Busch 2003;
Caves–Fuchs–Manne–Renes 2004).

D0 closes it from M1: a phase-blind response on a two-component amplitude must be invariant under
the quarter-turn `J(x,y) = (−y, x)`, and `x² + y²` is the unique quadratic form with that
invariance. Owners: `D0.Core.BornQuadraticResponse`, `D0-SYMPLECTIC-GLEASON-001`.

**A correction of record.** The corpus previously justified this by *symplectic-area preservation*.
That is false as stated and is now machine-checked false: the shear `(x,y) ↦ (x+y, y)` has `det = 1`,
is area-preserving, does **not** preserve `x² + y²` (norm `2 → 5` at `(1,1)`), and preserves a
different quadratic form instead. Area preservation is strictly weaker than what the argument needs.
The load-bearing premise is invariance under a specific order-4 rotation — phase blindness — which
is what the Lean owner always used. Negative control:
`D0-BORN-AREA-PRESERVATION-INSUFFICIENT-NOGO-001` (`D0.Core.BornAreaPreservationNoGo`).

Relation to the literature: Busch's POVM route reaches the same conclusion. The narrower and
stronger D0 claim is *the same closure from M1 without POVM axiomatics* — not priority over Busch.

---

## 4. Why φ, with the equation as an output

φ appears throughout the corpus. The honest question is whether it is selected or assumed.

**The audit first.** Of four "independent routes" the books claimed, three were readings of one
object: the Galois route *is* `x² − x − 1`; the dynamical fixed point `r = 1 + 1/r` is that equation
multiplied by `r`; the icosian/`E₈` route takes φ in as the coefficient ring `ℤ[φ]`. The arithmetic
route had independent content but two defects: Hurwitz extremality selects the entire `GL(2,ℤ)`
noble **class** (φ, `1/φ`, `2+φ`, `(φ+1)/(φ+2)` all attain `1/√5`), and the formal owner quantified
over `D0ResponseRoot x := 0 < x ∧ x + x² = 1` — i.e. it maximised *inside* the detector route's own
equation family.

**The repair.** Two steps, neither mentioning the target equation:

1. **Hurwitz over all reals** (external, 1891) selects the noble class.
2. **`M1⁺` canonization** selects the representative: within the period-one continued fractions
   `[n;n,n,…]` — roots of `x² − nx − 1`, discriminant `n² + 4` — minimal description selects `n = 1`
   uniquely, giving discriminant 5 and `(1+√5)/2`.

At `n = 1` the equation `x² − x − 1 = 0` is the **conclusion**. Negative control: `n = 2` gives
discriminant 8 and `1 + √2`, so the canonization step can fail and is load-bearing. Owner:
`D0-PHI-HURWITZ-CLASS-CANONIZATION-001` (`D0.NumberTheory.HurwitzClassCanonization`).

**A second, genuinely independent route.** Jones (1983) forces the subfactor index below 4 into
`{4cos²(π/n)}`. Finite depth gives `index < 4`; the corpus's own M1 rational-capture clause (a
rational value is captured at a finite stage, hence indistinguishable from a periodic catalogue
entry) gives irrationality; and by Niven the slots at `n = 3,4,6` are the rationals `1,2,3`, so the
least irrational slot is `n = 5`, with value `(3+√5)/2 = φ²`. Again φ is the output. Owner:
`D0-JONES-SLOT-SELECTOR-001` (`D0.NumberTheory.JonesSlotSelector`).

---

## 5. The arrow of time as a corollary

The thermodynamic arrow normally requires an independent low-entropy past hypothesis. Here
information time `I(t) = −log P(t)` is monotone because the heat trace of a finite graph Laplacian
decays — a spectral property, not a boundary condition. The time layer is two-dimensional because
`deg ℚ(φ) = 2`, and a smooth Markov partition of a toral automorphism exists **iff** the spectrum is
Pisot (Adler–Weiss 1967), so 2 is the only pathology-free dimension; three-dimensional time would
meet the Bowen/Kenyon–Vershik non-smoothness. Owners: `D0-PISOT-CONTRACTION-TIME-ARROW-001`,
`D0-TIME-2D-PISOT-001`, BOOK_06 §06.30a.

Audited scope: the books claim three independent routes to the arrow; two of them (Fibonacci-fusion
non-invertibility and the eigenvalue split of the time operator) share the golden quadratic and
collapse to one. **Two** routes survive — the commutator obstruction `[J,Y] ≠ 0` and the golden
quadratic — making the arrow the first object outside φ with genuine support multiplicity.

---

## 6. The role algebra, pinned by a classification theorem

A non-normal subgroup would force recording *which* conjugate copy — a catalogue — so every subgroup
of the role group is normal; order memory forbids abelian; hence the group is Hamiltonian; and by
Baer (1933) every Hamiltonian group is `Q₈ × B × D`. So `Q₈` is a forced **factor** of any such
group, not the smallest example a search happened to find. Owner: `D0-Q8-DEDEKIND-MINIMALITY-001`,
BOOK_02 §02.18.1.

---

## 7. The thesis, and how far it is carried

The corpus's central claim is that structure is not assembled but *unfolded*: each level exists
because the one below provably fails a named distinguishability obligation. Formalized shape — per
floor, an obligation recorded at both carriers, an `insufficient` lemma, and a `control` exhibiting a
structure that *does* satisfy it (without which the obligation is vacuous and forces nothing).

Four floors are carried, machine-checked:

| floor | obligation | fails on | repaired by |
|---|---|---|---|
| 2→3 | verifiability — the acceptor must be able to fail | a monopoly acceptor (provably constant) | the dyad: direct vs return |
| 4→5 | operation memory — the state determines its history | one `ℤ` register | two registers |
| 5→6 | order memory — the record distinguishes `ab` from `ba` | `π₁(T²) = ℤ×ℤ`, abelian | `S₃`, and `Q₈` |
| 6→7 | non-capture — no finite stage matches the scale ratio | any rational ratio | an irrational one |

And the property that makes it a cascade rather than a list: **the repair at one floor is the failure
at the next.** The two-register carrier that fixes floor 4→5 *is* `ℤ × ℤ`, which is abelian, so it is
precisely what floor 5→6 rejects. The unfolding cannot stop at its own repair.

The counting half — "three insufficiencies, hence three zones" — is carried only as a **lower
bound**: because the operation-memory repair provably fails order memory, one structural addition
cannot discharge both, so the chain past the register model is at least two steps. The *exact* count
is not claimed and is marked open.

Owners: `D0-CASCADE-CHAIN-SCAFFOLD-001`, `D0-CASCADE-FLOOR-COMPARISON-001`,
`D0-CASCADE-FLOOR-ONE-LOOP-001`, `D0-CASCADE-FLOOR-ORDER-MEMORY-001`,
`D0-CASCADE-FLOOR-SCALE-RATIO-001`. The remaining floors — defect⇒closure⇒shell, three
insufficiencies⇒three zones — are open, and the chain claim
`D0-CASCADE-INSUFFICIENCY-CHAIN-001` stays `PROOF-TARGET`.

---

## 8. What this does not claim

- **No discriminating empirical confirmation exists.** Survivors against downloaded data are
  single-number or bridge matches; the PMNS and LIGO passports were demoted to post-hoc fits after
  self-audit; the SPARC phason-halo dark-matter kernel is an honest negative, rejected in ~91% of
  galaxies; the DESI thawing-corner reading was an over-read and is corrected.
- **The gap-labelling channel does not discriminate.** It was the most plausible route to a
  laboratory test — Fibonacci gap labels are measured in photonic and cold-atom platforms — and was
  checked before any comparison: all 25 computed plateaux lie in `ℤ + ℤ/φ`, Bellissard's module for
  *any* Fibonacci hull. A measurement agreeing with them distinguishes nothing
  (`D0-GAP-LABEL-GENERICITY-NOGO-001`).
- **α is not derived.** `α⁻¹ = 359φ⁻² − φ⁻⁵ + φ⁻¹⁷(1+lnφ·sin(12/5))` matches CODATA to nine digits,
  but an exhaustive sweep shows the leading two-term structure is rare while the third term's ratio
  is fitted. Roughly 5.5 digits are structural; the rest is a consequence-grade check.
- **Multiplicity of forcing routes is mostly absent.** Of 19 assertions in the books that some object
  is forced by several independent routes, none survived audit in its original form: five shared a
  load-bearing premise, two were decomposition (mechanisms forcing *different components*, which buys
  no redundancy), one was external corroboration correctly labelled, one was partially right. Two
  have since been repaired to genuine independence. The current honest count of objects with real
  multiple support is **two**.

---

## 9. Reproduction

```bash
lake build D0.All                          # Lean 4 + mathlib, 0 sorry
python tools/validate_csv.py               # registry integrity
python tools/d0_route_audit.py --strict    # no unadjudicated independence claim
python tools/check_value_ledger_sync.py    # value ranking is a live view
python 05_CERTS/vp_gap_label_genericity_nogo.py
```

Every result above is one registry row with a named Lean module or a can-fail certificate. The
registry, the route audit and the value ranking are regenerated views, not hand-maintained prose.
