> **Scope correction — 21 October 2026.** The title below should be read as a
> barrier for deriving GR from the *current explicit Cost-Info/history
> interfaces alone*. Book03 §03.25 already supplies a unique master bootstrap
> action `B_N = beta^-1 log Tr exp(-beta Delta_N(V)) - log det(I-zF_N(V))`.
> Hence the current specification is not missing an aggregation scalar at the
> action layer. What is still absent is the native same-execution
> identification/pullback of the bootstrap Hodge Laplacian `Delta_N(V)` and
> feedback `F_N(V)` to the actual moving GR carrier, including all field,
> observer, preparation, clock and refinement jets. Existing
> `A4D_NATIVE_SOLDERED_HEAT_SOURCE.md` explicitly records
> `bootstrap_heat_identification = OPEN`. Sections below remain valid as
> no-shortcuts showing that mean Cost-Info, normalized coherent amplitudes,
> endpoint allocation, or D_min cannot substitute for that pullback.

# Current-specification GR closure barrier

21 October 2026. Existing Draft PR #334 only.
Phase: native realization / final composition.

This theorem composes four already-owned exact boundaries:

1. the literal Book03 `Cost-Info` path formula;
2. the exact endpoint-allocation family from
   `gr_assembly/sources/d0_cost_info_boundary_2026-10-19/theorem.md`;
3. the formal `ActionProtocol` excess-profile classification and full depth-two
   response in `A4D_NATIVE_BOOK03_OPERATOR_VARIATION_BOUNDARY.md`;
4. the corrected candidate-source comparison and full128 operator-family
   tangent in
   `A4D_BOOK03_FIRST_SOURCE_UNDERDETERMINATION_THEOREM_2026_10_21.md`.

It proves a statement about **logical derivability from the currently explicit
G0/Book03 interface**. It does not forbid a future native completion, and it
does not weaken any positive finite GR construction.

`GR_closed=false`.

## 1. Formal ActionProtocol does not identify the native Book03 pullback

The exact formal `ActionProtocol` fiber is already classified. For every
off-diagonal ordered pair, its nonnegative excess is independent; the type
imposes no path-composition, symmetry, refinement or field-source law.
`book03PathWeight` takes total `info` as a supplied real argument. The formal
owner explicitly records that `ActionProtocol` does not identify its
transition action with physical Book03 `Cost`, does not contain native
`Info(v)`, memory assignment or refinement, and therefore has no native field
source to differentiate.

Independently, Book03 writes the literal path price as:

`S(gamma) = sum_{e in gamma} C(e) - sum_{v in gamma} I(v)`.

The exact boundary theorem shows that the literal all-vertices reading is
incompatible with nonzero `Info` if singleton histories are action identities
and path action is additive. The full additive repair is a one-parameter
family:

`w_theta(u,v) = C(u,v) - theta*I(u) - (1-theta)*I(v)`.

For an open history from `v_0` to `v_n`:

`S_theta(gamma) - S_eta(gamma) = (theta-eta)*(I(v_n)-I(v_0))`.

The current Book03 text does not select `theta`. Closed paths do not see this
freedom, but finite retained tapes are open histories. Whenever the
endpoint-information difference has a physical first jet,

`D S_theta - D S_eta = (theta-eta)*D[I(v_n)-I(v_0)]`

is a genuine first-source ambiguity even with the same edge costs and the
same interior information values.

## 2. Conditional candidate-source identity under complete amplitude binding

Now grant more than the formal G0 layer currently proves. Assume the
normalized Book vector on the complete orthogonal native history basis equals
the actual native coherent record. Then the existing amplitude-binding
theorem forces:

`I_omega = C_omega + (1/2)*log_phi(q_omega) + J`

`S_omega = -(1/2)*log_phi(q_omega) - J`.

Thus relative branch gains and phases are fixed; only the common real mode
`J` remains.

For exactly the same complete history data define:

`M = sum_omega q_omega*S_omega = (1/2)*H_phi(q) - J`

`P = -log_phi(|Q_B|) = -J`.

Both are scalar functions of the same amplitude-bound Book family. Their
first sources satisfy:

`D M - D P = (1/2)*D H_phi(q)`.

The common mode cancels. Therefore an absolute anchor for `J` cannot make
these two variational readings equivalent on a chart with moving record
entropy.

**Correction to the former tangent.** The trial derivative
`(Dq0,Dq1)=(-1,+1)` inside one nonblank Golden pair is not admitted by the
original Kraus law: `q0=p^2*x` and `q1=p*x` keep their conditional ratio
fixed. The value `D H_phi=-1` and the resulting `-1/2` are withdrawn as
full128 native-tangent claims.

A separate exact full128 operator-family theorem
(`sources/d0_variational_selection_synthesis_2026-10-21/aggregation_audit/PROOF.md`)
proves `D_nu H_phi > 0` for `0 < nu < sqrt(3)/2`, retaining all 128 labels
and the actual moving Julia defects. At `nu=0.5` its replay gives
`D_nu H_phi is approximately 0.7671427296`; the strict sign comes from the proof, not
from that decimal. This is an operator-family tangent only: physical
controller admission, Fourier preparation and identification of `nu` with an
original GR field direction remain unproved. A separate proper-Lorentz
theta-chart calculation is also available, but its sign at `theta=0.08` has
no interval enclosure. Neither candidate tangent selects the Book03 master
bootstrap or proves a physical source equation.

## 3. Matching the configured CQ price does not remove the ambiguity

Let the already-owned complete CQ scalar be:

`S_CQ = C_bar - H_phi`.

If one requires the **mean** amplitude-bound Book path price in section 2 to
equal this CQ value, then necessarily:

`J = (3/2)*H_phi - C_bar`.

The amplitude pressure of the same Book vector is then:

`P = S_CQ - (1/2)*H_phi`,

hence:

`D P - D S_CQ = -(1/2)*D H_phi`.

For any tangent, this gives the exact conditional identity
`D(P-CQ) = -D H_phi/2`. Conversely, if the amplitude pressure is required
to equal CQ, then `M = CQ + H_phi/2` and
`D(M-CQ) = D H_phi/2`. Thus for any tangent with `D H_phi != 0` the two
scalar candidates differ after matching one candidate value. The exact
nu-family theorem above supplies such a tangent on its declared operator
family under the separate amplitude-binding hypothesis; it does not prove
`nu` is an admitted physical controller or GR field variation.

These identities do not show that either candidate equals Book03's master
bootstrap `B_N`. That action is already specified; the unresolved step is
its same-execution pullback to the physical field, history, preparation,
clock and work variables. No physical aggregation or source conclusion
follows from the candidate comparison alone.

## 4. Actual closure consequence: the bootstrap pullback is missing

Book03 §03.25 fixes the action-layer scalar B_N. The current documents do not
provide one admitted same-execution map from the original 42 field variables
and independent physical inputs to the moving bootstrap operators
Delta_N(V), F_N(V), retained history, preparation, observer, clock, work and
Book03 Info. In particular, no field jet of B_N on the original GR carrier
can currently be evaluated from the specified physical execution.

PR #334 also carries a separate [two-bin rectangular CFL theorem and
checker](A4D_NATIVE_GOLDEN_RECTANGULAR_CFL_AND_CAUSAL_TWO_SCALAR_2026_10_21.md).
On its stated rank-two chart and linearized frozen N=1 two-CAR equation, one
temporal bin per spatial step is unstable at `r=1` for any positive spatial
PF, while two native time bins give a strict CFL gap under the proved PF-ratio
bound. The bounded original `n=24, L=8` history census, rectangular grouping
and inverse-PF volume weight replay exactly. This closes that scoped
material-stability gate only: the anisotropic original 16+24 geometric
source, outgoing boundary term, physical clock selection and same-execution
Book03 pullback remain open.

The exact candidate identity in section 2 and the nonzero nu-family entropy
source are useful controls on proposed substitutions, but neither supplies
that map. The pairwise (-1,+1) Golden direction is withdrawn as an inadmissible
native tangent. The proper-Lorentz theta-chart source remains numerical
without an interval enclosure; the nu-family sign is exact on its declared
operator family but its physical controller admission is open.

This is a derivation boundary in the current specification, not a
construction of two fully admitted D0 completions and not a no-go theorem
for every future completion. The positive finite GR families remain intact;
the missing evidence is their same-history physical selection and pullback.

## 5. The missing same-execution theorem

Book03 already names the action-layer functional. The required theorem must
identify its arguments and all source-bearing variables on one admitted
history:

1. **Common-initial execution map.** Derive the actual preparation, field
   writer, scene/LEFT interaction, CAR instrument, observer and outcome tape
   from one admitted initial D0 state and named primitives.
2. **Complete Book03 valuation.** Compute the moving Delta_N(V) and F_N(V),
   every retained history and memory class, branch Cost and Info, absolute
   normalization, clock, work, failures and cut on that same execution.
3. **All independent equations.** Differentiate the full price in the
   original 16 coframe, 24 proper-link and 2 matter directions, plus every
   independent preparation/controller/clock direction and genuine constraint
   reaction. No source may be fitted or discarded.
4. **Physical selection and refinement.** Prove that this execution is
   compulsory under the existing D0 admission law and carry its source to
   the original raw-216 refinement norm.

The current BOOK_SOURCE_BINDING owner explicitly does not identify state code
length with Book03 vertex Info on the native full128 tape. The formal
ActionProtocol also lacks the physical memory assignment, refinement and
field-source map. Thus neither the action-layer formula nor an entropy
identity alone supplies items 1--4.

Existing PR #334 now also contains two **numerical finite roots** of all 42
field rows for the configured original N=1 CQ price on a spatially homogeneous
two-interval slab, at positive diagnostic weights `(1,1)` and `(1,2)`. Each
root was checked against independent complex-step derivatives of the complete
CQ value; the latest local replay has maximum 42-row residuals about
`5.2e-15` and `6.5e-15`.
The second-variation audit also qualifies these roots: for both diagnostic
weights the fixed-link, fixed-matter raw 16-coframe Hessian has inertia
`(8+,8-)`, and independent second differences of the complete N=1 CQ value
have both signs. For `(1,1)`, the checked directions give approximately
`+3.02833` and `-1.09127`; for `(1,2)`, approximately `+2.98687` and
`-1.10617`. These stationary roots are coframe saddles of this configured
price, not free coframe minima. This is not a no-go for a physically
justified constrained or stationary principle, but unrestricted Cost-Info
minimization cannot be inferred from these roots.
A separate warm-start replay finds full42 roots at five sampled positive
time-slice PF ratios `1, 1.25, 1.5, 1.75, 2`, with maximum source residual
below `7.9e-15` and minimum reported numerical singular value above
`0.04468`. These are discrete numerical points only; they do not prove a
continuous root branch, validated interval existence, actual native AF
weights or mesh refinement.
This closes a useful finite candidate-price test, but not an interval-certified
root, a longer-slab theorem, actual native AF counts, physical writer
admission or compulsory full Book03 selection. It tests the 42 geometric and
matter directions only for the configured CQ price, so item 3 remains open
for the specified Book03 master price and for independent preparation,
controller and clock directions. It does not supply items 1, 2 or 4 above.
The detailed [witness note](A4D_COMPLETE_N1_FULL42_FIXED_COLLAR_FIRST_NONFLAT_RANK2_NUMERICAL_ROOT_2026_10_21.md)
checks nonzero site curvature and matter invariants, rank-two real stress and
a nonidentity spatial Lorentz plaquette. Its separate
84-variable, three-interval run did not reach a root within its iteration
budget; this numerical failure is not a no-go theorem, but the two-interval
result supplies no refining sequence.

The same PR now gives an exact formula and sharp bound for the normalized
complementary full128 feedback component in terms of the principal angles
between the normalized history range and the active-return cut. This closes
its algebraic first-source expression once that complete map and cut are
provided. It supplies neither the actual physical angle velocities and cut
jets nor the independent thermal source in `B_N`; these still must be
computed on the same admitted execution.

Combining the sharp angle-speed bound with the existing soldered-heat
calculation gives a conditional rejection threshold: if that heat is the
selected `Delta_N` source and every other `H_01` term vanishes, stationarity
requires `sum_k |D theta_k[H_01]| >= (128/(9*r_R))*sqrt(1-zeta)/zeta`.
For the illustrative values `r_R=128`, `zeta=1/2`, this is at least
`0.1571348403`. The common execution has not yet been shown to identify that
heat, cut or fugacity, and any other priced source changes the numerator.

Until this map is derived, a CQ price, raw amplitude norm, normalized
feedback or mean Cost-Info cannot be identified with the full physical
Book03 pullback by notation. The exact full128 nu-family source is a scoped
candidate comparison, not a replacement for that missing theorem.

## 6. Research disposition

Do not repeat geometry scans or the now-replayed two-interval CQ root search.
The next scientific step is to pull the specified Book03 bootstrap back along
the same admitted histories and compare its full source with the existing
42-row CQ roots, or identify the precise core definition that determines that
map. Do not treat nu as an independent physical field/controller coordinate
without an admission theorem, and do not add a new physical selector or
postulate as a computational convenience.

If existing core axioms do not determine the map, record that exact
definition boundary before attempting a physical GR promotion. This is an
open construction task, not proof that no future D0 completion exists.

The accompanying checker validates the generic amplitude-bound source
identities, the corrected full128 operator-family replay and the conditional
endpoint-allocation identity. It does not certify physical Book03 admission
or the bootstrap pullback.

Positive results remain intact: exact all40 Cartan families, the configured
all42 CQ source, rank-two double-zero finite sheets, paid writers, direct
signed-curvature readouts, full128 preparation/input closure and conditional
GR recovery remain valid within their declared interfaces.

GR_closed=false.
