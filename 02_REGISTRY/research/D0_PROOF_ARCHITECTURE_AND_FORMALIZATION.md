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

#334 remains an unmerged scientific owner. Its task-pinned published head is fe5cf335da04cac14e50407b03f98b96be17dc52. The selected raising-operator source and consumer slices below pass their source-pin/read gate; the finite Eq. (26) adapter has a scoped independent review recorded below. The full inverse, consumer transport, physical premises, and independent C0 acceptance remain open. Any additional #334 slice must record its published commit, path, blob, read proof, scope, and reviewed slice.

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

The declaration extractor queries a selected compiled public import (`D0.All` by default) and records full name, raw elaborated type, the telescope binders with weak-head-normalized type/implicitness/proposition status, the weak-head-normalized conclusion after opening the binders, type/proof dependencies, transitive axiom footprint, source declaration range/module, snapshot, toolchain, and public import path. Raw type and reduced conclusion are retained together so an ordinary definition alias cannot hide a trivial status proposition or erase an actual premise from the displayed conclusion. Before extraction it asks Lake to build the selected import root under the same shared lock; the source digest is checked across both build and query, so an old `.olean` cannot be reported against current project source. The digest includes repository-owned Lean files and the Lake configuration with line endings normalized, while `.lake` package checkouts are excluded and pinned through `lake-manifest.json`. `--all-claims` retains every current claims.csv row, including unresolved theorem locators, and batch-resolves exact candidates in one imported environment; `--module MODULE` enumerates declarations owned by that module, while `--all-d0` enumerates D0-owned declarations reachable through the selected import. Bulk module enumeration can omit proof-term dependencies and axiom closures with `--omit-proof-details`; the crosswalk uses that bounded mode for source co-location candidates, then requests full details for exact claim-locator matches. These produce reproducible crosswalk candidates, not semantic coverage. This is exact elaborated evidence, not a normalized semantic equivalence proof. A reviewer binds that type to the source claim's object, domain, quantifiers, and assumptions. Load-bearing applications need compiled Lean adapters over actual objects and maps; a field that assumes the desired conclusion is not an adapter.

The collector has run successfully on `D0.Foundation.VerificationCore.verification_core` and the new `D0.Geometry.archiveJuliaRaisingQuery_vacuum_exterior`. Both are found in the compiled environment with actual types, binders, proof/type dependencies, source ranges, and axiom footprints. The verification theorem retains its quantified `FutureExecution` and `TheoryVerification` inputs and is located at lines 227–240 of its source. The Eq. (26) model theorem is located at lines 50–57 of `ArchiveJuliaRaisingOperatorReadout.lean`; its exact type is `∀ u M, archiveFockExteriorEquiv (archiveJuliaRaisingQuery u M vacuum) = ι ℝ u`, with `u : RoleSpace` and `M : RoleSpace ≃ₗ[ℝ] RoleSpace`. The collector reports `Classical.choice`, `Quot.sound`, and `propext` for both this theorem and its existing creator-on-vacuum lemma. These are exposed dependencies of the existing finite-carrier representation; this checkpoint does not claim an axiom-free kernel. The Eq. (26) inventory result was captured at HEAD `b2b73963991bb18c42766ae753bef1c70314c9ab` with `worktree_dirty=true`, Lean source digest `8993ecd144677720658cb3187ba737cb512b7c20a27d541ac93cc212b2b28f3f`, and collector script SHA-256 `4d4edc04deec3e2ad185e9fcf1ba3b7e63bfb16ba1fbc3d9905d253aa2d8ef11` under Lean 4.30.0.

Search is deterministic and bounded: exact IDs/names, aliases, sections, declared result/application links, and scoped attempts first. The content pass uses one `rg --json` scan to build query-specific concept hits, then reads evidence and follows pins only from its bounded top candidates. Russian/English concepts are grouped; low-information words are dropped from scoring when enough specific groups remain. Results include matched lines and nearest headings, with direct content, filename-only hits, and citations kept distinct. Ranking may suggest candidates but cannot set truth. Search failure is not nonexistence.

`reuse --lean CLAIM-ID` joins one exact claims.csv row to its theorem-name candidates, declarations actually present in the selected compiled Lean import, and their reported proof dependencies. It also reports exact dependency-name intersections with other claim locators as candidate crosswalk edges. This compiled Lean evidence remains separate from declared assembly application edges, conceptual presuppositions, and semantic acceptance.

The read-only `tools/proof_architecture.py` view composes current claims, registered assumptions, formal-support locators, aliases, assembly contracts/results/applications/attempts, conceptual presupposition edges, and bounded full-text candidates. Claims expose their registered assumption rows separately from applications and conceptual edges. Commands are `search`, `show`, `why`, `reuse`, `crosswalk`, and `impact`; `show NAME --lean --import-root MODULE` calls the elaborated declaration collector. `crosswalk RESULT-ID` verifies pinned Lean evidence blobs, compares them with current source, and enumerates declarations from the compiled `D0.All` environment only when the bytes match. It reports compiled types and source ranges for co-located declarations, full proof dependencies and axiom footprints for exact claim-locator matches, and formal-support module locators as candidates. `crosswalk` without a key gives a bounded all-result summary without declaration enumeration. Every answer includes source digests and a snapshot commit. Conceptual edges, assumption links, alias lookup, text matches, declared application edges, and elaborated Lean facts are distinct output kinds. `why` reports unknown hypotheses separately from explicitly empty declarations and distinguishes unmapped hypotheses, unknown targets, and invalid map entries. `impact KEY` follows only currently declared evidence/application refs; `impact --base REF` delegates to the existing assembly diff impact. Neither form claims a complete global semantic impact graph.

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
- The 54 assembly results already carry pinned evidence records with commit, path, and SHA-256. The missing crosswalk is from each result to a C0 mathematical unit (a claim ID or exact source:<commit>:<path>#<section> key), and to any relevant public declaration or application disposition. Obligations, results, evidence, and reviewed application edges remain distinct; the application file still lacks a canonical claim-ID crosswalk.
- Enumerate theorem-like public declarations reachable through the compiled D0.All import as candidates. Public helpers, generated declarations, definitions, and instances must be classified; inclusion in an import closure alone does not make them reusable mathematical results.
- Bounded candidates from 04_CERTIFICATES/ and 05_EXPERIMENTS/ are exact computations, certificates, constructions, and negative controls found on cited or otherwise in-scope paths. A missing mathematical-consumer edge is a reconciliation gap, not an exclusion reason; exclude raw logs and exploratory runs without a mathematical assertion.
- The assembly attempts (4), anti_substitutions (25), synthesis (8), and source_fork_reconciliations (1 record pointing to two child PRs and four result IDs) are retrieval, provenance, and countercontrol inputs. They inform unit resolution and expose crosswalk gaps, but do not become extra result units merely by being indexed.
- Bound the original raw response terminal to its exact existing contract key: consumer RAW-216 → obligation raw_response_terminal → interface raw-216-v1. Preserve the complete interface: carrier = original fixed smooth Q_h with genuine Lorentz quotient and independently fixed smooth τ; action = original designated geometric Euler response and declared source equations; variations = exact joint connection and metric source equations; source = original #216 comparator Xi(Q_h,K_h)=h²τ(hx); normalization = h⁻² times the unweighted raw ℓ1 sum over h⁻⁴ sites; refinement = exact samples of the same g and τ on a refining sequence in the admitted log chart; scope = original response terminal. Exact comparator source pin: merged PR #216, commit 5523d8f679c1ea02f9b73d757c81649740010d0a, file 02_REGISTRY/research/MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md, blob 21b768681cd4bf12b9dda22fc86c43d6b831bbec, source key 5523d8f679c1ea02f9b73d757c81649740010d0a:02_REGISTRY/research/MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md#Sections 4, 7-9. Sections 4 and 7 give the smooth approximate sheet and residual; Section 8 leaves the uniform full coupled normal rescue open; Section 9 states the conditional response/reconstruction. This pins the provenance of K_h^sm only. It does not provide an exact raw-terminal root sequence or close RAW-216; the full interface and its fixed source, joint variations, unweighted norm, refinement, and quantifiers remain as specified above. Preserve its quantifiers and owner; do not import the whole historical corpus or claim this architecture closes the terminal.
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

Next: reconcile the exact-name inventory with source-keyed mathematical units and dispositions, obtain independent acceptance of the exact C0 package, and continue the remaining established mathematical migrations. The 24 October checkpoints below record the refreshed 13-case cold-start suite, compiled claim-reuse examples, shared Vieta migration, and current `D0.All` build. The reviewed Eq. (26) application covers the finite-carrier vacuum response; all-state operator comparison, endpoint-field binding, the §§8.4–8.5 inverse, and the §5.1 consumer transport remain with their existing owners. Migrate connected mathematical blocks while preserving public imports and scopes; formalize or obtain accepted owner review for every established C0 unit. This checkpoint is not completion.

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

### Current parent-namespace candidate refresh

The later locator refresh expands each module locator through its enclosing namespaces before the `D0.` fallback. This catches exact declarations such as `D0.Foundation.omega8_center_collapse` when the claims row points to source module `D0.Foundation.Omega8Center`. The expansion is a candidate-name rule; compiled name resolution remains exact, and no claim/application relation is accepted from it.

On source snapshot `b6e624b3473682758d0fe98c48313243db8f62c8` with `worktree_dirty=true`, the 889-row `claims.csv` SHA-256 is `e986bcc75fd6a2c84a80ee61b639482af1b21464fcfe4c961491b4a97bb9037f`. The request contains 2,741 theorem-atom mappings and 8,426 candidate references, deduplicated to 8,294 exact candidate names. The compiled `D0.All` resolution-only run found 2,497 names and 5,797 exact misses; 2,537 theorem-atom mappings have at least one resolved declaration, across 705 claim rows. The 176 rows with no theorem locator remain visible. These counts use an updated claims source and candidate-generation rule, so they are not a coverage percentage or a direct continuation of the older 5,487-name snapshot.

The refreshed inventory is [claim_candidate_resolution_parent_namespace.json](sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_parent_namespace.json), SHA-256 `a3ab4d9ec0ad5a77f041e2e88fa1d7d0b3a740f9ddebd8016bae87918e828a65`. It records Lean source digest `4b760603dd653cf0354beacd1d78da0879c570b744059c37115ec2ac2d8936ac`, collector SHA-256 `24289b940bc867e4ccea28cbd9771033669662dc5017f53e7a14ad780cadd30d`, toolchain Lean 4.30.0, `D0.All`, the claims source SHA, and dirty-worktree state. The generated inventory checks that every requested candidate receives exactly one response; all found names have an owning module and source path. The run does not bind claims to prose or freeze C0.

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

### Independent scope review of the finite Eq. (26) CAR adapter

The read-only review of PR #402 head
`20d5ef7915338d856dd16e5676d7cf669b04d273` returns a scoped PASS: the current
`archiveCARVectorCreator` is the coefficient-weighted sum of the repository's
owned Jordan--Wigner `carCreateEnd` matrices, and
`archiveJuliaCARRaisingQuery` composes it with the 16-state exterior frame
lift. On the vacuum, the CAR and exterior-model queries agree and their
exterior image is `ι u`; the readout therefore returns `u`. This is a finite
carrier application of pinned #334 Eq. (26). The result holds for the broader
Lean parameters `u : RoleSpace` and `M : RoleSpace ≃ₗ[ℝ] RoleSpace`; the
source's nonzero and Lorentz-endpoint hypotheses are not needed for this
vacuum identity.

The review leaves explicit boundaries: the CAR/model comparison is only on
the vacuum, not equality of the full query operators on all 16 inputs; `u` and
`M` are not bound to the source endpoint fields and observer maps; and the
full inverse, its all-jet pullback, and the §5.1 consumer are not formalized by
this slice. It changes no #334 owner, C0 disposition, scientific status, or
physical admission premise. The reviewer did not edit files or run a build.
The exact source was commit
`fe5cf335da04cac14e50407b03f98b96be17dc52`, file
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
§§8.4–8.5, including Eq. (26), blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`.

Reviewed Lean blob hashes at that PR head:

| Input | Git blob |
|---|---|
| `03_FORMALIZATION/D0/Geometry/ArchiveJuliaRaisingOperatorReadout.lean` | `0840cf6e075274a4604695a32fae5a61e61c4ce4` |
| `03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean` | `087afdd443ffc02701376e00728193c020da259d` |
| `03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean` | `8ff68576d92ff67532733a0ca2646de9d50105e2` |
| `03_FORMALIZATION/D0/Geometry/A4DNilpotentAffineMatterLift.lean` | `a923290e3f4e0ee7289db1142251141a25d6c42a` |
| `03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean` | `1acfaec4d7a41b50f50dd55cced7613b80852514` |

### 24 October shared tripartite spectral-gap application

The established claim family `D0-SYMMETRIC-FUNCTION-ACTIVE-SPECTRUM-001`
contained the same rational degeneracy-gap definition in
`ActiveSplittingFromDistinctness` and `ActiveSpectrumClosedForm`. Both are now
abbreviations to the existing lower-level Vieta invariants,
`tripartiteGap = tripartiteV * tripartiteE - 9 * tripartiteT`. The common
`TripartiteVieta` module owns its exact weighted sum-of-squares identity,
nonnegativity for positive sizes, and zero-if-and-only-if-equal criterion.
The previous `gap`, `gap_sos`, `gap_nonneg`, and `gap_zero_iff_equal` names
remain available as compatibility APIs.

The spectrum module now proves its general `discriminant_eq` application by
composing the owned `SymmetricFunctionCalculus.degree_product` with the common
tripartite-gap formula. Its ladder identity consumes the shared sum-of-squares
theorem; the `(9,11,13)` and `(10,11,12)` checks consume that ladder result.
The existing claim row gained exact locators for these named applications and
the shared API, with the original status and owner unchanged. `formal_support`
now lists both Lean consumers, and the generated `ClaimMap` was refreshed.
No new claim, assumption, status, physical premise, or assembly edge was added.

The compiled `reuse --lean D0-SYMMETRIC-FUNCTION-ACTIVE-SPECTRUM-001
--import-root D0.All` view resolves all 13 exact theorem-name atoms. Its
proof-dependency evidence shows:

- `ActiveSplittingFromDistinctness.gap_sos` uses
  `TripartiteVieta.tripartiteGap_sos`, and
  `gap_zero_iff_equal` uses `tripartiteGap_eq_zero_iff`;
- `ActiveSpectrumClosedForm.discriminant_eq` uses
  `SymmetricFunctionCalculus.degree_product` and the shared gap formula;
- `gap_ladder` uses the shared sum-of-squares theorem, and this module's
  `scene_gap` uses `gap_ladder`.

The source claim atom `scene_gap` resolves to both existing scene-specific
declarations, one in each consumer module; both remain visible as separate
compiled sources. This does not claim that their surrounding source claims
are semantically equivalent beyond this exact rational equality. The compiled
footprint for these declarations reports `Classical.choice`, `Quot.sound`,
and `propext`, as does the existing rational quotient representation; this
checkpoint makes no axiom-free-kernel claim.

Validation on the local tree at parent snapshot
`7f5eb1d83f40a865ac18032702b907f9f331046b` (`worktree_dirty=true`): narrow
Lean 4.30.0 builds of `TripartiteVieta` (2,946 jobs),
`ActiveSplittingFromDistinctness` (2,947 jobs), and `ActiveSpectrumClosedForm`
(2,948 jobs) passed. Final `D0.All` passed (4,564 jobs) with source digest
`20302031987450765dc6c63b19fb9b968681b9c4a506534678ec54db3ee0065f`.
The compiled-reuse collector SHA-256 is
`06944bb4e3b3b530ac552716fa61eaaa2b4161ac85de5511f526b7dd886f9c76`; its
Lean source digest matches the final-build stamp. The existing proof-architecture
suite passes 26/26 tests; cold-start retrieval finds all required sources in
13/13 cases, and the 14-case impact benchmark passes. Generated Lean views
(stale=0), claim-map coverage, and `git diff --check` pass. No proof hole was
added in these three modules; the only search hit for `admit` there is in a
docstring.

Exact file SHA-256 values at this checkpoint:

| Input | SHA-256 |
|---|---|
| `03_FORMALIZATION/D0/Combinatorics/TripartiteVieta.lean` | `cf048f006496e7d0fb86eb94bdd8414739129a2e33b4b7cc3ac2337ec2dfebde` |
| `03_FORMALIZATION/D0/Synthesis/ActiveSplittingFromDistinctness.lean` | `cc720d10d9b2881fa3c0235f428c128703d802369740a3c2e18a511282e6152c` |
| `03_FORMALIZATION/D0/Synthesis/ActiveSpectrumClosedForm.lean` | `00280f3d52ea7b64cedbc09e29cab511678fdee90540845fb1611d917c74205c` |
| `03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean` | `f08e64ef7243c8da2055415a2754dcde71c37a7c6d7bb95edbc258fa5ae14488` |
| `02_REGISTRY/claims.csv` | `e7fb0e77368540e4fcb77446a63678e84867149020a7191627a2d82d565b3e87` |
| `02_REGISTRY/formal_support.csv` | `9550a4390b13c1429dfedf61d97c2e8401bb283a04ae74de8319c3269dbfb9bf` |

This is a vertical refactor and compiled reuse application inside one existing
finite mathematical claim family. It neither freezes nor accepts C0, and it
does not alter #334 ownership, the native physical action/source, or any open
GR-selection assumption.

### 24 October shared Perron-GNS refinement lemma

`D0.Algebra.FibonacciAFTower.gns_refinement_isometry` and
`D0.VNext.PerronGNSTower.gns_refinement_isometry` had the same generic
statement and proof. The core module is now the single proof owner; the
vNext theorem remains under its old public name as a compatibility wrapper.
The duplicate nonzero-phi and Perron-trace consistency results in the vNext
module likewise delegate to the existing core declarations. The vNext owner
theorem still consumes the compatibility wrappers, so its public theorem type
is unchanged.

The existing vNext claim row now lists both module locators and the exact
supporting declarations; `formal_support` records the core module's vNext
consumer, and the generated `ClaimMap` was refreshed. The claim ID, scientific
owner, status, and all physical assumptions are unchanged. The compiled
`reuse --lean D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001 --import-root D0.All` view
resolves the owner, wrapper, and Perron helper locators. Its extracted proof
dependencies show the vNext isometry wrapper calls the core isometry theorem,
the vNext trace wrapper calls the core trace-consistency theorem, and the
vNext owner theorem consumes those wrappers. The vNext and core declarations
remain separate elaborated sources with the same displayed isometry type.
This is exact dependency evidence, not semantic claim acceptance.

The type boundary remains explicit: the generic result assumes that a supplied
map preserves multiplication and star and that supplied traces agree on that
map. The vNext owner theorem itself retains that conditional type. The finite
application below constructs one explicit real refinement embedding, but does
not prove positivity and completion of a GNS Hilbert space or construct all
levels of the complex AF tower. Those remain outside this proof slice and
with the existing owner.

Local validation: narrow Lean builds passed for `D0.Algebra.FibonacciAFTower`
(2,947 jobs) and `D0.VNext.PerronGNSTower` (2,948 jobs). The current public
import `D0.All` passed at 4,564 jobs after the updated `ClaimMap`; the exact
Lean source digest is `2c8ab138a4ec9315544f461df3e8eb0a2188782762a616c4c4ad651d687a5606`.
The compiled-reuse collector SHA-256 is
`e4dd22a88a58f03d98672c4133f742f38483a39b8f06cd71bf8dfcc11540319e`.

SHA-256 for the changed source and generated registry inputs:

| Input | SHA-256 |
|---|---|
| `03_FORMALIZATION/D0/VNext/PerronGNSTower.lean` | `3e555de788da152afad833288d0e0945da3b74ce4abe7a587bb9d8696b64f544` |
| `03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean` | `0d0829b214e1b0a18654e5cd07a729528c2075f185b0bb23c32c9068d4411250` |
| `02_REGISTRY/claims.csv` | `493866102b2c4c13c9c31c502c4142abc1349178f35edeb32322f23c42314770` |
| `02_REGISTRY/formal_support.csv` | `e90d167d4b719783b90f0e5e24d848c39fa38bfcce6d09bb40599fad8cfa0709` |

### 24 October all-level finite real Bratteli map and compatibility refactor

The canonical core module now owns the Fibonacci path-count and dimension
recurrence used by the vNext compatibility API. `D0.VNext.FibonacciAFAlgebra`
keeps its former public names as aliases and wrappers. The existing total
33-dimension no-go proof now unfolds the core recurrence explicitly; its
theorem statements and scope are unchanged.

For every level `n`, `FibonacciAFLevel n` is the product of the two real square
matrix algebras whose sizes are the two components of `pathCount n`.
`fibonacciAFRefinementHom n` constructs the actual Bratteli map
`(A,B) ↦ (diag(A,B), A)`. The core proves this map is a unital ring
homomorphism, injective, and star-preserving. With
`τₙ(A,B) = (φ⁻¹)^n (φ·tr(A) + tr(B))`, `fibonacciAFRefinement_trace_preserving`
proves exact trace transport at every step. The concrete application
`fibonacciAFRefinement_pairing` then applies the shared generic
`gns_refinement_isometry` to prove pairing preservation for every `n` and all
inputs, with its exact dependencies visible in the compiled declaration.

The existing `D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001` claim row now includes the
core map, trace and pairing locators. `formal_support` names the vNext consumer;
generated `ClaimMap` and views follow the source registries. The compiled
`reuse --lean` output was regenerated against public import `D0.All`, and the
focused compiled declaration
`D0.Algebra.FibonacciAFTower.fibonacciAFRefinement_pairing` reports direct
dependencies on the generic isometry, constructed ring map, star-preservation
and trace-preservation proofs. This supplies a concrete every-level finite
application of the reused result.

Scope remains finite and real: this does not establish positivity of a trace
state, the complex C*-inductive limit, the GNS quotient/Hilbert completion, or
physical Hilbert-space identification. It does not freeze or accept C0, change
the physical selection assumptions, or alter the ownership of #334.

Validation on this source snapshot: narrow builds passed for the core tower
(2,947 jobs), the vNext Perron-GNS compatibility module (2,948 jobs), and the
updated 33-skip consumer (2,949 jobs). The final public `D0.All` build passed
(4,564 jobs); its Lean source digest and final-build stamp are both
`359038283894257580b8ba360cad11a27c40d0b12009e0b3ba861f8b71e76912`. The
focused compiled pairing view has collector SHA-256
`4224b95cee4404aecf5599339323587d6044a15071e33e594d98482374a93f36`; the full
compiled claim-reuse view has collector SHA-256
`71124231eb5dba16b3b98e4ca8894c7465fbd81d378fe4224934edaa69f83d0a`. Proof
architecture tests passed 26/26, declaration-inventory tests 12/12, generated
views report `stale=0`, ClaimMap coverage passes, formalization-debt findings
remain at baseline (3/3), and `git diff --check` passes.

SHA-256 for this checkpoint's source and generated registry inputs:

| Input | SHA-256 |
|---|---|
| `03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean` | `aacfc863ef18e774e6f97e697e2c593a0862ede76e1be1d1e333a2469ce53f8b` |
| `03_FORMALIZATION/D0/VNext/FibonacciAFAlgebra.lean` | `e4716d1f6f3cb393dc77b24738aeef90f6a0d186863b19c5608dd4d112241066` |
| `03_FORMALIZATION/D0/VNext/AFD0LaplacianComparisonNoGo.lean` | `64a20335dc4a1339eed1229b4bcf3b6e29e92525c2c7474047a1f3c529b1e91c` |
| `03_FORMALIZATION/D0/VNext/PerronGNSTower.lean` | `c317e65c0b4d239bcdf161a0c3494176a358b319e691a61064edb71e6bc3b2c5` |
| `03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean` | `5757cbbdaacfbb6eba15694ef09769b17525002e3fe5800094725faa00e91e96` |
| `02_REGISTRY/claims.csv` | `d70e7d4546d4cc85530be297bb75ff9384fe16b35c73137ea2b8c152e0c4d312` |
| `02_REGISTRY/formal_support.csv` | `cea9176d163d18e9dc06523ae402286dbdbde6b310b22f96e1be83e342a88d22` |

### 24 October first finite Perron refinement application

The vNext module constructs the first finite real refinement map
`(x,y) ↦ (diag(x,y),x)` from `ℝ × ℝ` to `M₂(ℝ) × ℝ`. Lean proves that it is
a unital ring homomorphism, injective, and star-preserving. The explicit
functionals
`τ₀(x,y)=φ*x+y` and
`τ₁(A,z)=φ⁻¹*(φ*Matrix.trace(A)+z)` satisfy exact trace preservation for this
map. `fibonacci_first_refinement_pairing` applies the shared generic theorem
to prove `τ₁(star(ι y)*ι x)=τ₀(star y*x)` for all inputs at this finite step.

The existing vNext claim row lists the finite application and its map/trace
locators; generated `ClaimMap` follows the same source row. Compiled
`reuse --lean` resolves all ten locators. Its actual proof dependencies for
the finite pairing include the canonical
`D0.Algebra.FibonacciAFTower.gns_refinement_isometry`, the concrete ring map,
its star-preservation theorem, and its trace-preservation theorem. The
compiled declaration reports the existing rational quotient axioms
`Classical.choice`, `Quot.sound`, and `propext`.

This is a concrete first-step real algebra model only. It does not establish
trace positivity, the GNS quotient/Hilbert completion, the full infinite
complex AF tower, or any physical Hilbert-space identification. Existing
owners and statuses are unchanged. At this source snapshot the Lean digest is
`d56dfa1bf4dc15f6a56fb2bbba093deeffd3185a0cbc46573c98a355ba93b0b8`; the
compiled-reuse collector SHA-256 is
`3578878542b346af5a7f30e50f5c1927ac7f4258da1db806fceb6a747382b39a`.

The final local `D0.All` build on this exact Lean digest passed (4,564 jobs);
the `d0-final-build.sha256` stamp matches. The new finite-step module passed
its narrow build (2,948 jobs). Proof-architecture tests pass 26/26, generated
views report `stale=0`, claim-map coverage passes, formalization-debt findings
remain at the existing 3/3 baseline, and `git diff --check` passes.

SHA-256 for the finite-step source and its registry views:

| Input | SHA-256 |
|---|---|
| `03_FORMALIZATION/D0/VNext/PerronGNSTower.lean` | `c317e65c0b4d239bcdf161a0c3494176a358b319e691a61064edb71e6bc3b2c5` |
| `03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean` | `c1a1a4757a5409973a9286b346f761d0166f9300d23702184a4fc7a0db1f16e1` |
| `02_REGISTRY/claims.csv` | `43ae5a73034941e029a0284aec54352f9bb24ad2cf6d7d5cbb7b71f0fa3a3ff1` |
| `02_REGISTRY/formal_support.csv` | `e90d167d4b719783b90f0e5e24d848c39fa38bfcce6d09bb40599fad8cfa0709` |
### 24 October 2026 Perron refinement scope correction (independent review pending)

The published source snapshot for this correction is execution PR #402 at
`b6e624b3473682758d0fe98c48313243db8f62c8`. The current Lean declarations construct, for every
Fibonacci path-count level, a finite real matrix refinement map and prove its injectivity, unital
ring-homomorphism, and star-preservation properties. The specified real-valued Perron functional is
transported exactly, and the resulting algebraic pairing is preserved. The generic
`gns_refinement_isometry` theorem is conditional on supplied multiplication, star, map, and
trace-preservation facts; it does not construct a state or Hilbert space.

The retained formal boundary excludes positivity or normalization as a state, a complex AF C*-inductive
limit, uniqueness of a trace on that limit, the GNS quotient and Hilbert completion, an isometry between
GNS Hilbert spaces, and Dixmier normalization. The historical broader tower assertion remains open under
`D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001`; the existing owner IDs and the separate scale and comparison-map
owners are preserved.

The prior `vp_vnext_perron_gns_tower.py` association is detached from both AF/GNS claim rows. Its checks
are floating-point scalar identities and a separate normalized `M₂(ℝ) → M₄(ℝ)` example; the hardcoded
negative-control flags do not verify the constructed Fibonacci tower. The legacy script remains at its original path, unedited for provenance, but is no longer linked as evidence for the narrowed formal result.

The related dimension certificate proves that no finite Fibonacci level has dimension 33. That blocks
an equal-dimensional carrier identification only. It does not prove the absence of an arbitrary or
canonical comparison map without a specified map class and compatibility conditions. Accordingly, the
formal owner and primitive entries retain the dimension-separation result and preserve the broader
`PRIM-COMPARISON-MAP-XI-N` question as open. The two registered scale/Xi edges are necessary downstream
obligations and are not an exhaustive decomposition of the full Hilbert-GNS/Dirac target.

**Review state:** the exact scope correction is staged in the current execution branch, but the required
independent acceptance has not yet been received. Do not treat this C0 reclassification as complete until
that review accepts the corrected source, dependent claim rows, detached certificate associations, and
primitive map. The broader GNS construction and all unrelated physical premises remain open.
### 24 October Bratteli trace-uniqueness scope and finite composition

Independent scope review found that D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001 still described the
existence of one positive Perron vector as uniqueness of a normalized AF/cylinder trace. The claim row
now retains the same owner ID and is PROOF-TARGET for that all-level trace statement. Its formalized
slice records incidence recovery, the quadratic identity, the initial path-count step, and one explicit
positive left-Perron vector. The separate D0-FIBONACCI-PERRON-PROFILE-CANONICITY-001 theorem proves
uniqueness of the normalized positive two-component eigenprofile; a new Lean application in the
Bratteli module consumes that result without identifying the vector theorem with uniqueness of AF
traces.

The existing high-level finite tower claim now points to the compiled
finite_renormalization_refinement_composition: it binds the incidence recovered from the language,
the actual all-level finite-real matrix refinement and its specified compatible functional, the
normalized Perron profile theorem, and the scale-ratio theorem. Its scope excludes a complex AF limit,
uniqueness of all compatible AF traces, GNS completion, Hilbert-space isometry, and the physical
inductive spectral triple. The independent all-level compatibility derivation remains in
A4D_NATIVE_AF_TRACE_PREPARATION.md and is still to be formalized under the retained Bratteli owner.

The canonical BOOK_02 and BOOK_05 summaries now state these boundaries. The compiled narrow build of
D0.Geometry.FibonacciBratteliRefinement passed (2,952 Lake jobs) after the new application and
composition were added. The refreshed ClaimMap lists both the finite owner result and its reused
profile application; the high-level finite composition is now an elaborated declaration rather than
a metadata-only cross-reference. Independent follow-up review accepted the corrected scope: the exact
certificate establishes only the checked transitions N=0..3, and both the all-N theorem and canonical
selection/transport remain open. The theorem docstring in D0.Algebra.FibonacciAFTower was narrowed to
state scalar Perron weight/functional identities, with no trace-state or AF trace-uniqueness claim;
its narrow build passed (2,947 Lake jobs). This review accepts these wording corrections only and does
not accept the broader AF trace or spectral-triple owners. The current full-source integration remains
pending.

### 24 October pinned assembly-to-Lean declaration crosswalk

`tools/proof_architecture.py crosswalk` now produces a read-only summary over all 54 assembly results;
`crosswalk RESULT-ID` verifies each Lean evidence blob with Git, compares its exact bytes with the current
source, and queries the corresponding owner module through the compiled `D0.All` environment. The
`crosswalk --all-current` mode enumerates the union of all verified current D0 owner modules in one
compiled pass and returns a detailed row for every assembly result. Each output records the exact
authority-source and Python-tool SHA-256 digests used to produce its candidate rows. The declaration
inventory reads each module's imported module data directly instead of scanning every constant in the
full import. It reports elaborated types, binders, type dependencies, source ranges, declaration kind,
and internal-name status. For exact claims.csv name-locator matches it also extracts proof dependencies
and axiom footprints. Other co-located declarations are labeled as candidates and mark bulk-omitted proof
details explicitly. Parent namespace candidates allow a source module locator to resolve a theorem
declared in its enclosing namespace; they remain exact-name locators, not application edges.

In the current applications.json snapshot, all 13 pinned Lean evidence blobs verify against their
recorded Git commit/path/SHA-256. Eleven working-tree files still match those pins: ten are direct
`03_FORMALIZATION/D0` module sources across nine distinct modules, and one is the current research
certificate `02_REGISTRY/research/certificates/a4d_native_retained_record_admission.lean`, outside the
`D0.All` module tree. The two non-current D0 source pins are the missing #334 cost-information
certificate and `D0.Foundation.EmpiricalTheoryFactorization.lean`, whose bytes changed since its
recorded commit. They remain citation-only for current compiled-declaration purposes until a matching
source or reviewed bridge is supplied. The other 45 assembly results have no direct pinned Lean
evidence and stay unresolved in this declaration crosswalk.

The detailed result `original-q8-spin-sheet-current-fullstep-boundary` enumerates 30 declarations in its
two matching current files (`Omega8Center.lean`: 14; `GoldenCoherentMemory.lean`: 16). Parent-namespace
resolution finds the exact claim locator `D0-OMEGA8-CENTER-001` at
`D0.Foundation.omega8_center_collapse`, a theorem at lines 59–69. The compiled theorem has three
`native_decide`-generated axiom dependencies. This is a declaration/claim locator candidate only: the
result's semantic relation remains unresolved, and no result-to-claim acceptance is inferred. The
Q8 result owner, source scope, and physical admissions remain unchanged.

The all-current batch output contains 899 co-located declarations across six result rows and nine D0
modules. Exact theorem-name joins produce 18 candidate declaration matches in two result rows: 17
under `native-actionprotocol-book03-pullback-boundary` and the Q8 match above. Both rows retain
ambiguous/candidate locator dispositions as reported by their exact match counts; neither gains a
semantic result-to-claim relation. The machine-readable output
`sources/d0_proof_architecture_formalization_2026-10-24/assembly_result_declaration_crosswalk.json`
includes all 54 result rows, the three pinned but missing/changed/out-of-module source cases, all seven authority-source
digests, tool-source digests, and collector metadata. The JSON SHA-256 is
`4e92d2d872164344b943ca84256ffa3b028b23a211daa0f77385477f1ef9a922`. This generated view is an input to C0 review, not C0 acceptance.

The proof-architecture and Lean-inventory suites pass 44/44 tests. The live `D0.All` declaration
extraction used Lean source digest `4b760603dd653cf0354beacd1d78da0879c570b744059c37115ec2ac2d8936ac`;
the module and exact-detail collector scripts are pinned in the generated output. This crosswalk closes
no C0 classification or physical assumption, and the exact C0 package remains unaccepted.


### 24 October refreshed all-claims Lean locator resolution

The earlier all-claims resolution above is retained at its original Lean source digest `dd056ebca233774b20e628d8b7efd3f94e344b18d0fa07e8abf973e229e1857d`. The current D0 sources have changed, so the exact-name resolution was rerun against `D0.All` on clean snapshot `1b7f1cbb5e597af31b59a83bd37edac73b0d4e47`, with Lean source digest `4b760603dd653cf0354beacd1d78da0879c570b744059c37115ec2ac2d8936ac` and claims registry SHA-256 `e986bcc75fd6a2c84a80ee61b639482af1b21464fcfe4c961491b4a97bb9037f`.

Across 889 claims, the collector expands 2,741 theorem-locator atoms into 8,294 unique exact candidate names. It finds 2,497 current declarations and 5,797 exact misses. Of the locator atoms, 2,533 match one candidate declaration, four match two candidates, and 204 match none. At the claim-row level, 705 rows have at least one resolved locator and 184 have none. These are current name/module/source-path availability counts, not theorem coverage or application acceptance.

The reproducible prior output is `sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_snapshot_1b7f1cbb.json` (2,535,647 bytes; SHA-256 `e0f4705fc20db6e236cf9c8de4a094ed97e2f7b2054891005fa82e17e1aef40c`). It records clean snapshot `1b7f1cbb5e597af31b59a83bd37edac73b0d4e47`, Lean source digest `4b760603dd653cf0354beacd1d78da0879c570b744059c37115ec2ac2d8936ac`, claims registry digest `e986bcc75fd6a2c84a80ee61b639482af1b21464fcfe4c961491b4a97bb9037f`, collector SHA-256 `24289b940bc867e4ccea28cbd9771033669662dc5017f53e7a14ad780cadd30d`, and toolchain `leanprover/lean4:v4.30.0`. The current all-claims result after the subsequent locator corrections is recorded below. The matching claim names remain locator candidates until their scope and application are checked; this refresh changes no status, owner, assumption, C0 disposition, or physical premise.


### 24 October compiled reuse through controlled claim aliases

The `reuse --lean` view now follows an exact `CANONICAL_TARGET` entry in aliases.csv to the named canonical claim, then compiles that claim's exact theorem locators. It returns the canonical claim's scope/status metadata separately from the compiled declarations. A legacy lookup-only alias does not trigger Lean compilation; a missing canonical target is reported without querying a guessed name. If an alias key is also an exact claims.csv ID, the direct claim and alias target compile as separate views; the alias never silently replaces or merges the direct record.

Two live applications were run on clean snapshot `7156fe33397669278bf4a558c003743dc842b19a`, with `tools/proof_architecture.py` SHA-256 `0d883453b8bb9ae5e8cbfe5d124c3d0cfd0c950b88f7c82dde690fc7dce6a3f6` and Lean source digest `4b760603dd653cf0354beacd1d78da0879c570b744059c37115ec2ac2d8936ac`:

- `D0-ARCHIVE-WEYL-INTERFACE-VACUITY-NOGO-001` resolves to canonical claim `D0-ARCHIVE-WEYL-DIMENSION-VACUITY-NOGO-001` (`NO-GO`); all four registered theorem locators resolve to current compiled declarations.
- `D0-ALBERT-SM-GAUGE-DIMENSION-ALIGNMENT-001` exists both as a direct claim and as an alias to `D0-ALBERT-SM-GAUGE-PROJECTION-001`. The direct row's one locator resolves; the canonical target's five locators resolve. Both claim records and both declaration sets remain distinct, with their existing `CORE-FORMALIZED` status.

The full outputs are in `sources/d0_proof_architecture_formalization_2026-10-24/controlled_alias_compiled_reuse_current.json` (129,255 bytes; SHA-256 `225ef78202be3c4552d511d3b0f3743f17f2fe89ed1914f698689b2c1e72b370`). This verifies alias routing and current declaration availability only; it proves no semantic equivalence between the two Albert claims, no assembly application, and no new acceptance or scientific status.

### 24 October exact locator repair and scope boundary

After the two exact stale-name repairs, the all-claims resolution-only query was rerun against `D0.All` on working-tree snapshot `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`. The worktree was dirty because the two Lean comment files and evidence artifacts had been updated. It used Lean 4.30.0, claim-registry SHA-256 `d86d7965f0cf64164cdf7536a4fb5119ec9655e5b5082e3bbe34ce6459d35003`, and current Lean source digest `3530b705e2d59e76c37b153ae6c38f36efe01570f788e052e4624dd13db9ddf7`.

Across 889 claims and 2,741 claim-locator mappings it expanded 8,291 candidate names, found 2,498 exact declarations and 5,793 misses. At least one candidate resolved for 2,539 mappings; 707 claim rows have a resolved name and 182 have none. These are name-resolution counts, not semantic-coverage or claim-acceptance counts. The current output is `sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_current.json` (2,535,371 bytes; SHA-256 `60f8e0925e7ba45298b76084d5706a645c7d0851ffba2e303dd20bef13659577`; collector SHA-256 `3546dc3dc677c9a3e3d205f45fb8e8b636f2d158a05e28b84180eeb2d89ae10d`).
Two registry locators were stale names for declarations with matching bounded
scope, so their locator strings now point to the actual compiled owners:

- `D0-SEDENION-BRANCH-THREESET-SCAFFOLD-001` resolves to
  `D0.Algebra.Sedenions.branch_label_s3_scaffold` in
  `03_FORMALIZATION/D0/Algebra/Sedenions.lean`. Its type gives a carrier of
  cardinality three, transitivity under the listed six S3 permutations, and
  distinct left- and right-projection products. It is a combinatorial
  scaffold; it does not derive Cayley-Dickson multiplication or minimal left
  ideals.
- `D0-ARCHIVE-METRIC-MEASURE-HODGE-LIFT-001` resolves to
  `D0.Geometry.archive_metric_measure_hodge_lift_owner` in
  `03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean`. For real
  `mu` and `c_r`, its type proves the two endpoint weight identities and the
  cardinalities 16 for `CubicalCellType` and 4 for `Role`. It does not prove
  uniqueness or canonicity of the formula across grades, or derive it from
  frozen refinement weights.

Both compiled declarations report `Classical.choice`, `Quot.sound`, and
`propext` in their axiom footprint. The saved compiled-reuse result is
`sources/d0_proof_architecture_formalization_2026-10-24/corrected_claim_locator_reuse_current.json`
(SHA-256 `db084ec50e7414d4d06665907d9a069e1ef1483943da5f26d75efa80903c8de4`;
snapshot `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`; Lean source digest
`88032d37e72ffe0c5868a528eeb7af8da5ec61cb9d658ddaae001c707a2aa3d1`). This
compiled-reuse snapshot predates the final comment-only corrections; theorem
statements and elaborated types are unchanged.

Two wider registered statements remain unmatched and were not redirected to
nearby, insufficient theorems. For
`D0-TRIALITY-SEDENION-S3-DISJOINTNESS-GUARD-001`, the exact registered name
`triality_sedenion_s3_disjointness_guard` is absent from the compiled
environment. The compiled nearby
`D0.Algebra.Sedenions.bare_threeset_insufficient_for_sedenion_realization`
only exhibits two distinct, fully relabeling-equivariant products on the same
three-element carrier. It does not state the Spin(8) outer-automorphism/group
order comparison or an intertwiner, so it cannot discharge that claim.
For `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001`, the registered
name `archive_naive_weighted_degree_leakage_nogo_owner` is absent. The actual
compiled `archive_naive_weighted_car_degree_leakage_nogo_owner` has type
`Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1 ∧ Fintype.card Role = 4`;
its source defines weights 1 and 4. This does not prove failure of
nilpotency, generation of the claimed cross-terms, form-degree leakage, or
that curvature must enter only through the Hodge metric. The earlier Lean
comment described that broader conclusion; it has been corrected to identify
only the two fixed sample weights used in the square-root inequality. The
theorem statement is unchanged.

The two supporting declarations were queried separately through the compiled
`D0.All` environment. Their full elaborated types, source ranges, dependency
lists, axiom footprints, snapshot, and input digests are preserved in
`sources/d0_proof_architecture_formalization_2026-10-24/sedenion_scope_inventory.json`
(SHA-256 `f2a4bbbcdb6bf95eea73e5cf02c27c87728a520bb37cd4630bdcc9dec3314b85`)
and `sources/d0_proof_architecture_formalization_2026-10-24/weighted_degree_scope_inventory.json`
(SHA-256 `e24d12058dd7b6741f93a38e18cfb12c9edf611c5e59bdee38155a2c32a94245`).
Both record source snapshot `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`, Lean digest
`88032d37e72ffe0c5868a528eeb7af8da5ec61cb9d658ddaae001c707a2aa3d1`,
and a dirty-worktree observation caused by the generated evidence outputs.
These are preserved as historical source snapshots; the later edits changed
comments only, not these declarations' statements or elaborated types. The
inventory tool SHA-256 is
`fbc15a59aa7baff75d8c0cc7ce75743301a7cfc7b15d545e0ad1c239ea1c1818`.

No claim status, scientific owner, assumption, or application was changed for
these two unmatched rows. They need owner/reviewer disposition of the exact
scope discrepancy before the registry can state a corrected formal result.
The two repaired locator rows retain their original claim scope and status;
locator correction is not semantic acceptance. C0 remains unfrozen and
unaccepted, and no physical GR selection premise is discharged by this
checkpoint.

An independent read-only scope review of source commit
`6b59bc57ca97275df9e973715cdb503ec8fc5c4e` supports the two locator repairs
within those scopes, with two wording qualifications: the sedenion theorem
lists six transitive functions but does not package an abstract `S3` group
action or construct octonionic branch embeddings; the Hodge-lift claim row is
narrow, while the Lean module's former prologue/docstring had asserted
all-grade uniqueness and frozen-weight reduction. The Hodge comments are now
narrowed to the candidate formula, two endpoint identities, and carrier
counts; the weight definition documents that its real arguments have no
positivity precondition. Theorem statements and claim status are unchanged.

The review also confirms that the separate `triality_outer_order` result is
only `Nat.factorial 3 = 6`; it does not compare a Spin(8) triality action with
the sedenion carrier. The current registered `LEAN_PROVED` / `NO-GO` row is
not supported by the compiled declaration inventory. The weighted-CAR row's
registered locator is likewise absent and its broader `LEAN_PROVED` / `NO-GO`
statement exceeds the neighboring two-value theorem. Its Lean comments are
now narrowed to the theorem's exact weight and cardinality facts. These are
formalization-scope risks for the existing owners, not accepted C0
reclassifications. Status, owner, and source history remain intact pending a scientific-owner
decision or formal independent registry acceptance under repository process;
this read-only review alone is neither.
The read-only scope review did not build Lean; the two touched modules were
subsequently built separately on the working tree (2,953 jobs each), with no
theorem changes.

## Cubical coboundary transfer (24 October 2026)

The registered `D0-ARCHIVE-CUBICAL-COBOUNDARY-001` module previously represented
nilpotency by a Boolean equality and fixed the direction count to four. It now
defines the actual unit-step operator pointwise as
`sum_r (U_r - I) c_r†`. The implementation reuses the existing finite
`dForward` operator, whose coefficient is the refinement scale `L = N + 2`,
by normalizing it with the proved nonzero inverse scale. The adapter proves the
pointwise unit-step formula, `d² = 0`, and degree raising from the existing
compiled `dForward_sq_zero` and `dForward_degree_raise` results. The direction
count is derived from `card_role`, and the 16-state fiber from the existing CAR
carrier theorem. `formal_support.csv` now records the exact module dependency
from the registered coboundary to `ArchiveCubicalDifferential`.

The compiled reuse record is preserved in
`sources/d0_proof_architecture_formalization_2026-10-24/cubical_coboundary_claim_reuse.json`
(SHA-256 `ca1a352d0e6b4d26d2ea120413a35cf853d1025839f53955c2645f662c4b20ae`).
Against public import `D0.All`, both registered atoms resolve to declarations in
`ArchiveCubicalCoboundary.lean`; the owner theorem's compiled proof uses the
Fock-carrier result and the exact `d_squared_eq_zero` declaration. The captured
source digest is `1d10e03b6fe2451cb3c90e98050f42071cd7aad8ca7bc904bb76ad88a2398655`
and the collector digest is
`9e00d0e06830bb13dfb8cc53cdc4f9a12844ccd950d00782fe51b7240a829cfa`. The run
reports the pre-publication local HEAD `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`
and `worktree_dirty=true`; the source digest binds the compiled working-tree
content. Its axiom report includes `Classical.choice`, `Quot.sound`, `propext`,
and the named native-decision axiom from `car_create_anticommutator_int`; the
owner package additionally inherits the one from `carCreateInt_degree_raise`.
These are exposed dependencies, not silently removed assumptions.

This is a concrete proof transfer and compiled application for the named Lean
locators; it does not itself establish that the registered `BOOK_06` source
section and its formula have passed C0 source-key review. The C0 unit package,
semantic source crosswalk, and independent acceptance remain open. No claim
status, scientific owner, physical assumption, or GR premise changed.

Local validation for this slice passed: narrow build of
`D0.Geometry.ArchiveCubicalCoboundary` (2,975 Lake jobs), exact claim reuse via
`proof_architecture.py --json reuse D0-ARCHIVE-CUBICAL-COBOUNDARY-001 --lean`
against `D0.All`, generated-view check (`stale=0`), formalization-debt
non-growth (3 findings, baseline 3), and `git diff --check`. On published
commit `cd9d40e215b5697ab251912203277dfbb685a3b4`, GitHub `D0 Lean build` run
2991 and `D0 guards` run 5029 both succeeded. The compiled-reuse record retains
its pre-publication dirty-worktree provenance and source digests above.

## Hodge degree-preservation application (24 October 2026)

The registered `D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001` module previously exposed
degree preservation only as `DegreePreservingLaplacian true`. It now also
contains a concrete theorem for the existing unweighted Hodge/CAR operator:
if a cochain is supported in Fock degree `k`, then `hodgeCarDirac²` remains in
degree `k`. The proof applies the owned `hodgeCarDirac_sq_fibre` identity and
the fact that the scalar difference Laplacian acts independently on each
fixed Fock component. The number of degrees is now derived as
`Fintype.card Role + 1 = 5` rather than introduced as a bare constant.

The weighted operator `W`, weighted adjoint, and standard-Hilbert self-adjoint
representative are still not constructed in this module. The legacy Boolean
field remains visible as a scope limitation, and the weighted claim's source
and semantic C0 review remain open. No claim status, owner, physical assumption,
or Hodge-metric selection is changed. `formal_support.csv` records the concrete
consumer edge from `ArchiveHodgeCARDiracSquare` to this application.

The compiled reuse record is preserved at
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_hodge_claim_reuse.json`
(SHA-256 `456a37d3eeebc5319e30559ed330e21c2716c8b9d08b78ea822f49480c2f5408`).
The locator resolves through `D0.All`; the elaborated owner type now includes
the exact homogeneous-degree-preservation conclusion, and its proof dependencies
include `unweightedHodgeSquare_degree_preserving` and
`formDegreeCount4D_eq_five`. Source digest
`f964dae2c27862dd29ba822d4368ec329998a821db96dcca080215ab63eee600`, collector
digest `7160df1ba73e78919758cefb84b6dcbc08c04fe21caf3210d3adbfd8b8ed4f45`,
pre-publication local HEAD `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`, and
`worktree_dirty=true` are recorded. The axiom footprint includes the existing
named `native_decide` axioms for the CAR creation, annihilation, and mixed
anticommutator results, as well as `Classical.choice`, `Quot.sound`, and
`propext`.
