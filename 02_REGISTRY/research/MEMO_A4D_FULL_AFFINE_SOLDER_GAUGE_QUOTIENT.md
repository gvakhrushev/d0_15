# MEMO A4D — full affine solder gauge quotient

**Task:** \`CTRL-A4D-FULL-AFFINE-SOLDER-GAUGE-QUOTIENT\`  
**Execution:** PR #178  
**Status:** terminal CONTROL research classification  
**Motivation:** close or sharpen the full-affine quotient blocker exposed by PR #175

## 0. Principal verdict

The previous blocker

\[
\texttt{FULL-AFFINE-SOLDER-GAUGE-QUOTIENT-MISSING}
\]

splits into two mathematically distinct questions.

The first question is constructive:

> can the raw solder/coframe be given an exact finite action of the affine node
> gauge which extends the owned pure-linear frame action and reproduces the
> owned flat translation chart?

On the raw solder **alone**, the natural affine-linear answer is no. A fixed
translation-to-row intertwiner \(M\) must satisfy

\[
g^T M g=M
\]

for every Lorentz frame \(g\), so the intertwiner space is exactly

\[
\mathbb R\,\eta .
\]

The owned flat chart instead identifies the translation vector components
directly with the raw coframe row, which requires \(M=I\). The two coincide
only in the Euclidean case, not for Lorentz signature.

However D0 already owns exactly the moving intertwiner needed to repair this:
the observer-positive metric

\[
h_n=-\eta+2n^\flat\otimes n^\flat,
\qquad
h_{n_0}=I.
\]

With the observer transported together with the frame, \`observerFlat\`
transforms contragrediently. This gives an exact semidirect affine action on
the enlarged already-owned carrier

\[
(A_{\rm lin},e,n).
\]

So the representation blocker is **not terminal**.

The second question is the actual kill gate:

> is the accepted canonical \(\star\)-density invariant under this finite
> affine translation action, so that a nonlinear affine gauge quotient of its
> Euler equations exists?

The answer is no.

An exact rational \(L=2\) full-torus witness gives

\[
\boxed{
S_\star[e,A]=-\frac23,
\qquad
S_\star[e^c,A]=-\frac43
}
\]

under a pure node translation \(c\), while the same certificate verifies exact
proper-Lorentz invariance.

Therefore the terminal verdict is

\[
\boxed{
\texttt{STAR-DENSITY-NONLINEAR-AFFINE-TRANSLATION-SYMMETRY-NOGO}.
}
\]

This is a no-go for treating the **full affine translation subgroup** as an
off-shell gauge symmetry of the already-selected finite \(\star\)-density.

Consequently there is no full nonlinear affine-gauge physical quotient
\(d_P\) for this action as it stands.

PR #175's scoped flat statement

\[
d_{P,\mathrm{flat},L=2}=1
\]

is not contradicted: at zero curvature the translation variation vanishes, so
the forward-coframe directions are exact flat Hessian nulls. This PR proves
that they do **not** extend to a global off-shell affine gauge orbit on curved
backgrounds.

The new strongest blocker is therefore not "missing gauge action" but

\[
\boxed{
\texttt{AFFINE-TRANSLATION-NOT-OFFSHELL-SYMMETRY-OF-STAR-DENSITY}.
}
\]

Any attempt to restore a full affine translation quotient must either:

1. enlarge/change the action by independently justified
   translation-compensating terms; or
2. prove a separate on-shell symmetry mechanism after constraints.

Neither is owned. In particular PR #175 already killed the shortcut that
identifies the finite connection equation with the naive torsion equation.

Exact certificate:

\`02_REGISTRY/research/certificates/a4d_full_affine_solder_gauge_quotient_check.py\`.

---

## 1. Scope and independence from PR #175 acceptance

PR #175 motivated this task by isolating a full-affine quotient boundary after
a flat quadratic pressure test.

The classification in this memo does not require accepting PR #175's
\(d_E,d_P\) bookkeeping. It uses only owners already on \`main\`:

- \`ArchiveAffineCartanConnection\`: affine node gauge, linear/shift laws and
  exact flat translation chart;
- \`A4DRawSolderFrameAction\`: right action on the full raw solder;
- \`A4DObserverPositiveExterior\`: moving observer metric and
  \`observerFlat\` contragredience;
- \`A4DAffineOriginSolderBoundary\`: exact distinction between affine-point and
  linear-only solder covariance;
- the accepted Role-bivector \(\star\)-density packet on main.

Thus PR #178 can be reviewed independently from PR #175.

---

## 2. Types and conventions

Let

\[
V=\operatorname{RoleSpace},
\qquad
\eta=\operatorname{diag}(1,-1,-1,-1).
\]

For the positive Role edge

\[
y=x+r,
\]

write the affine link as

\[
A_{x,r}(z)=L_{x,r}z+b_{x,r}.
\]

A node affine gauge is

\[
h_x(z)=g_xz+c_x.
\]

The exact connection gauge law is

\[
L'_{x,r}
=
g_xL_{x,r}g_y^{-1},
\tag{2.1}
\]

\[
b'_{x,r}
=
g_xb_{x,r}
+
c_x
-
L'_{x,r}c_y.
\tag{2.2}
\]

Define the inhomogeneous translation cocycle

\[
\boxed{
\tau_{x,r}(h;L)
=
c_x-L'_{x,r}c_y.
}
\tag{2.3}
\]

Then

\[
b'=g_xb+\tau.
\]

The raw solder matrix is

\[
\Theta_x=\eta+e_x
\]

with Role-labelled rows \(\Theta_{x,r}\). The owned solder vector is

\[
v_r(e,x)=\eta\,\Theta_{x,r}^T.
\tag{2.4}
\]

If the vector frame is \(g_x\), the corresponding owned right row frame is

\[
\Lambda_x=g_x^{-1}.
\]

For \(c=0\), the existing raw solder action is

\[
\boxed{
\Theta'_x=\Theta_x\Lambda_x.
}
\tag{2.5}
\]

---

## 3. Why a fixed same-carrier affine-linear completion fails

Consider the natural affine-linear row extension

\[
\Theta'_{x,r}
=
\Theta_{x,r}\Lambda_x
+
\tau_{x,r}^TM
\tag{3.1}
\]

with one fixed \(4\times4\) matrix \(M\).

The affine group law contains the semidirect relation

\[
(g,0)(I,\tau)(g,0)^{-1}
=
(I,g\tau).
\]

For (3.1) to respect it,

\[
(g\tau)^TM
=
\tau^TMg^{-1}
\]

for all \(\tau\), hence

\[
\boxed{
g^TMg=M.
}
\tag{3.2}
\]

Infinitesimally,

\[
X^TM+MX=0,
\qquad
X\in\mathfrak{so}(1,3).
\tag{3.3}
\]

The exact rational system has 16 unknowns and rank 15:

\[
\dim\{M:X^TM+MX=0\}=1.
\]

The unique line is

\[
\boxed{
M\in\mathbb R\eta.
}
\tag{3.4}
\]

This is the ordinary uniqueness of the Lorentz-invariant bilinear form on the
vector representation.

### 3.1 Conflict with the owned flat translation chart

The repository's exact theorem
\`affineTranslation_flat_eq_forwardGaugeCoframe\` identifies the flat affine
shift components directly with the raw coframe components.

For a flat link and pure translation gauge,

\[
e'_r=\tau_r.
\tag{3.5}
\]

Thus (3.1) must reduce to

\[
\tau^TM=\tau^T
\]

for arbitrary \(\tau\), which requires

\[
M=I.
\tag{3.6}
\]

But \(I\notin\mathbb R\eta\).

For the exact spacelike control

\[
\tau=e_B,
\]

the Lorentz-compatible choice gives

\[
e_B^T\eta=-e_B^T,
\]

while the owned chart gives \(+e_B^T\).

Hence:

\[
\boxed{
\text{raw solder alone has no fixed-intertwiner affine-linear action
satisfying both Lorentz composition and the owned flat chart.}
}
\tag{3.7}
\]

This is a scoped representation no-go, not a universal no-go against
state-dependent or enlarged carriers.

---

## 4. The already-owned observer metric repairs the representation mismatch

D0 owns

\[
h_n
=
-\eta+2n^\flat\otimes n^\flat.
\tag{4.1}
\]

For the rest observer \(n_0\),

\[
\boxed{
h_{n_0}=I.
}
\tag{4.2}
\]

When an allowed Lorentz frame \(g\) moves the observer,

\[
n'=gn,
\]

the observer form obeys inverse congruence

\[
\boxed{
h_{n'}
=
g^{-T}h_ng^{-1}.
}
\tag{4.3}
\]

At the typed level this is exactly the already-owned
\`observerFlat_contragredient\` law.

Therefore \(h_n\) is a moving vector-to-covector intertwiner which:

- equals the direct coordinate identification at the rest observer;
- transforms with the contragredient representation required by the solder
  row;
- does not identify a Lorentz vector with a covector by a fixed Euclidean
  matrix.

This is the missing representation-theoretic ingredient.

It is already owned; no external observer is introduced.

---

## 5. Exact observer-completed affine solder action

Let

\[
n'_x=g_xn_x,
\qquad
H'_x:=h_{n'_x}.
\]

Define, row by row,

\[
\boxed{
\Theta'_{x,r}
=
\Theta_{x,r}g_x^{-1}
+
\tau_{x,r}^TH'_x.
}
\tag{5.1}
\]

Equivalently, the added row is

\[
\operatorname{observerFlat}(n'_x,\tau_{x,r}).
\]

The background variables transform simultaneously by

\[
L'_{x,r}=g_xL_{x,r}g_y^{-1},
\qquad
n'_x=g_xn_x.
\tag{5.2}
\]

### 5.1 Pure-linear restriction

If \(c=0\),

\[
\tau=0,
\]

and (5.1) becomes exactly

\[
\Theta'=\Theta g^{-1},
\]

the owned \`rawFullSolderFrameAction\`.

### 5.2 Flat pure translation restriction

Take

\[
L=I,
\qquad
g=I,
\qquad
n=n_0.
\]

Then

\[
H'=I
\]

and

\[
\Theta'_{x,r}
=
\Theta_{x,r}
+
(c_x-c_y)^T.
\tag{5.3}
\]

For the repository's \`translationGauge\`,

\[
c_x=-\operatorname{forwardDifferenceScale}(N)\,\xi(x),
\]

so

\[
c_x-c_y
=
\operatorname{forwardDifferenceScale}(N)
\bigl(\xi(y)-\xi(x)\bigr)
=
d_f\xi(x,r).
\]

Therefore

\[
\boxed{
e'=d_f\xi
}
\tag{5.4}
\]

literally reproduces
\`affineTranslation_flat_eq_forwardGaugeCoframe\`.

This closes the flat-chart requirement without changing conventions.

---

## 6. Exact composition law

Take two node gauges

\[
h=(g,c),
\qquad
k=(p,d).
\]

At the target site,

\[
(kh)_x
=
(p_xg_x,\;p_xc_x+d_x).
\]

The linear link transforms successively in the usual way.

For the translation cocycle,

\[
\tau_h
=
c_x-L^hc_y,
\]

\[
\tau_k
=
d_x-L^{kh}d_y.
\]

A direct calculation gives

\[
\boxed{
\tau_{kh}
=
p_x\tau_h+\tau_k.
}
\tag{6.1}
\]

The observer form after both transformations is

\[
H^{kh}_x
=
p_x^{-T}H^h_xp_x^{-1}.
\tag{6.2}
\]

Hence

\[
(p_x\tau_h)^TH^{kh}_x
=
\tau_h^TH^h_xp_x^{-1}.
\tag{6.3}
\]

Using (6.1)-(6.3),

\[
\begin{aligned}
(\Theta^h)^k
&=
\left(
\Theta g_x^{-1}
+
\tau_h^TH^h_x
\right)p_x^{-1}
+
\tau_k^TH^{kh}_x
\\
&=
\Theta(p_xg_x)^{-1}
+
\tau_{kh}^TH^{kh}_x
\\
&=
\Theta^{kh}.
\end{aligned}
\]

Thus

\[
\boxed{
\Phi_k\circ\Phi_h=\Phi_{kh}.
}
\tag{6.4}
\]

The exact certificate verifies this over a nontrivial rational boost/rotation
pair with nonzero source and target translations.

So the full-affine **representation** problem is constructively closed on the
already-owned \((e,n)\) enlargement.

---

## 7. What this construction does not do

Equation (5.1) supplies a gauge action. It does not imply that a given action
functional is invariant under that gauge action.

That distinction is load-bearing.

The accepted finite \(\star\)-density is

\[
\mathcal L_\star(S,x)
=
c\,\epsilon_S
G_2\left(
B_{S^c}(e,x),
\star\,\mathfrak b
\left(
\frac12(P_S-P_S^{-1})
\right)
\right).
\tag{7.1}
\]

It depends on:

- the linear plaquette holonomy;
- the raw solder legs.

It does **not** contain:

- the affine link shift \(b\);
- the observer \(n\);
- a torsion term;
- an independent translation compensator.

Under a pure node translation,

\[
g=I.
\]

Therefore:

- every linear link \(L\) is unchanged;
- every linear plaquette \(P_S\) is unchanged;
- the curvature bivector \(C_S\) is unchanged;
- the observer is unchanged;
- only the raw solder changes.

At general \(n\), define

\[
s_r
=
\eta H_n\tau_r
\]

for the corresponding solder-vector increment.

Then

\[
v'_r=v_r+s_r.
\tag{7.2}
\]

For \(S^c=\{u,v\}\),

\[
B'_{S^c}
=
B_{S^c}
+
s_u\wedge v_v
+
v_u\wedge s_v
+
s_u\wedge s_v.
\tag{7.3}
\]

Therefore the exact finite density change is

\[
\boxed{
\Delta\mathcal L_\star
=
c\,\epsilon_S
G_2\left(
s_u\wedge v_v
+
v_u\wedge s_v
+
s_u\wedge s_v,
\star C_S
\right).
}
\tag{7.4}
\]

There is no algebraic reason for (7.4) to vanish on a curved background.

The next section gives an exact full-periodic counterexample.

---

## 8. Exact \(L=2\) curved translation counterexample

Use the period-two four-Role torus

\[
X=(\mathbb Z/2)^4.
\]

Set all linear links to identity except at the origin \(o\):

1. the \(A\)-link carries the rational \(A/B\) boost

\[
G_{AB}
=
\begin{pmatrix}
5/3&4/3&0&0\\
4/3&5/3&0&0\\
0&0&1&0\\
0&0&0&1
\end{pmatrix};
\]

2. the \(B\)-link carries the \(B/C\) quarter-turn

\[
R_{BC}
=
\begin{pmatrix}
1&0&0&0\\
0&0&1&0\\
0&-1&0&0\\
0&0&0&1
\end{pmatrix}.
\]

Both satisfy

\[
L^T\eta L=\eta.
\]

Take the flat raw coframe

\[
e=0
\]

and rest observer

\[
n=n_0.
\]

Using the exact accepted finite extraction

\[
\mathcal R(P)=\frac12(P-P^{-1})
\]

and summing all 16 sites and all six Role two-faces, the exact rational action
is

\[
\boxed{
S_\star^{\rm before}=-\frac23.
}
\tag{8.1}
\]

Now apply a pure node translation with

\[
c_o=e_B,
\qquad
c_x=0
\quad(x\ne o).
\tag{8.2}
\]

Because \(n=n_0\),

\[
H_n=I,
\]

so (5.1) gives exactly

\[
e'_{x,r}
=
c_x-L_{x,r}c_{x+r}.
\tag{8.3}
\]

The linear links and all plaquette curvatures are unchanged.

The full exact action becomes

\[
\boxed{
S_\star^{\rm after}=-\frac43.
}
\tag{8.4}
\]

Hence

\[
\boxed{
\Delta S_\star=-\frac23\ne0.
}
\tag{8.5}
\]

This is an off-shell finite periodic counterexample. It is not a local-density
artifact and not a boundary-effect claim.

Therefore pure node translations are not a symmetry of the accepted action.

---

## 9. Proper-Lorentz positive control

On the same curved \(L=2\) background, apply the rational boost \(G_{AB}\)
globally:

\[
L'_{x,r}
=
G_{AB}L_{x,r}G_{AB}^{-1},
\]

\[
\Theta'_x
=
\Theta_xG_{AB}^{-1}.
\]

The exact certificate gives

\[
\boxed{
S_\star'=S_\star=-\frac23.
}
\tag{9.1}
\]

Thus the failure in (8.5) is not a generic frame-covariance bug in the
certificate.

The accepted density passes the proper-Lorentz control and fails specifically
at the affine translation subgroup.

---

## 10. Why the flat Hessian nulls survive

For a flat linear connection,

\[
P_S=I,
\qquad
C_S=0.
\]

Therefore

\[
\mathcal L_\star=0
\]

for every coframe, including a translated one.

The certificate verifies both

\[
S_\star[0,I]=0
\]

and

\[
S_\star[e^c,I]=0.
\]

This explains why the forward-coframe directions can be exact Hessian nulls at
the flat background while failing to define a global symmetry.

The implication

\[
\text{flat Hessian null}
\Longrightarrow
\text{nonlinear gauge direction}
\]

is false here.

---

## 11. Consequence for \(d_P\)

The action family remains the already-selected one-dimensional family

\[
S_c=cS_\star.
\]

The present task does not alter \(d_A\).

A physical operator quotient by a transformation requires that transformation
to be an actual redundancy/symmetry of the action or of a separately proved
on-shell constraint system.

Equation (8.5) shows that full affine translations are not an off-shell
symmetry.

Therefore the quotient

\[
\operatorname{EL}(S_\star)/
\{\text{full affine node translations}\}
\]

is not a defined gauge quotient of this action.

So:

\[
\boxed{
d_{P,\mathrm{full\ affine}}
\text{ is not defined for the accepted action as an off-shell gauge quotient.}
}
\tag{11.1}
\]

This is stronger than saying merely that the quotient owner is missing.

It says the obvious quotient would be mathematically wrong.

---

## 12. Relation to the finite torsion boundary

One possible continuum-inspired escape would be:

1. vary the connection;
2. prove an exact torsion constraint;
3. show affine translations become an on-shell redundancy;
4. quotient only after imposing the constraint.

That route is not available yet.

PR #175's exact hostile control found that the finite connection Euler equation
is not identical to the naive forward torsion equation for the accepted
placement.

Therefore this PR does not replace the off-shell failure (8.5) by an unproved
on-shell claim.

No statement of the form

\[
D(e\wedge e)=0\Rightarrow T=0
\]

or

\[
\text{translation}=\text{diffeomorphism on shell}
\]

is made here.

---

## 13. Independent affine shift remains distinct

The construction (5.1) does not set the affine connection shift \(b\) equal to
the coframe.

The exact affine connection still transforms by

\[
b'=g_xb+\tau.
\]

The raw solder transforms independently by (5.1).

A nonzero independent \(b\) is therefore not silently erased.

This preserves the established distinction between:

- affine link translation data;
- raw coframe/solder data;
- their exact coincidence only on the specific flat translation-gauge chart.

The action (7.1) remains blind to \(b\); that blindness is part of why no
translation compensation exists in the accepted density.

---

## 14. What would be required to restore a full affine translation symmetry

Equation (8.5) means a repair cannot be a mere change of quotient language.

It must change the mathematical system.

There are only two honest routes.

### 14.1 Enlarge the action

Add independently justified terms whose pure-translation variation cancels
(7.4).

Natural candidates would have to involve data not present in (7.1), such as:

- affine shift / torsion;
- an exact sourced overlap field;
- another covariant cell term.

But this reopens the action-family problem:

\[
d_A=1
\]

for the accepted linear-curvature insertion no longer implies uniqueness of the
**enlarged** action.

Any such term needs its own TYPE/Hom-space/symmetry/variation classification.

### 14.2 Prove an on-shell symmetry

Derive a finite constraint system under which (7.4) vanishes or becomes a
constraint combination.

That requires a new exact theorem relating the selected connection Euler
equation to the relevant solder/affine translation defect.

Current owners do not supply it.

These are research forks, not hidden assumptions.

---

## 15. The observer metric's exact role

The observer field closes a representation problem here. It does **not**
select a physical reference or make translations a symmetry.

This is consistent with the earlier labelled-reference packet:

- \(h_n\) is a canonical positive, frame-covariant pairing;
- it does not select the missing \(A/e\) overlap;
- full-affine covariance alone does not select the reference section.

The new result is narrower:

> the same \(h_n\) supplies the exact moving vector-to-row intertwiner
> needed for the affine solder transformation law.

This is a constructive reuse of an existing owner, not a new observer
postulate.

---

## 16. Theorem-ready statements

1. **Fixed-intertwiner equation.**  
   For the affine-linear raw solder law
   \[
   \Theta'=\Theta g^{-1}+\tau^TM,
   \]
   affine semidirect composition requires
   \[
   g^TMg=M.
   \]

2. **Lorentz invariant-form dimension.**  
   The exact infinitesimal system
   \[
   X^TM+MX=0
   \]
   has rank 15 in 16 unknowns.

3. **Unique fixed intertwiner.**  
   \[
   M\in\mathbb R\eta.
   \]

4. **Owned-chart incompatibility.**  
   Exact flat translation calibration requires \(M=I\), so no fixed
   same-carrier intertwiner satisfies both requirements.

5. **Rest observer repair.**  
   \[
   h_{n_0}=I.
   \]

6. **Moving observer congruence.**  
   \[
   h_{gn}=g^{-T}h_ng^{-1}.
   \]

7. **Observer-flat contragredience.**  
   \(\operatorname{observerFlat}(gn,gv)\) is the right-contragredient transform
   of \(\operatorname{observerFlat}(n,v)\).

8. **Affine solder action.**  
   \[
   \Theta'_{x,r}
   =
   \Theta_{x,r}g_x^{-1}
   +
   \tau_{x,r}^Th_{g_xn_x}.
   \]

9. **Translation cocycle.**  
   For successive gauges \(h=(g,c)\), \(k=(p,d)\),
   \[
   \tau_{kh}=p_x\tau_h+\tau_k.
   \]

10. **Exact composition.**  
    The action in Proposition 8 satisfies
    \[
    \Phi_k\Phi_h=\Phi_{kh}.
    \]

11. **Pure-linear recovery.**  
    With \(c=0\), Proposition 8 is exactly the owned
    \`rawFullSolderFrameAction\`.

12. **Flat translation recovery.**  
    At \(L=I,n=n_0,g=I\), Proposition 8 gives exactly
    \[
    e'=d_f\xi
    \]
    for the owned \`translationGauge\`.

13. **Pure translation curvature invariance.**  
    The linear plaquette curvature is unchanged by a pure node translation.

14. **Exact solder-density variation.**  
    Under a pure translation, the complete density change is (7.4).

15. **Curved finite counterexample.**  
    The explicit period-two Lorentz-link configuration of §8 satisfies
    \[
    S_\star=-2/3,\qquad S_\star^c=-4/3.
    \]

16. **Proper-Lorentz positive control.**  
    A global rational proper Lorentz frame leaves the same action exactly
    unchanged.

17. **Off-shell affine-translation no-go.**  
    The full affine translation subgroup is not an off-shell gauge symmetry of
    the accepted \(\star\)-density.

18. **Flat-null/global-gauge distinction.**  
    Exact flat forward-coframe Hessian nulls do not imply a nonlinear affine
    translation gauge orbit.

19. **Full affine quotient no-go for current action.**  
    A physical quotient by full affine node translations is not defined for
    the accepted action without additional dynamics or an enlarged action.

---

## 17. Mandatory hostile controls

| Control | Result |
|---|---|
| fixed \(M=I\) flat chart | matches flat chart, fails Lorentz semidirect composition |
| fixed \(M=\eta\) | composes, fails spacelike flat chart |
| invariant \(M\) classification | rank 15, unique line \(\mathbb R\eta\) |
| observer rest metric | exactly \(I\) |
| observer boost congruence | exact |
| mixed boost/rotation + translations | observer-completed action composes exactly |
| pure-linear restriction | exact owned raw solder right action |
| flat pure translation | exact owned \`forwardGaugeCoframe\` |
| proper Lorentz star action | invariant |
| flat translation star action | zero before/after because curvature zero |
| curved pure translation star action | fails: \(-2/3\to-4/3\) |
| independent affine shift | remains separate; not absorbed |
| torsion-free shortcut | not used |
| Einstein/time/continuum interpretation | not used |

---

## 18. Terminal disposition

The investigation changes the frontier in a useful way.

We no longer need to say

\[
\text{"a full affine solder action is missing"}.
\]

A canonical exact affine action can be written on the already-owned
observer-extended carrier using \`observerFlat\`.

But that does **not** rescue the desired physical quotient.

The accepted finite \(\star\)-density fails exact pure-translation invariance on
a curved periodic background.

Therefore the terminal statement is

\[
\boxed{
\texttt{STAR-DENSITY-NONLINEAR-AFFINE-TRANSLATION-SYMMETRY-NOGO}.
}
\]

The strategic next gate is no longer representation theory. It is a choice
between:

- **Lorentz-only nonlinear quotient**, keeping affine translations as physical
  background data rather than gauge; or
- a genuinely new **translation-invariant action completion / on-shell
  constraint mechanism**.

That fork must be decided explicitly. It must not be hidden by quotienting flat
Hessian null directions as though they were already a global affine gauge
symmetry.


---

## Ready-state CONTROL audit

PR #178 is \`Lifecycle: REVIEW\`; the CONTROL task row remains present in the
branch manifest with state \`REVIEW\`, and the executable brief remains present,
as required for a Ready CONTROL PR. This audit-only commit changes no
mathematical result; it exists to run repository guards against the final
Ready-state contract.
