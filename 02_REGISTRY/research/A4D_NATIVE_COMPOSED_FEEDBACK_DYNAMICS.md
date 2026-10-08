# Native composed feedback: full archive, actual source and golden refinement

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing Draft #310.
Input research head: `609e7daa7c801254ee671874750c5bc61f4efc71`.
Input main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Prepared-readout follow-up input: `58407f912e6f4cedfff3625cdd4e7ba09c6e7951`.
Two-native-preparation follow-up input: `7479dbcb5970b4450912cc848a53e1622e9524af`.
Recorded-quadratic follow-up input: `7c204c9d0e6a405216f9762ddd4d4d55ba57dab4`.
Whole-bootstrap follow-up input: `bbd81c495ea6fcea683f78872b392015c9407401`.
Operator/source follow-up input: `e74df7d999ae04a667d4de08625b8ec77bcdab5a`.
Consumer: G0b in `D0_NATIVE_CORE_EXECUTION_PLAN_2026-10-08.md`.
Status: proved finite operator/action/refinement slice; G0--G4 remain open.

## 1. Result and native ownership

The existing golden gate and the existing golden gate followed by coherent
recording have identical one-transition feedback actions. Their two-transition
feedback actions differ by `-log(1-4*z*p^3)`. Thus one-transition feedback
blindness does not imply that the existing action is blind to composed history.
The same record is retained between the two transitions.

The prepared-readout follow-up below also classifies every compatible fine
projector, derives the exact missing-norm correction to the compressed
history action, transports its genuine moving source, and proves explicit
finite action-error bounds. Literal cylinder readout is bound to replicated
multiplication; it is kept distinct from the image-supported preparation
filter. No physical readout is changed to obtain an action identity.

The two-preparation follow-up restores the full literal-cylinder experiment:
the owned preparation J and its next native history GJ span the entire new
factor. All four cross-return operators reconstruct the full joint operator,
including complementary dynamics, and hence its literal feedback action and
actual derivative. Reconstruction does not select the physical scene law.

The whole-bootstrap follow-up in §6.6 now derives the actual thermal
covector and its coupling to feedback. Literal binary replication retains
the heat covector and doubles the feedback covector. A coarse stationary
variation transfers precisely when the fine thermal covector also doubles.
An independent connected-Laplacian control has a genuinely stationary
coupled slice and a nonstationary replicated image. Native scene constraints
and their actual spectral transition are not replaced by that control.

The operator/source follow-up in §6.7 differentiates the actual source-port
chain from shared D/A primitives, retains the trace normalizer and canonical
pairing, and derives complete-word/feedback jets. Moving eigenvectors are
included in the actual matrix heat derivative. Whole bootstrap covariance
proves a genuine basis Ward identity. General finite operator heat/Jacobi
calculus is proved analytically; physical metric/matter Ward and the complete
native state/tangent/refinement law remain independent requirements.

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

### 6.1. Complete readout extension and transported preparation

The replicated readout in (11) is one full fine experiment. There is also a
precise image-supported preparation test associated with the coarse experiment.
For any isometry J:E->H, define

\[
 R_0=JPJ^T,\qquad E_J=JJ^T.                              \tag{13}
\]

Here P is the old orthogonal readout projector. R_0 is the unique operator
satisfying `R_0 J=JP` and `R_0 E_J=R_0`. The latter condition explicitly says
that this test has no active range outside the preparation image.
It is not imposed on the whole physical apparatus without a native owner.

More generally, **every** orthogonal fine projector R with `RJ=JP` has the
unique decomposition

\[
 R=JPJ^T+S,\quad SJ=0,\quad J^TS=0,\quad S^T=S,\quad S^2=S. \tag{14}
\]

Conversely every such S produces a compatible orthogonal fine readout.
Proof: put `S=R-JPJ^T`. Compatibility and symmetry make the two summands
orthogonal; squaring proves `S^2=S`. Both directions and uniqueness of
(13) are compiled for arbitrary finite dimensions. Thus matching the old
prepared reading allows precisely additional active projectors on the
complement, not an unclassified arbitrary map. Setting S=0 defines the
image-supported test. Its identification with a native experiment needs
that experiment's readout owner; the complementary active range is retained.

For the actual golden preparation, the rectangular matrix J has blocks
`(a I,p I)`, whose entries are the first column of the owned `gate(a,p)`.
The capsule directly proves `J^T J=I` and identifies its matrix-vector
map with the already constructed golden inclusion. This consumes the
native gate, not just a named abstract isometry.

There is an important literal binding to the profinite cylinder readout.
A finite value f is pulled back to both children by forgetting the last
branch. In the normalized cylinder basis its multiplication operator is
`diag(f on both children)=L(diag f)`, as compiled directly. For an event
projector P, this is the replicated readout, with
`S=L(P)-JPJ^T`, not the image-supported filter (13). The distinction can be
measured: on an actual first-child basis state with parent event true,
replicated readout gives one while the image-supported filter gives p.
Thus their difference is `p^2`, with the actual golden weights. The image
filter cannot silently replace the native cylinder event. The scalar
profinite readout and a coherent preparation filter retain different types.

### 6.2. The complete history action, including the missing norm

Let U be **any** real orthogonal full operator on H. No assumption that
U preserves `im J` is made. Its full prepared return and escaped part are

\[
 C=J^TUJ,\qquad L=UJ-JC=(I-E_J)UJ.
\]

Orthogonality gives the exact identities

\[
 J^TL=0,\qquad L^TL=I-C^TC.                            \tag{15}
\]

The escaped norm is recorded in the complement. It is not discarded or
replaced by a new blank. Direct multiplication of the **owned** feedback
functional gives

\[
 F(R_0,U)=J\mathcal F_P(C)J^T,
\]
\[
 \mathcal F_P(C)
 =F(P,C)+P(I-C^TC)P
 =P-PC^TPCP.                                         \tag{16}
\]

The last equality uses `P^2=P`; the compiled expanded identity before that
specialization has `P^2` as its first term. The extra term in (16) is
necessary: applying the feedback formula to C alone loses the norm that
went into unresolved memory. For example the native golden scalar
compression `C=aI`, `P=I` has `F(P,C)=0`, while the full result is `p^2 I`.
This recovers the actual golden feedback without adding a density.

The rectangular determinant identity, with `J^T J=I`, now proves

\[
 \det(I-zJ\mathcal F_P(C)J^T)=\det(I-z\mathcal F_P(C)),
\]
\[
 S_z(F(R_0,U))=S_z(\mathcal F_P(C)).                  \tag{17}
\]

These are compiled identities of the actual matrix expression. For every
internal word, replace U by its full product; in particular
`C_k=J^T U^k J` gives the action of every repeated history. **One may not
replace C_k by C_1^k.** On the owned scalar golden gate and its prepared
first column, `C_1=a` and `C_2=a^2-p^2`, whereas `C_1^2=a^2`. Thus even this
small native example records a returning contribution already at step two.
The full operator preserves the record throughout.

Consequently equality of the *whole* prepared return for a specified word
implies equality of its prepared feedback action for every orthogonal
completion, regardless of unobserved complementary coordinates. Equality
along admitted variation curves also preserves the actual source. This
corrects an overly strong next-step requirement: the entire complementary
operator need not be selected before its action on a transported experiment
can be determined. Its influence is exhausted by the full returns in (16).

This is consistent with (12). For replicated U and the image-supported test R_0,
(17) preserves the action. For the literal cylinder pullback `L(P)`, the
complementary active projector S in (14) is also scored and (12) doubles it. The exact
checker verifies both results on the same golden apparatus. The physical
family `P_N` still needs its own refinement binding; this proof does not
choose which new active modes belong to it.

### 6.3. Genuine moving source and quantitative finite-probe transfer

Equation (17) is pointwise in J,U,P. Hence it remains valid when preparation,
joint dynamics and the readout move together. The capsule proves a genuine
`HasDerivAt` transport for the resulting matrix actions. No stationary
condition or zero source is placed in its premise. Differentiating the
actual compressed operator gives

\[
 \delta C=(\delta J)^TUJ+J^T(\delta U)J+J^TU\delta J.   \tag{18}
\]

For differentiable projector curves, the source of (16) is exactly
`Tr[z(I-z mathcal F)^(-1) delta mathcal F]`, with

\[
\begin{split}
\delta\mathcal F={}&\delta P
 -(\delta P)C^TPCP-P(\delta C)^TPCP-PC^T(\delta P)CP\\
 &-PC^TP(\delta C)P-PC^TPC(\delta P).
\end{split}                                         \tag{19}
\]

This finite derivative formula includes the moving preparation through
(18). The checker independently differentiates noncommuting moving
preparations and shows that freezing J can give a false zero source.
It also checks the source against Jacobi's determinant derivative.
Physical metric/link variations still require their native maps into
J,U,P; a derivative in an arbitrary matrix coordinate is not a matter
stress tensor.

There is an all-size analytic stability estimate with explicit constants.
For contractions C,D, one fixed orthogonal P of rank r, and `0<z<1`,

\[
 |S_z(\mathcal F_P(C))-S_z(\mathcal F_P(D))|
 \le {2rz\over1-z}\,\|C-D\|_{op}.                   \tag{20}
\]

Proof: the segment C_t is contractive. On the r-dimensional active range,
`0 <= mathcal F_P(C_t) <= I` and the inverse pencil has norm at most
`1/(1-z)`. Its derivative is
`-P[(D-C)^T P C_t+C_t^T P(D-C)]P`, with trace norm at most
`2r ||D-C||`. Jacobi's formula and integration give (20). This proof uses
no continuum equation or source fit. For different orthogonal P,Q on the
same n-dimensional comparison space, telescoping the five factors gives

\[
 |S_z(\mathcal F_P(C))-S_z(\mathcal F_Q(D))|
 \le {nz\over1-z}(4\|P-Q\|_{op}+2\|C-D\|_{op}).      \tag{21}
\]

Indeed the feedback difference has the displayed norm bound; the straight
segment of feedback matrices stays between 0 and I. Integrate its
resolvent derivative in dimension n. The coarser n bound is deliberate. Taking J=I recovers the original full
feedback operator, so these bounds also apply directly to the actual full
cylinder readout when its entire fine dynamics is known. The image-test
factorization does not erase any missing blocks of that full experiment.

For two isometric preparations J,K and orthogonal operators U,V on the
same full carrier,

\[
 \|J^TUJ-K^TVK\|_{op}\le\|U-V\|_{op}+2\|J-K\|_{op}. \tag{22}
\]

For full words the first error is at most the sum of the individual
operator errors, by telescoping products of norm one. Thus recording,
preparation and composition errors enter the **same** finite action bound.
A signed probe contrast obeys the sum of these bounds weighted by the
absolute values of its declared coefficients. One fixed nonzero calibration
rescales this estimate by its fixed absolute inverse; it is not tuned to
individual probes or levels.

Equations (20)--(22) prove the quantitative transfer in this prepared
feedback class. To obtain a uniform O(h) bound one still must derive native
error estimates with the displayed rank/dimension and resolvent factors
included. These factors cannot be suppressed: repeated independent active
copies multiply the action, and an approaching pole defeats an unqualified
continuity claim. For example `C=0`, `D=epsilon`, `z=1-epsilon^2` has a
nonvanishing action gap tending to `log 2` although `C-D -> 0`.
No O(h) native metric preparation, calibrated Palatini contrast,
source-subtracted stationarity, soundness or recovery is assumed here.

### 6.4. The owned next history resolves the complete new factor

The complement of one preparation need not be a permanently hidden sector.
Apply the **same owned golden gate** G to the new factor, retaining all old
coordinates. Put J_0=J and J_1=GJ. The native orthogonal frame gives

\[
 G=\begin{pmatrix}aI&-pI\\pI&aI\end{pmatrix},\quad
 T=\begin{pmatrix}I&aI\\0&pI\end{pmatrix},\quad B=[J_0,J_1]=GT,
 \quad T^{-1}=\begin{pmatrix}I&-aI/p\\0&I/p\end{pmatrix}. \tag{23}
\]

For p!=0 these two preparations span the entire new layer, at every old
finite dimension. The second preparation is a full native history, not a
power of a compressed scalar return. The capsule binds G to actual gate
entries, identifies both columns and proves both inverse identities.

For an arbitrary full operator U retain **all four signed cross-return
operators**. Then

\[
 R_{ij}=J_i^TUJ_j,\quad R=B^TUB,\quad
 C=T^{-T}RT^{-1}=G^TUG,\quad U=GCG^T.                 \tag{24}
\]

This reconstructs the unique operator from independently specified return
data. The explicit blocks are

\[
 C_{00}=R_{00},\quad C_{01}=(R_{01}-aR_{00})/p,\quad
 C_{10}=(R_{10}-aR_{00})/p,
\]
\[
 C_{11}=(R_{11}-aR_{10}-aR_{01}+a^2R_{00})/p^2.       \tag{25}
\]

No splitter angle, complementary selector or enumeration of candidate
dynamics is introduced. All cross blocks are essential: the exact G versus
G^T control has identical diagonal return amplitudes but different cross
returns. Diagonal readings or their probabilities alone are insufficient.
Full signed amplitude readout requires controlled routing, inverse access
and interference implementation. `GoldenOrderInterferometer` explicitly
retains those requirements; this matrix theorem does not prove physical
availability on every scene factor.

Literal cylinder readout L(P) commutes with G for every P. Consequently

\[
 F(L(P),C)=G^TF(L(P),U)G,\qquad
 S_z(F(L(P),U))=S_z(F(L(P),T^{-T}RT^{-1})).            \tag{26}
\]

These identities, full operator injectivity and genuine derivative transport
for moving U,P are compiled. They need no orthogonality of U for the algebraic
identity and no preservation of im J. Physical action still requires the
positive-pencil domain. Golden calibration is fixed through variations.
The prior complementary extensions are now distinguished by the second
preparation. More sharply, U(t)=G diag(I,H(t)) G^T has first prepared return
exactly I at every t, but the full literal determinant is
`1-4*z*t^2/(1+t^2)^2`. Its derivative is nonzero at t=1/3. The complete
four-return reconstruction preserves that genuine source.

The analytic error bound follows from

\[
 T^TT=\begin{pmatrix}I&aI\\aI&I\end{pmatrix},\qquad
 \|T^{-1}\|_{op}^2={1\over1-|a|}.
\]

Indeed the symmetric/antisymmetric sectors have eigenvalues 1+a and 1-a;
a^2+p^2=1 and p!=0 give |a|<1. Hence

\[
 \|U-V\|_{op}\le {\|R_U-R_V\|_{op}\over1-|a|}.        \tag{27}
\]

For orthogonal U,V, fixed P of rank r and 0<z<1, apply (20) on the actual
full literal readout of rank 2r:

\[
 |S_z(F(L(P),U))-S_z(F(L(P),V))|
 \le {4rz\over(1-z)(1-|a|)}\|R_U-R_V\|_{op}.          \tag{28}
\]

These norm estimates are analytic. Independent application to d declared
new golden factors gives the tensor preparation frame and inverse squared
norm `(1-|a|)^(-d)`. This is an all-depth algebraic induction; literal active
rank grows as well. The conditioning cannot be suppressed without a native
error/normalization theorem. Its growth alone does not exclude approximation.

Thus complete native cross returns determine the whole declared operator
class without a separate arbitrary complementary selector. Remaining inputs
are the actual joint scene law, admitted variations and physical preparation/
readout implementation, with errors controlled through (27). The result does
not prove that this class exhausts all D0 physical states, or derive the
metric/coframe/link/matter dynamics by supplying them as matrix parameters.

### 6.5. Direct feedback reconstruction by the owned recorded comparer

Follow-up input: 7c204c9d0e6a405216f9762ddd4d4d55ba57dab4.
The feedback consumer need not reconstruct signed U amplitudes first.
Set \(A=(I-P)UP\), with P an orthogonal projector. Then
\[
A^TA=PU^T(I-P)UP=F(P,U).
\]
For complete target vectors x,y the actual owned fullStep on a comparison
port and a blank comparison record gives
\[
(Ax,0,Ay,0)\longmapsto(aAx-pAy,0,0,pAx+aAy).       \tag{29}
\]
The old target record belongs to x,y and to the entire composed U. It is
never replaced between operations of that word. The comparison record
in (29) is a separate apparatus register. Retain both output records.
Writing \(q_x=\|Ax\|^2,\ q_y=\|Ay\|^2,\ q_{xy}=\|aAx-pAy\|^2\), one obtains
\[
\langle Ax,Ay\rangle=
 {a^2q_x+p^2q_y-q_{xy}\over2ap},\qquad ap\ne0.     \tag{30}
\]
This is a fixed native golden calibration, not a fitted source. The sum
of the two recorded responses is \(q_x+q_y\), by \(a^2+p^2=1\).
Both (29)--(30) and their all-size Gram reconstruction are compiled.

The active preparation is implemented without discarding its complement.
On a retained preparation flag define the reversible operator
\[
W_P=\begin{pmatrix}P&I-P\\I-P&P\end{pmatrix},\quad
W_P^TW_P=W_P^2=I,\quad
W_P(x,0)=(Px,(I-P)x).                            \tag{31}
\]
This matrix does not assert physical actuation of every abstract P. For
a literal Boolean cylinder event f its flag is the already owned reversible
basis registration \((i,b)\mapsto(i,b\mathbin{\mathrm{xor}}\neg f(i))\).
Its linear permutation extension gives (31), up to flag ordering, for
the corresponding diagonal projector. Injectivity and blank registration
are bound in Lean to FiniteProtocolClock.register. A basis-label
permutation is not a cloning map on unknown superpositions.

The complete retained operator is explicitly
\[
\mathcal U_{\rm cmp}=
 (W\otimes I)(I_4\otimes L(U))(I_4\otimes W_P)
 =W\otimes(L(U)W_P),                             \tag{32}
\]
where W is the owned recorded golden matrix and L(U)=diag(U,U).
Its detector event is comparison record/port 0, active preparation flag,
and target event I-P. Its amplitude is
\((I-P)(aUPx-pUPy)=aAx-pAy\). All other branches remain in (32).
The complete orthogonality, operator factorization and event reading are
compiled for arbitrary finite target dimension. Common execution of the
whole U on both arms suffices: selective controlled-U or an inverse-U
oracle is not used by this feedback reconstruction.

flaggedComparisonProgram is the explicit three-stage program of (32)
on the existing internal stage register: flag preparation, common full
word, recorded comparison. Lean proves that its owned autonomous
FiniteProtocolClock.run gives exactly (32) after the first three stages
and that the complete transition is injective. These are operations of
the internal program; no independent physical time coordinate is added.
The compiler consumes the declared reversible operations. It does not
derive their physical availability, a blank apparatus, or unbounded
history capacity from M1.

Use the existing complete preparation frame B=[J,GJ]=GT. Each column
\(b_i\) has unit norm. A single-arm query has total input norm one, and
its detector union over both comparison output records reads q_i.
A pair query \((b_i,0,b_j,0)\) has total norm squared two, independently
of the overlap between b_i,b_j or the moving projector P. The measured
normalized mixed probability is therefore \(m_{ij}=q_{ij}/2\).
Consequently there is **one fixed factor two**, with no postselection:
\[
K_{ij}={a^2q_i+p^2q_j-2m_{ij}\over2ap},\quad
K=B^TF(L(P),U)B,\quad
F=GT^{-T}KT^{-1}G^T.                             \tag{33}
\]
The existing action is exactly \(S_z(T^{-T}KT^{-1})\), by orthogonal
conjugacy. It does not become a new measurement-based action. Lean proves
this identity and transports a genuine derivative along moving P(s),U(s),
retaining both projector derivatives. A derivative of the recorded action
is an explicit premise of that transport; stationarity and physical
metric/matter variations are not inferred from the reconstruction.

For two exact preparations/experiments with each of q_i and m_ij changed
by at most epsilon, (30) gives
\[
|\delta K_{ij}|\le {3\epsilon\over2|ap|},\quad
\|\delta K\|_{op}\le m\max_{ij}|\delta K_{ij}|,\quad
\|\delta F\|_{op}\le {\|\delta K\|_{op}\over1-|a|}. \tag{34}
\]
Here m=2n is the number of full-frame columns. The matrix bound follows
from the Frobenius norm. The factor three includes the normalized pair
calibration; its omission fails the exact control. For fixed readout
L(P) of rank 2r, orthogonal full processes and 0<z<1, both feedback
operators are positive contractions supported on that readout. Integrate
the log-determinant derivative on their convex segment to obtain
\[
|\delta S_z|\le {2rz\over(1-z)(1-|a|)}\|\delta K\|_{op}. \tag{35}
\]
The trace is over the common active range. Thus rank, dimension, resolvent
gap and golden conditioning remain explicit. An arbitrary noisy K ledger
need not reconstruct a positive contraction; (35) is not asserted for it
without checking the positive-pencil domain and its gap. No projection
or renormalization of that ledger is introduced as a physical rule.
Moving readouts additionally retain the projector error terms of §6.3.
Tensor conditioning at greater depth is still required. Uniform native
O(h) input and the fixed physical continuum calibration remain open.

Exact controls use both actual native words of lengths one through three
and complete flagged operators in target dimensions one, two and three.
Dephasing before the owned comparer loses a nonzero Gram entry. Dropping
the fixed factor two changes that entry. Normalizing only the active
preparation branch changes a moving query and its genuine source; the
retained complementary branch keeps total norm constant. These controls
do not claim that every tested abstract orthogonal curve is M1-admitted.

The physical input has been narrowed to coherent pair preparation, common
execution of the actual full scene word, retained cylinder registration
and event readout, together with admitted variations and their error law.
Availability of this coupled experiment has not been proved merely by
matrix orthogonality. The full scene law and the separate bootstrap
heat-trace term retain their own owners. No new action, physical source,
complementary selector or metric field law is supplied.


### 6.6. Whole bootstrap: joint thermal source and refinement balance

BOOK_03 §03.25 uses both contributions, with ordinary finite traces:

\[
 \mathcal B_\beta(\Delta,P,U)
 =\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta}
  -\log\det(I-zF(P,U)),\qquad
 F=P U^T(I-P)UP.                                               \tag{29}
\]

The feedback reconstruction in §6.5 does not supply the joint spectral
law for \(\Delta,P,U\). Here fix \(\beta\ne0\) and a nonempty finite real
spectral profile \(\lambda_i(t)\), differentiable at the tested parameter.
This spectral formula applies to a real self-adjoint finite operator
with the declared profile; no Lorentz heat trace or variable spectral
decomposition is assumed. Set

\[
 Z=\sum_i e^{-\beta\lambda_i},\quad H=\beta^{-1}\log Z,\quad
 h(v)=-\frac{\sum_i e^{-\beta\lambda_i}v_i}{Z}.                 \tag{30}
\]

The partition is strictly positive. The compiled `genuine_thermal_source`
differentiates the exponential sum and logarithm, proving that \(h\) is
the genuine derivative of \(H\). Adding an actual feedback derivative
\(f\) gives the genuine whole derivative \(h+f\). Neither contribution
is prescribed from a desired root. The capsule also binds the real
coefficient extension directly to `SceneHeatKernel.zoneHeat`. Its three
zone traces sum to the existing combinatorial-scene polynomial
\(1+12x^{20}+10x^{22}+8x^{24}+2x^{33}\). This binding does not identify
the combinatorial scene Laplacian with the separately normalized default
operator or derive a varied physical scene from the frozen polynomial.

**Complete raw replication calculation.** For the already defined
\(L(A)=\operatorname{diag}(A,A)\), use the literal cylinder projector
\(L(P)\), the full process \(L(U)\), the replicated spectrum, and the
same fixed \(\beta,z\). This is an explicitly declared refinement;
its physical admission and completeness in the core are not hypotheses
that have been proved. Direct trace and determinant identities give

\[
 Z_+=2Z,\quad H_+=H+\beta^{-1}\log2,\quad S_+=2S,
 \quad d\mathcal B_+=h+2f.                                  \tag{31}
\]

The last identity is compiled as a `HasDerivAt` proposition, using the
actual heat derivative and the actual feedback derivative. The added
constant has zero variation; it is not a selected counterterm. Thus

\[
 h+f=0\ \Longrightarrow\ d\mathcal B_+=f,
 \qquad (h+f=0\ \wedge\ h+2f=0)\iff(h=f=0).                 \tag{32}
\]

For a different independently owned fine spectral transition, with its
genuine thermal covector \(h_+\), the exact condition on a coarse
stationary variation is instead

\[
          h_++2f=0\iff h_+=2h.                              \tag{33}
\]

Apply this equality to every admitted tangent direction of the actual
joint family. Independently varying heat and feedback would be stronger
than that family; the capsule does not assert that independence is native.
For all independent real \(h,f\), a single calibration obeying
\(h+kf=c(h+f)\) exists only for \(k=c=1\). This excludes a universal
single normalization of raw replication, not a constrained native
variation class. Iteration of (31) gives
\(H_d=H+d\beta^{-1}\log2\), \(S_d=2^dS\), and
\(d\mathcal B_d=h+2^df\). These follow by induction from the same
dimension-independent identities, rather than by a finite depth search.
For each native stage (33), not a new action, is the next compatibility
condition to prove or classify from its own spectral/variation owner.

**Nonempty independent stationary-slice control.** The formulas are fixed
before solving the equation. On a connected two-vertex graph take

\[
 \Delta(t)=t\begin{pmatrix}1&-1\\-1&1\end{pmatrix},\quad
 P=\operatorname{diag}(1,0),\quad
 U(t)=\frac1{1+t^2}
       \begin{pmatrix}1-t^2&-2t\\2t&1-t^2\end{pmatrix},
 \quad \beta=1,\quad z=\tfrac12.                            \tag{34}
\]

This is a control in the finite spectral/orthogonal class, not a newly
selected physical scene. For \(t>0\), the Laplacian has its exact zero
mode and positive mode \(2t\); its quadratic form is
\(t(x_0-x_1)^2\). The readout is an orthogonal projector and \(U\)
is orthogonal for every real \(t\). The pencil is exactly
\(\operatorname{diag}((1+t^4)/(1+t^2)^2,1)\), hence positive definite.
No empty determinant fiber or lost zero mode is used. The sources are

\[
 h(t)=-\frac{2e^{-2t}}{1+e^{-2t}},\qquad
 f(t)=\frac{4t(1-t^2)}{(1+t^2)(1+t^4)}.                     \tag{35}
\]

Both actual derivatives are compiled and bound to (29), including the
matrix determinant. The continuous coupled-slice source \(h+f\) is
\(-1\) at zero. At \(1/2\), \(f=96/85\) and \(h\ge-1\), giving
\(h+f\ge11/85>0\). The compiled intermediate-value argument therefore
gives a root \(t_*\in(0,1/2)\). Since \(f(t_*)>0\), its actual
replicated derivative equals \(f(t_*)>0\). This is stationarity along
the declared coupled curve, not a full joint root for all independent
matrix variations and not an admitted native physical solution. It
refutes unconditional slice-stationarity transfer for raw replication;
it neither fits a source nor proves a whole-core obstruction.

**Why the admissible tangent class matters.** An independent uniform
spectral shift has the exact identity
\(\mathcal B(\lambda+t,P,U)=\mathcal B(\lambda,P,U)-t\), with source
\(-1\). The capsule proves that it cannot be stationary whenever that
variation is allowed. A native Laplacian's zero-mode constraint can
exclude the shift; the control (34) keeps its zero mode. This statement
cannot be promoted to a native no-go by silently enlarging the domain.

The remaining single constitutive arrow is the owned joint
\(\Delta/P/U\) state and tangent law and its real spectral refinement.
It must decide (33) on its complete admitted domain while preserving
the recorded experiment and its normalization. An independently supplied
thermal tower, a selected temperature rescaling or a replacement trace
would not prove this arrow. No physical source/Ward, metric contrast,
Einstein stationarity, soundness or curved recovery is inferred here.

### 6.7. Actual source-port chain, moving eigenvectors and basis Ward

Operator/source follow-up input: `e74df7d999ae04a667d4de08625b8ec77bcdab5a`.
This follows the single G0b arrow from the native owners. In particular,
`SourcePortPreparation` already defines an interaction from the frozen
zone degree and adjacency data. Its port, projector and normalizer cannot
be varied independently and then called the same native preparation.
The calculation below differentiates those actual polynomial/rational
operations and the complete retained word. It neither selects a new scene
nor asserts that every smooth matrix curve is physically admitted by M1.

**The owned constituent map.** Use D for the degree matrix of `RawZone`,
A for its equitable adjacency, and G for the canonical part-size pairing.
D is a degree operator, not the physical Dirac operator. The polynomial
coefficients below are the existing source's fixed coefficients:

\[
 K=[D,A],\quad P_a=-K^2/2840,\quad
 E=(D-22I)(D-20I)/8,\quad M=P_a E P_a,
 \quad\tau=\operatorname{Tr}M,\quad R=M/\tau,\quad Q=P_a-R.
                                                               \tag{36}
\]

At the actual source D=diag(24,22,20), A=[[0,11,13],[9,0,13],
[9,11,0]], G=diag(9,11,13), the compiled bindings give exactly
`RawZone.Pact`, `degreePort`, `compressed`, `signalPort`, `inputPort`,
and \(\tau=567/710>0\). They rebuild the required equalities from the
matrix definitions with kernel-checked arithmetic; none consumes a
`native_decide` theorem. With the existing Q8 matrix L=spin(2),

\[
 X=(I-R)\otimes I+R\otimes L                                \tag{37}
\]

is exactly the owned `coupled` interaction. The max-degree port remains
the owner's declared source-internal choice; this does not prove M1
uniqueness of max degree over other intrinsic choices.

For every differentiable D(s), A(s) through this constituent map with
\(\tau\ne0\), the following are genuine derivatives, not independently
supplied source covectors:

\[
 \begin{aligned}
 dK&=[dD,A]+[D,dA],\\
 dP_a&=-(dK\,K+K\,dK)/2840,\\
 dE&=\{dD(D-20I)+(D-22I)dD\}/8,\\
 dM&=dP_a E P_a+P_a dE P_a+P_a E dP_a,\\
 d\tau&=\operatorname{Tr}(dM),\\
 dR&=\tau^{-1}dM-\tau^{-2}\operatorname{Tr}(dM)M,\\
 dQ&=dP_a-dR,\qquad dX=dR\otimes(L-I).
 \end{aligned}                                               \tag{38}
\]

All arrows in (38), including their composition from D,A to X, are
compiled `HasDerivAt` propositions. The normalizer derivative is required
by the actual port definition. Dropping it changes the interaction jet.
The algebraic formulas still exist for curves that leave the projector
or spectral class; those curves are **not** thereby admitted native states.
In particular the fixed 2840/22/20 coefficients must not be advertised
as a projector calculus for an arbitrary changed spectrum. Physical
state/tangent admission and the full scene Laplacian retain their owners.
The three-dimensional zone quotient is not substituted for the full
33-dimensional scene heat operator. In graph coordinates its combinatorial
Laplacian is D-A, whereas the bootstrap's separately normalized physical
operator requires its own identification.

**The full word and the native pairing.** For a fixed retained carrier,
let \(W=U_m\cdots U_1\) be the actual chronological product. Its derivative is

\[
 dW=\sum_{j=1}^{m}U_m\cdots U_{j+1}\,dU_j\,
                      U_{j-1}\cdots U_1.                    \tag{39}
\]

The recursive `wordJet` and its genuine derivative theorem cover every
finite list of differentiable stages. This retains all earlier records;
no compression power, reset, external time variable or inverse oracle
is inserted. A change of word length/carrier is a refinement transition,
not an extra differentiable parameter justified by (39).

In native quotient coordinates the adjoint is
\(W^{\dagger_G}=G^{-1}W^T G\). Thus the same feedback action, written
in those coordinates, uses

\[
 F=P G^{-1}W^T G(I-P)WP.                                    \tag{40}
\]

This is the existing adjoint action, not a new metric-dependent action.
Write GI=G^{-1}. The compiled seven-term `weightedFeedbackJet` is

\[
\begin{aligned}
 dF={}&dP\,GI W^TG(I-P)WP+P\,dGI W^TG(I-P)WP\\
 &+P GI\,dW^TG(I-P)WP+P GI W^T\,dG(I-P)WP\\
 &-P GI W^TG\,dP WP+P GI W^TG(I-P)\,dW P\\
 &+P GI W^TG(I-P)W\,dP,\qquad dGI=-GI\,dG\,GI .
\end{aligned}                                               \tag{41}
\]

The inverse jet follows from differentiating G(s)GI(s)=I, with both
pointwise inverse identities checked. The actual `HasDerivAt` theorem
for (41) differentiates the products and transpose. A port/scene law must
supply the stages and their admitted primitive jets; it cannot supply dF
as an unrelated covector fitted to stationarity.

**Full operator heat/source calculation.** Fix a nonempty finite real
carrier, \(\beta\ne0\), fixed z, a positive-definite G, a G-self-adjoint
\(\Delta\), a G-orthogonal P, and a G-isometric W. For \(0<z<1\),
F is G-positive with spectrum in [0,1], so the heat trace Z is positive
and \(N=I-zF\) has positive determinant. These are sufficient conditions;
the derivative formula only needs Z>0 and det N>0 along the tested curve.
Define \(\rho=e^{-\beta\Delta}/Z\) and \(\Pi=zN^{-1}\). Then the actual
BOOK_03 functional has the derivative

\[
 d\mathcal B=-\operatorname{Tr}(\rho\,d\Delta)
                +\operatorname{Tr}(\Pi\,dF).                \tag{42}
\]

Here dF is (41), and any source-dependent stage uses (38)--(39).
There is no prescribed matter source or stationarity gate in (42).

For completeness, the heat derivative holds even for a noncommuting
matrix variation and at spectral collisions. A proof that assumes
eigenvalue derivatives is unnecessary. For a finite matrix A and tangent V,
termwise differentiation of the exponential series gives

\[
 d(A^k)[V]=\sum_{j=0}^{k-1}A^j V A^{k-1-j},\quad
 \operatorname{Tr}(d(A^k)[V])=k\operatorname{Tr}(A^{k-1}V).
                                                               \tag{43}
\]

The finite power jets, genuine curve derivatives and cyclic-trace identity
in (43) are compiled for arbitrary matrix size. To justify the infinite
sum, on \(\|A\|\le M\), in a submultiplicative operator norm, the derivative
remainder after degree m obeys

\[
 \|d e^A[V]-dE_m(A)[V]\|
 \le\|V\|\sum_{r=m}^{\infty}\frac{M^r}{r!}
 \le\|V\|e^M\frac{M^m}{m!},\quad
 E_m(A)=\sum_{k=0}^{m}A^k/k!.                               \tag{44}
\]

Uniform convergence of the series and its derivatives on every bounded
ball proves differentiability. Taking traces in (43), passing to the
convergent sum and putting A=-beta*Delta, V=-beta*dDelta gives
\(dZ=-\beta\operatorname{Tr}(e^{-\beta\Delta}d\Delta)\), hence the
first term of (42). The determinant term follows by factoring
N+t*dN=N(I+t*N^{-1}*dN). In the column-multilinear determinant expansion,
the linear coefficient at I is Tr(N^{-1}*dN), and all other terms have
degree at least two. Therefore d log det N=Tr(N^{-1}*dN);
dN=-z*dF gives the second term. This proves (42) for every C1 finite
operator curve on the stated domain, without requiring [Delta,dDelta]=0.

Proof status is explicit: (42), its infinite-series passage (44) and the
general Jacobi step have a self-contained analytic proof here. Lean
currently proves their finite noncommutative power/word/feedback jets,
the previously established scalar thermal derivative, and the **actual
matrix exponential** thermal derivative on every declared differentiable
spectral factorization \(T(s)\operatorname{diag}\lambda(s)T(s)^{-1}\).
The latter allows moving, noncommuting eigenvectors. General matrix
heat/Jacobi differentiation is not labeled fully Lean-formalized by
that restricted theorem. Exact controls test noncommuting frames and
normalizer jets; they do not replace the analytic proof.

**Genuine basis Ward from the whole action.** For any invertible T,
transport every owned datum and pairing together:

\[
 D'=TDT^{-1},\ A'=TAT^{-1},\ P'=TPT^{-1},\ W'=TWT^{-1},
 \quad \Delta'=T\Delta T^{-1},\quad
 G'=T^{-T}GT^{-1},\quad GI'=TGI T^T.                        \tag{45}
\]

The compiled covariance theorems prove (36)--(37) transform by the same
conjugation, including the joint tensor carrier and every complete word.
They also prove F'=TFT^{-1}, actual matrix heat invariance and determinant
invariance. Consequently the **whole** bootstrap is constant along any
such frame curve. `genuine_whole_basis_ward` proves its actual derivative
is zero, even without assuming a differentiable frame: scalar action
constancy suffices. At T(0)=I, the corresponding jets are

\[
 dD=[\Omega,D],\ dA=[\Omega,A],\ dP=[\Omega,P],\
 dW=[\Omega,W],\ d\Delta=[\Omega,\Delta],\quad
 dG=-\Omega^T G-G\Omega,\quad dGI=\Omega GI+GI\Omega^T,
 \quad dF=[\Omega,F].                                     \tag{46}
\]

The constituent and full feedback jet identities are compiled.
Since rho commutes with Delta and Pi with F, both contractions in (42)
vanish by cyclic trace. This is a proved **basis Ward identity** of the
existing finite joint action and its owned source operations. It does
not remove non-gauge response-null directions, make an off-shell state
stationary on physical variations, or prove the local metric/matter Ward
identity. Freezing G while shearing the other data creates a different
adjoint and a false source; an exact hostile control detects it.

Quantitative consequences preserve their domains. For example,
\(\|dR\|\le(|\tau|^{-1}+n\|M\|/\tau^2)\|dM\|\), and
\(\|dW\|\le\sum_j\|dU_j\|\prod_{i\ne j}\|U_i\|\).
The first follows from (38) and |Tr(dM)|<=n*norm(dM), the second from
(39). Uniform native normalizer, condition, rank and resolvent bounds
still have to be obtained from the preparation/refinement owner. No
uniform physical O(h) estimate is inferred from the frozen positive tau.

The next single constitutive input is now narrower: the **owned joint
primitive state/tangent and spectral refinement law** must determine
Delta and the chronological stages from the same admitted history data.
Equations (38)--(42) then compute its source rather than leaving the
port, normalizer, metric and stages as independently supplied hypotheses.
On that actual tangent image, test the refinement condition (33), derive
native on-shell equations, and preserve non-gauge null directions.
No new action, temperature law, selector or physical postulate is used.

### 6.8. The two native histories force the passive spectral class

Input: `45f19d1399829b284f15b41899b49ee9961ea394`. This uses the **same**
owned J, GJ and complete frame B=GT of §6.4, on every old finite carrier,
including all 33 scene coordinates and retained memory. It does not
identify the three-zone degree operator with the full scene Laplacian.
Fix the existing golden a,p, with a²+p²=1 and p!=0. For coarse Delta and
an arbitrary full fine operator Delta+ define the two actual defects

\[
 e_0=\Delta_+J-J\Delta,\qquad
 e_1=\Delta_+GJ-GJ\Delta,\qquad
 E_H=[e_0,e_1]=\Delta_+B-BL(\Delta).
\]

These are intertwining residuals, not a native stationarity/admission gate.
The inverse is exactly B^-1=T^-1 G^T. Because G and T commute with every
literal L(Delta), multiplication gives

\[
 \Delta_+-L(\Delta)=E_HB^{-1},\qquad
 (e_0=e_1=0)\iff \Delta_+=L(\Delta).                 \tag{43}
\]

Both inverse identities, reconstruction and the explicit column-level iff
are compiled. This is the **complete class of all finite operators with
both declared history intertwinings**, not a finite sample or a claim that
this class exhausts native physical refinements. Neither symmetry nor
positivity is needed for (43). In particular one cannot choose an invisible
complement after imposing both histories. With only e_0=0,

\[
 e_1=[\Delta_+,G]J.                                \tag{44}
\]

The commutator identity is compiled. If the fine scene is passive under
the next golden tick, meaning it commutes with G, first-history naturality
already forces literal replication. **Passivity itself is not derived
from M1.** The recorded golden dynamics retain correlations, so passivity
must be checked on the actual scene law rather than presumed.

For completeness, the entire self-adjoint first-history class has the
analytic description

\[
 \Delta_+=G\begin{pmatrix}\Delta&0\\0&A\end{pmatrix}G^T,
 \quad A=A^T,\quad
 e_1=pG\binom{0}{A-\Delta}.                         \tag{45}
\]

Proof: J=G( I,0 )^T, so the first column of G^T Delta+ G is
(Delta,0)^T. Self-adjointness makes the other off-diagonal block zero;
the remaining block is uniquely A. Conversely every displayed A satisfies
the first intertwining. Orthogonal conjugacy gives
norm(Delta+-L(Delta))=norm(e_1)/abs(p). This full one-history class and
its operator-norm equality are analytic; the Lean capsule claims the
compiled (43)--(44), not a new formalized classification of physical states.

**Actual thermal and whole-action consequence.** For a nonempty finite
self-adjoint scene, ordinary heat trace is positive and

\[
 H_\beta(L(\Delta))=H_\beta(\Delta)+\beta^{-1}\log2,
 \qquad d\mathcal B_+=h+2f.                         \tag{46}
\]

This is the same bootstrap of §6.6. Diagonalization proves the matrix-heat
identity for the whole finite self-adjoint class. Lean binds the actual
matrix exponential directly on declared diagonal spectra, proves its
genuine thermal derivative for every curve satisfying (43), and adds the
actual replicated feedback derivative. Thus genuine zero derivatives on
both coarse and fine curves force h=f=0 separately on that tangent. These
are explicit conditional derivative propositions; no desired native
zero derivative is hidden in the definition of E_H. A nonzero heat source
cannot transfer by a spectral law passive on **both** native histories.

**First variation is essential.** Vanishing defects at one state do not
imply their derivatives vanish. At a replicated spectral value let
rho=exp(-beta Delta)/Tr exp(-beta Delta), and put

\[
 E_V=\dot\Delta_+-L(\dot\Delta),\qquad
 h_+=h-\tfrac12\operatorname{Tr}(L(\rho)E_V),\qquad
 h=-\operatorname{Tr}(\rho\dot\Delta).              \tag{47}
\]

The general matrix derivative is the analytic theorem of §6.7; rho+ is
L(rho)/2. The capsule compiles the exact trace identity and both iffs:

\[
 h_+=2h\iff\operatorname{Tr}(L(\rho)E_V)=-2h,
 \qquad h_+=h\iff\operatorname{Tr}(L(\rho)E_V)=0.     \tag{48}
\]

The last kernel can contain nonzero spectral defects. They remain
response-null directions, not a declared physical gauge. On fixed golden
coordinates E_V=dot(E_H)B^-1, so positivity and trace rho=1 give the
analytic necessary lower bounds

\[
 \|E_V\|_{op}\ge |h|,\qquad
 \|\dot E_H\|_{op}\ge\sqrt{1-|a|}\,|h|
 \quad\hbox{whenever }h_+=2h.                      \tag{49}
\]

Indeed norm(L(rho))_trace=2 and norm(B^-1)=1/sqrt(1-|a|).
If first-history naturality and symmetry also hold through the variation,
(45) yields the sharper constraint
Tr(rho(dot(A)-dot(Delta)))=-2h and
norm(dot(e_1))>=2 abs(p) abs(h). These are quantitative **necessary**
constraints to test against a source law derived independently; they are
not a recipe for selecting A, its jet, a source or a new coupling.

Exact controls retain both histories, a nonzero complement invisible on
J, nonzero cross-history defects, defects with zero thermal contraction,
and a point where e_0=e_1=0 but dot(e_1)!=0. The latter rejects the false
inference from pointwise compatibility to compatible sources. The actual
33-state scene polynomial fixes its Gibbs normalization and protected zero
mode in a separate full-profile control; it is not replaced by quotient
D-A or by a tuned thermal sector.

The next G0b proof must derive Delta+ and its **history defect and first
jet** from the same admitted primitive history as P and the retained word.
If that owner proves passivity, apply the complete scoped obstruction;
if it produces a coupled spectral change, evaluate (47)--(49) on its full
native tangent image. Algebraic room for a nonzero E_V is not physical
admission, and satisfying (48) by fitting E_V is not a proof. The full
primitive/tangent/refinement law, physical source/Ward, contrast, genuine
native on-shell system, curved roots, soundness/recovery and GR remain open.


## 7. Verification and next load-bearing input

`certificates/a4d_native_composed_feedback_dynamics.lean` contains 215
compiled propositions, with each actual type and transitive axiom list
printed in its transcript. The receipt pins all seventeen transitively imported
D0 sources and the actual toolchain inputs. Standard logical axioms only;
no new axiom or placeholder. The companion exact checker passes 670 controls and binds the book,
native matrices, complete-block identities, delayed archive control,
composed source, joint projection refinement, determinant scaling and
immutable result ledger. Finite controls do not replace the all-size proofs.

The remaining single G0b input is the **joint scene process with its admitted
coherent pair preparations, retained flag registration, common full-word
execution and quadratic event readings, together with the owned joint
Delta/P/U tangent law and spectral refinement satisfying (33)**. For the feedback component,
(29)--(35) replace a requirement for signed U tomography or inverse access.
The compiler and fixed calibration are constructed; physical actuation,
native admitted variations and uniform preparation bounds must follow from
their owners. The thermal covector now includes moving eigenvectors on the declared
spectral family. Source-dependent stages are differentiated from the actual
shared primitive chain, including their normalizer and pairing. The all-size
operator heat/Jacobi formula is analytic; its general infinite differentiation
is not mislabeled fully Lean-formalized. Native state/tangent admission, the
full scene spectral coupling and its actual refinement are still required. Apply the proved bounds with actual
native rank, normalization and recording errors.
For the distinct image-supported preparation test, all completion effects
are already exhausted by (16)--(17); one need not choose its unobservable
coordinates. Equating these two experiments is explicitly rejected. This
narrows the needed operator/variation law without changing the physical
readout or supplying metric field dynamics by hand.

The established profinite point-history tower remains distinct from the
Hilbert amplitude tower until their physical preparation/readout map is
proved. No condensed-sheaf equivalence, physical Ward identity, joint
Einstein stationarity, curved recovery or GR soundness is inferred here.
The original fixed-source/raw-owner #310 terminal and the independent
#202/#317 obligations are unchanged; no registry claim is promoted.
