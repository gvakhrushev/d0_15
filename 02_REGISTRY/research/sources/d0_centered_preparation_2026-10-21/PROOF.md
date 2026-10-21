# Exact joint elimination of the original coherent CAR preparation

21 October 2026. Supporting mathematical application within existing Draft
#334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`. Read source: `dfc0275e`.

## 1. The new parent substitution

The existing logarithmic reduction proves a unique preparation minimizer at
**fixed original material coordinates** and an explicit, generally nonzero
reduced field source. That statement remains correct. The missing joint
application is that the admitted mathematical preparation directions are
tangent to material coordinates that the SAME carrier already varies
independently. They must be used together when solving all equations.

On this original cap2 carrier, introduce the weighted centre of the two
material angles, without changing the instrument, price, selector, reference,
history, or physical gate inventory. The relative preparation source then
vanishes identically on the coincident-arm section. Its positive logarithmic
normal makes that section the **only** nearby relative stationary section.
Consequently:

* every nearby full joint critical point has coincident arms;
* the full joint critical set equals the critical set of the diagonal price;
* the already constructed fixed-material reduced price has exactly that same
  critical set, despite its nonzero off-shell logarithmic correction;
* local minima, strict local minima and decreasing directions of the diagonal
  price are preserved by the full preparation extension;
* the former mixed matrix is exactly `p^3` times selected rows of the
  diagonal material Hessian. It is not an independently adjustable source.

This removes the independent restricted preparation equations for THIS
specified complete coherent component and its genuine linear ledgers. It does
not identify this cap2 action with the distinct N=1 CQ action, solve the
diagonal field equations, select physical Book03 Info, or prove refinement
uniformity. The result is finite-chart and same-action.

The word "full" in the theorem quantifies over all geometric and original
scalar/top field variables in this declared chart, together with the selected
`k` independent `J_w` directions. It does not quantify over arbitrary
Stiefel preparations, other selectors, or an unspecified physical work ledger.

## 2. Exact original objects and price

Use the original 256-site, CAR16, oldRIGHT128 carrier of
`d0_native_logarithmic_source_reduction_2026-10-21/PROOF.md`, §§2–4.
Put `p=phi^-1`, `alpha=p`, `beta=p^2`; hence `alpha+beta=1`.
The geometric parameter `g` contains the independent coframes and proper
Lorentz links. The complete cap2 instrument depends on `g`, not on the
independently supplied material preparation:

```
L_gamma(g) in {K_eta(g), K_eta(g) B(g), B(g)^2 : eta != 0},
sum_gamma L_gamma^* L_gamma = I.
```

There are all 255 actual histories, including terminal abort and identically
dark leaves. Every active old RIGHT Gram is faithful on the inherited small
fixed-mesh chart. No new support floor or eigenvalue deletion is used.

At site `z`, the actual dictionary is

```
C_m(z,:) = [sqrt(p)|1> + c_z|0> + b_z|15>
             + sqrt(p^2-c_z^2-b_z^2)|14>] f(z)^T/sqrt(128),
C_m^* C_m = I_128/128.
```

For the same selected distinct interior sites `w`, retain the full rank-eight
CAR generators

```
J_w = sum_(j=6,10,12,14) (|w,j+1><w,j|-|w,j><w,j+1|),
U(a) = product_w exp(a_w J_w).
```

These operators keep all complements. Their other high-grade planes are
unoccupied in this supplied dictionary; the equality on this dictionary
below does not replace the full operators or alter their Book trace.

The actual two-arm mixed input and complete coherent conditional component
are

```
rho(g,m,a) = alpha C_m C_m^* + beta U(a)C_m C_m^*U(a)^*,
Theta_g(rho) = direct_sum_gamma L_gamma(g) rho L_gamma(g)^*,
A(g,m,a) = S_phi(Theta_g(rho)) - log_phi 128.
```

We also cover the already owned complete fixed-central-reference price

```
S(g,m,a) = A(g,m,a) - log_phi 2 + Tr[C_ledger(g) rho(g,m,a)],
C_ledger(g) = sum_gamma [c_gamma + log_phi mu_gamma] L_gamma^*L_gamma.
```

Here the positive complete `mu_gamma` and actual leaf costs `c_gamma` are the
ones supplied in `PRIMARY_STOPPED_PORT_PRICE_AND_PREPARATION_EULER.md`, §§4–5;
they are fixed under material/preparation variations. All source derivatives
in `g` remain. This is the exact identity for
`E[c_port]-D_phi(Omega_PYR || Tau_mu)`, with the same PR algebra and the
same central reference `Tau_mu=direct_sum mu_gamma I_256/256`.
The `-log_phi 2` selector-capacity term is retained, not erased or charged
twice.

In particular, for that owner's stated counting/port reference,

```
mu_(0^j eta) = 64^(-T) p^(c_port),
mu_abort = (p/64)^2,
C_ledger(g) = -log_phi 64 [I + B(g)^2],
S = A - log_phi 2 - log_phi 64 E[T].
```

For cap2, `E[T]=Tr[rho(I+B^2)]` counts every first round and every second
round reached through the actual first blank. It is the same stopped
process, not a fresh-input reset. The code identity has already canceled
the counted port cost once. We do not add a second copy.

Write `S_0(g,m)=S(g,m,0)`. This is the **diagonal restriction of the SAME
two-arm execution**, including its pure selector, capacity constant, old
RIGHT and supplied ledger. Its spectrum can be computed by the one-arm
formula. It is not a claim that the selector, its prefix, or its physical
work can be removed for free. For the entropy component alone use `S=A`,
`S_0=A_0`; every result below still holds.

## 3. The exact material-angle action

Keep each `c_w` independent, and set

```
r_w = sqrt(p^2-c_w^2),
b_w = r_w sin(theta_w),
slack_w = r_w cos(theta_w) > 0.
```

The strict slack chart makes this an analytic invertible coordinate change
in the original independently varied top amplitudes. Other material
coordinates are unchanged. The literal CAR rotation gives, exactly,

```
exp(a_w J_w) C_(c,theta) = C_(c,theta+a_w e_w),
J_w C_m = slack_w partial_(b_w) C_m.
```

The full oldRIGHT columns obey the equality because the same local CAR
identity multiplies each unchanged Fourier row. Distinct site rotations
commute. Thus, writing `sigma(c,theta)=C_(c,theta) C_(c,theta)^*`, the SAME
mixed input is

```
rho(g,c,theta,a) = alpha sigma(c,theta)
                    + beta sigma(c,theta+a).
```

The new coordinates are the weighted centre and relative angle

```
u = theta + beta a,
theta_0 = u-beta a,
theta_1 = u+alpha a.
```

The map `(theta,a) <-> (u,a)` is a constant invertible linear map in these
angle coordinates. Hence the centred action is the original action under
an invertible change of the existing variables:

```
S_c(g,c,u,a) = S(g,c,u-beta a,a),
rho_c = alpha sigma(c,u-beta a) + beta sigma(c,u+alpha a).
```

In particular the whole density, not just its pointer probabilities, has

```
D_a rho_c(g,c,u,0)[v]
  = -alpha beta D_theta sigma[v] + beta alpha D_theta sigma[v] = 0.
```

This cancellation holds for arbitrary `g,c,u`, all complete-history
channels, noncommuting effects and the full correlated oldRIGHT. Amplitude
entropy is C1 at rank birth by the inherited theorem; the new eigenvalue
mass is quadratic and contributes zero first derivative. Therefore

```
D_a S_c(g,c,u,0) = 0                                           (1)
```

exactly, for both the complete entropy and the actual linear ledger.

The whole source pullback, with columns for angle gradients, is

```
D_u S_c = D_theta S,
D_a S_c = D_a S - beta D_theta S,                              (2)
```

at the corresponding point. Geometry, scalar amplitudes and every
unselected material coordinate have their ordinary transported derivatives.
In the original amplitude coordinates this gives the exact diagonal Ward
identity

```
partial_(a_w) S(g,m,0)
   = beta slack_w partial_(b_w) S_0(g,m).                      (3)
```

Equation (3) includes the nonlinear normalization of mask14. It is exactly
where the last two mixed terms in the previous matrix `M` enter. No
preparation direction or material equation has been frozen.

## 4. Positive logarithmic normal in the centred chart

This section is needed: a coordinate change alone does not prove that (1)
is the only relative stationary section.

The inherited finite old-support gap gives analytic old/new spectral
projectors of the complete leaf Grams. For one leaf put

```
X = L_gamma C_(c,u-beta a),
DeltaX = L_gamma[C_(c,u+alpha a)-C_(c,u-beta a)],
V_gamma = [X+beta DeltaX, sqrt(alpha beta) DeltaX].
```

The nonzero spectrum of `V_gamma^*V_gamma` is the actual leaf spectrum.
Let `E_new` be its analytic small-cluster projector and
`Z_gamma=V_gamma E_new`. Then `Z_gamma(g,c,u,0)=0` and all amplitude
derivatives are uniformly bounded on a smaller compact parameter chart.
The old-cluster entropy is analytic, even though the small cluster may
change rank.

At `a=0`, the relative difference tangent is the same original
`sum_w v_w J_w C_(c,u)`. The common first-arm displacement is tangent to
the old range and cannot change the first small-cluster mass. Equivalently,
the previous small-cluster amplitude `Z(g,m,a)` vanishes for every `m`
at `a=0`, so its derivative in `m` vanishes there; composing
`m=m(c,u-beta a)` leaves `D_a Z` unchanged at zero. Consequently the
exact quadratic mass is the **same**

```
Q_(g,m)(v)
 = p^3 sum_gamma ||(I-P_gamma)L_gamma sum_w v_w J_w C_m||_HS^2.
```

On the matter-free centre, original parity and complete-leaf normalization
give `Q_(g,0)=nu I`, `nu=p^5/256`, for every strict `g`. The inherited
defect identity gives `Q_(g,m)=nu I+O(||m||^2)`. Shrink the chart so that
`Q >= (nu/2)I`. The centred chart therefore has the same nonzero
logarithmic stiffness as the original chart.

For `r=||a||`, the full centred price has the uniform expansion

```
S_c(g,c,u,a)-S_0(g,c,u)
  = Q_(g,m(c,u))(a) log(1/r^2)/ln(phi) + O(r^2).                (4)
```

The former linear term is zero by (1). The old cluster and the complete
linear ledger have bounded second derivatives. For the new cluster write
`Z=r Zhat`; its bounded amplitude entropy gives the `O(r^2)` remainder
without requiring a positive newborn eigenvalue floor. In particular there
are constants `r_0>0`, `c_0>0`, uniform on this fixed compact chart, such that

```
S_c(g,c,u,a)-S_0(g,c,u)
  >= c_0 ||a||^2 log(1/||a||) > 0,
       0 < ||a|| < r_0.                                     (5)
```

For uniqueness of stationary points, not just of the minimum, use the
same amplitude convexity estimate as the inherited proof. For
`E_eta(Z)=-Tr Z^*Z log(Z^*Z+eta I)`, the scalar singular-value function
has

```
f_eta''(s) = -2log(s^2+eta)-10v+4v^2,
v=s^2/(s^2+eta),
f_eta''(s), f_eta'(s)/s >= -2log(epsilon^2+eta)-6
```

on `||Z||_op<=epsilon`. Here
`6-10v+4v^2=(1-v)(6-4v)>=0`. The singular-value convexity argument
therefore gives the same matrix lower curvature. On a small centred
`a`-ball of radius `R`, continuity of the analytic amplitude derivative
and `Q>=nu I/2` imply `||D_a Z[v]||_HS^2>=nu||v||^2/4`.
The nonlinear amplitude chain-rule term is bounded by
`C R(1+|log R|)||v||^2`; the old entropy and ledger contribute a bounded
negative curvature at worst. Thus the regularized full centred action has
preparation curvature bounded below by

```
c_1 log(1/R)-c_2-c_3 R|log R| > 0
```

for sufficiently small `R`, uniformly as `eta -> 0`. Integrating on
line segments and passing to the actual C1 entropy proves strong convexity
in the centred relative variable. In conjunction with (1), its unique
interior stationary point and minimum is `a=0` for every fixed centre.
No finite preparation Hessian at rank birth is asserted.

## 5. Exact all-equation critical-set equivalence

Let `x` denote `g`, all scalar amplitudes, and all material coordinates,
with independently varied `b_w` and `a_w` at each actuated interior site.
Work in the common small open chart just proved.

If `(x,a)` is a full critical point of the original price, invertibility
of the angle and centre changes makes it a full critical point of `S_c`.
Its relative equation and uniqueness force `a=0`. On that section,
`S_c=S_0` and all base derivatives equal those of `S_0`. Hence `D S_0=0`.

Conversely if `D S_0(x)=0`, take `a=0`. The base sources agree exactly;
the centred relative source vanishes by (1). Inverting (2) proves every
original field and preparation source zero. We have proved

```
Crit(S) intersect U = {(x,0): D S_0(x)=0}.                     (6)
```

This is equality of the full nearby critical sets, not just a map taking
known roots in one direction. It preserves all original geometric sources,
scalar/top equations and selected preparation equations; no new metric or
new physical action has been introduced.

The earlier fixed-original-material minimizer `a_*(x)` still exists uniquely
by the inherited strong-convexity theorem, also for the bounded analytic
ledger above. Define its actual reduced price `F(x)=S(x,a_*(x))`.
The C1 envelope theorem gives `D F=D_x S(x,a_*)`. Thus a critical point of
`F` lifts to a full critical point of `S`, and (6) forces `a_*=0`. Conversely
`D S_0=0` makes `a=0` satisfy the original preparation equation (3), hence
it is the unique fixed-material minimizer and `D F=D S_0=0`. Therefore

```
Crit(F) = Crit(S_0)                                          (7)
```

locally, in the **same original physical base coordinates**. Moreover on
any point where just the selected top-field derivatives of `S_0` vanish,
`a_*=0`, `F=S_0`, and the complete base sources agree there. A full exact
root of this same diagonal action does not acquire a preparation-induced
logarithmic residual.

## 6. Local minima and honest boundary scope

Equation (5) gives `S_c(x,a)>=S_0(x)` locally, with equality only at `a=0`.
Hence a local minimum of `S_0` is a local minimum of the full joint price;
a strict local minimum remains strict. Conversely the diagonal restriction
of a joint local minimum is a local minimum of `S_0`. Any decreasing
diagonal curve remains an actual decreasing joint curve at `a=0`, so this
result cannot turn a saddle into a minimum. The same local-minimum
equivalence holds for the fixed-original-material reduced `F`: an interior
minimum of `F` is critical and has `a_*=0` by (7), and continuity of `a_*`
relates nearby joint and reduced comparisons. No transverse finite Hessian
or Hessian inertia claim is needed.

These conclusions use **independent** top-field variations at the actuated
sites. They apply directly to the open finite chart stated by the source
owner. The angles at all fixed-collar sites are unchanged because the
actuated sites are interior; the full RIGHT Gram, rest-clock amplitude,
CAR normalization, and all other field variables are preserved.

If an additional task fixes a top waveform, constrains `b_w`, fixes one
arm independently, couples `a` to a physical clock, or restricts admissible
finite programmes, its actual constraint/tangent set must be transported
through `theta=u-beta a`. It cannot be retained unchanged by fiat. For
example freezing original `theta` forces `du=beta da`; it is precisely the
earlier fixed-material problem with a generally nonzero optimum. This
does not satisfy the full independent field-equation hypothesis of (6).

The continuous chart is the mathematical closure of the explicitly owned
finite Golden returns. This proof does not establish that each small real
`a` is one admitted finite word, give its physical preparation price, or
derive a smooth physical field writer. At the surviving stationary section
`a=0` no nonzero continuous return is required, but the common selector and
baseline programme still require their actual admission and payment.

## 7. The former mixed matrix is a material-Hessian row map

For the entropy component, keep the source owner's notation

```
s(g,m) = D_a A(g,m,0) = M(g)m + O(||m||^3),
H_m(g) = D_m^2 A_0(g,0),
P_b = selection of the k actuated top-amplitude rows.
```

At the vacuum, `slack_w=p`; the first material gradient is zero by parity.
Differentiate the exact identity (3), with `beta=p^2`, to obtain

```
M(g) = p^3 P_b H_m(g).                                      (8)
```

The same formula holds for the stated complete linear-ledger price when
`M,H_m` are both those of that SAME diagonal price. In particular a null
vector of the material Hessian necessarily lies in `ker M`; the generic
possibility of a new `-t^2/log(1/t)` instability on a Hessian-null ray is
excluded on this actual dictionary. The previously derived value and
source corrections become

```
F-A_0 = -(K p^6/L) ||P_b H_m m||^2 + o(||m||^2/L),
K=ln(phi)/(8nu), L=ln(1/||m||),
```

for the entropy component. The correction is an explicitly derived square
of linearized material Euler rows. This explains why the old fixed-field
off-shell source generally remains, while the full critical set is unchanged.
It does not say that the two off-shell actions are equal or that their
nonvacuum Hessians/response operators coincide under the identity map.

An exact finite negative control with scalar effects `E_gamma=q_gamma I`
has `H_m=0` and hence `M=0`. Keeping only the first two terms of the old
four-term mixed formula would violate (8), just as the original hostile
control found. The angle identity retains the missing normalization term
automatically.

## 8. Novelty, decisive checks and remaining application

The inherited proof proves uniqueness at **fixed original matter**, the
complete logarithmic correction and equality of vacuum Hessians. It does
not contain (1)–(8), the exact centred-chart material action, or equality of
joint critical sets. Searches of the current same-action owners found no
existing weighted-angle-centre or selected-Hessian-row theorem. The new
argument consumes their spectral and completeness facts; it does not replay
the original full128 spectral calculation or assert a new mesh-uniform gap.

The narrow checker retains the exact full16 high-CAR generator and its
complements, the arbitrary two-component material normalization, the exact
weighted density/source cancellation, the fixed-reference cap2 ledger and
the source/Hessian identity. A coupled two-site, three-leaf, eight-dimensional
noncommuting matrix fixture independently checks the complete source
pullback, positive logarithmic centred gap, and diagonal source lift. This
fixture checks the newly used identities; it is not a replacement for the
inherited DATA4096/RIGHT128/255-leaf support certificate. Source hashes are
frozen in `SOURCE_PINS.json`.

The consuming next step is now the diagonal price `S_0` and its actual
physical admission/remaining ledger, without a separate search for these
restricted preparation roots. No result for the N=1 two-query valuation is
imported. Additional noncentral/moving-reference Info, material-dependent
query operators, nonlinear history work or separately priced continuous
controls may destroy (1) and need their own SAME-action source. General
Book selection, nonlinear field roots of this diagonal cap2 price,
refinement-uniform transport and physical GR remain open.
