# D0 verification foundation and operational theory transfer

**Task:** `WRK-A4D-LEAN-FOUNDATION-THEORY-TRANSFER`
**Execution:** [PR #386](https://github.com/gvakhrushev/d0_15/pull/386)
**Scientific input baseline:** `dff7498b9071ad4d9fd1580b80829d91eb55f534`
**Phase:** composed verification kernel and generic conditional theory transfer.

This result supplies two previously missing applications in the existing
argument. The exact scientific acceptance is recorded in
[`applications.json`](../gr_assembly/applications.json); this note describes
the proof and its physical boundary. The original foundation owners,
`positive_gr` target and ongoing native research remain unchanged.

## 1. Exact parent substitutions

| Parent obligation | New formal owner | Substituted mathematical interface |
|---|---|---|
| `verification_core` on `verification-core-v1` | [`VerificationCore.lean`](../../03_FORMALIZATION/D0/Foundation/VerificationCore.lean) | The existing verification representation, record, comparison and future-process quotient are composed on one carrier, with explicit Book Sigma witnesses. |
| `theory_transfer` on `theory-transfer-v1` | [`TheoryTransfer.lean`](../../03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean) | Primitive operational interpretation produces finite-program composition, a faithful common empirical image and reuse of existing implication proofs. |

The detailed proof maps are in the
[foundation note](D0_VERIFICATION_CORE_COMPOSITION_2026_10_20.md) and
[transfer note](D0_THEORY_TRANSFER_2026_10_20.md). The common-carrier bridge is
proved inside the transfer module; these are not two unrelated certificates.

The prior owners consumed at the input baseline are
`VerifiabilityNecessity`, `EmpiricalTheoryFactorization`, `FutureExecution`
and `M1Universality`. Their existing statements and proof bodies are reused.
The code interface follows Book 01, sections 01.1.2 and 01.1.4, with every
finite-coding and algorithmic premise exposed.

## 2. One record kernel for every admitted future

Let `F` be an existing `FutureExecution` and let `E` be a supplied
`TheoryVerification F.futureEmpiricalTheory`. Write

\[
\Phi_F(s)(w,t)=\operatorname{observe}_F(\operatorname{run}_F(w,s),t).
\]

The module constructs an equivalence between the owned future quotient and
the empirical-theory quotient. Transporting the same verified protocol
through that equivalence defines a represented state `rho(s)`, its actual
protocol record `r(s)`, its original comparator and the represented actions.
The main identity is

\[
\boxed{r(s)=r(t)\quad\Longleftrightarrow\quad\Phi_F(s)=\Phi_F(t).}
\]

This is `representedRecord_eq_iff`. It derives the exact kernel of the same
record map from the existing record-injectivity theorem and the constructed
quotient equivalence. For every finite word,

\[
\widehat{\operatorname{run}}(w,\rho(s))
 =\rho(\operatorname{run}_F(w,s)).
\]

`representedComparison_iff` identifies every correct line's Boolean answer
with inequality of these complete future profiles.
`representedComparison_catalogue_independent` preserves the original
catalogue/line invariance. `verification_core` composes these statements with
the owned forced-functional-tuple and no-catalogue-outsourcing result on the
same `E` and `F`.

The retained-memory theorem now has an actual consumer:
`sufficient_memory_preserves_record` proves that any memory sufficient for
the future profile is sufficient for this represented record. The existing
hidden-bit example still requires distinct records although the current
readout agrees. An entirely uncoupled coordinate produces the same record.
Both controls are specialized through the new record map without repeating
their original proofs.

## 3. The coded Sigma roles and their algorithms

`SigmaWitness E` supplies a finite ordered, primitively coded alphabet and a
code presentation of

\[
P.\mathrm{State}\;\sqcup\;
 (P.\mathrm{State}\times P.\mathrm{Line}).
\]

The tags keep state facts and registered state-plus-line facts in one code
universe. Round trips, the shortlex-minimal representative and genuine
Mathlib `Computable` witnesses for canonicalization and comparison are
explicit inputs of this coded realization.

The module constructs `D_min`, comparison, chronological retained archive,
prefix frames and positional access. It proves:

\[
D_{\min}(s)=D_{\min}(t)\iff\Phi_F(s)=\Phi_F(t),
\]

\[
\operatorname{archiveCode}(s,l)=\operatorname{archiveCode}(t,l')
\iff\Phi_F(s)=\Phi_F(t)\land l=l'.
\]

`query_computable` proves actual algorithmic access to stored codes.
`query_archive` and `query_append_retains` identify the retrieved entry and
prove that appending later entries preserves earlier readable entries.
The supplied canonicalization/comparison hypotheses are retained in
`coded_verification_core`; they are not inferred from a semantic quotient.

`finiteSigmaWitness` additionally constructs a nonempty coded interface for
every supplied finite verified-state and line presentation. Each tagged
object has one valid singleton code; canonicalization is the identity and
comparison is primitive recursive. This construction establishes consistency
of the coded interface. It does not select a physical alphabet, derive an
encoder for arbitrary infinite future profiles, or identify code length with
physical action or duration.

## 4. From primitive interpretation to all finite executions

For two existing execution systems `F` and `G`, an `Interpretation F G`
supplies four maps: state `i`, action-to-native-word `c`, test `j` and
injective outcome encoding `e`. Its only operational equations are

\[
i(F_a(s))=\operatorname{run}_G(c(a),i(s)),\qquad
\operatorname{read}_G(i(s),j(t))=e(\operatorname{read}_F(s,t)).
\]

The module derives, by finite-word induction,

\[
\boxed{i(\operatorname{run}_F(w,s))
 =\operatorname{run}_G(c(w),i(s)),}
\]

and the corresponding outcome equation. Compilation respects concatenation
and composition of two interpretations. No complete-execution or
theorem-preservation field is assumed in `Interpretation`.

The common execution keeps the full native state type and uses the compiled
source actions and mapped source tests. On its explicit empirical image,

\[
\Phi_{G|I}(i(s))=\Phi_{G|I}(i(t))
\quad\Longleftrightarrow\quad\Phi_F(s)=\Phi_F(t).
\]

This constructs an equivalence from the source future quotient onto that
image. The image is closed under interpreted source actions. Raw-state
injectivity and surjectivity onto every native state are not required.

The final composition uses the foundation's actual maps:
`verifiedStateImageEquiv_representedState` identifies its represented state,
and `verifiedRun_image` sends its represented finite run to the class of
the actual native run `G.run (I.compile w) (I.stateMap s)`.

## 5. Existing proofs now have a precise transfer rule

Assertions are predicates on future empirical classes. The constructed
equivalence transports those predicates, preserving conjunction, negation,
implication, indexed universal quantification and interpreted action.
`assertionFaithful` proves the existing `M1Universality.Faithful` interface;
its final derivability equivalence is a conclusion of the construction.

`transfer_theorem` reuses the existing `faithful_preserves_derivable` owner:

\[
\bigl(\forall x,\ H(x)\Rightarrow P(x)\bigr)
\Longrightarrow
\bigl(\forall y\in\operatorname{image}(I),\
 I_*H(y)\Rightarrow I_*P(y)\bigr).
\]

`transfer_from_premises` accepts an arbitrary indexed premise family and a
proof of every translated premise. The imported source proof is reused;
none of its hypotheses disappears. The proof interface is Lean-checked
semantic entailment under an explicit regime, not a parser or soundness
theorem for every external formal language.

`translate_future_observation` anchors this translation in actual readout:
the translated assertion that the source future observation is `o` is
equivalent to the common native quotient readout being `e(o)`. Thus the
transferred observational assertion has the same measurement meaning as
the already proved execution diagram.

The original native system retains every extra operation and test. An
optional `NativeContextCoverage` supplies the translation of each such
experiment; only then is full-native future equivalence concluded. A
two-bit Lean counterexample proves why that extra input is necessary: the
source reads the first bit, the native system also reads the second, and all
common primitive diagrams commute while the full native profiles differ.

## 6. Application scope and immutable acceptance

The two existing obligation statements, interface definitions, outcome and
family scope stay unchanged. Their previously textual quantified domains
receive named hypothesis keys for the existing assembly mechanism:

| Scoped target | Named domain conditions |
|---|---|
| `verification_core` | The declared execution interface; its supplied `TheoryVerification`; explicit code/algorithm witnesses whenever the coded realization is used. |
| `theory_transfer` | Primitive operational interpretation and injective outcomes; the same verification representation where used; semantic assertions with source proofs and explicit regime premises; coverage only for the optional all-native upgrade. |

These conditions were already required by the original target text. The
independent application review must compare them to that text and reject any
new premise that would weaken the original conclusion. No chosen physical
price, native admission, Einstein equation or prospective optimum is inserted
as a closed target hypothesis.

The active-result budget is explicitly raised from 52 to 54 solely for these
two distinct architectural proof owners. Existing entries and their source
provenance remain. This is a bounded contract change, not permission to add
unbounded supporting results. Each new result has a direct consuming
application; the source hashes, complete hypothesis maps and independent
acceptance markers are recorded in the existing assembly files.

## 7. Next physical substitution: one admitted process and complete price

The next consumer is `gr_operational_realization`. It must supply the actual
native states, admitted operations, preparations, records, complete action,
source, genuine variations, clocks and refinement maps on the same family
used by `positive_gr`. The generic theorem now gives the transport once those
physical inputs are proved. It does not construct them by encoding equations.

The ongoing `constitutive`/`native_sector` work remains with its existing
owner, [PR #334](https://github.com/gvakhrushev/d0_15/pull/334). Its exact
native law and full Cost-Info must determine the continuation and source.
The already owned `ProspectiveExecution.optimal` remains a premise until that
native derivation supplies it or the precise native variational law required
by the physical application.

One useful distinction for that work follows directly from the pinned
[all327 source](https://github.com/gvakhrushev/d0_15/blob/bf82fb54c63bbe95aee5e459a30f17a27f576519/02_REGISTRY/research/A4D_GLOBAL_327_BOOK_FISHER_CAR16_MAGNETIC_WICK_AND_DARK_REVIVAL_2026_10_20.md):
zero oriented current does not imply an idle process. For positive symmetric
`B`, `Br=rho*r`, positive normalized `r`, define

\[
P_{uv}=\frac{B_{uv}r_v}{\rho r_u},\qquad
\pi_u=r_u^2,\qquad
\mu_{uv}=\pi_uP_{uv}=\frac{B_{uv}r_ur_v}{\rho}.
\]

Then `sum_v P_uv=1`, `sum_uv mu_uv=1` and `mu_uv=mu_vu`. Every
antisymmetric oriented current has zero mean, although one completed step
is counted by the normalization. If the separately supplied physical edge
cost satisfies `C_uv>=1`, its mean is at least one. The normalization
conditions the ensemble on a step; it does not prove that a physical step
must occur. Graph-edge inequality alone also does not prove that its actual
verified physical states differ.

Consequently the next missing input is actual activity/clock/admission and
the complete paid price, not a universal assumption of nonzero oriented
current. This sharpens the existing native question without creating a new
execution or claiming a native selection result.

## 8. Validation and execution provenance

The new modules are compiled narrowly with the pinned Lean 4.30.0 toolchain
and the repository's source-change guard. The finite witness, direct readout
bridge and extra-native-test obstruction are part of those compiled modules.
The final integration imports both through generated `D0.All`; its build and
the independent pinned application reviews are the completion gates.

The initial Draft was opened before either proof module existed. Its opening
guard correctly rejected the bundled queue/brief registration because an
initial WORKER Draft permits only the lifecycle changes of an already
registered task. [CONTROL PR #387](https://github.com/gvakhrushev/d0_15/pull/387)
places the unchanged registration on main before the scientific PR is made
Ready. The failed opening run remains visible; no gate, task class or
scientific requirement is weakened to bypass it.
