# A4D source-image collapse: the non-tautological response terminal

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Status: exact reformulation of the task target; no new physical assumption.

## 1. Exact source image

Fix one sampled smooth background \(Q_h\), the genuine Lorentz quotient, and
the declared admissible connection class.  Define

\[
\mathscr T_h(Q_h)
=
\left\{
\tau_h\;:\;
\exists K_h,\quad
E_K(Q_h,K_h)=0,\quad
E_Q(Q_h,K_h)=h^2\tau_h
\right\}.
\tag{1}
\]

The source is an input label of the equation and must be fixed independently
of the candidate when testing a particular branch.  Definition (1) is only
the image of the exact stationary response map; it does not assign a source
after the fact in a counterexample.

Let

\[
\rho_h^{\rm sm}(g)
=
h^{-2}E_Q(Q_h,K_h^{\rm sm}(g)).
\tag{2}
\]

The #216 owner gives
\[
\rho_h^{\rm sm}(g)\to\rho[g]=-\tfrac12G[g]
\]
in its declared reconstruction/testing topology.

## 2. The response problem is exactly source-image collapse

For every exact joint/source solution in (1),

\[
\boxed{
h^{-2}\bigl[
E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\rm sm})
\bigr]
=
\tau_h-\rho_h^{\rm sm}(g).
}
\tag{3}
\]

This is an identity, not an estimate.

Consequently, for any norm/testing topology \(\mathcal T\), the positive
response-decoupling terminal on a declared admissible class is equivalent to

\[
\boxed{
\sup_{\tau_h\in\mathscr T_h(Q_h)}
\|\tau_h-\rho_h^{\rm sm}(g)\|_{\mathcal T}
\longrightarrow0,
}
\tag{4}
\]

with the supremum restricted by whatever compact-chart, source regularity, or
other hypotheses are part of that class.

Thus the scientific question is not connection uniqueness and not comparison
of two exact roots with the same source.  It is the asymptotic **diameter and
location of the realizable source image**.

Two exact roots satisfying the identical source have zero mutual response
difference tautologically.  Equation (4) instead asks whether any source
different from the designated geometric response is realizable by a
microstructured stationary connection.

## 3. M1 meaning

The canonical response memory already proves that every metric observation
factors through \(\Xi\).  Equation (1) goes one step further: after imposing
the source normalization, all raw connection representatives are forgotten
and only the image

\[
K_h\longmapsto h^{-2}\Xi(K_h)=\tau_h
\]

remains.

Therefore the correct M1 reduction is

\[
\boxed{
\text{stationary connection space}
\longrightarrow
\mathscr T_h(Q_h)
\longrightarrow
\text{continuum source class}.
}
\tag{5}
\]

A new Y/quarter/circle/coupled microscopic family creates no new proof
obligation merely by existing.  It matters only if it enlarges the source
image (1).

This is the exact sense in which the proof should remove classes rather than
enumerate representatives.

## 4. Existing owners become source-image constraints

Several results in #310 already have a simpler interpretation in (1).

* The exact flat #232/Y family has \(\Xi=0\).  It adds connection
  representatives but does not enlarge the flat vacuum source image.
* The flat #227 boost family enlarges the **connection-stationary** response
  image, but its staggered \(\Xi\) is not an independently prescribed smooth
  source and therefore does not by itself enlarge the admissible joint-source
  image.
* The full commuting Y-plane rigidity theorem collapses that entire nonlinear
  completion back to the flat source class.
* The all-amplitude temporal-B current theorem proves that, on the fixed
  nonconstant warp, no bounded smooth source lies in the source image of that
  whole candidate family on sufficiently fine meshes.
* The one-envelope nonregular isolation theorem shows that, near the exact
  designated root on the same warp, the source image of the full invariant
  sector has only the designated branch.
* The full-field stationary action identity gives the necessary scalar source
  condition
  \[
  h^4\sum_xQ_h(x):\tau_h(x)
  =\frac{\pi^2}{1250}+O(h)
  \]
  for every full-four-dimensional log-O(h) exact root on that warp.  In
  particular the preset vacuum source is outside the full source image there.

These are restrictions on one image, not separate solution classes requiring
separate terminals.

## 5. Compose with the finite quartic correlation memory

Use relative Lorentz matrices
\[
(K_h^*)^{-1}K_h=I+U_h.
\]

The finite-current/correlation owner proves that \(E_K\) and \(\Xi\) are
exact degree-at-most-four finite-stencil polynomials in \(U_h\).
Therefore the realizable source image (1), in every bounded local chart, is
the projection of one finite-degree shared-link correlation system:

\[
\mathcal P_{\le4}(S_h,K_h^*;\mathfrak C_h)=0,
\qquad
\tau_h=\mathcal D_{\le4}(\mathfrak C_h).
\tag{6}
\]

The number of microscopic representatives may grow without bound, but the
types of correlation data and polynomial equations in (6) do not.

For the quadratic continuum limit, the response projection factors further
through the 21 certified matrix shift moments.  Thus frequency itself is not
part of the minimal readout memory.

The terminal (4) may therefore be attacked directly as a statement about the
image of (6).  No all-Bloch rank classification is logically required.

## 6. Positive and negative certificates in the new language

A positive certificate need not construct or classify every \(K_h\).  It is
enough to prove an image bound

\[
\mathcal P_{\le4}=0
\quad\Longrightarrow\quad
\|\mathcal D_{\le4}(\mathfrak C_h)-\rho_h^{\rm sm}\|_{\mathcal T}
\le\varepsilon_h,\qquad
\varepsilon_h\to0.
\tag{7}
\]

This can be a polynomial-ideal identity, real-radical certificate, finite
moment/PSD dual inequality, compensated-compactness identity, or another
uniform algebraic estimate.

A negative terminal requires a point in the realizable image separated from
the designated response:

\[
\tau_h\in\mathscr T_h(Q_h),\qquad
\liminf
\|\tau_h-\rho_h^{\rm sm}\|_{\mathcal T}>0,
\tag{8}
\]

with the source family declared independently before solving the links.

Equation (8) is precisely the original task's hostile sequence criterion.

## 7. Consequence for proof architecture

From this point, a proposed computation should answer one question:

> Does it shrink, characterize, or separate the source image
> \(\mathscr T_h(Q_h)\)?

If not, it is not on the shortest closure path.

In particular:

* another Bloch zero is not itself a blocker;
* another exact joint vacuum with the same \(\Xi\) is not a blocker;
* connection uniqueness is unnecessary;
* a source-incompatible connection-stationary branch is not a counterexample.

The remaining target is one image-collapse theorem, not an unlimited catalogue
of microscopic solution types.

Verdict:

\[
\boxed{\texttt{JOINT-RESPONSE-DECOUPLING-EQUIVALENT-TO-SOURCE-IMAGE-COLLAPSE}}
\]

The task remains open because (7) has not yet been proved in the full declared
topology, but its quantifiers no longer range over separately classified
microstructure families.
