# Independent analytical review: finite-cap propagation and radial reduction

21 October 2026. Cross-check by the stationary-composition task agent,
independent of the two derivations' authors. This is an internal analytical
review, not external peer review or a fresh replay of original native
implementations. No additional numerical test suite was created.

## 1. Sources reviewed

- [All-cap nonlinear matter response and exact null-background propagation](../../A4D_ALL_CAP_NULL_MATTER_CAUSAL_CONE_2026_10_21.md),
  including the correction that the held coframe is the reduced coframe,
  and the condition on retained baseline/collar matter sources.
  Restored publication-copy SHA256:
  d089347aab15853075561eb292c03499dac5197a73f84745010b70131f53ab29.
- [Exact native radial minimization and all-order matter normal form](../../A4D_EXACT_NATIVE_RADIAL_MINIMIZATION_ALL_ORDERS_2026_10_21.md).
  The mathematics was first read in its complete working draft. The
  restored, more compact publication copy was read again; its equations,
  estimates and source boundaries agree with that reviewed derivation.
  Restored publication-copy SHA256:
  6507bbbc15bce28a2352564c3e0d8102bbd4435d13fcd39827d1cab61a130621.

The unit-charge premise kappa>53 is a consumed input of both texts.
Its original implementation provenance has not been reverified here.
The scalar price parameters are held in the density derivatives.

## 2. All-cap normalized curvature: PASS

Direct differentiation of the displayed detector gives the three
derivative ratios in equation (8) of the propagation note. Substitution
into its normalized response yields

\[
S_z=45+31\varphi-\frac{32zp^5}{Q}
       +\frac{16zp^{12}}{R+p^6Q}.
\]

The finite correction is confirmed by p^6-p^3=-2p^5.
The stated bounds 4<S_z<97 and 4r_y<(16/5)z follow from the given
golden inequalities.

For N>=2 the exact outer logarithmic derivative has numerator
-h''E_N-2 beta h'E_N'+beta A E_N'' and denominator
M=A E_N'-h'E_N. The estimates M>10 and M>A/5 justify all the
upper and lower bounds used in the note. With d=1-2z, the upper-bound
condition reduces to

\[
1-182z+60z^2-40z^3>0
\]

at the stated z=2^(-20). The derivation actually gives
-98<theta_N<-3 for N>=2 and -113<theta_1<-4. The convenient common
bound -128<theta_N<-3 is therefore valid.

The numerical constants refer to the original detector coordinate Y.
For Y=c q the physical normalized kinetic curvature is c theta_N.
In particular, the sign c=-eta^2 is essential to the claimed narrowing
of the ray cone. No absolute kinetic-energy or full-action minimum
statement follows from these signs.

## 3. Principal metric and exact rotating propagation: PASS with stated scope

The null rank-one inverse and determinant formulas are exact. For
chi>0 in signature (+---), effective-null vectors obey
g(v,v)=chi(ell.v)^2>=0; the claimed nesting concerns ray cones, with
the covector cones ordered oppositely.

The full linearized kinetic equation on the reduced Brinkmann
background has no omitted derivative of C(u): the extra current is in
the v direction, so its divergence differentiates v, not u.
With partial_v represented by ik, the proposed ODE

\[
U'=-ikc\theta_N CC^TU
\]

has the correct sign:
2ikU'=2c theta_N k^2 CC^TU, canceling the added matrix term.
The generator is anti-Hermitian even for a rotating internal profile.
Thus the ordered solution is unitary, preserves Fourier reality, and
intertwines both operators, including the k=0 mode.

Integrating this ODE gives

\[
\|U-I\|\le\min\{2,128|k|\eta^2\mathcal E(u)\}.
\]

The H^1-in-v to L^2 comparison follows directly by Plancherel. The
bound is uniform in the stated finite-cap interface, with the profile,
scalar coefficients and comparison background held as specified.

The restored publication now explicitly uses v on the real line with
appropriate transform regularity, or periodic v. Boundary conditions
must be transported with U; the fixed-endpoint problem with unchanged
boundary data is not asserted to be equivalent. This qualification is
consistent with the translation and Fourier-multiplier proof.

The source-scope correction is necessary and is now present: holding
the transformed coframe does not hold the original coframe, because
delta e_original=-delta pi e/(2a). Baseline or collar terms with a
matter variation also retain their first and linearized sources.
Without their stated absence, the intertwiner concerns the displayed
kinetic sector alone. This is not a full coupled lattice or original-
geometry hyperbolicity theorem.

## 4. Explicit radial branch and all-order kinetic function: PASS

The identity r=R(y)+A(y)(x-x^2/p) follows exactly from the native
detector. Its trace equation has the stated quadratic coefficients.
The rationalized small-root formula is correct; the other root remains
outside |x|<1/4 on the proposed interval.

The bounds 12<C<36, Delta>3/4, |tau|<48|y| and 0<tau'<50
are supported by the displayed derivative formulas. In particular,
the estimates for A''/A and R''/A correctly retain the derivative of
the factor c(y). They give the claimed bounds on the derivative of
log r_x and on rbar'.

The finite-cap logarithmic derivative bound is also valid. The middle
numerator term is controlled by

\[
\frac{2\beta h'E_N'}{D_N}
 <\frac{10h'}{J}<\frac{400}{51}<8,
\]

using D_N>J E_N'/5; no cap-dependent growth is hidden in that step.
Consequently the stated normalized coframe scale interval and strict
monotonicity of Y(y)=y/u(y) follow. The common target interval
|Y|<2^(-13) is covered for every admitted fixed finite cap.

The parametric K_N, its auxiliary section, and the identity

\[
K_N'(Y_N(y))
 =\frac{[g_N'(\bar r(y))]^2}{a_N}\,
    r_x(\tau(y),y)r_y(\tau(y),y)
\]

are exact, including at the null endpoint. They do not require the
physical density queries to be independent coordinates.

## 5. Actual partial minimization and its limits: PASS

The invariant xy together with the sign quadrant fixes a unique
representative on the small trace branch. The radial Hessian has sign
sign(g_N' y), and the other quadratic root fixes the derivative sign
throughout each stated connected orbit segment. Therefore the result
is a genuine minimum of the original signed local price on that
segment: y<0 for N=1 and y>0 for N>=2. The opposite branches are
maxima. No division by the possibly negative curvature coefficient is
used to relabel a maximum as a minimum.

The product-site conclusion requires the factorization, positive
weights and radial independence of the baseline stated in the draft.
It does not establish a minimum over coframe shapes, shared links,
matter or internal preparation. The signed square-root asymptotics of
the profiled invariant price are consistent with an analytic K_N in
its different coordinate.

Finally, the uniform-response full-source transfer and its Hessian
formula are exact chain-rule identities, conditional on an actual
uniform-response full critical point. The trace branch alone does not
construct that point. No full nonnull finite-lattice Einstein solution,
native action inevitability, compulsory Book information or physical
clock is certified by this review.

## 6. Frozen checker and receipt review: PASS within the stated scopes

The source of [check_explicit_branch_and_propagation.py](check_explicit_branch_and_propagation.py)
and its saved [CHECK_RESULTS.json](CHECK_RESULTS.json) were independently
read. Both the checker hash and its imported parent-checker hash agree
with the receipt and the current bytes on disk:

- Checker SHA256:
  efc80841b6223e1e26c09c0e8b596c4a3d85f2714256190efdad7913b962c431.
- Parent checker SHA256:
  c4ae04cdc4b3f5b1e6e23d922f26329448d723eb9b6cfeea4fc41e3e61d2b031.
- Receipt SHA256:
  8391264de003ab306850923608f5434c65f44702879c7fb19b2d06ee56627a64.

The exact section uses the parent's rational golden-field arithmetic and
rational comparisons for S_z, derivative signs, the discriminant constant
and the uniform estimates. Its nonzero-point polynomial checks are
correctly labelled as evaluations; the all-argument identity comes from
the supplied expansion proof.

The explicit branch section checks 12 cap/parameter combinations and
9 density points each using 90-digit Decimal arithmetic. It includes a
different Newton route through the original auxiliary equations and a
direct radial Hessian calculation. The saved largest normalized trace
residual is approximately 2.09e-91; the auxiliary residual is 2.7e-91,
and the Newton comparison is approximately 7.97e-72. These are numerical
diagnostics, not interval certificates or proofs of a uniform domain.

The rotating transport fixture actually uses noncommuting projectors:
their displayed commutator has maximum-entry magnitude about 0.4496.
Its closed form is U=R(u) exp(Mu), with
M=-omega J-ik gamma P_0. The centered constant matrix squares to
-[omega^2+(k gamma/2)^2]I, which verifies the exponential formula.
Differentiating this closed form cancels the rotation generator and
gives the intended ordered ODE; it is not a commuting approximation.

The comparison wave on H=x^2+4y^2 is also consistent:
the Gaussian has transverse Laplacian (k^2 H-3k) times itself, while
2ik times its u derivative is -3k times itself. Thus the unperturbed
wave equation vanishes before applying U. The test uses a curved
reduced-background kinetic fixture, not a claimed simultaneous native
gravity-matter background solution. The saved largest corrected wave
residual is 8.88e-16 and the unitarity residual is 4.44e-16; these are
IEEE complex diagnostics.

The added Bianchi subsection is distinguished appropriately: its
curvature expressions are exact coefficient identities in Q[t,t0],
whereas its metric-source cancellation is a 90-digit diagnostic at
one nonzero branch point and four caps. This checker inspection does
not replace the separate review of the complete Bianchi theorem or
establish the original native finite-lattice equations.

This review binds the existing successful execution to the inspected
sources and checks its mathematical scope. It did not add another
test suite or claim a new independent native-compiler replay.

