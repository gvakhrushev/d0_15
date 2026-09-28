# A4D joint response decoupling — stationary-center quotient attack

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
Execution PR: #310  
Status: **IN PROGRESS / decisive response-quotient route selected**  
Scientific boundary: unchanged naked star action; no selector, no torsion equation, no spectral filter.

## 0. Typed target and source convention

The finite metric response is the literal partial Euler vector in the ten symmetric Gram directions at each site,
[
E_Q(Q,K)in igoplus_x mathrm{Sym}^2(mathbb R^4)^*,
]
taken at fixed connection before imposing the metric equation. The physical normalization is applied only afterwards:
[
mathcal R_h(Q,K)=h^{-2}E_Q(Q,K).
]

For exact finite supercell certificates, equality/non-equality is checked componentwise in the full phase-by-Gram vector; this is stronger than any finite-dimensional norm statement. For refinement estimates, use the owner sum norm from #226,
[
|F|_Sigma=sum_xsum_{mule
u}|F_{mu
u}(x)|,
]
unless a later theorem explicitly pushes the result through the existing physical reconstruction map into a local tensor/testing topology.

The non-tautological comparator is the #216 designated smooth approximate/exact continuation on the **same sampled smooth metric** (Q_h). Comparing two exact solutions of an identical prescribed metric-source equation gives zero by substitution and is retained only as a tautological control.

The scientific target is therefore
[
D_h(K_h):=
h^{-2}igl(E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{m sm})igr),
]
for exact connection-stationary or joint-critical sheets in the declared physical class, with the actual source convention stated in each theorem.

## 1. Structural correction: do not try to rescue every connection to one smooth sheet

Merged #232 owns an exact analytic curved nongauge joint-vacuum family through the flat point,
[
E_K(eta,K_Y(z))=0,qquad E_Q(eta,K_Y(z))=0,
]
with nonzero plaquette curvature for (z
e0).

Therefore a universal estimate of the form
[
d(K_h,mathcal Z_h^{m sm})le C h^{-p}|r_h|^eta
]
cannot be the main terminal for a class that includes this stationary center: at zero residual it would force every curved nongauge root into the smooth/LC-like fiber.

The correct decomposition is

[
	ext{stationary center} oplus 	ext{transverse/range directions}.
]

Uniform normal rescue remains useful only transversely. Along the physical stationary center, the required theorem is **metric-response equivalence**.

This changes the closure question from

> does the finite equation uniquely suppress UV connection amplitudes?

to

> does the finite metric Euler response factor through the quotient by all physical stationary-center moduli relevant in the continuum class?

## 2. Decisive exact experiment: slow Bloch/normal-jet response around the Y branch

The first target is the exact period-four Y joint-vacuum family, because it is already a certified curved nongauge stationary center and therefore cannot be removed by a connection-uniqueness argument.

Let (z) be its microstructure amplitude and let (k) denote a slow Bloch momentum / normal-jet modulation. Linearize the **literal full finite Euler system** around
[
(Q,K)=(eta,K_Y(z))
]
in the genuine Lorentz quotient.

Build the exact supercell block derivative
[
mathcal H_z(k)=
egin{pmatrix}
A_z(k) & B_z(k)\
C_z(k) & D_z(k)
end{pmatrix},
]
where

- (A_z=D_KE_K),
- (B_z=D_QE_K),
- (C_z=D_KE_Q),
- (D_z=D_QE_Q),

with one fixed polarization/character convention and all shifted edge occurrences included.

### 2.1 Required negative control

At (z=0), the reduction must reproduce the already-owned IR Schur symbol and direct Einstein identification:
[
S_0^{[2]}(k)=-	frac12 K_G^{(1)}(k)
]
in the repository Gram/output convention.

Failure of this control invalidates the new block assembly.

### 2.2 No illegal inverse at the stationary center

At nonzero (z), (A_z(0)) may have a physical stationary-center kernel. Do **not** write (A_z^{-1}).

Construct exact right/left kernel-complement data and a Lyapunov--Schmidt split:
[
a=a_{m c}+a_{m r}.
]

Solve only the range equation on a certified complement. Project the remaining connection equations to the cokernel and retain the reduced center equations. The allowed center tangent is whatever survives the full reduced system; it is not declared gauge merely because its metric readout vanishes at the flat point.

The effective metric response on the stationary correspondence is then computed after the range correction and the reduced center compatibility. Symbolically it has Schur form only on the proven invertible complement:
[
S_z(k)
=
D_z(k)-C_{z,m r}(k)A_{z,m r}(k)^{-1}B_{z,m r}(k)
+	ext{center-correction terms}.
]

Every extra term must come from the actual reduced equations.

## 3. The bifurcation test

Extract the total slow-momentum degree-two coefficient:
[
S_z^{[2]}(k).
]

The primary exact question is

[
oxed{S_z^{[2]}(k)stackrel{?}{=}S_0^{[2]}(k)}
]
on the entire allowed Y stationary-center branch, modulo the already-owned metric gauge/coframe kernel.

### Positive finite terminal

If the identity holds coefficient-by-coefficient for exact symbolic (z), record:

[
	exttt{A4D-Y-STATIONARY-CENTER-EINSTEIN-RESPONSE-EQUIVALENT}.
]

This is not yet the global continuum theorem. It is the first exact proof that a genuinely curved nongauge UV stationary modulus can be invisible to the Einstein principal response.

### Negative finite terminal

If there is an exact non-gauge metric component and admissible center solution with
[
S_z^{[2]}-S_0^{[2]}
e0,
]
record the precise coefficient and branch. It becomes a candidate universality defect, but **not** the task's final no-go until it is realized by an actual smooth nonflat exact joint-critical/source-compatible sequence satisfying the #310 comparator contract.

## 4. Curved-background realization gate

The existing exact Y slow extensions with fixed spatial Gram / time-dependent coframe are macroscopically flat. They are mandatory controls but cannot decide Einstein universality on curved metrics.

The next realization must carry a genuine nonzero normal metric Hessian at the observation point. Use the existing normal-jet realization passport; do not infer curvature from a varying coframe alone.

Required construction:

1. choose an arbitrary symmetric normal Hessian (J_{ab,cd});
2. sample a smooth compact periodic realization (Q_h(J)) with
   (q(0)=0), (partial q(0)=0), (partial^2q(0)=J);
3. continue the Y stationary center plus its range correction over this background, or prove the exact obstruction to continuation;
4. evaluate the literal metric Euler on the solved branch;
5. compare after the single (h^{-2}) normalization with the #216 smooth comparator.

A nonzero off-shell vector such as the known Orth3 slow-solder coefficient is not enough. The connection equations must be solved to the required order/all orders for the claimed terminal.

## 5. Nonlinear completion route after the degree-two test

A positive quadratic response identity still needs a nonlinear/uniform theorem.

The preferred architecture is a response quotient:

[
pi_h:mathcal C_h(Q_h)	omathcal R_h,
qquad
Ksim K'
Longleftrightarrow
h^{-2}|E_Q(Q_h,K)-E_Q(Q_h,K')|	o0.
]

Prove on the declared near-flat class that:

1. the full stationary correspondence exists over the sampled curved background;
2. transverse deviations from that correspondence obey a refinement-uniform estimate with only polynomial (h^{-1}) loss;
3. physical center amplitudes need not be small, but the metric response is constant on each allowed stationary fiber up to (o(h^2));
4. the common response agrees with the designated smooth comparator;
5. the #201/#273 coefficient and normal-coordinate locality then give
   [
   h^{-2}E_Q(Q_h,K_h)=-	frac12G[g]+o(1).
   ]

A proof may use exact Lyapunov--Schmidt reduction, compensated compactness, a finite set of envelope fields attached to torsion/Bloch strata, or another method. It may not assume weak convergence is sufficient for the nonlinear metric variation.

## 6. Hostile controls that must stay live

The following are separate and must not be conflated:

- #232 exact Y family: curved, nongauge, joint vacuum, flat metric response zero.
- #227 family: exact (E_K=0), curved, nonzero metric response; not a joint-critical counterexample.
- #275 Orth3 slow coefficient: exact resonance connection obstruction plus nonzero off-shell metric coefficient; not an on-shell response residue.
- #317 complex rank-23 witness: algebraic complex character control; physical even-rank theorem survives on the unit torus.
- #315 diagonal Smith data: local singularity control; not a multivariable stationary-response theorem.
- identical prescribed metric-source equations on two exact branches: response equality is tautological and does not identify the common value with Einstein.

## 7. Final task terminals

Close positively with

[
oxed{	exttt{A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED}}
]

only if the proved class includes the exact Y-type grid-scale stationary microstructure and genuinely curved smooth backgrounds, with explicit source/comparator convention and a norm/topology in which
[
D_h(K_h)	o0.
]

Close negatively with

[
oxed{	exttt{A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO}}
]

only with a genuine smooth-background joint-critical/source-compatible sequence in the Lorentz quotient and a certified nonzero normalized response gap.

Otherwise remain Draft and name exactly one smallest missing map/estimate.

## 8. Immediate certificate deliverables

The next exact artifact should contain, in one convention:

- period-four Y supercell (A_z,B_z,C_z,D_z);
- exact (z=0) reconstruction of the known Schur/Einstein symbol;
- right kernel and left cokernel of (A_z(0));
- certified range-complement inverse or exact solve;
- reduced center compatibility matrix;
- exact (S_z^{[2]}-S_0^{[2]});
- gauge/coframe-kernel checks;
- one hostile assembly control with a deliberately wrong transpose or omitted shifted edge occurrence that fails.

Do not start another determinant census before this response test is resolved.
