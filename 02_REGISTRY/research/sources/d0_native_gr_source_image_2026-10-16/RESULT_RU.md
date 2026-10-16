# D0 → GR: exact stored-adjoint metric-image and Bianchi-invisible source

Date: 2026-10-16. Scope: research calculation consumed by Draft #334, not physical/native GR closure. No native operator, action, BOOK, task, or claim is modified. Parent inputs: `A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md` §2, `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md` §§0–0.3, `A4D_COFRAME_TORSION_INTRINSIC_GR_RECONSTRUCTION.md` §§2–6, plus accepted `sources/d0_w2_weighted_source_2026-10-16/RESULT_RU.md`. This packet does not replay expensive v8/Lean owners.

## Exact theorem: metric variation ranks 10,9,8,7,5

At a homogeneous regular stored-adjoint configuration take `n=e0`, `u_r=(tau_r,w_r)`, `w_r∈R³`, `W=[w_0,w_1,w_2,w_3]`, `eta=diag(1,-1,-1,-1)`, and
```
Q=F eta F^T=tau tau^T-W^T W,    g=Q^-1.
```
The *actual* joint chart (not an ambient metric variation) imposes, for Fourier support `P={r:k_r!=0}`, exactly
```
r∈P: δtau_r=0, w_r·δw_r=0;
r∉P: δtau_r,δw_r arbitrary;
δQ=δtau tau^T+tau δtau^T-δW^T W-W^T δW.
```
The moved observer/boost is a common Lorentz transformation of the four legs and does not change Q. The compensating SO3 link angles also do not change Q. This is not a frozen-observer assumption.

Suppose W has row rank 3, all w_r are nonzero, and every subset of up to three columns is linearly independent. These properties hold for the regular symmetric `F=(a-b)I+b J`, `a>b>0`, `b>0`, near the actual homogeneous chart. The allowed `δu` has dimension `16-2p`, `p=|P|`. The kernel of the full Lorentz Gram differential consists exactly of infinitesimal common Lorentz transformations (dimension 6); in the constrained chart, all three rotations survive while boosts must satisfy `b·w_r=0` for all `r∈P`. Thus kernel dimension is `6-min(p,3)` and
```
rank(DQ|native_P) = (16-2p)-(6-min(p,3))
                  = 10,9,8,7,5 for p=0,1,2,3,4.
```
For p=4 there is also a direct argument: 8 transverse spatial components modulo the exact three-dimensional kernel `δW=ΩW`, `Ω∈so(3)`, give rank 5. Their metric image obeys five independent equations
```
δQ_rr=0 (r=0..3),  λ^T δQ λ=0 (0!=λ∈ker W).
```
The last is the first variation of the rank-three spatial Gram determinant. It is not a free torsion or scalar-weight equation.

## Exact all-16-support calculation and Bianchi test

Use the nondegenerate rational witness `F=I_4+J_4`, `det F=5`; its spatial legs are nonzero and W has rank 3. For each of the 16 subsets of four directions, take the actual allowed transverse `δw`, free `δtau` for inactive directions, and the corresponding `δQ`. Define the Fourier Bianchi condition `(Qk)^T E=0` for a covariant symmetric source `E`, with `k_r=1` for the selected support and zero otherwise. The exact source-image and Bianchi intersection results are

| p=number of active directions | number of supports | image rank (out of 10) | dimension of Bianchi-compatible source invisible to the image |
|---|---:|---:|---:|
| 0 | 1 | 10 | 0 |
| 1 | 4 | 9 | 0 |
| 2 | 6 | 8 | 0 |
| 3 | 4 | 7 | 0 |
| **4** | **1** | **5** | **1** |

The checks preserve the factor 2 for off-diagonal entries in `Tr(E δQ)`. A real Fourier field pairs `k` and `-k`; the table counts one complex Fourier amplitude, not physical propagating degrees of freedom.

For full support, the exact fixture gives
```
Q = [[1,-2,-2,-2],[-2,-5,-4,-4],[-2,-4,-5,-4],[-2,-4,-4,-5]]
λ=(-4,1,1,1),  Wλ=0
k=(1,1,1,1),   Qk=(-5,-15,-15,-15),  k^TQk=-50
E = [[-54,6,6,6],[6,1,-3/2,-3/2],
     [6,-3/2,1,-3/2],[6,-3/2,-3/2,1]].
```
For **every** one of the eight independent allowed transverse leg probes,
```
(Qk)^T E=0,     Tr(E δQ)=0,    E!=0,     Tr(QE)=-105.
```
The witness is an *actual linearized Einstein source*, not a formal symmetric matrix. With `g=Q^-1` and `k^2=-50`, define `bar h=(2/k^2)E=-E/25` and `h=bar h-(g/2)Tr(Q bar h)`. Then `k^μ bar h_{μν}=0` and the full Fierz–Pauli/linearized Einstein tensor of `h exp(i k·x)` is identically `E`. The source can satisfy Bianchi while lying in the annihilator of the native metric differential. **Projected stored Euler equations plus Bianchi do not algebraically imply the full Einstein covector**. This does *not* exhibit a nonflat constrained stationary root: the restricted Fierz–Pauli Hessian on this nonnull mode is nonsingular (rank 5), and h itself need not be an admitted stored variation.

The checker also rejects a radial leg variation and a source with a wrong Bianchi component.

## Scalar weighted-source route: explicit no-identification test

The existing W2 result defines site `omega_x>0` as **supplied**, not PF/volume. With a simultaneous similarity `Dhat=IDI^-1`, `rhohat=I rho I^-1` and `K=dot I I^-1`, `dot Dhat=[K,Dhat]` and `dot rhohat=[K,rhohat]`; the same scalar spectral price is unchanged by cyclic trace. Thus its edge factor `(1/2)(dlog omega_x-dlog omega_y)` is a *representation jet*. Its mere presence does not establish a native linear or quadratic torsion/source coupling. A physical weight-law variation which changes the operator and not just the frame is a different, presently unselected input.

Even if one *proposes* the geometric volume law, it cannot supply all GR components: take `e=I+H(x,y)N`, `F=I-HN`, with `N_00=N_03=1/2`, `N_30=N_33=-1/2`, `N²=0`, `A=I`, `n=e0`. Then `det e=1`, all own-leg equations hold, and the scalar volume weight `sqrt(|det g|)=1` is constant. For `H=x²+y²`, exact second derivatives give `Ric(0)=2(dt+dz)²!=0`, `R=0`; for `H=x²-y²`, `Ric(0)=0` but `R_0101(0)=-1`. No functional of *only* the scalar volume field and its derivatives reconstructs the full tensor source on this class. This does not rule out other F/link/record dependence of the complete native price.

## Action and physical selection: exact status, not future guesses

The original conditional v8 action and its full constrained source already exist in `A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`: `dS=Tr(W dDelta)+Tr(Delta d rho_m)` with `W=rho_m-B^(m-1)/Z+M beta z B^(m-1) A^-1`, plus exact second-order Schur contribution. Replacing this source by the intrinsic geometric transgression would change the action without a native proof. Golden cochain-shift splice does not derive the physical coefficient gates, controller32, preparation/reference128 or history price. The full-Lorentz matrix-interface of #334 enlarges the admissible class but is not yet derived as the physical native process. Its separate controlled-coefficient minmax result `Z>=c/beta²`, combined with necessary `M z beta Z<1`, already rules out a fixed-positive-`Mz` beta→0 stationary refinement in that conditional class.

**Acceptance criterion for a future genuine GR claim:** an M1-derived, admitted one-process full operator/controller/preparation/source; an explicit native-to-intrinsic action derivative equality on precisely admitted variations with independently sourced matter/observer/archive; an independent equation eliminating the above Bianchi-invisible source or a physically forced enlargement of the variation image; and a uniform refinement norm/scale trajectory. None follows from coframe reconstruction or similarity. This research packet closes the concrete variation-image and scalar-weight identification questions, **not** D0→GR.

## Local reproduction

A self-contained exact SymPy checker `check_source_image.py` was executed normally and with `python -O`; its complete JSON is byte-identical (SHA256 `ba6f20e4d66bc20f3b0fd3af66b86d7f477931b64ac1b4b4480061262532395c`). It tests 16 support masks (32 rank/source-dimension assertions), full Bianchi witness, all eight tangent directions, complete Fierz–Pauli source, mutated radial/Bianchi controls, spectral similarity and independent pp-wave Ricci second jets. No v8/Lean/CI pass is claimed.


## Addendum: exact minimal one-row linear completion (not physical admission)

The source-image obstruction is considerably smaller than the missing five raw metric dimensions suggest, once **the four independent linearized Bianchi equations are imposed**. On full-support modes at the regular fixture, the native annihilator of the five-dimensional metric image has a basis consisting of the four diagonal covectors and \`lambda lambda^T\` (with \`lambda=(-4,1,1,1)\`). Bianchi cuts its dimension from five to one. Therefore a **single additional physically admitted equation** separating that one residual covector suffices for local algebraic identification of the whole ten-slot Einstein source **at this fixture and Fourier momentum**.

For the computed witness \`E\`, the ordinary conformal metric direction \`delta Q=Q\` separates it, since \`Tr(Q E)=-105!=0\`. Exact ranks are

\`\`\`
rank native image = 5;
rank [native image ; Bianchi] = 9;
rank [native image ; Bianchi ; conformal scalar row] = 10.
\`\`\`

This is an algebraic **conditional sufficient repair**, not an existing native equation: the conformal direction is *forbidden* by the full-support literal stored own-leg constraints, and the supplied W2 site weight/similarity does not create a physical conformal source. Nor does one trace direction solve action selection or refinement. For other momenta, trace pairing can be zero, so no assertion of a universal conformal repair is made. The right obligation is to derive a single full-support scalar/source row or physically force a larger variation domain, and to show its coefficient and matter/archive coupling come from the actual unchanged native programme.
