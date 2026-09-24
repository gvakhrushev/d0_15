# Common-center matter transport: an exact scalar cocycle, its cell-support obstruction, and the remaining comparison jet

**Audited baseline:** `origin/main = d928cbccc28cf59989f9be4d6ed54f56db1d746e`, fetched 2026-09-24.  
**Brief:** the complete attached common-center/background-dependent matter-lift research brief.  
**Frozen packets:** both durable research memos on second-order Cartan integrability and soldered-creator/observer frame lift were consumed in full; comparison with the previously completed packets showed only the final-newline difference.  
**Work type:** mathematical research and exact rational controls. No Lean, lifecycle, manifest, claim, generated-view or repository-file edits. An unrelated pre-existing change in the redshift source tar archive was left untouched. No wait on the two formalization workers.

## 0. Result

The primary terminal is **COMMON-CENTER-CELL-ACTION-NEW-PRIMITIVE-REQUIRED**.

There is substantial constructive progress before this terminal:

1. On a scalar Role cycle, exact groupoid composition **forces** the missing derivative within the entire class in which the gauge parameter multiplies the output at the same site,
   \[
   g_\xi(e)=M_\xi D_e,\qquad
   (D_e g_\xi)_0[h]=-M_\xi H_0(h)D,\qquad
   K_\xi=M_{\xi^2}D^2.
   \tag{0.1}
   \]
   This derivative was obtained from the groupoid law and the owned flat generator, before constructing any energy.
2. This class has an explicit, energy-independent, exact finite analytic action on a neighborhood in the pure-gauge background orbit. It preserves scalar constants. It is generally spatially dense. Its induced energy has a forced second derivative with nonzero **same-axis distance-two** entries. A direct elementary-cell energy on the original scalar carrier cannot have those entries. Thus this whole generator class is excluded for that precise locality requirement, even if `D_e` itself is allowed to be nonlocal.
3. Independently of that class, **any** differentiable lift with the specified constant-parameter tangent has `R(t\mathbf1;0)=\exp(tD)`. It cannot have a compressed stencil radius, or a nearest-neighbor circuit depth, bounded uniformly over archive periods. This is an isotropy argument, not the scalar reverse-star theorem.
4. For general scalar lifts, all flat background derivatives allowed by the mixed cocycle differ from (0.1) by a symmetric bilinear correction
   \[
   \mathcal S:\operatorname{Sym}^2(\operatorname{im}d_f)\longrightarrow
   \operatorname{End}(C^0).
   \tag{0.2}
   \]
   In the generator it appears as `\mathcal S(h_\xi,h)`. Strict cell support imposes explicit nonzero entries of this correction; the class `g_\xi=M_\xi D_e` has set them to zero. Constants preservation imposes `\mathcal S(h_1,h_2)\mathbf1=0`.
5. A graded reference extension reproduces the owned Cartan generator and **every pure-gauge first-jet block**, including Nyquist and the corner. It does not define an all-background, observer-covariant common-center cell law. Nonexact coframes and the rational boost leave its pure-gauge domain; its scalar support obstruction already persists.

The new earliest datum is therefore a **geometric second-order endpoint-comparison jet `\mathcal S`, with a finite overlap-composition law integrating it**. It must allow dependence on endpoint differences of the gauge parameter. Naming a star, moving `J`, or inserting a coefficient in `M_q` does not supply this datum. The scoped results below do not exhaust lifts with such corrections, or inverse-free parents with additional variables; hence a universal local-matter no-go would be false to claim here.

## 1. Literal owners and the transport boundary

| Audited owner | What can be used literally | Remaining boundary |
|---|---|---|
| `ArchiveAffineCartanConnection.lean`, PR #70 | Affine pulls `A_{x\leftarrow x+r}`; path composition; `affineGauge_lin`; exact `affineTranslation_flat_eq_forwardGaugeCoframe`; open curvature/torsion | Translation of an internal affine fiber does not prescribe the transformation of sampled matter amplitudes |
| `ArchivePathWordAlgebra.lean`, PR #70 | Crossed-product evaluation; oriented path words; loop/endpoint distinction; word-length accounting | Membership in the finite full matrix envelope does not establish bounded local geometry dependence |
| `ArchiveFiniteCartanLieClosureNoGo.lean`, PR #70 | Constant-preserving local gates; Lie-closure and pointwise-derivation results | The gates do not automatically represent the abelian node-translation groupoid |
| `A4DDiscreteEnergyKernel.lean`, PR #75 | `a4dCartanGenerator`, exact expansion, full `flatStaggeredH`, independently written linear `fluxEnergy`, polarization/Riesz, all-degree/parity, Nyquist/corner | No finite background-dependent matter action or nonlinear physical energy follows from the linear Riesz identity |
| `A4DLocatedPrimalDualCell.lean` and `A4DLocatedTopologicalStar.lean`, PR #76 | Distinct typed colors; fixed located `J`; independent incidence; square; parity; orientation; chirality-correct Dirac conjugacy | No metric-dependent recentering or arbitrary sitewise Lorentz intertwiner |
| `A4DLocalReverseStarNoGo.lean`, PR #74 | Stated scalar two-sided inverse/locality obstruction | Not used to forbid any cocycle, observer metric or inverse-free parent below |
| Durable second-order and observer memos | Two-jet identities; exterior lift; observer-positive form; same-fiber link construction and its limits | They explicitly leave the endpoint/common-center finite law unowned |

All named Lean owners are under [`03_FORMALIZATION/D0/Geometry` at the audited commit](https://github.com/gvakhrushev/d0_15/tree/d928cbccc28cf59989f9be4d6ed54f56db1d746e/03_FORMALIZATION/D0/Geometry). The two frozen packets are [second-order integrability](https://github.com/gvakhrushev/d0_15/blob/d928cbccc28cf59989f9be4d6ed54f56db1d746e/02_REGISTRY/research/MEMO_A4D_SECOND_ORDER_CARTAN_CELL_ENERGY_INTEGRABILITY.md) and [soldered creator / observer lift](https://github.com/gvakhrushev/d0_15/blob/d928cbccc28cf59989f9be4d6ed54f56db1d746e/02_REGISTRY/research/MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT.md).

For an owned **pull** link with linear part `L_{x\leftarrow y}` on the four-dimensional internal Role space, the exterior lift gives
\[
T_{x\leftarrow y}=\rho(L_{x\leftarrow y}),\quad
T'_{x\leftarrow y}=\rho(g_x)T_{x\leftarrow y}\rho(g_y)^{-1},
\quad
TC^\dagger(v)T^{-1}=C^\dagger(Lv).
\tag{1.1}
\]
Contractions transform by `L^{-T}`. This is the exterior representation on the existing 16-state carrier, **not** a Spin/Dirac-spinor representation. On degree zero, `\rho(L)=1`: affine linear transport alone cannot produce `M_\xi D` on scalar samples. An affine translation changes the solder/link shift, not this exterior scalar representation.

The owned lattice links also do not specify a factorization through a new half-edge center. Factoring an endpoint isomorphism through a center requires a comparison to that center and a rule on overlaps. Different path words need not agree when their relative holonomy is nontrivial. The located topological `J` fixes complementary cell placement; it does not choose these interpolation maps. The exact equality of the affine shift with `d_f\xi` on the flat translation orbit is not an all-background identification of that shift with the raw solder row `E=\eta+e`; the frozen frame packet explicitly leaves their compatibility unowned.

## 2. Scalar class, assumptions and the derivative forced by composition

Let `X=\mathbb Z/L`, `L\ge3`, `(U\psi)_x=\psi_{x+1}`,
\[
\Delta=L(U-I),\quad D=\frac L2(U-U^{-1}),\quad
H_0(h)=\tfrac12(M_hU+U^{-1}M_h),\quad G_\xi=M_\xi D.
\tag{2.1}
\]
Thus `D^T=-D` and `H_0(\Delta\xi)=-(G_\xi+G_\xi^T)`. Backgrounds initially lie in `\mathcal E=\operatorname{im}\Delta`. The owned affine translation has `e\mapsto e+\Delta\xi`, exactly, with zero acceleration.

Assume a twice continuously differentiable normalized action groupoid
\[
R(\zeta;e+\Delta\xi)R(\xi;e)=R(\xi+\zeta;e),\qquad R(0;e)=I.
\tag{2.2}
\]
Its infinitesimal generator is linear in `\xi`. For this section impose the additional, explicit **output-site parameter locality** condition
\[
(g_\xi(e)\psi)_x=\xi_x(D_e\psi)_x,\qquad D_0=D.
\tag{2.3}
\]
There is **no** assumption here that `D_e` has bounded stencil, local background dependence, preserves a chosen energy, or is an exponential. Equation (2.3) says only that the scalar response at `x` uses `\xi_x`, rather than its endpoint differences or neighboring values.

Write `h_\xi=\Delta\xi`. The mixed groupoid condition is
\[
B(\zeta,h_\xi)-B(\xi,h_\zeta)+[G_\zeta,G_\xi]=0,
\quad B(\xi,h)=(D_e g_\xi)_0[h].
\tag{2.4}
\]
Put `\zeta=\mathbf1`. This is a genuine stabilizer of the owned flat affine background: `h_{\mathbf1}=0`, but `G_{\mathbf1}=D`. Since `g_{\mathbf1}(e)=D_e`, (2.4) forces
\[
(\mathrm d D_\bullet)_0[h_\xi]=[M_\xi D,D]
=[M_\xi,D]D=-H_0(h_\xi)D.
\tag{2.5}
\]
Here `\mathrm dD_\bullet` is the derivative of the operator family `e\mapsto D_e`. Consequently
\[
\boxed{B_{\rm adv}(\xi,h)=-M_\xi H_0(h)D,\qquad
K_\xi=G_\xi^2+B_{\rm adv}(\xi,h_\xi)=M_{\xi^2}D^2.}
\tag{2.6}
\]
The cancellation uses `DM_\xi=M_\xi D+H_0(h_\xi)`. Substituting (2.6) directly in (2.4) verifies the complete mixed law. In particular `K_\xi` is **neither** the previously rejected background-independent exponential jet `G_\xi^2` nor zero on the delta witness.

## 3. Exact finite integration before defining an energy

For `e=\Delta\phi` define the matrix whose `x`-th row is the `x`-th row of a constant-shift exponential:
\[
F_\phi(x,y)=\bigl[\exp(\phi_x D)\bigr]_{xy}
=\sum_{m\ge0}\frac{\phi_x^m}{m!}(D^m)_{xy}.
\tag{3.1}
\]
Equivalently `F_\phi=\sum_m M_{\phi^m}D^m/m!`. This is **normal ordering** of coefficient multiplication and path-word powers; it is generally not `\exp(M_\phi D)`. It uses the already owned scalar difference operator and a displacement potential, with no `W_c` input. At fixed finite `L` it is a finite-dimensional analytic matrix, invertible near `\phi=0`.

The essential identities are
\[
\partial_\xi F_\phi=M_\xi F_\phi D,\qquad
F_{\phi+c\mathbf1}=F_\phi\exp(cD),\qquad F_\phi\mathbf1=\mathbf1.
\tag{3.2}
\]
They follow row by row from the ordinary exponential series. Define
\[
D_e=F_\phi D F_\phi^{-1},\qquad
R_{\rm adv}(\xi;e)=F_{\phi+\xi}F_\phi^{-1}.
\tag{3.3}
\]
Both expressions are independent of the representative `\phi+c\mathbf1`, because the common right factor in (3.2) cancels. They satisfy **exactly**, without truncation, (2.2) and `g_\xi(e)=M_\xi D_e`. Composition telescopes:
`F_{\phi+\xi+\zeta}F_{\phi+\xi}^{-1}F_{\phi+\xi}F_\phi^{-1}=F_{\phi+\xi+\zeta}F_\phi^{-1}`.
Scalar constants are preserved at finite parameter.

More precisely, take the open subset `\mathcal U\subset\mathcal E` on which `F_\phi` is invertible, containing `0`. It is independent of the representative by (3.2). Formula (3.3) defines arrows whose source and target belong to `\mathcal U`, and (2.2) holds whenever all three backgrounds do. No assertion that `F_\phi` is invertible on the entire orbit is needed or made. The same neighborhood qualification applies to the graded construction below and to finite dressings in Section 5.

This is also the locally unique smooth solution in class (2.3). At any background the same constant-parameter argument gives
`\partial_{h_\xi}D_e=[M_\xi D_e,D_e]`. Along a ray in `\mathcal E` it is a finite-dimensional polynomial ODE with fixed initial value `D`. Formula (3.3) solves it; local ODE uniqueness fixes `D_e` and then the normalized transport `R`.

Only **after** this construction set
\[
W_{\rm adv}(e)=F_\phi^{-T}F_\phi^{-1}.
\tag{3.4}
\]
It is well-defined on `\mathcal E` because `\exp(cD)` is counting-orthogonal. It is positive definite where `F_\phi` is invertible and obeys
`W(e+h_\xi)=R(\xi;e)^{-T}W(e)R(\xi;e)^{-1}`. Thus its Hessian below is a consequence of transport, not a chosen energy fitted to `K`.

The construction is a **pure-gauge, generally nonlocal benchmark**. Obtaining `\phi_x-\phi_y` from `e` requires path integration, and (3.1) includes paths of unbounded length as `L` varies. It is not a claimed local physical cell action.

## 4. Full second jet, energy Hessian, and elementary-cell no-go

Let `e(t)=th` with `h=\Delta\xi`. Equations (2.6) and the frozen congruence calculus give
\[
\mathcal H_{\rm adv}(h,h):=D^2W_0[h,h]
=2(G^T)^2+2G^TG+2G^2
-M_{\xi^2}D^2-D^2M_{\xi^2}.
\tag{4.1}
\]
With `X=M_\xi` this can be reorganized as
\[
\mathcal H_{\rm adv}=2H_0(h)^2-[X,[X,D^2]].
\tag{4.2}
\]
For `L\ge5` the **entire matrix** therefore has
\[
\begin{split}
(\mathcal H_{\rm adv})_{i,i}&=\tfrac12(h_i^2+h_{i-1}^2),\\
(\mathcal H_{\rm adv})_{i,i+2}
&=(\mathcal H_{\rm adv})_{i+2,i}
=-\tfrac14(h_i^2+h_{i+1}^2),
\end{split}
\tag{4.3}
\]
with all remaining entries zero. Indices are cyclic. The same formulas must be periodized with collisions at smaller periods; no large-period support inference is made from `L=2,3`.

For `\xi=\delta_0`, `h_0=-L`, `h_{-1}=L`, `G^2=0`, while
\[
K_\xi=\frac{L^2}{4}M_{\delta_0}(U^2-2I+U^{-2}).
\tag{4.4}
\]
At `L=5`, in order `(0,1,2,3,4)=(0,+1,+2,-2,-1)`, the two complete matrices are
\[
K_\xi=
\begin{pmatrix}
-25/2&0&25/4&25/4&0\\
0&0&0&0&0\\0&0&0&0&0\\0&0&0&0&0\\0&0&0&0&0
\end{pmatrix},
\]
\[
\mathcal H_{\rm adv}=
\begin{pmatrix}
25&0&-25/4&-25/4&0\\
0&25/2&0&0&-25/2\\
-25/4&0&0&0&0\\
-25/4&0&0&0&0\\
0&-25/2&0&0&25/2
\end{pmatrix}.
\tag{4.5}
\]
These are `K=R''(0)` and `W''(0)`, so the expansion uses `t^2K/2` and `t^2\mathcal H/2`.

For either reference law `W_c=I+H+cM_q` the scalar Hessian would be `2cM_{h^2}`. Its required `K_{\rm sym}:=(K+K^T)/2` has `(+,+)` diagonal `L^2/4` and `(+,-)` entry `-L^2/4`. The derived `K_{\rm sym}` in (4.4) has **zero in both places**. Thus neither `c=1` nor `c=2`, nor any value of this scalar diagonal-\(q\) coefficient, matches this transport. The new Hessian contains actual pair couplings absent from every member of that ansatz. As a check, `\mathbf1^T\mathcal H_{\rm adv}\mathbf1=0`, consistent with exact constants preservation.

For the independent control `\xi=\delta_0+2\delta_1` at `L=5`, `G^2\ne0` and
\[
K_\xi=
\begin{pmatrix}
-25/2&0&25/4&25/4&0\\
0&-50&0&25&25\\
0&0&0&0&0\\0&0&0&0&0\\0&0&0&0&0
\end{pmatrix}.
\tag{4.6}
\]
The equality `K=G^2+B_{\rm adv}(\xi,h_\xi)` and all entries of (4.1) were checked exactly at `L=3,5,7`, rather than generalizing the delta nilpotence.

**Scoped theorem: no direct elementary-cell energy in class (2.3).** Assume (2.2–2.3), the flat generator (2.1), a smooth invariant quadratic form with `W(0)=I`, and a direct cell-additive energy on the original scalar cochains whose matter arguments in each term all belong to the closure of one elementary archive cell. Then for `L\ge5` an entry between sites `-1` and `+1` along the **same axis** is identically zero: no such cell contains both. Its second derivative must be zero. But (4.3–4.5) force `W''_{+1,-1}=-L^2/2\ne0`. Contradiction.

This excludes the whole class (2.3), without assuming any radius bound on `D_e`. The obstruction is not the allowed `s-r` corner for distinct axes: that corner fits in a square, whereas the two sites here are separated by two steps in one coordinate. It does not exclude an effective nonlocal kernel obtained by eliminating auxiliary parent variables, an energy supported on larger patches, or a generator with the correction classified next.

## 5. Complete scalar classification of the still-free flat comparison jet

Drop (2.3), retain the specified flat `G_\xi` and exact groupoid law. On the pure-gauge space the full set of background derivatives satisfying the mixed two-jet condition is
\[
\boxed{
B(\xi,h)=B_{\rm adv}(\xi,h)+\mathcal S(h_\xi,h),\qquad
\mathcal S(h_1,h_2)=\mathcal S(h_2,h_1).
}
\tag{5.1}
\]
Here symmetry concerns the two coframe inputs; the **matrix output need not be symmetric**. To prove completeness, subtract the particular solution `B_{\rm adv}` from any `B`. The mixed law says the difference is symmetric after substituting `h_\xi,h_\zeta`. Taking a constant parameter shows the difference vanishes when that parameter is constant. Since `\ker\Delta=\mathbb R\mathbf1`, it factors through `h_\xi`, giving (5.1). This is a classification at the flat two-jet level, with no unproved assertion about locality of a finite completion.

The resulting jets are
\[
K_\xi=M_{\xi^2}D^2+\mathcal S(h_\xi,h_\xi),\qquad
D^2W_0[h,h]=\mathcal H_{\rm adv}(h,h)
-\mathcal S(h,h)-\mathcal S(h,h)^T.
\tag{5.2}
\]
Every such `\mathcal S` can be integrated **as an unrestricted finite matrix groupoid dressing**, which proves that composition alone does not select it. Choose any smooth invertible
`P(e)=I+\frac12\mathcal S(e,e)+O(e^3)` and set
\[
R_P(\xi;e)=P(e+h_\xi)R_{\rm adv}(\xi;e)P(e)^{-1}.
\tag{5.3}
\]
The groupoid law is exact by telescoping; the flat generator is unchanged, and its background derivative is exactly (5.1). This construction does not use an energy. Locality of `P^{-1}`, cell support of the induced energy and its physical interpretation do **not** follow.

For example `(\mathcal S(h,k)\psi)_i=h_i k_i(\psi_{i+1}-\psi_i)` is symmetric in `h,k`, translation-covariant and has nearest-neighbor matrix support and `\mathcal S(h,k)\mathbf1=0`. It supplies genuine two-jet freedom without changing the first jet or the mixed cocycle. A finite dressing built from it may spread under inversion.

Strict cell support requires, already on the delta cycle,
\[
\bigl(\mathcal S(h,h)+\mathcal S(h,h)^T\bigr)_{+1,-1}
=-L^2/2,\qquad
\bigl(\mathcal S(h,h)+\mathcal S(h,h)^T\bigr)_{0,+2}
=-L^2/4.
\tag{5.4}
\]
Thus a correction confined to a nearest-neighbor **matrix output** cannot repair this witness; comparison across the two-edge patch must enter the matter transformation even if the final energy is strictly cell-additive. This is a precise constraint on the missing common-center rule.

If the finite scalar action preserves constants, (5.1) additionally requires `\mathcal S(h_1,h_2)\mathbf1=0`. The frozen rejection of `c=1,2` then remains in force: their positive constant-field second variation cannot be obtained from such a lift. Allowing a scalar density that does not preserve constants changes this hypothesis; it is extra transformation data, not an implicit repair.

## 6. Graded pure-gauge benchmark and the exact limit of its first-jet match

The owned PR #75 expansion is
\[
G_\xi=A_\xi+\mathcal K(h_\xi),\quad
A_\xi=\sum_r M_{\xi^r}D_r,\quad
\mathcal K(e)=\sum_{s,r}M_{e_s{}^r}U_sA_rE_{sr},\quad
A_r=\tfrac12(I+U_r^{-1}),\ E_{sr}=c_s^\dagger c_r.
\tag{6.1}
\]
The complete owned target is
\[
H(e)=\sum_r H_r(e_r{}^r)I-\mathcal K(e)-\mathcal K(e)^T,
\quad H_r(a)=\tfrac12(M_aU_r+U_r^{-1}M_a).
\tag{6.2}
\]

There is a useful **independently specified transport benchmark** on `e=d_f\phi` in all grades. Let
\[
F_\phi^{\rm sc}(x,y)=
\left[\exp\left(\sum_r\phi^r(x)D_r\right)\right]_{xy},\quad
P(e)=I+\mathcal K(e),\quad
\mathcal F_\phi=P(d_f\phi)(F_\phi^{\rm sc}\otimes I_{\mathcal F}).
\tag{6.3}
\]
This chooses a finite continuation of the owned flux part *in the matter comparison*, before an energy; it is not claimed to be forced by geometry. The commuting `D_r` imply
`\mathcal F_{\phi+c}=\mathcal F_\phi\exp(\sum c^rD_r)`. Hence
`R_{\rm gr}(\xi;e)=\mathcal F_{\phi+\xi}\mathcal F_\phi^{-1}` is an exact well-defined pure-gauge cocycle. Set `D_{r,e}^{\rm sc}=F_\phi^{\rm sc}D_r(F_\phi^{\rm sc})^{-1}`. Its generator is explicitly
\[
g_\xi^{\rm gr}(e)=\mathcal K(h_\xi)P(e)^{-1}
+P(e)\left(\sum_r M_{\xi^r}D_{r,e}^{\rm sc}\right)P(e)^{-1}.
\tag{6.4}
\]
At flat it is exactly `G_\xi`. With
\[
B_{\rm sc}(\xi,h)=
-\sum_{r,a}M_{\xi^r}H_r(h_r{}^a)D_a,
\]
its derivative and second jet are
\[
\begin{split}
B_{\rm gr}(\xi,h)
&=-\mathcal K(h_\xi)\mathcal K(h)+[\mathcal K(h),A_\xi]+B_{\rm sc}(\xi,h),\\
K_\xi^{\rm gr}
&=\sum_{r,a}M_{\xi^r\xi^a}D_rD_a+2\mathcal K(h_\xi)A_\xi .
\end{split}
\tag{6.5}
\]
The mixed cocycle was checked with a nonzero commutator, not merely a disjoint-support pair.

The derived form `\mathcal W=\mathcal F_\phi^{-T}\mathcal F_\phi^{-1}` therefore satisfies
`D\mathcal W_0[h_\xi]=-(G_\xi+G_\xi^T)=H(h_\xi)` in all Fock degrees. The construction preserves degree and parity and is equivariant under simultaneous signed Role/site permutations. It reuses the **owned first-order** half-average in (6.1); it does not derive an all-order half-edge rule from incidence.

The exact controls are informative:

| Required component | Status of (6.3) |
|---|---|
| Scalar nearest-neighbor coefficient on `e=d_f\xi` | Exact via the Ward identity |
| Both `U_s` and `U_sU_r^{-1}` paths, all degrees | Exact at first order on that same domain |
| `L=2` alternating `e_A{}^A=(-2,2)` | Correct occupied-A slopes `(2,-2)`; the raw field survives even though the centered readout vanishes |
| `L=3` corner from `\xi^B=\delta_A` | `H_{(0,\{A\}),(A-B,\{B\})}=-3/2` exactly |
| Flat `e=0`, parity and nontrivial Role swap | Exact |
| General uncentered `e` | Not defined without another prescription; pure-gauge equality does not prove `DW_0=H` on the full coframe space |
| Strict scalar elementary-cell energy | Excluded by Section 4, since (6.3) restricts to the scalar construction |
| Combined local Lorentz/observer action | Not established; even a constant boost leaves the pure-gauge domain |

There are two concrete transverse failures of potential-based continuation. A constant `e_A{}^A=t\ne0` has a nonzero period integral and cannot equal `d_f\phi` on a periodic lattice; (6.2) nevertheless acts on a constant scalar as `tI`. A coframe with nonzero plaquette curl has no path-independent `\phi` even locally around that square.

One can integrate affine shifts along a **chosen** root-to-site path word, but different paths differ by the affine open torsion and a root/word selection is not a common-center law. If `p(e)` denotes any linear path-based potential extraction and one substitutes it in (6.3) while retaining the raw `\mathcal K(e)`, its first jet would be
\[
\sum_r H_r((d_fp(e))_r{}^r)I-\mathcal K(e)-\mathcal K(e)^T.
\tag{6.6}
\]
The missing target is exactly
`\sum_r H_r((e-d_fp(e))_r{}^r)I`. Thus the failure is visible even before nonlinear coefficients: a gauge-orbit construction cannot be promoted to the full PR #75 first jet by an unstated choice of paths.

## 7. Finite composition and five distinct locality questions

The scalar and graded benchmarks satisfy node-translation **groupoid** composition exactly. Affine path composition and exterior frame composition are separate owned group laws. Archive site translations are discrete permutations; Role permutations simultaneously relabel sites and Fock directions. None of these is identified with the others.

There is also a universal scoped support theorem independent of (2.3). Constant node translations stabilize the entire flat affine background, so every differentiable exact lift with `G_{\mathbf1}=D` must restrict to a one-parameter representation:
\[
R(t\mathbf1;0)=\exp(tD).
\tag{7.1}
\]
Given a proposed uniform radius `R_0`, choose `L>2(R_0+1)`. The entry from `0` to `R_0+1` has leading term
\[
\bigl[\exp(tD)\bigr]_{0,R_0+1}
=\frac{(L/2)^{R_0+1}}{(R_0+1)!}t^{R_0+1}
+O(t^{R_0+2}).
\tag{7.2}
\]
The shortest oriented path is unique before wraparound, so this coefficient is nonzero. A uniformly bounded compressed stencil on an interval of finite parameters is impossible. A fixed number of nearest-neighbor circuit layers would impose such a bound and is impossible too.

| Notion | Result |
|---|---|
| Infinitesimal stencil | `G` is the owned local operator; `B_{\rm adv}` has length-two support |
| Elementary cell support of the direct effective energy | Fails in the entire scalar class (2.3) at second order |
| Compressed support of finite `R` | Generally global; no uniform finite radius is possible for any lift satisfying (7.1) |
| Factorization into local path/gate operations | May be possible with cost and path length growing with `L`; a finite full-matrix realization is not by itself a derived local cell law |
| Locality of the inverse | Not established by a local numerator or by finite dimension; no reverse-star theorem is needed for the present arguments |

At finite `L`, analytic functions of `D` can be reduced to a polynomial by its minimal polynomial, but the required path length and coefficient dependence need not be uniformly local. A continuous flow generated by local operations, a finite-depth circuit, and a direct elementary-cell action are different claims. An inverse-free parent can have an effective nonlocal `W` after elimination and is outside the direct-energy no-go.

## 8. Observer/frame and fixed located primal/dual compatibility

The independently established exterior frame lift uses
`h_n=-\eta+2n^\flat\otimes n^\flat` and `B_n=\bigoplus_k C_k(h_n)`. The rational A/B boost `g` with entries `5/4,3/4` satisfies
\[
h_{gn_0}|_{AB}=
\begin{pmatrix}17/8&-15/8\\-15/8&17/8\end{pmatrix},
\quad g^T h_{gn_0}g=I.
\tag{8.1}
\]
The link law (1.1), moving creators and this moving positive form are compatible. The exterior lift remains non-spinorial. `n_0=e_A` is only a reference observer gauge; `U_A` is not time evolution.

For the raw solder convention `E=\eta+e`, the vector boost `g` corresponds to right row action `E\mapsto Eg^{-1}`. At flat,
\[
e'|_{AB}=
\begin{pmatrix}1/4&-3/4\\3/4&-1/4\end{pmatrix}.
\tag{8.2}
\]
This is constant with nonzero cycle sums, hence outside `\operatorname{im}d_f`. The reference action (6.3) has no value there; it does not pass a claimed combined finite boost test. The observer form itself passes (8.1) exactly. In degree zero `B_n=1` for every observer, so changing `n` cannot cancel the scalar support obstruction in Section 4.

For any constructed primal cocycle, the fixed perfect located pairing gives a compatible dual cocycle by the contragredient, in the packet's coordinate convention,
\[
R_D(\xi;e)=J^{-T}R_P(\xi;e)^{-T}J^T.
\tag{8.3}
\]
This is an exact algebraic pairing statement and respects groupoid composition. It neither changes `J` nor guarantees dual sitewise or inverse locality. A generic exterior boost mixes primal `|A\rangle,|B\rangle` at one site, whereas their located complements land at `x-(B+C+D)` and `x-(A+C+D)`. A naïve sitewise dual exterior action cannot hit both anchors. The forced action (8.3) includes these shifted-anchor effects. No new common-center transport has been derived that removes them while preserving the original sitewise interpretation.

The three-star distinction is intact: `J` is the fixed topological placement, `h_n` or the Lorentzian exterior form determines a metric/observer pairing, and the PR #74 scalar inverse-star no-go has its own hypotheses.

## 9. Transverse plaquette freedom is not removed

With identity linear links, define the translational plaquette mismatch
\[
\omega_{rs}^a(x;e)=e_r{}^a(x)+e_s{}^a(x+r)
-e_s{}^a(x)-e_r{}^a(x+s).
\tag{9.1}
\]
Here the affine links have linear part `I` and shift coordinates `\theta_r=e_r`, as in the owned translation chart. Then (9.1) is exactly their open translation difference for the two square paths. It is invariant under `e\mapsto e+d_f\xi` and vanishes on every pure gauge. The forward-difference curl is `\mathfrak c=L\omega`. Two root-to-site potential reconstructions differing by that square disagree by `\omega/L=\mathfrak c/L^2`. Thus this is literal path dependence, not a numerical artifact.

For actual Lorentz-linear affine links extend this definition as `\mathfrak c=L\,T_{\rm open}`. On the **flat-linear-connection subclass**, open torsion transforms as a frame vector even under affine node translations: the extra term `-F'b_y` vanishes when linear curvature `F'=0`. Consequently
\[
z_c=h_{n_x}(\mathfrak c_c,\mathfrak c_c)
\tag{9.2}
\]
is frame/observer covariant there and is an exact affine-translation scalar. It has zero value and first derivative at flat. A one-edge perturbation `e_B{}^A(0)=1` on the `L=3` test has `\mathfrak c(0)=-3e_A` and `z_c=9`, whereas all tested pure-gauge curls vanish. Transforming both `n` and `\mathfrak c` by the rational boost leaves `z_c=9` exactly.

Therefore, **if** an individually covariant positive seed term exists on a cell containing this plaquette and has a nonzero flat value, multiplying that term by `1+\lambda z_c` preserves its covariance, matter support and flat first jet while changing a transverse Hessian coefficient. For simultaneous Role symmetry, use the equally weighted sum of `z` over the corresponding plaquettes of the same cell. Positivity is preserved near flat for bounded `\lambda`. Termwise covariance is an explicit hypothesis here: invariance only of a total energy would not justify arbitrary cellwise weights.

This is a conditional modulus theorem on affine-link backgrounds, not a proposed seed energy. The vector transformation of the affine shift is not silently identified with the raw-solder row transformation (8.2); their compatibility still needs an independent axiom. At nonzero linear curvature, the inhomogeneous affine torsion law must be handled separately. No globally curved invariant or combined solder/Cartan energy is claimed. The present transport construction provides no constraint eliminating this transverse freedom.

## 10. Direct answers to all 14 primary questions

| # | Answer |
|---|---|
| 1 | There is an independent exact **pure-gauge scalar** lift (3.3), and a graded reference extension (6.3). Neither is the requested all-background local common-center action. The scalar advective class is excluded for a direct elementary-cell energy. |
| 2 | In that class `g_\xi(e)=M_\xi F_\phi D F_\phi^{-1}`; the graded benchmark is (6.4). General scalar completions add the comparison jet (5.1). |
| 3 | `(D_e g_\xi)_0[h]=-M_\xi H_0(h)D` in the scalar class; (6.5) gives the graded derivative. |
| 4 | `K_\xi=M_{\xi^2}D^2`, with full delta and non-delta matrices (4.5–4.6); for the graded benchmark use (6.5). |
| 5 | Yes exactly for the two specified pure-gauge cocycles; the mixed condition was also verified directly, including a nonzero graded commutator. |
| 6 | The graded benchmark matches every component of `H(d_f\xi)`. It does **not** prove `DW_0=H` on the full coframe space; (6.6) identifies the defect of a path-based extension. |
| 7 | The forced scalar Hessian is (4.1–4.3), including same-axis distance-two terms. A general correction changes it by `-\mathcal S-\mathcal S^T`. |
| 8 | Neither `c=1` nor `c=2` matches the forced transport. Constants-preserving completions still reject both reference laws. No unique alternative is selected; (5.1) and Section 9 exhibit different remaining freedoms. |
| 9 | No. Pure-gauge transport does not measure it, and the covariant flat-linear subclass admits the conditional plaquette multiplier (9.2). |
| 10 | The owned observer/exterior family passes the rational boost; the reference transport is not defined on the boosted raw-solder background (8.2). Combined covariance of the desired action is not established. |
| 11 | Exact as a forced typed contragredient dual action (8.3); obstructed for naïve sitewise exterior actions on both colors. The shifted anchors are retained, not repaired by changing `J`. |
| 12 | Local infinitesimal and finite-jet path stencils are explicit. Finite matrix support and inverses are generally global; uniform finite circuit depth is excluded by (7.2). Direct elementary-cell energy fails in the scalar class. |
| 13 | No. There is no all-background, observer/frame-compatible local action from which physical stress can yet be varied. |
| 14 | A geometric endpoint-comparison jet `\mathcal S:\operatorname{Sym}^2(\operatorname{im}d_f)\to\operatorname{End}(C^0)` satisfying (5.4), with constants/degree/frame/located constraints and a finite overlap-composition law. This is the first coefficient missing from a full common-center interpolation, not a new choice of `J`. |

## 11. Exact controls and proof boundaries

The appended standalone checker passed **145/145** exact assertions using rational arithmetic:

- scalar `L=3,5,7` delta and non-delta full matrices, Ward, nonzero derived `K`, mixed cocycle, the complete Hessian formula and constants;
- nonzero `L=5` same-axis distance-two entries, both reference-law mismatches, and the constant-isotropy leading path coefficient;
- finite Taylor inverse and constant-representative identities; unrestricted finite composition is proved by exact telescoping in (3.3), rather than inferred from a truncated numerical experiment;
- a two-role invariant site sector retaining **all 16 Fock states and all degrees 0–4**, with nontrivial graded mixed commutator, (6.5), parity and a simultaneous signed Role/site swap;
- `L=2` occupied one-form Nyquist response, `L=3` distinct-axis corner, a constant harmonic strain, a transverse non-pure-gauge plaquette, rational observer boost, and the located-anchor mismatch.

The scope of the checks is stated deliberately. They do not verify an unconstructed 4D all-order local law. General-period uniqueness, the support no-gos and the completeness of (5.1) are theorem-level arguments above. No Lean build or new proof ownership is claimed.

## 12. Theorem-ready handoff and exactly one next step

Proposed module names are not claims of existing proofs:

1. **`A4DScalarAdvectiveGroupoidObstruction.lean`.** On rational cyclic matrices first prove `[M_\xi,D]=-H_0(\Delta\xi)`, the mixed-constant consequence (2.5), `K=M_{\xi^2}D^2` and the exact `L=5` matrices. Define the scalar parameter-local class (2.3) explicitly, direct elementary-cell matter support explicitly, and prove the contradiction from the `(+1,-1)` Hessian entry. This needs only the finite two-jet groupoid identities, not an analytic exponential API.
2. **`A4DScalarComparisonJetFreedom.lean`.** Prove that the difference of two mixed-cocycle solutions factors uniquely through `\operatorname{Sym}^2(\operatorname{im}\Delta)`, with the matrix-output symmetry distinction; add constants and energy-Hessian formulas (5.1–5.4). Later integrate the specific unrestricted dressing as a separate conditional theorem.
3. **`A4DPureGaugeSamplingCocycle.lean`.** After a finite matrix-exponential API is available, define (3.1), prove constant-representative invariance, exact composition, constants preservation, local uniqueness in the parameter-local class, and the finite-support obstruction from constant isotropy. Extend to the graded benchmark (6.3) using the already owned PR #75 expansion, with its domain restriction explicit.
4. **`A4DCommonCenterTransportBoundary.lean`.** Package the harmonic/curl path obstruction, shifted located-dual action, and the conditional observer-covariant plaquette modulus on flat linear links. Keep any finite face-to-center interpolation law as an explicit hypothesis until constructed.

**Exactly one next step:** formalize `A4DScalarAdvectiveGroupoidObstruction.lean`, including the complete `L=5` `K` and Hessian and the direct-cell support contradiction. This converts the newly derived missing derivative and the first unavoidable scalar obstruction into an owner before another finite interpolation rule is proposed. No speculative follow-up task is opened by this memo.

Do **not** promote this result to: a full local matter action; an all-background first-jet reconstruction; a unique nonlinear energy; selection of `c=1` or `c=2`; a Spin representation; physical time; physical Lorentz stress or its conservation; Einstein equations; BOOK `F_N`; a direct `99\to matter` source; SM gauge derivation; a metric reinterpretation of `J`; or a universal no-go for inverse-free parents or all background-dependent lifts.

### Standalone exact checker

```python
"""Exact controls: scalar advective cocycle, graded pure-gauge benchmark, boundaries."""
from fractions import Fraction as F
from itertools import product
from math import factorial

checks = []


def check(label, claim):
    assert claim, label
    checks.append(label)


def eye(n):
    return {(i, i): F(1) for i in range(n)}


def add(*args):
    out = {}
    for a in args:
        for ij, value in a.items():
            out[ij] = out.get(ij, F(0)) + value
    return {ij: v for ij, v in out.items() if v}


def scale(c, a):
    return {ij: c * v for ij, v in a.items() if c * v}


def neg(a):
    return scale(-1, a)


def transpose(a):
    return {(j, i): v for (i, j), v in a.items()}


def mul(a, b):
    brows = {}
    for (i, j), v in b.items():
        brows.setdefault(i, []).append((j, v))
    out = {}
    for (i, k), av in a.items():
        for j, bv in brows.get(k, []):
            out[i, j] = out.get((i, j), F(0)) + av * bv
    return {ij: v for ij, v in out.items() if v}


def comm(a, b):
    return add(mul(a, b), neg(mul(b, a)))


def diag(v):
    return {(i, i): F(x) for i, x in enumerate(v) if x}


def apply(a, v):
    out = [F(0)] * len(v)
    for (i, j), x in a.items():
        out[i] += x * v[j]
    return out


def matrix(a, n):
    return [[str(a.get((i, j), 0)) for j in range(n)] for i in range(n)]


for L in (3, 5, 7):
    U = {(i, (i + 1) % L): F(1) for i in range(L)}
    Ui = transpose(U)
    D = scale(F(L, 2), add(U, neg(Ui)))
    Delta = scale(L, add(U, neg(eye(L))))
    D2 = mul(D, D)

    def H(h):
        return scale(F(1, 2), add(mul(diag(h), U), mul(Ui, diag(h))))

    def B(xi, h):
        return neg(mul(diag(xi), mul(H(h), D)))

    for label, xi in (('delta', [F(i == 0) for i in range(L)]),
                      ('nondelta', [F((i == 0) + 2 * (i == 1)) for i in range(L)])):
        h = apply(Delta, xi)
        G = mul(diag(xi), D)
        K = mul(diag([v * v for v in xi]), D2)
        check(f'L{L}-{label}-Ward', add(G, transpose(G), H(h)) == {})
        check(f'L{L}-{label}-derived-K', add(mul(G, G), B(xi, h)) == K)
        check(f'L{L}-{label}-constant-matter', apply(K, [F(1)] * L) == [0] * L)
        zeta = [F((i == 1) - (i == L - 1)) for i in range(L)]
        hz = apply(Delta, zeta)
        Gz = mul(diag(zeta), D)
        check(f'L{L}-{label}-mixed-cocycle',
              add(B(zeta, h), neg(B(xi, hz)), comm(Gz, G)) == {})
        def symmetric_correction(h1, h2):
            return add(*({(i, (i + 1) % L): h1[i] * h2[i],
                          (i, i): -h1[i] * h2[i]} for i in range(L)))
        corrected = add(B(zeta, h), symmetric_correction(hz, h),
                        neg(B(xi, hz)), neg(symmetric_correction(h, hz)), comm(Gz, G))
        check(f'L{L}-{label}-symmetric-jet-freedom', corrected == {})
        check(f'L{L}-{label}-correction-preserves-constants',
              apply(symmetric_correction(h, h), [F(1)] * L) == [0] * L)
        Hess = add(scale(2, mul(transpose(G), transpose(G))),
                   scale(2, mul(transpose(G), G)), scale(2, mul(G, G)),
                   neg(K), neg(transpose(K)))
        check(f'L{L}-{label}-constant-energy-second-variation', sum(Hess.values()) == 0)
        for c in (1, 2):
            check(f'L{L}-{label}-reject-reference-c{c}',
                  Hess != scale(2 * c, diag([v * v for v in h])))
        if L >= 5:
            formula = diag([(h[i] ** 2 + h[(i - 1) % L] ** 2) / 2 for i in range(L)])
            for i in range(L):
                j = (i + 2) % L
                value = -(h[i] ** 2 + h[(i + 1) % L] ** 2) / 4
                formula = add(formula, {(i, j): value, (j, i): value})
            check(f'L{L}-{label}-full-local-Hessian-formula', Hess == formula)
        if label == 'delta':
            check(f'L{L}-delta-G-square-zero', mul(G, G) == {})
            check(f'L{L}-delta-K-not-zero', K != {})
            if L >= 5:
                check(f'L{L}-delta-forbidden-same-axis-corner',
                      Hess[1, L - 1] == -F(L * L, 2)
                      and Hess[0, 2] == -F(L * L, 4))
            if L == 5:
                print('L=5 delta K:', matrix(K, L))
                print('L=5 delta W second derivative:', matrix(Hess, L))
        else:
            check(f'L{L}-nondelta-G-square-nonzero', mul(G, G) != {})
            if L == 5:
                print('L=5 nondelta K:', matrix(K, L))

    # Taylor coefficients of row-evaluation F(t*xi), with exact inverse recurrence.
    xi = [F(i == 0) for i in range(L)]
    powers = [eye(L)]
    for k in range(1, 4):
        powers.append(mul(powers[-1], D))
    for distance in range(1, min(3, (L - 1) // 2) + 1):
        check(f'L{L}-constant-isotropy-leading-entry-{distance}',
              powers[distance].get((0, distance), 0) == F(L, 2) ** distance)
    coeff = [mul(diag([v ** k for v in xi]), scale(F(1, factorial(k)), powers[k]))
             for k in range(4)]
    invcoef = [eye(L)]
    for k in range(1, 4):
        invcoef.append(neg(add(*(mul(coeff[j], invcoef[k - j]) for j in range(1, k + 1)))))
    for k in range(1, 4):
        check(f'L{L}-row-evaluation-inverse-order{k}',
              add(*(mul(coeff[j], invcoef[k - j]) for j in range(k + 1))) == {})
    # Constant representatives factor on the right by exp(cD), not on the left.
    for p in range(3):
        for q in range(3 - p):
            left = mul(diag([v ** p for v in xi]),
                       scale(F(1, factorial(p) * factorial(q)), powers[p + q]))
            right = mul(coeff[p], scale(F(1, factorial(q)), powers[q]))
            check(f'L{L}-constant-representative-p{p}-q{q}', left == right)


# Embedded two-role site torus with the full 16-state Fock carrier.
# Spectator directions C,D are site-constant, but every Fock degree is retained.
def graded(L):
    sites = list(product(range(L), repeat=2))
    site_ix = {x: i for i, x in enumerate(sites)}
    dim = 16 * len(sites)

    def ix(x, mask):
        return 16 * site_ix[x] + mask

    def shift(r, sign=1):
        out = {}
        for x in sites:
            y = tuple((v + (sign if a == r else 0)) % L for a, v in enumerate(x))
            for mask in range(16):
                out[ix(x, mask), ix(y, mask)] = F(1)
        return out

    U = [shift(r) for r in range(2)]
    Ui = list(map(transpose, U))
    Ds = [scale(F(L, 2), add(U[r], neg(Ui[r]))) for r in range(2)]
    Av = [scale(F(1, 2), add(eye(dim), Ui[r])) for r in range(2)]

    def mult(field):
        return diag([field[x] for x in sites for _ in range(16)])

    def creator(r):
        out = {}
        for x in sites:
            for mask in range(16):
                if not mask & (1 << r):
                    out[ix(x, mask | (1 << r)), ix(x, mask)] = F(
                        (-1) ** ((mask & ((1 << r) - 1)).bit_count()))
        return out

    creates = [creator(r) for r in range(4)]
    E = {(s, r): mul(creates[s], transpose(creates[r])) for s in range(2) for r in range(2)}

    def gauge(xi):
        return {(s, r): {x: F(L) * (xi[r][tuple(
            (v + (1 if a == s else 0)) % L for a, v in enumerate(x))] - xi[r][x])
                        for x in sites} for s in range(2) for r in range(2)}

    def adv(xi):
        return add(*(mul(mult(xi[r]), Ds[r]) for r in range(2)))

    def flux(e):
        return add(*(mul(mult(e[s, r]), mul(U[s], mul(Av[r], E[s, r])))
                     for s in range(2) for r in range(2)))

    def bond(r, h):
        return scale(F(1, 2), add(mul(mult(h), U[r]), mul(Ui[r], mult(h))))

    def H(e):
        z = flux(e)
        return add(*(bond(r, e[r, r]) for r in range(2)), neg(z), neg(transpose(z)))

    def bscalar(xi, h):
        return neg(add(*(mul(mult(xi[r]), mul(bond(r, h[r, a]), Ds[a]))
                         for r in range(2) for a in range(2))))

    def bgraded(xi, h):
        return add(neg(mul(flux(gauge(xi)), flux(h))),
                   comm(flux(h), adv(xi)), bscalar(xi, h))

    xi = [{x: F(r == 1 and x == (1, 0)) for x in sites} for r in range(2)]
    zeta = [{x: F(r == 0 and x == (1, 0)) for x in sites} for r in range(2)]
    h, hz = gauge(xi), gauge(zeta)
    A, Bx, G = adv(xi), flux(h), add(adv(xi), flux(h))
    Gz = add(adv(zeta), flux(hz))
    check(f'graded-L{L}-nontrivial-mixed-commutator', comm(Gz, G) != {})
    check(f'graded-L{L}-full-pure-gauge-Ward', add(H(h), G, transpose(G)) == {})
    check(f'graded-L{L}-mixed-cocycle',
          add(bgraded(zeta, h), neg(bgraded(xi, hz)), comm(Gz, G)) == {})
    Kscalar = add(*(mul(mult({x: xi[r][x] * xi[a][x] for x in sites}), mul(Ds[r], Ds[a]))
                    for r in range(2) for a in range(2)))
    Kgrade = add(Kscalar, scale(2, mul(Bx, A)))
    check(f'graded-L{L}-derived-second-jet', add(mul(G, G), bgraded(xi, h)) == Kgrade)
    for k in range(5):
        check(f'graded-L{L}-degree-{k}', all(
            (i % 16).bit_count() == k for (i, j) in G if (j % 16).bit_count() == k))
    check(f'graded-L{L}-parity', all(
        (i % 16).bit_count() % 2 == (j % 16).bit_count() % 2 for (i, j) in G))
    if L == 3:
        check('L3-owned-corner', H(h)[ix((0, 0), 1), ix((1, 2), 2)] == -F(3, 2))
    if L == 2:
        nx = [{x: F(r == 0 and x[0] == 0) for x in sites} for r in range(2)]
        nh = gauge(nx)
        nH = H(nh)
        for mask in range(16):
            if mask & 1:
                check(f'L2-Nyquist-occupied-{mask}', nH[ix((0, 0), mask), ix((0, 0), mask)] == 2
                      and nH[ix((1, 0), mask), ix((1, 0), mask)] == -2)
        check('L2-Nyquist-scalar-zero', all(i % 16 != 0 for i, j in nH if j % 16 == 0))
        check('L2-Nyquist-centered-zero', all(
            nh[0, 0][x] + nh[0, 0][((x[0] - 1) % L, x[1])] == 0 for x in sites))

    # Nontrivial simultaneous Role/site permutation A<->B.
    P = {}
    for x in sites:
        for mask in range(16):
            images = [1 - r if r < 2 else r for r in range(4) if mask & (1 << r)]
            p_mask = sum(1 << r for r in images)
            sign = (-1) ** sum(images[i] > images[j] for i in range(len(images))
                              for j in range(i + 1, len(images)))
            P[ix((x[1], x[0]), p_mask), ix(x, mask)] = F(sign)
    xi_p = [{x: xi[1 - r][(x[1], x[0])] for x in sites} for r in range(2)]
    hp = gauge(xi_p)
    check(f'graded-L{L}-Role-equivariance', mul(P, mul(G, transpose(P))) ==
          add(adv(xi_p), flux(hp)))

    def curl(e):
        return {x: L * (e[1, 0][((x[0] + 1) % L, x[1])] - e[1, 0][x]
                        - e[0, 0][(x[0], (x[1] + 1) % L)] + e[0, 0][x])
                for x in sites}
    check(f'L{L}-pure-gauge-curl-zero', all(v == 0 for v in curl(h).values()))
    transverse = {(s, r): {x: F(s == 1 and r == 0 and x == (0, 0)) for x in sites}
                  for s in range(2) for r in range(2)}
    check(f'L{L}-transverse-curl', curl(transverse)[(0, 0)] == -L)
    uniform = {(s, r): {x: F(s == r == 0) for x in sites}
               for s in range(2) for r in range(2)}
    scalar_constant = [F(mask == 0) for x in sites for mask in range(16)]
    check(f'L{L}-full-jet-uniform-strain-scalar',
          apply(H(uniform), scalar_constant) == scalar_constant)


graded(2)
graded(3)

# Rational observer boost and the pure-gradient-domain obstruction.
boost = {(0, 0): F(5, 4), (0, 1): F(3, 4), (1, 0): F(3, 4), (1, 1): F(5, 4),
         (2, 2): F(1), (3, 3): F(1)}
eta = diag([1, -1, -1, -1])
Binv = mul(eta, mul(transpose(boost), eta))
n = apply(boost, [F(1), F(0), F(0), F(0)])
en = apply(eta, n)
hn = add(neg(eta), {(i, j): 2 * en[i] * en[j] for i in range(4) for j in range(4)})
check('rational-boost-observer', mul(transpose(boost), mul(hn, boost)) == eye(4))
torsion = [F(-3), F(0), F(0), F(0)]
tv = apply(boost, torsion)
check('transverse-observer-curl-square', sum(x * y for x, y in zip(tv, apply(hn, tv))) == 9)
raw = add(mul(eta, Binv), neg(eta))
check('boost-leaves-periodic-gradient-domain', raw[0, 0] == F(1, 4) and raw[0, 1] == -F(3, 4))
check('located-anchor-boost-obstruction',
      (0, -1, -1, -1) != (-1, 0, -1, -1) and boost[1, 0] != 0)

print(f'PASS {len(checks)}/{len(checks)} exact common-center controls')
```

**Terminal verdict: COMMON-CENTER-CELL-ACTION-NEW-PRIMITIVE-REQUIRED.**
