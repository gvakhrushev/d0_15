# Q8 quadrature and realification: a complete finite Book-feedback source interface

**21 October 2026 · Existing Draft PR #334 · bounded mathematical synthesis · `GR_closed=false`.**

## Executive result

The earlier reverse-source theorem reconstructs the **real symmetric** effects
`N=W*W`, `B=W*P W` of the normalized complementary Book feedback from
ordinary unequal Golden input superpositions. It explicitly leaves the
**complex Hermitian** Fourier/CAR case outside that real-probe theorem.
This note closes that *mathematical phase-input gap* by combining the existing
Golden pair with the already described real quaternion/quarter-turn memory
representation of Book03 §03.1.3. It does **not** construct or claim the
native physical port that implements the doubled complex instrument.

For a complex input space of dimension `d`, exactly **d²** explicitly
specified realified Golden input settings recover **every entry** of an
arbitrary Hermitian effect and all its admitted first variations. This count
is dimension-minimal for unconstrained Hermitian effects. The entire
cost-normalized Book feedback and first source transport **exactly**, with
one mandatory factor `1/2` when taking the doubled real determinant. The
actual original full128 Fourier/CAR16 `n=2` fixture passes the complete test:
128 native Kraus operators, their jets, realified completeness, all 256
settings for both effects, and the true nonscalar marked source.

Two further results make the physical boundary precise. Real-only Golden
probes are insufficient even for the first source at an original
complex native anchor. Faithful terminal Q8 memory representations can
recover aggregate class coefficients but not separate weights of distinct
histories mapped to the same memory class. Thus the missing native Book03
`Info` cannot be supplied by *either* unphased effect statistics or a
memory-class sum without retained history resolution.

## 1. Exact realification as a *-representation, not an extra action

For a complex rectangular matrix `T=X+iY`, let

\[
\mathcal R(T)=\begin{pmatrix}X&-Y\\Y&X\end{pmatrix},\qquad
J=\begin{pmatrix}0&-I\\I&0\end{pmatrix},\qquad J^2=-I.
\tag{1}
\]

In particular, a complex input `v=x+iy` is represented by the **real**
vector `\widehat v=(x,y)`. These identities follow by direct block
multiplication, for compatible matrices:

\[
\mathcal R(TS)=\mathcal R(T)\mathcal R(S),\quad
\mathcal R(T^*)=\mathcal R(T)^T,\quad
\|\mathcal R(T)\widehat v\|^2=\|Tv\|^2.
\tag{2}
\]

If the complete complex instrument obeys `sum_omega K_omega* K_omega=I`,
its doubled **real** instrument obeys
`sum_omega R(K_omega)^T R(K_omega)=I_(2d)`. Its complete retained Kraus
columns and field jets are transported algebraically, not thrown away.
The original real Q8 left-multiplication carrier has a compatible
quarter-turn; its `J` has exactly the multiplication rule used in (1).
This is a specific **representation-level identification**. It does not
show that a controlled `J` and every `R(K_omega)` are executable from the
same blank state with the original paid Golden/CNOT scene controller.

Let `W` be the complete (possibly cost-marked) retained amplitude and `P`
the **actual specified** active cut. Put

\[
N=W^*W>0,\quad B=W^*PW,\quad M=(1-z)N+zB,\quad0<z<1.
\tag{3}
\]

The original full128 normalization theorem already proves
`J_C=r_R[log det_C N-log det_C M]`, including the nonscalar normalizer.
Under (1), `N_R=R(N)`, `B_R=R(B)`, `P_R=R(P)` and `M_R=R(M)`.
For any positive-definite Hermitian X,

\[
\det_\mathbb R\mathcal R(X)=(\det_\mathbb C X)^2,
\quad
\operatorname{Tr}_{\mathbb R}\log\mathcal R(X)
=2\operatorname{Tr}_{\mathbb C}\log X.
\]

Hence **on the same input, same cut, same cost mark and same source jets**

\[
\boxed{\quad
J_C={r_R\over2}
 \left[\log\det_\mathbb R N_R-\log\det_\mathbb R M_R\right].
\quad}\tag{4}
\]

For arbitrary genuine first variations, including a moving cut, moving
mark and moving z,

\[
\boxed{\quad
DJ_C={r_R\over2}\operatorname{Tr}_{\mathbb R}
\left[N_R^{-1}DN_R-M_R^{-1}DM_R\right]
=r_R\operatorname{ReTr}_{\mathbb C}
\left[N^{-1}DN-M^{-1}DM\right],\quad}
\tag{5}
\]

where `DM=(1-z)DN+z DB+(B-N)Dz` and `DB` includes `W*(DP)W`.
**No new source term is fitted.** In the original spectator oldRIGHT
instance `r_R=128`, the doubled real trace prefactor is **64**, not
128 or 256. Equation (5) is an identity of functional derivatives and
also works at second order when the exact same lifted family exists.
It does not imply that an analytically cost-marked amplitude has become
an actual free physical filter. Its paid filter failures or joint
cost-return statistics remain necessary as in the original owner.

## 2. Exactly d² native-weight quadrature settings suffice

Let `p=phi^-1`, `a=sqrt(p)`, so `a²+p²=1`. For each input basis index j,
use `v_j=e_j`. For each j<k, use the **two** normalized vectors

\[
v_{jk}^{R}=a e_j+p e_k,\qquad
v_{jk}^{Q}=a e_j+i p e_k.
\tag{6}
\]

They correspond respectively to **real-only doubled inputs**
`(a e_j+p e_k,0)` and `(a e_j,p e_k)`. Their unequal weights are exactly
the existing Golden pair; the second vector uses the real quadrature
index `J`, not a presumed native S gate or an imaginary scalar prepared
for free. A fresh doubled real address and the same fixed Boolean
permutations suffice to *prepare these real input vectors on the declared
addressed interface*. The **realified effect/channel access** is an
additional contract; existence of an algebraic representation alone does
not supply a paid physical gate.

For any Hermitian `E`, measure its quadratic expectations on the
**specified realified input effect**. With `q_j=<v_j,E v_j>` and
`q^{R/Q}_{jk}=<v^{R/Q}_{jk},E v^{R/Q}_{jk}>`,

\[
\boxed{\begin{aligned}
E_{jj}&=q_j,\\
\operatorname{Re}E_{jk}&=
 \frac{q^R_{jk}-p q_j-p^2q_k}{2ap},\\
\operatorname{Im}E_{jk}&=-
 \frac{q^Q_{jk}-p q_j-p^2q_k}{2ap}.
\end{aligned}}\tag{7}
\]

There are `d + 2 binom(d,2)=d²` scalar settings; Hermitian d×d
matrices have d² real parameters. Every linear scalar expectation map
into fewer than d² real outcomes has a nontrivial kernel on **all**
Hermitian effects. Thus the count is optimal for arbitrary effects.
The same fixed linear inverse (7) reconstructs `DN`, `DB` from admitted
first variations of the **complete probabilities**; its conditioning
factor `1/(2ap)` and all factory readiness factors must be retained.

For the actual old Fourier/CAR16 feedback, the proven native parity
algebra is block diagonal `M8 \oplus M8`. If the realified tests can
address each original parity sector without changing the cut, equation
(7) needs only `2*8²=128` scalar settings **per effect**, rather than
256. At an anchor the old source-sufficiency theorem preserves the
entire first source even against arbitrary off-parity effect jets.
It does not preserve an arbitrary ambient Hessian; the exact defect
from that owner remains in force. Do not discard a parity block,
spatial sites, ports, histories, or the full oldRIGHT multiplicity.

### An exact obstruction if quadrature is absent

Ordinary real Golden superpositions cannot distinguish `E=X+iY`
from `E'=X-iY` at the level of a chosen real input, or see a purely
imaginary Hermitian first jet `iY` with Y real antisymmetric. This
failure affects the Book feedback itself, not merely microscopic phases.
For the exact two-dimensional witness

\[
N=I,\quad B(s)=\begin{pmatrix}1/2&i(1/4+s)\\
-i(1/4+s)&1/2\end{pmatrix},\quad z=1/2,
\]

`0<B(s)<I` for sufficiently small s. All real vectors have
`d/ds <v,B(s)v>=0`, while `det M(s)=9/16-(1/8+s/2)^2` gives

\[
\boxed{\quad \frac{d}{ds}[-\log\det M(s)]_{s=0}=\frac8{35}\ne0.\quad}\tag{8}
\]

At the **original** numerical two-round full128 CAR anchor
`theta=.08, marker t=.7, z=2^-20`, an imaginary Hermitian ambient effect
jet supported on the `(0,3)` Fourier entries likewise yields a nonzero
Book first derivative about `1.12385665e-7`, while all original real
Golden probes see its zero first jet. This ambient effect variation is
positive-feasible near the anchor, but is **not** claimed to be an
admitted geometric, preparation or native primitive variation. The
numerical control excludes a universal claim that original *real*
Golden probes suffice for every ambient Book source; the exact (8)
proves the mathematical need independently of numerics.

## 3. Book06 maximum entropy and what it really determines

The Book06 §§06.24–25 retained-test rule is a maximum-entropy coupling,
with specified test algebra and loss quotient. The earlier source algebra
theorem establishes that, among fixed unital complex *-algebras and
**arbitrary independent Hermitian N/B jets**, `A_min=C*(N,B)` is the
minimal algebra retaining the first feedback source. It is **not** a
claim that all of these algebra elements are affordable native tests.

There is a precise, useful dual consequence. Let `A` be a fixed finite
unital *-algebra of actually declared retained tests, and `E_A` its
trace-preserving conditional expectation. For any full-rank density
`rho`, the only state maximizing von Neumann entropy among all sigma
with `Tr sigma a=Tr rho a` for all `a in A` is

\[
\boxed{\tau=E_A(\rho).}\tag{9}
\]

Indeed, `log tau in A`, so every admissible sigma satisfies
`D(sigma||tau)=S(tau)-S(sigma)>=0`, with equality only at sigma=tau.
In particular, `S(tau)-S(rho)=D(rho||tau)>=0` is an exact
maximum-entropy **loss of fine distinctions**. Along nested retained
algebras `A_0\subseteq A_1\subseteq\cdots`, the relative-entropy
increments telescope and are nonnegative, giving an additive finite
candidate information accounting. This is a genuine intersection of
source sufficiency and Book06's entropy-selected forgetting. However
`A_min` need not be a native admitted affordable test algebra, and
this **mean** entropy loss is not automatically Book03's branchwise
`Info(gamma)`. Neither the observer's cut nor the pathwise gains are
thereby physically chosen. In particular a parity-even input may
have zero loss under parity expectation even while its output
instrument has a nonzero reported Shannon entropy.

## 4. Why full faithful Q8 memory still may not determine branch Info

Book03 §03.1.3 supplies the finite Q8 regular memory representation
`R_q` which faithfully recovers coefficients of an **algebraic sum**
`Z=sum_q w_q R_q` by reading the identity column. This is powerful
and remains exact. But if **two distinct retained histories**
`gamma1!=gamma2` map to the same terminal memory class q, only
`w_gamma1+w_gamma2` occurs in that coefficient. For every small epsilon,

\[
(w_{\gamma_1},w_{\gamma_2})\mapsto
 (w_{\gamma_1}+\epsilon,w_{\gamma_2}-\epsilon)
\tag{10}
\]

preserves the entire regular-representation operator and all tests of
that **summed** operator, while it changes the individual positive
history weights and their Book gains (at fixed costs). This is an
exact linear kernel whenever the terminal quotient is noninjective.
It disappears if the actual full path/history tape, rather than the
terminal quotient, separates those histories. One must prove that
separation on the real chosen observer, not assume that Q8's faithful
representation of its **eight memory classes** is a faithful map of
all long chronological histories.

Thus Book03's existing Q8 quarter-turn is a concrete plausible phase
primitive, but **neither** its algebraic representation **nor** its
terminal weight inversion completes the native branchwise valuation
and selection without the fully retained history interface.

## 5. Literal original native computation and scope

The accompanying standalone checker rebuilds the exact original
CAR16/L4 Fourier fixture (`nu=3/5`, role order `0,2,3,1`, phases
`(i,i,-1,-i)`) with its actual 128 Kraus labels and analytic boost/
Julia defect jets. It executes the original two-step **cost-marked
Heisenberg transfer** with charges `1,2` and the actual chronological
blank return `A=e^-t K_00^2`; it does **not** simulate a replacement
full256 spatial geometry or a new Book03 HJR completion.

Checks cover `sum K* K=I`, its derivative, positivity, complex-to-real
*-homomorphism, completeness of all 128 realified outcome maps, exact
`d²` tomography for N/B and DN/DB, whole determinant and complete first
source, imaginary-jet blindness, max-entropy and the memory collision
kernel. The normal and `python -O` runs have **50 scoped checks each**, with
byte-identical result JSON. In the original fixture:

\[
\begin{aligned}
J_{\rm feedback}&\approx5.69052768\cdot10^{-5},\\
D_\theta J_{\rm feedback}&\approx-4.79117979\cdot10^{-6},\\
DJ[\delta B_{(0,3)}]&\approx1.12385665\cdot10^{-7}.
\end{aligned}
\]

The first two agree with the original pre-existing normalization/source
fixture. These decimal numbers are finite numerical diagnostics; the
realification, inverse, entropy and collision theorems above are algebraic.
The checker is a self-contained reimplementation of the original pinned
source formula, not an independently executed full original history suite.
No external peer review, Lean build or complete original root campaign is
claimed for this packet.

**What is newly closed:** the previous complex-phase algebraic input gap
for feedback source tomography and its exact real representation, plus
the universal obstruction to real-only source tomography. This uses
precisely the Q8 complex structure which Book03 already carries.

**Still open for GR:** one native paid preparation of the actual doubled
input and realified primitive/observer; one actual common controller and
retained time/Info history; the independent matter/preparation rows and
Book03 H+J+R/source equality on that execution; and the original-carrier
uniform refinement. There is no assertion of exact finite-code stationary
GR, physical necessity of the Golden realization, or a fixed physical
`Info` rule. `GR_closed=false` and PR #334 stays Draft.