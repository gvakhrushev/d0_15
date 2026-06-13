# D0 v14 Integration Log

Append-only journal of the whole-repo refactor + scoring + Lean-integration work.
Plan: `C:\Users\kmeze\.claude\plans\sharded-humming-stallman.md`.
Canonical registry: `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` (generated:
`03_THEORY_MAP/theory_status_map.csv`, `theory_graph.*`, index markdowns).

---

## Phase 0 — git snapshot + guards

- `git init` + initial commit `base-v14` (1144 files; the four over-ignored
  `05_CERTS/*.json` schema/locked-param files force-added). base-v14 is the
  revert point for all deletes and the `--base` for `check_firewall`.
- Fixed `tools/sync_theory_status_map.py`: `modules_exist()` splits
  semicolon/comma-joined `lean_module` lists before existence checks (the 8
  multi-module LEAN_PROVED rows now resolve True); `cert_path()` strips a leading
  `05_CERTS/` (double-prefix false-negatives). Verified: 8 multi-module rows OK,
  0 missing certs, 0 LEAN_PROVED rows with an absent module.
- New shared status model `tools/d0_status_model.py`: canonical 12 `release_status`
  enum + collapse map, Lean `D0Status` firewall mapping + `canPromoteTo`, and the
  track-fair scoring ladder (spine 1/2/4/7/12/20; track ceilings 20/12/11/7/2/0).
- New guards: `tools/validate_csv.py` (schema/enum/artifacts/FK/staleness),
  `tools/check_firewall.py` (anti-promotion vs base-v14), `tools/regen_graph.ps1`
  (regenerate + delta sanity + `--check-only` idempotence).
- New `00_ROADMAP/INTEGRATION_LOG.md` (this file).

Known worklist surfaced by `validate_csv.py` (handled in Phase 3): ~30 non-canonical
`release_status` values to collapse; `D0-PUB-001` is PYTHON_CERTIFIED with an empty
`python_cert`; generated `theory_status_map.csv` (156) / graph (139) are stale vs
canonical (164) — regenerated in Phase 4.
