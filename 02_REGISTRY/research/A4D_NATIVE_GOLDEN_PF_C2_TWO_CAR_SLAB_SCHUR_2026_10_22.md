# D0 — original Golden/PF regularity plus exact two-real-field material elimination in the same nonlinear N=1 CQ action

22 October 2026. Existing scientific Draft PR #334 / `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `constitutive/native-programme-v1`. **A global finite-temporal-slab, fixed-geometric-background material theorem, a proof of original Golden/PF discrete C² regularity at an explicit logarithmic depth, and a quantitative reduced-source/Schur handoff.** Not a full 16+24+2 coupled finite root, not a physical Book03 action selection, not a refinement theorem for the whole raw full128 HJR, `GR_closed=false`.

## Input owners, on THEIR original carrier

1. Original equal-cost Golden boxes, genuine 4D addresses, full counts and the quantitative uniform-cell bound (7)–(10): [`gr_assembly/sources/d0_original_golden_moving_mean_j2_2026-10-19/theorem.md`](../../gr_assembly/sources/d0_original_golden_moving_mean_j2_2026-10-19/theorem.md). No re-ranked or invented site priors.
2. Actual original `G2STAR_NEG_EPS` six-face and two-real-CAR time-dependent rank-two geometry: [`sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py`](sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py) and its **closed-form exact six-face temporal contraction** [`check_global_star_pf_jump.py`](sources/d0_star_rank2_seam_2026-10-21/check_global_star_pf_jump.py). The latter produces a genuine counterexample when positive ρ jumps abruptly; this is what the new PF theorem prevents at the specified depth.
3. One and ONLY one signed original complete N=1 monitored CQ native GoldenMaster (9/20 cap; original sigma-minus plus canonical star operand `x=-τ f/ρ`): [`sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py`](sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py). No other sigma-plus or affine substitute.
4. The recent genuine all42 short-slab numerical stationary witness [`A4D_RANK2_FULL_N1_CQ_42_SOURCE_FINITE_CONSISTENCY_2026_10_21.md`](A4D_RANK2_FULL_N1_CQ_42_SOURCE_FINITE_CONSISTENCY_2026_10_21.md) and actual simultaneous two-cell solver on #334. **These are independent 42-row numerical results, not consequences of the new theorem.**

## 1. Original Golden boxes imply a rigorous O(h³) PF error and O(h) SECOND mesh derivative

Let `h=1/L`, `s=ceil(log_phi L)`, and use the **actual** original Golden exact-cost word depth

\[
\boxed{n(L)=64s+128,\qquad k=n/4=16s+32,\qquad \rho_z=\frac{L^4N_{n,z}}{F_{n+1}}.}\tag{1}
\]

From the original theorem, with `a_n=F_(n+1)p^n`, `a_inf=phi/sqrt(5)`, `epsilon=p^(2(n-2k)+1)/sqrt(5)` and `delta=2p^(floor(k/4))`,

\[
\sup_z|\rho_z-1|\le\frac{L^4\epsilon+128 L\delta+|a_n-a_\infty|}{a_n}.\tag{2}
\]

For this particular schedule:

\[
\epsilon=p^{64s+129}/\sqrt5,\qquad\delta=2p^{4s+8},\qquad
|a_n-a_\infty|=p^{128s+257}/\sqrt5.
\]

The inequality `p^s ≤ 1/L`, `p^8<0.022`, `a_n>0.72` (for all L≥4) gives, using the tiny explicit remainder terms,

\[
\boxed{\|\rho-1\|_\infty<9h^3\qquad(L\ge4).}\tag{3}
\]

This is NOT an assumption that integer counts are smooth: it is a uniform estimate of the original actual counts themselves, proven from the original Golden first-passage measure. It makes every site positive, all inverses bounded, and entails, for any coordinate neighbor and true centered second difference,

\[
\boxed{
\|\nabla_h\log\rho\|_\infty<36h^2,
\qquad \|\nabla_h^2\log\rho\|_\infty<72h.
}\tag{4}
\]

Indeed with `e=9h³≤9/64<1/2`, `|logρ_i-logρ_j|≤2e/(1-e)` and second differences `≤4e/(1-e)`. On a weighted OPEN Dirac edge, the original endpoint factor `sqrt(ρ_x/ρ_y)` differs from unity by O(h³), while its **spatial** logarithmic gradient is O(h²). This bound does NOT identify the open-edge weighted adjoint with the inverse and does NOT erase its **field variation** or the unrelated original Dirac/heat spectral source. The exact CLOSED based-plaquette product still telescopes independently.

The true original READY fraction is retained:

\[
P_{\rm READY}=2F_{n+1}p^{n+3}=2p^3 a_n \to2p^3\varphi/\sqrt5>0.
\]

Thus this source regularity is not paid for by making the native signal vanish. Depth is O(logL), although its enormous numerical coefficient is NOT an efficient all-word enumeration, nor physically selected without an admissible n(L) controller.

## 2. Whole-rectangle coercivity of the **real original N=1 Golden CQ function**

Keep the original `F(x,y)=-αβ[h_phi(r(x,-y))-h_phi(r(0,0))]`, where `α,β>0` are the actual old factory readiness factors, `p=φ^-1`, `z=2^-20`, and

\[
E=p²(1+x),\quad u=p-p² y,\quad \ell=4E(1-E),\quad
B=4u²(1-u²),\quad A=\ell+(1-\ell)B,
\]
\[
r=1-(1-zB)(1-zA).
\]

Let `B_m=8p²u(1-2u²)`, `B_mm=8p⁴(1-6u²)` where m=-y, and set

\[
T=(1-zA)+(1-\ell)(1-zB),\quad
r_m=zB_mT,\quad r_{mm}=z[B_{mm}T-2z(1-\ell)B_m²].
\]

With `H'=log_phi[(1-r)/r]`, `H''=-1/[r(1-r)lnφ]`, the **literal original** material derivatives are

\[
F_y=αβ H' r_m,
\quad F_{yy}=αβ\left[\frac{r_m²}{r(1-r)\lnφ}-H' r_{mm}\right].\tag{5}
\]

An outward-rounded interval evaluation at 45 decimal precision on the ENTIRE rectangle `|x|,|y|≤1/128`, with the independent radial scalar `|y-y_perp|≤1/128`, proves

\[
\frac{F_y}{αβ}\in[1.1333310,1.3306867]10^{-5},
\quad\frac{F_{yy}}{αβ}\in[4.0591660,4.3166417]10^{-5},
\]
\[
\boxed{\frac{F_y+2(y-y_\perp)F_{yy}}{αβ}>1.06588\cdot10^{-5}>0.}\tag{6}
\]

These intervals were obtained directly in `mpmath.iv` with no sample-only positivity inference. The actual original γ/b factory factor is positive; no positivity of the *whole* Book03 action or the FULL metric Hessian is claimed.

## 3. Exact elimination of BOTH real temporal CAR-Euler rows on an arbitrary finite time chain

Fix the original time-chain geometry, inverse timelike coefficient `g_i=g_i^{00}>0`, existing positive PF `ρ_i`, spatial differences of BOTH physical real CAR fields and the original native f_i. Let `ψ_i∈R²`, `u_i=(ψ_{i+1}-ψ_i)/h`, fixed `ψ_0,ψ_N`. Write any fixed spatial/shift contribution in the true metric kinetic contraction as

\[
q_i=g_i\|u_i+b_i\|²+q_{\perp,i},
\quad y_i=\frac{\tau q_i}{\rho_i},
\quad x_i=-\frac{\tau f_i}{\rho_i}.
\]

Here `b_i` comes from genuine `g^{0a}` times the already fixed spatial CAR differences; for the original diagonal rank-two geometry b_i=0 and q_perp,i is the actual negative contribution of the second scalar's x-gradient, NOT a hand-added matter potential. Define the declared **full N=1 CQ scalar time action**

\[
\mathcal S[ψ]=\sum_{i=0}^{N-1}\rho_i F(x_i,y_i).
\tag{7}
\]

All other existing Gaussian/CAR/control parts must have their own true source: (7) is precisely the original declared two-field N=1 CQ **material dependence on this time-chain interface**, not the absolute Book03 H+J+R or a newly imposed quadratic matter action.

Its exact independent time-material Euler equations (for each of the two real components and EVERY interior node) are

\[
\boxed{J_{i-1}=J_i,\qquad
J_i=g_i F_y(x_i,y_i)(u_i+b_i)\in\mathbb R².}\tag{8}
\]

**No approximation, freeze of F_y, or extra Lagrange multiplier:** the vector flux follows by differentiating all original (7) terms. Its Jacobian is

\[
D_{u_i}J_i=g_i\left[F_y I_2+2(y_i-y_{\perp,i})F_{yy}
\frac{(u_i+b_i)(u_i+b_i)^T}{\|u_i+b_i\|²}\right],\quad y_{\perp,i}=\tau q_{\perp,i}/\rho_i.
\tag{9}
\]

Equation (6) proves this Jacobian is **uniformly SPD** whenever `|x_i|,|y_i|,|y_i−y_perp,i|≤1/128`. In the strictly convex subchart `|y_perp,i|+τ g_i||u_i+b_i||²/ρ_i<1/128`, all interpolations of admissible temporal configurations remain inside the derivative interval. Consequently (7) is **strictly convex on fixed-endpoint time fields** and can have at most ONE stationary solution there. Existence follows for boundary data in the local open image of the flux-to-total-displacement map:

\[
\mathcal B(J)=h\sum_i G_i^{-1}(J)-h\sum_i b_i,
\quad G_i(v)=g_i F_y(x_i,y_i(v))v.
\tag{10}
\]

Every local inverse has SPD derivative; D\mathcal B(J) is SPD. Thus (10) has a local unique inverse for the genuine prescribed endpoint difference and determines **BOTH components of the scalar field across the entire finite time slab**, not just a single-site Euler row.

If b_i=0 and y_perp independent of time-component orientation, J_i and u_i are aligned; even a nonzero second scalar temporal boundary current reduces to ONE positive scalar root plus the prescribed common direction. This is the numerical construction below.

The scalar Dirichlet Hessian is explicitly

\[
H_{ψψ}=\frac{2\tau}{h²}B_{\rm edge}^T
\operatorname{diag}_i D_{u_i}J_i\,B_{\rm edge}\succ0.
\tag{11}
\]

If g_i≥g_min and the interval lower bound is m=(αβ)1.06588e−5, then

\[
\lambda_{\min}(H_{ψψ})\ge
\frac{2\tau g_{\min}m}{h²}
4\sin²\!\left(\frac{\pi}{2N}\right)>0.
\]

Thus the full two-real-scalar temporal block is NOT the unidentified singular part of the coupled finite inverse on this chart.

## 4. The EXACT geometric source after the true full material elimination

Where the permitted time-chain material solution ψ_*(g) exists, put `S_red(g)=S(g,ψ_*(g))`. Full differentiation of THE SAME (7) gives the exact envelope law

\[
\boxed{D_g S_{\rm red}=D_g S(g,ψ_*),\quad
D²_gS_{\rm red}=H_{gg}-H_{gψ}H_{ψψ}^{-1}H_{ψg}.}\tag{12}
\]

The matter-induced Schur term is **retained**, not declared zero. This is the correct whole-layer consumer for a future actual gauge/boundary-compatible 40-geometric-row inverse: the material input variables are now mathematically eliminated with a genuine positive inverse, without changing the field price or its input Info algebra. The original discrete spatial material Euler equations and the physical writer/controller/preparation remain distinct and must be included when their directions are allowed; (12) does not solve them by decree.

### Connection with native PF discontinuity negative control

The owned PF-jump counterexample uses only `ρ_i>0`; a fixed ratio jump `ρ_i:ρ_{i+1}=1:2` feeds an O(1) matter Euler residual because the true nonlinear slope changes across the temporal edge. Under (3) the actual native ratio satisfies `|1/ρ_i−1/ρ_{i+1}|=O(h³)`, so for smooth bounded CAR and curvature operands the *pure PF-induced part* of this time difference is O(h²) after dividing by h. In particular that counterexample cannot persist along this specified native schedule. Smooth-geometric variations and the remaining 40 equations still contribute and need their own compatible inverse.

## 5. Executed original L4/L8 finite geometry / FULL CQ witness, not fitted scalar functions

The standalone checker reproduces ALL original F/R nested-box counts for (n,L)=(20,4),(24,8), including the specific temporal lines:

- L=4: n_i=(38,44,60,56), original rho=(0.8887,1.0291,1.4033,1.3097).
- L=8: n_i=(8,5,8,7,6,7,8,6), original rho=(0.4368,0.2730,0.4368,0.3822,0.3276,0.3822,0.4368,0.3276).

The geometric f_i are NOT invented: they are the literal finite six-face boost/plaquette closed expression from the original rank-two source, using the actual time-to-radius erfi coordinate, both neighboring null boosts and `star_density` normalization. For the two original real CAR scalars, the first has nonconstant time gradient, the second has the actual constant x-spatial slope AND a nonzero prescribed time-boundary difference 0.006. The root of (10) is found numerically and reinserted into the full ORIGINAL `GoldenMaster.F(x,y)` action (not an affine or sigma-plus price).

| actual native test | L4 | L8 |
|---|---:|---:|
| max independent scalar temporal CQ Euler numerical gradient | 3.83e−11 | 1.71e−11 |
| true fixed-endpoint error | 4.2e−17 | 2.4e−15 |
| smallest eigenvalue of full 2(N−1)×2(N−1) scalar Hessian | 8.99e−6 | 9.39e−6 |
| independent geometrical envelope derivative against re-optimized scalar finite difference | 9.55e−13 | 1.86e−13 |
| both temporal CAR currents nonzero | YES | YES |

The full temporal Euler equation (8) is exact; these floating numbers validate the actual concrete two-field original-source input and the analytic Schur/positivity route. The L4/L8 particular roots are bisection diagnostics, not interval-certified algebraic exact point descriptions. The whole-rectangle material positivity IS rigorously interval-enclosed; the global fixed-endpoint uniqueness theorem is analytic. No Euler claims for all42 unrestricted FIELD directions follow from a temporal source test.

## 6. Proper placement and the next exact consumer

The recent same N1 42-source **short-collar numerical** root is already owned on #334 (including five PF-jump continuations), and the global temporal link constraint was identified as a covariant difference, not a sitewise 24×24 inverse. This proof adds a useful exact reduction in that *same price family*: the two-real-scalar **temporal** block has its own globally defined positive inverse and exact Schur source for arbitrary finite duration. Thus one can target the 40 connected geometric equations AFTER eliminating the 2(N−1) time-scalar variables, and require the original covariant whole-slab Cartan/coframe gauge+boundary inverse. A chosen 42-root and source error O(h) are not a true existence theorem until that inverse is certified.

The full physical writer/controller and absolute Book03 branch Info/HJR normalization, independent spatial scalar variations, actual original PF clock/source and genuine compulsory selection remain OPEN, as does all42 exact finite joint root/refinement. The present theorem does not claim 10% of the PHYSICAL derivation closed by adding a file, and its significance must be measured by the precisely removed finite time-scalar block. No new action, scalar, detector, target coefficient, invented Golden count, book-layer promotion, or physical GR claim. `GR_closed=false`.

Reproduction: `OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_pf_time_scalar_schur_2026-10-22/check_pf_scalar_schur.py`. Requires sympy-independent NumPy, SciPy, mpmath; the 45dps rigorous source interval is mpmath.iv. The script consumes the exact original n=20/24 count algorithm by literal reimplementation; it does not rerun the full42 solver or remote CI. JSON replay attached and SHA256 pinned in the receipt.
