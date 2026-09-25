# A4D finite graded coframe dressing: skew modulus

**Canonical task:** `EXP-A4D-FINITE-GRADED-COFRAME-DRESSING`
**Start baseline:** `31bdb4bac83e5222dc6fa480e5819ae6b3a81e0a`
**Research PR:** #134
**Terminal:** `FINITE-GRADED-COFRAME-DRESSING-MODULI-CLASSIFIED`
**Checker:** `02_REGISTRY/research/certificates/a4d_finite_graded_coframe_dressing_check.py`
**Reconciled landed input:** PR #130 `MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md`
**Lifecycle audit:** task row and canonical brief are retired on this Ready head.

## 0. Verdict

No canonical coframe-only finite dressing \(\mathcal F_e\) is determined by the landed stack.
Bare finite representatives exist after auxiliary finite-dimensional choices, but the full
frame-covariant selection problem is not solved by those representatives. PR #130 now
supplies the complementary obstruction: a coframe-only exact-orbit retraction cannot be
equivariant under the owned full raw-solder frame action.

The owned identity

\[
DW_0[e]=-(G(e)+G(e)^T)=H(e)
\]

fixes the symmetric part of the tangent generator and nothing else. The
carrier of \(H(e)\) is the CAR/group-algebra operator space of the crossed-lift
memo (4.1), not \(\mathfrak{gl}(4)\). A count that puts the modulus in
\(\mathfrak{so}(4)\) is the wrong type and is withdrawn.

On an exact coframe the owned generator is not the symmetric one. In the
scalar \(L=3\) block, with \(\xi=\delta_0\),

\[
G_{\xi}=M_{\xi}D+K(h),\qquad h=D\xi,
\]

and \(M_{\xi}D\) has skew part

\[
\tfrac12(M_{\xi}D-D M_{\xi})
=
\begin{pmatrix}0&3/4&-3/4\\-3/4&0&0\\3/4&0&0\end{pmatrix}
\neq 0.
\]

So \(G=-H/2\), the polar/symmetric choice, fails pure-gauge specialization.
Matching \(\mathcal F_\phi\) forces this skew on \(\operatorname{im}d_f\).

Off that chart it forces nothing. At \(L=3\) the scalar cycle splits as

\[
\operatorname{im}D=\{\text{mean-free functions}\}\ (\dim 2),
\qquad
(\operatorname{im}D)^{\perp}=\{\text{constants}\}\ (\dim 1),
\]

and \(D=0\) at \(L=2\), so the scalar block does not even separate the two
there. A constant transverse mode plus any skew operator \(S\) gives

\[
DW(G_0)=DW(G_0+S)
\]

while both generators agree on \(\operatorname{im}D\). The same holds mode by
mode on the full carrier.

Minimal missing datum, named exactly:

\[
\boxed{
\Sigma_{\rm skew}:\{\text{raw coframe modes}\}/\operatorname{im}d_f
\longrightarrow
\{\text{skew operators on the CAR/group-algebra carrier}\},
}
\]

linear in the coframe, equal to \(\operatorname{skew}(G_{\xi})\) on
\(\operatorname{im}d_f\), and intertwining the owned frame action.
No integer dimension is stated: the carrier dimension depends on \(L\) and on
which CAR block is occupied, and no landed theorem fixes those.

Nothing in PRs #123, #125, #126, #127, #128, #129 supplies \(\Sigma_{\rm skew}\).
Polar decomposition is the point \(\Sigma_{\rm skew}=0\) off the exact chart, not a theorem.

## 0.0 The dressing is not a function of the coframe

This is earlier than the skew modulus, and it is exact.

The owned pure-gauge family obeys

\[
F_{\phi+c}=F_\phi\exp\!\Big(\sum_a c^a D_a\Big)
\]

with the same gradient \(d_f(\phi+c)=d_f\phi\). On the scalar \(L=3\) block
\(D^3=-\tfrac{27}{4}D\), so

\[
\exp(tD)=I+A(t)D+B(t)D^2,
\qquad
A(t)=\sum_{m\ge 0}\frac{(-27/4)^m t^{2m+1}}{(2m+1)!}.
\]

The alternating series at \(t=1\) is bounded away from zero: the partial
sum through \(m=7\) and the tail through the next term give

\[
\big\lvert A(1)\big\rvert\ge \frac{23144717353997}{116275502120960}>0.
\]

Hence \(\exp(D)\neq I\) and \(F_{\phi+c}\neq F_\phi\). No map
\(e\mapsto\mathcal F_e\) can satisfy both \(\mathcal F_{d_f\phi}=F_\phi\)
and dependence on \(e\) alone.

The constitutive shadow does not see this. With \(E=\exp(cD)\) and
\(E^T=E^{-1}\),

\[
W(\phi+c)=(F_\phi E)^{-T}(F_\phi E)^{-1}=F_\phi^{-T}F_\phi^{-1}=W(\phi).
\]

So \(W\) descends to the coframe and \(F\) does not. A finite dressing that
specializes to \(F_\phi\) needs either a section of \(d_f\) (a gauge-fixed
representative) or a torsor/groupoid-valued formulation carrying the constant
isotropy explicitly. PR #130 further proves that no coframe-only retraction onto
the exact-coframe subspace can be equivariant under the owned full raw-solder
frame action. Thus a gauge-fixed representative can witness finite existence,
but it is not the final covariant target.

## 0.1 Single-site exponential is already impossible on the exact chart

The modulus above is the linearized statement. The finite statement is
sharper, and it does not need transverse modes.

A single-site family \(e\mapsto\mathcal F_e\) with \(\mathcal F_0=I\) and
linear tangent \(G\), required to be a homomorphism
\(\mathcal F_{e_1+e_2}=\mathcal F_{e_1}\mathcal F_{e_2}\), must have

\[
[G(u),G(v)]=0
\qquad\text{for all coframe values }u,v.
\]

On the scalar \(L=3\) block the owned shift piece \(M_{\xi}D\) of \(G_{\xi}\)
already fails this on two exact directions \(\xi=\delta_0\) and
\(\xi=\delta_1\):

\[
[M_{\delta_0}D,\,M_{\delta_1}D]
=
\begin{pmatrix}-9/4&0&9/4\\0&9/4&-9/4\\0&0&0\end{pmatrix}
\neq 0.
\]

The same is true of the symmetric parts alone, so the failure is not an
artefact of the skew piece. Therefore no coframe-linear single-site
exponential homomorphism specializes to the owned pure-gauge generator.
The owned \(\mathcal F_\phi\) evades this only because it is normal-ordered in
the potential, \(F^{\rm sc}_\phi(x,y)=[\exp(\sum_a\phi^a(x)D_a)]_{xy}\),
which is not a function of \(h=d_f\phi\) through the exponential of \(G(h)\).

So the residual family, if it exists at all, cannot be a single-site
\(\mathcal F_e\). It has to be potential-ordered on the exact chart and
path-ordered off it. Both orderings are extra data. The transverse skew
assignment of §0 is the linearized shadow of the second one; it is not a
substitute for it.

## 1. Typing firewall

Do not identify:

| Object | Owner | Domain |
|---|---|---|
| \(\ell_{d_f\phi,r}=\mathcal F_\phi U_r\mathcal F_\phi^{-1}\) | pure-gauge bisection | \(e=d_f\phi\) |
| \(W^{\rm gr}_{d_f\phi}=\mathcal F_\phi^{-T}\mathcal F_\phi^{-1}\) | pure-gauge constitutive shadow | \(e=d_f\phi\) |
| \(W_{\rm flux}(e)=I+H(e)\) | constitutive/Riesz section | arbitrary raw \(e\) |
| \(J^{\rm can}, \mathscr R, M, R_r\) | relative A/e span | affine increments |
| \(\kappa\) / diagonal seed | sourced diagonal | labelled overlap |
| \(T_\kappa\) | mismatch transport | after \(\kappa\) is typed |

\(DW_0=H\) does not mean \(D\mathcal F_0=H\).

If \(\mathcal F_{\varepsilon e}=I+\varepsilon G(e)+O(\varepsilon^2)\), then

\[
DW_0[e]=-(G(e)^T+G(e)).
\tag{1.1}
\]

So \(H(e)\) fixes

\[
G(e)+G(e)^T=-H(e)
\tag{1.2}
\]

and does not fix \(G(e)-G(e)^T\).

The owned pure-gauge formula (crossed-lift memo (4.2))

\[
G_\xi=\sum_a M_{\xi^a}D_a+K(h),
\qquad
H(h)=-(G_\xi+G_\xi^T)
\]

is a full generator, but only for \(h=d_f\xi\). Its skew part on exact
directions is already owned. It does not extend by algebra to a transverse
raw coframe.

## 2. What the landed stack actually constrains

| Landed fact | What it sees | What it does not see |
|---|---|---|
| #123/#126 \(J^{\rm can}=\mathcal S\circ\Sigma_{\rm skew}\) on \(U=\operatorname{im}\mathcal B\) | labelled increments \((\Delta b,\Delta v)\) | fibre generator \(G(e)\) |
| #125 sourced diagonal / \(\kappa\) | those increments plus a supplied comparison | \(\mathfrak{so}(4)\) of a coframe dressing |
| #127 active-span extension independence | full-fibre extensions of \(J\) off \(U\) | a reason to use that freedom as \(G\) |
| #128 classical passport | graphification \(M=0\) and endpoint descent \(D_\ell\) | a stable dressing |
| #129 endpoint locality | path-word evaluation depends only on endpoints iff holonomy is trivial | a coframe-linear skew map |

#127 is used only as a firewall: an arbitrary extension of \(J\) off the active
span is not an input to \(\mathcal F_e\). The skew modulus (0.1) is not that
extension freedom. It lives in the fibre of the coframe generator, which the
sourced-diagonal chain never reads.

## 3. Routes

### 3.1 Ordered exponential of a chosen \(G\)

Once \(\Sigma_{\rm skew}\) is chosen, set

\[
G(e)=-\tfrac12 H(e)+\Sigma_{\rm skew}(P_\perp e)+G_{\rm exact}(P_{\rm exact}e)
\]

with \(G_{\rm exact}\) the owned pure-gauge generator on \(\operatorname{im}d_f\),
and integrate by ordered exponential along any chosen coframe path from \(0\).
Flat identity holds. Pure-gauge specialization holds because
\(P_\perp d_f\phi=0\). First derivative is \(H\) because \(\Sigma_{\rm skew}\) is skew.
The path order of noncommuting transverse generators is a second extra datum
inside this route. Neither \(\Sigma_{\rm skew}\) nor the order is owned. The exponential is a representative of the family.

### 3.2 Background-groupoid cocycle

A cocycle \(F(e,e')\) with \(F(0,0)=I\) and \(F(d_f\phi,0)=\mathcal F_\phi\)
has the same tangent ambiguity: the infinitesimal generator along a
transverse direction is still an arbitrary solution of the symmetric constraint. A cocycle law
constrains finite composition after a generator is chosen. It does not choose
the generator.

### 3.3 Polar / metric square root

The symmetric positive square root forces skew zero everywhere. That already
contradicts the owned pure-gauge generator, whose skew part is nonzero at
\(L=3\) (checker: `pure_gauge_skew_nonzero`). Restoring that skew on
\(\operatorname{im}d_f\) and setting it to zero only transversely is exactly
the choice \(\Sigma_{\rm skew}=0\) off the exact chart. Positivity of \(I+H(e)\) for
arbitrary raw \(e\) is not owned.

### 3.4 Path-resolved graded trivialization

Path-ordering distinguishes noncommuting \(G\)'s. The checker records that
\([G_0,S]\neq[G_1,S]\) for two generators with the same symmetric part.
No landed path law is a function of the raw coframe skew.

### 3.5 Crossing with \(T_\kappa\)

Not used to define \(G\). \(T_\kappa\) is typed from the diagonal seed, which
depends on \((\Delta b,\Delta v)\) and \(J^{\rm can}\), not on \(\Sigma_{\rm skew}\).
A mixed bracket \([G(e),N_\kappa]\) can be computed after both are typed.
Different \(\Sigma_{\rm skew}\) produce different brackets (checker: the two commutators
differ). The bracket is a consequence, not a selector.

### 3.6 Bare compatibility versus the covariance obstruction

At the level of bare finite integration there is no inconsistency: the pure-gauge
chart and the transverse symmetric constraint (1.2) are compatible, and explicit
noncanonical representatives exist after choosing a retraction, a potential section,
and a transverse orthogonal/skew law.

The full task, however, also requires frame covariance. PR #130 now supplies the
stronger boundary: under the owned full raw-solder frame action, a coframe-only
exact-orbit retraction cannot be equivariant. Therefore the obstruction is not
"finite integration does not exist"; it is "no canonical frame-equivariant
coframe-only selection follows from the landed data."

This is why the terminal remains `FINITE-GRADED-COFRAME-DRESSING-MODULI-CLASSIFIED`:
the family and its nonselection are classified, while the next admissible target
must be torsor/groupoid-valued or jointly background-typed rather than a silently
canonical \(e\mapsto\mathcal F_e\).

## 4. Hostile controls

| Control | Result |
|---|---|
| Flat background | \(H(0)=0\), \(G(0)=0\) for every \(\Sigma_{\rm skew}\); \(\mathcal F_0=I\) |
| Exact pure shift / translation gauge | \(e=d_f\phi\) lies in \(\operatorname{im}d_f\); \(\Sigma_{\rm skew}\) is invisible; \(\mathcal F\) reduces to \(\mathcal F_\phi\) |
| L=3 gauge rank drop | graphification and rank of \(\mathcal B\) do not read \(\Sigma_{\rm skew}\) |
| L=2 Nyquist | off-diagonal symmetric \(H\) is retained; skew fibre over it is still free. Not deleted |
| L=3 corner | same: the corner sits in \(\operatorname{sym}\), not in \(\mathfrak{so}(4)\) |
| Harmonic raw coframe | can have \(H=0\) with \(e\notin\operatorname{im}d_f\); then \(G=\Sigma_{\rm skew}(e)\) is pure skew and \(DW=0\). Two such \(G\) are distinguished only by \(\Sigma_{\rm skew}\) |
| Nontrivial labelled holonomy | endpoint descent fails for the path family; that predicate does not constrain \(\Sigma_{\rm skew}\) |
| Rank-deficient active span | #127: sourced chain ignores \(J\) off the span. It still ignores \(\Sigma_{\rm skew}\) |

No control was passed by dropping Nyquist, corner, or harmonic modes.

## 5. Second-order firewall

No Hessian, \(Q\), universal \(S\), or second-order constitutive kernel is
chosen. For each fixed \(\Sigma_{\rm skew}\), the second derivative of the ordered
exponential is a later object. It is not part of this classification.

## 6. Not claimed

No Einstein equation, GR limit, QFT, physical time, golden/AF refinement,
\(k=n\), or continuum limit.

## 7. Checker

`python3 02_REGISTRY/research/certificates/a4d_finite_graded_coframe_dressing_check.py`

Exact `Fraction` arithmetic. Records: the first-order identity; that polar
projection is a choice; that \(J\)/\(\kappa\)/observer/endpoint data do not
read the skew fibre; that frame conjugation preserves nonzero skew orbits;
that the transverse constant mode at \(L=3\) carries a free skew operator; that ordered exponentials keep the
difference at order \(\varepsilon\); that a nonzero corner entry of \(H\) does
not remove the skew fibre.

## 8. Reconciled handoff after PR #130

The finite-existence question is no longer the frontier. The remaining constitutive
research seam is an **equivariant joint-background dressing/groupoid law** which
must decide its domain explicitly:

\[
(A,e)\in\mathfrak A_{\rm stable}
\qquad\text{or}\qquad
(A,e,\Xi)
\]

when the dressing is coupled to the already-owned affine-sensitive channel
\(T_\kappa\).

A satisfactory next construction must simultaneously account for:

- the constant-potential orthogonal torsor of the exact pure-gauge dressing;
- the no-go for a coframe-only frame-equivariant exact-orbit retraction;
- the transverse skew/order modulus \(\Sigma_{\rm skew}\);
- exact labelled path/background composition;
- the stable/resolved \(\kappa\) typing from PR #130;
- raw Nyquist/corner/harmonic controls without an endpoint quotient that erases them.

Until such a law is owned, any explicit finite \(\mathcal F_e\) should be described
as a **chosen representative** of the classified family, not as a canonical
arbitrary-background dressing.

No second-order Hessian/stress/Einstein step is opened by this terminal.
