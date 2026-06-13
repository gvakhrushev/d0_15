# D0 v15 full proofreading changelog

## Scope

Full release-readiness proofreading pass over Books 00-08, v15 theory-map documents, active certificates and synchronization checks.

## Text corrections applied

1. Fixed residual mojibake in Books 00, 01, 04, 05, 06 and 07:
   - arrows (`->`/mojibake forms) normalized to `→` where the source had corrupted glyphs;
   - `phi`, `tau`, `pi`, `rho`, superscript/subscript fragments restored where mojibake was visible;
   - `D†D` restored in Born/readout text;
   - smart quote mojibake repaired.
2. Fixed duplicated words and repeated phrases:
   - `four four terminal roles` → `four terminal roles`;
   - `finite finite ...` → `finite ...`;
   - `external external comparison protocol` → `external comparison protocol`;
   - `traced-out complement complement` → `traced-out complement`;
   - `ordered ordered` → `ordered`;
   - duplicate Higgs-VEV sentence removed.
3. Retired old `q_mass` wording in active Book 02/03 tables in favor of Boundary Residual Eigenvalue `r_∂` language.
4. Repaired Book 08 SRC synchronization wording:
   - `Nuclear shell-contact SRC passport boundary` restored;
   - Core-13 pointer corrected to `vp_core13_shell_geometry_passport.py`.
5. Rephrased Book 06 Wilsonian map sentence as a definition rather than defensive prose.
6. Standardized pressure notation in Book 07/08 around `mathsf P_fb` / `mathsf P_cap` while preserving required sync tokens.
7. Removed duplicate black-hole-like region line in Book 08.
8. Corrected the master bootstrap theory-map document so the exact finite pressure split uses forward log-differences; the Jacobi trace expression is now explicitly a linearized deformation formula.
9. Tempered publication-facing gauge/horizon/edge synthesis language from overclaiming physical theorem closure to positive D0 sector-law / theorem-target wording.

## Validation

The proofreading pass includes a markdown/text lint over Books 00-08 and v15 theory documents:

- code fences balanced;
- display math fence counts balanced;
- no detected mojibake fragments in active books;
- no duplicated adjacent words in active books or v15 theory documents.

## Checks rerun

- `PASS_V14_CLEAN_CORPUS`
- `PASS: physical bridge discipline (139 claims checked)`
- `PASS` from `09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py`
- `PASS_STANDARD_LANGUAGE_GLOSSARY`
- `PASS_STANDARD_LANGUAGE_AUDIT_BUDGET flagged=114 max=125`
- `PASS_THEORY_HARDENING_SYNC`
- `PASS_V14_BOOK04_OPERATOR_BOUNDARY_SYNC`
- `PASS_V14_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE_SYNC`
- `PASS_MESON_PHASON_DOMAIN_WALLS_SYNC`
- `PASS_V14_GRAVITY_CLOSURE_SYNC`
- `PASS_V14_BOOK04_COMBINATORIAL_SELECTOR_ORIGINS`
- `PASS_ICECUBE_PHASON_DECOHERENCE_SYNC`
- `PASS_V14_BOOK04_COEFFICIENT_ORIGIN_SYNC`
- `PASS_V14_NUCLEAR_SHELL_CONTACT_SRC_SYNC`
- `PASS_V14_TORUS_CORE13_SYNC`
- `PASS_V14_COSMOLOGY_SPLIT_SYNC`
- `PASS_V14_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING_SYNC`
- `PASS_RUN_ALL_CORE_CERTS`
- `PASS_RUN_ALL_BRIDGE_CERTS`
- `PASS_RUN_ALL_EMPIRICAL_PASSPORTS`

## Remaining editorial notes

The corpus is now clean under the active automated checks. Remaining publication work is conceptual organization, not broken-text repair: move legacy sync tokens out of main books only after replacing the check scripts that currently require them.
