# Independent integration and scope review: joint closure/source synthesis

21 October 2026. Reviewer: `complete_clock_information`, bounded reviewer
within the existing #334 integration. No author proof file was modified.

## Verdict and exact reviewed text

**ACCEPT the synthesis as a composition of the three stated conditional
results, at the scopes below.** Its all-cap Jacobi-kernel consequence and its
strict monitored-source balance are mathematically valid. Its local dust
construction does not assert physical diffeomorphism equivalence, an
arbitrary-matter classification, or a native finite-lattice realization.
The final text retains the source of the entire additional price and does
not identify the three executions or claim complete Book03/GR closure.

This review binds:

`02_REGISTRY/research/A4D_JOINT_CLOSURE_SOURCE_SYNTHESIS_2026_10_21.md`

SHA256:
`894eb2f075928288b1c5357f5dba0c379a46245b03244f598abe979a07c934d4`.

The final amendments explicitly retain `A_rest`, restrict the mixed-matrix
identity to the matter-free base, and state the fixed-RIGHT/remaining-price
hypotheses of the full LEFT-orbit screening result. All three amendments
were read before binding this final hash.

The scientific input snapshot for the three new packets remains
`dfc0275eea67ebc21ffe539de9b6ea96713863a5`. The following proof bytes were
read and were verified equal to their repository copies:

| Packet proof | SHA256 |
|---|---|
| `d0_centered_preparation_2026-10-21/PROOF.md` | `5d844191e050f2831f72c269e43a543d1670c0d3394d17fa5d2fb80a0ae516ed` |
| `d0_native_density_rigidity_2026-10-21/PROOF.md` | `23794bfbfbbe8c3524f370461ccc616d2c7653318e4a578250354db378fa26a2` |
| `d0_complete_return_entropy_2026-10-21/PROOF.md` | `ceb2ce2d05642977014ece32d8fa293302a3b23200b6cf60cf28ec916c0d5ec7` |

All packet paths above are relative to `02_REGISTRY/research/sources/`.
This reviewer independently reviewed and replayed the preparation packet,
and independently reviewed the density/Jacobi and integration arguments.
This reviewer authored the entropy packet: this report is therefore **not**
a second independent review of that derivation. Its separate mathematical
review and replay by `physical_source_closure` are retained in the entropy
packet's `INDEPENDENT_REVIEW.md`.

## 1. All-cap stationary sets: the actual hypotheses are necessary

The density theorem concerns precisely

```
S_N = integral V_N(r(x,y)) d^4z,
x = eta^2 e R(e,omega),   y = -eta^2 sum_A g^{mu nu} d_mu psi_A d_nu psi_A,
V_N = alpha [kappa-beta h_phi(r)] sum_{j=0}^{N-1}(beta r)^j.
```

The coordinate measure is fixed. The coframe, Lorentz connection, and both
real matter components are varied independently before any ansatz or
elimination. The coframe is nondegenerate, the fields are sufficiently
smooth, the domain is connected, and variations have proper interior
compact support or vanish on an open fixed collar. Eta and all internal
price parameters are spatial constants, with `alpha>0`, `0<beta<=1`,
`kappa>53`, and a fixed finite integer `N>=1`. The common operand rectangle,
the unique trace branch, and the nonvanishing price derivative are the
ones in the pinned radial owner; the theorem does not choose another
detector or material density.

The induced active Lie variation is a legitimate combination of these
field variations even though the action lacks arbitrary-coordinate
diffeomorphism symmetry. The density weight of `x` and scalar weight of `y`
give exactly

```
DS_N[L_xi Phi] = integral xi^mu partial_mu P_N,
P_N = F_N-x F_(N,x).
```

Together with the independent local coframe scaling identity, full
stationarity yields `dP_N=0` and `T=x r_x-y r_y=0`. Along `x=tau(y)`,

```
P_N' = Q_N-tau M_N' = Q_N(1-y M_N'/M_N).
```

The inherited bounds give the exact rational interval
`2475/266 < P_N'/a_N < 80512/1845`, hence the synthesis's weaker `9<...<44`.
The factor `a_N` is nonzero and retained; it is not uniformly bounded away
from zero across arbitrary readiness parameters. Therefore `x,y,r` are
constant on every full stationary field in this chart.

At such a field, `DS_M=(V_M'/V_N') DS_N` holds on **all** ambient field
variations, not only density-preserving variations. This proves equality
of the full critical sets for the same boundary task and every admitted
fixed finite cap. It does not apply to an optimized cap envelope, an
infinite cap, spatially varying internal parameters, or an automatically
identified finite PF ledger. It does not identify the prices or their
minima. In particular the opposite cap-one/higher-cap radial stability
signs remain possible and are preserved.

## 2. The strengthened Jacobi assertion is valid without integrability

At a common stationary background let `H_N=D^2S_N`, and let `v` be in its
full kernel: `H_N[v,w]=0` for every compactly supported ambient test `w`.
Differentiate the two **off-shell** identities from the preceding section:

```
H_N[v,L_xi Phi] + DS_N[L_xi v] = integral xi d(delta_v P_N),
H_N[v,R_t Phi]  + DS_N[D_v(R_t Phi)]
    = integral t delta_v(V_N' T).
```

At stationarity the `DS_N` terms vanish; the kernel condition kills the
Hessian terms; `T=0` kills the differentiated multiplier. Thus
`d(delta P_N)=0` and `delta T=0` for every Jacobi vector. No nonlinear
solution family tangent to `v` was assumed.

Since `T_x` and the branch pressure derivative are nonzero,
`delta x=tau'(y_*) delta y` and `d(delta x)=d(delta y)=0`. Proper interior
compact support or vanishing on the open fixed collar forces these
constants to be zero. This uses the collar to control the derivatives
entering `x,y`; boundary values alone must not silently replace it.
Consequently `delta_v r=0` pointwise.

The full Hessian is

```
H_N[v,w] = V_N'(r_*) integral delta^2 r[v,w]
           + V_N''(r_*) integral delta_v r delta_w r.
```

Its second term vanishes against every `w` for this `v`. The remaining
nonzero cap multiplier transfers the kernel inclusion, and reversing the
argument proves `ker H_N=ker H_M` on the **same fixed-collar variation
space**. This is stronger than testing perturbations tangent to a known
solution family, but weaker than equality of Hessian operators, quadratic
forms, stability, or finite perturbations. Without the collar, constant
density-changing modes have not been excluded and the equality is not
asserted. Also `delta y=0` constrains the coupled metric and matter
perturbation; it does not say `delta psi=0`.

## 3. Dust is a local representative theorem with the stated matter source

At constant densities the independent connection equation reduces to the
nondegenerate Lorentz Palatini equation with constant nonzero multiplier.
It forces the torsion-free connection of the original coframe. The
remaining rows are precisely

```
r_x e G_(mu nu) - r_y sum_A d_mu psi_A d_nu psi_A = 0,
partial_mu(g^(mu nu) partial_nu psi_A) = 0.
```

The scalar equation is undensitized. There is no inserted canonical
massless-scalar `-g_(mu nu) q/2` term. All original coframe, connection and
two scalar rows are accounted for, including the Lorentz-identity rows.

For one active real scalar with constant `q_*>0`, its normalized gradient
is a unit geodesic velocity. The first equation is pressureless Einstein
matter with `rho=(r_y/r_x)q_*/e>0`; the second gives its continuity equation.
For two active real scalars the source need not have rank one. The synthesis
correctly retains the broader density/cap theorem without classifying that
whole two-component sector as dust.

The converse starts with a smooth positive irrotational Einstein-dust
solution, a local unit velocity potential, and a regular flow box before
caustics. Conservation in proper-time/comoving coordinates gives
`e rho=C(X)>0`. The displayed time-independent spatial coordinate change
has Jacobian `C/k`, so `e_new rho=k`. Choosing
`q_*=-y_*/eta^2`, `k=-tau(y_*)/eta^2`, and
`psi=sqrt(q_*) T` gives the original `x,y` dictionary and the exact relation
`r_x k=r_y q_*`. All original rows then follow. The null version similarly
requires a nonvanishing null potential differential and positive density;
normalizing the positive local volume form gives `e varrho=L0 c^2`.

These constructions need no Bianchi, Brinkmann or VSI restriction. They
provide local representatives in chosen mass coordinates. They do not
prove invariance of the nonlinear action under arbitrary coordinate
changes, handle vortical dust/caustics/density zeros, select an actual
native continuum dictionary, or lift arbitrary dust to refining finite
executions. The synthesis preserves these distinctions.

## 4. The strict source balance now retains the entire price

The monitored theorem fixes the prepared ray and return projector on the
declared noncommuting unitary neighborhood and compares the actual cap law,
including its unresolved probability, with the infinite monitored law.
The bound is on the complete first derivative. It does not infer a zero
source from the constant mean clock, nor transfer coherent-cut entropy
to the monitored execution. The native-point interval
`10.61 < H_infinity'(sqrt(5)-2) < 10.62` is an analytic-tail/interval result,
not a floating sign inference.

For exactly the stated compatible price,

```
A_infinity = B_setup + Tr C_cycle - H_infinity,
```

an actually admitted independent continuous `c` tangent must obey
`partial_c(B_setup+Tr C_cycle)=H_infinity'` at a stationary point. If both
cost derivatives vanish, its price derivative lies in
`(-10.62,-10.61)` and that native point is not an interior stationary point
of this price on that tangent set. This is a necessary source condition,
not a theorem that the native finite gate language admits that tangent or
that all neighboring points fail stationarity.

The reviewed final text explicitly handles the larger price:

```
A_total = A_infinity + A_rest,
partial_c(B_setup+Tr C_cycle+A_rest) = H_infinity'.
```

This repairs the earlier possible overstatement from merely *including*
the monitored apparatus in a larger execution. Zero setup/cycle derivatives
exclude a full root only if the additional derivative also vanishes or the
additional price is absent. Unknown work, reference, preparation, monitoring
or other supplied price sources are not assigned zero. A moving projector
or preparation requires its own terms and is not contained in the fixed-ray
entropy estimate by default.

The logarithmic cap rule suppresses the truncation error after the actual
declared source amplification. It does not suppress the strictly nonzero
infinite source itself or prove a finite/native source-binding map.

## 5. Preparation, free input orbits and the concurrent Q8 result stay separate

The preparation theorem refers to the original cap2/CAR16/RIGHT128 channel,
its specified complete central reference and ledger, all given geometric
and material coordinates, and the selected `k` independent CAR directions.
Its exact center identity and local singular-entropy convexity eliminate
those relative preparation coordinates near the stated fixed-mesh base.
They do not eliminate a larger Stiefel/LEFT orbit or all possible
controller, selector, reference or work variables.

The displayed `M=p^3 P_b H_m` is the old mixed matrix **at the declared
matter-free base point**. On the general chart its exact underlying Ward
identity has coefficient `beta slack_w` and the corresponding differentiated
terms. The null-direction consequence concerns a true Hessian-kernel
vector, not every isotropic vector of an indefinite form. The original
material coordinates must remain independently varied as specified; a
constrained material waveform has a different tangent image.

The concurrently published cap-one owner requires fixed RIGHT, the stated
remaining price, no additional independent input-source term, and its
nonzero scalar price slope to derive `[E_y,rho]=0` on the full free LEFT
orbit. Since its query change has the commutator form, this screens the
query source there. The paid rank-two slice instead keeps a normal
constraint reaction. The synthesis correctly declines to transfer the
selected-direction cap2 elimination to this different full-orbit problem.

The Q8 append proves the representation/program transport of the existing
identity/order comparator to full CAR16. Its record effects are scalar
operators on CAR16; its apparatus still includes the arm, retained bit,
clock and program factors. Neither that transport nor the older faithful
CAR16 Spin representation supplies physical controlled-gate admission,
complete payment, a field pullback or a common Book03 source. The synthesis
states only the algebraic carrier repair and keeps those obligations open.

The incoming source texts were read directly. Exact bindings are:

| Incoming text at `afc4294f` | SHA256 | Git blob |
|---|---|---|
| `A4D_PHYSICAL_CAP1_EXECUTION_COMPOSITION_2026_10_21.md` | `6589f3dadfbc896752dab612d38be512c83bf5224f8ab5dc91db26513aebaaed` | `7047672e1500d43cf3678dab0f25bc461940184b` |
| `A4D_NATIVE_BOOK03_OPERATOR_VARIATION_BOUNDARY.md` | `d184ff7758b2ae4cc32d1bfdb6b07bb827d5e194a0e77a1030061df2e2cdf8ac` | `3a1202ab4e992efedf2228b3c03afac7238b1178` |
| `sources/d0_book03_car16_q8_order_2026-10-21/README.md` | `2bb8510087c005714ea732c350fec53ad8d3c959fb4e75cda83a9a0f1679ceb2` | `4e3996a9f43a07232d99a9dcc5f471894179e44d` |

These paths are relative to `02_REGISTRY/research/`. The first result was
introduced by `8463b0a4`; its text was read from the later `afc4294f` tree.
The two Q8 file copies supplied under `/tmp/d0_concurrent_inputs/` were
verified against their exact Git blob identities. This is consumption and
scope review, not a new independent replay of the Q8 checker.

## 6. Verification budget and remaining parent obligation

This integration review consisted of analytic checks, source reading,
exact byte/hash comparisons and review of the separate frozen reports.
The preparation packet has this reviewer's earlier independent 75-check
replay. The density packet has the other reviewer's independent 101-check
replay, including the strengthened Jacobi controls. The entropy packet has
its distinct independent reviewer and source-sign replay. Those reports
are retained; their empirical controls do not replace the analytical
arguments. No unchanged full spectral, geometry, compiler or Lean suite
was rerun for this document review, and no remote CI outcome is asserted.

The remaining parent substitution is one actual paid execution, its
admitted tangent map, its complete absolute price and its full internal
source at the relevant field root. The three new results remove specific
mathematical premises inside their own owners; they neither construct that
common execution nor solve all its remaining sources. The final synthesis
preserves `GR_closed=false`, the existing field-minimum exclusion, and the
open physical Book valuation, field admission, finite-to-continuum and
uniform-refinement obligations.
