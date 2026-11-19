# A precise completion criterion for the original HJR metric zero mode

20 October 2026. Read-only synthesis for the existing #334 integrator. No new native action, selector, restriction of the original carrier, or claim promotion is proposed. The statements below are exact mathematical consequences with explicitly conditional physical application.

## 1. Pinned inputs and what is actually being tested

Scientific source commit: `41582f57ce2b4bc8c9fad322e3c2d8ecaadb8b70`.
This is newer than local `ac14cbcae94b919b9709691c359628247ffdf0d4`.

Inputs in that commit:

- `02_REGISTRY/research/A4D_HJR_ZERO_MOMENTUM_EINSTEIN_CONSTITUTIVE_GAP_2026_10_20.md`, Sections 2–3: actual original L=8 full-CAR16, all4096-momenta, full128 moving-Riesz, true-global-Z homogeneous Hessian.
- `02_REGISTRY/research/A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md`, Sections 4–5: actual invariant coframe/link coordinates and unchanged second source.
- `02_REGISTRY/research/A4D_COMPLETE_BOOK_GOLDEN_SELF_CODE_STATIONARY_ENVELOPE_AND_ODD_GEOMETRY_2026_10_20.md`: full normalized conditional-record extension and its exactly neutral moving-KL envelope.
- `02_REGISTRY/research/A4D_BOOK_GOLDEN_PROJECTIVE_RADIAL_EINSTEIN_SCALE_WARD_DOUBLE_SCHUR_2026_10_20.md`, Sections 3–4: conditional zero-action normal form and history Schur.

Additional conditional bridge read at `origin/control/gr-golden-blowup-condensed-2026-10-20`: `02_REGISTRY/research/A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md`. Its metric descent/Golden scale hypotheses are not assumed proved for D0.

At the exact original HJR flat stationary root, write

    x=(S0,S2,S3), z=(S4,T0,T1,T2,T3),
    H0 = [[A,B],[B^T,C]], M=A-B C^{-1} B^T.

Here x consists of three independent genuine metric variations. S4 is the observer-relative Lorentz coframe direction and T0..T3 are the four actual invariant proper-link families. S1 remains another physical metric coordinate held fixed on this slice; it is not silently deleted or reclassified as an internal variable. The complete physical field equations are not reduced to this eight-dimensional slice.

The accepted interval input is `COLLAR_HESSIAN_ARB.json`, SHA-256
`a38386a86af4be283631d42a890caf66c035c12a4f9d421037160550d36989f4`.
The original exact-rational comparison proves

    C > 4 I5,                 M > m I3,       m=2489/1000.

The metric midpoint Schur is approximately

    [ 2.699090784804  -0.167047396148  -0.035983317627 ]
    [-0.167047396148   8.476793441348   2.722549046232 ]
    [-0.035983317627   2.722549046232   8.392836012235 ].

The companion checker independently reconsumes the pinned interval bytes and exact midpoint inverse. No new spectral replay or new source is substituted.

## 2. Flat-vacuum naturality already forces the entire homogeneous metric Jacobian to vanish

**Theorem A.** Let E[g] be a local-diffeomorphism-natural metric-only tensor on open Lorentz patches, defined and differentiable on an open set containing all constant Lorentz metrics. Suppose E[eta]=0 at one constant Lorentz metric eta. Then

    E[g_const]=0,
    D E_g_const[V_const]=0

for every constant Lorentz metric in the common chart and every constant symmetric metric tangent V.

**Proof.** Every constant Lorentz metric g is the pullback of eta by an invertible linear coordinate map L on suitable open patches. Naturality gives E[g]=L*E[eta]=0. Differentiate the identically zero function on the open cone of constant Lorentz metrics. This uses neither differential order, curvature classification, Golden scaling, nor an Einstein equation. The same argument applies to a tensor density. At a stationary point, conversion between Euler tensor and Euler density does not add a Hessian term because the first source vanishes.

Consequently the q=0 homogeneous metric Hessian of a metric-only local variational source with a flat vacuum must vanish. A geometric cosmological term b g does not evade this: flat vacuum implies b=0.

**Precise physical boundary.** This theorem applies to the reduced gravitational metric-only source. A full action with separately retained matter, observer, reference density, clock, torsion, archive, or other physical background can have a nonzero homogeneous restoring source. Covariance of (g,n,clock,...) under simultaneous transformations is not metric-only naturality. The total Einstein–matter equation need not obey this metric-only premise with matter fixed. Global flat torus moduli can enter a nonlocal functional, so finite periodic global dependence does not itself violate Theorem A.

The original positive M therefore obstructs exact source-preserving identification of this bare conditional HJR slice with a local metric-only flat-vacuum source, in precisely the finite source chart in which the comparison is made. It does not by itself obstruct continuum descent or a different full stationary branch.

## 3. Arbitrarily many new positive stationary penalties cannot remove the gap

Let u be any collection of additional internal archive/preparation/history variables on which the *bare HJR action is independent*. Its extended Hessian is

    Hbar0 = diag(H0,0_u).

Let E be the Hessian of an actual additional paid source at a common stationary point of the original and completed actions. Thus the additional first source must vanish there; if it does not, the original root is already not a stationary root of the completed theory.

Let H=Hbar0+E. Order variables as x followed by w=(z,u), and write

    H=[[P,Q],[Q^T,D]],     Mfull=P-Q D^{-1} Q^T.

The internal block D must be invertible on the actual admitted internal/gauge quotient. Where D>0, its elimination is a stable local stationary minimum.

**Theorem B, convex-completion rigidity.** If E is positive semidefinite and D>0, then

    Mfull >= M > m I3.

**Proof.** For fixed x the Schur variational formula gives

    x^T Mfull x = min_(z,u) [(x,z)^T H0 (x,z) + (x,z,u)^T E (x,z,u)]
                 >= min_z (x,z)^T H0 (x,z)
                 = x^T M x.

This covers any number of new internal variables and all their mixed blocks. It does not freeze their response. A positive semidefinite E and invertible D actually imply D>0 here, since its baseline is diag(C,0_u)>=(0).

A useful corollary: if an added smooth price is nonnegative near the common root and vanishes at that root, its Hessian is positive semidefinite; it cannot cancel the gap. Positivity of the *value* of a price that is nonzero at the root is insufficient to imply Hessian positivity. Negative Hessian directions are not negative costs or negative probabilities.

**Exact conditional-record application.** A complete moving conditional KL envelope has the local Hessian

    E_KL = [[L^T Q L, -L^T Q],[-Q L,Q]], Q>0,

in parent variables y and internal probability coordinates u, with u'(y)=L. It is positive semidefinite and its own exact stationary Schur is zero. After adjoining it to *any* action S0(y), minimizing u yields exactly S0(y), hence every reduced first and higher source is unchanged. In particular the original HJR M and its Golden first-source scale defect are unchanged.

Using only the negative cross-Schur term -L^T Q L while dropping the true direct field block +L^T Q L manufactures a cancellation that the complete normalized record does not have.

This statement applies to genuinely neutral conditional enrichment. It does not identify the actual full128 native price with that enrichment; the owner explicitly distinguishes actual observed and code-prior distributions.

## 4. Exact compensation requires at least three negative Hessian directions

Define the actual internal stationary lifting

    K=-D^{-1}Q^T,      Lx=(x,Kx).

Then the following are equivalent:

    Mfull=0
    H L=0.

The second equality exhibits three independent lifted zero modes with nonzero physical metric projection. It is the precise linearized compensation condition on this slice; satisfying a scalar cost normalization does not imply it.

**Theorem C, inertia requirement.** If D is invertible and Mfull=0, then the actual completion Hessian E has at least three strictly negative eigenvalues. More precisely,

    (Lx)^T E (Lx)
      = -(Lx)^T Hbar0 (Lx)
      = -x^T M x - (z_*(x)+C^{-1}B^T x)^T C
                         (z_*(x)+C^{-1}B^T x)
      < -m ||x||^2,                    x != 0.

**Proof.** The completed quadratic form vanishes on its stationary lift because its Schur is zero. Completing the square in the original H0 gives the displayed identity. L is injective because its x block is the identity. Thus the restriction of E to a three-dimensional subspace is negative definite. The inertia law/min-max principle gives at least three negative directions. This proof only needs D invertible; it does not claim saddle elimination is a stable physical preparation.

For an approximate target with ||Mfull||_2<=delta<m, the same proof gives

    (Lx)^T E(Lx) <= -(m-delta)||x||^2.

In the declared Euclidean coordinate norm, at least three eigenvalues of E are <=

    -(m-delta)/(1+||K||_2^2).

The number of negative directions is coordinate invariant at a common stationary root; this numerical eigenvalue bound depends on the declared coordinate norm. The theorem does not demand three new fields: mixed couplings to existing/new variables can produce the required negative curvature. It does demand a real source mechanism, rather than an omitted direct Hessian or a fitted subtraction.

If all metric variations were physically constrained away, or the root moves after adding actual first sources, or singular internal constraints change the quotient, a different problem must be proved. Those possibilities are not silently excluded.

## 5. An exact source interface where such curvature can arise honestly

For a genuinely selected additional finite history ensemble with actual net prices c_a(y) and beta=ln(phi), define

    F(y)=-(1/beta) ln sum_a exp(-beta c_a(y)),
    p_a=exp(-beta c_a)/sum_b exp(-beta c_b).

Direct differentiation gives

    D F = mean_p(D c),
    D^2 F = mean_p(D^2 c) - beta Cov_p(D c).

This is an exact source identity. The covariance term supplies negative curvature without negative probabilities or negative price values. For locally affine prices the Hessian is precisely -beta Cov(scores). A pure covariance cancellation of three independent positive metric directions requires score covariance of rank at least three, hence at least four score classes, but rank alone does not set its magnitude or physical identity.

At a common stationary root, the actual first score must also satisfy mean_p(D c)=0 (or the explicitly required full-source balance). If F is the actual already-reduced additive completion of HJR, the required metric equation is

    beta Cov_p(D c) = M + mean_p(D^2 c)

on this slice. For histories coupled before original internal elimination, this equation must instead be imposed through the full blocks P,Q,D above, including all cross derivatives. Schur reduction cannot be distributed over a sum of actions.

This is a concrete candidate *test* for an actual Book history price, not construction of the native action by choosing a covariance to match M. One must avoid counting again the thermal covariance already present in the original HJR source.

The conditional zero-action normal form B(z)+W(x,z)A(x)+A(x)^2 R(x,z), with A=DA=0 and DB=0, has the correct metric Hessian W D^2 A. If it is claimed to be a completion of the specific bare HJR source at the same flat root, its actual difference from HJR must meet Theorem C. Calling the missing part a positive neutral history cost does not establish that normal form.

## 6. Finite gap, Golden scaling, and continuum normalization are different claims

The strict bound m applies to the original L=8 K9(0) source convention. Multiplying this fixed action by any nonzero scalar or using an invertible physical metric coordinate map cannot turn a nonzero Hessian into zero.

For an actual refinement sequence, let a_h be the prescribed action/source normalization and let x=J_h v identify physical metric tangents with lattice variables. At a stationary point the physical homogeneous Hessian is

    Mphysical_h = a_h J_h^T M_h J_h.

A persistent normalized obstruction follows only from actual bounds such as a_h>0 and

    liminf_h a_h m_h sigma_min(J_h)^2 > 0,

together with convergence of the relevant reduced sources/derivatives. A single L=8 gap gives none of these by itself. If the prescribed normalization makes this expression vanish, its finite gap may disappear. Uniform flat differentiability is independently needed to exchange refinement with the flat metric differential.

Likewise the archive Golden level factor and the transformation g->phi^2 g are different inputs. Exact stationary elimination transports a genuine same-action symmetry only when its internal solution branch and metric interpretation transform equivariantly. A source-neutral moving-KL envelope cannot repair a scale defect already present in the action because its reduced value is identically zero.

## 7. Reproducible checks and conclusion

Run:

    python3 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/check_schur_completion.py

The checker uses the pinned original interval bytes, exact Fraction arithmetic for the gap, and exact symbolic rational matrices for the completion controls. It verifies:

- original C>4 and M>2489/1000;
- exact neutrality of a moving internal quadratic/KL Hessian;
- a positive extra penalty increases the reduced metric block;
- deleting its true direct field block creates a false negative Schur;
- a sharp genuine completion has exactly three negative directions and zero completed Schur;
- a rank-two covariance cannot cancel a positive three-dimensional M.

The strongest new deduction is not a further GR uniqueness theorem. It identifies a necessary mechanism: at the common original HJR flat root, a full source achieving local metric-only flat-vacuum descent must generate three actual lifted Ward zero modes and an indefinite completion with at least three negative curvature directions. Neutral record enrichment and convex zero-baseline costs cannot do this. The actual Book valuation and its same-execution coupling are the place where the missing compensation must be derived or disproved.

Status: exact mathematical theorem plus pinned fixed-L8 input consequence; full native action selection, continuum metric descent, and physical GR closure remain open.
