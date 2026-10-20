# Complete stopped Golden-Julia flag archive: a source bound without a spectral floor

Research increment for the existing #334 native realization, consuming the
specified compact instrument and finite-cap success-count execution in
`sources/d0_relational_coherent_synthesis_2026-10-20/coherent_execution.md`,
input `07f2f2b15b7050a612d0075aa73db8dc46087a95`.

This calculation concerns the **complete chronological flag archive after
tracing the data and its reference**, not the full native record or the
different literal full128 instrument. It supplies a quantitative first-source
estimate for that archive's coherent relative-code term. Identification of
this term with the compulsory Book03 Info remains a separate physical premise.

## 1. The actual carrier and all complete histories

Let `p=phi^-1`, `g=p^2`, and use the already specified compact Julia Kraus
operators `K_G=p V_j(y)` and `K_B=sqrt(p) I`, with unitary `V_j` on the
original CAR16 data. Repeat each ordered letter until success, advance after
success, stop at `m` successes or at the finite attempt cap `N`. Retain every
chronological flag word, actual stop time and unfinished cap branch.

For each leaf `s`, let `T_s` be its actual attempts and `K_s` its successes.
Its weight and original raw Golden code length are exactly

\[
w_s=g^{K_s}p^{T_s-K_s}=p^{T_s+K_s},\qquad L_s=T_s+K_s.
\]

The leaf tree is complete, so `sum_s w_s=1`. Its Kraft reference is the same
`mu_s=p^{L_s}=w_s`; no normalization or condition on successful completion
has been omitted. These weights and lengths are independent of the compact
field `y` when the integer `m,N` and the actual observer Hilbert fiber are
fixed under variation. A varying observer/coframe metric is included only
after the actual Hilbert fibers have a specified isometric trivialization;
its derivatives must enter the actual U1/P1 bounds below. A fixed-fiber
identity by itself does not establish the native observer source.
The exact Born flag diagonal of the coherent record is
`w`, including all failures. The existing owner's classical identity therefore
continues to hold at the actual stopping time:

\[
\mathbb E L=H_\varphi(w)=(1+g)\mathbb E T.
\]

Every completed branch has the same actual ordered unitary `U_m=V_m...V_1`.
Every unfinished branch has its actual prefix `U_k=V_k...V_1`, `0<=k<m`.
Branchwise unitarity preserves the complete oldRIGHT reduced density, for
arbitrary supplied entanglement. Define

\[
\varepsilon=\Pr[\operatorname{Bin}(N,g)<m].
\]

No incomplete branch is deleted. The mathematical regrouping below is a
unitary change of coordinates within the retained flag register, not physical
forgetting: histories with a common prefix multiply the same data vector.

Choose any supplied normalized initial purification `psi(y)` of the actual
data/oldRIGHT state; an additional purification is a mathematical device,
not a new physically admitted apparatus. With the reference left untouched,
the coherent execution is

\[
|\Psi(y)\rangle=\sum_s\sqrt{w_s}|s\rangle\otimes
  (U_{K_s}(y)\otimes I)|\psi(y)\rangle.
\]

Its complete flag density is `rho_F=Tr_(data,reference) |Psi><Psi|`.
Its nonzero eigenvalues equal those of

\[
\sigma=(1-\varepsilon)|\psi_m\rangle\langle\psi_m|
 +\sum_{s:K_s<m}w_s|\psi_{K_s}\rangle\langle\psi_{K_s}|.
\]

This follows because these are respectively `A^*A` and `AA^*` for the same
matrix of weighted branch vectors. All branch vectors lie in
`{(M tensor I)psi : M in End(C^d)}`, whose dimension is at most `d^2`.
Consequently the flag density rank is at most `r=d^2=256` for CAR16,
independently of the number of histories, attempt cap or oldRIGHT dimension.

## 2. Removing the target from the entropy calculation

Conjugate the complementary density by `U_m^* tensor I`; this changes no flag
eigenvalue. The completed vector becomes `psi`, and every failed vector
becomes `R_s psi`, with `R_s=U_m^* U_(K_s)`.

First suppose the supplied preparation is fixed. The amplitude matrix has
one completed column `sqrt(1-epsilon) psi` and all failed columns
`sqrt(w_s) R_s psi`. Its completed column has zero field derivative. If

\[
\|D_V(R_s\psi)\|\le B\|V\|
\]

for every failed prefix, then

\[
\|D_V A\|_{\rm HS}\le B\sqrt\varepsilon\,\|V\|.
\tag{1}
\]

A moving supplied preparation is also allowed when it has a bounded actual
purification first jet. At the point of variation choose its horizontal phase
and let `K=|D_V psi><psi|-|psi><D_V psi|`. Then `K psi=D_V psi` and
`||K||=||D_V psi||`. An auxiliary unitary connection transports `psi` to a
constant vector for this spectral calculation. The failed-vector derivative
becomes `(D_V R_s)psi+[R_s,K]psi`. Thus (1) holds with

\[
B=2U_1+2P_1,\qquad
\|D_V U_k\|\le U_1\|V\|,\quad
\|(I-|\psi\rangle\langle\psi|)D_V\psi\|\le P_1\|V\|.
\tag{2}
\]

This is an entropy-coordinate change. It does not charge a nonexistent
physical operation or remove a physical preparation/work source. If no
bounded actual preparation jet is supplied, (2) is not available.

## 3. Uniform C1 entropy bound, including rank births

Use natural logs in the entropy `S=-Tr sigma log sigma`. The function of the
amplitude matrix

\[
A\longmapsto-\operatorname{Tr}(AA^*)\log(AA^*)
\]

is C1 even when its rank changes: its singular-value function
`-s^2 log(s^2)` has derivative `-2s(log(s^2)+1)` continuously extended by
zero at `s=0`. A direct regularization makes this a full matrix statement:
put `f_eta(x)=-(x+eta)log(x+eta)+eta log eta`. The smooth functions
`F_eta(A)=Tr f_eta(AA*)` have real Hilbert--Schmidt gradients
`-2[log(AA*+eta I)+I]A`. Their gradient difference from the continuous
zero-mode extension has singular values bounded by
`2 sqrt(lambda) log(1+eta/lambda)<=2 sqrt(eta)` because
`log(1+t)<=sqrt(t)` for t>=0. Thus the gradients converge uniformly on each
fixed finite matrix space, with norm error at most `2 sqrt(r eta)`. The
functions converge to the stated entropy and are all zero at A=0, so uniform
gradient convergence proves C1 and its full derivative, including rank
changes. The rank r in this regularization can be the finite ambient rank
bound; the sharper actual CAR16 bound is used in the moment below.
For a normalized amplitude the trace derivative is zero, hence

\[
|D_V S|\le2\|D_VA\|_{\rm HS}
  \sqrt{\operatorname{Tr}\sigma(\log\sigma)^2}.
\tag{3}
\]

The dominant eigenvalue is at least `1-epsilon`. Every other eigenvalue is
at most epsilon and their sum is at most epsilon. If
`0<epsilon<=exp(-2)` and `r>=2`, concavity of `x(log x)^2` on
`0<x<=exp(-1)` and its monotonicity on `0<x<=exp(-2)` give

\[
\operatorname{Tr}\sigma(\log\sigma)^2
\le (1-\varepsilon)\log^2(1-\varepsilon)
 +\varepsilon\log^2\!\frac{\varepsilon}{r-1}.
\tag{4}
\]

Indeed, if the tail mass is `a<=epsilon`, Jensen bounds its at-most `r-1`
entries by `a log^2(a/(r-1))`, which increases over this range; the dominant
term is bounded at `1-epsilon`. Zeros contribute zero. Combining (1)--(4):

\[
\boxed{
\|DS(\rho_F)\|_*
\le2B\sqrt\varepsilon\,
\sqrt{(1-\varepsilon)\log^2(1-\varepsilon)
 +\varepsilon\log^2\!\frac{\varepsilon}{r-1}}
=O\!\left(B\varepsilon\log\frac{r-1}{\varepsilon}\right).
}\tag{5}
\]

No lower bound on a nonzero eigenvalue or per-history probability is used.
For epsilon=0 the flag archive is a fixed pure product factor and the source
is exactly zero. Formula (5) controls the full derivative, including moving
eigenvectors: it was derived from the full amplitude matrix, not from an
assumed diagonal source formula.

## 4. Actual code-relative flag source and normalized refinement

For the specific coherent relative-code component on this archive,

\[
\mathcal A_F
=D_\varphi(\rho_F\Vert\operatorname{diag}w)
=H_\varphi(w)-S(\rho_F)/\log\varphi.
\]

The equality uses the exact actual diagonal `w`. It does not replace the
full native price by this component. Since the original Golden code and all
flag probabilities are fixed under these compact variations,

\[
\boxed{D\mathcal A_F=-DS(\rho_F)/\log\varphi.}\tag{6}
\]

Thus (5), divided by `log phi`, gives an actual missing-code source bound,
including complete coherent retained failure memory. The classical relative-code component is exactly
`D_phi(w||w)=0`; this does not select a Book Cost/Info convention. The
coherent relative-code component generally has a nonzero and large value `H_phi(w)-S/log phi`; only its field derivative
is small. The whole flags+data+reference evolution is an isometry and has the
input entropy. It must not be conflated with the reduced archive entropy.

The value H_phi(w), actual attempt counts and all paid controller work remain
in the prospective comparison of different programmes or caps. Their zero
compact-field derivative holds at fixed m,N; it is not permission to erase
nonzero costs when D_min compares alternatives with different clocks.

For the already-owned cap `m_h=floor(tau/h^2)`, `N_h=ceil(2m_h/g)`,
`epsilon_h<=exp(-m_h/4)`. On a bounded compact field chart, (5)--(6) imply

\[
h^{-2}\|D\mathcal A_{F,h}\|_*
\le O\!\left(h^{-2} B_h\varepsilon_h
                     \log((r-1)/\varepsilon_h)\right)\longrightarrow0,
\]

whenever `B_h` and the actual carrier rank grow at most polynomially in
`1/h` (fixed CAR16 gives r<=256). The actual `m_h,N_h` are held fixed in each
field derivative. If the physical price uses this specified relative-code component, this
removes its quantitative *hidden flag coherence first-source* premise for
this compact protocol. It does not remove the
final Golden17 readout's own field-dependent source, the full128 source,
coframe-dependent native implementation/preparation/work/clock cost, or the
physical choice of Info algebra. Those retain their original owners.

For a raw l1 source over O(h^-4) actual site terms with a common polynomial
bound B_h, followed by the stated h^-2 normalization, the conservative
estimate is O(h^-6 B_h epsilon_h log((r-1)/epsilon_h)), which still vanishes
under the exponential cap estimate. More generally sum the actual local
B_(x,h) and cap/rank bounds before normalizing. A local site bound alone
cannot be substituted into a global norm without the declared locality or
bounded-overlap map and source convention.

## 5. Hostile control: no C2 entropy or smooth squared-ideal theorem follows

Use the actual full CAR16 Choi vector `Omega_16` and the original compact
rotation `V(theta)=Lambda(exp(theta J23))`. Its exact overlap is

\[
\langle\Omega_{16}|(V(\theta)\otimes I)|\Omega_{16}\rangle
=\operatorname{Tr}V(\theta)/16
=\cos^2(\theta/2).
\]

For `m=1` and any finite cap N, all successful branches implement this same
V, while the one all-B cap branch is identity, with `epsilon=p^N>0`.
The two nonzero archive eigenvalues satisfy

\[
\lambda_-=\frac{1-\sqrt{1-4\varepsilon(1-\varepsilon)
                            [1-\cos^4(\theta/2)]}}2
=\frac{\varepsilon(1-\varepsilon)}2\theta^2+O(\theta^4).
\]

Consequently `S=-lambda_- log lambda_-+O(lambda_-)` is C1 at theta=0,
with zero first derivative, but its second derivative diverges to +infinity.
The coherent relative-code second derivative diverges to -infinity. Taking
N=6 already places epsilon=p^6 below exp(-2), so this occurs inside the
source bound's regime. Exponentially small cap probability does not make a
finite-h entropy Hessian exist. Use the proved C1/refinement source bound;
an exact smooth coframe dressing or C2 argument requires its own physical
regularity premise or a different genuinely selected action.

At any common-output point the complete flag density is pure, so its entropy
is zero and this relative-code component equals H_phi(w). Since entropy is
nonnegative everywhere, that point is a maximum of the component, not a
local minimum. Adding this component cannot stabilize a separately descending
price direction through the *same* common-output point, even when the entropy
Hessian does not exist. This observation is conditional on one actual common
carrier/variation and price; it does not identify the compact Julia flag
component with the distinct whole-Lorentz HJR collar system.


## 6. Consumed inputs and validation boundary

Input commit: `07f2f2b15b7050a612d0075aa73db8dc46087a95`.

- `sources/d0_relational_coherent_synthesis_2026-10-20/coherent_execution.md`,
  SHA256 `14f9b909779146eeff099029039d15137eea3761e9972b31ef63cfeec9ab8287`:
  actual scalar-failure instrument, full leaf words, native code, cap and jets.
- Its `check_coherent_execution.py`, SHA256
  `f6f17ab63227b64074bcddeeea68d2dfd6059f05e593cbc1200b3dcd7eba7fd6`:
  original CAR16 exterior matrices and native finite all-word controls.
- `A4D_PHYSICAL_FULL_HISTORY_COHERENCE_SOURCE_AND_BINARY_COMPRESSION_GATE_2026_10_19.md`,
  SHA256 `87e44b774107e714c3cc6f1cc0419bf9e78028f56117ed0a0d4b75da2244c0fd`:
  full-code/coherent-source distinction. Its literal full128 source is not
  replaced by this different compact Julia calculation.

`check_flag_source.py` checks the exact native complete stopped leaf code,
the all-grade CAR16 Choi charge decomposition, full-leaf coherent Gram
regrouping, the analytic entropy covector in the three-dimensional actual
J23 Choi sector, all cap failure prefixes, the source bound and the actual
CAR16 nonsmooth second-jet control. The general bound above is analytic;
finite examples do not establish physical Book selection, uniform full
noncompact source or new GR closure.
