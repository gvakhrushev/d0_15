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

    J_full=-log det K_II-log det(K_EE-K_EI K_II^-1 K_IE).

Every internal factor and its derivative are retained. The positive Schur block has spectrum within [1-z,1]. Operator block elimination is not physical stationary-field elimination and is not a proof of refoliation invariance.

## Execution and boundary

Executed with Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, PyTorch 2.10.0+cpu and SymPy 1.14.0. Normal and python -O JSON outputs match byte-for-byte. Full Hessian vs AD error <=1.18e-16; finite-difference gradient Hessian error <=1.11e-11; stationary boundary Schur check 9.38e-13; symplectic defect 2.26e-13; actual implicit-map Jacobian relative error 2.59e-11. Removing the interior determinant changes the tested source by 0.0777634. Frozen-interior and commuting-covariance controls also fail as expected.

The numerical controls use structural finite-matrix charts (with a frozen Golden/SourceI block), NOT a physically proved D0 causal boundary. A native boundary map, its stationary branch and mixed rank, metric identification, local lapse generators and their algebra remain unconstructed here. A formal canonical relation for a scalar price does not by itself equal the physical evolution supplied by U. No original all42/READY replay, Lean, CI, universal GR, or scientific promotion is claimed. `GR_closed=false`.

Executed checker SHA256: `226222ebc056869c4fbe2df916fa1ccaebf2ceb6a6e0190bdd3c15d764770e86`; Git blob `bd7aacf768beb0b9be79b3e76c38161a7c8e76c7`.
Observed result SHA256: `94310fbd18e51708c8e91b5ceb74ccf09677911d93e4e428badeefb05ceb33dc`; Git blob `95b454f07beec518b6feae0f5e8338328b901074`.
