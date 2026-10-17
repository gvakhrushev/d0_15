# Native weighted traces, moving lifts and the full compensator gate

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `0af401558deca37468c077c40b53ac670a7ccaf3`.
Status: scoped research proofs; positive GR and global closure remain OPEN.

This tests three concrete mechanisms left outside the fixed-norm and
[signed-quadratic results](A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md).
Neither a new action nor an admissibility constraint is added to the core.
In particular, the candidate physical volume map below and continuous lift
variations are stated as hypotheses, not attributed to existing owners.

## 1. Literal weighted trace coordinates

`ConformalLaplacianTrace` owns
\(W_\rho=\operatorname{diag}(1/\sqrt{\rho_i})\) and
\(L_\rho=W_\rho L W_\rho\), with positive \(\rho\).
`EntropyArchiveFlow.archiveVolume` is exactly
\[
 \operatorname{Vol}_N(\rho)=|N|^{-1}\sum_i\rho_i^{-1}.
\]
Thus the literal volume coordinate is \(\mu_i=\rho_i^{-1}\), not
\(\rho_i\). `HeatTraceEHProxy` owns
\[
 P(L,\rho)=\sum_{i\ne j}\frac{L_{ij}^2}{\rho_i\rho_j}
           =\sum_{i\ne j}L_{ij}^2\mu_i\mu_j.                 \tag{1}
\]
The similarly named action in `HeatTraceA2Decomposition` is **half**
of (1); its trace-square decomposition contains twice that action.
The research Lean capsule proves (1) and its exact quadratic expansion
on every affine \(\mu\)-pencil for arbitrary finite index type.

More generally, for \(p\ge1\), cyclicity of a finite trace gives
\[
 \operatorname{tr}((W_\rho L W_\rho)^p)
 =\operatorname{tr}((D_\mu L)^p)
 =\sum_{i_1,\ldots,i_p}
   \mu_{i_1}\cdots\mu_{i_p}
   L_{i_1i_2}\cdots L_{i_pi_1}.                              \tag{2}
\]
For example, move the initial \(W_\rho\) of
\(W_\rho L(W_\rho^2L)^{p-1}W_\rho\) to the end and use
\(W_\rho^2=D_\mu\). Symmetry of \(L\) is unnecessary for (2).
Consequently this moment has degree at most \(p\) in \(\mu\).
The diagonal part removed in (1) is also quadratic. Products of moments
have the sum of their moment degrees. Mesh-dependent signed coefficients,
normalizations and increasing finite carriers do not change that fact.

### Bounded-degree volume-faithful contrast theorem

Fix an integer \(D\), independent of mesh. At each mesh use a fixed,
metric-independent \(L_h\) and an action polynomial in \(\mu\)
of degree at most \(D\), for example any finite polynomial in the
moments (2) of weighted degree at most \(D\). No auxiliary elimination
with variable coefficients is silently included. Assume the proposed
physical readout admits the curved Gram pencil from the preceding proof
and identifies its sitewise volume by
\[
 \mu_{h,i}(s)=b_{h,i}\sqrt{|\det g_s(y_{h,i})|},\quad
 b_{h,i}>0\text{ independent of }s.                         \tag{3}
\]
This includes the literal choice \(b_{h,i}=1\). The core's global volume
identity alone does not prove (3); (3) defines the candidate class tested.
No freedom to encode an arbitrary action value in a weight is assumed.

For this actual metric/coframe-affine pencil, \(|s|<1/4\),
\[
 \Omega(y)=1+\tfrac1{10}\cos(2\pi y_2),\qquad
 \sqrt{|\det g_s|}=\Omega^3(\Omega+s).                       \tag{4}
\]
Hence the native value \(F_h(s)\) is a polynomial of degree at most
\(D\), even though \(\rho=1/\mu\) and the original weights depend
nonlinearly on the metric. Its centered secant has degree at most
\(D-1\) for \(D\ge1\). A pointwise limit on an open interval of
polynomials of degree at most \(D-1\) has the same degree bound:
choose \(D\) distinct fixed anchors, write the exact Lagrange
interpolation formula, and pass to the limit in that finite sum.
No uniform coefficient bound or derivative of an error is needed.

If the planned half-contrast transfer held with a fixed \(a\ne0\),
total recording/refinement error \(O_s(h)\), and
\(\epsilon_h=h^{1/3}\), then the completed physical probe law would give
\[
 a^{-1}\frac{F_h(s+\epsilon_h)-F_h(s-\epsilon_h)}{2\epsilon_h}
     \longrightarrow I'(s),\qquad\text{error }O_s(h^{2/3}). \tag{5}
\]
The endpoint preparation must satisfy the physical probe law's actual
24-row conditions; no on-shell condition is inserted into a gate here.
By interpolation, (5) would force \(I\) to have degree at most \(D\).

But the independently computed literal Einstein action on this pencil is
\[
 I(s)=\int C(s,\Omega)(\Omega')^2,\qquad
 C(s,w)=\frac{(s+2w)(5s+6w)}{4w(s+w)}
       =\frac{5s}{4w}+\frac{11}{4}+\frac{w}{4(w+s)}.         \tag{6}
\]
The all-component Ricci calculation, convention and periodic integration
by parts are pinned in the preceding artifact and its exact certificate.
For **every** integer \(k\ge2\), differentiation of the last rational
term, followed by differentiation under the compact integral, gives
\[
 I^{(k)}(0)=\frac{(-1)^k k!}{4}
       \int\frac{(\Omega')^2}{\Omega^k}\ne0.                \tag{7}
\]
Indeed \(9/10\le\Omega\le11/10\),
\(\int(\Omega')^2=\pi^2/50\), and
\((-1)^k I^{(k)}(0)\ge k!\pi^2/[200(11/10)^k]>0\).
Differentiation is justified on any closed subinterval of \(|s|<1/4\)
by the positive denominator bound and smoothness. The case \(D=0\)
also fails: its secant is zero whereas
\(I'(0)=\int(\Omega')^2/\Omega>0\).

This excludes every **uniformly bounded-degree** member of the specified
volume-faithful fixed-operator class, for either sign of calibration.
An independently fixed affine source pairing, or any subtraction obeying
the same fixed degree bound, cannot repair (7). No conclusion is asserted
for arbitrary nonlinear matter coupled to a different total action.

### Protected exceptions and actual spectral owners

* Degree increasing with refinement is outside this theorem. The Taylor
  polynomials of (6) on \(|s|<1/4\) provide a concrete counterexample to
  dropping the uniform degree bound: they converge with their derivatives.
* A geometry-dependent \(L\), nonpolynomial function of its weighted
  spectrum, nonlinear volume readout, or metric-dependent auxiliary
  elimination needs a separate native owner and analysis.
* `ArchiveHeatTrace` uses `archiveEigenvalue n x = x.val`. Its actual
  \(\sum_x e^{-u x.val}\) at fixed \(u\) has no metric/density argument,
  so its metric contrast is zero. It is not the heat trace of
  \(W_\rho L W_\rho\); replacing it by that object is an additional step.
  The structural spectral-admissibility owner does not supply this step.
* `EntropyArchiveFlow` assumes mass preservation for a supplied flow.
  This does not define the admissible variations of an action. If one
  separately imposes \(\sum\rho_i=\text{constant}\) together with (3),
  unrestricted metric probes are lost: \(g_t=(1+t)g\) gives
  \(\mu_t=(1+t)^2\mu\), \(\rho_t=(1+t)^{-2}\rho\), and nonzero
  total-mass derivative. A physical restricted-probe recovery would need
  its own argument; mass preservation is not treated as a universal no-go.

For completeness, the **free density** Euler gate of (1) itself is empty
for a fixed \(L\) having any nonzero off-diagonal entry:
\(P(L,t\rho)=t^{-2}P(L,\rho)\), so its scaling derivative is
\(-2P\), strictly negative. If this full positive-cone gate is admitted,
stationarity implies all off-diagonal entries vanish. Adding row-sum zero
would then imply \(L=0\). This statement requires free density scaling;
it is not applied to an independently constrained action.

## 2. All linear intertwining lifts between adjacent canonical cycles

For the actual canonical stages put \(m=n+2\ge3\). Their Laplacians
are \(L_m=2I-U_m-U_m^{-1}\) and \(L_{m+1}\).
Allow any real linear lift \(J:\mathbb R^m\to\mathbb R^{m+1}\).
This is an explicitly enlarged candidate class; the existing
`archiveLiftOperator` is the fixed modulo point-map pullback.

**Exact classification.** Every solution of
\(L_{m+1}J=JL_m\) has the form
\(J=c\,\mathbf1_{m+1}\mathbf1_m^T\). To see this without a numerical
spectral assumption, complexify. The Fourier vectors \((1,z,\ldots,
z^{m-1})\), \(z^m=1\), form a basis (a Vandermonde matrix on distinct
roots) and have eigenvalue \(2-z-z^{-1}\). Equality with the eigenvalue
of an \((m+1)\)-st root \(w\) says
\[
 z^2-(w+w^{-1})z+1=(z-w)(z-w^{-1})=0.
\]
Thus \(z=w\) or \(z=w^{-1}\); coprimality of \(m,m+1\) forces
\(z=w=1\). Only the constant-to-constant matrix block survives in the
intertwining equation. The real classification follows immediately.
If \(J\mathbf1_m=\mathbf1_{m+1}\), its unique possible value is
\[
 P_m=m^{-1}\mathbf1_{m+1}\mathbf1_m^T,\qquad\operatorname{rank}P_m=1.
                                                                    \tag{8}
\]
In particular **no injective linear lift** satisfies exact compatibility,
not just the particular modulo lift tested in `ArchiveLaplacianRG`.

Now use the unchanged positive seam norm but vary the lift independently:
\(S(J)=\|L_{m+1}J-JL_m\|_F^2\). In the full unital affine space the
direction \(P_m-J\) is allowed, and
\[
 S((1-t)J+tP_m)=(1-t)^2S(J),\qquad DS(J)[P_m-J]=-2S(J).    \tag{9}
\]
Consequently full lift stationarity implies \(J=P_m\). The same
descent direction remains in the nonnegative row-stochastic set for
\(0\le t\le1\); it rules out a constrained local minimum with
\(S>0\) even on its boundary. Injectivity is open, so restricting to
injective lifts still admits this direction for sufficiently small
positive \(t\), and leaves no full-gate root. A fixed positive weighted
quadratic seam norm gives the same scaling argument.

**Locality is an actual exception.** On the pair \(m=3,4\), restrict
row \(i\) to columns \(i\bmod3\) and \((i+1)\bmod3\), with entries
\(1-x_i,x_i\). Exact minimization in those four allowed coordinates gives
\[
 x=(1/2,5/8,3/8,1/2),\qquad
 J_* =\begin{pmatrix}1/2&1/2&0\\0&3/8&5/8\\
                         3/8&0&5/8\\1/2&1/2&0\end{pmatrix},
 \quad\operatorname{rank}J_*=3,\quad S(J_*)=3/4.             \tag{10}
\]
All four allowed first derivatives vanish and the Hessian is positive
definite. The dense direction in (9) violates the prescribed support.
This is a real nonempty constrained stationary fiber, not an Einstein
solution or an invented native constraint. It prevents applying the
full-lift theorem to arbitrary local lift classes.

Nor does exact incompatibility imply a uniform approximation barrier.
For the injective modulo pullback \(J_0\),
\(J_\delta=P_m+\delta(J_0-P_m)\) is row-stochastic and injective for
\(0<\delta\le1\), and \(S(J_\delta)=4\delta^2\to0\).
Injectivity follows by splitting the domain into constants and mean-zero
vectors; \(J_0\) maps no nonzero mean-zero vector to a constant. Its
inverse on nonconstant data degenerates. No uniform range estimate or
continuum obstruction is inferred from (8).
Nonadjacent cycle lengths, scaled intertwining equations, varying
Laplacians and nonlinear lift constraints are separate classes.
The owner's entrywise `RenormalizedProjectiveCompatibility` is also a
different definition and is not renamed into this operator equation.

## 3. Full gate of the existing weighted A2 compensator

`A2CompensatorNoether` is an actual finite rational owner. With unsigned
endpoint incidence \(B\), positive edge weights \(W\), and independent
edge and vertex fields \(h,\eta\), it defines
\[
 r=h-\tfrac12B^T\eta,\quad A=2\sum_e W_er_e^2,\quad
 E_h=4Wr,\quad T_{\rm diag}=-4BWr.                          \tag{11}
\]
Its exact first-variation theorem justifies the edge gate, and its Ward
identity is off shell. **All edge equations** \(E_h=0\) are equivalent
to \(r=0\) when \(W>0\). Hence \(A=0\),
\(T_{\rm diag}=0\), and every first weight variation vanishes. These
are Lean-proved statements of the literal rational owner. The same
coordinate proof works over the reals, without a spectral-gap assumption.
For differentiable external geometry dependence of \(B,W\), the ordinary
chain rule gives zero geometry response at \(r=0\) as well.
If \(W\) depends on the very edge field being varied, (11) is no longer
the full derivative and the theorem must not be used as that gate.

Crucially, eliminating **only** \(\eta\) is a different operation.
Its equation \(BWr=0\) admits nonzero residuals and the resulting
profile can be a rational function of moving weights. On the unsigned
four-cycle take \(\rho=(1,2,3,4)\),
\(W=(1/2,1/6,1/12,1/4)\), \(k=(1,-1,1,-1)\),
\(h=W^{-1}k=(2,-6,12,-4)\), and \(\eta=0\). Then
\(Bk=0\), so the entire vertex gate and diagonal response vanish, but
\(A=48\) and \(E_h=4k\ne0\). This hostile control protects the
distinction between an auxiliary-only profile and a full joint solution.
No nonlinear Einstein source is inferred from the conditional Ward law.

## 4. Verification and remaining obligation

The exact checker replays **86 controls**: trace moments, the volume pencil, all
finite interpolation coefficients, reciprocal derivative controls, cycle
characteristic-polynomial gcds, full lift kernels, constrained lift roots,
the degenerate approximate family and all compensator rows. Its default
mode compares an immutable ledger and checks source hashes and the Lean
receipt with six transitive D0 source pins. Finite fixtures support the stated general analytic proofs; they
are not substituted for those proofs. The research Lean capsule prints
axiom dependencies of seven literal propositions, with no `sorryAx`.

The full-core completeness question remains open. The next unclassified
possibilities include native local/nonlinear lift constraints, genuinely
geometry-dependent operators, nonpolynomial spectral laws with an actual
owner, and combined actions with their complete independent variations.
Each needs a concrete native definition before a physical solver can be
counted toward soundness/recovery. #310's fixed-source raw-owner terminal,
#202 and #317 keep their separate criteria. No claim, release, BOOK text,
supported Lean module or parent status is promoted by this artifact.
