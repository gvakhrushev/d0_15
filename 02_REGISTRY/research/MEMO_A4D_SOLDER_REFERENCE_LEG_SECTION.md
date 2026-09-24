# A4D solder reference-leg section: candidate exhaustion, path junctions, and nonselection

**Canonical task:** \`EXP-A4D-SOLDER-REFERENCE-LEG-SECTION\`  
**Audited baseline:** \`8c365722bb3b7e19408fbba836fb16cd0203e8f5\`  
**Research PR:** #114  
**Terminal:** \`SOLDER-REFERENCE-LEG-REQUIRES-NEW-GEOMETRIC-SELECTION-PRINCIPLE\`  
**Status:** theorem-ready deep-research classification; no Lean source and no finite graded E dressing.

## 0. Terminal verdict

PR #112 reduced the B/E seam to one typed question.  For a positive Role edge

\[
y=x+r,
\qquad
A_{x,r}=(L_{x,r},b_{x,r}):V_y\to_{\rm aff}V_x,
\]

the owned raw solder already gives

\[
v_r(e,x)=\operatorname{solderLegVector}(N,e,x,r)\in V_x.
\]

For any supplied source reference leg

\[
q_r(y)\in V_y
\]

the conditional mismatch is

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(q_r(y))-v_r(e,x)
=
b_{x,r}+L_{x,r}q_r(y)-v_r(e,x).
\tag{0.1}
\]

The present task asks whether current D0 selects

\[
q_N(A,e;y,r)
\]

intrinsically.

The answer is narrower than a universal no-go and stronger than “we have not guessed the formula”:

1. several natural local candidate classes are excluded exactly;
2. a constant source/target/shift linear ansatz is terminally incompatible with the simultaneous exact pure-gauge and nonzero pure-shift controls;
3. an affine inverse target-predecessor choice is tautological and erases every mismatch;
4. a single node affine origin cannot replace the Role-labelled section;
5. labelled path composition exposes an unavoidable junction defect, so \(q\) is intrinsically an **edge-labelled/path-resolved source reference**, not an endpoint-only origin;
6. a full affine solder/origin action would repair covariance under node translations, but it still would not select \(q\);
7. even if one admissible \(q\) is supplied, current owners leave explicit frame-covariant deformations
   \[
   q_{\lambda,\mu}=q+\lambda z_{\rm curl}+\mu z_{\rm harm}
   \tag{0.2}
   \]
   that preserve flat, exact pure-gauge, pure-shift and pure-linear frame controls while changing generic curl and harmonic backgrounds.

Therefore current \((A,e)\) data do not select a unique intrinsic section, and the candidate audit does not justify a universal impossibility theorem for every conceivable nonlocal/orbitwise section.

The strongest honest terminal is

\[
\boxed{
\texttt{SOLDER-REFERENCE-LEG-REQUIRES-NEW-GEOMETRIC-SELECTION-PRINCIPLE}.
}
\tag{0.3}
\]

A full affine solder/origin action is an additional covariance structure if desired, not the missing selector by itself.

---

## 1. Exact type contract

Fix

\[
X=X_N=\operatorname{ArchiveRolePhaseGroup}N,
\qquad
V=\operatorname{RoleSpace}=\operatorname{Role}\to\mathbb R.
\]

For \(y=x+r\),

\[
A_{x,r}:V_y\to_{\rm aff}V_x,
\qquad
A_{x,r}(z)=L_{x,r}z+b_{x,r}.
\]

The raw coframe row is

\[
e(x,r,\cdot),
\]

the full raw solder row is

\[
E_r(e,x)=\eta_r+e(x,r,\cdot),
\]

and the already-owned row-to-vector conversion is

\[
v_r(e,x)=\eta E_r(e,x)^T\in V_x.
\tag{1.1}
\]

No additional raise/lower map is introduced in this memo.

The sought section is Role-labelled and source-typed:

\[
\boxed{
q_N(A,e;y,r)\in V_y.
}
\tag{1.2}
\]

The predecessor is literal and unique:

\[
x=y-r.
\]

Thus a rule may use the edge \(A_{y-r,r}\), the target solder \(v_r(e,y-r)\), the source solder \(v_r(e,y)\), and additional path/cell data, while remaining source-typed.

The intrinsic mismatch would then be

\[
\boxed{
\kappa_N(A,e;x,r)
=
A_{x,r}\bigl(q_N(A,e;x+r,r)\bigr)-v_r(e,x).
}
\tag{1.3}
\]

---

## 2. Frozen normalization equations

Any accepted section must satisfy all three equations below.

### 2.1 Flat

For

\[
A=A_{\rm flat},
\qquad
e=0,
\]

one must have

\[
\boxed{
q(A_{\rm flat},0;y,r)=e_r.
}
\tag{2.1}
\]

Since \(A_{\rm flat}=I\) and \(v_r(0,x)=e_r\),

\[
\kappa(A_{\rm flat},0;x,r)=0.
\tag{2.2}
\]

### 2.2 Exact translation-gauge chart

On the owned chart

\[
L=I,
\qquad
b=d_f\phi,
\qquad
e=d_f\phi,
\]

PR #112 proves that exact cancellation is equivalent to

\[
\boxed{
q(A_\phi,d_f\phi;x+r,r)
=
v_r(d_f\phi,x)-b_{x,r}.
}
\tag{2.3}
\]

Then

\[
\kappa(A_\phi,d_f\phi;x,r)=0.
\tag{2.4}
\]

The fixed-coordinate rewrite

\[
q=e_r+(\eta-I)b
\tag{2.5}
\]

is only a chart check.  It is not used as a global frame-covariant definition.

### 2.3 Pure affine shift

For

\[
e=0,
\qquad
L=I,
\qquad
b\ne0,
\]

the section must not absorb the translation.  The strongest natural normalization is

\[
q=e_r,
\]

giving

\[
\boxed{
\kappa((I,b),0;x,r)=b\ne0.
}
\tag{2.6}
\]

At minimum \(\kappa\) must remain nonzero.

---

## 3. Pure-linear frame covariance

Let the owned right solder frame be \(\Lambda_x\), with vector frame

\[
g_x=\Lambda_x^{-1}.
\]

For a pure-linear affine node gauge,

\[
L'_{x,r}
=
g_xL_{x,r}g_y^{-1},
\qquad
b'_{x,r}=g_xb_{x,r},
\tag{3.1}
\]

and the solder vector obeys

\[
v'_r(e',x)=g_xv_r(e,x).
\tag{3.2}
\]

Therefore the required section law is

\[
\boxed{
q(A^g,e^g;y,r)=g_yq(A,e;y,r).
}
\tag{3.3}
\]

Equation (1.3) then gives

\[
\boxed{
\kappa(A^g,e^g;x,r)=g_x\kappa(A,e;x,r).
}
\tag{3.4}
\]

This remains the exact covariance target throughout the candidate audit.

---

## 4. Exact rational A/B boost control

Use the vector boost

\[
g=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix},
\]

with right-row inverse

\[
\Lambda=
\begin{pmatrix}
5/3&-4/3&0&0\\
-4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}.
\]

Exact arithmetic gives

\[
g\Lambda=\Lambda g=I,
\qquad
g^T\eta g=\eta,
\qquad
\eta\Lambda^T=g\eta.
\tag{4.1}
\]

For the PR #112 chart witness

\[
r=A,
\qquad
b=e_B,
\]

one has

\[
v_A=e_A-e_B,
\qquad
q_A=v_A-b=e_A-2e_B.
\]

After the boost,

\[
b'=
\left(\frac43,\frac53,0,0\right),
\]

\[
v'=
\left(\frac13,-\frac13,0,0\right),
\]

\[
q'=(-1,-2,0,0),
\]

and exactly

\[
v'-q'=b'.
\tag{4.2}
\]

Thus a genuine section must transport \(q\) as a source vector.  Recomputing the chart formula (2.5) in the boosted fixed basis gives a different answer and is not a covariant construction.

---

## 5. Candidate class I: fixed flat reference

The first candidate is

\[
q_r(y)=e_r.
\tag{5.1}
\]

It passes flat normalization and pure-shift visibility.

On the exact translation-gauge chart,

\[
v_r=e_r+\eta b,
\]

so

\[
\kappa=b+e_r-v_r
=
b-\eta b.
\tag{5.2}
\]

For spacelike \(b\),

\[
\kappa\ne0.
\]

It therefore fails the exact pure-gauge diagonal.

In addition, (5.1) is not a source-vector covariance law under a general active local Lorentz frame.

This candidate is excluded.

---

## 6. Candidate class II: source solder

Take

\[
q_r(y)=v_r(e,y).
\tag{6.1}
\]

This is perfectly source-typed and obeys the correct pure-linear frame law.

It fails exact pure gauge.

A simple \(L=3\) witness uses an \(A\)-dependent potential with one internal \(B\) component

\[
\phi^B=(0,1,2)
\]

around the \(A\) cycle.  With the owned forward scale, the consecutive \(A\)-edge strains are

\[
(3,3,-6)e_B.
\]

On the first edge,

\[
b=3e_B,
\]

while the two adjacent solder legs coincide:

\[
v_A(x)=v_A(x+A)=e_A-3e_B.
\]

Therefore (6.1) gives

\[
\kappa=b\ne0
\]

although the background is exactly on the translation-gauge diagonal.

This candidate is excluded.

---

## 7. Candidate class III: target-predecessor constructions

There are two distinguished predecessor formulas.

### 7.1 Transport the target solder without the shift

Define

\[
q^{(0)}
=
L^{-1}v_r(e,x).
\tag{7.1}
\]

Then

\[
A(q^{(0)})=v_r(e,x)+b,
\]

so

\[
\boxed{
\kappa_{q^{(0)}}=b
}
\tag{7.2}
\]

on every background.

This preserves pure shift but cannot vanish on a nonzero exact pure-gauge shift.

It also makes the mismatch blind to all coframe-only data when \(b=0\).

### 7.2 Affine-inverse target solder

Define

\[
q^{(1)}
=
L^{-1}(v_r(e,x)-b)
=
A^{-1}(v_r(e,x)).
\tag{7.3}
\]

Then

\[
\boxed{
\kappa_{q^{(1)}}=0
}
\tag{7.4}
\]

on every background.

This is the tautological choice explicitly forbidden by the brief.  It erases:

- every nonzero pure affine shift;
- the \(L=2\) raw Nyquist mismatch at flat \(A\);
- the \(L=3\) off-diagonal corner mismatch;
- generic curl and harmonic B/E distinctions.

This candidate is excluded.

### 7.3 Constant interpolation

The family

\[
q^{(\lambda)}
=
L^{-1}(v-\lambda b)
\]

gives

\[
\kappa=(1-\lambda)b.
\tag{7.5}
\]

Pure gauge requires \(\lambda=1\), while nonzero pure-shift visibility excludes \(\lambda=1\).

No constant interpolation closes the controls.

---

## 8. Candidate class IV: constant source/target/shift linear combinations

Consider the complete constant affine span of the three obvious source-fibre vectors:

\[
\boxed{
q
=
a\,v_r(e,y)
+
c\,L^{-1}v_r(e,x)
+
d\,L^{-1}b.
}
\tag{8.1}
\]

Each term is source-typed and pure-linear frame covariant.

Flat normalization forces

\[
a+c=1.
\tag{8.2}
\]

Now use the exact \(L=3\) pure-gauge witness of §6, for which

\[
L=I,
\qquad
v_r(e,y)=v_r(e,x)=v,
\qquad
b\ne0.
\]

Exact pure-gauge cancellation requires

\[
q=v-b.
\]

Using (8.1) and (8.2),

\[
q=v+d\,b,
\]

so necessarily

\[
d=-1.
\tag{8.3}
\]

But on a pure affine-shift background,

\[
e=0,
\qquad
v_x=v_y=e_r,
\qquad
L=I,
\]

equations (8.1)–(8.3) give

\[
q=e_r-b.
\]

Hence

\[
\boxed{
\kappa=b+(e_r-b)-e_r=0.
}
\tag{8.4}
\]

This contradicts the mandatory nonzero pure-shift control.

Therefore:

\[
\boxed{
\text{No constant linear combination of }
v_y,\ L^{-1}v_x,\ L^{-1}b
\text{ satisfies all mandatory controls.}
}
\tag{8.5}
\]

This is a scoped candidate-class no-go, not a universal theorem about arbitrary nonlinear/nonlocal functions.

---

## 9. Candidate class V: a scalar selector only renames the missing primitive

One can generalize (7.5) to

\[
q
=
L^{-1}\bigl(v-\lambda(A,e;x,r)b\bigr).
\tag{9.1}
\]

Then

\[
\kappa
=
(1-\lambda)b.
\tag{9.2}
\]

The controls demand

\[
\lambda=1
\]

on the exact translation-gauge diagonal, but

\[
\lambda\ne1
\]

on nonzero pure-shift backgrounds; exact \(\kappa=b\) asks for \(\lambda=0\) there.

Thus a successful \(\lambda\) must distinguish “this shift is the exact coframe gauge displacement” from “this shift is an independent affine translation.”

That distinction is exactly the missing B/E selection law in scalar disguise.

No current owner supplies such a frame-natural selector on arbitrary raw backgrounds.

---

## 10. Candidate class VI: node affine origin plus source solder

A tempting affine-origin formulation is

\[
q_r(y)=o_y+v_r(e,y),
\tag{10.1}
\]

with a single node origin \(o_y\in V_y\).

This is already too small.

On the exact translation-gauge chart, the required origin is

\[
o_y^{(r)}
=
v_r(e,y-r)-b_{y-r,r}-v_r(e,y).
\tag{10.2}
\]

The right side depends on the edge Role \(r\).

Use a potential depending only on the \(A\) archive coordinate, with one internal \(B\) component.  At a site \(y\) where the two consecutive \(A\)-edge strains are equal and nonzero,

\[
o_y^{(A)}=-b_{y-A,A}\ne0.
\]

For the \(B\)-edge at the same site,

\[
e_B=0,
\qquad
b_B=0,
\qquad
v_B=e_B,
\]

so

\[
o_y^{(B)}=0.
\]

Therefore no single node vector \(o_y\) can satisfy all Role legs.

The sought datum is at least Role-labelled:

\[
q(y,r),
\]

not one node origin.

An “affine origin” language is legitimate only if accompanied by an additional directional frame/leg structure; it does not reduce the selection problem.

---

## 11. Full affine solder/origin covariance boundary

Let a full affine node gauge be

\[
h_x=(g_x,c_x).
\]

The affine connection obeys

\[
A'_{x,r}=h_xA_{x,r}h_y^{-1}.
\]

If a future reference point transforms affinely,

\[
q'_y=h_y(q_y)=g_yq_y+c_y,
\tag{11.1}
\]

then the affine evaluation identity gives

\[
A'_{x,r}(q'_y)
=
h_x(A_{x,r}(q_y)).
\tag{11.2}
\]

If the target solder point also transformed affinely,

\[
\widehat v'_x=h_x(\widehat v_x),
\tag{11.3}
\]

then

\[
A'(q')-\widehat v'
=
g_x\bigl(A(q)-\widehat v\bigr).
\tag{11.4}
\]

This is the clean full-affine covariance mechanism.

Current \`solderLegVector\` does not have (11.3).  Its owned rule is linear:

\[
v'_x=g_xv_x.
\tag{11.5}
\]

Combining (11.2) and (11.5) leaves the node-translation defect

\[
A'(q')-v'
=
g_x(A(q)-v)+c_x.
\tag{11.6}
\]

### 11.1 Why one cannot silently declare the current raw solder to be the affine point

On a translation gauge of flat,

\[
b_{x,r}=c_x-c_y
\]

up to the repository sign/scale convention, while the actual raw-solder vector is

\[
v_r(d_f\phi,x)
=
e_r+\eta b_{x,r}.
\tag{11.7}
\]

An affine point obtained from flat \(e_r\) by \(h_x\) would instead be

\[
e_r+c_x.
\tag{11.8}
\]

Equations (11.7) and (11.8) are different data.

Therefore a full affine solder/origin action would be a **new structure**, not a reinterpretation of the current \`rawFullSolderFrameAction\`.

### 11.2 Full affine covariance still does not select q

Even if (11.3) is adopted, covariance alone only specifies how a chosen section moves.

If \(z\) transforms linearly,

\[
z'_y=g_yz_y,
\]

then

\[
q'_y=h_y(q_y)
\]

implies

\[
(q+z)'_y
=
h_y(q_y+z_y).
\]

Thus the deformation freedom constructed below survives a full affine-point action.

Full affine solder/origin covariance is therefore not the missing uniqueness/selection principle.

---

## 12. Exact labelled-path composition audit

Consider two consecutive positive links

\[
x_0
\ \xleftarrow{A_1=(L_1,b_1)}\
x_1
\ \xleftarrow{A_2=(L_2,b_2)}\
x_2.
\]

Let

\[
q_1\in V_{x_1},
\qquad
q_2\in V_{x_2},
\]

and target solder legs

\[
v_1\in V_{x_0},
\qquad
v_2\in V_{x_1}.
\]

Define edge mismatches

\[
\kappa_1=A_1(q_1)-v_1,
\qquad
\kappa_2=A_2(q_2)-v_2.
\]

The semidirect translation assembled by labelled path multiplication is

\[
\kappa_1+L_1\kappa_2.
\]

A direct expansion gives the exact identity

\[
\boxed{
\kappa_1+L_1\kappa_2
=
\bigl((A_1A_2)(q_2)-v_1\bigr)
+
L_1(q_1-v_2).
}
\tag{12.1}
\]

The second term

\[
\boxed{
J_{12}:=L_1(q_1-v_2)
}
\tag{12.2}
\]

is a junction defect.

Therefore the edge mismatches telescope to one endpoint-origin formula if and only if the intermediate reference equals the next target solder leg:

\[
q_1=v_2.
\tag{12.3}
\]

That identity is not true generically.

It already fails as a universal statement at flat for a mixed-Role word:

\[
q_1=e_r,
\qquad
v_2=e_s,
\qquad
r\ne s.
\]

In that case the endpoint term and junction defect cancel so that the two zero edge mismatches still compose to zero.

Thus:

> labelled path composition of the **matter letters** remains exact for arbitrary edge-wise \(\kappa\), but the reference section does not compress to one path-endpoint origin without retaining the ordered Role junction data.

This is compatible with the merged labelled-path skeleton and is a reason not to quotient nontrivial path provenance.

The correct type of any future selector is therefore an edge-labelled/path-resolved section, not an endpoint-only node origin.

---

## 13. Local covariant nonselection: the solder-curl deformation

Assume one admissible section \(q\) has been supplied.

For any two Roles \(r,s\), define the covariant forward solder defect

\[
D_r^A v_s(x)
=
L_{x,r}v_s(e,x+r)-v_s(e,x)
\in V_x.
\tag{13.1}
\]

Under a pure-linear local frame,

\[
(D_r^A v_s)'(x)
=
g_xD_r^A v_s(x).
\tag{13.2}
\]

Define the solder curl

\[
\boxed{
C_{rs}^{A,e}(x)
=
D_r^A v_s(x)-D_s^A v_r(x).
}
\tag{13.3}
\]

It obeys

\[
C'_{rs}(x)=g_xC_{rs}(x).
\tag{13.4}
\]

### 13.1 Flat and pure shift

For

\[
e=0,
\qquad
L=I,
\]

all solder legs are constant, so

\[
C_{rs}=0.
\tag{13.5}
\]

This remains true for arbitrary affine shifts \(b\), because \(C_{rs}\) uses the linear pull and solder legs.

### 13.2 Exact pure gauge

On the translation-gauge chart,

\[
L=I,
\qquad
v_s=e_s+\eta e_s^{\rm row},
\qquad
e=d_f\phi.
\]

Therefore

\[
C_{rs}
=
\eta\bigl(\Delta_r e_s-\Delta_s e_r\bigr)^T.
\]

Forward translations commute, hence exact coframes obey

\[
\Delta_r e_s=\Delta_s e_r,
\]

so

\[
\boxed{
C_{rs}=0
\quad\text{on every exact translation-gauge background.}
}
\tag{13.6}
\]

### 13.3 Source-fibre deformation

For the edge \(y=x+r\), define

\[
\boxed{
z^{\rm curl}_{r,s}(A,e;y)
=
L_{x,r}^{-1}C_{rs}^{A,e}(x).
}
\tag{13.7}
\]

Then

\[
(z^{\rm curl})'(y)=g_yz^{\rm curl}(y).
\tag{13.8}
\]

For any scalar \(\lambda\),

\[
q_\lambda=q+\lambda z^{\rm curl}
\]

preserves:

- flat normalization;
- exact pure-gauge cancellation;
- exact pure-shift \(\kappa=b\);
- pure-linear frame covariance.

But

\[
\kappa_{q_\lambda}
=
\kappa_q+\lambda C_{rs}.
\tag{13.9}
\]

Thus generic coframe curl changes continuously with \(\lambda\).

### 13.4 Exact L=3 curl/corner witness

Take flat \(A\) and

\[
e_A{}^B(0)=1
\]

with all other entries zero.

Then

\[
v_A(0)=e_A-e_B,
\]

while the neighbouring \(A\)-leg in the \(B\) direction is \(e_A\), and the \(B\)-leg is constant.

At the origin,

\[
\boxed{
C_{AB}=-e_B\ne0.
}
\tag{13.10}
\]

So (13.9) changes this raw L=3 corner/curl background while leaving all mandatory normalization controls untouched.

This proves a local one-parameter nonselection family.

---

## 14. Global covariant nonselection: a harmonic deformation

The local curl deformation vanishes on a constant harmonic coframe.  A separate global witness shows that harmonic freedom is also not selected.

### 14.1 Full solder frame map

Package the four solder legs into a linear map

\[
B_e(x):V_{\rm ref}\to V_x
\]

defined by

\[
B_e(x)e_s=v_s(e,x).
\tag{14.1}
\]

In coordinates,

\[
B_e(x)=I+\eta\,e(x)^T.
\tag{14.2}
\]

At flat,

\[
B_0(x)=I.
\tag{14.3}
\]

Under the pure-linear frame subgroup,

\[
B_{e'}(x)=g_xB_e(x).
\tag{14.4}
\]

### 14.2 Path-transported global solder sum

Choose one archive base site \(o\), and for every site \(x\) choose a labelled path

\[
p_x:o\to x.
\]

Let

\[
P_x(A)
=
\operatorname{covariantLin}(A,p_x,o):
V_x\to V_o.
\tag{14.5}
\]

Define

\[
\boxed{
S_{A,e}^{o,p}
=
\sum_{x\in X}P_x(A)B_e(x)
:
V_{\rm ref}\to V_o.
}
\tag{14.6}
\]

From the path gauge law,

\[
P'_x
=
g_oP_xg_x^{-1}.
\]

Together with (14.4),

\[
\boxed{
S'_{A,e}=g_oS_{A,e}.
}
\tag{14.7}
\]

Assume the frame subgroup is Lorentz.  Then the abstract Gram

\[
G_{A,e}
=
(S_{A,e})^T\eta S_{A,e}
\tag{14.8}
\]

is exactly frame invariant.

Let

\[
m=|X|.
\]

Define the nonnegative invariant scalar

\[
\boxed{
\chi_{A,e}^{o,p}
=
\sum_{a,b}
\left(
G_{A,e}(a,b)-m^2\eta(a,b)
\right)^2.
}
\tag{14.9}
\]

No endpoint interpolation weight is introduced.

### 14.3 Flat and pure shift

For flat \(A\), \(e=0\),

\[
P_x=I,
\qquad
B_e(x)=I,
\]

hence

\[
S=mI,
\qquad
G=m^2\eta,
\qquad
\chi=0.
\tag{14.10}
\]

For a pure affine shift with \(e=0,L=I\), the translation \(b\) does not enter \(P_x\), so again

\[
\chi=0.
\tag{14.11}
\]

### 14.4 Exact pure gauge

For the translation-gauge chart, every linear link is \(I\), so

\[
P_x=I.
\]

Moreover

\[
B_e(x)=I+\eta e(x)^T.
\]

For every Role pair,

\[
\sum_{x\in X}e(x,r,a)=0
\]

because \(e=d_f\phi\) is a periodic forward difference.

Therefore

\[
\sum_xB_e(x)=mI.
\]

Thus

\[
\boxed{
\chi=0
\quad\text{on every exact translation-gauge background.}
}
\tag{14.12}
\]

By (14.7)–(14.9), it remains zero on every pure-linear frame transform of that background.

### 14.5 Constant harmonic witness

Take flat \(A\) and the constant coframe

\[
e_A{}^B(x)=1
\quad
\forall x.
\tag{14.13}
\]

This has a nonzero \(A\)-cycle sum and is not an exact periodic forward difference.

Equation (14.2) gives

\[
B
=
I-E_{B,A}.
\]

Exact arithmetic gives

\[
B^T\eta B-\eta
=
\begin{pmatrix}
-1&1&0&0\\
1&0&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix},
\]

so

\[
\sum_{a,b}
\bigl(B^T\eta B-\eta\bigr)_{ab}^2
=
3.
\tag{14.14}
\]

Since \(S=mB\),

\[
\boxed{
\chi=3m^4>0.
}
\tag{14.15}
\]

### 14.6 Harmonic deformation

Define

\[
\boxed{
z^{\rm harm}(A,e;y,r)
=
\chi_{A,e}^{o,p}\,v_r(e,y).
}
\tag{14.16}
\]

The scalar \(\chi\) is frame invariant and \(v_r(e,y)\) transforms by \(g_y\), so

\[
(z^{\rm harm})'(y)=g_yz^{\rm harm}(y).
\tag{14.17}
\]

It vanishes on flat, exact pure gauge and pure shift, but is nonzero on the harmonic witness (14.13).

Thus for any admissible \(q\),

\[
q_\mu=q+\mu z^{\rm harm}
\tag{14.18}
\]

preserves all mandatory normalizations while changing a nonzero harmonic cycle.

This proves a second independent nonselection direction.

### 14.7 The path choice is itself visible on curved backgrounds

For nontrivial linear holonomy, changing the chosen paths \(p_x\) changes the transported sum (14.6).

This is not a defect of the witness.  It exposes the actual path-selection problem:

> a harmonic-sensitive covariant selector requires a path/basepoint or equivalent global comparison rule, and current labelled-path ownership deliberately retains that provenance.

On flat and exact pure-gauge backgrounds, where the control is evaluated, the construction is path independent.

---

## 15. Two-parameter nonselection theorem

Assume \(q\) satisfies:

1. flat normalization;
2. exact pure-gauge cancellation;
3. exact pure-shift \(\kappa=b\);
4. pure-linear frame covariance.

Fix one ordered Role pair \(r,s\), one basepoint \(o\), and one labelled path family \(p\).

For any

\[
\lambda,\mu\in\mathbb R
\]

define

\[
\boxed{
q_{\lambda,\mu}
=
q
+
\lambda z^{\rm curl}
+
\mu z^{\rm harm}.
}
\tag{15.1}
\]

Then \(q_{\lambda,\mu}\) satisfies the same four mandatory controls.

Yet:

- varying \(\lambda\) changes the L=3 curl/corner witness;
- varying \(\mu\) changes the constant harmonic witness.

Therefore the mandatory controls do not select \(q\) uniquely.

This is a constructive nonselection result, not a dimension-counting analogy.

It also shows why adding the full affine transformation law alone would not select a unique section: linear-covariant \(z\) deformations can be added to any affine-point section.

---

## 16. Raw-data hostile controls

### 16.1 L=2 Nyquist

The owned period-two coframe has

\[
e_A{}^A=(-2,+2).
\]

Its centered coframe vanishes, while the raw solder legs are

\[
v_A=(-e_A,3e_A).
\tag{16.1}
\]

With flat affine connection and the flat reference \(q=e_A\),

\[
\kappa=(2e_A,-2e_A).
\tag{16.2}
\]

Thus the raw Nyquist mode remains literally distinguishable.

On the exact translation-gauge background with the same raw coframe, the affine shift is \(b=e\), and the required pure-gauge section gives \(\kappa=0\) as it must.

The two backgrounds have the same raw \(e\) but different \(A\).  Any selector that silently sets \(A=A(e)\) would destroy this distinction.

### 16.2 L=3 corner

For flat \(A\) and

\[
e_A{}^B(0)=a\ne0,
\]

the raw target solder is

\[
v_A(0)=e_A-ae_B.
\]

The fixed flat reference gives the nonzero mismatch

\[
\kappa=ae_B.
\]

The local curl deformation of §13 changes the same background by another nonzero covariant vector.

The corner is therefore not quotiented away by the classification.

### 16.3 Plaquette curl

Equation (13.10) gives an exact nonzero curl witness.

The family \(q+\lambda z^{\rm curl}\) shows that all mandatory pure-gauge tests leave its coefficient unselected.

### 16.4 Harmonic cycle

Equation (14.13) has nonzero cycle sum and \(\chi>0\).

The family \(q+\mu z^{\rm harm}\) shows that all mandatory pure-gauge tests leave its harmonic response unselected.

---

## 17. Why a local exact/coexact projector does not solve the frame problem

Because the archive is finite, one could choose a coordinate Hodge decomposition of the raw coframe and reconstruct a zero-mean potential on the exact subspace.

That would provide a chart-dependent prescription which recognizes

\[
e\in\operatorname{im}d_f
\]

and could force (2.3).

But \`rawFullSolderFrameAction\` is an active local Lorentz action on the full solder.  It does not preserve the fixed-coordinate condition

\[
e\in\operatorname{im}d_f
\]

as a literal equality in the raw perturbation coordinates.

Thus a counting-coordinate Hodge projector is not the required pure-linear frame-natural section.

Promoting it would introduce an additional gauge-fixing/metric principle, precisely the kind of new selector classified by the terminal.

---

## 18. Why path integration of the affine shift also needs a new selector

A second possible repair is to reconstruct an affine origin by integrating \(b\) along paths from a base site.

On a flat/pure-gauge connection this works after fixing a basepoint constant.

On a generic connection:

- different labelled paths can differ by affine holonomy;
- harmonic cycle translations are not reconstructed from a single-valued periodic potential;
- choosing a spanning tree/basepoint is additional data.

The merged labelled-path skeleton correctly keeps those alternatives distinct.

Therefore path integration is a valid **possible new selection principle**, not something already forced by \((A,e)\).

---

## 19. Existence versus selection

The present analysis does not prove that no frame-equivariant section can exist as a set-theoretic or highly nonlocal function.

For example, one could in principle:

1. classify pure-linear frame orbits of the finite background space;
2. choose a representative on every orbit;
3. prescribe \(q\) there;
4. transport it equivariantly.

That construction would require arbitrary orbit representatives and stabilizer checks.  It is not a geometric derivation from the current owners.

Likewise, a basepoint/path gauge fixing or a new observer/minimality functional could select one section.

Therefore a universal no-go would be too strong.

What is proved is:

- current local natural classes fail;
- current covariance laws do not select;
- the exact path skeleton prevents endpoint-only compression;
- explicit curl and harmonic deformation families survive all mandatory controls.

This is exactly the scope of terminal (0.3).

---

## 20. Exact finite checker

A standalone exact-rational checker passed **26/26 assertions**.

It verifies:

1. \(g\Lambda=I\);
2. \(\Lambda g=I\);
3. \(g^T\eta g=\eta\);
4. \(\eta\Lambda^T=g\eta\);
5. the \(L=3\) exact gauge cycle \((3,3,-6)\) has zero sum;
6. the first two neighbouring pure-gauge solder legs coincide;
7. the required pure-gauge \(q=v-b\) cancels exactly;
8. source solder gives nonzero \(\kappa=b\) on that exact gauge witness;
9. fixed flat reference gives \(6e_B\) on the same witness;
10. predecessor-without-shift gives \(\kappa=b\);
11. affine-inverse predecessor gives \(\kappa=0\);
12. the constant-linear candidate is forced to the pure-gauge value;
13. the same coefficient then erases a generic pure shift;
14. the \(L=2\) flat-A Nyquist mismatches are \(+2e_A,-2e_A\);
15. both Nyquist values are nonzero;
16. the L=3 curl witness is \(-e_B\);
17. the curl deformation is nonzero;
18. the constant harmonic Gram defect has exact squared size \(3\);
19. the global \(m\)-site harmonic defect is \(3m^4\);
20. the exact-gauge global solder-frame sum is \(3I\) on the one-cycle checker;
21. its Gram is \(9\eta\);
22. the harmonic Gram is invariant under the rational boost;
23. boosted pure-gauge cancellation remains exact;
24. the boosted reference vector is \((-1,-2,0,0)\);
25. the two-link junction identity (12.1) holds exactly;
26. the chosen junction witness is nonzero.

All arithmetic uses exact rational fractions; no floating tolerance is involved.

---

## 21. Theorem-ready handoff

The following are research-theorem-ready statements.  They are not claimed as merged Lean owners in this EXP.

### Theorem A — constant local linear candidate no-go

For a section of the form

\[
q
=
a\,v_y+c\,L^{-1}v_x+d\,L^{-1}b
\]

with constants \(a,c,d\), flat normalization plus exact pure-gauge cancellation on the \(L=3\) equal-neighbour gauge witness forces

\[
a+c=1,
\qquad
d=-1.
\]

Then every pure shift with \(e=0,L=I\) has

\[
\kappa=0.
\]

Hence this candidate class cannot satisfy the mandatory controls.

### Theorem B — target-predecessor endpoints

The candidate

\[
q=L^{-1}v_x
\]

has

\[
\kappa=b
\]

identically.

The candidate

\[
q=L^{-1}(v_x-b)
\]

has

\[
\kappa=0
\]

identically.

Neither solves the required diagonal/off-diagonal distinction.

### Theorem C — one node origin is insufficient

A decomposition

\[
q_r(y)=o_y+v_r(e,y)
\]

with one Role-independent node vector \(o_y\) cannot satisfy the generic exact pure-gauge condition for all Roles.

### Theorem D — exact path junction identity

For two consecutive links,

\[
\kappa_1+L_1\kappa_2
=
(A_1A_2)(q_2)-v_1
+
L_1(q_1-v_2).
\]

Hence a path endpoint-origin compression requires the extra junction condition

\[
q_1=v_2.
\]

The labelled path evaluator itself needs no such quotient and remains the correct parent.

### Theorem E — covariant solder curl

The vector

\[
C_{rs}^{A,e}(x)
=
\bigl(L_{x,r}v_s(x+r)-v_s(x)\bigr)
-
\bigl(L_{x,s}v_r(x+s)-v_r(x)\bigr)
\]

transforms as

\[
C'_{rs}(x)=g_xC_{rs}(x)
\]

under pure-linear frames.

It vanishes for flat, pure shift, and every exact translation-gauge coframe.

### Theorem F — curl nonselection family

The source deformation

\[
z^{\rm curl}_{r,s}(y)
=
L_{y-r,r}^{-1}C_{rs}(y-r)
\]

is source-vector covariant and vanishes on all mandatory normalization sectors.

Therefore

\[
q+\lambda z^{\rm curl}
\]

passes the same mandatory controls for all \(\lambda\), while changing a generic curl background.

### Theorem G — path-transported harmonic invariant

For a basepoint \(o\), path family \(p_x\), solder frame map \(B_e(x)e_s=v_s(e,x)\), and path linear pull \(P_x\),

\[
S=\sum_xP_xB_e(x)
\]

transforms by

\[
S'=g_oS.
\]

The scalar

\[
\chi
=
\sum_{a,b}
\left(
(S^T\eta S-m^2\eta)_{ab}
\right)^2
\]

is pure-linear frame invariant.

It vanishes on flat, pure shift and the full exact translation-gauge orbit.

### Theorem H — harmonic nonselection family

The source vector

\[
z^{\rm harm}(y,r)=\chi\,v_r(e,y)
\]

is frame covariant and vanishes on every mandatory normalization sector.

For the constant harmonic coframe

\[
e_A{}^B=1
\]

with flat \(A\),

\[
\chi=3m^4>0.
\]

Therefore

\[
q+\mu z^{\rm harm}
\]

changes harmonic response without changing any mandatory control.

### Theorem I — two-parameter nonselection

If one admissible \(q\) exists, then

\[
q_{\lambda,\mu}
=
q+\lambda z^{\rm curl}+\mu z^{\rm harm}
\]

is a two-parameter family with identical flat, exact pure-gauge, pure-shift and pure-linear covariance controls but inequivalent transverse responses.

### Theorem J — full affine action boundary

If both \(q\) and a target solder point transform affinely, then the mismatch transforms homogeneously.

If \(q\) transforms affinely but the current solder leg only linearly, the residual node-translation defect is \(c_x\).

A full affine action therefore repairs covariance but does not select the section.

---

## 22. Why the terminal is a new geometric selection principle

The missing datum is no longer algebraic representability, row/vector typing, or path multiplication.

All of those are already controlled.

The residual freedom is geometric:

- which edge-labelled source reference is used;
- how exact translation-gauge displacement is recognized without absorbing independent affine translation;
- how reference legs compare at path junctions;
- how harmonic/curl transverse data affect the section;
- whether a basepoint/path, minimality condition, affine-origin field, observer, or another independent structure selects one representative.

Current owners provide no theorem choosing among the explicit \(q_{\lambda,\mu}\) family.

Therefore the exact terminal is

\[
\boxed{
\texttt{SOLDER-REFERENCE-LEG-REQUIRES-NEW-GEOMETRIC-SELECTION-PRINCIPLE}.
}
\]

This terminal does not assert that a future selector cannot be built.

It says finite graded E dressing must not begin by silently choosing one.

---

## 23. Exactly one recommended next step

Create one dedicated research task for a **labelled-edge reference selection principle with an explicit junction/overlap law**.

Its first acceptance test should be that the proposed principle eliminates both constructed deformation freedoms

\[
z^{\rm curl},
\qquad
z^{\rm harm}
\]

while preserving:

\[
q_{\rm flat}=e_r,
\qquad
\kappa_{\rm pure\ gauge}=0,
\qquad
\kappa_{\rm pure\ shift}\ne0,
\]

and the exact pure-linear frame law.

Do not start finite graded E dressing until such a selector is derived from an independently stated geometric principle rather than inserted as a convenient formula.
