# MEMO A4D — affine translation-curvature action completion

**Task:** \`EXP-A4D-AFFINE-TRANSLATION-CURVATURE-ACTION-COMPLETION\`  
**Execution:** PR #185  
**Status:** terminal EXPENSIVE research classification  
**Baseline:** main after the first Cartan-Hodge translation no-go

## 0. Verdict

A continuous full-affine **single-plaquette** scalar cannot carry nontrivial
information from the translational part of one affine holonomy.

For one based affine holonomy

\[
H=(P,t),
\qquad
P\in SO^+(1,3),
\qquad
t\in V,
\]

an affine node change at the base gives

\[
P'=gPg^{-1},
\qquad
t'=gt+(I-P')c.
\tag{0.1}
\]

On the open generic stratum

\[
\det(I-P)\ne0,
\]

the translation subgroup is transitive on \(t\):

\[
t\mapsto t+(I-P)c.
\]

Therefore every invariant scalar is independent of \(t\) there.

The generic stratum is dense in \(SO^+(1,3)\).  Hence every **continuous**
full-affine invariant defined across all holonomy ranks is independent of
\(t\) everywhere.

The same kill gate applies to the owned open torsion.  Its exact gauge law is

\[
T'_{\rm open}
=
g_xT_{\rm open}
-
F'c_{\rm far}.
\tag{0.2}
\]

Whenever \(F\) is invertible, the far-site node translation is transitive on
\(T_{\rm open}\), so a continuous invariant is generically torsion-blind as
well.

Thus the single-plaquette terminal is

\[
\boxed{
\texttt{SINGLE-PLAQUETTE-AFFINE-TRANSLATION-SCALAR-NOGO-IN-CONTINUOUS-CLASS}.
}
\]

This does **not** force a supplied affine reference field.

There is a smaller constructive escape.

For two based affine holonomies at the same site,

\[
H_i=(P_i,t_i),
\qquad i=1,2,
\]

define

\[
M_i:=I-P_i,
\qquad
d_1:=\det M_1,
\]

\[
q_1^\#
:=
\operatorname{adj}(M_1)t_1,
\tag{0.3}
\]

and

\[
\boxed{
R_{2|1}
:=
d_1t_2-M_2q_1^\#.
}
\tag{0.4}
\]

Then under simultaneous full affine conjugation,

\[
\boxed{
R'_{2|1}=gR_{2|1}.
}
\tag{0.5}
\]

This formula is polynomial.  It uses no inverse and remains defined on
rank-deficient strata.

Consequently

\[
\eta(R_{2|1},R_{2|1})
\]

is a full-affine scalar, and

\[
h_n(R_{2|1},R_{2|1})
\]

is an observer-positive full-affine scalar.

On the exact nongauge one-edge shift from the relative-solder frontier, one
ordered pair of plaquettes gives

\[
R_{2|1}
=
\left(
-\frac{32}{9},
-\frac{40}{9},
\frac83,
0
\right)^T,
\]

with

\[
\boxed{
\eta(R_{2|1},R_{2|1})=-\frac{128}{9}.
}
\tag{0.6}
\]

Before the shift the same residual is zero.

The edge shift is independently certified not to be node gauge:

\[
\operatorname{rank}D_L=64,
\qquad
\operatorname{rank}[D_L\mid u]=65.
\]

So the two-holonomy residual detects an exact nongauge edge mode that the
relative-solder-only completion erased.

The minimal carrier statement is therefore

\[
\boxed{
\texttt{JOINT-TWO-HOLONOMY-TRANSLATION-RESIDUAL-SURVIVES}.
}
\]

At the level of based-holonomy count, one loop is terminally too small and two
loops already suffice.

This packet does **not** yet select a final action term.  The remaining problem
is to classify Role-natural combinations of the joint residuals and determine
how much of the full nongauge \(\operatorname{coker}D_L\) sector they separate.

Exact certificate:

\`02_REGISTRY/research/certificates/a4d_affine_translation_curvature_action_completion_check.py\`.

---

## 1. Single plaquette reduces to affine conjugacy

A plaquette has two affine square paths from the far corner to the base site,

\[
A_\square,
\qquad
B_\square.
\]

Under endpoint affine gauges,

\[
A'_\square
=
h_xA_\square h_f^{-1},
\qquad
B'_\square
=
h_xB_\square h_f^{-1}.
\tag{1.1}
\]

Their based relative affine holonomy is

\[
H
=
A_\square B_\square^{-1}.
\tag{1.2}
\]

The endpoint pair quotient is equivalent to the conjugacy class of \(H\).

Indeed one may use the far-end gauge to set \(B_\square=1\).  The residual
endpoint gauge then acts by simultaneous conjugation on

\[
H=A_\square B_\square^{-1}.
\]

Thus any single-plaquette gauge scalar can be regarded as a scalar on one
affine conjugacy class

\[
(P,t)
\sim
\left(
gPg^{-1},
gt+(I-gPg^{-1})c
\right).
\tag{1.3}
\]

This is why the based affine holonomy is the right KILL-FIRST object.

---

## 2. Generic translation conjugacy orbit

Fix \(P\).

For a pure node translation

\[
g=I,
\]

equation (1.3) becomes

\[
\boxed{
t\mapsto t+(I-P)c.
}
\tag{2.1}
\]

Therefore the exact translational conjugacy invariant is the residual class

\[
\boxed{
[t]\in
\operatorname{coker}(I-P).
}
\tag{2.2}
\]

This is the previously identified affine residual object.

If

\[
\det(I-P)\ne0,
\]

then

\[
\operatorname{coker}(I-P)=0.
\]

For arbitrary \(t,s\), choose

\[
c=(I-P)^{-1}(s-t).
\]

Then

\[
t+(I-P)c=s.
\tag{2.3}
\]

So the pure-translation orbit is the whole vector space.

No scalar invariant on that stratum can depend on \(t\).

---

## 3. The generic stratum is nonempty and dense

The certificate uses the exact rational proper-Lorentz matrix

\[
P_{\rm lox}
=
B_{AB}R_{CD},
\]

where

\[
B_{AB}
=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix}
\]

and \(R_{CD}\) is a \(90^\circ\) rotation in the \(C/D\) plane.

They commute, and

\[
P_{\rm lox}^T\eta P_{\rm lox}=\eta,
\qquad
\det P_{\rm lox}=1.
\]

Exactly,

\[
\boxed{
\det(I-P_{\rm lox})
=
-\frac83.
}
\tag{3.1}
\]

Thus the polynomial

\[
D(P)=\det(I-P)
\]

is not identically zero on \(SO^+(1,3)\).

Since \(D\) is real analytic on the connected proper-orthochronous Lorentz
group, its nonzero locus is open and dense.

For an explicit approach to the identity, define

\[
P(q)
=
B(q)\oplus R(q),
\]

with rational parametrizations

\[
\cosh\chi
=
\frac{1+q^2}{1-q^2},
\qquad
\sinh\chi
=
\frac{2q}{1-q^2},
\]

\[
\cos\theta
=
\frac{1-q^2}{1+q^2},
\qquad
\sin\theta
=
\frac{2q}{1+q^2}.
\]

Then

\[
P(0)=I
\]

and exactly

\[
\boxed{
\det(I-P(q))
=
\frac{16q^4}
{(q-1)(q+1)(q^2+1)}.
}
\tag{3.2}
\]

So every sufficiently small nonzero \(q\) lies in the generic stratum.

---

## 4. Continuous single-loop no-go

Let \(Z\) denote any additional local data that are invariant under a pure node
translation at the chosen base site; examples include:

- observer \(n\);
- linear holonomy \(P\);
- linear curvature;
- the affine-invariant relative solder from the preceding frontier.

Let

\[
f(P,t,Z)
\]

be continuous and invariant under

\[
t\mapsto t+(I-P)c.
\]

For every generic \(P\),

\[
f(P,t,Z)=f(P,0,Z).
\tag{4.1}
\]

Take any singular \(P_0\) and a sequence

\[
P_k\to P_0
\]

with

\[
\det(I-P_k)\ne0.
\]

Continuity gives

\[
\begin{aligned}
f(P_0,t,Z)
&=
\lim_k f(P_k,t,Z)
\\
&=
\lim_k f(P_k,0,Z)
\\
&=
f(P_0,0,Z).
\end{aligned}
\]

Hence

\[
\boxed{
f(P,t,Z)
\text{ is globally independent of }t.
}
\tag{4.2}
\]

This is the precise single-loop no-go.

It does not forbid discontinuous/rank-stratified functions of the residual
class (2.2).

---

## 5. Why the observer does not repair one loop

At fixed pure translation,

\[
n'=n.
\]

The observer metric supplies a positive bilinear form

\[
h_n.
\]

But on a generic holonomy the translation orbit is all of \(V\).

Therefore

\[
h_n(t,t)
\]

cannot be invariant.

The certificate gives two exactly conjugate vectors with different observer
norms and different Lorentz norms.

So the observer solves vector/covector typing, but not affine-origin freedom.

This sharply separates the role of \(h_n\) here from its successful role in
the relative-solder construction.

---

## 6. Open torsion has the same generic obstruction

The owned open torsion is

\[
T_{\rm open}
=
a_\square-b_\square.
\]

Its exact gauge law is

\[
\boxed{
T'_{\rm open}
=
g_xT_{\rm open}
-
F'c_{\rm far}.
}
\tag{6.1}
\]

The owned open curvature obeys

\[
F'
=
g_xF g_f^{-1}.
\]

For pure translations,

\[
F'=F,
\]

so

\[
T'_{\rm open}
=
T_{\rm open}-Fc_{\rm far}.
\tag{6.2}
\]

The exact relation

\[
F=(P-I)B
\]

contains an invertible square-path linear map \(B\).

Thus

\[
F
\text{ is invertible}
\iff
I-P
\text{ is invertible}.
\]

On the generic stratum, choose

\[
c_{\rm far}=F^{-1}T_{\rm open}.
\]

Then

\[
T'_{\rm open}=0.
\]

Therefore a continuous same-plaquette scalar cannot recover translation data
merely by replacing the based shift with open torsion.

In particular, a generic term informally called

\[
T^2
\]

is not an affine gauge invariant.

---

## 7. Homogeneous affine matrix traces are blind as well

Represent an affine map by the homogeneous matrix

\[
\widetilde H
=
\begin{pmatrix}
P&t\\
0&1
\end{pmatrix}.
\]

For every positive integer \(k\),

\[
\widetilde H^k
=
\begin{pmatrix}
P^k&*\\
0&1
\end{pmatrix}.
\]

Hence

\[
\boxed{
\operatorname{tr}\widetilde H^k
=
\operatorname{tr}P^k+1.
}
\tag{7.1}
\]

The translation is absent.

The exact certificate checks this for \(k=1,\dots,5\), but (7.1) is general.

So ordinary polynomial conjugacy invariants of one homogeneous affine matrix do
not provide the missing action term.

---

## 8. Why rank-stratified residuals are not ruled out

At

\[
P=I,
\]

the pure-translation conjugacy shift vanishes:

\[
t\mapsto t.
\]

There the full vector \(t\) is a genuine translational loop invariant, up to
the Lorentz frame.

More generally, for rank-deficient \(I-P\), the class

\[
[t]\in\operatorname{coker}(I-P)
\]

can be nonzero.

So the no-go is not the statement

\[
\text{"translation holonomy contains no invariant data."}
\]

The statement is:

> no **continuous scalar across the varying-rank single-loop carrier** can
> retain that residual data, because the residual vanishes identically on a
> dense generic stratum.

A pseudoinverse, explicit quotient basis, rank branch or projector could expose
the singular residual, but that is a rank-stratified/discontinuous extra
structure and must be declared as such.

---

## 9. Two loops change the orbit dimension

Now take two based affine holonomies sharing the same base site,

\[
H_1=(P_1,t_1),
\qquad
H_2=(P_2,t_2).
\]

The same base translation \(c\) acts simultaneously:

\[
t_i'
=
gt_i+(I-P_i')c.
\tag{9.1}
\]

Even if each \(I-P_i\) is individually invertible, one \(c\in V\) cannot
generically eliminate both \(t_1\) and \(t_2\).

Thus joint affine conjugacy has nontrivial translational moduli already on the
generic stratum.

This is the first place where continuity no longer forces translation
blindness.

---

## 10. Polynomial two-holonomy residual

Set

\[
M_i:=I-P_i,
\qquad
d_1:=\det M_1,
\]

\[
q_1^\#
:=
\operatorname{adj}(M_1)t_1.
\]

Under

\[
P_1'=gP_1g^{-1},
\]

one has

\[
M_1'=gM_1g^{-1},
\]

\[
d_1'=d_1,
\]

and

\[
\operatorname{adj}(M_1')
=
g\operatorname{adj}(M_1)g^{-1}.
\]

Using

\[
\operatorname{adj}(M_1)M_1=d_1I,
\]

equation (9.1) gives

\[
\boxed{
(q_1^\#)'
=
gq_1^\#
+
d_1c.
}
\tag{10.1}
\]

Thus \(q_1^\#\) is a polynomial weighted affine point.

Define

\[
\boxed{
R_{2|1}
=
d_1t_2
-
M_2q_1^\#.
}
\tag{10.2}
\]

Then

\[
\begin{aligned}
R'_{2|1}
&=
d_1\left(gt_2+M_2'c\right)
-
M_2'\left(gq_1^\#+d_1c\right)
\\
&=
gR_{2|1}.
\end{aligned}
\]

Therefore

\[
\boxed{
R'_{2|1}=gR_{2|1}.
}
\tag{10.3}
\]

This is an exact full-affine covariance theorem.

No inverse and no reference section appear.

---

## 11. Generic fixed-point interpretation

If

\[
d_1\ne0,
\]

define

\[
q_1
=
(I-P_1)^{-1}t_1.
\]

Then

\[
P_1q_1+t_1=q_1.
\]

So \(q_1\) is the unique affine fixed point of \(H_1\).

Moreover

\[
q_1^\#=d_1q_1.
\]

Hence

\[
R_{2|1}
=
d_1\left[
t_2-(I-P_2)q_1
\right].
\tag{11.1}
\]

The bracket is exactly the displacement of the dynamically selected fixed point
of loop 1 under loop 2.

This explains geometrically why two loops can define a translation residual
without an external affine origin.

The polynomial formula (10.2) is the denominator-free extension of that
construction to singular \(P_1\).

---

## 12. Scalar channels

Because \(R_{2|1}\) is a Lorentz vector,

\[
\boxed{
I^\eta_{2|1}
=
R_{2|1}^T\eta R_{2|1}
}
\tag{12.1}
\]

is a full-affine scalar.

If the owned observer is part of the action carrier,

\[
\boxed{
I^n_{2|1}
=
R_{2|1}^Th_nR_{2|1}
}
\tag{12.2}
\]

is also full-affine invariant and is positive for nonzero \(R\).

These are distinct scalar channels unless an additional observer-independence
principle is imposed.

This packet does not select between them or their coefficients.

---

## 13. Orientation/reversal controls

For a generic anchor loop, reversing its orientation does not change its affine
fixed point.

The certificate verifies on the exact control that

\[
q_1^\#(H_1^{-1})
=
q_1^\#(H_1).
\tag{13.1}
\]

Reversing the target loop gives

\[
\boxed{
R_{H_2^{-1}|H_1}
=
-P_2^{-1}R_{H_2|H_1}.
}
\tag{13.2}
\]

Since \(P_2\) is Lorentz,

\[
\eta(R,R)
\]

is unchanged.

Thus the quadratic Lorentz scalar is compatible with target loop orientation
reversal on the control.

A full Role-face aggregation law still requires its own action-level audit.

---

## 14. Exact nongauge edge witness

Use the curved \(L=2\) linear connection from the relative-solder pressure.

Before adding the matched one-edge shift,

\[
b=0,
\]

so every based affine loop translation vanishes and

\[
R_{2|1}=0.
\]

Now add

\[
u=e_A
\]

to the affine shift on one \(A\)-edge.

The previous frontier established that the corresponding matched solder/shift
change is invisible to the relative-solder-only action.

Independently,

\[
\operatorname{rank}D_L=64,
\]

and

\[
\operatorname{rank}[D_L\mid u]=65,
\]

so this edge shift is not generated by any node translation.

Choose at the origin:

- anchor face \(S_1=(A,C)\);
- target face \(S_2=(A,B)\).

Exactly,

\[
\det(I-P_{AC})
=
-\frac83.
\]

The joint residual becomes

\[
\boxed{
R_{AB|AC}
=
\begin{pmatrix}
-32/9\\
-40/9\\
8/3\\
0
\end{pmatrix}.
}
\tag{14.1}
\]

Its Lorentz norm is

\[
\boxed{
R_{AB|AC}^T\eta R_{AB|AC}
=
-\frac{128}{9}.
}
\tag{14.2}
\]

Thus the two-loop residual detects a concrete nongauge edge direction that one
relative solder did not.

This is a positive action-completion signal, not yet a completeness theorem for
all nongauge edge modes.

---

## 15. Minimality statement

The preceding results give an exact carrier hierarchy:

### One based loop

Continuous full-affine scalar dependence on translation is impossible.

### Two based loops

A polynomial affine-covariant translation residual exists and is nontrivial.

Therefore

\[
\boxed{
\text{minimum based-holonomy count for continuous translational sensitivity}
=2.
}
\tag{15.1}
\]

This statement is about the classified local holonomy carrier.

It does not exclude other carriers such as a supplied affine point, a
rank-stratified quotient object or longer path data.

---

## 16. Consequence for action completion

A naive single-plaquette term

\[
T_{\rm open}^2
\]

does not pass affine gauge symmetry.

Neither does any other continuous scalar whose only translation-sensitive
input is one affine holonomy.

The first constructive no-reference action building block is instead a joint
two-loop scalar such as

\[
I^\eta_{2|1}
\]

or

\[
I^n_{2|1}.
\]

This narrows the next research problem sharply.

One must now classify:

1. which ordered Role-face pairs are admitted;
2. whether Role/site naturality forces a unique aggregate;
3. the dimension of the scalar channel space
   \(\eta\) versus observer \(h_n\);
4. the flat and pure-shift limits;
5. the rank of the joint residual map on
   \(\operatorname{coker}D_L\);
6. whether adding the selected joint term to the relative-solder star term
   removes the accidental nongauge kernel without introducing new ones;
7. the resulting enlarged
   \[
   d_A\to d_E\to d_P.
   \]

Those questions are not answered by this packet.

---

## 17. Theorem-ready statements

1. **Single-loop translation orbit.**
   \[
   t\sim t+(I-P)c.
   \]

2. **Generic transitivity.**
   If
   \[
   \det(I-P)\ne0,
   \]
   all \(t\in V\) lie in one pure-translation orbit.

3. **Exact generic witness.**
   There exists rational
   \(P_{\rm lox}\in SO^+(1,3)\) with
   \[
   \det(I-P_{\rm lox})=-8/3.
   \]

4. **Generic stratum density.**
   \[
   \{P:\det(I-P)\ne0\}
   \]
   is open dense in \(SO^+(1,3)\).

5. **Continuous single-loop no-go.**
   Every continuous full-affine invariant scalar on one based affine holonomy
   is independent of its translation \(t\).

6. **Observer no cure.**
   Adding translation-inert observer data does not change Proposition 5.

7. **Open torsion transitivity.**
   On invertible \(F\),
   \[
   T\mapsto T-Fc_{\rm far}
   \]
   is transitive.

8. **No generic \(T^2\) invariant.**
   A continuous single-plaquette scalar quadratic in open torsion is not a full
   affine invariant.

9. **Affine matrix traces are translation blind.**
   \[
   \operatorname{tr}\widetilde H^k
   =
   \operatorname{tr}P^k+1.
   \]

10. **Polynomial weighted affine point.**
    \[
    q_1^\#
    =
    \operatorname{adj}(I-P_1)t_1
    \]
    obeys
    \[
    (q_1^\#)'=gq_1^\#+d_1c.
    \]

11. **Joint residual covariance.**
    \[
    R_{2|1}
    =
    d_1t_2-(I-P_2)q_1^\#
    \]
    obeys
    \[
    R'_{2|1}=gR_{2|1}.
    \]

12. **Two-loop scalar.**
    \[
    R_{2|1}^T\eta R_{2|1}
    \]
    is a full-affine scalar.

13. **Observer-positive two-loop scalar.**
    \[
    R_{2|1}^Th_nR_{2|1}
    \]
    is a full-affine scalar.

14. **Nongauge edge detection.**
    The exact one-edge nongauge witness gives
    \[
    R_{AB|AC}\ne0
    \]
    and Lorentz norm
    \[
    -128/9.
    \]

15. **Holonomy-count minimality.**
    One based loop is too small in the continuous class; two based loops admit
    nontrivial translational invariants.

---

## 18. Hostile controls

| Control | Result |
|---|---|
| rational generic loxodromic \(P\) | \(\det(I-P)=-8/3\) |
| arbitrary \(t\to s\) pure translation | exact |
| observer norm on same orbit | changes; not invariant |
| Lorentz norm on same orbit | changes; not invariant |
| open torsion with invertible \(F\) | gauges to zero |
| rational path \(P(q)\to I\) | generic for \(q\ne0\) |
| homogeneous affine traces | translation blind |
| two-loop mixed affine conjugation | \(R'\!=gR\) exactly |
| target loop reversal | norm preserved |
| one-edge nongauge \(u\) | augmented rank 65 |
| relative-solder blind witness | joint residual nonzero |
| supplied affine reference | not used |
| pseudoinverse/rank branch | not used |

---

## 19. Terminal disposition

The naive next step after the relative-solder frontier would have been to add a
single-plaquette torsion-square term.

That route is now closed in the continuous class.

The exact negative terminal is

\[
\boxed{
\texttt{SINGLE-PLAQUETTE-AFFINE-TRANSLATION-SCALAR-NOGO-IN-CONTINUOUS-CLASS}.
}
\]

But the action-completion programme does not die.

The exact constructive survivor is

\[
\boxed{
\texttt{JOINT-TWO-HOLONOMY-TRANSLATION-RESIDUAL-SURVIVES}.
}
\]

No external affine origin is required: the first loop supplies a polynomial
weighted fixed point, and the second loop measures its affine displacement.

The next legitimate gate is therefore not another one-loop torsion scalar.

It is a **Role-natural joint-holonomy completion** and a rank pressure test of
its residual map on the nongauge
\(\operatorname{coker}D_L\) sector.
