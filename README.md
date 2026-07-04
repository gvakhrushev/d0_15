# D0 v15

**Finite verification theory of a condensed φ-quasicrystalline vacuum.**

Repository: **[github.com/gvakhrushev/d0_15](https://github.com/gvakhrushev/d0_15)** · 537 registered claims · Lean 4 (mathlib) + deterministic Python certificates · all integrity gates green.

D0 treats *finite detector readout* over a condensed/profinite information-quasicrystalline support as the primitive object — not a smooth continuum, particle fields, or a string vacuum. Observable physics (matter spectrum, gauge interactions, mesons, baryons, neutrinos, cosmology, gravity limits) arises as defects, holonomies, domain walls, gap labels, and capacity saturations of that support.

## Core principles

- **Finite first** — everything is ultimately grounded in finite, machine-checkable structures.
- **Strict closure discipline** — a claim is closed only when backed by a Lean theorem, a complete finite certificate, a formal no-go, or an empirical passport *within declared scope*. "Bridges" to standard physics/EFT are explicit obligations, never proof.
- **Standard language** — D0 mnemonics are always secondary abbreviations; primary statements use conventional mathematical/physical objects (Rosetta stone: [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/)).
- **Reproducibility & audit** — Lean formalization + deterministic Python cert runners + pinned external-data manifests + a corpus knowledge graph, all enforced by CI gates.

## Status at a glance

537 registered claims ([full registry](09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv) · [theory status map](03_THEORY_MAP/theory_status_map.csv) · [scoreboard](03_THEORY_MAP/SCOREBOARD.md)):

| Closure type | Count | Meaning |
|---|---:|---|
| `CORE-FORMALIZED` | 184 | present-core Lean theorem (the canonical results) |
| `CERT-CLOSED` | 166 | complete finite executable certificate |
| `NO-GO` / `NO_GO_PROVED` | 72 / 8 | proven impossibility within a declared admissible class |
| `BRIDGE-ASSUMPTIONS-EXPLICIT` / `CORE_BRIDGE_SPLIT` | 25 / 7 | result holds modulo a named, explicit external bridge |
| `PASSPORT-CLOSED` / `EMPIRICAL-PASSPORT` | 20 / 8 | comparison against frozen external data (PDG/DESI/CMB/LIGO/…) |
| `PROOF-TARGET` | 41 | open: a named missing primitive or external datum |
| `BRIDGE-CALIBRATION` · `EXTERNAL-BACKGROUND` · `DEPRECATED` | 3 · 1 · 2 | calibration edges / external context / retired |

**D0 is not "complete physics."** Every physical reading remains gated by an explicitly named missing primitive, a no-go, or an external passport — by design. The value is a precise, machine-checked statement of what this finite structure *does* and *does not* determine.

**Real-data honesty (external-data review).** Confronted with downloaded data ([scoreboard](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md)): single-number/bridge matches hold (sin²θ_W on-shell 0.23σ, `m_s/m_d=20`, `m_μ/m_e` integer 206, Coldea `φ`, `α⁻¹` leading term, the PDG seam-`α` falsifier); DESI DR2 confirms *evolving* dark energy but **not** the specific thawing corner (an over-read, corrected); the PMNS `δ₀`-family and the LIGO `φ⁻¹` mass-defect are **post-hoc passport fits, not discriminating** (demoted); and the SPARC phason-halo dark-matter kernel is an honest **negative** (rejected in 91% of galaxies). There is no sharp multi-point discriminating confirmation — stated plainly rather than dressed up.

## Repository layout

| Path | Contents |
|---|---|
| [`01_BOOKS/`](01_BOOKS/) | the theoretical spine — `BOOK_00` is the entry contract + admissibility rules; `BOOK_01`–`08` develop the mathematics and physics |
| [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/) | the standard-language Rosetta stone (D0 mnemonic ↔ conventional object) |
| [`00_PUBLICATION/`](00_PUBLICATION/) | publication-facing docs: claims register, abstract, release notes, do-not-claim list, reviewer risk ledger |
| [`03_THEORY_MAP/`](03_THEORY_MAP/) | section maps, dependency graph, semantic index, status map, scoreboard |
| [`04_VERIFICATION/`](04_VERIFICATION/) | closure protocol, blocker tables, claim-owner normalization, inflation audit |
| [`05_CERTS/`](05_CERTS/) | Python verification scripts (`vp_*.py`) + runners that produce finite certificates |
| [`06_AUDIT/`](06_AUDIT/) | corpus peer/self review + standard-language audit trail |
| [`08_PASSPORTS/`](08_PASSPORTS/) | curated external data (PDG, BAO/DESI, CMB, LIGO, IceCube, SPARC, CKM…) + manifests; [`_EXTERNAL_DATA_REVIEW/`](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/) holds the git-safe real-data test flow (SHA256 manifests + fetch scripts committed, raw data gitignored) and the honest [scoreboard](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md) |
| [`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/) | the Lean 4 package (mathlib-backed); core theorems under `D0/` — see [its README](09_LEAN_FORMALIZATION/README.md) |
| [`tools/`](tools/) | gate scripts, registry sync, scoreboard, and the vendored graphify knowledge-graph tool |
| [`docs/`](docs/) | internal roadmaps and developer notes |

Generated outputs (cert `*.results.json`, `graphify-out/`, the external-data cache, release bundles) are git-ignored by design.

## Verification pillars

1. **Lean theorems** ([`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/)) — `lake build D0.All` + claim-map coverage + no-`sorry` checks.
2. **Finite certificates** ([`05_CERTS/`](05_CERTS/)) — deterministic `vp_*.py` with reachable FAIL controls, run via `run_all_core_certs.py` / `run_all_bridge_certs.py`.
3. **Empirical passports** — D0 readouts compared against frozen experimental data (`run_all_empirical_passports.py`, `vp_*_passport.py`); data never *defines* a core theorem.

Rules of record: [`D0_CLAIM_CLOSURE_CONTRACT.md`](D0_CLAIM_CLOSURE_CONTRACT.md) and [`01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md`](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md).

## Getting started (after clone)

```bash
# 0. Python dependencies for the certs/tools (numpy, sympy, pandas)
pip install -r requirements.txt

# 1. Lean (from repo root) — heavy build artifacts are kept outside the repo
./tools/lean_dev.ps1 update
./tools/lean_dev.ps1 exe cache get        # optional accelerator
./tools/lean_dev.ps1 build D0.All
python 09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py
python 09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py

# 2. Integrity gates (the CI suite — see .github/workflows/guards.yml)
python tools/validate_csv.py              # canonical registry integrity
python tools/check_firewall.py            # anti-promotion firewall (diff vs baseline)
python tools/check_book_cert_references.py
python tools/check_no_tautology_proofs.py
python tools/d0_score.py                  # writes 03_THEORY_MAP/SCOREBOARD.md

# 3. Certificates / passports
cd 05_CERTS
python run_all_core_certs.py
python run_all_empirical_passports.py
```

`tools/lean_dev.ps1` junctions `09_LEAN_FORMALIZATION/.lake` to `$HOME/.d0_lean_cache/...` (override with `D0_LEAN_CACHE_ROOT`). For normal editing, Lean runs are deferred — see [`LEAN_DEFERRED_RUN_POLICY.md`](09_LEAN_FORMALIZATION/docs/LEAN_DEFERRED_RUN_POLICY.md).

## Mathematical entry points

1. [`D0_CLAIM_CLOSURE_CONTRACT.md`](D0_CLAIM_CLOSURE_CONTRACT.md) — what "closed" means.
2. [`01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md`](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md) — admissibility rules.
3. [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/) — the standard-language Rosetta stone.
4. The Lean `D0/` modules and the active closure indexes in [`09_LEAN_FORMALIZATION/D0/TheoremLedger/`](09_LEAN_FORMALIZATION/D0/TheoremLedger/).

## Contributors / AI agents

This repo follows a strict long-term skill-accumulation workflow — repeated processes become reusable skills, not one-off prompts. See [`CLAUDE.md`](CLAUDE.md) and [`AGENTS.md`](AGENTS.md).

## License / status

Private research snapshot (**v15**). Contact the author for usage or collaboration.
