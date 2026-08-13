# A1/A2 acquisition record + frozen observables (committed BEFORE the proofreading-floor mint)

**Order-of-record:** this file is committed BEFORE `D0-CASCADE-FLOOR-PROOFREADING-001` is
minted, deliberately: R-A2 below is the empirical falsifier of the floor's carrier
hypothesis, and freezing it after the mint would make any agreement post-hoc (the
pre-registration race, named by the acquisition scout).

## Contamination ledger (scouting IS partial data contact — recorded verbatim)

Headline numbers seen during scouting and therefore INADMISSIBLE as frozen observables:
Potapov–Ong Table 3 error-rate span (5.3e-7…1.5e-4); Betancurt-Anzola wt rates + exo⁻
folds (15×/2×/2×); St Charles Table 2 proofreading/MMR folds (160×/1000×, 65×/250×);
Drake 1991 (0.0033/genome); Johansson 2012 d-range; Zhang 2015 Table S1 d-range
(200–80000); Ieong 2016 I/F RANGES (I=40–123, F=17–239, F₂≈10–50); Gromadski–Rodnina
350× equilibrium vs 650× kinetic. CLEAN: the A1 pin `results.csv` was touched at
header+rowcount ONLY (49 rows, 12 substitution cells + Deletion/Insertion per sample) —
zero numeric values seen; R-A1 is therefore a genuinely clean freeze. R-A2 is PARTIALLY
contaminated (ranges seen, per-variant values not); its Bayesian force is reduced
accordingly and this sentence is part of the record.

## A1 pick (replication fidelity, move 1 = record)

**Potapov V, Ong JL (2017), PLoS ONE 12(1):e0169774** (+ correction 10.1371/journal.pone.0181128
— PrimeSTAR/KOD labels swapped in Fig 1A, must be co-pinned). Pin:
`github.com/potapovneb/pcr-fidelity` → `results/results.csv` at commit
`733e062ec49031f235bb7cc9540bce35cecfd6c8` (frozen 2017, no commits since), + `input/samples.csv`,
+ article XML from journals.plos.org (pin the journals URL + SHA256 of retrieved bytes,
NOT the 24h-signed GCS redirect). CC-BY. 9 polymerases × 3 amplicons, full 12-cell
substitution matrix, and a within-backbone proofreading pair (Deep Vent exo⁺/exo⁻, n=3).
Backups: Betancurt-Anzola 2025 NAR (best cross-family wt/exo⁻ design; licence-open but
bot-blocked — browser acquisition, honest barrier), St Charles 2015 (three-stage
decomposition, headline numbers contaminated), Drake 1991 (classical anchor only).

### R-A1 (FROZEN, clean): is record fidelity a scalar or a vector?

On the pinned `results.csv`: normalize each sample's 12 off-diagonal substitution counts
to a probability vector. PASS iff the mean between-enzyme Jensen–Shannon divergence
exceeds the mean within-enzyme (replicate/amplicon) JSD by ratio **R ≥ 2.0**, with null
control (10 000 enzyme-label permutations, seed 20260814) firing iff permuted R ≥ 2.0 in
< 1% of permutations. PASS ⇒ WHICH distinction is lost is channel-specific — the move-1
floor cannot be parameterized by a single rate f (fidelity is a vector). FAIL ⇒ scalar
parameterization vindicated, the "which distinction" refinement is dead. CONTROL-FAIL ⇒
criterion void, recorded. Secondary R-A1b (declared underpowered, n=3): JSD(exo⁺, exo⁻)
of the Deep Vent pair vs 99th percentile of within-enzyme replicate JSDs — does
proofreading attenuate uniformly or selectively?

## A2 pick (kinetic proofreading, move 2 = memory)

**Ieong–Uzun–Selmer–Ehrenberg 2016 PNAS (10.1073/pnas.1610917113)** — the only source
resolving the discrimination cascade into ≥3 separately measured multiplicative stages
(A = I × F₁ × F₂), Tables S2–S4 — **plus Zhang 2015 PNAS (10.1073/pnas.1506823112)**
Table S1 (largest initial-selection d-set, same lab/platform) **plus mandatory control
source Gromadski–Rodnina 2004 (10.1016/S1097-2765(04)00005-X)** — the only measurement of
BOTH the equilibrium ratio and the realized kinetic gain for the SAME step. Acquisition
honesty: all three need browser/manual retrieval (Cloudflare/paywall); recorded as the
cost in the manifest citation_note. Fersht 1977 stays a cited structural reference.

### R-A2 (FROZEN, partially contaminated — see ledger): stage gains vs the Boltzmann bound

Declared before opening any SI table at per-variant granularity: (i) every individually
measured EQUILIBRIUM-stage gain is ≤ the equilibrium binding-ratio bound of its own step,
while (ii) the total accuracy A exceeds any single step's equilibrium bound by ≥ 10×, and
(iii) for ≥ 80% of tabulated variants log F / log A ∈ [0.15, 0.85] (neither stage alone
carries the accuracy). Falsified outright by an equilibrium stage exceeding its own bound.
**Known candidate kill (recorded IN the freeze, seen during scouting): the
Gromadski–Rodnina initial-selection step realizes 650× against a 350× equilibrium ratio —
a KINETIC stage exceeding its equilibrium bound.** This does not refute Hopfield (kinetic
amplification beyond equilibrium is his point); it KILLS the naive identification
"one biochemical stage = one equilibrium test of the proofreading floor". Consequence,
frozen now: the floor's carrier applies to EQUILIBRIUM tests only; any real stage that
beats its equilibrium bound must be graded as internally multi-test (it embeds an
irreversible step — GTP hydrolysis) — i.e. the floor's register count is a LOWER-bound
reading, never a per-biochemical-stage count. The proofreading-floor row note MUST carry
this sentence; agreement of data with the floor may never be claimed at
per-biochemical-stage granularity.

## Manifest skeleton (A1, mirrors icecube_manifest.json discipline)

dataset_id potapov_ong_pcr_fidelity_2017 · source doi:10.1371/journal.pone.0169774 ·
files: results.csv @ raw.githubusercontent/733e062…, input/samples.csv, article XML,
correction DOI record · fields: Enzyme, Amplicon, GroupID, 12 off-diagonal cells,
Deletion, Insertion · license CC-BY 4.0 + repo LICENSE co-pinned · status MISSING until
each SHA256 verified locally. Fetch is scriptable (no browser) — the only A-target with
that property; that is why A1 is first.
