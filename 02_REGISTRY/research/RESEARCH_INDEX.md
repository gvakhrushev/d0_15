# D0 research navigation and preservation

This navigation map describes the repository at commit `5d632e3c613e9b7ef44aff1a2a3377ec36fe788e` and the open GitHub PRs observed on 26 November 2026. The [research ledger](../RESEARCH_LEDGER.md), [claim registry](../claims.csv), [work manifest](../../00_WORK/manifest.json), and [gravity assembly](../gr_assembly/VIEW.md) remain the authoritative sources for their respective scopes. PR status should be refreshed before using it for a later decision.

The [prioritized synthesis queue](RESEARCH_PRIORITY_2026_11_26.md) records
dependencies and falsification tests for the current research snapshot. The
[certificate inventory](../CERTIFICATE_INVENTORY.md) traces scripts that are
not named directly in books or claim rows to their known consumers.

## Open interfaces

| Interface | Current evidence and boundary | Entry points |
|---|---|---|
| Native physical price and GR | The primary nonlinear case provides an exact sourced construction on the declared family. Its application still needs the physical selection and complete execution price on the same carrier. The source-preserving stopped-price minimum has a scoped exclusion; the reachable field-and-price graph or a native law remains the prospective bridge. | [Primary case](D0_GR_PRIMARY_POSITIVE_CASE.md) · [same-carrier exclusion](A4D_NATIVE_JOINT_FIELD_MINIMUM_EXCLUSION_2026_10_20.md) · [Draft PR #334](https://github.com/gvakhrushev/d0_15/pull/334) |
| Full-affine stationary sector | The registered task asks for an exact nondegenerate curved stationary witness or a no-go on its declared carrier. The published E2 transverse control excludes the earlier witness on the specified enlarged parabolic family. | [Task](../../00_WORK/tasks/EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE.md) · [E2 checker](certificates/a4d_resolved_curved_stationary_e2_enlarged12_full_transverse_check.py) · [Draft PR #202](https://github.com/gvakhrushev/d0_15/pull/202) |
| Resonance divisor | The exact algebraic result and point controls in the packet have a stated carrier. Full higher-codimension rank/nullity stratification remains the registered task; Draft PR #317 contains additional candidate results. | [Published packet](A4D_RESONANCE_DIVISOR_STRATIFICATION.md) · [task](../../00_WORK/tasks/EXP-A4D-RESONANCE-DIVISOR-STRATIFICATION.md) · [Draft PR #317](https://github.com/gvakhrushev/d0_15/pull/317) |
| Dixmier residue and finite moments | `D0-ALPHA-MU2-FULL-LEDGER-001` and `D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001` own finite results. `D0-ALPHA-FESHBACH-DIXMIER-OWNER-001` remains `PROOF-TARGET`, while `D0-DIXMIER-RESIDUE-OWNER-001` has explicit bridge assumptions. The trace-class tower and finite heat trace have their own scoped no-go owners. | [Registry](../claims.csv) · [finite heat-trace module](../../03_FORMALIZATION/D0/Spectral/DixmierFeshbachFiniteHeatTrace.lean) · [tower no-go module](../../03_FORMALIZATION/D0/Spectral/AlphaProfiniteTowerNoGo.lean) |
| CMB smoothing and scale | `D0-CMB-IDS-SMOOTHING-OWNER-001` remains `PROOF-TARGET`. The smoothing-underdetermination and matched-scale tautology no-gos constrain a proposed scale rule. | [Registry](../claims.csv) · [smoothing no-go](../../03_FORMALIZATION/D0/Cosmology/CMBNsSmoothingUndeterminedNoGo.lean) · [matched-scale audit](../../03_FORMALIZATION/D0/Cosmology/FiedlerTiltTautologyNoGo.lean) |
| Matter representation | Clifford relations and CAR are machine-owned on the declared finite representation. The typed sedenion-to-D0 representation and independent-family owners remain `PROOF-TARGET`; the explicit SM subgroup representation in the Albert algebra is `UNPROVED / PROOF-TARGET`. | [Registry](../claims.csv) · [Clifford module](../../03_FORMALIZATION/D0/Algebra/SedenionClifford8.lean) · [family scaffold](../../03_FORMALIZATION/D0/Algebra/CliffordThreeFamilies.lean) · [BOOK_04 §04.8](../../01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md) |
| Formal proof architecture | The work manifest names a formalization and retrieval task with declared remaining physical assumptions. The execution remains open in Draft PR #402. | [Task](../../00_WORK/tasks/WRK-D0-PROOF-ARCHITECTURE-FORMALIZATION.md) · [Draft PR #402](https://github.com/gvakhrushev/d0_15/pull/402) |

The gravity assembly currently reports 22 obligations and 98 results, with five discharged and 54 active results at the configured limit. Its released gates record `D0-FOUNDATION` and `THEORY-TRANSFER` as discharged and `GR` and `RAW-216` as open. These are assembly gates with their own acceptance criteria. [Assembly view](../gr_assembly/VIEW.md) · [Assembly contract](../gr_assembly/contract.json)

## Navigating completed and historical packets

The [research ledger](../RESEARCH_LEDGER.md) records CONTROL dispositions. The [research README](README.md) lists accepted packets, historical supersessions, pending intake, and four reproduced checkpoints from the pilot and PRs #334, #402 and #202. A packet's closure applies to its stated result and carrier. Its downstream premise or physical application may remain open.

Useful reviewed boundaries include the [finite common-center matter groupoid action](MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md), the [endpoint overlap law](MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW.md), and the [path-resolved matter word action](MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md). Their separate conclusions and remaining constitutive requirements are recorded in the research README and ledger.

## Inventory and preservation

At the specified `main` commit, `git ls-files 02_REGISTRY/research` lists 1,532 tracked files, including 746 under `sources/`, 490 under `certificates/`, 288 files at the research root and eight under `inputs/`. At pilot commit `56d097dbae19d5dd9798150f5dd1ba3715dd33f6`, the same query lists 7,761 tracked files. Its working directory also contained 13 untracked files when inventoried. The two counts describe different snapshots and do not classify the difference as disposable.

Some certificates bind exact files and hashes. [Historical book input bindings](../../tools/historical_book_inputs.py), [native checkpoint bindings](../../tools/native_checkpoint_inputs.py), [the research replay runner](../../tools/run_research_certs.py), per-packet source pins and the ledger identify consumers and provenance. Before moving any packet, trace references and committed hashes, preserve its recorded source and result together, and replay affected consumers against the moved inputs. A historical replay checks its pinned inputs and its stated scope. Current books and current claims require their own validation.
