# Joint H+J stationarity does not preserve a field source carried by the same free controller

31 October 2026. Existing research PR #334, `gvakhrushev/d0_15`.
Input: `1e44de960dabaa86d47d86dfa6193d55d5fd5742`.

[Full Russian proof](sources/d0_joint_source_balance_2026-10-31/PROOF_RU.md),
[executed checker](sources/d0_joint_source_balance_2026-10-31/check_joint_balance.py),
[observed result](sources/d0_joint_source_balance_2026-10-31/result.json).

## Actual attempted closure

The previous native-word result left a nonzero QUERY source on an isospectral
reflection orbit. This packet tests the untried alternative: solve that source
jointly with the already-present full homogeneous Book03 heat, rather than
restrict the variation or add a compensating action. It uses the same price,
K(9,11,13), beta=2p^2, zeta=2^-20, 32-dimensional carrier and canonical rank-eight
input. A new non-reflection endpoint family changes the spectrum; it is NOT
asserted to be the old fixed-report task or an emitted native programme.

The result is a mathematical complete-source critical point, followed by a proof
that this particular cancellation cannot complete the reporter-to-Einstein map.
No unrestricted physical D0 closure or universal impossibility is claimed.

## Full endpoint stationarity, not one angular equation

On the input and an equal-dimensional return complement take
U(c)=[[c I,-sqrt(1-c^2) I],[sqrt(1-c^2) I,c I]], with identity on the remaining
16 coordinates. Conjugate both U and the input by the original two Golden births.
The true compression is c I8, and

    J(c)=-8 log(1-zeta+zeta c^2).

With all scene/right/clock modes retained, the old winding theorem gives

    Z_N(c)=ND(2a0+359)+4N sum_(k>=1) a_(kN)[D-2r+2r T_k(c)],
    D=32, r=8, H_N=log Z_N/beta.

Exact rational bounds prove, for EVERY fixed N>=4, that B_N=H_N+J has a unique
critical c_N in (0,1/16). They establish B_c(0)>0, B_c(1/16)<0 and B_cc<0
throughout that interval, using the full positive Laurent coefficients and
standard Chebyshev/Bessel identities. Numeric roots are diagnostics, not the
existence proof. At N4, c_N is approximately0.00031895957879453447 and
H_c=-J_c approximately4.8669415737663557e-9.

For every skew-Hermitian endpoint generator X, a direct computation of BOTH
terms gives

    DB_N[XU]=[-sqrt(1-c^2) B_c/(2r)] ReTr(J0^dagger X),

where J0 is the active rotation generator. Thus the whole U(32) covector
vanishes at c_N, including all496 real orthogonal directions and their complex
extension. Rank-fixed cut variations vanish too. Beta, scene, rank, Gram and
clock length remain fixed; their independent equations are not claimed solved.
N is a mathematical clock length, NOT a claimed compiled word length. Exact
native factorization of these critical endpoints is not proved. Changing the
length changes the critical point; compilation density alone cannot erase this
coupling. There is a negative second-variation direction, so no minimum claim.

## Why the missing normal cannot be selectively cancelled on this route

If a field Y and an independent controller t enter the same fixed price only
through c(Y,t), controller stationarity B_c=0 simultaneously makes D_Y B=0.
Locally c(Y,t)=c0(Y)+t and the stationary section is t_*(Y)=c_N-c0(Y). Hence

    B_eff(Y)=B_N(c_N),
    H_eff=H_YY-H_Yt H_tt^(-1)H_tY=0.

The effective action is constant, not Einstein gravity. A positive RETURN gain
at c_N is not a nonzero FULL field gain: the latter has cancelled along with
the unwanted controller row. The check preserves a nonzero off-shell field
covector to expose this false closure.

More generally, on ONE map Xi(Y,t), if D_Y Xi=D_t Xi L with all other price
arguments fixed, then exactly E_Y=L* E_t. This includes real norm constants in
approximate statements. No source can be removed by calling the controller
internal while retaining its identical field direction. This does not cover
an independent source from the true spatial Dirac, moving scene or another
actually selected price argument. Their same-execution sources would have to
be computed, not inserted by hand. The physical admission of the free controller
is not deduced here; a fixed-task graph is a different domain with its reaction.

## Actual checks and status

47 checks executed; ordinary, python -O and repeat outputs are byte-identical.
All1024 endpoint basis directions are separately evaluated. Complete33-scene
spectral reduction, independent positive Laurent series, 65-digit full H+J
finite differences, all54,400 Hodge modes at N4 through exact multiplicities,
and symbolic Schur elimination are checked. Maximum numeric full endpoint
source residual5.05e-23, compared with individual H/J components3.76e-10.
Removing the harmonic contribution breaks the balance. The old reflected QUERY
source remains nonzero, consistently with the preceding result.

A cut-derivative transpose error in the first code draft was detected and fixed;
the final trace coefficient is -2zeta(EU-UE). This is recorded in the proof and
local run receipt. Analytic source and root theorems do not rely on the runtime
check count or numerical zero thresholds.

No new native word, full42 geometric root, Einstein PDE trajectory, physical
variation-domain proof, Lean, CI, main merge or accepted-claim promotion.
`GR_closed=false`.
