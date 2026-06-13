# D0 v14 PDG / Golden Pass30 Integration Audit

This audit records the active import from the older `d0-main` Golden Pass30 branch into the current archive.

## Active imports

- `08_PASSPORTS/PDG/data/mass_width_2025.mcd`
- `08_PASSPORTS/PDG/pdg_dataset_manifest.json`
- `08_PASSPORTS/PDG/pdg_strict_protocol.json`
- `08_PASSPORTS/PDG/core13_geometry_protocol.json`
- `05_CERTS/vp_pdg_strict_passport.py`
- `05_CERTS/vp_core13_shell_geometry_passport.py`

## Pinned dataset

```text
file: 08_PASSPORTS/PDG/data/mass_width_2025.mcd
sha256: 7073c02222f08c19f5c40e422c5a54e9f9a75622b9e10b1b64096144e262d4b5
legacy protocol: PHI_PDG_STRICT_V1
holdout seed: 20250101
holdout fraction: 0.2
multiple testing: bonferroni over delta8_hypotheses
```

## Preserved source

The legacy branch is preserved outside the active theory text:

```text
99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/
```

This preserved source is not a core theorem owner. It is retained for reproducibility, audit, and future passport refactoring.

## Active discipline

PDG and Core-13 diagnostics validate or falsify frozen D0 operators and geometry embeddings. They do not create D0 core operators, tune torus geometry, or promote diagnostic fits into theorem owners.
