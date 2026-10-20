# D0 — generic finite-program interpretation and theorem transfer

**Task:** `WRK-A4D-LEAN-FOUNDATION-THEORY-TRANSFER`
**Phase:** interpretation and generic transfer
**Primary consumer:** `theory_transfer`, interface `theory-transfer-v1`
**Formal owner:** `03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean`
**Input baseline:** main `dff7498b9071ad4d9fd1580b80829d91eb55f534`

## Exact result

Let `F` and `G` be the existing `FutureExecution` systems. An interpretation
contains a state map `i`, a finite native program `c(a)` for each source
primitive, a test map `j`, and an injective outcome encoding `e`. Its primitive
requirements are exactly

\[
i(F_a(s))=\operatorname{run}_G(c(a),i(s)),\qquad
\operatorname{read}_G(i(s),j(t))=e(\operatorname{read}_F(s,t)).
\]

All-finite-word execution/readout commutation, future equivalence and theorem
preservation are not fields of that structure. The module derives them from
these maps and the declared scope below. Physical history labels, paid steps
and clock duration still require their own realization maps.

For a word `w=[a₁,…,aₙ]`, define `c(w)=c(a₁)++…++c(aₙ)`. Induction proves

\[
i(\operatorname{run}_F(w,s))=\operatorname{run}_G(c(w),i(s)),
\]

and consequently every compiled future experiment has exactly its encoded
source outcome. Compilation preserves concatenation. Composing two
interpretations compiles each intermediate word through the second
interpretation; `comp_compile` proves the resulting equality on every word.
Identity interpretation compiles each source primitive to itself.

## The common empirical carrier is constructed

The interpreted common execution has the **full native state type**, source
action labels implemented by their native programs, source test labels
implemented by their native tests, and native outcomes. The original `G`
still has all of its additional actions and tests.

On this explicitly declared common execution:

\[
\operatorname{profile}_{G|I}(i(s))=
\operatorname{profile}_{G|I}(i(t))
\quad\Longleftrightarrow\quad
\operatorname{profile}_F(s)=\operatorname{profile}_F(t).
\]

The reverse implication uses primitive/run/readout commutation; reflection
uses injectivity of the outcome encoding. Thus the raw state map descends to
an **injective map of future empirical quotients**. Its image is recorded as
an explicit subtype, producing a constructed equivalence

\[
F/{\sim_F}\;\simeq\;
\operatorname{image}\bigl(F/{\sim_F}\to(G|I)/{\sim_{G|I}}\bigr).
\]

The image is closed under the interpreted source actions. Its action diagram
commutes with the source quotient action (`futureMap_step`,
`imageEquiv_step`). Neither surjectivity onto all native states nor raw state
injectivity is assumed. An interpretation is therefore free to remove an
actually unobservable redundant coordinate, but cannot remove a distinction
present in the common future experiments.

The foundation module supplies `futureClassEquivEmpirical`, identifying this
same future quotient with the existing empirical-theory quotient.
`verifiedStateImageEquiv` composes that proved map with the supplied
`TheoryVerification` representation and the new image equivalence. The
verified foundation and theorem transfer therefore use one identified
empirical carrier.

This composition is checked on the actual state and run maps:
`verifiedStateImageEquiv_representedState` sends the foundation's represented
state of `s` to the common image of its future class. For every finite word,
`verifiedRun_image` identifies the represented foundation run with the
native class of `run_G(c(w),i(s))`. Thus the composed interface uses the
existing foundation's execution, rather than a separately chosen state map.

## What is transferred, and how the proof is reused

An assertion is any predicate on a future empirical class. This includes
arbitrary parameterized assertions invariant under the declared empirical
equivalence. Assertions about extra unobserved microscopic coordinates need
an enlarged observable interface before this theorem can apply to them.

For a source predicate `P` and a native common-image class `n`, the translated
predicate is

\[
(I_*P)(n)=P(E_I^{-1}(n)),
\]

where `E_I` is the equivalence **proved above**. Translation preserves
conjunction, negation, implication and externally indexed universal
quantification. Action-dependent assertions use the same commuting image
action, as stated by `translate_after_step`.

The observation meaning is proved explicitly by
`translate_future_observation`. The translated source assertion
`quotientProfile_F(x,w,t)=o` is equivalent to the **actual** common native
quotient readout at the same word and mapped test equalling `e(o)`. This
follows from all-word/readout commutation and outcome injectivity, connecting
predicate transport directly to measured outcomes.

The existing `M1Universality.DescSystem` is instantiated as assertions with
semantic entailment under a declared regime `H`:

\[
\operatorname{derivable}_H(P)\;:=\;
\forall x,\ H(x)\Rightarrow P(x).
\]

`assertionFaithful` **derives** its preservation/reflection field from the
constructed equivalence; it does not accept `iff_derivable` as a premise.
`transfer_theorem` then invokes the already owned
`faithful_preserves_derivable` theorem with an actual source Lean proof.
There is no need to repeat the proof of `H ⇒ P` inside the native description.

`transfer_from_premises` takes an arbitrary indexed premise family `Aᵢ`, the
source theorem `(∀i,Aᵢ) ⇒ P`, and proofs of every translated premise at the
native class. It produces the translated conclusion. Every imported premise
remains either a proved input or an explicit regime hypothesis.

This is a semantic theorem interface checked by Lean. It does not claim to
implement the parser, inference rules or soundness theorem of an arbitrary
external proof language. A physical application must first represent that
theory's objects and assertions on this operational carrier.

## Additional native tests remain load-bearing

Mapped source experiments need not exhaust the actual native system. For a
stronger statement about **all** native future experiments, the optional
`NativeContextCoverage` witness supplies, for each native word/test pair, a
source future context and an outcome postprocessing map valid on every
represented source state. The witness gives a concrete test translation,
not an assumption of future-equivalence preservation.

With this witness, `NativeContextCoverage.native_profile_eq_iff` proves
preservation and reflection for the original full native future profiles.
Without it, only the declared common-sector theorem has been established.

The exact finite control uses the same two-bit state `(visible,hidden)` and
identity actions in both systems. The source reads `visible`; the native
system additionally reads `hidden`. Every required primitive and mapped
readout diagram commutes. Nevertheless `(false,false)` and `(false,true)`
have equal **all-source future profiles** and different native profiles.
`extra_native_test_prevents_coverage` proves that no coverage witness exists.
Hence restricting the common test family cannot silently establish a claim
about every native observable or its physical source contribution.

A positive family uses the already owned `uncoupledCenter` construction:
projection of its unobservable Boolean coordinate is an interpretation on
every `FutureExecution F`, and all native contexts are covered using the
existing `uncoupledCenter_run` theorem. This demonstrates that raw-state
injectivity is correctly absent from the transfer assumptions.

## Application to the registered obligation

| Required part of `theory-transfer-v1` | Formal construction |
|---|---|
| States and finite native programs | `Interpretation`, `compile`, `run_commutes` |
| Tests and outcomes | `observe_commutes`, `profile_commutes` |
| Composition | `compile_append`, `comp`, `comp_compile`, `identity_compile` |
| Preserve and reflect empirical distinctions on the common sector | `common_profile_eq_iff`, `futureMap_injective`, `imageEquiv` |
| Foundation on the same carrier | `verifiedStateImageEquiv`, `verifiedStateImageEquiv_representedState`, `verifiedRun_image` |
| Imported assertions and proofs with explicit premises | `assertionFaithful`, `transfer_theorem`, `transfer_from_premises` |
| Actual meaning of translated observations | `translate_future_observation` |
| Interpreted dynamics | `futureMap_step`, `imageEquiv_step`, `translate_after_step` |
| Additional native tests | `NativeContextCoverage`, `native_profile_eq_iff`, `extra_native_test_prevents_coverage` |

This supplies the generic conditional transfer used by
`gr_operational_realization`. Its later physical interpretation must supply
the actual admitted state/action/readout maps and retain its clocks, full
Cost−Info, source, variations, units and refinement estimates. No finite
program-length identity selects a physical action or calibrates time.
No Einstein equation or physical optimum occurs among the premises or
conclusions of this module.

## Validation boundary

The formal owner is submitted for narrow compilation followed by the task's
single final Lean closure and independent frozen-input review. Compilation
and accepted application evidence are recorded by the integrator in the
task's primary composition artifact; this note itself is not an acceptance
or a claim that a physical realization has been constructed.
