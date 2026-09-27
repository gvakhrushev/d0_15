# A4D FUGU response intake and task map

**Intake date:** 2026-09-27  
**Repository baseline checked:** main at 420cf140adabacadd73e6fd8da556b4f36f7c6e1  
**Input archive:** sources/a4d-fugu-intake-2026-09-27/

## What is integrated

The submitted files are preserved byte-for-byte with SHA-256 provenance in
the input archive. Their scripts and embedded prose were treated as source
material, not as instructions for this task; no supplied script was executed.
The old NumPy/SVD tables are evidence of the exploratory path, not exact
symbolic owners. In particular, the exploratory scripts import the absent
a4d_fugu_p1p2_check.py and cannot reproduce themselves from this submission.

The attached stationary-sheet memo is not byte-identical to the copy already
on [PR #240](https://github.com/gvakhrushev/d0_15/pull/240). The submitted
copy is archived with SHA-256
d1772fcda9d1b92cb5cd6d020c7e2f3230f560cda63fd7128c1c948217df444b. At the
checked PR #240 head 6d436488b540ae16cdb836b75539b7472001e05c, the memo blob
is 58fd42b33f0c38bd9597436873dfaf9cf80ba5b8 and contains the submitted text
plus an eight-line update: the four adjacent L=2 characters remain silent
through order u^5, the period-4 envelope does not rescue the shear jet, and
roots of unity of order greater than four remain open. The current PR body
also records the exact period-2 Fourier-support result: on even grids the
corrected shear jet has support only at the identity and
(-1,1,-1,1), so an outside root-of-unity envelope cannot cancel -432; a slow
amplitude u(hx) remains open. PR #240 is still Draft / IN_PROGRESS and not
merged, so its results remain research on an open branch, not on main.

## Canonical distinctions retained

1. **Moving metric germ.** In the accepted #270 convention,
   $d_r=z_r^{-1}-1$ and $q_0(z)=d(z)d(z)^T$ satisfy
   $C(z)q_0(z)=0$ as a Laurent identity on $(\mathbb C^\times)^4$.
   Differentiation gives
   $C\,Dq_0[\delta z]+(D C[\delta z])q_0=0$, with
   $\delta q=\delta d\,d^T+d\,\delta d^T$ and $\delta p=0$.
   This is tangent transport of a moving kernel line; it does not put
   $\delta q$ in the frozen fiber. At $z=(1,1,1,1)$ this generator is zero.

2. **Two Fourier pairings.** The holomorphic comparison
   $[A(z)\mid C(z)]$ and the physical conjugate-paired map
   $[A(z)\mid C(\bar z)]$ are different operators. The accepted #262 carrier
   has physical rank 23 on orbit types 5 and 7; the unpaired comparison has
   rank 24 there. The zero class of the special moving-germ forcing is not a
   statement that the physical cokernel itself is zero.

3. **Stress is a separate channel.** The moving-germ identity determines a
   joint motion preserving the connection equation. It does not imply
   $E_Q=0$ on a fixed metric or on every stationary sheet. The #240 shear
   witness already gives a nonzero $q_{11}$ response, while $q_0$ at that
   character has support only in slots $(00,02,22)$ and hence has zero
   pairing with that particular witness component. This one component does
   not decide the response along the full $q_0$ metric path. On a varying
   smooth background, $q_0(z)$ is a UV Fourier coefficient, not a sitewise
   field $q_0(z(x))$; the global identity alone does not give the stress.

4. **Do not merge the carriers.** The #232/Y quarter-wave family is the
   connection-only slow-lift lane and has its own response-cancellation
   controls. The 180-degree shear witness is a different connection-kernel
   polarization with a metric-response entry. The earlier RTF proposal to
   identify the sum of germ-to-anomaly ranks with a scene parameter is
   retired: the sum 11 is an untyped census total, not stress or a physical
   invariant.

5. **Three live lanes.** PR #240 owns the global realizable-response / defect
   question and is still partial. [PR #275](https://github.com/gvakhrushev/d0_15/pull/275)
   owns the separate Y slow continuation; it is Draft / BLOCKED on the
   nonlinear cross-term from PR #260. The metric-stress and physical-image
   tasks below isolate the two requested response calculations. A separate
   worker exposes the already-merged #270 `C(d)=H_AQ(d)` null identity
   coefficient by coefficient; it is an owner audit, not another response
   lane. These tasks are siblings under CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE,
   not children minted by the executor of PR #240.

6. **Old census claims are retired as evidence.** The v1-v5 phase scans,
   finite-difference derivatives, rank sum 11, and floating SVD residuals are
   not repeated or promoted. In particular, the current #240 branch corrects
   the physical rank convention and records the order-u^5 status. No new
   physics, BOOK, claim, or Lean status is asserted here. The older RTF's
   weak-average proposal through $\operatorname{im}G_5$ and its holomorphic
   $[A(z)\mid C(z)]$ joint-rank proposal are superseded as tests for the
   present question: the live physical-image task uses
   $[A(z)\mid C(\bar z)]$ and the specified $w_j$, while the stress task
   follows the $q_0$-generated metric path. They are not extra registered
   tasks.

## Registered task split

| Task | State | Purpose | Boundary |
|---|---|---|---|
| EXP-A4D-Q0-STATIONARY-SHEET-STRESS | PLANNED | Evaluate the actual metric Euler response along the real Fourier metric path generated by $q_0(z)$, with a fixed source and an explicitly continued connection-stationary sheet. | No inference from $Cq_0=0$ to zero stress; no joint-critical no-go without both Euler equations. |
| WRK-A4D-Q0-PHYSICAL-FORCING-IMAGE | PLANNED | Prove exact image/cokernel membership for $w_j=(z_j\partial_{z_j}C)q_0$ in the physical map $[A(z)\mid C(\bar z)]$ on the rank-23 orbit types. | Exact arithmetic in the #216/#262/#270 convention; no floating projector and no nonlinear stress claim. |
| WRK-A4D-HAQ-COEFFICIENTWISE-IDENTITY | PLANNED | Extract the exact linear coefficient matrices of merged #270 $C(d)=H_{AQ}(d)$ and verify all 20 cubic coefficients of $C(d)\operatorname{vec}_{sym}(dd^T)$ vanish. | Audits the existing owner coefficient by coefficient; no repeated rank/kernel proof or stress inference. |
| EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE | Existing, open Draft | Global response estimate or same-source joint-critical counterexample. | Remains the owner of the correlation-measure closure question. |
| WRK-A4D-Y-SLOW-JOINT-CONTINUATION | Existing, open Draft / BLOCKED | Y-family slow continuation. | Keep its PR #260 nonlinear N0 cross-term prerequisite; do not duplicate its germ convention. |

The planned tasks are registrations only. They are not dispatch authorization.
The metric-stress task must pin its background, source, and comparator before
execution. The exact physical-image task consumes only merged owners #216,
#262, and #270; it must report the orbit-5 claim independently on orbit 7
rather than extrapolating it.

The coefficientwise identity task consumes the merged #270 definition
`C=H_AQ` only. It complements that owner's exact zero test with an explicit
coefficient ledger; it must not substitute the separate J2 census operator
also called `HAQ` or rely on sampled torus values.

## Exact physical-image target

Use $z_5=(i,i,-i,-i)$ for orbit 5 and
$z_7=(-1,i,i,-1)$ for orbit 7, with $q_0(z)=d(z)d(z)^T$ in the owned
10-coordinate symmetric convention. For each $j=0,1,2,3$, set
$w_j=(z_j\partial_{z_j}C(z))q_0(z)$; the phase tangent differs by the scalar
$i$ and has the same image-membership status. Compare exact ranks of
$P(z)=[A(z)\mid C(\bar z)]$ and $[P(z)\mid w_j]$ over $\mathbb Q(i)$.
Report the exact Hermitian cokernel norm both for raw $q_0$ and the stated
unit normalization, so the submitted $\sqrt{8/5}$ residual can be reconciled
without changing the membership test. Do not substitute the holomorphic
$C(z)$ slot.

## Interpretation firewall

The archived discussions contain historical recommendations and commands.
They do not change the current user request, repository control plane, or task
gates. Only the exact results on merged owner branches are accepted inputs.
The PR #240 and #275 statuses above are live metadata checked during intake;
refresh them before dispatch because they can change.
