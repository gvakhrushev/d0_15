# SYNTHESIS A4D — affine action-completion checkpoint

**Purpose:** durable checkpoint for the current nonlinear affine-action frontier.  
**Scope:** consolidate the exact results from PR #184, PR #185, PR #188 and the
follow-up CONTROL rank-pressure that otherwise existed only in PR comments.

This file is a checkpoint, not a new claim owner.  The detailed proofs and
exact certificates remain in the individual research memos.

---

## 1. Canonical star sector already fixed

The accepted oriented Role-bivector insertion is the star channel, unique up to
overall scale in the owned spatial-Role-natural class.

The corresponding finite star density has:

\[
d_A=1,\qquad d_E=1,
\]

and survives the nonlinear local proper-Lorentz quotient on the all-site
nondegenerate solder sector:

\[
d_{P,\mathrm{Lor},\mathrm{nd}}=1.
\]

The full affine translation subgroup is not a symmetry of the original star
density.

---

## 2. First on-shell translation rescue class is closed

The first Cartan/Hodge deformation class of the flat translation tangent was
classified and killed.

The six correction channels are:

- two solder-nonparallelism contractions;
- four curvature-driven connection contractions.

Exact L=2 controls give

\[
\operatorname{rank}A=6,
\qquad
\operatorname{rank}[A|-c]=7.
\]

Hence no nontrivial on-shell/Noether affine translation symmetry exists in that
class.

Terminal:

\[
\texttt{STAR-TRANSLATION-ONSHELL-SYMMETRY-NOGO-IN-FIRST-CARTAN-HODGE-CLASS}.
\]

Therefore an action completion is required in this class.

---

## 3. Relative solder is the unique affine-covariant completion in its family

For the observer-completed affine solder law, define

\[
\widehat\Theta^{(\lambda)}
=
\Theta-\lambda\,b^{T}h_n.
\]

Its exact transformation is

\[
\widehat\Theta'^{(\lambda)}
=
\widehat\Theta^{(\lambda)}g^{-1}
+
(1-\lambda)\tau^Th_{n'}.
\]

Thus full affine covariance uniquely forces

\[
\boxed{\lambda=1}.
\]

The selected relative solder is

\[
\boxed{
\widehat\Theta
=
\Theta-b^Th_n.
}
\]

The canonical star density built from \(\widehat\Theta\) is exactly invariant
under mixed site-dependent Lorentz + node-translation gauges.

Exact L=2 control verifies all 96 site/face cells individually.

The curved selector witness gives

\[
S_{\rm after}(\lambda)-S_{\rm before}
=
\frac23(\lambda-1),
\]

so there is no second \(\lambda\)-solution.

At \(b=0\) this reduces literally to the accepted star density.

---

## 4. Relative solder alone overquotients the common-edge sector

The relative action depends on \((\Theta,b)\) only through

\[
\Theta-b^\flat_n.
\]

Hence every matched edge shift

\[
(\Theta,b)
\mapsto
(\Theta+u^\flat,b+u)
\]

leaves the relative solder and action unchanged.

On the exact curved L=2 witness,

\[
\dim C^1_+(X,V)=256,
\]

while the node-translation coboundary

\[
(D_Lc)_{x,r}=c_x-L_{x,r}c_{x+r}
\]

has

\[
\operatorname{rank}D_L=64.
\]

Therefore the intended gauge image is only 64-dimensional, while the relative
action is blind to the full 256-dimensional matched-edge diagonal.

The excess accidental nullity is

\[
\boxed{256-64=192}.
\]

An explicit one-edge \(u\) satisfies

\[
\operatorname{rank}[D_L|u]=65,
\]

so it is not node gauge while the relative action remains unchanged.

Terminal:

\[
\texttt{AFFINE-RELATIVE-SOLDER-COMPLETION-OVERQUOTIENTS-EDGE-DIAGONAL}.
\]

---

## 5. Single-plaquette translational scalar no-go

For one based affine holonomy

\[
H=(P,t),
\]

pure node translations act by

\[
t\mapsto t+(I-P)c.
\]

On the open dense stratum

\[
\det(I-P)\ne0,
\]

this action is transitive on the whole translation vector space.

Therefore every continuous full-affine scalar depending on a single based
holonomy is translation-blind on the generic stratum, and continuity extends
that blindness across rank-deficient strata.

The owned open torsion obeys

\[
T'_{\rm open}=gT_{\rm open}-F'c_{\rm far},
\]

so when \(F\) is invertible it has the same generic transitivity obstruction.

Hence a naive one-plaquette \(T^2\) completion is not full-affine invariant.

Terminal:

\[
\boxed{
\texttt{SINGLE-PLAQUETTE-AFFINE-TRANSLATION-SCALAR-NOGO-IN-CONTINUOUS-CLASS}
}.
\]

---

## 6. Two based holonomies are the first continuous translational carrier

For two based affine holonomies

\[
H_i=(P_i,t_i),
\]

define

\[
M_i=I-P_i,
\qquad
d_1=\det M_1,
\]

\[
q_1^\#
=
\operatorname{adj}(M_1)t_1,
\]

and

\[
\boxed{
R_{2|1}
=
d_1t_2-M_2q_1^\#.
}
\]

Then exactly

\[
\boxed{
R'_{2|1}=gR_{2|1}.
}
\]

This is polynomial, inverse-free and defined on singular strata.

Therefore

\[
R_{2|1}^T\eta R_{2|1}
\]

and

\[
R_{2|1}^Th_nR_{2|1}
\]

are full-affine scalars.

On the exact nongauge one-edge witness from the relative-solder frontier,

\[
R_{AB|AC}
=
\begin{pmatrix}
-32/9\\
-40/9\\
8/3\\
0
\end{pmatrix},
\]

with

\[
R^T\eta R=-128/9.
\]

Thus two loops detect an exact nongauge edge mode missed by the relative-solder
term.

Constructive survivor:

\[
\boxed{
\texttt{JOINT-TWO-HOLONOMY-TRANSLATION-RESIDUAL-SURVIVES}
}.
\]

---

## 7. Full joint-residual rank pressure

The full ordered elementary-face-pair residual family was then tested as one
linear operator on the complete edge-shift space.

### Generic curved rational backgrounds

On five independent deterministic rational Lorentz-link backgrounds:

\[
\boxed{
\operatorname{rank}R_{\rm joint}=192.
}
\]

Because

\[
R_{\rm joint}D_L=0
\]

exactly and

\[
\operatorname{rank}D_L=64,
\]

the rank cannot exceed

\[
256-64=192.
\]

Thus the generic joint residual family separates the entire nongauge quotient:

\[
\boxed{
\ker R_{\rm joint}
=
\operatorname{im}D_L
}
\]

on these generic backgrounds.

Sitewise, each site contributes exact rank

\[
20=24-4,
\]

i.e. six plaquette translations times four vector components minus one common
four-vector base translation.

### Sparse curved witness

On the earlier sparse curved control,

\[
\operatorname{rank}R_{\rm joint}=20.
\]

Thus the coordinate rank is strongly background-stratified.

### Exact flat linear connection

At

\[
L=I,
\]

the polynomial joint residual collapses:

\[
\operatorname{rank}R_{\rm joint}=0.
\]

So it is a generic chart, not a uniform carrier across the flat rank seam.

---

## 8. Exact flat quotient is nevertheless complete by path data

At exact flat \(L=I\),

\[
\operatorname{rank}D_{\rm flat}=60,
\]

so

\[
\dim\left(C^1_+/\operatorname{im}D_{\rm flat}\right)
=
256-60
=
196.
\]

The exact flat path invariants give:

\[
\operatorname{rank}(\text{plaquette translation curl})
=
180,
\]

\[
\operatorname{rank}(\text{four fundamental Role cycles})
=
16,
\]

and jointly

\[
\boxed{
\operatorname{rank}(\text{curl}\oplus\text{cycles})
=
196.
}
\]

Hence their kernel has dimension

\[
256-196=60,
\]

exactly the flat node-gauge image.

So the flat quotient is not missing information.

It is simply described by a different chart from the generic two-loop residual
chart.

---

## 9. Rank-stratified affine-holonomy quotient

For fixed \(L\), the fundamental invariant carrier is

\[
\boxed{
Q_L
=
C^1_+(X,V)/\operatorname{im}D_L.
}
\]

A spanning-tree gauge argument identifies this with translation data of
fundamental based loops modulo one common base translation:

\[
Q_L
\cong
\{(t_\gamma)_\gamma\}/
\{((I-P_\gamma)c)_\gamma\}.
\]

This quotient is valid without a rank hypothesis.

The generic two-loop residuals are coordinates on the regular 192-dimensional
stratum.

The exact flat plaquette+cycle variables are coordinates on the
196-dimensional flat stratum.

Thus the correct object is rank-stratified; no single fixed polynomial
coordinate formula covers all strata faithfully.

---

## 10. Non-closed affine gauge relation at the flat seam

The affine gauge-orbit relation is not closed when \(L\to I\).

For a one-edge vector \(u\), choose a non-null \(v\) with

\[
\eta(v,u)=0
\]

and a Lorentz generator \(A\in\mathfrak{so}(1,3)\) satisfying

\[
Av=-u.
\]

Let

\[
L_e(\varepsilon)
=
\left(I+\frac{\varepsilon A}{2}\right)
\left(I-\frac{\varepsilon A}{2}\right)^{-1}
\to I,
\]

and use the large node translation

\[
c_x=\frac{v}{\varepsilon}.
\]

Then on that edge

\[
(I-L_e(\varepsilon))\frac{v}{\varepsilon}
\to u,
\]

while the other edge shifts can be kept zero.

Therefore a sequence of gauge-equivalent nearby configurations can converge to
two distinct pointwise flat configurations differing by a matched edge shift
that is not an actual flat node-gauge image.

Consequently every continuous full-affine scalar must identify those endpoint
limits.

This gives the exact trilemma:

1. full affine node-gauge invariance;
2. continuity across the linear-holonomy rank transition;
3. sensitivity to every intrinsic flat nongauge matched-edge direction.

Without extra resolution data, all three cannot be imposed simultaneously.

---

## 11. Existing PR #135 resolution memory is not enough for this seam

PR #135 owns

\[
\Xi_{\rm str}
=
((W_y)_y,\mathcal K).
\]

Its local part \(W_y\) stores lost active directions in the relative A/e
synthesis kernel.

Its global part \(\mathcal K\) stores limiting common-fixed node directions.

The affine quotient seam instead depends on the **image** of \(D_L\).

Two rational Lorentz Cayley histories were constructed with:

\[
L_t^A\to I,
\qquad
L_t^B\to I,
\]

and

\[
b_t=e_t=0
\]

along both.

Thus both histories have

\[
\boxed{
\Xi_{\rm str}^A
=
\Xi_{\rm str}^B
=
((0)_y,0).
}
\]

Nevertheless their limiting gauge-image spaces differ.

Exactly,

\[
\operatorname{rank}D_0=60,
\]

\[
\operatorname{rank}\mathcal I_A
=
\operatorname{rank}\mathcal I_B
=
64,
\]

and

\[
\boxed{
\operatorname{rank}(\mathcal I_A+\mathcal I_B)=65.
}
\]

Hence

\[
\mathcal I_A\ne\mathcal I_B.
\]

So PR #135 kernel memory cannot reconstruct the affine gauge-image seam.

---

## 12. New affine gauge-image resolution memory

For a fixed endpoint map \(D_L\), define

\[
\boxed{
\operatorname{ResIm}(D_L)
=
\{
\mathcal I\le C^1_+(X,V):
\operatorname{im}D_L\subseteq\mathcal I
\}.
}
\]

For a convergent fixed-rank approach,

\[
\boxed{
\mathcal I_*
=
\lim\operatorname{im}D_{L_t}.
}
\]

The equivalent compressed datum is

\[
\boxed{
G_*
=
\mathcal I_*/\operatorname{im}D_L
\le
Q_L.
}
\]

This is the minimum new structural memory for the affine quotient seam.

Terminal:

\[
\boxed{
\texttt{AFFINE-GAUGE-IMAGE-RESOLUTION-CONSTRUCTED}
}.
\]

Negative subterminal:

\[
\boxed{
\texttt{PR135-KERNEL-MEMORY-INSUFFICIENT-FOR-GAUGE-IMAGE-SEAM}
}.
\]

---

## 13. Exact positive resolved affine-shift action term

The owned observer form gives a positive edge metric

\[
\langle u,v\rangle_{h_n,1}
=
\sum_{x,r}
h_{n_x}(u_{x,r},v_{x,r}).
\]

For supplied image-incidence memory \(\mathcal I\), define

\[
\boxed{
E_{\mathcal I}(b;n)
=
\operatorname{dist}_{h_n,1}(b,\mathcal I)^2.
}
\]

Equivalently,

\[
E_{\mathcal I}(b;n)
=
\|P_{\mathcal I^{\perp_{h_n,1}}}b\|^2.
\]

Under a full affine node gauge,

\[
L'=gLg^{-1},
\qquad
b'=G_1b+D_{L'}c,
\qquad
n'=gn,
\]

and the memory transports as

\[
\mathcal I'=G_1\mathcal I.
\]

Because

\[
D_{L'}c\in\operatorname{im}D_{L'}\subseteq\mathcal I'
\]

and \(G_1\) is an observer isometry,

\[
\boxed{
E_{\mathcal I'}(b';n')
=
E_{\mathcal I}(b;n).
}
\]

Thus \(E_{\mathcal I}\) is an exact positive full-affine action building block.

Its zero locus is exactly

\[
E_{\mathcal I}(b)=0
\iff
b\in\mathcal I.
\]

Therefore the universal quadratic readout determines \(\mathcal I\); the
incidence memory is structurally minimal for this readout.

---

## 14. Intrinsic versus resolved flat lifts

At exact flat \(L=I\):

### Intrinsic lift

\[
\mathcal I_{\rm int}
=
\operatorname{im}D_0,
\]

so

\[
\dim Q_{\rm int}=196.
\]

### Generic-limit resolved lift

For a rank-64 curved approach,

\[
\dim\mathcal I_*=64,
\]

so

\[
\dim Q_{\mathcal I_*}=192.
\]

Thus the same pointwise flat background has different resolved lifts depending
on approach memory.

This is the correct resolution of the non-closed gauge relation.

It must not be collapsed into one pointwise quotient without stating which
continuity contract is intended.

---

## 15. Current candidate action carrier

The canonical affine-covariant curvature term is the relative-solder star term

\[
S_{\widehat\star}.
\]

The new independent translation-sensitive resolved term is

\[
E_{\mathcal I}.
\]

Therefore the first exact full-affine two-channel trial family is

\[
\boxed{
S_{\rm trial}
=
\alpha S_{\widehat\star}
+
\beta E_{\mathcal I}.
}
\]

At the current stage:

\[
d_A\le2
\]

for this selected two-channel class before any normalization.

No theorem yet selects \(\beta/\alpha\).

No theorem yet proves whether the two action directions remain independent after
variation or physical quotient.

So do **not** promote this to \(d_E=2\) or \(d_P=2\).

---

## 16. Next exact blocker

The next task is not another covariance search.

It is the **variational status of the image-incidence memory**.

There are three distinct contracts:

1. **frozen-memory variation** — \(\mathcal I\) is supplied and not varied;
2. **constrained Grassmannian variation** — \(\mathcal I\) varies subject to
   \[
   \operatorname{im}D_L\subseteq\mathcal I;
   \]
3. **history-germ variation** — \(\mathcal I\) is reconstructed from a resolved
   approach and the history itself is varied.

These contracts need not have the same Euler family or physical quotient.

The next pressure must classify them before any coefficient selector or final
\(d_P\) statement.

---

## 17. Active PRs / durable owners at checkpoint

### PR #184

\`EXP-A4D-AFFINE-RELATIVE-SOLDER-ACTION-COMPLETION\`

Terminal:

\[
\texttt{AFFINE-RELATIVE-SOLDER-COMPLETION-OVERQUOTIENTS-EDGE-DIAGONAL}.
\]

Primary memo:

\`MEMO_A4D_AFFINE_RELATIVE_SOLDER_ACTION_COMPLETION.md\`.

### PR #185

\`EXP-A4D-AFFINE-TRANSLATION-CURVATURE-ACTION-COMPLETION\`

Terminals:

\[
\texttt{SINGLE-PLAQUETTE-AFFINE-TRANSLATION-SCALAR-NOGO-IN-CONTINUOUS-CLASS},
\]

\[
\texttt{JOINT-TWO-HOLONOMY-TRANSLATION-RESIDUAL-SURVIVES}.
\]

Primary memo:

\`MEMO_A4D_AFFINE_TRANSLATION_CURVATURE_ACTION_COMPLETION.md\`.

### PR #188

\`EXP-A4D-AFFINE-GAUGE-IMAGE-RESOLUTION-MEMORY\`

Terminals:

\[
\texttt{AFFINE-GAUGE-IMAGE-RESOLUTION-CONSTRUCTED},
\]

\[
\texttt{PR135-KERNEL-MEMORY-INSUFFICIENT-FOR-GAUGE-IMAGE-SEAM}.
\]

Primary memo:

\`MEMO_A4D_AFFINE_GAUGE_IMAGE_RESOLUTION_MEMORY.md\`.

---

## 18. Restart point

If the research session is interrupted, restart from this exact question:

> For
> \[
> S_{\rm trial}
> =
> \alpha S_{\widehat\star}
> +
> \beta E_{\mathcal I},
> \]
> classify the three variational contracts for \(\mathcal I\), compute
> \(d_E\), then quotient the genuine full-affine gauge verticals and determine
> whether \(\alpha,\beta\) remain independent at \(d_P\).

Do not reopen:

- the star/identity insertion selector;
- nonlinear local-Lorentz gauge invariance;
- the first Cartan-Hodge translation-symmetry class;
- the single-loop \(T^2\) route;
- the need for image-incidence memory at the rank seam.
