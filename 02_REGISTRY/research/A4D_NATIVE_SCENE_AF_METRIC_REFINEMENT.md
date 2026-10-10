# Scene joint registers: genuine AF metric refinement

Task: existing #310. Input SOURCE:
`812abc87da9c494d14d4b8549b2b219b88c60f86`.

**Result.** The declared scene-register AF construction does give a metric
for the weak-star topology for every fixed b>1. The old certificate's
constant-two tail bound is false on this very construction. A complete
operator proof replaces it by

\[
 \|a-E_n a\|\le {33b^{1-n}\over(b-1)^2}\|[D_b,L_a]\|.       \tag{1}
\]

The register dimension, trace, full noncommutative algebra and all archive
sectors are retained. This supplies the missing quantitative estimate for
this existing observable/refinement rule. It does not construct a physical
four-dimensional readout or the common full-action preparation of T0.

## 1. The actual declared composition rule

BOOK_02 §02.34c and `vp_compositional_closure_spectral_limit.py` use

\[
 H=\mathbb C^{33},\quad G=S_9\times S_{11}\times S_{13},\quad
 A_n=\operatorname{End}(H^{\otimes n})^G,\quad A_0=\mathbb C1,
 \qquad a\longmapsto a\otimes I_{33}.                       \tag{2}
\]

The G action is diagonal on the n registers. Use the actual normalized
matrix trace \(\tau_n=33^{-n}\operatorname{Tr}\); it is faithful and
compatible with these inclusions. Uniqueness among all AF traces is not
needed below. The normalized partial trace of the last register is
G-equivariant, hence maps A_n to A_(n-1). Its iterates give the tracial
conditional expectations E_n onto A_n. They preserve positivity and trace,
are contractive in operator norm, and satisfy the A_n bimodule identity.
These assertions follow directly from partial trace on the full tensor
matrices, then restrict to the fixed-point algebra.

Let A be the norm closure of the union. In its faithful tracial GNS space
write P_n for the orthogonal projection onto A_n, Q_n=P_n-P_(n-1), and

\[
 D_b=\sum_{n\ge1}b^n Q_n,\qquad D_b1=0.                    \tag{3}
\]

This is the filtration operator underlying the certificate's increment
multiplicities and zeta sum. The scalar base is retained as a zero mode.
Every finite-level a commutes with P_k for k at least its level, by the
bimodule identity. Thus [D_b,L_a] is a bounded finite-rank operator. The
finite-dimensional eigenspaces and b^n tending to infinity give compact
resolvent. No scale b, temperature, new algebra or physical state is selected.

## 2. Exact counterexample to the old tail constant

The first algebra is \(A_1=M_3(\mathbb C)\oplus\mathbb C^3\). Its GNS
dimension is 12, while its trace is inherited from the **33-dimensional**
scene. Indeed, a commuting matrix has constant diagonal and off-diagonal
entries within each zone and constant cross-zone blocks; the nine maps
between zonal constant vectors and the three archive identities span it.
In matrix-unit coordinates for M_3 followed by the three archive
identities, the pairing is

\[
 W=\operatorname{diag}(\underbrace{1/33,\ldots,1/33}_{9},
                         8/33,10/33,12/33).
\]

Let e be the rank-one projection onto the normalized constant vector of
the nine-vertex zone. It is fixed by G and belongs to A_1. Put t=τ(e)=1/33.
On GNS(A_1), P_0 is the projection onto the unit vector 1 and

\[
 \|[D_b,L_e]\|^2=b^2t(1-t),\qquad
 \|e-E_0e\|=1-t.                                         \tag{4}
\]

For b=2, the square of the left side of the previously claimed bound
\(\|a-E_na\|\le2\|[D_b,L_a]\|/(b^{n+1}-b^n)\)
is 1024/1089, whereas its right side squared is 512/1089.
The failure is exact, by a factor two after squaring.
It also fails at b=phi: the squared ratio is 8/phi^4>1, since
phi^4=(7+3 sqrt(5))/2<8. This is a scale test, not a scale-selection law.

This is not an artefact of truncating the Hilbert space: L_e commutes with
all P_k for k>=1, so the infinite commutator is this first block. If the
bound is read only for n>=1, take \(a=1^{\otimes n}\otimes e\).
Then E_n a=t1. With B=Q_(n+1)L_aP_n one has
\(B^*B=t(1-t)P_n\) and
\(Q_{n+1}[D_b,L_a]P_n=B(b^{n+1}-D_b|_{P_n})\).
The lower block of L_a is tI and the higher block has scalar D_b, so
the full commutator norm is \(b^{n+1}\sqrt{t(1-t)}\).
The same factor-two violation therefore occurs at every n when b=2.

The old executable checked only positivity of b-1 and a geometric series;
it never checked this operator inequality. The registered certificate is
repaired to test the actual weighted first-level commutator and to reject
the false estimate. No weak-star failure is inferred from this wrong constant.

## 3. The register estimate, including its necessary dimension factor

For x in \(B(K\otimes\mathbb C^d)\), put
\(E(x)=(\mathrm{id}\otimes\operatorname{tr}_d)(x)\), with normalized trace.
Writing x in d-by-d operator blocks, Cauchy--Schwarz gives for ξ=(ξ_j)

\[
 \|x\xi\|^2
 \le d\sum_{i,j}\|x_{ij}\xi_j\|^2
 \le d\Big\|\sum_{i,j}x_{ij}^*x_{ij}\Big\|\|\xi\|^2.
\]

Consequently

\[
                    \|x\|\le d\|E(x^*x)\|^{1/2}.          \tag{5}
\]

Restriction to the G-fixed algebra preserves (5), with d=33 at every
register step. The factor cannot be replaced by a dimension-independent
one in this estimate: already at A_2 the projection onto
\(33^{-1/2}\sum_{i=1}^{33}e_i\otimes e_i\) belongs to A_2, since it is
fixed by every diagonal real permutation. Its norm is one and its
normalized partial trace is I/33^2. Hence equality holds in (5).
This uses an element of the full actual algebra, with every scene sector.

## 4. Operator tail estimate on the complete tower

For a finite-level a put a_m=E_m a-E_(m-1)a and
B_m=Q_m L_a P_(m-1). For x in A_(m-1), the bimodule identity gives
B_m x=a_m x. Faithfulness of the finite left regular representation gives

\[
 \|B_m\|^2=\|E_{m-1}(a_m^*a_m)\|.                        \tag{6}
\]

On P_(m-1) the spectrum of D_b lies in [0,b^(m-1)] (for m=1 it is {0}).
The full commutator, rather than just its value on the vacuum, therefore gives

\[
 Q_m[D_b,L_a]P_{m-1}=B_m(b^m-D_b|_{P_{m-1}}),\qquad
 \|B_m\|\le {\|[D_b,L_a]\|\over b^m-b^{m-1}}.             \tag{7}
\]

Indeed the right factor is invertible, with inverse norm at most the
reciprocal displayed gap. Combining (5)--(7), telescoping a-E_n a, and
summing the exact geometric series proves (1), since

\[
 \sum_{m=n+1}^{\infty}{1\over b^m-b^{m-1}}
                  ={b^{1-n}\over(b-1)^2}.                 \tag{8}
\]

At b=phi, (1) specializes to the coefficient 33 phi^(3-n). This
arithmetic specialization does not establish its physical scale admission.

The same proof applies to bounded-commutator elements of A, using the
finite compressions and E_N a tending to a in norm. It makes no
finite-sample extrapolation and assumes no uniform eigenvalue-gap theorem
for unrelated AF towers. The fixed register dimension is essential to
the uniform constant used here.

## 5. State-space metric and physical boundary

Let L(a)=\|[D_b,L_a]\| on self-adjoint elements. Formula (1) with n=0
bounds every a with τ(a)=0 and L(a)<=1 by C_b=33b/(b-1)^2. At level n
their E_n images lie in a bounded finite-dimensional set, with uniform
tail at most C_b b^(-n). The centered Lipschitz ball is therefore totally
bounded. Also L(a)=0 forces a=τ(a)1; finite-level elements have bounded
commutator and are norm dense. Thus the associated distance on all states
is finite and separates them.

For completeness, weak-star convergence implies convergence in this
distance: choose n with 2C_b b^(-n) small, then use uniform convergence
of the state evaluations on the finite-dimensional bounded set of E_n
images. Conversely distance convergence controls every finite-level
evaluation after scaling by its finite L, and norm density controls all
evaluations. This proves equality of the topologies for every fixed b>1.

The general AF spectral-triple context is the primary paper of
[Christensen and Ivan, J. Operator Theory 56 (2006)](https://jot.theta.ro/jot/archive/2006-056-001/2006-056-001-002.pdf).
Its existence results do not, by themselves, prove the claimed constant
or every chosen eigenvalue sequence. Here (1) is proved directly from
the particular native tensor-register inclusions and their partial trace.

This noncommutative refinement is distinct from literal strict scalar
pullback families on the archive diagram. It retains increasingly many
observables with a genuine norm estimate. It does not identify these
register inclusions with archiveProjection, select b=phi, turn b^(-n)
into the physical mesh h, or construct the four-dimensional field readout.
In particular neither weak-star metric closure nor (1) gives a varying
full heat/feedback preparation, its source, Ward identity or stationarity.
The normalized algebra trace used for GNS and E_n does not replace the
operator trace in the full bootstrap heat price or supply its normalization.
T0--T3 and all original #310/#202/#317 terminals remain open.

The all-level operator and topology arguments above are analytic, not
claimed Lean-formalized. The [repaired registered certificate](../../04_CERTIFICATES/vp_verifiable_registration_metric_closure.py),
[research replay](certificates/a4d_native_scene_af_metric_refinement_check.py)
and [pinned ledger](certificates/a4d_native_scene_af_metric_refinement_certificate.json)
provide exact finite controls and
hostile mutations; they do not replace these proofs.
