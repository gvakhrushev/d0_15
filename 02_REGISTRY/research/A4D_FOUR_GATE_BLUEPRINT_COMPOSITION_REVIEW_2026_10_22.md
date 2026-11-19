# Four-gate synthesis: corrected composition and executable audit

Date: 2026-10-22. Repository: `gvakhrushev/d0_15`. Existing scientific owner: Draft PR #334, `exp/a4d-joint-response-continuation-2026-10-16`.

Status: research review of a proposed composition, NOT a physical closure theorem. No accepted source owner is changed. `GR_closed=false`.

## 1. What to preserve

The productive proposal is to retain an actual nonflat root of the complete source, rather than require that a new physical price have exactly the same function or old stationary point as the configured native 0/10 price. This is already the purpose of the original unpadded full42 robustness owner. Its hypotheses, however, concern the entire extra covector on a specified field ball, with the actual normalization and independent-input equations.

The proposed four-gate closure makes several further inferences that do not follow. Two involve false mathematical identities, not merely a missing large computation. The following replacements preserve the constructive route without introducing a fitted heat operator or a physical minimum by definition.

Source snapshot inspected: `07a328a29843d5f21e0d5b4fec1b5ec0be923e3b`.

## 2. Gate C: the Legendre lift is a stationary equivalence, not a hidden convex minimum

For an operand map q(Y) and a strictly convex cost c, let V=c* on the owned local response chart. Then

    S(Y) = c(q(Y)) = sup_a L(Y,a),
    L(Y,a) = a.q(Y) - V(a),
    L_aa = -V_aa < 0.

In the real original two-cell construction, the response block is

    L_aa = -kappa diag_s[rho_s D2 V_s],

with kappa>0 and rho_s>0. The correct reduced Hessian is

    H42 = L_YY - L_Ya (L_aa)^(-1) L_aY.

Writing Q=-L_aa>0 gives

    H42 = L_YY + L_Ya Q^(-1) L_aY.

The Schur correction is POSITIVE semidefinite. Replacing L_aa by +V_aa while keeping the outer minus reverses its sign. This is explicitly incompatible with equation (15) of the original constitutive owner.

There is a stronger exact conclusion. For the full block Hessian

    H46 = [[A,B],[B^T,D]],  D=L_aa<0,

congruence by [[I,0],[-D^(-1)B^T,I]] gives

    diag(A-B D^(-1)B^T, D) = diag(H42,D).

Hence, if the four response coordinates are independent,

    n_minus(H46) = n_minus(H42)+4,
    n_plus(H46)  = n_plus(H42),
    n_zero(H46)  = n_zero(H42).

The lift therefore cannot turn this saddle into an unconstrained minimum in 46 variables. It preserves the stationary equations and gives an invertible auxiliary block. It does NOT establish the physical minimum-description selector.

A minimal exact control: c(q)=q^2/2 is strictly convex, q(Y)=1+Y1^2-Y2^2. At Y=0, S has Hessian diag(2,-2). Its exact Legendre lift a q-a^2/2 at a=1 has Hessian diag(2,-2,-1).

A different constrained optimization interpretation remains possible only after its actual feasible set and allowed variations are derived. Calling all 42 original freely varied fields 'Lagrange multipliers' does not construct that feasible set. At an ambient critical point a price-preserving smooth writer w has pullback Hessian Dw^T H42 Dw; if Dw has full row rank 42, any negative ambient direction has a preimage. Thus an unconstrained minimum cannot be obtained merely by such a full-rank reparameterization.

## 3. Gate A: an exact work echo neither selects the Book projector nor erases a retained macro outcome

The original Q8 owner really proves the complete 15-operation inverse and conditional restoration of work coherence, with 30 non-idle calls. It explicitly retains the separate clock-mode switch/admission obligation and the archive-nondemolition restriction. The new statement must not discard these premises.

After a perfect inverse on its OWN work, an independently retained outcome tag gives

    |Psi> = sqrt(1-r)|0,blank,W0> + sqrt(r)|1,blank,W1>,
    <W0|W1> = 0.

Tracing out the retained archive gives diag(1-r,r) on the programme. Its programme-only X contrast is zero. The joint X_programme X_archive contrast can be nonzero, but that observable does not commute with the old outcome projections. This is exactly the distinction already proved in the paid-echo owner.

Keeping only the common site label is different from retaining both site and READY_AND_CLICK: the latter can preserve the orthogonal tag which prevents the advertised programme-only interference. A different permitted joint readout may be useful, but it needs an explicit complete operation and information/cost account.

There is also a cut/time distinction. If the full operation used in F=P U* (I-P) U P is the restored echo identity on the same active range, U P=P, then F=0. A nontrivial intermediate-stage cut may have nonzero feedback, but its value cannot be copied from the 15-step protocol to the completed echo without recomputation including clock and controller. The identity is not being asserted for the complete stage/control apparatus unless that apparatus has actually been restored.

A pure state has density rank one. Tensoring a moving rank-one programme range with a four-dimensional spin identity defines a rank-four PREPARATION RANGE, not a unique physically required active projector. Purity, minimal support and the compulsory Book active cut are different claims.

## 4. Gate B, heat: the proposed Gibbs/Fredholm cancellation is false

Grant the proposed substitution temporarily, without claiming that it is the real scene Hodge:

    M = I-zeta F > 0,
    Delta = -(1/beta) log M + mu I,

where beta and mu are field-independent. Then exactly

    exp(-beta Delta) = exp(-beta mu) M,
    H = -mu + (1/beta) log Tr M,
    J = -log det M.

Therefore

    d(H+J) = zeta Tr[(M^(-1) - I/(beta Tr M)) dF].

These are different linear functionals. For the two actual native flat bands A0=B0(1+p^6), B0=4p^3, p=(sqrt(5)-1)/2, take the operator-space variation

    F(t) = diag((A0+t) I_528, (B0-t) I_528).

Its trace is constant, so dH/dt=0 for EVERY beta. But

    dJ/dt = 528 zeta^2 (A0-B0) / ((1-zeta A0)(1-zeta B0)) > 0.

At zeta=2^-20 this is approximately 2.52700516181125e-11. This diagnostic disproves a purported operator identity. It is not an assertion that this particular direction has already been realized by the admitted 42-field writer, nor a direct recalculation of its psi1 component. Any accidental cancellation on a specified physical tangent would require that actual tangent to be computed.

A field-independent mu has no derivative and cannot repair the identity. Choosing mu(Y) to cancel it supplies exactly the additional source that needs independent justification.

### Correct constructive replacement: scale and spectral shape

Let d=dim M, t=Tr M and rho=M/t. Then

    H+J = d D(I_d/d || rho)
          + (1/beta-d) log(t/d)
          + (log d)/beta - mu.

This follows directly from D(I/d||rho)=-log d-(log det rho)/d. It separates trace scale from spectral anisotropy; it does not erase either. Along trace-preserving variations, the entire source is the derivative of the reverse relative entropy. For unequal bands it is generally nonzero.

This identity is conditional on the proposed logarithmic Delta. It is NOT a new definition of the actual Book03 scene operator. For the actual operator retain

    dH = -Tr(sigma_beta dDelta_actual),
    dJ = zeta Tr((I-zeta F_actual)^(-1) dF_actual),

with every cut, input, clock and valuation term on the same execution. Also establish whether measured-code Cost-Info is an additional component or an alternative representation before adding it to H+J: otherwise the same payment can be counted twice.

## 5. Gate B, root: use a whole-ball certificate, not a small scalar derivative

The actual unpadded robustness source gives

    ||A||_inf < 28.883,
    ||I-A H42(z0)||_inf < 0.036547.

The latter number is an INVERSE DEFECT, not ||H42^(-1)||. It implies the upper bound

    ||H42^(-1)||_inf < 28.883/(1-0.036547) < 29.979.

The known robustness cube has radius 1e-20 and requires the COMPLETE extra 42-source sup-norm <=1e-22. Continuity supplies existence; the separate Lipschitz bound <=0.01 supplies uniqueness. The original root enclosure of radius 1e-24 is not a certificate for displacements 1e-11 to 1e-7. Those displacements exceed its radius by 13 to 17 orders; comparison with the mesh parameter h0~0.1838 has no relevant implication.

One source component near 1e-11 does not bound the complete covector by that number. A scalar slope ratio from a different cut/execution is not a bound after the original 42-field pullback and normalization. Newton linearization is a predictor; its nonlinear remainder must be bounded.

No conclusion of nonexistence follows. A wider corrected-root certificate or a verified continuation may succeed. But success is not implied by the numbers currently supplied.

Exact no-root control: F0(x)=x has unit derivative and zero inverse defect. Add R(x)=epsilon-x+x^2, with epsilon>0 arbitrarily small. R(0)=epsilon, yet F0+R=x^2+epsilon has no real zero. The missing whole-neighborhood derivative control matters even with an excellent base inverse.

## 6. Gate D: conditional information is useful, but is not a logdet replacement or a uniform inverse

For fixed positive address probabilities pi_s summing to one, the measured code price satisfies

    S_cond = sum_s pi_s [1+r_s-h_phi(r_s)],
    S_mean = 1+rbar-h_phi(rbar),
    S_cond-S_mean = I_phi(site:bit),
    rbar=sum_s pi_s r_s.

This is a genuine information identity. If pi_s moves, its derivatives must also be retained. It does not replace J(rbar) by S_cond: a spectral logdet and a code-relative entropy remain different functions until a full source-preserving execution map is proved.

For example, equal weights and r0=1/4, r1=3/4 with dr0=-dr1 keep rbar fixed, hence any scalar J(rbar) has zero source. The conditional code source is -log(3)/log(phi), not zero. Retaining the address prevents loss, but does not automatically cancel an additional Book source at an old off-null root. The h0 unpadded and h=1/4 padded prices/collars must remain distinct.

Likewise a pointwise invertible 34-coordinate observation map is not a field-evolution inverse. For the stated coordinates, 42-34=(16-10)+2; assigning these eight directions to four translations, two material and two normalization phases is not established by counting. The actual map, gauge action and collars are needed. Fibre descent of a covector is not a spacetime Noether/Bianchi identity merely because both are called a vertical condition.

Finally, O(h^2) consistency and a smooth PF tower do not alone prove root recovery. The scalar family

    E_h(x)=h^3 x+h^2

has O(h^2) residual at x=0 and an invertible Jacobian at every h>0, but its unique exact root -1/h diverges. A gauge/boundary-compatible uniform inverse, or an equivalent nonlinear stability argument, is indispensable. This diagnostic is not a claim about the actual D0 inverse.

## 7. The corrected single construction to certify

Fix ONE admissible execution first. Let z be the existing 42 field coordinates and u all truly independent apparatus/preparation coordinates, after the actual gauge/boundary conditions. Define its complete real price once, without charging a component twice:

    S_actual(z,u),
    F(z,u)=(partial_z S_actual, partial_u S_actual).

Mathematical Legendre response variables and the one global thermal variational variable can be eliminated with their correct signs, where their regularity hypotheses hold. This does not eliminate physical u by name. If the genuine input equation has an established locally unique section u*(z), its reduced Hessian is

    H_eff = S_zz - S_zu (S_uu)^(-1) S_uz.

Otherwise certify the complete joint system; the 42-field inverse alone does not control it.

On a closed admissible ball B(c,r), take a nonsingular fixed preconditioner A and calculate rigorous bounds

    alpha >= ||A F(c)||,
    b >= sup_B ||I-A DF||,
    b < 1,
    alpha+b*r <= r.

Then T(x)=x-AF(x) maps B into itself and is a contraction; its unique fixed point solves the complete system, with distance <=alpha/(1-b). This is the correct finite root-persistence theorem. Domain, nonflatness, metric signature and preserved archive/clock conditions must hold throughout the accepted ball. For a merely continuous remainder use the already owned Brouwer theorem and do not claim uniqueness without its extra Lipschitz premise.

For a refinement family the norms and inverse/control constants must also be tracked as h changes. An exact finite root, a regular continuum equation-class identification and uniform finite recovery are separate conclusions.

## 8. Validation and exact scope

The accompanying `check_blueprint.py` executes 33 controls: exact symbolic Schur/congruence and archive calculations, native 528+528 scalar heat/logdet check, the corrected scale-shape identity, exact rational reproduction of the existing robustness arithmetic, conditional-information differentiation and a consistency-without-stability control. Ordinary Python and `python -O` give byte-identical JSON. These tests are intended to reject the incorrect compositions; a PASS is NOT a PASS for Gates A-D.

Not run or claimed: a new full42 residual computation, a new full42 interval root, a complete writer/echo/Book execution, a new Lean build, repository-wide CI or a physical GR closure. The prior local global-spectral packages are not newly uploaded or accepted by this review.

## Source owners inspected (unchanged)

All paths below are under `02_REGISTRY/research/` at the snapshot above.

- `A4D_UNPADDED_GOLDEN_N1_CONSTITUTIVE_LEGENDRE_COMPLETE_2026_10_22.md`, equations (11)-(15); blob `4f081ff7925b6fa2c3625ae78966929444aeff10`.
- `A4D_ORIGINAL_UNPADDED_0_10_FULL42_SOURCE_ROBUSTNESS_2026_10_22.md`; blob `5c3062a9ce151d754b81b7bad01ea69600d269f3`.
- `A4D_Q8_PAID_ECHO_ARCHIVE_QND_SELECTION_2026_10_22.md`, sections 1-4.
- `A4D_Q8_COHERENT_PROGRAM_NATIVE_BOOK42_SOURCE_FORK_2026_10_22.md`, sections 2-5.

No private correspondence is copied into the repository. The review records mathematical claims and their source boundaries only.
