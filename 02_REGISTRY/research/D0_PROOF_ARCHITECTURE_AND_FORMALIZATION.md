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
`166922e1057cc20f495393e9c53947b52912e3ce`. The current formalization also
consumes two separately pinned later capsule inputs: commit
`c3ceba511bab5c435d715fd56382615fc1dc1505` (blob
`7bb3b8e92c8d9b816ab61f9cb8027061b4820dd9`, SHA-256
`960b0fb2ff4cf0d8fc7f22d99dfa620617b8fc997189d2e00d59aad8d17b0906`) adds
the full-carrier Eq. 6 restriction step; descendant commit
`a6ff3f2fc7e0e6b94d673c2cd713cb4faeb94004` (blob
`60de6702e232d6b68fc3b707a058383c4c09b2ff`, SHA-256
`fdf62644f086ba78c5d1ef203a4d3b7989488395c68afb0920bfa211f5c1d0f3`)
generalizes the null-kernel lemmas to division-ring scalars for the complex
Fourier-fibre application. These later pins supplement the original source
and capsule; they do not change their provenance.

| Key suffix | Mathematical unit and formalization boundary |
|---|---|
| `2. Constructive weighted operator, with explicit hypotheses (Eq. 1)` | **Represented at the algebraic core.** For caller-supplied invertible `W` on the actual finite cochains, the capsule defines the weighted codifferential, Dirac map, and pairing, then proves the square, nilpotency, adjoint, and symmetry identities under their stated symmetry hypotheses. The CAR kernel and nilpotency leaves are also rebuilt. It does not prove positivity of `W`, the square-root representative, or the grading consequence. |
| `2. Constructive weighted operator, with explicit hypotheses (positivity and grading consequences)` | **Partial in separate compiled companions; absent from the pinned capsule itself.** `FiniteWeightedAdjoint.finiteHermitianPairing_weightSquareRoot` proves the square-root pairing identity, and `finiteWeightedConjugate_self_adjoint` proves standard-Hermitian self-adjointness for a caller-supplied positive diagonal profile. `ArchiveWeightedHodgeDirac.cubicalWeightedHodgeDirac_positive_profile_application` and `_standard_representative_application` apply positive-profile pairing, self-adjointness and conjugate representation to the cubical operator; `_square_degree_preserving` proves degree preservation of its square for nonzero supplied diagonal profiles. General `W`, Lorentz-induced `W_Q`, geometric derivation and physical selection remain open. See “Positive supplied-profile standard-Hilbert representative” below. |
| `3. Genuine mixed metric dependence is preserved (Eqs. 2–3)` | **Partial.** `inverse_weight_derivative` proves the generic inverse-operator derivative identity. The capsule does not construct the metric compound `W_Q`, prove its minor formula or diagonal agreement, evaluate the ten metric probes, or derive `Q ↦ sQ` operator homogeneity. |
| `Finite mixed spectral moments: a quantitative contrast obstruction (generic identities and annihilator)` | **Finite-degree identities and their generic application represented.** The capsule binds the actual trace, scalar trace homogeneity, and coefficient-independent annihilator/error-bound lemmas. The companion module now proves the arbitrary-p binomial annihilator, reciprocal-weight normalization, and total variation, then applies the capsule's annihilator to every real coefficient family independent of the scale index. It still does not instantiate the physical fibers/probes or the refinement error bound. |
| `Finite mixed spectral moments: a quantitative contrast obstruction (physical contrast, Eq. 3c)` | **Conditional finite-probe estimate formalized; physical application remains partial.** `eq3c_finite_probe_error_bound` cancels any scale-independent inverse-scale polynomial of fixed degree, applies the owned weighted-error inequality, and returns the stated lower-bound constant under explicit base-action, weighted-remainder, per-scale-profile, and smallness hypotheses. It does not construct the two curved fibers/probes or derive those physical/source hypotheses. |
| `4. Direct flat Lorentz binding on the owned carrier (Eqs. 4–5)` | **Partial, with the all-size operator application now formalized in companion modules.** `ArchiveLorentzianFourierApplication.archiveLorentzianDifferenceOperator_fourier_mode` proves the signed scalar Fourier symbol for every archive period; `ArchiveLorentzianCARDiracApplication.archiveLorentzianCARDirac_square_fourier_mode` proves the full-carrier \(D^2\) bridge, and `archiveLorentzianCARDirac_fourier_mode` / `archiveLorentzianCARFourierFockAction_square` give the exact first-order Fourier action on each 16-component Fock profile and its square. The first-order map preserves each Fourier subspace but acts on its internal profile, so this does not give a global first-order eigendecomposition or multiplicities. Role-order intertwiners and physical metric/source selection remain open. |
| `4. Direct flat Lorentz binding on the owned carrier (Eq. 6, spatial block)` | **Exact all-even-period matrix application, conditional on a separately recorded transfer formalization.** The exact pinned capsule supplies the isolated `spatial_block_has_no_positive_metric` 2×2 result. The PR branch adds the full-carrier restriction lemma at `c3ceba511bab5c435d715fd56382615fc1dc1505` (capsule blob `7bb3b8e92c8d9b816ab61f9cb8027061b4820dd9`): from a positive form, full-matrix self-adjointness, and the two nonzero invariant-vector equations, it derives the contradiction on the entire finite carrier. The application represents the actual weighted CAR/Hodge operator by `LinearMap.toMatrix'` on the complete finite cochain basis and proves the vacuum/B-singleton block for every even archive period `L=N+2`; the earlier L=4 result is an explicit specialization. Neither positivity nor self-adjointness is derived from a physical source, so physical selection remains open. |
| `5. Complete constant-metric null-mode classification (Eq. 7)` | **Partial, with exact per-fibre classification and a full-cochain lower bound now formalized.** `archiveLorentzian_kernel_finrank_cases` proves fibre dimensions 16/8/0 for zero, nonconstant-null, and non-null-symbol modes; `archiveLorentzian_nonzero_null_mode_classification` proves `ker D = range D` and dimension 8 on nonconstant null modes. `archiveLorentzian_nonzero_null_momentum_count_lower_bound` constructs at least $N+1$ distinct diagonal null momenta, and `archiveLorentzian_full_cochain_kernel_finrank_ge_diagonal_family` proves the full-cochain kernel lower bound `16 + 8 * (archiveFibers N - 1)` = $16+8(N+1)$. The complex-fibre use depends on the separately pinned division-ring generalization at `a6ff3f2fc7e0e6b94d673c2cd713cb4faeb94004` above. Exact total null-root count and full kernel dimension, physical gauge quotient, broader refinement classification, and physical/source selection remain open. |
| `6. Fixed-positive-time heat trace cannot supply the claimed refinement (Eq. 8)` | **Conditional inequality represented; spectral application not represented.** The exponential lower bound and its consequence compile from a supplied heat-trace lower bound. The capsule does not define the actual `H_L`, prove its minimum eigenvalue, or derive divergence from the Lorentz spectrum. |

An independent read-only source review verified both exact source blobs and
accepted these source-to-capsule scope boundaries at that checkpoint. The 47-row inventory has 38 source-ranged
declarations (34 theorems and 4 definitions) and 9 generated/range-less
auxiliaries; the latter are not separate mathematical units. All collected
declarations have only the recorded `Classical.choice`, `Quot.sound`, and/or
`propext` footprints, with no `sorryAx`. The inventory's `snapshot_commit`
`2b605d0592cce7a5518b704fe1da16328f049694` and `worktree_dirty=true` describe
its pre-commit generation; its Lean-source digest
`33e3042c75f5b7f94140dd3eb7cf43735ce90477d3142d0cd4b8865531bf86ef` was
independently recomputed and matches the committed Lean tree at `db3091ad`.
This 47-row inventory is the historical inventory of the pinned capsule. The
later Fourier/kernel companions have a separate 240-declaration inventory
across four selected modules, recorded below under “Typed full-cochain CAR
operator and additive null-kernel bound”; it is not a replacement or
reinterpretation of the historical capsule inventory.
The review accepts this source-to-Lean scope reconciliation only. It does not
make the C0 disposition, semantic package acceptance, physical selection, or
GR closure.

### Arbitrary finite-moment identities in Lean (25 October 2026)

The companion module
`D0.Research.NativeWeightedDiracMomentIdentities` formalizes the generic
identities used in source §3 for every fixed finite degree `p`. With
`s_r = 1/(r+1)` and `w_r = (-1)^r * choose(p+1,r)`, it proves
`sum_r w_r * s_r^(-j) = 0` for `0 <= j <= p`,
`sum_r w_r * s_r = 1/(p+2)`, and `sum_r |w_r| = 2^(p+1)`. The theorem
`fixedDegreeScaleContrast_eq_zero` applies the already-owned
`finite_moment_annihilator` to any real coefficient family independent of the
scale index. The proof of the first identity uses a Pascal recurrence and the
binomial expansion of the shifted power; the two normalization identities
use the alternating-binomial sum and the row-sum identity.

This vertical slice consumes the generic capsule result and closes its
explicit finite-degree algebraic gap. It does not derive the actual curved
fibers, the physical action/source coefficient binding, the contrast transfer
error bound, or its refinement premise from a native execution. The §3 Eq.
(3c) application remains outside this Lean module.

The module is registered through the existing `formal_support.csv` authority
and generated public `D0.All` import; it does not add a claim or change claim
status. Its focused build passed (2,998 Lake jobs). The declaration inventory
compiled public `D0.All` and records 29 declarations (22 theorems, 7
definitions; 18 source-ranged and 11 generated auxiliaries), all with
elaborated types and collected proof details. Axiom closures contain only
`Classical.choice`, `Quot.sound`, and `propext`; no `sorryAx` occurs. Inventory
SHA-256 is
`8b22aaf3a2b6483f1584684417f2b17e90f899951c44c00485debc9089904e33`, Lean
source digest
`e1e6aa4c7ca3e2c395a1864e7eea72e77b6480cb9dc1135dec297cd4f04d9478`, and
collector SHA-256
`97eb93d8f8d3ef715c4932cf33fc79d9deddb95c67ed565ab6e6d4f5841cacad`.
The Lean module SHA-256 is
`eeb9cec30eaea1192d41f42be32a0eb4f720bfaeb8b9fbec3e8bf514a388b98f`.
The inventory records `snapshot_commit=6ac2da8113003c8141cfba10dbb14c0499a205d7`
and `worktree_dirty=true`; that provenance describes generation before this
checkpoint commit. This is a formalized generic identity/application, not
independent C0 acceptance or physical GR closure.

Structural validation on the final local slice passed: repo validation
(`claims=889`, `assumptions=31`, `formal_support=191`, `lean_closure=924`, zero
warnings), work/protocol checks, gravity assembly check/render, generated
Lean-view check, ClaimMap coverage, formalization-debt non-growth (5 findings,
all baseline), and the EOL-aware diff check. The declaration inventory built
the public import, but this checkpoint is not the final Ready `D0.All` replay.
The cold-start query `finite weighted moment identities binomial scale
contrast` returns this Lean module as the leading direct-content candidate and
now carries the exact source commit/blob/§3 pin in its result card. No
independent review of the new mathematical application is claimed here.

### Conditional finite-probe application of Eq. (3c) (25 October 2026)

The same source-pinned module now proves
`D0.Research.NativeWeightedDiracMomentIdentities.eq3c_finite_probe_error_bound`.
For `p+2` finite scales `s_r=1/(r+1)`, it assumes the paired error profile is
the scale-linear base contrast plus an arbitrary degree-`p` polynomial in
`s_r⁻¹`, plus a remainder. The arbitrary polynomial coefficients may be any
real values but are independent of the scale index. The proof uses the
previously formalized binomial moments to cancel that polynomial and the
capsule's `finite_annihilator_error_bound` to show that every uniform envelope
`M` for the two experiments' errors obeys
`9π² ε / (400 (p+2) 2^(p+2)) ≤ M`.

The statement keeps the physical inputs visible: `h=ε³`, an explicit
`ε < eq3cSmallnessThreshold p Cbase Crem`,
`|d + 9π²/200| ≤ Cbase*h`, and a weighted remainder bound `≤ Crem*h`.
Thus it formalizes the finite weighted-contrast/error calculation and its
constant. It does not construct the two curved fibers or probes, prove the
per-scale error decomposition from their actual native source, derive the
`d_h` estimate or weighted remainder bound, or establish their field/source
premises. Those applications remain open; no C0 acceptance or physical GR
selection is inferred.

The refreshed inventory compiled public `D0.All` and records 42 declarations
(34 theorems, 8 definitions; 20 source-ranged and 22 generated auxiliaries),
with no `sorryAx`. The new theorem's elaborated type retains all of the
conditions above; its axiom footprint is `Classical.choice`, `Quot.sound`,
and `propext`. Inventory SHA-256 is
`da78195683883f011ef9df904c58dd78bc0085356a6ab50fe774ee0b3d11ebdf`, the
Lean-source digest independently recomputed from the current tree is
`f32c5db2f5cafb1ad13d770039cb30f9eb967ef0160c8cf6ee3d22d733b003e8`, the
Lean module SHA-256 is
`065b01fc6a7af15ed898f2454ffff789fc1177f2c4e90568114e7e817ea334a3`, and the
collector SHA-256 remains
`97eb93d8f8d3ef715c4932cf33fc79d9deddb95c67ed565ab6e6d4f5841cacad`. The
inventory records pre-commit snapshot `59ff3ab5dd20cd1b957690d1976091baf580f776`
with `worktree_dirty=true`.

The narrow Lean target built successfully (2,998 Lake jobs). The declaration
inventory's public-import build compiled `D0.All`; this is not the Ready
integration replay. The cold-start suite found all 18/18 required sources and
passed all 19/19 search/impact cases. A fresh direct query returned this Lean
module first as direct content with `pin_complete=true` and the same exact
commit/blob/§3 source reference. Repository validation passed
(`claims=889`, `assumptions=31`, `formal_support=191`, `lean_closure=924`, zero
warnings); generated Lean views were current, ClaimMap coverage passed under
Python 3.12.14, formalization-debt non-growth stayed at its five baseline
findings, and `git diff --check` passed. The supporting source is pinned to §3 of
`A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md` at commit
`db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, blob
`2de670c0e2f9a53104be8105a3554cdd9aaa85e7`. Independent theorem review and
application acceptance have not occurred. The PR remains Draft and the task
remains `IN_PROGRESS`.

### Conditional full-carrier transfer of the Eq. (6) spatial-block obstruction (25 October 2026)

The PR branch extends the capsule mirror with `matrix_adjoint_pairing`, which
derives the vector bilinear identity from the full matrix equation
`TᵀG=GT`, and `positive_selfadjoint_spatial_invariant_block_impossible`.
The latter takes a positive quadratic pairing on the finite carrier,
full-matrix self-adjointness, and two nonzero vectors `u,v` with
`Tu=-2L v` and `Tv=2L u` for `L≠0`; it derives a zero sum of their positive
diagonal pairings and closes the contradiction. The exact source-pinned
capsule at commit `db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, blob
`166922e1057cc20f495393e9c53947b52912e3ce`, contains the isolated
`spatial_block_has_no_positive_metric` 2×2 proof, not these two transfer
lemmas. The branch extension was added at commit
`c3ceba511bab5c435d715fd56382615fc1dc1505`; its capsule blob is
`7bb3b8e92c8d9b816ab61f9cb8027061b4820dd9` (SHA-256
`960b0fb2ff4cf0d8fc7f22d99dfa620617b8fc997189d2e00d59aad8d17b0906`).
This is a separately reviewable Lean formalization delta from the pinned
source. The full-carrier theorem does not assume the pairing is diagonal or
the carrier is two-dimensional.

This closes only the conditional linear-algebra transfer in source §4, Eq.
(6). It does not define the selected full Lorentz CAR matrix, construct the
empty/B-singleton vectors on its complete carrier, prove the two action
equations for that operator, or establish positivity/self-adjointness from a
physical source. Therefore the actual §4 application remains partial, with no
physical matter selection or GR closure inferred.

The rebuilt narrow target is `D0.Research.NativeWeightedDiracBoundary` (2,997
Lake jobs). Its refreshed public-import inventory records 49 declarations
(45 theorems, 4 definitions; 40 source-ranged and 9 generated auxiliaries),
including the two additions above. Both have only
`Classical.choice`, `Quot.sound`, and `propext` in their transitive axiom
closures; neither introduces a computation axiom or `sorryAx`. The inventory
was generated at pre-commit snapshot `524397d6ac89d90e5c07df73f9a3a675759e384d`
with `worktree_dirty=true`. Its whole-Lean-source digest
`06113c1f8fef43734facd63ccce691f892feb314faf68fb8d2f9e8bc79f72040` was
recomputed independently from the current formalization tree. Inventory
SHA-256 is `4cdef1c106efb55a9c976b4d7883147a8be49ea334b56347e6b7bad3880c2c21`,
Lean capsule SHA-256 is `960b0fb2ff4cf0d8fc7f22d99dfa620617b8fc997189d2e00d59aad8d17b0906`,
and collector SHA-256 is
`25f0569099c3e7421ca0ef146e23890b66095c5e43b96a1b007684af9608b068`.
The inventory's public import root is `D0.All`. This is a supporting
mathematical result, not an independent acceptance of the source application.

### Exact L=4 CAR/Hodge instantiation of the spatial Nyquist block (25 October 2026)

The separately registered adapter
`D0.Research.NativeWeightedDiracNyquistApplication` in
`03_FORMALIZATION/D0/Research/NativeWeightedDiracNyquistApplication.lean`
consumes the branch-local full-carrier transfer lemma recorded above. The
source pin remains the original §4 Eq. (6) memo and capsule; the L=4 adapter
does not claim that the new transfer lemma was present in that pinned blob.
It uses the existing `flatLorentzSubsetWeight` on the actual
`ArchiveRolePhaseGroup 2 × ArchiveFockState` cochain carrier and the owned
`dForward`/Hodge-CAR codifferential. For the period-four B character at
`L=4`, it proves the two operator equations
`D_W vacuum = -8 • BState` and `D_W BState = 8 • vacuum`, and proves both
vectors are nonzero. It then represents the same linear operator using
`LinearMap.toMatrix'` and `Matrix.mulVec`, and applies the existing full-carrier
obstruction to conclude that any positive-definite quadratic form on this
complete finite coordinate carrier is incompatible with self-adjointness of
this matrix.

This is an exact formal application of the source's Eq. (6), not a physical
selection result. The theorem is conditional on a supplied positive form and
matrix self-adjointness equation; it derives neither premise and does not
claim that D0 selects either one. The remaining physical/source application,
all-size Fourier/spectrum results, and native action selection remain open.
Phase: Lean application/transport of a pinned conditional result, not native
physical realization. Parent substitution: the prior missing step “the exact
CAR operator, its two vectors, and both invariant-action equations are not
instantiated” is replaced by the concrete `L=4` weighted-operator matrix and
its two nonzero-vector equations on the full finite cochain carrier. Remaining
assumptions: a positive full-carrier quadratic form and self-adjointness of
that matrix are supplied only as hypotheses to the impossibility theorem; no
physical source derives them, and the theorem establishes no D0/GR selection.
This architecture WORKER has no scientific assembly binding; the prescribed
`gr_assembly.py template WRK-D0-PROOF-ARCHITECTURE-FORMALIZATION` correctly
returns `unknown scientific binding`, so no gravity assembly result/status was
created.
The adapter is explicitly registered by `formal_support.csv` and the generated
`D0.All` import. The original pinned source bytes and receipt remain
unchanged; the PR branch adds the separately identified formalization delta
to the capsule mirror as recorded above. Its source input is pinned to §4,
Eq. (6) of
`02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md` at commit
`db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, Git blob
`2de670c0e2f9a53104be8105a3554cdd9aaa85e7`.

The focused build of `D0.Research.NativeWeightedDiracNyquistApplication`
passed (3,005 Lake jobs); the public-import inventory compiled `D0.All`.
The inventory records 83 declarations (71 theorems and 12 definitions; 54
source-ranged and 29 generated/range-less), with the operator block, matrix
bridge, and conditional obstruction included. The exact input snapshot was
`c3ceba511bab5c435d715fd56382615fc1dc1505` with `worktree_dirty=true`; this is
pre-commit provenance, not a claim that the inventory was generated from the
eventual checkpoint commit. The whole-Lean-source digest is
`52af7566629ee534bc96f1842244f12a0a3bd324c6739b9a53c93f23c9ac553d`, the
adapter SHA-256 is
`d6b6f2231aea7963591f8251e2c7705d22676b0defe524a4d06120aa7e31cc40`, the
inventory SHA-256 is
`b3d500f042b88c40f7fa4ae0498006a31252367c7071e69fa0b124099e020ccf`, and the
collector SHA-256 is
`7f8d83cda9105151a2e6e07bd66a5f1cdf03fa35f9bb6a5da336ac4324593c5a`.
The inventory file is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_nyquist_application_inventory_2026-10-25.json`.

The main operator theorem inherits the five existing `native_decide` CAR
proof leaves in addition to `Classical.choice`, `Quot.sound`, and `propext`;
the matrix bridge and conditional application add no further axiom. No
`sorryAx` occurs. Repository validation passed (`claims=889`, `assumptions=31`,
`aliases=58`, `formal_support=192`, `lean_closure=925`, zero warnings), as did
work/protocol, assembly check/render, generated-work-view and generated-Lean
view checks. The generated `D0.All` file retained its repository-standard
CRLF line endings; the EOL-aware diff check passed. This is a supporting
mathematical result, not independent source acceptance or physical GR
selection. The PR remains Draft and the execution remains in progress.

### Reusable typed matrix interface for the weighted Hodge--Dirac operator (25 October 2026)

The new support module
`D0.Research.NativeWeightedDiracLinearOperator` provides one reusable API
between the function-level weighted operator and the finite cochain matrix.
`weightedCodiffLinear` conjugates the owned `hodgeCodifferentialₗ` by the
caller-supplied equivalence `W`; `weightedDiracLinear` adds the owned
`dForwardₗ`; and `weightedDiracMatrix` uses `LinearMap.toMatrix'` in the
unchanged `ArchiveCochainBasis` coordinates. The theorem
`weightedDiracMatrix_mulVec` proves that multiplying this matrix by any
cochain vector is exactly `weightedDirac N W ψ`. Thus later applications reuse
the same typed transport instead of rebuilding a bespoke matrix wrapper.

The L=4 flat-Lorentz Nyquist adapter now consumes this generic matrix API and
still proves the same two exact vacuum/B-singleton action equations and the
conditional full-carrier positive-form/self-adjointness obstruction. The
generic API carries only `Classical.choice`, `Quot.sound`, and `propext`; the
specific CAR application retains the five existing `native_decide` leaves
listed in the prior checkpoint. Neither module selects a positive `W`, a
physical pairing, or a native action.

Both focused Lean targets pass: `D0.Research.NativeWeightedDiracLinearOperator`
(2,998 Lake jobs) and `D0.Research.NativeWeightedDiracNyquistApplication`
(3,006 Lake jobs). After removing the redundant application-local linear-map
wrapper, the paired-module declaration inventory compiled the public import
`D0.All` and records 87 declarations (73 theorems, 14 definitions; 58
source-ranged, 29 generated/range-less). Its exact snapshot is
`51a1c3162fa3dd625c7513e33939bf03e023af0a` with `worktree_dirty=true`;
Lean source digest is
`825bf290d3252802ae9605772cfe8cee00acd7fff0ed25fc05954d2a0cae4305`, paired
inventory SHA-256 is
`acb4b9baa771ac53e347495aa7acb5c80f7754812f98b62a22e176e0a56a3f8c`, module
collector SHA-256 is
`424ca2786503d04e4f7bbf9e02cc722fea312ac7a3eb5dc7340a38a077a42478`, and
the two Lean source SHA-256 values are
`d3d36f1994dce386d192984f16ba6c14feeb021ff3097370aa7030c806736fb0` and
`dd09c1f72e436b77c303abd75c4bd839b77ad8dcbfe94886b37c027ba9b6c732`. The
inventory is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_linear_matrix_adapter_inventory_2026-10-25.json`.

The compiled all-result crosswalk and all-claims name-resolution snapshot
were regenerated from that same public-import source digest and pre-commit
snapshot. The crosswalk contains 54 results and 191 evidence records: 182
verified source pins, eight unavailable blobs, and one pinned hash mismatch.
It shows 22 exact section references and 140 ranked heading candidates across
35 results; 37 result rows still have incomplete section mapping. All 54
semantic relations remain unresolved and `acceptance_inferred=false`. The
compiled view enumerates 1,001 co-located declarations, ten explicit
declaration locators, 18 claim-locator candidates, and nine formal-support
candidates; these are review inputs, not accepted edges. The refreshed file
is `02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/assembly_result_declaration_crosswalk.json`,
SHA-256 `b5bb87576d899d48cb0c3f063432084010cc3efbf632409ff8ea7b0a92a4b8e4`;
its collectors are `5e9074769ba45eb74e6ade808f9aaac82dd09454e14941d6aea6c7885051b0f1`
and `e936c031368d608029317bb6e746954ad507a986885b9a29a9a4e8c54d711bdc`.

The resolution-only view records the same Lean source digest, claims registry
SHA-256 `e2fcba29050a9017aa6d1e7501f192e6209d2f6c04d8e9b791930c4e54c6cbf5`,
and 889 claim rows. It expands 2,751 theorem-locator mappings and 8,458
candidate references to 8,323 unique names; 2,512 resolve and 5,811 do not.
At the mapping level 2,553 have at least one match, including four ambiguous
mappings; 176 have no candidate name and 22 have candidates but no match. A
total of 709 claim rows have at least one match and 180 have none. These are
exact current-name availability counts, not semantic coverage or C0
acceptance. The file is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_current.json`,
SHA-256 `fc3701d1ab339e009d57aaf74603c0127448f0ef219d3c63e93b78960916bc35`,
collector SHA-256
`dd33d4ab45852eb1d2aef0311f00db6249832d41f9957a50e29b5e3e51f953a8`.
Both refreshed views remain provenance and locator evidence only; C0 stays
unfrozen and independent semantic acceptance remains outstanding.

### Cold-start replay and independent review of the weighted-Dirac matrix adapter (25 October 2026)

The repeatable cold-start set now includes a distinct case for the generic
typed matrix bridge and its exact L=4 consumer. The 19-case replay at snapshot
`16b7b62e59f5f43c2db94d33f808c733d1992137` found all required source paths in
19/19 cases; the 20th benchmark control also passed, showing that a declared
source edit changes its dependent input while unrelated prose leaves it
unchanged. The new case found the generic API at rank 1, the L=4 application
at rank 2, the source memo at rank 2, and the capsule mirror at rank 15, all
as direct content with a candidate window of 18. Its required references are
the §4 source memo, the certificate capsule mirror, and the two Lean modules.
The case states that the original pin supplies the isolated 2×2 result while
the full-carrier transfer is a separately identified PR delta; the search
results remain retrieval candidates, not accepted semantic edges.

The focused `tools.test_proof_architecture` suite passes 41/41 tests,
including a regression that keeps the db309 source pin separate from the
c3ceba full-carrier implementation delta. The cold-start runner SHA-256 is
`9d3bb55cdfbfec94895ad1030a9b9fc74b95865af9108d6a2beb5daafa4fbdc5`; its
focused test module SHA-256 is
`825014016b7372fb31f8c4b9f4ce6cc2535baf4fad2ce0e40e8c06577673196c`.
The replay used `worktree_dirty=true` on the published base commit shown above;
the Lean-source digest and registered authority inputs are the same as the
paired inventory and refreshed crosswalk documented immediately above.

An independent read-only review confirmed that `weightedDiracMatrix_mulVec`
uses the unchanged `ArchiveCochainBasis` coordinates, the L=4 specialization
retains the site×Fock carrier and proves the stated −8/+8 action equations,
and the paired inventory reports the same five existing CAR `native_decide`
leaves with no `sorryAx`. The reviewer found no mathematical or coordinate
composition error. It separately identified that the full-carrier transfer
lemma was absent from the original db309 capsule blob; this is now recorded
as the c3ceba branch implementation delta above, not as content of the source
pin. The review is limited to this finite mathematical application and does
not accept C0 membership, a physical pairing, action/source selection, an
all-size spectrum, or GR closure.

### Identity-weight matrix adapter for the existing Hodge/CAR operator (25 October 2026)

The reusable matrix interface now has an exact identity-transport
specialization. `weightedCodiffLinear_identity_eq_hodgeCodifferential` reduces
the conjugated codifferential to the owned `hodgeCodifferentialₗ`; its proof
uses the literal identity equivalence. `weightedDiracLinear_identity_eq_hodgeCarDirac`
then consumes the existing theorem that the counting codifferential is the
finite-Hermitian adjoint of `dForwardₗ` and identifies the generic operator
with `hodgeCarDiracₗ`. The resulting `hodgeCarDiracMatrix_mulVec` states that
the matrix in the unchanged `ArchiveCochainBasis` acts exactly as the existing
function-level Hodge/CAR operator for every cochain. This is an API/application
bridge; it selects no nonidentity weight, positive pairing, physical Hodge
profile, action, or source.

The focused Lean build passed for
`D0.Research.NativeWeightedDiracLinearOperator` (2,998 Lake jobs). The paired
inventory for this adapter and its L=4 consumer was
rebuilt by compiling the public import `D0.All` on dirty snapshot
`8687da5602a1ca327802827a778567faa646e15f`, with Lean source digest
`d938fdbea247eb87434f81aa5bc1859f192ef69db6faf04cbedbe1f50b00146c` and
toolchain `leanprover/lean4:v4.30.0`. Compared with the previous paired
inventory it adds four declarations and removes none: the three named
theorems above plus the generated `weightedCodiffLinear.eq_1` equation
theorem. The three named theorems have the existing
`[Classical.choice, Quot.sound, propext]` footprint. The resulting inventory
contains 91 declarations (77 theorems, 14 definitions); collector SHA-256 is
`424ca2786503d04e4f7bbf9e02cc722fea312ac7a3eb5dc7340a38a077a42478`, and
the paired JSON SHA-256 is
`ffdde5c6f401f4b150b74fc3e6f1e8a14f019a76437dcc6dc5d5281ec1515364`.

Both generated compiled views now use that same Lean source digest and
snapshot. The 54-result assembly crosswalk has 191 evidence records (182
verified source pins, eight unavailable pinned blobs, one pinned hash
mismatch); all 54 semantic relations remain unresolved and no acceptance is
inferred. Its JSON SHA-256 is
`761bd39f097a6f7565352eb0b8bcbed67d22743ad929e9bc432b9f295d0fd1bb`.
The 889-row claims resolution has 2,751 theorem-locator mappings and 8,458
candidate references over 8,323 unique names; 2,512 resolve and 5,811 do not.
At least one candidate resolves for 709 claim rows, while 180 have none.
These are current name-locator counts, not semantic coverage or C0 status;
its JSON SHA-256 is
`1d6ca5a9fa93087e526060c9042ea7e13c1f8eaea9b87d3b4dd4b9d2cd6e395e`.

The existing cold-start case now searches for both the supplied-weight matrix
bridge and its identity-weight Hodge/CAR specialization. The replay found all
required sources in 19/19 cases, and the 20-case exact-source versus unrelated
prose impact control passed. The focused proof-architecture suite passed
41/41. Runner SHA-256 is
`6dd358a2f008ea8fc334db51a72c82770ab0c48f9bca567814617aa65bf93dc8`, and
test SHA-256 is
`d8e34623e720f425b5fd7b2a9e37c6eff3baf0a5982d5d547c1eafd7b9205f35`.
The checkpoint consumes an existing adjoint identity and adds one concrete
finite-carrier application; it does not freeze C0 or independently accept
semantic mappings. Full C0 dispositions, independent C0 acceptance, broader
library migration, and the remaining GR/physical premises stay open.

### Self-adjoint operator to symmetric matrix application (25 October 2026)

The typed matrix API now exposes the finite-coordinate consequence of the
existing adjoint interface. `weightedDiracMatrix_symmetric_of_finiteHermitianAdjoint_eq_self`
proves that whenever the supplied weighted Dirac linear map equals its
`finiteHermitianAdjoint`, its matrix in the same `ArchiveCochainBasis` is
symmetric. The proof reads an entry from the adjoint identity on coordinate
vectors, retaining the real finite-carrier convention explicitly. The
concrete `hodgeCarDiracMatrix_symmetric` application sets the transport to the
identity and consumes the existing
`hodgeCarDirac_finiteHermitianAdjoint_eq_self` theorem. This is a matrix
representation of the registered counting Hodge/CAR operator; it does not
assert positivity of a weighted form, select a geometric Hodge profile, or
identify the distinct nearest-neighbour hopping `carDirac` with the Hodge
difference operator.

The narrow Lean target
`D0.Research.NativeWeightedDiracLinearOperator` passed (2,998 Lake jobs),
including the unchanged function-action and new matrix-symmetry applications.
The new declarations have only `Classical.choice`, `Quot.sound`, and
`propext`. Paired enumeration of the generic API and L=4 consumer on dirty
snapshot `d90cb89fa5c615c21db76a1cc12ba0571a4f3fb2` compiled public import
`D0.All` with Lean 4.30.0 and source digest
`2de2f2ab07d7a828bf5a19176904e72e6bf5457615de3e01da4d2a76edb8c14c`. It
contains 94 declarations (80 theorems, 14 definitions), adding three names
relative to the prior 91-row paired inventory and removing none. The additions
are the two matrix-symmetry theorems and generated equation theorem
`weightedDiracLinear.eq_1`. Collector SHA-256 remains
`424ca2786503d04e4f7bbf9e02cc722fea312ac7a3eb5dc7340a38a077a42478`; paired
inventory SHA-256 is
`a755142a1d543389b2e2198bdf1aac8b60ed00620a9e5898394eca2d625554d2`.

The all-claims resolution and 54-result assembly crosswalk were regenerated
against that same source digest and snapshot. Name-resolution counts remain
889 claim rows, 2,751 mappings, 8,458 references and 8,323 unique candidates;
2,512 names resolve. These remain locator counts, not semantic coverage.
Current JSON SHA-256 values are
`f78a8b7cebaa2189bda821588f5541c8ec49a71d355ec81ffdc8e35347c90a42` for the
claim resolution and
`edfc8d3ee06ed8e575fb999a81f8dd2c9bc028aec4a6e56d9bf3c28ab27264f9` for the
assembly crosswalk. C0 is still unfrozen and these generated views do not
independently accept semantic edges or close a physical premise.

The updated cold-start replay found all required sources in 19/19 cases;
its 20-case exact-source versus unrelated-prose impact control passed. For
the new matrix-symmetry query, the primary memo and then the Lean API module
ranked as direct content, followed by the paired inventory. The focused
proof-architecture suite passed 41/41. Runner SHA-256 is
`e68106a1d752bc67e73ef6caf738abe603ec08b1fce8e511d99e12cfda1c70bc` and test
SHA-256 is
`7aae6a5920cb0c1ffa60832e65ea5f1b50fef1aecd82d99ed38fe5597392be76`.

### All-even-period CAR/Hodge Nyquist block on the full archive carrier (25 October 2026)

The `L=4` application is generalized to every even archive period
`L = archiveFibers N = N + 2`. For `Even (archiveFibers N)`,
`evenGridAlternatingSign` defines the alternating character from the actual
`ZMod L` representative. Its translation lemma handles wraparound using
evenness of `L`; the character flips under the spatial B translation and is
unchanged under the other Role translations. The owned forward and backward
differences therefore act by `-2L` and `+2L` on the scalar character. On the
actual archive cochains, the CAR/Hodge weighted Dirac action is
`vacuum ↦ -(2L) • BState` and `BState ↦ (2L) • vacuum`.
`spatialNyquistEven_weightedDirac_matrix_block` transfers these equations to
the existing matrix in the unchanged `ArchiveCochainBasis` coordinates, and
`spatialNyquistEven_weightedDirac_matrix_block_L4` proves compatibility with
the prior `-8/+8` specialization.

The companion theorem
`flatLorentzWeightedDiracEven_no_positive_selfadjoint_pairing` applies the
existing invariant-block argument at every such even period: any supplied
matrix `G` that is positive on every nonzero real cochain and satisfies
`DᵀG = GD` yields a contradiction. This is conditional on those two
hypotheses; it derives neither the positive pairing nor self-adjointness from
a physical source. The formalized parent substitution is specifically the
all-even finite-carrier extension of Eq. (6). The signed scalar second-order
dispersion from Eq. (5) now has an all-size Fourier application on the actual
site × Fock carrier, recorded below. The first-order CAR symbol and its
square-to-source bridge, the full first-order Dirac spectrum, all-role-order
intertwiners, physical action or source selection, independent source
acceptance, and GR closure remain open. No C0 disposition or acceptance is
inferred.

The source remains pinned to §4, Eq. (6) of
`02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md` at commit
`db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, blob
`2de670c0e2f9a53104be8105a3554cdd9aaa85e7`; the original source pin is
unchanged. The result is a branch-local Lean extension that composes the
previous full-carrier L=4 adapter with the same conditional transfer on each
even `N+2` carrier.

The focused build of `D0.Research.NativeWeightedDiracNyquistApplication`
passed (3,006 Lake jobs). On the pre-commit snapshot
`fdebdc21a54eafe4fa877e51fdc684e657b4dd03` with `worktree_dirty=true`, the
public-import inventories compiled `D0.All` under
`leanprover/lean4:v4.30.0`. The module-only inventory contains 135 declarations
(117 theorems, 18 definitions); the paired linear-operator/application
inventory contains 152 declarations (131 theorems, 21 definitions). Their
shared whole-Lean source digest is
`e156d37e8100174bed48b1db6fdc5f0b5dc97f411700b0c312cc3576ffd32c9c`.
The application source SHA-256 is
`d00f24cef74cf117c2f085527101ff195aa5e5140b1f52d190e2f1f503b691f2`.
The module-only and paired inventory JSON SHA-256 values are
`5b74c0cf477804eb1a0f894005a86ebb8310c6a00ebceb79371330cea050a28f` and
`6572199b500e49ee456c3f4e34af675d93226816d3cd85f0072f4b25e18758c8`,
respectively. The paired declarations contain no `sorryAx`; the concrete
CAR/Hodge equations retain the same five existing CAR `native_decide` leaves,
with no new axiom introduced by the even-period extension.

The all-claims name-resolution view and 54-result assembly crosswalk were
refreshed against the same Lean digest and snapshot. The 889 claim rows still
produce 2,751 locator mappings and 8,458 candidate references over 8,323
unique names; 2,512 names resolve and 5,811 do not. At the mapping level,
2,553 have at least one name match, four are ambiguous, 176 have no candidate
names, and 22 have candidates but no match. These locator counts are not
semantic coverage or C0 acceptance. The crosswalk retains 191 evidence
records (182 verified source pins, eight unavailable blobs, one pinned hash
mismatch), 22 exact section references, and 140 ranked section candidates
across 35 results; 37 results have incomplete section mapping. All 54 semantic
relations remain unresolved and `acceptance_inferred=false`. The refreshed
claim-resolution and crosswalk JSON SHA-256 values are
`7101999f010f11cfb9bb73fb5e24cddccccac58c69bfc99befe55a38ff178e25` and
`a5375df20f1bfc1468ee7fa5813f1f1e876a96328317aaef976bc9be15c47daa`; the
declaration, name-resolution, and crosswalk collectors remain
`424ca2786503d04e4f7bbf9e02cc722fea312ac7a3eb5dc7340a38a077a42478`,
`dd33d4ab45852eb1d2aef0311f00db6249832d41f9957a50e29b5e3e51f953a8`, and
`5e9074769ba45eb74e6ade808f9aaac82dd09454e14941d6aea6c7885051b0f1`.
The views are current name and source-locator evidence only; they accept no
semantic edge and close no scientific or physical premise.

The native weighted-Dirac cold-start case now asks for both the all-even
matrix block and the conditional positive-self-adjointness no-go. In the
19-case replay, all 19 cases found every required source directly within the
18-candidate window, and the 20th exact-source/unrelated-prose impact control
passed. For both new exact-name queries the primary memo ranked first and the
Lean application module ranked second; the source memo, capsule mirror, typed
matrix API, and application module were all retrieved. The semantic scope
review remains manual; these search results are candidates, not accepted
relations. `tools/test_proof_architecture.py` passed 41/41 tests. The runner
SHA-256 is
`37bfb2769d2a913d87889c82cccac2b008801746de6d44e171b476611393c128` and the
focused test SHA-256 is
`030b5248d3c01115697ddf5dae57c2af7b0b04967340ba8d8cc1ac8808837273`.

### All-size signed Fourier application for the Eq. (5) scalar symbol (25 October 2026)

`D0.Geometry.ArchiveLorentzianFourierApplication` composes the owned generic
product-cycle coordinate-difference eigenvalue with the archive carrier
`Role → ZMod (N+2)`. For arbitrary real role weights it proves that every
product character is an eigenvector of the finite signed second-difference
expression. Specializing the existing `roleLorentzSign` gives the exact
`A/B/C/D` symbol
`4L²(sin²(πk_A/L) − sin²(πk_B/L) − sin²(πk_C/L) − sin²(πk_D/L))` for every
`L=N+2`, with no extra period or mode premise. The Fockwise lift has the same
eigenvalue for every coefficient profile; its mode embedding is injective,
and the existing product Fourier inversion is specialized to every archive
scalar site field. The existing Fock carrier has 16 labels, so this preserves
all sixteen coefficients over each Fourier mode without asserting a global
eigenvalue multiplicity when distinct momenta share an eigenvalue.

This result does **not** construct the first-order Lorentzian CAR operator
`Dη(k)=Σ[aᵣcᵣ†−εᵣbᵣcᵣ]`, prove that its square is the signed difference
expression on the actual carrier, or select a physical role metric/source.
The weights are the already-declared role-sign assignment. Therefore the
source Eq. (5) first-order-to-second-order application and full Dirac spectrum
remain open; the formalized theorem is its all-size scalar-symbol consequence,
not a completed Eq. (5) physical claim.

The compiled declaration inventory uses Lean 4.30.0 and import root `D0.All`;
it records 28 elaborated declarations from the owning module, with signatures,
dependencies, axiom footprints, source paths, and current Lean source digest
`6645b9c4163233883a8c614242345a2990e00ad7d6574e25b0705e83bb0cb543`. Its
collector SHA-256 is
`68f8eb4de8ff4110b0cc4174a2cf4877efb707ddfb3326020d7cd22c46b7b87a`; the
inventory JSON SHA-256 is
`8b81f6b1a54733396c8b6474d8ad1c3551a0e95b46e8dc03382c0e232555211a`. The
inventory records source snapshot `d63ffb2dd737f70a801a6ef79c5d39369d056ed1`
and a dirty worktree. The new Lean module SHA-256 is
`bdb424320b5171227297c069a1fbcf12590e5ee192d8510fe2ad924aa99a4474`.

The final 19-case cold-start run found all required source sets; all four
new exact-declaration queries rank the application module first, and the
compiled inventory ranks second for the signed Laplacian and Fock-mode
queries. The 20th exact-source/unrelated-prose impact control passed. The
complete output is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_fourier_cold_start_2026-10-25.json`
(SHA-256 `88a73db2d582499ccd342726b0e9462c54c427bd0880a91e5c717f1fbbc25927`).
Its input snapshot is `d63ffb2dd737f70a801a6ef79c5d39369d056ed1` with a dirty
worktree; the `formal_support.csv` digest is
`288b76ab1e583de5cca75dc9cb55d93863d82bedbb06697c66fa6422dc96c436`. The
cold-start runner SHA-256 is
`059f053ef9b83b7e0d81e46c8904573c5ad12f82a330e7cb6a05c65dcba6cb22`, and the
focused test SHA-256 is
`b445e77f86f83cab4b1d170087c24c05a867a3c9264806a4b44144502aeb8e5e`.
Semantic scope review remains manual; retrieval results are not application
acceptance.

The affected structural checks passed: `D0.All` built 4,575 jobs; 41/41
proof-architecture tests passed; `validate_repo.py` reports 889 claims,
31 assumptions, 58 aliases, 194 formal-support rows, 927 Lean-closure rows,
and zero warnings. `check_claim_map_coverage.py`, `validate_work.py`,
`validate_agent_protocol.py`, `gr_assembly.py check`,
`gr_assembly.py render --check`, `render_work_status.py --check`,
`generate_lean_views.py --check`, `check_no_sorry_in_core.py`, and the
CRLF-aware `git -c core.whitespace=cr-at-eol diff --check` also pass. The task
remains in progress: C0 is unfrozen, the 54 compiled semantic relations are
unresolved, and full C0 dispositions, independent acceptance, remaining
library migration, and physical GR/source selection remain open. This
intermediate checkpoint does not satisfy the WRK-401 completion conditions.

### Actual role-signed CAR square composed with the all-size Fourier symbol (25 October 2026)

`D0.Geometry.ArchiveLorentzianCARDiracApplication` now closes the exact
first-order-to-second-order operator bridge left open by the preceding Fourier
checkpoint. It defines the source's ordinary forward creation term plus the
explicitly role-weighted backward annihilation term on the same finite complex
site × Fock carrier. For arbitrary real weights `w`, the CAR anticommutators
give `D_w² = Σᵣ wᵣ(-∇⁻ᵣ∇⁺ᵣ) ⊗ I`; the proof retains the weights as input and
does not select a metric. Instantiating the owned `roleLorentzSign` and
composing with `archiveLorentzianDifferenceOperator_fourier_mode` proves that
every product-cycle character tensored with an arbitrary 16-component Fock
profile is an eigenvector of the squared operator with the Eq. (5) symbol for
every archive period `L=N+2`.

This closes the mathematical square-to-source application for the declared
operator and sign assignment. It does not prove that an admitted D0 execution
selects that operator or role-sign assignment, and it does not prove that the
first-order operator itself preserves an individual character profile. The
direct first-order Fourier action, physical action/source selection, matter
compatibility, and GR closure remain open. The result is not a physical
`GR_closed` claim.

The module is registered in `formal_support.csv` and generated into
`D0.All`. Its source SHA-256 is
`749be35f4074ec7408408fb62d68cc9b3724ecfd0920eee146f7866275229e33`. The
compiled declaration inventory is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_car_dirac_module_declarations_2026-10-25.json`
(11 declarations, SHA-256
`16be766dd280b46115472a3a3a11866c4ee684b71df16a63789e49233fc2dea0`, Lean
source digest `f0c6d4d35672206e02a2eea043cf9dd15770c0aa09b9793461b07890b537482e`,
collector SHA-256
`4dfa08c1502dc0ee81bc9eb590811a536e5367dbfb39c9e552e6ec48051e388d`). It
records the module under public import root `D0.All`, toolchain Lean 4.30.0,
and the new `archiveLorentzianCARDirac_square_fourier_mode` declaration.

The cold-start replay after integrating the claim-source resolver found every
required source in 19/19 cases and passed its 20th exact-source/unrelated-prose
impact control. The new exact-name query ranked the Lean module first, the
previous compact cold-start record second, and the compiled declaration
inventory third; all seven required sources in the native weighted-Dirac case
were found. The merged-input target record is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_car_dirac_cold_start_merged_2026-10-25.json`
(SHA-256
`9beadb7007f2caebb88f21a3a158d70b0687e21e198c52350dace4e59ddd29ab`). Its
input snapshot is `48bc48a149473702eae9d6b2bf9445057a685a2c` with a dirty
worktree; the cold-start runner SHA-256 is
`904ca43814330d6ce8bd669774f0f4284ee165c461ec105b483e4d880a58fd56` and the
integrated `proof_architecture.py` SHA-256 is
`a6114ed772f36251a54953f13531694cac1734020f5ce128cafae0ae4eb8053b`.
Semantic scope review remains manual; retrieval is not physical acceptance.

The final integrated `D0.All` build passed all 4,576 jobs. After combining
both PR lines, the focused proof-architecture suite passed 43/43 tests (test
SHA-256
`88ee84d5f43a0875843dfa161b53a5e43a35f21736f89e79865ff71e571770e5`).
Repository validation reports 889 claims, 31 assumptions, 58 aliases, 195
formal-support rows, 928 Lean-closure rows, and zero warnings. Claim-map
coverage, work validation, agent-protocol validation, gravity-assembly check,
generated-view check, core sorry guard, and the CRLF-aware diff check passed.
The PR remains Draft and WRK-401 remains in progress.

### Exact claim BOOK/section source-key candidate pass (25 October 2026)

The generated `claim-sources` view resolves the existing `claims.csv`
`book/section` fields against Markdown ATX headings in the ten `01_BOOKS`
files. It expands conservative `BOOK_01/02` shorthand, pairs equal-length
composite book/section lists, and permits one book to carry several explicit
sections. It classifies mismatched multi-book lists as malformed locator rows
with no source selected, ignores body text and fenced-code headings, and reports
duplicate exact headings as ambiguous.
No source locator, claim statement, release status, or owner is rewritten.

At source snapshot `84b32c7189bb3793032622dab1b990bb59307929`, the view
contains all 889 claim rows and all 731 parseable source pairs. There are 94
rows with only unique exact heading matches, four partially resolved rows,
zero ambiguous rows, 611 rows with no exact heading match, 170 malformed rows
whose composite BOOK and section counts do not pair, and ten non-BOOK source
rows. The pair-level counts are 116 unique and 615 unresolved. The row
categories are disjoint. All ten current book files match their Git blobs at
the snapshot; the current `claims.csv` SHA-256 also equals its snapshot blob.

The fully resolved `D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001` example now
has exact candidate source keys at Book 01 §01.8.1 (line 1111) and Book 02
§02.34 (line 2121). Four partial rows remain explicit: the intrinsic-quotient
claim has no exact Book 04 §04.11 heading; the automorphism/Hodge claim has no
heading for the literal §08.12.5-6 range; two cascade-floor claims have no
Book 01 headings for their literal §03.23.2 and §03.23.4 references. The
resolver does not split ranges or move a section to another book to force a
match.

The complete derived view is
`sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json`.
Its Windows working-tree representation uses CRLF (608,420 bytes; SHA-256
`b7372d8eab69b9f1b2f40a833f5057846d6bb651c928b53c9f902073a7750fb7`); the
published Git blob uses LF (594,056 bytes; SHA-256
`228a1a3c201ef61045746a2ae0788fa8caed1a92955cf17d16942c0ee1b292f1`). The
line-ending conversion preserves the JSON data. It records the `claims.csv`
digest `e2fcba29050a9017aa6d1e7501f192e6209d2f6c04d8e9b791930c4e54c6cbf5`
and resolver SHA-256
`a6114ed772f36251a54953f13531694cac1734020f5ce128cafae0ae4eb8053b`;
re-running the CLI produced byte-identical output in the working-tree
representation. Exact unique headings carry
candidate source keys of the form
`source:<snapshot>:<path>#L<line>: <heading>`. This is source-location
evidence only; no C0 semantic disposition, coverage figure, or acceptance is
inferred.

An independent read-only review at published head
`31ccbc40bdcb05baa377cda0d522931eae65c16b` reproduced the 889 claim rows, ten
Book inputs, 731 locator pairs, 116 unique coordinates, and the row counts
above. The reviewed view is Git blob
`90df5b814739516b21533be239ec311b38899404`, which is unchanged at the current
head. It accepted source-coordinate locator integrity only; it did not accept
claim semantics, C0 dispositions, or coverage.

The focused proof-architecture suite passes 43/43. Its new cases check paired
and one-to-many locators, duplicate headings, body/fenced-code false matches,
non-BOOK sources, malformed composite pairs, and UTF-8 CLI output on a legacy
Windows code page. C0 remains unfrozen and unaccepted; existing scientific
owners, physical premises, and the 54 unresolved assembly semantic relations
remain unchanged.

### Exact first-order CAR action on each archive Fourier fibre (25 October 2026)

`D0.Geometry.ArchiveLorentzianCARDiracApplication` now formalizes the
first-order Fourier action that the preceding squared-mode result left open.
On the actual `ArchiveCochainC N` site × Fock carrier, a mode is the product
character `piCycleChar k` tensored with an arbitrary `ArchiveFockState → ℂ`
profile. The profile retains all sixteen Fock components.

The forward and backward role multipliers are
`L * (cycleChar (k r) 1 - 1)` and
`L * (1 - cycleChar (k r) (-1))`, respectively, where `L = archiveFibers N`.
The induced `roleWeightedArchiveFourierFockAction` applies the actual CAR
creation and annihilation maps to the profile, with the supplied role weights
acting on the backward term. `roleWeightedArchiveCARDirac_fourier_mode`
proves, for every archive period, momentum, real role-weight function and
profile, that the full operator maps this Fourier subspace to itself and
acts by exactly that finite Fock-profile map.

The map's square is also exact:
`roleWeightedArchiveFourierFockAction_square` gives the real weighted Fourier
symbol times the identity on every profile. Its proof factors through the
already-proved full-carrier CAR square and the generic weighted Fourier
operator theorem, so it does not introduce a second independent symbol
calculation. `archiveLorentzianCARDirac_fourier_mode` and
`archiveLorentzianCARFourierFockAction_square` specialize to the repository's
`roleLorentzSign` and Eq. (5) symbol. The first-order operator generally
changes the internal Fock profile; this does not make an arbitrary profile a
first-order eigenvector.

The exact formalization claim is carrier-level operator algebra conditional
on the explicit role weights. It does not prove that a physical admitted D0
execution selects the sign assignment, CAR action, metric, source, matter
coupling or refinement. GR closure and the remaining full-source premises
remain open. The compiled axiom inventory for the square explicitly reports
the existing finite CAR anticommutator proofs' `native_decide` trust
dependencies (`car_create_anticommutator_int`, `car_annihilate_anticommutator_int`
and `car_mixed_anticommutator_int`), alongside `Classical.choice`,
`propext` and `Quot.sound`; the declarations are not represented as
axiom-free. The direct first-order mode-map theorems have only the usual
classical finite-carrier footprint in their extracted inventory.

The complete compiled declaration inventory is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_car_fourier_fiber_action_declarations_2026-10-25.json`
(31 declarations, 142,132 bytes, SHA-256
`4e5e2af64f2312c32851deec89006836e4fd6cea2d481b93b222730a13bcb1f4`).
Its Lean source digest is
`760d0201ef6f1d9cdbebbaa97816e299124a8570660366036deae456b2efcb73`,
collector SHA-256
`4dfa08c1502dc0ee81bc9eb590811a536e5367dbfb39c9e552e6ec48051e388d`,
public import root `D0.All`, and compiled snapshot
`9c9053ab31f3a669cf1174bb47ded5cf89377d8e` with the worktree dirty.
The source file SHA-256 is
`326bdc85b448f8042544a7ee90eaf102e606991246df917585a2591749f79153`.
The focused Lean build passed all 3,395 jobs, and the final `D0.All` build
passed all 4,576 jobs. The exact Lean `show --lean` query resolves
`roleWeightedArchiveCARDirac_fourier_mode` from `D0.All` with its full
signature, source location and axiom footprint.

The updated cold-start replay found all required sources in 19/19 cases and
passed the exact-source/unrelated-prose impact control (20 benchmark cases).
The new three-name query surfaces the primary memo first, the compiled Lean
module second, and its declaration inventory third; both direct source and
compiled inventory are present. The compact replay record is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_car_fourier_fiber_cold_start_2026-10-25.json`
and carries the runner checksum and the bounded exact-name query evidence.
The focused proof-architecture tests passed 43/43. `validate_repo.py` reports
889 claims, 31 assumptions, 58 aliases, 195 formal-support rows, 928
Lean-closure rows, zero warnings; formalization debt remains at the five-item
baseline. Work validation, agent-protocol validation, gravity-assembly check,
generated-view check and the CRLF-aware diff check passed. The goal remains
in progress: C0 and independent acceptance are still open, as are the 54
assembly semantic relations, native source/physical selection, matter
compatibility and GR closure.

### Shared finite CAR matrix action and typed Fourier-fibre operator (25 October 2026)

The 16-state CAR matrix action now has one owner at the carrier layer:
`D0.Geometry.carMatrixEnd` is generic over a commutative semiring, with a
compiled composition theorem identifying composition with finite matrix
multiplication. The previous real-only definition in
`ArchiveExteriorFrameLift` was removed; its real `carCreateEnd` and
`carAnnihilateEnd` APIs retain the same types. The complex Fourier application
now builds its creation/annihilation profile maps from this same API.

The role-weighted first-order Fourier-fibre map is additionally exposed as an
actual complex `LinearMap` on the sixteen-component Fock-profile space. Its
application equals the existing function-valued API, and its self-composition
is proved equal to multiplication by the exact Eq. (5) Fourier symbol. The
proof reuses the existing full-carrier CAR-square theorem and generic scalar
Fourier theorem; it does not add another independent CAR-square calculation.
The existing complex `fibreComposeC` theorem now delegates to the shared
finite-matrix composition result, so the established create/create,
annihilate/annihilate and mixed CAR composition lemmas consume the refactored
API.

The edited support row for `ArchiveCARRelations` records an existing source
and the already registered CAR claim locator. It does not revise that claim's
status, accept its semantic scope independently, or infer a physical
application. The operator result remains conditional on explicit role
weights; no physical sign, action/source, metric, matter coupling, or
refinement is selected. Full-source physical selection and GR closure remain
open.

Narrow builds passed for `ArchiveCARRelations`, `ArchiveExteriorFrameLift`,
`ArchiveTwistedHodgeDirac`, `ArchiveJuliaRaisingOperatorReadout`, and
`ArchiveLorentzianCARDiracApplication`. The focused compiled inventory
enumerates 247 declarations from `ArchiveCARRelations`,
`ArchiveTwistedHodgeDirac`, and `ArchiveLorentzianCARDiracApplication`, using
the latter as its import root. Its SHA-256 is
`66df83fd8691df082585f0debd0d5ba4b25b40432855ae071d1ea146397ab480`; the
Lean source digest is
`0a3b065f3343293c07246f078e41b6a0dce10e334f5dcd273ae46313ca2f2688`, and the
collector SHA-256 is
`608448595c1dd37cc1ac7ad9b77d7378d812388ce299b1a40ba27004bf10310d`. The
compiled `roleWeightedArchiveFourierFockActionLinear_square` footprint is
`Classical.choice`, `propext`, `Quot.sound`, and the three existing finite
CAR `native_decide` anticommutator dependencies; the generic matrix action and
function-to-operator adapter introduce no `native_decide` dependency.

The public `D0.All` replay is deferred to the task's Ready integration
checkpoint under the repository validation budget. The focused inventory and
the five changed-consumer narrow builds are complete. The inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/archive_car_matrix_linear_operator_refactor_declarations_2026-10-25.json`.

### Complete per-fibre kernel classification for the weighted Fourier operator (25 October 2026)

The new application module
`D0.Research.NativeWeightedDiracFourierNullModes` consumes the actual complex
first-order Fourier-fibre `LinearMap` on `ArchiveFockState → ℂ`, retaining all
sixteen Fock coefficients. For every period, momentum, real role-weight
function, and role `r` whose forward multiplier `a_r` is nonzero,
`roleWeightedArchiveFourierFockActionLinear_contraction` constructs
`K = a_r⁻¹ A_r` from the existing annihilation map and proves the operator
identity `D K + K D = I`. The proof uses the shared finite CAR matrix action
and the actual creation/annihilation anticommutators.

The role condition is now derived from the momentum. The new
`archiveFourierForwardMultiplier_ne_zero_iff` proves that the forward
multiplier is nonzero exactly when that role's `ZMod (N+2)` coordinate is
nonzero, using primitivity of the standard finite-cycle character. Thus every
nonzero product momentum supplies a contracting role. Composing this result
with the existing exact square-to-symbol theorem and the capsule's generic
nilpotent-kernel implications gives, for every supplied nonconstant
zero-symbol fibre, `ker D = range D` and complex kernel dimension exactly 8.
The zero-symbol equation and the explicit real role weights remain hypotheses;
this does not prove the full dispersion/root count or refinement persistence.

The same fibre module now closes all three kernel-dimension cases. At zero
momentum, both difference multipliers vanish, so the sixteen-component map is
zero and its complex kernel has dimension 16. For a nonzero symbol, the module
constructs the two-sided inverse `symbol⁻¹ • D` directly from the exact
square-to-symbol theorem; the kernel dimension is then 0. The new generic
`roleWeightedArchiveFourierFockActionLinear_kernel_finrank_cases` and its
`archiveLorentzian_kernel_finrank_cases` specialization state the exact split:
16 at zero momentum, 8 at a nonconstant null symbol, and 0 off the null shell.
The nonconstant null case additionally proves kernel equals range, with each
space of complex dimension 8.

This is a classification on each actual finite Fourier fibre. The number of
momenta on the null shell, total-kernel counts on a grid, and their refinement
behavior remain open; no all-size root count is inferred from the per-fibre
result.
The final specialization
`archiveLorentzian_nonzero_null_mode_classification` binds the result to the
repository's existing `roleLorentzSign` and `archiveLorentzianFourierSymbol`;
it proves kernel equals range and that both spaces have complex dimension 8.

This formalizes the actual Fourier-contraction and kernel/half-dimension
application in §5 (Eq. 7) of
`A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md`, pinned at commit
`db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, blob
`2de670c0e2f9a53104be8105a3554cdd9aaa85e7`. The branch-local capsule mirror
widens its two generic linear-map implications from real vector spaces to
division-ring modules so the existing theorem can be applied over `ℂ`; its
real specialization is unchanged. This separate mirror delta is at Git blob
`60de6702e232d6b68fc3b707a058383c4c09b2ff` (SHA-256
`fdf62644f086ba78c5d1ef203a4d3b7989488395c68afb0920bfa211f5c1d0f3`); the
new adapter source SHA-256 is
`7b88a6a550ca540336540ba4b030fdb16e142c30489c0eb42810d631849f4da2` and the
updated geometric application SHA-256 is
`3d7858a61101347807d9784579f1475739a1a75223dc2f5888d77362c9f699af`. The
pinned source memo and its original source blobs are not rewritten.

The new declarations are registered in `formal_support.csv` and imported by
the generated `D0.All`; no claim status, C0 acceptance, gravity obligation,
or physical source choice changes. The focused compiled inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_fourier_null_modes_declarations_2026-10-25.json`
(at the prior per-fibre checkpoint: 200 declarations across four owning
modules, including 22 in the adapter; historical SHA-256
`528512daf3d95794f1c43033f67bdbeef929aa2fc145da1aeb61913a07d5fbfd`; refreshed
after the fixed-mode persistence result below). It uses
import root `D0.Research.NativeWeightedDiracFourierNullModes`, Lean source
digest `c038d0b12cbf6064a7a370532bba2487104e55e243577b316f71a39f9ced606a`,
collector SHA-256
`cd8acaf6fa202e54f8090f9c5fb9fc210dfe03ba3197f21115581d7b7afad0cb`, and
source snapshot `2d0c2e2c7ffaa54d3b7d44fd6a674a7bf2619dbb` with a clean
worktree. The non-null inverse and null-kernel classification inherit the
existing square theorem's CAR proof leaves. The contraction theorem's axiom
footprint includes the existing
finite annihilation and mixed-CAR `native_decide` leaves plus
`Classical.choice`, `propext`, and `Quot.sound`; the null-kernel application
also inherits the creation-CAR leaf through the square theorem. No `sorryAx`
is present in these declarations.

The focused Lean builds passed for
`D0.Geometry.ArchiveLorentzianCARDiracApplication` (3,395 Lake jobs) and
`D0.Research.NativeWeightedDiracFourierNullModes` (3,410 jobs). The public
`D0.All` import was updated; generated-view validation passed (`stale=0`),
`validate_repo.py` passed (`claims=889`, `assumptions=31`, `aliases=58`,
`formal_support=197`, `lean_closure=929`, zero warnings), the formalization-debt
audit remained at its five-item baseline, and the CRLF-aware diff check passed.
The full public-import Lean replay remains deferred to the task's Ready
checkpoint. The physical CAR/source/action selection, matter compatibility,
all-size dispersion classification, and GR closure remain open. This is a
conditional mathematical application, not physical `GR_closed`.

### Fixed-frequency null-root persistence on every archive period (25 October 2026)

The adapter now defines `archiveLorentzianDiagonalMomentum N m` on the actual
`Role → ZMod (N+2)` Fourier carrier, with coordinates `(m,m,0,0)` in the
repository's `A/B/C/D` ordering. The Lean theorem
`archiveLorentzian_diagonal_momentum_is_null` proves the exact Eq. (5) symbol
is zero for every `N` and every natural `m`: the positive A and negative B
terms are identical and cancel, while C and D vanish. This directly formalizes
the source memo's diagonal null family rather than supplying a numerical
root-search result.

When `0 < m < N+2`,
`archiveLorentzian_diagonal_momentum_ne_zero` proves the momentum itself is
nonzero using the exact `ZMod` divisibility criterion. Composing it with the
already established actual-fibre contraction and Eq. (7) classification,
`archiveLorentzian_diagonal_null_fibre_classification` proves for the
repository's explicit `roleLorentzSign` that the first-order CAR operator has
`ker D = range D`, each of complex dimension eight. In particular,
`archiveLorentzian_unit_null_fibre_classification` establishes this for the
same unit frequency `m=1` at every period `N+2`, so one nonconstant null mode
persists under every refinement in the declared archive sequence.

This discharges the fixed-mode persistence statement in §5 of
`A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md`, pinned at commit
`db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, blob
`2de670c0e2f9a53104be8105a3554cdd9aaa85e7`. The general fibre dimension
theorem remains the consumer; no separate role or root is assumed in the
unit-frequency corollary. The existing module stays registered through
`formal_support.csv` and generated `D0.All`; no claim, physical source choice,
or gravity acceptance changes.

The narrow Lean build of
`D0.Research.NativeWeightedDiracFourierNullModes` passed (3,410 Lake jobs).
Other roots on the null shell, their all-grid count, total cochain kernel
dimensions, and any physical gauge quotient remain outside this result. The
theorem proves persistence of one explicit mathematical family on the given
carrier; it does not prove physical selection, a continuum limit, or GR
closure.

The refreshed declaration inventory compiles the selected adapter import and
records 208 declarations across the same four owning modules, including 30 in
the adapter (eight newly elaborated declarations, counting generated helper
declarations). Inventory SHA-256 is
`d6a8a177ea18307d1ee8417f0a884a379fa84325d03342190254a792f9c87a67`; the Lean
source digest is
`8f510881a8dbd744acff07050e813af51cace498b41c5e4c36381f1577b7548b`, and the
module SHA-256 is
`8f7bb090857a60e55adf6c2e50fbe2f651b59a4983454baef5eec59ef198b976`. The
inventory snapshot is commit `0421706162e663513ca39a03590c72ffccdc1eac` with
`worktree_dirty=false`; no new declaration has `sorryAx`. The exact symbol and
nonzero-frequency lemmas have only the standard `Classical.choice`,
`propext`, and `Quot.sound` footprint; the composed fibre classification also
retains the existing finite CAR `native_decide` leaves. The public `D0.All`
import list is current, while its full build remains reserved for Ready.

### Lift of the persistent null fibre to a full exact cochain (25 October 2026)

The adapter now composes the eight-dimensional unit-frequency fibre result
with the actual site × Fock Fourier intertwining theorem. Since the fibre map
has an eight-dimensional kernel inside the sixteen-dimensional profile
space, it is nonzero. `archiveLorentzian_unit_null_mode_exact_cochain_witness`
therefore proves, for every archive period, existence of a profile `v` whose
full complex cochain `D v` is nonzero and whose next image is exactly zero:
`D(D v)=0`. The profile is carried by the fixed unit-frequency mode
`(1,1,0,0)` in `Role → ZMod (N+2)`; this is an existential exact witness on
the full operator, not only a fibre-level kernel statement.

This consumes the preceding fibre classification plus
`archiveLorentzianCARDirac_fourier_mode` and
`archiveLorentzianCARDirac_square_fourier_mode` on the actual complex
site × Fock carrier. It strengthens the scoped §5 null-cochain application
from tested even grids to every declared period. It does not give an explicit
closed-form profile, a real-valued representative on each grid, a gauge
quotient, or the total cochain kernel dimension. It supplies no physical
selection or continuum conclusion.

The narrow build of
`D0.Research.NativeWeightedDiracFourierNullModes` passed again (3,410 Lake
jobs). Repository validation passed (`claims=889`, `assumptions=31`,
`aliases=58`, `formal_support=197`, `lean_closure=929`, zero warnings),
generated Lean views passed (`stale=0`), and formalization-debt non-growth
passed (five findings, unchanged baseline); the EOL-aware diff check passed.
No claim or `formal_support` entry changed.

The refreshed compiled declaration inventory now records 209 declarations
across the same four owning modules, including 31 in the adapter. Inventory
SHA-256 is
`f2438c5ed799c9ce2267e3d465784981c8d8fb0adabdbcd26bfd1f57e01f2c77`; Lean
source digest is
`112436f04eb5f9eaa6648c2cea4b2fd2941ed5e873a87f1669d3e0ec8e258303`, module
SHA-256 is
`9081b243bef28b5e82a2e3ab28518198d66a1e43951e369f8dcae6956f2ddefd`, and the
collector SHA-256 remains
`cd8acaf6fa202e54f8090f9c5fb9fc210dfe03ba3197f21115581d7b7afad0cb`. Its
snapshot is commit `59f1802f9df226cc5d6a22dc611d8fd3bf65a232` with
`worktree_dirty=false`. The new exact cochain theorem has no `sorryAx`; its
transitive footprint retains the existing CAR `native_decide` leaves along
with `Classical.choice`, `propext`, and `Quot.sound`. The full `D0.All` build
remains reserved for Ready.

### Structural lower bound on the all-grid null-root count (25 October 2026)

The same exact family now yields a finite cardinality result. For the period
`L=N+2`, the adapter proves the map
`i ↦ (i+1,i+1,0,0)`, `i : Fin (L-1)`, is injective in the actual
`Role → ZMod L` carrier by recovering the natural representative through
`ZMod.val`. Each image is a nonzero root of the exact Eq. (5) symbol. The
compiled theorem `archiveLorentzian_nonzero_null_momentum_count_lower_bound`
therefore proves that the full nonzero null shell contains at least
`L-1 = N+1` momenta for every archive period.

This is the exact cardinality of the explicit diagonal subfamily and a lower
bound for the whole shell. It does not classify roots with other role
coordinates, give the exact all-grid root count, or compute the total site ×
Fock kernel dimension. The exact full-cochain witness above and this root
lower bound are mathematical properties of the declared complex carrier;
they do not define a physical gauge quotient or select the source.

Validation on the source checkpoint passed: the adapter narrow build completed
(3,410 Lake jobs), repository validation reported zero warnings, generated
Lean views had `stale=0`, the debt audit stayed at its five-item baseline, and
the EOL-aware diff check passed. The refreshed selected-import inventory has
216 declarations across the same four owning modules, including 38 in the
adapter and no `sorryAx`. Its SHA-256 is
`6c7bd30bf64f1db5cad67bf56bf333d7f25a1381cafbe1808bd126c5747a5d77`; Lean
source digest is
`c7859453678c46f50435b7e0b2eb0cf726317e8f3057e12962ace05918bd3e81`, module
SHA-256 is
`8635403019347dba0160d57de34d500791ad1e8e99817349d53d02e81b096b5d`, and
collector SHA-256 is
`cd8acaf6fa202e54f8090f9c5fb9fc210dfe03ba3197f21115581d7b7afad0cb`. It
records snapshot `8d35e0c308e648281492cb1f9b4ed7a8cea70302` with
`worktree_dirty=false`. The lower-bound theorem's transitive footprint is
`Classical.choice`, `propext`, and `Quot.sound`; the full cochain witness also
retains the existing CAR computation leaves. No claim or `formal_support`
entry changed, and the full `D0.All` build remains a Ready-checkpoint action.

### Typed full-cochain CAR operator and additive null-kernel bound (25 October 2026)

The full site × Fock CAR operator has a typed `LinearMap` API for arbitrary
supplied role weights, with a specialized typed Lorentzian operator for the
repository's declared role signs. The established function-level definitions
remain available through exact compatibility theorems. The Fourier-mode
embedding also has a typed linear-map form, and its intertwining identity
transports each classified null-fibre kernel into the kernel of the actual
full cochain operator.

The new theorem
`archiveLorentzian_full_cochain_kernel_finrank_ge_diagonal_family` proves
`16 + 8 * (archiveFibers N - 1) ≤ finrank ℂ (ker D_full)`. Its family contains
the sixteen-dimensional zero-frequency fibre and each of the `N+1`
constructed, distinct diagonal null frequencies, whose fibre kernels have
dimension eight. Exact character orthogonality on the finite product-cycle
carrier proves that the sum of these mode embeddings is injective, so their
dimensions add on the full site × Fock carrier. This strengthens the earlier
one-fibre lower bound without requiring an exact total kernel computation.

This remains a lower bound from an explicit family. The exact total null-root
count and full kernel dimension, the physical gauge quotient, and
source/action selection remain open. The role-sign assignment remains a
mathematical input, not physical selection; no claim status or
`formal_support` entry changed. The owning-module declaration inventory is
stored at
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_fourier_null_modes_declarations_2026-10-25.json`.
It enumerates 240 declarations across the four selected owning modules
(76/60/49/55); no declaration has `sorryAx`. The inventory SHA-256 is
`08624b561817f68f2b39b2c3a721971a99c9a44715853d80ac57e54249ce6653`, its
Lean-source digest is
`584f100caaff6b217aa7cef2d8b1779406c9fd0f7b8ff23b0dc6d9c206c556b7`, and
the collector SHA-256 is
`cd8acaf6fa202e54f8090f9c5fb9fc210dfe03ba3197f21115581d7b7afad0cb`. It
records snapshot `95cbbcfffd8441d529b0d4549b92d74bcd81b7db` with
`worktree_dirty=false`. The geometry adapter source SHA-256 is
`cb9aaa751c755402d28ac7c6aaf4fbc63e31b9cd6e4e1d566f6096aced391509`; the
Fourier adapter source SHA-256 is
`8dd722212e61f8ba1137ea5ab92c5f9963001fa1cda317269d4b66f25cfa0a13`. The
aggregate theorem's transitive footprint consists of the existing CAR
anticommutator `native_decide` leaves, `Classical.choice`, `propext`, and
`Quot.sound`; no new axiom or `sorryAx` is introduced. A full `D0.All` replay
remains reserved for the Ready checkpoint.

The source checkpoint is published commit
`95cbbcfffd8441d529b0d4549b92d74bcd81b7db`. The narrow build of
`D0.Research.NativeWeightedDiracFourierNullModes` passed with 3,410 Lake jobs
under Lean 4.30.0. On the final tree, repository validation passed with
`claims=889`, `assumptions=31`, `aliases=58`, `formal_support=197`,
`lean_closure=929`, and zero warnings; generated Lean views reported
`stale=0`; the formalization-debt audit remained at five findings, its
unchanged baseline; gravity assembly reported `valid=true` and
`scientific_promotion=false`; and the EOL-aware diff check passed.

### Clean compiled claim-candidate availability snapshot (25 October 2026)

The all-claims resolver compiled the public `D0.All` import under Lean 4.30.0
and extracted exact candidate-name availability for all 889 registry claims.
At snapshot `14932cfd156877888716790824d637c0d0acbcd7`, the worktree was clean;
the Lean-source digest is
`66ef38e495f22833eab58841ce5365575e96e2ecef382473d47b4986b2a07a8b`, the
claim-registry digest is
`e2fcba29050a9017aa6d1e7501f192e6209d2f6c04d8e9b791930c4e54c6cbf5`, and the
collector digest is
`dd33d4ab45852eb1d2aef0311f00db6249832d41f9957a50e29b5e3e51f953a8`.

The registry expands to 2,751 candidate mappings: 2,575 theorem-name atoms
and 176 rows without a theorem atom. Those mappings contain 8,458 candidate
references to 8,323 distinct Lean names. The compiled environment contains
2,512 of those names and does not contain 5,811. At least one candidate name
resolves for 2,382 mappings and for 680 claim IDs; all listed theorem atoms
resolve for 635 claim IDs. Found names span 646 owner modules. These are exact
locator-availability results only. A matching declaration name does not
establish that its elaborated theorem has the claim's meaning, and a missing
candidate name does not establish that no equivalent theorem exists.

The complete resolution-only artifact is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/claim_candidate_resolution_2026-10-25.json`.
Its Windows working-tree representation is 2,546,688 bytes (SHA-256
`8c7961f6e4497eed7b8add7a4375593ba9eb83c19da0f7d16ce1ba098af5d480`); its
LF-normalized representation is also 2,546,688 bytes with the same SHA-256.
The artifact records public import root `D0.All` and `resolution_only=true`.
It does not freeze C0, assign semantic coverage, change claim/owner status,
or discharge the open scientific and physical premises. C0 remains open and
independently unaccepted; #334 and the existing physical owners remain
preserved.

### Exact compiled lookup and dependency record for the full-cochain bound (25 October 2026)

The bounded `show --lean` query resolved
`D0.Research.NativeWeightedDiracFourierNullModes.archiveLorentzian_full_cochain_kernel_finrank_ge_diagonal_family`
in the compiled public import `D0.All`. The elaborated type is
`∀ (N : ℕ), 16 + 8 * (D0.archiveFibers N - 1) ≤ Module.finrank ℂ ↥(D0.Geometry.archiveLorentzianCARDiracLinear N).ker`.
The declaration lives in
`03_FORMALIZATION/D0/Research/NativeWeightedDiracFourierNullModes.lean`
(declaration lines 568–708; selected name at line 572). The exact-name query
returns a compiled declaration, while the source map still classifies the
broader Eq. (7) unit as partial: this theorem supplies a full-cochain kernel
lower bound, not an exact total kernel dimension.

The unabridged single-declaration inventory is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_full_cochain_kernel_declaration_2026-10-25.json`
(12,883 bytes; SHA-256
`e9f2e85c138cfb022745ca4ca61bdddd9c2d95a0f82870aa716f2ba138552277`). It
records snapshot `49f7f3f506286860c82c5960bf4735fb123095f2` with a clean
worktree, Lean source digest
`66ef38e495f22833eab58841ce5365575e96e2ecef382473d47b4986b2a07a8b`,
collector SHA-256
`05223c192382c3e084fd44d452c3dd11559bc5f0460b455604493635f2247c57`,
toolchain `leanprover/lean4:v4.30.0`, and public import `D0.All`. It contains
265 proof dependencies and 42 type dependencies. The axiom closure lists
`Classical.choice`, `Quot.sound`, `propext`, and the three existing CAR
anticommutator `native_decide` leaves; `sorryAx` is absent.

The elaborated proof dependencies expose the actual composition: the diagonal
null-fibre classification and distinct-momentum injectivity feed the finite
Fourier-mode sum; the zero-fibre theorem supplies its 16-dimensional summand,
and `LinearMap.finrank_le_finrank_of_injective` transfers the resulting family
to the full cochain kernel. The exact inventory also retains the private
`archiveFourierFockMode_sum_fourier_projection` helper in this dependency
chain.

The exact-name lookup has no claim ID and creates no semantic claim edge. The
theorem remains conditional on the declared finite-carrier operator and role
signs; the exact null-root count, gauge quotient, physical source selection,
and GR closure remain open under their existing owners.

### Cold-start route for actual foundation/transfer controls (25 October 2026)

The `verification-kernel-transfer-outside-gr` retrieval case now points to the
existing end-to-end owner in
`D0.Foundation.VerificationTransferApplication`. Its
`visible_only_memory_cannot_decode_hiddenBit_futures` theorem shows that any
decoder satisfying the complete future-profile equation would force the
visible-only encoder to be injective, contradicting two states with the same
visible bit and different future archives. The supporting
`hiddenBit_sufficient_encoder_injective` lemma now derives this implication
through the generic `FutureExecution.sufficient_memory_reflects_future` result
and quotient exactness, instead of duplicating its profile-equality argument.
The companion `erased_hiddenBit_operation_map_is_impossible` theorem uses the actual
`Interpretation` structure and rules out the identity state map paired with an
empty action word: the archive-revealing operation contradicts
`step_commutes`. The positive
`verified_visibleFalseReadout_transfers_to_common_execution` theorem composes
the real `TheoryVerification.representedState` map with
`Interpretation.transfer_theorem` and the native common-sector readout.

The same retrieval card pins
`D0.Bridge.connes_reconstruction_conditional`. `ConnesReconstruction` carries
the finite-spectral-triple and external metric-reconstruction statements as
fields; the theorem only returns their supplied witnesses. The bridge therefore
remains conditional and does not select a physical execution or close GR.

The refactored application owner passed its narrow build (2,971 Lake jobs
under Lean 4.30.0). The decoder control and supporting injection now inherit
`propext` and `Quot.sound` through the generic future quotient; the operation
map control reports only `propext`. The positive foundation/transfer
composition reports `propext`, `Classical.choice`, and `Quot.sound`; the Connes
projection theorem reports no axioms. The focused proof-architecture suite
passes 44/44, and the final cold-start run found every required source in all
19 cases (20 benchmark cases including the impact regression). These checks
reuse existing Lean results; no duplicate theorem or physical selector was
added.

### Generic finite-memory lower bound from future-profile separation (25 October 2026)

`D0.Foundation.FutureExecution` now owns the reusable consequence needed by
the hidden-bit control. Given an injective complete future profile and a
decoder satisfying `decode (encode s) = F.profile s` for every state, the
generic theorem
`FutureExecution.sufficient_encoder_injective_of_profile_injective`
proves `Function.Injective encode`. With finite native-state and memory types,
`FutureExecution.sufficient_memory_cardinality_lower_bound` derives
`Fintype.card F.State ≤ Fintype.card C`. Both conclusions consume the existing
`sufficient_memory_reflects_future` theorem; the cardinality result then uses
Mathlib's finite-cardinality bound for an injective map.

The existing `hiddenBit_sufficient_encoder_injective` and
`hiddenBit_minimum_future_memory_four` results are now applications of these
generic theorems, supplying the already-proved injectivity of the concrete
hidden-bit future profile. The explicit local `Fintype` instance exposes the
definitional `Bool × Bool` state carrier; it adds no cardinality assumption to
the theorem statement. The exact compiled declarations were queried from the
`D0.Foundation.FutureExecution` import. Their elaborated types retain profile
injectivity, total decoder correctness, and finite-type assumptions. The
reported proof dependencies show the chain through
`sufficient_memory_reflects_future`, `Quotient.exact`, and
`Fintype.card_le_of_injective`. The axiom closure is
`Classical.choice`, `Quot.sound`, and `propext`; `sorryAx` is absent.

The six-declaration compiled inventory is saved at
`sources/d0_proof_architecture_formalization_2026-10-24/future_profile_memory_cardinality_declarations_2026-10-25.json`.
It records pre-edit snapshot `b649e766d0adf049ddb3d263e30d83fd3fcc347f`
with `worktree_dirty=true`, source SHA-256
`22a3071bef687e2009ccb7ebfed6d6fad469c8f35be57cc2b0a7fa39a8d36da6`, Lean
source digest `ae5f197c7d5043800c867a916c8fd6b1bb5e885e64e1b7b40047ddd1818158db`,
collector SHA-256
`fc9aae28d37ec54fca3267ca2957f09893d2ea23f9ad9ddb4ff8b1ebe0667e14`, and
inventory SHA-256
`62f9e5c2ce527fa3a9929ca866e594b1895ae2625e6ba423e9bfdf41478c5ddd`.

On the tree based at `b649e766d0adf049ddb3d263e30d83fd3fcc347f`, narrow
Lean 4.30.0 builds passed for `D0.Foundation.FutureExecution` (2,960 Lake
jobs) and its concrete consumer
`D0.Foundation.VerificationTransferApplication` (2,971 jobs). No claim,
`formal_support` row, assembly edge, or physical-selection premise changed.
This strengthens the reusable mathematical kernel and its existing finite
control; it does not freeze C0 or report coverage.

The existing cold-start case `verification-kernel-transfer-outside-gr` now
includes a query for the generic injectivity/cardinality results and a
filename query for their compiled inventory. The exact theorem query returns
the primary artifact and `FutureExecution.lean` as direct-content candidates;
the filename query returns the six-declaration inventory at rank 2. Its
focused case test passes. The full cold-start replay then completed on clean
snapshot `56125b5cec3f6687d9fcd7fb2bb49364228acb2b`: all 19/19 cases found
every required source, including this inventory, and all 20 benchmark cases
ran. The `exact-source-vs-unrelated-prose` impact control passed, confirming
that a declared source edit changes its dependent result while unrelated
prose leaves that source digest unchanged.

### Candidate C0 source-unit reconciliation: CAR hopping zero mode (25 October 2026)

This is one unresolved source-unit crosswalk, not a C0 freeze, acceptance, or
coverage result. The inspected snapshot is PR head
`c3c56c15ad2e84a0dba796a6fb42e03bf9438118`. Current source pins are:

| Candidate source | Git blob | SHA-256 | Scope |
|---|---|---|---|
| `02_REGISTRY/claims.csv` | `609336b5d57600383ce141cc62cb1e7ec15b9e21` | `e2fcba29050a9017aa6d1e7501f192e6209d2f6c04d8e9b791930c4e54c6cbf5` | Claim `D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001`, row 816 |
| `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md` | `99721fb50de66688564638f5f2b449a38675d7bd` | `592bbbb1dae9cc599df2eef9cabf117b19f8566d755ad072b77beb04624271d7` | Claimed source locator does not resolve to a heading |
| `03_FORMALIZATION/D0/Geometry/ArchiveCARDirac.lean` | `032cb37242abebee30f6a8715b90a61235bec348` | `d12ee600d7976228ffcb88e5c40c08d66cd361664901594ea0379bf2b97a2388` | Actual hopping operator and arithmetic scaffold |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean` | `5b6ee2265a9abec3eacfb8905cd45d4ef3c95b73` | `7ab9550c7a25464131ec23a21e9eeac9f38eb651ee23c8d65296415aa593ab58` | Separately typed finite-difference operator |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracKernel.lean` | `5d5193361fc5f4a564018a03f66b02e5ef1effd3` | `e0d69896a6e667a9a87380c281dc9adff196c0d4608a68b9515acfac999e1832` | Hodge-operator kernel theorem |
| `02_REGISTRY/formal_support.csv` | `26500cdabd22dc6286b1741640420ca43690b886` | `e926db5c0b36d3e17c45b8e35b8b534530331f5b3339310e4943b3d6f6b0ea6e` | Explicit support exists for the Hodge kernel only |

The claim and generated `ClaimMap` both leave the zero-mode obligation `OPEN`.
`ArchiveCARDirac.lean` defines `carDirac` / `hoppingCarDirac` as a finite
nearest-neighbour Clifford hopping matrix on `CARHilbertPoint n`; its module
header explicitly distinguishes it from the Hodge/difference operator.
`carDiracKernelDim := 16`, `car_zero_mode_independent_of_L`, and
`archive_car_zero_mode_owner` establish only an integer constant and a size
inequality. Their statements do not refer to `ker (carDirac n)` or its
`Module.finrank`.

A follow-up finite proof now closes the literal hopping matrix at `L=2` only:
`carDirac_square_eq_four_id_at_zero` proves `D² = 4 I`, and
`carDirac_zero_kernel_trivial_at_zero` proves every vector in its kernel is
zero. This is a counterexample to reading the scaffold's value 16 as the
kernel dimension of the registered hopping matrix at every period. It does
not determine the kernel at larger periods, establish a uniform finrank
formula, or resolve the absent Book 06 source unit; the registry row remains
OPEN pending source reconciliation and owner review.

The similarly numbered theorem
`hodgeCarDirac_kernel_finrank (N) :
Module.finrank ℝ (LinearMap.ker (hodgeCarDiracₗ N)) = 16` is for the distinct
forward/backward finite-difference operator on the cubical cochain carrier.
There is no operator equality or kernel-transport theorem connecting it to
`carDirac`. `formal_support.csv` records this Hodge kernel at row 99 and has no
`ArchiveCARDirac` or CAR zero-mode support row. Both modules being imported
into `D0.All` does not identify their operators.

The narrow compiled inventories were generated at PR commit
`560739696d60e14417d6054185933dc2ea249385`, Lean 4.30.0, with unchanged
Lean-source digest
`ae5f197c7d5043800c867a916c8fd6b1bb5e885e64e1b7b40047ddd1818158db`. The CAR
query used public import `D0.Geometry.ArchiveCARDirac` from a clean snapshot;
`car_zero_mode_independent_of_L` elaborates to
`∀ n, D0.Geometry.carDiracKernelDim = 16` with no axioms, and
`archive_car_zero_mode_owner` elaborates to that constant equality plus a size
inequality, with `Classical.choice`, `Quot.sound`, and `propext` in its axiom
closure. The Hodge query used public import
`D0.Geometry.ArchiveHodgeCARDiracKernel` and confirms the kernel-finrank type
above; its recorded axiom closure includes the two existing `native_decide`
CAR-identity proofs, `Classical.choice`, `Quot.sound`, and `propext`. The Hodge
inventory's `worktree_dirty=true` records that the earlier CAR inventory JSON
was already present; its Lean-source digest and exact declaration are pinned.
The machine records are
[`car_zero_mode_claim_declarations_2026-10-25.json`](sources/d0_proof_architecture_formalization_2026-10-24/car_zero_mode_claim_declarations_2026-10-25.json),
SHA-256 `12752bfed1ce3613efbca34b6456a3a05940306e21785c92368088174179d860`,
and
[`hodge_car_dirac_kernel_declaration_2026-10-25.json`](sources/d0_proof_architecture_formalization_2026-10-24/hodge_car_dirac_kernel_declaration_2026-10-25.json),
SHA-256 `cd4d6a4bf092088bf0d6a554c2d38f7ab6516fa7bcaaddbee4a87ffada2a0dbb`.
Each inventory builds and imports only its named owner module; neither invokes
the full `D0.All` Ready replay.

Cold-start case `car-scaffolds-vs-hodge-operator-claims` retrieves the four
open CAR claims, the CAR and Hodge operator modules, `ClaimMap`, the source
crosswalk, and the narrow compiled inventories in the bounded search window.
Its focused test separately reads `formal_support.csv` as structured data and
confirms that support is recorded for the Hodge square, kernel, and shell
modules, but not `ArchiveCARDirac`; it also checks the four OPEN CAR statuses
and the independently LEAN_PROVED shell status. This is a retrieval negative
control, not an automatic semantic acceptance; the focused case passes.

The claimed Book locator `BOOK_06 / 06.spectral kernel dimension of the actual
CAR Dirac operator` has no exact heading match in the source-candidate view;
the current Book 06 contains no CAR/Dirac/zero-mode passage. A read-only
independent scope review reached the same result and verified the claim's
Lean-name mapping. No claim row, `formal_support` row, or operator definition
was changed to manufacture a source correspondence.

**Disposition:** retain this registry entry as unresolved pending an actual
kernel theorem or a scoped counterexample for `carDirac` / `hoppingCarDirac`.
The Hodge theorem remains a separate mathematical result and cannot discharge
this claim. The Book locator, exact C0 membership, semantic acceptance, and
all broader formalization/refactoring obligations remain open. This slice
removes no scientific premise and reports no C0 coverage.

### Candidate C0 source-unit reconciliation: CAR square and Hodge operator (25 October 2026)

This is a source/operator crosswalk, not acceptance of the square claim or a
C0 freeze. The inspected source snapshot is PR head
`02a5a6e2c734614cfaa0bdfe16bd90cf53714053`; the exact source identities are:

| Candidate source | Git blob | SHA-256 | Scope |
|---|---|---|---|
| `02_REGISTRY/claims.csv` | `609336b5d57600383ce141cc62cb1e7ec15b9e21` | `e2fcba29050a9017aa6d1e7501f192e6209d2f6c04d8e9b791930c4e54c6cbf5` | Row 815 keeps `D0-ARCHIVE-CAR-DIRAC-SQUARE-001` OPEN; row 816 keeps the zero-mode claim OPEN; row 868 keeps the spatial Hodge shell claim LEAN_PROVED |
| `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md` | `99721fb50de66688564638f5f2b449a38675d7bd` | `592bbbb1dae9cc599df2eef9cabf117b19f8566d755ad072b77beb04624271d7` | `BOOK_06 / 06.spectral` has no exact heading match for the asserted CAR square |
| `03_FORMALIZATION/D0/TheoremLedger/ClaimMap.lean` | `b86e4246ad91a85e3fbc154def85b8b9f14e5c09` | `53337b3ce2d6490bc60e789f2e118ef397de775ef170fbe39fe2f24631e90c4b` | Row 1948 maps the square claim to the CAR arithmetic scaffold; row 2107 independently maps the proved spatial-shell claim |
| `03_FORMALIZATION/D0/Geometry/ArchiveCARDirac.lean` | `032cb37242abebee30f6a8715b90a61235bec348` | `d12ee600d7976228ffcb88e5c40c08d66cd361664901594ea0379bf2b97a2388` | Lines 29–35 distinguish the self-adjoint hopping matrix from the Hodge operator; lines 467–495 define the square and kernel arithmetic scaffolds |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean` | `5b6ee2265a9abec3eacfb8905cd45d4ef3c95b73` | `7ab9550c7a25464131ec23a21e9eeac9f38eb651ee23c8d65296415aa593ab58` | Defines `hodgeCarDirac` on cubical cochains and explicitly distinguishes it from `carDirac` |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracSquare.lean` | `f387d8badc868eed5ff3eba872fafd560b3b3b20` | `d504f2c5bd4959e779cca38ea1d484bce9aafbf31d5aea0fa7c116c920f1df7d` | Proves the Hodge square and oriented difference formula; records the L=2 graph-diagonal factor |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracKernel.lean` | `5d5193361fc5f4a564018a03f66b02e5ef1effd3` | `e0d69896a6e667a9a87380c281dc9adff196c0d4608a68b9515acfac999e1832` | Proves the 16-dimensional kernel for the Hodge operator |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracShell.lean` | `631db44c0b5fd3c33d2376768c3fb400352764f4` | `870d9d4b1f849a2fda7465bc157ba561432d67bd1a22098af75da9d780930caa` | Proves the Hodge shell, its large-L rank, energy limit, and the L=2 rank control |
| `03_FORMALIZATION/D0/Geometry/ArchiveHodgeSpatialShellOperator.lean` | `9ff627b325126bfefc19e3903eb73faa0224599f` | `4c7004ee4422c8d020bc58230b50abe9213db408f4440e7876e5ab873503b5fa` | Packages the spatial-shell operator claim and role-preserving symmetry results |
| `02_REGISTRY/formal_support.csv` | `26500cdabd22dc6286b1741640420ca43690b886` | `e926db5c0b36d3e17c45b8e35b8b534530331f5b3339310e4943b3d6f6b0ea6e` | Rows 90, 99, and 101 support Hodge square, kernel, and shell modules; no `ArchiveCARDirac` support row exists |

The mapped `ArchiveCARDirac` declarations do not state a square of the
operator. `carDiracSquareScalarSectorFactor_eq_fock_dim` elaborates only to
`carDiracSquareScalarSectorFactor = Fintype.card ArchiveFockState`, and
`archive_car_dirac_square_owner` elaborates only to the two equalities that
those quantities are 16. Both have axiom closure
`Classical.choice`, `Quot.sound`, and `propext`; neither mentions
`carDirac`, `hoppingCarDirac`, or an operator composition. The claim row itself
describes the massless owner as `hodgeCarDirac`, so these mapped declarations
cannot serve as its operator proof either.

The independent Hodge results do establish substantial parts of the written
target on their own typed cochain carrier:

* `hodgeCarDirac_sq` proves `hodgeCarDirac N (hodgeCarDirac N ψ) =
  cochainDifferenceLaplacian N ψ` for every `N` and cochain `ψ`.
  `cochainDifferenceLaplacian_eq_backward_forward` expands this as the sum of
  negative backward-after-forward differences over the four roles. Its
  recorded axiom closure includes `Classical.choice`, `Quot.sound`,
  `propext`, and the two existing `native_decide` CAR anticommutator proof
  constants.
* `hodge_difference_diagonal_double_metric_at_l2` proves that the L=2
  oriented point-mass diagonal is twice the undirected graph-metric diagonal.
  This is a factor-two normalization mismatch for an exact graph-operator
  identification under the current conventions; it must be reconciled in the
  target statement, not silently normalized away.
* The separately inventoried kernel theorem gives Hodge kernel finrank 16.
  For `3 ≤ archiveFibers N`, the spatial shell has finrank 96 and the squared
  Hodge operator acts there by `shellEnergy²`; its energy tends to `2*pi`.
  At L=2, the sine modes collapse and the cosine shell has rank 48.
  The shell restriction requires the A-axis-preserving subspace; role
  transports that move A are explicitly not covered by that invariance.

These are Hodge/cochain theorems, while `carDirac` / `hoppingCarDirac` is a
matrix operator on `CARHilbertPoint n = ArchiveRolePhasePoint n ×
ArchiveFockState`. The carrier sets have a pointwise correspondence, but no
proved linear operator intertwiner transports the Hodge square, kernel, or
shell statements to the hopping matrix. The theorem
`hoppingRoleTransport_commutes_hoppingCarDirac` proves a symmetry commutation
only; it is not a square or kernel theorem. Thus the exact graph normalization
and typed map needed by the registered square target remain unresolved, and
the actual hopping-operator square/kernel are also unproved if that operator
is intended. `D0-SPATIAL-HODGE-SHELL-OPERATOR-001` remains a separate proved
claim and does not close `D0-ARCHIVE-CAR-DIRAC-SQUARE-001` by registry status
alone.

Seven narrow compiled inventories are pinned beside the prior CAR and Hodge
kernel inventories. All use Lean 4.30.0 and the unchanged Lean-source digest
`ae5f197c7d5043800c867a916c8fd6b1bb5e885e64e1b7b40047ddd1818158db`; the CAR
scaffold inventory was generated from clean snapshot `02a5a6e2...`, and the
six subsequent inventories record `worktree_dirty=true` because earlier
inventory JSON files were present. Their exact SHA-256 values are:

| Inventory | SHA-256 |
|---|---|
| `car_dirac_square_claim_declarations_2026-10-25.json` | `feec6ad683826f291bf96dc16776b321fb7261a55c0ad6edd009a0b5d8427524` |
| `hodge_car_dirac_square_declaration_2026-10-25.json` | `3b1fae9af8586afe3ce8bbfe984a45cf2cf64e3383535b838f65f75b0b2612de` |
| `hodge_square_backward_forward_declaration_2026-10-25.json` | `12886618d9a5fe4b7fab837cf1d7be60a096f2440d49156eb3f9ba839f6754e2` |
| `hodge_car_dirac_l2_normalization_declaration_2026-10-25.json` | `d40be0ddfeb0f82f01e0280f654b9222ae34c88bf5213ae171b427f2d289e644` |
| `hodge_spatial_shell_claim_declarations_2026-10-25.json` | `1c0c418960a0e263d05dc020e329b9ff14ea90826e36850432441ea43c55a096` |
| `hodge_shell_energy_limit_declaration_2026-10-25.json` | `c8ae36d12687b13ec628383349d15f8182d1e03a4460acfbab1d2b66708be2fb` |
| `hodge_shell_rank_l2_control_declaration_2026-10-25.json` | `e09f6f27c111c8bd65f51661e422a4cbebde8b6785c52468059f2a781adc3265` |

The cold-start retrieval case now covers both open CAR claims, the distinct
Hodge operator results and all seven inventories. Its test reads
`formal_support.csv` as structured data, checks that both CAR claims remain
OPEN while the spatial-shell claim remains LEAN_PROVED, and verifies the
operator-scope statements. This is a source-retrieval control, not semantic
claim acceptance. The narrow inventories query only their named public import
roots; this slice does not run the full `D0.All` Ready replay.

**Disposition:** keep `D0-ARCHIVE-CAR-DIRAC-SQUARE-001` OPEN. The Hodge square,
kernel and shell results are genuine proved mathematics at their declared
scope. The original source-unit/normalization reconciliation and any typed
transport to the intended registered operator remain to be supplied before
the square target can be accepted. No claim row, `formal_support` row,
operator definition, or physical interpretation is changed here; this closes
no C0 or GR obligation.

### Candidate C0 source-unit reconciliation: CAR spectrum amplification and heat trace (25 October 2026)

This adjacent crosswalk uses the same exact source pins as the preceding CAR
square section; only the claim rows and compiled declaration records below are
new. In the source snapshot `6b41ccc5566d3b7a7e69c5591e3cb5c6fdfbc678`,
`D0-ARCHIVE-CAR-SPECTRUM-AMPLIFICATION-001` is OPEN at claims row 818 and
`D0-ARCHIVE-DIRAC-HEATTRACE-MULTIPLICITY-001` is OPEN at row 819. The generated
`ClaimMap` resolves them to `car_amplification_times_spinor_eq_sixteen` /
`archive_car_spectrum_amplification_owner` and
`diracHeatTraceMultiplicity_eq_fock_dim` /
`archive_dirac_heattrace_multiplicity_owner` in `ArchiveCARDirac.lean`.
`formal_support.csv` has no `ArchiveCARDirac` row.

The narrow compiled queries use public import
`D0.Geometry.ArchiveCARDirac`, Lean 4.30.0, and the unchanged source digest
`ae5f197c7d5043800c867a916c8fd6b1bb5e885e64e1b7b40047ddd1818158db`:

| Inventory | Compiled declaration scope | SHA-256 |
|---|---|---|
| `car_spectrum_amplification_claim_declarations_2026-10-25.json` | `car_amplification_times_spinor_eq_sixteen` states only `carDiracAmplificationFactor * 4 = Fintype.card ArchiveFockState`; the owner states the factor is 4 and its product is 16. It does not state an operator decomposition or a mode limit. The arithmetic owner has no axioms; the equality-to-card theorem has `Classical.choice`, `Quot.sound`, and `propext`. | `6f6feef0d0255d59bf715fea675411e7a2e913f032acfe9b8a0b44d1497b60aa` |
| `dirac_heattrace_multiplicity_claim_declarations_2026-10-25.json` | `diracHeatTraceMultiplicity_eq_fock_dim` equates the declared integer to the Fock cardinality; the owner states both are 16. No trace, exponential, or spectral sum occurs in either type. Both have `Classical.choice`, `Quot.sound`, and `propext` in their axiom closures. | `b0d1298429f95c1680a0a8ca6fa0a906023065c183448c71692599c0ddc50abc` |

The spectrum-amplification row still requires an explicit invariant
decomposition/intertwiner into four spinor copies and analytic convergence of
the finite eigenvalues to the stated continuum modes. The heat-trace row still
requires definitions of the finite traces and a trace identity derived from
an accepted square or decomposition. These are separate remaining premises;
the cardinality equalities do not imply either one. The inventories were
generated sequentially from the same clean source snapshot: the first records
`worktree_dirty=false`, and the second `worktree_dirty=true` because the first
JSON was present. Neither query changes a Lean module or invokes `D0.All`.

**Disposition:** retain both claims OPEN. The existing Hodge and finite CAR
parity results remain at their own scopes and supply neither a spinor
decomposition nor a heat-trace definition/equality. This crosswalk changes no
claim, support row, source convention, or physical interpretation and closes
no C0 or GR obligation.
### Full cold-start replay before the expanded CAR/Hodge claim controls (25 October 2026)

The full cold-start runner completed on clean published snapshot
`02a5a6e2c734614cfaa0bdfe16bd90cf53714053`. All 20/20 real search cases
found every required source; the 21st exact-source impact benchmark also
passed. The source-change control changed its dependent digest, while unrelated
prose left that digest unchanged. The case-level receipt is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_02a5a6e2.json`
(SHA-256 `0bd58b2eba4b9ac31ebd0e29b08f1ea4446c07cf3de3f01f77c182da20d514c7`).
It captures all seven authority-source digests, 20 case-level required-source
counts, the impact result, Python 3.11.9, ripgrep 15.2.0, runner SHA-256
`e973584228ba06db4f75afb3417e3534e2f11b78045c9263851cc4b72acc0307`, and
search-engine SHA-256
`a6114ed772f36251a54953f13531694cac1734020f5ce128cafae0ae4eb8053b`.
Semantic scope review remains manual.

The subsequent head `86afce5f6ee5a98c707ac4e36aff65f7a95a413b` expanded the
CAR/Hodge case to include the CAR square, spectrum-amplification, and heat-trace
claims alongside the existing Hodge square, kernel, normalization, and shell
results. The focused `test_car_hodge_cold_start_keeps_distinct_operator_claims`
passed in `D0 guards` run 5160; `D0 Lean build` run 3122 also succeeded. This
validates the changed retrieval case on that head. The complete all-case replay
for the expanded case set remains part of the final Ready validation.

These results establish source retrieval, recorded exact pins, and the scoped
CAR/Hodge distinction. They do not accept claim semantics, freeze C0, or close
physical selection or GR.
### Current-source guard for compiled CAR/Hodge scope inventories (25 October 2026)

On head `c3f6aa1f896164819589136871e66f769d7dff91`, the strengthened
`test_car_hodge_cold_start_keeps_distinct_operator_claims` checks ten compiled
declarations: four CAR arithmetic scaffolds and six Hodge operator/kernel/shell
results. It requires each inventory's `lean_source_digest` to equal the digest
of the current Lean source tree and checks exact elaborated-type fragments,
declaration kind, axiom-list presence, and the one-sided Hodge `formal_support`
entries. `D0 guards` run 5163 and `D0 Lean build` run 3125 both succeeded.

This closes the stale-inventory and declaration-scope regression for this
bounded example. It still does not supply the missing CAR operator proofs or a
transport from Hodge; semantic claim acceptance remains manual, and the complete
cold-start replay on the expanded case set remains due at final Ready.

### Exact axiom-footprint control for the CAR/Hodge crosswalk (25 October 2026)

The focused guard now checks eleven compiled declarations: four CAR arithmetic
scaffolds and seven Hodge square, kernel, normalization, and shell results. In
addition to the current Lean-source digest and elaborated type fragments, it
pins each declaration's exact axiom closure. The Hodge square and kernel
explicitly retain the two existing finite `native_decide` CAR-identity leaves;
the other Hodge rows and three of the CAR scaffolds retain only
`Classical.choice`, `Quot.sound`, and `propext`, while the CAR zero-mode
constant has an empty axiom closure. The test therefore detects both stale
inventories and an unreviewed trust-footprint change.

This is still a regression guard for compiled evidence, not independent
semantic acceptance. The Hodge operator remains distinct from the registered
hopping CAR matrix, all four CAR claims remain OPEN, and full cold-start/C0
acceptance and final `D0.All` integration remain outstanding.

### Correct stale Hodge proof list in the open CAR square registry note (25 October 2026)

The source review found that `claims.csv` row 815 still listed the Hodge
square, L=2 diagonal comparison, kernel, shell rank, and energy limit as
missing even though their scoped Lean declarations are present. The row note
now records those results and their exact Hodge/cochain scope, including the
factor-two L=2 comparison. It also states the remaining boundary: no operator
square/kernel for the distinct hopping `carDirac`, no typed map to the
registered `D_L`/`Delta_L^(4)` tensor formulation, and no matching exact Book
06 heading.

The claim ID, book/section locator, module/theorem locator, `OPEN` status and
`PROOF-TARGET` release status are unchanged. `proof_architecture show`
confirmed the revised note while returning the same open claim; generated
`ClaimMap.lean` remains current. The cold-start test now checks that the note
records the proved Hodge square and missing typed transfer, preserves `OPEN`,
and does not restore the former `EXACT MISSING: D_H squared` wording.
`validate_repo.py` passes with zero warnings, `generate_lean_views.py --check`
passes, and
`check_claim_map_coverage.py` passes under Python 3.12.14.

The regenerated exact-heading candidate view is
`sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json`,
at clean source snapshot `4b0630b1b3220857e5ef52f3e4041803277b71c7`. Its
`claims.csv` SHA-256 is
`f6d0b25659f137fda4ba35f17dbfba00899ec384a42fbad601ebaf1feb4f2003`; the
view SHA-256 is
`005703883c253df5a2e51659293dbefba086452c06eb4f1229721fe4d8ec2537`. It
still reports 889 claim rows, 94 uniquely resolved rows, four partial rows,
zero ambiguous rows, 611 unresolved rows, and 170 malformed composite rows.
These are locator-resolution counts only. The existing full cold-start
summary remains pinned to its earlier registry snapshot; regenerate it with
the expanded case set at final Ready. No C0 freeze, coverage acceptance,
operator transfer, or physical closure follows from this note correction.

### Candidate C0 source-unit map: finite Hodge complex core (25 October 2026)

This is a source-map reconciliation for `D0-HODGE-001`, not claim acceptance,
C0 acceptance, or a coverage result. An independent read-only source review
was performed at the previous PR head
`efb6423281c83d206fcf3f085b80471fc85510a6`. The only subsequent `claims.csv`
edit is row 815; row 192 and the Book/Lean sources below are unchanged. The
regenerated exact-heading candidate view at source snapshot
`4b0630b1b3220857e5ef52f3e4041803277b71c7` still marks the registered Book 07
locator unresolved. Current source identities at that snapshot are:

| Candidate source | Git blob | SHA-256 | Scope |
|---|---|---|---|
| `02_REGISTRY/claims.csv` | `f5a01cd7a74ea8940dc40e0ddfd511f1b7d88611` | `f6d0b25659f137fda4ba35f17dbfba00899ec384a42fbad601ebaf1feb4f2003` | Row 192 keeps `D0-HODGE-001` at `BOOK_07 / finite Hodge complex core`, `LEAN_PROVED` / `CORE-FORMALIZED` |
| `01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md` | `a5a0d800d906c3cd02713bab42ab80722fd799a8` | `d02a7fc25034c914a70b70a30339a509e1196b9300cfe2ee4f071409e77737fb` | No exact heading; lines 184–185 only say the finite TT carrier is compatible with a finite Hodge complex |
| `01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md` | `bea003880b42666ce9568dfa98c8a09b5d6cd852` | `051234590ec6f8cf8d93f84b4ab91779af2925000d2b73edde19091d9f7a70d1` | Line 175 heading “Finite cochain complex and Hodge Laplacian” gives the general carrier; §02.27 at line 1883 records the `K(9,11,13)` cochain complex and `∂₁∂₂=0` at lines 1885–1893, but not the scene ranks, middle exactness, adjoints, or full Hodge results |
| `03_FORMALIZATION/D0/Topology/BoundaryBoundary.lean` | `7fba27d1d9f680ebb7e63a49b6eae9cefbcba03c` | `c2ad42e5cdb4177a1fa78a2d6fd1a4ba87b305f365bcbba3d1cd44b33630a8e5` | Generic incidence identity `boundary_boundary_zero`, lines 5–7 |
| `03_FORMALIZATION/D0/Topology/FiniteCochainNoAxion.lean` | `2d9a4175d89b26a9e387fb0bebfad2d9d8df651a` | `c24876d440a0a9f806bbb64ed431d37b5ff51da26444bc8d60ae5285ce397d37` | Generic graded cochain identity `finite_d_d_zero`, lines 10–18 |
| `03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean` | `08bc045297b3bb839e7aabfba0ee438280f822ff` | `13798b43d8bca20c0d9bc42efbeb03cc8a9196e4a9316dafff085cc5d9a5f12d` | Lines 10–19 define actual rational tripartite incidence maps for `(p,q,r)=(8,10,12)`, i.e. zone sizes `(9,11,13)`; lines 39–134 prove carrier counts, incidence ranks, nilpotency, and exactness |
| `03_FORMALIZATION/D0/Geometry/SceneHodgeDecomposition.lean` | `f2ca68e267f6ad86536933249908456160175eef` | `50fd6322248017048bb1b3053d0aad24f4af9588acb0947d2c7545ff6466dd3c` | Lines 10–14 bound this to literal Euclidean cochains; lines 35–163 prove adjoint identities, codifferential nilpotency, exact/co-exact orthogonality, and `H¹=0` |
| `05_EXPERIMENTS/FiniteHodgeComplex/finite_hodge_manifest.json` | `d250fd7b0eac92056d9e4e1443fdd78feafae068` | `66f6b6c8b39be1cc1bed6ae49fbab7c03abc5e731116cea81e50755642abd7fb` | Historical manifest explicitly says its Book update is in Book 02 |
| `04_CERTIFICATES/vp_finite_hodge_complex_core.py` | `2dddecaabb44334faaed97af0a36a8972dc55d3a` | `de53f90de28540769321c27848ed7ed3d367044fa5a13493d10113be52a51e44` | Exact certificate is only the tetrahedron (`4,6,4` carriers), `d₁d₂=0`, `L₀`, and `b₀=1`; it does not certify the `K(9,11,13)` specialization |

The independent review concluded that Book 02 is a valid candidate source, but
the current locator does not resolve and a Book 02 citation alone does not
cover the whole claim. The appropriate candidate is a composite source map:
the two Book 02 passages for general context and the scene cochain identity,
plus the exact generic and specialized Lean modules for the formal claims. The
exact-heading resolver cannot turn this semantic composite into an accepted
source automatically. Do not append the current Book 07 body-text locator to
Book 02 as if both were exact headings, or treat the tetrahedron certificate
as evidence for the scene specialization.

The source map does not change `claims.csv`, the existing owner, theorem
locators, release labels, or the explicit limits in the claim: no `B₊`,
`ker B₊`, `Q_H`, weighted metrics, spatial propagator, or TT dynamics. Source
owner review and independent C0 disposition remain open; no coverage is
reported.

### Compiled claim-to-Lean reuse view for D0-HODGE-001 (25 October 2026)

Ran `reuse --lean D0-HODGE-001 --import-root D0.All` on source snapshot
`d37152b7a330e4fd616ebe9e171efb793a6dabb1`. The generated view is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/d0_hodge_001_compiled_claim_reuse_2026-10-25.json`
(Git blob `36f03af0970fe78fc060a7cdedb9d43a7781d46b`, SHA-256
`44474c2d42bc6356494abda57043076f8463866f5799654823842cda4ce8eeda`,
129,620 bytes in the Git blob). Its 12 theorem-name locators all resolve to 12 compiled
declarations; the view records each elaborated type, source range, proof/type
dependencies, and axiom footprint. `lean_source_digest` is
`6c459c7340129d85977a72a6ebbdadbe0fd796318859948a7789ab42c1b7f590` and the
collector SHA-256 is
`101d89cc1a197f2951f67eb2a43480a4ae0f20fecc0a6d8a1a380255780cae2e`.

The compiled types establish the exact finite scope: scene carrier counts
`33, 359, 1287`; boundary ranks `32, 327`; the middle range/kernel equality;
the rational cochain adjoint identities; exact/co-exact orthogonality; and
zero rational first homology. All 12 declarations report the same axiom set:
`Classical.choice`, `Quot.sound`, and `propext`.

The compiled dependency view contains nine candidate links. One crosses to
`D0-GRADED-BIANCHI-EXACT-001`: `finite_d_d_zero` actually depends on
`D0.Topology.discrete_exact_bianchi`. Eight links point to theorem locators
inside `D0-HODGE-001`. The claim metadata has no declared assembly applications
or assumptions. These elaborated proof dependencies are useful retrieval
evidence, while the dependency-to-claim joins remain name-locator candidates;
they do not create an accepted application edge or C0 disposition. The view
therefore improves exact reuse discovery without changing claim status, owner,
or physical scope.

### Independent review of the compiled Hodge reuse view (25 October 2026)

An independent read-only review at published PR head
`5e91b1be54732aa3590338cf97ca419535b7c941` returned scoped PASS for the 12
compiled locator records. Every claim atom resolves to exactly one declaration,
and each selected source range contains the declaration named by the locator.
The reviewed ranges are `BoundaryBoundary.lean:5–7`,
`FiniteCochainNoAxion.lean:15–18`, `SceneCochainComplex.lean:55–62, 64–77,
79–86, 101–134`, and `SceneHodgeDecomposition.lean:34–62, 64–92, 94–123,
125–132, 140–146, 148–163`. The recorded types match these declarations.

The review sharpened two scope boundaries. First, the implicit parameters of
`scene_first_homology_zero` and the corresponding conjunction component
pretty-print as `FirstHomology` without their fixed indices; their source
specializes to `sceneP/Q/R = 8/10/12`, so this is the rational `K(9,11,13)`
case, not a general first-homology theorem. Second, the module name
`SceneHodgeDecomposition` does not imply a full direct-sum Hodge decomposition:
the recorded results are the listed adjoint/cochain identities, orthogonality,
and `H¹=0` only. The tetrahedron certificate remains separate from the scene
complex.

The direct elaborated dependency from `finite_d_d_zero` to
`D0.Topology.discrete_exact_bianchi` is genuine. The latter declaration is
defined in `D0.Topology.GradedIncidenceComplex` at lines 39–41, whereas the
claim row's module field says `D0.Gauge.GradedBianchiIdentity`; that field is
only the claim's registered locator/import context, not the declaration owner.
The reviewer confirmed the claim row and all mapped Lean-file blobs are
unchanged between the artifact snapshot and the published review head. This
remains a candidate claim crosswalk, with no assembly application or owner
acceptance. The independent review accepts artifact integrity and the stated
finite scope only; it does not accept the claim semantics, freeze C0, or close
a physical premise.

### Historical C0 claim-source candidate snapshot at `6a160a11` (25 October 2026)

This subsection preserves the first regenerated snapshot. It is superseded as
the current view by the `eb405cbd` checkpoint below; its counts and artifact
hash refer only to the historical snapshot.

The claim-source view previously labeled 170 rows `malformed_locator` because
each listed multiple books but only one descriptive section string. The new
resolver preserves these as **unresolved, unpaired** source sets. It emits a
separate candidate group per listed book; an exact heading or ranked lexical
heading remains a retrieval candidate and never creates a book/section pair.
Single-book descriptive locators also receive up to three ranked heading
candidates. Numeric section IDs receive no lexical fallback when their exact
heading is absent. Lexical suggestions require at least two locator terms in
the heading and at least 75% of the locator terms in the heading's section
text, with a one-term locator requiring its single term. This keeps malformed
source syntax, missing exact headings, and unreviewed search suggestions
distinct.

The historical view is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json`
(SHA-256
`81b8fe55cb2afee4b99d1c9ce941399ad842a4fa99c2fa0d68df8448018580ef`),
collected cleanly at `6a160a11f5f732c6c964864075cc94b7c6e2b010`. Its collector
SHA-256 is
`cb4d6c92b777d5daeb590d952dc8dd9de6bb81e681237179916a458a30b54d52`, and the
`claims.csv` SHA-256 remains
`f6d0b25659f137fda4ba35f17dbfba00899ec384a42fbad601ebaf1feb4f2003`.
For the same 889 claim rows, that snapshot reports 94 exact unique rows, four
partial rows, zero ambiguous rows, 781 unresolved rows, 10 non-book rows and
zero malformed rows. Its 731 actual locator pairs are unchanged: 116 exact
unique and 615 unresolved. The 170 shared-book rows remain unresolved with no
paired locator; 242 rows expose 416 ranked heading candidates. These counts
describe source-location retrieval only, not C0 membership, semantic coverage,
or accepted claim-to-source maps.

As controls, `D0-FOUND-001` remains unresolved while the view surfaces
unreviewed candidates in both listed books. `D0-HODGE-001` still has no exact
Book 07 heading candidate, and the pseudo-section `06.spectral` for
`D0-ARCHIVE-CAR-DIRAC-SQUARE-001` receives no lexical fallback. The focused
source-locator regression passes, and the complete proof-architecture suite
passes 45/45. This parser/candidate improvement adds no Lean theorem, claim
status, C0 disposition, or physical conclusion; source-unit review and
independent C0 acceptance remain outstanding.

### Candidate C0 crosswalk for the graded Bianchi claim (25 October 2026)

The exact compiled reuse view for `D0-GRADED-BIANCHI-EXACT-001` is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/d0_graded_bianchi_compiled_claim_reuse_2026-10-25.json`
(SHA-256
`5c3d5b9f41b96ac892a9a1e68afcae7edef8e3e4954c12e2d91ab22a6ce81c7d`),
collected at `c042c1a73c7463a750a6631a37973194152ffaa9`. The registered claim
row at that snapshot is pinned by blob
`f5a01cd7a74ea8940dc40e0ddfd511f1b7d88611` and SHA-256
`f6d0b25659f137fda4ba35f17dbfba00899ec384a42fbad601ebaf1feb4f2003`.
Its original `BOOK_05/06 / graded incidence Bianchi closure` locator has no
unique pairing. The current candidate view correctly leaves it unresolved and
unpaired. A manually identified source-unit candidate is
`source:c042c1a73c7463a750a6631a37973194152ffaa9:01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md#L1121: 06.32.1 Boundary status for Hurwitz, Bianchi and gauge transformations`
(Book 06 blob `99721fb50de66688564638f5f2b449a38675d7bd`, SHA-256
`592bbbb1dae9cc599df2eef9cabf117b19f8566d755ad072b77beb04624271d7`). That
section names `D0.Gauge.GradedBianchiIdentity` and explicitly limits the
ungraded non-abelian matrix residual to its recorded no-go. The Book 05/06
claim locator still needs source-owner reconciliation; this candidate does
not update the registry or accept the source mapping.

At the same immutable snapshot, `D0.All` resolves all five theorem atoms to
compiled declarations. `GradedIncidenceComplex.lean` supplies
`D0.Topology.graded_nilpotency` and
`D0.Topology.discrete_exact_bianchi` for
`GradedCellComplex`, plus `D0.Topology.graded_bianchi_exact` for
`GradedCellComplex3`; `GradedBianchiIdentity.lean` supplies the two Gauge
compatibility wrappers. The elaborated types and exact source ranges are in the
view. The Topology source blob is
`536ebd764d874651f30032eed6a2915043e711c0` (SHA-256
`959e38f191ff40ff895ad93f0fc650d9db7a3f473a631751386acba131f1d813`); the
Gauge source blob is `e1112312bc36b42631cdae2089a4794bf4cfd41e` (SHA-256
`840a3e61aa8ad4680b8626d53d0ccfb898af28380e21ba1e280f7a7254ea06a2`). All
five declarations have the same transitive axiom footprint:
`Classical.choice`, `Quot.sound`, and `propext`.

The scope is conditional on the supplied finite complex. Its
`boundary_nilpotency` field is an input to `discrete_exact_bianchi`; the
three-cell extension supplies `boundary_nilpotency2`, and
`graded_bianchi_exact` returns that field. Thus the finite-sum theorem proves
`d₁(d₀ A)=0` from the declared boundary-composition law, while the separate
three-cell equation is carried by the structure. The Gauge wrappers preserve
those types. This does not instantiate a concrete D0 mesh, derive physical
curvature identities, or discharge a gauge/source application.

The compiled Hodge reuse view records the real Lean proof dependency from
`finite_d_d_zero` to `D0.Topology.discrete_exact_bianchi`. That is proof-level
reuse evidence; the join to the Bianchi claim ID remains a locator candidate,
and neither claim declares a reviewed assembly application. Claim status stays
`LEAN_PROVED` / `CORE-FORMALIZED` at its own finite conditional scope. No C0
membership or semantic acceptance is inferred.


### Bianchi lexical source-candidate retrieval follow-up (25 October 2026)

The lexical fallback now allows one matched heading term when the section text
matches at least three quarters of the locator terms. Commits
`8ba7119e6364bd9e4935fd081e52f5f2e04a3b31` and
`8c6e961b4c62aef911ba1696618d3bbc0f9d71ef` add this retrieval rule and a
focused regression for the unpaired Bianchi locator. The regression passes.

On source snapshot `8c6e961b4c62aef911ba1696618d3bbc0f9d71ef`, the resolver
surfaces Book 06 §06.32.1 as one `unreviewed_lexical_candidate`, matching all
four locator terms. Book 05 has no candidate. The source row is recorded in
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/d0_graded_bianchi_source_candidate_2026-10-25.json`
(Git blob `1c30937508e44b74171d0aabdaae58f0f4765f88`; artifact commit
`d895310f2e4efce2fb890dea23bcd05732ad0d83`). The original
`BOOK_05/06` locator remains unresolved and unpaired. This changes candidate
retrieval only: it does not assign the Book 06 source, update the claim row,
change status or owner, accept C0, or close a physical premise.

### Source-candidate and compiled Bianchi checkpoint at `eb405cbd` (25 October 2026)

The checkpoint candidate view is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json`
(SHA-256
`218ef724270ae90c4cf88a6d6e6b10c9ccd2dde1bb841713a62d08920fbacf8d`),
generated cleanly from snapshot `eb405cbd36c591203efe867526ccef2e3e173a5c`
with collector SHA-256
`c18c5e32cc3176c0a2527627f1e4a56681acfffa13ebf11469522c36b547d93d`.
`claims.csv` remains pinned by SHA-256
`f6d0b25659f137fda4ba35f17dbfba00899ec384a42fbad601ebaf1feb4f2003`.
Across the same 889 claim rows it reports 94 exact unique, four partial, zero
ambiguous, 781 unresolved, 10 non-book and zero malformed rows. There are 731
locator pairs (116 exact unique, 615 unresolved), 170 unresolved unpaired
multi-book rows, 380 rows with ranked heading candidates, and 711 ranked
candidates. These remain retrieval counts, not source acceptance or C0
coverage.

The resolver at this checkpoint requires at least one matched locator term in the
heading and at least 75% of the locator terms in that section's text. Numeric
section IDs still receive no lexical fallback when their exact heading is
absent. For `D0-GRADED-BIANCHI-EXACT-001`, Book 06 §06.32.1 is surfaced as an
unreviewed lexical candidate matching all four terms (`graded`, `incidence`,
`bianchi`, `closure`); Book 05 has no candidate. The shared `BOOK_05/06`
locator remains unresolved and unpaired. The current row records the source
key against `eb405cbd` and the matching Book 06 blob; no source pairing or
semantic claim acceptance is inferred.

The checkpoint compiled declaration inventory is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/d0_graded_bianchi_compiled_claim_reuse_current_2026-10-25.json`
(SHA-256
`6ad6daa9d57630a96322d9849b643ea29f7526cde419fbfd69808c27e0af1eaf`). It
was collected cleanly at the same snapshot with public import root
`D0.Gauge.GradedBianchiIdentity`, Lean source digest
`8909eebca5df94b496915718cd6bd853f9c2147d2b1e3bd43fd6950433abe9a8`, and
collector SHA-256
`6488dd50771c225d45c7874452c9e54028486d358f9130e7ff146fdd360562a4`. It
resolves the same five declarations: the three generic Topology theorems and
two Gauge wrappers. Each reports axioms `Classical.choice`, `Quot.sound`, and
`propext`. The wrapper source blob at this snapshot is
`8ea893bd9e826d00b205bb1c75994c2ec5b8d7d0`; `GradedBianchiIdentity.lean`
keeps both public theorem signatures and delegates directly to
`D0.Topology.discrete_exact_bianchi` and
`D0.Topology.graded_bianchi_exact`. The narrow build succeeded for
`D0.Gauge.GradedBianchiIdentity` (2,949 Lake jobs).

The direct wrapper reuse is a small compatibility-layer refactor; it does not
strengthen the generic theorem premises. `discrete_exact_bianchi` still uses
the supplied `GradedCellComplex.boundary_nilpotency` field, and the three-cell
statement remains conditional on `GradedCellComplex3.boundary_nilpotency2`.
The theorem family is not an instantiated D0 mesh, physical curvature law, or
accepted C0 application.

The Lean source change made the existing CAR/Hodge source-digest guards reject
11 stale declaration inventories. All 11 were regenerated at clean source
snapshot `4443d184663c99ea09f003ff9fed6dd50ef17184`; their 57 declaration rows
were unchanged. The proof-architecture suite then passed 45/45, and the
focused Lean module build passed. This refresh records source provenance; it
does not revise any claim, assembly edge, or physical interpretation.


### Current CAR/Hodge inventories and D0.All Bianchi reuse (25 October 2026)

The common Lean source digest after the Bianchi wrapper refactor is
`d775d429420bea2867f256924cdb55389f29c4dc4653cddfba4576629c9db3bb`.
All eleven CAR/Hodge declaration inventories now match it and record clean
generation. Their 57 elaborated declaration records are unchanged from the
previous inventories. Five were generated at clean snapshot
`60e4007f7dda87d106b3d54a545a5d03294d30c1`; the remaining six at clean
snapshot `f9afa4bcfffd8212fc23a3f5ba415aab0c3d3ad0`. Their published Git
blobs were verified on PR head `29ce093a9596089a522b9a066caa351af8a53fc6`:

| Inventory | Git blob |
|---|---|
| `car_zero_mode_claim_declarations_2026-10-25.json` | `bca39a85559d4f4f2dd5131c5724141f0b214ecd` |
| `car_dirac_square_claim_declarations_2026-10-25.json` | `67dda6f1046549588e47c03225c9f07ca8f671b8` |
| `car_spectrum_amplification_claim_declarations_2026-10-25.json` | `011e23017ecd0e37ac52617ce60214ce0e6ac5f9` |
| `dirac_heattrace_multiplicity_claim_declarations_2026-10-25.json` | `3ef683cd63d8f42d7f6902915f0bbf533c9b0cd0` |
| `hodge_car_dirac_kernel_declaration_2026-10-25.json` | `b6ba36f7861b66ce014fef548575446c511349fa` |
| `hodge_car_dirac_l2_normalization_declaration_2026-10-25.json` | `43a6ebb12fb17647d8f3cb4bc4e783458bc64727` |
| `hodge_car_dirac_square_declaration_2026-10-25.json` | `98e13ff7db89f3d8a503975927c985a0e25c9392` |
| `hodge_shell_energy_limit_declaration_2026-10-25.json` | `3ba6ea8f76f3041cb7f4734bacdcf80e73623760` |
| `hodge_shell_rank_l2_control_declaration_2026-10-25.json` | `674e0dd696120e816fc4b56004a0c62cb4381e20` |
| `hodge_spatial_shell_claim_declarations_2026-10-25.json` | `e6a5d1902df9d8386273f590006891a674267a72` |
| `hodge_square_backward_forward_declaration_2026-10-25.json` | `82288267f25b4f865b5789b0e2fa6cb4591c7ab1` |

The Bianchi claim-reuse command was also rerun against public import
`D0.All` at clean snapshot `60e4007f7dda87d106b3d54a545a5d03294d30c1`.
The view is
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/d0_graded_bianchi_proof_architecture_reuse_d0_all_2026-10-25.json`
(Git blob `b5da6a98169ec9cf1dae9ca8eccbcddba68adceb`), with Lean source
digest `d775d429420bea2867f256924cdb55389f29c4dc4653cddfba4576629c9db3bb`
and collector SHA-256
`6d3b9fc7e65a135a5727905b22b83c1f18131e51639b6e1daaa7420267ab8cb5`.
It resolves the same five declarations under `D0.All`; their elaborated
types, proof dependencies and axiom sets are unchanged. The two Gauge
wrapper source ranges now end at lines 15 and 20 after the direct-core
refactor. The dependency-to-claim-locator joins remain candidates, not
accepted application edges.

On this source tree the full proof-architecture suite passes 45/45. The
narrow `D0.Gauge.GradedBianchiIdentity` build passes (2,949 Lake jobs).
GitHub `D0 guards` run 5188 and `D0 Lean build` run 3150 both passed on
`29ce093a9596089a522b9a066caa351af8a53fc6`. These results establish
reproducible finite declarations and retrieval; they do not freeze or
accept C0, change claim statuses or owners, select a physical source, or
close the remaining physical GR premises.

### Literal CAR hopping square: exact `L=2` counterexample (25 October 2026)

The mapped OPEN row `D0-ARCHIVE-CAR-DIRAC-SQUARE-001` names the literal
nearest-neighbour `carDirac`/`hoppingCarDirac` and the identity
`D_L^2 = Delta_L^(4) tensor I_16`. A scoped counterexample is now formalized
in `D0.Geometry.ArchiveCARDirac`:
`carDirac_square_ne_archiveMetricProductLaplacian_at_zero` proves
`carDirac 0 * carDirac 0 != tensorProduct
(archiveMetricProductLaplacian 0) fockIdMatrix`, where `n=0` means the actual
two-site period `L=2`.

The proof uses the constant spatial vacuum vector. The metric product
Laplacian kills its spatially constant profile. For the current hopping
matrix, its image has a nonzero singleton-A component at the origin: the
component is the sum of nonnegative nearest-neighbour coefficients and the
site obtained by updating only coordinate A from 0 to 1 contributes exactly
1. If the square identity held, self-adjointness would force the dot product
`(D v) dot (D v)` to vanish; coordinatewise nonnegativity would then make
every entry of `D v` zero, contradicting that component. The compiled
declaration inventory records the exact type and axiom closure, including the
existing finite `native_decide` support lemmas; no new axiom or `sorry` was
introduced.

This is a no-go only for the current `carDirac` matrix, the owned metric graph
Laplacian, and the `L=2` carrier. It does not transfer the Hodge/cochain square
to the CAR carrier, rule on a differently normalized or selected operator,
or identify the absent `BOOK_06/06.spectral` source unit. The claim and
`formal_support` rows remain unchanged and OPEN pending source/operator
reconciliation and owner review. It is not a C0 disposition or a physical
interpretation.

The narrow Lean build passed for `D0.Geometry.ArchiveCARDirac` (2,977 Lake
jobs) on Lean 4.30.0. The new compiled record is
`sources/d0_proof_architecture_formalization_2026-10-24/car_dirac_square_l2_no_go_declaration_2026-10-25.json`
(SHA-256 `5166885f0aa5b9bdb1d720b5336e95c4c9727364a492926739bcab969244a3f2`),
collected at snapshot `29ce093a9596089a522b9a066caa351af8a53fc6` with
`worktree_dirty=true`, public import root `D0.Geometry.ArchiveCARDirac`, and
Lean-source digest
`089f0e6d888039facb2fc3354eec21f40be34530bb5fde39d32c6a5c67974768`. The
CAR/Hodge declaration-scope regression now checks this type and its exact
trust footprint alongside the prior eleven declarations. This checkpoint
does not run final `D0.All`, freeze C0, or accept the OPEN claim.

All eleven pre-existing CAR/Hodge inventories were regenerated from the same
dirty worktree snapshot so the current-source guard continues to cover the
changed Lean tree. The new no-go inventory uses the same Lean-source digest
and snapshot; all twelve records have `worktree_dirty=true`. Their SHA-256
values are:

| Inventory | SHA-256 |
|---|---|
| `car_zero_mode_claim_declarations_2026-10-25.json` | `6e59e54a77c618260d5b297f033d5466642fcaf00b88c0f50a4d84c7009163e7` |
| `car_dirac_square_claim_declarations_2026-10-25.json` | `9aef69306d3190f29713adc14aedd5a20eb0a99cd0aacc0a08d27248f0521587` |
| `car_spectrum_amplification_claim_declarations_2026-10-25.json` | `4de444d2eb117e70499ffd568771b80ec981a7d7297f651d96f52c1a9da6fd52` |
| `dirac_heattrace_multiplicity_claim_declarations_2026-10-25.json` | `b35421bd30117a67e3bf7af3fb147c4ff60ebd22c49ca6578051c4a11535dbf5` |
| `hodge_car_dirac_square_declaration_2026-10-25.json` | `7b803bfbc096e5bbf39bc790ca101f569d3003796475ae71fe9334ef7e49fdbd` |
| `hodge_car_dirac_kernel_declaration_2026-10-25.json` | `f0a77381c0d6b186568bce2a23a31daf72d58385c011a3f80f06ba6ab920f081` |
| `hodge_square_backward_forward_declaration_2026-10-25.json` | `d986a114125f5733acf07b09d09b0ded8a7d73693e2f6aa8a470f23460fcb8b5` |
| `hodge_car_dirac_l2_normalization_declaration_2026-10-25.json` | `e67fdc0c8f56644d772ff4697ef93ff852240a7e0843c01e8b7e347fca35a196` |
| `hodge_spatial_shell_claim_declarations_2026-10-25.json` | `fd085633b6155ef29e92a3b009a6e32186ce6b97a1bcdba26aa563897e14436e` |
| `hodge_shell_energy_limit_declaration_2026-10-25.json` | `35ca1f710fc574f90ec4e71a606a3a11a5b239431c69c5c4a03af9f11ffbaed1` |
| `hodge_shell_rank_l2_control_declaration_2026-10-25.json` | `c4514380155772062892a1fe388fffafb07cc0f57dda032f6ebe4ae07e2f92f1` |
| `car_dirac_square_l2_no_go_declaration_2026-10-25.json` | `5166885f0aa5b9bdb1d720b5336e95c4c9727364a492926739bcab969244a3f2` |

### Literal CAR hopping zero-mode follow-up: exact `L=2` exclusion (25 October 2026)

The current hopping operator admits a stronger finite control than the earlier
square-versus-Laplacian no-go. At `n=0` (`L=2`), each spatial role block is a
coordinate flip. The exact integer spatial controls prove each block squares
to identity and that the blocks commute. The already-owned finite CAR
anticommutation relations then give
`carDirac_square_eq_four_id_at_zero : carDirac 0 * carDirac 0 = 4 • 1`.
Consequently `carDirac_zero_kernel_trivial_at_zero` proves
`carDirac 0 *ᵥ v = 0 → v = 0` on the complete site × Fock carrier.

The computation is confined to the 16-site spatial factor and uses integer
entries; the CAR cross terms are discharged from the existing creation and
annihilation relations. The compiled square and kernel inventories record the
resulting exact trust footprint, including these finite `native_decide`
controls. No new axiom or `sorry` was introduced. The dense 256-by-256
matrix-square proof path was discarded after its narrow build remained
CPU-bound without diagnostics; it is not part of the artifact.

This is an exact mathematical counterexample to interpreting the scaffold
`carDiracKernelDim := 16` as the kernel dimension of the current `carDirac`
at all periods: the actual kernel is zero at `L=2`. It does not prove an
all-period kernel formula, transfer the separate Hodge kernel, or close the
source locator. The zero-mode and square claim rows remain OPEN, with their
source reconciliation and owner review still outstanding; C0 and physical
GR status are unchanged.

The current-source inventories were written as follow-up snapshots rather
than replacing the prior records. All 14 inventories have
`lean_source_digest=3fb4418f79959a53ee700efa41976a9b845e237d995ae069f8769a0103f4b88e`,
`snapshot_commit=831f1717f3145dd63eca4f0c9d0d9f6357b02f12`, and
`worktree_dirty=true`:

| Inventory | SHA-256 |
|---|---|
| `car_zero_mode_claim_declarations_followup_2026-10-25.json` | `ae52c64e8f92f68fda062430082c4e7d7a8838ca4c440e6e1d3c264fb500df3f` |
| `car_dirac_square_claim_declarations_followup_2026-10-25.json` | `2e0b530f0c3adab47bc21b552f9e2db06d7ebdab27cdea5044a4471c38194e9d` |
| `car_spectrum_amplification_claim_declarations_followup_2026-10-25.json` | `1ff1f7aa991f8be9a8a51681681e65dc054d273a3500f18a470245f430bc2a7c` |
| `dirac_heattrace_multiplicity_claim_declarations_followup_2026-10-25.json` | `d31bb6b78975811265ca27ca75d0049201e242191be9b2576b20a183f6d0096b` |
| `car_dirac_square_l2_no_go_declaration_followup_2026-10-25.json` | `c277a8cba05f37e944378462d565105f595fff0c88c1b0dcad5c770fff54b22a` |
| `car_dirac_square_l2_identity_declaration_2026-10-25.json` | `9bb3bcd36991434534b6557e628f5dfe87254ec5d952a57bb48eca9884735a12` |
| `car_dirac_l2_zero_kernel_trivial_declaration_2026-10-25.json` | `ae92bda5a021fc10f185b555302427a6cb7df0cc71dcf203464e585772bc1661` |
| `hodge_car_dirac_square_declaration_followup_2026-10-25.json` | `c4db89c7eaee8f76d134de4ff1989991b045c9ad61f23567fe5b81498c2b1bb5` |
| `hodge_car_dirac_kernel_declaration_followup_2026-10-25.json` | `b693ccc26e8e3d04434e01d119de4e6ece1111d12f038425295d187a3875fc0d` |
| `hodge_square_backward_forward_declaration_followup_2026-10-25.json` | `48f52c57b3e3c52105dcb3eabc0ccbd0f3e4bf74e63dc15d0ab8378356809d44` |
| `hodge_car_dirac_l2_normalization_declaration_followup_2026-10-25.json` | `bf13475a53cf68a9dc831dc33359ad313eecfdc346b22e31cd177a00fc116d1f` |
| `hodge_spatial_shell_claim_declarations_followup_2026-10-25.json` | `5b79d0d70286ab114f5d7e602eada37ee40efbc1ebb16e03f09cd9973650a904` |
| `hodge_shell_energy_limit_declaration_followup_2026-10-25.json` | `8027c36fa674e3a7b2c7a566c23a09dd8709f842c4a4eb9523ef4838400122d0` |
| `hodge_shell_rank_l2_control_declaration_followup_2026-10-25.json` | `1d00bd41ad5b32e985f99474855b4a09e6a7f962b967a62f700a1daef58ea880` |

The regression now checks the exact `L=2` square and kernel types and their
axiom closures together with the existing CAR/Hodge declarations. This
checkpoint is scoped finite mathematics; it does not promote either OPEN
claim or change physical D0 status.

### Generic finite tensor algebra consumed by the CAR square (25 October 2026)

Added `D0.Algebra.FiniteMatrixTensorProduct` as a geometry-independent home
for finite matrix tensor products, their multiplication/addition/scalar laws,
the product identity, and the finite Clifford-square reduction for commuting
first-factor blocks and Kronecker-anticommuting second-factor blocks. The CAR
module now keeps `D0.Geometry.tensorProduct` and `tensorProduct_mul` as
compatibility names while delegating their implementation to this shared API.
Its former private add/scalar proofs and 60-line CAR-specific square
rearrangement are replaced by an application of the generic square theorem.

The consumer is the literal hopping CAR operator. The existing `L=2` spatial
coordinate-flip identities and owned CAR anticommutators instantiate the
generic reduction, yielding the exact `D²=4I` theorem; the zero-kernel result
then follows on that same finite carrier. This is one algebra API -> real
consumer refactor with an executable compatibility path. It says nothing
about other periods, the distinct Hodge operator, the all-period claim, or
physical selection. The associated zero-mode and square claims remain OPEN,
and no C0 denominator or physical status changes.

The new module is listed in `formal_support.csv` and the generated `D0.All`
public import. `lean_declaration_inventory.py --name` now accepts repeated
exact names, allowing one current compiled-source inventory to replace
per-result re-enumeration. The CAR/Hodge scope regression checks one such
17-declaration inventory; prior crosswalk files remain historical snapshots
at their original source pins. This avoids regenerating the fourteen
versioned candidate inventories for every unrelated Lean-source edit.

The current inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_current_declaration_inventory_2026-10-25.json`,
SHA-256 `95c7fdb21d78009edc81f16bba1b8d3fe7a15e9e0384286907ef0d749b5eb829`.
It records snapshot `81577a0eee9c383f10900fed92fea12e99c920f7`,
`worktree_dirty=true`, public import root `D0.All`, Lean-source digest
`a88e5ddb1f0dae71e62e9f7a093c19060dd5465ee9dfcaed2c24e51f5f976901`, and
collector SHA-256 `9d8f81a6de74511e2d215c5837f192b0e8e851771ea7d99e592560a0f8f8f289`.
It includes the generic square/identity laws, the compatibility multiplication
theorem, and the exact CAR/Hodge declarations used by the cold-start control,
with elaborated types and axiom footprints. The collector's successful query
also built `D0.All` before reading declarations. The Lean 4.30.0 narrow builds
passed for `D0.Algebra.FiniteMatrixTensorProduct` and
`D0.Geometry.ArchiveCARDirac`; the full import replay is an integration
checkpoint, not a Ready or final publication build.

Source SHA-256 values are `d26f5ccbfdd0e01566a49ccf46ce4ac0c78f223a35e05fae6d544dbee9d320d2`
for `FiniteMatrixTensorProduct.lean`, `bbdf412934a471e67890f2b230bf1e6a65de0d55cd03ef23ed129a0f0bc4b1df`
for `ArchiveCARDirac.lean`, and `fa8ef745339d45a22d539a899f5be7f3e92d3abe19f47bbc0be5e618c8c8553d`
for the generated `D0/All.lean`. The exact declaration scope regression
passes with the consolidated current inventory; `test_proof_architecture.py`
passes 45/45 and `test_lean_declaration_inventory.py` passes 16/16.
`check_claim_map_coverage.py`, `check_no_sorry_in_core.py --all`, generated
Lean-view checks and the formalization-debt audit pass (`findings=5`,
`baseline=5`). `gr_assembly.py check` remains valid with scientific promotion
false. The scope regression also checks that the generic reduction has only
the two structural proposition inputs (`hAcomm`, `hGanti`) and that its
elaborated proof dependencies include the shared addition/scalar laws; the
compatibility multiplication theorem must depend on the shared multiplication
declaration. This rejects a type-shaped premise shell or a name-only wrapper.
This refactor creates no new claim or acceptance row.

### Generic transpose law applied to CAR parity symmetry (25 October 2026)

Extended `D0.Algebra.FiniteMatrixTensorProduct` with the factorwise transpose
law. The geometry namespace keeps a typed `tensorProduct_transpose`
compatibility theorem whose proof dependency is the shared algebra result.
`spatialIdMatrix_symmetric` now exposes the finite identity-factor symmetry,
and `totalParityOperator_symmetric` composes it with the existing Fock-parity
symmetry through the shared transpose law. The earlier coordinate-by-coordinate
symmetry proof is removed.

This is another finite algebra API -> concrete CAR application. It does not
change any CAR/Hodge claim status, period scope, source interpretation, or
physical conclusion.

The refreshed current inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_transpose_current_declaration_inventory_2026-10-25.json`,
SHA-256 `1842e4e2b586258aa30167955d13bbc855aefaf22d023345a682945d7b647694`.
It records snapshot `6ccfa2266cded8d4a33cffe5509700068b8994eb`,
`worktree_dirty=true`, public import `D0.All`, Lean-source digest
`e0ccf4dc8d30118bbdc0a734247988c9696f5390577a4f31958086975d95b987`,
collector SHA-256
`2508e85ff81ddc89abe8eb60617dd2a5dad8ae0bdb8d24e044416d16ec6d8ae4`, and
25 exact declarations. Its successful query built the current `D0.All` import
before reading the elaborated environment. The generic tensor API source hash
is `23f791dc17e0122ed2a98b704a280c8c4d56572197fe0dfabe918ebff2cf64c4`; the
CAR consumer hash is
`934511cf8e7b39fc7537361bd7ecea51b93b99b607adb60e7acfbc9a5e21bd0a`.
The focused CAR/Hodge cold-start regression passes and checks exact trust
footprints plus the compiled dependency chain from shared transpose law to
parity symmetry. The previous current inventory remains preserved at its
original digest and is now historical evidence.

### Diagonal CAR factor symmetries use the standard matrix theorem (25 October 2026)

The spatial identity and Fock parity matrices are definitionally diagonal.
Their symmetry proofs now expose that representation and apply Mathlib's
`Matrix.diagonal_transpose`, replacing two separate entrywise equality
arguments. The compiled dependency inventory confirms both symmetry theorems
depend on that exact library result; `totalParityOperator_symmetric` continues
to consume the shared tensor-transpose theorem and both factor symmetries.
The represented operators, carrier, period scope, and claims are unchanged.

The refreshed 25-declaration inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-25.json`,
SHA-256 `611f1f7f538d0b387c299a5428a444a7d1d8f6cc2e3dc14374e32f8aeecb1c64`.
It was collected at snapshot `ce780d53f88491f2aacc2436e80bc9bbe568853e`
with `worktree_dirty=true`, public import `D0.All`, Lean-source digest
`d719580bd7b35b7effebcfe67533e484890dd30c0911dff6780638316295cb94`,
collector SHA-256
`2508e85ff81ddc89abe8eb60617dd2a5dad8ae0bdb8d24e044416d16ec6d8ae4`, and
Lean 4.30.0. The successful inventory run built the public import before
reading its elaborated declarations. The changed CAR module SHA-256 is
`00f497a9b6175a04efba8557f97623b52657023320696af81ccc89139f7200f5`.
The CAR/Hodge cold-start regression passes against this current inventory.

### Full cold-start replay after the compiled diagonal-symmetry update (25 October 2026)

The complete bilingual cold-start runner was replayed on clean published
snapshot `5c4a630b4d66da0671b758e40bd306f5a4b1aa90`. All required sources were
found in **20/20** real cases; the **21/21** benchmark also passed its
exact-source-versus-unrelated-prose impact control. The CAR/Hodge case finds
the new 25-declaration diagonal-transpose inventory as direct content and
matches its exact SHA-256. No required source was missing.

The replay output SHA-256 is
`b0dedf47b4d3337b654c79fb81143440880904405494c2b50358fc14460ab26f`; the
runner SHA-256 is
`abe71f0a30054c8ba7e41d6a0d2e329f87d7e136e0c8f161223c9f55ae96fd5d`. The
snapshot was clean (`worktree_dirty=false`). Its seven authority inputs had
these exact digests:

| Input | SHA-256 |
|---|---|
| `02_REGISTRY/aliases.csv` | `8cda9e7ebfa26a01a04a4d51b56eb6b93425816a5fe073aa74cbae94041f672f` |
| `02_REGISTRY/assumptions.csv` | `2bc9f8c040a776d784fdbfdf62569b72e4f70ff0a182fc66d0ced31cb5f13a36` |
| `02_REGISTRY/claims.csv` | `6b19168191ad4e68e106f7b89dcd008b3ec3cabdca7b3266864f61fe64455fc8` |
| `02_REGISTRY/formal_support.csv` | `7f7a0b308745836e8747317a52079a2b644488f181f07d34c42a93817e9a321f` |
| `02_REGISTRY/gr_assembly/applications.json` | `d841fe9ccbb5e578836740b46d436147f74d9eb9c92413bbc924b942be6ee511` |
| `02_REGISTRY/gr_assembly/contract.json` | `72fb3bbbc320b4af217cbe7c09580b44556b354e9668cbd11e76933fa8209ba6` |
| `02_REGISTRY/presupposition_edges.json` | `7ff9d1e4ac3447f321afd603eab66554468644bb5fddb33551fdfa22e3e2585d` |

An independent read-only review at this head found no actionable issue in
the generic transpose theorem, its CAR compatibility/application, the two
diagonal symmetry proofs, or the inventory provenance. The review accepts
only this finite algebra/refactor slice; it does not accept a CAR claim, C0,
or any physical interpretation. The final-Ready cold-start and integration
replays remain required after the remaining task changes.

### Hostile-control coverage audit at the current proof-architecture head (25 October 2026)

On clean tree `d66fede1844a66d4e24c3e51df787167fe4f1ec6`, the four relevant
Python suites pass: proof architecture **45/45**, declaration inventory
**16/16**, gravity assembly **106/106**, and task dispatch **19/19**. The
existing tests cover the required fail-closed cases as follows:

| Failure mode | Existing controls |
|---|---|
| Missing/incorrect Lean target and stale source | `test_compiled_reuse_reports_missing_canonical_alias_target_without_compiling`; `test_result_crosswalk_stale_current_source_is_citation_only`; `test_inventory_discards_build_when_lean_sources_change` |
| Goal smuggled in as a premise or unresolved hypothesis | `test_every_hypothesis_needs_a_binding`; `test_unlisted_target_hypothesis_is_rejected`; `test_retained_assumption_prevents_closure_even_after_review`; the CAR inventory regression checks the Clifford-square theorem has exactly the two structural proposition binders |
| Carrier, action, or normalization mismatch | `test_application_cannot_switch_carrier_without_typed_edge`; `test_same_carrier_different_action_needs_transport`; `test_acceptance_is_invalidated_by_interface_or_statement_change`; `test_complete_proved_transport_can_be_accepted` checks all declared interface fields are mapped |
| Finite result or no-go inflated to a family/existence result | `test_finite_certificate_cannot_claim_uniform_family`; `test_finite_result_does_not_fill_family_premise`; `test_negative_result_cannot_fill_positive_existence`; `test_classification_cannot_be_relabelled_as_a_positive_goal` |
| Cycle or dangling proof path | `test_cycle_and_dangling_input_fail`; `test_hidden_cycle_in_hypothesis_bindings_fails` |
| False obligation closure from PASS, partial evidence, or one AND input | `test_passing_or_proposed_evidence_does_not_discharge_premise`; `test_and_dependencies_do_not_close_from_only_one_premise`; `test_acceptance_marker_cannot_be_replaced_by_arbitrary_green_receipt`; `test_self_review_is_rejected` |

The exact-source and scoping regressions also pass: changing a linked source
invalidates its declared application while unrelated prose does not, and the
real cold-start replay above found every required source. This audits the
current controls; it does not mean the full C0 package has been reviewed or
accepted. No claim status or scientific owner changed.

### Shared finite-coordinate expansion in ordinary and weighted adjoints (25 October 2026)

The repeated private proof that a finite function is the sum of its
coordinates times `Pi.single` has one canonical home now:
`D0.Algebra.FiniteCoordinateBasis.finiteCoordinate_eq_sum_single`. Its exact
scope is `[Fintype ι] [DecidableEq ι] [Semiring K]`; it depends on neither an
inner product nor a weight profile.

Both existing adjoint derivations consume this result in their actual proof
terms: `finiteHermitianPairing_adjoint` and
`finiteWeightedPairing_adjoint`. Their local duplicate `pi_eq_sum_single`
proofs were removed. The compiled proof-dependency inventory confirms both
edges. The statement and proof closures remain honest: the weighted identity
retains its sole proposition input `hw : ∀ i, w i ≠ 0`, the unweighted
identity has no proposition input, and each declaration reports exactly the
standard trust footprint `{Classical.choice, Quot.sound, propext}`.

The module is listed in `formal_support.csv` for both consumers and included
in the generated `D0.All` public import. A source-bound regression checks the
current compiled theorem types, trust footprints, proposition binders,
proof-dependency edges, and inventory source digest. The inventory uses the
existing CAR/Hodge snapshot path and contains 28 declarations: its previous
25 declaration version is preserved at commit
`4cfded11970445e0ed8efa58f5b3d2d9bd63fca1`, path
`02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-25.json`,
Git blob `37c595d9354b44ec2bb80832df287e26cf9cd103`, SHA-256
`611f1f7f538d0b387c299a5428a444a7d1d8f6cc2e3dc14374e32f8aeecb1c64`.

The refreshed 28 declaration inventory is the same file path, SHA-256
`0e71add500f8db5d4b3548d639536f68813043b9f0f9ef86c9e90d05c803e8d9`.
It records clean snapshot `3126540dc7afb80c25682a12e47c37e8ec7d062f`,
`worktree_dirty=false`, public import `D0.All`, Lean 4.30.0, Lean-source
digest `ecc3a835e2b3f285916eedd7d14f04bf8a08e89f0797940b4fc3434acc9a8a6a`,
and collector SHA-256
`5873b6dae017975ee7f5c3e20cb703ae422b18ae32c8611894b6f249d69e53a5`.
The new module SHA-256 is
`e2dd31f9bbb4e2fd29ac631cbdf4f21c61464cacfc4306e588563f74c13c5dc1`;
the two consumer source hashes are
`0481115fd1d32e571fc5bfadd1eebb880e4d07daef6f8b84841e287a2032216c` and
`f07fceb849a48657dffa8165b6570109016adfc817322605e09b27d9812712d2`.

The narrow `D0.Algebra.FiniteWeightedAdjoint` build compiled the new shared
module and both adjoint consumers (2,948 Lake jobs). Generated Lean views and
claim-map coverage pass; `tools.test_proof_architecture.py` passes **46/46**
and `tools.test_lean_declaration_inventory.py` passes **16/16**. GitHub
`guards` and `lean-build` both pass at PR head `3126540d`. An independent
read-only API review found no actionable issue in the theorem scope, consumer
dependencies, or support/import wiring.

This is a finite algebra API and reuse refactor only. It changes no claim row,
C0 disposition, application acceptance, adjoint interpretation, weight
selection, or physical status. C0 freeze and final D0.All/Ready integration
remain outstanding.

### Exhaustive book-heading source candidates for C0 reconciliation (25 October 2026)

The current locator view now enumerates every Markdown heading found in the
ten pinned top-level book sources. For each heading it records the path, line,
text, whether that source blob matches the snapshot, and claim IDs with either
an exact-heading or ranked lexical-heading candidate. The v2 view contains
674 heading coordinates: 40 with exact-heading candidates, 212 with ranked
heading candidates, 23 in both sets, and 445 with neither candidate type.

These are retrieval coordinates only. The 445 unlocated headings remain
unclassified; they are not excluded source units. Exact and ranked links do
not accept claim statements, pair multi-book rows with sections, establish
semantic coverage, change claim status, or freeze C0. The current claim view
still has 781 unresolved rows and 170 unpaired multi-book rows. No C0
disposition or owner changed.

The generated snapshot is clean at commit
`1b6f5e964f75a28b97e44e4a46346e5703b6b6c6`, schema
`d0-claim-source-candidate-view-v2`, with `worktree_dirty=false`. Its path is
`sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json`;
SHA-256 is
`2a5bd779f41d2dab918356e740ccdf243d5752b949b04b6758d791a8d19d17af`.
The collector SHA-256 is
`3e2f3e0fc64457515d458b4e655405c28dedc060bb4fe48598cb7c16f6457dd6`; the
claim-register SHA-256 is
`6b19168191ad4e68e106f7b89dcd008b3ec3cabdca7b3266864f61fe64455fc8`.
The previous v1 view remains recoverable at commit
`5182ad8a1534e4e49cce7826122f9e1c1081237e`, same path, Git blob
`aad69da53407a57b7de58aae99795924cee94cc9`, SHA-256
`218ef724270ae90c4cf88a6d6e6b10c9ccd2dde1bb841713a62d08920fbacf8d`.

The source-view regressions pass **47/47**, declaration-inventory tests
**16/16**, and claim-map coverage tests **25/25**; generated Lean views are
current. An independent read-only review found no actionable issue in the
674-coordinate enumeration, source pins, candidate counts, or unresolved
multi-book boundary. This is a source-locator checkpoint only. It does not
accept any C0 unit or replace the remaining source reconciliation and final
Ready checks.

### Shared finite linear-map coordinate action in both adjoint proofs (25 October 2026)

The pairing-independent module `D0.Algebra.FiniteCoordinateBasis` now also
owns `finiteLinearMap_apply_eq_sum_single`: for any finite coordinate space
over a semiring, each coordinate of `A x` is the finite sum of the matching
coordinate of each basis image, weighted by the corresponding coordinate of
`x`. The theorem is derived from `finiteCoordinate_eq_sum_single` and does
not assume an inner product, weight profile, or nonzero-weight condition.

The ordinary and diagonal-weighted adjoint identities now call this shared
coordinate-action theorem directly. Their duplicated local derivations of
`A x = sum_i x_i A(Pi.single i 1)` and its pointwise form are removed. The
actual adjoint statements, carriers, pairing definitions, and weight
assumptions are unchanged. The compiled dependency chain is
`finiteHermitianPairing_adjoint` and `finiteWeightedPairing_adjoint` ->
`finiteLinearMap_apply_eq_sum_single` -> `finiteCoordinate_eq_sum_single`.
The helper and both consumers retain exactly
`{Classical.choice, Quot.sound, propext}`; the weighted adjoint continues to
retain its only proposition input `hw : ∀ i, w i ≠ 0`.

The refreshed inventory remains at
`sources/d0_proof_architecture_formalization_2026-10-24/car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-25.json`.
It contains 29 declarations, was produced by compiling public import `D0.All`,
and records clean snapshot
`5818c7dbc8a630c4156ac7cdec4c98614e68f372`,
`worktree_dirty=false`, Lean 4.30.0, Lean-source digest
`61626928b804f4e4c14f2c763e9f9ef303693b44a1b320dc9277e076cf8f3743`, and
collector SHA-256
`2a41ca981b50bd5131a022d1315e5fca68b0f696651ff6b441f4f80016e434b7`.
Inventory SHA-256 is
`bc7f6ab766fea7e2dc1760335a9775feda21b85e8b412f8e1b230457e4167cf7`.
The new helper source SHA-256 is
`c4eb95a0e97acc43ef5f747f6430b83b0adbd56b8200438db9cae967f1bb0689`; the
unchanged consumers are pinned at `6acb7a145d69736801f835ed655b6e1e89c2120fc565eee0fd6130a1202c06ef` and
`a8360a1f30ce55a5320fed025d8c35cea2c9983e55d8d381c87665ef8cae87d0`.
The preceding 28-declaration inventory remains recoverable at commit
`3126540dc7afb80c25682a12e47c37e8ec7d062f`, same path, SHA-256
`0e71add500f8db5d4b3548d639536f68813043b9f0f9ef86c9e90d05c803e8d9`.

Validation passed: narrow `D0.Algebra.FiniteWeightedAdjoint` build (2,948
Lake jobs), the public-import inventory build of `D0.All`, proof-architecture
tests **47/47**, declaration-inventory tests **16/16**, ClaimMap coverage
tests **25/25**, generated Lean-view check, and EOL-aware diff check. An
independent read-only API review found no actionable scope or dependency
issue. This is reusable finite algebra only; it does not select a weight
profile or physical pairing, accept a C0 unit, or change any physical status.

The full bilingual cold-start runner on this clean published snapshot found
all required pinned sources in **20/20** real cases and passed the **21/21**
benchmark, including the exact-source versus unrelated-prose impact control.
Its output SHA-256 is
`39848e8d9170d51f3e9945c270036a1b5d4cde08ce4c10fefc9536a06ec92533`; the
runner SHA-256 is
`abe71f0a30054c8ba7e41d6a0d2e329f87d7e136e0c8f161223c9f55ae96fd5d`.

The adjoint cold-start case now includes the exact query
`finiteLinearMap_apply_eq_sum_single finite coordinate basis action` and
requires the canonical `FiniteCoordinateBasis.lean` source. On the resulting
clean published snapshot `cb5cf7d0045865a6e25bd8800eb03dba9cb64986`, the
updated runner again found all required sources in **20/20** cases and passed
the **21/21** benchmark; the new query returned the helper module as direct
content. Output SHA-256:
`87782b0df347ff9da99405b9778f53f099342d4de1ec8138a6349dca8aba18df`;
updated runner SHA-256:
`b157636922aec4ed3dc1a448513afa7db2b64f28fa15db3d52c5af579ba0434e`.
The added retrieval regression brings the proof-architecture suite to **48/48**.

### Literal claim-ID source coordinates remain retrieval candidates (25 October 2026)

The v3 book-source view supplements heading candidates with every exact,
boundary-aware occurrence of a current `claims.csv` ID in the ten top-level
book files. It records the book/path/line, zero-based half-open character
offsets, bounded source-line excerpt, nearest parsed Markdown heading, and
whether the file blob matches the snapshot. A `candidate_coordinate_key` is
emitted only for a matching pinned blob. Markdown code fences are excluded;
the same corrected closing-fence rule now drives heading parsing and the
mention scan. A literal ID can still be a citation or cross-reference, so
this coordinate is not evidence that the surrounding text proves the claim.
No claim status, owner, application edge, or C0 disposition changed.

On the clean source snapshot `5cfb97165e2b197b3671690aada0cc2341a167ac`,
the view records **833** literal mentions across **424** of the 889 claim rows
and **9** of the 10 book files. The earlier unfiltered text scan counted 837;
the four additional matches lie inside fenced code and are now omitted. The
existing heading results remain 674 coordinates: 40 with exact-heading
candidates, 212 with ranked-heading candidates, 23 in both groups, and 445
with neither. The candidate view does not classify those unlocated headings
as units or exclusions.

One useful retrieval case is
`D0-NONRECIPROCAL-ACTIVE-DYNAMICS-FORMALISM-BRIDGE-001`. Its locator still
resolves uniquely to the `BOOK_03 §03.3` heading at line 123; the literal ID
appears at line 238 under `03.3.2 The closed feedback action component` at
line 226. This exposes the exact paragraph carrying its explicit
FORMALISM/PASSPORT boundary. The current Lean declaration
`D0.Bridge.ConstrainedHamiltonianEmbeddingPassport.nonreciprocal_active_dynamics_has_formalism_bridge`
only proves `Jsymp * Jsymp = -I` for a 2×2 integer matrix. The typed result
does not prove the full feedback/action-to-constrained-Hamiltonian application
described in the book. The mention and heading are retrieval coordinates; the
application remains partial and no CORE/physical claim is promoted.

The current JSON is
`sources/d0_proof_architecture_formalization_2026-10-24/claim_source_candidates_current.json`,
schema `d0-claim-source-candidate-view-v3`, generated with
`worktree_dirty=false` at the clean snapshot above. Its SHA-256 is
`e30de22bf507c0f65f752f08b6f98c74941ff8ecd17670b4330e89f1ce083a21`; the
collector SHA-256 is
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`, and
the claim-register SHA-256 remains
`6b19168191ad4e68e106f7b89dcd008b3ec3cabdca7b3266864f61fe64455fc8`.
All **48/48** proof-architecture tests pass, including exact-token boundaries,
code-fence exclusion and snapshot-key gating. Independent read-only review
found no remaining issue in the mention mapping or its candidate-only scope.
This is a source-retrieval improvement, not semantic coverage, independent C0
acceptance, or physical closure.

### CAR/Hodge cold-start consumes the v3 claim-source view (25 October 2026)

The existing `car-scaffolds-vs-hodge-operator-claims` cold-start case now
queries and requires the v3 claim-source view. For each of the four OPEN CAR
rows—zero mode, hopping square, spectrum amplification, and heat-trace
multiplicity—the regression reads the corresponding view row and confirms:
the declared Book locator remains unresolved, there is no exact-heading
candidate, and no literal claim-ID occurrence was found in the scanned book
files. This is a bounded textual-source result; it does not establish that no
semantically relevant prose exists or accept a C0 source disposition. All four
claims remain OPEN, and the separate Hodge results keep their own carrier and
status.

The clean replay at snapshot
`4745618b020811b777acb4250761356b3b242355` found all required sources in
**20/20** cases and passed the **21/21** benchmark, including the
exact-source-versus-unrelated-prose impact control. The CAR/Hodge case now
finds **28/28** required references. Its query
`D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001 literal claim ID source candidate view`
returns `claim_source_candidates_current.json` as direct content at rank 1;
the result's source SHA-256 is
`e30de22bf507c0f65f752f08b6f98c74941ff8ecd17670b4330e89f1ce083a21`.
The compact replay record is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_4745618b.json`,
SHA-256
`ca83c1f9049ed9f1750b65d78c530bf0fd58f8351bc04b41560751501caf5dce`.
It pins cold-start runner SHA-256
`762a3664ced0012ea56810836e7cc93c556d32778f4b96e2f2ae5018fadcfef0` and
search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.

The full proof-architecture suite passes **48/48** with the new cold-start
control. An independent read-only review found no issue in the query,
candidate-only wording, or four-row status guard. This closes a retrieval
consumer for the new source view only; it does not resolve the missing
Book 06 source unit, accept a claim, freeze C0, or change any physical owner.

### Current compiled Bianchi reuse at the retrieval-tool head (25 October 2026)

The 29-declaration CAR/Hodge inventory previously recorded at snapshot
5818c7dbc8a630c4156ac7cdec4c98614e68f372 has source digest
61626928b804f4e4c14f2c763e9f9ef303693b44a1b320dc9277e076cf8f3743, which
does not match the current Windows source resolver. The same exact 29
declaration names were recollected at clean snapshot
cb5cf7d0045865a6e25bd8800eb03dba9cb64986, public import D0.All, Lean 4.30.0.
That current inventory records source digest
151ed9a7b44aa795987d2c4c2b14c5cdaa67323fd3cd15585885dcee0b0ca2d8, SHA-256
689c85a8de404cf58b1a537b183851c39d4230bf1242106b4f35b84f0d160694, and
collector SHA-256
2a41ca981b50bd5131a022d1315e5fca68b0f696651ff6b441f4f80016e434b7. All
requested declarations resolve. Later commits through c9c7448 changed
retrieval tooling and cold-start coverage but no Lean source, so this digest
remains current for the present D0.All source tree.

At the same Lean-source digest, the current proof-architecture reuse view for
D0-GRADED-BIANCHI-EXACT-001 is
d0_graded_bianchi_proof_architecture_reuse_d0_all_2026-10-25.json, SHA-256
5bd8e35810e5649a0fb2a3d5d58d20e34eebbbc7b1b0d55b63d237c7d1f354f6. Its
snapshot is 00c56c5242d2b20d1e23134886069919569b0960; the resolved literal
consumer is a theorem for every A : SceneVertex → ℚ with conclusion
d1 (d0 A) = 0. The compiled proof depends on sceneGradedComplex and the
generic D0.Topology.discrete_exact_bianchi theorem, and reports only the
standard axiom footprint {Classical.choice, Quot.sound, propext}. The
D0-HODGE-001 compiled reuse view is also refreshed at 00c56c5 and the same
Lean-source digest; its artifact SHA-256 is
2b5a0d16c1ba6ff181a44fcd008824eff502d2df1cecbb05973db75d008e59c4.

The reusable source is the coefficient-generic graded incidence complex over
a commutative semiring with Real as its compatibility default. The concrete
consumer uses the actual transposed tripartite incidence matrices over ℚ at
(p,q,r)=(8,10,12): zones (9,11,13), with 33 vertices, 359 edges, and 1,287
triangles. The registry row D0-GRADED-BIANCHI-EXACT-001 remains LEAN_PROVED
and CORE-FORMALIZED under its existing owner. This application is a discrete
cochain identity only; it supplies no Hodge/metric/dynamics/matter equation,
physical weight choice, or GR source selection.

Final integration checks at retrieval-tool head 00c56c5242d2b20d1e23134886069919569b0960 pass: the proof-architecture, declaration-inventory, generated-view, and Lean-build-helper suites report 97/97 tests; generated Lean views have stale=0; ClaimMap coverage passes; the formalization-debt audit reports findings=3 against baseline=5; gr_assembly check is valid with scientific_promotion=false; and the EOL-aware diff check is clean.

### Exact stencil-to-midpoint application for the positive nonvacuum source (25 October 2026)

Source unit key:
`8b94198c8dfbdf5983ad0b350b058fb30bb68a54:02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md#§§7.1–7.2`, blob `63c36b18af67fc1f113f9e33deb13cf43ddf4556` ([pinned source](https://github.com/gvakhrushev/d0_15/blob/8b94198c8dfbdf5983ad0b350b058fb30bb68a54/02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md)). This is one finite algebraic subresult of the existing positive example; it is not an independent claim row or an accepted C0 disposition.

`D0.Geometry.NonvacuumBrinkmannStencil` is now an explicit support root in `formal_support.csv` and is imported by generated `D0.All`. It defines the exact centered five-point transverse Laplacian, the source's harmonic quadratic/cubic family, the radial quadratic profile, the real two-component norm, and the actual finite midpoint update/forward gradient. The compiled theorems prove: (1) the displayed harmonic terms are annihilated for every nonzero mesh width; (2) the radial quadratic reads as four; (3) the combined profile reads as `-4 * coupling * energy`; (4) the forward difference of the same finite midpoint matter update equals its midpoint rate; and (5) the sourced profile's energy is exactly the squared norm of that record's forward gradient.

The key application theorem is `D0.Geometry.nonvacuumProfile_source_eq_finiteMidpointMatterNorm`. Its elaborated type retains `h ≠ 0`, and its compiled proof depends on both `transverseFivePoint_nonvacuumBrinkmannProfile_eq_source` and `twoComponentMatterNormSq_midpointGradient_eq_rate`. The owning-module inventory records all 15 declarations visible from this module: 12 source declarations and three generated `_proof_` auxiliaries, which are not separately counted as mathematical result units. The six source-level theorem declarations report axiom footprint `{Classical.choice, Quot.sound, propext}`. Inventory: `sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_brinkmann_stencil_declarations_2026-10-25.json`, SHA-256 `34d04902ab1a98b6b03f6e8bc1a401c5ce7fd9df89b2680329c7be059d2cd514`; captured at source snapshot `9274b3abedd67cdc39bd33653a878e4f87a513ae`, worktree dirty, Lean 4.30.0, source digest `b7589a9549138f5b2e4ecdf7ff1dc7d9056cec6fcbc3fcd1f9440ef51cb5053a`, collector SHA-256 `6a4fdcdaecc9ae9bc6a5f7b74d57d64ce6d2577a08aa91b267f3346cbda9b73b`. The 29-entry CAR/Hodge declaration inventory at this checkpoint was collected against this earlier Lean source digest; its SHA-256 is `6e5e059dfd3f48efa948a62e50a7c8857c4e3c69c11343be43f1d35609391162` and its snapshot remains in the branch history at `9274b3abedd67cdc39bd33653a878e4f87a513ae`. The combined post-refactor inventory is recorded below.

The same source is now discoverable by the existing `positive-nonvacuum-recovery` cold-start case through the pinned §§7.1–7.2 owner, the module itself, and the compiled declaration inventory. The full cold-start run on snapshot `9274b3abedd67cdc39bd33653a878e4f87a513ae` found all required sources in 20/20 cases and passed its 21-case benchmark; its compact report is `sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_nonvacuum.json`, SHA-256 `16368a7a3fca73dfa2bc9973d822af20e1721a90e68cb533a11a995c8b7eb850`; runner SHA-256 `7da9ed4eec1fc1f0c6a1ec217cd89e9d09bfc05ae176384e364e0d5bdbe73285`. This remains a partial application: it does not construct the original CAR operator, substitute the original 40→3→1 Cartan classification, prove all 16 coframe + 24 proper-Lorentz link + two matter Euler rows, establish the refinement estimate, or select the physical Book, clock, source, or execution. Those parent physical premises and existing scientific owners remain open.

The new module passes its narrow Lean build and the complete `D0.All` build. This checkpoint adds one exact compiled source application and its retrieval path; C0 still has no independent freeze/acceptance, and no physical claim status changes.
### Spectrum and Matter reuse the generic finite matrix tensor API (25 October 2026)

The Spectrum operators `tensor_product_I` and `kronecker_C_I` now delegate to
`D0.Algebra.finiteMatrixTensorProduct`; Matter's `kronecker_I_C` remains
available as a compatibility name and delegates to Spectrum's `1 ⊗ C`
operator. The entrywise constructor no longer requires `Fintype` instances
that its pointwise definition does not use, preserving the old public
signatures without adding a finiteness premise to callers.

The generic algebra module now also proves the finite trace identity for
`1 ⊗ B`, and `stage3_trace_relation` consumes it instead of repeating a
coordinate-level trace sum. The matrix-shift and partial-trace commutation
proofs still compile against the shared operator definitions. Narrow Lean
builds pass for `D0.Spectrum.GenerationTensorExactness`,
`D0.Matter.ArchivePartialTrace`, `D0.Geometry.ArchiveCARDirac`, and
`D0.Bridge.FinalBridgeIndex`. This consolidates finite matrix algebra only: it
changes no claim status, carrier interpretation, or physical conclusion.

The merged public `D0.All` integration build passes **4,580/4,580** Lake
jobs. The combined compiled declaration inventory at source snapshot
`472436ef795f7f6ad096eb711b8987e4d89fb13c` records **36** declarations,
including the shared operator, its trace law, the preserved Spectrum/Matter
names, and their consuming theorems. It pins Lean source digest
`a077fdd36281e539c7ec4a9dbea51cc6152268928ab1679b17b95135d3425578`, collector
SHA-256 `3c41633e10ad03c3bb0a8e440f94506a632630561697a6c44f6a76cda6155b2a`, and
inventory SHA-256
`9b0a22b100858f88ae0c215940ea9e0a515f045277633f30d7c9a3f0ba307b2b`. The
nonvacuum stencil inventory was refreshed at clean snapshot
`6c01ea00f084271116faf61e7d608b859f14f6dc`; it retains all 15 owning-module
declarations and pins the same Lean source digest, with file SHA-256
`5da75971dce0b383e151110098468c7d7aa755de9c0114918ebabd21fa1e7c80`.
The proof-architecture suite passes **50/50**, including checks of actual
elaborated signatures, dependency edges, and current source digests. Repository
validation passes with 889 claims, 31 assumptions, 58 aliases, 200 formal
support rows, and closure 932. No theorem status or scientific acceptance
boundary changed.

### Clean cold-start replay after the shared tensor API integration (25 October 2026)

The full bilingual runner completed on clean source commit
`0668f20acf507fb58bb0d8cff586cd52136fd7d8` (`worktree_dirty=false`). All
**20/20** cold-start cases found every required source, and all **21/21**
benchmark controls passed, including the exact-source versus unrelated-prose
impact regression. The CAR/Hodge case found **28/28** required references.
Its v3 claim-source query returned the candidate view as direct content at
rank 1; the existing generic CAR/Hodge algebra query returned
`D0/Algebra/FiniteMatrixTensorProduct.lean` as direct content at rank 1.

The compact replay record is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_0668f20a.json`,
SHA-256
`a6cc6abf3fafd9f5ccb837ca57d75a6aeac435fc0ca5fd49606fb067703a94fe`.
It pins runner SHA-256
`762a3664ced0012ea56810836e7cc93c556d32778f4b96e2f2ae5018fadcfef0`,
search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`, and
the updated formal-support digest
`c1bb2183581ca009694908c5b77e2632f9c4122eee2eaa1ba660ffcab80e7296`.

This validates retrieval and compiled reuse metadata on the current corpus.
It does not accept the four OPEN CAR claims, change C0, or promote any
physical interpretation.

### Delegate the shared tensor operator to Mathlib (25 October 2026)

`D0.Algebra.finiteMatrixTensorProduct` is now a stable D0 abbreviation for
Mathlib's `Matrix.kronecker`, with the same product carrier and entry formula.
The multiplication, transpose, additivity, scalar, identity, and trace laws
delegate to Mathlib's compiled Kronecker results. This removes the duplicated
entrywise constructor and its coordinate proofs while preserving the D0 API.
The CAR-specific sum-square theorem stays in the shared algebra module; the
CAR parity application now unfolds through Mathlib's `kroneckerMap_apply`.

Narrow builds pass for `D0.Algebra.FiniteMatrixTensorProduct`,
`D0.Spectrum.GenerationTensorExactness`, `D0.Matter.ArchivePartialTrace`,
`D0.Geometry.ArchiveCARDirac`, and `D0.Bridge.FinalBridgeIndex`. The final
`D0.All` integration passes **4,580/4,580** Lake jobs in 361.5 seconds.
The current 36-declaration CAR/Hodge inventory was captured at clean source
snapshot `a2b66422d255d6c617413b0450a1947e3c6652a8`; its Lean-source digest is
`3149a01a3c2641979b255aaaa699b0fcf7532ddd3a20264a23a2e2100296aa8c`, collector
SHA-256 `3c41633e10ad03c3bb0a8e440f94506a632630561697a6c44f6a76cda6155b2a`, and
inventory SHA-256 `75c6c9fe9b0342e2c9bb8516deb909ab4d2916e85c8c83bda44c2d3c4df513b7`.
The refreshed 15-declaration nonvacuum stencil inventory records clean source
snapshot `7854e3fee49965689c81da4af6eba1bdf20a3ebe` and the same Lean-source
digest; its file SHA-256 is
`b1415113ad7844e243ba5f014d6ee1a27846e4eef8f6c0b29243194087e9fed9`.

The exact trust footprint is pinned as well: direct `#print axioms` reports
`{Quot.sound}` for Mathlib's `Matrix.kronecker`, `Matrix.kroneckerMap`, and
the D0 abbreviation. The tensor definition's inventory assertion therefore
records `{Quot.sound}` rather than the empty footprint of the prior local
entrywise lambda; dependent algebraic theorems retain their recorded standard
axioms. This is the standard Mathlib dependency introduced by the API
delegation, not a project-local axiom or an admitted proof.

The focused proof-architecture and declaration-inventory suites pass **66/66**;
repository validation also passes with zero warnings on this integration.

This is finite matrix library consolidation only. The public operator names,
CAR/Matter/Spectrum theorem statements, carrier, and premise boundaries remain
unchanged; no physical interpretation or scientific status changes.

### Reuse the shared product-matrix API in the gauge flat-tensor no-go (25 October 2026)

`D0.Gauge.flatTensor` now preserves its public name as a compatibility
abbreviation for `D0.Algebra.finiteMatrixTensorProduct`; the duplicate local
entrywise constructor is removed. The shared transpose law now requires only
`[Mul R]`, since Mathlib's `kroneckerMap_transpose` is pointwise and does not
need finite index types. The existing theorem
`flat_tensor_of_two_skew_is_symmetric` keeps its original all-types scope and
proves the same conditional result through the shared transpose law and
pointwise cancellation. The naive tensor remains a no-go for the stated
nonabelian-curvature reading; this refactor adds no physical interpretation.

The Gauge target builds **2,947/2,947** jobs; the public `D0.All` build passes
**4,580/4,580** jobs in 238.3 seconds. The compiled four-declaration inventory
for `D0.Gauge.FlatTensorNoGo` has public root `D0.All`, no `sorryAx`, and pins
snapshot `fcbaac7da0fc5bd52b060d6e567f8fa644ca5b17`, Lean-source digest
`f2c3341e548000a7596cf006c8cf51a0f567d5146bf8f980568038413d39dd2c`, collector
SHA-256 `358926670c102b53cf9cec7ac88157833a32429fb28a14e7e05dbaa755232bce`, and
inventory SHA-256 `ce125769d2359f9c1fd1cdcc6f11bab55e8097b1167236a68a98c295fec88407`.
The existing 36-declaration CAR/Hodge inventory and 15-declaration nonvacuum
inventory were refreshed at the same clean snapshot and source digest; their
file SHA-256 values are `dae88318c4ac583ac91bfc7741ad7704d04a86b58a5b7338113d819db810a5f4`
and `51126147f971ee1e0ce962f5ad0cff83ea3572299daf2b65ebff982905c4898f`.
Direct axiom reporting for the refactored Gauge alias and theorem retains only
the standard `{Classical.choice, Quot.sound, propext}` footprint.
The exact query `flatTensor finiteMatrixTensorProduct` retrieves
`D0/Gauge/FlatTensorNoGo.lean` first as direct content, and a regression test
pins that rediscovery together with the elaborated API dependency and
all-types theorem signature. The proof-architecture and declaration-inventory
suites pass **67/67**; repository validation reports 889 claims, 31 assumptions,
58 aliases, 200 formal-support rows, and closure 932 with zero warnings;
generated Lean views report `stale=0`; ClaimMap coverage passes; and the
formalization-debt audit remains at five findings against its five-finding
baseline. `git diff --check` is clean.
GitHub `D0 Lean build` run 3179 and `D0 guards` run 5217 both passed on the
published code and inventory head `1630a1d92311b7490122bb3aa25f356c64d33796`;
the Draft workflows skip release-proof closure and native capsule steps.

This is a finite algebra API migration with a compatibility path. It changes no
registry claim status, source premise, or scientific acceptance boundary.

### Route source preparation through the shared matrix tensor API (25 October 2026)

`D0.Representation.SourcePortPreparation` now imports
`D0.Algebra.FiniteMatrixTensorProduct` and uses
`finiteMatrixTensorProduct` for its coupled operator, joint metric, interaction
generator, and independent-product control. The `coupled_fourth` proof consumes
the shared multiplication and identity laws. Existing public theorem names and
finite rational matrices remain intact; the D0 constructor is definitionally
Mathlib's `Matrix.kronecker`. This consolidates the operator API without
changing the model's declared scope or promoting physical availability.

The module's narrow build passed **2,956/2,956** Lake jobs. Declaration
extraction rebuilt public `D0.All` and recorded all **73** declarations at
clean source snapshot `efd8ffcf8fb6c0e0fc3303dd2d88d3ee40cf619e`, Lean source
digest `7612be00391142e8332473911e83202aefe309b5b43525d10dee622da429f75c`,
collector SHA-256 `eada9c6f24ed4cb04c4a6d5afd1d6c229296257642a11230550bd14c2ac6cd8f`,
and inventory SHA-256
`eac9c906b152765af63e48f68e32be6305a1e4d58e0236893cbbb1e23b847f94`.
The elaborated `coupled`, `jointMetric`, and `interactionGenerator` depend on
the shared D0 constructor; `coupled_fourth` depends on its multiplication and
identity theorems; the nonfactorization application consumes both the generic
independent-product control and the exact interaction witness. No declaration
in this module has `sorryAx` in its recorded footprint. Existing
`formal_support` now lists this module as a consumer of the shared API.

Because the declaration collector pins the digest of the complete Lean source
tree, the three other current inventories were refreshed together at clean
metadata snapshot `f8430243ace312c1abc0c393b465bfa6c72b1c1b`, with the same Lean
source digest above: the CAR/Hodge inventory retains 36 declarations (collector
`3c41633e10ad03c3bb0a8e440f94506a632630561697a6c44f6a76cda6155b2a`, file
SHA-256 `5007e2e3fac8e324891934e4986fe69b73c706e0fae798c6257601536f23e968`);
the Gauge inventory retains four (collector
`358926670c102b53cf9cec7ac88157833a32429fb28a14e7e05dbaa755232bce`, file
SHA-256 `f3b6eef41746ca3ef36d6d2ed8a24dfebbac6c9e35e231ee223c5570a71e5035`);
and the nonvacuum stencil inventory retains 15 (collector
`6a4fdcdaecc9ae9bc6a5f7b74d57d64ce6d2577a08aa91b267f3346cbda9b73b`, file
SHA-256 `216f950c64332c0996f4127331b75ebd03bbd351ef106fc65cab655ca0a20fb2`).
The earlier inventory blobs remain available through Git history at their
recorded snapshots.

Six targeted proof-architecture regressions pass, covering the current
CAR/Hodge and nonvacuum declaration inventories, shared coordinate and tensor
APIs, the SourcePortPreparation application, and Gauge compatibility. Repository
validation passes with 889 claims, 31 assumptions, 58 aliases, 200
formal-support rows, and closure 932 with zero warnings; generated Lean views
are current, the formalization-debt count remains five against its five-item
baseline, and `git diff --check` is clean. This is a finite algebra/library
slice. C0 freeze and independent acceptance, remaining mathematical
migrations, and the physical GR premises remain open.

### Clean cold-start replay for the source-preparation tensor slice (25 October 2026)

The full bilingual cold-start runner completed on clean snapshot
`e85c64c6e8a6f135b928679f213860c9cad5bb2f` (`worktree_dirty=false`). All
**20/20** scenarios found every required source, and the **21/21** benchmark
checks passed, including exact-source versus unrelated-prose impact. The run
used the updated `formal_support.csv` digest
`1edc5ddf0e53d46d72c7533beb0e7285dcb25b0d3cca0243d2f3d2c646899e1a`. The
compact replay record stores all authority digests, case-level results, and
required source pins at
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_e85c64c6.json`,
SHA-256 `840db313a7de8bc390c12f96a0df1597fd6ee951282c05fdbe4e8a958030df96`.
The full verbose output remains retrievable at Git commit
`88b336d3196d95e35f5646a423ea4e027e613815`, path
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_e85c64c6.json`,
blob `de4aeb7ece8f4e9c556588ee0d67d723de1d8c4d` (SHA-256
`9078db77bf2524844795e2449dd528916f784f64be7067f18360e4392e86be04`). The
runner and search engine are pinned by SHA-256
`7da9ed4eec1fc1f0c6a1ec217cd89e9d09bfc05ae176384e364e0d5bdbe73285` and
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`,
respectively. Semantic scope review remains manual.

GitHub `D0 Lean build` run **3183** and `D0 guards` run **5221** both succeeded
on `e85c64c6`. These checks and retrieval results verify this engineering
checkpoint only; they do not freeze C0, accept claim semantics, or close the
remaining mathematical, physical, and independent-review obligations.

### Generic finite partial trace and its CAR consumer (25 October 2026)

`D0.Algebra.FiniteMatrixPartialTrace` now owns the generic left-factor partial
trace. Over arbitrary finite carriers, it proves trace preservation for an
additive commutative monoid and proves that if an operator on `V × N` commutes
with `1 ⊗ C`, its partial trace over `V` commutes with `C` over any
commutative semiring. The exact algebraic premise remains visible; the theorem
does not assume a state, positivity, or a selected physical weight.

`D0.Matter.ArchivePartialTrace` keeps its existing public names and types.
`partialTraceV` delegates to the shared definition, `trace_partialTrace`
consumes the generic trace law, and `partial_trace_commutes_with_shift`
consumes the generic intertwining result. This replaces the local 50-line
coordinate derivation while preserving the CAR consumer's `ℝ` carrier and
commutation premise. The substitution is a reusable finite-matrix identity;
it accepts no claim or C0 disposition and supplies no physical interpretation.

Both narrow Lean targets pass: `D0.Algebra.FiniteMatrixPartialTrace`
**2,947/2,947** jobs and `D0.Matter.ArchivePartialTrace` **2,980/2,980** jobs.
Declaration extraction from compiled public import `D0.All` records the six
shared API/consumer declarations with no `sorryAx`. Its clean source snapshot
is `f191c30475281622bcae0901856e66f05aff8ef9`, Lean 4.30.0, source digest
`d972c29cfa1de8b86778da6e6311ef02efd370a6039b9a1cfa73f509b4bccb88`;
collector SHA-256 is
`8f19aae5e1e058bd8e3724f6a5033d405600edbc46ae35083fcd7732e6b932c5`, and the
inventory at
`sources/d0_proof_architecture_formalization_2026-10-24/finite_matrix_partial_trace_current_declarations_2026-10-25.json`
has SHA-256
`2ce47be1dcb83f5c2b475bd90cdd93dd7ee0d9451ca96a69594f03d07be36eb4`.
The compiled types retain the generic `CommSemiring R` and `1 ⊗ C` premise,
and the CAR consumer's proof depends on the shared intertwining theorem.

To keep current declaration records aligned with the whole Lean-tree digest,
the 36-declaration CAR/Hodge, four-declaration Gauge, 15-declaration
nonvacuum, and 73-declaration SourcePort inventories were refreshed at that
same clean snapshot and digest. Their file SHA-256 values, in that order, are
`634d0aa28fab39cca36903750130fa67f60f55e8093041e0aed06fc1f7bcc3ed`,
`8db6437e44434ea01280f036b4a5a6681d0d4dc9d2ca0014e81851c01688b1ac`,
`91b6413be1d4fda712d2b4970bfe5e4f6d7619cbea581bbd81acec57d0100edf`, and
`84d114e4bfe17a7d1bca9059c661d248f33825492a9cb4a2a222c79322e4cc3e`.
Their earlier blobs remain in branch history.

The full cold-start replay on the same clean source snapshot found every
required source in **20/20** cases and passed **21/21** benchmark checks,
including exact-source versus unrelated-prose impact. All **123** required
source records were found. The compact record is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_f191c304.json`,
SHA-256
`42071e0879044653d0b5f26cbf6266aaaf80167aa7634b221751ce97e9dfb417`; it binds
the updated `formal_support.csv` digest
`4520818e1940d8844ba94198f3d9107803ec63202b3f4f6dec67146237c66e94`, every
case result, each required path and its declared exact source pin where present,
and the SHA-256
`bb32739c6d1396486272e5c15cb6d94ccdc833e08525416fb53151735435fa39` of the
full replay output. The pinned runner and search engine hashes remain
`7da9ed4eec1fc1f0c6a1ec217cd89e9d09bfc05ae176384e364e0d5bdbe73285` and
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.
Semantic source classification remains manual.

The proof-architecture suite passes **54/54**, declaration-inventory tests
**16/16**, and generated-view tests **27/27**. Repository validation passes
with 889 claims, 31 assumptions, 58 aliases, 201 formal-support rows, closure
933, and zero warnings. Generated Lean views are current; formalization-debt
findings remain five against the five-finding baseline; the EOL-aware diff
check is clean. C0 freeze and independent acceptance, remaining mathematical
migrations, final Ready integration, and physical GR premises remain open.

### Partial trace factors through an exact lifted generation operator (25 October 2026)

The shared `D0.Algebra.finiteMatrixPartialTraceLeft` API now includes the
factorization
`partialTraceLeft (A ⊗ B) = Matrix.trace A • B` for a finite left carrier and
any commutative semiring. The actual type retains the `CommSemiring R`
hypothesis and does not require the retained carrier to be finite. It adds no
positivity, state, or physical-selection premise.

Two existing consumers now use this result. `D0.Spectrum.stage3_trace_relation`
derives the trace of `1 ⊗ Γ_SM` from generic partial-trace preservation and
the tensor-product factorization. `D0.Matter.partial_trace_generation_lift`
computes the full retained operator as `Fintype.card G • Γ_SM`. The existing
`generation_trace_neutrality_connection` uses that operator identity and keeps
both inputs explicit: the lift is `1 ⊗ Γ_SM`, and `trace Γ_SM = 0`. This
strengthens the consumer from a trace-only shortcut to the exact operator map;
the conclusion remains source-neutrality under those mathematical premises.

The established Matter public definitions and theorem names are unchanged.
The former spectrum proof's specialized tensor-trace call is replaced by the
shared partial-trace API. Formal support now lists both Spectrum and Matter as
consumers. The regression checks inspect compiled theorem types and proof
dependencies for the generic factorization, both applications, the retained
cardinality factor, and absence of `sorryAx`.

The three changed modules pass narrow builds: `D0.Algebra.FiniteMatrixPartialTrace`
**2,947/2,947** jobs, `D0.Spectrum.GenerationTensorExactness` **2,948/2,948**,
and `D0.Matter.ArchivePartialTrace` **2,980/2,980**. Compiled declaration
extraction through public import `D0.All` records nine partial-trace API and
consumer declarations at clean Lean-source snapshot
`05faf0c078b74ab74d963041f52749422813b7aa`, Lean 4.30.0, source digest
`ee24661fd9c5d5e5b2d78ab720422fd46eae28a5b1d786d2280a7d03b16f87f2`;
collector SHA-256 is
`41b6ae7c600534ec0142643958aca0a5d5281afa53c3863e7ec828f5caafdc6d`, and the
inventory SHA-256 is
`84e95c91481b25a66a57f0391c475c4ef6780e0b47e96e236b7a7edd16de59e8`.
The four current CAR/Hodge, Gauge, nonvacuum and SourcePort inventories were
also refreshed against that same Lean-source digest; their respective file
SHA-256 values are `cfcc5264e70fb2e707825a02fd351c51db518c468f0102956f0912664b873559`,
`9774fd2aba215b1088d19749226f55953e1e920d5af987a5aae85a11e3b5af01`,
`04276baddecb224dcf54dcc52672468f2bb13a30b356cde33deebf6a3c662dfd`, and
`4aae92f6bd7763386835024fee4bcb3cd24db9842cd7d31ccd4eee8a9f865453`.

Repository validation passes with 889 claims, 31 assumptions, 58 aliases, 201
formal-support rows and closure 933; generated Lean views remain current, and
formalization-debt findings remain five against the five-finding baseline.
The cold-start replay on clean snapshot
`cc5f4e9280493c9ab5a18143b39a006b35e1e6f5` found all required sources in
**20/20** cases and passed **21/21** benchmark checks. It found all **123**
source records and passed exact-source versus unrelated-prose impact with the
updated `formal_support.csv` SHA-256
`2684e49cdcc731a7839dc0686cd193155237de9d90188c964070c3ed3474f997`. Its
compact case-level report is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_cc5f4e92.json`,
SHA-256 `aa30a259f8607da68af1f5378feba28ee39cf60286ca2dd375d659e9a90f07c9`;
the full 6,879,199-byte replay output has SHA-256
`6a6f39955a95c35ff4d9d5287fc5523e2911cb9a34ad2d6514b4aa71cfc26846`. The
runner and search-engine hashes are
`7da9ed4eec1fc1f0c6a1ec217cd89e9d09bfc05ae176384e364e0d5bdbe73285` and
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.
The affected proof-architecture tests pass **54/54**, declaration-inventory
tests **16/16**, and generated-view tests **27/27**. Repository validation
passes with zero warnings, generated views have zero stale entries, and
formalization-debt findings remain five against the five-finding baseline.
This slice does not freeze or accept C0, change claim owners/status, select a
physical source, or close any physical GR premise.

### Cyclic archive-shift proofs reuse the transitive-permutation API (25 October 2026)

`D0.Geometry.ArchivePhaseShift` now defines its `ZMod n` archive step as an
explicit permutation and defines `archiveShiftMatrix` through the shared
`D0.Topology.shiftMatrix`. Its public right/left multiplication laws and
one-step diagonal law retain their existing names and elaborated statements,
while forwarding to `D0.Topology.shift_matrix_mul_right`,
`shift_matrix_mul_left` and `commute_with_shift_step`. The `k`-step law now
uses the generic iterate-commutation theorem together with the exact cyclic
iterate identity. A private `ArchiveTopology (ZMod n)` instance proves
single-orbit reachability from `(j - i).val`; the existing public
diagonal-constancy theorem delegates to
`abstract_shift_commute_implies_diagonal_constant`.

The concrete consumer remains `D0.Matter.density_uniform_from_commute` in
`ArchivePartialTrace`; its public interface and retained trace premise are
unchanged. `formal_support.csv` now records the direct dependency from the
shared topology module to the concrete adapter, and the cold-start case asks
for the generic theorem, its `ZMod n` specialization, and the partial-trace
consumer together. The compiled declaration regression pins the old public
statements and checks proof-term dependencies through the generic iterate and
diagonal-constancy results.

Both affected modules pass narrow builds: `D0.Geometry.ArchivePhaseShift`
**1,280/1,280** jobs and `D0.Matter.ArchivePartialTrace` **2,981/2,981**.
The result is a finite algebraic matrix statement: finiteness, a transitive
permutation and exact commutation imply constant diagonal. It does not select
a physical shift, source, state or GR realization. Compiled inventory,
cold-start replay and repository checks are pinned below.

The twelve-declaration ArchiveShift inventory and the five existing
digest-gated inventories were extracted through public import `D0.All` at
clean Lean-source snapshot `db3a201a7e8f4529e45effa4d71e578d1d0e3733`, with
Lean 4.30.0 and common source digest
`84495a35213e0664f044c79b1642f135386189a139d85b6d25b1cb0309d34b3b`. The new
inventory is
`sources/d0_proof_architecture_formalization_2026-10-24/archive_shift_topology_current_declarations_2026-10-25.json`,
SHA-256 `61380c29b71a74acfbc63b90b7e11ddfa15e2e71a5a7d29661f3075a035fce22`,
collected by tool SHA-256
`4cdcc682b0b2ff80a9646052f2e275b28e211619d9cf4dbd6058734cb7b2cd8c`. The
CAR/Hodge, partial-trace, Gauge, nonvacuum and SourcePort inventories contain
36, 9, 4, 15 and 73 declarations; their refreshed file SHA-256 values are
`1db92b9a60ab5e76f3385c30bf7f219ed95d53a942f52e1c5c77358df0be74c8`,
`1096f7df96ee7147fa367bd35fd4a250c5c02e6d9a5dc672250a0c7c9010c0bf`,
`ceaf3a0c79037fa7f15c4b8a713416b5cb00ea54dfafea4fc7fde6ab549d87b1`,
`e9582d503d838430f396f74f2bdf22025b028fcb8085a12a9a5dc5662509187d` and
`fa8fbb1a3a1d68eec05e94aa97c776e116de9bc6911910c169e84619b468d40f`.

The full cold-start replay on clean snapshot
`be64f646016706dfb6e92fea173a3b3a8cb281e7` found all required sources in
**21/21** cases and passed **22/22** benchmarks, including exact-source versus
unrelated-prose impact. It found all **126** required source records. The new
archive-shift case resolves the generic topology theorem, the concrete `ZMod n`
adapter and its partial-trace consumer with direct-content evidence. Its
compact report is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_be64f646.json`,
SHA-256 `f13c36721d4f0442ed492f4794cdc1952b6a0a6fa53caddf66287d75d967aa90`;
the full replay output SHA-256 is
`4666168f786c9d437b2180d368a1657f9cdeaf218ee33363f96efaf18987bf8a`. The
replay binds `formal_support.csv` SHA-256
`411acc91cbd78104ee85b613170ca19ebf8bb9ec2da028cc0967e963da26c9f4`, runner
SHA-256 `087f556e9280da7ce502f4f1413ce58b51405e5dee5810e9227b4b0f169d2904`
and search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.

The proof-architecture regression suite passes **56/56**, compiled declaration
inventory tests **16/16**, and generated-view tests **27/27** under the
bundled Python 3.12 runtime. `validate_repo.py` passes with 889 claims, 31
assumptions, 58 aliases, 202 formal-support rows, closure 933 and zero
warnings. Generated Lean views are current, formalization-debt findings remain
five against the five-finding baseline, and `git diff --check` is clean. No
claim owner/status, physical selector or GR closure status changed.
GitHub `D0 Lean build` run [3188](https://github.com/gvakhrushev/d0_15/actions/runs/40225497980)
and `D0 guards` run [5226](https://github.com/gvakhrushev/d0_15/actions/runs/40225498017)
both passed on published head `8c8f8a100d5784e51463a0e97a3f05594b729619`.
The execution remains on open Draft PR #402 and task lifecycle
`IN_PROGRESS`; no merge or physical-closure claim is made.

### Fin-indexed archive-shift consumers use the same topology API

The `Fin n` partial-trace path now adapts Mathlib's `finRotate` to the existing
`D0.Spectrum.cyclicShiftMatrix`, proving their matrix equality once. Its
one-step diagonal lemma delegates to
`D0.Topology.commute_with_shift_step`; the `k`-step lemma delegates to
`commute_with_shift_iterate`. The concrete `Fin n` cyclic-orbit witness is
retained as a private `ArchiveTopology` adapter, and
`partial_trace_density_uniform_under_shift` now delegates to
`abstract_shift_commute_implies_diagonal_constant`. The public lemma names and
types are unchanged, including the existing `NeZero n` scope.

`formal_support.csv` now lists `ArchivePartialTrace.lean` as a direct consumer
of `ArchiveShiftTopology.lean`. The existing archive-shift cold-start case
also queries the `Fin n` specialization, and its compiled declaration
regression checks that the old public statements depend on the generic step,
iterate and transitivity theorems. The narrow build of
`D0.Matter.ArchivePartialTrace` passes **2,981/2,981** jobs. This remains an
algebraic partial-trace result: it does not select a physical shift or close a
physical GR premise.

### Entrywise shift covariance and the lifted tensor consumer

`D0.Topology.commute_with_shift_entries` now states the full covariance
`M i j = M (f i) (f j)` from exact commutation with a permutation shift;
the existing diagonal step is its specialization. `GenerationTensorExactness`
adapts `cyclicShiftMatrix` to `finRotate` and identifies
`kronecker_C_I (cyclicShiftMatrix n)` with the shift permutation on
`Fin n × N`. This replaces the hand-expanded pair of double sums in
`flavor_blindness_step` with the generic entrywise theorem. Stronger one-step,
iterated and cross-generation results now carry only the commutation premise;
the prior `flavor_blindness_step`, `flavor_blindness_step_k` and
`stage2_flavor_blindness` statements remain as compatibility wrappers with
their original off-generation-zero premises. The partial-trace consumer uses
the shared Spectrum adapter for its matrix and iterate bridges.

The archive-shift cold-start case now resolves all three concrete consumers:
the ZMod geometry adapter, the Fin partial-trace adapter, and the lifted
generation/flavor tensor theorem. Its compiled declaration regression pins
the entrywise covariance dependency and the weaker-premise theorem. These are
finite algebraic results and do not select a physical shift or GR source.

The rebuilt 15-declaration archive-shift inventory and five refreshed
digest-gated inventories were extracted through `D0.All` at clean Lean-source
snapshot `cacb895eb20616a36043b25d0e500b9a28128ac1`, Lean 4.30.0, with common
Lean source digest
`11f1d22fac61ca5f1090ba2bad4432661ab28e5c11abe32bdda79d13c2c317cd`. The new
archive-shift inventory SHA-256 is
`c41879a8744e1c222036a50b407145fbfe4bb6547734d09199631651f104d4a3`; its
collector SHA-256 is
`e899e5510353ed5be18018d463f612c4c978e06c4af32eec55a26cd80c4908f3`. The
nonvacuum, CAR/Hodge, partial-trace, SourcePort and flat-tensor inventories
contain 15, 36, 9, 73 and 4 declarations; their SHA-256 values are
`14b024ee3ce64fe6979b8bd61e73e9355e33fb20a33933f467e53d6981356f1d`,
`4dce363ea1be68b98d56a84bf2d8a72d51a1d4a8dd6da20413e56708a04f3666`,
`79c34602ccfb8dc420564a8cc71718a58f0c74e65857eee23a68d20242091894`,
`da8cf7f2ad3d08e3bd77202525fe702bd40405ced4d664c5d9d94bc535a90ebf` and
`cd7f24fa5c9020bfbf4c86dd7e1002312c894a647dfe79b772bf038ddb483965`.

The full cold-start replay on clean snapshot
`cacb895eb20616a36043b25d0e500b9a28128ac1` found all required sources in
**21/21** cases, passed **22/22** benchmarks and found **126/126** required
source records. Its compact report is
`sources/d0_proof_architecture_formalization_2026-10-24/proof_architecture_cold_start_summary_2026-10-25_cacb895e.json`,
SHA-256 `8d5e6c71dbe64b7656d38e46206e270060f013385f2868cfcb965efd879fcbf7`;
the 6,951,679-byte full replay output SHA-256 is
`583b51911d5e39ac66f2b802f6db56c54ef82bad9a119a9f4c99bef9f2851286`. The
replay binds `formal_support.csv` SHA-256
`c0f2f9b5a68d9a15c851971f50cabc8632a7755c34fd85c3f3312bf366b212c1`, runner
SHA-256 `63b3c3d3a6b00384cc0bec3c34729478e671cd9ca1a702cfc2bbde024aff0320` and
search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.

The focused proof-architecture regression passes **56/56**, declaration
inventory tests pass **16/16**, repository validation passes with zero
warnings, generated Lean views have zero stale entries, and formalization-debt
findings remain five against the five-finding baseline. No claim status or
physical interpretation changed.

### Lifted tensor shift covariance: compiled evidence

The generalized entrywise shift covariance and its three consumers are
recorded at clean Lean-source snapshot
`1fa15d5584144813c8b2811ebeb48ba7fbccd23b`, Lean 4.30.0, with common source
digest
`aef360e0b6f96eae699c8d9f96ed448289c817327711892f23ef999ec20761a6`.
The 22-declaration ArchiveShift inventory has SHA-256
`efdff53749a0d65cad65d553e33afea48af556aef5d22f67a174dd5ddeb1f0df`; collector
SHA-256 is
`d10e1c5a6bd9ac9930968f6a5db22a94255d93374ddb4f759de6bd72f6c95386`. The
refreshed nonvacuum, CAR/Hodge, partial-trace, SourcePort and flat-tensor
inventories contain 15, 36, 9, 73 and 4 declarations and have SHA-256 values
`2c054839ba7332b9c099a57f4d0225944ce8148805a48ca837f60600d00b03a9`,
`8dde2b4c81dacf8d9bb55867b48489e66427486dd437045011a2a0387219e641`,
`dfea67d5828e37a6deab579aef04fd08c7d4f08cebc6fcc35bb13332118edf1a`,
`2fcd65a99793ed52ce92a8a72da64ac431d86dbd29f98071eab520778f20a774` and
`e99790dac9b9f32f478ded4936746049aa2f19570b0483c20b4f78d7310f153f`.

The clean-snapshot cold-start replay found every required source in **21/21**
cases, passed **22/22** benchmarks and resolved **127/127** required source
records. Its compact summary
`proof_architecture_cold_start_summary_2026-10-25_1fa15d55.json` has SHA-256
`46f64627a03c2ebd15e38215a96eb82ef9d0a6445505cc9055a9cee94ffdcb93`; the
6,966,448-byte full output has SHA-256
`9498779977407b2953a0c380c656567f7bf729c42df332bced3394c88c8256c5`. The
replay binds `formal_support.csv` SHA-256
`b538abd4bfbb919f948cbf619dbf2e24859223532e0443ece644c512d050568a`, runner
SHA-256 `1ae378b9ca27e4389f1006ca9f98424a0ae1573c7cea79c8a515ceab6e6be8b0`
and search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.

The proof-architecture regression passes **56/56**, compiled declaration
inventory tests pass **16/16**, `validate_repo.py` reports 889 claims, 31
assumptions, 58 aliases, 202 formal-support rows and zero warnings, generated
Lean views have zero stale entries, and formalization-debt findings remain
five against baseline five. The three narrow builds pass: Spectrum **2,949**,
Matter **2,981** and Geometry **1,280** jobs. This remains finite algebraic
covariance; no physical selector, claim status or GR closure changed.

### Iterated flavor blindness from commutation alone

The exact shift-commutation premise now proves the one-step, arbitrary
`k`-step and cross-generation equality of diagonal flavor blocks without an
off-generation-zero premise. The existing `flavor_blindness_step`,
`flavor_blindness_step_k` and `stage2_flavor_blindness` retain their former
argument lists and delegate to the stronger statements. The separate
`stage3_tensor_exactness` still requires off-generation-zero entries for its
independent tensor-product reconstruction step; this result does not remove
that hypothesis or claim a full tensor reconstruction from commutation alone.

The 25-declaration ArchiveShift inventory was extracted through `D0.All` at
clean snapshot `533fe58714e80d4d2026f80b3916c1dde57cc1b6`, Lean 4.30.0, with
Lean-source digest
`d66ddf0d2a669075aea355fbf1bef2807e29333f04984afcc9d83a6d38b14793`. Its
SHA-256 is
`1bf66c4227087fb06f668b180e2186196149e102684e72fd82969fddcd52fe40`; the
Spectrum source SHA-256 is
`9eae6a6503565c6302745710787cbaa68697b4ff5c7afdcecf9b25f32cae5fee`. The
other refreshed nonvacuum, CAR/Hodge, partial-trace, SourcePort and flat-tensor
inventories contain 15, 36, 9, 73 and 4 declarations and have SHA-256 values
`f1be6d4f3ad11b4287956cae4b32071f5c207faa8b1d91a3d6e19e15cd2a6241`,
`542520fe6be8a491a2b822f57026d12eb4a8d3d3976bcc8c1c35a7b87fde72c2`,
`855ae51c4c092469f16f6b9a530df39c595d041a6205f1d4b7dc76a36abc2142`,
`43011eba0c845f4c933b8bce3497c7e78deffc7c7949694149480f4f06ac17e7` and
`668cabb994f00422856565d0b477f24ca0fb86ba1850918cbd05830f5b9cf927`.
The inventory collector SHA-256 is
`d10e1c5a6bd9ac9930968f6a5db22a94255d93374ddb4f759de6bd72f6c95386`.

The cold-start replay on the same clean source snapshot found every required
source in **21/21** cases, passed **22/22** benchmarks and resolved **127/127**
required source records. Its fifth archive-shift query directly finds the
iterated and cross-generation result in `GenerationTensorExactness.lean`. The
compact summary
`proof_architecture_cold_start_summary_2026-10-25_533fe587.json` has SHA-256
`873ffa66376d96e1261a715bf97f4725df4b0705fea8fa7740074a6b4dca77cd`; the
6,991,605-byte replay output has SHA-256
`535481a84924ec2fea1b5b311d9fe845846ab5eeed5c6ea5b9366da172dd6c1e`. It
binds `formal_support.csv` SHA-256
`b538abd4bfbb919f948cbf619dbf2e24859223532e0443ece644c512d050568a`, runner
SHA-256 `63f2b140a1d0c3127aa27a5cb47ee5059a186f1466e1840d038a17769edb8824`
and search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.

The Spectrum narrow build passed **2,949/2,949** jobs; the dependent Matter
partial-trace build passed **2,981/2,981**. Proof-architecture tests pass
**56/56**, declaration-inventory tests **16/16**, repository validation has
zero warnings, generated Lean views have zero stale entries, and formalization
debt remains five findings against baseline five. This strengthens only the
finite algebraic theorem and its explicit application scope; it changes no
physical selector, claim status or GR conclusion.

### Strong covariance theorem is consumed by tensor reconstruction

`stage3_tensor_exactness` now calls
`stage2_flavor_blindness_of_commute` directly to transport the diagonal block
from its anchor generation. Its public theorem still carries the original
off-generation-zero premise because `stage1_tensor_exactness` separately uses
that fact to reconstruct the full tensor product. The compiled dependency
inventory confirms both facts at once: the strong commutation-only theorem is
the diagonal transport dependency, while the stronger theorem's consumer
still exposes the exact independent off-block premise.

The refreshed 26-declaration ArchiveShift inventory is pinned to clean source
snapshot `5be41d7cb83e0a7dbeaa55491d8a8fcc99dce1fd`, Lean 4.30.0, source digest
`81857a8868b81cfa73e3b85503fc17f5a476e12c9a9820b1eea590b970602b81`, and
SHA-256 `36c4cc30e2a31d4509d2b1e1665a65b3c9d5faf3f2ee52298fedadb24449e8ab`.
The current Spectrum source SHA-256 is
`2ec8fd610bff3a09f0f67a6e1ec43f313cddf2db2ac6ad520e2a6d96e5cfc36c`. The
other refreshed nonvacuum, CAR/Hodge, partial-trace, SourcePort and flat-tensor
inventories contain 15, 36, 9, 73 and 4 declarations and have SHA-256 values
`5e3f1ac45faf503c18439a26dd2af87ce1025e3c33534c240d4d229c9d81d36f`,
`182ee417061895e2afce3bca5dca61cedf7d988ca30b7aab4f683fb676954c08`,
`bcbcf40298a7126b619f2093118f8f8572e2e58e40f8514d92db9bbcb8bb249f`,
`8682ced8d10122ea30280055195c211cef2960fcd9dc02a16e736dea2a98650c` and
`f3fdc6aa8d5b381f3f9b5c2f4e2fe2a99b17f77ad409774818eecdc38d41b7ac`.
The inventory collector SHA-256 remains
`d10e1c5a6bd9ac9930968f6a5db22a94255d93374ddb4f759de6bd72f6c95386`.

The cold-start replay on this clean snapshot found every required source in
**21/21** cases, passed **22/22** benchmarks and resolved **127/127** required
source records. The updated query finds `GenerationTensorExactness.lean` as its
top direct-content candidate. Its compact report
`proof_architecture_cold_start_summary_2026-10-25_5be41d7c.json` has SHA-256
`060c4a131ff652fed23971052055f30757e01491121c66edfa5d199e64b1c437`; the
6,991,517-byte full output has SHA-256
`4335f6433c40892a0b29f36263df6853a2b789e19c8cdf9706d06ceb9a368299`. It
binds `formal_support.csv` SHA-256
`b538abd4bfbb919f948cbf619dbf2e24859223532e0443ece644c512d050568a`, runner
SHA-256 `67362b36a94a7ec338af265637ce814c482199ab9b2c682fd7b906750e40daf9`
and search-engine SHA-256
`aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262`.

The Spectrum narrow build passed **2,949/2,949** jobs and the dependent Matter
partial-trace build passed **2,981/2,981**. Proof-architecture tests pass
**56/56**, declaration-inventory tests **16/16**, repository validation reports
zero warnings, generated Lean views have zero stale entries, and debt remains
five findings against baseline five. This is a checked mathematical reuse
improvement; it does not remove the physical-source or GR-selection premises.

### Candidate C0 source-unit reconciliation: nonlinear J² metric tangent (25 October 2026)

This crosswalk separates two adjacent units in the pinned J² bridge instead of
treating them as one statement. The immutable source is
`77d3ab6059bd1a3ce48637b97b9f30aa8825fc5f:02_REGISTRY/research/MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md`,
blob SHA-256 `ce56193edac787640840921310d265e5ebb5a0bd4d628414109dacaa6836b7bc`:

1. Section A, line 16, states that the selected nondegenerate star-action
   quotient has the nonlinear carrier `Q = ΘηΘᵀ`.
2. Section B, line 48, states the flat detector tangent
   `DQ_flat[H] = Hη + ηHᵀ` and the symmetric-direction convention
   `H(q) = qη/2`, giving the first-order coefficient `q`.

The original Lean pin is retained as historical provenance:
`4aff58affff315eae09572640166b90cb0e5bdde`,
`03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean`, SHA-256
`6234a6480aad6ca2a78caa3a64f59def4c50dc38beeb3c8ab1cc3df94c6db3cb`.
It proved the finite Role-indexed solder-Gram symmetric tangent, but did not
encode the source convention or its map to `Q`.

The subsequent vertical slice adds the shared
`D0.Algebra.finiteGram_one_smul_expand` API and uses it in the current
`D0.Geometry.A4DSolderMetricCompletion` source adapter. The exact source path
`Q(1+tH) = (1+tH)η(1+tH)ᵀ` expands with linear term `Hη+ηHᵀ` and retains the
quadratic remainder. For `H(q)=qη/2`, the Lean theorem proves the linear
coefficient is `q` and the exact difference quotient is `q+tR`. The adapter
maps the source frame to the existing solder carrier by `Θ' = Θη`; the
identity `ηηηᵀ=η` proves this right multiplication preserves the finite Gram
matrix. `j2DetectorMetricPath_symmetric_solder_adapter` supplies an explicit
coframe whose existing readout is `q` and whose nonlinear solder-Gram path
equals the source path.

The added theorem `j2DetectorMetricPath_hasFDerivAt_direction` proves, for
every matrix direction `H`, that the scalar path `t ↦ Q(1+tH)` has derivative
`Hη + ηHᵀ` at `t=0`. Its symmetric-direction corollary proves the pinned `q`
derivative for `H(q)=qη/2`. The proof locally equips the finite Role matrices
with the explicit nested sup norm needed for `HasFDerivAt`. This is a Fréchet
derivative of each real-parameter path; it is not a full Fréchet derivative
of the matrix-valued map as a function of its matrix argument. The exact
quadratic remainder and difference-quotient theorem remain available
alongside the derivative result.

The current geometry source is pinned at commit
`051c30ea5e5a02db2816fb5e5cebe5ea63938910`, SHA-256
`7293a532763ff09418bb2b42690e3753c8c2e22a92faf5e09ec8b1af48135f74`.
The shared Gram API remains pinned at `150c34ad0ff1a1f4eb0edfb06363d7d6bfa45bab`,
SHA-256 `26864e383f68dc793907ae14d07982c967346459500aad92d057cfa81c13f900`.
The targeted `D0.Geometry.A4DSolderMetricCompletion` build passed
**3,087/3,087** jobs. The `metric-provenance` record splits source A and B and
pins the current declarations without changing its owner or outcome. The
generated `02_REGISTRY/gr_assembly/SYNTHESIS.md` view is derived from that
record; the assembly README and shared dispatcher were not modified.

The fresh clean `D0.All` crosswalk snapshot is
`2e5038da397e1027c4b760456efede546630a7df`, with Lean-source digest
`a8fe81dbc2537b936bc0beef34ecd7c4b8efe8d8cea7a61980e4ac3ed3c7a0d9` and
`applications.json` SHA-256
`e38c5d4deba94bba6ff72f4bdf0b22caa2a81330250dd7c9ca599a54ddfed8e4`.
Both source sections are verified but remain candidate section locators
requiring review. All nine requested explicit Lean declaration locators
resolve in the compiled environment. The compact recorded crosswalk is
`sources/d0_proof_architecture_formalization_2026-10-24/metric_provenance_crosswalk_2026-10-25_2e5038da.json`,
SHA-256 `fbb13fe71fc5b4cd99c42a3c366eee8ab4be95918cedf11850f68066313b4b71`.
The semantic relation remains unresolved, claim locators remain unresolved,
and `acceptance_inferred=false`.

This formalizes a finite matrix bridge for source B. It does not formalize the
selected finite action's quotient provenance in source A, its nondegeneracy
sector, global connection elimination, physical metric/source selection, or
independent C0 acceptance. The two source units remain candidates; no claim
status or physical interpretation changes.

### Full matrix-variable Fréchet derivative of the finite J² metric (26 October 2026)

The geometry module now proves the map-level statement
`HasFDerivAt j2DetectorMetricPath j2DetectorMetricPath_tangent 0`, where
`j2DetectorMetricPath H = (1+H)η(1+H)ᵀ`. Both the matrix variable and the
codomain use the Frobenius norm. The pinned tangent is an explicit continuous
linear map, and `j2DetectorMetricPath_tangent_apply` proves its action is
`Hη + ηHᵀ`; the transpose isometry used by that map also has an explicit
application lemma. This supplements the already-proved scalar path derivatives
and exact quadratic remainder with a Fréchet derivative of the matrix-valued
map itself.

The geometry source is pinned at commit
`5057775c28a3ff04fe827aed883debf90d8bccb9`, SHA-256
`04d2ac86ae3c91f771a29171ea328297615fa31443c9954294e1a27314bf58ff`.
The shared `D0.Algebra.finiteGram_one_smul_expand` API remains pinned at
`150c34ad0ff1a1f4eb0edfb06363d7d6bfa45bab`, SHA-256
`26864e383f68dc793907ae14d07982c967346459500aad92d057cfa81c13f900`.
The targeted `D0.Geometry.A4DSolderMetricCompletion` build passed
**3,087/3,087** jobs, and the crosswalk's full `D0.All` build completed
successfully. The clean crosswalk snapshot is
`fcf89ad048992d71a89bc838a0eb10921db5707e`, Lean-source digest
`c333de44ffd644df0fb3ffbd8bfbe59e6b65e903359c40427d38022396f564a2`, and
`applications.json` SHA-256
`8c752a9ff8f2e48a81030d5306606172526601570857a6271e3a4fc6ac122fef`.
All twelve requested explicit Lean declaration locators resolve in the
compiled environment. The compact crosswalk is
`sources/d0_proof_architecture_formalization_2026-10-24/metric_provenance_crosswalk_2026-10-26_fcf89ad0.json`,
SHA-256 `1d347faf34489d7bd5fc7fe059a8e5bd0c676665c49f0a8b0d52ff6f88254937`.
Both source sections remain candidate locators requiring review; the semantic
relation and claim locators remain unresolved, and `acceptance_inferred=false`.

This closes only the finite matrix calculus step for source B. It does not
connect source A's selected-action quotient to the Lean carrier, establish
physical metric/source selection or global connection elimination, or grant
independent C0 acceptance. No claim status or physical interpretation changes.
