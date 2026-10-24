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

`reuse --lean CLAIM-ID` joins one exact claims.csv row to its theorem-name candidates, declarations actually present in the selected compiled Lean import, and their reported proof dependencies. It also reports exact dependency-name intersections with other claim locators as candidate crosswalk edges. This compiled Lean evidence remains separate from declared assembly application edges, conceptual presuppositions, and semantic acceptance.

The read-only `tools/proof_architecture.py` view composes current claims, registered assumptions, formal-support locators, aliases, assembly contracts/results/applications/attempts, conceptual presupposition edges, and bounded full-text candidates. Claims expose their registered assumption rows separately from applications and conceptual edges. Commands are `search`, `show`, `why`, `reuse`, and `impact`; `show NAME --lean --import-root MODULE` calls the elaborated declaration collector. Every answer includes source digests and a snapshot commit. Conceptual edges, assumption links, alias lookup, text matches, declared application edges, and elaborated Lean facts are distinct output kinds. `why` reports unknown hypotheses separately from explicitly empty declarations and distinguishes unmapped hypotheses, unknown targets, and invalid map entries. `impact KEY` follows only currently declared evidence/application refs; `impact --base REF` delegates to the existing assembly diff impact. Neither form claims a complete global semantic impact graph.

Exact GitHub `blob/<commit>/<path>` links are now resolvable when their commit objects are already present in the local repository: the search derives the blob from `commit:path`, reads it, and returns the derived blob with direct line/section evidence. Explicit commit/path/blob references are checked against the expected blob. Git lazy fetching is disabled for this lookup, so unavailable external commits remain citation-only rather than causing a network fetch. The caller distinguishes a direct pinned source from a path mention and from a local filename match.

## C0 candidate boundary

### Pinned #334 raising-inverse retrieval key

For the direct query `Перенос и тетрада восстанавливаются из самого native raising operator`, use §8.4 of `02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, published commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`. For the all-jet query, §8.5 states that the full tangent space retains all 16 coframe and 24 link directions on a node, including observer jets, beyond only null/pp-wave-ansatz variations. The pin covers the owner content only; the §5.1 AF radial coframe consumer has its separate exact pin below.

C0 is a reviewed set of mathematical units, not files, modules, registry rows, or graph nodes. The figures below describe candidate inputs only; they are not a frozen denominator and no coverage percentage is valid before independent acceptance of the exact package.

Initial candidate sources and crosswalk inputs:

- The 889 claims.csv IDs are claim candidates keyed initially by claim ID and exact book/section locator. Each may split, overlap, or need a source-backed disposition before becoming one unit.
- The 31 assumption IDs are premise crosswalk inputs. Preserve the actual quantified hypotheses on results; do not count an assumption row as a result by default.
- The 180 formal_support.csv rows are proof-support crosswalk inputs and candidate declaration locators, not 180 independently accepted results.
- The 58 aliases are lookup edges: resolve the two canonical-target aliases and inspect the 56 legacy first_reference values for missing assertions.
- The 54 assembly result pointers still require reconciliation to a claim or exact source:<commit>:<path>#<section> key. They are not already reconciled. Obligations, results, evidence, and reviewed application edges remain distinct; the application file still lacks a canonical claim-ID crosswalk.
- Enumerate theorem-like public declarations reachable through the compiled D0.All import as candidates. Public helpers, generated declarations, definitions, and instances must be classified; inclusion in an import closure alone does not make them reusable mathematical results.
- Bounded candidates from 04_CERTIFICATES/ and 05_EXPERIMENTS/ are exact computations, certificates, constructions, and negative controls found on cited or otherwise in-scope paths. A missing mathematical-consumer edge is a reconciliation gap, not an exclusion reason; exclude raw logs and exploratory runs without a mathematical assertion.
- The assembly attempts (4), anti_substitutions (25), synthesis (8), and source_fork_reconciliations (1 record pointing to two child PRs and four result IDs) are retrieval, provenance, and countercontrol inputs. They inform unit resolution and expose crosswalk gaps, but do not become extra result units merely by being indexed.
- Bound the original raw response terminal to its exact existing contract key: consumer RAW-216 → obligation raw_response_terminal → interface raw-216-v1. Preserve the complete interface: carrier = original fixed smooth Q_h with genuine Lorentz quotient and independently fixed smooth τ; action = original designated geometric Euler response and declared source equations; variations = exact joint connection and metric source equations; source = original #216 comparator Xi(Q_h,K_h)=h²τ(hx); normalization = h⁻² times the unweighted raw ℓ1 sum over h⁻⁴ sites; refinement = exact samples of the same g and τ on a refining sequence in the admitted log chart; scope = original response terminal. The exact owner source path/blob/slice is not yet pinned and remains a freeze blocker. Preserve its quantifiers and owner; do not import the whole historical corpus or claim this architecture closes the terminal.
- Include unrepresented book assertions and published research explicitly cited by books, active registry, assembly, and selected current GR sources. Key each by exact source commit/path/section or equation. For #334, the task-pinned slice gate is now read and pinned: published commit fe5cf335da04cac14e50407b03f98b96be17dc52, path 02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md, blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62; read §§8.4–8.5, equations (26)–(31), and §6.25, equations (13br1)–(13br2). The owner states `DR DΦ=I` on its full tangent space and preserves all 16 coframe and 24 proper-Lorentz link directions, with observer jets retained when the observer changes; it explicitly exceeds null/pp-wave-ansatz variations. По-русски: полный касательный срез содержит все 16 направлений кофрейма и 24 proper-Lorentz link-направления; jets наблюдателя сохраняются при его изменении, а вариации не ограничены null/pp-wave ansatz. Its concrete consumer is pinned in the same published snapshot: 02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md, blob 734e21ae6bc04ff3446ad15858936d417fdd2e55, §5.1. That application uses the recovered geometry to evaluate the existing star density from Julia queries and transfer its finite cubic response, conditional on the stated addressed-access, work-return, and strict-chart assumptions. This is not evidence of physical admission or mandatory price selection. The reusable mathematical scope is reconstruction of the typed native Julia raising-operator geometry on the stated charts and its full tangent pullback; it does not identify the reconstructed geometric functional with the native physical price/source or accept/retire #334.

Book/section pairs are not unique units: 49 pairs contain 192 claims. Multiple theorem strings and repeated theorem atoms are review flags, not automatic merges. The starting snapshot has 715 claim rows with a Lean module, 713 with a theorem string, and 360 with semicolon-separated theorem names. The bulk locator inventory contains 889 claim rows, 2,702 theorem-atom mappings, 5,487 unique candidate Lean names, and 176 rows without a theorem locator. Exact-name resolution against the elaborated `D0.All` environment is complete for the pinned snapshot recorded below. An independent scope review found 174 rows without a module, 176 without a theorem string, and 23 theorem atoms shared across IDs. Source-unit reconciliation, semantic review, and independent C0 acceptance remain open; these queues are not automatic proof debts or exclusions.

The freeze must bind exact source hashes, a reproducible unit list and classification, stable source keys, dispositions, exclusions and reasons, overlap/alias resolutions, public-declaration dispositions, and result-to-claim/source/application crosswalks. An independent reviewer must accept that exact package before coverage is reported. New research after freeze is a delta; do not alter C0 to improve a percentage.

The existing structural `formalization_debt_audit.py` was replayed on this
snapshot: 918 Lean modules and 148,617 source lines, with only its three
baseline heartbeat-override findings and no proof holes, self/umbrella imports,
duplicate imports, missing local imports, or import cycles. This is a library
structure check, not a classification of the mathematical units above and not
evidence that C0 is formally covered.
## Scientific boundary and reuse vertical

This work does not select a physical implementation or close GR. Keep complete Book03/Cost-Info/source admission, same-execution clock/controller/work selection, physical metric descent/frame selection, original H+J+R, positive_gr, and raw216 open under their existing owners. Preserve #334; do not duplicate or retire its science. Conditional assumptions remain in theorem signatures. Connes reconstruction remains conditional when its needed object is a supplied field.

A useful cold-start reuse case is the native raising-operator inverse with a null leg: published #334 labelled-record source §§8.4-8.5, equations (26)-(31), with rational alternative §6.25 (13br1)-(13br2). Its selected source gate is satisfied at commit fe5cf335da04cac14e50407b03f98b96be17dc52, path 02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md, blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62. The concrete consumer is the exact AF radial coframe equivalence source §5.1, blob 734e21ae6bc04ff3446ad15858936d417fdd2e55. In `D0.Geometry.ArchiveJuliaRaisingOperatorReadout`, the exterior model has an exact vacuum readout, and a compiled adapter now builds its vector creator from the owned Jordan--Wigner `carCreateEnd` matrices. It proves `carCreateEnd r |0⟩` is the corresponding one-particle state, that the CAR and exterior queries have the same vacuum response, and that the CAR-query vacuum readout returns `u`; equality of complete CAR query operators therefore implies equal shifts. This supplies a concrete source-to-existing-operator application for the vacuum identity in Eq. (26), accounting for the repository's four-mode role basis and real coefficients. It does not prove equality of the two query operators on arbitrary 16-state inputs, the full Lorentz null inverse (28), its all-jet extension, coframe/metric recovery, or the full variational pullback in (31). It supplies no physical price, compiler, admission, or GR selection result; the fuller consumer remains conditional on its stated assumptions.

At this earlier checkpoint, the added adapter and readout corollaries passed `lake build D0.Geometry.ArchiveJuliaRaisingOperatorReadout` at Lean 4.30.0 (3,014 Lake jobs), while the full `D0.All` replay after those additions was still pending. The current integrated replay and its exact source digest are recorded in the 24 October checkpoint below.

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
lines 119–129 of the new module. The final `D0.All` replay for the later
24 October Lean source tree is recorded below; this earlier collector snapshot
and its digest remain historical provenance.

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

An independent read-only scope review at snapshot
`709ea27c3e7dc6865708aac076e4230655ad0cce` accepts one claim-to-book-to-Lean
correspondence: `D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001`. The exact source
blobs are `fc24227434bc917fa40ec880e9caff9b6b6b07b4`
(`02_REGISTRY/claims.csv`), `87f3dbd0e5e760d46a577a275aabc16623d3f09e`
(`01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md`, §01.8.1),
`79ad345ddef6bb06c638f41721db1a84843e4a9b`
(`01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md`, §02.34),
and `eaf1094cdb86260afcac2d9279ef0c2b46f15bc8`
(`03_FORMALIZATION/D0/Synthesis/TopHodgeInverseSpectralRigidity.lean`,
`topHodge_inverse_spectral_rigidity`). The reviewed match is equality of the
three actual top-Hodge coordinates implying equality of unordered positive
zone-size multisets, for the canonical positive complete-tripartite class.
This is one scoped correspondence review only: it does not accept C0
membership for neighboring assertions, establish coverage, extend the theorem
to arbitrary finite complexes, or record approval from the scientific owner.

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

Next: reconcile the exact-name inventory with source-keyed mathematical units and dispositions, obtain independent acceptance of the exact C0 package, and obtain independent review of the Eq. (26) adapter against the pinned source and consumer. The 24 October checkpoints below record the refreshed 13-case cold-start suite, compiled claim-reuse examples, shared Vieta migration, and current `D0.All` build. Migrate connected mathematical blocks while preserving public imports and scopes; formalize or obtain accepted owner review for every established C0 unit. This checkpoint is not completion.

## Concrete reuse application: top-Hodge scene

The generic theorem `D0.Synthesis.TopHodgeInverseSpectralRigidity.topHodge_inverse_spectral_rigidity` is now consumed by a separately named compiled application, `scene_topHodge_inverse_spectral_rigidity_application`. For any natural-number reduced zone sizes whose actual top-Hodge coordinates are `(D,H,M₂)=(1287,960,50193)`, the application concludes `{p+1,q+1,r+1}={9,11,13}`. It obtains those reference coordinates from `scene_topHodge_spectral_coordinates`, then invokes the generic theorem; the elaborated proof dependencies contain both declarations. The older scene-specific reconstruction remains available as a second proof route.

This adds the application theorem to the existing `D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001` theorem locator list and regenerates `TheoremLedger/ClaimMap.lean`; it creates no claim ID or acceptance status. The source/declaration correspondence reviewed independently at PR head `709ea27c3e7dc6865708aac076e4230655ad0cce` covered only the generic theorem before this application was added. The new application itself has not received independent semantic review and does not enlarge that review or the generic theorem's positive complete-tripartite scope.

Validation on the current dirty worktree: narrow `D0.Synthesis.TopHodgeInverseSpectralRigidity` build passed at Lean 4.30.0 (2,993 Lake jobs). The compiled declaration inventory resolved the new theorem under that public import with binders `p q r`, the three numeric-coordinate hypotheses, conclusion `{p+1,q+1,r+1}={9,11,13}`, and transitive axioms `Classical.choice`, `Quot.sound`, and `propext`. Inventory provenance: parent snapshot `709ea27c3e7dc6865708aac076e4230655ad0cce`, dirty Lean source digest `87ca08a0fbef5dfca4b61134d55f5e08cfac3928b86e9682ebafda895667a2bf`, collector SHA-256 `550a3d4cda78902a0a7a35b220160e524347aa0cad9a3e6f8082473d7a675f27`. `generate_lean_views.py --check` passed, and the exact-name search returned the claim locator plus direct Lean source content. A concurrent `show --lean` request was correctly rejected while the inventory held the Lake lock; it was rerun after the lock was released and completed against the same compiled public import.

## Top-Hodge application crosswalk repair

Independent review of the application at PR head `7b2f4cac3a6904f5d5a44e94279b103bcbf18499` accepts the compiled proof-level application and confirms that it consumes both the generic inverse-rigidity theorem and the actual scene-coordinate theorem. The reviewer identified that the application had not been listed under the existing scene-reconstruction claim. The fully qualified declaration `D0.Synthesis.TopHodgeInverseSpectralRigidity.scene_topHodge_inverse_spectral_rigidity_application` is now listed in the existing `lean_theorem` locator fields for both the scene-reconstruction claim and the generic inverse-rigidity claim. The generated ClaimMap includes the same locator for both. This uses existing authorities, adds no claim ID or acceptance status, and leaves the old scene-specific reconstruction theorem as a separate route.

Claim-targeted declaration inventories for both claim IDs resolve the fully qualified locator to the same elaborated declaration under public import `D0.Synthesis.TopHodgeInverseSpectralRigidity`. At snapshot `7b2f4cac3a6904f5d5a44e94279b103bcbf18499`, the final metadata and generated ClaimMap produce Lean source digest `dd056ebca233774b20e628d8b7efd3f94e344b18d0fa07e8abf973e229e1857d` and collector SHA-256 `600e569e2f522c9f617eb82d52dccf14a761dbde372ef83a5a6ca9aaef6ad854`. The inventory reports binders `p q r`, coordinate hypotheses `D=1287`, `H=960`, and `M₂=50193`, conclusion `{p+1,q+1,r+1}={9,11,13}`, and proof dependencies on `topHodge_inverse_spectral_rigidity` and `scene_topHodge_spectral_coordinates`; it does not depend on `reconstruct_scene_unordered_from_topHodge_spectral_data`. The theorem source is unchanged from the reviewed source digest `87ca08a0fbef5dfca4b61134d55e5f08cfac3928b86e9682ebafda895667a2bf`; the project digest changed because the generated ClaimMap is included in the digest. Independent review accepts this bounded machine-resolvable locator crosswalk, with the limit that the current `lean_theorem` schema records locators, not a typed `application_of` edge. Neither the scene claim as a whole nor C0 has been accepted by this checkpoint.

At the first locator-update checkpoint, `generate_lean_views.py` regenerated `TheoremLedger/ClaimMap.lean`, and `generate_lean_views.py --check`, `formalization_debt_audit.py --check`, the proof-architecture tests (21), declaration-inventory tests (8), and Lean-build-tool tests (3) passed. The all-claims declaration-resolution run is now complete below. The exact C0 candidate freeze, independent C0 package acceptance, and remaining established C0 unit migration/review are still open.

## Broad exact declaration-locator resolution

The all-claims request contains 5,487 unique candidate names and 5,575 candidate references across 889 rows and 2,702 theorem atoms in `claims.csv`. Deep signature, proof-dependency, and axiom traversal remains available for selected results. The new `tools/lean_declaration_inventory.py --resolution-only` mode reports exact name existence, owning Lean module, and source path while building the selected public import and checking the Lean-source digest. It omits signature, dependency, range, and axiom details. The JSON records `resolution_only: true`.

The initial broad collector exposed Lean's code-generator recursion limit when one command embedded all candidate names in one array. The collector now emits bounded batches of 128 names as independent `run_cmd` blocks. A 257-name live Lean query passed and returned 257 exact misses as expected; the focused unit suite checks the 128/128/1 split. A completeness check then exposed 213 malformed candidates caused by semicolon-separated `lean_module` locators being treated as one module. Candidate generation now expands each module locator separately and retains the `D0.` fallback. The collector also rejects any response whose Lean-rendered name fails an exact round trip to its requested candidate; a regression test covers that failure mode. The completed inventory has zero requested candidates missing from its response and zero unexpected response names. The default selected-declaration mode still emits full types, dependencies, ranges, and axiom details.

The completed `--all-claims --resolution-only` run built and imported `D0.All` at Lean 4.30.0 and resolved all 5,487 unique candidates. It found 1,823 declarations and 3,664 misses; all found declarations mapped to a source path. Of the 2,526 theorem atoms with candidate names, 1,858 had at least one declaration in the compiled public environment. This includes 471 of 889 claim rows with at least one available locator; 176 theorem atoms had no candidate name to query. These are exact locator-resolution counts and carry no claim-semantic or C0-coverage judgment.

The complete machine-readable result is [claim_candidate_resolution.json](sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution.json), SHA-256 `C9D244C8D8B0FEA53B9056788981C3E8E16EF6401A7E788E827B704F2DC3AF1B`. The JSON records source snapshot `5c4f77c2fb440c8eb60133b41402d73183b2a92e`, the then-published PR tree `710cce783aa66c479505d95e2f9f841247ed2b73` at head `1701ec750376ba13058e3ea3c4f101c1462a958d`, Lean source digest `dd056ebca233774b20e628d8b7efd3f94e344b18d0fa07e8abf973e229e1857d`, collector SHA-256 `021841d09e9e2ba30eff014a4b2719dd83f4b28883f66081e6806e669efd5fd8`, and public import `D0.All`. Those local and published trees matched when the inventory ran. The subsequent artifact-only publication advanced the PR to `12eae2429289a8663bc3925ba2bdeeeb17d0585e` without changing its claims, inventory/build scripts, toolchain, Lake inputs, or `D0/All.lean`.

An independent locator-integrity review at PR head `12eae2429289a8663bc3925ba2bdeeeb17d0585e` recomputed all 2,702 claim/theorem mappings from the 889 source rows and confirmed exact agreement. It verified 5,575 references against 5,487 ordered unique response records, including all 25 semicolon-separated module rows; all 1,823 found declarations have valid module-derived paths across 426 source files. The reviewer reproduced the collector hash and Lean source digest and checked the 128-name maximum (43 batches, last batch 111). The reviewed snapshot is not an ancestor of the PR head, but all relevant source inputs and digests match. This accepts locator expansion, completeness, ordering, path integrity, and provenance only; it does not establish semantic claim coverage or C0 acceptance. C0 remains unfrozen and has no coverage denominator or acceptance.

At PR head `f2e2b54cb21ac1f20c2afa4e6cbc1e86313c1ed7`, GitHub `D0 guards` passed. The `D0 Lean build` workflow completed successfully as a Draft run, with `Build release proof closure` and `Compile native checkpoint capsules` skipped. The full local `lake build D0.All` succeeded against the recorded source snapshot; therefore the skipped Draft steps are not represented as GitHub release-closure validation.

## 24 October integrated retrieval and adapter checkpoint

The cold-start suite was replayed at local parent snapshot
`e58ef06572db3436f109359e8bd90d3cd5fbb4b9` (`worktree_dirty=true`) after
adding query-scoped exact-source checks and context-ranked source references.
The full 33-query run found every required source in 13/13 scenarios; the
14-case benchmark also passed, including the exact-source-versus-unrelated-
prose impact control. For the pinned #334 raising-inverse owner, all six
owner queries resolved the exact path/commit/blob, and the two all-tangent
queries exposed §8.5; the separate AF radial coframe consumer query resolved
its exact §5.1 pin. The search now rejects aggregate-only coverage when an
individual scoped query misses and no longer drops a late exact source pin
behind unrelated references. This verifies retrieval and provenance only,
not semantic C0 acceptance or physical selection.

The focused proof-architecture suite passes 24/24 tests. The generated-view
check (`generate_lean_views.py --check`), `check_no_sorry_in_core.py`, and
`check_claim_map_coverage.py` pass. One initial full `D0.All` attempt exposed
an auto-generated `LinearOrder Role` declaration collision between the new
raising-readout module and `A4DObserverPositiveExterior`; giving the new
module's local instance a unique name removed the integration conflict. The
narrow raising-readout build then passed (3,014 Lake jobs), followed by the
final current-source `D0.All` build (4,563 jobs, Lean 4.30.0). Existing
imported-module linter warnings remain with their owners.

Build provenance: local snapshot `e58ef06572db3436f109359e8bd90d3cd5fbb4b9`,
dirty worktree; project-owned Lean source digest
`f806ee18e9f9333b6c92db25c579f5843f066da1df1830e1a6ae18730ebd58ba`, matching
the final-build stamp; build helper SHA-256
`255bd49a5211154683a698b1163bcebcaeb52b2fd125fbc0590d73d696ee3104`. The
compiled raising-readout source SHA-256 is
`c968312ac93f8230fd3b400279e1dce9b4e030ade5444c8d7816fc1b1fec048a`. The
search and authority inputs are pinned by these SHA-256 digests:

| Input | SHA-256 |
|---|---|
| `tools/proof_architecture.py` | `234c428bf9b98b6adb10b16204718f91e4f6e3ae2258379587c36c3a64359c6b` |
| `tools/proof_architecture_cold_start.py` | `00b8f483601c36ba3d548afca0752c9d6760db930a01dcdab4aa273b4c047d48` |
| `tools/test_proof_architecture.py` | `b5efb2321910f52b549578fd55579b7a4a89e79341aa1c64801f1d1bb53560ad` |
| `02_REGISTRY/claims.csv` | `fcc9c0b2b4a010ec3c7cf8a1a0d883a0f445320e6588f0c3e4f775dd787ad222` |
| `02_REGISTRY/assumptions.csv` | `2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36` |
| `02_REGISTRY/formal_support.csv` | `2891e51611f95df046adf132c165822d9156666b6dae44703830e7c5b72a3d42` |
| `02_REGISTRY/aliases.csv` | `8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f` |
| `02_REGISTRY/gr_assembly/applications.json` | `a493c0161b2f39ec14925e38131f7c2d240cd07bd2e27404a35098bc96eb0dc8` |
| `02_REGISTRY/gr_assembly/contract.json` | `72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6` |
| `02_REGISTRY/presupposition_edges.json` | `9740e8192f65f674f4d82013e526cf9d8524d2d74d75eed749f48dcf43bef5c1` |

The `D0.All` result is local validation of this dirty source tree; it does not
stand for the skipped GitHub Draft release-closure or capsule jobs. #334
remains the scientific owner. The CAR adapter is a finite vacuum-response
application and does not prove equality on arbitrary 16-state inputs, the
full all-jet Lorentz inverse or its complete variational pullback. Independent
C0 acceptance and the native physical Book/Cost-Info/clock/controller/source
selection premises remain open under their existing owners.

## 24 October compiled claim-reuse view

The new `reuse --lean` path was run through the CLI on
`D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001` using public import `D0.All`.
All 11 exact theorem-name atoms in that claim row resolved to declarations in
the compiled environment. The view finds the concrete application
`D0.Synthesis.TopHodgeInverseSpectralRigidity.scene_topHodge_inverse_spectral_rigidity_application`
in `03_FORMALIZATION/D0/Synthesis/TopHodgeInverseSpectralRigidity.lean`; its
reduced conclusion is `{p + 1, q + 1, r + 1} = {9, 11, 13}`. Its compiled
proof dependencies include the generic
`topHodge_inverse_spectral_rigidity` result and the scene's
`scene_topHodge_spectral_coordinates` and coordinate declarations. The exact
dependency-to-locator join shows the application declaration consuming the
generic result locator. The scene-coordinate declaration is visible as a
compiled dependency but currently has no exact theorem locator in claims.csv.

For this claim, the separate declared assembly-application list is empty. The
view therefore records typed Lean proof dependencies and candidate claim
locator crosswalks without inventing an assembly application edge or semantic
claim acceptance. It creates no claim ID, status, or scientific owner.

The current 33-query cold-start rerun still passes all 13/13 scenarios and the
14-case source-impact benchmark. The focused proof-architecture suite passes
26/26 tests, including a negative control that an assembly application key
retains its metadata route without entering the claim-locator Lean join. The
claim-reuse CLI run used Lean source digest
`f806ee18e9f9333b6c92db25c579f5843f066da1df1830e1a6ae18730ebd58ba` and
collector SHA-256
`0b80b2f838d2e1607d2bb93596e239802fe66edad23fbd3b0e269637b4a69881`; current
tool digests are:

| Input | SHA-256 |
|---|---|
| `tools/proof_architecture.py` | `d0e92e3b42e99562a151a41baad18c6569148c3195298002d213d11d96fbae71` |
| `tools/proof_architecture_cold_start.py` | `00b8f483601c36ba3d548afca0752c9d6760db930a01dcdab4aa273b4c047d48` |
| `tools/test_proof_architecture.py` | `ff77f330082786867e84d0100819d6e1175f7c41901df73651e8e3ff25841029` |

This is an exact compilation and name-crosswalk example on a finite
mathematical result. It neither closes the full D0 proof corpus nor changes the
unresolved physical premises, C0 acceptance boundary, or #334 ownership.

### 24 October shared tripartite Vieta layer and compiled applications

- The rational tripartite invariants and Vieta/root-multiset proof now have a
  lower-level owner in `D0.Combinatorics.TripartiteVieta`. The normalized
  quotient module keeps its previous `tripartiteV`, `tripartiteE` and
  `tripartiteT` names as abbreviations. The inverse-spectral module preserves
  its existing `zoneRootPolynomial_*` and `unordered_*` theorem locators as
  compatibility wrappers.
- `reconstruct_scene_unordered_from_topHodge_spectral_data` now derives the
  triangle, vertex and edge invariants from its actual top-Hodge inputs
  `(D,H,M₂)`, then applies the shared unordered Vieta theorem. The existing
  finite sum/product classification remains available under its old names;
  this capstone no longer depends on that separate enumeration route.
- The shared invariant formula lemmas are exposed as global `[simp]` rules
  through imports. This intentional simplifier-environment change keeps the
  old transparent abbreviations reducible in downstream normalized-spectrum
  proofs; the complete `D0.All` build checks those consumers.
- Argument phase: formalization and library migration of an existing finite
  mathematical result. Parent substitution: the scene capstone's unordered
  reconstruction now consumes the shared `V,E,T` root theorem. Its stated
  assumptions remain the canonical complete-tripartite class and equalities
  for the actual `D,H,M₂` data.
- The compiled `reuse --lean` view resolves all 11/11 exact locators for
  `D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001` and all 7/7 for
  `D0-TOP-HODGE-SPECTRAL-SCENE-RECONSTRUCTION-001`. The compiled scene
  application lists dependencies on the shared rational `V`, `E`, `T`,
  `unordered_nat_triple_eq_of_VET_eq`, and the existing Hodge edge-count
  identity. The inverse-spectral application has compiled dependency joins to
  its generic rigidity theorem and to the scene's actual multiplicity and
  second-moment declarations. These remain candidate locator crosswalks; the
  claim text and scientific status are unchanged.
- Validation on local `HEAD=e58ef06572db3436f109359e8bd90d3cd5fbb4b9`
  (`worktree_dirty=true`): narrow builds of
  `D0.Synthesis.TopHodgeSpectralSceneReconstruction` (2,984 jobs) and
  `D0.Synthesis.TopHodgeInverseSpectralRigidity` (2,994 jobs); final
  `D0.All` build (4,564 jobs); proof-architecture tests 26/26; generated Lean
  views, no-sorry-in-core and claim-map coverage checks passed; `git diff
  --check` passed. The initial narrow integration exposed transparent-alias
  simplification gaps; adding the shared invariant formula simp lemmas restored
  the downstream normalized-spectrum proofs before the successful builds.
- Build and compiled-reuse provenance: Lean 4.30.0, public import `D0.All`,
  Lean source digest `bb5b03d60eb57ee1cafff2223af6fa695413dc410c57dbc9f88f557934195386`,
  equal to the final-build stamp. The inverse-claim collector SHA-256 is
  `0b80b2f838d2e1607d2bb93596e239802fe66edad23fbd3b0e269637b4a69881`; the
  scene-claim collector SHA-256 is
  `7950c99a15f0937b21f0cdc80cab0434cea08ddfbd89b9c3cae6f6602eb76dea`.
  Source SHA-256 values:

  | Input | SHA-256 |
  |---|---|
  | `03_FORMALIZATION/D0/Combinatorics/TripartiteVieta.lean` | `507d015725394d9c5b1b9df822f6169a0cae25ab6e6fd6057ea5af8cb6dc65e5` |
  | `03_FORMALIZATION/D0/Synthesis/TopHodgeSpectralSceneReconstruction.lean` | `813454ca03e9ed54f3690d9916edf8916350d6db51f7fe64fae6b441a0ebc349` |
  | `03_FORMALIZATION/D0/Synthesis/TopHodgeNormalizedQuotientSpectrum.lean` | `a94c832a5bfedd5c510024f30188b8f3f3ba6b08e567327c6cf2421c5da664bf` |
  | `03_FORMALIZATION/D0/Synthesis/TopHodgeInverseSpectralRigidity.lean` | `419f2419e6bae0fbeaf0cd498815f5bce5ddbd70c65ff34499f49d7fd198a9ca` |
  | `03_FORMALIZATION/D0/All.lean` | `0a584418ecd94624690eb572c4e2a9051e4afd9d9d91bad3158a318134ac170a` |
  | `02_REGISTRY/formal_support.csv` | `d635f0a0b9c616ec38fd8e7e550ae282e9f7ab0c6953f6db29a922b123df80d2` |
  | `tools/lean_task_build.py` | `255bd49a5211154683a698b1163bcebcaeb52b2fd125fbc0590d73d696ee3104` |

- Independent read-only review: scoped PASS for the generic rational Vieta
  theorem, natural-number specialization, scene reconstruction application,
  preserved public locators, and acyclic imports. It noted the global `[simp]`
  effect above and found no correctness blocker. This review does not accept
  C0, close a physical premise, or alter the scope of #334.

This checkpoint covers a finite algebraic library migration and two compiled
uses; it makes no corpus-wide C0 coverage claim. C0 remains unfrozen and
independently unaccepted. #334, its physical source/admission owners, and the
open GR selection premises retain their existing scope and ownership.
