# All-cap nonlinear matter response and exact null-background propagation

**Date:** 2026-10-21.  
**Parent result:** [complete-price nonvacuum stationary normal form](A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md).  
**Status:** analytic consequences of the displayed finite detector and complete-price formulas, with an explicitly conditional continuum kinetic dictionary. No fresh repository implementation replay is asserted.  
**Closure:** GR_closed = false.

This document was restored from the reviewed mathematical content after a workspace snapshot inconsistency. Its statements include the final corrections concerning the reduced geometry, retained spectator sources, and fixed measure.

## 1. Positive conclusions

The previous normal form derived a nonlinear kinetic response \(K_N\) from the actual fixed-cap price. This continuation proves:

1. In the original dimensionless detector coordinate \(Y\),
   \[
   \boxed{-128<\theta_N:=K_N''(0)/K_N'(0)<-3}
   \tag{1}
   \]
   for every finite \(N\ge1\), every \(\alpha>0\), \(0<\beta\le1\), and the consumed unit-charge premise \(\kappa>53\). The absolute coefficients change sign between cap one and higher caps, but their ratio keeps the same strict sign.
2. For the stated local continuum kinetic dictionary and physical sign \(Y=-\eta^2q\), the longitudinal matter principal metric on a nonzero aligned null background is Lorentzian, has the same determinant as the original background metric, and has its ray cone contained in that background cone. Orthogonal internal polarizations have the original principal cone.
3. With uniform coefficients and a Brinkmann background, the entire linearized matter equation with the **reduced geometry held** has an exact unitary intertwiner with the ordinary Brinkmann wave equation. This is a phase or translation for a fixed internal direction and an ordered matrix transport for rotating internal profiles.
4. If a separately supplied physical scaling has \(\eta\to0\), the resulting propagation returns to the ordinary Brinkmann propagation at an explicit cap-uniform \(O(\eta^2)\) rate for disturbances with one controlled longitudinal derivative.

The held geometry is the transformed coframe of the exact stationary normal form. Holding it is not equivalent to holding the original coframe under a matter perturbation; Section 5 gives the differential relation. Retained baseline and collar spectators must have no matter variation on the chosen patch for the stated full matter equation to apply. The conclusions do not prove the full coupled gravity-matter initial-value problem, the positivity of total physical energy, or an obligatory physical action and clock.

## 2. Exact normalized nonlinear coefficient

Use the literal detector and complete-price formulas of the parent theorem:
\[
\varphi=(1+\sqrt5)/2,\quad p=\varphi^{-1},\quad z=2^{-20},
\]
\[
L=4p^3=1-p^6,\quad A_0=L(1+p^6)=1-p^{12},
\quad Q=1-zL,\quad R=1-zA_0,\quad r_0=1-QR.
\tag{2}
\]
The detector is
\[
\begin{aligned}
\ell(E)&=4E(1-E),\\
B(y)&=4(p+p^2y)^2[1-(p+p^2y)^2],\\
A(x,y)&=\ell(p^2(1+x))+[1-\ell(p^2(1+x))]B(y),\\
r(x,y)&=1-[1-zB(y)][1-zA(x,y)].
\end{aligned}
\tag{3}
\]
All density derivatives below are at \((x,y)=(0,0)\). In particular,
\[
r_x=4zQp^{11}>0,\qquad r_y=8z(Rp^6+Qp^{12})>0,
\tag{4}
\]
and \(r_{xx},r_{xy},r_{yy}\) are strictly negative.

The fixed-cap price is
\[
V_N(r)=\alpha[\kappa-\beta h_\varphi(r)]E_N(\beta r),
\qquad E_N(t)=\sum_{j=0}^{N-1}t^j.
\tag{5}
\]
The parameters \(\alpha,\beta,\kappa\) are held in the density derivatives. Normalize \(F_N(x,y)=V_N(r(x,y))-V_N(r_0)\), carrying the subtracted value and its full internal derivative in the actual baseline.

The parent theorem gives
\[
b_N=K_N'(0)=V_N'(r_0)r_y\ne0,
\]
\[
K_N''(0)=F_{yy}+2\rho F_{xy}+\rho^2F_{xx},
\qquad \rho=r_y/r_x.
\tag{6}
\]
Since \(Dr\,(\rho,1)^T=2r_y\), it follows exactly that
\[
\boxed{\theta_N
=4r_y\frac{V_N''(r_0)}{V_N'(r_0)}-S_z,\qquad
S_z=-\frac{\rho^2r_{xx}+2\rho r_{xy}+r_{yy}}{r_y}.}
\tag{7}
\]
This separates the detector term from the logarithmic derivative of the outer valuation. The overall factor \(\alpha\) cancels. The response generally still depends on the actual \(\beta,\kappa,N\); numerical equality of all \(\theta_N\) is not asserted.

## 3. Exact golden detector term

Direct differentiation gives
\[
\begin{aligned}
r_{xx}/r_x&=-2/p,\\
r_{xy}/r_x&=-8-8zp^6/Q,\\
r_{yy}/r_y&=p^{-2}-6-\frac{16zp^{12}}{R+p^6Q},\\
\rho&=16+12p-\frac{8zp^4}{Q}.
\end{aligned}
\tag{8}
\]
Therefore
\[
\boxed{S_z=45+31\varphi-\frac{32zp^5}{Q}
+\frac{16zp^{12}}{R+p^6Q}.}
\tag{9}
\]
The constant part uses \(32/p+46-p^{-2}=45+31\varphi\); the correction uses \(p^6-p^3=-2p^5\). These are identities of the actual golden detector, with no Diophantine averaging premise.

Two coarse bounds suffice:
\[
\boxed{4<S_z<97.}
\tag{10}
\]
Indeed, \(\rho=2p^{-5}R/Q+2p>2p\), and the mixed and \(yy\) Hessian entries are negative, giving \(S_z>2\rho/p>4\). For the upper bound use \(p>3/5\), hence \(\varphi<5/3\), and \(R>1-z>1/2\). Dropping the negative correction in (9) gives \(S_z<45+31(5/3)+32z<97\).

Also \(p<2/3\) implies
\[
p^6+p^{12}<\frac{64}{729}+\frac{4096}{531441}<\frac1{10}.
\]
Since \(Q,R<1\), equation (4) yields
\[
\boxed{4r_y<\frac{16}{5}z.}
\tag{11}
\]

## 4. Uniform sign and magnitude for every fixed finite cap

Set \(d=1-2z\). The parent estimates give
\[
z<r_0<2z,\qquad 0<h_\varphi'(r_0)<40,\qquad 0<h_\varphi(r_0)<2.
\tag{12}
\]
Moreover \(\ln\varphi>2/5\): use \(\varphi>8/5\) and \(\ln t\ge2(t-1)/(t+1)\) for \(t\ge1\), whose difference has nonnegative derivative. Hence
\[
0<-h_\varphi''(r_0)
=\frac1{\ln\varphi\,r_0(1-r_0)}<\frac5{2zd}.
\tag{13}
\]

### 4.1 Caps \(N\ge2\)

Write
\[
t=\beta r_0,\quad A=\kappa-\beta h_\varphi(r_0)>51,\quad
M=A E_N'(t)-h_\varphi'(r_0)E_N(t).
\]
The earlier cap estimate gives \(M>10\). Also \(M>A/5\): since \(E_N<d^{-1}<51/50\) and \(E_N'\ge1\), we have \(h'E_N<40(51/50)<(4/5)A\). Derivatives of \(E_N\) are with respect to \(t\).

Exactly,
\[
\frac{V_N''}{V_N'}
=\frac{-h''E_N-2\beta h'E_N'+\beta A E_N''}{M}.
\tag{14}
\]
Using \(E_N<d^{-1}\), \(E_N''<2d^{-3}\), \(M>10\), and \(M>A/5\), and dropping the negative middle term,
\[
\frac{V_N''}{V_N'}<\frac1{4zd^2}+\frac{10}{d^3}.
\tag{15}
\]
Consequently,
\[
4r_y\frac{V_N''}{V_N'}
<\frac4{5d^2}+\frac{32z}{d^3}<1.
\tag{16}
\]
The last inequality is equivalent to \(1-182z+60z^2-40z^3>0\), immediate at \(z=2^{-20}<1/182\). With \(S_z>4\), this proves \(\theta_N<-3\).

For a lower bound, the first and last numerator terms in (14) are nonnegative. Since \(h'<40\), \(M>10\), \(\beta\le1\), and \(E_N'<d^{-2}\),
\[
\frac{V_N''}{V_N'}>-8d^{-2},\qquad
4r_y\frac{V_N''}{V_N'}>-\frac{128z}{5d^2}>-1.
\tag{17}
\]
The last inequality follows from \(d>1/2\) and \((512/5)z<1\). Thus \(\theta_N>-98\).

### 4.2 Cap one

For \(N=1\),
\[
V_1''/V_1'=h_\varphi''(r_0)/h_\varphi'(r_0)<0,
\]
so \(\theta_1<-4\). Also \(h_\varphi'(r_0)>1\), since \(r_0<1/4\) gives \((1-r_0)/r_0>3>\varphi\). Equations (11)--(13) imply
\[
4r_y V_1''/V_1'>-8/d>-16.
\]
Hence \(\theta_1>-113\). The common bound (1) follows.

This uniformity concerns the normalized response, without an infinite bank, an optimized cap envelope, or a cap-uniform auxiliary neighborhood. Since \(b_1<0\) and \(b_N>0\) for \(N\ge2\),
\[
K_1''(0)>0,\qquad K_N''(0)<0\quad(N\ge2).
\tag{18}
\]
Causal orientation depends on their ratio. The constants in (1) refer to \(Y\); if \(Y=cq\),
\[
\left.\frac{d^2K(cq)/dq^2}{dK(cq)/dq}\right|_{q=0}
=c\theta_N.
\tag{19}
\]
The sign and units of \(c\) must be retained.

## 5. Conditional kinetic dictionary and source domain

Assume the local continuum kinetic dictionary
\[
q=g^{\mu\nu}\sum_{A=1}^{m}\partial_\mu\psi_A\partial_\nu\psi_A,
\qquad Y=cq,\qquad c=\sigma\eta^2\ne0,
\tag{20}
\]
where \(g\) is the metric of the transformed coframe \(\widetilde e\), and the positive internal quadratic form has been orthonormally diagonalized. Complex components may be represented by real components with their actual normalization included in (20). The local price uses \(K_N(cq)\) in its original nonzero smooth measure. The transformed geometry and internal parameters are held. A correlated nonlocal \(K(Y_1,\ldots,Y_n)\) is not covered by this local differential statement.

For the full matter equation claim, additionally require that retained baseline and collar spectators have no matter variation supported on the patch. This holds when the baseline depends only on held parameters and the patch is buffered away from all collar matter stencils. Any spectator that does depend on the varied matter must retain its first and linearized sources. Without their cancellation or compatible form, the following equation and intertwiner concern the displayed kinetic part only.

There is a second essential source distinction. Even where the original and transformed coframes have equal values, the parent auxiliary section gives, at fixed internal parameters,
\[
\delta\pi=\left(F_{xx}\frac ba+F_{xy}\right)\delta Y,\qquad
\delta e_{\rm original}
=-\frac{\delta\pi}{2a}e_{\rm original}
\quad\text{when }\delta\widetilde e=0.
\tag{20a}
\]
Thus this independent matter variation in the reduced stationary description generally represents a mixed matter/conformal-coframe variation in the original carrier. This is not the operator obtained by freezing the original coframe, nor a solution of all linearized geometric and auxiliary equations. Those require the full source transport and remaining geometric rows.

## 6. Principal symbol and exact causal cone

On an aligned null background,
\[
\partial_\mu\psi_A=C_A\ell_\mu,\qquad
g^{\mu\nu}\ell_\mu\ell_\nu=0,
\tag{21}
\]
the density vanishes but its ambient differential need not. Dividing the linearized matter equation by its nonzero common kinetic coefficient yields the normalized principal symbol
\[
\mathsf P_{AB}^{\mu\nu}
=\delta_{AB}g^{\mu\nu}
+2c\theta_N C_A C_B\ell^\mu\ell^\nu.
\tag{22}
\]
Polarizations perpendicular to \(C\) have principal metric \(g\). The parallel polarization has
\[
G_N^{\mu\nu}=g^{\mu\nu}+\chi_N\ell^\mu\ell^\nu,\qquad
\chi_N=2c\theta_N|C|^2.
\tag{23}
\]
For a covector \(k\), the determinant factorizes:
\[
\det(\mathsf P_{AB}^{\mu\nu}k_\mu k_\nu)
=(g^{\mu\nu}k_\mu k_\nu)^{m-1}
(G_N^{\mu\nu}k_\mu k_\nu).
\tag{24}
\]
At \(C=0\), all factors coincide. A varying internal direction affects lower-order terms but not this pointwise factorization.

The null rank-one update has the exact inverse and determinant
\[
\boxed{(G_N)_{\mu\nu}=g_{\mu\nu}-\chi_N\ell_\mu\ell_\nu,
\qquad \det G_N^{\mu\nu}=\det g^{\mu\nu}.}
\tag{25}
\]
Matrix multiplication proves the inverse, because the cross terms cancel and the quadratic correction contains \(\ell^2=0\). The determinant lemma gives the factor \(1+\chi_N\ell^2=1\). Along the continuous parameter from zero to any finite \(\chi_N\), the matrix never degenerates; its Lorentzian signature is therefore unchanged.

For \(\sigma=-1\), equation (1) gives \(\chi_N>0\) whenever \(C\ne0\). In the \(+---\) convention every \(g\)-timelike covector remains \(G_N\)-timelike:
\[
G_N^{\mu\nu}\tau_\mu\tau_\nu
=g^{\mu\nu}\tau_\mu\tau_\nu+\chi_N(\ell^\mu\tau_\mu)^2>0.
\]
This supplies a common time orientation. An effective-null ray vector satisfies
\[
g_{\mu\nu}v^\mu v^\nu=\chi_N(\ell_\mu v^\mu)^2\ge0.
\tag{26}
\]
The effective ray cone therefore lies inside the background cone. They touch along the shared null generator; perpendicular internal modes retain the background cone. For \(\sigma=+1\), the update remains Lorentzian but the cone nesting reverses. No total physical energy-positivity conclusion follows from either sign alone.

The uniform response bound gives
\[
|\chi_N|<256\eta^2|C|^2.
\tag{27}
\]
With an independently provided scaling \(\eta\to0\) and bounded background amplitude, the principal metric returns to \(g\) at a cap-uniform \(O(\eta^2)\) rate.

## 7. Full linearized propagation with reduced Brinkmann geometry held

Take
\[
ds^2=2\,du\,dv+H(u,x,y)\,du^2-dx^2-dy^2,\qquad
\psi_A=\Psi_A(u),\quad C_A=\Psi_A'(u).
\tag{28}
\]
Use a factorized local price with constant scalar coefficients throughout the patch and its original coordinate measure \(du\,dv\,dx\,dy\). On this particular chart \(\det g=-1\), so the scalar divergence operator in that fixed measure is
\[
\Box_g=2\partial_u\partial_v-H\partial_v^2
-\partial_x^2-\partial_y^2.
\tag{29}
\]
This agreement on the background does not change the action's measure away from it. The background solves the reduced matter equation, since its current points in the \(v\) direction and all coefficients are independent of \(v\).

Let \(\xi_A\) be an arbitrary small material disturbance. It need not be null, independent of \(v\), or aligned with \(C\). Under the spectator condition of Section 5, the full first variation of the reduced matter equation is exactly
\[
\boxed{\mathcal D_N\xi
=\Box_g\xi+2c\theta_N C(u)C(u)^T\partial_v^2\xi=0.}
\tag{30}
\]
Indeed \(\delta Y=2cC^T\partial_v\xi\), and variation of the kinetic coefficient is \(K_N''(0)\delta Y\). Its outer divergence is \(\partial_v\), which does not differentiate the \(u\)-dependent background. No terms have been discarded. Higher derivatives of \(K_N\) enter higher disturbance orders and are not asserted to vanish.

For the Fourier statement, take \(v\in\mathbb R\) with the smoothness and integrability needed for the displayed transforms and estimates, or take periodic \(v\) and the corresponding discrete Fourier modes. External boundary conditions must be transported by the intertwiner. It does not in general preserve a prescribed boundary condition at a fixed finite \(v\)-endpoint; equality of two problems with identical untransported boundary data is not asserted.

### 7.1 Exact unitary intertwiner

Use \(\partial_v\mapsto ik\). Define
\[
\boxed{\frac{dU_{N,k}}{du}
=-ikc\theta_N C(u)C(u)^T U_{N,k},\qquad U_{N,k}(u_0)=I.}
\tag{31}
\]
For real \(k\), the generator is anti-Hermitian, hence
\[
U_{N,k}^*U_{N,k}=I.
\tag{32}
\]
This remains true when the internal direction rotates. The solution is then an ordered exponential, not generally one exponential of a commuting integral.

If \(\widehat\zeta(u,k,x,y)\) solves the Fourier-transformed ordinary Brinkmann wave equation, then
\[
\boxed{\widehat\xi_N=U_{N,k}(u)\widehat\zeta}
\tag{33}
\]
solves (30), and the inverse matrix gives the converse. The transformed operator is
\[
2ik\partial_u+k^2H-\Delta_\perp
-2c\theta_N k^2CC^T.
\]
The matrix \(U\) depends only on \(u,k\), so it commutes with \(H\) and the transverse scalar operators. The extra derivative \(2ikU'\) exactly cancels the last matrix term. At \(k=0\), \(U=I\) and the identity holds without dividing by \(k\).

At each fixed \(u\), this multiplier is unitary on the internal \(L^2\) space in \(v\), also after integrating in \(x,y\). Since \(U_{N,-k}=\overline{U_{N,k}}\), it preserves the reality condition. The nonlinear response gives an explicit norm-preserving longitudinal transport on the held reduced curved background, including arbitrary internal rotation. This is an expression for the relative propagation effect, not an assertion that it is physically absent.

### 7.2 Fixed direction, translation and curvature

If \(C(u)=a(u)n\) for a fixed internal unit vector \(n\), put \(P=nn^T\) and
\[
J_N(u)=c\theta_N\int_{u_0}^{u}a(s)^2\,ds
=\frac12\int_{u_0}^{u}\chi_N(s)\,ds.
\tag{34}
\]
Then
\[
U_{N,k}=I-P+e^{-ikJ_N}P.
\tag{35}
\]
Only the parallel component is translated to \(\zeta_\parallel(u,v-J_N(u),x,y)\). Its effective metric is
\[
ds_{N,\parallel}^2
=2\,du\,dv+[H(u,x,y)-\chi_N(u)]\,du^2-dx^2-dy^2.
\tag{36}
\]
This is the pullback of the background metric under \((u,v,x,y)\mapsto(u,v-J_N(u),x,y)\). The effective metric individually has the same curvature as the background. The transverse second derivatives of \(H\), which determine Ricci and Weyl curvature, are unchanged. The relative cone nesting in the same chart remains (26); changing coordinates for one metric alone does not remove that relation.

For rotating internal direction, the effective principal metric defined by \(|C(u)|^2\) has the same individual isometry. The exact full internal matter-system intertwiner nevertheless remains the matrix transport (31), because diagonalization varies with \(u\).

### 7.3 Cap-uniform propagation estimate

Define
\[
\mathcal E(u)=\int_{\min(u,u_0)}^{\max(u,u_0)}|C(s)|^2\,ds.
\]
Integrating (31) and using unitarity and (1) gives
\[
\boxed{\|U_{N,k}(u)-I\|
\le\min\{2,128|k|\eta^2\mathcal E(u)\}.}
\tag{37}
\]
For a disturbance with one square-integrable \(v\) derivative, Plancherel yields
\[
\|\xi_N(u)-\zeta(u)\|_{L^2(v,x,y)}
\le128\eta^2\mathcal E(u)
\|\partial_v\zeta(u)\|_{L^2(v,x,y)}.
\tag{38}
\]
This is uniform over the admitted fixed finite caps and price parameters. It gives a genuine \(O(\eta^2)\) linearized propagation recovery when a separate physical scaling supplies \(\eta\to0\), the background is fixed, and the displayed derivative is controlled. It does not require an infinite-cap limit or assert a rate without that derivative control.

## 8. Retained interface obligations

The finite response theorem uses the literal detector and fixed-cap formula. Its bound \(\kappa>53\) is a consumed unit-charge premise whose native implementation was not freshly replayed here.

The propagation theorem additionally requires the local kinetic dictionary, its normalization and sign, the fixed measure on the Brinkmann chart, and constant scalar coefficients on the patch. It does not cover a correlated nonlocal kinetic functional or arbitrary transverse variation of compiler weights. Such cases retain additional derivative terms.

Geometry held in this calculation means the transformed geometry. The original coframe generally varies as (20a). Retained spectators must have no matter variation on the patch for the full matter equation claim. This is a full off-null *linearized* material calculation within that reduced description, not a solution of all original coupled gravity and auxiliary rows, a proof of the nonlinear gravity-matter Cauchy problem, or a lattice-refinement theorem.

No physical energy sign for all degrees of freedom, minimizing history/field execution, compulsory price, independent preparation root, or clock selection is inferred. Those source equations remain as retained by the parent normal form.

The positive extension is an exact cross-cap response theorem and explicit propagation law for the nonlinear matter term already forced by the price. A curved Brinkmann null background of the previously constructed form supports controlled reduced material propagation, with exact Lorentzian cone structure and a cap-uniform recovery estimate under separately supplied scaling.
