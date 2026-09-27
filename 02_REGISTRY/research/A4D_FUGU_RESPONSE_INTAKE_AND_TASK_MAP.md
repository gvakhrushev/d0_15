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
   nonlinear cross-term from PR #260. The two new tasks below isolate the
   requested metric-stress and physical-image calculations. They are
   siblings under CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE, not children minted
   by the executor of PR #240.

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
| WRK-A4D-Q0-PHYSICAL-FORCING-IMAGE | MERGED #290 | Exact cross-character cokernel and same-carrier transport terminal integrated on current main. | Carrier-mismatch diagnostic only; actual same-carrier moving germ is absorbed exactly. |
| EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE | Existing, open Draft | Global response estimate or same-source joint-critical counterexample. | Remains the owner of the correlation-measure closure question. |
| WRK-A4D-Y-SLOW-JOINT-CONTINUATION | Existing, open Draft / BLOCKED | Y-family slow continuation. | Keep its PR #260 nonlinear N0 cross-term prerequisite; do not duplicate its germ convention. |
| WRK-A4D-HAQ-COEFFICIENTWISE-IDENTITY | TERMINAL in PR #292 | Exact coefficient ledger: `C(d)=sum_r d_r C_r`; all 20 cubic 24-vectors vanish, 480 scalar equalities; Laurent substitution zero. | Owner audit only; becomes main owner on merge of #292; no stress/physical-transfer inference. |

The planned tasks are registrations only. They are not dispatch authorization.
The metric-stress task must pin its background, source, and comparator before
execution. The exact physical-image task is now completed and merged as #290. The coefficientwise worker has now completed on integration PR #292 and is
retired in that PR. Its exact coefficient ledger becomes durable main owner
only after #292 merges.

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


## CONTROL synthesis update — Veronese complex / crossing program

The mechanism-level owner for the next phase is
[A4D_VERONESE_KERNEL_COMPLEX_AND_CROSSING_PROGRAM.md](A4D_VERONESE_KERNEL_COMPLEX_AND_CROSSING_PROGRAM.md).

This update changes the research organization, not the already certified
terminals:

- #270 is read as the exact complex \(P_d\to C(d)\), with metric homology
  \(\ker C/\operatorname{im}P\) zero wherever its rank/kernel theorem applies.
- #278 retires frozen/cross-carrier detune residuals as stress evidence:
  same-carrier moving-germ forcing is absorbed exactly.
- #279 remains an exact joint-defect census but is not a divisor
  classification without a carrier-transfer theorem.
- #240's shear witness remains a joint-response witness; its identification
  with divisor homology is an open theorem.
- #260/#275 remain a separate connection-only/N0 sector.

The next mechanism theorem is not another orbit census. It is the exact
determinantal rank/homology stratification of \(C(d)\), followed by a typed
joint-defect transfer, chamber-envelope theorem, and crossing theorem.

Do not promote \(\bigcup_r\{d_r=0\}\) to the rank-jump divisor before that
exact stratification is certified.

The synthesis memo also records the exact unit-torus half-angle identity
\[
d_r=-2i\,e^{-i\theta_r/2}\sin(\theta_r/2).
\]
Use it only as an algebraic/nodal reparameterization at present: the two
half-angle sign changes cancel, so \(d_r\) and \(q_0=dd^T\) remain
single-valued on the original torus. Spinor and Kerr--Schild language is
interpretive until separate null/representation theorems are certified.


## CONTROL synthesis update — harmonic tower / N0 odd gate

The follow-up packet
[A4D_GERM_TOWER_WARD_N0_SYNTHESIS.md](A4D_GERM_TOWER_WARD_N0_SYNTHESIS.md)
reconciles the later exact carrier results with the nonlinear continuation
queue.

Execution consequences:

- merged #290 remains the owner of the physical same-carrier/cross-character
  split; the historical `8/5` residual is not reused as moving-germ stress;
- merged #296 remains the fixed-link harmonic-forcing owner and is not read as
  a contradiction to same-carrier absorption after connection continuation;
- the algebraic harmonic-tower compression `M1=0`,
  `F_n=sum_{k>=2} binom(n,k) M_k`, universal leading `M2`, and
  `sum binom(n,2)s^(n-1)=s/(1-s)^3` is now isolated as the bounded worker
  `WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT` instead of being left in chat;
- #260 is narrowed to the degree-7 odd resonant connection Euler on
  `N0=span{lambda1,lambda3,lambda4,lambda6}`; its solved degree-6 even
  correction is not reopened;
- #275 may prepare the same-source slow-response algebra in parallel and must
  block only the final substitutions that genuinely depend on the missing
  odd-7 coefficient;
- #299 should spend effort only on making the existing exact rank/cokernel
  Lean proof cheap enough to compile, not on expanding scientific scope;
- #202 keeps its own untruncated stationary-witness/no-go component and does
  not absorb the N0/germ calculation.

This update is a dependency/ownership refinement. It introduces no new
Einstein, stress, continuum, BOOK, ClaimMap, or release-status assertion.
