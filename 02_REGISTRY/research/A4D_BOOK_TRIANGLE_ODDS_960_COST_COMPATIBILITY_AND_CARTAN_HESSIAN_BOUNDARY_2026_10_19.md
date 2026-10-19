# D0 → GR: 327 closed-history odds, 960 exact price-compatibility constraints, and Hessian inertia boundary

2026-10-19. **RESEARCH / EXACT GRAPH-PRICE INTERFACE / SAME SCIENTIFIC CONTEXT #334.** Base: `03bd6fed84830e72e55341cc38215c880d287357`. No native field-to-price binding, original full H+J+R source selection, raw #216, periodic GR root or `GR_closed` promotion. This standalone research note does **not** amend BOOK/CORE.

## 0. Existing owners, not a new rank discovery

The original tripartite scene topology is **already proved** in Book 01 and `03_FORMALIZATION/D0/Topology/TypedTripartiteBoundaryRank.lean`, `03_FORMALIZATION/D0/Geometry/SceneCochainComplex.lean`, `03_FORMALIZATION/D0/Topology/GenericTripartiteUniversalHomology.lean`: 33 vertices, 359 undirected edges, 1287 triangles; `rank ∂1=32`, `rank ∂2=327`, `H1=0`, `H2=ℤ^960`. Nothing in this note claims to rederive those as new D0 physics. The increment is their **native Book03 complete-history reverse-odds interpretation**, an explicit 960-constraint image test, and a narrow original 24-Lorentz-Hessian incompatibility theorem.

Read with [native Cost−Info boundary](A4D_NATIVE_COST_INFO_BOUNDARY.md), [Book endpoint cohomology](A4D_BOOK_INFO_ENDPOINT_COHOMOLOGY_FULL_GRAVITY_QUOTIENT_2026_10_19.md), [scene Perron source](A4D_SCENE_PERRON_DOOB_SINGLE_HISTORY_GOLDEN_INFO_SOURCE_2026_10_19.md), [exact mixed Cartan](A4D_DOUBLE_NULL_EXACT_FINITE_QUADRATIC_CARTAN_EINSTEIN_BOOTSTRAP_2026_10_19.md), and [quartic exact polynomial replay](A4D_DOUBLE_NULL_CUBIC_EINSTEIN_QUARTIC_AREA_WARD_2026_10_19.md).

## 1. Original additive Cost−Info yields a measured *conditional* triangle-odds invariant

On every one of the 718 directed original edges let

```text
s_theta(u,v)=C_uv-theta I_u-(1-theta)I_v,
W_theta(gamma)=phi^[-sum_(u,v) in gamma s_theta(u,v)].
```

Both primitive Costs `C_uv(y)` and vertex Info `I_v(y)` may vary with **every** physical tangent. For a real triangle with `a∈A,b∈B,c∈C`, retain both complete opposite paths **with identical starting and ending vertex**:
`gamma_+=(a,b,c,a)`, `gamma_-=(a,c,b,a)`. Then the exact all-field identity is

```text
log_phi [W_theta(gamma_-)/W_theta(gamma_+)]
 = F_abc
 = (C_ab-C_ba)+(C_bc-C_cb)+(C_ca-C_ac).
```

This holds for all θ and all derivatives without Perron selection or a chosen stationary prior: **all vertex Info and its field derivatives cancel from the clockwise/anticlockwise contrast.** Conditional probability odds of this same two-history Book-weight pair equal the unnormalized weight ratio. Equality to actually recorded Born/Book probabilities still requires the native `w=Nq` binding; no real detector action is inferred.

For the **optional**, separately defined Perron–Doob scene transfer of the current owner, the same identity holds:
`P_ab P_bc P_ca/(P_ac P_cb P_ba)=phi^(-F_abc)`, because λ and Perron eigenvectors telescope. That stochastic presentation is not logically required for the Book-weight closed-path ratio.

The sym/antisym split is exact:
```text
(s_uv+s_vu)/2=(C_uv+C_vu)/2-(I_u+I_v)/2,
(s_uv-s_vu)/2=(C_uv-C_vu)/2+(1/2-theta)(I_u-I_v).
```
Thus **all non-gradient oriented triangle data come from primitive *directed edge Costs*, not from repartitioning 33 vertex information values.** This does not imply that `DI_v` is absent from scalar pressure or that real geometric Weyl equals triangle affinity.

## 2. Explicit 960-equation image test with exact edge reconstruction

Orient the 359 underlying scene edges as `A→B`, `B→C`, `C→A`. If `a_ab=C_ab-C_ba` etc., define
`F[a,b,c]=a_ab[a,b]+a_bc[b,c]+a_ca[c,a]`. Choose reference vertices `a0=b0=c0=0`. The **necessary and sufficient** test for an arbitrary 1287-entry scalar triangle signal to come from *a single additive set of 718 original scalar edge prices* is

```text
T_abc(F) = F[a,b,c]-F[a0,b,c]-F[a,b0,c]-F[a,b,c0]
          +F[a0,b0,c]+F[a0,b,c0]+F[a,b0,c0]-F[a0,b0,c0] = 0
```

for each `a≠a0,b≠b0,c≠c0`. There are exactly `8·10·12=960` independent tests. **Sufficiency is constructive**: set

```text
a_ab[a,b]=F[a,b,c0]
a_bc[b,c]=F[a0,b,c]-F[a0,b,c0]
a_ca[c,a]=F[a,b0,c]-F[a,b0,c0]-F[a0,b0,c]+F[a0,b0,c0].
```

Then the generated full 1287-array equals `F` iff the 960 tests vanish. Consequently `rank(edge→triangle)=1287-960=327`, with the known 32-dimensional vertex-gradient kernel, agreeing exactly with the *existing Lean* `H1=0,H2=960` owners. The new result is a **typed operational rejection criterion** for an alleged native *scalar additive edge-price* source: a nonzero triple contrast proves it cannot arise that way (without ruling out non-additive memory, phases, Wilson holonomies, or other original channels).

## 3. A sharp no-shortcut theorem: positive Perron pressure cannot be the entire indefinite Palatini Hessian via affine prices

For the positive primitive scalar transfer `K_uv=phi^(-s_uv)` on the 718 allowed edges, `p(s)=log_phi ρ(K(s))` satisfies the exact finite-Markov asymptotic-variance formula

```text
D²p(s)[a,a] = ln(phi) lim_(N→∞) (1/N)
    Var_(π,P) [ sum_(j=0)^(N-1) a_(Y_j,Y_(j+1)) ] ≥ 0.
```

The variance is zero exactly when `a_uv=c+b_u-b_v`; the Hessian has `718−(1+32)=685` positive quotient directions. Under the **extra conditional** hypothesis `C_uv=C_vu`, the θ=1/2 transfer is symmetric and the Perron process reversible. An antisymmetric perturbation changes `K_t` into `K_{−t}^T`, so `p(t)=p(−t)`; its 327 non-gradient cycle directions have **zero first** and **positive second** pressure responses. This is a useful candidate signature for *orientation memory visible at second order despite a vanishing first vacuum source*, not an established Weyl-to-Book field map.

The already-owned original homogeneous 24-link Palatini Hessian `M` has exact spectrum `2^[4],−2^[4],1^[8],−1^[8]`, inertia (12 positive, 12 negative), determinant 256. For any **affine** map from all 24 Lorentz coordinates to edge prices, `s(ω)=s0+Lω`, the scalar-positive-Perron-pressure pullback Hessian `Lᵀ D²p L` is positive semidefinite. Neither its nonzero positive nor negative multiple can equal `M` on the 24 independent directions. Therefore:

**NOGO (scoped):** an *affine-edge-price, scalar-positive-Perron-pressure-only* action cannot be the full 24-link original Lorentz–Palatini quadratic action.

This excludes no genuine D0 full price: nonlinear `s(ω)` contributes `Dp · D²s`; the original full `H+J+R`, physical preparation/work/clock/measurement, and memory/complex sectors are not captured by scalar Perron pressure.

## 4. One consuming test rather than new quartic polynomials

Reuse original all40 `840×1008` local rational saved-vector replay from `03bd6fe` (all 15 monomials through amplitude degree 4 on one nonperiodic section). Obtain from **one admitted** physical record an actual typed `(e,U,Psi,clock,prep)→(C_uv,I_v)`. Evaluate native forward/reverse triangle odds and all 960 triple contrasts at both mixed `[ab]` Weyl (`A⊥B,w≠0,d=0`) and parallel `A∥B,d≠0` controls. If nonzero triple contrast appears, classify it as **failure of additive one-edge Cost−Info realization for that proposed triangle readout**, not a GR no-go. If the array is edge-derived by definition, the constraints pass automatically and provide only a regression check; physical admission remains unproved. Compare the actual complete `40+matter` Book source to the *same*-programme star/CAR covector, preserving normalizer and independent preparation/clock. Use `M^{-1}` only in its verified 24 spatially constant directions. An exact match with geometric closed-form `δω(ab),H3,J3,σ4,χ4` must still undergo all 840 finite spatial-row checks; the continuum form and a restricted projected rank do not replace them.

**Status:** EXACT GRAPH-PRICE INTERFACE; pressure-inertia NOGO restricted as above; **not** a physical source or Cartan-to-scene map; `GR_closed=false`.


## 5. NEW direct extraction from the actual saved finite quartic representative

This is distinct from the Book triangle theorem, but resolves one immediate requested finite-vs-closed-form comparison without another polynomial solve. Read the actual pinned `quartic_full_spatial_jet_solution.json` at parent `03bd6fe`, using its official ordering (672 link coefficients at spatial degree≤6, then 336 coframe coefficients at degree≤5, coframe entry row-major and monomials x^i y^j ordered by total degree then descending i). At `[a²b²]` exactly 118 link coefficients and 20 coframe coefficients are nonzero.

The saved coframe representative is **not literally** the continuum `sigma4,chi4` closed form from `check_quartic_full_ricci.py` in the same untransformed coframe coordinates. Specifically:

```text
[2,2]delta e^+_u = (3/128)(x²+xy+y²)
                  +(3/256)(x³+x²y+xy²+y³)
[2,2]delta e^2_x = -(7/256)y²-(9/128)xy²-(1/128)y³
                   +(3/128)x²y²+(1/256)y⁴
[2,2]delta e^3_y = 0
```

By contrast, the continuum candidate has `sigma4=-(x²+y²)²/128` in the null-leg scale and `chi4=3(x²+y²)²/1024` in each transverse conformal leg (for `A=(1,0), B=(0,1)`). Thus the saved rational vector is **not already a coefficientwise encoding** of that compact ansatz. One may not infer a no-go for the compact solution: the `840×1008` equation has a solution family, the saved vector is one representative, and a nontrivial kernel/gauge/coordinate transformation may map one to the other. No such transformation has been constructed or tested by this note. The only certified statement is the literal mismatched representative. This is pinned by [the exact checker](sources/d0_book_triangle_odds_2026-10-19/check_saved_quartic_normal_form.py).

The next correct finite task is therefore a **gauge-aware range test**: insert `delta omega(ab),H3,J3,sigma4,chi4` in the original full 40×15 polynomial checker, allow only genuinely owned gauge/kernel lifts, and determine whether the proposed compact coefficient is in the saved solution's affine space. Avoid declaring equality based on the already solved rank alone. Still `GR_closed=false`.
