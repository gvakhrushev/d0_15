# Refinement maps: what exists, and the correct boundary-source comparison

Read-only inspection at scientific commit `41582f57ce2b4bc8c9fad322e3c2d8ecaadb8b70`, 20 October 2026. Existing #334 integrator. This is a scoped source audit, not a claim that no related theorem exists anywhere in the repository.

## 1. Four different maps must not be conflated

### A. The actual finite-point archive tower

Exact Lean types in `03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean`:

- `D0.ArchivePoints n := Fin (archiveTower n).modes`, with modes `(n+2)^4`.
- `D0.archiveProjection n : ArchivePoints (n+1) -> ArchivePoints n`, implemented by reduction modulo the coarse cardinality.
- `D0.archiveProfiniteSystem : FiniteInverseSystem`.
- `D0.archive_record_kernel_projectively_compatible`: entrywise pullback of the record kernel. The older name `archive_laplacian_projectively_compatible` is explicitly a legacy alias, not a graph-Laplacian theorem.

The categorical owner `03_FORMALIZATION/D0/Geometry/ArchiveLightProfinite.lean` defines:

- `D0.archiveFintypeDiagram : Nat^op -> FintypeCat`;
- `D0.archiveLightDiagram : LightDiagram`;
- `D0.archiveLightProfinite : LightProfinite`.

The generic `D0.CompatibleOperatorFamily (S : ProjectiveSystem)`, in `03_FORMALIZATION/D0/Condensed/OperatorNaturality.lean`, has

    op : forall n, S.Stage n -> S.Stage n.

Its naturality is a commuting diagram of *point endomorphisms*. This is not a type of real Hessian forms, coframe fields, Jones operators, or physical heat generators. `inducedLimitOperator` maps coherent points to coherent points.

The first actual sizes are 16,81,256 with nonuniform fibres 5/6 and 3/4. Equality of cardinality with a possible four-dimensional grid does not identify the modulo map with geometric mesh refinement or source transport.

There is an already-owned stronger scoped discriminator in `A4D_NATIVE_HODGE_ARCHIVE_METRIC_REFINEMENT.md`: for *every* bijective identification of the archive points with the full scalar Hodge four-torus sites, the actual long map from 2L to L has metric distortion at least

    ((L+1)^(1/4)-1)/(4L).

Thus it is not an O(h) metric refinement in that complete class. This does not exclude slower o(1) convergence, other represented observables, or a different physically derived readout.

### B. An actual full matrix/Jones refinement DOES exist

`A4D_NATIVE_GOLDEN_COST_REFINEMENT.md` constructs the original Fibonacci AF inclusion

    A_n=M_a(C) (+) M_b(C),
    alpha_n(X,Y)=(diag(X,Y),X),
    tau_n(X,Y)=p^(n+1)Tr(X)+p^(n+2)Tr(Y),
    C_n([[X,U],[V,Y]],W)=(pX+p²W,Y).

It is trace preserving, `C_n alpha_n=I`, and its full GNS complement retains both rectangular blocks. Precise generic/formal owners include:

- `D0.Algebra.FibonacciAFTower.pathCount`, `dimA`, `gns_refinement_isometry`;
- `D0.Geometry.FibonacciBratteliRefinement.Mphi`;
- `D0.Research.GoldenCostRefinement.actual_trace_preservation`,
  `actual_gns_isometry`, `actual_conditional_adjoint`, `expect_retraction`.

`A4D_NATIVE_JONES_RECORD_TRANSPORT.md` goes further. The actual all-level frame overlap is p³, and the square R_n of the original Golden gate rotates the included old Jones corner to the next corner while fixing its orthogonal complement. The composite

    alphaHat_n = Ad(R_n) alpha_n,
    CHat_n = C_(n+6) Ad(R_n*),
    CHat_n alphaHat_n=I,
    alphaHat_n(e_n)=e_(n+1)

transports every corner outcome including off-diagonal records. Its named capsule statements include `D0.Research.JonesRecordTransport.owned_square_transport`, `all_frame_outcomes`, `conditioned_state_covariance`, and `conjugated_refinement`. The capsule uses explicit frame hypotheses; actual all-level native path binding has the stated separate analytic/certificate status.

This is a positive algebraic state/record refinement. It is not a theorem transporting the HJR seven-slice Hessian, a physical coframe tangent, or the selected Book03 action. The same owner distinguishes ordinary inclusion from the composite operation and leaves physical execution/preparation/metric variation open.

The separate recent Jones+ full128 observer/tomography experiments use one homogeneous L4 Fourier mode. Their owners `A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md`, final paragraph, and `A4D_ORIGINAL_FULL128_COMMON_METRIC10_LINK24_JONES_TOMOGRAPHY_2026_10_20.md`, opening paragraph, explicitly state that these are not the curved Brinkmann carrier and not refinement results.

### C. The configured Brinkmann continuum-to-finite recovery DOES exist

`A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md`, Sections 7–9, gives a family of maps from fixed smooth continuum solution data to actual finite configured Golden-J2 roots:

    R_h : (Psi, W) -> (coframe_h, proper_links_h, CAR16_history_h).

The installed coframe uses `tau_j=jh-h/2`; links are the original Cartan-determined differences. Matter is constructed by

    Psi^(h)_(j+1)=Psi^(h)_j+h Psi'(jh+h/2).

All original 16 coframe +24 proper-link +2 matter Euler rows vanish exactly at all free interior sites of each admissible mesh.

For the maximal exactly sampled transverse class

    span{1,x,y,x²-y²,xy,x³-3xy²,3x²y-y³,xy(x²-y²)},

the metric is the same fixed continuum metric sampled at each mesh's true midpoint readout. For arbitrary smooth harmonic profiles, the owned `D_h` discrete Dirichlet lift and `I_h` reconstruction from finite records give C^r metric and curvature recovery with O(h²) control on compact interiors. Section 9 explicitly distinguishes derivatives in solution data from the Hessian of the unrestricted action.

This is a positive continuum-to-finite right-inverse/recovery family. It is not automatically an exact finite-to-finite projective system. A literal control:

    Psi'(u)=u², Psi(0)=0.

One coarse midpoint increment over [0,h] is h³/4. Two fine h/2 midpoint increments total 5h³/16. They differ by h³/16, although both produce exact configured roots and converge to the same continuum matter field. Coframe readout grids `jh-h/2` and `kh/2-h/4` are not nested either. These differences do not invalidate recovery; they prohibit silently calling it literal state restriction.

### D. Seven-slice HJR boundary response remains a fixed-L8 result

`A4D_WIDE_COLLAR_DIRICHLET_TO_NEUMANN_REVERSE_SOURCE_2026_10_20.md` consumes one L8 source with 64 internal variables and one boundary deformation. It proves

    S_eff''(0)=K_partial/8,
    K_partial=C-b^T A^-1 b,
    57/1000 < K_partial <49/100.

Interior A is invertible but has negative directions; its elimination is stationary, not an assumed minimum. All incoming/incident link and moving-Riesz data are kept.

The last step of its Section 5 explicitly leaves compatible fixed-physical-width smooth collars and a uniform full-joint inverse/refinement estimate for subsequent proof. The exact collar owner `A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md`, Section 11.8, provides uniform C² preparation/Rayleigh bounds on a discrete-C¹/O(h)-link chart, but explicitly excludes a uniform inverse of the full HJR field Hessian or a nonshrinking joint-IFT radius. A thin collar jump of amplitude epsilon has Lipschitz size approximately epsilon/h; a fixed epsilon is not in its uniform smooth chart.

In these named sources and a targeted search of the corresponding archive/condensed/Fibonacci formal owners and research refinement/collar/Jones owners, no actual interlevel map transporting this K_partial was found. This is a scoped inspection finding, supported by the owners' explicit open boundary. It is not an assertion that the positive Jones and Brinkmann maps are absent.

## 2. The correct refinement law for a Hessian is congruence after actual elimination

Let the fine action be S_f(i,b), where i is its full admitted interior set and b its physical boundary. Suppose its actual interior equations admit a smooth stationary branch i=sigma_f(b), with invertible internal Hessian on the appropriate quotient. Define

    W_f(b)=S_f(sigma_f(b),b),
    K_f = S_bb-S_bi S_ii^-1 S_ib.

No positive-definiteness assumption is needed for this algebraic stationary formula.

Let beta send coarse physical boundary data c to fine boundary data b=beta(c). If the *actual source-normalized coarse action* satisfies

    W_c(c)=W_f(beta(c))+constant,

then by the chain rule, with B=D beta,

    t_c=B^T t_f,
    K_c=B^T K_f B + sum_a (t_f)_a D² beta_a.

At a common fully stationary boundary base, t_f=0, hence

    K_c=B^T K_f B.

The same simplification holds for linear beta even away from boundary stationarity. If physical action normalization includes a prescribed field-independent factor a, the right side acquires a; absorb it into the definition of normalized K rather than dropping it. A moving normalization contributes additional first/second source terms.

The equality is not implied merely by both actions having stationary roots. It requires the actual coarse/fine action-source correspondence. Literal matrix equality is generally false even under perfect physical compatibility because sizes, tangent normalization, coordinates and volume weights differ.

If some new fine boundary modes are also internally relaxed rather than prescribed by beta, first include them among i. Equivalently, use the genuine stationary boundary lift B_eff: its additional components solve their actual stationarity equations. An arbitrary interpolation matrix B is not automatically this lift.

Sequential elimination is associative: for a full block Hessian in kept variables c and two internal groups y,z,

    Schur_y(Schur_z(H)) = Schur_(y,z)(H)

when the relevant actual blocks are invertible. Thus one may eliminate new refinement variables, then old interior variables, or all together. Freezing either group gives a different form.

For response *operators* identified using positive tangent pairings G_c,G_f, distinguish K from L=G^-1 K:

    G_c L_c = B^T G_f L_f B.

Only when B is isometric does this become the familiar adjoint compression L_c=B* L_f B. The original Lorentz field metric should not be confused with this positive coordinate pairing.

**Consequence for proposal screening.** Failure of untransported matrix equality cannot justify discarding a physical source. Even failure of one proposed B only rejects that proposed correspondence. To identify an irrelevant regulator effect one needs the actual normalized transport and an estimate

    ||K_c-B^T K_f B|| ->0

in the declared physical source topology, or a stronger exact relation. A nonzero finite discrepancy can coexist with a valid continuum limit.

## 3. Compatibility alone still leaves the price unspecified

The complete owner `A4D_NATIVE_CONDENSED_PRICE_NATURALITY.md` proves, for actual positive conditional pairings and maps J,C with CJ=I, the self-adjoint compatible heat extension class

    L_f=J L_c C + Q B Q,     Q=I-JC,

with an arbitrary self-adjoint new-complement block. It has corresponding named capsule theorem `D0.Research.CondensedPrice.natural_extension_complete`, plus `uniform_gap_all_level_compatibility`, `genuine_full_price_source`, `complete_scalar_price_jet_fibre`, and `fixed_phi_shape_source_nonzero`.

The source-visible freedom survives all-level compatibility, actual phi spectral norms and a trace-class heat limit. Therefore an actual refinement map is necessary data but does not by itself select the Book price or its geometric source. This is already proved; repeating a rank/naturality census would not close the missing mechanism.

The research focus is to attach one actually selected full action and physical boundary/clock readout to the existing positive recovery maps, prove the stationary source transport, and then consume the known Einstein sector. It is not to discard every finite quantity that changes when one increases an archive level.

## 4. Existing cochain source already shows why a noninvariant term cannot simply be discarded

`A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md`, Sections 1–3, concerns a *different* actual graded cochain lift J, with `d_f J=J d_c` on all sixteen exterior sectors. Its coordinate folding differs from the flat-index archive map and from the AF matrix inclusion.

The complete retained compression obeys

    C D_f J=D_c,
    C D_f² J=D_c²+R^dagger R,
    R=Q D_f J, Q=I-JC.

The reaction R^dagger R is positive and has its own actual source derivative, including moving pairing, J and C. The heat source is evaluated in the Gibbs state of the *complete* `D_c²+R^dagger R`, not the Gibbs state of D_c². The owner proves that no positive local diagonal pairing can make the literal lift an adjoint intertwiner, while a nonlocal pairing can repair it and leaves a source-visible modulus.

This is an existing exact example where a refinement mismatch identifies a real missing term rather than authorizing its removal. It does not prove that this cochain compression or its heat is the selected Book03 physical action. The correct retained source and the physical selection problem remain distinct.
