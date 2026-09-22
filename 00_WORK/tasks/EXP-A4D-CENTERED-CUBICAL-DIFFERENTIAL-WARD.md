# EXP-A4D-CENTERED-CUBICAL-DIFFERENTIAL-WARD

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

Design the literal exterior/cochain differential owner required by E-CARHODGE and determine whether its matter reparametrization/Ward algebra can be made compatible with the already-owned centered metric gauge.

Repository edits: **NONE**.

## Required reading

- \`02_REGISTRY/research/A4D_CAR_HODGE_METRIC_ACTION.md\`
- \`02_REGISTRY/research/A4D_CAR_MATTER_STATE_ACTION_PROVENANCE.md\`
- \`D0.Geometry.ArchiveCARRelations\`
- \`D0.Geometry.ArchiveCubicalCoboundary\`
- \`D0.Geometry.A4DSymRoleCentralDifference\`
- CAR Dirac worker output if landed.

## Literal owner target

Give exact Lean-ready types for:
\[
ArchiveCochainBasis(N)=X_N\times ArchiveFockState,
\]
\[
ArchiveCochain(N)=ArchiveCochainBasis(N)\to\mathbb R
\]
(or \(\mathbb C\) if materially better),
and an actual linear map/matrix \(d_N\).

Start from the forward cubical candidate
\[
d_N=L\sum_r(U_r-I)c_r^\dagger
\]
and prove what exact CAR relations are required for \(d_N^2=0\) and degree raising.

## Centered/Ward problem

The metric gauge owner uses centered derivatives \(D_r\), not \(U_r-I\).

Investigate all honest options:

1. a centered exterior differential built from \(U_r-U_r^{-1}\);
2. a staggered/link-field differential with an averaging map;
3. an exact intertwiner between forward cochains and centered metric variables;
4. a mixed construction where topological \(d^2=0\) remains forward while the Lie/Cartan action is centered.

For each route test:

- nilpotency;
- locality radius;
- degree raising;
- CAR sign algebra;
- adjoint/Hodge compatibility;
- whether a finite Cartan identity
  \[
  L_\xi=d\,\iota_\xi+\iota_\xi d
  \]
  or a corrected discrete analogue exists;
- whether the induced metric-side transformation is literally \`symmetricRoleGradient\` or only an approximation.

Do not fake a Ward theorem by declaring the transformations independently.

## Deliverable

End with:

- recommended differential owner;
- exact theorem signatures;
- whether full CAR anticommutators must be formalized first;
- smallest future worker package;
- exact remaining Ward gap.

## Terminal verdict

Return exactly one:

- \`CENTERED-CUBICAL-DIFFERENTIAL-WARD-REACHED\`
- \`FORWARD-COBOUNDARY-OWNER-FIRST\`
- \`CAR-ANTICOMMUTATOR-OWNER-FIRST\`
- \`CENTERED-NILPOTENCY-NOGO\`
- \`WARD-CARTAN-INTERTWINER-MISSING\`

## Deliverable

\`MEMO_39_A4D_CENTERED_CUBICAL_DIFFERENTIAL_WARD.md\`
