# A4D Y curved response — next closure gate

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
Execution PR: #310
Status: `IN_PROGRESS` / nonlinear continuation open
Action: unchanged naked star action; no added selector or torsion equation.

## Work mode for the theory-closure worker

Use the current head of PR #310 on `exp/a4d-joint-response-resolvent` as the source baseline; the corrected certificates and this brief are on that branch, not yet on the default branch. Prioritize a rigorous analytic derivation of the nonlinear reduction, continuation, or exact obstruction. Reuse the pinned finite certificates instead of rerunning expensive searches or large symbolic pipelines. Small checks are welcome; if a substantial exact computation is needed, specify its rational inputs, conventions, expected output, and a local replay recipe for the owner to run.

Keep every claim within its proved scope. In particular, do not promote the unverified rank-4 response-by-curvature claim, the unverified site scalar `2626083/44800`, the one-witness pairing, or finite normal-jet compatibility to a nonlinear theorem. Do not mark either terminal unless its complete proof obligation below is met.

## Corrected finite result

The result at `ea6e9d0` used the wrong mixed Bloch placement and its finite TT-defect interpretation is withdrawn. The corrected convention is connection equation `lambda^(-s)` and metric readout `lambda^(+s)`.

Two exact certificates are now pinned in this PR:

- `a4d_y_curved_response_phase_corrected_check.py` verifies the 10-component aggregate response for all four Bloch axes, the exact flat and curved connection ranks, the center/range equations, and a hostile swapped-phase control. Its four `q12` averages and defect ranks match the submitted corrected ledger.
- `a4d_y_curved_normaljet_compatibility_check.py` builds all 40 phase-resolved metric rows and the 20-dimensional Riemann normal-jet system. Exact ranks, kernels, curvature projection, smooth-source compatibility, and response comparison match the pinned JSON.

The normal-jet result is:

- connection ranks: flat 80, curved `z=1` 94; curved center dimension 2;
- quadratic phase system: rank 10, nullity 30, curvature projection rank 20;
- all-direction first-slow system: rank 43, nullity 5, curvature projection rank 1;
- smooth-source fast-phase-erasure system: rank 5, nullity 2, curvature projection rank 1;
- response difference from the independently built Einstein control: rank 0 on the compatible smooth-source kernel.

After normalization, the only compatible curved direction is `-Y tensor Y`, with `Y=(1,-1,1)` in spatial bivector order `(12,13,23)`. Its common response is `(3/2,0,0,0,-1/2,-1,-1,-1/2,-1,-1/2)` in metric-coordinate order `(q00,q01,q02,q03,q11,q12,q13,q22,q23,q33)`, exactly equal to the flat Einstein control.

These are finite exact normal-jet statements. They do not construct an exact branch on a curved background or prove a refinement-uniform limit.

## Exact stationary-center envelope symbol

The certificate `a4d_y_center_envelope_symbol_check.py` computes the principal quadratic symbol of the two center amplitudes at `z=1`. They decouple and give

`S_Y(t) = -2/188307 * [26250*(t0-16*s/75)^2 - (2283779/2)*r_perp^2]`

and

`S_dual(t) = -1/6408 * [882*(t0-16*s/21)^2 - (603687/2)*r_perp^2]`,

where `s=t1+t2+t3` and `r_perp^2=t1^2+t2^2+t3^2-s^2/3`. These are two transported `2+1` hyperbolic envelope modes; there is no elliptic spectral gap. This is only the quadratic principal symbol. It does not prove nonlinear envelope existence or an energy estimate.

The exact dual-center visibility check gives a second boundary at zero slow momentum: its finite Cayley path has zero connection Euler on all 96 rows, while its metric response alternates sign between the first and second phase pairs. The four-phase average vanishes, but requiring the metric Euler output to be equal on all four phases forces the dual amplitude to zero near the origin.

The small-amplitude Schur certificate starts from the 16-dimensional flat connection kernel and gives effective ranks `(0,0,12,12,14,14,14)` through order six. After the order-two reduction, four directions remain; the order-four and order-five reduced blocks vanish, and the order-six block is `diag(0,0,9/8,3/8)`. Thus twelve transverse directions first lift at order two, two soft transverse directions at order six, and two exact center directions remain. The worst inverse loss is `O(z^-6)`, so this finite splitting does not supply the uniform estimate needed for the continuum limit.

## Site-resolved source response on the `t0/t1` compatible class

The certificate `a4d_y_phase_resolved_compatible_response_check.py` independently builds the four-phase, 40-component metric source space at `z=1` for the `e0` axis. Its first two exact Fredholm conditions have ranks 1 and 2, leaving a 37-dimensional source class. The second-order averaged response defect has rank 8 on that class. The averaged first-order response has rank 4 there, although it vanishes on the ten-dimensional phase-independent source subspace. On that phase-independent subspace, the single-source defect has rank 6 and its `q12` coefficient is `-34163/118125`, matching the corrected four-axis certificate.

For a 10-by-40 matrix on all source coordinates, the checker explicitly extends the restricted defect by the Euclidean orthogonal projection onto the compatible class. This convention gives rank 8 and kernel dimension 32; the stationary response itself is only defined on the compatible class. This source-response calculation is distinct from the curvature normal-jet system above, which also imposes spatial center-gradient and fast-phase-erasure equations. It does not change that system's exact Einstein response on its surviving curvature direction.

The submitted scalar `2626083/44800` is not adopted: the supplied JSON does not identify the source vector or projection defining that `q12` value, and it is not the phase-independent `q12` coefficient under the pinned convention.

## Leading-order phase-independent source and curvature witness

The certificate `a4d_y_singleq_curvature_witness_check.py` independently verifies the latest consolidated single-source result. For one metric `q` shared across the four phases, both the curved order-zero and order-one connection cokernel maps have rank zero; the flat controls also have rank zero. The `q12` source excites the two center amplitudes by `(-3311/3750, 0)`, and its corrected second-order defect has rank 6 with `q12` coefficient `-34163/118125`.

The same checker verifies the supplied 10-by-10 normal-jet matrix as an element of the 20-dimensional algebraic Riemann-jet image. Its Frobenius pairing with the single-source defect is exactly `-27247/17500`. Six generators in the checker’s deterministic Riemann basis have nonzero pairings; that count depends on basis choice, while the explicit matrix and its nonzero pairing do not. This is a finite witness for the single-axis response map. It has not been shown to satisfy the full coupled slow-center and fast-phase-erasure system; the separate full normal-jet certificate still leaves only `-Y tensor Y` and matches Einstein on that surviving direction.

The latest submitted report also states that a defect map over all 20 Riemann jets has rank 4. The supplied JSON contains the explicit witness and its scalar pairing, but not the full response-by-curvature matrix or a replayable rank certificate. The six nonzero entries recorded above are pairings against one pinned basis and are not a matrix-rank result. Keep the rank-4 statement unverified until that map is supplied and independently replayed; it is distinct from the certified rank-6 single-q metric defect and the rank-1 curvature projection in the fully compatible normal-jet system.

## Reproduction

From the repository root:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_response_phase_corrected_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_dual_center_joint_visibility_check.py
python3 02_REGISTRY/research/certificates/a4d_y_center_envelope_symbol_check.py
python3 02_REGISTRY/research/certificates/a4d_y_small_amplitude_kernel_splitting_check.py
python3 02_REGISTRY/research/certificates/a4d_y_phase_resolved_compatible_response_check.py
python3 02_REGISTRY/research/certificates/a4d_y_singleq_curvature_witness_check.py
python3 02_REGISTRY/research/certificates/a4d_y_joint_first_slow_injectivity_check.py
python3 02_REGISTRY/research/certificates/a4d_y_product_plane_seed_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree4_gate_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree2_obstruction_check.py
```

The first checker also records the submitted report JSON as provenance; it cross-checks its aggregate four-axis fields, not the report's per-site `q12` arrays. The normal-jet checker owns the full curvature compatibility theorem. The dual-center and center-symbol checks distinguish the staggered flat mode from the two hyperbolic principal forms. The small-amplitude checker certifies the zero-momentum splitting through order six. The phase-resolved source-response checker verifies the 37-dimensional `t0/t1` compatible class. The single-source witness checker verifies the corrected phase-independent defect and its explicit algebraic curvature pairing; neither is a nonlinear continuation result.

## Remaining target: nonlinear continuation

The follow-up `A4D_Y_JOINT_FIRST_SLOW_REDUCTION.md` proves a new boundary before the connection-only wave equations: the complete first-slow metric constraint has rank 5 on four derivatives of the Y amplitude and the visible dual correction. Its exact minor determinant is `-975737200/35590023`, with inverse Frobenius norm less than 8. A regular leading Y envelope on the flat metric is therefore constant under the smooth-source condition. The stacked fixed-metric joint symbol has an injective first-order center symbol and a local `c|k|` lower bound; this is not a global gap or a z-to-zero estimate.

The same follow-up derives the analytic constrained first-order reduction near `(eta,1)`, an exact finite-lattice nonlinear range/cokernel reduction with explicit contraction hypotheses, and a genuinely curved commuting seed with exact response erasure. An exact connection row rules out that seed as a nonflat periodic stationary branch, so full transverse corrections must be retained. Two small companion certificates verify these new finite/algebraic inputs. No nonlinear terminal is claimed.

The follow-up now also contains an exact second-order normal-jet obstruction
on the normalized surviving `-Y tensor Y` curvature slice. The homogeneous
degree-four forcing vanishes; the degree-three reduced system is compatible
and forces the degree-four center correction to zero; the degree-two reduced
system has exact ranks `20 -> 21` after retaining arbitrary common metric
sources and every free degree-three center coefficient. Its `xi3^2` left
witness pairs to `-22209` in the reduced cokernel basis (`-166034484` for
the primitive integer 136-row Euler witness). A separate 140-by-140
connection-only reduced system has ranks `30/30`; the script constructs a
rational solution and verifies all 96 connection rows through degree four.
Thus the new defect forbids exact phase-common metric readout at order
`delta^2`, but does not obstruct the stationary connection branch at this
order. For bounded curvature `delta^2=O(h^4)`, below the required `h^2`
scale. It still does not control the omitted-order remainder, h-dependent
center growth, other curvature directions, or the full finite-lattice
continuation. The task remains `IN_PROGRESS` and both global terminals remain
unreached.

The exact connection-only replay also extracts the zero-momentum cokernel
coefficient for the constant-center restriction on this normalized germ. In
the certificate's recorded `ker(H^T)` basis it is
`(351402359/2108160, 21506403637/154949760)`, nonzero, while constant
kernel-shift columns vanish. A constant stationary center is therefore
obstructed at `delta^2`; the all-row connection solution cancels this source
with a spatially varying center jet through normal degree four. This is a
finite germ statement only: it does not exclude an exact branch with a
varying center or establish the refinement-uniform theorem.

The new symbolic family certificate allows an arbitrary first-order constant
retuning `z -> z + delta*s`. It proves that the two connection-cokernel
components stay equal to the displayed nonzero vector and that the
`xi3^2` phase-common metric witness stays `-22209`, after solving the degree-
three range equations. Thus this local defect cannot be tuned away by that
one center parameter. Spatially varying higher center jets and the global
finite-lattice branch remain open.

The replay is an exact identity in the indeterminate `s`, so it also covers a
bounded, nonconvergent or nonanalytic sequence of constant retunings
`s=s_h`: at every refinement the tracked order-`delta^2` coefficient remains
exactly the same. Such a scalar drift cannot cancel the curvature source by
choosing a special subsequence or fractional-power dependence on `h`. This
does not extend to unbounded `s_h` (where higher powers can reorder the
expansion), spatially varying center fields, or nonzero Bloch modes; those
remain the singular branch gate.

### Amplitude and parameter consequences of the degree-two witness

The phase-common degree-two obstruction is homogeneous in the curvature
amplitude on this normal-jet slice. With `delta=kappa*h^2`, the first metric
and connection tangents scale as `kappa`, and the quadratic normal-jet forcing
scales as `kappa^2`. The reduced matrix for the 20 free degree-three center
coefficients is built from the flat Hessian and its shift moments, so it does
not depend on `kappa`. The exact ranks therefore remain `20 -> 21` for every
nonzero `kappa`, and the pinned pairings scale to

```text
reduced cokernel witness:        -22209 * kappa^2
primitive 136-row Euler witness: -166034484 * kappa^2
```

Thus at `z=1`, on `R=kappa*R_Y`, no phase-common joint formal normal-jet
continuation through degree two exists when `kappa != 0`. This extends the
unit-amplitude certificate to the full nonzero ray; it remains a finite-jet
statement for this one curvature direction.

A generic-`z` consequence follows without knowing an explicit obstruction
polynomial. Every fixed-degree matrix in this calculation is rational in the
one Cayley parameter `z`. On a pivot chart through `z=1`, the reduced matrix
has 20 coefficient columns, while its augmentation has rank 21 at `z=1`. Some
21-by-21 augmented minor is therefore nonzero there. Its entries are rational
in `z`, so it is a nonzero rational function and can vanish at only finitely
many regular values. Away from those zeros and the finite poles/rank-drop set
of the pivot chart, the augmented rank is at least 21 while the coefficient
rank is at most 20. Hence the same curvature direction is obstructed at
generic regular `z`. This proves that any exceptional regular values lie in
a finite algebraic set, but does not identify that set or cover the singular
flat point `z=0`.

Since `z=1` itself is regular and obstructed, that finite exceptional set has
positive distance from `1` on the fixed pivot chart. Hence there is a
neighborhood of `1` in which the same degree-two rank obstruction holds.
Consequently any refinement-dependent *constant* parameter `z_h -> 1` stays
obstructed for all sufficiently small `h`, regardless of whether its rate is
integer-power, fractional-power, or nonconvergent after rescaling. This is a
coefficient-level normal-jet statement only; it does not control spatially
varying `z_h(x)`, nonzero Bloch modes, or omitted orders of an exact branch.

For an `h`-dependent amplitude the leading witness is
`-22209*kappa(h)^2*h^4`. A uniform remainder `o(h^4)` would rule out a limit
`kappa(h)->kappa_0 != 0`. A stronger estimate
`|R_h| <= C*h^(4+epsilon)` would imply
`|kappa(h)| <= sqrt(C/22209)*h^(epsilon/2)`. Neither estimate is available
for the full finite-lattice center/range system, so the witness alone does
not force a general `h`-dependent branch to shrink. A singular center
correction of the same order may still cancel it. The quadratic witness also
does not automatically rule out branches whose first nonzero curvature jet
occurs at a higher order.

### Periodic mean obstruction for regular branches

There is now a sharper conditional theorem for the regular branch, recorded
in `a4d_y_periodic_regular_branch_mean_check.py` and its pinned JSON. Assume a
periodic spatial product background with real `C^4` Gaussian curvature
`kappa(x)`, the owner's global product framing and `z=1` Y sheet, and a joint
stationary family with a uniform integer-power expansion through `h^4`,
bounded `C^4` coefficient fields, and an `O(h^5)` remainder. The first-slow
joint equations and their exact nonzero-covector injectivity force the
order-`h` homogeneous Y-center envelope to be constant and its visible dual
component to vanish. At curvature order `h^2`, the local Y retuning may vary
with `x`, but its pointwise value is the parameter `s` in the amplitude-family
certificate, whose projected source is independent of every `s`; its spatial
derivatives first enter one order later.

Sum the two zero-momentum connection-cokernel equations over the periodic
sites. Every flat range term vanishes under the left-kernel rows. Every
transport term from a higher center correction is a linear combination of
periodic shift differences and has zero sum. In the variable-curvature normal
jet, the linear order-`h^4` Hessian term also has zero mean. Products of the
leading order-`h^2` curvature tangents contribute only `kappa^2` at order
`h^4`; gradient corrections first enter one order later. The exact amplitude
family certificate gives the remaining mean source, independently of `s`,
as

```text
(351402359/2108160) * mean(kappa^2) = 0
(21506403637/154949760) * mean(kappa^2) = 0.
```

Both coefficients are positive, so this regular periodic branch requires
`kappa == 0`. This closes the periodic-mean route for uniformly regular
integer-power branches on the stated Y sheet. It does not exclude a
nonanalytic or nonuniform refinement-dependent center correction, and it is
not an exact finite-lattice continuation theorem. In particular, the global
uniform response gate remains open until those singular branches are
controlled or constructed.

The owned joint low-frequency symbol explains the singular scale. On a fixed
periodic domain with `h=1/L`, the first nonzero slow mode has `|k|~h`; the
injective first-order reduced symbol therefore has inverse size `~h^-1`.
Smooth normal-chart forcing of size `h^2` yields a center correction of size
`h`, while a generic quadratic remainder is again `h^2` and is sent back to
size `h` by that inverse. The ordinary contraction argument is thus not
uniform. The next missing estimate is a projected nonlinear gain (such as
`O(h^3)` forcing on admissible `O(h)` center modes), or a tame alternative
that controls resonant mode interactions and the zero-mode cokernel. This
identifies why the exact regular mean obstruction alone does not dispose of
the singular branch; it does not assert that the nonlinear term actually
attains the generic bound.

The regular periodic branch is excluded under the stated integer-power and
uniformity hypotheses. The remaining continuation problem is therefore the
singular/nonanalytic or nonuniform refinement-dependent class. Derive and
control the nonlinear **joint constrained** equations, rather than two free
connection-center wave equations, then either continue the surviving curved
normal jet `J` to an exact stationary branch

`K_h(J) = K_Y + a_h(J)`

over sampled smooth metrics `Q_h(J)` with `q(0)=0`, `partial q(0)=0`, and `partial^2 q(0)=J`. Solve the literal finite connection Euler equation `E_K(Q_h,K_h)=0`, retaining the center variables and imposing the full cokernel equations at every order.

Acceptable proof routes include analytic Lyapunov–Schmidt/Kuranishi continuation with a convergent majorant, Newton–Kantorovich on a certified range complement plus exact reduced hyperbolic center estimates, or another finite-dimensional analytic continuation with constants tracked in `h`. The continuation radius must support the background scaling, and omitted orders must be controlled. An elliptic inverse or elliptic spectral-gap estimate cannot be assumed for the center symbol.

The branch must then satisfy the owner-topology estimate

`|E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)| = o(h^2)`

uniformly under refinement. Control near-resonant complements, the allowed stationary-center amplitudes, conjugate Bloch-sector interactions, and the declared compact set of smooth background parameters.

For the regular class, the exact mean equation and its nonzero `mean(kappa^2)` coefficient are now the first reduced obstruction. For the remaining singular class, return the first exact reduced center or cokernel equation that fails, its rational/polynomial obstruction, the surviving nonlinear curvature variety, and whether the obstruction forces the Y amplitude to shrink with `h`. A finite normal-jet compatibility result alone is not a nonlinear failure.

## Selector and terminal rules

Do not claim a selector is required unless two exact source-compatible stationary branches over the same admissible smooth background have different normalized metric responses. The corrected finite normal-jet response agrees with Einstein on its compatible direction.

Keep PR #310 Draft and the lifecycle `IN_PROGRESS` until the nonlinear continuation and uniform remainder are proved or refuted. Neither global task terminal has been reached:

- Positive: `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED`.
- Negative: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.
