# D0 v16 Final Theory Claim Audit

Status: FINAL-THEORY-CLAIM-AUDIT / PUBLICATION-GUARDRAIL-PASS

## Scope

This audit adds the final publication-facing claim hierarchy for D0 v16. It does not add new physics. It freezes the distinction between core finite-readout claims, sector certificates, theorem targets, lab bridges, and empirical negative controls.

## Files added

- `00_PUBLICATION/D0_v16_CLAIMS_REGISTER.md`
- `00_PUBLICATION/D0_v16_CLAIMS_REGISTER.csv`
- `00_PUBLICATION/D0_v16_THEOREM_DEPENDENCY_GRAPH.md`
- `00_PUBLICATION/D0_v16_PUBLICATION_ABSTRACT.md`
- `00_PUBLICATION/D0_v16_REVIEWER_RISK_LEDGER.md`
- `00_PUBLICATION/D0_v16_DO_NOT_CLAIM.md`
- `00_PUBLICATION/D0_v16_FINAL_PUBLICATION_CHECKLIST.md`
- `00_PUBLICATION/D0_v16_RELEASE_NOTES.md`
- `00_PUBLICATION/D0_v16_MINIMAL_THEORY_SPINE.md`

- `05_CERTS/vp_publication_claim_register_guardrail.py`
- `05_CERTS/run_all_publication_guardrails.py`
- `06_AUDIT/D0_v16_FINAL_THEORY_CLAIM_AUDIT.json`
- `06_AUDIT/D0_v16_FINAL_THEORY_CLAIM_AUDIT.md`

## Claim-class counts

| Claim class | Count |
|---|---:|
| AUDIT/PUBLICATION | 1 |
| CORE/SECTOR-CERTIFIED | 9 |
| EMPIRICAL-NEGATIVE | 1 |
| LAB-BRIDGE / EMPIRICAL-PASSPORT | 9 |
| NO-GO/AUDIT | 15 |
| SECTOR-CERTIFIED | 3 |
| STATUS-CHECK-REQUIRED | 106 |
| THEOREM-TARGET / FRONTIER | 11 |

## Book scan

| File | Replacement chars | NUL bytes | Unclosed code fence | Publication status |
|---|---:|---:|---|---|
| `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md` | 0 | 0 | False | True |
| `01_BOOKS/BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md` | 0 | 0 | False | True |

## Final claim boundaries

```text
Core finite-readout algebra: publishable as internal theorem/cert layer.
Sector constructions: publishable only inside their named certificate/theorem scope.
Dusty plasma: lab bridge / tabletop passport seed only.
LIGO/GWOSC: negative controls / transfer-map target only.
Phi external predictions: pre-registered targets only.
```

## Decision

`PUBLICATION-CLAIM-GUARDRAILS-ADDED`

The package is ready for a first publication-candidate freeze after optional graph/index regeneration.
