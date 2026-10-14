# G0b: full-CAR current on the already owned closed native record sector

**Research / exact conditional theorem, 14 October 2026.**
Repository: \`gvakhrushev/d0_15\`. Original research owner: Draft
[#310](https://github.com/gvakhrushev/d0_15/pull/310), task
\`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`.
CONTROL [#322](https://github.com/gvakhrushev/d0_15/pull/322) remains a
separately reviewed checkpoint, **not** automatically re-certified by this
new research slice.

This document continues
[A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md](A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md)
§8 and [A4D_NATIVE_CLOSED_RECORD_ENGINE.md](A4D_NATIVE_CLOSED_RECORD_ENGINE.md).
The [exact standalone symbolic check](certificates/a4d_native_record_car_joint_sector_check.py)
is committed in this same existing SOURCE branch. No new execution task,
branch, action density, source selector, CORE owner or BOOK claim is installed.

## 1. The same full sixteen-component carrier, two separate invariant sectors

At the existing rest preparation fix \(q=\eta=\operatorname{diag}(1,-1,-1,-1)\),
the positive exterior pairing \(W=I_{16}\), retained reference \(u=e_0\),
and the actual native signed gate \(U_\sigma=U_{\sigma e_0}\), where the sign
is read from \(m_1\), never from an external tick counter. Put
\(p=\varphi^{-1}>0\) and \(a>0\) with

\[
a^2=p,\qquad p^2+p=1,\qquad a^2+p^2=1.
\]

Use the *literal* sixteen mask coordinates of the native CAR exterior
representation. The previously certified collinear closed-record executor
has invariant linear carrier

\[
S=\operatorname{span}\{e_0,e_1,e_6,e_7,e_{10},e_{11},
 e_{12},e_{13},e_{14},e_{15}\}\subset\mathbb R^{16}.
\tag{1}
\]

The actual transition is defined on the nonzero-first-grade part of this
carrier satisfying the inherited closed-engine band. It does **not**
follow that every \(m\in S\) is an admitted trajectory.

The *specific whole-blank seed* \(m_0=e_1+e_{15}\) lies in the smaller
reducing subspace

\[
V=\operatorname{span}\{e_0,e_1,e_{14},e_{15}\}\subset S.
\tag{2}
\]

Both signed gates leave \(V,S\) (and their orthogonal complements)
invariant. There is no deletion, trace-out or reduction of the
**ambient** sixteen-dimensional matter representation; these are
invariant-subspace statements about the current native operator.

## 2. Exact current classification on S

Write \(C_i\) for literal exterior creation and
\(A_i=C_i^\dagger\) for the \(W=I\) adjoint. The correlated CAR
current uses exactly the earlier owner's operators

\[
\beta=C_0+A_0,\qquad
\alpha_i=\beta(C_i-A_i)\quad(i=1,2,3),\qquad
J=e_0+\sum_i r_i e_i,
\quad r_i=\frac{\langle m,\alpha_i m\rangle}{\langle m,m\rangle}.
\tag{3}
\]

All three \(\alpha_i\) are selfadjoint and satisfy
\(\alpha_i\alpha_j+\alpha_j\alpha_i=2\delta_{ij}I\).
Direct full-CAR multiplication gives

\[
P_V\alpha_iP_V=0\quad (i=1,2,3).
\tag{4}
\]

Therefore, **every** nonzero state in the whole-blank seed's four-mask
space has \(J=e_0\). Since \(V\) is invariant under both signed native
gates, the original nonrepeating autonomous seed record has
\(J_t=e_0\) at every tick. Its source-producing current-defined
positive pairing stays \(h_J=I\), without implying that other direct
record-dependent terms vanish.

The larger ten-dimensional sector is different. Define pair coordinates

\[
h=(m_{14},m_{15}),\quad
w_1=(m_{12},m_{13}),\quad
w_2=(m_{10},m_{11}),\quad
w_3=(m_{6},m_{7}),\quad N=\langle m,m\rangle.
\]

The *complete* CAR expectations on \(S\) are

\[
(r_1,r_2,r_3)
=\frac2N\bigl(\det(w_1,h),-\det(w_2,h),\det(w_3,h)\bigr),
\quad \det((x,y),(u,v))=xv-yu.
\tag{5}
\]

On each high pair the actual engine applies the **same** matrix

\[
H_\sigma=
\begin{pmatrix} a&-\sigma p\\-\sigma p&-a\end{pmatrix},
\qquad \det H_\sigma=-a^2-p^2=-1.
\tag{6}
\]

The operator check is stronger than a sampled orbit calculation:

\[
P_S U_\sigma^\top\alpha_i U_\sigma P_S
=-(a^2+p^2)P_S\alpha_i P_S,\qquad
U_\sigma^\top U_\sigma=(a^2+p^2)I.
\tag{7}
\]

Consequently, on **every admissible** signed native transition in \(S\),

\[
\boxed{\mathbf r_{t+1}=-\mathbf r_t,\quad
  \|\mathbf r_{t+1}\|=\|\mathbf r_t\|,\quad
  \eta(J_{t+1},J_{t+1})=\eta(J_t,J_t).}
\tag{8}
\]

In particular, the native engine cannot **create** a nonzero CAR spatial
current starting from zero while staying in this unchanged sector.
This is an exact restricted dynamical obstruction, not a NO-GO for all
possible native interactions.

## 3. A positive nonblank witness, with its essential preparation boundary

Take the full native state with exactly

\[
m_1=m_6=m_{15}=1,\qquad m_i=0\ \text{otherwise}.
\tag{9}
\]

The inherited \((m_0,m_1)\) low-band and \((m_{14},m_{15})\)
high-band coincide with the original certified seed. Thus the
all-time nonzero-first-grade guard and infinite-order high-pair
recurrence from the old proof remain available: adding \(m_6\) does not
alter those components. The vector stays in \(S\), and the same
state-selected program runs without new blanks.

On this new seed, \(N=3\) and

\[
\boxed{
J_t=(1,0,0,(-1)^t\,2/3),\qquad
\eta(J_t,J_t)=5/9>0.
}
\tag{10}
\]

So the already owned closed record engine and a nonzero uniformly
future-timelike CAR current do coexist on one complete 16-component
carrier **conditionally on the nonblank initial state being admitted**.
No fresh physical field, external spatial frame or additional operator
is needed for this algebraic representation statement.

But the *actual* whole-blank projector from the signed native
apparatus satisfies

\[
\dim(S\cap \operatorname{im}P_{\rm blank})=2,
\qquad
S\cap\operatorname{im}P_{\rm blank}
=\operatorname{span}\{e_0+e_{14},e_1+e_{15}\}.
\tag{11}
\]

Every state in this intersection has zero current by (4). The witness
(9) is not whole-blank. Equations (8) and (11) rule out deriving its
nonzero current by **only** iterating the existing closed-sector
program from one of those blank states. They do not exclude a different
native admitted preparation or an interaction that leaves \(S\).

## 4. Endpoint-isometry obstruction to a gratuitous readout swap

Even admitting (9) as a mathematical input is not a common physical
preparation of gate, observer pairing and source. Set its current-derived
metric by the already owned correlated-current formula

\[
h_J=-\eta+\frac{2(\eta J)(\eta J)^\top}{J^\top\eta J}.
\]

For \(J=(1,0,0,2/3)\) it has determinant one, eigenvalues
\((5,1/5,1,1)\), and

\[
(h_J)_{00}=13/5.
\tag{12}
\]

Try to **keep the old** \(U_{\sigma e_0}\), originally orthogonal for
\(W=I\), while replacing only the full exterior pairing by
\(W_J=C_*(h_J)\). Its scalar basis column maps to
\(a e_0+\sigma p e_1\); the grade-0 and grade-1 Gram blocks are
orthogonal, with weights \(1\) and \((h_J)_{00}\). Therefore

\[
\langle U_\sigma e_0,U_\sigma e_0\rangle_{W_J}
 -\langle e_0,e_0\rangle_{W_J}
 =a^2+\frac{13}{5}p^2-1
 =\boxed{\frac85p^2>0}.
\tag{13}
\]

The opposite-current endpoint has the same \((h_J)_{00}\), so even
the two-endpoint scalar-column test does not repair the mismatch.
Hence **changing only the observer/current readout is not an
endpoint-isometric physical joint transition**. A truly updated
operator, pairing and action must come from a declared owned
interaction, not by declaring this defect to be zero.

Equation (13) is a necessary-test failure for this attempted identification,
not a theorem excluding all conformal/transformed gates or arbitrary
metric/connection dynamics.

## 5. Proof status, acceptance and next arrow

The attached executable checker verifies the sixteen signed CAR matrices,
three Clifford/selfadjoint tests, the \`V\` compression, both signs on
all ten carried coordinates, the general bilinear current formula,
the actual signed blank projector and two-dimensional intersection,
the positive nonblank witness and the exact nonzero Gram defect.
It uses only SymPy for exact rational/polynomial matrix operations.
The all-time statements follow analytically from invariant blocks,
determinants and the existing closed-engine induction; no finite run
is used as an infinity proof.

**This is a SOURCE research continuation only.** It does not replace the
existing immutable correlated-current certificate, alter the 448-artifact
CONTROL intake, compile new Lean, close the physical G0b obligation,
change task lifecycle, or promote a claim.

**Next required arrow:** derive a physically admissible blank-to-spatial-
correlated operation (or justify a nonblank preparation from existing
owned primitives), together with joint endpoint pairing and retained
history, complete feedback/heat/action variation on true
\((q,D,b,m)\)-curves, and compatible archive refinement. The
previous \(r'(0)=8\delta_0\) belongs to a *different*, separately
prepared source-active sector until such a weld is demonstrated.
Physical source/Ward, stationarity, quantitative transfer, curved
roots, soundness/recovery, GR and original #310/#202/#317 remain open.


## 6. The original whole-scene autonomous compiler cannot excite the zero-current sector

The existing [autonomous scene-record compiler](A4D_NATIVE_AUTONOMOUS_SCENE_RECORD.md)
uses the fixed forward program on all 718 directed edges of the genuine
K(9,11,13) scene, two values of the permanent controller bit and all
sixteen Fock coordinates:

\[
\mathcal H=\mathbb R^{718}\otimes\mathbb R^2
               \otimes\Lambda^*(\mathbb R^4),
\quad \dim\mathcal H=718\cdot2\cdot16=22976.
\tag{14}
\]

Its displayed chronological factors are \`C_fN, G_N, C_fN, C_cN,
G_N, C_cN, U_+, C_cf\`, with \`U_+\` expanded to two forward primitives;
this is the **already owned** nine-primitive word, not a new program.
The two controlled registers act by flipping the *temporal occupation
bit* N when their control is set; \`G_N\` rotates the temporal
occupation pair uniformly; \`U_+\` is the native full signed
gate; \`C_cf\` acts on controller/scene orientations only.

Let \(\Pi_V\) denote the orthogonal projector onto the four-mask
space (2), and \(\widehat\Pi_V=I_{718}\otimes I_2\otimes\Pi_V\).
The temporal-bit flip \(X_N\), golden rotation \(G_N\), both
native signs \(U_{\pm}\) and the identity all preserve \(V\)
*and its orthogonal complement* on the complete sixteen-coordinate
matter fibre. Their controlled block versions preserve the corresponding
global subspace. Scene/controller-only reversals preserve it as well.
Therefore the actual compiled word \(\mathcal W\) reduces this
subspace:

\[
\mathcal W\,\widehat\Pi_V
 =\widehat\Pi_V\,\mathcal W,\quad
\widehat\Pi_V\,(I_{718}\otimes I_2\otimes\alpha_i)
 \,\widehat\Pi_V=0\qquad(i=1,2,3).
\tag{15}
\]

The first identity holds for an **arbitrary finite product** of these
owned generators; the second is (4) tensored with the whole
scene/controller identity. Hence even an entangled scene/controller/
matter state supported in \(\operatorname{im}\widehat\Pi_V\)
has **zero** spatial current expectation after any number of actual
compiled steps. The all-scene fixed word retains an internal switching
record and a nonconstant price, but these features alone do not turn
the source-inactive native whole-blank orbit into the source-active
sector of the independent correlated-current owner.

The exact checker verifies every 16-mask primitive's cross-block zeros
and the genuine full-scene dimension, not an impractical
22976-by-22976 sampled matrix. Tensor-factor preservation and closure
under products prove (15) at all word lengths. This is a restriction
on the *specified compiled palette and preparation*, not a no-go for
all D0 interactions, general fields or physical spacetime links.

**Sharpened constructive target:** identify an **already owned**
same-carrier operation whose actual represented matrix has a nonzero
\(\Pi_{V^\perp}T\Pi_V\) coupling and whose joint source/price action,
frame covariance, retained memory and physical admission are established.
Alternatively derive a permitted correlated nonblank initial preparation.
Adding another edge-reversal controller that acts only outside the
matter subspace cannot satisfy this target.
