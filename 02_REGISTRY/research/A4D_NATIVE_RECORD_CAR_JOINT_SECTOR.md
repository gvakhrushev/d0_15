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


## 7. Proper spatial symmetry fixes the exact missing input type

The finite full-Fock obstruction can be stated independently of a
particular compiled word. At fixed \(q=\eta,u=e_0\), the stabilizer of
the retained reference contains \(SO(3)\). It acts by its **actual
exterior lift**, preserving all sixteen masks. Let \(R_{12}\) and
\(R_{23}\) be the two exact \(90^\circ\) spatial quarter-turns in the
\(e_1e_2\) and \(e_2e_3\) planes, and \(E_{12},E_{23}\) their full
sixteen-dimensional exterior matrices. The exact rational calculation
gives

\[
\operatorname{rank}(E_{12}-I)=8,\qquad
\operatorname{rank}
\begin{bmatrix}E_{12}-I\\E_{23}-I\end{bmatrix}=12,
\quad
\ker(E_{12}-I)\cap\ker(E_{23}-I)=V.
\tag{16}
\]

Every vector of \(V\) is already fixed by *all* proper spatial
rotations: its masks are the scalar, temporal first grade,
spatial orientation volume, and full four-volume. Thus (16)
establishes exactly

\[
(\Lambda^*\mathbb R^4)^{SO(3)}=V,
\tag{17}
\]

without approximating the group by a sampled angle or discarding any
spectator grades. One quarter-turn alone leaves eight directions;
using only it would be an insufficient symmetry test.

Now consider **any** operation \(T\), linear or nonlinear, equivariant
under this stabilizer, whose other inputs are scalar/unchanged under
proper spatial rotations (for example, a controller or archive
label with no represented spatial orientation). An invariant input
\(\psi\) obeys \(E(g)\psi=\psi\), hence

\[
E(g)T(\psi)=T(E(g)\psi)=T(\psi)\quad\forall g\in SO(3).
\]

By (17), \(T(\psi)\in V\); by (4), its spatial CAR current is zero.
For scene/controller Hilbert factors carrying the trivial \(SO(3)\)
action, the same argument uses \(H_{\rm record}\otimes V\).
This holds for arbitrary record-dependent equivariant **nonlinear**
updates as well as the fixed word of Section 6; it is not an
operator-counting or bounded-word no-go.

**Necessary new input type (not an installed primitive):**
an allowed spatially transforming relative datum (e.g. a genuine
coframe/link/matter correlation with an owned comparison interface),
or a physically justified non-\(SO(3)\)-invariant preparation, must
enter before a nonzero vector can be selected from the invariant
blank state. The nonblank witness (9) supplies that spatial direction
as initial state data, not as a derivation from M1. A simultaneously
transported frame change, which transports the reference and all
readouts, is just covariance and cannot be mistaken for generated
relative current.

Equation (17) is a **precise symmetry gate** on the same G0b
physical-admission obligation. It does not classify fields that
carry nontrivial spatial representations, prohibit spontaneous
symmetry breaking in larger admissible models, or produce a physical
source/Ward theorem.


## 8. Ladder gate T0 → T1: the full native two-record price is constant

The scientific objective is **not** the existence of another recording
model. The T0→T1 contract in
[D0_NATIVE_TANGENT_SOURCE_PLAN_2026-10-09.md](D0_NATIVE_TANGENT_SOURCE_PLAN_2026-10-09.md)
requires an *owned physically admitted* preparation and the differential
of its complete heat/feedback/Gram price on a common constraint tangent.
Here we close a candidate **matter-only contribution** exactly, so the
ladder does not continue chasing spatial current without an actual
native coupling.

Keep the very same rest collinear interface as above:
\(q=\eta,\ Q=G=I,\ W=I_{16}\), identity spatial links
\(D_e=I\), zero shifts, the retained cut \(P=I-N_0\),
and the literal native state-selected operator \(U_\sigma\).
These are fixed **values** of geometric fields, not a law fixing
them for all physical metric probes. The first-grade sign may change;
the entire first/second-transaction sequence is retained.

For any two consecutive signed native record operators, set

\[
K_{\sigma_2,\sigma_1}=U_{\sigma_2}U_{\sigma_1},\qquad
F_{\sigma_2,\sigma_1}
 =P K_{\sigma_2,\sigma_1}^{\top}
   (I_{16}-P)K_{\sigma_2,\sigma_1}P.
\tag{18}
\]

The four combinations \((\sigma_1,\sigma_2)\in\{+,-\}^2\)
have exactly the **same complete nonzero feedback spectrum**.
For equal signs, the four nonzero eigenvalues occur on the even
spatial-degree 0/1 pairs with masks \(\{0,2,4,8\}\);
for opposite signs they occur on the spatial-degree 2/3
pairs with masks \(\{6,10,12,14\}\).
For each nonzero mode, the eigenvalue is

\[
4a^2p^2=4p^3=8\delta_0\,p^0\ \text{(using }a^2=p\text{)};
\tag{19}
\]

the final expression \(4p^3=8\delta_0\) follows from
\(\delta_0=p^3/2\), as already owned. All twelve other
eigenvalues remain *explicitly* zero; they are not deleted
or divided away. The exact full-carrier determinant is

\[
\boxed{\det(I_{16}-zF_{\sigma_2,\sigma_1})
      =(1-4zp^3)^4},\qquad 0<z<1.
\tag{20}
\]

The certificate computes (18) on **all 16 mask rows** for all
four sign pairs and proves \(F^2=4p^3F\) after golden
substitution. No sampled eigenvalue argument is used.
Equation (20) is the original \(-\log\det\) functional,
not a new feedback definition.

For every smooth admitted variation of the **higher matter
coordinates** in the regular collinear band, with the
low first-grade sign history fixed and all geometric
fields \(q,D,b\) held at these values, \(U_\sigma,P,W\)
and the native Hodge operator of this homogeneous
geometric interface have zero variation.
Even if the *alternative* full-CAR current varies,
the two-tick feedback contribution is constant by (20),
and the native geometric heat contribution is constant
because its full operator and pairing are unchanged.
Therefore

\[
d_m\bigl(H_{\rm native}+J_2\bigr)[\dot m]=0
\tag{21}
\]

**on this exact restricted interface**. If the full action
contains further matter terms, (21) is not their derivative;
it is not a statement about variations changing \(q,D,b\),
different observer/heat bindings, the true physical field
equations, or the ten metric-source rows. It is not a claim
that the physical joint tangent contains all such variations.

The distinction is decisive for the closure ladder:
a spatially nonzero \(\mathbf r(m)\) by itself does **not**
make that same native readout a varying argument of the
actual heat/feedback action. Replacing the pairing by
\(h_J\) fails endpoint-isometry by (13). Transporting a
frame and all fields together is covariance, not a
new physical response. The existing record-only,
flat-collinear heat-plus-two-tick-feedback route has now
been classified completely for the stated signed gate
class and cannot by itself supply a nonzero matter-source
on this fibre.

An explicit nonzero-versus-zero differential makes the inference
firewall observable on the same 16-component carrier.
Perturb only \(m_6\) in the positive-witness state (9), writing
\(m_6(t)=1+t\) while \(m_1=m_{15}=1\).
The owned normalized full-CAR expectation is

\[
r_3(t)=\frac{2(1+t)}{3+2t+t^2},
\qquad r_3'(0)=\frac29\ne0.
\tag{22}
\]

The initial observer sign remains positive; this is an actual
same-carrier matter curve in the regular collinear band.
The whole native signed two-tick feedback and homogeneous Hodge
operator remain fixed, so their **combined matter derivative is zero**.
Thus this is a sharp example where \(DR_{\rm CAR}[\dot m]\ne0\)
but \(d_mS_{\rm native}[\dot m]=0\) for this restricted
heat-plus-feedback interface. It does not assert that the full
D0 field action has zero matter derivative or that this tangent
has independently been physically admitted.

**Return immediately to the T0 owner obligation, without
another symmetry or word search:** derive from the actual
physical preparation one joint field/readout rule which
couples the already-owned CAR/record state into the
native \((q,D,b,m)\) heat/price operators, and justify
its full endpoint/constraint variations. A candidate
must expose a nonzero genuine price/response jet
rather than merely a changed current observable.
Then and only then compute the full constrained covector,
all ten source components, Ward, stationarity and
refinement. If no current candidate meets this test,
record the one explicit missing physical-interface lemma,
not a universal D0 impossibility theorem.

## 9. The blank-to-current CAR tick fails the direct endpoint-metric weld

This exact check tests the specific base-level AF/CAR route in the preceding
correlated-current owner. Its AF blank welds to
\(m_0=B(a,p)\in\operatorname{im}P_{\rm blank}\), and one literal full-CAR
record step gives \(m_1=Um_0\). The step creates the already owned current

\[
J_0=(1,0,0,0),\qquad J_1=(1,2ap,0,0),\qquad
J_1^T\eta J_1=p^6>0.
\tag{23}
\]

Take the current-defined positive pairing from the same CAR-current owner,
\(h_J=-\eta+2(\eta J)(\eta J)^T/(J^T\eta J)\). Then \(h_0=I_4\), while
\((h_1)_{00}=2/p^6-1\); its \((0,1)\) block has determinant one and positive
leading entry, so \(h_1\) and its full exterior Gram \(W_1=C_*(h_1)\) are
positive. The original literal gate \(U\) is orthogonal for \(W_0=C_*(h_0)=I_{16}\).

However, its scalar-mask column is
\(Ue_{\varnothing}=a e_{\varnothing}+p e_{\{0\}}\). The full exterior metric
has no cross-grade term, so this single column gives the exact necessary-test
defect

\[
\langle Ue_{\varnothing},Ue_{\varnothing}\rangle_{W_1}
-\langle e_{\varnothing},e_{\varnothing}\rangle_{W_0}
=a^2+p^2(2/p^6-1)-1
=\boxed{8/p=8(1+p)>0}.
\tag{24}
\]

Thus \(U^T W_1 U\ne W_0\): the actual blank-to-current step does not
transport the positive pairing inferred from its own source current. This
rules out that **direct fixed-gate/current-pairing identification** as the
joint metric weld. It does not rule out an independently derived link update,
a field-dependent gate, or another native pairing; none is installed here.
The exact checker pins the three consumed matrix owners and retains the full
16-state gate and exterior Gram. Its one-column witness suffices to disprove
whole-operator isometry; it does not claim the full defect has rank 16.

The source-active CAR readout therefore now has two distinct integration
boundaries: the state-selected closed engine cannot reach it from its own
blank sector, and the AF/CAR blank tick cannot be paired with \(h_{J_1}\) while
keeping its old gate. The next positive proof must derive the common
\((q,D,b,m)\) endpoint update and price variation from an existing native
owner. The full source/Ward, stationary roots, refinement transfer, curved
solutions, soundness/recovery and GR remain open.

Certificate: [exact source-endpoint metric check](certificates/a4d_native_source_endpoint_metric_check.py),
[immutable result](certificates/a4d_native_source_endpoint_metric_results.json).
