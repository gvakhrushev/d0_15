# A4D equivariant joint-background dressing: strict-conjugation obstruction and cocycle pressure

**Canonical task:** `EXP-A4D-EQUIVARIANT-JOINT-BACKGROUND-DRESSING-GROUPOID`
**Start baseline:** `4527bd8` (`Open equivariant mixed-background research seam`)
**Research PR:** #136
**Terminal after cocycle pressure:** `EQUIVARIANT-JOINT-BACKGROUND-DRESSING-OBSTRUCTED`  
**Scope:** exact one-cocycle/torsor correction on the frozen graded CAR/group-algebra carrier.  
**Important repair:** the old strict-conjugation proof was insufficient; the terminal now comes from a noncommuting-generator bracket obstruction that allows arbitrary skew correction.
**Checker:** `02_REGISTRY/research/certificates/a4d_equivariant_joint_dressing_check.py`

## 0. Verdict

No dressing of a joint background \((A,e)\) or \((A,e,\Xi)\) can satisfy all
three of the following at once:

1. flat identity, \(\mathfrak F(\mathrm{flat})=I\);
2. raw-solder frame covariance implemented by conjugation;
3. \(DW_0[e]=H(e)\) on every raw coframe direction.

The obstruction is already visible on the frame orbit of the flat solder, and
neither \(A\) nor \(\Xi\) is an argument of it.

Minimal missing datum:

\[
\boxed{
\sigma(\Lambda)
=
\mathfrak F(T_\Lambda\cdot\mathrm{flat}),
\qquad
\sigma(I)=I,
\qquad
D(W\circ\sigma)_I[K]=H(\eta K),
}
\]

a section of the dressing along the owned full-solder frame orbit whose
constitutive derivative matches \(H\). Conjugation of the identity forces
\(\sigma\equiv I\), and that section has derivative \(0\), not \(H(\eta K)\).

## 1. Owned action

The full raw-solder frame action (`rawFullSolderFrameAction`) holds \(\eta\)
fixed:

\[
T_\Lambda(e)=(\eta+e)\Lambda-\eta.
\]

The rational A/B boost of PR #130,

\[
\Lambda=\begin{pmatrix}5/3&4/3&0&0\\4/3&5/3&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix},
\qquad
\Lambda^T\eta\Lambda=\eta,
\]

sends the flat perturbation to

\[
T_\Lambda(0)=\eta\Lambda-\eta
=
\begin{pmatrix}2/3&4/3&0&0\\-4/3&-2/3&0&0\\0&0&0&0\\0&0&0&0\end{pmatrix}
\neq 0.
\]

A nonzero constant coframe has Role period \(L\) times itself, so it is not
in \(\operatorname{im}d_f\). This is the PR #130 fact (51.5). The present
memo does not reprove it; it uses the orbit as the place where dressing
covariance and \(H\) collide.

The infinitesimal generator of that orbit is a boost \(K\) with
\(K^T\eta+\eta K=0\) and direction

\[
v=\eta K
=
\begin{pmatrix}0&1&0&0\\-1&0&0&0\\0&0&0&0\\0&0&0&0\end{pmatrix}.
\]

\(v\) is a nonzero constant, hence not exact on a periodic archive.

The perturbation-only action \(e\mapsto e\Lambda\) fixes \(0\). The no-go does
not apply to that weaker action. The brief asks for the owned full action.

## 2. Conjugation kills the derivative

Assume a representation \(\rho\) of frames on the operator carrier and

\[
\mathfrak F(T_\Lambda(A,e,\Xi))
=
\rho(\Lambda)\,\mathfrak F(A,e,\Xi)\,\rho(\Lambda)^{-1}.
\]

At the flat point \(\mathfrak F=I\), so

\[
\mathfrak F(T_\Lambda\cdot\mathrm{flat})
=
\rho(\Lambda)I\rho(\Lambda)^{-1}
=
I
\]

for every \(\Lambda\). Differentiating in the boost direction gives

\[
G(v)=0,
\qquad
DW_0[v]=-(G(v)+G(v)^T)=0.
\]

## 3. \(H(v)\neq 0\)

On this direction the only nonzero coframe entries are \(e_A{}^B=1\) and
\(e_B{}^A=-1\). The diagonal average in the owned formula (crossed-lift memo
(4.1)) sees only \(e_r{}^r\) and vanishes. The remainder is

\[
K(v)=U_AB_BE_{AB}-U_BB_AE_{BA},
\qquad
H(v)=-K(v)-K(v)^T.
\]

On the rational representation with two \(\mathbb Z/3\) cycles and a 2-level
Role block (dimension 18), this operator is not zero. The checker computes
it. Therefore

\[
DW_0[v]=0\neq H(v).
\]

## 4. Why \((A,\Xi)\) do not repair it

`rawFullSolderFrameAction` takes the coframe and the frame. It does not take
an affine connection or a resolution memory. \(H\) is a function of the
coframe alone. The identity being conjugated is the identity operator, for
any spectator labels \((A,\Xi)\) attached to the flat point.

So the same contradiction holds for every proposed source category in the
brief:

- \((A,e)\in\mathfrak A_{\rm stable}\);
- \((A,e,\Xi)\) with \(\Xi=((\Pi_y)_y,Q_o)\).

Changing how \(A\) or \(\Xi\) transforms under \(\Lambda\) does not change
\(T_\Lambda(0)\) or \(H(v)\). A row pull \(R\) of the kind in
`transportedSolderCenter_covariance` makes a solder *center* covariant. It
is not an argument of \(H\) and it does not change the identity operator.

## 5. What remains constructible, and what does not

On the exact pure-gauge chart the owned torsor law \(F_{\phi+c}=F_\phi R_c\)
still holds, and the horizontal letters and \(W^{\rm gr}\) still descend to
the coframe. That package is not a dressing of arbitrary \((A,e)\), and it
does not see the frame orbit of the flat solder.

Bare representatives off that chart still exist after a retraction, a
potential section and a skew assignment, by PR #134. None of those choices
is conjugation-equivariant under the full solder action, by PR #130 §52 and
by §2–§3 here.

## 6. Routes

| Route | Where it fails |
|---|---|
| Torsor-valued dressing with conjugation covariance | §2 forces \(\sigma=I\), §3 contradicts \(H\) |
| Action groupoid of potential sections | potential shifts preserve \(\operatorname{im}d_f\); the frame orbit leaves it |
| Resolved background \((A,e,\Xi)\) | \(\Xi\) is a spectator of \(T_\Lambda\) and of \(H\) |
| Path-ordered exponential | at flat identity the generator along \(v\) is \(0\), so every ordering stays \(I\) |
| Crossed product with background transport | a row pull repairs centers, not \(DW_0[v]\) |

## 7. Hostile controls

| Control | Result |
|---|---|
| Flat | \(F=I\), and conjugation keeps \(F=I\) on the whole frame orbit |
| Exact translation gauge | stays inside \(\operatorname{im}d_f\); the frame orbit of flat does not |
| L=3 rank / period | constant \(v\) has period \(3v\neq 0\), so it is not exact |
| L=2 | not used as a witness: \(U\neq U^{-1}\) is needed for the operator representation; the finite rational boost itself is \(L\)-independent |
| Nyquist / corner / harmonic | not deleted; the witness direction is a constant off-diagonal shear, which is one of the harmonic/raw modes the controls require to be kept |
| #130 rank jump | not the obstruction here; the obstruction is earlier, at the flat orbit |
| Labelled holonomy | does not enter \(H(v)\) |

## 8. Not claimed

No Hessian, stress, Einstein equation, continuum limit, physical time, or
golden refinement. This memo does not select a dressing and does not compute
the crossed \(T_\kappa\) action; that is a separate task.

## 9. Checker

`python3 02_REGISTRY/research/certificates/a4d_equivariant_joint_dressing_check.py`

Records the rational boost, the period obstruction, the negative control for
the perturbation-only action, and \(H(v)\neq 0\) on the 18-dimensional
representation.


---

## 10. Pressure correction: strict conjugation is only the zero-cocycle sector

The original argument assumed
\[
\mathfrak F(T_\Lambda x)
=
\rho(\Lambda)\mathfrak F(x)\rho(\Lambda)^{-1}.
\]
That is one special equivariance law. It corresponds to a vanishing torsor
correction.

Because the owned full-solder frame transformation is a **right** action,
\[
T_M(T_\Lambda x)=T_{\Lambda M}x,
\]
the clean right-action convention is
\[
\boxed{
\mathfrak F(x\cdot\Lambda)
=
\alpha_\Lambda(\mathfrak F(x))\,\sigma(\Lambda),
\qquad
\alpha_\Lambda(F)=\rho(\Lambda)^{-1}F\rho(\Lambda).
}
\tag{10.1}
\]

The automorphisms obey
\[
\alpha_M\circ\alpha_\Lambda
=
\alpha_{\Lambda M}.
\tag{10.2}
\]

Exact composition of (10.1) is equivalent to the nonabelian right-cocycle law
\[
\boxed{
\sigma(\Lambda M)
=
\alpha_M(\sigma(\Lambda))\,\sigma(M).
}
\tag{10.3}
\]

The identity and inverse laws are forced:
\[
\boxed{
\sigma(I)=I,
}
\tag{10.4}
\]
\[
\boxed{
\sigma(\Lambda^{-1})
=
\alpha_{\Lambda^{-1}}(\sigma(\Lambda))^{-1}.
}
\tag{10.5}
\]

At the flat point,
\[
\mathfrak F(x_0)=I,
\]
equation (10.1) gives
\[
\boxed{
\mathfrak F(x_0\cdot\Lambda)=\sigma(\Lambda).
}
\tag{10.6}
\]

Therefore the strict-conjugation argument of §§2–3 is exactly the special
case
\[
\sigma\equiv I.
\]
It does not test the full torsor/groupoid problem.

---

## 11. Every correction cocycle is a relative representation

The cocycle law admits an exact classification.

Define
\[
\boxed{
\tau(\Lambda)=\rho(\Lambda)\sigma(\Lambda).
}
\tag{11.1}
\]

Using (10.3),
\[
\begin{aligned}
\tau(\Lambda M)
&=
\rho(\Lambda M)
\rho(M)^{-1}\sigma(\Lambda)\rho(M)\sigma(M)
\\
&=
\rho(\Lambda)\sigma(\Lambda)\rho(M)\sigma(M)
\\
&=
\tau(\Lambda)\tau(M).
\end{aligned}
\]

Hence
\[
\boxed{
\sigma\text{ obeys (10.3)}
\iff
\tau=\rho\sigma\text{ is an ordinary representation.}
}
\tag{11.2}
\]

Conversely, for any representation \(\tau\) on the same carrier,
\[
\boxed{
\sigma(\Lambda)=\rho(\Lambda)^{-1}\tau(\Lambda)
}
\tag{11.3}
\]
obeys identity, composition and inverse exactly.

The corrected covariance can therefore be written
\[
\boxed{
\mathfrak F(x\cdot\Lambda)
=
\rho(\Lambda)^{-1}\mathfrak F(x)\tau(\Lambda).
}
\tag{11.4}
\]

This is the exact algebraic type of the missing frame torsor datum.

A terminal obstruction to equivariant joint dressing must therefore rule out
**every** admissible second representation \(\tau\) satisfying the remaining
tangent and pure-gauge constraints. The old proof ruled out only
\(\tau=\rho\).

---

## 12. First-jet condition becomes a representation-extension equation

Let
\[
r(K)=D\rho_I[K],
\qquad
t(K)=D\tau_I[K],
\]
and define
\[
\boxed{
S(K)=t(K)-r(K)=D\sigma_I[K].
}
\tag{12.1}
\]

Since
\[
W(\sigma)=\sigma^{-T}\sigma^{-1},
\]
one has
\[
D(W\circ\sigma)_I[K]
=
-\bigl(S(K)^T+S(K)\bigr).
\]

The required frame-orbit first jet is therefore exactly
\[
\boxed{
S(K)+S(K)^T
=
-H(\eta K).
}
\tag{12.2}
\]

This fixes only the symmetric part of \(S(K)\).

But \(t=r+S\) must also be a Lie-algebra representation:
\[
\boxed{
t([K,L])=[t(K),t(L)].
}
\tag{12.3}
\]

Substituting \(t=r+S\) gives
\[
\boxed{
S([K,L])
=
[r(K),S(L)]
+
[S(K),r(L)]
+
[S(K),S(L)].
}
\tag{12.4}
\]

Equations (12.2) and (12.4), for the six Lorentz generators, are the first
honest terminal test.

The skew parts
\[
A(K)=\tfrac12(S(K)-S(K)^T)
\]
are not free independently: they must solve the coupled quadratic bracket
system (12.4).

Thus the pressure problem is:

> Does the prescribed symmetric six-generator map
> \[
> K\mapsto-\tfrac12H(\eta K)
> \]
> extend, after adding skew parts, to the difference of two exact Lorentz
> representations on the owned operator carrier?

---

## 13. The original A/B boost cannot be a terminal obstruction

Restrict to any one-parameter subgroup
\[
\Lambda(t)=\exp(tK).
\]

A representation of this subgroup is determined by one arbitrary matrix
generator. Therefore choose
\[
\boxed{
S_K=-\tfrac12H(\eta K)+A_K,
\qquad
A_K^T=-A_K,
}
\tag{13.1}
\]
and set
\[
t_K=r(K)+S_K.
\]

Then
\[
\rho_K(t)=e^{t\,r(K)},
\qquad
\tau_K(t)=e^{t\,t_K}
\]
are exact representations of the additive one-parameter group, and
\[
\boxed{
\sigma_K(t)
=
\rho_K(t)^{-1}\tau_K(t)
}
\tag{13.2}
\]
is an exact cocycle by §11.

Its derivative is
\[
D\sigma_K(0)=S_K,
\]
hence
\[
\boxed{
D(W\circ\sigma_K)_0
=
H(\eta K).
}
\tag{13.3}
\]

No commutativity assumption between \(r(K)\) and \(S_K\) is needed.

Therefore the exact rational A/B boost direction used by the original memo
cannot terminally obstruct cocycle-corrected equivariance. It proves only
that the zero cocycle is impossible.

Any genuine no-go must involve at least two noncommuting Lorentz generators
and fail (12.4).

---

## 14. Pure-gauge compatibility is a quotient condition

On the exact chart the dressing representative is a right torsor:
\[
F_{\phi+c}=F_\phi R_c.
\]

Suppose a frame arrow carries one exact background to another exact
background. Corrected frame covariance need not identify one chosen
representative literally. The correct requirement is existence of an allowed
constant-potential isotropy element \(R_c\) such that
\[
\boxed{
\rho(\Lambda)^{-1}F_\phi\tau(\Lambda)
=
F_{\phi'}R_c.
}
\tag{14.1}
\]

For composable frame arrows the corresponding \(R_c\)'s must obey the induced
torsor cocycle obtained from (10.3).

For the flat full-solder orbit used in the original no-go, every nontrivial
constant Lorentz direction is a nonzero constant coframe and therefore lies
outside \(\operatorname{im}d_f\) on the periodic archive. Consequently
pure-gauge specialization does **not** force \(\sigma(\Lambda)=I\) there.

This is exactly why the old flat-orbit argument was too strong.

---

## 15. Resolution memory remains a spectator of the cocycle integrability

The correction above repairs the frame law at the dressing level. It does not
change the #135 classification of
\[
\Xi_{\rm str}=((W_y)_y,\mathcal K).
\]

If the resolved background is included in the source category, the frame
arrow acts on \(\Xi_{\rm str}\) by the already-classified functorial action.
The new equation (12.4) still lives entirely in the dressing/operator carrier.

Thus resolution can be carried consistently through the groupoid, but it does
not solve or obstruct the Lorentz representation-extension equation.

---

## 16. What is now proved and what remains open

The pressure review changes the research status.

### Proved exactly

1. strict conjugation is only the \(\sigma=I\) sector;
2. corrected right-equivariance has exact identity/composition/inverse iff
   (10.3) holds;
3. every such cocycle is exactly a relative representation
   \[
   \sigma=\rho^{-1}\tau;
   \]
4. the constitutive first derivative is exactly (12.2);
5. full Lorentz integrability is exactly the six-generator quadratic system
   (12.4);
6. the old one-boost witness cannot produce a terminal no-go, because every
   one-parameter direction admits the exact cocycle (13.2);
7. pure-gauge compatibility is modulo the constant-potential right isotropy,
   not literal equality of representatives.

### Still open

Whether there exists one full Lorentz representation \(\tau\) on the owned
finite carrier whose difference from \(\rho\) satisfies (12.2) for all six
generators simultaneously.

Equivalently: whether the skew parts \(A(K)\) can solve (12.4).

Until that finite representation-extension problem is solved, neither
\[
\texttt{EQUIVARIANT-JOINT-BACKGROUND-DRESSING-GROUPOID-CONSTRUCTED}
\]
nor
\[
\texttt{EQUIVARIANT-JOINT-BACKGROUND-DRESSING-OBSTRUCTED}
\]
is justified.

The previous terminal claim is therefore withdrawn. PR #136 must remain
Draft under
\[
\boxed{
\texttt{FULL-LORENTZ-COCYCLE-INTEGRABILITY-OPEN}.
}
\]

The remaining problem is now one explicit finite algebraic system:
(12.2) + (12.4), plus the quotient compatibility (14.1).


---

## 17. The graded carrier turns the open integrability problem into a finite block test

The remaining freedom in §16 is not an arbitrary endomorphism of an unrelated
larger space. The frozen dressing problem is graded:

- the owned pure-gauge dressing is degree preserving;
- the transverse skew datum of PR #134 is explicitly typed in the same
  CAR/group-algebra operator carrier;
- \(H(e)\) preserves Fock degree and parity.

Therefore an admissible corrected representation \(\tau\) on the current
target preserves every Fock-degree block.

It is enough to test degree one.

Take the Lorentz subalgebra on Roles \(A,B,C\):
\[
\mathfrak s
=
\operatorname{span}\{B_{AB},B_{AC},R_{BC}\}
\cong\mathfrak{so}(1,2),
\]
with
\[
[B_{AB},B_{AC}]=R_{BC},
\]
\[
[R_{BC},B_{AB}]=-B_{AC},
\qquad
[R_{BC},B_{AC}]=B_{AB}.
\tag{17.1}
\]

Use \(N=1\), hence archive period \(L=3\).

The fourth Role \(D\) is a spectator for this subalgebra. On degree one, the
active \(A,B,C\) component is
\[
\boxed{
\mathcal V
=
\operatorname{Fun}((\mathbb Z/3)^3,\mathbb R^3).
}
\tag{17.2}
\]

A solution on the full four-Role archive would restrict to this active block:

1. the prescribed symmetric operators for (17.1) are block diagonal between
   \(\operatorname{span}(A,B,C)\) and the \(D\) one-particle direction;
2. the active-active block of a commutator with such an operator depends only
   on the active-active block of the unknown skew operator;
3. the unused \(D\)-archive coordinate can be averaged out.

So failure on (17.2) is a failure of the full frozen graded carrier, not a
failure caused by throwing away a possible compensating \(D\) component.

---

## 18. Symmetric bracket equation: quadratic integrability has a linear necessary part

For every Lorentz generator \(X\), write
\[
t(X)=A_X+B_X,
\qquad
A_X^T=-A_X,
\qquad
B_X^T=B_X.
\tag{18.1}
\]

The first-jet condition fixes
\[
\boxed{
B_X
=
\frac12\bigl(r(X)+r(X)^T\bigr)
-\frac12H(\eta X).
}
\tag{18.2}
\]

Now take the symmetric part of
\[
t([X,Y])=[t(X),t(Y)].
\]

Because
\[
[A_X,A_Y]^T=-[A_X,A_Y],
\qquad
[B_X,B_Y]^T=-[B_X,B_Y],
\]
the quadratic same-parity commutators disappear from the symmetric part.
Every admissible \(\tau\) must satisfy the linear system
\[
\boxed{
B_{[X,Y]}
=
[A_X,B_Y]+[B_X,A_Y].
}
\tag{18.3}
\]

This condition already allows the entire unknown skew modulus.
No polar choice, no zero-skew assumption, and no commutation assumption is
made.

Thus failure of (18.3) is stronger than failure of the original
strict-conjugation ansatz.

---

## 19. Literal L=3 degree-one operators

Let \(U_r\) be the period-three archive shift and
\[
A_r=\frac12(I+U_r^{-1}).
\]

On degree one,
\[
E_{sr}=|s\rangle\langle r|.
\]

For a constant Lorentz tangent \(X\), put
\[
e_X=\eta X.
\]
Every Lorentz generator in (17.1) has zero diagonal, so the scalar-link term
of the owned first jet vanishes.

Define
\[
K_X
=
\sum_{s,r\in\{A,B,C\}}
(e_X)_{sr}\,U_sA_rE_{sr}.
\tag{19.1}
\]

The literal first-jet owner therefore gives
\[
\boxed{
H_X
=
-\bigl(K_X+K_X^T\bigr).
}
\tag{19.2}
\]

The exterior frame derivative on degree one is
\[
r(X)=I_{\rm archive}\otimes X.
\tag{19.3}
\]

Equations (18.2), (19.1) and (19.2) determine the three symmetric matrices
\(B_{AB},B_{AC},B_{BC}^{\rm rot}\) exactly over \(\mathbb Q\).

No continuum or Fourier approximation is used.

---

## 20. Translation averaging removes no solutions

All three \(B_X\) commute with the archive translation group
\[
G=(\mathbb Z/3)^3.
\]

Suppose arbitrary skew matrices \(A_X\) solved (18.3). Average them:
\[
\boxed{
\bar A_X
=
\frac1{|G|}
\sum_{g\in G}T_gA_XT_g^{-1}.
}
\tag{20.1}
\]

Every \(T_g\) is orthogonal, so
\[
\bar A_X^T=-\bar A_X.
\]

Since the coefficients and right-hand sides of (18.3) commute with every
\(T_g\), the averaged \(\bar A_X\) solve the same system.

Therefore it is lossless to restrict to translation-invariant skew operators.

A translation-invariant operator on (17.2) has one \(3\times3\) matrix
coefficient for each of the 27 displacements.

Skewness leaves exactly

- \(3\) parameters at zero displacement;
- for the \(13\) nonzero inverse-pairs \(\{d,-d\}\), \(9\) free matrix
  coefficients per pair.

Hence each \(A_X\) has
\[
3+13\cdot9=120
\]
free rational parameters.

For the three generators there are
\[
\boxed{360}
\]
unknowns.

The three bracket equations (17.1) give
\[
3\cdot27\cdot9
=
\boxed{729}
\]
exact rational scalar equations.

---

## 21. Exact left-null certificate: the linear system is inconsistent

The checker constructs the \(729\times360\) rational matrix
\[
M_{\rm br}
\]
of (18.3) and its right-hand side
\[
y_{\rm br}.
\]

It then uses one explicit integer covector
\[
\ell\in\mathbb Z^{729}
\]
with 96 nonzero entries, all in
\[
\{-5,-4,-3,-1,1,3,4,5\}.
\]

The complete support table is embedded literally in the checker.

Exact Fraction arithmetic verifies
\[
\boxed{
\ell^TM_{\rm br}=0
}
\tag{21.1}
\]
for all 360 skew columns, while
\[
\boxed{
\ell^Ty_{\rm br}=2.
}
\tag{21.2}
\]

Therefore
\[
\boxed{
M_{\rm br}a=y_{\rm br}
\quad\text{has no solution over }\mathbb R.
}
\tag{21.3}
\]

This is an exact inconsistency certificate; it does not depend on
floating-point rank or a numerical minimizer.

The certificate is already on the symmetric projection of the Lie bracket.
The remaining nonlinear skew bracket equations are never reached.

---

## 22. Lift of the obstruction to the full frozen carrier

Assume, for contradiction, that the cocycle-corrected frame law of §10 exists
on the frozen graded carrier.

Then by §11 it determines a Lorentz representation
\[
\tau
\]
on that carrier.

Degree preservation restricts \(d\tau\) to the degree-one block.

Restrict the Lorentz algebra to \(\mathfrak s\) from §17. Project the
degree-one block to its \(A,B,C\) component and average over the spectator
\(D\)-archive coordinate and the active archive translations.

The resulting skew parts satisfy exactly the 360-variable system of §§18–20.

But §21 proves that system inconsistent.

Contradiction.

Therefore no exact cocycle
\[
\sigma(\Lambda)
\]
with the required first derivative can exist in the current graded
CAR/group-algebra dressing carrier.

This closes the gap left by the old one-boost argument.

---

## 23. Why the one-parameter positive control is still correct

Section 13 is retained.

For each single generator \(X\), one can choose
\[
S_X=-\tfrac12H(\eta X)+A_X
\]
and integrate an exact one-parameter relative representation.

The obstruction appears only when two noncommuting boosts and their rotation
must be glued simultaneously.

Thus the final result is not
“\(H(\eta X)\neq0\), therefore impossible.”

It is
\[
\boxed{
\text{every individual Lorentz line integrates, but the }so(1,2)
\text{ bracket cannot be satisfied.}
}
\tag{23.1}
\]

This is exactly the pressure distinction requested after the first review.

---

## 24. Pure-gauge isotropy and resolution do not evade the certificate

The right constant-potential isotropy changes a chosen dressing representative
by an orthogonal factor. Infinitesimally this contributes only to the unknown
skew pieces \(A_X\).

Equation (21.1) annihilates all 360 skew directions. Therefore the certificate
already includes every such infinitesimal isotropy correction.

Likewise the #135 resolution datum
\[
\Xi_{\rm str}=((W_y)_y,\mathcal K)
\]
does not enter \(H(\eta X)\) or the constant-frame bracket. Transporting
\(\Xi_{\rm str}\) functorially cannot change (21.2).

So neither pure-gauge torsor freedom nor rank/holonomy resolution repairs the
frame cocycle.

---

## 25. Exact terminal and minimal escape datum

The strengthened terminal is now justified:
\[
\boxed{
\texttt{EQUIVARIANT-JOINT-BACKGROUND-DRESSING-OBSTRUCTED}.
}
\]

Its scope is exact:

> No exact \(\sigma(\Lambda)\) one-cocycle/torsor correction in the frozen
> degree-preserving CAR/group-algebra dressing carrier can simultaneously
> satisfy the owned full raw-solder frame action, exact Lorentz composition,
> and
> \[
> D(W\circ\sigma)_I[X]=H(\eta X).
> \]

The earliest exact obstruction is the degree-one \(L=3\)
\(\mathfrak{so}(1,2)\) symmetric bracket system, not the old single boost.

To evade the theorem one must add at least one datum outside the current task:

1. enlarge the matter/dressing carrier to allow degree mixing, and supply
   the corresponding enlarged horizontal algebra and raw-control semantics; or
2. replace the exact one-cocycle by a genuinely higher isotropy-valued
   2-cocycle / nontrivial group extension, with its own exact source/target and
   composition law; or
3. change the owned constitutive first jet or the owned full-solder frame
   action.

None of these is present in the landed stack.

A different transverse skew assignment, path order, potential section, or
resolution representative is not enough: all such degree-preserving skew
freedom was already quantified in (18.3).

This is therefore a terminal obstruction for the canonical task as typed,
while clearly naming the extra structure required to reopen a larger theory.


---

## 26. Ready lifecycle audit

The cocycle pressure requested after the first review is closed.

Final research surface:

- strict conjugation is retained only as the zero-cocycle negative control;
- exact one-cocycles are classified as relative representations
  \(\sigma=\rho^{-1}\tau\);
- every individual Lorentz one-parameter subgroup has a positive exact
  cocycle control with the prescribed constitutive tangent;
- the full graded problem fails only at the noncommuting-generator stage;
- the exact \(L=3\), degree-one \(\mathfrak{so}(1,2)\) certificate annihilates
  all 360 translation-invariant skew unknowns and evaluates the required
  bracket right-hand side to \(2\);
- pure-gauge isotropy and #135 resolution memory do not evade that
  certificate;
- the minimal escape data are explicitly outside the current canonical task:
  degree-mixing carrier/enlarged horizontal algebra, a genuine higher
  isotropy-valued 2-cocycle/group extension, or a change of the owned
  first-jet/frame law.

The canonical EXPENSIVE task is self-retired on this Ready head.  No Lean
source or claim registration is added by this research PR.

Lifecycle: REVIEW.  Do not self-merge.
