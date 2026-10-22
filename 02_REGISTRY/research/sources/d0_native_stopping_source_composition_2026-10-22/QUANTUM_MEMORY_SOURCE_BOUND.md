# Actual native quantum-memory source: finite-window and stopped-tree bounds

22 October 2026. Application to the unchanged CAR16/full128 native instrument,
with its actual inverse-Delta preparation. No reset, fitted Markov model, new
physical tariff, or paid memory rotation is introduced. `GR_closed=false`.

## 1. What this consumes and what it adds

The existing owner
[A4D_NATIVE_FULL128_STOPPED_KL_QUANTUM_MEMORY_BUDGET_2026_10_22.md](https://github.com/gvakhrushev/d0_15/blob/5e3f639b447c367b46b05673731dba0931e8edfe/02_REGISTRY/research/A4D_NATIVE_FULL128_STOPPED_KL_QUANTUM_MEMORY_BUDGET_2026_10_22.md)
already proves the actual first-return occupation, stopped measured KL source,
quantum-capacity value bound, and independent-preparation defect. It explicitly
does not turn a small entropy tail VALUE into a derivative bound.

The earlier literal-price reduction already gives, on the same execution,

\[
 P_{{\rm port},K}=\mathbb E[N_b+2N_o+p^3N_{\rm pair}]
 -\frac{S(\Gamma_{M,K})-S(\rho)}{\ell},\qquad
 p=\phi^{-1},\quad\ell=\ln\phi.                                      \tag{1}
\]

Here merged words retain blank and orphan separately: 65 physical labels,
33 live at the actual fixture. This note adds a **quantitative first-source
bound** on the remaining conditional quantum term, with constants computed on
the same original noncommuting matrices. It also gives an exact finite-tree
tangent telescope and consumes the owned first-return occupation to make the
stopped source bound independent of the cap.

The general coordinate equivalence by phase and memory conjugation, its
Poisson equation, and linear Fisher-information growth belong to existing
quantum Markov theory; see [Guta–Kiukas, arXiv:1402.3535](https://arxiv.org/html/1402.3535v1).
The identification of efficient-measurement entropy reduction with the
initial-reference Holevo information is also standard; see
[Buscemi–Das–Wilde, arXiv:1601.01207, Section IV](https://arxiv.org/html/1601.01207v3).
Those general facts, the entropy chain rule, and stationary block
superadditivity are not claimed as new results here.

## 2. The boundary whose derivative must be controlled

Let an efficient complete instrument have one Kraus operator per full recorded
leaf, including all cap-abort leaves. For an initial DATA state rho, choose an
amplitude C with CC*=rho. A leaf w has amplitude A_w=K_w C, weight p_w, and
conditional DATA state sigma_w=A_w A_w*/p_w. Put

\[
 R_{\mathcal T}=\sum_w p_w S(\sigma_w),\qquad
 \chi_{\mathcal T}=S(\rho)-R_{\mathcal T}.                       \tag{2}
\]

Purifying rho by an **initial reference**, each conditional DATA-reference leaf
is pure. The reference marginal is unchanged by the complete instrument.
Therefore chi is the Holevo information between the record and that initial
reference, and

\[
 0\le\chi_{\mathcal T}\le S(\rho)\le\ln16,\qquad
 S(\Gamma_{\mathcal T})-S(\rho)=H(W)-\chi_{\mathcal T}.          \tag{3}
\]

This statement does not require the stopped final DATA marginal to equal rho.
For a fixed window with stationary input it also equals the Holevo information
between the record and final DATA. The initial-reference definition works for
both cases without that extra assumption.

For the fixed-window merged native record, (1) becomes

\[
 P_{{\rm port},K}
 =\mathbb E C_{{\rm eff},K}-\frac{H_{M,K}}\ell
    +\frac{\chi_K}\ell.                                      \tag{4}
\]

The positive value bound chi<=ln16 alone says nothing about D chi. The following
argument supplies the missing derivative control.

## 3. Dimension-only conditional-entropy derivative bound

On any differentiable amplitude chart, the log p_w terms cancel exactly:

\[
 DR_{\mathcal T}
 =-2\operatorname{Re}\sum_w
   \operatorname{Tr}[\dot A_w^*\log(\sigma_w)A_w].               \tag{5}
\]

All zero modes are interpreted by the continuous amplitude expression
`s log(s^2)->0`. A zero-probability leaf contributes zero first derivative.
Thus this argument does not discard dark modes or require an artificial
positive eigenvalue cutoff. A faithful differentiable initial rho and smooth
Kraus matrices suffice for the amplitude chart; arbitrary boundary density
directions without a differentiable amplitude are not silently included.

For every density matrix on dimension 16,

\[
 \operatorname{Tr}\sigma(\log\sigma)^2\le (\ln16)^2.            \tag{6}
\]

One elementary proof maximizes sum lambda(log lambda)^2 on the probability
simplex. A boundary point cannot maximize when a zero coordinate can be
populated, since epsilon(log epsilon)^2 dominates its linear cost. At an
interior critical point, unequal eigenvalues a,b must obey ab=e^-2. A maximum
can have only one eigenvalue above e^-1, because the scalar second derivative
there is positive. Thus an unequal maximum would require
a+15b=1 and ab=e^-2, impossible by AM-GM. The uniform state is the maximum.

Cauchy-Schwarz in (5), followed by (6), gives the exact inequality

\[
 \boxed{|DR_{\mathcal T}|\le
  2\ln16\left(\sum_w\|\dot A_w\|_2^2\right)^{1/2}.}            \tag{7}
\]

The constant is independent of the number of recorded words. In particular,
there is no factor 64^K, 33^K, or 128 from the independent oldRIGHT spectator.

## 4. Native Poisson normalization, including the moving preparation

At a faithful stationary base point rho of the primitive DATA channel Phi,
write

\[
 \beta=\sum_z K_z^*\dot K_z,\quad b=-i\beta=b^*,\quad
 a=\operatorname{Tr}(\rho b),\quad
 (I-\Phi^*)X=b-aI,\quad\operatorname{Tr}(\rho X)=0.             \tag{8}
\]

Differentiated completeness makes beta anti-Hermitian; the centered Poisson
equation is solvable on the owned primitive chart. Define

\[
 \dot K_z^{\rm h}=\dot K_z+i[X,K_z]-iaK_z,\quad
 E_{\rm h}=\sum_z(\dot K_z^{\rm h})^*\dot K_z^{\rm h},\quad
 \kappa=\operatorname{Tr}(\rho E_{\rm h}).                      \tag{9}
\]

Then sum K_z* dot K_z^h=0 as an operator, not merely after taking its expectation.
This is essential to the norm telescope.

The local mathematical family
`K_z(t)->exp(itX) exp(-iat) K_z(t) exp(-itX)` and
`rho(t)->exp(itX) rho(t) exp(-itX)` leaves each outcome probability and every
CQ entropy unchanged. A stopped word acquires a phase depending on its own
length, which still cancels in its recorded quantum block. This is a change
of coordinates for estimating the derivative, not a physically executed
memory rotation or a waived work charge.

The input derivative is transformed too:

\[
 \dot\rho_{\rm h}=\dot\rho+i[X,\rho],\quad
 \rho L+L\rho=2\dot\rho_{\rm h},\quad
 C=\sqrt\rho,\quad \dot C_{\rm h}=\tfrac12LC,\quad
 u=\|\dot C_{\rm h}\|_2^2.                                    \tag{10}
\]

The last choice only fixes the purification's unitary freedom and minimizes
the initial amplitude norm. It does not freeze preparation. Any normalized
input tangent at this stationary base point can be used in (10), even one
which leaves the stationary family. For such a tangent the actual cost and
preparation-defect sources must still be differentiated before reducing them
to a stationary-section formula.

For every fixed K, chronological multiplication and the operator horizontal
condition give the **exact finite identity**

\[
 \boxed{\sum_{|w|=K}\|\dot A_w^{\rm h}\|_2^2=u+K\kappa.}       \tag{11}
\]

Indeed, replacing a live parent amplitude A by all children K_z A adds
Tr(A A* E_h) to its squared tangent norm; the cross term is zero by
sum K_z* dot K_z^h=0. Summing one entire level uses Phi^j(rho)=rho.

Combining (2), (7), and (11) proves

\[
 \boxed{\frac{|D\chi_K|}{K}
 \le\frac{|DS(\rho)|+2\ln16\sqrt{u+K\kappa}}{K}.}              \tag{12}
\]

This is a first-source estimate, not differentiation of the value bound in
(3). It tends to zero for each fixed admissible tangent. Parameter-independent
scalar refinements, including the actual Golden paired ports, preserve Phi,
beta, E_h and kappa, so the same estimate applies to fine and merged records.

The immediately usable constitutive comparison is

\[
 \left|D\frac{P_{{\rm port},K}}K-
 \left(\frac{D\mathbb E C_{{\rm eff},K}}K-
       \frac{DH_{M,K}}{K\ell}\right)\right|
 \le\frac{|DS(\rho)|+2\ln16\sqrt{u+K\kappa}}{K\ell}.           \tag{13}
\]

On a moving stationary family the first term inside parentheses is the
derivative of the one-tick effective cost. Its exact expression is
`1+4p^3 h-(2-p) 4p^2 h(1-mu)`, with
`h=16/Tr Delta^-1` and `mu=Tr Delta/16`.

Equation (13) eliminates the unknown conditional quantum source up to a
computed error. The remaining classical merged-history source DH_M,K must
still be evaluated by its actual filter. No assertion is made that this
source equals a one-shot source or a fitted classical Markov source.

## 5. Stronger bounded-stopping application

For any complete finite stopping tree, let X_w=A_w A_w* be the unnormalized
DATA block at a live prefix, including the empty prefix. The same parent-child
calculation telescopes exactly, now across a tree rather than a level:

\[
 \boxed{\sum_{w\ {\rm leaf}}\|\dot A_w^{\rm h}\|_2^2
   =u+\operatorname{Tr}\!\left[E_{\rm h}
                \sum_{w\ {\rm live}}X_w\right].}              \tag{14}
\]

This includes all fine outcomes and cap aborts. It does not assume that the
stop rule ignores the Golden port.

For the actual stationary first-return task with m coarse comparison labels,
let T_a be its mismatch CP map and sigma_a=(I-T_a)rho the anchor block. If the
number of later comparisons is capped at K, the existing occupation theorem
gives directly

\[
 \sum_{w\ {\rm live}}X_w
 =\rho+\sum_a\sum_{j=0}^{K-1}T_a^j\sigma_a
 =(m+1)\rho-\sum_a T_a^K\rho\preceq(m+1)\rho.                 \tag{15}
\]

Consequently every finite cap obeys the same source bound

\[
 \boxed{|D\chi_{{\rm stop},K}|
 \le |DS(\rho)|+2\ln16\sqrt{u+(m+1)\kappa}.}                  \tag{16}
\]

For the real binary-port comparison m=2. The complete finer archive is retained
throughout; no binary-pointer entropy replaces its complete CQ entropy.
If the actual stopping controller reads PORT, scalar port merging must be
handled separately. Equations (14)-(16) apply directly to the full fine tree
and do not use the invalid shortcut of merging away its stop predicate.

## 6. Actual unchanged native constants and decisive checks

The checker AST-loads only the required functions from these immutable inputs:

| Original input | Git blob |
|---|---|
| `d0_book_uniform_source_2026-10-21/check_uniform_book_source.py` | `ee8de4635d24c668949ac9a0186616ab7d59f2ed` |
| `d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py` | `c133c6aec28e2a4068b36a6d9646bc8fb04fc2a4` |

It uses the original `r=1/9`, `nu=3/5`, `theta=2 atanh(r)`,
`dtheta/dr=2/(1-r^2)`, phases `(i,i,-1,-i)`, all sixteen CAR grades,
and the generated `rho=Delta^-1/Tr Delta^-1`. The second direction is exactly
`v=partial_r+0.04408551592126523 partial_nu`, which keeps h constant to first
order. The two source coordinate units have not been identified with a unit
norm all42 geometric variation.

| Quantity | r direction | one-port-null v direction |
|---|---:|---:|
| kappa | 0.0023033168084690943 | 0.002299614349137185 |
| u, optimized initial amplitude norm squared | 0.03722069453649128 | 0.03722069453649129 |
| D S(rho), nats per coordinate | -0.015366667601082844 | -0.015366667601082802 |
| operator horizontal residual | 2.65e-16 | 2.57e-16 |
| stopped bound (16), nats per coordinate | 1.1802584600858133 | 1.1801118532581272 |

The non-horizontal beta Frobenius norm is 0.03620328880512053, so replacing the
actual tangent by an unproved horizontal one would be material. The centered
Poisson generator has Frobenius norm 1.13262573164554. Its superoperator solve
has condition number approximately 975.47.

For fixed windows the resulting numerical values of the right side of (12)
are:

| K | r bound, nats per coordinate per tick | v bound, same units |
|---:|---:|---:|
| 4096 | 0.004170212617377603 | 0.004166875758234655 |
| 1,000,000 | 0.0002661465686482541 | 0.0002659325902015270 |
| 100,000,000 | 0.00002661306098883534 | 0.00002659166297286413 |

For the Golden price source (13), divide these by ell=0.48121182505960347.
Thus the K=4096 price bounds are 0.00866606429894 and 0.00865913001560;
the K=100,000,000 bounds are 0.0000553042539749 and 0.0000552597870378.
These bounds do not certify a tiny all42 source cancellation or a source sign.

`check_memory_source_bound.py` passed 560 checks. It verifies the original
input hashes, normalization, actual Poisson condition, transformed preparation,
and preservation of all merged K1/K2 pointer and CQ entropy derivatives.
It directly builds the 33 and 1089 live merged words: their tangent norms
agree with (11) to better than 2e-16 in the displayed run. It separately
propagates full-fine first-return amplitude Gram jets at caps 1,2,8,64;
(14) agrees to better than 7e-17, and the occupation remainder in (15) is
positive. No old unrelated suite was rerun.

All displayed native constants and residuals are **ordinary double-precision
diagnostics, not outward interval certificates**. The inequalities and
telescopes (7), (11)-(16) are analytic. Inserting the displayed rounded
constants is a numerical evaluation of their right sides, not a certified
enclosure; an interval Poisson solve would be needed for that promotion.

Reproduce from a repository checkout with both canonical source folders:

```sh
OPENBLAS_NUM_THREADS=1 python check_memory_source_bound.py --json RESULT_MEMORY_SOURCE_BOUND.json
```

Alternatively pass `--input-dir /path/to/pinned-inputs` containing the two
original Python files. The checker has no implicit temporary-directory
dependency and writes a receipt only when `--json` is supplied.

## 7. Limits of the conclusion

For fixed windows, (12) proves `D chi_K / K -> 0`. Hence normalized complete-CQ
and classical pointer sources have the same limits **if either sequence of
sources converges**. It does not prove that the derivative of the entropy rate
exists, justify interchange of derivative and infinite-history limit, or bound
the distance to such a derivative. The finite-tree estimate (16) is likewise
not a claim of differentiability of an uncapped stopping limit.

The dimension16 numerical application covers the actual mixed DATA input and
an independent oldRIGHT spectator, whose entropy cancels in the gain. At a
faithful product base `Omega=rho tensor omega`, it also covers **ambient
correlation tangents**: the already-owned spectator cotangent result in
`d0_native_stationary_memory_composition_2026-10-22/SPECTATOR_POISSON.md`
shows that, for a complete spectator-blind instrument, all `log omega` terms
cancel between output and input entropy. The gain cotangent is `M_DATA tensor
I`, as is the pointer cotangent. Hence D chi depends only on
`D rho=Tr_RIGHT D Omega`; tangents with zero DATA marginal have zero chi
source at that product base. This argument does not require the varied state
to remain a product.

A genuinely nonproduct base requires its actual joint amplitude and an
appropriate source bound; it is not silently replaced by an independent
spectator. Independent preparation variations are permitted in (10)-(14) but
their cost, Poisson boundary, and other physical Euler rows are not removed by
this estimate.

The price under discussion remains the declared literal port component minus
full CQ input gain. Actual label tariffs, controller, preparation, elapsed
clock, factory and Book03 heat/information choices remain their real separate
contributions. This work supplies a quantitative same-instrument source
comparison, not a selection of the complete physical Book price or a proof
of `GR_closed`.
