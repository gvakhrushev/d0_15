# D0: actual full42 J₂ continuation and exact N1 preparation lift

22 October 2026. Application of the global joint-existence programme in existing Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), task `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Scientific constructor inputs are pinned to `af6e7eb8952564d86ddbfe910eb5f41d4a1b4e4b`. This result changes neither the original model nor its previous certificates.

**Two concrete premises are now completed.** The literal original addressed two-tick Book feedback J₂ has a new, rigorously certified nonflat root of all 42 independent field equations on the original rational collar. Separately, the original unpadded N1 root has an exact 50-variable lift on the explicitly stated fixed-support independent-input domain. These are different prices and different field points. The complete physically selected Book03 heat/return/information/work and independent upstream source have not thereby been identified or solved. `GR_closed=false`.

## 1. The actual source obstruction was continued through

The [previous global joint-index theorem](A4D_GLOBAL_JOINT_INDEX_AND_GR_RIGIDITY_2026_10_22.md) supplied an existence mechanism, conditional on the actual full source and preparation domain. Its small-source application at the old unpadded root allowed a normalized additional 42-covector of norm at most `1e-22` on the stated small field boundary.

We evaluated the genuine next operator component, retaining the original two addresses, all six based G2STAR faces, 16 coframe entries, 24 proper-Lorentz link coordinates and two real CAR amplitudes. With the original operands,

\[
E_j=p^2(1+x_j),\quad \ell_j=4E_j(1-E_j),\quad
b_j=p-p^2y_j,\quad B_j=4b_j^2(1-b_j^2),\quad
A_j=\ell_j+(1-\ell_j)B_j,
\]
\[
r_j=\zeta(A_j+B_j)-\zeta^2A_jB_j,
\qquad \zeta=2^{-20},\qquad p=\varphi^{-1}.
\]

The previously owned literal feedback is exactly

\[
J_2=-528\sum_{j=0}^1
\bigl[\log(1-\zeta A_j)+\log(1-\zeta B_j)\bigr]
=-528\sum_{j=0}^1\log(1-r_j).
\tag{1}
\]

The factor 528 and both eigenbands are retained. The combined OR probability can exceed ζ while each eigenband remains below one; no rank-one `f=r/ζ` is introduced.

Let S₀ be the original unpadded N1 scalar, which already includes the actual report charge `1+r`. Use only the constant equation-comparison factor

\[
a_J=\frac{\nu[h'_\varphi(r_{\rm ref})-1](1-r_{\rm ref})}{528}
\simeq-1904017.766584186.
\tag{2}
\]

It is fixed by the old common-null normalization and does not change the zeros of J₂. It is not a new physical coupling. The full difference is

\[
R_y^J=a_Jd_yJ_2-d_yS_0
=\sum_j\left[\frac{528a_J}{1-r_j}
-\nu\bigl(h'_\varphi(r_j)-1\bigr)\right]d_yr_j.
\tag{3}
\]

At the old rational center the actual 42-component computation gives

\[
\|dJ_2\|_\infty\simeq3.03028669886\,10^{-11},\qquad
\|R_y^J\|_\infty\simeq5.76971971248\,10^{-5}.
\tag{4}
\]

Thus the earlier tiny sufficient budget does not apply. Instead of declaring an obstruction to existence, the calculation continued the complete system to a different field point. Ten numerical steps in `(1−λ)S₀+λa_JJ₂` located the endpoint; a high-precision refinement supplied a rational candidate. The numerical path is a construction aid. The endpoint existence proof below is independent of whether every intermediate path segment has been certified.

Full operator ownership, all 42 initial source components and the remaining physical residual are in [SOURCE_COMPARISON.md](sources/d0_j2_joint_preparation_application_2026-10-22/source/SOURCE_COMPARISON.md) and [J2_SOURCE_AT_UNPADDED.json](sources/d0_j2_joint_preparation_application_2026-10-22/source/J2_SOURCE_AT_UNPADDED.json).

## 2. Exact nonflat all42 endpoint for the literal feedback

**Theorem.** On the original fixed two-cell/three-node collar at

\[
h=0.183801524658179446663931692878752644250497528167344843803260291378571211,
\]

there is a unique zero of `d₄₂J₂` in the closed infinity-norm cube of radius `1e-30` about the published [new rational center](sources/d0_j2_joint_preparation_application_2026-10-22/certificate/J2_CENTER_HIGH_PRECISION.json). The field Hessian is nonsingular throughout that cube. The root is nonflat and has nonzero temporal and spatial matter gradients.

The proof uses outward interval arithmetic for the unchanged original geometric constructor, including its proved matrix-exponential remainder. On the complex polydisc of radius `5e-5` around the new center, the constant-shifted comparison scalar has absolute value below 5. Cauchy bounds control the complex-step differentiation remainders and Hessian variation. Every one of the 1764 Hessian entries is enclosed; no row is inferred from a restricted ansatz.

For the fixed rational preconditioner A the certified bounds are:

| Quantity | Outward bound |
|---|---:|
| `||A||∞` | `<29.975703` |
| Complete normalized first source at the new center | `<8.011e-67` |
| `||I−A H(center)||∞` | `<0.000143094689` |
| Hessian Lipschitz bound on the inner analytic domain | `3.38688e18` |
| Contraction on the radius-`1e-30` cube | `<0.000143094791` |
| Preconditioned center drift | `<2.402e-65` |

The map `T(y)=y−A∇(a_JJ₂)(y)` is therefore a strict contraction mapping this cube into its interior. The near-inverse inequality proves A invertible, so its unique fixed point solves every literal J₂ field equation.

The new center differs from the old unpadded center by

\[
\|y_{J,c}-y_{0,c}\|_\infty
=8.64111074016287493069\ldots\,10^{-7}.
\tag{5}
\]

The old radius `1e-24` and new radius `1e-30` are far smaller than this displacement: these are distinct exact field roots of distinct functionals. The whole new cube has

\[
\det e>1.52566,\qquad (P_{12})_{12}>0.002021,
\]
\[
\frac{\psi_{1,1}-\psi_{1,0}}h>0.08811,
\qquad \partial_{\mathrm{spatial}}\psi_2>0.14612.
\tag{6}
\]

These are the actual coframe, based Lorentz plaquette and CAR differences. The second matter gradient is the retained nonzero transverse collar datum. The certificate does not substitute a flat or matter-free configuration.

A separate rational-congruence interval check proves inertia `16 negative / 26 positive` for the comparison scalar, and therefore `26 negative / 16 positive` for the literal J₂ because `a_J<0`. This is a nondegenerate stationary saddle. Finite stationarity does not require a positive Hessian.

The complete proof is [ENDPOINT_PROOF.md](sources/d0_j2_joint_preparation_application_2026-10-22/certificate/ENDPOINT_PROOF.md), with [existence receipt](sources/d0_j2_joint_preparation_application_2026-10-22/certificate/J2_INTERVAL_RESULT.json) and [inertia receipt](sources/d0_j2_joint_preparation_application_2026-10-22/certificate/J2_INERTIA_RESULT.json).

## 3. Exact independent preparation equations for the original N1 price

The actual N1 query has the fixed input support

\[
P=\operatorname{span}\{|0\rangle,|2\rangle\},\qquad
\psi_\pm=(|0\rangle\pm|2\rangle)/\sqrt2.
\]

At each of the two addresses the full eight-dimensional query obeys

\[
P Q_j(y)P\psi_+=A_j(y)\psi_+,\qquad
P Q_j(y)P\psi_-=B_j(y)\psi_-.
\tag{7}
\]

Thus the same fixed rays are stationary input directions for every nearby field, not only at the old root. Four independent normalized complex rays inside P have the declared manifold `(CP¹)⁴`, of real dimension eight. In local coordinates `u=(Re ξ,Im ξ,Re η,Im η)` per address, the original Born report satisfies

\[
r_j(y,u)=r_j(y,0)
-\zeta(1-\zeta B_j)(A_j-B_j)|\xi|^2
+\zeta(1-\zeta A_j)(A_j-B_j)|\eta|^2+O(|u|^4).
\]

For the original unpadded N1 functional this proves exactly

\[
S_{0,u}(y,0)=0,\qquad S_{0,yu}(y,0)=0.
\tag{8}
\]

Consequently the previously certified exact field root `y₀,*` gives the exact **50-variable** joint root `(y₀,*,0)` on this declared domain. Its Hessian is the direct sum of the old invertible field Hessian and the two explicit four-dimensional preparation blocks. On the entire old certified field cube the new interval consumer proves

\[
A_j-B_j>0.0526,\qquad
\min|\lambda(H_u)|>100,
\]

with four positive and four negative preparation eigenvalues. If only real inputs are admitted, the same construction gives a 46-variable root. Neither version requires a global Euler-characteristic argument because the stationary section is explicit.

This theorem assumes the specified independent fixed-P input interface and its stated price. The paid bank actually generates the displayed rays; it does not by itself admit every independent variation in `(CP¹)⁴` at unchanged cost. Generated factory/work/clock states are instead eliminated through the exact finite causal constraints and their backward adjoints.

The remaining 48 real input directions of `(CP⁷)⁴` are normal to this support. Their sources are explicitly nonzero. The proof supplies their constraint multipliers and retains the reaction of any genuinely moving support. It does not silently treat those directions as gauge or assert a root for unrestricted input states.

See [the complete preparation proof](sources/d0_j2_joint_preparation_application_2026-10-22/preparation/PROOF.md) and its [interval receipt](sources/d0_j2_joint_preparation_application_2026-10-22/preparation/RESULT.json).

## 4. What the combined result does and does not identify

| Interface | Completed substitution | Remaining physical premise |
|---|---|---|
| Original unpadded source → literal addressed J₂ field source | Full 42-covector evaluated; the failed small-source budget replaced by a new exact all42 endpoint | Actual complete heat/return and other selected source on this same execution |
| Original N1 field root → independent fixed-P preparation root | Eight exact new Euler rows, mixed block zero, invertible preparation Hessian, explicit normal reactions | Admission and full price of precisely that preparation interface |
| Literal J₂ → input-dependent Born-report extension | The two functions agree on the configured section | Actual operator/input map off that section; a fixed-cut determinant may be independent of the input rays |
| Finite certified roots → physical D0/GR | A concrete finite source solution and preparation consumer are available | Same-execution physical source selection, admitted writer/upstream equations, uniform refinement and source convergence |

In particular, the eight nondegenerate N1 preparation Hessian directions are not attached to the literal J₂ determinant without its actual moving-input definition. If that determinant is independent of the rays, its corresponding preparation Hessian is zero. The already owned positive rank-one heat source multiplier also belongs to a different coherent READY carrier and is not substituted for the addressed two-band heat.

For the actual fixed-β, fixed-ζ Book03 bootstrap write its genuinely identified return as `J_actual=J₂+J_extra` and retain only any additionally required price terms `P_rest`. At the new J₂ root the full field equation becomes the explicit remaining covector

\[
d_y\mathcal B_{\rm actual}
=-\operatorname{Tr}\!\left(
\frac{e^{-\beta\Delta_N}}{\operatorname{Tr}e^{-\beta\Delta_N}}
\,d_y\Delta_N\right)
+d_yJ_{\rm extra}+d_yP_{\rm rest}=0.
\tag{9}
\]

For the bare §03.25 action there is no `P_rest`. A paid-history binding must identify its information algebra and avoid double-counting the already paid report before adding any such terms. Every independently admitted input/clock/controller direction has its corresponding derivative of the same actual price. The exact residual formulas, including varying calibration and finite-cap preparation boundaries, are in the source note.

The new endpoint removes the concrete inability to pass from the original unpadded source to its actual addressed feedback equations. The preparation theorem removes the unexplained fixed-P input first source for the N1 price. Equation (9), on one fully identified execution, is the next source to consume. No inference of complete physical GR is made from the existence of these finite roots.

**Concurrent result consumed for compatibility.** Commit `22ddd08389dbf00b86d8bf8a964264ae54a77ac5` adds [nonvacuum collective preparation source equivalence](A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md). It constructs paid coherent joint preparations on its actual N-copy moment-writer carrier and proves two-sided, signal-normalized asymptotic recovery of the field source from the pure-preparation source. That construction is a real advance beyond assuming product-only inputs. Its carrier, paid selector baseline and preparation tangents have not been identified with the four original query rays used here; it does not claim an exact finite joint root or compulsory Book03 selection. The present fixed-P theorem is therefore retained at its explicit scope, and no absence of paid joint preparations elsewhere is asserted.

## 5. Reproduction and review

The source packet is [d0_j2_joint_preparation_application_2026-10-22](sources/d0_j2_joint_preparation_application_2026-10-22/). It consumes exact, hash-verified original repository dependencies; duplicate original models and scratch proposal arrays are not republished. The packet contains rational center/preconditioner/congruence data, all outward Hessian endpoints, fresh proof receipts and independent review.

The expensive computation was the new J₂ endpoint Hessian. The old unpadded existence proof was consumed. Preparation intervals and source comparison were recomputed on their actual pinned inputs. The independent review reconstructs the literal two-factor feedback and checks the endpoint proof and frozen matrix bounds without treating numerical convergence as existence.

[REVIEW.md](sources/d0_j2_joint_preparation_application_2026-10-22/REVIEW.md) records verification and exact file hashes. Existing task, original receipts, physical acceptance flags and Draft status are preserved. No whole Lean/CI or mesh-uniform physical proof is claimed.
