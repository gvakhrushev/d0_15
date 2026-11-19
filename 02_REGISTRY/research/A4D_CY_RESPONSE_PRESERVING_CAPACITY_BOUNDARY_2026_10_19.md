# Response-preserving entropy bridge for the retained `C_Y` leaf

19 October 2026. Same-source continuation inside Draft #334. This is an exact
finite boundary for applying BOOK_02 §§02.20–02.21 to the existing `C_Y`
address copy. It selects no new native action or physical instrument.

## Result

BOOK_02's entropy extremum is taken over coupling kernels that preserve the
declared D0 response vector (or a separately declared loss quotient). It does
not license changing the input response while optimizing the bridge kernel.
For the `C_Y` bridge, if the complete old LEFT-leaf projectors are retained
as response coordinates, the leaf kernel is forced to be the identity.
Consequently its leaf marginal is the input marginal `π`; entropy can vary
inside each leaf, subject to the remaining response constraints, but it cannot
reweight the leaves through the bridge.

The actual `C_Y` owner gives the exact effect identity

```text
J_Y* (I ⊗ |enc(i)><enc(i)|) J_Y = P_i^L.
```

Therefore, for every input density `ρ`,

```text
Pr(Y = enc(i)) = Tr(ρ P_i^L) = π_i.
```

This is an actual response-preserving finite map, not a probability
approximation. If a declared loss map identifies some leaves, only its
quotient response is fixed; redistribution inside a loss fiber needs to be
named and justified at that quotient.

By contrast, the fine-history capacity profile in strategic synthesis §7.5
uses independently variable leaf probabilities

```text
r_i* = Z_i / Σ_j Z_j.
```

At the vacuum `Z_i` are equal, so this becomes `1/n`. It is admissible for a
`C_Y` bridge only when this profile agrees with the preserved `π` (or when a
declared quotient actually loses the distinguishing leaf responses). If
`r_i` denotes the output marginal of `Y`, the §7.5 profile and the fixed-input
response-preserving bridge are different variational domains. The former may
still describe a separately admitted change of the native preparation state;
that state law must then account for the full changing response and its
preparation/clock source. BOOK_02 alone does not make that input variation
available.

This distinction leaves the principal §7.39 construction intact: it keeps
the original unequal golden addresses and uses the proved inverse-PF factor
to cancel their weights in the linear source. It does not replace them by a
uniform Born prior or by the §7.5 unconstrained capacity optimizer.

## Fixed-leaf source identity

Let the retained instrument have one `good` outcome and failure outcomes
`ζ`, with a common normalized failure law `β`. On a fixed input leaf `i`,
write

```text
q_i(good) = g_i,
q_i(ζ)    = (1-g_i) β_ζ,
g_i       = exp(-2 J_i),
H_β       = -Σ_ζ β_ζ log β_ζ.
```

For the joint law `P(i,s)=π_i q_i(s)`, ordinary finite Shannon entropy gives

```text
H(P) = H(π) + Σ_i π_i [h(g_i) + (1-g_i) H_β],
h(g)  = -g log g - (1-g) log(1-g).
```

Differentiating the complete law, including moving leaf masses, gives

```text
D H(P) = D H(π)
       + Σ_i Dπ_i [h(g_i)+(1-g_i)H_β]
       + 2 Σ_i π_i κ(g_i) D J_i
       + Σ_i π_i (1-g_i) D H_β,
κ(g) = g [H_β - log((1-g)/g)].
```

The last term is zero when the failure law is fixed. At a common base
`g_i=g_*` with fixed `β`, the coefficient of `Dπ_i` is constant and
`Σ_i Dπ_i=0`; hence

```text
D H(P) = D H(π) + 2 κ(g_*) Σ_i π_i D J_i.
```

On a fixed-past geometry/matter variation `Dπ=0`, this is exactly the
weighted feedback source already used in §7.33. For a preparation or clock
variation, `D H(π)` remains. The full `Cost-Info` normalization in base-φ
units divides these identities by `log φ`. A changing failure law, unequal
base conditional entropies, or leaf-dependent response adds the displayed
terms; those cannot be dropped by naming the result a capacity bridge.

## Scope and next binding

The exact CNOT effect identity establishes the readout map for the declared
finite `C_Y` construction. Physical admission of that controller, the full
native source/response vector for the complete experiment, and the actual
same-carrier `good/failure` law and complete price remain open. This result
does not assert that the fixed-input bridge law is the only native
preparation variation. It shows exactly what must be proved before using
§7.5's reweighted profile: either a native input-state law that permits that
change and supplies its full response source, or a declared response-loss
quotient that makes it admissible.

The exact symbolic and rational controls are in
[`check_cy_response_preserving_capacity.py`](sources/d0_cy_response_preserving_capacity_2026-10-19/check_cy_response_preserving_capacity.py).
The checker pins the two primary inputs used here:

| Input | SHA-256 |
|---|---|
| `01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md` | `90d493492834c36900baddc57c987aa5e9910ee560993a793f6d178b4d827f03` |
| `02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md` | `748f723516dead3a713f31dd5a49dcbde7805ef0a15e7450f3026790abefa5e2` |

This is a scoped source/bridge result. G0, same-carrier physical Ward,
quantitative transfer, soundness/recovery, physical constraints, and positive
GR closure remain open.
