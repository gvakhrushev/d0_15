# D0 Theory Strength Scoreboard

_Generated from `CLAIM_TO_LEAN_MAP.csv` + on-disk artifacts by `tools/d0_score.py`. Track-fair: core spine L0->L5 = 1/2/4/7/12/20; ceilings no-go 12, bridge 11, passport 7, external 2._

## Headline

- **Realized strength:** 9337 / 12058 (**77.4%** of track-fair max)
- **Core spine:** 7266 / 9920 (headroom **2654** points to take every core claim to L5)
- Claims: 693 active (695 total); integrity demotions: 0; duplicates: 0

## Repository hygiene / refactor score

- **Hygiene:** 96.3 / 100 (penalties **-3.7**, bonuses **+0.0**) — cleanup *gains* points here; tracked meta-trash / fake proofs / book-clutter *lose* them.

| signal | count | points | what to clean |
|---|--:|--:|---|
| `tracked_meta_trash` | 0 | -0 | tracked files under add/ + _QUARANTINE/v17_overshoots/ (vendored input, not release) |
| `tracked_but_ignored` | 0 | -0 | tracked-but-gitignored files (scratch that should not ship) |
| `tautology_proofs` | 0 | -0 | Lean (h:stmt):stmt:=h tautologies marked leanCoreProved (prove nothing) |
| `proof_debt` | 0 | -0 | sorry/axiom inside the built D0/ tree |
| `phantom_certs` | 0 | -0 | vp_*.py cited in books but absent on disk and not OPEN/PROOF-TARGET |
| `orphan_proof_targets` | 37 | -3.7 | PROOF-TARGET markers in book prose with no registry row |
| `dev_comments` | 0 | -0 | developer '# ...' TODO/notes left in book prose |
| `path_leaks` | 0 | -0 | internal repo paths / vp_*.py / D0.* module names dumped in book prose |
| `corpus_errors` | 0 | -0 | check_v14_clean_corpus violations (duplicate headings, version logs) |
| `real_in_project_lake` | 0 | -0 | a real .lake build tree inside the repo (must be an external junction) |
| `files_deleted_vs_base` | 0 | +0 | net files removed vs base-v14 (rewards shrinking the publish tree) |

**Top cleanup actions (most points to regain):** `orphan_proof_targets` (-3.7)

## Where to gain points next (cheapest promotions)

| claim | domain | at | -> | +pts | effort |
|---|---|---|---|--:|---|
| `D0-DARK-RATIO-TRANSFER-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001` | cosmology | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-P-M1-SATURATION-001` | frontier | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-P-ABELIAN-001` | frontier | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-GAP-W-COPY-CAP-M1-001` | frontier | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
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

## Highest-leverage open core gaps

| claim | domain | leverage | at | score |
|---|---|--:|---|--:|
| `D0-P-DEGREE2-EXHAUSTION-001` | frontier | 4 | HYP | 2 |
| `D0-TOWER-STOP-NOEXT-001` | frontier | 3 | HYP | 2 |
| `D0-DARK-RATIO-TRANSFER-OWNER-001` | cosmology | 2 | LEAN_PROVED | 12 |
| `D0-ARCHIVE-PHASON-METRIC-TRANSFER-OWNER-001` | cosmology | 2 | LEAN_PROVED | 12 |
| `D0-COSMOLOGY-INTERNAL-TRANSFER-COMPOSITION-001` | cosmology | 2 | LEAN_PROVED | 12 |
| `D0-P-M1-SATURATION-001` | frontier | 2 | LEAN_PROVED | 12 |
| `D0-P-ABELIAN-001` | frontier | 2 | LEAN_PROVED | 12 |
| `D0-TORAL-TIME-MARKOV-CONJUGACY-001` | frontier | 1 | HYP | 2 |
| `D0-GAP-W-COPY-CAP-M1-001` | frontier | 1 | LEAN_PROVED | 12 |
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

## By domain

| domain | n | realized | max | core headroom |
|---|--:|--:|--:|--:|
| formal_core | 405 | 6039 | 7222 | 1143 |
| frontier | 60 | 270 | 1200 | 930 |
| cosmology | 56 | 843 | 1021 | 178 |
| smooth_geometry | 42 | 524 | 685 | 152 |
| empirical_passport | 56 | 678 | 831 | 144 |
| spectral_action | 11 | 143 | 195 | 52 |
| gauge_bridge | 51 | 705 | 744 | 39 |
| rg | 7 | 93 | 113 | 16 |
| external_background | 1 | 1 | 2 | 0 |
| si_calibration | 3 | 30 | 34 | 0 |
| interpretation_spine | 1 | 11 | 11 | 0 |

## By book

| book | n | realized | max | core headroom |
|---|--:|--:|--:|--:|
| BOOK_04 | 123 | 1624 | 2130 | 486 |
| BOOK_08 | 92 | 1194 | 1598 | 395 |
| BOOK_02 | 87 | 1078 | 1424 | 336 |
| BOOK_01 | 66 | 990 | 1220 | 230 |
| BOOK_07 | 73 | 947 | 1253 | 292 |
| BOOK_06 | 45 | 547 | 776 | 224 |
| BOOK_05 | 31 | 384 | 555 | 171 |
| BOOK_00/01 | 22 | 366 | 392 | 26 |
| BOOK_01/02 | 15 | 284 | 284 | 0 |
| BOOK_06/08 | 13 | 170 | 209 | 39 |
| BOOK_07/08 | 13 | 151 | 218 | 62 |
| BOOK_00 | 12 | 145 | 222 | 77 |
| BOOK_01/03 | 5 | 100 | 100 | 0 |
| BOOK_05/06 | 6 | 96 | 96 | 0 |
| BOOK_03 | 7 | 82 | 90 | 8 |
| BOOK_01/02/08 | 4 | 80 | 80 | 0 |
| BOOK_06/07 | 4 | 80 | 80 | 0 |
| BOOK_01/04 | 3 | 60 | 60 | 0 |
| BOOK_02/04 | 4 | 58 | 71 | 13 |
| BOOK_04/08 | 7 | 52 | 140 | 88 |
| METROLOGY | 5 | 51 | 100 | 49 |
| BOOK_02/04/08 | 3 | 44 | 44 | 0 |
| BOOK_02/03 | 2 | 40 | 40 | 0 |
| D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE | 3 | 33 | 33 | 0 |
| BOOK_05/08 | 2 | 32 | 32 | 0 |
| Lean formalization | 2 | 31 | 31 | 0 |
| BOOK_02/05 | 2 | 27 | 40 | 13 |
| BOOK_01/06 | 2 | 27 | 31 | 0 |
| BOOK_09 | 2 | 27 | 27 | 0 |
| BOOK_04/06 | 2 | 27 | 40 | 13 |
| BOOK_01/02/04/08 | 1 | 20 | 20 | 0 |
| BOOK_02/08 | 1 | 20 | 20 | 0 |
| BOOK_01/05 | 1 | 20 | 20 | 0 |
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
| BOOK_00/05 | 1 | 20 | 20 | 0 |
| BOOK_00/07 | 1 | 20 | 20 | 0 |
| BOOK_03/04 | 1 | 20 | 20 | 0 |
| BOOK_00/06 | 1 | 20 | 20 | 0 |
| BOOK_02/04/07/08 | 1 | 20 | 20 | 0 |
| BOOK_00/01/06 | 1 | 20 | 20 | 0 |
| BOOK_04/05 | 2 | 18 | 18 | 0 |
| BOOK_06/01 | 2 | 14 | 40 | 26 |
| BOOK_04/07 | 2 | 13 | 31 | 18 |
| BOOK_02/04/05/06/07 | 1 | 12 | 12 | 0 |
| BOOK_01/03/04/07 | 1 | 12 | 12 | 0 |
| BOOK_00/08 | 1 | 11 | 11 | 0 |
| BOOK_01/03/06/07/08 | 1 | 11 | 11 | 0 |
| BOOK_04/05/08 | 1 | 7 | 7 | 0 |
| BOOK_00/01/02/04/05/06 | 1 | 7 | 20 | 13 |
| BOOK_01/07 | 1 | 7 | 20 | 13 |
| BOOK_07/05 | 1 | 7 | 20 | 13 |
| BOOK_07/01 | 1 | 7 | 20 | 13 |
| BOOK_04/06/07/08 | 1 | 2 | 20 | 18 |
| PUBLICATION | 1 | 2 | 20 | 18 |
