# D0 Theory Strength Scoreboard

_Generated from `CLAIM_TO_LEAN_MAP.csv` + on-disk artifacts by `tools/d0_score.py`. Track-fair: core spine L0->L5 = 1/2/4/7/12/20; ceilings no-go 12, bridge 11, passport 7, external 2._

## Headline

- **Realized strength:** 6188 / 8584 (**72.1%** of track-fair max)
- **Core spine:** 4876 / 7240 (headroom **2364** points to take every core claim to L5)
- Claims: 488 active (490 total); integrity demotions: 0; duplicates: 0

## Repository hygiene / refactor score

- **Hygiene:** 100.0 / 100 (penalties **-3.8**, bonuses **+10.0**) — cleanup *gains* points here; tracked meta-trash / fake proofs / book-clutter *lose* them.

| signal | count | points | what to clean |
|---|--:|--:|---|
| `tracked_meta_trash` | 0 | -0 | tracked files under add/ + _QUARANTINE/v17_overshoots/ (vendored input, not release) |
| `tracked_but_ignored` | 0 | -0 | tracked-but-gitignored files (scratch that should not ship) |
| `tautology_proofs` | 0 | -0 | Lean (h:stmt):stmt:=h tautologies marked leanCoreProved (prove nothing) |
| `proof_debt` | 0 | -0 | sorry/axiom inside the built D0/ tree |
| `phantom_certs` | 0 | -0 | vp_*.py cited in books but absent on disk and not OPEN/PROOF-TARGET |
| `orphan_proof_targets` | 38 | -3.8 | PROOF-TARGET markers in book prose with no registry row |
| `dev_comments` | 0 | -0 | developer '# ...' TODO/notes left in book prose |
| `path_leaks` | 0 | -0 | internal repo paths / vp_*.py / D0.* module names dumped in book prose |
| `corpus_errors` | 0 | -0 | check_v14_clean_corpus violations (duplicate headings, version logs) |
| `real_in_project_lake` | 0 | -0 | a real .lake build tree inside the repo (must be an external junction) |
| `files_deleted_vs_base` | 135 | +10 | net files removed vs base-v14 (rewards shrinking the publish tree) |

**Top cleanup actions (most points to regain):** `orphan_proof_targets` (-3.8)

## Where to gain points next (cheapest promotions)

| claim | domain | at | -> | +pts | effort |
|---|---|---|---|--:|---|
| `D0-DARK-RATIO-TRANSFER-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-FIBONACCI-IF-FORCING-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-PHASON-PRESSURE-EOS-SCAFFOLD-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001` | empirical_passport | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-LUCAS-VORONOI-MARKOV-PARTITION-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-PAGE-CURVE-FINITE-RANK-OWNER-001` | smooth_geometry | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-BLACK-HOLE-INFORMATION-UNITARITY-OWNER-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-REHEATING-PERCOLATION-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-C-LIGHTCONE-PERCOLATION-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-FIBONACCI-ANYON-UNIQUENESS-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-TIME-ARROW-ORDERED-SELF-READOUT-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-ARCHIVE-NEUMANN-TICK-OWNER-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001` | smooth_geometry | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-CONTINUOUS-TIME-SEMIGROUP-ENVELOPE-001` | smooth_geometry | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-STATIC-TO-DYNAMICS-OWNER-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-DYNAMICS-NOT-PRIMITIVE-CERT-CLOSED-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-INFLATIONLESS-THRESHOLD-ENERGY-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-REHEATING-PHASON-INITIAL-DATA-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |

## Highest-leverage open core gaps

| claim | domain | leverage | at | score |
|---|---|--:|---|--:|
| `D0-DARK-RATIO-TRANSFER-OWNER-001` | cosmology | 2 | LEAN_PROVED | 12 |
| `D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001` | cosmology | 2 | LEAN_PROVED | 12 |
| `D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001` | cosmology | 2 | LEAN_PROVED | 12 |
| `D0-TORAL-TIME-MARKOV-CONJUGACY-001` | frontier | 1 | HYP | 2 |
| `D0-FIBONACCI-IF-FORCING-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-PHASON-PRESSURE-EOS-SCAFFOLD-001` | cosmology | 1 | LEAN_PROVED | 12 |
| `D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001` | empirical_passport | 1 | LEAN_PROVED | 12 |
| `D0-LUCAS-VORONOI-MARKOV-PARTITION-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-PAGE-CURVE-FINITE-RANK-OWNER-001` | smooth_geometry | 1 | LEAN_PROVED | 12 |
| `D0-BLACK-HOLE-INFORMATION-UNITARITY-OWNER-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001` | cosmology | 1 | LEAN_PROVED | 12 |
| `D0-REHEATING-PERCOLATION-OWNER-001` | cosmology | 1 | LEAN_PROVED | 12 |
| `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001` | cosmology | 1 | LEAN_PROVED | 12 |
| `D0-C-LIGHTCONE-PERCOLATION-OWNER-001` | cosmology | 1 | LEAN_PROVED | 12 |
| `D0-FIBONACCI-ANYON-UNIQUENESS-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-JY-NONCOMMUTATIVE-ORDER-OBSTRUCTION-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-TIME-ARROW-ORDERED-SELF-READOUT-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-ARCHIVE-NEUMANN-TICK-OWNER-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001` | smooth_geometry | 1 | LEAN_PROVED | 12 |
| `D0-CONTINUOUS-TIME-SEMIGROUP-ENVELOPE-001` | smooth_geometry | 1 | LEAN_PROVED | 12 |
| `D0-STATIC-TO-DYNAMICS-OWNER-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-DYNAMICS-NOT-PRIMITIVE-CERT-CLOSED-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-INFLATIONLESS-THRESHOLD-ENERGY-OWNER-001` | cosmology | 1 | LEAN_PROVED | 12 |

## By domain

| domain | n | realized | max | core headroom |
|---|--:|--:|--:|--:|
| formal_core | 287 | 4033 | 5056 | 1013 |
| frontier | 46 | 132 | 920 | 788 |
| cosmology | 50 | 753 | 931 | 178 |
| smooth_geometry | 36 | 433 | 602 | 165 |
| empirical_passport | 32 | 328 | 481 | 144 |
| spectral_action | 6 | 73 | 112 | 39 |
| gauge_bridge | 20 | 313 | 334 | 21 |
| rg | 7 | 93 | 113 | 16 |
| external_background | 1 | 1 | 2 | 0 |
| si_calibration | 2 | 18 | 22 | 0 |
| interpretation_spine | 1 | 11 | 11 | 0 |

## By book

| book | n | realized | max | core headroom |
|---|--:|--:|--:|--:|
| BOOK_04 | 88 | 1110 | 1548 | 428 |
| BOOK_08 | 82 | 1072 | 1504 | 428 |
| BOOK_07 | 67 | 818 | 1142 | 310 |
| BOOK_02 | 55 | 613 | 873 | 260 |
| BOOK_06 | 39 | 473 | 673 | 200 |
| BOOK_05 | 26 | 339 | 484 | 145 |
| BOOK_01 | 19 | 271 | 363 | 92 |
| BOOK_01/02 | 11 | 212 | 212 | 0 |
| BOOK_00 | 9 | 101 | 162 | 61 |
| BOOK_05/06 | 6 | 96 | 96 | 0 |
| BOOK_03 | 7 | 82 | 90 | 8 |
| BOOK_06/07 | 4 | 80 | 80 | 0 |
| BOOK_07/08 | 8 | 80 | 160 | 80 |
| BOOK_04/08 | 7 | 52 | 140 | 88 |
| METROLOGY | 5 | 51 | 100 | 49 |
| BOOK_06/08 | 4 | 41 | 80 | 39 |
| BOOK_02/03 | 2 | 40 | 40 | 0 |
| BOOK_00/01 | 2 | 40 | 40 | 0 |
| BOOK_01/04 | 2 | 40 | 40 | 0 |
| BOOK_02/04 | 3 | 38 | 51 | 13 |
| D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE | 3 | 33 | 33 | 0 |
| BOOK_05/08 | 2 | 32 | 32 | 0 |
| Lean formalization | 2 | 31 | 31 | 0 |
| BOOK_02/05 | 2 | 27 | 40 | 13 |
| BOOK_01/06 | 2 | 27 | 31 | 0 |
| BOOK_09 | 2 | 27 | 27 | 0 |
| BOOK_03/06/07/08 | 1 | 20 | 20 | 0 |
| BOOK_00/01/03/06/07/08 | 1 | 20 | 20 | 0 |
| BOOK_00/01/06/07/08 | 1 | 20 | 20 | 0 |
| BOOK_00/01/02/06/08 | 1 | 20 | 20 | 0 |
| BOOK_00/01/02/04/06/07/08 | 1 | 20 | 20 | 0 |
| BOOK_06/07/08 | 1 | 20 | 20 | 0 |
| BOOK_02/04/05/08 | 1 | 20 | 20 | 0 |
| BOOK_00/01/02/03 | 1 | 20 | 20 | 0 |
| BOOK_01/02/06 | 1 | 20 | 20 | 0 |
| BOOK_03/06 | 1 | 20 | 20 | 0 |
| BOOK_01/03 | 1 | 20 | 20 | 0 |
| BOOK_00/05 | 1 | 20 | 20 | 0 |
| BOOK_04/05 | 2 | 19 | 19 | 0 |
| BOOK_06/01 | 2 | 14 | 40 | 26 |
| BOOK_02/04/05/06/07 | 1 | 12 | 12 | 0 |
| BOOK_02/04/08 | 1 | 12 | 12 | 0 |
| BOOK_00/08 | 1 | 11 | 11 | 0 |
| BOOK_01/03/06/07/08 | 1 | 11 | 11 | 0 |
| BOOK_04/05/08 | 1 | 7 | 7 | 0 |
| BOOK_00/01/02/04/05/06 | 1 | 7 | 20 | 13 |
| BOOK_01/07 | 1 | 7 | 20 | 13 |
| BOOK_04/06 | 1 | 7 | 20 | 13 |
| BOOK_07/05 | 1 | 7 | 20 | 13 |
| BOOK_04/07 | 2 | 4 | 40 | 36 |
| BOOK_04/06/07/08 | 1 | 2 | 20 | 18 |
| PUBLICATION | 1 | 2 | 20 | 18 |
