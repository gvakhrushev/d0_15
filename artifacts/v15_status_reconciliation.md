# D0-v15 status reconciliation

| claim | status_before | status_after | reason |
|---|---|---|---|
| D0-ZONE-CURRENT-001 | CONDITIONAL (naive, oblique) | THE | Hermiticity gate met in the canonical frozen part-size inner product; projectors genuinely G-orthogonal |
| D0-ZONE-NEUTRAL-ACTIVE-SPLIT-001 | CONDITIONAL | THE | orthogonal (not oblique) once G is used; FIREWALL: not a physical neutral current/neutrino/charge |
| D0-FESHBACH-SCHUR-FACTORIZATION-V15 | (identity not previously isolated) | THE (algebraic identity only) | true block-determinant identity; NOT an energy-pressure tensor |
| D0-BRANCH-CP-READOUT-NOGO-V15 | (open) | NO-GO | branch symmetry leaves a family; needs PRIM-BRANCH-ISOTROPIC-READOUT |
| D0-LEPTON-DECIMAL-MASS-RATIOS | (open) | NO-GO | exponents impose no constraint on ratios; needs PRIM-EFT-IR-MATCHING-FUNCTIONAL |
| D0-P1-PHYSICAL-EOS | (open) | NO-GO | response fixes only the total; needs PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT; no rho=e^u-1,p=e^u/phi |
| D0-EDGE-COVER-FAMILY-001 | (open) | CONDITIONAL-EXTENSION | lambda unfixed; needs PRIM-EDGE-HOLONOMY-SELECTOR; Halmos existence != uniqueness |
| D0-STURMIAN-REFINEMENT | (open) | CONDITIONAL-EXTENSION | valid extension; identifying with archive maps needs PRIM-STURMIAN-REFINEMENT-OWNER; no CFT import |
| D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001 | (open) | NO-GO | archive map is contracting, not regular; do not substitute a regular cover |
| D0-PRESENT-CORE-LIMITS-REGRESSION-V15 | NO-GO (each) | NO-GO (regression holds) | v15 work did not breach established limits |
| D0-AMS-HEAVY-NUCLEI-PASSPORT-001 | (none) | EMPIRICAL-PASSPORT | external target; needs internal nuclear-flux transfer operator before any prediction |

## Counts

- CONDITIONAL-EXTENSION: 2
- EMPIRICAL-PASSPORT: 1
- NO-GO: 4
- NO-GO (regression holds): 1
- THE: 2
- THE (algebraic identity only): 1

## Rejected inputs (non-existent *_RESULT.md): 8

- D0_INTERFACE_DISPLACEMENT_RESULT
- D0_DYADIC_REFINEMENT_AND_SEAM_GROUPOID_RESULT
- D0_UNIVERSAL_PHASE_BRANCH_AND_FESHBACH_RESULT
- D0_X5_INTERFACE_BRANCH_ROUTE_FINAL_NO_GO
- D0_CANONICAL_ZONE_CURRENT_RESULT
- D0_ZONE_STURMIAN_PHI_CLOSURE_RESULT
- D0_LEPTON_BRANCH_COUPLING_CLOSURE
- D0_PHYSICAL_EDGE_COVER_AND_EFT_IR_BOUNDARY

**D0 is NOT declared complete.** Two genuine present-core THE (zone-current split, Feshbach algebraic identity); the rest are proved no-gos, named conditionals, or external passports.
