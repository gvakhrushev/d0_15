# A4D relative A/e comparison primitive: canonical span map, linear relation, and rank-stratified extension

**Canonical task:** \`EXP-A4D-RELATIVE-AE-COMPARISON-PRIMITIVE\`  
**Audited baseline:** \`3b11811ca8d555a0336b45e2dabbbffb0f306146\`  
**Research PR:** #123  
**Terminal:** \`RELATIVE-AE-SPAN-MAP-CONSTRUCTED\`  
**Status:** positive theorem-ready deep-research construction; no Lean source and no finite graded E dressing.

## 0. Result in one statement

PR #120 showed that the remaining diagonal/source mechanism needs only the
action of a relative A/e comparison on the **actual source-fibre shift
increments**

\[
\Delta^b_r(y),
\]

not a full endomorphism of every vector in \(V_y\).

The present task constructs that minimum object globally.

Let

\[
E_{\rm lab}:=\mathbb R^{\mathrm{Role}}
\]

be a second copy of the Role-indexed vector space used only as the
**coefficient space of labelled edge generators**.  Local Lorentz frames act
on the fibre \(V_y\); they do not act on the edge-label coefficient slot.

Write \(\varepsilon_r\) for the standard Role basis of \(E_{\rm lab}\), and
give \(E_{\rm lab}\) its canonical counting product

\[
\langle c,d\rangle_{\rm lab}
=
\sum_{r:\mathrm{Role}}c_rd_r.
\tag{0.1}
\]

At every site \(y\), define two labelled synthesis maps

\[
\boxed{
\mathcal B_y:E_{\rm lab}\to V_y,
\qquad
\mathcal B_y\varepsilon_r=\Delta^b_r(y),
}
\tag{0.2}
\]

\[
\boxed{
\mathcal S_y:E_{\rm lab}\to V_y,
\qquad
\mathcal S_y\varepsilon_r=\Delta^v_r(y).
}
\tag{0.3}
\]

Set

\[
K_y:=\ker\mathcal B_y,
\qquad
H_y:=K_y^{\perp_{\rm lab}},
\qquad
U_y:=\operatorname{im}\mathcal B_y.
\tag{0.4}
\]

Because \(E_{\rm lab}\) is finite-dimensional Euclidean,

\[
E_{\rm lab}=K_y\oplus H_y,
\]

and the restriction

\[
\mathcal B_y|_{H_y}:H_y\to U_y
\]

is an isomorphism.  Let

\[
\sigma_y:U_y\to H_y
\]

be its inverse.

Then define the canonical relative A/e comparison only on the subspace that
PR #120 actually needs:

\[
\boxed{
J_y^{\rm can}
:=
\mathcal S_y\circ\sigma_y
:
U_y\to V_y.
}
\tag{0.5}
\]

No raw-solder inverse, affine-passport inverse, observer metric, basepoint,
path choice, or full-\(V_y\) extension is used.

For every Role generator,

\[
\boxed{
R_r^{A/e}(y)
:=
\Delta^v_r(y)
-
J_y^{\rm can}\Delta^b_r(y)
=
\mathcal S_y
\bigl(P_{K_y}\varepsilon_r\bigr),
}
\tag{0.6}
\]

where \(P_{K_y}\) is the counting-orthogonal projection in the labelled
coefficient space.

Thus the geometry decomposes canonically into:

- the part of the solder increment correlated with the labelled affine-shift
  span;
- the residual carried by coefficient relations invisible to the affine
  increments.

The associated canonical linear relation is

\[
\boxed{
\mathscr R_y
=
\operatorname{im}
\begin{pmatrix}
\mathcal B_y\\
\mathcal S_y
\end{pmatrix}
\subset V_y\oplus V_y.
}
\tag{0.7}
\]

Its vertical part is

\[
\boxed{
M_y
=
\{w:(0,w)\in\mathscr R_y\}
=
\mathcal S_y(K_y).
}
\tag{0.8}
\]

Every fibre of the relation has the exact form

\[
\boxed{
(\mathscr R_y)_u
=
J_y^{\rm can}(u)+M_y.
}
\tag{0.9}
\]

Therefore the strict span calibration

\[
J_y^{\rm span}(\Delta^b_r)=\Delta^v_r
\]

exists iff

\[
\boxed{
\ker\mathcal B_y\subseteq\ker\mathcal S_y
}
\tag{0.10}
\]

iff

\[
M_y=0.
\]

When this holds, the relation is the graph of one unique map on \(U_y\), and

\[
J_y^{\rm can}=J_y^{\rm span}.
\]

When it fails, there is no map that sends every labelled generator exactly to
its solder increment.  The failure is not discarded: it is exactly the
relative defect (0.6).

This gives a global pointwise comparison on every rank stratum, including:

- singular raw solder;
- singular regular-passport reconstruction;
- zero shift-increment rank;
- arbitrary rank drops.

Under a pure-linear frame \(g_y\),

\[
\mathcal B'_y=g_y\mathcal B_y,
\qquad
\mathcal S'_y=g_y\mathcal S_y.
\]

Hence

\[
K'_y=K_y,
\qquad
H'_y=H_y,
\]

and

\[
\sigma'_y(g_yu)=\sigma_y(u).
\]

Therefore

\[
\boxed{
J_y^{{\rm can}\prime}(g_yu)
=
g_yJ_y^{\rm can}(u)
}
\tag{0.11}
\]

for every \(u\in U_y\), while

\[
\boxed{
R_r^{A/e\,\prime}=g_yR_r^{A/e}.
}
\tag{0.12}
\]

On the exact translation-gauge chart,

\[
\mathcal S_y=\eta\mathcal B_y.
\]

Thus

\[
K_y\subseteq\ker\mathcal S_y,
\qquad
M_y=0,
\]

and

\[
\boxed{
J_y^{\rm can}
=
\eta|_{U_y}.
}
\tag{0.13}
\]

After the rational boost this becomes the required conjugated partial map

\[
g_y\eta g_y^{-1}|_{g_yU_y},
\]

without ever declaring fixed numerical \(\eta\) to be a covariant
endomorphism.

The PR #120 finite seed is therefore now unconditional at the required
arguments:

\[
\boxed{
a_r(y)
=
-\bar b_r(y)
-
J_y^{\rm can}\Delta^b_r(y).
}
\tag{0.14}
\]

The full-endomorphism interface was larger than necessary.

The correct finite primitive is the **rank-stratified partial span map
\(J^{\rm can}:U_y\to V_y\)** together with its canonical relation
\(\mathscr R_y\) and vertical defect \(M_y\).

The strongest terminal is therefore positive:

\[
\boxed{
\texttt{RELATIVE-AE-SPAN-MAP-CONSTRUCTED}.
}
\tag{0.15}
\]

The construction is pointwise global but naturally rank-stratified.
A globally continuous full endomorphism across rank jumps is neither supplied
nor needed.

---

## 1. Frozen PR #120 interface

For \(x=y-r\), PR #120 defines

\[
\bar b_r(y)
=
L_{x,r}^{-1}b_{x,r},
\]

\[
\bar v_r(y)
=
L_{x,r}^{-1}v_r(e,x),
\]

\[
\Delta^b_r(y)
=
b_{y,r}-\bar b_r(y),
\tag{1.1}
\]

\[
\Delta^v_r(y)
=
v_r(e,y)-\bar v_r(y).
\tag{1.2}
\]

Both increments lie in the source fibre \(V_y\).

Under a pure-linear frame,

\[
(\Delta^b_r)'=g_y\Delta^b_r,
\qquad
(\Delta^v_r)'=g_y\Delta^v_r.
\tag{1.3}
\]

PR #120 only evaluates the missing comparison on

\[
\Delta^b_r.
\]

Specifically,

\[
a_r
=
-\bar b_r-\mathfrak J_y\Delta^b_r.
\tag{1.4}
\]

No downstream formula requires a value of \(\mathfrak J_y\) on a vector
outside

\[
U_y
=
\operatorname{span}\{\Delta^b_r\}_r.
\tag{1.5}
\]

Therefore a full endomorphism

\[
V_y\to V_y
\]

is strictly unnecessary.

This observation is the key simplification of the present task.

---

## 2. Label coefficient space is distinct from the fibre frame

Use

\[
E_{\rm lab}
=
\mathbb R^{\mathrm{Role}}
\]

as the coefficient space of the four labelled generators.

Although \(E_{\rm lab}\) has the same underlying coordinate cardinality as
\(V_y\), its transformation role is different.

A local Lorentz frame acts on

\[
V_y.
\]

It does not mix the archive edge label \(r\) in

\[
\Delta^b_r,
\qquad
\Delta^v_r.
\]

Thus the coefficient vector

\[
c=(c_A,c_B,c_C,c_D)
\]

is fixed by a local frame.

This makes the counting product

\[
\langle c,d\rangle_{\rm lab}
=
\sum_r c_rd_r
\tag{2.1}
\]

legitimate for resolving linear relations among the four labelled
generators.

This is not the Lorentz metric and not an observer metric.

It is the permutation-invariant counting product on the finite label set.

---

## 3. Synthesis maps

Define

\[
\mathcal B_y(c)
=
\sum_r c_r\Delta^b_r(y),
\tag{3.1}
\]

\[
\mathcal S_y(c)
=
\sum_r c_r\Delta^v_r(y).
\tag{3.2}
\]

Equivalently,

\[
\mathcal B_y\varepsilon_r=\Delta^b_r,
\]

\[
\mathcal S_y\varepsilon_r=\Delta^v_r.
\]

Under a pure-linear frame,

\[
\boxed{
\mathcal B'_y
=
g_y\circ\mathcal B_y,
}
\tag{3.3}
\]

\[
\boxed{
\mathcal S'_y
=
g_y\circ\mathcal S_y.
}
\tag{3.4}
\]

Since \(g_y\) is invertible,

\[
\boxed{
\ker\mathcal B'_y
=
\ker\mathcal B_y.
}
\tag{3.5}
\]

Likewise

\[
\ker\mathcal S'_y
=
\ker\mathcal S_y.
\]

Thus every coefficient relation is frame invariant.

---

## 4. Exact span-map well-definedness criterion

Suppose one asks for a linear map

\[
J_y^{\rm span}:U_y\to V_y
\]

such that

\[
J_y^{\rm span}(\Delta^b_r)
=
\Delta^v_r
\tag{4.1}
\]

for all Roles.

For arbitrary coefficients \(c_r\),

\[
\sum_r c_r\Delta^b_r=0
\]

means

\[
c\in\ker\mathcal B_y.
\]

Equation (4.1) is well defined iff every such relation also gives

\[
\sum_r c_r\Delta^v_r=0,
\]

i.e.

\[
c\in\ker\mathcal S_y.
\]

Therefore:

\[
\boxed{
J_y^{\rm span}
\text{ exists}
\iff
\ker\mathcal B_y
\subseteq
\ker\mathcal S_y.
}
\tag{4.2}
\]

If it exists, it is unique on \(U_y\).

This is the exact requested well-definedness criterion.

---

## 5. Canonical generated linear relation

Whether or not (4.2) holds, define

\[
\boxed{
\mathscr R_y
=
\{
(\mathcal B_yc,\mathcal S_yc):c\in E_{\rm lab}
\}
\subset
V_y\oplus V_y.
}
\tag{5.1}
\]

This relation is always defined.

Its domain is

\[
\operatorname{dom}\mathscr R_y
=
U_y.
\tag{5.2}
\]

Its vertical part is

\[
\begin{aligned}
M_y
&=
\{w:(0,w)\in\mathscr R_y\}
\\
&=
\{\mathcal S_yk:k\in\ker\mathcal B_y\}.
\end{aligned}
\]

Hence

\[
\boxed{
M_y
=
\mathcal S_y(K_y).
}
\tag{5.3}
\]

The relation is the graph of a function iff

\[
M_y=0.
\]

Thus

\[
\boxed{
\mathscr R_y
\text{ is a graph}
\iff
\ker\mathcal B_y\subseteq\ker\mathcal S_y.
}
\tag{5.4}
\]

This is the relation form of the span criterion.

---

## 6. Canonical quotient comparison exists on every background

Because two coefficients \(c,c'\) with the same affine increment satisfy

\[
c-c'\in K_y,
\]

their solder outputs differ by an element of \(M_y\).

Therefore the quotient class is unambiguous:

\[
\boxed{
\bar J_y:
U_y
\to
V_y/M_y,
\qquad
\bar J_y(\mathcal B_yc)
=
[\mathcal S_yc].
}
\tag{6.1}
\]

This map is globally well defined.

It needs no rank assumption.

It is exactly the functional content of the linear relation.

However the quotient map alone is not yet enough for PR #120, because the
finite diagonal seed lives in the actual vector fibre \(V_y\), not only in a
quotient.

The next section supplies the needed vector representative without using an
observer.

---

## 7. Canonical coefficient-orthogonal representative

Set

\[
K_y=\ker\mathcal B_y.
\]

Using the counting product (2.1), define

\[
H_y=K_y^\perp.
\]

Finite-dimensional orthogonal decomposition gives

\[
\boxed{
E_{\rm lab}
=
K_y\oplus H_y.
}
\tag{7.1}
\]

The restriction

\[
\mathcal B_y|_{H_y}:H_y\to U_y
\]

is injective because

\[
H_y\cap K_y=0.
\]

It is surjective because if

\[
c=k+h
\]

with \(k\in K_y,\ h\in H_y\), then

\[
\mathcal B_yc
=
\mathcal B_yh.
\]

Therefore

\[
\boxed{
\mathcal B_y|_{H_y}
:
H_y\xrightarrow{\sim}U_y.
}
\tag{7.2}
\]

Let

\[
\sigma_y
=
(\mathcal B_y|_{H_y})^{-1}.
\tag{7.3}
\]

This is the unique coefficient representative of minimum counting norm for a
given affine increment.

---

## 8. Global rank-stratified partial comparison

Define

\[
\boxed{
J_y^{\rm can}
=
\mathcal S_y\circ\sigma_y
:
U_y\to V_y.
}
\tag{8.1}
\]

This exists for every rank of \(\mathcal B_y\).

It is a partial map only on the span \(U_y\).

That is sufficient for PR #120.

No value outside \(U_y\) is required.

For every labelled generator, decompose

\[
\varepsilon_r
=
P_{K_y}\varepsilon_r
+
P_{H_y}\varepsilon_r.
\]

Since

\[
\sigma_y(\Delta^b_r)
=
P_{H_y}\varepsilon_r,
\]

one obtains

\[
\boxed{
J_y^{\rm can}\Delta^b_r
=
\mathcal S_y(P_{H_y}\varepsilon_r).
}
\tag{8.2}
\]

The residual is therefore

\[
\boxed{
R_r^{A/e}
=
\mathcal S_y(P_{K_y}\varepsilon_r).
}
\tag{8.3}
\]

This is the exact canonical decomposition of each solder increment.

---

## 9. Relation fibre decomposition

Let

\[
u\in U_y.
\]

Every coefficient producing \(u\) is of the form

\[
\sigma_y(u)+k,
\qquad
k\in K_y.
\]

Therefore every corresponding solder output is

\[
J_y^{\rm can}(u)+\mathcal S_yk.
\]

Hence

\[
\boxed{
(\mathscr R_y)_u
=
J_y^{\rm can}(u)+M_y.
}
\tag{9.1}
\]

Equivalently,

\[
\boxed{
\mathscr R_y
=
\{
(u,J_y^{\rm can}(u)+m):
u\in U_y,\ m\in M_y
\}.
}
\tag{9.2}
\]

Thus \(J^{\rm can}\) is not an arbitrary selection from the relation.

It is the representative selected by the canonical orthogonal splitting of
the **label coefficient relations**.

No fibre metric has entered.

---

## 10. Recovery of the strict span map

If

\[
\ker\mathcal B_y
\subseteq
\ker\mathcal S_y,
\]

then

\[
M_y=0.
\]

Equation (9.1) becomes

\[
(\mathscr R_y)_u
=
\{J_y^{\rm can}(u)\}.
\]

Therefore

\[
J_y^{\rm can}
\]

is exactly the unique map satisfying

\[
J_y^{\rm can}(\Delta^b_r)
=
\Delta^v_r.
\]

Conversely, if this equality holds for every generator, then for any
\(k\in\ker\mathcal B_y\),

\[
\mathcal S_yk
=
J_y^{\rm can}\mathcal B_yk
=
0.
\]

Thus the graph criterion is exact in both directions.

---

## 11. Pure-linear covariance of the canonical map

Under a local frame,

\[
\mathcal B'_y=g_y\mathcal B_y.
\]

Since \(g_y\) is invertible,

\[
K'_y=K_y.
\]

The counting product is on the unchanged coefficient space, so

\[
H'_y=H_y.
\]

For \(u\in U_y\),

\[
\mathcal B'_y\sigma_y(u)
=
g_y\mathcal B_y\sigma_y(u)
=
g_yu.
\]

By uniqueness of the \(H_y\) representative,

\[
\boxed{
\sigma'_y(g_yu)
=
\sigma_y(u).
}
\tag{11.1}
\]

Then

\[
\begin{aligned}
J_y^{{\rm can}\prime}(g_yu)
&=
\mathcal S'_y\sigma'_y(g_yu)
\\
&=
g_y\mathcal S_y\sigma_y(u)
\\
&=
g_yJ_y^{\rm can}(u).
\end{aligned}
\]

Therefore

\[
\boxed{
J_y^{{\rm can}\prime}
=
g_yJ_y^{\rm can}g_y^{-1}
}
\tag{11.2}
\]

as a map

\[
g_yU_y\to V_y.
\]

This is the correct partial-map version of the requested covariance law.

---

## 12. Covariance of the relation and vertical defect

The generated relation obeys

\[
\boxed{
\mathscr R'_y
=
(g_y\oplus g_y)\mathscr R_y.
}
\tag{12.1}
\]

The vertical subspace transforms as

\[
\boxed{
M'_y
=
g_yM_y.
}
\tag{12.2}
\]

For the generator residual,

\[
\begin{aligned}
R_r^{{A/e}\prime}
&=
\Delta^{v\prime}_r
-
J_y^{{\rm can}\prime}\Delta^{b\prime}_r
\\
&=
g_yR_r^{A/e}.
\end{aligned}
\]

Hence

\[
\boxed{
R_r^{{A/e}\prime}
=
g_yR_r^{A/e}.
}
\tag{12.3}
\]

The comparison and its failure are both covariant.

---

## 13. Exact translation-gauge calibration

On the literal exact translation-gauge chart,

\[
L=I,
\qquad
b=e=d_f\phi.
\]

PR #120 gives

\[
\Delta^v_r
=
\eta\Delta^b_r.
\]

Therefore

\[
\boxed{
\mathcal S_y
=
\eta\mathcal B_y.
}
\tag{13.1}
\]

For every

\[
k\in K_y,
\]

\[
\mathcal S_yk
=
\eta\mathcal B_yk
=
0.
\]

Thus

\[
M_y=0.
\]

The relation is a graph and

\[
\boxed{
J_y^{\rm can}(u)
=
\eta u
\quad
(u\in U_y).
}
\tag{13.2}
\]

In particular,

\[
\boxed{
J_y^{\rm can}\Delta^b_r
=
\Delta^v_r.
}
\tag{13.3}
\]

Therefore the exact translation-gauge calibration is satisfied on every
rank stratum.

---

## 14. Translation-gauge orbit under a frame

After a pure-linear frame \(g_y\),

\[
U'_y=g_yU_y.
\]

Equation (11.2) gives

\[
J_y^{{\rm can}\prime}
=
g_y
(\eta|_{U_y})
g_y^{-1}.
\tag{14.1}
\]

Thus the numerical chart matrix \(\eta\) is not held fixed.

It is transported as a partial operator exactly as required.

This resolves the rational-boost obstruction that killed fixed-\(\eta\) in
PR #120.

---

## 15. Exact rational A/B boost firewall

Use

\[
g=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

Its inverse is

\[
g^{-1}
=
\begin{pmatrix}
5/3&-4/3&0&0\\
-4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

Exact arithmetic gives

\[
g^T\eta g=\eta.
\]

The conjugated chart comparison is

\[
\boxed{
g\eta g^{-1}
=
\begin{pmatrix}
41/9&-40/9&0&0\\
40/9&-41/9&0&0\\
0&0&-1&0\\
0&0&0&-1
\end{pmatrix}.
}
\tag{15.1}
\]

For the L=3 gauge witness the active increment line is the \(e_B\) line.

Its transformed generator is

\[
u'=ge_B.
\]

Then

\[
(g\eta g^{-1})u'
=
g\eta e_B
=
-u'.
\]

Thus the partial map transports exactly.

No fixed vector-endomorphism \(\eta\) is asserted.

---

## 16. L=3 exact translation-gauge hostile control

For the frozen cycle

\[
b_A=(3,3,-6)e_B,
\]

the source-site affine increments are

\[
\Delta^b_A
=
(9,0,-9)e_B.
\tag{16.1}
\]

The solder increments are

\[
\Delta^v_A
=
(-9,0,+9)e_B.
\tag{16.2}
\]

At the two nonzero sites,

\[
U_y=\operatorname{span}\{e_B\},
\]

and

\[
J_y^{\rm can}(e_B)=-e_B.
\]

At the middle site,

\[
U_y=0,
\]

and both increments vanish.

Thus

\[
R_A^{A/e}=0
\]

at every site.

The PR #120 seed becomes exactly

\[
\boxed{
a_A=(15,-3,-12)e_B,
}
\tag{16.3}
\]

so the already-derived sourced mechanism gives

\[
\kappa=0.
\]

The rank drop at the middle site causes no ambiguity.

---

## 17. Flat control

At

\[
A=A_{\rm flat},
\qquad
e=0,
\]

all increments vanish:

\[
\mathcal B_y=0,
\qquad
\mathcal S_y=0.
\]

Hence

\[
K_y=E_{\rm lab},
\qquad
H_y=0,
\qquad
U_y=0.
\]

The unique partial map is

\[
J_y^{\rm can}:0\to V_y.
\]

It is zero.

The relative defect is zero.

Thus PR #120 retains

\[
\delta=0,
\qquad
\kappa=0.
\]

No spurious source is introduced.

---

## 18. Constant pure affine shift

Take

\[
e=0,
\qquad
L=I,
\qquad
b_{x,r}=b_r
\]

site-independently.

Then

\[
\Delta^b_r=0
\]

and

\[
\Delta^v_r=0.
\]

Therefore

\[
\mathcal B_y=\mathcal S_y=0
\]

and the partial comparison is zero.

The PR #120 seed remains

\[
a_r=-b_r.
\]

Its post-source parallel correction gives

\[
\delta_r=0,
\]

hence

\[
\boxed{
\kappa=b_r.
}
\tag{18.1}
\]

The pure affine shift remains visible.

---

## 19. Coframe-only backgrounds: why the relation must be allowed to be vertical

Suppose

\[
b=0
\]

but the raw solder is nonparallel.

Then

\[
\mathcal B_y=0.
\]

Therefore

\[
U_y=0,
\qquad
K_y=E_{\rm lab},
\qquad
H_y=0.
\]

The canonical comparison is the zero map on the zero domain:

\[
J_y^{\rm can}=0.
\tag{19.1}
\]

But

\[
\mathcal S_y
\]

can be nonzero.

The linear relation is purely vertical:

\[
\mathscr R_y
=
\{0\}\oplus\operatorname{im}\mathcal S_y.
\tag{19.2}
\]

The relative defect is

\[
\boxed{
R_r^{A/e}
=
\Delta^v_r.
}
\tag{19.3}
\]

This is exactly the desired behavior.

A rule demanding the relation always be a graph would incorrectly erase the
raw coframe-only sectors.

---

## 20. L=2 Nyquist control

On the flat-connection L=2 Nyquist witness,

\[
b=0.
\]

Thus

\[
\mathcal B_y=0.
\]

The raw solder increment is nonzero; in the owned A-leg control its magnitude
is

\[
4e_A.
\]

Therefore

\[
J_y^{\rm can}=0
\]

and

\[
\boxed{
R_A^{A/e}=4e_A
}
\tag{20.1}
\]

up to the oriented sign at the two sites.

The PR #120 seed remains zero in this coframe-only sector.

Consequently the selected mismatch retains the nonzero raw Nyquist response.

The span primitive does not factor through centered solder.

---

## 21. L=3 off-diagonal corner control

Take flat affine connection and the single raw corner

\[
e_A{}^B(0)=1.
\]

Again

\[
\mathcal B_y=0.
\]

At the affected A edge,

\[
\Delta^v_A\ne0.
\]

Hence

\[
J_y^{\rm can}=0,
\]

while

\[
R_A^{A/e}=\Delta^v_A.
\]

Thus the corner survives as relative A/e defect.

The downstream PR #120 mismatch remains nonzero.

---

## 22. Symmetric duplicate-increment example

A useful generic non-graph control is

\[
\Delta^b_A
=
\Delta^b_B
=
u,
\]

but

\[
\Delta^v_A=v_1,
\qquad
\Delta^v_B=v_2,
\qquad
v_1\ne v_2.
\]

Then

\[
K_y
=
\operatorname{span}\{\varepsilon_A-\varepsilon_B,\ldots\}.
\]

On the active two-label sector,

\[
H_y
=
\operatorname{span}\{\varepsilon_A+\varepsilon_B\}.
\]

The unique minimum-counting representative of \(u\) is

\[
\frac12(\varepsilon_A+\varepsilon_B).
\]

Therefore

\[
\boxed{
J_y^{\rm can}(u)
=
\frac{v_1+v_2}{2}.
}
\tag{22.1}
\]

The residuals are

\[
\boxed{
R_A^{A/e}
=
\frac{v_1-v_2}{2},
}
\tag{22.2}
\]

\[
\boxed{
R_B^{A/e}
=
\frac{v_2-v_1}{2}.
}
\tag{22.3}
\]

This demonstrates three important properties:

1. the primitive exists even when the strict graph criterion fails;
2. it treats duplicate Role generators symmetrically;
3. it records rather than erases the disagreement.

A lexicographic choice of one Role would not have these properties.

---

## 23. Rank invariants and vertical dimension

Define

\[
r_b(y)
=
\operatorname{rank}\mathcal B_y,
\]

and

\[
r_{\rm pair}(y)
=
\operatorname{rank}
\begin{pmatrix}
\mathcal B_y\\
\mathcal S_y
\end{pmatrix}.
\]

Then

\[
\dim U_y=r_b.
\]

The relation dimension is

\[
\dim\mathscr R_y=r_{\rm pair}.
\]

Projection of the relation onto its first factor has kernel \(M_y\).

Therefore rank-nullity gives

\[
\boxed{
\dim M_y
=
r_{\rm pair}(y)-r_b(y).
}
\tag{23.1}
\]

Consequently:

\[
\boxed{
\mathscr R_y
\text{ is a graph}
\iff
r_{\rm pair}=r_b.
}
\tag{23.2}
\]

The pair

\[
(r_b,r_{\rm pair})
\]

is a convenient finite rank-stratum label.

Both ranks are frame invariant.

---

## 24. Rank-stratified smoothness and unavoidable rank-jump singularity

On a fixed-rank stratum, the kernel \(K_y\) has constant dimension.

The counting-orthogonal projector onto \(K_y\) and the inverse

\[
(\mathcal B_y|_{H_y})^{-1}
\]

vary smoothly/algebraically in any local chart where a fixed nonzero minor is
used.

Across rank jumps, a globally continuous operator extension is impossible in
general.

Use the exact one-generator family

\[
\mathcal B_t\varepsilon_A
=
t e_A,
\]

\[
\mathcal S_t\varepsilon_A
=
e_B,
\]

with all other columns zero.

For \(t\ne0\),

\[
K_t
\]

does not contain \(\varepsilon_A\), and

\[
J_t^{\rm can}(t e_A)=e_B.
\]

As an operator on the normalized line,

\[
\boxed{
J_t^{\rm can}(e_A)
=
t^{-1}e_B.
}
\tag{24.1}
\]

Thus its norm diverges as

\[
t\to0.
\]

At \(t=0\),

\[
U_0=0,
\]

the relation is vertical, and

\[
R_A^{A/e}=e_B.
\]

The relation line

\[
\operatorname{span}\{(t e_A,e_B)\}
\]

has the well-defined vertical limit

\[
\operatorname{span}\{(0,e_B)\}.
\]

Therefore:

\[
\boxed{
\text{the linear relation extends naturally across the rank drop, while a continuous graph map does not.}
}
\tag{24.2}
\]

This is why the correct global object is rank-stratified.

---

## 25. No global continuity requirement should be added by hand

The finite archive configuration space allows rank changes.

Nothing in the current owners excludes them.

Demanding a globally continuous full comparison endomorphism would therefore
add a new regularity principle that is contradicted by the exact family in
§24 if one also insists on preserving the vertical coframe defect at the rank
drop.

The pointwise rank-stratified construction is the maximal natural statement
from current data.

---

## 26. Full-endomorphism extension freedom

Suppose

\[
\dim U_y=r.
\]

The downstream PR #120 package only needs \(J_y^{\rm can}\) on \(U_y\).

If one nevertheless asks for

\[
\widetilde J_y:V_y\to V_y
\]

extending \(J_y^{\rm can}\), extensions always exist in finite dimension.

They are nonunique unless

\[
U_y=V_y.
\]

If \(\widetilde J_1,\widetilde J_2\) are two extensions, then

\[
T=\widetilde J_1-\widetilde J_2
\]

satisfies

\[
T|_{U_y}=0.
\]

Therefore \(T\) factors through

\[
V_y/U_y.
\]

The extension freedom is

\[
\boxed{
\operatorname{Hom}(V_y/U_y,V_y).
}
\tag{26.1}
\]

For \(\dim V_y=4\),

\[
\boxed{
\dim
\operatorname{Hom}(V_y/U_y,V_y)
=
4(4-r).
}
\tag{26.2}
\]

Thus a full endomorphism is unique only at rank four.

The nonuniqueness firewall is exact.

---

## 27. Why that extension freedom is harmless

Every actual affine increment lies in

\[
U_y.
\]

Therefore all full extensions satisfy

\[
\widetilde J_y\Delta^b_r
=
J_y^{\rm can}\Delta^b_r.
\]

The finite seed

\[
a_r
=
-\bar b_r
-
J_y^{\rm can}\Delta^b_r
\]

is independent of any full-\(V_y\) extension.

Hence the extension freedom never enters the sourced diagonal transport.

There is no reason to select it.

---

## 28. Observer/generalized-inverse audit

One can choose an observer-dependent complement

\[
V_y
=
U_y
\oplus
U_y^{\perp_{h_n}}
\]

and extend \(J_y^{\rm can}\) by zero on the observer-orthogonal complement.

This gives a full endomorphism.

It depends on \(n\).

Likewise a pseudoinverse that uses \(h_n\) on the fibre gives an
observer-dependent full extension.

Neither is needed.

The present construction already gives the required action on \(U_y\) before
any observer is introduced.

Thus the observer firewall is passed in its strongest form:

\[
\boxed{
\text{observer positivity is not used to manufacture the longitudinal source.}
}
\tag{28.1}
\]

The PR #120 observer remains only in the already-solved post-source
parallel-kernel selection.

---

## 29. Why the coefficient counting product is not an observer substitute

The counting product acts on the coefficient space of the four edge labels.

It does not act on \(V_y\).

Under a local frame, the coefficient space is unchanged.

Under a permutation of Role labels, the counting product is invariant.

Therefore the minimum-coefficient representative in §7 is combinatorial and
Role-symmetric.

It is not a choice of physical timelike observer, spacetime metric, or
constitutive energy.

---

## 30. Quotient interpretation

The coefficient quotient

\[
E_{\rm lab}/K_y
\]

is canonically isomorphic to

\[
U_y
\]

through \(\mathcal B_y\).

The strict solder map \(\mathcal S_y\) descends to this quotient iff

\[
K_y\subseteq\ker\mathcal S_y.
\]

When it does not, the obstruction is exactly

\[
M_y=\mathcal S_y(K_y).
\]

The canonical quotient target construction

\[
\bar J_y:U_y\to V_y/M_y
\]

always exists.

The counting-orthogonal splitting chooses one vector representative of this
quotient comparison in a way that is independent of the fibre frame.

This is the precise relation between the quotient and span formulations.

---

## 31. Degenerate raw-solder locus

PR #120's regular passport used the raw solder map

\[
B_e(x):V_{\rm ref}\to V_x.
\]

The repository proves that \(B_e\) can be singular.

The current construction does not invert \(B_e\).

It uses only:

- the already-defined solder legs \(v_r(e,x)\);
- their source-fibre increments \(\Delta^v_r\);
- the affine-shift increments \(\Delta^b_r\);
- finite linear algebra in the label coefficient space.

Therefore it remains defined even at

\[
\det B_e=0.
\]

An extreme example is a site with zero raw solder matrix.

The solder legs are still well-typed vectors, possibly zero, and
\(\mathcal S_y\) remains a valid finite linear map.

Thus:

\[
\boxed{
\text{the degenerate raw-solder locus is not a singularity of }J^{\rm can}.
}
\tag{31.1}
\]

---

## 32. Singular regular-passport reconstruction locus

The regular passport defines

\[
K=B_e^{-1}C_A
\]

when \(B_e\) is invertible, and reconstructs through

\[
\mathcal L_K(X)
=
X-\eta XK.
\]

The map \(\mathcal L_K\) can be singular.

An explicit exact example is

\[
K=I.
\]

Take a nonzero matrix \(X\) supported only in the A row.

Because the A Lorentz sign is \(+1\),

\[
\eta X=X.
\]

Hence

\[
\boxed{
\mathcal L_I(X)
=
X-\eta X
=
0.
}
\tag{32.1}
\]

So \(\mathcal L_I\) is singular.

This \(K\) occurs algebraically with flat raw solder

\[
B_e=I
\]

and a rolewise affine shift map

\[
C_A=I.
\]

The regular reconstruction is therefore genuinely singular on an allowed
matrix background.

The current span primitive remains defined.

If the rolewise shift map is site-constant with \(L=I\), then

\[
\Delta^b=0,
\qquad
\Delta^v=0,
\]

so

\[
U_y=0
\]

and

\[
J_y^{\rm can}=0.
\]

Thus:

\[
\boxed{
\text{singularity of }\mathcal L_K
\text{ does not propagate to the span primitive.}
}
\tag{32.2}
\]

---

## 33. Compatibility with the regular passport

On the regular translation-chart branch, the passport reconstructs a
representative with

\[
B=I+\eta D,
\qquad
C=D.
\]

The exact gauge relation gives

\[
\mathcal S_y
=
\eta\mathcal B_y.
\]

Therefore the present primitive is

\[
J_y^{\rm can}
=
\eta|_{U_y}.
\]

This is exactly the comparison required by the reconstructed translation
chart.

After a frame change it becomes the conjugated partial operator.

Thus the regular passport and the span primitive agree wherever both are
applicable.

Outside the translation-gauge locus, the regular passport does not by itself
force

\[
\mathcal S=\eta\mathcal B.
\]

The present residual \(R^{A/e}\) measures that failure rather than imposing it.

---

## 34. Relation to the PR #120 finite seed

Replace the oversized full-endomorphism symbol in PR #120 by the partial map:

\[
\boxed{
a_r(y)
=
-\bar b_r(y)
-
J_y^{\rm can}\Delta^b_r(y).
}
\tag{34.1}
\]

This is well typed because

\[
\Delta^b_r(y)\in U_y.
\]

Under a frame,

\[
\bar b'_r=g_y\bar b_r,
\]

and

\[
J_y^{{\rm can}\prime}\Delta^{b\prime}_r
=
g_yJ_y^{\rm can}\Delta^b_r.
\]

Hence

\[
\boxed{
a'_r=g_ya_r.
}
\tag{34.2}
\]

The sourced append/reverse/path laws of PR #120 now apply without a supplied
external comparison endomorphism.

No full extension is needed.

---

## 35. PR #120 controls with the constructed primitive

### Flat

\[
J^{\rm can}=0,
\qquad
a=0.
\]

Hence

\[
\delta=0,
\qquad
\kappa=0.
\]

### Exact translation gauge

\[
J^{\rm can}\Delta^b=\Delta^v.
\]

Hence the exact L=3 diagonal

\[
(15,-3,-12)e_B
\]

is reproduced and

\[
\kappa=0.
\]

### Constant pure shift

\[
\Delta^b=0,
\qquad
J^{\rm can}=0.
\]

The seed is

\[
a=-b.
\]

The already-derived parallel-kernel correction gives

\[
\delta=0,
\qquad
\kappa=b.
\]

### Coframe-only Nyquist/corner

\[
\Delta^b=0.
\]

Thus the comparison contributes nothing and raw solder mismatch remains
visible.

The entire mandatory control package survives.

---

## 36. Curl and harmonic nonselection after this construction

PR #120 already proved:

- a calibrated relative A/e comparison gives a sourced path law;
- \(z_{\rm curl}\) violates that source law on the explicit L=3 corner;
- \(z_{\rm harm}\) lies in the parallel kernel and is uniquely removed by the
  post-source positive selector.

The present construction supplies the previously conditional comparison action

\[
J^{\rm can}\Delta^b_r
\]

globally.

Therefore those rejection results no longer require an externally supplied
full endomorphism.

Nothing in this task reopens the solved path or observer-kernel algebra.

---

## 37. Rank-stratified character is intrinsic, not a new gap

The primitive exists at every point.

What changes across strata is:

- \(\dim U_y\);
- \(\dim K_y\);
- \(\dim M_y\);
- whether the generated relation is a graph.

This is finite geometric information, not failure of definition.

The correct package is therefore:

\[
\boxed{
\left(
U_y,\,
J_y^{\rm can},\,
M_y,\,
R_r^{A/e},\,
\mathscr R_y
\right).
}
\tag{37.1}
\]

A fixed-rank full endomorphism is not the invariant object.

---

## 38. Orbitwise extension and stabilizers

No orbit representative is needed.

The formula is evaluated directly from

\[
(\mathcal B_y,\mathcal S_y).
\]

If a frame \(g_y\) stabilizes the background pair, then

\[
g_y\mathcal B_y=\mathcal B_y,
\qquad
g_y\mathcal S_y=\mathcal S_y.
\]

The covariance theorem gives

\[
g_yJ_y^{\rm can}(u)
=
J_y^{\rm can}(g_yu)
\]

on \(U_y\).

Thus the partial primitive is automatically stabilizer compatible.

By contrast, an arbitrary full-\(V_y\) extension would still have to choose a
stabilizer-compatible action on \(V_y/U_y\).

This is another reason not to extend it.

---

## 39. Longitudinal necessity is retained

The construction uses the actual one-edge longitudinal increments

\[
\Delta^b_r
\]

and

\[
\Delta^v_r.
\]

It does not factor through:

- affine square curvature;
- affine open torsion alone;
- solder curl alone;
- endpoint holonomy alone.

Thus PR #120's longitudinal necessity result remains literal.

The primitive compares exactly the data which distinguish the L=3 exact gauge
from an independent affine shift.

---

## 40. Exact finite checker

A standalone exact-rational checker passed **63/63 assertions**.

It checks:

1. rational A/B boost right inverse;
2. left inverse;
3. exact Lorentz relation;
4–7. exact entries of \(g\eta g^{-1}\);
8–16. the three L=3 gauge rank strata
   \(\Delta^b=(9,0,-9)e_B\), including graph rank equality and zero residual;
17–19. zero/flat/pure-shift relation and zero comparison;
20–23. vertical L=2 Nyquist relation and retained residual;
24–25. vertical L=3 corner relation and retained residual;
26–32. duplicate affine increments with unequal solder increments, including
   the canonical average and opposite residuals;
33–37. arbitrary rational-frame covariance of the coefficient kernel,
   canonical comparison, residual, affine rank and pair rank;
38 onward. exact graph criterion on a rank-two example;
full-extension nonuniqueness;
four rational points on the rank-drop family;
the vertical \(t=0\) limit;
the singular \(\mathcal L_K\) example \(K=I\);
an actual regular-passport matrix realization \(B_e=I,C_A=I\);
the degenerate raw-solder matrix;
and four independent checks of
\[
\dim M
=
\operatorname{rank}
\binom{\mathcal B}{\mathcal S}
-
\operatorname{rank}\mathcal B.
\]

All arithmetic is exact rational/symbolic arithmetic.

No floating tolerance is used.

---

## 41. Theorem-ready handoff

### Theorem A — synthesis-map covariance

Define

\[
\mathcal B_y\varepsilon_r=\Delta^b_r,
\qquad
\mathcal S_y\varepsilon_r=\Delta^v_r.
\]

Then under a pure-linear frame,

\[
\mathcal B'_y=g_y\mathcal B_y,
\qquad
\mathcal S'_y=g_y\mathcal S_y.
\]

Hence

\[
\ker\mathcal B'_y=\ker\mathcal B_y.
\]

### Theorem B — strict span-map criterion

A map

\[
J^{\rm span}:U_y\to V_y
\]

with

\[
J^{\rm span}\Delta^b_r=\Delta^v_r
\]

for every Role exists iff

\[
\ker\mathcal B_y\subseteq\ker\mathcal S_y.
\]

If it exists, it is unique.

### Theorem C — canonical linear relation

The subspace

\[
\mathscr R_y
=
\operatorname{im}(\mathcal B_y,\mathcal S_y)
\]

has domain \(U_y\) and vertical part

\[
M_y=\mathcal S_y(\ker\mathcal B_y).
\]

It is a graph iff the strict span-map criterion holds.

### Theorem D — canonical quotient comparison

For every background,

\[
\bar J_y(\mathcal B_yc)
=
[\mathcal S_yc]
\in V_y/M_y
\]

is well defined.

### Theorem E — coefficient-orthogonal span primitive

Let

\[
H_y=(\ker\mathcal B_y)^\perp
\]

in the canonical label counting product.

Then

\[
\mathcal B_y|_{H_y}:H_y\to U_y
\]

is an isomorphism.

Defining

\[
J_y^{\rm can}
=
\mathcal S_y(\mathcal B_y|_{H_y})^{-1}
\]

gives a canonical partial comparison on every rank stratum.

### Theorem F — canonical relative defect

For each Role,

\[
R_r^{A/e}
=
\Delta^v_r-J_y^{\rm can}\Delta^b_r
=
\mathcal S_yP_{\ker\mathcal B_y}\varepsilon_r.
\]

### Theorem G — relation fibre decomposition

For every \(u\in U_y\),

\[
(\mathscr R_y)_u
=
J_y^{\rm can}(u)+M_y.
\]

### Theorem H — partial-map covariance

For every \(u\in U_y\),

\[
J_y^{{\rm can}\prime}(g_yu)
=
g_yJ_y^{\rm can}(u).
\]

Also

\[
R_r^{{A/e}\prime}=g_yR_r^{A/e}.
\]

### Theorem I — exact translation-gauge calibration

On the exact translation-gauge chart,

\[
\mathcal S_y=\eta\mathcal B_y,
\]

hence

\[
M_y=0,
\]

and

\[
J_y^{\rm can}
=
\eta|_{U_y}.
\]

Thus

\[
J_y^{\rm can}\Delta^b_r=\Delta^v_r.
\]

### Theorem J — rank formula

\[
\dim M_y
=
\operatorname{rank}
\binom{\mathcal B_y}{\mathcal S_y}
-
\operatorname{rank}\mathcal B_y.
\]

### Theorem K — full-extension freedom

If \(\dim U_y=r\), full endomorphism extensions of \(J_y^{\rm can}\) differ by

\[
\operatorname{Hom}(V_y/U_y,V_y),
\]

of dimension

\[
4(4-r).
\]

This freedom is irrelevant to PR #120 because only
\(J_y^{\rm can}\Delta^b_r\) is used.

### Theorem L — degenerate-solder robustness

The partial primitive uses no inverse of the raw solder map \(B_e\).

It is defined on the full singular raw-solder locus.

### Theorem M — singular-passport robustness

The regular reconstruction operator is singular at \(K=I\), but the span
primitive remains defined.

### Theorem N — rank-jump boundary

The family

\[
\mathcal B_t\varepsilon_A=t e_A,
\qquad
\mathcal S_t\varepsilon_A=e_B
\]

has a continuous relation limit but no continuous graph-map limit.

Therefore the global primitive is naturally rank-stratified.

### Theorem O — PR #120 seed closure

The finite seed

\[
a_r
=
-\bar b_r
-
J_y^{\rm can}\Delta^b_r
\]

is globally defined and pure-linear covariant on every background.

It reproduces all flat, pure-gauge, pure-shift, Nyquist and corner controls
required by PR #120.

---

## 42. Why the terminal is positive

The previous terminal was

\[
\texttt{DIAGONAL-OVERLAP-REQUIRES-NEW-RELATIVE-AE-DEFECT}.
\]

The present task constructs that defect and the comparison producing it.

The apparent need for a full endomorphism came from an oversized interface.

The actual downstream formula needs the comparison only on

\[
U_y
=
\operatorname{span}\{\Delta^b_r\}.
\]

On this span there is a canonical map on every rank stratum, obtained by:

1. recording all Role-labelled coefficient relations;
2. taking the canonical counting-orthogonal representative modulo
   \(\ker\mathcal B_y\);
3. evaluating the solder synthesis map on that representative.

Generic failure of the strict generator assignment is not an obstruction.

It becomes the covariant vertical relative defect.

Neither singular raw solder nor singular regular-passport reconstruction is a
singularity of this construction.

Therefore the strongest honest terminal is

\[
\boxed{
\texttt{RELATIVE-AE-SPAN-MAP-CONSTRUCTED}.
}
\]

The construction is not promoted to a globally continuous full endomorphism.

It does not need to be.

---

## 43. Exactly one recommended next step

Lean-own the rank-stratified partial comparison package in one worker module,
for example

\[
\texttt{D0.Geometry.A4DRelativeAEComparisonSpan}.
\]

Formalize:

- the labelled synthesis maps;
- the kernel-inclusion graph criterion;
- the generated linear relation and vertical subspace;
- the counting-orthogonal restriction isomorphism;
- \(J^{\rm can}:U\to V\);
- the residual formula;
- pure-linear covariance;
- exact translation-gauge specialization;
- full-extension nonuniqueness;
- the rank-jump counterexample.

After this research PR is merged and the rank-stratified span package is formally adopted/Lean-owned, the relative-A/e comparison gate is no longer the blocker for the finite graded coframe dressing frontier.
