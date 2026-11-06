# D0: a joint density map and the general smooth first source of the existing complete cut price

27 October 2026. Existing research owner: `gvakhrushev/d0_15`, Draft #334.
Input branch head: `28811643e84b474384fb08cb31dce18ca050e30f`.

**Result at its actual scope.** On the existing supplied coframe/link/CAR source interface, one invertible four-dimensional density transformation simultaneously identifies the geometric numerator and the nondensitized scalar kinetic moment with Palatini and minimally coupled scalar densities. Combining the unchanged full-CAR geometric error with the actual two-band polynomial reporter and the complete cut-Hodge heat+feedback price gives a uniform first-source comparison on bounded general smooth field charts, not just the common-null family. The original positivity norm forces a small-signal scale on the full material moment interface. This is a mathematical composition of a specified candidate execution. Native input/gate admission, the physical metric dictionary, literal Book heat selection, and nonlinear solution recovery are NOT silently inferred. `unconditional_GR_closed=false`.

## 0. Inputs, not new physics

All repository paths below are pinned at the input head unless a different owner pin is specified.

1. `A4D_PARITY_RESOLVED_GEOMETRIC_SOURCE_GLOBAL_2026_10_27.md`: the all-SL4 parity identity and the explicit polynomial difference between the original full CAR trace and the odd Palatini density. The original full trace is retained here; no new parity gate is required.
2. `A4D_FULL_TWO_BAND_FIXED_TEN_SIGN_CAR_CHOI_SOURCE_2026_10_21.md`, equations (1), (8)–(16): the actual polynomial probability, supplied inverse-coframe/link source moments, genuine material moment, full-Hilbert positivity bound, and its field-independent attenuation. These source-resource assumptions remain visible.
3. `sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/proof.md`, equations (3)–(12): the exact original cofactor map, orientations and units.
4. `sources/d0_coupled_cut_partition_2026-10-22/COUPLED_PARTITION_PROOF.md` at `438abae40fd6008e486504a31f92867084ebc1ba`: the complete cut Hodge price, all harmonic modes, gain, true PF weighting and refinement.
5. `A4D_COMPLETE_BOOK_SOURCE_FIXED_INITIAL_APPLICATION_2026_10_27.md`: nonlinear constrained execution-state lift, its fixed-initial hypothesis, and the distinction between genuine independent inputs and generated states.
6. `A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md`, section 9: the earlier vacuum-only coframe map and the failure of that particular radial map for the nondensitized matter query. The map below is different: it first reads the actual inverse-coframe numerator, not a nonlinear correction to the previous density.

The target of this calculation is not another CAR rank or a geometry-only solution. It is the full source of the specified heat-plus-feedback scalar on the same existing source operands.

## 1. Exact density involution: no extra field and no lost coframe direction

Work in one original Role-coordinate chart with an oriented nondegenerate real coframe matrix e, E=det(e)>0, and the original Lorentz form eta, det(eta)=-1. Let g=e^T eta e. Define

    T(e)=e_tilde=E^(-1/2)e.                                    (D1)

Then

    det(e_tilde)=E^(-1), T(T(e))=e,
    g_tilde=E^(-1)g,
    det(e_tilde) g_tilde^(-1)=g^(-1).                          (D2)

The full derivative is

    DT_e[v]=E^(-1/2)[v-(1/2)e tr(e^(-1)v)].                    (D3)

In the 16-dimensional coframe matrix space, the rank-one determinant lemma gives

    det(DT_e)=E^(-8)[1-(1/2)tr(I_4)]=-E^(-8) != 0.             (D4)

This is an invertible variable transformation, not a restriction to det(e)=1, not the removal of a conformal mode, and not an additional scalar degree of freedom. All coframe variations survive. Links and matter are left unchanged.

**Coordinate/physical boundary.** D1 is stated in the fixed native Role chart. If e is already declared an ordinary coframe under arbitrary spacetime diffeomorphisms, e_tilde is not automatically an ordinary coframe under that same transformation law: det(e) has a density weight. Equivalently, one may take e_tilde as the continuum coframe and induce the transformation law of e by the involution. This is mathematically consistent and invertible, but a physical D0 metric readout must actually support that dictionary. It is NOT proved that g and g_tilde are operationally identical. They have the same null cone and agree on the old det(e)=1 solution family, but their volume/length readouts differ in general. No hidden background-density invariance is assumed.

## 2. The unchanged geometric moment already has the right density for e_tilde

Use the exact original inverse-leg operands and orientation:

    U_inv=[u_0 ... u_3]=nu eta e^(-T),
    d=det(U_inv)=-nu^4/E,
    N_rs=(u_r u_s^T-u_s u_r^T)eta,
    B_rs(e)=-(h^2 nu^2/d)N_rs=(h^2 E/nu^2)N_rs.                (D5)

The independent link plaquette is the original four-edge P_rs. Define

    f(B,P)=-tr_4[B(P-P^(-1))]/4,
    a(N,P)=-Tr_16[dGamma(N)Lambda(P)]/8.

By quadratic coframe homogeneity and D2,

    B_rs(e_tilde)=B_rs(e)/E=(h^2/nu^2)N_rs.                    (D6)

Therefore the parity-resolved moment, using the exact already-proved trace identity, satisfies on ALL proper Lorentz plaquettes

    f(N_rs,P_rs)/(nu^2 h^2)
        = h^(-4) f(B_rs(e_tilde),P_rs).                       (D7)

No density denominator has been thrown away. The original *unweighted* actual moment is

    f_mom,h = sum_(r<s) a(N_rs,P_rs)/(nu^2 h^2).               (D8)

The consumed polynomial residual is

    a(N,P)-f(N,P)=tr_4[adj(I-P)NP]/8.                         (D9)

On a bounded smooth coframe/connection chart with det(e) bounded above and away from zero, actual small-loop P-I=O(h^2), and uniformly bounded smooth field variations, N=O(1), DN=O(1), DP=O(h^2). Hence

    f_mom,h = h^(-4) sum_faces f(B_rs(e_tilde),P_rs)
               + O_C1(h^4).                                (D10)

Here C1 refers to the field functional and bounded smooth variations, not arbitrary lattice UV tangents. The proof uses ||adj Y||<=||Y||^3 and ||D adj(Y)[Z]||<=3||Y||^2||Z||. Before dividing by nu^2 h^2 the error is O(h^6), including its first variation. N carries an exact factor nu^2. A field-independent native nu_h>0 may depend on h; that factor cancels from the error after division. A field-varying nu requires its own derivative. The original units are retained.

Thus the OLD full16 source need not be replaced by a new parity-weighted physical instrument. D10 supplies its actual error on general smooth fields.

## 3. The same map fixes the matter density exactly

The existing material moment is

    q_mom,h = sum_A g^(mu nu) D_mu^+Psi_A D_nu^+Psi_A,
    A=0,15,                                                  (D11)

with the original site/PF factors transported as in the owner. It is nondensitized in the original g. By D2, however,

    q_mom,h = det(e_tilde) sum_A g_tilde^(mu nu)
                                D_mu^+Psi_A D_nu^+Psi_A.      (D12)

This is the usual minimally coupled scalar kinetic DENSITY for the same e_tilde as in D7. It holds pointwise before imposing matter, Cartan or Einstein equations. All sixteen coframe and both matter derivatives agree, including the determinant derivative. The connection remains independent and there is no scalar spin/torsion source.

D12 concerns the actual massless two-component kinetic query, not an arbitrary potential or a different matter action. A potential requires its own density map.

**Why this differs from the old radial failure.** The old vacuum map scaled a coframe in a theory with f(e) of degree +2 and q(e) of degree -2. Here the actual inverse-coframe geometric numerator has degree -2, the SAME as q_mom(e). D1 maps both to degree +2 densities in e_tilde. We have not claimed that arbitrary finite nonlinear functions of the two densities become linear under a radial change.

## 4. Small signal is forced by the existing full-input norm bound

The ten-sign owner uses a field-INDEPENDENT bound

    Lambda_h >= max(||H_f,h||,||H_q,h||),
    epsilon_h := eta_h^2 = 1/(64 Lambda_h).                   (D13)

This is an operator bound on the complete supplied source-input Hilbert space, not merely a bound on smooth classical field values.

There is a simple normalized witness forcing ||H_q,h|| to grow. Use the existing source section with one material component psi_x=+a0 at a site and psi_(x+hat1)=-a0 at its spatial neighbor, all other forward differences at that site zero, a0=1/8, and fixed allowed flat coframe. The actual CAR state at each site is

    m_x=sqrt(p)|1>+psi_x|0>+sqrt(1-p-psi_x^2)|14>.

For S sites, the whole bank S^(-1/2)sum_x |x>m_x is normalized and the already-owned moment (13) returns exactly psi_x. On the two independent material copies used in H_q, together with the fixed coframe programme copies, its expectation at the chosen site is

    q_mom,h=-4 a0^2/h^2=-1/(16h^2).                          (D14)

Consequently ||H_q,h||>=1/(16h^2), and

    epsilon_h <= h^2/4.                                      (D15)

If the bounded inverse-PF factor 1/rho_x is included inside the source operand rather than applied afterward, the same proof gives epsilon_h<=rho_max h^2/4. Fixed nonzero original metric/nu normalization multiplies these constants but does not change O(h^2).

The witness is a normalized input for the EXISTING moment operator. It does not assert that a physical same-initial closed evolution can produce this high-frequency material state. That assertion is unnecessary for a lower bound on the full-Hilbert operator norm used by the existing positivity construction. Conversely, if a different construction bounds only a reduced physical subspace excluding this state, D15 must be reproved there. The present result uses exactly D13's full-input contract.

No new attenuation is chosen to fit gravity. The existing positivity normalization itself implies epsilon_h -> 0 under this source interface. A norm bound may grow faster, making the physical gain smaller; none of the following statements deletes that gain.

## 5. Compose the unchanged complete polynomial report before differentiating

The original finite report is

    E0=p^2(1+x), u=p+p^2 y,
    ell=4E0(1-E0), b=4u^2(1-u^2), A0=ell+(1-ell)b,
    r(x,y)=1-(1-z b)(1-z A0), z=2^-20.                       (D16)

Write r0=r(0,0), r_f=partial_x r(0,0)>0 and r_q=partial_y r(0,0)>0. The already-owned exact coefficients give

    lambda=-r_q/r_f
      =-2p^(-5)(R_E/Q_E+p^6)
      =-23.416406751884074972895582... .                       (D17)

At each true site x retain its actual positive, FIELD-INDEPENDENT PF density rho_x. On a unit coordinate-volume domain write v_h=h^4, sum_x v_h rho_x=1, and assume the actual covered PF refinement has fixed 0<rho_min<=rho_x<=rho_max<infinity. The same execution's conditional READY average is

    rbar_h=sum_x v_h rho_x
        r(epsilon_h f_mom,h,x/rho_x,
          -epsilon_h q_mom,h,x/rho_x).                       (D18)

This includes all sites, not uniform Born priors. Taylor's theorem on the actual polynomial gives, on any bounded C1 smooth field chart,

    rbar_h=r0+epsilon_h r_f I_h+O_C1(epsilon_h^2),
    I_h=sum_x v_h [f_mom,h,x+lambda q_mom,h,x].                (D19)

Proof: the constant term sums to r0 by the true density normalization. Each first-order rho_x cancels its own inverse-PF source factor. The second-order remainder is bounded by C epsilon_h^2 sum_x v_h/rho_x, and its field derivative has the same order because epsilon_h and rho_x are fixed on the chart. Uniform bounds on f,q and their first field variations suffice. If weights or attenuation move WITH the field, their actual derivatives must be kept and D19 in this form is not asserted.

## 6. The full thermal and return price has the same GENERAL smooth source

Keep exactly the previous three-status cut construction, all harmonic modes, full oldRIGHT multiplicity s_R=128, and beta=2p^2. Let a_h be its actual READY probability. For one scalar report r put

    q=(1-a_h, a_h(1-r), a_h r), f(q)=4q(1-q),
    Z_h(r)=M_h W_h-6+2 sum_(j=1)^3 exp[-beta f(q_j)],
    B_h(r)=beta^(-1)log[s_R Z_h(r)]
                         -s_R sum_(j=1)^3 log[1-z f(q_j)].    (D20)

This is the WHOLE specified cut-Hodge/feedback scalar. It is not merely the reporting cost and not the independently defined tensor/spatial heat. The actual physical source is D B_h(rbar_h).

At n>=20 the owned READY weights obey a_h=2F_(n+1)p^(n+3), so 1/3<a_h<7/20. The owned full thermal estimate gives eta<1/80000 when M_h(W_h-2)>=3661675227. Let

    kappa_h=B'_h(r0)>0, G_h=kappa_h epsilon_h r_f.              (D21)

The lower bound is uniform in all those carrier dimensions. On 0<=r<=1/4,

    B'_h(r)>=4(1-eta)s_R z(1-2z)(1/3)^2 > 0.                (D22)

For completeness, the full probability Hessian gives a uniform bound on |B''_h(r)|. Put Zmin=3661675227 and

    C2=s_R[8z/(1-z)+16z^2/(1-z)^2]
          +(32beta+16)/Zmin+192beta/Zmin^2.

Then |B''_h(r)|<=2(7/20)^2 C2. This retains the derivative of the thermal normalizer. The ratio sup|B''_h|/kappa_h is therefore uniformly bounded, even as the true number of work modes grows.

Define ONLY AS AN ANALYTICAL COMPARISON the calibrated scalar

    Jcal_h=[B_h(rbar_h)-B_h(r0)]/G_h.                         (D23)

B_h(r0) is still paid in the actual action; no physical counterterm is inserted. At each fixed h, the subtracted number and G_h are field independent, so D Jcal_h=(D B_h)/G_h and stationary field equations are unchanged. Comparing different ranks/clocks still uses the full absolute prices; D23 does not authorize dropping those variations.

Substitute D19 in D23 and use D21–D22 and the full second derivative bound:

    ||Jcal_h-I_h||_C1 <= C epsilon_h.                         (D24)

A direct derivative proof is

    D Jcal_h = [B'_h(rbar_h)/kappa_h]
                      [D rbar_h/(epsilon_h r_f)],
    B'_h(rbar_h)/kappa_h=1+O(epsilon_h),
    D rbar_h/(epsilon_h r_f)=D I_h+O(epsilon_h).

This is a statement about the complete specified price on a GENERAL bounded smooth coframe/link/matter chart, not equality restricted to f=q=0 and not inference from the previous one-dimensional CAR fixture.

## 7. End-to-end mathematical consequence

By D10, D12, D15 and D24,

    Jcal_h = S_Palatini+scalar,h(e_tilde,U,Psi)
                   +O_C1(epsilon_h+h^4)
            = S_Palatini+scalar,h + O_C1(h^2).                (D25)

The target uses the original six oriented faces, original shared links and original two scalar components; its matter term is the density D12. For smooth sampled links and regular coframes, the ordinary small-loop expansion and Riemann sums give a general continuum consistency remainder (conservatively O(h) for uncentered forward sampling; better orders require the actual midpoint conditions). Thus

    (D B_h)/G_h -> D S_Palatini+scalar(e_tilde,omega,Psi)      (D26)

uniformly on the declared bounded smooth charts. At the identity coframe the original contraction is one-half the Ricci scalar; this fixes the same orientation/normalization convention as the existing null-family equation. The continuum scalar is

    S = integral d^4x det(e_tilde)
       [ (1/2) R(e_tilde,omega)
          +lambda sum_A g_tilde^(mu nu) partial_mu Psi_A partial_nu Psi_A ]. (D27)

Vary omega BEFORE identifying it with Levi-Civita. For nondegenerate tetrads and this spinless matter term its equation is torsion freedom, yielding the compatible connection. Then the metric and two matter equations are

    G_mu_nu(g_tilde)=-lambda T_mu_nu,
    T_mu_nu=2 sum_A partial_mu Psi_A partial_nu Psi_A
                 -g_tilde_mu_nu sum_A (partial Psi_A)^2,
    Box_(g_tilde) Psi_A=0.                                  (D28)

One can derive the metric equation directly from delta(sqrt(-g)R) and delta(sqrt(-g)g^mu_nu): the latter is sqrt(-g)[delta^mu_(alpha)delta^nu_(beta)-(1/2)g^mu_nu g_alpha_beta]delta g^alpha_beta. No Einstein tensor is used to define the native report, map T or gain. All these are independently specified above. The standard Palatini variational interpretation is background mathematical context; this packet does not claim a new proof of the general Palatini theorem.

### What source consistency DOES establish about solutions

If a family of actual fixed-initial executions realizes these same fields and price, has all its true independent upstream equations satisfied, and has exact stationary discrete field sources with a sufficiently strong smooth convergent interpolation, D26 implies that its limit satisfies D28. One tests stationarity against every compatible sampled compactly supported smooth variation and passes through the uniform estimate. This is a conditional soundness theorem on genuinely smooth convergent sequences.

Source consistency alone DOES NOT construct such exact discrete stationary sequences near every continuum solution, give uniform inverse/Hessian estimates after gauge fixing, or control UV/non-smooth branches. It is not a two-sided solution-recovery theorem. The existing exact Brinkmann family is retained, but no new general exact finite-root search is claimed.

## 8. What this removes and what is still physical

This composition removes the earlier **general-field density mismatch** of the raw inverse-coframe geometric numerator and the nondensitized massless matter query, and extends the COMPLETE cut price's smooth first-source comparison beyond the special common-null family. Unlike changing the action to match a target, it uses the existing polynomial response, existing full heat/return formula, and a single invertible algebraic dictionary. The source smallness follows from the original full-input norm construction, not a fitted gravitational coefficient.

The following actual interfaces remain unproved by this packet:

- preparing the full supplied coframe/link/material resource banks by the allowed native closed word, with the stated complete initial boundary and truly admissible variations;
- selecting the physical metric/density readout D1 and its induced coordinate transformation law, rather than silently treating two conformally related metric readings as the same measurement;
- identifying the selected Book03 heat and actual total apparatus valuation with the declared full cut construction, or proving a source-equivalent stationary-section transport; real additional field-dependent work/clock/preparation terms must be bounded RELATIVE to G_h, not merely shown small before gain division;
- exact nonlinear finite-root recovery and physical mesh-uniform control beyond the conditional smooth limit.

These are not external observers or extra fields demanded by this theorem. They are equality/admission statements about objects already present in the model. The original no-external-catalog premise does not by itself prove the selected field map or price. A future source application may discharge them by actual native constructions; they must not be renamed zero.

## 9. Reproducibility

Executed in this turn: Python 3.13.5, SymPy 1.14.0, mpmath 100 digits. Both normal and optimized Python runs produced identical JSON. Tests raise exceptions explicitly.

Checks include a non-unimodular rational coframe (det=4), all six cofactor maps, the exact 16x16 density-map Jacobian and inverse, all sixteen independent matter-source variations, the original scalar normalization, the normalized complete material-bank norm witness, the unchanged full-CAR smooth residual and its derivative, and the complete nonlinear heat+feedback source with unequal weights. A fixed nonzero attenuation is deliberately verified NOT to equal the linear target, preventing an exact-finite-action overclaim.

The local test uses a four-cell unequal-weight source-moment control for the probability composition. It is not an execution of the huge original READY gate word, a full lattice root solve, an original all42 replay, Lean, or CI.

Executed code SHA256: `168209b98d64da98d16fa7515807fb56418fa99de314c6e74fcd6d67310b15ff`.
Observed result SHA256: `5a7604a57008c884956f17c2ac9ebf18db0adf240f7604f57c55c1105f30700e`.

The algebraic proof and uniform estimates, not extrapolation from test points, establish the mathematical statements at the scope stated above.
