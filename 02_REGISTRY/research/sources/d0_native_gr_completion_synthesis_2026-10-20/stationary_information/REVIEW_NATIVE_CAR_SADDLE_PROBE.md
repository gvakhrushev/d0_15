# Independent read-only review: same-slice native CAR information direction

20 October 2026. Reviewer: full_price_weld. Existing PR #334 only.

**Verdict: PASS, no remaining blocking mathematical or scope defect found.**

Reviewed final note:
`/private/tmp/d0_equation_equivalence_20261020/EQUATION_EQUIVALENCE_AND_RECORD_TEST.md`

SHA-256:
`45cfe4eb454a11433a08168fd20797ff861dca67ce9147dbf7f3a8c341d6de77`.

Final delta from the previously reviewed `f4b42aa2...` bytes: the ancillary
post-hoc multiplier construction in section 2 now explicitly assumes C3
regularity. This harmless regularity-qualifier correction preserves the
reviewed mathematics and scope. Section 5.1 and the checker are unchanged;
no additional searches or checker runs were performed for this update.

Associated checker:
`check_equation_equivalence.py`, SHA-256
`00eba64b158a80120d052c95bf95833c8ee23c7907bcfe546f1c77ea6d0492d8`.
The author reports PASS; this review independently checked the derivations
and inspected the checker, without repeating its execution.

Repository inspected at `20d976647fa52e247d15139d3f4f14351f175b70`.
Read the actual `book_source/NATIVE_CAR_ACTUATED_METRIC.md`, the original
8D fixed-basis checker, the primary native-domain RESULT, the local LEFT
query source, and the already accepted stopped saddle formula. All paths
are in the existing worktree. No repository files were modified.

## Independently verified calculation

For the displayed null-coordinate tetrad, direct inversion gives

    ghat^-1=s_cal^2 [[0,1/a,0,0],[1/a,0,0,0],
                    [0,0,-1,0],[0,0,0,-a^2]].

The addressed CAR rotation changes the actual REST top amplitude at the
central site by a fixed delta. A constant initial scalar/top profile then
has top forward differences (-delta/h) in all four directions at that
site. Contracting with this inverse metric gives exactly

    q_i(a)=s_cal^2 delta^2 (2/a-1-a^2)/(rho_0 h^2),
    q_i(1)=0,
    q_a(1)=-4 s_cal^2 delta^2/(rho_0 h^2), q_u=0.

At each affected backward neighbor only one derivative changes, and the
held neighbor coframe makes its q_i independent of a,u. The nonzero
neighbor baseline probabilities are retained, rather than replaced by
the central null baseline.

For the actual full 8D returned compression, (1,-1) is an eigenvector
with eigenvalue 1-2b independently of E. Its complementary cut therefore
has probability B=1-(1-2b)^2=4b(1-b). With
b=(p+sigma p^2 eta'^2 q_i)^2, using 1-2p^2=p^3 gives

    B_*=4p^3,
    B_a=-32 sigma p^6 eta'^2 s_cal^2 delta^2/(rho_0 h^2),
    B_u=0.

For the normalized address/readiness law, the two central components
have derivatives r omega_0 B_a and -r omega_0 B_a. The corresponding
probabilities are r omega_0 L and r omega_0(1-L). All other retained
coarse outcomes have zero slice derivative. Summing (dP)^2/P and
dividing by ln(phi) proves exactly

    K_aa=r omega_0 B_a^2/[ln(phi)L(1-L)]>0, K_au=K_uu=0.

The stated full-price comparison is explicitly conditional. For its
hypothetical sum with the already owned stopped second form, when
kappa<0 the u-u entry is positive and the determinant is

    (-kappa) g [2D K_aa-(-kappa)g].

Thus the PSD threshold is K_aa >= -kappa g/(2D), with positive definiteness
for strict inequality. For kappa>0 the negative u-u entry cannot be repaired
by this one coframe-direction statistic. There is no sign or factor error.

## Record, calibration and scientific scope

Two initially implicit conventions were made explicit before acceptance:

1. The displayed null geometric frame is not the Euclidean CAR mask basis.
   The final note keeps the original REST four-mask state, T map, actual
   raw frame rho^-1/2 T ehat, conjugated proper links and the original
   epsilon/Hodge orientation pullback. The fixed calibration is transported
   by the owner's exact off-shell price identity with its declared gains;
   no Hessian identity is inferred from first-source equality alone.
2. omega is the entire normalized retained address law, including inactive
   and unchanged addresses, or an explicit remaining constant-mass outcome.
   The central omega_0 is not normalized among the active addresses. Abort
   is retained; an identically absent abort only has zero Fisher support.

The native operation retains the full CAR complement, changes its coupled
slack coherently and preserves the oldRIGHT Gram; it is not a top-only nonunitary
edit. The fixed minus preparation is a supplied, paid probe preparation,
not a field-dependent eigenvector oracle. Coarse scoring of the retained
output is not a claim that fine records have been erased. A singular full
KL is explicitly distinguished from the finite coarse statistic.

The conclusion is an actual nonzero sensing direction on the same saddle
slice, conditional on the inherited live material-code/query interface and
address/preparation admission. It is not a price-faithful field-action map,
selected Info, a compelled reference, a root-preserving action, or GR.
The actuated matter is explicitly not asserted to remain an Einstein root.
No free repetition factor or tunable multiplier is used to assert the
threshold. Full extra sources and clock/preparation charges remain due.

The surrounding matrix-equivalence argument is also correctly scoped:
closedness is required off the root; an invertible source multiplier can
change inertia when it is not positive, but an actual coordinate pullback
cannot. The scalar cleaned-record obstruction is not promoted into a
no-go for every possible additional native record or physical price.
