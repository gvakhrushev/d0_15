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


## 8. Two exact source-image collapses already owned

### 8.1 Small real four-phase flat chart

The full nonlinear owner
\`A4D_IDENTITY_QUARTER_NONLINEAR_RESPONSE.md\` does not merely classify the
linear center.  In the complete 96-real-dimensional four-phase link chart it
sets

\[
F(l)=\bigl(E_K(\eta,e^l),\Pi_{\ne0}E_Q(\eta,e^l)\bigr)
\]

and proves that every sufficiently small zero of \(F\) lies on one of eight
explicit exact axis families.  Every one of those families has the **full**
metric Euler equal to zero.  Therefore, with a phase-common prescribed source,

\[
\boxed{
\mathscr T_h^{\rm fourphase,small}(\eta)=\{0\}.
}
\tag{19}
\]

This is a nonlinear source-image theorem.  It includes all mixed quarter-center
directions in that local chart; it is not a statement that the connection is
unique.

The same owner proves the quantitative readout gain

\[
\|\overline E_Q(l)\|
\le C\|l\|_\infty
\bigl(\|E_K(l)\|+\|\Pi_{\ne0}E_Q(l)\|\bigr),
\tag{20}
\]

with an \(L\)-independent repeated-cell version in every componentwise
\(\ell^p\), including the unweighted \(p=1\) sum.  Thus the singleton image is
stable under the exact residual topology used by that restricted sector.

### 8.2 Moving simple-plane current class

The moving-current owner
\`A4D_MOVING_SIMPLE_PLANE_CURRENT_RIGIDITY.md\` treats two neighboring
simple-plane layers before a Bloch decomposition.  It proves

\[
E_Q\equiv0
\]

throughout the class, while the shared spatial-link Euler equations force
conservation of the complete spatial difference-plane Gram and of the Cayley
amplitude magnitude.  The only opposite-sign transition is the corresponding
internal Lorentz rotation of the spatial triad.

Hence this class contributes no new source value:

\[
\boxed{
\mathscr T_h^{\rm simple\text{-}plane,current}
\subseteq\{0\},
}
\tag{21}
\]

and exact stationarity prevents the response-null packet from carrying a
genuinely changing spatial Gram.  In the one-coordinate continuum reduction,
after frame alignment, the surviving metric has constant spatial metric and
only time-dependent lapse/shift, hence is flat.

Equations (19)--(21) are examples of the intended proof architecture:
collapse whole realizability images instead of cataloguing their microscopic
representatives.

### 8.3 Full-link commuting B, including spatial compensation

[The full-link current owner](A4D_COMMUTING_B_FULL_LINK_CURRENT_RIGIDITY.md)
now allows arbitrary full-four-dimensional links in `exp(R B)` on all four
roles. On eta, unrestricted connection stationarity makes `Xi=z*m` and
conserves `|z|` over the entire torus, while allowing an invisible spatial
current. Independent uniformly C5 sampled sources then imply

\[
h^{-2}\|\Xi\|_{\mathrm{owner},1}\le3M_5h\longrightarrow0.
\]

This is the original unweighted topology; for a fixed C-infinity source the
bound is super-algebraic. The microscopic links and signs are not classified.

On the fixed warped background, arbitrary spatial B holonomies leave the
three diagonal source-to-flux relations unchanged. The exact common current
therefore excludes the whole bounded-source image on fine meshes, with the
same raw Euler lower bound `(102/625)L^3-90 M^2`. Noncommuting spatial links
add the explicit adjoint-transport torque of that owner; its control is
still required for the unrestricted source image.

## 9. Audit of the proposed harmonic-plus-sign terminal

The instruction to use one object rather than another family census is
retained. The proposed `(J_harm,sigma)` first needs a precise definition,
a sufficient readout map and a valid terminal implication. This audit uses
only the mandatory #232 and #227 controls already owned by the task.

### 9.1 Same-source response separation is impossible here

Fix the same sampled Q_h and the same independently prescribed tau_h. Two
exact joint/source roots obey

\[
\Xi(K_1)=h^2\tau_h=\Xi(K_2),\qquad\Xi(K_1)-\Xi(K_2)=0.
\tag{22}
\]

Thus a pair with one tau and different Xi cannot satisfy the exact equations.
Nonuniqueness of a finer current memory at fixed tau does not establish
`A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.
The valid negative terminal is a predeclared source and an exact admissible
sequence separated from the designated response:

\[
E_K(Q_h,K_h)=0,\quad\Xi(K_h)=h^2\tau_h,\quad
\liminf h^{-2}\|h^2\tau_h-\Xi(K_h^{\rm sm})\|_{\mathrm{owner},1}>0.
\tag{23}
\]

The comparator need not solve the same metric-source equation. If it does,
(23) is zero by substitution, as required by the task brief.

### 9.2 Literal harmonic momentum is not determined by the source

Use the right face momentum of the finite-current owner,

\[
\Pi_{rs}(x)[X]=\frac12\langle W_{rs}(S_x),P_{rs}X+XP_{rs}^{-1}\rangle.
\tag{24}
\]

At S=I its ordinary periodic harmonic projection is the 36-component
constant two-cochain `bar Pi_rs=mean_x Pi_rs(x)`. This is the natural
ordinary-Hodge interpretation of the proposed current. For other local
Lorentz frames at the same Q=eta, pull each covector back by its solder:
evaluate it on `S_x X S_x^-1`. This gives the same components in the S=I
representative and retains the genuine Lorentz quotient.

The mandatory #232/Y joint vacuum has

\[
Y=J_{12}-J_{13}+J_{23},\quad Y^3=-3Y,\quad
U_Y(t)=I+\frac{4tY+2t^2Y^2}{4+3t^2},
\]

with Role0 links `(U_Y(t),I,U_Y(t)^-1,I)` in the repeated four-phase cell
and identity spatial links. Its **complete** Euler numerator is identically
zero: `E_K=0`, `Xi=0`. The source tau=0 is fixed before choosing t. The
designated I root has the same source and response. The Y field has
nonzero curvature `4tY/(4+3t^2)` for t!=0 and is nongauge.

The exact harmonic difference has temporal-face/boost block

\[
\boxed{\overline\Pi(Y_t)-\overline\Pi(I)
=\frac{t^2}{4+3t^2}
\begin{pmatrix}-2&1&1\\1&-2&1\\1&1&-2\end{pmatrix},}
\tag{25}
\]

where rows are faces 01,02,03 and columns K1,K2,K3; all other entries are
zero. This is a coefficientwise identity from (24). For t=ah, a>0,

\[
h^{-2}(\overline\Pi(Y_{ah})-\overline\Pi(I))_{01,K1}
\longrightarrow-\frac{a^2}{2},\qquad\Delta\Xi=0.
\tag{26}
\]

Thus the log-O(h) admissible joint vacuum has continuously variable harmonic
current memory at one smooth source and one designated sheet. A sign label
cannot make that varying component a function of the fixed source. This is
response-invisible current memory. It falsifies the proposed implication
from undetermined current memory to a response NO-GO.

### 9.3 The canonical stationary current is transported

On the same Y vacuum the ordinary codifferential of (24) is nonzero. One
literal row at phase zero is

\[
(D^*\Pi)_{\mathrm{Role1},K2}=-\frac{4t}{4+3t^2},\qquad E_K=0.
\tag{27}
\]

The exact current formula retains every tail adjoint transport. With
`T_r v(x)=Ad_(L_xr) v(x+e_r)`, direct multiplication gives

\[
[T_r-I,T_s-I]=(\operatorname{Ad}_{P_{rs}}-I)T_sT_r.
\tag{28}
\]

This commutator is nonzero on the curved Y control. A flat cochain complex
and its fixed harmonic dimension therefore cannot be assumed for the
transported operator. A different J or transported harmonic quotient needs
an explicit construction and its readout proof. Equations (25)--(27)
concern the canonical momentum's ordinary Hodge projection; they do not
reject every possible finite sufficient invariant.

The mandatory #227 control also tests one amplitude sign on the full E_K
fiber. A phase translate changes response signs from `(+,+,-,-)` to
`(+,-,-,+)` while preserving the entire harmonic momentum and the positive
amplitude, including the origin response sign. Xi changes sitewise.
These fields need different fast sources; they are not two roots of one
smooth joint/source problem. A sitewise sign field has a number of entries
growing with L, rather than one global bit.

### 9.4 Divergence cancellation does not bound the owner norm

A divergence telescopes in signed summation. The period-four flux
`(1,0,-1,0)` has divergence `(1,-1,-1,1)`, zero signed mean and unweighted
l1 norm four. Repeated at amplitude h^2 on `(Z/LZ)^4`, its normalized raw
norm is L^4. This is an algebraic norm control, not an asserted joint field.
Deleting curls/divergences requires an estimate in the actual owner norm;
weak smooth-test cancellation does not prove the required raw `o(h^2)`.

### 9.5 The single terminal object

The response-sufficient object remains the realizable source image (1),
with the exact degree-four shared-link constraint system as its algebraic
presentation. A current invariant V must provide a map `Xi=R(V)`; V itself
may vary at fixed Xi, as (25) proves. Positive closure needs the uniform
image bound (4) in the unweighted norm; negative closure needs (23).

Finite stencil and degree mean a fixed list of local equation types. They
do not prove that one fixed global vector parameterizes every refinement:
physical sites, overlap constraints and sitewise sign entries grow with L.
A refinement-uniform dual identity/inequality for the source image remains
required. Subsequent family certificates do not replace that obligation
or count as the terminal.

The [quadratic bracket-memory owner](A4D_QUADRATIC_BRACKET_MEMORY.md),
at `a60378f7c8d7f08435838ddb67a3c3b093fafb8d`, provides an exact 36-component
local projection for the leading odd-curvature interaction. It is consumed
as a coefficient input to this same image problem. Its quadratic order
alone does not control the cubic/quartic physical sums in the raw norm.

The audit checks the complete degree-eight Y Euler numerator, every
coefficient of (25), the existing B phase controls, the transport
commutator and the exact norm control:

```sh
python3 02_REGISTRY/research/certificates/a4d_harmonic_sign_candidate_audit_check.py
```

Verdict: `CANONICAL-HARMONIC-SIGN-TERMINAL-DICHOTOMY-INVALID`.
This closes the audit of that proposed criterion. The parent response
theorem remains `PARTIAL / OPEN`; no new family or task-level NO-GO is added.
