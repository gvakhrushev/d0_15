# D0 v16 Books Proofread Audit

Status: `BOOKS-PROOFREAD-PATCHED`

## Scope

Active books checked: `01_BOOKS/BOOK_00...BOOK_08`.

## Repairs performed

- repaired replacement-character / mojibake symbol corruption in book titles and mathematical lines;
- restored recurring symbols: `φ`, `Ω8`, `π`, `∂`, `δ_0`, `ρ(F)`, `Σ`, `D†D`, `×`, `→`, `∞` where context and reference material made the replacement unambiguous;
- corrected grammar instances such as `a ordered` → `an ordered`;
- removed one duplicated explanatory sentence in Book 01;
- preserved bridge/status discipline: dusty-plasma and LIGO rows remain bridge/negative-control material, not core proof.

## Validation after patch

Certificate smoke tests rerun after book proofreading:

```text
PASS_RUN_ALL_BRIDGE_CERTS
PASS_RUN_ALL_V16_INTEGRATED_CERTS
```


| Book | Lines | Replacement chars | Open code fence | Bad headings |
|---|---:|---:|---:|---:|
| `BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md` | 455 | 0 | False | 0 |
| `BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` | 1339 | 0 | False | 0 |
| `BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md` | 1808 | 0 | False | 0 |
| `BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` | 710 | 0 | False | 0 |
| `BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md` | 1266 | 0 | False | 0 |
| `BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md` | 748 | 0 | False | 0 |
| `BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md` | 933 | 0 | False | 0 |
| `BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md` | 1481 | 0 | False | 0 |
| `BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md` | 1045 | 0 | False | 0 |

## Residual limitations

- I did not rewrite theorem content or change mathematical claims beyond typo/symbol/grammar cleanup.
- Some external data bundles from conversation-level LIGO V11/V12 remain status summaries rather than full data passports.
- Lean artifacts were not rebuilt as part of book proofreading.
