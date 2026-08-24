# D0 — v15

**A finite verification theory of physics, built to know exactly where its own knowledge ends.**

Repository: **[github.com/gvakhrushev/d0_15](https://github.com/gvakhrushev/d0_15)** · 569 registered claims · Lean 4 (mathlib) + deterministic Python certificates · every integrity gate green (`lake build D0.All` → 4028 jobs; 74-script guard suite passes).

---

D0 takes **finite detector readout** over a condensed / profinite information support as the primitive object — not a smooth continuum, not particle fields, not a string vacuum. Observable physics (matter spectrum, gauge structure, mixing, cosmology, gravity limits) is made to arise as *defects, holonomies, gap labels, and capacity saturations* of that finite support, and every such reading is tracked to one of three honest fates: a machine-checked theorem, a named external bridge, or a proven impossibility.

The theory is organized around one finite scene — the tripartite graph **K(9,11,13)** (33 vertices, 359 edges) with terminal role algebra the quaternion group **Q₈** — and a golden-ratio ladder fixed by four invariants. What can be *forced* from that scene is proved; what cannot is either bounded by a no-go or handed to an explicitly named bridge. Nothing is asserted in between.

## What makes this different

Most speculative fundamental theories hide the seam between what they derive and what they assume. D0 is built to expose it:

- **Forcing, not fitting.** A structure is "owned" only if it is *forced* by the admissibility axiom M1 (no external catalog) — never chosen to match a target. When something is merely selected, it is labeled a passport, not a result.
- **No-gos are first-class.** "X cannot be done" is a proved theorem with a stated admissible class, not a gap. Many of them are the negative face of a positive **extremality theorem** ("what exists is already minimal/maximal") — e.g. the invariant observable algebra is the *unique minimal* one, the present core *saturates* its growth and commutativity extrema, and φ is the minimal quadratic-Pisot carrier selected simultaneously by self-reference, Hurwitz minimax, and Pisot stability.
- **Every physical claim carries its escape hatch.** Each row states the exact missing primitive, no-go, or measured datum it depends on. The corpus counts **25 explicit bridge assumptions**, each with an owner file and a written failure condition.
- **Settled means settled.** A headline claim enters the record only after an independent skeptic pass with a kill-mandate; promotions are monotone and blocked by the anti-inflation firewall unless every dependency is itself closed. The registry is an audited artifact, not a wish list.

The value proposition is not "here is the theory of everything." It is a precise, machine-checked statement of what this finite structure *does* and *does not* determine — and a methodology for building physics claims that cannot quietly lie to themselves.

## Status at a glance

569 registered claims ([full registry](09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv) · [status map](03_THEORY_MAP/theory_status_map.csv) · [scoreboard](03_THEORY_MAP/SCOREBOARD.md)) — **409 backed by a Lean theorem**:

| Closure type | Count | Meaning |
|---|---:|---|
| `CORE-FORMALIZED` | 194 | present-core Lean theorem (the canonical results) |
| `CERT-CLOSED` | 169 | complete finite executable certificate |
| `NO-GO` / `NO_GO_PROVED` | 72 / 7 | proven impossibility within a declared admissible class |
| `BRIDGE-ASSUMPTIONS-EXPLICIT` / `CORE_BRIDGE_SPLIT` | 26 / 13 | holds modulo a named, individually-falsifiable external bridge |
| `PASSPORT-CLOSED` / `EMPIRICAL-PASSPORT` | 20 / 8 | comparison against frozen external data (PDG/DESI/CMB/LIGO/…) |
| `PROOF-TARGET` | 54 | open: a named missing primitive or external datum |
| `BRIDGE-CALIBRATION` · `EXTERNAL-BACKGROUND` · `DEPRECATED` | 3 · 1 · 2 | calibration edges / external context / superseded rows kept for audit continuity |

**The foundational spine, machine-checked.** The scene's uniqueness — that `(9,11,13)` is the unique admissible triple given the capacity ladder and the return-window structure — is a closed Lean capstone (`D0.VNext2.SceneTripleUnique`, `D0-SCENE-TRIPLE-UNIQUE-001`), and the capstone's interval `[9,13]` has itself been dissolved into the owned capacity chain: `D0.VNext2.SceneTripleForced` (`D0-SCENE-FORCED-CHAIN-001`) derives the endpoints, the steps, and the centre `L₅ = 11` from the `FiniteTypes` cardinalities with zero hypotheses, restating the capstone as a reduction with two NAMED joints (GAP-W witness "+1", GAP-E extension completeness) whose ledger rows carry the open-residual state. Every layer states which inputs it owns and which it cites.

**Real-data honesty** ([external-data review](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md)). Against downloaded data: single-number and bridge matches hold (sin²θ_W on-shell 0.23σ, `m_s/m_d = 20`, `m_μ/m_e` integer 206, Coldea `φ`, the α⁻¹ leading term, the PDG seam-α falsifier). DESI DR2 confirms *evolving* dark energy but **not** the specific thawing corner (an over-read, corrected). The PMNS `δ₀`-family and the LIGO `φ⁻¹` mass-defect are **post-hoc passport fits, not discriminating** (demoted). The SPARC phason-halo dark-matter kernel is an honest **negative** (rejected in ~91% of galaxies). There is no sharp multi-point discriminating confirmation — stated plainly rather than dressed up.

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
| [`08_PASSPORTS/`](08_PASSPORTS/) | curated external data (PDG, DESI, CMB, LIGO, IceCube, SPARC, CKM…) + SHA256 manifests; [`_EXTERNAL_DATA_REVIEW/`](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/) holds the git-safe real-data test flow and the honest [scoreboard](08_PASSPORTS/_EXTERNAL_DATA_REVIEW/tests/SCOREBOARD.md) |
| [`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/) | the Lean 4 package (mathlib-backed); theorems under `D0/`, the canonical registry + assumption ledger under `docs/` — see [its README](09_LEAN_FORMALIZATION/README.md) |
| [`tools/`](tools/) | CI guard scripts, registry sync, scoreboard, and knowledge-graph tooling |
| [`docs/`](docs/) | internal roadmaps and developer notes |

Generated outputs (cert `*.results.json`, `graphify-out/`, external-data cache, release bundles) are git-ignored by design.

## Verification pillars

1. **Lean theorems** ([`09_LEAN_FORMALIZATION/`](09_LEAN_FORMALIZATION/)) — `lake build D0.All` (4028 jobs) + claim-map coverage + no-`sorry`-in-core checks.
2. **Finite certificates** ([`05_CERTS/`](05_CERTS/)) — deterministic `vp_*.py` with *reachable FAIL controls* (a cert that cannot fail is rejected by `check_cert_can_fail.py`), run via `run_all_core_certs.py` / `run_all_bridge_certs.py`.
3. **Explicit bridges & passports** — external data compared against frozen manifests; data never *defines* a core theorem, and every bridge assumption is registered in [`docs/LEAN_ASSUMPTION_LEDGER.csv`](09_LEAN_FORMALIZATION/docs/LEAN_ASSUMPTION_LEDGER.csv) with an owner file and a failure meaning.
4. **Anti-inflation firewall** — `vp_status_inflation_audit.py` + `check_firewall.py` block any promotion that closes a claim without an owner; the audit ships with a planted negative control that must fire.

Rules of record: [`D0_CLAIM_CLOSURE_CONTRACT.md`](D0_CLAIM_CLOSURE_CONTRACT.md) and [`01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md`](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md).

## Getting started (after clone)

```bash
# 0. Python deps for the certs/tools (numpy, sympy, pandas)
pip install -r requirements.txt

# 1. Lean (heavy build artifacts are kept outside the repo)
./tools/lean_dev.ps1 update
./tools/lean_dev.ps1 exe cache get         # optional accelerator
./tools/lean_dev.ps1 build D0.All
python 09_LEAN_FORMALIZATION/tools/check_no_sorry_in_core.py
python 09_LEAN_FORMALIZATION/tools/check_claim_map_coverage.py

# 2. Integrity gates (the CI suite — .github/workflows/guards.yml)
python tools/validate_csv.py                       # canonical registry integrity
python 05_CERTS/vp_status_inflation_audit.py       # anti-promotion audit (control must fire)
python tools/check_firewall.py                     # firewall vs baseline
python tools/d0_score.py                           # writes 03_THEORY_MAP/SCOREBOARD.md

# 3. Certificates / passports
cd 05_CERTS
python run_all_core_certs.py
python run_all_empirical_passports.py
```

For normal editing, Lean runs are deferred — see [`LEAN_DEFERRED_RUN_POLICY.md`](09_LEAN_FORMALIZATION/docs/LEAN_DEFERRED_RUN_POLICY.md).

## Mathematical entry points

1. [`D0_CLAIM_CLOSURE_CONTRACT.md`](D0_CLAIM_CLOSURE_CONTRACT.md) — what "closed" means, and the status vocabulary above.
2. [`01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md`](01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md) — the admissibility axiom M1 and the forcing grammar.
3. [`01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md`](01_BOOKS/) — the scene K(9,11,13), Ω₈ ≅ Q₈, and the golden ladder.
4. [`00_LANGUAGE_NORMALIZATION/`](00_LANGUAGE_NORMALIZATION/) — the standard-language Rosetta stone (every D0 mnemonic in conventional terms).
5. The Lean `D0/` modules and the active closure indexes in [`09_LEAN_FORMALIZATION/D0/TheoremLedger/`](09_LEAN_FORMALIZATION/D0/TheoremLedger/).
6. **The measurement-dyad house** — complementarity as derived architecture: `D0.Core.DyadComplementarity` → `DyadFringeBridge` (fringe contrast ≡ V, derived) → `DyadClosureForcing` (unit closure forced by M1) → `TriadComplementarity` + `TriadSufficiency` (the trinary law and its exactness), with `EWTransportSectors` owning the α depth decomposition.

## License / status

Private research snapshot (**v15**). Contact the author for usage or collaboration.
