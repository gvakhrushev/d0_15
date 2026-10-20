# Complete-history code classes: universal first source and exact-root transfer

19 October 2026. Same Draft #334, task
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input: `46147621adcbfd64fd639b3ca7f8d6730565b4de`.
**Status: analytical source theorem, exact finite controls, conditional full-root
transfer. Physical D0 price selection and GR closure remain open.**

## 1. The parent substitution, and what is actually new

The [existing golden coding owner](A4D_OPERATIVE_GOLDEN_INFORMATION_AND_GR_GATE_2026_10_17.md),
§§2–3, already constructs ONE fixed universal F/R code and proves C1 entropy
convergence on a fixed faithful IID chart. We do not claim that result anew.
[Strategic §7.43](A4D_STRATEGIC_SYNTHESIS_FOUNDATIONS_TO_GR_2026_10_17.md)
still asks how the actual `D_min` of a complete history can inherit that source.

Here the first-source theorem applies to EVERY fixed competitive injective
code, including non-prefix canonical descriptions. It requires no chosen
optimal encoder, no equality of `D_min` to the universal code, and no separate
positive probability floor. A full-history score bound replaces IID where
available. We also prove that these hypotheses do NOT imply C2 convergence,
but C1 source control can still produce exact roots by a finite-dimensional
fixed-point argument. No new physical action is introduced.

The consumer is the full-source seam, then the
[two-coefficient Einstein stratum](A4D_MICROHISTORY_EINSTEIN_QUOTIENT_AND_PRICE_EULER_UNIVERSALITY_2026_10_18.md),
§3, and its
[time-dependent all-40 extension](A4D_ARBITRARY_BRINKMANN_ALL40_CARTAN_DISCRETE_EINSTEIN_2026_10_19.md).
The conditional substitution does not close an accepted assembly obligation.

## 2. The finite complete-history source theorem

Fix a finite set of COMPLETE distinguishable histories `Omega_N`, one
field-independent code length `L_N(w)`, and a positive C1 probability law
`P_x(w)` on that same set. `N>0` is a declared rate denominator, not the
number of alternative outcomes. Put

\[
 \ell=\log\varphi,\quad R(w)=L_N(w)+\ell^{-1}\log P_x(w),\quad
 s_V(w)=D_V\log P_x(w),\quad I_N(V)=\mathbb E_x s_V^2.
 \tag{1}
\]

Suppose, uniformly on the chart where a uniform conclusion is needed,

\[
 \sum_w e^{-\ell L_N(w)}\le K_N,\qquad K_N\ge1,
 \qquad R(w)\le B_N,
 \qquad B_N\ge0.
 \tag{2}
\]

Define `a_N=log(K_N)/ell` and

\[
 C_N^2=B_N^2+a_N^2+2a_N/\ell+2/\ell^2.
 \tag{3}
\]

Then, with Shannon measured in the SAME golden cost unit,

\[
 -a_N/N\le {\mathbb E L_N\over N}-{H_\varphi(P_x)\over N}
 \le B_N/N,
 \tag{4}
\]
\[
 \boxed{
 D_V\left[{\mathbb E L_N-H_\varphi(P_x)\over N}\right]
 ={\mathbb E(Rs_V)\over N},\qquad
 \left|D_V\left[{\mathbb E L_N-H_\varphi(P_x)\over N}\right]\right|
 \le {C_N\sqrt{I_N(V)}\over N}.}
 \tag{5}
\]

**Proof.** Normalization gives `E s_V=0`. The entire code mass, including all
outcomes, satisfies

\[
 \mathbb E e^{-\ell R}=\sum_w e^{-\ell L_N(w)}\le K_N.
\]

Jensen gives `E R>=-a_N`; the upper bound is pointwise. Markov's inequality
gives `Pr(R<-t)<=min(1,K_N exp(-ell t))`. Thus

\[
 \mathbb E R_-^2
 \le\int_0^{a_N}2t\,dt+
       \int_{a_N}^{\infty}2t e^{-\ell(t-a_N)}dt
 =a_N^2+2a_N/\ell+2/\ell^2.
\]

Since `R_+<=B_N`, (3) bounds `E R²`. Differentiating the finite expectation
retains the moving law: `D E R=E(Rs_V)+E s_V/ell=E(Rs_V)`.
Cauchy–Schwarz proves (5). This is an analytic theorem, not inference from
the finite checker.

For any specified physical variation norm,

\[
 \left\|D\left[{\mathbb E L_N-H_\varphi(P_x)\over N}\right]\right\|_*
 \le {C_N\over N}
 \sup_{\|V\|\le1}\sqrt{I_N(V)}.
 \tag{6}
\]

Small probabilities are allowed: there is no separate `min P` in (6).
Uniform control of the displayed Fisher norm is still required. This theorem
does not assert differentiability through moving zero probabilities or a
change of the complete record space/code/admissibility predicate.

## 3. Prefix-free is unnecessary for canonical descriptions

Let one fixed injective decoder representation assign each complete outcome
a finite F/R word with TRUE cost `c=#F+2#R`. For words of cost `j`, the count
`A_j` satisfies `A_0=A_1=1`, `A_j=A_(j-1)+A_(j-2)`, and hence
`A_j<=phi^j`, since `phi^-1+phi^-2=1`.

If all assigned costs are at most `M_N`, then

\[
 \boxed{\sum_w\varphi^{-L_N(w)}
 \le\sum_{j=0}^{\lfloor M_N\rfloor} A_j\varphi^{-j}
 \le\lfloor M_N\rfloor+1.}
 \tag{7}
\]

Thus the logarithmic Kraft defect `a_N` is at most
`log_phi(floor(M_N)+1)`. Prefix-free codes give the stronger `a_N=0`, but are
not necessary for (4)–(6). Injectivity and one fixed represented history set
ARE necessary; independent shortest-code choices with no common decoder do
not supply (7).

More generally, for a cost language with `A_j<=C b^j`, the same proof uses
`ell=log b` and `K_N=C(floor M_N+1)`. An ordinary alphabet of size `b` and
unit letter costs has entropy unit `log b`. Golden unit costs cannot be
inferred from the notation `|D_min|` alone.

## 4. One universal competitor suffices for the whole code class

For `k` complete outcomes and `N` IID copies, the existing owner uses the
type count and complete universal law

\[
 T_N={N+k-1\choose k-1},\qquad
 Q_N(w)={1\over T_N M(\operatorname{type}w)}.
\]

The actual golden midpoint encoder has cost
`c_U(w)<-log_phi Q_N(w)+b_phi`, where `b_phi=2+log_phi 2`.
Since `P_q^N(w)/Q_N(w)=T_N P_q(type w)<=T_N`, ANY fixed injective description
satisfying the same-object competitive inequality

\[
 L_N(w)\le c_U(w)+d_N
 \tag{8}
\]

with `d_N>=0` (without loss of generality) meets (2)–(3) with

\[
 B_N=\log_\varphi T_N+b_\varphi+d_N,\qquad
 M_N=N\log_\varphi k+B_N,\qquad
 a_N=\log_\varphi(\lfloor M_N\rfloor+1).
 \tag{9}
\]

For fixed `k`, `d_N=O(log N)` and bounded one-copy Fisher norm `J(V)`,
`I_N(V)=N J(V)^2`. Therefore every such code has

\[
 {\mathbb E L_N\over N}\longrightarrow H_\varphi(q),\qquad
 D\!\left[{\mathbb E L_N\over N}\right]
 =D H_\varphi(q)+O_*(\log N/\sqrt N).
 \tag{10}
\]

The constant is given by (6), not an implicit dimension-independent claim
when `k=k(h)` grows. This improves the parent's single-encoder faithful-chart
estimate to a code-class result without requiring computation of `D_min`.

**Correlated histories.** The general theorem never used IID. The same type
competitor dominates every exchangeable law by `T_N`; its entropy target is
then `H(P_N)/N`, not necessarily a one-site Shannon entropy. For a finite
directed graph with `s` states and `E` edges, all complete TIME-HOMOGENEOUS
Markov histories on that fixed support
of length `N` are partitioned by initial state and edge counts. Their
probabilities are constant within each type. There are at most
`s(N+1)^E` nonempty types. The uniform-type/uniform-within-type law and the
same golden interval code give (8) with
`B_N<=log_phi s+E log_phi(N+1)+b_phi+d_N`.
No identification of the full quantum D0 history with this Markov class is
made. In particular, the actual central scene/Perron law is not thereby
turned into a curvature source.

For ANY normalized sequential law `P=prod_j p_x(Y_j|Y_<j)`, the conditional
scores have zero conditional expectation. Their cross inner products vanish,
so exactly

\[
 I_N(V)=\sum_j\mathbb E I_j(V\mid Y_{<j}).
 \tag{11}
\]

Consequently a genuine uniform per-step conditional Fisher bound can replace
IID in the source estimate, provided the required competitive code is also
owned. For a differentiable complete recorded purification
`Psi=sum_w |w> Psi_w`, Cauchy–Schwarz separately gives
`I_N(V)<=4 sum_w ||D_V Psi_w||²`. These are possible ways to supply the
displayed norm, not free bounds for long coherent native words.

## 5. What `D_min` now needs, and an exact obstruction to assuming it

[Book 01](../../01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md),
§§01.1.2, 01.1.4 and 01.2, gives `D_min=Can(Enc X)`, a shortest
representative in the actual equivalence class, and `F0=|D_min|`. Its
self-delimiting `Pair` has logarithmic length overhead. It does NOT state
that the universal compressed history and the expanded history are
equivalent under the actual `Delta`, or identify ordinary code length with
golden weighted cost.

The sufficient semantic bridge is narrower than “implement the unique
optimal encoder”: in the SAME cost unit and on the same complete history,
an ALREADY admitted decoder must make

\[
 \operatorname{Pair}(\mathrm{decoder}_N,U_N(X_N))
 \sim_\Delta\operatorname{Enc}(X_N)
 \tag{12}
\]

with overhead `d_N` satisfying (6). The actual minimizing descriptions must
themselves have ONE fixed injective F/R representation with that cost, or a
different code language with its proved growth bound `A_j<=C b^j` and the
corresponding entropy unit. A golden competitor inside an unrestricted
binary language does not change that language's growth from `2^j` to
`phi^j`. Under this additional representation hypothesis, minimality gives
(8), and injectivity/counting gives (7) in the golden case. In another
language of capacity `log b`, one must ALSO supply a capacity-matched
competitor with `L_N+log_b P_N<=B_N` small enough for (6). A golden
competitor alone can leave a linear redundancy in binary cost units and
does not prove the corresponding source limit. One need not know the minimizing code or
make its codewords prefix-free. The `Pair` theorem controls formatting only
AFTER this same-object decoder has been admitted.

**Exact interface countermodel.** Use the existing literal golden binary
format `F->0`, `R->10`; distinguish objects by equality of their complete
literal binary words, and let `Can` be identity on these equivalence
classes. Then `|D_min(X_N)|=#F+2#R`. On IID complete F/R histories with
`Pr(R)=theta`,

\[
 N^{-1}\mathbb E |D_{\min}|=1+\theta,
 \qquad D_\theta(N^{-1}\mathbb E |D_{\min}|)=1,
 \qquad H_\varphi'(1/2)=0.
 \tag{13}
\]

Every history is retained and uniquely represented, but (12) is absent:
compressed words are not synonyms in this declared comparison interface.
Thus canonicity, injectivity and golden word counts alone do NOT imply the
entropy source. This is a countermodel to that inference from the cited
interfaces, not a countermodel to the complete D0 foundation.

**Expected description and Book weights are different interfaces.** For
a fixed code on a fixed frame, `phi^-L_N(w)` and its total mass do not vary
with the fields. They cannot simultaneously be the normalized law of a
nonconstant detector family `P_x`. Equation (5) differentiates the expected
description under the ACTUAL moving law; it does not select that law as a
Boltzmann weight of the same fixed code. A field-dependent code, changing
frame or decoder introduces additional sources and is outside (1).

The [same-history Book owner](A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md)
instead has, AFTER its own likelihood binding,

\[
 {1\over N}D\mathbb E S_{\rm Book}
 ={D H_{\rm nat}(P_N)-D\log Z_{\rm raw}\over N\ell}.
 \tag{14}
\]

Our code source differs by the controlled term (5) PLUS
`D log Z_raw/(N ell)`. No code theorem removes this term, native work,
preparation, clock, or old-history price. Short description is not cheap
execution; the [compiler owner](A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md)
retains those budgets.

## 6. A sharp C2 obstruction, with all codewords retained

Take ANY fixed competitive prefix code for Bernoulli blocks of length
`N=4m²` (for example, the existing universal code). Append
one F to precisely the codewords with
`A_N={|K-N/2|<=m}`, where `K` counts the second symbol. Prefix-freeness and
injectivity survive, every outcome remains, and the competitive overhead
increases by only one. The two expected code rates differ by

\[
 \delta_N(p)={\Pr_p(A_N)\over N},\qquad
 0\le\delta_N\le N^{-1},\qquad
 |\delta_N'|\le[Np(1-p)]^{-1/2}.
\]

Nevertheless, at `p=1/2`, putting `Z_N=2(K-N/2)/sqrt N` gives

\[
 \delta_N'(1/2)=0,\qquad
 \delta_N''(1/2)=4\mathbb E[(Z_N^2-1)1_{|Z_N|\le1}]
 \longrightarrow -8\,\varphi_G(1)\ne0,
 \tag{15}
\]

where `varphi_G` is the standard Gaussian density, not the golden number.
The limit follows directly from Stirling's formula uniformly on this bounded
central window and its Riemann sum; integrating `(z²-1)varphi_G(z)` gives
`[-z varphi_G(z)]_-1^1=-2 varphi_G(1)`. An exact finite form is

\[
 \delta_N''(1/2)=
 -{2(N-1)(2m+1)\over N/2+m}
 \Pr\{\mathrm{Bin}(N-2,1/2)=N/2+m-1\}.
 \tag{16}
\]

Thus the two competitive codes cannot BOTH have the same limiting Hessian.
We do not assert which one fails without an independent Hessian theorem for
the baseline code. Value and first-source universality do not prove
code-independent spin-2 response, second-source Ward, or C2 recovery.

## 7. Exact roots can nevertheless be transferred with first-source control

There is a useful alternative to demanding a universal C2 code theorem.
Let `B_r(x0)` be a CLOSED finite-dimensional ball and
`F_0: B_r(x0)->R^d` the FULL reference source in one admitted finite
coordinate chart with all non-gauge internal rows included. Suppose
`F_0(x0)=0`, `A=D F_0(x0)` is invertible, and

\[
 \sup_{x\in B_r}\|A^{-1}[F_0(x)-A(x-x_0)]\|\le\rho<r.
 \tag{17}
\]

For a continuous finite code-price source `F_N` on the same chart, if

\[
 \sup_{B_r}\|A^{-1}(F_N-F_0)\|\le r-\rho,
 \tag{18}
\]

there is an EXACT zero of `F_N` in that closed ball. Indeed
`T_N(x)=x-A^-1 F_N(x)` maps the ball into itself by (17)–(18); the
finite-dimensional Brouwer fixed-point theorem gives `T_N(x)=x`.
No derivative of `F_N`, contraction, uniqueness or Hessian convergence is
claimed. Strict inequalities give room for other controlled perturbations.

Equations (6) and (18) compose directly, after the actual source
reconstruction, normalization and full-price remainder are included. If
their amplification is `M_h`, a sufficient bound is

\[
 M_h\left[{C_{N,h}\over N}
       \sup_{\|V\|_h\le1}\sqrt{I_{N,h}(V)}
       +\epsilon_{\rm rest}(h,N)\right]<r_h-\rho_h.
 \tag{19}
\]

This is a genuine exact-root sufficiency theorem, not an assertion that
the all-40 Brinkmann family has such an inverse. Its free wave profiles,
gauge, boundary and internal preparation rows must first be resolved on an
actual admissible chart. An invertible Poisson subblock alone does not
establish (17) for the complete system. If supplying copies changes the
dimension, (17)–(19) must hold on the genuine enlarged systems; no hidden
fixed-dimensional reduction is supplied here. To recover one continuum
solution, the balls/readout errors must also shrink in the required norm.

Without any stability hypothesis, C1 convergence does not preserve roots:
`S_0=x³/3` has source `x²`, whereas `S_epsilon=x³/3+epsilon*x` has no real
critical point for positive epsilon, despite uniform first-source
convergence on compact sets.

## 8. Precise substitution into the GR route

After actual internal stationarity, the existing nonempty null/star sector
needs the SAME full first source

\[
 D S_h=a_hD\sum_x\widehat f_x+b_hD\sum_xq_x,\qquad a_h\ne0.
 \tag{20}
\]

The complete-pointer Shannon consumers already specify the hypotheses under
which their source has this form. With (12), the price binding, and bounded
physical Fisher/reconstruction, (5) transfers that source asymptotically
to an ENTIRE class of minimal descriptions. A common change of code unit
scales `a_h,b_h` together and preserves their ratio; it does not remove
separately sourced native terms. Exact finite substitution requires exact
source equality, or the genuine full-root stability (17)–(19).

For the original unweighted raw ten-row convention, the actual dual norm
and its reconstruction must be used in (6). With signal `sigma_h`, write
`delta_raw` for the UNRESCALED raw-l1 code/rest remainder. The requirement is
`h^-2 delta_raw / |sigma_h| -> 0`, equivalently
`delta_raw=o(|sigma_h| h²)`. If (6) already uses the `h^-2`-scaled dual norm,
its bound must instead be `o(|sigma_h|)`; do not count the mesh factor twice.
This still does not identify the
designated smooth comparator or allow fitting its source.

Increasing `N` is not free. [Full-source §6.81](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md)
already retains an actual copy/preparation window. Any encoder/copy overhead
in (19) must fit that same full-price budget. If the physical action is a
total rather than a rate, divide ALL its Euler rows by the same nonzero
`N`; normalize neither the geometric piece alone nor an independently
priced matter term.

The next missing physical datum is now sharply reduced: one actually
admitted SAME-object decoder, actual description-language growth/cost, and
complete-price law satisfying (12), including its real normalizer/work/internal
sources. Prefix-free `D_min`,
an exactly optimal implemented encoder, and arbitrary C2 coding universality
are not prerequisites for the conditional first-source/existence route.
The underlying field-to-programme binding and general joint geometric
recovery are still independent obligations. Full D0=>GR is NOT proved.

## 9. Decisive checks and review scope

The standard-library checker in
[sources/d0_complete_code_source_2026-10-19/](sources/d0_complete_code_source_2026-10-19/)
uses exact `Q(sqrt(5))` golden intervals and rational complete IID/Markov
laws, verifies the code-class score bounds, and computes the exact
second-jet hostile formula. It tests mathematical interfaces, not physical
actuation, an Einstein root, or the whole repository. Read-only independent
reviews checked the redundancy/score proof and the foundation/price
application; their conclusions are recorded in that packet. Formal
acceptance and scientific promotion are not inferred from these checks.
