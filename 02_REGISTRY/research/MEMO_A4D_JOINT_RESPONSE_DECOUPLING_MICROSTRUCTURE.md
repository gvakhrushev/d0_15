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

An exact nonlinear transport check now gives a sign-free restriction inside
the pure-Y ansatz. Every spatial-boost edge equation factors as
`±8(a-b)(a+b)/((4+3a^2)(4+3b^2))`. Since the denominator is positive for real
amplitudes, stationarity forces `a^2=b^2` along each of six transport moves.
Those moves generate the connected even-sum sublattice on periodic `L=4m`,
so `|a|` is constant there, even if signs vary. A fixed-sign branch is thus
constant. This closes the pure-Y amplitude variation channel more broadly
than the earlier near-`z=1` fixed-sign statement. The remaining solder rows
have not been used to classify sign-changing patterns, and transverse/non-Y
corrections remain outside this ansatz result.

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

A second small certificate treats the genuinely curved product-plane seed `S=I+(f-1)P_perp`, with f time independent and constant along `(1,1,1)`. Commuting spatial spin links give exact sitewise metric-response erasure for the Y carrier, and all 96 connection coefficients through first slow order vanish without linearizing in f. However the exact temporal boost-dual row is `3 f(x)^2-sum_i f(x-h e_i)^2`. On a connected periodic spatial lattice this excludes nonconstant f within the commuting seed ansatz. It is not an obstruction to the full connection space: the transverse corrections at the next order remain essential.

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

The exact checker `a4d_y_small_amplitude_kernel_splitting_check.py` reduces the flat 16-dimensional connection kernel twice. The effective ranks through order six are `(0,0,12,12,14,14,14)`. After the order-two block, four directions remain; the reduced order-four and order-five blocks vanish, while the order-six block is `diag(0,0,9/8,3/8)`. The final kernel consists of the exact Y and boost-dual center tangents. Twelve transverse modes lift at order two, two soft modes at order six, and the worst inverse loss is `O(z^-6)`. This exact zero-momentum splitting identifies the small-amplitude conditioning that a nonlinear uniform estimate must control; it is not itself an `h`-uniform continuation theorem.

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
python3 02_REGISTRY/research/certificates/a4d_y_product_plane_seed_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree2_obstruction_check.py
python3 02_REGISTRY/research/certificates/a4d_y_stationary_center_family_coker_check.py
python3 02_REGISTRY/research/certificates/a4d_y_variable_curvature_normal_jet_check.py
python3 02_REGISTRY/research/certificates/a4d_y_periodic_regular_branch_mean_check.py
```

The first command verifies the four-axis aggregate, exact center/range solves, three direct rational Schur controls, and a hostile swapped-phase control. The second verifies full curvature normal-jet compatibility and Einstein response. The next four verify dual-center source visibility, the hyperbolic center symbol, the new cubic vertex, and the zero-momentum small-amplitude splitting. The subsequent pair verify the 37-dimensional site-resolved class and the phase-independent single-source curvature witness. The next two verify joint first-slow injectivity and the nonlinear product-plane seed identities. The following pair verify the exact `delta^2` connection/metric normal-jet system and its invariance under arbitrary constant first-order Y retuning. The next command derives the variable-curvature Riemann-normal metric jet and checks its constant-curvature specialization against that owner. The final command replays the exact amplitude law, first-slow injectivity, and periodic shift identities used by the regular-branch mean obstruction. Each checker compares its result with a pinned JSON. The old `a4d_y_curved_response_quotient_check.py` and its output remain historical regression material; its `ea6e9d0` TT-defect interpretation must not be used.

The submitted aggregate JSON has SHA-256 `79e6db7d96a0863a6af56e94752d080d5505a7fc47a307b752269dd092c4e230`. Its per-site `q12` arrays are not separately asserted by the aggregate checker.

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
