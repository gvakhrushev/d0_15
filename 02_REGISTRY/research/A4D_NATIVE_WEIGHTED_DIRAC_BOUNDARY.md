# Actual weighted Hodge–Dirac: mixed spectral contrast and Lorentz boundary

Research continuation of #310. Input head:
`139ba614c85381a0b2c2cdf432d2912e852a92c3`.

**Result.** The documented weighted adjoint can be constructed on the actual
frozen D0 cochain differential, with genuine nilpotency, weighted symmetry
and a square identity. Every fixed finite polynomial in its spectral moments,
with a separately arbitrary volume profile and the stated exact metric/probe
domain, fails the common Einstein contrast by a quantitative finite
annihilator. The direct flat Lorentz Hodge binding has nonconstant
null modes and negative spatial modes. It cannot inherit the positive
Hilbert representation or the constant-only kernel theorem of the counting
Hodge operator. Its ordinary fixed-positive-time heat trace diverges under
refinement, even after the site-volume normalization. These are complete
operator statements for the specified binding, not a no-go for every native
action or a choice of a physical matter law.

No supported Lean owner, native action, selector, source, causal prescription,
claim/release status, or original #310/#202/#317 terminal is changed.
Positive GR and global closure remain **OPEN**.

## 1. What the existing declarations actually supply

`ArchiveWeightedHodgeDirac` documents the formula

\[
\delta_W=W^{-1}d^TW,\qquad D_W=d+\delta_W.
\]

Its actual capstone proves five form degrees, sixteen carrier components,
four Roles, and the Boolean equation `DegreePreservingLaplacian true`.
It does not define these operators or prove their equations. The new
research capsule prints that proposition and constructs the formula on
`ArchiveCochain N`, using the actual `dForward` and counting
`hodgeCodifferential`. Here \(L=N+2\), with periodic four-Role sites.

The counting operator in `ArchiveHodgeCARDirac` is genuine:

\[
d=\sum_r c_r^\dagger\nabla_r^+,
\quad \delta_0=-\sum_r c_r\nabla_r^-,
\quad \nabla_r^+u(x)=L[u(x+e_r)-u(x)],
\quad \nabla_r^-u(x)=L[u(x)-u(x-e_r)].
\]

Its counting adjoint, square and constant-only kernel have existing owners.
They concern the counting pairing. They do not select a curved physical
pairing. `ArchiveNaturalTwistedDirac`'s numeric cycle Laplacian is also
distinct: at \(L=2\) its diagonal-one scaffold differs from the actual
normalized difference square with diagonal two and off-diagonal minus two.
The coincident forward/backward neighbours are retained in this package.

## 2. Constructive weighted operator, with explicit hypotheses

Let \(W\) be a **supplied invertible real linear map** on the full finite
cochains. Set

\[
\delta_W=W^{-1}\delta_0W,\qquad
\langle u,v\rangle_W=\langle u,Wv\rangle_0.
\]

Conjugation and the actual nilpotencies give

\[
\delta_W^2=0,\qquad
D_W^2=d\delta_W+\delta_Wd.
\tag{1}
\]

The actual counting adjoint gives
\(\langle du,v\rangle_W=\langle u,\delta_Wv\rangle_W\).
If \(W\) is symmetric for the counting pairing, that pairing is symmetric
and \(D_W\) is symmetric for it. **Positivity is an additional hypothesis.**
Only when \(W>0\) does this become a positive inner product, with the usual
self-adjoint representative \(W^{1/2}D_WW^{-1/2}\).
Invertibility or indefinite symmetry does not imply that conclusion.

For a graded \(W\), its inverse preserves each degree. The literal creation
and annihilation supports show that \(d\) raises degree and \(\delta_0\)
lowers degree. Thus the two summands of (1) preserve degree. This full
grading argument is analytic; the capsule compiles (1) on the actual
cochains. Exact controls check every degree block of explicit bindings.
The old Boolean statement is not used as an operator proof.

The upstream finite CAR leaves used `native_decide`. This package proves
the two needed integral identities again by kernel `decide` on the literal
Role/Fock carrier. The real identities, directional anticommutation and
both actual nilpotencies are then rebuilt. All thirty-four printed
research propositions have only `propext`, `Classical.choice` and
`Quot.sound` as transitive axioms. No upstream computation axiom, `sorry`,
or physical premise enters their proof closure. The original owners remain
untouched.

## 3. Genuine mixed metric dependence is preserved

For an independently supplied nondegenerate metric \(Q\), write
\(M=Q^{-1}\), \(\mu=\sqrt{|\det Q|}\). The tested full compound binding is

\[
(W_Q)_{S,T}=\begin{cases}
\mu\det M[S,T],&|S|=|T|,\\
0,&|S|\ne|T|.
\end{cases}
\tag{2}
\]

The empty minor is one. On diagonal metrics this agrees with the actual
`hodgeMetricMeasureWeight` formula after setting
\(c_r=\mu M^{rr}\):
\(\mu^{1-|S|}\prod_{r\in S}c_r=\mu\prod_{r\in S}M^{rr}\).
The full off-diagonal compound is a tested supplied geometric binding;
the existing scalar owner does not prove its constitutive uniqueness.

For a symmetric probe \(V\),

\[
\dot M=-MVM,\qquad \dot\mu=\tfrac12\mu\operatorname{tr}(MV),
\quad
\dot\delta_W=-W^{-1}\dot W\delta_W+W^{-1}\delta_0\dot W,
\quad
\dot\Delta_W=d\dot\delta_W+\dot\delta_Wd.
\tag{3}
\]

The inverse derivative follows from differentiating \(W^{-1}W=1\), not
from fixing the codifferential during a metric variation. All ten
symmetric probes are checked at a non-diagonal Lorentz metric. The
off-diagonal packed dual weight is two. Omitting that factor or the
inverse derivative changes the result. Thus a geometry-dependent
operator remains a real mixed scale/shape mechanism outside the previous
separate-volume obstruction.

Under a uniform metric scaling \(Q\mapsto sQ\), \(s>0\),
\(W_Q|_{C^k}\mapsto s^{2-k}W_Q|_{C^k}\). Hence
\(\delta_W\mapsto s^{-1}\delta_W\) and
\(\Delta_W\mapsto s^{-1}\Delta_W\). With
\(J_s|_{C^k}=s^{k/2}\),
\(D_{sQ}=s^{-1/2}J_sD_QJ_s^{-1}\).
This is operator homogeneity. It supplies no Einstein action, source or stationarity theorem. The following stated spectral family
is tested separately for contrast transfer.

### Finite mixed spectral moments: a quantitative contrast obstruction

The actual `SpectralActionLadder.spectralTracePower` binds literally to
\(\operatorname{Tr}(\Delta_Q^j)\) when its supplied \(\rho\) is one.
The binding and scalar matrix-power/trace homogeneity compile. The
geometry-dependent \(\Delta_Q\) is now constructed; it is not silently
replaced by a fixed operator depending only on volume.

Consider the complete **stated family**

\[
I_h^N(Q,R,z)=A_{0,h}(Q,R,z)+
\sum_{j=1}^{p}a_{j,h}(Q,R,z)\operatorname{Tr}(\Delta_Q^j)
+B_h(\mu_Q,z),
\tag{3a}
\]

where \(p\) is any one fixed finite degree. The \(A_0\) and \(a_j\)
are invariant under uniform metric/raw scale along the admitted probes.
They may depend on shape, links and matter held fixed during each probe,
may differ between experiments, and may diverge with the mesh.
\(B_h\) is an arbitrary common functional of the full volume vector and
common \(z\); it does not acquire experiment-specific link/shape inputs.
No positivity, locality, bounded sensitivity or bounded coefficients is
assumed. The class must admit the two exact curved native fibers and their
finitely many homothetic probes from
[A4D_NATIVE_COUPLED_HODGE_SCALE_BOUNDARY.md](A4D_NATIVE_COUPLED_HODGE_SCALE_BOUNDARY.md).
It is a test of existing supplied spectral scalars, not a new action choice.

Write those metrics as
\(g_c=f^2\operatorname{diag}(c^2,-c^{-2},-1,-1)\),
\(c=1,2\), \(f=1+\cos(2\pi y^0)/10\).
At every \(L\in4\mathbb N\), their constructed raw/link fields have
exact transported readouts and the same pointwise volume \(f^4\).
For each fixed \(s>0\), raw scaling by \(\sqrt{s}\) gives exactly
\(sg_c\), with common volume \(s^2f^4\) and unchanged links.
The same-carrier \(\Delta_{sg_c}=s^{-1}\Delta_{g_c}\) follows from (1)–(3).
All preparation/inverse bounds remain uniform over the finite list of
scales below. These are kinematic off-shell test fibers, not claimed
native joint solutions.

At amplitude \(\epsilon\), the polynomial half-contrast at scale \(s\)
is a linear combination of \(s^{-j}\), with factors
\(q_j(\epsilon)=[(1+\epsilon)^{-j}-(1-\epsilon)^{-j}]/2\).
The \(A_0\) contrast is zero and the common \(B_h\) contrast cancels
between the two experiments **exactly**, before any sensitivity estimate.
Set

\[
s_r=\frac1{r+1},\quad
w_r=(-1)^r\binom{p+1}{r},\quad 0\le r\le p+1.
\]

For every \(0\le j\le p\),

\[
\sum_r w_rs_r^{-j}=0,\qquad
\sum_r w_rs_r=\frac1{p+2},\qquad
\sum_r|w_r|=2^{p+1}.
\tag{3b}
\]

The first identity is the \((p+1)\)-st finite difference of a degree-\(j\)
polynomial. The second follows by integrating the binomial identity
\(\sum_r w_rx^r=(1-x)^{p+1}\) from zero to one. The third is the
ordinary binomial sum. Thus (3b) holds for **every fixed finite \(p\)**;
finite controls at \(p=0,\ldots,8\) are not the general proof.
The generic annihilation of arbitrary coefficient sums and its error
inequality compile independently of those finite controls.

The finite physical Palatini half-action is exactly linear in this
uniform metric scale with the fixed prepared links. Its unscaled paired
base-action difference is
\(d_h=-9\pi^2/200+O(h)\). The weighted sum of paired physical
half-contrasts is therefore \(\epsilon d_h/(p+2)\), while the
corresponding native sum is zero. For any one nonzero fixed calibration,
let \(E_{c,r,h}\) denote each total transfer error. Then, allowing the
stated \(O(h)\) recording/refinement errors,

\[
\max_{c,r}|E_{c,r,h}|\ \ge\
\frac{9\pi^2}{400(p+2)2^{p+2}}\,h^{1/3}
\quad\text{for all sufficiently small }h,
\qquad \epsilon=h^{1/3}.
\tag{3c}
\]

Indeed the weighted paired error has magnitude
\(|\epsilon d_h/(p+2)+O(h)|\), while its magnitude is at most
\(2\max|E|\sum_r|w_r|\). Since \(h/\epsilon\to0\), half the
nonzero limiting coefficient remains. Constants depend on this fixed
finite probe list, as permitted in the transfer criterion. Arbitrary
mesh coefficients never enter the estimate because their terms are
annihilated exactly. A total \(O_V(h)\) contrast transfer is impossible
in class (3a); after division by \(\epsilon\), the response error does
not tend to zero at the required \(O_V(h^{2/3})\) rate.

This does **not** exclude a degree growing with refinement, nonpolynomial
spectral laws, coefficient dependence on metric scale, a volume insertion
inside an operator trace, or an independently owned domain excluding the
stated fibers/probes. In particular a density-weighted moment such as
\(\operatorname{Tr}(\mu_Q\Delta_Q)\) has homogeneity \(+1\), not
\(-1\), and is outside (3a). No Einstein law is claimed for that surviving
mechanism. Its native owner, full metric/source/connection variation and
refinement would require their own proof.

## 4. Direct flat Lorentz binding on the owned carrier

Use the explicitly tested flat metric
\(\eta=\operatorname{diag}(1,-1,-1,-1)\), \(\mu=1\).
Let \(\epsilon=(1,-1,-1,-1)\) in the actual A,B,C,D role order.
Then (2) is diagonal on Fock states, with
\(w_S=\prod_{r\in S}\epsilon_r\).
The inertia by degree is

| Degree | Positive | Negative |
|---|---:|---:|
| 0 | 1 | 0 |
| 1 | 1 | 3 |
| 2 | 3 | 3 |
| 3 | 3 | 1 |
| 4 | 0 | 1 |

There are eight weights of each sign and no zero weights.
The exact Jordan–Wigner support gives
\(W_\eta c_rW_\eta=\epsilon_rc_r\), so

\[
\delta_\eta=-\sum_r\epsilon_rc_r\nabla_r^-,\qquad
D_\eta^2=-\sum_r\epsilon_r\nabla_r^-\nabla_r^+\otimes I_{16}.
\tag{4}
\]

Creation-creation and annihilation-annihilation terms cancel by CAR.
Mixed terms with different roles cancel because translations commute;
the same-role CAR gives (4). This works at every \(L\ge2\).
The controls construct the **full site/Fock matrices**, not only a
Fourier ansatz, at \(L=2,4,8\), and check the square, signed adjoint and
real witness cochains exactly with integer arithmetic. All twenty-four
Role orders are checked by their explicit Fock sign intertwiners.
This role labeling is a binding; it is not a derivation of physical time.

On the Fourier character indexed by \(k\in(\mathbb Z/L)^4\), set
\(z_r=e^{2\pi ik_r/L}\). The forward and backward symbols are
\(a_r=L(z_r-1)\) and \(b_r=L(1-z_r^{-1})\). Thus

\[
D_\eta(k)=\sum_r[a_rc_r^\dagger-\epsilon_rb_rc_r],
\quad
\lambda_\eta(k)=4L^2\left[
\sin^2(\pi k_0/L)-\sum_{i=1}^3\sin^2(\pi k_i/L)\right].
\tag{5}
\]

Each eigenvalue of \(\Delta_\eta\) has Fock multiplicity sixteen.
In particular the spatial Nyquist mode \(k=(0,L/2,0,0)\) exists on
every even \(L\), including every \(L\in4\mathbb N\). On the empty and
B-singleton subspace, the actual Dirac matrix is

\[
\begin{pmatrix}0&2L\\-2L&0\end{pmatrix},\qquad D^2=-4L^2I_2.
\tag{6}
\]

If a positive real inner product made this block self-adjoint, its matrix
\(G\) would satisfy \(D^TG=GD\). The 01 entry forces
\(G_{00}+G_{11}=0\), contradicting positivity. The capsule proves this
without assuming a diagonal \(G\). The subspace is invariant, so the
restriction of any positive self-adjoint pairing on the full cochains
would contradict (6). The obstruction is not merely failure of the
particular counting pairing.

## 5. Complete constant-metric null-mode classification

At \(k=0\), \(D_\eta(k)=0\), giving sixteen kernel components.
If \(\lambda_\eta(k)\ne0\), (5) makes the block invertible.
At a **nonzero null** momentum, \(D^2=0\) but \(D\ne0\).
Choose a role with \(a_r\ne0\) and set \(K=c_r/a_r\).
The mixed CAR gives \(DK+KD=I\). Consequently

\[
\ker D=\operatorname{range}D,\qquad
\dim\ker D=\operatorname{rank}D=8,
\quad\dim\ker\Delta=16.
\tag{7}
\]

The kernel/range and half-dimension implications compile as generic
linear-map theorems; the explicit Fourier contraction is checked exactly.
Fourier decomposition proves the all-size classification. Real dimensions
agree with the complexified dimensions of these real finite operators.
On \(L=4\), there are 28 null momenta, so

\[
\dim\ker D_\eta=232,\qquad \dim\ker\Delta_\eta=448.
\]

These are not the counting operator's kernel dimension sixteen, and
\(\ker D_\eta=\ker\Delta_\eta\) is false. Exact counts also cover
\(L=2,8\); their values are in the pinned ledger.

Nonconstant null roots persist along refinement: \(k=(m,m,0,0)\)
is null for every \(m\), at every \(L\). The real double-Nyquist
character gives a directly checked nonzero cochain \(u=Dv\) with
\(Du=0\) on every tested even grid. Thus the operator is not injective
after removing only constant cochains. No physical gauge quotient has
been constructed here; these modes cannot be discarded by labeling
them gauge. This is a statement about the tested operator equation,
not a native metric–connection–matter Euler equation or an Einstein
solution.

## 6. Fixed-positive-time heat trace cannot supply the claimed refinement

For each finite \(L\), \(\Delta_\eta\) is a real symmetric matrix and
its ordinary heat trace is well-defined:

\[
H_L(t)=16\sum_k e^{-t\lambda_\eta(k)}.
\]

When \(L\) is even its minimum eigenvalue is \(-12L^2\), at
\(k=(0,L/2,L/2,L/2)\). All heat eigenvalues are positive. Hence for
any one fixed \(t>0\),

\[
H_L(t)\ge16e^{12tL^2},\qquad
L^{-4}H_L(t)\ge4608t^3L^2\longrightarrow\infty.
\tag{8}
\]

The polynomial lower bound uses \(e^x\ge x^3/6\) for \(x\ge0\).
That inequality and the conditional numerical implication in (8) compile.
The spectral premise of (8) is independently proved by (5), not inserted
into the definition of \(H_L\). This excludes ordinary fixed-positive-
time heat-trace refinement for this direct Lorentz binding.

It does not exclude \(t=t_L\to0\), a separately specified renormalized
or oscillatory law, positive Euclidean weights, or an independently
owned positive observer pairing. For example the lower bound in (8)
at \(t_L=L^{-2}\) is \(4608L^{-4}\), not a divergence proof.
No such prescription is selected or supplied as a new physical postulate.

## 7. Validation and remaining physical transition

The companion capsule compiles thirty-four propositions, including
kernel-only CAR leaf checks, actual-cochain nilpotencies, weighted adjoint
and square, generic null contraction, inverse variation, the spatial
block obstruction, the heat inequality and the finite spectral annihilator.
Its receipt pins the complete
D0 import closure and toolchain. All-size symbol, grading, spectral
classification and refinement and all-degree finite-polynomial contrast arguments above are analytic; finite
controls are not promoted to compiled continuum statements.

The exact checker retains all sixteen sectors, all twenty-four role
orders, all ten metric variations, packed weights, three full periodic
matrix sizes, nonconstant roots and the exact null spectrum. Negative
controls distinguish indefinite symmetry from positive symmetry,
\(\ker D\) from \(\ker D^2\), the actual \(L=2\) collision, omitted
inverse variation, and fixed heat time from mesh-dependent time. False
scope ledgers are separately rejected.

The next physical arrow still requires an independently owned native
matter/action sector and its coupled equations and source on the same
carrier. This package supplies an actual weighted operator construction
and classifies the direct Lorentz continuation of its positive/counting
claims. It neither chooses that operator as physical matter nor proves
the action contrast, Ward hypotheses, native refinement admission,
curved joint solutions, soundness or recovery. Other mixed scale/shape
mechanisms remain open under their own stated owners and hypotheses.

Reproduce the exact ledger with
`python3 02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary_check.py`.
The capsule, compiler output, receipt and immutable ledger share that
filename stem in `certificates/`.
