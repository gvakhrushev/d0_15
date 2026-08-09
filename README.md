# D0 — v15

**A finite theory of physics whose axiom is minimum description length, and which is built to know exactly where its own knowledge ends.**

Repository: **[github.com/gvakhrushev/d0_15](https://github.com/gvakhrushev/d0_15)** · Lean 4 (mathlib) + deterministic Python certificates · `lake build D0.All` green, 0 `sorry` · 53/53 guard scripts pass.

---

## The axiom

Everything below descends from one principle, **M1**:

> If two constructions give the same class of distinguishable outcomes, the one requiring an extra mandatory external catalogue is inadmissible.

This is not an aesthetic preference. In Kolmogorov terms, adding an underivable `θ` moves a law from `K(T)` to `K(T) + K(θ|T)` — it strictly lengthens the minimal description at unchanged predictive content. **M1 is minimum description length applied to physical laws** ([BOOK_00 §0.3.1](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md)), and it is what terminates the infinite regress `a = b + c + c₁ + c₂ + …` that otherwise collapses the distinction between theorem and fit.

The operational reconstruction programme (Hardy 2001; Chiribella–D'Ariano–Perinotti 2011; Masanes–Müller 2011) derives complex Hilbert space from finite information capacity plus tomographic locality. D0 takes a **different entry point to the same target**: MDL instead of tomographic locality. That substitution is the theory's actual novelty claim.

## The results, ranked by value

Ranking is [computed, not asserted](03_THEORY_MAP/D0_VALUE_RANKED.md) — structural weight in the derivation chain, semantic load of the formal statement, falsifiability reach, foundation position, and declared external significance (every weight carrying a [named external question and citation](03_THEORY_MAP/D0_EXTERNAL_SIGNIFICANCE.csv), disputable per row).

| result | what it answers outside D0 | status |
|---|---|---|
| **Linearity of superposition is derived, not postulated** (`D0-BRANCH-SYMPLECTIC-FORCING-001`) | Linearity is postulate I in every standard axiomatisation. Here: a mediator's arity is forced to 2, any interaction term needs a coupling constant = a catalogue, and truncating the resulting series presupposes a scale catalogue. The only catalogue-free form has no interaction term. [§01.6.0](01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md) | CORE-FORMALIZED |
| **The Born rule's quadratic form, including the 2D case Gleason cannot reach** (`D0-SYMPLECTIC-GLEASON-001`, `D0-BORN-QUADRATIC-ORIGIN-001`) | Gleason's theorem requires dim ≥ 3; in dim 2 the Born rule is a known open loophole, closed in the literature only by moving to POVMs (Busch 2003). D0 closes it from M1: a phase-blind response must be invariant under the **quarter-turn** `J(x,y)=(-y,x)`, and `x²+y²` is the unique such quadratic form. *Scope, corrected 2026-07: this is invariance under a specific order-4 rotation, **not** symplectic-area preservation — the shear is area-preserving and does not fix `x²+y²` (machine-checked negative control, `D0-BORN-AREA-PRESERVATION-INSUFFICIENT-NOGO-001`).* [§01.6.1b, §01.17.1a](01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md) | CORE-FORMALIZED |
| **φ is selected by minimum description length** (`D0-PHI-HURWITZ-001`) | Why φ and not another constant? Because `φ = [1;1,1,1,…]` is the irrational whose continued fraction stores no information — the MDL optimum — and by Hurwitz it is maximally resistant to rational capture *at every truncation depth*, hence compatible with the inverse limit. *Scope: the corpus presents this as one of several **independent** routes alongside `p+p²=1` and Fibonacci fusion. That independence does not currently hold — the formal owner quantifies over `D0ResponseRoot x := 0 < x ∧ x + x² = 1`, i.e. it maximises **inside** the detector route's own equation family, and `1/√5` is just `1/√disc(x²−x−1)`. Treated as one route with several readings until a genuinely independent second route is proved; see the [route audit](03_THEORY_MAP/D0_FORCING_ROUTES.json).* | CORE-FORMALIZED |
| **The arrow of time is a corollary, not a postulate** (`D0-PISOT-CONTRACTION-TIME-ARROW-001`) | The thermodynamic arrow normally requires an independent low-entropy past hypothesis. Here information time `I(t) = −log P(t)` is monotone because the heat trace decays — a spectral property of a finite Laplacian. The time layer is 2-dimensional because `deg ℚ(φ) = 2`, and a smooth Markov partition exists **iff** the spectrum is Pisot, so 2 is the only pathology-free dimension. [§06.30a](01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md) | CORE-FORMALIZED |
| **Lorentzian signature from tripartiteness alone** (`D0-SIGNATURE-31-SPLIT-001`, `D0-RANK3-METRIC-TRANSPORT-001`) | Recovering `(3,1)` rather than assuming it is an open problem shared by causal sets, CDT and spin foams. The equitable quotient of any 3-zone graph has characteristic polynomial `λ³ − e₂λ − 2e₃`; with zero trace and positive `e₃` this forces exactly one positive and two negative eigenvalues. Space rank 3 is proved on the literal 33×33 adjacency matrix. **Falsifier**: the two negative eigenvalues split unless the zones are equal — the carrier-level spatial form is anisotropic. | CORE-FORMALIZED |
| **The role algebra is pinned by a classification theorem** (`D0-Q8-DEDEKIND-MINIMALITY-001`) | Not "the smallest example a search found": a non-normal subgroup would force recording *which* conjugate copy = a catalogue, so all subgroups are normal; order memory forbids abelian; hence Hamiltonian; and by Baer 1933 every Hamiltonian group is `Q₈ × B × D`, so `Q₈` is a forced **factor**, not a minimal instance. [§02.18.1](01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md) | CORE-FORMALIZED |
| **M1 itself is a proven predicate, and grammar-stable** (`D0-M1-PREDICATE-001`) | The exogenous-parameter test transports and reflects along faithful interpretations, with kernel-checked countermodels showing each direction load-bearing — so the criterion is not parochial to D0's own vocabulary. | CORE-FORMALIZED |

The scene **K(9,11,13)** (33 vertices, 359 edges, role algebra `Q₈`) is the object these forcings converge on; the α-line, the mass chain and the cosmology sector are its representation theory. Those are downstream and are *not* the entry point — see the honest status below.

**For a foundations reader:** [`D0_FOUNDATIONS_ARTIFACT.md`](00_PUBLICATION/D0_FOUNDATIONS_ARTIFACT.md) states the above self-contained, with every claim's machine-checked owner and its scope, and requires no entry into the corpus.

## The honest boundary

**No sharp multi-point discriminating confirmation exists.** This is stated first because it is what a physicist needs to know before reading anything else. From the [external-data scoreboard](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md), against downloaded data:

- **Survivors** are single-number or bridge matches: `sin²θ_W` on-shell (0.23σ), `m_s/m_d = 20` (0.02σ), the Coldea `φ`, the α leading term, the PDG seam-α falsifier.
- **Demoted after self-audit**: the PMNS `δ₀`-family and the LIGO `φ⁻¹` mass-defect are post-hoc passport fits, not discriminating.
- **Honest negative**: the SPARC phason-halo dark-matter kernel is rejected in ~91% of galaxies.
- **Corrected over-read**: DESI DR2 confirms *evolving* dark energy but not the specific thawing corner.

On the flagship α line: `α⁻¹ = 359φ⁻² − φ⁻⁵ + φ⁻¹⁷(1+lnφ·sin(12/5))`. The leading term is structurally rare — an exhaustive sweep of `N·φᵖ + m·φᵠ` over `N ≤ 500`, `|m| ≤ 12`, exponents to ±20 finds exactly **one** value within `4·10⁻⁴` of `α⁻¹`, and it is this one. But the third term's ratio is fitted, and simple alternatives fit it better. So roughly 5.5 digits are structural and the rest is a consequence-grade check — the registry says so, and so does this README.

The theory is at the stage where the mathematical structure is being built and the discriminating test does not yet exist. Gap labelling was the most plausible route to one — Fibonacci-quasicrystal gap labels are *measured* in photonic and cold-atom platforms rather than Planck-suppressed — and it was checked before any comparison with data: **the D0 label set is generic** (`D0-GAP-LABEL-GENERICITY-NOGO-001`). All 25 computed plateaux lie in `ℤ + ℤ/φ`, Bellissard's module for *any* Fibonacci hull, so a measurement agreeing with them distinguishes nothing. The channel revives only if a forced gap-opening *subset* is derived. Recorded as a closed lead, in the same class as the SPARC dark-matter negative.

## The structural defect worth knowing about first

The corpus repeatedly claims an object is forced by **several independent routes** — "two independent
forcings of φ", "two-channel forced centre", "(3,1) from two distinct mechanisms". That redundancy is
what would make the structure antifragile: kill one route, the object survives.

An adversarial audit of 20 of the 82 such claims ([route audit](03_THEORY_MAP/D0_FORCING_ROUTES.json))
found **none** of the 20 independent — each pair or family shares a load-bearing premise. Three spot
checks, verified by hand:

- the machine-checked Hurwitz/phase-generator uniqueness quantifies over `D0ResponseRoot x := 0 < x ∧ x + x² = 1`, so the "MDL route" to φ is formalised *inside* the detector route's equation family;
- the two routes to the Born quadratic are the same three-line computation on the same map `J`, and the stated weaker premise (area preservation) is provably insufficient;
- the registry itself already mints `D0-P-DEGREE2-EXHAUSTION-001` as the *shared parent* of several claims the books present as independent.

A second failure mode surfaced in the hand audit: several assertions are **decomposition, not
redundancy**. BOOK_06 §06.30a derives the `3` of `(3,1)` from a graph rank and the `1` from a Pisot
flow — each mechanism forcing a *different component*. That is correct mathematics and zero
antifragility: kill either and its component is gone, because neither covers for the other.

Nothing here refutes a theorem. What collapses is the **redundancy**: the structure is more
single-threaded than the prose says.

**Two routes have since been repaired to genuine independence, machine-checked** — the arithmetic
route to φ (`D0-PHI-HURWITZ-CLASS-CANONIZATION-001`: Hurwitz selects the `GL(2,ℤ)` noble class,
`M1⁺` canonization selects the representative, and `x²−x−1` comes out as the *conclusion*) and the
Jones channel (`D0-JONES-SLOT-SELECTOR-001`: external quantization + the owned M1 rational-capture
clause select `n=5`, and `φ` is the output). Under φ — the corpus's most load-bearing object — there
is now a real pair of independent supports rather than a claimed one.

Proving a genuinely independent second route to any remaining high-load object is the highest-value
theorem available: it strengthens everything above that object and needs no new empirical input.
Ranked targets: the fragile joints in [the architecture map](03_THEORY_MAP/D0_ARCHITECTURE.md);
full inventory of assertions in [the route inventory](03_THEORY_MAP/D0_ROUTE_INVENTORY.md).

## Where to attack

The [attack queue](03_THEORY_MAP/D0_VALUE_RANKED.md#1-attack-queue--highest-value-not-yet-closed) is the ranked list of claims that are high-value **and** open — closing anything on it moves the corpus, closing anything below it does not. Also standing:

- **Refute a bridge** — 25 named external assumptions, each with an owner file and a written failure condition ([ledger](09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv)).
- **Exhibit a second object** against any uniqueness row — the kill rule works for outsiders.
- **Break a certificate** — every cert must be able to fail (`check_cert_can_fail.py` enforces it).
- **The root**: `D_anchor = 4`, `D_Σ = 5` and the `+2` step rest on the M1 squeeze (`N < D` loses distinguishability; `N > D` needs a significance catalogue). The lower branch is solid; the upper branch is carried by MDL plus canonization (`M1+`). That is the load-bearing argument of the whole scene selection.

## Repository layout

| Path | Contents |
|---|---|
| [`01_BOOKS/`](01_BOOKS/) | the theoretical spine — `BOOK_00` is the entry contract; `BOOK_01`–`08` the mathematics and physics |
| [`03_THEORY_MAP/`](03_THEORY_MAP/) | **[value ranking](03_THEORY_MAP/D0_VALUE_RANKED.md)**, **[derivation chain](03_THEORY_MAP/D0_LOGIC_CHAIN.json)**, dependency graph, status map, scoreboard |
| [`05_CERTS/`](05_CERTS/) | deterministic `vp_*.py` certificates with reachable FAIL controls |
| [`08_PASSPORTS/`](08_PASSPORTS/) | curated external data (PDG, DESI, CMB, LIGO, SPARC…) + SHA256 manifests and the real-data scoreboard |
| [`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/) | the Lean 4 package; the canonical registry and the **[value ledger](09_LEAN_FORMALIZATION/docs/D0_VALUE_LEDGER.csv)** under `docs/` |
| [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/) | Rosetta stone: every D0 mnemonic in conventional terms |
| [`tools/`](tools/) | guard scripts, registry sync, the value model and the chain builder |

## Registry, by the numbers

Counts come last on purpose: they measure bookkeeping, not insight. 563 claims — 377 `LEAN_PROVED` (+29 with named bridge assumptions), 109 python-certified, 80 proved impossibilities, 58 open proof-targets, 25 declared external bridges. The [derivation chain](03_THEORY_MAP/D0_LOGIC_CHAIN.json) reports the shape honestly: **205 of 424 Lean-backed claims are genesis blocks** — they import no other D0 module — and the maximum derivation depth is 10. The corpus is currently wide, not deep; connecting those islands is the structural work ahead.

## Getting started

```bash
pip install -r requirements.txt
python tools/d0_logic_chain.py        # rebuild the derivation chain + block hashes
python tools/d0_value_model.py        # rebuild the value ledger and the ranking
python tools/validate_csv.py          # registry integrity
python 05_CERTS/vp_status_inflation_audit.py   # anti-promotion audit (its control must fire)
```

Lean (heavy build artifacts live outside the repo):

```bash
./tools/lean_dev.ps1 build D0.All
python 09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py
```

## Method

The corpus is built by an adversarial forcing loop — pre-flight against the registry, compute first with can-fail certificates, a memo with a pre-registered attack surface, then an independent skeptic with a kill mandate. Kills are accepted in full and recorded with their refuting object. Details: [the engine](D0_EPISTEMIC_ENGINE_README.md) · [domain-independent spec](docs/ADVERSARIAL_FORCING_ENGINE_SPEC.md) · [closure contract](D0_CLAIM_CLOSURE_CONTRACT.md).

## License / status

Private research snapshot (**v15**). Contact the author for usage or collaboration.
