# D0 (Golden Pass30) - executable corpus

This repository contains the D0 books, executable certificates (CERT), protocol files, and reproducible artifacts.

## 0. Navigation

- [1. Repository layout](#1-repository-layout)
- [2. Requirements](#2-requirements)
- [3. Setup](#3-setup)
- [4. Quickstart](#4-quickstart)
- [5. Running certificates](#5-running-certificates)
- [6. Protocol policy](#6-protocol-policy)
- [7. Certificate index](#7-certificate-index)
- [8. PDG data](#8-pdg-data)
- [9. Environment variables](#9-environment-variables)
- [10. Publication manifest](#10-publication-manifest)
- [11. CI](#11-ci)

## 1. Repository layout

- `.github/` - CI workflows
- `books/` - the six books (I-VI)
- `d0/` - CORE library (single source of truth for constants + shared utilities)
- `cert/` - executable certificates (entrypoints)
- `protocols/` - protocol files (all knobs must live here)
- `tools/` - release tools (manifest generation/verification)
- `D0_PUBLICATION_MANIFEST_GOLDEN_PASS30.txt` - release manifest (sha256 + bytes)
- `artifacts/` - runtime outputs (ignored by git; runtime outputs are moved here)
- `data/` - pinned external datasets (PDG cache)

## 2. Requirements

- Python 3.9+ (3.10+ recommended)
- Packages: `numpy`, `pandas`, `matplotlib`, `requests`

## 3. Setup

All commands below assume you are in the repo root.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy pandas matplotlib requests
export PYTHONPATH=.
```

## 4. Quickstart

Run a single certificate (outputs go to `artifacts/` by default):

```bash
export D0_OUTDIR=artifacts
python3 cert/book6_certpack.py --protocol protocols/book6_certpack.json --core-only --no-perc
```

## 5. Running certificates

General pattern (recommended):

```bash
export D0_OUTDIR=artifacts
export PYTHONPATH=.
python3 cert/<script>.py --protocol protocols/<protocol>.json
```

You can also set a default protocol via `D0_PROTOCOL` and omit `--protocol`:

```bash
export D0_PROTOCOL=protocols/d0_sr_budget.json
python3 cert/d0_sr_budget.py
```

Exit codes:
- Most certificate scripts return `0` on PASS and `2` on FAIL.
- `cert/book6_certpack.py` is a report pack and does not return a PASS/FAIL exit code (it exits `0` unless there is a runtime error).
- `cert/d0_sr_budget.py` (SELFTEST) and `cert/d0_decay5.py` (CHK) structurally always exit `0`: their comparison cannot return FAIL. They emit a `status_class` field in their JSON report and are **not** counted as empirical verification (see [Certificate index](#7-certificate-index)).

Run all certificates (CI order):

```bash
export D0_OUTDIR=artifacts
export PYTHONPATH=.
python3 cert/book6_certpack.py --protocol protocols/book6_certpack.json --core-only --no-perc
python3 cert/metrological_audit.py --protocol protocols/metrological_audit.json --selftest
python3 cert/phi_pdg_strict.py --protocol protocols/phi_pdg_strict.json
python3 cert/d0_sr_budget.py --protocol protocols/d0_sr_budget.json
python3 cert/d0_decay5.py --protocol protocols/d0_decay5.json
python3 cert/qec_comparison.py --protocol protocols/book5_qec_comparison.json
python3 cert/phi_cop_complete.py --protocol protocols/book5_phi_cop_complete.json
python3 cert/sat_solver.py --protocol protocols/book5_sat_solver.json
python3 cert/tsp_solver.py --protocol protocols/book5_tsp_solver.json
```

## 6. Protocol policy

- All certificate knobs must live in `protocols/*.json`.
- Changing a protocol requires updating the publication manifest.

## 7. Certificate index

Honesty discipline: a check that cannot structurally return FAIL is not a
certificate. Entries are tagged by status class — genuine falsifiable
certificates (e.g. `book6_certpack`, `phi_pdg_strict`, `qec_comparison`) carry
no extra tag, while **SELFTEST** (`d0_sr_budget`) and **CHK** (`d0_decay5`)
entries restate their own model/generator, emit a `status_class` field in their
JSON report, and are not counted as empirical verification.

### cert/book6_certpack.py (BOOK VI pack)

- Protocol: `protocols/book6_certpack.json`
- Outputs (default):
  - `artifacts/book6_certpack.json`
  - `artifacts/d0_summary_L129.png`
  - `artifacts/d0_cosmo_timeseries_L129.csv`
- Notes:
  - Use `--core-only` to skip slow/optional sections.
  - Use `--no-perc` or set `D0_PERC=0` to skip percolation toy.
  - Use `--show` to display plots interactively (otherwise they are saved).

### cert/metrological_audit.py (BOOK IV audit)

- Protocol: `protocols/metrological_audit.json`
- Output: `artifacts/d0_metrological_audit_report.json`
- Notes:
  - Use `--selftest` for the built-in canonical PASS case.
  - Otherwise provide at least one of: `--geom`, `--spectrum`, `--seam`, `--power`.

### cert/phi_pdg_strict.py (BOOK III/IV PDG strict)

- Protocol: `protocols/phi_pdg_strict.json`
- Output (default): `artifacts/cert_phi_pdg_strict/phi_pdg_strict_report.json`
- Notes:
  - Downloads PDG data if missing (see [PDG data](#pdg-data)).
  - Plots are saved under `artifacts/cert_phi_pdg_strict/plots/`.

### cert/d0_sr_budget.py (SELFTEST 19.4.SR)

- Status class: **SELFTEST** — not a falsifiable PASS/FAIL certificate.
- Protocol: `protocols/d0_sr_budget.json`
- Output (default): `artifacts/cert_19_4_sr/`
  - `sr_budget_report.json` (carries `status_class: "SELFTEST"`)
  - `sr_budget_table.csv`
  - `sr_budget_plot.png`
  - `sr_budget_error.png`
- Notes:
  - The "measured" channel is defined as the predicted value (`meas := pred`),
    so the error is identically 0 and the check can never return FAIL. It only
    confirms `tau/t = sqrt(1 - v^2)` is evaluated without error.
  - It does **not** verify the relation against any independent dataset and
    must **not** be counted as empirical verification. To promote it to a real
    certificate, ingest a measured `tau/t` dataset and compare against `pred`.

### cert/d0_decay5.py (CHK 19.4.DECAY5)

- Status class: **CHK** — self-consistency check, not a falsifiable PASS/FAIL
  certificate (matches `[CHK 19.4.DECAY5]` in BOOK IV).
- Protocol: `protocols/d0_decay5.json`
- Output (default): `artifacts/cert_19_4_decay5/`
  - `decay5_report.json` (carries `status_class: "CHK"`)
  - `decay5_counts.csv`
  - `decay5_loglog.png`
- Notes:
  - The count series is generated as exactly `round(count_scale * R**5)`, so
    the fitted log-log slope is ~5 by construction (only integer-rounding
    noise). The check restates its own generator and can never return FAIL.
  - It is **not** external evidence that `D_Sigma = 5` and must **not** be
    counted as empirical verification. To promote it to a real certificate,
    supply an independently-produced count series instead of the `R**5`
    generator.

### cert/qec_comparison.py (CERT 24.5.1)

- Protocol: `protocols/book5_qec_comparison.json`
- Output (default): `artifacts/cert_24_5_1_qec/book5_qec_comparison_report.json`
- Notes:
  - Add `--core-only` to disable the BRIDGE proxy channel.

### cert/phi_cop_complete.py (CERT 24.5.2)

- Protocol: `protocols/book5_phi_cop_complete.json`
- Outputs (default): `artifacts/cert_24_5_2_phi_cop/`
  - `phi_cop_certificate.txt`
  - `phi_cop_certificate.json`
  - `phi_cop_logic_proof.txt`
  - `phi_cop_tree.json.gz` (only if enabled in protocol)
  - `book5_phi_cop_report.json`

### cert/sat_solver.py (CERT 24.5.3 SAT)

- Protocol: `protocols/book5_sat_solver.json`
- Output (default): `artifacts/cert_24_5_3_phi_sat/book5_phi_sat_report.json`

### cert/tsp_solver.py (CERT 24.5.3 TSP)

- Protocol: `protocols/book5_tsp_solver.json`
- Output (default): `artifacts/cert_24_5_3_phi_tsp/book5_phi_tsp_report.json`

## 8. PDG data

`cert/phi_pdg_strict.py` uses the PDG mass/width table.

Pinned dataset (default year 2025):
- `data/mass_width_2025.mcd`
- SHA256: `7073c02222f08c19f5c40e422c5a54e9f9a75622b9e10b1b64096144e262d4b5`

Behavior:
- If the file is present, the script uses the cache.
- If missing and `D0_PDG_OFFLINE=0`, the script downloads it.
- If missing and `D0_PDG_OFFLINE=1`, the script fails fast.

## 9. Environment variables

Global:
- `D0_OUTDIR` - output directory (default: `artifacts/`)
- `D0_PROTOCOL` - default protocol path for cert scripts
- `D0_DATA_DIR` - dataset cache root (default: `data/`)

PDG strict (cert/phi_pdg_strict.py):
- `D0_PDG_YEAR` - PDG year (default: `2025`)
- `D0_PDG_OFFLINE` - set to `1` to disable network download
- `D0_PDG_TIMEOUT_S` - download timeout in seconds (default: `30`)
- `D0_MIN_POOL_N` - minimum pool size for delta8 structure tests (default: `72`)

Book VI pack (cert/book6_certpack.py):
- `D0_VERBOSE` - `1` to print details, `0` to silence
- `D0_UQ_N` - grid size for u-quantities (default: `4096`)
- `D0_SDE_COARSE_N` - coarse grid for S_DE search (default: `4096`)
- `D0_SDE_GOLD_ITERS` - golden-section iterations (default: `80`)
- `D0_SDE_FWHM_ITERS` - FWHM iterations (default: `80`)
- `D0_T0_S` - BRIDGE-only SI tick override (seconds per D0-time)
- `D0_AGE_UNIVERSE_S` - macro age anchor (seconds)
- `D0_DISABLE_TOME23` - set to `1` to disable micro-to-macro bridge
- `D0_M_E_KG` - electron mass override (kg)
- `D0_HBAR_J_S` - hbar override (J*s)
- `D0_D_ELECTRON` - electron depth override
- `D0_D_VACUUM` - vacuum depth override
- `D0_REF_NEUTRON_BOTTLE_S` - neutron bottle reference (seconds)
- `D0_REF_NEUTRON_BEAM_S` - neutron beam reference (seconds)
- `D0_PLATEAU_T_LO` - lower bound for plateau search (t)
- `D0_PLATEAU_T_HI` - upper bound for plateau search (t)
- `D0_PLATEAU_N` - plateau scan grid size
- `D0_PLATEAU_MIN_PTS` - minimum points per plateau window
- `D0_BOOK6_CERTS` - set to `0` to skip BOOK VI cert pack
- `D0_PERC` - set to `0` to skip percolation toy
- `D0_PERC_TRIALS` - percolation trials (default: `200`)
- `D0_PERC_GRID` - percolation grid size (default: `40`)

## 10. Publication manifest

Generate and verify the release manifest (sha256 + bytes):

```bash
python3 tools/make_manifest.py
python3 tools/verify_manifest.py
```

The manifest file is `D0_PUBLICATION_MANIFEST_GOLDEN_PASS30.txt`.
It is expected to cover:
- `books/`, `d0/`, `cert/`, `protocols/`, `tools/`, `data/`, `.github/`, and `README.md`
It intentionally excludes:
- `artifacts/` (runtime outputs)
- `__pycache__/` (bytecode caches)
- the manifest file itself (self-hash would be unstable)
- `.DS_Store` (OS metadata)

## 11. CI

GitHub Actions runs certificates + manifest verification on every push/PR:
- `.github/workflows/certs.yml`
