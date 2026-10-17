# Actual spatial preparation: existence, lattice minimizers and full weak source

17 October 2026. Same Draft #334, input `2b5bd2af3348d5c49937413580878ed046a460cb`.
Consumer: the complete native price/source must use its actual preparation
equation before comparison with the reconstructed Einstein covector.
The [shell preparation theorem](A4D_COMPLETE_RECORD_PREPARATION_DESCENT.md)
does not supply compactness of unknown spatial minimizers. This proof removes
that premise for the declared port-dominated coherent candidate below.
It uses the [actual variable process](A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md),
[whole-grid energy estimates](A4D_VARIABLE_RECORD_ENTROPY_AND_CODE_LIMIT.md)
and [logarithmic source bounds](A4D_VARIABLE_RECORD_FIRST_SOURCE_LIMIT.md).
It introduces no physical code, Info, admission rule or action term.

**Result.** At fixed positive record time, actual port cost controls the
initial preparation energy, whereas coherent entropy grows logarithmically.
The declared full-spatial functional therefore has a minimizer with exactly
the existing reference128 carrier. Actual grid minima converge, and every
cluster point of actual grid minimizers is a continuum minimizer. The full
weak preparation equation and finite-grid minimized field sources are derived
without a faithful-rank restriction. Higher regularity of these minimizers,
their limiting geometric envelope and physical selection remain separate.

## 1. Same process and precise conditional price

Fix one uniformly smooth compact field chart from the input owners: real
nondegenerate coframe, strict Julia bounds, proper Lorentz links, actual
observer/density trivialization and all 16 exterior components. The finite
round is exactly Phi_h=Id+epsilon_h L_h, epsilon_h=p^2 h^2/64,
p+p^2=1, Delta_h=D_h^2; n_h epsilon_h=T_h -> T>0. Use the entire spatial
torus H=L2(T4;C16), with G=I-sum partial_r^2. Constants are uniform on
that chart and on compact positive time intervals, not over arbitrary
physical fields or T down to zero.

A pure normalized actual preparation is an amplitude

```text
C : C128_ref -> H,  ||C||HS=1,
Psi_C=vec(C),  rho0=C C*,  E(C)=Tr C* G C.
```

All 128 reference columns and all 16 form components are variable. The
data density has rank <=128, as required by this actual purifier. Optimizing
over all data densities would change the carrier. Rank births are allowed;
rank128/faithfulness is not imposed. No reference unitary or invisible
coherence is discarded as a physical gauge.

Supply a fixed additive per-round code in **natural-log units**. Let g_0
be its blank/port0 price, and c_alpha=g_alpha-g_0 the 127 relative prices.
The sufficient hypothesis used here is

```text
c_alpha >= log(phi) 1_{port1}(alpha)  for every nonblank alpha.    (1)
```

This is the original golden port code plus nonnegative EXTRA RELATIVE
branch prices. An inequality on raw g_alpha alone does not imply (1) if
g_0 also increases. No such complete code is derived physically here.
The original port part is exact, including blank-label/port1:

```text
A_port,h = p log(phi) Delta_h,
A_c,h = sum_alpha c_alpha ell_alpha,h* ell_alpha,h >= A_port,h.
```

The ell_alpha,h are the literal physical nonblank maps rescaled by
sqrt(epsilon_h), not an analytical recombination of the tape. The special
blank-label/port1 map is -sqrt(p) h Delta_h/16. It tends to zero on
smooth inputs, but is retained at finite h.

Let rho_h,j=Phi_h^j(C_h C_h*). Write the actual expected code as
n_h g_0+q_h(C_h), where

```text
q_h(C_h)=epsilon_h sum_(j<n_h) Tr A_c,h rho_h,j.
Sigma_h,C=(Phi_h^n_h tensor Id128)|Psi_C><Psi_C|,
F_h(C)=q_h(C)-eta S(Sigma_h,C).                            (2)
```

Eta is a specified finite real coefficient; eta=1 is the coherent
relative-entropy candidate in these units. Neither its sign nor its
physical Info interpretation is selected by this proof. Because the
actual total state is pure and every record is retained, S(Sigma_h,C)
equals the complete coherent-record entropy, not pointer Shannon entropy.

For the owned continuum channel P_t set

```text
q(C)=integral_0^T Tr A_c P_t(C C*)dt,
Sigma_C=(P_T tensor Id128)|Psi_C><Psi_C|,
F(C)=q(C)-eta S(Sigma_C).                                 (3)
```

The explicit n_h g_0 baseline has no preparation derivative. Its actual
field/clock/calibration derivative must be returned when those vary.
Equations (2),(3) do not replace the registered H+J+R price or identify
its ensemble/workspace terms with this supplied candidate.

## 2. Lower energy propagation, not just an upper Lyapunov bound

The energy owner constructs H_h with Lambda_h=I+Delta_h,
Lambda_h <= H_h <= c0 Lambda_h. Its proof gives a symmetric order-2
remainder for L_h*H_h. The absolute form estimate of its Section2
therefore gives the stronger two-sided inequality

```text
-c H_h <= L_h*H_h <= c H_h.                              (4)
```

No cancellation of the bare cubic defect is assumed: H_h is the same
auxiliary corrected energy, not a change in the physical cost Delta_h.
For sufficiently fine h, c epsilon_h<1. Complete positivity and the exact
Euler identity iterate (4) to

```text
(1-c epsilon_h)^j H_h <= (Phi_h*)^j H_h
                         <=(1+c epsilon_h)^j H_h.
```

Consequently, for every normalized input, including actual minimizers,

```text
epsilon_h sum_(j<n_h) Tr Delta_h rho_h,j
 >= [1-(1-c epsilon_h)^n_h]/(c c0) Tr H_h rho_h,0 - T_h. (5)
```

At c=0 the quotient is T_h/c0. Uniform ellipticity identifies the
initial H_h form with the full Fourier H1 energy. Since T>0, (5)
is at least a_T E_h(C_h)-b_T, with a_T>0 independent of h.

The continuum analogue follows first for smooth finite-rank inputs
from the already proved actual cost limit:

```text
integral_0^T Tr Delta rho_t dt
 >= (1-exp(-cT))/(c c0) Tr H rho0 - T.                   (6)
```

To extend it to EVERY finite-energy input, use smooth density in the
weighted trace class S1,1 and bounded propagation there, established by
the moment/source owners. The integrated energy form is continuous in
that norm. Lower semicontinuity by itself would have the wrong direction
for this extension. Both (5) and (6) give q >= a_T E-b_T by (1).

## 3. Closed cost form and entropy continuity on energy balls

The upper energy estimate and the finite relative code weights give
q(C)<=b_T E(C); the same upper bound holds uniformly on the grid.
For clarity, closedness does not assume an unproved operator formula
for the backward channel on an unbounded observable.

Let Q_N be increasing smooth finite Fourier projections on OUTPUT data.
For each nonzero limiting physical jump ell_alpha, define the bounded
positive operator

```text
A_c,N=sum_alpha c_alpha ell_alpha* Q_N ell_alpha.
```

It is bounded because ell_alpha* Q_N has finite-dimensional smooth
range. A_c,N increases as a quadratic form to A_c. Thus

```text
q(C)=sup_N integral_0^T Tr A_c,N P_t(C C*)dt             (7)
```

is a supremum of continuous nonnegative quadratic forms in C. Here (7)
is used on the declared H1 domain. On that domain q+K||C||HS^2 has a
norm equivalent to H1 for large fixed K, so the restriction is a closed
positive form. Extended by infinity outside H1 it is lower semicontinuous
in HS: a bounded-cost strongly converging sequence is bounded in H1 by
(6); its weak H1 limit is identified by the HS limit, and the positive
cutoffs give the cost liminf. This does not assert that the maximal
unrestricted output-cutoff form has no additional finite-cost L2 vectors;
no such larger preparation domain is used. Denote the associated
selfadjoint operator of this closed H1 restriction by K_T, acting on all
128 columns. This notation is the ACTUAL integrated code form, not a
new preparation Hamiltonian or replacement action.

The owned first-moment propagation bounds the final system/reference
energy by C_T E(C). Its counting function has growth O(R^2), with fixed
16*128 multiplicity. Therefore

```text
0 <= S(Sigma_C) <= C_T+2 log(1+E(C)).                    (8)
```

On each initial-energy ball, HS convergence of amplitudes gives trace
convergence of the actual initial pure states, then of their outputs.
The energy-constrained entropy continuity bound used by the input owner
therefore gives convergence of S(Sigma_C). This holds with the actual
reference128; no infinite auxiliary purifier has been introduced.

## 4. Existence of a full spatial optimal preparation

From (5),(6),(8), uniformly on the grid and in the continuum,

```text
F(C) >= a_T E(C)-b_T-2 max(eta,0) log(1+E(C)).           (9)
```

This tends to infinity with E. A fixed smooth normalized comparison
amplitude gives a uniform finite upper bound for the infima. Hence a
uniform initial first-energy bound for minimizers is a CONCLUSION of
the actual port/code law, not an assumed moment bound on an unknown
preparation.

For the continuum direct method, take a minimizing sequence. Its 128
columns are bounded in H1, so a subsequence converges weakly in H1 and
strongly in HS by Rellich on T4. Normalization is retained. The limit
has finite energy; (7) gives cost liminf and (8) gives entropy continuity.
It therefore minimizes F. Finite-grid minimizers exist by compactness
of their normalized finite-dimensional amplitude sphere.

This theorem is on the normalized finite-energy amplitude domain,
closed under energy-bounded HS limits. Rank<=128 survives. An open
faithful-rank128, timelike, or primitive-reachability restriction is
not covered automatically; a physically admitted subset would need its
own closure and recovery proof. There is no claimed uniqueness, uniform
spatial Hessian, fixed support or interior preparation.

## 5. Gamma limit of actual grid optima

Embed grid amplitudes by the exact Fourier isometries and set F_h=+infinity
outside their normalized grid domain. We prove Gamma convergence in the
strong HS topology, with equicoercivity from (9).

**Liminf.** Let C_h -> C in HS and suppose liminf F_h(C_h) is finite.
After choosing that subsequence, (9) bounds the initial first energies.
The actual trajectory theorem gives trace convergence of outputs and
(8) gives their entropy convergence. It remains to prove the cost liminf
without pretending that compression of a positive operator decreases it.

Use OUTPUT cutoffs, not P_N A_c,h P_N. For fixed N, let Q_N,h be the
sampled finite Fourier output projection. Positivity of every relative
c_alpha gives

```text
A_c,h >= A_c,N,h=sum_alpha c_alpha ell_alpha,h* Q_N,h ell_alpha,h.
```

Adjoint consistency on the fixed smooth finite-dimensional range gives
operator-norm convergence of the embedded A_c,N,h to A_c,N. The special
h Delta_h row converges to zero there by moving its adjoint to those
smooth output tests. Actual trajectory convergence and uniform boundedness
of these cutoff operators give convergence of their time sums to the
integral in (7). Thus liminf q_h(C_h)>=q_N(C) for every N; increase N
to obtain liminf q_h>=q(C). Noncommuting input compression need satisfy
no inequality. This also proves the limiting amplitude lies in H1.

**Recovery.** For any normalized H1 amplitude C, smooth finite Fourier
truncations followed by normalization converge in H1. The closed cost
form is H1-continuous, and entropy is continuous on the resulting energy
ball, so F(C^N)->F(C). For each FIXED N, actual sampled amplitudes have
all the moments required by the existing code-value theorem; their
grid values converge to F(C^N). Choose N=N(h) increasing sufficiently
slowly by a diagonal argument. No unrestricted projection of a general
H1 amplitude is asserted to satisfy a second-moment bound uniformly.

Equicoercivity, liminf and recovery imply

```text
min F_h -> min F,
every HS cluster point of actual minimizers C_h minimizes F.      (10)
```

Equivalently, their distance to the continuum minimizer set tends to
zero. This is convergence of actual optimal preparations in the declared
domain, not just a value theorem for a supplied preparation, and not
uniqueness or convergence of their field derivatives.

## 6. Full preparation Euler equation through rank births

Fix geometry and let V_T be a Stinespring isometry of the actual retained
process, tensor the EXISTING reference128. For Psi=V_T vec(C), the
input owner's energy/Renyi estimate gives

```text
||[(log Sigma_C-log(Sigma_C+zI)) tensor I_record]Psi||
                                                <=C_E z^(1/8).
```

Thus the vector

```text
B_C=vec^-1 V_T*[(log Sigma_C) tensor I_record]V_T vec(C)          (11)
```

exists in HS; log0 acts as zero on the purifying vector. Regularized
versions converge uniformly on energy balls and are continuous there.
For any H1 preparation germ, V_T is fixed and its tangent is simply
V_T vec(delta C), a bounded Hilbert vector. The fundamental-theorem
regularization argument of the source owner therefore proves

```text
d S(Sigma_C)[delta C]=-2 Re <B_C,delta C>HS,
                      Re <C,delta C>HS=0.               (12)
```

Only the first moment is needed for THIS preparation derivative:
no unbounded field derivative of V_T is being taken. At every minimizer,
all 128 column variations, including rank-birth directions, give

```text
K_T C + eta B_C = F(C) C,                               (13)
```

first as a weak H1 form equation. The multiplier is F(C), since
<C,B_C>=Tr Sigma_C log Sigma_C=-S(Sigma_C).
Because B_C and C are Hilbert vectors, (13) implies C belongs to D(K_T).
No physical matter row has been dropped by setting an off-shell R
constant, pinching the density or choosing one reference column.

## 7. Minimized field sources: exact finite grid and the remaining limit

At every fixed h and locally fixed integer n, the actual finite tape
isometry is smooth in the full native fields. Its coherent entropy is
C1 through rank births by the same purification/log argument. On the
compact finite-grid minimizer set M_h, the one-sided derivatives of the
minimized value in ANY admitted field direction X are therefore

```text
D_+ min_C F_h[X]=min_(C in M_h) partial_X F_h(C),
D_- min_C F_h[X]=max_(C in M_h) partial_X F_h(C).          (14)
```

The derivative is the exact code expectation derivative minus eta times
the actual coherent-entropy derivative. The preparation term vanishes
by (13); observer, density, normalization, proper-link and clock jets
do not. The full price adds the actual derivative of n g_0 and of any
specified other terms. Equation (14) retains every permitted native
field row. It does not enlarge the restricted stored metric image into
all ten ambient metric directions. Even at finite h, nonunique optima
can produce distinct sources, so a single covector requires their
agreement or a unique retained branch.

For passage of these sources to the continuum, the present theorem
gives moment1 and membership in D(K_T). The existing geometric-source
theorem requires moment3 for state/coherent entropy and moment4 for
code. FORM comparability K_T+K ~ G does not identify D(K_T) with H2,
let alone give H3/H4. A regularity theorem for this actual integrated
code operator, or a direct extension of the field source to the energy
domain, is still needed. With such uniform source continuity, (10)
supplies the missing compactness for the continuum version of (14).
Gamma convergence alone does not differentiate minima.

## 8. Decisive geometric consumer: preparation cannot restore an invisible cone

The previous causal/source owner proves blindness of the spectral H+J+R
continuum reading. We now test the stronger possibility that the actual
complete coherent record, or solving its FULL SPATIAL preparation equation,
restores the missing geometric source. On the following whole family the
answer is negative for the declared unscaled continuum price, by an exact
operator identity rather than a one-direction fit or finite spectrum.

Use the owned period-2pi torus family, with fixed normalized coordinate
measure, e_theta=s O01(theta(y)), n=e0, s>1, and actual proper links
sampling omega_LC(e_theta). Here G=s^2 I, coordinate torsion is zero,
and mu=dV_G is constant in theta. Choose s large enough for the strict
Julia chart on each bounded smooth family. Use the existing full16
coordinate-form isometry U_e and the constant positive G-trivialization.
They act as identity on the same reference128. Then

```text
U_e D_theta U_e^-1 = D0 = s^-1 sum_r gamma_r partial_r,
U_e C_r,theta U_e^-1 = c_r/s.                            (15)
```

The second identity is essential: equality of D alone would NOT prove
equality of the actual record. Every limiting labelled row N_k,0 is the
same fixed Walsh combination of C_r, C_r*, sqrt(I-C_r C_r*) and
sqrt(I-C_r* C_r); see the variable-process owner Section2. Isometry
commutes with true adjoints and their positive square roots. Thus EACH
N_k,0 becomes the same theta-independent matrix in (15), in the original
record-label basis. No field-dependent environment rotation is used.
Every literal limiting port jump ell_alpha and the no-jump semigroup
exp(-t Delta0/2) are consequently theta-independent.

The actual trajectory construction composes precisely these labelled
jumps and no-jump factors on its common waiting-time cubes. It follows
that the entire limiting continuous-jump Stinespring isometry is the
same on this family, not just the summed marginal generator. In
particular, for every fixed coordinate-form amplitude C,

```text
q_theta(C)=q_0(C),  S(Sigma_theta,C)=S(Sigma_0,C),
F_theta(C)=F_0(C).                                      (16)
```

The normalized reference128 energy domain itself is unchanged by the
isometry. This is the full declared amplitude class with independent
observer n=e0. An additional observer=current law or primitive-reachability
subset would require its own invariance proof, as in Section4; it is not
inferred from reference rank. Hence (16) holds after minimizing over ALL its spatial
preparations, including every grade and possible rank:

```text
min_C F_theta(C)=min_C F_0(C),
M_theta=U_e^-1 M_0 in native coordinates.                 (17)
```

The existence theorem above makes M_0 nonempty. Neither a unique
minimum nor H3/H4 regularity is required for this conclusion, because
the entire functional and its domain coincide. More generally, every
smooth preparation-critical branch of the SAME objective has zero
theta-source by the chain rule and (13), even if it is not minimizing.
A deliberately nonstationary preparation may add a source; it would
not solve that retained equation. Nonminimal critical branches are
not excluded by the minimizer theorem.

The independently owned Lorentz metric is g_theta=e_theta^T eta e_theta.
It is not constant or a Lorentz frame gauge. The causal/source owner
Section4 gives, in the same coordinate-volume convention,

```text
I_EH[theta]=-2 s^2 integral (theta')^2 dx,
I_EH[a f]=-2 s^2 a^2 integral (f')^2 dx,
d/da I_EH[a f]=-4 s^2 a integral (f')^2 dx !=0            (18)
```

for nonconstant smooth periodic f and a!=0. The volume is independent
of a. The actual native Rayleigh matter price for any fixed C is also
theta-independent, since its operator is Delta0. On a prep-critical
branch of F the full F derivative includes the transported preparation
term; its contribution to (17) vanishes by (13), rather than by freezing
a raw amplitude. On the canonical transported branch with coordinate C
fixed, the Rayleigh price is constant directly. Equation (13) for F
does not eliminate the preparation derivative of a separately added R.
If the declared objective actually includes +kappa R with kappa>=0,
apply the same proof to that WHOLE objective: replace K_T by
K_T+kappa Delta0 in its form equation. Coercivity/compactness persist,
and the entire enlarged objective and its minimum still satisfy (16),(17).
The stationary equation used must always be that of the same total price.

Therefore the declared optimized continuum code/coherent price cannot
equal nonzero constant times this intrinsic EH source plus ONLY its
already specified theta-blind matter/volume/baseline terms. The mismatch
survives full spatial preparation elimination. It cannot be repaired by
proving a stronger preparation Hessian or by another scalar edge-jet
identification. Any additional physical matter/history term must be
derived independently; it cannot be defined as this residual.

This is not a finite-h history-blindness theorem. The retained-history
owner already proves a theta-dependent labelled event of order h^2.
The original task amplifies precisely such terms by h^-2. Thus (16),(17)
do not erase that event, exclude a properly derived rescaled price or
prove the original fixed-source terminal. Nor is the LC matrix family
automatically a joint root or physically primitive-admitted. The
positive-adjoint chart is larger than the restricted stored-adjoint
chart; the two variation domains are not interchanged.

The route is now sharper: unscaled fixed-code coherent preparation
cannot by itself restore this Lorentz source. The physical programme
must identify its actual retained comparison/history/clock contribution
and scale, with all equations. Geometry reconstructed from the coframe
supplies the target covector; it does not force that price contribution.

## 9. Consumed geometry and exact scope of this closure

The newly supplied coframe/weighted-edge text is byte-identical to
the already preserved [input](sources/d0_coframe_heat_source_2026-10-16/USER_INPUT_RU.txt),
SHA256 `ee36bd15a6c57cd393d297918086f07faf0c0dbd8dedcdc989c0536d55d38c61`.
Its request for complete work is retained. Its claimed scalar
edge-jet/contorsion equality is not a premise: the
[native coframe/source bridge](A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md),
Sections1,4, disproves both the linear inference and the claimed
quadratic Lorentz matching. No duplicate reconstruction is run here.

The result established here is the complete spatial variational block
(1)-(14), followed by its exact Lorentz-source consumer (15)-(18), for
the given process and conditional coherent/positive relative code class.
It supplies actual minimizers, their lattice limit and their full weak
equation to the current synthesis. Physical code/Info selection
and the complete retained price belong to the coordinated native lane;
neither a log-Sobolev guess nor an EH term is inserted to choose them.

The full target still needs the SAME admitted price and all retained
equations to produce the intrinsic Lorentz Einstein source with a
nonzero derived coupling, and a nonempty compatible refining joint
family. The original fixed nonconstant g, independent tau, all ten
packed metric rows, unweighted raw h^-2/#216 comparator terminal is
unchanged. Existence of a preparation minimum is not an Einstein
equation or existence of a joint field/observer/matter root.

This is an analytical proof using published owned estimates. No new
finite-spectrum/rank census, helper execution, old scientific replay,
Lean build or independent acceptance is claimed. Input pins and analytical
review are recorded in the [bounded intake](sources/d0_spatial_preparation_2026-10-17/README.md).
