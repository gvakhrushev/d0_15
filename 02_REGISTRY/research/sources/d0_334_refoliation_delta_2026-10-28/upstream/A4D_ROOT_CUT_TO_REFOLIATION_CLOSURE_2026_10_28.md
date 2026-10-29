# Root cut versus geometric closure: exact conditional law-selection calculation

28 October 2026. Existing PR #334; input `eebcb5e467742df3e9cf7fa9702042d7294aa742`. No new task, replacement action, native gate, claim or assembly promotion.

[Full Russian proof](sources/d0_refoliation_closure_2026-10-28/PROOF_RU.md), [executed checker](sources/d0_refoliation_closure_2026-10-28/check_refoliation_closure.py), [observed result](sources/d0_refoliation_closure_2026-10-28/result.json).

## Consumed result and the exact missing distinction

The unchanged root Book03 source with moving P is owned by [the previous continuation](A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md). Its Kato connection has exact curvature `Omega_ij=-[partial_i P,partial_j P]`, with `[Omega_ij,P]=0`. This is internal block-frame curvature, NOT the metric hypersurface-deformation algebra. Likewise the original local-Lorentz Gauss propagation does not by itself supply canonical lapse generators.

A global closure route can instead test actual native local normal generators, their symplectic boundary data and the strong identity `{H[N],H[M]}=D[q^ij(N partial_j M-M partial_j N)]`. The well-known Hojman–Kuchar–Teitelboim/relational-geometrodynamics method is explicitly credited; this packet does not claim its discovery or infer its premises from the word closed.

## Exact theorem at its stated scope

Assume a local canonical 3-metric/momentum sector, an arbitrary smooth even ultralocal kinetic density T(q,pi), curvature potential `-b sqrt(q) R`, b != 0, and separate scalar matter with quadratic spatial gradients and no additional canonical pairs. Demand the strong geometric deformation algebra for all lapse functions BEFORE imposing constraints. The proof derives

    T=(pi^ij pi_ij-pi^2/2)/(b sqrt(q)) + cosmological density.

Quadratic momentum dependence is a consequence inside this declared class, not an initial kinetic ansatz. For scalar kinetic density `sqrt(q) F(phi,p/sqrt(q))` and spatial matrix D(phi), the same algebra forces `F=nu^T D^-1 nu/2+V(phi)`.

For constant coefficients the complete off-shell bracket is

    {H[N],H[M]}=ab D_g[v] + integral v^i p^T C D partial_i phi
                 +2ab(1-2lambda) integral v^i nabla_i pi.

Consequently the required algebra is equivalent to `ab=1`, `lambda=1/2`, `CD=I`. Explicit independent periodic witnesses prove necessity. Eliminating momenta yields the full Einstein–scalar/sigma-model action, not only a Brinkmann solution. Newton normalization, Lambda, scalar potential and field-space metric remain undetermined by the algebra.

## Actual execution and scientific boundary

Executed with Python 3.13.5, SymPy 1.14.0 and PyTorch 2.10.0+cpu. Normal and python -O JSON outputs are identical. Automatic differentiation of the unreduced curvature+kinetic+two-scalar Hamiltonian on a periodic Fourier regulator verifies the bracket (all six spatial metric components, fields depending on one spatial coordinate). Correct-family discrepancies at n=17,33,65 are 1.21e-8, 0 and 1.67e-16. Deliberately wrong trace, gravitational, matter and quartic-kinetic terms give nonzero geometric defects, with the derived full bracket accurate below 3.89e-16 on the fine control. Ten exact symbolic identities/structure tests plus the nonzero-curvature control are included.

Executed code SHA256: `d2b83484e840b91e62b8ac2af4155d5fd8c8e5748ee3027f6cbea0b19263da33`; Git blob `615e2b2a0421e11485c9f15497edaa47fd2b37e1`.
Observed result SHA256: `3b13c4146e3fdb3990572ac56db837d2badaf22794eca78ce7f72f159d791204`.

This is a conditional analytic selection theorem with structural controls, NOT an original D0 lattice replay. The actual root history must supply the native symplectic form, normal/tangential generators, admissible local lapse family, local continuum class and controlled bracket limit. None is silently replaced by the displayed ADM variables. Finite all42 roots and their mesh-uniform recovery are not newly proved. No Lean or repository CI was run. `GR_closed=false`.
