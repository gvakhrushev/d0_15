# D0 proof architecture and formalization

## Status

Primary integration artifact for WRK-D0-PROOF-ARCHITECTURE-FORMALIZATION. The broad objective remains active. C0 is not frozen or independently accepted, so no formalization coverage percentage is reported. Counts below describe starting inputs, not the C0 denominator.

## Starting snapshot

Task registration was merged into main as 8b94198c8dfbdf5983ad0b350b058fb30bb68a54. Execution continues on wrk/d0-proof-architecture-formalization in Draft PR #402. Lean toolchain: leanprover/lean4:v4.30.0.

Pinned starting inputs at that commit:

| Path | Blob |
|---|---|
| 00_WORK/tasks/WRK-D0-PROOF-ARCHITECTURE-FORMALIZATION.md | d68b0120b8e202bcec0db26f26cdb3effa7f5a80 |
| 00_WORK/manifest.json | 011ea3c335746b5e05d1b4e6bc5cfa95782a5a1e |
| 02_REGISTRY/claims.csv | fc24227434bc917fa40ec880e9caff9b6b6b07b4 |
| 02_REGISTRY/assumptions.csv | 69594ed273d327d7ff541b0ff1ad4349a3f799f9 |
| 02_REGISTRY/aliases.csv | 4e52bb7a642334c7ad958e6d83e3ef7e47a6bb53 |
| 02_REGISTRY/formal_support.csv | 8044cf4065658c2ae471ad5daf9d8ac9d5857e31 |
| 02_REGISTRY/gr_assembly/contract.json | 3d4a93cb2ba70f124e258669218df3f056a903d6 |
| 02_REGISTRY/gr_assembly/applications.json | 33e7114821f2bdf849f00bbeaf31e783885bd442 |
| 03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean | 8f52c249a17a57d36b8bdf249450f9f9bdb29273 |
| 03_FORMALIZATION/D0/All.lean | 04e7d1abbe2f09eaafe258a5fc91f9ed7d66bcee |
| tools/generate_lean_views.py | fc8b9a41dac18c69fae5ea54797354a3ca9cd3fe |
| tools/formalization_debt_audit.py | 0e45cb38012f1948d89cb77c2e6987db50dfb13b |
| tools/lean_task_build.py | 911df7af16c7169f1611bd5f63a80b93d283d9c1 |

#334 remains an unmerged scientific owner. Its task-pinned published head is fe5cf335da04cac14e50407b03f98b96be17dc52. The selected raising-operator source and consumer slices below pass their source-pin/read gate; formalization, application review, and independent C0 acceptance remain outstanding. Any additional #334 slice must record its published commit, path, blob, read proof, scope, and reviewed slice.

## Architecture

Keep three relations distinct:

1. **Lean proof dependencies:** actual elaborated declarations in theorem types/proof terms, transitive axioms, source range, module, and compiled public import path.
2. **Mathematical applications:** exact theorem, objects, maps, hypotheses, carrier/source/norm, conclusion, and a compiled adapter or independently accepted application.
3. **Conceptual retrieval:** claim IDs, assumptions, aliases, owners, source sections, results, counterexamples, and attempts.

A proof dependency is not an application; a similar name is not proof; indexing is not independent acceptance.

| Concern | Authority and rule |
|---|---|
| Claim text/status | claims.csv; preserve IDs, owners and current status. |
| Assumptions | assumptions.csv plus actual theorem premises; keep them quantified. |
| Lean support | formal_support.csv, elaborated declarations and imports; CSV names are locators only. |
| Aliases | aliases.csv and source locators; aliases are lookup edges. |
| GR obligations/interfaces | gr_assembly/contract.json; keep existing owners and conventions. |
| Results/applications | gr_assembly/applications.json; a result pointer or evidence file closes no obligation. |
| Historical evidence | pinned Git commit/path/blob and source digest; retain bytes and scope. |
| Public imports/views | D0.All, compatibility modules and existing generators; preserve paths or add wrappers. |

ClaimMap.lean stores theoremName as String and explicitly says it is metadata. check_claim_map_coverage.py and formalization_debt_audit.py are structural checks, not semantic theorem-to-prose verification. Add a semantic layer over current authorities; do not create another claim, assumption, status, acceptance, queue, or obligation registry.

The declaration extractor queries a selected compiled public import (`D0.All` by default) and records full name, elaborated type, telescope binders with type/implicitness/proposition status, type/proof dependencies, transitive axiom footprint, source declaration range/module, snapshot, toolchain, and public import path. Before extraction it asks Lake to build the selected import root under the same shared lock; the source digest is checked across both build and query, so an old `.olean` cannot be reported against current project source. The digest includes repository-owned Lean files and the Lake configuration, while `.lake` package checkouts are excluded and pinned through `lake-manifest.json`. `--all-claims` retains every current claims.csv row, including unresolved theorem locators, and batch-resolves exact candidates in one imported environment; this produces a reproducible crosswalk candidate, not semantic coverage. This is exact elaborated evidence, not a normalized semantic equivalence proof. A reviewer binds that type to the source claim's object, domain, quantifiers, and assumptions. Load-bearing applications need compiled Lean adapters over actual objects and maps; a field that assumes the desired conclusion is not an adapter.

The collector has run successfully on `D0.Foundation.VerificationCore.verification_core` and the new `D0.Geometry.archiveJuliaRaisingQuery_vacuum_exterior`. Both are found in the compiled environment with actual types, binders, proof/type dependencies, source ranges, and axiom footprints. The verification theorem retains its quantified `FutureExecution` and `TheoryVerification` inputs and is located at lines 227–240 of its source. The Eq. (26) model theorem is located at lines 50–57 of `ArchiveJuliaRaisingOperatorReadout.lean`; its exact type is `∀ u M, archiveFockExteriorEquiv (archiveJuliaRaisingQuery u M vacuum) = ι ℝ u`, with `u : RoleSpace` and `M : RoleSpace ≃ₗ[ℝ] RoleSpace`. The collector reports `Classical.choice`, `Quot.sound`, and `propext` for both this theorem and its existing creator-on-vacuum lemma. These are exposed dependencies of the existing finite-carrier representation; this checkpoint does not claim an axiom-free kernel. The Eq. (26) inventory result was captured at HEAD `b2b73963991bb18c42766ae753bef1c70314c9ab` with `worktree_dirty=true`, Lean source digest `29155ab90a339219f44c38b8c69cc91b76e74121cc4a86ef2bcb186910a80884`, and collector script SHA-256 `4d4edc04deec3e2ad185e9fcf1ba3b7e63bfb16ba1fbc3d9905d253aa2d8ef11` under Lean 4.30.0.

Search is deterministic and bounded: exact IDs/names, aliases, sections, declared result/application links, and scoped attempts first. Ranking may suggest text candidates but cannot set truth. Search failure is not nonexistence.

The read-only `tools/proof_architecture.py` view composes current claims, registered assumptions, formal-support locators, aliases, assembly contracts/results/applications/attempts, conceptual presupposition edges, and bounded full-text candidates. Claims expose their registered assumption rows separately from applications and conceptual edges. Commands are `search`, `show`, `why`, `reuse`, and `impact`; `show NAME --lean --import-root MODULE` calls the elaborated declaration collector. Every answer includes source digests and a snapshot commit. Conceptual edges, assumption links, alias lookup, text matches, declared application edges, and elaborated Lean facts are distinct output kinds. `impact KEY` follows only currently declared evidence/application refs; `impact --base REF` delegates to the existing assembly diff impact. Neither form claims a complete global semantic impact graph.

## C0 candidate boundary

C0 is a reviewed set of mathematical units, not files, modules, registry rows, or graph nodes. The figures below describe candidate inputs only; they are not a frozen denominator and no coverage percentage is valid before independent acceptance of the exact package.

Initial candidate sources and crosswalk inputs:

- The 889 claims.csv IDs are claim candidates keyed initially by claim ID and exact book/section locator. Each may split, overlap, or need a source-backed disposition before becoming one unit.
- The 31 assumption IDs are premise crosswalk inputs. Preserve the actual quantified hypotheses on results; do not count an assumption row as a result by default.
- The 178 formal_support.csv rows are proof-support crosswalk inputs and candidate declaration locators, not 178 independently accepted results.
- The 58 aliases are lookup edges: resolve the two canonical-target aliases and inspect the 56 legacy first_reference values for missing assertions.
- The 54 assembly result pointers still require reconciliation to a claim or exact source:<commit>:<path>#<section> key. They are not already reconciled. Obligations, results, evidence, and reviewed application edges remain distinct; the application file still lacks a canonical claim-ID crosswalk.
- Enumerate theorem-like public declarations reachable through the compiled D0.All import as candidates. Public helpers, generated declarations, definitions, and instances must be classified; inclusion in an import closure alone does not make them reusable mathematical results.
- Bounded candidates from 04_CERTIFICATES/ and 05_EXPERIMENTS/ are exact computations, certificates, constructions, and negative controls found on cited or otherwise in-scope paths. A missing mathematical-consumer edge is a reconciliation gap, not an exclusion reason; exclude raw logs and exploratory runs without a mathematical assertion.
- The assembly attempts (4), anti_substitutions (25), synthesis (8), and source_fork_reconciliations (1 record pointing to two child PRs and four result IDs) are retrieval, provenance, and countercontrol inputs. They inform unit resolution and expose crosswalk gaps, but do not become extra result units merely by being indexed.
- Bound the original raw response terminal to its exact existing contract key: consumer RAW-216 → obligation raw_response_terminal → interface raw-216-v1. Preserve the complete interface: carrier = original fixed smooth Q_h with genuine Lorentz quotient and independently fixed smooth τ; action = original designated geometric Euler response and declared source equations; variations = exact joint connection and metric source equations; source = original #216 comparator Xi(Q_h,K_h)=h²τ(hx); normalization = h⁻² times the unweighted raw ℓ1 sum over h⁻⁴ sites; refinement = exact samples of the same g and τ on a refining sequence in the admitted log chart; scope = original response terminal. The exact owner source path/blob/slice is not yet pinned and remains a freeze blocker. Preserve its quantifiers and owner; do not import the whole historical corpus or claim this architecture closes the terminal.
- Include unrepresented book assertions and published research explicitly cited by books, active registry, assembly, and selected current GR sources. Key each by exact source commit/path/section or equation. For #334, the task-pinned slice gate is now read and pinned: published commit fe5cf335da04cac14e50407b03f98b96be17dc52, path 02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md, blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62; read §§8.4–8.5, equations (26)–(31), and §6.25, equations (13br1)–(13br2). Its concrete consumer is pinned in the same published snapshot: 02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md, blob 734e21ae6bc04ff3446ad15858936d417fdd2e55, §5.1. That application uses the recovered geometry to evaluate the existing star density from Julia queries and transfer its finite cubic response, conditional on the stated addressed-access, work-return, and strict-chart assumptions. This is not evidence of physical admission or mandatory price selection. The reusable mathematical scope is reconstruction of the typed native Julia raising-operator geometry on the stated charts and its full tangent pullback; it does not identify the reconstructed geometric functional with the native physical price/source or accept/retire #334.

Book/section pairs are not unique units: 49 pairs contain 192 claims. Multiple theorem strings and repeated theorem atoms are review flags, not automatic merges. The starting snapshot has 715 claim rows with a Lean module, 713 with a theorem string, and 360 with semicolon-separated theorem names. The new bulk locator pass currently exposes 889 claim rows, 2700 theorem-atom mappings, 4974 unique candidate Lean names, and 176 rows without a theorem locator; exact-name resolution against the elaborated D0.All environment is still pending. An independent scope review found 174 rows without a module, 176 without a theorem string, and 23 theorem atoms shared across IDs. These are reconciliation queues, not automatic proof debts or exclusions.

The freeze must bind exact source hashes, a reproducible unit list and classification, stable source keys, dispositions, exclusions and reasons, overlap/alias resolutions, public-declaration dispositions, and result-to-claim/source/application crosswalks. An independent reviewer must accept that exact package before coverage is reported. New research after freeze is a delta; do not alter C0 to improve a percentage.
## Scientific boundary and reuse vertical

This work does not select a physical implementation or close GR. Keep complete Book03/Cost-Info/source admission, same-execution clock/controller/work selection, physical metric descent/frame selection, original H+J+R, positive_gr, and raw216 open under their existing owners. Preserve #334; do not duplicate or retire its science. Conditional assumptions remain in theorem signatures. Connes reconstruction remains conditional when its needed object is a supplied field.

A useful cold-start reuse case is the native raising-operator inverse with a null leg: published #334 labelled-record source §§8.4-8.5, equations (26)-(31), with rational alternative §6.25 (13br1)-(13br2). Its selected source gate is satisfied at commit fe5cf335da04cac14e50407b03f98b96be17dc52, path 02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md, blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62. The concrete consumer is the exact AF radial coframe equivalence source §5.1, blob 734e21ae6bc04ff3446ad15858936d417fdd2e55. The new compiled module `D0.Geometry.ArchiveJuliaRaisingOperatorReadout` applies the existing vacuum-fix and creator-on-vacuum lemmas to recover `u` exactly with `ιInv`, and proves that equality of full model query operators implies equality of their shifts. The formalized scope is the finite-carrier vacuum identity in Eq. (26). It does not prove the full Lorentz null inverse (28), its all-jet extension, coframe/metric recovery, or the full variational pullback in (31). It supplies no physical price, compiler, admission, or GR selection result; the fuller consumer remains conditional on its stated assumptions.

## Implemented and remaining

The task branch replaces the Windows-incompatible fcntl import and truncating lock-file open in tools/lean_task_build.py with non-blocking POSIX flock or Windows CRT byte-range locking over a persistent one-byte file. The source digest and Lake invocation remain serialized. tools/test_lean_task_build.py passed on native Windows/Python 3.11: its cross-process test verified exclusion, release, reacquisition, and byte preservation. This verifies locking only.

The first narrow build `D0.Foundation.VerificationCore` completed successfully (2,968 build jobs). The subsequent narrow build `D0.Geometry.ArchiveJuliaRaisingOperatorReadout` also completed successfully (3,014 build jobs); no errors occurred in the new module. Existing linter warnings in imported modules remain with their owners. The collector's initial compile exposed an unqualified `Lean.Meta.forallTelescope`, which is now opened explicitly; its smoke run then returned the actual elaborated declarations and source metadata. The source digest was also narrowed to project-owned Lean files after the first cold build showed that including checked-out `.lake` dependency sources made freshness checks unnecessarily expensive.

The focused Python retrieval/locking/declaration-collector suite passes 25 tests on the native Windows runtime. The cold-start runner finds every required source in 11/11 real scenarios (the ten mandated cases plus a separate verification-kernel/theory-transfer case outside the GR specialization); its additional exact-source impact control passes, for 12 measured checks. The source-impact control changes when the declared source changes and stays fixed when unrelated prose changes. These results measure navigation and source binding only; scope review remains manual. `why verification_core` preserves its three explicit representation hypotheses and reports a complete name-level hypothesis map to the accepted `TheoryTransfer` application; this remains registry/application evidence, not a replacement for independent semantic acceptance. `show --lean D0.Geometry.archiveJuliaRaisingQuery_vacuum_exterior --import-root D0.Geometry.ArchiveJuliaRaisingOperatorReadout` resolves the compiled theorem, exact type, binder map, dependencies, transitive axioms, source module/range, source digest, and toolchain.

The existing `tools/test_gr_assembly.py` suite has 106/106 passing tests with a temporary Git `core.autocrlf=false` override. Its default native-Windows run reaches 15 errors and one secondary assertion failure because the fixture hashes a CRLF worktree `decisions.md` before Git stores the normalized blob; the resulting evidence digest differs from `git show`. The fixture is owned by open PR #398, so this branch records the environment-dependent result and leaves that file to its existing owner.

Next: extend the exact candidate inventory and source/declaration crosswalk, obtain independent acceptance of the exact C0 package, and review the Eq. (26) adapter against the pinned source and consumer. All ten required cold-start cases and the additional outside-GR case pass; migrate connected mathematical blocks while preserving public imports and scopes; formalize or obtain accepted owner review for every established C0 unit; then run affected integration and one current `D0.All` build on final sources. This checkpoint is not completion.

