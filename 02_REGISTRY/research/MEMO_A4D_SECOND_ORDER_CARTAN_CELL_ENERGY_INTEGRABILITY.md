# A4D second-order Cartan and cell-energy integrability

**Research snapshot:** fetched `origin/main = 750ac39236aedd5a3b120f9251ab1bb10f8d637f` on 2026-09-24. PR #69 and PR #70 are merged and used as frozen input.  
**Task:** `EXP-A4D-SECOND-ORDER-CARTAN-CELL-ENERGY-INTEGRABILITY`.  
**Status:** research proofs and exact rational controls; no new Lean owner or task-state change.

## 0. Result and scope of the terminal

The terminal verdict is **FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED**. The affine background gauge exists exactly, including the orbit \(e(t)=t\,d_f\xi\). What is not owned is its action on graded archive matter. The energy Ward identity fixes only the **symmetric** part of that matter action's second jet \(K\), and that part depends on the proposed cell energy. The affine background group by itself does not choose \(K\), hence it does not select \(c=1\) versus \(c=2\).

Two sharper conditional results make this statement useful:

1. A **background-independent differentiable representation** of the owned additive node translations cannot have the prescribed scalar Cartan tangent \(G_\xi=M_\xi D\) for every \(\xi\). The group is abelian, but \([G_{\delta_0},G_{\delta_1}]_{00}=-L^2/4\ne0\). Even for the single delta one-parameter subgroup, representation composition forces \(K=G^2=0\), inconsistent with both displayed energies (and with \(c=0\)).
2. Any finite scalar matter lift that **preserves constants** exactly rejects both displayed \(c=1,2\) energies along the owned pure-gauge orbit, without choosing an antisymmetric part of \(K\) or assuming uniform stencil radius. It forces \(c=0\) within the specific diagonal \(cM_{h^2}\) ansatz, but does not establish a complete covariant action for \(c=0\).

These are not an unconditional no-go for a *background-dependent gauge-groupoid cocycle*: such a cocycle can have \(K=G^2+\partial_e g_\xi[h]\). An explicit nonlocal, energy-engineered scalar countermodel below accommodates either \(c\); it demonstrates the logical gap, **not** a physical matter lift or a proposed selector. A frame-covariant soldered-creator law remains a separate physical gate. No result here identifies Cartan gauge with a local Lorentz boost.

## 1. Audited owners and typed boundaries

| Owner on the audited main | Frozen mathematical input | What it does not provide |
|---|---|---|
| `ArchiveAffineCartanConnection.lean`, PR #70 | Affine maps \((F,b)\), node gauge \(A_{xy}\mapsto h_x A_{xy}h_y^{-1}\), word transport, curvature and open torsion; `affineTranslation_flat_eq_forwardGaugeCoframe` | Representation of the same node gauge on archive cochain amplitudes/Fock states |
| `ArchiveFiniteCartanLieClosureNoGo.lean`, PR #70 | Scalar edge Lie closure, `no_uniform_radius_lie_closed`, zero derivations of a finite pointwise site algebra, rational local gates that fix constants | A homomorphism from the **abelian affine translation subgroup** to those noncommuting gates with tangent \(G_\xi\) |
| `ArchivePathWordAlgebra.lean`, PR #70 | Crossed product, path evaluation and distinction between factorized-local circuit cost and compressed stencil support | Action of affine translations on the matter carrier or an energy law |
| `A4DStaggeredHodgeSelector.lean` and `A4DConstitutiveKernelClassification.lean`, PR #69 | Radius-one Ward-null class dimension 24, Role-invariant subspace dimension 1, polynomial first-jet nonselection, density candidate | Neither the displayed full cell-energy \(Q_c(e)\) nor its gauge-covariant second jet is a Lean-owned physical action |
| `ArchiveMovingDifferential.lean`, `ArchivePrimalDualMovingAction.lean`, `A4DPathWordParentWard.lean` | Moving \(d\), pairing-forced inverse-transpose dual action, conditional mixed-parent transformation and first-order Ward | Actual constitutive \(S(e,U)\) or independently derived second-order matter lift |
| Earlier geometric-dual and located-star research memos | Cell-additive reference \(E_{\rm flux}\), both \(q_S\) models, Nyquist/corner controls, typed \(J\) and a scoped reverse-locality no-go | Physical Lorentz/observer star, or an energy selection theorem |

The active flux-energy worker branch was not treated as a merged Lean theorem on this snapshot. The three starred objects stay separate: the two-color topological placement \(J\), a Lorentz/observer metric star, and the scoped scalar reverse-locality inverse. None determines \(K\) here.

## 2. Exact covariance and two-jet calculus

Let \(W(0)=I\), \(Q(0)=I\), and use the convention that \(Q\) acts on matter fields, so invariance of the **same** quadratic energy reads

\[
W(e(t))=Q(t)^{-T}W(0)Q(t)^{-1}.
\tag{2.1}
\]

Set \(e(t)=t h+t^2 a/2+O(t^3)\), \(Q(t)=I+tG+t^2K/2+O(t^3)\), and \(DW_0[h]=H(h)=-(G^T+G)\). Direct multiplication gives

\[
Q^{-1}=I-tG+\tfrac{t^2}{2}(2G^2-K)+O(t^3),
\quad
Q^{-T}=I-tG^T+\tfrac{t^2}{2}(2(G^T)^2-K^T)+O(t^3).
\]

The chain rule on the background side and congruence on the matter side give the exact identity

\[
\boxed{
H(a)+D^2W_0[h,h]
=2(G^T)^2+2G^TG+2G^2-(K^T+K).
}
\tag{2.2}
\]

For \(Q(t)=\exp(tG)\), \(K=G^2\), reducing the right side to
\((G^T)^2+2G^TG+G^2\). This specialization is a test of that *particular* finite action; it is not permission to delete \(K\) for an arbitrary gauge-groupoid lift. The PR #70 pure translation of the flat identity-linear affine background gives **exactly** \(h=d_f\xi\), \(a=0\). An arbitrary \(a\) is retained below as a hostile calculus check.

More generally, if a nonidentity flat form \(B_0\) is used in (2.1), its second derivative is
\[
2(G^T)^2B_0+2G^TB_0G+2B_0G^2-K^TB_0-B_0K.
\]
For a fixed perfect primal/dual pairing \(J:P\to D^*\), the dual action is the pairing-forced inverse transpose in \(J\)-coordinates:
\[
R(t)=I-tG^T+\tfrac{t^2}{2}\bigl(2(G^T)^2-K^T\bigr)+O(t^3).
\tag{2.3}
\]
This relation does not make \(J\) a metric selector. If a geometric pairing itself depends on the background, its own \(J'\) and \(J''\) must also be included.

The constitutive map \(S(t)=R(t)S_0Q(t)^{-1}\) has
\[
\begin{split}
S'&=H_D S_0-S_0G_P,\\
S''&=K_D S_0-2H_D S_0G_P+S_0(2G_P^2-K_P),
\end{split}
\tag{2.4}
\]
where \(R=I+tH_D+t^2K_D/2+\cdots\). These are typed primal-to-dual formulas; no physical construction of \(S(e,U)\) is inferred.

## 3. Full scalar delta witness, not just three diagonals

On one embedded Role cycle let \(L\ge3\), \(Uf(x)=f(x+1)\), \(D=L(U-U^{-1})/2\), \(\Delta=L(U-I)\), \(\xi=\delta_0\), \(h=\Delta\xi\) and \(G=M_\xi D\). Put \(p=L/2\) and order the three occupied site labels as \(0,+1,-1\). The rest of the \(L\)-site matrix is zero in the displayed blocks:

\[
h_0=-L,\quad h_{+}=0,\quad h_{-}=L,\quad
G=
\begin{pmatrix}0&p&-p\\0&0&0\\0&0&0\end{pmatrix},
\quad G^2=(G^T)^2=0,
\]
\[
G^TG=
\begin{pmatrix}
0&0&0\\
0&p^2&-p^2\\
0&-p^2&p^2
\end{pmatrix}.
\tag{3.1}
\]

For arbitrary second background acceleration \(a\),
\(H_0(a)=\bigl(M_aU+U^{-1}M_a\bigr)/2\) has **zero diagonal** at every \(L\ge3\). It may change the off-diagonal equations; the actually owned orbit has \(a=0\).

For the specified two reference models, \(W_c(th)=I+tH(h)+ct^2M_{h^2}\) exactly in this scalar sector, \(c=1,2\); hence \(D^2W_c[h,h]=2cM_{h^2}\). Let \(K_{\rm sym}=(K+K^T)/2\). Equation (2.2) classifies **all** compatible second jets:
\[
\boxed{
K_{\rm sym}=G^TG-cM_{h^2}-\tfrac12H_0(a),\quad
K=K_{\rm sym}+A,\quad A^T=-A.
}
\tag{3.2}
\]
The antisymmetric \(A\) is invisible to this quadratic Ward, although composition, locality and moving \(d\) may constrain it. On the owned \(a=0\) orbit, the complete nonzero \(3\times3\) block is
\[
K_{\rm sym}=
\begin{pmatrix}
-cL^2&0&0\\
0&L^2/4&-L^2/4\\
0&-L^2/4&L^2(1/4-c)
\end{pmatrix}.
\tag{3.3}
\]
Thus \(K_{++}=L^2/4\), \(K_{00}=-cL^2\), \(K_{--}=L^2(1/4-c)\) and, additionally,
\[
K_{+,-}+K_{-,+}=-L^2/2.
\tag{3.4}
\]
At \(L=3\), the two endpoints \(+1,-1\) are adjacent on the cycle; at \(L\ge5\) they have graph distance two. The latter is support information for \(K\), not a reclassification of the cell support of \(W_c\). For \(L=5,c=1\), the three forced diagonals are \(25/4,-25,-75/4\), while the symmetric mixed entries are both \(-25/4\). The worker's \(25/4\) is precisely the \(L^2/4\) specialization.

If \(K=0\) or \(K=G^2=0\), the right side of (2.2) at \(a=0\) is \(2G^TG\). Its \(+\) diagonal equals \(L^2/2\), whereas \(2cM_{h^2}\) has zero \(+\) diagonal for **all \(c\)**. It also has a nonzero \((+,-)\) entry \(-L^2/2\), where \(M_{h^2}\) is zero. An arbitrary \(a\) cannot change the diagonal contradiction; at \(L\ge5\) it cannot repair the distance-two entry through radius-one \(H_0(a)\) either.

The non-delta control \(\xi=\delta_0+2\delta_1\) at \(L=3,5,7\) has \(G^2\ne0\); the generic formula is
\[
K_{\rm sym}=(G^T)^2+G^TG+G^2-cM_{h^2}-\tfrac12H_0(a).
\tag{3.5}
\]
It is not legitimate to generalize \(G^2=0\) from the delta witness to an arbitrary Cartan field.

## 4. Constant preservation rejects the displayed positive coefficients

The accepted scalar tangent obeys \(G_\xi\mathbf1=0\). PR #70's scalar local gates also fix \(\mathbf1\) **at finite parameter**. Assume the candidate matter lift shares this natural scalar-cochain property:
\[
Q(t)\mathbf1=\mathbf1\quad\hbox{for every small }t.
\tag{4.1}
\]
Then \(K\mathbf1=0\) and \(Q(t)^{-1}\mathbf1=\mathbf1\). By exact covariance (2.1),
\[
\langle\mathbf1,W(e(t))\mathbf1\rangle
=\|Q(t)^{-1}\mathbf1\|^2=\|\mathbf1\|^2.
\tag{4.2}
\]
On the owned pure-gauge orbit \(e(t)=th\), \(\sum_xh_x=0\), so the flux part has zero constant-vector expectation at first order. The reference models give instead
\[
\langle\mathbf1,W_c(th)\mathbf1\rangle
=L+ct^2\sum_xh_x^2
=L+2cL^2t^2
\tag{4.3}
\]
for the delta witness. Therefore \(c=1\) and \(c=2\) **both fail** under (4.1), at every \(L\ge3\). Equivalently,
\(\mathbf1^TK_{\rm sym}\mathbf1=-c\sum h^2\), which cannot vanish for \(c\ne0\) if \(K\mathbf1=0\).

This is not merely a delta accident. On any nonconstant one-dimensional \(\xi\), \(h=\Delta\xi\ne0\), \(G_\xi\mathbf1=0\), and (3.5) implies
\[
\mathbf1^TK_{\rm sym}\mathbf1=-c\|h\|^2;
\tag{4.4}
\]
the \(G^2\), \((G^T)^2\) and \(G^TG\) contributions have zero contraction with two constant vectors. Thus within this diagonal \(c\,e^2\) ansatz, constant preservation forces \(c=0\). It does **not** prove that \(W_0=I+H\) is a globally positive, frame-covariant or groupoid-integrable physical energy; the strong finite representation test below also rejects \(c=0\).

If a future scalar matter field is a nontrivial density whose finite gauge action does *not* fix constants, (4.1) must be removed explicitly. Its \(K\mathbf1\) is then a new second-order density datum; the existing first derivative \(G\mathbf1=0\) does not supply it.

## 5. What PR #70's affine gauge does and does not lift

The affine node group acts on **internal affine fibers** by \((F,b):z\mapsto Fz+b\). Its pure translations \(b_x=-L\xi(x)\) have pointwise additive composition. For the flat identity-linear connection their transformed link shift is exactly \(d_f\xi\), with no hidden \(t^2\) background term. The linear part has the ordinary exterior lift on fiber forms and creators. The **translation part has identity linear differential** on each internal fiber, so that exterior lift alone has zero scalar Cartan site tangent; it cannot become \(M_\xi D\) without an additional rule relating affine displacements, incidence, sites and matter amplitudes.

A smooth action of pure translations by permutations/pointwise-algebra automorphisms of the finite site set is also unavailable: the finite permutation group is discrete and PR #70 owns the stronger algebraic statement that a pointwise derivation of the finite scalar function algebra vanishes. This does **not** forbid general linear actions on cochains. PR #70's invertible local gates are such linear actions; they fix constants but obey the individual gate parameter law \(s\oplus t=s+t-st\), and gates for different edges need not commute. They are not automatically a representation of the abelian node-translation group. A product of local gates may be factorized-local even when its compressed matrix has long support; `no_uniform_radius_lie_closed` is frozen, not recomputed.

**Background-independent representation test.** If \(Q(\xi)\) is a differentiable representation of the additive pure-translation subgroup, \(Q(t\xi)=\exp(tG_\xi)\) and \(K_\xi=G_\xi^2\). For the whole group, its differential must satisfy \([G_\xi,G_\zeta]=0\). But the exact scalar matrices give
\[
[G_{\delta_0},G_{\delta_1}]_{0,0}=-L^2/4\ne0
\quad(L\ge3).
\tag{5.1}
\]
Thus no such representation has the stipulated tangent for all parameters, regardless of the energy or stencil radius. Even restricting to the one-parameter delta subgroup gives the second-order contradiction of Section 3 for every \(c\), including \(c=0\). This is a scoped representation no-go, **not** a no-go for a background-dependent action-groupoid cocycle.

**Background-dependent composition.** Let \(R(\xi;e)\) be a matter map for background \(e\), with \(e\mapsto e+h_\xi\), \(h_\xi=d_f\xi\). A genuine action-groupoid law is
\[
R(\zeta;e+h_\xi)R(\xi;e)=R(\xi+\zeta;e).
\tag{5.2}
\]
Put \(g_\xi(e)=\partial_tR(t\xi;e)|_{t=0}\). Differentiating (5.2) along one parameter gives
\[
K_\xi=G_\xi^2+\bigl(D_e g_\xi\bigr)_0[h_\xi].
\tag{5.3}
\]
The mixed parameter law is
\[
\bigl(D_e g_\zeta\bigr)_0[h_\xi]
-\bigl(D_e g_\xi\bigr)_0[h_\zeta]
+[G_\zeta,G_\xi]=0.
\tag{5.4}
\]
This is the exact way a nonzero commutator (5.1) **can** be canceled: a moving/background-dependent generator. The affine link law defines \(h_\xi\), but does not define \(g_\xi(e)\), its derivative or the mixed cocycle. For the delta family (3.2), only the symmetric part of \(D_eg_\xi[h_\xi]\) is fixed by a chosen energy; neither this derivative nor the antisymmetric part follows from PR #70.

For contrast, if \(Q(\xi)\) were background independent and smooth, its mixed second derivative \(B(\xi,\zeta)\) under additive composition would obey
\(B(\xi,\zeta)=G_\xi G_\zeta=G_\zeta G_\xi\). Equation (5.1) rules this out. It would be wrong to use this relation for the action groupoid, where the extra derivatives in (5.4) are essential.

**Hostile nonselection countermodel, not a candidate matter lift.** On a single finite cycle restrict to small pure-gauge edge fields \(e\in\operatorname{im}\Delta\), where the positive reference \(W_c(e)\) is invertible. Write \(\xi=\xi_0+\bar\xi\mathbf1\), with \(\sum_x\xi_{0,x}=0\), and let \(s(e)\) be the unique mean-zero vector with \(\Delta s(e)=e\). Define
\[
\begin{split}
A(e)&=\tfrac12\bigl(G_{s(e)}-G_{s(e)}^T\bigr),\\
F_c(e)&=W_c(e)^{-1/2}\exp A(e),\qquad
\rho(u)=\exp(uD),\\
R_c(\xi;e)&=F_c(e+\Delta\xi)\,\rho(\bar\xi)\,F_c(e)^{-1}.
\end{split}
\tag{5.5}
\]
Because \(\rho\) is orthogonal and additive, (5.5) obeys the **exact** composition law (5.2) and the exact congruence covariance of \(W_c\). Its flat tangent is \(G_\xi\): \(F_c'(0)[\Delta\xi]=G_{\xi_0}\), while \(\rho'(0)[\bar\xi]=G_{\bar\xi}\). The formula works for \(c=1\) and \(c=2\) near flat. It uses the proposed energy to define the lift, a global inverse of \(\Delta\), a matrix square root and generally dense matrices; it need not fix constants. Therefore it is expressly **inadmissible as an independently derived local physical lift**. It proves only that the affine group law plus the first derivative alone cannot yield an unconditional rejection of both models.

The actual selection task is to construct \(g_\xi(e)\) from affine links, oriented incidence, transported creators and legitimate path words **before** inserting \(W_c\). Its \(D_e g_\xi[h]\) and (5.4), combined with (2.2), would then decide \(c\). At the audited baseline that construction is not owned.

## 6. Which Hessian freedom is symmetry data, and which is constitutive?

Equation (2.2) sees the combination \(D^2W_0[h,h]+K^T+K\) on a gauge direction \(h=d_f\xi\). Before \(K\) is specified independently, changing the energy Hessian can be offset by changing \(K_{\rm sym}\), as (3.2) shows; \(K_{\rm skew}\) is wholly invisible to the quadratic energy. Constants preservation and finite composition give further tests but do not manufacture \(K\).

Even after a genuine \(K\) has fixed \(D^2W\) on **all pure-gauge directions**, the full coframe Hessian is not thereby determined. On \(X=(\mathbb Z/L\mathbb Z)^4\), uncentered \(e_r{}^a(x)\) has real dimension \(16L^4\); \(d_f:\xi^a(x)\mapsto e_r{}^a(x)\) has kernel the four constant internal vectors, hence image dimension \(4(L^4-1)\) and codimension \(12L^4+4\). Polarization of the Ward tests the Hessian on \(\operatorname{im}d_f\times\operatorname{im}d_f\), not on transverse arguments.

A finite local transverse witness is the squared plaquette curl of the uncentered coframe,
\[
z_{rs}^a(x;e)=\bigl(\Delta_r e_s{}^a(x)-\Delta_s e_r{}^a(x)\bigr)^2.
\tag{6.1}
\]
It vanishes on \(e=d_f\xi\) because forward differences commute, including period two with oriented slots retained. On a translation-only affine connection, the unsquared curl is exactly invariant under \(e\mapsto e+d_f\xi\). A local term supported on the corresponding square and proportional to \(z_{rs}^a\) can change transverse second-order cell coefficients while escaping *every* pure-gauge two-jet test. Multiplying an independently covariant cell action by a frame-invariant scalar \(1+\lambda z_c\) with \(z_c(0)=Dz_c(0)=0\) is a conditional deformation that preserves its covariance. Formula (6.1) alone does not establish a Lorentz-covariant full action or license a new stress claim. It locates genuinely constitutive freedom that a pure-gauge Ward cannot measure.

## 7. Second-order Ward with moving differentials

For grade-dependent \(Q_k(t)=I+tG_k+t^2K_k/2+\cdots\), the **moved** primal differential is \(d_k(t)=Q_{k+1}(t)d_kQ_k(t)^{-1}\). Its first and second derivatives are
\[
\begin{split}
d_k'&=G_{k+1}d_k-d_kG_k,\\
d_k''&=K_{k+1}d_k-2G_{k+1}d_kG_k
       +2d_kG_k^2-d_kK_k.
\end{split}
\tag{7.1}
\]
The same applies to independently typed dual \(d_D\) with its pairing-forced dual action. In particular \(d''\) need not vanish when the first-order expression has been accepted. It is the second-order completion of the quadratic remainder explicitly retained by `movingDifferential_infinitesimal`.

For the mixed parent operator \(C(t)=d_D(t)S_1(t)d_P(t)\), with all compositions typed, the product rule is
\[
\begin{split}
C''={}&d_D''S_1d_P+d_D S_1''d_P+d_D S_1d_P''\\
&+2d_D'S_1'd_P+2d_D'S_1d_P'+2d_D S_1'd_P'.
\end{split}
\tag{7.2}
\]
If a background-dependent perfect pairing moves, its derivatives enter the mixed action as well. Equations (2.4), (7.1) and (7.2), together with the first-order six-term Ward, are the exact algebraic handoff; they are conditional on the still-missing constituent \(g_\xi(e)\) and \(S(e,U)\). Treat the connection Euler term as independent. No sourced stress Ward or Lorentz covariance follows from this scalar Cartan calculation.

## 8. Post-selector checks and the three-star firewall

The earlier **one-color scalar reverse-stencil** theorem rules out a uniformly bounded local inverse for a scalar neighboring first jet when both forward and reverse stencils must remain uniformly local across all \(L\). That scoped result neither changes the two-color placement \(J\) nor proves an obstruction to the Lorentzian metric star or an inverse-free parent. It does not choose \(c\): its assumptions would exclude both reference \(W_c\) when interpreted as simultaneously local inverse stars.

An energy-weight-equals-specified-volume/minor law might impose a different Hessian, but it must be stated and derived on the full uncentered cell geometry. Incidence/Jacobi identities alone do not turn geometric volume into matter energy. The centered determinant density has zero first derivative and can supply another quadratic coefficient; along the Nyquist family it is blind, and its geometry support can exceed one cell. None of these post-selector laws is an owner of \(K\), and none resolves the local Lorentz/observer frame-lift gate. The finite Cartan gauge acts on affine internal fibers and coframe links, not on archive sites by \(x\mapsto\Lambda x\); simultaneous Role permutations form a third distinct action.

## 9. Direct answers

| No. | Question | Exact answer |
|---|---|---|
| 1 | Second-order covariance identity? | Equation (2.2), with the sign from \(Q^{-1}=I-tG+t^2(2G^2-K)/2\). |
| 2 | Required data beyond \(G\)? | Background acceleration \(a\), matter second jet \(K\), full \(D^2W\), and, for parent Ward, the jets of \(d_P,d_D,S\) and possibly the pairing. |
| 3 | Does \(e''(0)\) affect delta scalar diagonals? | No for \(L\ge3\), since \(\operatorname{diag}H_0(a)=0\). The PR #70 orbit has \(a=0\) exactly. |
| 4 | Forced \(K\)? | Complete symmetric matrix (3.2–3.3), mixed entry (3.4), arbitrary skew part until composition/locality is imposed. |
| 5 | Why exponential fails? | It sets \(K=G^2=0\) for delta; the \(+\) diagonal and mixed \((+,-)\) entries of \(2G^TG\) have no counterpart in \(2cM_{h^2}\), for any \(c\). |
| 6 | Does owned affine background action already induce the needed matter representation? | No. Its translation acts on internal affine fibers; the exterior linear lift does not produce \(M_\xi D\). A background-independent translation representation is ruled out by (5.1). |
| 7 | Does composition fix \(K\)? | Yes to \(G^2\) for a background-independent additive representation, which fails; for an action-groupoid cocycle it instead gives (5.3–5.4), with an unowned background derivative. |
| 8 | Does \(K\) select \(c=1,2\), another \(c\), or neither? | No independently fixed \(K\) is owned. A constants-preserving scalar lift rejects both and makes \(c=0\) necessary within this ansatz; the additive representation also rejects \(c=0\). Without those restrictions, (5.5) accommodates both and is not a selector. |
| 9 | Exact no-go if no finite action? | No background-independent representation of the owned *abelian* translation subgroup has all \(G_\xi\) as tangents; a finite background-dependent cocycle is not generally excluded. Under exact constants preservation, the two positive \(q\) actions cannot be gauge invariant. |
| 10 | Truly constitutive remainder? | Transverse Hessian components outside \(\operatorname{im}d_f\), and any gauge Hessian component after an independent \(K\) has been fixed; (6.1) is an explicit transverse witness. |
| 11 | Reverse-star selector after Cartan? | The scoped scalar two-sided local inverse condition rejects both if imposed; it does not choose one and is not a theorem about \(J\) or the physical metric star. |
| 12 | Energy-volume identity independent? | Yes. Even after a Cartan matter lift, an explicit local energy/density law is additional data unless derived from that lift and a physical action. |

### Secondary terminals

| Status | Result |
|---|---|
| SECOND-ORDER-COVARIANCE-IDENTITY | Exact (2.2); exponential is a strict specialization |
| SCALAR-DELTA-WITNESS-STATUS | Generic \(L\ge3\) full matrix (3.3), diagonals and mixed entry; \(L=3,5,7\) checked |
| EXPONENTIAL-CARTAN-STATUS | Fails for every constant \(c\) on the owned delta orbit |
| MATTER-TRANSFORMATION-SECOND-JET-STATUS | Not Lean-owned or determined by affine background alone; constants-preserving class rejects \(c=1,2\) |
| BACKGROUND-ACCELERATION-STATUS | Owned \(a=0\); arbitrary \(a\) cannot change scalar diagonals |
| CELL-HESSIAN-STATUS | \(2cM_{h^2}\) for the two reference laws; pure-gauge Ward leaves transverse Hessian freedom |
| MOVING-D-SECOND-ORDER-STATUS | Equations (7.1–7.2) derived, not yet formalized as a physical action |
| REVERSE-STAR-POSTSELECTOR-STATUS | Two-sided local inverse no-go is scoped and rejects both, without selecting |
| ENERGY-VOLUME-POSTSELECTOR-STATUS | Independent constitutive identity, not owned |

## 10. Exact controls and reproducibility

The appended rational checker passes **162/162** assertions. It builds the matrices independently at \(L=3,5,7\) and checks first-order Ward signs, delta and non-delta \(\xi\), the generic full \(K_{\rm sym}\) equation for \(c=0,1,2\), arbitrary \(a\) diagonal and full acceleration equation, \(K=0\), \(K=G^2\), explicit commutator, constant-vector obstruction, a noncommuting generic congruence and the second-order moving-\(d\) product rule. The symbolic support, action-groupoid construction and transverse rank arguments are proofs in Sections 3, 5 and 6, not claims that a finite test proves them.

### Standalone checker

```python
"""Exact rational second-jet controls; supplements proofs in the terminal memo."""
from fractions import Fraction as F

checks=[]
def check(name, condition):
    assert condition, name
    checks.append(name)

def zero(n,m=None): return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def trans(a): return [list(r) for r in zip(*a)]
def add(a,b): return [[v+w for v,w in zip(r,s)] for r,s in zip(a,b)]
def scale(t,a): return [[t*v for v in row] for row in a]
def sub(a,b): return add(a,scale(-1,b))
def mul(a,b):
    out=zero(len(a),len(b[0]))
    for i,row in enumerate(a):
        for k,v in enumerate(row):
            if v:
                for j,w in enumerate(b[k]):out[i][j]+=v*w
    return out
def diag(v): return [[x if i==j else F(0) for j in range(len(v))] for i,x in enumerate(v)]
def vecmul(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def dot(v,w): return sum(x*y for x,y in zip(v,w))
def shift(L): return [[F(j==(i+1)%L) for j in range(L)] for i in range(L)]

for L in (3,5,7):
    U=shift(L);UT=trans(U); D=scale(F(L,2),sub(U,UT))
    Delta=scale(L,sub(U,eye(L)))
    ones=[F(1)]*L
    check(f'L{L}-D-skew',trans(D)==scale(-1,D))
    check(f'L{L}-D-kills-constants',vecmul(D,ones)==[0]*L)
    for tag,xi in (("delta",[F(i==0) for i in range(L)]),
                   ("nondelta",[F(i==0)+2*F(i==1) for i in range(L)])):
        h=vecmul(Delta,xi); G=mul(diag(xi),D)
        H=scale(F(1,2),add(mul(diag(h),U),mul(UT,diag(h))))
        G2=mul(G,G); GTG=mul(trans(G),G)
        base=add(add(mul(trans(G),trans(G)),GTG),G2)
        check(f'L{L}-{tag}-first-Ward',H==scale(-1,add(G,trans(G))))
        check(f'L{L}-{tag}-gauge-h-sum',sum(h)==0)
        check(f'L{L}-{tag}-G-kills-constants',vecmul(G,ones)==[0]*L)
        check(f'L{L}-{tag}-H-a-diagonal',all(H[i][i]==0 for i in range(L)))
        arbitrary_a=[F(i+1) for i in range(L)]
        Ha=scale(F(1,2),add(mul(diag(arbitrary_a),U),mul(UT,diag(arbitrary_a))))
        check(f'L{L}-{tag}-arbitrary-a-diagonal', all(Ha[i][i]==0 for i in range(L)))
        for c in (0,1,2):
            B=scale(2*c,diag([v*v for v in h]))
            Ksym=sub(base,scale(c,diag([v*v for v in h])))
            K=Ksym
            RHS=sub(scale(2,base),add(K,trans(K)))
            check(f'L{L}-{tag}-c{c}-full-second-jet',RHS==B)
            check(f'L{L}-{tag}-c{c}-constant-norm', dot(ones,vecmul(B,ones))==2*c*dot(h,h))
            check(f'L{L}-{tag}-c{c}-constant-preserve-obstruction',
                  dot(ones,vecmul(Ksym,ones)) == -c*dot(h,h))
            Ksym_acc=sub(Ksym,scale(F(1,2),Ha))
            check(f'L{L}-{tag}-c{c}-arbitrary-acceleration-full',
                  sub(scale(2,base),add(Ksym_acc,trans(Ksym_acc)))==add(Ha,B))
            expRHS=add(add(mul(trans(G),trans(G)),scale(2,GTG)),G2)
            check(f'L{L}-{tag}-c{c}-exp-fails',expRHS!=B)
        if tag=="delta":
            p=F(L,2); plus=1; minus=L-1
            check(f'L{L}-delta-h',h[0]==-L and h[minus]==L and all(h[i]==0 for i in range(1,L-1)))
            check(f'L{L}-delta-G-square',G2==zero(L) and mul(trans(G),trans(G))==zero(L))
            check(f'L{L}-delta-2GTG-diag',
                  2*GTG[plus][plus]==F(L*L,2) and
                  2*GTG[minus][minus]==F(L*L,2) and GTG[0][0]==0)
            check(f'L{L}-delta-mixed',GTG[plus][minus]==-F(L*L,4))
            check(f'L{L}-delta-zero-K-fails-all-c',
                  all(scale(2,GTG)!=scale(2*c,diag([v*v for v in h]))
                      for c in (0,1,2)))
            for c in (1,2):
                Ks=sub(GTG,scale(c,diag([v*v for v in h])))
                check(f'L{L}-delta-c{c}-forced-diagonals',
                      (Ks[plus][plus],Ks[0][0],Ks[minus][minus])==
                      (F(L*L,4),-c*L*L,F(L*L)*(F(1,4)-c)))
            # G_delta and G_delta1 cannot be tangents of one background-independent
            # representation of the abelian pure-translation subgroup.
            xi1=[F(i==1) for i in range(L)]
            G1=mul(diag(xi1),D)
            check(f'L{L}-noncommuting-additive-tangents',mul(G,G1)!=mul(G1,G))
            check(f'L{L}-commutator-explicit-entry',
                  sub(mul(G,G1),mul(G1,G))[0][0]==-F(L*L,4))
        else:
            check(f'L{L}-nondelta-G-square-nonzero',G2!=zero(L))

# General polynomial Q^-1 to order t^2 and three-factor congruence, using
# arbitrary noncommuting rational matrices (not just the delta witness).
G=[[F(0),F(2)],[-F(1),F(3)]]
K=[[F(1),F(4)],[F(5),F(-2)]]
R=scale(F(1,2),sub(scale(2,mul(G,G)),K))
check('inverse-t1',add(G,scale(-1,G))==zero(2))
check('inverse-t2',add(add(scale(F(1,2),K),R),scale(-1,mul(G,G)))==zero(2))
lhs2=add(add(scale(2,trans(R)),scale(2,R)),scale(2,mul(trans(G),G)))
rhs2=sub(add(add(scale(2,mul(trans(G),trans(G))),scale(2,mul(trans(G),G))),
             scale(2,mul(G,G))),add(trans(K),K))
check('general-congruence-t2',lhs2==rhs2)

# Moving differential d'=Q1 d Q0^-1; exact product rule to t^2.
G0=[[F(1),F(2)],[F(3),F(4)]]; K0=[[F(5),F(1)],[F(-1),F(2)]]
G1=[[F(-1),F(2),F(0)],[F(0),F(3),F(2)],[F(4),F(-2),F(1)]]
K1=[[F(2),F(3),F(1)],[F(4),F(5),F(0)],[F(-1),F(0),F(2)]]
d=[[F(1),F(0)],[F(2),F(1)],[F(3),F(4)]]
dt=sub(mul(G1,d),mul(d,G0))
dtt=sub(add(sub(mul(K1,d),scale(2,mul(mul(G1,d),G0))),
             scale(2,mul(d,mul(G0,G0)))),mul(d,K0))
check('moving-d-first',dt==sub(mul(G1,d),mul(d,G0)))
check('moving-d-second-product-rule',
      dtt==add(add(mul(K1,d),scale(2,mul(G1,mul(d,scale(-1,G0))))),
               mul(d,sub(scale(2,mul(G0,G0)),K0))))
check('moving-d-quadratic-not-frozen',dtt!=zero(3,2))

print(f'PASS {len(checks)}/{len(checks)} exact checks')
L=5
U=shift(L)
delta=[F(i==0) for i in range(L)]
G=mul(diag(delta),scale(F(L,2),sub(U,trans(U))))
h=vecmul(scale(L,sub(U,eye(L))),delta)
Ks=sub(mul(trans(G),G),diag([v*v for v in h]))
print('L=5 delta forced symmetric K c=1:', [[str(z) for z in row] for row in Ks])
```

## 11. Theorem-ready handoff, with dependency order

These are **proposed** Lean statements, not claims already formalized. Keep the PR #69/#70 modules frozen, use the existing finite cyclic model and rational coefficients for the scalar controls, and prove the purely algebraic statements before introducing a physical cell law.

1. **`A4DSecondOrderCartanCongruence`.** Define truncated two-jets over a commutative ring with `2` invertible, and show `invJet₂ (I+tG+t²K/2) = I-tG+t²(2G²-K)/2`. For a symmetric form `B₀` prove the full congruence coefficient in Section 2, including the `B₀`-weighted formula and its specialization (2.2). State the typed dual inverse-transpose jet and the constitutive product (2.4). No assumed exponential.
2. **`A4DScalarDeltaSecondJet`.** On `ZMod L` with `L ≥ 3` and `D=L(U-U⁻¹)/2`, prove `Gδ₀²=0`, the complete block (3.1), and `diag H₀(a)=0` for arbitrary `a`. Obtain (3.2–3.4) by entry equality for the two reference `c`. Include the off-diagonal distance-two entry when `L ≥ 5`, a direct `L=5` corollary, and a nondelta witness where `G² ≠ 0`. Derive the constant-vector contradiction for `c ≠ 0` under the explicit hypothesis `Q(t) 1=1`. Avoid adding a global positivity claim for `c=0`.
3. **`A4DAffineMatterLiftObstruction`.** From `ArchiveAffineCartanConnection.translationGauge` prove that pure translation changes the flat coframe exactly by `t d_f ξ` and its acceleration vanishes. Separately prove the matrix commutator entry (5.1). The representation no-go should quantify only over a *background-independent* group action whose finite two-jets obey the additive subgroup law and whose prescribed tangent is `MξD`. It must not quantify over background-dependent groupoid actions or equate an affine fiber translation with a site permutation.
4. **`A4DActionGroupoidSecondJet`.** Specify `R(ζ;e+d_f ξ) R(ξ;e)=R(ξ+ζ;e)` as an explicit hypothesis on a well-typed matter carrier. Derive (5.3–5.4). This declaration is the **missing primitive**: obtain its generator `gξ(e)` from affine links plus oriented path-word or solder data independently of `W_c`. The nonlocal construction (5.5) is an obstruction to a proof of universal no-go from group law and first jet alone, and must never be promoted to a candidate local law.
5. **`A4DMovingDifferentialSecondJet`.** Extend `movingDifferential_infinitesimal` with (7.1), the analogous pairing-forced dual jet, and (7.2). Place moving pairing terms in their own conditional statement. Keep connection Euler variation independent, as in the existing six-term Ward.
6. **`A4DCellHessianTransverseModulus`.** Prove the rank of `d_f` over finite periodic real cochains and the vanishing of the curl (6.1) on its image. Record a transverse-Hessian freedom statement conditional on a fully covariant cell density; do not infer a physically Lorentz-covariant deformation just from the scalar example.

The next research experiment is concrete: construct the background-dependent generator in item 4 without reading either proposed energy; compute its `D_e gξ[d_f ξ]` on the generic delta cycle and compare its **full** symmetric matrix, including the `(+,-)` entry, to (3.2). A match to exactly one model would change the terminal to selection; a contradiction for every independently derived local generator would justify a stronger no-go. The owned affine connection alone settles neither possibility.

**Terminal verdict: FINITE-CARTAN-SECOND-JET-PRIMITIVE-REQUIRED.**