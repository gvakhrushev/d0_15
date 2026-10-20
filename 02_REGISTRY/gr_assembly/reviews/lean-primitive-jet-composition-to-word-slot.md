# Independent review: ordered primitive words and first jets

Assembly-Acceptance: lean-primitive-jet-composition-to-word-slot 2fd27f22e6d5da240a116a56a372d01d9605bc03fcd070654fbeacceebe74e2d

Decision: ACCEPT for the scoped `primitive_jet_composition` obligation only.

Reviewer: Codex CONTROL independent reviewer (merge_research_intake, 2026-10-20).
Result owner: PR #342 / WRK-A4D-LEAN-PRIMITIVE-JET-COMPOSITION (original worker).

## Reviewed statement and evidence

The reviewed assembly application is
`lean-primitive-jet-composition-to-word-slot` at published commit
`7dad5382aff9a80d3fea2daa293739679034f8c4`.

GitHub's commit API identifies its tree as
`8323101ecbcbb6a3b1b2146cb5299a36416d441c`, exactly the tree of local
publication checkpoint `4eb6bc7020f541fdcd2e4364771dd5b1deff821c`.
The independent scope review was performed at local frozen commit
`88e3a74e9609bef75e313405dc659f1463c9548a`, tree
`925ccbd22048e45dffb2d505b6539dffb73c6bde`. The complete diff from that
reviewed checkpoint to the published tree changes only the integration-timing
paragraph in
`02_REGISTRY/research/sources/d0_w2_primitive_jet_lean_2026-10-16/CONTROL_INTEGRATION.md`.
The result, target, interface, hypothesis maps and proof bytes are unchanged.
The published commit is the durable review target.

The application digest was independently recomputed as
`2fd27f22e6d5da240a116a56a372d01d9605bc03fcd070654fbeacceebe74e2d`.

The original task brief at
`9e3073851e9fa59d3564caeb02a8a5cb4d6d936b` requires ordered-word
intertwining, the exact telescoping residual and the first-jet version with a
moving intertwiner, with explicit branching/comparison hypotheses. It requires
generic finite-word proofs and supplied norm bounds; real typed primitive
instantiations and physical admission remain with their existing owners.

The proof owner is
`03_FORMALIZATION/D0/Research/PrimitiveJetComposition.lean` at published source
commit `9e3073851e9fa59d3564caeb02a8a5cb4d6d936b`, SHA-256
`4e93661bd8d4f4a8402b9f177fbe0e1e2f8e635adb9622f541ad84abe1499731`,
Git blob `8fd7c8c1560c2a0018d6e4a7401a9549bb35d99c`.
Its bytes are identical in the independently reviewed published tree.

The fixed and vertex-dependent terminal identities are
`wordResidual_eq_orderedSum` and `movingWordResidual_eq_orderedSum`.
Their first-jet versions are `jet_wordResidual_eq_orderedSum` and
`jet_movingWordResidual_eq_orderedSum`. Exact endpoint intertwining follows
under supplied vanishing one-step residuals via `word_intertwining_of_steps`
and `moving_word_intertwining_of_steps`.

## Hypotheses and interface maps

The application uses the direct method on the identical `word-jet-v1`
interface. Each named result hypothesis maps identically to the same named
target hypothesis. No carrier transport or new scientific dependency is used.

- `algebraic_domain`: a finite ordered word of pairs `(V,U)` in one ring,
  and an arbitrary ring element at each vertex as its intertwiner. The head
  of the list is the leftmost multiplicative factor. First jets are the
  defined noncommutative value/derivative ring `Jet R`.
- `supplied_norm_bounds`: value estimates require `NormedRing`,
  `NormOneClass`, step contractions and the declared one-step residual
  bounds. The numerical derivative estimate additionally uses nonnegative
  `M` and `epsilon`, the supplied step and residual derivative bounds,
  and one shared parameter-dependent intertwiner.
- `branch_and_comparison`: labels, preparations, tests, adjacent carriers
  and endpoint readings require separately supplied agreement propositions.
  No word residual proves these propositions or postselection normalization.

The arbitrary-ring identities are algebraic. Treating a formal jet as an
actual derivative, representing physical typed maps in the common carrier,
or verifying the norm and agreement hypotheses for those maps is a further
application obligation. This acceptance does not supply those identifications.

## Applicability argument

For a vertex family `I_0,...,I_m`, the local residual at position `k` is
`R_k=V_k I_(k+1)-I_k U_k`. The ordered sum places the `V` prefix on its
left and the `U` suffix on its right. Induction on the finite word gives
exact cancellation of the internal vertex terms and leaves
`V_w I_m-I_0 U_w`. The proof uses associativity and distributivity without
commuting the factors. Constant vertices specialize to the fixed identity.

The proved ring structure on `Jet R` uses
`(x*y).deriv=x.deriv*y.val+x.val*y.deriv`. Applying the same ordered identity
in that ring preserves both adjacent intertwiner derivatives. In particular,
the one-step derivative contains `V dI_right-dI_left U`; it does not freeze
either vertex derivative. Vanishing of every supplied one-step residual
then yields the respective endpoint intertwining equality.

Under the supplied contraction hypotheses, each prefix and suffix has norm
at most one. Bounding each inserted residual and summing gives
`norm(R_w) <= m*epsilon`, for both fixed and vertex-dependent intertwiners.
For one shared parameter-dependent intertwiner, the three-factor product
rule and derivative bounds for the prefix/suffix give
`norm(dR_w) <= m*delta + m*(m-1)*M*epsilon`.

The finite controls preserve the distinctions between ordered and reversed
products, kept and frozen intertwiner derivatives, constant and unequal
vertices, and vanishing of a labelled sum versus each individual label.

These generic identities and conditional estimates supply the original
bounded formal premise recorded as `primitive_jet_composition`.

## Boundary and remaining assumptions

This acceptance supplies only `primitive_jet_composition` on `word-jet-v1`.
It does not discharge `native_sector` on `native-programme-v1`.

The numerical derivative estimate is accepted only for one shared
parameter-dependent intertwiner. For unequal vertex intertwiners, the
accepted owners provide the exact jet identity and the value-residual bound;
no corresponding numerical derivative estimate is asserted.

The branch/comparison propositions are explicit supplied hypotheses, not
derived physical agreement. Postselection normalization, label-wise
equivalence, physical primitive admission, actual preparations/readout,
the full native action/source, joint dynamics and GR closure remain separate.
No new physical operator, primitive or price is selected by this decision.

The independent review checks the original task terminal, exact statement,
proof structure, immutable source bytes, published scoped equivalence and application maps. Actual Lean
build validation for the integration is a separate PR gate; no Lean build
was rerun as part of this bounded review.
