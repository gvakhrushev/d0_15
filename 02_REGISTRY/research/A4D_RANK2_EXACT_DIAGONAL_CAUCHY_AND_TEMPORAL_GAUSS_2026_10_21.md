# Finite D0 rank-two GR continuation: FOUR exactly solved diagonal coframe rows, two material Euler rows, and six exact temporal-link Gauss zeros

21 October 2026. Existing Draft PR #334, native-programme-v1 / constitutive. **CONSTRUCTIVE FINITE ORIGINAL-ACTION CAUCHY THEOREM IN A SCOPED SPATIALLY HOMOGENEOUS SECTOR.** No new action, matter, coupling, geometry carrier, observer, null-zone assignment, field writer or physical Book03 price. Consumes the literal original six based Cartesian G2/STAR action and the correctly retyped SAME N=1 Golden scalar CQ price; all claims pertain to the exact common f_star=q_CAR=0 sheet. Not an all42 finite stationary root. GR_closed=false.

## 1. The missing Cauchy first integral is FORCED by two genuinely independent material variations

Use the already-owned original two nonzero real CAR scalar/top gradients on a spatially homogeneous diagonal coframe with time t and first space direction x:

    e(t)=diag(X(t),Y(t),Z(t),W(t)), X,Y,Z,W>0;
    p_t(t)=D_t^+ psi1(t) !=0, p_x=D_x^+psi2=epsilon !=0;
    all other original two-real-field components of D^+psi are zero.

The exact original real Lorentz Clifford contraction is

    q = p_t²/X² - epsilon²/Y².

The original fixed positive AF/PF weights rho are arbitrary and may be discontinuous, but on the ACTUAL double-zero field sheet f_star=q=0 the full N=1 Golden CQ first source is the globally constant nonzero gradient M*tau (a Dsum f+b Dsum q) (the full nonlinear MASTER K and higher second jets are NOT deleted). Consequently the two original scalar Euler rows are exactly the backward-adjoint conservation equations for the ACTUAL currents

    J_t=p_t/X²,      J_x= -epsilon/Y².

The spatial material row is automatically zero for homogeneous Y. The nontrivial time row forces J_t=constant with the original time boundary convention. Simultaneously q=0 requires p_t=epsilon X/Y on the chosen positive nonzero-gradient branch. Hence

    BOX: J_t=epsilon/(XY)=const, so XY=const.                 (1)

This is a mathematical CONSEQUENCE of the original two-field finite Euler and null cancellation, not an extra imposed unimodular constraint. The old historical rank-two seed has XY=1, so select that existing initial/boundary constant and write Y=1/X. The finite material increment is thereby FORCED to be p_t=epsilon X². Integrating those increments constructs the real chronological scalar history; the second remains psi2=epsilon*x.

## 2. Exact original six-face reduced density: 4 diagonal Euleri are only 3 different equations

On this ORIGINAL branch retain the old spatial boost links (all three genuine independent spatial outgoing Role links)

    U_t=I,
    U_x(t)=exp(h k1(t) K1),
    U_y(t)=exp(h k2(t) K2),
    U_z(t)=exp(h k2(t) K3),

with K1,K2,K3 the original proper Lorentz boosts, full noncommutative based spatial P_yz and time-spatial faces. Their k2 equality is a symmetry restriction, NOT an independent Lorentz equation or a claim of physical equality of all link components.

Let

    S1=sinh(h[k1(t+h)-k1(t)]),
    S2=sinh(h[k2(t+h)-k2(t)]),
    C12=C(h*k1,h*k2), C22=C(h*k2,h*k2),
    C(x,y)=sinh(x)sinh(y)[1-(cosh(x)-1)(cosh(y)-1)/2].

At a based time cell with coframe diag(X,Y,R,R), the ORIGINAL 6-face G2/STAR density is exactly

    f_star,h= [R² S1 + 2Y R S2 + 2X R C12 + X Y C22]/h².     (2)

This is exact at arbitrary finite h and retains the actual nonlinear P-P^-1/2 odd curvature. No continuum Einstein density was substituted. The original material q=p_t²/X²-epsilon²/Y² has NO independent proper-link derivative.

Before imposing the field ansatz in variations, differentiate the ORIGINAL action with respect to all four diagonal coframe components (two transverse variations independent) and the two scalar fields. At XY=1, p_t=epsilon X² and the EXISTING native ratio kappa=-lambda_minus, epsilon²=1/(2*kappa), the true normalized affine Euler components at f=q=0 are

    h² E_X = 2R C12 + C22/X -h² X,                         (3a)
    h² E_Y = 2R S2 + X C22 +h² X³,                         (3b)
    h² E_Z = h² E_W = R S1 + S2/X +X C12.                 (3c)

The equality E_Z=E_W is the k2=k3, Z=W symmetry; they are separately computed ORIGINAL Euler rows, not one variation restricted to a single R. The source is the first variation of the SAME N=1 actual scalar price by the exact f=q=0 theorem.

The exact local coframe homogeneity/Noether relation on q=0 is

    X E_X +Y E_Y+Z E_Z+W E_W=2 f_star,h.                  (4)

It follows that solving ALL FOUR diagonal Euler rows forces f_star,h=0 automatically. This is stronger than selecting f=0 first and testing only its radial derivative. It also shows why the old double-zero source projection is an exact consequence of the true stationarity equations on this branch.

## 3. Explicit TWO algebraic equations + ONE forward connection recursion

Take the original smooth rank-two seed on a fixed positive-radius interval:

    A(r)=sqrt(r) exp(-r²/4),
    B(r)=1/A(r),
    k1^0(r)=(1-r^-2)/2,
    k2^0(r)=exp(-r²/4)/sqrt(r),
    dr/dt=exp(-r²/2).

Prescribe only the SAME k2(t)=k2^0(r(t)) and one initial k1(t0)=k1^0(r0). From (3a,b), X,R are obtained by TWO exact algebraic equations

    2R C12 + C22/X=h² X,
    2R S2 +X C22=-h² X³.                                (5)

Eliminating R gives the exact quadratic in the existing variable z=X²>0:

    BOX: h² C12 z²+(h² S2+C12 C22)z-S2 C22=0.           (6)

Use the positive branch near the original A(r)^2, not an arbitrary negative/remote algebraic root. The transverse coframe equation (3c) then supplies a unique future value of the ORIGINAL proper-Lorentz boost link

    BOX: k1(t+h)=k1(t)
       + asinh[-(S2/X+X C12)/R]/h.                        (7)

This is a COHERENT one-step recurrence: a spatial link on time t+h is shared by the preceding and following original based faces. The one-site replacement k1(t+h) is never made separately for two neighboring plaquettes. The equations are local initial-value equations. Their terminal time value is OUTPUT; they do not solve a second, arbitrarily imposed temporal Dirichlet collar.

### Exact analytic regularity and nondegeneracy interval

Divide equations (5) by h² and take h->0 in a smooth original frame. The limiting two algebraic equations are

    E1(X,R;k1,t)=2R k1 k2+k2²/X-X=0,
    E2(X,R;k1,t)=2R dot(k2)+X k2²+X³=0.                  (8)

At the unchanged source seed X=A(r),R=r,k1=k1^0(r), BOTH vanish exactly. The determinant of their original X,R Jacobian is

    BOX: det D_(X,R)(E1,E2)
       = -2(r^4-2r²-1) exp(-3r²/4)/r^(7/2).             (9)

It is STRICTLY POSITIVE for every 0<r<sqrt(1+sqrt(2)) ≈1.553773974. Therefore on ANY compact subinterval of that domain, the implicit-function theorem defines unique positive real near-source X(t,k1,h),R(t,k1,h). At r=sqrt(1+sqrt(2)) this particular algebraic chart loses invertibility; it is NOT automatically a physical singularity of spacetime or a failure of full D0.

Equation (7) defines a smooth Cauchy map, and its h->0 evolution is precisely the old physical k1 flow:

    dot(k1)=-(dot(k2)/X+X k1 k2)/R,
    dot(k1^0)=exp(-r²/2)/r³.                             (10)

Standard local consistency and discrete Gronwall on a fixed finite t interval imply

    sup|X_h-A|+sup|R_h-r|+sup|k1_h-k1^0|=O(h).             (11)

This is for the just-defined constrained forward recursion with prescribed k2(t), fixed initial k1 and the original bounded positive-radius chart. It does not control a full 40-variable gauge-fixed Jacobian or an independently fixed final collar.

Equations (1)-(7) then give the EXACT finite result on all free based time cells:

    f_star,h=0, q_CAR,h=0,
    E_X=E_Y=E_Z=E_W=0,
    E_psi1=E_psi2=0.                                      (12)

The original volume det(e)=R² is positive and differs by O(h) from the old r² volume, unlike the preceding determinant-r²-preserving projection. This change is a legitimate correction of existing ORIGINAL coframe components; preserving the old r² was never an independent native Euler equation. The full metric approaches the old rank-two non-VSI continuum metric in the same chart.

## 4. Additional exact six time-link Gauss zeros on this VERY geometry

A second exact structural result explains why all original temporal proper-link source entries were zero in each of the independent full4 matrix controls. For ANY spatially homogeneous diagonal coframe and the original time link U_t=I, with Ui(t) and Ui(t+h) on a single SO(1,1) boost subgroup Ki for each i=1,2,3, vary the original temporal link at one spatial address by δU_t=X U_t for an arbitrary original Lorentz generator X.

It enters one based temporal-spatial face at that address with

    P_out=V W^-1, dP_out=X P_out,

and the spatial predecessor face with the SAME diagonal coframe at its based site and

    P_in=V W^-1, dP_in=-V X W^-1,

where V=Ui(t+h), W=Ui(t) COMMUTE because they belong to the same Ki subgroup. The original true odd curvature differential is

    dR(P)[dP]=(dP+P^-1 dP P^-1)/2.

The total differential of these TWO actual based faces is

    dR_out+dR_in
      =[X V W^-1+W V^-1 X-V X W^-1-W X V^-1]/2.          (13)

For diagonal coframe the complementary-wedge G2/STAR contraction of the (t,i) face projects ONLY onto the internal Ki component. Split an arbitrary Lorentz X into its Ki part and the other five generators: the Ki part COMMUTES with V,W so (13) vanishes, while each perpendicular generator remains outside the (t,i) 2×2 block under conjugation by V,W and has zero Ki projection. Hence each spatial direction's outgoing/predecessor pair has ZERO original first source from every X.

Therefore, on this specific homogeneous diagonal/pure-boost sector,

    BOX: E_(U_t,X_ab)=0 FOR ALL SIX original Lorentz generators X_ab,     (14)

exactly at every free spatially homogeneous site, for arbitrary smooth or nonsmooth time profiles of X,Y,R,k_i. This does NOT rely on the other Euler equations, f=q=0, or the new recursion. It is a true finite Gauss-type identity with both neighboring based plaquettes included. The same trace result also follows from the original finite local Lorentz Noether architecture; it is NOT six newly independent constraints or license to discard six more rows on an arbitrary inhomogeneous field.

The six exact projections are additionally checked with rational original Lorentz boosts and all six generators on each of three Role directions. They are not an assertion that ALL twenty-four independent links are solved. Spatial link Euleri remain generally nonzero even on the new exact Cauchy branch.

## 5. Independent ORIGINAL six-face 4x4 numerical replay and its honest residual

The standalone [finite Cauchy checker](sources/d0_star_rank2_seam_2026-10-21/check_diagonal_coframe_cauchy_recurrence.py) pins the ORIGINAL six-face G2STAR matrix calculator and the actual full N=1 GoldenMaster (K_pre=9, L_gate=20). It symbolically verifies the exact Jacobian (9), continuum flow (10), elimination polynomial (6), radial Ward identity (4) and forced CAR first integral (1). It constructs the algebraic-positive branch and shared next-time boost link by (5)-(7), never requiring a full 40x40 inverse.

The original 4x4 full based-holonomy calculation then verifies q=0 and f=0 at EVERY free temporal cell, and independently differentiates each original diagonal coframe entry with the real CAR forward increments held fixed. Three compact, genuinely curved radius intervals [1,1.2], [0.85,1.15], [0.9,1.4] were tested with n=16,32,64,128 cells. Representative largest deviations on [1,1.2]:

| n | max |X-A| | max |R-r| | max |k1-k1^0| | max off-diagonal coframe Euler |
|---:|---:|---:|---:|---:|
| 16 | .00142211 | .01877531 | .00074399 | .00696776 |
| 32 | .00070911 | .00937059 | .00038965 | .00348381 |
| 64 | .00035401 | .00468085 | .00019920 | .00174190 |
| 128 | .00017686 | .00233929 | .00010069 | .00087095 |

On each same run the actual original six-face star zero and all four diagonal coframe source components have floating point error no more than the 1e-9-1e-10 thresholds declared in the executable, and the two real CAR Euler currents are analytically conserved. The off-diagonal coframe source remains NONZERO, as do the spatial proper-link sources, so there is no all42 stationarity claim.

The independent random-diagonal/full4 source replay further shows all SIX temporal-link Euler entries vanish below rational/complex arithmetic tolerance even without any of the above coframe roots. The exact proof (13)-(14) is the basis of the claim.

**Result accounting:** 4 ORIGINAL diagonal coframe +2 scalar Euler +6 temporal-link Euler = 12 raw original finite Euler COMPONENTS exactly zero on the constructed branch; 30 raw components remain. Six exact local Lorentz Noether identities relate components of the complete 40 geometrical source, and can NOT be subtracted a second time as though independent of the six solved temporal-link rows. The analytical existence theorem covers this homogeneous single-direction Cauchy branch, not fixed arbitrary final coframe, not general 4D fields and not the physical H+J+R/D0 Book licence. GR_closed=false.

## 6. The correct next joint problem

This result makes the earlier "39 remaining independent fields" and random one-site 24x24 Cartan inverse framing obsolete ON THE DECLARED RANK-TWO HOMOGENEOUS SECTOR. The next actual map is the remaining off-diagonal coframe and spatial-link Euler covector, evaluated on the EXACT 12-component zero branch (with all real CAR currents preserved); its homogeneous/inhomogeneous gauge and boundary compatibility can be tested separately. If the complement lies in the image of the whole-slab gauge-fixed Jacobian, a true 42-root may be continued. An O(h) residual alone does not imply this.

The original null Brinkmann all40 exact family and the genuinely physical compulsory Book03 price, clock/observer/preparation/oldRIGHT and primitive field writer remain distinct accepted/open carriers. Do not infer a universal physical full GR theorem from this homogeneous recursion. The analytic fold rcrit is a chart limit, not a metric singularity. Preserve the genuine original PF irregularity and the exact source retyping; no sigma-plus detector is physically chosen here.


## 7. Exact original Euler SUPPORT: only 18 components remain potentially nonzero

For this SAME spatially homogeneous diagonal-coframe, pure three-boost link and two independent CAR scalar-gradient sector, the remaining source can be reduced further by a finite structural theorem **before** solving another equation. This is not a stochastic rank scan and uses NO approximation in h.

At every based face, the original finite odd curvature \((P-P^{-1})/2\) lies in a small invariant Lorentz Lie subalgebra:
- the temporal-spatial face (0,i) is a pure boost \(K_i\), because both endpoint spatial links lie in the same 1-parameter boost subgroup;
- the spatial face (i,j) is inside \(\mathfrak{so}(1,2)\) on the exact three-dimensional subspace span(e0,ei,ej), hence its bivector components can lie ONLY in \(K_i,K_j,J_{ij}\). The fourth internal direction is acted on identically.
This statement is exact for arbitrary finite boost exponents and all based plaquettes, not just a first curvature Taylor coefficient.

The ORIGINAL diagonal based coframe gives a complementary wedge on the two Role legs u,v. Differentiating one leg \(e^a{}_\mu\) can meet the above curvature support only when the corresponding internal unordered index-pair is its Hodge complement. An exhaustive exact six-face combinatorial certificate therefore gives the EXACT source support

  Coframe (potentially nonzero): 
    (a,mu)=(0,0),(1,1),(2,2),(3,3),(1,0),(2,0),(3,0).
  Coframe identically zero:
    all other 9 of the original 16 independent components.

For the original 24 spatial/temporal Lorentz left-link source components, Section 4 already proves 6 temporal-link Gauss zeros EXACTLY. Three additional spatial-link rows vanish EXACTLY by the same subgroup-support argument: at U_x, the generator J23; at U_y, generator J13; at U_z, generator J12. To see this without restricting the link tangent, choose an actual based spatial plaquette containing Ui and Uj. Every unvaried link acts on span(e0,ei,ej) and identically on the orthogonal fourth internal axis k. A tangent \(J_{jk}\) with j,k perpendicular to i necessarily has at least one internal index OUTSIDE that 3D invariant subspace in each plaquette that contains Ui; multiplying by any existing unvaried group element keeps it outside. It cannot affect the Lie component \(J_{ij}\) to which the original diagonal complementary coframe projects that spatial face. The temporal-spatial face similarly projects only Ki and is already covered by the six temporal-link zeros. These are source identically-zero statements for all original proper-Lorentz variations, not an assertion that the three links or their holonomies are trivial.

Thus the complete original 42-component FIRST Euler covector in this declared rank-two homogeneous sector has the exact support count BEFORE using any stationarity:

| Original field component | Exact structural zeros | Potentially nonzero |
|---|---:|---:|
| 16 coframe | 9 | 7 |
| 24 left-Lorentz link | 6 temporal +3 spatial =9 | 15 |
| 2 real scalar | 0 generically | 2 |
| TOTAL | 18 | 24 |

The new Cauchy recurrence of Sections 2-3 then makes all four diagonal coframe entries and both material Euler zero EXACTLY. Therefore, on its constructed nonflat TWO-stream null-kinetic Cauchy family:

  BOX: at most 18 original Euler COMPONENTS can remain NONZERO,
       namely three (a,mu)=(1,0),(2,0),(3,0) coframe rows
       and fifteen spatial proper-Lorentz left-link rows.

The exact six local SO^+(1,3) Noether identities relate these components; they are NOT six additional independent equations to subtract blindly. In the original all4x4 numerical replay, all nine forbidden coframe and all nine forbidden link source entries are zero at machine precision even for random nonsymmetric diagonal-coframe/pure-boost controls; the permitted three off-diagonal and multiple permitted spatial-link entries are genuinely NONZERO at small finite h. In particular a reduced action varied ONLY inside diagonal tetrads and prescribed boosts cannot promote this statement to a full42 root: the remaining 18 must be tested as independent ambient variations with the original neighbor faces.

This is the practical architectural reduction: the next source solver needs a small, exact **18-slot observed residual**, not a blind all42 search or one-site 24x24 inverse. This says nothing about whether those 18 slots lie in a globally compatible gauge-fixed field-writer image with a fixed two-ended temporal collar. GR_closed=false.
