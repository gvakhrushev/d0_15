# E-STAGHODGE — Staggered / Primal-Dual Hodge Carrier

CONTROL disposition: **ACCEPT AS RESEARCH / PRIMAL-DUAL-HODGE-CARRIER-REQUIRED**

Source memo: MEMO_45_A4D_STAGGERED_PRIMAL_DUAL_HODGE_CARRIER.

The minimal pre-centered coframe perturbation is
\[
e_r{}^a(x),\qquad \dim=16L^4,
\]
with forward gauge law
\[
\delta_\xi e_r{}^a=\nabla_r^+\xi^a.
\]
The centered metric readout
\[
R(e)_{ab}=A_ae_a{}^b+A_be_b{}^a
\]
satisfies exactly
\[
R(d_f\xi)=\texttt{symmetricRoleGradient}(N,\xi).
\]

For odd \(L\), \(R\) is surjective and its kernel has dimension \(6L^4\), the expected frame-type sector.

For even \(L\), centering loses canonical Nyquist metric data:
\[
\dim\ker R=6L^4+4L^3+6L^2,
\]
\[
\operatorname{rank}R=10L^4-4L^3-6L^2,
\]
\[
\dim\operatorname{coker}R=4L^3+6L^2.
\]
The missing residue consists of diagonal single-Nyquist and off-diagonal joint-Nyquist metric modes. A surjective common carrier therefore requires an explicit gauge-invariant Nyquist residue \(n\) with
\[
m=R(e)+n.
\]

At the Hodge level there is an explicit bounded-stencil self-adjoint non-diagonal variation \(\mathfrak H(e)\) satisfying
\[
\mathfrak H(d_f\xi)=-(G_\xi^*+G_\xi)
\]
for centered Cartan. Hence at the flat Hodge background both first-order \(S_D\) and second-order \(S_2\) have exact finite tangent Ward cancellation.

The required offsets remain bounded:
\[
0,\ \pm e_r,\ \pm e_s,\ \pm(e_s-e_r).
\]

However a sparse non-diagonal primal-only Hodge matrix has a generically dense inverse, so the finite-deformation codifferential \(W^{-1}d^*W\) loses bounded-stencil locality. The natural locality-preserving architecture is therefore a mixed primal/dual cubical carrier with a local constitutive Hodge map rather than an explicitly inverted primal mass matrix.

Finally, the additive coframe gauge is only linearized. Exact arbitrary-\(e\) covariance needs an \(e\)-dependent transport/connection or nonlinear coframe Lie derivative. Metric stress conservation also requires the coframe equation (or an explicit frame-gauge quotient) through a parent constraint such as
\[
S_{\rm parent}=S_H[e,\psi]+\langle\Lambda,m-R(e)-n\rangle.
\]

Terminal result:
\[
\boxed{\texttt{PRIMAL-DUAL-HODGE-CARRIER-REQUIRED}}.
\]
