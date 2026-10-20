# D0 / M1 — CORRECTION: PROSPECTIVE D_MIN SELECTS A PHYSICAL HISTORY BEFORE EXECUTION; IT DOES NOT COMPRESS AN ALREADY EXECUTED HISTORY

**20 October 2026. FOUNDATIONAL STRATEGIC CORRECTION, integrated in the same ongoing Draft scientific PR #334.** This memo explicitly supersedes the mistaken physical interpretation of the older 2-step-versus-8-step original Q8 comparison. Existing original formal theorems about ACTUALLY EXECUTED history cost, memory and clock are valid in their original scope, but they DO NOT refute a PROSPECTIVE principle which selects a MINIMUM-COST feasible history BEFORE it occurs. \`GR_closed=false\`.

## 0. The user's critique was right about the temporal ordering

The earlier analysis mistakenly treated D_min primarily as a post-hoc compression function on an already registered physical path. That does not address the user's proposed fundamental *dynamics*:

\[
\boxed{
\gamma_{\rm actually\ selected}
\in
\arg\min_{\gamma\in\mathcal H_{\rm physically\ admissible}
                 (\sigma_0,\mathcal B,\mathcal Q)}
 S_{\rm COMPLETE\ native}[\gamma],
}\tag{1}
\]
where \(\sigma_0\) is the COMPLETE initial physical state (including the true momenta, old/right history, controller, clock, archive and reference), \(\mathcal B\) is the SAME physical boundary/goal, and \(\mathcal Q\) is the SAME required set of admissible independent future verifications. The full price includes primitive ActionProtocol Cost, original Book Info, retained path-order/history/source, preparation, observer/reference, controller, failed records and clock/work. Minimizing only space length or number of letters is NOT automatically minimizing this full price.

If an alternative \(\gamma_A\) is truly admissible from the SAME FULL \(\sigma_0\), satisfies the SAME \(\mathcal B,\mathcal Q\), and has \(\mathcal S(\gamma_A)<\mathcal S(\gamma_B)\), then a prospective minimization law cannot select \(\gamma_B\). This is a fact about choices BEFORE execution and not a permission to rewrite the past after the long history occurred.

The sharp audit of the original TOME I §2.2 finds its explicit \`D_min\` definition refers to the SHORTEST **DESCRIPTION** among explanations preserving the same distinguishability. The original formal \`ActionProtocol\` only bounds actual nonidentity transition cost from below. **Neither theorem yet proves (1) is compulsory physical law**, especially not with full Book03 H+J+R net source or CAR matter. Deriving (1) from foundational M1/D_min/actual endogenous Price rather than ADDING IT as an independent physical axiom is now a NAMED important bridging theorem. Its premises must never be hidden inside an apparently automatic "physics always shortest" slogan.

## 1. NEW COMPILED prospective finite dynamical law and Bellman consistency

New Lean owner attached DIRECTLY to
\`03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean\`:
- \`ProspectiveDynamics\`: actual full State, available native Action, \`step\`, \`allowed\`, state-dependent \`price\`;
- \`run\`, \`totalPrice\`, \`executable\` and exact APPEND/COMPOSITION laws;
- \`ProspectiveExecution\`: explicitly typed PRE-EXECUTION selected chronological path, feasible same end-goal and an OPTIMALITY PREMISE;
- \`reject_strictly_dominated\`: cannot select a history with a cheaper FULLY feasible alternative of the SAME goal and full initial state;
- \`optimal_suffix\`: Bellman principle-of-optimality for all suffixes after a common prefix, using the complete endogenous state and additive executed price;
- \`no_positive_redundant_detour\`: a truly avoidable strictly positive-Cost excursion that returns to the EXACT SAME COMPLETE future-relevant state is IMPOSSIBLE inside such an optimal selected history.

This is a genuine formal dynamic-programming/no-waste theorem from the NAMED prospective-selection assumption. It does not prove the original M1/Book03 HAS that assumption. The correctness of the Bellman replacement depends on complete state-dependent admissibility and additive price; the original raw Book H+J+R logarithmic partition, quantum interference and full archived history may require state enlargement or a separately proved time-consistency lemma before the hypothesis applies literally.

**Important logical detail:** "same spatial position" is NOT "same physical state". An outward initial momentum, angular momentum around a black hole, a planned future destination, or environmental interactions can make a nominally shorter geometrical route IMPOSSIBLE from the same full initial state or more expensive in genuine full action. A free particle with nonzero outward initial velocity can first move away and subsequently return under gravity without any third attracting object; this is not a stochastic violation of deterministic laws. D_min must compare genuinely permissible programmes under COMPLETE initial conditions and actual field-source selection, not an arbitrary observer's choice of a geometrical route.

## 2. The native Q8 correction is even sharper than the user's 2-vs-8 objection

On the ALREADY OWNED original quaternion alphabet \(I:=\mathrm{localIQ}, J:=\mathrm{commonJQ}\) and Golden-\(p\) comparator:

**Task A — only implement the relative sign \(R=\operatorname{diag}(I_4,-I_4)\).** The original two-step \(\gamma_2=(I,I)\) already implements \(R\), and no zero/one-gate native word does. The pre-existing eight-step \(\gamma_8=(I,J,I,I,I,J,J,J)\) ALSO implements R, but is NOT the minimum implementation for this restricted goal. For a canonical cost of one per source-changing original primitive and no extra differential Info/preparation constraints, prospective D_min selects \(\gamma_2\) before it happens. Our old assertion "the eight-step history already happened, thus cannot be replaced" was irrelevant to this physical **selection** question. The old theorem remains a correctly scoped audit of COST IN AN ACTUALLY EXECUTED \(\gamma_8\), not the law requiring it to happen.

**Task B — actually test noncommutativity/chronological order with two words containing IDENTICAL primitive counts.** Even the old eight-step contrast against the grouped eight-step word is unnecessary for the same Golden two-port TASK. There is a shorter native matched-inventory assay:
\[
\boxed{
\begin{aligned}
\gamma_{\rm dark}&=(I,J,I),&
U(\gamma_{\rm dark})&=J,\\
\gamma_{\rm bright}&=(J,I,I),&
U(\gamma_{\rm bright})&=R\,J.
\end{aligned}}\tag{2}
\]
Both have EXACTLY TWO local-i and ONE common-j operations (three steps), but their actual original coherent Golden response is:
\[
\boxed{
P_{\rm bright}(\gamma_{\rm dark})=0,\qquad
P_{\rm bright}(\gamma_{\rm bright})=4p^3,\quad p=\varphi^{-1}.
}\tag{3}
\]
This is VERIFIED on all four quaternion-reference basis states using the actual ORIGINAL 8×8 integer matrices and actual original Golden two-port splitter, no new gate or angle. **Exhaustive enumeration of ALL 0/1/2-step ORIGINAL gate words and all their equal-inventory classes** establishes that NONE of them yields an order-sensitive Golden port contrast. Therefore the MINIMUM for this precise task/allowed alphabet/comparator is **three gates**, not eight. New compiled Lean original-owner \`nativeQ8MinimalReferenceWord\`, \`nativeQ8MinimalOrderWord\`, \`nativeQ8ThreeWordSamePrimitiveInventory\`, \`nativeQ8ThreeGateIJIEqualsCommonJ\`, \`nativeQ8ThreeGateJIIEqualsRelativeCommonJ\`, \`nativeQ8ThreeGateDistinctSourceOperators\` certify the group identities; the full native Golden port and minimality checks are separately independently replayed JS (48 PASS groups).

This is a CONSTRUCTIVE ACTUAL PROSPECTIVE-MDL SCIENTIFIC UPGRADE, not merely an adjustment to words. It reduces the nominal order-verification primitive programme to three original Q8 actions in this fixed task, and shows why even a perfectly legitimate historical eight-step demonstration need not be called the required fundamental generating law.

**Task C — independently verify one ALREADY RETAINED eight-step Book historical provenance record.** If the actual goal explicitly includes reproducing the eight-tick timestamp, individual intermediate witness records, or its whole physical price, the two-step implementation has different output history and is NOT the same task. The existing original \`FiniteProtocolClock\` records 2 versus 8 and the original actual \`ActionProtocol\` can price those distinct histories differently. This is why the retrospective-history theorems remain valid and USEFUL, but are not an objection to prospective minimum selection in Task A or B.

## 3. Rule rather than coin flip: keep the EXACT distinction between dynamics and measurements

A deterministic prospective choice of a complete PROGRAMME/rule does not by itself eliminate all possible quantum measurement outcomes. The already-owned Golden Born law has strictly positive bright and dark probabilities in its Q8-ordered branch. To claim that an original underlying D0 law selects ONE concrete measurement history rather than a probability distribution requires a separate endogenous source/preparation/hidden-archive derivation reproducing those native Born statistics. Neither "the world minimizes an MDL description" nor a primitive ActionProtocol inequality supplies that theorem automatically. Deterministic field trajectories with fixed full initial data and stochastic detector outcomes are conceptually different levels.

Similarly the physical GR geodesic variational principle is usually STATIONARITY of an appropriate action/proper-time functional subject to causal and boundary constraints, not a claim that every atom always travels the Euclidean spatial shortest-distance path. If a minimum principle is to force GR rather than simply fit it, D0 must derive the precise correct PHYSICAL functional and admissible constraint class, including cases where the extremum is a maximum or a saddle.

## 4. The real next non-circular D0→Einstein forcing theorem

The corrected project chain is:
\[
\boxed{
\begin{gathered}
\mathrm{M1\ independent\ verification}\\
\Downarrow\\
D_{\min}\text{ (shortest indistinguishable DESCRIPTION)}\\
\text{\bf ?}\\
\Downarrow\\
\text{Prospective physical selection of MINIMAL admissible}\\
\text{COMPLETE Cost−Info/clock/archive history}\\
\Downarrow\\
\text{Bellman/time consistency on future-complete D0 state}\\
\Downarrow\\
\text{Original selected finite Euler + CAR matter}\\
\Downarrow\\
\text{Einstein limit on the same refining physical carrier}.
\end{gathered}}\tag{4}
\]

The **question-mark step** is the TRUE next fundamental proof burden. It is not solved by the logic of compressing syntactically equivalent theories, nor by the mathematical construction of a retrospective paid-history price. However the fully compiled prospective finite theorem shows exactly the dynamical meaning of the user's principle if it can be derived. The original Q8 exhaustive test shows how a newly cheaper PROSPECTIVE verifier can be constructed from literal original gates.

### Falsifiable physical statement

On ONE genuine complete originally admissible M1/G0 carrier, find two histories with SAME true full starting state and same admissible final testing goal. Compute ALL actual paid Book03 H+J+R Cost−Info/clock/prep/outcomes, including allowed future-testing constraints. If physical evolution selects the strictly more expensive history while an exactly allowed strictly cheaper alternative exists, the *proposed prospective MDL physical law* fails. If the apparent detour is explained by omitted initial momentum, another interaction, a future verification requirement, or the wrong partial Cost definition, this does NOT contradict MDL; it instead identifies the missing native state/constraint or price component.

No extra invisible "third attractor" should be posited without evidence. Hidden conditions are possible, but not guaranteed; the whole input state and execution law must make them testable.


## 4B. The idle-history test: positive Cost alone would SELECT the empty physical history

The original quantum ActionProtocol assigns strictly positive price to each truly distinguishable transition, but the EMPTY history has zero executed primitive action Cost. Therefore a PROSPECTIVE physical minimizer with no required new test or other terminal constraint and ALL strictly positive primitive transition prices chooses NOTHING, not a falling apple. This is the key missing endogenous FORCE needed for the user's D_min to be an actual dynamics rather than a description preference.

**NEW COMPILED Lean:** ProspectiveDynamics.totalPrice_nonneg, ProspectiveExecution.no_motion_without_a_required_distinction and ProspectiveExecution.nonempty_forces_unsatisfied_initial_goal prove:

\[
\boxed{
\operatorname{goal}(\sigma_0)=\mathrm{true},\quad
c(\sigma,a)>0\;\forall(\sigma,a)
\ \Longrightarrow\ 
\gamma_{\min}=[].
}\tag{5}
\]

Consequently a nonempty selected history requires an initially UNSATISFIED genuine mandatory future verification/physical task, or a FULL native Cost-minus-Info source which makes empty nonoptimal. Neither is automatically supplied by the primitive Cost quantum alone. The missing physics theorem must DERIVE the obligatory test/goal/endogenous source from M1, and derive prospective minimization of actually selected Book03 complete Cost-Info from D_min's existing shorter-description principle. Do not invent the destination or a fitted gravitational coefficient.

The black-hole atom example confirms the importance of COMPLETE initial state: outward radial velocity and inward radial gravity naturally produce outward-then-inward motion even without a third attractor. An immediately inward trajectory with different initial momentum is NOT a feasible alternative at the same state. Geometric spatial path length also need not be the true Einstein/Palatini variational action. All comparisons must hold source momentum, interactions, boundary and permitted future tests fixed.

This is an exact semantic/dynamical forcing boundary, not a claim the original M1 has already proved selection. GR_closed=false.

## 5. Implemented in the SAME repo; previous negative controls kept but scope-corrected

The prior compiled original \`original_roundtrip_no_endpoint_only_paid_action\`, \`nativeQ8CanonicalActionCannotFactorThroughEndpoint\` and \`nativeQ8SameEndBookSecondSourceGap\` are mathematically sound as *retrospective price/provenance statements for executions which ACTUALLY occur*. They **DO NOT** imply the prospective physical minimal selector ever chooses those overlong executions. This is now an explicit correction to their prior interpretative framing. Do not promote an action-ambiguity theorem as a no-go against prospective MDL.

New compiled Lean \`ProspectiveExecution\` + Bellman/no-detour theorems in \`EndogenousActionQuantum.lean\`, and exact native \`IJI\) vs \`JII\` Q8 3-gate theorems in \`OrderMemoryControl.lean\`. New strengthened existing native JS \`check_original_q8_forward_comparator_autonomous_program.mjs\` exhausts all native gate words up to length2 and tests the three-gate exact Golden probabilities across all four quaternion basis states. Both are integrated on original #334 branch without touching BOOK/CORE/claims or inventing a physical GR action.

**GR_closed=false**: the abstract prospective selector remains a named dynamical selection PREMISE pending derivation from original M1/D_min and complete Book03 Cost–Info. The user-corrected temporal ordering (selection BEFORE history) is binding on all future interpretation of this research.
