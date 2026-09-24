# A4D labelled reference selection principle: overlap defect, observer minimality, and the missing junction primitive

**Canonical task:** \`EXP-A4D-LABELLED-REFERENCE-SELECTION-PRINCIPLE\`  
**Audited baseline:** \`398e31e9944523bcce29bf5811d58d71fe5f8a58\`  
**Research PR:** #117  
**Terminal:** \`REFERENCE-SELECTION-REQUIRES-NEW-JUNCTION-OVERLAP-PRIMITIVE\`  
**Status:** theorem-ready deep-research classification; no Lean source and no finite graded E dressing.

## 0. Result in one statement

The selector problem can now be reduced to one exact Role-labelled overlap variable.

For every site \(y\) and Role \(r\), write

\[
\delta_r(y)
:=
q_r(y)-v_r(e,y)
\in V_y.
\tag{0.1}
\]

Then

\[
q_r(y)=v_r(e,y)+\delta_r(y),
\tag{0.2}
\]

and for the incoming edge \(x\xleftarrow{\,r\,}y=x+r\),

\[
\kappa_q(A,e;x,r)
=
\tau_r(A,e;x)
+
L_{x,r}\delta_r(y),
\tag{0.3}
\]

where

\[
\boxed{
\tau_r(A,e;x)
:=
A_{x,r}\bigl(v_r(e,y)\bigr)-v_r(e,x)
=
b_{x,r}+L_{x,r}v_r(e,y)-v_r(e,x).
}
\tag{0.4}
\]

The labelled junction from an incoming Role \(r\) to an outgoing Role \(s\) at the same site \(y\) is governed by

\[
\Omega_{rs}(y)
:=
q_r(y)-v_s(e,y).
\tag{0.5}
\]

But this overlap is not new independent data:

\[
\boxed{
\Omega_{rs}
=
\bigl(v_r-v_s\bigr)+\delta_r.
}
\tag{0.6}
\]

It satisfies the exact twisted cocycle identity

\[
\boxed{
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
}
\tag{0.7}
\]

Since

\[
\Omega_{ss}=\delta_s,
\]

the whole nonselection of \(q\) is exactly the freedom in the **diagonal overlap field**

\[
\delta_r(y).
\]

The strict ordinary cocycle law

\[
\Omega_{rs}+\Omega_{st}=\Omega_{rt}
\]

would force

\[
\delta_s=0,
\qquad
q_s=v_s,
\]

which is already excluded by the exact pure-gauge witness from PR #114.

Thus the existing labelled-path algebra does not select \(q\); it only exposes where the selector must enter.

The other mandatory principle classes do not close this gap:

1. the owned positive observer form \(h_n\) supplies a canonical positive norm, but no canonical anchor/relative A/e overlap;
2. the natural observer-positive quadratic built from \(\kappa\) and normalized junction defects has an exact gauge-vs-pure-shift contradiction;
3. basepoint/tree/path fixing cannot even propagate the required \(\delta\) without a sourced overlap law, and simple parallel propagation fails an exact \(L=3\) pure-gauge witness;
4. full-affine origin covariance makes differences of affine points transform linearly, but it still leaves every admissible \(\delta\mapsto\delta+z\) deformation;
5. orbitwise equivariance likewise does not select: if one equivariant section exists, the already-constructed equivariant \(z_{\rm curl}\) and \(z_{\rm harm}\) generate more.

The strongest honest terminal is therefore

\[
\boxed{
\texttt{REFERENCE-SELECTION-REQUIRES-NEW-JUNCTION-OVERLAP-PRIMITIVE}.
}
\tag{0.8}
\]

This is not a universal nonexistence theorem.

It says that the next independent datum must prescribe the diagonal Role-labelled overlap \(\delta_r(y)\), or an equivalent junction/overlap object whose diagonal determines it, before observer minimality or path gauge fixing can become a genuine selector.

---

## 1. Frozen PR #114 nonselection theorem

The current owner stack supplies the conditional mismatch

\[
\kappa_q(A,e;x,r)
=
A_{x,r}\bigl(q_r(x+r)\bigr)-v_r(e,x),
\tag{1.1}
\]

with

\[
v_r(e,x)=\operatorname{solderLegVector}(N,e,x,r).
\]

PR #114 established:

- flat:
  \[
  q=e_r,\qquad \kappa=0;
  \]
- exact translation-gauge diagonal:
  \[
  q_r(x+r)=v_r(e,x)-b_{x,r},
  \qquad
  \kappa=0;
  \]
- pure affine shift:
  \[
  e=0,\ L=I,\ b\ne0
  \quad\Longrightarrow\quad
  q=e_r,\ \kappa=b;
  \]
- pure-linear frame covariance:
  \[
  q'_r(y)=g_yq_r(y)
  \quad\Longrightarrow\quad
  \kappa'=g_x\kappa;
  \]
- explicit conditional nonselection:
  \[
  q_{\lambda,\mu}
  =
  q+\lambda z_{\rm curl}+\mu z_{\rm harm}.
  \tag{1.2}
  \]

Both deformations vanish on flat, exact pure gauge and pure shift, while changing transverse curl/harmonic backgrounds.

The present task must therefore select among (1.2), not merely verify the old controls again.

---

## 2. Exact overlap variable

At one source site \(y\), define

\[
\delta_r(y)=q_r(y)-v_r(e,y).
\tag{2.1}
\]

This is a source-fibre vector.

Under the owned pure-linear frame action,

\[
q'_r(y)=g_yq_r(y),
\qquad
v'_r(y)=g_yv_r(y),
\]

hence

\[
\boxed{
\delta'_r(y)=g_y\delta_r(y).
}
\tag{2.2}
\]

Thus \(\delta\) is exactly the kind of vector that the observer form \(h_n\) can norm covariantly.

Equation (1.1) becomes

\[
\begin{aligned}
\kappa_q
&=
b+L(v_y+\delta)-v_x
\\
&=
\underbrace{b+Lv_y-v_x}_{\tau}
+
L\delta.
\end{aligned}
\]

Therefore

\[
\boxed{
\kappa=\tau+L\delta.
}
\tag{2.3}
\]

Selection of \(q\) and selection of \(\delta\) are equivalent.

---

## 3. Labelled junction / overlap derivation

Consider two consecutive positive labelled edges

\[
x_0
\xleftarrow{\ r\ }
x_1
\xleftarrow{\ s\ }
x_2.
\]

The PR #114 junction term is

\[
J_{rs}(x_1)
=
L_{x_0,r}\bigl(q_r(x_1)-v_s(e,x_1)\bigr).
\tag{3.1}
\]

This motivates the site overlap

\[
\boxed{
\Omega_{rs}(y)
=
q_r(y)-v_s(e,y).
}
\tag{3.2}
\]

Using \(q_r=v_r+\delta_r\),

\[
\boxed{
\Omega_{rs}
=
v_r-v_s+\delta_r.
}
\tag{3.3}
\]

Hence

\[
J_{rs}
=
L_r(v_r-v_s)
+
L_r\delta_r.
\tag{3.4}
\]

The first term is already determined by the raw solder legs.

The second term is precisely the selector freedom.

### 3.1 Exact twisted cocycle

For any Roles \(r,s,t\),

\[
\begin{aligned}
\Omega_{rs}+\Omega_{st}-\Omega_{rt}
&=
(q_r-v_s)+(q_s-v_t)-(q_r-v_t)
\\
&=
q_s-v_s
\\
&=
\delta_s.
\end{aligned}
\]

Therefore

\[
\boxed{
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
}
\tag{3.5}
\]

This is an exact algebraic identity, not a proposed physical law.

### 3.2 Ordinary cocycle is too strong

If one imposes

\[
\Omega_{rs}+\Omega_{st}=\Omega_{rt}
\]

for all Roles, then (3.5) gives

\[
\Omega_{ss}=\delta_s=0.
\]

Thus

\[
q_s=v_s
\]

for every \(s\).

PR #114 already excludes \(q=v\) on the exact translation-gauge diagonal.

Therefore:

\[
\boxed{
\text{the naive ordinary Role-overlap cocycle is incompatible with the required pure-gauge section.}
}
\tag{3.6}
\]

### 3.3 Normalizing by the owned solder transition removes q entirely

Subtract the diagonal overlap from (3.3):

\[
\Omega_{rs}-\delta_r
=
v_r-v_s.
\tag{3.7}
\]

The right side obeys the ordinary additive Role cocycle

\[
(v_r-v_s)+(v_s-v_t)=v_r-v_t.
\tag{3.8}
\]

But (3.7) contains no information selecting \(\delta\).

Thus the current geometry gives either:

- a strict cocycle that incorrectly forces \(q=v\); or
- the correct twisted cocycle, which leaves the diagonal overlap free.

This is the first precise reason the next primitive must have a **diagonal overlap law**, not merely another path append identity.

---

## 4. Flat, pure gauge and pure shift in overlap variables

### 4.1 Flat

At

\[
A=A_{\rm flat},
\qquad
e=0,
\]

one has

\[
v_r=e_r,
\qquad
q_r=e_r,
\]

therefore

\[
\boxed{
\delta_r=0.
}
\tag{4.1}
\]

Then \(\tau=0\) and \(\kappa=0\).

### 4.2 Pure affine shift

For

\[
e=0,
\qquad
L=I,
\qquad
b\ne0,
\]

the desired section is still

\[
q_r=e_r=v_r.
\]

Hence

\[
\boxed{
\delta_r=0,
\qquad
\tau=b,
\qquad
\kappa=b.
}
\tag{4.2}
\]

### 4.3 Exact translation gauge

For

\[
L=I,
\qquad
b=d_f\phi,
\qquad
e=d_f\phi,
\]

the required section is

\[
q_r(y)=v_r(e,x)-b_{x,r},
\qquad y=x+r.
\]

Therefore

\[
\boxed{
\delta_r(y)
=
v_r(e,x)-b_{x,r}-v_r(e,y).
}
\tag{4.3}
\]

This is generically nonzero.

The exact cancellation condition is

\[
\kappa=\tau+\delta=0,
\]

so

\[
\boxed{
\delta=-\tau
}
\tag{4.4}
\]

on the exact pure-gauge diagonal.

Thus the selector must distinguish:

- pure shift: \(\delta=0\);
- exact gauge: \(\delta=-\tau\).

The observer norm alone does not encode that distinction.

---

## 5. Exact L=3 pure-gauge overlap witness

Use the PR #114 periodic \(A\)-direction witness with internal \(B\) component

\[
b_A=(3,3,-6)e_B.
\tag{5.1}
\]

Since \(B\) is spacelike,

\[
v_A=e_A-\bigl(3,3,-6\bigr)e_B,
\]

so the \(B\)-coordinates of the three target solder legs are

\[
(-3,-3,6).
\tag{5.2}
\]

The required pure-gauge source references have \(B\)-coordinates

\[
(12,-6,-6)
\tag{5.3}
\]

at the three source sites.

Therefore the diagonal overlaps have \(B\)-coordinates

\[
\boxed{
(15,-3,-12).
}
\tag{5.4}
\]

They satisfy

\[
15-3-12=0
\]

but are not constant.

This witness will be used repeatedly below.

---

## 6. Basepoint / path parallel propagation fails before any minimization

A natural basepoint attempt is:

1. choose \(o\);
2. choose \(\delta_r(o)\);
3. transport it by the owned linear path transport.

On the exact translation-gauge chart,

\[
L=I.
\]

Any such parallel transport therefore makes \(\delta_r\) constant along the connected archive.

But the exact pure-gauge witness (5.4) requires

\[
\delta_A=(15,-3,-12)e_B,
\]

which is not constant.

Hence:

\[
\boxed{
\text{a basepoint value plus homogeneous path transport cannot reproduce the required pure-gauge overlap.}
}
\tag{6.1}
\]

A sourced propagation law is required.

That source term is exactly a new overlap/junction law.

Therefore basepoint/path fixing is logically **downstream** of the missing local primitive.

---

## 7. Exact observer-positive metric input

The owned observer form is

\[
h_n
=
-\eta+2n^\flat\otimes n^\flat.
\tag{7.1}
\]

For every Lorentz-unit observer \(n\),

\[
h_n
\]

is strictly positive definite.

At the rest observer,

\[
h_{n_0}=I.
\tag{7.2}
\]

Under an allowed Lorentz frame,

\[
n'=gn,
\qquad
u'=gu,
\]

the observer form transforms by inverse congruence, so

\[
h_{n'}(gu,gu)=h_n(u,u).
\tag{7.3}
\]

Thus \(h_n\) is a legitimate positive norm for \(\delta,\kappa\), junction defects and any covariant vector built from them.

This is strong metric input.

It is not yet a selection principle.

---

## 8. Observer-positive minimality: the canonical local quadratic

The first variational principle to test is the one requiring no new target vector:

\[
\boxed{
\mathcal E_{\alpha,\beta}(\delta)
=
\alpha\,\|\kappa\|_{h_n}^2
+
\beta\,\|\delta\|_{h_n}^2,
\qquad
\alpha,\beta\ge0.
}
\tag{8.1}
\]

The second term is exactly the positive normalized-junction penalty.

Indeed from (3.3),

\[
\Omega_{rs}-(v_r-v_s)=\delta_r.
\tag{8.2}
\]

Summing this over all outgoing \(s\) only multiplies \(\|\delta_r\|^2\) by the number of Roles.

No new geometry is introduced by writing the junction term explicitly.

### 8.1 Exact one-edge minimizer at rest

On the exact \(L=3\) equal-neighbour pure-gauge edge from PR #114,

\[
L=I,
\qquad
v_y=v_x,
\qquad
\tau=b\ne0.
\]

At the rest observer \(h_n=I\),

\[
\kappa=b+\delta.
\]

The quadratic is

\[
\mathcal E_{\alpha,\beta}
=
\alpha\|b+\delta\|^2
+
\beta\|\delta\|^2.
\]

If

\[
\alpha+\beta>0,
\]

the unique minimizer is

\[
\boxed{
\delta_*
=
-\frac{\alpha}{\alpha+\beta}\,b,
}
\tag{8.3}
\]

and

\[
\boxed{
\kappa_*
=
\frac{\beta}{\alpha+\beta}\,b.
}
\tag{8.4}
\]

### 8.2 Pure-gauge requirement forces beta = 0

Exact pure-gauge cancellation requires

\[
\delta_*=-b,
\qquad
\kappa_*=0.
\]

Equations (8.3)–(8.4) force

\[
\boxed{\beta=0.}
\tag{8.5}
\]

### 8.3 Pure-shift visibility then fails

On a pure affine shift with the same nonzero vector \(b\),

\[
L=I,
\qquad
e=0,
\qquad
\tau=b.
\]

With \(\beta=0\), the minimizer is again

\[
\delta_*=-b,
\]

so

\[
\boxed{
\kappa_*=0.
}
\tag{8.6}
\]

This violates pure-shift visibility.

Conversely, \(\alpha=0\) gives

\[
\delta_*=0,
\qquad
\kappa=b,
\]

which is correct for pure shift but fails exact pure gauge.

For \(\alpha,\beta>0\), both sectors are interpolated and exact pure-gauge cancellation fails.

Therefore:

\[
\boxed{
\text{no background-independent positive combination of }
\|\kappa\|_{h_n}^2
\text{ and normalized junction norm }
\|\delta\|_{h_n}^2
\text{ closes the mandatory controls.}
}
\tag{8.7}
\]

This is a scoped variational no-go, not a no-go for every possible nonlinear functional.

---

## 9. Why \(h_n\) does not supply the missing coefficient

The key point in (8.7) is not a lack of positivity.

The observer metric already proves strict convexity whenever both coefficients are positive.

The problem is that positivity cannot decide **which background is diagonal gauge and which is independent affine shift**.

On the hostile pair:

- exact equal-neighbour pure gauge;
- pure affine shift,

the local relation between the two optimized vectors is the same:

\[
\kappa=b+\delta.
\tag{9.1}
\]

But the required minima differ:

\[
\delta=-b
\]

versus

\[
\delta=0.
\]

A selector must therefore contain another A/e-relative datum.

The observer field \(n\) can be chosen identical in the two controls.

Hence \(h_n\) cannot provide that datum by itself.

---

## 10. Optional curl/harmonic penalties do not repair the local contradiction automatically

The task allows optional positive penalties for curl/harmonic data.

Two cases must be separated.

### 10.1 Background-only penalties

If a term depends only on the background and not on \(q\), adding it to \(\mathcal E\) does not change the minimizing \(\delta\).

It cannot select \(q\).

### 10.2 q-dependent transverse penalties

A term that depends on a derivative or cycle of \(\delta\) can change the minimizer.

But then one must specify:

- which derivative/overlap operator acts on \(\delta\);
- which target value it should approach;
- how path junctions enter;
- how harmonic cycles are anchored;
- its relative coefficient against the local \(\kappa\) term.

None of those is supplied by \(h_n\).

Choosing them to remove the known \(z_{\rm curl}\) and \(z_{\rm harm}\) directions would simply insert the missing selector by hand.

Thus \(h_n\) gives a norm **after** the overlap law is known; it does not derive the overlap law.

---

## 11. Existing solder parallel defect is not the selector

The repository owns

\[
\operatorname{archiveAffineSolderParallelDefect}.
\]

At flat \(A\), the \(L=2\) Nyquist witness gives exactly

\[
4.
\tag{11.1}
\]

This proves that current raw geometry sees the alternating solder field.

However this object is:

- a finite difference of the raw coframe row;
- independent of the affine shift \(b\);
- not the exact diagonal relation selecting \(\delta\);
- not an owned full frame-covariant A/e comparison.

In particular, a pure-gauge coframe can have nonzero solder variation.

Penalizing this defect with a positive coefficient would generically pull away from the required exact pure-gauge \(\kappa=0\) solution unless another cross term compensates it.

That compensation is again a new relative A/e rule.

---

## 12. The L=2 truth firewall for any selector

The owned period-two witness has

\[
e_A{}^A=(-2,+2),
\]

while its centered solder readout vanishes.

At flat affine connection,

\[
\operatorname{archiveAffineSolderParallelDefect}=4.
\]

Therefore a valid selector must not factor only through:

- centered coframe;
- affine curvature;
- endpoint descent;
- a background-independent local \(q=v\) rule.

The raw alternating datum is genuine.

Any principle that sets

\[
\kappa=0
\]

whenever affine holonomy is trivial is also invalid: the flat connection has trivial affine holonomy while the Nyquist coframe remains nonparallel and must remain distinguishable.

This is an important obstruction to “use only connection holonomy to decide gauge-vs-shift”.

---

## 13. L=3 corner/curl control

Take flat affine connection and one raw off-diagonal coframe component

\[
e_A{}^B(0)=1.
\]

The PR #114 solder curl satisfies

\[
C_{AB}(0)=-e_B\ne0.
\tag{13.1}
\]

The deformation

\[
z_{\rm curl}
=
L^{-1}C
\]

is source-vector covariant and vanishes on all old normalization sectors.

A selector that uses only:

- local \(\kappa\) norm;
- the tautological twisted overlap identity;
- full-affine covariance;

still admits

\[
\delta\mapsto\delta+\lambda z_{\rm curl}.
\]

To reject this family, the new overlap primitive must impose a nontrivial local equation on \(\delta\).

Neither append/reverse path algebra nor \(h_n\)-positivity supplies such an equation.

---

## 14. Harmonic control and why purely local selection is insufficient

PR #114 gives a constant harmonic coframe witness

\[
e_A{}^B=1
\]

with flat affine connection.

The solder leg is constant in space.

For the local source-solder choice

\[
\delta=0,
\qquad
q=v,
\]

one has

\[
A(v_y)-v_x=0,
\]

hence

\[
\kappa=0.
\]

Thus every purely local principle whose unique zero is

\[
\kappa=0,\qquad \delta=0
\]

is blind to this nonzero harmonic coframe.

The explicit deformation

\[
z_{\rm harm}
=
\chi\,v_r
\]

shows the same nonselection covariantly.

Therefore a successful selector requires a global cycle/overlap condition in addition to local junction data.

---

## 15. Basepoint, spanning tree and path gauge fixing

A basepoint/path rule can address global integration freedom only after a local propagation law exists.

### 15.1 A basepoint alone is insufficient

As shown in §6, homogeneous path propagation fails the exact pure-gauge witness because required \(\delta\) is not parallel-constant even when \(L=I\).

### 15.2 A spanning tree without a source law is only a list of paths

The existing labelled path skeleton supplies:

- endpoints;
- append;
- reversal;
- exact holonomy provenance.

It does not supply an equation

\[
\delta(y')-\mathcal P_{y\to y'}\delta(y)
=
\text{source}(A,e).
\tag{15.1}
\]

Without the right side of (15.1), a tree cannot determine the required section.

### 15.3 A sourced tree law is a new overlap primitive

Once a source is specified, one can integrate it along a chosen tree.

But then:

- changing the tree changes the result on curl backgrounds;
- changing cycle representatives changes harmonic anchoring;
- nontrivial labelled holonomy cannot be quotiented.

Therefore the tree/path family must be recorded as additional selector data unless the source law proves path independence.

### 15.4 Canonical-looking coordinate paths are still a gauge choice

The archive group has a distinguished algebraic zero and labelled Role directions.

One can therefore write a lexicographic path family.

But using that family as the physical reference assignment is an additional gauge-fixing rule.

The current geometric owners do not prove that the result is independent of that choice on nontrivial holonomy backgrounds.

Hence basepoint/path gauge fixing is a possible **post-primitive completion**, not the primitive itself.

---

## 16. Full affine origin structure

PR #115 Lean-owns the exact statement:

if both source reference and target solder are affine points,

\[
q'_y=h_y(q_y),
\qquad
v'_x=h_x(v_x),
\]

then

\[
A'(q')-v'
=
g_x(A(q)-v).
\tag{16.1}
\]

If the reference transforms affinely but the solder only linearly, the residual node translation is

\[
c_x.
\tag{16.2}
\]

### 16.1 Difference variable under a true full-affine point law

If both \(q_r(y)\) and \(v_r(y)\) are affine points transformed by the same node map, then

\[
\delta_r(y)=q_r(y)-v_r(y)
\]

transforms linearly:

\[
\delta'_r=g_y\delta_r.
\tag{16.3}
\]

This is elegant.

It makes the overlap variable geometrically natural.

### 16.2 It still does not select delta

For every linearly covariant \(z_r(y)\),

\[
(q+z)'=h(q+z)
\]

whenever \(q'=h(q)\) and \(z'=gz\).

Therefore both PR #114 deformations remain admissible:

\[
\delta\mapsto\delta+\lambda z_{\rm curl},
\]

\[
\delta\mapsto\delta+\mu z_{\rm harm}.
\]

Thus:

\[
\boxed{
\text{full-affine origin covariance repairs transformation law but does not select the diagonal overlap.}
}
\tag{16.4}
\]

A full affine origin action is not the earliest selector.

---

## 17. Affine-origin overlap/cocycle does not remove the diagonal freedom

Suppose one upgrades \(\Omega_{rs}\) to a difference of affine points.

Differences of affine points are vectors, so equations (3.3)–(3.5) remain valid.

The exact twisted cocycle still has diagonal

\[
\Omega_{rr}=\delta_r.
\]

Therefore the affine torsor language changes the covariance interpretation but not the selection algebra.

To eliminate \(z_{\rm curl}\) and \(z_{\rm harm}\), one must add a law fixing \(\Omega_{rr}\).

This is precisely the missing primitive identified by the terminal.

---

## 18. Orbitwise / equivariant selection

Could one choose \(q\) by selecting one representative on every frame orbit?

In principle, a set-theoretic construction could proceed:

1. choose an orbit representative of \((A,e,n)\);
2. choose one admissible \(q\) there;
3. transport \(q\) equivariantly.

This faces stabilizer consistency and is not guaranteed to exist for arbitrary choices.

More importantly for selection:

if \(q\) is equivariant and

\[
z_{\rm curl},
\qquad
z_{\rm harm}
\]

are equivariant, then

\[
q+\lambda z_{\rm curl}+\mu z_{\rm harm}
\]

is equivariant as well.

Therefore equivariance alone cannot select one section.

Choosing orbit representatives and one value on each orbit is additional noncanonical data.

It is not an intrinsic consequence of the owned geometry.

---

## 19. Fixed-coordinate diagonal projection is not frame covariant

In one fixed archive coordinate chart one can write the obvious normal coordinate between translation and coframe:

\[
b-e_{\rm row}.
\tag{19.1}
\]

It has exactly the desired intuition:

- zero on the translation-gauge diagonal;
- nonzero on a pure affine shift;
- nonzero on coframe-only Nyquist/corner/harmonic backgrounds.

But PR #109/#112 already establish why this is not a geometric selector.

The raw perturbation does not transform homogeneously:

\[
e'
=
(\eta+e)\Lambda-\eta.
\tag{19.2}
\]

The full solder row transforms, not \(e\) by itself.

Hence (19.1) is not a vector-frame law.

### 19.1 Observer positivity does not repair the inhomogeneous background subtraction

One may try to use \(h_n\) to raise the raw row.

But the obstruction is earlier:

the perturbation \(e\) itself is not a tensor under the active full-solder frame action.

A positive row-to-vector map cannot make the subtraction of the fixed flat row \(\eta\) equivariant.

A transformed reference frame/tetrad would be needed.

That is another presentation of the same missing overlap datum.

---

## 20. Rational A/B boost control

Use the exact rational boost

\[
g=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

The owned observer transforms to

\[
n'=gn
\]

and the observer form satisfies

\[
h_{n'}(gu,gv)=h_n(u,v).
\tag{20.1}
\]

For every covariant overlap variable,

\[
\delta'=g\delta,
\qquad
\kappa'=g\kappa,
\]

so the quadratic functional (8.1) is exactly invariant.

This confirms that the failure of (8.1) is not a frame-covariance failure.

It is a **selection failure**.

The rational boost therefore strengthens, rather than weakens, the terminal:

even an exactly covariant positive functional still needs the missing relative A/e overlap rule.

---

## 21. Why affine holonomy penalties are insufficient

A pure affine shift has nontrivial cycle translation and an exact translation gauge of flat has trivial affine holonomy.

This suggests weighting the observer functional by affine cycle data.

Such a term can distinguish those two sectors.

But it does not solve the full task.

### 21.1 Flat coframe-only Nyquist

For

\[
A=A_{\rm flat}
\]

the affine holonomy is trivial.

Yet the raw \(L=2\) Nyquist coframe has nonzero parallel defect \(4\).

A selector that turns off its regularization whenever affine holonomy is trivial can erase the Nyquist datum.

### 21.2 Flat harmonic coframe

The constant harmonic coframe also has flat affine holonomy.

Nevertheless it must remain distinguishable.

Therefore a successful weight must depend on a **relative** A/e defect, not on affine holonomy alone.

Constructing that relative defect is the original selector problem.

---

## 22. Why solder curl/harmonic penalties alone are insufficient

The converse strategy uses only coframe transverse invariants.

It also fails to distinguish the required sectors.

The exact gauge diagonal can have nonzero local solder variation even though it is physically to satisfy

\[
\kappa=0.
\]

Thus a positive penalty on raw solder variation alone generically moves away from the required pure-gauge solution.

To know which part of the solder variation is compensated by affine translation, the functional needs a relative A/e overlap law.

Again the missing input is not positivity.

It is the cross-channel comparison.

---

## 23. Junction primitive: minimal exact type

The research now identifies the smallest useful new object.

Introduce a Role-labelled overlap field

\[
\boxed{
\Omega_N(A,e,n;y;r,s)\in V_y
}
\tag{23.1}
\]

with the intended meaning

\[
\Omega_{rs}=q_r-v_s.
\]

It must satisfy:

### 23.1 Source-frame covariance

\[
\Omega(A^g,e^g,n^g;y;r,s)
=
g_y\Omega(A,e,n;y;r,s).
\tag{23.2}
\]

### 23.2 Solder-difference compatibility

For fixed \(r\),

\[
\boxed{
\Omega_{rs}-\Omega_{rt}
=
v_t-v_s.
}
\tag{23.3}
\]

This guarantees that

\[
q_r
=
v_s+\Omega_{rs}
\]

is independent of the chosen outgoing label \(s\).

### 23.3 Twisted Role cocycle

\[
\boxed{
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
}
\tag{23.4}
\]

### 23.4 Diagonal selector

The genuinely new law is a rule fixing

\[
\boxed{
\delta_r(y)=\Omega_{rr}(y).
}
\tag{23.5}
\]

The old geometry supplies (23.2)–(23.4) conditionally.

It does **not** supply (23.5).

This is why the terminal names the missing datum a **junction-overlap primitive** rather than a generic new \(q\).

---

## 24. Acceptance contract for the future diagonal overlap law

A successful primitive must force:

### Flat

\[
\delta_r=0.
\tag{24.1}
\]

### Exact translation gauge

\[
\delta_r(y)
=
v_r(e,y-r)-b_{y-r,r}-v_r(e,y).
\tag{24.2}
\]

### Pure affine shift

\[
\delta_r=0.
\tag{24.3}
\]

### Curl sector

It must forbid

\[
\delta\mapsto\delta+\lambda z_{\rm curl}
\]

unless \(\lambda=0\).

### Harmonic sector

It must forbid

\[
\delta\mapsto\delta+\mu z_{\rm harm}
\]

unless \(\mu=0\).

### Path compatibility

For the junction \(r\to s\),

\[
J_{rs}
=
L_r\Omega_{rs}
\]

must be used explicitly.

No endpoint quotient is allowed.

### Full-affine option

If a future affine solder action is adopted, \(\Omega\) must remain a vector difference of affine points.

---

## 25. Curl deformation test against the audited principles

### Naive strict cocycle

Rejects all nonzero \(\delta\), including required pure gauge.

Invalid.

### Twisted cocycle

Allows every \(\delta+z_{\rm curl}\).

Does not select.

### Observer-positive local quadratic

Can penalize \(z_{\rm curl}\), but the same positive junction anchor causes the gauge-vs-shift contradiction of §8.

Does not close.

### Basepoint homogeneous propagation

Cannot reproduce the required varying pure-gauge \(\delta\).

Invalid.

### Full affine covariance

\(z_{\rm curl}\) transforms correctly and remains allowed.

Does not select.

### Orbitwise equivariance

\(q+\lambda z_{\rm curl}\) is equally equivariant.

Does not select.

Therefore none of the currently owned principle classes rejects \(z_{\rm curl}\) while preserving all mandatory controls.

---

## 26. Harmonic deformation test against the audited principles

### Local junction/cocycle algebra

A constant harmonic coframe can have

\[
\delta=0,\qquad \kappa=0
\]

for the source-solder local zero.

No local cocycle detects that the coframe has a nonzero global cycle.

Insufficient.

### Observer-positive local quadratic

Same blindness.

Insufficient.

### Basepoint/path family

Can make a harmonic choice, but only after:

- a sourced transport/overlap law is known;
- a path/tree/cycle representative is selected.

This is additional datum.

### Full affine covariance

\(z_{\rm harm}\) is still covariant.

Does not select.

### Orbitwise equivariance

\(q+\mu z_{\rm harm}\) remains equivariant.

Does not select.

Therefore the harmonic family also survives all currently owned selector ingredients.

---

## 27. L=2 / L=3 / curl / harmonic truth table

| Sector | Required visibility | Audited result |
|---|---|---|
| Flat \(A,e=0\) | \(q=e_r,\ \kappa=0\) | compatible with \(\delta=0\) |
| Exact pure gauge | \(\kappa=0\) | requires nontrivial \(\delta=-\tau\) |
| Pure affine shift | \(\kappa\ne0\), preferably \(b\) | requires \(\delta=0\) |
| L=2 raw Nyquist, flat A | remain visible | affine holonomy alone cannot select it; raw defect \(=4\) |
| L=3 off-diagonal corner | remain visible | \(z_{\rm curl}\) changes it; current overlap identities do not fix coefficient |
| Plaquette curl | remain visible | local new diagonal-overlap equation required |
| Harmonic cycle | remain visible | global cycle/overlap law required |
| Nontrivial labelled holonomy | retain provenance | no endpoint quotient permitted |

The table shows why neither a purely local principle nor a purely global gauge fixing is enough by itself.

---

## 28. Exact finite checker

A standalone exact-rational checker passed **36/36 assertions**.

It checked:

1. the exact twisted overlap cocycle;
2. extraction of the diagonal defect from the cocycle failure;
3. normalization of overlap by \(\delta_r\) gives the owned solder Role difference;
4. a nonzero diagonal defect breaks the ordinary cocycle;
5. the ordinary cocycle is restored exactly when the diagonal defect is zero in the control;
6. the \(L=3\) pure-gauge shift cycle \(3+3-6=0\);
7. the first two pure-gauge solder legs coincide;
8. the exact pure-gauge source-reference values are \((12,-6,-6)\) in the checked \(B\) coordinate;
9. the required diagonal overlaps are \((15,-3,-12)\);
10. their sum is zero;
11. they are not constant under \(L=I\);
12. the first exact gauge edge has \(\kappa=0\);
13. the source-solder choice on the same edge leaves \(\kappa=3e_B\);
14–22. three independent positive coefficient pairs in the observer quadratic have the exact interior minimizer (8.3), with neither \(\delta=-b\) nor \(\kappa=0\);
23–24. \(\beta=0\) gives exact gauge cancellation and erases pure shift;
25–26. \(\alpha=0\) keeps pure shift and fails pure gauge;
27. two zero flat mixed-Role edge mismatches compose to zero;
28. the flat mixed-Role junction defect is \(e_A-e_B\ne0\);
29. the endpoint term is its negative;
30. endpoint plus junction cancels exactly;
31. a constant harmonic solder leg gives zero local parallel difference;
32. that solder leg is nevertheless nonzero;
33. the L=2 Nyquist local solder variation is \(4e_A\);
34. its squared counting norm is \(16\);
35. difference of two fully translated affine points cancels the translation;
36. linear-only solder transformation leaves the exact translation residual.

All arithmetic is exact \`Fraction\` arithmetic; no floating tolerance is used.

---

## 29. Theorem-ready handoff

The following statements are research-theorem-ready.

### Theorem A — overlap decomposition

Define

\[
\delta_r=q_r-v_r,
\qquad
\Omega_{rs}=q_r-v_s.
\]

Then

\[
\Omega_{rs}=v_r-v_s+\delta_r.
\]

### Theorem B — twisted overlap cocycle

For all Roles,

\[
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
\]

### Theorem C — strict cocycle obstruction

If

\[
\Omega_{rs}+\Omega_{st}=\Omega_{rt}
\]

for all labels, then

\[
q_s=v_s
\]

for every \(s\).

Hence the strict cocycle cannot satisfy the generic exact pure-gauge reference condition.

### Theorem D — mismatch in diagonal-overlap variables

For \(y=x+r\),

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(v_r(e,y))-v_r(e,x)
+
L_{x,r}\delta_r(y).
\]

### Theorem E — exact L=3 gauge overlap is nonparallel

For the periodic pure-gauge witness with \(B\)-shift cycle

\[
(3,3,-6),
\]

the required diagonal overlap values are

\[
(15,-3,-12)e_B.
\]

Therefore homogeneous basepoint/path transport cannot generate the required section even though \(L=I\).

### Theorem F — observer-positive local quadratic minimizer

At \(L=I\), rest observer, and a control with

\[
\kappa=b+\delta,
\]

the functional

\[
\alpha\|\kappa\|^2+\beta\|\delta\|^2
\]

has unique minimizer

\[
\delta_*=-\frac{\alpha}{\alpha+\beta}b
\]

whenever \(\alpha+\beta>0\).

### Theorem G — observer quadratic gauge/shift incompatibility

Exact pure gauge forces \(\beta=0\), which then gives \(\kappa=0\) on a pure affine shift.

Hence no background-independent positive \((\alpha,\beta)\) closes both controls.

### Theorem H — basepoint propagation boundary

A basepoint plus homogeneous linear path transport cannot select the required \(\delta\).

A sourced overlap transport equation is logically prior.

### Theorem I — full-affine covariance does not select

If both \(q\) and \(v\) are promoted to affine points, \(\delta=q-v\) transforms linearly.

Every linearly covariant deformation \(z\) can still be added.

Thus full affine covariance leaves PR #114 nonselection intact.

### Theorem J — equivariance does not select

If \(q\), \(z_{\rm curl}\), and \(z_{\rm harm}\) are equivariant, then so is

\[
q+\lambda z_{\rm curl}+\mu z_{\rm harm}.
\]

Frame equivariance alone cannot select the section.

### Theorem K — minimum new primitive

A Role-labelled overlap field \(\Omega_{rs}\) satisfying source-frame covariance, solder-difference compatibility and the twisted cocycle determines \(q\) if and only if its diagonal

\[
\delta_r=\Omega_{rr}
\]

is specified.

Therefore the genuinely new selection datum is the diagonal overlap law.

---

## 30. Why the terminal is the junction/overlap primitive

The current repo owns:

- positive observer geometry;
- linear and affine path transport;
- labelled append/reverse/holonomy;
- conditional \(\kappa_q\);
- full-affine covariance boundary;
- raw solder data;
- explicit curl and harmonic nonselection witnesses.

What it does not own is a law saying which diagonal overlap

\[
q_r(y)-v_r(e,y)
\]

belongs to one Role-labelled edge.

Every tested selector class fails for a precise reason:

- strict cocycle is too strong;
- twisted cocycle is tautological;
- \(h_n\)-minimality has no relative anchor and gives the exact gauge/shift conflict;
- basepoint transport lacks a source law;
- tree/path fixing is extra data and is downstream of that source law;
- full-affine covariance leaves linear deformations untouched;
- equivariant orbit selection remains nonunique;
- local principles miss harmonic data;
- holonomy-only global principles miss raw Nyquist/coframe-only data.

Therefore the strongest scoped terminal is

\[
\boxed{
\texttt{REFERENCE-SELECTION-REQUIRES-NEW-JUNCTION-OVERLAP-PRIMITIVE}.
}
\]

This does not say such a primitive cannot be derived later.

It says it is not currently forced by \(A,e,n,h_n\) plus labelled path algebra.

---

## 31. Exactly one recommended next step

Open one focused research task to derive or explicitly postulate the **diagonal junction-overlap law**

\[
\boxed{
\delta_N(A,e,n;y,r)
=
\Omega_N(A,e,n;y;r,r),
}
\]

together with its sourced path-transport equation.

That task should require, before any finite E dressing:

\[
\delta_{\rm flat}=0,
\]

\[
\delta_{\rm pure\ gauge}
=
v_r(e,y-r)-b_{y-r,r}-v_r(e,y),
\]

\[
\delta_{\rm pure\ shift}=0,
\]

and exact rejection of both

\[
z_{\rm curl},
\qquad
z_{\rm harm}.
\]

Only after that diagonal overlap law is owned should \(h_n\)-minimality or a basepoint/tree choice be used to solve any remaining finite-dimensional global integration freedom.
