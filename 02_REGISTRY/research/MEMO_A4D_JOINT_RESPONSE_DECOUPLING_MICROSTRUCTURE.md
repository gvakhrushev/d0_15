# A4D joint response decoupling — corrected Y normal-jet result

> **Finite normal-jet compatibility is certified; the nonlinear continuum gate remains open.**
>
> The physical TT-defect interpretation at `ea6e9d0` is superseded. Its mixed metric/connection Bloch placement was swapped. The corrected convention is connection-side `lambda^(-s)` and metric-readout `lambda^(+s)`, derived from the actual face-base and shifted-link placement. The flat `z=0` control could not detect the sign error.
>
> The corrected four-direction, 20-curvature normal-jet certificate now passes exactly. Full joint compatibility leaves one curved spatial direction, and imposing only fast-phase erasure makes its common metric response equal the independently constructed flat Einstein response. This is a finite normal-jet theorem, not a nonlinear or refinement-uniform theorem.

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
Execution: PR #310
Lifecycle: `IN_PROGRESS`; PR remains Draft
Action: unchanged naked star action; no selector, torsion equation, spectral filter, or added term.

## Inputs and response convention

The calculation consumes merged #216, #223, #226, #227, #232, #237, and #275. The exact merge commits are pinned in the execution history and task brief.

The target is the normalized response difference

`D_h(K_h) = h^-2 [E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)]`

for exact joint-critical sequences, with the #216 smooth branch evaluated on the same sampled smooth metric. The owner sum norm from #226 is the default for refinement claims. Comparing two exact solutions to the identical prescribed metric source is tautological and is not the source condition used below.

The exact #232 period-four Y family is a curved nongauge joint vacuum at the flat metric. It rules out a universal claim that every zero-residual connection lies in one smooth/LC-like fiber. The response question is whether its stationary center can remain compatible with a genuinely curved metric background.

The [quantitative pure-Y transport theorem](A4D_Y_PURE_CENTER_QUANTITATIVE_TRANSPORT.md)
now derives a nonlinear gradient estimate directly from two literal boost
Euler rows on each graph edge. It also reconstructs all 136 joint Euler rows
as fixed difference operators on two Cayley scalar functions and proves
`||R_Y(c)||_(p,comp) <= 1152 ||c||_infinity ||D_G c||_p`, with no lattice-size
constant. This refines the norm-only quadratic scaling objection for the
pure-Y interaction. It does not prove curved reduced-center solvability or
the required transverse size, and the actual owner sum-norm scaling must
still be discharged.

The [folded center-gradient module theorem](A4D_Y_CURVED_JOINT_CENTER_GRADIENT_MODULE.md)
recovers the 94 physical complement coordinates and the actual six center
graph differences by analytic combinations of the full joint rows near
every folded character. The local holomorphic module is 95 invertible
coordinates plus the four-character maximal ideal. If the joint symbol
has no other physical torus zeros, these identities glue to a smooth
multiplier with absolutely summable Fourier coefficients. This would
supply the unweighted owner sum-norm estimate and flat local nonlinear
joint rigidity modulo constant Y amplitudes, uniformly in L. The local
identity is proved; the all-torus rank premise and curved continuation
are not. Four short Laurent inverse templates are excluded over Q.

The [current mixed-current probe](A4D_H_NORMAL_RESCUE_CURRENT_PROBE.md)
organizes the remaining estimate around
`X_(h,p)=||w_tr||_(p,comp)+||D_G c||_p`.
The exact three-ratio finite convolution has only the folded interior
rank drop on periods 8, 12, 16 and 24, including every genuine
three-ratio character on those grids. A full-row-rank interior still
leaves 28 right-kernel directions. The continuous torus and full joint
boundary are not closed by this finite calculation.
Under the open torus premise, finite-stencil metric perturbation and
nonlinear absorption give
`X_(h,p) <= 2C [h^2||tau_h||_p + C_g||g-eta||_p]`
on a fixed small chart, in the actual specified norm. No separate
inverse loss acts on the center gradient. The numerical mixed fields
fail the necessary equations and are not joint witnesses.
Neither task terminal follows.

## Subsequence response law for small link-log deviations

There is a useful conditional homogenized statement before the global
realizability question is solved. It applies only to sequences in the common
local logarithm chart with

```text
Q_h(x) = g(hx),                 g fixed, smooth and nondegenerate,
A_h = log K_h,                 ||A_h||_infinity <= C h,
A_h^sm = log K_h^sm,           ||A_h^sm||_infinity <= C h,
b_h = (A_h - A_h^sm)/h,        ||b_h||_infinity <= C,
```

after fixing the same local Lorentz gauge slice for both fields. Assume the
prescribed source is fixed independently of the candidate branch,
`E_K(Q_h,K_h)=0`, and the **sitewise** source equation is
`E_Q(Q_h,K_h)=h^2*tau_h`, with `||tau_h||_infinity<=C` and `tau_h`
converging weakly to a smooth `tau`. This pointwise bound is an additional
hypothesis; weak convergence of the normalized response alone does not give
it. Assume also the #216 comparator has the stated reconstruction and the
**strong** residual/source bounds
`||E_K(Q_h,K_h^sm)||_infinity<=C*h^2` and
`||E_Q(Q_h,K_h^sm)||_infinity<=C*h^2`, with its normalized metric response
converging to `rho[g]`. These bounds must be checked for any proposed
smooth comparator; the conditional #216 normal rescue does not supply an
unconditional exact joint branch. Require `b_h` to converge weakly to zero.
If its macroscopic weak part is nonzero, an additional linear response term
remains and must be controlled separately.

Use the owner ten-component metric coordinates
`(00,01,02,03,11,12,13,22,23,33)` with its dual pairing, and the normalized
site pairing `h^4 sum_x` on the unit four-torus. The following is a
subsequential distributional law, not convergence in the stronger owner sum
norm. Every bounded sequence `b_h` has subsequential shift correlations
represented by a positive Hermitian `24 x 24` matrix-valued frequency
measure `mu_x(dz)`. Concretely, for every fixed lattice shift `r` and smooth
test `phi`, subsequential limits of the matrix products
`h^4 sum_x phi(hx) b_h(x+r) b_h(x)^*` are its shift-correlation moments.
Positivity follows by testing squared norms of finite linear combinations
of shifts; the uniform pointwise bound on `b_h` bounds the spatial trace
mass. The physical Fourier pairing, including real-field conjugacy, is the
one fixed by #216/#240.

Let `H_g(x,z)` be the physical connection Hessian symbol and let
`C_g(x,z)` be the physical connection-to-metric block (the adjoint of the
oppositely placed metric-to-connection block). Sitewise finite-stencil
expansion of the two Euler equations gives
`||H_g(T)b_h||_(2,h) = O(h)` and `||C_g(T)b_h||_(2,h) = O(h)`, where
`||v||_(2,h)^2=h^4 sum_x |v(x)|^2`. These are **strong** residuals: expand
the sitewise Euler equations about the comparator, divide their `h`-linear
terms by `h`, and use the uniform `O(h^2)` comparator and prescribed-source
bounds. Multiplication by a smooth test function commutes with each fixed
lattice shift up to `O(h)`. Positivity of the shift-correlation measures,
the strong residuals, and these commutator bounds therefore imply

```text
Ran mu_x(z) subset ker H_g(x,z) intersect ker C_g(x,z)
```

for almost every `(x,z)` with respect to `dx dmu_x`. This is a necessary
support condition; it does not assert that every positive measure satisfying
it is generated by exact nonlinear solutions.

The strength of this hypothesis matters. If one only has tested/weak
`H_g(T)b_h -> 0`, the support conclusion is false: on even periodic lattices,
`b_h(x)=(-1)^{x_0}` converges weakly to zero, while for the scalar operator
`H=I` its shift-correlation measure has nonzero mass at frequency `pi`,
outside `ker I`. A weakly smooth metric source may conceal such an
oscillatory `O(h)` raw response. The previous tested-only formulation of
this paragraph did not prove the stated support claim; the sitewise source
and strong-residual assumptions above are required.

For any smooth symmetric metric test field `q`, analyticity of the finite
stencil on the fixed compact chart gives the tested expansion

```text
h^-2 (E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm))
  = h^-1 L_h[b_h] + 1/2 R_{Q,h}[b_h,b_h] + O(h),
```

where `L_h` is the linear connection-to-metric term and `R_{Q,h}` is the
quadratic coefficient of that same metric variation. The leading Euler
constraints supply the two approximate-symbol equations above. For the
linear response, move the finite shifts in `L_h` onto the smooth test `q`.
The zero-frequency curl block vanishes, so its adjoint on `q` is `h` times a
smooth first-difference expression plus `O(h^2)`; after division by `h`, the
weak-zero condition on `b_h` kills this term. The remaining cross term with
`A_h^sm/h` has a smooth coefficient and also vanishes against `b_h`. The
uniform compact-chart Taylor remainder is `O(h)` after normalization. The
finite-shift quadratic term is exactly the term whose correlations converge
to `mu`; hence

```text
<tau - rho[g], q>
  = 1/2 integral_x integral_z
      tr(D_Q H_g(x,z)[q(x)] dmu_x(z)) dx.
```

The trace uses the Hermitian physical carrier and the owner metric-coordinate
pairing; no extra factor for a conjugate pair is inserted. The formula is
the controlled quadratic correlation defect, not an on-shell Ward identity.
The exact constant-solder `L=4` census in
[`A4D_JOINT_RESPONSE_SOLDER01_DEFECT_CENSUS.md`](A4D_JOINT_RESPONSE_SOLDER01_DEFECT_CENSUS.md)
verifies 1,602 nonzero frozen response moments in a predeclared 0/1 solder
class. Thus the support condition alone cannot force the integrand to vanish;
the census is tangent-level and does not show that any candidate measure is
generated by an exact sequence. The missing step is to identify which such
measures are realizable by the full coupled nonlinear Euler equations,
including the phase-resolved metric equations.
Moreover, weak distributional control alone does not imply the task's owner
sum-norm limit. The result narrows the closure problem but is not either
task-level terminal and does not cover sequences outside the `O(h)` log
chart.

## Corrected finite response across the four Bloch axes

`a4d_y_curved_response_phase_corrected_check.py` independently reconstructs the 96-by-96 connection Hessian and the 10-component low-color response with the corrected mixed phase convention. It verifies the submitted aggregate ledger in `a4d_y_curved_response_corrected_report.json` and writes `a4d_y_curved_response_phase_corrected_results.json`.

At `z=0`, the Hessian matches the owned #275 `L2/2` entry by entry, has rank 80 and kernel dimension 16, and reproduces the half-Einstein symbol on all four axes. At `z=1`, it has rank 94 and a two-dimensional center. The exact range and center equations pass for all four Bloch axes; the reduced center determinant for `e0` is `625/16287`.

For the 10-component metric perturbation shared across the four phases, the exact aggregate `q12` coefficients are:

| Bloch axis | Curved `q12` coefficient | Difference from flat | Rank of 10-by-10 defect |
|---|---:|---:|---:|
| `e0` | `-186451/236250` | `-34163/118125` | 6 |
| `e1` | `-2665927/85127280` | `-2665927/85127280` | 8 |
| `e2` | `-2665927/85127280` | `-2665927/85127280` | 8 |
| `e3` | `177811967/340509120` | `7557407/340509120` | 8 |

The averaged first-order response is zero in this ten-component reduction. The per-site `q12` arrays from the submitted JSON are retained for provenance, but this four-axis checker cross-checks only the aggregate fields. The separate normal-jet checker below supplies the phase-resolved compatibility calculation used for the finite theorem.

## Exact phase-resolved normal-jet compatibility at `z=1`

`a4d_y_curved_normaljet_compatibility_check.py` builds the 40-row phase-resolved metric equations and all four slow directions, then checks the exact ledger in `a4d_y_curved_normaljet_compatibility_results.json`.

The algebraic Riemann normal-jet space has dimension 20. The pure quadratic phase-resolved system has rank 10 on 40 variables; its kernel still projects onto all 20 curvature directions. After adding the four slow directions, connection Fredholm equations, phase-resolved first-slow metric equations, and spatial center gradients, the combined system has rank 43, nullity 5 on 48 variables, and curvature projection rank 1. The constant-order connection Fredholm condition is automatic on that kernel.

Impose only fast-phase erasure of the metric Euler output: the ten components must agree across all four fast phases, without prescribing their common value. This smooth-source system has rank 5, nullity 2, and still projects onto one curved direction. Only after solving these compatibility equations is the response compared with Einstein. The exact response difference has rank zero on the full smooth-source kernel.

With spatial bivector basis `(12,13,23)`, the surviving curvature operator, after the declared normalization, is

`-Y tensor Y`, where `Y=(1,-1,1)`.

The common metric response in coordinate order `(q00,q01,q02,q03,q11,q12,q13,q22,q23,q33)` is

`(3/2, 0, 0, 0, -1/2, -1, -1, -1/2, -1, -1/2)`.

The independently assembled flat Einstein control is exactly the same vector. The finite terminal is `A4D-Y-CURVED-NORMAL-JET-RESPONSE-COMPATIBLE`.

## Nonlinear status of the second connection-center mode

The exact checker `a4d_y_dual_center_joint_visibility_check.py` integrates the boost-dual connection-kernel tangent to a finite Cayley path at the `z=1` flat Y vacuum. All 96 connection Euler rows vanish identically on this path. Its ten Gram-response components are

`(0,0,0,0,-f,f,f,-f,f,-f)`

on fast phases 0 and 1, and the negative vector on phases 2 and 3, where `f=4d/(3d^2-4)`. The four-phase average is zero, but a smooth source requires fast-phase erasure and forces `d=0` near the origin. Thus the second connection-Hessian center is not an independent smooth-source joint modulus: it is connection-stationary and staggered-metric-visible.

### Fixed-solder joint tangent near the selected Y vacuum

There is a sharper finite-cell statement behind that visibility test. Let
`H(z)` be the 96-by-96 connection Hessian and `C0(z)` the full 40-by-96,
phase-resolved derivative of the metric Euler rows with respect to the
connection, both at the flat-solder period-four Y vacuum. The exact owner
calculation at `z=1` gives `rank H=94` and
`rank [H; C0]=95`. The exact Y-family tangent lies in the latter kernel, so
the fixed-solder linearized joint-critical connection space is exactly
one-dimensional: it is the tangent to the Y family. The boost-dual tangent
is removed by `C0`, and there are no other constant-cell transverse joint
tangents.

This statement persists on some open interval about `z=1`. The entries of
`[H(z); C0(z)]` are rational functions of the Cayley parameter. A 95-by-95
minor nonzero at `z=1` stays nonzero in a neighborhood, while the exact Y
family tangent supplies a kernel vector throughout that neighborhood;
therefore the rank remains exactly 95 and the kernel remains precisely that
tangent. This is an algebraic local-in-`z` consequence of the pinned ranks,
not a uniform estimate over Bloch momentum or refinement.

This also clarifies the limit of the transverse `K2` inertia result:
indefinite connection energy alone cannot supply a joint-critical branch,
because the full fixed-solder tangent at `z=1` has only the Y direction.
This still does not rule out a sourced
nonlinear continuation whose range correction has a transverse component,
or spatially varying/high-Bloch branches; those require the nonlinear
reduced equations and uniform remainder control.

## Quadratic symbol of the surviving center envelopes

The follow-up certificate `a4d_y_center_envelope_symbol_check.py` computes the exact quadratic symbol of the two-dimensional stationary center at `z=1`. The two components decouple at principal order. With `s=t1+t2+t3` and `r_perp^2=t1^2+t2^2+t3^2-s^2/3`, their symbols are

`S_Y(t) = -2/188307 * [26250*(t0-16*s/75)^2 - (2283779/2)*r_perp^2]`

and

`S_dual(t) = -1/6408 * [882*(t0-16*s/21)^2 - (603687/2)*r_perp^2]`.

These are two transported `2+1` hyperbolic envelope modes, not an elliptic range with a spectral gap. The exact symbol fixes the linear principal part only; nonlinear envelope existence, energy estimates, and uniform coupling to the transverse range remain open.

This low-frequency estimate also quantifies why the linear calculation does
not close the nonlinear branch. On a fixed periodic domain sampled with
`h=1/L`, the first nonzero slow covector has `|k|` proportional to `h`. The
one-column reduced symbol is `Gamma.k + O(|k|^2)` with `Gamma` injective, so
its smallest singular value on that mode is `Theta(h)` and its inverse is
`Theta(h^-1)`. A normal-chart smooth forcing of size `O(h^2)` can therefore
produce a center correction of size `O(h)`. A generic quadratic reduced
remainder is then `O(h^2)`; applying the same near-resonant inverse returns an
`O(h)` term, the size of the proposed correction. Thus this norm-only bound
supplies no small factor for a contraction. A continuation proof needs an additional
projected cancellation (for example, an `O(h^3)` nonlinear forcing on these
admissible modes), a tame estimate that closes without contraction, or a
different exact reduction. This scaling is a proof obstruction, not a
counterexample or evidence that a branch exists.

An exact nonlinear transport check now proves sign-free rigidity inside the
pure-Y ansatz. On each of the 12 phase/spatial-edge pairs, one boost equation
factors as `±8(a-b)(a+b)/((4+3a^2)(4+3b^2))`, forcing `a^2=b^2`. A second
boost component on the same edge evaluates at `b=-a` to
`±4*a*(3*a^2+4)/(4+3*a^2)^2`, which cannot vanish for real `a!=0`; when
`a=0`, the primary equation forces `b=0`. Therefore the pair forces `a=b`
for all real values. Since the six transport moves generate the connected
even-sum sublattice on periodic `L=4m`, every real pure-Y stationary amplitude
is constant there, without a fixed-sign assumption. Transverse/non-Y
corrections remain outside this exact ansatz result.

The norm-only quadratic bound is not sharp for every interaction. The new
exact certificate `a4d_y_center_wave_cubic_vertex_check.py` differentiates the
quadratic reduced center symbol along the exact boost-dual
connection-stationary path. For every shift pair `(i,j)`, the derivative of
the `Y,Y` entry in the dual direction is exactly zero. The checker first
reproduces the pinned two-center wave symbol and verifies that the first
constant-center cokernel row is the dual tangent; the corresponding
curvature-squared source remains the positive rational
`351402359/2108160`. Therefore a pair of opposite low-frequency `Y` waves
does not supply the leading quadratic term in that dual zero-mode equation,
even though dimensional counting alone allows an `h^4` contribution. This
is a real cancellation in the flat-background cubic vertex. The dual-dual
entry also vanishes; the mixed `Y`/dual entry is the only nonzero center pair
in this derivative. Under the owned smooth-source scaling the visible dual
amplitude has no `O(h)` term, so for an `O(h)` Y wave its mixed flat vertex
first contributes at `O(h^5)`, below the `O(h^4)` curvature source. This
rules out cancellation by these flat low-frequency center pairs under that
scaling. It does not control curved-background vertices, nonzero resonance
strata, aliases, or higher vertices.

## Joint first-slow reduction: the connection waves are constrained

The analytic follow-up [A4D_Y_JOINT_FIRST_SLOW_REDUCTION.md](A4D_Y_JOINT_FIRST_SLOW_REDUCTION.md) retains the full metric equations before treating the connection-center wave symbols. Its exact 40-by-5 first-slow map acts on `(d0 z,d1 z,d2 z,d3 z,b_dual)`. A five-row minor has determinant `-975737200/35590023`; the inverse minor has Frobenius norm less than 8. Thus the map has lower bound `||M v||_2 >= ||v||_2/8`.

For a flat metric and raw smooth source O(h^2), this forces a regular leading Y envelope to be constant and removes the order-h visible dual correction. Equivalently, the fixed-metric stacked joint Bloch derivative has an injective first-order center symbol in every nonzero real slow covector. Analytic range elimination yields `sigma_min J(i k) >= c |k|` locally near zero momentum. This is a derived local joint estimate, not an assumed elliptic connection gap and not a global Bloch bound. It does not extend to z=0 without another estimate.

Over the exact frozen constant-metric Y family, the same rank condition persists near `(eta,1)`. The leading nonlinear joint equations reduce to a constrained first-order system for the Y amplitude and metric gradients, with all residual compatibility equations retained. The follow-up also states an exact finite-lattice analytic range-reduction theorem with explicit contraction hypotheses and the first nonlinear joint cokernel equation. Those hypotheses have not been proved uniform under refinement.

A second exact certificate treats the genuinely curved product-plane seed `S=I+(f-1)P_perp`, with f time independent and constant along `(1,1,1)`. Commuting spatial spin links give exact sitewise metric-response erasure for the Y carrier, and all 96 connection coefficients through first slow order vanish without linearizing in f. The new independent-parameter face check verifies that inserting the boost dual `B` into any face with four independent Cayley Y parameters returns exactly `±B`; the exact temporal boost-dual row therefore remains `3 f(x)^2-sum_i f(x-h e_i)^2` even when the center amplitude `z(x)` varies from site to site. On a connected periodic spatial lattice this excludes every nonconstant f within this commuting Y seed class, including sitewise center retuning. It is not an obstruction to the full connection space: transverse/non-Y corrections remain essential.

The exact check `a4d_y_two_center_cartan_transport_check.py` adds a sitewise boost-dual center amplitude `d_x` to this transport row. For phase-0 role-0 links `C_Y(z_x) C_B(-d_x)` and phase-2 links `C_Y(z_x)^(-1) C_B(+d_x)`, the literal phase-0 `B`-variation row is

```text
E_(K0,B)(x) = (3*d_x^2+4)/(3*d_x^2-4) * (sum_i f(x-e_i)^2 - 3*f(x)^2).
```

The exact replay treats the incident temporal `z` and `d` amplitudes as independent symbols; the row loses every `z` and depends only on the boost amplitude at the tested link. Its coefficient is nonzero throughout the real Cayley chart `4-3*d_x^2 != 0`. The block split explains why arbitrary spatial Y-rotations leave this row unchanged: they act trivially on the boost-dual plane, while preserving the transverse Y-area paired with the boost variation. Because `f` is time-independent, every spatial site has a phase-0 temporal representative. On a connected periodic spatial torus, stationarity therefore makes `f^2` backward-harmonic; the finite maximum principle forces `f` constant. This rules out a curved product-plane stationary rescue within the commuting Y/dual-center ansatz, including sitewise center retuning. It does not rule out transverse/non-Y corrections or establish a task-level terminal.

### Off-shell phase partial versus the full joint Euler response

The `q01` row `-sigma(p)*h*z/(4+3*z^2)`, with
`sigma=(1,1,-1,-1)`, belongs to merged #241's **uncorrected**
microstructure on a valued slow coframe, compared there with the identity
connection. It is not a row of a jointly stationary `K_sm` from #216/#275.
At `z=h`, the sitewise normalized limit is `-sigma(p)/4`. Its four-phase
Fourier average at a *fixed slow coordinate* vanishes; only `k=1,3` remain.
That calculation alone proves neither a persistent high-Bloch defect on a
joint branch nor an all-order Einstein identity for its phase-common part.

Even within the #241 off-shell profile, a physical four-site average
depends on how the slow coordinate is sampled. On consecutive time sites
with `x0=p`, its `q12` slope row is
`-sigma(p)*h^2*p*z/(4+3*z^2)`. The four-site mean is exactly
`h^2*z/(4+3*z^2)`, hence `h/(4+3*h^2)` after `h^-2` normalization at
`z=h`. Freezing the slow coordinate before the phase DFT is a different
projection from taking this finite four-site mean.

Merged #275 instead completes the same valued affine coframe with an exact
connection lift. Its full Euler replay has all 96 connection and 64
unrestricted solder rows zero, and hence all 40 phase-resolved Gram rows
zero. Its varying metric is macroscopically flat. This exact control blocks
the inference that #241's off-shell high-Bloch row survives the joint lift;
it supplies no all-order finite-`L` Einstein identity on a curved product.
The #310 normal-jet match is `r=G_standard[J]/2=-K_Schur[J]` on one
linear curvature direction, with a phase-common degree-two obstruction
`-22209*kappa^2` for nonzero curvature. In merged #273, `det A0=256` for
the generic connection block; the four diffeomorphism directions are in
the Schur metric symbol's kernel, not `ker A0`.

The exact `delta^2` normal-jet forcing has now been evaluated in
`a4d_y_curved_normaljet_degree2_obstruction_check.py`. The 96 connection
equations admit a rational local jet through normal degree four. Before
allowing a spatially varying center, its two zero-momentum connection-cokernel
components are exactly
`(351402359/2108160, 21506403637/154949760)`; the exact quartic center jet
transports the negative vector and solves all 96 local Taylor equations.
These components are independent of an arbitrary first-order constant Y
retuning `s`.

The same calculation gives a different, joint conclusion: after eliminating
the connection range and allowing all 20 degree-three center coefficients,
the `xi3^2` phase-common metric witness pairs to `-22209`. The symbolic
family replay proves this pairing is independent of the same constant
retuning `s`. Since this is an exact identity in `s`, it covers any bounded
sequence `s_h`, including nonconvergent and nonanalytic dependence on
refinement: the tracked order-`delta^2` source is unchanged at each `h`.
Constant center drift on this scale therefore cannot cancel the obstruction.
This does not cover unbounded retunings, whose higher powers may change the
asymptotic ordering, spatially varying center fields, nonzero Bloch modes, or
the global finite-lattice branch. Thus this normal jet cannot have exactly
phase-common metric readout at order `delta^2`, even though its connection
equations solve.
For the connection-solved local profile, the phase-difference coefficient
has the exact cell bound `11000*delta^2`; for bounded `kappa` this is
`O(h^4)`, or `O(h^2)` after the task normalization. It is therefore a
finite source-compatibility obstruction, not a nonzero normalized response
gap. Neither calculation constructs an exact finite-lattice joint branch.

### Periodic mean obstruction for a regular Y-sheet branch

The local geometric input to a possible periodic Fredholm test is now
certified independently in
`a4d_y_variable_curvature_normal_jet_check.py`. For the product's two-
dimensional factor, the radial Jacobi equation gives, in geodesic-normal
coordinates and the pinned convention `K=3*kappa`,

```text
Q_h-eta = h^2*kappa*T(xi)
        + h^3*(grad(kappa) dot xi)*T(xi)/2
        + h^4*[-2*kappa^2*|xi|^2/5
              + 3*Hess(kappa)(xi,xi)/20]*T(xi)
        + O(h^5),
T(xi)=|xi|^2 I-xi xi^T.
```

The regular-branch mean argument is now recorded in
`a4d_y_periodic_regular_branch_mean_check.py`. Under its explicit hypotheses
(global owner product framing, periodic real `C^4` curvature, joint first-slow
constraints, a uniform integer-power expansion through `h^4` with bounded
`C^4` coefficients and `O(h^5)` remainder), first-slow injectivity kills the
order-`h` nonconstant Y envelope and visible dual component. The pointwise
order-`h^2` Y retuning may vary, but the exact family certificate is
independent of its value; its derivatives enter only later. Summing the two zero-momentum connection
cokernel equations kills periodic shift differences; the linear
`Hess(kappa)` term has zero mean, while the quadratic order-`h^4` source is
`kappa^2`. The exact family certificate makes its coefficients independent
of the retuning, giving
`(351402359/2108160, 21506403637/154949760) * mean(kappa^2) = (0,0)`.
The positive coefficients force `kappa == 0` for any branch satisfying those
regularity hypotheses.
The replay checker verifies the pinned local coefficients, the normal-metric
jet, and the periodic shift identity; the global identification of all
order-`h^4` transport terms with shift differences is the analytic step in
this memo, not a separate full finite-lattice Euler assembly in the JSON.
Here `kappa` is the fixed, h-independent curvature profile of the sampled
background. If the background itself is a family `kappa_h` with an
integer-power expansion, the order-`h^4` mean equation constrains its
leading curvature coefficient only. For example, `kappa_h=h*kappa_1` is not
excluded at order `h^4` by this identity. The exact-zero conclusion must
not be applied to every h-dependent background merely because its expansion
uses integer powers.

This closes the periodic-mean route for regular integer-power branches on the
`z=1` Y sheet. It is not an exact finite-lattice continuation theorem: a
nonanalytic or nonuniform refinement-dependent center correction may enter
at the same order. It gives no task-level response gap and does not close the
global uniform gate.

The phase-common metric obstruction itself is homogeneous in the curvature
amplitude: the exact `-22209` and `-166034484` pairings become those constants
times `kappa^2`. At generic regular `z`, the exact rank jump at `z=1` also
implies a degree-two obstruction outside a finite algebraic exceptional set,
because the reduced matrices are rational in `z`. Neither deduction
identifies exceptional `z` values or rules out a singular `h`-dependent
center correction of the same order.

Because `z=1` is itself regular and obstructed, the finite exceptional set is
separated from `1` on this chart. Every refinement-dependent constant
retuning `z_h -> 1` therefore remains obstructed at the same degree-two
normal-jet level for all sufficiently small `h`, with no integer-power
assumption on the rate. This does not cover a spatially varying center,
nonzero Bloch modes, or the omitted-order remainder of an exact branch.

## Small-amplitude splitting at zero slow momentum

The exact checker `a4d_y_small_amplitude_kernel_splitting_check.py` reduces the flat 16-dimensional connection kernel twice. The effective ranks through order six are `(0,0,12,12,14,14,14)`. The leading order-two Schur block has exact inertia `(4 positive, 8 negative, 4 zero)`, so it supplies no positive-definite energy on the full transverse sector. After this block, four directions remain; the reduced order-four and order-five blocks vanish, while the order-six block is `diag(0,0,9/8,3/8)`. The final kernel consists of the exact Y and boost-dual center tangents. Twelve transverse modes lift at order two, two soft modes at order six, and the worst inverse loss is `O(z^-6)`. This exact zero-momentum splitting identifies both indefiniteness and the small-amplitude conditioning that a nonlinear uniform estimate must control; it is not itself an `h`-uniform continuation theorem or evidence that the negative directions satisfy the full joint metric equations.

## Site-resolved source response on a 37-dimensional compatibility class

The follow-up certificate `a4d_y_phase_resolved_compatible_response_check.py` builds the 40-dimensional, four-phase metric-source problem for the `e0` axis at `z=1`. The exact zero-order and first-order Fredholm maps have ranks 1 and 2, so their common kernel has dimension 37. Solving the range and two center equations through second order gives a defect of rank 8 on this class. Its averaged first-order response has rank 4 on the full class but vanishes on the phase-independent ten-dimensional source subspace. The phase-independent second-order defect has rank 6 and reproduces the previously pinned `q12` value `-34163/118125`.

The 10-by-40 defect matrix extends the map from the compatible class by Euclidean orthogonal projection; the checker states this convention explicitly. It is a finite source-response calculation, separate from the curvature normal-jet system, and does not alter the latter's Einstein match after spatial center-gradient and fast-phase-erasure constraints. The submitted value `2626083/44800` lacks a specified source vector/projection in the provided package and is not treated as verified.

## Phase-independent single-source curvature witness

The exact checker `a4d_y_singleq_curvature_witness_check.py` verifies that the phase-independent `R^10` metric source has zero order-zero and order-one connection cokernel ranks at both the flat and `z=1` curved vacua. For the `q12` source, the corrected center amplitude is `(-3311/3750,0)` and the exact second-order defect has rank 6 with coefficient `-34163/118125`.

The reported sparse 10-by-10 jet matrix lies in the image of the exact 20-dimensional algebraic Riemann normal-jet map. Its Frobenius pairing with the single-source response defect is `-27247/17500`. This establishes a finite nonzero pairing for the single-axis response. The witness has not been shown to satisfy the full coupled spatial-center and fast-phase-erasure constraints; the full normal-jet certificate still leaves only `-Y tensor Y`, with the Einstein response. The pairing does not establish a physical no-go or a nonlinear branch.

The latest submitted report additionally claims rank 4 for a response-defect map over all 20 Riemann jets. Its JSON provides one witness jet and a nonzero scalar pairing, but no full response-by-curvature matrix or replayable rank certificate. The six nonzero pairings in the witness checker are basis-coordinate pairings, not that matrix rank. Treat rank 4 as unverified until its defining map is supplied; it is a different quantity from the certified rank-6 single-q defect and the rank-1 curvature projection after full normal-jet compatibility.

## Reproduction

From the repository root, run:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_response_phase_corrected_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_dual_center_joint_visibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_pure_center_transport_check.py
python3 02_REGISTRY/research/certificates/a4d_y_center_envelope_symbol_check.py
python3 02_REGISTRY/research/certificates/a4d_y_center_wave_cubic_vertex_check.py
python3 02_REGISTRY/research/certificates/a4d_y_small_amplitude_kernel_splitting_check.py
python3 02_REGISTRY/research/certificates/a4d_y_phase_resolved_compatible_response_check.py
python3 02_REGISTRY/research/certificates/a4d_y_singleq_curvature_witness_check.py
python3 02_REGISTRY/research/certificates/a4d_y_joint_first_slow_injectivity_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_mu4_locus_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_torus_lipschitz_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_folded_range_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_quarter_spatial_diagonal_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_symmetry_check.py
python3 02_REGISTRY/research/certificates/a4d_y_product_plane_seed_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree2_obstruction_check.py
python3 02_REGISTRY/research/certificates/a4d_y_stationary_center_family_coker_check.py
python3 02_REGISTRY/research/certificates/a4d_y_variable_curvature_normal_jet_check.py
python3 02_REGISTRY/research/certificates/a4d_y_periodic_regular_branch_mean_check.py
```

The first command verifies the four-axis aggregate, exact center/range solves, three direct rational Schur controls, and a hostile swapped-phase control. The second verifies full curvature normal-jet compatibility and Einstein response. The next four verify dual-center source visibility, the hyperbolic center symbol, the new cubic vertex, and the zero-momentum small-amplitude splitting. The subsequent pair verify the 37-dimensional site-resolved class and the phase-independent single-source curvature witness. The next two verify joint first-slow injectivity and the nonlinear product-plane seed identities. The following pair verify the exact `delta^2` connection/metric normal-jet system and its invariance under arbitrary constant first-order Y retuning. The next command derives the variable-curvature Riemann-normal metric jet and checks its constant-curvature specialization against that owner. The final command replays the exact amplitude law, first-slow injectivity, and periodic shift identities used by the regular-branch mean obstruction. Each checker compares its result with a pinned JSON. The old `a4d_y_curved_response_quotient_check.py` and its output remain historical regression material; its `ea6e9d0` TT-defect interpretation must not be used.

The submitted aggregate JSON has SHA-256 `79e6db7d96a0863a6af56e94752d080d5505a7fc47a307b752269dd092c4e230`. Its per-site `q12` arrays are not separately asserted by the aggregate checker.

## Exact curved joint Bloch control near the folded Y locus

Three exact owners now replace the earlier numerical full-joint scout in the
part of Bloch space they cover.

1. `a4d_y_curved_joint_mu4_locus_check.py` evaluates the literal
   `136 x 96` joint symbol on all 256 characters of `mu_4^4`.  Exactly
   252 have full column rank 96.  The only rank drops are the four diagonal
   folded points `(lambda,lambda,lambda,lambda)`,
   `lambda in {1,i,-1,-i}`; each has exact rank 95 and nullity one, and
   phase unfolding identifies all four kernels with the same constant
   Y-center.

2. `a4d_y_curved_joint_torus_lipschitz_check.py` certifies the exact
   21-term nearest-difference Laurent support and the global unit-torus bound

   ```text
   ||Q(theta)-Q(phi)||_2 <= (22/7) sum_j |theta_j-phi_j|.
   ```

3. `a4d_y_curved_joint_folded_range_check.py` fixes a 95-dimensional
   transverse Lyapunov-Schmidt chart at the folded point.  Deleting the
   phase-0 Role-0 `J13` coordinate and selecting the pinned 95 output rows
   gives an invertible `95 x 95` minor.  Its exact inverse Frobenius norm
   squared is

   ```text
   1449607289608826796462600607206428282020098585931893046315145431
   /1525932452501592103567428379487267246378717660095190382527232
   ```

   and is strictly below `31^2`.  A stronger exact rational Collatz
   certificate for `H=M^{-T}M^{-1}` has maximum weighted row ratio
   `39324659450219131318503292696502016712938627281350055258788171173083
   /100748164243965117045935891327267332674908454790124849815977965568
   < 400`, hence `||M^{-1}||_2 < 20`.  Entrywise diagonal phase covariance
   `Q(z,z,z,z)=D_out(z) Q(1,1,1,1) D_in(z)` for `z^4=1` transfers the
   same operator bound to all four folded copies.  Combining it with the
   `22/7` Lipschitz owner gives a uniform Neumann chart on every folded
   `l1`-angular ball of radius `7/880`, with transverse inverse norm
   strictly below 40.

This is the first rigorous transverse range estimate around the physical
folded center.  It is local.  The complement of those four balls on the
physical unit torus is still missing an exact full-rank cover or equivalent
algebraic certificate, and the reduced nonlinear Y-center equation on a
genuinely curved metric remains open.

## What is and is not settled

The finite claim that a nonzero Y microstructure necessarily induces a different smooth metric response is false on the corrected compatible normal-jet subspace: its sole curved linear direction has the Einstein response after phase erasure. This is stronger than comparing two solutions with an already prescribed common source.

The following boundaries remain:

- #232 is still a curved nongauge joint vacuum at the flat metric.
- #227 is connection-stationary but is not a joint-critical metric counterexample.
- The corrected normal-jet certificate is finite and linear in the sampled curvature jet.
- No exact finite-lattice joint-stationary branch over a genuinely curved sampled metric is constructed here; only the stated local normal jet is solved on the connection side.
- No refinement-uniform `o(h^2)` response remainder is proved here.
- No global selector or task-level no-go is established.

## Remaining global gate

The variable-curvature derivative-jet reduction and the regular periodic-mean obstruction are now certified. The regular integer-power `z=1` branch is excluded for nonflat periodic product curvature under the stated uniform `C^4`/`O(h^5)` hypotheses. The remaining gate is to control or construct nonanalytic or nonuniform h-dependent center/transverse branches under the fixed source convention, with the phase-resolved metric equations retained. The first-slow metric constraints must remain imposed; the two connection-only hyperbolic symbols are not free joint envelopes. Only after this singular branch-or-obstruction gate can one prove the refinement-uniform estimate

`|E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)| = o(h^2)`

in the owner topology, including almost-resonant complements and the allowed stationary-center amplitudes. A finite jet theorem alone does not close the task.

Keep PR #310 Draft and the task `IN_PROGRESS` until the nonlinear continuation and uniform remainder are proved or refuted. Do not claim either global terminal:

- Positive: `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED`.
- Negative: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.

### Supersession note on the historical degree-two obstruction

The older `-22209*kappa^2` and related phase-common degree-two obstruction
belongs to a more restrictive formal continuation ansatz and must not be
used as the current terminal for the surviving Y curvature.  The corrected
phase placement in the full 40-row, four-direction normal-jet owner leaves
one curvature direction, `-Y tensor Y`, and after imposing only
fast-phase erasure its common metric response is exactly the independent
Einstein control.  Thus the current finite terminal is

`A4D-Y-CURVED-NORMAL-JET-RESPONSE-COMPATIBLE`.

The historical obstruction certificates remain useful regression data for
their declared restricted ansatz, but they do not exclude the corrected
phase-resolved compatible jet and they do not prove a nonlinear no-go.

The remaining Y-sheet problem is therefore sharper.  Near each folded
character the 95 transverse variables now have an explicit uniform
Lyapunov-Schmidt inverse on the certified radius `7/880`.  The first
missing spectral step is the exact regular-complement theorem on the rest of
`(S^1)^4`.  The first missing nonlinear step is to solve or obstruct the
reduced center/compatibility equations for a genuinely curved sampled metric,
with estimates uniform under refinement.  Only after those steps can the
owner-topology `o(h^2)` response statement, or an admissible response-gap
counterexample, be promoted to a task-level terminal.

The exact [designated-germ normalization and tower audit](A4D_DESIGNATED_GERM_SCHUR_NORMALIZATION_AUDIT.md)
contracts #273's independent Schur/Einstein symbol with the **same** normal
Hessian as this task's pinned #310 response. On that input the response is
`K_G[J]/2 = -K_Schur[J]`, so an unqualified equation
`E_Q=G=-2*K_Schur` is not the owner normalization. The audit also identifies
why the regular periodic mean certificate cannot be promoted to an exact
every-period tower identity by zero-padding means or invoking M1, and why
the #216 coupled normal rescue is not supplied by #275's macroscopically
flat exact Y lift. Neither task-level terminal is changed.


## Exact temporal SO(3)-spin product rigidity

The scoped result in
[`A4D_Y_TEMPORAL_SPIN_PRODUCT_RIGIDITY.md`](A4D_Y_TEMPORAL_SPIN_PRODUCT_RIGIDITY.md)
extends the product-plane transport test from separate spin axes to an
arbitrary simultaneous real spatial rotation
`R=a J12+b J13+c J23` on the curved temporal links, together with the
independent boost-dual amplitude `d`.  Exact elimination of the three
role-0 boost Euler rows leaves the nonnegative multiplier

`3*d^4*(a-b+c+3)^2 + 4*(a-b+c-4)^2`.

Its only real exceptional locus is `d=0, a-b+c=4`.  There the nine
spatial-role rotation Euler rows have exact rank 3 on
`(f0,f1,f2,f3)` and kernel `span(1,1,1,1)`.  Hence both the generic and
exceptional cases force the product profile to be constant on a connected
periodic spatial carrier.  Replay with
`python3 02_REGISTRY/research/certificates/a4d_y_temporal_spin_transport_check.py`.

This is not a full transverse theorem: spatial links are fixed to identity
in this certificate.  Under the corrected phase-resolved normal-jet owner,
the remaining loophole is singular/refinement-dependent high-Bloch
spatial-transverse correction, not the historical restricted degree-two
obstruction.  A numerical
full-joint singular-value scout suggests that, after the folded Y-center is
separated, the next singular value stays near `0.1128`; that observation is
diagnostic only.  The required next theorem is an exact all-Bloch lower bound
on the transverse complement plus a uniform nonlinear remainder estimate.


## Current-frontier override: corrected normal jet and folded transverse range

This section is the controlling interpretation for subsequent work.  Earlier
sections that discuss the phase-common `-22209*kappa^2` degree-two witness
record the historical formal-jet route and must not be read as overriding the
later corrected phase-resolved normal-jet owner.  The current owner
`a4d_y_curved_normaljet_compatibility_check.py` leaves the single physical
curved direction `-Y tensor Y` after the stated compatibility/phase-erasure
conditions and matches the independently normalized Einstein response there.
Accordingly, no task-level no-go may be inferred from the historical
phase-common obstruction alone.

The local high-Bloch transverse loophole at the four folded Y characters is
now quantitatively reduced.  The exact owner
`a4d_y_curved_joint_folded_range_check.py` builds one 95-by-95
Lyapunov-Schmidt range chart for the full 136-by-96 curved joint Bloch symbol.
It proves entrywise diagonal fourth-root covariance

`Q(z,z,z,z) = D_out(z) Q(1,1,1,1) D_in(z)`,  `z^4=1`,

so the same chart applies at all four folded copies.  After deleting the
phase-0 role-0 `J13` coordinate, which is nonzero on the exact Y kernel, the
selected minor has rank 95 and

`||M_*^{-1}||_F < 31`.

The stronger rational Collatz bound on `M_*^{-T}M_*^{-1}` gives

`||M_*^{-1}||_2 < 20`.

Together with the independently certified global unit-torus bound

`||Q(theta)-Q(phi)||_2 <= (22/7) sum_j |theta_j-phi_j|`,

the Neumann estimate gives, for l1 angular distance at most `7/880` from
any folded point,

`||M(theta)^{-1}||_2 < 40`.

Thus the 95 transverse connection coordinates are uniformly solvable in an
explicit neighbourhood of every folded Y copy; the remaining equations are
the reduced compatibility/center equations.  This is a local range theorem,
not an all-Bloch theorem and not nonlinear reduced-center solvability.

A further exact stratum theorem removes the continuous metric-block rank-drop
line that passes through these folded points.  The owner
`a4d_y_curved_joint_quarter_spatial_diagonal_check.py` considers

```text
lambda0 = zeta in mu4,
lambda1 = lambda2 = lambda3 = x in C^*.
```

For `zeta=1`, augmenting the 95 folded-range rows by connection rows 4 and
15 gives two 96-by-96 minors.  After clearing the common denominator 14,
their Laurent determinants are reconstructed exactly by 256-root finite-field
DFT and 25-prime CRT.  A Hadamard/Cauchy coefficient bound makes the centered
CRT reconstruction unique; after removing Laurent units and integer contents,
both primitive polynomials have degree 94 and their exact gcd in `Z[x]` is

```text
x - 1.
```

Therefore the full joint symbol has rank 96 for every complex `x != 1` on
this entire stratum.  The entrywise fourth-root covariance is actually global,

```text
Q(zeta * lambda) = D_out(zeta) Q(lambda) D_in(zeta),  zeta^4 = 1,
```

so the result transfers to every quarter-temporal copy: the unique rank drop
on `lambda0=zeta, lambda1=lambda2=lambda3=x` is `x=zeta`.  This removes a
whole continuous exceptional layer, not merely sampled characters.  It still
does not classify the rest of the four-dimensional unit torus.

The exact symmetry owner
`a4d_y_curved_joint_symmetry_check.py` further reduces any global physical
cover.  It certifies, entry by entry on all 2,988 nonzero Laurent
coefficients:

- common quarter covariance
  `Q(zeta*lambda)=D_out(zeta) Q(lambda) D_in(zeta)`, `zeta^4=1`;
- the full spatial `S3`: the even generator is the cycle
  `1->2->3->1`, while the odd generator `2<->3` is accompanied by
  fast-phase `p->p+2`, which restores the background after `Y->-Y`;
- physical inversion `theta->-theta`, since all Laurent coefficients are
  rational-real.

Rank and singular values are therefore constant on a generic physical orbit
of size 48.  This does not itself supply the missing compact-complement
certificate, but it reduces the domain that such a certificate must cover by
the exact discrete symmetry group rather than by heuristic identification.

The active linear gap is therefore split cleanly into two pieces:

1. folded neighbourhoods: transverse range is now exact and quantitative;
2. compact complement of those neighbourhoods: an exact no-extra-zero /
   positive-gap certificate is still required.

After the complement is closed, the remaining nonlinear gate is the reduced
Y-center equation on genuinely curved sampled metrics, with a
refinement-uniform relative remainder in the owner topology.  The exact
macroscopically-flat Y lift remains a positive all-order control but does not
settle that genuinely curved reduced equation.

Keep #310 Draft / IN_PROGRESS.  Neither task-level terminal is promoted by
this local range theorem.


### Exact three-prime modular elimination on the representative two-ratio plane

The zone-folding reduction has now been pushed beyond one-ratio slices.  On

`rho0=1, rho1=x, rho2=y, rho3=1`

the owner
`a4d_y_curved_joint_two_ratio_modular_check.py` uses the 68 interior
(connection+metric) rows in fast phases 1 and 2 and four fixed 68-column
charts.  After multiplying each selected entry by `14*x*y`, every matrix
entry has bidegree at most two.  Integer assignment bounds certify finite DFT
windows for each determinant before any interpolation is performed.

For each of the three independent good primes

`664448401, 996672601, 1328896801`

the four bivariate determinants are reconstructed exactly over `F_p`.
Pairwise Sylvester elimination in `y` gives resultants of degrees
`2576` and `2742`.  Their exact polynomial gcd is

`x^229 * (x-1)^11`.

The factor `x^229` is a Laurent-clearing unit on the algebraic torus.
At `x=1`, the exact gcd of all four determinant restrictions in `y` is

`(y-1)^3`.

Hence for every pinned prime, on `(Fbar_p^*)^2` the common zero-set of
these four interior minors is exactly `(x,y)=(1,1)`.  This agrees with the
owned first-slow projective isolation and the exact one-ratio slices, but is
strictly stronger than either finite torsion sampling or a local Taylor
statement.

The scope fence is important: agreement at three good primes is an exact
finite-field terminal, not yet a characteristic-zero elimination theorem.
The next algebraic gate is to lift this two-ratio resultant/gcd statement to
`Q` (for example by a degree/leading-coefficient preservation plus modular
coprimeness argument, or by a bounded CRT reconstruction of the needed
univariate resultant cofactors).  Only after that should the genuinely
three-ratio interior locus be attacked.  No all-Bloch or task-level response
terminal is promoted here.

### Characteristic-zero two-ratio lift: exact structural divisor and reduction

The characteristic-zero gate in the preceding modular section is now closed
for that same representative plane. The integer-minors owner reconstructs
and saves all four exact coefficient ledgers, using 15 CRT primes per chart
and an independent prime replay. The new owner
`a4d_y_curved_joint_two_ratio_charzero_check.py` proves

`gcd_Q[x](R_01,R_23) = x^229*(x-1)^11`.

This is a reduction-lemma proof, not an inference from three matching primes.
Exact assignment duals give x=0 orders at least 229 and 259. Rational local
Sylvester Schur complements at x=1 have pivot orders `(1,2,3,5)` and
`(3,5,7)`, so both resultants have the required exact common divisor.
An infinity assignment normalization, constant rank 71, and zero first
null-vector pairing prove `deg R_01 <= 2576`; the nonzero modular degree
2576 then certifies degree preservation. The modular gcd at just one prime
now bounds the primitive characteristic-zero gcd degree by 240, equal to
the already proved structural divisor degree.

The exact x=1 fiber gcd is `(y-1)^3`, and the independent y=1 fiber gcd is
`(x-1)^3`. Consequently the four-minor common zero-set on `(C*)^2` is
exactly `(1,1)`. The literal interior operator has rank 65 at that point
and full row rank 68 elsewhere on this plane.

The detailed proof is in
`A4D_Y_CURVED_JOINT_TWO_RATIO_CHARACTERISTIC_ZERO.md`; the exact ledger and
lift results are pinned in their certificate JSONs. The new terminal is
`A4D-Y-CURVED-JOINT-TWO-RATIO-CHARACTERISTIC-ZERO-ELIMINATION-CERTIFIED`.
The genuine three-ratio interior locus, remaining boundary equations, and
the quantitative all-Bloch gap remain open. Nonlinear reduced-center
solvability and the normalized owner-topology response estimate are also
open. Keep #310 Draft / IN_PROGRESS.

### Explicit folded isolation radius

The local folded graph chart now has a conservative quantitative radius.
`A4D_Y_CURVED_JOINT_FOLDED_EXPLICIT_RADIUS.md` proves, for any of the four
folded characters and angular `L1` distance `0<delta<=10^-8`, that
`sigma_min Q(theta)>delta/20150`. This combines the owned chart inverse
and reduced four-angle derivative inverse with the global Laurent
derivative envelope; the new lightweight certificate checks the exact
kernel, phase covariance, and all rational constants. This excludes
additional joint zeros in four explicit punctured neighborhoods only. The
compact complement, nonlinear center equation and response remainder
remain open.

### Exact common-phase boundary line

`A4D_Y_CURVED_JOINT_COMMON_PHASE_BOUNDARY.md` now proves the full joint
rank on `lambda0=lambda1=lambda2=lambda3=mu in C*`, not just on a finite
torsion grid or the physical circle. Zone folding leaves a 68-row
phase-1/2 interior block of rank 65 and a 31-column boundary reduction
over `Q[w]`, `w=mu^4`. Two exact 31-by-31 minors have monic gcd
`w^23*(w-1)`. Therefore the joint rank is 96 for `mu^4!=1` and 95 at
the four folded points. This closes the nonfolded common-phase boundary
question on that line only. Genuinely three-ratio characters, the compact
regular complement, nonlinear center equations and response remainder
remain open.

### Quantitative nonlinear Y transport and the center remainder

The new owner
`a4d_y_pure_center_quantitative_transport_check.py` establishes the exact
all-row identity

`E_Y(a)=T_u u(a)+T_v v(a)`, `T_u 1=T_v 1=0`,

where `u(a)=4a/(4+3a^2)` and `v(a)=2a^2/(4+3a^2)`. The rational ledgers
have 84 and 108 nonzero coefficients, with total absolute sums 42 and 72.
All 136 derivative components agree coefficientwise with the existing
Bloch owner. An independent nonconstant rational field reproduces every
component using literal inverse-plaquette and unrestricted solder variation.

On each of the six even-carrier graph moves, two boost rows satisfy
`du^2+3dv^2=16(a-b)^2/[(4+3a^2)(4+3b^2)]` and control this chord by six
times their squared Euclidean norm. Hence for `|a|,|b|<=3/2`,

`|a-b| <= 7 sqrt(e_P^2+e_S^2)`.

On a periodic `L in 4N` carrier this yields
`osc(a) <= 28 L max_selected_pair sqrt(e_P^2+e_S^2)`. Thus a pure-Y
sitewise connection residual O(h^2), h=1/L, forces amplitude oscillation
O(h), without first imposing a smooth envelope.

The exact coefficient sums give the nonlinear derivative cancellation:

`||E_Y(z0+c)-D E_Y(z0)c||_(p,comp) <= 1152 ||c||_infinity ||D_G c||_p`.

For the metric rows the constant is 81. The statement holds in physical
space for `1<=p<=infinity`, with or without constant site weights, on the
fixed compact amplitude chart. If the actual gradient norm is O(h^2) and
the amplitude is O(h), this remainder is O(h^3). A pointwise scaling cannot
be substituted for the unweighted owner sum-norm hypothesis. The accompanying
memo also gives the analytic mixed bound with arbitrary small connection
corrections, but does not prove that those corrections are O(h^2) on curved
sampled metrics.

Finite terminal: `A4D-Y-PURE-CENTER-QUANTITATIVE-TRANSPORT-CERTIFIED`.
The first continuation obligation remains a refinement-uniform estimate for
the genuinely curved range and reduced compatibility equations. The full
Bloch compact complement remains open, and neither physical task terminal
is promoted. Keep #310 Draft / IN_PROGRESS.

## Current frontier: local joint module and the sum-norm bridge

The center-gradient module owner proves a local analytic normal form for
the entire joint symbol: 95 invertible coordinates plus the four-character
maximal ideal. It divides the physical target containing all 94 complement
coordinates and all 12 phase-resolved graph rows by the full joint symbol.
The target has complex rank 96 except at the four folded characters, where
it has rank 95 and the same Y kernel.

Under the open all-torus rank premise, gluing the divisions gives a smooth
multiplier with an absolutely summable Fourier kernel. Periodization
proves a component-sum l^p estimate for the complement and center gradient,
including the unweighted owner sum norm at p=1, independently of L. The
derivative remainder then yields flat local joint rigidity modulo constant
Y amplitudes in a fixed chart. These global and nonlinear conclusions are
conditional; the torus premise is not verified.

The exact checker excludes inverse supports of 9 and 21 monomials and the
full l1 shift balls of radii two and three. The last exclusion uses only
the phase-0 sector; no rank for its other sectors is asserted. Full modular
column rank and maximal augmented rank prove the exclusions over Q.
They do not refute a longer inverse or an analytic physical estimate.

The recovered source and compact ledger were independently replayed
locally. GitHub guards at `14bdb90` completed with success in run
`36718097905`, including the research certificates.
First remaining linear premise: full joint rank on the physical compact
complement of the four folded points. Curved reduced compatibility and
the actual owner sum-norm response remain the subsequent obligation.
No physical terminal, selector, action modification, or claim promotion.
Keep PR #310 Draft and IN_PROGRESS.

## Current execution focus: H-NORMAL-RESCUE

The first remaining object is the size of the genuinely mixed transverse
current on the sampled smooth metric, with the source and unweighted
owner topology fixed. Pure Y is an exactly controlled difference current;
its derivative remainder does not justify a separate new branch.
The finite three-ratio convolution and residual-qualified numerical
probe are recorded in `A4D_H_NORMAL_RESCUE_CURRENT_PROBE.md`.

The convolution has left nullity three at each tested period, coming
only from the common zero-frequency fold. It does not establish the
continuous three-ratio/full-joint rank theorem. The weak-metric estimate
is conditional on the torus premise and does not replace normal-chart
gluing on a fixed nonconstant smooth g. A pointwise O(h^2) metric or
current field is not O(h^2) in the unweighted sum over L^4 sites.

All recorded searches fail the necessary connection and phase-erasure
equations, including the c~h envelope with its linear range correction.
Their X values belong to rejected candidates. They prove neither success
nor failure of H-NORMAL-RESCUE on exact joint fields, and no candidate-
dependent source turns them into a response counterexample.

The environment disconnected during publication. Recovered executable
sources require independent replay as documented in the probe note.
Keep #310 Draft / IN_PROGRESS; no new physical terminal.

### Spatial-diagonal interior rank and boundary rescue

`A4D_Y_CURVED_JOINT_SPATIAL_DIAGONAL_INTERIOR.md` classifies the 68-row
interior operator on `lambda=(1,r,r,r)`, `r in C*`. Two direct exact minors
have gcd `r^45*(r-1)^3*(r-4/21)`. The interior ranks are 65 at `r=1`, 67
at `r=4/21`, and 68 elsewhere on that line. The full joint rank at
`r=4/21` is 96, demonstrating exact boundary rescue; `4/21` is off the
physical unit circle. This is a hostile control against assuming that the
two-ratio interior theorem extends unchanged to three ratios. It does
not classify three independent ratios or prove the all-torus gap.

### Full joint spatial-diagonal line

`A4D_Y_CURVED_JOINT_SPATIAL_DIAGONAL_FULL.md` strengthens the preceding
interior result to all 136 joint rows on the same complex line. Two
integer-polynomial 96-row determinant charts have exact
characteristic-zero gcd `r^56*(r-1)^4`, established by complete signed
CRT reconstruction with a Leibniz coefficient bound and a degree-preserving
first-prime gcd. Therefore the full joint symbol has rank 96 for every
`r in C*` except `r=1`, where its exact rank is 95. The `4/21` interior
defect is globally rescued on this line. This does not settle three
independent ratios or the full physical torus; the nonlinear curved
response and owner sum-norm estimate remain open.

The exact line theorem plus the owned folded analytic module also yields
an unconditional refinement-uniform `l^p` inverse on the physical
fourfold spatial-diagonal symmetry sector, including the unweighted
owner sum norm. `A4D_Y_SPATIAL_DIAGONAL_UNIFORM_SECTOR.md` proves this
by smooth one-circle division and absolutely summable Fourier kernels.
Compactness also extends the linear estimate to some open Fourier tube
around that sector, with no explicit tube radius yet.
The same estimate and the owned nonlinear remainder give flat local
joint rigidity in that sector modulo the constant nongauge Y amplitude,
with a chart radius independent of `L`. Smooth nonconstant metrics break
the sector symmetry; neither H_TORUS nor the curved response terminal is
deduced from this restricted theorem.
