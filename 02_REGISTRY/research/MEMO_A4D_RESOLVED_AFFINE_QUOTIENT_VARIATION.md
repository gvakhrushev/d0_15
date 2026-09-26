# MEMO A4D — resolved affine quotient variation

**Task:** \`EXP-A4D-RESOLVED-AFFINE-QUOTIENT-VARIATION\`  
**Execution:** PR #189  
**Status:** terminal EXPENSIVE research classification  
**Baseline:** \`297067714e7c1a246b06ed981578105c58d9f3db\`

## 0. Verdict

The resolved affine quotient has a well-defined endpoint variational geometry,
but the three natural interpretations of its incidence memory are not
equivalent.

Let

\[
\mathcal N=C^0(X,V),
\qquad
\mathcal E=C^1_+(X,V),
\]

\[
D=D_L:\mathcal N\to\mathcal E,
\qquad
J:=\operatorname{im}D,
\]

and let the supplied gauge-image incidence satisfy

\[
J\subseteq\mathcal I\subseteq\mathcal E.
\]

Using the owned observer-positive edge product \(h\), let

\[
P=P_{\mathcal I},
\qquad
Q=I-P,
\]

\[
p:=Pb,
\qquad
r:=Qb.
\]

The resolved quotient term is

\[
E_{\mathcal I}(b)
=
\langle b,Qb\rangle_h
=
\|r\|_h^2.
\]

For an incidence tangent

\[
A:\mathcal I\to\mathcal I^\perp
\]

and an edge variation \(\dot b\), the exact first variation at fixed metric is

\[
\boxed{
\dot E
=
2\langle r,\dot b\rangle_h
-
2\langle r,Ap\rangle_h.
}
\tag{0.1}
\]

If the observer metric varies as well, one adds exactly

\[
\boxed{
\dot h(r,r).
}
\tag{0.2}
\]

The linearized incidence constraint

\[
\operatorname{im}D_t\subseteq\mathcal I_t
\]

is

\[
\boxed{
A(Dc)
=
Q\,\dot D(c)
\qquad
\forall c\in\mathcal N.
}
\tag{0.3}
\]

This immediately classifies the three contracts.

### Frozen incidence

If

\[
A=0,
\]

then (0.3) requires

\[
\boxed{
\operatorname{im}\dot D\subseteq\mathcal I.
}
\tag{0.4}
\]

Thus frozen memory does **not** support arbitrary connection variations.  It
is a restricted-variation problem, not the unconstrained endpoint action
principle.

### Constrained Grassmannian incidence

Let

\[
G
=
\mathcal I\cap J^{\perp_h},
\]

so

\[
\mathcal I=J\oplus_h G.
\]

The incidence constraint fixes the tangent \(A\) on \(J\) whenever it is
feasible, but leaves a free block

\[
\boxed{
B:G\to\mathcal I^\perp.
}
\tag{0.5}
\]

The free incidence variation is

\[
\boxed{
\dot E_{\rm free}
=
-2\langle r,B(P_Gb)\rangle_h.
}
\tag{0.6}
\]

Therefore the new incidence Euler equation is

\[
\boxed{
r\otimes(P_Gb)^\flat
=
0.
}
\tag{0.7}
\]

Equivalently,

\[
\boxed{
r=0
\quad\text{or}\quad
P_Gb=0.
}
\tag{0.8}
\]

This equation is absent from the star term because the star term has no
dependence on the incidence variable.

### History-derived incidence

A complete differentiable history determines both

\[
\mathcal I_*
\]

and its tangent

\[
\dot{\mathcal I}_*.
\]

But the endpoint pointwise data do not.

More strongly, the endpoint pair

\[
(D_0,\mathcal I_*)
\]

**and the first pointwise jet**

\[
\dot D_0
\]

still do not determine \(\dot{\mathcal I}_*\).

The exact \(L=2\) certificate constructs two proper-Lorentz histories with:

- the same flat endpoint \(D_0\);
- the same limiting incidence \(\mathcal I_A\);
- the same first pointwise \(D\)-jet;
- rank \(64\) on both punctured histories;
- different first incidence tangents.

Thus history-derived first variation requires additional tangent memory.

The exact subterminal is

\[
\boxed{
\texttt{HISTORY-FIRST-VARIATION-REQUIRES-INCIDENCE-TANGENT-MEMORY}.
}
\]

The overall terminal is

\[
\boxed{
\texttt{RESOLVED-AFFINE-QUOTIENT-VARIATION-CLASSIFIED}.
}
\]

For the two-channel trial action

\[
S_{\rm trial}
=
\alpha S_{\widehat\star}
+
\beta E_{\mathcal I},
\]

the action family has

\[
\boxed{
d_A=2
}
\]

inside this explicitly defined class.

Under the constrained-Grassmannian contract, the \(\beta\)-channel has a
generically nonzero incidence Euler component while the star channel has
identically zero incidence Euler component.  Since the accepted star channel
already has a nonzero Euler family, the coefficient-to-Euler map is injective:

\[
\boxed{
d_E=2
}
\tag{0.9}
\]

for this two-channel resolved variational family.

No statement about

\[
d_P
\]

is made here.

That now requires the exact Hessian/gauge quotient of the combined action.

Exact certificate:

\`02_REGISTRY/research/certificates/a4d_resolved_affine_quotient_variation_check.py\`.

---

## 1. Resolved quotient geometry

Fix one finite background and the edge observer product

\[
\langle u,v\rangle_h.
\]

The affine gauge-image resolution supplies

\[
J=\operatorname{im}D
\subseteq
\mathcal I.
\]

Let

\[
P=P_{\mathcal I}
\]

be the \(h\)-orthogonal projector and

\[
Q=I-P.
\]

For the affine edge shift \(b\), decompose

\[
\boxed{
b=p+r,
\qquad
p=Pb\in\mathcal I,
\qquad
r=Qb\in\mathcal I^\perp.
}
\tag{1.1}
\]

The positive quotient energy is

\[
\boxed{
E_{\mathcal I}(b)
=
\langle r,r\rangle_h.
}
\tag{1.2}
\]

At the intrinsic point

\[
\mathcal I=J,
\]

this is the ordinary positive norm on the affine translation quotient.

At a rank-transition endpoint,

\[
J\subsetneq\mathcal I
\]

records lost gauge-image directions of a supplied approach.

---

## 2. Tangent space to the Grassmannian

Let

\[
t\mapsto\mathcal I_t
\]

be a differentiable fixed-dimensional Grassmannian curve through
\(\mathcal I\).

Its tangent is canonically represented by

\[
\boxed{
A\in\operatorname{Hom}(\mathcal I,\mathcal I^\perp).
}
\tag{2.1}
\]

Choose the skew-adjoint infinitesimal generator

\[
K
=
\begin{pmatrix}
0&-A^\ast\\
A&0
\end{pmatrix}
\]

relative to

\[
\mathcal E
=
\mathcal I\oplus_h\mathcal I^\perp.
\]

For

\[
P_t=e^{tK}Pe^{-tK},
\]

one gets

\[
\boxed{
\dot P
=
AP+A^\ast Q.
}
\tag{2.2}
\]

Therefore

\[
\boxed{
\dot Q
=
-AP-A^\ast Q.
}
\tag{2.3}
\]

The exact certificate checks this in the minimal
\(\mathbb R^3\) model.

---

## 3. First variation at fixed observer metric

Write

\[
E=b^TQb
\]

in an \(h\)-orthonormal coordinate system.

Then

\[
\dot E
=
2\langle Qb,\dot b\rangle
+
\langle b,\dot Qb\rangle.
\]

Using

\[
p=Pb,
\qquad
r=Qb,
\]

and (2.3),

\[
\langle b,\dot Qb\rangle
=
-2\langle r,Ap\rangle.
\]

Hence

\[
\boxed{
\dot E
=
2\langle r,\dot b\rangle
-
2\langle r,Ap\rangle.
}
\tag{3.1}
\]

This is the basic variational formula.

The first term is the ordinary quotient-edge force.

The second is the force conjugate to motion of the resolved incidence plane.

---

## 4. Moving observer metric

The distance formulation is

\[
E_{\mathcal I}(b;h)
=
\min_{u\in\mathcal I}
h(b-u,b-u).
\]

At the minimizing point

\[
u=p,
\qquad
r=b-p,
\]

the derivative with respect to \(u\) vanishes.

Therefore the envelope theorem in this finite quadratic problem gives

\[
\boxed{
\dot E
=
\dot h(r,r)
+
2h(r,\dot b)
-
2h(r,Ap).
}
\tag{4.1}
\]

No additional hidden derivative of the minimizing representative is needed.

The observer variation is thus cleanly separate from the incidence variation.

---

## 5. Linearized incidence constraint

A valid resolved path must satisfy

\[
QD=0.
\]

Differentiate:

\[
\dot QD+Q\dot D=0.
\]

For

\[
j=Dc\in J\subseteq\mathcal I,
\]

equation (2.3) gives

\[
\dot Qj=-Aj.
\]

Hence

\[
\boxed{
A(Dc)=Q\dot D(c).
}
\tag{5.1}
\]

This is the exact linearized incidence law.

---

## 6. Feasibility condition at a rank seam

Equation (5.1) must depend only on

\[
j=Dc,
\]

not on the chosen preimage \(c\).

If

\[
k\in\ker D,
\]

then \(Dk=0\), so (5.1) requires

\[
\boxed{
Q\dot D(k)=0.
}
\tag{6.1}
\]

Equivalently,

\[
\boxed{
\dot D(\ker D)\subseteq\mathcal I.
}
\tag{6.2}
\]

This is the first-order feasibility condition for a fixed-dimensional
incidence lift.

When it holds, define

\[
A_J:J\to\mathcal I^\perp
\]

by

\[
\boxed{
A_J(Dc)=Q\dot D(c).
}
\tag{6.3}
\]

This is well defined.

Any full incidence tangent must extend \(A_J\).

---

## 7. Frozen-memory contract

If the incidence memory is declared frozen,

\[
A=0.
\]

Then (5.1) becomes

\[
Q\dot D(c)=0
\qquad
\forall c.
\]

Therefore

\[
\boxed{
\operatorname{im}\dot D\subseteq\mathcal I.
}
\tag{7.1}
\]

This is much stronger than gauge invariance.

It forbids every infinitesimal link variation whose node-difference image
points outside the supplied incidence plane.

On the exact \(L=2\) branch of PR #188:

\[
\dim\mathcal I_A=64.
\]

A new Lorentz variation on the fourth origin edge produces a first-order image
matrix \(H\) satisfying

\[
\boxed{
\operatorname{rank}[\mathcal I_A\mid H]=66.
}
\tag{7.2}
\]

Thus two independent first-order image directions lie outside
\(\mathcal I_A\).

Frozen incidence rejects that legitimate connection variation.

Therefore frozen memory is not a full endpoint variational contract.

It may still define a restricted background variation, but one must say so
explicitly.

---

## 8. Intrinsic constant-rank stratum

Suppose

\[
\mathcal I=J=\operatorname{im}D
\]

and the variation stays on a constant-rank stratum.

Then

\[
G=0.
\]

Equation (5.1) uniquely determines the Grassmannian tangent of the image.

There is no independent incidence variable.

Thus:

\[
\boxed{
\text{intrinsic constant-rank variation adds no new incidence Euler equation.}
}
\tag{8.1}
\]

This is the regular situation.

The quotient term varies only through the ordinary pointwise fields.

---

## 9. Resolved rank-drop stratum

Now suppose

\[
J\subsetneq\mathcal I.
\]

Use the observer metric to split

\[
\boxed{
\mathcal I=J\oplus_h G,
}
\tag{9.1}
\]

where

\[
G=\mathcal I\cap J^\perp.
\]

The forced tangent on \(J\) is \(A_J\).

Every extension has the form

\[
\boxed{
A=A_{\rm forced}+B,
}
\tag{9.2}
\]

where

\[
\boxed{
B\in\operatorname{Hom}(G,\mathcal I^\perp)
}
\tag{9.3}
\]

is arbitrary.

This is the genuinely new resolved incidence variation.

---

## 10. Dimension of the free incidence tangent

Let

\[
m=\dim\mathcal E,
\qquad
s=\dim J=\operatorname{rank}D,
\qquad
r_I=\dim\mathcal I.
\]

Then

\[
\dim G=r_I-s
\]

and

\[
\dim\mathcal I^\perp=m-r_I.
\]

Therefore

\[
\boxed{
\dim\operatorname{Hom}(G,\mathcal I^\perp)
=
(r_I-s)(m-r_I).
}
\tag{10.1}
\]

For the exact \(L=2\) flat generic-limit resolved branch,

\[
m=256,
\]

\[
s=60,
\]

\[
r_I=64.
\]

Hence

\[
\boxed{
\dim T_{\rm free}
=
4\cdot192
=
768.
}
\tag{10.2}
\]

This is a tangent-space dimension, not a count of independent physical modes.

---

## 11. Free incidence Euler equation

Decompose

\[
p=Pb
\]

further into

\[
p=p_J+p_G
\]

with

\[
p_G=P_Gb.
\]

The free tangent \(B\) vanishes on \(J\).

Therefore the \(B\)-dependent variation is

\[
\boxed{
\dot E_B
=
-2\langle r,Bp_G\rangle.
}
\tag{11.1}
\]

Stationarity for every

\[
B:G\to\mathcal I^\perp
\]

is equivalent to

\[
\boxed{
r\otimes p_G^\flat=0.
}
\tag{11.2}
\]

Indeed, if both \(r\) and \(p_G\) are nonzero, choose \(B\) sending \(p_G\)
to \(r\).

Thus

\[
\boxed{
r=0
\quad\text{or}\quad
p_G=0.
}
\tag{11.3}
\]

The exact \(\mathbb R^3\) certificate takes

\[
J=\operatorname{span}(e_1),
\]

\[
G=\operatorname{span}(e_2),
\]

\[
\mathcal I^\perp=\operatorname{span}(e_3),
\]

\[
b=e_2+e_3,
\]

and

\[
Be_2=e_3.
\]

Then

\[
\boxed{
\dot E_B=-2.
}
\tag{11.4}
\]

So the incidence equation is not vacuous.

---

## 12. Combined trial action

Consider the explicitly defined two-channel family

\[
\boxed{
S_{\rm trial}
=
\alpha S_{\widehat\star}
+
\beta E_{\mathcal I}.
}
\tag{12.1}
\]

The two terms are linearly independent functionals:

- the star term depends on the relative solder and linear curvature;
- the resolved quotient term is positive and depends on the affine shift
  quotient.

Therefore, inside this family,

\[
\boxed{
d_A=2.
}
\tag{12.2}
\]

Under constrained-Grassmannian variation, the star action has

\[
\frac{\delta S_{\widehat\star}}{\delta\mathcal I}=0.
\]

The quotient channel has the incidence gradient

\[
\boxed{
\frac{\delta E}{\delta B}
=
-2\,r\otimes p_G^\flat,
}
\tag{12.3}
\]

which is nonzero on the exact finite control.

Hence no nonzero multiple of the quotient Euler family can equal the star
Euler family.

The accepted star action already has a nonzero Euler family.

Therefore the coefficient-to-Euler map on the two-dimensional trial family is
injective:

\[
\boxed{
d_E=2.
}
\tag{12.4}
\]

This conclusion is specific to the constrained-Grassmannian resolved
variational contract.

It is not yet a physical quotient statement.

---

## 13. Why 768 tangent directions do not mean \(d_E=768\)

The incidence gradient is the rank-one tensor

\[
-2r\otimes p_G^\flat.
\]

The 768-dimensional tangent space merely supplies all probes of this tensor.

The Euler equation is the vanishing of that tensor.

It factorizes into the nonlinear union

\[
r=0
\]

or

\[
p_G=0.
\]

Thus tangent dimension and action-family dimension must not be confused.

The present

\[
d_E=2
\]

statement concerns the two-dimensional **action coefficient family**, not the
number of components of one Euler equation.

---

## 14. History-derived contract

Suppose the incidence is not varied independently but is defined as a
Grassmannian limit of a complete punctured background history.

Then a differentiable history can determine

\[
\mathcal I_*
\]

and

\[
\dot{\mathcal I}_*.
\]

The question is whether the endpoint data already determine that tangent.

They do not.

---

## 15. Same endpoint and same incidence, different incidence tangent

Use the same \(L=2\) flat endpoint and the same three first-order boost links
as in PR #188.

For the first history:

- the three origin edges \(A,B,C\) have Cayley arguments
  \[
  tA_{01},\quad tA_{02},\quad tA_{03};
  \]
- the fourth origin edge is identity.

For the second history:

- the same first three links are used;
- the fourth origin edge has Cayley argument
  \[
  t^2A_{01}.
  \]

Both are proper-Lorentz histories for small \(t\).

The fourth-link difference starts at order \(t^2\).

Therefore both histories have:

\[
\boxed{
L_0=I,
}
\]

and the same first pointwise link jet.

Consequently they have the same first pointwise

\[
\boxed{
\dot D_0.
}
\tag{15.1}
\]

---

## 16. Same limiting incidence

On constant node vectors, divide the lost image by the leading activation
scale \(t\).

For both histories the limit is the same map

\[
\Gamma_A
\]

supported on the first three origin edges.

Therefore both histories have the same limiting image incidence

\[
\boxed{
\mathcal I_*
=
\mathcal I_A
=
\operatorname{im}D_0+\operatorname{im}\Gamma_A.
}
\tag{16.1}
\]

Exactly,

\[
\dim\mathcal I_A=64.
\]

Both punctured histories have

\[
\operatorname{rank}D_t=64
\]

at the exact rational sample \(t=1/7\).

---

## 17. Different incidence tangent

For the fourth link of History 2,

\[
L_4(t)
=
\operatorname{Cayley}(t^2A_{01}).
\]

Exactly,

\[
L_4'(0)=0.
\]

But

\[
\frac12
\frac{d^2}{dt^2}
\left(I-L_4(t)\right)_{t=0}
=
-A_{01}.
\tag{17.1}
\]

After normalizing the lost constant-kernel columns by the leading scale \(t\),
this contributes a first incidence-tangent matrix \(H\) supported on the
fourth edge.

The exact augmented rank is

\[
\boxed{
\operatorname{rank}[\mathcal I_A\mid H]
=
66.
}
\tag{17.2}
\]

Thus the incidence tangent is genuinely different.

We have therefore constructed two histories with:

\[
D_0^{(1)}=D_0^{(2)},
\]

\[
\dot D_0^{(1)}=\dot D_0^{(2)},
\]

\[
\mathcal I_*^{(1)}=\mathcal I_*^{(2)},
\]

but

\[
\boxed{
\dot{\mathcal I}_*^{(1)}
\ne
\dot{\mathcal I}_*^{(2)}.
}
\tag{17.3}
\]

This is the exact history nonreconstruction theorem needed for first
variation.

---

## 18. Minimal history memory for first variation

For one endpoint resolved state, let two history tangents be represented by

\[
A_1,A_2:
\mathcal I\to\mathcal I^\perp.
\]

Suppose

\[
A_1\ne A_2.
\]

Then there exists

\[
p\in\mathcal I
\]

with

\[
(A_1-A_2)p\ne0.
\]

Choose

\[
r=(A_1-A_2)p\in\mathcal I^\perp
\]

and

\[
b=p+r.
\]

The difference of the incidence parts of the first variation is

\[
-2\langle r,(A_1-A_2)p\rangle
=
-2\|r\|^2
\ne0.
\]

Therefore a universal first-variation readout distinguishes \(A_1\) and
\(A_2\).

Hence the source-independent structural first-variation memory is

\[
\boxed{
(\mathcal I,\dot{\mathcal I})
}
\]

or equivalently

\[
\boxed{
(\mathcal I,A).
}
\tag{18.1}
\]

Endpoint \(\mathcal I\) alone is not enough.

---

## 19. Relation to complete history

A complete differentiable background germ may reconstruct the tangent \(A\).

That does not make \(A\) pointwise geometry.

The hierarchy is now:

\[
\text{pointwise background}
\longleftarrow
\text{endpoint incidence }\mathcal I
\longleftarrow
\text{incidence tangent }A
\longleftarrow
\text{complete history germ}.
\]

Each left arrow forgets information that can affect downstream readouts.

This is the affine gauge-image analogue of the memory hierarchy already found
for the relative A/e resolution.

---

## 20. Variational contract classification

### Contract A — frozen memory

**Mathematically defined:** yes.

**Full endpoint variation:** no.

It restricts connection variations by

\[
\operatorname{im}\dot D\subseteq\mathcal I.
\]

Use only when a restricted background family is intended.

### Contract B — constrained Grassmannian

**Mathematically defined:** yes.

**Endpoint-local:** yes, on the resolved configuration space.

**New Euler equation:** yes, whenever

\[
G\ne0.
\]

This is the minimal self-contained endpoint variational problem.

### Contract C — history-derived

**Mathematically defined:** yes, once a differentiable history is supplied.

**Determined by endpoint \(\mathcal I\):** no.

**Determined by endpoint plus first pointwise jet:** no.

A universal first variation requires at least incidence-tangent memory.

---

## 21. Why the constrained contract is the minimal endpoint closure

The resolved configuration space can be defined as pairs

\[
(D,\mathcal I)
\]

with

\[
\operatorname{im}D\subseteq\mathcal I
\]

and fixed incidence dimension on each stratum.

Its tangent space is determined internally by (5.1) and (6.1).

No external history is needed.

Thus Contract B is the smallest endpoint-local configuration space on which:

- the resolved action value is defined;
- full compatible field variations are defined;
- the incidence memory can respond to changing \(D\);
- the extra Euler equation is explicit.

This does not prove that Nature/D0 must choose Contract B.

It proves that it is the minimal closed endpoint variational geometry.

---

## 22. The next physical quotient gate

The present task advances the chain to

\[
\boxed{
d_A=2
\longrightarrow
d_E=2
}
\]

for the explicit two-channel resolved family under Contract B.

The remaining question is

\[
\boxed{
d_P\;?
}
\]

That requires the exact Hessian and gauge quotient of

\[
\alpha S_{\widehat\star}
+
\beta E_{\mathcal I}
\]

on a fixed regular resolved stratum.

The first pressure should be finite and exact:

1. choose an intrinsic constant-rank background, so \(G=0\);
2. compute the two-parameter Hessian pencil;
3. quotient local Lorentz and affine node translations;
4. determine whether \(\beta/\alpha\) survives in the physical operator;
5. only then decide whether an action-level coefficient selector is needed.

This is exactly the repository's required
\(d_A\to d_E\to d_P\) order.

---

## 23. Theorem-ready statements

1. **Grassmannian tangent.**
   \[
   T_{\mathcal I}\mathrm{Gr}
   \cong
   \operatorname{Hom}(\mathcal I,\mathcal I^\perp).
   \]

2. **Projector derivative.**
   \[
   \dot P=AP+A^\ast Q.
   \]

3. **Fixed-metric energy variation.**
   \[
   \dot E
   =
   2\langle r,\dot b\rangle
   -2\langle r,Ap\rangle.
   \]

4. **Moving-metric variation.**
   \[
   \dot E
   =
   \dot h(r,r)
   +2h(r,\dot b)
   -2h(r,Ap).
   \]

5. **Linearized incidence.**
   \[
   A(Dc)=Q\dot D(c).
   \]

6. **Feasibility.**
   \[
   \dot D(\ker D)\subseteq\mathcal I.
   \]

7. **Frozen-memory condition.**
   \[
   \operatorname{im}\dot D\subseteq\mathcal I.
   \]

8. **Resolved split.**
   \[
   \mathcal I=J\oplus_h G.
   \]

9. **Free incidence tangent.**
   \[
   B\in\operatorname{Hom}(G,\mathcal I^\perp).
   \]

10. **Free Euler gradient.**
    \[
    -2r\otimes(P_Gb)^\flat.
    \]

11. **Incidence stationarity.**
    \[
    r=0
    \quad\text{or}\quad
    P_Gb=0.
    \]

12. **Intrinsic regular branch.**
    \[
    G=0
    \Rightarrow
    \text{no independent incidence Euler equation}.
    \]

13. **Exact L2 free-tangent dimension.**
    \[
    4\cdot192=768.
    \]

14. **Frozen-control failure.**
    \[
    \operatorname{rank}[\mathcal I_A\mid H]=66>64.
    \]

15. **History nonreconstruction.**
    Same
    \[
    (D_0,\dot D_0,\mathcal I_*)
    \]
    can have different
    \[
    \dot{\mathcal I}_*.
    \]

16. **First-variation memory minimality.**
    Universal first variation determines the incidence tangent \(A\).

17. **Two-channel action dimension.**
    \[
    d_A=2.
    \]

18. **Constrained resolved Euler dimension.**
    \[
    d_E=2.
    \]

19. **Physical dimension unclassified.**
    \[
    d_P
    \text{ remains open.}
    \]

---

## 24. Hostile controls

| Control | Result |
|---|---|
| \(\mathbb R^3\) projector tangent | exact |
| \(\dot E\) direct vs factorized formula | equal |
| free incidence tangent | nonzero \(-2\) variation |
| outer-product Euler gradient | rank one on witness |
| intrinsic \(G=0\) | no free tangent |
| L2 flat \(D_0\) | rank 60 |
| resolved \(\mathcal I_A\) | rank 64 |
| free resolved tangent dimension | 768 |
| new fourth-edge Lorentz variation | frozen \(\mathcal I_A\) rejects it |
| history 1 punctured rank | 64 |
| history 2 punctured rank | 64 |
| fourth-link first jet | zero |
| normalized lost-image tangent | nonzero |
| same endpoint incidence | yes |
| different incidence tangent | yes |
| pseudoinverse | not used |
| Lean | not changed |

---

## 25. Terminal disposition

The affine quotient completion is now past pure covariance.

The resolved incidence datum contributes genuine variational structure.

The strongest terminal is

\[
\boxed{
\texttt{RESOLVED-AFFINE-QUOTIENT-VARIATION-CLASSIFIED}.
}
\]

The history-specific negative subterminal is

\[
\boxed{
\texttt{HISTORY-FIRST-VARIATION-REQUIRES-INCIDENCE-TANGENT-MEMORY}.
}
\]

The minimal self-contained endpoint variational geometry is the constrained
Grassmannian carrier

\[
(D,\mathcal I),
\qquad
\operatorname{im}D\subseteq\mathcal I.
\]

For the explicit two-channel action family it yields

\[
\boxed{
d_A=2,\qquad d_E=2.
}
\]

The next pressure point is now unambiguous:

\[
\boxed{
\text{EXACT PHYSICAL HESSIAN / GAUGE QUOTIENT OF THE TWO-CHANNEL ACTION}.
}
\]

Only that calculation can decide whether the new coefficient survives to
\(d_P\), disappears after constraints, or is selected by degeneracy removal.


---

## Ready-state EXPENSIVE audit

PR #189 is \`Lifecycle: REVIEW\`. The EXPENSIVE task self-retired before Ready:
its manifest/status entry and executable task brief are absent from the branch,
while the durable memo, exact certificate, and research-ledger verdict remain.
This audit-only commit changes no mathematical result; it exists so repository
guards evaluate the final Ready-state contract rather than the preceding Draft
event.
