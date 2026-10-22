# D0 → GR: exact Golden two-aperture source projector, positive-mixture no-go, and paid-sign gate

22 October 2026 · Mathematical research continuation of the EXISTING scientific Draft PR #334
(\`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`).
Status **ANALYTICAL CONSTITUTIVE THEOREM, NOT SELECTED D0 PHYSICS**.
\`GR_closed=false\`, \`full_Book03_HJR_selected=false\`, \`raw216_closed=false\`.

**Exact reused owners, not new assumptions or a new field action:**
- \`A4D_UNPADDED_GOLDEN_N1_CONSTITUTIVE_LEGENDRE_COMPLETE_2026_10_22.md\`:
  unchanged original Golden 0/10 report polynomial, nonlinear Cost-minus-measured-Shannon, positive definite open-chart constitutive Hessian and true moving-PF derivative;
- \`A4D_GOLDEN_SCALE_CONSTITUTIVE_NO_GO_AND_NATIVE_H2_APERTURE_2026_10_22.md\`:
  exact fixed-aperture physical-scale obstruction and **conditional** \`tau_h=O(h^2)\` scalar escape;
- \`A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md\`:
  existing **conditional** native metric-only/Golden-weight-zero/Ward Einstein-rigidity theorem;
- \`A4D_BOOK03_ALL42_SOURCE_DESCENT_AND_COHERENT_SADDLE_SYNTHESIS_2026_10_22.md\`:
  actual Book/Jones same-carrier admission, absolute Info and independent-input gate.

## 1. One actual local measured-code function, not a modified model

Let \(\varphi=(1+\sqrt5)/2\), \(p=\varphi^{-1}\), \(\sigma=p^2=1-p\),
\(\zeta=2^{-20}\), and let \(c(x,y)\) be the EXACT original normalized
0/10 Cost-minus-measured-Shannon function:
\[
\begin{split}
E&=p^2(1+x),\quad L=4E(1-E),\\
b&=p-p^2y,\quad B=4b^2(1-b^2),\quad A=L+(1-L)B,\\
r(x,y)&=1-(1-\zeta A)(1-\zeta B),\\
h_\varphi(r)&=-[r\ln r+(1-r)\ln(1-r)]/\ln\varphi,\\
c(x,y)&=r(x,y)-h_\varphi(r(x,y))
        -[r(0,0)-h_\varphi(r(0,0))].
\end{split}\tag{1}
\]
Thus \(c(0,0)=0\). The REAL original interval owner certifies positive
definiteness of \(D^2c\) for \(|x|,|y|\le0.01\), and in particular
\(c_{xx}>m=1.0788\,10^{-6}\),
\(\lambda_{\min}(D^2c)>4.48\,10^{-7}\) throughout this square.

For a finite original 42-field chart \(Y\), the ACTUAL geometry/matter
operands \(\xi_i(Y)=(f_{B,i}(Y),q_i(Y))\), and the TRUE possibly moving
positive PF site weights \(\rho_i(Y)\), consider the existing normalized
measured-CQ **mathematical family**
\[
S_t(Y)=\frac Kt\sum_i \rho_i(Y)
       c\!\left(\frac{t\xi_i(Y)}{\rho_i(Y)}\right),
\quad t>0,\quad K>0.\tag{2}
\]
For the original fixed \(t=\tau=1/20\), this is the old configured N1
action. For GENERAL \(t\), this is an ANALYTICAL APERTURE FAMILY,
**not** a claim that the same native full128/Book03 machine can physically
prepare all scaled operands. The \(K/t\) normalization is the old
source-normalized continuation, not a newly admitted price or coupling.
All conclusions below concern (2), *not* a new compulsory physical action.

Set \(\alpha=Dc(0)\), \(H=D^2c(0)\), and the source limit
\[
S_0(Y)=K\sum_i\alpha\cdot\xi_i(Y).\tag{3}
\]
This is exactly the original affine six-based-plaquette Palatini/CAR
source, with the already derived ratio
\(\alpha_y/\alpha_x=\lambda_-(2^{-20})\).
Its mathematical \`DS_0\` is not an assertion of independent physical
Book03 selection or universal metric descent.

## 2. THEOREM A — exact two-Golden-scale first-source cancellation, ALL field/PF directions

Assume \(Y\) lies in a compact smooth original field chart, every
\(\rho_i\ge\rho_*>0\), \(\xi_i,\rho_i\in C^1\), and
\(\|t\xi_i/\rho_i\|_\infty<0.01\) for \(0\le t\le\tau\).
The existing \(c\) is analytic on this real square and in particular
has \(N_3=\sup\|D^3c\|_{\rm op}<\infty\) on its compact interior.
For every physical 42-direction \(v\), including those changing original
coframe, proper Lorentz links, both CAR scalar coordinates, and original
PF densities, the EXACT differential is
\[
D_vS_t=K\sum_i\left[
 Dc(v_i)\cdot D_v\xi_i+
 \frac{c(v_i)-v_i\cdot Dc(v_i)}{t}D_v\rho_i
\right],\qquad
v_i=\frac{t\xi_i}{\rho_i}.\tag{4}
\]
Put
\[
\begin{split}
A_1[v]=K\sum_i\Big[
  \frac{(H\xi_i)\cdot D_v\xi_i}{\rho_i}
 -\frac{\xi_i^TH\xi_i}{2\rho_i^2}D_v\rho_i
\Big],\qquad
W[v]=K N_3\sum_i\Big[
 \frac{\|\xi_i\|^2\|D_v\xi_i\|}{2\rho_i^2}
+\frac{\|\xi_i\|^3|D_v\rho_i|}{3\rho_i^3}
\Big].
\end{split}\tag{5}
\]
Then the complete off-shell first-source expansion, *without freezing*
the moving PF density, satisfies
\[
\boxed{\quad
|D_vS_t-D_vS_0-tA_1[v]|\le t^2W[v].
\quad}\tag{6}
\]

**Proof:** \(Dc(z)=\alpha+Hz+R(z)\) with
\(\|R(z)\|\le N_3\|z\|^2/2\).
The exact perspective identity
\[
c(z)-z\cdot Dc(z)=-\int_0^1 s\,z^TD^2c(sz)z\,ds
\]
gives
\[
\left|c(z)-z\cdot Dc(z)+\frac12z^THz\right|
 \le N_3\|z\|^3/3.
\]
Substitute in (4) to obtain (5)–(6) for EACH v, not just null or
stationary directions. No Euler equation was assumed.

Now introduce the \(\varphi\)-fixed *algebraic* source transform
\[
\boxed{\quad
(\mathcal R_\varphi S)_t
=\frac{S_{\sigma t}-\sigma S_t}{1-\sigma}
=\varphi S_{\varphi^{-2}t}-pS_t.
\quad}\tag{7}
\]
Because \(1-\sigma=p\), (7) is exact native Golden arithmetic.
It preserves \(S_0\), and annihilates EVERY term linear in t:
\[
D(\mathcal R_\varphi S)_t=DS_0+O(t^2)
\quad\text{in the COMPLETE original 42-field source.}\tag{8}
\]
The weights \((\varphi,-p)\) are UNIQUE among all real normalized
two-aperture combinations
\(w_1 S_{\sigma t}+w_2S_t\)
satisfying \(w_1+w_2=1\) and \(w_1\sigma+w_2=0\).
In particular \(w_2<0\) is **mathematically unavoidable**.

## 3. THEOREM B — iterated Golden finite-source projector, uniform C1 convergence

Define \(\mathcal R_\varphi^n\) by iteration on the t-index, with t
and \(Y\) held to the SAME original field chart and original source
normalization K. The exact formula is
\[
\boxed{
(\mathcal R_\varphi^n S)_t=
\sum_{j=0}^{n}
 \binom nj\frac{(-\sigma)^{n-j}}{(1-\sigma)^n}
 S_{\sigma^j t}.
}\tag{9}
\]
Let \(B_t[v]=D_vS_t-D_vS_0-tA_1[v]\). For any remainder with
\(|B_t[v]|\le W[v]t^2\), the weighted \(t^2\)-norm obeys
\[
\left\|\mathcal R_\varphi B\right\|_{t^2}
\le\gamma\,\|B\|_{t^2},\qquad
\gamma=\frac{\sigma^2+\sigma}{1-\sigma}
=\boxed{3p-1=0.85410196624968\ldots<1}.\tag{10}
\]
Indeed \(\mathcal R_\varphi\) evaluates the remainder at \(\sigma t\)
and t with absolute weights \(1/(1-\sigma)\), \(\sigma/(1-\sigma)\),
hence \(\gamma\) exactly. The constant in (3) is fixed by the
transform, while the \(tA_1\) term is killed at its first iteration.
Therefore, for every \(n\ge1\) and EVERY original direction v,
\[
\boxed{
\left|D_v(\mathcal R_\varphi^nS)_t-D_vS_0\right|
\le W[v]\,t^2\,\gamma^n.
}\tag{11}
\]
The same conclusion holds uniformly in an operator norm over all
42 original field directions when the bounds in (5) are uniform over
unit tangents. No native field direction, moving PF term or independent
matter derivative has been omitted.

**Analytic sharpening (optional, strictly typed):** if the common
same-field t-family has an absolutely and uniformly convergent Taylor
series \(DS_t=DS_0+tA_1+\sum_{k\ge2}t^kA_k\) on the chosen interval,
then the transform's EXACT eigenvalue on t^k is
\[
\lambda_k=\frac{\sigma^k-\sigma}{1-\sigma}
=-p(1-\sigma^{k-1}),\quad k\ge2,\qquad
|\lambda_k|<p.
\]
Thus
\[
\left\|D(\mathcal R_\varphi^nS)_t-DS_0\right\|
\le p^n\sum_{k\ge2}t^k\|A_k\|,\qquad n\ge1.\tag{12}
\]
This is not inferred merely from a real C3 bound: the displayed
uniform analytic-series hypothesis is necessary for (12).

The transform is a source projector only in the **limit of real
signed linear functionals**. It is not a projection by one physical
finite native operation, and no source-selection status is promoted.

## 4. THEOREM C — positive randomized Golden apertures CANNOT substitute for the signed gate

Let \(t_j>0\) lie inside the same certified chart and \(w_j\ge0\),
\(\sum_jw_j=1\), fixed independently of physical field Y.
For a finite mixture (or a convergent positive mixture with the
corresponding derivatives justified), set
\(S_{\rm mix}=\sum_j w_j S_{t_j}\).

Holding original PF weights fixed and differentiating with respect
to TWO genuine independent native operands \(\xi_i=(f_i,q_i)\) gives
\[
D^2_{\xi_i}S_{\rm mix}
=\frac K{\rho_i}
 \sum_jw_jt_j
 D^2c(t_j\xi_i/\rho_i)
\succ0,\tag{13}
\]
with the certified uniform lower eigenvalue
\[
D^2_{\xi_i}S_{\rm mix}
\succeq\frac{K(4.48\,10^{-7})}{\rho_i}
  \left(\sum_jw_jt_j\right)I_2.\tag{14}
\]
Thus positive randomization at any strictly positive mean aperture
retains nonlinear operand stiffness and can **NEVER equal the affine
Einstein–CAR source as a function of BOTH native operands on an open
chart**. This is an operand-level theorem, not an unproved claim that
arbitrary 42 physical tangent images are onto both operands.

There is also the stronger *physical constant-coframe-scaling control*
already used by the original Golden-scale owner. On genuine constant
matter (\(q_i=0\)), unchanged positive original PF weights and
\(e\mapsto\sqrt{s}e\), the actual original geometrical operand changes
\(f_i\mapsto s f_i\). For \(s=\varphi^2\) and
\(\{t_jf_i/\rho_i,st_jf_i/\rho_i\}\) inside the chart, the owner's strict
\(c_{xx}>m=1.0788\,10^{-6}\) yields
\[
\boxed{
S_{\rm mix}[\sqrt{s}e]-sS_{\rm mix}[e]
>\frac{Kms(s-1)}2\left(\sum_jw_jt_j\right)
 \sum_i\frac{f_i^2}{\rho_i}>0
}\tag{15}
\]
if at least one actual curvature operand is nonzero. Hence no fixed
field-independent positive random mixture of the declared bare measured
Golden prices repairs their exact Golden weight-one action gate.
This does not preclude a different genuinely selected full Book source,
a moving-field-dependent controller with its full source, or a
vanishing-aperture refinement limit.

## 5. The exact paid-sign/noise barrier — NOT a free physical extrapolation

The sum of the ACTUAL signed coefficients in (9) is 1, but their
absolute mass is
\[
\boxed{
\sum_{j=0}^n|w_{n,j}|=
\left(\frac{1+\sigma}{1-\sigma}\right)^n
=(\sqrt5)^n,\qquad
\sum_{j=0}^nw_{n,j}=1.
}\tag{16}
\]
This is an exact special Golden identity, not a cost model.
No valid expected primitive cost is allowed to replace the signed
coefficients \(w_{n,j}\) with unpaid negative edge lengths.

**Conditional elementary independent-readout resource lower bound.**
Suppose every \(S_{\sigma^j t}\) is estimated on genuinely independent
fresh histories, one sample of the j-th estimator has variance at
least \(v_*>0\), the n+1 experiments receive \(N_j\) independent
samples, and their estimator variances obey the usual
\(\ge v_*/N_j\) bound. With \(N=\sum_jN_j\), Cauchy–Schwarz gives
\[
\operatorname{Var}\widehat{\mathcal R_\varphi^nS}
\ge v_*\sum_j\frac{w_{n,j}^2}{N_j}
\ge \frac{v_*}{N}\left(\sum_j|w_{n,j}|\right)^2
=\boxed{\frac{v_*5^n}{N}}.\tag{17}
\]
This is NOT a universal coherent quantum lower bound. It applies
only under the stated independent, nonzero-noise estimator contract
and illustrates why mathematical source projection does not erase
physical work/clock/sample costs. The smallest demanded scalar
aperture is \(\sigma^n t\); all intermediate executions and aborts
must be paid and their complete Info valued.

**Consequent exact new physical acceptance gate:**
A D0 physical application of (7)–(12) must derive, from ONE genuinely
admitted common initial state and paid original Book03/H+J+R/Cost−Info
operator stack, either (i) this whole signed source contrast with ALL
of its genuine branch Info, oldRIGHT, clock, preparation, controller and
work, or (ii) an independently established source-equivalent
stationary/constraint law. It must supply the actual compiled
\(t\mapsto\sigma t\) native QUERY—not merely classical Golden prefix
probability; the old result proves rare-prefix thinning and
\(r(\sigma t\xi)\) are generally different nonlinear functions.
A post hoc negative counterterm or an unsigned averaged score is
**not** permitted.

Even successful selection of this gate would yield at first an
affine finite Einstein–CAR source on its stated field chart. The
real all-metric Diff naturality, off-shell Ward, metric-only descent,
physical source normalization, common physical refinement and
universal recovery premises of the already-owned Golden-rigidity
theorem would still require proof. This packet neither changes
\`positive_gr\` nor accepts the original \`raw216\` terminal.

## 6. Bounded reproducibility and actual check scope

Checker:
\`sources/d0_golden_source_projection_2026-10-22/check_golden_source_projection.py\`.

A locally executed 100-digit mpmath test (NOT an all42 physical/root
proof) checks:
- exact Golden coefficient identities, binomial eigensystem and
  \(\sqrt5^n\) total variation for n up to 10;
- direct differentiation of the original nonlinear c with f,q AND
  nonzero \(D\rho\), matching the perspective source formula;
- the actual two-scale iterated source error, for nonzero source
  gradients and moving PF;
- strict positive-mixture scalar-curvature second derivative.

For the illustrative single-cell parameterized direction
\(f=0.2,q=-0.1,\rho=1.3,Df=0.7,Dq=-0.4,D\rho=0.15,t=0.05\)
with \(K=1\), the measured gradient errors versus the TRUE
affine first source were:
\[
n=0:\ 9.2542539010\,10^{-8},\qquad
n=1:\ 1.5201875152\,10^{-10},\qquad
n=10:\ -2.1246797692\,10^{-14}.
\]
The algebraic proof is (4)–(17), not the numerical sample. Historic
Golden/42/Lean/assembly suites were NOT rerun; no original receipts,
physical model files or acceptance flags are changed.

**Result summary:** exact conditional all42 first-source projector +
uniform moving-PF C1 error control + complete positive-mean no-go +
exact signed-readout amplification/price barrier. This removes the
algebraic "how could a native Golden nonlinear constitutive response
converge to affine Einstein/CAR without a fitted coupling?" problem
*within a precisely defined mathematical aperture family*. It
DOES NOT remove the compulsory native Book physical selection,
same-programme writer, Diff/Ward, or refinement premises.
