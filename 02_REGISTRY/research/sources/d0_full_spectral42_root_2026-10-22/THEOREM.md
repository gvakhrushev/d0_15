# Full spectral 42-root and exact 47-variable thermal/Legendre stationary lift

22 October 2026. Repository `gvakhrushev/d0_15`; existing scientific owner Draft PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.

## 0. The changed input and the completed mathematical step

The previous proof established a nonflat root of a configured measured-code CQ action. The proposed four-gate composition did not prove that adding heat and feedback preserved that point. This continuation does not repeat the old CQ root search and does not assume a small extra source there. It solves **the entire previously specified paired-Hodge spectral action** on the unchanged original 42-coordinate, six-plaquette, two-CAR, fixed-collar model, then certifies a different root in a fresh interval ball.

The result is a unique exact nonflat root of all 42 field equations for this declared `H_C+J` model. Its global thermal stationary extension and its four Legendre-response equations also close, giving a nondegenerate 47-variable stationary system. The system remains a saddle. There is no fictitious heat/determinant cancellation, no Newton step substituted for a proof, and no additional `Cost-Info` term counted on top of the spectral action without a valuation identity.

**Scope:** the spectrum below is the paired-cut spectrum, not a demonstrated pullback of the compulsory scene Hodge or the complete paid apparatus. The five extra variables are algebraic thermal/constitutive coordinates, not five independently prepared physical inputs. Native action/cut selection, any genuine independent preparer/controller equations, and mesh-uniform dynamical recovery remain separate. `GR_closed=false`.

## 1. One fixed action and the original unchanged field map

Use the original exact rational collar and

- `h = 0.183801524658179446663931692878752644250497528167344843803260291378571211`;
- 16 independent coframe, 24 proper-Lorentz link-exponential, and two real CAR scalar coordinates;
- original six based G2STAR plaquettes, neighboring temporal face, and two true signed matter currents;
- `tau=1/20`, `rho_0=rho_1=1`, sigma-minus;
- `p=(sqrt(5)-1)/2`, `zeta=2^-20`, `beta=2p^2`, and band multiplicity `m=528`.

The geometric implementation `original_model.py` is an exact copy of Git blob `6d5b41ce11a941fde95e722e708ebb02d689985c`. The collar bytes have SHA256 `b86d94a59f5b0ecfec55af3a6c0db80eec257d41b09f3a03c59e367f56093fa1`. The former unpadded centre is copied exactly from blob `6b520fbd6218444601d90d7e30b738f8c828bd22`. The local `inputs` adapter supplies that same collar; the old padded centre is not used by the field map.

For each of the two cells, obtain from this map

\[
x_s=-\tau f_{C,s},\qquad y_s=\tau q_s,
\]
\[
E_s=p^2(1+x_s),\quad L_s=4E_s(1-E_s),\quad b_s=p-p^2y_s,
\]
\[
B_s=4b_s^2(1-b_s^2),\qquad A_s=L_s+(1-L_s)B_s.
\]

Define `F` to have the four bands `A_0,B_0,A_1,B_1`, each with multiplicity 528. Thus `dim(F)=2112`. The declared paired Hodge has two copies of these bands, dimension 4224, and no additional thermal block (`Z_fixed=0`). This is the explicit spectral contract of this finite test, not an identification of every original scene/work mode with this carrier.

The complete scalar tested is

\[
\boxed{S(z)=6\left\{\frac{\log Z(z)}\beta
       -m\sum_{s=0}^1[\log(1-\zeta A_s)+\log(1-\zeta B_s)]\right\},}
\]
\[
Z(z)=2m\sum_{s=0}^1(e^{-\beta A_s}+e^{-\beta B_s}).
\]

The factor 6 is a fixed nonzero numerical normalization. It does not change any stationary field, introduce a coupling, or modify the heat/feedback ratio. The heat is **one logarithm of the whole trace**. All derivatives of this logarithm are included.

## 2. New centre rather than a false small perturbation of the old centre

The exact decimal vector `spectral_center.json` defines the rational centre `c`. A floating candidate was found by automatic differentiation of an independently implemented original field map. Refinement then used the unchanged original arbitrary-precision exponential/plaquette implementation, reaching a numerical complex-step residual about `1.56e-85`. Neither step is the existence certificate.

The new centre is about `0.02743588350729` away from the former unpadded CQ centre in infinity norm. Consequently the old `1e-24`-radius certificate and its small residual gate do not apply to this displacement. A new certificate is required and supplied below.

Approximate operands at the new centre are

\[
(x_0,y_0)=(0.0003798126018446403,-0.00005823507498259639),
\]
\[
(x_1,y_1)=(-0.0001380910419693269,0.000005678625159067302).
\]

These are genuinely off-null values. The coframe determinant is about `1.5933820551339955381`. The original two matter covectors remain linearly independent.

## 3. Fully outward 42-dimensional existence and uniqueness certificate

The executable certificate uses 140-decimal-digit `mpmath.iv` interval arithmetic. For the entire complex polydisc `|z_i-c_i|<=R`, `R=1e-4`, a rectangular complex enclosure verifies:

1. every inherited matrix exponential obeys the original `||hX||_infinity<1` chart;
2. the metric inverse exists, all logarithm arguments have positive real part, and the price is analytic on the polydisc;
3. `|S|<100` (the actual verified upper bound is below 60).

The imported exponential is not a tolerance-stopped interval exponential. It is the original degree-30 Taylor enclosure after scaling by `2^11`, with a proven rectangular `1e-120` tail, followed by eleven interval squarings. The integer tail inequality and norm checks are independently kept active under Python `-O`.

At the exact centre use imaginary step `d=1e-35`. The derivative enclosures are

\[
g_i\in\frac{\Im S(c+id e_i)}d+[-\epsilon_g,\epsilon_g],
\qquad \epsilon_g=2M d^2/R^3,
\]
\[
H_{ii}\in-2\frac{\Re S(c+id e_i)-S(c)}{d^2}+[-\epsilon_H,\epsilon_H],
\]
\[
H_{ij}\in-\frac{\Re S(c+id(e_i+e_j))-\Re S(c+id e_i)-\Re S(c+id e_j)+S(c)}{d^2}
       +[-\epsilon_H,\epsilon_H],
\quad \epsilon_H=8M d^2/R^4.
\]

Here `M=100`. The slack is not an empirical finite-difference error estimate. Cauchy bounds on the complex polydisc give the even/odd Taylor tails; `d/R<0.01` makes the displayed conservative constants sufficient. All interval exponential and arithmetic errors remain in the evaluated function intervals. There are 904 distinct centre function evaluations and all 1764 Hessian entries are enclosed, using symmetry only to avoid duplicate evaluations.

Invert the midpoint matrix numerically and round each inverse entry to an exact 90-significant-digit decimal rational, forming `A`. The certificate verifies `||I-AH(c)||<1`; it does not assume this from a numerical inverse. Matrix infinity norms are bounded by the **maximum of outward row upper bounds**, never by an ambiguous comparison of overlapping intervals.

For `r=1e-25`, the Cauchy third-derivative estimate gives

\[
\|H(z)-H(c)\|_\infty\le C\|z-c\|_\infty,
\quad C=42^2\,48M/R^3=8.4672\cdot10^{18}.
\]

With

\[
\alpha=\|Ag(c)\|_\infty,\qquad
b=\|I-AH(c)\|_\infty+\|A\|_\infty C r,
\]

the recorded interval run verifies `b<0.1` and `alpha+br<r`. Therefore

\[
T(z)=z-A\nabla S(z)
\]

is a strict contraction of the entire closed real 42-cube into itself. Invertibility of `AH(c)` implies invertibility of `A`. The fixed point is consequently a genuine zero of all 42 Euler components, unique in that cube. Its distance from the centre is at most `alpha/(1-b)`.

The same real cube is checked for positive coframe determinant, both nonzero curvature contractions, two independent CAR currents, and all four spectral bands in `(0,1)`. Two diagonal Hessian signs remain opposite after adding the full `Cr` displacement allowance: `H_00>0` and `H_55<0`. Hence the exact root is nonflat, nondegenerate and a saddle, not just a floating candidate.

Exact outward numerical bounds are stored in `RESULT.json`. This is a computational interval proof with explicit library/transcendental-arithmetic trust, not a Lean theorem or an independent external review.

## 4. Exact global thermal stationary extension: 42 to 43

Put

\[
j(x,y)=-\log(1-\zeta A)-\log(1-\zeta B),
\quad t(x,y)=e^{-\beta A}+e^{-\beta B},
\quad F_\theta=j+\theta t/\beta.
\]

The scalar identity

\[
\log Z=\min_{\theta>0}\{\theta Z/2-\log(\theta/2)-1\}
\]

gives the exact extension

\[
\mathcal A(z,\theta)=6\left[m\sum_sF_\theta(x_s,y_s)
       -\frac{\log(\theta/2)+1}{\beta}\right].
\]

Its unique thermal equation is `theta=2/Z`. At the certified field root,

\[
\theta_*\simeq0.000993648162791503042839273656479.
\]

The thermal Hessian at fixed fields is `6/(beta theta^2)>0`. Its Schur complement is the full certified field Hessian, including the genuine global rank-one correction

\[
H_{42}=\mathcal A_{zz}-6\frac{DZ\otimes DZ}{\beta Z^2}.
\]

The 43-variable stationary system is thus nondegenerate. No thermal derivative has been frozen or discarded.

## 5. Uniform convex response chart and exact 47-variable closure

The unchanged scalar jet module from Git blob `1491cc3d854c83af4256906499fd5f753987215c` verifies by outward intervals on the **whole** chart

\[
|x|\le0.002,\quad |y|\le0.0002,\quad
0.00098\le\theta\le0.00101
\]

that

\[
F_{\theta,xx}>2.95\cdot10^{-5},\quad
\det D^2F_\theta>1.84\cdot10^{-8},\quad
\operatorname{Tr}D^2F_\theta<0.000888,
\]
\[
\boxed{\lambda_{\min}(D^2F_\theta)>2\cdot10^{-5}.}
\]

The entire certified root image and its theta interval lie strictly inside this chart. For each fixed theta, the response map `a_s=F_theta,x`, `b_s=F_theta,y` is injective there, with a unique analytic local inverse. Define its genuine Legendre potential

\[
V_\theta(a,b)=ax+by-F_\theta(x,y),\quad D^2V_\theta=(D^2F_\theta)^{-1}.
\]

The exact 47-variable stationary extension is

\[
\boxed{\mathcal L(z,a_0,b_0,a_1,b_1,\theta)
=6\left[m\sum_s(a_sx_s+b_sy_s-V_\theta(a_s,b_s))
       -\frac{\log(\theta/2)+1}{\beta}\right].}
\]

Its four response equations give `V_a=x`, `V_b=y`; its thermal equation gives `theta=2/Z`; its 42 field equations give the already certified `grad S=0`. Conversely, eliminating these locally unique responses and the thermal coordinate returns precisely S. No order interchange between a maximum and a minimum is asserted.

The four response Hessian directions are **negative**, not positive. Successive Schur congruences give

\[
H_{47}\sim\operatorname{diag}\left(
H_{42},\frac6{\beta\theta^2},
-6m[D^2F_\theta(x_0,y_0)]^{-1},
-6m[D^2F_\theta(x_1,y_1)]^{-1}\right).
\]

Every block is invertible at the certified root. This proves local uniqueness/nondegeneracy of the 47-variable stationary lift. It resolves the actual equations of the declared spectral/response model, while retaining its saddle rather than declaring an unconstrained convex minimum.

The cell response ratios are approximately `-24.36124658616` and `-24.31768924716`. They are computed, not fitted, and are not asserted equal to the old common-null `lambda_minus`. They also are not two freely selected physical couplings.

## 6. Parent substitution and what this does not infer

This removes the previously unproved finite-root premise for the **declared complete paired spectral action** on the original unrestricted 42 chart. No smallness of the full thermal perturbation at the old CQ point is needed; the new point is certified directly. It also makes the correct mixed thermal/Legendre system executable and supplies all its mathematical stationary equations together.

It does not identify `Delta_C` with `L_sym(K(9,11,13))`, derive a compulsory native active projector, or solve a genuinely independent physical preparer merely by calling theta a preparation variable. It does not prove a continuation to every lattice size, generic continuum recovery, a global minimum, or universal GR. Those statements require the actual same-execution map and its remaining sources. A different actual spectrum must be substituted into the scalar before reusing this root; it cannot be cancelled or renamed by hand.

## 7. Previous work is already in Git, with exact bytes verified

Before this continuation, the current remote branch was read at `4f5eec1632b0d1308d192ab7ae428f7532e2153b`. All 29 files of the earlier local delivery patch are already present, not merely linked from a chat:

- global spectral packet, 18 blobs, tree `ce21ef8c137292eb5ecdcc1389350392bbaf572d`;
- native65 packet, 10 blobs, tree `510d44802962d7ed72b484d5dd101b73d5af3bcf`;
- routing document, blob `cfcc0673a26d1679c67b40e3478c822d7ca9ae1e`.

Both remote trees and the routing blob equal those calculated independently from the preserved local ZIP. This verifies publication and unchanged content; it does not attribute the earlier concurrent upload to this turn. No existing source, accepted Book, or other agent's branch work is overwritten.

## Reproduction

From this packet directory:

```
python check_spectral42.py
python -O check_spectral42.py
python check_lift47.py
```

The expensive first command encloses every Hessian entry afresh and does not overwrite the stored receipt. The second should print the identical certificate because all load-bearing guards remain active. The lift consumes the certified root theorem and independently checks the full constitutive chart. Dependencies are `mpmath`; the frozen input and source blobs are included. JAX and NumPy were used only for candidate discovery, not for the interval proof.
