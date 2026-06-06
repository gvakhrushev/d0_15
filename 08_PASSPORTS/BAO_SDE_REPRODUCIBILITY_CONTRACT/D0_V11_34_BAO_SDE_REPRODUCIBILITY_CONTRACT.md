# D0 v11.34 — BAO/SDE reproducibility contract

## Claim ID

`D0-BAO-SDE-REPRO-001`

## Status

`EMPIRICAL-PASSPORT-CONTRACT / DATA-HASH-REQUIRED`

## Problem fixed

The previous BAO/SDE passport could replay archived D0-side results, but external review requires an independently reproducible likelihood pipeline using fixed public data products and hashes.

## Required data products

The release contract requires a manifest with:

```text
source_name
source_url
download_date
local_path
sha256
license/usage note
role: BAO | CMB | SN | covariance | chain | baseline
```

## Required runs

1. D0 SDE prediction evaluation.
2. Flat `ΛCDM` baseline.
3. `w0waCDM` baseline if using DESI extended dark-energy comparison.
4. Negative controls:
   - replace `λ_c,λ_r` by neighboring roots/shifted windows;
   - swap Pantheon+ and DES-SN5YR when available;
   - disable archive-pressure correction.

## PASS condition

A BAO/SDE empirical claim may be promoted only if:

```text
all data hashes match;
runner is one-command executable;
D0 parameter count is fixed before data evaluation;
ΛCDM and D0 baselines are reported side by side;
negative controls fail in the predicted direction.
```

## Current v11.34 status

The contract is now release-defined.  Full external likelihood execution remains a data-environment task, not a theorem claim.  This prevents archived-result replay from being presented as full empirical reproduction.

