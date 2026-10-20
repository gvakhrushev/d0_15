# Curved soldered sector: exact adjoint class and unavoidable full-grade heat

Research continuation, 2026-10-13. Input SOURCE
`5fdddb1ff924de12b38c886999a40662628cc313`. Original #310 and all G0–G4
obligations remain open. No action, heat selection, torsion equation or
physical postulate is added.

The existing stored soldered operator has a nonempty, exactly classified
selfadjoint sector with nonconstant and genuinely curved metric readouts.
Its scalar compression lands in the existing four-dimensional local
conductance owner. However the full square necessarily mixes scalar and
two-form components on a nonconstant warp. Removing those components changes
even the scalar-sector heat trace at every beta>0. This gives a positive
operator construction and a quantitative obstruction to the proposed scalar
heat identification, rather than another search for an arbitrary preparation.

## 1. Carrier, owners and the actual exterior order

Use the complete carrier `(Z/LZ)^4 x exterior(Role)` with all sixteen exterior components,
`L=N+2>=2`. The principal refinement examples use `L in 4N`. Internal affine
links are identity and the observer is the constant rest observer, whose
induced exterior pairing is counting. Raw solder `F_x=eta+e_x` is invertible;
its row legs are `v_r(x)=eta F_r(x)^T`. The differential and codifferential
are exactly `archiveSolderedForwardDifferential` and
`archiveSolderedCodifferential` in `ArchiveAffineExteriorLink.lean`.

One convention requires an explicit bridge. `ArchiveCARRelations` orders
Jordan–Wigner roles `A,B,C,D`, whereas `ArchiveExteriorFrameLift` actually
installs `LinearOrder.lift' roleCode`, giving `A,C,D,B`. Its introductory
comment claiming the same order is not used as evidence. On occupation set S,

\[
 J_S=(-1)^{1_{B\in S}(1_{C\in S}+1_{D\in S})},\quad
 C_r^{ext}=J C_r^{JW}J,\quad A_r^{ext}=J A_r^{JW}J,\quad J^2=I. \tag{1}
\]

This is the wedge reordering sign, proved by counting inversions. The exact
certificate checks every entry and uses the actual exterior order for the
new operators. The preceding homogeneous packet used the ABCD matrix basis;
its CAR, Gram, square and trace formulas remain valid after (1), with its
Gram conjugated by the same J. They are not literal entrywise equal to the
other basis without this conversion. The new Lean capsule checks the
integer/real CAR order conversion; the abstract exterior-basis identification
retains its analytic status.

## 2. Complete selfadjoint class for this actual interface

Let `S_r` be forward site shift, `nabla_r^+=L(S_r-I)`. Write creation and
contraction multiplication operators as `M_Cr` and `M_Ar`. Local counting
adjointness gives `M_Cr^*=M_Ar`. The actual owners give

\[
 d=L\sum_rM_{C_r}(S_r-I),\quad
 \delta_{stored}=L\sum_rM_{A_r}(S_r^{-1}-I),
\]
\[
 \delta_{stored}-d^*=L\sum_r
 (M_{A_r}S_r^{-1}-S_r^{-1}M_{A_r}).                         \tag{2}
\]

The exact classification is

\[
 \boxed{D=d+\delta_{stored}=D^*\quad\Longleftrightarrow\quad
       v_r(x)=v_r(x-e_r)\ \hbox{for every }x,r.}             \tag{3}
\]

Sufficiency follows directly from (2). For necessity, degree raising and
degree lowering cannot cancel each other in `D-D*`, so `delta_stored=d*`.
At fixed x the four predecessor sites `x-e_r` are distinct for every L>=2.
The coefficient at each is contraction by `v_r(x)-v_r(x-e_r)`; contraction
is injective in its vector, as seen on one-forms. Each difference vanishes.
This also proves (3) for L=2; coincidence of forward/backward neighbors in
one direction does not produce an exception. L=1 is outside this owner.

Equation (3) classifies the stated fixed-observer, flat-internal-link,
counting-pairing interface. It is not a classification of every native
connection/pairing. It changes no stored definition.

## 3. The admitted tangent is not all local metric probes

At the flat raw reference `F=eta`, one has `delta q=delta F+delta F^T`.
For Fourier frequency k, condition (3) allows row r of `delta F(k)` precisely
when `k_r=0`. If m coordinates of k are zero, the full metric image consists
of symmetric H such that

\[
 H_{rs}=0\quad\hbox{whenever }k_r\ne0\hbox{ and }k_s\ne0.
\]

Its dimension is `m(9-m)/2`, and the raw-solder kernel has dimension
`m(m-1)/2`. The kernel is the antisymmetric block on the m available rows;
it is not declared native gauge. Thus ranks for m=0,1,2,3,4 are 0,4,7,9,10.
For complex Fourier modes these are complex dimensions; conjugate modes are
paired for real fields. Summing over the real lattice gives raw dimension
`16L^3`, metric image `16L^3-6L^2`, kernel `6L^2` (at L=4: 1024,928,96).

Consequently the positive curved sector below does not supply every smooth
ten-component local probe. The earlier all-ten **homogeneous** tangent is
the k=0 case and remains valid. A full local source requires the larger
native link/pairing preparation, not extrapolation from this restriction.

## 4. Explicit curved metric with the stored adjoint unchanged

For any positive periodic sequence a, set

\[
 F_x=\operatorname{diag}(1,-a(x_0),-1,-1),\quad n=e_0,
 \quad q_x=F_x\eta F_x^T=\operatorname{diag}(1,-a(x_0)^2,-1,-1). \tag{4}
\]

Every row is constant along its own coordinate. Therefore (3) applies even
when a is nonconstant. Coordinate links are **not** identity: they are
`D_xy=F_x F_y^-1`, satisfying `D_xy q_y D_xy^T=q_x` identically. The raw
internal links remain identity. Choose also the separate row-pull argument
`Rpull=I` of `transportedSolderCenter`. Its rowwise transported center equals
F by the own-axis constancy, so the transported metric is also q; there is
no discarded centering defect. The row pull and affine links have different
types; their physical identification is not inferred from these choices.

Take the fixed smooth periodic profile `a(t)=2+cos(2 pi t)` and sample it at
`t=x_0/L`. It stays in [1,3] at all levels. Under the declared metric readout
`g=q`, use
`R^rho_(sigma mu nu)=partial_mu Gamma^rho_(nu sigma)-partial_nu Gamma^rho_(mu sigma)+Gamma^rho_(mu lambda)Gamma^lambda_(nu sigma)-Gamma^rho_(nu lambda)Gamma^lambda_(mu sigma)`.
The only needed Christoffel components are `Gamma^0_11=a a'` and
`Gamma^1_01=Gamma^1_10=a'/a`, giving

\[
 R_{0101}=aa'',\qquad R=-2a''/a,\qquad R_{0101}(0)=-12\pi^2\ne0. \tag{5}
\]

The coordinate links telescope around every plaquette, so their holonomy
is identity. They are metric-compatible but are not thereby Levi-Civita.
Nonzero curvature in (5) is the curvature of the metric readout, not of the
flat internal connection. No torsion equation, Palatini solution, causal time
interpretation or on-shell claim follows. The profile supplies a nonempty
curved **kinematic** operator class with uniform nondegeneracy.

## 5. Exact scalar bridge and the term it cannot erase

Let `K_r=C_r nabla_r^+ + A_r (nabla_r^+)^*` be the constant single-direction
Hodge/CAR operators. With M multiplication by a(x_0), the same stored operator
and its full square are

\[
 D=K_0+MK_1+K_2+K_3,
 \quad \Delta=D^2=K_0^2+M^2K_1^2+K_2^2+K_3^2+[K_0,M]K_1. \tag{6}
\]

All spectator grades are retained. The commutator vanishes only in the
appropriate constant-coefficient limit; it cannot be replaced by a frozen
scalar Fourier symbol.

Let P project onto the scalar exterior degree. Its compression is exactly

\[
 A=P\Delta P=\nabla_0^{+*}\nabla_0^+
  +a(x_0)^2\nabla_1^{+*}\nabla_1^+
  +\nabla_2^{+*}\nabla_2^++\nabla_3^{+*}\nabla_3^+.           \tag{7}
\]

For L>=3 this is a four-dimensional nearest-neighbor conductance Laplacian.
Via the actual `archiveRolePhasePointGroupEquiv`, its difference from the
flat metric-scaled `archiveProductLaplacian` is precisely
`archiveLocalLaplacianForward(delta w)`, where `delta w=a(t)^2-1` on axis-1
edges and zero on other edges. The owner's `archiveMetricLaplacianScale=L^2`
fixes the normalization. At L=2 the oriented two-neighbor stencil doubles
the undirected edge contribution; the certificate explicitly rejects using
the L>=3 identification without that factor.

However the scalar subspace does not reduce Delta. Its entire outgoing block
is the two-form component

\[
 B=(I-P)\Delta P=d^2P
  =C_0C_1 L^2M_{a(t+1)-a(t)}S_0(S_1-I),
 \quad \boxed{\|B\|_{HS}^2=2L^7\sum_t(a(t+1)-a(t))^2.}      \tag{8}
\]

Each scalar output row has two distinct entries of magnitude
`L^2|a(t+1)-a(t)|`; there are L^3 rows at each t. This proves (8) for every
L>=2. Therefore scalar reduction holds exactly when a is constant. At L=4,
`a=(3,2,1,2)` and the norm squared is 131072. For the scalar input
`cos(pi x_1/2)`, the two-form `(01)` output at `x_0=x_1=0` is 16.

This is an explicit composition of owned finite objects. It is not an
identification of their entire Hilbert spaces or heat operators.

## 6. Full heat differs at every beta, with a quantitative lower bound

Let `0<=Delta<=M0 I`, beta>0. Compression A has spectrum in [0,M0]. Then

\[
 \boxed{\operatorname{Tr}(P e^{-\beta\Delta}P)
      -\operatorname{Tr}_P(e^{-\beta A})
  \ \ge\ \frac{\beta^2e^{-\beta M_0}}2\|B\|_{HS}^2.}         \tag{9}
\]

Here the first trace is the scalar-sector trace of the **full** heat; it is
not the full partition trace with the other grades added. To prove (9), choose
an orthonormal eigenbasis u_j of A with eigenvalues a_j. The spectral measure
of Delta in u_j has mean a_j and variance
`<u_j,Delta^2 u_j>-a_j^2=||B u_j||^2`. The scalar function exp(-beta x) has
second derivative at least `beta^2 exp(-beta M0)` on [0,M0]. Apply its scalar
Taylor lower bound and sum. No operator-convexity claim about exp is used.
Equivalently, the exact moment defect is
`P Delta^2 P-A^2=B*B` on the scalar space.

Thus (9) is strictly positive at every beta>0 for every nonconstant discrete
warp. It excludes an exact scalar heat intertwiner/compression identity for
this class. It does not exclude an approximate continuum readout.

One valid finite bound is `M0=4L^2(3+max a)^2`, obtained from
`||K_r||<=2L`. At `L=4,a=(3,2,1,2),beta=log(2)/32`, (9) is at least
`log(2)^2/2^66>0`. This bound is intentionally finite. For the smooth cosine
profile, `||B||^2=4L^8 sin^2(pi/L)` for L>=3; its normalized raw HS norm
does not tend to zero, and exp(-beta M0) degenerates with refinement. Neither
fact proves a thermal continuum obstruction or the required uniform transfer.

## 7. Complete comparison with the existing diagonal conformal family

Another real owner is `ConformalLaplacianTrace.weightedLaplacian`:
`L_rho=W_rho L_flat W_rho`, `W_rho=diag(rho^-1/2)`, rho>0. This is a diagonal
congruence, not the edge-conductance construction (7).
In this section L>=3 and L_flat is the metric-scaled native undirected
product graph. For L=2 its undirected edge normalization instead gives
`A_(a=1)=2 L_flat`, and the equality below has rho=1/2. The nonconstant-warp
exclusion still holds, but the constant normalization must not be copied.

For the connected flat four-role graph, `ker L_flat=R 1`: the quadratic form
is the sum of edge-difference squares, and coordinate steps connect all
vertices. If `A=W_rho L_flat W_rho`, then A1=0 forces
`L_flat(W_rho 1)=0`. Hence W_rho=wI. The unchanged axis-0,2,3 edge entries
force w^2=1; axis-1 entries then force a(t)^2=1. With a>0,

\[
 A_{warp}=W_\rho L_{flat}W_\rho\quad\Longleftrightarrow\quad
 a\equiv1,\ \rho\equiv1.                                 \tag{10}
\]

This covers **all positive rho** at the fixed metric scale and fixed flat
input L_flat. It does not exclude substituting a different supplied L, but
that substitution would need its own native selection. The generic wrapper
does not perform it. No full-core NO-GO follows from (10).

## 8. What this resolves and what the next proof must retain

The moving-adjoint defect does not prohibit every nonconstant metric: (3)–(5)
construct and classify an actual surviving interface. Its scalar part has a
genuine typed native conductance owner, with exact normalization. But (8)–(9)
force the remaining degrees back into any full-heat comparison, and (10)
prevents silently substituting the existing conformal family.

For an admissible warp variation b(t), `delta D=M_b K_1` and, conditionally
on this square being the action's actual heat,
`delta B_H=-2 Tr(rho_beta(Delta) D M_b K_1)`. This keeps the commutator modes.
It does not supply arbitrary local metric variations or the feedback/source
part of the full stationary system. The primary next arrow is still the
native map to the **same full** Delta,P,U,G and its admitted variations and
refinement. It must use the grade-mixing heat or prove a controlled reduction;
compression (7) alone is insufficient. Native source/Ward, quantitative
transfer, curved joint roots and soundness/recovery remain open.

## 9. Golden depth calibration retained from the existing owner

The user's older delta notes match `Core.Delta` and
`Claims.DimLadderCompact`: with p=phi^-1,
`delta0=p^3/2` and `Q(D)=2 delta0 phi^(D-1)=phi^(D-4)`.
The exact scalar ladder is already proved for every integer D. Its unit
crossing at D=4 is not a dynamical change of recurrence.

The sharper existing link is
[Fibonacci record activation](A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md),
sections 2 and 6: three inclusions (four levels including the initial level)
are necessary and sufficient for that covariant full-record representation
at every initial n. The prepared corner has `tau(e)=p^6=4 delta0^2`, and
the two-tick feedback coefficient is `4p^3=8 delta0=1-4 delta0^2`.
This gives an actual apparatus threshold and exact shared normalization.
It does not identify four levels with the four coordinate axes in (4).
No new threshold law or coefficient is installed.

The Vieta pair implies both quadratic relations, so the four equations are
not independent scalar invariants. The half-difference cascade has ratio
delta0, the recorded diagonal contrast has ratio 2 delta0, and the tick
amplitude has ratio p. These are different stated observables; one scalar
recursion cannot be substituted for the full heat/refinement arrow in
section 8. The present packet preserves the already proved golden apparatus
and addresses the geometric heat side of that missing joint arrow.

## 10. Evidence and reproducibility

Run `python3 02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat_check.py`.
The immutable ledger pins this proof, source owners, implementation, exact
checks and the narrow Lean receipt. Finite blocks are constructed in the
actual exterior order; all sixteen exterior components, endpoint signs, graph scale and
the two-form coupling are retained. The analytic proofs above cover every
stated level/class; finite witnesses are additional checks, not substitutes
for that quantification.

The research Lean capsule proves its named matrix, CAR-order and variance
kernels. Its receipt records actual declarations, axioms and compiler input
provenance. Abstract exterior/counting adjointness, the complete Fourier
classification, curvature and scalar strong-Jensen estimate retain their
explicit analytic/certificate status. No supported CORE or claim is changed,
and no D0.All or physical closure is asserted.
