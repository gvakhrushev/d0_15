# Existing affine-CAR transport is blind to link shifts

**Exact scoped Lean result, 14 October 2026.** The affine-CAR link and both
existing linked/soldered Dirac operators depend only on the linear parts of
their affine connections. At fixed linear links, raw coframe and observer,
changing any affine translation leaves these operators exactly unchanged.
This closes the direct route from the existing affine-CAR transport to the
candidate same-edge shift readout. It is not a whole-core no-go.

## Native variables and the owned operators

The complete joint kinematic quotient uses an affine link
\(A_e=(U_e,a_e)\) and the coframe \(F_x\), with
\[
q_x=F_x\eta F_x^T,\qquad D_e=F_xU_eF_y^{-1},\qquad
b_e=F_xa_e,\qquad m_x=\rho(F_x)\psi_x.
\]
For fixed \(F_x\), changing the affine shift \(a_e\) changes the native
coordinate \(b_e\); the quotient imposes no further kinematic constraint on
\(b_e\). These are admissible kinematic variations, not yet a physical
transition law.

The existing CAR pull link is
`archiveAffineExteriorLink A x r = archiveExteriorFrameLift (A x r).lin`.
Its primary owner already proves
`archiveAffineExteriorLink_shift_irrelevant`: connections with equal linear
parts induce equal CAR pull links. The new Lean declarations extend this
identity to both complete operators:

```text
archiveAffineLinkedHodgeDirac_shift_irrelevant
archiveSolderedDirac_shift_irrelevant
```

For every cochain, and for every fixed solder/observer in the soldered case,
if \((A_e).lin=(B_e).lin\) on every edge, then the two complete Dirac outputs
are equal. The proofs are in
[`ArchiveAffineExteriorLink.lean`](../../03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean)
and compile with the narrow target
`lake build D0.Geometry.ArchiveAffineExteriorLink`. `#print axioms` reports
only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no
additional axiom or physical assumption is introduced.

## Consequence for the gravity candidate

The conditional candidate uses
\[
n_e=\frac{b_e}{\sqrt{b_e^TG(q,m)b_e}}
\]
to turn each existing oriented shift into the record ray. The two existing
affine-CAR Dirac operators cannot derive this map: at fixed \(F,U_e,m\),
their outputs do not respond when \(a_e\), hence \(b_e\), changes. Therefore
the positive metric covector computed for the candidate v3 cost remains
conditional on a separate local record/preparation owner that actually reads
\(b_e\).

This result does **not** classify \(b_e\) as gauge, exclude other
field-dependent operations, or prove that the full native core has no such
owner. The next search is limited to an already-owned local record or
preparation law whose inputs include the affine shift. If no such owner is
found, that absence alone is not a full-core obstruction. The original #310,
#202 and #317 terminals, physical source/Ward, curved roots and global GR
closure remain open.
