# Root bootstrap: full spectral Hessian and conditional boundary relation

28 October 2026. Existing owner: PR #334 in gvakhrushev/d0_15.
Input checkpoint: `c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a`.

[Full proof in Russian](sources/d0_root_boundary_reduction_2026-10-28/PROOF_RU.md), [executed checker](sources/d0_root_boundary_reduction_2026-10-28/check_root_boundary.py), [observed result](sources/d0_root_boundary_reduction_2026-10-28/result.json).

Consume the unchanged [moving-cut root source](A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md) and address the boundary-data premise of the [conditional refoliation theorem](A4D_ROOT_CUT_TO_REFOLIATION_CLOSURE_2026_10_28.md). Do not replace the root price by an encoded target polynomial or the ADM action.

## Mathematical result

For the full Book03 functional `B=beta^-1 log Tr exp(-beta Delta)-log det(I-zF)`, including moving P in F, its exact coordinate Hessian is

    B_ab = beta Cov_rho(Delta_a,Delta_b)-Tr(rho Delta_ab)
           +z Tr(R F_ab)+z^2 Tr(R F_b R F_a),
    R=(I-zF)^-1, rho=exp(-beta Delta)/Tr exp(-beta Delta).

Cov is the noncommutative Kubo–Mori integral, not an ordinary product covariance. No commuting-variation assumption or omitted thermal normalizer is used.

For a PROVIDED actual boundary chart x=(x_-,x_+) and interior w, a regular solution B_w=0 yields the exact reduced Hessian

    S_ab=B_ab-B_aw B_ww^-1 B_wb.

The boundary response p_-=-S_-, p_+=S_+ is a Lagrangian relation and, if the mixed boundary Hessian is invertible, gives a symplectic map. This uses the standard generating-function formalism, explicitly credited in the proof. The interior can be a saddle; no global minimum is assumed.

For a separate OPERATOR block partition of K=I-zF, exact determinant sewing is

    J_full=-logdet K_II-logdet(K_EE-K_EI K_II^-1 K_IE).

Every internal factor and its derivative are retained. The positive Schur block has spectrum within [1-z,1]. Operator block elimination is not physical stationary-field elimination and is not a proof of refoliation invariance.

## Execution and boundary

Executed with Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, PyTorch 2.10.0+cpu and SymPy 1.14.0. Normal and python -O JSON outputs match byte-for-byte. Full Hessian vs AD error <=1.18e-16; finite-difference gradient Hessian error <=1.11e-11; stationary boundary Schur check 9.38e-13; symplectic defect 2.26e-13; actual implicit-map Jacobian relative error 2.59e-11. Removing the interior determinant changes the tested source by 0.0777634. Frozen-interior and commuting-covariance controls also fail as expected.

The numerical controls use structural finite-matrix charts (with a frozen Golden/SourceI block), NOT a physically proved D0 causal boundary. A native boundary map, its stationary branch and mixed rank, metric identification, local lapse generators and their algebra remain unconstructed here. A formal canonical relation for a scalar price does not by itself equal the physical evolution supplied by U. No original all42/READY replay, Lean, CI, universal GR, or scientific promotion is claimed. `GR_closed=false`.

Executed checker SHA256: `226222ebc056869c4fbe2df916fa1ccaebf2ceb6a6e0190bdd3c15d764770e86`; Git blob `bd7aacf768beb0b9be79b3e76c38161a7c8e76c7`.
Observed result SHA256: `94310fbd18e51708c8e91b5ceb74ccf09677911d93e4e428badeefb05ceb33dc`; Git blob `95b454f07beec518b6feae0f5e8338328b901074`.

## Same-carrier application of the concurrent QUERY/cut result

Consume the incoming `172876cdf38bfce6f87fdd4a059d524b60c10eb9`, same residual memo section7cu, equations831 and835. The primary owner and its task brief are left unchanged.

[Exact application](sources/d0_root_boundary_reduction_2026-10-28/QUERY_ORBIT_APPLICATION_RU.md), [executed full-column checker](sources/d0_root_boundary_reduction_2026-10-28/check_query_cut_orbit.py), [observed receipt](sources/d0_root_boundary_reduction_2026-10-28/query_cut_result.json).

For the SAME reflection Q, true prepared psi, c=<psi,Q psi>, u=sqrt(1-c^2), K0=[Q,|psi><psi|], independently transport QUERY by t and its active cut by s. On the whole protected/work carrier the exact feedback is

    J(t,s)=-R log(1-zeta+zeta[c cos(2u(t-s))-u sin(2u(t-s))]^2).

Thus j'(0) is the original row831, and the second relative source is

    j''(0)=8R zeta u^2[1-(2-zeta)u^2]/(1-zeta u^2)^2,
    Hessian_(s,t) J=j''(0)*[[1,-1],[-1,1]].

This extends the original complete first cut-balance835 to the finite action and its full two-parameter jet. Pure joint transport is null; relative response remains. The exact mixed-rank-loss condition is c^2=(1-zeta)/(2-zeta), so no uniform twist is assumed. If those coordinates belong to a real boundary problem, their generating relation has equal boundary momenta, not automatically zero Euler sources. Actual physical temporal-boundary identification is NOT supplied by this algebra.

The incoming DH=0 at its reflection base is not used as proof of D2H=0; the full thermal Hessian above remains necessary unless an actual isospectral family is established. The different unpadded rank-two root, tau=0.05, its nonzero direct-click row and the common-null carrier are not identified.

Symbolic identities hold for arbitrary original c. A six-column rational control with protected rank2 inside dimension3 verifies values, gradient and Hessian, at both zeta=1/7 (structural control only) and original 2^-20. Maximum Hessian discrepancy 2.45e-15; normal/-O receipts match. No original26-stage/full42/Lean replay or GR promotion.

Executed added checker SHA256: `eacd5d6456bacde02ddf3bab22f8ea7782ccdfcecce7afc232d928d9692f2fd9`; Git blob `fac2d4717b13a1f87767ad3c9a06e7e1cf6be882`.
Added receipt SHA256: `272502430370992230f6575fa558d8681d0b90dd9f9c4cfa9106d4be35e4ecd6`; Git blob `f9ef19b2ad8a5c8f54cb665741dcc3fed442c8e4`.

## Consuming application: solve the independent QUERY before using its Schur block

The [retained-history final composition](A4D_RETAINED_HISTORY_FINAL_COMPOSITION_2026_10_28.md)
now classifies the whole relative reflection QUERY critical set for the
unchanged return. At full free-QUERY stationarity the active compression has
only eigenvalues -1,0,+1, and every connected fixed-rank stationary section
has J=-m log(1-z). If EVERY stage remains INTERNAL over the whole section
and scene, clock, beta, dimension and reflection signature are fixed, the
complete heat is also constant. Hence the actual reduced boundary Hessian
in this application is zero, including after a justified gauge reduction.
The general conditional Schur theorem remains valid; its nonzero mixed-rank
hypothesis is not supplied by this free-QUERY elimination. Genuine restricted
tasks, noninternal histories, varying scenes and actual extra prices retain
their separate physical applications. No promotion of GR closure follows.
