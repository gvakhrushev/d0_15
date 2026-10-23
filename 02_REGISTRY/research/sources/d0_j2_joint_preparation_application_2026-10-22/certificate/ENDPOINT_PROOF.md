# Exact nonflat all42 endpoint of the literal addressed feedback

22 October 2026. Supporting certificate in the existing task
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #334.
Source snapshot: `af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b`.
`GR_closed=false`.

## Result

**Для исходных 42 независимых полевых переменных найден и строго
сертифицирован новый точный неплоский стационарный корень действительного
двухадресного feedback (J_2).** Он сохраняет положительную ориентацию и
две независимые ненулевые материальные производные. Полная полевая матрица
Гессе невырождена и имеет оба знака. Это применённый сертификат нового
операторного источника; существование этого конечного корня больше не
зависит от предположения о малом остатке при старом CQ-корне или от
эйлеровой характеристики пространства подготовки.

The operator/source identification and the distinction from the old CQ
price are in [the same-packet source comparison](../source/SOURCE_COMPARISON.md).
For its two original report addresses, set

\[
 J_2(z)=-528\sum_{j=0}^1\log(1-r_j(z)).
\]

Here each (r_j=\zeta(A_j+B_j)-\zeta^2A_jB_j), so

\[
 -\log(1-r_j)
 =-\log(1-\zeta A_j)-\log(1-\zeta B_j).
\]

The calculation retains both addresses and all six original Lorentz
faces, the 16 independent coframe components, 24 independent link
coordinates, and two real CAR fields. The two-cell collar and fixed

\[
 h=0.183801524658179446663931692878752644250497528167344843803260291378571211
\]

are unchanged. It does not compress the two addresses to one arithmetic
mean, and it does not add the old measured-CQ price to (J_2).

Let (z_c) be the exact rational-decimal vector in
[J2_CENTER_HIGH_PRECISION.json](J2_CENTER_HIGH_PRECISION.json). There is a
unique real (z_\star) in

\[
 \|z-z_c\|_\infty\le10^{-30}
\]

such that **all 42 components of (dJ_2(z_\star)) vanish**. On this ball,
the Hessian of the literal (J_2) has inertia

\[
 (n_-,n_0,n_+)=(26,0,16).
\]

This establishes a saddle, not a full-field minimum. The new center is
about (8.6411107402\times10^{-7}) from the previously certified unpadded
CQ center. The [new existence receipt](J2_INTERVAL_RESULT.json) and
[full-inertia receipt](J2_INERTIA_RESULT.json) contain the outward bounds.

## 1. One unchanged field model and one fixed comparison normalization

The original mathematical field/report map is loaded directly from
`d0_full42_interval_banach_2026-10-22/certified_model.py`, Git blob
`6d5b41ce11a941fde95e722e708ebb02d689985c`; its exact collar/input loader is
Git blob `2c12d84fb3454dbf3cda6d71852d0cd4e57e1f65`.
Both blobs are checked before the certificate. The portable repository
loader uses these existing owners; the isolated scratch fallback, when
present, contains byte-identical originals under explicit local aliases.

For comparison with the old normalized field source, the checker uses

\[
 \bar S_J=a_JJ_2+\mathrm{constant},\qquad
 a_J=\frac{\nu[h'_\varphi(r_{\rm ref})-1](1-r_{\rm ref})}{528}
 =-1904017.766584186086\ldots\ne0.
\]

Here (\nu) and (r_{\rm ref}) are the original model constants. This is
the fixed, derived null-source comparison gain. It is independent of all
42 fields. Its sign reverses Hessian inertia but does not change the
stationary equations. Subtracting the constant at (r_{\rm ref}) only
improves the analytic bound; it contributes no source.

The first-point residual at the old CQ root is nonzero; the source note
computes it. Numerical continuation generated the new candidate, then
high-precision refinement proposed the rational center. Neither numerical
step is assumed exact in the proof below.

## 2. Verified holomorphic domain and exponential remainder

At the **new** center the checker evaluates the complete scalar on the
42-dimensional complex rectangular box with real and imaginary radii

\[
 R=5\times10^{-5}.
\]

This box contains the complex polydisc of radius (R). Outward interval
arithmetic proves

\[
 |\bar S_J|<2.965<5=:M,\qquad
 10^{-6}<\Re r_j<10^{-5},\qquad |r_j|<10^{-5}.
\]

The inverses used by the model are defined on this box. The logarithms
therefore stay on one analytic branch. The extension is the holomorphic
extension of the **real** field formula: the original Lorentz inverse is

\[
 U^{-1}=\eta U^{T}\eta,
\]

and coframe/matter contractions use ordinary transpose. The calculation
does not introduce complex conjugation of variable coordinates. Physical
adjoints agree with the specified real field formula on the real chart;
their literal antiholomorphic extension would not support this Cauchy
argument and is not what the checker evaluates.

Every original link exponential uses the unchanged interval algorithm:
for (\|X\|_\infty<1), expand (e^{X/2048}) through degree 30, add the
outward rectangular tail (10^{-120}) to each entry, and perform 11
interval squarings. The tail follows from

\[
 \frac{e^{1/2048}}{31!\,2048^{31}}
 <\frac{2}{31!\,2048^{31}}<10^{-120}.
\]

The last inequality is checked by integer arithmetic. The local wrapper
rechecks the generator norm and the integer tail predicate with explicit
exceptions, including when Python optimization is enabled; it does not
alter the original matrix calculation.

## 3. All 42 derivatives and all 1,764 Hessian entries

For the complete scalar, outward complex-step differences use

\[
 \delta_F=10^{-40},\qquad\delta_H=10^{-19}.
\]

The first-derivative remainder is at most (2M\delta_F^2/R^3).
The diagonal and mixed second-derivative remainders are at most

\[
 4M\delta_H^2/R^4.
\]

For example, the mixed formula is

\[
 H_{ij}= -\frac{\Re\bar S_J(z_c+i\delta_H e_i+i\delta_H e_j)
 -\Re\bar S_J(z_c+i\delta_H e_i-i\delta_H e_j)}{2\delta_H^2}
 +\varepsilon_{ij}.
\]

The Cauchy coefficient bounds on the polydisc give the stated uniform
bound on (\varepsilon_{ij}). No floating Hessian eigenvalue is used as
an invertibility premise. All symmetric Hessian entries are stored as
exact binary interval endpoints in
[J2_INTERVAL_HESSIAN_ENDPOINTS.json](J2_INTERVAL_HESSIAN_ENDPOINTS.json).
The full expensive interval calculation was executed successfully; its
receipt reports 1,764 outward entries.

On the real half-radius box, the same holomorphic bound gives

\[
 \|D^2\bar S_J(z)-D^2\bar S_J(z_c)\|_\infty
 \le C\|z-z_c\|_\infty,
 \quad C=42^2\frac{48M}{R^3}=3.38688\times10^{18}.
\]

This conservative bound is sufficient at the new tiny verification
ball. No bound on the whole numerical continuation path is assumed.

## 4. Actual strict Banach inequalities

The saved [rational preconditioner](J2_RATIONAL_PRECONDITIONER.json) is an
arbitrary proposed matrix (A). Every entry is an exact decimal rational;
its numerical origin is not part of the proof. The outward calculation
gives

\[
 \begin{aligned}
 \|A\|_\infty&<29.975703,\\
 \|I-A D^2\bar S_J(z_c)\|_\infty&<0.000143094689,\\
 \|d\bar S_J(z_c)\|_\infty&<8.011\times10^{-67},\\
 \|A d\bar S_J(z_c)\|_\infty&<2.402\times10^{-65}.
 \end{aligned}
\]

For (r=10^{-30}), the map (T(z)=z-A d\bar S_J(z)) has Lipschitz
constant

\[
 q\le\|I-A D^2\bar S_J(z_c)\|_\infty+\|A\|_\infty Cr
 <0.000143094791<1.
\]

Its center drift is strictly less than ((1-q)r). Thus (T) maps the
closed ball strictly into itself and is a contraction. The near-inverse
inequality also proves (A) invertible, so its unique fixed point is a
zero of the complete original-coordinate gradient. The nonzero fixed
gain then gives (dJ_2=0).

The actual geometric quantities are evaluated with intervals over this
**new** ball, rather than borrowed from the old center:

| Quantity | Certified strict lower bound |
|---|---:|
| Oriented coframe determinant | (1.5256645603) |
| Based spatial holonomy entry (P_{12}) | (0.0020210174) |
| First scalar temporal derivative | (0.0881179660) |
| Second scalar spatial derivative | (0.1461251182) |

The identity holonomy has this off-diagonal entry zero, so the first
curvature witness is explicitly nonflat. The two nonzero derivatives
occupy independent time/spatial directions.

## 5. Full rigorous saddle split

Let (Q) be the saved
[exact rational congruence frame](J2_RATIONAL_CONGRUENCE_FRAME.json).
The checker proves

\[
 \|I-Q^TQ\|_\infty<7.100\times10^{-15}<1,
\]

so (Q) is invertible. For the true interval Hessian, every row of

\[
 B=Q^T D^2\bar S_J(z_c)Q
\]

is strictly diagonally dominant, and the minimum absolute diagonal
minus off-diagonal row sum exceeds (0.04308485262). Exactly 16 diagonal
entries are negative and 26 positive. Turning off the off-diagonal
entries preserves the strict signed dominance, so no eigenvalue can
cross zero. Sylvester's congruence law therefore gives inertia

\[
 \operatorname{inertia}(D^2\bar S_J)=(16,0,26).
\]

The bound (\|Q^T\|_\infty\|Q\|_\infty Cr<4.232\times10^{-11})
preserves signed dominance over the whole root ball. Because (a_J<0),
the literal (J_2) has the reversed inertia ((26,0,16)) there.

## 6. Reproduction and scope

Python 3 and `mpmath` 1.3.0 suffice for the published checks; NumPy is not
needed when replaying the frozen rational matrices. From this directory:

```bash
python3 check_feedback_interval42.py --audit
python3 check_feedback_inertia.py --audit
```

Both are read-only by default and also run with `python3 -O`. They
recompute the saved matrix/ball inequalities and the geometric witnesses;
the first audit explicitly reports that it does not repeat the costly
Hessian evaluation. For a fresh full evaluation, use new output paths:

```bash
python3 check_feedback_interval42.py --recompute --workers 8 \
  --output /tmp/j2_replay_result.json \
  --matrix-output /tmp/j2_replay_hessian.json
python3 check_feedback_inertia.py --recompute \
  --output /tmp/j2_replay_inertia.json
```

The full-inertia command always consumes the frozen interval Hessian in
this packet; its ordinary audit verifies that matrix's SHA256. It is not
advertised as independently rebuilding all second derivatives.

The proved endpoint concerns the explicitly identified addressed
feedback field action. The independently prepared Born-score section
and the rank-two determinant have different preparation dependence;
their Hessian blocks must not be conflated. This certificate makes no
claim of a 50-equation full-Book stationary point, a selected field
writer, or a continuum limit. The actual heat, information, retained
reference, clock/work payments and independently admitted preparation
variations must be composed on the same execution. Their complete source
comparison is the remaining physical input, stated in the sibling
source note. `GR_closed=false`.
