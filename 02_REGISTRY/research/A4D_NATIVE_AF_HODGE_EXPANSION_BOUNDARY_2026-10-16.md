# AF resolution versus the owned normalized Hodge/CAR metric

Research continuation, 2026-10-16. This note tests one concrete bridge from
the growing AF record engine to the already-owned Hodge/CAR metric. It uses
the exact all-size metric theorem in
[`A4D_NATIVE_HODGE_CONNES_METRIC.md`](A4D_NATIVE_HODGE_CONNES_METRIC.md)
and the AF capacity/record theorem in
[`A4D_NATIVE_ENGINE_CORRELATED_CURRENT_EXTENSION_2026-10-15.md`](A4D_NATIVE_ENGINE_CORRELATED_CURRENT_EXTENSION_2026-10-15.md).
It installs no new scale, operator, state restriction, or physical readout.

## Exact diameter under refinement

For the owned scalar point readout on the actual operator
\[
\mathcal D_L=L\sum_{r=1}^4\bigl[c_r^\dagger(S_r-I)+c_r(S_r^{-1}-I)\bigr],
\]
the proved Connes distance is
\[
d_L(x,y)=\frac1L\sqrt{\sum_{r=1}^4\ell_r(x,y)^2},\qquad
\ell_r(x,y)=\min(|x_r-y_r|,L-|x_r-y_r|).
\]
Let \(L\in4\mathbb N\). Each cyclic coordinate distance is at most \(L/2\),
so for every pair of sites
\[
d_L(x,y)^2\le \frac{4(L/2)^2}{L^2}=1.
\]
Equality is attained from any site to its antipode in all four coordinates,
\(y-x=(L/2,L/2,L/2,L/2)\). Thus the finite metric diameter is exactly
\[
\operatorname{diam}(X_L,d_L)=1\quad\text{for every }L\in4\mathbb N.
\]
An adjacent pair has distance \(1/L\), so increasing \(L\) makes the same
unit-diameter torus finer. This is an exact all-level conclusion from the
owned distance formula, not a finite-size extrapolation.

The factor that defines this cell scale is itself owned. In the phase carrier
\(L=N+2\), `archivePhaseDistance` assigns adjacent points length \(1/L\),
`forwardDifferenceScale` in the actual Hodge/CAR differential is \(L\), and
`archiveMetricLaplacianScale` is \(L^2\). The new Lean capsule proves for all
\(N\) that the actual Hodge difference coefficient squared times the phase
edge length squared is exactly one, and reuses the owned all-cochain identity
\(D_H^2=\Delta_{\mathrm{cochain}}\). Thus refinement and its inverse-square
heat coefficient are connected inside the current owners; the unit-diameter
result shows what this connection currently means: finer resolution at fixed
macroscopic size.

## What this says about the AF bridge

The AF engine's record tick \(k\) advances its Bratteli level by three and
has exact GNS capacity \(d_k=F_{6k+5}\), with \(d_0,d_1,d_2=5,89,1597\) and
strictly accelerating capacity. Its inherited \(M_2\) Lorentz readout stays
fixed at every depth. The owners do not identify AF tick \(k\), capacity
\(d_k\), and the Hodge torus size \(L\); there is no owned map \(k\mapsto L_k\)
or fine-sector map into a varying \((q,D)\).

Even if a future bridge assigns some \(L_k\in4\mathbb N\) and uses this same
normalized Hodge/CAR readout at each level, the diameter remains exactly one
while its cell scale becomes \(1/L_k\). If it keeps \(L\) fixed while the AF
carrier grows, this readout also remains unchanged. Therefore the specific
identification “AF capacity growth is expansion under the existing
normalized Hodge metric” fails: capacity growth and metric expansion are
different observables here.

Removing the factor \(L\) from \(\mathcal D_L\) would instead multiply every
Connes distance by \(L\), giving diameter \(L\). More generally, replacing
the owned operator by \(\lambda_k\mathcal D_{L_k}\) divides all distances by
\(|\lambda_k|\). Such a changing coefficient can produce a chosen scale
factor, but it is a change of operator/readout. No existing AF owner derives
it, so it cannot serve as the missing physical expansion law.

## Scope and next required result

This closes only the direct candidate bridge that reads AF refinement through
the already-owned normalized Hodge/CAR metric without a derived varying scale.
It does not rule out a genuinely fine AF observable or a different admitted
transition. The AF result remains positive for growing internal resolution
and retained record information; the Hodge result remains positive for an
exact flat metric on its represented scalar algebra.

The next load-bearing construction is still an owned transition from fine AF
records to the constrained variables \((q,D,b,m)\), including its actual
tangent and full-price readout. That transition must derive any scale change
from the existing preparation/action and survive the full constrained
equations. Until then, this candidate supplies neither physical expansion,
curvature, a source/Ward identity, nor Einstein dynamics. The checker binds
the prior AF and Hodge certificates and replays exact rational controls; the
all-size diameter proof is the two-line bound and antipodal equality above,
not a Lean formalization of the analytic Hodge metric theorem. Its replay
passes 844 controls over 128 carrier sizes and 35 AF capacity increments. The
Lean scale bridge compiles with standard axioms; the imported Hodge-square
owner retains its recorded three native CAR `native_decide` axiom leaves.
