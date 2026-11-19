# Same-native fine archive beyond the finite age clock

22 October 2026. Bounded continuation of `AGE_CLOCK_SOURCE.md`, equation (10).
This note consumes the existing original CAR16/full128 instrument and the
already-owned complete-CQ calculation. It adds its exact composition with
the **same finite age readout**, and isolates an exactly computable Golden
port contribution for every finite archive length. No Book03 heat or
information convention is selected by this calculation.

## 1. Result and ownership

The missing fine-history conditional entropy is already material at the
original native point `r=1/9`, `nu=3/5`. At K=1 and K=2 its derivative along
the actual one-port-null direction is positive, although the finite age
gain has negative derivative. Thus restoring this actual omitted term
reverses the sign of the information contribution to the price source.
An independent exact spectral/interval audit proves this sign reversal
at K=1; K=2 is the controlled numerical source diagnostic below.

There is also an exact result at **every finite K**, including K=4096.
The actual paired Golden port bits contribute

\[
 I_{\rm bit,K}=K\,2t h(1-\mu)\,H_2(p),\qquad
 H_2(p)=\log\phi\,(2-p),\quad p=\phi^{-1},\quad t=2p^2.
 \tag{1}
\]

They are a genuine part of the missing fine-given-age information. At the
same native point,

\[
 H(\text{fine}\mid\text{age,DATA})\big|_{K=4096}
 \ge I_{\rm bit,4096}>56.5\quad\text{nats}.                 \tag{2}
\]

The displayed strict lower bound is checked by exact rational arithmetic
and a positive logarithm series. The actual bit term is approximately
`56.61855280703027` nats. This does not bound the derivative of the remaining
conditional entropy: a nonnegative function can have either derivative.

**Existing owner.** The original K1/K2 fullfine entropies and their field
sources are already owned by
`A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md` and
`sources/d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py`.
They are replayed unchanged here. The new consumers are the SAME-K age
subtraction, the resulting source comparison, and the all-K paired-bit
composition with this age readout. The general entropy chain rule and the
stationary row-Gram identity are not claimed as newly discovered.

## 2. Exact original instrument and source conventions

The checker consumes the pinned original repository constructor and
owned entropy checker directly:

| Input | Immutable identifier |
|---|---|
| `sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py` | Git blob `ee8de4635d24c668949ac9a0186616ab7d59f2ed` |
| Original native constructor SHA256 | `1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9` |
| `sources/d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py` | SHA256 `cd0052f10bc43abb3736a1637c850c2a3d637f428dd116f6320f68bcf84e3931` |
| `sources/d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_RESULT.json` | Git blob `7530a050c3e0d4cc0aad29648f61fa3b86a524c8` |

The constructor comes from repository path
`02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py`
at `cd7595b0808e47c38147f25e2cabe476ecb508f8`. The two complete-CQ inputs
come from the existing `c8d2a38` tree. The checker verifies the exact native
blob, the complete checker SHA256 and Git blob
`c133c6aec28e2a4068b36a6d9646bc8fb04fc2a4`, and the prior receipt blob before use;
it AST-loads only the required definitions and does not rerun unrelated
old suites.

Let the 64 original Walsh/Julia rows be `N_j`, `A=N_0`,
`Delta=A* A`, and `B=I-t Delta`. The 128 actual Kraus slots are

\[
 K_{0,0}=B,\qquad
 K_{j,b}=-\alpha_bN_j^*A\quad ((j,b)\ne(0,0)),\qquad
 \alpha_0=t,\quad\alpha_1=2p\sqrt p.                       \tag{3}
\]

The constructor retains the actual CAR ordering, phases, one proper
boost, both Julia defects, and all physical label multiplicities. It has
64 structurally dark slots and 64 live slots at this point; the dark
slots and their jets are exactly zero. They remain physical slots even
though zero arithmetic is skipped.

The stationary mixed DATA state is `rho=Delta^-1/Z`, `Z=Tr Delta^-1`.
Set `h=16/Z` and `mu=Tr Delta/16`. The owned exact fixture values are

\[
 h=\frac{69399}{5030720},\qquad
 \mu=\frac{141489}{10240000},\qquad
 h_r=-\frac{20040939}{9885993640},\qquad
 \mu_r=-\frac{328779}{204800000}.                           \tag{4}
\]

We use analytic derivatives through the true Kraus matrices and the
inverse-state preparation, including the derivative of its normalization.
The first direction is the original boost coordinate `r`, with
`theta=2atanh(r)` and `dtheta/dr=81/40`. The second is

\[
 v=\partial_r-\frac{\nu h_r}{2h}\partial_\nu,
 \qquad D_vh=0,\qquad
 D_v\mu=\mu_r-\mu h_r/h>0.                                \tag{5}
\]

Numerically the coefficient of `partial_nu` is `+0.04408551592126523`.
These are two named native directions, not a full spatial 42-field test.

## 3. Same actual K-window: fine output, age output, and normal source

For an actual chronological word `w=(a_1,...,a_K)`, use
`K_w=K_(a_K)...K_(a_1)` and `X_w=K_w rho K_w*`. The fine CQ output is
`Gamma_F=directsum_w X_w`. There is no reset between letters.
The age is the number of trailing blank labels, where **only label 0 is
blank**. The orphan `(j=0,b=1)` is a nonblank event.

Directly grouping all actual words by that last-nonblank age gives

\[
 X_n^{\rm age}=B^n(\rho-B\rho B)B^n\quad(0\le n<K),
 \qquad X_K^{\rm age}=B^K\rho B^K.                         \tag{6}
\]

The last term is the actual allblank tail. Both the block matrices and
their analytic field jets are checked against the grouped fine words.
The maximum numerical discrepancies are below `4.2e-16` and `7.7e-17`,
respectively, in the displayed K1/K2 cases.

Define true input gains

\[
 G_{F,K}=S(\Gamma_F)-S(\rho),\quad
 G_{A,K}=S(\Gamma_A)-S(\rho),\quad
 R_K=G_{F,K}-G_{A,K}
     =H(\text{fine}\mid\text{age,DATA})\ge0.                \tag{7}
\]

Equation (7) is exactly the previously uncomputed term in the age proof.
It compares the same K, input, DATA carrier, labels, and record. In
particular, no K1/K2 fullfine number is compared with an infinite-age
number.

This difference is also valid for an independently varied input `sigma`.
The correct off-stationary age channel is the actual word grouping:

\[
 L_n=\mathcal B^n(\Phi-\mathcal B)\Phi^{K-n-1}\ (n<K),
 \quad L_K=\mathcal B^K,\quad\mathcal B(X)=BXB.
 \tag{8}
\]

Thus `R_K(sigma)=S(F_K sigma)-S(A_K sigma)` for all inputs. Its preparation
score at `rho`, on the supports of the actual blocks, is

\[
 M_{R,K}=A_K^*(\log\Gamma_A)-F_K^*(\log\Gamma_F).
 \tag{9}
\]

The identity terms cancel because both channels preserve trace. Its
PRICE score is `-M_R/log(phi)`. Formula (9) supplies the missing independent
preparation cotangent; computing only the displayed stationary field
derivatives would not supply that normal equation. The age proof's
correction from conditional output entropy to true input gain, equations
(13a,b), still applies to both gains. Their difference (9) is exact
off-section and needs no additional arbitrary extension.

The numerical totals below use the original mixed DATA convention. An
independent retained oldRIGHT state adds the same entropy to the two CQ
outputs and cancels from (7). A purification or correlated retained input
changes the total CQ calculation and must be declared; the exact paired
refinement theorem below remains valid with such a reference retained.

## 4. Actual K1/K2 values and sources

All entropies are in nats. The fine gain column is the existing owner's
value; age gain and the conditional difference use the same actual words.
These tables reproduce the floating receipt. Section 9 supplies independent
exact K1 source enclosures and supersedes its final floating rounding digits.

| K | Fine gain `G_F` | Age gain `G_A` | Missing `R_K` |
|---:|---:|---:|---:|
| 1 | 0.136820928683922 | 0.101756999125088 | 0.035063929558834 |
| 2 | 0.273641861298791 | 0.201377896046870 | 0.072263965251920 |

| Direction | K | `D G_F` | `D G_A` | `D R_K` |
|---|---:|---:|---:|---:|
| original boost `r` | 1 | -0.014892336676930 | -0.012115916987736 | -0.002776419689194 |
| original boost `r` | 2 | -0.029784592156762 | -0.023716418741907 | -0.006068173414855 |
| one-port-null `v` | 1 | +0.004690557706558 | -0.000339098881652 | +0.005029656588210 |
| one-port-null `v` | 2 | +0.009381199244728 | -0.000722215192551 | +0.010103414437278 |

With the native information unit `ell=log(phi)`, the v-source comparison is

| K | Age-only information price `-D_v G_A/ell` | Missing fine price `-D_v R_K/ell` | Fullfine information price `-D_v G_F/ell` |
|---:|---:|---:|---:|
| 1 | +0.000704676950967 | -0.010452063574263 | -0.009747386623296 |
| 2 | +0.001500825945957 | -0.020995773401926 | -0.019494947455968 |

This sign reversal is the concrete source consumer. It does not assert a
sign for the total physical Book source. The large-K coarse age entropy
cancellation remains an exact result on its declared coarse carrier;
this table shows why that result cannot be promoted to fullfine
information by suppressing the conditional term.

## 5. Exact paired-bit theorem for all finite K

Merge the two ports of each row `j!=0`, keeping the blank and the orphan
as two distinct labels. The resulting 65 physical merged labels have
Kraus matrices

\[
 M_0=B,\quad M_1=K_{0,1},\quad
 M_j^{\rm pair}=-\sqrt{2t}\,N_j^*A\quad(j\ne0).
 \tag{10}
\]

For each paired row,

\[
 K_{j,0}=pM_j^{\rm pair},\qquad
 K_{j,1}=\sqrt p\,M_j^{\rm pair},\qquad p^2+p=1.
 \tag{11}
\]

Fix any merged chronological word z containing `N_pair(z)` paired
occurrences. Each fine refinement multiplies its entire operator product
by the product of the corresponding scalars `p` or `sqrt(p)`.
These scalars commute with every intervening noncommuting Kraus matrix.
Consequently, conditional on z, all fine port assignments have probability
`product q_b`, with `q_0=p^2,q_1=p`, and **the same normalized conditional
DATA state**. This statement remains true with an arbitrary initially
correlated reference retained throughout.

If `Gamma_M` denotes the merged CQ output, this proves directly

\[
 S(\Gamma_F)-S(\Gamma_M)=H_2(p)\,\mathbb E[N_{\rm pair}].
 \tag{12}
\]

Age is still a deterministic function of z, since blank and orphan were
kept separate. Therefore the full missing term splits exactly as

\[
 \boxed{R_K=H_2(p)\,\mathbb E[N_{\rm pair}]
              +H(\text{merged}\mid\text{age,DATA}).}
 \tag{13}
\]

The second term is nonnegative; its derivative has no sign restriction.
Equation (13) is a decomposition of the already retained physical tape.
It does not declare a physical erase gate or remove the cost of either
record.

The original Walsh rows satisfy both `sum N_j* N_j=I` and
`sum N_j N_j*=I`. The latter follows directly from Walsh orthogonality
and each original Julia row pair `(x,sqrt(I-xx*))`, with the corresponding
adjoint and base pairs. The actual paired count effect is consequently

\[
 C_{\rm pair}=\sum_{j\ne0,b}K_{j,b}^*K_{j,b}
 =2tA^*(I-AA^*)A=2t(\Delta-\Delta^2).                      \tag{14}
\]

For any input, including a correlated retained preparation, its expected
count and preparation score are the finite expressions

\[
 \mathbb E_\sigma[N_{\rm pair}]
  =\sum_{s=0}^{K-1}\operatorname{Tr}(C_{\rm pair}\Phi^s\sigma),
 \qquad
 M_{\rm bit,K}=H_2(p)\sum_{s=0}^{K-1}(\Phi^*)^sC_{\rm pair}.
 \tag{15}
\]

For a retained reference the displayed score is tensored with its
identity. Thus the all-K piece has a fully explicit normal source; it is
not obtained by freezing preparation. All field derivatives of `C_pair`
and the K-step propagation in (15) remain in its direct source.

On the actual stationary section, (14) gives
`q_pair=Tr rho C_pair=2t h(1-mu)`. Finally
`H_2(p)=-p log(p)-p^2 log(p^2)=ell(2-p)`, which proves (1).
The checker separately constructs the 33 live merged Kraus outcomes and
their actual K1/K2 products; full-minus-merged entropy and source agree
with (12). The residual merged-given-age quantities are

| K | `H(merged | age,DATA)` | r-source | v-source |
|---:|---:|---:|---:|
| 1 | 0.021241040689933 | -0.000767624109456 | +0.005035615134320 |
| 2 | 0.044618187514036 | -0.002050582255381 | +0.010115331529499 |

## 6. K4096 is an exact partial consumer, not a full transfer solution

At K=4096 the actual bit entropy and its sources are

| Quantity | Value |
|---|---:|
| Paired-bit entropy | 56.61855280703027 |
| Original boost source | -8.228026694604413 |
| One-port-null source | -0.024406204867662453 |

The exact one-port-null expression is

\[
 D_v I_{\rm bit,K}=-2tK h\,(D_v\mu)\,H_2(p)<0.              \tag{16}
\]

An elementary rational certificate avoids relying on the decimals.
Take `p_L=309/500 < p < p_U=6181/10000`, verified by the sign of
`x^2+x-1`. Since `ell=2atanh(p^3)`, put `x_L=p_L^3`, `x_U=p_U^3` and use

\[
 2(x_L+x_L^3/3)<\ell
 <2\left(x_U+x_U^3/3+\frac{x_U^5}{5(1-x_U^2)}\right).
 \tag{17}
\]

Substitution into (1), using the exact rational h and mu in (4), gives a
rational lower bound greater than `56.5640`, hence proves (2). The same
bounds and the exact positive rational `D_v mu` prove

\[
 -0.025<D_v I_{\rm bit,4096}<-0.024.                       \tag{18}
\]

The receipt saves the exact rational endpoints. Neither (2) nor (18)
computes the remaining merged-record entropy source at K4096. Its
noncommuting conditional states have not been replaced by a finite
classical Markov model, and K1/K2 values have not been extrapolated.

## 7. Actual charges and the limited price conclusion

For any supplied literal fine-label charges `c_a`, the fixed-window
stationary charge is exactly

\[
 C_K=K\sum_a c_a\operatorname{Tr}(K_a\rho K_a^*).           \tag{19}
\]

The script verifies the existing extra-port count `b`, not an invented
total Book charge: its expectation is `K 4p^3 h`, its v-source is exactly
zero, and its r-source is `K 4p^3 h_r`. A previously declared constant
baseline plus an affine port tariff therefore has the same v-source as
the information table, but label-dependent charges, literal stage
payments, preparation, clock/controller work and any further paid
operations still need their actual ledgers. No zero/ten stage ledger is
replaced by a unit port count.

The paired-bit calculation can be applied to actual tariffs without
choosing them. For a paired row with literal charges `c_(j,0),c_(j,1)`,
the expected retained charge conditioned on that merged row is
`p^2 c_(j,0)+p c_(j,1)`. If the declared information is the full CQ input
gain, eliminating this exactly known conditional entropy from the
formula yields the effective paired contribution

\[
 \bar c_j-(2-p),\qquad
 \bar c_j=p^2c_{j,0}+pc_{j,1}.                             \tag{20}
\]

This is an exact Cost-minus-Info decomposition for the actual scalar
refinement. The original full128 port-report owner does in fact specify
the tariff: [PROOF.md](../d0_book_uniform_source_2026-10-21/PROOF.md),
Git blob `faac1bc80e25cfbcaba951f46b22b3ba1d9f3b84`, §1, has
`c_b=1+b`. Its §7 keeps this price attached to the original port under
any output relabeling, unless additional real padding is paid.
Therefore the actual paired residual is fixed:

\[
\bar c=p^2+2p=1+p,\qquad
\boxed{\bar c-(2-p)=2p-1=p^3>0.}                     \tag{20a}
\]

Reversing the tariff to `(2,1)` would give a different price and is not
authorized by the original port-report definition. Nor is this conclusion
borrowed from the distinct N1 F/R code.

There is a useful exact whole-price consequence on the declared port-CQ
gain interface. Let the merged record retain the true blank, orphan and
all SELECT-row labels. For any finite K and any input, including an
arbitrarily correlated retained reference,

\[
\boxed{
P_{\rm port-gain,K}
=\mathbb E[N_{\rm blank}+2N_{\rm orphan}+p^3N_{\rm pair}]
-\frac{S(\Gamma_{\rm merged,K})-S(\Omega)}{\ell}.}
\tag{20b}
\]

Here the left side is the original true cost `E sum(1+b)` minus the
full fine CQ input gain. Equation (20b) follows from the conditional
expected tariff and (12), before imposing stationarity. It therefore
preserves every independent input equation and all field jets on their
regular support. The positive `p^3` is a derived net contribution after
accounting for actual refined-bit information, not a new physical tariff
or a license to erase recorded bits. The mathematical merged expression
has 65 physical labels (33 live at the named fixture), while the actual
fine execution still retains all 128 slots.

The full merged CQ information and every real additional factory,
fine-label, preparation, controller and clock cost remain. This exact
reduction settles the declared port-report/CQ-gain component; it does
not identify it with compulsory full Book03. `GR_closed=false`.

## 8. Reproduction and numerical scope

Run `OPENBLAS_NUM_THREADS=1 python check_fine_archive_source.py` from the
repository or the checker directory. It discovers the repository root
from the current working directory and script ancestors, then consumes
the three original source files listed in section 2. Use `--repo-root
/path/to/repository` to select an explicit repository. It always emits
JSON on stdout and writes a receipt file only when requested with
`--json RESULT_FINE_ARCHIVE_SOURCE.json`. The optional `--input-dir DIR`
accepts an existing directory containing the same three pinned files;
it is mutually exclusive with `--repo-root`. There is no implicit output
path or temporary-directory dependency.

For K1 and K2 it uses respectively 128 and 16384 physical word slots,
of which 64 and 4096 are live. It retains every singular mode of every
live amplitude and uses the owned analytic-jet entropy algorithm with
`eta=1e-22` and the control `eta=1e-24`. Its regularization source bounds
for the fullfine entropy are approximately `5.44e-10` and `8.37e-9`.
These are smoothing bounds, not outward floating-point certificates.

All same-K age blocks have eigenvalues above `1e-3`; the sum of the trace
norms of their displayed source matrices is below 1. For
`S_eta(X)=-Tr X log(X+eta I)`, the source error factor obeys
`log(1+u)-u/(1+u) <= u^2/2`, `u=eta/lambda`. Hence the age source smoothing
error is below `5e-39`, and the conditional source bound is the inherited
fullfine bound plus this quantity. No source sign is inferred from
entropy positivity. Exact claims (10)-(18) follow from the actual
operator/scalar identities and rational comparisons, independently of
the numerical spectral evaluation of the remaining merged entropy.

## 9. Independent exact K1 sign certificate

The separate audit `FINE_ARCHIVE_SPECTRAL_AUDIT.md`, executable
`check_fine_archive_spectral.py`, and receipt
`RESULT_FINE_ARCHIVE_SPECTRAL.json` independently certify the
one-round source using the actual original row matrices. The audit also
approves the all-K refinement, correlated preparation, count effect,
tariff averaging, and rational K4096 bounds in sections 5–7.

Its new exact reduction retains all 64 row slots and both ports. The 32
live row Grams fall into eight spectral classes with the same classwise
v-jets. The odd-operator rows obey exact quadratic Gram identities with
eightfold eigenvalue multiplicities. The even Julia rows split into
actual scalar and 2 by 2 Hermitian blocks. The complex matrices have
coefficients in `Q(i,sqrt(24142))`; positive Julia roots and their
differentiated square identities are checked exactly. No SVD or numerical
eigenvalue cutoff enters the interval proof.

For `E_j=N_j* N_j` and `Acal=sum_j Tr(E_j log E_j)`, cancellation of the
same ordinary blank from fine and age at K1 gives the exact v-source
identity

\[
 \boxed{
 D_vR_1=\frac{t^2}{Z}\operatorname{Tr}\!\left[
 \log\!\left(\frac{t\Delta}{2I-t\Delta}\right)D_v\Delta
 \right]-\frac{2t}{Z}D_v\mathcal A.}
 \tag{21}
\]

Here `D_vZ=0` follows from the actual original matrices. The existing
stationary row-block identity is consumed, not claimed as new. The eight
exact classes evaluate the remaining `D_v Acal`, including every
physical multiplicity and zero mode.

The independent checker passed 659 checks. It encloses all scalar roots
by integer square roots and all logarithms by rational atanh-series
remainders, with outward rounding to 100-bit dyadic endpoints. The
resulting strict intervals include

\[
 \begin{aligned}
 D_vR_1&\in
 (0.0050296565882099257579220245,
  0.0050296565882099257579220345),\\
 D_vG_{A,1}&\in
 (-0.0003390988816519018581384328,
  -0.0003390988816519018581384200),\\
 D_vG_{F,1}&\in
 (0.0046905577065580238997835917,
  0.0046905577065580238997836144).
 \end{aligned}                                             \tag{22}
\]

Thus the K1 sign reversal is a strict statement about the original
mixed-DATA quantum blocks, without a floating entropy-error hypothesis.
The fine gain and conditional entropy values independently evaluate to
`0.136820928683929019866458...` and
`0.0350639295588407180528597...`; the small difference from the replay
table is ordinary floating arithmetic, already distinguished from its
smoothing bound. No K2 or K4096 fullfine interval-source result is
claimed. Equation (22), the all-K partial identity, and the exact normal
scores still do not select the complete physical Book information or
heat.
