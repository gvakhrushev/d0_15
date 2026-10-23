# Independent review: complete-price nonvacuum stationary normal form

**Review date:** 21 October 2026, Europe/Moscow.  
**Reviewer:** a separate analytical review agent; this is not an external
human peer review or a Lean formalization.  
**Mathematical theorem:** **PASS**, under its explicitly stated carrier,
support and free-variable hypotheses.  
**Displayed native-detector application:** **PASS** as an algebraic deduction
from the supplied formulas and the consumed unit-charge premise.  
**Current original-repository interface:** **CONDITIONAL / NOT REPLAYED**.  
**Closure:** `GR_closed = false`.

The complete proof was read, including its statements about fixed collars,
moving dictionaries, correlated prices, finite coupling, critical inertia
and retained internal sources. The exact algebra was independently derived.
The checker was inspected and executed once in a separate process. No
mathematical correction remains in the reviewed theorem. The final two
provenance-only paragraph edits were then read: they correctly make the
unit-charge bound an explicit consumed premise and remove an unverified
attribution to one source file. The final proof has 31,632 bytes.

## 1. Reviewed artifacts and execution

| Artifact | SHA-256 of the reviewed bytes |
|---|---|
| `A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md` | `314f067f683a36eeaf68da513d5aa84a053521d065503a2468f63417ca96193b` |
| `check_nonvacuum_normal_form.py` | `c4ae04cdc4b3f5b1e6e23d922f26329448d723eb9b6cfeea4fc41e3e61d2b031` |
| `CHECK_RESULTS.json` | `4dcff347751b0dc1c26afd61c1d1fc1e34878f8f55f2087f3d7f944be6e13cb2` |
| `CAP_AND_COUPLING_REVIEW.md` | `21f88c364caf0828e64f14f6933828cdc63da87df19b22a117d2c2da2bdb487c` |

The independent checker execution completed **PASS** with Python 3.12.14
at `2026-10-20T21:44:39.540681+00:00`, with no stderr. Its self-reported
script digest was compared to the bytes actually read and agrees with the
table. The original `CHECK_RESULTS.json` was not overwritten.

The exact `Fraction` fixture has two coupled sites and twelve independent
coordinates. It checks the extended-function identity through its full
value, gradient and Hessian, including shared variables and moving
dictionary terms. Its curvature Hessian is singular by construction; the
auxiliary inverse and the independent Schur calculation still succeed.
Its nonzero null-matter example has a nonzero kinetic differential. Removing
either its baseline derivative or its dictionary-source terms fails the
corresponding comparison.

The ordered field calculation checks the finite coefficient identity and
strict inequalities in exact rational arithmetic over `Q(sqrt(5))`.
The all-cap derivative conclusion is an analytic inequality, not inferred
from enumerating the tested caps.

The 85-digit Decimal diagnostics solve the new auxiliary branch at nonzero
`Y = -1e-4, +1e-4` for caps 1, 2, 7 and 31. The largest reported auxiliary
residual is approximately `5.91290e-67`; the largest reported relative
error in the central derivative comparison is approximately
`2.50699e-21`. These are **non-interval diagnostics** for the illustrative
parameters `alpha=3/5, beta=5/7, kappa=54`. They do not certify a native
preparation bank, a uniform implicit-function neighborhood, or the original
40 geometric plus two matter equations. The analytic theorem does not
depend on these small numerical residuals.

## 2. The exact stationary theorem passes

The decisive hypotheses are independent sitewise homogeneity

\[
x_i((\sqrt{u_j}e_j)_j)=u_i x_i(e),\qquad
y_i((\sqrt{u_j}e_j)_j)=u_i^{-1}y_i(e),
\]

and nonzero `a_i = F_{x_i}(0,0)`, on the declared product domain of free
coframes. A common global scaling identity alone would not suffice.
The density dictionary may be singular, and the density values need not
be independent field coordinates.

The auxiliary extension

\[
\widehat S=B_{\rm tot}+F(s,y)+\sum_i\pi_i(x_i-s_i)
\]

has the unique original-chart auxiliary section `s=x`, `pi=F_x(x,y)`.
It therefore reproduces the actual original action, its critical points
and its stationary values exactly. On `pi_i/a_i>0`, the simultaneous
coframe map `e_tilde_i=sqrt(pi_i/a_i)e_i` is an invertible map of the
extended carrier. It converts the function exactly to

\[
B_{\rm tot}+\sum_i a_iX_i+
F(s,((\pi_i/a_i)Y_i)_i)-\sum_i\pi_i s_i.
\]

At `Y=0`, the auxiliary root is `s=0, pi=a`. Its block and inverse are

\[
H_{\rm aux}=\begin{pmatrix}F_{xx}&-I\\-I&0\end{pmatrix},
\qquad
H_{\rm aux}^{-1}=\begin{pmatrix}0&-I\\-I&-F_{xx}\end{pmatrix}.
\]

The inverse is verified by multiplication. Each block has exactly one
positive and one negative auxiliary direction per free site. The
implicit-function theorem therefore applies even when `F_xx` is singular
or indefinite. It defines the unique local derived function `K(Y;zeta)`.

The sequence of exact auxiliary extension, extended-coordinate
diffeomorphism and stationary elimination proves a local bijection of
full critical sets and equality of the associated stationary values.
It does not require convexity, invertibility of the physical Hessian,
or a new physical field law. It is a stationary normal form, not an
asserted field-only off-shell equality. In particular, away from critical
points the new auxiliary section need not satisfy the old `s=x` equation
at fixed original coframe. The proof explicitly respects this distinction.

For a correlated ledger, the same proof gives a correlated `K`. A local
sum of kinetic functions follows only from the corresponding factorization
of the actual price. The original nondensitized query and measure remain
unchanged; the theorem does not establish a generally covariant continuum
`sqrt(|g|) P(X)` matter action.

## 3. The derived positive matter coefficient is substantive

With `D=diag(b_i/a_i)`, differentiation of the auxiliary equations gives

\[
K_Y(0)=b,\qquad
K_{YY}(0)=F_{yy}+D F_{xy}+F_{yx}D+D F_{xx}D.
\]

This is precisely the density Hessian restricted to the trace-compatible
directions `(D v,v)`. For a single density pair,

\[
K''(0)=F_{yy}+2(b/a)F_{xy}+(b/a)^2F_{xx}.
\]

The formula follows independently from the Schur complement of the
auxiliary block. The same direction arises directly from the original
free-coframe trace equation `x F_x-y F_y=0`. Thus the higher response is
fixed by the original price and its actual conformal stationarity
condition; it is not an independently chosen compensator.

For the displayed one-stage detector, `r_x,r_y>0` and all three entries
`r_xx,r_xy,r_yy` are strictly negative at the base point. Consequently,
with `w=(b/a,1)` and `b/a=r_y/r_x>0`,

\[
K''(0)=-\alpha\beta\left[
h_\varphi''(r_0)(Dr\,w)^2+
h_\varphi'(r_0)w^TH_rw\right]>0.
\]

Here `h_phi'(r0)>0` and `h_phi''(r0)<0`. Both terms inside the brackets
are negative. This is a direct analytic sign proof; it does not consume
a positive-definiteness claim about the full two-density Hessian.
The forced nonzero nonlinear matter term, together with the all-order
stationary representation, is the new positive content beyond the
already-owned first-source identity on the null stratum.

## 4. Fixed collar, shared links and genuine source equations

The final theorem uses the safe domain: only actually free coframes
receive auxiliary pairs and are rescaled. Held collar coframes remain
literally unchanged. A retained collar price may depend on shared links,
neighboring matter values and internal variables; all of those derivatives
remain present. It can be called a spectator only if it is independent
of the free coframes. A buffered support can establish that independence,
but the word "collar" does not establish it by itself.

This qualification is necessary. For example, take `x=e^2 z`,
`F(x)=x+x^2/2`, a spectator `B(z)=-z`, and fixed original `e=1`.
The constrained original action is `z^2/2`. If one also dresses this
fixed coframe, the transported constraint is `e_tilde^2=pi`. Eliminating
auxiliaries freely at fixed `e_tilde` gives `s=0, pi=1`; imposing the
constraint only afterwards would incorrectly leave the identically
zero action. The correctly constrained variation gives `s=z, pi=1+z`
and retains `z^2/2`. The reviewed theorem avoids precisely this error.

On the common null stratum, the correct full source is

\[
dS=dB_{\rm tot}+\sum_i(a_i\,dX_i+b_i\,dY_i).
\]

In particular, for a moving internal dictionary,

\[
D_\zeta S=D_\zeta B_{\rm tot}
 +\sum_i(a_i D_\zeta X_i+b_i D_\zeta Y_i).
\]

The pointwise equations `X_i=Y_i=0` do not set these differentials to
zero. Nonconstant null matter with a nonzero ambient stress differential
is fully compatible with the theorem. Baseline normalization must carry
the original value and its entire derivative into `B`; this is explicit
in the proof. Generated or constrained internal coordinates must retain
their actual pullback rather than be silently treated as independent.

## 5. Inertia and minima

At a genuine full critical point on the declared free-variable domain,
both auxiliary eliminations add the same hyperbolic inertia `(n,n,0)`.
The extended diffeomorphism gives Hessian congruence at that critical
point. Subtracting the common auxiliary inertia proves equality of all
positive, negative and null dimensions of the two physical Hessians.
Gauge degeneracy does not invalidate this argument.

This statement also applies on a conditional slice when its internal
parameters are explicitly held. If the internal parameters are free
and the retained internal source is nonzero, the geometric configuration
is not a full critical point and the full Hessian-congruence argument
cannot be invoked there. The proof correctly states the full-critical-point
condition. An old negative physical direction is not removed by adding
or eliminating the algebraic pairs. No minimizing physical execution
is proved by this stationary equivalence.

## 6. Native cap, finite coupling and nonvacuum consumer

The analytic cap calculation passes under the consumed premise
`kappa=mu-H_T>53`, with `alpha>0`, `0<beta<=1` on the same fixed
unit-charge interface. It yields a negative slope for cap 1 and a
strictly positive slope greater than `10 alpha beta` for every fixed
finite cap at least 2. It establishes noncancellation separately for
those actual fixed-cap prices. It does not prove noncancellation in
an optimized envelope or mixture with opposite slopes, or a uniform
physical infinite-bank limit.

The exact finite query coefficient is

\[
\rho_{z_\star}=\frac{r_y}{r_x}
=10+6\sqrt5-\frac{8z_\star p^4}{1-z_\star L}.
\]

Its correction at `z_star=2^-20` is nonzero. With the displayed common
operand normalization, the physical coefficient is `sigma rho_zstar`.
Calling this the old owner's `lambda_minus` requires its exact original
normalization. If that owner uses the literal limiting coefficient,
the old metric is not unchanged in the nonzero-matter sector merely
because the finite correction is small. A parametric owner can instead
be instantiated at the derived finite coefficient to supply the
corresponding new common curved family. The reviewed proof makes this
distinction explicitly.

Common coefficient ratios alone also do not establish equality of the
complete geometric and matter equations when site multipliers differ.
The total linear source must match the original owner's actual weights,
shared-link and matter stencils, and held collar. A single nonzero common
multiplier on a fixed-parameter field block preserves its critical set;
arbitrary site-dependent multipliers need not.

## 7. Precise final scope

The mathematical positive result passes: the declared complete nonlinear
two-density price has an exact local stationary Palatini normal form
with a uniquely derived nonlinear kinetic response. Its common null
sector retains the entire ambient first source, and the displayed
one-stage price has a forced positive quadratic matter coefficient.

The current environment did not provide a fresh checkout or original
remote source bodies. The independent review therefore does not certify
that every current native operand, source owner or carrier definition
has been replayed. The sitewise matter homogeneity, complete-ledger
dependency, actual variation admission, consumed unit-charge premise,
finite coefficient and weights must match the original repository
interfaces when this theorem is consumed there. The original all40
and matter checkers, native preparation bank, physical clock equations,
independent preparation roots and uniform refinement were not rerun.

Those are concrete application and physical-selection conditions;
they do not create an algebraic gap in the theorem proved here. The
normal form retains the unsolved internal source rather than declaring
it zero. No obligatory complete D0 action, unique minimizing execution
or full general-relativistic closure follows from the reviewed result.
No remote publication was performed by this reviewer.
