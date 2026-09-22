# E-PDH-PARENT — Primal/Dual Hodge Parent Ward

CONTROL disposition: **ACCEPT AS RESEARCH / DISCRETE-SPIN-CONNECTION-REQUIRED**

Source memo: MEMO_47_A4D_PRIMAL_DUAL_HODGE_PARENT_WARD.

The accepted staggered coframe data remain:
\[
\delta_\xi e=d_f\xi,\qquad
m=R(e)+n,\qquad
R(d_f\xi)=K_N\xi.
\]

The direct nonlinear total-coframe transport
\[
\delta_\xi e=d_f\xi+G_\xi^{(1)}e
\]
has the correct flat tangent and chain behavior but is incompatible with retaining both the frozen linear metric readout and exact affine metric gauge. On odd \(L\), the one-role diagonal restriction makes the readout invertible, so exact constraint preservation forces the nonlinear transport term to vanish.

Allowing an \(e\)-dependent centered generator does not solve locality. On an exact \(L=5\) scalar control, the commutator of local centered generators has unavoidable cyclic distance-two symmetric entries. No radius-one correction can cancel them, and the direct Hodge congruence orbit grows stencil at higher orders.

Hence the missing nonlinear datum is an independent connection carrying chain-transport curvature. A pure local Lorentz spin connection is insufficient because the obstruction already occurs on scalar cochains.

The parent algebra itself is viable. With local primal/dual complexes, a constitutive map
\[
\star_k:C_P^k\to C_D^{4-k},
\]
an auxiliary codifferential field and multiplier, the mixed \(S_2\) action can be written without any explicit \(\star^{-1}\), preserving bounded locality. Under chain generators commuting with the incidence differentials and
\[
\delta\star=G_D\star-\star G_P,
\]
the mixed action has an exact finite Ward identity.

Combined with
\[
m=R(e)+n,\qquad \delta n=0,
\]
the coframe equation and the already-owned adjoint theorem for \(K_N=\texttt{symmetricRoleGradient}\), the parent Ward identity conditionally descends to
\[
\operatorname{centeredRoleDivergence}\Lambda=0.
\]

The remaining load-bearing theorem is a local equivariant constitutive law
\[
\star=\mathcal S(e,n,\Omega)
\]
for a new link/chain transport connection \(\Omega\), with flat derivative equal to the accepted staggered Hodge response and curvature absorbing centered-Cartan closure.

Terminal result:
\[
\boxed{\texttt{DISCRETE-SPIN-CONNECTION-REQUIRED}}.
\]
