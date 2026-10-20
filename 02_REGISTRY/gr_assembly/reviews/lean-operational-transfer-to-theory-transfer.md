# Independent review: operational finite-program theorem transfer

Assembly-Acceptance: lean-operational-transfer-to-theory-transfer 0230078042b9861d8a3599d32ceea20452eba9e945260507c4c0dd325d46fd2a

Decision: ACCEPT for `theory_transfer` on `theory-transfer-v1`, retaining the
`verification_core` prerequisite and the original conditional common-sector
scope.

Reviewer: Codex CONTROL independent reviewer
(`native_selection_synthesis`, 2026-10-20).
Result owner: PR #386 / WRK-A4D-LEAN-FOUNDATION-THEORY-TRANSFER
(composition executor).

## Frozen application and evidence

The reviewed application is `lean-operational-transfer-to-theory-transfer`
at published commit `7ed1f35722242f68bd4a1939d36c5f92c498aa5f`.
GitHub's commit API identifies its tree as
`9033e0baeb277ba75e52d5b5e47da3b2cefc62bc`; local frozen commit
`f48a4734def8ef2af0816ddb335d1f1c799b5a90` has that same tree.

The application digest was independently recomputed with the repository's
`application-digest` command as
`0230078042b9861d8a3599d32ceea20452eba9e945260507c4c0dd325d46fd2a`.

The evidence is pinned to published source commit
`7cb104eddfa6fa2479b3c7ee296a1be14df30b6b`, GitHub-confirmed tree
`c009e0fad6327ca3694acf08bd5feb586ac6a61d`:

| Evidence | Independently verified SHA-256 |
|---|---|
| `03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean` | `c164818dc50de94afad690946d4c209309350340b5cb1586ddc9f91f74bcb203` |
| `03_FORMALIZATION/D0/Foundation/VerificationCore.lean` | `382b2b506e17c6422623b6a2581756468e157def9ea783445f0943bd124a19d7` |
| `02_REGISTRY/research/D0_THEORY_TRANSFER_2026_10_20.md` | `4e47964de7f334ebc9c0d69be28004b1235f7a113ee8006d85c2d56648af1482` |

Each evidence blob was independently read and hashed and is byte-identical
in the source commit, application commit and reviewed working tree. The
primary composition artifact, original M1 proof-transport owner and original
target text were also inspected.

## Comparison with the original target

The original target at main
`dff7498b9071ad4d9fd1580b80829d91eb55f534` requires generic conditional
transfer between two operational systems, state/action/test/outcome maps,
finite-program execution and composition, preservation and reflection of
empirical distinctions on the declared common sector, an explicit
assertion/proof interface and retained imported premises. It separately
requires physical realizations and visibility of additional native tests.

Its statement, interface, positive outcome, family scope and
`verification_core` acceptance dependency are unchanged. The new hypothesis
keys identify those pre-existing domains. The assertion interface chosen
here is semantic entailment of predicates on future empirical classes;
the theorem does not claim a parser or soundness proof for every external
formal language. This is an explicit realization of the target's declared
proof interface, not a claim of physical dynamics from syntax.

The bounded 52-to-54 active-result budget change introduces the two direct
architectural owners. It neither adds a new physical assumption nor replaces
any existing native/GR target.

## Exact hypothesis map

The application uses the direct method on `theory-transfer-v1`.

- `operational_interpretation` maps identically: two declared total
  `FutureExecution` systems and primitive state, finite-program, test and
  injective outcome maps, with primitive execution/readout equations.
  Complete-word commutation, common-sector faithfulness and proof
  preservation are proved later; none is a structure field.
- `foundation_representation` maps identically: the same original
  `TheoryVerification F.futureEmpiricalTheory` used in the foundation.
  Its use in identifying the verified state with the native empirical image
  is explicit. The separate `verification_core` prerequisite is retained.
- `assertion_regime` maps identically: a predicate regime or indexed premise
  family on source empirical classes, together with an actual source Lean
  proof. Every translated premise is supplied by a proof or retained as an
  explicit regime hypothesis. No source hypothesis is erased by translation.
- `additional_native_contexts` maps identically: the unconditional result is
  on exactly the compiled source experiments. Only the stronger all-native
  result requires a concrete `NativeContextCoverage` witness. Extra native
  operations and observations remain in the original target system.

These are concrete interface inputs already called for by the original
obligation. In particular no native Einstein equation, complete-price
identity, physically selected optimizer or final equivalence of theorems is
introduced as a new closed hypothesis.

## Operational derivation and common carrier

`Interpretation` supplies only primitive diagrams. `compile` concatenates
the actual native programs. `run_commutes` follows by induction from the
primitive state equation, and `profile_commutes` follows by combining that
result with primitive observation commutation. `compile_append`, `comp` and
`comp_compile` preserve chronological composition, including compilation
through an intermediate interpretation.

`commonExecution` keeps the full native state carrier while exposing the
source actions and tests through their compiled native realizations.
Outcome injectivity gives reflection in `common_profile_eq_iff`; the
execution/readout diagrams give preservation. The quotient map is therefore
well-defined and injective without requiring raw-state injectivity.
`imageEquiv` is constructed onto the explicit common empirical image, and
`imageStep` proves that image closed under interpreted source actions.

The bridge to the foundation is checked on actual maps:
`verifiedStateImageEquiv_representedState` identifies the represented state
of each source state, and `verifiedRun_image` identifies its represented
finite run with the class of the actual compiled native run. Thus the
accepted foundation is used on the same carrier; the proof does not merely
declare the two independently constructed quotients compatible.

## Proof reuse is derived and has observational meaning

Predicates are transported through the constructed image equivalence.
`translate_future_observation` proves that a translated source observation
assertion is exactly the actual common native quotient readout with the
specified injective outcome encoding. This prevents the result from being
only an uninterpreted renaming of predicate symbols.

Translation preserves conjunction, negation, implication and indexed
universal quantification. `translate_after_step` uses the same proved action
diagram. `assertionFaithful` derives the existing `Faithful.iff_derivable`
field from the image equivalence; it is not assumed. `transfer_theorem`
then consumes the already owned `faithful_preserves_derivable` theorem with
the supplied source proof. `transfer_from_premises` makes every imported
premise explicit at the target point.

The source assertion proof itself is an intended input of theorem reuse.
Its reuse is not circular: the newly established content is the operational
interpretation, its empirical equivalence and the equality between
translated observational predicates and native readouts.

## All-native boundary and decisive controls

Full native indistinguishability always reflects source indistinguishability
because compiled source experiments are among the native experiments.
The converse is not inferred from that inclusion. `NativeContextCoverage`
requires a source context and readout postprocessing for every native finite
experiment on represented states. Its correctness equation yields the
stronger `native_profile_eq_iff`.

The extra-bit test example is a genuine counterexample to dropping this
coverage input: all primitive diagrams commute, source future profiles
coincide for two states, and an additional native test separates them.
`extra_native_test_prevents_coverage` proves that no coverage witness exists.
The existing uncoupled-center projection provides a positive family with
actual coverage while correctly allowing a noninjective raw-state map.

The reviewed wording explicitly describes all-finite-word execution/readout
commutation. It does not claim injective preservation of every paid history,
native intermediate stage, clock duration or number of primitive gates.
An interpretation may compile an empirically idle source action to an empty
word. Physical clock and payment preservation consequently remain separately
required maps for a physical application.

## Acceptance boundary and next consumer

This acceptance supplies the generic conditional transfer obligation. The
existing `verification_core` prerequisite must also be accepted; this review
does not bypass it. The named next consumer is
`gr_operational_realization`, whose actual state/action/preparation/readout,
complete Cost-Info, matter-source, clock, variation, unit and refinement
premises are still to be proved on the same family used by `positive_gr`.

No native action, physical admission, causal independence, prospective
optimizer, nonlinear GR dynamics or controlled continuum limit follows from
the generic theorem alone. Additional native distinctions cannot be erased
by restricting the common test family.

This decision independently checks the exact statement, source and target
interfaces, complete hypothesis map, proof structure, consumer, evidence
hashes and published tree identity. Full serialized Lean closure and final
integration validation remain separate PR completion gates. This reviewer
ran no build and does not report an unfinished final build as successful.
