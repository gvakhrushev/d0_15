# D0 M1 → D_min → FUTURE-CONTEXT ARCHIVE: a canonical minimal generator, finite computable closure, and exact original Q8/Spin memory bound

**20 October 2026. New fundamental formal theorem + exact bounded finite certificate; scientific integration in existing Draft #334.** This document integrates rather than replaces the original D0 Tome I \(D_{\min}\), [Book 00 M1 contract](../../01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md), original Book03 retained histories, currently compiled binary generator [PopperianBootstrap.lean](../../03_FORMALIZATION/D0/Foundation/PopperianBootstrap.lean), actual [EmpiricalTheoryFactorization.lean](../../03_FORMALIZATION/D0/Foundation/EmpiricalTheoryFactorization.lean), and the already-owned [original 327 native Q8/Spin sheet + 960 compatibility gates](A4D_Q8_SPIN_SHEET_327_TRIANGLE_INVERSE_AND_960_COHERENCE_GATES_2026_10_20.md). No independent physical dynamics or new primitive is postulated. **GR_closed=false.**

## 1. Correct the logical object of MDL: a MINIMAL PROGRAMME OF GENERATORS, not a count of all later hardware

The central user's objection was right in its stated scope. The original \`fin3Protocol\` shows only that hardware with three witness LINE labels is possible and not type-isomorphic to the two-line \`boolProtocol\`; it does not show that THREE primitive independent witness generators are necessary. The already compiled \`killingTest_has_minimal_binary_generator\` gives for ANY original exact \`KillingTest P\` a proper 2-line retract:
- use two ACTUAL different original line labels, not a fictitious new apparatus;
- restrict \`Record\` to its actual generated image;
- retain ALL original verified outcomes over EVERY catalogue;
- choose any other original witness pair without changing the public verification result;
- a one-line projection violates the CURRENT exact independent-witness contract.

This is an EXACT theorem about a contract ALREADY containing two source labels. It does NOT independently derive the PHYSICAL causal independence of two apparatuses or strictly charge the third's actual work. Strict primitive MDL needs positive marginal cost (or a proven strict minimum description comparison). Three truly different later detectors can still be GENERATED from the core and must be paid/archived if actually executed. Distinct THREE functional semantic roles \((\mathrm{distinction,retention,comparison})\) are not three checking lines or three K(9,11,13) scene zones.

**The missing point in the previous step:** Reducing based solely on the CURRENT verdict could mistakenly discard a hidden-but-retained state which affects some future admitted observation. That would violate the original M1/MDL demand to preserve reproducible distinctions. The proper object is the **smallest future-complete quotient**.

## 2. NEW COMPILED Lean source: take ALL ORIGINAL future actions BEFORE quotienting the record

Let an arbitrary original deterministic execution interface have retained states \(S\), allowed primitive actions \(A\), test choices \(T\), observable results \(O\), state step \(\delta:A\times S\to S\), and record readout \(r:S\times T\to O\). No physical information on \(S\) is presupposed except its supplied actions/tests. Form the already-generated finite word monoid \(A^\ast\), without a foreign list of future measurements.

For every original state \(s\), its full **future observational profile** is
\[
\boxed{
\mathrm{Prof}(s)(w,t)
=r(\delta_w(s),t),\qquad
w\in A^\ast,\ t\in T.
}\tag{1}
\]
The fundamental MINIMAL generated operational equivalence is
\[
\boxed{
s\sim_{\infty} s'
\quad\Longleftrightarrow\quad
\forall w\in A^\ast,\ \forall t\in T,\ 
\mathrm{Prof}(s)(w,t)=\mathrm{Prof}(s')(w,t).
}\tag{2}
\]

**Exact theorem A — automatic right congruence.** For EVERY ORIGINAL allowed action \(a\in A\),
\[
s\sim_\infty s'\ \Longrightarrow\
\delta_a(s)\sim_\infty\delta_a(s').
\]
*Proof:* any later word \(w\) after \(a\) is the ALREADY LEGAL original word \(a::w\) starting from the original state. No compatibility of the current readout with \(\delta_a\) is postulated. The future quotient has a well-defined induced native transition for EVERY allowed action.

**Exact theorem B — greatest observation-stable identification.** If ANY candidate relation \(R\subseteq S^2\) preserves the current readout on related states AND is preserved by EVERY allowed native action, then \(R\subseteq\sim_\infty\), by induction on the actual finite action words. Thus \(\sim_\infty\) is the COARSEST sound identification (largest relation) that does not break the original complete test/action execution. This is more informative than defining a quotient after assuming an ad hoc \`pullTest\` for the instantaneous readout: the completion GENERATED all pullbacks by word prefixing.

**Exact theorem C — universal minimal sufficient memory.** The evaluation map
\[
S/{\sim_\infty}\ \hookrightarrow\ O^{A^\ast\times T}
\]
is INJECTIVE. Any original memory \(\mathrm{encode}:S\to M\) with a decoder reproducing the WHOLE profile for every original state cannot identify states in DIFFERENT \(\sim_\infty\)-classes. For finite memory, the resulting conditional capacity lower bound is
\[
\boxed{|M|\ge |S/{\sim_\infty}|,\qquad
\operatorname{bits}(M)\ge
\left\lceil\log_2|S/{\sim_\infty}|\right\rceil.}\tag{3}
\]
The quotient achieves the exact minimum of distinguishable states (not necessarily the minimum PHYSICAL number of gates or Joules). The original EmpiricalTheoryFactorization theorem applies to the explicitly generated future theory whose \`Test\` is \(A^\ast\times T\); each actual action produces the correct \`OperationalProcess.pullTest\` by \(w\mapsto a::w\).

**Formal Lean owners appended to the pre-existing source \`D0.Foundation.EmpiricalTheoryFactorization\`:**
\`FutureExecution\`, \`FutureExecution.run\`, \`profile\`, \`profile_step\`, \`futureSetoid\`, \`FutureClass\`, \`profile_step_congr\`, \`quotientStep\`, \`quotientStep_mk\`, \`quotientProfile\`, \`quotientProfile_injective\`, \`sufficient_memory_reflects_future\`, \`largest_observation_stable_relation\`, \`futureEmpiricalTheory\`, \`asOperationalProcess\`. These compile in actual D0 Lean build and guards at checkpoint \`210f22bdb7bd23ca2cf3fa00f06a212e43b4d252\`. The separately compiled source \`D0.Foundation.PopperianBootstrap.binary_core_preserves_all_shared_action_histories\` proves the earlier TWO ORIGINAL independent line retract continues to give exactly the same public verdict after ANY finite word of the SAME actual shared state operations. **Important:** if a third line supplies a NEW physical action, deleting it changes \(A\) and its future test family, so this theorem cannot justify that deletion.

## 3. A real NEGATIVE control: a presently invisible ARCHIVE bit is FORCED by one future test

A compact exact experiment is owned as \`hiddenBitExecution\`. Its actual physical-type retained state is \((v,h)\in\{0,1\}^2\): current visible record \(v\), hidden archived history \(h\). Current readout sees only \(v\). The actual allowed future action \(\delta_1(v,h)=(h,h)\) copies retained history into the visible detector.

Thus
\[
\mathrm{read}(0,0)=\mathrm{read}(0,1)=0,\qquad
\mathrm{read}(\delta_1(0,0))=0,\quad
\mathrm{read}(\delta_1(0,1))=1.
\]
The instantaneous readout quotient has TWO distinct recorded classes, but the FULL future-context quotient has EXACTLY FOUR; any correct predictive archive must retain TWO independent binary bits. Deleting the hidden bit is NOT MDL, it destroys a possible future falsification. Original compiled Lean theorem \`hiddenBit_minimum_future_memory_four\` proves the literal lower bound \(|M|\ge4\) for ANY finite future-sufficient encoder; the proof is not just based on counting toy labels.

**Scope:** this toy \`FutureExecution.State\` includes microscopic retained variables NOT perfectly distinguishable by the present detector and is intentionally weaker than the perfect original \`VerificationContract\` on ALL raw states. It is a model of a physical detector PROJECTION of future-accessible memory, not a counterexample to the already proven \`VerificationContract.record_injective\` on its own verified state carrier.

## 4. NEW finite MDL theorem: no actual need for an UNBOUNDED catalogue of all future test words

For any genuinely finite deterministic native process with \(n\) recorded states, \(m\) allowed actual actions, and an ACTUAL current readout partition containing \(k\) classes, define the endogenous Moore refinement:
\[
P_0(s)=\mathrm{current\ output\ signature}(s),\quad
P_{d+1}(s)=
\bigl(P_d(s),P_d(\delta_{a_1}(s)),\ldots,
P_d(\delta_{a_m}(s))\bigr)_{\text{equal-key quotient}}.
\tag{4}
\]
At each stage \(P_d\) remembers exactly the observed outcomes after all actual action words of length at most \(d\). It REFines the previous partition. If one refinement changes no partition blocks, the induced actions already preserve those equivalence classes, so the partition is forever stable by induction; it equals \(\sim_\infty\). Every STRICT refinement increases the number of classes by at least one, and there cannot be more than \(n\).

Thus the algorithm TERMINATES after at most \(n-k\) strict refinements. If \(k=1\), all current outputs are identical on the ENTIRE state space and remain identical at ALL later deterministic step states, so the partition is stable immediately. In any nontrivial actually measurable case \(k\ge2\):
\[
\boxed{\text{full future-MDL memory computed by at most }n-2\text{ refinements}.}\tag{5}
\]
This bound is SHARP: the actual native-type unilateral chain \(s\mapsto\min(s+1,n-1)\), readout \(\mathbf1_{s=n-1}\), makes exactly \(n-2\) refinements before the states are all distinguished. **This is an ordinary mathematical finite partition argument; the new Lean owner proves the all-future quotient and its universal property, while this particular numerical n-k termination bound is recorded with its direct elementary proof and executable finite regression, not advertised as an additional compiled Lean theorem.**

Independent no-dependency JS regression [finite future-MDL partition/minimization](sources/d0_mdl_binary_generator_2026-10-20/check_finite_future_contextual_mdl_partition.mjs) EXHAUSTS **ALL** original abstract Boolean-output deterministic processes for:
- 2 states, 2 allowed primitive actions: 64 machines;
- 3 states, 2 actions: 5832 machines;
- 4 states, 1 action: 4096 machines.

For each one it compares full bounded future-word signatures with the refinement quotient, verifies the n−k bound and produces exact sharp examples n=3 through n=12. Original 2-bit Lean negative example is replayed. 16 PASS groups; 9992 fully enumerated finite systems, not a physically forced arbitrary transition algebra.

This is a legitimate M1 advantage: a FINITE observer can determine the exact future quotient of a KNOWN FINITE test/dynamics process in finitely many INTERNAL generated steps, without an oracle over infinitely many outside tests. The exact step bound applies to the number of ACTUAL finite states, not automatically to the 33 vertices of K(9,11,13) when a retained Golden/Book/Spin archive enlarges its true state space.

## 5. MOST IMPORTANT D0 physics consumer: original Q8 Spin center shows exactly what MDL must NOT throw away

The already-owned original [327 Q8 Spin triangle sheet and 960 octahedral consistency theorem](A4D_Q8_SPIN_SHEET_327_TRIANGLE_INVERSE_AND_960_COHERENCE_GATES_2026_10_20.md) provides a NONTOY decisive example of the same logical difference.

On the TRUE K(9,11,13) scene there are **359** original unoriented edges and **32** nontrivial vertex-central \(\mathbb Z_2\) Spin gauge transformations. For a FIXED underlying original SO link connection the relative Spin lifts modulo vertex gauge therefore have
\[
\boxed{\#\text{classes}=2^{359-32}=\mathbf{2^{327}}.}\tag{6}
\]
The original SO/vector/exterior-CAR16 positive Golden probabilities are IDENTICAL for all these central sign choices: the original Q8 central \(z=-1\) projects to SO identity and acts trivially on CAR16 exterior vector representation. That is a rigorous whole-present-detector blindness, not an infinitesimal rank failure. Its group-algebra witness \(e_-=([1]-[z])/2\ne0\) is annihilated by exterior SO/CAR16 but acts as identity on a faithful spinor doublet.

Yet ORIGINAL three-tick ABC retained Book memory already contains all **1287** oriented triangle sheet labels, and their \(\mathbb F_2\) boundary matrix has EXACT rank327. Exactly 327 independent basis labels reconstruct all359 edge sheet choices modulo32 vertex gauges, while exactly 960 independent original eight-triangle octahedral constraints prevent inconsistent fake records.

**The conditional minimum-memory theorem now follows immediately from future-MDL, not a guess about apparatus capacity:**

- If the physically admitted future test family contains a faithful set of spin-sensitive Q8 central comparison experiments that distinguish all \(2^{327}\) relative Spin sheets, then EVERY future-sufficient binary archive needs **at least 327 bits**, and the ACTUAL 327 independent original triangle basis syndromes achieve the bound. The 960 additional triangle checks are CONSTRAINTS/verification redundancy, NOT 960 new independent bits.
- Still only TWO independent exact witness lines are necessary to verify any given native spin-sheet verdict under the original fault-free verification contract. A third correct line brings NO new fundamental witness generating role; it may be a later paid/fault-tolerant replica.
- If literal original fullStep/G0 does NOT admit a spin-sensitive future test, the central sign remains unobservable even under its actual allowed SO/exterior operations, and the Q8 sheet may be quotiented by the observational theory without violating THAT narrower future contract. Full genuine spinor matter claims would then require a NEW proven native admission rather than a verbal assertion.

This produces the sharp new D0 distinction:
\[
\boxed{
N_{\rm primitive\ verifier\ lines}^{\min}=2,\qquad
\operatorname{bits}_{\rm future\ Q8\ history}^{\min}=327\
\text{ IF genuine future spin tests are admitted}.
}\tag{7}
\]
No conflation with the previously owned **685 continuous scalar Book martingale archive directions**: those are a different tangent/cost carrier, not 685 binary Q8 sheets or 327 automatically independent physical fermion fields.

**Independent full ORIGINAL graph computational consumption:** [native Q8 future-MDL 327 sheet checker](sources/d0_mdl_binary_generator_2026-10-20/check_native_q8_future_archive_mdl_327.mjs) reconstructs all359 genuine edge central bits modulo actual32 rooted gauge, computes the actual \(\mathbb F_2\) rank327 from all1287 REAL ABC triangle boundary rows, verifies all960 original cube/octagon parity constraints, reconstructs all1287 after 143+104+80 original passes, checks an adversarial changed Spin signal violates consistency, and exhibits independent detectability of EACH of327 basis sheet bits by future Spin tests. 13 PASS groups. The underlying 327/960 structural theorem is independently owned elsewhere in the SAME PR and is consumed here, not falsely presented as newly forced by bare Boolean M1.

## 6. Physical falsification agenda — one sharp transition instead of a new rank search

**Current existing evidence / bounded result**: 2 original witness lines are enough for the given exact verification contract; complete future-MDL quotient is canonical and dynamics-compatible; finite generated-process MDL is computable without an external test catalogue; for actual original Q8 central sheets the minimum future archive is EXACTLY327 bits under a named Spin-test admission. Every theorem now has an actual compiling Lean owner or fully replayed finite certificate, plus a strong HOSTILE negative control.

**Named remaining physical premise**: The registered native \`GoldenCoherentMemory.fullStep\` presently acts on a 4-dimensional two-qubit \`Fin4\` matrix and has NO typed Q8/scene/Spin center input, as independently audited by the native Q8 owner. It therefore does NOT, by its signature alone, prove the physical spin-sensitive future test required by (7). More generally the strong \`KillingTest\` already postulates two correct registered line labels; its causal physical independence and genuinely positive native marginal work are still unresolved. A physically actual test family must be selected from the ORIGINAL G0/Book03 allowed programme, not silently extended with all imaginable operations.

**Critical D0→GR consequence**: The previous obligation "prove ONE RAW hardware carrier is universally unique" is unnecessarily strong as a goal for M1, and the old Fin3 counterexample applies only to THAT raw uniqueness. The correct demanding goal is:
\[
\text{original M1 verification}
\ \to\ D_{\min}(\text{complete ADMITTED future testing})
\ \to\ \text{minimal faithful archive}
\ \to\ \text{original H+J+R fully paid dynamics}
\ \to\ \text{actual 16+24+matter Einstein source}.
\]
The current work rigorously establishes the FUTURE-MDL quotient and scoped 2-line generator/Spin memory consequences. It does **not** prove an actual physically compelled Golden programme generates its own spin test family, original Q8 CAR spinorial matter, unique Cost-versus-Info/clock selector, or full GR/RAW216/refinement. **GR_closed=false.** The remaining test is now a typed physical admission/paid-work premise that can be killed by inspecting actual G0 signatures, not another unconstrained numerical fit.
