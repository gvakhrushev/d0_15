# Full h² price: a causal thermal form factor survives finite-shell elimination

17 October 2026. Same Draft #334, input e397a0af. Consumer: the explicit
[full-price coefficient (14a)](A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md)
is tested as a functional, beyond the earlier single
[longitudinal Einstein-kernel control](A4D_FINITE_CAUSAL_RESPONSE_AND_CLOSURE_TEST.md).
The calculation uses the actual proper-link Delta_1, both ordered thermal
insertions, the full trace and the actual normalized matter Schur term.

**Result.** On the declared fixed-positive-G LC graph at fixed beta>0,
the transverse quadratic h² coefficient has a discrete Stieltjes thermal
form factor. Its inverse-frequency expansion has superexponentially
growing coefficients. Local stencil seagulls are polynomials; stationary
matter on the actual eight-momentum first shell adds an eventually
rational function. Neither can cancel this tail. Thus this full conditional coefficient is not a
finite-order local Einstein functional on the whole family.

This is a theorem about the controlled coefficient (14a), not an existence
theorem for joint roots or a universal D0 no-go. The independently derived
physical price/observer/archive law could differ. No new term is installed.

## 1. The actual family, conventions and limiting order

Work on the period2pi torus. Keep all16 exterior components and reference128.
On the true-LC graph let G=nu^-2 I4 and vary one Lorentz-cone field

```text
theta_1(x)=epsilon cos(q x2), theta_2=theta_3=0,
0<nu<1, q a positive odd integer.
```

The raised-form intertwiner in the existing coframe/source bridge gives
`D0=nu sum_r gamma_r partial_r`, independent of theta, where
`gamma_r=C_r-I_r`, `beta_r=C_r+I_r`. Hence
`lambda_k=nu^2 |k|^2`, k in Z4. At the flat base Delta_1=0, since the
constant-coefficient D1 uses beta_r and {gamma_r,beta_s}=0. The discrete
native stencil has the actual
proper-link coefficients D1,D2, not a replaced Hodge difference operator.
The full-price h² coefficient is taken under the declared combined
heat/source expansion hypotheses. No new global finite-h C² remainder
is inferred merely from the finite symbolic checks below.

Each q defines one smooth germ and is fixed during refinement. Only after
forming that coefficient do we examine q→infinity along odd integers.
No simultaneous high-q/h limit, uniform bound in q or original raw
h^-2/#216 conclusion is asserted.

Let E_k=exp(-beta lambda_k), Z=16 sum_k E_k, A_k=1-z+zE_k,
M>0, 0<z<1. The combined H+J spectral gradient at the background is

```text
kappa(lambda)=-exp(-beta lambda)/Z
             +M beta z exp(-beta lambda)/(1-z+z exp(-beta lambda)). (1)
```

Its divided difference is exactly

```text
kappa^[1](lambda_k,lambda_l)
 =(E_k-E_l)/(lambda_l-lambda_k)
   [1/Z-M beta z(1-z)/(A_k A_l)].                         (2)
```

Use the derivative at equal eigenvalues. The global logZ Hessian term is
zero for this nonzero Fourier transfer by trace orthogonality, not by
freezing Z. The clock insertion Delta0² is cone-independent on this
particular fixed-G graph; it remains in other field directions.

## 2. Full16 proper-link vertex, including the shifted endpoint

Write Gamma for the full exterior lift of a4x4 generator. With R_ab the
spatial rotation generator and B_ab the boost generator, the pinned LC
first connection coefficients give

```text
B0=-beta_0 Gamma(R12), B1=-gamma_1 Gamma(B02),
B2= beta_2 Gamma(R01), B3=0.
```

For the unit complex mode exp(i q x2), put l=k+q e2, u=k2+q/2. The actual
D1 and Delta_1 vertices are

```text
V_q(k)=-nu q(B0 k0+B1 k1+B2 u),
X_q(k)=D0(l)V_q(k)+V_q(k)D0(k).                           (3)
```

The q/2 is the moving-endpoint contribution from both proper derivative
legs and the true reverse-block adjoint. Using an unshifted k2 is wrong.
Full16 CAR, followed only by the k0/k1 parity average allowed by (2), gives

```text
||X_q(k)||_HS²_even
 =16 nu^4 q²[P0+u²P2],
A=k0²+k1², P0=A(2k1²+q²/4), P2=2A+q²/2.                 (4)
```

No grade or high mode is discarded. For the real cosine, the epsilon²
susceptibility coefficient in S2 is

```text
B(q)=(1/4) sum_k kappa^[1](lambda_k,lambda_(k+qe2))
                    ||X_q(k)||_HS².                    (5)
```

The factor1/4 combines the two Fourier edges, each cosine amplitude1/2,
and the coefficient/Hessian factor1/2. It is not a separate calibration.

## 3. Exact discrete form factor and local part

For c=k0²+k1²+k3² define

```text
F_kappa(q;c)=sum_(j in Z)
 [kappa(nu²((j+q)²+c))-kappa(nu²(j²+c))]
 /[nu²((j+q)²-j²)].                                    (6)
```

For odd q there is no denominator zero. Shift the first numerator index
by q; absolute convergence of the exponentially decaying terms justifies
this operation. The exact identity is

```text
F_kappa(q;c)=(2/nu²) sum_j kappa(nu²(j²+c))/(4j²-q²).      (7)
```

At a finite cutoff N>=q, retain the boundary
`[sum_(j=N+1)^(N+q) f_j/(2j-q)-sum_(j=-N)^(-N+q-1)
f_j/(2j-q)]/(nu²q)`; it tends to zero. It must not be silently dropped
from a finite numerical sum.

Similarly the weighted u² sum equals `-sum_j kappa(lambda_j)/(2nu²)`.
Consequently the complete bubble is

```text
B(q)=4nu^4 q² sum_(k0,k1,k3) A(2k1²+q²/4) F_kappa(q;c)
     -2nu² q² sum_k (2A+q²/2) kappa(lambda_k).            (8)
```

The second term is a local polynomial. Equation (8), rather than a
single sampled eigenvalue or the sign of one probability, is the consumer
of the full signed/nonlinear price.

## 4. The nonlocal term cannot be a rational function

The Poincare Laurent expansion of the first term of (8), along odd q at
infinity, has for every r>=1 the coefficient of q^(-2r)

```text
C_r=-8nu² 4^r sum_k A k2^(2r)(2k1²+k2²) kappa(lambda_k). (9)
```

Both q² and q⁴ prefactors in (8) are combined in this formula. There is
no independent prefactor available to cancel its tail.

For fixed expansion order, split |k2|<=q/4 from its complement. In the
first region expand the geometric denominator in (7) with its exact
remainder. The complement is exponentially small in q², even including
the near-pole odd-grid terms (whose denominators have magnitude at least
of order q). Gaussian bounds on the other three momenta justify summing
all polynomial weights. This proves the Poincare expansion with (9).
It is not claimed to be a convergent Laurent series.

For large lambda the same combined gradient has

```text
kappa(lambda)=a1 exp(-beta lambda)+O(exp(-2beta lambda)),
a1=-1/Z+M beta z/(1-z).
```

If a1=0, the leading term is instead
`a2 exp(-2beta lambda)`, with `a2=-M beta z²/(1-z)²<0`.
Thus kappa always has a fixed nonzero sign beyond some finite spectral
threshold. The finite set below that threshold contributes at most an
exponential in r to (9). All terms in the remaining tail have the same
sign and nonnegative polynomial weights. Already k0=1,k1=k3=0 and
`|k2|` nearest `sqrt(r/(j_* beta nu²))`, j_*=1 or2, give growth of order
`[r/(e j_* beta nu²)]^r` up to subexponential factors. Therefore C_r is
eventually nonzero and

```text
lim_(r→infinity) |C_r|^(1/r)=+infinity.                  (10)
```

A rational function has a Laurent expansion at infinity whose tail
coefficients grow at most exponentially. Uniqueness of Poincare
coefficients therefore proves that (8) is not rational. This argument
retains the heat and feedback terms together, including the possible
cancellation a1=0; it does not rely on heat dominance or float signs.

## 5. Actual first-shell preparation cannot cancel the tail

Use the actual shell `Sigma={+/-e0,+/-e1,+/-e2,+/-e3}` at lambda0=nu²,
its entire projector P, and all16 form/reference128 components. Let C0
be any normalized purification on that shell; its rank, phases, momentum
coherences and reference frame are unrestricted. Leading preparation may
move inside this same shell with epsilon. Its value at the common flat
background is fixed across the Fourier tests.

For odd q, no integer-shell point p has another p±qe2 on the same energy:
equality would require q=+/-2p2. Therefore for the **linear epsilon jet**
`V=partial_epsilon Delta_1|0`, we have P V P=0. This does not assert that
P Delta_1(epsilon) P vanishes at nonlinear epsilon.

Let R_Q invert Delta0-lambda0 on the orthogonal complement of P. Whenever
the actual normalized amplitude Euler family has the necessary jets,
its off-shell first correction and second Rayleigh coefficient obey

```text
C1_Q=-R_Q Delta_1 C0,
R2=Tr(rho0 Delta_2)-Tr(rho0 Delta_1 R_Q Delta_1).         (11)
```

Expansion of the normalized Rayleigh quotient gives the minus sign: its
two mixed terms combine with the off-shell quadratic term. Projected
shell terms cancel using that same amplitude Euler equation and
normalization, not by freezing them. If projected compatibility fails,
there is no such stationary preparation family; (11) does not assert one.

The moving leading-shell derivatives also cannot hide a cancellation in
the epsilon² coefficient under consideration. On this actual first shell,
the literal flat dispersion gives `P Delta_2,flat P=-nu² P/12`:
`4nu² sin²(h/2)/h²=nu²-h²nu²/12+O(h^4)` on every incoming shell
momentum. Also
`P(partial_epsilon Delta_2|0)P=0` by the odd Fourier transfer. Thus rho0'
terms vanish and rho0'' pairs only with a scalar times Tr(rho0'')=0.
In the Schur term both Delta_1 factors vanish at epsilon=0, so only rho0(0)
contributes to its epsilon² coefficient. All actual moving normalization,
shell-frame and reference derivatives are retained in these cancellations.

Only eight incoming momenta occur in the remaining Schur expression.
Vertices are polynomial in q; inverse denominators are
`nu²(q²+/-2p2q)`. Therefore this expression is rational for all
sufficiently large odd q,
with finitely many poles, for the fixed base preparation. Coherent shell
entries can contribute at isolated small q where two vertices transfer
+/-2q between incoming shell points (q=1 on this first shell). Those
finitely many terms are retained; they do not change the asymptotic
argument. Local Delta_2 seagulls in H+J are polynomials; matter seagulls
are polynomial beyond the same finite coherent exceptions: the actual
proper-link coefficient is a
finite-order local differential expression tested against fixed background
weights. None can cancel the superexponential tail (10).

Hence S2 after this actual amplitude elimination still has a nonrational
transverse quadratic multiplier. This is partial amplitude elimination,
not a solution of all field equations or a revival of an excluded common
cone branch. General higher shells with nonscalar Delta_2,flat, an
infinite-spectrum preparation, or a different retained field section are
outside this preparation statement. The H+J form factor (8) itself does
not depend on those extra preparation choices.

## 6. Consequence for the GR route

A fixed finite-order local metric action, including EH+Lambda, has a
polynomial Fourier Hessian on this constant background. The same actual
first-shell matter source or its stationary, eventually rational Schur correction
does not repair the nonrational thermal coefficient above. A single-mode
EH match therefore cannot identify the full unchanged coefficient.

For the present programme, a native derivation must supply its complete
observer/archive/clock law or a different justified limiting regime.
The existing fixed-positive-Mz small-beta stationary obstruction remains
in force; no running coupling or extra stress has been fitted here.
This theorem neither rules out another physically forced programme nor
excludes special on-shell coincidences, a nonlocal retained sector,
non-finite-shell matter or an original fixed-source terminal.

The adjacent bounded helper checks the actual full16 vertex, global-Z
combined weight, exact index-shift boundaries and all-order prefactor
identity. Infinite-moment growth, nonrationality and (11) are analytic
arguments stated above, not purported outputs of finite tests.
