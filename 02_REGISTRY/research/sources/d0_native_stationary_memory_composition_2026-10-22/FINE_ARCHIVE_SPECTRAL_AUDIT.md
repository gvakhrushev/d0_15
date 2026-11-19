# Independent audit: full native fine record versus the same finite age record

## Result and scope

**Approved, with a strict native one-round sign certificate.** On the original CAR16/Walsh/Julia/full128 instrument, the retained fine CQ information cannot be replaced by the age CQ information without changing the source. At the actual one-port-null tangent `v`, the one-round age entropy-gain source is negative and the full fine entropy-gain source is positive. Their difference is the positive conditional fine-record source.

This audit derives that conclusion independently from exact row spectra and rational interval arithmetic. It does not depend on clipping eigenvalues, a purity assumption for mixed DATA, replacing quantum entropy by pointer Shannon entropy, or a fitted information correction. The full K=2 comparison remains the independently grouped numerical computation from the companion source application. The all-K proportional-port refinement below is exact, but it does not determine the remaining merged-record source.

The physical Book03 information/cost selection, the paid preparation and other executor costs, and the full 42-field Euler closure remain open. `GR_closed = false`.

## Ownership and inputs

These parents are consumed as existing results, not claimed again:

- The original native constructor is `sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`, immutable Git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed`; its `native` definition starts at line 64.
- Existing `sources/d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py` already computes the original complete K=1,2 CQ entropies and both source directions. Its analytic joint jet starts at line 92, full-word CQ calculation at line 151, and all-label stationary row identity is explicitly checked at lines 314–322. Its SHA256 is `cd0052f10bc43abb3736a1637c850c2a3d637f428dd116f6320f68bcf84e3931`.
- Existing `sources/d0_original_full128_native_julia_reflection_2026-10-22/check_original_julia_exact_car_algebra.mjs`, blob `2f3310fd3b9eaf31d8ca86bb6f0718021930e662`, establishes the exact original CAR/boost/Julia algebra at this fixture.
- The fixed-algebra/oldRIGHT Fredholm theorem and raw terminal-CQ uniform-RIGHT result are already owned by `A4D_ORIGINAL_OLDRIGHT_ARCHIVE_FREDHOLM_INFORMATION_AND_TWO_STAGE_GATE_2026_10_22.md`. They are not new findings of this audit.

The new material is the exact eight-class row-spectrum reduction including the actual `v` jets, the same-one-round conditional-source formula, its rational interval sign certificate, and the audit of the exact all-K proportional-port refinement.

## Exact original fixture

Use

\[
p=\varphi^{-1},\quad t=2p^2=3-\sqrt5,\quad
r=\frac19,\quad \nu=\frac35,\quad \theta=\log\frac54,
\]

with CAR order `(0,2,3,1)` and phases `(i,i,-1,-i)`. The boost generator satisfies `G^3=G`, so

\[
U=I+\frac9{40}G+\frac1{40}G^2,
\qquad \frac{d\theta}{dr}=\frac{81}{40}.
\]

Let `A=N_0`, `Delta=A* A`, and `E_j=N_j* N_j` for the unchanged 64 Walsh/Julia row slots. The stationary mixed DATA input is

\[
\rho=\frac{\Delta^{-1}}Z,\qquad
Z=\operatorname{Tr}\Delta^{-1}=\frac{16}{h}.
\]

The exact scalar data are

\[
\mu=\frac{141489}{10240000},\quad
h=\frac{69399}{5030720},\quad
h_r=-\frac{20040939}{9885993640}.
\]

The actual tangent is

\[
v=\partial_r-\frac{\nu h_r}{2h}\,\partial_\nu,
\qquad d_vh=0,
\qquad d_v\mu=\frac{671335371}{1579212800000}>0.
\]

The audit checks `d_v h=0` from the exact original matrices, rather than assuming it only from the parameter label.

## Exact row-spectrum reduction

The native row identities give

\[
\sum_j E_j=I,\qquad \sum_jN_jN_j^*=I.
\]

The second identity also follows directly from the Julia pairs before the Walsh transform. The audit verifies both in exact arithmetic.

All 32 odd Walsh labels vanish by duplicate-word cancellation, including their first jets. The 32 live row slots form the following eight classes, with equality of the complete Gram spectral data **and of their `v` derivatives**:

| Row slots `j` | Multiplicity | Exact reduction |
|---|---:|---|
| 0, 4, 32, 36 | 4 | quadratic Gram polynomial |
| 8, 12, 40, 44 | 4 | quadratic Gram polynomial |
| 16, 20, 48, 52 | 4 | quadratic Gram polynomial |
| 24, 28, 56, 60 | 4 | quadratic Gram polynomial |
| 1, 5, 17, 21, 25, 33, 37, 41, 49, 53, 57 | 11 | scalar and two-mode Hermitian blocks |
| 9 | 1 | scalar and two-mode Hermitian blocks |
| 13, 45 | 2 | scalar and two-mode Hermitian blocks |
| 29, 61 | 2 | scalar and two-mode Hermitian blocks |

For every odd-operator row, the exact identity is

\[
(E_j-\mu_jI)^2=w_jI.
\]

The two eigenvalues `mu_j +/- sqrt(w_j)` each have multiplicity eight. Differentiating this matrix identity gives their full trace-functional first source; the audit verifies that differentiated identity as well.

Every even Julia row is Hermitian and preserves the occupations of spectator modes 2 and 3 and total occupation of modes 0 and 1. For each spectator configuration its remaining four-dimensional block splits as `1 + 2 + 1`. For the real symmetric two-dimensional block

\[
N=\begin{pmatrix}a&c\\c&d\end{pmatrix},
\quad z=\frac{a+d}{2},\quad
w=\left(\frac{a-d}{2}\right)^2+c^2,
\]

the Gram eigenvalues are `(z +/- sqrt(w))^2`. Their derivatives follow by scalar differentiation. At a degenerate block, the derivative of the trace entropy uses the trace of the block derivative, so no arbitrarily chosen eigenbasis is introduced.

All complex matrices and jets are in the field `Q(i,sqrt(24142))` at this fixture; the real root matrices, scalar spectral coefficients, and real block data lie in `Q(sqrt(24142))`. The boosted positive root is the polynomial interpolating the positive values `1`, `4/5`, and `sqrt(24142)/200` on the exact Gram spectrum `0`, `9/25`, `7929/20000`. The audit verifies the minimal polynomial, multiplicities, positive root values, root square, and differentiated root square.

Thus the calculation retains actual mixed quantum blocks, all zero modes, all fine-label multiplicities, and all derivatives. Exact zero modes contribute zero first entropy source; they are not removed by a numerical threshold.

## A same-one-round conditional-source formula

Write the actual sole blank as

\[
B=I-t\Delta.
\]

The existing stationary-block identity is

\[
X_{j,0}=\frac{t^2E_j}{Z}\quad(j\ne0),\qquad
X_{j,1}=\frac{u^2E_j}{Z}\quad(\text{all }j),
\qquad u^2=4p^3=2t-t^2.
\]

The ordinary blank is `B rho B`. Coarsening the actual record to age at K=1 retains that blank block and merges every other physical label into

\[
Q=\rho-B\rho B=\frac{t(2I-t\Delta)}Z.
\]

This is the actual CP grouping. There is no resetting of DATA and no replacement of a mixed block by its trace.

Let

\[
R_1=S(F_{\rm fine,1}(\rho))-S(F_{\rm age,1}(\rho))
=H(\text{fine}\mid\text{age,DATA}),
\quad
\mathcal A=\sum_j\operatorname{Tr}(E_j\log E_j).
\]

The blank terms cancel. Summing both ports with their proper multiplicities gives

\[
R_1=\frac1Z\left\{
\operatorname{Tr}[q\log q]-2t\mathcal A
+t^2\operatorname{Tr}(\Delta\log\Delta)
-t^2\log(t^2)\,[16-\operatorname{Tr}\Delta]
-16u^2\log(u^2)\right\},
\qquad q=t(2I-t\Delta).
\]

All `log Z` terms cancel because the fine nonblank mass equals `Tr Q`. Since `d_v Z=0`, differentiating yields the particularly compact exact source identity

\[
\boxed{
d_vR_1=
\frac{t^2}{Z}\operatorname{Tr}\!\left[
\log\!\left(\frac{t\Delta}{2I-t\Delta}\right)d_v\Delta
\right]
-\frac{2t}{Z}\,d_v\mathcal A.}
\]

This is a source formula for the unchanged original 128-output instrument. It is not a pointer-Shannon approximation. The eight exact spectral classes evaluate `d_v A` with all quantum multiplicities intact.

## Strict rational interval certificate

The executable audit is `check_fine_archive_spectral.py`; its receipt is `RESULT_FINE_ARCHIVE_SPECTRAL.json`. SymPy performs exact matrix/field identities. A separate evaluator uses only `fractions.Fraction` for every interval endpoint:

- arithmetic rounds outwards to 100-bit dyadic rationals;
- square roots use integer `isqrt` with explicit lower and upper endpoints;
- logarithms reduce the argument to `[1,2]`, then use the positive atanh series with 34 terms and the explicit geometric remainder;
- the printed 75-digit mpmath values are an independent display check, not the basis of the inequalities.

The resulting strict enclosures include

\[
\begin{aligned}
d_vR_1&\in
(0.0050296565882099257579220245,
\ 0.0050296565882099257579220345),\\
d_v I_{\rm age,1}&\in
(-0.0003390988816519018581384328,
\ -0.0003390988816519018581384200),\\
d_v I_{\rm fine,1}&\in
(0.0046905577065580238997835917,
\ 0.0046905577065580238997836144).
\end{aligned}
\]

The exact rational endpoints are stored in the receipt. They prove the sign reversal without a floating-point entropy error hypothesis. The whole conditional-source enclosure has width below `10^-23`.

The checker requires Python 3, SymPy, and mpmath; the verified dependency versions were SymPy 1.14.0 and mpmath 1.3.0. Run:

```bash
python check_fine_archive_spectral.py --json RESULT_FINE_ARCHIVE_SPECTRAL.json
```

The complete JSON receipt is always printed to standard output. `--json PATH` additionally writes the same receipt to the explicit path; without that option, the checker creates no output file. The mathematical calculation contains 659 executed checks, including under `python -O` because it does not use `assert` for its gates.

Here `I_fine=S(F_fine(rho))-S(rho)` and likewise for age. The identity `dI_fine=dI_age+dR` is imposed only after differentiating the same original finite instrument.

## Independent audit of the companion finite-history computation

The companion computation explicitly enumerates actual native products at K=1,2, reads the last-nonblank age of each fine word, and sums quantum states and their jets by that age. The grouped states and jets agree with

\[
X_n=B^n(\rho-B\rho B)B^n\quad(n<K),
\qquad X_K=B^K\rho B^K.
\]

Reported maximum errors are below `4.2e-16` for states and `7.7e-17` for jets. All physical `128^K` slots remain in the description; only structurally zero words are skipped in numerical summation. No rank-one conditional-state assumption is made.

For the native `v` direction, its K=2 results are

\[
d_v I_{\rm fine,2}=0.009381199244727648,
\quad d_v I_{\rm age,2}=-0.0007222151925508451,
\quad d_vR_2=0.010103414437278493.
\]

The inherited all-mode entropy regularization source bound is below `8.4e-9` at K=2. That bound controls smoothing, not floating arithmetic; the companion correctly leaves its K=2 interval-certificate flag false. The independent strict interval proof above is specifically K=1.

## Exact all-K paired-port refinement: approved

For every `j != 0`, merge only the two proportional ports. Keep `j=0,b=0` (the blank) and `j=0,b=1` (the orphan nonblank) distinct. The merged Kraus operator is

\[
L_j=\sqrt{2t}\,N_j^*A,
\qquad
K_{j,0}=-p\,L_j,\quad
K_{j,1}=-\sqrt p\,L_j.
\]

Thus each paired event splits with probabilities `(p^2,p)`. For every chronological merged word, refining its paired events multiplies the whole Kraus amplitude by a scalar product. These scalars commute through all later native operations. Conditional on the merged word, the normalized final quantum state is independent of the refined bits, even for correlated retained preparation.

The merged word still determines age, so the exact chain rule is

\[
R_K=Kq_{\rm pair}H_2(p)+R_{\rm merged,K}
\quad\text{on the stationary input},
\qquad R_{\rm merged,K}\ge0,
\]

where

\[
H_2(p)=-p^2\log p^2-p\log p
=\log\varphi\,(2-p),
\quad q_{\rm pair}=2t h(1-\mu).
\]

The exact arbitrary-input count effect is

\[
C_{\rm pair}=2t(\Delta-\Delta^2),
\]

so the arbitrary-input/refined-bit information is

\[
H_2(p)\sum_{j=0}^{K-1}\operatorname{Tr}[C_{\rm pair}\Phi^j(\sigma)].
\]

This makes the identity a full channel statement rather than just an equality of stationary scalar values.

On `v`,

\[
d_v[Kq_{\rm pair}H_2(p)]
=-2tKh\,d_v\mu\,H_2(p)<0.
\]

The companion has additionally verified the merged Kraus products and both r/v sources at K=1,2. Its exact rational bounds at K=4096 give

\[
R_{4096}>56.5\ \text{nats},\qquad
-0.025<d_v[4096q_{\rm pair}H_2(p)]<-0.024.
\]

These are compatible with the positive full K=1 conditional source: the remaining merged-record source has no established sign. **The negative known subterm is not a sign proof for the complete K=4096 source.**

## Cost, oldRIGHT, and the permitted inference

The actual extra-port count obeys

\[
C_{{\rm port},K}=K\,4p^3h,
\qquad d_v C_{{\rm port},K}=0.
\]

A fixed per-step baseline plus this already defined port charge has zero `v` source. Consequently the corresponding price `C-I/log(phi)` has a positive age-only source and a negative complete-fine source at K=1 and K=2. This statement does **not** identify that partial ledger with the complete physical Cost. No charge is added to cancel the refined-bit information.

For an independent faithful oldRIGHT spectator, both complete channels tensor with its identity. In entropy **gain**, its additive entropy cancels. The same is true for the fine-minus-age conditional correction. This is also an ambient cotangent cancellation at product stationary input, including arbitrary correlated first variations, under the spectator-blind readout/cost assumptions already stated in `SPECTATOR_POISSON.md`. It does not make a genuinely entangled original purification into an independent spectator. For a pure retained purification, conditional DATA/reference blocks are pure and the fine CQ entropy is pointer entropy; that is a different, explicitly identified carrier.

Finally, the fine-minus-age correction can be appended to the same finite-age Poisson/adjoint weld: the input-versus-output entropy-gain boundary correction remains unchanged because both fine and age channels have the same total marginal `Phi^K`. What changes is the actual field source. The exact native sign certificate therefore identifies the next compulsory term in that common carrier, rather than closing or negating the unresolved physical selection problem.
