# MEMO A4D — Grassmann graph-closure resolution of the affine gauge-rank seam

**Task:** \`EXP-A4D-GRASSMANN-GRAPH-CLOSURE-RESOLUTION\`  
**Execution:** PR #193  
**Status:** terminal EXPENSIVE research classification  
**Baseline:** \`6eb2886d054d2aa34d49b8b7d419529b6a9839f5\`

## 0. Principal verdict

The rank-changing affine node-gauge quotient admits a canonical intrinsic
resolution.

It is not the full arbitrary incidence fibre

\[
\{\mathcal I:\operatorname{im}D_L\subseteq\mathcal I\}
\]

introduced as a universal envelope in PR #188.

The canonical resolved carrier is the closure of the regular rank-64 graph

\[
\Gamma_{\rm reg}
=
\left\{
(L,\operatorname{im}D_L):
\operatorname{rank}D_L=64
\right\}
\]

inside

\[
\mathcal L\times\operatorname{Gr}(64,\mathcal E),
\]

where \(\mathcal L\) is the finite proper-Lorentz link space and

\[
\mathcal E=C^1_+(X,V).
\]

At the \(L=2\) flat point \(L_0=I\), let

\[
U=\operatorname{im}D_0,
\qquad
K=\ker D_0,
\qquad
Q=\mathcal E/U.
\]

Exactly,

\[
\dim U=60,
\qquad
\dim K=4,
\qquad
\dim Q=196.
\]

Every graph-closure lift over \(L_0\) is a 64-plane
\(\mathcal I_*\) satisfying

\[
U\subseteq\mathcal I_*,
\]

hence is equivalent to a 4-plane

\[
G_*=\mathcal I_*/U\in\operatorname{Gr}(4,Q).
\]

The exceptional fibre is **not** all of
\(\operatorname{Gr}(4,196)\).

Choose any spanning tree of the positive-edge graph.  Then

\[
Q
\cong
H^1(\Gamma;V),
\]

with cycle rank

\[
|E|-|X|+1
=
64-16+1
=
49.
\]

After exact tree gauge, a near-flat connection is encoded by 49 fundamental
proper-Lorentz holonomies.  In infinitesimal/Cayley coordinates

\[
\Omega=(\Omega_\gamma)_\gamma
\in
H^1(\Gamma;\mathfrak{so}(1,3)),
\]

define

\[
\boxed{
A_\Omega:V\to H^1(\Gamma;V),
\qquad
v\mapsto(\Omega_\gamma v)_\gamma.
}
\tag{0.1}
\]

The parameter space

\[
W
=
H^1(\Gamma;\mathfrak{so}(1,3))
\]

has dimension

\[
\boxed{\dim W=49\cdot6=294.}
\tag{0.2}
\]

The flat exceptional fibre is exactly

\[
\boxed{
\mathfrak F_0
=
\overline{
\left\{
\operatorname{im}A_\Omega:
\operatorname{rank}A_\Omega=4
\right\}
}
\subset
\operatorname{Gr}(4,Q).
}
\tag{0.3}
\]

Under the Plücker embedding this is the closure of the rational quartic map

\[
\boxed{
\rho:
\mathbb P(W)
\dashrightarrow
\operatorname{Gr}(4,Q),
\qquad
[\Omega]
\mapsto
[\wedge^4A_\Omega].
}
\tag{0.4}
\]

Its base locus is exactly

\[
\{\operatorname{rank}A_\Omega\le3\}.
\]

The map has generic projective fibre dimension zero.  Hence

\[
\boxed{
\dim\mathfrak F_0
=
293.
}
\tag{0.5}
\]

By comparison,

\[
\dim\operatorname{Gr}(4,196)
=
4(196-4)
=
768.
\]

Therefore the canonical graph-closure exceptional fibre has codimension

\[
\boxed{768-293=475}
\tag{0.6}
\]

inside the arbitrary four-plane incidence fibre.

This is the decisive carrier-selection result.

The terminal is

\[
\boxed{
\texttt{AFFINE-GAUGE-RANK-SEAM-RESOLVED-BY-GRASSMANN-GRAPH-CLOSURE}.
}
\]

The earlier PR #188 image-incidence object remains useful as a universal
envelope and for source-independent quadratic readouts, but the actual
link-generated resolved states form the much smaller graph-closure subset
described above.

---

## 1. The exact affine node-gauge map

For fixed linear links \(L\),

\[
D_L:C^0(X,V)\to C^1_+(X,V)
\]

is

\[
(D_Lc)_{x,r}
=
c_x-L_{x,r}c_{x+r}.
\tag{1.1}
\]

At the period-two flat point,

\[
L_{x,r}=I,
\]

this is the ordinary graph coboundary with vector coefficients.

The graph has

\[
|X|=16,
\qquad
|E_+|=64.
\]

Because the graph is connected,

\[
\ker D_0
=
\{\text{constant node vectors}\}
\cong V.
\]

Thus

\[
\boxed{
\dim K=4.
}
\tag{1.2}
\]

The scalar graph incidence has rank

\[
16-1=15.
\]

Tensoring with \(V\),

\[
\boxed{
\operatorname{rank}D_0=15\cdot4=60.
}
\tag{1.3}
\]

Therefore

\[
\boxed{
\dim Q
=
256-60
=
196.
}
\tag{1.4}
\]

This reproduces the exact rank result of PR #188.

---

## 2. Spanning-tree normal form

Choose:

- a root node \(o\);
- a spanning tree \(T\subset E_+\).

There are

\[
64-(16-1)=49
\]

non-tree edges.

For a connection \(L\) sufficiently close to flat, use node Lorentz frame
transport along the tree to put every tree link into the identity frame.

The remaining 49 chord links become the based fundamental-loop holonomies

\[
P_\gamma\in SO^+(1,3),
\qquad
\gamma\in H_1(\Gamma).
\]

On the node-translation map, exact row/column elimination along the tree
separates:

1. the always-present \(4(|X|-1)=60\) tree-gauge image directions;
2. the root translation \(v\in V_o\), whose remaining chord-edge image is

\[
\boxed{
A_P(v)
=
\bigl((I-P_\gamma)v\bigr)_\gamma.
}
\tag{2.1}
\]

Consequently

\[
\boxed{
\operatorname{rank}D_L
=
60+\operatorname{rank}A_P.
}
\tag{2.2}
\]

In particular,

\[
\operatorname{rank}D_L=64
\iff
\bigcap_\gamma\operatorname{Fix}P_\gamma=0.
\tag{2.3}
\]

At flat,

\[
P_\gamma=I
\]

for every fundamental loop and

\[
A_P=0.
\]

The quotient of the edge space by the flat tree-gauge image is canonically

\[
Q
\cong
V^{49}
\cong
H^1(\Gamma;V).
\tag{2.4}
\]

This is the exact carrier in which the exceptional fibre lives.

---

## 3. Cayley coordinates remove nonlinear holonomy clutter

Near identity, write a fundamental holonomy as

\[
P_\gamma
=
\operatorname{Cayley}(X_\gamma)
=
\left(I+\frac12X_\gamma\right)
\left(I-\frac12X_\gamma\right)^{-1},
\]

with

\[
X_\gamma\in\mathfrak{so}(1,3).
\]

Exactly,

\[
I-P_\gamma
=
-X_\gamma
\left(I-\frac12X_\gamma\right)^{-1}.
\tag{3.1}
\]

Since \(X_\gamma\) commutes with every rational function of itself,

\[
I-P_\gamma
=
-\left(I-\frac12X_\gamma\right)^{-1}
X_\gamma.
\tag{3.2}
\]

The block factor

\[
-\left(I-\frac12X_\gamma\right)^{-1}
\]

is invertible and tends to \(-I\) as \(X_\gamma\to0\).

Therefore for every curve approaching flat,

\[
\boxed{
\lim\operatorname{im}A_P
=
\lim\operatorname{im}A_X,
}
\tag{3.3}
\]

where

\[
A_X(v)
=
(X_\gamma v)_\gamma.
\tag{3.4}
\]

Thus the nonlinear Lorentz holonomy problem reduces, at the seam, to one
linear family of maps

\[
A_\Omega\in\operatorname{Hom}(V,Q)
\]

with

\[
\Omega\in W
=
H^1(\Gamma;\mathfrak{so}(1,3)).
\]

No arbitrary external incidence subspace is introduced.

---

## 4. First-jet map

Let

\[
L(t)
\]

be a differentiable path with

\[
L(0)=I.
\]

Equivalently, after tree gauge let

\[
X_\gamma(t)
=
t\Omega_\gamma+O(t^2).
\]

The endpoint kernel is

\[
K\cong V.
\]

The abstract first-jet map required by the task is

\[
\Phi(\dot L):
K\to Q,
\qquad
k\mapsto[\dot D\,k].
\]

Under the tree/cycle identification it is exactly

\[
\boxed{
\Phi(\dot L)
=
-A_\Omega
}
\tag{4.1}
\]

up to the inessential orientation sign convention for the fundamental loops.

Thus

\[
\operatorname{rank}\Phi
=
\operatorname{rank}A_\Omega.
\]

This turns the seam question into ordinary finite-dimensional rank geometry.

---

## 5. Transverse limit theorem

Assume

\[
\operatorname{rank}\Phi=4.
\]

Then

\[
\wedge^4\Phi\ne0.
\]

For

\[
X(t)=t\Omega+O(t^2),
\]

the Plücker vector satisfies

\[
\wedge^4A_{X(t)}
=
t^4\wedge^4A_\Omega
+
O(t^5).
\]

Therefore the projective limit is

\[
[\wedge^4A_\Omega].
\]

Equivalently,

\[
\boxed{
G_*
=
\operatorname{im}\Phi.
}
\tag{5.1}
\]

Since

\[
\mathcal I_*/U=G_*,
\]

the incidence lift is the unique 64-plane containing \(U\) with quotient
\(G_*\):

\[
\boxed{
\mathcal I_*
=
\pi^{-1}(\operatorname{im}\Phi),
\qquad
\pi:\mathcal E\to Q.
}
\tag{5.2}
\]

If one chooses a complement of \(U\), this is the earlier shorthand

\[
\mathcal I_*=U\oplus\operatorname{im}\Phi.
\]

Thus the requested transverse formula is proved.

Higher jets have no effect whenever the first jet has full rank.

---

## 6. Exact transverse control

The exact certificate uses

\[
\Omega
=
B_{01}+R_{23},
\]

where \(B_{01}\) is the \(0/1\) boost generator and \(R_{23}\) the \(2/3\)
rotation generator.

Exactly,

\[
\det\Omega=-1,
\]

so

\[
\operatorname{rank}\Omega=4.
\]

Putting this generator on one fundamental cycle gives

\[
\operatorname{rank}A_\Omega=4.
\]

The rational Cayley sample at

\[
t=\frac17
\]

is proper Lorentz and satisfies

\[
\operatorname{rank}(I-P(t))=4.
\]

This is the smallest exact transverse witness.

---

## 7. Plücker classification of the exceptional fibre

The vector space

\[
W
=
H^1(\Gamma;\mathfrak{so}(1,3))
\]

has dimension 294.

The stacked map

\[
\Omega\mapsto A_\Omega
\]

is linear.

Each Plücker coordinate of

\[
\operatorname{im}A_\Omega
\]

is a \(4\times4\) minor of a \(196\times4\) matrix linear in \(\Omega\).

Hence every Plücker coordinate is homogeneous degree four.

Therefore the rank-4 locus defines the rational quartic map

\[
\rho:
\mathbb P^{293}
\dashrightarrow
\operatorname{Gr}(4,196).
\]

Its base locus is exactly

\[
\mathcal B
=
\{
[\Omega]:
\operatorname{rank}A_\Omega\le3
\}.
\tag{7.1}
\]

The exceptional fibre is

\[
\boxed{
\mathfrak F_0
=
\overline{\rho(\mathbb P(W)\setminus\mathcal B)}.
}
\tag{7.2}
\]

This is independent of spanning-tree choice: changing the tree merely changes
the basis of

\[
H^1(\Gamma;V)
\]

by an invertible linear transformation.

---

## 8. Generic fibre of the quartic map

To determine the dimension of \(\mathfrak F_0\), choose a tuple whose cycle
components span all six generators of

\[
\mathfrak{so}(1,3).
\]

Its stacked map is injective.

Suppose another injective tuple \(B\in W\) has the same image.

Then there is a unique

\[
S\in GL(V)
\]

such that

\[
A_B=A_\Omega S.
\]

Blockwise,

\[
B_\gamma=\Omega_\gamma S.
\]

Because the \(\Omega_\gamma\) span all of \(\mathfrak{so}(1,3)\), this requires

\[
XS\in\mathfrak{so}(1,3)
\quad
\text{for every }
X\in\mathfrak{so}(1,3).
\]

Equivalently,

\[
(XS)^T\eta+\eta XS=0
\]

for all six Lorentz generators.

The exact 16-unknown linear system has rank

\[
\boxed{15}.
\]

Its solution is

\[
\boxed{
S=\lambda I.
}
\tag{8.1}
\]

Thus after projectivizing \(W\), the fibre at this point is a singleton.

By upper-semicontinuity of fibre dimension, the rational map has generic fibre
dimension zero.

Therefore

\[
\boxed{
\dim\mathfrak F_0
=
\dim\mathbb P(W)
=
293.
}
\tag{8.2}
\]

The Grassmannian ambient dimension is

\[
\dim\operatorname{Gr}(4,196)
=
768.
\]

Hence the canonical exceptional fibre is a proper subvariety of codimension

\[
\boxed{475}.
\]

This is the exact minimality improvement over the universal PR #188 incidence
envelope.

---

## 9. Higher jets: exact criterion

Let

\[
X(t)
=
t\Omega_1+t^2\Omega_2+t^3\Omega_3+\cdots
\in W
\]

be an analytic or formal path with

\[
\operatorname{rank}A_{X(t)}=4
\quad(t\ne0).
\]

### Case 1 — full-rank first jet

If

\[
\operatorname{rank}A_{\Omega_1}=4,
\]

then

\[
\wedge^4A_{X(t)}
=
t^4\wedge^4A_{\Omega_1}+O(t^5)
\]

and the limit is completely determined by \(\Omega_1\).

No higher jet is required.

### Case 2 — rank-deficient first jet

If

\[
\operatorname{rank}A_{\Omega_1}<4,
\]

then

\[
\wedge^4A_{\Omega_1}=0.
\]

The order-\(t^4\) Plücker coefficient vanishes.

Since the punctured map still has rank four, the first nonzero Plücker
coefficient occurs at higher order and necessarily depends on higher jet data.

Thus:

\[
\boxed{
\text{higher jets are required exactly when }
\operatorname{rank}\Phi<4.
}
\tag{9.1}
\]

This is a statement about determination of the endpoint resolved point from
the first jet.

It does not say that higher jets enlarge the resolved carrier.

---

## 10. Same first jet, different resolved points

The exact certificate gives a direct hostile control.

Let the common first jet have only

\[
\Omega_{1,\gamma_0}=B_{01}
\]

on one fundamental cycle.

Then

\[
\operatorname{rank}A_{\Omega_1}=2.
\]

The first-jet kernel contains

\[
\operatorname{span}\{e_2,e_3\}.
\]

### History A

At order \(t^2\), activate

\[
R_{23}
\]

on a second fundamental cycle \(\gamma_1\).

### History B

Use the same first jet, but activate

\[
R_{23}
\]

on a different fundamental cycle \(\gamma_2\).

For both histories the punctured stacked map has rank four.

Their limiting four-planes are

\[
G_A
=
\operatorname{span}
\{
A_1e_0,
A_1e_1,
A_{2,A}e_2,
A_{2,A}e_3
\},
\]

\[
G_B
=
\operatorname{span}
\{
A_1e_0,
A_1e_1,
A_{2,B}e_2,
A_{2,B}e_3
\}.
\]

Exactly,

\[
\dim G_A=\dim G_B=4,
\]

while

\[
\boxed{
\dim(G_A+G_B)=6.
}
\tag{10.1}
\]

Hence

\[
G_A\ne G_B.
\]

The first jets are identical.

This proves strict first-jet nonreconstruction on the base locus of \(\rho\).

---

## 11. Higher-jet limits do not enlarge the exceptional fibre

Although the two histories above require second-order data, their limits are
already boundary points of the same first-jet Plücker variety.

For nonzero \(\varepsilon\), define

\[
\Omega_A(\varepsilon)
=
\Omega_1+\varepsilon\Omega_{2,A}.
\]

Then

\[
\operatorname{rank}A_{\Omega_A(\varepsilon)}=4
\]

for every nonzero \(\varepsilon\), and

\[
\operatorname{im}A_{\Omega_A(\varepsilon)}
\longrightarrow
G_A
\qquad
(\varepsilon\to0).
\]

Likewise for History B.

More generally, an arbitrary admissible path

\[
X(t)\in W
\]

with rank four for \(t\ne0\) is itself a path through the rank-4 locus of
\(W\).  Its image limit is therefore, by definition, a point of the closure

\[
\mathfrak F_0.
\]

Thus:

\[
\boxed{
\text{higher jets select boundary points of }\mathfrak F_0;
\text{ they do not create a larger carrier.}
}
\tag{11.1}
\]

This is the key graph-closure theorem.

---

## 12. Relation to PR #188

PR #188 constructed the universal incidence envelope

\[
\operatorname{ResIm}_{64}(D_0)
=
\{
\mathcal I:
U\subseteq\mathcal I,\ 
\dim\mathcal I=64
\}.
\]

After quotienting by \(U\), this full fibre is

\[
\operatorname{Gr}(4,Q)
=
\operatorname{Gr}(4,196).
\]

That object was correct as a universal source-independent resolution space.

The present task proves that link-generated limits occupy only

\[
\mathfrak F_0
\subsetneq
\operatorname{Gr}(4,196).
\]

Therefore the canonical graph-closure carrier is

\[
\boxed{
\overline{\Gamma_{\rm reg}}
\subset
\mathcal L\times\operatorname{Gr}(64,\mathcal E),
}
\tag{12.1}
\]

not the whole incidence envelope.

The two exact histories A/B from PR #188 are both legitimate points of
\(\mathfrak F_0\); the new theorem does not remove their distinction.

It classifies the full set of distinctions that can actually arise from the
proper-Lorentz link geometry.

---

## 13. Relation to PR #135

The PR #135 memory

\[
\Xi_{\rm str}=((W_y),\mathcal K)
\]

is still a different seam.

It records:

- local lost active directions in the relative A/e comparison;
- limiting common-fixed node-kernel directions.

The present graph-closure fibre records the **image** of the lost node-kernel
directions in edge-cochain quotient space.

The exact #188 witness already showed that equal PR #135 memory can lead to
different points of \(\mathfrak F_0\).

Thus graph closure does not collapse back to the older kernel memory.

---

## 14. Endpoint data versus history

The graph closure resolves the **action-value carrier** intrinsically.

A resolved endpoint state is simply

\[
\boxed{
(L,\mathcal I)
\in
\overline{\Gamma_{\rm reg}}.
}
\tag{14.1}
\]

No complete path history is part of this state.

Different histories may converge to the same resolved endpoint.

Conversely, at a base-locus point of the first-jet map, different histories
with the same pointwise endpoint and same first jet may select different
resolved endpoints, as §10 proves.

So there are three levels:

\[
\text{pointwise }L
\quad\leftarrow\quad
\text{resolved endpoint }(L,\mathcal I)
\quad\leftarrow\quad
\text{history germ}.
\]

The first arrow loses graph-closure fibre data.

The second arrow loses tangent/history data.

This precisely separates endpoint resolution from true history dependence.

---

## 15. Relation to PR #189 variation

PR #189 classified variation on the larger constrained incidence carrier

\[
\{
(D,\mathcal I):
\operatorname{im}D\subseteq\mathcal I
\}.
\]

That remains a valid universal envelope.

The present result selects the smaller physical candidate carrier

\[
\overline{\Gamma_{\rm reg}}.
\]

At the flat seam, its exceptional fibre has dimension 293 rather than the full

\[
4\cdot192=768
\]

free Grassmannian tangent dimension available in the envelope.

Therefore the final variational and physical quotient calculation must use the
tangent/conormal geometry of the graph closure, not assume that every
Grassmannian incidence variation is link-realizable.

In particular, the PR #189 result

\[
d_A=2,\qquad d_E=2
\]

under the full constrained-Grassmannian endpoint contract is a strong envelope
result, but coefficient-to-Euler independence must be rechecked on the selected
graph-closure tangent before promotion to the final physical quotient.

No contradiction is present: the carrier was intentionally not yet selected
when PR #189 was executed.

---

## 16. Generic regular stratum

When

\[
\operatorname{rank}D_L=64,
\]

there is no incidence ambiguity:

\[
\mathcal I=\operatorname{im}D_L.
\]

The graph closure agrees with the ordinary graph.

The affine-shift quotient dimension is

\[
256-64=192.
\]

The graph-closure resolution changes nothing on this open regular stratum.

All new geometry is concentrated at rank-drop seams.

---

## 17. Flat intrinsic point versus graph-closure points

The pointwise intrinsic flat quotient uses

\[
\mathcal I_{\rm int}=U=\operatorname{im}D_0
\]

of dimension 60.

That object is **not** a point of the fixed-rank-64 graph closure fibre, because
the graph closure stores limits of 64-dimensional gauge images.

The resolved flat points instead have

\[
U\subset\mathcal I_*,
\qquad
\dim\mathcal I_*=64,
\]

with

\[
\mathcal I_*/U\in\mathfrak F_0.
\]

Thus one should distinguish:

1. the intrinsic rank-60 flat quotient \(Q_0\), dimension 196;
2. the resolved rank-64 graph-closure lifts, each with quotient dimension 192.

The latter are the continuous endpoints of the generic rank-64 branch.

The former is the literal pointwise orbit quotient at flat.

The graph closure does not identify them by fiat.

It records them as different strata/objects.

---

## 18. Canonical carrier statement

Define the regular resolved graph

\[
\Gamma_{\rm reg}
=
\{
(L,\operatorname{im}D_L):
\operatorname{rank}D_L=r_{\max}
\}.
\]

For the \(L=2\) Role torus,

\[
r_{\max}=64.
\]

Then define

\[
\boxed{
\mathscr R_{\rm aff}
=
\overline{\Gamma_{\rm reg}}.
}
\tag{18.1}
\]

This construction uses only:

- the owned link space;
- the owned affine node-gauge map \(D_L\);
- finite-dimensional Grassmann topology/algebraic incidence.

It imports no arbitrary resolution memory.

On the regular stratum it is the ordinary gauge image.

At the flat seam its fibre is the projective variety \(\mathfrak F_0\) above.

Therefore

\[
\boxed{
\mathscr R_{\rm aff}
}
\]

is the canonical finite resolved carrier selected by the current data.

---

## 19. Theorem-ready statements

1. **Flat node-gauge ranks.**
   \[
   \dim K=4,\quad
   \dim U=60,\quad
   \dim Q=196.
   \]

2. **Cycle-space identification.**
   \[
   Q\cong H^1(\Gamma;V),
   \qquad
   \dim H^1(\Gamma)=49.
   \]

3. **Tree-gauge normal form.**
   \[
   \operatorname{rank}D_L
   =
   60+\operatorname{rank}
   \bigl[v\mapsto((I-P_\gamma)v)_\gamma\bigr].
   \]

4. **Cayley linearization.**
   The graph-closure image limits are unchanged when
   \((I-P_\gamma)\) is replaced by the Cayley coordinate
   \(X_\gamma\in\mathfrak{so}(1,3)\).

5. **First-jet space.**
   \[
   W=H^1(\Gamma;\mathfrak{so}(1,3)),
   \qquad
   \dim W=294.
   \]

6. **First-jet map.**
   \[
   \Phi(\dot L)=-A_\Omega.
   \]

7. **Transverse limit theorem.**
   If
   \[
   \operatorname{rank}\Phi=4,
   \]
   then
   \[
   \mathcal I_*/U=\operatorname{im}\Phi.
   \]

8. **Exceptional-fibre Plücker map.**
   \[
   \rho:[\Omega]\mapsto[\wedge^4A_\Omega]
   \]
   is quartic.

9. **Base locus.**
   \[
   \operatorname{Base}(\rho)
   =
   \{\operatorname{rank}A_\Omega\le3\}.
   \]

10. **Generic projective fibre.**
    It is zero-dimensional.

11. **Exceptional-fibre dimension.**
    \[
    \dim\mathfrak F_0=293.
    \]

12. **Properness inside arbitrary incidence.**
    \[
    \operatorname{codim}_{\operatorname{Gr}(4,196)}
    \mathfrak F_0
    =
    475.
    \]

13. **Higher-jet criterion.**
    Higher jets are needed to determine the endpoint iff the first-jet map has
    rank \(<4\).

14. **First-jet nonreconstruction witness.**
    Same rank-2 first jet admits two different exact proper-Lorentz resolved
    limits.

15. **No carrier enlargement by higher jets.**
    Every higher-jet limit lies in
    \[
    \mathfrak F_0.
    \]

16. **Canonical resolved carrier.**
    \[
    \mathscr R_{\rm aff}
    =
    \overline{\Gamma_{\rm reg}}.
    \]

---

## 20. Hostile controls

| Control | Result |
|---|---|
| \(L=2\) flat \(D_0\) | rank 60 |
| flat quotient | dimension 196 |
| graph cycle rank | 49 |
| first-jet parameter space | dimension 294 |
| invertible Lorentz generator \(B_{01}+R_{23}\) | rank 4 |
| six Lorentz generators | common kernel zero |
| right-stabilizer system | rank 15 / scalar line |
| projective exceptional variety | dimension 293 |
| full \(\mathrm{Gr}(4,196)\) | dimension 768 |
| first-jet rank 4 | higher jets irrelevant |
| first-jet rank 2 | higher jets required |
| same first jet / History A,B | different 4-plane limits |
| both higher-jet limits | boundary points of same \(\mathfrak F_0\) |
| arbitrary incidence memory | strictly larger than graph closure |
| Lean | not changed |

---

## 21. Terminal disposition

The carrier-selection problem is closed.

The graph closure is canonical, finite and intrinsic:

\[
\boxed{
\mathscr R_{\rm aff}
=
\overline{
\{(L,\operatorname{im}D_L):\operatorname{rank}D_L=64\}
}.
}
\]

At the flat seam, its exceptional fibre is the 293-dimensional quartic
Plücker image variety

\[
\boxed{
\mathfrak F_0
=
\overline{
\{
\operatorname{im}A_\Omega:
\Omega\in H^1(\Gamma;\mathfrak{so}(1,3)),
\ \operatorname{rank}A_\Omega=4
\}
}.
}
\]

It is not the full 768-dimensional Grassmannian incidence fibre.

The first-jet formula is exact on the transverse locus.

Higher jets are required precisely on the first-jet base locus, but they only
select boundary points of the same graph-closure carrier.

Thus the terminal is

\[
\boxed{
\texttt{AFFINE-GAUGE-RANK-SEAM-RESOLVED-BY-GRASSMANN-GRAPH-CLOSURE}.
}
\]

The smallest remaining dependency is now exactly the queued task

\[
\boxed{
\texttt{EXP-A4D-RESOLVED-AFFINE-PHYSICAL-QUOTIENT}.
}
\]

That task must recompute the two-channel Euler/physical quotient on the
**selected graph-closure tangent geometry**, rather than on the full arbitrary
incidence envelope.
