# A4D diagonal junction overlap law: relative A/e source, labelled transport, and the residual comparison primitive

**Canonical task:** \`EXP-A4D-DIAGONAL-JUNCTION-OVERLAP-LAW\`  
**Audited baseline:** \`dbc81ec072f8b9a9af6766f73427d3faa93cbd3d\`  
**Research PR:** #120  
**Terminal:** \`DIAGONAL-OVERLAP-REQUIRES-NEW-RELATIVE-AE-DEFECT\`  
**Status:** theorem-ready deep-research classification with an exact conditional sourced-transport construction; no Lean source and no finite graded E dressing.

## 0. Result in one statement

PR #117 localized the reference problem to the Role-labelled diagonal overlap

\[
\delta_r(y)=q_r(y)-v_r(e,y)=\Omega_{rr}(y).
\]

The present task asks for a finite law which fixes that diagonal, supplies a
sourced labelled transport equation, and literally removes the two known
deformations

\[
z_{\rm curl},\qquad z_{\rm harm}.
\]

The strongest result is a conditional construction plus an exact identification
of the missing primitive.

Let

\[
x=y-r,
\qquad
A_{x,r}=(L_{x,r},b_{x,r}).
\]

Pull the predecessor shift into the source fibre:

\[
\boxed{
\bar b_r(y)
:=
L_{x,r}^{-1}b_{x,r}
\in V_y.
}
\tag{0.1}
\]

The next same-Role shift already lives in \(V_y\):

\[
b_r^+(y):=b_{y,r}.
\]

Define the source-fibre affine-shift increment

\[
\boxed{
\Delta^b_r(y)
:=
b_r^+(y)-\bar b_r(y).
}
\tag{0.2}
\]

Likewise define the pulled solder increment

\[
\boxed{
\Delta^v_r(y)
:=
v_r(e,y)-L_{x,r}^{-1}v_r(e,x).
}
\tag{0.3}
\]

A genuine relative A/e bridge must compare (0.2) and (0.3).  The minimum useful
typed datum is a source-fibre endomorphism

\[
\boxed{
\mathfrak J_y(A,e):V_y\to V_y
}
\tag{0.4}
\]

with pure-linear frame law

\[
\boxed{
\mathfrak J'_y
=
g_y\mathfrak J_y g_y^{-1},
}
\tag{0.5}
\]

and exact translation-gauge calibration

\[
\boxed{
\mathfrak J_y\Delta^b_r(y)
=
\Delta^v_r(y)
}
\tag{0.6}
\]

on the owned \(L=I,\ b=e=d_f\phi\) chart and its pure-linear frame orbit.

The associated **relative A/e defect** is

\[
\boxed{
\mathfrak R^{A/e}_r(y)
:=
\Delta^v_r(y)-\mathfrak J_y\Delta^b_r(y).
}
\tag{0.7}
\]

It is a genuine source vector and vanishes on the exact translation-gauge
diagonal.

Once \(\mathfrak J\) is supplied, define the finite diagonal seed

\[
\boxed{
a_r(y)
:=
-\bar b_r(y)-\mathfrak J_y\Delta^b_r(y).
}
\tag{0.8}
\]

For a labelled path \(p:y\to y'\), let

\[
P_p(A):V_{y'}\to V_y
\]

be the owned linear pull \(\operatorname{covariantLin}(A,p,y)\).  Then define

\[
\boxed{
S_p^{A/e}(y,r)
:=
P_p(A)a_r(y')-a_r(y).
}
\tag{0.9}
\]

The sourced diagonal law is

\[
\boxed{
P_p(A)\delta_r(y')-\delta_r(y)
=
S_p^{A/e}(y,r).
}
\tag{0.10}
\]

Equivalently,

\[
P_p(A)\bigl(\delta_r-a_r\bigr)(y')
=
\bigl(\delta_r-a_r\bigr)(y).
\tag{0.11}
\]

Thus every solution is

\[
\boxed{
\delta_r=a_r+h_r,
}
\tag{0.12}
\]

where \(h_r\) is an \(A\)-parallel section.  Local/curl freedom is therefore
removed by the source equation; the only remaining freedom is the exact
parallel/holonomy-fixed kernel.

That remaining finite kernel can be selected **after** the source law by the
already-owned positive observer form \(h_n\).  At a basepoint \(o\), let

\[
\mathcal H_o(A)
=
\bigcap_{\gamma:o\to o}
\operatorname{Fix}P_\gamma(A).
\tag{0.13}
\]

Choose explicit labelled paths \(p_y:o\to y\) and form the transported seed
mean

\[
\bar a_o
=
\frac1{|X|}
\sum_y P_{p_y}(A)a_r(y).
\tag{0.14}
\]

The unique \(h_{n(o)}\)-positive correction is the minimizer

\[
\boxed{
h_o
=
\arg\min_{h\in\mathcal H_o(A)}
\|\bar a_o+h\|_{h_{n(o)}}^2.
}
\tag{0.15}
\]

Strict positivity of \(h_n\) makes (0.15) unique.  Extend \(h_o\) as the
parallel section \(h_r\).  This kills the full parallel kernel, including the
PR #114 harmonic deformation whenever it survives the local source equation.

On the mandatory control sectors:

- flat: \(a=0\), so \(h=0\), \(\delta=0\);
- exact translation gauge: \(a=\delta_{\rm req}\) and its periodic transported
  mean is zero, so \(h=0\), \(\kappa=0\);
- pure constant affine shift: \(a=-b\) is parallel, so (0.15) gives \(h=b\),
  hence \(\delta=0\), \(\kappa=b\);
- coframe-only Nyquist/corner/curl/harmonic backgrounds: \(b=0\), so \(a=0\);
  the selected \(\delta\) is zero on the flat-linear controls, preserving raw
  solder response instead of cancelling it.

The conditional package therefore does what was requested:

1. it gives a finite diagonal law;
2. it gives exact sourced append/reverse transport;
3. it rejects \(z_{\rm curl}\);
4. it reduces \(z_{\rm harm}\) to the parallel kernel and then rejects it by
   the post-source positive selection;
5. it retains labelled holonomy rather than quotienting it.

But current D0 does **not** own the comparison datum (0.4)–(0.6).

The obvious current candidates fail exactly:

- fixed \(\eta\) has the right translation-chart value but is not a
  vector-endomorphism intertwiner under the rational A/B boost;
- the observer-derived \(h_n^{-1}\eta\) is covariant but changes the required
  pure-gauge diagonal when \(n\) moves, and uses observer positivity to invent
  the source before the source law;
- the solder-conjugate \(B_e\eta B_e^{-1}\) is covariant on a nondegenerate
  branch but is not \(\eta\) on the explicit \(L=3\) translation-gauge shear;
- path-transporting a basepoint copy of \(\eta\) requires a new basepoint
  reference involution and becomes path/holonomy dependent.

There is also a useful **regular nondegenerate passport** built from the owned
raw solder and affine shifts, but it does not extend to a globally selected
source on every raw coframe.  It is recorded below.

Therefore the strongest honest terminal is

\[
\boxed{
\texttt{DIAGONAL-OVERLAP-REQUIRES-NEW-RELATIVE-AE-DEFECT}.
}
\tag{0.16}
\]

This is not a universal no-go.  It identifies the exact missing cross-channel
operation and proves that, once supplied, the rest of the sourced
junction/path/harmonic selection problem has a finite solution.

---

## 1. Exact overlap type contract

Fix

\[
X=X_N=\operatorname{ArchiveRolePhaseGroup}N,
\qquad
V=\operatorname{RoleSpace}.
\]

For each positive Role edge

\[
x\xleftarrow{\ r\ }y=x+r
\]

the repository owns

\[
A_{x,r}:V_y\to_{\rm aff}V_x,
\qquad
A_{x,r}(z)=L_{x,r}z+b_{x,r},
\]

and the raw solder leg

\[
v_r(e,x)\in V_x.
\]

For a reference section \(q\),

\[
\delta_r(y)=q_r(y)-v_r(e,y)\in V_y.
\tag{1.1}
\]

The Role overlap is

\[
\boxed{
\Omega_{rs}(y)
=
q_r(y)-v_s(e,y)
=
v_r(e,y)-v_s(e,y)+\delta_r(y).
}
\tag{1.2}
\]

The conditional edge mismatch is

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(q_r(y))-v_r(e,x).
\tag{1.3}
\]

Writing

\[
\tau_r(A,e;x)
=
A_{x,r}(v_r(e,y))-v_r(e,x),
\]

one has exactly

\[
\boxed{
\kappa_q
=
\tau_r+L_{x,r}\delta_r(y).
}
\tag{1.4}
\]

Thus the only remaining selector variable is \(\delta\).

---

## 2. Source-frame law and frozen Role overlap identities

Under a pure-linear node frame,

\[
L'_{x,r}=g_xL_{x,r}g_y^{-1},
\qquad
b'_{x,r}=g_xb_{x,r},
\]

and

\[
v'_r(e',x)=g_xv_r(e,x).
\]

Hence a selected diagonal must obey

\[
\boxed{
\delta'_r(y)=g_y\delta_r(y).
}
\tag{2.1}
\]

Then (1.2) gives

\[
\boxed{
\Omega'_{rs}(y)=g_y\Omega_{rs}(y).
}
\tag{2.2}
\]

The solder-difference identity is automatic:

\[
\boxed{
\Omega_{rs}-\Omega_{rt}=v_t-v_s.
}
\tag{2.3}
\]

The exact twisted Role cocycle is also automatic:

\[
\boxed{
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
}
\tag{2.4}
\]

The diagonal is

\[
\Omega_{rr}=\delta_r.
\tag{2.5}
\]

Therefore none of (2.2)–(2.4) selects the diagonal.  The source law below is
the genuinely new content.

---

## 3. The predecessor defect and why it is not the selector

There is one obvious source-fibre vector that exactly reproduces the
pure-gauge diagonal:

\[
\boxed{
\rho_r(y)
=
A_{x,r}^{-1}(v_r(e,x))-v_r(e,y)
=
L_{x,r}^{-1}(v_r(e,x)-b_{x,r})-v_r(e,y).
}
\tag{3.1}
\]

On exact pure gauge,

\[
\rho_r(y)=\delta_r^{\rm req}(y).
\]

But \(\rho\) is not the physical selector.

### 3.1 Pure shift

For

\[
e=0,\qquad L=I,\qquad b\ne0,
\]

one has

\[
\rho=-b.
\]

Choosing \(\delta=\rho\) gives

\[
\kappa=0
\]

and erases the required pure affine shift.

### 3.2 Coframe-only backgrounds

For

\[
b=0,
\]

\[
\rho=L^{-1}v_x-v_y.
\]

At flat linear connection this is minus the raw solder finite difference.

Thus choosing \(\delta=\rho\) cancels the raw \(L=2\) Nyquist and generic
coframe nonparallelism.

The predecessor defect is therefore a useful algebraic endpoint but not a
relative A/e selector.

---

## 4. Why the sourced derivative of rho also fails

A natural attempted repair is to use only the derivative of \(\rho\):

\[
P_s\rho(y+s)-\rho(y)
\]

as the source and leave its parallel component to a later global condition.

This still fails the raw finite controls.

On a coframe-only background with

\[
b=0,
\]

the source is the derivative of the raw solder predecessor defect.  Solving it
forces

\[
\delta-\rho
\]

to be parallel.

At the flat \(L=2\) Nyquist witness, the positive observer/global zero-mode
choice then removes the parallel remainder and gives

\[
\delta=\rho,
\]

which cancels the raw solder mismatch.

Therefore

\[
\boxed{
S=d_A\rho
\text{ is not an admissible sourced overlap law.}
}
\tag{4.1}
\]

The source must know which solder variation is correlated with affine shift,
not simply use every solder variation.

---

## 5. Why a shift-only source fails exact pure gauge

The opposite attempt uses only the pulled predecessor shift

\[
-\bar b_r(y)
=
-L_{x,r}^{-1}b_{x,r}.
\]

This keeps coframe-only backgrounds visible and makes a constant pure shift a
parallel mode.

It fails the \(L=3\) exact gauge witness.

The B-valued shift cycle is

\[
(3,3,-6)e_B.
\tag{5.1}
\]

The required diagonal overlap, ordered by source site, is

\[
\boxed{
(15,-3,-12)e_B.
}
\tag{5.2}
\]

The shift-only predecessor gives

\[
\boxed{
(6,-3,-3)e_B.
}
\tag{5.3}
\]

The difference is

\[
\boxed{
(9,0,-9)e_B,
}
\tag{5.4}
\]

which is not parallel.

Therefore no later harmonic/basepoint correction can turn the shift-only source
into the required pure-gauge diagonal.

This proves that a **longitudinal A/e cross-channel comparison** is necessary.

---

## 6. Exact relative A/e increments

For \(x=y-r\), pull predecessor data into \(V_y\):

\[
\bar b_r(y)=L_{x,r}^{-1}b_{x,r},
\tag{6.1}
\]

\[
\bar v_r(y)=L_{x,r}^{-1}v_r(e,x).
\tag{6.2}
\]

Define

\[
\Delta^b_r(y)=b_{y,r}-\bar b_r(y),
\tag{6.3}
\]

\[
\Delta^v_r(y)=v_r(e,y)-\bar v_r(y).
\tag{6.4}
\]

Both are source-fibre vectors.

Under a pure-linear frame,

\[
\boxed{
(\Delta^b_r)'(y)=g_y\Delta^b_r(y),
\qquad
(\Delta^v_r)'(y)=g_y\Delta^v_r(y).
}
\tag{6.5}
\]

The type problem is therefore not source/target typing.

The missing question is:

> what geometric operation says how much of \(\Delta^v\) is the solder image
> of \(\Delta^b\)?

On the literal translation-gauge chart,

\[
L=I,\qquad b=e=d_f\phi,
\]

and the already-owned solder formula gives

\[
\boxed{
\Delta^v_r(y)
=
\eta\,\Delta^b_r(y)
}
\tag{6.6}
\]

in the fixed chart coordinates.

Equation (6.6) is the finite longitudinal relation the selector needs.

But the fixed matrix \(\eta\), acting as a vector endomorphism, is not
pure-linear frame equivariant.

---

## 7. The minimum comparison primitive

Introduce a source-fibre endomorphism

\[
\mathfrak J_y:V_y\to V_y
\]

with

\[
\boxed{
\mathfrak J'_y
=
g_y\mathfrak J_yg_y^{-1}.
}
\tag{7.1}
\]

The required translation-gauge calibration is

\[
\boxed{
\mathfrak J_y\Delta^b_r(y)
=
\Delta^v_r(y).
}
\tag{7.2}
\]

On the literal chart, this reduces to

\[
\mathfrak J_y=\eta
\]

on the span of the actual shift increments.

A full endomorphism is a convenient theorem-ready interface; logically the
minimum datum could be an edge-labelled map only on the actual increment
\(\Delta^b_r(y)\).

Define the relative A/e defect

\[
\boxed{
\mathfrak R_r^{A/e}(y)
=
\Delta^v_r(y)-\mathfrak J_y\Delta^b_r(y).
}
\tag{7.3}
\]

Then

\[
(\mathfrak R_r^{A/e})'
=
g_y\mathfrak R_r^{A/e}.
\tag{7.4}
\]

On exact translation gauge,

\[
\boxed{
\mathfrak R_r^{A/e}=0.
}
\tag{7.5}
\]

This is the first genuinely cross-channel tensor in the selector chain.

---

## 8. The finite diagonal seed

Define

\[
\boxed{
a_r(y)
=
-\bar b_r(y)-\mathfrak J_y\Delta^b_r(y).
}
\tag{8.1}
\]

This is source-typed and transforms by

\[
a'_r(y)=g_ya_r(y).
\tag{8.2}
\]

The predecessor defect (3.1) satisfies the exact identity

\[
\boxed{
\rho_r(y)
=
a_r(y)-\mathfrak R_r^{A/e}(y).
}
\tag{8.3}
\]

Thus:

- on the translation-gauge diagonal, \(\mathfrak R^{A/e}=0\), hence
  \(a=\rho=\delta_{\rm req}\);
- on coframe-only backgrounds \(b=0\), one has \(a=0\) while
  \(\mathfrak R^{A/e}=\Delta^v\), so raw solder variation is retained instead
  of cancelled;
- on a constant pure affine shift, \(\Delta^b=0\) and
  \[
  a=-b,
  \]
  which is purely parallel and can be removed by the downstream global
  condition without touching local response.

This is exactly the separation that the predecessor and shift-only attempts
could not achieve.

---

## 9. Exact L=3 translation-gauge control

Use the frozen B-valued cycle

\[
b=(3,3,-6)e_B.
\]

Since \(\eta e_B=-e_B\), the solder B-coordinates are

\[
v=(-3,-3,6)e_B.
\]

At source site \(y\), with predecessor \(x=y-A\),

\[
a_A(y)
=
-b_A(x)-\eta\bigl(b_A(y)-b_A(x)\bigr).
\]

Exact arithmetic gives

\[
\boxed{
a_A=(15,-3,-12)e_B.
}
\tag{9.1}
\]

This is exactly the PR #117 required diagonal.

It also has

\[
\sum_y a_A(y)=0.
\tag{9.2}
\]

Therefore the downstream parallel-kernel selector leaves it unchanged:

\[
\delta_A=a_A.
\]

Then

\[
\boxed{
\kappa=0
}
\tag{9.3}
\]

edge by edge.

---

## 10. Pure affine-shift control

Take

\[
e=0,\qquad L=I,\qquad b\ne0
\]

with the repository's constant pure-shift connection.

Then

\[
\Delta^b=0,
\qquad
a=-b.
\]

The source below is zero because \(a\) is constant.

The solution space is

\[
\delta=-b+h
\]

with constant/parallel \(h\).

The positive global selector chooses

\[
h=b,
\]

hence

\[
\boxed{
\delta=0.
}
\tag{10.1}
\]

Therefore

\[
\boxed{
q=e_r,
\qquad
\kappa=b\ne0.
}
\tag{10.2}
\]

The affine shift is not absorbed.

---

## 11. Flat control

For

\[
A=A_{\rm flat},
\qquad
e=0,
\]

one has

\[
b=0,
\qquad
a=0.
\]

The selected parallel correction is zero.

Hence

\[
\boxed{
\delta=0,
\qquad
q=e_r,
\qquad
\kappa=0.
}
\tag{11.1}
\]

---

## 12. Sourced labelled transport

Let

\[
p:y\to y'
\]

be an arbitrary labelled path and let

\[
P_p(A)=\operatorname{covariantLin}(A,p,y):V_{y'}\to V_y.
\]

Define

\[
\boxed{
S_p^{A/e}(y,r)
=
P_p(A)a_r(y')-a_r(y).
}
\tag{12.1}
\]

The diagonal transport law is

\[
\boxed{
P_p(A)\delta_r(y')-\delta_r(y)
=
S_p^{A/e}(y,r).
}
\tag{12.2}
\]

No endpoint-only quotient is taken.

Equation (12.2) is equivalent to

\[
P_p(A)(\delta_r-a_r)(y')
=
(\delta_r-a_r)(y).
\tag{12.3}
\]

Thus the residual field

\[
h_r:=\delta_r-a_r
\]

is parallel.

This is the precise finite meaning of "source first, basepoint later."

---

## 13. Exact append law for the source

Let

\[
p:y\to y',
\qquad
q:y'\to y''.
\]

In repository pull order,

\[
P_{p++q}=P_pP_q.
\]

Then

\[
\begin{aligned}
S_{p++q}
&=
P_pP_q a(y'')-a(y)
\\
&=
\bigl(P_pa(y')-a(y)\bigr)
+
P_p\bigl(P_qa(y'')-a(y')\bigr).
\end{aligned}
\]

Therefore

\[
\boxed{
S_{p++q}
=
S_p+P_pS_q.
}
\tag{13.1}
\]

This is the sourced cocycle/append law.

It is not imposed separately; it follows from the finite seed.

---

## 14. Exact reverse law

For the reversed labelled path \(\bar p:y'\to y\),

\[
P_{\bar p}=P_p^{-1}.
\]

Hence

\[
\begin{aligned}
S_{\bar p}
&=
P_p^{-1}a(y)-a(y')
\\
&=
-P_p^{-1}\bigl(P_pa(y')-a(y)\bigr).
\end{aligned}
\]

Thus

\[
\boxed{
S_{\bar p}
=
-P_p^{-1}S_p.
}
\tag{14.1}
\]

The source therefore has the exact reverse law required by the existing
labelled path skeleton.

---

## 15. Junction overlap after diagonal selection

Once \(\delta\) is selected, define

\[
\boxed{
\Omega_{rs}(y)
=
v_r(e,y)-v_s(e,y)+\delta_r(y).
}
\tag{15.1}
\]

Then:

\[
\Omega_{rs}-\Omega_{rt}=v_t-v_s,
\]

and

\[
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
\]

For an \(r\to s\) path junction, the actual transported overlap is

\[
\boxed{
J_{rs}
=
L_r\Omega_{rs}.
}
\tag{15.2}
\]

The original exact two-edge identity remains

\[
\kappa_1+L_1\kappa_2
=
(A_1A_2)(q_2)-v_1+J_{rs}.
\tag{15.3}
\]

Nothing is compressed to endpoint-only provenance.

---

## 16. General solution and the holonomy-fixed kernel

Equation (12.3) says that \(h=\delta-a\) is parallel.

Fix a basepoint \(o\).

For every loop

\[
\gamma:o\to o,
\]

parallelity requires

\[
P_\gamma h(o)=h(o).
\]

Therefore

\[
\boxed{
h(o)\in
\mathcal H_o(A)
:=
\bigcap_{\gamma:o\to o}\operatorname{Fix}P_\gamma(A).
}
\tag{16.1}
\]

Conversely, any \(h(o)\in\mathcal H_o(A)\) extends path-independently to a
global parallel section.

Thus the source law reduces the entire remaining nonselection to the finite
vector space \(\mathcal H_o(A)\).

This is an exact kernel classification.

---

## 17. Observer-positive selection only after the source law

The repository owns a strictly positive observer form \(h_n\).

Choose one basepoint \(o\) and labelled paths

\[
p_y:o\to y.
\]

Transport every seed value to \(V_o\):

\[
P_y:=P_{p_y}(A):V_y\to V_o.
\]

Define

\[
\boxed{
\bar a_o
=
\frac1{|X|}
\sum_y P_ya_r(y).
}
\tag{17.1}
\]

Now minimize only over the already-classified parallel kernel:

\[
\boxed{
\Phi_o(h)
=
h_{n(o)}(\bar a_o+h,\bar a_o+h),
\qquad
h\in\mathcal H_o(A).
}
\tag{17.2}
\]

Since \(h_{n(o)}\) is positive definite and \(\mathcal H_o\) is finite
dimensional, there is a unique minimizer

\[
\boxed{
h_o^*
=
-\operatorname{Proj}^{\,h_{n(o)}}_{\mathcal H_o}\bar a_o.
}
\tag{17.3}
\]

Extend \(h_o^*\) as the unique parallel section.

Finally set

\[
\boxed{
\delta_r=a_r+h_r^*.
}
\tag{17.4}
\]

This is the correct logical order:

1. relative A/e source;
2. labelled transport;
3. parallel-kernel classification;
4. observer-positive minimization.

The observer does not invent the source.

---

## 18. Frame covariance of the post-source selector

Under a pure-linear frame,

\[
P'_y
=
g_oP_yg_y^{-1},
\]

and

\[
a'_r(y)=g_ya_r(y).
\]

Therefore

\[
\boxed{
\bar a'_o=g_o\bar a_o.
}
\tag{18.1}
\]

Loop holonomies conjugate by \(g_o\), so

\[
\mathcal H'_o=g_o\mathcal H_o.
\tag{18.2}
\]

The observer transforms as

\[
n'_o=g_on_o,
\]

and the owned observer congruence gives

\[
h_{n'_o}(g_ou,g_ov)=h_{n_o}(u,v).
\]

Uniqueness of the minimizer therefore yields

\[
h_o^{*\prime}=g_oh_o^*.
\]

Consequently

\[
\boxed{
\delta'_r(y)=g_y\delta_r(y).
}
\tag{18.3}
\]

The conditional full selector is exactly pure-linear frame covariant.

---

## 19. Why a path family is still an explicit datum on generic holonomy

The source law itself is path-functorial and retains every labelled path.

The transported mean (17.1) additionally chooses one path \(p_y\) from \(o\)
to each site.

On flat and exact translation-gauge controls, all linear pulls are identity,
so this choice is invisible.

On a generic background with nontrivial linear holonomy, changing \(p_y\)
changes \(P_ya(y)\) by a loop holonomy.

If every loop preserves \(h_{n(o)}\), projection onto the common fixed subspace
may remove part of that dependence.

No such all-loop observer-isometry theorem is owned for arbitrary \(A\).

Therefore:

\[
\boxed{
\text{the post-source harmonic/global selection retains an explicit basepoint/path gauge datum on generic holonomy backgrounds.}
}
\tag{19.1}
\]

This datum is downstream of the relative A/e source and must not be hidden.

---

## 20. Curl deformation rejection

PR #114 defines a covariant local deformation

\[
z_{\rm curl}.
\]

Under the sourced law, replacing

\[
\delta\mapsto\delta+\lambda z_{\rm curl}
\]

preserves (12.2) if and only if

\[
P_pz_{\rm curl}(y')=z_{\rm curl}(y)
\]

for every labelled path.

Thus \(z_{\rm curl}\) would have to be parallel.

On the flat \(L=3\) single-corner witness

\[
e_A{}^B(0)=1,
\]

the exact solder curl has the B-coordinate pattern, along the relevant
three-cycle,

\[
\boxed{
(-1,0,+1).
}
\tag{20.1}
\]

Flat transport is identity, so this field is not parallel.

Therefore

\[
\boxed{
\lambda=0
}
\tag{20.2}
\]

is forced.

The known curl deformation is literally eliminated by the local sourced
transport equation.

---

## 21. Harmonic deformation rejection

For the constant harmonic witness

\[
e_A{}^B=1,
\qquad
A=A_{\rm flat},
\]

the affine shifts vanish.

Hence

\[
a=0.
\]

The local source law is homogeneous, so a constant \(z_{\rm harm}\) is a
parallel solution.

This is exactly the residual kernel identified in §16.

For flat connection,

\[
\mathcal H_o=V.
\]

The transported mean of the zero seed is zero, and the unique observer-positive
minimizer is

\[
h_o^*=0.
\]

Any nonzero constant addition changes \(h\) away from the unique minimizer.

Therefore

\[
\boxed{
\mu=0
}
\tag{21.1}
\]

is forced for the PR #114 harmonic deformation.

The two deformations are thus killed for structurally different reasons:

- \(z_{\rm curl}\) fails the sourced transport equation;
- \(z_{\rm harm}\) lies in the parallel kernel but fails the unique
  post-source positive kernel selector.

This is the desired local/global split.

---

## 22. L=2 raw Nyquist control

Take the owned period-two raw coframe

\[
e_A{}^A=(-2,+2)
\]

with flat affine connection.

The corresponding A-solder vector component is

\[
v_A=(-1,3)e_A.
\]

Since \(b=0\),

\[
a=0,
\qquad
\delta=0.
\]

Thus

\[
q_A=v_A.
\]

The edge mismatch is the raw solder finite difference:

\[
\boxed{
\kappa_A=(+4,-4)e_A.
}
\tag{22.1}
\]

In particular it is nonzero at both sites.

This matches the already-owned raw parallel-defect magnitude

\[
\operatorname{archiveAffineSolderParallelDefect}=4.
\]

Therefore the conditional selector does **not** factor through centered solder
data and does not erase the Nyquist mode.

---

## 23. L=3 off-diagonal corner control

Take flat \(A\) and

\[
e_A{}^B(0)=1
\]

with all other components zero.

Then

\[
b=0,
\qquad
a=0,
\qquad
\delta=0.
\]

At the origin,

\[
v_A(0)=e_A-e_B,
\]

while at its positive A-neighbour,

\[
v_A(A)=e_A.
\]

Therefore the A-edge mismatch at the origin is

\[
\boxed{
\kappa_A(0)=e_B\ne0.
}
\tag{23.1}
\]

The corner remains visible.

---

## 24. Constant harmonic coframe control

Take

\[
e_A{}^B(x)=1
\]

for every site and flat \(A\).

Then

\[
b=0,
\qquad
a=0,
\qquad
\delta=0.
\]

The A-solder leg is constant,

\[
v_A=e_A-e_B.
\]

Hence the local same-Role mismatch may vanish.

This does **not** identify the background with flat:

- the raw coframe has a nonzero cycle period;
- the Role overlaps \(\Omega_{rs}=v_r-v_s\) differ from flat;
- the PR #114 global harmonic invariant is nonzero;
- the post-source kernel selector forbids adding a new nonzero constant
  diagonal overlap.

The harmonic datum is retained as raw geometry even when one local edge
mismatch vanishes.

---

## 25. Nontrivial labelled holonomy control

For a loop \(\gamma:o\to o\), the source is

\[
S_\gamma(o,r)
=
P_\gamma a_r(o)-a_r(o).
\tag{25.1}
\]

The selected diagonal satisfies

\[
P_\gamma\delta_r(o)-\delta_r(o)
=
S_\gamma(o,r).
\tag{25.2}
\]

Subtracting gives

\[
(P_\gamma-I)h_r(o)=0.
\]

Thus nontrivial holonomy is not quotiented.

It directly restricts the admissible parallel correction by

\[
h_r(o)\in\operatorname{Fix}P_\gamma.
\]

Different labelled loops remain different constraints.

This is compatible with the merged labelled path parent.

---

## 26. Candidate audit I — fixed eta

On the literal translation-gauge chart the desired comparison is

\[
\mathfrak J=\eta.
\]

One might therefore simply use \(\eta\) as a vector endomorphism everywhere.

This fails pure-linear frame covariance.

For the exact rational A/B boost

\[
g=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix},
\]

one has

\[
\eta g\ne g\eta.
\tag{26.1}
\]

Therefore

\[
\eta(gu)\ne g(\eta u)
\]

for generic \(u\).

The fixed Lorentz metric is the correct row/vector converter in its typed
representation role, but it is not an equivariant **vector endomorphism**.

So fixed \(\eta\) cannot be promoted to \(\mathfrak J\).

---

## 27. Candidate audit II — observer-derived comparison

Because \(h_n\) is positive and covariant, one can form an observer-dependent
endomorphism schematically equivalent to

\[
\mathfrak J_n=h_n^{-1}\eta.
\]

At the rest observer,

\[
h_n=I,
\qquad
\mathfrak J_n=\eta.
\]

Under the rational boost it becomes the conjugate

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
\tag{27.1}
\]

In particular,

\[
e_B
\mapsto
\left(-\frac{40}{9},-\frac{41}{9},0,0\right),
\]

not

\[
-e_B.
\]

This is exactly what covariance requires for a **moved observer**.

But the frozen exact translation-gauge diagonal is a geometric A/e statement
and is independent of an arbitrary observer choice.

Using \(\mathfrak J_n\) as the source would therefore make the diagonal depend
on \(n\) before the source law has been established.

It also violates the task's required logical order: \(h_n\) may resolve the
post-source kernel, not invent the source.

Thus observer positivity is not the missing relative A/e bridge.

---

## 28. Candidate audit III — solder-conjugate eta

Package the raw solder legs into

\[
B_e(x):V_{\rm ref}\to V_x,
\qquad
B_e(x)e_s=v_s(e,x).
\]

When \(B_e\) is invertible, the endomorphism

\[
\mathfrak J_B
=
B_e\eta B_e^{-1}
\tag{28.1}
\]

has exactly the desired conjugation law.

It fails translation-gauge calibration.

On the \(L=3\) equal-neighbour shear with

\[
B=I-3E_{B,A},
\]

exact arithmetic gives

\[
\boxed{
\mathfrak J_B-\eta
=
-6E_{B,A}\ne0.
}
\tag{28.2}
\]

Thus \(\mathfrak J_B\) does not equal the required chart \(\eta\).

Moreover raw solder need not be invertible on every allowed coframe.

This candidate is excluded as the global comparison primitive.

---

## 29. Candidate audit IV — basepoint-transported eta

Choose a basepoint \(o\), a path \(p_y:o\to y\), and define

\[
\mathfrak J_y
=
P_{p_y}^{-1}\mathfrak J_oP_{p_y}.
\tag{29.1}
\]

If one supplies

\[
\mathfrak J_o=\eta
\]

in a chosen frame, this reproduces \(\eta\) on the flat translation chart.

But:

1. \(\mathfrak J_o=\eta\) is itself a new basepoint reference datum;
2. under an active frame it must transform as
   \[
   \mathfrak J'_o=g_o\mathfrak J_og_o^{-1},
   \]
   so it cannot remain a fixed numerical \(\eta\);
3. on nontrivial holonomy, changing the path to \(y\) changes (29.1) unless
   \(\mathfrak J_o\) commutes with every loop holonomy.

Therefore path transport can propagate a comparison primitive.

It cannot derive one.

---

## 30. A useful regular nondegenerate A/e passport

Although current geometry does not give a global \(\mathfrak J\), there is a
real constructive partial result on a regular branch.

Define the affine-shift frame map

\[
C_A(x):V_{\rm ref}\to V_x,
\qquad
C_A(x)e_s=b_{x,s}.
\tag{30.1}
\]

Under pure-linear frames,

\[
B'_e=g_xB_e,
\qquad
C'_A=g_xC_A.
\tag{30.2}
\]

If \(B_e(x)\) is invertible, the ratio

\[
\boxed{
K_x
=
B_e(x)^{-1}C_A(x)
}
\tag{30.3}
\]

is exactly frame invariant.

On the literal translation-gauge chart, write the shift matrix as \(D_x\).
Then

\[
B_x=I+\eta D_x,
\qquad
C_x=D_x.
\tag{30.4}
\]

Since

\[
K_x=B_x^{-1}D_x,
\]

one obtains the finite reconstruction equation

\[
\boxed{
D_x-\eta D_xK_x=K_x.
}
\tag{30.5}
\]

Equivalently, with

\[
\widehat B_x=I+\eta D_x,
\]

\[
\boxed{
\widehat B_x-\eta\widehat B_xK_x=I.
}
\tag{30.6}
\]

Thus the invariant \(K_x\) carries enough local information to reconstruct a
canonical translation-chart representative whenever the finite linear operator

\[
\mathcal L_{K_x}:X\mapsto X-\eta XK_x
\tag{30.7}
\]

is invertible.

In vectorized coordinates the regularity matrix is

\[
I-K_x^T\otimes\eta.
\tag{30.8}
\]

This is a genuine finite A/e **passport**.

It shows that the covariance problem is not hopeless.

---

## 31. Why the regular passport is not the global selector

The passport does not close the canonical task.

### 31.1 Raw solder can be degenerate

The repository already proves that not every coframe has nondegenerate solder.

No physical admissibility theorem restricts this task to the invertible branch.

### 31.2 The reconstruction operator can be singular

Even with invertible \(B_e\), the operator (30.7) need not be invertible for
arbitrary \(K\).

### 31.3 Local passport is not global exactness

A periodic exact translation gauge also has global zero-period conditions.

A constant pure shift can share local algebraic features while carrying a
nonzero translation period.

Cycle data are still required.

### 31.4 A canonical representative is not yet a canonical physical source

On the regular branch one can reconstruct a chart representative and compare
its solder Gram with the actual solder Gram.

That classifies whether a pair lies on the same local Lorentz orbit.

It does not supply an owned theorem selecting a vector response on every
off-orbit raw background or across the singular locus.

Promoting one arbitrary extension would again be an ansatz.

Thus (30.3)–(30.8) are a positive regular-branch result, not a complete
selector.

---

## 32. Relative curvature/torsion alone do not supply the missing longitudinal map

The repository owns affine open curvature and open torsion.

PR #114 also constructs the solder curl

\[
C_{rs}.
\]

These are important transverse data.

They cannot replace \(\mathfrak J\).

On exact flat translation gauge:

- affine curvature vanishes;
- affine open torsion vanishes;
- solder curl vanishes.

On a constant pure affine shift:

- the same local square defects can vanish.

Yet the diagonal requirements differ:

\[
\delta_{\rm gauge}\ne0
\]

generically, while

\[
\delta_{\rm shift}=0.
\]

The difference lives in the **longitudinal edge correlation** between affine
shift and solder change, precisely (6.3)–(6.6).

Therefore a source built only from current square curvature/torsion/curl cannot
reproduce the required \(L=3\) pure-gauge diagonal.

---

## 33. Full affine origin option

PR #115 proves that if both reference and solder are affine points, their
difference transforms homogeneously.

That would make

\[
\delta=q-v
\]

a natural vector under full affine node gauges.

It does not supply the comparison map \(\mathfrak J\).

Current raw solder owns only a linear frame action, not the affine translation
law.

Even after an affine solder/origin action is added, a linearly covariant
endomorphism/source still has to be selected.

Thus full-affine origin structure is compatible with the conditional package
but does not remove the terminal.

---

## 34. Exact rational checker

A standalone exact-rational checker passed **41/41 assertions**.

It verifies:

1. rational A/B boost right inverse;
2. left inverse;
3. exact Lorentz relation;
4. \(\eta g\ne g\eta\);
5–6. the exact \(41/9,-40/9,40/9,-41/9\) observer-conjugate block;
7. its action on \(e_B\);
8. the literal \(\eta e_B=-e_B\);
9. observer candidate differs from chart \(\eta\);
10. the \(L=3\) shift period is zero;
11. its solder B-coordinates are \((-3,-3,6)\);
12. the required diagonal is \((15,-3,-12)\);
13. that diagonal has zero mean;
14. the conditional \(\mathfrak J=\eta\) seed reproduces it exactly;
15. it is nonconstant;
16. the shift-only predecessor seed is \((6,-3,-3)\);
17. its error is \((9,0,-9)\);
18. a pure-shift seed is parallel;
19. its mean is nonzero;
20. the parallel correction restores \(\delta=0\);
21. pure-shift \(\kappa=b\);
22. coframe-only seed vanishes;
23. the \(L=2\) selected raw mismatch is \((+4,-4)e_A\);
24. both values are nonzero;
25. the \(L=3\) corner mismatch is nonzero;
26. the exact corner curl pattern is \((-1,0,+1)e_B\);
27. it is nonparallel;
28. nonzero \(z_{\rm curl}\) violates homogeneous flat source transport;
29. the harmonic deformation is nonzero and parallel;
30. its mean is nonzero, so the global selector rejects it;
31. full affine point differences cancel node translation;
32. linear-only solder leaves the translation residual;
33. \(B\eta B^{-1}\ne\eta\) on the gauge shear;
34. its exact off-diagonal deviation is \(-6E_{B,A}\);
35. source append law;
36. source reverse law;
37–39. the sourced solution on two consecutive toy pulls and their append;
40. twisted Role overlap cocycle;
41. extraction of the diagonal overlap.

All calculations use exact rational fractions; no floating tolerance is used.

---

## 35. Theorem-ready handoff

### Theorem A — relative shift and solder increments

The source-fibre quantities

\[
\Delta^b_r(y)
=
b_{y,r}-L_{y-r,r}^{-1}b_{y-r,r}
\]

and

\[
\Delta^v_r(y)
=
v_r(y)-L_{y-r,r}^{-1}v_r(y-r)
\]

transform by the source frame \(g_y\).

### Theorem B — conditional relative A/e defect

If \(\mathfrak J'_y=g_y\mathfrak J_yg_y^{-1}\), then

\[
\mathfrak R_r^{A/e}
=
\Delta^v_r-\mathfrak J_y\Delta^b_r
\]

is source-vector covariant.

If \(\mathfrak J\) obeys the translation-gauge calibration, then
\(\mathfrak R^{A/e}=0\) on the exact diagonal.

### Theorem C — finite diagonal seed

Define

\[
a_r
=
-\bar b_r-\mathfrak J\Delta^b_r.
\]

Then \(a\) is source-vector covariant and equals the required diagonal overlap
on exact translation gauge.

It vanishes on every \(b=0\) coframe-only background.

On a constant pure shift it equals \(-b\), a parallel mode.

### Theorem D — predecessor decomposition

For

\[
\rho_r=A^{-1}_{y-r,r}v_r(y-r)-v_r(y),
\]

\[
\rho_r
=
a_r-\mathfrak R_r^{A/e}.
\]

Thus the relative defect is exactly the term preventing the tautological
predecessor from being used as the physical diagonal.

### Theorem E — sourced append/reverse law

For

\[
S_p=P_pa(y')-a(y),
\]

\[
S_{p++q}=S_p+P_pS_q,
\]

and

\[
S_{\bar p}=-P_p^{-1}S_p.
\]

### Theorem F — sourced diagonal solution space

The equation

\[
P_p\delta(y')-\delta(y)=S_p
\]

holds for all labelled paths iff

\[
\delta=a+h
\]

with \(h\) a global \(A\)-parallel section.

At a basepoint,

\[
h(o)\in\bigcap_\gamma\operatorname{Fix}P_\gamma.
\]

### Theorem G — observer-positive kernel uniqueness

Given a basepoint/path family after the source law, the functional

\[
h\mapsto
\|\bar a_o+h\|_{h_{n(o)}}^2
\]

on the holonomy-fixed subspace has a unique minimizer.

The resulting diagonal is pure-linear frame covariant.

### Theorem H — exact control package

With a calibrated \(\mathfrak J\) and the post-source kernel selector:

- flat gives \(\delta=0\);
- exact translation gauge gives
  \[
  \delta_r(y)=v_r(y-r)-b_{y-r,r}-v_r(y)
  \]
  and \(\kappa=0\);
- pure constant affine shift gives \(\delta=0,\ \kappa=b\);
- L=2 raw Nyquist remains nonzero;
- L=3 corner remains nonzero.

### Theorem I — curl rejection

The known \(z_{\rm curl}\) deformation fails the sourced transport equation on
the explicit flat L=3 corner unless its coefficient is zero.

### Theorem J — harmonic rejection

The known \(z_{\rm harm}\) deformation lies in the flat parallel kernel on the
constant harmonic witness.

The unique post-source positive kernel minimizer selects zero coefficient.

### Theorem K — current candidate obstruction

None of:

- fixed \(\eta\);
- observer-derived \(h_n^{-1}\eta\);
- solder-conjugate \(B_e\eta B_e^{-1}\);
- basepoint-transported fixed \(\eta\);

is an already-owned global \(\mathfrak J\) satisfying all required calibration
and covariance properties without additional data or domain restrictions.

### Theorem L — regular nondegenerate passport

On the branch where \(B_e\) and
\(X\mapsto X-\eta X(B_e^{-1}C_A)\) are invertible, the invariant ratio

\[
K=B_e^{-1}C_A
\]

determines a unique translation-chart representative by

\[
D-\eta DK=K.
\]

This is a finite frame-invariant A/e passport, but not a global selector across
the singular/degenerate locus.

---

## 36. Exact terminal

The task has advanced beyond PR #117 in three ways:

1. it derives the exact longitudinal A/e quantity which a diagonal law must
   compare;
2. it constructs an exact sourced labelled transport and classifies its kernel;
3. it proves that observer positivity can uniquely remove the harmonic/parallel
   kernel **after** that source is supplied.

What is not owned is the cross-channel comparison itself.

The fixed chart relation

\[
\Delta^v=\eta\Delta^b
\]

cannot simply be promoted to a frame-covariant vector-endomorphism law.

The current natural candidates fail, while the regular \(B^{-1}C\) passport
only covers a restricted branch and does not give a globally selected
off-orbit source.

Therefore the strongest honest terminal is

\[
\boxed{
\texttt{DIAGONAL-OVERLAP-REQUIRES-NEW-RELATIVE-AE-DEFECT}.
}
\]

This terminal is narrower than "owned geometry never selects."

It explicitly identifies the missing primitive and gives the complete finite
selection mechanism conditional on that primitive.

Finite E dressing remains blocked.

---

## 37. Exactly one recommended next step

Open one focused task to construct the **relative A/e comparison primitive**
\(\mathfrak J\) (or an equivalent edge-labelled map on \(\Delta^b\)) globally,
including the degenerate raw-solder locus.

It must satisfy:

\[
\mathfrak J'_y=g_y\mathfrak J_yg_y^{-1},
\]

\[
\mathfrak J_y\Delta^b_r=\Delta^v_r
\]

on the full exact translation-gauge orbit,

and it must extend across backgrounds where the regular passport

\[
K=B_e^{-1}C_A
\]

is unavailable or singular.

The task should use the regular passport of §30 as the positive branch, retain
the rational boost as the covariance firewall, and not reopen the already
solved sourced transport / observer-kernel algebra.

Do not start finite graded E dressing before that global relative A/e primitive
is either derived or explicitly adopted as new geometric data.
