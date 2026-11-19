# Fixed-measure complete price: density rigidity, all-cap critical-set equivalence and the general Einstein–dust sector

21 October 2026. Existing research owner: Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, constitutive/native-programme-v1.
Input snapshot: `086fab99d8aaed7f712e9a3d2858c516b61901fc`.

**New result:** the already declared continuum two-density price has a previously unused on-shell Ward constraint. Combined with the original local coframe trace equation, it forces BOTH densities to be spacetime constants for every local field solution in the regular chart. For the literal detector this holds on the existing cap-independent interval, for every fixed finite cap. Thus the complete local field critical sets of all those prices are identical, not just their previously constructed Bianchi-I members. In the aligned timelike scalar sector their field equations are exactly Einstein–irrotational-dust equations with a determined volume/current relation. An arbitrary-function inhomogeneous non-VSI example is checked through all ambient field rows.

**What this is not:** the fixed-measure continuum dictionary and all moving field queries have not been derived as compulsory native Book03 physics. The action in this proof is precisely the continuum action already supplied in `d0_complete_price_explicit_dynamics_2026-10-21`, with its physical source-binding restrictions. No new action, entropy law, volume degree of freedom, constraint imposed before variation, controller or geometric coefficient is chosen. No original finite-lattice lift, independent upstream root, physical admission or `GR_closed` claim follows. The result closes a full coupled FIELD-equation calculation for that given model, not the parent native-selection premise.

## 1. Exact inherited model and the unresolved statement it now consumes

The original complete-price normal form gives a stationary auxiliary reduction of a local price depending on two oppositely scaling densities. Its explicit-dynamics continuation constructed constant-density Bianchi-I solutions and a matter propagation formula with the **reduced metric held fixed**. It did not classify all coupled field solutions and explicitly did not identify the held-metric propagation with the full coupled system.

We keep that action and its measure literally. Let e be a nondegenerate coframe, Ω an INDEPENDENT proper Lorentz connection, and ψ=(ψ₁,ψ₂) the original two real scalar/top fields. Put

    g=eᵀηe,  v=√|det g|,
    q=g^{μν}Σ_A ∂_μψ_A ∂_νψ_A,
    x=η₀² (v/ϖ) R(e,Ω),     y=−η₀² q,
    I_F=∫ ϖ F(x,y) d⁴x.                                      (1)

Here η₀>0 is the existing query-scale constant, not the Lorentz matrix η. The positive external density ϖ is fixed. The literal inherited action has ϖ=1. Allowing general ϖ in (1) is only a tensorial bookkeeping device to identify the fixed-volume Ward identity; ϖ is NOT a new variational field. Setting it back to 1 changes nothing. In particular, the matter integrand does NOT gain a factor v.

All coefficients, discrete caps, actual internal parameters and η₀ are held fixed in these continuum field variations. A genuinely field-dependent or nonuniform compiler coefficient, an independently varied internal parameter, nonlocal density coupling, additional curvature invariant, or extra preparation/work term must be retained separately and can change the following Ward identity. The inherited native admission/source-binding gap is not erased.

The literal specialization is

    p=(√5−1)/2, z=2⁻²⁰,
    B(y)=4(p+p²y)²[1−(p+p²y)²],
    ℓ(E)=4E(1−E),
    A(x,y)=ℓ(p²(1+x))+[1−ℓ(p²(1+x))]B(y),
    r(x,y)=1−[1−zB(y)][1−zA(x,y)],
    F_N(x,y)=V_N(r(x,y)),
    V_N(r)=α[κ−βh_φ(r)] Σ_{j=0}^{N−1}(βr)^j.                (2)

The same actual unit-charge conditions α>0, 0<β≤1, κ>53 and finite fixed N≥1 are consumed. Field-independent price baselines are kept as values but do not affect these field equations. This is not a claim that those conditions or the fixed measure have been derived for arbitrary native Book valuations.

## 2. Two exact on-shell identities, derived before any ansatz or elimination

### 2.1 The original local coframe trace

Use a compactly supported local scale variation e↦exp(εσ/2)e while Ω and ψ are held independently fixed. In four dimensions v scales by exp(2εσ), R(e,Ω) by exp(−εσ), and q by exp(−εσ). Since Ω is independent, no derivatives of σ enter this variation. Consequently

    δx=σx,  δy=−σy,
    x F_x − y F_y = 0                                      (3)

at every full field critical point. This is an actual Euler consequence, not a restriction of the variation domain. For F_N=V_N(r), V_N′≠0 gives exactly the previously owned trace equation

    T(x,y):=x r_x−y r_y=0.                                 (4)

### 2.2 The missing fixed-volume Ward integral

Choose any compactly supported coordinate vector ξ and vary ALL dynamical fields by their Lie variations, including the Lorentz connection as a one-form. Keep ϖ fixed, as required by (1). With div_ϖ ξ=ϖ⁻¹∂_μ(ϖξ^μ),

    δx=ξ^μ∂_μx+x div_ϖ ξ,    δy=ξ^μ∂_μy.

Therefore, after one integration by parts,

    δI_F=∫ϖ[ξ·∂F+xF_x div_ϖ ξ]d⁴x
         =∫ϖ ξ·∂(F−xF_x)d⁴x.

On a solution of ALL coframe, connection and matter equations this vanishes for every such ξ. Thus

    dH_F=0,      H_F(x,y):=F(x,y)−xF_x(x,y).                (5)

This proof does NOT assert full active diffeomorphism invariance of the fixed-measure theory. It is its on-shell background-volume consistency condition. Equivalently one may use a transforming external density as a spurion; varying that density is not added to the physical equations. Freezing matter or the independent connection would invalidate this use of full stationarity.

## 3. General local theorem: any regular two-density price freezes its densities on shell

Let F be C² in a neighborhood of (0,0), with

    a=F_x(0,0)≠0,   b=F_y(0,0)≠0.

Define T_F=xF_x−yF_y. At the zero-density point,

    D(T_F,H_F)|₀ = [[a,−b],[0,b]],
    det D(T_F,H_F)|₀ = ab ≠ 0.                            (6)

The inverse function theorem supplies a neighborhood where (x,y)↦(T_F,H_F) is one-to-one with nonsingular Jacobian. Equations (3) and (5) then imply:

> **Density-rigidity theorem.** On each connected field region whose densities remain in that neighborhood, every full stationary solution satisfies x=x_* and y=y_* with constant x_*, y_*. No spacetime symmetry, constant-curvature condition, homogeneous scalar profile, or prior restriction of variations is assumed.

The constants are solution-sector integration data, not new couplings inserted into F. The spacetime metric and R itself need NOT be constant: x fixes vR/ϖ, not R. The theorem covers all C² local F in this regular class, not just the Golden valuation. At a more general point, nonsingularity of D(T_F,H_F) is the precise sufficient condition. No conclusion is made at a singular branch or for F_xF_y=0.

This also explains why a nonlinear two-density price need not introduce a new propagating local density scalar after the other gravitational equations are enforced. It is a statement about the coupled system, not about a matter equation on an externally fixed background.

## 4. Strong uniform application to the actual detector: every finite cap, whole owned branch

The original radial owner proves on |y|≤2⁻¹² and |x|<1/4:

    x=τ(y) is the unique solution of T=0,
    r_x>0, r_y>0, V_N′≠0,
    M_N(y)=V_N′(r(τ(y),y)) r_x(τ(y),y),
    |d_y log|M_N||<202.                                  (7)

The values and all-cap proof, not just numerical samples, are already owned. Different caps may have different constant α,β,κ satisfying the same stated inequalities.

Restrict the NEW Ward integral to the trace branch:

    H_N(y)=V_N(r(τ(y),y))−τ(y)M_N(y).

Differentiate using the actual chain rule and τr_x=yr_y:

    H_N′=V_N′r_y−τM_N′
        =V_N′r_y[1−y d_y log|M_N|].                       (8)

The bracket is strictly greater than

    1−202/4096 =1947/2048 >15/16.                          (9)

Thus H_N′ never vanishes on the ENTIRE owned branch, for EVERY admitted finite N. Its sign is negative for N=1 and positive for N≥2, but either sign gives strict monotonicity. Together with (4)–(5), this removes any need to assume constant densities in the explicit-dynamics packet: they are FORCED by the full equations throughout this common branch.

The same argument applies to the bare detector price F=r and to the literal local determinant valuation F=−log(1−r). For the latter,

    d_y log|M|=r̄′/(1−r̄)+d_y log r_x,

and the owned r̄′<5z, |d_y log r_x|<192, z<r̄<2z keep the bracket positive. The local determinant is NOT identified with the entire physical H+J+R/Book price.

## 5. Exact equivalence of the full local field critical sets, not equality of scalar prices

Let I_r=∫ϖr(x,y)d⁴x. For any full solution of I_{F_N} in the branch, (8) implies x,y constant, so r=r_* and V_N′(r_*) is one nonzero spacetime-constant number. For ANY compactly supported ambient field variation, including one that leaves the constant-density family,

    δI_{F_N}=V_N′(r_*) δI_r.                              (10)

Thus the same fields solve every Euler equation of I_r. Conversely a full I_r solution has constant densities by the same Ward/radial argument and (10) shows it solves I_{F_N}. Therefore, with the SAME fixed measure, field dictionary, boundary-variation class and no extra independently varying ledger,

    Crit(I_{F_N}) = Crit(I_r) = Crit(I_{F_M})               (11)

for all fixed finite N,M on the stated branch. Also Crit(I_{−log(1−r)}) is the same set. This is an all-order exact **equation-level** transport among these existing valuations. It is stronger than checking common specially constructed constant-density cosmologies. It is not an off-shell equality of first sources or prices, a cap-optimization theorem, or a statement about extrema versus saddles.

For general F, the same result gives Einstein-form equations below but the constant sector relation F_y/F_x can differ. Equality (11) uses a COMMON actual detector r and the proved nonzero Ward slope; an arbitrary reassigned Info/work depending on other variables is outside it.

### 5.1 The full coupled linearized equations

Linearize (3),(5) at one regular full solution. The density-map Jacobian is invertible (on the native branch det D(T,H_N)=T_x H_N′≠0). Therefore any full Jacobi field has spatially constant δx and δy. Compactly supported perturbations have δx=δy=0.

At a common background root the Hessian identity is

    δ²I_{F_N}[v,w]=V_N′ δ²I_r[v,w]
                     +V_N″∫ϖ δr[v]δr[w]d⁴x.             (12)

For a full Jacobi field v, δr[v] is constant; the extra term is then V_N″δr[v]δI_r[w]=0 for every allowed test w. The converse uses the I_r Ward identity. Hence the local full Jacobi kernels also agree under these conditions. The whole Hessians are NOT asserted equal; their negative directions and cap-dependent radial stability remain. No global Cauchy well-posedness, uniform mesh inverse, or stability theorem is inferred.

The previously derived K_N″-dependent propagation equation holds with the transformed metric artificially fixed. It cannot alone supply the coupled physical sound cone: the full system imposes δY=constant, as the next derivation makes explicit. There is no contradiction with that owner's scope.

### 5.2 Nonuniform real costs: the exact source is retained, with a cap-one exception

The constant-parameter premise is not cosmetic. If a supplied external ledger parameter ζ varies in spacetime, the same Lie-variation calculation gives

    d(F−xF_x)=Σ_A F_{ζ_A} dζ_A.                            (12a)

A field-independent baseline B(ζ) occurs on BOTH sides and cancels; it is not discarded by declaring the background fixed. For the literal finite-cap price with fixed α,β but a spatially varying actually charged κ, the trace branch is still x=τ(y), and (12a) becomes

    H_{N,y} dy=τ αβ E_N′(βr̄) r_x dκ.                     (12b)

In particular E_1′=0: the density rigidity survives arbitrary unequal κ at cap one because that part of the actual price is an additive field-independent baseline. For N≥2 it generally does NOT. The full source of varying actual prices is displayed, not assumed zero. More generally every varying α,β or genuine external source parameter contributes τ∂_ζ(V_N′r_x)dζ. This is consistent with the already-owned special N=1 same-spatial-source result; it does not identify this continuum measure with its finite native site weights.

## 6. Independent reduced-equation proof and exact Einstein matter interpretation

Consume the existing stationary auxiliary normal form, without adding its variables as physical fields:

    I_eff=∫[a_N η₀² √|g̃| R(g̃,Ω)+ϖ K_N(Y)]d⁴x,
    Y=−η₀² q(g̃,ψ),   a_N≠0,   K_N′(Y)≠0.              (13)

The Lorentz connection equation gives the torsion-free connection of g̃. Writing X_{μν}=Σ_A ∂_μψ_A∂_νψ_A and W=(ϖ/√|g̃|)K_N′, the remaining equations are

    a_N G_{μν}(g̃)=W X_{μν},
    ∇_μ(W∂^μψ_A)=0.                                     (14)

A direct divergence calculation, with commuting scalar second derivatives, is

    ∇^μ(WX_{μν})
      =Σ_A[∇_μ(W∂^μψ_A)]∂_νψ_A +(W/2)∂_νq.             (15)

The actual Bianchi identity plus all matter equations therefore gives dq=0. Since K_N′≠0, dY=0. The inherited monotone map Y=y/u_N(y) then gives dy=0, and x=τ(y) gives dx=0. This is a second derivation of the rigidity using the actual field equations.

Returning to the ORIGINAL fields, the constant F_x and F_y give exactly

    Ω=Ω_LC(e),
    G_{μν}(g)=(ϖ/v) κ_* X_{μν},
    ∂_μ(ϖ g^{μν}∂_νψ_A)=0,
    κ_*=F_y(x_*,y_*)/F_x(x_*,y_*) .                      (16)

For the literal common r, κ_*=r_y/r_x is positive, independent of cap, and the original radial equation fixes x_*=κ_*y_*. At the null center the ratio is the already-owned native detector ratio. Away from it κ_* depends on the density sector; no universal fixed Newton constant or unproved original continuum normalization is assigned.

### 6.1 Aligned timelike matter: arbitrary irrotational Einstein dust

If ψ_A=n_A φ with a constant internal unit vector n and q_*>0, define

    u_μ=∂_μφ/√q_*,
    ρ_eff=κ_* q_* ϖ/v.

Then (16) is precisely

    G_{μν}=ρ_eff u_μu_ν,
    u^μu_μ=1,
    ∇_μ(ρ_eff u^μ)=0,
    u^μ∇_μu_ν=0.                                         (17)

The last identity follows from the constant norm of a gradient. There is no separately inserted dust action or Lagrange multiplier, and no cosmological term is generated by a field-independent fixed-measure baseline. For two NON-aligned scalars retain the two currents and their constant TOTAL kinetic norm; do not call that sector one dust fluid. The null branch is distinct and includes the inherited Brinkmann matter family.

Conversely, any smooth positive-density irrotational Einstein-dust solution with Λ=0 has a LOCAL representation of this aligned sector before caustics, with the specified volume/current relation. In synchronous comoving coordinates (τ,z^i), conservation says ρ_eff v=F(z)>0. Fix a small y_*<0 in the owned branch, q_*=−y_*/η₀² and κ_*=τ(y_*)/y_*. A local purely spatial coordinate map with Jacobian F(z)/(κ_*q_*) makes ρ_eff v=κ_*q_* while preserving τ. Set φ=√q_*τ. Then y=y_* and x=−η₀²κ_*q_*=τ(y_*) and all equations follow. This constructs a representative relative to the declared fixed measure; it does not prove full Diff invariance, a global chart, native moving weights, or physical availability of that coordinate adjustment.

The linear fixed-volume scalar/dust mechanism is known in TDiff literature (e.g. de Cruz Pérez–Maroto, arXiv:2504.02541v2, 10 July 2025). What is newly proved here is the direct nonlinear two-density Ward rigidity, its uniform use on the actual Golden all-cap branch, and exact full critical/Jacobi-set equivalence for these completed prices. No general Einstein-dust solution is claimed newly discovered.

## 7. An arbitrary-function inhomogeneous NON-VSI exact check of every field row

To avoid a homogeneous or null-only test, use coordinates (t,s,z,w), s>0, |z|<1, and any smooth b(s) on a patch where

    T=t−b(s)>0,   D=T−2s b′(s)>0.

Let A>0 and

    ℛ(t,s)=A s^(1/3)T^(2/3),
    ds²=dt²−ℛ_s² ds²−ℛ²[dz²/(1−z²)+(1−z²)dw²].          (18)

This is a standard marginally-bound LTB dust geometry, not a new spacetime discovery. Direct Christoffel/Ricci computation gives

    G_tt=4/(3TD),  every other G_{μν}=0,
    R=−4/(3TD),  v=A³TD/3,
    vG_tt=4A³/9,
    C_{hat0 hat1 hat0 hat1}=−8s b′/(9T²D).                (19)

For b′≠0, the Weyl tensor is nonzero and varies in space; Ricci and the scalar R are nonzero as well. This is not a VSI witness and not restricted to polynomial gravitational waves.

Choose the original small sector y_*<0, x_*=τ(y_*), and set

    q_*=−y_*/η₀²,
    A³=−9x_*/(4η₀²)=9κ_*q_*/4,
    ψ₁=√q_* t,  ψ₂=constant.                              (20)

Then the literal query densities (1) are x=x_*, y=y_* and the metric source is

    v r_x G_{tt}−r_y q_*
       =−(x_*r_x−y_*r_y)/η₀²=0.                         (21)

All other metric components vanish; the diagonal coframe and its independently constructed proper Lorentz spin connection satisfy all 24 Cartan equations; both fixed-measure scalar Euler equations vanish. Thus ALL 16+24+2 continuum field rows of every admitted fixed-cap I_{F_N} vanish, including lapse and arbitrary ambient variations. No restriction to the (18) ansatz is made before variation. The same original fields and connection work for every cap.

The checker derives the 4D Ricci tensor before imposing the arbitrary-function ℛ, constructs the antisymmetric spin connection and verifies every torsion component, then substitutes (18). It also checks that wrongly replacing the scalar measure by v would give a NONZERO scalar residual ∂_t(v√q_*). This protects the actual nondensitized dictionary instead of silently correcting it to standard k-essence.

## 8. Parent substitution, limits and genuine remaining work

This removes three specific mathematical assumptions in the explicit complete-price dynamics packet:

1. Constant detector densities are now consequences of the FULL field equations, not an ansatz used to find one cosmology.
2. Equality across caps is now equality of the entire regular local field critical sets, not just common specially constructed roots.
3. The nonlinear reduced K_N does not independently supply the full coupled matter propagation law; its density mode is constrained by Bianchi. Full Jacobi kernels are the same across these valuations on the regular chart.

The result therefore lets a physical application establish an appropriate **class of local two-density valuations** instead of literal off-shell equality of a very particular entropy functional, provided the actual process really descends to this fixed-measure continuum action and its full admitted field variations. It does not prove that descent. Actual spatial compiler weights, moving query primitives, absolute Book anchoring, independent preparation/observer/work/clock equations and the original finite-lattice lift remain unproved here. Native H+J+R with extra spectral terms is not silently declared a function of only x,y. A field-dependent coefficient or nonlocal record coupling can reintroduce an explicit Ward residual.

No parent physical premise is promoted by the statistical observation or by the fact that (18) is a solution of GR. The new theorem is the full on-shell reduction of the already given nonlinear complete-price continuum model. `GR_closed=false`.

## 9. Validation and reproducibility

`check_complete_price_ward.py` was executed normally and with `python -O`; all explicit checks stay active in both modes and the stdout/JSON agree byte for byte. Checks include the exact generic Ward/radial algebra, original Golden polynomial identities, application of the inherited ALL-cap monotonicity bounds, 85-digit diagnostics at positive/zero/negative density points, the full arbitrary-function LTB Ricci/Weyl computation, 16 coframe and 24 torsion and 2 scalar source checks, and the hostile scalar-measure change.

The finite cap/parameter samples are diagnostics, not the proof for every N; that theorem consumes the pinned analytic |d_y log|M_N||<202 bound. The Jacobian/monotonicity and variational proof above establish the universal statements. This is an author check, not independent review, a new Lean build, a rerun of primary all128 spectral/finite-lattice suites or physical acceptance.
