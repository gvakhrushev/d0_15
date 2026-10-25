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

Search is deterministic and bounded: exact IDs/names, aliases, sections, declared result/application links, and scoped attempts first. The content pass uses one `rg --json` scan to build query-specific concept hits, then reads evidence and follows pins only from its bounded top candidates. Russian/English concepts are grouped; low-information words are dropped from scoring when enough specific groups remain. Search cards show at most five text candidates, three matched evidence lines and three source pins per candidate, preserve exact commit/blob/section coordinates, and report omitted counts; `show` remains the full-record view. Direct content, filename-only hits, and citations stay distinct. Ranking may suggest candidates but cannot set truth. Search failure is not nonexistence.

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

### Reusable finite Gram algebra and consumer refactor (25 October 2026)

`D0.Algebra.FiniteGramTangent` now owns the generic finite Gram map and its
algebraic laws: symmetry for symmetric `η`, right invariance under any
`Λ` satisfying `Λ η Λᵀ = η`, the exact expansion
`(η + t C) η (η + t C)ᵀ = η + t(C + Cᵀ) + t² CηCᵀ` for symmetric involutive
`η`, and the explicit preimage `C=q/2` of every symmetric `q`. The quadratic
remainder is retained. These results depend only on finite matrix algebra.

The generic API is now used by concrete consumers. In
`D0.Geometry.A4DSolderMetricCompletion`, the solder metric is defined through
the shared Gram map; its symmetry, right-Lorentz invariance, exact tangent, and
all-site symmetric-direction witness use the generic lemmas. The existing
raw-solder frame adapter continues through that invariance theorem.
`D0.Geometry.A4DPathCovariantHodge` now makes its flat Nyquist witness through
the shared map, while `D0.Geometry.A4DStarFiniteLorentzQuotient` defines its
site Gram through the same generic map and preserves the existing full-frame
invariance application. This is a finite algebra refactor across distinct
centered and raw coframe carriers; the theorem hypotheses retain their exact
Role-Lorentz action.

It establishes neither physical selection of the metric path nor
finite-parameter nondegeneracy, the independent full 16+24 variation, a
continuum field equation, refinement, or C0 coverage. It remains an exact
finite algebra application within the metric-provenance route.

The changed modules passed narrow Lean 4.30.0 builds: 2,980 jobs for
`D0.Geometry.A4DSolderMetricCompletion` and 3,213 jobs for
`D0.Geometry.A4DStarFiniteLorentzQuotient`. The public `D0.All` build passed
(4,569 jobs). Generated Lean views are current; formalization-debt, claim-map
coverage, core no-sorry, and gravity-assembly checks passed. The compiled
owning-module inventory records 173 declarations across the algebra module
and three concrete consumers; the selected declarations report the standard
`Classical.choice`, `Quot.sound`, and `propext` footprint. Its path is
`sources/d0_proof_architecture_formalization_2026-10-24/finite_gram_tangent_inventory_2026-10-25.json`,
captured at snapshot `844985b1da25b33884afe5b2fce3701a983a3a29` with
`worktree_dirty=true`, Lean source digest
`6ff55724920a14097e3a4078050c6e8f1f2b15ba6e98aca48623d6691a6e7c40`,
collector SHA-256
`38cf062919c9e100b58cd8800f81f03ea03d26200fe3f9d414d0ed5de74150a`, and
inventory SHA-256
`63d0b2f1627212726f588e8a18423aa3072b2b1e59700ee0c3b50b9e96748dbe`. The
generic module SHA-256 is
`5608710839870914c5ddc007f5efbe5331453a1e560ef43f311060774f24dfc8`.

### Exact Lean declaration locators for `metric-provenance` (25 October 2026)

The existing `metric-provenance` result combines two distinct source claims:
the selected-action quotient coordinate in
`source:77d3ab6059bd1a3ce48637b97b9f30aa8825fc5f:02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md#L16: A. The selected finite action already owns a nonlinear metric carrier`
and the flat Einstein-detector tangent in
`source:77d3ab6059bd1a3ce48637b97b9f30aa8825fc5f:02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md#L48: B. The #201 Einstein detector differentiates that genuine metric quotient`.
Both immutable source pins verify; the section keys remain C0 candidates pending
unit review. No exact `claims.csv` ID or declared application edge currently
binds this result.

The Lean evidence in the existing result now pins
`03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean` at
`4aff58affff315eae09572640166b90cb0e5bdde` (SHA-256
`6234a6480aad6ca2a78caa3a64f59def4c50dc38beeb3c8ab1cc3df94c6db3cb`) and
names two exact declarations. The rebuilt public `D0.All` inventory resolves
both in that pinned module:

- `D0.Geometry.coframeMetricReadout_realizes_symmetric` constructs a finite
  coframe whose site readout equals any symmetric Role matrix `q`.
- `D0.Geometry.solderMetric_realizes_symmetric_tangent` constructs that
  coframe and proves the all-site finite path expansion, retaining its exact
  quadratic remainder and the corresponding difference quotient.

These declarations formalize the finite tangent calculation only. They do not
prove that the selected star action chooses this quotient, identify its
variation with the #201 Einstein detector, or close the global connection
equations. The result's broader source-to-Lean relation therefore remains
unresolved. The inventory records 173 declarations over the shared Gram API
and its three consumers; this result's source module contributes 102. The
selected declarations report `Classical.choice`, `Quot.sound`, and
`propext`; full proof and type dependencies are retained in
`sources/d0_proof_architecture_formalization_2026-10-24/finite_gram_tangent_inventory_2026-10-25.json`
(snapshot `4aff58affff315eae09572640166b90cb0e5bdde`, Lean digest
`6ff55724920a14097e3a4078050c6e8f1f2b15ba6e98aca48623d6691a6e7c40`,
collector SHA-256
`38cf062919c9e100b58cd8800f81f03ea03d26200fe3f9d414d0ed5de74150a7`,
`worktree_dirty=true`, and inventory SHA-256
`9deeb9580efce0a6fc93a07aba9b171ab07d586ce5f88a2ee60b6a73053cdd88`).

`proof_architecture.py crosswalk` now checks explicit `declaration_names`
against the pinned current module and stores the elaborated types, proof
dependencies, and axiom footprint. Its regenerated all-result view records
`all_resolved` for these two names while keeping the module-wide declaration
set `ambiguous`, claim locator `unresolved`, semantic relation `unresolved`,
and `acceptance_inferred=false`. It contains all 54 active results at snapshot
`4aff58affff315eae09572640166b90cb0e5bdde` (`worktree_dirty=true`, Lean digest
`6ff55724920a14097e3a4078050c6e8f1f2b15ba6e98aca48623d6691a6e7c40`,
collector SHA-256
`5e9074769ba45eb74e6ade808f9aaac82dd09454e14941d6aea6c7885051b0f1`, proof
detail collector SHA-256
`1899bd10c2928a66d4b961f5b4d12a884b6d721f30bcc187ffcfe02c0f07830a`). The
refreshed crosswalk SHA-256 is
`7a16ee71fefd69d3cd5cc8807c2a514acfa393f3b48a41c029d278c3b6d0c0df`.
The 40 proof-architecture tests pass, and `gr_assembly.py check` remains valid
with scientific promotion false. This is one source-keyed candidate
reconciliation, not an accepted C0 package or coverage claim.

## Scientific boundary and reuse vertical

This work does not select a physical implementation or close GR. Keep complete Book03/Cost-Info/source admission, same-execution clock/controller/work selection, physical metric descent/frame selection, original H+J+R, positive_gr, and raw216 open under their existing owners. Preserve #334; do not duplicate or retire its science. Conditional assumptions remain in theorem signatures. Connes reconstruction remains conditional when its needed object is a supplied field.

A useful cold-start reuse case is the native raising-operator inverse with a null leg: published #334 labelled-record source §§8.4-8.5, equations (26)-(31), with rational alternative §6.25 (13br1)-(13br2). Its selected source gate is satisfied at commit fe5cf335da04cac14e50407b03f98b96be17dc52, path 02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md, blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62. The concrete consumer is the exact AF radial coframe equivalence source §5.1, blob 734e21ae6bc04ff3446ad15858936d417fdd2e55. At the earlier vacuum-only checkpoint, `D0.Geometry.ArchiveJuliaRaisingOperatorReadout` had an exact exterior vacuum readout and a CAR adapter for the owned Jordan--Wigner `carCreateEnd` matrices; it proved the Eq. (26) shift identity but not full-query equality or the null inverse. The 24 October continuation below now supplies complete query equality and the finite-carrier null-block inverse under its explicit endpoint-form, chart and branch assumptions. The all-jet extension, coframe/metric recovery and variational pullback (31) remain open. No physical price, compiler, admission or GR-selection result follows; the fuller consumer remains conditional on its stated assumptions.

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

At that checkpoint, the next work was to reconcile the exact-name inventory with source-keyed mathematical units and dispositions, obtain independent acceptance of the exact C0 package, and continue the remaining established mathematical migrations. The 24 October checkpoints below record the refreshed 13-case cold-start suite, compiled claim-reuse examples, shared Vieta migration, and current `D0.All` build. The reviewed Eq. (26) application covers the finite-carrier vacuum response; all-state operator comparison, endpoint-field binding, the §§8.4–8.5 inverse, and the §5.1 consumer transport remain with their existing owners. Migrate connected mathematical blocks while preserving public imports and scopes; formalize or obtain accepted owner review for every established C0 unit. This checkpoint is not completion.

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


### 25 October complete assembly-source locator refresh

The refreshed `crosswalk --all-current` output contains every one of the 54
assembly-result rows and all 190 source records. An exact
`source:<commit>:<path>` file key is emitted only after the immutable Git blob
matches its recorded SHA-256. A verified historical pin remains usable if its
file is missing or changed in the current checkout; an unavailable blob or
digest mismatch yields no exact key. These are provenance locators, not C0
mathematical units.

Of the 190 source pins, 181 verify, eight pinned blobs are unavailable, and
one recorded SHA-256 mismatches its commit/path blob. Current checkout status
is 70 matches, 112 missing files, two changed files under verified historical
pins, and six files whose pin is unverified. The digest mismatch remains
recorded for `orthogonal-exit-conditional-gram-einstein-source-ratio`, path
`02_REGISTRY/research/A4D_NATIVE_ORTHOGONAL_EXIT_DOUBLE_CLOCK_EINSTEIN_SOURCE_2026_10_17.md`;
the expected and observed blob hashes remain visible in the generated JSON.
The eight unavailable objects are listed individually there. No expected hash
was rewritten.

Fifteen evidence records now have explicit section references for fifteen result
rows: `phase-count-counterexample`, `brinkmann-j2-null-family`,
`original-golden-inverse-pf-moving-mean-j2`,
`two-line-full-julia-car-observability`, and the eight existing double-null results
`double-null-cubic-uniform-control`,
`double-null-cubic-polynomial-chart-obstruction`,
`double-null-continuum-fourth-order-ricci-jet`,
`double-null-finite-cubic-euler-jet`,
`double-null-finite-quartic-selected-cubic-branch-obstruction`,
`double-null-finite-mixed-quartic-euler-jet`,
`double-null-finite-asymmetric-quartic-euler-jet`, and
`double-null-degree5-selected-rref-ward-obstruction`. Each locator names an exact heading coordinate in its pinned source. An independent read-only reviewer
verified all twelve pins, hashes, and heading coordinates, and checked that
each section supports its result statement at the recorded scope. The locators identify source sections only; they do not establish C0 membership,
semantic acceptance, or closure of a parent application. The
independent read-only review also checked each section against its exact
assembly-result statement and recorded the following scope boundaries:

| Result | Supported statement and retained boundary |
|---|---|
| `phase-count-counterexample` | The witness `(-1,-1,i,i)` has rank 22 and nullity 2 where the proposed phase-count rule predicts 4. This refutes that rule; it does not classify the full divisor or its rank strata. |
| `smooth-parametrix` | The fixed smooth realization has Fourier-tail, normal-center, summable-remainder, and uniform IR-parametrix controls. A refinement-uniform coupled normal rescue remains unresolved, so the Einstein operator statement is conditional. |
| `original-stage-resolved-book-selector-143484` | The full two-depth, stage-labelled 143,484-event record recovers attempts, acceptances, the shared verifier, closed-path weights, the absolute Book action modulo 32 endpoint similarities, and its source jets. The event record and inverse are pinned in adjacent sections. The shared positive verifier is a substantive hypothesis; this does not identify the full H+J+R cost or establish physical selection. |
| `metric-provenance` | Sections A and B support the exact nonlinear quotient coordinate `Q=Theta eta Theta^T` and the owned Einstein flat-metric tangent. Global all-mode connection elimination remains obstructed. |
| `brinkmann-j2-null-family` | On the declared six-plaquette Lorentz-star family, all 16+24 geometric rows reduce to three, with the link equations fixing the one-u-step connection and the remaining equation a transverse Poisson equation. The composed corrected two-tick Golden AF×scene J2 gives the stated finite roots and smooth Einstein-scalar family. This is a mathematical AF-star instrument result; compulsory foundational D0 selection and the original fixed-g/tau raw terminal remain open. |
| `original-golden-inverse-pf-moving-mean-j2` | On original golden-box addresses with true nonuniform weights, the specified inverse-PF and moving-volume operand of the same two-tick AF×scene J2 transfers Brinkmann roots with exact finite first-source equality and yields the conditional off-null mean source. The original weights, source-compatible factor, moving-volume map, and J2 are hypotheses; physical programme selection, full H+J+R/clock/preparation Euler, and raw #216 remain open. |
| `two-line-full-julia-car-observability` | For two specified grade-one CAR16 probes, the complete positive Julia GOOD/BAD instrument gives a nonsingular six-by-six Jacobian from the original proper-Lorentz directions to unconditioned CAR responses, with determinant `1/373248`. The result is local and does not select probes, measurements, or their cost, or identify the response with the full Book action or Palatini link Euler. |
| `double-null-cubic-uniform-control` | For the fixed coframe, a site-independent cubic correction fails at the origin and adjacent node for `[a²b]` and `[ab²]`. Spatially varying corrections, lower-order coframe modes, and a full root remain open. |
| `double-null-cubic-polynomial-chart-obstruction` | A degree-at-most-two spatial polynomial correction chart is inconsistent at `[a²b]`. Arbitrary lattice corrections, higher-degree corrections, other branches, and physical selection remain open. |
| `double-null-continuum-fourth-order-ricci-jet` | The continuum jet supports the `k=3/1024` cancellation and harmonic area radius through degree four for the stated arbitrary orthogonal slopes. It establishes no finite Euler solution, all-order root, or native D0 selection. |
| `double-null-finite-cubic-euler-jet` | On `H=a*x, J=b*y, h=1`, site-dependent degree-at-most-three corrections solve the specified Euler coefficients through total amplitude degree three. Higher orders, arbitrary slopes, refinement, sources, and full Cost-Info selection are not proved. |
| `double-null-finite-quartic-selected-cubic-branch-obstruction` | For the selected cubic representative with free parameters set to zero, no degree-at-most-five spatial-polynomial quartic correction solves `[a²b²]`. Other cubic representatives and correction classes remain open. |
| `double-null-finite-mixed-quartic-euler-jet` | In the checked truncated ring, the selected joint cubic/free-mode solution includes the `[a²b²]` correction. Pure cubic coefficients, all-order behavior, arbitrary slopes, refinement, and physical selection remain open. |
| `double-null-finite-asymmetric-quartic-euler-jet` | The selected branch supports the 13 retained coefficients, including `[a³b]`, `[ab³]`, and `[a²b²]`. It is not a complete fourth-order jet; `[a⁴]`, `[b⁴]`, `[a³b²]`, `[a²b³]`, and `[a³b³]` are unchecked. |
| `double-null-degree5-selected-rref-ward-obstruction` | Nonzero fifth-order Ward projections rule out extension of the one selected RREF representative. Other lower-order free modes may change the source; this is not a general crossed-null obstruction or GR closure. |

These are evidence-to-result matches with explicit mathematical scope, not
accepted C0 dispositions or result-to-parent applications. The assembly
registry makes these fifteen results C0 candidates; independent acceptance of
the C0 denominator and dispositions remains pending.

For verified pinned Markdown sources without an explicit section locator, the
view ranks up to three heading candidates by lexical overlap with the
assembly-result statement. Candidate records contain matched terms, overlap
fraction, and the exact pinned line/heading coordinate, and remain labeled
`unreviewed_lexical_candidate`. The current output contains 151 ranked
suggestions across 37 result rows; 39 result-to-unit mappings remain
incomplete. Independent read-only review checked the earlier 178 ranked
candidates against 59 unique pinned Git blobs; the current 169 are a subset.
The reviewer also recomputed the 54-result/190-evidence summary. These checks
validate locator provenance and output integrity only. All 54 semantic result
relations remain `unresolved`, and `acceptance_inferred` is false for every
row.

The regenerated artifact
`sources/d0_proof_architecture_formalization_2026-10-24/assembly_result_declaration_crosswalk.json`
was built from clean snapshot
`938166589cd5f95e2fbb94e5591d9de3b8ccaaab`; its SHA-256 is
`040dccf0c6ea8b85585341a3ee9a79a87fc18fe3929eb8051f2541fffb35ae2c`.
Its `D0.All` pass enumerates 899 co-located declarations in nine current
modules. Lean source digest
`e2d01817a8f7a3c11b64f0e84a9a44aa58e82304715793c0fb95ddffcbae4dae` and the
collector digests are recorded in the JSON. The output has no truncated
result lists. C0 remains unfrozen and independently unaccepted; these counts
do not establish coverage.


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
name `archive_naive_weighted_degree_leakage_nogo_owner` now resolves through a
compatibility wrapper to an exact finite witness in the existing CAR16
cubical differential. At refinement `N = 1`, the profile is `w = 4` at the
intermediate `A` site and `w = 1` elsewhere; a scalar delta at the `A+B` site
produces coefficient `1` in the degree-two `A∧B` component at the origin after
two `sqrt(w)`-weighted steps. The theorem proves this one case and does not
establish the registered universal no-go for every nonconstant profile or the
claim that geometry must enter only through the Hodge metric. The registry
claim row, status, and scientific owner are unchanged; this formal result is
scoped evidence and does not independently accept the broader wording. The
older `weighted_degree_scope_inventory.json` remains a historical snapshot of
the preceding source and must not be used as current-source evidence.

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

This also updates one input to the earlier E-CARHODGE route in
`A4D_CAR_HODGE_METRIC_ACTION.md`: that memo identified the absence of a literal
finite cochain differential as its first blocker. The finite operator and its
unit-step nilpotency adapter now exist in the compiled library. This changes
only that finite premise; the metric-dependent exterior weight `W_m`, weighted
adjoint, full Hodge action and variation, and centered Cartan/Ward compatibility
remain open. The original research owner and its broader scope remain intact.

Local validation for the operator package passed: narrow build of
`D0.Geometry.ArchiveWeightedHodgeDirac` (2,986 Lake jobs), exact claim reuse
through `D0.All`, generated-view check (`stale=0`), formalization-debt
non-growth (3 findings, baseline 3), and diff check. GitHub `D0 Lean build`
run 2994 and `D0 guards` run 5032 both succeeded on code commit
`23f9f5c7093386a30c87386353d06ae03dace9b6`.

## Hodge degree-preservation and diagonal-adjoint applications (24 October 2026)

The registered `D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001` module previously exposed
degree preservation only as `DegreePreservingLaplacian true`. It now also
contains a concrete package for the existing finite operators: the normalized
unit-step coboundary has square zero, `hodgeCarDirac²` preserves homogeneous
Fock degree, and `hodgeCarDirac` is self-adjoint for the counting pairing. The
degree proof applies the owned `hodgeCarDirac_sq_fibre` identity, whose scalar
difference Laplacian acts independently on each fixed Fock component; the
self-adjoint result reuses `hodgeCarDirac_self_adjoint`. The number of degrees
is now derived as `Fintype.card Role + 1 = 5` rather than introduced as a bare
constant.

The geometric weight operator `W_m` derived from a coframe or metric and the
conjugated positive-Hilbert self-adjoint representative remain unconstructed.
The module now also applies a generic finite algebraic adjoint to the existing
`hodgeCarDirac` for an externally supplied nonzero diagonal cochain profile.
That pairing need not be positive, and this result does not derive the actual
geometric profile. The legacy Boolean field remains visible as a scope
limitation, and the weighted claim's source and semantic C0 review remain open.
No claim status, owner, physical assumption, or Hodge-metric selection is
changed.
`formal_support.csv` records the concrete consumer edge from
`ArchiveHodgeCARDiracSquare` to this application.

The compiled reuse record and declaration inventory are refreshed below for
the current owner type. The locator resolves through `D0.All`; the elaborated
owner type contains the zero-square, degree-preservation, counting-pairing
self-adjointness, and arbitrary nonzero diagonal-weight adjoint conclusions.
The full axiom footprint remains recorded in the current inventory.

The reusable algebra module `D0.Algebra.FiniteWeightedAdjoint` defines, on any
finite coordinate type over a field, the bilinear pairing
`Σ_i w_i x_i y_i` and its coordinate adjoint
`(A†_w y)_i = w_i⁻¹ Σ_j w_j A(e_i)_j y_j`. Its theorem proves the adjoint
identity for every linear operator when each `w_i ≠ 0`; it does not assume
positivity. The application module defines
`hodgeCarDiracDiagonalAdjoint` from the existing linear map `hodgeCarDiracₗ`
and includes the all-refinement identity in
`archive_weighted_hodge_dirac_owner`. `formal_support.csv` tracks the generic
module's actual consumer, and the generated public import `D0.All` imports the
new support module directly.

The exact module inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_hodge_adjoint_module_declarations.json`
(SHA-256 `0ae014de540605926765d158ce5850fc5396b67922a746e161ce2ee5b1d9a865`).
It enumerates 21 declarations from the generic and application modules under
Lean 4.30.0 and public import `D0.All`; it records Lean source digest
`692151ba3f36ceb30848a89d1eec5cc738fc68ca1944ebb2e42e7adea2e5576a` and
collector SHA-256
`ec3a29823eea0ff27ddde532d985c732063b796f1ba08052702f103a494d6300`.
The compiled claim-reuse record at
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_hodge_claim_reuse.json`
has SHA-256 `7e259243d104ca5294e921b1cce34d8ae4cdfff53a88cd31500f9c1d98472683`.
Its owner type includes the arbitrary nonzero-weight identity; the elaborated
proof dependencies include `hodgeCarDirac_diagonal_weight_adjoint` and the
generic `finiteWeightedPairing_adjoint`. The generic adjoint theorem's axiom
closure is `Classical.choice`, `Quot.sound`, and `propext`; the owner retains
its existing CAR `native_decide` dependencies as recorded in the full
inventory. Both machine-readable records bind the current source digest above
and report the pre-publication local snapshot `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`
with `worktree_dirty=true`.

The final local `lake build D0.All` passed (4,565 jobs), rebuilding both the
generic adjoint module and its Hodge consumer on the final Lean source. The
inventory and reuse extraction also compiled through `D0.All`; the Hodge
source remains conditional on the supplied weight and has no physical or
metric-selection interpretation.

## Exact finite weighted-differential leakage witness (24 October 2026)

`ArchiveCubicalCoboundary` now owns the reusable operator
`weightedCubicalDifferential N w ψ = sqrt(w) · dψ`, with arbitrary refinement
and real-valued site profile. The no-go module keeps
`naiveWeightedCubicalDifferential` as a compatibility specialization at
`N = 1` and its registered sample profile. On the fixed full CAR16 carrier,
the selected two-step coefficient for the scalar delta at `A+B` and output
state `A∧B` is exactly
`sqrt(w(origin)) * (sqrt(w(siteA)) - sqrt(w(siteB)))`. The positive-output
weight and unequal-intermediate-root corollary gives a reusable sufficient
condition for nonzero leakage on this path. For the explicit profile with
weight `4` at the `A` intermediate site and `1` elsewhere, the degree-zero
input yields coefficient `1` at the origin in a degree-two state. The proof
reduces the full role/state sums using the existing CAR support theorem and
exact integer-shadow creation coefficients; it does not use floating-point
evaluation. The shared module also proves that every constant profile remains
nilpotent at every refinement by linearity of the base coboundary, and that an
arbitrary site profile preserves one-step Fock-degree raising. The concrete
two-step output is homogeneous of degree two, with the coefficient formula
showing it is nonzero for the registered nonconstant profile; a unit-profile
control consumes the all-level nilpotency result beside that sample.

The registered locator `archive_naive_weighted_degree_leakage_nogo_owner`
now compiles as a compatibility wrapper to the existing
`archive_naive_weighted_car_degree_leakage_nogo_owner`. The wrapper's
elaborated type contains the finite profile, degree-zero input, degree-two
output, and exact coefficient `1`. This resolves the exact name locator; it
does not validate the broader claim-row wording that every nonconstant
weight breaks nilpotency or that geometry must enter only through the Hodge
metric. The claim row, `LEAN_PROVED` label, and scientific owner were left
unchanged. The broad semantic claim remains for review by its existing owner.

`formal_support.csv` now records the source chain from the BOOK_06 locator to
the cubical coboundary and the no-go application, and lists the no-go module as
a consumer of `ArchiveCubicalDifferential`.

The compiled declaration inventory for both linked modules is preserved at
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_module_declarations.json`
(SHA-256 `de5bb040a9089618a003e00c764cd2a03f61bdecc0d77121f86b72da0272a40f`).
Under public import `D0.All` and Lean 4.30.0 it records the exact signatures,
proof dependencies, source ranges, and axiom footprints for the shared
operator, the generic coefficient formula, its nonzero corollary, the
constant-profile theorem/control, the arbitrary-profile degree-raising
theorem and its concrete two-step application, and the registered owner
theorem. The owner theorem now consumes the formula-based exact sample, the
general nonzero criterion, and the result that its complete two-step output is
homogeneous of degree two. That application depends on the arbitrary-profile,
all-refinement degree-raising theorem, so the exact coefficient `1` belongs to
the complete degree-two output rather than only to a labelled component.
The inventory binds Lean source digest
`c092c246193023d8047b698d7cb62bb9c70f625c62424a41856353cd1eed0964` and
collector SHA-256
`db0648931c63054d7e9ba4546790035d61d76fc0b4e20c190794c99f197f9104`.

The compiled claim-reuse record is
`sources/d0_proof_architecture_formalization_2026-10-24/naive_weighted_leakage_claim_reuse.json`
(SHA-256 `be5aba779b5acf3526276bd28794cecc72bbe6fe3faf2c400075936281d93491`).
The exact theorem locator resolves through public import `D0.All`; its
elaborated proof dependency is the scoped CAR owner theorem above, whose
compiled type includes the complete degree-two output and whose dependencies
include the generic weighted degree-raising result. The reuse record was
queried at local source snapshot `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`
with `worktree_dirty=true`; the inventory's Lean source digest above binds the
actual Lean contents. The transitive axiom footprint includes
`Classical.choice`, `Quot.sound`, `propext`, and existing CAR
`native_decide` results for CAR support, singleton-vacuum behavior, degree
raising, the finite pair degree, and the two creation coefficients; no
axiom-free claim is made.

Validation for this slice passed: narrow build of
`D0.Geometry.ArchiveNaiveWeightedDegreeLeakageNoGo` (2,976 Lake jobs), compiled
claim reuse through `D0.All`, generated-view check (`stale=0`), formalization-
debt non-growth (3 findings, baseline 3), and `git diff --check`. No physical
Hodge metric, universal weight obstruction, GR premise, claim status, or
scientific owner is selected or closed by this finite example.

An independent read-only scope review of PR head
`52eee9d7668ed3849b809b1f61f9a118355e5e44` supports the arbitrary-profile
degree-raising result and the registered `N=1` complete-output application.
The review did not build the sources and did not accept C0 or the broader
scientific claim. It identified the two omitted CAR axiom entries for support
and singleton-vacuum behavior; the full inventory already recorded them, and
the summary above now names them explicitly. The broad registry wording and
status remain with the existing owner.

## Finite weighted-adjoint composition and Hodge-square application (24 October 2026)

The generic finite weighted-adjoint module now also proves uniqueness from
the adjoint identity for a nowhere-zero diagonal profile and the composition
law `(A ∘ B)† = B† ∘ A†`. The uniqueness proof uses the coordinate-basis
pairing and the nondegeneracy supplied by the nonzero weights. No positivity
or inner-product structure is assumed.

The Hodge/CAR consumer applies this law to the square of its existing linear
operator: for every refinement and every supplied nonzero diagonal profile,
the weighted adjoint of `hodgeCarDiracₗ.comp hodgeCarDiracₗ` equals the
composition of its two diagonal-weight adjoints. This composes the generic
algebra result with the registered finite Hodge operator. It does not derive
the geometric profile, a positive metric, or the physical Hodge action.

This is the latest inventory for the preceding Hodge application; it
supersedes the earlier 21-declaration inventory and reuse hash recorded
above. The compiled inventory at
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_hodge_adjoint_module_declarations.json`
has SHA-256 `011f65653ca29a5390a09fd6ea606d22edb6ade79448cb712f77e2fe32aa7bf2`,
enumerates 27 declarations through public import `D0.All`, and records Lean
source digest `aaab156c8747604c76004ecda7d7ec82a3e24094449100592dfe853cd0e39231`,
collector SHA-256 `ec3a29823eea0ff27ddde532d985c732063b796f1ba08052702f103a494d6300`,
and Lean 4.30.0. The refreshed compiled reuse record at
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_hodge_claim_reuse.json`
has SHA-256 `f046b794ea8a123c8fc7b86d3228ff51f5e0196614c32a6aa85987cb8501863c`;
its elaborated owner type includes the new Hodge-square application. The new
generic composition and uniqueness declarations have axiom closure
`Classical.choice`, `Quot.sound`, and `propext`; the registered Hodge owner
retains its explicit CAR `native_decide` footprint. These records describe
the pre-publication source snapshot `6b59bc57ca97275df9e973715cdb503ec8fc5c4e`
with `worktree_dirty=true`; the Lean source digest binds the exact compiled
contents.

Validation for this slice: the narrow Hodge target built successfully through
2,988 Lake jobs. The final `D0.All` integration on this expanded source is
still required before the checkpoint is ready. C0 remains unfrozen and
independently unaccepted, and the existing scientific and physical owners
remain unchanged.

## Bounded search-card regression (24 October 2026)

A real query for `weighted adjoint composition Hodge` exposed that the CLI
returned more than 1,000 formatted lines despite ranking only five text
candidates, because it repeated long evidence and reference lists. Search now
renders at most three evidence lines and three exact source references for
each candidate, with omitted counts and source-file digest retained. The full
evidence remains available through the exact source and `show` view; ranking,
pins, and mathematical status do not change.

The same query now returns five text candidates in 13,412 characters and 358
formatted lines; the leading direct-content candidate is
`03_FORMALIZATION/D0/Geometry/ArchiveWeightedHodgeDirac.lean`. The focused
`tools/test_proof_architecture.py` suite passed 35/35, including a new bound
and source-pin preservation regression. This is an output-size correction,
not semantic acceptance of the text candidate or its scientific claim.

## Conditional cubical weighted Hodge-Dirac application (24 October 2026)

The finite weighted-adjoint API now includes the symmetric bilinear-pairing
identities, the equivalent right-adjoint identity, nilpotency transfer to the
adjoint, and degree support for its lowering action. For a finite coordinate
space and any caller-supplied pointwise-nonzero diagonal profile, the generic
operator `A + A†_w` is self-adjoint for that bilinear pairing. When `A² = 0`,
its square is the anticommutator `A A†_w + A†_w A`; when `A` raises the supplied
grading by one, this square preserves each grade. These are algebraic results
for a nondegenerate pairing and do not assume positive weights.

The cubical module now exposes the normalized registered coboundary as a
linear map, retaining its existing nilpotency and degree-raising proofs. The
Hodge consumer constructs `d + d†_w` from that coboundary itself, and the
compiled application `D0.Geometry.cubicalWeightedHodgeDirac_application`
bundles bilinear self-adjointness, the Hodge anticommutator identity, and
form-degree preservation of the square for every refinement and every supplied
nonzero profile. This closes the earlier gap where the weighted-adjoint
composition law was applied only to the already-composed unweighted CAR
operator. It still does not derive a positive, canonical, or geometric weight,
a standard-Hilbert self-adjoint representative, or physical Hodge selection.

The existing claim row
`D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001` now lists both
`archive_weighted_hodge_dirac_owner` and
`cubicalWeightedHodgeDirac_application` as theorem-name locators. Its existing
`LEAN_PROVED` and `CORE-FORMALIZED` fields are unchanged; the row's scope note
states that these locator strings are not independent semantic acceptance of
the stronger canonical or physical properties. `generate_lean_views.py`
regenerated `TheoremLedger/ClaimMap.lean`; only this row's theorem-name string
changed. No claim or assumption ID was added, and C0 remains unfrozen and
independently unaccepted.

The 82-declaration module inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_module_declarations_current.json`
(SHA-256 `7804f70e072b6fbbef10ee12b876a3a47f471a456a303c9ed3c7a85d8fe39ae5`).
It was collected through public import `D0.All`, at source snapshot
`91dd15ac621c7241dcc0255184569c7361eb1002` with `worktree_dirty=true`; the
normalized Lean source digest is
`8a5fbd369001be5d17860b56f141e6a6994e8b7c44e1a6d0e8012b69f330314f`, and the
collector SHA-256 is
`48f6a0da41a6c15222a97463851f43b3d7db651e3ac42868031574bc52e09f38`. The
exact claim-reuse view is
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_claim_reuse_current.json`
(SHA-256 `72372e889bccb5256319573874cc590db3b31e9f7562a7864c0c14908127a6fd`);
both claim locators resolve to elaborated declarations through `D0.All`, and
the application proof dependencies include the generic self-adjointness,
square, and grading results together with the registered cubical nilpotency
and degree-raising results. The application inherits `Classical.choice`,
`Quot.sound`, `propext`, and the existing CAR `native_decide` results for
creation degree raising and the creation anticommutator; no `sorryAx` is
reported.

Validation: the three edited Lean modules compile with Lean 4.30.0, and a
temporary OLean overlay compiled all 21 PR-changed Lean modules, six
cache-missing dependencies, and current `D0.All` against the preserved local
Mathlib cache. This validates the current-source integration but is not a
fresh Lake build: unchanged imports reuse their cached OLean files, so the
clean CI `D0.All` build remains the publication gate. The generator check
(`python3 tools/generate_lean_views.py --check`), ClaimMap coverage under
Python 3.12, the debt audit (`python3 tools/formalization_debt_audit.py --check`;
3 findings, baseline 3), and `git -c core.whitespace=cr-at-eol diff --check`
pass. The CRLF-aware setting matches the committed generated ClaimMap line
endings. No scientific owner or release status was changed.


### Published cubical weighted-Hodge checkpoint (24 October 2026)

- Commit `3cbd6033583e3eb52769aa53c72cc1754dc20480` publishes the conditional `d + d†_w` application on the existing Draft PR #402. The PR remains open and Draft; no merge or readiness transition was performed.
- GitHub `guards` completed successfully on this head (run `40115181286`). `lean-build` also completed successfully (run `40115181248`), but its log explicitly says `Draft PR: full D0.All is deferred until ready_for_review`; this is not a remote full Lean build.
- The local current-source integration compiled all 21 PR-changed Lean modules, six cache-missing dependencies, and `D0.All` through Lean 4.30.0 using a temporary OLean overlay and the preserved local Mathlib cache. Unchanged imported modules reused cached OLean files. The exact module inventory and claim-reuse artifacts above bind the compiled source digest and axiom footprint.
- A clean CI `D0.All` build and independent semantic acceptance remain pending. The weighted-Hodge application remains conditional on pointwise-nonzero supplied weights and does not select positive or geometric weights. C0 remains unfrozen and independently unaccepted; existing scientific owners and statuses remain unchanged.

## Positive-profile comparison specialization for cubical Hodge (24 October 2026)

The generic diagonal pairing now has a positive-definiteness theorem: for any
finite coordinate type and any caller-supplied pointwise-positive real profile,
`x ≠ 0` implies `finiteWeightedPairing w x x > 0`. The concrete cubical
Hodge-Dirac module applies it to `ArchiveCochainBasis N` and packages that
result with self-adjointness of the existing `d + d†_w` operator for the same
positive comparison profile, at every refinement. The signed-profile Hodge
square and grading results remain in the existing application.

This positive profile is an auxiliary comparison form. It is not the
Lorentz-induced Hodge profile in `A4D_CAR_HODGE_METRIC_ACTION.md`, whose
finite exterior pairing is indefinite with signature `(8,8)`. No positive or
geometric metric weight is constructed, and this does not establish a
standard-Hilbert representative or physical Hodge selection.

The existing claim row
`D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001` now lists
`cubicalWeightedHodgeDirac_positive_profile_application` as a third exact
theorem-name locator. Its `LEAN_PROVED` and `CORE-FORMALIZED` fields, owner,
assumptions, and claim ID are unchanged. The locator records a conditional
compiled application and does not independently accept the broader canonical
claim or C0 membership. `formal_support.csv` now points the Julia readout
module to this current artifact because its older `referenced_by` path was an
unmerged source file; the Lean module itself now records the source and
consumer commit/path/blob pins directly.

The compiled declaration inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_positive_profile_module_declarations_current.json`
(SHA-256 `6cb3ded2b09a15a0121b015a03ed6ba22f105edc411376e24c9e11d58ec584e2`).
It enumerates 84 declarations in the finite weighted-adjoint, cubical
coboundary, and weighted Hodge modules through public import `D0.All`, at
Lean source digest `3f8df9fb7950c123c2c665de47937cb43b90b796c89c0c445e7a14bf68363126`
and collector SHA-256 `48f6a0da41a6c15222a97463851f43b3d7db651e3ac42868031574bc52e09f38`.
The refreshed claim-locator record is
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_positive_profile_claim_reuse_current.json`
(SHA-256 `f5d1833f8aad3bc340773050457ff77886998c459c32efab20f9a1d991e5b256`),
collector SHA-256 `24ba74141d67ee3f9b2474dca339fc333d559c6c29774e4b40e36aa38a670c50`.
It pins the exact input authority bytes: `claims.csv` SHA-256
`b0165dbcd3bd558f81506fe8b77b8c16c989448dea20341e61dfbc200833c6b5`,
`formal_support.csv` SHA-256
`60e86d55dc9919bfbb51a44de4844fd93e13b0a462e1b0e554b754877cf11f31`, and
the generated ClaimMap SHA-256
`c8602c403e359d421c7b34e2a7ebeb5b3c65996c8cfedd3ba5d6368bc0aeace2`.
All nine generated candidate names were answered; the three exact registered
locators resolve through `D0.All`. The new application depends on the generic
positive-definiteness theorem and the registered cubical operator's
self-adjointness theorem, with transitive axioms `Classical.choice`,
`Quot.sound`, and `propext`; no `sorryAx` or `native_decide` appears in this
new theorem's closure.

Validation: Lean 4.30.0 compiled the changed generic pairing module, the
cubical weighted-Hodge owner module, the updated Julia readout module, and the
current `D0.All` into a temporary OLean overlay using the preserved local
Mathlib cache. Unchanged imports reused cached OLeans, so this is not a fresh
Lake build. `generate_lean_views.py --check` passes with `stale=0`; ClaimMap
coverage passes; `formalization_debt_audit.py --check` reports 3 findings,
matching the baseline of 3; `test_proof_architecture.py` passes 35/35 and
`test_lean_declaration_inventory.py` passes 14/14. The CRLF-aware diff check
and the changed `formal_support.csv` path check also pass. The current source
remains unmerged in Draft PR #402; clean remote `D0.All` and independent
semantic acceptance are still pending. C0 remains unfrozen and unaccepted.

## CAR/exterior role-order alignment and full basis-state creator action (24 October 2026)

The finite exterior lift had been ordered by `roleCode` from the role-pair
metric carrier (`A,C,D,B`), while the owned Jordan–Wigner matrices count
preceding occupations using `roleOrderIndex` (`A,B,C,D`). The vacuum-only
readout does not expose this sign difference. The exterior lift, affine-matter
lift, and Julia readout now all lift `roleOrderIndex`; the exterior module no
longer imports the unrelated pair-metric carrier just to obtain an order. The
duplicate injectivity proof in `RoleFockPermutation` now references the shared
`ArchiveCARRelations.roleOrderIndex_injective` theorem.

`carCreateEnd_single_state` now states the CAR creator's action on an arbitrary
occupation basis state: occupied target modes are killed, and unoccupied
target modes are updated with the Jordan–Wigner phase. Its auxiliary proof
records that adding the target occupation leaves the number of *preceding*
occupations unchanged. This characterizes the CAR creator on all 16 basis
states and makes its sign convention explicit. It does not by itself prove
equality of the complete CAR and exterior creator operators on non-vacuum
states; the registered Julia CAR/exterior query equality remains the vacuum
statement. Equations (27)–(28), Lorentz-null inversion, full coframe or metric
recovery, variational/source/price maps, physical selection, and `GR_closed`
remain outside this formal result.

Validation: the five changed Lean modules and the current `D0.All` import root
compiled with Lean 4.30.0 into the temporary
`/private/tmp/d0-pr402-lean-overlay`, with unchanged imported modules resolved
from the preserved checkout cache. This is an overlay integration compile, not
a fresh `lake build D0.All`; the passing PR #402 CI runs are from the preceding
head and do not validate this unpushed change. `#print axioms` for both
`carCreateEnd_single_state` and the shared order-injectivity theorem reports
`propext`, `Classical.choice`, and `Quot.sound`. The broader C0 freeze and
independent acceptance remain open.

Changed Lean-source SHA-256 values: `ArchiveCARRelations.lean`
`44336838c34198e0df0680e075f7795fe0957602f6dd23c3458117f4b59661df`,
`A4DNilpotentAffineMatterLift.lean`
`edb86401f1efd8c1ab55020dd29ecf31a7248a91a34eb247bfb4d66f35c7f69a`,
`ArchiveExteriorFrameLift.lean`
`fbc55f53e75657b96f11a7752d973198df35b6542937ab636b86d104bdbda5ee`,
`ArchiveJuliaRaisingOperatorReadout.lean`
`c609cac95402f1c477b77b5029406be1ecf0198103fd077736660405d3586d4a`, and
`RoleFockPermutation.lean`
`e36d3751b7aa4ebfcea135e8e5a1fc1659296ee7b2299e38fa5eee380016f3fd`.

## Complete CAR/exterior creator and Julia-query equality (24 October 2026)

This checkpoint supersedes the preceding statement that all-state operator
comparison remained open. `carCreateEnd_exterior_basis` proves, for every one
of the four roles and every one of the 16 occupation labels, that the existing
Jordan--Wigner creator transported through `archiveFockExteriorEquiv` equals
left multiplication by the corresponding exterior basis vector. When the
target role is occupied, the exterior product is zero by the basis
anti-symmetry theorem. When it is empty, `basis_mul_of_disjoint` gives the
inserted subset and its permutation sign; `archiveCreatorPermSign` checks that
sign against `jwSignInt` over the exact finite four-role/state domain, and the
support update identifies the resulting exterior basis vector.

Linearity now yields `archiveCARVectorCreator_basis_exterior` on each of the 16
coefficient basis vectors and
`archiveCARVectorCreator_eq_archiveExteriorCreatorLM` for the entire linear
operator. Composing both creators with the same arbitrary linear frame lift
gives `archiveJuliaCARRaisingQuery_eq_model`; the older vacuum query equality
is now a direct specialization. This substitutes the prior finite-carrier
vacuum-only creator/query comparison in the pinned Eq. (26), §8.4 application
to its §5.1 consumer, for the exact existing carrier and frame map. It does
not yet transport that identity through the full coframe/metric recovery or
Lorentz-null inverse (27)–(28), and it establishes no variational/source/price
map, physical admission, or GR selection.

Trust boundary: `archiveCreatorPermSign` uses `native_decide +revert` for this
finite permutation-sign identity. `#print axioms` for the basis-state
creator, whole-creator equality, whole-query equality, and CAR-query shift
injectivity reports `propext`, `Classical.choice`, `Quot.sound`, and the
generated `archiveCreatorPermSign._native.native_decide.ax_1_1` certificate
axiom. This is not a kernel-only or arbitrary-mode proof. No `sorry` or
`admit` is used.

Validation: the changed Julia module and current `D0.All` import root both
compiled from this worktree's Lean sources with Lean 4.30.0 into
`/private/tmp/d0-pr402-lean-overlay`; imports were resolved from the preserved
checkout's pinned Lake package cache and the prior overlay for unchanged
modules. This is a narrow module plus import-root overlay integration compile,
not a fresh `lake build D0.All`. The public declaration collector's generated
Lean query, run directly against this compiled overlay import root, resolved
the three new theorem names in `D0.Geometry.ArchiveJuliaRaisingOperatorReadout`;
it reports the basis-state theorem at lines 199–225 with binders `r : Role`,
`s : ArchiveFockState`, and conclusion exactly
`archiveFockExteriorEquiv (carCreateEnd r (Pi.single s 1)) =
ι ℝ (archiveRoleBasis r) * archiveFockExteriorBasis s`. The generated query
also records the whole-creator and whole-query signatures and their common
axiom footprint. This direct metadata query used source digest
`9f91c6206c8b781a506fc896c3c799415dcf44f7bd3ee046d8b629c001073ddb` and
collector SHA-256
`61634b3f3d9524c979d9b1092a86073b6f67c4e5bcbc27f434e3c00a7f339ff3`; it did
not invoke the CLI wrapper's Lake rebuild/freshness gate.

GitHub CI for the exact proof-source head
`81eda63d9d3ece0a34bac92930db650a4032b7c9` passed both `guards` (run
`40120569575`) and `lean-build` (run `40120569693`). C0 remains unfrozen and
independently unaccepted.

The updated `03_FORMALIZATION/D0/Geometry/ArchiveJuliaRaisingOperatorReadout.lean`
has SHA-256 `5b1192c912e22e622ae535fa65a2030839ae819b4dd744165ca62010ca29c057`.

## Faithful finite-carrier affine representation (24 October 2026)

The next carrier-level application formalizes the exact parameter recovery
implicit in the existing affine representation result, rather than treating
equality of its matrices as an unexamined geometry readout. The source owner is
`02_REGISTRY/research/MEMO_A4D_AFFINE_SENSITIVE_SITE_MATTER_LINK.md`, current
main snapshot `8b94198c8dfbdf5983ad0b350b058fb30bb68a54`, blob
`e278b41df9a6e555e85be0a78e6301f57d4098f5`, §19 Theorem A. That theorem gives
the exact law for `R_nil(L,b)=T_b ρ(L)`; the Lean carrier and its defining
maps remain the existing PR #109 formalization.

`archiveExteriorFrameLift_injective` proves that equality of the complete
16-state exterior-frame operators implies equality of the underlying linear
equivalences. Its proof uses covariance of the creator and the exact vacuum
identity to read `ι(L v)` for every role vector `v`, then applies the owned
left inverse of `ι`. `nilpotentAffineTranslation_injective` cancels a complete
translation with its already-proved inverse. These combine in
`nilpotentAffineRep_injective`: equality of complete `R_nil` operators implies
both `L=M` and `b=c`. The vacuum image recovers `b`; after that translation
cancellation isolates the frame action, where the first theorem recovers `L`.

The vacuum support, scalar-vacuum equivalence, frame-vacuum identity, and
creator-vacuum identity were moved to `ArchiveExteriorFrameLift.lean`, the
lowest existing module that owns the carrier/functor maps. Their public names
and types are preserved for the affine module and downstream imports. This
lets the faithful frame theorem live with its actual representation, rather
than depending on the higher affine construction.

The existing `formal_support.csv` rows for both modules now also reference this
primary artifact while retaining their original research-owner references.
This makes the proof slice discoverable through the existing support map; it
creates no claim, owner, application-acceptance, or C0-status row.
The updated support-map SHA-256 is
`ddb09492ec2323a5bda54816d40bd08951c962ed3188da2c755a1c155e78e183`.

The real cold-start suite now includes
`finite-affine-carrier-parameter-recovery`: an exact Lean theorem-name query,
an owner-theorem query, and a full-frame-action query find the research owner,
primary application artifact, and both Lean modules as direct-content
candidates. The suite found all four expected references in 14/14 scenarios
(15 total including the source-impact control). This is discovery evidence
only; the separate compiled declaration query above supplies the actual Lean
types and trust footprint. The updated runner SHA-256 is
`1e3724b7aee65aae644399a9769f075d5f3a302b040fd6249068458a59c52cc2`.

Scope is exact: this is faithfulness of the algebraic exterior and nilpotent
affine representations on the existing four-role, 16-state carrier. That
affine-representation result by itself does not prove that the single raising
query `C†(u)ρ(M)` recovers `M` (that map has only the one creator leg), nor the
Lorentz null inverse, all-jet or coframe/metric recovery, the full variational
pullback, source/price maps, physical admission, or GR selection. The next
checkpoint below now supplies the query's degree-one contraction block and
conditional null inverse. No claim or assumption is added, C0 is not frozen,
and this remains no physical-source theorem.

`#print axioms` for the three new public theorems reports only
`propext`, `Classical.choice`, and `Quot.sound`; no computational certificate,
axiom, `sorry`, or `admit` was added. The current worktree's sources for
`ArchiveExteriorFrameLift`, `A4DNilpotentAffineMatterLift`, and
`ArchiveJuliaRaisingOperatorReadout`, followed by the current `D0.All` import
root, compiled with Lean 4.30.0 into the temporary overlay using the preserved
Lean/Mathlib package cache. This is a targeted source plus import-root compile,
not a fresh Lake build. The generated declaration collector, run directly
against this compiled `D0.All` overlay rather than through the CLI wrapper's
Lake freshness gate, resolves:

- `archiveExteriorFrameLift_injective : Function.Injective archiveExteriorFrameLift`
  at source lines 204–243;
- `nilpotentAffineTranslation_injective : ∀ b, Function.Injective (T_b)` at
  lines 288–301;
- `nilpotentAffineRep_injective : R_nil(L,b)=R_nil(M,c) → L=M ∧ b=c` at
  lines 303–340.

That query records source digest
`42aee52c2ff5c28d4b66ad64ff5c60030d7d3bbfb51b46fcf4777c4e9e8f8a6d` and
collector SHA-256
`8cd6b7da3e1feedc07b615aa061128e19ebf51b451662e5bccb5cc5a9f3caa84`.
Source SHA-256 values are `ArchiveExteriorFrameLift.lean`
`f608b6851b487b6eaa2c34e640805a02eab9ff3c5af68fa742417d9a6b624b0e` and
`A4DNilpotentAffineMatterLift.lean`
`61b434d7e4cfba4a41b7c2b0cb436ff1e9fd1c62b21412a61d5632c4aed2486b`.
`formalization_debt_audit.py --check` passed with the unchanged three baseline
findings, `check_claim_map_coverage.py` passed, and
`generate_lean_views.py --check` passed with no stale generated views. The
focused proof-architecture suite passed 35/35 when invoked as the `tools` test
module, and the cold-start suite passed 14/14. GitHub CI for code/retrieval
head `f36ccfd34414c47da4f930167d6049e8e93e1994` passed `guards` (run
`40122035588`) and `lean-build` (run `40122035591`). The PR remains OPEN/DRAFT.
C0 remains unfrozen and independently unaccepted.

## Finite-carrier Julia null-block inverse (24 October 2026)

This continuation composes the existing complete CAR/exterior query result
with the null-leg inverse owned by published PR #334. The source is pinned at
commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, path
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §§8.4–8.5, equations
(26)–(31). Its concrete consumer is §5.1 of
`02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`. The consumer uses the
recovered query geometry for the declared Julia/star-density application; the
formalization below establishes only the algebraic map, not that consumer's
physical price, admission or selection premises.

In `D0.Geometry.ArchiveJuliaRaisingOperatorReadout`,
`archiveExteriorContraction_creator` derives the exact CAR contraction/creator
identity. `archiveJuliaNullBlock_readout` then applies contraction to the same
complete query `C†(u)ρ(M)` on `C†(v)|0⟩` and recovers
`Bv=Mv-α(Mv)u`, assuming the chart normalization `α(u)=1`. Thus the block is
read from the actual finite query, rather than introduced as an unrelated
geometric map. `archiveJuliaNullBlock_decomposition` records the complementary
identity `Mv=Bv+α(Mv)u`.

The bilinear-form theorem `archiveJuliaNullProjectedMetric` derives
`S(x,y)=b(x)a(y)+a(x)b(y)+q a(x)a(y)` from symmetry of the source endpoint
form and the endpoint isometry, where `a=α∘M`, `b(x)=Pₓ(u,Bx)`,
`q=Pₓ(u,u)`, and `S=Pᵧ-Pₓ(B·,B·)`. The coordinate theorem
`archiveJuliaNullReconstructCovector` uses the explicit chart data `b(z)=1`
and branch `1+q a(z)>0`; it proves `d=sqrt(1+q S(z,z))=1+q a(z)`,
`t=S(z,z)/(1+d)=a(z)`, and recovers every component of `a` by
`a(x)=(S(x,z)-b(x)t)/d`. `archiveJuliaNullBlock_reconstructsAffineFunctional`
composes this inversion with the block and endpoint-form definitions.

The source's normalized witness is also constructed as
`archiveJuliaNullEuclideanWitness b=b/(bᵀb)` in `archiveRoleBasis` coordinates;
`archiveJuliaNullEuclideanWitness_normalized` proves `b(z)=1` when `b≠0`.
In the null case `q=Pₓ(u,u)=0`,
`archiveJuliaNullBlock_covector_ne_zero` obtains `b≠0` from nondegeneracy of
`Pₓ`, `u≠0`, and invertibility of `M`. The witness existence is therefore
proved for that stated null case, not silently supplied by the reconstruction
theorem.

The carrier-specific scope is the existing four-role real vector space and
16-state Fock query. Endpoint symmetry, endpoint isometry, nondegeneracy,
nonzero/null data, chart normalization, and the positive branch remain explicit
hypotheses in their respective lemmas. The proof does not instantiate the
source's concrete `Jx,Jy` matrices and proper-Lorentz constraint together as a
single theorem, formalize the non-null formula (27), or prove all-jet extension,
coframe/metric recovery, the variational pullback, source/price maps, physical
admission, or GR selection. This is not a physical-source theorem and makes no
C0 acceptance or claim-status change.

Validation: with Lean 4.30.0, the changed Julia module and the current `D0.All`
import root compiled from this worktree into `/private/tmp/d0-pr402-lean-overlay`
using the preserved pinned Lean/Mathlib package cache. This is a targeted
module and import-root overlay compile, not a fresh Lake build. The direct
generated declaration query imported that compiled `D0.All`, found all nine
new public declarations, and reports the standard axiom set
`propext`, `Classical.choice`, `Quot.sound` for each; it adds no computational
certificate axiom. The project Lean source digest is
`32ce3a83ad5c7228c7862d7105798036b09a23b3c96b7713d1a16a5ab3afbf96`. The
generated collector script SHA-256 is
`9085600f24ad463e88d4df76d23c5cf8ecd403a5b6e6e8cdfb36168cdaf3a397`; the
updated Julia module SHA-256 is
`ffa6780f5d646a9e0ed71366191316af76446d5f1e9a38416beee22f685e8135`.
The exact declaration ranges are: contraction/creator identity 324–335;
block decomposition and null covector nonzero 355–383; projected metric
identity 385–426; role-coordinate evaluation 420–431; Euclidean witness
positivity/normalization 467–491; covector inverse 493–537; block-level
affine-functional inverse 539–579; and full-query block readout 581–621.
The proof-architecture unit suite passed 35/35 and claim-map coverage passed
25/25 under the bundled Python runtime. The full cold-start search found all
15/15 cases; the new Julia-null case found all four required refs as direct
content, and its source-change regression passed (16 total benchmark checks).
The updated cold-start runner SHA-256 is
`9b92abb0342a9fbbfdb239ef0375271eec4e57c795924072934c490959aa6487`.
`formalization_debt_audit.py --check` remains at 3/3 baseline findings, and
`generate_lean_views.py --check` reports `stale=0`. The code/retrieval head and
GitHub CI for the proof-source head `bf914625a6cc82b0c6bb37dd5e3a57d17b280a68`
both pass on PR #402: `D0 guards` run `40123581569` and `D0 Lean build` run
`40123581419`. The guard's unchanged-science-input check, artifact freshness,
semantic mutations and preservation checks passed; its isolated research
replay and registered/Bartholdi certificate stages were skipped in Draft mode.
The PR remains OPEN/DRAFT. C0 remains unfrozen and independently unaccepted.

## Shared exterior/CAR relation reused by the Julia application (24 October 2026)

The Julia-specific `archiveExteriorContraction_creator` is now a compatibility
adapter over the already proved generic
`archiveExterior_contraction_creator_car` in
`D0.Geometry.ArchiveExteriorFrameLift`. The two statements differ only by
rearranging the same real-vector-space identity. The Julia theorem keeps its
public name and exact type for existing readout proofs, while its proof now
depends on the shared CAR/exterior law instead of repeating the Clifford
calculation. No claim status, carrier, source scope or C0 disposition changes.

Validation used `python3 tools/lean_task_build.py cache` for the Mathlib roots
in this module's import chain, then
`python3 tools/lean_task_build.py narrow D0.Geometry.ArchiveJuliaRaisingOperatorReadout`.
The narrow target compiled successfully under Lean 4.30.0 (2,992 Lake jobs).
The build helper's post-run source digest is
`0e5371eeaa557b23a7cb553386be192b2ea81bf765cdcd4bb449f7dc9ed7209b`; the
manifest SHA-256 is
`4ed211000f753c64c6b1fc155970f6b28c9500763f1ad520d8762ae165ac24fa`, and the
updated Julia module SHA-256 is
`416e7e552343192a2bd01c8f209a7cd743a866a51b11201ea087694bc1a4b2a3`. The
build completed without Lean errors; warnings were existing lints in imported
modules. This is a targeted module build, not the final `D0.All` build.

## Fibonacci first-step block API reuse (24 October 2026)

The finite scalar example in `D0.VNext.PerronGNSTower` now derives its
diagonal-block multiplication, star and trace identities from the shared
`fibonacciBlockMatrix_mul`, `fibonacciBlockMatrix_star` and
`trace_fibonacciBlockMatrix` API in `D0.Algebra.FibonacciAFTower`. The scalar
embedding `firstRefinementScalarMatrix`, level-zero input map
`firstRefinementLevelZero`, and all-level output `firstRefinementAFStep` are
public definitions, so the new compiled theorem
`firstRefinementMap_is_level_zero_specialization` states an accessible map
equality: the old scalar map is exactly the coordinate readout of
`fibonacciAFRefinementHom 0` after embedding its two scalar inputs as
one-by-one matrices. The exact theorem locator and its three public adapter
definitions are added to the existing finite-real owner row and generated
`ClaimMap`; that row remains a locator, while the Lean theorem is the checked
application. No status is promoted. Existing first-step theorem types and the
finite-level map/pairing remain unchanged. No AF C*-limit, positive trace state
or completed GNS space is constructed.

Validation: `python3 tools/lean_task_build.py narrow
D0.VNext.PerronGNSTower` and `python3 tools/lean_task_build.py narrow
D0.TheoremLedger.ClaimMap` passed under Lean 4.30.0 (2,948 and 2 Lake jobs).
With the bundled Python 3.12 runtime, `generate_lean_views.py --check` reports
`stale=0`, `check_claim_map_coverage.py` passes, and
`formalization_debt_audit.py --check` remains at 3/3 baseline findings. A
compiled `#print` confirms the theorem type names public `firstRefinementAFStep`;
`#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound`.
The CRLF-aware `git diff --check` passes. The post-run Lean source digest is
`caa32872b68505e3a1f69fe625a7991c247372f5ecb73ff39f3fc752072227de`; manifest
SHA-256 is `4ed211000f753c64c6b1fc155970f6b28c9500763f1ad520d8762ae165ac24fa`;
`claims.csv` SHA-256 is `8ba9bfbac99a5fe0d8e8f2b6ef8d69f3190f8c1073051eca9f005e5a93b578cf`;
generated `ClaimMap.lean` SHA-256 is
`eca8ee59abf66cae2ca5d73d727caed8920b05073dbea2dce408b17fb7c9ba61`;
and `PerronGNSTower.lean` SHA-256 is
`3090b4db023f000f5c7c10c6e50ddede4bbcad446e359c177f02d5cc3ca2e573`. This
is targeted validation, not the final `D0.All` build or release integration.

## Full null-query frame recovery from the observed carrier block (24 October 2026)

This continues the pinned raising-operator source in #334, commit
`fe5cf335da04cac14e50407b03f98b96be17dc52`,
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §§8.4–8.5, Eq. (28). Its
downstream consumer is §5.1 of
`A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`. These are unchanged source
pins; this Lean result formalizes an algebraic application and does not accept
the scientific owner's broader application.

`archiveJuliaQueryNullBlock X α` is now a linear map built from the supplied
full 16-state operator `X`: insert a role vector into the vacuum's one-particle
state, apply `X`, contract with `α`, and read out the degree-one coefficient.
The compiled `archiveJuliaQueryNullBlock_readout` proves that for the actual
`X = archiveJuliaRaisingQuery u M`, with `α u = 1`, this observed map equals
the owned block `B = M - (α ∘ M) • u`. The recovered covector value and frame
are defined from this observed `B` and the two endpoint bilinear forms; they do
not use a separate frame oracle in their definitions.

The compiled `archiveJuliaQueryNullRecoveredFrame_eq` composes the observed
block identity, the projected-metric identity, the exact square-root/correction
inverse, and `M x = B x + α(M x) • u`. Given endpoint symmetry/isometry, the
normalized chart vector and the positive branch, it proves the recovered
function is the complete `M`. The stronger null specialization,
`archiveJuliaQueryNullRecoveredFrame_eq_of_null`, derives `b ≠ 0` from
nondegeneracy of `Pₓ`, `u ≠ 0`, and `Pₓ(u,u)=0`; it constructs the canonical
Euclidean witness `z=b/(bᵀb)`, proves `b(z)=1`, and gets the branch from
`q=0`. Thus this null application does not take the normalized witness or the
branch as extra inputs.

The remaining hypotheses are explicit: `Pₓ` is symmetric and nondegenerate;
`Pᵧ` is its pullback along `M`; `X` equals the actual raising query; and the
query chart satisfies `α(u)=1`. The formalization does
not identify `α` with a physical clock/timelike observer, instantiate the
source's concrete `Jₓ,Jᵧ` endpoint frames or proper-orientation determinant,
formalize the non-null formula (27), or prove all-jet smoothness, coframe and
metric recovery (30a), the variational pullback (31), the complete physical
price/source, or D0 admission. It adds no claim, assumption, application
acceptance, or C0 status; the existing `formal_support.csv` row continues to
index this Lean module and primary artifact.

The targeted Lean 4.30.0 build
`python3 tools/lean_task_build.py narrow D0.Geometry.ArchiveJuliaRaisingOperatorReadout`
passed (2,992 Lake jobs). The declaration inventories for the two recovered
frame theorems are
`sources/d0_proof_architecture_formalization_2026-10-24/julia_null_query_frame_recovery_inventory.json`
(SHA-256 `ddf187b917f103c71b911ff0c8f3abc51d21ef377f4f3429b7a1cd6a1a3b7943`)
and
`sources/d0_proof_architecture_formalization_2026-10-24/julia_null_query_frame_recovery_null_inventory.json`
(SHA-256 `f1489649fe907f0ff4ad765d4135ab684253893eea2525791cd1355ba7d9cc42`).
Both were queried from the compiled module import
`D0.Geometry.ArchiveJuliaRaisingOperatorReadout`, at snapshot
`8a496eabae10af441de1c4aad628a9ac56f6bf33` with `worktree_dirty=true`, under
Lean 4.30.0 and manifest SHA-256
`4ed211000f753c64c6b1fc155970f6b28c9500763f1ad520d8762ae165ac24fa`. The
common project Lean source digest is
`0f8a70695c1764fc095c260f98248e9da859fdc6948d6deb706e628eb38a8bf5`; the
collector SHA-256 is `8cd6b7da3e1feedc07b615aa061128e19ebf51b451662e5bccb5cc5a9f3caa84`.
Both declarations resolve to the expected module and source; their elaborated
axiom reports are exactly `Classical.choice`, `Quot.sound`, and `propext`.
The updated Lean module SHA-256 is
`06cc8cce2c0aa75017b0182f095905c8e695f99ce8d70e4281c429c6188b57ad`.
These inventories verify the declaration types and provenance through the
module import. They are not a current-source `D0.All` replay; the final
integration build remains for the Ready checkpoint.

## Query-to-principal-frame coframe recovery (24 October 2026)

This checkpoint formalizes the next map in the same published #334 source:
commit `fe5cf335da04cac14e50407b03f98b96be17dc52`,
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §§8.4–8.5, Eqs. (26) and
(30a). The identified downstream consumer is §5.1 of
`A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`, blob
`734e21ae6bc04ff3446ad15858936d417fdd2e55`.

The new supported module
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` composes the existing full
finite-carrier query and vacuum readout with the existing solder/Lorentz matrix
convention. It takes a family of actual query operators `X_r` and retains the
explicit hypothesis that each equals the owned raising query `C(u_r)ρ(M_r)`.
For each role `r`, `u_r` is the `r`-th column of `U_mat = L η Fᵀ`; the readout
theorem recovers that vector from `X_r`'s vacuum response, with its `M_r`
linear equivalence left explicit. The four outputs therefore form the same
`U_mat`. In the existing
`IsRoleLorentz Λ` convention, taking `L = Λᵀ` proves
`F̄ = U_matᵀ η = F L⁻¹`; if `F e = 1`, the recovered coframe is `L e`, and
`(L e)ᵀ η (L e) = eᵀ η e`. The base matrix lemmas live beside the existing
frame action in `A4DRawSolderFrameAction`; the new module is registered in
the existing `formal_support.csv` and generated `D0.All` view.

This consumes the narrow mathematical application from the pinned operator
readout to the inverse-coframe reconstruction. Its remaining conditions and
scope stay visible: `M_r` ranges over arbitrary finite-dimensional linear
equivalences and is not constrained to the source's proper-Lorentz endpoint
family; and the matrix proof does not derive the `X_r=C(u_r)ρ(M_r)` hypothesis
or establish that an admitted D0 execution selects those inputs. It proves no
all-jet regularity, variational pullback (31), native price/source equality,
physical admission, or GR selection. No claim status,
C0 disposition, scientific acceptance, or #334 lifecycle state changes.

The targeted Lean 4.30.0 build
`python3 tools/lean_task_build.py narrow D0.Geometry.A4DJuliaPrincipalFrameRecovery`
passed (3,020 Lake jobs); the base module
`D0.Geometry.A4DRawSolderFrameAction` also passed its narrow build (2,981
jobs). The declaration inventory
`sources/d0_proof_architecture_formalization_2026-10-24/principal_frame_recovery_inventory.json`
was queried through import root `D0.Geometry.A4DJuliaPrincipalFrameRecovery`
from the worktree at published base commit `0cc9ba5526a80cc0e1b509af267e0f9fb3f3c96f`
with its explicit query-representation comment update in the dirty tree,
with Lean 4.30.0 and collector SHA-256
`8e95fbfb6896de85a8d0309aa2b7ad68051cce7b7d42749b54ce4bef07131ed7`.
The new matrix and query-recovery declarations report `Classical.choice`,
`Quot.sound`, and `propext`; their query-family dependency closure also
contains the private `native_decide` axiom generated by
`archiveCreatorPermSign` in the existing CAR/exterior proof. The inventory
SHA-256 is
`44b03bdd62a8fd00b5546caedb5541cf77add6ae1082610f8a1012f5da06558c`; its
Lean source digest is
`8baf2d4665ac1c3c36602a754fd4f2eca0d3e4ab4ad6f5c4bbe687c1c47cb1de`. The
query-to-frame composition module SHA-256 is
`ae3a27dd27fdb72e3f04e54c4075d44812db8c3b0ec3ec3c9182a5dee1787da3`.
`generate_lean_views.py --check` reports `stale=0`, claim-map coverage passes,
and `formalization_debt_audit.py --check` remains at the three baseline
findings. This is a targeted application build, not a `D0.All` integration
replay; the latter remains deferred to Ready.

The cold-start suite now includes
`julia-query-principal-frame-coframe-recovery`, which separates the Eq. (30a)
owner in §8.5 from its §5.1 consumer and requires the new Lean composition and
matrix adapter to be discoverable. The full run found all 16/16 search cases;
both pinned source sections and both Lean modules were found as direct content.
`python -m unittest tools.test_proof_architecture` passed 35/35 tests, and the
updated runner SHA-256 is
`ddbf8ac8a0c70c6586d038e03fd586dd4eda6ebbe5444c3645df99d8c7f39138`.

### Null-chart endpoint-map recovery (24 October 2026)

This continues the same pinned source and consumer: #334 commit
`fe5cf335da04cac14e50407b03f98b96be17dc52`,
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §§8.4–8.5, Eqs. (26), (28),
and (30a); consumer §5.1 of
`A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`. The former theorem handled
the observed coframe after assuming that each supplied operator had the
raising-query representation. This continuation adds a concrete query-family
constructor and consumes the existing finite-carrier null inverse.

`principalFrameJuliaQueryFamily F L M` constructs the four full finite-carrier
queries from the repository-owned CAR creator matrices, using the four columns
of `U_mat = L η Fᵀ` and their endpoint linear maps `M_r`. The existing
full-carrier CAR/exterior identity supplies the exact bridge to the query
readout. Its `columnMatrix`, coframe-recovery, and metric-invariance theorems
specialize the prior composition without a separate operator-equality
hypothesis. `principalFrameObservedNullQueryFrameReadout` then exposes a
per-role endpoint decoder from the same observed operator and its
vacuum-readout vector.
`principalFrameJuliaQueryFamily_null_link_recovery` composes that decoder with
the existing Eq. (28) result and recovers `M_r` for any selected role `r` on
the null chart.

The link theorem retains the actual endpoint assumptions for that selected
role: the source form is symmetric and nondegenerate, `M_r` transports it to
the target form, `α_r(u_r)=1`, and `u_r` is nonzero and null. The theorem does
not require the other three shifts to be null. The canonical Euclidean witness
supplies the separate normalized vector and fixes the positive branch at
`q=0`. Thus this is an algebraic left-inverse application for one complete
finite query in the four-query family. It does not prove smoothness of the
full inverse or `D R D Φ = I`, compose the non-null chart (27), impose the
source's proper-Lorentz endpoint family, recover observer/clock jets, or
establish the variational pullback (31), native price/source equality,
physical admission, or GR selection. It changes no claim status, C0
disposition, scientific acceptance, or #334 lifecycle state.

The targeted Lean 4.30.0 build of
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` passed (3,020 Lake jobs). The
compiled declaration inventory contains 53 declarations across
`A4DRawSolderFrameAction` and `A4DJuliaPrincipalFrameRecovery`; the new query
and endpoint-map theorems include `Classical.choice`, `Quot.sound`, and
`propext` in their transitive axiom footprint. A follow-up inventory replay
also reports the private `native_decide` axiom generated by the existing
`archiveCreatorPermSign` finite CAR/exterior proof; the earlier three-item
summary omitted this dependency. At snapshot
`0a613fcd6683786fa6bb2ad37463601aec0cc61c` with `worktree_dirty=true`, Lean
source digest is
`a6a4743b44c682c5cc6729742f65eabd2b96f45be873259312c7cdf5dd83d73f`,
inventory SHA-256 is
`22bec2d3c61f70d4b10208aaa16d3004c5c57c9edecdbc845a9dc0e87cd4fac2`,
module SHA-256 is
`124303f49c30f72bc6829206e70e8ce20e3431640ba6caaad08fca0f5bc13f39`, and
collector SHA-256 remains
`8e95fbfb6896de85a8d0309aa2b7ad68051cce7b7d42749b54ce4bef07131ed7`.

The cold-start case now searches the null inverse as a distinct §8.4 source
from the §8.5 coframe map and §5.1 consumer, and requires the new constructor,
decoder, and Lean module to be discoverable. The runner SHA-256 is
`030bbecb93338ce2f1c991d13bf17141dd8dcfdea1dcf8f113eef7599342dadf`.
The full cold-start run found all 16/16 search cases, passed all 17 benchmark
cases, and retained the exact-source versus unrelated-prose impact control.
The focused proof-architecture suite passed 35/35 tests; generated-view and
claim-map checks passed; the debt audit remains at its three baseline findings.
The full cold-start run found all 16/16 search cases, passed all 17 benchmark
cases, and retained the exact-source versus unrelated-prose impact control.
The focused proof-architecture suite passed 35/35 tests.

### Full open-chart endpoint-map recovery (24 October 2026)

This continues the same pinned source and consumer: #334 commit
`fe5cf335da04cac14e50407b03f98b96be17dc52`,
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §8.4, Eq. (28), and consumer
§5.1 of `A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`. The preceding formalization
composed Eq. (28) only on the null locus. This checkpoint composes the same
inverse with the repository-owned `principalFrameJuliaQueryFamily` throughout
its full open chart.

`principalFrameJuliaQueryFamily_open_chart_link_recovery` uses the actual
four-query CAR family and recovers the selected endpoint map `M_r` from the
observed query at role `r`. It retains symmetry of the source endpoint form,
the endpoint isometry, normalization of the source covector on the principal
coframe column, a nonzero observed projected metric covector, and the positive
square-root branch. The shift need not be null: non-null `q` values are covered
where these open-chart conditions hold. The historical `Null` in
`principalFrameObservedNullQueryFrameReadout` remains in the declaration name;
that decoder is the Eq. (28) open-chart readout.

`principalFrameJuliaQueryFamily_null_link_recovery` is now a specialization of
this theorem. Its existing nondegeneracy, normalized covector, and one selected
nonzero null shift derive the projected-covector and positive-branch
conditions. The other three shifts need not be null. The separate non-null
gamma formula (27), proper-Lorentz endpoint-family selection, smoothness of
the full inverse or the all-jet identity `D R D Φ = I`, observer/clock jets,
variational pullback (31), native price/source selection, physical admission,
and GR closure remain open. This algebraic composition changes no claim
status, C0 disposition, scientific acceptance, or #334 lifecycle state.

The targeted Lean 4.30.0 build of
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` passed (3,020 Lake jobs). The
compiled inventory contains 54 declarations across
`A4DRawSolderFrameAction` and `A4DJuliaPrincipalFrameRecovery`; both the new
open-chart theorem and its null specialization have transitive axioms
`Classical.choice`, `Quot.sound`, the private `native_decide` axiom generated
by the existing `archiveCreatorPermSign` CAR/exterior proof, and `propext`.
The inventory SHA-256 is
`cb0855e9b823dd154fc820590865b2537ace10f55e4e206d2673bd3fadb3e3f2`; its Lean
source digest is
`84c20d4b1432affa35f2552a961a175da0775a64decdd4818237cc215af0a06f`.
The query-to-frame module SHA-256 is
`fa6869603483d3c839fe5f0ddaf30aa951104b2480acb12fc82618ce710a6f9b`, and the
inventory collector SHA-256 remains
`8e95fbfb6896de85a8d0309aa2b7ad68051cce7b7d42749b54ce4bef07131ed7`.

The updated cold-start case finds all 16/16 search cases and passes all 17
benchmark cases, including the exact-source versus unrelated-prose impact
control. The focused proof-architecture suite passed 35/35 tests;
`generate_lean_views.py --check` reports `stale=0`, claim-map coverage passes,
the formalization-debt audit remains at its three baseline findings, and
`git diff --check` is clean. The cold-start runner SHA-256 is
`c41562c5e56878cc7c4a6c2ba3266bcff8ac82cfb89733458c549b7e228623df`. This is
the targeted Eq. (28) application, not a `D0.All` integration replay or
physical GR acceptance.

### Non-null Lorentz-Clifford recovery adapter (24 October 2026)

This continues the pinned #334 source and consumer: commit
`fe5cf335da04cac14e50407b03f98b96be17dc52`,
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §8.4, Eq. (27), and consumer
§5.1 of `A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`.

The new module `D0.Geometry.A4DJuliaNonNullGammaRecovery` defines the actual
finite-carrier Lorentz-Clifford operator `Γ(u)=C(u)+i_(P u)` and derives
`Γ(u)^2=P(u,u)·I` from the owned creator/contraction CAR. Its Eq. (27)
recovery theorem takes the exact exterior-model query `C(u)ρ(M)` and proves
the full frame-lift identity
`U=(P(u,u))⁻¹ Γ(u)·(X−χₓXχᵧ⁻¹)` when `P(u,u)≠0`. A companion theorem applies
the existing all-state CAR/exterior query equality to the repository-owned
Jordan–Wigner query. These declarations operate on the complete finite
16-state carrier.

The two endpoint identities remain explicit hypotheses: conjugation of the
creator by `χₓ` yields negative metric contraction, and the endpoint volume
operators intertwine the frame lift. The adapter does not derive them for the
source's proper-Lorentz endpoint package. The Eq. (27) and Eq. (28) charts are
not yet joined into one formal theorem covering every `u ≠ 0`; smooth all-jet
recovery, variational pullback (31), physical admission, full price/source
selection, and GR closure remain open. This advances the compiled algebraic
composition while preserving the endpoint and physical boundaries.

The narrow Lean 4.30.0 build passed for
`D0.Geometry.A4DJuliaNonNullGammaRecovery` (2,993 Lake jobs); the dependent
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` build also passed (3,020 jobs).
The new-module inventory contains five declarations, including its generated
`_abel` helper. Its main Eq. (27) recovery theorem has transitive axioms
`Classical.choice`, `Quot.sound`, and `propext`; the CAR corollary additionally
inherits the existing private `native_decide` axiom from
`archiveCreatorPermSign`. At snapshot
`5035534a54bc6c308a2f50750e14cbb6bc8c3b29` with `worktree_dirty=true`, the
Lean source digest is
`52bdc96a1c98eef44d209a9a8e2ca84c9ac56992615467b1ba718204f6a31516`, the
inventory SHA-256 is
`622ae764a7413a230b8358a6fc1742f409b2b720003e8f71bbf0394a46c984c0`, and the
collector SHA-256 is
`d688a0e49f872a6d32941a59121c9c0ac452167608446976abccebad6b37dbb3`.
The new module SHA-256 is
`6c61216a3557d41595243fe924a318e40866bfc5dd0ca6bbb55618ee3b2f6bcc`.

The module is registered in existing `formal_support.csv`; the generator adds
it to the public `D0.All` import view. The cold-start case now searches for
both Eq. (27) and Eq. (28), pins their shared §8.4 source separately from the
§8.5 coframe-map owner and §5.1 consumer, and states the conditional endpoint
scope explicitly. Adding the new Lean module moved the Russian Eq. (28) query's
pinned source behind the previous 15-candidate inspection window. The cold-start
runner now inspects the minimum 18 candidates; the query again resolves the
exact §8.4 commit/blob rather than accepting a citation-only match. A regression
test pins this bounded window. The replay found all 16/16 required-source cases
and all 17 search/impact benchmark cases; the exact-source-versus-unrelated-prose
impact control passed. Runner SHA-256:
`39838fa98e10dc748fdb7dca40a385605ef1eacb2efb47f65221e2573132cbba`.

The generated-view writer now preserves each existing view's newline
convention. This keeps the CRLF `D0/All.lean` change to its one added import
instead of rewriting the full file; the regression covers CRLF, LF, and new
files. Generator SHA-256:
`a91f9a26ca43e083d7d470e637e075c0d94296627d3a3f8f02270f58ac8ff319`.

On final local inputs, both narrow Lean builds passed: the new Eq. (27) module
(2,993 Lake jobs) and its principal-frame dependent (3,020 jobs). The generator
suite passed 27/27, the proof-architecture suite 36/36, generated-view and
claim-map checks passed, the no-sorry scan passed, and the debt audit remained
at its three baseline findings. The CRLF-aware whitespace check passed. At
code commit `23773edd`, GitHub Draft workflows `D0 guards` (run
`40131508206`) and `D0 Lean build` (run `40131508181`) passed. Draft policy
skipped `Build release proof closure` and `Compile native checkpoint capsules`
in the Lean workflow; this is therefore not a `D0.All` replay, C0 acceptance,
or physical GR closure.

### Fixed-chart Eq. (27) endpoint composition (25 October 2026)

This checkpoint continues the same pinned #334 §8.4 source and §5.1 consumer.
In `D0.Geometry.A4DJuliaNonNullGammaRecovery`, the source's fixed diagonal
Lorentz form and dual covector now determine four canonical gamma generators
on the full 16-state carrier. Their CAR-derived volume operator is packaged as
a linear equivalence. The basis creator identity is extended by linearity to
every `u`, proving
`χ C(u) χ⁻¹ = -i_(P u)` for this fixed source chart without leaving that map
as an input hypothesis.

The new theorem
`archiveJuliaSourceIdentityCARRaisingQuery_nonNull_gamma_recovery` closes the
Eq. (27) identity for the owned Jordan--Wigner query when the frame transport
is the identity and `P(u,u) ≠ 0`. The proof uses the all-state CAR/exterior query
equality, the derived volume conjugation, and the already-derived Clifford
square. It is a complete finite-carrier algebraic application in this chart.
It does not prove endpoint covariance for a nonidentity proper-Lorentz map;
the arbitrary-transport adapter still names that hypothesis. The Eq. (27)/Eq.
(28) join, all-jet and variational pullback, physical admission, full price/source
selection, and GR closure remain open.

The final narrow Lean 4.30.0 build passed for
`D0.Geometry.A4DJuliaNonNullGammaRecovery` (2,993 jobs), and its dependent
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` build passed (3,020 jobs).
The exact owning-module inventory contains 64 declarations. The new arbitrary-
vector volume-conjugation theorem has transitive axioms
`Classical.choice`, `Quot.sound`, and `propext`. The concrete CAR query
specialization also retains the existing private `native_decide` axiom from
`archiveCreatorPermSign`. At base snapshot
`e5524078016f37663658a4bf92a8a7442509fda6` with `worktree_dirty=true`, its Lean
source digest is
`0c853ad5a989f7eb779cb0f95c69b54f0d20d95f3377881ad001878570472678`, inventory
SHA-256 is
`7a736afd45d0a36e6f67d219f50649444e08a88b90b2151dcd38b10f86f51d2f`, module
SHA-256 is
`6f100b9789fff132522c3caf5fd0206fa01fad99806fc812d33e33d97850003f`, and
generated Lean collector SHA-256 remains
`d688a0e49f872a6d32941a59121c9c0ac452167608446976abccebad6b37dbb3`.
The Python inventory writer was adjusted to write normalized newlines with
`Path.open`, so the artifact can also be generated by the repository's Python
3.9 runtime; its updated CLI SHA-256 is
`d0e9f62697184c2969cb5d082d8b6c58ce088fc330c6f177264605327fd6d1ac`.
`git diff --check` passes. GitHub `D0 guards` run `40135114305` and `D0 Lean
build` run `40135114293` both succeeded on code commit
`1dedffad57cd0c18a05fd1416065805040d63e54`; the remote inventory, Lean module,
primary artifact, and collector-writer blobs match their recorded local
SHA-256 values. Draft policy skipped isolated research-certificate replay,
registered certificates, release proof closure, and native checkpoint capsule
compilation. This is therefore not a `D0.All` replay, positive physical
selection, or GR closure.

### Eq. (27) recovery under derived oriented-isometry covariance (25 October 2026)

This checkpoint extends the preceding fixed-chart result on the same finite
16-state carrier and pinned #334 §8.4 source. In
`D0.Geometry.A4DJuliaNonNullGammaRecovery`,
`archiveJuliaSourceVolumeEquiv_frameLift_commute` now derives endpoint
covariance for an arbitrary linear isometry of the source chart. Its inputs are
preservation of `archiveJuliaSourceLorentzForm` on every pair and preservation
of the single oriented vector
`archiveJuliaSourceVolumeVacuum`, defined as the source volume equivalence
applied to the Fock vacuum. The proof transports creators and contractions,
then uses that oriented vector to fix the scalar. It does not assume covariance
of the volume operator on the full carrier.

The theorem
`archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_oriented_isometry`
uses this derived commutation identity to establish Eq. (27) for the owned CAR
query under those hypotheses and nonzero source Lorentz norm. The prior
identity-transport recovery is now a corollary. This removes the arbitrary
endpoint-covariance premise from that finite-chart application. The current
formal hypothesis is preservation of the oriented volume vector; identifying
it in this implementation with the coordinate condition `det M = 1` remains
an explicit unproved adapter and is not claimed here.

The result remains conditional mathematics on the fixed source chart. It does
not instantiate the source's physical endpoint maps or prove their isometry and
orientation hypotheses. The Eq. (27)/Eq. (28) join, all-jet and variational
transport, physical admission, complete price/source selection, and GR closure
remain open.

The narrow Lean 4.30.0 build passed for
`D0.Geometry.A4DJuliaNonNullGammaRecovery` (2,993 Lake jobs). The owning-module
inventory contains 73 declarations and records transitive axioms
`Classical.choice`, `Quot.sound`, and `propext` for the derived covariance
theorem. The Eq. (27) application also inherits the existing private
`native_decide` axiom from `archiveCreatorPermSign`. The inventory was generated
against the owning-module import root, not by rebuilding public `D0.All`.
At base snapshot `93cf621c0c561abaedcbba5112d35a3c07c2d2ec` with
`worktree_dirty=true`, the Lean source digest is
`a8a5616b396261313dff12f480a3c64b85d93523e424bc04bff30207d169979d`, collector
SHA-256 is
`d688a0e49f872a6d32941a59121c9c0ac452167608446976abccebad6b37dbb3`, inventory
SHA-256 is
`7282fcc4e75435ac3d979e9764bab0e615ca4a64593501ece67a8269ee2ec3e4`, and the
Lean module SHA-256 is
`f0ac215c92ed4957fbbde1f71d881767c7372683627e1f363b99aa4f9d1ec0de`. The
declaration inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/non_null_gamma_oriented_isometry_inventory.json`.

### Exact ordered-creator form of the source-volume vector (25 October 2026)

The oriented vector used in the preceding endpoint hypothesis now has an
explicit representative on the owned finite carrier:
`archiveJuliaSourceVolumeVacuum_eq_ordered_creator_product` proves that it is
the ordered `A,B,C,D` creator product applied to the Fock vacuum. The proof
first shows every exterior contraction kills the vacuum, then inducts through
the distinct source gamma generators using their CAR anticommutation with
creators. This records the vector itself, not merely the action of the volume
operator on the full carrier.

The owning-module inventory contains 89 declarations. The new vector
factorization theorem has transitive axioms `Classical.choice`, `Quot.sound`,
and `propext`; it does not inherit the older CAR sign-checker's
`native_decide` dependency. This makes the remaining orientation step concrete
for a determinant adapter, but does not prove that preservation of this vector
is equivalent to the coordinate condition `det M = 1`. That adapter and the
physical endpoint instantiation remain open; all-jet/variational transport,
physical admission, price/source selection, and GR closure remain open as well.

The narrow Lean 4.30.0 build passed again for
`D0.Geometry.A4DJuliaNonNullGammaRecovery` (2,993 Lake jobs). The inventory was
generated against this owning-module import root. At base snapshot
`9fba40378f5a6c0f9176a8cd771b0f0669092b1a` with `worktree_dirty=true`, Lean
source digest is
`6fd381b4d89216b33fa8d3dd5018481812c145d199d650d07b739f6de772396a`, collector
SHA-256 is
`d688a0e49f872a6d32941a59121c9c0ac452167608446976abccebad6b37dbb3`, inventory
SHA-256 is
`1fea1790da7d7560646b1453eaf16b32a15842f514eff615d1b51caa50851396`, and
Lean module SHA-256 is
`d68f497fee520202de4079de95e437cd5ca84ba51488c2946ad31a18053d7237`. The
declaration inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/non_null_gamma_volume_vector_factorization_inventory.json`.

### Non-null source orientation as the coordinate determinant (25 October 2026)

This closes the finite-chart adapter left open in the previous checkpoint.
`archiveJuliaSourceTopExteriorMap_scale` identifies the action on the unique
four-role exterior sector with its full `4×4` coordinate minor.
`archiveJuliaSourceTopMinor_eq_linearMap_det` proves that minor is the ordinary
`LinearMap.det` in the `A,B,C,D` role basis. Composing these with the ordered
creator representation gives

`archiveJuliaSourceVolumeVacuum_frameLift_eq_det_smul`:
`archiveExteriorFrameLift M volume = LinearMap.det M • volume`.

Consequently,
`archiveJuliaSourceVolumeVacuum_frameLift_preserved_iff_det_one` proves that
preservation of the oriented source-volume vector is equivalent to
`LinearMap.det M = 1`. The new corollary
`archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_det_one` composes
this adapter with Eq. (27): its hypotheses are source-chart metric isometry,
determinant one, and nonzero source Lorentz norm. The determinant premise is
now an ordinary coordinate condition rather than an opaque vector equation.

The result remains a finite algebraic statement for the owned CAR source
chart. It does not prove that the physical endpoint maps are isometries or
have determinant one, join Eq. (27) to Eq. (28), establish all-jet or
variational transport, or select physical admission, price/source, or GR
closure. The existing `native_decide` dependency in the CAR query specialization
is inherited from `archiveCreatorPermSign`; the new determinant adapter itself
has transitive axioms `Classical.choice`, `Quot.sound`, and `propext`.

The narrow Lean 4.30.0 build passed for
`D0.Geometry.A4DJuliaNonNullGammaRecovery` (2,993 Lake jobs). Its owning-module
inventory contains 123 declarations and was generated against the module-only
import root. At base snapshot
`7d663b01b33a22d4b68550a6e79f1a228c5cd28a` with `worktree_dirty=true`, the Lean
source digest is
`5876470aff4fbce7b759c7084bb94cf2b53c1f58915f1d01c9278fb4840f52cb`, collector
SHA-256 is
`d688a0e49f872a6d32941a59121c9c0ac452167608446976abccebad6b37dbb3`, inventory
SHA-256 is
`5f3e206171c60e2468b755d98bc9f7861b4618b4a15f331fb5ad3242c4354317`, and the
Lean module SHA-256 is
`9221008fc45490aff466c435809a1f87a40edbbd34e414bb1933e87f143394b8`. The
inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/non_null_gamma_determinant_adapter_inventory.json`.

### Generic Eq. (28) decoder and Eq. (27)/(28) overlap application (25 October 2026)

The source is the published #334 snapshot
`fe5cf335da04cac14e50407b03f98b96be17dc52`, §8.4, equations (26)–(28),
path `02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`. The declared downstream
consumer remains §5.1 of the exact AF radial coframe equivalence source, blob
`734e21ae6bc04ff3446ad15858936d417fdd2e55`.

The Eq. (28) open-chart proof in
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` now exposes a generic reusable
adapter, `principalFrameObservedQuery_open_chart_link_recovery`. It takes the
actual query representation `hQuery` and the complete vacuum readout map
`hColumn` as explicit witnesses, then proves the endpoint-map readout from the
existing finite Eq. (28) reconstruction. The prior
`principalFrameJuliaQueryFamily_open_chart_link_recovery` is now a specialization
of this adapter for the owned principal-frame query constructor. This keeps
query representation, readout transport, and the reconstruction theorem as
separate typed inputs.

The new composition module
`D0.Geometry.A4DJuliaRecoveryComposition` adds
`archiveJuliaSourceQuery_nonNull_open_chart_joint_recovery`: for the same
complete role-query family, it composes the Eq. (28) endpoint-map readout with
the Eq. (27) all-grade exterior-frame recovery. Its hypotheses explicitly bind
the query to the same shift/map (`hQuery`, `hColumn`), require a source-chart
isometry with `det M = 1` and nonzero Lorentz norm, and retain Eq. (28)'s
normalized covector, nonzero projected covector, and positive square-root
branch. The concrete
`principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery` supplies
both maps from the existing principal-frame CAR query and Eq. (26) readout.

This proves a finite algebraic overlap application in the common fixed source
chart: both inverse formulas recover the same endpoint map, while Eq. (27)
recovers its exterior lift on all grades. It does not cover the null locus by
Eq. (27), extend the endpoint covariance to distinct endpoint forms, prove
the physical endpoint package has determinant one, or establish all-jet,
variational, admission, complete-price/source, or GR closure.

The new owning-module inventories are
`sources/d0_proof_architecture_formalization_2026-10-24/principal_frame_generic_decoder_refactor_2026-10-25_inventory.json`
and
`sources/d0_proof_architecture_formalization_2026-10-24/eq27_eq28_joint_recovery_2026-10-25_inventory.json`.
They were collected at snapshot `0f9a94a85e5e82167db2087eec46c838fea181b1`
with `worktree_dirty=true` under Lean 4.30.0. The first lists 18 declarations;
the generic Eq. (28) adapter has transitive axioms `Classical.choice`,
`Quot.sound`, and `propext`, with no `native_decide`. The second lists the two
joint-composition declarations; both retain the existing private
`native_decide` dependency from `archiveCreatorPermSign`, alongside
`Classical.choice`, `Quot.sound`, and `propext`.

The principal-frame source SHA-256 is
`eea5270e1eb6b5c16ce4ac4ae86501b0490beaf2bd653f8567b25b48038105e3`; the
composition source SHA-256 is
`eaeae662b21e9e13c9cc9255bcd524cd6b81ff342e1a9cfd53439ba4dfd245fb`. The
inventory SHA-256 values are
`fc41b0ab64a3bc1b512c696852f99340ea053cf3942051fb2c7e1afb4439ce32` and
`426784e96ed7ccb1aeb71a837953c2f33efc56c503c1d8263850601acb995c75`;
their recorded collector digests are
`863a320fafb6bb4bb16e1164cf84f60af198d337b8726494aa56f147ef42f43d` and
`392354a7fdaa9e00bd00d5c4c04ebd8f656e665942bee46cd95a9f1b892eaf66`.

Narrow Lean 4.30.0 builds passed for
`D0.Geometry.A4DJuliaPrincipalFrameRecovery` (3,020 jobs) and
`D0.Geometry.A4DJuliaRecoveryComposition` (3,022 jobs). The generated
`D0.All` view now includes the new composition module, and
`python3 tools/generate_lean_views.py --check` reports `PASS lean_views
stale=0`. No full `D0.All` replay was run for this intermediate checkpoint.

### Eq. (27)/(28) coverage for every nonzero principal-frame shift (25 October 2026)

`D0.Geometry.A4DJuliaRecoveryComposition` now turns the full Eq. (27)
exterior-frame formula into a degree-one endpoint decoder. The readout applies
the complete query operator to creator states above the vacuum;
`archiveExteriorFrameLiftRoleReadout_frameLift` proves that this readout of the
full frame action is `M`. Composing it with
`archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_det_one` recovers
`M` from the Eq. (27) CAR formula on the non-null source chart, with source
isometry and determinant one, and without Eq. (28)'s normalized-covector,
projected-covector, or square-root-branch premises.

The new `archiveJuliaSourceLorentzForm_symmetric` and
`archiveJuliaSourceLorentzForm_nondegenerate` establish those properties for
the fixed diagonal source form from its basis pairing and four nonzero
coordinate signs. The concrete
`principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage` then covers each
nonzero shift in two cases. For nonzero source norm, the result returns the
Eq. (27) endpoint decoder under the explicit implication `det M = 1 → ...`.
For a nonzero null shift, the existing Eq. (28) null-link theorem returns its
endpoint decoder; source-form nondegeneracy and `α(u)=1` derive the projected
covector and positive branch internally. Thus the null case does not inherit
Eq. (27)'s determinant premise. The endpoint isometry remains an explicit
input in both cases.

The generic and concrete overlap theorems also return three facts when both
charts apply: the Eq. (28) decoder returns `M`, the Eq. (27) degree-one
decoder returns `M`, and the Eq. (27) operator identity holds on every grade
of the finite carrier. This covers the algebraic nonzero-shift chart for the
owned query family; it does not instantiate physical endpoint maps or prove
their isometry, determinant, or covector normalization. All-jet and
variational transport, physical admission, complete price/source selection,
and GR closure remain open.

The owning-module inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/eq27_eq28_chart_coverage_2026-10-25_inventory.json`.
It records eight declarations at snapshot `ec43ce33d152eea718056937364b23efb0563809`
with `worktree_dirty=true`, Lean 4.30.0, and lean-source digest
`fc8921050dea5e545c04124655c786b584ccbb1b3afd7c0e77300ac820748bf8`. The
collector digest is
`392354a7fdaa9e00bd00d5c4c04ebd8f656e665942bee46cd95a9f1b892eaf66`, the
inventory SHA-256 is
`08a2098f28e19284882d9ec96ad4c151d9a516ec5c190beb29f7c2fb095b79ee`, and the
composition source SHA-256 is
`83472c7c03ef2b69d86b96bfc9f40b60b26af0bf7947f1a24febc07b70e6b36c`. The new
source symmetry and
nondegeneracy proofs use only `Classical.choice`, `Quot.sound`, and `propext`;
Eq. (27) and the joint results retain the existing private `native_decide`
dependency from `archiveCreatorPermSign`.

The narrow Lean 4.30.0 build passed for
`D0.Geometry.A4DJuliaRecoveryComposition` (3,022 Lake jobs). No full `D0.All`
replay was run. This remains finite-carrier algebra under explicit endpoint
hypotheses, not physical source selection or GR closure.

### Cold-start scope refresh for the joined Julia charts (25 October 2026)

The Julia principal-frame cold-start case now queries
`principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage` in English and
Russian, requires the composition module as a discoverable result, and no
longer says the Eq. (27)/(28) charts are unjoined. Its manual scope card now
states the exact boundary: non-null Eq. (27) retains `det M = 1`; the null
Eq. (28) branch derives its projected-covector and positive-branch conditions;
the source proper-Lorentz endpoint identities remain unproved.

At snapshot `de4cfeb1b000363d85367b0b9da6f19edad67246` with
`worktree_dirty=true`, the full cold-start run found all 16/16 search cases
with every required source and passed all 17 benchmark checks, including the
exact-source-versus-unrelated-prose impact control. The exact chart-coverage
query returned the owning-module inventory, this primary artifact, and
`A4DJuliaRecoveryComposition.lean` as its top three direct-content candidates.
This required a search fix: the batched query path previously trusted
ripgrep's non-overlapping submatches, which could hide a longer declaration
name behind a shorter term from another query. It now matches query terms
against each complete matching line, and a regression exercises the full
12-query Julia case. All 38 proof-architecture tests passed. This checks
retrieval and scope routing; semantic scope acceptance remains manual. The
search implementation SHA-256 is
`fb15d7c2e02bb4134fd5be772ffb196e0f5fef6062a6c4f6e7e4be6b8abac11b`; the
cold-start runner SHA-256 is
`08ddac8d5ca7339444b07c53b5d1ea79d68d69054d15c9f05e143776aa1a01c5`.
`python3 -m unittest tools.test_proof_architecture` passed 38/38 after adding
regressions for the joined chart scope and batched declaration retrieval. The
test file SHA-256 is
`9bf1ce5075ae72733f585e09b163195cfa13c290c2c6e30ccd2984b07e50f49e`.

### Row-action Lorentz endpoint adapter for Eq. (27) (25 October 2026)

The previous composition left the source's endpoint metric-isometry and
orientation maps as explicit hypotheses. The current repository convention
already provides `IsRoleLorentz Λ`, meaning
`Λ * roleLorentzMetric * Λ.transpose = roleLorentzMetric`; the principal-frame
coframe action uses the transpose. In
`D0.Geometry.A4DJuliaRecoveryComposition`,
`archiveJuliaProperRoleLorentzEquiv` constructs that transposed `RoleSpace`
linear equivalence from `det Λ = 1`. Its application theorem identifies the
map with `Λ.transpose.mulVec`, and the adapter proves preservation of the
fixed source Lorentz form and determinant one. The new
`archiveJuliaSourceCARRaisingQuery_nonNull_recovery_of_proper_roleLorentz`
then composes those facts with the owned Eq. (27) decoder on the same finite
CAR carrier. This closes the matrix-convention transport for an
orientation-preserving row-action Lorentz endpoint.

The exact Lean theorem still assumes the endpoint matrix satisfies both
`IsRoleLorentz Λ` and `det Λ = 1`, plus a non-null source shift. It does not
prove that an admitted physical endpoint supplies that matrix, add a
time-orientation premise, or establish query admission, smooth/all-jet or
variational transport, complete price/source selection, or GR closure. Its
Eq. (27) theorem inherits the existing `native_decide` axiom from
`archiveCreatorPermSign`; the new matrix adapter declarations themselves
report only `Classical.choice`, `Quot.sound`, and `propext`.

The narrow Lean 4.30.0 build passed for
`D0.Geometry.A4DJuliaRecoveryComposition` (3,022 Lake jobs). The owning-module
inventory records 22 declarations at snapshot
`f3ef1b81e7bba2cb458d662506bcb379f1338d6b` with `worktree_dirty=true`, Lean
source digest
`e2d01817a8f7a3c11b64f0e84a9a44aa58e82304715793c0fb95ddffcbae4dae`, collector
SHA-256
`392354a7fdaa9e00bd00d5c4c04ebd8f656e665942bee46cd95a9f1b892eaf66`, and
toolchain `leanprover/lean4:v4.30.0`. The inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_endpoint_inventory_2026-10-25.json`.

The updated cold-start run found all 16/16 search cases with every required
source and passed all 17 benchmark checks, including the exact-source versus
unrelated-prose impact regression. The exact theorem query returned this
artifact, `A4DJuliaRecoveryComposition.lean`, and the owning-module inventory
as its first three direct-content candidates. This validates retrieval and
scope routing; semantic and physical acceptance remain separate.

### All-site symmetric metric tangent composition (25 October 2026)

The existing `D0.Geometry.A4DSolderMetricCompletion` module already defines
the finite solder Gram map `Theta * eta * Thetaᵀ`, its exact expansion, and its
flat difference quotient. The new
`coframeMetricReadout_realizes_symmetric` makes the missing linear application
explicit: for every finite lattice size `N` and every symmetric `Role` matrix
`q`, one constant field `e(x,r,a)=q(r,a)/2` realizes `q` at every site.
`solderMetric_realizes_symmetric_tangent` composes that same witness with the
nonlinear Gram path. For every site and every real `t`, the path is exactly
`eta + t q + t² C eta Cᵀ`; when `t ≠ 0`, its difference quotient is exactly
`q + t C eta Cᵀ`. Thus the first-order coefficient is an arbitrary symmetric
metric direction, with its finite-parameter remainder retained rather than
discarded.

This theorem has no nondegeneracy premise on `q`, and it does not claim that
the finite-`t` Gram remains nondegenerate. It formalizes the all-site finite
solder-Gram tangent used by the metric-provenance route; it does not prove
selection of this map by the physical star action or an admitted execution,
the full independent 16+24 variation, a continuum field equation, or
refinement. The owned nonlinear quotient and Einstein detector remain at the
source memo's stated research scope; physical metric/source selection and
global all-mode connection elimination remain open.

The compiled `D0.All` owning-module inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/solder_metric_tangent_inventory_2026-10-25.json`.
It records 99 declarations in `D0.Geometry.A4DSolderMetricCompletion`,
including both new theorems with the quantified symmetric-matrix statement,
explicit coframe witness, exact quadratic remainder, and difference quotient.
The inventory is at snapshot `981a543df11e1acc7c62ac515939692c8103ae9c`,
with the project Lean source digest
`8fb449ea0985ce8efbd85b1ef2ca5315283d875e755b138c4853eea2f04953ba`,
collector SHA-256
`1a4b7f2476594e0c124609dfcdd97d1c76dad72ee01f9af157c4e491d5767531`, and
Lean `leanprover/lean4:v4.30.0`. The declarations report the standard
`Classical.choice`, `Quot.sound`, and `propext` footprint. The module SHA-256
is `64e61c514b1e57cc89fc46c879fee59540427900eb09a9a66b67d79ce8d530c2`.

The changed module passed the narrow build (2,979 Lake jobs); the public
`D0.All` final build passed (4,568 Lake jobs). The direct source pin is added
to the existing `metric-provenance` evidence record; it is a formal locator
for this algebraic tangent, not a new application acceptance or C0 status.
The refreshed all-result declaration crosswalk keeps all 54 active results;
it records 191 evidence references, 182 verified pins, and the new module pin
with all 99 owning-module declarations. For `metric-provenance`, the pin is
verified but the semantic relation remains `unresolved` and
`acceptance_inferred=false`. The captured crosswalk snapshot is at
`981a543df11e1acc7c62ac515939692c8103ae9c` with `worktree_dirty=true`, Lean
source digest `8fb449ea0985ce8efbd85b1ef2ca5315283d875e755b138c4853eea2f04953ba`,
collector SHA-256
`5e9074769ba45eb74e6ade808f9aaac82dd09454e14941d6aea6c7885051b0f1`, and
artifact SHA-256
`a938dc26f8151e0b6ec64c67d64a6d8aa90761d9b5b364ff67c88af71ad14fd5`.
`python3 -m unittest tools.test_proof_architecture` passed 40/40, and
`gr_assembly.py check` reports a valid 54-result assembly with
`scientific_promotion=false`. These are pin, build, and routing checks only;
they do not accept a semantic or physical link.

### `smooth-parametrix` exact owner-source reconciliation (25 October 2026)

The existing `smooth-parametrix` result now pins the final merge commit for
PR #216, `5523d8f679c1ea02f9b73d757c81649740010d0a`, rather than the earlier
commit that happened to carry the same memo bytes. Its SHA-256 remains
`3ba0c4355999b147bc77048b082660558c538c48d49ef7fff98d4541069bf28a`; the
crosswalk verifies the immutable pin and confirms that the current checkout
matches it. The evidence now names the memo's exact section locators for the
partial verdict, smooth Fourier tails, IR parametrix, normal-center
cancellation, summed remainder, arbitrary fixed smooth realizations, and the
still-open coupled normal-rescue certificate.

The locator emits seven
`source:5523d8f679c1ea02f9b73d757c81649740010d0a:02_REGISTRY/research/MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md#...`
section-key candidates with status `candidate_section_keys_need_review`.
The result still has unresolved declaration, claim, and semantic dispositions,
with `acceptance_inferred=false`; it has no pinned Lean declaration or declared
application edge. PR #216 itself records only
`J2-SMOOTH-PARTIAL-CLOSURE` and leaves its refinement-uniform full coupled
normal rescue unresolved. Therefore this pin does not bind the memo to the
separate RAW-216 exact-source terminal and does not close that obligation.

The regenerated all-result crosswalk retains 54 results and 191 evidence
references, of which 182 pins verify; its source-locator summary explicitly
states that these are not accepted C0 units or semantic source relations. The
artifact is at
`sources/d0_proof_architecture_formalization_2026-10-24/assembly_result_declaration_crosswalk.json`,
snapshot `136e47add98e4ccc6b4d1f3eaa9401b648d0f66f` (`worktree_dirty=true`),
Lean source digest
`6ff55724920a14097e3a4078050c6e8f1f2b15ba6e98aca48623d6691a6e7c40`, and
artifact SHA-256
`6e119be67b78c0d5484e9db7c49f8c2ae0c265157bf54086ed2ab719e3d60bc5`.
`gr_assembly.py check` remains valid for 54 active results with
`scientific_promotion=false`. This is a source-provenance refinement only;
RAW-216 and physical GR selection remain open.

### Role-indexed proper Lorentz specialization of the joined Julia recovery (25 October 2026)

The source is the published #334 snapshot
`fe5cf335da04cac14e50407b03f98b96be17dc52`, §8.4, equations (26)–(28),
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, blob
`1c8d59e5533b443d9a015dc4512cfbc160ae7e62`. The declared downstream
consumer remains §5.1 of the exact AF radial coframe equivalence source, blob
`734e21ae6bc04ff3446ad15858936d417fdd2e55`.

`D0.Geometry.A4DJuliaRecoveryComposition` now assembles a role-indexed family
of the repository's proper row-action Lorentz matrices into the transposed
source-frame equivalences used by the principal-frame CAR query. The new
`principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz`
composes that same family with the existing Eq. (27)/(28) proof. Its
conclusion gives one endpoint map from the observed null-query readout, the
CAR/exterior endpoint readout, and the full exterior frame lift. The proof
reuses `IsRoleLorentz` preservation of the fixed source form and the existing
determinant-one map; it adds no parallel decoder or independent endpoint.

The hypotheses remain exact: every role matrix has `IsRoleLorentz` and
determinant one; the selected principal-frame source norm is nonzero; the
input covector is normalized; and Eq. (28)'s projected-covector and positive
branch conditions are supplied. This is the non-null chart of the finite
algebraic composition. It does not identify an admitted physical endpoint
with these matrices, prove time orientation or query admission, establish
all-jet/variational transport or complete price/source selection, or close
GR. No claim or assembly application was accepted by this specialization.

The exact declaration inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_joint_recovery_inventory_2026-10-25.json`.
It records snapshot `1ca175b68f20d4ccf26927d8d3b027aafbb48343`
(`worktree_dirty=true`), Lean source digest
`8cdcca1b292a651ef95a36a9ff64971c8e4b0a0b2c93da556dc208beac7a7231`,
generated collector SHA-256
`b246de83143607fbb866612a7c5b0ce83c71307561a37497b3c2fd1dab25a8db`,
and Lean `leanprover/lean4:v4.30.0`. Its elaborated type retains the Lorentz,
determinant, non-null, normalization, projected-covector, and positive-branch
hypotheses. The theorem's transitive axiom footprint is
`Classical.choice`, `Quot.sound`, `propext`, and the existing private
`native_decide` axiom from `archiveCreatorPermSign`; the new endpoint adapter
does not remove or conceal that inherited computation boundary. The module
SHA-256 is
`c43919374a019e7a9a27f8099edf6206cfa9226f0a8fa7198114d0ec4450349a`, and the
inventory SHA-256 is
`34ec4a2091bb81ef36337fab5d7d8a3e219e3749045239bf13a914ece2b6aa09`.

The module narrow build passed under Lean 4.30.0 (3,023 Lake jobs), and the
public `D0.All` final build passed (4,569 jobs). The inventory extractor's
`--output` path also had a Python 3.9.6 compatibility defect: `Path.write_text`
does not accept `newline` there. It now writes through `Path.open`, and its
focused tests pass 15/15. Extractor SHA-256 is
`d2f177774f3cd95c28066b4052d0c712e43abe1f8a79ccaaa03cbb5a4abaf943`; test
SHA-256 is
`0768c3c5c974044ab7853c5ce70cf6bf48f80f5b4d172d85fc4066efe7f54813`.
These build and inventory checks verify the Lean application and its recorded
trust boundary; physical admission and semantic source acceptance remain open.

The updated Julia cold-start replay on snapshot
`7283fc0ac68ee5a1a7f0a12e2a87f1a25258d28f` (`worktree_dirty=true`) found all
16/16 required-source cases and passed all 17 search/impact benchmarks. The
new exact declaration query returns this primary artifact and the Lean module
as its first two direct-content candidates; the separate Russian Eq. (27)/(28)
query finds the pinned §8.4 source and exact commit/blob. The exact-source
versus unrelated-prose impact control passed. Cold-start runner SHA-256 is
`f1ac1d58e1b8318ad6688315c415243d7150c5c3de97a03dfbc8f0246d22545d`, and the
updated proof-architecture test SHA-256 is
`03f1fc5fd21e18efcf0be84b44533d54bbb121afde34b7f8c30eacdbd352fd62`.
This replay verifies retrieval and pin routing; source-to-claim semantic
acceptance and physical endpoint binding remain separate.

### Current-source refresh of compiled claim and assembly crosswalks (25 October 2026)

The all-result crosswalk was regenerated after the Julia Lean source changed.
It now records snapshot `5c1d07ab4a743eefcf6d42b9f9c47c6f53ccb50d`
(`worktree_dirty=true`), current Lean source digest
`8cdcca1b292a651ef95a36a9ff64971c8e4b0a0b2c93da556dc208beac7a7231`,
generated module collector SHA-256
`5e9074769ba45eb74e6ade808f9aaac82dd09454e14941d6aea6c7885051b0f1`, and
proof-detail collector SHA-256
`1899bd10c2928a66d4b961f5b4d12a884b6d721f30bcc187ffcfe02c0f07830a`.
The machine-readable artifact remains at
`sources/d0_proof_architecture_formalization_2026-10-24/assembly_result_declaration_crosswalk.json`
with SHA-256
`bb7365ef7a8a5617a159e7760c8b0b6d2a945f73c8c15364cf2ab7b532d71f7b`.
It retains 54 result rows and 191 source records: 182 verified pins, eight
unavailable pinned blobs, and one immutable SHA mismatch. There are 15 exact
section locators and 151 unreviewed heading candidates across 37 results;
39 result-to-unit mappings remain incomplete. The refreshed view continues
to label these as source/declaration candidates, with no inferred semantic
acceptance. `gr_assembly.py check` passes for the 54 active-result limit with
`scientific_promotion=false`.

The all-claims resolution was also rerun against this same public `D0.All`
source digest and current claims registry. The current artifact is
`sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_current.json`,
SHA-256
`cbde9036d60167ebfd4f2904e627372c24736ba9683c5d79ace6ed7ff2df90f2`. It
records 889 claim rows and 2,747 theorem-locator atoms expanded to 8,317
ordered unique exact names; 2,506 names resolve in the compiled environment
and 5,811 do not. At the atom level, 2,547 have at least one exact name
match, four are ambiguous, 200 have no match, and 176 have no candidate
name. At the claim-row level, 708 rows have at least one matched locator and
181 have none. The current claims registry SHA-256 is
`8ba9bfbac99a5fe0d8e8f2b6ef8d69f3190f8c1073051eca9f005e5a93b578cf`; the
Lean collector SHA-256 is
`2ceba4405c8b46ac0cc924318d33955e59b7a3296be9a88afb57dfb8f4451818`, and
the toolchain is `leanprover/lean4:v4.30.0`.

These are current exact-name availability measurements, not mathematical
coverage: resolution does not validate a declaration's domain against its
claim or prove an application edge. The crosswalk's source records likewise
do not establish the frozen C0 denominator or independent acceptance. The
updated locators improve current-state reproducibility while C0 classification,
semantic review, and the remaining mathematical migrations stay open.

### Reviewed normal-chart estimator source locator (25 October 2026)

The `normal-chart-estimator` result now records the exact section
`L6: Exact estimator theorem` in its existing evidence record. I checked the
section in the pinned Git object `77d3ab6059bd1a3ce48637b97b9f30aa8825fc5f`
at `02_REGISTRY/research/ATORUS_NORMAL_JET_EINSTEIN_BRIDGE.md`; its blob SHA-256
is `ad1a72868ca3122314661695943664a5e4f7377413b416c3ccef43ea2ad531b6` and
the current file still matches that pin. The section states the centered-ray
reconstruction of `-2G[g](x) + O(epsilon_N^2)` for smooth Lorentz inputs in
their metric-normal chart, including the stated Ricci-sign convention.

The all-result crosswalk was regenerated from snapshot
`65fbc878959f9e5c51bb4313938de067a9618798` (`worktree_dirty=true`). Its Lean
source digest remains
`8cdcca1b292a651ef95a36a9ff64971c8e4b0a0b2c93da556dc208beac7a7231`; the
updated applications source digest is
`72b28e6e36e4ad4bab3145c497cf26540379f4eb2650b4b03c1736646ec436cb`. The
crosswalk SHA-256 is
`d57f7aa04bb40457e6a01fd92d85196dc4bbf3a256e9a8d386294b72246686bd`. It
still contains all 54 results and 191 evidence records. Exact section
locators increased from 15 to 16, and result rows with incomplete section
mapping decreased from 39 to 38; verified pin counts are unchanged.

This closes one source-provenance locator only. The crosswalk still labels the
section key as a candidate needing review, keeps the semantic relation
`unresolved`, and records `acceptance_inferred=false`. This does not establish
C0 membership or its accepted denominator, validate a Lean declaration as the
semantic proof of this research statement, or select a physical D0 realization.

### Exact verification-core declaration locators need a renewed application review (25 October 2026)

The compiled current-source inventory already exposes the verification-core
declarations at their Lean source locations. I checked three precise candidates
against the pinned module: `D0.Foundation.VerificationCore.verification_core`
(line 230), `D0.Foundation.VerificationCore.finiteSigmaWitness` (line 375),
and `D0.Foundation.VerificationCore.SigmaWitness.coded_verification_core`
(line 487). Their different roles match the general representation theorem,
the finite-code construction, and the conditional coded realization.

Adding those names and their line locators to the existing result record made
`gr_assembly.py check` reject the already accepted
`lean-verification-core-to-foundation` receipt as having a stale acceptance
digest. This is expected: `application_digest` includes the complete result
record, including evidence locators. I reverted that proposed registry change
and kept its accepted receipt intact rather than replacing its digest without
a renewed independent review. The candidates therefore remain visible in the
compiled inventory but are not promoted to an explicitly reviewed result-to-
declaration mapping. Recording them in the assembly result requires review of
the exact declarations and the unchanged application hypotheses at the
existing consumer edge.

### Exact action-protocol and finite-history declaration locators (25 October 2026)

The `native-actionprotocol-book03-pullback-boundary` result now pins the exact
source sections for its Book03 boundary and records eight fully qualified Lean
declaration names across `EndogenousActionQuantum.lean`,
`NativeHistoryActionResponse.lean`, and `GoldenCylinderOneStepBridge.lean`.
The generated crosswalk resolves all eight names in the compiled `D0.All`
inventory at the recorded source lines: the `ActionProtocol` and
`ActionExcessProfile` families and their equivalence; the same-history weight
ratio, same-endpoint cost witness, and complete fixed-memory two-tick response;
and the one-step cylinder match and non-product-history counterexample. The
reported trust footprint for these declarations is
`Classical.choice`, `Quot.sound`, and `propext`.

This improves exact retrieval and type visibility for the result's scoped
mathematical statements. Its row deliberately remains
`declaration_disposition=ambiguous` at the whole-module level while
`explicit_declaration_locator_disposition=all_resolved`: the exact names
resolve, but this inventory does not itself establish that their signatures
fully encode every research hypothesis. The semantic result relation remains
`unresolved`, `acceptance_inferred=false`, and `declared_applications` is empty.
No parent obligation has therefore been discharged. In particular, the
diagnostic identification of path cost with `ActionProtocol.action` and the
mathematical Book03 source lifts still lack the physical history-to-price and
geometry-to-operator pullbacks stated by the result owner.

The regenerated all-result crosswalk uses snapshot
`419262368ed464a739326adbe36d4495715ecf2b` with `worktree_dirty=true`, Lean
source digest
`8cdcca1b292a651ef95a36a9ff64971c8e4b0a0b2c93da556dc208beac7a7231`, and
applications digest
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`. Its
SHA-256 is
`d92918db52b12d8b32a8a7bc1fb9cccba9d2e948a635ac81444f06f0598b5ef9`.
The module collector SHA-256 is
`5e9074769ba45eb74e6ade808f9aaac82dd09454e14941d6aea6c7885051b0f1`, and
the proof-detail collector SHA-256 is
`e936c031368d608029317bb6e746954ad507a986885b9a29a9a4e8c54d711bdc`.
It contains 54 result rows and 191 evidence records: 182 verified pins, eight
unavailable pinned blobs, and one immutable SHA mismatch. Exact section
locators total 22, and 37 results still have incomplete section mappings.
These remain provenance and retrieval counts, not C0 coverage or acceptance.
`gr_assembly.py check` passes with 54 active results and
`scientific_promotion=false`. C0 remains unfrozen and independently
unaccepted; no claim status or physical assumption changes here. The checkpoint
is published on PR #402 at commit `99c4bba26f43f374dc558f9c5678be2a529229b5`;
remote Git tree blob IDs match all three changed artifacts. GitHub `guards`
(run `40153040215`) and `lean-build` (run `40153040195`) both passed on that
head. This updates no Lean source digest and is not a final `D0.All` replay.

### Compiled exact-name locators for the conditional redshift passport (25 October 2026)

The `D0-PHYSICAL-REDSHIFT-DETECTION-PASSPORT-001` row used theorem atoms
without the namespace declared by its Lean source. I changed only its
`lean_theorem` locator field to the two fully qualified names
`D0.Bridge.BridgeAssumption.represented_physicalOnePlusRedshift_eq_internal`
and `D0.Bridge.BridgeAssumption.represented_physical_redshift_drift_relation`;
the import-module locator remains
`D0.Bridge.PhysicalRedshiftDetection`. The status remains
`LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS`, and the row retains
`ASSUMP-PREREGISTERED-SELF-RETURN-FREQUENCY-REPRESENTATION`.

Both names resolve in the compiled `D0.All` environment as theorem
declarations owned by `D0.Bridge.PhysicalRedshiftDetection`, at source lines
22 and 30 of `03_FORMALIZATION/D0/Bridge/PhysicalRedshiftDetection.lean`.
Their compiled types quantify over a
`PreregisteredSelfReturnFrequencyRepresentation` and a
`FrequencyComparison`; the first equates the represented physical ratio to
the internal ratio, and the second states the represented one-tick drift law.
These signatures expose the external protocol representation required by the
claim. They do not establish that an actual apparatus supplies it.

At published PR head `c5f430df76975f9aae7d3aa48eaa9896601fd5ac`, the
all-claims artifact at
`sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_current.json`
had SHA-256
`400cfc7f3dfe82619579bb4599fdbed9301e9f839a7a91b1d776e4b37604ba4f`. That
version records snapshot `2d839f582ffe84763a9ac487c7060a9e32f8e4e1`
(`worktree_dirty=true`), Lean source digest
`b76d89ea4cc4e983eeb80ff1fa2784eaf147e0a8a5ec4521a60d936711d80976`, claims
registry SHA-256 `6566b397c0ca892ea278466da1b2c717fe230bd1b87c8ee358a1f276ee8e1b57`,
collector SHA-256
`7d84b5232692eb49f44de507610990c584b9417c5938f7e0706049ffdba81bce`, and
Lean 4.30.0. Its exact contents remain recoverable from that Git commit and
path; the next checkpoint below records the refreshed current artifact.

`generate_lean_views.py --check` passes, and the compiled inventory query
built `D0.All` successfully. The change updates no assembly result,
application receipt, or physical assumption. No reviewed consumer edge was
found for this claim in the current assembly registry, so no parent obligation
is discharged by this locator correction.

### Concrete visible-bit verification-to-transfer application (25 October 2026)

`D0-VERIFIABILITY-CLASS-001` already states that a concrete Boolean two-line
protocol witnesses non-vacuity. Its claim locator now lists the existing
`D0.Foundation.VerificationTransferApplication` alongside the generic owner
module and names three exact declarations: `visibleBitVerification`,
`visibleBit_records_follow_complete_future_equivalence`, and
`verified_visibleFalseReadout_transfers_to_common_execution`. The
`formal_support.csv` entry now also points to `claims.csv`. No theorem body,
claim status, bridge assumption, or assembly application was changed.

The compiled declaration inventory places the three declarations at lines
59–77, 79–85, and 119–129 of
`03_FORMALIZATION/D0/Foundation/VerificationTransferApplication.lean`.
`visibleBitVerification` constructs a `TheoryVerification` for the actual
`visibleBitSystem.futureEmpiricalTheory`. The record-equivalence theorem
proves equal represented records for `(false,false)` and `(false,true)` using
the owned `visibleBit_same_all_source_futures` theorem and
`representedRecord_eq_iff`. The transfer theorem's compiled type maps the
verified represented state `(false,false)` through
`verifiedStateImageEquiv` to the common execution readout, equal to
`outcomeMap false`; its proof depends on the concrete interpretation maps and
the `visibleFalseReadout_transfers_to_common_execution` theorem. The compiled
trust footprint is `Classical.choice`, `Quot.sound`, and `propext`.

The compiled claim-reuse record is
`sources/d0_proof_architecture_formalization_2026-10-24/verification_transfer_claim_reuse_current.json`,
SHA-256 `f5f8bde6236ddb4426414d28855009ccaf8c3df1067e927f13182c8f69bcd7bd`.
It records source snapshot `c5f430df76975f9aae7d3aa48eaa9896601fd5ac`
(`worktree_dirty=true`), Lean source digest
`c367897a077f251765b6a11ca60dd30098ea1b6c4bfe3b1dec34c213ffd5dd08`,
collector SHA-256
`550af8d1c80fdb9c00c16b0f9f2eb703b2d60780ba9dc56d9fb9f3a8bd1d2fb1`, and
public import `D0.All`. All seven exact locators on the claim now resolve.
The all-claims refresh records 889 claim rows, 2,750 locator mappings, and
2,511 resolved names among 8,320 unique candidates; its source, registry and
collector digests are stored in
`claim_candidate_resolution_current.json` (SHA-256
`576e160eedf89e002058b1af443841f37708b1ca0195cf44e923142248858f31`).

The reuse view reports proof-dependency-to-locator candidates from each
application theorem to `visibleBitVerification`, plus the generic quotient
equivalence dependency from `protocolTheoryVerification`. It still reports
`declared_applications=[]`; those compiled dependency joins do not create an
accepted application edge. This is a finite mathematical application, not an
external physical apparatus, causal-independence proof, cost selection, or
physical D0 realization. No physical or assembly premise is discharged.

### Generic finite Hermitian adjoint applied to the twisted CAR operator (25 October 2026)

This vertical slice adds `D0.Algebra.FiniteHermitianAdjoint` as a general
finite-coordinate API and connects it to the existing complex twisted CAR
implementation. For a finite carrier over a field with `StarRing`, the module
defines the standard sesquilinear pairing, proves its conjugate symmetry,
constructs the coordinatewise conjugate-transpose operator, proves the
adjoint identity, and proves uniqueness from evaluation on coordinate basis
vectors. It asserts no weighted or physically selected metric.

The concrete consumer is the existing finite site × Fock carrier in
`D0.Geometry.ArchiveTwistedHodgeDirac`. The new `dTwistedLinear` packages the
already-defined differential as a genuine complex-linear map, and
`cochainPairingC_eq_finiteHermitianPairing` identifies its nested site/Fock
sum with the generic coordinate pairing. Under the existing explicit premise
`∀ r, star (H r) * H r = 1`,
`dTwistedAdjoint_eq_finiteHermitianAdjoint` proves that the existing CAR
annihilation formula is exactly the generic adjoint. The unit-holonomy premise
remains quantified; this does not select `H`, a Hodge profile, a physical
inner product, or an action.

The generic declarations are in
`03_FORMALIZATION/D0/Algebra/FiniteHermitianAdjoint.lean`:
`finiteHermitianPairing_conj`, `finiteHermitianAdjoint`,
`finiteHermitianPairing_adjoint`, `finiteHermitianPairing_single_left`, and
`finiteHermitianAdjoint_unique`. The application declarations are in
`03_FORMALIZATION/D0/Geometry/ArchiveTwistedHodgeDirac.lean`:
`cochainPairingC_eq_finiteHermitianPairing`, `dTwistedLinear`, and
`dTwistedAdjoint_eq_finiteHermitianAdjoint` (the theorem begins at line 935;
the inventory declaration range is 931–958, including its doc comment).
The adapter retains the existing detailed `dTwisted_adjoint` proof as its
dependency. `formal_support.csv` records the concrete consumer, and
the generated `D0.All` view now imports the general Algebra module. No claim
status, bridge assumption, assembly application, or physical premise changes.

Compiled declaration inventories are stored at
`sources/d0_proof_architecture_formalization_2026-10-24/finite_hermitian_adjoint_module_declarations_2026-10-25.json`
(SHA-256
`240668cf139904e9d4e677a783c79bf4569a8d8e76e07a58bf5064492dcf54a8`) and
`sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hermitian_adjoint_application_2026-10-25.json`
(SHA-256
`4d56681d078ff994d020bafa2a5d46badbfb4ce682ba3abedd959a738877df98`). Both
were collected against snapshot
`cf15304e9e69472ecf9ba7a977585af8e3f41dcf` with
`worktree_dirty=true`, Lean 4.30.0, and common Lean-source digest
`9a93491afc17e98ccb519a36708e4b632cbeec4e94ea8a6af90b5f5da596f594`.
Their declaration collectors have SHA-256
`f158ffe2996c7b579add2dc96b967571088ec838d7efcb36b9b337bb0f4e342b` for the
generic module and
`440dd0248e99da01879635f9d08d7abeb46b780d75b099b00aa6863e89ee1a85` for the
concrete application. The compiled trust footprint of the adjoint identity
and concrete adapter is `Classical.choice`, `Quot.sound`, and `propext`; this
checkpoint removes none of those trust dependencies.

The narrow `D0.Geometry.ArchiveTwistedHodgeDirac` target builds with the new
API imported. This is a compiled finite mathematical adapter, not a positive
metric theorem or a physical Hodge/GR application. No assembly receipt is
created from a matching declaration name.

### Real-case cold-start retrieval replay (25 October 2026)

The repository's existing `tools/proof_architecture_cold_start.py` runner was
replayed against clean snapshot `57c7e64b6bb4ef4fba42eb294a3d110d255e5637`
with a bounded candidate window of 18. All 16 real search cases found every
required source as direct searchable content. Where a case declares an exact
pin or section scope, the runner also checked its pinned commit/blob and
required sections for the designated queries. The combined 17-check benchmark
passed: the 16 retrieval cases plus the exact-source-vs-unrelated-prose
change-impact regression. That control observed the linked source hash change,
kept it stable after unrelated prose changed, and retained the declared
application ID `native-result-to-obligation`.

This validates retrieval and source-impact routing only. The runner continues
to mark semantic scope review as manual; candidate matches, pinned retrieval,
and the synthetic impact control do not freeze C0, accept a source-to-claim
application, or discharge a physical obligation. The replay was evaluated on
the clean committed tree before recording this checkpoint.

Replay provenance: runner SHA-256
`f1ac1d58e1b8318ad6688315c415243d7150c5c3de97a03dfbc8f0246d22545d`;
authority digests at the replay snapshot were `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`8e26f20f22698af3761f969556b16e13755f42cd3b910b51cfab15c1bc125c39`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

### Real Hodge/CAR operator self-adjointness through the Hermitian API (25 October 2026)

The real nested counting pairing on the site × Fock carrier is now identified
with `finiteHermitianPairing`. This bridge consumes the existing
`hodgeCarDirac_self_adjoint` result to prove the stronger typed operator
equality
`finiteHermitianAdjoint (hodgeCarDiracₗ N) = hodgeCarDiracₗ N`. Composing it
with the previously proved real unit-profile bridge shows that the supplied
weighted adjoint at `w=1` is the existing Hodge/CAR operator itself. The
arbitrary nonzero-profile weighted API and its conditions are unchanged.

Three compiled inventories record the pairing adapter, typed operator
self-adjointness, and unit-profile specialization:

- `sources/d0_proof_architecture_formalization_2026-10-24/real_counting_pairing_hermitian_adapter_2026-10-25.json` (SHA-256 `fb8c094c2f28f2b654e0f7ad695b8d3008b933329c4aad0e9209b788ce8f68f3`, collector `8df7c417ae85695a479c9aa41e9434bbf39bc9392e75b67b1bdae383b048b274`);
- `sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_hermitian_adjoint_self_2026-10-25.json` (SHA-256 `675440bb95def09816429ec70fc47b1e4bdbc36b54634767a642273447280d7d`, collector `1f5aec36799d23bb3be8c0ddd6f93f9047b7f19241d640c43744b459ffe9e4b9`);
- `sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_unit_profile_adjoint_self_2026-10-25.json` (SHA-256 `c0f473e10b6bf5fdb36a3ceddf4d947d5ccf68d4a5af689f29dea0feec47d30d`, collector `bfd39f925bf01281dfbe752cf72ff83a2a7cda6709633ea3e80fdfbe103f4482`).

All three use import root `D0.Geometry.ArchiveWeightedHodgeDirac`, snapshot
`0c6bd55d33dfa654aa2f12931c32bb1a1cb2802c`, `worktree_dirty=true`, Lean 4.30.0,
and Lean-source digest
`ebed062fe0aa1f43bf76636fb42a0fc0c5cc03bf8ffb01474b4dbba319655209`. Their
trust footprint is `Classical.choice`, `Quot.sound`, and `propext`. The narrow
consumer build passes (2,989 jobs). This identifies the algebraic unit-profile
specialization only; it does not derive a geometric Hodge profile or select a
physical metric/source.

### Cold-start replay after the real Hodge/CAR adjoint application (25 October 2026)

The `real-unit-profile-weighted-hermitian-bridge` case now includes exact-name
queries for the real counting-pairing adapter, typed finite-Hermitian operator
self-adjointness, and its unit-profile weighted consequence. All 14/14
required sources were found as direct content. The full suite found all sources
in 18/18 cases; the 19/19 benchmark passed, including the exact-source-versus-
unrelated-prose impact control. Semantic scope review remains manual.

Replay used candidate limit 18 at snapshot
`0c6bd55d33dfa654aa2f12931c32bb1a1cb2802c` with `worktree_dirty=true`. Runner
SHA-256 was
`b833bd3d4e77c87f2fc50e7c15ca3d748e5a2b2d6d13b9e122b38164aa8ef3df`; the
primary artifact at replay time had SHA-256
`67ba7ad29aea83c25f4eb19221732ef6f6361dd068911c45695552dddc1fd416`. The
seven authority digests were: `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

This replay confirms rediscovery of the real algebraic unit-profile adapter;
it does not derive a geometric Hodge profile, select physical source/action,
accept semantic C0 coverage, or close GR.

### Complex twisted-CAR Hodge adapter and square (25 October 2026)

The existing complex `dTwisted` on the actual site × Fock carrier now has a
compiled linear-map nilpotency adapter that consumes its existing
anticommutation proof. Under the retained assumption
`∀ r, star (H r) * H r = 1`, the existing explicit `dTwistedAdjoint` is
identified with `finiteHermitianAdjoint (dTwistedLinear N H)`. This yields a
linear Hermitian Hodge--Dirac adapter equal pointwise to the existing
`hodgeCarDiracTwisted` function. The generic self-adjointness theorem and
Hodge anticommutator formula are then applied to that same finite operator;
the pointwise square keeps the explicit unitary-holonomy condition required
for the native adjoint formula.

Five exact-declaration inventories record the linear nilpotency adapter, the
operator bridge, self-adjointness, the linear square, and the pointwise square:

- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_differential_nilpotency_adapter_2026-10-25.json`, SHA-256 `d9f2572dbff91f2ac9272237fc95f8774a01c92fd79004c842e16b0489fa6d22`, collector `65b136c13e60e36a5e06c20913ef988bb3cab53b2bc997b3c43dad9541a9fc74`;
- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_operator_adapter_2026-10-25.json`, SHA-256 `b5df7761a5cdebbc03bab5825af283ec271b00cacd9c5068f5c3612ebb3ace99`, collector `c3554173a54aa30b0a9434cdb5662c093177fa00e552276093b89ccc511fe40d`;
- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_self_adjoint_2026-10-25.json`, SHA-256 `a4c40b3db2885cfff0c0f1e0e82a0d308a30e5fc06e662d2008ba787811dcbd4`, collector `1df218b77662ba1bd497fc3c2712e37c985987dc6c944de090e766f292b3bfa2`;
- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_linear_square_2026-10-25.json`, SHA-256 `2c7f58c022520690657dc95042383283fc0de00eadcaa7f158d8cb9f444a1789`, collector `9fe2e9291c7bc7d2ace94d1d16463b33c354b68b8139955e2deec12e18098bd7`;
- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_hodge_hermitian_pointwise_square_2026-10-25.json`, SHA-256 `3babb5cac31cfd53c73434faf5ee5640e471e523ba92a394467cb55e706e5eb4`, collector `b488f669079a9c7bddf2d633e22ac234914ee620bacd73a74485c4492961649b`.

All use public import root `D0.Geometry.ArchiveTwistedHodgeDirac`, snapshot
`613fb03906632ef36a2ea269fa5b4170b06d1b32`, `worktree_dirty=true`, source
digest `22f535222b7fbf4f1c95b56f706125fb262b278972988ec6f96233e5fe8815fb`, and
Lean 4.30.0. The selected square/nilpotency declarations retain the existing
`D0.Geometry.car_create_anticommutator_int._native.native_decide.ax_1_1`
trust boundary in addition to `Classical.choice`, `Quot.sound`, and `propext`;
the adapter does not hide or enlarge it. The narrow build of
`D0.Geometry.ArchiveTwistedHodgeDirac` passes 2,985 jobs. No physical holonomy,
action, source, or GR application is selected.

### Cold-start replay after complex twisted-CAR Hodge adapter (25 October 2026)

The `finite-hermitian-adjoint-twisted-car-application` case now asks seven
exact-name queries covering the actual twisted differential's linear-map
nilpotency, its Hermitian Hodge operator adapter, self-adjointness, and both
linear and pointwise square statements. All eight required sources were found
as direct content. The full suite found all sources in 18/18 cases; its 19/19
benchmark passed, including the exact-source-versus-unrelated-prose impact
control. Semantic scope review remains manual.

Replay used candidate limit 18 at snapshot `613fb03906632ef36a2ea269fa5b4170b06d1b32`
with `worktree_dirty=true`. The runner SHA-256 was
`5949c4b444cab840615922d1c9fbec8031bf83dcb7d4ee9a4417a419ce92b319`; the
primary artifact at replay time had SHA-256
`c23c649244176fdfb945a38daa7451025d9acf32c7405927557eeef0ba10b415`. The
seven authority digests were: `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

This verifies source rediscovery, not physical holonomy/action/source
selection, semantic acceptance, C0 freeze, or GR closure.

### Existing twisted-CAR adjoint theorems now reuse the generic API (25 October 2026)

The public `dTwistedAdjoint_adjoint` and
`hodgeCarDiracTwisted_self_adjoint` statements keep their existing signatures
and unitary-holonomy premise. Their proof bodies now bridge the established
`cochainPairingC` to `finiteHermitianPairing`, then consume respectively the
generic right-adjoint identity through
`dTwistedAdjoint_eq_finiteHermitianAdjoint`, and the generic Hodge
self-adjointness application. This removes the duplicated conjugation and
pairing calculations while retaining both compatibility theorem names.

The two compiled declaration inventories were extracted from
`D0.Geometry.ArchiveTwistedHodgeDirac` at snapshot
`2fe468c3d8ba889ddad49e3f9a73a094e5a95867`, with `worktree_dirty=true`, source
digest `998d8f0ad9ab02577931130f4614d4c89a088bf4b3b54325a3b7d1cfa476cf05`, and
Lean 4.30.0:

- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hermitian_right_adjoint_wrapper_2026-10-25.json` (SHA-256 `8592d75640eabe9f27db38a0ef0a4f4dc079e46ce59363cc856e9f597ebfc044`, collector `35beb5ad6a2fbc906da1c32e4ccfe0cd328dff39e37871e0c50100c5f4150de3`);
- `sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hermitian_self_adjoint_wrapper_2026-10-25.json` (SHA-256 `1feb993ab81de1f1dd83aeceb83f508bde0871f608ab763dbff4b393d6ca0c01`, collector `fc2dc85814c81ed8a7c7967b6167328939dc835fe9301e9648609f06b1f4cac3`).

Both report the existing `Classical.choice`, `Quot.sound`, and `propext`
footprint. The narrow `D0.Geometry.ArchiveTwistedHodgeDirac` build passes
(2,985 jobs). This is a proof-library refactor under the unchanged finite
pairing and holonomy assumptions; it selects no physical inner product,
holonomy, source, or GR realization.

### Cold-start replay after twisted-CAR wrapper refactor (25 October 2026)

The twisted-CAR case now has nine exact-name queries, including both retained
compatibility theorem names, and ten required sources. All 10/10 sources were
found as direct content. The complete suite found every required source in
18/18 cases; its 19/19 benchmark passed, including the exact-source-versus-
unrelated-prose impact control. Semantic scope review remains manual.

Replay used candidate limit 18 at snapshot
`2fe468c3d8ba889ddad49e3f9a73a094e5a95867` with `worktree_dirty=true`. The
runner SHA-256 was
`9cb9c9bced36a3330ab94e86ef6520d7e81672ce60f2b3aec739595c2ae7e2c2`; the
primary artifact at replay time had SHA-256
`5404b3dccdf14d0c83fe342148dbd8c3993e7bc9fae284e2dcf6d30990237427`. The
seven authority digests were: `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

The replay verifies rediscovery and compatibility routing only; it does not
accept semantic coverage or select physical Hodge/GR data.

### Existing twisted-CAR Laplacian theorem now consumes the generic square (25 October 2026)

The existing pointwise theorem `hodgeCarDiracTwisted_sq` keeps its statement:
the square of the complex site × Fock Hodge--Dirac equals the registered
`twistedDifferenceLaplacian`. Its proof now composes the generic pointwise
Hermitian Hodge-square law with the explicit
`dTwistedAdjoint_eq_finiteHermitianAdjoint` adapter and the already-owned
cross-term identity `hodgeCarDiracTwisted_cross`. Thus the generic
anticommutator is transported to the existing CAR Laplacian without repeating
the square expansion. The fibre corollary keeps its public name and result.

The refreshed exact declaration inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/twisted_car_hodge_laplacian_from_generic_square_2026-10-25.json`
(SHA-256 `437e3a49c2e5afd33bc1d760fc73df88726fb257e71603a413e29b6dedf08372`,
collector `8cfca97ab7f6a886ef713b80465b7ad51e23da2331af8fcac144ed42afa945da`).
It was compiled with import root
`D0.Geometry.ArchiveTwistedHodgeDirac`, Lean 4.30.0, source snapshot
`56023287037a872a03d616863e7e8cec93e1734d`, `worktree_dirty=true`, and Lean
source digest `9f86e52334d192c8e772b3a48ff6775c45b6e8f120984df39154677d788c2d91`.
Its trust footprint includes the existing
`car_create_anticommutator_int` and `car_mixed_anticommutator_int`
`native_decide` declarations reached through the owned cross-term proof, along
with `Classical.choice`, `Quot.sound`, and `propext`; this refactor adds no new
trust assumption. The narrow module build passes (2,985 jobs). No physical
holonomy, action, source, or GR selection follows.

### Cold-start replay after twisted-CAR square refactor (25 October 2026)

The `finite-hermitian-adjoint-twisted-car-application` case now has ten
exact-name queries and eleven required sources, including the preserved
pointwise Laplacian theorem and its refreshed compiled inventory. All 11/11
sources were found as direct content. The full suite found all required
sources in 18/18 cases; all 19/19 benchmark checks passed, including the
exact-source-versus-unrelated-prose impact control. Semantic scope review
remains manual.

Replay used candidate limit 18 at snapshot
`56023287037a872a03d616863e7e8cec93e1734d` with `worktree_dirty=true`. The
runner SHA-256 was
`5debd99f51990fcfdb201c4ba05c4b5b13acd716b31128feae1bd8a002239136`; the
primary artifact at replay time had SHA-256
`f90a9ee4a379a73d5fa84f8cb98049f89e8a3ffed9aa01cd1f0f71a045226568`. The
seven authority digests were: `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

This replay establishes rediscovery and scoped source routing; it does not
establish semantic acceptance, physical source/holonomy selection, C0 freeze,
or GR closure.

### Hermitian Hodge square and cubical anticommutator application (25 October 2026)

The generic finite Hermitian API now also proves that adjoints reverse
composition, that nilpotency transfers to the adjoint, and that the square of
`A + A†` is `A A† + A† A` whenever `A² = 0`. This supplies the Hermitian
counterpart of the already-owned weighted bilinear Hodge-square law without
assuming a positive or geometrically selected profile.

For the concrete application, the existing cubical coboundary nilpotency
theorem is consumed directly. At the real unit profile the registered
cubical weighted Hodge--Dirac square equals the anticommutator of that
coboundary and its standard Hermitian adjoint for every refinement `N`. The
statement is conditional on the unit profile identity already proved above;
it does not transport the result to other profiles or assert physical Hodge
selection.

The narrow build of `D0.Geometry.ArchiveWeightedHodgeDirac` passes all 2,989
jobs. The two exact-declaration inventories are
`sources/d0_proof_architecture_formalization_2026-10-24/finite_hermitian_hodge_dirac_square_2026-10-25.json`
(SHA-256
`73af6e2eaaaa92d9262d04cedc9aa209433fc8d80bed6feaed945384cb42a933`, collector
`92052e1ef0adf33cc5e5d5d9789df4bacc8bde192f4774d85d932fb90881b1c1`, import
root `D0.Algebra.FiniteHermitianAdjoint`) and
`sources/d0_proof_architecture_formalization_2026-10-24/cubical_unit_profile_hermitian_hodge_square_2026-10-25.json`
(SHA-256
`3d91554e60d8adcefb54ef32ec39d75b18c31a0c8ff0d7bcc57769d664b37f3d`, collector
`dd5c9d0aed95485addc5d4758a5a29347633bb2a702df537f779843ed7e9a11d`, import
root `D0.Geometry.ArchiveWeightedHodgeDirac`). Both were compiled at snapshot
`20c72a70de807b44ef804595d0ef1566c6f624b9` with `worktree_dirty=true`, source
digest `f0782da31588c76bc1aafdf95f45191dfd8757e0f666eac2c61f4997a0d7e501`,
and Lean 4.30.0. Their reported trust footprint is `Classical.choice`,
`Quot.sound`, and `propext`.

The real unit-profile cold-start case has been expanded to retrieve the generic
composition/square proof and its concrete nilpotent cubical application. Its
final search replay is recorded below; the suite remains a retrieval check and
manual semantic scope review is still required.

### Cold-start replay after Hermitian Hodge-square application (25 October 2026)

The updated unit-profile case now has seven exact-name queries: the weighted
and Hermitian adjoint bridge, generic self-adjointness and square laws, the
concrete cubical operator equality, and its pairing and square applications.
All 11 required sources were found as direct content. Across the full suite,
all 18/18 cases found every required source, and the 19/19 benchmark passed its
exact-source-versus-unrelated-prose impact control. Semantic scope review
remains manual.

Replay used candidate limit 18 at HEAD
`20c72a70de807b44ef804595d0ef1566c6f624b9`, `worktree_dirty=true`. Runner
SHA-256 is
`5f6d2f15fc46fc3ce83fc1495fe3e976dc8f62daa63135a5b23999b0ea128ae0`; the
primary artifact at replay time had SHA-256
`0f7348fe2b94455ce67faefe8a79d4a1c778c976974946ee21bafc28fdaed9cb`. The
authority digests were unchanged from the preceding replay: `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.
This confirms retrieval of the newly compiled square application, not semantic
acceptance, C0 freeze, or physical Hodge/GR selection.

### Generic Hermitian Hodge--Dirac and concrete cubical application (25 October 2026)

`D0.Algebra.FiniteHermitianAdjoint` now owns the equivalent right-operator
adjoint identity, additivity of its finite sesquilinear pairing, the generic
operator `finiteHermitianHodgeDirac A = A + A†`, and its self-adjointness proof.
The right-operator identity is derived from conjugate symmetry and the existing
left-form adjoint theorem; the Hodge result is therefore a composition of
already established adjoint laws, not a premise asserting self-adjointness.

The actual consumer is the registered finite cubical coboundary in
`D0.Geometry.ArchiveWeightedHodgeDirac`. At profile `w = 1`, its existing
weighted cubical Hodge--Dirac is proved equal as a linear operator to the new
generic Hermitian specialization. The pointwise application then proves
self-adjointness for the standard finite Hermitian pairing for every lattice
size `N`. The exact type carries no claim about a nonconstant profile or its
physical/geometric origin; the arbitrary nonzero profile continues to use the
separate bilinear weighted API.

The narrow build `python3 tools/lean_task_build.py narrow
D0.Geometry.ArchiveWeightedHodgeDirac` passes all 2,989 dependency jobs.
Three exact-declaration inventories record the generic theorem and both
concrete application declarations, with elaborated types, proof dependencies
and trust footprints:

- `sources/d0_proof_architecture_formalization_2026-10-24/finite_hermitian_hodge_dirac_self_adjoint_2026-10-25.json`, SHA-256 `db29932e9a252f6d85426b6f3705f1bc9ee70b221059774609c71a490d0922f2`, collector `687214e1bcf7ffce794095a40b9152053805424e49f9847fd52e9ddb1a11b824`, public import root `D0.Algebra.FiniteHermitianAdjoint`;
- `sources/d0_proof_architecture_formalization_2026-10-24/cubical_unit_profile_hermitian_hodge_equality_2026-10-25.json`, SHA-256 `33dca7028428c2342198f74f493b7ee4d4146e2b22a0fdf3209b633d132e4d88`, collector `28949a22bba7399afa6901c9182c342b0052799b02d8f9380378f7f3c6a9e41b`, public import root `D0.Geometry.ArchiveWeightedHodgeDirac`;
- `sources/d0_proof_architecture_formalization_2026-10-24/cubical_unit_profile_hermitian_hodge_self_adjoint_2026-10-25.json`, SHA-256 `adda5d8fffa98b7f2ee980ac75edee56bcbdc3beaeb93e6ae9fd47198e9cc4e6`, collector `7ef0ecb23290c4f883a7a7667f2b1c90e3ab31e3ea35c55f015e2ff90c6ae98e`, public import root `D0.Geometry.ArchiveWeightedHodgeDirac`.

All three were built at snapshot `e063c098ce6b62a496b7226e664fb1bae25deab3`
with `worktree_dirty=true`, Lean source digest
`6901e9eadb25230df7bac4f3814c2caf0159c043ad5e3c72226c6fdb6e467e65`, and
toolchain `leanprover/lean4:v4.30.0`. Their selected declarations report
`Classical.choice`, `Quot.sound`, and `propext`, matching the explicit trust
boundary.

The existing unit-profile cold-start case now asks for the generic Hodge
self-adjointness theorem, the exact cubical operator equality, and its concrete
pairing application. Search replay for the expanded case is recorded in the
following checkpoint. C0 remains unfrozen and independently unaccepted; this
algebraic slice changes no claim, assumption, assembly result, physical source,
or GR status.

### Cold-start replay after the Hermitian Hodge--Dirac application (25 October 2026)

The existing `real-unit-profile-weighted-hermitian-bridge` case now checks
five exact-name lookups across the generic weighted/Hermitian bridge, generic
Hermitian Hodge--Dirac theorem, concrete operator equality, and concrete
self-adjoint application. Its required sources include all three Lean modules,
all five compiled inventories, and this primary artifact. Replay found every
required source directly in all 18/18 real cases; the 19/19 total benchmark
also passed its exact-source-versus-unrelated-prose impact control. Semantic
scope review remains explicitly manual.

Replay used candidate limit 18 at HEAD
`e063c098ce6b62a496b7226e664fb1bae25deab3`, `worktree_dirty=true`. Runner
SHA-256 is
`f216047eabcbf9d0bab51bc181280a4936ed7771c8a2b709f6b980ee3242c02b`; the
primary artifact at replay time had SHA-256
`7a6dcf1e5473f234d81c4dbee77925ec6b0b282388273847fd1e7d8d891ef410`. The
authority digests remained: `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.
The new case found all three Lean module sources, all five exact compiled
declaration inventories, and this artifact as direct content; this is retrieval
evidence, not scientific acceptance or a C0 freeze.

### Cold-start case for the finite-adjoint application (25 October 2026)

The replay above was extended with the real case
`finite-hermitian-adjoint-twisted-car-application`. Its two queries require
direct retrieval of the generic finite-coordinate adjoint module, the concrete
site×Fock twisted-CAR consumer, and this primary artifact. The query-specific
scope note retains the explicit unit-holonomy premise and says that retrieval
does not select a weighted/physical inner product, holonomy, action, or physical
Hodge/GR application.

The expanded runner replay found all 17/17 required-source cases; all required
paths returned `found_direct_content`. The combined benchmark passed 18/18,
including the exact-source-versus-unrelated-prose impact regression. The
semantic scope review remains manual. Snapshot was HEAD
`57c7e64b6bb4ef4fba42eb294a3d110d255e5637` with `worktree_dirty=true`; the
runner SHA-256 was
`b3a5dc1dd53d0dcaf3d9302a0200eb4a14d42a9c3c70dcc5d10e7f6a62ea3791`, and the
primary artifact at replay time had SHA-256
`c1009f21ae292db81c4cebbc0fc973a06f94bfce63b153a5e4bedb30cbb5b78d`. The
seven authority-table digests matched the immediately preceding cold-start
replay record. As above, this is a retrieval/application-discovery check, not
a semantic acceptance, C0 freeze, or physical-obligation closure.

### Same-query legacy/new search comparison (25 October 2026)

I compared the existing GR-only `gr_assembly.search` route with the new
`proof_architecture.full_text_search` route (`limit=5`) on the same two exact
Lean-name questions. For `finiteHermitianAdjoint_unique` and
`dTwistedAdjoint_eq_finiteHermitianAdjoint`, the legacy assembly search
returned zero result groups. The new search returned three direct-content
candidates for each query, with the exact owning Lean module at rank 2. The
other two candidates were the primary artifact and the corresponding compiled
declaration inventory; none of the three returned sources was unrelated. The
serialized compact-card sizes were 2,488 and 3,330 characters respectively.
These lengths measure returned candidate cards, not human reading time or
model token consumption.

The compiled types preserve the relevant scope: the generic uniqueness result
is over a finite index and a field with `StarRing`, and assumes the candidate
map satisfies the pairing adjoint identity. The concrete application retains
`N`, the holonomy `H`, the quantified unit condition
`∀ r, star (H r) * H r = 1`, and the cochain `φ`; it equates the existing CAR
annihilation formula with the generic adjoint of `dTwistedLinear`. The scope
does not require new mathematics for this already compiled finite adapter.
Physical inner-product or holonomy selection and any physical Hodge/GR
application remain outside its conclusion. This comparison measures a narrow
lookup-route difference: `gr_assembly.search` searches its GR assembly result
groups, while the new route also searches Lean source and compiled inventories.

### Real unit-profile bridge between adjoint APIs (25 October 2026)

The two finite-adjoint modules use different pairings in general: the weighted
API is bilinear over an arbitrary field with an arbitrary nowhere-zero
profile, while the standard API is sesquilinear over a field with `StarRing`.
The proved overlap is deliberately limited to `K = ℝ` and `w = 1`, where real
star is trivial. `finiteWeightedPairing_one_eq_finiteHermitianPairing` proves
the pairing equality, and `finiteWeightedAdjoint_one_eq_finiteHermitianAdjoint`
uses the existing uniqueness theorem to identify the operators. No equivalence
is asserted for a nonconstant profile or a general involution.

The concrete consumer is `D0.Geometry.ArchiveWeightedHodgeDirac`:
`hodgeCarDirac_unit_profile_adjoint_eq_finiteHermitianAdjoint` applies that
specialization to the existing `hodgeCarDiracₗ N` at every `N`. Its type fixes
the profile to the constant one; it does not construct or select the
Lorentz-induced Hodge weight. The existing signed/nonzero weighted theorem is
unchanged. `formal_support.csv` now records the generic API's actual weighted
bridge and both concrete consumers; no claim, assumption, assembly status, or
application receipt changes.

The two exact compiled declaration records are
`sources/d0_proof_architecture_formalization_2026-10-24/finite_weighted_unit_profile_adjoint_bridge_2026-10-25.json`
(SHA-256
`f2c12832b0d4760e529d1f41e908ff957b6d8f10e269fae44e9d811589b45dac`) and
`sources/d0_proof_architecture_formalization_2026-10-24/archive_weighted_hodge_hermitian_bridge_2026-10-25.json`
(SHA-256
`1038de80229d66c72ec5880a1b6847bf193b38c53231de44e4345b84912b312c`). Both
were compiled at snapshot `c512a8cc5042e0b6160cfa3320665b2f3abc7cbe` with
`worktree_dirty=true`, Lean 4.30.0, and Lean-source digest
`fdba5314e1ef785e14b40f7c5509d1c9d2426e22f08903c5b3aa62de75aec65b`. Their
collector SHA-256 values are `59045a2abf642c22941b4d1b74f88262456ed83538e6751bc811386d91d00d6c`
and `919751a13135b91d8454bbc91cfb9f7cfb834378bb34dde6187e6c39beac66cd`,
using import roots `D0.Algebra.FiniteWeightedAdjoint` and
`D0.Geometry.ArchiveWeightedHodgeDirac`, respectively. Both report the
existing `Classical.choice`, `Quot.sound`, and `propext` trust footprint.
The narrow `D0.Geometry.ArchiveWeightedHodgeDirac` build passes (2,989 jobs).
This finite compatibility result selects no physical profile or Hodge/GR
source.

### Cold-start replay after the weighted-adjoint bridge (25 October 2026)

The suite now includes `real-unit-profile-weighted-hermitian-bridge`, with
separate exact-name queries for the generic unit-profile bridge and its actual
Hodge/CAR consumer. At the replay, all 18/18 search cases found every required
source as direct content; the expanded 19/19 benchmark also passed the exact
source-versus-unrelated-prose impact regression. The new case found both Lean
modules, both compiled inventories, and this primary artifact. Manual semantic
scope review remains required; retrieval does not select the unit profile as a
physical metric or close any C0 or GR obligation.

Replay used candidate limit 18 at HEAD
`c512a8cc5042e0b6160cfa3320665b2f3abc7cbe` with `worktree_dirty=true`. Runner
SHA-256 is
`c9c0b374452cb6db31adb644d65049f3092688d4778a9ea7ce9870b2da2bf734`; the
primary artifact at replay time had SHA-256
`37031033e6ce0fc91a2d76299a3b21f093ef5854b3f6ff551aad656a3945f2eb`. The
authority input digests were `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`aa783fa732b9a5a6e5fa351e064cb2013c394848d6e1e43f273efbeb5c3289c2`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

### Real Hodge/CAR square through the generic Hermitian API (25 October 2026)

`ArchiveHodgeCARDiracSquare` now packages the registered real forward CAR
differential and counting codifferential as finite linear maps on the actual
site × Fock carrier. The existing counting-pairing identity, converted to the
standard real finite Hermitian pairing, proves that this codifferential is
exactly the Hermitian adjoint of `dForwardₗ`. Nilpotency is transferred from
the existing function-level theorem, so the generic Hermitian Hodge-square
theorem yields the typed CAR anticommutator. The previous function-level
`hodgeCarDirac_sq` is now recovered from that anticommutator and the already
owned `hodgeCarDirac_cross` identity; its theorem statement and fibre corollary
are preserved. The linearity lemmas for the backward CAR summand and the
codifferential now live beside their operator and square laws, with their
public theorem names retained for existing consumers.

`ArchiveHodgeCARDiracKernel` also proves that its pre-existing
`hodgeCarDiracₗ` is the pointwise generic Hermitian adapter. The exact
declaration inventory records all eleven adapter and refactor declarations,
including their elaborated types, dependencies and trust footprints:

- `sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_square_from_generic_hermitian_2026-10-25.json`, SHA-256 `b72fef51de38cb26b27852170236e8a28cc3c2669d1859a179cc4f0f7e90546f`, collector SHA-256 `5371efd69f4423aa2a60238f8190002b923d4e6dcb24c7034f66122bb7f9e4a9`, public import root `D0.Geometry.ArchiveHodgeCARDiracKernel`.

The inventory was compiled at snapshot `00c5209a6da14b7b9d40bcb66deb395a965bb3c5` with `worktree_dirty=true`, Lean 4.30.0, and Lean-source digest `b7bcb4e77a930c6a0d0c922b8677d0a1be4d6fc888f9145ce7eaa957368c1af1`. The established `native_decide` dependency in the CAR anticommutator enters through the existing nilpotency and square proofs and is retained in the inventory. `formal_support.csv` names the square module as a direct consumer of the generic API. This is an algebraic real-carrier refactor: it selects no weighted/geometric profile, source, dynamics, or physical Hodge metric and changes no C0 or GR status.

Narrow builds passed for `ArchiveHodgeCARDiracSquare` (2,984 jobs),
`ArchiveHodgeCARDiracKernel` (2,985), `ArchiveWeightedHodgeDirac` (2,989),
`A4DLocatedTopologicalStar` (2,991), `ArchiveHodgeCARDiracShell` (3,398),
`ArchiveHodgeGradingSymmetry` (2,989), `ArchiveSpatialHistorySplit` (3,400),
and `A4DDiscreteEnergyKernel` (3,073). `validate_repo.py`,
`generate_lean_views.py --check`, `formalization_debt_audit.py --check`
(3 findings, unchanged from the baseline), `validate_work.py`, and
`validate_agent_protocol.py` also pass. The PR remains Draft, so the final
`D0.All` build is reserved for the Ready checkpoint.

### Cold-start replay after the real Hodge/CAR square refactor (25 October 2026)

The expanded `real-unit-profile-weighted-hermitian-bridge` case now includes
the actual forward/codifferential adjoint map, typed nilpotency, generic
Hodge-square application, preserved Laplacian theorem, and kernel-facing
linear-map adapter. Its Lean sources, the eleven-declaration compiled
inventory, and this primary artifact were all found as direct content. The
full suite passed 18/18 search cases and the 19/19 benchmark, including the
exact-source-versus-unrelated-prose impact regression. Semantic scope review
remains manual; retrieval does not establish physical profile selection or
C0/GR closure.

Replay used candidate limit 18 at HEAD
`00c5209a6da14b7b9d40bcb66deb395a965bb3c5`, `worktree_dirty=true`. Runner
SHA-256 is
`fce4fdecc4c026a94517d8363af85e3197d023a2911ce29080f22c90089ee16e`; the
primary artifact at replay time had SHA-256
`26ff2daacf2571aed39b370af82a2eebd12c624ed831e696b069d4e8344cd3c1`. The
authority input digests were `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`e6ca1a5ea0d3272ff3967da52a5885fe95d2ffd2f96fb5ff77449eca27079a56`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

### Generic typed adjoint equality for finite Hodge--Dirac operators (25 October 2026)

The generic finite Hermitian API now upgrades Hodge--Dirac self-adjointness
from the pairing identity to the typed operator equality
`finiteHermitianAdjoint (A + A†) = A + A†`. It follows directly from the
existing pairing theorem and finite adjoint uniqueness. The real Hodge/CAR
application now rewrites its established linear map through the registered
`dForwardₗ` Hodge--Dirac adapter and consumes this generic equality, replacing
its custom coordinate-pairing uniqueness proof. The existing unit-profile
weighted corollary remains unchanged.

The five exact declarations are recorded in
`sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_generic_adjoint_self_2026-10-25.json`
(SHA-256 `a78c3e153a16a3f3fb4590bef2f3b88de0e2fe08c76a52445ea2ab623bbb423e`,
collector SHA-256 `c256bf5b97bd04bb7927b0786a4c25cb0d72b912adb4aa9016f3f3db3bf72f0e`,
public import root `D0.Geometry.ArchiveWeightedHodgeDirac`). The inventory was
compiled at snapshot `81057d96d2bb04c9d081a10835ab3eb827537e40` with
`worktree_dirty=true`, Lean 4.30.0, and Lean-source digest
`9673ad896d3bf6e9f0f43ff45db0b3b19bad01975506800a9d5df79173769e80`. Its
trust footprint for all five declarations is `Classical.choice`, `Quot.sound`,
and `propext`. Narrow builds passed for
`D0.Algebra.FiniteHermitianAdjoint` and
`D0.Geometry.ArchiveWeightedHodgeDirac` (2,989 dependency jobs). No physical
profile or source is selected by this operator identity.


### Cold-start replay after generic Hodge/CAR adjoint equality (25 October 2026)

The expanded `real-unit-profile-weighted-hermitian-bridge` case now searches the
new generic typed operator-adjoint equality and the real Hodge/CAR application
that consumes it. Every required Lean source, prior inventory, the new
five-declaration inventory and this primary artifact were found as direct
content. The complete suite passed 18/18 search cases and the 19/19 benchmark,
including the exact-source-versus-unrelated-prose impact regression. The
semantic scope review remains manual; no physical profile or GR obligation is
closed by these algebraic equalities.

Replay used candidate limit 18 at HEAD
`81057d96d2bb04c9d081a10835ab3eb827537e40`, `worktree_dirty=true`. Runner
SHA-256 is
`e5b63ce1cebcf4e1d376c9a0e51f1f45788458ef3004f5822312fceed47c17a1`; the
primary artifact at replay time had SHA-256
`374eb5975b32939d81946b00fe08abce766fda609902a4ccc64b411de8702bf9`. The
authority input digests were `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`e6ca1a5ea0d3272ff3967da52a5885fe95d2ffd2f96fb5ff77449eca27079a56`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

### Canonical map refactor for the real Hodge/CAR kernel API (25 October 2026)

The kernel-facing `hodgeCarDiracₗ` now aliases the already-proved generic
finite Hermitian Hodge--Dirac map on the same site × Fock carrier. This removes
the second manually assembled `LinearMap`. The public function-level
`hodgeCarDirac` remains available: `hodgeCarDiracₗ_apply` is the compiled
pointwise bridge, and the existing `hodgeCarDirac_add` and
`hodgeCarDirac_smul` theorems now follow from the canonical map's own linearity
laws. The adapter equality is reflexive. Kernel membership/equivalence proofs,
the weighted-pairing application and spatial-shell compression now use the
bridge explicitly where the old implementation relied on definitional
reduction. Existing theorem statements and the 16-dimensional kernel result
are preserved.

The compiled declaration inventory for the full kernel module is
`sources/d0_proof_architecture_formalization_2026-10-24/real_hodge_car_canonical_map_refactor_2026-10-25.json`
(SHA-256 `30b4e32d3327379baba9e9f4b7935486434863c1772e9ddae269f49cdf630531`,
collector SHA-256 `7043a40e051ae7717f95638b649187c90c25a31f2e4b9b446fbc3545f8237eb2`,
public import root `D0.Geometry.ArchiveHodgeCARDiracKernel`). It contains 38
declarations with elaborated types, dependencies and trust footprints, and
records source digest `74b6c15666c7de63f098cc92d74772c1e4e65fe0643c43fe296ab7ce79f5600e`
at snapshot `d67eb595f09e13e682a4c26035efec4d45f24a03` with
`worktree_dirty=true`, Lean 4.30.0. `formal_support.csv` now records the
kernel as a consumer of the generic Hermitian API; the real Hodge/CAR
cold-start case includes the new bridge and inventory.

Narrow builds passed for `ArchiveHodgeCARDiracKernel` (2,985 jobs),
`ArchiveWeightedHodgeDirac` (2,989),
`ArchiveHodgeSpatialShellOperator` (3,405),
`A4DLocatedTopologicalStar` (2,991),
`ArchiveHodgeGradingSymmetry` (2,989), and
`TwistedHodgeZeroModeLifting` (2,988). The first dependent build exposed the
weighted-pairing proof's reliance on definitional reduction; the final proof
uses the exact bridge, and the dependent builds then pass. This remains an
algebraic refactor on the stated finite carrier. It selects no weighted or
geometric profile, physical source, or GR dynamics, and it changes no C0 or
physical-closure status.

### Cold-start replay after the canonical Hodge/CAR map refactor (25 October 2026)

The updated `real-unit-profile-weighted-hermitian-bridge` case searches for
the canonical `hodgeCarDiracₗ` definition, its explicit function-level bridge,
the generic linearity applications, and the compiled 38-declaration
inventory. The full replay found all required sources in all 18/18 cases at
candidate limit 18. The 19/19 benchmark passed, including the exact-source vs
unrelated-prose impact regression. The replay result is retrieval evidence;
semantic scope review remains manual and no physical profile or GR obligation
is closed.

Replay used snapshot `d67eb595f09e13e682a4c26035efec4d45f24a03` with
`worktree_dirty=true`. Runner SHA-256 is
`1ac6614700d3acc99e2000d47c00e761af63c0943f3cf59009034c5f4bd2844c`; the
primary artifact at replay time had SHA-256
`a16a0bbd1077b142f2969c88ec35b38503a275e2f6d20e6fb17cad6c437c4b02`.
Authority digests were `claims.csv`
`e64c1223d0e69c79374b592d4a289d341e64b976337ba8129fb9ab804812f718`,
`assumptions.csv`
`2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36`,
`formal_support.csv`
`852690a586e3b3f504dd9d78ccdfd622a38933aa448d093e920b48a52872dd54`,
`aliases.csv`
`8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f`,
assembly applications
`d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511`,
assembly contract
`72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6`, and
presupposition edges
`7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d`.

## Positive supplied-profile standard-Hilbert representative (25 October 2026)

The generic finite weighted-adjoint API now proves the square-root change of
coordinates explicitly. For every finite real coordinate carrier and every
caller-supplied pointwise-positive profile, the weighted pairing is the
standard finite Hermitian pairing after coordinate scaling by `sqrt(w)`. If
an operator is self-adjoint for that weighted pairing, its conjugate
`S_w A S_w⁻¹` is self-adjoint for the standard pairing
(`finiteWeightedConjugate_self_adjoint`). This is an algebraic result for a
given positive profile; it does not construct or select one.

The concrete cubical application
`cubicalWeightedHodgeDirac_standard_representative_application` applies this
theorem to the registered finite cubical coboundary and its weighted adjoint,
for every supplied positive profile and every refinement. `claims.csv` records
the exact compiled locator. Its existing `LEAN_PROVED` and `CORE-FORMALIZED`
fields remain unchanged. The standard-Hermitian representative is conditional
on the supplied profile and is not a construction of the Lorentz-induced
Hodge weight or a physical selection.

The focused narrow build compiled
`D0.Geometry.ArchiveWeightedHodgeDirac` (2,989 jobs), including the changed
`D0.Algebra.FiniteWeightedAdjoint` dependency. The generated-view check passed
with `stale=0`. The current claim-reuse replay through public import `D0.All`
resolves all four listed declarations; for the new concrete representative
application it reports `Classical.choice`, `Quot.sound`, and `propext`, with no
`native_decide` dependency. Exact types, dependencies, source digest, and
collector output are pinned in
`sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_standard_representative_claim_reuse_2026-10-25.json`
(SHA-256 `0024c82cbc7edf1ccc8c1f90798b4d15f735df447f426195bfb4caa3f3c71a88`,
Lean-source digest `297b6755258b7496bcb272b141a4e047e69e4384c4634b28110d45005e19280a`,
collector SHA-256
`9a8bf7be063ac36db542055fb8a4f4de877cadd32546b8126a7463f65798f95c`,
snapshot `566aeca2eb3a06f6d2d38e5a01b77541d9a571a4`,
`worktree_dirty=true`).

### Independent source-locator review for the registered weighted-Hodge claim

An independent source-locator review checked the canonical tracked
`BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md` at current snapshot
`566aeca2eb3a06f6d2d38e5a01b77541d9a571a4` and at the claim-introduction
commit `76c5e0255ee8e184d4dbdab23cbd947549e58a7e`. Neither version contains a
`06.spectral` section or a Hodge/Dirac passage. The claim row was introduced
without a corresponding Book 06 source change. Its original Lean owner had
only finite counts and the legacy Boolean degree-preservation flag; the
accompanying Python certificate is a floating-point 4×4 two-site example.
The current Lean module itself explicitly leaves geometric `W` and the
Lorentz-induced profile outside its results.

The review verdict is that the `BOOK_06 §06.spectral` source locator cannot be
accepted and the registered canonical claim remains unresolved pending
primary-source recovery. The reviewed current Book 06 hash is
`592bbbb1dae9cc599df2eef9cabf117b19f8566d755ad072b77beb04624271d7`; its
introduction-commit hash is
`4adeb0338484ea9ea698ad04751a2c846152c69409ef26f70878c856f8603cb3`. The
claim-introduction `claims.csv` hash is
`5b4c06f9e1af0b46814a9dbbfad30c8dcdb5f53c165da20ed176d36f500f2f45`, the
initial Lean module hash is
`cbb1563817e81f686962be2337b1eec52646a5c342c0348da3bacbf5e5dc1296`, and the
certificate hash at the reviewed current snapshot is
`381038f64926f3a37602975bc72475a5c515608ea526dd5ca9fb999a7f33e75a`.
This review records a locator/source mismatch only. It does not correct claim
status, decide C0 membership, or accept the broader canonical construction.
The broader C0 freeze and independent package acceptance remain open.

The same independent reviewer separately accepted the exact positive-profile
standard-representative slice above after checking its statement and proof
chain. The review verified that the square-root pairing identity, supplied
weighted self-adjointness, and uniqueness of the Hermitian adjoint are the
only mathematical steps. It found no `sorry` or introduced `axiom`; it did not
rerun the build. The reviewed Lean source hashes are
`f982a15b6b56d934fa9fbccdae1d5c9df4c3ecc92139d25f87248e9e39eb2e7d` for
`FiniteWeightedAdjoint.lean` and
`a33d2395336ba949244f0725a1b08bef34f0602e4865be2fc47e7a2a095aff2e` for
`ArchiveWeightedHodgeDirac.lean`. Acceptance is limited to this conditional
algebraic slice; the geometric profile and canonical C0 claim remain open.

### Public D0 import of the native weighted-Dirac capsule (25 October 2026)

The existing exact research capsule
`02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary.lean`
is now reachable through public import `D0.All` without copying or editing
its pinned proof source. `D0.Research.NativeWeightedDiracBoundary.lean` is a
relative symlink to that certificate; the existing `formal_support.csv`
authority records the support locator, and the generated `D0/All.lean`
imports it. The capsule remains byte-identical to its source pin at the
starting head (`git blob 166922e1057cc20f495393e9c53947b52912e3ce`,
SHA-256 `211f43dc97b9c809156bcb87939596757a7143b3e393d4dc4f3215c18d14cff6`).
An independent review accepted the relative target, public import, and
support registration for the repository's Ubuntu CI; symlink support is
required when checking out this module.

The focused `D0.Research.NativeWeightedDiracBoundary` build passed (2,997
Lake jobs). The declaration collector then built the selected public
`D0.All` import and extracted 47 declarations owned by the module: 38 have
source ranges and 9 are generated auxiliaries without ranges. All 47 rows
retain elaborated types, binder/conclusion data, type and proof dependencies,
axiom closure, source path, and toolchain. The 34 propositions explicitly
audited by the capsule and every other collected declaration have only the
recorded `Classical.choice`, `Quot.sound`, and `propext` footprint; one
generated auxiliary uses only `propext`. The exact inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_boundary_inventory_2026-10-25.json`
(SHA-256 `25a98f10bf0d8abc1e9d835c8224a5fa0fdf8cebe3f7698ff4de828ab3bfabdb`,
Lean-source digest
`33e3042c75f5b7f94140dd3eb7cf43735ce90477d3142d0cd4b8865531bf86ef`,
collector SHA-256
`25f0569099c3e7421ca0ef146e23890b66095c5e43b96a1b007684af9608b068`,
snapshot `2b605d0592cce7a5518b704fe1da16328f049694`,
`worktree_dirty=true`, Lean `leanprover/lean4:v4.30.0`).

The mirror retains the capsule's two explicit `maxHeartbeats 0` settings.
They are recorded as exact path/line exceptions in the existing formalization
debt baseline because changing them would change the source bytes pinned by
the research receipts; these settings are proof-resource controls, not axioms
or physical assumptions. No claims or claim statuses changed. The result
formalizes a conditional finite operator family and the stated finite
obstructions; it does not establish selection of a physical profile, an
action/source, or GR. The canonical weighted-Hodge source locator remains
unresolved, and C0 freeze/independent acceptance remains open.

Validation on this slice: narrow module build and public-import inventory
passed; `validate_repo.py` (`lean_closure=923`, 0 warnings), work/protocol
validators, gravity assembly check/render, generated work/Lean views, and
claim-map coverage (Python 3.12.14) passed. Formalization-debt non-growth
passed on 926 modules / 155,195 lines (5 findings, all path-specific
baseline). The generated import preserves `All.lean`'s
existing CRLF convention; the EOL-aware diff check passed. GitHub `D0 guards`
run 5115 passed on commit `db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`. GitHub
`D0 Lean build` run 3077 concluded successfully, but the Draft workflow skipped
release-proof closure and native checkpoint-capsule steps. The declaration
inventory's local build compiled public `D0.All`; this is an integration
check, not the final Ready replay.

### Candidate C0 source-unit map for the native weighted-Dirac capsule (25 October 2026)

This is one source-unit reconciliation slice, not a C0 freeze or acceptance.
Every key below has the common exact prefix
`source:db3091aded8f6cfe8d39dcd973ccf30ec40dfb08:02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md#`;
the source file SHA-256 is
`8c4c662f9f05430ef9f9ff91c670b15e6c678c9b2b1c0ced90e08c79f507e83c` and its
Git blob is `2de670c0e2f9a53104be8105a3554cdd9aaa85e7`. The paired Lean
capsule at the same commit has SHA-256
`211f43dc97b9c809156bcb87939596757a7143b3e393d4dc4f3215c18d14cff6` and blob
`166922e1057cc20f495393e9c53947b52912e3ce`.

| Key suffix | Mathematical unit and formalization boundary |
|---|---|
| `2. Constructive weighted operator, with explicit hypotheses (Eq. 1)` | **Represented at the algebraic core.** For caller-supplied invertible `W` on the actual finite cochains, the capsule defines the weighted codifferential, Dirac map, and pairing, then proves the square, nilpotency, adjoint, and symmetry identities under their stated symmetry hypotheses. The CAR kernel and nilpotency leaves are also rebuilt. It does not prove positivity of `W`, the square-root representative, or the grading consequence. |
| `2. Constructive weighted operator, with explicit hypotheses (positivity and grading consequences)` | **Not represented in this capsule.** It does not prove positivity of `W`, construct `W^{1/2}D_WW^{-1/2}`, or formalize degree preservation. The supplied equivalence `W` is not constrained to preserve degree. |
| `3. Genuine mixed metric dependence is preserved (Eqs. 2–3)` | **Partial.** `inverse_weight_derivative` proves the generic inverse-operator derivative identity. The capsule does not construct the metric compound `W_Q`, prove its minor formula or diagonal agreement, evaluate the ten metric probes, or derive `Q ↦ sQ` operator homogeneity. |
| `Finite mixed spectral moments: a quantitative contrast obstruction (generic identities and annihilator)` | **Partial.** The capsule proves actual trace binding, scalar trace homogeneity, and generic coefficient-independent finite-moment annihilator/error-bound lemmas. It does not formalize the explicit binomial identities. |
| `Finite mixed spectral moments: a quantitative contrast obstruction (physical contrast, Eq. 3c)` | **Not represented as an application.** The capsule does not apply the generic tools to the two curved fibers and probes, derive the physical contrast/refinement lower bound, or prove its field/source premises. |
| `4. Direct flat Lorentz binding on the owned carrier (Eqs. 4–5)` | **Not represented as a full result.** The capsule has CAR/nilpotency facts and an identity-weight specialization, but not the full signed `W_eta` and site/Fock binding, Fourier symbol/dispersion, all-size spectrum, or all-role-order intertwiners. |
| `4. Direct flat Lorentz binding on the owned carrier (Eq. 6, spatial block)` | **Isolated block lemma represented; full application partial.** `rotationBlock`, its square, and `spatial_block_has_no_positive_metric` prove the 2×2 obstruction for nonzero `L`, assuming positive diagonal entries and `DᵀG = GD`. The capsule does not prove this is an invariant restriction of the actual full Lorentz operator. |
| `5. Complete constant-metric null-mode classification (Eq. 7)` | **Generic implication represented; actual classification not represented.** The kernel/range and half-dimension lemmas assume `D² = 0` and a supplied contraction `DK + KD = I`. The capsule does not construct the Fourier contraction on actual null modes, prove the dispersion classification/counts, or show refinement persistence. |
| `6. Fixed-positive-time heat trace cannot supply the claimed refinement (Eq. 8)` | **Conditional inequality represented; spectral application not represented.** The exponential lower bound and its consequence compile from a supplied heat-trace lower bound. The capsule does not define the actual `H_L`, prove its minimum eigenvalue, or derive divergence from the Lorentz spectrum. |

An independent read-only source review verified both exact source blobs and
accepted these scope boundaries. The 47-row inventory has 38 source-ranged
declarations (34 theorems and 4 definitions) and 9 generated/range-less
auxiliaries; the latter are not separate mathematical units. All collected
declarations have only the recorded `Classical.choice`, `Quot.sound`, and/or
`propext` footprints, with no `sorryAx`. The inventory's `snapshot_commit`
`2b605d0592cce7a5518b704fe1da16328f049694` and `worktree_dirty=true` describe
its pre-commit generation; its Lean-source digest
`33e3042c75f5b7f94140dd3eb7cf43735ce90477d3142d0cd4b8865531bf86ef` was
independently recomputed and matches the committed Lean tree at `db3091ad`.
The review accepts this source-to-Lean scope reconciliation only. It does not
make the C0 disposition, semantic package acceptance, physical selection, or
GR closure.
