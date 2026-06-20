# D0 Book / Claim Cross-Reference Consistency

Single source of truth: `CLAIM_TO_LEAN_MAP.csv` (446 active claims). Status distribution:

- CORE-FORMALIZED: 162
- CERT-CLOSED: 131
- NO-GO: 46
- PROOF-TARGET: 44
- BRIDGE-ASSUMPTIONS-EXPLICIT: 20
- PASSPORT-CLOSED: 17
- NO_GO_PROVED: 8
- CORE_BRIDGE_SPLIT: 6
- EMPIRICAL-PASSPORT: 6
- BRIDGE-CALIBRATION: 3
- DEPRECATED: 2
- EXTERNAL-BACKGROUND: 1

## Integrity
- closed-without-owner: 0
- closed+open-inside: 0
- empty lean_status: 0
- anonymous open targets: 12

Each claim_id is unique in the registry (no duplicate-owner-incompatible-status). Guards: `vp_no_cert_closed_with_open_core_dependency`, `vp_no_passport_promoted_to_core`, `vp_no_scaffold_promoted_to_physical_claim`, `vp_no_no_go_route_revival`, `vp_cross_book_owner_consistency`.
