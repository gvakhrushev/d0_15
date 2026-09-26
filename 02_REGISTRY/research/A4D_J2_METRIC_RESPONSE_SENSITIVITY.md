# A4D J² metric-response sensitivity

**Task:** `WRK-A4D-J2-METRIC-RESPONSE-SENSITIVITY`
**Class:** `WORKER`
**Research lane:** `EXP-A4D-J2-UNIFORM-COUPLED-NORMAL-RESCUE`
**Parent:** `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
**Inputs read:** `MEMO_A4D_STAR_DENSITY_LORENTZ_NONLINEAR_QUOTIENT.md` (density (4.1), quotient coordinates (10.1)–(10.3)); `MEMO_A4D_STAR_DENSITY_VARIATION_PRESSURE.md` (first variation (2.1)–(2.5)); `A4D_J2_NORMAL_COORDINATE_LOCALITY.md` and merged `MEMO_A4D_J2_SMOOTH_RESONANCE_CLOSURE.md` (the final factor `h^{-2}` in (6.4) and (7.2)). Equation (8.3) of that partial-closure memo is the raw comparison supplied here. Its normal-rescue hypothesis is not an input theorem.
**Certificate:** `02_REGISTRY/research/certificates/a4d_j2_metric_response_sensitivity_check.py`

## 0. Terminal

\[
\boxed{\texttt{J2-METRIC-RESPONSE-POLYNOMIAL-SENSITIVITY-CERTIFIED}}
\]

\[
\boxed{p_{m,\mathrm{raw}}=0,\qquad p'=2.}
\]

Both exponents are sharp on the chart below. This is a finite-stencil Lipschitz estimate. It does not produce a stationary sheet, an ultraviolet isolation theorem, or an Einstein equation.

## 1. Chart, response, and norm

**H-STAR-CHART.** Keep the naked star density

\[
\mathcal L_\star(S,x)
=
c\,\epsilon_S\,
G_2\bigl(B_{S^c}(e,x),\,\star C_S(x)\bigr),
\qquad
C_S=\mathfrak b\bigl(\mathcal R(P_S)\bigr),
\qquad
\mathcal R(P)=\tfrac12(P-P^{-1}).
\]

The connection coordinate is the dimensionless link logarithm: \(L_{x,r}=\exp(A_{x,r})\) with \(A_{x,r}\in\mathfrak{so}(1,3)\). The metric coordinate is the site Gram \(Q_x=\Theta_x\eta\Theta_x^T\), read through one analytic Gram section \(\Theta(Q)\) with \(\Theta(\eta)=I\) on a neighborhood of the standard solder. These are the quotient coordinates \((Q,K)\) of the nonlinear-quotient memo, with \(K\) the dressed link and \(A=\log K\) in the section gauge. No formula in this chart divides by \(h\).

The raw metric partial \(E_Q(Q,A)\) is the derivative of \(S_\star=\sum_{x,S}\mathcal L_\star\) with respect to \(Q\), at fixed link logarithms. Equation (2.5) of the variation-pressure memo splits that derivative from the connection Euler term. Only the coframe/Gram slot is retained here.

The normalized response is exactly \(h^{-2}E_Q\). The factor \(h^{-2}\) is applied once, after the dimensionless derivative, and is not inserted into the link, the plaquette, or the Gram section.

**H-DOMAIN.** Fix \(\rho>0\) small enough that the closed sup-norm neighborhood

\[
\mathcal U_\rho
=
\bigl\{
(Q,A):
\sup_x\|Q_x-\eta\|\le\rho,\;
\sup_{x,r}\|A_{x,r}\|\le\rho
\bigr\}
\]

has three uniform bounds, independent of the mesh \(h\) and of the period \(L\):

1. every Gram stays in a fixed compact subset of nondegenerate Lorentzian metrics, and \(\|D\Theta\|\), \(\|\Theta^{-1}\|\) stay bounded;
2. every matrix exponential, every plaquette product, and every inverse \(P^{-1}\) stays in a fixed compact subset of \(\mathrm{GL}(4)\);
3. the resulting pointwise Jacobian of \(\mathcal L_\star\) in \((Q,A)\) is bounded.

Such a \(\rho\) exists because \(\exp\), inversion on \(\mathrm{GL}(4)\), \(\mathcal R\), the wedge product, \(G_2\), and \(\star\) are analytic on that compact set, and a Gram section exists on a nondegenerate neighborhood of \(\eta\).

**H-NORM.** The declared sum norm of a lattice field is

\[
\|F\|_1=\sum_x\|F(x)\|,
\]

with one fixed fibre norm (Frobenius norm on the Gram and on \(\mathfrak{so}(1,3)\)). A unit Role shift is an isometry of \(\|\cdot\|_1\). The same exponent statement holds in the Wiener norm \(\|F\|_{W^0}=\sum_k\|\widehat F_k\|\), because a radius-one stencil is a fixed Banach-algebra operation on absolutely summable Fourier series and a unit shift is a unimodular multiplier. Lattice cardinality never enters that count.

## 2. Theorems

**T-RAW.** On \(\mathcal U_\rho\), for every mesh \(h>0\),

\[
\boxed{
\|E_Q(Q,A+\Delta A)-E_Q(Q,A)\|_1
\le
M(\rho)\,\|\Delta A\|_1.
}
\]

The admissible raw exponent is \(p_{m,\mathrm{raw}}=0\). The constant \(M(\rho)\) depends on the chart radius and on the fixed stencil, not on \(h\) or \(L\).

**T-NORM.** With the same constant,

\[
\boxed{
\|h^{-2}\bigl(E_Q(Q,A+\Delta A)-E_Q(Q,A)\bigr)\|_1
\le
M(\rho)\,h^{-2}\,\|\Delta A\|_1.
}
\]

The admissible normalized exponent is \(p'=2\).

**T-SHARP.** Neither exponent can be lowered. At standard solder and identity links, the derivative of \(E_Q\) along the \(0\)-\(1\) boost of the single link \(A_{x,0}\), contracted with the solder variation \(\delta v_2=e_2\), equals the rational number \(1\). The certificate records that entry.

**T-INFINITY.** If \(\|\Delta A_h\|_1=O(h^\infty)\), then

\[
\|h^{-2}\bigl(E_Q(Q_h,A_h+\Delta A_h)-E_Q(Q_h,A_h)\bigr)\|_1
=O(h^\infty),
\]

whenever the two connection arguments remain in \(\mathcal U_\rho\). A fixed polynomial loss does not destroy superalgebraic decay.

In the sheet notation of the coupled-rescue contract, \(K\) is this dimensionless link logarithm, so

\[
\|E_Q(Q_h,K_h)-E_Q(Q_h,K_h^{\mathrm{sm}})\|_1
\le
M(\rho)\,\|K_h-K_h^{\mathrm{sm}}\|_1
\]

and the normalized fields differ by at most \(M(\rho)\,h^{-2}\) times the same distance.

## 3. Proof of the bounds

The first variation (2.5) writes the metric slot as a sum over sites and Role faces of

\[
c\,\epsilon_S\,
G_2\bigl(DB_{S^c}[\delta Q],\,\star C_S(A)\bigr).
\]

Each face uses the solder at its base site and the four links of its based plaquette. That is a radius-one stencil: one output site depends on finitely many input sites, and one input link meets finitely many output sites. Both counts are absolute (at most six faces and four links on four Roles). They do not grow with \(L\).

On \(\mathcal U_\rho\) the chain

\[
A\mapsto\exp(A)\mapsto P\mapsto P^{-1}\mapsto\mathcal R(P)\mapsto C_S
\]

and the chain

\[
Q\mapsto\Theta(Q)\mapsto B_{S^c}
\]

have bounded derivatives. The chart Jacobians of the Gram section and of the exponential are among those derivatives, so they contribute only to \(M(\rho)\). No step divides by \(h\). The mean-value integral in the link-logarithm direction therefore yields T-RAW with

\[
p_{m,\mathrm{raw}}=0.
\]

Multiplying by the single reconstruction factor \(h^{-2}\) moves the exponent from \(0\) to \(2\). That is T-NORM. There is no other negative power to track.

## 4. Proof that the exponents are sharp

At \(A=0\) and \(Q=\eta\), formula (2.2) of the variation memo says \(D\mathcal R_I[\dot P]=\dot P\). For the ordered face \((0,1)\), the based plaquette begins with \(L_0(x)\). Differentiating only that link along the boost \(X\) with \(X_{01}=X_{10}=1\) produces plaquette velocity \(X\) at the base site. The complementary bivector of that face is \(e_2\wedge e_3\). Scaling the leg \(v_2\) by the variation \(e_2\) differentiates the bivector onto that same area element.

The owned pairing \(G_2(\,\cdot\,,\star\,\cdot\,)\) on this pair of bivectors, times the face orientation, equals \(1\). The other two faces that contain the varied link have complementary pairs which do not meet this solder leg, so they contribute \(0\). The certificate evaluates the sum and checks

\[
\boxed{D_A E_Q(\text{boost}_{01})[\delta v_2]=1.}
\]

Thus the operator norm of \(D_A E_Q\) at the flat point is at least \(1\). Along that ray the raw difference quotient tends to \(1\), not to \(0\). If \(p_{m,\mathrm{raw}}<0\), then \(h^{-p_{m,\mathrm{raw}}}\to 0\) as \(h\to 0\), and no \(h\)-independent constant dominates the difference quotient. The raw exponent \(0\) is sharp.

The normalized difference quotient tends to \(h^{-2}\). If \(p'<2\), then \(h^{-p'}/h^{-2}=h^{2-p'}\to 0\), so \(p'\) is not an upper exponent on the whole range of small \(h\). The normalized exponent \(2\) is sharp.

The certificate also checks the pure power identity \(h^{-2}h^{12}=h^{10}\) at the reciprocals \(h=1/2,1/4,1/8\), and checks \(h^{10}<h\) there.

## 5. Super-algebraic corollary

Let \(\|\Delta A_h\|_1\le C_N h^N\) for every \(N\), with the two fields inside \(\mathcal U_\rho\). T-NORM gives

\[
\|h^{-2}\Delta E_Q\|_1
\le
M(\rho)\,C_N\,h^{N-2}.
\]

For a requested decay \(h^K\), choose \(N=K+2\). The right-hand side is \(O(h^K)\). Since \(K\) is arbitrary, the normalized metric-response difference is \(O(h^\infty)\).

The same substitution with any larger fixed loss \(h^{-p}\), \(p\) independent of \(h\), only changes the choice to \(N=K+p\). Polynomial loss is absorbed. The corollary does not require the sheet to be unique, and it does not assert that an exact sheet exists.

## 6. Negative control

Replace \(M(\rho)\) by a hidden constant \(C(N)=\exp(N)\) and set \(N=1/h\) in the integer model used by the certificate. The connection error \(\|\Delta A\|_1=\exp(-N)\) is \(O(h^\infty)\), because it decays faster than every positive power of \(h\). The product is

\[
\exp(N)\exp(-N)=1,
\]

which the certificate checks at \(N=2,4,8\). That remainder is not \(O(h)\). An \(L\)-dependent constant that is not bounded by a fixed power of \(L\) does not turn connection rescue into metric-response rescue. The sum norm of §1 is used precisely so that the proved constant is not of this kind: the stencil degree is absolute.

## 7. What this does not say

- No exact stationary sheet is constructed, and no normal-form rescue inequality is proved.
- Ultraviolet isolation, chart locality of the infrared jet, and the Einstein identification stay in their own lanes.
- The estimate is local to \(\mathcal U_\rho\). It is not uniform down to degenerate solder or out to unbounded link logarithms.
- A physical flat modulus still has to be checked inside the rescue lane if it moves the metric response by more than \(O(h^\infty)\). Vanishing of that tangential difference is not a corollary of T-RAW alone.
- #202 is not edited. No filter and no new invariant is added.
