# A4D stationary response memory: quotient before spectral classification

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `909ad048d25de2def8875290c41bf9475e9180e6`.
Status: exact response factorization and universal minimality; unrestricted
connection-stationary singleton collapse is false; admissible joint continuum
collapse remains open. No action, source, selector, or Lean owner is changed.

The 2026-10-01 architecture correction restores the original task's response
quotient objective. The main target is one class of mandatory metric readouts,
not one connection and not a census of Bloch zeros. This note derives a
source-independent finite memory from the literal action, proves its universal
property for arbitrary candidates, and identifies precisely what this does
and does not settle.

## 1. Typed local object from the action

Use column solder `S=(S_0,...,S_3)` in a fixed proper/time-oriented
nondegenerate component, `Q=S^T eta S`. This is equivalent to the row-solder
convention of the [nonlinear Lorentz quotient owner](MEMO_A4D_STAR_DENSITY_LORENTZ_NONLINEAR_QUOTIENT.md). The based plaquette is

\[
P_{rs}(x)=L_{x,r}L_{x+r,s}L_{x+s,r}^{-1}L_{x,s}^{-1},\qquad
C_{rs}(x)=\tfrac12(P_{rs}-P_{rs}^{-1})\in\mathfrak{so}(1,3).
\]

There are six faces and six Lie coordinates per face: the ambient curvature
carrier at a site is `V=so(1,3)^6`, of dimension 36. Realizability by one
shared-link field is retained; independent face data are used only to compute
the local linear projection, not to assert existence of connections.

The unit-coefficient cell action is

\[
\ell(S,C)=\sum_{r<s}\epsilon_{rs}
G_2\bigl(S_u\wedge S_v,\star\mathfrak b(C_{rs})\bigr),
\qquad\{u,v\}=\{0,1,2,3\}\setminus\{r,s\}.
\tag{1}
\]

Define the **solder current** `H=M_S C` by

\[
d_S\ell[\dot S]=\operatorname{tr}(H^T\dot S).
\tag{2}
\]

This is an explicit `16x36` linear map: each contribution is obtained by
replacing one of the two complementary legs in (1) by `dot S`. It uses all
actual based plaquettes. It discards no boundary link or frequency.

The true Gram lift is `dot S=S Q^{-1} dot Q/2`. Hence

\[
d_Q\ell[\dot Q]=\operatorname{tr}(\Xi^T\dot Q),\qquad
\boxed{\Xi=\tfrac12\operatorname{sym}(Q^{-1}S^T H).}
\tag{3}
\]

Here `sym A=(A+A^T)/2`. Pack the symmetric covector in the owner order
`(00,01,02,03,11,12,13,22,23,33)`: diagonal entries are `Xi_aa`, and
off-diagonal entries are `2 Xi_ab`. Write the resulting map as

\[
\mathsf D_S:C\longmapsto\operatorname{pack}\Xi\in\mathbb R^{10}.
\tag{4}
\]

Thus the metric partial is exactly `mathsf D_S C`. This derives the memory
from curvature and the action rather than declaring an unknown quotient to
be sufficient. Its kernel is linear in the curvature carrier even though
`L -> C(L)` is nonlinear.

On `E_K=0`, (3) agrees with the descended metric Euler independently of the
choice of Lorentz section: changes of section add only link variations, whose
pairing with `E_K` is zero. For the off-shell #216 comparator the corresponding
section term is controlled by its owned super-algebraic connection residual.

## 2. All nondegenerate coframes: ranks and stationary Ward identity

The map `dot S -> (dot(S_u wedge S_v))_{u<v}` is injective when S is
invertible. Reduce by `S^{-1}` to `S=I`, and write `dot S=S T`. An off-diagonal
entry `T_au`, `a!=u`, appears in the `(u,v)` wedge coefficient `e_a wedge e_v`
for any `v` distinct from a,u, so all such entries vanish if all wedge
derivatives vanish. The remaining equations are `T_uu+T_vv=0` for every pair.
Three distinct indices force each diagonal entry to vanish. Therefore the
map is injective on all sixteen coframe directions.

The bivector pairing and star are nondegenerate, and the complementary faces
exhaust all six wedge directions. Taking the dual proves `rank M_S=16`.
The Gram lift is injective on ten symmetric directions; composing with the
same injective wedge differential proves, for **every** invertible S,

\[
\boxed{\operatorname{rank}\mathsf D_S=10,\quad
\dim\ker M_S=20,\quad\dim\ker\mathsf D_S=26.}
\tag{5}
\]

These dimensions concern the ambient local curvature projection. They are
not a dimension or surjectivity claim about the nonlinear stationary fiber.

The actual local-Lorentz Noether identity includes every incident link at x.
With all link Euler equations zero, it gives

\[
\operatorname{tr}(H_x^T X S_x)=0
\quad\forall X\in\mathfrak{so}(1,3).
\tag{6}
\]

The ten Gram lifts and six vectors `X S` form a direct sum of the sixteen
coframe directions: the Gram differential is onto and has exactly those six
vertical vectors as its kernel. Consequently (3) reconstructs the complete
solder current H on the stationary Ward annihilator. There are no further
independent solder-Euler observations there. This does not reconstruct C or L.

Proper Lorentz covariance of (1) gives gauge invariance of (3): `S -> g S`,
`C -> g C g^{-1}`, and Q is unchanged. Thus the memory is defined on the
genuine nondegenerate Lorentz quotient, not on a gauge-fixed ansatz.

## 3. Exact minimality for arbitrary candidate types

Fix a sampled Q and let `Sstat(Q)={L:E_K(Q,L)=0}/G_Lor`. Define

\[
L\sim_Q L'\quad\Longleftrightarrow\quad
\mathsf D_{S_x}C(L)_x=\mathsf D_{S_x}C(L')_x\quad\forall x.
\tag{7}
\]

The canonical quotient is naturally equivalent to the image of the current
memory on the stationary fiber. Every sitewise Gram Euler observation, every
linear test of it, and every declared linear reconstruction factors through
this quotient. No Fourier support or microscopic candidate list is assumed.

For **any** type Y and map `f:Sstat(Q)->Y`, all those observations factor
through f if and only if

\[
f(L)=f(L')\ \Longrightarrow\ L\sim_Q L'.
\tag{8}
\]

Necessity follows by applying all coordinate Gram variations at each site.
For sufficiency, define the readout at `f(L)` to be the memory of L; (8) makes
it well-defined. On `im f` this map is unique. Equivalently there is a unique

\[
\operatorname{im}f\longrightarrow\operatorname{im}\Xi,
\qquad f(L)\longmapsto\Xi(L).
\tag{9}
\]

This is the coarsest sufficient quotient. The arrow in a minimality statement
runs **from any sufficient finer datum to Xi**. An arbitrary finer datum need
not be a function of Xi. Two coarsest sufficient presentations are naturally
equivalent.

If the protocol retains only a specified reconstruction `mathcal R_h`, the
corresponding coarsest memory is instead the image of
`mathcal R_h h^{-2} mathsf D_{S_h}`. Its ambient invisible subspace is
`ker(mathcal R_h mathsf D_{S_h})`. Changing the testing protocol can change the
minimal memory; that is not a proof that the deleted observations agree.

## 4. Universal no-extension, and the M1 boundary

For an arbitrary microscopic label type Theta and arbitrary admissible
realizations `(L,theta)`, equal Xi means equal **every original metric Euler
observation**. A label varying at fixed Xi cannot add a distinction in that
protocol. If a realization changes a metric observation, (7) proves that its
Xi has changed: the distinction already lies in the original observable
carrier. This quantifies over all Theta and all realizations, not a catalogue.

This exhausts extra **metric-response channels**. It does not forbid a new
realizable stationary value of Xi and does not prove the image is a singleton.
Nor does it claim minimality for other owned holonomy or history observations.

The [M1 observational quotient](../../03_FORMALIZATION/D0/Foundation/M1RepairObservationalQuotient.lean)
computes its class count only after it proves the image and carried
representatives. Here the stationary image is the remaining problem. The
[M1 faithful-interpretation theorem](../../03_FORMALIZATION/D0/Foundation/M1Universality.lean) cannot supply that
missing calculation: preservation and reflection of the required derivability
and protocol must be proved for the concrete interpretation.

There is an exact deletion control. At eta, put arbitrary Cayley-Y matrices
on Role 0 at the four phases and identity on other Roles. Parameters
`(1/5,1/7,1/11,1/13)` give Xi=0, the same memory as I, but 36 nonzero connection
Euler components. Thus response sufficiency does not by itself preserve and
reflect the full stationary equations. Restricting to Sstat is legitimate;
pretending that the quotient alone proves stationarity is not.

## 5. Exact controls: what can and cannot collapse

The [owned #232 family](MEMO_A4D_JOINT_PALATINI_LOCAL_UNIQUENESS.md) has
`Y=J12-J13+J23`, Cayley U(tY), Role-0 phase pattern `(U,I,U^{-1},I)`, and
identity other links. It is curved, nongauge, exactly connection stationary,
and has Xi=0. The memory quotient identifies it with I without calling it
gauge or choosing a connection.

The [owned #227 family](MEMO_A4D_J2_UNIFORM_COUPLED_NORMAL_RESCUE.md) replaces
Y by `B=K1+K2+K3`. It is also exactly connection stationary, but

\[
\operatorname{pack}\Xi_p
=\sigma_p\frac{4t}{4-3t^2}
(0,0,0,0,-1,1,1,-1,1,-1),\qquad
\sigma=(1,1,-1,-1).
\tag{10}
\]

Hence the proposed singleton statement on **all** of Sstat is false, even
near I on the fixed smooth background eta. Setting `t=h^2` gives at the origin

\[
h^{-2}\Xi_{11}=-\frac4{4-3h^4}\longrightarrow-1,
\qquad
h^{-2}\|\operatorname{pack}\Xi\|_1
=\frac{24L^4}{4-3h^4},
\tag{11}
\]

in the full unweighted owner sum. The latter cardinality factor is not
replaced by an average. Yet the four-phase mean is exactly zero. Phase
forgetting therefore identifies this field with I while losing mandatory
sitewise readouts; it fails (8). For a protocol containing only weak smooth
tests this particular staggered control has zero limit, and (11) is not a
counterexample to that weaker claim.

### Universal negative continuum theorem on the full EK fiber

This is stronger than checking two representatives. For every real a, take
the same exact boost family with `t_h=a h^2` on sufficiently fine meshes.
It remains in the fixed compact logarithm chart, with log size `O_a(h^2)`,
has the same fixed smooth metric eta, and is exactly connection stationary.
All these connections tend to the identical endpoint I. Nevertheless

\[
\rho_h(a):=h^{-2}\Xi_{11}(0)
=-\frac{4a}{4-3a^2h^4}\longrightarrow-a.
\tag{11a}
\]

Define asymptotic observational equivalence of stationary sequences by
vanishing normalized response difference in the declared full owner protocol.
For a!=b, even the fixed-origin component of the difference tends to `b-a`,
so the sequences are not equivalent. Thus

\[
\boxed{\mathbb R\hookrightarrow
\mathscr S^{\rm seq}(\eta)/\!\sim_{\rm obs}.}
\tag{11b}
\]

For **any** target type Y and any continuum forgetting map sufficient for
that protocol, equal forgotten classes must imply observational equivalence.
By (11b) the map must separate all values of a. Therefore there is no
response-sufficient singleton continuum quotient on the full `EK=0` domain.
This is a universal no-go for every proposed sufficient quotient, not a
candidate census. It also identifies unavoidable approach memory: the scale
of the projected curvature current divided by h^2 survives while the
pointwise connection and curvature approach the same flat endpoint.

The complete parametric identity is independently replayed without SymPy.
With `B^3=3B` and `D=4-3t^2`, the Cayley link numerator is
`D I+4t B+2t^2 B^2`. Give **every** link the same denominator D, including
inactive identities. Every literal Euler term contains four link factors;
its full numerator has degree at most eight. All connection coefficients
vanish, and the entire metric numerator is `4t D^3 sigma_p V`. Exact
coefficient equality therefore proves the rational family for all parameters
in the real chart; degree eight is not a truncated jet.

Equation (10) is not an independently prescribed smooth metric source.
Therefore #227 refutes unrestricted **connection-stationary** collapse, but
does not establish the original #310 joint-source no-go. Assigning its metric
response as its source afterward remains forbidden. The original source
admissibility condition must stay in the domain of any positive theorem.

## 6. The single remaining response-memory obligation

For the independently specified admissible joint/source class on fixed smooth
g, the non-tautological target in the declared owner topology is now

\[
\boxed{
\bigl\|\mathsf D_{S_h}
[C(K_h)-C(K_h^{sm})]\bigr\|_1=o(h^2).
}
\tag{12}
\]

Section terms at the comparator are handled by the #216 residual as above.
Then the owner reconstruction supplies the designated `-G[g]/2` limit.
For a different declared testing topology, (12) must be stated with its actual
readout operator and norm, not silently changed to an averaged sum.

The universal quotient is complete as a **readout quotient**; stationary
collapse of its admissible continuum image is not proved. The image must be
bounded from the literal shared-link equations and the independently declared
source class, or separated by an exact admissible counterexample. Connection
uniqueness and a full torus gap are optional sufficient lemmas, not the target.
Existing scoped designated and warped joint-isolation theorems remain valid.

## 7. Replay and status

`a4d_stationary_response_memory_check.py` derives M, the true Gram lifts and D
from 4x4 face matrices. Exact controls check the ranks, right inverses,
stationary Ward reconstruction, independent symmetric-tensor formula,
Lorentz covariance, scalar-memory failure, actual shared-link Euler equations
on three rational parameters of each already owned family, and the
same-response/different-stationarity deletion control. It also verifies every
coefficient of the full denominator-cleared degree-eight boost Euler family.
The all-coframe and
arbitrary-type proofs are the analytic arguments above, not finite-sample
extrapolations.

```sh
python3 02_REGISTRY/research/certificates/a4d_stationary_response_memory_check.py
```

Verdict: `STATIONARY_RESPONSE_MEMORY_FACTORIZATION_CERTIFIED`;
`ALL_EK_SINGLETON_CONTINUUM_QUOTIENT_NOGO`;
`JOINT_CONTINUUM_COLLAPSE_OPEN`. The all-EK singleton proposal is terminally
negative, with a real family of distinguishable classes. No claim/BOOK/CORE
promotion or original joint-source task terminal is made.
