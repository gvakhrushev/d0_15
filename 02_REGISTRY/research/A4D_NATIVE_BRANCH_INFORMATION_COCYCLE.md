# A pathwise information cocycle from the owned golden record process

15 October 2026. SOURCE #310. This is a **conditional positive derivation**
for the actual direct/return record instrument. It does not close G0 or select
the full D0 physical action.

## The missing scalar can be solved once the path weight is bound

Three existing pieces meet on the same complete history `ω`:

1. Book III sets the path weight to `w(ω)=φ^(-S(ω))` and the path action to
   `S(ω)=Cost(ω)-Info(ω)`.
2. The owned golden prefix code assigns direct `0` cost 1 and return `10`
   cost 2. Its reference cylinder is
   `μ(ω)=φ^(-Cost(ω))`; every record remains in the complete parser.
3. The actual complete comparator has recorded probability
   `qρ(ω)=Tr(ρ Aω* Aω)`. The existing likelihood construction proves
   `qρ(ω)=μ(ω) Tr(ρ Mω)`, including all prefixes and both outcomes.

Instantiate Book III's `w` with this measured probability `qρ`. On histories
with positive probability, the three equations force

```text
Sρ(ω)       = -log_φ qρ(ω)
Infoρ(ω)    = Cost(ω) - Sρ(ω)
            = log_φ(qρ(ω)/μ(ω))
            = log_φ Tr(ρ Mω).
```

There is no remaining choice of a Shannon or von Neumann entropy in this
pathwise equation: those are different state functionals. The local increment
at a branch `y` after prefix `ω` is

```text
Infoρ(ωy)-Infoρ(ω) = log_φ(qρ(y|ω)/μ(y)).
```

Earlier recorded outcomes enter through the actual conditional probability
`qρ(y|ω)` and the full-history effect `Mω`. This is the exact Bayesian
likelihood cocycle on the owned branch algebra, not a one-record approximation.

The expected branch information is the KL divergence
`D_φ(qρ || μ)`, while the expected path action is the actual path entropy
`H_φ(qρ)`. The identity is

```text
E_q[Cost] = H_φ(q) + D_φ(q || μ),
E_q[Info] = D_φ(q || μ),
E_q[Cost - Info] = H_φ(q).
```

This distinguishes two quantities that were previously easy to conflate.
The Shannon entropy of the tape is an expected surprisal; it is not the
pathwise `Info(ω)` forced by the exponential path-weight equation when
`w=qρ`. The previously checked Shannon `Cost-Info` calculation remains a
valid conditional entropy candidate, but it is a different action
interpretation.

The three expectation identities above are for a finite complete history
partition at a fixed number `T` of instrument rounds. They do not assert the
same formula at a variable accumulated-cost stopping cut; the existing direct
forcing result gives an exact control showing that a cost cut is not a fixed
round cut and that its expectation needs stopping-time terms.

## Refinement and joint variation

Put `Lρ(ω)=qρ(ω)/μ(ω)=Tr(ρ Mω)`. It is nonnegative on every history and
strictly positive on the support of `qρ`. Completeness of the two actual
instrument outcomes and golden cylinder refinement give

```text
μ(ω0)Lρ(ω0) + μ(ω10)Lρ(ω10) = μ(ω)Lρ(ω).
```

Equivalently, `Lρ` is a positive likelihood martingale on the full golden
history tree. The identity is exactly the already-owned operator relation
`p Mω0 + p² Mω1 = Mω`; it neither drops an archive branch nor replaces the
native cost cut by a fixed number of rounds.

For a fixed code and any admitted differentiable variation `V`, write
`Fω=Aω* Aω`. On a positive-probability branch the joint source is

```text
D_V Infoρ(ω) = Tr[(D_V ρ) Fω + ρ (D_V Fω)]
               / (log(φ) Tr(ρ Fω)).
```

Both preparation and return-operator variation are present. Substituting the
moving conditional state from v3 therefore retains its event-normalization
term; freezing the preparation would delete part of this source. The Lean
capsule proves the scalar log derivative for an arbitrary probability jet,
and the v3 certificate supplies the actual full-carrier moving-preparation
jet in its declared commuting-reference instrument class.

## Verification and source pins

The Lean capsule imports the actual `cylWeight` / `weightExp` owner and proves
the code-surprisal identity, pathwise action decomposition, uniqueness of the
information value, local cocycle, nonnegative likelihood, refinement
identity, and joint derivative. All seven declarations depend only on
`propext`, `Classical.choice`, and `Quot.sound`. The exact checker verifies the
saved Lean declaration/axiom output and its source blob, in addition to all 126
binary histories through depth six, all 63 prefixes through depth five, local
telescoping, the KL expectation and derivative, a moving state/effect control,
and hostile entropy/branch-omission controls. The finite KL and expectation
instances use the explicitly diagnostic factorized law
`q_r(ω)=∏(1-r)` on direct letters and `r` on return letters, for `0<r<1` and
fixed round depths `T=1,…,5`. They are exact symbolic checks of that fixture,
not a replay of the actual noncommuting comparator instrument. The Lean
pathwise lemmas are generic in `q`; the actual comparator's probability law
and positive likelihood lift are consumed from the pinned direct-forcing
owner, not re-proved by this finite fixture.

| Input | Git blob |
|---|---|
| `BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md` | `ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa` |
| `DetectorSupportGoldenWeight.lean` | `d7f7f170815cc3ad2052ad48280ae5919652b314` |
| `A4D_NATIVE_DIRECT_FORCING_ATTACK.md` | `2def57a045d3a3f83b058c35bb56aec390ce1733` |
| Direct-forcing source `RESULT.md` | `d421f20e91c3feb0d636428a1db19233ffb89f5f` |
| v3 `MOVING_PREPARATION_SOURCE_RU.md` | `2fe1893246a6ed4985649b6e20af800cec4870f6` |

Reproduce from the repository root:

```sh
cd 03_FORMALIZATION && lake env lean ../02_REGISTRY/research/certificates/a4d_native_branch_information_cocycle.lean
python3 02_REGISTRY/research/certificates/a4d_native_branch_information_cocycle_check.py
```

## Exact boundary

This closes the **branch-probability algebra** if the actual recorded
probability is the Book III path weight and the already-owned prefix length is
the `Cost` readout. The remaining owner decision is whether those two maps are
indeed the physical `w` and `Cost` in the full D0 history action. The current
`ActionProtocol` has no `Info` field, so this theorem does not silently make
that admission.

The logarithmic formula is stated only on positive-probability histories.
Zero-probability branches need an owned support convention or an extended-real
action; no finite logarithm is asserted there. The formula also measures
information on the complete classical record-outcome algebra. It does not
promote full-operator entropy of the coherent record state to, or exclude it
from, the physical `Info(v)` unless the native history-to-readout map says so.

There is a further normalization condition before this branch formula is the
full Book III source. If `w(ω)=φ^{-S(ω)}` is an unnormalized history weight and
`q(ω)=w(ω)/N` is the Born-normalized probability on the same finite outcomes,
then `Info(ω)=log_φ(q(ω)/μ(ω))+log_φ N`. Its joint derivative contains
`D N/(N log φ)`. The exact finite theorem and the moving-normalizer control are
in [the partition-corrected continuation](A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md).
The older cocycle is complete for the physical source only if the common
history/readout binding is proved and `N` is identically one along the admitted
family, or an independently owned term supplies its full variation.

No map to the complete `(q,D,b,m)` tangent, all ten `ρ₀` components, own
source/Ward identity, exact curved joint roots, soundness/recovery, physical
constraints, G0 closure, or positive GR follows yet. No action, selector,
axiom, CORE/BOOK owner, claim status, or parent terminal is changed.
