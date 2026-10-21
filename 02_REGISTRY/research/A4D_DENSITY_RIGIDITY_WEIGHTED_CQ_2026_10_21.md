# Density rigidity for weighted CQ price

**Date:** 2026-10-21
**Status:** analytic consequence of the weighted CQ price and its stationary transformation. Not yet a physical price selection.
**Closure:** GR_closed = false.

## Statement

For the continuum expression of the N=1 CQ price with inhomogeneous PF weights,
\[
S = M \int \rho(z) F(x,y)\,d^4z + B_0,
\]
the stationary equations imply
\[
\boxed{d\left(\frac{\rho\,y}{F_x}\right) = 0}
\]
on a connected regular domain. In the already constructed stationary chart \(g_E = u g\) this is equivalent to \(dQ_E = 0\), where \(Q_E\) is the kinetic norm of the two matter fields.

## Consequences

The metric and matter equations become
\[
G_{\mu\nu}(g_E) = \mu \sum_{A=1}^{2} \partial_\mu\psi_A \partial_\nu\psi_A,
\]
\[
\nabla_\mu^E(\mu \nabla_E^\mu \psi_A) = 0,\qquad Q_E = q_* = \text{const}.
\]
A local bidirectional dictionary exists between the weighted CQ price and this constrained Einstein-matter system, subject to an explicit volume matching condition. On the primary family, full Jacobi fields satisfy \(\delta Q_E = 0\), so the nonlinear term does not correct the linear solutions.

## Limits

This does not select the physical price. It does not prove that finite native queries and clocks generate this continuum dictionary. Compact Lie variations are not automatic on the lattice. Upstream equations remain open.

## Checks

65 checks including variational identities, bidirectional dictionaries, source rank, and numerical controls on the original Golden function with inhomogeneous \(\rho\).

## Integration note

This note records the density rigidity result for the weighted CQ price. The full archives (proof, certificates, SHA256) remain in the local packages uploaded by the user and are not yet committed as separate files. The mathematical content of the result is integrated into the existing constitutive composition path.
