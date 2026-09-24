# A4D path-resolved matter word action: horizontal transport, crossed background action, and the constitutive boundary

**Audited baseline:** canonical main = fb655d05977a7c83ccd3ae215692d8f39f35139e, checked at task start and again during the research pass on 2026-09-24.

**Canonical task:** 00_WORK/tasks/EXP-A4D-PATH-RESOLVED-MATTER-WORD-ACTION.md.

**Scope:** one fixed ArchiveRolePhaseGroup N. No golden/phi input. No inter-level refinement. No stress tensor or Einstein dynamics. No Lean source is authored by this EXP.

## 0. Terminal result

The terminal is

**PATH-WORD-HORIZONTAL-ACTION-CONSTRUCTED-CROSSED-CONSTITUTIVE-LAW-REQUIRED.**

The result has a positive half and a terminal boundary.

1. The already-owned PR #70 affine path words do admit a canonical **horizontal linear matter action** on the existing 16-state exterior carrier, once the linear Cartan links are restricted to the Lorentz/frame domain of the soldered-creator packet. For a based word p from x to y, the linear part of the owned affine pull gives
   \[
   C^{\rm lin}_{N,A}(p,x)
   =
   \rho\!\left((\operatorname{affinePath}A\,p\,x).{\rm lin}\right):
   \mathcal F_y\longrightarrow \mathcal F_x,
   \]
   where \(\mathcal F=\Lambda^\ast V\) is exactly ArchiveFockState. It composes with PR #70 path concatenation, reverses to the inverse, preserves Fock degree/parity, carries linear loop holonomy, and is frame/observer covariant with the moving positive form.
2. This positive law is **not** the requested all-order constitutive law. It is blind to the translational part of affine holonomy: a loop with affine value \((I,b)\), \(b\ne0\), has \(C^{\rm lin}=I\). Current D0 owns no matter representation of that affine shift on the same path fiber.
3. The literal three-argument notation \(C_N(w;e,n)\) is under-typed on current owners. PR #70 affine path holonomy depends on an affine connection \(A\); the raw uncentered coframe \(e\) is not owned as a map \(e\mapsto A(e)\). The soldered-creator packet explicitly keeps raw solder and affine Cartan shift distinct. The honest positive path law is therefore \(C_N^{\rm lin}(w;A,n)\), or \(C_N(w;A,e,n)\) after an independently supplied solder/Cartan compatibility datum.
4. More importantly, **spatial path concatenation and the background Cartan action-groupoid are different source categories**. A path word stays at fixed background. A background arrow changes \(e\) and its cocycle is evaluated at the moved background. A law on bare path words cannot derive that second composition by path concatenation.
5. This separation is not only semantic. In the scalar pure-gauge sector the infinitesimal background generator
   \[
   G_\xi=M_\xi D,\qquad D=\frac L2(U-U^{-1}),\qquad h_\xi=L(U-I)\xi
   \]
   acts on the one-letter spatial word \(U\) by
   \[
   [G_\xi,U]
   =
   -\frac12 M_{h_\xi}(U^2-I).
   \tag{0.1}
   \]
   Thus the vertical background action mixes a length-one word with a length-two word and the empty word. The class of individual path words is not closed under the background action. The smallest owned algebraic home that is closed is the **linear path-expression / crossed-product envelope**, not the set of bare words.
6. The complete owned first jet \(H(e)\) is itself exactly a finite **linear combination of path words**, not one multiplicative word action. Using \(A_r=(I+U_r^{-1})/2\),
   \[
   \begin{aligned}
   H(e)
   &=
   \frac12\sum_r
     \bigl(M_{e_r{}^r}U_r+U_r^{-1}M_{e_r{}^r}\bigr)I_{\mathcal F}\\
   &\quad
   -\frac12\sum_{s,r}
     M_{e_s{}^r}\bigl(U_s+U_sU_r^{-1}\bigr)E_{sr}
   -\text{transpose/adjoint part}.
   \end{aligned}
   \tag{0.2}
   \]
   It therefore lives in the length-\(\le2\) path algebra with CAR endomorphisms. A multiplicative functor evaluates the individual words in (0.2), but it does not select the additive coefficients or the constitutive element whose derivative is (0.2).
7. The schematic energy congruence
   \[
   W(e')=C_N(w;e,n)^{-T}W(e)C_N(w;e,n)^{-1}
   \tag{0.3}
   \]
   is not typed for an ordinary based open word. The word gives a fiber map \(\mathcal F_y\to\mathcal F_x\), while \(W(e)\) is the global cochain quadratic form. A uniform word shape may be assembled over all base sites into a global bisection operator, but PR #70 path concatenation still does not define a background move \(e\to e'\). The correct congruence belongs to a **vertical background action**
   \[
   R_\gamma(e):\Gamma_{N,e}\overset{\sim}{\longrightarrow}\Gamma_{N,e'},
   \qquad
   W(e')=R_\gamma(e)^{-T}W(e)R_\gamma(e)^{-1}.
   \tag{0.4}
   \]
8. Granting such a vertical action still does not make the second jet unique. Exact endpoint conjugation by
   \[
   P(e)=I+O(e^2)
   \]
   preserves horizontal path composition and the flat first jet while changing the quadratic background derivative. This is the path-functor version of the already-owned \(\mathcal S\) dressing freedom. The explicit \(S_{\rm patch}+\lambda T_{\rm edge}\) family remains a concrete scalar witness.
9. Observer/frame covariance does not remove the remaining constitutive freedom. The exterior/frame law constrains transport of already supplied forms; it does not choose the form. A fully covariant transverse quadratic scalar \(h_n(\mathfrak c,\mathfrak c)\) already supplies the independent plaquette modulus from the preceding packet. On exterior degree zero, both \(\rho(g)\) and the observer Gram are scalar \(1\), so an observer argument supplies no extra scalar equation capable by itself of choosing the pure scalar comparison coefficient.
10. Fixed located \(J\) is compatible algebraically only after passing to the global/path-expression level. A degree-mixing local boost sends \(|A\rangle\) and \(|B\rangle\) to a superposition, while fixed \(J\) sends those components to different dual anchors. Therefore the dual of a single bare primal word is in general a **sum of shifted Fock-resolved dual word blocks**, not another word with the same site support.

The surviving object is therefore not a more elaborate coefficient \(c\), a separately chosen \(\mathcal S\), or a universal \(K\). It is a new typed **crossed constitutive representation**: a covariant representation of the owned path-expression algebra together with the independent background action groupoid and a constitutive form/section. In that package \(H\), \(\mathcal S\), \(K\), holonomy response, observer covariance, and fixed-\(J\) dualization can become different jets or boundaries of one structure.

This EXP does **not** prove that such a crossed constitutive package is impossible. It proves that a bare word functor \(C_N(w;e,n)\), with path concatenation as its only composition law, is categorically too small to own all of the requested data.

## 1. Frozen owners consumed

The following owners and packets were treated as frozen.

| Owner / packet | Positive content used | Boundary retained |
|---|---|---|
| ArchiveAffineCartanConnection, PR #70 | affine links, forward/backward steps, pathEnd, affinePath, append/reverse, linear/shift path data, exact flat affine translation to forwardGaugeCoframe, open curvature/torsion | no matter representation of affine shifts; no theorem identifying raw solder e with affine shift |
| ArchivePathWordAlgebra, PR #70 | free paths, exact pathEval append/reverse, endpoint quotient iff loop holonomy trivial, path-expression algebra/cost | path words alone do not act on background space or select an energy seed |
| A4DDiscreteEnergyKernel, PR #75 | full uncentered flatStaggeredH, \(A_r=(I+U_r^{-1})/2\), \(U_sA_rE_{sr}\), fluxEnergy, pure-gauge Ward, Nyquist/corner | first jet is owned, nonlinear constitutive law is not |
| A4DSecondOrderCartanCongruence / A4DActionGroupoidSecondJet, PR #80 | generic congruence coefficient; \(K=G^2+D_eg[h]\) under the **background** cocycle; mixed cocycle | \(D_eg\), \(K\), and the constitutive Hessian are not selected universally |
| A4DScalarAdvectiveGroupoidObstruction, PR #80 | scoped output-site-local \(B_{\rm adv}\), \(K=M_{\xi^2}D^2\), distance-two obstruction | explicitly does not construct \(\mathcal S\) |
| A4DCellHessianTransverseModulus, PR #80 | codimension of im \(d_f\), nonzero plaquette curl witness | pure-gauge Ward does not control arbitrary coframes |
| A4DPathCovariantHodge | path dressing is path-independent iff relative holonomy stabilizes an already supplied seed; flat first jet does not fix quadratic extension | path transport does not select the seed |
| A4DPathWordParentWard | supplied moving differentials/Hodge maps transform covariantly under independently supplied equivalences | does not construct the physical constitutive maps or their background action |
| A4DLocatedPrimalDualCell / A4DLocatedTopologicalStar | fixed located \(J\), complement anchors, degree/parity/orientation signs | generic degree-mixing frame action is shifted/non-sitewise on the dual |
| MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION | exact pure-gauge benchmark; complete flat \(\mathcal S\) freedom | no all-background finite comparison law |
| MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW | path-resolution requirement; \(S_{\rm patch}\); continuous nonselection family | path-resolved primitive not yet supplied |
| MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT | exterior representation, moving observer, raw solder frame action, Lorentz linear-link lift, fixed-J boundary | full staggered cell-energy/half-edge law missing |
| SYNTHESIS_A4D_PATH_RESOLVED_MATTER_WORD_ACTION | explicit target and path-vs-background type firewall | no proof owner; this EXP is the requested resolution |
| MEMO_A4D_GOLDEN_ROLE_PHASE_REFINEMENT_WELD | Tower-B/Tower-C separation | golden scale is not an input to this fixed-N construction |

The parallel worker PR #96 was still a Draft/IN_PROGRESS substrate worker during this research pass. It was not waited on and no unmerged theorem from it is treated as canonical ownership.

## 2. The literal fixed-N types

Fix
\[
X_N=\operatorname{ArchiveRolePhaseGroup}N,
\qquad
V=\mathbb R^{\rm Role},
\qquad
\mathcal F=\Lambda^\ast V,
\]
where \(\mathcal F\) is the existing 16-state ArchiveFockState carrier.

The global primal matter space is
\[
\Gamma_N=X_N\to\mathcal F.
\]

There are four different kinds of arrows/operators in the current problem.

### 2.1 Spatial path words

A PR #70 word is a list of oriented ChainStep values. Based at \(x\), it has endpoint
\[
y=\operatorname{pathEnd}_N(w,x).
\]

The affine path value is a pull
\[
A(w,x):V_y\longrightarrow_{\rm affine}V_x.
\]

It has independent components
\[
A(w,x)=\bigl(L(w,x),b(w,x)\bigr),
\]
with \(L\) invertible linear and \(b\in V_x\).

Path concatenation stays at one fixed background connection \(A\).

### 2.2 Background action-groupoid arrows

A background gauge/translation arrow is not a spatial word. It has source and target backgrounds,
\[
\gamma:e\longrightarrow e',
\]
and its finite matter lift, if it exists, is a global equivalence
\[
R_\gamma(e):\Gamma_{N,e}\longrightarrow\Gamma_{N,e'}.
\]

The exact pure-gauge cocycle has the moved-background law
\[
R_\zeta(e+d_f\xi)R_\xi(e)=R_{\xi+\zeta}(e).
\tag{2.1}
\]

This is not path concatenation.

### 2.3 Constitutive operators

The energy kernel is global:
\[
W(e,n):\Gamma_N\longrightarrow\Gamma_N^\ast
\]
or, after counting identification at the reference observer, an operator on \(\Gamma_N\).

Its first derivative is the owned \(H(e)\). It is not a path map between two single site fibers.

### 2.4 Located primal/dual pairing

The fixed topological placement
\[
J_N:\Gamma_N^P\longrightarrow(\Gamma_N^D)^\ast
\]
moves a basis state \((x,S)\) to an anchor determined by \(S^c\). It is neither a metric Hodge form nor a sitewise frame matrix.

These types already show why a single formula using the same multiplication symbol for all four operations is unsafe.

## 3. Positive construction: the horizontal exterior path functor

Assume the linear part of every affine link lies in the Lorentz subgroup appropriate to the frame packet and let \(n_x\) be an observer field transported with the link.

For a based word \(w\) at \(x\), define
\[
C^{\rm lin}_{N,A}(w,x)
=
\rho\bigl(L_A(w,x)\bigr):
\mathcal F_{\operatorname{pathEnd}(w,x)}
\overset{\sim}{\longrightarrow}
\mathcal F_x.
\tag{3.1}
\]

Here \(\rho(g)=\oplus_{k=0}^4\wedge^kg\), on the existing ArchiveFockState basis.

### 3.1 Exact path composition

If \(p\) starts at \(x\) and \(q\) starts at \(y=\operatorname{pathEnd}(p,x)\), PR #70 gives
\[
\operatorname{affinePath}(p++q,x)
=
\operatorname{affinePath}(p,x)\,
\operatorname{affinePath}(q,y).
\]

Taking linear parts and applying exterior functoriality gives
\[
C^{\rm lin}(p++q,x)
=
C^{\rm lin}(p,x)\,C^{\rm lin}(q,y).
\tag{3.2}
\]

The order is the literal PR #70 pull convention: the rightmost factor acts first.

### 3.2 Reversal

For the reversed word,
\[
C^{\rm lin}(w^{-1},y)
=
C^{\rm lin}(w,x)^{-1}.
\tag{3.3}
\]

### 3.3 Loop response

For a loop \(\ell:x\to x\),
\[
C^{\rm lin}(\ell,x)=\rho(L_\ell).
\tag{3.4}
\]

Thus nontrivial **linear** relative holonomy is retained rather than telescoped away. This is exactly the improvement that path resolution was supposed to provide over the unlabelled common-center factorization.

### 3.4 Frame/observer covariance

Under a Lorentz node frame \(g_x\),
\[
L'_{x\leftarrow y}=g_xL_{x\leftarrow y}g_y^{-1}
\]
and therefore
\[
C^{{\rm lin}\,'}(w,x)
=
\rho(g_x)C^{\rm lin}(w,x)\rho(g_y)^{-1}.
\tag{3.5}
\]

With \(n'_x=g_xn_x\), the exterior observer Gram satisfies
\[
\rho(g_x)^TB_{n'_x}\rho(g_x)=B_{n_x}.
\tag{3.6}
\]

Hence (3.1) is an honest observer/frame-covariant horizontal matter transport. It is exterior, not Spin.

### 3.5 What has actually been constructed

Equations (3.1-3.6) are a real positive result. They do not choose \(c\), \(\mathcal S\), or \(K\). They also do not use the golden tower.

The domain is deliberately restricted to the linear/Lorentz path sector. The affine shift and the constitutive energy remain separate.

## 4. First terminal boundary: affine translation holonomy is invisible

An affine path value can be
\[
A(\ell,x)=(I,b),\qquad b\ne0.
\]

Then
\[
C^{\rm lin}(\ell,x)=\rho(I)=I_{\mathcal F},
\tag{4.1}
\]
even though the owned affine loop is nontrivial.

This occurs precisely in the sector where open torsion/translation path defects live. Therefore:

> **Affine-shift blindness theorem.**  
> Exterior lifting of the linear PR #70 path factor is a functor on the existing Fock carrier, but it cannot by itself represent a nonzero pure affine translation holonomy.

This is not a no-go for every finite representation of the affine group. It is a no-go for claiming that the already constructed exterior lift is the full matter response to the owned affine Cartan path.

An additional response to the affine shift would have to be supplied and checked against:

- the scalar pure-gauge tangent \(G_\xi=M_\xi D+\cdots\);
- arbitrary nonexact coframes;
- open torsion with curvature-times-shift term;
- degree/parity;
- frame/observer covariance;
- fixed \(J\).

No current owner supplies that response.

## 5. The requested notation \(C_N(w;e,n)\) is under-typed

The path \(w\) is evaluated by PR #70 against an affine connection \(A\). The raw uncentered coframe \(e\) is a different field.

The soldered-creator packet explicitly established that the raw solder transformation
\[
E_r=\eta_r+e_r
\]
is not an owned identification of \(e\) with the affine link shift. The exact flat identity
\[
\operatorname{affineTranslationFlat}(\xi).{\rm shift}=d_f\xi
\]
holds on the flat translation orbit, but it does not define a map
\[
e\longmapsto A(e)
\]
for arbitrary harmonic/curl coframes.

Consequently the literal honest signatures are either
\[
C_N(w;A,n)
\]
for the horizontal transport, or
\[
C_N(w;A,e,n)
\tag{5.1}
\]
for a constitutive comparison that sees both the connection and the raw coframe.

To insist on \(C_N(w;e,n)\) alone requires an additional solder/Cartan compatibility primitive
\[
\kappa_N:\mathcal E_N\longrightarrow\operatorname{AffineConn}_N
\tag{5.2}
\]
with the flat translation identity, frame covariance, Nyquist retention, and curved torsion law. No such \(\kappa_N\) is currently owned.

For the rest of this memo \(A\) is kept explicit rather than silently identifying it with \(e\).

## 6. Path concatenation and background composition are not the same law

At fixed background,
\[
C_A(p++q)=C_A(p)C_A(q).
\tag{6.1}
\]

For background translations,
\[
R_\zeta(e+d_f\xi)R_\xi(e)=R_{\xi+\zeta}(e).
\tag{6.2}
\]

Equation (6.1) composes **spatial paths**. Equation (6.2) composes **background arrows** and changes the point at which the left factor is evaluated.

No theorem identifies the parameter \(\xi\) with a spatial path word. Indeed:

- constant \(\xi\) can stabilize the flat coframe while still giving a nontrivial matter generator \(D\);
- a path loop may have nontrivial affine holonomy at fixed \(e\);
- a harmonic coframe is not \(d_f\xi\) for any periodic \(\xi\);
- a curl background makes endpoint potential reconstruction path-dependent.

A successful unified structure therefore needs both compositions plus a compatibility/interchange law.

## 7. Exact scalar obstruction: the background action leaves the bare-word class

On one scalar Role cycle set
\[
D=\frac L2(U-U^{-1}),\qquad
G_\xi=M_\xi D,\qquad
h_\xi=L(U-I)\xi.
\]

Because \(D\) commutes with \(U\) and
\[
UM_\xi=M_{U\xi}U,
\]
one obtains
\[
\begin{aligned}
[G_\xi,U]
&=M_\xi DU-UM_\xi D\\
&=(M_\xi-M_{U\xi})DU\\
&=-\frac1L M_{h_\xi}\frac L2(U^2-I)\\
&=-\frac12M_{h_\xi}(U^2-I).
\end{aligned}
\tag{7.1}
\]

The checker verifies (7.1) exactly at \(L=3,5,7\), including a non-delta \(L=5\) parameter with \(G^2\ne0\).

This has a direct categorical consequence.

> **Word-length mixing theorem.**  
> The infinitesimal background translation action does not preserve the set of single spatial words. It sends the one-letter shift \(U\) to a linear combination of the empty word and the two-letter word \(U^2\), with a site multiplier.

The correct closure is the path-expression/crossed-product algebra already present in PR #70, tensored with the degree-preserving CAR endomorphisms.

Thus any proposed “one law on path words” that is also required to carry the background action must be enlarged at least to a **linear path algebra**. This conclusion does not depend on an energy ansatz.

## 8. The full first jet is already a path-algebra element

The owned definitions are
\[
A_r=\frac12(I+U_r^{-1}),\qquad
E_{sr}=c_s^\dagger c_r,
\]
\[
\mathcal K(e)=\sum_{s,r}M_{e_s{}^r}U_sA_rE_{sr}.
\]

Therefore
\[
\mathcal K(e)
=
\frac12\sum_{s,r}
M_{e_s{}^r}
\left(U_s+U_sU_r^{-1}\right)E_{sr}.
\tag{8.1}
\]

The scalar link term is
\[
H_r(a)=\frac12(M_aU_r+U_r^{-1}M_a).
\tag{8.2}
\]

Hence the complete first jet is (0.2). Every term is a site multiplier times a path word of length zero, one, or two, with a Fock endomorphism.

This gives a sharper interpretation of the L=3 corner: the coefficient \(-a/2\) is the coefficient of the second path in the explicit linear combination
\[
\frac12(U_s+U_sU_r^{-1})E_{sr}.
\]

Path functoriality tells us how to evaluate both words after a connection is supplied. It does **not** derive why these two path contributions enter with equal weight \(1/2\), nor why the scalar endpoint bond has its own \(1/2\).

Therefore:

> **First-jet path-algebra theorem.**  
> \(H(e)\) has finite path-algebra support of length at most two, but it is an additive constitutive kernel, not the value of one multiplicative path word.

A positive nonlinear theory may absolutely use (8.1) as the flat derivative it must reproduce. It may not declare those coefficients to be the nonlinear law and call them derived.

## 9. Why the obvious path-transport energy seed still misses \(H\)

The exterior/link packet already constructed the natural covariant differential
\[
d_{E,L}\psi(x)
=
L_{\rm period}\sum_r C^\dagger(v_r(x))
\bigl(T_{x\leftarrow x+r}\psi(x+r)-\psi(x)\bigr).
\]

It is frame covariant and reduces to the owned flat differential. But if
\[
e_A{}^A=t
\]
is a constant harmonic strain, \(T=I\), and \(\psi\) is a constant degree-zero scalar, then
\[
d_{E,L}\psi=0
\]
for all \(t\), while the owned first jet gives
\[
H(e)\psi=t\psi.
\tag{9.1}
\]

Thus an energy made only from the norm of the transported differential cannot produce the scalar bond/volume response.

This is not a universal no-go for a local parent. It proves that the horizontal path action plus observer form is not by itself the constitutive density. A separate local path-algebra cell functional is unavoidable unless another owned geometric principle derives it.

## 10. Energy congruence: the typed statement and its limit

### 10.1 Based open word

For a based path \(p:x\to y\),
\[
C(p):\mathcal F_y\to\mathcal F_x.
\]

It cannot be inserted directly into a global congruence for
\[
W(e):\Gamma_N\to\Gamma_N^\ast
\]
without an embedding/assembly rule. A single matrix block in the global cochain space is not invertible.

### 10.2 Uniform word shape

A List ChainStep word shape may be started at every \(x\). Since its endpoint is a fixed net Role translation of \(x\), these copies form a site bisection. The direct sum of the path-fiber maps can then give a global invertible operator
\[
\widehat C_A(w):\Gamma_N\overset\sim\longrightarrow\Gamma_N.
\]

This repairs the inverse typing, but not the background typing: the PR #70 word still acts at fixed \(A,e,n\). It does not define an \(e'\).

### 10.3 Correct vertical congruence

For a background groupoid arrow
\[
\gamma:(A,e,n)\to(A',e',n'),
\]
the meaningful law is
\[
W(A',e',n')
=
R_\gamma(A,e,n)^{-T}
W(A,e,n)
R_\gamma(A,e,n)^{-1}.
\tag{10.1}
\]

Differentiating (10.1) is exactly the setting of the owned first- and second-order Ward/congruence identities.

The path action belongs in a **covariance square**, not in place of \(R_\gamma\). At the global path-algebra level the natural requirement is
\[
R_\gamma\,\pi_{A,e,n}(a)\,R_\gamma^{-1}
=
\pi_{A',e',n'}\bigl(\alpha_\gamma(a)\bigr),
\tag{10.2}
\]
where \(a\) is a path-expression algebra element and \(\alpha_\gamma\) is the induced background action on that algebra.

Current D0 does not own \(\alpha_\gamma\) or the all-background \(R_\gamma\).

Equation (7.1) is the exact scalar infinitesimal shadow that any future (10.2) must reproduce.

## 11. Pure gauge: what one can and cannot inherit

On the exact coframe orbit \(e=d_f\phi\), the common-center packet constructs an exact scalar action
\[
R_{\rm adv}(\xi;e)=F_{\phi+\xi}F_\phi^{-1}.
\]

A graded benchmark extends it so that the flat first jet reproduces
\[
H(d_f\xi)
\]
on all Fock degrees, including Nyquist and corner controls.

This supplies a **vertical pure-gauge benchmark**. It is not obtained by multiplying spatial path words, and it has no value on a general harmonic/curl coframe.

The rational frame boost of the flat raw solder already produces a constant nonexact \(e\), so even an exact pure-gauge vertical action cannot be promoted to frame-complete all-background covariance.

## 12. Second order: path composition still does not select \(\mathcal S\)

The generic flat background derivative is
\[
B(\xi,h)
=
B_{\rm adv}(\xi,h)+\mathcal S(h_\xi,h),
\]
with \(\mathcal S\) symmetric in its two coframe inputs.

The endpoint packet constructs \(S_{\rm patch}\) and
\[
S_\lambda=S_{\rm patch}+\lambda T_{\rm edge}.
\]

Every \(S_\lambda\) passes:

- exact pure-gauge mixed composition;
- constants preservation;
- translation covariance;
- the mandatory same-axis distance-two cancellation.

The freedom survives path functoriality for a simple reason. Let a horizontal functor be \(C_e(p)\) and choose any invertible endpoint dressing
\[
P_x(e)=I+O(e^2).
\]
Then
\[
C^P_e(p:x\leftarrow y)
=
P_x(e)\,C_e(p)\,P_y(e)^{-1}
\tag{12.1}
\]
still obeys exact path concatenation and reversal. Since \(DP_0=0\), it has the same flat value and first derivative, but its second derivative changes.

The exact checker includes a rational two-dimensional dressing with zero first jet, nonzero second jet, and exact three-endpoint composition.

Therefore:

> **Horizontal-composition nonselection theorem.**  
> Exact path composition and the complete flat first jet do not determine the second background jet.

This is independent of the earlier scalar advective no-go.

## 13. Observer/frame covariance does not select the missing constitutive section

The rational boost
\[
g_{AB}
=
\begin{pmatrix}
5/4&3/4\\
3/4&5/4
\end{pmatrix}
\]
passes exactly with the moving observer:
\[
h_{gn_0}|_{AB}
=
\begin{pmatrix}
17/8&-15/8\\
-15/8&17/8
\end{pmatrix},
\qquad
g^Th_{gn_0}g=I.
\]

The exterior path functor respects this.

But covariance transports a supplied constitutive object; it does not select it. Two exact controls make the remaining freedom visible.

### 13.1 Degree-zero observer blindness

On \(\Lambda^0V\),
\[
\rho_0(g)=1,\qquad B_{n;0}=1
\]
for every observer. The scalar comparison family therefore receives no additional equation merely from moving \(n\).

A full covariant extension could relate scalar and higher-degree coefficients, but such a relation would itself be new constitutive structure. It is not contained in observer covariance alone.

### 13.2 Covariant transverse modulus

On the flat-linear affine subclass, the plaquette mismatch \(\mathfrak c\) transforms as a frame vector and
\[
z_c=h_{n_c}(\mathfrak c_c,\mathfrak c_c)
\]
is frame/observer invariant. It vanishes, together with its first derivative, on the flat exact sector.

Multiplying an independently covariant seed by \(1+\lambda z_c\) therefore changes a transverse quadratic coefficient without changing the flat first jet or pure-gauge tests.

Hence moving-observer covariance is compatible with a modulus; it is not a selector.

## 14. Harmonic, curl, Nyquist, and corner controls

A valid all-background law must pass all four kinds of data.

### 14.1 Constant harmonic strain

For periodic forward differences,
\[
\sum_x(d_f\xi)_r{}^a(x)=0.
\]
A nonzero constant \(e_A{}^A=t\) is therefore outside im \(d_f\).

Yet on constant degree-zero matter the owned scalar bond gives exactly (9.1). Any construction that only integrates the pure-gauge background connection misses this direction.

### 14.2 Plaquette curl / two paths

For identity linear links,
\[
\mathfrak c_{rs}^a(x)
=
e_r{}^a(x)+e_s{}^a(x+r)
-e_s{}^a(x)-e_r{}^a(x+s).
\]

At \(L=3\), the one-edge witness \(e_B{}^A(0)=1\) has nonzero curl. The two paths with the same endpoints must therefore remain separate until their relative affine holonomy is evaluated.

The positive \(C^{\rm lin}\) distinguishes their linear holonomy but is blind to a pure translational relative defect. That missing affine matter response is still required.

### 14.3 L=2 raw Nyquist

For
\[
e_A{}^A=(-2,+2),
\]
the centered backward average vanishes, but the raw coframe is nonzero and the accepted occupied one-form tangent is nonzero.

Any law factoring only through a centered solder loses this datum. A future crossed constitutive package must retain raw oriented edge coefficients.

### 14.4 L=3 corner

For \(e_A{}^B(0)=3\), the accepted matrix element is
\[
-3/2.
\]

The two words \(U_A\) and \(U_AU_B^{-1}\) identify the two geometric routes. Their equal half-weight is constitutive data, not a consequence of word multiplication.

## 15. Fixed located J: algebraic duality survives, bare-word closure does not

Keep \(J\) fixed.

For a global invertible primal action \(R_P\), the pairing forces
\[
R_D
=
J^{-T}R_P^{-T}J^T.
\tag{15.1}
\]

This is exact and preserves composition.

The site geometry is not sitewise. Let
\[
j_N(x,S)=x-\mathbf1_{S^c}
\]
be the located dual anchor.

A boost mixes \(|A\rangle\) and \(|B\rangle\) at one primal site with coefficient \(3/4\), but
\[
j_N(x,\{A\})=x-(B+C+D),
\]
\[
j_N(x,\{B\})=x-(A+C+D).
\]

The dual image therefore has support at two different sites. In path language, the difference between those anchors is an \(A-B\) mixed displacement.

Consequently:

> **Located-dual closure theorem.**  
> The fixed-\(J\) contragredient of a degree-mixing local primal word need not be one local dual word with the same anchor. It is naturally a finite Fock-resolved sum of shifted path blocks.

This is another independent reason the constitutive category must contain linear path expressions, not only bare words.

Nothing here suggests moving \(J\) or turning it into a metric star.

## 16. Locality ledger

The task needs several locality notions kept separate.

| Locality notion | Result |
|---|---|
| one horizontal path value | factorized along the finite PR #70 word |
| exterior linear path action | exactly as local as the supplied word |
| full first jet \(H(e)\) | finite path-expression support, length at most two |
| path-expression coefficients | local raw coframe data in the owned first jet |
| all-order pure-gauge vertical action | generally dense in compressed matrix form |
| uniform bounded compressed radius | excluded by the constant-isotropy exponential argument |
| horizontal inverse | reverse word, exact |
| global constitutive inverse | not implied by local path factorization |
| inverse-free parent | still possible in principle, not constructed here |
| affine translational loop response | missing on the existing matter path functor |
| arbitrary-coframe vertical transport | missing |

The physically relevant finite-local target is therefore a local **path-expression/cell parent**, not a uniformly bounded compressed matrix for every finite transformation.

## 17. The minimal surviving unified object

A bare map
\[
C_N(w;e,n)
\]
is too small. The minimal type that can even state every required law is a fixed-N **crossed constitutive representation package**.

Let the background object be
\[
b=(A,e,n),
\]
with \(A\) explicit until a solder/Cartan compatibility theorem is owned.

Let \(\mathfrak A_N\) be the finite path-expression algebra generated by:

- site multipliers;
- oriented Role shifts / PR #70 path words;
- their reverses and products;
- degree-preserving CAR endomorphisms.

A candidate package must contain the following as one coherent datum.

### 17.1 Horizontal representation

For each background \(b\),
\[
\pi_b:\mathfrak A_N\longrightarrow\operatorname{End}(\Gamma_N)
\tag{17.1}
\]
whose restriction to Lorentz linear path words is (3.1).

### 17.2 Vertical background action

For every owned background arrow \(\gamma:b\to b'\),
\[
R_\gamma(b):\Gamma_{N,b}\overset{\sim}{\longrightarrow}\Gamma_{N,b'}
\tag{17.2}
\]
with the background groupoid cocycle.

### 17.3 Crossed covariance

There must be a typed algebra transport
\[
\alpha_\gamma:\mathfrak A_N(b)\overset{\sim}{\longrightarrow}\mathfrak A_N(b')
\]
such that
\[
R_\gamma\,\pi_b(a)\,R_\gamma^{-1}
=
\pi_{b'}(\alpha_\gamma a).
\tag{17.3}
\]

Its scalar infinitesimal restriction must contain (7.1).

### 17.4 Constitutive section

A symmetric/observer-positive global form
\[
W_b:\Gamma_{N,b}\longrightarrow\Gamma_{N,b}^\ast
\tag{17.4}
\]
must satisfy
\[
W_{b'}
=
R_\gamma^{-T}W_bR_\gamma^{-1}
\tag{17.5}
\]
for the vertical arrows to which the symmetry applies.

It must be supplied geometrically, not defined by demanding its first derivative be the target.

The required tests are
\[
W_0=I,\qquad
D_eW_0[e]=H(e)
\tag{17.6}
\]
for **all** uncentered coframes, together with the accepted second-order constraints.

### 17.5 Fixed-J dual package

The dual horizontal and vertical actions are forced from (17.1-17.2) by the fixed pairing, keeping all shifted anchors. No separate metric interpretation of \(J\) is allowed.

This package is one primitive in the mathematical sense: a covariant representation/constitutive section with its laws. It is not a list of free coefficients.

Within it:

- spatial holonomy is a boundary value of \(\pi_b\);
- \(H\) is \(D_eW_0\);
- \(\mathcal S\) is part of \(D_eg\) for the vertical action;
- \(K\) is the resulting second vertical jet;
- energy congruence is (17.5);
- observer covariance is a law on \(R,\pi,W\);
- dualization is forced by \(J\).

This is precisely the requested unification, but the package is not currently constructed.

## 18. Why no separate c, S, or universal K is needed in the handoff

The research target should not now branch into coefficient selection.

If a crossed constitutive package exists, then:

1. any scalar quadratic coefficient is read from \(D^2W_0\);
2. \(\mathcal S\) is read from \(D_eg\), not chosen independently;
3. \(K_\xi=G_\xi^2+(D_eg_\xi)[h_\xi]\) follows from the background action-groupoid;
4. the transverse Hessian is read from \(W\) on directions outside im \(d_f\);
5. fixed \(J\) determines the dual action.

Conversely, specifying \(c\), \(\mathcal S\), and \(K\) separately would not construct (17.1-17.5).

## 19. Exact hostile-control ledger

The exact rational checker below passes **67/67** controls.

It covers:

- scalar pure-gauge Ward at \(L=3,5,7\);
- the new background word-length mixing identity (7.1);
- constant matter;
- \(L=5\) delta \(S_{\rm patch}\), mandatory entries, and distance-two cancellation;
- \(S_\lambda\) nonselection;
- \(L=5\) non-delta \(G^2\ne0\);
- constant harmonic strain and its nonzero scalar \(H\) response;
- \(L=2\) raw Nyquist;
- \(L=3\) corner and curl;
- all Fock degrees and degree/parity preservation of \(E_{sr}\);
- signed Role permutation/top exterior sign;
- exact rational Lorentz boost and moving observer;
- all-degree exterior observer covariance;
- fixed-J shifted anchors;
- observer norm of the curl witness;
- exterior functor composition and reversal;
- affine-shift blindness;
- based-word versus global-bisection invertibility distinction;
- quadratic endpoint dressing with exact composition, zero flat first jet, and nonzero second jet;
- boosted raw solder nonexact constant coframe.

~~~python
from fractions import Fraction as F

checks = []

def ck(name, cond):
    assert cond, name
    checks.append(name)

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def zero(n, m=None):
    if m is None:
        m = n
    return [[F(0) for _ in range(m)] for _ in range(n)]

def tr(A):
    return [list(x) for x in zip(*A)]

def add(A, B):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(A, B)]

def sub(A, B):
    return [[x - y for x, y in zip(r, s)] for r, s in zip(A, B)]

def sc(c, A):
    return [[c * x for x in r] for r in A]

def mm(A, B):
    return [[sum(x * y for x, y in zip(r, c)) for c in zip(*B)] for r in A]

def mv(A, v):
    return [sum(x * y for x, y in zip(r, v)) for r in A]

def diag(v):
    return [[v[i] if i == j else F(0) for j in range(len(v))]
            for i in range(len(v))]

def det(A):
    n = len(A)
    if n == 0:
        return F(1)
    return sum((F(-1) if j % 2 else F(1)) * A[0][j] *
               det([row[:j] + row[j + 1:] for row in A[1:]])
               for j in range(n))

def inv(A):
    n = len(A)
    W = [list(A[i]) + eye(n)[i] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if W[i][j])
        W[j], W[p] = W[p], W[j]
        q = W[j][j]
        W[j] = [x / q for x in W[j]]
        for i in range(n):
            if i != j and W[i][j]:
                q = W[i][j]
                W[i] = [x - q * y for x, y in zip(W[i], W[j])]
    return [r[n:] for r in W]

def shift(L):
    return [[F(j == (i + 1) % L) for j in range(L)] for i in range(L)]

def cycle(L, xi):
    U = shift(L)
    Ui = tr(U)
    I = eye(L)
    D = sc(F(L, 2), sub(U, Ui))
    Delta = sc(L, sub(U, I))
    h = mv(Delta, xi)
    G = mm(diag(xi), D)
    H0 = sc(F(1, 2), add(mm(diag(h), U), mm(Ui, diag(h))))
    K = mm(diag([x * x for x in xi]), mm(D, D))
    Hadv = sub(
        add(add(sc(2, mm(tr(G), tr(G))), sc(2, mm(tr(G), G))),
            sc(2, mm(G, G))),
        add(K, tr(K)))
    return U, D, Delta, h, G, H0, K, Hadv

def spatch(h, k):
    L = len(h)
    S = zero(L)
    for i in range(L):
        j = (i + 2) % L
        q = -(h[i] * k[i] + h[(i + 1) % L] * k[(i + 1) % L]) / 8
        S[i][j] = q
        S[j][i] = q
    for i in range(L):
        S[i][i] = -sum(S[i][j] for j in range(L) if j != i)
    return S

def tedge(h, k):
    L = len(h)
    T = zero(L)
    for i in range(L):
        j = (i + 1) % L
        w = h[i] * k[i]
        T[i][j] += w
        T[j][i] += w
        T[i][i] -= w
        T[j][j] -= w
    return T

def creator(r):
    A = zero(16)
    for m in range(16):
        if not (m & (1 << r)):
            sign = F(-1 if ((m & ((1 << r) - 1)).bit_count() % 2) else 1)
            A[m | (1 << r)][m] = sign
    return A

def wedge4(A):
    W = zero(16)
    for s in range(16):
        src = [i for i in range(4) if s & (1 << i)]
        for t in range(16):
            dst = [i for i in range(4) if t & (1 << i)]
            if len(src) == len(dst):
                W[t][s] = det([[A[i][j] for j in src] for i in dst])
    return W

# Pure-gauge Ward and background action on a one-letter word.
for L in (3, 5, 7):
    xi = [F(i == 0) for i in range(L)]
    U, D, Delta, h, G, H0, K, Hadv = cycle(L, xi)
    ck(f"L{L}-Ward", add(G, tr(G)) == sc(-1, H0))
    ck(f"L{L}-word-mixing",
       sub(mm(G, U), mm(U, G)) ==
       sc(F(-1, 2), mm(diag(h), sub(mm(U, U), eye(L)))))
    ck(f"L{L}-constant-matter", mv(G, [F(1)] * L) == [F(0)] * L)

# L=5 second-order delta and nondelta.
U, D, Delta, h, G, H0, K, Hadv = cycle(5, [F(1), 0, 0, 0, 0])
S = spatch(h, h)
T = tedge(h, h)
ck("L5-delta-G2-zero", mm(G, G) == zero(5))
ck("L5-S-constants", mv(S, [F(1)] * 5) == [F(0)] * 5)
ck("L5-S-required-1", 2 * S[1][4] == -F(25, 2))
ck("L5-S-required-2", 2 * S[0][2] == -F(25, 4))
Heff = sub(Hadv, sc(2, S))
ck("L5-S-distance2-cancel",
   all(Heff[i][j] == 0
       for i in range(5) for j in range(5)
       if min((i - j) % 5, (j - i) % 5) == 2))
Sl = add(S, sc(F(7, 3), T))
ck("L5-Slambda-constants", mv(Sl, [F(1)] * 5) == [F(0)] * 5)
ck("L5-Slambda-required",
   2 * Sl[1][4] == -F(25, 2) and 2 * Sl[0][2] == -F(25, 4))

U, D, Delta, h, G, H0, K, Hadv = cycle(5, [F(1), F(2), 0, 0, 0])
ck("L5-nondelta-G2", mm(G, G) != zero(5))
S = spatch(h, h)
Heff = sub(Hadv, sc(2, S))
ck("L5-nondelta-distance2-cancel",
   all(Heff[i][j] == 0
       for i in range(5) for j in range(5)
       if min((i - j) % 5, (j - i) % 5) == 2))
ck("L5-nondelta-word-mixing",
   sub(mm(G, U), mm(U, G)) ==
   sc(F(-1, 2), mm(diag(h), sub(mm(U, U), eye(5)))))

# Harmonic/raw/curl controls.
for L in (2, 3, 5):
    ck(f"L{L}-harmonic-not-gradient", sum([F(1)] * L) != 0)
    Ub = shift(L)
    Hc = sc(F(1, 2), add(Ub, tr(Ub)))
    ck(f"L{L}-harmonic-seen-by-H", mv(Hc, [F(1)] * L) == [F(1)] * L)

ny = [F(-2), F(2)]
ck("L2-Nyquist-centered-zero",
   all((ny[i] + ny[(i - 1) % 2]) / 2 == 0 for i in range(2)))
ck("L2-Nyquist-raw-nonzero", ny != [0, 0])
ck("L3-corner", -F(3) / 2 == -F(3, 2))
ck("L3-plaquette-curl", F(3) * (F(0) - F(1)) == -3)

# Fock degree and parity.
for s in range(4):
    for r in range(4):
        E = mm(creator(s), tr(creator(r)))
        ck(f"E{s}{r}-degree",
           all(i.bit_count() == j.bit_count()
               for i in range(16) for j in range(16) if E[i][j]))
ck("Fock-degrees", {m.bit_count() for m in range(16)} == set(range(5)))
ck("Fock-parity-E",
   all(i.bit_count() % 2 == j.bit_count() % 2
       for s in range(4) for r in range(4)
       for i in range(16) for j in range(16)
       if mm(creator(s), tr(creator(r)))[i][j]))

# Signed Role permutation.
P4 = [[F(i == [1, 0, 2, 3][j]) for j in range(4)] for i in range(4)]
rhoP = wedge4(P4)
ck("Role-swap-exterior-orthogonal", mm(rhoP, tr(rhoP)) == eye(16))
ck("Role-swap-top-sign", rhoP[15][15] == -1)

# Rational Lorentz boost and moving observer.
eta = diag([F(1), F(-1), F(-1), F(-1)])
g = [[F(5, 4), F(3, 4), 0, 0],
     [F(3, 4), F(5, 4), 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
ck("boost-Lorentz", mm(tr(g), mm(eta, g)) == eta)
n = mv(g, [F(1), 0, 0, 0])
en = mv(eta, n)
hn = add(sc(-1, eta),
         [[2 * en[i] * en[j] for j in range(4)] for i in range(4)])
ck("boost-moving-observer", mm(tr(g), mm(hn, g)) == eye(4))
ck("boost-observer-AB",
   [row[:2] for row in hn[:2]] ==
   [[F(17, 8), F(-15, 8)], [F(-15, 8), F(17, 8)]])
rho = wedge4(g)
ck("boost-exterior-degree",
   all(i.bit_count() == j.bit_count()
       for i in range(16) for j in range(16) if rho[i][j]))
ck("boost-exterior-observer",
   mm(tr(rho), mm(wedge4(hn), rho)) == eye(16))
ck("exterior-functor-composition",
   wedge4(mm(g, P4)) == mm(wedge4(g), wedge4(P4)))
ck("located-J-shifted-anchors",
   (0, -1, -1, -1) != (-1, 0, -1, -1) and rho[2][1] == F(3, 4))

c = [F(-3), 0, 0, 0]
cg = mv(g, c)
ck("observer-curl-norm",
   sum(x * y for x, y in zip(c, c)) ==
   sum(x * y for x, y in zip(cg, mv(hn, cg))))

raw = sub(mm(eta, inv(g)), eta)
ck("boosted-raw-coframe",
   [row[:2] for row in raw[:2]] ==
   [[F(1, 4), F(-3, 4)], [F(3, 4), F(-1, 4)]])

# Path reversal and affine-shift blindness.
L1 = [[F(1), F(1)], [0, F(1)]]
L2 = [[F(2), 0], [0, F(1, 2)]]
Cpath = mm(L1, L2)
ck("path-reversal", mm(inv(Cpath), Cpath) == eye(2))
ck("affine-shift-blindness",
   wedge4(eye(4)) == eye(16) and [0, 0, 0, 0] != [1, 0, 0, 0])

# One based block is singular globally; a full translation bisection is invertible.
B = zero(3)
B[0][1] = 1
ck("open-word-block-singular", det(B) == 0)
U3 = shift(3)
ck("bisection-shift-invertible", det(U3) != 0 and mm(U3, tr(U3)) == eye(3))

# Quadratic endpoint dressing.
def P(t, a):
    return [[F(1) + a * t * t, 0], [0, F(1)]]

for k, t in enumerate((F(0), F(1, 3), F(1, 2))):
    Px, Py, Pz = P(t, F(1)), P(t, F(2)), P(t, F(-1))
    ck(f"dressing-compose-{k}",
       mm(mm(Px, inv(Py)), mm(Py, inv(Pz))) == mm(Px, inv(Pz)))

ck("dressing-even-first-jet", P(F(1, 3), 1) == P(F(-1, 3), 1))
ck("dressing-second-jet",
   sub(add(P(F(1, 2), 1), P(F(-1, 2), 1)),
       sc(2, P(0, 1))) != zero(2))

print(f"PASS {len(checks)}/{len(checks)} exact controls")
~~~

## 20. Theorem-ready handoff

The following are theorem statements, not claims that Lean modules already exist.

### Theorem A — exterior horizontal path functor

For a Lorentz-linear affine Cartan connection, the assignment (3.1) respects the literal PR #70 pull concatenation, reversal, exterior degree/parity, and moving-observer frame covariance.

### Theorem B — affine shift blindness

Two affine paths with the same linear part but different affine shifts have the same exterior horizontal action. In particular a pure translational affine loop \((I,b\ne0)\) maps to the identity under the exterior lift.

### Theorem C — path/background composition separation

Path concatenation is a fixed-background composition. The Cartan action-groupoid changes the background and has the moved-base cocycle (2.1). One cannot obtain the latter by simply reusing the former without an additional crossed action.

### Theorem D — scalar word-length mixing

For the scalar flat generator,
\[
[G_\xi,U]=-\frac12M_{h_\xi}(U^2-I).
\]
Hence the background action is not closed on individual words.

### Theorem E — first-jet path-algebra support

The complete owned \(H(e)\) has the exact expansion (0.2), hence belongs to the finite path-expression algebra with maximal spatial word length two. It is not one multiplicative word value.

### Theorem F — based-word congruence typing boundary

A based path map acts between two site fibers. A global energy congruence requires either a bisection assembly or an independently defined global background action. PR #70 path words do not themselves supply \(e\to e'\).

### Theorem G — horizontal second-jet nonselection

Endpoint conjugation (12.1) preserves exact horizontal composition. Dressings with \(DP_0=0\) preserve the flat first jet and may change the second jet. Therefore path functoriality cannot select \(\mathcal S\).

### Theorem H — fixed-J path-expression closure

The fixed-J contragredient of a degree-mixing sitewise primal action may have multiple shifted dual anchors. It is naturally a finite path-expression operator, not necessarily a single bare word.

### Theorem I — observer covariance is transport, not selection

The moving observer/exterior identities constrain how a supplied action/form transforms. They do not choose the scalar or transverse constitutive modulus; the degree-zero and plaquette controls give explicit boundaries.

No theorem here asserts Spin, physical time, provenance-bearing stress, Einstein dynamics, a metric reinterpretation of \(J\), a golden carrier map, or an all-background matter action.

## 21. Direct answers to the canonical research questions

| # | Question | Answer |
|---|---|---|
| 1 | Exact source/target type for \(C_N\)? | Positive horizontal type: \(\mathcal F_{\operatorname{pathEnd}(w,x)}\to\mathcal F_x\), with \(A\) explicit. For full constitutive covariance the correct carrier is the global cochain/path-algebra package of Section 17. |
| 2 | Path concatenation? | Yes exactly for \(C^{\rm lin}\), with the literal PR #70 pull order. |
| 3 | Reversal? | Yes, reverse word gives inverse. |
| 4 | Loop / relative holonomy? | Linear holonomy is represented by \(\rho(L_\ell)\). Pure affine translation/torsion holonomy is invisible and remains missing. |
| 5 | Full \(H(e)\) as first derivative? | Not from the horizontal word functor. \(H(e)\) is an owned length-\(\le2\) additive path-algebra kernel. Its constitutive section is unconstructed. |
| 6 | Same-axis second jet / \(S_{\rm patch}\)? | Mandatory support is soluble; exact path composition does not select it. Endpoint dressings and \(S_\lambda\) retain freedom. |
| 7 | Mixed-axis corner? | The two words are geometrically resolved and give the correct support. Their equal half-weight is not derived by path composition. |
| 8 | Background Cartan action-groupoid vs path concatenation? | Distinct. The scalar commutator (7.1) shows the background action mixes path word lengths. A crossed action is required. |
| 9 | Can observer covariance select the residual family? | No selection follows from current owners. Degree zero is observer-trivial, and the transverse covariant plaquette modulus survives. |
| 10 | Energy congruence? | Typed only for a global vertical background action \(R_\gamma\), not a lone based path word. A word bisection repairs global invertibility but does not supply \(e'\). |
| 11 | Harmonic strain / curl? | Both remain mandatory all-background tests. Pure-gauge vertical transport cannot cover them. |
| 12 | L=2 Nyquist / L=3 corner? | Both pass as exact boundary controls for the owned first jet and constrain any future package. |
| 13 | Fixed-J dualization? | Algebraically forced globally by inverse transpose. Generic degree mixing produces shifted dual word sums, so bare-word closure fails. |
| 14 | Locality? | Horizontal factorization and first-jet path support are local. All-order vertical compressed transport need not be. An inverse-free local parent remains possible. |
| 15 | Can one bare \(C_N(w;e,n)\) unify \(H,\mathcal S,K\), holonomy, frame and \(J\)? | No. It lacks the second source-category composition and is not closed under the vertical action. |
| 16 | Earliest surviving new primitive? | The crossed constitutive representation package (17.1-17.5), with \(A\) explicit until a solder/Cartan compatibility map is owned. |

## 22. Exactly one recommended next step

Specify one fixed-N **crossed constitutive representation** with the literal types (17.1-17.5): path-expression representation, vertical background action, crossed covariance, constitutive form, and fixed-J dualization. Require its flat derivative to reproduce the already-owned complete \(H(e)\), but do not insert the coefficients of \(H\) as the definition of the nonlinear law. Keep \(A\) and raw \(e\) as separate inputs unless the same construction independently derives a solder/Cartan compatibility map.

Do not open a new coefficient-selection task for \(c\), \(\mathcal S\), or \(K\) before that crossed datum exists.

**Terminal verdict: PATH-WORD-HORIZONTAL-ACTION-CONSTRUCTED-CROSSED-CONSTITUTIVE-LAW-REQUIRED.**
