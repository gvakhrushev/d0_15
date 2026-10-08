# Native composed feedback: full archive, actual source and golden refinement

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing Draft #310.
Input research head: `609e7daa7c801254ee671874750c5bc61f4efc71`.
Input main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Consumer: G0b in `D0_NATIVE_CORE_EXECUTION_PLAN_2026-10-08.md`.
Status: proved finite operator/action/refinement slice; G0--G4 remain open.

## 1. Result and native ownership

The existing golden gate and the existing golden gate followed by coherent
recording have identical one-transition feedback actions. Their two-transition
feedback actions differ by `-log(1-4*z*p^3)`. Thus one-transition feedback
blindness does not imply that the existing action is blind to composed history.
The same record is retained between the two transitions.

This result uses the actual entries of
`D0.Representation.GoldenOrderInterferometer.gate` and
`D0.Representation.GoldenCoherentMemory.fullStep`. The functional is the
feedback component in BOOK_03 §03.3.2:

\[
F(P,U)=PU^T(I-P)UP,\qquad S_z(F)=-\log\det(I-zF).
\]

Here P is the orthogonal active/archive **block** projection. It is not the
quantum partial trace over the internal record. The gate operates on the full
active-port × record space. BOOK_03 §03.3 and §03.26 already compose internal
operations; evaluating the same functional at that composed operator changes
no action formula. It does not establish that a two-transition term alone is
the complete physical variational law. In particular BOOK_03 §03.25 includes
the separate heat-trace term in the full bootstrap functional.

The parameter class below is complete for real orthogonal operators whose
retained block is the declared golden scalar. Orthogonality is not a proof
of physical actuation or M1 admission of every matrix in that class. The
native owners themselves retain these admission conditions. The generic
class also makes the exact limits of the two-transition observation explicit.

## 2. Complete joint operator, including every archive direction

Fix finite real active and archive spaces E=R^n, A=R^m, `p != 0`,
`a^2+p^2=1`. Write a joint orthogonal operator as

\[
U=\begin{pmatrix}aI&B\\ C&D\end{pmatrix}.
\]

There is a unique normalized block description

\[
R=-B^T/p,\quad S=C/p,\quad V=D-aSR^T,\qquad
U=\begin{pmatrix}aI&-pR^T\\pS&aSR^T+V\end{pmatrix}.       \tag{1}
\]

It is orthogonal if and only if

\[
S^TS=I,\quad S^TV=0,\quad V^TV=I-RR^T.                  \tag{2}
\]

For square finite U these conditions also imply

\[
R^TR=I,\quad VR=0,\quad VV^T=I-SS^T.                  \tag{3}
\]

Proof: multiply all four blocks of `U^T U=I`. The first block yields
`p^2(S^TS-I)=0`; the off-diagonal block then yields `S^TV=0`; the last block
yields the last equation in (2). Conversely (2) makes all four blocks those
of I. Since the full matrix is square, left orthogonality gives right
orthogonality; applying the same calculation to `U^T` yields (3).
Reconstruction (1), both implications of (2), and all six constraints are
compiled for arbitrary finite n,m. No finite rank experiment substitutes
for completeness. The isometric embedding S is injective, so m>=n; the
dimension consequence follows from elementary finite-dimensional injectivity.

V is the map between the remaining archive complements. It cannot generally
be deleted. With `D=aSR^T+V`, elimination of the archive gives the exact
internal-transition recurrence

\[
y_k=D^ky_0+p\sum_{j=0}^{k-1}D^{k-1-j}Sx_j,
\]
\[
x_{k+1}=ax_k-pR^TD^ky_0
 -p^2\sum_{j=0}^{k-1}R^TD^{k-1-j}Sx_j.                 \tag{4}
\]

k counts compositions of the given internal transition, not an independent
physical clock. Equation (4) retains the initial archive and every return.
It specializes the already compiled complete archive recurrence in
`A4D_NATIVE_HISTORY_RESPONSE_DESCENT.md`.

For an invertible `I-zD`, the retained Schur resolvent is

\[
[I-zaI+z^2p^2R^T(I-zD)^{-1}S]^{-1},                  \tag{5}
\]

whenever this remaining factor is invertible. Its Neumann expansion needs
the separate convergence condition. Formula (5) is a resolvent of U; it
does not replace the owned feedback pencil `I-zF` in the action.

## 3. What two transitions determine

For every completion (1), the active feedback of one transition is `p^2 I`.
The retained block after two transitions is

\[
A_2=a^2I-p^2H,\qquad H=R^TS.                         \tag{6}
\]

In the minimal archive m=n, (3) forces V=0, and R,S are orthogonal. Changing
only the archive coordinates by `y'=R^T y` puts the full operator into

\[
U(H)=\begin{pmatrix}aI&-pI\\pH&aH\end{pmatrix},\quad H\in O(n). \tag{7}
\]

Multiplying the coordinate-change blocks proves (7); the exact checker
also checks this identity on noncommuting instances. The anchored active
basis is retained. Equation (6) recovers H uniquely from the full retained
transition block, and (7) then determines every future transition. A scalar
action value alone does not provide this reconstruction.

For a larger archive, H alone is insufficient. A complete exact control is

\[
U_\epsilon=\begin{pmatrix}a&-p&0\\0&0&\epsilon\\p&a&0\end{pmatrix},
\qquad \epsilon=\pm1.
\]

Both matrices are orthogonal, have `R=e1`, `S=e2`, H=0, and have the same
retained first and second powers a,a^2. Their retained third powers are
`a^3-epsilon*p^2`. This is the contribution of
`V=epsilon*e1*e2^T` in (4), without additional clocks or resets.

In the minimal class, orthogonality gives `F_2=I-A_2^T A_2`, hence

\[
F_2=a^2p^2(2I+H+H^T)=p^3(2I+H+H^T)                 \tag{8}
\]

in the golden case `a^2=p`, `p+p^2=1`. These identities and the injectivity
of (6) in H are compiled. H and H^T can have equal F_2 while having different
A_2; response kernels are not declared physical gauge.

## 4. Binding to the existing D0 gates and action

In the owned coordinate order `(00,01,10,11)`, let `G=gate(a,p)`,
`U0=G tensor I2`, and `W=fullStep(a,p)`. After the explicit finite index
equivalence, (7) identifies `U0=U(I2)` and `W=U(X)`, where
`X=[[0,1],[1,0]]`. These are equalities of actual native definitions,
not source names attached to independent replacement matrices.

The full feedback `PU^T(I-P)UP` equals `diag(C^TC,0)` for the active/archive
blocks; the inactive determinant factor is one. Therefore

\[
F_1(U0)=F_1(W)=p^2I_2,
\quad F_2(U0)=4p^3I_2,
\quad F_2(W)=2p^3(I_2+X).
\]

The exact determinants and action gap are

\[
\det(I-zF_2(U0))=(1-4zp^3)^2,\quad
\det(I-zF_2(W))=1-4zp^3,
\]
\[
S_z(F_2(U0))-S_z(F_2(W))=-\log(1-4zp^3)>0           \tag{9}
\]

when `p>0`, `z>0`, `4zp^3<1`. All these statements are compiled. Lean's
total real logarithm also admits algebraic statements outside this physical
positive-pencil domain; those extensions are not used as physical actions.
The actual probabilities starting from `(1,0,0,0)` give another control:
the second-return first-port weights are respectively `p^6` and `p^2+p^4`,
with difference `2p^3`. One does not partial-trace and reinitialize the record
between applications of W.

## 5. Genuine derivative of the composed action

To check variation rather than assign an arbitrary source, use the entire
Cayley coordinate curve inside the explicitly declared orthogonal class:

\[
H(t)=\frac1{1+t^2}\begin{pmatrix}1-t^2&-2t\\2t&1-t^2\end{pmatrix}.
\]

Direct multiplication proves `H(t)^T H(t)=I`. Substituting into the actual
matrix expression (8) gives

\[
F_2(t)=\frac{4p^3}{1+t^2}I_2,\quad
S_2(t)=-2\log\left(1-\frac{4zp^3}{1+t^2}\right),
\]
\[
S_2'(t)=\frac{-16zp^3t}{(1+t^2)(1+t^2-4zp^3)}.      \tag{10}
\]

The `HasDerivAt` theorem is about the matrix-derived functional itself,
with nonzero denominator; it does not assume the proposed derivative as
a gate. On the positive-pencil branch the derivative is nonzero at t=1
for positive p,z. The independent exact certificate differentiates the
determinant expression and checks the same value and sign.

This source is the derivative with respect to an orthogonal-completion
coordinate. It is not yet a metric matter source `T_mu_nu`. Physical
admission of this continuous variation and its relation to coframe/link
variations must come from the native preparation law. In particular a
continuously chosen Cayley gate is not silently added to the fixed Q8
primitive palette of BOOK_03 §03.26.3.

## 6. Joint golden refinement and the exact action scaling

Use the golden cylindrical inclusion already constructed from the owned
branch weights `(p,p^2)`:

\[
Jx=(ax,px),\qquad J^TJ=I.
\]

For an already specified joint operator or projection, set
`L(A)=diag(A,A)`. This is tensoring by the identity on the new factor, in
sum-coordinate order. It obeys `L(A)J=JA`, preserves products, transpose,
identity and differences, and refines the **complete** state and split.
For every internal word, and in particular every power k,

\[
F(L(P),L(U)^k)=L(F(P,U^k)).                          \tag{11}
\]

The capsule proves the isometry, intertwining, homomorphism identities and
(11) for all finite dimensions and all k. The word statement follows by
induction from the proved multiplication identity, without any commutativity
assumption. This connects the actual joint feedback operator to the
previously constructed golden inclusion, including all record coordinates.

The ordinary determinant is multiplicative over the two copies:

\[
\det L(A)=(\det A)^2,\qquad
S_z(L(F))=2S_z(F),\qquad dS_z(L(F))=2dS_z(F).        \tag{12}
\]

The source identity is compiled as an actual derivative theorem for every
differentiable coarse curve, not a Boolean compatibility flag. Repeating
the construction gives factor `2^r` after r binary refinements. In contrast,
the golden state pairing and cylindrical expectations remain normalized.
These are different quantities, with exactly known transition laws.

No level-dependent normalization or counterterm is introduced to conceal
(12). The full physical action must account for this ordinary-trace scaling
through its own scene/volume dictionary and the other existing terms.
Equation (12) alone neither proves nor excludes that compatibility. Nor
does it control new independent fine-level interaction variations: it
transports the given coarse variations. An orthogonal operator on the
complement of `im J` may be invisible on prepared coarse states and still
affect an operator determinant. Exact controls retain this distinction.

## 7. Verification and next load-bearing input

`certificates/a4d_native_composed_feedback_dynamics.lean` contains 56
compiled propositions, with each actual type and transitive axiom list
printed in its transcript. The receipt pins all four transitively imported
D0 sources and the actual toolchain inputs. Standard logical axioms only;
no new axiom or placeholder. The companion exact checker passes 177 controls and binds the book,
native matrices, complete-block identities, delayed archive control,
composed source, joint projection refinement, determinant scaling and
immutable result ledger. Finite controls do not replace the all-size proofs.

The remaining single G0b input is now narrower: **derive the physically
admitted extension on the new-factor complement and its action/variation
law from the complete native preparation/scene rule**. Coherent replication
is constructed, and its action/source scaling is known. The theorem does
not make replication the only admitted extension, and preserving a prepared
subspace alone does not determine its determinant on the full apparatus.
This is the next dependency of the full bootstrap and history-to-geometry
transfer. It is not another unconstrained field-family search.

The established profinite point-history tower remains distinct from the
Hilbert amplitude tower until their physical preparation/readout map is
proved. No condensed-sheaf equivalence, physical Ward identity, joint
Einstein stationarity, curved recovery or GR soundness is inferred here.
The original fixed-source/raw-owner #310 terminal and the independent
#202/#317 obligations are unchanged; no registry claim is promoted.
