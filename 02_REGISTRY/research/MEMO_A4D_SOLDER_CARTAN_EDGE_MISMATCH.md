# A4D solder–Cartan edge mismatch: transported reference leg and the exact covariance boundary

**Canonical task:** \`EXP-A4D-SOLDER-CARTAN-EDGE-MISMATCH\`  
**Audited baseline:** \`9a4acc11955412a41e93e8c066b8c35c08fd1227\`  
**Research PR:** #112  
**Terminal:** \`SOLDER-CARTAN-MISMATCH-REQUIRES-REFERENCE-LEG-SECTION\`  
**Status:** theorem-ready research classification; no Lean source and no finite E dressing.

## 0. Result in one statement

The row/vector ambiguity can be removed with already-owned structure, but the edge comparison still does not close from \((A,e)\) alone.

For one positive Role edge
\[
y=x+r,
\qquad
A_{x,r}=(L_{x,r},b_{x,r}):V_y\to_{\rm aff}V_x,
\]
the repository already provides a target-fibre solder vector
\[
v_r(e,x)
=
\operatorname{solderLegVector}(e,x,r)
\in V_x.
\]

If one supplies a source reference-leg section
\[
q_r(y)\in V_y,
\]
then the transported-reference construction has the exact geometric form
\[
\boxed{
\kappa_q(A,e;x,r)
=
A_{x,r}\bigl(q_r(y)\bigr)-v_r(e,x)
=
b_{x,r}+L_{x,r}q_r(y)-v_r(e,x).
}
\tag{0.1}
\]

This is literally a target-fibre vector. No additional \(\iota\), metric raise/lower, endpoint averaging, or matter dressing is needed **after** \`solderLegVector\`.

Under the owned right-Lorentz solder convention, let the row matrix be \(\Lambda_x\) and the corresponding vector frame be
\[
g_x=\Lambda_x^{-1}.
\]
For a pure-linear affine node gauge, if
\[
q'_r(y)=g_yq_r(y),
\qquad
v'_r(x)=g_xv_r(x),
\]
then
\[
\boxed{
\kappa_q(A',e';x,r)=g_x\kappa_q(A,e;x,r).
}
\tag{0.2}
\]

Thus the transported-reference ansatz solves the literal source/target and Lorentz-covariance problem.

What is not owned is the section \(q\).

The four required controls force nontrivial chart data for it:

- flat:
  \[
  q_r^{\rm flat}(y)=e_r;
  \]
- exact translation-gauge orbit \(e=d_f\phi\), where \(L=I\) and \(b=e_r\):
  \[
  q_r^{\rm pg}(x+r)
  =
  v_r(d_f\phi,x)-b_{x,r};
  \tag{0.3}
  \]
- pure affine shift with \(e=0,L=I\): the flat reference gives
  \[
  \kappa_q=b\ne0.
  \]

The natural owned source solder leg
\[
q_r(y)=v_r(e,y)
\]
does **not** satisfy (0.3) on a generic exact translation-gauge orbit. A fixed flat reference \(q=e_r\) also fails there. A second fixed metric conversion cannot repair the failure covariantly.

Therefore current D0 does not construct a function
\[
\kappa_N(A,e;x,r)
\]
from the supplied pair \((A,e)\) alone. It constructs the exact conditional family
\[
\kappa_{N,q}(A,e;x,r)
\]
once a reference-leg section is supplied.

The earliest missing datum is precisely that section, with its transformation law and pure-gauge specialization:

\[
\boxed{\texttt{SOLDER-CARTAN-MISMATCH-REQUIRES-REFERENCE-LEG-SECTION}.}
\]

A full affine action on the solder/reference legs is a later strengthening if one wants covariance under arbitrary affine node gauges, rather than the exact linear-frame covariance plus separately verified translation-gauge normalization established here.

---

## 1. Literal repository type audit

Fix
\[
X=X_N=\operatorname{ArchiveRolePhaseGroup}N,
\qquad
V=\operatorname{RoleSpace}=\operatorname{Role}\to\mathbb R.
\]

### 1.1 Affine Cartan link

The repository type is

\[
\operatorname{AffineCartanConnection}N\,\mathbb R\,V
=
X\to\operatorname{Role}\to\operatorname{AffineCartanMap}\mathbb R V.
\]

For
\[
A_{x,r}=A\,x\,r,
\]
the stored link is a **pull**
\[
V_{x+r}\longrightarrow_{\rm aff}V_x.
\]

It has

\[
(Ax r).{\rm lin}:V_{x+r}\simeq V_x
\]
and
\[
(Ax r).{\rm shift}\in V_x.
\]

Thus
\[
b_{x,r}:=(Ax r).{\rm shift}
\]
is already a target-fibre vector.

The affine application is
\[
A_{x,r}(z)=L_{x,r}z+b_{x,r}.
\tag{1.1}
\]

### 1.2 Raw coframe row

The raw coframe is

\[
e:X\to\operatorname{Role}\to\operatorname{Role}\to\mathbb R.
\]

For fixed \(x,r\),
\[
e_r(x):a\mapsto e(x,r,a)
\]
is used by the repository as a **row/covector datum**.

The full raw solder row is

\[
E_r(e,x)_a
=
\eta_{ra}+e_r{}^a(x),
\tag{1.2}
\]
where \(\eta=\operatorname{roleLorentzMetric}\).

The owned active right-frame law is
\[
E'_r(x)=E_r(x)\Lambda_x.
\tag{1.3}
\]

This is not the vector law used by affine shifts.

### 1.3 Row-to-vector conversion is already owned

The repository defines

\[
v_r(e,x)
:=
\operatorname{solderLegVector}(N,e,x,r)
=
\eta E_r(e,x)^T.
\tag{1.4}
\]

Hence
\[
v_r(e,x)\in V_x.
\]

At flat,
\[
v_r(0,x)=\operatorname{archiveRoleBasis}(r)=:e_r.
\tag{1.5}
\]

Equation (1.4) is the literal row-to-vector conversion. It already contains the Lorentz metric.

Therefore the terminal is **not**
\[
\texttt{SOLDER-CARTAN-MISMATCH-REQUIRES-ROW-VECTOR-COMPARISON-PRIMITIVE}.
\]

No second raise/lower map is required once one works with \(v_r\).

### 1.4 Right frame versus vector frame

For a right Lorentz matrix
\[
\Lambda\eta\Lambda^T=\eta,
\]
the owned vector representative is
\[
g=\Lambda^{-1}.
\tag{1.6}
\]

Indeed
\[
\eta\Lambda^T=g\eta,
\tag{1.7}
\]
so from (1.3)
\[
v'_r
=
\eta(E_r\Lambda)^T
=
\eta\Lambda^TE_r^T
=
g\,v_r.
\tag{1.8}
\]

This is the exact convention needed below.

### 1.5 Affine node gauge

A node gauge is
\[
h_x=(g_x,c_x).
\]

The exact affine-link law is
\[
A'_{x,r}=h_xA_{x,r}h_y^{-1},
\qquad y=x+r.
\tag{1.9}
\]

Its linear part is
\[
L'_{x,r}=g_xL_{x,r}g_y^{-1}.
\tag{1.10}
\]

Its shift is
\[
b'_{x,r}
=
g_xb_{x,r}
+
c_x
-
L'_{x,r}c_y.
\tag{1.11}
\]

For the **pure-linear subgroup** \(c=0\),
\[
b'=g_xb.
\tag{1.12}
\]

The raw solder currently owns (1.3)/(1.8), which is a linear frame action. It does not own the analogue of (1.11).

---

## 2. Transported-reference-leg hypothesis

Let
\[
q_r(y)\in V_y
\]
be a source-fibre reference leg at \(y=x+r\).

Transport it with the already-owned linear Cartan pull:
\[
L_{x,r}q_r(y)\in V_x.
\]

Define
\[
\sigma_q(A,e;x,r)
=
v_r(e,x)-L_{x,r}q_r(y).
\tag{2.1}
\]

Every term in (2.1) is now a target-fibre vector.

The natural mismatch is therefore

\[
\begin{aligned}
\kappa_q(A,e;x,r)
&=
b_{x,r}-\sigma_q(A,e;x,r)
\\
&=
b_{x,r}+L_{x,r}q_r(y)-v_r(e,x)
\\
&=
A_{x,r}\bigl(q_r(y)\bigr)-v_r(e,x).
\end{aligned}
\tag{2.2}
\]

The last line is the cleanest interpretation:

> \(\kappa_q\) is the difference between the affine image of a source reference leg and the actual target solder leg.

This is an exact comparison of two values in \(V_x\).

### 2.1 The proposed \(\iota\) is identity

The task asked whether
\[
\kappa=b-\iota(\sigma_q)
\]
needs a separate conversion.

With (2.1), it does not:
\[
\boxed{\iota=\operatorname{id}_{V_x}.}
\]

The metric conversion has already happened in (1.4).

Trying to apply \(\eta\) once more to \(\sigma_q\) is not “raising the row index”; \(\sigma_q\) is already a vector. That second \(\eta\) is not an intertwiner for the vector Lorentz representation.

---

## 3. Exact linear-frame covariance

Restrict first to the pure-linear subgroup
\[
h_x=(g_x,0).
\]

Let the right solder frame be
\[
\Lambda_x=g_x^{-1}.
\]

Assume the reference section transforms in its source fibre:
\[
q'_r(y)=g_yq_r(y).
\tag{3.1}
\]

Then from (1.10),
\[
L'_{x,r}q'_r(y)
=
g_xL_{x,r}g_y^{-1}g_yq_r(y)
=
g_xL_{x,r}q_r(y).
\tag{3.2}
\]

From (1.8),
\[
v'_r(e',x)=g_xv_r(e,x).
\tag{3.3}
\]

Therefore
\[
\sigma'_q
=
g_x\sigma_q.
\tag{3.4}
\]

Using (1.12),
\[
\boxed{
\kappa'_q
=
g_x\kappa_q.
}
\tag{3.5}
\]

This is exactly the requested target-fibre Lorentz/frame law.

No endpoint averaging was used.

---

## 4. Flat normalization

For the flat affine link
\[
A_{\rm flat}(x,r)=(I,0)
\]
and zero coframe,
\[
v_r(0,x)=e_r.
\]

If the reference section has the flat value
\[
q_r^{\rm flat}(y)=e_r,
\tag{4.1}
\]
then
\[
\kappa_q(A_{\rm flat},0;x,r)
=
0+e_r-e_r
=
0.
\tag{4.2}
\]

Thus flat normalization is a theorem of (2.2) once the flat reference value (4.1) is part of the section.

It is not an extra subtraction inserted into \(\kappa\).

---

## 5. Pure affine-shift visibility

Take
\[
e=0,
\qquad
L=I,
\qquad
b\ne0,
\]
and retain the same flat reference
\[
q=e_r.
\]

Then
\[
v_r(0,x)=e_r,
\]
so
\[
\sigma_q=e_r-e_r=0.
\]

Hence
\[
\boxed{
\kappa_q((I,b),0;x,r)=b\ne0.
}
\tag{5.1}
\]

This is the exact pure-shift control.

It also shows why setting the reference to an expression that absorbs every affine shift would be unacceptable: it would destroy (5.1).

---

## 6. Exact translation-gauge diagonal

The owned translation gauge has trivial linear part. On the flat affine connection,

\[
L_\phi=I
\]
and
\[
b_\phi(x,r)
=
d_f\phi(x,r).
\tag{6.1}
\]

The raw coframe on the joint chart is
\[
e=d_f\phi.
\tag{6.2}
\]

### 6.1 What the solder vector is on this chart

Write the raw row \(e_r(x)\) as a column of the same coordinate numbers only for this calculation. From (1.4),

\[
v_r(d_f\phi,x)
=
e_r+\eta\,e_r(x)^T.
\tag{6.3}
\]

Since the affine shift has coordinate vector
\[
b_\phi=e_r(x),
\]
the flat reference \(q=e_r\) gives

\[
\sigma_{\rm flat}
=
\eta b_\phi.
\tag{6.4}
\]

Therefore

\[
\kappa_{\rm flat}
=
b_\phi-\eta b_\phi.
\tag{6.5}
\]

This is not zero for a generic spacelike component.

The exact pure-gauge diagonal is therefore **not** obtained from the fixed flat reference leg.

### 6.2 Required pure-gauge value of the reference section

Equation (2.2) requires

\[
0
=
b_\phi+q_r(x+r)-v_r(d_f\phi,x)
\]
because \(L=I\).

Thus the reference value must be

\[
\boxed{
q_r^{\rm pg}(x+r)
=
v_r(d_f\phi,x)-b_\phi(x,r).
}
\tag{6.6}
\]

Using (6.3),

\[
q_r^{\rm pg}(x+r)
=
e_r+(\eta-I)b_\phi(x,r).
\tag{6.7}
\]

Then

\[
\boxed{
\kappa_q(A_\phi,d_f\phi;x,r)=0.
}
\tag{6.8}
\]

So exact pure-gauge normalization is compatible with the transported-reference formula.

But (6.6) is not currently supplied by the repository as a reference-leg section.

---

## 7. Why the owned source solder leg is not that section

A first attempt is to avoid introducing new data by setting

\[
q_r(y)=v_r(e,y).
\tag{7.1}
\]

Then
\[
\sigma_q
=
v_r(e,x)-L_{x,r}v_r(e,y)
\]
is precisely a solder nonparallelism.

It has correct target typing and is an important geometric quantity.

It nevertheless fails the exact translation-gauge diagonal.

Take an \(L=3\) one-axis exact field with one internal \(B\) component, generated by a periodic potential whose values along the \(A\) cycle are
\[
\phi^B=(0,1,0).
\]

With the owned forward scale, the \(A\)-edge coframe values are proportional to
\[
(3,-3,0).
\]

At the first edge,
\[
b=3e_B.
\]

But
\[
v_A(x)-v_A(x+A)
=
\eta(3e_B-(-3e_B))
=
-6e_B.
\]

Thus
\[
\kappa
=
3e_B-(-6e_B)
=
9e_B
\ne0.
\]

Therefore

\[
\boxed{q=v(e,\text{source})\text{ is not the required pure-gauge reference section}.}
\tag{7.2}
\]

The missing reference cannot be dismissed as a rename of an already-owned solder leg.

---

## 8. Why a second fixed metric conversion does not repair the problem

One might keep the flat reference \(q=e_r\), observe
\[
\sigma=\eta b
\]
on the pure-gauge chart, and try
\[
\kappa=b-\iota(\sigma)
\]
with a fixed linear \(\iota\).

To obtain \(\kappa=0\) for all \(b\), one needs
\[
\iota\eta=I,
\]
hence
\[
\iota=\eta.
\tag{8.1}
\]

But \(\sigma\) is already a vector. Covariance would require
\[
\eta g=g\eta
\]
for every allowed Lorentz vector frame.

This fails for the exact A/B boost below.

Therefore a second fixed \(\eta\) is not a covariant repair.

This is why the terminal is not a missing row/vector map: the correct row/vector conversion is already (1.4), while the remaining failure is the missing reference section.

---

## 9. Exact rational A/B boost

Use the merged rational A/B Lorentz boost on vectors

\[
g=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\tag{9.1}
\]

Its right-row solder matrix is

\[
\Lambda=g^{-1}
=
\begin{pmatrix}
5/3&-4/3&0&0\\
-4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\tag{9.2}
\]

Exact rational arithmetic gives

\[
g\Lambda=\Lambda g=I,
\]
\[
g\eta g^T=\eta,
\qquad
\Lambda\eta\Lambda^T=\eta,
\]
and
\[
\eta\Lambda^T=g\eta.
\tag{9.3}
\]

Thus the row/vector convention is exact.

### 9.1 Boosted pure-gauge control

Take Role \(r=A\) and a pure-gauge edge shift
\[
b=e_B.
\]

Then

\[
v_A=e_A+\eta e_B=e_A-e_B.
\]

The required reference value from (6.6) is

\[
q_A=e_A-2e_B.
\]

Directly,

\[
v_A-q_A=e_B=b,
\]
so \(\kappa=0\).

Transport all three vector quantities:

\[
b'=gb,
\qquad
v'=gv,
\qquad
q'=gq.
\]

Exact values are

\[
b'=\left(\frac43,\frac53,0,0\right),
\]
\[
v'=\left(\frac13,-\frac13,0,0\right),
\]
\[
q'=(-1,-2,0,0).
\]

Therefore

\[
v'-q'
=
\left(\frac43,\frac53,0,0\right)
=
b',
\]
and again
\[
\kappa'=0.
\tag{9.4}
\]

This is the exact rational target-fibre covariance control.

### 9.2 Why the pure-gauge coordinate formula is not itself a covariant definition of \(q\)

If one takes (6.7) as a formula to be recomputed in the boosted coordinates with the fixed basis \(e_A\), one gets

\[
e_A+(\eta-I)b'
=
\left(1,-\frac{10}{3},0,0\right),
\]
which is **not**
\[
q'=(-1,-2,0,0).
\]

Therefore (6.7) supplies the required value in the translation-gauge chart, but it is not by itself a global frame-covariant definition of the section.

The section must have its own transformation law (3.1).

This is the decisive reference-leg boundary.

---

## 10. Linear frame covariance versus full affine node gauge

The task requires these to be audited separately.

### 10.1 What is constructed

For the pure-linear node gauge
\[
h_x=(g_x,0),
\]
the package
\[
(A,e,q)\mapsto\kappa_q
\]
has the exact homogeneous law (3.5).

This is enough for the requested Lorentz/frame covariance.

### 10.2 What is not currently owned

For a full affine node gauge
\[
h_x=(g_x,c_x),
\]
the affine link shift has the inhomogeneous law (1.11).

The raw solder currently has only the linear rule
\[
v'_x=g_xv_x.
\]

There is no owned translation action
\[
v'_x=g_xv_x+c_x.
\tag{10.1}
\]

Likewise there is no owned full affine transformation of a reference leg.

If one extends \(q\) naturally as an affine point,
\[
q'_y=h_y(q_y)=g_yq_y+c_y,
\]
then
\[
A'_{x,r}(q'_y)
=
h_x(A_{x,r}(q_y))
=
g_xA_{x,r}(q_y)+c_x.
\]

For the difference
\[
A'(q')-v'
\]
to transform homogeneously, the target solder leg would need exactly (10.1).

Hence:

> a **single full-affine covariance theorem** for \(\kappa\) would require a full affine solder/reference action not currently owned.

This does not change the earliest terminal. The present task can—and does—separate:

1. exact Lorentz/linear-frame covariance of \(\kappa_q\);
2. exact pure-translation-gauge normalization on the owned chart.

It does not pretend these two existing actions are already one full affine action on raw \(e\).

---

## 11. Endpoint/reference freedom

The four controls do not select an endpoint average or a half-edge weight.

### 11.1 Source reference versus target reference

The source-reference presentation is
\[
q_r(y)\in V_y,
\qquad
\kappa=b+Lq-v.
\]

Equivalently one can write a target-fibre reference
\[
p_{x,r}:=L_{x,r}q_r(y)\in V_x
\]
and
\[
\kappa=b+p-v.
\tag{11.1}
\]

Thus “source transported by \(L\)” and “target reference” are equivalent once the reference is provided.

The edge controls do not choose one as more physical.

### 11.2 No endpoint averaging is forced

Nothing in flat normalization, pure-gauge normalization, pure-shift visibility, or Lorentz covariance produces coefficients
\[
\frac12,\quad \frac13,\quad \ldots
\]

No endpoint average is introduced in this memo.

Any such weight would be a new selector and belongs downstream, if at all.

### 11.3 Nonuniqueness even after existence

Suppose one valid \(q\) were supplied.

Any covariant correction
\[
z_r(A,e;y)
\]
that vanishes on the flat and exact pure-gauge control sets gives another section
\[
q'_r=q_r+z_r
\]
with the same required controls, while changing generic-background \(\kappa\).

Therefore the four controls do not prove uniqueness of \(q\) or \(\kappa\).

The present terminal is about missing existence/selection of the reference section, not a false uniqueness theorem.

---

## 12. L=2 Nyquist control

The owned raw Nyquist field has on the \(A\)-edge
\[
e_A{}^A=(-2,+2)
\]
around the period-two cycle.

Its centered coframe is zero, but the raw field is nonzero. The owned affine-solder parallel defect is exactly \(4\).

Use flat \(A\) and the flat reference \(q=e_A\).

Because \(A\) is timelike,
\[
\eta e_A=e_A.
\]

At the two sites,
\[
v_A=e_A+e_A{}^A\,e_A
\]
has values
\[
-e_A,\qquad 3e_A.
\]

Therefore
\[
\kappa_q
=
e_A-v_A
\]
has alternating values
\[
2e_A,\qquad -2e_A.
\tag{12.1}
\]

So the transported-reference comparison retains the raw Nyquist mode.

Any proposal that first replaces \(e\) by its centered solder readout would instead see zero and fails this control.

No centered endpoint average is admissible as the definition of the mismatch.

---

## 13. L=3 mixed-corner control

Take a local raw off-diagonal edge datum at the origin
\[
e_A{}^B(0)=a,
\qquad
a\ne0,
\]
with flat affine link and flat reference \(q=e_A\).

Since \(B\) is spacelike,
\[
\eta e_B=-e_B.
\]

Thus
\[
v_A(0)=e_A-ae_B
\]
and
\[
\kappa_q(0,A)=ae_B.
\tag{13.1}
\]

The raw off-diagonal edge datum remains visible at its literal site and Role slot.

This task does **not** derive the downstream \(-a/2\) corner coefficient of the constitutive first jet. That coefficient belongs to finite E dressing/cell assembly and is explicitly outside scope.

The control here is only that the mismatch does not center or quotient away the raw corner datum needed downstream.

---

## 14. Curl and harmonic controls

A generic plaquette-curl coframe and a harmonic cycle coframe need not satisfy
\[
\kappa=0.
\]

They are not gauge conditions for this task.

The mismatch (2.2) is edge local and does not identify paths or quotient periodic cycles. Therefore:

- a nonzero plaquette curl remains available as path-resolved edge data;
- a nonzero harmonic period remains available around the cycle;
- no endpoint quotient is imposed by the definition of \(\kappa_q\).

The reference-leg problem is logically earlier than deciding any finite E response to those transverse directions.

---

## 15. Interaction with the nilpotent affine response

PR #109 supplies the research-theorem-ready translation unit

\[
T_b
=
I+C^\dagger(b)P_0.
\]

Once a typed mismatch exists, this task uses only

\[
\boxed{
T_{\kappa_q}
=
I+C^\dagger(\kappa_q)P_0.
}
\tag{15.1}
\]

No finite E dressing is constructed.

### 15.1 Flat

From (4.2),
\[
\kappa_q=0
\quad\Longrightarrow\quad
T_{\kappa_q}=I.
\]

### 15.2 Exact pure-gauge diagonal

From (6.8),
\[
\kappa_q=0
\quad\Longrightarrow\quad
T_{\kappa_q}=I.
\]

Thus the degree-mixing B response disappears **before** any graded E dressing, exactly as required by the post-PR-109 synthesis.

### 15.3 Pure shift

From (5.1),
\[
\kappa_q=b
\quad\Longrightarrow\quad
T_{\kappa_q}=T_b.
\]

Pure affine translation remains visible.

### 15.4 Lorentz covariance

Creator covariance gives
\[
\rho(g)C^\dagger(\kappa)\rho(g)^{-1}
=
C^\dagger(g\kappa).
\]

The vacuum projector is fixed by the exterior lift, hence

\[
\boxed{
\rho(g)T_\kappa\rho(g)^{-1}
=
T_{g\kappa}.
}
\tag{15.2}
\]

Together with (3.5), the conditional mismatch feeds the nilpotent affine response covariantly.

---

## 16. Commutator firewall

The identity operator commutes with every operator:

\[
\boxed{
[I,T_b]=0.
}
\tag{16.1}
\]

It does not produce \(-T_b\), \(T_b\), or any cancellation of the affine response.

This memo does not use
\[
[H,T_b]
\]
to eliminate degree mixing.

A mixed B/E commutator is downstream and may only be studied after a finite E dressing exists. It plays no role in the present terminal.

---

## 17. Why the terminal is the reference-leg section

The candidate comparison itself is fully typed:

\[
\kappa_q=A(q)-v.
\]

The row-to-vector conversion exists.

The target-fibre Lorentz law exists.

The flat and pure-shift controls exist.

The exact pure-gauge condition reduces to an explicit required value of \(q\).

What is missing is a repository-owned rule that selects the reference section with all these properties.

The following obvious attempts fail:

1. **fixed archive basis**
   \[
   q=e_r:
   \]
   flat and pure-shift pass, generic exact pure gauge fails;

2. **source solder leg**
   \[
   q=v(e,x+r):
   \]
   typed and geometric, but exact pure gauge fails;

3. **fixed second metric conversion**
   \[
   \iota=\eta:
   \]
   can repair the fixed-chart pure-gauge equation but fails Lorentz intertwining because \(\eta g\ne g\eta\) for the rational A/B boost;

4. **recompute the chart formula \(q=e_r+(\eta-I)b\) after every frame change:**
   it is not the vector transform of the original \(q\).

Thus no already-owned datum supplies the section.

The exact terminal is

\[
\boxed{
\texttt{SOLDER-CARTAN-MISMATCH-REQUIRES-REFERENCE-LEG-SECTION}.
}
\]

### 17.1 Scope of the terminal

This terminal does not claim that every future matter construction must expose a separately named \(q\).

It says that **within the transported-reference-leg construction demanded by the current edge geometry**, an additional reference section—or an equivalent datum carrying exactly the same source/target and transformation information—is necessary.

If a future construction instead supplies a full affine solder action, its translational origin/reference field may absorb this datum. That would be an equivalent geometric resolution, not evidence that the current \((A,e)\) already selects \(\kappa\).

---

## 18. Full affine solder action as the next boundary after \(q\)

A natural stronger package would treat the reference and solder legs as affine points:

\[
q'_y=h_y(q_y),
\qquad
v'_x=h_x(v_x).
\tag{18.1}
\]

Then the affine gauge identity gives automatically

\[
A'_{x,r}(q'_y)=h_x(A_{x,r}(q_y)),
\]
so
\[
\kappa'_q
=
g_x\kappa_q.
\tag{18.2}
\]

This is elegant, but (18.1) is **not** an owned transformation law for raw solder/coframe data.

Current D0 owns only the linear right-frame action.

Therefore a full-affine solder action is a legitimate later primitive if the project wants one unified affine covariance law. It is not required to state the present linear-frame result and exact pure-gauge chart separately.

---

## 19. Exact hostile controls

A standalone exact-rational checker for this memo passed **24/24 assertions**.

It checked:

1. \(g\Lambda=I\);
2. \(\Lambda g=I\);
3. \(g\) is Lorentz;
4. \(\Lambda\) is Lorentz;
5. \(\eta\Lambda^T=g\eta\);
6. the pure-gauge solder vector for \(b=e_B\);
7. fixed flat \(q\) gives \(\sigma=\eta b\);
8. fixed flat \(q\) fails generic pure-gauge cancellation;
9. \(\eta^2=I\);
10. \(\eta\) does not commute with the A/B boost;
11. the required chart value \(q=e_A-2e_B\);
12. conditional \(q\) gives \(\sigma=b\);
13. conditional \(q\) gives \(\kappa=0\);
14. transformed \(q\) preserves \(\sigma'=b'\);
15. transformed \(q\) preserves \(\kappa'=0\);
16. recomputing the chart coordinate formula is not boost covariant;
17. flat \(\sigma=0\);
18. pure affine shift gives \(\kappa=b\ne0\);
19. the source solder choice \(q=v_y\) fails an exact \(L=3\) gauge witness;
20. a full affine node translation produces an unowned inhomogeneous defect if solder/reference legs have only linear laws;
21. the \(L=2\) centered perturbation is zero;
22. the local solder vectors retain the \(L=2\) Nyquist mode;
23. the \(L=3\) off-diagonal raw corner remains visible in \(v\) and \(\kappa\);
24. \([I,T_b]=0\).

All entries were exact rational \`Fraction\` arithmetic. No floating tolerance was used.

---

## 20. Theorem-ready handoff

The following are theorem-ready research statements. They are not claimed as existing Lean owners in this EXP.

### Theorem A — row/vector typing

For a right Lorentz frame \(\Lambda\) and vector frame
\[
g=\Lambda^{-1},
\]
the owned solder vector obeys
\[
v_r(\operatorname{rawFullSolderFrameAction}(e,\Lambda),x)
=
g_xv_r(e,x).
\]

The proof is
\[
v'=\eta(E\Lambda)^T=\eta\Lambda^TE^T=g\eta E^T.
\]

### Theorem B — transported-reference mismatch is well typed

For a supplied section
\[
q_r(y)\in V_y,
\]
define
\[
\kappa_q(A,e;x,r)=A_{x,r}(q_r(x+r))-v_r(e,x).
\]

Then
\[
\kappa_q(A,e;x,r)\in V_x.
\]

No additional row/vector conversion is required.

### Theorem C — exact linear-frame covariance

For a pure-linear node gauge \(h_x=(g_x,0)\), right solder frame
\[
\Lambda_x=g_x^{-1},
\]
and
\[
q'_r(y)=g_yq_r(y),
\]
one has
\[
\kappa_{q'}(A^h,e^\Lambda;x,r)
=
g_x\kappa_q(A,e;x,r).
\]

### Theorem D — flat control

If
\[
A=A_{\rm flat},
\quad
e=0,
\quad
q_r=e_r,
\]
then
\[
\kappa_q=0.
\]

### Theorem E — pure-shift control

If
\[
A=(I,b),
\quad
e=0,
\quad
q_r=e_r,
\]
then
\[
\kappa_q=b.
\]

### Theorem F — pure-gauge reference condition

On the exact translation-gauge orbit,
\[
L=I,
\qquad
b=d_f\phi,
\qquad
e=d_f\phi,
\]
one has
\[
\kappa_q=0
\]
if and only if
\[
q_r(x+r)=v_r(d_f\phi,x)-b_{x,r}.
\]

In coordinates this is
\[
q_r=e_r+(\eta-I)b.
\]

### Theorem G — fixed flat reference fails generic pure gauge

For \(q=e_r\),
\[
\kappa=b-\eta b
\]
on the translation-gauge chart. There exist spacelike \(b\) for which this is nonzero.

### Theorem H — source solder is not the required reference

There exists an exact periodic \(L=3\) potential for which
\[
q_r(x+r)=v_r(e,x+r)
\]
gives
\[
\kappa_q\ne0
\]
despite
\[
e=d_f\phi
\]
and the affine link being the exact translation-gauge image of flat.

### Theorem I — no fixed second-\(\eta\) repair in the rational boost control

The only fixed linear map satisfying
\[
\iota(\eta b)=b
\]
for all \(b\) is \(\iota=\eta\). For the rational A/B boost,
\[
\eta g\ne g\eta.
\]
Thus this repair is not vector-frame covariant.

### Theorem J — L=2 raw visibility

For the owned Nyquist coframe, the centered readout vanishes but the local \(\kappa_q\) with flat \(A,q\) is nonzero and alternating.

### Theorem K — conditional nilpotent response

Define
\[
T_{\kappa_q}=I+C^\dagger(\kappa_q)P_0.
\]

Then under the controls above:

- flat: \(T_{\kappa_q}=I\);
- pure-gauge diagonal: \(T_{\kappa_q}=I\);
- pure shift: \(T_{\kappa_q}=T_b\);
- pure-linear Lorentz frame:
  \[
  \rho(g)T_{\kappa_q}\rho(g)^{-1}
  =
  T_{g\kappa_q}.
  \]

### Theorem L — full affine action boundary

If one requires a single covariance theorem under arbitrary affine node gauges, then a natural affine-point law for the reference section forces a matching affine-point law for the target solder leg. Current \`rawFullSolderFrameAction\` does not contain this translation law.

---

## 21. Exactly one recommended next step

Construct and formalize the missing **reference-leg section**

\[
\boxed{
q_N(A,e;x,r)\in V_x
}
\]

or an explicitly equivalent affine-origin field, **before** starting the finite graded E dressing.

Its contract should be:

\[
q(A_{\rm flat},0;x,r)=e_r,
\]

on the exact translation-gauge chart,
\[
q(A_\phi,d_f\phi;x+r,r)
=
v_r(d_f\phi,x)-b_\phi(x,r),
\]

under pure-linear local frames,
\[
q(A^g,e^g;y,r)=g_yq(A,e;y,r),
\]

and it must preserve raw \(L=2\) Nyquist and \(L=3\) off-diagonal edge data rather than factor through centered solder.

Only after such a section exists should the project define

\[
\kappa_N(A,e;x,r)
=
A_{x,r}\bigl(q_N(A,e;x+r,r)\bigr)-v_r(e,x)
\]

as a function of \((A,e)\) alone and feed it into \(T_\kappa\).

Do not start finite E dressing until this reference/origin datum is either derived from an independent principle or explicitly accepted as a new primitive.
