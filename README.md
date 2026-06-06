# D0 v14

**Finite verification theory of a condensed φ-quasicrystalline vacuum.**

D0 is a research program that treats finite detector readout over a condensed/profinite information-quasicrystalline support as the primitive object, rather than a smooth continuum, particle fields, or a string vacuum.

Observable physics (matter spectrum, gauge interactions, mesons, baryons, neutrinos, cosmology, gravity limits, etc.) arises as defects, holonomies, domain walls, gap labels, and capacity saturations of this support.

## Core principles

- **Finite first**: everything is ultimately grounded in finite, machine-checkable structures.
- **Strict closure discipline**: a claim is closed only when backed by a Lean theorem, a complete finite certificate, a no-go, or an empirical passport within declared scope. "Bridges" to standard physics/EFT are explicit obligations, not proof.
- **Standard language**: D0 mnemonics are always secondary abbreviations. Primary statements use conventional mathematical and physical objects (see the Rosetta stone in `00_LANGUAGE_NORMALIZATION/`).
- **Reproducibility & audit**: Lean formalization + deterministic Python cert runners + pinned external data manifests + knowledge graph of the corpus.

## Repository layout

- `01_BOOKS/` — the theoretical spine (BOOK_00 is the entry contract + admissibility rules; BOOK_01–08 develop the mathematics and physics).
- `03_THEORY_MAP/` — section maps, dependency graphs, semantic index, status.
- `05_CERTS/` — Python verification scripts (`vp_*.py`) and runners that produce finite certificates and diagnostics.
- `08_PASSPORTS/` — curated external data (PDG, BAO/DESI, CMB, LIGO, IceCube, SPARC, CKM, etc.) + manifests + passport results.
- `09_LEAN_FORMALIZATION/` — the Lean 4 package (mathlib-backed). Core theorems live under `D0/`. See its README for build instructions.
- `tools/` — supporting Python (including the vendored graphify knowledge-graph tool).
- `00_LANGUAGE_NORMALIZATION/`, `00_ROADMAP/`, `99_PRESERVED_SOURCE/` — terminology, dependency audits, and frozen reference artifacts.

Generated outputs (certs results, graphify-out, external data cache, release bundles) are git-ignored by design.

## Verification pillars

1. **Lean theorems** (`09_LEAN_FORMALIZATION/`) — `lake build D0.All` + claim map / no-sorry checks.
2. **Finite certificates** (`05_CERTS/`) — `python run_all_core_certs.py`, `run_all_bridge_certs.py`, etc.
3. **Empirical passports** — comparison of D0 readouts against real experimental data (`run_all_empirical_passports.py` and specific `vp_*_passport.py`).

See `D0_CLAIM_CLOSURE_CONTRACT.md` and `01_BOOKS/BOOK_00_*.md` for the exact rules.

## Getting started (after clone)

```bash
# Lean (from repo root)
cd 09_LEAN_FORMALIZATION
lake update
lake exe cache get   # optional accelerator
lake build
lake build D0.All
python tools/check_no_sorry_in_core.py
python tools/check_claim_map_coverage.py

# Example cert / passport runs (from repo root)
cd 05_CERTS
python run_all_core_certs.py
python run_all_empirical_passports.py
```

The project is intentionally large and self-contained. Many heavy caches and one-off outputs are excluded from the repository.

## Knowledge graph

The corpus has an associated persistent knowledge graph (produced by the included graphify tooling). After changes:

- Rebuild orientation with the graphify skill / CLI on the project.
- See `AGENTS.md` for the exact workflow expected inside this project.

## Notes for contributors / AI agents

This repository follows a strict long-term skill-accumulation workflow (see `CLAUDE.md` and `AGENTS.md`).

Repeated processes are turned into reusable skills rather than one-off prompts.

## License / status

Private research snapshot (v14). Contact the author for usage or collaboration.

---

For the mathematical entry point start with:

1. `D0_CLAIM_CLOSURE_CONTRACT.md`
2. `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md`
3. `00_LANGUAGE_NORMALIZATION/D0_STANDARD_LANGUAGE_ROSETTA.md`
4. The Lean `D0/` modules and the active closure indexes in `TheoremLedger/`.
