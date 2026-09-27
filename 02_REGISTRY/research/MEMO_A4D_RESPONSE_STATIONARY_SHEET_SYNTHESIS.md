# A4D / FUGU: moving metric germ, stationary sheets, and response defects

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`  
Execution: PR #240, existing task branch  
Input head: `dcedd5760bda65a238e8655964c1ee02e03f63ad`  
Status: exact symbol identity + research theorems + conditional closure route.  
Neither `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED` nor
`A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO` is claimed.

This note consumes the supplied FUGU v1-v5 files, discussion, and v7 text.
It supplements the primary response memo. It does not register child tasks,
change the action, or promote a claim/BOOK result.

## 1. The synthesis

There are two different derivatives of the same variational system:

* frequency variation of a **metric-only null vector**;
* metric variation of the quadratic action of a **connection null vector**.

The first has an explicit moving-kernel identity. The second is the possible
macroscopic response defect. Vanishing of the first does not imply vanishing
of the second. Both fit a kernel-to-cokernel deformation map, but occupy
different entries of that map.

The correct macroscopic object is the metric derivative of the action on
connection-stationary sheets, or equivalently its quadratic correlation
defect. Connection uniqueness is unnecessary. A smooth connected family of
critical points that extends in the metric has one response. Singular or
disconnected critical branches require a separate comparison of their
critical values.

The global linear null-form condition (NF) in the primary memo is false.
Replacing it by a larger first-order image does not repair it. The remaining
question is whether the nonzero stress directions are **realizable by the
nonlinear equations with the prescribed smooth source and fixed background**.

## 2. Exact moving metric germ: a symbol complex, not nine coincidences

Use the #216 owner notation

\[
 B(z)=H_{AQ}(z)\in\mathbb C^{24\times10},\qquad
 d_r(z)=z_r^{-1}-1,\qquad q_0(z)=d(z)d(z)^T.
\]

Here a symmetric matrix is represented by its ten entries, with off-diagonal
coordinate directions paired with \(E_{ij}+E_{ji}\), exactly as in the owner.
The superscript \(T\) in \(dd^T\) is the algebraic transpose, not conjugation.
The identity is

\[
 \boxed{B(z)\,\operatorname{vec}_{\rm sym}(d(z)d(z)^T)=0.} \tag{G0}
\]

This is an identity of Laurent rational functions on \((\mathbb C^\times)^4\).
It is not restricted to fourth roots. On each of the nine specified orbits,
\(\operatorname{rank}B=9\), so this vector spans the complex metric-only
kernel. Its conjugate-paired real carrier has dimension two.

The identity has a direct all-solder proof. Let \(E\) be any invertible real
solder, \(Q=E^T\eta E\), and use the actual horizontal Gram lift. For
\(q=dd^T\),

\[
 \delta E=\tfrac12 EQ^{-1}dd^T,\qquad
 \delta E_r=\tfrac12 d_r U,\quad U=EQ^{-1}d.
\]

The complementary area variation is

\[
 \delta(E_u\wedge E_v)
 =\tfrac12 U\wedge(d_uE_v-d_vE_u).
\]

The mixed action pairs this role two-form with
\(d_r X_s-d_s X_r\), alternating over \((r,s,u,v)\). Every term therefore
contains the role factor \(d\wedge d=0\). The fixed internal bivector pairing
and Hodge map do not change this cancellation. Thus (G0) holds for the same
constant-solder symbol at every nondegenerate \(E\).

This gives a two-arrow symbol complex

\[
 \mathbb C\xrightarrow{\;P(z):f\mapsto f\,dd^T\;}
 \operatorname{Sym}^2\mathbb C^4
 \xrightarrow{\;B_E(z)\;}\mathbb C^{24},\qquad B_EP=0.
\]

It resembles the symbol of a scalar Hessian. This note does **not** identify
it with a new exact nonlinear gauge symmetry.

Differentiating (G0) gives the explicit absorption formula

\[
 (D_z B[\delta z])q_0+B\,D_zq_0[\delta z]=0, \tag{G1}
\]
\[
 \delta d_r=-z_r^{-2}\delta z_r,\qquad
 \delta q=\delta d\,d^T+d\,\delta d^T,\qquad\delta p=0.
\]

Therefore the moving germ continues through the **full linear joint system**:
the connection row is (G1), and the metric row vanishes because \(\delta p=0\).
No surjectivity of a connection block is needed. Normalizing \(q_0\) only adds
a multiple of \(q_0\) to its derivative, which is also killed by \(B\).

Crucially, \(\delta q\) is generally **not** in the old fiber \(\ker B(z)\).
If \(\delta q\in\ker B(z)\), it cannot absorb a nonzero \(w\). The derivative
is tangent to the moving kernel bundle, not constrained to its frozen fiber.
This corrects the corresponding sentence in v7 while proving its moving-germ
conclusion in a stronger form.

At \(z=(1,1,1,1)\), \(d=0\), so this particular generator vanishes. No
one-dimensional-kernel assertion at the zero character follows from (G0).

## 3. Physical Fourier pairing corrects the v7 rank table

Let \(z\) now label the physical character. In the owned convention the
physical connection block is \(A(z)=H_{AB}(z)^T\), while the lower mixed
block is \(B(z)=H_{AQ}(z)\). On the unit torus the full physical Hessian is

\[
 \mathcal J(z)=
 \begin{pmatrix}0&B(z)^\dagger\\B(z)&A(z)\end{pmatrix},\qquad
 \mathcal J(z)^\dagger=\mathcal J(z). \tag{P}
\]

Equivalently, using table character \(\zeta=z^{-1}\), the lower row is
\([H_{AB}(\zeta)\mid H_{AQ}(\zeta^{-1})]\). Inverting just one of these
blocks changes the problem.

The exact audit gives:

| Orbit | Physical rank \([A\mid B]\) | Physical cokernel dimension | Rank of the unpaired \([H_{AB}(z)\mid H_{AQ}(z)]\) |
|---|---:|---:|---:|
| 0 `(0,0,1,1)` | 23 | 1 | 23 |
| 1 `(0,0,1,3)` | 24 | 0 | 24 |
| 2 `(0,1,1,2)` | 24 | 0 | 24 |
| 3 `(1,0,1,2)` | 24 | 0 | 24 |
| 4 `(1,1,1,1)` | 20 | 4 | 20 |
| 5 `(1,1,3,3)` | **23** | **1** | 24 |
| 6 `(2,0,1,1)` | 24 | 0 | 24 |
| 7 `(2,1,1,2)` | **23** | **1** | 24 |
| 8 `(2,1,2,3)` | 24 | 0 | 24 |

The unpaired column reproduces the supplied v7 ranks. In particular the
physical cokernel on orbit 5 is not zero. Nevertheless the **specific**
forcing of the moving metric germ has zero class in that cokernel by (G1).
This is the difference between a zero obstruction class and a zero
obstruction space. Neither the sum 5 in v7 nor its corrected sum 7 is assigned
physical meaning.

For an arbitrary forcing, testing only the connection row is insufficient:

\[
 A\delta p+B\delta q=-w,\qquad B^\dagger\delta p=0
\]

are both required. A full-row-rank \([A\mid B]\) need not make this joint
system solvable. For example, take
\(A=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\),
\(B=(1,0)^T\), and \(w=(0,1)^T\). The lower row is surjective, but its
second equation forces \(\delta p_1=-1\), contradicting the upper row.
The special moving germ avoids this problem through its explicit solution.

The familiar auxiliary matrix also becomes transparent:

\[
 \boxed{\ker(A+iBB^\dagger)=\ker A\cap\ker B^\dagger.} \tag{F}
\]

Indeed the imaginary part of \(v^\dagger(A+iBB^\dagger)v=0\) is
\(\|B^\dagger v\|^2=0\); then \(Av=0\). The converse is immediate.
This is a detector of the linear connection-only joint kernel. It is not a
detector of metric stress. Replacing \(BB^\dagger\) by \(BB^T\) invalidates
this argument in a complex character basis.

## 4. One intrinsic deformation map unifies the two channels

For any smooth family of linearized equation maps \(\mathcal J_\lambda\),
define

\[
 \mathfrak O_\lambda(\dot\lambda):
 \ker\mathcal J_\lambda\longrightarrow\operatorname{coker}\mathcal J_\lambda,
 \qquad u\longmapsto[(D_\lambda\mathcal J[\dot\lambda])u]. \tag{O}
\]

This map is independent of a choice of projector. Under invertible changes
of domain/codomain bases, the extra differentiated terms are killed either
by \(\mathcal Ju=0\) or by the quotient modulo \(\operatorname{im}\mathcal J\).
Its vanishing is precisely the solvability condition for a first-order
continuation of the null vector. On a Hermitian physical carrier it can be
paired with another kernel vector:

\[
 \Omega_\lambda(v,u;\dot\lambda)=v^\dagger(D_\lambda\mathcal J[\dot\lambda])u.
\]

There are now two distinct entries:

1. **FUGU entry.** \(u=(q_0,0)\), \(\dot\lambda=\delta z\).
   Its class vanishes by (G1). The frozen \(G\) quotients by a smaller image
   because it disallows the motion \(D_zq_0\).
2. **Response entry.** \(u=v=(0,b)\), with
   \(Ab=B^\dagger b=0\), and \(\dot\lambda=q\) a background Gram variation.
   This entry is
   \[
    \Omega((0,b),(0,b);q)=b^\dagger D_QA[q]b.
   \]
   Half of it is the mean quadratic metric response.

Thus the entire moving-germ channel may be exact while the response entry
is nonzero. The shear witness in the primary memo realizes precisely this
linear algebraic possibility:

\[
 E=\begin{pmatrix}1&1&0&0\\0&1&1&0\\0&0&1&0\\0&0&0&1\end{pmatrix},\quad
 z=(-1,1,-1,1),\quad
 b^TD_QA[q_{11}]b=-2.
\]

Its normalized nonzero entries are
\(b_5=1,b_{14}=-1,b_{16}=-1,b_{17}=1,b_{18}=2,b_{19}=1,b_{21}=1\),
with role-major generator order \((K_1,K_2,K_3,J_{12},J_{13},J_{23})\).
It lies in the joint kernel, whose dimension there is one. This refutes
universal (NF), not response decoupling for exact nonlinear sequences.

If a null vector extends smoothly in a background direction at **fixed
character**, differentiating \(A(Q)b(Q)=0\) gives
\(b^\dagger D_QA[q]b=0\). This explains the all-solder diagonal theorem:
the quarter-wave connection kernel has constant rank as the solder varies.
If continuation instead requires moving the character, then

\[
 b^\dagger D_QA[q]b
 =-b^\dagger D_\theta A[D_Q\theta[q]]b. \tag{D}
\]

Equation (D) is a dispersion/transport relation, not a vanishing theorem.
A moving resonance can carry a metric response.

## 5. Exact envelope theorem for connected stationary sheets

Let \(S(Q,a)\) be the finite real action in a common link-coordinate chart,
\(F=\partial_aS\) the coordinate connection Euler covector, and
\(R=\partial_QS\) the actual metric response with the link fixed.

**Proposition.** Suppose \(a(Q,s)\), \(0\le s\le1\), is a differentiable
family defined on an open metric neighborhood and
\(F(Q,a(Q,s))=0\) for all \((Q,s)\). Then

\[
 R(Q,a(Q,1))=R(Q,a(Q,0)). \tag{E}
\]

**Proof.**
\(\partial_sS(Q,a(Q,s))=F\cdot\partial_sa=0\), so the on-shell action is
independent of \(s\). Differentiate this equality in \(Q\). The chain-rule
terms involving \(\partial_Qa\) vanish because \(F=0\). This yields (E).

No uniqueness, gauge equivalence, or connection compactness enters the
proof. Existence of a family only at one fixed \(Q\) is insufficient: its
action can be constant along the fiber while its metric derivative changes.
Nor does a submersion on two disconnected stationary sheets alone identify
their responses; their critical values must still be compared.

At a single stationary point, the obstruction to a horizontal metric lift
\(u\) is

\[
 H_a u+B_a q=0,\qquad H_a=S_{aa},\quad B_a=S_{aQ}.
\]

For a vertical tangent \(v\in\ker H_a\),

\[
 D_aR[v][q]=\langle v,B_aq\rangle.
\]

This is the same Fredholm pairing as (O). Response variation along a
stationary fiber measures the obstruction to transporting that fiber in
the metric. It is an obstruction to continuation, not evidence that the
connection is gauge.

### Quantitative identity suitable for the h-limit

Use the physical pairing \(\langle f,g\rangle_h=h^4\sum_x f_x\cdot g_x\).
For any path \(a_h(s)\) at fixed \(Q_h\), a smooth metric test \(\phi\), and
any proposed lift \(u_h(s,\phi)\), put

\[
 r_h=H_{a_h}u_h+B_{a_h}\phi.
\]

Symmetry of the **coordinate** Hessian gives the exact identity

\[
 \boxed{
 \langle R(a_h(1))-R(a_h(0)),\phi\rangle_h
 =\int_0^1\bigl[
 \langle\dot a_h,r_h\rangle_h
 -\langle\partial_sF(a_h),u_h\rangle_h\bigr]\,ds .} \tag{H}
\]

Consequently the normalized tested response vanishes if

\[
 \int_0^1\|\dot a_h\|_{2,h}\,ds=O(h),\qquad
 \sup_s\|r_h\|_{2,h}=o(h),\qquad
 \int_0^1|\langle\partial_sF,u_h\rangle_h|\,ds=o(h^2). \tag{HL}
\]

On an exact stationary path the last term is zero. Formula (H) also permits
an approximate smooth comparator, provided the displayed error is controlled.
Right-trivialized link Euler equations must first be converted to the common
coordinate gradient; their zeros agree, but an off-shell Hessian need not
be represented by the same matrix.

(HL) is a concrete alternative sufficient condition to global (NF), imposed
only along relevant solution paths. Its existence for every admissible
sequence is **not** proved here. It does not cover disconnected critical
branches automatically.

## 6. The reduced action, rather than separate rank tables

On a fixed finite cell, where a chosen range block is invertible, eliminate
the range variables in the connection equation and obtain a reduced action
\(\Phi(Q,\alpha)\). Subtract the chosen smooth-sheet action. Then

\[
 \partial_\alpha\Phi=0\quad\text{is the reduced connection equation},\qquad
 \partial_Q\Phi\quad\text{is its metric response difference}. \tag{LS}
\]

Both must come from the **same** reduced action and the same Fourier/source
convention. At a resonant point,

\[
 \Phi(Q,\alpha)=\tfrac12\alpha^*M(Q)\alpha+
 \Phi_{\ge3}(Q,\alpha),\qquad M(Q_0)=0,
\]

and the leading response is \(\tfrac12\alpha^*D_QM[q]\alpha\). Its
vanishing on the whole linear kernel is stronger than its vanishing on the
nonlinear critical set \(\{\partial_\alpha\Phi=0\}\).

The exact curved #232 vacuum is the indispensable response-null control.
The all-solder diagonal moment theorem proves its frozen leading quadratic
channel is silent. It does not by itself construct its continuation on a
nonconstant background.

The recent period-two shear/chain calculations in PR #240 instead report
a reduced connection coefficient \(-432u^5\) after lower-order corrections.
Such a coefficient, if established for the complete stated ansatz, is a
**fifth-order** obstruction. It cannot be reinterpreted as a nonzero
quadratic coefficient of the bare connection Euler map. At order two,
the actual equation is

\[
 H a_2+N_2(a_1,a_1)=0,
\]

so even a nonzero bare \(N_2\) need not obstruct continuation. In fact the
order-five certificate explicitly uses a second-order range correction.
The file `a4d_joint_response_joint_critical_check.py` at the input head checks
only linear kernel membership; its printed quadratic terminal does not
follow from its computations. This note does not adopt that terminal.

A fixed-cell cutoff does not automatically exclude slowly modulated packets,
sidebands, or other carrier combinations. Their derivative and background
terms must be included at the order where the reduced obstruction appears.
For \(u=O(h)\), an \(u^5\) coefficient lives at order \(h^5\); residuals
controlled merely by \(O(h^2)\) cannot test that coefficient.

## 7. The unconditional quadratic response-defect description

Retain the primary memo's actual scope:

* \(Q_h(x)=g(hx)\), one fixed smooth nondegenerate Lorentz Gram field;
* \(A_h=\log K_h\), \(\|A_h\|_\infty+\|A_h^{sm}\|_\infty\le Ch\);
* exact connection equations and \(E_Q(Q_h,K_h)=h^2\tau_h\), with the
  prescribed \(\tau_h\) converging uniformly to a fixed smooth \(\tau\);
* the designated #216 smooth comparator, its small connection residual, and
  its response limit \(\rho[g]\) under the actual reconstruction assumptions.

Set \(b_h=(A_h-A_h^{sm})/h\). The expansions and summation by parts in the
primary memo give \(H_g(T)b_h=O(h)\), \(C_g(T)b_h=O(h)\), and
\(b_h\rightharpoonup0\). Here \(C_g\) is the **connection-to-metric** block,
the adjoint of the \(B_g\) used above; this distinction is essential.

For every subsequence one may extract the correlations of all finite shifts.
Positivity of \(\|\sum_\ell a_\ell T_\ell b_h\|^2\) yields a positive
matrix-valued frequency measure \(\mu_x(dz)\). Its spatial marginal obeys
\(\operatorname{tr}\mu_x(\mathbb T^4)\le C'\) almost everywhere, because
\(b_h\) is uniformly bounded. Finite-shift commutators with smooth tests are
\(O(h)\). The leading equations imply

\[
 \operatorname{Ran}\mu_x(z)\subset
 \ker H_{g(x)}(z)\cap\ker C_{g(x)}(z)
 \quad\text{for }dx\,d\mu_x\text{-almost every }(x,z). \tag{S}
\]

The linear curl term and smooth-cross term have zero weak limit. The remaining
response is exactly

\[
 \boxed{
 \mathcal T_\mu(x)[q]
 =\frac12\int_{\mathbb T^4}
 \operatorname{tr}\!\left(D_QH_{g(x)}(z)[q]\,d\mu_x(z)\right).} \tag{R}
\]

The measure uses the whole frequency torus with the physical Parseval
normalization and conjugate symmetry inherited from the real link field;
there is no additional conjugate-pair multiplicity factor in (R).

Thus the source/comparator limit must satisfy, distributionally,

\[
 \tau-\rho[g]=\mathcal T_\mu. \tag{M}
\]

This is the useful homogenized statement even after (NF) fails. It is a
constraint on an effective response, not an extra term added to the action.
The admissible \(\mu\)'s are those generated by the **full nonlinear**
equations. A rank-one vector in (S) is not automatically realizable.
Nonlinear constraints may couple carriers and require higher correlations or
correctors; they cannot in general be imposed separately on each Fourier atom.

The exact closure question is whether (R) vanishes on all such realizable
correlation measures. A source chosen after measuring a candidate response
does not satisfy the stated source contract.

### Two useful consequences

**Diagonal-support corollary.** If the actual defect measure is supported on
the two diagonal quarter-wave characters, the all-solder theorem in the
primary memo annihilates (R). Hence the tested response decouples; uniform
source/comparator convergence upgrades this to the uniform response limit.
This is a proved conditional subclass, not the global requested terminal.

**Almost-everywhere-background corollary.** It is enough that (NF) hold at
\(Q=g(x)\) for almost every physical \(x\), for every phase and polarization.
One need not impose it in a whole neighborhood of the metric image. More
generally, if the bad-background set has preimage of spatial measure zero,
the bounded spatial marginal of \(\mu\) rules out a response supported there.
No genericity or codimension classification of that bad set is asserted here.

The contrast is important: a measure-zero set of **frequencies** can carry
all of \(\mu_x\), including an isolated character. Isolating the shear
frequency does not make its stress small. The pointwise constraint estimate
away from that character has no uniform constant as the character is
approached. Accordingly the frequency-isolation result in the primary memo
does not restore its uniform epsilon inequality across the puncture.

## 8. What v7 resolves, and what it does not

| Statement | Verdict after this synthesis |
|---|---|
| The metric-only germ can be continued in frequency | **Exact**, by (G0)-(G1), throughout the constant-solder symbol domain |
| The needed correction lies in the old \(\ker C\) | False in general; the correction is the derivative of the moving germ |
| Orbit 5 has zero physical connection-row cokernel | False for the owned physical pairing; its dimension is 1 |
| The specific germ forcing has zero cokernel class | **Exact**, including orbit 5; zero class does not mean zero cokernel |
| Frozen-germ ranks establish a new metric stress | They do not; the stress is the separate quadratic response entry (R) |
| All nonlinear smooth-background response is absorbed | Still open |
| A radial symbol test proves nonlinear protection on a varying background | It does not test the variable-coefficient Euler equations or their commutators |
| A floating residual below \(10^{-12}\) proves an exact rational singular value | Numerical evidence only unless an exact algebraic identity is supplied |

For a Laurent symbol, the paths \(z_j(1+t)\) and \(z_je^{it}\) have derivatives
\(z_j\partial_{z_j}\) and \(iz_j\partial_{z_j}\). The two derivative matrices
differ by multiplication by \(i\), so their complex ranks, and with the same
norm their singular values, must coincide. This is not an independent
stability experiment. Off-unit-circle symbols are legitimate analytic
continuations but are not real Bloch waves on a periodic lattice.

The supplied v7 \(\varepsilon\)-scans do not include the full varying-solder
Euler calculation. Their nonlinear and gradient conclusions therefore remain
unproved. The explicit formula (G0) explains constant-symbol persistence
without assigning a physical time direction or a new physical modulus.

## 9. Narrow follow-up packets for CONTROL

These are research specifications, **not newly registered executable tasks**.
They stay within the existing response task until CONTROL dispatches them.

1. **Complete modulated reduced action at a known NF defect.** Use the exact
   shear witness, the same genuine Gram lift, real conjugate pairing, and
   fixed prescribed-source convention. Include the entire range correction,
   free kernel variables, sidebands, and slow-background terms through the
   first nonzero reduced connection order. Derive both Euler slots from one
   \(\Phi\), with remainder estimates at that order. Deliver a uniform
   obstruction or an explicit surviving stress branch. A bare single-mode
   jet or another phase census is not the deliverable.
2. **Prove a response estimate on the realizable branches.** Use either the
   approximate horizontal-lift criterion (HL), or a uniformly controlled
   real-radical/constraint identity for the reduced stress. State all powers
   of \(h\), treatment of resonant mixtures, and localization errors. A
   fixed-cell identity whose multipliers diverge with \(h\) is insufficient.
3. **Exactify only a branch that survives the first two tests.** Fix a smooth
   background and source before constructing the sequence; solve both finite
   Euler equations and compute the gap to the designated #216 comparator.
   This is the route to NOGO. If all realizable branches have zero (R) with a
   uniform passage to the limit, this is the route to CLOSED.

The first missing global statement remains the annihilation of (R) on
nonlinearly realizable correlations. The proposed first calculation now
targets the mechanism deciding that statement, not more connection ranks.

The quadratic piece of that calculation is now exact at the shear witness.
`a4d_joint_response_shear_reduced_quadratic_check.py` takes
\(\Phi=\tfrac12 u^2 v^*H(Q)v\) on \(z=(-1,1,-1,1)\). Then \(\partial_u\Phi=0\)
for every amplitude, and \(\partial_{q_{11}}\Phi=-u^2\). At this character
\(d=(-2,0,-2,0)\) and \(q_0=dd^T\) is supported on slots \((00,02,22)\) only,
so its witness stress is 0. Frequency absorption and the \(q_{11}\) stress
are different slots of one quadratic action. A slowly modulated packet and
the order-\(u^5\) reduced connection jet are not decided by \(\Phi\) at this order.

## 10. Evidence and boundaries

The accompanying certificate
`certificates/a4d_joint_response_moving_germ_check.py` checks the Laurent
identity (G0), all four differentiated identities (G1), three nonstandard
solders at symbolic phases, the full physical joint metric germ, all nine
physical/unpaired rank comparisons, and the kernel identity (F) on those
orbits. It reuses the existing #216 owners through the #240 symbol module.

The all-solder exterior-algebra proof, (O), (E), (H), and the corollaries of
(R) are research proofs in this note, not Lean formalizations. The old
large finite censuses and order-five calculations were not rerun for this
synthesis. In particular, sampled solder values do not prove an entire
parameter-line classification, and the recent quadratic terminal is not
accepted as an order-five computation.

The correlation framework is consistent with the position/frequency defect
measure method of Gérard and Tartar; the D0 symbol and response calculations
above are specific to this task and are not supplied by those general papers:

* Patrick Gérard, *Microlocal defect measures*, CPDE 16 (1991), 1761-1794,
  https://doi.org/10.1080/03605309108820822.
* Luc Tartar, *H-measures, a new approach for studying homogenisation,
  oscillations and concentration effects in partial differential equations*,
  Proc. R. Soc. Edinburgh A 115 (1990), 193-230,
  https://doi.org/10.1017/S0308210500020606.

The quadratic reduction assumes \(A_h=O(h)\). At larger amplitudes the
normalized cubic and higher terms may survive. The exact flat #232 identity
remains an exact control there, but the general reduction above makes no
claim at those larger scales.
