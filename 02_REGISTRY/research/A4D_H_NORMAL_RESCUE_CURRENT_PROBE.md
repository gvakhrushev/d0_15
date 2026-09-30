# H-NORMAL-RESCUE: the mixed current and two concrete gates

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Input head: `14bdb90ddf4dbbc16524313d5c8a80aee5451153`.
The task remains Draft / `IN_PROGRESS`. This note introduces no physical terminal.
GitHub guards at the input head passed in run `36718097905`.

The remaining object is `K=K_Y(1+c) exp(Bw)` and
`X_(h,p)=||w||_(p,comp)+||D_G c||_p`.
B is the owned 94-column physical complement. Both actual even-site
Cayley amplitude fields remain inputs. The six graph moves are
`e_s-e_0` and `e_s+e_0`, with their actual phase interchange.
Use the primary memo's Lorentz gauge slice, Gram coordinates and source convention.
At p=1 these are unweighted component sums over physical sites.
The graph norm is the maximum of the six move norms. Fibre conversions
have fixed constants, not powers of the number of sites.

The pure-Y bound is `1152 ||c||_infinity ||D_G c||_p`, with metric
constant 81. Hence c=O(h) in sup norm and X=O(h^2) in the specified norm
give a pure-Y remainder O(h^3) in that same norm. Leading phase-resolved
compatibility, the designated comparator and the mixed terms still matter.
Failure to prove this sufficient size bound is not a response counterexample.

## 1. Three-ratio interior: exact finite convolution

The literal 68-by-96 phase-1/2 interior is independent of the common
Floquet variable in `lambda_j=mu*rho_j`, `rho0=1`, `w=mu^4`.
The [checker](certificates/a4d_y_three_ratio_convolution_check.py) and
[ledger](certificates/a4d_y_three_ratio_convolution_results.json) cover
every triple on four finite complex character tori:

| N | Rank 68 | Rank 65 | Three nonunit ratios | Four distinct characters |
|---:|---:|---:|---:|---:|
| 8 | 511 | 1 | 343 | 210 |
| 12 | 1,727 | 1 | 1,331 | 990 |
| 16 | 4,095 | 1 | 3,375 | 2,730 |
| 24 | 13,823 | 1 | 12,167 | 10,626 |

The rank-65 point is `(1,1,1)`. On each tested periodic ratio lattice
the convolution rank is `68 N^3-3`; left nullity is three, confined to
zero frequency, while right nullity is `28 N^3+3`.
An interior of full row rank still leaves 28 right-kernel directions
off the fold. The other joint rows remain necessary.

Clear denominators by 14 and reduce `Z[zeta_N,1/14] -> F_1000033`,
`zeta_N -> omega_N`. The checker verifies the good prime, primitive
root order and cyclotomic relation. A nonzero specialized maximal minor
was nonzero before reduction, so these ranks hold in characteristic zero
at the specified complex roots. The center rank is checked separately over Q.
This is not an inference of a polynomial gcd from modular agreement.

The continuous three-ratio torus, full joint compact complement and
possible non-torsion zeros are not classified by these finite grids.
The common-phase and two-ratio owners are consumed without repetition.

## 2. Conditional weak-metric size estimate

Retain the open H_TORUS premise of the
[module owner](A4D_Y_CURVED_JOINT_CENTER_GRADIENT_MODULE.md).
Its linear estimate for the complement and gradient has a constant C
independent of the period. Let g lie in a fixed compact Gram chart near eta
and impose the declared equations `E_K(g,K)=0`, `E_Q(g,K)=h^2 tau_h`,
with the source prescribed independently of the candidate.

Finite-stencil analyticity gives a period-independent C_g such that
`||E_g(K)-E_eta(K)||_(p,comp) <= C_g ||g-eta||_(p,comp)`.
E includes all 136 geometric Euler rows. Apply the mean value formula
on the compact charts; bounded derivatives multiply finitely many
translates of g-eta. Translations preserve the actual l^p norm.
No normalized site average or metric-gradient hypothesis is substituted.

The module and mixed remainder therefore give

```text
X_(h,p) <= C [h^2 ||tau_h||_p + C_g ||g-eta||_p]
         + C [1152 ||c||_infinity
              + C_r (||c||_infinity+||w||_infinity)] X_(h,p).
```

C_r is the finite mixed analyticity constant, with the fixed B-coordinate
conversion absorbed in it. In a fixed small chart the last coefficient
is at most one half. Consequently every exact joint field there satisfies

```text
X_(h,p) <= 2C [h^2 ||tau_h||_p + C_g ||g-eta||_p].
```

For p=infinity, a bounded source and `||g-eta||_infinity=O(h^2)`
give X=O(h^2). No separate h-dependent inverse acts on the center gradient.
For p=1, the same order requires those bounds in the **unweighted** norms.
Pointwise O(h^2) at L^4 sites only supplies an O(h^-2) sum bound.
A fixed smooth nonconstant g is not globally eta+O(h^2); compatible
normal-chart freezing and gluing still require proof.
This conditional weak-metric result does not close the original response topology.

## 3. Mixed-field search and the criticality gate

The [numerical probe](experiments/a4d_mixed_y_rescue_probe.py) uses
`S_f=I+(f-1)P_perp`, `P_perp=-Y^2/3`, `g_h=S_f^T eta S_f`,
`f=1+h^2 cos(2 pi (x1-x2)/L)`.
This deliberately h-dependent test does not realize the task's fixed g.
Four fast phases and L slow values form an exact quotient of the L^4
lattice; each `(phase,slow value)` occurs L^3/4 times.
All 94L transverse coordinates and both L-site center fields vary.
The actual mean of c is fixed exactly to zero by a linear projection.

The connection residual is the full chart gradient of the literal action.
The Gram variation uses `S_f dS+dS S_f=eta dq` at the perturbed metric.
The 30L metric phase-erasure rows are a necessary gate for a source
depending on the slow coordinate alone. This restricts the probe's
source ansatz; it is not a condition on every sampled smooth source.
No branch-independent metric source is assigned in this numerical test.
Even a numerical zero would require exact-root and source verification.
Search-coordinate bounds are 0.15; local least squares does not prove global absence.

The [numerical ledger](experiments/a4d_mixed_y_rescue_probe_results.json)
records rejected candidates, with physical-site norms and all-phase
aggregates kept separate:

| L / seed | X_infinity / h^2 | X_1 | Connection chart residual | Metric erasure |
|---|---:|---:|---:|---:|
| 4 / zero | 11.5491 | 133.5974 | 0.0292505 | 0.0167430 |
| 8 / zero | 4.85607 | 255.5623 | 0.00254404 | 0.00169231 |
| 12 / zero | 2.97827 | 348.9229 | 0.000486672 | 0.000260133 |
| 12 / c~h | 2.97827 | 348.9229 | 0.000486672 | 0.000260133 |

Every candidate fails the numerical necessary-equation tolerance 1e-10.
The tolerance itself is not an exact criticality certificate.
These X values are not measurements on exact joint fields and imply
neither a rescue scaling nor a nonzero response gap.
The singular seed uses `c=h cos(2 pi xi/L)` and its least-squares
linear range correction on the full connection/phase-erasure system.

The flat exponential-chart control matched the owned rational connection
Hessian and metric-incidence stencil to respectively
`2.7755575615628914e-17` and `5.551115123125783e-17`, with vacuum residual zero.
This checks coordinates and placement, not nonlinear criticality.

Reproduction needs the repository requirements plus optional
`jax==0.4.35` and `jaxlib==0.4.35`; no CI dependency was added.
Use `--period 4 --amplitude 0` for the flat control, then
`--period 12 --seed singular`, with `--output-dir` a temporary directory.

The environment disconnected during publication. The exact checker and
numerical source were restored from the completed calculations.
The exact checker requires independent CI replay; the restored optional
numerical source requires independent model replay. The reported searches
and flat controls completed before the disconnect.

The first remaining object is a uniform bound for X on admissible exact
mixed joint fields on the sampled smooth metric, in the declared source
convention and norm. The finite convolution is an entry into the torus
route. Rejected numerical fields establish neither that bound nor a no-go.
