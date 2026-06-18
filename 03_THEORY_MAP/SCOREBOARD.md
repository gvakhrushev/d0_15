# D0 Theory Strength Scoreboard

_Generated from `CLAIM_TO_LEAN_MAP.csv` + on-disk artifacts by `tools/d0_score.py`. Track-fair: core spine L0->L5 = 1/2/4/7/12/20; ceilings no-go 12, bridge 11, passport 7, external 2._

## Headline

- **Realized strength:** 4222 / 5119 (**82.5%** of track-fair max)
- **Core spine:** 3626 / 4500 (headroom **874** points to take every core claim to L5)
- Claims: 286 active (288 total); integrity demotions: 0; duplicates: 0

## Repository hygiene / refactor score

- **Hygiene:** 100.0 / 100 (penalties **-0.2**, bonuses **+10.0**) — cleanup *gains* points here; tracked meta-trash / fake proofs / book-clutter *lose* them.

| signal | count | points | what to clean |
|---|--:|--:|---|
| `tracked_meta_trash` | 0 | -0 | tracked files under add/ + _QUARANTINE/v17_overshoots/ (vendored input, not release) |
| `tracked_but_ignored` | 0 | -0 | tracked-but-gitignored files (scratch that should not ship) |
| `tautology_proofs` | 0 | -0 | Lean (h:stmt):stmt:=h tautologies marked leanCoreProved (prove nothing) |
| `proof_debt` | 0 | -0 | sorry/axiom inside the built D0/ tree |
| `phantom_certs` | 0 | -0 | vp_*.py cited in books but absent on disk and not OPEN/PROOF-TARGET |
| `orphan_proof_targets` | 2 | -0.2 | PROOF-TARGET markers in book prose with no registry row |
| `dev_comments` | 0 | -0 | developer '# ...' TODO/notes left in book prose |
| `path_leaks` | 0 | -0 | internal repo paths / vp_*.py / D0.* module names dumped in book prose |
| `corpus_errors` | 0 | -0 | check_v14_clean_corpus violations (duplicate headings, version logs) |
| `real_in_project_lake` | 0 | -0 | a real .lake build tree inside the repo (must be an external junction) |
| `files_deleted_vs_base` | 135 | +10 | net files removed vs base-v14 (rewards shrinking the publish tree) |

**Top cleanup actions (most points to regain):** `orphan_proof_targets` (-0.2)

## Where to gain points next (cheapest promotions)

| claim | domain | at | -> | +pts | effort |
|---|---|---|---|--:|---|
| `D0-FIBONACCI-IF-FORCING-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-GENERATIVE-DYNAMICS-001` | rg | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-UNITY-SPLIT-SPACETIME-001` | formal_core | LEAN_PROVED | CORE_FORMALIZED | 8 | release-bless to core |
| `D0-ARCHIVE-HEATTRACE-001` | spectral_action | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-SPECTRAL-ACTION-ADMISS-001` | spectral_action | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-HST-ARCHIVE-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-ARCHIVE-ENTROPY-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-DM-CLASSICALITY-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-QUASI009-CKM-PHASON-HOLONOMY-001` | empirical_passport | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-QUASI007-MESON-PHASON-DOMAIN-WALLS-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-KTHEORY-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-SOLENOID-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-SOLENOID-GRAVITY-001` | spectral_action | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-MESON-K0-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-CKM-K0-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-SDE-K0-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-CVFT-F4` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-CVFT-F7` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-MINCUT-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-MASTER-BOOTSTRAP-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-MESON-DEFECT-ALGEBRA-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-CANONICAL-OP-001` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-LEPTON-002` | empirical_passport | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-NEUTRON-002` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |
| `D0-GRAV-002` | formal_core | PYTHON_CERTIFIED | LEAN_PROVED | 5 | write Lean proof |

## Highest-leverage open core gaps

| claim | domain | leverage | at | score |
|---|---|--:|---|--:|
| `D0-FIBONACCI-IF-FORCING-001` | formal_core | 1 | LEAN_PROVED | 12 |
| `D0-CVFT-001B` | frontier | 0 | HYP | 2 |
| `D0-CVFT-F2` | frontier | 0 | HYP | 2 |
| `D0-CVFT-F3` | empirical_passport | 0 | HYP | 2 |
| `D0-CVFT-F5` | frontier | 0 | HYP | 2 |
| `D0-CVFT-F6` | frontier | 0 | HYP | 2 |
| `D0-CVFT-F8` | frontier | 0 | HYP | 2 |
| `D0-EDGE-002` | frontier | 0 | HYP | 2 |
| `D0-PUB-001` | frontier | 0 | HYP | 2 |
| `D0-QUANT-MET-003` | frontier | 0 | HYP | 2 |
| `D0-QUANT-MET-004` | frontier | 0 | HYP | 2 |
| `D0-SPECTRAL-EINSTEIN-001` | frontier | 0 | HYP | 2 |
| `D0-HODGE-LINKS-001` | frontier | 0 | HYP | 2 |
| `D0-PASSPORT-DESI-BAO-001` | frontier | 0 | HYP | 2 |
| `D0-PMNS-DELTACP-PI0-001` | frontier | 0 | HYP | 2 |
| `D0-ARCHIVE-HEATTRACE-001` | spectral_action | 0 | PYTHON_CERTIFIED | 7 |
| `D0-SPECTRAL-ACTION-ADMISS-001` | spectral_action | 0 | PYTHON_CERTIFIED | 7 |
| `D0-HST-ARCHIVE-001` | formal_core | 0 | PYTHON_CERTIFIED | 7 |
| `D0-ARCHIVE-ENTROPY-001` | formal_core | 0 | PYTHON_CERTIFIED | 7 |
| `D0-DM-CLASSICALITY-001` | formal_core | 0 | PYTHON_CERTIFIED | 7 |
| `D0-QUASI009-CKM-PHASON-HOLONOMY-001` | empirical_passport | 0 | PYTHON_CERTIFIED | 7 |
| `D0-QUASI007-MESON-PHASON-DOMAIN-WALLS-001` | formal_core | 0 | PYTHON_CERTIFIED | 7 |
| `D0-KTHEORY-001` | formal_core | 0 | PYTHON_CERTIFIED | 7 |
| `D0-SOLENOID-001` | formal_core | 0 | PYTHON_CERTIFIED | 7 |
| `D0-SOLENOID-GRAVITY-001` | spectral_action | 0 | PYTHON_CERTIFIED | 7 |

## By domain

| domain | n | realized | max | core headroom |
|---|--:|--:|--:|--:|
| formal_core | 173 | 2785 | 3261 | 471 |
| frontier | 13 | 26 | 260 | 234 |
| empirical_passport | 24 | 233 | 295 | 57 |
| smooth_geometry | 18 | 272 | 315 | 39 |
| spectral_action | 5 | 61 | 100 | 39 |
| gauge_bridge | 19 | 301 | 314 | 13 |
| cosmology | 24 | 446 | 459 | 13 |
| rg | 5 | 61 | 73 | 8 |
| external_background | 1 | 1 | 2 | 0 |
| si_calibration | 3 | 25 | 29 | 0 |
| interpretation_spine | 1 | 11 | 11 | 0 |

## By book

| book | n | realized | max | core headroom |
|---|--:|--:|--:|--:|
| BOOK_08 | 47 | 737 | 842 | 101 |
| BOOK_04 | 47 | 708 | 871 | 158 |
| BOOK_07 | 48 | 660 | 852 | 182 |
| BOOK_01 | 15 | 223 | 278 | 55 |
| BOOK_06 | 13 | 221 | 242 | 21 |
| BOOK_01/02 | 11 | 212 | 212 | 0 |
| BOOK_02 | 13 | 207 | 220 | 13 |
| BOOK_05 | 8 | 133 | 133 | 0 |
| BOOK_05/06 | 6 | 96 | 96 | 0 |
| BOOK_07/08 | 8 | 85 | 147 | 62 |
| BOOK_06/07 | 4 | 80 | 80 | 0 |
| BOOK_04/08 | 7 | 57 | 127 | 70 |
| METROLOGY | 5 | 51 | 100 | 49 |
| BOOK_06/08 | 4 | 41 | 80 | 39 |
| BOOK_02/03 | 2 | 40 | 40 | 0 |
| BOOK_00/01 | 2 | 40 | 40 | 0 |
| BOOK_01/04 | 2 | 40 | 40 | 0 |
| D0_OPERATOR_BRIDGE_TRIPLE_CLOSURE | 3 | 33 | 33 | 0 |
| BOOK_05/08 | 2 | 32 | 32 | 0 |
| Lean formalization | 2 | 31 | 31 | 0 |
| BOOK_02/04 | 2 | 31 | 31 | 0 |
| BOOK_02/05 | 2 | 27 | 40 | 13 |
| BOOK_01/06 | 2 | 27 | 31 | 0 |
| BOOK_09 | 2 | 27 | 27 | 0 |
| BOOK_00 | 2 | 22 | 22 | 0 |
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
| BOOK_03 | 1 | 20 | 20 | 0 |
| BOOK_01/03 | 1 | 20 | 20 | 0 |
| BOOK_00/05 | 1 | 20 | 20 | 0 |
| BOOK_04/05 | 2 | 19 | 19 | 0 |
| BOOK_02/04/05/06/07 | 1 | 12 | 12 | 0 |
| BOOK_02/04/08 | 1 | 12 | 12 | 0 |
| BOOK_00/08 | 1 | 11 | 11 | 0 |
| BOOK_01/03/06/07/08 | 1 | 11 | 11 | 0 |
| BOOK_04/05/08 | 1 | 7 | 7 | 0 |
| BOOK_00/01/02/04/05/06 | 1 | 7 | 20 | 13 |
| BOOK_01/07 | 1 | 7 | 20 | 13 |
| BOOK_04/06 | 1 | 7 | 20 | 13 |
| BOOK_04/07 | 2 | 4 | 40 | 36 |
| BOOK_04/06/07/08 | 1 | 2 | 20 | 18 |
| PUBLICATION | 1 | 2 | 20 | 18 |
