# All-cap noncancellation, finite coupling and source-scope review

21 October 2026. Independent analytical check by the stationary-composition
subagent for the existing native-programme-v1 / PR #334 research route.
This review uses the exact functions supplied in the parent conversation.
The old unit-charge estimate kappa > 53 has **not been re-read in a fresh
checkout**: repository access was unavailable. Its original admission and
pricing assumptions remain a consumed input, not a newly certified fact.
No numerical tests or historical suites were run for this review.

## 1. Exact all-cap calculation: PASS under the stated input

Let p=phi^(-1), z=2^(-20), L=4p^3, A0=L(1+p^6),
Q=1-zL, R=1-zA0, and r0=1-QR. Golden algebra gives

\[
L=1-p^6,\qquad A_0=1-p^{12}.
\]

Since p>3/5, L>3/4; also L<A0<1. Thus

\[
r_0=z(L+A_0)-z^2LA_0
 >z(3/2-z)>z,\qquad r_0<2z=2^{-19}.
\tag{1}
\]

This proves the needed lower bound analytically; an upper bound alone
would not suffice to bound the entropy derivative.

For binary entropy in base phi, phi^2>2 implies

\[
0<h_\phi'(r_0)<\log_\phi(1/z)
 =20\log_\phi2<40,\qquad h_\phi(r_0)<2.
\tag{2}
\]

On the fixed complete-ledger interface, take alpha>0, 0<beta<=1 and
kappa=mu-H_T>53, with these parameters held when differentiating r.
The actual finite-cap field-dependent valuation is

\[
F_N(r)=\alpha[\kappa-\beta h_\phi(r)]E_N(\beta r),
\qquad E_N(t)=\sum_{j=0}^{N-1}t^j.
\]

Its derivative is exactly

\[
F_N'(r_0)=\alpha\beta\{
[\kappa-\beta h_\phi(r_0)]E_N'(\beta r_0)
-h_\phi'(r_0)E_N(\beta r_0)\}.
\tag{3}
\]

For N=1 this is -alpha beta h_phi'(r0)<0. For every finite N>=2,
E_N'>=1 and E_N<1/(1-2^(-19)). Consequently

\[
\boxed{F_N'(r_0)>
\alpha\beta\left(51-\frac{40}{1-2^{-19}}\right)
>10\alpha\beta>0\quad(N\ge2).}
\tag{4}
\]

The final strict inequality uses 41<2^19. There is no cancellation cap.
This applies separately to each cap's real bank/readiness/prefix data if
that cap satisfies the consumed unit-charge bound. It does not assume a
common bank when comparing different caps, a physical infinite bank, or
a uniform lower bound as readiness tends to zero.

**Envelope qualification.** The signs N=1 negative and N>=2 positive
prohibit assigning one universally positive source multiplier to an
arbitrary optimized cap envelope. They do not prove that every envelope
is nonsmooth: an envelope with a unique fixed active cap can be smooth.
At ties or in mixtures, opposite multipliers can cancel; use the actual
same-task price comparison and an active-branch argument instead of
differentiating a presumed smooth minimum. Caps corresponding to
different required tasks cannot be compared as one physical D_min.

## 2. Finite query coupling: PASS, with a necessary calibration distinction

For the stated two-band detector at (x,y)=(0,0), the literal derivatives are

\[
r_x=4zQp^{11},\qquad r_y=8z(Rp^6+Qp^{12}).
\]

Hence for any cap with nonzero outer derivative,

\[
\frac{\partial_y(F_N\circ r)}{\partial_x(F_N\circ r)}
=\frac{r_y}{r_x}
=2p^{-5}\frac RQ+2p.
\tag{5}
\]

Using R-Q=-zLp^6, p^(-5)=8+5p and L=4p^3 gives

\[
\boxed{\rho_z:=\frac{r_y}{r_x}
=16+12p-\frac{8zp^4}{Q}
=10+6\sqrt5-\frac{8zp^4}{1-zL}.}
\tag{6}
\]

The finite correction is strictly positive when subtracted from
10+6 sqrt(5); it is not zero at z=2^(-20). No limit z->0 was taken.

With physical operands x=eta^2 f and y=sigma_sign eta^2 q_mat,
eta!=0 and sigma_sign in {+1,-1}, the two first-source coefficients
are eta^2 F_N' r_x and sigma_sign eta^2 F_N' r_y. Their ratio is

\[
\lambda_{\mathrm{ratio}}=\sigma_{\mathrm{sign}}\rho_z.
\tag{7}
\]

Thus the common eta^2, entropy-log convention and outer cap multiplier
cancel. Do not confuse sigma_sign with a separate native scale also
called sigma (for example p^3 in a preparation owner). Nor may unequal
operand normalizations be silently replaced by this common eta^2.

Equation (7) is the matter/geometric coefficient ratio in these exact
operands. Calling it the original action's lambda requires the owner's
convention J2=f+lambda q_mat, including any density, trace and matter-field
normalization. If the old lambda_minus is -(10+6 sqrt(5)), then for
sigma_sign=-1 the finite ratio is lambda_minus+8zp^4/Q, not lambda_minus.
If that original owner already includes Q,R in lambda_minus, there may
instead be exact agreement; this cannot be decided without its definition.
Neither the small size of the difference nor a rounded decimal resolves it.

## 3. Source scope and the actual positive novelty

The universal auxiliary construction needs only a_N!=0. Equations (3)-(4)
therefore remove its remaining cap-specific noncancellation hypothesis on
the stated actual unit-charge interface. Its auxiliary Hessian determinant
-1 is independent of the Hessian of F_N; no positivity estimate for the
two-density Hessian is required.

The resulting K_N satisfies K_N(0)=F_N(r0) and its first kinetic coefficient
is the actual b_N. On q_mat=f=0 the auxiliary section is constant and the
coframe map is identity, so nonconstant null matter is allowed: dq_mat
need not vanish. All independent field Euler rows follow by the full
source identity, not merely by varying within the null ansatz.

However, null-stratum first-source preservation itself is already the
owned chain-rule mechanism. The new contribution is the explicit exact
stationary normal form with its derived nonlinear kinetic functional,
and this all-cap application. Do not advertise the old null first-source
identity or the already-owned Einstein family as newly proved.

If the old geometric theorem is parametric in its action coefficient,
it can be instantiated at the derived finite ratio (7). That supplies
the corresponding family common to all these caps. It does not preserve
the literally same old metric when its fixed coefficient differs and
the matter source is nonzero. The original weights must also match:
site-dependent compiler multipliers require their actual weighted target
and link/matter source transport, not only equality of b_i/a_i.

Keep the original nondensitized q_mat and measure. The derived K_N is a
nonlinear kinetic valuation in that measure, not automatically the
covariant density sqrt(|g|) P(X). The auxiliary elimination adds no
propagating fields; it is a mathematical stationary equivalence, not a
claim of native physical gates implementing the auxiliary variables.

Finally, generated finite compiler states can use the existing causal
adjoint, but genuine independent preparation, reference and clock inputs
retain their full baseline source DB. Compulsory Book Info, actual
field-writer/variation admission and compatible physical refinement are
not supplied by this cap lemma or by the auxiliary normal form.
