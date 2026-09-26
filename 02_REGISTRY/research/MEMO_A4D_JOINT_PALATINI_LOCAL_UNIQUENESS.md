# MEMO A4D — joint Palatini local uniqueness

**Task:** \`EXP-A4D-JOINT-PALATINI-LOCAL-UNIQUENESS\`  
**Execution:** PR #232  
**Status:** EXACT JOINT NO-GO  
**Baseline at start:** \`966e280f81d5d3e27d8715dd5fdc98f3c3e9b35d\`  
**Exact parent certificate:** \`02_REGISTRY/research/certificates/a4d_joint_palatini_exact_diagonal_vacuum_check.py\`

## 0. Terminal

The requested positive terminal is **not** reached.

Instead the unchanged naked star action has an exact analytic, curved,
non-gauge joint-vacuum curve through the flat point:

\[
\boxed{
E_K(\eta,K(z))=0,
\qquad
E_Q(\eta,K(z))=0
}
\]

for all sufficiently small real \(z\), while the plaquette curvature is
nonzero for \(z\neq0\).

Therefore the flat/LC-like joint vacuum is not locally isolated by

\[
E_K=0,\qquad E_Q=\kappa T
\]

even in the vacuum subcase \(T=0\).

The exact task terminal is

\[
\boxed{
\texttt{NAKED-STAR-JOINT-PALATINI-LOCAL-UNIQUENESS-NOGO}
}
\]

and not

\[
\texttt{NAKED-STAR-JOINT-PALATINI-SMOOTH-EINSTEIN-BRANCH-CLOSED}.
\]

This is a no-go for **joint local uniqueness / UV elimination**. It is not a
no-go for the existence of the designated smooth Einstein branch, nor for its
already-owned coefficient \(-\tfrac12G\).

---

## 1. Scope and source contract

The task declares the stress-only sourced system

\[
E_K=0,\qquad E_Q=\kappa T.
\]

The repository lane audited here does not independently derive that every
possible D0 matter realization has zero connection/spin current. Thus the
statement remains scoped to this declared stress-only source class.

Vacuum \(T=0\) is a valid member of that class. An exact curved joint vacuum
through flat is therefore sufficient to obstruct the requested local
uniqueness theorem.

No new action channel, Holst term, \(\varphi\), boundary selector, spectral
filter, torsion constraint, or connection selector is introduced.

---

## 2. Mandatory input audit

The parent consumed the following results without reopening their owned
calculations:

- #201: the regular IR metric Hessian of naked \(S_\star\) has
  \[
  T_1^{[2]}=\frac14E_\eta,
  \qquad
  E_\eta=-2G
  \]
  on the owned normal-jet convention, hence the designated smooth branch has
  coefficient \(-\frac12G\).

- #208/#216: the metric is the genuine nonlinear quotient coordinate and the
  connection symbol has UV resonances although the zero-phase/IR block is
  regular.

- #223: normal-center nonlinear terms of total derivative degree \(\le2\)
  vanish beyond the linear Einstein term.

- #226: finite-stencil metric response is polynomially sensitive to connection
  corrections; after the single \(h^{-2}\) normalization, an
  \(O(h^\infty)\) connection correction remains \(O(h^\infty)\).

- #227: all-\(E_K\)-sheet branch independence is false. Its explicit curved
  connection-stationary family is source-visible under \(E_Q\).

- merged #233: the #227 family is torsionful globally except at the identity,
  but torsion is diagnostic only and is not added as a field equation.

The diagonal worker #235 found the correct source-invisible direction and
proved

\[
E_Q(\eta,K(t))=0
\]

exactly, while its connection calculation stopped at

\[
E_K(\eta,K(t))=O(t^9).
\]

The parent exactification below upgrades that finite jet to an exact analytic
joint-vacuum curve.

---

## 3. Corrective audit of worker PR #231

PR #231 contains useful exact symbol reconstruction, but two parts of its
published REVIEW terminal are not accepted as load-bearing by this parent.

### 3.1 Polarized block is genuinely nonsymmetric

This part is correct:

\[
H_{AA}\neq H_{AA}^{\mathsf T}.
\]

Therefore the earlier parent draft's symmetric-KKT/radical discussion is
withdrawn. No symmetric Hessian argument is used in the terminal no-go.

### 3.2 The published \(N_0\) refinement uses the wrong stack

The worker brief defines

\[
N=\ker H_{AA},
\qquad
N_0=\ker H_{AA}\cap\ker H_{QA}.
\]

Its own checker first computes \(N=\ker H_{AA}\), but then constructs

\[
\ker
\begin{pmatrix}
H_{AA}^{\mathsf T}\\
H_{QA}
\end{pmatrix}
\]

instead of

\[
\ker
\begin{pmatrix}
H_{AA}\\
H_{QA}
\end{pmatrix}.
\]

The checker subsequently verifies that the vectors it found also happen to lie
in \(\ker H_{AA}\); that does not prove it found the entire intersection.

A corrected exact replay of the same symbol gives

\[
\dim N_0=
(1,0,0,0,4,1,0,1,0)
\]

on orbit types \(0,\ldots,8\), respectively. In particular the two
one-dimensional sectors on orbit 5 and orbit 7 do **not** disappear.

The exact missing bases are:

### orbit 5, phase ids \((1,1,3,3)\)

\[
\begin{aligned}
&(0,-1+i),\ (6,-1+i),\\
&(12,1),\ (14,-1),\ (16,1),\\
&(18,1),\ (19,-1),\ (21,1).
\end{aligned}
\]

### orbit 7, phase ids \((2,1,1,2)\)

\[
(2,1),\ (7,-i),\ (8,i),\ (11,-i),\
(12,-i),\ (14,i),\ (16,-i),\ (20,1).
\]

The original 1/1/4 residual expectation is therefore restored.

### 3.3 The published full mixed-Hessian table is malformed

The worker checker constructs its \(34\times34\) matrix as

\[
\operatorname{vstack}
\left(
[0_{10\times10}\mid Q],
[H_{AA}\mid0_{24\times10}]
\right).
\]

The upper row uses the column partition \((10,24)\), while the lower row places
the \(24\times24\) block in the **first** 24 columns. Those column partitions
are incompatible. Consequently the reported full-joint rank/nullity/mixed
table is not a valid block operator and is not used here.

These worker-remediation points matter for the registry, but the exact
diagonal no-go below is independent of them.

---

## 4. Exact diagonal invisible generator

Use the standard Lorentz basis

\[
(K_1,K_2,K_3,J_{12},J_{13},J_{23})
\]

and define

\[
Y=J_{12}-J_{13}+J_{23}.
\]

This is the Role-0 source-invisible diagonal direction already identified by
#235.

It satisfies

\[
Y^3+3Y=0.
\]

Also define the boost sum

\[
B=K_1+K_2+K_3.
\]

A direct Lie-algebra calculation gives

\[
\boxed{[B,Y]=0.}
\]

This commutation is the key exact cancellation missed by the finite Taylor
expansion.

---

## 5. Exact analytic family

Use the Cayley coordinate on the same one-parameter subgroup,

\[
U(z)
=
\left(I-\frac z2Y\right)^{-1}
\left(I+\frac z2Y\right).
\]

For real \(z\) near zero,

\[
U(-z)=U(z)^{-1},
\qquad
U(z)^T\eta U(z)=\eta.
\]

On every torus with side length divisible by four, put

\[
p(x)=x_0+x_1+x_2+x_3\pmod4
\]

and

\[
(W_0,W_1,W_2,W_3)
=
(U,I,U^{-1},I).
\]

Define

\[
\boxed{
L_0(x)=W_{p(x)},
\qquad
L_s(x)=I\quad(s=1,2,3).
}
\tag{5.1}
\]

This is a reparameterization of the same local analytic subgroup used by
#235's exponential cosine family. No new branch or action is introduced.

---

## 6. Curvature is exact and nonzero

For every \(s=1,2,3\),

\[
P_{0s}(x)
=
W_pW_{p+1}^{-1}.
\]

Hence by phase

\[
P_{0s}
=
(U,U,U^{-1},U^{-1}),
\]

while every spatial plaquette is the identity.

For

\[
\mathcal R(P)=\frac12(P-P^{-1}),
\]

the certificate proves

\[
\boxed{
\mathcal R(U)
=
\frac{4z}{4+3z^2}\,Y.
}
\tag{6.1}
\]

Since

\[
\lim_{z\to0}
\frac1z\frac{4z}{4+3z^2}
=1,
\]

the branch has nonzero plaquette curvature for every sufficiently small
\(z\neq0\).

Thus this is not a flat connection family.

---

## 7. Exact metric equation

At standard solder, the complementary area of a face \((0,s)\) is spatial.
The Hodge dual of the rotation bivector \(b(Y)\) lies in the boost sector.
Their degree-two Lorentz pairing vanishes.

The certificate checks all three cell functionals:

\[
G_2(B_{(0,s)^c},\star b(Y))=0.
\]

More importantly, it checks the full solder/Gram differential. For each of
the \(16\) independent leg variations, the oriented sum over
\((0,1),(0,2),(0,3)\) vanishes identically.

Therefore the statement is not merely that the restricted action is zero:

\[
\boxed{
E_Q(\eta,K(z))=0
}
\tag{7.1}
\]

as the full descended metric partial, for every \(z\) in the chart.

This reproduces and strengthens the exact metric part of #235.

---

## 8. Exact connection equation

The finite curvature differential is the owned identity

\[
D\mathcal R_P[\dot P]
=
\frac12
\left(
\dot P+P^{-1}\dot P P^{-1}
\right).
\tag{8.1}
\]

The proof checks one edge at a time against all six Lorentz generators.

### 8.1 Role-0 edge

Let

\[
A=W_p,\qquad
C=W_{p+1},\qquad
D=W_{p-1}.
\]

The varied Role-0 edge meets six nontrivial faces. After summing the three
complementary face functionals, the relevant covector is

\[
\ell_B(X)=\frac12\operatorname{tr}(BX).
\]

For an arbitrary Lorentz generator \(G\), the two incident base-site
contributions reduce to

\[
\frac12\ell_B
\left(
AGC^{-1}
+
CGA^{-1}
-
DGA^{-1}
-
AGD^{-1}
\right).
\tag{8.2}
\]

At phases \(p=0,2\) the matrix terms cancel directly.

At phases \(p=1,3\), cyclicity of trace together with

\[
[B,U]=0
\]

pairs the remaining two terms exactly. Hence

\[
\boxed{
E_{K,0}(x)[G]=0
}
\]

for every phase and every \(G\in\mathfrak{so}(1,3)\).

### 8.2 Spatial Role edge

For a Role-\(s\) edge, \(s=1,2,3\), the two nontrivial \((0,s)\) face
contributions are evaluated separately.

For every phase and every Lorentz generator \(G\), their exact sum vanishes.
No commutation hypothesis is required for this cancellation.

The remaining spatial-spatial faces are identity plaquettes at constant solder.
Their two appearances of the edge form the flat forward curl, and since

\[
D\mathcal R_I=\operatorname{id},
\]

they telescope exactly.

Thus

\[
\boxed{
E_{K,s}(x)[G]=0
\qquad
(s=1,2,3)
}
\]

for every site and all six independent generators.

The parent checker executes

\[
4\times
\left(
6+3\times6
\right)
=
96
\]

independent nontrivial edge-Euler identities, all exactly over \(\mathbb Q(z)\).

Therefore

\[
\boxed{
E_K(\eta,K(z))=0
}
\tag{8.3}
\]

identically, not merely through order eight.

---

## 9. The branch is not pure gauge

All three spatial links are the identity.

If (5.1) were a pure gauge image of the identity while preserving those side
links, the gauge function would be constant along the three spatial
directions. The Role-0 link could then depend only on \(x_0\).

But \(L_0(x)\) depends on

\[
p(x)=x_0+x_1+x_2+x_3\pmod4.
\]

There are sites with the same \(x_0\) and different spatial sums carrying
different phases \(U\) and \(I\). Therefore the branch is not that gauge orbit.

Together with the nonzero plaquette curvature, this gives a direct
gauge-invariant obstruction to interpreting the curve as flat.

---

## 10. Exact joint no-go

Sections 6–9 give an analytic family through the flat point with

\[
K(0)=I,
\]

such that for every sufficiently small nonzero \(z\),

\[
\boxed{
E_K(\eta,K(z))=0,
\qquad
E_Q(\eta,K(z))=0,
\qquad
\mathcal R(P)\neq0.
}
\tag{10.1}
\]

The family is physical in the only sense needed for this task: it is not a
pure-gauge flat connection and carries nonzero plaquette curvature.

Therefore the zero-source joint normal set is not isolated. No positive
Brouwer-degree/Łojasiewicz/Puiseux argument can force all invisible UV
amplitudes to \(O(h^\infty)\), because the centered zero-source germ already
contains a nontrivial exact analytic curve.

This directly kills the requested local uniqueness statement.

---

## 11. What this does **not** kill

The no-go must be kept sharply scoped.

### 11.1 It does not kill the smooth Einstein coefficient

On the designated regular IR branch, #201/#216/#223 still give

\[
h^{-2}E_{\star,Q}
=
-\frac12G+O(h)
\]

under their stated smooth-realization hypotheses.

Nothing in the exact diagonal curve changes the #201 coefficient.

### 11.2 It does not produce a wrong metric response at flat \(Q\)

Along the exact curved joint-vacuum curve,

\[
Q=\eta,
\qquad
E_Q=0.
\]

Since

\[
G[\eta]=0,
\]

the metric response agrees with the flat vacuum value despite the hidden
curved connection.

Thus this result obstructs **connection/Palatini local uniqueness**, not the
pointwise vacuum metric equation itself.

### 11.3 It does not justify adding torsion-free by hand

Merged #233 is diagnostic only. The no-go is obtained from the unchanged
joint equations. No torsion equation is added to remove the curve.

### 11.4 It does not prove that every sourced smooth branch is bad

For nonzero smooth \(T\), source-visible sectors such as #227 are strongly cut
by the metric equation. The present obstruction is already enough because the
target included the vacuum local branch.

A narrower theorem about existence of one designated smooth branch, or about
metric-response independence despite nonunique hidden connections, remains a
separate possible research target. It is not the uniqueness theorem requested
here.

---

## 12. Relation to the original 4/1/1 strategy

The original strategy expected residual source-invisible orbit dimensions

\[
(4,1,1).
\]

The corrected replay of #231 restores exactly that expectation.

However the diagonal four-dimensional sector already contains the exact
analytic curve (10.1). Therefore the one-dimensional workers are no longer
load-bearing for this EXPENSIVE terminal.

They may still be useful for a later classification of the complete joint
critical set, but no result on those sectors can restore local uniqueness once
(10.1) exists.

---

## 13. Validation

Parent exact certificate:

\[
\texttt{a4d\_joint\_palatini\_exact\_diagonal\_vacuum\_check.py}.
\]

The exact replay checks:

- Lorentz subgroup and inverse identities;
- \([B,Y]=0\);
- exact curvature formula (6.1);
- all three zero cell-density pairings;
- all \(16\) metric Euler components;
- \(96\) independent nontrivial edge-Euler identities;
- flat spatial-face telescoping;
- non-gauge phase witness;
- nonzero first curvature coefficient.

No numerical root tolerance or finite-order Taylor truncation is used in the
terminal proof.

---

## 14. Final disposition

The task asked for either

\[
\texttt{NAKED-STAR-JOINT-PALATINI-SMOOTH-EINSTEIN-BRANCH-CLOSED}
\]

or an exact joint no-go.

The exact result is

\[
\boxed{
\texttt{NAKED-STAR-JOINT-PALATINI-LOCAL-UNIQUENESS-NOGO}.
}
\]

Reason:

\[
\boxed{
\exists\ \text{analytic curved non-gauge }K(z)\to I:
\quad
E_K(\eta,K(z))=E_Q(\eta,K(z))=0.
}
\]

The selected naked-star joint equations therefore do not by themselves isolate
the LC-like smooth connection branch.

The already-owned IR Einstein coefficient remains intact and may support a
future **selected-branch or metric-response-only** theorem, but that theorem
must not be advertised as local uniqueness of the joint Palatini critical set.
