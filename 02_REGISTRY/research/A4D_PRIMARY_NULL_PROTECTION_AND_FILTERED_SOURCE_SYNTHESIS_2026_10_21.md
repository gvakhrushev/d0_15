# D0 primary nonvacuum family: protected curvature sources and filtered residual recovery

21 October 2026. Existing owner **PR #334**, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive/native-programme-v1. Input snapshot `c49ebdb12244943d1ec45ef6d148a0432481141e`. Supporting source-composition result, not a new task, action, physical selection, or GR promotion.

## 0. The useful synthesis, and what is NOT new

The pp-wave reduction of general metric curvature tensors is a KNOWN theorem, not a new D0 discovery. We consume Gürses–Şişman–Tekin, [arXiv:1407.5301](https://arxiv.org/abs/1407.5301), section II, especially equations (24)–(43) and the pure-radiation discussion on page 6; see also Kuchynka–Málek–Pravda–Pravdová, [arXiv:1810.02178](https://arxiv.org/abs/1810.02178), the TNS class. The cited reduction is for a particular local metric-only curvature-source class; it does NOT classify the actual Book03/controller/clock action.

The new parent-level application combines that result with THREE existing D0 owners:

1. [The primary exact nonvacuum family](D0_GR_PRIMARY_POSITIVE_CASE.md) and its same-metric midpoint representatives.
2. [The complete terminal-source gain and remaining price](sources/d0_primary_normal_source_recovery_2026-10-21/README.md). Its common gain multiplies geometry and matter together; it is not free.
3. [The normal-source recovery theorem](A4D_PRIMARY_NORMAL_SOURCE_RECOVERY_SYNTHESIS_2026_10_21.md), including the actual signal denominator and the all-other-row compatibility condition.

**Conclusion within the stated hypotheses:** not every unknown higher-curvature coefficient has to be small. An entire class of reduced geometric source corrections annihilates the primary family EXACTLY. For a further explicit positive-resolvent class, even the correction-to-source inverse retains the original mesh-uniform 1/8 bound. Only the actual unprotected source remainder needs the prior quantitative control.

This changes the intended parent test from “bound every microscopic correction” to “prove the actual source's descent/type; separate the protected part; compute the unprotected source.” The actual descent is NOT provided by this application.

## 1. The original nonvacuum field has a stronger property than VSI

Use the unchanged signature and metric

`g = 2 du dv + H(u,x,y) du^2 - dx^2 - dy^2`,

`H = -lambda_* j(u)(x^2+y^2) + W(u,x,y)`,

`j(u)=|Psi'(u)|^2`, `Delta_perp W=0`.

Here lambda_* is the existing finite Golden-J2 ratio, not a fitted parameter. In the exact finite primary family W has arbitrary u-dependent quadratic and cubic harmonic coefficients. Work locally on the same unwrapped null interval; no whole-periodic-spacetime claim.

With the standard convention used in the companion calculation,

`l = du`, `nabla l = 0`, `Ric_ab = (Delta_perp H/2) l_a l_b`, `R = 0`.

For every v-independent scalar f,

`Box_g f = -Delta_perp f`,

and therefore, because l is parallel,

`Box_g (f l_a l_b) = -(Delta_perp f) l_a l_b`.

On the primary sourced family this gives the exact nonlinear identities

`Ric_ab = -2 lambda_* j(u) l_a l_b = -lambda_* T_ab`,

`Box_g Ric_ab = 0`, hence `Box_g^k Ric_ab = 0` for EVERY k>=1.

This holds for arbitrary smooth u dependence, not only constant matter density or weak waves. The Weyl part supplied by W can be nonzero. The original two-component null scalar still satisfies Box_g Psi=0 and its stress is covariantly conserved.

**Why scalar invariant cancellation alone is insufficient:** every pp-wave here has R=Ric_ab Ric^ab=0, but for H=x^4 one has `Ric_uu=6x^2` and `Box Ric_uu=-12`. A curvature-squared Euler source can consequently be nonzero even when its action density evaluates to zero on the ansatz. We evaluate the FULL Euler tensor first, not the identically restricted scalar action. The extra property protecting the primary family is Box Ric=0.

## 2. Which complete geometric sources are protected

Assume a candidate's genuinely reduced GRAVITATIONAL source is already a metric-only local symmetric tensor, formed by a finite sum of polynomial contractions of the metric, Riemann curvature and a finite number of its covariant derivatives, with fixed couplings. Use the parity-even contraction class of the cited theorem. There is no independent observer, torsion, clock, grid, archive field or material field left in this gravitational tensor. A scalar regular function of vanishing curvature invariants only supplies its values/derivatives at zero; singular quotients and inverse Box are excluded. Convergent regular form factors require their own domain/convergence justification.

The known pp-wave theorem then gives, on the entire Brinkmann class,

`E_ab[g] = Lambda g_ab + sum_(k=0)^K b_k Box_g^k Ric_ab`,

with constants b_k. In brief, each curvature factor contains two uncontractible parallel null covectors. A rank-two contraction of two or more such factors vanishes. Commuting covariant derivatives introduces another curvature factor, also zero in such a contraction. The surviving linear curvature terms reduce by Bianchi identities to powers of Box acting on Ricci. This explains the theorem's applicability; the finite checker does not claim to prove its arbitrary-order classification.

On the PRIMARY D0 family, the reduction is stronger:

`E_ab[g_primary] = Lambda g_ab + b_0 Ric_ab`.

All b_k with k>=1 disappear exactly, whatever their finite magnitude. If the same physical theory admits the specified flat vacuum with no compensating vacuum stress, Lambda=0. If its matter source is the original null T with coefficient d_0, the full reduced metric equation

`E_ab + d_0 T_ab = 0`

becomes

`(d_0 - b_0 lambda_*) T_ab = 0`.

Thus the primary family survives when the **derived** ratio d_0/b_0 equals lambda_* and b_0 is nonzero. The existing common terminal gain preserves that ratio; an unrelated renormalization of geometry alone would NOT. The separately reconstructed complete two-density price has an exact finite-z ratio result, but its density/measure/internal-source hypotheses must still be applied to the SAME physical programme. Numerical agreement of ratios is not that application.

### Exact scope of the compatibility improvement

This supplies the reduced metric normal-row support for the protected local curvature sector AFTER a legitimate connection/internal elimination and source/metric transport. It does NOT prove the independent 24 link equations, material equations, preparation/clock equations, or the native all42 source support. Their solution is a premise of that descent. In particular a frame-covariant source that still depends on a real observer is not a metric-only source.

A nonminimal material coupling F(Psi)R is outside the stated gravitational class and contributes `(g_ab Box - nabla_a nabla_b) F(Psi)`; for Psi=Psi(u) its uu term is `-d_u^2 F`, generally nonzero. Native matter/observer sources cannot be hidden among the protected b_k.

## 3. Exact same-mesh counterpart, with the boundary type retained

The original primary five-point transverse stencil satisfies on its quadratic/cubic family, for every mesh h,

`Delta_h H_h = -4 lambda_* j_h(u)`.

The actual finite CAR midpoint history gives this j_h. Since it is constant in transverse position,

`L_h Ric_h = 0`, `L_h=-Delta_h`, `Ric_h=Delta_h H_h/2`,

and every higher power also vanishes. Hence ANY finite polynomial reduced source

`b_0 Ric_h + sum_(k>=1) b_k(h) L_h^k Ric_h + d_0 T_h`

has the same primary zero when d_0/b_0=lambda_*. The coefficients may depend on the mesh and need not be perturbatively small. This is an exact consequence of the SAME stencil IF the actual microscopic source has this form. We do not assert that covariance of a continuum action forces every finite native discretization to have it.

**Collars are essential.** These differences use the original polynomial/null source continued through every stencil site. Powers require their complete wider collars. Applying a homogeneous Dirichlet matrix directly to a transverse CONSTANT Ricci array produces a boundary artifact, not this protected source. Conversely the existing zero-boundary Green operator acts on the CORRECTION v, not on the unshifted primary Ricci profile. The two boundary problems must not be conflated.

A quartic harmonic `W4=x^4-6x^2y^2+y^4` has `Delta_h W4=4h^2`, not zero. It is deliberately rejected as an exact same-mesh primary witness, even though its continuum Laplacian is zero. The existing higher-order midpoint/analytic recovery owner is the appropriate consumer for that extension.

## 4. Large compatible corrections need not spoil the previous recovery bound

This is a second, explicit conditional application, not an assertion that all higher-curvature theories are stable.

Let all other genuine equations be solved, and suppose the actual normal correction equation after subtraction of the primary representative is

`(g_h a_J,h/(2h)) A_h(L_D) L_D v + r_h(H0+v) = 0`,

where L_D is the original positive transverse five-point Dirichlet operator, `g_h != 0` is the actual complete-source gain, and the physical higher-derivative boundary realization is compatible with the stipulated primary collars and zero-boundary correction. These additional boundary data must be supplied by the actual programme, not chosen to obtain the result.

Assume, for example,

`A_h(L_D) = product_(j=1)^m (I + ell_j(h)^2 L_D)`, with every ell_j^2>=0.

There is no smallness condition on m or on the nonnegative scales. Each inverse `(I+ell_j^2 L_D)^-1` is positive and has infinity norm at most1 by the discrete maximum principle. Hence

`B_h=A_h(L_D)^-1 >=0`, `||B_h||_(infinity->infinity)<=1`,

`||L_D^-1 B_h||_(infinity->infinity)<=1/8`.

The same estimate holds for a supplied inverse filter `B_h=int_0^infty exp(-t L_D) dmu_h(t)` with positive measure of total mass at most1. This is a condition on an actual filter, not a claim that a native Perron/Book feedback automatically has this representation. The heat semigroup here is a mathematical source filter, NOT a free physical preparation.

Set `rho_h=2h r_h/(g_h a_J,h)`. The corrected fixed-point map is

`v=-L_D^-1 B_h rho_h(H0+v)`.

The existing continuous-source/Brouwer argument now applies with EXACTLY the old constant:

`||v||_infinity <= (1/8) sup||rho_h||_infinity`

`               <= h sup||r_h||_infinity /(4 |a_J,h| g_min,h)`.

The norm, actual query-size gain and admitted closed-ball hypotheses are unchanged. Only the UNPROTECTED remainder appears in this bound; the protected coefficients need not be bounded as small errors. No C2 entropy assumption is added. The theorem establishes stationary corrections, not minima, real-time stability, ghost-freedom or quantum unitarity.

A sharp negative control is `A=I-L_D/64` on the h=1/4 three-by-three interior grid: it is singular. Arbitrary signed higher-derivative coefficients do not inherit this inverse bound. Similarly a singular inverse-Box memory at its zero mode is not protected by the regular-polynomial argument.

## 5. Unified source decomposition and the actual next physical test

The three D0 source classes can now be distinguished without inventing a counterterm:

1. **Derived common gain:** the known complete terminal component multiplies geometry and matter by the same g_h. It changes source normalization, not their original ratio.
2. **Protected geometric contribution:** a proved local metric-only curvature source reduces to b_0 Ric plus derivative terms annihilated on the primary family. If its correction inverse is positive-resolvent, the existing residual bound survives even for large coefficients.
3. **Unprotected full source:** actual observer/grid dependence, independent connection or matter response, nonlocal/singular memory, clock/preparation/work/absolute-Book terms and lattice/source-transport defects. These must be calculated and tested; they are not erased by this classification.

The new application therefore changes ONE parent premise: the prior instruction to establish support/size of an undifferentiated unknown residue can first remove any contribution actually proved to belong to class2. The remaining row compatibility and source estimate apply to class3, with class1's REAL gain denominator. This can be much less restrictive than forcing the complete microscopic action to equal Einstein-Hilbert or demanding every microscopic correction be small.

It is not a claim that the native source satisfies the hypotheses. Native metric descent, actual 24-link/internal stationarity, the material coefficient, boundary transport and compulsory Price/Info/task selection remain open. The known source-preserving field-minimum exclusion remains fully in force.

**This family does not identify the theory globally.** Its protection means that many inequivalent higher-curvature theories share it. The already-owned Golden-step rigidity/Lovelock routes remain separate ways to obtain an all-metric Einstein equation class once their actual action/source hypotheses are established. We neither re-prove those routes nor use this family as evidence that all non-Einstein corrections vanish on arbitrary spacetime.

## 6. Reproduction, provenance and claims

The new bounded checker is in the EXISTING recovery packet:

`python3 02_REGISTRY/research/sources/d0_primary_normal_source_recovery_2026-10-21/check_null_source_protection.py`

It computes generic Brinkmann Ricci from the metric/connection, verifies the parallel null covector and Box reduction, substitutes the original arbitrary-coefficient sourced family, preserves the null material wave equation, checks the actual five-point stencil and finite-boundary negative control, and proves one exact rational large-filter contraction. Numerical positive resolvent/heat checks use49,225,961 interior sites. The saved `NULL_PROTECTION_RESULT.json` is the actual local output. Normal and `python -O` executions are byte-identical. The known arbitrary-order tensor-classification theorem is a cited input, not inferred from six checked powers.

The new file's geometric/script controls are not a replay of the whole 42-equation parent certificate, a new Lean proof, independent review, remote CI or proof of an actual Book filter. Prior checks and receipts remain unchanged. `GR_closed=false`.

### Pinned repository inputs

All at `c49ebdb12244943d1ec45ef6d148a0432481141e`:

- `D0_GR_PRIMARY_POSITIVE_CASE.md` (same field/matter/mesh witness).
- `A4D_PRIMARY_NORMAL_SOURCE_RECOVERY_SYNTHESIS_2026_10_21.md` and its source packet (Green bound, same-source assumptions).
- `A4D_CAUSAL_BOOK_SOURCE_TO_EXACT_GR_SYNTHESIS_2026_10_20.md` (complete source and causal elimination).
- `A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md` (finite ratio and its local-density/internal scope).
- `A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md` (distinct all-metric rigidity route, actual source descent still required).
- `A4D_NATIVE_JOINT_FIELD_MINIMUM_EXCLUSION_2026_10_20.md` (stationary is not a field minimum).
