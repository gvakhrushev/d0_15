# MEMO A4D — affine gauge-image resolution memory

**Task:** \`EXP-A4D-AFFINE-GAUGE-IMAGE-RESOLUTION-MEMORY\`  
**Execution:** PR #188  
**Status:** terminal EXPENSIVE research classification  
**Baseline:** \`297067714e7c1a246b06ed981578105c58d9f3db\`

## 0. Verdict

The affine translation quotient has its own rank-transition memory.

It is **not** determined by the already-landed PR #135 resolution memory

\[
\Xi_{\rm str}
=
((W_y)_y,\mathcal K).
\]

The correct instantaneous gauge map is

\[
\boxed{
D_L:C^0(X,V)\longrightarrow C^1_+(X,V),
\qquad
(D_Lc)_{x,r}
=
c_x-L_{x,r}c_{x+r}.
}
\tag{0.1}
\]

The affine-shift orbit quotient at fixed linear connection is

\[
\boxed{
Q_L
=
C^1_+(X,V)/\operatorname{im}D_L.
}
\tag{0.2}
\]

When \(\operatorname{rank}D_L\) changes, continuity of the physical quotient
cannot be encoded by the endpoint map \(D_{L_0}\) alone.

For a convergent fixed-rank approach \(L_t\to L_0\), the missing datum is the
Grassmannian limit

\[
\boxed{
\mathcal I_*
=
\lim_{t\to0}\operatorname{im}D_{L_t}
\subset C^1_+(X,V),
}
\tag{0.3}
\]

whenever that limit exists.

It necessarily satisfies

\[
\boxed{
\operatorname{im}D_{L_0}
\subseteq
\mathcal I_*.
}
\tag{0.4}
\]

Equivalently, the genuinely new memory is the lost quotient subspace

\[
\boxed{
G_*
=
\mathcal I_*/\operatorname{im}D_{L_0}
\le
Q_{L_0}.
}
\tag{0.5}
\]

The terminal positive construction is therefore

\[
\boxed{
\texttt{AFFINE-GAUGE-IMAGE-RESOLUTION-CONSTRUCTED}.
}
\]

There is also a strict negative subterminal:

\[
\boxed{
\texttt{PR135-KERNEL-MEMORY-INSUFFICIENT-FOR-GAUGE-IMAGE-SEAM}.
}
\]

An exact \(L=2\) witness gives two rational proper-Lorentz Cayley histories
approaching the **same**

\[
L_0=I,\qquad b_0=e_0=0,
\]

with the same PR #135 structural memory

\[
((W_y)_y,\mathcal K)=((0)_y,0),
\]

but with distinct limiting gauge-image spaces

\[
\mathcal I_A\ne\mathcal I_B.
\]

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

while

\[
\boxed{
\dim(\mathcal I_A+\mathcal I_B)=65.
}
\tag{0.6}
\]

Thus the old memory records which node-kernel directions survive, but not
where the lost gauge-image directions land in the edge quotient.

The new resolution is not merely a classification object.  The already-owned
observer form gives an exact positive full-affine invariant on a supplied
image-incidence branch:

\[
\boxed{
E_{\mathcal I}(b;n)
=
\inf_{u\in\mathcal I}
\|b-u\|_{h_n,1}^2
=
\|P_{\mathcal I^{\perp_{h_n,1}}}b\|_{h_n,1}^2.
}
\tag{0.7}
\]

It is invariant under the complete affine node gauge and continuous on every
resolved fixed-rank Grassmannian chart.

For the intrinsic choice

\[
\mathcal I=\operatorname{im}D_L,
\]

it is the positive quotient norm on \(Q_L\).

At the exact flat \(L=2\) point,

\[
\dim Q_{I}=256-60=196.
\]

Along either generic Cayley branch,

\[
\dim Q_{\mathcal I_*}=256-64=192.
\]

Therefore the same pointwise flat background has several legitimate resolved
lifts.  The intrinsic flat lift keeps 196 affine-shift quotient directions;
a generic curved-limit lift keeps 192.  This is not a contradiction.  It is
the exact finite content of the non-closed gauge-orbit seam.

The next blocker is variational, not kinematic:

> should \(\mathcal I\) be frozen approach memory, a constrained dynamical
> Grassmannian variable, or the endpoint of a varied background germ?

Until that is classified, one must not claim a final \(d_E\) or \(d_P\) for
the completed action.

Exact certificate:

\`02_REGISTRY/research/certificates/a4d_affine_gauge_image_resolution_memory_check.py\`.

---

## 1. Fixed-\(L\) affine translation quotient

Let

\[
X=(\mathbb Z/L\mathbb Z)^{\mathrm{Role}}
\]

be the finite periodic site set and let \(E_+\) be the positive Role edges.

Write

\[
\mathcal N
=
C^0(X,V)
=
\bigoplus_{x\in X}V_x,
\]

\[
\mathcal E
=
C^1_+(X,V)
=
\bigoplus_{(x,r)\in E_+}V_x.
\]

The linear link on the positive edge

\[
x\xleftarrow{\ r\ }x+r
\]

is

\[
L_{x,r}:V_{x+r}\to V_x.
\]

The node-translation coboundary is (0.1):

\[
(D_Lc)_{x,r}
=
c_x-L_{x,r}c_{x+r}.
\]

For a pure affine node translation \(c\),

\[
b\longmapsto b+D_Lc.
\tag{1.1}
\]

Hence the exact orbit space of the affine shifts at fixed \(L\) is (0.2).

No solder identification is used here.

This quotient exists before any action is selected.

---

## 2. Kernel = common fixed holonomy

Assume the underlying positive-edge graph is connected.

If

\[
D_Lc=0,
\]

then every edge obeys

\[
c_x=L_{x,r}c_{x+r}.
\]

Choose a basepoint \(o\).  All node values are obtained by transporting one
vector \(c_o\).

Consistency around every based loop \(\gamma:o\to o\) requires

\[
P_\gamma c_o=c_o.
\]

Therefore

\[
\boxed{
\ker D_L
\cong
\mathcal H_o(L)
:=
\bigcap_{\gamma:o\to o}
\operatorname{Fix}P_\gamma.
}
\tag{2.1}
\]

Consequently

\[
\boxed{
\operatorname{rank}D_L
=
4|X|-\dim\mathcal H_o(L).
}
\tag{2.2}
\]

This identifies exactly what the **global** part of PR #135 memory sees:
it remembers limiting subspaces of the common-fixed node kernel.

It does not yet say where directions that leave that kernel map in
\(\mathcal E\).

That is the new seam.

---

## 3. Flat and generic \(L=2\) ranks

For the period-two Role torus,

\[
|X|=16,
\]

\[
\dim\mathcal N=64,
\]

\[
\dim\mathcal E=16\cdot4\cdot4=256.
\]

At

\[
L=I,
\]

the kernel of \(D_0\) is the four-dimensional space of constant node vectors.

Hence

\[
\boxed{
\operatorname{rank}D_0=64-4=60.
}
\tag{3.1}
\]

The intrinsic flat quotient therefore has

\[
\boxed{
\dim Q_0=256-60=196.
}
\tag{3.2}
\]

On a background with trivial common-fixed holonomy,

\[
\ker D_L=0,
\]

so

\[
\boxed{
\operatorname{rank}D_L=64,
}
\tag{3.3}
\]

and

\[
\boxed{
\dim Q_L=256-64=192.
}
\tag{3.4}
\]

The four-dimensional difference is the exact gauge-rank seam.

---

## 4. Two exact Lorentz approaches to the same flat endpoint

Let

\[
A_{01},A_{02},A_{03}\in\mathfrak{so}(1,3)
\]

be the three boost generators

\[
(A_{0i})_{0i}=(A_{0i})_{i0}=1.
\]

Their common kernel is zero:

\[
\boxed{
\bigcap_{i=1}^3\ker A_{0i}=0.
}
\tag{4.1}
\]

For any scalar \(a\) define the rational Cayley curve

\[
C_{aA}(t)
=
\left(I+\frac t2aA\right)
\left(I-\frac t2aA\right)^{-1}.
\tag{4.2}
\]

Whenever the inverse exists,

\[
C_{aA}(t)^T\eta C_{aA}(t)=\eta,
\]

\[
\det C_{aA}(t)=1.
\]

For sufficiently small real \(t\), the \(00\) entry is positive, so this lies
in the proper orthochronous component.

Set every edge link to identity except the three positive Role edges
\((o,A),(o,B),(o,C)\) leaving the origin.

### History A

Use scales

\[
(1,1,1).
\]

### History B

Use scales

\[
(1,2,3).
\]

Both histories converge to

\[
L_0=I.
\]

For every sufficiently small nonzero \(t\), their common fixed space is zero
by (4.1), hence

\[
\ker D_{L_t}=0.
\]

The exact certificate checks at

\[
t=\frac17
\]

that both have rank \(64\).

---

## 5. Why PR #135 gives the same memory for both histories

Along both histories choose

\[
b_t=0,
\qquad
e_t=0.
\]

Then the PR #123 synthesis maps are identically

\[
\mathcal B_y=0,
\qquad
\mathcal S_y=0.
\]

Hence the intrinsic local active projector is zero at every site for every
\(t\), and its limit is zero.

Thus

\[
\boxed{
W_y^*=0
\quad\forall y.
}
\tag{5.1}
\]

Globally, for every nonzero \(t\),

\[
\ker D_{L_t}=0.
\]

Equivalently the common-fixed holonomy bundle is zero.

Therefore

\[
\boxed{
\mathcal K^*=0.
}
\tag{5.2}
\]

Both histories have the same landed memory

\[
\boxed{
\Xi_{\rm str}^{A}
=
\Xi_{\rm str}^{B}
=
((0)_y,0).
}
\tag{5.3}
\]

Any distinction found below is therefore invisible to PR #135.

---

## 6. First-order lost gauge-image map

At the flat endpoint, the kernel of \(D_0\) consists of constant node fields.

Let

\[
v\in V
\]

and let \(c^v\) be the constant node section.

For one perturbed edge,

\[
(I-C_{aA}(t))v
=
-taAv+O(t^2).
\]

Hence

\[
\boxed{
\Gamma(v)
=
\lim_{t\to0}
\frac1tD_{L_t}c^v
}
\tag{6.1}
\]

is the edge cochain supported on the perturbed edges with values

\[
-a_rA_rv.
\]

For History A call this map

\[
\Gamma_A:V\to\mathcal E,
\]

and for History B call it

\[
\Gamma_B.
\]

The certificate gives

\[
\boxed{
\operatorname{rank}\Gamma_A
=
\operatorname{rank}\Gamma_B
=
4.
}
\tag{6.2}
\]

Moreover

\[
\operatorname{im}\Gamma_A
\cap
\operatorname{im}D_0
=
0
\]

and similarly for \(B\), in the sense of quotient rank.

Thus define

\[
\boxed{
\mathcal I_A
=
\operatorname{im}D_0+\operatorname{im}\Gamma_A,
}
\tag{6.3}
\]

\[
\boxed{
\mathcal I_B
=
\operatorname{im}D_0+\operatorname{im}\Gamma_B.
}
\tag{6.4}
\]

Exactly,

\[
\operatorname{rank}\mathcal I_A
=
\operatorname{rank}\mathcal I_B
=
64.
\tag{6.5}
\]

These are the Grassmannian limits of the gauge-image spaces along the two
transversal rank-64 approaches.

---

## 7. The two image-incidence memories are different

The exact augmented rank is

\[
\boxed{
\operatorname{rank}
\left(
\mathcal I_A+\mathcal I_B
\right)
=
65.
}
\tag{7.1}
\]

Therefore

\[
\boxed{
\mathcal I_A\ne\mathcal I_B.
}
\tag{7.2}
\]

A concrete separating cochain is obtained from

\[
v=e_0
\]

in History A:

\[
z
=
\Gamma_Ae_0.
\]

It has exactly three nonzero edge values:

\[
z_{(o,A)}=-e_1,
\]

\[
z_{(o,B)}=-e_2,
\]

\[
z_{(o,C)}=-e_3.
\tag{7.3}
\]

The exact ranks give

\[
\boxed{
z\in\mathcal I_A,
}
\tag{7.4}
\]

but

\[
\boxed{
z\notin\mathcal I_B.
}
\tag{7.5}
\]

Thus the missing information is not merely the four-dimensional endpoint
kernel.

Both histories gain the same four constant node directions at the endpoint.

They differ in **where those directions were landing in edge-cochain space
before they disappeared from the image**.

---

## 8. General image-incidence resolution

For any finite covariant node-difference map

\[
D:\mathcal N\to\mathcal E
\]

define its image-incidence fibre by

\[
\boxed{
\operatorname{ResIm}(D)
=
\{
\mathcal I\le\mathcal E:
\operatorname{im}D\le\mathcal I
\}.
}
\tag{8.1}
\]

If one also wants to remember the rank of a specified punctured approach, use
the fixed-dimensional component

\[
\operatorname{ResIm}_r(D)
=
\{
\mathcal I:
\operatorname{im}D\le\mathcal I,\ 
\dim\mathcal I=r
\}.
\tag{8.2}
\]

Every convergent Grassmannian limit

\[
\mathcal I_*=
\lim\operatorname{im}D_t
\]

belongs to this incidence fibre.

The quotient-space presentation is

\[
\boxed{
G_*
=
\mathcal I_*/\operatorname{im}D
\le
\mathcal E/\operatorname{im}D.
}
\tag{8.3}
\]

Given \(D\), the two presentations are losslessly equivalent:

\[
\boxed{
\mathcal I_*
\longleftrightarrow
G_*.
}
\tag{8.4}
\]

This is exactly analogous to the local incidence resolution of #130/#135,
but it lives on the **image side of the affine gauge map**, not in the
Role-label coefficient kernel.

---

## 9. Why a first derivative is not the definition

The witness above is transversal, so the lost image is represented by the
first derivative \(\Gamma\).

That is not universal.

A history can activate a lost image at order

\[
t^k
\]

or through a smooth-flat factor.

Finite jets were already shown insufficient for the PR #135 memory, and the
same phenomenon occurs here.

Therefore the structural object is the limiting subspace

\[
\mathcal I_*,
\]

not a chosen derivative order.

The derivative map is only a convenient coordinate on a transversal chart.

---

## 10. Frame covariance of the gauge-image resolution

Let \(g_x:V_x\to V'_x\) be invertible Lorentz frame maps.

Define node and edge maps

\[
(G_0c)_x=g_xc_x,
\]

\[
(G_1u)_{x,r}=g_xu_{x,r}.
\]

With

\[
L'_{x,r}
=
g_xL_{x,r}g_{x+r}^{-1},
\]

one has exactly

\[
\boxed{
D_{L'}G_0
=
G_1D_L.
}
\tag{10.1}
\]

Hence

\[
\boxed{
\operatorname{im}D_{L'}
=
G_1\operatorname{im}D_L.
}
\tag{10.2}
\]

For a supplied incidence lift define

\[
\boxed{
\mathcal I'
=
G_1\mathcal I.
}
\tag{10.3}
\]

Then

\[
\mathcal I\in\operatorname{ResIm}(D_L)
\Longrightarrow
\mathcal I'\in\operatorname{ResIm}(D_{L'}).
\]

Identity, composition and inverse are inherited from \(G_1\).

Thus the image-incidence resolution is an exact finite frame groupoid.

---

## 11. Role/site naturality

A Role/site relabeling permutes:

- sites;
- positive Role edges;
- node coefficient blocks;
- edge coefficient blocks.

Let the induced permutation maps be

\[
U_0:\mathcal N\to\mathcal N,
\qquad
U_1:\mathcal E\to\mathcal E.
\]

The relabeled connection satisfies

\[
D_{L^\sigma}U_0
=
U_1D_L.
\]

Therefore

\[
\operatorname{im}D_{L^\sigma}
=
U_1\operatorname{im}D_L,
\]

and the incidence memory transforms by

\[
\mathcal I^\sigma
=
U_1\mathcal I.
\]

No preferred Role edge is introduced by the resolution.

The exact witness uses three named edges only to prove nonreconstruction; the
structural definition does not.

---

## 12. Observer-positive edge metric

The owned observer at site \(x\) gives the positive form

\[
h_{n_x}.
\]

Define the counting edge product

\[
\boxed{
\langle u,v\rangle_{h_n,1}
=
\sum_{x,r}
h_{n_x}(u_{x,r},v_{x,r}).
}
\tag{12.1}
\]

This is positive definite.

Under a Lorentz frame,

\[
n'_x=g_xn_x,
\]

and the observer congruence gives

\[
h_{n'_x}(g_xu,g_xv)
=
h_{n_x}(u,v).
\]

Therefore

\[
\boxed{
G_1:
(\mathcal E,h_n)
\to
(\mathcal E',h_{n'})
}
\tag{12.2}
\]

is an isometry.

The counting product on the edge labels is Role/site permutation invariant.

No extra metric is introduced.

---

## 13. Resolved quotient energy

For

\[
\mathcal I\in\operatorname{ResIm}(D_L)
\]

define

\[
\boxed{
E_{\mathcal I}(b;n)
=
\operatorname{dist}_{h_n,1}(b,\mathcal I)^2.
}
\tag{13.1}
\]

Equivalently,

\[
E_{\mathcal I}(b;n)
=
\|P_{\mathcal I^{\perp_{h_n,1}}}b\|_{h_n,1}^2.
\tag{13.2}
\]

This definition needs no pseudoinverse.

Its exact zero locus is

\[
\boxed{
E_{\mathcal I}(b;n)=0
\iff
b\in\mathcal I.
}
\tag{13.3}
\]

For the intrinsic incidence

\[
\mathcal I=\operatorname{im}D_L,
\]

one gets the ordinary positive quotient norm on \(Q_L\).

---

## 14. Exact full-affine invariance

Under a full affine node gauge,

\[
L'_{x,r}
=
g_xL_{x,r}g_{x+r}^{-1},
\]

\[
b'
=
G_1b+D_{L'}c,
\]

\[
n'_x=g_xn_x.
\]

Transport the resolution memory by

\[
\mathcal I'=G_1\mathcal I.
\]

Because

\[
D_{L'}c
\in
\operatorname{im}D_{L'}
\subseteq
\mathcal I',
\]

translation by \(D_{L'}c\) does not change the distance to \(\mathcal I'\).

Because \(G_1\) is an observer isometry,

\[
\operatorname{dist}_{h_{n'},1}(G_1b,\mathcal I')
=
\operatorname{dist}_{h_n,1}(b,\mathcal I).
\]

Therefore

\[
\boxed{
E_{\mathcal I'}(b';n')
=
E_{\mathcal I}(b;n).
}
\tag{14.1}
\]

This is a complete finite full-affine action scalar.

It is not merely pure-translation invariant.

---

## 15. Intrinsic and resolved flat branches

At exact flat \(L=I\), the intrinsic incidence is

\[
\mathcal I_{\rm int}
=
\operatorname{im}D_0,
\]

with

\[
\dim\mathcal I_{\rm int}=60.
\]

Therefore

\[
\boxed{
\dim Q_{\rm int}=196.
}
\tag{15.1}
\]

For either generic rank-64 history above, the resolved endpoint incidence has

\[
\dim\mathcal I_*=64.
\]

Therefore

\[
\boxed{
\dim Q_{\rm resolved}=192.
}
\tag{15.2}
\]

So one pointwise flat background has multiple resolved lifts.

### Intrinsic flat lift

\[
(L_0,\mathcal I_{\rm int})
\]

keeps every actual nongauge flat edge class.

### Generic-limit flat lift

\[
(L_0,\mathcal I_*)
\]

forgets the four edge directions that were still gauge-image directions
arbitrarily close to the endpoint.

Both are exact finite objects.

They answer different continuity questions.

---

## 16. Continuity theorem on the resolved carrier

Let

\[
t\mapsto(L_t,b_t,n_t,\mathcal I_t)
\]

be a family such that:

1. \(L_t,b_t,n_t\) are continuous;
2. \(\dim\mathcal I_t\) is constant;
3. \(\mathcal I_t\) is continuous in the Grassmannian topology.

Then the orthogonal projectors

\[
P_{\mathcal I_t}^{h_{n_t}}
\]

vary continuously.

Therefore

\[
\boxed{
E_{\mathcal I_t}(b_t;n_t)
}
\]

is continuous.

In particular, if for \(t\ne0\)

\[
\mathcal I_t=\operatorname{im}D_{L_t}
\]

has constant rank and

\[
\operatorname{im}D_{L_t}\to\mathcal I_*,
\]

then the endpoint value on the resolved state

\[
(L_0,b_0,n_0,\mathcal I_*)
\]

is the continuous limit.

The discontinuity of the pointwise intrinsic quotient is therefore resolved
by decorating the endpoint, not by pretending the rank did not change.

---

## 17. Exact separating energy witness

Use the cochain \(z\) of (7.3).

Since

\[
z\in\mathcal I_A,
\]

positivity gives

\[
\boxed{
E_{\mathcal I_A}(z)=0.
}
\tag{17.1}
\]

Since

\[
z\notin\mathcal I_B,
\]

and the observer edge metric is positive definite,

\[
\boxed{
E_{\mathcal I_B}(z)>0.
}
\tag{17.2}
\]

Thus the two histories have:

- the same pointwise endpoint;
- the same PR #135 structural memory;
- different resolved affine quotient readouts.

This proves strict insufficiency of the old memory.

No numerical projector needs to be evaluated.

Membership and positivity are enough.

---

## 18. Structural minimality

Fix \(D\) and the positive edge metric.

For every incidence space \(\mathcal I\), the universal quadratic readout is

\[
b\mapsto E_{\mathcal I}(b).
\]

Its zero locus is exactly \(\mathcal I\).

Therefore if

\[
E_{\mathcal I_1}(b)
=
E_{\mathcal I_2}(b)
\quad
\text{for every }b,
\]

then their zero sets agree and

\[
\boxed{
\mathcal I_1=\mathcal I_2.
}
\tag{18.1}
\]

Hence no source-independent universal forgetful map may identify two distinct
image-incidence subspaces while retaining the full resolved quotient energy.

Because \(D\) is already part of the background, the lossless compressed
presentation is

\[
G=\mathcal I/\operatorname{im}D.
\]

Thus

\[
\boxed{
\mathcal I
\;\simeq\;
G
}
\tag{18.2}
\]

is the structural minimum for this universal readout, up to natural
equivalence.

As in #135, one fixed downstream source may see a smaller quotient.

That source-dependent compression is not the universal structural memory.

---

## 19. Relation to the non-closed gauge relation

Near the flat connection, the affine gauge relation is not closed after the
pointwise resolution memory is forgotten.

A large node parameter can combine with a small Lorentz link deformation so
that

\[
D_{L_t}c_t
\]

has a finite nonzero edge limit.

Such a limiting edge direction belongs precisely to a limiting gauge-image
space \(\mathcal I_*\).

A continuous gauge invariant along that history must be blind to it.

The resolved energy does exactly that:

\[
u\in\mathcal I_*
\Longrightarrow
E_{\mathcal I_*}(u)=0.
\]

Different histories can produce different \(\mathcal I_*\).

That is why one pointwise flat scalar cannot simultaneously remember every
flat quotient direction and be continuous along every curved approach.

The resolution does not remove the theorem.

It separates the different approach branches instead of identifying them.

---

## 20. Relation to the joint-holonomy frontier

The concurrent joint-holonomy pressure finds that, on generic curved
backgrounds, a complete family of affine loop residuals can coordinatize the
192-dimensional quotient.

The present result identifies the invariant carrier beneath those
coordinates:

\[
Q_L
=
\mathcal E/\operatorname{im}D_L.
\]

A two-loop polynomial residual is therefore a generic chart on this quotient,
not the definition of the quotient.

At a rank transition, the correct resolved carrier is

\[
\boxed{
Q_{\mathcal I}
=
\mathcal E/\mathcal I.
}
\tag{20.1}
\]

On the intrinsic flat branch it has dimension 196.

On a generic-limit flat branch it has dimension 192.

This is the precise sense in which the flat plaquette/cycle chart and generic
joint-holonomy chart belong to one rank-stratified quotient geometry without
being one fixed coordinate formula.

---

## 21. Relation to the relative-solder completion

The relative solder

\[
\widehat\Theta
=
\Theta-b^{\flat_n}
\]

is exactly affine covariant but blind to arbitrary matched edge-diagonal
changes.

On a regular curved background, if such a change is not node gauge, then

\[
u\notin\operatorname{im}D_L.
\]

For the intrinsic image incidence,

\[
\mathcal I=\operatorname{im}D_L,
\]

one has

\[
E_{\mathcal I}(u)>0.
\]

Thus the resolved quotient energy supplies exactly the kind of independent
translation-sensitive action term that the relative-solder star term lacks.

At a rank-transition endpoint, the answer depends on the supplied incidence
memory, as continuity requires.

---

## 22. What is and is not selected at action level

The canonical star density and the new resolved quotient scalar have different
functional dependence.

Schematically one may now form

\[
\boxed{
S_{\rm trial}
=
\alpha\,S_{\widehat\star}
+
\beta\,E_{\mathcal I}.
}
\tag{22.1}
\]

Both terms are full-affine invariants on the resolved carrier.

Nothing in this memo selects

\[
\beta/\alpha.
\]

Nor should a coefficient selector be invented before variation and physical
quotient are checked.

The current result is only:

- one exact relative-solder curvature channel exists;
- one exact positive affine-shift quotient channel exists on the resolved
  carrier;
- their relative action coefficient remains open;
- whether that coefficient survives to \(d_E\) or \(d_P\) is downstream.

This is precisely the KILL-FIRST discipline required by the repository.

---

## 23. Why PR #135 memory cannot simply be enlarged by interpretation

The two memories live in different spaces.

### PR #135 local memory

\[
W_y
\le
\ker\mathcal B_y
\subset E_{\rm lab}.
\]

It remembers lost Role-label coefficient directions in the relative A/e
synthesis problem.

### PR #135 global memory

\[
\mathcal K
\le
\ker D_L
\]

after basepoint identification.

It remembers node vectors that remain in the common fixed-holonomy kernel
along an approach.

### Present memory

\[
G_*
\le
\mathcal E/\operatorname{im}D_L.
\]

It remembers where node-kernel directions were still landing in the **edge
image** before the rank drop.

The witness has

\[
W_y=0,
\qquad
\mathcal K=0,
\]

for both histories but

\[
G_A\ne G_B.
\]

Therefore this is not a change of notation for \(\Xi_{\rm str}\).

It is a genuinely orthogonal resolution seam.

---

## 24. The next variational blocker

A resolved action depends on an incidence datum.

There are three mathematically different variational contracts.

### A. Frozen memory

Treat \(\mathcal I\) as supplied approach/superselection data and vary only
the pointwise fields.

This is not automatically stable under arbitrary variations of \(L\), because

\[
\operatorname{im}D_L\subseteq\mathcal I
\]

must remain satisfied.

### B. Constrained Grassmannian variable

Vary \(\mathcal I\) together with \(L,b,e,n\), subject to

\[
\operatorname{im}D_L\subseteq\mathcal I
\]

and fixed incidence rank.

Then \(E_{\mathcal I}\) has additional Euler directions from motion of the
subspace itself.

### C. History-germ variation

Regard \(\mathcal I\) as reconstructed from a complete approach germ and vary
the resolved history rather than only its endpoint.

This preserves the literal origin of the memory but enlarges the variational
carrier.

These three contracts need not have the same \(d_E\) or \(d_P\).

Therefore no final variational claim follows until this choice is classified.

---

## 25. Theorem-ready statements

1. **Affine node coboundary.**
   \[
   (D_Lc)_{x,r}=c_x-L_{x,r}c_{x+r}.
   \]

2. **Translation orbit quotient.**
   \[
   Q_L=\mathcal E/\operatorname{im}D_L.
   \]

3. **Kernel/holonomy equivalence.**
   \[
   \ker D_L\cong\bigcap_\gamma\operatorname{Fix}P_\gamma.
   \]

4. **Rank formula.**
   \[
   \operatorname{rank}D_L=4|X|-\dim\mathcal H_o.
   \]

5. **Flat \(L=2\) rank.**
   \[
   \operatorname{rank}D_0=60,
   \qquad
   \dim Q_0=196.
   \]

6. **Generic \(L=2\) rank.**
   On trivial common-fixed holonomy,
   \[
   \operatorname{rank}D_L=64,
   \qquad
   \dim Q_L=192.
   \]

7. **Gauge-image incidence.**
   Every fixed-rank image limit satisfies
   \[
   \operatorname{im}D_0\subseteq\mathcal I_*.
   \]

8. **Lost quotient memory.**
   \[
   G_*=\mathcal I_*/\operatorname{im}D_0.
   \]

9. **PR #135 insufficiency.**
   Two same-endpoint histories can have equal
   \[
   ((W_y),\mathcal K)
   \]
   but different \(\mathcal I_*\).

10. **Exact witness ranks.**
    \[
    \operatorname{rank}\mathcal I_A
    =
    \operatorname{rank}\mathcal I_B
    =
    64,
    \]
    \[
    \operatorname{rank}(\mathcal I_A+\mathcal I_B)=65.
    \]

11. **Frame covariance.**
    \[
    D_{L'}G_0=G_1D_L.
    \]

12. **Image-memory covariance.**
    \[
    \mathcal I'=G_1\mathcal I.
    \]

13. **Resolved quotient energy.**
    \[
    E_{\mathcal I}(b)
    =
    \operatorname{dist}(b,\mathcal I)^2.
    \]

14. **Full-affine invariance.**
    \[
    E_{\mathcal I'}(b';n')
    =
    E_{\mathcal I}(b;n).
    \]

15. **Zero-locus theorem.**
    \[
    E_{\mathcal I}(b)=0
    \iff
    b\in\mathcal I.
    \]

16. **Resolved continuity.**
    Fixed-rank Grassmannian continuity of \(\mathcal I_t\) implies continuity
    of \(E_{\mathcal I_t}\).

17. **Universal structural minimality.**
    The universal quadratic readout determines \(\mathcal I\) from its zero
    locus.

18. **Intrinsic/resolved flat split.**
    \[
    \dim Q_{\rm int}=196,
    \qquad
    \dim Q_{\rm generic-limit}=192.
    \]

---

## 26. Hostile controls

| Control | Result |
|---|---|
| exact flat \(L=I\) | rank \(D_0=60\) |
| three rational boost Cayley links | proper Lorentz |
| History A at \(t=1/7\) | rank \(D=64\) |
| History B at \(t=1/7\) | rank \(D=64\) |
| \(b=e=0\) along both histories | same PR #135 local memory |
| common fixed space on punctured histories | zero in both |
| first lost-image map | rank 4 in both |
| \(\mathcal I_A,\mathcal I_B\) | both rank 64 |
| joint incidence span | rank 65 |
| explicit \(z\) | \(z\in I_A,\ z\notin I_B\) |
| intrinsic flat quotient | dimension 196 |
| generic-limit resolved quotient | dimension 192 |
| pseudoinverse | not used |
| supplied affine point | not used |
| Lean source | not changed |

---

## 27. Terminal disposition

The affine-action frontier has now separated three different finite objects
that had previously been close enough to confuse:

1. the relative solder, which removes the inhomogeneous translation law;
2. the affine orbit quotient \(Q_L\), which retains nongauge edge shift data;
3. the image-incidence memory, which resolves the rank-changing gauge quotient.

The landed PR #135 memory remains correct and minimal for its own A/e selected
readout.

It is not the memory required by the affine gauge-image quotient.

The exact new terminal is

\[
\boxed{
\texttt{AFFINE-GAUGE-IMAGE-RESOLUTION-CONSTRUCTED}.
}
\]

The exact negative subterminal is

\[
\boxed{
\texttt{PR135-KERNEL-MEMORY-INSUFFICIENT-FOR-GAUGE-IMAGE-SEAM}.
}
\]

The next legitimate pressure is no longer another covariance construction.

It is:

\[
\boxed{
\text{VARIATION OF THE RESOLVED INCIDENCE CARRIER}.
}
\]

One must decide whether \(\mathcal I\) is frozen, constrained-dynamical, or
history-derived under variation, and then compute the resulting
\(d_E\to d_P\).

Until that is done, the new quadratic is an exact action building block, not a
completed physical theory.
