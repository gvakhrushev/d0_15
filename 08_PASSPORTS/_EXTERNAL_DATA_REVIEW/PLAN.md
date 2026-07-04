# D0 external-data test program — plan (multi-phase)

GOAL: test D0's falsifiable predictions against real downloaded data; refine toward finalizing the theory.
GIT-SAFE: raw data lives in 08_EXTERNAL_DATA/cache/ (gitignored). Committed = manifests (SHA256+URL+date) +
fetch scripts (08_EXTERNAL_DATA/fetch/) + test scripts+results (08_EXTERNAL_DATA/tests/). Reproducible flow, no data blobs.

## Falsifiable external contact points (from the corpus), ranked by value×testability
1. DESI DR2 BAO -> dark-energy w(z): D0 phason W-Z predicts DYNAMICAL DE, sign from Galois σ(φ⁻¹)=−φ.
   DESI DR2 (2024/25) finds evolving DE (w0>−1, wa<0). HIGH value (live, famous). Magnitude open.
2. NuFIT PMNS angles -> D0 δ0-family + large-mixing dichotomy. HIGH.
3. PDG masses (have mass_width_2025.mcd) -> lepton ratios (Lucas 206 + decimals HYP), CKM Wolfenstein. MED-HIGH.
4. Planck n_s -> F8 (corpus: n_s undetermined no-go; test only bounds). MED.
5. CODATA α -> already checked (137.0356 param-free / 137.036 CHK). DONE.
6. Coldea CoNb2O6 E8 m2/m1=φ -> empirical passport. LOW (single ratio, known).
7. SPARC rotation curves -> phason halo (corpus has failure diagnostics). MED, likely negative.
8. Σm_ν bound -> P_sterile=Δα². LOW.

## Phases
0. [DONE] infra: cache(gitignore)+manifests+fetch+tests, network verified, d0_15 is git.
1. DESI DR2 BAO: download official, hash, test D0 w(z) sign+shape vs CPL fit. -> confirm/refute dynamical-DE sign.
2. NuFIT PMNS: download, test δ0/dichotomy predictions vs measured angles.
3. PDG: parse mass_width, test lepton/CKM predictions.
4. Consolidate: data-test report; manifest+fetch committed, data gitignored.

## Discipline
Each test: download->hash->record provenance; compute D0 prediction from FROZEN inputs (no data tuning);
compare; label PASS / PASSPORT / TENSION / REFUTED. Adversarially sanity-check any "confirmed" before recording.
