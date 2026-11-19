# D0 — exact noncommuting global temporal-Lorentz holonomy constraint and constructive link reconstruction

22 October 2026. Existing Draft #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `constitutive/native-programme-v1`. This is an exact all-order finite theorem for the ORIGINAL based-temporal-plaquette/spatially homogeneous **temporal gauge U_time=I** in the non-VSI rank-two sector. It extends the published covariant time-difference owner (`A4D_RANK2_FULL_N1_CQ_42_SOURCE_FINITE_CONSISTENCY_2026_10_21.md`, §7; `sources/d0_star_rank2_seam_2026-10-21/check_whole_slab_cartan_compatibility.py`) from one-site first jets to a NECESSARY AND SUFFICIENT global nonlinear link/collar criterion. It does not solve the full 16+24+2 system, derive temporal gauge from M1, or choose the compulsory Book03 action. `GR_closed=false`.

## 1. Original based-temporal plaquettes and their exact nonabelian product law

Take the actual original 4×4 **proper Lorentz** link words on each of a finite sequence of time nodes `j=0,...,N`, with a spatially homogeneous profile and temporal link `U_time(j)=I` in the declared original chart. For any one of the three ORIGINAL spatial link roles `a=1,2,3`, the true based 4-edge temporal plaquette is

\[
\boxed{P_j=U_a(j+1)U_a(j)^{-1}\in SO^+(1,3).}\tag{1}
\]

(If the true input includes nontrivial `U_time`, (1) must be replaced by its COMPLETE gauge-covariant 4-edge word with its actual moving observer. No free gauge fixing is assumed.) Since the order matters, define the time-ordered product

\[
\mathcal H(P)=P_{N-1}\cdots P_1 P_0.
\]

Then the FULL nonlinear telescoping identity is exact:

\[
\boxed{\mathcal H(P)=U_a(N)U_a(0)^{-1}.}\tag{2}
\]

**Global reconstruction theorem (no infinitesimal assumption).** Given ANY complete target family `P'_j∈SO+(1,3)`, a UNIQUE full sequence of proper-Lorentz spatial links `U'_j` sharing BOTH the original initial `U_0` and final `U_N` exists if and ONLY if

\[
\boxed{P'_{N-1}\cdots P'_0=U_NU_0^{-1}.}\tag{3}
\]

It is constructed by the ORIGINAL forward recursion

\[
\boxed{U'_0=U_0,\qquad U'_{j+1}=P'_jU'_j.}\tag{4}
\]

No squared-distance penalty, new boundary action, invented source or site-by-site independent choice. On an open chart of the true original Lorentz group, (3) has precisely six independent constraints per spatial link role; for all three roles there are 18. One may use `P'_0,...,P'_{N-2}` as the true independent curvature variables and set

\[
P'_{N-1}=U_NU_0^{-1}(P'_{N-2}\cdots P'_0)^{-1}.
\tag{5}
\]

This gives an explicit global smooth chart of dimension `6(N-1)` per spatial role and is a finite diffeomorphism with the original interior link coordinates. The old `24-link at one site` isolated inverse is **not** equivalent to this global chart because it need not satisfy (3) and because changing interior links also changes neighboring temporal plaquettes and the spatial plaquettes.

## 2. Exact first linearization, all link directions and the missing six-dimensional cokernel

Let `Z_j=δU_j U_j^{-1}∈so(1,3)` for an actual unrestricted proper-Lorentz variation preserving both fixed temporal collar endpoints, `Z_0=Z_N=0`. Let `C_j=δP_j P_j^{-1}∈so(1,3)`. Differentiation of the TRUE based word (1) gives

\[
\boxed{C_j=Z_{j+1}-\mathrm{Ad}_{P_j}Z_j.}\tag{6}
\]

This is exactly the existing owner’s `δP_j/h²=Z_{j+1}P_j-P_j Z_j` when the actual link correction is `δU_j=h²Z_j U_j`, without dropping either endpoint term or replacing noncommuting Lorentz transport by a scalar derivative.

For arbitrary Lie-algebra-valued source data `C_j`, the forward solution with `Z_0=0` is uniquely

\[
Z_m=\sum_{j=0}^{m-1}
\mathrm{Ad}_{P_{m-1}\cdots P_{j+1}}C_j,
\quad m=1,\ldots,N.
\tag{7}
\]

The second ORIGINAL fixed collar is preserved **if and only if** the transported total source is zero:

\[
\boxed{\sum_{j=0}^{N-1}
\mathrm{Ad}_{P_{N-1}\cdots P_{j+1}}C_j=0.}\tag{8}
\]

Therefore the exact covariant temporal difference

\[
\mathcal D_P: (Z_1,\ldots,Z_{N-1})\mapsto(C_0,\ldots,C_{N-1})
\]

has **zero kernel** and a precisely **6-dimensional cokernel** for each spatial role:

\[
\boxed{\operatorname{rank}\mathcal D_P=6(N-1),\qquad
\operatorname{codim}\operatorname{im}\mathcal D_P=6.}\tag{9}
\]

No generic-rank or nonresonance hypothesis is required. Indeed, the first `N-1` output rows are block-triangular with identity on the main diagonal; the last six rows encode (8). This is a genuine global boundary mode, not an arbitrary numerical null vector. Across three spatial link roles, the space of admissible temporal-plaquette perturbations has **18 exact holonomy compatibility constraints**. The original unrestricted temporal-link and coframe gauges remain to be treated on their own typed carrier.

## 3. Uniform causal inverse on the exact image and the actual O(h) coframe-source scaling

Write `N=T/h` time intervals over a fixed positive physical extent T and choose any submultiplicative matrix norm. Assume the actual original proper-Lorentz links and their inverses have an ALREADY chart-valid common bound `||U_j||,||U_j^-1|| ≤ K`. Then for all `m,j` the product transported by (7) equals `U_m U_{j+1}^-1` and

\[
\left\|\mathrm{Ad}_{P_{m-1}\cdots P_{j+1}}\right\|\le K^4.
\]

Consequently on the TRUE compatible target image (8),

\[
\boxed{\|Z\|_\infty\le NK^4\|C\|_\infty
=TK^4\|C/h\|_\infty.}\tag{10}
\]

This explicit finite inverse is bounded UNIFORMLY under refinement for source currents of the natural form `C_j=h c_j`, `||c||∞≤C0`. The owner’s demonstrated smooth `h²Z` link adjustment produces precisely such an `O(h)` normalized temporal-plaquette differential:

\[
\frac{\delta P_j}{h²}=Z_{j+1}P_j-P_jZ_j
=h[\partial_t Z+[Z,F]]+O(h²)
\]

for smooth bounded `Z`, `P_j=I+hF_j+O(h²)`. A one-site isolated correction gives instead the incompatible O(1) source `−P_jZ_j` and cannot be justified by the local 24×24 Jacobian. Equations (8)–(10) are the exact global cure for **that** omitted finite neighbor-coupling, not a claim that the full geometric Euler inverse has been proved.

## 4. Direct link to the same-action full N1 42-system — do not drop the hidden global equation

For any genuine scalar action built from original temporal plaquette and spatial coframe/Lorentz faces, the Euler coframe+link rows must be differentiated through the ACTUAL map (1)–(4). In the temporal-plaquette part, a covector `G_j∈so(1,3)^*` contributes to the interior link equation the proper adjoint difference

\[
\boxed{E_{U_j}^{(0a)}=G_{j-1}-\mathrm{Ad}_{P_j}^{*}G_j,}
\tag{11}
\]

plus all spatial-plaquette/coupled-coframe terms of the SAME action. In the globally reconstructed curvature variables, the allowed target variations are restricted by (8), not all `6N` freely varied plaquettes. Arbitrary scalars fit to cancel the missing boundary mode are forbidden.

**Strategic conjunction with the separate exact two-real temporal-CAR theorem:** the same existing N1 price now has (i) a unique positive-inverse temporal material block and an exact Schur residual and (ii) a constructive noncommuting temporal Lorentz link/plaquette change of variables with EXACT fixed-collar compatibility and uniform inverse bound on its image. This removes two mathematically independent causes of an invalid one-cell proof, and identifies the remaining genuine target as the coframe/curvature Euler on the joint constrained image plus the native spatial matter and field-writer equations.

The existing short-slab 42-row numerical roots, positive scalar Hessian and link rank tests remain valuable SEEDS; (3) and (8) explain which global compatibility equation a quantitative interval-Newton or nonlinear gauge-fixed theorem must include to promote them to real finite roots. The changed coordinate map does not establish existence by itself and does not import continuous-Einstein equations or solve the original Book03 physical price/selection.

## 5. Exact computational validation

The runnable checker uses the original 4×4 `eta=diag(1,-1,-1,-1)` and ALL SIX genuine proper-Lorentz generators. Noncommuting rational Cayley words define three authentic based temporal plaquettes. It verifies exact (2) and (3) for perturbed interior links; changing just one plaquette violates the real final collar; the exact linearized covariant source has rank `12` in `18` rows with exactly six codimension; one in-image perturbation is reconstructed and a deliberately incompatible right-hand side is rejected. The original one-site O(1) spike versus coherent O(h) cancellation is checked as a separate exact noncommuting 2×2 algebraic identity. Every check is symbolic exact rational SymPy, not float matrix tolerances. Normal and Python `-O` outputs are byte-identical.

Reproduce: `OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_native_temporal_holonomy_global_2026-10-22/check_native_temporal_holonomy.py`. The source was author tested on the printed carrier; full N1 16+24+2, actual allowed temporal gauge, nonvacuum refinement, oldRIGHT/clock and compulsory Book03 absolute Info remain open. No promotion; `GR_closed=false`.
