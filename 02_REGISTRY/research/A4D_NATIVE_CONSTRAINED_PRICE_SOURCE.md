# Native constrained price: intrinsic source chart and a stationary feedback contribution

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input SOURCE: `0545eaf95ac3857b30c43f266311c80c1d751d01`;
main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **partial T1 computation, not a native metric source or a parent terminal**.

This computes two reusable parts of the proposed constrained-price arrow:
(1) the complete intrinsic cotangent normal form on the existing joint carrier;
(2) vanishing first variation of the two-step feedback price at the ordinary
and recorded golden operations, throughout the fixed-golden-compression
orthogonal completion class, with arbitrary finite archive size.
The second conclusion concerns the scalar price differential. The feedback
operator itself can have a nonzero first jet there.

The [joint quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md) supplies the carrier.
The [composed price](A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md) supplies the
orthogonal completion class, actual native operation bindings and the price.
No new action is introduced. The [core-to-stress arrow](A4D_CORE_TO_STRESS_ARROW.md)
remains a strategy: it does not establish the hypotheses that make a surviving
covector native or equal to `rho0`.

## 1. All joint variations and their intrinsic covector

For one edge write (Dq_tD^T=q_s), with symmetric invertible (q_s,q_t)
and invertible (D). All allowed first jets satisfy

\[
DV_tD^T+Wq_tD^T+Dq_tW^T=V_s.                 \tag{1}
\]

Put (R=q_s^{-1}D). Then (Rq_tD^T=I). With
(Z=Wq_tD^T), (1) is exactly (Z+Z^T=V_s-DV_tD^T). Consequently

\[
 W=\left[\tfrac12(V_s-DV_tD^T)+K\right]R,
 \qquad K^T=-K.                            \tag{2}
\]

This parameterization is complete and unique in (K). Both endpoint metric
jets are arbitrary symmetric matrices. In four dimensions this gives ten
metric slots per site and six free link slots per edge, in addition to every
retained affine/matter direction. Those six directions belong to the joint
quotient; they are not discarded as local Lorentz gauge.

Use the Frobenius pairing only as coordinates for a covector,
(langle A,V\rangle=\operatorname{tr}(A^TV)). Given the actual action
partials (A_s,A_t,B), set (M=BR^T). Direct substitution in (2) gives

\[
\begin{aligned}
\langle A_s,V_s\rangle+\langle A_t,V_t\rangle+\langle B,W\rangle
={}&\langle A_s+\tfrac12 M,V_s\rangle\\
 &+\langle A_t-\tfrac12D^TMD,V_t\rangle+\langle M,K\rangle. \tag{3}
\end{aligned}
\]

Symmetrize the two metric coefficients and antisymmetrize the link coefficient
when writing their ten and six independent components. Sum incoming/outgoing
contributions at every site. Equation (3) is the restricted covector itself;
it does not select an orthogonal projection or remove a link equation.
For symmetric metric coordinates the packed off-diagonal dual weight is two.
Affine/matter covector terms are appended without change.

An off-constraint extension (langle\Lambda,Dq_tD^T-q_s\rangle), with
symmetric (Lambda), changes ambient coefficients by

\[
 A_s\mapsto A_s-\Lambda,\quad
 A_t\mapsto A_t+D^T\Lambda D,\quad
 B\mapsto B+2\Lambda Dq_t.
\]

It changes (M) by (2\Lambda). Both metric coefficients in (3) and the
skew link coefficient are therefore unchanged. This proves extension
independence. It also shows exactly why the ambient (q)-partial is not the
native source. Two lifts of the same metric probe differ by the last term
in (3); lift independence holds precisely when the link covector annihilates
that fibre. It cannot be assumed before the corresponding link equation or
native lift law is established.

The physical transported readout is still (widehat q=B(D)qB(D)^T), where
this (B(D)) is the established readout matrix, not the covector (B) above.
Its derivative includes both (delta B(D)) terms. Equation (3) is first
written for raw (q); it does not silently replace transported metric probes.

## 2. The full archive class of the two-tick price

Fix (a,p,z), with (a^2=p, p+p^2=1, p>0, 0<4zp^3<1).
In active/archive coordinates the already classified operator is

\[
 U=\begin{pmatrix}aI&-pR_a^T\\pS_a&aS_aR_a^T+V_a\end{pmatrix},
 \quad U^TU=I.                             \tag{4}
\]

Here (R_a,S_a:\mathbb R^n\to\mathbb R^m) are isometries;
(V_aR_a=0, S_a^TV_a=0, V_a^TV_a=I-R_aR_a^T,
V_aV_a^T=I-S_aS_a^T). Every archive row remains in (4).
These subscripts distinguish archive embeddings from the chart matrix (R)
in (2). The prior completion theorem proves this whole fixed active-block
class; it does not prove that this class exhausts all native field variations.

Let (H=R_a^TS_a). The full two-step retained block and feedback are

\[
 A_2=(U^2)_{11}=a^2I-p^2H,\qquad
 F_2=(U^2)_{21}^T(U^2)_{21}=I-A_2^TA_2.    \tag{5}
\]

The archive complement is eliminated here by the exact full orthogonality
identity, not by dropping a determinant factor. The existing price is
(J_2=-\log\det(I-zF_2)). The active determinant equals the determinant on
the full active/archive space after its feedback-zero block is retained.
This calculation concerns that particular full feedback determinant; it is
not permission to drop archive determinants in another Schur reduction.

## 3. First variation at the actual golden operations

Assume at the base point

\[
 S_a=R_aH,\qquad H^T=H,\qquad H^2=I.        \tag{6}
\]

The ordinary golden operation has (H=I). The actual
`GoldenCoherentMemory.fullStep` has (H=X=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)).
The new Lean capsule checks the literal recorded-operator block identity.
Isometric embeddings of these active operations into larger full archives
satisfy the same calculation.

Let a differentiable curve stay in (4), with fixed (a,p,z), and denote
first jets by dots. Differentiate both isometry equations. Then

\[
 \dot H=\dot R_a^TS_a+R_a^T\dot S_a,\qquad
 \dot H^TH+H^T\dot H=0.                   \tag{7}
\]

For clarity, the second identity is the sum

\[
 H^T(\dot R_a^TR_a+R_a^T\dot R_a)H+
 \dot S_a^T(R_aH)+(R_aH)^T\dot S_a=0.
\]

Thus (H\dot H) is skew. Symmetric times skew has zero trace, so

\[
 \operatorname{tr}\dot H=\operatorname{tr}(H\dot H)=0.
\]

Differentiating (5), with all multiplication orders retained, gives

\[
 \dot F_2=a^2p^2(\dot H+\dot H^T)
          -p^4(\dot H^TH+H^T\dot H)
          =p^3(\dot H+\dot H^T).          \tag{8}
\]

At the base, (F_2=2p^3(I+H)). Set (c=2zp^3). Its actual resolvent is

\[
 (I-zF_2)^{-1}=\frac{1-c}{1-2c}I+rac{c}{1-2c}H. \tag{9}
\]

The denominator is positive by the stated price domain. Equations (7)–(9)
therefore prove

\[
 \boxed{\dot J_2=z\operatorname{tr}((I-zF_2)^{-1}\dot F_2)=0.} \tag{10}
\]

This is an all-size statement, not an inference from finite ranks. The
finite-dimensional analytic derivative used in (10) follows directly from
multilinearity of the determinant: for invertible (Q),
(det(Q+tE+o(t))=det Q[1+t\operatorname{tr}(Q^{-1}E)+o(t)]).
Differentiate the real logarithm on the positive determinant domain, using
(E=-z\dot F_2). No spectral commutativity of the curve is required.
The capsule proves (5), (7)–(9) and the zero trace in (10); the general
`HasDerivAt` theorem for this analytic determinant/log step is **not** claimed
to be kernel-formalized in this packet.

For any actual native operator map whose first jets stay in this declared
class at these base points, (10) pulls back to zero on every joint tangent
(1). The map does not have to be guessed to establish this conditional
vanishing contribution. Admission into that class still needs its owner.

## 4. Sharp limits of the result

The theorem is local at (6). The already owned orthogonal Cayley family
(H(t)=(1+t^2)^{-1}\left(\begin{smallmatrix}1-t^2&-2t\\2t&1-t^2\end{smallmatrix}\right))
has price (-2\log(1-4zp^3/(1+t^2))), whose derivative at (t=1) is
(-4zp^3/(1-2zp^3)\ne0). This is a protected exception to an all-state
source-zero claim. Physical admission of that curve is a separate prior
obligation. A valid tangent at (H=X) can also have (dot F_2\ne0)
while (10) vanishes: scalar-price stationarity is not operator stationarity.

Moving the pairing/readout is covered only if an actual differentiable
co-moving frame preserves the price and the fixed golden compression in
(4). That condition is not silently assumed for all ((q,D,b,m)) variations.
Changes of (p,z), active rank, preparation law or heat carrier do not fall
under (10) merely because the base operation is golden.

In particular, the price difference (-\log(1-4zp^3)) is not the whole
bootstrap. Its nonzero value supplies no missing derivative. The full price
still has its heat differential, any remaining admitted feedback contributions,
all moving-pairing terms, and any required archive determinant variations.
The scene-return law (2\Delta-\Delta^2) and all delays
((I-T^2)(-T)^k) are retained as their own branch of the computation; neither
is identified with (4) or declared derivative-invisible by (10).
The fixed seam (12/5) and the golden (p_0) retain their own owners.

## 5. What this changes in the strategy

The next calculation is the **remaining full-price first jet**. Start from
the actual native preparation and scene operator on the complete joint
carrier, establish its admitted heat/feedback/pairing jets, and substitute
them into (3). Terms covered by (10) are zero contributions with a checked
hypothesis list. Other terms must be computed, not discarded as archive.
This is T1 partial progress with T0 still open; it is not a new role search.

Only after that substitution is there a native metric covector to compare
with all ten packed slots of `rho0`, including trace, one calibration and
refinement errors. A surviving nonzero traceless covector need not equal
`rho0`; a trace-only result is also a scoped outcome. Own source/Ward,
stationarity, curved joint roots, soundness/recovery and physical constraints
remain distinct required theorems. The fixed-source/raw-owner #310 terminal
and the independent #202/#317 criteria remain unchanged.

## 6. Reproduction and proof boundary

The [Lean capsule](certificates/a4d_native_constrained_price_source.lean)
prints 33 actual propositions and their transitive axioms. They include
algebraic helpers; declaration count is not a measure of physical closure.
The [receipt](certificates/a4d_native_constrained_price_source_results.json)
pins the capsule, compiler output, transitive D0 imports, toolchain and prior
proof inputs. The [exact checker](certificates/a4d_native_constrained_price_source_check.py)
checks full orthogonal operators, archive-preserving first jets, the protected
noninvolutive exception, all 50 metric and 24 connection probes, all ten
packed weights and conormal/lift controls. Its
[ledger](certificates/a4d_native_constrained_price_source_certificate.json)
keeps every unproved native/physical promotion false.

Run the capsule from `03_FORMALIZATION` with
`lake env lean ../02_REGISTRY/research/certificates/a4d_native_constrained_price_source.lean`,
then run the checker from the repository root. The supported D0 owner tree is
unchanged. This is a research certificate, not a CORE or release promotion.
