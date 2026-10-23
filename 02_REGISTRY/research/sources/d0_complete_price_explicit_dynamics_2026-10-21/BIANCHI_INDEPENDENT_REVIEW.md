# Independent review: common nonnull Bianchi I complete-price family

**Date:** 2026-10-21.  
**Reviewer:** a separate analytical review agent; no external human peer review or Lean formalization is claimed.  
**Declared continuum theorem:** **PASS**.  
**Identification with the original native matter/geometry dictionary:** **CONDITIONAL / NOT REPLAYED**.  
**Finite-lattice counterpart:** not proved by this theorem.  
**Closure:** GR_closed = false.

The entire Bianchi proof was read and independently checked. The lapse, undensitized material variation, independent Lorentz-connection equation, all metric components, general Kasner identities and explicit Weyl components were recomputed analytically. No mathematical correction remains. One purely editorial change, replacing an inaccurate reference to spatial metric dependence with “time-dependent spatial scale factors,” was incorporated in the final source.

## 1. Exact reviewed snapshot

| Artifact | SHA-256 |
|---|---|
| A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE_2026_10_21.md, 14,619 bytes | cc856a24ded799d1c17e1ec645991f8206f187b49c61ab1debbc5e4c321a87f5 |
| check_explicit_branch_and_propagation.py, inspected Bianchi calculation | efc80841b6223e1e26c09c0e8b596c4a3d85f2714256190efdad7913b962c431 |
| CHECK_RESULTS.json, inspected recorded execution | 8391264de003ab306850923608f5434c65f44702879c7fb19b2d06ee56627a64 |

The mathematical review is independent of the recorded numerical residual. The combined checker was run by the parent agent; this reviewer inspected its relevant code and stored PASS receipt and did not perform a redundant second execution.

## 2. The action and its full first variation are correctly specified

The theorem solves, on a fixed oriented coordinate cylinder and in signature \(+---\),
\[
S_N=\int g_N(r(x,y))\,d^4x,\qquad
x=\eta^2 eR(e,\omega),\qquad
y=-\eta^2g^{\mu\nu}\partial_\mu\overline\psi\,\partial_\nu\psi,
\qquad e=\sqrt{|\det g|}.
\]

The coframe and Lorentz connection are independent variables. The matter is the explicitly declared connection-independent complex scalar with Hermitian kinetic contraction. The measure outside the nonlinear price is fixed. These assumptions are part of the theorem, not conclusions about the current native CAR carrier.

At spacetime-constant \(x_*,y_*\), the exact ambient first variation is
\[
\delta S_N
=\eta^2g_N'(r_*)\int
\left[r_x(x_*,y_*)\,\delta(eR)
-r_y(x_*,y_*)\,\delta q\right]d^4x.
\]
This calculation is valid for arbitrary admitted field variations, including inhomogeneous variations that do not preserve either query. Constant queries are a property of the background, not a restriction imposed before differentiating.

All three coefficients are spacetime constant at this background. Thus integration by parts produces no missing gradients of a response coefficient. A common nonzero outer derivative multiplies the complete first source.

### Independent connection and coframe rows

The connection equation is the nondegenerate Lorentz-Palatini equation, with a nonzero scalar prefactor. The torsion-free spin connection solves it. The declared scalar query has no independent connection source.

At that connection the symmetric coframe equations are equivalent to
\[
r_x eG_{\mu\nu}
-r_y\partial_{(\mu}\overline\psi\,\partial_{\nu)}\psi=0.
\]
The antisymmetric coframe equations vanish with the connection equation by internal Lorentz invariance; equivalently, the torsion-free Ricci tensor and the displayed material source are symmetric. The proof consequently checks all sixteen coframe rows and all twenty-four independent Lorentz-connection rows in this continuum action.

The use of an independent connection matters. The general reciprocal-homogeneity and coframe normal-form argument is a Palatini argument; a metric-only curvature expression has additional conformal derivative terms. No silent replacement of those two off-shell actions is needed in the Bianchi proof.

### Undensitized matter and scalar rows

The material query has no factor \(e\). Its inverse-metric variation is therefore the Hermitian product of first derivatives, with no extra \(-g_{\mu\nu}q/2\) term. Inserting such a term would change the proposed solution and would solve a different action.

For the same reason, at this constant response the material equation is
\[
\partial_\mu(g^{\mu\nu}\partial_\nu\psi)=0,
\]
not the equation with \(e g^{\mu\nu}\) inside the divergence. The two real scalar equations are both retained. This distinction is essential for the linear-in-time scalar below.

## 3. General Bianchi geometry: direct calculation

Let \(D=t(t+t_0)\), \(t>0\), \(t_0>0\), and let real exponents satisfy
\[
\sum_i\nu_i=\sum_i\nu_i^2=1.
\]
Take
\[
a_i=A_i t^{\nu_i}(t+t_0)^{2/3-\nu_i},\qquad
ds^2=dt^2-\sum_i a_i^2(dx^i)^2.
\]
Then
\[
e=A_*D,\quad A_*=\prod_iA_i,\qquad
H_i=\frac{(2/3)t+\nu_i t_0}{D},\qquad
\Theta=\frac{2t+t_0}{D}.
\]

Independently differentiating gives
\[
\dot H_i+\Theta H_i=\frac2{3D},\qquad
\sum_{i<j}H_iH_j=\frac4{3D}.
\]
The second identity follows by expanding the numerator and using both Kasner constraints. They imply, in exactly the curvature convention stated in the proof,
\[
R_{00}=\frac2{3D},\qquad R^i{}_i=-\frac2{3D},\qquad
R=-\frac4{3D},
\]
and hence
\[
G_{00}=\frac4{3D},\qquad G_{0i}=0,\qquad G_{ij}=0.
\]

These are complete tensor-component identities. The result is not inferred by varying a gauge-fixed homogeneous action.

## 4. Nonzero query realization and every field equation

Take any \(-2^{-12}<y_*<0\) and \(x_*=\tau(y_*)<0\) from the proved trace branch. Choose
\[
A_*=-\frac{3x_*}{4\eta^2}>0,\qquad
\psi(t)=c_\psi t+\psi_0,\qquad
c_\psi^2=-\frac{y_*}{\eta^2}>0.
\]
The queries then equal
\[
\eta^2 eR=x_*,\qquad -\eta^2q=y_*
\]
at every point. Both are nonzero. The remaining \(00\) equation is exactly
\[
r_x eG_{00}-r_yc_\psi^2
=\frac{-x_*r_x+y_*r_y}{\eta^2}=0.
\]
The last equality is the original detector trace equation. Every other metric component vanishes separately. The scalar current equation is \(\partial_t c_\psi=0\); the imaginary scalar equation also vanishes. The torsion-free connection already solves the independent connection equation.

Thus the construction turns the trace branch into a real **full-field** solution of the declared continuum action. It does not merely exhibit a trace-stationary pair. The choice of \(A_*\) is a solution constraint relating integration constants and matter amplitude; no coefficient of the price or detector has been fitted to the desired geometry.

The same original fields work for every fixed finite cap with the stated parameter interface. More generally, any regular smooth outer function of the same response has the same vanishing first source at this background. Site-dependent or spacetime-dependent prices would require their actual coefficient derivatives and are not automatically included.

## 5. The lapse equation is present

Permitting \(g_{00}=N(t)^2\) during variation and only afterwards evaluating \(N=1\) gives
\[
\delta g^{00}=-2\delta N,\qquad
\delta q=-2c_\psi^2\delta N.
\]
The exact lapse coefficient in the first variation is
\[
2\eta^2g_N'(r_*)[-r_xeG_{00}+r_yc_\psi^2],
\]
which vanishes by the displayed full \(00\) equation. This confirms that the use of proper-time coordinates for the solution has not erased the constraint equation.

Compactly supported variations, or original collar data held on a time cylinder with \(t_->0\), justify the integrations by parts. The singular endpoint \(t=0\) is outside the stated domain. The result does not require a variation of a lapse-fixed reduced action.

## 6. Nonzero Weyl and Ricci curvature

For \((\nu_1,\nu_2,\nu_3)=(-1/3,2/3,2/3)\),
\[
a_1=A_1(t+t_0)t^{-1/3},\qquad
a_{2,3}=A_{2,3}t^{2/3}.
\]
In the orthonormal frame and the proof's curvature convention,
\[
R_{0i0i}=\dot H_i+H_i^2,\qquad
C_{0i0i}=R_{0i0i}+\frac2{9D}.
\]
Direct substitution gives
\[
(C_{0101},C_{0202},C_{0303})
=\frac{t_0}{9tD}(4,-2,-2).
\]
The off-diagonal mixed curvature components vanish, so the magnetic Weyl tensor vanishes. Consequently
\[
C_{abcd}C^{abcd}=\frac{64t_0^2}{27t^2D^2}>0.
\]
The Ricci scalar is also nonzero. The source has the pressureless algebraic form
\[
G_{\mu\nu}=\frac4{3D}(dt)_\mu(dt)_\nu.
\]
This is the source derived from the specified fixed-measure scalar action. No separately postulated dust fluid is needed, and no identification with native CAR stress is inferred without its actual dictionary.

## 7. Normal-form and minimum interpretation

The original solution is cap-independent. Its transformed normal-form coframe is a positive spacetime-constant, generally cap-dependent rescaling:
\[
\widetilde e_N=\sqrt{u_N(y_*)}\,e.
\]
There is no contradiction: the stationary equivalence changes coordinates while the original common solution is fixed.

For this family \(y_*<0\). The actual radial second variation has sign \(g_N'(r_*)y_*\). It is a strict radial minimum for cap one and a strict radial maximum for caps at least two. The common family is therefore a stationary family. It is not a common all-cap minimum or a minimizing full physical execution, and no positivity of its remaining Hessian is asserted.

## 8. Verification scope and native interface

The inspected combined checker contains exact polynomial identities over \(\mathbb Q[t,t_0]\) for the explicit anisotropic representative: all displayed Einstein components, scalar curvature and electric Weyl components are checked for all times, rather than sampled times. Its stored receipt reports PASS. Its additional 90-digit calculation tests the complete inverse-metric source at one nonzero trace point and caps \(1,2,7,31\); the recorded normalized residual is approximately \(1.8731\times10^{-92}\).

That numerical check is a non-interval diagnostic. The general Kasner family, arbitrary finite-cap statement and all ambient equations are justified by the analytic proof, not by those four samples. The checker is not a native finite-lattice all40 execution, and its scalar or connection component statements are not fresh implementations of the original repository operators.

For native use, the original geometric density must match \(\eta^2 eR\) in the stated convention and normalization, the matter query must match the connection-independent Hermitian scalar expression without a volume factor, and the complete price and fixed measure must actually be the stated ones on the admitted sector. Native spinor, charged, constrained-preparation or moving-weight sources cannot be silently dropped.

The theorem holds its internal parameters fixed. It does not solve independent preparation, clock, writer, reference or other baseline-source equations. It also does not prove a discrete Bianchi solution at finite lattice spacing, a continuum limit, or full diffeomorphism covariance of the nonlinear fixed-measure price.

**Final verdict:** the displayed model has an exact common nonnull, anisotropic, fully stationary continuum family with nonzero Ricci and Weyl curvature, including the lapse and independent-connection equations. This is a strong constructive extension beyond null first-source persistence. The current native dictionary binding and compulsory physical-action selection remain separate, explicit obligations.
