# Actual native port constraint and maximum-entropy preparation

22 October 2026. Existing Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Phase: native realization / constitutive source composition.
Read-only input checkpoint: `cd7595b0808e47c38147f25e2cabe476ecb508f8`.

## 0. Exact contribution and parent use

The original full128 process has the invariant DATA marginal
`rho_* = Delta^-1 / Tr(Delta^-1)` on its regular mixing chart. Its actual
Golden port effect is `E_port = c Delta`, with the previously derived
positive constant `c = 4 p^3` on the literal CAR16 Fourier normalization.
Neither state nor response test is chosen to match an Einstein equation.

This note applies Book06's specified maximum-entropy-under-retained-tests
construction to **this actual DATA response test**. It proves:

1. For a positive finite `Delta`, its inverse-square preparation is the
   maximum-entropy state at its own mean energy if and only if `Delta`
   has at most two distinct eigenvalues.
2. On the original native two-band CAR16 fixture it is therefore already
   that maximum-entropy representative. The marginal information gain
   `S(maximum-entropy state) - S(rho_*)` is zero, with zero full first source
   in every smooth native direction, even a direction that splits bands.
3. The second source detects precisely the traceless within-band splitting;
   its formula is given below. A moving retained test has a nonzero source
   even when its measured mean is fixed. Freezing that test is incorrect.

This is a **positive identification of one specific forgetting problem**,
and an exact restriction on using it as the missing native information.
It does not identify the DATA marginal with the complete retained history,
make the generated dual temperature the physical Book03 temperature, or
select this forgetting problem as compulsory Book03 `Info`. The complete
fine history, conditional quantum work, preparations, oldRIGHT and clock
remain in the full-price problem. `GR_closed=false`.

### Owned inputs, consumed without replay

- [Book06](../../../../01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md),
  sections 06.24--06.25: maximum entropy is conditional on specified
  retained response tests, forgotten coordinates, loss quotient and
  entropy representative. Its global accounting paragraph distinguishes
  that quotient from destruction of a complete archive.
- [Original preparation](../d0_native_preparation_closure_2026-10-21/PROOF.md),
  sections 1--3 and 7: the actual full128 stationary state, moving-state
  derivative and CAR16 quadratic spectral identity.
- [Original complete channel](../../A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md),
  sections 1--3 and 6--7: actual port effect; distinction between complete
  coherent record, measured pointer and retained conditional work.
- [Original modular compatibility](../../A4D_NATIVE_CORRELATED_RETURN_MODULAR_HEAT_COMPATIBILITY_2026_10_22.md),
  sections 1--2: the two-band Gibbs dual formula was already known;
  the actual Golden temperature does not give this state.
- [Native Ward test](../../A4D_ORIGINAL_FULL128_BOOK_THERMAL_WARD_OBSTRUCTION_2026_10_22.md),
  equations (1)--(5), (14) and (19)--(23): exact native `mu,h,mu',h'`,
  one-port-neutral tangent and nonzero modular entropy source.

The new statement is the maximum-entropy **gain and full-source
application**, including the classification and transverse Hessian. The
known formula for the two-band dual temperature is not claimed as new.

## 1. One precisely specified native forgetting problem

Let `Delta > 0` act on a `d`-dimensional complex Hilbert space. Define

\[
 Z_{-1}=\operatorname{Tr}\Delta^{-1},\qquad
 \rho=\frac{\Delta^{-1}}{Z_{-1}},\qquad
 h=\operatorname{Tr}(\rho\Delta)=\frac d{Z_{-1}}.
 \tag{1}
\]

Use natural-log von Neumann entropy throughout; division by `ln(phi)`
converts to Golden information units. The problem is

\[
 \sigma_*=\arg\max_{\sigma\succeq0}
 \{S(\sigma):\operatorname{Tr}\sigma=1,
                  \operatorname{Tr}(\sigma\Delta)=h\}.
 \tag{2}
\]

On the native fixture, (2) is exactly the same response constraint as
`Tr(sigma E_port)=q`, since the actual `E_port=c Delta` and `q=c h`.
If `c` itself moves, these identities are differentiated together; (2)
remains equivalent on any chart where `c>0`. There is no unrecorded
replacement of the measured test by a fixed energy table.

For nonscalar `Delta`, `lambda_min < h < lambda_max`. The strictly
decreasing Gibbs mean

\[
 m(\beta)=\frac{\operatorname{Tr}\Delta e^{-\beta\Delta}}
                       {\operatorname{Tr}e^{-\beta\Delta}},
 \qquad m'(\beta)=-\operatorname{Var}_{\sigma_\beta}\Delta<0
 \tag{3}
\]

has one solution `m(beta_*)=h`. It is positive because the harmonic mean
`h` is strictly smaller than the arithmetic mean `m(0)`. The unique
maximizer is `sigma_* = exp(-beta_* Delta)/Z_beta`. Its uniqueness can
also be read directly from the relative-entropy identity in section 3.

## 2. Complete spectral classification

**Theorem 1.** The inverse-square state (1) equals (2) if and only if
`Delta` has at most two distinct eigenvalues.

If `Delta=lambda I`, the response constraint is redundant. Both states
are `I/d`; a Gibbs multiplier is not unique. No smooth unique-multiplier
claim at this scalar degeneracy is used below.

If `Delta` is nonscalar, equality of the two faithful states requires

\[
 \log\lambda=a+\beta_*\lambda
 \quad\text{for every distinct eigenvalue }\lambda.
 \tag{4}
\]

The strictly concave logarithm cannot meet one affine line at three
ordered points: its middle value would lie strictly above the chord
through the first and third. Thus there can be at most two eigenvalues.

Conversely, for two eigenvalues `0<lambda_-<lambda_+`, with arbitrary
positive multiplicities, the unique slope

\[
 \beta_*=
 \frac{\log\lambda_+-\log\lambda_-}{\lambda_+-\lambda_-}>0
 \tag{5}
\]

makes `exp(-beta_* Delta)` a common scalar multiple of `Delta^-1`.
Normalization gives equality, and its mean is exactly (1).

Equivalently, pinch any feasible state into the two spectral blocks and
replace each block by its scalar trace multiple of the identity. These
operations cannot lower entropy. Normalization and the one energy moment
fix both block weights, and they are exactly the weights of (1).

Equation (5) is an **endogenous dual variable of the explicitly specified
constraint problem**. It does not authorize changing an execution's
actual inverse temperature or Hodge operator.

## 3. Exact information gap and its whole first source

Because `rho` and `sigma_*` share trace and the true energy moment,

\[
 \begin{split}
 I_\Delta
 &:=S(\sigma_*)-S(\rho)\\
 &=D_{\rm rel}(\rho\Vert\sigma_*)\ge0.
 \end{split}
 \tag{6}
\]

This follows by inserting `log sigma_*=-beta_* Delta-log Z_beta`.
In particular, three or more distinct eigenvalues give a strict positive
gap, while the one- and two-band cases give zero.

On a smooth chart about a **nonscalar** two-band point, all states are
faithful and the variance in (3) is strictly positive. The implicit
function theorem therefore makes `beta_*(Delta,h)` smooth, also when a
tangent splits an eightfold band. Matrix logarithm and exponential are
smooth on the positive cone. Consequently (6) is a smooth nonnegative
function with a zero at the native point, so

\[
 \boxed{D I_\Delta[E]=0\quad\text{for every Hermitian tangent }E.}
 \tag{7}
\]

The conclusion includes field-generated preparation and moving response
tests. It is stronger than differentiating along a curve that happens to
stay two-band. Any actual admitted native tangent is a subset of these
matrix tangents; (7) therefore does not assume that every matrix tangent
is physically writable.

For clarity, the maximum entropy **itself** is generally not stationary.
Its exact envelope derivative is

\[
 \boxed{D S(\sigma_*)
       =\beta_*\{D h-\operatorname{Tr}(\sigma_*D\Delta)\}.}
 \tag{8}
\]

This follows by differentiating
`S(sigma_*)=beta_* h+log Z_beta`; the `D beta_*` terms cancel by the
constraint. At a two-band point (8) equals `D S(rho)`, which proves (7)
directly. At fixed measured mean `D h=0`, the moving-test term remains.
Dropping it would confuse a fixed response value with a fixed observable.

## 4. What the first nonzero marginal response detects

The following exact Hessian makes the zero first source constructive.
Write the nonscalar two-band base as

\[
 \Delta_0=\lambda_-P_-+\lambda_+P_+,\quad
 m_a=\operatorname{rank}P_a,\quad
 \tau_a=(Z_{-1}\lambda_a)^{-1},
\]

where `tau_a` is the probability of each vector in block `a`. For the
Hermitian tangent `E=D Delta`, define its traceless compression

\[
 E_a^0=P_aEP_a-
       \frac{\operatorname{Tr}(P_aE)}{m_a}P_a.
\]

**Theorem 2.** Along any twice differentiable positive path with initial
velocity `E`,

\[
 \boxed{
 D^2 I_\Delta[E,E]
 =\sum_{a\in\{-,+\}}
   \tau_a(\beta_*-\lambda_a^{-1})^2
   \operatorname{Tr}[(E_a^0)^2].}
 \tag{9}
\]

The path's acceleration does not enter because (7) holds. No commuting
variation is assumed.

Proof. Let `X=D rho-D sigma_*` at the equality point. Differentiating
the two matching moments gives `Tr X=Tr(Delta_0 X)=0`, hence zero trace
in each spectral block. On a cross-band matrix entry, the inverse
derivative and Gibbs divided difference coincide:

\[
 (D\rho)_{ij}=-\frac{E_{ij}}{Z_{-1}\lambda_a\lambda_b},
 \qquad
 (D\sigma_*)_{ij}
 =\frac{\tau_a-\tau_b}{\lambda_a-\lambda_b}E_{ij}
 =-\frac{E_{ij}}{Z_{-1}\lambda_a\lambda_b}.
\]

Inside one band, normalization and multiplier derivatives contribute
only scalar matrices. The zero band traces therefore give

\[
 X_{aa}=\tau_a(\beta_*-\lambda_a^{-1})E_a^0,
 \qquad X_{ab}=0\ (a\ne b).
\]

The Hessian of relative entropy at equal faithful arguments is
`Tr[X Dlog_rho(X)]`. On a scalar block `rho=tau_a I`,
`Dlog_rho(X)=X/tau_a`. Substitution proves (9).

Thus within-band scalar motion and rotations between the bands create
no second-order gap. Genuine splitting of a degenerate band creates a
strict positive gap, since the secant slope (5) lies strictly between
`1/lambda_+` and `1/lambda_-`. This describes the precise extra marginal
distinction rather than assigning a new physical selector.

## 5. Application to the unchanged original CAR16 fixture

Consume its exact two-band identity with multiplicities `8+8`:

\[
 \lambda_\pm=\mu\pm\epsilon,\qquad
 \epsilon^2=\mu(\mu-h),\qquad
 \mu=\frac{141489}{10240000},\quad
 h=\frac{69399}{5030720}.
 \tag{10}
\]

The original response `q=c h` therefore admits exactly the
maximum-entropy representative `rho_*` without introducing a new state.
Its dual `beta_*` is approximately `72.4119882775`, while the owned
Golden inverse temperature is `beta_0=2p^2`, approximately `0.7639320225`.
They are different quantities. The already owned fixed-`beta_0` Gibbs
mismatch and strict thermal Ward source are preserved.

For its proper-boost derivative `r=tanh(theta/2)` at `r=1/9`, use the
unchanged exact data

\[
 \mu'=-\frac{328779}{204800000},\qquad
 h'=-\frac{20040939}{9885993640},\qquad
 \epsilon'=\frac{(2\mu-h)\mu'-\mu h'}{2\epsilon}.
 \tag{11}
\]

Then the true entropy source is

\[
 D_rS(\rho_*)
 =\beta_*\left[h'-\mu'+\frac\epsilon\mu\epsilon'\right]
 \simeq-0.01536666760108
 \quad\text{(natural nats per unit }r\text{)}.
 \tag{12}
\]

Both terms in (8) are necessary. On the already owned one-port-neutral
tangent `v`,

\[
 D_vh=0,\quad
 D_v\mu=\mu'-\mu h'/h>0,\quad
 D_v\epsilon=\frac{2\mu-h}{2\epsilon}D_v\mu,
\]

and (8) still has a nonzero negative value. Nevertheless the **gain**
in (6) has exactly zero source on both directions, and on every other
smooth tangent at this fixture.

Therefore one cannot cancel its already measured thermal imbalance by
calling `S(rho_*)` the entropy gained relative to the same marginal
maximum-entropy state. That latter gain is zero. The complete temporal
record and its quantum correlations remain a different, source-visible
object; their evaluation in the companion complete-CQ proof is the next
actual same-execution term, not a change to this marginal constraint.

## 6. Validation and explicit boundary

`check_maximum_entropy_preparation.py` uses standard-library `Decimal`
at 80 digits. It consumes the exact rational native spectral data;
it does not rerun the original 128-Kraus or all42 source suites.

- The native two-band Gibbs/moment equality and its moving-test source
  are checked against independent entropy differentiation.
- A three-band `diag(1,2,4)` control has a strict positive gap at the
  same actual harmonic-energy constraint; the two adjacent secant slopes
  disagree analytically.
- A controlled splitting of the actual native eightfold band has zero
  first gap source and the positive Hessian (9).
- A generated dual multiplier is distinguished from the owned Golden
  temperature; scalar degeneracy has no asserted unique multiplier.

The logarithm/exponential comparisons are high-precision numerical
checks of the analytical proof, **not interval-certified numerical
bounds**. Normal and optimized execution perform the same explicit
checks. The result file records the immutable authored output.

No interpretation of this marginal gain as compulsory `Book03 Info`
has been introduced. No hidden preparation is supplied; exact stationary
preparation is the consumed marginal theorem, and a finite paid prewarm
keeps its own complete source. Selection of the actual retained algebra,
all fine work/record/clock terms, and comparison with the original
42-field covector remain the parent obligations. `GR_closed=false`.
