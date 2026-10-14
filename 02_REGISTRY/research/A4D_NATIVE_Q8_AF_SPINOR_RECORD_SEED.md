# Q8/Role, the first Fibonacci (M_2) block, and internal recording

Research synthesis, 14 October 2026. SOURCE #310 at
`36d87087fd4ee08f1a7946a8be135e3b8635d12d`.
Status: **exact finite kinematic seed and record witness; physical admission,
metric variation, and GR remain open**.

This note tests a concrete bridge suggested by the older golden-split notes.
The useful structure is not the scalar identity (Q(4)=1) alone. It is the
coincidence, with exact owners, between the role-phase quaternion extension,
the first noncommutative Fibonacci AF block, its Lorentzian determinant cone,
and the actual internal record transition. These structures fit together at
the level of finite representations. The note does not identify AF matrix
dimension with physical volume or a Jones step with physical time.

## 1. The role cocycle is the Pauli commutator

The existing D0 type is `Role = Fin(2) x Fin(2)`. Its canonical alternating
pairing is

\[
\omega(u,v)=u_1v_2+u_2v_1\pmod 2,
\]

and the existing Q8 extension has cocycle

\[
c(u,v)=u_1v_1+u_2v_2+u_2v_1\pmod 2.
\]

Let (X,Y,Z) be the Pauli matrices and set (S=iZ, T=iY). For
(u=(u_1,u_2)\in\mathbb F_2^2), define

\[
\pi(u)=S^{u_1}T^{u_2}.
\]

Then (S^2=T^2=-I), (ST=-TS), and direct multiplication gives

\[
\pi(u)\pi(v)=(-1)^{c(u,v)}\pi(u+v),\qquad
\pi(u)\pi(v)=(-1)^{\omega(u,v)}\pi(v)\pi(u).
\]

For the repository's labels (A=(0,0), B=(1,1), C=(0,1), D=(1,0)), these
matrices are

\[
\pi(A)=I,\quad \pi(B)=iX,\quad \pi(C)=iY,\quad \pi(D)=iZ.
\]

Thus the nonzero role classes are the three Pauli axes, up to the signs and
permutations already allowed by the role symmetries. A one-dimensional
representation cannot realize the nontrivial commutator: nonzero complex
scalars commute, while two distinct nonzero roles must anticommute. The
two-dimensional representation is therefore minimal. This is the explicit
matrix realization of the already-owned Q8/Role cocycle, not a new role
alphabet.

## 2. The first AF refinement contains the minimal Lorentz cone

The actual Fibonacci incidence gives

\[
A_0=\mathbb C\oplus\mathbb C,
\qquad A_1=M_2(\mathbb C)\oplus\mathbb C,
\qquad \iota_0(x,y)=(\operatorname{diag}(x,y),x).
\]

The unique noncommutative simple block of (A_1) is (M_2(\mathbb C)), the
same matrix algebra that carries the minimal Q8 representation. Any
*-identification of these two simple blocks differs by a unitary conjugation;
the determinant and positive cone are invariant under that freedom. This is
an isomorphism-class weld of one finite simple block. It does not identify the
whole Q8 group algebra or the full AF tower with the Role-phase point tower.

For a Hermitian element, write

\[
H=x_A I+x_B X+x_C Y+x_D Z
 =\begin{pmatrix}
x_A+x_D & x_B-i x_C\\
x_B+i x_C & x_A-x_D
\end{pmatrix}.
\]

Its exact determinant is

\[
\det H=x_A^2-x_B^2-x_C^2-x_D^2.
\]

The eigenvalues are (x_A\pm\sqrt{x_B^2+x_C^2+x_D^2}), so positive
semidefiniteness is exactly the closed future Lorentz cone; positive
definiteness is its interior. The identity direction is the unique scalar
direction and the traceless Hermitian subspace has dimension three. In this
enriched structure the signature ((1,3)) is selected by the matrix
determinant and positivity, with (A) as the identity role and (B,C,D) as
the three spatial axes. This does not contradict the existing result that
four role labels alone do not determine a signature: the Q8 representation
and the AF (M_2) block are additional structural inputs.

## 3. The golden state and the exact feedback weight

Put (p=\phi^{-1}\), so (p+p^2=1), and

\[
\delta_0=\frac{p-p^2}{2}=\frac{p^3}{2}.
\]

The supplied scalar dimensional formula is exactly
\(Q(D)=2\delta_0\phi^{D-1}=\phi^{D-4}\), hence \(Q(4)=1\); iterating the
same scalar split gives \(\delta_{-1}=\delta_0^2\). These identities are
checked exactly below. They fix a scalar normalization, not spacetime
dimension: the native AF tail has its own affine two-sector recursion.

The unique AF trace at level zero assigns the inherited diagonal projections
the weights (p,p^2). Pinching onto the diagonal algebra singled out by the
actual inclusion gives the normalized two-state density

\[
\rho_\phi=\operatorname{diag}(p,p^2),\qquad
\operatorname{Tr}\rho_\phi=1,\quad \det\rho_\phi=p^3.
\]

Use the doubled Pauli coordinates already used by the recorded-observer
readout: 2ρ = j_A I + j_B X + j_C Y + j_D Z, where
j = (Tr ρ, 2 Re ρ₀₁, −2 Im ρ₀₁, ρ₀₀ − ρ₁₁). For this diagonal state,
j = (1,0,0,p³), so

\[
j^T\eta j=4\det\rho_\phi=4p^3=8\delta_0,
\qquad p^6=4\delta_0^2,
\qquad 4p^3+p^6=1.
\]

The first scalar is the already-owned two-tick AF feedback eigenvalue; the
second is the already-owned prepared-corner weight. This is a no-fit equality
between two existing readouts, not proof that they are the same instrument or
the same physical observable.

There is a necessary state boundary here. The conditional restriction of the
full AF trace to the (M_2) block has density (I/2), not
\(\rho_\phi\). The latter is the ancestor's nontracial diagonal state,
extended to (M_2) by the canonical diagonal pinching. The diagonal weights
alone allow off-diagonal coherence; invariance under the inherited diagonal
phase group (equivalently the conditional expectation) removes it. Physical
admission of this prepared density remains open.

The freedom is observable: replacing \(\rho_\phi\) by
\(\rho_c=\begin{pmatrix}p&p^3/2\\p^3/2&p^2\end{pmatrix}\) preserves both
diagonal weights and has
\(\det\rho_c=p^3-p^6/4>0\), yet
\(\operatorname{Tr}(X\rho_c)=p^3\) whereas
\(\operatorname{Tr}(X\rho_\phi)=0\). Thus the inherited diagonal data do not
determine the state seen by a non-diagonal Role probe; the pinching is a real
preparation choice that needs its own native owner.

The actual Jones preparation gives a sharper answer. Let \(e\) be its owned
prepared corner in \(A_7\), and let \(P_0,P_1\) be the two inherited \(A_0\)
type projections. Restrict the normalized corner state
\(\omega_e(Y)=\tau_7(eY)/p^6\) to \(A_1=M_2\oplus\mathbb C\) using the six
literal AF inclusions. Exact contraction of all four \(M_2\) matrix units
gives

\[
\omega_e|_{M_2}=p^2 I_2,\qquad
\omega_e(M_2)=2p^2,\qquad
\omega_e(\,\cdot\mid M_2)=I_2/2.
\]

The type-conditioned states are
\[
\omega_{e,0}|_{A_1}=p\,|0\rangle\langle0|\oplus p^2,\qquad
\omega_{e,1}|_{A_1}=|1\rangle\langle1|\oplus0,\qquad
\omega_e=p\,\omega_{e,0}+p^2\,\omega_{e,1}.
\]
Thus the old-type-zero sector really does produce the same two probabilities
\((p,p^2)\), but they sit in different AF summands: the \(M_2\) outcome has
weight \(p\), and the scalar outcome has weight \(p^2\). Mixing both retained
old types gives equal \(p^2\) weights on the two \(M_2\) basis states, hence
the conditional \(M_2\) state \(I_2/2\), not
\(\rho_\phi=\operatorname{diag}(p,p^2)\). The exact Jones transition leaves
all four of these \(M_2\) matrix-unit expectations unchanged for these
prepared states. The golden pair is therefore an actual classical sector
record here. This particular corner does not give the Q8 spinor density. The
companion certificate binds this contraction directly to the owned ordered AF
matrices; it does not infer it from the matching scalar weights.

### The four-level activation also prepares the Q8 spinor marginal

The missing finite state map is supplied by a different, already-owned
transition: the four-copy activation represents the literal
`GoldenCoherentMemory.fullStep` in the actual AF right-module corner. At each
level its apparatus frame is
\(V:\mathbb C^4\otimes H_n\to H_{n+3}\), and the actual native operator is
\(W=V(U\otimes I)V^*+(I-VV^*)\). The complement remains an identity sector.
Use the existing blank frame \(|00\rangle\otimes\Omega_n\), where
\(\Omega_n\) is the normalized cyclic vector for the forced AF trace. The
owned gate equation gives, in the full retained carrier,

\[
W V(|00\rangle\otimes\Omega_n)
 =V\bigl((a|00\rangle+p|11\rangle)\otimes\Omega_n\bigr),
\qquad a^2=p,\quad p+p^2=1.
\]

Tracing out the record bit and the spectator gives the system density
\(\operatorname{diag}(a^2,p^2)=\operatorname{diag}(p,p^2)\); tracing out
the system instead gives the same density on the retained record. The full
apparatus state still contains its \(00\)-to-\(11\) coherence \(ap\), and
the complement is retained. Thus the AF-embedded activation does produce an
actual finite Q8-system state with Role expectations
\((I,X,Y,Z)=(1,0,0,p^3)\). The four-level startup is doing more than matching
scalar weights: its existing reversible gate generates the spinor marginal
and its internal record together.

This resolves the finite representation/readout map for the activation
apparatus. It does not identify that state with the distinct conditional
trace of the first \(A_1=M_2\oplus\mathbb C\) block, which remains \(I_2/2\)
in the Jones calculation. Nor does the mathematical representation prove
that the physical preparation law selects or executes \(W\), or that this
apparatus marginal is the metric/matter readout on \((q,D,b,m)\). Those
admissions are the remaining bridge.

## 4. The record transition supplies an internal change

The all-level Jones owner gives an actual unitary composite on the Fibonacci
AF refinement and retains every outcome and the orthogonal complement. In
its prepared old-type-zero sector, the exact two-bit table changes from

\[
\begin{pmatrix}p^2&p^3\\p^3&p^4\end{pmatrix}
\quad\longrightarrow\quad
\begin{pmatrix}p&0\\0&p^2\end{pmatrix}.
\]

Both row and column marginals stay ((p,p^2)); the first table is independent
and the second records one internal label exactly. The canonical full trace
is unchanged, and the failed/complement sector is retained. This is a
constructive internal record update. It can be tested as a candidate internal
clock because it distinguishes before and after through a retained
correlation, while the construction itself does not supply physical time.

The separate four-copy owner proves that the full-record apparatus first
fits after three AF inclusions: its conjugation-fixed capacities are
\(2,3,7,18\), and four copies need eight fixed directions. Including the
input, this is the four-level startup window. Beyond it, the same AF incidence
continues with Fibonacci growth; its normalized sector-weight tail contracts
with alternating factor (-p^2). The scalar cascade
\(\delta_{-n}=\delta_0^{n+1}\) is a different chosen scalar operation and
must not be substituted for that native AF transition.

## 5. Kill-first boundary: kinematics is not the native Lorentz dynamics

The determinant cone has the full algebraic spin action

\[
H\mapsto AHA^*,\qquad A\in SL_2(\mathbb C),
\]
which preserves \(\det H\) and realizes the connected Lorentz group on
Hermitian \(2\times2\) matrices. On one fixed \(M_2\) block, conjugation by
\(U\in U(2)\) fixes \(I\) and rotates the three-dimensional traceless Hermitian
subspace. It cannot equal a Lorentz boost, which moves the identity direction.
The exact checker includes a generic SU(2) identity-fixing control and a
determinant-preserving noncompact boost.

This rejects the shortcut “the Jones unitary, identified with an inner
automorphism of one fixed \(M_2\) block, is already a Lorentz link.” The exact
native corner contraction is now known: the golden \((p,p^2)\) pair appears as
a classical record across the \(M_2\) and scalar AF summands, while the
conditional state inside the full \(M_2\) block is \(I_2/2\); the owned Jones
step preserves all four matrix-unit expectations for these preparations.
This is a scoped result for the actual corner state, not a classification of
every possible conditional instrument.

The highest-value next calculation is now to pull this exact AF-embedded
spinor readout through the complete native \((q,D,b,m)\) preparation and its
constrained tangent. Compute the full action derivative, including the
retained record and complement, and compare all physical metric slots with
\(\rho_0\). The full-preparation owner already exhibits a price-changing
direction that preserves both marginals and the complete Jones table, so the
state law must handle that direction as well. The desired zero source may not
be built into admission. If the existing four-level operation is not admitted
by that state law, classify that failure for the explicitly owned preparation
class; do not promote the Jones-corner calculation to a whole-core NO-GO.

Failure of this (M_2)/Jones route would be a scoped obstruction. It would
not close the fixed-source/raw-owner parent, prove a whole-core NO-GO, or
settle OTO. The remaining terminal still requires the actual metric and link
source, Ward identity, ten-component response transfer, native stationarity,
curved joint roots, soundness, recovery, and physical constraints.

## Reproducible exact checks

The companion checker pins all source owners by SHA-256 and checks the full
16-entry Q8/Role product and commutator tables, the Hermitian (M_2)
determinant, the first AF path/dimension sequence, the exact golden density
and feedback/corner identities, the Jones record tables, and all four
matrix-unit expectations of the actual \(A_1\to A_7\) prepared-corner
restriction before and after the Jones transition. It also executes the
four-level AF-embedded gate on the canonical \(A_0\) cyclic vector and checks
the decoded full state, both system/record partial traces, and all Q8 Pauli
expectations. The Lean certificate proves the determinant form, the literal
gate output and its two exact marginals, plus the scalar golden identities;
it compiles under the repository's pinned Lean toolchain and uses only
standard Lean axioms.
Hostile controls keep the AF tracial state distinct from the ancestor density,
exhibit a positive coherent extension with the same diagonal but a different
Pauli-X readout, and reject boosts from fixed-block unitary conjugation.

Files:

- [checker](certificates/a4d_native_q8_af_spinor_seed_check.py)
- [pinned results](certificates/a4d_native_q8_af_spinor_seed_results.json)
- [Lean certificate](certificates/a4d_native_q8_af_spinor_seed.lean)
