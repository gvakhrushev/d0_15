# Weighted CQ density rigidity and Einstein-matter dictionary

**Date:** 2026-10-21.  
**Status:** analytic consequence of the weighted N=1 CQ price and its stationary normal form.  
**Closure:** GR_closed = false.

## 1. Conserved combination

For the weighted continuum price
\[
S = M\int \rho(z) F(x,y)\,d^4z + B_0,
\]
with
\[
x = \frac{\tau e R(e,\omega)}{\rho},\qquad y = -\frac{\tau Q}{\rho},
\]
the independent radial coframe variation and the compactly supported joint Lie variation together imply
\[
\boxed{d\!\left(\frac{\rho\,y}{F_x}\right)=0}
\]
on any regular connected domain where \(F_x F_y \ne 0\).

## 2. Stationary chart

In the already constructed stationary chart \(g_E = u g\) with \(u = F_x / a\),
\[
\frac{\rho y}{F_x} = -\frac{\tau}{a} Q_E.
\]
Hence
\[
\boxed{d Q_E = 0}.
\]

## 3. Einstein-matter system

The resulting equations are
\[
G_{\mu\nu}(g_E) = \mu\sum_{A=1}^{2}\partial_\mu\psi_A\partial_\nu\psi_A,
\]
\[
\nabla_\mu^E(\mu\nabla_E^\mu\psi_A)=0,\qquad A=1,2,
\]
\[
Q_E = q_* = \mathrm{const}.
\]
The coefficient \(\mu(z)\) absorbs the inhomogeneous \(\rho(z)\). The dictionary is bidirectional on the regular stationary branch under the explicit volume condition
\[
e_E\mu = -\frac{K'(\tau q_*/\rho)}{a}.
\]

## 4. Primary family

On the primary zero family, for any full Jacobi field,
\[
\delta Q_E = 0.
\]
The nonlinear term involving \(K''(0)\) therefore vanishes on full Jacobi fields. The stationary map preserves the metric and its linear solutions.

## 5. Boundary

The result lives in the continuum dictionary of the already constructed weighted price. It does not select the physical price, does not generate the continuum variations from the finite lattice, and does not solve the independent upstream equations. All physical selection gates remain open.

The full derivation, exact finite-source substitution, independent review, and
checker are in
[`WEIGHTED_WARD_AND_DUST.md`](sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/WEIGHTED_WARD_AND_DUST.md),
[`REVIEW.md`](sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/REVIEW.md),
and [`check_weighted_ward.py`](sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/check_weighted_ward.py).
The supplied synthesis is retained in the package handoff folder with only
trailing spaces removed; the note there pins the original attachment hash.
Its historical publication-status sentence is intake metadata; current
repository status is determined by the PR that carries these files.
