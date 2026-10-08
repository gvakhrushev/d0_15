# Native composed feedback: full archive, actual source and golden refinement

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing Draft #310.
Input research head: `609e7daa7c801254ee671874750c5bc61f4efc71`.
Input main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Prepared-readout follow-up input: `58407f912e6f4cedfff3625cdd4e7ba09c6e7951`.
Two-native-preparation follow-up input: `7479dbcb5970b4450912cc848a53e1622e9524af`.
Recorded-quadratic follow-up input: `7c204c9d0e6a405216f9762ddd4d4d55ba57dab4`.
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


## 7. Verification and next load-bearing input

`certificates/a4d_native_composed_feedback_dynamics.lean` contains 115
compiled propositions, with each actual type and transitive axiom list
printed in its transcript. The receipt pins all five transitively imported
D0 sources and the actual toolchain inputs. Standard logical axioms only;
no new axiom or placeholder. The companion exact checker passes 421 controls and binds the book,
native matrices, complete-block identities, delayed archive control,
composed source, joint projection refinement, determinant scaling and
immutable result ledger. Finite controls do not replace the all-size proofs.

The remaining single G0b input is the **joint scene process with its admitted
coherent pair preparations, retained flag registration, common full-word
execution and quadratic event readings**. For the feedback component,
(29)--(35) replace a requirement for signed U tomography or inverse access.
The compiler and fixed calibration are constructed; physical actuation,
native admitted variations and uniform preparation bounds must follow from
their owners. The scene contribution to the full bootstrap, including its
heat-trace term, is still required. Apply the proved bounds with actual
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
