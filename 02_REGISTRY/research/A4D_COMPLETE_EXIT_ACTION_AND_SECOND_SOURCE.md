# Complete exit operator → unchanged action and full second source

17 October 2026. Same Draft #334. Input checkpoint
`729db01f8d175a1a94cd8abdeb56cf45cfa9cbf2`. Consumer: the complete
retained-history/action-source morphism after the
[rare-output boundary](A4D_FULL_RARE_HISTORY_GAUGE_SPAN_BOUNDARY.md).
The [literal instrument](A4D_RETAINED_HISTORY_CAUSAL_SOURCE.md),
[same-price unfolding](A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md)
and [action-selection owner](sources/d0_native_action_selection_2026-10-16/RESULT_RU.md)
are inputs, not new physical assumptions.

**Constructive result.** The complete first-exit **operator**, actual clock
and actual preparation determine the entire supplied v8 price, with an
explicit inverse and unique operator source. The 13 ordinary rows and
the rare block have a complete noncommuting second-source balance. Their
redistribution does not create an independent term in that price.

The inverse is well-conditioned on a fixed energy block but loses uniform
control on UV modes. An exact flat full 16-component example proves that the rare
smooth-preparation h^-2 limit diverges for uniform heat preparation.
Consequently separate rare/ordinary smooth limits must not be traced to
obtain H+J: combine the actual finite operators first.

This closes an operator action/source interface for the **given** programme.
It does not select physical Cost−Info, implement tomography, identify all
physical fields with their readout, or prove the Einstein/refinement target.

## 1. Actual complete history and the exact ordinary complement

Let `A_blk=hD_h/16`, `alpha=p^2 h^2/128`, `B=I-2p^2 A_blk^2=I-alpha Delta_h`.
The complete blank amplitude for one Julia/golden round is B. For **n
actual rounds**, blank amplitude is `B^n` and blank probability operator
is `K=B^(2n)`. Thus `m=2n`, `beta=m alpha`. It is not m Julia rounds.

For the 32 even-duplicate row/coefficient blocks
`N_kappa=Q_(blank;kappa)`, row unitarity gives
`sum_kappa N_kappa N_kappa*=I`, with `N_blank=A_blk`.
There are 18 nonblank zero-N0 rows, 13 nonzero-N0 rows and one blank row;
the other duplicate outputs are identically dark. Put
`R_r=sum_(18 rare rows) N_kappa N_kappa*`.

The canonical rare projector retains both ports of those 18 rows and
the separate blank-label/port1 exit. The ordinary complement retains both
ports of the 13 other rows (and the irrelevant dark outputs). Exactly,

```text
E_r=4p^2 A_blk* R_r A_blk+4p^3 A_blk^4,
E_o=4p^2 A_blk* (I-A_blk^2-R_r) A_blk,
E_o+E_r=I-B^2.                                       (1)
```

The last identity uses `p+p^2=1`. In particular the blank/port1 term is
not assigned the nonblank two-port coefficient. For the disjoint retained
first-exit observables, with every later outcome unrestricted,

```text
F_r=sum_(j=0)^(n-1) B^j E_r B^j,
F_o=sum_(j=0)^(n-1) B^j E_o B^j,
E:=F_o+F_r=I-B^(2n)=I-K.                              (2)
```

This uses the actual unmeasured history, without a reset. The exact
complement is a statement about the canonical partition; an arbitrary
weighted coherent rare detector is not substituted for its projector.

One useful closed contribution, on the full carrier, is

```text
F_blank,port1=(alpha/p) Delta_h (I-K)(2I-alpha Delta_h)^-1,
h^-2 F_blank,port1 -> (p/256) Delta_0(I-exp(-beta Delta_0)). (3)
```

The displayed leading h^-2 limit has zero cone derivative on the
fixed-positive-G LC graph because Delta_0 is fixed there. The finite
effect can still vary through Delta_1/Delta_2; general scale and metric
sources must be retained.

## 2. Explicit action quotient and inverse

On the actual positive window `b0 I<=B<=I`, the positive root is unique:

```text
K=I-E, B=K^(1/m), Delta=(I-K^(1/m))/alpha,
Z=Tr K, Q_fb=I-zE,
S_v8(E,rho)=Tr(rho Delta)+log(C Z)/beta-M Tr log Q_fb.  (4)
```

Here rho is the normalized **actual matter** preparation, not an auxiliary
Gibbs state or uniform heat input. All site/form/reference components
remain. Formula (4) is the same price as before, not a replacement action.
At fixed clock and calibration it factors through E and rho: internal
details invisible to both cannot change that action. This is an action
quotient, not equality of the programme's complete future-test signatures.
Different D with the same Delta need not be operationally equivalent.

The forward derivative on Hermitian Delta is

```text
T_B[V]=D_Delta E[V]=alpha sum_(j=0)^(m-1) B^j V B^(m-1-j). (5)
```

In a B eigenbasis its Hilbert–Schmidt multipliers are
`t_ij=alpha sum_(k=0)^(m-1) b_i^k b_j^(m-1-k)`. They lie in
`[beta b_min^(m-1), beta]`. Thus T_B is invertible, selfadjoint and
positive on the entire Hermitian operator space, with sharp inverse norm
`1/(beta b_min^(m-1))`. No detector eigenbasis oracle is assumed: this
basis is used only to prove the invariant operator statement.

On an energy block `Delta<=Lambda`, with `alpha Lambda<1`,

```text
||T_B^-1||_HS <= 1/[beta(1-alpha Lambda)^(m-1)]
              <= exp[beta Lambda/(1-alpha Lambda)]/beta. (6)
```

The first bound tends to `exp(beta Lambda)/beta` at fixed beta as
alpha→0; this continuum expression is not a universal finite-clock bound.
The estimate does not discard the rest of the carrier or control all
physical field variations: it is an explicitly bounded readout block.
Across the full grid, b_min can stay below 1 while m grows as h^-2, and
the inverse grows exponentially. Finite injectivity is not uniform
continuum tomography or the original all10 raw response estimate.

## 3. Unique operator covector, without assuming [rho,B]=0

Let `f(K)=K^(1/m)`. Its Fréchet derivative is selfadjoint in the HS
pairing. At fixed alpha,m,C,z,M, the complete E-source is

```text
G_E=(1/alpha) Df_K[rho]+M z Q_fb^-1-I/(beta Z),
dS=Tr(G_E dE)+Tr(Delta d rho).                        (7)
```

The first term has a **positive** root derivative because `dK=-dE`.
Composing (7) with (5) gives exactly the previous source

```text
T_B[G_E]=rho-B^(m-1)/Z+M beta z B^(m-1)Q_fb^-1.        (8)
```

No commutation of rho with B is needed. This is a genuine finite operator
readout/source construction in place of an arbitrary postulated
`H(V)` or an injectivity assumption on all internal state coordinates.
It does not make the physical field→Delta map injective or its admitted
metric variation image full rank.

For moving calibration at fixed integer m, E-coordinates give additionally

```text
dS=Tr(G_E dE)+Tr(Delta d rho)-R dalpha/alpha
   +(dlog C)/beta-log(CZ) dbeta/beta^2
   -Tr(log Q_fb)dM+M Tr(Q_fb^-1 E) dz,
dbeta=m dalpha.                                      (9)
```

Actual discrete n and reference counts are not differentiated as continuous
fields. When rho=Sigma/Tr Sigma, its source is
`Tr[(Delta-R I)dSigma]/Tr Sigma`. No preparation or clock derivative is
silently frozen. Uniform operator reconstruction is a mathematical
interface; measuring a scalar first-exit probability on one state does
not supply the whole E matrix.

## 4. Full noncommuting second-source balance

For `P_N(B)=B^N`, keep the ordered derivatives

```text
DP_N[U]=sum_(a+b=N-1) B^a U B^b,
D2P_N[U,V]=sum_(a+b+c=N-2)
 [B^a U B^b V B^c+B^a V B^b U B^c].                   (10)
```

On two genuine field directions i,j,
`B_i=-alpha Delta_i-alpha_i Delta` and
`B_ij=-alpha Delta_ij-alpha_i Delta_j-alpha_j Delta_i-alpha_ij Delta`.
Use `P_N,ij=DP_N[B_ij]+D2P_N[B_i,B_j]`. Consequently

```text
F_o,ij=-K_ij-F_r,ij.                                 (11)
```

For F_r, differentiating `B^j E_r B^j` gives all nine ordered second
product terms. A root's mixed derivative obeys
`L L_ij+L_ij L=-(PP*)_ij-L_i L_j-L_j L_i`; its RHS retains both ordered
`P_i P_j*` terms and the true second operator jet. The right root is
analogous. Thus the aggregate ordinary source is determined without
replaying thirteen separate root calculations, but its actual second
stencil jet is not inferred from a positive first-jet Gram.

For any of these effects, `q=Tr(Sigma F)/N`, `N=Tr Sigma`,

```text
q_ij=[Tr(Sigma_ij F+Sigma_i F_j+Sigma_j F_i+Sigma F_ij)
      -q N_ij-q_i N_j-q_j N_i]/N.                    (12)
```

This preserves the moving normalizer and all preparation components.

For the H+J part of the same price, at fixed calibration let
`V_E=M z Q_fb^-1-I/(beta Z)`. Its full second source is

```text
(H+J)_ij=Tr(V_E E_ij)
 -Tr(E_i)Tr(E_j)/(beta Z^2)
 +M z^2 Tr(Q_fb^-1 E_i Q_fb^-1 E_j).                  (13)
```

Matter contributes its actual normalized second derivative of R. If
using the E-coordinate formula (4), this includes
`Delta_ij=[Df_K[E_ij]-D2f_K[E_i,E_j]]/alpha`, plus clock terms when
alpha moves. Moving beta,z,M,C also differentiate their displayed scalar
factors in (9). The negative global heat-normalizer term in (13), the
feedback term and E_ij are essential. The whole source is not a fixed
positive detector on separately priced rare/ordinary outputs.

## 5. Actual h^2 coefficient and the ordinary contribution

Under the owned controlled smooth heat/history hypotheses, write
`Delta_h=Delta_0+h Delta_1+h^2 Delta_2+...`, where
`Delta_1={D0,D1}`, `Delta_2=D1^2+{D0,D2}`. D2 is the actual proper-link
and true-adjoint stencil coefficient. Let `H_t=exp(-t Delta_0)` and

```text
J_b[V]=integral_0^b H_(b-t) V H_t dt,
T_b[V,V]=integral_(0<s<t<b) H_(b-t) V H_(t-s) V H_s ds dt.
```

Keep the actual `beta_h=2n_h alpha_h`, `alpha_h=c0 h^2`; no convergence of
the integer-rounding coefficient is presumed. Then, in the declared smooth
matrix elements/source testing rather than UV operator norm,

```text
E_h=I-H_beta_h+h J_beta_h[Delta_1]
 +h^2{J_beta_h[Delta_2]-T_beta_h[Delta_1,Delta_1]
       +(beta_h c0/2)H_beta_h Delta_0^2}+o(h^2).       (14)
```

The simplex integral already supplies the commuting factor1/2. The last
term is the actual finite-clock correction from log B. It is not zero
under general scale/metric variation. If beta_h is instead expanded
around a fixed beta, its actual rounding terms must also be retained.

If `F_r,h=h^2 L_r+o(h^2)` with the corresponding smooth source remainder,
the ordinary h^2 effect coefficient is exactly the braces in (14)
**minus L_r**. The rare contribution cancels back in E_h. It is not an
extra Einstein source added to the original action. For the normalized **exit probability**, preparation coefficients give
`Tr(rho_0 E_2+rho_1 E_1+rho_2 E_0)` before differentiation. The actual
matter price uses Delta, as in (14a), not the exit effect.

### The complete h² price coefficient, before any rare split

There is also an explicit consuming formula. Under the owned **combined**
trace/source remainder hypotheses, put

```text
K0=H_beta, K1=-J_beta[Delta_1],
K2=-J_beta[Delta_2]+T_beta[Delta_1,Delta_1]
    -(beta c0/2)H_beta Delta_0^2,
Zi=Tr Ki, Q0=(1-z)I+zK0.
```

For fixed field calibration, retain the exact field-independent
`log(C_h)/beta_h` (and the dimension term below) in the price. These can
diverge as h→0, since the actual workspace includes 128^n. The h²
coefficient of the remaining **field-dependent** part is

```text
S2=Tr(rho_0 Delta_2+rho_1 Delta_1+rho_2 Delta_0)
   +(Z2/Z0-Z1^2/(2Z0^2))/beta
   -M z Tr(Q0^-1 K2)
   +(M z^2/2)Tr(Q0^-1 K1 Q0^-1 K1).                 (14a)
```

If the rounding coefficient has not been fixed, every beta in K_i,Z_i,
Q0 and 1/beta in (14a) means the actual beta_h. An expansion about a fixed
beta requires its rounding terms. This does not assert a finite Taylor
expansion for the full price including its workspace constant.

Here rho_i are coefficients, not i-th derivatives; every normalizer in
rho=Sigma/Tr Sigma must be expanded. The ordered K1 pair cannot be replaced
by a scalar variance. Formula (14a) is a coefficient identity, and its
field source requires the same controlled derivative remainder. It is
not justified by smooth matrix elements alone.

For 0<z<1 the feedback factorization is exact on every finite carrier of
dimension d:

```text
J=-M d log(1-z)-M Tr log[I+zK/(1-z)].                (14b)
```

The second term has smoothing field derivatives on the controlled compact
heat domain. The first term is field-independent only at fixed d,z,M.
It is kept when calibration moves. This is algebraic separation, not an
added counterterm, renormalization prescription or physical clock law.
Thus (14a) consumes the actual Delta_2 and both ordered Delta_1 insertions
without separately tracing a divergent rare coefficient. A rare/ordinary
redistribution at fixed K,rho and calibration cannot change S2.

## 6. Exact UV separation of the two preparations

This separation is necessary, not a hypothetical regularity warning.
On the actual flat torus stencil with C_r=nu c_r, every Fourier block has

```text
Delta_h(k)=lambda_h(k) I16,
r=h^2 lambda_h=4nu^2 sum_r sin^2(k_r/2),
D_chi,h(k)^2=Delta_h(k) for every role character.
```

For any one existing nonblank role character/coefficient0, the exact
two-port first-exit probability operator in that block is

```text
F_chi,n(k)= r[1-(1-c0 r)^(2n)]/[256(1-c0 r/2)] I16,
c0=p^2/128.                                         (15)
```

On a fixed occupied smooth momentum it is O(h^2), with the owned finite
h^-2 limit. On the **same programme with uniform preparation I/d**,
take L=4ell and Fourier patch `k_1 in [pi/2,3pi/2)`. Its exact fraction
is1/2 and r>=2nu^2. For large enough n, for example
`4n c0 nu^2>=1`, the survival power is below 1/2. Hence

```text
Tr[(I/d)F_chi,n] >= nu^2/512,
h^-2 Tr[(I/d)F_chi,n] -> +infinity.                   (16)
```

The smooth faithful-shell limit therefore cannot be promoted to the
uniform heat preparation used to represent `Z/d`. In particular,
separate continuum traces of L_r and its ordinary complement need not
exist. Combine finite E=I-K **before** taking heat traces and use the
owned weighted heat/source estimate on the combined K. This preserves
the global Z term and all UV modes rather than discarding them.

## 7. Physical consumer and remaining work

This supplies the complete operator-level history→given-action map and
its second sources, including the aggregate ordinary block. It answers
neither physical ensemble selection nor admission of an operator-tomographic
readout. A single prepared probability is not E; the faithful shell is
not I/d; `det(I-zE)` remains the separately constructed quasi-free blank
probability, not a probability of the ordinary 128-outcome tape.

The original native branch code fixes pathwise information only with its
specified probability/reference bindings. No complete code cost/reference
or ensemble law for the whole Julia/controller/coefficient tape is derived
by (1)–(16). The physical consumer is still the same-process Cost−Info
source identity on actual admitted field/preparation/clock variations.

Next use the actual Delta_2 and ordered Delta_1 pair with that full price;
do not infer them from the rare Gram or take separate divergent traces.
No physical action term, source, preparation, reset or scale law is added.
Nonflat joint stationarity, nonlinear all10 Einstein equality and the
original fixed-g/tau/raw h^-2/#216 terminal remain open.

Adjacent bounded helpers check new complete finite Julia/source jets,
operator readout/inverse and the flat full16 UV control. Old root, spectral
and Lean entrypoints are not executed; previous results remain immutable.

Evidence: [new complete-instrument/source control](sources/d0_complete_exit_source_2026-10-17/RESULTS.json)
and [positive inverse/flat-UV control](sources/d0_complete_exit_source_2026-10-17/INVERSE_UV_RESULTS.json),
with [input-pinned local validation](sources/d0_complete_exit_source_2026-10-17/VALIDATION.json).
Only these new bounded calculations were run, normally and with optimization;
the outputs are identical. Embedded negative controls reject commutation,
reset, preparation/trace substitution and dropped normalizer/calibration
terms. The general analytic/source claims retain their stated hypotheses.
