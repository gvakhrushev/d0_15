# A finite bridge from paid histories to a prescribed action

**Date:** 2026-10-21.  
**Status:** exact finite mathematical criterion, with proofs. Its identity
has not been verified for the actual native compiler kernel in the current
environment. It is not a new proof of physical action admission or GR closure.  
**Closure flag:** GR_closed = false.

## 1. The finite value identity

Let a finite native execution have complete recorded histories H, their
actual probabilities q_H(theta), and their actual paid costs. The variables
theta include whichever geometry, matter, preparation and clock coordinates
are genuinely admitted. Let A(theta) be an independently specified target
action, with its existing measure, coupling and boundary conventions.

The constructive criterion is that, after retaining the actual conditional
quantum entropy, the following scalar be the same on every complete history:

\[
\boxed{d_H(\theta)+\log_\phi q_H(\theta)=A(\theta)
\quad\text{for every admitted complete }H.}
\tag{1}
\]

Here d_H is defined from the real ledger below. It is not fitted to A.
Identity (1) fixes both the Gibbs probabilities and their paid normalization.
It turns conditional history minimality into the exact value A, with all
field derivatives, not just the same probabilities or a linear response.
For an additive finite compiler graph, it can be checked by a finite
relative cycle basis with its actual endpoints retained.

The already proved
[complete-price stationary normal form](A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md)
provides a precise target for such a comparison, including its derived
nonlinear kinetic functional. This note does not replace that functional
by canonical matter or its fixed measure by a covariant volume density.
The actual identity (1), and any relation between its A and that target,
remain to be established from the native ledger.

## 2. Complete CQ information must be retained

Work on a smooth finite support chart: q_H>0, sum_H q_H=1, and the set of
allowed histories is fixed. Suppose the actual retained record is the CQ
direct sum

\[
\Omega_\theta
 =\bigoplus_H q_H(\theta)\rho_H(\theta),
\qquad \operatorname{Tr}\rho_H=1.
\tag{2}
\]

The blocks are quantum density operators. No commutativity inside a block
is assumed. Orthogonality is supplied by the actual classical record
register; a coherent unrecorded history is not silently measured to obtain
(2). With entropy measured in base phi,

\[
S_\phi(\Omega)=H_\phi(q)+\sum_Hq_H S_\phi(\rho_H).
\tag{3}
\]

Suppose the actual cost decomposition is
C_actual=B_C+sum_H q_H c_H. Define

\[
d_H:=c_H-S_\phi(\rho_H),\qquad
R_I:=S_\phi(\Omega)-I_{\rm owned}.
\tag{4}
\]

Thus conditional quantum entropy is retained in d_H, while any difference
between the owned information functional and CQ entropy is retained in R_I.
In particular, no choice of a different Book information functional is
made. An owned input-entropy subtraction, a reference term or a remaining
baseline source must occur in B_C or R_I as its real ledger dictates.

The exact price is

\[
F_{\rm actual}
 =B_C+\sum_Hq_H d_H-H_\phi(q)+R_I.
\tag{5}
\]

If and only if the owned information here is exactly the CQ entropy in
(3), R_I vanishes. A field-dependent R_I or B_C cannot be dropped from
the source. Smoothness of the entropy expressions is part of the stated
support chart; rank-changing quantum blocks require separate treatment.

## 3. Exact Gibbs gap, including its first and second sources

Define the independently cost-determined weights and Gibbs law

\[
w_H=\phi^{-d_H},\qquad
Z=\sum_Hw_H,\qquad p_H=w_H/Z.
\tag{6}
\]

Expanding the relative entropy gives the exact identity

\[
\boxed{
F_{\rm actual}
 =B_C-\log_\phi Z+D_\phi(q\Vert p)+R_I,
}
\qquad
D_\phi(q\Vert p)=\sum_Hq_H\log_\phi(q_H/p_H).
\tag{7}
\]

Indeed log_phi p_H=-d_H-log_phi Z. Substituting this in D and using
sum_H q_H=1 proves (7). This is a finite identity and invokes neither an
infinite history nor a thermodynamic limit.

For the fixed data d_H, the functional sum_H r_H d_H-H_phi(r) has the
unique minimum -log_phi Z over the full probability simplex, attained
at r=p. This mathematical minimization proves a physical selection rule
only if those variations of r are actually admitted and the d_H remain
held under them. In particular, varying a branch probability while
independently holding a causally generated quantum block is not
automatically a native operation.

If q=p at a point theta_0, then the first derivative of the gap vanishes:

\[
D_\phi(q\Vert p)|_{\theta_0}=0,\qquad
dD_\phi(q\Vert p)|_{\theta_0}=0.
\tag{8}
\]

For admitted tangent vectors u,v, its Hessian there is

\[
\boxed{
d^2D_\phi(q\Vert p)[u,v]
 =\frac1{\ln\phi}\sum_H
 \frac{(dq_H[u]-dp_H[u])(dq_H[v]-dp_H[v])}{p_H}.
}
\tag{9}
\]

To prove this, differentiate sum q log(q/p) twice and use sum dq=sum dp=0.
At q=p the surviving quadratic terms combine into (dq-dp)^2/p.
Equation (9) is nonnegative on the diagonal. It is a Fisher metric of
the mismatch, not the Fisher metric of q alone.

Consequently, matching one probability distribution gives equality of
the first price sources at that point, but does not generally give the
same second source. If q-p=O(||theta-theta_0||^m), m>=1, the gap is
O(||theta-theta_0||^(2m)). Matching as functions on a neighborhood removes
the entire gap and all its derivatives. Every derivative of B_C and R_I
still remains.

## 4. A necessary and sufficient finite certificate

For a prescribed A and the fixed actual data in (4), the following are
equivalent:

1. Equation (1) holds for every complete history.
2. w_H=phi^(-A) q_H for every complete history.
3. q=p and -log_phi Z=A.

The first equivalence follows by exponentiation. Summation gives Z=phi^(-A),
which proves the second equivalence. Conversely q=w/Z and Z=phi^(-A)
give (1). Under these equivalent conditions,

\[
\boxed{F_{\rm actual}=B_C+A+R_I.}
\tag{10}
\]

If the data vary smoothly and (1) holds throughout a neighborhood, (10)
is equality of all full source derivatives there. It is not restricted
to a chosen wave ansatz.

This certificate cannot be replaced by declaring
d_H=A-log_phi q_H. That formula would manufacture a price for any desired
action. The d_H must already be fixed by the real compiler, and A must
be specified independently before the equality is tested.

History minimality in (7) and geometrical stationarity of (10) are
different variations. Minimization over history probabilities conditional
on theta does not imply minimization over theta. If physical selection
also minimizes over an open set of geometric directions, a stationary
point with an admitted negative second variation is not such a minimum.
The exact value identity does not erase this distinction.

## 5. Finite cycle certificate with the endpoints retained

Represent the real finite execution by a directed acyclic graph with a
source s and its recorded terminal vertices. This may be the actual finite
history graph, with the real cap and memory in its state. Include the
actual stopping outcomes and all terminal costs; no fictitious paid
padding is added.

For the linear-algebra statement, multiple terminals can be attached to
an algebraic collector t representing their already fixed boundary
functional. This does not erase or merge their protected records, identify
their CQ blocks, or introduce a physical completion gate. Its edge labels
are prescribed by that boundary functional, not optimized. For example,
once the actual terminal payoff is already included, a collector edge
has bookkeeping probability one and zero additional cost. Complete
history labels H remain distinct. Equivalently, one may work directly
with prescribed boundary potentials at the separate terminal vertices.
Every edge of the resulting test graph lies on a complete s-to-t path.

Let P_e>0 be the actual conditional probabilities, so that a complete
history has q_H=product_(e in H) P_e. Require an exact additive
representation d_H=sum_(e in H) c_e. Conditional quantum entropy in
(4) may be retained as a terminal contribution. If two histories have
different conditional quantum blocks, their separate terminal values
must remain present in this representation; the collector supplies no
license to replace them by a mixed block or to charge a new entropy.

Define

\[
\ell_e:=c_e+\log_\phi P_e.
\tag{11}
\]

Equation (1) is now sum_(e in H) ell_e=A for every complete path.
There is an exact finite linear-algebra criterion:

\[
\boxed{
\ell_e=b_{\operatorname{tail}(e)}
       -b_{\operatorname{head}(e)},\qquad b_s-b_t=A.
}
\tag{12}
\]

Necessity follows by defining b_v as the remaining sum from v to t.
Two such suffixes have the same sum: concatenate either with one fixed
s-to-v prefix and apply the assumed complete-path identity. For every
edge u->v this gives ell_e=b_u-b_v. Sufficiency follows by telescoping.

For a practical cycle test, adjoin a purely algebraic closing edge t->s
labelled -A. This is a test device, not a new physical execution or a
paid primitive. Let B be the oriented incidence matrix of the augmented
graph. Equation (12) is equivalent to the augmented edge vector lying in
im(B^T), hence to its pairing vanishing with every vector in ker(B).
A spanning tree supplies a fundamental signed cycle basis. On a connected
augmented graph the number of independent conditions is
|E_aug|-|V|+1, rather than the number of complete histories.

These are signed incidence cycles; the absence of directed cycles in a
finite execution DAG is not a certificate. If the actual finite program
has an economical exact state representation, the test can avoid
exponential path enumeration. If it needs a full history tree, no
unproved compression or polynomial-size claim is made.

The terminal condition in (12) is essential. On a bare tree, every edge
vector can be represented by vertex potentials. Arbitrarily changing the
leaf weights would therefore make the test vacuous. The actual terminal
entropy, cost and prescribed boundary functional fix the leaf data and
cannot be adjusted to make a desired A appear.

Variable stopping lengths cause no additional clock factor in (12):
the sum is over each history's actual paid events. Paths of different
lengths are compared as completed executions. The equality is not a
per-step pressure substituted for an already summed price.

## 6. Scalar factorization and finite-horizon endpoint formula

For comparison with an ordinary homogeneous transfer kernel, let W be
an irreducible nonnegative matrix on a fixed finite support, and let P
be the actual stochastic matrix on that support. Set c_e=-log_phi W_e
and s_e=-log_phi P_e. For a prescribed a(theta), the following are
equivalent:

\[
\begin{aligned}
&\sum_{e\in C}(c_e-s_e)=|C|a
   &&\text{for the signed cycle constraints},\\
&c_e-s_e-a=b_{\operatorname{tail}(e)}
                 -b_{\operatorname{head}(e)},\\
&W=\phi^{-a}D^{-1}PD,\qquad
  D=\operatorname{diag}(\phi^{b_i}).
\end{aligned}
\tag{13}
\]

For signed cycles, |C| in the first line denotes the signed pairing with
the all-ones edge vector; for a directed cycle it is its ordinary length.
Equivalently, test c-s-a directly on the incidence cycle basis. The
incidence criterion proves the second line and exponentiation proves
the third. Since rho(P)=1,

\[
-\log_\phi\rho(W)=a.
\tag{14}
\]

P may depend on theta and may have a full-rank observable probability
chart. Conjugacy to one fixed reference kernel would instead freeze its
Doob transition law and is not the same assertion.

For a real fixed finite horizon N, allow stage-dependent kernels:

\[
W_k=\phi^{-a_k}D_k^{-1}P_kD_{k+1},
\qquad k=0,\ldots,N-1.
\tag{15}
\]

With the owned initial and terminal weights u,v, exact multiplication
gives

\[
\begin{aligned}
Z_N&=u^TW_0\cdots W_{N-1}v\\
 &=\phi^{-\sum_k a_k}
   (u^TD_0^{-1})P_0\cdots P_{N-1}(D_Nv),\\
-\log_\phi Z_N
 &=\sum_k a_k-\log_\phi
 \big[(u^TD_0^{-1})P_0\cdots P_{N-1}(D_Nv)\big].
\end{aligned}
\tag{16}
\]

The last term is the actual endpoint contribution. It is not a disposable
constant unless it is field independent on the relevant domain.
In particular, suppose the actual initial law is mu, and the owned
endpoints satisfy u^TD_0^(-1)=zeta mu^T and D_N v=tau 1.
Then the normalized Gibbs path law equals the actual path law from mu
and the P_k, and

\[
F_{\rm actual}
 =B_C+\sum_k a_k-\log_\phi(\zeta\tau)+R_I.
\tag{17}
\]

The endpoint equalities must be verified on the given weights. They
are not prescriptions to alter those weights. A field-dependent zeta
or tau contributes its full source.

Equations (15)-(17) use precisely the stages already present in the
ledger. No N->infinity limit, additional normalization by N, or physical
clock rescaling is inferred. For variable-duration executions, use the
completed-path criterion (12) or retain the actual sum over durations.
A homogeneous per-step a generally produces length-dependent factors
phi^(-length*a); their sum is not automatically phi^(-N*a).

## 7. Positive-cost counterexample to dropping the endpoints or the gap

Take a source with two recorded terminal outcomes. Let the actual
probabilities be q_+=q_-=1/2 and the fixed ledger weights be

\[
w_\pm(t)=\frac{1\pm t}{4},\qquad |t|<1.
\tag{18}
\]

The corresponding costs c_pm=-log_phi w_pm are positive, and the
conditional blocks may be pure, so d_pm=c_pm. There is no baseline
source or information remainder in this example.

The bare graph is a tree: internal cycle conditions are empty. Yet

\[
\begin{aligned}
Z&=\frac12,\qquad
p_\pm=\frac{1\pm t}{2},\\
-\log_\phi Z&=\log_\phi2,\\
F_{\rm actual}
 &=\log_\phi2-\frac12\log_\phi(1-t^2),\\
D_\phi(q\Vert p)&=-\frac12\log_\phi(1-t^2).
\end{aligned}
\tag{19}
\]

Thus the gap is positive away from t=0. At t=0 its first derivative is
zero and its second derivative is 1/ln(phi), as (9) predicts. Although
the unnormalized partition sum is constant, the actual price is not.
The two leaf potentials cannot be erased by choosing new terminal
weights. For linear algebra, attach the two distinct recorded leaves to
a collector with the prescribed zero terminal labels of this example.
The resulting relative cycle constraint fails when t is nonzero. These
algebraic zero labels specify the boundary functional; they do not assert
that a physical zero-cost completion or record-erasure gate exists.

## 8. What rank 34 can and cannot supply

For a positive irreducible W(theta), let l,r be Perron left and right
vectors with l^Tr=1, let rho=rho(W), and define its Doob law and stationary
distribution by

\[
P^*_{ij}=\frac{W_{ij}r_j}{\rho r_i},
\qquad \pi_i=l_i r_i.
\tag{20}
\]

Differentiating l^TWr=rho gives the exact pressure source

\[
d[-\log_\phi\rho(W)]
 =\sum_{ij}\pi_i P^*_{ij}\,dc_{ij}.
\tag{21}
\]

This law is determined by the paid W. The actual Born history law is
not automatically P*. Their identification requires the same kind of
price/surprisal compatibility as (13), together with the finite endpoint
conditions when appropriate.

There is an unavoidable scalar ambiguity:

\[
W(\theta)\longmapsto\phi^{-\chi(\theta)}W(\theta)
\quad\Longrightarrow\quad
P^*\longmapsto P^*,\qquad
-\log_\phi\rho\longmapsto-\log_\phi\rho+\chi.
\tag{22}
\]

In the finite path formulation, d_H->d_H+chi leaves all normalized Gibbs
probabilities unchanged and adds chi to the value. Even an inverse
probability map with all derivatives known cannot recover this missing
paid scalar. Fixing it from the actual ledger is what makes (1) a
non-fitted test instead of arbitrary action engineering.

A reported local rank-34 history map can give a local observational
chart for ten metric and twenty-four link coordinates. It does not
establish that a native writer admits every corresponding physical
variation. If its coordinates are probabilities of one exhaustive
mutually exclusive experiment, at least thirty-five outcomes are
required: thirty-four normalized probabilities have Jacobian rank at
most thirty-three. Thirty-four independent conditional or nonexclusive
probes are a different interface and must not be silently treated as one
thirty-four-outcome CQ distribution.

The corresponding value/source bridge is therefore a ledger identity, not
another rank estimate: retain the owned complete CQ information and
boundaries, fix the target's normalization independently, and establish
(1), equivalently its finite graph certificate. If established on the
actual admitted field domain, it supplies the full value and source
identity (10). The present note proves that implication and its finite
test; it does not claim that the actual native compiler already passes
it, that geometry is thereby dynamically selected, or that physical
time and Book admission have been derived.

