# A4D affine-sensitive site matter link: exact L+B corner, first-jet assembly, and the solder–Cartan B/E boundary

**Canonical task:** EXP-A4D-AFFINE-SENSITIVE-SITE-MATTER-LINK  
**Audited baseline:** 2e9df963fbb4a9aff7ba1a3dc8dd1299d1277b42  
**Research PR:** #109  
**Terminal:** AFFINE-MATTER-LINK-REQUIRES-SOLDER-CARTAN-COMPATIBILITY-PRIMITIVE  
**Status:** theorem-ready research classification; no Lean source is authored here.

This memo starts from the merged PR #103/#107/#108 state and the elementary-link synthesis. It does not identify the affine Cartan connection \(A\), the raw coframe \(e\), or the observer \(n\). It does not introduce a separate \(Q\), \(\mathcal S\), universal \(K\), or abstract constitutive package.

## 0. Terminal verdict

The elementary-link problem can be sharpened substantially beyond “a crossed representation is missing.”

There is an exact **site-aware L+B construction** on the existing 16-state Fock carrier. Let

\[
X=X_N=\operatorname{ArchiveRolePhaseGroup}N,\qquad
\mathcal F=\Lambda^\ast\mathbb R^{\rm Role},\qquad
\Gamma_N=\operatorname{Fun}(X,\mathcal F).
\]

For a local affine pull
\[
A(x,r)=(L_{x,r},b_{x,r}),
\]
define on \(\mathcal F\)

\[
P_0=|0\rangle\langle0|,\qquad
N_b=C^\dagger(b)P_0,\qquad
T_b=I+N_b,
\]
and
\[
R_{\rm nil}(L,b)=T_b\,\rho(L),
\]
where \(\rho\) is the merged PR #103 exterior lift. Since
\[
N_bN_c=0,\qquad
T_bT_c=T_{b+c},\qquad
\rho(L)T_c\rho(L)^{-1}=T_{Lc},
\]
one gets the exact affine law
\[
R_{\rm nil}(L,b)R_{\rm nil}(M,c)
=
R_{\rm nil}(LM,b+Lc).
\]

Putting this coefficient into the literal archive shift gives an invertible site-aware bisection
\[
\mathscr L^{\rm nil}_r(A)
=
M_{x\mapsto R_{\rm nil}(L_{x,r},b_{x,r})}\,U_r.
\]
Its \((x,x+r)\) corner is a genuine map
\[
P_x\Gamma_N
\;\xleftarrow{\;\ell^{\rm nil,+}(A;x,r)\;}\;
P_{x+r}\Gamma_N.
\]
It has exact inverse/reversal, exact labelled path multiplication, reduces to PR #103 when \(b=0\), and distinguishes \((I,b\ne0)\) from the identity on the physical 16-state carrier.

So Channel B is **not** blocked by finite representability or by site support.

Separately, Channel E already has:

1. the exact PR #101 pure-gauge bisection
   \[
   \mathscr L_t(\varphi)=F_\varphi U_tF_\varphi^{-1};
   \]
2. the complete arbitrary-raw-coframe first jet \(H(e)\);
3. the independently defined finite flux energy whose Riesz operator is
   \[
   W_{\rm flux}(e)=I+H(e),
   \]
   hence
   \[
   W_{\rm flux}(0)=I,\qquad
   D_eW_{\rm flux}(0)[e]=H(e).
   \]

The first actual failure occurs when these channels must be **the same elementary object**.

The nilpotent affine response changes Fock degree and parity:
\[
T_b|0\rangle=|0\rangle+C^\dagger(b)|0\rangle.
\]
The PR #101 pure-gauge letter is degree preserving. On the joint pure-gauge orbit, where PR #70 gives the affine shift \(b=d_f\varphi\) and the raw coframe is \(e=d_f\varphi\), an extra B-response must therefore disappear or be converted into the already-owned E response. Off that orbit, it must remain nontrivial for \((I,b\ne0,e=0)\).

At tangent level this requires a comparison of the independent B and E variables modulo the diagonal
\[
(\delta b,\delta e)=(h,h).
\]
In a fixed flat coordinate chart the obvious normal coordinate is \(b-e_r\). But current D0 does not own a frame-covariant identification making this subtraction geometric. Under the merged full raw-solder frame law,
\[
\Theta(e)=\eta+e,\qquad
\Theta(e')=\Theta(e)\Lambda,
\]
so already from \(e=0\),
\[
e'=\eta\Lambda-\eta.
\]
For the exact rational A/B Lorentz boost used by PR #103,
\[
(e')_A{}^A=\frac23,\qquad
(e')_A{}^B=\frac43.
\]
Meanwhile a flat identity affine link with \(b=0\) remains \(b'=0\) under the same constant pure-linear node-gauge conjugation. Thus the naïve mismatch \(b-e_r\) is zero before the frame change and nonzero after it. It is not a covariant B/E comparison.

The full solder leg transforms homogeneously, but it carries a nonzero flat reference leg. Comparing it to the affine shift therefore requires an additional transported/reference edge identification tied to the Cartan link. Existing frame theorems such as the soldered creator covariance take precisely such leg compatibility as a hypothesis; they do not derive it from \(A\) and \(e\).

The earliest missing primitive is consequently:

> a **solder–Cartan edge comparison** that keeps \(A\) and \(e\) independent, vanishes on the joint pure-gauge diagonal, transforms covariantly at the target fibre, and supplies the relative B/E datum to the elementary matter letter.

This is the terminal
\[
\boxed{\texttt{AFFINE-MATTER-LINK-REQUIRES-SOLDER-CARTAN-COMPATIBILITY-PRIMITIVE}.}
\]

It is strictly earlier and sharper than asking for another crossed representation.

---

## 1. Frozen inputs and ownership boundaries

The required synthesis and owner stack were read before the research construction. The relevant frozen facts are:

- PR #70 owns affine maps \((L,b)\), exact multiplication/inverse, literal path append/reverse, node affine gauge, affine path shift, open torsion/curvature, and the exact flat-translation identity
  \[
  b_{x,r}=L\bigl(\xi(x+r)-\xi(x)\bigr)=d_f\xi.
  \]
  It does not identify arbitrary raw coframe data with affine shift data.
- PR #75 owns the complete uncentered \(H(e)\) and the independent finite flux energy.
- PR #101 owns the exact open pure-gauge chart \(F_\varphi\), its cocycle, and the exact pure-gauge matter bisection.
- PR #102 owns the additive path-expression support of the first jet and the scalar word-length obstruction.
- PR #103 owns the exterior lift of the linear affine path channel, all-degree composition/inverse, observer form, creator/contraction covariance, and the rational Lorentz boost control.
- PR #107 owns the free labelled-path research boundary and the conditional shifted-inverse/holonomy/descent skeleton.
- PR #108 owns the scalar first-jet integrability equations for \(L\ge3\): zero cycle sum and plaquette closedness.
- The located owners fix \(J_N\) only after a primal action exists.

The present memo uses none of these facts to set \(A=A(e)\), and it never uses the observer to select the missing B/E comparison.

---

## 2. Exact carrier and site-corner typing

Let
\[
V=\mathbb R^{\rm Role},\qquad
\mathcal F=\Lambda^\ast V,\qquad
\Gamma_N=\operatorname{Fun}(X,\mathcal F).
\]

For \(x\in X\), let \(P_x\) be the archive-site idempotent
\[
(P_x\psi)(y)=\delta_{xy}\psi(y).
\]

The positive Role-\(r\) archive shift has the pull convention
\[
(U_r\psi)(x)=\psi(x+r).
\]
Thus
\[
P_xU_rP_{x+r}:P_{x+r}\Gamma_N\to P_x\Gamma_N
\]
is the literal \((x,x+r)\) site corner.

A legitimate global Role-\(r\) letter is therefore an invertible weighted shift
\[
\mathscr L_r=M_{R_r}U_r,
\qquad
R_r:X\to GL(\mathcal F),
\]
and its local positive letter is
\[
\ell^+(x,r)=P_x\mathscr L_rP_{x+r}.
\]

The algebra for multiplication and inverses is the finite archive crossed endomorphism algebra on \(\Gamma_N\). The free labelled path remains external provenance: compression to a global matrix does not identify distinct words.

For the PR #103 linear channel, \(R_r(x)=\rho(L_{x,r})\), which preserves every exterior degree and parity.

For the exact nilpotent affine control below, \(R_r(x)=R_{\rm nil}(L_{x,r},b_{x,r})\); this acts on the same 16 physical Fock states but does not preserve degree/parity.

---

## 3. Positive L+B letter

On the 16-state carrier define
\[
N_b=C^\dagger(b)P_0.
\]
Because \(P_0C^\dagger(c)=0\),
\[
N_bN_c=0.
\]
Hence
\[
T_b=I+N_b
\]
obeys
\[
T_b^{-1}=I-N_b=T_{-b},
\qquad
T_bT_c=T_{b+c}.
\]

The exterior covariance of creators gives
\[
\rho(L)C^\dagger(c)\rho(L)^{-1}=C^\dagger(Lc),
\]
and \(P_0\) is fixed by the exterior lift, so
\[
\rho(L)T_c\rho(L)^{-1}=T_{Lc}.
\]

Therefore
\[
R_{\rm nil}(L,b)=T_b\rho(L)
\]
is an exact representation of the affine semidirect product:
\[
R_{\rm nil}(L,b)R_{\rm nil}(M,c)
=
R_{\rm nil}(LM,b+Lc).
\]

The corresponding positive global letter is
\[
\boxed{
\mathscr L_r^{\rm nil}(A)
=
M_{x\mapsto R_{\rm nil}(A(x,r))}U_r .
}
\]

Its site corner is
\[
\ell^{\rm nil,+}(A;x,r)
=
P_x\mathscr L_r^{\rm nil}(A)P_{x+r}.
\]

This is not yet the requested final \(\ell_N^+(A,e,n;x,r)\): it is the exact construction of the L+B subproblem and the control against which the B/E coupling is tested.

---

## 4. Negative letter and labelled word product

For any supplied positive family \(\ell^+(A,e,n;x,r)\), the negative label is not independent:

\[
\ell^-(A,e,n;x,r)
=
\bigl(\ell^+(A,e,n;x-r,r)\bigr)^{-1}
:
P_{x-r}\Gamma_N\to P_x\Gamma_N.
\]

Thus
\[
\ell^+(x-r,r)\,\ell^-(x,r)=I_{P_x\Gamma_N},
\]
and
\[
\ell^-(x+r,r)\,\ell^+(x,r)=I_{P_{x+r}\Gamma_N}
\]
with the corresponding pull-order convention.

For a labelled word
\[
p=[s_1,\ldots,s_m]
\]
and \(x_0=x\), \(x_j=\operatorname{pathEnd}(x;[s_1,\ldots,s_j])\), define
\[
\Pi_{A,e,n}(x;p)
=
\ell(x_0,s_1)\ell(x_1,s_2)\cdots\ell(x_{m-1},s_m).
\]

Then
\[
\Pi(x;[])=I,
\]
\[
\Pi(x;p{+\!\!+}q)
=
\Pi(x;p)\Pi(\operatorname{end}(x;p);q),
\]
and
\[
\Pi(\operatorname{end}(x;p);p^{-1})
=
\Pi(x;p)^{-1}.
\]

For \(\ell^{\rm nil,+}\), these are exact consequences of the affine representation and the crossed weighted-shift multiplication.

---

## 5. Exact Channel-L reduction

If the affine shift vanishes,
\[
A(x,r)=(L_{x,r},0),
\]
then
\[
R_{\rm nil}(L_{x,r},0)
=
\rho(L_{x,r}).
\]
Therefore
\[
\mathscr L_r^{\rm nil}(A)
=
M_{x\mapsto\rho(L_{x,r})}U_r.
\]

On each \((x,x+r)\) corner this is exactly the one-edge PR #103 exterior transport of the linear affine pull. Ordered products give
\[
\rho(L_{x,r_1}L_{x+r_1,r_2}\cdots)
\]
in the same pull order as the PR #70 affine path and PR #103 \(\operatorname{exteriorPathTransport}\).

Hence Channel L is recovered by equality, not by a limiting analogy.

---

## 6. Genuine Channel-B sensitivity and the L=3 witness

Take \(L=3\) and one link with
\[
A(x,r)=(I,b),\qquad b=e_A\ne0.
\]
Then
\[
R_{\rm nil}(I,b)=T_b.
\]

On the physical vacuum,
\[
T_b|0\rangle
=
|0\rangle+|A\rangle.
\]
Thus the positive site corner differs from the identity even though the linear affine part is \(I\). A same-endpoint path pair whose affine values differ only by a nonzero shift is distinguished before descent.

This is genuine B sensitivity on the existing physical 16-state fibre plus literal archive/site support. It is not a response living only in an auxiliary homogeneous coordinate.

The same equation exposes the first failure:
\[
T_b
\]
mixes degrees \(0\) and \(1\), and therefore mixes parity.

---

## 7. Channel-E assembly: the strongest already-owned arbitrary-coframe section

The complete uncentered first jet is
\[
\begin{aligned}
H(e)
&=
\sum_r\frac12
\left(
M_{e_r{}^r}U_r
+
U_r^{-1}M_{e_r{}^r}
\right)
-K(e)-K(e)^T,\\
K(e)
&=
\sum_{s,r}
M_{e_s{}^r}
U_sB_rE_{sr},
\qquad
B_r=\frac12(I+U_r^{-1}).
\end{aligned}
\]

The important point is that the repository owns an independent energy, not merely this formal operator. PR #75 defines the site/edge/corner flux energy directly and proves
\[
2E_{\rm flux}(e,\psi)
=
\langle\psi,(I+H(e))\psi\rangle.
\]

Therefore the explicit E-channel section
\[
\boxed{
W_{\rm flux}(e)=I+H(e)
}
\]
is justified by the independently defined finite energy. It obeys
\[
W_{\rm flux}(0)=I,
\qquad
D_eW_{\rm flux}(0)[e]=H(e)
\]
for every raw uncentered coframe direction.

This is the strongest current explicit \(W\)-assembly datum. It is not promoted here to the requested common assembly \(\operatorname{Asm}(\ell)\), because no theorem transports it by a common arbitrary-background affine-sensitive elementary letter.

### 7.1 Literal first-jet support

The derivative includes exactly:

- scalar edge polarization
  \[
  \frac12(M_{e_r{}^r}U_r+U_r^{-1}M_{e_r{}^r});
  \]
- both half-average pieces
  \[
  U_sB_r=\frac12(U_s+U_sU_r^{-1});
  \]
- all mixed CAR bilinears \(E_{sr}\);
- both forward and adjoint corner contributions through \(K+K^T\);
- the \(L=2\) raw Nyquist direction, which is nonzero in the one-form sector although the centered solder vanishes;
- the \(L=3\) distinct-role corner coefficient.

Thus no centered metric or endpoint-only compression can replace this raw E input.

---

## 8. Exact pure-gauge E letter

For
\[
e=d_f\varphi
\]
the merged PR #101 chart supplies an invertible degree-preserving dressing \(F_\varphi\) and the exact global letter
\[
\boxed{
\mathscr L_t^{\rm pg}(\varphi)
=
F_\varphi U_tF_\varphi^{-1}.
}
\]

Its background cocycle is
\[
R_\xi(\varphi)
=
F_{\varphi+\xi}F_\varphi^{-1}.
\]

This exact letter preserves Fock degree and parity. Its derivative on the exact-coframe orbit is the already derived full spatial operator
\[
Q_t(h)
=
-\frac1L\sum_aM_{h_t{}^a}D_aU_t+[K(h),U_t],
\qquad
h=d_f\xi.
\]

Equivalently, with
\[
B_t(h)=Q_t(h)U_t^{-1},
\]
\[
B_t(h)
=
-\frac1L\sum_aM_{h_t{}^a}D_a
+
K(h)-\operatorname{Ad}_{U_t}K(h).
\]

The first term is the scalar response; the second is a CAR/path coboundary. This is why a fixed-site one-edge fibre matrix cannot represent the E tangent.

---

## 9. Earliest failure: the B/E coupling

The exact nilpotent L+B letter and the exact pure-gauge E letter are both real constructions, but they cannot simply be declared to be the same family.

On the joint PR #70/#101 pure-gauge orbit,
\[
b_{x,t}=d_f\varphi(x,t),
\qquad
e_t(x)=d_f\varphi(x,t).
\]
The required specialization is
\[
\ell_t
=
F_\varphi U_tF_\varphi^{-1},
\]
which is degree preserving.

The nilpotent B response at the same nonzero \(b\) sends
\[
|0\rangle\mapsto |0\rangle+C^\dagger(b)|0\rangle.
\]
Therefore it cannot equal the PR #101 letter, nor be related to it by a grading-preserving typed equivalence.

Any successful extension must consequently distinguish two situations:

1. \((b\ne0,e=0)\): Channel B must remain visible;
2. the joint pure-gauge diagonal \(b=e_t=d_f\varphi\): the extra B response must be absorbed into, or become trivial relative to, the PR #101 E letter.

At tangent level, the independent pair
\[
(\delta b,\delta e_t)
\]
must therefore be compared modulo
\[
(h,h).
\]
In a fixed flat chart one would write the normal coordinate
\[
\delta b-\delta e_t.
\]
That subtraction is **not** a covariant D0 datum.

### 9.1 Exact rational boost witness

The merged raw-solder owner defines
\[
\Theta(e)=\eta+e
\]
and the full frame action
\[
\Theta(e')=\Theta(e)\Lambda.
\]
Starting from \(e=0\),
\[
e'=\eta\Lambda-\eta.
\]

For the exact rational A/B Lorentz matrix
\[
\Lambda_{AA}=\Lambda_{BB}=\frac53,
\qquad
\Lambda_{AB}=\Lambda_{BA}=\frac43,
\]
one gets
\[
(e')_A{}^A=\frac23,
\qquad
(e')_A{}^B=\frac43.
\]

Now take the flat identity affine link \(A=(I,0)\). Under a constant pure-linear node gauge, conjugation keeps the affine identity link equal to itself, so
\[
b'=0.
\]

Thus
\[
b-e_A=0
\]
before the frame change, while after the same exact frame change
\[
b'-e'_A=-e'_A\ne0.
\]

So the naïve B/E difference is not frame covariant.

### 9.2 Why the full solder does not close the gap by itself

The full solder leg transforms homogeneously, which is the correct geometric behavior. But at flat background it contains the nonzero reference leg \(\eta_r\), whereas the flat affine shift is zero. To compare a Cartan translation with a full solder leg one must also transport or identify the reference leg across the edge.

That is exactly an edge-level solder–Cartan compatibility datum.

The existing soldered creator/frame theorem is conditional on a hypothesis of the form
\[
\operatorname{solderLeg}(e',x,r)
=
h_x^{\rm lin}\operatorname{solderLeg}(e,x,r).
\]
It proves covariance once a compatible leg is supplied; it does not derive from \(A\) and \(e\) the comparison needed to turn affine shift into a relative solder displacement.

This is the earliest failed coupling. Channel L and Channel B already compose. Channel E already has an exact chart and a complete first jet. Their common finite letter stops at B/E comparison.

---

## 10. Exact finite cycle relation and its derivative to PR #108

Endpoint descent is not imposed on generic backgrounds. In any sector where the labelled action does descend, the exact finite Role-\(t\) period is

\[
\boxed{
\ell_t(x)
\ell_t(x+t)
\cdots
\ell_t(x+(L-1)t)
=
I.
}
\]

At flat background the global letter is \(U_t\) and \(U_t^L=I\).

Let the required scalar first derivative be
\[
Q_t^{\rm sc}(e)
=
-\frac1L\sum_aM_{e_t{}^a}D_aU_t,
\]
and put
\[
B_t^{\rm sc}(e)
=
Q_t^{\rm sc}(e)U_t^{-1}
=
-\frac1L\sum_aM_{e_t{}^a}D_a.
\]

Differentiating the exact period word gives
\[
\begin{aligned}
0
&=
D\bigl(\mathscr L_t^L\bigr)_0[e]\\
&=
\sum_{k=0}^{L-1}
U_t^kQ_t^{\rm sc}(e)U_t^{L-1-k}\\
&=
\sum_{k=0}^{L-1}
\operatorname{Ad}_{U_t}^kB_t^{\rm sc}(e)\\
&=
-\frac1L\sum_a
M_{\sum_{k=0}^{L-1}U_t^ke_t{}^a}
D_a.
\end{aligned}
\]

For \(L\ge3\), the PR #108 separation theorem for the skew-shift basis makes this equivalent to

\[
\boxed{
\sum_{k=0}^{L-1}
e_t{}^a(x+kt)=0
\quad\text{for every }a.
}
\]

This is literally the merged zero-cycle-sum theorem, now obtained as the tangent of the required exact finite period relation.

For the full pure-gauge derivative, the
\[
K-\operatorname{Ad}_{U_t}K
\]
piece telescopes around the cycle, so it contributes no extra period condition.

---

## 11. Exact finite plaquette relation and its derivative to PR #108

In a descended sector, the two labelled plaquette paths must agree in the repository pull order:

\[
\boxed{
\Pi(x;[s,t])
=
\Pi(x;[t,s]).
}
\]

At flat background this is
\[
U_sU_t=U_tU_s.
\]

Differentiate the exact equality. In left-tangent form one obtains
\[
B_s+\operatorname{Ad}_{U_s}B_t
-\operatorname{Ad}_{U_t}B_s-B_t=0.
\]

For the forced scalar tangent,
\[
\begin{aligned}
& B_s^{\rm sc}
+\operatorname{Ad}_{U_s}B_t^{\rm sc}
-\operatorname{Ad}_{U_t}B_s^{\rm sc}
-B_t^{\rm sc}\\
&\qquad=
-\frac1L\sum_a
M_{c_{st}{}^a}D_a,
\end{aligned}
\]
where
\[
c_{st}{}^a
=
e_s{}^a+U_se_t{}^a-U_te_s{}^a-e_t{}^a
=
(U_s-I)e_t{}^a-(U_t-I)e_s{}^a.
\]

For \(L\ge3\), PR #108 separation therefore gives exactly

\[
\boxed{
(U_s-I)e_t{}^a
=
(U_t-I)e_s{}^a .
}
\]

Again the CAR/path part of the pure-gauge tangent is a coboundary and cancels in the first plaquette holonomy, matching the PR #107 diagnostic computation.

Thus both merged PR #108 equations are not detached checks: they are precisely the first derivatives of the finite cycle and plaquette relations required by endpoint descent.

---

## 12. Exact L=2 period

At \(L=2\), the labelled slots
\[
\text{.fwd }r,\qquad \text{.bwd }r
\]
have the same endpoint but remain different labels before descent.

The scalar centered skew operator vanishes:
\[
D_r=\frac L2(U_r-U_r^{-1})=0,
\]
so the PR #108 scalar tangent formula carries no \(L=2\) information.

Nevertheless labelled endpoint descent still forces the exact finite relation
\[
\boxed{
\ell^+(x,r)\ell^+(x+r,r)=I.
}
\]

This is the first nontrivial period relation of the labelled parent and is logically independent of the degenerate scalar first derivative.

The E assembly still sees the raw \(L=2\) Nyquist coframe in occupied Fock sectors, exactly as PR #75/#102 require.

---

## 13. Pure-gauge specialization and exact finite descent

For the PR #101 letter
\[
\mathscr L_t^{\rm pg}(\varphi)
=
F_\varphi U_tF_\varphi^{-1},
\]
the exact period is automatic:
\[
(\mathscr L_t^{\rm pg})^L
=
F_\varphi U_t^LF_\varphi^{-1}
=
I.
\]

Likewise
\[
\mathscr L_s^{\rm pg}\mathscr L_t^{\rm pg}
=
F_\varphi U_sU_tF_\varphi^{-1}
=
F_\varphi U_tU_sF_\varphi^{-1}
=
\mathscr L_t^{\rm pg}\mathscr L_s^{\rm pg}.
\]

Therefore the exact pure-gauge chart lies inside the descended sector, and differentiating those exact identities yields the PR #108 cycle and plaquette equations.

The nilpotent affine L+B letter does not have this specialization on the joint orbit because it is degree mixing. That mismatch is what forces the missing solder–Cartan B/E comparison rather than another independent representation search.

---

## 14. Generic curl and harmonic data remain holonomy

The exact finite relations of §§10–13 are **descent relations**, not background constraints imposed universally.

For a generic harmonic coframe with nonzero Role-\(t\) cycle sum,
\[
\sum_k e_t{}^a(x+kt)\ne0,
\]
the first period holonomy is nonzero. The length-\(L\) labelled cycle therefore remains a nontrivial free-path word.

For a generic curl background with
\[
(U_s-I)e_t{}^a-(U_t-I)e_s{}^a\ne0,
\]
the two plaquette words have nontrivial relative holonomy and remain distinct.

The same principle applies to affine shift holonomy: two same-endpoint words with distinct affine shifts are not compressed until the matter holonomy is proved trivial.

Thus harmonic and curl information is retained as labelled holonomy before endpoint quotienting.

---

## 15. Observer and frame, only after the primal constructions

The observer \(n\) is not needed to define either the exact L+B control or the E first-jet section.

For Channel L, PR #103 already supplies:

- exterior frame covariance;
- moving observer-positive pairing;
- creator/contraction covariance;
- the exact rational A/B boost control.

The nilpotent affine response is also Lorentz covariant as a fibre representation:
\[
\rho(g)T_b\rho(g)^{-1}=T_{gb}.
\]
But it fails degree/parity preservation.

Earlier observer-dependent degree-preserving translation families do not repair the present boundary: they have a trivial scalar/vacuum block, contain free parameters, and therefore cannot reproduce the forced scalar archive response or select the B/E comparison.

The rational boost witness in §9 shows that observer/frame covariance actually sharpens the terminal: it rejects the flat-coordinate subtraction \(b-e_r\). The observer cannot be used to choose another subtraction coefficient.

No physical-time interpretation is made.

---

## 16. Fixed located \(J_N\), only after the primal action

The fixed located pairing does not construct the missing primal letter.

For any primal unit \(R_P\), the common-fibre dual is forced algebraically by inverse transpose, and the located dual is then transported through \(J_N\):
\[
R_D
=
J_N^{-T}R_P^{-T}J_N^T.
\]

For the PR #103 degree-preserving linear channel this retains the owned complement orientation/sign and shifted archive anchors.

For the nilpotent degree-mixing affine control, the same algebraic contragredient exists, but different degree components land in the corresponding different shifted dual blocks. Forcing them into one bare dual site word would erase the located information.

For \(W_{\rm flux}\), degree preservation allows the existing algebraic complementary representative, but no common arbitrary-background affine-sensitive primal transport exists yet.

Thus fixed \(J_N\) is downstream of the B/E coupling and is not the obstruction.

---

## 17. Candidate-carrier comparison

### 17.1 Current 16-state exterior fibre

**Positive:** exact Channel L, all five Fock degrees, parity, observer/frame covariance, creator/contraction covariance.

**Boundary:** the exterior action factors through the linear affine part and is blind to a pure shift \((I,b)\).

**Verdict:** not enough by itself, but it remains the correct physical coefficient carrier for the linear channel.

### 17.2 Nilpotent 16-state affine response

**Positive:** exact affine semidirect representation; inverse; path multiplication; direct physical response to \(b\); literal site-corner implementation; exact L+B reduction.

**Boundary:** mixes degree/parity; has only the elementary weighted-shift support before E dressing; does not specialize to the degree-preserving PR #101 pure-gauge letter.

**Verdict:** proves that Channel B itself is constructible, and localizes the failure to B/E coupling.

### 17.3 Homogeneous 32-state affine exterior lift

Let
\[
\widetilde V=V\oplus\mathbb Re_\ast,\qquad
\widetilde A(L,b)=
\begin{pmatrix}
L&b\\
0&1
\end{pmatrix}.
\]
Then \(\Lambda^\ast\widetilde V\) is a 32-state degree-preserving affine representation.

**Positive:** honest affine group representation and total-degree preservation.

**Boundary:** the original physical \(\Lambda^\ast V\) subspace is translation-blind; translation sensitivity lives in components containing \(e_\ast\). No owned projection/return map converts that auxiliary sensitivity into the physical PR #101/#75 archive action while preserving the required first jet and located \(J_N\).

**Verdict:** not the missing physical site-letter integration.

### 17.4 Site-corner/path-expression enlargement

The current crossed archive endomorphism algebra is large enough for the required one-/two-edge first-jet support. The PR #101 pure-gauge letter and the first-order \(Q_t(e)\) diagnostic live naturally there.

**Positive:** correct site/path support, shifted inverse, free labelled words, pure-gauge chart, and exact first derivatives of descent.

**Boundary:** away from the joint pure-gauge orbit, the coefficient that tells this path-expression letter how the independent affine shift should be compared with the raw solder is not owned.

**Verdict:** this is the correct target class after the missing solder–Cartan comparison is supplied.

---

## 18. Hostile controls

A standalone exact rational checker was run for this memo. It executed **19 exact assertions**:

1. \(N_bN_c=0\);
2. \(T_bT_c=T_{b+c}\);
3. \(T_bT_{-b}=I\);
4. \(T_b\) fails parity commutation;
5. the rational A/B matrix is Lorentz;
6. its 16-state exterior lift has the exact inverse;
7. \(\rho(g)T_b\rho(g)^{-1}=T_{gb}\);
8. a pure \(L=3\) translation changes the physical vacuum;
9. the \(L=3\) cycle derivative equals the cycle-sum operator;
10. \(U^3=I\);
11. the \(L=5\) cycle derivative equals the cycle-sum operator;
12. \(U^5=I\);
13. the \(L=3\) two-Role plaquette derivative equals the closedness obstruction;
14. the two flat Role shifts commute;
15. the \(L=2\) centered scalar skew derivative is zero;
16. the \(L=2\) exact positive period \(U^2=I\) survives;
17. the rational boost moves the flat raw perturbation under the full-solder frame rule;
18. its A-row values are exactly \(2/3,4/3\);
19. a constant pure-linear affine gauge keeps the zero affine shift equal to zero.

These controls were exact Fraction arithmetic; no floating-point tolerance was used.

In addition, the hostile controls already Lean-owned by the merged stack cover:

- all five Fock degrees;
- parity preservation of the exterior/first-jet channels;
- \(L=2\) raw Nyquist visibility;
- \(L=3\) mixed corner support;
- \(L=3\) curl witnesses;
- \(L=5\) harmonic/cycle witnesses;
- scalar cycle and plaquette integrability at \(L\ge3\);
- exact rational observer/frame covariance for Channel L;
- located shifted-anchor behavior.

---

## 19. Theorem-ready handoff

The following statements are suitable for subsequent formalization. They are research statements here; this EXP does not claim new Lean ownership.

### Theorem A — nilpotent affine representation

For \(P_0=|0\rangle\langle0|\) and
\[
T_b=I+C^\dagger(b)P_0,
\]
the map
\[
R_{\rm nil}(L,b)=T_b\rho(L)
\]
is an exact representation of the affine semidirect product:
\[
R_{\rm nil}(L,b)R_{\rm nil}(M,c)
=
R_{\rm nil}(LM,b+Lc).
\]

### Theorem B — exact site-aware L+B weighted shift

The global weighted shift
\[
\mathscr L_r^{\rm nil}(A)
=
M_{x\mapsto R_{\rm nil}(A(x,r))}U_r
\]
is invertible, has source/target corners
\[
P_x\mathscr L_r^{\rm nil}P_{x+r},
\]
and its labelled products reproduce the full affine path law under \(R_{\rm nil}\).

### Theorem C — exact linear reduction

If every affine shift on the word is zero, the site-corner product of \(\mathscr L^{\rm nil}\) equals the PR #103 exterior lift of the linear PR #70 path.

### Theorem D — genuine affine-shift witness

At \(L=3\), \(R_{\rm nil}(I,e_A)\) sends the vacuum to
\[
|0\rangle+|A\rangle
\]
and hence distinguishes \((I,e_A)\) from the identity on the physical carrier.

### Theorem E — grading incompatibility with the pure-gauge chart

For \(b\ne0\), \(T_b\) is degree/parity mixing, whereas the PR #101 pure-gauge letter \(F_\varphi U_tF_\varphi^{-1}\) is degree preserving. Therefore the nilpotent affine response cannot itself be the required B/E-integrated letter on the joint pure-gauge orbit.

### Theorem F — exact E-channel assembly seed

The independently defined flux energy has Riesz operator
\[
W_{\rm flux}(e)=I+H(e),
\]
so
\[
W_{\rm flux}(0)=I,\qquad
D_eW_{\rm flux}(0)[e]=H(e)
\]
for arbitrary raw coframe \(e\), including the landed Nyquist/corner controls.

### Theorem G — finite cycle relation differentiates to PR #108

For any descended finite letter with the owned scalar flat tangent, differentiation of the exact length-\(L\) period gives
\[
-\frac1L\sum_a
M_{\sum_kU_t^ke_t{}^a}D_a=0.
\]
For \(L\ge3\), the merged separation theorem is exactly the zero-cycle-sum condition.

### Theorem H — finite plaquette relation differentiates to PR #108

Differentiation of
\[
\Pi(x;[s,t])=\Pi(x;[t,s])
\]
at flat gives
\[
-\frac1L\sum_a
M_{(U_s-I)e_t{}^a-(U_t-I)e_s{}^a}D_a=0.
\]
For \(L\ge3\), the merged separation theorem is exactly the plaquette/closedness condition.

### Theorem I — \(L=2\) descent survives scalar degeneration

Although \(D_r=0\) at \(L=2\), labelled endpoint descent still forces
\[
\ell^+(x,r)\ell^+(x+r,r)=I.
\]

### Theorem J — naïve B/E subtraction is not frame covariant

Under the merged full-solder frame rule, the flat raw perturbation becomes
\[
e'=\eta\Lambda-\eta.
\]
For the rational A/B boost its A-row is nonzero, while the zero affine shift remains zero under constant pure-linear node-gauge conjugation. Hence \(b-e_r\) cannot define the required frame-covariant mismatch.

### Theorem K — earliest coupling boundary

A common finite elementary letter that is simultaneously:

- affine-shift sensitive off the joint orbit;
- exactly PR #101 on the joint pure-gauge orbit;
- compatible with the complete raw E first jet;
- frame covariant;

requires an edge comparison that relates affine translation data to full solder/coframe data without setting \(A=A(e)\).

This is the solder–Cartan compatibility primitive identified by the terminal.

---

## 20. Exactly one recommended next step

Construct and formalize one **solder–Cartan edge mismatch**
\[
\boxed{
\kappa_N(A,e;x,r)\in V_x
}
\]
before any further matter-link or constitutive selector search.

It should satisfy all of the following as one object:

\[
\kappa_N(A_{\rm flat},0;x,r)=0,
\]

\[
\kappa_N(A_\varphi,d_f\varphi;x,r)=0
\]
on the exact joint pure-gauge orbit,

\[
\kappa_N((I,b),0;x,r)\ne0
\]
for a nonzero pure affine shift,

and the exact target-fibre frame law
\[
\kappa_N(A^h,e^h;x,r)
=
h_x^{\rm lin}\kappa_N(A,e;x,r).
\]

Its flat first derivative must represent the relative normal direction to
\[
(\delta b,\delta e_t)=(h,h)
\]
without identifying \(A\) and \(e\) away from that orbit.

Once such a \(\kappa_N\) exists, feed it into the already explicit site-corner affine response and demand that the resulting single primal letter simultaneously specializes to PR #101, has the exact descended cycle/plaquette relations above, and transports the independently owned \(W_{\rm flux}\) first jet. Until \(\kappa_N\) exists, those requirements cannot be imposed on one common finite letter without inserting an unowned B/E identification by hand.
