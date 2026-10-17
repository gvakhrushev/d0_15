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

**Heat continuation.** Section 6 proves that the full heat trace of this
same D_b squared has no positive finite four-dimensional leading
coefficient for any fixed b>1. It retains the valid fixed-phase geometric
subsequence limits and does not identify this heat with the bootstrap price.
Section 7 computes the full retained-stratum expansion and shows that even
on every fixed phase the ordinary next curvature coefficient fails: a
positive archive contribution lies strictly between the t^-2 and t^-1 orders.

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

## 6. The full native spectrum cannot supply a usual four-dimensional heat coefficient

Continuation input: `43fc7657d88d50f390b72b52e86317e98e1f5974`.
This tests the next specific use of the same declared operator: taking
the **full operator heat trace of D_b squared** as the four-dimensional
heat carrier. No new heat spectrum, action or field preparation is defined.
The conclusion is about this complete family, for every fixed b>1; it is
not a no-go for other physical readouts or for all D0 preparations.

Write g=|S_9 x S_11 x S_13| and c_f for the number of its permutations
having f fixed scene vertices. Burnside gives the actual register dimensions

\[
 d_n=\dim A_n={1\over g}\sum_f c_f f^{2n},\qquad
 d_0=1,\quad m_n=d_n-d_{n-1}.                              \tag{9}
\]

The exponent is 2n because matrix entries have two n-register indices.
At n=0 use 0^0=1. The registered composition certificate supplies these
counts; independently c_33=1, c_32=0 and
c_31=binom(9,2)+binom(11,2)+binom(13,2)=169. A nonidentity permutation
cannot move only one vertex. Thus no other group element has more than
31 fixed vertices. In particular d_1=12, d_2=309 and m_1=11. All sectors,
including the scalar zero mode and the nonidentity contributions, remain.

Put R=33^2=1089, S=31^2=961, B=b^2 and

\[
 \alpha={\log R\over\log B}={\log33\over\log b},\quad
 \sigma={\log S\over\log B}<\alpha,\quad
 c={1-R^{-1}\over g}>0.
\]

Equation (9), including the exceptional f=0 term at n=1, gives

\[
 m_n=cR^n+e_n,\qquad |e_n|\le {g-1\over g}S^n.             \tag{10}
\]

Indeed each nonidentity summand is
`c_f (f^2-1) f^(2n-2)/g`. Its absolute value without c_f/g is at most
S^n, also for f=0 and n=1. This is a bound on the actual full spectrum,
not deletion of a lower-order archive block.

The full heat trace exists for every t>0 and is exactly

\[
 K_b(t)=\operatorname{Tr}_{GNS}e^{-tD_b^2}
             =1+\sum_{n\ge1}m_n e^{-tB^n}.                \tag{11}
\]

The one is the scalar zero mode. Define the positive function

\[
 Q_B(s)=\sum_{k\in\mathbb Z}(sB^k)^\alpha e^{-sB^k},
 \qquad Q_B(Bs)=Q_B(s).                                   \tag{12}
\]

The series converges uniformly on every compact positive s interval:
the negative tail is geometric, and the positive tail is dominated by
arbitrarily high inverse powers, using `exp(x)>=x^p/p!` with an integer
p>alpha. Therefore Q_B is continuous, bounded above and bounded away
from zero on [1,B]. Completing the main sum in (11) to all integer levels
and applying the same estimate with exponent sigma to (10) proves

\[
 t^\alpha K_b(t)=cQ_B(t)+O_b(t^{\alpha-\sigma})+O_b(t^\alpha).
                                                               \tag{13}
\]

For the completion error, the added levels n<=0 contribute at most
`t^alpha/(1-R^-1)`. Formula (13) consequently proves two-sided bounds
`K_b(t) asymp t^-alpha` for small t, with genuine positive constants.
It follows that a finite **positive** leading four-dimensional coefficient

\[
                     t^2K_b(t)\longrightarrow a_0>0       \tag{14}
\]

is possible only at alpha=2, equivalently b=sqrt(33). If b is larger,
the left side tends to zero; if b is smaller, it diverges to infinity.
This is a necessary test of the heat reading, not permission to select b.
In particular spectral dimension four alone is not yet (14).

### 6.1 Exact phase separation at the only possible scale

At B=33, alpha=2, two geometric sequences give different limits:

\[
 \lim_{N\to\infty}(33^{-N})^2K_b(33^{-N})=cQ_{33}(1),
\]
\[
 \lim_{N\to\infty}(33^{-N}/3)^2K_b(33^{-N}/3)=cQ_{33}(1/3).
                                                               \tag{15}
\]

The difference can be bounded with rational arithmetic, without a
numerical heat extrapolation, a complex-pole argument or a Gamma theorem.
The k=0 term and exp(1)<3 give Q_33(1)>1/3. For s=1/3, split (12) into
k<=-1, k=0, k=1 and k>=2. Respectively their upper bounds are

\[
 {1\over9(1089-1)},\qquad {1\over12},\qquad
 121(3/8)^{11},\qquad {216\over1089(1089-1)}.              \tag{16}
\]

The first is a geometric sum with exp(-x)<=1. The second uses
exp(1/3)>=4/3. The third uses exp(1)>8/3. For the last, use
`x^2 exp(-x)<=24/x^2` and sum the whole positive tail from k=2.
The four rational bounds sum to

\[
 {13694175177875\over159025459101696}<{1\over10}.
\]

The elementary bounds on exp(1) also have finite controls: its first
four Taylor terms sum to 8/3; bounding the rest by a ratio-1/5 geometric
tail gives exp(1)<87/32<3. Hence the two limits in (15) differ by more
than 7c/30. All infinite tails and all nonidentity group contributions
have been controlled analytically. This is not evidence from a finite
list of levels.

**Conclusion for the whole stated operator family.** For no fixed b>1
does the full heat trace of this D_b squared have a positive finite
coefficient (14). In particular it cannot have the usual four-dimensional
heat expansion `a_0 t^-2 + a_2 t^-1 + o(t^-1)` with a_0>0. Matching the
spectral exponent to four does not supply even its first coefficient.
A fixed positive rescaling of heat time, a fixed nonzero trace calibration,
or a bounded finite-mode change cannot remove the separated subsequences:
they shift the phases, multiply both limits, or give a vanishing t^2 error.
No such alteration is introduced here.

### 6.2 What this excludes, and what it leaves open

This is a complete obstruction to directly using **the full unaveraged
trace of this geometric filtration operator** for the usual positive-volume
four-dimensional small-time heat law. That particular input to a curvature
coefficient/Einstein-Hilbert bridge is unavailable. The metric theorem in
Sections 1--5 remains true; it never asserted this heat expansion.

At each fixed phase s>0, the geometric subsequence
`t=s*33^-N` does have the positive limit cQ_33(s). Thus a native construction
using only a specified discrete level sequence is not excluded by failure
of (14). Its actual physical scale law, phase dependence, metric readout
and complete price variation would have to be derived. Likewise this
argument does not exclude a separately owned physical observable algebra,
another native coupled operator, or a justified limiting/averaged reading.
None is chosen, and no trace or archive sector is discarded.

The full bootstrap action has not been identified with (11). Accordingly
this result does not imply absence of every F, zero or pure-trace stress,
failure of all gravitational limits, or closure of T0--T3. It removes the
specific inference from this actual AF metric/finite spectral dimension
to the standard four-dimensional heat coefficient. The common preparation,
all joint field directions and the source comparison remain the same
open obligations. The full asymptotic proof is analytic; the replay checks
the exact owned multiplicities, rational tail bounds and hostile alterations.

## 7. Every fixed phase retains an intermediate archive order

Continuation input: `cad6f9a3168d26c72a72a98a71d737e470bac508`.
The geometric-subsequence exception in Section 6 is genuine. We now test
its next necessary heat coefficient on the **same full operator**, without
choosing a phase, spectrum, averaging law or counterterm. The positive
leading subsequence limit survives. The usual following t^-1 curvature
coefficient does not exist on any fixed phase.

Only b=sqrt(33) can have the required positive leading t^-2 order, so fix
B=b^2=33 for this necessary test. This is not native scale admission.
For each f>=2 with c_f>0 define

\[
 \alpha_f={\log(f^2)\over\log33},\quad
 \kappa_f={c_f\over g}(1-f^{-2}),\quad
 Q_f(s)=\sum_{k\in\mathbb Z}(s33^k)^{\alpha_f}e^{-s33^k},
 \quad a_f(s)=\kappa_f Q_f(s)>0.                         \tag{17}
\]

These functions have multiplicative period 33 and are bounded above and
away from zero on a fundamental phase interval. The uniform convergence
argument in Section 6 applies separately to each of the finitely many f.
The f labels form a Burnside counting decomposition, not an asserted
orthogonal sum of physical sectors. Its generally fractional coefficients
do not license independently variable native heat blocks.
The complete Burnside multiplicities in (9) give an **exact**, all-t>0
decomposition

\[
 K_b(t)=\sum_{f\ge2,\ c_f>0} a_f(t)t^{-\alpha_f}+r(t),    \tag{18}
\]
\[
 r(t)=1-{c_0\over g}e^{-33t}
       -\sum_{f\ge2,\ c_f>0}\kappa_f
                    \sum_{n\le0}f^{2n}e^{-t33^n}.        \tag{19}
\]

To obtain (18), first expand `m_n` using (9). The f=0 contribution is
exactly `-c_0 exp(-33t)/g`, because only n=1 survives. The f=1 increment
is zero. For every f>=2, complete its positive n sum to all integer levels.
Absolute convergence, or finite f summation followed by its positive
convergent series, justifies the rearrangement. No modes have been removed.

The remainder has particularly simple exact bounds:

\[
                 {c_1\over g}\le r(t)\le1,
          \qquad r(t)\longrightarrow {c_1\over g}.        \tag{20}
\]

Indeed each exponential is at most one and
`kappa_f sum_(n<=0) f^(2n)=c_f/g`. The lower bound follows from
`sum_f c_f=g`, and the upper bound from nonnegative subtracted terms.
Dominated convergence in the summable negative-level geometric tails
proves the limit. This also accounts explicitly for the zero and one
fixed-point strata; neither is silently dropped.

### 7.1 The second coefficient fails for every fixed phase

Along `t_N=s*33^-N`, s>0 fixed, every a_f(t_N) equals a_f(s).
The positive leading coefficient is exactly a_33(s). The next stratum
has c_31=169 and

\[
             1<\alpha_{31}={\log961\over\log33}<2.        \tag{21}
\]

There is no f=32 stratum, and all f<=30 have smaller exponents. Therefore

\[
 t_N^{\alpha_{31}}
   \bigl(K_b(t_N)-a_{33}(s)t_N^{-2}\bigr)
                     \longrightarrow a_{31}(s)>0.        \tag{22}
\]

This follows directly from the finite exact decomposition (18): after
multiplication all smaller powers tend to zero and r is bounded. In
particular the proposed ordinary second heat coefficient diverges:

\[
 t_N\bigl(K_b(t_N)-a_{33}(s)t_N^{-2}\bigr)
                           \longrightarrow +\infty.      \tag{23}
\]

No choice of a fixed phase s avoids (23). More strongly, even subtracting
the **exact phase-dependent leading term** at every t leaves

\[
 t\bigl(K_b(t)-a_{33}(t)t^{-2}\bigr)
                           \longrightarrow +\infty       \tag{24}
\]

through all positive t tending to zero. To see uniform positivity without
an unspecified compactness constant, reduce s to [1,33]. The k=-1 term
in Q_31 has `x=s/33 in [1/33,1]`, hence
`x^alpha_31 >= 1/961` and `exp(-x)>1/3`. Consequently for every phase

\[
 a_{31}(s)>{169\cdot320\over g\cdot961^2}>0.              \tag{25}
\]

All other terms remaining in (18) and r(t) are nonnegative. This lower
bound times `t^(1-alpha_31)` proves (24). A fixed positive time or trace
unit rescaling changes constants, not the intervening power.

The normalized leading convergence on a fixed phase has the exact first
error order

\[
 t_N^2K_b(t_N)-a_{33}(s)
      =a_{31}(s)t_N^{2-\alpha_{31}}
                   +o(t_N^{2-\alpha_{31}}).               \tag{26}
\]

In level coordinates its rate is `(961/1089)^N`, times the fixed s
coefficient. This is a statement about this heat reading. It is not an
O(h) action-contrast obstruction: no physical h or price normalization
has been derived from the archive level.

### 7.2 All intervening powers remain explicit

For the actual count table, every f in {0,...,31,33} occurs. The strata
f=6,...,31 all have `1<alpha_f<2`; f=2,...,5 have `0<alpha_f<1`.
There is no alpha_f=1 because no integer f has f^2=33. Thus (18) identifies
the entire finite set of intermediate orders, not only a sampled leading
error. Positivity prevents their cancellation within this full heat trace.

As an algebraic negative control, if one formally subtracts **every** term
with f>=6, the remaining trace multiplied by t tends to zero, even while
the phase varies. This follows from bounded periodic a_f for f<=5 and
(20). Such a subtraction is not a native operation or an admitted
counterterm here; it does not construct a curvature coefficient or prove
zero physical stress. It exposes exactly what a putative reading would
have to account for, rather than hiding the archive terms in an error.

The retained fixed-phase leading limit therefore cannot, by itself,
support the usual two-term `a_0 t^-2+a_2 t^-1+o(t^-1)` bridge. A separately
derived physical observable, coupled price or limiting law may obey a
different theorem. None is introduced or excluded wholesale. In particular
the full bootstrap heat/feedback/matter derivative has not been identified
with this scalar heat expansion. Common terms might cancel in actual
paired price contrasts; that must be tested on an owned preparation and
is not excluded by a scalar heat-coefficient obstruction. Native F, all joint metric/link/matter
directions, source/Ward, stationarity and the original GR/recovery goals
remain open. This is the complete second-coefficient boundary of the
named full operator, with the whole native archive retained.

The cumulative replay has 452 exact controls (195 metric, 121 first heat,
136 full-stratum/phase controls), nineteen executed mathematical mutation
rejections and thirty-three false scope rejections. Two explicit shallow-path
replays verify that the mutation runner resolves `--repo` before inspecting
its temporary script location. The analytical limits above are not claimed
Lean-formalized.
