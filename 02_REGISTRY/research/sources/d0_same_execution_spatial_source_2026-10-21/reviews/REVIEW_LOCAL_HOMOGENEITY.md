# Independent bounded review: actual primary dictionary and spatial source

21 October 2026. Reviewer: metric_source_synthesis, inside existing #334.
Repository input c49ebdb12244943d1ec45ef6d148a0432481141e; no repository edits.

Reviewed files:

- `SAME_EXECUTION_LOCAL_HOMOGENEITY_AND_WEIGHT_SOURCE.md`, SHA256
  `62aa5b45923e6e9d51e2075507cd114d42c5f7d1f5107a99e1b08be053e3c034`.
- `check_spatial_source.py`, SHA256
  `75feeeee89aa0db6069205f8116d27e89f08b1d3a595897071ec62054200235a`.

Scope: the same-primary dictionary, §§1 and 3–5, together with the actual
weight definition and multiplicity boundary in §2. This is not a review of
physical task/Info/query admission or a new proof of the old primary roots.

**Status: ACCEPT at the stated scope. No mathematical defect found.**

The local star uses the coframe only at its anchor; the signed material
square uses the inverse metric at the same anchor, with neighboring forward
matter differences independent of their coframes. Thus independent local
scaling gives x_i→u_i x_i and y_i→y_i/u_i on the actual dictionary. The two
inverse powers in raw material variables reduce to one common inverse rho
in operational variables; no density measure is inserted.

The full 24-row table includes both forward and inverse appearances of
each shared link and its own face-anchor weight. Its four displayed
weight-only rows force the four backward coefficient equalities without
using a matter equation or a nonzero curvature assumption. Once equal,
the remaining rows are the original Cartan rows times that coefficient.
The necessity is correctly restricted to the actual free incident stencil;
it is not silently imposed on fixed exterior links.

The coframe residual is exactly −2(B_i−lambda A_i)E_u/h after the original
Poisson equation. The material variation is the weighted backward-v
adjoint, so varying coefficients are retained even when q itself is zero.
The stated internal differential includes actual density/preparation
dependence; derivatives of coefficients multiply zero densities on Sigma,
while the baseline derivative survives. The necessary-and-sufficient claim
is for the stated two-density price and actual admitted tangent; an extra
real price contributes its full covector rather than a free compensation.

The global aggregate auxiliary example consistently uses one common
coframe scale pi/a; its induced material interaction retains cross-site
terms. It is not converted into a sum of independent local interactions.
The transported collar qualification is necessary and is explicitly kept.

Independent verification: read the checker and ran its one new narrow
symbolic calculation once. PASS, elapsed 0.572777667 seconds. The checker
imports only the owned stencil definitions, differentiates the changed
weighted face expression directly, and compares it with the separate
displayed table. It also tests four unequal-neighbor controls, moving
inverse-PF derivatives, the material adjoint and the aggregate auxiliary
identity. No old root, continuum, rank or Lean suite was rerun.

Receipt: `INDEPENDENT_SPATIAL_CHECK.json` beside this review. The fixed
programme cost/Info and actual replication hypotheses remain the author's
stated source inputs; a shared correlated factory or random-address
execution would require its own full law.
