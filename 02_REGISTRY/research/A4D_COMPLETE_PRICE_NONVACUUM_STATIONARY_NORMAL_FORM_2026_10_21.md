# Complete two-density price: local stationary normal form

21 October 2026. Reconstruction from the user's third pasted text, checked anew against repository snapshot `8ba0bd92`. Existing PR #334; native realization / conditional mathematical composition. The historical sandbox files, scripts, numerical receipts and independent review named in the pasted text have not been recovered. This document and its checker are new reconstructions, not byte-identical restorations or attestations of those past runs.

## 1. Exact statement and sufficient hypotheses

Let the finite physical chart have coframes `e_i`, independent links, original material variables and genuine internal coordinates `zeta`. Let its **given complete price**, with actual weights already incorporated, be

`S = B(zeta) + F(x_1,...,x_n,y_1,...,y_n; zeta)`.

Move `F(0,0;zeta)` into `B`, with every derivative; hence `F(0,0;zeta)=0`. Neither operation changes the price. Assume:

1. The actual density map admits independent local positive scales `T_u`, leaving links, matter and `zeta` fixed, with `e_i -> sqrt(u_i)e_i`, `x_i -> u_i x_i`, and `y_i -> y_i/u_i`, for **every independent vector** `u` near 1. The action is smooth and its inverse is `T_(1/u)`. A global scaling identity alone is insufficient.
2. The theorem is stated on an open nondegenerate coframe chart. A smooth constrained chart is also allowed if it is invariant under the required independent local scales. General boundary conditions or constraints must instead be transported through the full extension and both reductions; the same untransformed physical constraint cannot simply be imposed on the final formula. A reduced chart can be used only if the required local scaling action is actually available on it.
3. `B,F` are jointly C4 and the density maps and scale action are C3. These are convenient sufficient, not minimal, assumptions: the transformed function and its stationary section are at least C3 and C2 respectively, so the full source and Hessian arguments are legitimate. Entropy rank births do not automatically satisfy these hypotheses. Fixed-support analytic detector charts do. Discrete caps, trace multiplicities and forced constants remain fixed.
4. `a_i(zeta)=F_(x_i)(0,0;zeta)` are all nonzero in the chosen neighborhood. Set `b_i=F_(y_i)(0,0;zeta)`. Internal coordinates may change the density map, weights and compiler ledger, provided the displayed complete price and scaling law remain valid with those derivatives retained.

Then a unique local auxiliary stationary section, for the construction below, defines `K(Y;zeta)` and establishes a bijection between nearby **full critical points** of `S` and of

`S_eff = B(zeta) + sum_i a_i(zeta) X_i + K(Y;zeta)`,

where `X,Y` are the original density functions evaluated at the transformed coframe. This is stationary equivalence via an auxiliary extension and two reductions; it is not a claimed off-shell identity `S=S_eff composed with a physical-only radial map`. Uniqueness concerns this specified auxiliary branch through `(s,pi)=(0,a)`, not all possible normal forms. `F` and `K` may couple distinct cells.

## 2. Auxiliary extension, elimination and radial condition

Introduce mathematical variables `s,pi` and the exact extension

`S_hat = B + F(s,y;zeta) + sum_i pi_i (x_i-s_i)`.

Their equations at fixed original physical fields are `s=x`, `pi=F_x(x,y;zeta)`. Substitution returns `S` exactly, and the envelope rule returns **every** original source, including internal ones. These variables are neither new paid operations nor proposed physical fields.

On the open set `pi_i/a_i>0`, make the invertible extended-coordinate change

`e_tilde_i = sqrt(pi_i/a_i) e_i`, keeping `s,pi,zeta`, links and matter fixed.

The inverse uses `e_i=sqrt(a_i/pi_i)e_tilde_i`. Exact local homogeneity gives

`x_i=(a_i/pi_i)X_i`, `y_i=(pi_i/a_i)Y_i`.

Thus the SAME extension becomes

`S_hat = B + sum_i a_i X_i + G(s,pi;Y,zeta)`,

`G = F(s, w;zeta) - pi^T s`, `w_i=pi_i Y_i/a_i`.

Its new auxiliary equations are

`F_x(s,w;zeta)=pi`,

`s_i=(Y_i/a_i) F_(y_i)(s,w;zeta)`.

At `Y=0`, the solution is `(s,pi)=(0,a)`. At that solution, writing `A=F_xx(0,0;zeta)`,

`H_aux = [[A,-I],[-I,0]]`,

`H_aux^(-1) = [[0,-I],[-I,-A]]`, `det H_aux=(-1)^n`.

No inverse of `A` or any physical/preparation Hessian is needed. The implicit-function theorem gives the unique section `s(Y,zeta),pi(Y,zeta)`, with positive `pi_i/a_i` after shrinking the neighborhood. Define

`K(Y;zeta)=G(s(Y,zeta),pi(Y,zeta);Y,zeta)`.

Critical points lift to the extension, transform by the extended diffeomorphism, and reduce along this section; the inverse does the opposite. This proves full critical-point equivalence.

The construction is consistent with, rather than imposing, the original radial equations. When the independent radial directions are admitted, original stationarity implies for each i

`x_i F_(x_i) - y_i F_(y_i) = 0`.

At a stationary point the old auxiliary section therefore also satisfies the new one. Linearization at the common-zero stratum gives `delta x=D delta y`, `D=diag(b_i/a_i)`. Restricting all variations to that radial condition in advance would be a different, unjustified operation.

## 3. Coupled Hessian and the order of its factors

Conventions: `F_xy` has row index x and column index y, so `F_yx=F_xy^T`; columns represent tangent vectors. At the base point

`G_(s,pi),Y = [F_xy; D]`, `G_YY=F_yy`.

The derivative of the section is

`[s_Y; pi_Y] = -H_aux^(-1)[F_xy;D] = [D; F_xy+F_xx D]`.

The stationary Schur formula consequently gives the exact symmetric matrix

`K_YY(0) = F_yy + D F_xy + F_yx D + D F_xx D`

`          = [D;I]^T [[F_xx,F_xy],[F_yx,F_yy]] [D;I]`.

In particular, `F_xy D + D F_yx` is generally the wrong cross term. The checker uses a nonsymmetric `F_xy` and unequal diagonal entries of D to distinguish these orders. Also

`K(0;zeta)=0`, `K_Y(0;zeta)=b(zeta)`.

For a single density pair,

`K''(0)=F_yy + 2(b/a)F_xy + (b/a)^2 F_xx`.

The remainder `K-b^T Y` is quadratic in Y and has zero full first differential on `Y=0`; it can still have a nonzero Hessian. With C3 K this gives `K=b^T Y + (1/2)Y^T K_YY(0)Y + O(||Y||^3)` locally at fixed zeta.

## 4. Complete source, internal equations and Hessian inertia

On the reduced chart, without freezing any declared internal variable,

`dS_eff = dB + sum_i(a_i dX_i + X_i da_i) + K_Y^T dY + partial_zeta K d zeta`.

The envelope formula, holding Y fixed, is

`partial_zeta K = partial_zeta F(s,w;zeta)`

`                 - sum_i F_(y_i)(s,w;zeta) (pi_i Y_i/a_i^2) partial_zeta a_i`.

Density-map dependence in zeta also contributes through `dX,dY`. At `X=Y=0` the transformation is identity, and

`dS_eff = dB + sum_i(a_i dX_i + b_i dY_i)`.

In particular `D_zeta S_eff = D_zeta B + sum_i(a_i D_zeta X_i+b_i D_zeta Y_i)` on this stratum. Moving weights, common Book normalization, oldRIGHT/preparation, clock, controller and work sources remain included in B or F or outside the claimed factorization; none is declared stationary merely by renaming it. A nonconstant null material field may have `Y=0` and `dY!=0` and its source survives.

For any symmetric A, the quadratic form of `[[A,-I],[-I,0]]` is `s^T A s-2s^T pi`. Substituting `pi'=pi-(1/2)As` turns it into `-2s^T pi'`, proving inertia `(n,n,0)`. The original extension's auxiliary block has this inertia everywhere. The transformed auxiliary block has the same inertia near the base point by invertibility and continuity.

At corresponding **full critical points**, the two extended Hessians are congruent under the extended coordinate map. Taking the two stationary Schur complements adds the same auxiliary inertia `(n,n,0)` to their physical Hessians. Hence original and reduced physical Hessians have identical positive, negative and null counts. No regularity/invertibility of the physical Hessian is assumed. This preserves every negative quadratic direction; it does not by itself equate degenerate higher-order local minima. No saddle is turned into a minimum by deleting auxiliary directions. Constraint/boundary tangents must be transported for this conclusion.

## 5. Literal detector specialization and the finite coupling

Consume the native two-band function of `COMPLETE_COMPILER_COFRAME_EQUIVALENCE.md`, §6, without changing the action measure:

`p=(sqrt(5)-1)/2`, `z=2^-20`, `L=4p^3=1-p^6`,

`B_scene(y)=4(p+p^2 y)^2[1-(p+p^2 y)^2]`,

`ell(E)=4E(1-E)`, `A(x,y)=ell(p^2(1+x)) + [1-ell(p^2(1+x))]B_scene(y)`,

`r(x,y)=1-[1-z B_scene(y)][1-z A(x,y)]`.

Write `Q=1-zL`, `R=1-zL(1+p^6)`, `r0=1-QR`. Here x and y are dimensionless query operands, not the site coordinate and not the click probability. The actual density convention is `x=eta^2 f`, `y=sigma eta^2 q_mat`, `sigma=+1 or -1`.

At zero, the owned exact derivatives are

`B_y=8p^6`, `B_yy=8p^4(1-6p^2)`,

`A_x=4p^11`, `A_y=8p^12`, `A_xx=-8p^10`, `A_xy=-32p^11`, `A_yy=p^6 B_yy`,

`r_x=z Q A_x`, `r_y=z(R B_y+Q A_y)`,

`r_xx=z Q A_xx`, `r_xy=z Q A_xy-z^2 B_y A_x`,

`r_yy=z(R B_yy+Q A_yy)-2z^2 B_y A_y`.

Thus `r_x,r_y>0` and `r_xx,r_xy,r_yy<0`. The given complete finite-cap CQ term is

`V_N(r)=alpha[kappa-beta h_phi(r)] E_N(beta r)`,

`E_N(v)=sum_(j=0)^(N-1) v^j`, `F_N(x,y)=V_N(r(x,y))-V_N(r0)`.

For each N for which `V_N'(r0)!=0`,

`b_N/a_N = r_y/r_x = 2p^-5(R/Q+p^6)`

`         = 10+6sqrt(5) - 8 z p^4/(1-zL)`.

At the actual finite z this is approximately `23.41640675188407497289558`, strictly less than the limit `10+6sqrt(5)`. The original local CAR source owner, equations (11)–(12), already uses this finite expression: its `lambda_sigma=sigma*2p^-5(R/Q+p^6)`. Thus **the scalar ratio matches the current lambda_minus exactly for sigma=-1**, rather than only approximately. This does not establish equality of the full spatial weights, measure, query preparation or internal source equations.

For N=1, `F_1=constant-alpha beta h_phi(r)`, `a_1,b_1<0`. With `w=(b_1/a_1,1)` both entries are positive. Hence

`K''(0)=-alpha beta [h_phi''(r0)(grad r dot w)^2 + h_phi'(r0) w^T H_r w] > 0`.

The inequalities follow from `0<r0<1/2`, `h_phi'>0`, `h_phi''<0`, and the displayed derivative signs. This positivity is a material-density coefficient, not positivity of the full physical Hessian. In the original material operand the coefficient of `q_mat^2` is `eta^4 K''(0)/2`; the orientation sigma squares out. No density factor `sqrt(|g|)` is inserted.

## 6. Every finite cap: recovered actual unit-price hypothesis

Unlike the historical pasted account, the current source is available. `GOLDEN_EXACT_DETECTOR.md`, §5, proves on its declared admitted gate/measurement/feedforward/pure-input interface that every reached CZ, CCZ and X cycle has net cost greater than 18, 40 and 4 respectively, with all retry, sign, clock and abort records retained. The first CZ is always reached and the first CCZ is reached with probability greater than 22/25. Consequently

`kappa > 18+(22/25)*40 = 266/5 > 53`.

This is consumed with the owner's literal unit charge per primitive, nonnegative extra costs, and absence of unpriced independent stochastic controller distinctions. It is not a universal bound on arbitrary physical Book valuations. The same owner provides `alpha>=1/2`, `1/2<beta<=1`; the following elementary bound only needs `alpha>0`, `0<beta<=1`, `kappa>53`.

Exactly `2^-20<r0<2^-19`. For example `L>47/50`, `L<1`, `p^6=1-L` imply `r0/z=L(3-L)-z L^2(2-L)>1` and `<2`. Therefore

`0<h_phi(r0)<log_phi 2<2`, `0<h_phi'(r0)<20 log_phi 2<40`.

For N>=2, `E_N'(beta r0)>=1` and `E_N(beta r0)<1/(1-2^-19)`. Differentiating the actual finite polynomial gives

`V_N'(r0)=alpha beta { [kappa-beta h_phi(r0)] E_N'(beta r0) - h_phi'(r0) E_N(beta r0) }`

`         > alpha beta [51-40/(1-2^-19)] > 10 alpha beta > 0`.

For N=1 it equals `-alpha beta h_phi'(r0)<0`. Thus every fixed finite cap has `a_N!=0` at the same detector operand chart. This is an analytic all-N proof, not inference from the checker's finitely many example caps. It does not optimize over caps or prove a uniform total runtime under refinement.

## 7. Exact consumer and unresolved application

This is the stationary extension of the current **vacuum-only physical radial identity** to a given complete two-density price. The previously proved obstruction to radially rewriting that price as `aX+bY` is preserved: the determined nonlinear K supplies its nonzero quadratic material term. Coupled prices are allowed if they still factor through the stated densities.

For the original independent star, local homogeneity is already owned because each complementary coframe wedge is based at one site while Lorentz links are independent. For the nondensitized scalar contraction with fixed original differences, inverse local metric scaling gives the opposite material weight. Applying this to a **particular compiled all40+2 query** still requires proving that its actual old-code/PF normalization, preparation/difference map and spatial weights obey precisely this independent-site law. A mean/global rescaling cannot substitute for it. Link elimination before varying the coframes would also change the hypothesis.

On the common `X=Y=0` stratum, a solution of the actual weighted linear source `dB+sum_i(a_i dX_i+b_i dY_i)=0`, including every internal equation, is a solution of the full nonlinear price. The finite lambda match supplies the scalar ratio in this conditional substitution; it does not remove unequal-weight equations, a nonzero preparation baseline or the missing native execution/valuation selection. No new physical action, native coframe writer, CORE claim, compulsory dynamics, or `GR_closed` result is asserted.

## 8. New verification only

`check_nonvacuum_normal_form.py` checks exact coupled block inverse/Schur identities with nonsymmetric cross Hessian, the extended-coordinate identity, full null-stratum sources with moving internal data, exact finite Golden ratio, derivative signs and rational cap bounds. It also solves the auxiliary section at 85-digit precision for diagnostic `alpha=3/5, beta=5/7, kappa=54`, caps 1,2,7,31 and both signs of Y, and checks the predicted second derivative by independently evaluating the section. These parameters are a mathematical fixture, not the actual primary preparation bank. The new run passed in 1.2964 seconds with Python 3.9.6, SymPy 1.14.0 and mpmath 1.3.0. Its maximum normalized auxiliary residual was approximately `9.105e-87`, and the maximum relative discrepancy in the second coefficient was approximately `1.254e-25`. The current run is reported separately in `CHECK_RESULTS.json`; no historical output or independent review is reconstructed as fact.

## 9. Context only

Afonso, Olmo, Orazi and Rubiera-Garcia, [A correspondence between modified gravity and General Relativity with scalar fields](https://arxiv.org/abs/1810.04239), Physical Review D 99, 044040 (2019), describe transferring Ricci-based metric-affine nonlinearities to a scalar matter sector. This is context for the auxiliary method, not an assumption in the proof above or a proof that its fixed measure equals a covariant `sqrt(|g|) P(X)` theory. The integrator verified that primary-source bibliographic reference during this reconstruction.
