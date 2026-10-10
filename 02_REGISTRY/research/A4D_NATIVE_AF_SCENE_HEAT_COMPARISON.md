# The actual scene-to-AF comparison: compression and heat are different gates

Existing parent #310. Input SOURCE
`833372049d1cbde14f51bcbc3ca06bb017025cb8`.
Status: a quantitative classification of the literal phi-martingale heat
comparison with the owned **combinatorial** scene Laplacian. This is a
proof-base repair and a completed comparison interface, not native T0.

The [constructed Fibonacci inclusion](A4D_NATIVE_GOLDEN_COST_REFINEMENT.md)
maps one AF level into the next. It does not supply the scene-to-AF map
required by the old Feshbach transport. Dimension inequality alone excludes
unitary identification of entire carriers; it does not exclude a rectangular
coisometry or a Laplacian compression. We determine those gates separately
for the literal internally sourced martingale scale.

The result is two-sided. On the full AF carrier of dimension 233 an isometry
can give **exact scene Laplacian compression**. Nevertheless, for every AF
level, every positive overall scale and every isometry J into a heat
operator with the literal phi-squared ladder spectrum,

\[
                  \|H J-JL_{scene}\|\ge {13\over2}.       \tag{1}
\]

The bound is sharp on the full 89-dimensional AF carrier. In particular
there is no exact heat-semigroup compression in this complete operator
class. The weak and sharpness witnesses are mathematical comparisons,
not native actuation, field preparation or solutions of the full price.

## The operators and the complete class being classified

Use the existing unweighted scene K(9,11,13), all 33 vertices and all 359
edges. Its combinatorial Laplacian is `L=D_degree-A`. This is the operator
in `VNext.AFD0LaplacianComparisonNoGo` and `Synthesis.SceneHeatKernel`.
It is **not** the degree-normalized `I-D_degree^-1 A` in the shared-scene
price calculation. The latter operator is outside the result below.

Let `P_zone` average within each of the three zones and `P_const` average
over all vertices. The five mutually orthogonal spectral projections are

\[
 P_0=P_{const},\quad
 P_{20}=I_{13}-{\mathbf1_{13}\mathbf1_{13}^T\over13},\quad
 P_{22}=I_{11}-{\mathbf1_{11}\mathbf1_{11}^T\over11},\quad
 P_{24}=I_9-{\mathbf1_9\mathbf1_9^T\over9},\quad
 P_{33}=P_{zone}-P_{const}.                                \tag{2}
\]

The middle three matrices are extended by zero outside their zones.
Their ranks are respectively `1,12,10,8,2`, and they sum to the identity.
Direct multiplication by the actual adjacency gives

\[
              L=20P_{20}+22P_{22}+24P_{24}+33P_{33}.        \tag{3}
\]

For example, the difference of two vertices in the 13-zone has eigenvalue
20, the analogous 11-zone difference has eigenvalue 22, and a zone-constant
vector with total sum zero has eigenvalue 33. These are actual eigenvectors;
the argument does not merely quote a list of multiplicities.

The AF side uses the actual compatible GNS inclusions already constructed.
The nested orthogonal level spaces have dimensions `2,5,13,34,89,233,...`.
The martingale increments therefore have dimensions `3,8,21,55,144,...`.
For the literal scale `lambda_j=lambda_0*phi^j`, the square of a martingale
Dirac has positive spectrum in

\[
                \{c\,phi^{2j}:j\in\mathbb N\},\qquad c>0. \tag{4}
\]

The all-level forcing of this scale is conditional on the existing
`InternallySourced` premise; that premise is not inferred from a name or
from the existence of a trace. The comparison theorem actually covers
**every finite self-adjoint H** whose spectrum is contained in (4) together
with zero: arbitrary multiplicities, arbitrary zero space, arbitrary basis
and every positive c. Thus it covers all finite levels of the stated
martingale class, rather than just a hand-picked level or an AF basis.
All operator directions remain present. No auxiliary spectral levels
outside (4) are supplied.

For the two comparison witnesses below take the root-zero convention:
H vanishes on the full two-dimensional initial AF space and equals
`c*phi^(2j)` on increment j, for j=1,...,N. This defines a member of the
quantified comparison class. It is not a derivation of a physical kernel
convention; the obstruction permits any zero multiplicity. The second
root direction is retained even when J uses only one root vector.

## An all-level, scale-uniform separation

Write `b=phi^2`. The golden identity implies `b>64/25`. Two distinct
positive values of (4) differ by a multiplicative factor at least b.
Suppose three such spectral values x,y,z were simultaneously within
`13/2` of 20,22,33. Then

\[
 x\in(27/2,53/2),\quad y\in(31/2,57/2),\quad
 z\in(53/2,79/2).                                         \tag{5}
\]

The two possible ratios between x and y are both below `64/25`; hence
x=y. Likewise both possible ratios between y and z are below `64/25`
(the larger relevant bound is `79/31<64/25`), hence y=z. But the first
and third intervals in (5) are disjoint. This is a contradiction. Zero
cannot be any of these approximating values. Consequently

\[
 \max_{a\in\{20,22,33\}}\operatorname{dist}(a,\sigma(H))
                  \ge13/2.                              \tag{6}
\]

This argument is independent of the number of levels, c and eigenvalue
multiplicities. For a unit scene eigenvector v of eigenvalue a, isometry
of J gives `||Jv||=1`, and the finite spectral theorem gives

\[
 \|(HJ-JL)v\|^2=\|(H-a)Jv\|^2
 =\sum_{\mu\in\sigma(H)}(\mu-a)^2\|P_\mu Jv\|^2
 \ge\operatorname{dist}(a,\sigma(H))^2.                   \tag{7}
\]

Equations (6)--(7) prove (1). No dimension argument or convergence of a
numerical singular-value scan is used. A fixed positive target calibration
`a0*L` changes the bound to `a0*13/2`, by applying the result to `H/a0`.
This does not identify degree normalization with a scalar calibration.

The constant is sharp, even while all AF modes remain. At level 4 the
new increment has dimension 55. Set its ladder energy to `53/2` using
one positive overall scale. Embed the 32-dimensional nonconstant scene
space isometrically into this increment, and its constant line into an
existing AF zero line. The residual on the five scene eigenspaces is
`0,13/2,9/2,5/2,-13/2`, up to sign convention. Its operator norm is exactly
13/2. All other AF levels and every unused direction of the 55-dimensional
increment remain part of H and its heat trace. This proves nonemptiness
and sharpness of the comparison class; it does not declare the embedding
physically executable or specify a native scale.

## Exact compression still exists on the literal ladder

For a constructive negative control against the stronger nonexistence
claim, use the full AF level 5 (dimension 233). Its consecutive increments
of dimensions 55 and 144 may carry energies

\[
                       l=13,\qquad u=13phi^2.             \tag{8}
\]

This uses a single overall scale in (4). Each has room for 32 orthonormal
vectors, one for every nonconstant scene direction. For a scene eigenvector
of eigenvalue `a in {20,22,24,33}`, define

\[
 w_a={a-l\over u-l},\qquad
 Jv=\sqrt{1-w_a}\,e_{l,v}+\sqrt{w_a}\,e_{u,v}.            \tag{9}
\]

All weights are strictly between zero and one: `13<20<=a<=33<13phi^2`.
Different scene vectors use orthogonal pairs. Send the scene constant to
an existing zero vector. Hence `J*J=I_33` and

\[
                         J^*HJ=L.                        \tag{10}
\]

In a spectral basis the map (9) is explicit. Returning to the actual
scene is legitimate by the complete projector decomposition (2). The AF
increment decomposition is supplied by its actual GNS inclusions; its
basis choices are comparison data, not a forced native encoding. No AF
complement is deleted or reset. This is a genuine coisometry `C=J*`
with exact Laplacian compression on the declared literal ladder, even
though no AF level has dimension 33.

This witness also shows exactly what the weaker gate loses. On each
nonconstant scene eigenvector,

\[
 J^*H^2J-L^2=(a-l)(u-a)>0.                                \tag{11}
\]

The left side denotes its eigenvalue on that vector. The quadratic
defect is computed from the same two weights, not fitted separately.
The original scene matrix, every AF mode, the scalar zero line and the
chosen common scale are all retained in this comparison.

## Heat compression fails; a Feshbach memory relation is still possible

For finite self-adjoint H and L and an isometry J, suppose

\[
             J^*e^{-tH}J=e^{-tL}                          \tag{12}
\]

for all t in an interval starting at zero. Differentiating the finite
matrix exponential twice gives `J*HJ=L` and `J*H^2J=L^2`. With the first
identity and `J*J=I`, direct multiplication gives

\[
 (HJ-JL)^*(HJ-JL)=J^*H^2J-L^2.                            \tag{13}
\]

Thus (12) forces `HJ=JL`. This contradicts (1) for the stated literal
phi-squared heat class. Equation (11) is an explicit hostile control:
the entire first compression matches, while its second heat derivative
does not. Equality of the weaker compression cannot be used as a heat
law or to discharge a stronger Feshbach compatibility requirement.

This does **not** rule out a Feshbach relation that keeps its memory term.
The weak witness provides an exact coupled block, not a freely varied
archive energy. In the basis consisting of Jv and its orthogonal partner,
write `d=l+u-a` and `k=sqrt((a-l)*(u-a))`. Up to the sign of the partner,
the full two-dimensional block is

\[
 H_a=\begin{pmatrix}a&k\\k&d\end{pmatrix},\qquad
 a+d=l+u,\quad ad-k^2=lu.                                  \tag{14}
\]

Conversely, every self-adjoint two-dimensional block with eigenvalues
l,u and retained diagonal a has this d and this absolute coupling; a
complex off-diagonal phase is not fixed by these two identities. For
`l<a<u` the coupling is nonzero. Let `j_a=(1,0)^T` be the retained
inclusion in this two-dimensional basis. Thus the complete two-dimensional
spectral fiber, not an independently chosen hidden-energy block, has
the exact compressed resolvent

\[
 j_a^*(H_a-sI)^{-1}j_a
 =\left(a-s-\frac{k^2}{d-s}\right)^{-1}
 =\frac{d-s}{(l-s)(u-s)}.                                  \tag{15}
\]

The Schur expression requires `s!=d`; the last expression extends it
where the full resolvent exists (`s!=l,u`). Its memory/self-energy term
is `k^2/(d-s)`. It is determined by the same coupled block and is not
zero. A heat-semigroup comparison that discards this term is a stronger
and different requirement than exact Feshbach elimination.

If l,u are fixed while a changes, then `delta d=-delta a` and
`delta |k|^2=(l+u-2a)*delta a`. The memory term generally changes, but
the complete two-mode heat trace remains
`exp(-beta*l)+exp(-beta*u)` at fixed beta. With all other AF modes fixed,
the full heat price therefore has zero derivative on this fiber. One
cannot retain only `delta d` as a source while omitting the linked
coupling variation. This does not assert that the feedback or matter
price is fixed, or that the spectral-fiber curve is a native metric
variation. The q,D,b,m readout and native admission still have to be
proved. The same warning applies to any proposed use of (14) as F:
it is a coupled comparison relation, not yet the requested own law.

The old `af_skips_d0_dim_total` theorem really proves a dimension
inequality; the old level-3 multiplicity theorem concerns a reduced
unitary comparison. Neither is a proof that no rectangular compression
exists. Equations (8)--(10) supply the countercontrol on the literal
ladder; (1) supplies the all-level heat obstruction using actual spectral
content. No canonical/M1 admission of the weak witness is inferred.

## Consequence for the native preparation problem

The constructed AF inclusion and forced trace cannot, by themselves,
discharge the **heat-semigroup** scene comparison on this literal scale.
An exact weak Xi exists mathematically in the stated class; physical
admission and a stronger operator law remain separate obligations.
Feshbach elimination with its retained memory is explicitly compatible
with the weak witness, so no Feshbach no-go follows from the heat gap.
This class is fully quantified. The weak-comparison and sharpness fibers
are explicitly nonempty at levels 5 and 4 respectively.

The result does not exclude arbitrary AF scales, other already-owned
heat operators, the degree-normalized scene operator, nonlinear state
readouts, or native finite paired contrasts. In particular an operator
norm gap is not an action-contrast error bound or a physical no-go.
No new generator, temperature, action, state selector or source is
installed. T0--T3, all 44 dependency nodes and the original #310/#202/#317
terminals remain open. A common admitted preparation and its constrained
price variation still have to be derived.

## Verification scope

The companion Lean capsule proves the scalar all-index gap, the incompatible
three-band theorem, the exact 13/2 sharpness arithmetic, both moments of
the mixing control and the actual finite AF dimension facts. The operator
norm, spectral-subspace embeddings and matrix-exponential implications
have analytic proofs above. Exact controls reconstruct the scene graph
and all five projectors, and retain the full 89/233-dimensional spectral
models. No matrix or native admission theorem is claimed merely from
the scalar declarations. Verification receipts record the completed
build, executed controls and rejected mathematical mutations.
