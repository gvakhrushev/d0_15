# D0 — v15

**A finite theory of physics whose single axiom is minimum description length, stated as
exact theorems: hypotheses inside every statement, conclusions machine-checked, open
problems named as targets.**

Repository: **[github.com/gvakhrushev/d0_15](https://github.com/gvakhrushev/d0_15)** ·
Lean 4 (mathlib) + deterministic Python certificates · `lake build D0.All` green, 0
`sorry`, 4476 jobs · full guard gate green.

**The results, stated exactly: [`D0_EXACT_RESULTS.md`](D0_EXACT_RESULTS.md)** — 24 theorems,
7 no-go theorems, 5 named open problems. Everything below is a digest of that ledger.

---

## The axiom

Everything descends from one principle, **M1**:

> If two constructions give the same class of distinguishable outcomes, the one requiring an
> extra mandatory external catalogue is inadmissible.

In Kolmogorov terms: an underivable `θ` moves a law from `K(T)` to `K(T) + K(θ|T)` — a
strictly longer minimal description at unchanged predictive content. **M1 is minimum
description length applied to physical laws** ([BOOK_00 §0.3.1](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md)).
The operational reconstruction programme (Hardy 2001; Chiribella–D'Ariano–Perinotti 2011;
Masanes–Müller 2011) derives complex Hilbert space from finite capacity plus tomographic
locality; D0 reaches the same target from MDL instead of tomographic locality. That
substitution is the novelty claim; M1 is a proven predicate whose derivability clause is
grammar-functorial (`D0-M1-PREDICATE-001`, `D0-M1-UNIVERSALITY-001`).

## What is proved (digest — exact forms in the [ledger](D0_EXACT_RESULTS.md))

**Quantum mechanics.** Linearity of superposition: the unique catalogue-free mediator
evolution has no interaction term (T1). The Born quadratic `x²+y²` is the unique phase-blind
form invariant under the quarter-turn `J` — a hypothesis that covers dimension 2, where
Gleason does not apply; the weaker area-preservation hypothesis provably does not suffice
(T2, with machine-checked counterexample). The role algebra: all-subgroups-normal +
non-abelian ⇒ Hamiltonian ⇒ `Q₈` is a forced factor by Baer's classification (T3). The
arrow of time is heat-trace monotonicity of a finite Laplacian; the time layer has dimension
`deg ℚ(φ) = 2`, the unique Pisot-clean choice (T5).

**Geometry.** For any 3-zone scene the quotient cubic is `λ³ − e₂λ − 2e₃`, forcing
signature (1,2); on K(9,11,13) the coefficients ARE the scene: `e₂ = 359 = |E|`,
`2e₃ = 2574` (T6–T7). The spectrum data `(D,H,M₂)` determine the zone triple — inverse
spectral rigidity with every hypothesis load-bearing (T8). The multiplicative pair
`(1287, 960)` has the unique preimage `(9,11,13)` over all part counts (T9). The dark
sector is exactly the Aut-invariant-free part of `ker A` (T10).

**One invariant, five sectors.** The edge count `359` is the identical owned object in the
discrete Einstein–Hilbert proxy, the α leading term, the metric cubic, the Yukawa
non-degeneracy, and the S_DE window product `359/160` — with a certificate whose control
moves every structural face together on a rival scene, and a proven no-intertwiner ceiling
(Bézout certificate `39590739579959`) (T13).

**Golden/toral calculus.** `Tr(Tⁿ) = (−1)ⁿLₙ`; `(φ⁻¹)ⁿ = (−1)ⁿ(Lₙ − φⁿ)`; the composition
law `L_{m+n} = L_mL_n − (−1)ⁿL_{m−n}` transports to traces; at `17 = 12+5`:
`L₁₇ = L₁₂L₅ + L₇` with the correction forced by `det T⁵ = −1`, and
`φ⁻¹⁷ = (φ⁵−11)(322−φ¹²)` — both factors of the α depth are return defects of one toral
automorphism (T14).

**The α line.** `ζ_E(0) = 359` and `ζ_E(−1) = 359φ⁻² − φ⁻⁵ = α_top⁻¹`, exact in ℤ[φ] (T17;
the pre-refactor sweep-uniqueness claim failed reproduction and is retired — the true sweep
combinatorics are pinned by a can-fail certificate, see T17). Of the dressing: angle `12/5`, `sin` channel, seam
factor `ξ₅`, linear form — each an exact theorem; under the five named hypotheses of T18
the per-crossing weight is exactly `φ⁻¹`. And a full-closure negative: `√5` lies outside
the entire splitting field of the transport cubic (`Gal = S₃`, discriminant certificates
mod 9 and mod 7) — no rational-coefficient function of all transport eigenvalues jointly
produces golden content, so the φ-power mechanism's only owned home is the toral return
system (T19–T20).

**The cascade** (the central thesis, carried part): seven insufficiency floors, each with a
proved insufficiency and satisfiable control; four interlock links of the exact shape *the
repair of floor n is the failing carrier of floor n+1*; the count **3** derived from the
closure structure itself (least reflection-closed completion of the two interior layers —
no `3 ≤ _` hypothesis anywhere); all of it composed in one clean-axiom theorem
(T21–T24).

**No-go theorems** are exact results, not caveats: transport spectrum blindness, ΛCDM
excluded by degeneracies alone in the ratio reading, gap-label genericity (the 25 computed
plateaux all lie in the module of any Fibonacci hull — such a measurement cannot
discriminate D0; revival condition: a forced gap-opening subset), equivariant seam
vanishing, three dead count routes (N1–N7; reopening conditions live in the registry rows).

## Open problems ([ledger §Open problems](D0_EXACT_RESULTS.md#open-problems-named-targets-not-qualifications))

- **P1** — a second forcing route to φ with premises disjoint from the detector equation
  family (one repaired pair exists: Hurwitz-class canonization + Jones slot; the route audit
  found 0/20 sampled multiplicity claims independent — proving one more is the
  highest-value theorem available).
- **P2** — the α depth total `φ⁻¹⁷ = ξ₅·φ⁻¹²` as a seam statement; sharpest form: identify
  the seam transport with the twelfth toral return; door 1 (`dim g_light`) is the live
  rival awaiting an owner decision.
- **P3** — cascade completion: the each-floor-forced statement over the full chain, the
  2-cell reading of shell closure, the typed count seam.
- **P4** — a discriminating experiment. Pre-registered candidates: two-tone SBSL
  golden-drive (frozen before data contact), the Keller–Miksis window (≤ 2·10⁻³),
  `w = 3/5 − φ` vs future DESI.
- **P5** — the [computed attack queue](03_THEORY_MAP/D0_VALUE_RANKED.md) (6 items).

## Empirical record (exact, from the [external-data scoreboard](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md))

| test | result |
|---|---|
| `sin²θ_W` on-shell | 0.23σ |
| `m_s/m_d = 20` | 0.02σ (bridge) |
| α leading term | exact identity (T17); sweep-uniqueness claim retired by reproduction; 9-digit total = consequence check pending P2 |
| Coldea `φ` (CoNb₂O₆) | corroborates; not discriminating |
| SPARC phason-halo kernel | rejected in ~91% of galaxies (recorded negative) |
| PMNS `δ₀` family, LIGO `φ⁻¹` defect | recorded non-discriminating (post-hoc family) |
| DESI DR2 | consistent with evolving dark energy; thawing corner not confirmed |

No multi-point discriminating confirmation exists yet; producing one is P4.

## Verify it yourself

```bash
pip install -r requirements.txt
python tools/validate_csv.py            # registry integrity (635 claims)
python tools/d0_logic_chain.py          # derivation chain + block hashes
python tools/d0_value_model.py          # value ledger + ranking
python tools/d0_score.py --strict       # scoreboard (75.2%, 0 integrity demotions)
```

```bash
cd 09_LEAN_FORMALIZATION && lake build D0.All   # 4476 jobs, 0 sorry
python 09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py
```

Ways to attack the theory (the kill rules work for outsiders): refute one of 27 named
bridge assumptions ([ledger](09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv), each
with a written failure condition); exhibit a second object against any uniqueness row;
break a certificate (every cert must be able to fail — `check_cert_can_fail.py` enforces
it); attack the root M1 squeeze (`N < D` loses distinguishability, `N > D` needs a
significance catalogue; the squeeze's lower branch is solid — the upper branch is carried
by MDL plus canonization, and that is where to press).

## Repository layout

| Path | Contents |
|---|---|
| [`D0_EXACT_RESULTS.md`](D0_EXACT_RESULTS.md) | **the theorem ledger — start here** |
| [`01_BOOKS/`](01_BOOKS/) | the theoretical spine — `BOOK_00` entry contract; `BOOK_01`–`09` mathematics and physics |
| [`03_THEORY_MAP/`](03_THEORY_MAP/) | [value ranking](03_THEORY_MAP/D0_VALUE_RANKED.md), [derivation chain](03_THEORY_MAP/D0_LOGIC_CHAIN.json), architecture, route inventory |
| [`05_CERTS/`](05_CERTS/) | deterministic `vp_*.py` certificates with reachable FAIL controls |
| [`08_PASSPORTS/`](08_PASSPORTS/) | curated external data (PDG, DESI, CMB, LIGO, SPARC…) + SHA256 manifests + real-data scoreboard |
| [`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/) | the Lean 4 package; canonical registry + [value ledger](09_LEAN_FORMALIZATION/docs/D0_VALUE_LEDGER.csv) |
| [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/) | Rosetta stone: every D0 mnemonic in conventional terms |
| [`tools/`](tools/) | guard scripts, registry sync, value model, chain builder |

## Registry, by the numbers

635 claims — 442 `LEAN_PROVED` (+31 with named bridge assumptions), 111 python-certified,
49 open, 2 deprecated; 231 core-formalized, 169 cert-closed, **96 no-go theorems** (89
NO-GO + 7 NO_GO_PROVED), 62 proof-targets. Derivation chain: 494 of 635 chained, 226
genesis blocks, max depth 10 — the structure is wide, not deep.
Counts measure bookkeeping, not insight; the [value ranking](03_THEORY_MAP/D0_VALUE_RANKED.md)
measures what matters.

## Method

Every claim passes an adversarial forcing loop before registration: registry pre-flight →
exact computation with can-fail certificates → memo with a pre-registered attack surface →
an independent skeptic mandated to kill by naming a second object or a precise gap →
repairs accepted as errors of record. Kills, retractions and false grades are themselves
registered results: the registry carries 2 deprecated rows, a quarantine ledger, and
accepted-kill records — the loop's output is not that errors never happen, but that they
are caught, named and kept.

## License / status

Private research snapshot (**v15**). Contact the author for usage or collaboration.
