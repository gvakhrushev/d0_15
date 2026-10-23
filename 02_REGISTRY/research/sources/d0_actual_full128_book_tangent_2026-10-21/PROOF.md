# Corrected full128 Book mean/pressure gap: an actual proper-Lorentz tangent

21 October 2026. Scientific continuation in existing Draft #334. Scope: original 128-Kraus one-round instrument, one explicitly supplied proper-Lorentz/Julia chart, the mathematical amplitude-bound Book **candidate** and the complete classical-record mean. This is not a proof Book03 selects either aggregation. GR_closed=false.

## 1. Reject an unphysical probability tangent

The literal original nonblank pair is

\[
K_{0,k}=-2p^2N_k^*A,\quad K_{1,k}=-2p\sqrt p\,N_k^*A,\quad k=1,\ldots,63,
\]
where \(p=\varphi^{-1}\), \(p+p^2=1\), \(A=N_0\), and \(N_k\) are the original full16 Walsh/Julia rows. Thus, for every physical field/preparation tangent, the *joint* positive probabilities obey
\[
q_{0,k}=p^2 x_k,\quad q_{1,k}=p x_k,\quad x_k=q_{0,k}+q_{1,k},
\qquad D(q_{1,k}/x_k)=0.
\tag{1}
\]
The earlier `A4D_BOOK03_FIRST_SOURCE_UNDERDETERMINATION_THEOREM_2026_10_21.md` §3 proposed \(Dq_0=-1,Dq_1=+1\) **within one such conditional pair**. That is not a tangent of the actual original full128 instrument. Its claimed witness \(-1/2\) in that scope is withdrawn. The abstract scalar identity \(D\bar S-DP_B=\tfrac12 DH\), when the amplitude binding is *assumed*, remains exact, but needs a **real** nonzero full-record entropy tangent.

## 2. Exact all-outcome grouped entropy and full derivative

Keep **both** original blank-label ports as separate outcomes, \(q_{0,0},q_{1,0}\), plus all 63 nonblank label pairs. Let \(h_G=-p^2\log_\varphi p^2-p\log_\varphi p=2p^2+p\). The chain rule gives an exact finite identity on any positive support:
\[
\boxed{H_\varphi(q_{128})=
H_\varphi(q_{0,0},q_{1,0},x_1,\ldots,x_{63})+
 h_G\sum_{k=1}^{63}x_k.}
\tag{2}
\]
Zeros are retained but omitted only from terms of the form \(0\log0\). In a smooth stratum of constant support,
\[
\boxed{D H_\varphi(q_{128})=
-\sum_{b=0}^1Dq_{b,0}\log_\varphi q_{b,0}
-\sum_{k:x_k>0}Dx_k\log_\varphi x_k
+h_G\sum_kDx_k.}
\tag{3}
\]
The \(+1/\ln\varphi\) derivative contributions cancel because \(\sum Dq=0\). Equation (3) respects the unchanging original port ratios (1); it is not a hypothetical classical reallocation.

Grant as a separate explicit hypothesis that the normalized Book amplitude equals the entire purified orthogonal record, with branch prices \(S_\omega=-\tfrac12\log_\varphi q_\omega-J\). Then the two distinct scalar candidate actions obey
\[
\bar S=\tfrac12H_\varphi(q_{128})-J,\quad P_B=-J,
\quad \boxed{D\bar S-DP_B=\tfrac12DH_\varphi(q_{128}).}
\tag{4}
\]
Book03 must still select which (if either) action/Info law is physically compulsory. The complete binary-port Cost\(-\)record-entropy functional, which is a different declared CQ price, obeys
\[
S_{CQ,\text{port}}=1+\sum_{k=0}^{63}q_{1,k}-H_\varphi(q_{128}),
\qquad DS_{CQ,\text{port}}=\sum_kDq_{1,k}-DH_\varphi.
\tag{5}
\]
This is only the original port part of the actual paid ledger; all other work, controller, clock and Book Info must be retained separately.

## 3. Literal original 16-CAR, 128-Kraus proper-Lorentz witness

The supplied checker constructs the complete original 32 Walsh-controlled Julia words, both coefficient columns, complete 16-grade CAR lift with exterior order (0,2,3,1), the original native parameter \(\nu=3/5\), p, both Golden ports, and actual fixed oldRIGHT purification \(\rho=I_{16}/16\). One proper-Lorentz link moves as \(U(\theta)=\exp(\theta X_G)\) where \(X_G=\sum X_{ij}c_i c_j^\dagger\), \(X_{01}=X_{10}=1\). The generated 16-grade lift and strict Julia square roots are differentiated **analytically**: for \(R=\sqrt S\), \(DR\) is the unique solution of \(RDR+DRR=DS\), computed in the exact spectral divided-difference formula \((DR)_{ij}=(DS)_{ij}/(\sqrt{\lambda_i}+\sqrt{\lambda_j})\). No frozen Julia root, preparation, complete flag or oldRIGHT term is silently deleted.

Writing each original Kraus operator as \(K_{b,k}(\theta)\), the **full** field entropy source is evaluated from
\[
q_{b,k}={1\over16}\operatorname{Tr}(K_{b,k}^\dagger K_{b,k}),\quad
Dq_{b,k}={2\over16}\Re\operatorname{Tr}(K_{b,k}^\dagger DK_{b,k}),
\tag{6}
\]
and (3). The native channel obeys \(\sum_{b,k}K_{b,k}^\dagger K_{b,k}=I\) and its entire derivative is zero. All128 labels remain; 64 are identically dark in this specific even/odd-character fixture. On the constant 64-positive-outcome stratum, the analytic expression is smooth.

At \(\theta=0.08\), the **numerical diagnostic, not an interval certificate**, is
\[
D_\theta H_\varphi(q_{128})=-0.019550941179130216,\quad
D_\theta \mathbb E C_{\text{port}}=-0.001118765021955193,
\]
\[
D_\theta S_{CQ,\text{port}}=+0.018432176157175025,
\quad \tfrac12 D_\theta H_\varphi=-0.009775470589565108.
\tag{7}
\]
The checker also computes theta=0.04 and 0.12, uses all 128 complete Kraus branches, enforces exact port ratio identities (1) and all output normalization and linearized completeness, rederives (2) and (3) from the grouped 65-bin distribution, and independently checks analytical derivatives by real finite differences at 10^-4,10^-5,10^-6. Numerical agreement is ~10^-10 or better. Equation (2), the Kraus identity and the amplitude-bound algebra are exact analytic theorems; a rigorous floating-point enclosure of (7) has **not** been supplied, so (7) is a strong diagnostic, not an independent interval-certified source no-go.

## 4. What this changes, and what it does not

It repairs the specific same-execution defect in the earlier purported \(-1/2\) witness and gives a real *full128* information source that does not vary the immutable Golden nonblank conditional coins. Even if normalized amplitude matching is granted, the mean-path and log-amplitude-pressure DIFFERENTIALS are mathematically distinct on this actual Lorentz chart, with their difference determined by (3), not by arbitrary relative Info coefficients.

**It does not demonstrate that either candidate is an allowed complete physical Book03 action.** Nor does it identify the full128 port-only CQ score with the same selected all42 source or close GR. Physical selection of the original memory-valued aggregation, actual branchwise Info/Cost and preparation/clock/work sources remain. The result prevents using a physically impossible tangent to pretend those obligations are closed. GR_closed=false.
