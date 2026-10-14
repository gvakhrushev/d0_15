# Source audit: what the native `Info(v)` term currently means

**Status:** research audit and scoped underdetermination witness. This does not
promote any information readout to the D0 core and does not close the physical
source, Ward, or GR obligations. It asks a narrower question: does the source
actually cited for `Info(v)` select one functional?

## Primary-source trace

Book III §03.3.0a defines

```math
S(γ) = Σ_e Cost(e) − Σ_v Info(v)
```

and describes `Info(v)` as a distinguishability gain: a history commits to a
choice at a branch, lowering uncertainty entropy. Its footnote points to
`BOOK-II-MECHANISM §II.3.APPX8.3.A`.

I checked that cited text in the preserved v14 source, rather than inferring its
contents from the footnote:

- source commit: `4f99c2c46e646d21ae5b9b0491da17bd1b094da0`;
- source blob: `19701354c459014fb88e33aace667e0904409f17`;
- SHA-256: `42224fdbfb6e474e2025d38da45d01bf1c9e17132c182e82d8875868df62c9b0`.

That section gives the same balance and qualitative explanation, but no
functional for `Info(v)`, no probability-to-information map, no entropy
formula or order, no base/unit, and no rule saying whether information is
measured on the branch-outcome algebra or on the full path-amplitude algebra.
The same source separately defines a heat-trace quantity
`I(u) = −ln P_return(u)` and a Bayesian update of a normalized measure
`σ_k`; neither is connected there to the vertex term `Info(v)`. The distinction
matters: a defined information-time observable is not a definition of action
information.

The current Lean action protocol also has only an action assignment,
reflexivity, and a nontrivial-transition lower bound. It has no `Info` field.
The M1/QM reconstruction bridge is conditional on an explicit assumption and
does not define this action term.

## Same native golden process, different information readouts

The existing coherent-AF certificate supplies a concrete discrimination test.
For the golden direct/return instrument `K₀ = √p I`, `K₁ = p Uθ`, where
`p = φ⁻¹`, every cost cut has the already-owned golden cylinder probabilities.
At the first cut its full record state has a nonzero off-diagonal block, while
its diagonal is exactly the golden reference `μ`.

Two standard uncertainty readouts therefore agree on the branch probabilities
and disagree on the information assigned to the full record:

```math
I_cl(σ) = −Σ_i σ_ii log_φ(σ_ii),
I_op(σ) = −Tr(σ log_φ σ).
```

For this process the classical code-minus-information action and its source
are identically zero. The full-operator readout has, at `cos θ = 3/5`, the
exact derivative

```math
−4p² log(4)/(5 log φ)
```

and the independently checked outward interval
`(-0.8803064263350401, -0.8803064263350399)`. The underlying packet gives the
full state, the formula, and the exact/interval replay in
`A4D_NATIVE_COHERENT_AF_COST_INFO.md` and
`sources/d0_coherent_af_cost_info_2026-10-14/RESULT.md`.

This is a witness against the claim that the cited **qualitative definition
alone** distinguishes record-diagonal information from information in the
noncommutative record algebra. It is not a countermodel to every D0 premise:
the source does not yet give the map that would admit or reject either
functional as the physical `Info(v)`. Exact distinguishability of recorded
basis outcomes does not, by itself, state that every joint record state is
dephased.

There is a second, independent interface gap. The owned golden prefix code
assigns direct/return lengths `1/2`, matching cylinder surprisal
`−log_φ(p), −log_φ(p²)`. This determines surprisal on that commutative
cylinder algebra. It does not by itself identify the vertex term with that
surprisal, its expectation, a reduction in a state entropy, or an extension to
off-diagonal record correlations. The path-weight identity
`w(γ)=φ^{-S(γ)}` cannot resolve the choice on its own: `S` is already defined
using the `Info` term being sought.

## Exact next theorem-or-countermodel target

The next proof should not introduce a new action. It should derive, from the
owned finite code and the Bayesian record update, a map

```text
native branch/history → recorded outcome algebra → Info increment
```

and prove that the result is invariant under admissible re-encoding and
compatible with the native refinement. The sharp test is whether M1 plus the
existing path-memory/verification requirements force the diagonal golden
surprisal, force an information functional on the full noncommutative record
state, or permit two full models satisfying all of those named premises. If
the last alternative holds, it is a scoped no-go for unique `Info` within
those premises; if one readout is forced, carry that exact functional and its
joint variation to the existing ten-slot source comparison. Until this edge
is proved, neither entropy candidate is the native physical source.

## Scope and replay

This audit does not change CORE, Book III, the claims registry, the old source
certificates, or the #310/#202/#317 terminal status. It adds no axiom and
selects no physical entropy. The quantitative witness is replayed by:

```sh
python 02_REGISTRY/research/certificates/a4d_native_coherent_af_cost_info_check.py
```
