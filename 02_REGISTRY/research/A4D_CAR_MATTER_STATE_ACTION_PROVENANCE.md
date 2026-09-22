# E-CARMAT — CAR Matter State / Action Provenance

CONTROL disposition: **ACCEPT AS RESEARCH / CAR-DIRAC-OWNER-FIRST**

Source memo: MEMO_36_A4D_CAR_MATTER_STATE_ACTION_PROVENANCE.

At the audited baseline, \`ArchiveFockState\` is a 16-element basis-label type, not a 16-dimensional amplitude space, and \`carHilbertSpaceDim n\` is only dimension arithmetic. Current main does not yet own the advertised total supported CAR Dirac operator on
\[
ArchiveRolePhaseGroup(N)\times ArchiveFockState
\]
with self-adjointness and parity anticommutation.

Hence the first literal dependency remains the active \`WRK-GEO-CAR-DIRAC-PARITY\`.

Conditional post-worker classification:

- an explicit self-adjoint Dirac operator selects eigenspaces/projectors, not automatically a unique nonconstant physical state;
- zero modes are constant/degenerate;
- evolution requires an initial state;
- spectral projectors select subspaces or mixed states unless an additional ray/preparation rule is owned;
- anomaly-free internal species data are distinct from the 16 geometric Fock/exterior states and should enter as an additional tensor factor, not be identified by cardinality.

The strongest constructive metric route is the exterior/Hodge interpretation of the 16-state fibre. For a full pointwise 4+6 metric \(m\), build a graded Hodge weight \(W_m\), then
\[
\delta_m=W_m^{-1}d^TW_m,\qquad D_m=d+\delta_m.
\]
A finite matter action based on \(D_m\) could then be varied in all ten metric slots to produce
\[
T_N[m,\psi]\in LocalSymRoleField(N).
\]
This full \(W_m/D_m\) owner, its Lorentz/Krein treatment, a selected physical state, and a matter reparametrization law are not yet owned.

Terminal result:
\[
\boxed{\texttt{CAR-DIRAC-OWNER-FIRST}}.
\]
