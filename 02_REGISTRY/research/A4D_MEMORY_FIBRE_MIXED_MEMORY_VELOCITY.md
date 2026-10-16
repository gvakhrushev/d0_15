# Memory motion cannot rescue the q3300 crossing

Date: 2026-10-16. This is a local continuation of the [certified q3300 crossing](A4D_MEMORY_FIBRE_CROSSING_TRANSVERSALITY.md), using the exact reduced functional and the memory-source compatibility condition already owned there.

## Theorem

Fix any root in the certified \((d,o)\) box and its unique crossing \(t_*\in(0.42,0.44)\). Let \(v\ne0\) be any real vector in the two-dimensional realification of the crossing \(q,-q\) mode pair. Let \(w\) be an arbitrary first-order tangent to the smooth affine stationary preparation fibre at \(\sigma_{t_*}\), where

\[
\sigma_t=(1-t)I_{16}/16+t|\chi\rangle\langle\chi|,
\qquad \chi=(e_1-e_{15})/\sqrt2.
\]

If the complete first velocity has **only** these field modes and this memory component, \(\xi=(v,w)\), then it fails the second-order stationary-jet compatibility condition. Thus no choice of a first-order velocity along the memory fibre can repair the q3300 obstruction. This does not cover additional field Fourier modes.

## Proof

The smooth reduced functional owned by the full-rank preparation analysis is

\[
\Phi(x,\sigma)=F_{\rm price}(\Delta(x))+\widehat\epsilon(x,\sigma),
\qquad \operatorname{Tr}(\sigma E(x,\widehat\epsilon))=0,
\]

with \(-D_\epsilon\operatorname{Tr}(\sigma E)=\operatorname{Tr}(\sigma G)>0\). At the fixed root, every normalized density on the degenerate shell has the same eigenvalue, so \(\widehat\epsilon(x_0,\sigma)=\epsilon_0\) throughout the stationary memory fibre. Since \(t_*\in(0.42,0.44)\), the base density is strictly positive, and these are ordinary tangent directions in a smooth affine fibre.

For \(\Omega=\{\pm e_r\}_{r=0}^3\subset(\mathbb Z/8)^4\), the q3300 representative \(q=(3,0,0,3)\) and its negative are outside \(\Omega-\Omega\). Translation support therefore gives \(P D_xE(x_0,\epsilon_0)[v]P=0\). Hence \(D_x\widehat\epsilon(x_0,\sigma)[v]=0\) identically over the entire affine memory fibre, not just at its midpoint.

Write the first velocity as \(\xi=(v,w)\), and test second-order solvability against the memory tangent \((0,\zeta)\). Its cubic compatibility component is

\[
D^3\Phi[\xi,\xi,(0,\zeta)]
=D^3\widehat\epsilon[(v,0),(v,0),(0,\zeta)]
 +2D^3\widehat\epsilon[(v,0),(0,w),(0,\zeta)]
 +D^3\widehat\epsilon[(0,w),(0,w),(0,\zeta)].
\]

The last term vanishes because \(\widehat\epsilon(x_0,\sigma)\) is constant on the fibre. The middle term vanishes because \(D_x\widehat\epsilon[v]\) is identically zero there. The remaining term is exactly the owned second-response pairing \(\operatorname{Tr}(\zeta M_v)\); the field-only price has no memory derivative. This is the full reduced functional, so the argument includes the field-dependent matter reconstruction.

Take the actual tangent \(\zeta=|\chi\rangle\langle\chi|-I_{16}/16\), which has zero trace and zero pairing with all three native source rows. The stationary source fibre is a smooth critical submanifold, so \((0,\zeta)\) is a genuine Hessian-kernel direction. The outward interval certificate gives \(\operatorname{Tr}(\zeta M_v)<-0.8441\) for every unit crossing vector, uniformly over the root box. For any nonzero scale \(a\), the pairing for \(av+w\) is \(a^2\operatorname{Tr}(\zeta M_v)\ne0\). But second-order solvability requires this pairing to vanish for every Hessian-kernel tangent \((0,\zeta)\). Contradiction.

The exact quotient-jet identity and Fourier support check replay in [the source packet](sources/d0_memory_fibre_mixed_memory_velocity_2026-10-16/README.md). The numerical bound is consumed unchanged from the prior outward certificate.

## Boundary

This removes the memory-only escape direction for the one simple q3300 crossing pair. A first velocity containing other field modes can contribute additional quadratic terms and remains unclassified; so do other preparations, distant roots, exact nonlinear continuation, physical admission, refinement, recovery, and Einstein identification. No action, selector, or physical postulate is added.
