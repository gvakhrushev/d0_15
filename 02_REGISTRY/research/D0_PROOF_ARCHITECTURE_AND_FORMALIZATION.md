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

The declaration extractor queries a selected compiled public import (`D0.All` by default) and records full name, raw elaborated type, the telescope binders with weak-head-normalized type/implicitness/proposition status, the weak-head-normalized conclusion after opening the binders, type/proof dependencies, transitive axiom footprint, source declaration range/module, snapshot, toolchain, and public import path. Raw type and reduced conclusion are retained together so an ordinary definition alias cannot hide a trivial status proposition or erase an actual premise from the displayed conclusion. Before extraction it asks Lake to build the selected import root under the same shared lock; the source digest is checked across both build and query, so an old `.olean` cannot be reported against current project source. The digest includes repository-owned Lean files and the Lake configuration with line endings normalized, while `.lake` package checkouts are excluded and pinned through `lake-manifest.json`. `--all-claims` retains every current claims.csv row, including unresolved theorem locators, and batch-resolves exact candidates in one imported environment; this produces a reproducible crosswalk candidate, not semantic coverage. This is exact elaborated evidence, not a normalized semantic equivalence proof. A reviewer binds that type to the source claim's object, domain, quantifiers, and assumptions. Load-bearing applications need compiled Lean adapters over actual objects and maps; a field that assumes the desired conclusion is not an adapter.

The collector has run successfully on `D0.Foundation.VerificationCore.verification_core` and the new `D0.Geometry.archiveJuliaRaisingQuery_vacuum_exterior`. Both are found in the compiled environment with actual types, binders, proof/type dependencies, source ranges, and axiom footprints. The verification theorem retains its quantified `FutureExecution` and `TheoryVerification` inputs and is located at lines 227–240 of its source. The Eq. (26) model theorem is located at lines 50–57 of `ArchiveJuliaRaisingOperatorReadout.lean`; its exact type is `∀ u M, archiveFockExteriorEquiv (archiveJuliaRaisingQuery u M vacuum) = ι ℝ u`, with `u : RoleSpace` and `M : RoleSpace ≃ₗ[ℝ] RoleSpace`. The collector reports `Classical.choice`, `Quot.sound`, and `propext` for both this theorem and its existing creator-on-vacuum lemma. These are exposed dependencies of the existing finite-carrier representation; this checkpoint does not claim an axiom-free kernel. The Eq. (26) inventory result was captured at HEAD `b2b73963991bb18c42766ae753bef1c70314c9ab` with `worktree_dirty=true`, Lean source digest `8993ecd144677720658cb3187ba737cb512b7c20a27d541ac93cc212b2b28f3f`, and collector script SHA-256 `4d4edc04deec3e2ad185e9fcf1ba3b7e63bfb16ba1fbc3d9905d253aa2d8ef11` under Lean 4.30.0.

Search is deterministic and bounded: exact IDs/names, aliases, sections, declared result/application links, and scoped attempts first. The content pass uses one `rg --json` scan to build query-specific concept hits, then reads evidence and follows pins only from its bounded top candidates. Russian/English concepts are grouped; low-information words are dropped from scoring when enough specific groups remain. Results include matched lines and nearest headings, with direct content, filename-only hits, and citations kept distinct. Ranking may suggest candidates but cannot set truth. Search failure is not nonexistence.

The read-only `tools/proof_architecture.py` view composes current claims, registered assumptions, formal-support locators, aliases, assembly contracts/results/applications/attempts, conceptual presupposition edges, and bounded full-text candidates. Claims expose their registered assumption rows separately from applications and conceptual edges. Commands are `search`, `show`, `why`, `reuse`, and `impact`; `show NAME --lean --import-root MODULE` calls the elaborated declaration collector. Every answer includes source digests and a snapshot commit. Conceptual edges, assumption links, alias lookup, text matches, declared application edges, and elaborated Lean facts are distinct output kinds. `why` reports unknown hypotheses separately from explicitly empty declarations and distinguishes unmapped hypotheses, unknown targets, and invalid map entries. `impact KEY` follows only currently declared evidence/application refs; `impact --base REF` delegates to the existing assembly diff impact. Neither form claims a complete global semantic impact graph.

Exact GitHub `blob/<commit>/<path>` links are now resolvable when their commit objects are already present in the local repository: the search derives the blob from `commit:path`, reads it, and returns the derived blob with direct line/section evidence. Explicit commit/path/blob references are checked against the expected blob. Git lazy fetching is disabled for this lookup, so unavailable external commits remain citation-only rather than causing a network fetch. The caller distinguishes a direct pinned source from a path mention and from a local filename match.

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

### Concrete foundation-to-transfer application

Added `D0.Foundation.VerificationTransferApplication` as a vertical use of the
owned `VerificationCore` and `TheoryTransfer` results. It constructs a concrete
two-line verification protocol whose state carrier is the exact visible-bit
empirical quotient, proves that the archive bit discarded by the existing
`visibleBitSystem` is future-indistinguishable, and transfers the actual false
profile readout through `visibleBitInterpretation` to its common native
execution. The module is registered in the existing `formal_support.csv` and
the generated public import list; it adds no claim, assumption, acceptance,
or assembly status row.

The same compiled slice consumes the existing hidden-bit lower-bound result to
rule out a decoder that stores only the current visible bit, and proves that
an interpretation with identity state map but an empty action translation
cannot commute with the admitted archive-revealing action. These finite
controls exercise the actual maps and hypotheses in the owned interfaces;
they do not claim a physical D0 implementation.

The new module builds narrowly under Lean 4.30.0. The generated-view check
passes and the focused proof-architecture, declaration-inventory, and build
lock suite passes 32/32 tests. The declaration collector reports the full
composed theorem
`D0.Foundation.VerificationTransferApplication.verified_visibleFalseReadout_transfers_to_common_execution`
with no binders and transitive axioms `Classical.choice`, `Quot.sound`, and
`propext`, reflecting the existing quotient representation. It starts from
the concrete represented state, passes through the owned verified-state/image
equivalence, and reaches the mapped common-sector profile. At snapshot
`65b4831f38eec190f81fcc9144d03f41985960a4`, the dirty-worktree Lean source
digest is `ece1f667d2ce2e474ea5f6e383b03067b8968eda4da739a34e40bfc5405b021e`,
the collector digest for this query is
`c447c2952e3893855d479a19a7a1de0aa037a20dd96d46cd6fbd38cbf598cde0`, and the
toolchain is `leanprover/lean4:v4.30.0`. The emitted declaration range is
lines 119–129 of the new module. A current `D0.All` build is still reserved
for the final integration run.

The same collector check on
`D0.Bridge.connes_reconstruction_conditional` reports the explicit binder
`h : D0.Bridge.BridgeAssumption.ConnesReconstruction`, whose reduced type is
`h.d0FiniteSpectralTriple ∧ h.metricEqualsSpectrum`, and no axioms. This
confirms that the conditional bridge remains conditional in the compiled
environment; it is not a discharged physical assumption. The query uses the
same dirty-worktree Lean source digest
`ece1f667d2ce2e474ea5f6e383b03067b8968eda4da739a34e40bfc5405b021e`.

The exact claim crosswalk was also run against its declared owner import.
`D0-LEAN-CORE-001` resolves to `D0.lean_core_release_candidate`; its raw type
is `D0.LeanCoreReleaseCandidate` and its reduced conclusion is
`D0.claimMap = [] → False`, a nonempty-generated-map status check. The
`D0-LEAN-BRIDGE-001` locator resolves to `D0.lean_bridge_assumptions_explicit`;
its raw type is `D0.BridgeAssumptionsExplicit` and its reduced conclusion is
`True`. Both are in `D0/TheoremLedger/ReleaseStatus.lean` at lines 26 and 31,
respectively, with no binders or axioms. The batch query used collector
SHA-256 `6339cdaaea69325cf514248294b2c4bde015dd550b29798d62ea67a46222f1ec`
and the same Lean source digest above. These declarations remain exact
registry locators but are not evidence that the mathematical core is fully
formalized or that bridge assumptions have been discharged. No claim, owner,
or status metadata changed.

The cold-start runner was replayed after the composed theorem and reduced-type
collector changes at snapshot
`65b4831f38eec190f81fcc9144d03f41985960a4` with `worktree_dirty=true` (28.7
seconds): all 11/11 original scenarios found their required sources as direct
content across 29 queries. The later expanded run at that same snapshot found
all required sources in 13/13 scenarios across 33 queries; this adds the
top-Hodge inverse theorem and dense finite-scene reconstruction outside the GR
branch. The 14-case benchmark passed, including the control that a declared
source edit changes its dependent result while unrelated prose does not. The
current `formal_support.csv` digest is
`2891e51611f95df046adf132c165822d9156666b6dae44703830e7c5b72a3d42`; the
other authority digests match the values listed for this branch below.

The same public CLI was used for the exact claim
`D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001`. Under its owner import, the
compiled `topHodge_inverse_spectral_rigidity` at lines 170–209 has six
implicit natural-number indices, exactly three proposition binders `hD`,
`hH`, `hM2` for the top-Hodge coordinates, and conclusion
`{p + 1, q + 1, r + 1} = {p' + 1, q' + 1, r' + 1}`. Its transitive axiom
footprint is `Classical.choice`, `Quot.sound`, and `propext`. The compiled
`topHodge_data_do_not_choose_zone_labels` control proves equal coordinates for
permuted `(1, 2, 3)` and `(2, 1, 3)` while their ordered triples differ;
`without_H_inverse_rigidity_fails` is an exact counterexample to dropping
the harmonic coordinate. This is a mathematical result for the encoded
positive complete-tripartite class; it does not choose zone labels or extend
to arbitrary complexes. The three-declaration inventory used collector
SHA-256 `09875ba336968932ac5f1f8f4d362092b5c7f7fbf66177d6c2f1d6c2c38876f0`
and the same Lean source digest above.

The task branch replaces the Windows-incompatible fcntl import and truncating lock-file open in tools/lean_task_build.py with non-blocking POSIX flock or Windows CRT byte-range locking over a persistent one-byte file. The source digest and Lake invocation remain serialized. tools/test_lean_task_build.py passed on native Windows/Python 3.11: its cross-process test verified exclusion, release, reacquisition, and byte preservation. This verifies locking only.

The first narrow build `D0.Foundation.VerificationCore` completed successfully (2,968 build jobs). The subsequent narrow build `D0.Geometry.ArchiveJuliaRaisingOperatorReadout` also completed successfully (3,014 build jobs); no errors occurred in the new module. Existing linter warnings in imported modules remain with their owners. The collector's initial compile exposed an unqualified `Lean.Meta.forallTelescope`, which is now opened explicitly; its smoke run then returned the actual elaborated declarations and source metadata. The source digest was also narrowed to project-owned Lean files after the first cold build showed that including checked-out `.lake` dependency sources made freshness checks unnecessarily expensive.

The current focused Python retrieval/locking/declaration-collector suites pass 32/32 tests on native Windows/Python 3.11. The 29-query cold-start run completed in 27.3 seconds and found direct content for all required sources in 11/11 scenarios; the additional exact-source impact control passed, for 12 measured checks. The source-impact control changes when the declared source changes and stays fixed when unrelated prose changes. On this run the exact #334 owner and consumer resolved at commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, blobs `1c8d59e5533b443d9a015dc4512cfbc160ae7e62` (§§8.4–8.5) and `734e21ae6bc04ff3446ad15858936d417fdd2e55` (§5.1); the fixedRIGHT source resolved at commit `4873b3c245a91bd8c9cb25bceeb82662e9f62944`, blob `6395c736c54d0c0a704d22ffdf046dbfc2c6c84b` (§5). These checks prove retrieval and exact source binding only; they do not independently accept the mathematical application or select physical price/source.

The search run used snapshot `1c7e39336381658fd2d7b17f2a077e5c2fec0817` with `worktree_dirty=true`. Its authority digests were: `claims.csv` `9c7a38e9016061dd76ac999f1039686c2c1d08a7e30355c70a635a1433e9358f`; `assumptions.csv` `2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`; `formal_support.csv` `5b5efbc1767bb5b910c53bf5da1eaa5ce44ff9255ff936bfb2b05f026393560d`; `aliases.csv` `8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`; `applications.json` `a493c0161b2f39ec14925e38131f7c2d240cd07bd2e27404a35098bc96eb0dc8`; `contract.json` `72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`; and `presupposition_edges.json` `9740e8192f65f674f4d82013e526cf9d8524d2d74d75eed749f48dcf43bef5c1`.

The existing `tools/test_gr_assembly.py` suite has 106/106 passing tests with a temporary Git `core.autocrlf=false` override. Its default native-Windows run reaches 15 errors and one secondary assertion failure because the fixture hashes a CRLF worktree `decisions.md` before Git stores the normalized blob; the resulting evidence digest differs from `git show`. The fixture is owned by open PR #398, so this branch records the environment-dependent result and leaves that file to its existing owner.

Next: extend the exact candidate inventory and source/declaration crosswalk, obtain independent acceptance of the exact C0 package, and review the Eq. (26) adapter against the pinned source and consumer. All ten required cold-start cases and the additional outside-GR case pass; migrate connected mathematical blocks while preserving public imports and scopes; formalize or obtain accepted owner review for every established C0 unit; then run affected integration and one current `D0.All` build on final sources. This checkpoint is not completion.
