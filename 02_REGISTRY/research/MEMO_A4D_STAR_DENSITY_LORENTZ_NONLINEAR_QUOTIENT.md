# MEMO A4D — nonlinear local-Lorentz quotient of the canonical star density

**Task:** \`CTRL-A4D-STAR-DENSITY-LORENTZ-NONLINEAR-QUOTIENT\`  
**Execution:** PR #179  
**Status:** terminal CONTROL research classification  
**Baseline:** current main with accepted star-density variation pressure

## 0. Verdict

The canonical finite star density survives the **full finite site-dependent
proper-Lorentz quotient**.

The strongest honest statement is

\[
\boxed{
d_A=1,\qquad d_E=1,\qquad
d_{P,\mathrm{Lor},\mathrm{nd}}=1,
}
\]

where the last quantity is the descended nonlinear physical-operator family on
the open sector in which every raw solder matrix is nondegenerate.

More precisely:

1. the complete finite cell density is invariant under an arbitrary
   site-dependent proper-Lorentz frame field;
2. this invariance is cellwise, not a cancellation after summing cells;
3. the Euler covector is exactly gauge equivariant;
4. every infinitesimal local-Lorentz vertical direction satisfies the exact
   Noether identity;
5. at a critical point, every such vertical direction lies in the Hessian
   kernel;
6. on the nondegenerate solder sector the gauge action is free and proper, so
   the quotient is a genuine smooth principal quotient;
7. on that sector one has explicit complete gauge-invariant coordinates
   \[
   Q_x=\Theta_x\eta\Theta_x^T,\qquad
   K_{x,r}=\Theta_xL_{x,r}\Theta_{x+r}^{-1},
   \]
   together with the discrete component data needed to choose
   \(SO^+(1,3)\) rather than the full Lorentz group;
8. the descended action is not constant on the quotient, so the one-dimensional
   Euler/operator family does not disappear;
9. the degenerate solder locus has enhanced stabilizers, so the **global**
   orbit space is stratified/singular and must not be described as one
   principal bundle.

Thus the exact terminal is

\[
\boxed{
\texttt{STAR-DENSITY-NONLINEAR-LOCAL-LORENTZ-QUOTIENT-SURVIVES}.
}
\]

This result is independent of whether affine translations are later treated as
physical background data, completed into a new action, or recovered as an
on-shell symmetry.  No affine translation is quotiented in this PR.

Exact certificate:

\`02_REGISTRY/research/certificates/a4d_star_density_lorentz_nonlinear_quotient_check.py\`.

---

## 1. Configuration and gauge group

Let

\[
X=(\mathbb Z/L)^4
\]

be one finite Role torus, and

\[
V=\operatorname{RoleSpace},\qquad
\eta=\operatorname{diag}(1,-1,-1,-1).
\]

At each site \(x\), write the full raw solder matrix as

\[
\Theta_x=\eta+e_x.
\]

Its Role-\(r\) row is \(\Theta_{x,r}\), and the owned solder vector is

\[
v_r(e,x)=\eta\,\Theta_{x,r}^T.
\tag{1.1}
\]

For the positive edge \(y=x+r\), let the linear link be

\[
L_{x,r}:V_y\to V_x.
\]

The local proper-Lorentz gauge group is

\[
\mathcal G_L
=
\prod_{x\in X}SO^+(1,3)_x.
\]

For \(g=(g_x)\in\mathcal G_L\), the exact finite action is

\[
\boxed{
L'_{x,r}
=
g_xL_{x,r}g_{x+r}^{-1},
}
\tag{1.2}
\]

and, in the repository's right-row convention,

\[
\boxed{
\Theta'_x
=
\Theta_xg_x^{-1}.
}
\tag{1.3}
\]

Because

\[
g_x^T\eta g_x=\eta,
\]

equation (1.3) is exactly equivalent to the vector law

\[
\boxed{
v'_r(e',x)=g_xv_r(e,x).
}
\tag{1.4}
\]

No affine translation term is present anywhere in this task.

---

## 2. Based plaquette covariance

For a Role face \(S=\{r,s\}\), let

\[
P_S(x)
\]

be the based linear plaquette holonomy at \(x\).

The owned link gauge law immediately gives

\[
\boxed{
P'_S(x)=g_xP_S(x)g_x^{-1}.
}
\tag{2.1}
\]

Use the accepted exact finite curvature extraction

\[
\mathcal R(P)
=
\frac12(P-P^{-1}).
\]

Conjugation commutes with inversion, hence

\[
\boxed{
\mathcal R(P'_S)
=
g_x\mathcal R(P_S)g_x^{-1}.
}
\tag{2.2}
\]

Let

\[
\mathfrak b:
\mathfrak{so}(1,3)\to\Lambda^2V
\]

be the owned tangent-to-bivector weld.

Its Lorentz equivariance gives

\[
\boxed{
C'_S(x)
=
\rho_2(g_x)C_S(x),
}
\tag{2.3}
\]

where

\[
C_S(x)
=
\mathfrak b(\mathcal R(P_S(x)))
\]

and \(\rho_2\) is the induced degree-two exterior representation.

---

## 3. Complementary solder covariance

For the complementary Role pair

\[
S^c=\{u,v\},
\]

the accepted solder bivector is

\[
B_{S^c}(e,x)
=
v_u(e,x)\wedge v_v(e,x).
\]

Using (1.4),

\[
\boxed{
B'_{S^c}(e',x)
=
\rho_2(g_x)B_{S^c}(e,x).
}
\tag{3.1}
\]

The crucial point is that both \(B_{S^c}\) and \(C_S\) live in the same based
fiber \(V_x\).

No endpoint interpolation or cross-site pairing enters the density.

---

## 4. Exact cellwise invariance

The canonical density is

\[
\mathcal L_\star(S,x)
=
c\,\epsilon_S\,
G_2\left(
B_{S^c}(e,x),
\star C_S(x)
\right).
\tag{4.1}
\]

For proper Lorentz transformations,

\[
\rho_2(g)^T G_2\rho_2(g)=G_2,
\tag{4.2}
\]

and the oriented Lorentz middle-degree star obeys

\[
\boxed{
\star\rho_2(g)=\rho_2(g)\star.
}
\tag{4.3}
\]

The base Role-face orientation factor \(\epsilon_S\) is unchanged because this
is an internal frame change, not a Role/site permutation.

Therefore

\[
\begin{aligned}
\mathcal L'_\star(S,x)
&=
c\,\epsilon_S
G_2\left(
\rho_2(g_x)B_{S^c},
\star\rho_2(g_x)C_S
\right)
\\
&=
c\,\epsilon_S
G_2\left(
\rho_2(g_x)B_{S^c},
\rho_2(g_x)\star C_S
\right)
\\
&=
\mathcal L_\star(S,x).
\end{aligned}
\]

Hence

\[
\boxed{
\mathcal L_\star(g\cdot(A,e);S,x)
=
\mathcal L_\star(A,e;S,x)
}
\tag{4.4}
\]

for every site and every face separately.

The finite action

\[
S_\star[A,e]
=
\sum_x\sum_{S\in\binom{Role}{2}}
\mathcal L_\star(S,x)
\]

therefore satisfies

\[
\boxed{
S_\star[g\cdot(A,e)]
=
S_\star[A,e].
}
\tag{4.5}
\]

No periodic telescoping or integration-by-parts argument is used.

---

## 5. Exact finite site-dependent certificate

The exact rational checker uses the full \(L=2\) four-Role torus with:

- one rational \(A/B\) boost link;
- one \(B/C\) quarter-turn link;
- one \(C/D\) quarter-turn link at another site;
- nonzero raw solder perturbations;
- a gauge field taking 14 distinct proper-Lorentz matrices over the 16 sites.

For every gauge matrix it verifies

\[
g_x^T\eta g_x=\eta,
\qquad
\det g_x=1,
\]

\[
\rho_2(g_x)^TG_2\rho_2(g_x)=G_2,
\]

\[
\star\rho_2(g_x)=\rho_2(g_x)\star.
\]

It then transforms all 64 positive links and all 16 solder matrices.

The result is stronger than total-action invariance:

\[
\boxed{
\mathcal L'_\star(S,x)=\mathcal L_\star(S,x)
}
\]

for all

\[
16\times6=96
\]

site/face cells exactly over \(\mathbb Q\).

The summed action is consequently identical as a corollary.

---

## 6. Euler equivariance

Let the full finite configuration space be denoted by \(\mathcal C\), and let

\[
\Phi_g:\mathcal C\to\mathcal C
\]

be the finite local-Lorentz action.

Equation (4.5) is

\[
S_\star\circ\Phi_g=S_\star.
\tag{6.1}
\]

Define the Euler covector

\[
E_z:=dS_\star|_z.
\]

Differentiating (6.1) gives, for every tangent perturbation \(\delta z\),

\[
E_{\Phi_g(z)}
\left[
D\Phi_g|_z(\delta z)
\right]
=
E_z[\delta z].
\tag{6.2}
\]

Equivalently,

\[
\boxed{
E_{\Phi_g(z)}
=
\left(D\Phi_g|_z^{-1}\right)^*E_z.
}
\tag{6.3}
\]

Therefore the critical locus is exactly gauge invariant:

\[
\boxed{
E_z=0
\Longrightarrow
E_{\Phi_g(z)}=0.
}
\tag{6.4}
\]

This is the finite nonlinear Euler covariance needed before any quotient is
called physical.

---

## 7. Infinitesimal local-Lorentz Noether identity

Let

\[
X=(X_x)_{x\in X},
\qquad
X_x\in\mathfrak{so}(1,3).
\]

For the one-parameter gauge field \(g_x(t)=\exp(tX_x)\), the vertical tangent
is

\[
\boxed{
\delta_X\Theta_x=-\Theta_xX_x,
}
\tag{7.1}
\]

\[
\boxed{
\delta_XL_{x,r}
=
X_xL_{x,r}
-
L_{x,r}X_{x+r}.
}
\tag{7.2}
\]

Differentiating the exact finite symmetry gives

\[
\boxed{
E_z[V_X(z)]=0
}
\tag{7.3}
\]

for every local Lie-algebra field \(X\) and every configuration \(z\).

This is the exact finite-lattice local-Lorentz Noether identity.

It is not a continuum conservation law.

---

## 8. Hessian vertical kernel at a critical point

Let \(z\) be a critical configuration,

\[
E_z=0.
\]

Differentiate (7.3) in an arbitrary direction \(\delta z\).

The derivative contains:

\[
H_z(V_X(z),\delta z)
+
E_z[D_{\delta z}V_X].
\]

The second term vanishes because \(E_z=0\).

Thus

\[
\boxed{
H_z(V_X(z),\delta z)=0
}
\tag{8.1}
\]

for every \(X\) and every \(\delta z\).

Therefore local-Lorentz vertical directions are genuine Hessian nulls at every
critical point, not only at the flat background.

This is the nonlinear parent of the six local-Lorentz null directions per
nonzero momentum seen in the accepted flat \(L=2\) Hessian calculation.

---

## 9. Nondegenerate solder sector

Define

\[
\mathcal C_{\rm nd}
=
\left\{
(A,e):
\det\Theta_x\ne0\ \text{for every }x
\right\}.
\tag{9.1}
\]

This is an open gauge-invariant sector.

### 9.1 Freeness

Suppose \(g\in\mathcal G_L\) stabilizes \((A,e)\in\mathcal C_{\rm nd}\).

From the solder alone,

\[
\Theta_xg_x^{-1}=\Theta_x.
\]

Since \(\Theta_x\) is invertible,

\[
g_x^{-1}=I
\]

for every site.

Hence

\[
\boxed{
\operatorname{Stab}_{\mathcal G_L}(A,e)=\{1\}
\quad
\text{on }\mathcal C_{\rm nd}.
}
\tag{9.2}
\]

No link-genericity hypothesis is needed.

### 9.2 Properness

At one site, \(SO^+(1,3)\) is a closed Lie subgroup of \(GL(4,\mathbb R)\), and
its right action on \(GL(4,\mathbb R)\) is proper.

The solder sector is a finite product of these right actions.

Adding the link variables with the diagonal gauge action preserves properness,
because the solder factor already supplies a proper action.

Therefore the action on \(\mathcal C_{\rm nd}\) is free and proper.

Consequently

\[
\boxed{
\mathcal C_{\rm nd}/\mathcal G_L
}
\tag{9.3}
\]

is a genuine smooth quotient and

\[
\mathcal C_{\rm nd}\to
\mathcal C_{\rm nd}/\mathcal G_L
\]

is a principal \(\mathcal G_L\)-bundle.

This statement is intentionally restricted to nondegenerate solder.

---

## 10. Explicit quotient invariants

On \(\mathcal C_{\rm nd}\), define the site Gram matrix

\[
\boxed{
Q_x
=
\Theta_x\eta\Theta_x^T.
}
\tag{10.1}
\]

Under \(\Theta'_x=\Theta_xg_x^{-1}\),

\[
Q'_x
=
\Theta_xg_x^{-1}\eta g_x^{-T}\Theta_x^T
=
Q_x.
\]

Thus

\[
\boxed{Q'_x=Q_x.}
\tag{10.2}
\]

For an edge \(y=x+r\), define the solder-dressed link

\[
\boxed{
K_{x,r}
=
\Theta_xL_{x,r}\Theta_y^{-1}.
}
\tag{10.3}
\]

Then

\[
\begin{aligned}
K'_{x,r}
&=
(\Theta_xg_x^{-1})
(g_xL_{x,r}g_y^{-1})
(\Theta_yg_y^{-1})^{-1}
\\
&=
\Theta_xL_{x,r}\Theta_y^{-1}.
\end{aligned}
\]

Hence

\[
\boxed{
K'_{x,r}=K_{x,r}.
}
\tag{10.4}
\]

These are exact finite nonlinear gauge invariants.

---

## 11. Completeness of the quotient coordinates

Suppose two nondegenerate configurations
\((\Theta,L)\) and \((\widetilde\Theta,\widetilde L)\) satisfy

\[
Q_x=\widetilde Q_x
\]

at every site.

Set

\[
A_x
=
\Theta_x^{-1}\widetilde\Theta_x.
\]

Equality of the Grams gives

\[
A_x\eta A_x^T=\eta.
\]

Thus \(A_x\in O(1,3)\).

On a fixed orientation/time-orientation component, require the corresponding
discrete labels to agree.  Then

\[
A_x\in SO^+(1,3).
\]

Define

\[
g_x=A_x^{-1}.
\]

Then

\[
\widetilde\Theta_x=\Theta_xg_x^{-1}.
\]

If in addition

\[
K_{x,r}=\widetilde K_{x,r}
\]

for every edge, cancellation of the invertible solder matrices gives

\[
\widetilde L_{x,r}
=
g_xL_{x,r}g_{x+r}^{-1}.
\]

Therefore:

> on each fixed proper/time-oriented component of the nondegenerate sector,
> the collection \((Q_x,K_{x,r})\) is a complete set of local-Lorentz orbit
> coordinates.

The only extra data relative to the full \(O(1,3)\) quotient are the discrete
component labels selecting the \(SO^+(1,3)\) orbit.

This is stronger than merely asserting existence of an abstract quotient.

---

## 12. Degenerate solder and quotient strata

The preceding freeness fails once solder degenerates.

Take

\[
\Theta_x=0
\quad\text{for every }x,
\]

and

\[
L_{x,r}=I
\quad\text{for every edge}.
\]

For every constant Lorentz frame \(g_x=g\),

\[
\Theta_xg^{-1}=0,
\]

and

\[
gIg^{-1}=I.
\]

Therefore the stabilizer contains the full constant proper-Lorentz group:

\[
\boxed{
SO^+(1,3)
\subseteq
\operatorname{Stab}(\Theta=0,L=I).
}
\tag{12.1}
\]

So the full configuration quotient is not one free principal orbit space.

The correct global language is:

\[
\boxed{
\text{principal nondegenerate sector}
\quad+\quad
\text{lower-rank stabilizer strata}.
}
\tag{12.2}
\]

No single global quotient-manifold dimension is claimed across all solder
ranks.

---

## 13. Descent of the action

Because of exact gauge invariance, on the principal sector there exists a
unique descended action

\[
\overline S_\star:
\mathcal C_{\rm nd}/\mathcal G_L
\to\mathbb R
\]

such that

\[
\boxed{
S_\star
=
\overline S_\star\circ\pi.
}
\tag{13.1}
\]

The Euler covector \(E=dS_\star\) is horizontal by (7.3) and equivariant by
(6.3), hence it is the pullback of the quotient Euler covector

\[
\overline E=d\overline S_\star.
\]

At critical points, the Hessian descends to the quotient tangent space after
removing the vertical gauge directions.

Thus the quotient is not merely a relation on solutions: the action itself is
already defined downstairs.

---

## 14. Exact nonlinear nontriviality on the quotient

The remaining danger is that the descended action could be constant, making the
Euler/operator family disappear after quotienting.

It does not.

Use the exact curved \(L=2\) link configuration with flat solder for which

\[
S_\star=-\frac23.
\tag{14.1}
\]

Scale every raw solder matrix by a common scalar \(\lambda\):

\[
\Theta_x(\lambda)
=
\lambda\Theta_x.
\]

The complementary solder bivector is quadratic in \(\Theta\), while the
curvature is fixed, so exactly

\[
\boxed{
S_\star[\lambda\Theta,L]
=
\lambda^2S_\star[\Theta,L].
}
\tag{14.2}
\]

The exact certificate verifies

\[
S_\star(\lambda)
=
-\frac23\lambda^2.
\]

Therefore

\[
\boxed{
\left.\frac{dS_\star}{d\lambda}\right|_{\lambda=1}
=
-\frac43
\ne0.
}
\tag{14.3}
\]

This direction is not Lorentz vertical.

Indeed proper-Lorentz right multiplication preserves

\[
\det\Theta_x,
\]

whereas

\[
\det(\lambda\Theta_x)=\lambda^4\det\Theta_x.
\]

For the exact control,

\[
\det\Theta=-1,
\qquad
\det(2\Theta)=-16.
\]

Equivalently, the quotient Gram changes by

\[
Q_x\mapsto\lambda^2Q_x.
\]

Hence the action is genuinely nonconstant on the quotient.

---

## 15. Dimension of the descended family

Upstream work has already selected the one-dimensional action family

\[
S_c=cS_\star,
\]

so

\[
d_A=1.
\]

Its Euler family is

\[
E_c=cE_\star,
\]

and accepted variation pressure establishes

\[
d_E=1.
\]

Local-Lorentz descent is linear:

\[
\overline E_c=c\,\overline E_\star.
\]

Section 14 proves

\[
\overline E_\star\ne0.
\]

Therefore

\[
\boxed{
d_{P,\mathrm{Lor},\mathrm{nd}}=1.
}
\tag{15.1}
\]

This is a **nonlinear finite** result on the nondegenerate local-Lorentz
quotient.

It is stronger than the previous flat Hessian statement and narrower than any
claim involving affine translations.

---

## 16. Relation to the flat \(L=2\) pressure test

The accepted flat result found six local-Lorentz vertical directions plus four
forward-coframe null directions at each nonzero momentum.

This PR explains exactly the first six nonlinearly:

\[
\text{local-Lorentz Hessian nulls}
\Longleftarrow
\text{exact finite local-Lorentz symmetry}.
\]

The four forward-coframe directions have a different status.

They are not used in this quotient.

Nothing in this PR upgrades them to a nonlinear gauge symmetry.

Thus the two classes of flat null direction are now cleanly separated:

- Lorentz nulls are true nonlinear gauge verticals;
- forward-coframe nulls remain a separate affine/constraint question.

---

## 17. Theorem-ready statements

1. **Raw solder vector covariance.**  
   If
   \[
   \Theta'_x=\Theta_xg_x^{-1},
   \]
   then
   \[
   v'_r(x)=g_xv_r(x).
   \]

2. **Based plaquette covariance.**  
   \[
   P'_S(x)=g_xP_S(x)g_x^{-1}.
   \]

3. **Finite curvature covariance.**  
   \[
   \mathcal R(P'_S)
   =
   g_x\mathcal R(P_S)g_x^{-1}.
   \]

4. **Curvature bivector covariance.**  
   \[
   C'_S=\rho_2(g_x)C_S.
   \]

5. **Complementary solder covariance.**  
   \[
   B'_{S^c}=\rho_2(g_x)B_{S^c}.
   \]

6. **Proper-Lorentz star commutation.**  
   \[
   \star\rho_2(g)=\rho_2(g)\star.
   \]

7. **Degree-two metric invariance.**  
   \[
   \rho_2(g)^TG_2\rho_2(g)=G_2.
   \]

8. **Cellwise density invariance.**  
   \[
   \mathcal L'_\star(S,x)=\mathcal L_\star(S,x).
   \]

9. **Full action invariance.**  
   \[
   S_\star[g\cdot z]=S_\star[z].
   \]

10. **Euler equivariance.**  
    \[
    E_{gz}\circ Dg_z=E_z.
    \]

11. **Critical-orbit invariance.**  
    \(E_z=0\Rightarrow E_{gz}=0\).

12. **Infinitesimal Noether identity.**  
    \[
    E_z[V_X(z)]=0.
    \]

13. **Critical Hessian vertical nullity.**  
    At \(E_z=0\),
    \[
    H_z(V_X,\delta z)=0.
    \]

14. **Nondegenerate freeness.**  
    If every \(\Theta_x\) is invertible, the local-Lorentz stabilizer is
    trivial.

15. **Nondegenerate proper quotient.**  
    The proper local-Lorentz action on the all-site nondegenerate solder sector
    is free and proper.

16. **Site Gram invariant.**  
    \[
    Q_x=\Theta_x\eta\Theta_x^T
    \]
    is gauge invariant.

17. **Dressed-link invariant.**  
    \[
    K_{x,r}=\Theta_xL_{x,r}\Theta_{x+r}^{-1}
    \]
    is gauge invariant.

18. **Orbit completeness.**  
    On each fixed \(SO^+\) component, equality of all \(Q_x,K_{x,r}\) implies
    gauge equivalence.

19. **Degenerate stabilizer witness.**  
    \(\Theta=0,L=I\) has a nontrivial constant proper-Lorentz stabilizer.

20. **Exact quotient nontriviality.**  
    On the curved witness,
    \[
    S_\star(\lambda\Theta)=-\frac23\lambda^2,
    \]
    so the descended Euler covector is nonzero.

21. **Lorentz physical-family dimension.**  
    \[
    d_{P,\mathrm{Lor},\mathrm{nd}}=1.
    \]

---

## 18. Hostile controls

| Control | Result |
|---|---|
| genuinely site-dependent gauge | 14 distinct \(g_x\) over 16 sites |
| local Lorentz condition | exact at every site |
| proper determinant | \(\det g_x=1\) at every site |
| degree-two pairing | exact invariant |
| star commutation | exact at every site |
| 96 individual cell densities | all exactly invariant |
| total action | exactly invariant |
| quotient site Grams | exactly invariant |
| quotient dressed links | exactly invariant |
| nondegenerate stabilizer | trivial |
| degenerate stabilizer | explicit nontrivial constant boost |
| quotient action collapse | rejected by exact scaling derivative \(-4/3\) |
| affine translation quotient | not used |
| torsion-free / Einstein / time / wave | not used |

---

## 19. Terminal disposition

The Lorentz branch of the previous strategic fork is now closed positively.

The selected finite star density has a genuine nonlinear local proper-Lorentz
gauge symmetry, a clean nondegenerate principal quotient, explicit quotient
coordinates, and a nonzero descended Euler/operator family.

Therefore:

\[
\boxed{
d_A=1
\longrightarrow
d_E=1
\longrightarrow
d_{P,\mathrm{Lor},\mathrm{nd}}=1.
}
\]

The remaining unresolved gauge question is **not Lorentz**.

It is exactly whether the flat forward-coframe / affine-translation null
directions can be promoted by:

- an independently selected translation-invariant completion of the action; or
- an exact on-shell constraint symmetry.

Until such a mechanism is derived, the nonlinear physical quotient should be
taken as local-Lorentz only.
