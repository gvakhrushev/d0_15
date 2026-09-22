# E-METPROV — Finite Metric Provenance Carrier

CONTROL disposition: **ACCEPT AS RESEARCH / FINITE-METRIC-CARRIER-ENLARGEMENT-REQUIRED**

Source memo: `MEMO_33_A4D_FINITE_METRIC_PROVENANCE_CARRIER.md`.

## Exact obstruction

For (L=N+2\ge3), the owned nearest-neighbour role-product graph has (L^4) sites and exactly (4L^4) undirected axis edges. Therefore
[
\dim EdgeConductanceVariation(N)=4L^4,
]
and the owned `archiveLocalLaplacianVariationEquiv` gives the same dimension for `LocalLaplacianVariation N`.

By contrast,
[
\dim LocalSymRoleField(N)=10L^4.
]

Hence no linear conductance/Laplacian realization can be surjective onto the general local symmetric Role metric field. Any differentiable realization through this carrier has differential rank at most (4L^4).

The constant-fibre (S_4) decomposition sharpens the statement. The four axis slots form the permutation module
[
P\cong \mathbf1\oplus\mathbf3,
]
while
[
Sym^2P\cong2\mathbf1\oplus2\mathbf3\oplus\mathbf2.
]
The exact missing six-dimensional module is the unordered distinct Role-pair module
[
Q\cong\mathbf1\oplus\mathbf3\oplus\mathbf2.
]

Existing cubical degree-two cochains transform as the exterior module
[
\Lambda^2P\cong\mathbf3\oplus\mathbf3',
]
so the six cubical labels may be reused combinatorially but their oriented cochain amplitudes cannot be identified with symmetric metric shear.

## Minimal repair

Add one independent local scalar for every unordered distinct Role pair, in addition to the four axis variables:
[
\mathcal M_N^{min}
=
X_N\to
(\mathbb R^{Role}\oplus\mathbb R^{\binom{Role}{2}}).
]

This has exactly (10L^4) real coordinates and is canonically (S_4)-equivalent to the symmetric Role tensor field once the six pair variables are declared as unoriented symmetric shear/Role-pair data.

The old conductance sector embeds only as the diagonal locus.

Carrier enlargement by itself does not derive:

- the physical conductance-to-metric normalization;
- the Lorentz (E_{\eta,N}) action/response;
- finite metric gauge provenance.

Those are separate obligations.

Terminal result:
[
\boxed{\texttt{FINITE-METRIC-CARRIER-ENLARGEMENT-REQUIRED}}.
]
