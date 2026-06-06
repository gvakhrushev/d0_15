# PDG Passport History Appendix

This appendix preserves the historical PDG passport import trail outside the active books. The active corpus should refer to the PDG route only as an empirical passport over frozen D0 operators.

Preserved historical inputs:

```text
99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/
99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/cert/phi_pdg_strict.py
99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/protocols/phi_pdg_strict.json
```

Active passport files:

```text
08_PASSPORTS/PDG/data/mass_width_2025.mcd
08_PASSPORTS/PDG/pdg_dataset_manifest.json
08_PASSPORTS/PDG/pdg_strict_protocol.json
08_PASSPORTS/PDG/core13_geometry_protocol.json
05_CERTS/vp_core13_shell_geometry_passport.py
05_CERTS/vp_pdg_strict_passport.py
```

Mandatory passport facts:

```text
PDG dataset: 08_PASSPORTS/PDG/data/mass_width_2025.mcd
SHA-256: 7073c02222f08c19f5c40e422c5a54e9f9a75622b9e10b1b64096144e262d4b5
holdout: seed=20250101, fraction=0.2
multiple testing: Bonferroni over delta8_hypotheses
rank/minimax distinction: required
```

Acceptance rule: a PDG passport can only run after the D0 operator or geometry owner is frozen. A geometry diagnostic may not tune a core operator. A mass-table fit may not become a theorem owner.
