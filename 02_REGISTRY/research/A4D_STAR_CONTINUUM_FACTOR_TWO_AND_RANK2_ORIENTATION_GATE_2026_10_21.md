# D0 → GR: literal six-plaquette normalization gate and the two-field rank-two finite-source test

21 October 2026. Existing Draft PR #334, \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, constitutive/native-programme-v1. Consume the original six-plaquette \`S_star\` (\`a4d_star_density_variation_pressure_check.py\`), the original all40 Brinkmann proof, the actually weighted two-density N=1 CQ source, and the published two-real-scalar non-VSI continuum/finite-matter examples. **New:** an explicit checked finite-to-continuum **normalization/type gate** and an alternative pre-existing detector-orientation **constructive first-source limit** on the same two-field geometry. No new action, Hilbert carrier, scalar, numerical coupling, field writer or GR promotion. **GR_closed=false.**

## 1. The missing bridge was a SIGN AND FACTOR OF TWO, not another rank

The positive-orientation Cartesian comparison lives in \(\eta=\mathrm{diag}(1,-1,-1,-1)\), with 16 independent coframe entries \(e^a{}_\mu\) and six original proper-Lorentz generators \(F_{\mu\nu}\in\mathfrak{so}(1,3)\). Fix precisely the ORIGINAL \`G2\`, \`STAR_MAP\`, complementary coframe wedge, face sign \(\epsilon_{\mu\nu\rho\sigma}\), and \(b(F)=F\eta\) used in the accepted \`a4d_star_density_variation_pressure_check.py\`. No geometric star is inserted into an alternative detector. Define for each based infinitesimal face \(\mu<\nu\)

\[
\mathcal L_{\star,\mu\nu}(e,F)=
\epsilon_{\mu\nu\rho\sigma}
 G_2(e_\rho\wedge e_\sigma,\star\, b(F_{\mu\nu})).
\]

For comparison, use the STANDARD torsion-free Riemann/Palatini convention explicitly stated in the continuum \`A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE\` (its equation (2)), with

\[
R^\lambda{}_{\alpha\mu\nu}
=(e^{-1})^\lambda{}_a (F_{\mu\nu})^a{}_b e^b{}_\alpha,
\quad
R_{\alpha\nu}=R^\mu{}_{\alpha\mu\nu},
\quad
R=g^{\alpha\nu}R_{\alpha\nu}.
\]

Here \(F_{\mu\nu}\) can be ANY independent Lorentz-curvature entry, not only a Levi-Civita curvature. For a single face, antisymmetry of \(F\eta\) gives the exact scalar density

\[
eR_{\mu\nu}
=2\det(e)\, (e^{-1})^\mu{}_a(F_{\mu\nu}\eta)^{ab}(e^{-1})^\nu{}_b
\qquad(\det e>0).
\]

The complementary wedge/Hodge contraction equals its negative half, so

\[
\boxed{
\mathcal L_{\star,\mu\nu}(e,F)
=-\tfrac12\,eR_{\mu\nu}(e,F)
\qquad\text{in the specified oriented Cartesian }(+---)\text{ chart}.
}\tag{1}
\]

This is a basis-independent algebraic epsilon/wedge identity on the stated orientation component. It is **NOT** an equality with \(eR_{\mathrm{standard}}\) having unit coefficient, unless the target owner has explicitly redefined its scalar or its face orientation. For example at \(e=I\), \(F_{01}=K_{01}\), the literal original star contribution is \(+1\), while the standard scalar-density contribution is \(-2\). The same ratio holds on all six matched face/generator slots.

The new checker verifies (1) in **108 exact rational cases**: every one of six face roles against all six independent Lorentz generators, on three nontrivial positive-oriented coframes. With smooth links \(U_\mu=\exp(h\omega_\mu)\), the finite plaquette has \((P-P^{-1})/2=h^2F_{\mu\nu}+O(h^3)\) on a common smooth collar, and the original \(h^{-4}\mathcal P_{\star,h}\) has continuum leading density \(-eR_{\mathrm{standard}}/2\), not \(eR_{\mathrm{standard}}\). The finite remainder needs its own derivative norm and does not vanish identically.

**Consequent architecture gate:** the true literal finite geometry input \(x_{\star}=\eta_{\rm query}^2 h^{-4}\mathcal P_{\star,h}\) and the continuum-paper input \(x_{\mathrm{cont}}=\eta_{\rm query}^2eR_{\mathrm{standard}}\) satisfy \(x_{\mathrm{cont}}\sim -2 x_\star\) at leading order on this typed chart. They cannot be substituted as equal arguments of the same fixed nonlinear detector without transporting the first-source Jacobian. This is a *normalization defect in the claimed identification*, not license to fit a new Einstein coefficient. In the original null-frame positive family, frame orientation, null epsilon and normalizer have their OWN declared conventions; the present Cartesian comparison must be transported into those conventions before making a global contradiction claim.

## 2. A decisive actual finite coframe-source control on the rank-two non-VSI solution

Consume the already published two-real-field seed from
\`sources/d0_covariant_multiscalar_price_2026-10-21/CROSSING_STREAMS.md\` and the previous exact finite matter lift from
\`sources/d0_weighted_two_field_rank2_2026-10-21/check_weighted_two_field_rank2.py\`.
Let \(\kappa=-\lambda_-(2^{-20})=23.416406751884\ldots>0\).
With \(c=1\), around \(r=1\) use the same standard oriented diagonal coframe

\[
e^a{}_\mu=\operatorname{diag}
\bigl(\sqrt r\,e^{-r^2/4},\;
e^{r^2/4}/\sqrt r,\;r,\;r\bigr),
\quad
\frac{dt}{dr}=e^{r^2/2},
\quad
\psi_1=\varepsilon(r^2-1)/2,\;\psi_2=\varepsilon x.
\tag{2}
\]

The actual **finite CAR-forward matter gradients**, NOT direct samples of first scalar amplitudes, are

\[
D_t^+\psi_1=\varepsilon r e^{-r^2/2},\qquad
D_x^+\psi_2=\varepsilon.
\]

Every site has \(q_h=0\) EXACTLY. Moreover \(g^{tt}D_t^+\psi_1=\varepsilon\) and \(g^{xx}D_x^+\psi_2=-\varepsilon r e^{-r^2/2}\), so the corresponding backward-time and backward-x matter Euler rows vanish exactly on the interior homogeneous stencil. The other gradients are zero.

For the geometry retain ALL six actual based finite plaquettes and independent link variables. The trial continuum Levi-Civita links, NOT pre-solved finite link Euler roots, are \(U_t=I\) and \(U_i=\exp(h\kappa_iK_i)\), with

\[
\kappa_x=(1-r^{-2})/2,\qquad
\kappa_y=\kappa_z=e^{-r^2/4}/\sqrt r.
\tag{3}
\]

Both neighboring time faces and all spatial commutator faces are included. At a spatially homogeneous local interior stencil the 16 coframe and 24 left-link source components are each identical at all translated spatial sites, so differentiation of the homogeneous sum gives each original local row up to its common site multiplicity. The checker differentiates all 40 independently via complex-step variation, not just the diagonal or the trial boost generators.

### 2.1. The previously used \(\sigma=-1\) ratio does NOT select this source

With the old material orientation \(\lambda_-=-\kappa\), and the old continuum/dust calibration \(\varepsilon^2=1/\kappa\) at \(c=1\), the literal original affine first source is \(D(f_\star+\lambda_-q_h)\).
Because (1) holds with the stated Riemann convention, and the known seed satisfies
\(G_{\mu\nu}=(\kappa/e)K_{\mu\nu}\),
its covariant metric source does NOT vanish. At \(r=1\) the two diagonal coframe-source limits are EXACTLY

\[
\boxed{
\lim_{h\to0} E_{e^0_t}=3e^{-1/4}\ne0,\qquad
\lim_{h\to0} E_{e^1_x}=-3e^{-3/4}\ne0.
}\tag{4}
\]

All fixed amplitudes used here are determined by the old \(\kappa\); the factor 3 is an actual relative-source mismatch, not a numerical fit. The checker confirms the limits monotonically on \(h=1/8,1/16,\dots,1/128\), including nonzero off-diagonal and link variations. Consequently **the published positive rank-two continuum \(\sigma=-1\) representative plus its exact matter lift is NOT by itself a same-source zero of the original Cartesian finite \(\mathcal P_\star+\lambda_-q\) geometry**. A continuum dictionary with \(eR\) cannot be identified with this source without the missing map (1).

### 2.2. The ORIGINAL alternate orientation \(\sigma=+1\) supplies a constructive compatible limit

The same original Golden two-band detector already contains \(\lambda_+=+\kappa\); no new price or coefficient is invented. In the Cartesian convention of (1), the affine source
\(f_\star+\lambda_+ q=-eR_{\mathrm{standard}}/2+\kappa q\)
has on-shell Einstein relation

\[
G_{\mu\nu}=\frac{2\kappa}{e}
\sum_A\partial_\mu\psi_A\partial_\nu\psi_A
\qquad(q=0).
\tag{5}
\]

Thus the SAME rank-two metric seed is a continuum candidate with the **derived** volume calibration \(e\mu=2\kappa\), i.e. \(\varepsilon^2=1/(2\kappa)\) at \(c=1\), not the \(\sigma=-1\) calibration \(e\mu=\kappa\). Its two finite scalar Euler rows remain exactly zero.

On the original noncommutative six-face finite star density and full set of 16+24 first-source directions, the independent local numerical test gives:

| mesh \(h\) | \(\max |E_{\rm coframe}|\), \(\sigma=+1\) | \(h\max|E_{\rm link}|\), physical spin-coordinate source | \(\max|E_{\rm coframe}|\), old \(\sigma=-1\) |
|---:|---:|---:|---:|
| 1/8 | 0.0680862840 | 0.038117598 | 2.338856918 |
| 1/16 | 0.0348811564 | 0.018980275 | 2.337017057 |
| 1/32 | 0.0176671783 | 0.009480316 | 2.336556092 |
| 1/64 | 0.0088925985 | 0.004738930 | 2.336440789 |
| 1/128 | 0.0044613619 | 0.002369312 | 2.336411959 |

The factor \(h\) in the link source is REQUIRED: the physical spin variable is \(\omega\) and the corresponding variation is \(\delta U=h\,\delta\omega\,U+O(h^2)\); holding the bare link tangent size fixed as \(h\to0\) describes a different variation. At \(\sigma=+1\) both measured source norms decrease roughly linearly with mesh size. The old \(\sigma=-1\) coframe source instead approaches the nonzero (4).

**Strong precise conclusion:** an EXISTING Golden orientation plus a CANONICALLY determined volume factor give a **consistent non-VSI, rank-two, two-material-field finite SOURCE sequence**, on this local interior stencil, with exact matter rows and numerically vanishing geometrical first-source residual. This does NOT prove an EXACT finite stationary root, a uniform analytic \(O(h)\) bound, a field-writer/clock preparation, a native selection of \(\sigma=+1\), or the full nonlinear N=1 CQ Euler equations at nonzero finite \(f_h=O(h^2)\). Their true weight/source corrections must be retained. A numerical sequence is not a replacement for all42 exact finite equations.

## 3. What this changes in the ONE parent architecture

There are now two independent limits and they must be compared on the SAME source:

1. **Original finite based star** -> standard continuum Palatini scalar with the EXACT sign/factor (1); this is a geometric conversion, not an arbitrary freedom to rescale \(\kappa\).
2. **Original Golden detector** -> scalar/top first-source ratio \(\lambda_\sigma=\sigma\kappa\); the sign is a physically typed orientation and its actual selection/price must be shown by the SAME execution.

The null-family exact all40 result remains independently valid on its native null-oriented chart. The positive Cartesian rank-two sector has a new scoped orientation gate and a constructive vanishing-residual test, NOT a promotion of all solutions to the same physical general GR law. One cannot silently transfer \(\sigma=-1\), the null-frame face orientation, or an \(eR\)-normalization to this sector merely because both have the same \(\kappa\) decimal.

**Next decisive scientific test:** derive the canonical proper-Lorentz **null-to-Cartesian orientation and normalization bridge** for the ORIGINAL star/detector on one shared oriented coframe; compute its actual detector \(\sigma\) and full first-source Jacobian. Separately, use the actual 40-row finite Euler map and its gauge-fixed linear inverse to test whether the \(O(h)\) rank-two source residual has a true compatible finite correction with fixed collar (and ALL off-diagonal/link rows). Do not add a fitted \(-2\) or re-solve matter by changing its fixed history.

## 4. Reproducibility, source boundaries and acceptance

\`sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py\` checks the literal accepted \(G_2/\star\) 108 rational identities and a separate complete 16+24 complex-step first-source replay of the rank-two interior stencil. It keeps both original Golden \(\sigma\) choices, the finite \(\kappa\) and exact-matter-current construction. Numerical tolerances are not formal continuum convergence proofs. The native all42 configured action and historical Lean owners are CONSUMED, not re-proved or reclassified. Physical G0/Book03 selection, complete actual clock and moving-query/field writer remain open. **GR_closed=false.**

Pinned conceptual owners at PR #334 input snapshot:
- \`02_REGISTRY/research/certificates/a4d_star_density_variation_pressure_check.py\`
- \`02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md\`
- \`02_REGISTRY/research/A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE_2026_10_21.md\` (its eqs (2)–(7))
- \`02_REGISTRY/research/sources/d0_covariant_multiscalar_price_2026-10-21/CROSSING_STREAMS.md\`
- \`02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/check_weighted_two_field_rank2.py\`
- \`02_REGISTRY/research/sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/WEIGHTED_WARD_AND_DUST.md\`


## 5. OWNER SIGN-SEAM RESOLVED EXACTLY: do not misread sigma-plus as a newly selected physical detector

The dedicated [original-owner all-order sign retyping theorem](A4D_ORIGINAL_STAR_NULL_CART_SIGN_AND_ALL_ORDER_CQ_RETYPE_2026_10_21.md) pin-checks BOTH actual original six-face implementations. The canonical flat G2*STAR matrix equals MINUS the internal six-by-six Levi-Civita pairing; the exact Brinkmann checker literally uses PLUS that same Levi-Civita pairing. Their full finite based-plaquette actions are NEGATIVES for the same transported oriented fields. The correct null-to-Cartesian internal change has determinant +1, so an ordinary proper frame change does not flip that sign. This is a cross-owner **normalization/convention discrepancy**, now explicitly resolved by a sign-typed map rather than altering either historical theorem.

In particular the originally used null affine source D(f_null+lambda_minus*q) equals -D(f_canonical+kappa*q), with kappa=-lambda_minus. This exact ALL42 first-Euler equality explains the sigma-plus affine Cartesian candidate of Section 2.2 **without proving a physical choice of a different Golden detector**. The earlier statement "alternate original sigma-plus supplies a compatible limit" is therefore to be READ AS AN AFFINE SAME-SOURCE COORDINATE PROXY ONLY; it does not authorize substituting the separately built sigma-plus full nonlinear price or a new absolute Book cost.

More strongly, for the SAME nonlinear actual sigma-minus CQ price F_null(x,y), its true canonical-coordinate presentation is F_cart(x,y)=F_null(-x,y). The master stationary equations conjugate under (s,P,a)->(-s,-P,-a), so K_cart(t)=K_null(t) as ENTIRE ANALYTIC FUNCTIONS; every higher matter coefficient, coframe scale P/a and true inverse-PF factor survive. The separate original sigma-plus detector yields F_plus(x,y)=F_null(x,-y), generally a different nonlinear function (original F_xx(0) is nonzero). The two affine gradients may have proportional stationary sources, but their all-order physical prices cannot be equated.

The independently observed five-mesh O(h) geometric source of Section 2.2 is thus the correct same-stationarity affine target after the original-owner sign transport, NOT a new all42 finite root. If the whole actual N=1 ledger is evaluated in the properly retyped variable, with f=O(h^2), q=0 and uniformly bounded native chart/field jets, its nonlinear-vs-affine source difference is O(h^2) per normalized site. The true full nonlinear matter rows need NOT stay identically zero once F_y varies; actual preparation/clock/work/upstream sources remain open. No full-grid inverse, physical sigma choice, nonlinear global minimum or GR closure is being claimed.
