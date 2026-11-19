# Weighted two-field CQ source: an explicit non-VSI Einstein representative and a finite material-source bridge

21 October 2026. Continue **existing PR #334**, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `constitutive/native-programme-v1`. Input snapshot: `401eafb2958e9d9626db833a25f02b35b3871c16`. This packet was prepared offline for integration because the available GitHub connection had no write operation. No remote publication, CI, Lean build or independent review is asserted.

## 0. What is inherited, what is supplied here

The current branch ALREADY contains [WEIGHTED_WARD_AND_DUST](sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/WEIGHTED_WARD_AND_DUST.md). In particular, the invariant `d(rho*y/F_x)=0`, its reduced interpretation `dQ_E=0`, the original-metric conformal/torsion distinction, a one-scalar dust converse and the frozen-slope Jacobi theorem are owned inputs. They are **not newly discovered by this packet**. The earlier uncommitted conversation's claimed 65-check receipt is not available and is not represented as a recovered historical run. The present package contains newly executed tests and their actual output.

Publication cross-check before packaging: the branch advanced to `b5175db6552426ff946fc3594d46a895bfa88275`. It NOW ALSO contains [the same crossing-stream continuum family](sources/d0_covariant_multiscalar_price_2026-10-21/CROSSING_STREAMS.md) (our displayed seed is its d=1 member), a two-field covariant representation, and a literal-coframe [discrete material Ward checker](sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/check_discrete_material_ward.py). These convergent results are NOT counted twice as new scientific progress. Their exact blobs and overlap are recorded in `CONCURRENT_INPUTS.json`.

The distinct continuation here is the **exact midpoint finite matter lift of that same non-VSI family**, and its explicit integration with the source-defect test. The tensor calculation is a fresh authored cross-check, not an independently accepted review. The inverse-metric version of the discrete tangent is not renamed the coframe tangent; section 5.1 gives their nonzero exact conversion. The packet supplies three bounded consumers:

1. A precise local two-scalar constrained-Einstein comparison, retaining the complete summed kinetic constraint, not replacing a rank-two source by single dust.
2. An explicit, elementary, two-active-scalar **rank-two non-VSI solution** on the common zero-density stratum. After an explicitly derived volume/coordinate matching, it solves the full declared continuum CQ coframe/connection/material equations in the ORIGINAL operational metric, for every prescribed positive PF weight. This is not a new historical claim about exact GR solutions.
3. An exact finite forward-difference matter lift of that witness, plus the explicit finite material Lie/product-rule defect requested by section 9 of the current weighted owner. The forty finite geometric rows and their Lie defect are **not** set to zero or claimed solved.

These are applications of the existing price, matter variables and stationary transformation. No new action, detector, information contract, matter degree, field-writing operation or competing task is introduced. **`GR_closed=false`.**

## 1. Fix the sign convention once

Use the CURRENT owner's orientation, not a mixture of two older conventions:

\[
F(x,y)=-\alpha\beta\{h_\varphi(r(x,-y))-h_\varphi(r_0)\},\qquad
x=\tau eR/\rho,\quad y=+\tau Q/\rho,
\]

where the negative material orientation is already INSIDE `F`. Here

\[
Q=\sum_{A=1}^2g^{\mu\nu}\partial_\mu\psi_A\partial_\nu\psi_A,
\quad a=F_x(0,0)<0,\quad b=F_y(0,0)>0,\quad \kappa=-b/a>0.
\]

The original, finite `z=2^-20` coupling is

\[
\kappa=2p^{-5}(R_0/Q_0+p^6)=23.41640675188407497289558\ldots,
\quad p=\varphi^{-1},
\]

with the original `Q0,R0` of the determinant. It is not replaced by its zero-z limit. The actual cap-one compiler parameters in the replay are `K_pre=9`, `L_gate=20`; changing them changes the common nonzero scale, not this ratio under the inherited fixed-interface hypotheses.

The price and its existing stationary normal form are

\[
S=B_0+M\int\rho F(\tau eR/\rho,\tau Q/\rho)\,d^4z,
\]
\[
S_{\rm red}=B_0+M\tau a\int e_E R(g_E,\omega)\,d^4z
+M\int\rho K(\tau Q_E/\rho)\,d^4z.
\]

The reference volume `d^4z` and the prescribed positive coefficient `rho(z)` are held fixed in these field variations. The independently varied connection has no material source in the inherited scalar/top dictionary. The real baseline is retained; its field-independence is only the declared CQ interface, not a statement that every upstream derivative vanishes.

Consume the established stationary map `g_E=U(t)g`, `t=tau Q_E/rho`, `U(0)=1`, `K(0)=0`, `K'(0)=b`. The original and reduced actions are stationary-equivalent through the owned auxiliary extension, not equal off shell by a physical-only redefinition.

## 2. Two-field comparison theorem, with a converse and the actual volume condition

The inherited reduced equations are

\[
G_{\mu\nu}(g_E)=\mu\sum_A\partial_\mu\psi_A\partial_\nu\psi_A,
\qquad
\nabla_\mu(\mu\nabla^\mu\psi_A)=0,
\]
\[
Q_E=q_*={\rm constant},\qquad
\mu=-\frac{K'(\tau q_*/\rho)}{a e_E}>0.
\tag{2.1}
\]

The first two equations imply the third directly: the divergence of their gradient source is

\[
\sum_A\nabla_\mu(\mu\nabla^\mu\psi_A)\partial_\nu\psi_A
+\frac\mu2\partial_\nu Q_E.
\]

The full scalar equations and contracted Bianchi kill it. This is the two-field statement, not a proof that either individual kinetic norm is constant. In particular `Q_E=0` does not imply either scalar is constant, either original gradient is null, or the total stress has rank one.

**Local converse.** Suppose `(g_E,psi_1,psi_2,mu)` solves (2.1)'s constrained Einstein and current equations with `mu>0`, and `Q_E=q_*`, on a local coordinate patch. For a prescribed smooth positive target `rho(z)` define

\[
H_\rho(z)=-K'(\tau q_*/\rho(z))/a>0.
\]

The positive volume form `mu vol_(g_E)` can locally be pulled back to `H_rho(z)d^4z`. One explicit construction fixes three coordinates and solves an ordinary differential equation for the fourth coordinate with positive Jacobian. Pull back the metric, BOTH scalars and `mu` together. Then

\[
e_E\mu=H_\rho,
\]

and each covariant scalar-current equation becomes exactly the original undensitized equation `partial_mu[K'(t)g_E^(mu nu)partial_nu psi_A]=0`. All reduced metric equations likewise agree. The owned inverse stationary section reconstructs the original weighted fields. Shrink the patch so `tau q_*/rho` stays in its common regular chart. Constraints/collars are transported, not imposed a second time in incompatible coordinates.

The constrained system has a comparison action

\[
I_*=\int e_E\,[R-\mu(Q_E-q_*)]d^4z.
\]

Varying `mu`, the two scalars and the metric gives exactly (2.1) with its constant parameter `q_*`. This is an on-shell comparison, **not a replacement of physical Book Cost-Info**, not equality of off-shell Hessians, and not a claim that the multiplier is an additional native field. Such constrained-scalar/mimetic systems are known in GR; see the primary references below. Their stability or number of physical modes is not deduced by this equivalence.

Away from `q_*=0`, the ORIGINAL observed metric remains `g=U(t)^-1 g_E`, with the already-owned conformal curvature and torsion terms. The result does not turn that transformation into a physical gauge. On `q_*=0`, however, `t=0`, `U=1`: the two metrics coincide exactly for arbitrary `rho`.

## 3. Explicit rank-two non-VSI solution on the original metric

Use coordinates `(r,x,y,z)` with `r>0` and define

\[
\boxed{ds_0^2=r e^{r^2/2}dr^2-\frac{e^{r^2/2}}r dx^2-r^2(dy^2+dz^2).}
\tag{3.1}
\]

First take

\[
\psi_1=r^2/2,\qquad\psi_2=x,\qquad\mu=r^{-2}.
\]

Direct calculation, with the same (+---) Einstein convention as the weighted owner, gives

\[
R_{\mu\nu}=\operatorname{diag}(1,r^{-2},0,0),\qquad R=0,
\]
\[
G_{\mu\nu}=\mu\sum_A\partial_\mu\psi_A\partial_\nu\psi_A,
\quad Q_1=r e^{-r^2/2},\quad Q_2=-r e^{-r^2/2},\quad Q=0.
\]

Both exact currents obey `nabla_mu(mu grad^mu psi_A)=0`. The source has rank TWO at every `r>0`, and

\[
\boxed{R_{\mu\nu}R^{\mu\nu}=2e^{-r^2}/r^2>0.}
\tag{3.2}
\]

Thus this metric is not a VSI pp-wave in disguise. The nonzero invariant gives a coordinate-independent distinction. In the rotated material basis `(psi_1+psi_2)/sqrt(2)`, `(psi_1-psi_2)/sqrt(2)`, both gradients are null, and the source is their two-stream sum. It is not one null-dust ray.

### A short constructive derivation, not a guess from the final tensor

In proper time, start with `ds^2=dT^2-A(T)^2 dx^2-B(T)^2(dy^2+dz^2)`, `psi_2=x`, `dot psi_1=1/A` and total `Q=0`. The scalar current implies `mu B^2=const`. Choose that positive constant as one for the displayed representative. The 00 and 11 Einstein equations imply `A B dot B=1` on one expanding local branch. Writing `r=B`, the remaining equation integrates to `A^2=e^(r^2/2)/r` and `dT=A r dr`, giving (3.1). The checker independently recomputes the full Ricci tensor rather than trusting this reduction.

### Match the actual D0 coefficient and fixed-coordinate volume

The seed chart is NOT yet automatically the fixed-coordinate CQ representative: its volume satisfies `e_0 mu=e^(r^2/2)`, not the required `kappa`. Keep an arbitrary positive small material amplitude `epsilon`, take

\[
\psi_1=\epsilon(r^2-r_0^2)/2,\quad\psi_2=\epsilon x,
\quad\mu=1/(\epsilon^2r^2),\quad c=\kappa\epsilon^2.
\]

Perform the actual coordinate change

\[
\boxed{\frac{dt}{dr}=\frac{e^{r^2/2}}c>0.}
\tag{3.3}
\]

The coordinate t in (3.3) is a continuum volume-chart coordinate, NOT the retained Book/reporting counter. No physical tick rescaling or primitive clock admission follows from this change. Its inverse `r(t)` is smooth on a compact interval away from zero. The original physical representative in the target coordinate chart is

\[
\boxed{ds^2=c^2r e^{-r^2/2}dt^2-\frac{e^{r^2/2}}r dx^2-r^2(dy^2+dz^2).}
\tag{3.4}
\]

Now `e=c r^2`, so `e mu=kappa` exactly. Moreover

\[
g^{tt}\partial_t\psi_1=\epsilon/c,\qquad
g^{xx}\partial_x\psi_2=-\epsilon r e^{-r^2/2},
\]

and the respective t and x divergences vanish. Therefore

\[
a e G_{\mu\nu}+b\sum_A\partial_\mu\psi_A\partial_\nu\psi_A=0
\]

and both original undensitized scalar equations hold. The explicit real coframe

`diag(c sqrt(r) exp(-r^2/4), exp(r^2/4)/sqrt(r), r, r)`

has a Lorentz-skew Levi-Civita spin connection and zero Cartan torsion. The checker verifies all 24 torsion components and the metric/current identities. Six antisymmetric coframe rows follow from the inherited local Lorentz identity; no independent finite-lattice source is inferred from this continuum calculation.

Because `eR=Q=0`, the full nonlinear weighted price has first source

`M tau [a d integral(eR)+b d integral Q]`

for EVERY prescribed smooth positive `rho(z)`, on this original metric. The stationary coframe map is exactly identity. On a sufficiently small patch the two material values can be made arbitrarily small by epsilon and constant shifts. This does not prove the primitive moving-query admission or the complete actual preparation chart of a finite implementation.

**Strength and limit:** the declared continuum CQ price now has an explicit two-active-field solution outside the prior Brinkmann/VSI and rank-one dust consumers. It is still one specified mathematical price, not all possible Book prices. In particular its nonzero Ricci-square means the earlier pp-wave higher-curvature protection theorem cannot simply be imported here.

## 4. Exact finite matter lift on the original forward-difference dictionary

Keep the actual original scalar contraction

`q_z=sum_A (D+ psi_A)_z^T g_z^-1 (D+ psi_A)_z`.

Sample (3.4) at the chronological midpoint `tau_i=t_i+h/2`, and let `r_i=r(tau_i)`. Generate the first material history by REAL finite increments

\[
\psi_{1,i+1}^h-\psi_{1,i}^h
=h\epsilon c r_i e^{-r_i^2/2},
\qquad \psi_2^h(x)=\epsilon x.
\tag{4.1}
\]

Do not replace the first forward difference by the derivative of a separately sampled field. The actual increments in (4.1) give exactly

\[
q_i^h=0,\qquad
g_i^{tt}D_t^+\psi_{1,i}^h=\epsilon/c.
\]

The second material current is independent of x; both original backward-adjoint material Euler rows therefore vanish EXACTLY on every complete interior stencil, for the reduced finite normal-form price. Its material coefficient is `K'(tau q_i^h/rho_i)=b`, even with arbitrary positive finite PF weights.

On a compact r-interval the midpoint quadrature gives O(h^2) matter-amplitude recovery; the proof is the ordinary composite-midpoint remainder with bounded third scalar derivative, not an inferred fit. The supplied numerical test checks 16,32,64,128 time intervals with actual forward increments. Values and errors are in RESULT.json.

**Do not over-promote:** this proves q_h=0 and the TWO material rows of the finite reduced price. It does not prove the original finite plaquette scalar f_h vanishes, solve its sixteen coframe and twenty-four link equations, or establish full criticality of the inverse auxiliary map. A continuum Einstein solution is not automatically a finite all42 root. A full finite representative must next be checked using the existing literal Palatini source, not a replacement discretization.

## 5. Exact finite material Ward defect: close the explicit missing term, not the continuum assumption

This is the direct consumer requested in section 9 of the current weighted owner. Work on a rectangular periodic grid, or a free interior with enough fixed collar so all summation-by-parts boundaries vanish. Set

`D_mu=D_mu^+`, `p_(A,mu)=D_mu psi_A`, `G^(mu nu)=g^(mu nu)`,
`q=sum_(A,mu,nu) G^(mu nu) p_(A,mu) p_(A,nu)`.

Choose the explicit sampled Lie-type field tangent

\[
\delta_\xi\psi_A=\xi^\nu p_{A\nu},
\]
\[
\delta_\xi G^{\mu\lambda}
=\xi^\nu D_\nu G^{\mu\lambda}
-G^{\nu\lambda}D_\nu\xi^\mu
-G^{\mu\nu}D_\nu\xi^\lambda.
\tag{5.1}
\]

It is a legitimate ambient inverse-metric tangent; a corresponding coframe tangent is `delta e=-e(delta G)g/2`. This does not establish that it is generated by an admitted physical writer. Independent link tangents must also be specified when the geometric action is evaluated.

For each nu, define the exact chain-rule defect coefficient

\[
C_\nu=\sum_{A,\mu,\lambda}\left[
(D_\nu G^{\mu\lambda})((D_\nu p_{A\mu})p_{A\lambda}+p_{A\mu}D_\nu p_{A\lambda})
+G^{\mu\lambda}(D_\nu p_{A\mu})(D_\nu p_{A\lambda})
+h(D_\nu G^{\mu\lambda})(D_\nu p_{A\mu})(D_\nu p_{A\lambda})\right].
\]

Using the EXACT forward product rule and commuting scalar differences gives

\[
\boxed{\delta_\xi q-\xi^\nu D_\nu q
=2h\sum_{A,\mu,\lambda,\nu}G^{\mu\lambda}p_{A\mu}
 (D_\lambda\xi^\nu)(D_\lambda p_{A\nu})
-h\sum_\nu\xi^\nu C_\nu.}
\tag{5.2}
\]

There is no omitted higher-order remainder: all h and h^2 pieces are written.

For the ACTUAL finite coefficient `k_z=K'(tau q_z/rho_z)` define

\[
\mathcal R_\nu=
2\sum_\lambda D_\lambda^-\left[
 k\sum_{A,\mu}G^{\mu\lambda}p_{A\mu}D_\lambda p_{A\nu}
\right]+k C_\nu.
\]

Complete summation by parts yields

\[
\boxed{\sum_z k_z\delta_\xi q_z
=\sum_{z,\nu}\xi_z^\nu[k_zD_\nu q_z-h\mathcal R_{z\nu}].}
\tag{5.3}
\]

ALL spatial derivatives of k (hence rho and q) are retained. This is the exact Riesz coefficient of the actual finite material source on the specified tangent, not a continuum Bianchi identity.

Let the actual original geometric first source on that SAME coframe/link tangent be `E_geom,h[xi]=sum xi e_geom,h`. Let `r_extra` denote the likewise contracted actual extra price source after dividing by the declared common `M tau`. Then a full finite stationary point satisfies

\[
\boxed{k D_\nu q=-a e_{\mathrm{geom},\nu}
+h\mathcal R_\nu-r_{\mathrm{extra},\nu}.}
\tag{5.4}
\]

This is a concrete replacement for assuming `Dq=0`. If `k>=k_min>0`, its exact bound is

\[
\|D^+q\|_\infty\le
\frac{|a|\|e_{\rm geom}\|_\infty+h\|\mathcal R\|_\infty+
\|r_{\rm extra}\|_\infty}{k_{\min}}.
\tag{5.5}
\]

Following grid paths from an anchor/collar multiplies the right side by the physical L1 path length, not by an additional inverse mesh power. Under independently proved uniform smooth-field/coefficient bounds, the displayed material R is bounded; the material defect is O(h). The geometric defect and additional source still require their own measured/analytical bounds. This packet does NOT claim that they are zero or that every finite root is smooth.

The checker verifies the exact algebraic triple-product rule and (5.2)-(5.3) on genuine two-field, variable-inverse-metric fixtures in two and four dimensions. The fixtures are diagnostic fields, not invented stationary roots or substitute native prices.


### 5.1. Match the actual coframe Lie tangent: retain the inverse-chain correction

The concurrent native checker samples the coframe Lie derivative itself,
`delta e=xi^nu D_nu e+e_nu D xi^nu`, then differentiates `G=(e^T eta e)^-1`.
This is NOT exactly the inverse-metric sampling in (5.1) on a finite mesh.
For `e_nu=D_nu e`, `L_nu=e_nu^T eta e+e^T eta e_nu`,
`H_nu=e_nu^T eta e_nu`, `G_+=G(z+nu)`, define

\[
B_\nu=D_eG[e_\nu]-D_\nu G
=h[(D_\nu G)L_\nu G+G_+H_\nu G].
\]

The inverse-product formula proves this identity exactly, not just to O(h).
The two complete tangents therefore satisfy

\[
\delta G_{\rm coframe}-\delta G_{\rm inverse\ metric}
=\sum_\nu\xi^\nu B_\nu.
\]

Consequently the source equation on the LITERAL coframe tangent is

\[
\boxed{k D_\nu q=-a e_{\rm geom,\nu}+h\mathcal R_\nu
-k\sum_A B_\nu^{\mu\lambda}p_{A\mu}p_{A\lambda}-r_{\rm extra,\nu}.}
\tag{5.6}
\]

Here `e_geom` is evaluated on this literal coframe/link tangent, not copied
from the other one. This agrees with the current owner's separate B-term.
The additional correction is retained in every error bound; its O(h)
control requires bounded inverse coframe and actual differences. The new
625-site four-dimensional check verifies the inverse formula, both
complete tangent maps and the nonzero material correction. No discrete
diffeomorphism symmetry or zero geometric defect is assumed.

## 6. What a genuinely moving PF coefficient would add

At fixed reduced fields the true material contribution to a rho-variation is

\[
\partial_\rho[ M\rho K(\tau Q/\rho)]
=M[K(t)-tK'(t)].
\]

It vanishes at Q=0, but is generally nonzero off null. The omitted baseline `D_rho B0`, changes in integer counts, preparation, operational metric/readout and genuinely allowed upstream variations still have to be retained. This packet does not make rho a new freely varied physical field or derive its physical equilibrium by that formula alone.

Likewise the full physical source may include other Info/work terms. They cannot be absorbed into the new two-field comparison simply because it is mathematically convenient. The field-writing/readout Jacobians and absolute Book valuation remain separate owners.

## 7. Validation, consumption and the next finite test

Run from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/check_weighted_two_field_rank2.py --repo .
```

Without `--repo`, the script is a standalone offline algebra/tensor/stencil replay and reports that historical Git input bytes were not re-read locally. With `--repo`, it validates the exact pinned source object IDs before doing the calculation. Existing historical receipts are never overwritten; `--output` writes only an explicitly named new file.

The fresh local run contains 122 checks: the correct weighted factorization and sign, actual native polynomial/section at 70 digits, both full Ricci calculations, metric and scalar source identities, all24 torsion components, nonzero invariant, actual forward matter lift, finite material product/source defects and negative controls. Normal and optimized Python outputs match byte-for-byte in the supplied environment. Numerically exact identities are tolerance checks; the written all-field statements follow from the displayed derivations. No old 65-check run, old native compiler, all42 finite suite, remote CI or Lean build is claimed.

The new input for the existing native finite solver is (3.4),(4.1) and their fixed collars. The next meaningful finite step is to evaluate/solve the remaining original 16+24 geometric rows and the actual `e_geom,h` in (5.4), NOT to assume that continuum R=0 forces finite f_h=0. This one missing computation now has an explicit non-VSI, two-active-field fixture and exact matter/no-copy history rather than a newly chosen action.

## Primary references and scope

The constrained-scalar comparison has known relatives, not a new foundational law:

- A. Golovnev, *On the recently proposed Mimetic Dark Matter*, arXiv:1310.2790.
- L. Shen, Y. Zheng, M. Li, *Two-field mimetic gravity revisited and Hamiltonian analysis*, arXiv:1909.01248. Its mode/stability analysis is not transferred to this particular null-total-kinetic background by a name match.

Repository owners, exact hashes, and what is consumed rather than re-proved are recorded in `sources/d0_weighted_two_field_rank2_2026-10-21/SOURCE_INPUTS.json`. The source archive remains the original one; no unlisted snapshots or independently certified receipts are asserted. The concurrent rank-two family is consumed rather than assigned a second discovery or competing owner.
