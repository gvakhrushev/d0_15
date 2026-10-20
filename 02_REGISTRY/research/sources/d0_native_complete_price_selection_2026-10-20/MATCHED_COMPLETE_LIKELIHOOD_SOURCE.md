# Completing the matched loop/void likelihood changes its source

Bounded analytical subtask of existing D0 PR #334. Read-only input checkout:
`c7a2e7c39fab6b60fa70a553998e9aa2ccc89f3f`. This is a source test of one
specific proposed information interpretation, **not** a claim that Book03's
algebra-valued action is an expected relative entropy.

## 1. The already owned proposal being tested

The newest `sources/d0_native_triz_reference_2026-10-20/TRIZ_MATCHED_LOOP_VOID_SOURCE.md`
uses the original positive feedback effect `0 <= A <= I`, `z=2^-20`, and

\[
J(A)=-128\operatorname{Tr}\log(I-zA)
 =\sum_{r\ge1}\lambda_r(A),\qquad
\lambda_r(A)=128z^r\operatorname{Tr}(A^r)/r.
\]

Independent mathematical Poisson counts with means `lambda_r` have zero-count
probability `exp(-J)`. A co-transported reference `A_0(e)=A(e,U_0)` therefore
gives the **one specified event** log likelihood contrast

\[
C_{\mathrm{void}}(e,U)=J(A(e,U))-J(A(e,U_0))
 =\log\frac{Q_e(N=0)}{P_{e,U}(N=0)}.
\tag{1}
\]

Its mixed coframe/link derivative may be nonzero. The positive construction
and its existing exact noncommutative mixed-source formula remain valid.
What follows answers the additional question: does completing this contrast
to the mean information of **all** count records preserve that mixed source?

## 2. Full normalized histories: exact diagonal cancellation theorem

Let `P(e,u)=(p_w(e,u))` be a C2 normalized positive distribution over one fixed
finite complete record set, including failures, duration, controls and any
other records actually retained. Let `Q(e)=P(e,0)` use the same moving
coframe and a held reference link. Set

\[
D(e,u)=\sum_w p_w(e,u)\log\frac{p_w(e,u)}{q_w(e)}.
\]

Then **for every e**, not merely at one field base,

\[
D(e,0)=0,\quad D_uD(e,0)=0,\quad D_eD_uD(e,0)=0,
\quad D_e^kD(e,0)=0.
\tag{2}
\]

Proof: at `u=0`, `p=q` and
`D_u D = sum_w (partial_u p_w)(log(p_w/q_w)+1)
 = partial_u sum_w p_w = 0`.
This identity holds for every e; differentiate it in e. Normalization is
the full reason. It does not require independence or any special Kraus law.
On a countable record set, impose the usual absolute dominated first/second
derivative summability; the statement is also immediate at every finite cap
when the unresolved/capped outcome is retained.

For two active-link tangents v,w, its exact remaining Hessian is

\[
D^2_{u_vu_w}D(e,0)=\sum_\omega
 \frac{p_{u_v,\omega}(e,0)p_{u_w,\omega}(e,0)}{q_\omega(e)}.
\tag{3}
\]

Thus a moving *common* coframe is a null row of the full local divergence
Hessian; the actual link-link Fisher block can survive. Moving the shared
reference must be included in (2); freezing it while differentiating e is
a different experiment. Reversing the divergence arguments, or reversing
the sign of the expected log likelihood, does not restore the mixed jet.

One can bypass strict positivity for (2): any C2 divergence which is
nonnegative and vanishes at the matching diagonal has a local minimum there.
Its u differential is zero at each e. This applies to rank-deficient models
only where the asserted C2 regularity actually holds; no smoothness at
support birth is assumed.

This also covers expected Bayesian information gain for two independently
labelled hypotheses: for any strictly interior prior it is their weighted
Jensen--Shannon divergence, nonnegative and zero when the two complete
output laws agree. Allowing that prior to move with e does not change the
zero diagonal. Thus simply replacing relative entropy by expected
distinguishability gain does not supply the missing mixed action jet.

### Quantum complete-record version

On one fixed finite Hilbert fibre, let `rho(e,u)>0` and
`sigma(e)=rho(e,0)>0` be normalized density matrices for the **complete**
retained quantum output. Umegaki relative entropy

\[
D_q(e,u)=\operatorname{Tr}\rho(e,u)
 [\log\rho(e,u)-\log\sigma(e)]
\]

has the same identities (2). For Hermitian trace-zero active tangents
`X_v=partial_{u_v}rho(e,0)`, its active Hessian is

\[
D^2_{u_vu_w}D_q(e,0)=\operatorname{Tr}
 \left[X_v\,\mathcal L_{\sigma}(X_w)\right],\qquad
\mathcal L_\sigma(X)=\int_0^\infty
 (\sigma+sI)^{-1}X(\sigma+sI)^{-1}\,ds.
\tag{4}
\]

Proof: `d Tr rho log rho = Tr(d rho)(log rho+I)` and
`Tr d rho=0`; first variation at `rho=sigma` is zero. Differentiating
the matrix logarithm gives (4). In a diagonal basis the logarithmic
divided differences are positive; hence (4) is positive semidefinite.
Noncommuting coherences remain in this formula. Pure complete states can
give infinite relative entropy against a distinct pure reference, so they
cannot be inserted into this faithful-state formula by declaration. The
C2 nonnegative-divergence argument above states exactly the extension
available on a smooth common-support family.

## 3. Application to the exact positive Poisson construction

Write `lambda_r=lambda_r(A(e,u))`, `mu_r=lambda_r(A(e,0))`. For finitely
many loop species R, the full log likelihood is

\[
\log\frac{P(N)}{Q(N)}
 =\sum_{r=1}^R\left[-\lambda_r+\mu_r
       +N_r\log\frac{\lambda_r}{\mu_r}\right].
\tag{5}
\]

Taking the expectation over **all** outcomes gives exactly

\[
D_R(P\|Q)=\sum_{r=1}^R
 \left[\lambda_r\log\frac{\lambda_r}{\mu_r}
       -\lambda_r+\mu_r\right].
\tag{6}
\]

The zero-count record gives `-C_void` in (5). The nonzero count records
supply `sum lambda_r log(lambda_r/mu_r)`. At the matched diagonal their
linear response cancels **every** `-partial_u lambda_r`; differentiating
that cancellation in e cancels the mixed response too. Equivalently,

\[
\partial_e\partial_uD_R|_{u=0}=0,\qquad
\partial_u^2D_R|_{u=0}=\sum_{r=1}^R
 \frac{(\partial_u\lambda_r)^2}{\mu_r}.
\tag{7}
\]

On any compact strict positive chart `delta I <= A <= (1-delta)I`, the
series and its first two derivatives converge absolutely: powers in
`lambda_r` have at most polynomial r growth in their relative derivatives
while `z^r` supplies a geometric majorant. Thus (6)--(7) hold for all
species as R tends to infinity. The mean total loop count is finite.
General positive-semidefinite charts are covered only when the same
support/regularity conditions hold; the exact finite-cap theorem never
needs to drop an unresolved outcome.

**Parent consequence.** The owned original P25 shared-link/coframe family
has `S_star(a,t)=(1-a)sin t`, hence
`partial_a partial_t S_star(1,0)=-1`. No nonzero constant multiple of
that mixed action jet is the completed matched KL in (6). This rules out
the specific proposed identification of the signed void contrast with
complete mean relative information. It neither invalidates the void
probability identity nor excludes an actual Book action with additional
paid source terms or a different algebra-valued/statistical aggregation.

The adjacent checker consumes the SAME positive 2x2 effect family used
by the newest loop/void checker, with no invented replacement geometry.
Its void mixed source is nonzero, yet its full mean mixed source is exactly
zero for loop truncations R=1,2,3 and by (7) for every R. A second
noncommuting fixture also has a nonzero surviving Fisher link-link block.

## 4. Complete Cost minus Shannon: the exact residual that cannot be hidden

Let `ell=log(phi)` and let `C_w(e,u)` be the **actual** total charge of
record w in Golden units. For arbitrary complete classical P and faithful
reference Q, without selecting Q as a physical code,

\[
\boxed{\mathcal S=\mathbb E_P C-H(P)/\ell
 =D(P\|Q)/\ell+\mathbb E_P B,\qquad
 B_w=C_w+\log q_w/\ell.}
\tag{8}
\]

This is an identity, not a derived native price. The second term is the
actual mismatch between paid charge and reference surprisal. At the matched
diagonal, **all** coframe-link mixed source comes from this term:

\[
\partial_e\partial_u\mathcal S|_{u=0}
 =\sum_w[p_{eu,w}B_w+p_{u,w}B_{e,w}
       +p_{e,w}B_{u,w}+q_wB_{eu,w}]_{u=0}.
\tag{9}
\]

Clock/control/preparation terms may be present in C and every derivative
in (9) must then be retained. If charge is exactly matched cross-code
`C_w=-log_phi q_w+c(e)` with no active-u dependence, then B=c(e), and
(9) is zero. Full normalized matched coding therefore cannot create the
required mixed source, even if the reference is physically paid.

For fixed actual record charges independent of e,u, (9) reduces to

\[
\sum_w p_{eu,w}(C_w+\log_\varphi q_w)
 +\ell^{-1}\sum_w p_{u,w}q_{e,w}/q_w.
\tag{10}
\]

There is **no universal sign** of (9) or (10) for unspecified charge and
native Info. The equality states the missing binding; it must not be
replaced by choosing B to fit a desired Palatini tensor.

## 5. A directly native all-launch flat-scale test

Reuse the original all128 invariant-shell identity in
`sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md`
and the full data/reference map in
`sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md`.
For the actual `n=128L^2`, `epsilon=p^2h^2/64`, `beta=n epsilon=2p^2`,
lowest shell `Delta=rho mu_(1,L) I`, `mu_(1,L)=2-2cos(2pi/L)>0`,

\[
\mathbb E C_{\mathrm{port}}=n+p\beta\rho\mu_{1,L},
\qquad \partial_\rho\mathbb E C_{\mathrm{port}}
 =p\beta\mu_{1,L}>0.\tag{11}
\]

It sums **all128^n** native histories with their actual costs; the IID port
identity computes that expectation without replacing the fine tape.
For a matched full-history reference `Q_rho=P_(rho,U0)`,
`D(P_(rho,U0)||Q_rho)=0` identically in rho. Therefore a proposal

\[
\mathcal S_{\rm candidate}=\mathbb E C_{\rm port}
                 +bD(P\|Q)/\ell
\]

has source (11) at the matched flat link for **every fixed b**, positive
or negative. The matched information alone cannot cancel the real paid
port source. Nor can a field-independent paid baseline change (11).
This is an exact finite-source obstruction for this stated candidate; the
source tends to zero as h^2, so it is not by itself a no-go for a different
normalized continuum or a complete physical price with other terms.

For comparison only, on the actual port marginal the different candidate
`E C_port-H(port)/ell` has exact derivative

\[
n r'(\rho)\left[1-\log_\varphi\frac{1-r}{r}\right],
\quad r=p\epsilon\rho\mu_{1,L}.
\tag{12}
\]

It is strictly negative for `0<r<p^2`, vanishes at `r=p^2`, and is positive
above it. This is **not** a claim about the entropy derivative of the full
fine pointer or coherent record; those keep their conditional fine-label
and coherent terms. Equation (12) demonstrates why selecting an information
algebra or interpreting KL as Shannon without binding the actual cost
changes the equation, even on the same instrument.

## 6. Scope and route change

The source-preserving matched **void observable** is sound. Its promotion to
the complete **mean relative-information action** loses the very mixed
source intended to supply P25. The complete price must derive a nonzero
source from the actual residual (8), from another owned action aggregation,
or from a genuinely different admitted task. No fitted cancellation or
unrecorded conditional return is supplied here. Physical Book03 selection,
all40+2 matching, upstream constraints and GR remain open.

There is a precise preserved alternative: when one complete outcome is
**already independently retained as evidence**, field alternatives can be
compared at that same fixed evidence rather than averaging over a newly
generated record. For actually fixed zero-count evidence the log likelihood
contrast is still (1) and retains the owned mixed source. This is a
different variational problem. Its native task, actual fixed evidence and
full payment must be derived; selecting the void event merely because it
has a desired source would not establish that problem. The cancellation
theorem must not be used to declare this pathwise/algebra-valued Book route
impossible.

The calculation is elementary normalization/Poisson algebra; the broader
standard relation between relative entropy's quadratic term and quantum
Fisher information is discussed in Lashkari and Van Raamsdonk,
`https://arxiv.org/abs/1508.00897`. That paper's holographic hypotheses are
not imported into D0 or used to claim a gravitational derivation.
